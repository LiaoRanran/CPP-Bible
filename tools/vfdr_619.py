"""619 A3 · VFDR（Vulnerability-Feedback-Driven Repair）状态机 v1

漏洞 → 修复 → 验证闭环。纯标准库、只读（`--check` 不写盘）。

状态：`OPEN → TRIAGED → FIXING → VERIFYING → CLOSED`（CLOSED 可 REOPEN 回 FIXING）
事件：TRIAGE / START_FIX / FIX_SHIPPED / VERIFY_PASS / VERIFY_FAIL / REOPEN

三条历史教训复盘（种子漏洞，演示闭环）：
- VFDR-585：红队发现 meta 攻击面（供应链溯源 / 信任根 / Merkle 证明）缺口
- VFDR-615：EV-MATRIX 规则误报（双实现一致率仅 68.4%）
- VFDR-616：CP 置信偷看（e-process 之前置信序列被反复偷看，虚报 13.80%）

铁律：新工具必有 `--check`（只读自验证，exit 0）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

DEFAULT_REPORT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "vfdr_619.md")

STATES: tuple[str, ...] = ("OPEN", "TRIAGED", "FIXING", "VERIFYING", "CLOSED")
TRANSITIONS: dict[str, dict[str, str]] = {
    "OPEN": {"TRIAGE": "TRIAGED"},
    "TRIAGED": {"START_FIX": "FIXING"},
    "FIXING": {"FIX_SHIPPED": "VERIFYING"},
    "VERIFYING": {"VERIFY_PASS": "CLOSED", "VERIFY_FAIL": "FIXING"},
    "CLOSED": {"REOPEN": "FIXING"},
}
CANONICAL_CLOSE: tuple[str, ...] = ("TRIAGE", "START_FIX", "FIX_SHIPPED", "VERIFY_PASS")


def can_transition(state: str, event: str) -> bool:
    return event in TRANSITIONS.get(state, {})


def transition(state: str, event: str) -> str:
    if event not in TRANSITIONS.get(state, {}):
        raise ValueError(f"非法转移：{state} --{event}--> ?（允许：{sorted(TRANSITIONS.get(state, {}))}）")
    return TRANSITIONS[state][event]


def seed_lessons() -> list[dict]:
    """三历史教训作为种子漏洞（state=OPEN，含真实修复落点，用于演示闭环）。"""
    return [
        {
            "id": "VFDR-585", "source": "REDTEAM", "severity": "critical",
            "title": "红队：meta 攻击面缺口（供应链溯源 / 信任根 / Merkle 证明）",
            "lesson": "验证系统未覆盖三层 meta 攻击：依赖链投毒、信任根缺失、证明树被篡改。",
            "fix": "601 supply_chain.py / merkle_integrity.py + 614 trust_root_status_check（in-toto HMAC / OTS / Merkle proof 三链）",
            "state": "OPEN", "history": [],
        },
        {
            "id": "VFDR-615", "source": "MATRIX", "severity": "high",
            "title": "EV-MATRIX 规则误报（双实现一致率仅 68.4%）",
            "lesson": "ev_matrix_unbacked 单实现与 gate_engine 隐性剥字段（artifact_sha256 行），导致 31.6% 分歧 = 误报/漏报。",
            "fix": "616 ev_matrix_unbacked_v2.py（独立语义）+ ev_matrix_dual_impl_lock.py（双实现锁 100%）",
            "state": "OPEN", "history": [],
        },
        {
            "id": "VFDR-616", "source": "STATS", "severity": "high",
            "title": "CP 置信偷看（e-process 之前置信序列被反复偷看）",
            "lesson": "置信序列在「看结果后」反复调参，虚报逃逸率 13.80%；统计偷看夸大确定性。",
            "fix": "616 confidence_sequence.py（Beta-混合 e-process，anytime 0.9062% vs CP 0.3370%；偷看虚报归零）",
            "state": "OPEN", "history": [],
        },
    ]


def apply_event(vuln: dict, event: str) -> str:
    """确定性地把事件作用到漏洞上，更新 state 并追加 history。"""
    new_state = transition(vuln["state"], event)
    vuln["state"] = new_state
    vuln.setdefault("history", []).append({"event": event, "to": new_state})
    return new_state


def simulate(vuln: dict, events: tuple[str, ...]) -> str:
    for ev in events:
        apply_event(vuln, ev)
    return vuln["state"]


def render_markdown() -> str:
    out: list[str] = []
    out.append("# 619 A3 · VFDR 状态机 v1（漏洞反馈驱动修复）\n")
    out.append("## 一、状态机定义")
    out.append(f"- 状态集：`{' → '.join(STATES)}`")
    out.append("- 转移表：\n")
    out.append("| 当前状态 | 事件 | 下一个状态 |")
    for s in STATES:
        for ev, nxt in TRANSITIONS[s].items():
            out.append(f"| {s} | {ev} | {nxt} |")
    out.append("")
    out.append("> 闭环：VERIFY_FAIL 退回 FIXING 重修；CLOSED 可 REOPEN 回 FIXING（回归则重开）。\n")

    out.append("## 二、三历史教训复盘（种子漏洞，演示闭环）")
    for v in seed_lessons():
        sim = dict(v)
        final = simulate(sim, CANONICAL_CLOSE)
        out.append(f"### {v['id']} · {v['title']}")
        out.append(f"- 来源：`{v['source']}` · 严重度：`{v['severity']}`")
        out.append(f"- 教训：{v['lesson']}")
        out.append(f"- 修复落点（历史真实）：{v['fix']}")
        out.append(f"- VFDR 闭环：OPEN `{' → '.join(CANONICAL_CLOSE)}` → **{final}** "
                   f"（路径：`{' → '.join(['OPEN'] + list(CANONICAL_CLOSE))}`）")
        out.append("")
    out.append("## 三、与 A1/A2 的前向链路（留 620）")
    out.append("- A2 的 `ranked` Top20 排序 → 可自动开 `VFDR-*` OPEN 条目（按 A1 子目标分类：")
    out.append("  `rule_blind_spot→MATRIX` / `provenance→REDTEAM` / `verdict_regime_disagreement→GOV`）。")
    out.append("- 闭环闸门：`VERIFY_PASS` 须由**真实门禁**（gate + replay，非攻击方自评）确认，")
    out.append("  与 619 §六「不跑监工门禁」一致：A3 只设计机，不自行宣布修复通过。")
    out.append("")
    out.append("## 四、已知限制")
    out.append("- 状态机是**确定性骨架**，不含时间/人审判定；真实 `REOPEN` 由人/CI 触发。")
    out.append("- 三历史教训已 CLOSED（修复已落历史批次）；本机只做**结构闭环演示**，不重新执行其修复。")
    return "\n".join(out)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("所有转移目标都是合法状态", all(nxt in STATES for d in TRANSITIONS.values() for nxt in d.values()))
    chk("非法转移被拒绝", not can_transition("OPEN", "FIX_SHIPPED")
        and not can_transition("CLOSED", "TRIAGE"))
    chk("确定性：同输入同输出", transition("OPEN", "TRIAGE") == "TRIAGED")
    chk("VERIFY_FAIL 闭环回 FIXING", transition("VERIFYING", "VERIFY_FAIL") == "FIXING")
    chk("REOPEN 回 FIXING", transition("CLOSED", "REOPEN") == "FIXING")

    for v in seed_lessons():
        sim = dict(v)
        final = simulate(sim, CANONICAL_CLOSE)
        chk(f"{v['id']} 经标准路径可达 CLOSED", final == "CLOSED")
        chk(f"{v['id']} history 记录 4 步", len(sim["history"]) == 4)

    # 异常路径：在错误状态发错误事件应抛 ValueError
    try:
        transition("OPEN", "FIX_SHIPPED")
        chk("OPEN+FIX_SHIPPED 抛错", False)
    except ValueError:
        chk("OPEN+FIX_SHIPPED 抛错", True)

    chk("报告可渲染且含状态机表", "VERIFY_FAIL" in render_markdown())
    print(f"A3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 A3 VFDR 状态机（漏洞反馈驱动修复）")
    ap.add_argument("--out", default=DEFAULT_REPORT, help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    md = render_markdown()
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
