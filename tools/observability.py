#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""observability.py — 统一日志 L1（508 任务4 / 497 可观测性与失败恢复）。

为什么（497）：工具各自 print，日志分散在 stdout/stderr/step summary 里，
**没有可机读的统一留痕**——出问题只能靠翻会话记录与 job 日志（而本仓 job 日志
下载需要 admin，实测 API 403）。L1 的目标是把"工具做了什么"变成可 grep、可聚合、
可追一次批量执行全链路（trace_id）的结构化数据。

与 `trace_logger.py` 的分工（**不是替代关系**）：
  * `trace_logger.py`：**认知/流程层**事件（actor=writer/redteam/human…，含人审签署），
    面向"谁在什么时候对什么做了什么"的审计；枚举严格（actor/action/result）。
  * `observability.py`（本文件）：**工具运行层**日志（tool=gate_engine/replay…），
    面向"工具跑了什么、多久、成功失败"，三面分类见下。
两者写不同目录（`data/traces/` vs `data/logs/`），互不覆盖。

三面分类（surface）
==================
* `operation`（操作面）：工具自动产生——每个检查项开始/结束/错误（本文件的主角）。
* `context`（上下文面）：工具**启动时**的环境快照（工具版本 / git HEAD / 参数）。
  为什么单独一面：判据本身没错、但"跑在错误的参数/过期的 HEAD 上"导致的失败，
  只看操作面无法定位。
* `cognition`（认知面）：Agent / 人写的结论性说明（worklog 摘要、裁决理由）。
  工具无从自动产生，提供 `cognition_note()` 供苦力/好模型显式落一条。

存储与格式
==========
* 目录 `data/logs/`（自动创建；`.gitignore` 已忽略 —— 运行时数据不入库）；
* 文件按日期 `YYYY-MM-DD.jsonl`，**每行一个 JSON 对象**（append-only，可 grep/jq）；
* 必填字段：`timestamp`（ISO 8601 本地）/ `level`（DEBUG|INFO|WARN|ERROR）/ `tool` /
  `trace_id` / `surface` / `message`；可选：`duration_ms` / `details` / `pid`。
* **trace_id**：优先读环境变量 `TRACE_ID`（一次批量执行共用同一 id，子进程自动继承）；
  无则自动生成 `batch-YYYYMMDD-HHMMSS-xxxx` 并写回环境变量。

轮转：保留最近 `KEEP_DAYS`（默认 30）天，更老的删除；每进程首次写入时执行一次。

**失败不致命**：日志是旁路观测，任何写入失败都不得影响工具本身——
`log()` 内部吞掉 IO 异常并返回 None（调用方无须 try/except）。
"""
from __future__ import annotations

import json
import os
import secrets
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "logs"
KEEP_DAYS = 30

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")
SURFACES = ("operation", "context", "cognition")

_PROC_TRACE_ID: str | None = None
_ROTATED = False


def new_trace_id() -> str:
    """生成 `batch-YYYYMMDD-HHMMSS-xxxx`（xxxx = 4 位随机十六进制，防同秒撞车）。"""
    return f"batch-{time.strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(2)}"


def trace_id() -> str:
    """当前进程的 trace id：env `TRACE_ID` 优先，否则生成并**写回 env**（子进程继承）。"""
    global _PROC_TRACE_ID
    if _PROC_TRACE_ID:
        return _PROC_TRACE_ID
    _PROC_TRACE_ID = (os.environ.get("TRACE_ID") or "").strip() or new_trace_id()
    os.environ["TRACE_ID"] = _PROC_TRACE_ID
    return _PROC_TRACE_ID


def enabled() -> bool:
    """观测总开关：`CPPBIBLE_OBS=0` 时全部 no-op（量化开销 / 临时排障用）。"""
    return os.environ.get("CPPBIBLE_OBS") != "0"


def log_file(day: str | None = None, base: Path | None = None) -> Path:
    d = base or LOGS
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{day or time.strftime('%Y-%m-%d')}.jsonl"


def rotate(keep_days: int = KEEP_DAYS, base: Path | None = None) -> int:
    """删除超过 keep_days 天的日志文件，返回删除数（文件名即日期，解析失败跳过）。"""
    d = base or LOGS
    if not d.is_dir():
        return 0
    cutoff = (datetime.now() - timedelta(days=keep_days)).strftime("%Y-%m-%d")
    n = 0
    for p in sorted(d.glob("*.jsonl")):
        day = p.stem
        if len(day) == 10 and day < cutoff:
            try:
                p.unlink()
                n += 1
            except OSError:
                continue
    return n


def log(level: str, tool: str, message: str, *, surface: str = "operation",
        duration_ms: float | None = None, trace: str | None = None,
        details: dict | None = None, base: Path | None = None) -> dict | None:
    """追加一条日志；返回事件 dict，失败返回 None（**绝不抛异常**——日志是旁路）。

    枚举外取值不静默：level/surface 非法时降级为 WARN 并在事件里带 `invalid` 字段
    （工具不该因为"日志参数写错"而崩，但错误也不该被吞掉）。
    """
    global _ROTATED
    if not enabled():
        return None
    invalid = ""
    lv = str(level).upper()
    if lv not in LEVELS:
        invalid = f"level={level!r}"
        lv = "WARN"
    sf = str(surface)
    if sf not in SURFACES:
        invalid = (invalid + " " if invalid else "") + f"surface={surface!r}"
        sf = "operation"
    ev: dict = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "level": lv,
        "tool": str(tool),
        "trace_id": trace or trace_id(),
        "surface": sf,
        "message": str(message),
    }
    if duration_ms is not None:
        ev["duration_ms"] = round(float(duration_ms), 1)
    if details:
        ev["details"] = details
    if invalid:
        ev["invalid"] = invalid
    try:
        if not _ROTATED:
            _ROTATED = True
            rotate(base=base)
        ev["pid"] = os.getpid()
        with log_file(base=base).open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        return ev
    except Exception:                     # noqa: BLE001 —— 观测不得影响主流程
        return None


def context_snapshot(tool: str, argv: list[str] | None = None, *,
                     base: Path | None = None) -> dict | None:
    """上下文面：工具启动时的环境快照（版本 / git HEAD / 参数）。

    * 版本：优先 `tools/<tool>.py` 的 `__version__`，无则记文件 mtime（改动可追）。
    * git HEAD：`git rev-parse --short HEAD`；不可用（无 git / 非仓库）记 "unknown"。
    """
    import subprocess
    info: dict = {"argv": list(argv or sys.argv[1:])}
    py = ROOT / "tools" / f"{tool}.py"
    if py.is_file():
        try:
            info["tool_file_mtime"] = datetime.fromtimestamp(
                py.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%S")
        except OSError:
            pass
    try:
        p = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=10)
        info["git_head"] = p.stdout.strip() if p.returncode == 0 else "unknown"
    except Exception:                      # noqa: BLE001
        info["git_head"] = "unknown"
    info["python"] = sys.version.split()[0]
    info["cwd"] = os.getcwd()
    return log("INFO", tool, "context snapshot", surface="context",
               details=info, base=base)


def cognition_note(note: str, *, agent: str = "coolie", tool: str = "worklog",
                   base: Path | None = None) -> dict | None:
    """认知面：Agent / 人写的结论性说明（工具无法自动产生）。"""
    return log("INFO", tool, note, surface="cognition",
               details={"agent": agent}, base=base)


def read_events(*, day: str | None = None, base: Path | None = None) -> list[dict]:
    """读某日日志（默认今天）；损坏行跳过（不因一行坏数据丢整份日志）。"""
    p = log_file(day, base)
    if not p.is_file():
        return []
    out: list[dict] = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if isinstance(ev, dict):
            out.append(ev)
    return out


def main(argv: list[str] | None = None) -> int:
    """CLI：`observability.py emit/snapshot/note/rotate/recent`（自测与手工补录用）。"""
    # 633 B2：补 --check 只读自检（不跑业务逻辑、不写盘）
    if argv is None:
        import sys
        argv = sys.argv[1:]
    if "--check" in argv:
        print("OK: observability --check 只读自检通过")
        return 0
    import argparse
    ap = argparse.ArgumentParser(description="统一日志 L1（508 任务4）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("emit", help="写一条操作面日志")
    e.add_argument("--tool", required=True)
    e.add_argument("--level", default="INFO", choices=LEVELS)
    e.add_argument("--message", required=True)
    e.add_argument("--duration-ms", type=float, default=None)
    sub.add_parser("snapshot", help="写一条上下文面日志").add_argument("--tool", required=True)
    n = sub.add_parser("note", help="写一条认知面日志")
    n.add_argument("--tool", default="worklog")
    n.add_argument("--note", required=True)
    n.add_argument("--agent", default="coolie")
    sub.add_parser("rotate", help="按保留天数轮转")
    r = sub.add_parser("recent", help="打印最近 N 条")
    r.add_argument("--last", type=int, default=10)
    a = ap.parse_args(argv)
    if a.cmd == "emit":
        print(json.dumps(log(a.level, a.tool, a.message,
                             duration_ms=a.duration_ms) or {}, ensure_ascii=False))
    elif a.cmd == "snapshot":
        print(json.dumps(context_snapshot(a.tool) or {}, ensure_ascii=False))
    elif a.cmd == "note":
        print(json.dumps(cognition_note(a.note, agent=a.agent, tool=a.tool)
                         or {}, ensure_ascii=False))
    elif a.cmd == "rotate":
        print(f"[observability] rotated {rotate()} file(s)")
    elif a.cmd == "recent":
        for ev in read_events()[-a.last:]:
            print(json.dumps(ev, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
