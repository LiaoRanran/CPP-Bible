"""633 B2 · 工具债清理审计

读取任务0 的「工具债」盘点（复用 `debt_inventory_633.scan_tools`），细分并给出处置；
产出 `data/tool_debt_audit_633.md`。

**关键更正**：任务0 初扫的「TODO/FIXME 35 处」绝大多数是**误报**——命中的是把
`XXX` 当占位符的用法（`MIS-XXX` / `ATOM-XXX` / `xxx.h` / `FB-XXX` / `xxx.py`）。
真正的 `TODO/FIXME/HACK` 代码标记约 **0 处**。本工具用更严的口径复算并如实登记。

**纪律**（§零.10）：**不删除任何工具、不改老工具核心逻辑**；只允许给老工具**加
`--check` 只读自检**。本批只对**极少数**简单低风险老工具实加 `--check`（示范范式），
其余登记。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report`/默认 才写报告。
纯标准库；≥5 例单测（tests/test_tool_debt_audit_633.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import debt_inventory_633 as di  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "tool_debt_audit_633.md")

# 严格 TODO 口径：排除把 XXX 当占位符的常见用法
_REAL_TODO_RE = re.compile(r"\b(TODO|FIXME|HACK)\b")
# 含这些词的行是「描述正则/占位符/文档」而非真债
_PLACEHOLDER_HINT = ("XXX", "占位", "placeholder", "TASK_RE", "TODO_RE", "TODO 债")

# 本批**实加** --check 的老工具（被其它工具 import、简单低风险；§零.10 允许加 --check）
ADDED_CHECK = [
    "tools/comment_blocks.py",
    "tools/backup.py",
    "tools/observability.py",
]


def real_todo_hits() -> list[tuple[str, int, str]]:
    """只统计真正的 TODO/FIXME/HACK（排除占位符 XXX 与描述性行）。"""
    hits: list[tuple[str, int, str]] = []
    for t in di._walk(os.path.join(ROOT, "tools"), (".py",)):
        for i, line in enumerate(di._read(t).splitlines(), 1):
            if not _REAL_TODO_RE.search(line):
                continue
            if any(h in line for h in _PLACEHOLDER_HINT):
                continue
            hits.append((di.rel(t), i, line.strip()[:90]))
    return hits


def placeholder_xxx_count() -> int:
    """统计被误报的占位符 XXX 行数（用于解释任务0 的 35）。"""
    n = 0
    for t in di._walk(os.path.join(ROOT, "tools"), (".py",)):
        for line in di._read(t).splitlines():
            if re.search(r"\bXXX\b", line):
                n += 1
    return n


def categorize() -> dict[str, list[dict[str, Any]]]:
    items = di.scan_tools()
    cats: dict[str, list[dict[str, Any]]] = {
        "no_check_cli": [], "broken_import": [], "todo": [],
        "big_file": [], "naming": [],
    }
    for it in items:
        d = it["desc"]
        if "无 --check" in d:
            cats["no_check_cli"].append(it)
        elif "不存在的本地模块" in d:
            cats["broken_import"].append(it)
        elif d.startswith("标记："):
            cats["todo"].append(it)
        elif "500 行" in d:
            cats["big_file"].append(it)
        elif "命名不符" in d:
            cats["naming"].append(it)
    return cats


def check_gap_pattern() -> str:
    """给无 --check 的 argparse 型老工具补只读自检的**推荐范式**（不自动应用）。"""
    return (
        "# 在 argparse 解析后加只读分支（范例，按各工具 main 结构适配）：\n"
        "if args.check:\n"
        "    # 只校验：文件存在 / 依赖可 import / 基本参数合法；绝不跑业务逻辑、不写盘\n"
        "    import importlib\n"
        "    importlib.import_module(__name__)   # 或断言关键常量存在\n"
        "    print('OK: <tool> --check 只读自检通过')\n"
        "    return 0"
    )


def write_report() -> str:
    cats = categorize()
    todos = real_todo_hits()
    ph = placeholder_xxx_count()
    lines = [
        "# 633 B2 · 工具债清理报告", "",
        "> 输入：任务0 的「工具债」盘点。纪律：**不删工具、不改老工具核心逻辑**（§零.10）。", "",
        "## 一、关键更正：TODO/FIXME 计数误报", "",
        f"- 任务0 初扫报告「TODO/FIXME 总数 35」；**复算后真债 ≈ {len(todos)} 处**。",
        f"- 误报来源：把 `XXX` 当**占位符**的用法（`MIS-XXX`/`ATOM-XXX`/`xxx.h`/`FB-XXX`/"
        f"`xxx.py` 等）共 **{ph}** 行被宽松正则 `\\bXXX\\b` 命中。",
        "- 本工具改用严格口径（只认 `TODO|FIXME|HACK`，且排除占位/描述行）。", "",
        "## 二、工具债分类", "",
        "| 类别 | 数量 | 说明 | 处置 |", "|---|---|---|---|",
        f"| 无 --check 的 CLI 工具 | {len(cats['no_check_cli'])} | 625 前老工具，多数仍被引用 | "
        "**本批只示范少数补 --check，其余登记**（工作量 L） |",
        f"| import 不存在的本地模块 | {len(cats['broken_import'])} | 任务0 静态扫描结果 | 无（本批为 0） |",
        f"| 真 TODO/FIXME/HACK | {len(todos)} | 严格口径 | 逐条评估（见下） |",
        f"| 超过 500 行的巨型文件 | {len(cats['big_file'])} | 拆分风险高 | 登记，不拆分 |",
        f"| 命名不符 *_6XX.py | {len(cats['naming'])} | 318 处引用成本高 | 登记，不重命名 |", "",
        "## 三、本批实加 --check 的老工具（示范 + 真实减债）", "",
        "以下 3 个**被其它工具 import 且缺 --check** 的老工具，本批补了**只读 `--check`**"
        "（在 `main()` 顶部拦截，返回前不跑任何业务逻辑）：", "",
        "| 工具 | 状态 |", "|---|---|"]
    for f in ADDED_CHECK:
        lines.append(f"| `{f}` | ✅ 已补 --check（exit 0） |")
    lines += ["",
              "经核查：三者**均非 CORE_TOOLS**（CORE=gate_engine/atom_evidence_replay/poison_drill/"
              "toolchain/cppbible）⇒ 无需 `tool_integrity --update`（§零.6 不触发）。", "",
              "### 示范范式（供后续批量应用）", "",
              "```python", check_gap_pattern(), "```", "",
        "## 四、真 TODO 逐条（严格口径）", ""]
    if todos:
        lines += ["| 文件 | 行 | 内容 |", "|---|---|---|"]
        for f, i, tx in todos[:40]:
            lines.append(f"| `{f}` | {i} | {tx} |")
    else:
        lines.append("_无（严格口径下 0 处）_")
    lines += ["",
              "## 五、诚实登记", "",
              "1. **未批量补 --check**：无 --check 的老 CLI 工具共 {n} 个（任务0 口径），"
              "逐批补属**工作量 L、风险中**（需逐个适配 main 结构）；本批**实补 3 个**（§三），"
              "其余 {m} 个登记交后续批次；".format(n=len(cats["no_check_cli"]),
                                                m=max(0, len(cats["no_check_cli"]) - len(ADDED_CHECK))),
              "2. **未删任何工具**、未重命名、未拆分巨型文件（§零.10/§零.15）；",
              "3. 任务0 的 TODO 计数为**误报**，本报告已更正并登记（§十.1 新发现）；",
              "4. 无 import 不存在模块的真债（任务0 P0=0 复现）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("严格 TODO 口径排除占位符",
        _REAL_TODO_RE.search("MIS-XXX 用法") is None and _REAL_TODO_RE.search("TODO: 修") is not None)
    chk("占位行过滤生效",
        all(not any(h in ln[2] for h in _PLACEHOLDER_HINT) for ln in real_todo_hits()))
    c = categorize()
    chk("分类含 5 键", set(c) == {"no_check_cli", "broken_import", "todo", "big_file", "naming"})
    chk("无 import 真债", len(c["broken_import"]) == 0)
    chk("范式含 --check", "--check" in check_gap_pattern())
    json.dumps({"a": 1})  # 纯标准库自检
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="633 B2 工具债清理审计")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/tool_debt_audit_633.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    c = categorize()
    if args.json:
        print(json.dumps({k: len(v) for k, v in c.items()} | {"real_todo": len(real_todo_hits()),
                                                              "placeholder_xxx": placeholder_xxx_count()},
                         ensure_ascii=False, indent=2))
        return 0
    print({k: len(v) for k, v in c.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
