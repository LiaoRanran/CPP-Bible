"""task_state 回归锁（494 任务 7 / 492 §4）：断点续跑的四个子命令与状态机。

隔离纪律：所有测试走 `base=tmp_path`（或 monkeypatch `ts.TASKS_DIR`），
**不写真实 `data/tasks/`**——运行时状态不入库（.gitignore 已加 `/data/tasks/`）。
"""
from __future__ import annotations

from pathlib import Path

import pytest
import task_state as ts


def test_create_writes_file_with_full_schema(tmp_path: Path):
    """create 落盘到 <base>/<id>.json，字段与 492 §4.2 逐字对齐。"""
    t = ts.create_task("fix_gate", "修 494 的 gate 规则", total=8,
                       assigned_to="cheap_agent", base=tmp_path)
    p = tmp_path / f"{t['task_id']}.json"
    assert p.is_file(), "create 必须落盘"
    import json
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("task_id", "type", "description", "status", "assigned_to",
                "created_at", "updated_at", "current_step", "total_step",
                "steps_completed", "steps_pending", "context_summary",
                "artifacts", "request_count", "request_limit"):
        assert key in data, f"缺字段 {key}"
    assert data["status"] == "pending" and data["current_step"] == 0


def test_update_advances_and_archives_previous_summary(tmp_path: Path):
    """推进步骤时上一步摘要归档进 steps_completed（自动累积，不靠人抄）。"""
    t = ts.create_task("demo", "d", total=3, base=tmp_path)
    tid = t["task_id"]
    ts.update_progress(tid, step=1, summary="第一步完成", base=tmp_path)
    t2 = ts.update_progress(tid, step=2, summary="第二步完成", base=tmp_path)
    assert t2["current_step"] == 2 and t2["status"] == "in_progress"
    assert any("第一步完成" in s for s in t2["steps_completed"]), t2["steps_completed"]
    assert t2["steps_pending"], "未完成步骤不得为空（total=3 且在第 2 步）"


def test_continue_prompt_contains_resume_context(tmp_path: Path):
    """continue-prompt 必须含：任务 id / 步骤进度 / 摘要 / 状态文件路径 / 更新命令。"""
    t = ts.create_task("demo2", "断点续跑冒烟", total=5, base=tmp_path)
    tid = t["task_id"]
    ts.update_progress(tid, step=2, summary="已跑一半", artifact="tools/x.py", base=tmp_path)
    text = ts.generate_continue_prompt(tid, base=tmp_path)
    for needle in (tid, "2/5", "已跑一半", f"data/tasks/{tid}.json",
                   "task_state.py update", "从第 3 步开始"):
        assert needle in text, f"续跑提示词缺 {needle!r}"


def test_request_limit_triggers_needs_continue(tmp_path: Path):
    """request_count 超过阈值 → status=needs_continue，且 check_request_limit 返回提示词。"""
    t = ts.create_task("demo3", "d", total=4, base=tmp_path)
    tid = t["task_id"]
    t2 = ts.update_progress(tid, step=1, summary="s", request_count=480, base=tmp_path)
    assert t2["status"] == "needs_continue", ">450 必须标记为待续跑"
    prompt = ts.check_request_limit(tid, 480, base=tmp_path)
    assert prompt and tid in prompt
    assert ts.check_request_limit(tid, 100, base=tmp_path) is None, "远未到上限不应触发"


def test_done_marks_finished(tmp_path: Path):
    t = ts.create_task("demo4", "d", total=2, base=tmp_path)
    tid = t["task_id"]
    ts.update_progress(tid, step=2, summary="做完", done=True, base=tmp_path)
    assert ts.load_task(tid, base=tmp_path)["status"] == "done"


def test_missing_task_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        ts.load_task("nope_20260101_000000", base=tmp_path)


def test_main_show_and_continue_do_not_write_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """CLI 路径：`show`/`continue-prompt` 输出到 stdout 且不触碰真实 data/。"""
    monkeypatch.setattr(ts, "TASKS_DIR", tmp_path / "tasks")
    assert ts.main(["create", "--type", "cli", "--desc", "d", "--total", "2"]) == 0
    tid = next((tmp_path / "tasks").glob("cli_*.json")).stem
    assert ts.main(["update", tid, "--step", "1/2", "--summary", "s"]) == 0
    assert ts.main(["show", tid]) == 0
    assert ts.main(["continue-prompt", tid]) == 0
    assert not (ts.ROOT / "data" / "tasks" / f"{tid}.json").exists(), "不得写真实 data/"
