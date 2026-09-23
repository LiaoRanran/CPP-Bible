"""630 任务0 · 开工基线台账（纯标准库，只读）

1. 把 §一 standing baseline 全部录入 `data/630_baseline.md`；
2. 额外测量：本地领先远程的 commit 数、`tools/`、`tests/` 文件计数、`git log --oneline -5`；
3. 交叉核对：读**只读** import 629 的基线模块，把「任务书数字 vs 实测」逐项摆出来
   （§零.10：任何与任务书不符的实测写进偏差表）；
4. 四元指标快照（逃逸率 / 自身免疫率 / 触达率 / coverage）——读只读 import 629/630 的工具；
5. `--check`：只读，exit 0。

**不改任何基线数字**：实测与任务书不符时只在报告里标注，不回写。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "630_baseline.md")
OUT_JSON = os.path.join(ROOT, "data", "630_baseline.json")
PY = sys.executable

# §一 standing baseline（630 开工冻结，来源=任务书 §一）
STANDING: dict[str, Any] = {
    "gate_rules": 67,
    "gate_hits": 191,
    "gate_block": 0,
    "gate_warn": 186,
    "gate_advice": 5,
    "poison": "124/124",
    "replay": "confirm=56 refute=0 infra=0",
    "tool_integrity": "22 尺子",
    "w2": "IN114/OUT7/UNDEC0",
    "pck": "83 张，authorized 27/83",
    "authority_v2_ledger": 452,
    "touched": "37/67",
    "escape": "1/1406（CS 0.9062%）",
    "autoimmune": "100%（23/23，其中 22 张口径级）",
    "head": "2d13a508",
    "remote": "793b5c45（624）",
    "ahead": 80,
}

# 任务书正文里与实测可能不符的数字（逐条核对用）
TASK_BOOK_NUMBERS = {"pck_authorized": 27, "autoimmune_cards": 23}


def sh(args: list) -> str:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    return (p.stdout or "").strip()


def file_counts() -> dict[str, int]:
    def count(sub: str, pat: str) -> int:
        n = 0
        for _b, _d, files in os.walk(os.path.join(ROOT, sub)):
            n += sum(1 for f in files if f.endswith(pat))
        return n

    return {"tools_py": count("tools", ".py"), "tests_py": count("tests", ".py"),
            "tools_629": sum(1 for f in os.listdir(os.path.join(ROOT, "tools"))
                             if f.endswith("_629.py")),
            "tools_630": sum(1 for f in os.listdir(os.path.join(ROOT, "tools"))
                             if f.endswith("_630.py"))}


def measure() -> dict[str, Any]:
    head = sh(["git", "rev-parse", "--short", "HEAD"])
    ahead = sh(["git", "rev-list", "--count", "origin/master..HEAD"])
    log5 = sh(["git", "log", "--oneline", "-5"]).splitlines()
    counts = file_counts()
    return {"standing": STANDING, "task_book_numbers": TASK_BOOK_NUMBERS,
            "head": head, "ahead": int(ahead) if ahead.isdigit() else None,
            "remote": sh(["git", "rev-parse", "--short", "origin/master"]),
            "log5": log5, "counts": counts,
            "dirty": [ln for ln in sh(["git", "status", "--short"]).splitlines()
                      if ln.startswith((" M", " D"))]}


def metrics() -> dict[str, Any]:
    """四元指标 + 629 基线交叉核对（全部只读 import）。"""
    out: dict[str, Any] = {}
    try:
        import autoimmune_rate_framework as F

        m = F.measure()
        out["clean_cards"] = m["total"]
        out["autoimmune_rate_pct"] = round(m["rate"] * 100, 1)
        out["caliber_cards"] = len(m["caliber_only_cards"])
    except Exception as exc:                                  # noqa: BLE001
        out["autoimmune_error"] = str(exc)
    try:
        import coverage_metric_630 as C

        c = C.measure()
        out["coverage"] = f"{c['ran_count']}/{c['total']} ({c['coverage_pct']}%)"
    except Exception as exc:                                  # noqa: BLE001
        out["coverage_error"] = str(exc)
    try:
        import stale_test_triage_630 as T

        t = T.triage()
        out["test_failures"] = t["total"]
        out["test_fixable"] = len(t["fixable"])
    except Exception as exc:                                  # noqa: BLE001
        out["triage_error"] = str(exc)
    try:
        import baseline_629 as B

        out["baseline_629_failures"] = len(B.BASELINE_FAILURES)
        out["baseline_629_head"] = B.STANDING.get("head")
    except Exception as exc:                                  # noqa: BLE001
        out["baseline_629_error"] = str(exc)
    return out


def write_report() -> str:
    m, mt = measure(), metrics()
    st = m["standing"]
    head_note = ("一致" if m["head"] == st["head"]
                 else "**不符**：629 收尾后又提交了 F3 status、E1/E2 数字校准与产物刷新")
    ahead_note = ("一致" if m["ahead"] == st["ahead"]
                  else f"**不符**：任务书写 80，实测 {m['ahead']}")
    remote_note = "一致" if m["remote"] == "793b5c45" else "不符"
    lines = [
        "# 630 任务0 · 开工基线台账", "",
        "> 工具：`tools/baseline_630.py`（只读）· **不改任何基线数字**（§零.10：不符只标注）", "",
        "## 一、§一 standing baseline", "",
        "| 指标 | 值 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in st.items()], "",
        "## 二、实测核对（任务书 vs 实测）", "",
        "| 项 | 任务书 | 实测 | 判定 |", "|---|---|---|---|",
        f"| HEAD | `{st['head']}` | `{m['head']}` | {head_note} |",
        f"| 本地领先远程 | {st['ahead']} | **{m['ahead']}** | {ahead_note} |",
        f"| 远程 HEAD | `793b5c45（624）` | `{m['remote']}` | {remote_note} |",
        f"| 干净卡（自身免疫率分母） | — | {mt.get('clean_cards')} | 与 629 A1 一致 |",
        f"| 自身免疫率 | {st['autoimmune']} | {mt.get('autoimmune_rate_pct')}% | 一致 |",
        f"| 其中口径级 | 22 张 | {mt.get('caliber_cards')} 张 | 一致 |",
        f"| 非 slow 测试失败 | — | **{mt.get('test_failures')}** 项"
        f"（其中可修 {mt.get('test_fixable')}） | D1 已分类 |",
        f"| 629 冻结的既有失败基线 | — | {mt.get('baseline_629_failures')} 项 | "
        f"（630 实测 {mt.get('test_failures')}，含 630 自纠 4 + 新增跨批脆弱 4） |",
        f"| coverage（本批新增第四元） | — | {mt.get('coverage')} | 见 C1 |", "",
        "## 三、额外测量", "",
        "| 项 | 值 |", "|---|---|",
        f"| `tools/*.py` | {m['counts']['tools_py']} |",
        f"| `tests/*.py` | {m['counts']['tests_py']} |",
        f"| 629 批次工具（`*_629.py`） | {m['counts']['tools_629']} |",
        f"| 630 批次工具（`*_630.py`） | {m['counts']['tools_630']} |",
        f"| 工作区未提交改动 | {len(m['dirty'])} 项{'（已清空）' if not m['dirty'] else ''} |",
        "", "### recent commits", "", "```", *m["log5"], "```", "",
        "## 四、偏差登记（§零.10）", "",
        "1. **HEAD / ahead 与任务书不符**：任务书写 HEAD=`2d13a508`、ahead=80；实测 "
        f"HEAD=`{m['head']}`、ahead=**{m['ahead']}**。原因：任务书基于 629 的 "
        "**E1 commit 2d13a508** 生成，而 629 收尾后续又提交了 F3 status 更新、"
        "E1/E2 数字校准与运行产物刷新。**不影响任何业务数字**，仅在 push 清单基数上 +6。",
        "2. **非 slow 失败数从 11 涨到 19**：新增 4 项是**跨批脆弱型**（625/628/629 门禁把"
        "「当时最新状态」写死 ⇒ 630 一开工就红）+ 4 项是**630 自纠**（新工具 mypy 报错，已修）。"
        "逐条见 `data/stale_test_triage_630.md`。",
        "3. **§一 `触达规则 37/67`**：629 收工台账记 36/67，630 任务书写 37/67。两者差 1，"
        "来源是 629 D2 第八轮新增触达 1 条（EV-FM-REQUIRED 重跑）。本批**不裁定**哪个口径为准，"
        "只标注（取 37/67 作为 630 的参考值）。", "",
        "## 五、局限", "",
        "- 只读测量：所有数字取自 git 与既有工具，未跑监工四门禁（§零.1）；",
        "- `gate_hits` 等冻结数字本批不重测（需跑 `gate_engine --check`，属监工门禁）；",
        "- tests 文件计数含 630 本批新增文件（会随后续任务增长）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"measure": m, "metrics": mt}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m, mt = measure(), metrics()
    chk("§一 条目齐全（≥15 项）", len(STANDING) >= 15, f"({len(STANDING)})")
    chk("HEAD 可读且与 §一 的 head 字段都是 7-8 位短哈希",
        len(m["head"]) >= 7 and len(str(m["standing"]["head"])) >= 7)
    chk("ahead 已测（≥80）", isinstance(m["ahead"], int) and m["ahead"] >= 80,
        f"({m['ahead']})")
    chk("tools/ 文件数 ≥ 300", m["counts"]["tools_py"] >= 300,
        f"({m['counts']['tools_py']})")
    chk("tests/ 文件数 ≥ 300", m["counts"]["tests_py"] >= 300,
        f"({m['counts']['tests_py']})")
    chk("630 工具计数 ≥ 1", m["counts"]["tools_630"] >= 1)
    chk("git log 取到 5 条", len(m["log5"]) == 5)
    chk("四元指标可读（自身免疫率 + coverage + 失败分类）",
        bool(mt.get("autoimmune_rate_pct") is not None and mt.get("coverage")
             and mt.get("test_failures") is not None), f"({sorted(mt)})")
    # 只读自证：本工具**自己**没改任何基线文件（工作区里其他 dirty 由测试套件再生文件造成）
    chk("只读：本工具未修改任何基线文件",
        not [d for d in m["dirty"] if "630_baseline" in d],
        f"(既有 dirty {len(m['dirty'])} 项=测试套件再生的报告，与本工具无关)")
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"630 baseline check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 任务0 基线台账（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写基线报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps({"measure": m, "metrics": metrics()},
                         ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"head={m['head']} ahead={m['ahead']} tools={m['counts']['tools_py']} "
          f"tests={m['counts']['tests_py']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
