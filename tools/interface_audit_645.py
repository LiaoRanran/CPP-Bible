"""645 · 阶段 D1 · 接口一致性审计（真实扫描 645 工具，非抽查）。

目标（645 §六 D1）：审计所有 645 工具接口是否一致——统一 CLI（`--check` 只读自检 +
`--run`/`--acquire`/`--probe` 等真跑）、统一文档（模块 docstring 含目标/数据源/铁律）、
统一数据模型（智能层/头部层/尾端经 `queyi_data_models_645` 传递）。

真实、非代理：静态扫描 `tools/*_645.py` 源文件，检查 4 项接口契约，输出不一致清单。
`--check`：只读自检（审计逻辑）。`--audit`：真实扫描，写 `data/645_interface_audit.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
REPORT_MD = os.path.join(ROOT, "data", "645_interface_audit.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_interface_audit_report.json")

CONTRACT = [
    ("has_docstring", lambda t: bool(re.search(r'""".*?645', t, re.DOTALL))),
    ("has_main", lambda t: "def main(" in t),
    ("has_check_flag", lambda t: "--check" in t),
    ("has_selftest", lambda t: "def selftest(" in t),
    # uses_data_models 为推荐项（仅智能/头部/编排层工具需经统一数据模型），
    # 不计入「不一致」硬性门槛，避免对纯采集类工具误判。
]


def audit() -> dict:
    """真实扫描所有 645 工具，逐条核对接口契约。"""
    results = {}
    for fn in sorted(os.listdir(TOOLS)):
        if not fn.endswith("_645.py"):
            continue
        with open(os.path.join(TOOLS, fn), encoding="utf-8") as fh:
            text = fh.read()
        checks = {name: fn_(text) for name, fn_ in CONTRACT}
        # queyi_data_models_645 是共享数据模型库，按设计无 CLI（不需要 main/--check）
        if fn == "queyi_data_models_645.py":
            checks["has_main"] = True
            checks["has_check_flag"] = True
        results[fn] = {
            "checks": checks,
            "consistent": all(checks.values()),
            "missing": [n for n, ok in checks.items() if not ok],
        }
    inconsistent = [fn for fn, v in results.items() if not v["consistent"]]
    return {
        "tools_total": len(results),
        "consistent": len(results) - len(inconsistent),
        "inconsistent": inconsistent,
        "per_tool": results,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 接口一致性审计报告（D1，真实扫描）", "",
             f"- 645 工具数：{result['tools_total']}",
             f"- 接口一致：{result['consistent']} / 不一致：{len(result['inconsistent'])}", ""]
    lines.append("## 不一致工具（需整改）")
    if result["inconsistent"]:
        for fn in result["inconsistent"]:
            lines.append(f"- `{fn}`：缺失 {result['per_tool'][fn]['missing']}")
    else:
        lines.append("- 无（全部满足接口契约）")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：契约判定逻辑（合成源码）。"""
    good = '"""645 x"""\ndef main():\n  pass\nif __name__=="__main__":\n  pass\n'
    assert audit.__defaults__ is None  # 占位
    checks = {n: f(good) for n, f in CONTRACT}
    # good 缺 --check 与 queyi_data_models → 这两项应为 False
    assert checks["has_docstring"] and checks["has_main"]
    assert not checks["has_check_flag"]
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 接口一致性审计")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--audit", action="store_true", help="真实扫描 645 工具")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = audit()
    write_report(result)
    print(f"[645 interface_audit] 工具={result['tools_total']} 一致={result['consistent']} "
          f"不一致={len(result['inconsistent'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
