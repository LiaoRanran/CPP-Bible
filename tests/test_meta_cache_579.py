"""579 任务 4 回归锁：`_META_CACHE`/`_FM_CACHE` 的失效契约（注释收紧 + 显式 `invalidate_meta`）。

背景：原注释称"改盘即失效，不存在'改了内容还命中旧值'的窗口"——**实测过强**：
同尺寸改写若落在同一次时钟 tick 内键会相撞（本机 NTFS，间隔 0ms 时 200 次里 132 次相撞；
间隔 ≥0.5ms 起 0/12）。故补一个 O(n) 的显式失效口子，规定"进程内改盘必须调用"。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import gate_engine as ge  # noqa: E402


def test_579_invalidate_meta_after_same_size_rewrite(tmp_path: Path):
    """同尺寸改写后 `invalidate_meta()` 必须让 `_meta` 读到**新**内容。"""
    f = tmp_path / "card.md"
    a = "---\nid: A\nclaim_type: observation\n---\n"
    b = "---\nid: B\nclaim_type: observation\n---\n"     # 同尺寸，仅内容不同
    assert len(a) == len(b)
    f.write_text(a, encoding="utf-8")
    assert ge._meta(f).get("id") == "A"                  # 入缓存
    f.write_text(b, encoding="utf-8")
    assert ge.invalidate_meta(f) >= 1, "必须摘到条目"
    assert ge._meta(f).get("id") == "B", "显式失效后必须读到新内容"


def test_579_invalidate_meta_is_scoped_and_idempotent(tmp_path: Path):
    """只摘目标路径（不牺牲别的卡），且对未缓存路径安全返回 0。"""
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    for p, i in ((a, "A"), (b, "B")):
        p.write_text(f"---\nid: {i}\n---\n", encoding="utf-8")
        ge._meta(p)
    assert ge.invalidate_meta(a) >= 1
    assert ge.invalidate_meta(a) == 0, "再摘一次必须幂等返回 0"
    assert ge._meta(b).get("id") == "B", "别的卡的缓存不许被牵连"
    assert ge.invalidate_meta(tmp_path / "never.md") == 0
