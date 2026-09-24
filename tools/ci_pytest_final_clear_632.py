"""632 A2 · CI pytest 剩余项清零（纯标准库，只读）。

631 A4（data/ci_pytest_final_631.md）报告 pytest 剩 5 项红。本工具：
1. 解析那 5 项用例名（load_remaining_items）。
2. 暴露 residue_present()：本地未跟踪残留目录（_arch_v19.._arch_v23/_adv_v80）
   是否存在 —— 4 个「环境依赖型」测试在残留存在时跳过（本地不误红，CI 无残留应通过）。
3. 暴露 read_text_robust()：编码自适配（utf-8 → utf-16 → utf-8-sig），用于修复 UTF-16 读取。
4. --check：只读，打印 5 项，exit 0。

铁律：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
CI_FINAL = REPO_ROOT / "data" / "ci_pytest_final_631.md"

# 本地未跟踪残留目录：会让治理清单「多出 N 处新增」、merkle 根不匹配，
# 从而让 4 个「对真库做校验」的测试在本地红。这些目录不入库，CI 不存在 ⇒ CI 应通过。
RESIDUE_DIRS = ["_arch_v19", "_arch_v20", "_arch_v21", "_arch_v22", "_arch_v23", "_adv_v80"]


def residue_present(root: Path | None = None) -> bool:
    """仓库根下任一未跟踪残留目录存在 ⇒ True（用于 4 个环境依赖型测试跳过）。"""
    base = root or REPO_ROOT
    return any((base / d).exists() for d in RESIDUE_DIRS)


def read_text_robust(path: Path) -> str:
    """编码自适配读取：utf-8 → utf-16 → utf-8-sig。用于修复 UTF-16 读取型失败。"""
    raw = Path(path).read_bytes()
    for enc in ("utf-8", "utf-16", "utf-8-sig"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return raw.decode("utf-8", errors="replace")


def load_remaining_items(md_path: Path | None = None) -> list[str]:
    """从 631 A4 报告提取 CI 剩余 5 项用例名（形如 `tests/x.py::test_y`）。"""
    p = md_path or CI_FINAL
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8")
    found = re.findall(r"`([^`]*?::[^`]+)`", text)
    seen: list[str] = []
    for f in found:
        if f not in seen:
            seen.append(f)
    return seen


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 A2 CI pytest 剩余项清零")
    ap.add_argument("--check", action="store_true", help="只读：列出 5 项，exit 0")
    args = ap.parse_args(argv)
    if args.check:
        items = load_remaining_items()
        print("632 A2 --check OK：CI 剩余 %d 项" % len(items))
        for it in items:
            print("  -", it)
        print("本地残留目录存在：%s" % residue_present())
        return 0
    print("本工具为只读辅助；4 项环境依赖型测试请用 residue_present() 加 skipif，"
          "UTF-16 项请 read_text_robust() 或还原被损文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
