#!/usr/bin/env python3
"""613 任务B3 · CI quality job 全步骤验收（本地复跑 + 记录，不改任何文件）。

逐个复跑 `.github/workflows/ci.yml` 中 **quality job** 的硬门禁步骤
（continue-on-error: false），记录 exit code 与耗时，输出验收报告。

本地跳过（环境依赖，CI 上有）：
  - cross-check matrix（需 clang++ 对照；本地只有 MinGW g++）
  - book_asm_freshness（需 binutils c++filt/objdump；本地 MinGW 可能无）

CLI：
  python tools/quality_gate_613.py              # 跑全部并写 data/quality_gate_acceptance_613.md
  python tools/quality_gate_613.py --only ruff  # 只跑某一步（名见 STEPS）
  python tools/quality_gate_613.py --check      # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"
OUT = ROOT / "data" / "quality_gate_acceptance_613.md"

# (名称, argv, 是否硬门禁)
STEPS: list[tuple[str, list[str], bool]] = [
    ("ruff", ["-m", "ruff", "check", "tools/"], True),
    ("mypy", ["-m", "mypy", "tools/"], True),
    ("gen_metrics --check", ["tools/gen_metrics.py", "--check"], True),
    ("star_h2 --star", ["tools/star_h2_audit.py", "check", "--star"], True),
    ("star_h2 h2-check", ["tools/star_h2_audit.py", "h2-check"], True),
    ("atom_coverage_map", ["tools/atom_coverage_map.py", "--check", "--check-doc"], True),
    ("preflight_check", ["tools/preflight_check.py"], True),
    ("consistency_check", ["tools/consistency_check.py"], True),
    ("data_sanity_audit", ["tools/data_sanity_audit.py", "--fail-on", "ERROR"], True),
    ("crossref_audit", ["tools/crossref_audit.py"], True),
    ("xref_check", ["tools/xref_check.py"], True),
    ("gen_indexes --check", ["tools/gen_indexes.py", "--check"], True),
    ("density_audit", ["tools/density_audit.py", "--check", "20"], True),
    ("d5_appendix_audit", ["tools/d5_appendix_audit.py"], True),
    ("d5_source_integrity", ["tools/d5_source_integrity.py", "--check"], True),
    ("terminology_normalize", ["tools/terminology_normalize.py", "--check"], True),
    ("exercise_dup_guard", ["tools/exercise_dup_guard.py"], True),
    ("verify_asm_evidence", ["tools/verify_asm_evidence.py", "--root", "Book",
                             "--examples", "Examples"], True),
    ("dangling_ref_linter", ["tools/dangling_ref_linter.py", "--json",
                             "outputs/t1_2_dangling.json"], True),
    ("prereq_topo_check", ["tools/prereq_topo_check.py", "--json",
                           "outputs/t1_3_topo.json"], True),
    ("structure_audit", ["tools/structure_audit.py", "--check"], True),
    ("sweep_fences", ["tools/sweep_fences.py", "--check"], True),
    ("whitespace_fix", ["tools/whitespace_fix.py", "--check"], True),
    ("s10_verify_mark", ["tools/s10_verify_mark.py", "--check"], True),
    ("fix_book_links", ["tools/fix_book_links.py", "--check"], True),
    # 软门禁（continue-on-error: true），仅记录
    ("d5_gap_scanner(soft)", ["tools/d5_gap_scanner.py"], False),
    ("mermaid_audit(soft)", ["tools/mermaid_audit.py"], False),
    ("table_style_audit(soft)", ["tools/table_style_audit.py"], False),
]

SKIPPED = [
    ("cross-check matrix", "需 clang++ 对照；本地仅 MinGW g++（CI runner 上有）"),
    ("book_asm_freshness", "需 binutils c++filt/objdump；CI ubuntu runner 自带"),
]

CONTROLLED = ["Examples/atoms/", "atoms/", "evidence/", "tools/golden_state.json"]


def run_step(name: str, argv: list[str], timeout: int = 240) -> dict:
    t0 = time.time()
    try:
        r = subprocess.run([str(PY), *argv], cwd=str(ROOT), capture_output=True,
                           text=True, timeout=timeout, encoding="utf-8", errors="replace")
        dt = time.time() - t0
        tail = (r.stdout + r.stderr).strip().splitlines()
        return {"name": name, "rc": r.returncode, "sec": round(dt, 1),
                "tail": tail[-1] if tail else ""}
    except subprocess.TimeoutExpired:
        return {"name": name, "rc": 124, "sec": timeout, "tail": f"TIMEOUT(>{timeout}s)"}
    except FileNotFoundError:
        return {"name": name, "rc": 127, "sec": 0.0, "tail": "命令/模块不存在"}


def worktree_clean() -> dict:
    t0 = time.time()
    r = subprocess.run(["git", "status", "--porcelain", "--", *CONTROLLED], cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    dirty = r.stdout.strip()
    return {"name": "worktree_cleanliness", "rc": 0 if not dirty else 1,
            "sec": round(time.time() - t0, 1),
            "tail": "干净" if not dirty else dirty.replace("\n", " | ")[:200]}


def render(results: list[dict], clean: dict) -> str:
    hard = [r for r in results if r["rc"] != 0]
    n_ok = sum(1 for r in results if r["rc"] == 0)
    L = ["# 613 · CI quality job 验收（B3）", "",
         f"> 生成：`python tools/quality_gate_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 本地逐个复跑 `.github/workflows/ci.yml` quality job 的门禁步骤并记录 exit code。",
         "> 本工具**只读**（各步骤自身可能写 build/ 等 ignore 产物，不碰受控目录）。", "",
         "## 一、总览", "",
         f"- 步骤数：{len(results)} ｜ 通过：**{n_ok}** ｜ 失败：**{len(hard)}**",
         f"- 受控目录清洁性：{'✅ 干净' if clean['rc'] == 0 else '❌ 不干净'}",
         f"- 本地跳过（环境依赖）：{len(SKIPPED)} 项", ""]
    L += ["## 二、逐步结果", "", "| 步骤 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
    for r in results + [clean]:
        mark = "✅" if r["rc"] == 0 else "❌"
        L.append(f"| `{r['name']}` | {r['rc']} {mark} | {r['sec']} | "
                 f"{(r['tail'] or '').replace('|', '/')[:110]} |")
    L += ["", "## 三、失败明细", ""]
    if hard:
        for r in hard:
            L.append(f"- **`{r['name']}`** exit={r['rc']} ｜ {r['tail'][:200]}")
    else:
        L.append("- 无失败步骤 ✅")
    L += ["", "## 四、本地跳过（CI 上有环境）", ""]
    for n, why in SKIPPED:
        L.append(f"- `{n}`：{why}")
    L += ["", "> 注：`mypy` 若本地未安装会记 127（模块不存在），CI 会自行安装 mypy==2.3.1。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 B3 · quality job 验收")
    ap.add_argument("--only", help="只跑指定步骤名")
    ap.add_argument("--check", action="store_true", help="自验证：STEPS 可构造 + 报告可渲染")
    a = ap.parse_args(argv)

    if a.check:
        assert STEPS and all(s[0] and s[1] for s in STEPS)
        probe = render([{"name": s[0], "rc": 0, "sec": 0.0, "tail": ""} for s in STEPS],
                       {"name": "worktree_cleanliness", "rc": 0, "sec": 0.0, "tail": "干净"})
        assert "CI quality job 验收" in probe
        print("[B3] ✅ 自验证通过")
        return 0

    steps = STEPS if not a.only else [s for s in STEPS if s[0] == a.only]
    if a.only and not steps:
        print(f"[B3] ✗ 未找到步骤 {a.only}")
        return 1

    results = []
    for name, argv_, _hard in steps:
        r = run_step(name, argv_)
        results.append(r)
        print(f"[B3] {'✅' if r['rc'] == 0 else '❌'} {name} exit={r['rc']} ({r['sec']}s)")
    clean = worktree_clean()
    print(f"[B3] {'✅' if clean['rc'] == 0 else '❌'} worktree_cleanliness exit={clean['rc']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(results, clean), encoding="utf-8", newline="\n")
    print(f"[B3] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
