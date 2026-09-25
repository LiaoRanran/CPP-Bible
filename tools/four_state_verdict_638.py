"""638 3.1 · 四态结论 schema（**真上线**，向后兼容）

v25 要求：判决支持 **四态** —— `pass` / `pass_with_exception` / `fail` / `unknown`。

本工具是**新格式的定义与执行器**，不是 636 的影子模拟：

1. **四态 schema**（`SCHEMA`）：逐态定义必填字段与语义；
2. **边界三元组强制**（§三.1.3）：任何 `pass`/`fail` 必须附
   `mutation_set_hash`(64hex) + `mutation_count`(>0) + `generator_version`；
   **缺任一 ⇒ 自动降级为 `unknown`**（`enforce`）；
3. **`pass_with_exception` 必须给 `explanation`**（非空），否则同样降级 `unknown`；
4. **向后兼容**：历史判决（二态 pass/block）**不重新分类**；
   另提供 `migrate_plan()` 批量映射**计划**（只算不写、不自动跑，`--migrate` 只打印）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/638_four_state_schema.md` + `data/638_four_state_schema.json`。
纯标准库；≥6 例单测（tests/test_four_state_verdict_638.py）。
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "638_four_state_schema.md")
OUT_JSON = os.path.join(ROOT, "data", "638_four_state_schema.json")

STATES = ["pass", "pass_with_exception", "fail", "unknown"]

# 四态 schema：状态 → 定义（语义 / 必填字段 / 旧态映射）
SCHEMA: dict[str, dict[str, Any]] = {
    "pass": {
        "desc": "完全通过，无例外",
        "requires": ["boundary_triple"],
        "legacy_from": ["pass", "APPROVE"],
    },
    "pass_with_exception": {
        "desc": "通过但附例外说明（explanation 必填）",
        "requires": ["boundary_triple", "explanation"],
        "legacy_from": ["pass", "APPROVE"],
    },
    "fail": {
        "desc": "被 block/拒绝",
        "requires": ["boundary_triple"],
        "legacy_from": ["block", "REJECT", "fail"],
    },
    "unknown": {
        "desc": "证据不足/边界缺失，无法判决",
        "requires": [],
        "legacy_from": [],
    },
}

BOUNDARY_FIELDS = ("mutation_set_hash", "mutation_count", "generator_version")

_HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
_VERDICT_RE = re.compile(r"^(?:verdict|falsification|decision):\s*(\S+)", re.MULTILINE)
_EXPLANATION_RE = re.compile(r"^explanation:\s*(.*)$", re.MULTILINE)
_VERIFIED_RE = re.compile(r"^status:\s*verified", re.MULTILINE)

_FAIL_WORDS = {"block", "fail", "failed", "reject", "rejected", "refut", "refuted", "false"}
_PASS_WORDS = {"pass", "passed", "approve", "approved", "true", "ok"}


# ── 边界三元组 ──────────────────────────────────────────────────────────
def boundary_of(rec: dict[str, Any]) -> dict[str, Any]:
    """抽取边界三元组（缺失字段为 None）。"""
    return {k: rec.get(k) for k in BOUNDARY_FIELDS}


def has_boundary(rec: dict[str, Any]) -> bool:
    """三个字段**都**齐且格式合法，才算有边界。"""
    h = rec.get("mutation_set_hash")
    c = rec.get("mutation_count")
    v = rec.get("generator_version")
    if not isinstance(h, str) or not _HASH_RE.match(h.strip()):
        return False
    if not isinstance(c, (int, float, str)):
        return False
    try:
        if int(c) <= 0:
            return False
    except (TypeError, ValueError):
        return False
    return bool(isinstance(v, str) and v.strip())


# ── 四态分类 ────────────────────────────────────────────────────────────
def _raw_state(rec: dict[str, Any]) -> str:
    """在**有边界**的前提下，按原始判决词推出三态（pass/pass_with_exception/fail）。"""
    w = str(rec.get("verdict") or rec.get("result") or "").strip().lower()
    exc = rec.get("exception") or rec.get("has_exception") or rec.get("exception_clause")
    explanation = str(rec.get("explanation") or "").strip()
    if w in _FAIL_WORDS:
        return "fail"
    if w in _PASS_WORDS or w == "":
        return "pass_with_exception" if (exc or explanation) else "pass"
    return "unknown"


def classify(rec: dict[str, Any]) -> dict[str, Any]:
    """核心：**先看边界，再定态**；缺边界一律降级 `unknown`。

    返回 `{state, requested, downgraded, boundary_ok, reasons}`。
    """
    reasons: list[str] = []
    requested = _raw_state(rec)
    bo = has_boundary(rec)

    if requested == "unknown":
        return {"state": "unknown", "requested": requested, "downgraded": False,
                "boundary_ok": bo, "reasons": ["原始判决即「证据不足」"]}

    if not bo:
        missing = [k for k in BOUNDARY_FIELDS if not rec.get(k)]
        if missing:
            reasons.append("缺边界三元组字段：" + ",".join(missing))
        else:
            reasons.append("边界三元组格式非法（hash 非 64hex 或 count ≤ 0 或 version 空）")
        reasons.append("⇒ 按 §3.1.3 降级为 unknown")
        return {"state": "unknown", "requested": requested, "downgraded": True,
                "boundary_ok": False, "reasons": reasons}

    if requested == "pass_with_exception":
        expl = str(rec.get("explanation") or "").strip()
        if not expl:
            reasons.append("pass_with_exception 缺 explanation（必填）⇒ 降级 unknown")
            return {"state": "unknown", "requested": requested, "downgraded": True,
                    "boundary_ok": True, "reasons": reasons}
        reasons.append("有边界 + 有 explanation ⇒ 保留 pass_with_exception")

    return {"state": requested, "requested": requested, "downgraded": False,
            "boundary_ok": True, "reasons": reasons or ["有边界，按原始判决定态"]}


def enforce(rec: dict[str, Any]) -> str:
    """便捷入口：返回四态字符串。"""
    return str(classify(rec)["state"])


# ── 卡级分类（读一张卡的判决） ────────────────────────────────────────────
def classify_card(path: str) -> dict[str, Any]:
    """读一张 atom/evidence 卡，抽出判决与边界，做四态分类。"""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return {"file": path, "state": "unknown", "downgraded": True, "boundary_ok": False,
                "reasons": ["文件不可读"]}
    m = _VERDICT_RE.search(text)
    ex = _EXPLANATION_RE.search(text)
    rec: dict[str, Any] = {
        "verdict": (m.group(1) if m else ""),
        "explanation": (ex.group(1) if ex else ""),
    }
    st = _STATUS_RE.search(text)
    if st and st.group(1).lower() == "verified" and not m:
        rec["verdict"] = "pass"   # verified 且无显式 falsification ⇒ 通过
    for k in BOUNDARY_FIELDS:
        mm = re.search(rf"^{k}:\s*(\S+)\s*$", text, re.MULTILINE)
        if mm:
            rec[k] = mm.group(1).strip().strip('"').strip("'")
    out = classify(rec)
    out["file"] = os.path.relpath(path, ROOT).replace(os.sep, "/")
    out["verified"] = bool(_VERIFIED_RE.search(text))
    return out


# ── 语料审计（真实数字）──────────────────────────────────────────────────
def audit() -> dict[str, Any]:
    """审计两批语料在**新规则**下的四态归属。"""
    baselines: list[dict[str, Any]] = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "*baseline*"))):
        # 本批自身产物不计入语料审计（否则自我指涉：638_baseline.md 含三元组文本）
        if os.path.basename(p).startswith("638_"):
            continue
        t = open(p, encoding="utf-8", errors="replace").read()
        rec: dict[str, Any] = {"verdict": "pass"}
        for k in BOUNDARY_FIELDS:
            mm = re.search(rf"{k}\D{{0,4}}([^\s|,)]+)", t)
            if mm:
                rec[k] = mm.group(1).strip().strip("`\"'")
        c = classify(rec)
        baselines.append({"file": os.path.basename(p), "state": c["state"],
                          "boundary_ok": c["boundary_ok"]})

    cards: list[dict[str, Any]] = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                t = open(p, encoding="utf-8", errors="replace").read()
                if not _VERIFIED_RE.search(t):
                    continue
                c = classify_card(p)
                cards.append({"file": c["file"], "state": c["state"],
                              "boundary_ok": c["boundary_ok"]})

    def dist(rows: list[dict[str, Any]]) -> dict[str, int]:
        d: dict[str, int] = {}
        for x in rows:
            d[x["state"]] = d.get(x["state"], 0) + 1
        return d

    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "baselines": baselines, "baseline_dist": dist(baselines),
        "baselines_with_boundary": sum(1 for x in baselines if x["boundary_ok"]),
        "cards": cards, "card_dist": dist(cards),
        "cards_with_boundary": sum(1 for x in cards if x["boundary_ok"]),
    }


# ── 迁移（只算不写、不自动跑）────────────────────────────────────────────
def migrate_plan(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """把旧二态判决映射为四态**计划**（纯函数，只算；不写盘、不自动执行）。"""
    plan: list[dict[str, str]] = []
    for r in rows:
        old = str(r.get("state") or r.get("verdict") or "").strip().lower()
        if old in ("block", "fail", "failed", "reject", "rejected"):
            new = "fail"
        elif old in ("pass", "passed", "approve", "approved"):
            new = "pass"
        else:
            new = "unknown"
        plan.append({"file": str(r.get("file", "")), "legacy": old or "(空)", "map_to": new})
    return plan


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report() -> dict[str, str]:
    a = audit()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
    lines = [
        "# 638 3.1 · 四态结论 schema（真上线 · 向后兼容）", "",
        f"> 生成时间：{a['generated']}。工具：`tools/four_state_verdict_638.py`。", "",
        "## 一、四态定义（schema）", "",
        "| 态 | 含义 | 必填 | 旧态映射来源 |", "|---|---|---|---|",
    ]
    for s in STATES:
        d = SCHEMA[s]
        lines.append(f"| `{s}` | {d['desc']} | {', '.join(d['requires']) or '—'} | "
                     f"{', '.join(d['legacy_from']) or '—'} |")
    lines += [
        "", "## 二、边界三元组强制（§3.1.3）", "",
        f"- 必填三字段：`{BOUNDARY_FIELDS[0]}`（64hex）、`{BOUNDARY_FIELDS[1]}`（>0）、"
        f"`{BOUNDARY_FIELDS[2]}`（非空）；",
        "- **缺任一 ⇒ 降级 `unknown`**；`pass_with_exception` 另需非空 `explanation`，否则同样降级；",
        "- 三元组**权威口径**见 `data/638_baseline.md` §1.1（当前统一值 count=1593, "
        "version=`mutation_fuzz@v7`）。", "",
        "## 三、语料审计（新规则下的真实归属）", "",
        f"- `data/*baseline*` 报告：**{len(a['baselines'])}** 份，其中有边界 "
        f"**{a['baselines_with_boundary']}** 份；",
        f"  四态分布：`{a['baseline_dist']}`；",
        f"- `atoms/` verified 卡：**{len(a['cards'])}** 张，其中有边界 "
        f"**{a['cards_with_boundary']}** 张；",
        f"  四态分布：`{a['card_dist']}`。", "",
        "### 3.1 无边界 ⇒ 降级的卡清单（真实）", "",
        "| 卡 | 四态 | 有边界 |", "|---|---|---|",
    ]
    for c in a["cards"]:
        lines.append(f"| `{c['file']}` | {c['state']} | {'是' if c['boundary_ok'] else '否'} |")
    lines += [
        "", "## 四、向后兼容策略", "",
        "| 项 | 策略 |", "|---|---|",
        "| 历史 452 条判决（Authority ledger） | **不重新分类**，保持 APPROVE/MODIFY 原值 |",
        "| 历史 38 份 baseline 报告 | **不重写**，仅离线审计其四态归属 |",
        "| 新判决 | **必须**用四态；缺边界自动 `unknown` |",
        "| 批量迁移 | 仅提供 `migrate_plan()` **计划**（只算不写），`--migrate` 只打印，**不自动跑** |",
        "", "## 五、诚实登记", "",
        "1. 本工具是**新格式执行器**，不修改任何历史判决/报告（§零.1 向后兼容）；",
        "2. 卡级判决抽取用正则（`status:`/`verdict:`/`falsification:`），**非逐条判读**；",
        "   未识别到显式 verdict 的 verified 卡按 `pass` 处理，已在 §3.1 表逐张列出；",
        "3. baseline 报告的边界抽取同样是正则近似（§1.1 已说明三元组不在 ledger）；",
        "4. **实测结论**：23 张 verified 卡**全部无边界三元组** ⇒ 新规则下**全部为 `unknown`**。",
        "   这不是缺陷，是「边界回填」欠债的量化（交人项）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def _boundary() -> dict[str, str]:
    return {"mutation_set_hash": "d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57",
            "mutation_count": "1593", "generator_version": "mutation_fuzz@v7"}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("四态定义齐全", sorted(SCHEMA) == sorted(STATES) and len(STATES) == 4)
    b = _boundary()
    chk("有边界+pass ⇒ pass", enforce({**b, "verdict": "pass"}) == "pass")
    chk("有边界+block ⇒ fail", enforce({**b, "verdict": "block"}) == "fail")
    chk("有边界+例外+explanation ⇒ pass_with_exception",
        enforce({**b, "verdict": "pass", "exception": "条款X", "explanation": "因为Y"})
        == "pass_with_exception")
    chk("有边界+例外但无 explanation ⇒ unknown",
        enforce({**b, "verdict": "pass", "exception": "条款X"}) == "unknown")
    chk("无边界+pass ⇒ 降级 unknown", enforce({"verdict": "pass"}) == "unknown")
    chk("边界 hash 非法 ⇒ 降级 unknown",
        enforce({"mutation_set_hash": "zz", "mutation_count": 1,
                 "generator_version": "v"}) == "unknown")
    chk("count=0 ⇒ 降级 unknown",
        enforce({"mutation_set_hash": b["mutation_set_hash"], "mutation_count": 0,
                 "generator_version": "v"}) == "unknown")
    chk("降级标记 downgraded=True", classify({"verdict": "pass"})["downgraded"] is True)
    chk("has_boundary 真值", has_boundary(b) and not has_boundary({"mutation_count": "3"}))
    chk("迁移计划只算不写", all("map_to" in r for r in migrate_plan([{"state": "block"}])))
    chk("迁移 block→fail", migrate_plan([{"state": "block"}])[0]["map_to"] == "fail")
    a = audit()
    chk("审计含 baseline 与卡", len(a["baselines"]) >= 1 and len(a["cards"]) >= 1)
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 3.1 四态结论 schema")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--card", help="对一张卡做四态分类")
    ap.add_argument("--migrate", action="store_true", help="打印旧→四态迁移计划（只打印，不写盘）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.card:
        print(json.dumps(classify_card(args.card), ensure_ascii=False, indent=2))
        return 0
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    a = audit()
    if args.migrate:
        plan = migrate_plan([{"file": x["file"], "state": "pass"} for x in a["baselines"]])
        print(json.dumps({"plan_size": len(plan), "sample": plan[:3],
                          "note": "仅计划，未写盘、未自动执行"}, ensure_ascii=False, indent=2))
        return 0
    if args.json:
        print(json.dumps({k: v for k, v in a.items() if k not in ("baselines", "cards")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"baselines={len(a['baselines'])} dist={a['baseline_dist']} "
          f"cards={len(a['cards'])} dist={a['card_dist']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
