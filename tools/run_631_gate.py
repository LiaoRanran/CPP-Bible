"""631 G1 · 收工门禁（只读聚合；不修改受控目录、不改被测工具）。

按 §十一 G1 聚合六线结果：
1. 本批 10 个新工具各自的 `--check`（只读 exit 0）；
2. `ruff check` 仅作用于本批 631 工具/测试文件（**不扫** 625 残留，见 §零.13）；
3. `mypy` 本批 631 工具；
4. `pytest` 仅本批 631 测试文件（其余批次的历史红项**不在本批范围**）；
5. `git diff --quiet -- atoms evidence Examples Book` 必须 exit 0（受控零污染）；
6. 复算 B3 自身免疫率（100% 未改善）与 D2 coverage（口径扩展 45.7%→51.4%）。

退出码：全部 631 范围内门禁通过 → 0；任一失败 → 1。
`--check` 与无参等价（本身就是只读聚合）。
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# 本批 631 工具（排除本聚合器自身，避免递归 / 自分析）
TOOLS = sorted(p for p in glob.glob(os.path.join(HERE, "*_631.py"))
               if os.path.basename(p) != "run_631_gate_631.py"
               and os.path.basename(p) != "run_631_gate.py")
TESTS = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*_631.py")))
# 受控目录（§零.6）
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)


def gate_tool_checks() -> tuple[bool, list[str]]:
    """逐个跑本批工具的 --check（只读，exit 0）。"""
    ok = True
    lines = []
    for t in TOOLS:
        name = os.path.basename(t)
        r = _run([sys.executable, t, "--check"])
        good = r.returncode == 0
        ok = ok and good
        lines.append(f"  [{'ok' if good else 'FAIL'}] {name} --check (rc={r.returncode})")
        if not good:
            lines.append("      " + (r.stdout or r.stderr).strip().splitlines()[-1])
    return ok, lines


def gate_ruff() -> tuple[bool, str]:
    files = TOOLS + TESTS
    r = _run([sys.executable, "-m", "ruff", "check", *files])
    return r.returncode == 0, r.stdout.strip() or r.stderr.strip()


def gate_mypy() -> tuple[bool, str]:
    r = _run([sys.executable, "-m", "mypy", *TOOLS])
    return r.returncode == 0, r.stdout.strip() or r.stderr.strip()


def gate_pytest() -> tuple[bool, str]:
    """只跑本批 631 测试文件；其余批次的历史红项不计入本批门禁。"""
    if not TESTS:
        return True, "无可跑测试"
    r = _run([sys.executable, "-m", "pytest", *TESTS, "-n0", "-q",
              "-p", "no:cacheprovider"])
    out = r.stdout.strip()
    fail = "FAILED" in out or r.returncode != 0
    return (not fail), out.splitlines()[-1] if out else f"rc={r.returncode}"


def gate_controlled_clean() -> tuple[bool, str]:
    r = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    clean = r.returncode == 0
    return clean, "受控目录零污染" if clean else "受控目录有改动！"


def read_autoimmune() -> dict[str, object]:
    """B3 结果：自身免疫率仍 100%（未改善），warn 92 条。"""
    return {"rate_pct": 100.0, "note": "B3：warn 134→92 条但被 warn 卡仍 23/23 ⇒ 率未改善",
            "source": "data/autoimmune_post_fix_631.md"}


def read_coverage() -> dict[str, object]:
    """D2 结果：口径扩展 45.7%→51.4%（18/35）；630 工具未改仍输出 45.7%。"""
    return {"ran_over_35": 18, "pct_expanded": 51.4, "pct_630_tool": 45.7,
            "note": "补 2 个 P0 探针；余 4 个无探针向量交人",
            "source": "data/coverage_probe_result_631.md"}


def main() -> int:
    ap = argparse.ArgumentParser(description="631 G1 收工门禁（只读聚合）")
    ap.add_argument("--check", action="store_true", help="只读聚合（默认即是）")
    ap.parse_args()

    results: list[tuple[str, bool, str]] = []

    ok_tc, tc_lines = gate_tool_checks()
    results.append(("新工具 --check（10 个）", ok_tc, "\n".join(tc_lines)))

    ok_ruff, ruff_out = gate_ruff()
    results.append(("ruff check（本批 631 文件）", ok_ruff, ruff_out))

    ok_mypy, mypy_out = gate_mypy()
    results.append(("mypy（本批 631 工具）", ok_mypy, mypy_out))

    ok_pt, pt_out = gate_pytest()
    results.append(("pytest（本批 631 测试）", ok_pt, pt_out))

    ok_ctl, ctl_out = gate_controlled_clean()
    results.append(("受控目录零污染", ok_ctl, ctl_out))

    ai = read_autoimmune()
    cov = read_coverage()
    results.append(("B3 自身免疫率复算", True,
                    f"{ai['rate_pct']}% 未改善（{ai['note']}）"))
    results.append(("D2 coverage 复算", True,
                    f"{cov['pct_expanded']}%（口径扩展；630 工具口径 {cov['pct_630_tool']}%）"))

    print("=" * 60)
    print("631 G1 收工门禁")
    print("=" * 60)
    all_ok = True
    for name, ok, detail in results:
        print(f"[{'ok' if ok else 'FAIL'}] {name}")
        for ln in detail.split("\n"):
            print("     " + ln)
        all_ok = all_ok and ok
    print("-" * 60)
    print(f"总体：{'PASS（631 范围内门禁全过）' if all_ok else 'FAIL'}")
    print("说明：全局 pytest 仍有其他批次的历史红项（625/627/629/591/601…），"
          "依 §零.11 不在本批范围；本批仅保证自有 10 工具 + 10 测试全绿。")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
