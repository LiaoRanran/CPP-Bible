"""632 D1 · pollution_guard_session_632 单测（≥5 例，纯标准库，不碰真实仓库）。"""
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pollution_guard_session_632 as pg  # noqa: E402


class FakeRun:
    """可控的 git 替身：按调用次序返回预设的 diff 输出，并记录 checkout 调用。"""
    def __init__(self, diffs):
        self.diffs = list(diffs)
        self.di = 0
        self.checkout_calls = 0

    def __call__(self, *args):
        if args and args[0] == "diff":
            v = self.diffs[self.di] if self.di < len(self.diffs) else ""
            self.di += 1
            return types.SimpleNamespace(stdout=v, returncode=0)
        if args and args[0] == "checkout":
            self.checkout_calls += 1
            return types.SimpleNamespace(stdout="", returncode=0)
        return types.SimpleNamespace(stdout="", returncode=0)


def test_enter_captures_snapshot():
    fake = FakeRun([""])
    g = pg.PollutionGuard(run_git=fake)
    g.__enter__()
    assert g._pre == ""


def test_no_residual_no_restore():
    fake = FakeRun(["", ""])  # enter diff, exit diff 均空
    g = pg.PollutionGuard(run_git=fake)
    with g:
        pass
    assert fake.checkout_calls == 0


def test_residual_triggers_restore():
    # enter "" , exit "diff...", restore 后复检 ""
    fake = FakeRun(["", "M atoms/x.md", ""])
    g = pg.PollutionGuard(run_git=fake)
    with g:
        pass
    assert fake.checkout_calls == 1


def test_residual_after_restore_warns(capsys):
    # enter "" , exit "x", restore, 复检仍 "y" ⇒ 严重警告
    fake = FakeRun(["", "x", "y"])
    g = pg.PollutionGuard(run_git=fake)
    with g:
        pass
    assert fake.checkout_calls == 1
    err = capsys.readouterr().err
    assert "严重警告" in err


def test_exception_propagates():
    fake = FakeRun(["", ""])
    g = pg.PollutionGuard(run_git=fake)
    try:
        with g:
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    else:
        raise AssertionError("异常应透传")


def test_main_check_exit_0():
    assert pg.main(["--check"]) == 0
