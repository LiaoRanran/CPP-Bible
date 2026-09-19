#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task_state.py — 任务状态文件工具（494 任务 7，规格 492 §四）：断点续跑的最小闭环。

为什么需要（492 §4.1）
======================
Agent 单次会话有请求上限（约 500 次）。到顶后上下文丢失、必须人手动开新会话重新描述任务，
进度可能丢失。本工具把**进度外化成文件**（`data/tasks/<id>.json`）——
续跑只依赖文件，不依赖记忆；人只需把 `continue-prompt` 的输出喂给新会话。

四个子命令
==========
    python tools/task_state.py create --type <type> --desc "<描述>" [--total 8] [--assigned-to cheap_agent]
    python tools/task_state.py update <id> --step 3/8 --summary "<这一步的进展>" [--artifact <path>] [--request-count 480]
    python tools/task_state.py continue-prompt <id>     # 生成可直接投喂新会话的续跑提示词
    python tools/task_state.py show <id>

状态字段（492 §4.2，逐字对齐）
==============================
task_id / type / description / status / assigned_to / created_at / updated_at /
current_step / total_step / steps_completed / steps_pending / context_summary /
artifacts / request_count / request_limit

状态机：`pending` →（首次 update）`in_progress` →（request_count > 450 或显式 `--needs-continue`）
`needs_continue` →（`--done`）`done`。**不为门禁服务**：本工具只读写 `data/tasks/`（已 gitignore），
不参与 gate/replay/poison（运行时状态不入库，492 §十：状态文件由 git 跟踪的选择留给用户裁决）。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "data" / "tasks"

DEFAULT_REQUEST_LIMIT = 500
CONTINUE_THRESHOLD = 450          # 492 §4.2：>450 即建议输出续跑提示词
STATUSES = ("pending", "in_progress", "needs_continue", "done")


def _dir(base: Path | None = None) -> Path:
    d = base or TASKS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(task_id: str, base: Path | None = None) -> Path:
    return _dir(base) / f"{task_id}.json"


def load_task(task_id: str, base: Path | None = None) -> dict:
    p = _path(task_id, base)
    if not p.is_file():
        raise FileNotFoundError(f"任务不存在：{task_id}（{p}）")
    return json.loads(p.read_text(encoding="utf-8"))


def save_task(task: dict, base: Path | None = None) -> Path:
    p = _path(task["task_id"], base)
    task["updated_at"] = _now()
    p.write_text(json.dumps(task, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def create_task(task_type: str, description: str, *, total: int = 0,
                assigned_to: str = "unassigned", base: Path | None = None,
                request_limit: int = DEFAULT_REQUEST_LIMIT) -> dict:
    """创建任务并落盘，返回任务字典（`task_id` 可读且唯一：`<type>_<时间戳>`）。"""
    ts = time.strftime("%Y%m%d_%H%M%S")
    task_id = f"{task_type}_{ts}"
    n = 1
    while _path(task_id, base).exists():        # 同秒重复创建也能唯一
        n += 1
        task_id = f"{task_type}_{ts}_{n}"
    task = {
        "task_id": task_id, "type": task_type, "description": description,
        "status": "pending", "assigned_to": assigned_to,
        "created_at": _now(), "updated_at": _now(),
        "current_step": 0, "total_step": total,
        "steps_completed": [], "steps_pending": [],
        "context_summary": "", "artifacts": [],
        "request_count": 0, "request_limit": request_limit,
    }
    _refresh_pending(task)
    save_task(task, base)
    return task


def _refresh_pending(task: dict) -> None:
    """待完成步骤：显式列表优先，否则按 total-current 生成**可执行的下一步指引**。"""
    total, cur = int(task.get("total_step") or 0), int(task.get("current_step") or 0)
    explicit = task.get("_pending_explicit")
    if explicit:
        task["steps_pending"] = list(explicit)
    elif total > cur:
        task["steps_pending"] = [f"从第 {cur + 1}/{total} 步继续（见续跑提示词）"]
    else:
        task["steps_pending"] = []


def update_progress(task_id: str, *, step: int | None = None, total: int | None = None,
                    summary: str | None = None, artifact: str | None = None,
                    request_count: int | None = None, pending: str | None = None,
                    done: bool = False, needs_continue: bool = False,
                    base: Path | None = None) -> dict:
    """更新进度。步骤推进时把**上一步的摘要归档**进 `steps_completed`（自动累积，无需手抄）。"""
    task = load_task(task_id, base)
    prev_step = int(task.get("current_step") or 0)
    if total is not None:
        task["total_step"] = int(total)
    if step is not None:
        task["current_step"] = int(step)
    if pending is not None:
        task["_pending_explicit"] = [s.strip() for s in pending.split(",") if s.strip()]
    if summary is not None:
        old = str(task.get("context_summary") or "")
        if old and (step is None or int(step) != prev_step):
            task["steps_completed"] = list(task.get("steps_completed") or []) + \
                [f"step {prev_step}: {old}"]
        task["context_summary"] = summary
    if artifact:
        arts = list(task.get("artifacts") or [])
        if artifact not in arts:
            arts.append(artifact)
        task["artifacts"] = arts
    if request_count is not None:
        task["request_count"] = int(request_count)
    if task["status"] == "pending" and (step or summary):
        task["status"] = "in_progress"
    if needs_continue or int(task.get("request_count") or 0) >= CONTINUE_THRESHOLD:
        task["status"] = "needs_continue"
    if done:
        task["status"] = "done"
    _refresh_pending(task)
    if done:
        task.pop("_pending_explicit", None)
    save_task(task, base)
    return task


def generate_continue_prompt(task_id: str, base: Path | None = None) -> str:
    """生成**可直接投喂新会话**的续跑提示词（492 §4.3 模板 + 落地细节）。"""
    t = load_task(task_id, base)
    nxt = int(t.get("current_step") or 0) + 1
    total = int(t.get("total_step") or 0)
    done = "\n".join(f"  - {s}" for s in (t.get("steps_completed") or [])) or "  （无）"
    pend = "\n".join(f"  - {s}" for s in (t.get("steps_pending") or [])) or "  （无）"
    arts = "、".join(t.get("artifacts") or []) or "（未记录）"
    rel = f"data/tasks/{t['task_id']}.json"
    near = int(t.get("request_count") or 0) >= CONTINUE_THRESHOLD
    return f"""你是续跑 Agent。任务 {t['task_id']}（type={t.get('type')}，状态={t.get('status')}）
在上一个会话中执行到第 {t.get('current_step')}/{total or '?'} 步。

任务描述：{t.get('description')}

已完成：
{done}

待完成：
{pend}

当前进度摘要：{t.get('context_summary') or '（未填写）'}
涉及文件：{arts}

请从第 {nxt} 步开始继续（先 Read 状态文件与涉及文件，不要凭记忆）。
任务状态文件：{rel}
每次操作后更新：
  python tools/task_state.py update {t['task_id']} --step {nxt}/{total or '?'} --summary "<进展>"
{'⚠️ request_count=%s 已接近上限（>%d）：先更新状态文件，再输出本提示词。'
     % (t.get('request_count'), CONTINUE_THRESHOLD) if near else
 '接近请求上限（请求数 > %d）时，先更新状态文件，再输出本续跑提示词。' % CONTINUE_THRESHOLD}
"""


def check_request_limit(task_id: str, current_count: int,
                        base: Path | None = None) -> str | None:
    """492 §4.2：`>450` 时返回续跑提示词，否则 None（供外部调度器/Agent 轮询）。"""
    if current_count > CONTINUE_THRESHOLD:
        update_progress(task_id, request_count=current_count, base=base)
        return generate_continue_prompt(task_id, base)
    return None


def _show(task: dict) -> str:
    lines = [
        f"task_id     : {task['task_id']}",
        f"type        : {task.get('type')}",
        f"description : {task.get('description')}",
        f"status      : {task.get('status')}",
        f"assigned_to : {task.get('assigned_to')}",
        f"step        : {task.get('current_step')}/{task.get('total_step')}",
        f"requests    : {task.get('request_count')}/{task.get('request_limit')}",
        f"updated_at  : {task.get('updated_at')}",
        f"summary     : {task.get('context_summary') or '（空）'}",
        f"artifacts   : {', '.join(task.get('artifacts') or []) or '（无）'}",
        "completed   :",
    ]
    lines += [f"  - {s}" for s in (task.get("steps_completed") or [])] or ["  （无）"]
    lines.append("pending     :")
    lines += [f"  - {s}" for s in (task.get("steps_pending") or [])] or ["  （无）"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="任务状态文件（断点续跑，492 §4）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="创建任务")
    c.add_argument("--type", required=True)
    c.add_argument("--desc", required=True)
    c.add_argument("--total", type=int, default=0)
    c.add_argument("--assigned-to", default="unassigned")

    u = sub.add_parser("update", help="更新进度")
    u.add_argument("task_id")
    u.add_argument("--step", default=None, help="形如 3/8（同时给 --step 与总数）")
    u.add_argument("--summary", default=None)
    u.add_argument("--artifact", action="append", default=[])
    u.add_argument("--request-count", type=int, default=None)
    u.add_argument("--pending", default=None, help="逗号分隔的待完成步骤（覆盖自动生成）")
    u.add_argument("--done", action="store_true")
    u.add_argument("--needs-continue", action="store_true")

    p = sub.add_parser("continue-prompt", help="生成续跑提示词")
    p.add_argument("task_id")

    s = sub.add_parser("show", help="打印任务状态")
    s.add_argument("task_id")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "create":
            t = create_task(a.type, a.desc, total=a.total, assigned_to=a.assigned_to)
            print(t["task_id"])
            return 0
        if a.cmd == "update":
            step = total = None
            if a.step:
                if "/" in a.step:
                    step, total = (int(x) for x in a.step.split("/", 1))
                else:
                    step = int(a.step)
            t = update_progress(a.task_id, step=step, total=total, summary=a.summary,
                                artifact=(a.artifact[-1] if a.artifact else None),
                                request_count=a.request_count, pending=a.pending,
                                done=a.done, needs_continue=a.needs_continue)
            for art in a.artifact[:-1]:
                t = update_progress(a.task_id, artifact=art)
            print(_show(t))
            if int(t.get("request_count") or 0) >= CONTINUE_THRESHOLD and not a.done:
                print(f"\n[task_state] ⚠ 请求数 {t['request_count']} ≥ {CONTINUE_THRESHOLD}："
                      f"建议输出续跑提示词（`continue-prompt {t['task_id']}`）")
            return 0
        if a.cmd == "continue-prompt":
            print(generate_continue_prompt(a.task_id))
            return 0
        if a.cmd == "show":
            print(_show(load_task(a.task_id)))
            return 0
    except FileNotFoundError as e:
        print(f"[task_state] {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
