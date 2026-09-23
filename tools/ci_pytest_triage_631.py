"""631 A1 · CI pytest 失败用例逐条对齐（纯标准库，只读）

输入：已落盘的原始全量输出 `data/ci_pytest_raw_631.txt`
（`pytest -m "not slow" -n0 -q --tb=line -rf`，631 开工实测）。

对每个失败用例给出：**分类 → 根因 → 修复建议（是否本批可修）**。四类（§五 A1）：

| 分类 | 判定要点 | 本批处置 |
|---|---|---|
| 跨批脆弱型 | 断言了"会随批次变化的数字/状态"（warn 数、ahead 数、commit 数、`git diff BASE..HEAD` 新增集合、`status["batch"]`） | A2 修断言（数字改下界/改单调性/条件跳过） |
| 工具自检过期型 | **工具自身** `--check`/`selftest` 断言了旧状态（测试只是把它跑起来） | A3 修断言；改工具需越界 ⇒ 交人 |
| 环境依赖型 | 依赖本地未跟踪文件（`_arch_v2x/`）或编码差异（UTF-16 vs git blob）⇒ **CI 不成立** | 不修，登记 |
| 真实缺陷型 | 代码真有 bug | 不修，交人（§五 A4.2） |

**诚实边界**：分类里的"根因"部分是**人读断言后的结论**，写进 `REASONS` 逐条可审；
机器只负责解析输出、归类、统计、出报告。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

RAW = os.path.join(ROOT, "data", "ci_pytest_raw_631.txt")
OUT_MD = os.path.join(ROOT, "data", "ci_pytest_triage_631.md")
OUT_JSON = os.path.join(ROOT, "data", "ci_pytest_triage_631.json")

CATEGORIES = ("跨批脆弱型", "工具自检过期型", "环境依赖型", "真实缺陷型")

# 分类规则（nodeid 子串 → 分类）：**人读断言后登记**，逐条可审
PATTERN_RULES: list[tuple[str, str]] = [
    ("test_run_628_gate_628", "跨批脆弱型"),
    ("test_run_629_gate", "跨批脆弱型"),
    ("test_pre_push_630", "跨批脆弱型"),
    ("test_baseline_629", "工具自检过期型"),
    ("test_pre_push_checklist_627", "工具自检过期型"),
    ("test_ci_pytest_fix_625", "环境依赖型"),
    ("test_governance_doc_guard_591", "环境依赖型"),
    ("test_governance_self_hash_601", "环境依赖型"),
    ("test_supply_chain_chain_601", "环境依赖型"),
    ("test_pe_timestamp_caliber_611", "环境依赖型"),
]

# 逐条根因 + 修复建议（人写，机器只搬运）
REASONS: dict[str, dict[str, str]] = {
    "tests/test_baseline_629.py::test_selftest_and_baseline_failure_freeze": {
        "root": "629 工具 `baseline_629.py` 的 selftest 断言『push 前 ahead ≥ 62』；"
                "630 B2 完成 push 后 ahead = 0 ⇒ 工具自检过期",
        "fix": "测试侧：去掉对 `B.selftest()` 的依赖（保留基线计数断言）；"
               "工具侧（需改 629 工具 ⇒ §零.11 越界）交人",
    },
    "tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified": {
        "root": "治理 manifest 判定『29 处新增』源于本地**未跟踪**的 `_arch_v21/` 并行会话产物",
        "fix": "不修（CI 检出无这些文件 ⇒ CI 不成立）",
    },
    "tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches": {
        "root": "同上：`_arch_v2x/` 未跟踪残留使 manifest 比对失败",
        "fix": "不修（环境依赖型）",
    },
    "tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash": {
        "root": "同上：manifest 自哈希随未跟踪文件变化",
        "fix": "不修（环境依赖型）",
    },
    "tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch": {
        "root": "603 字节捕获产物是 UTF-16，测试按 UTF-8 解码 ⇒ "
                "`UnicodeDecodeError: 'utf-16-le' codec can't decode byte`",
        "fix": "不修（编码/环境依赖型；改断言需理解 611 原始意图 ⇒ 交人）",
    },
    "tests/test_pre_push_630.py::test_check_all_ok_and_ahead": {
        "root": "630 B1 的闸门语义是『push 时工作区干净』；但本测试跑在套件里，"
                "而套件总会留下本批未提交的新文件（631 工具/测试）⇒ 聚合 all_ok 在套件内必假",
        "fix": "改断言：不再断言聚合 all_ok，改为断言各分量（受控干净/ci.yml 合法/"
               "交付物齐/630 代码无未提交）",
    },
    "tests/test_pre_push_checklist_627.py::test_tools_all_check_pass": {
        "root": "627 工具 `pck_hash_drift_analyzer_627 --check` 仍断言 628 之前的状态"
                "（实测『无健康证书（全部有缺口）』在 628 A2 修复后已不成立）",
        "fix": "工具自检过期 ⇒ 修它要改 627 工具（§零.11 越界）⇒ 条件跳过 + 交人",
    },
    "tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok": {
        "root": "同上（627 pre-push 清单聚合依赖该工具自检）",
        "fix": "同上：条件跳过 + 交人",
    },
    "tests/test_run_628_gate_628.py::test_gate_other_steps_pass": {
        "root": "628 门禁内的 `v2_flag_integration_verify_628 --check` 断言"
                "『tool_integrity --update 已重钉（628 基准）』；629/630/631 新增工具后该基准过期",
        "fix": "条件跳过 + 交人（修它要改 628 工具的门禁检查）",
    },
    "tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete": {
        "root": "断言 `status['batch'] == 628`；629/630 收工后 status 已推进到 630",
        "fix": "改单调断言：`status['batch'] >= 628` 且 `last_completed_batch >= 628`",
    },
    "tests/test_run_629_gate.py::test_tool_manifest_is_complete": {
        "root": "629 门禁用 `git diff BATCH_BASE..HEAD -- tools/` 核验『本批工具无遗漏』；"
                "630/631 新增工具被判为『遗漏』",
        "fix": "改断言：按批次标记 `*_629.py` 核验（630 门禁已用此修正）",
    },
    "tests/test_run_629_gate.py::test_gate_other_steps_pass": {
        "root": "同上（该核验跑在 629 门禁内部，测试只是把它跑起来）",
        "fix": "条件跳过 + 交人（工具侧改法同上，需改 629 门禁 ⇒ 越界）",
    },
    "tests/test_run_629_gate.py::test_selftest_passes": {
        "root": "同上（629 门禁 selftest 含同一核验）",
        "fix": "条件跳过 + 交人",
    },
    "tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections": {
        "root": "链里含 governance_check，同样被 `_arch_v21/` 未跟踪产物判为『manifest 不一致』",
        "fix": "不修（环境依赖型）",
    },
}


def failures_from(raw_text: str) -> list[dict[str, Any]]:
    """解析 `FAILED <nodeid>` 行 + 紧随的证据行（--tb=line 的 `E ...`）。"""
    out: dict[str, str] = {}
    lines = raw_text.splitlines()
    for i, ln in enumerate(lines):
        if not ln.startswith("FAILED "):
            continue
        parts = ln.split()
        nid = parts[1] if len(parts) > 1 else ""
        if not nid:
            continue
        ev = ""
        for j in range(i + 1, min(i + 4, len(lines))):
            if lines[j].strip().startswith("E "):
                ev = lines[j].strip()[2:].strip()
                break
        if nid not in out or len(ev) > len(out[nid]):
            out[nid] = ev
    return [{"nodeid": k, "evidence": v} for k, v in sorted(out.items())]


def classify(nid: str) -> str:
    for pat, cat in PATTERN_RULES:
        if pat in nid:
            return cat
    return "真实缺陷型"


def triage() -> dict[str, Any]:
    if not os.path.exists(RAW):
        return {"total": 0, "rows": [], "per_category": {},
                "fixable": [], "not_fixable": [], "raw_present": False}
    rows = []
    for f in failures_from(open(RAW, encoding="utf-8", errors="replace").read()):
        nid = f["nodeid"]
        cat = classify(nid)
        why = REASONS.get(nid, {})
        rows.append({"nodeid": nid, "category": cat, "evidence": f["evidence"],
                     "root": why.get("root", "（未登记：需人工读断言后补充）"),
                     "fix": why.get("fix", "（未登记）"),
                     "fixable": cat in ("跨批脆弱型",)})
    per: dict[str, int] = {}
    for r in rows:
        per[r["category"]] = per.get(r["category"], 0) + 1
    return {"total": len(rows), "rows": rows,
            "per_category": {c: per.get(c, 0) for c in CATEGORIES},
            "fixable": [r["nodeid"] for r in rows if r["fixable"]],
            "not_fixable": [r["nodeid"] for r in rows if not r["fixable"]],
            "raw_present": True}


def write_report() -> str:
    t = triage()
    lines = [
        "# 631 A1 · CI pytest 失败用例逐条对齐", "",
        f"> 输入：`data/ci_pytest_raw_631.txt`（631 开工实测）· "
        f"共 **{t['total']}** 项失败", "",
        "## 一、分类统计", "",
        "| 分类 | 项数 | 本批处置 |", "|---|---|---|",
        f"| 跨批脆弱型 | {t['per_category'].get('跨批脆弱型', 0)} | A2 修断言（本批授权） |",
        f"| 工具自检过期型 | {t['per_category'].get('工具自检过期型', 0)} | A3 修断言；改工具越界 ⇒ 交人 |",
        f"| 环境依赖型 | {t['per_category'].get('环境依赖型', 0)} | 不修（CI 不成立） |",
        f"| 真实缺陷型 | {t['per_category'].get('真实缺陷型', 0)} | 不修，交人 |",
        f"| **合计** | **{t['total']}** | |", "",
        "## 二、逐条分类（证据 → 根因 → 修复建议）", "",
    ]
    for cat in CATEGORIES:
        sub = [r for r in t["rows"] if r["category"] == cat]
        if not sub:
            continue
        lines += [f"### {cat}（{len(sub)} 项）", "",
                  "| # | 用例 | 断言证据 | 根因 | 修复建议 |", "|---|---|---|---|---|"]
        for i, r in enumerate(sub, 1):
            ev = (r["evidence"] or "—")[:90].replace("|", "\\|")
            lines.append(f"| {i} | `{r['nodeid']}` | `{ev}` | {r['root']} | {r['fix']} |")
        lines.append("")
    lines += [
        "## 三、与 630 冻结基线的差额", "",
        f"- 630 冻结基线 **12 项** → 631 开工实测 **{t['total']} 项**（+"
        f"{t['total'] - 12}）：",
        "  1. `test_pre_push_630.py::test_check_all_ok_and_ahead`（跨批脆弱型，630 自己引入）；",
        "  2. `test_run_628_gate_628.py::test_gate_other_steps_pass`"
        "（628 门禁的 tool_integrity 重钉基准过期）。",
        "", "## 四、诚实登记", "",
        "1. **分类里的根因是人读断言后的结论**，写进 `REASONS` 逐条可审；"
        "机器只做解析/归类/统计；",
        "2. **环境依赖型在 CI 是否成立无法确证**（无 token ⇒ 未取 CI 日志）："
        "依据是『未跟踪 `_arch_v2x/` 不会进 CI 检出』这一推断；",
        "3. 本批 **A2/A3 只改测试断言**，不改任何 625-630 工具的生产逻辑（§零.11）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(t, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    t = triage()
    chk("原始输出已落盘", t["raw_present"], f"({os.path.basename(RAW)})")
    chk("失败用例 ≥ 12 项（630 冻结基线为 12）", t["total"] >= 12, f"({t['total']})")
    chk("每条都归到四类之一",
        all(r["category"] in CATEGORIES for r in t["rows"]))
    chk("每条都有根因与修复建议",
        all(r["root"] and not r["root"].startswith("（未登记")
            and r["fix"] and not r["fix"].startswith("（未登记") for r in t["rows"]),
        f"({[r['nodeid'] for r in t['rows'] if r['root'].startswith('（未登记')]})")
    chk("分类统计与逐条清单自洽",
        sum(t["per_category"].values()) == t["total"])
    chk("真实缺陷型为 0（630 未发现真 bug）",
        t["per_category"].get("真实缺陷型", 0) == 0)
    chk("可修清单只含跨批脆弱型",
        all(classify(n) == "跨批脆弱型" for n in t["fixable"]))

    def snap() -> str:
        import subprocess

        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    triage()
    chk("只读：triage() 不改变工作区", snap() == before)
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"A1 ci pytest triage check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 A1 CI pytest 失败分类（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写分类报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    t = triage()
    if args.json:
        print(json.dumps(t, ensure_ascii=False, indent=2))
        return 0
    print(f"failures={t['total']} per_category={t['per_category']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
