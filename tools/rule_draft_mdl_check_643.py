"""643 D3 · **规则草案 MDL 准入检查**（智能层：自动提案规则 #3）。

**定位**：对 D2 的草案跑 642 的 MDL 准入器，并**新增第五档「抗冗余」**
（A1-C5 / A4-D-3：642 的 MDL 器**没有**这一项，而"冗余规则比缺失规则更常见"是最常见的病）。

**两段判定（顺序固定）**：

| 段 | 判据 | 结论 |
|---|---|---|
| ① **抗冗余**（本批新增） | `overlap > 0.8` | **`REJECT_冗余`**（不再往下判） |
| ② **MDL 准入**（复用 642 器） | `admit_new_rule()` 六档 | `ADMIT` / `REFUSE_已有规则` / `PENDING_HUMAN` / `REJECT_豁免率` / `REJECT_热力图缺失` / `REJECT_编码长度` |

**`overlap` 的定义（两类草案不同，各自可复算）**：
- **NEW 草案**：`overlap = min(1, 该目标卡被多少条规则命中 / 10)` —— **覆盖密度代理**
  （卡已被 >10 条规则命中 ⇒ 再为它加规则大概率冗余）；
- **MODIFY 草案**：`overlap = max over 其它规则 ( |本草案字段 ∩ 该规则字段| / |本草案字段| )`
  —— **真实字段级重叠**（同一批字段被两条规则各管一次 = 冗余）。

**诚实边界**：
- **MODIFY 草案不是"新规则"** ⇒ 642 的 `admit_new_rule` 本不为它设计；本工具仍跑它，
  但把结果标 `mdl_applies_to="MODIFY（近似）"` 并说明**它衡量的是"新增条件的边际收益"**；
- `exempt_rate` 来自 624 热力图（**旧台账**，642 已登记其局限）⇒ NEW 草案必然"不在热力图"，
  会命中 `REJECT_热力图缺失` —— 这是**口径必然**，不是草案的错，报告里逐条标注。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_draft_mdl.md` + `.json`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import coverage_gap_scanner_643 as B1  # noqa: E402
import mdl_gate_642 as mg  # noqa: E402
import rule_drafter_643 as D2  # noqa: E402
import rule_precondition_analyzer_643 as C1  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_draft_mdl.md")
OUT_JSON = os.path.join(ROOT, "data", "643_draft_mdl.json")
OVERLAP_THRESHOLD = 0.80
DENSITY_K = 10                      # 与 B1 的"超阈值卡"同口径


def overlap_new(card: str, card_hits: dict[str, int]) -> float:
    """NEW 草案的覆盖密度代理（纯函数）。"""
    return round(min(1.0, card_hits.get(card, 0) / DENSITY_K), 4)


def overlap_modify(fields: list[str], target_rule: str,
                   fields_by_rule: dict[str, list[str]]) -> tuple[float, str]:
    """MODIFY 草案的字段级重叠（纯函数）：与其它规则共享字段的最大比例。"""
    if not fields:
        return 0.0, ""
    best, who = 0.0, ""
    for rid, f2 in fields_by_rule.items():
        if rid == target_rule:
            continue
        shared = len(set(fields) & set(f2))
        r = shared / len(set(fields))
        if r > best:
            best, who = r, rid
    return round(best, 4), who


def check(drafts_list: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    dl = drafts_list if drafts_list is not None else D2.drafts()["drafts"]
    cov = B1.report()
    card_hits = cov["analysis"]["card_hit_counts"]
    fields_by_rule = {r["rule_id"]: r["precondition"]["fields"]
                      for r in C1.analyze()["rows"]}
    existing = mg.existing_rule_ids()

    rows = []
    for d in dl:
        kind = d["kind"]
        if kind == "NEW":
            card = d["provenance"].get("card", "")
            ov = overlap_new(card, card_hits)
            ov_against = f"该卡已被 {card_hits.get(card, 0)} 条规则命中（密度代理）"
            mdl_res = mg.admit_new_rule(d["proposed_rule_id"], d["title"],
                                        existing=existing)
            mdl_applies = "NEW（直接用 642 器）"
        else:
            fields = list(d["provenance"].get("fields") or [])
            target = str(d["provenance"].get("target_rule", ""))
            ov, who = overlap_modify(fields, target, fields_by_rule)
            ov_against = f"与 `{who or '—'}` 的字段重叠" if who else "无可比规则/无字段"
            mdl_res = mg.admit_new_rule(d["proposed_rule_id"], d["title"],
                                        existing=existing)
            mdl_applies = "MODIFY（近似：衡量新增条件的边际收益）"
        redundant = ov > OVERLAP_THRESHOLD
        final = "REJECT_冗余" if redundant else mdl_res["decision"]
        rows.append({"draft_id": d["draft_id"], "proposed_rule_id": d["proposed_rule_id"],
                     "kind": kind, "overlap": ov, "overlap_against": ov_against,
                     "redundant": redundant, "mdl_decision": mdl_res["decision"],
                     "mdl_detail": mdl_res.get("detail", ""),
                     "mdl_savings_bits": mdl_res.get("savings_bits"),
                     "mdl_cost_bits": mdl_res.get("cost_bits"),
                     "mdl_applies_to": mdl_applies,
                     "final_decision": final, "admitted": final == "ADMIT"})
    by_final: dict[str, int] = {}
    for r in rows:
        by_final[r["final_decision"]] = by_final.get(r["final_decision"], 0) + 1
    return {"rows": rows, "n": len(rows), "by_final": by_final,
            "n_admitted": sum(1 for r in rows if r["admitted"]),
            "n_redundant": sum(1 for r in rows if r["redundant"]),
            "overlap_threshold": OVERLAP_THRESHOLD,
            "existing_rules": len(existing)}


def write_report() -> str:
    c = check()
    lines = [
        "# 643 D3 · 规则草案 MDL 准入（智能层：自动提案规则 #3；**新增抗冗余闸**）", "",
        f"> 草案 **{c['n']}** 条；`ADMIT` **{c['n_admitted']}** 条；"
        f"`REJECT_冗余` **{c['n_redundant']}** 条（阈值 overlap > {c['overlap_threshold']}）；"
        f"结论分布 `{c['by_final']}`。",
        f"> 在册规则 {c['existing_rules']} 条（642 MDL 器的 `REFUSE_已有规则` 依据）。", "",
        "## 一、逐条判定", "",
        "| 草案 | 形态 | overlap | 依据 | 642 MDL 结论 | 最终结论 | 是否准入 |",
        "|---|---|---|---|---|---|---|"]
    for r in c["rows"]:
        lines.append(f"| `{r['proposed_rule_id']}` | {r['kind']} | {r['overlap']} | "
                     f"{r['overlap_against']} | `{r['mdl_decision']}` | "
                     f"**{r['final_decision']}** | {'✅' if r['admitted'] else '—'} |")
    lines += ["", "## 二、判定顺序说明", "",
              "1. **先判抗冗余**（`overlap > 0.8` ⇒ `REJECT_冗余`，不再往下判）；",
              "2. 否则跑 **642 的 `admit_new_rule()`**（六档），取其结论为最终结论。", "",
              "## 三、642 MDL 的已知口径问题（逐条标注）", "",
              "- **NEW 草案必然「不在热力图」** ⇒ 会命中 `REJECT_热力图缺失`："
              "这是**口径必然**（624 的热力图早于草案存在），**不是草案的错** ⇒ "
              "NEW 草案应看「若非此条是否还有别的否决」，而不是直接否决；",
              "- **MODIFY 草案不是「新规则」** ⇒ 642 的器本不为它设计，"
              "本工具仍跑它并标 `MODIFY（近似）`，其 `savings/cost` 衡量的是"
              "**新增条件的边际收益**（近似，需人判）。", "",
              "## 诚实登记", "",
              "1. **MDL/抗冗余通过 ≠ 规则正确**（§十二.3）：这只是**费用与冗余**两道闸，"
              "规则**对不对**必须人审；",
              "2. **`overlap` 对两类草案的定义不同**（NEW 用覆盖密度代理、MODIFY 用字段重叠）"
              "⇒ 两者的 `overlap` **不可互相比较**，已在表里分列依据；",
              "3. **阈值 0.8 是本批新定的经验值**（642 没有这一档）⇒ 边界已在单测固定，"
              "改阈值会改变结论；",
              "4. **本工具不改 642 的 MDL 器**：`REJECT_冗余` 是本工具**新增的第五档**，"
              "不写回 642 的 `DECISIONS` 常量（避免改动已入库工具）；",
              "5. 本工具**只读**：不改规则库、不写侧车元数据（写侧车是 D2 的产出）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("密度代理：0 命中 ⇒ 0", overlap_new("c", {}) == 0.0)
    chk("密度代理：10 命中 ⇒ 1.0（封顶）", overlap_new("c", {"c": 10}) == 1.0)
    chk("密度代理：5 命中 ⇒ 0.5", overlap_new("c", {"c": 5}) == 0.5)
    chk("密度代理封顶（20 ⇒ 仍 1.0）", overlap_new("c", {"c": 20}) == 1.0)

    fbr = {"R1": ["status", "evidence"], "R2": ["status"], "R3": ["other"]}
    ov, who = overlap_modify(["status", "evidence"], "R0", fbr)
    chk("字段重叠：全同 ⇒ 1.0（R1）", ov == 1.0 and who == "R1", f"{ov}/{who}")
    ov2, who2 = overlap_modify(["status", "evidence"], "R1", fbr)
    chk("排除自身（目标规则不与自己比）", who2 != "R1", who2)
    chk("无字段 ⇒ 0", overlap_modify([], "R0", fbr) == (0.0, ""))

    chk("阈值常量在册", OVERLAP_THRESHOLD == 0.8)
    c = check()
    chk("草案全判（条数一致）", c["n"] == len(c["rows"]) and c["n"] > 0)
    chk("结论分布自洽", sum(c["by_final"].values()) == c["n"])
    chk("admitted 计数与 ADMIT 一致",
        c["n_admitted"] == sum(1 for r in c["rows"] if r["final_decision"] == "ADMIT"))
    chk("冗余条与 overlap 阈值一致",
        all((r["overlap"] > OVERLAP_THRESHOLD) == r["redundant"] for r in c["rows"]))
    chk("MDL 结论都在 642 六档内",
        all(r["mdl_decision"] in mg.DECISIONS for r in c["rows"]))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 D3 草案 MDL 准入 + 抗冗余")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    c = check()
    if x.json:
        print(json.dumps(c, ensure_ascii=False, indent=2))
        return 0
    print(f"[draft-mdl] {c['n']} 草案 ⇒ {c['by_final']}；准入 {c['n_admitted']}；"
          f"冗余 {c['n_redundant']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
