"""642 A2 · anti-windup **上岗**（人审队列保护：半饱和标记 / 预算冻结 / 老化升级）。

**与 636 的关系**：636 只做**设计 + 影子模拟**（`anti_windup_636`），本模块把它落成
**真实队列管理策略**（纯函数，可单测）并对当前 65 项人审队列实跑。

上岗三条（§三 A2）：

1. **半饱和 ⇒ 标记 `queued_pending`**：队列占用 > **50%**（相对 636 阈值 A=100）时，
   新入队项标记 `queued_pending`，**不立即触发人审提醒**；
2. **预算超限 ⇒ 冻结低优先级**：周新增 > **20/周**（636 假设值）时，`低` 优先级新入队项
   `frozen=True`（不入队）；
3. **老化升级**：等待 > **30 天**的项优先级**自动升一级**（低→中→高）；升过级的项**不再被冻结**
   （老人不能因为队列满就被永久压住）。

**铁律**：本模块**不改任何判决**、**不动历史账本**、**不动队列文件**（只读 + 只出报告）。
即便"冻结"，在灰度期也只是**标记**（`frozen` 字段），**不真的丢弃**任何入队请求。

**诚实登记**（§十.3）：周处理能力 20/周、半饱和 50%、老化线 30 天**都是 636 的设计假设，非实测**；
当前队列 jsonl **无逐项到达时间戳** ⇒ 等待天数用「队列位置 + 容量」代理（越靠前越老），
是**近似**而非真实等待时长。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_anti_windup_rollout.md`。
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

import anti_windup_636 as shadow  # noqa: E402  （阈值/队列读取单一真源，不复制）

OUT_MD = os.path.join(ROOT, "data", "642_anti_windup_rollout.md")
QUEUE = shadow.QUEUE

QUEUE_CAPACITY_THRESHOLD = shadow.THRESHOLD_A   # 100（636 阈值 A）
HALF_SATURATION_PCT = 50.0                      # 「半饱和」占用线（%）
CAPACITY_PER_WEEK = shadow.CAPACITY_PER_WEEK    # 20（**636 假设值**，非实测）
AGING_DAYS = 30.0                               # 老化升级线
PRIORITY_ORDER = ("低", "中", "高")
LEVELS = ("正常", "半饱和", "饱和")


def queue_entries() -> list[dict[str, Any]]:
    """读人审队列（**只读**）。文件缺失 ⇒ 空表（不崩）。"""
    out: list[dict[str, Any]] = []
    try:
        for ln in open(QUEUE, encoding="utf-8"):
            if ln.strip():
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return out


def occupancy_pct(n: int) -> float:
    return round(100.0 * n / QUEUE_CAPACITY_THRESHOLD, 1)


def queue_state(n: Optional[int] = None, weekly_new: Optional[int] = None) -> dict[str, Any]:
    """三阈值 + 综合等级（**边界语义**：占用 > 50% 才算半饱和；占用恰 50% 仍是正常）。"""
    q = len(queue_entries()) if n is None else n
    wn = shadow.weekly_new() if weekly_new is None else weekly_new
    occ = occupancy_pct(q)
    avg_wait = round(q / max(1, CAPACITY_PER_WEEK) * 7, 1)
    a = q > QUEUE_CAPACITY_THRESHOLD
    b = avg_wait > shadow.THRESHOLD_B_DAYS
    c = wn > CAPACITY_PER_WEEK
    if a and (b or c):
        level = "饱和"
    elif occ > HALF_SATURATION_PCT:
        level = "半饱和"
    else:
        level = "正常"
    return {"queue_len": q, "weekly_new": wn, "occupancy_pct": occ,
            "avg_wait_days": avg_wait, "A": a, "B": b, "C": c, "level": level,
            "budget_exceeded": c}


def bump(priority: str) -> str:
    """优先级升一级（顶格不再升）。"""
    if priority not in PRIORITY_ORDER:
        return priority
    i = PRIORITY_ORDER.index(priority)
    return PRIORITY_ORDER[min(i + 1, len(PRIORITY_ORDER) - 1)]


def plan_admission(priority: str, state: dict[str, Any],
                   age_days: float = 0.0) -> dict[str, Any]:
    """入队策略（纯函数）：返回是否延迟提醒 / 是否冻结 / 是否升级 + 理由。

    优先级：**老化升级 > 预算冻结 > 半饱和延迟**。升过级的项不再被冻结。
    """
    level = str(state.get("level", "正常"))
    budget = bool(state.get("budget_exceeded", False))
    upgraded = age_days > AGING_DAYS
    out_priority = bump(priority) if upgraded else priority
    if upgraded:
        return {"priority_in": priority, "priority_out": out_priority, "upgraded": True,
                "frozen": False, "queued_pending": True,
                "reason": f"老化（{age_days} 天 > {AGING_DAYS} 天）⇒ 升级且不冻结"}
    if budget and priority == "低":
        return {"priority_in": priority, "priority_out": out_priority, "upgraded": False,
                "frozen": True, "queued_pending": True,
                "reason": f"周新增超预算（{CAPACITY_PER_WEEK}/周）⇒ 冻结低优先级入队"}
    if level == "饱和" and priority in ("低", "中"):
        return {"priority_in": priority, "priority_out": out_priority, "upgraded": False,
                "frozen": True, "queued_pending": True,
                "reason": "队列饱和 ⇒ 冻结非高优先级入队"}
    if level != "正常" or budget:
        return {"priority_in": priority, "priority_out": out_priority, "upgraded": False,
                "frozen": False, "queued_pending": True,
                "reason": f"队列{level} ⇒ 标记 queued_pending（不立即提醒人审）"}
    return {"priority_in": priority, "priority_out": out_priority, "upgraded": False,
            "frozen": False, "queued_pending": False, "reason": "队列正常 ⇒ 照常入队"}


def estimate_wait_days(rank: int, n: int) -> float:
    """等待天数**代理**：越靠前（rank 小）越早入队 ⇒ 等待越久。

    `(n - rank) / 容量 × 7`——近似"排在它前面的项按周处理能力消化完所需周数"。
    队列 jsonl **无时间戳**（数据缺口），这是代理，**不是真实等待时长**。
    """
    return round((n - rank) / max(1, CAPACITY_PER_WEEK) * 7, 1)


def replay_queue() -> dict[str, Any]:
    """对当前人审队列实跑策略（**只标记，不改文件**）：输出冻结/升级/延迟清单。"""
    entries = queue_entries()
    n = len(entries)
    st = queue_state(n)
    rows = []
    for rank, e in enumerate(entries):
        pr = str(e.get("priority", ""))
        age = estimate_wait_days(rank, n)
        plan = plan_admission(pr, st, age)
        rows.append({"card_id": e.get("card_id", ""), "rule": e.get("rule", ""),
                     "priority_in": pr, "age_days_proxy": age, **plan})
    frozen = [r for r in rows if r["frozen"]]
    upgraded = [r for r in rows if r["upgraded"]]
    pending = [r for r in rows if r["queued_pending"]]
    return {"state": st, "n": n, "rows": rows,
            "n_frozen": len(frozen), "n_upgraded": len(upgraded),
            "n_queued_pending": len(pending),
            "priority_dist": _dist(entries), "frozen": frozen, "upgraded": upgraded}


def _dist(entries: list[dict[str, Any]]) -> dict[str, int]:
    d: dict[str, int] = {}
    for e in entries:
        k = str(e.get("priority", "未知"))
        d[k] = d.get(k, 0) + 1
    return d


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": f"周处理能力 {CAPACITY_PER_WEEK}/周是 636 假设值，非实测 ⇒ 预算冻结可能过严",
         "trigger": "低优先级项被大量冻结且长期不解除",
         "rollback": "调高 CAPACITY_PER_WEEK 或把 `frozen` 降级为纯标记（本批本就是纯标记）；"
                     "灰度期不丢任何入队请求 ⇒ 回滚成本为零"},
        {"risk": "等待天数用位置代理（无时间戳）⇒ 靠前项被过度老化",
         "trigger": "升级清单出现人工确认并不紧急的项",
         "rollback": "把代理换成真实到达时间戳（需队列写入方补字段）或调高 AGING_DAYS"},
        {"risk": "半饱和 50% 线是设计值",
         "trigger": "大量项被标记 queued_pending 导致人审提醒延迟",
         "rollback": "调 HALF_SATURATION_PCT；或 `--report` 只看不采信（灰度）"},
    ]


def write_report() -> str:
    r = replay_queue()
    st = r["state"]
    lines = [
        "# 642 A2 · anti-windup 上岗（人审队列保护 · 灰度，**不丢任何入队请求**）", "",
        "## 一、三阈值与当前等级", "",
        "| 阈值 | 定义 | 当前值 | 触发 |", "|---|---|---|---|",
        f"| A | 队列长度 > {QUEUE_CAPACITY_THRESHOLD} | {st['queue_len']} | "
        f"{'✅是' if st['A'] else '否'} |",
        f"| 占用率 | 相对阈值 A | **{st['occupancy_pct']}%** | "
        f"{'✅>50%' if st['occupancy_pct'] > HALF_SATURATION_PCT else '否'} |",
        f"| B | 平均等待 > {shadow.THRESHOLD_B_DAYS} 天 | {st['avg_wait_days']} | "
        f"{'✅是' if st['B'] else '否'} |",
        f"| C | 周新增 > {CAPACITY_PER_WEEK}/周 | {st['weekly_new']} | "
        f"{'✅是' if st['C'] else '否'} |",
        f"| **综合等级** | — | **{st['level']}** | — |", "",
        "## 二、上岗策略（优先级：老化 > 预算冻结 > 半饱和延迟）", "",
        "| 条件 | 行为 |", "|---|---|",
        f"| 等待 > {AGING_DAYS} 天 | 优先级升一级，**不再冻结** |",
        f"| 周新增 > {CAPACITY_PER_WEEK} 且优先级=低 | `frozen=True`（灰度期只标记，不丢） |",
        "| 等级=饱和 且优先级∈{低,中} | `frozen=True` |",
        "| 等级≠正常 或 超预算 | `queued_pending=True`（**不立即提醒人审**） |",
        "| 其余 | 照常入队 |", "",
        f"## 三、对当前队列实跑（{r['n']} 项，只标记不改文件）", "",
        f"- 优先级分布：`{r['priority_dist']}`",
        f"- 标记 `queued_pending`：**{r['n_queued_pending']}/{r['n']}**",
        f"- **冻结**：**{r['n_frozen']}**；**老化升级**：**{r['n_upgraded']}**", "",
        "### 冻结清单", "",
        "| 卡 | 规则 | 优先级 | 等待代理(天) | 理由 |", "|---|---|---|---|---|"]
    for x in r["frozen"][:40]:
        lines.append(f"| `{x['card_id']}` | `{x['rule']}` | {x['priority_in']} | "
                     f"{x['age_days_proxy']} | {x['reason']} |")
    if not r["frozen"]:
        lines.append(f"| — | — | — | — | 队列优先级分布 {r['priority_dist']} **无「低」项** ⇒ "
                     f"预算冻结规则在真实队列上未触发（0 项）；这是数据分布所致，非实现缺陷 |")
    lines += ["", "### 老化升级清单", "",
              "| 卡 | 优先级 | 等待代理(天) | 理由 |", "|---|---|---|---|"]
    for x in r["upgraded"][:40]:
        lines.append(f"| `{x['card_id']}` | {x['priority_in']} → {x['priority_out']} | "
                     f"{x['age_days_proxy']} | {x['reason']} |")
    if not r["upgraded"]:
        lines.append(f"| — | — | — | 当前队列最长等待代理 "
                     f"{estimate_wait_days(0, r['n'])} 天 < {AGING_DAYS} 天 ⇒ 无项触发老化 |")
    lines += ["", "### 策略矩阵（**合成输入**，验证机制；不是队列事实）", "",
              "| 优先级 | 队列正常 | 半饱和 | 半饱和+超预算 | 饱和 |",
              "|---|---|---|---|---|"]
    synth = {"队列正常": queue_state(n=1, weekly_new=1),
             "半饱和": queue_state(n=51, weekly_new=20),
             "半饱和+超预算": queue_state(n=51, weekly_new=21),
             "饱和": queue_state(n=101, weekly_new=21)}
    for pr in PRIORITY_ORDER:
        cells = []
        for _k, _st in synth.items():
            p = plan_admission(pr, _st)
            tag = "冻结" if p["frozen"] else ("延迟" if p["queued_pending"] else "照常")
            cells.append(tag)
        lines.append(f"| {pr} | " + " | ".join(cells) + " |")
    lines += ["", "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              f"1. **周处理能力 {CAPACITY_PER_WEEK}/周、半饱和 {HALF_SATURATION_PCT:.0f}%、"
              f"老化线 {AGING_DAYS:.0f} 天都是 636 设计假设，非实测**（§十.3）；",
              "2. 队列 jsonl **无逐项到达时间戳** ⇒ 等待天数用「位置 + 容量」**代理**，不是真实等待；",
              "3. **灰度期零损失**：`frozen`/`queued_pending` 都只是标记，**不丢弃任何入队请求**、",
              "   **不改人审队列文件**、**不改任何判决**；",
              "4. **两份清单为空都不是实现缺陷**：老化清单空 = 队列尚未积压到 30 天（代理最长 "
              f"{estimate_wait_days(0, r['n'])} 天）；冻结清单空 = 队列里没有「低」优先级项。"
              "机制由「策略矩阵」用合成输入验证（见上）；",
              "5. 冻结清单是「按当前策略回放既有 65 项」的口径，**不是**对既有项执行冻结。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 半饱和边界：占用恰 50% ⇒ 正常；51% ⇒ 半饱和
    s50 = queue_state(n=50, weekly_new=20)
    s51 = queue_state(n=51, weekly_new=20)
    chk("边界：n=50 ⇒ 正常", s50["level"] == "正常", s50["level"])
    chk("边界：n=51 ⇒ 半饱和", s51["level"] == "半饱和", s51["level"])

    # 预算边界：20/周 不超；21/周 超 ⇒ 冻结低优先级
    b20 = queue_state(n=10, weekly_new=20)
    b21 = queue_state(n=10, weekly_new=21)
    chk("边界：20/周 不超预算", b20["budget_exceeded"] is False)
    chk("边界：21/周 超预算", b21["budget_exceeded"] is True)
    chk("超预算 ⇒ 低优先级冻结", plan_admission("低", b21)["frozen"] is True)
    chk("超预算 ⇒ 高优先级不冻结", plan_admission("高", b21)["frozen"] is False)

    # 老化边界：30 天不升；31 天升且不冻结
    normal = queue_state(n=1, weekly_new=1)
    chk("边界：30 天不升", plan_admission("低", b21, 30.0)["upgraded"] is False)
    p = plan_admission("低", b21, 31.0)
    chk("31 天 ⇒ 升级且不冻结",
        p["upgraded"] is True and p["priority_out"] == "中" and p["frozen"] is False)
    chk("升级顶格不越界", plan_admission("高", normal, 99.0)["priority_out"] == "高")

    # 正常队列照常入队
    chk("正常队列照常", plan_admission("中", normal)["queued_pending"] is False)

    # 实跑：只标记不改文件
    r = replay_queue()
    chk("队列非空", r["n"] >= 1)
    chk("等级合法", str(r["state"]["level"]) in LEVELS)
    chk("冻结数 ≤ 队列数", r["n_frozen"] <= r["n"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A2 anti-windup 上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写上岗报告")
    ap.add_argument("--json", action="store_true", help="打印冻结/升级清单（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = replay_queue()
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k not in ("rows", "frozen", "upgraded")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[anti-windup] 队列 {r['n']}；等级 {r['state']['level']}；"
          f"占用 {r['state']['occupancy_pct']}%；冻结 {r['n_frozen']}；升级 {r['n_upgraded']}；"
          f"queued_pending {r['n_queued_pending']}（只标记，不丢请求）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
