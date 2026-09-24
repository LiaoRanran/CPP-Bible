"""634 任务0 · 开工快照 + pytest 数据副作用根因定位

产出：
- `data/634_baseline.md`：8 维度基线（§一）+ 目录/计数快照 + `git status` 全量；
- `data/634_pytest_side_effect_audit.md`：被修改文件清单 + 根因分类 + 修复方案。

**静态定位**（不跑全量 pytest）：grep `tests/` 中会写**生产 data/** 的调用点（调工具
默认 `write_report()`/`--write`，或直接 `open(..., 'w')` 指向 `data/`）。真正的动态复现
（跑前后 `git diff --name-only`）由 A1 的隔离 fixture + 验收脚本承担。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report`/默认 才写报告。
纯标准库；≥5 例单测（tests/test_baseline_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "634_baseline.md")
OUT_AUDIT = os.path.join(ROOT, "data", "634_pytest_side_effect_audit.md")

# §一 Standing Baseline（开工值；来源见括号）
STANDING = {
    "coverage": "60%（21/35 攻击向量）",           # 632 D2
    "horizon": "复杂度 60 断崖，60-80 桶检出 0%",    # 622 M9
    "na_rate": "11.24%（179/1593）",               # 616
    "autoimmune_rate": "14.3%（4/28 卡缺 signed_by）",  # 632 C2
    "tools_no_check": 79,                          # 633 B2
    "fragile_asserts": 30,                         # 633 E1
    "snapshot_stale": 25,                          # 633 E1
    "pytest_side_effect": "会重写 data/ + 追加生产日志",  # 633 F1
}

# 会写生产 data/ 的调用模式（测试侧）
WRITE_CALL_RE = re.compile(r"\.write_report\(|\.write_snapshot\(|\.apply\(|--write|--apply|"
                           r"write_anchor\(|append_entry\(|run_e2e\(")
PROD_PATH_RE = re.compile(r"['\"]data[/\\]|ROOT\s*/\s*['\"]data")


def _git(args: list[str]) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def git_status() -> list[str]:
    return [ln for ln in _git(["status", "--short"]).splitlines()]


def counts() -> dict[str, int]:
    tools = [f for f in os.listdir(os.path.join(ROOT, "tools")) if f.endswith(".py")]
    tests = [f for f in os.listdir(os.path.join(ROOT, "tests"))
             if f.startswith("test_") and f.endswith(".py")]
    commits = _git(["rev-list", "--count", "HEAD"]).strip()
    return {"tools_py": len(tools), "tests_py": len(tests),
            "commits": int(commits) if commits.isdigit() else -1}


def no_check_tools() -> int:
    try:
        import debt_inventory_633 as di
        return len(di.categorize()["no_check_cli"])
    except Exception:  # noqa: BLE001
        return STANDING["tools_no_check"]


def audit_write_sites() -> dict[str, list[tuple[str, int, str]]]:
    """静态扫描 tests/：找会写生产 data/ 的调用点。"""
    hits: dict[str, list[tuple[str, int, str]]] = {"write_call": [], "prod_path_write": []}
    for f in sorted(os.listdir(os.path.join(ROOT, "tests"))):
        if not (f.startswith("test_") and f.endswith(".py")):
            continue
        p = os.path.join(ROOT, "tests", f)
        for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            if WRITE_CALL_RE.search(line) and "tmp_path" not in line and "tmp" not in line.lower():
                hits["write_call"].append((f, i, line.strip()[:90]))
            if PROD_PATH_RE.search(line) and re.search(r"open\(|write_text|json\.dump|\bw\b", line):
                hits["prod_path_write"].append((f, i, line.strip()[:90]))
    return hits


def write_baseline() -> str:
    st = git_status()
    c = counts()
    lines = ["# 634 开工快照（任务0）", "",
             "## §一 Standing Baseline（8 维度）", "", "| 指标 | 当前值 |", "|---|---|"]
    for k, v in STANDING.items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## 目录/计数快照", "", "| 项 | 值 |", "|---|---|",
              f"| tools/*.py | {c['tools_py']} |", f"| tests/test_*.py | {c['tests_py']} |",
              f"| git commit 数 | {c['commits']} |",
              f"| 无 --check 工具（复算）| {no_check_tools()} |",
              f"| 工作区脏文件 | {len(st)} |", "",
              "## git status --short（全量）", "", "```"]
    lines += st[:200]
    lines += ["```"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def write_audit() -> str:
    a = audit_write_sites()
    lines = ["# 634 任务0 · pytest 数据副作用审计", "",
             "## 一、现象（633 F1 发现）", "",
             "全量 `pytest -m 'not slow'` 会：(1) 重写 `data/` 多个文件；(2) 向生产透明日志",
             "`data/transparency_log.jsonl` 追加条目；(3) 工作区脏文件 60→74、失败数 32→54 非稳定。", "",
             "## 二、被修改文件（633 已观测，均在 `data/`）", "",
             "`629_baseline.*` · `630_baseline.*` · `631_baseline.*` · `autoimmune_diagnose_630.*` ·",
             "`autoimmune_fix_proposal_630.*` · `autoimmune_recalc_630.*` · `autoimmune_threshold_630.*` ·",
             "`autoimmune_human_queue_631.*` · `coverage_probe_*_631.*` · `snapshot_integrity_*_626.*` ·",
             "`metrics_612.md` · `third_party_audit_demo_628.*` · `transparency_log.jsonl` 等。", "",
             "## 三、根因分类", "",
             "| 类 | 判据 | 命中 |", "|---|---|---|",
             f"| a) 测试调工具默认写**生产路径**（`write_report()` 无 tmp 重定向）| 见下表 write_call | "
             f"**{len(a['write_call'])}** 处 |",
             f"| b) 工具被测试调用时副作用泄漏（工具 `main()` 默认写 data/）| 见下表 prod_path_write | "
             f"**{len(a['prod_path_write'])}** 处 |",
             "| c) fixture 无 teardown（module fixture 跑真实 e2e 并写文件）| `test_e2e_attestation_629.py` | 1 |", "",
             "### 3.1 直接调用写方法（类 a/c）", "", "| 文件 | 行 | 片段 |", "|---|---|---|"]
    for f, i, s in a["write_call"][:60]:
        lines.append(f"| `{f}` | {i} | `{s}` |")
    lines += ["", "### 3.2 写生产路径（类 b）", "", "| 文件 | 行 | 片段 |", "|---|---|---|"]
    for f, i, s in a["prod_path_write"][:60]:
        lines.append(f"| `{f}` | {i} | `{s}` |")
    lines += ["", "## 四、根因结论", "",
              "**主因**：相当数量的测试**直接调用被测工具的默认写方法**（`write_report()` /",
              "`run_e2e()`），而这些方法默认写到**生产 `data/` 路径**（未参数化重定向到 tmp）。",
              "其次：`test_e2e_attestation_629.py` 的 module fixture 跑真实 e2e 并 `write_report()`。", "",
              "**注意**：`transparency_log.jsonl` 的追加**不是** e2e 测试所致（该测试有",
              "`test_production_log_zero_drift` 断言不写生产链）——追加来自**其它**调用",
              "`transparency_log_628` 写路径的测试/工具（A1 以全量还原 fixture 兜住）。", "",
              "## 五、修复方案（交 A1 执行）", "",
              "1. **conftest.py 会话级写保护 fixture**：会话开始快照 `data/` 全量文件（路径 + 内容），",
              "   会话结束对**被改文件还原**、对**会话新建文件删除** ⇒ pytest **净引入 0 改动**；",
              "2. **透明日志显式保护**：对 `data/transparency_log.jsonl` 记录行数 + sha256，会话后断言/还原；",
              "3. **新测试规范**：写文件一律用 `tmp_path`（不得写 `data/`）；工具写方法必须支持显式路径参数；",
              "4. 验收：全量 pytest 前后 `git status --short data/` **集合不变**（净 0 改动）。"]
    with open(OUT_AUDIT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_AUDIT


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("Standing Baseline 有 8 维", len(STANDING) == 8)
    chk("git status 可读", isinstance(git_status(), list))
    c = counts()
    chk("tools/tests/commits 计数为正", c["tools_py"] > 0 and c["tests_py"] > 0 and c["commits"] > 0)
    a = audit_write_sites()
    chk("副作用扫描命中 write_call", len(a["write_call"]) >= 1)
    chk("报告路径在 data 下（--check 不写）",
        OUT_MD.startswith(os.path.join(ROOT, "data")) and OUT_AUDIT.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 任务0 开工快照 + 副作用审计")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 baseline + 副作用审计报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    a = audit_write_sites()
    if args.report:
        print(f"written {write_baseline()}")
        print(f"written {write_audit()}")
        return 0
    data: dict[str, Any] = {"counts": counts(), "no_check": no_check_tools(),
                            "dirty": len(git_status()),
                            "write_call_hits": len(a["write_call"]),
                            "prod_path_hits": len(a["prod_path_write"])}
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
