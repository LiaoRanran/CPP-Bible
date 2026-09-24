"""632 D1 · L1 会话快照守卫（纯标准库，context manager，以 git 为真相源）。

`with PollutionGuard():` 包裹「可能写受控目录的操作」；退出时自动校验并在有残留时还原。
设计（632 规范 D1）：
1. 进入：`git diff -- atoms evidence Examples Book` 记录受控目录快照。
2. 退出：`git diff --quiet -- atoms evidence Examples Book`；有残留 →
   `git checkout -- atoms evidence Examples Book` 还原；还原后复检，仍残留 → 打印严重警告。
3. `--check`：只读，exit 0。
4. 单测 ≥5。

注：以 git 跟踪态为基准（未跟踪文件不计入；如需纳入，扩展 DIRS 为含 untracked 检测）。
铁律：纯标准库、必有 --check、≥5 例单测。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
CONTROLLED_DIRS = ("atoms", "evidence", "Examples", "Book")


class PollutionGuard:
    """受控目录会话守卫：进入记快照，退出校验+还原残留。"""

    def __init__(self, root: Path | None = None, run_git=None):
        self.root = Path(root) if root else REPO_ROOT
        self._run_git = run_git or self._real_run
        self._pre: str | None = None

    def _real_run(self, *args: str) -> "subprocess.CompletedProcess":
        return subprocess.run(
            ["git", *args], cwd=str(self.root),
            capture_output=True, text=True, check=False)

    def _diff(self) -> str:
        r = self._run_git("diff", "--", *CONTROLLED_DIRS)
        return r.stdout or ""

    def _restore(self) -> None:
        self._run_git("checkout", "--", *CONTROLLED_DIRS)

    def __enter__(self) -> "PollutionGuard":
        self._pre = self._diff()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        # 异常透传：守卫只管污染还原，不吞异常
        if exc_type is not None:
            return False
        post = self._diff()
        if post.strip():
            self._restore()
            if self._diff().strip():
                sys.stderr.write(
                    "严重警告：PollutionGuard 还原后受控目录仍有残留，"
                    "请人工核查（可能含未跟踪文件或还原失败）。\n")
        return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 D1 会话快照守卫")
    ap.add_argument("--check", action="store_true", help="只读，exit 0")
    args = ap.parse_args(argv)
    if args.check:
        print("632 D1 --check OK：PollutionGuard 可用（受控目录 %s）" % ", ".join(CONTROLLED_DIRS))
        return 0
    print("PollutionGuard 为 context manager，请用 `with PollutionGuard():` 包裹可能写受控目录的操作。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
