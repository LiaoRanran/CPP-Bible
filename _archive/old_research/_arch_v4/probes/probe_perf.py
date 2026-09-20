#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""560 A · 性能画像探针（只读，不改任何正式文件）。

输出 _arch_v4/probes/perf_*.json：
  1) replay：逐卡墙钟（56 卡）+ cProfile 累计归因（编译/运行/重编译/解析/其它）
  2) gate：冷/热两次墙钟（frontmatter 缓存效果）
  3) poison：总墙钟
全部用 .venv（仓库 .venv）；不跑 sanitizer（与日常门禁口径一致）。
"""
from __future__ import annotations

import cProfile
import io
import json
import pstats
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge               # noqa: E402

OUT = HERE / "perf_data"
OUT.mkdir(exist_ok=True)
PY = sys.executable


def section_replay() -> dict:
    cards = replay.find_cards()
    per_card, verdicts = [], {}
    t0 = time.perf_counter()
    pr = cProfile.Profile()
    pr.enable()
    for p in cards:
        c0 = time.perf_counter()
        v, _log = replay.replay_card(p, do_sanitizer=False)
        per_card.append({"card": p.name, "ms": round((time.perf_counter() - c0) * 1000, 1),
                         "verdict": v})
        verdicts[v] = verdicts.get(v, 0) + 1
    pr.disable()
    total = time.perf_counter() - t0
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(35)
    # 按关注函数归因
    want = ["_recompile_invariant", "check_negative_controls", "check_artifact_assert",
            "check_sanitizer", "run_commands", "_wrap_ccache", "parse_frontmatter",
            "card_fingerprint", "_symbol_body", "subprocess.py", "select_incremental"]
    att: dict[str, float] = {}
    for (file, line, name), (cc, nc, tt, ct, callers) in pr.stats.items():
        for w in want:
            if w in name or (w == "subprocess.py" and file.endswith("subprocess.py")):
                att[f"{name} ({Path(file).name}:{line})"] = round(ct, 2)
    (OUT / "replay_profile.txt").write_text(s.getvalue(), encoding="utf-8")
    per_card.sort(key=lambda x: -x["ms"])
    return {"total_s": round(total, 2), "n": len(cards), "verdicts": verdicts,
            "per_card_top10": per_card[:10],
            "per_card_median_ms": round(sorted(x["ms"] for x in per_card)
                                       [len(per_card) // 2], 1),
            "cumulative_attribution_s": att}


def section_gate() -> dict:
    def run() -> tuple[float, dict]:
        t0 = time.perf_counter()
        findings = ge.run_all_checks() if hasattr(ge, "run_all_checks") else None
        dt = time.perf_counter() - t0
        counts = {}
        if findings:
            for f in findings:
                counts[f.severity] = counts.get(f.severity, 0) + 1
        return dt, counts

    # 冷（清缓存若有）/热
    cold, c1 = run()
    warm, c2 = run()
    return {"cold_s": round(cold, 2), "cold_counts": c1,
            "warm_s": round(warm, 2), "warm_counts": c2,
            "rules_registered": len(getattr(ge, "Rule", type) and [1]) or None}


def section_cli(command: list[str], key: str) -> dict:
    t0 = time.perf_counter()
    r = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    dt = time.perf_counter() - t0
    tail = (r.stdout or "").strip().splitlines()[-3:]
    return {"key": key, "wall_s": round(dt, 2), "rc": r.returncode, "tail": tail}


def main() -> int:
    report: dict = {"python": sys.version.split()[0], "at": time.strftime("%Y-%m-%d %H:%M")}

    print("[1/4] replay 56 cards in-process + cProfile ...")
    report["replay"] = section_replay()
    print("  total", report["replay"]["total_s"], "verdicts", report["replay"]["verdicts"])

    print("[2/4] gate cold/warm ...")
    report["gate"] = section_gate()
    print("  ", report["gate"]["cold_s"], "->", report["gate"]["warm_s"])

    print("[3/4] poison_drill subprocess ...")
    report["poison"] = section_cli([PY, "tools/poison_drill.py"], "poison")
    print("  ", report["poison"]["wall_s"])

    print("[4/4] mutation_fuzz --help probe（规模，不跑全量）...")
    mf = section_cli([PY, "tools/mutation_fuzz.py", "--help"], "mutation_help")
    report["mutation_help"] = mf
    (OUT / "perf_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE ->", OUT / "perf_report.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
