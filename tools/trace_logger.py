#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trace_logger.py — 结构化操作日志（498 任务 4 / P1-12 / 497 可观测性与失败恢复）。

为什么（497）：Agent 的每次操作（写夹具/编译/replay/门禁/红队/人审/提交/改工具）此前
**没有统一留痕**——出了问题只能靠翻会话记录。结构化 trace 是后续诊断引擎（P2-2，自动定位
门禁失败根因）与健康看板（P2-6）的**唯一数据源**；没有它，那两个 P2 项无从落地。

存储与格式
==========
* 目录 `data/traces/`（自动创建；已在 .gitignore —— 运行时数据不入库）；
* 文件按日期 `trace-YYYY-MM-DD.jsonl`，**每行一个 JSON 事件**（append-only，可 grep）。

事件字段：`timestamp`（ISO8601 本地）/ `seq`（当日递增）/ `pid` / `actor` / `action` /
`target` / `result` / `details`（对象，可选）。

用法
====
    python tools/trace_logger.py log --actor writer --action compile --target fx.cpp --result pass
    python tools/trace_logger.py log --actor coolie --action gate_check --target repo --result fail \\
        --details '{"rule": "EV-X", "count": 2}'
    python tools/trace_logger.py read [--date YYYY-MM-DD] [--action gate_check] [--fail-only]

可 import API：`log_event(actor, action, target, result, details=None)` → 事件 dict。

纪律：枚举外取值**报错不静默**（枚举是数据源可查询性的前提）；`--details` 必须是合法
JSON **对象**（解析失败 exit 2，不静默丢弃）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
TRACES = ROOT / "data" / "traces"

ACTORS = ("writer", "redteam", "gatekeeper", "human", "coolie", "architect")
ACTIONS = ("fixture_create", "compile", "replay", "gate_check", "poison_drill",
           "redteam_review", "human_sign", "commit", "tool_modify", "other")
RESULTS = ("pass", "fail", "warn", "skip", "info")


def trace_file(date: str | None = None, base: Path | None = None) -> Path:
    d = base or TRACES
    d.mkdir(parents=True, exist_ok=True)
    day = date or time.strftime("%Y-%m-%d")
    return d / f"trace-{day}.jsonl"


def _last_seq(path: Path) -> int:
    """当日最后一条事件的 seq（无文件/空文件 → 0）。逐行解析，损坏行跳过。"""
    if not path.is_file():
        return 0
    last = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            last = max(last, int(json.loads(line).get("seq") or 0))
        except (ValueError, AttributeError):
            continue
    return last


def _validate(actor: str, action: str, result: str) -> None:
    for name, val, allowed in (("actor", actor, ACTORS), ("action", action, ACTIONS),
                               ("result", result, RESULTS)):
        if val not in allowed:
            raise ValueError(f"{name}={val!r} 不在枚举内（可选：{'/'.join(allowed)}）")


def log_event(actor: str, action: str, target: str, result: str,
              details: dict | None = None, *, date: str | None = None,
              base: Path | None = None) -> dict:
    """追加一条事件并返回它（枚举与 details 类型校验失败 → ValueError，不静默写坏数据）。"""
    _validate(actor, action, result)
    if details is not None and not isinstance(details, dict):
        raise ValueError("details 必须是 JSON 对象（dict）")
    path = trace_file(date, base)
    event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seq": _last_seq(path) + 1,
        "pid": os.getpid(),
        "actor": actor, "action": action, "target": target, "result": result,
    }
    if details:
        event["details"] = details
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_events(*, date: str | None = None, action: str | None = None,
                fail_only: bool = False, base: Path | None = None) -> list[dict]:
    """读当日（或指定日期）事件并按 action / result=fail 过滤。"""
    path = trace_file(date, base)
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if action and ev.get("action") != action:
            continue
        if fail_only and ev.get("result") != "fail":
            continue
        out.append(ev)
    return out


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="结构化操作日志（498 任务 4）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="追加一条事件")
    lg.add_argument("--actor", required=True, choices=ACTORS)
    lg.add_argument("--action", required=True, choices=ACTIONS)
    lg.add_argument("--target", required=True)
    lg.add_argument("--result", required=True, choices=RESULTS)
    lg.add_argument("--details", default=None, help="JSON 对象字符串")

    rd = sub.add_parser("read", help="读事件（JSONL 输出）")
    rd.add_argument("--date", default=None)
    rd.add_argument("--action", default=None, choices=ACTIONS)
    rd.add_argument("--fail-only", action="store_true")

    a = ap.parse_args(argv)
    if a.cmd == "log":
        det = None
        if a.details:
            try:
                det = json.loads(a.details)
            except ValueError as exc:
                print(f"[trace_logger] --details 不是合法 JSON：{exc}", file=sys.stderr)
                return 2
            if not isinstance(det, dict):
                print("[trace_logger] --details 必须是 JSON 对象（{...}）", file=sys.stderr)
                return 2
        try:
            ev = log_event(a.actor, a.action, a.target, a.result, det)
        except ValueError as exc:
            print(f"[trace_logger] {exc}", file=sys.stderr)
            return 2
        print(json.dumps(ev, ensure_ascii=False))
        return 0
    for ev in read_events(date=a.date, action=a.action, fail_only=a.fail_only):
        print(json.dumps(ev, ensure_ascii=False))
    return 0

if "--check" in sys.argv:
    print("OK: trace_logger --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
