#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""realworld_683_runner.py — 683-A2：真实靶场 RW 样本 × 8 资产判定矩阵生成器。

红线遵守（683 卡）
==================
* 不修改 `tools/holdout_reveal_661.py`（importlib 加载，detect() 一字未动）。
* 不修改 `tools/detect_for_assets.py`（只复用其 `load_rv661` / `decode_safety` /
  `detect_one_asset` / `aggregate`）。
* 不修改任何既有样本；本 runner 只读 `data/real_world/*.cpp`。

口径（与 676g/673r 完全一致，便于真实 vs 自造对比）
===================================================
* 8 资产 = asan / ubsan / tsan / compiler-warn / wunsequenced / cross-compile /
  linker / compile-time；wunsequenced 与 compile-time 在本工具链下恒 unknown。
* 聚合：任一 catch ⇒ catch；全部 unknown ⇒ unknown；否则 miss（unknown 绝不当 miss）。
* sanitizer 在 WSL（g++ 13.3，双档 -O0/-O2）；本地资产在 MinGW g++ 13.1 / clang++ 22.1。
* 并行安全性：sanitizer 三资产**串行**（detect() 写固定 /tmp/rv_bin_O0|O2，并发会互相覆写，
  676g 已论证）；本地四资产逐样本执行（保持简单、可复现；110 样本量级无需并行池）。

用法
====
    python data/realworld_683_runner.py --stage manifest   # 解析样本头部元数据
    python data/realworld_683_runner.py --stage detect     # 全量检测（增量 checkpoint）
    python data/realworld_683_runner.py --stage detect --limit 5   # 冒烟
    python data/realworld_683_runner.py --stage merge      # 合并 → 判定矩阵
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../data
ROOT = HERE.parent                              # 仓库根
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

RW_DIR = HERE / "real_world"
MANIFEST_OUT = HERE / "683_real_world_sample_manifest.json"
MATRIX_OUT = HERE / "683_real_world_detection_matrix.json"
CKPT = HERE / "683_realworld_ckpt_detect.jsonl"

ALL_ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
              "cross-compile", "linker", "compile-time"]
LOCAL_ASSETS = ["compiler-warn", "wunsequenced", "cross-compile", "linker"]

_HEAD_RE = re.compile(r"^//\s*(RW-\d{3})\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*defect_type:\s*(\S+)")


def _log(msg: str) -> None:
    print(f"[683-A2 {_dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_sample(path: Path) -> dict:
    """从 PoC 头注释解析元数据（PoC 文件本身是单一事实源）。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0] if lines else ""
    m = _HEAD_RE.match(head)
    if not m:
        raise ValueError(f"{path.name}: 头部不符合规范: {head[:90]}")
    rw_id, cve, project, defect_type = m.group(1), m.group(2), m.group(3), m.group(4)
    meta: dict = {"rw_id": rw_id, "cve_id": cve, "project": project,
                  "defect_type": defect_type, "file": path.name, "fields": {}}
    for ln in lines[1:40]:
        if not ln.startswith("//"):
            break
        body = ln[2:].strip()
        if ": " in body:
            k, _, v = body.partition(": ")
            meta["fields"][k.strip()] = v.strip()
    return meta


def load_manifest() -> list[dict]:
    files = sorted(RW_DIR.glob("RW-*.cpp"))
    if not files:
        raise SystemExit(f"[683-A2] {RW_DIR} 下没有 RW-*.cpp")
    out = []
    for p in files:
        out.append(parse_sample(p))
    ids = [m["rw_id"] for m in out]
    assert len(ids) == len(set(ids)), "RW id 重复！"
    return out


def stage_manifest() -> int:
    man = load_manifest()
    doc = {"schema": "queyi-683-realworld-manifest/v1",
           "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
           "n_samples": len(man), "assets": ALL_ASSETS, "samples": man}
    MANIFEST_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8", newline="\n")
    _log(f"manifest: {len(man)} 样本 → {MANIFEST_OUT.name}")
    return 0


def stage_detect(limit: int | None = None) -> int:
    import detect_for_assets as dfa

    man = load_manifest()
    if limit:
        man = man[:limit]
    done: dict[str, dict] = {}
    if CKPT.is_file():
        for ln in CKPT.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln:
                row = json.loads(ln)
                done[row["rw_id"]] = row
        _log(f"checkpoint 续跑：已有 {len(done)} 条")

    rv = dfa.load_rv661()
    t0 = time.time()
    with dfa.decode_safety() as env_info:
        _log(f"解码兜底层: L1_effect={env_info.get('L1_effect')}")
        for i, s in enumerate(man, 1):
            if s["rw_id"] in done:
                continue
            spec = dfa.SampleSpec(id=s["rw_id"], dataset="realworld",
                                  dir="data/real_world", files=(s["file"],))
            row = {"rw_id": s["rw_id"], "file": s["file"], "per_asset": {}}
            # sanitizer 串行；本地资产同循环内逐个执行（detect 各自独立 tmpdir）
            for a in ALL_ASSETS:
                out = dfa.detect_one_asset(rv, spec, a, atoms_root=str(RW_DIR))
                row["per_asset"][a] = {"verdict": out["verdict"],
                                       "note": out["note"][:400],
                                       "wall_seconds": out["wall_seconds"]}
            agg = dfa.aggregate(row["per_asset"])
            row["or_verdict"] = agg["verdict"]
            row["caught_by_all"] = agg["caught_by_all"]
            done[s["rw_id"]] = row
            with CKPT.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            el = time.time() - t0
            _log(f"{i}/{len(man)} {s['rw_id']} OR={row['or_verdict']:<7} "
                 f"caught={','.join(agg['caught_by_all']) or '-'}  [{el:.0f}s]")
    _log(f"detect 完成：{len(done)} 条落 checkpoint")
    return 0


def stage_merge() -> int:
    import detect_for_assets as dfa

    man = load_manifest()
    ms = {m["rw_id"]: m for m in man}
    rows = []
    if CKPT.is_file():
        for ln in CKPT.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                rows.append(json.loads(ln))
    rows = [r for r in rows if r["rw_id"] in ms]
    missing = sorted(set(ms) - {r["rw_id"] for r in rows})
    if missing:
        _log(f"警告：{len(missing)} 条缺检测记录：{missing[:8]}（矩阵将不含它们）")

    wall_by_asset: dict[str, float] = {a: 0.0 for a in ALL_ASSETS}
    catch_by_asset = {a: 0 for a in ALL_ASSETS}
    unk_by_asset = {a: 0 for a in ALL_ASSETS}
    samples = []
    for r in sorted(rows, key=lambda x: x["rw_id"]):
        m = ms[r["rw_id"]]
        for a, v in r["per_asset"].items():
            wall_by_asset[a] = wall_by_asset.get(a, 0.0) + float(v.get("wall_seconds", 0))
            if v["verdict"] == "catch":
                catch_by_asset[a] += 1
            elif v["verdict"] == "unknown":
                unk_by_asset[a] += 1
        samples.append({
            "uid": f"realworld:{m['rw_id']}",
            "rw_id": m["rw_id"], "cve_id": m["cve_id"], "project": m["project"],
            "defect_type": m["defect_type"], "fields": m["fields"], "file": m["file"],
            "per_asset": r["per_asset"], "or_verdict": r["or_verdict"],
            "caught_by_all": r.get("caught_by_all", []),
        })

    n = len(samples)
    n_or_catch = sum(1 for s in samples if s["or_verdict"] == "catch")
    n_or_unk = sum(1 for s in samples if s["or_verdict"] == "unknown")
    doc = {
        "schema": "queyi-realworld-matrix/683", "version": "1.0",
        "generated_by": "data/realworld_683_runner.py merge",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detector_owner": "tools/holdout_reveal_661.py::detect（未修改）",
        "wrapper": "tools/detect_for_assets.py（未修改，复用其 load_rv661/decode_safety/detect_one_asset/aggregate）",
        "assets": ALL_ASSETS,
        "asset_availability": {
            "wunsequenced": "本机 MinGW g++ 13.1 不认 -Wunsequenced ⇒ 恒 unknown（673u 判据）",
            "compile-time": "无本地检测器 ⇒ 恒 unknown（检测器池中的声明性资产）",
        },
        "environment": {
            "local_gcc": "MinGW g++ 13.1.0", "local_clang": "clang 22.1.8",
            "wsl_gcc": "WSL g++ 13.3.0", "os": "win32",
        },
        "aggregation": "OR：任一 catch ⇒ catch；全部 unknown ⇒ unknown；否则 miss（unknown 不当 miss）",
        "n_samples": n,
        "n_or_catch": n_or_catch,
        "n_or_unknown": n_or_unk,
        "or_catch_rate_pct": round(n_or_catch / n * 100, 4) if n else None,
        "per_asset_summary": {
            a: {"catch": catch_by_asset[a], "unknown": unk_by_asset[a],
                "miss": n - catch_by_asset[a] - unk_by_asset[a],
                "catch_rate_pct": round(catch_by_asset[a] / n * 100, 4) if n else None,
                "unknown_rate_pct": round(unk_by_asset[a] / n * 100, 4) if n else None}
            for a in ALL_ASSETS},
        "wall_seconds_by_asset": {a: round(v, 2) for a, v in wall_by_asset.items()},
        "missing": missing,
        "samples": samples,
    }
    MATRIX_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8", newline="\n")
    _log(f"矩阵: n={n} OR-catch={n_or_catch} ({doc['or_catch_rate_pct']}%) → {MATRIX_OUT.name}")
    for a in ALL_ASSETS:
        s = doc["per_asset_summary"][a]
        _log(f"  {a:<15} catch={s['catch']:<4} unknown={s['unknown']:<4} miss={s['miss']:<4} "
             f"({s['catch_rate_pct']}%)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("manifest", "detect", "merge"), required=True)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    if a.stage == "manifest":
        return stage_manifest()
    if a.stage == "detect":
        return stage_detect(limit=a.limit)
    return stage_merge()


if __name__ == "__main__":
    sys.exit(main())
