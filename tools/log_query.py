#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""log_query.py — 日志查询 CLI（508 任务4 / 可观测性 L1）。

读 `data/logs/*.jsonl`（见 `tools/observability.py`）并按维度过滤，彩色格式化输出。
**零第三方依赖**（纯标准库 ANSI；非 tty 或设了 NO_COLOR 时自动关闭颜色）。

用法
====
    python tools/log_query.py --trace-id batch-20260914-201530-a1b2   # 追一次批量执行全链路
    python tools/log_query.py --tool gate_engine --level ERROR        # 某工具的报错
    python tools/log_query.py --grep EV-MATRIX --since "2026-09-14 19:00"
    python tools/log_query.py --date 2026-09-13 --last 20
    python tools/log_query.py --json                                   # 原样 JSONL（供 jq/管道）

过滤器可任意组合（AND 语义）。默认查**今天**、按文件顺序（时间升序）输出。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:                                     # Windows 控制台 UTF-8（与 trace_logger 同用）
    from utf8_console import ensure_utf8
except Exception:                        # noqa: BLE001 —— 缺失时不影响查询
    def ensure_utf8() -> None:           # type: ignore[misc]
        return None

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "logs"

LEVEL_ORDER = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
_ANSI = {
    "DEBUG": "\033[2m", "INFO": "\033[36m", "WARN": "\033[33m", "ERROR": "\033[31m",
    "tool": "\033[35m", "trace": "\033[34m", "dim": "\033[2m", "reset": "\033[0m",
}


def use_color() -> bool:
    return (sys.stdout.isatty() and not os.environ.get("NO_COLOR")
            and os.environ.get("TERM", "") != "dumb")


def files_for(date: str | None, days: int | None) -> list[Path]:
    """选日志文件：`--date` 精确一天；`--days N` 最近 N 天；默认今天。"""
    if date:
        p = LOGS / f"{date}.jsonl"
        return [p] if p.is_file() else []
    if days and days > 1:
        import datetime
        out = []
        for i in range(days):
            d = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
            p = LOGS / f"{d}.jsonl"
            if p.is_file():
                out.append(p)
        return sorted(out)
    p = LOGS / f"{__import__('time').strftime('%Y-%m-%d')}.jsonl"
    return [p] if p.is_file() else []


def match(ev: dict, *, trace_id: str | None, tool: str | None, level: str | None,
          grep: str | None, since: str | None) -> bool:
    if trace_id and ev.get("trace_id") != trace_id:
        return False
    if tool and ev.get("tool") != tool:
        return False
    if level and LEVEL_ORDER.get(str(ev.get("level")).upper(), 0) < \
            LEVEL_ORDER.get(level.upper(), 0):
        return False
    if since and str(ev.get("timestamp", "")) < since:
        return False
    if grep:
        hay = json.dumps(ev, ensure_ascii=False)
        if grep not in hay:
            return False
    return True


def fmt(ev: dict, color: bool) -> str:
    lv = str(ev.get("level", "?"))
    ts = str(ev.get("timestamp", ""))[11:] or "?"
    tool = str(ev.get("tool", "?"))
    tid = str(ev.get("trace_id", ""))[-9:]
    surf = str(ev.get("surface", "operation"))[:4]
    dur = ev.get("duration_ms")
    dur_s = f" {dur:>7.1f}ms" if isinstance(dur, (int, float)) else " " * 10
    msg = str(ev.get("message", ""))
    det = ev.get("details")
    det_s = ""
    if det:
        try:
            det_s = "  " + json.dumps(det, ensure_ascii=False)[:120]
        except (TypeError, ValueError):
            det_s = ""
    if not color:
        return f"{ts} {lv:<5} {surf:<4} {tool:<16}{dur_s} [{tid}] {msg}{det_s}"
    c = _ANSI
    return (f"{c['dim']}{ts}{c['reset']} "
            f"{c.get(lv, '')}{lv:<5}{c['reset']} "
            f"{c['dim']}{surf:<4}{c['reset']} "
            f"{c['tool']}{tool:<16}{c['reset']}"
            f"{c['dim']}{dur_s}{c['reset']} "
            f"{c['trace']}[{tid}]{c['reset']} {msg}{c['dim']}{det_s}{c['reset']}")


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="日志查询（508 任务4）")
    ap.add_argument("--trace-id", default=None)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--level", default=None, choices=sorted(LEVEL_ORDER, key=LEVEL_ORDER.get))
    ap.add_argument("--grep", default=None)
    ap.add_argument("--since", default=None,
                    help='时间下界，格式 "YYYY-MM-DD HH:MM" 或 "YYYY-MM-DDTHH:MM:SS"')
    ap.add_argument("--date", default=None, help="只查某天（YYYY-MM-DD）")
    ap.add_argument("--days", type=int, default=None, help="查最近 N 天（含今天）")
    ap.add_argument("--last", type=int, default=None, help="只显示最后 N 条")
    ap.add_argument("--json", action="store_true", help="原样输出 JSONL")
    a = ap.parse_args(argv)

    since = a.since.replace(" ", "T") if a.since else None
    color = use_color() and not a.json
    rows: list[dict] = []
    for p in files_for(a.date, a.days):
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if isinstance(ev, dict) and match(ev, trace_id=a.trace_id, tool=a.tool,
                                              level=a.level, grep=a.grep, since=since):
                rows.append(ev)
    if a.last is not None:
        rows = rows[-a.last:]
    if a.json:
        for ev in rows:
            print(json.dumps(ev, ensure_ascii=False))
    else:
        for ev in rows:
            print(fmt(ev, color))
        print(f"[log_query] {len(rows)} 条（源：{', '.join(p.name for p in files_for(a.date, a.days)) or '无日志文件'}）",
              file=sys.stderr)
    return 0

if "--check" in sys.argv:
    print("OK: log_query --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
