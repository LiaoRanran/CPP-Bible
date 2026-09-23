"""631 B1 · auto 42 条 `liveness` 字段填充执行（纯标准库）

630 A2 方案甲把 132 条 warn 分成 **auto 42 / human 90**；本工具执行 **auto 42**：

- 全部是 `claim_structured[].liveness` 字段缺失（`OBSERVATION-LIVENESS` 规则）；
- 值 = **夹具特有符号**（`{kind: fixture_symbol, symbol: <sym>}`），
  符号取自本命题**引用卡**的 `artifact_assert`，口径与 gate 相同；
- §零.14：**每条值必须有来源**。本工具在填充前**独立复核**来源
  （重新推导符号 + 确认该符号确实出现在引用卡的 artifact_assert 文本里）。

**写入安全**：
1. 填充前把每张卡原文件备份到 `data/autoimmune_backup_631/<原相对路径>`（可 `git checkout` 亦可还原）；
2. **逐行最小编辑**：只在该命题块内新增/替换 `liveness` 这一行，其余字节不动；
3. 写后立刻用 YAML 解析校验：结构除 `liveness` 外与填充前**完全一致**；
4. 填充后跑 gate（只读 `run()`）比对每张卡的 warn 数。

`--check` **只读**（不写盘、exit 0）；`--apply` 才落盘。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_auto_fill_result_631.md")
OUT_JSON = os.path.join(ROOT, "data", "autoimmune_auto_fill_631.json")
BACKUP_DIR = os.path.join(ROOT, "data", "autoimmune_backup_631")


def _ge():
    import gate_engine

    return gate_engine


def plan_auto() -> list[dict[str, Any]]:
    """630 A2 方案甲里 `mode == auto` 的条目（只读调用 630 工具）。"""
    import autoimmune_fix_proposal_630 as P

    items = P.plan_a()["items"]
    return [i for i in items if i.get("mode") == "auto"]


def verify_source(item: dict[str, Any]) -> dict[str, Any]:
    """独立复核填充值的来源：符号必须出现在本命题引用卡的 artifact_assert 里。

    两步：①用 630 的同口径函数重新推导一次（防"方案与实现漂移"）；
    ②在引用卡的**原文**里逐字符找该符号（防"推导函数自身 bug"）。
    """
    import autoimmune_fix_proposal_630 as P

    ge = _ge()
    card = os.path.join(ROOT, item["card_rel"])
    sym = ((item.get("value") or {}).get("symbol") or "").strip()
    if not sym or not os.path.exists(card):
        return {"ok": False, "reason": "无符号或卡不存在"}
    try:
        prop = _prop_of(card, item["prop_id"])
    except Exception:                                          # noqa: BLE001
        prop = {}
    ev_idx = ge._ev_index()
    redriven = P.suggest_liveness_symbol(prop, ev_idx)
    if redriven != sym:
        return {"ok": False, "reason": f"重推导不一致（{redriven} != {sym}）"}
    # ②原文里逐字符确认
    refs = [str(r).strip() for r in ge._as_list(prop.get("evidence")) if str(r).strip()]
    ev_dir = os.path.join(ROOT, "evidence")
    found_in = []
    for r in refs:
        for base, _d, files in os.walk(ev_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                p = os.path.join(base, f)
                txt = open(p, encoding="utf-8", errors="replace").read()
                if f"id: {r}" in txt and sym in txt:
                    found_in.append(os.path.relpath(p, ROOT))
    return {"ok": bool(found_in), "symbol": sym, "refs": refs,
            "found_in": sorted(set(found_in))[:3],
            "reason": "" if found_in else f"引用卡原文未出现符号 {sym}"}


def _frontmatter_bounds(lines: list[str]) -> tuple[int, int]:
    """返回 (start, end)：frontmatter 内容行的下标区间（`---` 之间的行）。"""
    if not lines or lines[0].strip() != "---":
        return (0, 0)
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (1, i)
    return (1, len(lines))


def _prop_of(path: str, prop_id: str) -> dict[str, Any]:
    """从卡里取出指定命题（用 gate 的解析，避免自造 YAML 方言）。"""
    import autoimmune_diagnose_630 as D

    return D.prop_of(path, prop_id)


def _prop_block(lines: list[str], start: int, end: int,
                prop_id: str) -> Optional[tuple[int, int]]:
    """在 frontmatter 区间内找 `- id: <prop_id>` 块的行范围（含起行）。"""
    i = start
    while i < end:
        if lines[i].rstrip("\r\n") == f"  - id: {prop_id}":
            j = i + 1
            while j < end and not lines[j].startswith("  - id:") \
                    and not (lines[j].startswith("  ") and not lines[j].startswith("   ")):
                j += 1
            return (i, j)
        i += 1
    return None


def liveness_line(symbol: str) -> str:
    return f"    liveness: {{kind: fixture_symbol, symbol: {symbol}}}"


def edit_for_lines(lines: list[str], prop_id: str,
                   symbol: str) -> Optional[dict[str, Any]]:
    """对**给定文本行**算出一条最小编辑（纯函数，便于幂等与单测）。

    - 已存在 `liveness:` ⇒ `replace`（幂等：重复施加不会插第二行）；
    - 否则插到该命题块内**最后一个键行**之后（避免插进多行 `statement` 中间）。
    """
    s, e = _frontmatter_bounds(lines)
    blk = _prop_block(lines, s, e, prop_id)
    if not blk:
        return None
    b0, b1 = blk
    for k in range(b0, b1):
        if lines[k].startswith("    liveness:"):
            return {"mode": "replace", "line": k, "text": liveness_line(symbol)}
    last = b0
    for k in range(b0, b1):
        if lines[k].startswith("    ") and not lines[k].startswith("     "):
            last = k
    return {"mode": "insert_after", "line": last, "text": liveness_line(symbol)}


def intended_edits(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """算出**待施加的最小行编辑**（不落盘）。"""
    out = []
    for it in items:
        card = os.path.join(ROOT, it["card_rel"])
        if not os.path.exists(card):
            out.append({**it, "edit": None, "reason": "卡不存在"})
            continue
        lines = open(card, encoding="utf-8").read().split("\n")
        sym = ((it.get("value") or {}).get("symbol") or "").strip()
        ed = edit_for_lines(lines, it["prop_id"], sym)
        out.append({**it, "edit": ed, "symbol": sym,
                    "reason": "" if ed else "未找到命题块"})
    return out


def apply_edit_to_text(text: str, edit: dict[str, Any]) -> str:
    """把一条编辑施加到**文本**（纯函数，便于单测与试算）。"""
    lines = text.split("\n")
    mode, idx = edit["mode"], int(edit["line"])
    if mode == "replace":
        lines[idx] = edit["text"]
    else:
        lines.insert(idx + 1, edit["text"])
    return "\n".join(lines)


def _parse(text: str) -> dict[str, Any]:
    import yaml

    head = text.split("\n---", 1)[0]
    return yaml.safe_load(head.replace("---\n", "", 1)) or {}


def diff_structure(before: str, after: str) -> list[str]:
    """比较前后 frontmatter 结构，只报告**非 liveness 的差异**（liveness 变化是预期改动）。

    返回 `[]` = 安全：除目标字段外零副作用。
    """
    b, a = _parse(before), _parse(after)
    for d in (b, a):
        for p in (d.get("claim_structured") or []):
            if isinstance(p, dict):
                p.pop("liveness", None)
    if b == a:
        return []
    diffs = []
    for key in sorted({*b, *a}):
        if b.get(key) != a.get(key):
            diffs.append(f"{key} 变化")
    return diffs or ["结构不一致（细节未定位）"]


def measure_warns() -> dict[str, Any]:
    """跑 gate（只读 import run()）统计各卡 warn 数。"""
    import autoimmune_rate_framework as F

    m = F.measure()
    return {"clean_cards": m["total"], "warned": m["warned_count"],
            "rate_pct": round(m["rate"] * 100, 1),
            "per_card": {c["card"]: c["warn_rules"] for c in m.get("cards", [])}
            if "cards" in m else {}}


def apply(items: Optional[list[dict[str, Any]]] = None,
          dry_run: bool = False) -> dict[str, Any]:
    """落盘填充（含备份 + 写后结构校验）。"""
    items = items if items is not None else plan_auto()
    edits = [e for e in intended_edits(items) if e.get("edit")]
    skipped = [e for e in intended_edits(items) if not e.get("edit")]
    by_card: dict[str, list[dict[str, Any]]] = {}
    for e in edits:
        by_card.setdefault(e["card_rel"], []).append(e)
    results, diffs = [], []
    for rel, es in sorted(by_card.items()):
        card = os.path.join(ROOT, rel)
        before = open(card, encoding="utf-8").read()
        after = before
        # 逐条施加（行号会因插入而右移 ⇒ 从**后往前**施加）
        for e in sorted(es, key=lambda x: -int(x["edit"]["line"])):
            after = apply_edit_to_text(after, e["edit"])
        d = diff_structure(before, after)
        if d:
            diffs.append({"card": rel, "diff": d})
            results.append({"card": rel, "applied": 0, "skipped_reason": d})
            continue
        if not dry_run:
            bak = os.path.join(BACKUP_DIR, rel)
            os.makedirs(os.path.dirname(bak), exist_ok=True)
            if not os.path.exists(bak):
                shutil.copy2(card, bak)
            with open(card, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(after)
        results.append({"card": rel, "applied": len(es),
                        "symbols": [e["symbol"] for e in es]})
    return {"dry_run": dry_run, "cards": len(by_card), "edits": len(edits),
            "skipped": [{"card": s["card_rel"], "reason": s.get("reason")}
                        for s in skipped],
            "results": results, "unexpected_diffs": diffs}


def write_report(fill: Optional[dict[str, Any]] = None,
                 after: Optional[dict[str, Any]] = None) -> str:
    items = plan_auto()
    sources = [verify_source(i) for i in items]
    ok_src = sum(1 for s in sources if s["ok"])
    fill = fill or {"dry_run": True, "cards": 0, "edits": 0}
    lines = [
        "# 631 B1 · auto 42 条 liveness 字段填充结果", "",
        f"- 方案来源：630 A2 方案甲（`mode == auto`）：**{len(items)} 条**",
        f"- 来源独立复核：**{ok_src}/{len(sources)}** 条通过"
        "（重推导符号一致 + 引用卡原文出现该符号）",
        f"- 填充：`--apply` 已改 **{fill.get('cards', 0)}** 张卡 / "
        f"**{fill.get('edits', 0)}** 处（dry_run={fill.get('dry_run')}）",
        "- 备份目录：`data/autoimmune_backup_631/`（原文件逐张留档）", "",
        "## 一、填了什么（按卡汇总）", "",
        "| 卡 | 填充处数 | 符号 |", "|---|---|---|",
    ]
    for r in fill.get("results", []):
        syms = "、".join(f"`{s}`" for s in r.get("symbols", []))
        lines.append(f"| `{r['card']}` | {r.get('applied', 0)} | {syms or '—'} |")
    lines += ["", "## 二、来源复核（每条值的出处）", "",
              "| # | 卡 / 命题 | 符号 | 引用卡 | 复核 |", "|---|---|---|---|---|"]
    for i, (it, s) in enumerate(zip(items, sources), 1):
        lines.append(f"| {i} | `{it['card_id']}` / {it['prop_id']} | "
                     f"`{s.get('symbol', '—')}` | "
                     f"{'，'.join(s.get('found_in', [])) or '—'} | "
                     f"{'✅' if s['ok'] else '❌ ' + s.get('reason', '')} |")
    lines += ["", "## 三、填充后自身免疫率复算", ""]
    if after:
        lines += [f"- 干净卡：{after['clean_cards']} 张；仍被 warn："
                  f"**{after['warned']}** 张 ⇒ 自身免疫率 **{after['rate_pct']}%**", ""]
    else:
        lines += ["> 未复算（需 `--apply` 后跑 gate）。", ""]
    lines += [
        "## 四、诚实登记", "",
        "1. **只填 `liveness`**：`object`（语义）与 `signed_by`（人签）**一条没填**"
        "（§零.3 不代签、机器不做语义判断）；",
        "2. **写入方式是逐行最小编辑**：改前备份 + 改后用 YAML 结构比对，"
        "确认除 `liveness` 外零变化（`unexpected_diffs` 为空）；",
        "3. 符号取自**引用卡的 artifact_assert**，与 gate 判定 `OBSERVATION-LIVENESS` "
        "的口径一致；但「符号存在」**不等于**「该符号确为本命题的观测证据」——"
        "语义正确性仍需人复核（B2 清单的 human 项不含这些，但建议抽检）；",
        "4. 若填充后 warn 数未下降，如实记录（见 §三 与验收报告偏差表）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"items": items, "sources": sources, "fill": fill,
                   "after": after}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    items = plan_auto()
    chk("auto 条目 = 42 条且字段全是 liveness", len(items) == 42
        and all(i["field"] == "liveness" for i in items), f"({len(items)})")
    srcs = [verify_source(i) for i in items]
    chk("每条值都能追溯来源（引用卡 artifact_assert）",
        all(s["ok"] for s in srcs),
        f"({sum(1 for s in srcs if not s['ok'])} 条失败)")
    # 试算（不落盘）：编辑必须可施加且结构零副作用
    trial = apply(items, dry_run=True)
    chk("试算：无意外结构差异", not trial["unexpected_diffs"],
        f"({trial['unexpected_diffs'][:2]})")
    chk("试算：覆盖 23 张卡 / 42 处", trial["cards"] == 23 and trial["edits"] == 42,
        f"({trial['cards']}/{trial['edits']})")
    # 纯函数：编辑文本的行编辑可重复（幂等：已存在 liveness 时改为 replace）
    chk("幂等：对已含 liveness 的文本改为 replace（不重复插入）",
        _edit_mode_of_filled(items) == "replace")
    chk("报告存在", os.path.exists(OUT_MD))

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain", "--", "atoms"],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    plan_auto()
    intended_edits(items)
    apply(items, dry_run=True)
    chk("只读：--check 路径不改受控目录", snap() == before)
    print(f"B1 auto fill check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _edit_mode_of_filled(items: list[dict[str, Any]]) -> str:
    """把第一条编辑施加到文本后，再算一次 ⇒ 应变为 replace（幂等性佐证）。"""
    e = [x for x in intended_edits(items) if x.get("edit")]
    if not e:
        return "none"
    first = e[0]
    card = os.path.join(ROOT, first["card_rel"])
    text = open(card, encoding="utf-8").read()
    filled = apply_edit_to_text(text, first["edit"])
    # 对**已填过的文本**再算一次 ⇒ 必须变成 replace（否则会重复插入）
    again = edit_for_lines(filled.split("\n"), first["prop_id"], first["symbol"])
    return again["mode"] if again else "none"


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 B1 auto 42 条填充")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘）")
    ap.add_argument("--apply", action="store_true", help="落盘填充（含备份）")
    ap.add_argument("--report", action="store_true", help="写结果报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.apply:
        res = apply(dry_run=False)
        after = measure_warns()
        print(json.dumps({"fill": res, "after": after}, ensure_ascii=False, indent=2))
        write_report(res, after)
        print(f"written {OUT_MD}")
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    items = plan_auto()
    if args.json:
        print(json.dumps(intended_edits(items), ensure_ascii=False, indent=2))
        return 0
    print(f"auto_items={len(items)} cards={len({i['card_rel'] for i in items})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
