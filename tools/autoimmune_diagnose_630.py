"""630 A1 · 自身免疫率口径差异诊断（纯标准库，**只读，不改任何卡**）

629 A1 实测：23 张 verified 干净卡全部被 warn（自身免疫率 100%），其中 **22 张**仅命中
「命题级口径」三条规则（`CALIBER_RULES`）。本工具对**这 22 张卡逐张**列出：

- 卡 ID / 路径
- gate 要求的**字段名**（命题级）
- 卡当前 frontmatter 中该字段的**实际值**（或缺失）
- warn 的**具体规则名 + 消息原文**
- 分类：**字段缺失型 / 字段值不符型 / 格式型**
- 修复建议：**补字段（auto 可推断 / human 需人填）/ 改规则 / 豁免**

分类判据（显式写死，供人复核——分类本身是判断，不是机器真理）：
- **字段缺失型**：命题里没有该键，或值为空；
- **格式型**：键存在但**结构**不合规（`signed_by` 不是 `human:<名>`；`liveness` 不是
  `{kind, symbol}` 字典；`object` 是**句子**而非概念短语——含句读/过长）；
- **字段值不符型**：键存在、结构合规，但取值不被规则接受（如 object 是合规短语但不在
  规范概念集内）。

**本工具零写入**（只读 `import gate_engine` 与 629 框架），不修改任何卡、不改规则。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_diagnose_630.md")
OUT_JSON = os.path.join(ROOT, "data", "autoimmune_diagnose_630.json")

# 三条「命题级口径」规则 → 要求字段（判定沿用 gate_engine 的实现）
RULE_FIELD = {
    "OBSERVATION-LIVENESS": {
        "field": "liveness",
        "scope": "命题项",
        "want": "`liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}`",
        "fix_kind": "补字段",
    },
    "ATOM-CLAIM-CONCEPT-NORMALIZED": {
        "field": "object",
        "scope": "命题项",
        "want": "object ∈ 规范概念集（概念短语，不是句子）",
        "fix_kind": "补字段",
    },
    "INFERENCE-NOT-MACHINE-VERIFIED": {
        "field": "signed_by",
        "scope": "命题项",
        "want": "`signed_by: human:<在册实名>`（命题级人签）",
        "fix_kind": "补字段",
    },
}
SENTENCE_MARK = re.compile(r"[。；！？，、（）()《》]|\s{2,}")
PROP_ID_RE = re.compile(r"命题\s+([^\s（(]+)")


def _norm_set() -> set:
    """gate 的规范概念集（只读调用，口径与 ATOM-CLAIM-CONCEPT-NORMALIZED 一致）。"""
    import gate_engine as ge

    return set(ge._concept_normalized_set())


def caliber_warns() -> list[dict[str, Any]]:
    """22 张「仅口径」卡上的 warn 明细（复用 629 框架的求值口径）。"""
    import autoimmune_rate_framework as F

    m = F.measure()
    out: list[dict[str, Any]] = []
    for rec in m["warned"]:
        only_caliber = all(h["rule"] in F.CALIBER_RULES for h in rec["warn"])
        for h in rec["warn"]:
            if h["rule"] not in RULE_FIELD:
                continue      # 本工具只诊断三条「命题级口径」规则（硬缺陷桶归 A2 之外）
            out.append({"card_id": rec["id"], "card_rel": rec["rel"],
                        "path": rec["path"], "rule": h["rule"],
                        "message": h["message"], "caliber_only_card": only_caliber})
    return out


def prop_of(card_path: str, prop_id: str) -> dict[str, Any]:
    """取命题 dict（只读）。"""
    import gate_engine as ge

    meta = ge._meta(__import__("pathlib").Path(card_path))
    for pr in ge._claim_props(meta):
        if str(pr.get("id")) == prop_id:
            return dict(pr)
    return {}


def classify(rule: str, prop: dict[str, Any]) -> dict[str, Any]:
    """把一条 warn 归入三型之一，并给出 auto/human 修复能力。"""
    field = RULE_FIELD.get(rule, {}).get("field", "?")
    present = field in prop and str(prop.get(field, "")).strip() not in ("", "None", "{}")
    val = prop.get(field)
    if not present:
        return {"type": "字段缺失型", "current": "（缺失）",
                "auto": rule == "OBSERVATION-LIVENESS",
                "reason": f"命题里没有 `{field}` 键或值为空"}
    if rule == "ATOM-CLAIM-CONCEPT-NORMALIZED":
        obj = str(val)
        is_sentence = len(obj) > 20 or bool(SENTENCE_MARK.search(obj))
        if is_sentence:
            return {"type": "格式型", "current": obj,
                    "auto": False,
                    "reason": "object 是句子/长串而非概念短语"}
        return {"type": "字段值不符型", "current": obj, "auto": False,
                "reason": "object 是短语但不在规范概念集内"}
    if rule == "OBSERVATION-LIVENESS":
        ok_shape = isinstance(val, dict) and bool(val.get("symbol"))
        return {"type": "字段值不符型" if ok_shape else "格式型", "current": str(val),
                "auto": ok_shape, "reason": "liveness 存在但结构/取值不合规"}
    if rule == "INFERENCE-NOT-MACHINE-VERIFIED":
        s = str(val)
        ok_shape = s.startswith("human:") and len(s) > 6
        return {"type": "字段值不符型" if ok_shape else "格式型", "current": s,
                "auto": False,
                "reason": "signed_by 存在但不是有效 `human:<实名>`（机器不能代人签）"}
    return {"type": "字段值不符型", "current": str(val), "auto": False, "reason": ""}


def diagnose() -> dict[str, Any]:
    rows = []
    for w in caliber_warns():
        pid_m = PROP_ID_RE.search(str(w["message"]))
        pid = pid_m.group(1) if pid_m else "?"
        prop = prop_of(w["path"], pid) if os.path.exists(w["path"]) else {}
        cls = classify(w["rule"], prop)
        rows.append({**w, "prop_id": pid, "field": RULE_FIELD[w["rule"]]["field"],
                     "want": RULE_FIELD[w["rule"]]["want"], **cls})
    per_rule: dict[str, int] = {}
    per_type: dict[str, int] = {}
    per_card: dict[str, int] = {}
    for r in rows:
        per_rule[r["rule"]] = per_rule.get(r["rule"], 0) + 1
        per_type[r["type"]] = per_type.get(r["type"], 0) + 1
        per_card[r["card_id"]] = per_card.get(r["card_id"], 0) + 1
    return {"rows": rows, "warns": len(rows), "cards": len(per_card),
            "per_rule": per_rule, "per_type": per_type,
            "per_card": per_card,
            "auto_fixable": sum(1 for r in rows if r["auto"]),
            "human_required": sum(1 for r in rows if not r["auto"]),
            "caliber_only_cards": sorted({r["card_id"] for r in rows
                                          if r["caliber_only_card"]})}


def git_atoms_clean() -> bool:
    p = subprocess.run(["git", "diff", "--quiet", "--", "atoms"], cwd=ROOT,
                       check=False, capture_output=True)
    return p.returncode == 0


def write_report() -> str:
    d = diagnose()
    lines = [
        "# 630 A1 · 自身免疫率口径差异诊断（22 张口径级 warn 逐卡）", "",
        "> 工具：`tools/autoimmune_diagnose_630.py`（纯标准库，**只读，零写入**；"
        "分类判据写死在源码里供人复核）",
        f"> 实测：**{d['warns']} 条 warn** 分布在 **{d['cards']} 张卡**上", "",
        "## 一、分类统计", "",
        "| 分类 | 条数 | 判据 |", "|---|---|---|",
        f"| 字段缺失型 | {d['per_type'].get('字段缺失型', 0)} | 命题里没有该键，或值为空 |",
        f"| 字段值不符型 | {d['per_type'].get('字段值不符型', 0)} | 键在、结构合规，但取值不被规则接受 |",
        f"| 格式型 | {d['per_type'].get('格式型', 0)} | 键在但结构不合规（如 object 是句子） |", "",
        "| 规则 | 条数 | 要求字段 |", "|---|---|---|",
        *[f"| `{k}` | {v} | {RULE_FIELD[k]['want']} |" for k, v in
          sorted(d["per_rule"].items(), key=lambda kv: -kv[1])], "",
        f"- **auto 可自动补**（能从既有数据推断）：**{d['auto_fixable']} 条**",
        f"- **human 必须人填**：**{d['human_required']} 条**"
        f"{'（超过 5 条 ⇒ 触发任务书 §十.3「需人审批量处理」）' if d['human_required'] > 5 else ''}",
        "", "## 二、逐卡逐条诊断", "",
        "| # | 卡 ID | 命题 | 规则 | 要求字段 | 当前值 | 分类 | 可自动 |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {i} | `{r['card_id']}` | `{r['prop_id']}` | `{r['rule']}` | "
          f"`{r['field']}` | {str(r['current'])[:32]} | {r['type']} | "
          f"{'auto' if r['auto'] else 'human'} |" for i, r in enumerate(d["rows"], 1)], "",
        "## 三、修复建议（三选一，本批不执行）", "",
        "1. **补字段**：`OBSERVATION-LIVENESS` 的 `liveness` 在**能定位到夹具特有符号**时可自动推断"
        "（取本命题引用卡 `artifact_assert` 里的非通用符号）；其余字段需人填（尤其 `signed_by`，"
        "机器永不代签，§零.3）。",
        "2. **改规则**：三条规则都是 526/530 为**新卡**设计的命题级放权闸；若对老卡豁免"
        "（按 `created_at`/`meta_version` 分流），blast radius 覆盖**全库 27 张原子卡 + 未来所有卡**，"
        "且会让「命题级放权」在存量上失效 ⇒ 风险高，见 A2 方案乙。",
        "3. **豁免**：把 22 张卡登记进既有豁免治理（有哈希链、可审计），代价是**债被固化**。", "",
        "## 四、关键诚实", "",
        "- **这不是「gate 误杀」的直接证据**：三条规则都要求「命题级」字段，而老卡的命题只挂"
        "证据卡 id（卡级活性条件）⇒ 属**规则口径与存量形态的错配**；",
        "- 分类（缺失/值不符/格式）是**人工判据的机器实现**，边界情形（如「短语 vs 短句」）"
        "存在解释空间，逐条表格已列出当前值供人复核；",
        "- 本工具**不修改任何卡**（自检断言 `git diff --quiet -- atoms` 为空）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in d.items()}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import autoimmune_rate_framework as F

    m = F.measure()
    d = diagnose()
    caliber_cards = set(m["caliber_only_cards"])
    chk("629 基线：仅口径卡 = 22 张", len(caliber_cards) == 22, f"({len(caliber_cards)})")
    chk("诊断覆盖全部仅口径卡", caliber_cards <= set(d["caliber_only_cards"]),
        f"({len(set(d['caliber_only_cards']))})")
    chk("每条 warn 都被归入三型之一",
        all(r["type"] in ("字段缺失型", "字段值不符型", "格式型") for r in d["rows"]))
    chk("三条规则都被覆盖", set(d["per_rule"]) == set(RULE_FIELD),
        f"({sorted(d['per_rule'])})")
    chk("auto + human = 总条数",
        d["auto_fixable"] + d["human_required"] == d["warns"], f"({d['warns']})")
    chk("signed_by 类一律 human（机器不代签）",
        all(not r["auto"] for r in d["rows"]
            if r["rule"] == "INFERENCE-NOT-MACHINE-VERIFIED"))
    chk("词表：object 句子判为格式型",
        classify("ATOM-CLAIM-CONCEPT-NORMALIZED",
                 {"object": "这编译器在 2020 年之后的实现里都会这样优化，因为……"})["type"]
        == "格式型")
    chk("词表：object 缺失判为缺失型",
        classify("ATOM-CLAIM-CONCEPT-NORMALIZED", {})["type"] == "字段缺失型")
    chk("只读：atoms 目录零改动", git_atoms_clean())
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"A1 autoimmune diagnose check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 A1 口径差异诊断（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写诊断报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = diagnose()
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"warns={d['warns']} cards={d['cards']} types={d['per_type']} "
          f"auto={d['auto_fixable']} human={d['human_required']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
