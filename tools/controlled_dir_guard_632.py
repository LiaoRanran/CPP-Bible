"""632 C2 L1 · 受控目录快照守卫（纯标准库，只读）

把 631 C2 设计的「L1 会话级受控目录快照守卫」落地为可单测的工具：

- `snapshot(root)`：对受控目录（atoms/evidence/Examples/Book）每个文件算 sha256，
  返回 {相对路径: 哈希}；
- `diff(before, after)`：返回相对路径列表（新增 / 删除 / 内容变更）；
- 只比「会话结束时的最终状态」与「开始时」是否一致：测试内临时写盘、finally 还原的
  不算污染（放过"写脏又还原"是有意的，见 631 C2 设计 §五.3）；只有「残留改动」才判红。

`tests/conftest.py` 的 `controlled_dir_guard` 会话级 autouse fixture 调用本模块完成守护；
`--check` 用临时目录做自证（不碰真实受控目录），exit 0 = 通过。

铁律（沿用 631 §零）：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# 受控目录（与 631 C2 设计 §三 L1 一致）
CONTROLLED_DIRS = ("atoms", "evidence", "Examples", "Book")

# 快照时跳过的目录名（兜底；这些本就不在受控目录内）
_SKIP_DIRS = {".git", "__pycache__", ".pytest_tmp", "node_modules"}


def snapshot(root: Path | str) -> dict[str, str]:
    """受控目录下所有文件的 相对路径→sha256。目录不存在则跳过。"""
    root = Path(root)
    out: dict[str, str] = {}
    for d in CONTROLLED_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if any(part in _SKIP_DIRS for part in p.relative_to(root).parts):
                continue
            rel = p.relative_to(root).as_posix()
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def diff(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """返回相对路径列表：新增 / 删除 / 内容变更。稳定排序。"""
    changed: list[str] = []
    for rel in sorted(set(before) | set(after)):
        if before.get(rel) != after.get(rel):
            changed.append(rel)
    return changed


def _selftest() -> int:
    """临时目录自证：建树→快照→改→diff 检出→还原→diff 干净。不碰真实受控目录。"""
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "atoms").mkdir()
        (tdp / "atoms" / "a.md").write_text("hello")
        (tdp / "evidence").mkdir()
        (tdp / "evidence" / "e.txt").write_text("world")

        s0 = snapshot(tdp)
        assert s0, "空受控树也应产出快照"
        assert len(s0) == 2, s0

        # 改一个、删一个、加一个
        (tdp / "atoms" / "a.md").write_text("hello2")
        (tdp / "evidence" / "e.txt").unlink()
        (tdp / "atoms" / "b.md").write_text("new")
        s1 = snapshot(tdp)
        d = diff(s0, s1)
        assert set(d) == {"atoms/a.md", "evidence/e.txt", "atoms/b.md"}, d

        # 完全还原
        (tdp / "atoms" / "a.md").write_text("hello")
        (tdp / "atoms" / "b.md").unlink()
        (tdp / "evidence" / "e.txt").write_text("world")
        assert diff(s0, snapshot(tdp)) == [], "完全还原后应零差异"

    # 不存在的受控目录应安全跳过
    with tempfile.TemporaryDirectory() as td2:
        assert snapshot(Path(td2)) == {}, "无受控目录应返回空"
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 C2 L1 受控目录快照守卫")
    ap.add_argument("--check", action="store_true", help="只读自证，exit 0=通过")
    ap.add_argument("--root", default=str(ROOT), help="仓库根（默认自动推断）")
    args = ap.parse_args(argv)
    if args.check:
        return _selftest()
    snap = snapshot(args.root)
    print(f"受控目录守卫就绪：受控文件 {len(snap)} 个；运行 pytest 时由 conftest "
          f"在会话收尾比对残留改动（--check 可自证逻辑）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
