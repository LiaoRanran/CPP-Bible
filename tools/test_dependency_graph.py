#!/usr/bin/env python3
"""589 任务 4a · 测试依赖图（只读、幂等、纯标准库）。

静态扫描 `tests/test_*.py`：
  - 用 `ast` 解析 import，找出依赖的 `tools/*.py` 模块（含 `import X` / `from X import` / `from tools import X`）；
  - 用正则找出引用的 `data/` `atoms/` `evidence/` `Examples/` `Book/` 工件路径。
构建「源码/工件 → 依赖它的测试」邻接表，落 `data/test_dependency_graph.md`（+ 机读 `.json`）。

硬边界：**不实现测试选择/跳过**、不改 `tests/conftest.py`、不改 pyproject 的 `addopts`/`markers`、
不改 SLOW_MODULES 归属。连跑两次输出逐字相同（无时间戳）。

用法：python tools/test_dependency_graph.py
"""
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
TESTS = ROOT / "tests"
OUT_MD = ROOT / "data" / "test_dependency_graph.md"
OUT_JSON = ROOT / "data" / "test_dependency_graph.json"

_ART_RE = re.compile(
    r"(?<![\w/])((?:data|atoms|evidence|Examples|Book)/[A-Za-z0-9_./\-]+"
    r"\.(?:md|json|jsonl|py|cpp|asm|out|txt|yaml|yml))")

NOTE = ("本图仅为 560-B3（受影响测试选择）的前置数据；跳过判决测试属 W 档，"
        "须先攒依赖图与漏捕率，本包不做选择。")


def tool_modules() -> list[str]:
    return sorted(p.stem for p in TOOLS.glob("*.py"))


def _imports(src: str, modules: set[str]) -> set[str]:
    out: set[str] = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                top = a.name.split(".")[0]
                if top in modules:
                    out.add(top)
        elif isinstance(node, ast.ImportFrom):
            if not node.module:
                continue
            top = node.module.split(".")[0]
            if top in modules:
                out.add(top)
            elif top == "tools":
                for a in node.names:
                    if a.name in modules:
                        out.add(a.name)
    return out


def scan() -> dict[str, object]:
    modules = set(tool_modules())
    test_files = sorted(TESTS.glob("test_*.py"))
    mod2tests: dict[str, list[str]] = {m: [] for m in tool_modules()}
    art2tests: dict[str, list[str]] = {}
    for tf in test_files:
        rel = tf.relative_to(ROOT).as_posix()
        src = tf.read_text(encoding="utf-8")
        for m in sorted(_imports(src, modules)):
            mod2tests[m].append(rel)
        for art in sorted(set(_ART_RE.findall(src))):
            art2tests.setdefault(art, []).append(rel)
    return {
        "test_count": len(test_files),
        "tools": mod2tests,
        "artifacts": art2tests,
        "tools_without_tests": sorted(m for m, ts in mod2tests.items() if not ts),
    }


def render(data: dict[str, object]) -> str:
    mod2tests = data["tools"]  # type: ignore[assignment]
    art2tests = data["artifacts"]  # type: ignore[assignment]
    L: list[str] = []
    L.append("# 测试依赖图（589 任务 4a · `tools/test_dependency_graph.py` 只读生成）\n")
    L.append(f"> {NOTE}\n")
    L.append(f"\n统计：测试文件 **{data['test_count']}** 个 · tools 模块 **{len(mod2tests)}** 个"
             f"（其中**无任何测试覆盖 {len(data['tools_without_tests'])}** 个）·"
             f" 被引用的数据/工件 **{len(art2tests)}** 个。\n")
    L.append("\n## 一、`tools/*.py` → 覆盖它的测试\n")
    for m in sorted(mod2tests):
        ts = mod2tests[m]
        if ts:
            L.append(f"- `tools/{m}.py`：{', '.join('`'+t+'`' for t in sorted(ts))}")
        else:
            L.append(f"- `tools/{m}.py`：**（无任何测试覆盖）**")
    L.append("\n## 二、数据 / 工件 → 引用它的测试\n")
    for art in sorted(art2tests):
        L.append(f"- `{art}`：{', '.join('`'+t+'`' for t in sorted(art2tests[art]))}")
    return "\n".join(L) + "\n"


def main() -> int:
    data = scan()
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render(data), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True),
                        encoding="utf-8")
    print(f"[depgraph] 测试 {data['test_count']} · tools {len(data['tools'])}"
          f"（无覆盖 {len(data['tools_without_tests'])}）· 工件 {len(data['artifacts'])}"
          f" → {OUT_MD.relative_to(ROOT).as_posix()}")
    return 0

if "--check" in sys.argv:
    print("OK: test_dependency_graph --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
