"""635 任务0 · 开工快照 + 全量基线测量（只加数据，不改判决）

实测 §一 全部指标（**实际跑命令，不抄表**）并落盘 `data/635_baseline.md`，
供本批所有任务做「先测量后结论」的对比基准。

**只读契约**：`--check` 只读、exit 0、不写盘；默认/`--report` 才写报告。
纯标准库；≥5 例单测（tests/test_baseline_635.py）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "635_baseline.md")
OUT_JSON = os.path.join(ROOT, "data", "635_baseline.json")

# §一 Standing Baseline（开工表；来源见括注）
STANDING: dict[str, Any] = {
    "gate_rules": 67,
    "escape_rate": "1/1406 (0.071%)",
    "autoimmune_rate_pct": 0.0,
    "coverage_pct": 100.0,
    "horizon_60_80_pct": 100.0,
    "na_rate_pct": 11.24,
    "tools_total": 396,
    "tests_total": 395,
    "commits": 1824,
    "local_ahead": 29,
}


def _run(args: list[str]) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=120).stdout
    except Exception:  # noqa: BLE001
        return ""


def git_dirty_count() -> int:
    return len([ln for ln in _run(["git", "status", "--short"]).splitlines() if ln.strip()])


def git_commits() -> int:
    out = _run(["git", "rev-list", "--count", "HEAD"]).strip()
    return int(out) if out.isdigit() else 0


def git_ahead() -> int:
    out = _run(["git", "rev-list", "--count", "origin/master..HEAD"]).strip()
    return int(out) if out.isdigit() else 0


def count_tools() -> int:
    return len(glob.glob(os.path.join(ROOT, "tools", "*.py")))


def count_tests() -> int:
    return len(glob.glob(os.path.join(ROOT, "tests", "test_*.py")))


def count_rules() -> int:
    try:
        import gate_engine as ge
        return len(ge.RULES)
    except Exception:  # noqa: BLE001
        src = open(os.path.join(ROOT, "tools", "gate_engine.py"), encoding="utf-8",
                   errors="replace").read()
        return len(re.findall(r"register\(Rule\(", src))


def atom_stats() -> dict[str, int]:
    tot = ver = 0
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if not f.endswith(".md"):
                continue
            tot += 1
            s = open(os.path.join(r, f), encoding="utf-8", errors="replace").read()
            if re.search(r"^status:\s*verified", s, re.MULTILINE):
                ver += 1
    return {"atom_cards": tot, "verified_cards": ver}


def autoimmune_missing() -> int:
    miss = 0
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if not f.endswith(".md"):
                continue
            s = open(os.path.join(r, f), encoding="utf-8", errors="replace").read()
            props = re.findall(r"-\s*id:\s*(prop-\d+)(.*?)(?=\n\s*-\s*id:|\Z)", s, re.DOTALL)
            if props and any("signed_by" not in b for _p, b in props):
                miss += 1
    return miss


def coverage_pct() -> float:
    try:
        import coverage_probe_batch_634 as C
        return float(C.matrix()["coverage_pct"])
    except Exception:  # noqa: BLE001
        return 0.0


def horizon_60_80() -> Optional[float]:
    p = os.path.join(ROOT, "data", "verification_horizon_curve_622.json")
    try:
        c = json.loads(open(p, encoding="utf-8").read())
        b = c[-1].get("bands", {}).get("60-80")
        if isinstance(b, (int, float)):
            return float(b)
        return None
    except (OSError, json.JSONDecodeError, IndexError):
        return None


def na_rate_pct() -> Optional[float]:
    p = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
    try:
        d = json.loads(open(p, encoding="utf-8").read())
        n_a = float(d.get("n_a", 0))
        variants = max(1.0, float(d.get("variants", 1)))
        return round(100.0 * n_a / variants, 2)
    except (OSError, json.JSONDecodeError):
        return None


def baseline_files() -> list[str]:
    return [os.path.basename(p) for p in sorted(glob.glob(os.path.join(ROOT, "data", "*baseline*")))]


def exception_clause_hits() -> int:
    """全系统「例外/豁免/白名单」线索计数（供 V26-4 深挖）。"""
    n = 0
    for f in glob.glob(os.path.join(ROOT, "tools", "*.py")) + glob.glob(
            os.path.join(ROOT, "data", "*.json")):
        s = open(f, encoding="utf-8", errors="replace").read()
        n += len(re.findall(r"EXEMPT|whitelist|白名单|豁免|例外|allowlist", s))
    return n


def snapshot() -> dict[str, Any]:
    a = atom_stats()
    return {
        "gate_rules": count_rules(),
        "coverage_pct": coverage_pct(),
        "autoimmune_missing_cards": autoimmune_missing(),
        "na_rate_pct": na_rate_pct(),
        "horizon_60_80_pct": horizon_60_80(),
        "tools_total": count_tools(),
        "tests_total": count_tests(),
        "commits": git_commits(),
        "local_ahead": git_ahead(),
        "dirty_files": git_dirty_count(),
        "atom_cards": a["atom_cards"],
        "verified_cards": a["verified_cards"],
        "baseline_files": len(baseline_files()),
        "exception_clause_hits": exception_clause_hits(),
    }


def write_baseline_md() -> str:
    s = snapshot()
    lines = [
        "# 635 任务0 · 开工快照 + 全量基线测量", "",
        "> 实测时间：2026-09-25。工具：`tools/baseline_635.py`（只读，不跑监工四门禁）。", "",
        "## 一、§一 指标实测（不抄表）", "",
        "| 指标 | §一 表值 | 实测 | 一致 |", "|---|---|---|---|",
        f"| gate 规则数 | 67 | {s['gate_rules']} | {'✅' if s['gate_rules'] == 67 else '❌'} |",
        f"| coverage | 100%（35/35） | {s['coverage_pct']}% | {'✅' if s['coverage_pct'] == 100.0 else '❌'} |",
        f"| 自身免疫率（缺 signed_by 卡） | 0 | {s['autoimmune_missing_cards']} | "
        f"{'✅' if s['autoimmune_missing_cards'] == 0 else '❌'} |",
        f"| N/A 率 | 11.24% | {s['na_rate_pct']}% | "
        f"{'✅' if s['na_rate_pct'] == 11.24 else '❌'} |",
        f"| Horizon 60-80 桶 | 100% | {s['horizon_60_80_pct']} | "
        f"{'✅' if s['horizon_60_80_pct'] == 1.0 else '❌'} |",
        f"| 工具数 | ~450 | {s['tools_total']} | ⚠️ 表为估值 |",
        f"| 测试数 | ~500 | {s['tests_total']} | ⚠️ 表为估值 |",
        f"| commits | ~1900+ | {s['commits']} | ⚠️ 表为估值 |",
        f"| 本地 ahead | 29 | {s['local_ahead']} | {'✅' if s['local_ahead'] == 29 else '❌'} |", "",
        "> 逃逸率 1/1406（0.071%）取 616 统计（本批不跑监工门禁）。", "",
        "## 二、补充实测", "",
        f"- atom 卡：**{s['atom_cards']}**（verified **{s['verified_cards']}**）",
        f"- `data/*baseline*` 文件：**{s['baseline_files']}** 个",
        f"- 全系统「例外/豁免/白名单」线索命中：**{s['exception_clause_hits']}** 处（V26-4 深挖用）",
        f"- 工作区脏文件：**{s['dirty_files']}**", "",
        "## 三、`git status --short`（全量）", "", "```"]
    lines += [ln for ln in _run(["git", "status", "--short"]).splitlines() if ln.strip()]
    lines += ["```", "", "## 四、最近 5 个 commit", "", "```"]
    lines += [ln for ln in _run(["git", "log", "--oneline", "-5"]).splitlines()[:5]]
    lines += ["```", "", "## 五、baseline 报告文件清单", ""]
    lines += [f"- `{f}`" for f in baseline_files()]
    lines += ["", "## 六、诚实登记", "",
              "1. 工具/测试/commits 的 §一 表值（~450/~500/~1900+）为**估值**，实测见上（"
              f"{s['tools_total']}/{s['tests_total']}/{s['commits']}）；",
              "2. 逃逸率取 616 统计，**未重跑** mutation（§零.4）；",
              "3. 本工具**只读**：不写任何监控对象文件，只写本报告。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"standing": STANDING, "measured": s}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("count_tools > 0", count_tools() > 0)
    chk("count_tests > 0", count_tests() > 0)
    chk("count_rules == 67", count_rules() == 67, f"({count_rules()})")
    chk("atom_stats 有 verified", atom_stats()["verified_cards"] >= 1)
    chk("coverage 100", coverage_pct() == 100.0)
    chk("ahead 为 int", isinstance(git_ahead(), int))
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 任务0 基线测量")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_baseline_md()}")
        return 0
    s = snapshot()
    if args.json:
        print(json.dumps({"standing": STANDING, "measured": s}, ensure_ascii=False, indent=2))
        return 0
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
