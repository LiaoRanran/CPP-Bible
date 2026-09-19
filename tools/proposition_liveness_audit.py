#!/usr/bin/env python3
"""607 任务 2 · 命题活性锚审计（**只读**）。

问题：gate 的 `OBSERVATION-LIVENESS` 规则要求 observation 命题在**命题级**指认证伪锚
（`claim_structured[*].liveness = {kind: fixture_symbol, symbol: <夹具符号>}`），
否则每次 `gate_engine.py --check` 都出 warn。但"哪些缺、哪些有、哪些**根本不该**有"此前没有任何
清单 ⇒ 谁也无法推进。本工具产出**人审清单**。

三条硬边界（本工具的价值全在"不做"这三件事上）：
  1. **只读**：不写任何命题卡，**不自动补** `liveness`（补不补是人审权力）；
  2. 不改 `gate_engine.py`（判据的原作者），本工具只是把它的判据**清单化**；
  3. 纯标准库（frontmatter 解析子集照 `gate_engine._meta` 的现有写法自实现，不 import CORE，
     也不依赖 PyYAML —— 与 gate 保持**松耦合**，避免"工具改了判据也跟着变"的假一致）。

**口径与 gate 的对应**（不重复实现判决，只列清单）：
  * `missing`：observation 且**没有** `liveness` ⇒ gate 必报 warn；
  * `missing_symbol`：`kind: fixture_symbol` 但 `symbol` 空 ⇒ gate 同样不认（报 warn）；
  * `unknown_kind`：`kind` 非 `fixture_symbol`/`external_basis` ⇒ gate 不认，人审该填什么；
  * `needs_review`：`kind: external_basis` 的 observation —— 活性不由**单一工件**给出
    （靠外部标准/权威源背书），故它**无法被 replay 证伪**，任务书要求单独列出，
    供人审决定"改标 inference / 或补一条夹具级锚"；
  * `ok`：`kind: fixture_symbol` 且 `symbol` 非空。
  * inference 命题**不进**任何异常分类（gate 只对 observation 要求命题级锚）。

用法：
  python tools/proposition_liveness_audit.py --check    # 审计 + 写 data/proposition_liveness_audit.md（exit 0）
  python tools/proposition_liveness_audit.py --json     # JSON 到 stdout（不写报告）
  # 测试注入钩子（默认真实仓）：
  #   --atoms-root <dir>   只扫该目录     --report <path>  报告落盘位置
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATOMS_ROOT = ROOT / "atoms"
REPORT_PATH = ROOT / "data" / "proposition_liveness_audit.md"

#: observation 命题的状态分类（`ok` 之外全是"人审清单"，不是自动判决）
STATUSES: tuple[str, ...] = ("ok", "missing", "missing_symbol", "needs_review", "unknown_kind")

_ITEM_RX = re.compile(r"^(\s*)-\s+(.*)$")
_KEY_RX = re.compile(r"^(\s*)([^:\s][^:]*):\s?(.*)$")


# ── frontmatter 子集解析（照 gate_engine._meta / replay.parse_frontmatter 的写法）────────
def extract_frontmatter(text: str) -> str | None:
    """取 `---` 包裹的 frontmatter 文本；不是标准卡则返回 None。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    return text[3:end].strip("\n")


def _scalar(raw: str):
    """标量子集：内联列表 `[a, b]` / 引号串 / 裸串。"""
    v = raw.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [_scalar(x) for x in inner.split(",")] if inner else []
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        body = v[1:-1]
        if v[0] == '"':
            body = body.replace('\\"', '"').replace("\\\\", "\\")
        return body
    return v


def _text_of(prop: dict, key: str) -> str:
    v = prop.get(key)
    if isinstance(v, (dict, list)):
        return ""
    return str(v or "").strip()


def parse_claim_items(fm: str) -> list[dict]:
    """解析顶层 `claim_structured:` 的列表项（每项一个 dict；嵌套块（如 `liveness:`）进子 dict）。

    只认"缩进 0 的 `claim_structured:` + 其下更深缩进"的块；遇到下一个缩进 0 的键即结束。
    块标量（`>-` / `|`）按后续更深缩进行消费，避免把续行误当键。
    """
    lines = fm.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("claim_structured:"):
            start = i + 1
            break
    if start is None:
        return []
    items: list[dict] = []
    cur: dict | None = None
    item_indent: int | None = None
    nested: dict | None = None
    nested_indent = -1
    block_indent = -1          # >0 ⇒ 正在消费块标量的续行
    for ln in lines[start:]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        indent = len(ln) - len(ln.lstrip(" "))
        if indent == 0:
            break                                   # 回到顶层键 ⇒ 块结束
        if block_indent > 0 and indent > block_indent:
            continue                                # 块标量续行（内容不参与分类）
        block_indent = -1
        m = _ITEM_RX.match(ln)
        if m and (item_indent is None or len(m.group(1)) == item_indent):
            cur = {"_nested": {}}
            items.append(cur)
            item_indent = len(m.group(1))
            nested, nested_indent = None, -1
            rest = m.group(2).strip()
            if rest:
                k, _, v = rest.partition(":")
                cur[k.strip()] = _scalar(v)
            continue
        if cur is None:
            continue
        mk = _KEY_RX.match(ln)
        if not mk:
            continue
        key, raw = mk.group(2).strip(), mk.group(3)
        if nested is not None and indent > nested_indent:
            nested[key] = _scalar(raw)
            continue
        if not raw.strip():                         # 空值 ⇒ 可能是嵌套块或块标量
            nxt = {}
            cur[key] = nxt
            nested, nested_indent = nxt, indent
            continue
        if raw.strip() in (">-", ">", "|", "|-"):    # 块标量 ⇒ 消费更深缩进的续行
            block_indent = indent
            cur[key] = ""
            nested, nested_indent = None, -1
            continue
        cur[key] = _scalar(raw)
        nested, nested_indent = None, -1
    for it in items:
        it.pop("_nested", None)
    return items


# ── 分类 ──────────────────────────────────────────────────────────────────────
def classify(prop: dict) -> dict:
    """给一个命题打状态。返回 {claim_type, has_liveness, kind, symbol, status}。"""
    ct = _text_of(prop, "claim_type") or "unknown"
    lv = prop.get("liveness")
    has_lv = isinstance(lv, dict) and bool(lv)
    kind = _text_of(lv, "kind") if isinstance(lv, dict) else ""
    symbol = _text_of(lv, "symbol") if isinstance(lv, dict) else ""
    if ct != "observation":
        status = "n/a"                              # gate 只对 observation 要求命题级锚
    elif not has_lv:
        status = "missing"
    elif kind == "external_basis":
        status = "needs_review"
    elif kind == "fixture_symbol":
        status = "ok" if symbol else "missing_symbol"
    else:
        status = "unknown_kind"
    return {"claim_type": ct, "has_liveness": has_lv, "kind": kind, "symbol": symbol,
            "status": status}


def audit(atoms_root: Path | None = None) -> dict:
    """扫描命题卡并汇总。**只读**：不写卡、不补字段。"""
    root = Path(atoms_root) if atoms_root else ATOMS_ROOT
    if not root.is_dir():
        raise FileNotFoundError(f"命题卡目录不存在：{root}")
    props_total = obs = inf = other = 0
    lv_with = 0
    by_kind: dict[str, int] = {}
    obs_status = {s: 0 for s in STATUSES}
    cards: list[dict] = []
    unparsed: list[str] = []
    for card in sorted(root.rglob("*.md")):
        text = card.read_text(encoding="utf-8", errors="replace")
        fm = extract_frontmatter(text)
        if fm is None:
            continue                                # 非标准卡（无 frontmatter）⇒ 不进分母
        items = parse_claim_items(fm)
        if not items:
            continue
        card_id = card.stem
        for ln in fm.split("\n"):
            if ln.startswith("id:"):
                card_id = ln[3:].strip() or card_id
                break
        missing_here: list[dict] = []
        review_here: list[dict] = []
        for p in items:
            rec = classify(p)
            props_total += 1
            if rec["claim_type"] == "observation":
                obs += 1
                obs_status[rec["status"]] = obs_status.get(rec["status"], 0) + 1
            elif rec["claim_type"] == "inference":
                inf += 1
            else:
                other += 1
                unparsed.append(f"{card_id} :: claim_type={rec['claim_type']}")
            if rec["has_liveness"]:
                lv_with += 1
                by_kind[rec["kind"] or "(空)"] = by_kind.get(rec["kind"] or "(空)", 0) + 1
            if rec["status"] in ("missing", "missing_symbol", "unknown_kind"):
                missing_here.append({"id": _text_of(p, "id") or "?", "status": rec["status"],
                                     "kind": rec["kind"], "symbol": rec["symbol"],
                                     "statement": _text_of(p, "statement"),
                                     "evidence": p.get("evidence") if isinstance(p.get("evidence"), list) else []})
            if rec["status"] == "needs_review":
                review_here.append({"id": _text_of(p, "id") or "?", "kind": rec["kind"],
                                    "symbol": rec["symbol"],
                                    "statement": _text_of(p, "statement"),
                                    "evidence": p.get("evidence") if isinstance(p.get("evidence"), list) else []})
        if missing_here or review_here:
            cards.append({"card": card_id, "path": card.relative_to(root.parent).as_posix()
                          if root.parent in card.parents else card.as_posix(),
                          "missing": missing_here, "needs_review": review_here})
    return {
        "audited_at": datetime.now().isoformat(timespec="seconds"),
        "atoms_root": (root.relative_to(ROOT).as_posix() if root.is_relative_to(ROOT) else root.as_posix()),
        "propositions": {"total": props_total, "observation": obs, "inference": inf, "other": other},
        "liveness": {"with": lv_with, "without": props_total - lv_with, "by_kind": by_kind},
        "observation_status": obs_status,
        # 两个计数**分开**：`missing_cards` 只数"真有缺锚条目"的卡（§4 标题要与列出的卡对得上），
        # `review_cards` 只数"只有 needs_review"的卡；混用一个数会让标题虚高。
        "missing_cards": sum(1 for c in cards if c["missing"]),
        "review_cards": sum(1 for c in cards if c["needs_review"]),
        "cards": cards,
        "note": ("只读审计：不修改命题卡、不自动补 liveness（人审权力）；不做语义判断，"
                 "只按 gate `OBSERVATION-LIVENESS` 的判据列清单。"),
    }


# ── 报告 ──────────────────────────────────────────────────────────────────────
def _short(s: str, n: int = 60) -> str:
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[:n] + "…"


def render_markdown(res: dict) -> str:
    p, lv, st = res["propositions"], res["liveness"], res["observation_status"]
    out: list[str] = []
    out.append("# 命题活性锚审计（607 任务 2 · 只读）")
    out.append("")
    out.append(f"> 生成时间：{res['audited_at']} ｜ 扫描面：`{res['atoms_root']}` ｜ "
               "命令：`python tools/proposition_liveness_audit.py --check`")
    out.append(">")
    out.append("> **本报告是人审清单，不是自动判决**：工具只按 gate `OBSERVATION-LIVENESS` 的判据"
               "（observation 命题须有 `liveness.kind=fixture_symbol` 且 `symbol` 非空）列清单，"
               "**不自动补字段**、**不改任何卡**、不做语义判断。")
    out.append("")
    out.append("## 1 · 总览")
    out.append("")
    out.append("| 指标 | 数量 |")
    out.append("|---|---|")
    out.append(f"| 命题总数 | **{p['total']}** |")
    out.append(f"| └ observation | **{p['observation']}** |")
    out.append(f"| └ inference | **{p['inference']}** |")
    out.append(f"| └ 其它/未知 `claim_type` | {p['other']} |")
    out.append(f"| 含 `liveness` 字段的命题 | **{lv['with']}** |")
    out.append(f"| 不含 `liveness` 的命题 | {lv['without']} |")
    out.append("")
    out.append("**observation 命题的状态分布**（`ok` 之外都是待办/待审）：")
    out.append("")
    out.append("| 状态 | 数量 | 含义 |")
    out.append("|---|---|---|")
    out.append(f"| `ok` | **{st.get('ok', 0)}** | `kind: fixture_symbol` 且 `symbol` 非空（gate 不报 warn） |")
    out.append(f"| `missing` | **{st.get('missing', 0)}** | 无 `liveness` ⇒ gate 报 warn |")
    out.append(f"| `missing_symbol` | {st.get('missing_symbol', 0)} | `kind: fixture_symbol` 但 `symbol` 空 ⇒ gate 同样报 warn |")
    out.append(f"| `unknown_kind` | {st.get('unknown_kind', 0)} | "
               "`kind` 不在 `fixture_symbol` / `external_basis` 内 ⇒ 人审该填什么 |")
    out.append(f"| `needs_review` | **{st.get('needs_review', 0)}** | `kind: external_basis` 的 observation（见 §3） |")
    out.append("")
    out.append("## 2 · 已有 `liveness` 的命题（按 kind 分组）")
    out.append("")
    if lv["by_kind"]:
        out.append("| kind | 数量 |")
        out.append("|---|---|")
        for k in sorted(lv["by_kind"]):
            out.append(f"| `{k}` | {lv['by_kind'][k]} |")
    else:
        out.append("**0 条**：全库没有任何命题填过 `liveness`（因此下面的清单 = 全部 observation）。")
    out.append("")
    out.append(f"## 3 · `needs_review` 清单（`kind: external_basis` 的 observation，共 {st.get('needs_review', 0)} 条）")
    out.append("")
    out.append("含义：该命题的活性来自**外部标准/权威源**背书，而非**单一工件** ⇒ replay 无法证伪它，"
               "任务书要求单列，供人审决定「改标 inference」或「补夹具级锚」。")
    out.append("")
    if st.get("needs_review", 0):
        out.append("| 卡 | 命题 id | 说明 |")
        out.append("|---|---|---|")
        for c in res["cards"]:
            for e in c["needs_review"]:
                out.append(f"| `{c['card']}` | `{e['id']}` | {_short(e['statement'])} |")
    else:
        out.append("（空）")
    out.append("")
    out.append(f"## 4 · 缺 liveness 清单（按卡分组，共 {sum(len(c['missing']) for c in res['cards'])} 条 / "
               f"{res['missing_cards']} 卡）")
    out.append("")
    out.append("> 字段说明：本仓命题卡**没有 `brief` 字段**（任务书写的 `brief` 在本仓对应 `statement`），"
               "故此处取 `statement` 前 60 字；JSON 输出里有全文。")
    out.append("")
    if res["cards"]:
        for c in res["cards"]:
            if not c["missing"]:
                continue
            out.append(f"### `{c['card']}`（{len(c['missing'])} 条）")
            out.append("")
            out.append("| 命题 id | 状态 | 证据 | 内容（截断） |")
            out.append("|---|---|---|---|")
            for e in c["missing"]:
                ev = ", ".join(str(x) for x in (e["evidence"] or [])) or "—"
                st_mark = {"missing": "缺 `liveness`", "missing_symbol": "`symbol` 空",
                           "unknown_kind": f"未知 kind `{e['kind']}`"}.get(e["status"], e["status"])
                out.append(f"| `{e['id']}` | {st_mark} | {ev} | {_short(e['statement'])} |")
            out.append("")
    else:
        out.append("（空：无 observation 命题缺锚）")
    out.append("")
    out.append("## 5 · 口径与边界（诚实）")
    out.append("")
    out.append("- **不补字段**：`liveness` 填什么是人审权力（要判「哪个夹具符号真能证伪这条命题」）；"
               "本工具只列清单。")
    out.append("- **不做语义判断**：`needs_review` 只由 `kind == external_basis` 触发；"
               "工具不会去「理解」某条 observation 是否其实该叫 inference。")
    out.append("- **与 gate 松耦合**：本工具不 import `gate_engine`/`atom_evidence_replay`，"
               "frontmatter 解析子集自实现 ⇒ 两边判据若漂移，本报告**不会**自动跟着变（这种漂移必须由人发现）。")
    out.append("- **计数口径**：只统计**有 `claim_structured`** 的卡；无命题结构的卡不进分母。"
               "`claim_type` 非 observation/inference 的进 `其它/未知`，并列出卡 id。")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="607 · 命题活性锚审计（只读）")
    ap.add_argument("--check", action="store_true", help="跑审计 + 写报告（exit 0）")
    ap.add_argument("--json", action="store_true", help="JSON 输出到 stdout（不写报告）")
    ap.add_argument("--atoms-root", default=None, help="测试注入：只扫该目录")
    ap.add_argument("--report", default=None, help="测试注入：报告落盘位置")
    a = ap.parse_args(argv)
    try:
        res = audit(Path(a.atoms_root) if a.atoms_root else None)
    except (FileNotFoundError, OSError) as exc:
        print(f"[liveness] ❌ {exc}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    path = Path(a.report) if a.report else REPORT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(res), encoding="utf-8")
    p, st = res["propositions"], res["observation_status"]
    print(f"[liveness] 审计完成：命题 {p['total']}（observation {p['observation']} / "
          f"inference {p['inference']}）｜有 liveness 的命题 {res['liveness']['with']}")
    print(f"[liveness] observation 状态：ok={st.get('ok', 0)} missing={st.get('missing', 0)} "
          f"missing_symbol={st.get('missing_symbol', 0)} unknown_kind={st.get('unknown_kind', 0)} "
          f"needs_review={st.get('needs_review', 0)}")
    print(f"[liveness] 缺 liveness：{sum(len(c['missing']) for c in res['cards'])} 条 / "
          f"{res['missing_cards']} 卡 ⇒ {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
