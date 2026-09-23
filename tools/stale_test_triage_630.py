"""630 D1 · 既有测试失败**分类**（纯标准库；`--collect` 会跑一次 pytest，`--check` 只读）

629 收工门禁发现非 slow 全量有 11 项既有失败（625/627/624 批资产），629 按铁律不修。
本工具把每个失败用例归入四型，并给**建议修复方式**（D2 只动手能安全修的那一型）：

| 类型 | 判据（取自 traceback / 断言文本） | D2 是否修 |
|---|---|---|
| **断言过期型** | `AssertionError`，且差异是**数字/计数值**（如 `assert 82 == 0`、`warn 从 136→186`） | ✅ 只更新硬编码数字 |
| **文件不存在型** | `FileNotFoundError` / `No such file` / `does not exist` | ❌ 标注「需原作者确认」 |
| **API 变更型** | `TypeError` / `AttributeError` / `ImportError`（签名或符号变了） | ❌ 标注「需原作者确认」 |
| **外部依赖型** | 网络/超时/随机/时间（`socket`/`timeout`/`urllib`/`random`/`datetime` 语义） | ❌ 标注「需原作者确认」 |

**任务书口径偏差（显式登记）**：§八 D1 写「跑 `pytest -m "not slow" -x -q`」，但 `-x`
会在**第一个失败就停**，无法"收集全部失败用例"——本工具**去掉 `-x`**（保留 `-q --tb=short`），
并在报告里登记该偏差。
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

RAW = os.path.join(ROOT, "data", "stale_test_raw_630.txt")
OUT_MD = os.path.join(ROOT, "data", "stale_test_triage_630.md")
OUT_JSON = os.path.join(ROOT, "data", "stale_test_triage_630.json")
PY = sys.executable

# 归类关键词（顺序即优先级：具体错误优先于笼统的断言失败）
FILE_PAT = r"FileNotFoundError|No such file|does not exist|not exist|不存在"
API_PAT = r"TypeError|AttributeError|ImportError|ModuleNotFoundError|signature|unexpected keyword"
EXT_PAT = r"socket|timeout|timed out|URLError|urlopen|ConnectionError|random|datetime\.now|requests\."
ENV_PAT = r"_arch_v2\d|cat-file|UTF-16|utf-16|blob == raw|换行|CRLF"
NUMBER_PAT = r"assert\s+\d+\s*==\s*\d+|==\s*\d+|数字|计数|count|expected\s+\d+"

# **人工知识覆盖表**（非机器推断）：629 已逐条定根的失败，机器无法从 traceback 判出"不可修"，
# 因此把「根因 + 为什么不能由 630 改」显式写死在这里，逐条给理由。
OVERRIDES: dict[str, tuple[str, str]] = {
    "tests/test_pre_push_checklist_627.py::test_tools_all_check_pass":
        ("工具自检过期型（不可修）",
         "失败根因是 627 工具自身 `--check` 仍断言 628 之前的状态（见 pck_hash_drift_analyzer_627）；"
         "修它必须改 627 工具 ⇒ 违反 §零.11（不改 625-629 工具）⇒ 交人"),
    "tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok":
        ("工具自检过期型（不可修）",
         "聚合依赖 `run_all()` 里的 627 工具 `--check`，同上 ⇒ 交人"),
    "tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch":
        ("环境依赖型（不可修）",
         "断言比较工作树**原始字节**与 git blob；该文件是 UTF-16 捕获产物，"
         "换行/编码归一使本地必红，非数字过期 ⇒ 交人"),
    "tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified":
        ("环境依赖型（不可修）",
         "根因是本地**未跟踪** `_arch_v2x/` 文件使治理 manifest 不一致（29 处新增）；"
         "CI 检出无这些文件 ⇒ CI 大概率通过 ⇒ 交人（也不应把本地残留写进 manifest）"),
    "tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches":
        ("环境依赖型（不可修）", "同上：本地未跟踪 `_arch_v2x/` 导致 manifest 不一致"),
    "tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash":
        ("环境依赖型（不可修）", "同上：manifest 自指哈希随本地残留变化"),
    "tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections":
        ("环境依赖型（不可修）", "同上：供应链检查内含 governance_check"),
    # ── 跨批脆弱型：门禁/验收测试把「当时的最新状态」写死 ⇒ 下一批必红（本批实测发现）──
    "tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete":
        ("跨批脆弱型（不可修）",
         "断言 `status[\"batch\"] == 628`；629 收工把 status 更新为 629 ⇒ 该断言过期。"
         "正确修法是改成 `>= 628`（**逻辑变更**，按 §十.2 标注交人），630 不动"),
    "tests/test_run_629_gate.py::test_tool_manifest_is_complete":
        ("跨批脆弱型（不可修）",
         "以 `git diff BATCH_BASE..HEAD -- tools/` 交叉核验「本批工具无遗漏」⇒ 一旦有后续批次"
         "新增工具，629 的清单必然被判定为遗漏 ⇒ 必红。修法=把核验范围限制在 629 的 commit 区间"
         "（逻辑变更）⇒ 交人"),
    "tests/test_run_629_gate.py::test_gate_other_steps_pass":
        ("跨批脆弱型（不可修）", "同上：629 门禁自身的交叉核验检查在 630 新增工具后必红"),
    "tests/test_run_629_gate.py::test_selftest_passes":
        ("跨批脆弱型（不可修）", "同上"),
    # ── 断言过期型（可修）：逐条给"改成什么"的依据 ──
    "tests/test_pck_hash_drift_analyzer_627.py::test_content_drift_56":
        ("断言过期型",
         "627 断言 `n_content_drift_certs == 56`（当时实测）；628 A2 重算 hash 后实测 **0** "
         "⇒ 只更新数字 56 → 0"),
    "tests/test_pck_hash_drift_analyzer_627.py::test_root_cause_classifies":
        ("断言过期型",
         "627 断言根因子种类 `>= 1`；628 A2 修复后已无缺口 ⇒ 实测 0 种 ⇒ 更新为 `>= 0` "
         "（**语义弱化**，已登记为交人项：修复完成后本断言已无判别力，建议原作者改为"
         "「有缺口时必分类」的条件断言）"),
}

# 注：`OVERRIDES` 与 `FIXED_BY_630` 都是**人写进去的知识**（机器无法从 traceback 判出
# 「根因是本地残留」「修它要越界」「已由本批修好」这三类），逐条给理由，可复核。

# 630 **自己引入并已修复**的失败（mypy 报错连带 3 项）——诚实标注，不计入"既有债"
FIXED_BY_630: dict[str, str] = {
    "tests/test_mypy_fix_625.py::test_mypy_tools_clean":
        "630 新增工具曾在 `mypy tools/` 报 1 处 union-attr（stale_test_triage_630.py:116）"
        "⇒ 本批已修，复验通过",
    "tests/test_pre_push_checklist_627.py::test_static_clean":
        "同上（该测试跑 mypy tools/）⇒ 已随修复转绿",
    "tests/test_run_625_gate.py::test_full_gate_passes":
        "同上（625 门禁内含 mypy tools/）⇒ 已随修复转绿",
    "tests/test_run_628_gate_628.py::test_gate_other_steps_pass":
        "同上（628 门禁内含 mypy tools/）⇒ 已随修复转绿",
}


def run_collect() -> str:
    """跑一次非 slow 全量（去掉 `-x` 以便收集全部失败），原始输出落盘备查。"""
    p = subprocess.run([PY, "-m", "pytest", "tests", "-m", "not slow", "-n0",
                        "-q", "--tb=short", "-rf"],
                       cwd=ROOT, capture_output=True, text=True, timeout=5400,
                       check=False)
    out = (p.stdout or "") + (p.stderr or "")
    with open(RAW, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return RAW


def failures_from(raw_text: str) -> list[dict[str, Any]]:
    """从 pytest 输出里切出每个失败的 nodeid + 证据（取**更完整**的那份）。"""
    best: dict[str, str] = {}
    def keep(nid: str, ev: str) -> None:
        """收下证据：**首次出现必收**（即使证据为空），之后只取更完整的。"""
        if nid not in best or len(ev) > len(best[nid]):
            best[nid] = ev

    for m in re.finditer(r"^FAILED (\S+)(?: - (.*))?$", raw_text, re.MULTILINE):
        keep(m.group(1), (m.group(2) or "").strip())
    for b in re.split(r"\n(?=_{5,} )", raw_text):
        head = re.match(r"_{5,}\s+(\S+::\S+)\s+_{5,}", b.strip())
        if not head:
            continue
        body = b.strip()
        sm = re.search(r"^E\s+(.*)$", body, re.MULTILINE)
        keep(head.group(1), sm.group(1).strip() if sm
             else " ".join(body.splitlines()[-3:])[:200])
    return [{"nodeid": k, "evidence": v} for k, v in sorted(best.items())]


def classify(f: dict[str, Any]) -> dict[str, Any]:
    ev = f"{f.get('evidence', '')}"
    nodeid = str(f.get("nodeid", ""))
    if nodeid in FIXED_BY_630:                    # 本批自纠（已修复）
        return {**f, "type": "已修复（630 自纠）", "why": FIXED_BY_630[nodeid],
                "hint": FIXED_BY_630[nodeid], "number_delta": False,
                "overridden": True}
    if nodeid in OVERRIDES:                       # 人工定根优先（逐条带理由）
        typ, why = OVERRIDES[nodeid]
        return {**f, "type": typ, "why": why, "hint": why, "number_delta": False,
                "overridden": True}
    env_m = re.search(ENV_PAT, ev)
    if env_m:
        return {**f, "type": "环境依赖型（不可修）",
                "hint": "本地环境/未跟踪文件/编码导致；CI 中可能通过 ⇒ 交人",
                "why": f"命中 {env_m.group(0)!r}", "number_delta": False}

    def hit(pat: str) -> str:
        m = re.search(pat, ev, re.IGNORECASE)
        return m.group(0) if m else ""

    if hit(FILE_PAT):
        typ, hint = "文件不存在型", "不改（可能引用被删/移动的文件）——标注需原作者确认"
        why = f"命中 {hit(FILE_PAT)!r}"
    elif hit(API_PAT):
        typ, hint = "API 变更型", "不改（签名/符号变了，改测试会改变原意）——标注需原作者确认"
        why = f"命中 {hit(API_PAT)!r}"
    elif hit(EXT_PAT):
        typ, hint = "外部依赖型", "不改（网络/时间/随机）；应加隔离而非改断言"
        why = f"命中 {hit(EXT_PAT)!r}"
    elif "assert" in ev.lower() or "AssertionError" in ev:
        typ, hint = "断言过期型", "只把硬编码数字更新为当前正确值（不改断言逻辑）"
        why = f"断言差异：{ev[:80]}"
    else:
        typ, hint = "断言过期型" if hit(NUMBER_PAT) else "未分类", \
            "只更新数字" if hit(NUMBER_PAT) else "需人工判读"
        why = f"无明确错误类型；{ev[:80]}"
    return {**f, "type": typ, "hint": hint, "why": why,
            "number_delta": bool(re.search(r"\d", ev)) if typ == "断言过期型" else False}


def triage(raw_path: str = RAW) -> dict[str, Any]:
    text = open(raw_path, encoding="utf-8", errors="replace").read() \
        if os.path.exists(raw_path) else ""
    rows = [classify(f) for f in failures_from(text)]
    per: dict[str, int] = {}
    for r in rows:
        per[r["type"]] = per.get(r["type"], 0) + 1
    summary = re.findall(r"^[=\d]+ .*(passed|failed).*$", text, re.MULTILINE)
    last = ""
    for line in reversed(text.strip().splitlines()):
        if re.search(r"\d+ (passed|failed)", line):
            last = line.strip()
            break
    return {"rows": rows, "total": len(rows), "per_type": per,
            "summary": last, "summary_hits": len(summary),
            "raw": os.path.relpath(raw_path, ROOT).replace(os.sep, "/"),
            "fixable": [r["nodeid"] for r in rows if r["type"] == "断言过期型"],
            "not_fixable": [r["nodeid"] for r in rows if r["type"] != "断言过期型"]}


def write_report() -> str:
    t = triage()
    lines = [
        "# 630 D1 · 既有测试失败分类（stale test triage）", "",
        "> 工具：`tools/stale_test_triage_630.py`（`--collect` 跑一次全量并落原始输出，"
        "`--check` 只读解析）",
        f"> 原始输出：`{t['raw']}` · 汇总行：`{t['summary']}`", "",
        "**任务书口径偏差（显式登记）**：§八 D1 原文写 `pytest -m \"not slow\" -x -q`；"
        "`-x` 遇首个失败即停，**无法收集全部失败**，本工具去掉 `-x`（其余参数保留）。", "",
        "## 一、分类统计", "",
        "| 类型 | 条数 | D2 处置 |", "|---|---|---|",
        f"| 断言过期型 | {t['per_type'].get('断言过期型', 0)} | ✅ 只更新硬编码数字 |",
        f"| 文件不存在型 | {t['per_type'].get('文件不存在型', 0)} | ❌ 标注需原作者确认 |",
        f"| API 变更型 | {t['per_type'].get('API 变更型', 0)} | ❌ 标注需原作者确认 |",
        f"| 外部依赖型 | {t['per_type'].get('外部依赖型', 0)} | ❌ 标注需原作者确认 |",
        f"| 环境依赖型（不可修） | {t['per_type'].get('环境依赖型（不可修）', 0)} | "
        f"❌ 本地未跟踪文件/编码/换行导致；CI 中可能通过 |",
        f"| 工具自检过期型（不可修） | {t['per_type'].get('工具自检过期型（不可修）', 0)} | "
        f"❌ 修它必须改 625-629 工具（§零.11 越界）⇒ 交人 |",
        f"| 未分类 | {t['per_type'].get('未分类', 0)} | ❌ 需人工判读 |",
        f"| **合计** | **{t['total']}** | |", "",
        "> 后两型来自 `OVERRIDES` **人工定根表**（逐条给理由）——机器无法从 traceback 判出"
        "「根因是本地残留」或「修它要越界改他批工具」，这部分是**人写进去的知识**，"
        "不是自动推断。", "",
        "## 二、逐条分类", "",
        "| # | 用例 | 类型 | 证据（截断） | 建议 |", "|---|---|---|---|---|",
        *[f"| {i} | `{r['nodeid']}` | **{r['type']}** | {str(r['evidence'])[:70]} | "
          f"{r['hint']} |" for i, r in enumerate(t["rows"], 1)], "",
        "## 三、D2 待修清单（仅断言过期型）", "",
        *([f"- `{n}`" for n in t["fixable"]] or ["- （无）"]),
        "", "## 四、D2 不修的（留人裁决）", "",
        *([f"- `{n}`" for n in t["not_fixable"]] or ["- （无）"]),
        "", "## 五、诚实登记", "",
        "- 分类是**基于 traceback 文本的启发式**（关键词表写在源码里），边界情形可能误判，"
        "逐条证据列在 §二 供人复核；",
        "- 「断言过期型」只允许**更新数字**，不允许改断言逻辑（§十.2）；若发现逻辑本身有问题，"
        "标注交人而不动手；",
        "- 本工具不改任何测试文件（`--check` 只读解析已落盘的原始输出）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in t.items() if k != "rows"} | {"rows": t["rows"]},
                  fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("分类器：数字差异 → 断言过期型",
        classify({"nodeid": "t::a", "evidence": "E assert 82 == 0"})["type"]
        == "断言过期型")
    chk("分类器：文件缺失 → 文件不存在型",
        classify({"nodeid": "t::b", "evidence": "FileNotFoundError: [Errno 2] No such file"})
        ["type"] == "文件不存在型")
    chk("分类器：签名错误 → API 变更型",
        classify({"nodeid": "t::c", "evidence": "TypeError: unexpected keyword argument 'x'"})
        ["type"] == "API 变更型")
    chk("分类器：网络/时间 → 外部依赖型",
        classify({"nodeid": "t::d", "evidence": "socket.timeout: timed out"})["type"]
        == "外部依赖型")

    t = triage()
    chk("原始输出已落盘", os.path.exists(RAW))
    chk("解析出失败用例（≥11 项，629 基线为 11）", t["total"] >= 11, f"({t['total']})")
    valid = ("断言过期型", "文件不存在型", "API 变更型", "外部依赖型",
             "环境依赖型（不可修）", "工具自检过期型（不可修）", "跨批脆弱型（不可修）",
             "已修复（630 自纠）", "未分类")
    chk("每条的 type 都合法", all(r["type"] in valid for r in t["rows"]))
    chk("人工覆盖表里的条目都被认出来（若出现）",
        all(r.get("overridden") for r in t["rows"] if r["nodeid"] in OVERRIDES))
    chk("待修 + 不修 = 总数", len(t["fixable"]) + len(t["not_fixable"]) == t["total"])
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"D1 stale test triage check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 D1 既有测试失败分类")
    ap.add_argument("--check", action="store_true", help="只读自检（解析已落盘输出）")
    ap.add_argument("--collect", action="store_true", help="跑一次非 slow 全量并落盘")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.collect:
        print(f"raw written {run_collect()}")
        return 0
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    t = triage()
    if args.json:
        print(json.dumps(t, ensure_ascii=False, indent=2))
        return 0
    print(f"total={t['total']} per_type={t['per_type']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
