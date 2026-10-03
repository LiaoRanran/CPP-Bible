#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""676f 管线：A5 全量重跑的**数据面**（样本清单 / 判定矩阵生成 / 矩阵装配）。

子命令
======
    python data/676f_pipeline.py manifest
        合并旧 105 样本（holdout 41 + corpus 64）与扩样 expA..expG（1042）→
        data/a5_676f_sample_manifest.json（含去重与确定性派生/评估切分）

    python data/676f_pipeline.py matrix --tag <tag> --assets a,b,c [--limit N]
        对指定资产子集跑**真实** detect()，增量写 data/a5_676f_matrix_<tag>.jsonl
        （断点续跑：已完成的 (sample,asset) 自动跳过）

    python data/676f_pipeline.py matrix --tag verify --verify-old 12 --assets <八项>
        对旧 105 样本做 10% 抽检：重跑全部 8 资产，供与 673r 矩阵比对

    python data/676f_pipeline.py stability --target 60
        并发类样本的 TSan 三连跑（取众数），供稳定性统计

    python data/676f_pipeline.py assemble
        合并全部 JSONL + 673r 旧矩阵 → data/a5_676f_detection_matrix.json

红线
====
* **不改** `tools/holdout_reveal_661.py`（只 import 其 `detect`，经 673r 的
  `tools/detect_for_assets.py` 薄封装调用——那层是既有已测路径）。
* **不改**任何扩样样本、**不改** `research/`、**不改** `tools/`。
* 判定全部来自真实 detect() 调用；unknown 绝不记成 miss。
* 并行安全：sanitizer 资产的 detect() 在 WSL 里用**固定** /tmp/rv_bin_{O0,O2}
  路径 ⇒ 同一时刻只允许**一个**进程跑 sanitizer 资产。本脚本按资产子集分进程，
  `matrix --tag san`(sanitizer) 必须单独串行；`local` 五资产可另进程并行。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re as _re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import detect_for_assets as dfa  # noqa: E402  673r 既有薄封装（未改动）
import verifier_pool_673p as vp  # noqa: E402  资产池（未改动）

SEED_SPLIT = 20261003            # 派生/评估切分种子（固定，可复现）
SEED_RANDOM = 20260930           # 673p/673r 约定种子（Random 臂）
ASSETS = list(vp.selectable_ids(vp.ASSET_POOL))     # 8 项已实测资产
SANITIZER_ASSETS = ("asan", "tsan", "ubsan")        # WSL 固定路径 ⇒ 必须串行

MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
ATTRIB_673R = ROOT / "data" / "experiments" / "asset_attribution_673r.json"
H_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
C_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"

#: 扩样批次规格。`id_key` 是 INDEX 里样本 id 的字段名；`prefix` 用于命名空间化
#: （expA 与 expC 的原始 id 都是 `sample_0xx`，不前缀会撞）。
EXP_BATCHES = (
    dict(key="expA", list_key="index", id_key="id", prefix="A"),
    dict(key="expB", list_key="samples", id_key="sample_id", prefix="B"),
    dict(key="expC", list_key="index", id_key="id", prefix="C"),
    dict(key="expD", list_key="samples", id_key="sample_id", prefix="D"),
    dict(key="expE", list_key="samples", id_key="sample_id", prefix="E"),
    dict(key="expF", list_key="index", id_key="id", prefix="F"),
    dict(key="expG", list_key="samples", id_key="sample_id", prefix="G"),
)

#: 粗粒度缺陷分组（子组分析用；全部公开可核）。
GROUP_MAP = {
    # expA
    "memory_safety": "memory_safety", "out_of_bounds": "memory_safety",
    "null_pointer_deref": "memory_safety", "uninitialized_read": "memory_safety",
    "undefined_behavior": "undefined_behavior",
    # expC
    "move_semantics": "language_semantics", "raii_violation": "language_semantics",
    "virtual_function": "language_semantics", "cross_tu_ub": "odr_link",
    "optimization_dependent": "optimization_sensitive",
    "conditional_trigger": "conditional_trigger",
    # expD
    "iterator_invalidation": "stl", "stl_container_ub": "stl", "string_ub": "stl",
    "algorithm_misuse": "stl", "smart_pointer": "stl", "lambda_capture": "stl",
    # expB / expE（并发）
    "data_race": "concurrency", "memory_order": "concurrency",
    "race_condition": "concurrency", "deadlock": "concurrency",
    "atomicity": "concurrency", "false_sharing": "concurrency",
    "atomic_ub": "concurrency", "aba_problem": "concurrency",
    "lock_priority_inversion": "concurrency", "condition_variable": "concurrency",
    "timing_side_channel": "concurrency",
    # expB 其余
    "integer_overflow": "undefined_behavior", "type_punning": "undefined_behavior",
    "other_ub": "undefined_behavior", "resource_leak": "memory_safety",
    # expF（嵌入式/平台）
    "alignment": "embedded", "endianness": "embedded", "volatile_misuse": "embedded",
    "bit_operation": "embedded", "interrupt_safety": "embedded", "register_ub": "embedded",
}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jload(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _jwrite(p: Path, doc: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")


def _md5_files(base: Path, names: list[str]) -> str:
    h = hashlib.md5()
    for n in sorted(names):
        h.update(n.encode("utf-8"))
        h.update((base / n).read_bytes())
    return h.hexdigest()


def _md5_text(t: str) -> str:
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def _group_of(defect_type: str, batch: str) -> str:
    if defect_type in GROUP_MAP:
        return GROUP_MAP[defect_type]
    if batch in ("expG",):
        return "real_world"
    if batch in ("holdout_5_672h", "corpus_672h"):
        return "legacy"
    return "other"


def epoch_rank(seed: int, sample_id: str) -> str:
    """切分用的确定性排序键（sha256(seed:sample_id)）。"""
    return hashlib.sha256(f"{seed}:{sample_id}".encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# manifest
# ─────────────────────────────────────────────────────────────────────────────
def _files_for_sample(batch_dir: Path, sid: str) -> list[str]:
    """样本 id → 该样本的全部源文件（含头文件）；规则公开、可核。

    expC 的样本有多文件形态：`sample_091.cpp + sample_091_main.cpp + sample_091.h`、
    `sample_099_a.cpp + sample_099_a.h + sample_099_b.cpp + ...`。
    """
    names = []
    for f in sorted(os.listdir(batch_dir)):
        if f.endswith(".json"):
            continue
        stem = os.path.splitext(f)[0]
        if (stem == sid or stem.startswith(sid + "_")
                or stem == "sample_" + sid or stem.startswith("sample_" + sid + "_")):
            names.append(f)
    return names


def build_manifest() -> dict:
    rows: list[dict] = []
    unmatched_files: dict[str, list[str]] = {}

    # 1) 旧 105：holdout（磁盘夹具，planted=true 可测） + corpus（内联 code）
    h_rows = [r for r in _jload(H_DETAIL)["per_sample"]
              if r.get("planted") is True and r.get("verdict") in ("catch", "miss")]
    c_rows = [r for r in _jload(C_DETAIL)["per_sample"]
              if r.get("verdict") in ("catch", "miss")]
    cmap = dfa.corpus_code_map()
    for r in h_rows:
        base = ROOT / str(r.get("dir", ""))
        files = [str(f) for f in (r.get("files") or [])]
        rows.append(dict(
            sample_id=str(r["id"]), orig_id=str(r["id"]), origin="legacy",
            source_batch="holdout_5_672h", dataset="holdout",
            defect_type=f"legacy_{r.get('layer', 'unknown')}",
            defect_group="legacy", planted=bool(r.get("planted")),
            expected_verdict=str(r.get("verdict")), expected_detectors=[str(r.get("detector", ""))],
            severity="", dir=str(r.get("dir", "")), files=files,
            file_path=(Path(str(r.get("dir", ""))) / files[0]).as_posix() if files else "",
            content_md5=_md5_files(base, files) if files else "",
            reusable_from_673r=True))
    for r in c_rows:
        code = cmap.get(str(r["id"]), "")
        rows.append(dict(
            sample_id=str(r["id"]), orig_id=str(r["id"]), origin="legacy",
            source_batch="corpus_672h", dataset="corpus",
            defect_type=f"legacy_{r.get('category') or 'unknown'}",
            defect_group="legacy", planted=True,
            expected_verdict=str(r.get("verdict")), expected_detectors=[str(r.get("detector", ""))],
            severity="", dir="", files=[], file_path="(inline_code)",
            content_md5=_md5_text(code), reusable_from_673r=True))

    # 2) 扩样 expA..expG
    for b in EXP_BATCHES:
        key = b["key"]
        bdir = ROOT / "data" / "holdout_expansion" / key
        index = _jload(bdir / "INDEX.json")
        lst = index[b["list_key"]]
        used: set[str] = set()
        for item in lst:
            sid = str(item[b["id_key"]])
            files = _files_for_sample(bdir, sid)
            if not files:
                raise SystemExit(f"[FAIL] {key}/{sid} 找不到源文件 ⇒ 拒绝继续（fail-loud）")
            used.update(files)
            primary = next((f for f in files
                            if os.path.splitext(f)[0] in (sid, "sample_" + sid)), files[0])
            dt_ = str(item.get("defect_type", ""))
            num = _re.search(r"(\d+)$", sid)
            ns_id = f"{b['prefix']}{num.group(1) if num else sid}"
            rows.append(dict(
                sample_id=ns_id,
                orig_id=sid, origin="expansion", source_batch=key, dataset=key,
                defect_type=dt_, defect_group=_group_of(dt_, key),
                planted=bool(item.get("planted", True)),
                expected_verdict=str(item.get("expected_verdict", "")),
                expected_detectors=[str(x) for x in (
                    item.get("expected_detectors")
                    or ([item["detector"]] if item.get("detector") else []))],
                severity=str(item.get("severity", "")),
                dir=f"data/holdout_expansion/{key}", files=files,
                file_path=f"data/holdout_expansion/{key}/{primary}",
                content_md5=_md5_files(bdir, files),
                reusable_from_673r=False))
        leftover = sorted(f for f in os.listdir(bdir)
                          if not f.endswith(".json") and f not in used)
        if leftover:
            unmatched_files[key] = leftover

    # 3) 去重：先 sample_id，再内容 md5（保留先出现者：legacy → expA..expG）
    by_id: dict[str, dict] = {}
    dup_id: list[dict] = []
    for r in rows:
        if r["sample_id"] in by_id:
            dup_id.append({"sample_id": r["sample_id"], "dropped_of": r["source_batch"]})
        else:
            by_id[r["sample_id"]] = r
    kept = list(by_id.values())
    by_md5: dict[str, dict] = {}
    dup_md5: list[dict] = []
    unique: list[dict] = []
    for r in kept:
        h = r["content_md5"]
        if h and h in by_md5:
            dup_md5.append({"sample_id": r["sample_id"], "duplicate_of": by_md5[h]["sample_id"],
                            "source_batch": r["source_batch"]})
        else:
            if h:
                by_md5[h] = r
            unique.append(r)

    # 4) 确定性切分：按 (source_batch, defect_group) 分层，层内按 hash 排序后交替 D/E
    strata: dict[tuple, list[dict]] = {}
    for r in unique:
        strata.setdefault((r["source_batch"], r["defect_group"]), []).append(r)
    for srows in strata.values():
        srows.sort(key=lambda r: epoch_rank(SEED_SPLIT, r["sample_id"]))
        for i, r in enumerate(srows):
            r["split"] = "derivation" if i % 2 == 0 else "evaluation"

    unique.sort(key=lambda r: (r["origin"] == "expansion", r["source_batch"], r["sample_id"]))

    def _dist(keyfn) -> dict:
        out: dict[str, int] = {}
        for r in unique:
            k = str(keyfn(r))
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))

    doc = {
        "schema": "queyi-a5-676f-sample-manifest/v1",
        "generated_by": "data/676f_pipeline.py manifest",
        "generated_at": _now(),
        "seeds": {"split": SEED_SPLIT, "random_arm": SEED_RANDOM},
        "split_rule": ("按 (source_batch, defect_group) 分层；层内按 sha256('seed:sample_id') 升序，"
                       "偶数位 → derivation，奇数位 → evaluation（确定性，不依赖文件系统次序）"),
        "n_total": len(unique),
        "n_dedup_by_id": len(dup_id),
        "n_dedup_by_content": len(dup_md5),
        "dedup_by_id": dup_id,
        "dedup_by_content": dup_md5,
        "unmatched_source_files": unmatched_files,
        "stats": {
            "by_source_batch": _dist(lambda r: r["source_batch"]),
            "by_split": _dist(lambda r: r["split"]),
            "by_split_x_batch": _dist(lambda r: f"{r['split']}/{r['source_batch']}"),
            "by_defect_group": _dist(lambda r: r["defect_group"]),
            "by_defect_type": _dist(lambda r: r["defect_type"]),
            "by_planted": _dist(lambda r: r["planted"]),
            "by_planted_x_split": _dist(lambda r: f"{r['split']}/planted={r['planted']}"),
        },
        "samples": unique,
    }
    return doc


def cmd_manifest(_a) -> int:
    doc = build_manifest()
    _jwrite(MANIFEST, doc)
    st = doc["stats"]
    print(f"[676f] manifest: n={doc['n_total']} "
          f"(去重 id {doc['n_dedup_by_id']} / 内容 {doc['n_dedup_by_content']})")
    print(f"[676f]   批次分布: {st['by_source_batch']}")
    print(f"[676f]   切分: {st['by_split']}")
    print(f"[676f]   planted: {st['by_planted_x_split']}")
    print(f"[676f]   类型组: {st['by_defect_group']}")
    if doc["unmatched_source_files"]:
        print(f"[676f]   ⚠ 未被任何样本引用的源文件: {doc['unmatched_source_files']}")
    print(f"[676f] 写入 {MANIFEST.relative_to(ROOT).as_posix()}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# matrix
# ─────────────────────────────────────────────────────────────────────────────
def _spec_for(r: dict):
    """manifest 行 → detect_for_assets.SampleSpec（磁盘夹具）。"""
    return dfa.SampleSpec(id=r["sample_id"], dataset=r["source_batch"],
                          dir=r["dir"], files=tuple(r["files"]))


def _legacy_specs() -> dict:
    out = {}
    for ds in ("holdout", "corpus"):
        for sp in dfa.measurable_specs(ds):
            out[sp.id] = sp
    return out


def _worklist(manifest: dict, *, mode: str, verify_old: int = 0,
              limit: int | None = None) -> list[dict]:
    rows = manifest["samples"]
    if mode == "verify":
        legacy = [r for r in rows if r["origin"] == "legacy"]
        step = max(1, len(legacy) // max(1, verify_old))
        picks = legacy[::step][:verify_old]
        return picks
    out = [r for r in rows if r["origin"] == "expansion"]
    # 旧 105 的一个确定性子集也顺带重跑（抽检 10%），其余复用 673r 矩阵
    legacy = [r for r in rows if r["origin"] == "legacy"]
    step = max(1, len(legacy) // 12)
    out += legacy[::step][:12]
    if limit is not None:
        out = out[:limit]
    return out


def _done_keys(out_path: Path) -> set:
    keys = set()
    if not out_path.is_file():
        return keys
    for ln in out_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        try:
            row = json.loads(ln)
        except json.JSONDecodeError:
            continue
        for a in row.get("per_asset", {}):
            keys.add((row["sample_id"], a))
    return keys


#: 运行阶段超时帽（秒）。**只作用于「跑程序」阶段**，编译阶段保持 180s 不变。
#: 理由：扩样-E 的 deadlock 类样本按设计永不返回，detect() 内建 120s/180s 超时会让
#: 每个这样的样本烧掉 ~12min（san）/ ~6min（local），全批不可完成。帽子只把「跑程序」
#: 的等待上限从 120/180s 压到 5/30s；对任何在帽内正常退出的程序**判定不变**，
#: 每次触帽都被记进产物（`timeouts`），不是静默降级。
CAPS = {"wsl_run": 5.0, "local_run": 30.0, "compile": 90.0}

#: 触帽记录（每个样本处理后切片落盘，不跨样本串味）
CAP_LOG: list = []


def install_timeout_caps(rv, log: list, caps: dict) -> dict:
    """给 661 的 `_wsl` / `_local` 装「运行阶段超时帽」。不修改任何文件。"""
    o_wsl, o_local = rv._wsl, rv._local

    def _wsl_is_run(cmd: str) -> bool:
        return not str(cmd).lstrip().startswith("g++")

    def wsl_cap(cmd, timeout=180):
        t = min(timeout, caps["wsl_run"] if _wsl_is_run(cmd) else caps["compile"])
        t0 = time.perf_counter()
        rc, out = o_wsl(cmd, timeout=t)
        dt = time.perf_counter() - t0
        if isinstance(out, str) and "timed out after" in out:
            log.append({"phase": "wsl_run" if _wsl_is_run(cmd) else "wsl_compile",
                        "cap_s": t, "wall_s": round(dt, 2)})
        return rc, out

    def _local_is_run(cmd) -> bool:
        return isinstance(cmd, (list, tuple)) and len(cmd) == 1

    def local_cap(cmd, timeout=180):
        t = min(timeout, caps["local_run"] if _local_is_run(cmd) else caps["compile"])
        t0 = time.perf_counter()
        rc, out = o_local(cmd, timeout=t)
        dt = time.perf_counter() - t0
        if isinstance(out, str) and "timed out after" in out:
            log.append({"phase": "local_run" if _local_is_run(cmd) else "local_compile",
                        "cap_s": t, "wall_s": round(dt, 2)})
        return rc, out

    rv._wsl, rv._local = wsl_cap, local_cap
    return {"wsl_run_cap_s": caps["wsl_run"], "local_run_cap_s": caps["local_run"],
            "compile_cap_s": caps["compile"],
            "note": "仅运行阶段封顶；每次触帽都记录在样本行的 timeouts 字段"}


def cmd_matrix(a) -> int:
    assets = [x.strip() for x in a.assets.split(",") if x.strip()]
    bad = [x for x in assets if x not in ASSETS]
    if bad:
        raise SystemExit(f"[FAIL] 未知资产 {bad}；可选 {ASSETS}")
    if set(assets) & set(SANITIZER_ASSETS) and len(assets) > 3:
        raise SystemExit("[FAIL] sanitizer 资产与其它资产混在一个进程里跑会拉长关键路径；"
                         "请分进程（--tag san / --tag local）")
    out_path = ROOT / "data" / f"a5_676f_matrix_{a.tag}.jsonl"
    manifest = _jload(MANIFEST)
    mode = "verify" if a.verify_old else "normal"
    work = _worklist(manifest, mode=mode, verify_old=a.verify_old, limit=a.limit)
    if a.shard:
        i, n_ = (int(x) for x in a.shard.split("/"))
        work = work[i - 1::n_]
    if a.redo_window:
        allow: set[str] = set()
        for w in a.redo_window:
            tag, start, end = w.split("|")
            src = ROOT / "data" / f"a5_676f_matrix_{tag}.jsonl"
            for ln in src.read_text(encoding="utf-8").splitlines():
                if not ln.strip():
                    continue
                row = json.loads(ln)
                if start <= row.get("at", "") <= end:
                    allow.add(row["sample_id"])
        print(f"[676f] redo-window {a.redo_window} → {len(allow)} 个样本", flush=True)
        work = [r for r in work if r["sample_id"] in allow]
    if a.only_ids_file:
        ids = {ln.strip() for ln in (ROOT / "data" / a.only_ids_file).read_text(
            encoding="utf-8").splitlines() if ln.strip()}
        work = [r for r in work if r["sample_id"] in ids]
        print(f"[676f] only-ids-file {a.only_ids_file} → {len(work)} 个样本", flush=True)
    if a.redo_step > 1:
        work = work[::a.redo_step]
        print(f"[676f] redo-step={a.redo_step} → 抽 {len(work)} 个样本", flush=True)
    legacy_specs = _legacy_specs() if any(r["origin"] == "legacy" for r in work) else {}
    done = set()
    for src in ([out_path] + [ROOT / "data" / s for s in a.skip_done_from]):
        done |= _done_keys(Path(src))

    todo = [(r, asset) for r in work for asset in assets
            if (r["sample_id"], asset) not in done]
    print(f"[676f] tag={a.tag} assets={assets} 样本 {len(work)} 个；"
          f"待跑 {len(todo)} 次 detect（已完成 {len(done)} 次）", flush=True)
    if not todo:
        return 0

    rv = dfa.load_rv661()
    caps = dict(CAPS)
    for kv in (a.caps or []):
        k, _, v = kv.partition("=")
        caps[k] = float(v)
    cap_info = install_timeout_caps(rv, CAP_LOG, caps)
    hash_src = hashlib.sha256((ROOT / "tools" / "holdout_reveal_661.py").read_bytes()).hexdigest()[:16]
    t_all = time.perf_counter()
    n = 0
    with dfa.decode_safety() as env_info:
        print(f"[676f] 解码适配层 L1 生效={env_info.get('L1_effect')}；超时帽 {cap_info}", flush=True)
        with out_path.open("a", encoding="utf-8", newline="\n") as fh:
            for r in work:
                missing = [x for x in assets if (r["sample_id"], x) not in done]
                if not missing:
                    continue
                spec = legacy_specs.get(r["sample_id"]) or _spec_for(r)
                per_asset: dict[str, dict] = {}
                t0 = time.perf_counter()
                mark = len(CAP_LOG)
                try:
                    out = dfa.detect_for_assets(spec, missing, rv=rv, pool_ids=ASSETS)
                    per_asset = {k: {"verdict": v["verdict"], "note": v["note"][:200],
                                     "wall_seconds": v["wall_seconds"]}
                                 for k, v in out["per_asset"].items()}
                except Exception as e:  # noqa: BLE001
                    for x in missing:
                        per_asset[x] = {"verdict": "error",
                                        "note": f"{type(e).__name__}: {e}"[:200],
                                        "wall_seconds": None}
                row = {"sample_id": r["sample_id"], "source_batch": r["source_batch"],
                       "split": r.get("split"), "origin": r["origin"],
                       "dataset": r["dataset"], "detector_hash": hash_src,
                       "wall_seconds": round(time.perf_counter() - t0, 4),
                       "timeouts": CAP_LOG[mark:], "n_timeouts": len(CAP_LOG) - mark,
                       "caps": {k: v for k, v in cap_info.items() if k.endswith("_s")},
                       "at": _now(), "per_asset": per_asset}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
                if n % 5 == 0 or n == len(work):
                    el = time.perf_counter() - t_all
                    print(f"[676f] {a.tag} 样本 {n}/{len(work)} | {el:.0f}s "
                          f"| {r['sample_id']} {sorted(per_asset)}"
                          f" | 触帽 {row['n_timeouts']}", flush=True)
    print(f"[676f] tag={a.tag} 完成 {n} 个样本，墙钟 {time.perf_counter() - t_all:.1f}s "
          f"→ {out_path.relative_to(ROOT).as_posix()}", flush=True)
    return 0


def cmd_stability(a) -> int:
    """并发类样本 × TSan 三连跑（取众数用）。"""
    manifest = _jload(MANIFEST)
    conc_types = {"data_race", "memory_order", "race_condition", "deadlock",
                  "atomicity", "false_sharing", "timing_side_channel"}
    cand = [r for r in manifest["samples"]
            if r["defect_type"] in conc_types and r["origin"] == "expansion"]
    cand.sort(key=lambda r: r["sample_id"])
    step = max(1, len(cand) // max(1, a.target))
    picks = cand[::step][:a.target]
    out_path = ROOT / "data" / "a5_676f_matrix_stability.jsonl"
    asset = a.asset
    print(f"[676f] 稳定性抽检：{len(picks)} 个并发类样本 × {asset} × {a.rounds} 轮", flush=True)
    rv = dfa.load_rv661()
    cap_info = install_timeout_caps(rv, CAP_LOG, dict(CAPS))
    print(f"[676f] 超时帽 {cap_info['wsl_run_cap_s']}s（与矩阵生成同口径）", flush=True)
    t_all = time.perf_counter()
    with dfa.decode_safety():
        with out_path.open("a", encoding="utf-8", newline="\n") as fh:
            for i, r in enumerate(picks, 1):
                spec = _spec_for(r)
                votes = []
                for _ in range(a.rounds):
                    out = dfa.detect_for_assets(spec, [asset], rv=rv, pool_ids=ASSETS)
                    votes.append(out["per_asset"][asset]["verdict"])
                row = {"sample_id": r["sample_id"], "asset": asset, "votes": votes,
                       "at": _now()}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"[676f] stab {i}/{len(picks)} {r['sample_id']} votes={votes}", flush=True)
    print(f"[676f] 稳定性抽检完成 {len(picks)} 个，墙钟 {time.perf_counter() - t_all:.1f}s "
          f"→ {out_path.relative_to(ROOT).as_posix()}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# assemble
# ─────────────────────────────────────────────────────────────────────────────
def cmd_assemble(_a) -> int:
    manifest = _jload(MANIFEST)
    old = _jload(ATTRIB_673R)
    old_index: dict[str, dict[str, str]] = {}
    for ds in ("holdout", "corpus"):
        for r in old["datasets"][ds]["samples"]:
            old_index[str(r["id"])] = {a: v["verdict"] for a, v in r["per_asset"].items()}

    fresh: dict[str, dict] = {}
    walls: dict[str, float] = {a: 0.0 for a in ASSETS}
    used_files: list[str] = []
    # 按 mtime 升序读取：**最新一次测量胜出**（重测/补测会覆盖早期单元格）
    for p in sorted((ROOT / "data").glob("a5_676f_matrix_*.jsonl"),
                    key=lambda q: q.stat().st_mtime):
        if p.name.endswith("_stability.jsonl"):
            continue
        used_files.append(p.name)
        for ln in p.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            row = json.loads(ln)
            cell = fresh.setdefault(row["sample_id"], {"per_asset": {}, "sources": []})
            cell["sources"].append(p.name)
            for a, v in row["per_asset"].items():
                cell["per_asset"][a] = {**v, "from": p.name}
                if v.get("wall_seconds"):
                    walls[a] = walls.get(a, 0.0) + float(v["wall_seconds"])

    records: list[dict] = []
    missing_cells: list[dict] = []
    reused = 0
    fresh_n = 0
    for r in manifest["samples"]:
        sid = r["sample_id"]
        cell = fresh.get(sid)
        per: dict[str, dict] = {}
        if cell:
            per = dict(cell["per_asset"])
            fresh_n += 1
        if r["reusable_from_673r"] or not cell:
            for a in ASSETS:
                if a not in per and a in old_index.get(sid, {}):
                    per[a] = {"verdict": old_index[sid][a], "note": "(reused from 673r matrix)",
                              "wall_seconds": None, "from": "asset_attribution_673r.json"}
            if sid in old_index:
                reused += 1
        lack = [a for a in ASSETS if a not in per]
        if lack:
            missing_cells.append({"sample_id": sid, "missing": lack})
        verdicts = {a: per.get(a, {}).get("verdict", "MISSING") for a in ASSETS}
        caught = sorted(a for a in ASSETS if verdicts[a] == "catch")
        if caught:
            or_v = "catch"
        elif all(verdicts[a] == "unknown" for a in ASSETS):
            or_v = "unknown"
        else:
            or_v = "miss"
        records.append({"sample_id": sid, "orig_id": r["orig_id"],
                        "source_batch": r["source_batch"], "dataset": r["dataset"],
                        "origin": r["origin"], "split": r["split"],
                        "defect_type": r["defect_type"], "defect_group": r["defect_group"],
                        "planted": r["planted"], "expected_verdict": r["expected_verdict"],
                        "file_path": r["file_path"],
                        "per_asset": verdicts, "or_verdict": or_v, "caught_by_all": caught,
                        "source_of_record": ("fresh" if cell else "673r_reuse")})

    from collections import Counter
    def _dist(keyfn) -> dict:
        c = Counter(keyfn(x) for x in records)
        return dict(sorted((str(k), v) for k, v in c.items()))

    per_asset_dist = {a: _dist(lambda x, a=a: x["per_asset"][a]) for a in ASSETS}
    n = len(records)
    unknown_ratio = {a: round(sum(1 for x in records if x["per_asset"][a] == "unknown") / n, 4)
                     for a in ASSETS}

    stab_path = ROOT / "data" / "a5_676f_matrix_stability.jsonl"
    stability: dict = {"status": "skip"}
    if stab_path.is_file():
        rows = [json.loads(ln) for ln in stab_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        agree = sum(1 for r in rows if len(set(r["votes"])) == 1)
        flips = [r["sample_id"] for r in rows if len(set(r["votes"])) > 1]
        modes = {}
        for r in rows:
            if r["sample_id"] in fresh:
                mv = fresh[r["sample_id"]]["per_asset"].get(r["asset"], {}).get("verdict")
                modes[r["sample_id"]] = {"votes": r["votes"],
                                         "mode": Counter(r["votes"]).most_common(1)[0][0],
                                         "matrix": mv, "matches_mode": mv == Counter(r["votes"]).most_common(1)[0][0]}
        stability = {"status": "ok", "n_samples": len(rows), "rounds": len(rows[0]["votes"]) if rows else 0,
                     "all_rounds_identical": agree, "identical_pct": round(agree / len(rows) * 100, 2) if rows else None,
                     "flip_samples": flips, "per_sample": modes}

    # 旧样本抽检对比（fresh vs 673r）
    verify_rows = [x for x in records if x["origin"] == "legacy" and x["source_of_record"] == "fresh"]
    verify = {"n_samples": len(verify_rows), "n_cells": 0, "agree": 0, "diffs": []}
    for x in verify_rows:
        for a in ASSETS:
            got = x["per_asset"][a]
            want = old_index.get(x["sample_id"], {}).get(a)
            verify["n_cells"] += 1
            if got == want:
                verify["agree"] += 1
            else:
                verify["diffs"].append({"sample_id": x["sample_id"], "asset": a,
                                        "frozen_673r": want, "this_run": got})
    if verify["n_cells"]:
        verify["agree_pct"] = round(verify["agree"] / verify["n_cells"] * 100, 2)

    doc = {
        "schema": "queyi-a5-676f-detection-matrix/v1",
        "generated_by": "data/676f_pipeline.py assemble",
        "generated_at": _now(),
        "detector_owner": "tools/holdout_reveal_661.py::detect（未修改；673u 修复后的版本）",
        "detector_sha256_16": hashlib.sha256(
            (ROOT / "tools" / "holdout_reveal_661.py").read_bytes()).hexdigest()[:16],
        "execution_model": "real_per_asset_detect（每样本 × 每资产各一次真实 detect）",
        "rounds": 1,
        "aggregation": "OR：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（unknown 不当 miss）",
        "assets": ASSETS,
        "n_samples": n,
        "n_fresh": fresh_n,
        "n_reused_673r": reused,
        "coverage": {"n_missing_cells": len(missing_cells), "missing": missing_cells[:50]},
        "per_asset_distribution": per_asset_dist,
        "unknown_ratio": unknown_ratio,
        "or_verdict_distribution": _dist(lambda x: x["or_verdict"]),
        "or_by_split": _dist(lambda x: f"{x['split']}/{x['or_verdict']}"),
        "wall_seconds_by_asset": {k: round(v, 2) for k, v in sorted(walls.items())},
        "stability_concurrency": stability,
        "verify_old_vs_673r": verify,
        "inputs": used_files,
        "reuse_note": ("旧 105 样本（holdout 41 + corpus 64）复用 data/experiments/asset_attribution_673r.json"
                       "（post-673u 重跑版）；其余为本次真实 detect 调用。抽检子集为本次现场重跑。"),
        "samples": records,
    }
    _jwrite(MATRIX, doc)
    print(f"[676f] 矩阵 n={n}（fresh {fresh_n} / 复用 673r {reused}）"
          f" 缺格 {len(missing_cells)} 例")
    print(f"[676f]   OR 分布: {doc['or_verdict_distribution']}")
    print(f"[676f]   逐资产: { {a: {k: v for k, v in per_asset_dist[a].items()} for a in ASSETS} }")
    print(f"[676f]   unknown 比例: {unknown_ratio}")
    print(f"[676f]   抽检(本次重跑 vs 673r): {verify.get('agree')}/{verify.get('n_cells')}"
          f" = {verify.get('agree_pct')}%；差异 {len(verify['diffs'])} 例")
    print(f"[676f] 写入 {MATRIX.relative_to(ROOT).as_posix()}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="676f: A5 全量重跑数据面")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("manifest").set_defaults(fn=cmd_manifest)

    m = sub.add_parser("matrix")
    m.add_argument("--tag", required=True)
    m.add_argument("--assets", required=True)
    m.add_argument("--limit", type=int, default=None)
    m.add_argument("--verify-old", type=int, default=0)
    m.add_argument("--shard", default=None, help="i/n：只跑工作清单的第 i 片（跨步切片）")
    m.add_argument("--skip-done-from", action="append", default=[],
                   help="额外的已完成 JSONL（相对 data/）")
    m.add_argument("--redo-window", action="append", default=[],
                   help="TAG|START|END：只重跑该 tag 文件里 at 落在窗口内的样本（污染窗口重测）")
    m.add_argument("--redo-step", type=int, default=1, help="在 redo-window 结果里再抽 1/N")
    m.add_argument("--only-ids-file", default=None, help="data/ 下的样本 id 清单（每行一个）")
    m.add_argument("--caps", action="append", default=None,
                   help="超时帽覆盖，如 --caps wsl_run=5")
    m.add_argument("--resume", action="store_true", default=True)
    m.set_defaults(fn=cmd_matrix)

    s = sub.add_parser("stability")
    s.add_argument("--asset", default="tsan")
    s.add_argument("--target", type=int, default=60)
    s.add_argument("--rounds", type=int, default=3)
    s.set_defaults(fn=cmd_stability)

    sub.add_parser("assemble").set_defaults(fn=cmd_assemble)

    a = ap.parse_args(argv)
    print(f"[676f] cmd={a.cmd} at {_now()}", flush=True)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
