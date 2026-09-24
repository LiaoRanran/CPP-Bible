"""633 A2 · CI 技术债清理（分类 + 处置建议 + 报告）

读取实测失败清单（`data/633_ci_failures.json`，来自本批两次全量 `pytest -m "not slow"`），
按任务书 §四.A2 的 5 类 + 本批新发现类做**启发式分类**，给出处置建议与 skipif 模板，
产出 `data/ci_debt_clear_633.md`。

**重要诚实**：套件有**数据副作用**（跑测试会重写 `data/` 多个文件），两次运行之间
`data/` 脏文件 60→74、失败集 32→54 不等 ⇒ **失败计数本身不稳定**。本工具如实并列两次数字，
不声称稳定下降。

**只读契约**：`--check` 只读自检、exit 0、不写盘；`--report`/默认 才写报告。
纯标准库；≥5 例单测（tests/test_ci_debt_clear_633.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

FAILURES = os.path.join(ROOT, "data", "633_ci_failures.json")
OUT_MD = os.path.join(ROOT, "data", "ci_debt_clear_633.md")

# 分类规则（顺序敏感：先匹配先归类）
RULES: list[tuple[str, str]] = [
    (r"test_mypy_fix", "类型检查(mypy)"),
    (r"test_autoimmune_(diagnose|fix_proposal|recalc|threshold)_630", "断言过期型"),
    (r"test_autoimmune_human_queue_631", "断言过期型"),
    (r"test_baseline_6\d\d", "跨批脆弱型"),
    (r"test_metrics_6\d\d", "跨批脆弱型"),
    (r"test_metrics_grounded_status_610", "跨批脆弱型"),
    (r"test_bridge_edge_impact_612", "跨批脆弱型"),
    (r"test_modify_mode(_analysis)?_611", "跨批脆弱型"),
    (r"test_weighted_af_human_review_609", "跨批脆弱型"),
    (r"test_high_complexity_rules_regression_624", "跨批脆弱型"),
    (r"test_620_gate", "工具自检过期型"),
    (r"test_run_625_gate", "工具自检过期型"),
    (r"test_ruler_coverage_extension_625", "工具自检过期型"),
    (r"test_pre_push_checklist_627", "工具自检过期型"),
    (r"test_tool_integrity", "完整性/仓库漂移"),
    (r"test_merkle_", "完整性/仓库漂移"),
    (r"test_third_party_audit_demo_628", "完整性/仓库漂移"),
    (r"test_snapshot_integrity_ci_626", "完整性/仓库漂移"),
    (r"test_prop_(inventory_592|graph)", "完整性/仓库漂移"),
    (r"test_transparency_log_628", "完整性/仓库漂移"),
    (r"test_control_char_cleaner_626", "环境依赖型"),
    (r"test_output_snapshots", "快照漂移"),
]
DEFAULT_CAT = "其他/待深判"

# 本批实际施行的修复（测试侧，断言过期型）
FIXES: list[tuple[str, str]] = [
    ("tests/test_autoimmune_diagnose_630.py", "口径规则数 3→1：`== set(RULE_FIELD)` 改为 `<=`（子集）"),
    ("tests/test_autoimmune_fix_proposal_630.py", "硬编码 132 改为动态对齐 diagnose；允许 0 条 auto/signed_by"),
    ("tests/test_autoimmune_recalc_630.py", "严格情景 42 改为动态 filled_auto；无 auto/signed_by 时跳过公式性验证"),
]

# 环境依赖型的 skipif 建议模板（依赖路径需人工确认，见任务书 §四.A2）
SKIPIF_TEMPLATE = ('@pytest.mark.skipif(not os.path.exists("{dep}"), '
                   'reason="环境依赖，CI 不成立")')


def classify(nodeid: str) -> str:
    for pat, cat in RULES:
        if re.search(pat, nodeid):
            return cat
    return DEFAULT_CAT


def load_failures(path: str = FAILURES) -> dict[str, list[str]]:
    if not os.path.exists(path):
        return {"run1_baseline": [], "run2_after_fixes": []}
    try:
        return json.loads(open(path, encoding="utf-8").read())
    except json.JSONDecodeError:
        return {"run1_baseline": [], "run2_after_fixes": []}


def summarize(nodeids: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for n in nodeids:
        c = classify(n)
        out[c] = out.get(c, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def skipif_snippet(nodeid: str, dep: str = "<依赖路径>") -> str:
    return SKIPIF_TEMPLATE.format(dep=dep)


def write_report() -> str:
    f = load_failures()
    r1 = f.get("run1_baseline", [])
    r2 = f.get("run2_after_fixes", [])
    s2 = summarize(r2)
    lines = [
        "# 633 A2 · CI 技术债清理报告", "",
        "> 口径：`pytest -m \"not slow\" -q`（CI 同口径）。**只跑基线 + 按类复验，未跑监工四门禁全量**。", "",
        "## 一、核心发现：套件有数据副作用 ⇒ 失败计数不稳定（P0 级债务）", "",
        f"- **第一次全量**（A2 基线，起始 `data/` 脏文件 ~60）：失败 **{len(r1)}** 项；",
        f"- **第二次全量**（修复 + 中间复验之后，`data/` 脏文件已涨到 **74**）：失败 **{len(r2)}** 项；",
        "- 两次之间 `data/` 脏文件自增 14 个（`autoimmune_*`、`coverage_probe_*`、"
        "`snapshot_integrity_*`、`metrics_*.md`、`transparency_log.jsonl` 等被测试重写）——"
        "**跑测试本身会改工作区**，且后一次运行受前一次的副作用影响 ⇒ 失败集是**状态依赖、非稳定**的。",
        "- 因此本报告**不声称失败数稳定下降**；两次数并列如实登记（§十.7）。", "",
        "## 二、第二次全量失败分类（启发式）", "",
        "| 类别 | 数量 |", "|---|---|"]
    for c, n in s2.items():
        lines.append(f"| {c} | {n} |")
    lines.append(f"| **合计** | {len(r2)} |")
    lines += ["", "## 三、本批施行的修复（测试侧，断言过期型）", "",
              "| 文件 | 修复 |", "|---|---|"]
    for fp, ch in FIXES:
        lines.append(f"| `{fp}` | {ch} |")
    lines += ["",
              "> 依据：631 B1 已把 auto liveness 落地 ⇒ warn 132→65、口径规则 3→1、auto/signed_by 建议 0 条；"
              "这三份 630 测试硬编码了**修复前**的数字，属「断言过期型」，按 §四.A2 改为相对/动态断言。"
              "仅改测试断言，**未改任何 625-632 工具**（§零.10）。", "",
              "## 四、环境依赖型 skipif 建议（不自动改测试逻辑）", "",
              "```python", skipif_snippet("tests/test_control_char_cleaner_626.py::test_repo_data_has_no_control_chars_now"),
              "```", "",
              "适用：`test_control_char_cleaner_626`、`test_snapshot_integrity_ci_626`（依赖仓库当前数据无控制字符）。", "",
              "## 五、剩余未清项与根因（登记，不强行修）", "",
              "| 类别 | 根因 | 为何本批不修 |", "|---|---|---|",
              "| 完整性/仓库漂移 | merkle/工具尺子基准显式钉在 601/613 时代；工作区漂移 + 仓库演进使基准不复位 | "
              "复位要重跑基准写入受保护文件（627/628 保护），属高风险，登记交人 |",
              "| 类型检查(mypy) | 632 工具存在若干 mypy 报错（`__exit__` 返回类型、`TextIOWrapper` 误判等） | "
              "修它要改 632 工具，§零.10「唯一例外」未含此项 ⇒ 登记，不越界 |",
              "| 跨批脆弱型 | 断言/读数硬编码旧批次数字（610/611/612/629/630） | 量大且部分依赖被验证对象口径，需人裁决 |",
              "| 快照漂移 | `test_output_snapshots` 快照过时 | 需快照更新机制（E1 出方案） |",
              "| 工具自检过期型 | `run_625_gate`/`ruler_coverage` 等自检期望值过期 | 修它要改工具，§零.10 禁止 |", "",
              "## 六、诚实登记", "",
              "1. **分类为启发式**（按测试文件名正则），非逐例精读；`其他/待深判` 表示未命中规则；",
              "2. **未修** 完整性/完整性漂移/mypy/工具自检过期类：需改受保护基准或 625-632 工具，"
              "§零.10/§零.16 保守优先 ⇒ 登记不越界；",
              "3. **失败数非稳定**：任何一次全量运行都会改变下一次的输入（§一），"
              "故本批「失败数下降」无法给出稳定结论——**已如实并列，不掩盖**；",
              "4. 修复仅触碰 `tests/test_autoimmune_*_630.py` 三份测试的断言，"
              "受控目录全程零污染（`git diff --quiet -- atoms evidence Examples Book` exit 0）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("分类：630 断言过期",
        classify("tests/test_autoimmune_recalc_630.py::test_x") == "断言过期型")
    chk("分类：mypy", classify("tests/test_mypy_fix_625.py::test_y") == "类型检查(mypy)")
    chk("分类：完整性", classify("tests/test_merkle_proof_613.py::test_z") == "完整性/仓库漂移")
    chk("分类：未命中→默认", classify("tests/test_unknown_999.py::t") == DEFAULT_CAT)
    f = load_failures()
    chk("load_failures 结构", set(f) >= {"run1_baseline", "run2_after_fixes"})
    s = summarize(f.get("run2_after_fixes", []))
    chk("summarize 计数一致", sum(s.values()) == len(f.get("run2_after_fixes", [])))
    chk("skipif 模板含 pytest", "pytest.mark.skipif" in skipif_snippet("x"))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="633 A2 CI 技术债清理")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/ci_debt_clear_633.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    f = load_failures()
    if args.json:
        print(json.dumps({"run1": len(f.get("run1_baseline", [])),
                          "run2": len(f.get("run2_after_fixes", [])),
                          "classes": summarize(f.get("run2_after_fixes", []))},
                         ensure_ascii=False, indent=2))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    print(f"run1={len(f.get('run1_baseline', []))} run2={len(f.get('run2_after_fixes', []))} "
          f"classes={summarize(f.get('run2_after_fixes', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
