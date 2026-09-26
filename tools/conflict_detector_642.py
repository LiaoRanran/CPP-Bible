"""642 A1 · 冲突检测器**灰度上岗**（`--mode shadow|flag`；`block` 明确未实现，留 643）。

**与 636 的关系**：检测逻辑**不复制**——直接复用 636 影子实现（`conflict_detector_636`），
本模块只加**上岗层**：三档模式 + 「只加标记、不改判决」的机械契约。

| 模式 | 行为 | 本批状态 |
|---|---|---|
| `shadow` | 只离线出报告，判决结果**不带任何字段** | ✅ 保留（636 同款） |
| `flag` | 在判决结果上加 `conflict_flag` / `conflict_types` / `conflict_strength`，**不改 pass/fail** | ✅ 本批上岗 |
| `block` | 超阈时**拦截**判决 | ⛔ **未实现**（留 643；本批只灰度） |

**灰度契约（机械可验）**：
1. `flag_decision(decision, det)` 返回的字典除 `conflict_*` 三个字段外，与 `decision.to_dict()`
   **逐字段相等**（含 `decision_id` 与 `state`）；
2. 判决对象是 **641 内核 `Decision`**（保护器**消费**内核判决，内核**不依赖**保护器）；
3. `block` 模式**显式拒绝执行**（exit 2），不静默降级为 flag。

**诚实登记**（§十.1）：灰度上岗 **≠ 有效**。flag 只标记，不证明"拦截后系统更安全"；
有效性需要 643+ 的真实运行数据。θ=0.3 沿用 636 初值，未用真实样本回填。

只读契约：`--check` 只读、exit 0、不写盘；`--report` 写 `data/642_conflict_flag_run.md`。
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

import conflict_detector_636 as shadow  # noqa: E402  （检测逻辑单一真源，不复制）
import queyi_core_v10_641 as core  # noqa: E402  （判决对象用 641 内核协议）

OUT_MD = os.path.join(ROOT, "data", "642_conflict_flag_run.md")
MODES = ("shadow", "flag", "block")
BLOCK_IMPLEMENTED = False
FLAG_FIELDS = ("conflict_flag", "conflict_types", "conflict_strength")


def flag_decision(decision: core.Decision, det: dict[str, Any]) -> dict[str, Any]:
    """灰度 flag：**只加标记，不改判决**。

    返回值 = `decision.to_dict()` + 三个 `conflict_*` 字段；`state` / `decision_id`
    等一切原有字段**逐字不变**（由 `verdict_unchanged()` 机械核验）。
    """
    out = decision.to_dict()
    for k in FLAG_FIELDS:
        out.pop(k, None)          # 幂等：重复 flag 不叠加
    out["conflict_flag"] = bool(det.get("exceeds_theta"))
    out["conflict_types"] = list(det.get("types", []))
    out["conflict_strength"] = float(det.get("C", 0.0))
    return out


def verdict_unchanged(before: dict[str, Any], after: dict[str, Any]) -> bool:
    """除三个 `conflict_*` 字段外，前后**其余字段完全相等**（灰度契约 1）。"""
    keys = {k for k in set(before) | set(after) if not k.startswith("conflict_")}
    return all(before.get(k) == after.get(k) for k in keys)


def flag_card(card_rel: str, card_text: str, rules: list[dict[str, str]],
              ev_index: Optional[set[str]] = None) -> dict[str, Any]:
    """对单张卡实跑 flag 模式。

    **占位判决的来路（诚实）**：保护器**不产出判决**，真实判决来自 `gate_engine`。
    此处按 636 影子口径把 `status: verified` 映为内核四态的 `pass`，**仅用于**机械证明
    "加标记不改 pass/fail"；`reason` 字段写明这是占位判决。
    """
    det = shadow.detect(card_text, rules, ev_index=ev_index)
    artifact = core.Artifact.from_bytes(card_text.encode("utf-8"), "atom_card", uri=card_rel)
    decision = core.Decision.make(artifact.artifact_id, "pass",
                                  reasons=["占位判决：status: verified ⇒ 636 影子口径 pass"])
    flagged = flag_decision(decision, det)
    return {"card": card_rel, "detection": det, "decision_before": decision.to_dict(),
            "decision_after": flagged, "flagged": flagged["conflict_flag"],
            "unchanged": verdict_unchanged(decision.to_dict(), flagged)}


def run_flag() -> dict[str, Any]:
    """对全部 verified 卡（636 口径）实跑 flag 模式，输出冲突标记清单。"""
    rules = shadow.load_rules()
    rows = [flag_card(rel, text, rules) for rel, text in shadow.verified_cards()]
    marked = [r for r in rows if r["flagged"]]
    return {"mode": "flag", "theta": shadow.THETA, "n_cards": len(rows),
            "n_marked": len(marked), "n_verdict_changed": sum(0 if r["unchanged"] else 1
                                                             for r in rows),
            "type_dist": _type_dist(rows), "rows": rows, "marked": marked}


def _type_dist(rows: list[dict[str, Any]]) -> dict[str, int]:
    dist: dict[str, int] = {}
    for r in rows:
        for t in r["detection"]["types"]:
            dist[t] = dist.get(t, 0) + 1
    return dist


def risk_assessment() -> list[dict[str, str]]:
    """误判风险评估 + 回滚方案（每项：风险 / 触发条件 / 回滚动作）。"""
    return [
        {"risk": "θ=0.3 为 636 初值，未用真实样本回填 ⇒ 可能过紧（误标）或过松（漏标）",
         "trigger": "标记清单出现人工确认无冲突的卡",
         "rollback": "`--mode shadow` 立即回到只出报告；θ 调整需人审后改 THETA 并重跑"},
        {"risk": "RR 型是**全局规则集属性**（block 44 + warn 16 恒定共存）⇒ 所有卡 RR=1，区分度有限",
         "trigger": "RR 恒定导致 `conflict_raw` 基线抬高",
         "rollback": "报告已按型分列；如需按型定阈，643 再拆 θ_RR/θ_EE"},
        {"risk": "`agreement` 用「被引用证据存在率」近似，**非统计一致度**",
         "trigger": "悬挂引用（证据文件缺失）被当成冲突",
         "rollback": "只加标记不改判决 ⇒ 最坏后果是人工复核队列变长，不影响任何判 pass/fail"},
        {"risk": "占位判决（verified ⇒ pass）与 gate 真实判决未必一致",
         "trigger": "有人把本模块的 `decision_after` 当成生产判决使用",
         "rollback": "占位判决的 `reason` 字段自带声明；生产判决唯一来源仍是 gate_engine"},
    ]


def rollback_plan() -> list[dict[str, str]]:
    """A6 联调统一接口（与 A2–A5 同名，供 `protector_rollout_642.risk_summary()` 汇总）。"""
    return risk_assessment()


def write_report() -> str:
    s = run_flag()
    lines = [
        "# 642 A1 · 冲突检测器灰度上岗（flag 模式，**未拦截、未改判**）", "",
        "## 一、三档模式", "",
        "| 模式 | 行为 | 本批 |", "|---|---|---|",
        "| shadow | 离线报告，判决不带字段 | 保留 |",
        "| **flag** | 加 `conflict_flag`/`types`/`strength`，**不改 pass/fail** | ✅ **上岗** |",
        "| block | 超阈拦截 | ⛔ 未实现（留 643） |", "",
        "## 二、flag 模式实跑（全部 verified 卡）", "",
        f"- verified 卡：**{s['n_cards']}**；标记（C ≥ θ={s['theta']}）：**{s['n_marked']}**",
        f"- **判决被改变数：{s['n_verdict_changed']}**（必须为 0 —— 灰度契约）",
        f"- 型分布：`{s['type_dist']}`", "",
        "## 三、冲突标记清单", "",
        "| 卡 | 型 | raw | agreement | C | 标记 | 判决未变 |",
        "|---|---|---|---|---|---|---|"]
    for r in s["rows"]:
        d = r["detection"]
        lines.append(f"| `{r['card'].split('/')[-1][:-3]}` | {'/'.join(d['types']) or '—'} | "
                     f"{d['conflict_raw']} | {d['agreement']} | {d['C']} | "
                     f"{'⚠️' if r['flagged'] else '—'} | {'✅' if r['unchanged'] else '❌'} |")
    lines += ["", "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for r in risk_assessment():
        lines.append(f"| {r['risk']} | {r['trigger']} | {r['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **灰度上岗 ≠ 有效**：flag 只标记，不证明「拦截后更安全」（§十.1）；",
              "2. θ=0.3 沿用 636 初值，**未用真实样本回填**（交人项）；",
              "3. RR 为全局规则集属性 ⇒ 23/23 恒为 1，**区分度有限**（636 已登记，本批未改善）；",
              "4. 占位判决（verified ⇒ pass）只为机械证明「加标记不改判决」，非生产判决；",
              "5. **不合并不修改**任何历史判决/账本（append-only 铁律）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rules = [{"id": "A", "severity": "block", "scope": "atom"},
             {"id": "B", "severity": "warn", "scope": "atom"}]
    good = {"EV-T-%03d" % i for i in range(17)}

    # 已知冲突卡（20 引用 / 3 悬挂 ⇒ ee=1，C=0.3 边界）必标记
    conflict_text = ("status: verified\nevidence: ["
                     + ", ".join("EV-T-%03d" % i for i in range(20)) + "]\n")
    d_conf = shadow.detect(conflict_text, rules, ev_index=good)
    chk("已知冲突卡 C=0.3 且超阈", d_conf["C"] == 0.3 and d_conf["exceeds_theta"] is True,
        f"C={d_conf['C']}")

    # 已知无冲突卡（引用全存在 ⇒ agreement=1 ⇒ C=0）不标记
    clean_text = ("status: verified\nevidence: ["
                  + ", ".join("EV-T-%03d" % i for i in range(7)) + "]\n")
    d_clean = shadow.detect(clean_text, rules, ev_index=good)
    chk("已知无冲突卡 C=0 且不超阈", d_clean["C"] == 0.0 and d_clean["exceeds_theta"] is False,
        f"C={d_clean['C']}")

    # 阈值边界：C 恰等于 θ ⇒ 标记（>=）；略低 ⇒ 不标记
    near = {"EV-T-%03d" % i for i in range(18)}
    d_below = shadow.detect(conflict_text, rules, ev_index=near)
    chk("阈值边界：C<θ 不标记", d_below["C"] < shadow.THETA
        and d_below["exceeds_theta"] is False, f"C={d_below['C']}")

    # 灰度契约：加标记不改判决
    dec = core.Decision.make("a1", "pass", reasons=["r"], rule_ids=["R1"])
    flagged = flag_decision(dec, d_conf)
    chk("flag 不改判决（state/decision_id 保留）",
        flagged["state"] == dec.state and flagged["decision_id"] == dec.decision_id)
    chk("flag 契约机械核验通过", verdict_unchanged(dec.to_dict(), flagged) is True)
    chk("flag 字段齐全", all(k in flagged for k in FLAG_FIELDS))
    chk("flag 幂等（重复叠加不改变字段集）",
        set(flag_decision(dec, d_conf)) == set(flagged))

    # block 模式明确未实现
    chk("block 未实现（显式拒绝）", BLOCK_IMPLEMENTED is False)
    chk("--mode block 返回 exit 2", main(["--mode", "block"]) == 2)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A1 冲突检测器灰度上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写灰度报告")
    ap.add_argument("--json", action="store_true", help="打印标记清单（JSON）")
    ap.add_argument("--mode", choices=MODES, default="flag", help="灰度档位")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.mode == "block":
        print("block 模式未实现（留 643）。本批只做灰度：请用 --mode flag 或 shadow。")
        return 2
    if a.mode == "shadow":
        s = shadow.run_shadow()
        if a.json:
            print(json.dumps({k: v for k, v in s.items() if k != "rows"},
                             ensure_ascii=False, indent=2))
        else:
            print(f"[shadow] verified 卡 {s['n_cards']}；超阈 {s['over_theta']}；"
                  f"判决结果不带任何字段")
        return 0
    if a.report:
        print(f"written {write_report()}")
        return 0
    s = run_flag()
    if a.json:
        print(json.dumps({k: v for k, v in s.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[flag] verified 卡 {s['n_cards']}；标记 {s['n_marked']}；"
          f"判决被改变 {s['n_verdict_changed']}（应为 0）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
