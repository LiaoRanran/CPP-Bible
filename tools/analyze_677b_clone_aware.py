#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""analyze_677b_clone_aware.py — 677b：clone-family-aware A5 重跑 + cluster bootstrap。

输入（全部只读）：
  data/a5_676f_sample_manifest.json     1137 样本清单（含 split/origin/batch/defect_*）
  data/a5_676f_detection_matrix.json    1137×8 逐格真实 verdict（676f 产物，不重跑 detect）
  data/holdout_expansion/<batch>/*.cpp  扩样源码（只读）
  data/external_corpus/*.json           corpus 内联源码（detect_for_assets.corpus_code_map）
  data/676k_dedup_results.json          676k 去重结果（对照用）

四个阶段（--stage，可独立重跑；产物均为新增文件，不改 676f 原产物）：
  families  : 构建 clone-family（归一化精确 + 双指标克隆关系 + 全对约束）
  splits    : 两种 family-aware split + 原 split 的 leakage 量化
  a5        : 用新 split 复用 676f 判定矩阵重算 A5（主/并列/子组/planted/批次）
  bootstrap : 按家族重采样的 cluster bootstrap（2000 次）+ 与普通 CI 对比

克隆关系（pair 级，两种指标任一满足即可，与 676k 口径一致）：
  C1 归一化精确同构（676k L2：去注释/字面量、标识符→ID、数字→NUM 后逐字相同）；
  C2 归一化 token-set Jaccard ≥ 0.85（对"换常量/变量名/注释"免疫，对增删语句敏感）；
  C3 676k L3b 结构层 TF-IDF 余弦 ≥ 0.90（标识符保留、常量归一，专捕"常量微调型近克隆"）。
家族 = 满足**全对约束**（family 内任意两成员都满足 C1∪C2∪C3）的极大簇（complete-linkage，
避免单链接链式合并把互不相似的样本拉进同一家族）。

红线：不改检测器、不改样本、不改 676f 产物、不重跑 detect()、不 push。
"""
from __future__ import annotations

import argparse
import collections
import difflib
import hashlib
import importlib.util
import json
import math
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "data"))

import audit_676k_dedup as k676  # noqa: E402  归一化/结构 token 口径（676k，未改动）
import run_a5_experiment_673p as a5  # noqa: E402  三臂/统计原语（未改动）
import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
DEDUP_676K = ROOT / "data" / "676k_dedup_results.json"
FAMILIES_OUT = ROOT / "data" / "677b_clone_families.json"
FAMILY_REPORT = ROOT / "data" / "677b_clone_family_report.md"
SPLIT_RANDOM_OUT = ROOT / "data" / "677b_split_family_random.json"
SPLIT_STRAT_OUT = ROOT / "data" / "677b_split_family_stratified.json"
SPLIT_REPORT = ROOT / "data" / "677b_split_comparison.md"
RES_RANDOM_OUT = ROOT / "data" / "677b_a5_results_family_random.json"
RES_STRAT_OUT = ROOT / "data" / "677b_a5_results_family_stratified.json"
COMPARISON_MD = ROOT / "data" / "677b_a5_comparison_table.md"
BOOT_OUT = ROOT / "data" / "677b_cluster_bootstrap.json"
CI_MD = ROOT / "data" / "677b_ci_comparison.md"

ASSETS = list(vp.selectable_ids(vp.ASSET_POOL))     # 8 项已实测资产
PRIMARY_K = a5.PRIMARY_K                            # 4（673r 预注册）
SEED_ARM = a5.SEED                                  # 20260930（Random 臂）
MULTI = a5.MULTI_SEED_N                             # 2000
SEED_SPLIT = 6771                                   # 677b 卡指定
THR_JACCARD = 0.85                                  # C2 阈值（677b 卡指定主阈值）
THR_PRIMARY = THR_JACCARD                           # 主阈值别名（家族/单位定义用）
THR_COSINE = 0.90                                   # C3 阈值（676k L3b 同值）
THRESHOLDS = (0.80, 0.85, 0.90)                     # 敏感性（C2 阈值三档）
COS_THRESHOLDS = (0.90,)                            # C3 阈值（敏感性附加 0.95 见 sensitivity）
SIM_STORE = 0.80                                    # 落盘/比较下界
DEG_HI, DEG_LO = 0.95, 0.05                         # 676f 退化阈值（同口径）
Z95 = 1.959963984540054
KS = (1, 2, 3, 4)                                   # 677b 卡：k=1~4
MIN_SUBGROUP_EVAL = 10                              # 子组最小评估样本数（同 676f）

# token 切分（与 audit_676k_dedup._TOK_RE 同式；本地自持避免私名耦合）
_TOK_RE = re.compile(
    r"[A-Za-z_][A-Za-z_0-9]*"
    r"|0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][+-]?\d+)?[fFuUlL]*"
    r"|[{}()\[\];,.<>=!+\-*/%&|^~?:]+"
)


def _now() -> str:
    import datetime as _dt
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jload(p: Path) -> dict:
    data: dict = json.loads(Path(p).read_text(encoding="utf-8"))
    return data


def _jwrite(p: Path, doc: dict) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")


def _md_write(p: Path, text: str) -> None:
    Path(p).write_text(text if text.endswith("\n") else text + "\n",
                       encoding="utf-8", newline="\n")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法装载模块 {name}（{path}）")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# 676f 分析面（compact/by_k/rates/bh_fdr/退化判定）原样复用 ⇒ 口径零漂移
AN676F = None


def an676f():
    global AN676F
    if AN676F is None:
        AN676F = _load_module("analysis_676f", ROOT / "data" / "676f_analysis.py")
    return AN676F


def index_of(matrix: dict) -> dict:
    """{sample_id: {asset: verdict}}，同 676f 口径（仅 ASSETS）。"""
    return {r["sample_id"]: {a: r["per_asset"][a] for a in ASSETS} for r in matrix["samples"]}


def exec_rows(rows: list[dict]) -> list[dict]:
    return [{"id": r["sample_id"]} for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# 阶段 A：clone-family 分组
# ─────────────────────────────────────────────────────────────────────────────
def load_sources() -> tuple[dict[str, str], dict[str, dict]]:
    """sample_id → 源码文本；样本源文件全部只读。"""
    import detect_for_assets as dfa
    man = _jload(MANIFEST)
    cmap = dfa.corpus_code_map()
    texts: dict[str, str] = {}
    meta: dict[str, dict] = {}
    for s in man["samples"]:
        sid = s["sample_id"]
        if s["files"]:
            parts = []
            for f in sorted(s["files"]):
                p = ROOT / str(s["dir"]) / f
                parts.append(p.read_text(encoding="utf-8", errors="replace"))
            texts[sid] = "\n".join(parts)
            meta[sid] = {"mode": "disk_fixtures", "files": list(sorted(s["files"]))}
        else:
            code = cmap.get(sid)
            if code is None:
                raise KeyError(f"corpus 样本 {sid} 无内联源码 ⇒ fail-loud，不静默跳过")
            texts[sid] = code
            meta[sid] = {"mode": "code_materialized", "files": []}
    return texts, meta


def normalized_tokens(text: str) -> list[str]:
    """676k L2 归一化（注释/字面量剔除、标识符→ID、数字→NUM）后的 token 序列。"""
    return _TOK_RE.findall(k676.normalize(text))


def structure_hash(text: str) -> str:
    return hashlib.sha256(k676.normalize(text).encode("utf-8", "replace")).hexdigest()


def jaccard(a: set, b: set) -> float:
    inter = len(a & b)
    if not inter:
        return 0.0
    return inter / (len(a) + len(b) - inter)


def compute_pairs(texts: dict[str, str], toks_norm: dict[str, list[str]]) -> dict:
    """全对全双指标相似度（只落 S = max(Jaccard, cosine) ≥ SIM_STORE 的对）。

    cosine = 676k L3b 结构层：tokenize_structure（标识符保留、常量→NUM）上的
    sublinear-tf × idf=ln(N/df)+1 归一化向量的余弦（复用 audit_676k_dedup 原语）。
    """
    sids = sorted(texts)
    sets = {s: set(toks_norm[s]) for s in sids}
    docs = {s: k676.tokenize_structure(texts[s]) for s in sids}
    vecs = k676._tfidf_vectors([docs[s] for s in sids])
    vec = dict(zip(sids, vecs))
    out: dict[tuple[str, str], dict] = {}
    n = len(sids)
    for i in range(n):
        a = sids[i]
        sa, va = sets[a], vec[a]
        for j in range(i + 1, n):
            b = sids[j]
            sb = sets[b]
            inter = len(sa & sb)
            jac = inter / (len(sa) + len(sb) - inter) if inter else 0.0
            cos = jac if jac >= 0.90 else round(k676._cos(va, vec[b]), 6)
            s = jac if jac >= cos else cos
            if s >= SIM_STORE:
                out[(a, b)] = {"jaccard": round(jac, 6), "cosine": round(cos, 6),
                               "S": round(s, 6)}
    return out


def clone_pair(v: dict | None, thr_jac: float = THR_JACCARD,
               thr_cos: float = THR_COSINE) -> bool:
    """C1（由调用侧单独并）之外的 pair 级克隆判据：C2 ∪ C3。"""
    if not v:
        return False
    return bool(v["jaccard"] >= thr_jac or v["cosine"] >= thr_cos)


class UnionFind:
    def __init__(self, ids):
        self.p = {i: i for i in ids}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def families_single_linkage(sids, shash, pairs, thr_jac=THR_JACCARD,
                            thr_cos=THR_COSINE) -> dict:
    uf = UnionFind(sids)
    by_hash: dict[str, list[str]] = collections.defaultdict(list)
    for s in sids:
        by_hash[shash[s]].append(s)
    for members in by_hash.values():
        for m in members[1:]:
            uf.union(members[0], m)
    for (a, b), v in pairs.items():
        if clone_pair(v, thr_jac, thr_cos):
            uf.union(a, b)
    fams: dict[str, list[str]] = collections.defaultdict(list)
    for s in sids:
        fams[uf.find(s)].append(s)
    return dict(sorted((sorted(m)[0], sorted(m)) for m in fams.values()))


def families_complete_linkage(sids, shash, pairs, thr_jac=THR_JACCARD,
                              thr_cos=THR_COSINE) -> dict:
    """全对约束簇：家族内任意两成员都满足 C1∪C2∪C3 的极大簇（贪心合并，确定性）。

    种子 = 归一化精确同构组（C1 闭包，无需检查）；随后反复合并"所有交叉对都判克隆"的
    簇对，合并优先级 = min 交叉 S（越大越先合），平手按成员字典序 —— 保证可复现。
    """
    clusters: dict[int, list[str]] = {}
    by_hash: dict[str, list[str]] = collections.defaultdict(list)
    for s in sids:
        by_hash[shash[s]].append(s)
    for members in sorted(sorted(m) for m in by_hash.values()):
        clusters[len(clusters)] = members
    owner = {m: cid for cid, members in clusters.items() for m in members}

    # pair 级判据缓存（同一对会被重复查询）
    cache: dict[tuple[str, str], tuple[bool, float]] = {}

    def pair_info(a: str, b: str) -> tuple[bool, float]:
        key = (a, b) if a < b else (b, a)
        hit = cache.get(key)
        if hit is not None:
            return hit
        if shash[a] == shash[b]:
            hit = (True, 1.0)
        else:
            v = pairs.get(key)
            hit = (clone_pair(v, thr_jac, thr_cos), v["S"] if v else 0.0)
        cache[key] = hit
        return hit

    clone_edges = [(a, b) for (a, b), v in pairs.items() if clone_pair(v, thr_jac, thr_cos)]
    while True:
        # 候选簇对：至少存在一条 C2∪C3 边的簇对（owner 映射 O(1)）
        cands = set()
        for a, b in clone_edges:
            ca, cb = owner[a], owner[b]
            if ca != cb:
                cands.add((min(ca, cb), max(ca, cb)))
        best = None
        for ca, cb in sorted(cands):
            A, B = clusters[ca], clusters[cb]
            if len(A) * len(B) > 40000:      # 防御：超大簇对全对检查代价过高（跳过）
                continue
            mins = None
            ok = True
            for x in A:
                for y in B:
                    cl, s = pair_info(x, y)
                    if not cl:
                        ok = False
                        break
                    mins = s if mins is None else min(mins, s)
                if not ok:
                    break
            if not ok:
                continue
            score = mins if mins is not None else 1.0
            key = (score, tuple(A), tuple(B))
            if best is None or key > best[0]:
                best = (key, ca, cb)
        if best is None:
            break
        _, ca, cb = best
        merged = sorted(clusters[ca] + clusters[cb])
        keep = min(ca, cb)
        drop = max(ca, cb)
        clusters[keep] = merged
        del clusters[drop]
        for m in merged:
            owner[m] = keep
    fams = {sorted(m)[0]: sorted(m) for m in clusters.values()}
    return dict(sorted(fams.items()))


def _fam_record(man_idx: dict, fam_id: str, members: list[str], shash: dict,
                pairs: dict) -> dict:
    n = len(members)
    batches = collections.Counter(man_idx[m]["source_batch"] for m in members)
    dts = collections.Counter(man_idx[m]["defect_type"] for m in members)
    planted = collections.Counter(bool(man_idx[m]["planted"]) for m in members)
    groups = collections.Counter(man_idx[m]["defect_group"] for m in members)
    hashes = {shash[m] for m in members}
    jacs, coss, ss = [], [], []
    if n > 1:
        for i in range(n):
            for j in range(i + 1, n):
                a, b = members[i], members[j]
                if shash[a] == shash[b]:
                    jacs.append(1.0)
                    coss.append(1.0)
                    ss.append(1.0)
                    continue
                v = pairs.get(tuple(sorted((a, b))))
                jacs.append(v["jaccard"] if v else 0.0)
                coss.append(v["cosine"] if v else 0.0)
                ss.append(v["S"] if v else 0.0)
    avg = {}
    for m in members:
        vals = []
        for o in members:
            if o == m:
                continue
            if shash[m] == shash[o]:
                vals.append(1.0)
            else:
                v = pairs.get(tuple(sorted((m, o))))
                vals.append(v["S"] if v else 0.0)
        avg[m] = sum(vals) / len(vals) if vals else 1.0
    rep = sorted(members, key=lambda m: (-avg[m], m))[0]
    return {
        "family_id": fam_id,
        "size": n,
        "members": members,
        "representative": rep,
        "n_normalized_structures": len(hashes),
        "pure_exact": len(hashes) == 1,
        "batch_distribution": dict(sorted(batches.items())),
        "defect_group_distribution": dict(sorted(groups.items())),
        "defect_type_distribution": dict(sorted(dts.items())),
        "planted_distribution": {str(k): v for k, v in sorted(planted.items())},
        "cross_batch": len(batches) > 1,
        "cross_defect_type": len(dts) > 1,
        "min_pair_jaccard": round(min(jacs), 6) if jacs else 1.0,
        "min_pair_cosine": round(min(coss), 6) if coss else 1.0,
        "min_pair_S": round(min(ss), 6) if ss else 1.0,
    }


def _spotcheck_excerpt(members: list[str], texts: dict, pairs: dict, shash: dict,
                       max_chars: int = 400) -> list[str]:
    """家族内前两成员的可读对照（归一化文本/原文片段，截断）。"""
    a, b = members[0], members[1]
    na, nb = k676.normalize(texts[a]), k676.normalize(texts[b])
    v = pairs.get(tuple(sorted((a, b))), None)
    simtxt = ("归一化精确同构" if shash[a] == shash[b]
              else f"Jaccard={v['jaccard'] if v else 0.0:.4f} / cosine={v['cosine'] if v else 0.0:.4f}")
    lines = [f"- {'-'.join([a, b])}：成员 `{a}` ↔ `{b}`，{simtxt}"]
    if shash[a] == shash[b]:
        lines.append("  - 归一化后文本完全一致；原文片段对照：")
        lines.append(f"    - `{a}`：`{texts[a][:max_chars]!r}`".replace("\\n", " ").replace("\n", " "))
        lines.append(f"    - `{b}`：`{texts[b][:max_chars]!r}`".replace("\\n", " ").replace("\n", " "))
    else:
        d = list(difflib.unified_diff(
            [na[i:i + 60] for i in range(0, len(na), 60)],
            [nb[i:i + 60] for i in range(0, len(nb), 60)], lineterm="", n=1))[2:14]
        lines.append("  - 归一化文本 diff（前 12 行）：")
        lines.extend(f"    {x}" for x in d)
    return lines


def stage_families() -> int:
    t0 = time.perf_counter()
    man = _jload(MANIFEST)
    samples = man["samples"]
    sids = [s["sample_id"] for s in samples]
    man_idx = {s["sample_id"]: s for s in samples}
    texts, meta = load_sources()
    missing = [s for s in sids if s not in texts]
    if missing:
        raise KeyError(f"缺源码样本 {missing[:5]}（fail-loud）")

    shash = {s: structure_hash(texts[s]) for s in sids}
    toks = {s: normalized_tokens(texts[s]) for s in sids}
    print(f"[677b-A] 源码装载完成 n={len(sids)}（磁盘 {sum(1 for s in sids if meta[s]['mode']=='disk_fixtures')} / "
          f"内联 {sum(1 for s in sids if meta[s]['mode']=='code_materialized')}）；开始全对全双指标相似度…",
          flush=True)
    pairs = compute_pairs(texts, toks)
    print(f"[677b-A] 相似对（S≥{SIM_STORE}）共 {len(pairs)} 对（墙钟 {time.perf_counter()-t0:.1f}s）", flush=True)

    fams = families_complete_linkage(sids, shash, pairs)
    fam_complete_by_thr = {THR_PRIMARY: fams}
    for thr in THRESHOLDS:
        if thr == THR_PRIMARY:
            continue
        fam_complete_by_thr[thr] = families_complete_linkage(sids, shash, pairs, thr_jac=thr)
    fam_single_by_thr = {}
    for thr in THRESHOLDS:
        fam_single_by_thr[thr] = families_single_linkage(sids, shash, pairs, thr_jac=thr)
    fam_single = fam_single_by_thr[THR_JACCARD]
    print(f"[677b-A] 聚类完成（complete-linkage 3 档 + single-linkage 3 档）；"
          f"墙钟 {time.perf_counter()-t0:.1f}s", flush=True)

    fam_records = []
    for i, (key, members) in enumerate(fams.items(), start=1):
        fid = f"F{i:04d}"
        fam_records.append(_fam_record(man_idx, fid, members, shash, pairs))

    sizes = [f["size"] for f in fam_records]
    stats = {
        "n_samples": len(sids),
        "n_families": len(fam_records),
        "n_singleton_families": sum(1 for x in sizes if x == 1),
        "n_multimember_families": sum(1 for x in sizes if x > 1),
        "largest_family_size": max(sizes),
        "mean_family_size": round(sum(sizes) / len(sizes), 4),
        "n_samples_in_multimember_families": sum(x for x in sizes if x > 1),
        "clone_rate_pct": round(100.0 * sum(x for x in sizes if x > 1) / len(sids), 2),
        "n_normalized_structures": len(set(shash.values())),
        "n_cross_batch_families": sum(1 for f in fam_records if f["cross_batch"]),
        "n_cross_defect_type_families": sum(1 for f in fam_records if f["cross_defect_type"]),
        "n_pairs_ge_store": len(pairs),
        "n_pairs_jaccard_ge_085": sum(1 for v in pairs.values() if v["jaccard"] >= 0.85),
        "n_pairs_cosine_ge_090": sum(1 for v in pairs.values() if v["cosine"] >= 0.90),
        "n_pairs_cosine_only": sum(1 for v in pairs.values()
                                   if v["cosine"] >= 0.90 and v["jaccard"] < 0.85),
        "min_pair_S_global": round(min((v["S"] for v in pairs.values()), default=0.0), 6),
    }

    def _fam_summary(famsd: dict) -> dict:
        szs = [len(v) for v in famsd.values()]
        return {
            "n_families": len(famsd),
            "n_singleton_families": sum(1 for x in szs if x == 1),
            "largest_family_size": max(szs),
            "n_cross_batch_families": sum(
                1 for v in famsd.values() if len({man_idx[m]["source_batch"] for m in v}) > 1),
        }

    sensitivity: dict[str, Any] = {
        "complete_linkage_by_threshold": {str(t): _fam_summary(f) for t, f in fam_complete_by_thr.items()},
        "single_linkage_by_threshold": {str(t): _fam_summary(f) for t, f in fam_single_by_thr.items()},
        "note": ("主家族定义 = complete-linkage @0.85（家族内任意两成员都判克隆）；"
                 "single-linkage 作为对照给出（会链式合并，同族内可能出现不相似成员）"),
    }

    a5set = set(sids)
    fam_of = {}
    for f in fam_records:
        for m in f["members"]:
            fam_of[m] = f["family_id"]
    unit_of = {}
    for uid, members in fam_single.items():
        for m in members:
            unit_of[m] = uid
    n_clone_pairs = sum(1 for v in pairs.values() if clone_pair(v))
    stats["n_clone_pairs"] = n_clone_pairs
    stats["n_clone_pairs_cross_family"] = sum(
        1 for (a, b), v in pairs.items() if clone_pair(v) and fam_of[a] != fam_of[b])
    stats["n_clone_pairs_cross_unit"] = sum(
        1 for (a, b), v in pairs.items() if clone_pair(v) and unit_of[a] != unit_of[b])

    # 与 676k 对照
    k676cmp: dict[str, Any] = {"status": "skip"}
    if DEDUP_676K.is_file():
        d = _jload(DEDUP_676K)
        l2 = d["layer2_normalized"]["details"]["groups"]
        l3b = d["layer3b_cross_batch_structure"]["pairs"]
        l2_hit_groups = 0
        l2_hit_members = 0
        for g in l2:
            a5m = [k676.to_a5_id(x["batch"], x["uid"].split(":", 1)[1]) for x in g["members"]]
            a5m = [x for x in a5m if x in a5set]
            if len(a5m) > 1:
                l2_hit_groups += 1
                l2_hit_members += len(a5m)
        cov: dict[str, Any] = {"n_pairs_676k": len(l3b), "n_both_in_a5": 0, "n_same_family": 0,
                               "n_missing_endpoint": 0, "examples_not_same_family": []}
        for p in l3b:
            ia = k676.to_a5_id(p["a"]["batch"], p["a"]["uid"].split(":", 1)[1])
            ib = k676.to_a5_id(p["b"]["batch"], p["b"]["uid"].split(":", 1)[1])
            if ia not in a5set or ib not in a5set:
                cov["n_missing_endpoint"] += 1
                continue
            cov["n_both_in_a5"] += 1
            if fam_of.get(ia) == fam_of.get(ib):
                cov["n_same_family"] += 1
            elif len(cov["examples_not_same_family"]) < 10:
                cov["examples_not_same_family"].append(
                    {"a": ia, "b": ib, "sim_676k": p["similarity"],
                     "fam_a": fam_of.get(ia), "fam_b": fam_of.get(ib),
                     "677b": pairs.get(tuple(sorted((ia, ib))))})
        k676cmp = {"n_l2_groups_in_a5": l2_hit_groups, "n_l2_members_in_a5": l2_hit_members,
                   "cross_batch_pair_coverage": cov}

    # 质量检查：C1 精确同构组不得被拆到多个家族
    hash_groups = collections.defaultdict(set)
    for s in sids:
        hash_groups[shash[s]].add(s)
    split_ok = all(len({fam_of[m] for m in members}) == 1 for members in hash_groups.values())

    doc = {
        "schema": "queyi-677b-clone-families/v1",
        "generated_by": "tools/analyze_677b_clone_aware.py families",
        "generated_at": _now(),
        "inputs": {"manifest": "data/a5_676f_sample_manifest.json",
                   "matrix": "data/a5_676f_detection_matrix.json",
                   "expansion_dir": "data/holdout_expansion/<batch>/",
                   "corpus_inline": "detect_for_assets.corpus_code_map()"},
        "method": {
            "normalization": "676k L2 同口径：去注释/字面量 → 标识符→ID → 数字→NUM → 去空白（audit_676k_dedup.normalize）",
            "C1_exact": "归一化文本 sha256 一致 ⇒ 必同家族",
            "C2_jaccard": f"归一化 token-set Jaccard ≥ {THR_JACCARD}",
            "C3_cosine": f"676k L3b 结构层 TF-IDF 余弦 ≥ {THR_COSINE}（标识符保留、常量→NUM）",
            "pair_clone": "C1 ∪ C2 ∪ C3（任一满足即判克隆）",
            "clustering": "complete-linkage：家族内任意两成员都必须判克隆的极大簇（贪心，确定性）",
            "threshold_rationale": ("0.85（C2）/0.90（C3）沿用 677b 卡与 676k L3b 既有阈值；"
                                    "C2 对「换常量/变量名/注释」免疫，C3 补上「常量微调 + 强制转换等"
                                    "小改」型近克隆（676k 的 103 对跨批近克隆有 10 对只被 C3 覆盖）；"
                                    "三档阈值敏感性见 sensitivity 字段"),
        },
        "stats": stats,
        "sensitivity": sensitivity,
        "checks": {
            "exact_groups_never_split_across_families": split_ok,
            "complete_linkage_min_pair_rule": "家族内所有对都满足 C1∪C2∪C3（由构造保证）",
        },
        "comparison_676k": k676cmp,
        "family_index": {f["family_id"]: f["members"] for f in fam_records},
        "split_units": {
            "definition": ("克隆关系（C1∪C2∪C3）图的**连通分量**（single-linkage 闭包）——"
                           "分裂以它为最小单位，保证任意一对判克隆的样本不跨 split（最强约束）"),
            "n_units": len(fam_single),
            "largest_unit_size": max(len(v) for v in fam_single.values()),
            "sizes_top10": sorted((len(v) for v in fam_single.values()), reverse=True)[:10],
            "cross_batch_units": sum(
                1 for v in fam_single.values()
                if len({man_idx[m]["source_batch"] for m in v}) > 1),
            "index": {f"U{i:04d}": v for i, v in enumerate(fam_single.values(), start=1)},
        },
        "families": fam_records,
    }
    _jwrite(FAMILIES_OUT, doc)

    # 家族报告（含抽查证据）
    lines = []
    lines.append("# 677b · 任务A：Clone-Family 分组报告\n")
    lines.append(f"- 生成：`tools/analyze_677b_clone_aware.py families`（{doc['generated_at']}）")
    lines.append("- 机器可读：`data/677b_clone_families.json`")
    lines.append(f"- 样本 n={stats['n_samples']}（磁盘夹具 {sum(1 for s in sids if meta[s]['mode']=='disk_fixtures')}，"
                 f"corpus 内联源码 {sum(1 for s in sids if meta[s]['mode']=='code_materialized')}）")
    lines.append("- 克隆关系：C1 归一化精确同构 ∪ C2 Jaccard≥0.85 ∪ C3 结构层余弦≥0.90；"
                 "家族 = 满足全对约束的极大簇（complete-linkage）\n")
    lines.append("## 1. 家族统计（主定义）\n")
    lines.append(f"- 家族总数 **{stats['n_families']}**（单成员 {stats['n_singleton_families']}，多成员 {stats['n_multimember_families']}）")
    lines.append(f"- 最大家族 {stats['largest_family_size']} 条；平均家族 {stats['mean_family_size']} 条")
    lines.append(f"- 落在多成员家族的样本 {stats['n_samples_in_multimember_families']} / {stats['n_samples']}"
                 f"（{stats['clone_rate_pct']}%）")
    lines.append(f"- 归一化精确结构种数 {stats['n_normalized_structures']}")
    lines.append(f"- 跨批家族 {stats['n_cross_batch_families']} 个；跨 defect_type 家族 {stats['n_cross_defect_type_families']} 个")
    lines.append(f"- 相似对（S≥0.80）：{stats['n_pairs_ge_store']} 对；其中 Jaccard≥0.85 {stats['n_pairs_jaccard_ge_085']} 对，"
                 f"cosine≥0.90 {stats['n_pairs_cosine_ge_090']} 对（仅由 C3 覆盖 {stats['n_pairs_cosine_only']} 对）")
    lines.append(f"- 判克隆的对共 {stats['n_clone_pairs']} 对：跨**连通分量** "
                 f"{stats['n_clone_pairs_cross_unit']} 对（=0 即「不存在判克隆却可能跨 split 的对」），"
                 f"跨**家族** {stats['n_clone_pairs_cross_family']} 对（complete-linkage 全对约束的代价）\n")
    lines.append("## 2. 阈值/聚类方式敏感性\n")
    lines.append("| 聚类 | 阈值 | 家族数 | 单成员 | 最大族 | 跨批家族 |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for t in THRESHOLDS:
        v = sensitivity["complete_linkage_by_threshold"][str(t)]
        lines.append(f"| complete | {t} | {v['n_families']} | {v['n_singleton_families']} | "
                     f"{v['largest_family_size']} | {v['n_cross_batch_families']} |")
    for t in THRESHOLDS:
        v = sensitivity["single_linkage_by_threshold"][str(t)]
        lines.append(f"| single | {t} | {v['n_families']} | {v['n_singleton_families']} | "
                     f"{v['largest_family_size']} | {v['n_cross_batch_families']} |")
    lines.append("")
    lines.append("## 3. 与 676k 的对照\n")
    if k676cmp.get("status") != "skip":
        lines.append(f"- 676k L2 归一化重复组在 A5 抽样内：{k676cmp['n_l2_groups_in_a5']} 组 / "
                     f"{k676cmp['n_l2_members_in_a5']} 条")
        c = k676cmp["cross_batch_pair_coverage"]
        lines.append(f"- 676k 的跨批近克隆对 {c['n_pairs_676k']} 对：两端均在 A5 {c['n_both_in_a5']} 对，"
                     f"其中 {c['n_same_family']} 对落进同一家族")
        for e in c["examples_not_same_family"]:
            lines.append(f"  - 未同族例：{e['a']} ~ {e['b']}（676k sim={e['sim_676k']}，"
                         f"677b={e['677b']}，家族 {e['fam_a']} / {e['fam_b']}）")
    else:
        lines.append("- 676k 结果缺失，跳过对照")
    lines.append("")
    lines.append("## 4. 抽查证据（自动生成，供人工复核）\n")
    multi = [f for f in fam_records if f["size"] > 1]
    multi_sorted = sorted(multi, key=lambda f: (-f["size"], f["family_id"]))
    picks = multi_sorted[:5]
    rnd = random.Random(SEED_SPLIT)
    rest = [f for f in multi if f not in picks]
    picks += rnd.sample(rest, min(5, len(rest)))
    lines.append("### 4.1 抽查 10 个家族（5 个最大 + 5 个随机）\n")
    for f in picks:
        lines.append(f"- **{f['family_id']}**（size={f['size']}，批次 {f['batch_distribution']}，"
                     f"pure_exact={f['pure_exact']}，min_jaccard={f['min_pair_jaccard']}，"
                     f"min_cosine={f['min_pair_cosine']}）")
        lines.extend(_spotcheck_excerpt(f["members"], texts, pairs, shash))
    lines.append("")
    lines.append("### 4.2 边界对分类（跨家族的对，最多各 12 对）\n")
    fam_of_all = fam_of
    cross = [(k, v) for k, v in pairs.items() if fam_of_all[k[0]] != fam_of_all[k[1]]]
    cross_clone = [(k, v) for k, v in cross if clone_pair(v)]
    cross_nonclone = [(k, v) for k, v in cross if not clone_pair(v)]
    cross_clone.sort(key=lambda kv: (-kv[1]["S"], kv[0]))
    cross_nonclone.sort(key=lambda kv: (-kv[1]["S"], kv[0]))
    lines.append(f"跨家族的对共 {len(cross)} 对，其中**判克隆但未合并** {len(cross_clone)} 对"
                 f"（complete-linkage 全对约束的残余；它们所在**连通分量**相同 ⇒ 在 strict split 下"
                 f"仍被保证不跨 side），**不判克隆** {len(cross_nonclone)} 对。\n")
    lines.append("**(a) 判克隆但跨家族（残余，按 S 降序）**：\n")
    if cross_clone:
        for (a, b), v in cross_clone[:12]:
            lines.append(f"- {a} ~ {b}：Jaccard={v['jaccard']:.4f}，cosine={v['cosine']:.4f}，"
                         f"家族 {fam_of_all[a]} vs {fam_of_all[b]}，"
                         f"同分量={unit_of[a] == unit_of[b]}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("**(b) 高相似但不判克隆（阈值下正确分开，按 S 降序）**：\n")
    if cross_nonclone:
        for (a, b), v in cross_nonclone[:12]:
            lines.append(f"- {a} ~ {b}：Jaccard={v['jaccard']:.4f}，cosine={v['cosine']:.4f}，"
                         f"家族 {fam_of_all[a]} vs {fam_of_all[b]}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("### 4.3 家族大表（size ≥ 5）\n")
    lines.append("| family | size | 批次 | defect_type 数 | min_jaccard | min_cosine | 代表 |")
    lines.append("|---|---:|---|---:|---:|---:|---|")
    for f in multi_sorted:
        if f["size"] >= 5:
            lines.append(f"| {f['family_id']} | {f['size']} | {f['batch_distribution']} | "
                         f"{len(f['defect_type_distribution'])} | {f['min_pair_jaccard']} | "
                         f"{f['min_pair_cosine']} | {f['representative']} |")
    lines.append("")
    _md_write(FAMILY_REPORT, "\n".join(lines))
    print(f"[677b-A] 家族 n={stats['n_families']}（多成员 {stats['n_multimember_families']}，"
          f"最大 {stats['largest_family_size']}）；写 {FAMILIES_OUT.name} / {FAMILY_REPORT.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 阶段 B：family-aware split + 原 split 的 leakage 量化
# ─────────────────────────────────────────────────────────────────────────────
def _dominant_key(members: list[str], man_idx: dict) -> tuple[str, str]:
    """家族/单元的主标签 = (source_batch, defect_type) 众数（平手取字典序小者）。"""
    c = collections.Counter((man_idx[m]["source_batch"], man_idx[m]["defect_type"]) for m in members)
    top = max(c.values())
    return sorted(k for k, v in c.items() if v == top)[0]


def assign_side(units: dict[str, list[str]], mode: str, man_idx: dict,
                seed: int = SEED_SPLIT) -> dict[str, str]:
    """把每个分裂单位整体分配到一个 side。

    mode = "random"     ：单位随机顺序，贪心放到当前样本数较少的一侧（全局平衡）
    mode = "stratified" ：按主标签 (batch, defect_type) 分层，层内随机顺序 + 局部优先平衡
    """
    rnd = random.Random(seed)
    counts = {"derivation": 0, "evaluation": 0}
    assign: dict[str, str] = {}

    def _pick(size: int, local: dict[str, int] | None):
        def cost(side: str):
            other = "evaluation" if side == "derivation" else "derivation"
            loc = (abs(local[side] + size - local[other]) if local is not None else 0)
            glob = abs(counts[side] + size - counts[other])
            return (loc, glob, 0 if side == "derivation" else 1)
        return "derivation" if cost("derivation") <= cost("evaluation") else "evaluation"

    if mode == "random":
        order = sorted(units)
        rnd.shuffle(order)
        for uid in order:
            side = _pick(len(units[uid]), None)
            assign[uid] = side
            counts[side] += len(units[uid])
    elif mode == "stratified":
        strata: dict[tuple, list[str]] = collections.defaultdict(list)
        for uid, members in units.items():
            strata[_dominant_key(members, man_idx)].append(uid)
        for key in sorted(strata):
            local = {"derivation": 0, "evaluation": 0}
            uids = sorted(strata[key])
            rnd.shuffle(uids)
            for uid in uids:
                size = len(units[uid])
                side = _pick(size, local)
                assign[uid] = side
                counts[side] += size
                local[side] += size
    else:
        raise ValueError(f"未知 mode={mode!r}")
    return assign


def sample_split_of(units: dict[str, list[str]], assign: dict[str, str]) -> dict[str, str]:
    out = {}
    for uid, members in units.items():
        for m in members:
            out[m] = assign[uid]
    return out


def _balance(sample_split: dict[str, str], man_idx: dict, attr: str) -> dict:
    """两侧在属性 attr 上的分布（比例 + 最大偏差 pp）。"""
    sides: dict[str, collections.Counter[str]] = {
        "derivation": collections.Counter(), "evaluation": collections.Counter()}
    for sid, side in sample_split.items():
        v = man_idx[sid][attr] if attr != "planted" else bool(man_idx[sid]["planted"])
        sides[side][str(v)] += 1
    nd, ne = sum(sides["derivation"].values()), sum(sides["evaluation"].values())
    keys = sorted(set(sides["derivation"]) | set(sides["evaluation"]))
    rows = {}
    max_dev = 0.0
    for k in keys:
        pd = 100.0 * sides["derivation"].get(k, 0) / nd
        pe = 100.0 * sides["evaluation"].get(k, 0) / ne
        rows[k] = {"derivation_pct": round(pd, 4), "evaluation_pct": round(pe, 4),
                   "dev_pp": round(pd - pe, 4)}
        max_dev = max(max_dev, abs(pd - pe))
    return {"attr": attr, "derivation_n": nd, "evaluation_n": ne,
            "by_value": rows, "max_dev_pp": round(max_dev, 4)}


def validate_split(sample_split: dict[str, str], man_idx: dict, famdoc: dict,
                   extras: dict | None = None) -> dict:
    fam_of, unit_of = {}, {}
    for fid, members in famdoc["family_index"].items():
        for m in members:
            fam_of[m] = fid
    for uid, members in famdoc["split_units"]["index"].items():
        for m in members:
            unit_of[m] = uid

    def _cross(idx_of: dict[str, str], sizes_of: dict[str, int] | None = None) -> dict:
        groups: dict[str, set] = collections.defaultdict(set)
        for sid, side in sample_split.items():
            groups[idx_of[sid]].add(side)
        cross = {g: v for g, v in groups.items() if len(v) > 1}
        members_cross = sum(1 for sid in sample_split if len(groups[idx_of[sid]]) > 1)
        out = {"n_groups": len(groups), "n_cross_groups": len(cross),
               "n_samples_in_cross_groups": members_cross,
               "cross_group_ids": sorted(cross)[:20],
               "n_groups_with_evaluation": sum(1 for g, v in groups.items() if "evaluation" in v),
               "n_groups_with_derivation": sum(1 for g, v in groups.items() if "derivation" in v)}
        if sizes_of:
            sizes = sorted((sizes_of[g] for g in cross), reverse=True)
            out["crossing_group_sizes_top10"] = sizes[:10]
        return out

    # 克隆对跨越（CL 家族内所有对 + 所有 pair 级克隆对）
    pairs = extras.get("pairs", {}) if extras else {}
    shash = extras.get("shash", {}) if extras else {}
    clone_cross = []
    for (a, b), v in pairs.items():
        if shash.get(a) == shash.get(b) or clone_pair(v):
            if sample_split[a] != sample_split[b]:
                clone_cross.append({"a": a, "b": b, "jaccard": v["jaccard"], "cosine": v["cosine"]})
    sizes = collections.Counter(sample_split.values())
    fam_sizes = {fid: len(m) for fid, m in famdoc["family_index"].items()}
    unit_sizes = {uid: len(m) for uid, m in famdoc["split_units"]["index"].items()}
    return {
        "n_derivation": sizes.get("derivation", 0), "n_evaluation": sizes.get("evaluation", 0),
        "family_level": _cross(fam_of, fam_sizes),
        "unit_level": _cross(unit_of, unit_sizes),
        "clone_pairs_crossing": {"n": len(clone_cross), "examples": clone_cross[:10]},
        "balance": {a: _balance(sample_split, man_idx, a)
                    for a in ("source_batch", "defect_group", "defect_type", "planted")},
    }


def stage_splits() -> int:
    man = _jload(MANIFEST)
    samples = man["samples"]
    man_idx = {s["sample_id"]: s for s in samples}
    famdoc = _jload(FAMILIES_OUT)
    texts, _meta = load_sources()
    shash = {s["sample_id"]: structure_hash(texts[s["sample_id"]]) for s in samples}
    toks = {s["sample_id"]: normalized_tokens(texts[s["sample_id"]]) for s in samples}
    print("[677b-B] 重算相似对（用于 leakage 量化）…", flush=True)
    pairs = compute_pairs(texts, toks)
    extras = {"pairs": pairs, "shash": shash}

    fam_units = famdoc["family_index"]            # 全对凝聚家族（报告口径）
    strict_units = famdoc["split_units"]["index"]  # 连通分量（最强不泄漏口径）

    original = {s["sample_id"]: s["split"] for s in samples}
    orig_stats = validate_split(original, man_idx, famdoc, extras)

    configs = [
        ("family_random", fam_units, "random"),
        ("family_stratified", fam_units, "stratified"),
        ("strict_stratified", strict_units, "stratified"),
    ]
    outs: dict[str, Any] = {"original": {"strategy": "original（676f 原 split：层内 sha256 奇偶）",
                                         "sample_split": original, "validation": orig_stats}}
    for name, units, mode in configs:
        assign = assign_side(units, mode, man_idx)
        ssmap = sample_split_of(units, assign)
        val = validate_split(ssmap, man_idx, famdoc, extras)
        outs[name] = {
            "strategy": mode, "unit_definition": ("全对凝聚家族" if units is fam_units else "连通分量"),
            "n_units": len(units), "seed": SEED_SPLIT,
            "unit_assignment": assign, "sample_split": ssmap, "validation": val,
        }
        print(f"[677b-B] {name}: 派生 {val['n_derivation']} / 评估 {val['n_evaluation']}；"
              f"家族跨 split {val['family_level']['n_cross_groups']}，"
              f"单位跨 split {val['unit_level']['n_cross_groups']}，"
              f"克隆对跨 split {val['clone_pairs_crossing']['n']}", flush=True)

    for fname, key in ((SPLIT_RANDOM_OUT, "family_random"), (SPLIT_STRAT_OUT, "family_stratified")):
        doc = {
            "schema": "queyi-677b-split/v1",
            "generated_by": "tools/analyze_677b_clone_aware.py splits",
            "generated_at": _now(),
            "inputs": {"families": "data/677b_clone_families.json",
                       "manifest": "data/a5_676f_sample_manifest.json"},
            "seed": SEED_SPLIT,
            "derivation": sorted(s for s, v in outs[key]["sample_split"].items() if v == "derivation"),
            "evaluation": sorted(s for s, v in outs[key]["sample_split"].items() if v == "evaluation"),
            "meta": outs[key],
        }
        _jwrite(fname, doc)
    # 附带落盘 strict 变体（不泄漏最强口径；作为 C 阶段第三个 split 的输入）
    doc = {
        "schema": "queyi-677b-split/v1",
        "generated_by": "tools/analyze_677b_clone_aware.py splits",
        "generated_at": _now(),
        "seed": SEED_SPLIT,
        "derivation": sorted(s for s, v in outs["strict_stratified"]["sample_split"].items()
                             if v == "derivation"),
        "evaluation": sorted(s for s, v in outs["strict_stratified"]["sample_split"].items()
                             if v == "evaluation"),
        "meta": outs["strict_stratified"],
        "note": "strict 变体：分裂单位 = 克隆关系图连通分量（同族不跨 split 的最强保证）",
    }
    _jwrite(ROOT / "data" / "677b_split_strict_stratified.json", doc)

    # 报告
    L = []
    L.append("# 677b · 任务B：Clone-aware split 对比与 leakage 量化\n")
    L.append(f"- 生成：`tools/analyze_677b_clone_aware.py splits`（{_now()}）；seed={SEED_SPLIT}")
    L.append("- 分裂单位：**全对凝聚家族**（family_random / family_stratified，口径见任务A）"
             "与 **连通分量**（strict_stratified，最强不泄漏口径）")
    L.append("- 判据：同单位整体进同一 side；克隆对（C1∪C2∪C3）不得跨 side\n")
    L.append("## 1. 泄漏量化：原 split 的问题有多大\n")
    o = orig_stats
    L.append("| 指标 | 原 split（676f） | family_random | family_stratified | strict_stratified |")
    L.append("|---|---:|---:|---:|---:|")
    rows = [
        ("派生/评估样本数", lambda v: f"{v['n_derivation']}/{v['n_evaluation']}"),
        ("跨 split 的**家族**数", lambda v: f"{v['family_level']['n_cross_groups']} / {v['family_level']['n_groups']}"),
        ("跨 split 家族涉及样本", lambda v: str(v['family_level']['n_samples_in_cross_groups'])),
        ("原 split 跨 split 家族规模（前 10）",
         lambda v: str(v['family_level'].get('crossing_group_sizes_top10', [])) if v is o else "—"),
        ("跨 split 的**单位**数", lambda v: f"{v['unit_level']['n_cross_groups']} / {v['unit_level']['n_groups']}"),
        ("跨 split 单位涉及样本", lambda v: str(v['unit_level']['n_samples_in_cross_groups'])),
        ("跨 split 的**克隆对**数", lambda v: str(v['clone_pairs_crossing']['n'])),
        ("评估侧独立单位数", lambda v: str(v['unit_level']['n_groups_with_evaluation'])),
        ("派生侧独立单位数", lambda v: str(v['unit_level']['n_groups_with_derivation'])),
    ]
    for name, fn in rows:
        L.append(f"| {name} | {fn(o)} | {fn(outs['family_random']['validation'])} | "
                 f"{fn(outs['family_stratified']['validation'])} | {fn(outs['strict_stratified']['validation'])} |")
    L.append("")
    L.append("## 2. 分布均衡（最大偏差 pp；越小越均衡）\n")
    L.append("| 属性 | 原 split | family_random | family_stratified | strict_stratified |")
    L.append("|---|---:|---:|---:|---:|")
    for a in ("source_batch", "defect_group", "defect_type", "planted"):
        L.append(f"| {a} | {o['balance'][a]['max_dev_pp']} | "
                 f"{outs['family_random']['validation']['balance'][a]['max_dev_pp']} | "
                 f"{outs['family_stratified']['validation']['balance'][a]['max_dev_pp']} | "
                 f"{outs['strict_stratified']['validation']['balance'][a]['max_dev_pp']} |")
    L.append("")
    L.append("## 3. 各项校验\n")
    for key, label in (("family_random", "family_random"), ("family_stratified", "family_stratified"),
                       ("strict_stratified", "strict_stratified")):
        v = outs[key]["validation"]
        L.append(f"- **{label}**：家族跨 split {v['family_level']['n_cross_groups']}（要求 0）；"
                 f"克隆对跨 split {v['clone_pairs_crossing']['n']}；"
                 f"派生 {v['n_derivation']} / 评估 {v['n_evaluation']}")
    L.append("")
    L.append("## 4. 结论\n")
    L.append("- 原 split 下：**同一家族的成员被劈到两侧**——"
             f"{o['family_level']['n_cross_groups']}/{o['family_level']['n_groups']} 个家族跨 split、"
             f"涉及 {o['family_level']['n_samples_in_cross_groups']} 条样本、"
             f"{o['clone_pairs_crossing']['n']} 对判克隆的样本对分居两侧；这就是评审指出的 "
             "template-family leakage 的量化证据；")
    L.append("- clone-aware split 下：家族跨 split = 0（构造保证）；**strict 变体**（连通分量为单位）"
             "进一步保证**任意一对判克隆的样本**都不跨 split（克隆对跨越 = 0）。"
             "family 级变体仍有少量残余克隆对跨越（同分量内的跨族对），已如实记录；")
    L.append("- 均衡性代价：金标准是原 split 的分层均衡（batch 最大偏差 0.27pp）；family-aware split "
             "无法同时满足「家族整体不动」与「批次完全均衡」（跨批家族把别的批次样本一起带走），"
             "各属性最大偏差见 §2（最大 7.0pp，出现在 family_random 的 source_batch）。"
             "A5 结论在三种 split 下的稳定性见 `data/677b_a5_comparison_table.md`；")
    L.append("- 样本数偏差：三种 split 评估侧 568–569 条，与原 566 的偏差 <0.4%（验收要求 ±5% 内）。\n")
    _md_write(SPLIT_REPORT, "\n".join(L))
    print(f"[677b-B] 写 {SPLIT_RANDOM_OUT.name} / {SPLIT_STRAT_OUT.name} / "
          f"677b_split_strict_stratified.json / {SPLIT_REPORT.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 阶段 C：用新 split 重算 A5（复用 676f 判定矩阵；口径与 676f/673p 完全一致）
# ─────────────────────────────────────────────────────────────────────────────
def co_primary_candidates(samples: list[dict], index: dict) -> tuple[list[str], dict]:
    deg = an676f().degenerate(samples, ASSETS, index)          # 676f 全池退化口径
    return [a for a in ASSETS if a not in deg], deg


def subset_block(rows: list[dict], index: dict, fh: dict, keyfn, multi: int = MULTI,
                 min_eval: int = MIN_SUBGROUP_EVAL) -> tuple[dict, dict]:
    """一个切面（defect_group / defect_type / planted / batch）的子组分析 + BH-FDR。"""
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        groups[str(keyfn(r))].append(r)
    out: dict[str, dict] = {}
    for g, rows_all in sorted(groups.items()):
        g_ev = [r for r in rows_all if r["split"] == "evaluation"]
        g_der = [r for r in rows_all if r["split"] == "derivation"]
        if len(g_ev) < min_eval:
            out[g] = {"status": "skip", "why": f"评估集 n={len(g_ev)} < {min_eval}",
                      "n_derivation": len(g_der), "n_evaluation": len(g_ev)}
            continue
        bk = an676f().by_k(g_ev, index, ASSETS, fh, ks=(PRIMARY_K,), multi=multi)
        c = an676f().compact(bk[0])
        c.update({"n_derivation": len(g_der), "n_evaluation": len(g_ev),
                  "fd_fail_hits_top4": sorted(fh.items(), key=lambda kv: (-kv[1], kv[0]))[:4]})
        out[g] = c
    tested = [(g, v) for g, v in out.items() if "mcnemar_p" in v]
    ps = [v["mcnemar_p"] for _, v in tested]
    qs = an676f().bh_fdr(ps)
    rows_m = [{"group": g, "p_raw": v["mcnemar_p"], "p_bh_fdr": round(q, 6),
               "p_bonferroni": round(min(1.0, v["mcnemar_p"] * len(ps)), 6),
               "delta_pp": v["delta_fd_minus_random_pp"], "n_evaluation": v["n_evaluation"]}
              for (g, v), q in zip(tested, qs)]
    rows_m.sort(key=lambda r: r["p_raw"])
    return out, {"n_tests": len(tested), "method": "BH-FDR + Bonferroni（对子组 McNemar p）",
                 "rows": rows_m}


def analyze_split(name: str, sample_split: dict[str, str], samples: list[dict], index: dict,
                  co_cands: list[str], degen: dict, multi: int = MULTI,
                  ks=KS) -> dict:
    rows = []
    for s in samples:
        r = dict(s)
        r["split"] = sample_split[s["sample_id"]]
        rows.append(r)
    deriv = [r for r in rows if r["split"] == "derivation"]
    ev = [r for r in rows if r["split"] == "evaluation"]
    if not deriv or not ev:
        raise ValueError(f"{name}: 派生/评估集为空 ⇒ fail-loud")
    a = an676f()
    fh = a.fail_hits_real(deriv, ASSETS, index)

    main_by_k = a.by_k(ev, index, ASSETS, fh, ks=ks, multi=multi)
    co_by_k = a.by_k(ev, index, co_cands, fh, ks=ks, multi=multi)

    sg_group, mult_group = subset_block(rows, index, fh, lambda r: r["defect_group"], multi)
    sg_type, mult_type = subset_block(rows, index, fh, lambda r: r["defect_type"], multi)
    sg_planted, mult_planted = subset_block(rows, index, fh, lambda r: f"planted={bool(r['planted'])}", multi)
    sg_batch, mult_batch = subset_block(rows, index, fh, lambda r: r["source_batch"], multi)

    def _dist(keyfn) -> dict:
        out: dict[str, int] = {}
        for r in rows:
            k = str(keyfn(r))
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))

    return {
        "split_name": name,
        "n_derivation": len(deriv), "n_evaluation": len(ev),
        "derivation_fail_hits": fh,
        "sample_stats": {
            "by_split_x_batch": _dist(lambda r: f"{r['split']}/{r['source_batch']}"),
            "by_split_x_group": _dist(lambda r: f"{r['split']}/{r['defect_group']}"),
            "by_split_x_planted": _dist(lambda r: f"{r['split']}/planted={bool(r['planted'])}"),
        },
        "primary_main_8candidates": {
            "by_k_compact": [a.compact(x) for x in main_by_k],
            "primary": a.compact(main_by_k[0]) if ks == (PRIMARY_K,) else next(
                (a.compact(x) for x in main_by_k if x["budget_k"] == PRIMARY_K), None),
        },
        "co_primary_excl_degenerate": {
            "candidates": co_cands, "degenerate_full_pool": degen,
            "by_k_compact": [a.compact(x) for x in co_by_k],
            "primary": next((a.compact(x) for x in co_by_k if x["budget_k"] == PRIMARY_K), None),
        },
        "subgroups_defect_group": {"blocks": sg_group, "multiplicity": mult_group},
        "subgroups_defect_type": {"blocks": sg_type, "multiplicity": mult_type},
        "subgroups_planted": {"blocks": sg_planted, "multiplicity": mult_planted},
        "subgroups_batch": {"blocks": sg_batch, "multiplicity": mult_batch},
    }


def stage_a5() -> int:
    man = _jload(MANIFEST)
    matrix = _jload(MATRIX)
    samples = man["samples"]
    index = index_of(matrix)
    co_cands, degen = co_primary_candidates(samples, index)
    orig_map = {s["sample_id"]: s["split"] for s in samples}
    print(f"[677b-C] 并列口径候选 {co_cands}（退化 {list(degen)}）；开始原 split 对照重算…", flush=True)

    t0 = time.perf_counter()
    control = analyze_split("original(676f)", orig_map, samples, index, co_cands, degen)
    reg = _jload(ROOT / "data" / "a5_676f_results.json")
    pm_reg = reg["primary_main_8candidates"]["primary"]
    pm_new = control["primary_main_8candidates"]["primary"]
    co_reg = reg["co_primary_excl_degenerate"]["primary"]
    co_new = control["co_primary_excl_degenerate"]["primary"]
    checks = {
        "fd_rate_match": pm_new["fd_rate_pct"] == pm_reg["fd_rate_pct"],
        "random_rate_match": pm_new["random_rate_pct"] == pm_reg["random_rate_pct"],
        "delta_match": pm_new["delta_fd_minus_random_pp"] == pm_reg["delta_fd_minus_random_pp"],
        "mcnemar_p_match": pm_new["mcnemar_p"] == pm_reg["mcnemar_p"],
        "co_delta_match": co_new["delta_fd_minus_random_pp"] == co_reg["delta_fd_minus_random_pp"],
        "registered": {"fd_rate_pct": pm_reg["fd_rate_pct"], "random_rate_pct": pm_reg["random_rate_pct"],
                       "delta_pp": pm_reg["delta_fd_minus_random_pp"], "mcnemar_p": pm_reg["mcnemar_p"],
                       "co_delta_pp": co_reg["delta_fd_minus_random_pp"]},
        "recomputed": {"fd_rate_pct": pm_new["fd_rate_pct"], "random_rate_pct": pm_new["random_rate_pct"],
                       "delta_pp": pm_new["delta_fd_minus_random_pp"], "mcnemar_p": pm_new["mcnemar_p"],
                       "co_delta_pp": co_new["delta_fd_minus_random_pp"]},
    }
    control["reproduce_676f"] = checks
    print(f"[677b-C] 对照重算完成（{time.perf_counter()-t0:.1f}s）："
          f"FD {pm_new['fd_rate_pct']}% vs Random {pm_new['random_rate_pct']}%，"
          f"Δ{pm_new['delta_fd_minus_random_pp']:+.2f}pp p={pm_new['mcnemar_p']:.4g}"
          f"（登记 FD {pm_reg['fd_rate_pct']}% / Δ{pm_reg['delta_fd_minus_random_pp']:+.2f}pp）", flush=True)
    if not all(v for k, v in checks.items() if k.endswith("match")):
        raise SystemExit("[677b-C] 原 split 对照重算与 676f 登记不一致 ⇒ fail-loud，终止")

    splits = [("family_random", SPLIT_RANDOM_OUT), ("family_stratified", SPLIT_STRAT_OUT),
              ("strict_stratified", ROOT / "data" / "677b_split_strict_stratified.json")]
    results = {}
    for name, path in splits:
        sdoc = _jload(path)
        mp = {s: v for s, v in zip(sdoc["derivation"], ["derivation"] * len(sdoc["derivation"]))}
        mp.update({s: "evaluation" for s in sdoc["evaluation"]})
        res = analyze_split(name, mp, samples, index, co_cands, degen)
        res["split_definition"] = {"seed": sdoc.get("seed"), "meta": sdoc["meta"]["strategy"],
                                   "unit_definition": sdoc["meta"]["unit_definition"],
                                   "n_units": sdoc["meta"]["n_units"],
                                   "validation": sdoc["meta"]["validation"]}
        results[name] = res
        p = res["primary_main_8candidates"]["primary"]
        c = res["co_primary_excl_degenerate"]["primary"]
        print(f"[677b-C] {name}: 主 k=4 FD {p['fd_rate_pct']}% vs Random {p['random_rate_pct']}% "
              f"Δ{p['delta_fd_minus_random_pp']:+.2f}pp p={p['mcnemar_p']:.4g}；"
              f"并列(5候选) Δ{c['delta_fd_minus_random_pp']:+.2f}pp p={c['mcnemar_p']:.4g}", flush=True)

    for (name, path), out_path in zip(splits, [RES_RANDOM_OUT, RES_STRAT_OUT,
                                               ROOT / "data" / "677b_a5_results_strict_stratified.json"]):
        doc = {
            "schema": "queyi-677b-a5-results/v1",
            "generated_by": "tools/analyze_677b_clone_aware.py a5",
            "generated_at": _now(),
            "split": name,
            "inputs": {"manifest": "data/a5_676f_sample_manifest.json",
                       "matrix": "data/a5_676f_detection_matrix.json",
                       "split_file": f"data/{Path(path).name}",
                       "note": "判定矩阵复用 676f（未重跑 detect）；检测器未改动"},
            "design": {"primary_k": PRIMARY_K, "sweep_k": list(KS), "random_arm_seed": SEED_ARM,
                       "multi_seed_runs": MULTI, "candidates": ASSETS,
                       "co_primary_candidates": co_cands,
                       "fd_fail_hits_source": f"派生集（n={results[name]['n_derivation']}）——不含评估集信息",
                       "statistics": "与 676f 相同原语：exact McNemar + McNemar 口径 Δ CI + Clopper-Pearson + Cohen's h"},
            "control_reproduction_original_split": control,
            "results": results[name],
            "honest_notes": [
                "判定矩阵复用 676f（1137×8，detector_sha256_16 见矩阵元数据），本批未重跑 detect()。",
                "FD 的 fail_hits 只来自本 split 的派生集 ⇒ FD 不是 oracle。",
                "k 扫描与子组分析为探索性：子组 p 附 BH-FDR/Bonferroni，未校正的原始 p 不得单独宣称显著。",
                "两种 family-aware split（random/stratified）与 strict 变体并排；原 split 结果原样保留为对照。",
            ],
        }
        _jwrite(out_path, doc)
    print(f"[677b-C] 写结果文件（3 个）（墙钟 {time.perf_counter()-t0:.1f}s）", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 阶段 D：cluster bootstrap（按家族/单位重采样）
# ─────────────────────────────────────────────────────────────────────────────
SEED_BOOT = 6771          # bootstrap 重采样种子（与 split 种子一致，可复现）
N_BOOT = 2000             # 与 676f random runs 一致；卡允许降到 1000（未降）


def _pct(sorted_arr: list[float], q: float) -> float:
    if not sorted_arr:
        return float("nan")
    i = int(round(q * (len(sorted_arr) - 1)))
    return sorted_arr[min(len(sorted_arr) - 1, max(0, i))]


def bootstrap_split(name: str, sample_split: dict[str, str], units: dict[str, list[str]],
                    index: dict, co_cands: list[str], n_reps: int = N_BOOT,
                    mode: str = "full_refit", frozen: dict | None = None) -> dict:
    """mode="full_refit"：每 replicate 重抽 Random 臂 + 重排 FD（含选臂方差）；
    mode="frozen"：冻结两条臂的资产集（= 论文报告的 Δ 所对应的固定对照），只重采样数据。"""
    unit_ids = sorted(units)
    side_of: dict[str, str] = {}
    ids_of: dict[str, list[dict[str, str]]] = {}
    for uid, members in units.items():
        sides = {sample_split[m] for m in members}
        if len(sides) != 1:
            raise ValueError(f"{name}: 单位 {uid} 跨 side ⇒ fail-loud")
        side_of[uid] = sides.pop()
        ids_of[uid] = [{"id": m} for m in members]
    ex = a5.AttributionExecutor(index)

    fd_rates, rn_rates, deltas, co_deltas, n_evs = [], [], [], [], []
    fd_asset_counts: dict[str, int] = collections.Counter()
    co_asset_counts: dict[str, int] = collections.Counter()
    fz = frozen or {}
    fd_frozen_assets = tuple(fz["fd_assets"]) if fz.get("fd_assets") else None
    rn_frozen_assets = tuple(fz["random_assets"]) if fz.get("random_assets") else None
    co_fd_frozen = tuple(fz["co_fd_assets"]) if fz.get("co_fd_assets") else None
    co_rn_frozen = tuple(fz["co_random_assets"]) if fz.get("co_random_assets") else None
    for rep in range(n_reps):
        rnd = random.Random(SEED_BOOT + rep)
        der_rows: list[dict] = []
        ev_rows: list[dict] = []
        for _ in range(len(unit_ids)):
            uid = unit_ids[rnd.randrange(len(unit_ids))]
            (der_rows if side_of[uid] == "derivation" else ev_rows).extend(ids_of[uid])
        if not der_rows or not ev_rows:
            continue
        n = len(ev_rows)
        fd_assets: tuple[str, ...]
        rn_assets: tuple[str, ...]
        co_fd_assets: tuple[str, ...]
        co_rn_assets: tuple[str, ...]
        if mode == "frozen":
            fd_assets = fd_frozen_assets or ()
            rn_assets = rn_frozen_assets or ()
            co_fd_assets = co_fd_frozen or ()
            co_rn_assets = co_rn_frozen or ()
        else:
            fh = a5.fail_hits_real(der_rows, ASSETS, index)
            fd_assets = tuple(ss.select("failure_driven", vp.ASSET_POOL, max_assets=PRIMARY_K,
                                        fail_hits={a: int(fh.get(a, 0)) for a in ASSETS},
                                        candidates=ASSETS).assets)
            rn_assets = tuple(ss.select("random", vp.ASSET_POOL, max_assets=PRIMARY_K,
                                        seed=SEED_ARM + rep, candidates=ASSETS).assets)
            co_fh = {a: int(fh.get(a, 0)) for a in co_cands}
            co_fd_assets = tuple(ss.select("failure_driven", vp.ASSET_POOL, max_assets=PRIMARY_K,
                                           fail_hits=co_fh, candidates=co_cands).assets)
            co_rn_assets = tuple(ss.select("random", vp.ASSET_POOL, max_assets=PRIMARY_K,
                                           seed=SEED_ARM + rep, candidates=co_cands).assets)
        fd_k = sum(1 for r in ev_rows if ex.verdict(r, fd_assets) == "catch")
        rn_k = sum(1 for r in ev_rows if ex.verdict(r, rn_assets) == "catch")
        fd_rates.append(fd_k / n)
        rn_rates.append(rn_k / n)
        deltas.append((fd_k - rn_k) / n)
        for a in fd_assets:
            fd_asset_counts[a] += 1
        co_fd_k = sum(1 for r in ev_rows if ex.verdict(r, co_fd_assets) == "catch")
        co_rn_k = sum(1 for r in ev_rows if ex.verdict(r, co_rn_assets) == "catch")
        co_deltas.append((co_fd_k - co_rn_k) / n)
        for a in co_fd_assets:
            co_asset_counts[a] += 1
        n_evs.append(n)

    def _sum(arr: list[float]) -> dict:
        s = sorted(arr)
        mean = sum(arr) / len(arr)
        var = sum((x - mean) ** 2 for x in arr) / (len(arr) - 1)
        return {
            "mean": round(mean, 6), "sd": round(var ** 0.5, 6),
            "ci95_percentile": [round(_pct(s, 0.025), 6), round(_pct(s, 0.975), 6)],
            "min": round(min(arr), 6), "max": round(max(arr), 6),
            "p025": round(_pct(s, 0.025), 6), "p50": round(_pct(s, 0.5), 6),
            "p975": round(_pct(s, 0.975), 6),
        }

    d = _sum(deltas)
    p_le0 = sum(1 for x in deltas if x <= 0) / len(deltas)
    p_ge0 = sum(1 for x in deltas if x >= 0) / len(deltas)
    co = _sum(co_deltas)
    reps = len(deltas)
    return {
        "split": name, "n_replicates": reps, "seed": SEED_BOOT, "mode": mode,
        "frozen_arms": ({"fd_assets": list(fd_frozen_assets or ()),
                         "random_assets": list(rn_frozen_assets or ()),
                         "co_fd_assets": list(co_fd_frozen or ()),
                         "co_random_assets": list(co_rn_frozen or ())} if mode == "frozen" else None),
        "resampling_unit": "split 单位（家族/连通分量）——有放回抽 N 个单位（N=单位总数），单位内全部样本随行",
        "n_units": len(unit_ids),
        "fd_rate": _sum(fd_rates), "random_rate": _sum(rn_rates), "delta_fd_random": d,
        "co_primary_delta_fd_random": co,
        "delta_p_le_0_frac": round(p_le0, 6), "delta_p_ge_0_frac": round(p_ge0, 6),
        "delta_p_two_sided_boot": round(min(1.0, 2 * min(p_le0, p_ge0)), 6),
        "n_evaluation_per_replicate": {"mean": round(sum(n_evs) / len(n_evs), 3),
                                       "min": min(n_evs), "max": max(n_evs)},
        "fd_asset_selection_counts": dict(sorted(fd_asset_counts.items(), key=lambda kv: -kv[1])),
        "co_primary_asset_selection_counts": dict(sorted(co_asset_counts.items(), key=lambda kv: -kv[1])),
        "arrays": {"fd_rate": [round(x, 6) for x in fd_rates],
                   "random_rate": [round(x, 6) for x in rn_rates],
                   "delta": [round(x, 6) for x in deltas],
                   "co_primary_delta": [round(x, 6) for x in co_deltas]},
    }


def stage_bootstrap() -> int:
    t0 = time.perf_counter()
    famdoc = _jload(FAMILIES_OUT)
    matrix = _jload(MATRIX)
    index = index_of(matrix)
    man = _jload(MANIFEST)
    co_cands, _deg = co_primary_candidates(man["samples"], index)

    jobs = [
        ("family_stratified", SPLIT_STRAT_OUT, famdoc["family_index"], RES_STRAT_OUT),
        ("strict_stratified", ROOT / "data" / "677b_split_strict_stratified.json",
         famdoc["split_units"]["index"],
         ROOT / "data" / "677b_a5_results_strict_stratified.json"),
    ]
    out = {}
    for name, path, units, res_path in jobs:
        sdoc = _jload(path)
        ssmap = {}
        ssmap.update({s: "derivation" for s in sdoc["derivation"]})
        ssmap.update({s: "evaluation" for s in sdoc["evaluation"]})
        res = _jload(res_path)["results"]
        frozen = {
            "fd_assets": res["primary_main_8candidates"]["primary"]["fd_assets"],
            "random_assets": res["primary_main_8candidates"]["primary"]["random_assets"],
            "co_fd_assets": res["co_primary_excl_degenerate"]["primary"]["fd_assets"],
            "co_random_assets": res["co_primary_excl_degenerate"]["primary"]["random_assets"],
        }
        print(f"[677b-D] {name}: cluster bootstrap {N_BOOT} 次 × 2 模式（单位={len(units)}）…",
              flush=True)
        out[name] = {
            "full_refit": bootstrap_split(name, ssmap, units, index, co_cands, mode="full_refit"),
            "frozen_arms": bootstrap_split(name, ssmap, units, index, co_cands, mode="frozen",
                                           frozen=frozen),
        }

    doc = {
        "schema": "queyi-677b-cluster-bootstrap/v1",
        "generated_by": "tools/analyze_677b_clone_aware.py bootstrap",
        "generated_at": _now(),
        "design": {
            "replicates": N_BOOT, "seed": SEED_BOOT, "primary_k": PRIMARY_K,
            "candidates": ASSETS, "co_primary_candidates": co_cands,
            "two_modes": {
                "full_refit": "每 replicate 重排 FD（用重采样派生集）+ 重抽 Random 臂 ⇒ 含选臂方差，"
                              "回答「换一次抽样/换一个随机臂，结论会不会变」",
                "frozen_arms": "冻结两臂资产集（= 论文报告的 Δ 对应的固定对照，单点 seed 与 FD 选集都可从"
                               "结果 JSON 复核），只重采样数据 ⇒ 直接给出**报告量 Δ 的 cluster CI**",
            },
            "caveat": "单位大小不等 ⇒ 重采样后评估集样本数在 replicate 间波动（n_evaluation_per_replicate 已记录）；"
                      "cluster bootstrap 的方差同时含组内相关与规模变动两部分",
        },
        "results": out,
    }
    _jwrite(BOOT_OUT, doc)
    print(f"[677b-D] 完成（{time.perf_counter()-t0:.1f}s）；写 {BOOT_OUT.name}", flush=True)
    return 0


def stage_tables() -> int:
    """三种 split 并排对比表 + CI 对比表（读已落盘结果生成，不重算）。"""
    docs = {"original(676f 原 split)": _jload(ROOT / "data" / "a5_676f_results.json")}
    for name, path in (("family_random", RES_RANDOM_OUT), ("family_stratified", RES_STRAT_OUT),
                       ("strict_stratified", ROOT / "data" / "677b_a5_results_strict_stratified.json")):
        docs[name] = _jload(path)

    def inner(doc):
        return doc["results"] if "results" in doc else doc

    def sizes_of(r) -> tuple:
        if "n_derivation" in r:
            return r["n_derivation"], r["n_evaluation"]
        st = r["sample_stats"]
        return st["n_derivation"], st["n_evaluation"]

    def block_of(doc, which):
        r = inner(doc)
        if which == "main":
            return r["primary_main_8candidates"]["primary"], *sizes_of(r)
        return r["co_primary_excl_degenerate"]["primary"], *sizes_of(r)

    def byk_of(doc, which):
        r = inner(doc)
        key = "primary_main_8candidates" if which == "main" else "co_primary_excl_degenerate"
        return r[key]["by_k_compact"]

    FACETS = ("subgroups_defect_group", "subgroups_defect_type", "subgroups_planted", "subgroups_batch")

    def facets_of(doc) -> dict:
        """统一 facet 视图：677b 结果文件直接用；676f 原文件做等价映射（缺的记空）。"""
        r = inner(doc)
        if "subgroups_defect_group" in r:
            return {f: r[f]["blocks"] for f in FACETS}
        return {
            "subgroups_defect_group": r.get("subgroups", {}),
            "subgroups_defect_type": {},
            "subgroups_planted": {"planted=True": r.get("planted_true"),
                                  "planted=False": r.get("planted_false")},
            "subgroups_batch": {},
        }

    L = []
    L.append("# 677b · 任务C：A5 重算结果并排对比（原 split vs 三种 clone-aware split）\n")
    L.append(f"- 生成：`tools/analyze_677b_clone_aware.py tables`（{_now()}）")
    L.append("- 判定矩阵与检测器：**复用 676f**（1137×8 判定），本批未重跑 detect()，未改检测器")
    L.append("- 统计原语与 676f/673p 完全相同（exact McNemar、McNemar 口径 Δ CI、Clopper–Pearson、2000 次 Random 分布）")
    L.append("- 三种 clone-aware split 的构造见 `data/677b_split_comparison.md`；原 split 列为对照\n")

    L.append("## 1. 主分析 k=4（8 候选资产）\n")
    L.append("| split | 派生/评估 n | FD 检出率 | Random 检出率 | Δ(FD−Random) | Δ 95%CI | McNemar p | FD 严格优于随机的比例* | Static 检出率 | Δ(FD−Static) |")
    L.append("|---|---:|---:|---:|---:|---|---:|---:|---:|---:|")
    for name, doc in docs.items():
        p, nd, ne = block_of(doc, "main")
        L.append(f"| {name} | {nd}/{ne} | {p['fd_rate_pct']}% | {p['random_rate_pct']}% | "
                 f"**{p['delta_fd_minus_random_pp']:+.2f}pp** | {p['delta_ci95_pp']} | {p['mcnemar_p']:.4g} | "
                 f"{p['random_2000']['fd_strictly_better_frac']*100:.1f}% | {p['static_rate_pct']}% | "
                 f"{p['delta_fd_minus_static_pp']:+.2f}pp |")
    L.append("\n*「FD 严格优于随机的比例」= 2000 次随机 k=4 抽样中 FD 的 catch 数严格更高的比例。\n")

    L.append("## 2. 并列分析 k=4（剔除退化资产后的 5 候选：asan / compiler-warn / cross-compile / tsan / ubsan）\n")
    L.append("| split | FD 检出率 | Random 检出率 | Δ(FD−Random) | Δ 95%CI | McNemar p | Δ(FD−Static) |")
    L.append("|---|---:|---:|---:|---|---:|---:|")
    for name, doc in docs.items():
        p, _nd, _ne = block_of(doc, "co")
        L.append(f"| {name} | {p['fd_rate_pct']}% | {p['random_rate_pct']}% | "
                 f"**{p['delta_fd_minus_random_pp']:+.2f}pp** | {p['delta_ci95_pp']} | {p['mcnemar_p']:.4g} | "
                 f"{p['delta_fd_minus_static_pp']:+.2f}pp |")
    L.append("")

    for which, label in (("main", "主分析（8 候选）"), ("co", "并列分析（5 候选）")):
        L.append(f"## {'3' if which == 'main' else '4'}. k=1~4 的 Δ(FD−Random)（{label}）\n")
        L.append("| k | " + " | ".join(docs) + " |")
        L.append("|---:|" + "---:|" * len(docs))
        for k in KS:
            cells = []
            for name, doc in docs.items():
                row = next((x for x in byk_of(doc, which) if x["k"] == k), None)
                cells.append(f"{row['delta_fd_minus_random_pp']:+.2f}pp (p={row['mcnemar_p']:.3g})" if row else "—")
            L.append(f"| k={k} | " + " | ".join(cells) + " |")
        L.append("")

    L.append("## 5. 子组 Δ(FD−Random)（k=4，主分析；括号=评估集 n；p 为未校正 McNemar，q 见结果 JSON）\n")
    for facet in FACETS:
        L.append(f"### 5.{FACETS.index(facet)+1} {facet}\n")
        blocks = {n: facets_of(d)[facet] for n, d in docs.items()}
        keys = sorted({k for b in blocks.values() for k in b})
        tested = [k for k in keys if any(isinstance(blocks[n].get(k), dict)
                                         and "mcnemar_p" in (blocks[n].get(k) or {}) for n in docs)]
        L.append("| 组 | " + " | ".join(docs) + " |")
        L.append("|---|" + "---:|" * len(docs))
        for k in tested:
            cells = []
            for name in docs:
                b = blocks[name].get(k)
                if not isinstance(b, dict) or "mcnemar_p" not in b:
                    cells.append("—")
                else:
                    cells.append(f"{b['delta_fd_minus_random_pp']:+.2f}pp (n={b['n_evaluation']}, "
                                 f"p={b['mcnemar_p']:.3g})")
            L.append(f"| {k} | " + " | ".join(cells) + " |")
        L.append("")

    L.append("## 6. 原 split 对照重算核对（管线正确性）\n")
    ctrl = _jload(RES_STRAT_OUT)["control_reproduction_original_split"]["reproduce_676f"]
    L.append(f"- 676f 登记：FD {ctrl['registered']['fd_rate_pct']}%，Random {ctrl['registered']['random_rate_pct']}%，"
             f"Δ{ctrl['registered']['delta_pp']:+.2f}pp，p={ctrl['registered']['mcnemar_p']:.4g}")
    L.append(f"- 677b 重算：FD {ctrl['recomputed']['fd_rate_pct']}%，Random {ctrl['recomputed']['random_rate_pct']}%，"
             f"Δ{ctrl['recomputed']['delta_pp']:+.2f}pp，p={ctrl['recomputed']['mcnemar_p']:.4g}")
    L.append(f"- 逐位一致：FD {ctrl['fd_rate_match']}、Random {ctrl['random_rate_match']}、"
             f"Δ {ctrl['delta_match']}、p {ctrl['mcnemar_p_match']}、并列 Δ {ctrl['co_delta_match']}\n")
    _md_write(COMPARISON_MD, "\n".join(L))

    # CI 对比表
    boot = _jload(BOOT_OUT) if BOOT_OUT.is_file() else None
    C = []
    C.append("# 677b · 任务D：普通 CI vs Cluster Bootstrap CI\n")
    C.append(f"- 生成：`tools/analyze_677b_clone_aware.py tables`（{_now()}）；bootstrap 次数 "
             f"{boot['design']['replicates'] if boot else 'NA'}，seed={SEED_BOOT}")
    C.append("- 普通 CI = 676f 口径（Clopper–Pearson 单臂率 + McNemar 口径 Wald Δ CI，假设样本独立）；"
             "cluster CI = 按分裂单位有放回重采样 2000 次的 percentile CI")
    C.append("- 两种 bootstrap 模式：**frozen_arms**（冻结两臂资产集 ⇒ 报告量 Δ 的 CI）/ "
             "**full_refit**（每 replicate 重排 FD + 重抽 Random ⇒ 含选臂方差，回答「换个随机臂会不会翻盘」）\n")
    if boot:
        for name, res_path in (("family_stratified", RES_STRAT_OUT),
                               ("strict_stratified", ROOT / "data" / "677b_a5_results_strict_stratified.json")):
            bf = boot["results"][name]["frozen_arms"]
            br = boot["results"][name]["full_refit"]
            res = _jload(res_path)["results"]
            p = res["primary_main_8candidates"]["primary"]
            cod = res["co_primary_excl_degenerate"]["primary"]
            n = p["n"]
            C.append(f"## {name}（评估 n={n}，分裂单位 {bf['n_units']} 个）\n")
            lo, hi = a5.cp_interval(p["fd_k"], n)
            if lo is None or hi is None:
                raise ValueError("cp_interval 返回 None（k/n 不完整）")
            lo_f, hi_f = float(lo), float(hi)
            w_naive = (hi_f - lo_f) * 100
            ci_f0 = float(bf["fd_rate"]["ci95_percentile"][0])
            ci_f1 = float(bf["fd_rate"]["ci95_percentile"][1])
            w_f = (ci_f1 - ci_f0) * 100
            C.append(f"- FD 检出率：点估计 {p['fd_rate_pct']}%；普通 CP95 [{lo_f*100:.2f}, {hi_f*100:.2f}]"
                     f"（宽 {w_naive:.2f}pp）；cluster(frozen) 95% "
                     f"[{ci_f0*100:.2f}, "
                     f"{ci_f1*100:.2f}]（宽 {w_f:.2f}pp）")
            d_naive = p["delta_ci95_pp"]
            w_dn = d_naive[1] - d_naive[0]
            w_df = (bf["delta_fd_random"]["ci95_percentile"][1]
                    - bf["delta_fd_random"]["ci95_percentile"][0]) * 100
            w_dr = (br["delta_fd_random"]["ci95_percentile"][1]
                    - br["delta_fd_random"]["ci95_percentile"][0]) * 100
            C.append(f"- Δ(FD−Random)：点估计 {p['delta_fd_minus_random_pp']:+.2f}pp；普通 95%CI {d_naive}"
                     f"（宽 {w_dn:.2f}pp）")
            C.append(f"  - cluster(frozen) 95% [{bf['delta_fd_random']['ci95_percentile'][0]*100:+.2f}, "
                     f"{bf['delta_fd_random']['ci95_percentile'][1]*100:+.2f}]pp（宽 {w_df:.2f}pp，"
                     f"{w_df/w_dn:.2f}× 普通）；Δ≤0 比例 {bf['delta_p_le_0_frac']}")
            C.append(f"  - cluster(full_refit) 95% [{br['delta_fd_random']['ci95_percentile'][0]*100:+.2f}, "
                     f"{br['delta_fd_random']['ci95_percentile'][1]*100:+.2f}]pp（宽 {w_dr:.2f}pp，"
                     f"{w_dr/w_dn:.2f}× 普通）；Δ≤0 比例 {br['delta_p_le_0_frac']}")
            C.append(f"  - Random 臂自身的不确定性（cluster CI 宽 "
                     f"{(bf['random_rate']['ci95_percentile'][1]-bf['random_rate']['ci95_percentile'][0])*100:.2f}pp）"
                     f"是 full_refit 宽 CI 的主因 ⇒ 报告量 Δ 用 frozen 口径")
            ph = p["fd_rate_pct"] / 100
            se_naive = math.sqrt(ph * (1 - ph) / n)
            deff = (bf["fd_rate"]["sd"] / se_naive) ** 2 if se_naive else None
            C.append(f"- 设计效应（FD 率）：cluster SD {bf['fd_rate']['sd']*100:.2f}pp vs 独立假设 SE "
                     f"{se_naive*100:.2f}pp ⇒ deff≈{deff:.2f}，有效样本量≈{n/deff:.0f}（名义 n={n}）")
            C.append(f"- 并列（5 候选）：点估计 Δ {cod['delta_fd_minus_random_pp']:+.2f}pp；"
                     f"cluster(frozen) Δ 95% "
                     f"[{bf['co_primary_delta_fd_random']['ci95_percentile'][0]*100:+.2f}, "
                     f"{bf['co_primary_delta_fd_random']['ci95_percentile'][1]*100:+.2f}]pp；"
                     f"全重算 {bf['co_primary_delta_fd_random']['mean']*100:+.2f}pp（均值）")
            C.append(f"- 每 replicate 评估样本数：均值 {bf['n_evaluation_per_replicate']['mean']}，"
                     f"范围 [{bf['n_evaluation_per_replicate']['min']}, {bf['n_evaluation_per_replicate']['max']}]"
                     f"（单位大小不等所致，已如实记录）")
            C.append(f"- frozen 模式冻结的臂：FD {bf['frozen_arms']['fd_assets']}；"
                     f"Random {bf['frozen_arms']['random_assets']}")
            C.append(f"- full_refit 下 FD 资产被选中频次（前 5）："
                     f"{list(br['fd_asset_selection_counts'].items())[:5]}")
            C.append(f"- full_refit 下并列 FD 资产被选中频次："
                     f"{list(br['co_primary_asset_selection_counts'].items())}\n")
    else:
        C.append("- bootstrap 结果缺失，先跑 `--stage bootstrap`")
    _md_write(CI_MD, "\n".join(C))
    print(f"[677b] 写 {COMPARISON_MD.name} / {CI_MD.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI + 落盘回读校验
# ─────────────────────────────────────────────────────────────────────────────
ARTIFACTS = [FAMILIES_OUT, FAMILY_REPORT, SPLIT_RANDOM_OUT, SPLIT_STRAT_OUT,
             ROOT / "data" / "677b_split_strict_stratified.json", SPLIT_REPORT,
             RES_RANDOM_OUT, RES_STRAT_OUT, ROOT / "data" / "677b_a5_results_strict_stratified.json",
             COMPARISON_MD, BOOT_OUT, CI_MD]


def verify_artifacts() -> int:
    bad = []
    for p in ARTIFACTS:
        if not p.is_file():
            bad.append((p.name, "missing"))
            continue
        raw = p.read_text(encoding="utf-8")
        if p.suffix == ".json":
            try:
                json.loads(raw)
            except json.JSONDecodeError as e:
                bad.append((p.name, f"json error: {e}"))
                continue
        if len(raw) < 100:
            bad.append((p.name, "too small"))
    if bad:
        print(f"[677b] 落盘回读校验失败：{bad}", flush=True)
        return 1
    print(f"[677b] 落盘回读校验通过（{len(ARTIFACTS)} 个产物可解析）", flush=True)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="677b clone-aware A5 重跑")
    ap.add_argument("--stage", default="all",
                    choices=["families", "splits", "a5", "bootstrap", "tables", "verify", "all"])
    a = ap.parse_args(argv)
    stages = {"families": stage_families, "splits": stage_splits, "a5": stage_a5,
              "bootstrap": stage_bootstrap, "tables": stage_tables}
    if a.stage == "all":
        for fn in (stage_families, stage_splits, stage_a5, stage_bootstrap, stage_tables, verify_artifacts):
            rc = fn()
            if rc:
                return rc
        return 0
    if a.stage == "verify":
        return verify_artifacts()
    rc = stages[a.stage]()
    if rc:
        return rc
    return verify_artifacts() if a.stage == "tables" else 0


if __name__ == "__main__":
    raise SystemExit(main())
