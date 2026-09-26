"""642 A5 · MDL 规则准入**上岗**（新规则准入门槛；**只对新规则**，不动现有 67 条）。

**与 636 的关系**：636（`mdl_trial_636`）是**试运行**（离线算 admit/reject），本模块把它落成
**准入门槛**：新规则必须先过 MDL 长度判据 + 豁免率判据，才允许入库。

准入判据（§三 A5）：

| 判据 | 口径 | 不过的后果 |
|---|---|---|
| 编码长度 | 复用 636：`savings > L(rule)`（savings = 命中轮数×每轮样本×log2(N)） | `REJECT(编码长度)` |
| 热力图覆盖 | 新规则**必须在 VFDR 热力图**且**至少触达 1 轮** | `REJECT(热力图缺失/零触达)` |
| 豁免率 | 该规则**未触达轮占比** < 阈值 | `REJECT(豁免率)`；无数据 ⇒ `PENDING_HUMAN` |
| 是否已有 | `rule_id` 已在册 ⇒ **拒绝更新**（本批只对新规则准入） | `REFUSE(已有规则)` |

**豁免率口径澄清（诚实）**：636 报告 §三 把「通过率」误题为「豁免率趋势」（早期 66.7% → 近期 23.5%）。
642 明确区分：

* `admit_rate`（636 的 66.7% / 23.5%）= 规则分成两半后各自的 `savings > cost` 通过率；
* `exempt_rate`（642 准入判据用的）= 该规则在 **6 轮攻击中「未触达」的轮次占比**。

两者**不可混用**。task 要求的"近期 23.5% 作准入参考"在本模块体现为
`EXEMPT_RATE_REFERENCE = 0.235`（**只作量级参考**）；实际阈值 `EXEMPT_RATE_THRESHOLD = 0.30`
（在参考值之上留余量）。

**铁律**：**不修改现有 67 条规则**（`gate_engine.py` 只读，不重写）；被拒规则**不删除**
（准入结论只写侧车元数据 `data/642_rule_admission.json`）。

**诚实登记**（§十.4）：编码长度/豁免率都是**启发式**，**可能误杀好规则**；热力图缺失的"新规则"
也可能是**新方向**而非冗余（4 条 HC 规则即为例）。

只读契约：`--check` 只读、exit 0；`--report` 写报告 + 侧车元数据（均在 `data/` 下）。
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

import mdl_trial_636 as shadow  # noqa: E402  （长度判据/热力图单一真源，不复制）

OUT_MD = os.path.join(ROOT, "data", "642_mdl_admission.md")
OUT_JSON = os.path.join(ROOT, "data", "642_rule_admission.json")
VERSION = "642.1"

#: 636 报告的「近期值」——**实为通过率**，此处只作量级参考（见模块 docstring）
EXEMPT_RATE_REFERENCE = 0.235
#: 准入豁免率阈值（在参考值之上留余量）
EXEMPT_RATE_THRESHOLD = 0.30

DECISIONS = ("ADMIT", "REJECT_编码长度", "REJECT_热力图缺失", "REJECT_豁免率",
             "PENDING_HUMAN", "REFUSE_已有规则")


def existing_rule_ids() -> list[str]:
    """现有在册规则 id（`gate_engine` 只读）。"""
    return [r["id"] for r in shadow.rules()]


def exempt_rate(rule_id: str, hm: dict[str, dict[str, bool]]) -> Optional[float]:
    """**实测豁免率** = 该规则在热力图里「未触达」的轮次占比（0..1）；无热力图记录 ⇒ None。"""
    rounds = hm.get(rule_id)
    if not isinstance(rounds, dict) or not rounds:
        return None
    total = len(rounds)
    touched = sum(1 for v in rounds.values() if v)
    return round((total - touched) / total, 4)


def admit_new_rule(rule_id: str, title: str = "",
                   hm: Optional[dict[str, dict[str, bool]]] = None,
                   existing: Optional[list[str]] = None,
                   declared_exempt_rate: Optional[float] = None) -> dict[str, Any]:
    """准入判定（纯函数），**判定顺序固定**（先材料完整性，再技术判据）：

    1. 已在册 ⇒ `REFUSE_已有规则`（本批只对新规则准入）；
    2. 豁免率：`declared_exempt_rate` 优先，缺省用热力图**实测豁免率**；两者皆缺 ⇒
       `PENDING_HUMAN`（**也是不准入**，只是把缺数据的责任交回提案人，而非伪装成 REJECT）；
    3. 豁免率 ≥ 阈值 ⇒ `REJECT_豁免率`；
    4. 不在/零触达热力图 ⇒ `REJECT_热力图缺失`（无样本解释量）；
    5. `savings ≤ cost` ⇒ `REJECT_编码长度`；
    6. 全过 ⇒ `ADMIT`。
    """
    hm = shadow.heatmap() if hm is None else hm
    ex = existing_rule_ids() if existing is None else existing
    if rule_id in ex:
        return {"rule_id": rule_id, "decision": "REFUSE_已有规则",
                "detail": "只对新规则准入；现有规则**不改不删**"}
    m = shadow.admit({"id": rule_id, "title": title}, hm)
    er = declared_exempt_rate if declared_exempt_rate is not None else exempt_rate(rule_id, hm)
    if er is None:
        return {"rule_id": rule_id, "decision": "PENDING_HUMAN",
                "detail": "无豁免率数据（提案人未声明且热力图无记录）⇒ 需人补，不代决",
                "savings_bits": m["savings_bits"], "cost_bits": m["cost_bits"]}
    if er >= EXEMPT_RATE_THRESHOLD:
        return {"rule_id": rule_id, "decision": "REJECT_豁免率",
                "detail": f"豁免率 {er} ≥ 阈值 {EXEMPT_RATE_THRESHOLD}",
                "exempt_rate": er, "savings_bits": m["savings_bits"],
                "cost_bits": m["cost_bits"]}
    if rule_id not in hm or m["samples_explained"] == 0:
        return {"rule_id": rule_id, "decision": "REJECT_热力图缺失",
                "detail": f"不在 VFDR 热力图（{len(hm)} 条在册）或零触达 ⇒ "
                          "samples_explained=0 ⇒ 必 reject",
                "exempt_rate": er, "savings_bits": m["savings_bits"],
                "cost_bits": m["cost_bits"]}
    if not m["admit"]:
        return {"rule_id": rule_id, "decision": "REJECT_编码长度",
                "detail": f"savings({m['savings_bits']}) ≤ cost({m['cost_bits']})",
                "exempt_rate": er, "savings_bits": m["savings_bits"],
                "cost_bits": m["cost_bits"]}
    return {"rule_id": rule_id, "decision": "ADMIT",
            "detail": f"长度 OK（savings {m['savings_bits']} > cost {m['cost_bits']}）"
                      f"· 豁免率 {er} < {EXEMPT_RATE_THRESHOLD}",
            "exempt_rate": er, "savings_bits": m["savings_bits"],
            "cost_bits": m["cost_bits"]}


def trial_stats() -> dict[str, Any]:
    """复现 636 试运行数字（admit/reject + 两半通过率），并补**实测豁免率**分布。"""
    t = shadow.trial()
    hm = shadow.heatmap()
    rates = [exempt_rate(r["id"], hm) for r in shadow.rules()]
    known = [x for x in rates if x is not None]
    return {"total": t["total"], "admitted": t["admitted"], "rejected": t["rejected"],
            "admit_rate_pct": t["admit_rate_pct"],
            "early_rate_pct": t["early_rate_pct"], "recent_rate_pct": t["recent_rate_pct"],
            "heatmap_rules": len(hm), "not_in_heatmap": len([r for r in shadow.rules()
                                                            if r["id"] not in hm]),
            "zero_touched": len([r for r in shadow.rules()
                                 if shadow.samples_explained(r["id"], hm) == 0]),
            "exempt_known": len(known),
            "exempt_mean": round(sum(known) / len(known), 4) if known else None}


#: 合成热力图条目（**只为让合成候选走到 ADMIT/编码长度分支**；不是真实数据）
SYNTH_HEATMAP: dict[str, dict[str, bool]] = {
    "CAND-SHORT-001": {"R1": True, "R2": False},
    "CAND-LONG-001": {"R1": True, "R2": False},
}


def demo_candidates() -> list[dict[str, Any]]:
    """候选新规则（**合成**，用于验证准入边界；不是真实提案）。"""
    return [
        {"rule_id": "CAND-SHORT-001", "title": "短标题规则",
         "declared_exempt_rate": 0.10, "synthetic": True},
        {"rule_id": "CAND-LONG-001", "title": "冗长标题" * 60,
         "declared_exempt_rate": 0.10, "synthetic": True},
        {"rule_id": "CAND-NODATA-001", "title": "无豁免率数据",
         "declared_exempt_rate": None, "synthetic": True},
        {"rule_id": "CAND-HIGH-EXEMPT-001", "title": "高豁免率",
         "declared_exempt_rate": 0.85, "synthetic": True},
        {"rule_id": "ATOM-REL-TARGET-HC", "title": "（已在册）HC 规则",
         "declared_exempt_rate": 0.0, "synthetic": True},
        {"rule_id": "CAND-NEWDIR-X", "title": "新方向但无热力图",
         "declared_exempt_rate": 0.0, "synthetic": True},
    ]


def run_admission(candidates: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    hm = dict(shadow.heatmap())
    hm.update(SYNTH_HEATMAP)          # 只为触达 ADMIT/编码长度分支（合成，已标注）
    ex = existing_rule_ids()
    cands = demo_candidates() if candidates is None else candidates
    rows = [admit_new_rule(c["rule_id"], c.get("title", ""), hm=hm, existing=ex,
                           declared_exempt_rate=c.get("declared_exempt_rate"))
            for c in cands]
    return {"rows": rows, "n": len(rows),
            "by_decision": _count(rows), "trial_stats": trial_stats()}


def _count(rows: list[dict[str, Any]]) -> dict[str, int]:
    d: dict[str, int] = {}
    for r in rows:
        d[r["decision"]] = d.get(r["decision"], 0) + 1
    return d


def write_meta(rows: list[dict[str, Any]]) -> str:
    """准入结论写入**侧车元数据**（不改 gate_engine；被拒规则**不删除**）。"""
    payload = {"version": VERSION, "existing_rules_untouched": True,
               "note": "本文件只记**新规则**准入结论；被拒规则保留（不删除、不改现有 67 条）",
               "exempt_rate_threshold": EXEMPT_RATE_THRESHOLD,
               "exempt_rate_reference_636": EXEMPT_RATE_REFERENCE,
               "decisions": rows}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_JSON


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "编码长度是**启发式**（非严格 MDL）⇒ 可能误杀好规则",
         "trigger": "被 reject 的规则事后证明拦到了真实攻击",
         "rollback": "侧车元数据里 `REJECT_*` **保留全部信息**（savings/cost/理由）⇒ "
                     "人可直接改判并重新入库；**没有任何规则被删除**"},
        {"risk": "热力图缺失被判必 reject ⇒ 可能扼杀新方向",
         "trigger": "新方向规则长期无触达数据（需先有攻击样本）",
         "rollback": "先在沙箱跑攻击补齐热力图，再重提；或人工豁免（本批不自动化）"},
        {"risk": "豁免率阈值 0.30 是启发式",
         "trigger": "大量规则卡在阈值附近",
         "rollback": "阈值是单一常量 `EXEMPT_RATE_THRESHOLD`，改动一行 + 重跑报告即可"},
    ]


def write_report() -> str:
    r = run_admission()
    s = r["trial_stats"]
    lines = [
        "# 642 A5 · MDL 规则准入上岗（**只对新规则**；现有 67 条零改动）", "",
        "## 一、准入判据", "",
        "| 判据 | 口径 | 不过的后果 |", "|---|---|---|",
        "| 编码长度 | 复用 636：`savings > L(rule)` | `REJECT_编码长度` |",
        "| 热力图覆盖 | 必须在 VFDR 热力图且**至少触达 1 轮** | `REJECT_热力图缺失` |",
        f"| 豁免率 | 实测豁免率 < **{EXEMPT_RATE_THRESHOLD}** | `REJECT_豁免率`；无数据 ⇒ "
        "`PENDING_HUMAN` |",
        "| 是否已有 | 已在册 ⇒ 拒绝更新 | `REFUSE_已有规则` |", "",
        "## 二、现状复现（实测，非抄 636）", "",
        f"- 在册规则：**{s['total']}**；热力图覆盖：**{s['heatmap_rules']}**；"
        f"**不在热力图：{s['not_in_heatmap']}**；**零触达：{s['zero_touched']}**",
        f"- 636 试运行复现：admit **{s['admitted']}** / reject **{s['rejected']}**"
        f"（通过率 {s['admit_rate_pct']}%）",
        f"- 两半通过率：早期 **{s['early_rate_pct']}%** → 近期 **{s['recent_rate_pct']}%**",
        f"- **实测豁免率**（未触达轮占比）：有数据 {s['exempt_known']} 条，"
        f"均值 **{s['exempt_mean']}**", "",
        "### 2.1 口径澄清（诚实）", "",
        "636 报告 §三 把「通过率」误题为「豁免率趋势」（66.7% → 23.5%）。642 区分：",
        "`admit_rate` = 规则分两半各自的 `savings > cost` 通过率；"
        "`exempt_rate` = **6 轮攻击中未触达的轮次占比**。**两者不可混用**。",
        f"task 要求的「近期 23.5% 作准入参考」→ `EXEMPT_RATE_REFERENCE="
        f"{EXEMPT_RATE_REFERENCE}`（只作量级参考），实际阈值为 "
        f"`EXEMPT_RATE_THRESHOLD={EXEMPT_RATE_THRESHOLD}`（在其上留余量）。", "",
        "## 三、准入实跑（候选为**合成**，用于验证边界）", "",
        "| 候选规则 | 结论 | 理由 |", "|---|---|---|"]
    for x in r["rows"]:
        lines.append(f"| `{x['rule_id']}` | **{x['decision']}** | {x['detail']} |")
    lines += ["", f"- 结论分布：`{r['by_decision']}`",
              "- 侧车元数据：`data/642_rule_admission.json`（**只含新规则**；被拒规则保留）",
              "- 合成候选用 `SYNTH_HEATMAP` 补热力图条目，**只为触达 ADMIT/编码长度分支**", "",
              "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **编码长度/豁免率都是启发式**，**可能误杀好规则**（§十.4）；",
              f"2. 实测与 636 备忘有差异：636 记「7 条不在热力图」，642 实测 **{s['not_in_heatmap']} 条**"
              f"（以**实测**为准，差异原因未定位）；",
              "3. 热力图缺失/零触达的规则**可能是新方向**（4 条 HC 规则即为例）⇒ 判 reject 是"
              "**保守**选择，不表示它们无价值；",
              "4. **现有 67 条规则零改动**（本模块只读 gate_engine；侧车元数据只记新规则）；",
              "5. **被拒规则不删除**：全部结论（含 reject 理由与 savings/cost）保留在侧车，可人工改判；",
              "6. 候选清单为**合成**，本批**没有真实新规则提案**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    write_meta(r["rows"])
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    hm = dict(shadow.heatmap())
    hm.update(SYNTH_HEATMAP)      # 合成条目：让 ADMIT / 编码长度分支可达
    ex = existing_rule_ids()
    long_title = "长标题" * 400
    chk("67 在册规则", len(ex) == 67, str(len(ex)))

    # 实测：4 条不在热力图 + 33 条零触达（636 备忘记「7 条」，以实测为准）
    real_hm = shadow.heatmap()
    missing = [r["id"] for r in shadow.rules() if r["id"] not in real_hm]
    chk("实测 4 条不在热力图", len(missing) == 4, str(missing))
    chk("零触达条数 = 33", trial_stats()["zero_touched"] == 33)

    # 六种结论全部可达
    chk("① 已在册 ⇒ REFUSE",
        admit_new_rule(ex[0], "T", hm=hm, existing=ex)["decision"] == "REFUSE_已有规则")
    chk("② 无豁免率数据 ⇒ PENDING_HUMAN（不代决）",
        admit_new_rule("CAND-NODATA-001", "T", hm=hm, existing=ex,
                       declared_exempt_rate=None)["decision"] == "PENDING_HUMAN")
    chk("③ 豁免率 ≥ 阈值 ⇒ REJECT_豁免率",
        admit_new_rule("CAND-NODATA-001", "T", hm=hm, existing=ex,
                       declared_exempt_rate=0.9)["decision"] == "REJECT_豁免率")
    chk("④ 不在热力图 ⇒ REJECT_热力图缺失",
        admit_new_rule("CAND-NEWDIR-X", "T", hm=hm, existing=ex,
                       declared_exempt_rate=0.0)["decision"] == "REJECT_热力图缺失")
    chk("⑤ 超长标题 ⇒ REJECT_编码长度",
        admit_new_rule("CAND-LONG-001", long_title, hm=hm, existing=ex,
                       declared_exempt_rate=0.1)["decision"] == "REJECT_编码长度")
    chk("⑥ 全过 ⇒ ADMIT",
        admit_new_rule("CAND-SHORT-001", "短标题", hm=hm, existing=ex,
                       declared_exempt_rate=0.1)["decision"] == "ADMIT")

    # 豁免率计算 + 边界（实测口径：未触达轮占比）
    er = exempt_rate("ATOM-FM-REQUIRED", real_hm)
    chk("豁免率 ∈ [0,1]", er is not None and 0.0 <= er <= 1.0, str(er))
    chk("无热力图记录 ⇒ None", exempt_rate("__nope__", real_hm) is None)
    chk("阈值边界：0.30 不通过（>= 即 reject）",
        admit_new_rule("CAND-SHORT-001", "短标题", hm=hm, existing=ex,
                       declared_exempt_rate=EXEMPT_RATE_THRESHOLD)["decision"]
        == "REJECT_豁免率")
    chk("阈值边界：0.2999 通过",
        admit_new_rule("CAND-SHORT-001", "短标题", hm=hm, existing=ex,
                       declared_exempt_rate=0.2999)["decision"] == "ADMIT")
    fb = admit_new_rule("CAND-SHORT-001", "短标题", hm=hm, existing=ex,
                        declared_exempt_rate=None)
    chk("缺声明时回退**实测**豁免率（2 轮触 1 轮 ⇒ 0.5 ≥ 阈值 ⇒ reject）",
        fb["decision"] == "REJECT_豁免率" and fb.get("exempt_rate") == 0.5,
        f"{fb['decision']} er={fb.get('exempt_rate')}")

    # 元数据只含新规则（已在册的候选被 REFUSE，不计入准入面）
    payload = {"decisions": run_admission()["rows"]}
    chk("侧车元数据不含现有 67 规则",
        all(d["rule_id"] not in ex for d in payload["decisions"]
            if d["decision"] != "REFUSE_已有规则"))
    chk("六种结论全覆盖", set(run_admission()["by_decision"]) == set(DECISIONS),
        str(sorted(run_admission()["by_decision"])))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    chk("侧车路径在 data 下", OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A5 MDL 规则准入上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + 侧车元数据")
    ap.add_argument("--json", action="store_true", help="打印准入结论（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = run_admission()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    s = r["trial_stats"]
    print(f"[mdl-gate] 在册 {s['total']}；热力图 {s['heatmap_rules']}（缺失 {s['not_in_heatmap']}）；"
          f"候选 {r['n']} ⇒ {r['by_decision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
