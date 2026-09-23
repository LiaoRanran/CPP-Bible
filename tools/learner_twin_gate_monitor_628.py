"""628 D1 · 学习者镜像（Learner Twin）门状态监控

v18 调研的开门阈值：**50 条真实学习事件**。本工具只统计与展示门状态，
**不开门、不建设镜像**（门未开，建设无据）。

门状态定义：
- `closed`  （0 – 39）：远未达标
- `opening` （40 – 49）：接近阈值（阈值的 80% 起）
- `open`    （≥ 50）：达标，可启动镜像建设

`--check`：用合成计数验证三态判定 + 真实计数一致性。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EVENTS = os.path.join(ROOT, "data", "learner_behavior_events.jsonl")
REPORT = os.path.join(ROOT, "data", "learner_twin_gate_report_628.md")

THRESHOLD = 50          # 开门阈值（v18 调研）
NEAR_RATIO = 0.8        # 接近阈值的起点比例


def load_events() -> list[dict]:
    if not os.path.exists(EVENTS):
        return []
    return [json.loads(ln) for ln in open(EVENTS, encoding="utf-8") if ln.strip()]


def real_events(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("agent_assisted") is False]


def unclassified(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("agent_assisted") is None]


def gate_state(count: int, threshold: int = THRESHOLD,
               near_ratio: float = NEAR_RATIO) -> str:
    if count >= threshold:
        return "open"
    if count >= int(threshold * near_ratio):
        return "opening"
    return "closed"


def build(threshold: int = THRESHOLD) -> dict:
    events = load_events()
    real = real_events(events)
    by_kind: dict[str, int] = {}
    for e in events:
        by_kind[str(e["kind"])] = by_kind.get(str(e["kind"]), 0) + 1
    n = len(real)
    return {
        "stamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "threshold": threshold,
        "near_line": int(threshold * NEAR_RATIO),
        "real_learning_events": n,
        "candidates_total": len(events),
        "unclassified": len(unclassified(events)),
        "by_kind": by_kind,
        "state": gate_state(n, threshold),
        "progress": round(n / max(threshold, 1), 4),
    }


def write_report(d: Optional[dict] = None) -> str:
    d = d or build()
    import learner_behavior_collector_628 as C  # 只复用常量与正则，不重跑采集
    sessions = C.probe_session_stores()
    lines = [
        "# 628 D1 · 学习者镜像门状态报告", "",
        f"- 生成时刻：{d['stamp']}",
        f"- **门状态：`{d['state']}`**（真实学习事件 {d['real_learning_events']} / "
        f"阈值 {d['threshold']}，进度 {d['progress'] * 100:.1f}%）",
        f"- 近阈值线（{d['threshold']}×0.8）：{d['near_line']} 条",
        "",
        "## 一、当前真实学习事件数量", "",
        f"- **真实学习事件：{d['real_learning_events']} 条**",
        f"- 候选事件合计：{d['candidates_total']} 条",
        f"- 其中不可判定归属：{d['unclassified']} 条（既无流水线标识、也无人类学习正向信号，"
        f"**保守不计入**门）",
        f"- 分来源：`{json.dumps(d['by_kind'], ensure_ascii=False)}`",
        "",
        "## 二、采集来源", "",
        "| # | 来源 | 说明 |",
        "|---|---|---|",
        "| 1 | `git log --name-only -- Book atoms evidence Examples` | "
        f"涉及学习内容的提交 {d['by_kind'].get('git_commit', 0)} 条 |",
        "| 2 | `_auto/inbox/` + `_auto/outbox/` | 批次记录 "
        f"{d['by_kind'].get('batch_record', 0)} 条 |",
        "| 3 | `Book/ atoms/ evidence/` 文件 mtime | "
        f"{d['by_kind'].get('file_mtime', 0)} 条 |",
        "| 4 | 会话日志存储位置探测 | " + (
            "；".join(f"`{s['path']}`（{s['files']} 文件）" for s in sessions)
            if sessions else "未发现候选路径") + " |",
        "",
        "探测到的 IDE 会话存储**只用于定位**，其对话内容不构成\"用户修改学习内容\"的证据，"
        "因此**不计入门事件**。",
        "",
        "## 三、\"学习事件\"定义（可复现判定）", "",
        "事件必须满足「**用户主动修改了学习内容**（`Book/`/`atoms/`/`evidence/`），"
        "或运行学习相关工具」且**不属于 AI 批次/工具流水线产物**。",
        "",
        "三态判定（`learner_behavior_collector_628.classify`）：",
        "",
        "| 判定 | 规则 | 是否计入门 |",
        "|---|---|---|",
        "| `agent_assisted=True` | 命中流水线标识正则 `AGENT_PAT`（批次号 / 任务号 / "
        "`feat(...)` 等约定式前缀 / 监工·质检·原子化 等流程词） | ❌ 否 |",
        "| `agent_assisted=False` | 命中人类学习正向信号 `HUMAN_PAT`"
        "（学习笔记 / 读书笔记 / 错题本 / study-log …） | ✅ **是** |",
        "| `agent_assisted=None` | 两者都不命中 → 归属不可判定 | ❌ 否（保守） |",
        "",
        "**为什么这样定**：仓库内涉及学习内容的提交全部来自 AI 协作流水线"
        "（提交信息带批次/任务/流程标识），没有任何一条带人类亲手学习的正向信号。"
        "宁可少算（把不可判定的排除在外），也不把 agent 产物伪装成学习行为。",
        "",
        "## 四、开门建议", "",
        f"1. 当前 `{d['state']}`，距阈值还差 **{max(d['threshold'] - d['real_learning_events'], 0)} 条**"
        f"真实学习事件。",
        "2. 需要**用户主动**做 50 次学习相关操作（例如：本人编辑 `Book/` 章节笔记、"
        "亲手完成并提交习题/错题、以「学习笔记」类提交信息记录学习过程）才能开门。",
        "3. 采集器已就绪：用户每次真实学习行为会被 `learner_behavior_collector_628.py`"
        "采集进 `data/learner_behavior_events.jsonl`（append-only），"
        "`learner_twin_gate_monitor_628.py` 自动更新门状态。",
        "4. **不建议**为了开门而制造事件（例如让 agent 代写带「学习笔记」字样的提交）——"
        "那会污染镜像的语义前提，使镜像建立在假数据上。",
        "",
        "## 五、局限", "",
        "- 本批**只做采集器与门监控**，不做镜像、不做学习行为建模（门未开，无据可建）。",
        "- 判定规则是**启发式**：`AGENT_PAT`/`HUMAN_PAT` 是关键词正则，可能有误判；"
        "如果将来出现边界样本，应在报告中登记而不是悄悄调正则。",
        "- 会话日志只探测位置与文件数，未解析内容（涉及隐私，且不作为学习证据）。",
    ]
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return REPORT


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("阈值 50 → open", gate_state(50) == "open")
    chk("阈值 49 → opening", gate_state(49) == "opening")
    chk("阈值 40 → opening（80% 线）", gate_state(40) == "opening")
    chk("阈值 39 → closed", gate_state(39) == "closed")
    chk("阈值 0 → closed", gate_state(0) == "closed")
    chk("阈值可配置（100 时 60 → closed）", gate_state(60, threshold=100) == "closed")
    chk("阈值可配置（100 时 100 → open）", gate_state(100, threshold=100) == "open")
    d = build()
    chk("真实计数与事件文件一致",
        d["real_learning_events"] == len(real_events(load_events())),
        f'({d["real_learning_events"]})')
    chk("状态与计数一致", d["state"] == gate_state(d["real_learning_events"], d["threshold"]),
        f'({d["state"]})')
    chk("候选数 ≥ 真实数", d["candidates_total"] >= d["real_learning_events"])
    p = write_report(d)
    chk("报告已写入", os.path.exists(p) and os.path.getsize(p) > 500)
    print(f"D1 gate monitor check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 D1 学习者镜像门监控")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--threshold", type=int, default=THRESHOLD)
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    d = build(args.threshold)
    if args.report:
        print(f"written {write_report(d)}")
    print(f"state={d['state']} real={d['real_learning_events']}/{d['threshold']} "
          f"progress={d['progress'] * 100:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
