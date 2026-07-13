#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clean_root_artifacts.py — 把根目录编译产物移入 build/（可逆）

问题
====
compile_all.py / chapter_compile_check.py / run_cpp_assertions.py 等编译工具
把 `.cpp`/`.exe`/`.o` 写到了 CWD（项目根），而非 build/，违反 AGENT.md 的
「源只读、只写 build/」红线。长期累积后根目录泄漏了上千个编译副产物，
hy3_check.py 的「工作区卫生」项此前漏检它们，误报"工作区干净"。

本工具
======
把根目录（非 Book/、非 build/、非 tools/）下的 *.cpp *.exe *.o **移动**到
`build/_root_artifacts/`。

设计选择
========
- **移动而非删除**：这些产物虽可重生，但移动可逆（需恢复时从 build/ 移回），
  比直接 rm 安全，且不会丢失任何可能被引用的中间产物。
- **只动根目录**：Book/（章源码）、build/（合法产物）、tools/（工具）一律不动。
- **只动编译产物后缀**：`.cpp/.exe/.o`，不碰 `.py`/`.md` 等源文件。
- 目标目录在 build/ 下，已被 .gitignore 覆盖，不影响版本库。

用法
====
  python tools/clean_root_artifacts.py           # 执行移动 + 报告前后计数
  python tools/clean_root_artifacts.py --dry      # 只报告，不移动
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEST = ROOT / "build" / "_root_artifacts"
EXTS = ("*.cpp", "*.exe", "*.o")


def collect() -> list[Path]:
    files: list[Path] = []
    for ext in EXTS:
        for f in ROOT.glob(ext):  # 非递归：仅根目录
            files.append(f)
    return sorted(files, key=lambda p: str(p))


def main():
    ap = argparse.ArgumentParser(description="根目录编译产物清理（移入 build/）")
    ap.add_argument("--dry", action="store_true", help="只报告，不移动")
    args = ap.parse_args()

    files = collect()
    print(f"根目录编译产物: {len(files)} 个")
    if not files:
        print("  ✅ 已干净，无需清理")
        return 0

    by_ext = {}
    for f in files:
        by_ext[f.suffix] = by_ext.get(f.suffix, 0) + 1
    print("  明细:", "  ".join(f"{k}={v}" for k, v in sorted(by_ext.items())))

    if args.dry:
        print("  (--dry) 未执行移动")
        return 0

    DEST.mkdir(parents=True, exist_ok=True)
    moved = 0
    for f in files:
        target = DEST / f.name
        # 同名防覆盖：加序号
        if target.exists():
            i = 1
            while (DEST / f"{f.stem}.{i}{f.suffix}").exists():
                i += 1
            target = DEST / f"{f.stem}.{i}{f.suffix}"
        shutil.move(str(f), str(target))
        moved += 1

    print(f"  ✅ 已移动 {moved} 个 → {DEST}")
    print(f"  恢复命令: 把 build/_root_artifacts/ 下的文件移回项目根目录")
    return 0


if __name__ == "__main__":
    sys.exit(main())
