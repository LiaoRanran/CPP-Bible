"""642 C1 · auto_executor **白名单扩展评估**（只评估，**不实际扩展**）。

**定位**：640 B1 的 `auto_executor_640` 已落地「白名单 5 类 + 六重护栏」。本模块回答：
**下一批能否安全地把更多类别放进白名单？** 并给出每类的风险 / 护栏 / 回滚。

评估方法（**机械可复算**，不是拍脑袋）：

```
score = zone_weight(影响面) × (1 if 可逆 else 2) + blast_weight(影响范围)
zone_weight : 判决/信任面 6 · 治理面 4 · 数据产物 3 · 文档/报告 2
blast_weight: 单文件 0 · 数文件 +1 · 仓库级 +2
verdict:
  影响面 = 判决/信任面        ⇒ **拒绝**（铁律 §零.2：CORE_TOOLS 判决逻辑零改动）
  不可逆                     ⇒ **拒绝**
  score ≥ 6                  ⇒ **延后**
  score < 6 且 C2 门槛未达    ⇒ **技术可入选，但本批不扩大**（等校准度 > 60%）
```

**铁律**：本模块**不改** `auto_executor_640.WHITELIST`、**不改**任何受保护路径常量、
**不执行**任何自动修复（连 dry-run 都不调）。它只读常量 + 出评估报告。

**诚实发现（本工具照出的差异）**：inbox 642 §五 C1 把「当前白名单」描述为
「测试断言数字更新 / 快照重锁 / 补 --check / ruff / 控制字符清理」，但
`auto_executor_640.WHITELIST` **实测**是
`('control_chars','final_newline','trailing_ws','ruff_fix','snapshot_update')` ——
两处**不一致**（任务书口径 vs 代码事实），本工具以**代码事实**为准并登记该差异。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_whitelist_expansion_eval.md`。
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

import auto_executor_640 as ae  # noqa: E402  （只读其 WHITELIST / PROTECTED_PREFIXES 常量）
import loop_calibration_642 as lc  # noqa: E402  （C2 门槛，单一真源）

OUT_MD = os.path.join(ROOT, "data", "642_whitelist_expansion_eval.md")

ZONE_WEIGHT = {"判决/信任面": 6, "治理面": 4, "数据产物": 3, "文档/报告": 2, "已禁止": 99}
BLAST_WEIGHT = {"单文件": 0, "数文件": 1, "仓库级": 2}
DEFER_SCORE = 6

#: 候选类别评估表（**人工判据**：影响面 / 可逆性 / 影响范围，逐条给护栏与回滚）
CANDIDATES: tuple[dict[str, Any], ...] = (
    {"category": "protector_mark_write", "label": "保护器标记写入（如 data/642_*_marks.json）",
     "zone": "数据产物", "reversible": True, "blast": "数文件",
     "guardrails": ["只写 `data/` 下的**声明前缀**（如 `642_`）",
                    "写入幂等（同 (batch,category) 不重复追加）",
                    "**append-only**：不得改写已有标记文件的历史条目",
                    "标记**不得回写判决面**（不得改 gate_engine 输入）",
                    "写入前备份原字节、写入后校验 JSON 可解析"],
     "rollback": "删除/还原本次新建的标记文件即可（不改判决 ⇒ 回滚零语义影响）",
     "note": "642 A6 已实现 `rollback_marks()`（按保护器精确摘除）⇒ 回滚路径已被单测覆盖"},
    {"category": "rule_metadata_update", "label": "规则元数据更新（如 data/642_rule_admission.json）",
     "zone": "治理面", "reversible": True, "blast": "单文件",
     "guardrails": ["**不得**改 `tools/gate_engine.py`（判决面铁律）",
                    "**不得删除**被拒规则（只追加结论）",
                    "必须带版本号 + 生成来源 + 阈值常量快照",
                    "只允许写**新规则**的准入结论（现有 67 条零触碰）"],
     "rollback": "还原侧车 JSON 即可；因不改 gate_engine，回滚不影响任何判决",
     "note": "风险不在文件本身，而在「有人把侧车当成规则源」——需配套「侧车只读」约定"},
    {"category": "report_regen", "label": "报告重生成（重跑 `--report` 覆盖 data/*.md）",
     "zone": "文档/报告", "reversible": True, "blast": "数文件",
     "guardrails": ["只允许重生成**本批前缀**的报告（如 `642_*`），不得跨批覆盖",
                    "重生成后 diff 必须**有界**（仅数字/时间戳漂移；结构变化 ⇒ 拒绝）",
                    "**不得**写入受控目录（atoms/evidence/Examples/Book）",
                    "报告必须**从现算派生**（禁「报告另算」）——与 640c 单一权威源口径一致"],
     "rollback": "`git checkout -- <report>` 还原；因报告是派生量，重生成无副作用",
     "note": "风险最低且收益明确；**唯一真实风险**是覆盖别人的手写报告 ⇒ 前缀白名单可解"},
    {"category": "test_assertion_number_update", "label": "测试断言数字更新（inbox 声称在白名单）",
     "zone": "治理面", "reversible": True, "blast": "数文件",
     "guardrails": ["**禁止**把断言改成「当前值」（等于把测试降级为快照，会掩盖真实回归）",
                    "只允许改**派生自单一权威源**的数字断言（640b/640c 口径）",
                    "改动必须与权威源现算值一致（不变量 + 跨源校验）"],
     "rollback": "还原测试文件；但它直接降低回归发现力 ⇒ **建议拒绝**而非延后",
     "note": "🔴 **实测不在** `auto_executor_640.WHITELIST` 内"
             "（inbox 口径与代码事实不一致，见 §四 honest_diff）"},
    {"category": "add_check_flag", "label": "补 --check 子命令（inbox 声称在白名单）",
     "zone": "治理面", "reversible": True, "blast": "单文件",
     "guardrails": ["新增 `--check` 必须**只读幂等**（不得写盘、不得改状态）",
                    "必须有单测覆盖 `--check` 返回 0 且零写盘"],
     "rollback": "还原脚本文件；无运行时副作用",
     "note": "🟡 **实测不在** WHITELIST 内（inbox 口径与代码事实不一致）；"
             "但 634 A2 是**人工批量**补 --check，未走 auto_executor"},
    {"category": "ledger_write", "label": "权威账本写入（append 一条判决事件）",
     "zone": "判决/信任面", "reversible": False, "blast": "仓库级",
     "guardrails": ["**永不允许自动化**：账本写入 = 代签（铁律 §零.4）"],
     "rollback": "不可回滚（append-only 哈希链；改历史即破坏链）",
     "note": "🔴 明确**拒绝**：这是「机器不代签」红线的直接违反"},
    {"category": "gate_rule_edit", "label": "gate 规则编辑（CORE_TOOLS / 67 条规则）",
     "zone": "判决/信任面", "reversible": True, "blast": "仓库级",
     "guardrails": ["**永不允许自动化**：CORE_TOOLS 判决逻辑零改动（铁律 §零.2）"],
     "rollback": "理论可 git 还原，但一旦在自动化批次里发生，无法保证无中间污染",
     "note": "🔴 明确**拒绝**"},
    {"category": "knowledge_card_edit", "label": "知识卡编辑（atoms / evidence / Book）",
     "zone": "判决/信任面", "reversible": True, "blast": "仓库级",
     "guardrails": ["**永不允许自动化**：受控目录零污染（铁律 §零.3）"],
     "rollback": "可 git 还原，但会污染 Merkle 根与完整性台账",
     "note": "🔴 明确**拒绝**；`auto_executor_640.PROTECTED_PREFIXES` 已硬编码拦截"},
)


def score_of(c: dict[str, Any]) -> int:
    """机械可复算的风险分（不是被验证过的风险模型，见诚实登记 §2）。"""
    zone = ZONE_WEIGHT.get(str(c["zone"]), 99)
    if zone >= 99:
        return 99
    return zone * (1 if c["reversible"] else 2) + BLAST_WEIGHT.get(str(c["blast"]), 0)


def verdict_of(c: dict[str, Any], gate_passed: bool) -> tuple[str, str]:
    """(verdict, reason)。判定顺序：判决面 ⇒ 不可逆 ⇒ 分数 ⇒ C2 门槛。"""
    if c["zone"] == "判决/信任面":
        return "拒绝", "影响面是判决/信任面 ⇒ 违反铁律（CORE_TOOLS/账本/受控目录不可自动化）"
    if not c["reversible"]:
        return "拒绝", "不可逆 ⇒ 不进白名单（自动执行必须可回滚）"
    s = score_of(c)
    if s >= DEFER_SCORE:
        return "延后", f"score={s} ≥ {DEFER_SCORE}（影响面 × 可逆性 × 范围偏大）"
    if not gate_passed:
        best = lc.best_calibration()
        best_txt = "无可计算值" if best is None else f"{best:.1%}"
        return "技术可入选（本批不扩大）", (
            f"score={s} < {DEFER_SCORE}，但 C2 校准度门槛未达"
            f"（最高观测 {best_txt} ≤ {lc.EXPANSION_THRESHOLD:.0%}）⇒ **本批不扩大白名单**")
    return "可入选", f"score={s} < {DEFER_SCORE} 且门槛已达"


def evaluate() -> dict[str, Any]:
    gate = lc.expansion_gate()
    rows = []
    for c in CANDIDATES:
        v, why = verdict_of(c, bool(gate["passed"]))
        rows.append({**c, "score": score_of(c),
                     "in_current_whitelist": c["category"] in ae.WHITELIST,
                     "verdict": v, "verdict_reason": why})
    return {"gate": gate, "rows": rows,
            "current_whitelist": list(ae.WHITELIST),
            "protected_prefixes": list(ae.PROTECTED_PREFIXES),
            "by_verdict": _count(rows)}


def _count(rows: list[dict[str, Any]]) -> dict[str, int]:
    d: dict[str, int] = {}
    for r in rows:
        d[r["verdict"]] = d.get(r["verdict"], 0) + 1
    return d


def honest_diff() -> dict[str, Any]:
    """inbox 口径 vs 代码事实的差异（诚实登记）。"""
    claimed = ("测试断言数字更新", "快照重锁", "补 --check", "ruff", "控制字符清理")
    return {"inbox_claimed": list(claimed), "code_actual": list(ae.WHITELIST),
            "consistent": False,
            "note": "两处不一致：inbox 把「测试断言数字更新 / 补 --check」算作现有白名单，"
                    "但 `auto_executor_640.WHITELIST` 实测**不含**二者；"
                    "本工具以**代码事实**为准。另：`snapshot_update`（快照重锁）**在**白名单内，"
                    "但其语义风险（可能掩盖真实行为变化）值得 643 复核。"}


def write_report() -> str:
    r = evaluate()
    g = r["gate"]
    d = honest_diff()
    best_txt = ("—" if g["best_observed"] is None
                else "%.1f%%" % (g["best_observed"] * 100))
    lines = [
        "# 642 C1 · auto_executor 白名单扩展评估（**只评估，不实际扩展**）", "",
        f"> 现有白名单（**代码事实** `auto_executor_640.WHITELIST`）：`{r['current_whitelist']}`",
        f"> 受保护路径前缀（`PROTECTED_PREFIXES`）：**{len(r['protected_prefixes'])}** 条"
        "（含 CORE_TOOLS / 账本 / 受控目录）", "",
        "## 一、评估方法（机械可复算）", "",
        "```",
        "score = zone_weight(影响面) × (1 if 可逆 else 2) + blast_weight(影响范围)",
        "zone_weight : 判决/信任面 6 · 治理面 4 · 数据产物 3 · 文档/报告 2",
        "blast_weight: 单文件 0 · 数文件 +1 · 仓库级 +2",
        f"verdict: 判决/信任面 ⇒ 拒绝；不可逆 ⇒ 拒绝；score ≥ {DEFER_SCORE} ⇒ 延后；"
        "否则技术可入选（仍需过 C2 门槛）",
        "```", "",
        "## 二、候选逐条评估", "",
        "| 类别 | 影响面 | 可逆 | 范围 | score | 已在白名单 | 结论 |",
        "|---|---|---|---|---|---|---|"]
    for row in r["rows"]:
        lines.append(f"| `{row['category']}` | {row['zone']} | "
                     f"{'✅' if row['reversible'] else '❌'} | {row['blast']} | "
                     f"{row['score'] if row['score'] < 99 else '∞'} | "
                     f"{'是' if row['in_current_whitelist'] else '否'} | **{row['verdict']}** |")
    lines += ["", "### 2.1 逐条：护栏需求 / 回滚方案 / 结论理由", "",
              "| 类别 | 护栏需求 | 回滚方案 | 结论理由 |", "|---|---|---|---|"]
    marks = "①②③④⑤⑥⑦⑧⑨"
    for row in r["rows"]:
        guards = "；".join(f"{marks[i]} {x}" for i, x in enumerate(row["guardrails"]))
        lines.append(f"| `{row['category']}` | {guards} | {row['rollback']} | "
                     f"{row['verdict_reason']} |")
    lines += ["", "### 2.2 逐条补充说明", ""]
    for row in r["rows"]:
        lines.append(f"- `{row['category']}`：{row['note']}")
    lines += ["", "## 三、结论分布与最终建议", "",
              f"- 分布：`{r['by_verdict']}`",
              f"- **是否真的扩大**由 C2 门槛裁决：门槛 **{g['threshold']:.0%}**，"
              f"当前最高观测 **{best_txt}** ⇒ **{g['verdict']}**",
              f"- 附加条件：{g['caveat']}", "",
              "1. **本批不扩大白名单**（门槛未达；且 C1 铁律要求只评估）；",
              "2. 若 643 门槛达成，**优先考虑** `report_regen`（score 3，风险最低、收益明确）；",
              "3. `protector_mark_write`（score 4）次之 —— 其回滚路径已被 642 A6 单测覆盖；",
              "4. `rule_metadata_update`（score 4）**需先确立「侧车只读」约定**再谈自动化；",
              "5. `test_assertion_number_update` **建议拒绝**（把断言改成当前值等于降级测试），"
              "尽管 score 只有 4；",
              "6. `snapshot_update` **已在白名单**，但其语义风险建议 643 复核。", "",
              "## 四、诚实发现：inbox 口径 vs 代码事实", "",
              f"- inbox 声称的现有白名单：`{d['inbox_claimed']}`",
              f"- 代码事实 `WHITELIST`：`{d['code_actual']}`",
              f"- 一致：**{d['consistent']}** —— {d['note']}", "",
              "## 诚实登记", "",
              "1. **只评估不扩展**（§七.5）：本模块**未改动** `auto_executor_640.WHITELIST`、"
              "**未执行**任何自动修复（连 dry-run 都未调用）；",
              "2. `CANDIDATES` 的「影响面/可逆性/范围」是**人工判据**，score 公式是本批新造 ——"
              "它**可复算**，但不是**被验证过**的风险模型（无历史事故数据校准）；",
              "3. **风险等级 ≠ 闸门**：真正的闸门是「能不能回滚」与「是否触碰判决面」，"
              "score 只用于同类排序；",
              "4. `report_regen` 的最大隐患是「覆盖别人的手写报告」，"
              "前缀白名单能降低但不能消除；",
              "5. 门槛 60% 本身是**经验值**（C2 已登记样本极小）⇒ 是否降低门槛交人裁决。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("现有白名单 5 类（读 640 常量）", len(ae.WHITELIST) == 5)
    chk("未改 640 白名单", list(ae.WHITELIST) == ["control_chars", "final_newline",
                                                 "trailing_ws", "ruff_fix", "snapshot_update"])
    r = evaluate()
    chk("候选 ≥ 8 条", len(r["rows"]) >= 8)
    chk("判决面/不可逆 ⇒ 拒绝",
        all(row["verdict"] == "拒绝" for row in r["rows"]
            if row["zone"] == "判决/信任面" or not row["reversible"]))
    chk("记账本/改规则/改卡 都在拒绝之列",
        {row["verdict"] for row in r["rows"]
         if row["category"] in ("ledger_write", "gate_rule_edit", "knowledge_card_edit")}
        == {"拒绝"})
    chk("门槛未达 ⇒ 低风险项是『技术可入选（本批不扩大）』",
        any(row["verdict"] == "技术可入选（本批不扩大）" for row in r["rows"]))
    chk("report_regen 是低分低成本候选",
        next(row["score"] for row in r["rows"]
             if row["category"] == "report_regen") < DEFER_SCORE)
    chk("score 公式可复算",
        score_of({"zone": "数据产物", "reversible": True, "blast": "单文件"}) == 3)
    chk("不可逆翻倍",
        score_of({"zone": "数据产物", "reversible": False, "blast": "单文件"}) == 6)
    d = honest_diff()
    chk("照出 inbox 口径 ≠ 代码事实", d["consistent"] is False)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 C1 白名单扩展评估")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写评估报告")
    ap.add_argument("--json", action="store_true", help="打印评估（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = evaluate()
    if a.json:
        print(json.dumps({"by_verdict": r["by_verdict"], "gate": r["gate"],
                          "current_whitelist": r["current_whitelist"],
                          "rows": [{k: row[k] for k in ("category", "zone", "score", "verdict")}
                                   for row in r["rows"]]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[whitelist-eval] 候选 {len(r['rows'])} ⇒ {r['by_verdict']}；"
          f"C2 门槛 {'已达' if r['gate']['passed'] else '未达 ⇒ 本批不扩大白名单'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
