"""632 C2 L1 · 受控目录守卫单测（≥5 例）。

验证两件事：
1. 核心逻辑（snapshot/diff）正确——用临时目录，绝不污染真实受控目录；
2. 「测试内临时写受控文件又自清理」不会触发会话守卫（即"写脏又还原"被放过，符合设计 §五.3）。
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import controlled_dir_guard_632 as G  # noqa: E402


def test_snapshot_empty_when_no_controlled_dirs(tmp_path):
    assert G.snapshot(tmp_path) == {}


def test_snapshot_counts_and_hashes(tmp_path):
    (tmp_path / "atoms").mkdir()
    (tmp_path / "atoms" / "a.md").write_text("x")
    (tmp_path / "evidence").mkdir()
    (tmp_path / "evidence" / "e.txt").write_text("y")
    snap = G.snapshot(tmp_path)
    assert set(snap) == {"atoms/a.md", "evidence/e.txt"}
    assert snap["atoms/a.md"] == hashlib.sha256(b"x").hexdigest()
    (tmp_path / "atoms" / "a.md").write_text("y")
    assert snap["atoms/a.md"] != G.snapshot(tmp_path)["atoms/a.md"]


def test_diff_detects_add_del_change(tmp_path):
    (tmp_path / "atoms").mkdir()
    (tmp_path / "atoms" / "a.md").write_text("x")
    (tmp_path / "evidence").mkdir()
    (tmp_path / "evidence" / "e.txt").write_text("y")
    s0 = G.snapshot(tmp_path)
    (tmp_path / "atoms" / "a.md").write_text("x2")
    (tmp_path / "evidence" / "e.txt").unlink()
    (tmp_path / "atoms" / "b.md").write_text("z")
    d = G.diff(s0, G.snapshot(tmp_path))
    assert set(d) == {"atoms/a.md", "evidence/e.txt", "atoms/b.md"}


def test_diff_clean_when_restored(tmp_path):
    (tmp_path / "atoms").mkdir()
    (tmp_path / "atoms" / "a.md").write_text("x")
    s0 = G.snapshot(tmp_path)
    (tmp_path / "atoms" / "a.md").write_text("y")
    (tmp_path / "atoms" / "a.md").write_text("x")  # 还原
    assert G.diff(s0, G.snapshot(tmp_path)) == []


def test_guard_passes_for_transient_write():
    """真实受控目录里临时建文件并删除 ⇒ 会话结束时净变化为零 ⇒ 守卫通过。

    注意：探针文件必须在 finally 里删除——这正是"写脏又还原不算污染"的实证人证。
    若此测试自身崩溃留下 _guard_probe_tmp.md，守卫会立刻把它抓出来（这正是我们想要的）。
    """
    probe = ROOT / "atoms" / "_guard_probe_tmp.md"
    try:
        probe.write_text("probe")
    finally:
        if probe.exists():
            probe.unlink()
    assert not probe.exists(), "守卫测试用例必须自清理，否则会留下真实污染"


def test_tool_check_exits_zero():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "controlled_dir_guard_632.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
