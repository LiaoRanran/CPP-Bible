#!/usr/bin/env python3
"""412 成本追踪（421）：记录每颗原子的 token 消耗估算，建立 CPVA 基线。

没有测量就没有优化——本工具只记录、只读汇总，不改 gate/replay/poison 任何逻辑。

token 估算口径：tokens_est = chars / 3（中文 ~1.5 字/token、英文 ~4 字/token，混合取 3）。
估算不精确，但**相对值有意义**（不同原子/阶段的成本比例）。

用法：
  python tools/cost_tracker.py record --atom ATOM-MEM-RAII-001 --stage fixture --chars 15000
  python tools/cost_tracker.py report [--atom ATOM-MEM-RAII-001] [--json]
  python tools/cost_tracker.py cpva [--json]
  python tools/cost_tracker.py backfill --all      # 从 git log 回填存量原子（粗估）

数据：data/cost/<atom_id>.json（入库作为历史基线）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v7.0"
COST_DIR = ge.ROOT / "data" / "cost"
STAGES = ("fixture", "evidence_cards", "redteam", "gate_fix", "human_review", "other")


def tokens_est(chars: int) -> int:
    """chars → token 估算（chars/3，见模块 docstring）。"""
    return int(round(chars / 3))


def _atom_file(atom_id: str) -> Path:
    return COST_DIR / f"{atom_id}.json"


def _load(atom_id: str) -> dict[str, Any]:
    f = _atom_file(atom_id)
    if f.is_file():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"atom_id": atom_id, "created_at": _dt.date.today().isoformat(),
            "stages": {}}


def _totals(data: dict[str, Any]) -> dict[str, Any]:
    stages = data.get("stages") or {}
    chars = sum(int(s.get("chars") or 0) for s in stages.values())
    wins = sum(int(s.get("windows") or 0) for s in stages.values())
    mins = sum(int(s.get("duration_min") or 0) for s in stages.values())
    data["total_chars"] = chars
    data["total_tokens_est"] = tokens_est(chars)
    data["total_windows"] = wins
    data["total_duration_min"] = mins
    data["cpva"] = data["total_tokens_est"]
    return data


def record(atom_id: str, stage: str, chars: int, windows: int = 1,
           duration_min: int | None = None) -> dict[str, Any]:
    """记录某原子某阶段的成本（同阶段多次记录取累加，windows 累加）。"""
    if stage not in STAGES:
        raise SystemExit(f"[cost] 未知 stage：{stage}（取值 {STAGES}）")
    data = _load(atom_id)
    st = data["stages"].setdefault(stage, {"chars": 0, "windows": 0})
    st["chars"] += int(chars)
    st["windows"] += int(windows)
    st["tokens_est"] = tokens_est(st["chars"])
    if duration_min is not None:
        st["duration_min"] = int(st.get("duration_min") or 0) + int(duration_min)
    COST_DIR.mkdir(parents=True, exist_ok=True)
    _atom_file(atom_id).write_text(
        json.dumps(_totals(data), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return data


def report(atom_id: str | None = None) -> dict[str, Any]:
    """单原子分阶段报告，或全部原子汇总。"""
    if atom_id:
        f = _atom_file(atom_id)
        if not f.is_file():
            raise SystemExit(f"[cost] 无成本数据：{atom_id}（先 record/backfill）")
        return json.loads(f.read_text(encoding="utf-8"))
    files = sorted(COST_DIR.glob("ATOM-*.json")) if COST_DIR.is_dir() else []
    return {
        "tool": "cost_tracker", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "atoms": len(files),
        "total_tokens_est": sum(
            int(json.loads(f.read_text(encoding="utf-8")).get("total_tokens_est") or 0)
            for f in files),
        "files": [f.name for f in files],
    }


def cpva() -> dict[str, Any]:
    """全局 CPVA：总量/按域/按阶段/趋势（最近 5 颗 vs 最早 5 颗）。"""
    files = sorted(COST_DIR.glob("ATOM-*.json")) if COST_DIR.is_dir() else []
    datas = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    by_domain: dict[str, list[int]] = {}
    by_stage: dict[str, list[int]] = {}
    for d in datas:
        dom = str(d.get("domain") or "unknown")
        by_domain.setdefault(dom, []).append(int(d.get("total_tokens_est") or 0))
        for s, v in (d.get("stages") or {}).items():
            by_stage.setdefault(s, []).append(int(v.get("tokens_est") or 0))
    n = len(datas)
    total = sum(int(d.get("total_tokens_est") or 0) for d in datas)
    ordered = sorted(datas, key=lambda d: str(d.get("created_at") or ""))
    first5 = [int(d.get("total_tokens_est") or 0) for d in ordered[:5]]
    last5 = [int(d.get("total_tokens_est") or 0) for d in ordered[-5:]]
    avg = lambda xs: (sum(xs) / len(xs)) if xs else 0.0
    trend = ("improving" if avg(last5) < avg(first5) * 0.95 else
             "worsening" if avg(last5) > avg(first5) * 1.05 else "stable")
    return {
        "tool": "cost_tracker", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "total_verified_atoms": n,
        "total_tokens_est": total,
        "cpva_overall": (total // n) if n else 0,
        "cpva_by_domain": {k: sum(v) // len(v) for k, v in sorted(by_domain.items())},
        "cpva_by_stage": {k: sum(v) // len(v) for k, v in sorted(by_stage.items())},
        "cpva_first_5": int(avg(first5)), "cpva_recent_5": int(avg(last5)),
        "trend": trend,
    }


def backfill(atom_id: str) -> dict[str, Any]:
    """从 git log 粗估单原子成本：commit 数≈窗口数，改动行数×40≈字符数。

    粗略估算（仅回填基线用）：行→字符按混合密度 40 字/行折算。
    """
    rels: list[str] = []
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        if str(ge._meta(p).get("id") or p.stem) == atom_id:
            rels.append(p.relative_to(ge.ROOT).as_posix())
    if not rels:
        raise SystemExit(f"[cost] 原子不存在：{atom_id}")
    meta = ge._meta(ge.ROOT / rels[0])
    out = {"chars": 0, "commits": 0}
    for rel in rels:
        r = subprocess.run(
            ["git", "log", "--follow", "--numstat", "--format=%h", "--", rel],
            capture_output=True, text=True, cwd=ge.ROOT)
        for ln in r.stdout.split("\n"):
            ln = ln.strip()
            if not ln:
                continue
            parts = ln.split("\t")
            if len(parts) >= 3 and parts[0].isdigit():
                out["chars"] += (int(parts[0]) + int(parts[1])) * 40
            elif len(parts) == 1:
                out["commits"] += 1          # %h 行（numstat 行必含 tab）
    data = _load(atom_id)
    data["domain"] = str(meta.get("domain") or "").lower()
    data["backfill"] = {"method": "git_log_numstat", **out}
    data["stages"]["fixture"] = {
        "chars": out["chars"], "windows": max(out["commits"], 1),
        "tokens_est": tokens_est(out["chars"])}
    COST_DIR.mkdir(parents=True, exist_ok=True)
    _atom_file(atom_id).write_text(
        json.dumps(_totals(data), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return data


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="成本追踪（412：先测量再优化）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--atom", required=True)
    rec.add_argument("--stage", required=True, choices=STAGES)
    rec.add_argument("--chars", type=int, required=True)
    rec.add_argument("--windows", type=int, default=1)
    rec.add_argument("--duration-min", type=int, default=None)
    rep = sub.add_parser("report")
    rep.add_argument("--atom", default=None)
    cp = sub.add_parser("cpva")
    bf = sub.add_parser("backfill")
    bf.add_argument("--all", action="store_true")
    bf.add_argument("--atom", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "record":
        data = record(a.atom, a.stage, a.chars, a.windows, a.duration_min)
        print(json.dumps({"recorded": a.atom, "stage": a.stage,
                          "total_tokens_est": data["total_tokens_est"]},
                         ensure_ascii=False))
    elif a.cmd == "report":
        print(json.dumps(report(a.atom), ensure_ascii=False, indent=1))
    elif a.cmd == "cpva":
        print(json.dumps(cpva(), ensure_ascii=False, indent=1))
    elif a.cmd == "backfill":
        ids = ([str(ge._meta(p).get("id") or p.stem)
                for p in ge._cards(ge.ATOMS, "ATOM-*.md")] if a.all else [a.atom])
        for aid in ids:
            d = backfill(aid)
            print(f"[cost] backfill {aid}: {d['total_tokens_est']} tok est "
                  f"({d['total_windows']} windows)")
    return 0


if __name__ == "__main__":
    main()
