"""校验手册正文中的引用键是否在 SOURCING 登记的白名单内。

扫描 ``Book/**/ch*.md`` 中形如 ``[key]`` 的行内引用键（排除 Markdown 链接
``[text](...)`` 与代码围栏），按 ``docs/references/SOURCING.md`` §1-§3 的键
前缀白名单校验：

- T0 标准（精确匹配）：``std-cpp20`` ``std-cpp23`` ``std-cpp26`` ``std-c11``
  ``std-c17``
- T1-T7 前缀：``cppref:`` ``isocpp:`` ``core:`` ``cert:`` ``book:`` ``gcc:``
  ``clang:`` ``llvm:`` ``msvc:`` ``cmake:`` ``qt:`` ``ue:`` ``ubsan:`` ``asan:``
  ``cppcon:`` ``so:``
- ``book:<slug>:<loc>`` 的 slug 必须在已登记书单内
- 含 ``<...>`` 占位符的键（如 ``book:templates:<ch>``）合法但单独计数，
  提示后续落地为具体条目

用法::

    python tools/check_citations.py           # 未知键则退出码 1
    python tools/check_citations.py --quiet   # 仅失败时输出明细

退出码：0 = 全部合法；1 = 存在未登记键。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCAN_ROOT = REPO / "Book"

# 行内键：小写字母开头，允许 前缀:子路径。
# 前置排除：前面是标识符/`]`/`[`（数组下标 v[i]、属性 [[attr]]）或后面跟 `(`（Markdown 链接）
KEY_RE = re.compile(r"(?<![\w\]\[])\[([a-z][a-z0-9-]*(?::[^\]\s]+)?)\](?!\()")

STD_KEYS = {"std-cpp20", "std-cpp23", "std-cpp26", "std-c11", "std-c17"}

PREFIXES = (
    "cppref:", "isocpp:", "core:", "cert:", "book:",
    "gcc:", "clang:", "llvm:", "msvc:", "abi:",
    "cmake:", "qt:", "ue:",
    "ubsan:", "asan:", "cppcon:", "so:",
    "hopl:", "ritchie:", "stepanov:", "qcon:", "de:",
)

# SOURCING §3.5 已登记的书籍 slug（含两本仍缺的 krc / exceptional-cpp）
BOOK_SLUGS = {
    "effective-modern", "effective-stl", "effective-cpp", "templates",
    "stdlib4", "josuttis17", "concurrency", "more-exceptional",
    "optimized-cpp", "swe-google", "cpp-guide", "tour",
    "primercpp", "primercpp3", "c-tutorial", "krc", "exceptional-cpp",
}


def strip_code_fences(text: str) -> str:
    """把代码围栏内的行置空，避免把示例代码里的方括号当成引用键。"""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def check_text(text: str) -> tuple[list[str], list[str], list[str], int]:
    """返回 (未知键, 占位符键, 标准条款锚点, 键总数)。

    无冒号的小写记号（如 ``[temp]`` ``[atomics.order]``）是 WG21 条款锚点
    写法，单独计数不算未知；带冒号的键才是 SOURCING 引用键，严格校验。
    """
    unknown: list[str] = []
    placeholder: list[str] = []
    clause: list[str] = []
    total = 0
    for m in KEY_RE.finditer(text):
        key = m.group(1)
        total += 1
        if ":" not in key:
            clause.append(key)
            continue
        if key in STD_KEYS:
            continue
        if not key.startswith(PREFIXES):
            unknown.append(key)
            continue
        if key.startswith("book:"):
            parts = key.split(":")
            if len(parts) < 2 or parts[1] not in BOOK_SLUGS:
                unknown.append(key)
                continue
        if "<" in key and ">" in key:
            placeholder.append(key)
    return unknown, placeholder, clause, total


def main() -> int:
    quiet = "--quiet" in sys.argv[1:]
    chapters = sorted(SCAN_ROOT.rglob("ch*.md"))
    if not chapters:
        print(f"[check_citations] no chapters found under {SCAN_ROOT}")
        return 1

    unknown_by_key: dict[str, list[str]] = {}
    key_total = 0
    placeholder_total = 0
    clause_total = 0
    with_refs = 0

    for ch in chapters:
        raw = ch.read_text(encoding="utf-8")
        if "## 参考引用" in raw:
            with_refs += 1
        unknown, placeholder, clause, total = check_text(strip_code_fences(raw))
        key_total += total
        placeholder_total += len(placeholder)
        clause_total += len(clause)
        rel = ch.relative_to(REPO).as_posix()
        for k in unknown:
            unknown_by_key.setdefault(k, []).append(rel)

    if not quiet or unknown_by_key:
        print(f"[check_citations] chapters={len(chapters)} with_refs={with_refs} "
              f"keys={key_total} clause_anchors={clause_total} "
              f"placeholders={placeholder_total} "
              f"unknown={sum(len(v) for v in unknown_by_key.values())}")
    if unknown_by_key:
        print("[check_citations] UNREGISTERED KEYS (add to SOURCING or fix):")
        for key in sorted(unknown_by_key):
            files = unknown_by_key[key]
            head = ", ".join(files[:3])
            more = f" …(+{len(files) - 3})" if len(files) > 3 else ""
            print(f"  [{key}]  {head}{more}")
        return 1
    if not quiet:
        print("[check_citations] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
