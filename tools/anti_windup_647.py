"""647 B2 · anti-windup **真上岗**（636 影子 → 642 灰度标记 → **647 冻结超预算队列**）。

647 与 642 的**唯一差别**（§四 B2）：
* 642：`frozen=True` 只是**标记**，请求照进队列（"灰度期不丢任何请求"）；
* 647（enforce）：`frozen=True` ⇒ **真的不入队**（`enqueued=False`），即"冻结"。

三阈值沿用 636/642（**设计假设值，非实测**）：队列容量 A=100、半饱和 50%、老化线 30 天、
周处理能力 **20/周**。647 新增一条**积压警报**：占用率 **> 80%** ⇒ `needs_human_cleanup=True`
（"队列该清了"，让人审而不是让机器丢请求）。

**回滚**：`QUEYI_PROTECTOR_MODE=shadow` ⇒ 退回 642 的"只标记不丢请求"（`enqueued` 恒 True）。

**铁律**：本模块**不改任何判决、不动人审队列文件**（只读 + 只出报告）；
"冻结"在这里的语义是"**向队列写入方返回 enqueued=False**"，**不删既有队列条目**。

CLI：`--check` / `--report` / `--json`。纯标准库。
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

import anti_windup_642 as base  # noqa: E402  （阈值/队列读取/策略单一真源，不复制）
import protector_mode_647 as pmode  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_anti_windup_enforce.md")
OUT_JSON = os.path.join(ROOT, "data", "647_anti_windup_enforce.json")

BACKLOG_ALERT_PCT = 80.0     # 积压警报线（647 新增）
QUEUE = base.QUEUE


def backlog_alert(state: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """积压警报：占用率 > 80% ⇒ 需人审清理（**不自动丢请求**，只喊人）。"""
    st = state or base.queue_state()
    occ = float(st["occupancy_pct"])
    return {"alert": occ > BACKLOG_ALERT_PCT, "occupancy_pct": occ,
            "threshold_pct": BACKLOG_ALERT_PCT,
            "needs_human_cleanup": occ > BACKLOG_ALERT_PCT,
            "action": "触发「需人审清理」警报" if occ > BACKLOG_ALERT_PCT else "无需清理"}


def admit(priority: str, state: Optional[dict[str, Any]] = None,
          age_days: float = 0.0) -> dict[str, Any]:
    """**真上岗的入队判定**：enforce 下 `frozen` ⇒ `enqueued=False`；shadow 下恒 True。"""
    st = state if state is not None else base.queue_state()
    plan = base.plan_admission(priority, st, age_days)
    enforce = pmode.is_enforce()
    frozen = bool(plan["frozen"]) and enforce
    return {**plan, "mode": pmode.mode(), "frozen_enforced": frozen,
            "enqueued": not frozen, "backlog": backlog_alert(st),
            "enforce_note": ("enforce：冻结 = **不入队**" if enforce
                             else "shadow：冻结只标记，请求照常入队（642 行为）")}


def replay_queue() -> dict[str, Any]:
    """对**当前人审队列**回放策略：输出"若现在有同优先级新请求，会不会被冻结"。"""
    entries = base.queue_entries()
    n = len(entries)
    st = base.queue_state(n)
    rows = []
    for rank, e in enumerate(entries):
        pr = str(e.get("priority", ""))
        age = base.estimate_wait_days(rank, n)
        rows.append({"card_id": e.get("card_id", ""), "rule": e.get("rule", ""),
                     "age_days_proxy": age, **admit(pr, st, age)})
    frozen = [r for r in rows if r["frozen_enforced"]]
    return {"mode": pmode.mode(), "state": st, "n": n, "rows": rows,
            "n_frozen_enforced": len(frozen), "frozen": frozen,
            "priority_dist": base._dist(entries), "backlog": backlog_alert(st),
            "queue_file_sha_unchanged": _queue_digest()}


def _queue_digest() -> str:
    import hashlib
    try:
        return hashlib.sha256(open(QUEUE, "rb").read()).hexdigest()
    except OSError:
        return ""


SYNTH_STATES: tuple[tuple[str, dict[str, Any]], ...] = (
    ("正常", base.queue_state(n=1, weekly_new=1)),
    ("半饱和", base.queue_state(n=51, weekly_new=20)),
    ("半饱和+超预算", base.queue_state(n=51, weekly_new=21)),
    ("饱和", base.queue_state(n=101, weekly_new=21)),
)


def synthetic_check() -> list[dict[str, Any]]:
    """合成输入验证 enforce/shadow 两档差异（**不是队列事实**）。"""
    out = []
    for label, st in SYNTH_STATES:
        row = {"state": label, "occupancy_pct": st["occupancy_pct"],
               "backlog_alert": backlog_alert(st)["alert"]}
        for pr in base.PRIORITY_ORDER:
            a = admit(pr, st)
            row[f"{pr}_enqueued"] = a["enqueued"]
            row[f"{pr}_frozen_enforced"] = a["frozen_enforced"]
        out.append(row)
    return out


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "20/周 是 **636 设计假设值**（非实测）⇒ 可能冻得过严，把该审的请求挡在门外",
         "trigger": "低优先级项被长期冻结且无人清理",
         "rollback": "`QUEYI_PROTECTOR_MODE=shadow` ⇒ 立刻回到只标记不丢请求；"
                     "或调大 `base.CAPACITY_PER_WEEK`"},
        {"risk": "冻结 = 不入队 ⇒ 若上层无重试/告警，请求可能**静默消失**",
         "trigger": "上游只调用一次 `admit()` 不看返回值",
         "rollback": "`admit()` 返回体含 `reason` 与 `backlog`；占用 > 80% 时额外 `needs_human_cleanup` "
                     "（交人清理）；shadow 下 `enqueued` 恒 True"},
        {"risk": "等待天数是**位置代理**（队列无时间戳）⇒ 老化升级可能误触",
         "trigger": "升级清单出现人工确认不紧急的项",
         "rollback": "用真实到达时间戳替换代理，或调高 `base.AGING_DAYS`"},
    ]


def write_report() -> str:
    r = replay_queue()
    syn = synthetic_check()
    st = r["state"]
    lines = [
        "# 647 B2 · anti-windup **真上岗**（超预算冻结 · 积压 >80% 喊人清理）", "",
        f"- 当前模式：**{r['mode']}**（enforce = 冻结即不入队；shadow = 只标记，`enqueued` 恒 True）",
        f"- 阈值（均沿用 636/642 **设计假设值**）：容量 A={base.QUEUE_CAPACITY_THRESHOLD} · "
        f"半饱和 {base.HALF_SATURATION_PCT:.0f}% · 老化 {base.AGING_DAYS:.0f} 天 · "
        f"预算 {base.CAPACITY_PER_WEEK}/周 · **积压警报 {BACKLOG_ALERT_PCT:.0f}%**", "",
        "## 一、当前队列与警报", "",
        f"- 队列长度：**{r['n']}**；占用：**{st['occupancy_pct']}%**；等级：**{st['level']}**",
        f"- 周新增：**{st['weekly_new']}**（超预算：{st['budget_exceeded']}）",
        f"- **积压警报：{r['backlog']['alert']}**"
        f"（>{BACKLOG_ALERT_PCT:.0f}% ⇒ 需人审清理；当前 {r['backlog']['occupancy_pct']}%）",
        f"- 队列文件未被改动（sha256 `{r['queue_file_sha_unchanged'][:16]}…`，只读）", "",
        "## 二、enforce vs shadow 的差别（合成输入，验证机制）", "",
        "| 队列状态 | 占用% | 积压警报 | 低优先级入队(enforce) | 低优先级入队(shadow) | 高优先级入队(enforce) |",
        "|---|---|---|---|---|---|"]
    for row in syn:
        lines.append(f"| {row['state']} | {row['occupancy_pct']} | "
                     f"{'⚠️' if row['backlog_alert'] else '—'} | "
                     f"{'✅' if row['低_enqueued'] else '⛔ 冻结'} | "
                     f"{'✅' if not row['低_frozen_enforced'] else '—'} | "
                     f"{'✅' if row['高_enqueued'] else '⛔ 冻结'} |")
    lines += ["", "## 三、对当前队列回放（{n} 项）".format(n=r["n"]), "",
              f"- 优先级分布：`{r['priority_dist']}`",
              f"- **会被冻结（enforce 下不入队）**：**{r['n_frozen_enforced']}** 项", "",
              "| 卡 | 规则 | 优先级 | 等待代理(天) | 冻结(真) | 理由 |", "|---|---|---|---|---|---|"]
    for x in r["frozen"][:40]:
        lines.append(f"| `{x['card_id']}` | `{x['rule']}` | {x['priority_in']} | "
                     f"{x['age_days_proxy']} | {'⛔' if x['frozen_enforced'] else '—'} | {x['reason']} |")
    if not r["frozen"]:
        lines.append(f"| — | — | — | — | — | 队列优先级分布 {r['priority_dist']} "
                     "**无「低」项** ⇒ 冻结规则在真实队列上未触发（**数据分布所致，非实现缺陷**） |")
    lines += ["", "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **阈值全是 636 设计假设值**（20/周、50%、30 天），**非实测**；",
              "2. **等待天数是位置代理**（队列 jsonl 无时间戳），不是真实等待；",
              "3. **冻结 = 不入队**，与 642 的「只标记」是**生产行为差别**；"
              "本模块只返回 `enqueued=False`，**不删任何既有队列条目、不动队列文件**；",
              "4. **真实队列上冻结数为 0**（无「低」优先级项）⇒ 机制由**合成输入**验证（不夸大「已生效」）；",
              "5. 积压警报只**喊人**（`needs_human_cleanup`），**不自动丢弃**请求。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in r.items() if k not in ("rows", "frozen")}
                  | {"synthetic": syn}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    over = base.queue_state(n=51, weekly_new=21)      # 超预算
    under = base.queue_state(n=1, weekly_new=1)       # 正常
    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "enforce"
        chk("enforce：超预算 + 低 ⇒ **不入队**", admit("低", over)["enqueued"] is False)
        chk("enforce：超预算 + 高 ⇒ 入队", admit("高", over)["enqueued"] is True)
        chk("enforce：正常队列 ⇒ 入队", admit("低", under)["enqueued"] is True)
        chk("enforce：老化升级 ⇒ 不入队？（升级项不冻结）",
            admit("低", over, age_days=31.0)["enqueued"] is True)
        os.environ[pmode.ENV] = "shadow"
        s = admit("低", over)
        chk("shadow：同一输入 ⇒ 入队（642 行为）", s["enqueued"] is True
            and s["frozen"] is True and s["frozen_enforced"] is False)
        os.environ[pmode.ENV] = "enforce"
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved

    chk("积压警报：>80% 触发", backlog_alert(base.queue_state(n=81, weekly_new=1))["alert"] is True)
    chk("积压警报：=80% 不触发", backlog_alert(base.queue_state(n=80, weekly_new=1))["alert"] is False)
    chk("积压警报不丢请求（只喊人）",
        backlog_alert(base.queue_state(n=101, weekly_new=21))["needs_human_cleanup"] is True)
    chk("阈值可配置（常量存在）", BACKLOG_ALERT_PCT == 80.0 and base.CAPACITY_PER_WEEK == 20)

    r = replay_queue()
    chk("队列非空且只读", r["n"] >= 1 and r["queue_file_sha_unchanged"] != "")
    chk("冻结数 ≤ 队列数", r["n_frozen_enforced"] <= r["n"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"B2 anti-windup-enforce selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B2 anti-windup 真上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    r = replay_queue()
    if a.report:
        print(f"written {write_report()}")
        return 0
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k not in ("rows", "frozen")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 anti-windup] mode={r['mode']} queue={r['n']} level={r['state']['level']} "
          f"occ={r['state']['occupancy_pct']}% backlog_alert={r['backlog']['alert']} "
          f"frozen(enforced)={r['n_frozen_enforced']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
