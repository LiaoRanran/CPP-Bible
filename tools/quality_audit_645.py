"""645 · 阶段 F1/F2 · 优雅代码审计（docstring 覆盖 + 冗余清理，只读）。

目标（645 §八 F1/F2）：
- **F1 注释**：智能层+头部层工具模块 docstring 覆盖率 100%、公开类/函数 docstring 全覆盖。
- **F2 冗余**：静态 AST 扫描未使用 import（对照 ruff F401，用于交叉核验），输出可安全清理清单。

设计要点：
- 纯标准库 AST 静态分析，**只读不修改**——删除动作留给人工/F3 统一执行，避免误删。
- 未使用 import 用「导入名在模块其余位置是否出现」近似（含字符串注解），与 ruff 口径近似但
  独立实现，用作交叉验证（两把尺子互证）。
- `--check` 只读自检；`--run` 真实审计 645 工具，写 `data/645_quality_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "645_quality_report.md")
REPORT_JSON = os.path.join(DATA, "645_quality_report.json")


def _target_tools() -> list[str]:
    """本批 645 工具文件（含闸门与数据模型）。"""
    return sorted(f for f in os.listdir(TOOLS)
                  if f.endswith("_645.py"))


def _imported_names(tree: ast.AST) -> set[str]:
    """收集模块顶层 import 绑定的名字。"""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue  # __future__ 导入（annotations 等）非「使用」语义，跳过
            for a in node.names:
                if a.name != "*":
                    names.add(a.asname or a.name)
    return names


def _used_names(tree: ast.AST) -> set[str]:
    """收集模块中除导入语句外出现的所有标识符（含属性根、注解字符串）。"""
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            base: ast.expr = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # 字符串化注解 / 动态引用里可能含类型名
            for tok in node.value.replace("[", " ").replace("]", " ").replace(",", " ").split():
                used.add(tok.strip("\"'()"))
    return used


def audit_file(path: str) -> dict:
    """审计单个文件：docstring 缺失项 + 未使用 import 候选。"""
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    missing_doc: list[str] = []
    if not ast.get_docstring(tree):
        missing_doc.append("<module>")
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue  # 私有符号不计入覆盖率
            if not ast.get_docstring(node):
                missing_doc.append(node.name)
    imported = _imported_names(tree)
    used = _used_names(tree)
    unused = sorted(n for n in imported if n not in used)
    return {
        "file": os.path.basename(path),
        "missing_docstrings": missing_doc,
        "unused_import_candidates": unused,
    }


def audit() -> dict:
    """审计全部 645 工具，汇总覆盖率与冗余候选。"""
    files = _target_tools()
    results = [audit_file(os.path.join(TOOLS, f)) for f in files]
    total_public = 0
    total_missing = 0
    for r in results:
        # 每个文件至少有 module 节点；公开符号数按缺失+已覆盖近似统计
        total_missing += len(r["missing_docstrings"])
        total_public += len(r["missing_docstrings"]) + _covered_count(os.path.join(TOOLS, r["file"]))
    coverage = 1.0 if total_public == 0 else round(
        (total_public - total_missing) / total_public, 4)
    unused_total = sum(len(r["unused_import_candidates"]) for r in results)
    return {
        "tool_count": len(files),
        "docstring_coverage": coverage,
        "missing_docstring_files": {r["file"]: r["missing_docstrings"]
                                    for r in results if r["missing_docstrings"]},
        "unused_import_total": unused_total,
        "unused_import_files": {r["file"]: r["unused_import_candidates"]
                                for r in results if r["unused_import_candidates"]},
    }


def _covered_count(path: str) -> int:
    """统计有 docstring 的公开类/函数数量（用于覆盖率分母）。"""
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    n = 1 if ast.get_docstring(tree) else 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_") and ast.get_docstring(node):
                n += 1
    return n


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 优雅代码审计报告（F1 注释 + F2 冗余，只读）", "",
             f"- 645 工具数：{result['tool_count']}",
             f"- **docstring 覆盖率：{result['docstring_coverage']}**（F1 目标 100%）",
             f"- 未使用 import 候选：{result['unused_import_total']}（F2，交叉核验 ruff F401）", ""]
    lines.append("## 缺失 docstring 的文件/符号")
    if result["missing_docstring_files"]:
        for f, syms in result["missing_docstring_files"].items():
            lines.append(f"- `{f}`：{syms}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("## 未使用 import 候选（需人工复核后清理，本工具只读）")
    if result["unused_import_files"]:
        for f, names in result["unused_import_files"].items():
            lines.append(f"- `{f}`：{names}")
    else:
        lines.append("- （无）")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：AST 分析在一段合成源码上行为正确。"""
    import tempfile
    src = ('"""mod doc"""\n'
           "import os\n"
           "import json\n"
           "\n"
           "def pub():\n"
           '    """doc"""\n'
           "    return json.dumps({})\n"
           "\n"
           "class C:\n"
           '    """doc"""\n'
           "    pass\n")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8", newline="\n") as fh:
        fh.write(src)
        tmp = fh.name
    try:
        r = audit_file(tmp)
        assert r["missing_docstrings"] == []
        assert r["unused_import_candidates"] == ["os"]  # os 未被使用
    finally:
        os.unlink(tmp)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 优雅代码审计（F1/F2，只读）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实审计 645 工具")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = audit()
    write_report(result)
    print(f"[645 quality] 工具={result['tool_count']} docstring覆盖="
          f"{result['docstring_coverage']} 未用import={result['unused_import_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
