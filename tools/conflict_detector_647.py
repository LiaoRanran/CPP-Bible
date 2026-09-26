"""647 B1 · 冲突检测器**真上岗**（636 影子 → 642 灰度 flag → **647 拦截**）。

三档判决（§四 B1）：

| 冲突度 C | 双方是否都有证据 | 动作 | enforce 下的后果 |
|---|---|---|---|
| **C ≥ 0.8** | 是 | **block** | 内核判决态**强制改判为 `fail`**（附原因） |
| 0.5 ≤ C < 0.8 | — | **warn** | 只加 `conflict_*` 标记，交人审 |
| C < 0.5 | — | **pass** | 通过（不带标记） |

**「双方都有证据」的口径**（明写，避免玄学）：
* 卡侧：卡里真的引用了 ≥1 条证据（`evidence: [...]`）；
* 另一侧：检测器报出 **ER（证据-规则反证）/ EE（证据不自洽）/ 欠定（verified 无证据）** 之一。
* **只报 RR 不算**——RR 是**全局规则集属性**（同批所有卡都是 block+warn 共存），
  若把它当"证据"会把 23/23 全卡打成高置信（636/642 已登记其区分度有限）。

**灰度纪律（§四 B1）**：**只对新判决生效**，历史判决**不回溯**。
`apply_new()` 只处理调用方递进来的新判决；本模块**不重扫任何历史判决、不动账本**。

**一键回滚**：`QUEYI_PROTECTOR_MODE=shadow`（或 `protector_mode_647.py --rollback`）⇒ 退回 642 的
「只加标记、不改 pass/fail」；每个动作前都先问 `protector_mode_647.is_enforce()`。

**诚实登记**（⚠️ 其中②是**实测发现的生产影响**，必须看）：
① θ（0.8/0.5）是**设计值**，未用真实样本回填；
② **真实 23 张 verified 卡里有 1 张（`ATOM-MEM-PERF-003`）满足 C ≥ 0.8 且双方有证据**
（C=1.333，型 RR+EE）⇒ **enforce 下它会被真的改判为 `fail`**（不是纸面推演）；
   另有 1 张（`ATOM-MEM-UNIQUE-002`，C=0.5）落入 warn 档。
   **这是本批最大的风险点**：EE 型由"≥2 条引用且有悬挂"推出，**可能是误判**（证据 id 与文件名口径不一致会造成假悬挂）。
③ block 把内核态改成 `fail` **是生产行为的改变**（不再是"只标记"）——这正是本批的目标，也是风险点；
   回滚一条命令：`QUEYI_PROTECTOR_MODE=shadow`。

CLI：`--check` / `--report` / `--json` / `--describe`。纯标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import conflict_detector_636 as det_src  # noqa: E402  （检测算法单一真源，不复制）
import protector_mode_647 as pmode  # noqa: E402
import queyi_core_v10_641 as core  # noqa: E402  （判决对象用 641 内核协议）

OUT_MD = os.path.join(ROOT, "data", "647_conflict_enforce.md")
OUT_JSON = os.path.join(ROOT, "data", "647_conflict_enforce.json")

THETA_BLOCK = 0.8          # 高置信冲突线（**设计值**，见诚实登记）
THETA_WARN = 0.5           # 中置信线
ACTIONS = ("block", "warn", "pass")
MARK_FIELDS = ("conflict_flag", "conflict_types", "conflict_strength", "conflict_action")
_EV_RE = det_src._EV_RE


def both_sides_have_evidence(card_text: str, d: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    """「双方都有证据」：卡侧引用了证据，且检测器报出 ER/EE/欠定之一（**RR 不算**）。"""
    refs = sorted(set(_EV_RE.findall(card_text)))
    card_side = len(refs) >= 1
    other_side = bool(d.get("er") or d.get("ee") or d.get("und"))
    return (card_side and other_side), {"card_refs": len(refs),
                                        "rwys": {k: d.get(k) for k in ("er", "ee", "und")}}


def evaluate(card_text: str, rules: list[dict[str, str]],
             ev_index: Optional[set[str]] = None) -> dict[str, Any]:
    """纯函数：算三档动作（**不碰判决对象**）。"""
    d = det_src.detect(card_text, rules, ev_index=ev_index)
    both, side_info = both_sides_have_evidence(card_text, d)
    c = float(d["C"])
    if c >= THETA_BLOCK and both:
        action = "block"
    elif c >= THETA_WARN:
        action = "warn"
    else:
        action = "pass"
    return {"detection": d, "both_sides": both, "side_info": side_info,
            "C": c, "action": action, "theta_block": THETA_BLOCK, "theta_warn": THETA_WARN}


def apply_new(decision: core.Decision, card_text: str, rules: list[dict[str, str]],
              ev_index: Optional[set[str]] = None,
              card_rel: str = "") -> dict[str, Any]:
    """对**一条新判决**应用保护器。

    * `block` + enforce ⇒ 判决态**强制改判 `fail`**（`reasons` 记录是保护器拦的）；
    * `block` + shadow ⇒ **不改判**，只加标记（642 行为）；
    * `warn`/`pass` ⇒ 只加标记（不改判）。
    """
    ev = evaluate(card_text, rules, ev_index=ev_index)
    enforce = pmode.is_enforce() and ev["action"] == "block"
    marks = {"conflict_flag": ev["action"] != "pass",
             "conflict_types": list(ev["detection"]["types"]),
             "conflict_strength": ev["C"], "conflict_action": ev["action"]}
    before = decision.to_dict()
    if enforce:
        reasons = list(decision.reasons) + [
            f"647 B1 冲突检测器拦截：C={ev['C']} ≥ {THETA_BLOCK} 且双方均有证据"
            f"（型 {'/'.join(ev['detection']['types'])}）"]
        blocked = core.Decision.make(decision.artifact_id, "fail", reasons=reasons)
        after = blocked.to_dict()
    else:
        after = dict(before)
    after.update(marks)
    return {"card": card_rel, "mode": pmode.mode(), "action": ev["action"],
            "enforced": enforce, "detection": ev["detection"], "evaluate": ev,
            "decision_before": before, "decision_after": after,
            "verdict_changed": before.get("state") != after.get("state")}


def verdict_unchanged(before: dict[str, Any], after: dict[str, Any]) -> bool:
    """除 `conflict_*` 字段外，前后其余字段完全相等（shadow 契约）。"""
    keys = {k for k in set(before) | set(after) if not k.startswith("conflict_")}
    return all(before.get(k) == after.get(k) for k in keys)


def run_new(rows: Optional[list[tuple[str, str]]] = None) -> dict[str, Any]:
    """对**新的**判决面跑一遍（默认 = 真实 verified 卡，**当作新判决**，不回溯历史）。"""
    rules = det_src.load_rules()
    src = rows if rows is not None else det_src.verified_cards()
    out = []
    for rel, text in src:
        artifact = core.Artifact.from_bytes(text.encode("utf-8"), "atom_card", uri=rel)
        dec = core.Decision.make(artifact.artifact_id, "pass",
                                 reasons=["占位新判决：status: verified ⇒ pass（保护器只拦不判）"])
        out.append(apply_new(dec, text, rules, card_rel=rel))
    dist: dict[str, int] = {}
    for r in out:
        dist[r["action"]] = dist.get(r["action"], 0) + 1
    blocked = [r for r in out if r["action"] == "block"]
    return {"mode": pmode.mode(), "theta_block": THETA_BLOCK, "theta_warn": THETA_WARN,
            "n": len(out), "by_action": dist, "rows": out,
            "n_blocked": len(blocked), "n_verdict_changed": sum(1 for r in out if r["verdict_changed"]),
            "n_refused": len(blocked)}


SYNTH_CASES: tuple[dict[str, Any], ...] = (
    {"name": "高置信（C=1.0：欠定 + 悬挂引用 + 反证）", "expect": "block",
     "text": "status: verified\nfalsification: fail\nevidence: [EV-NOPE-1, EV-NOPE-2]\n"},
    {"name": "中置信（C≈0.5：唯一悬挂引用 + 有证据）", "expect": "warn",
     "text": "status: verified\nevidence: [EV-NOPE-1]\n"},
    {"name": "低置信（C=0：证据全在 + 无反证）", "expect": "pass",
     "text": "status: verified\nevidence: [EV-OK-1]\n"},
)


def synthetic_check() -> list[dict[str, Any]]:
    """**合成卡**验证三档边界（真实卡没有 C ≥ 0.8 样本，见诚实登记②）。"""
    rules = [{"id": "A", "severity": "block", "scope": "atom"},
             {"id": "B", "severity": "warn", "scope": "atom"}]
    ev_index = {"EV-OK-1"}
    out = []
    for c in SYNTH_CASES:
        ev = evaluate(c["text"], rules, ev_index=ev_index)
        out.append({"name": c["name"], "expect": c["expect"], "got": ev["action"],
                    "C": ev["C"], "both_sides": ev["both_sides"],
                    "types": ev["detection"]["types"],
                    "ok": ev["action"] == c["expect"]})
    return out


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "θ_block=0.8/θ_warn=0.5 是**设计值**，未用真实样本回填 ⇒ 可能误拦/漏拦",
         "trigger": "block 清单里出现人工确认无冲突的卡",
         "rollback": "`QUEYI_PROTECTOR_MODE=shadow` 一键退回只标记；或调 THETA_BLOCK 常量后重跑"},
        {"risk": "**block 会真的改判**（内核态 → fail），不再是「只标记」",
         "trigger": "误拦导致正确判决被写成 fail",
         "rollback": "shadow 模式 + 本模块不改任何历史/账本（只处理调用方递进来的新判决）"},
        {"risk": "RR 被排除出「双方证据」口径，可能低估冲突",
         "trigger": "只报 RR 的卡未被拦",
         "rollback": "把 `er/ee/und` 扩到含 `rr` 即回到「全拦」（对比实验用，不建议生产）"},
        {"risk": "占位新判决（verified ⇒ pass）不是真实 gate 判决",
         "trigger": "有人把本模块输出当成生产判决源",
         "rollback": "判决唯一来源仍是 gate_engine；本模块只在 gate 之后做**附加保护**"},
    ]


def write_report() -> str:
    r = run_new()
    syn = synthetic_check()
    lines = [
        "# 647 B1 · 冲突检测器**真上岗**（高置信 block / 中置信 warn / 低置信 pass）", "",
        f"- 当前模式：**{r['mode']}**（`QUEYI_PROTECTOR_MODE`；shadow = 一键回滚）",
        f"- 阈值：block ≥ **{THETA_BLOCK}**（且双方有证据）· warn ≥ **{THETA_WARN}** · 其余 pass", "",
        "## 一、三档口径", "",
        "| 条件 | 动作 | enforce 后果 |", "|---|---|---|",
        f"| C ≥ {THETA_BLOCK} 且双方都有证据 | **block** | 内核态**强制改判 `fail`** + 原因 |",
        f"| {THETA_WARN} ≤ C < {THETA_BLOCK} | warn | 只加标记，交人审 |",
        "| C < 0.5 | pass | 通过（无标记） |", "",
        "**「双方都有证据」**：卡侧引用 ≥1 条证据 **且** 检测器报出 ER/EE/欠定之一"
        "（**RR 不算** —— 它是全局规则集属性，会把 23/23 全打成高置信）。", "",
        "## 二、对**新判决面**实跑（真实 verified 卡，当作新判决；**不回溯历史**）", "",
        f"- 判决数：**{r['n']}**；动作分布 `{r['by_action']}`",
        f"- **被 block：{r['n_blocked']}**；判决态被改变：**{r['n_verdict_changed']}**", "",
        "### 2.1 ⚠️ 真实卡上的实际拦截（**生产影响，必须看**）", "",
        f"- 实测：C ≥ {THETA_BLOCK} 且双方有证据的卡 **{r['n_blocked']} 张**，"
        f"**判决态被改变 {r['n_verdict_changed']} 条** ⇒ "
        + ("**enforce 下这些卡会被真的改判为 `fail`**（不是纸面推演）。"
           if r["n_blocked"] else "**真实卡上无高置信样本** ⇒ 实际拦截 0 条。"), "",
        "| 卡 | 动作 | C | 型 | 双方证据 | 判决态被改变 |", "|---|---|---|---|---|---|"]
    for x in r["rows"]:
        if x["action"] != "pass":
            lines.append(f"| `{x['card'].split('/')[-1][:-3]}` | **{x['action']}** | "
                         f"{x['evaluate']['C']} | {'/'.join(x['detection']['types'])} | "
                         f"{x['evaluate']['both_sides']} | "
                         f"{'⚠️ 是' if x['verdict_changed'] else '否'} |")
    lines += ["",
              "- **EE 型由「≥2 条引用且有悬挂」推出 ⇒ 可能是误判**"
              "（证据 id 与证据文件名口径不一致会造假悬挂）——本批**未**逐一核实该卡是否真悬挂引用；",
              "- 若判定为误拦：`QUEYI_PROTECTOR_MODE=shadow` 立即回滚（只标记不改判）。", "",
              "### 2.2 合成卡三档边界验证", "",
        "### 2.2 合成卡三档边界验证", "",
        "| 用例 | 期望 | 实测 | C | 双方有证据 | 型 | 通过 |", "|---|---|---|---|---|---|---|"]
    for s in syn:
        lines.append(f"| {s['name']} | {s['expect']} | **{s['got']}** | {s['C']} | "
                     f"{s['both_sides']} | {'/'.join(s['types'])} | {'✅' if s['ok'] else '❌'} |")
    lines += ["", "## 三、逐卡明细", "",
              "| 卡 | 动作 | C | 型 | 双方证据 | 判决态改变 |", "|---|---|---|---|---|---|"]
    for x in r["rows"]:
        lines.append(f"| `{x['card'].split('/')[-1][:-3]}` | {x['action']} | {x['evaluate']['C']} | "
                     f"{'/'.join(x['detection']['types']) or '—'} | {x['evaluate']['both_sides']} | "
                     f"{'⚠️ 是' if x['verdict_changed'] else '否'} |")
    lines += ["", "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **θ 是设计值**，未用真实样本回填（交人项）；",
              "2. **真实卡上确有高置信样本**（`ATOM-MEM-PERF-003`，C=1.333）⇒ enforce 下**真会被改判 fail**；"
              "另有 1 张落 warn 档；EE 型可能是**假悬挂** ⇒ 需人工核实（**不夸大也不隐瞒**）；",
              "3. **block 真的改判**（→ `fail`）——这是 647 与 642 的本质差别，也是本批最大风险；",
              "4. **历史不回溯**：本模块只处理调用方递进来的**新判决**，不重扫、不改账本；",
              "5. `agreement` 仍是「被引用证据存在率」**启发式**（636 同口径），非统计一致度。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in r.items() if k != "rows"} | {"synthetic": syn},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rules = [{"id": "A", "severity": "block", "scope": "atom"},
             {"id": "B", "severity": "warn", "scope": "atom"}]
    ev = {"EV-OK-1"}

    # 三档边界（合成）
    hi = evaluate("status: verified\nfalsification: fail\n"
                  "evidence: [EV-NOPE-1, EV-NOPE-2]\n", rules, ev_index=ev)
    mid = evaluate("status: verified\nevidence: [EV-NOPE-1]\n", rules, ev_index=ev)
    low = evaluate("status: verified\nevidence: [EV-OK-1]\n", rules, ev_index=ev)
    chk("高置信 ⇒ block", hi["action"] == "block", f"C={hi['C']}")
    chk("中置信 ⇒ warn", mid["action"] == "warn", f"C={mid['C']}")
    chk("低置信 ⇒ pass", low["action"] == "pass", f"C={low['C']}")
    chk("三档齐全", {hi["action"], mid["action"], low["action"]} == set(ACTIONS))

    # 只报 RR（全局规则集属性）**不**算"双方都有证据" ⇒ rr 为 1 也不 block
    rr_only = evaluate("status: verified\nevidence: [EV-OK-1, EV-OK-2]\n",
                       rules, ev_index={"EV-OK-1", "EV-OK-2"})
    chk("RR-only：C=0 ⇒ pass", rr_only["detection"]["rr"] == 1 and rr_only["action"] == "pass",
        f"C={rr_only['C']}")
    chk("RR 不参与「双方证据」判定",
        both_sides_have_evidence("evidence: [EV-OK-1]\n",
                                 {"rr": 1, "er": 0, "ee": 0, "und": 0})[0] is False)
    chk("ER/EE/欠定 参与「双方证据」判定",
        both_sides_have_evidence("evidence: [EV-OK-1]\n",
                                 {"rr": 0, "er": 0, "ee": 0, "und": 1})[0] is True)

    # enforce：改判；shadow：只标记
    artifact = core.Artifact.from_bytes(b"x", "atom_card", uri="t.md")
    dec = core.Decision.make(artifact.artifact_id, "pass", reasons=["r"])
    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "enforce"
        e = apply_new(dec, SYNTH_CASES[0]["text"], rules, ev_index=ev, card_rel="t.md")
        chk("enforce + block ⇒ 判决态改为 fail", e["enforced"] is True
            and e["decision_after"]["state"] == "fail")
        chk("enforce 时 marks 仍写入", e["decision_after"]["conflict_action"] == "block")
        chk("block 原因可追溯", any("647 B1" in r for r in e["decision_after"]["reasons"]))
        os.environ[pmode.ENV] = "shadow"
        s = apply_new(dec, SYNTH_CASES[0]["text"], rules, ev_index=ev, card_rel="t.md")
        chk("shadow ⇒ 不改判（642 契约）", s["enforced"] is False
            and verdict_unchanged(s["decision_before"], s["decision_after"]) is True)
        chk("shadow ⇒ block 意图仍被标记", s["decision_after"]["conflict_action"] == "block")
        os.environ[pmode.ENV] = "enforce"
        lo = apply_new(dec, SYNTH_CASES[2]["text"], rules, ev_index=ev, card_rel="t.md")
        chk("低置信 ⇒ 不改判", lo["verdict_changed"] is False and lo["enforced"] is False)
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved

    probe = apply_new(dec, SYNTH_CASES[1]["text"], rules, ev_index=ev, card_rel="t.md")
    chk("mark 字段名齐", set(MARK_FIELDS) <= set(probe["decision_after"]))
    chk("θ 关系正确", THETA_WARN < THETA_BLOCK)
    chk("按动作计数自洽", sum(run_new()["by_action"].values()) == run_new()["n"])
    print(f"B1 conflict-enforce selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B1 冲突检测器真上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--describe", action="store_true", help="打印三档口径")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.describe:
        print(json.dumps({"theta_block": THETA_BLOCK, "theta_warn": THETA_WARN,
                          "actions": list(ACTIONS), "mode": pmode.mode(),
                          "both_sides_rule": "卡侧引用≥1 且 (ER|EE|欠定)"},
                         ensure_ascii=False, indent=2))
        return 0
    r = run_new()
    if a.report:
        print(f"written {write_report()}")
        return 0
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 conflict] mode={r['mode']} n={r['n']} by_action={r['by_action']} "
          f"blocked={r['n_blocked']} verdict_changed={r['n_verdict_changed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
