#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_676k_dedup.py — 676k 任务A：跨批次语义去重（三层）。

只读审计：不修改任何样本数据。三层去重：
  L1 精确：每个样本源文件字节 md5（多文件按文件名排序拼接后再 md5）；标注 .json md5。
  L2 归一化：去注释 / 去空白 / 标识符→ID / 数字→NUM / 字符串→STR，再 sha256。
  L3 语义：defect_type 分组内，token TF-IDF（sublinear tf，idf=ln(N/df)+1）余弦相似度。

数据来源（权威清单）：
  data/blindspot_676g_sample_manifest.json  —— 1147 条（holdout 41 + corpus 64 + expA..expG 1042）
  样本文件位置由清单的 dir/files 给出；扩展批次的标注在 data/holdout_expansion/<batch>/*.json。

诚实边界：
  - corpus 批次 64 条为 input_mode=code_materialized，磁盘无源文件 → 文本层（L1/L2/L3）无法覆盖，
    仅用 data/a5_676f_sample_manifest.json 的 content_md5 做登记层比对，并如实计入覆盖率。
  - L3 阈值 0.9 为经验值，可能漏网或误报。

用法：
  python tools/audit_676k_dedup.py                # 人类可读摘要
  python tools/audit_676k_dedup.py --json OUT     # 写机器可读结果
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import re
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLINDSPOT = os.path.join(ROOT, "data", "blindspot_676g_sample_manifest.json")
A5MANIFEST = os.path.join(ROOT, "data", "a5_676f_sample_manifest.json")
EXPDIR = os.path.join(ROOT, "data", "holdout_expansion")

EXP_BATCHES = ["expA", "expB", "expC", "expD", "expE", "expF", "expG"]
ALL_BATCHES = ["holdout", "corpus"] + EXP_BATCHES
SEM_THRESHOLD = 0.90
TOP_N = 20

CPP_KEYWORDS = {
    "alignas", "alignof", "and", "asm", "auto", "bool", "break", "case", "catch", "char",
    "class", "const", "constexpr", "const_cast", "continue", "decltype", "default", "delete",
    "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false",
    "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace",
    "new", "noexcept", "not", "nullptr", "operator", "or", "private", "protected", "public",
    "register", "reinterpret_cast", "return", "short", "signed", "sizeof", "static",
    "static_assert", "static_cast", "struct", "switch", "template", "this", "throw", "true",
    "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void",
    "volatile", "while", "xor", "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t",
    "uint16_t", "uint32_t", "uint64_t", "size_t", "std", "string", "vector", "thread", "atomic",
    "memory_order_relaxed", "memory_order_acquire", "memory_order_release",
    "memory_order_seq_cst", "memory_order_acq_rel", "memory_order_consume",
}


# --------------------------------------------------------------------------- #
# 归一化
# --------------------------------------------------------------------------- #
def strip_comments_and_literals(src: str) -> str:
    """状态机：去 // 与 /* */ 注释，并把字符串/字符字面量替换为占位符。"""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":
            while i < n and src[i] != "\n":
                i += 1
        elif c == "/" and nxt == "*":
            i += 2
            while i + 1 < n and not (src[i] == "*" and src[i + 1] == "/"):
                i += 1
            i += 2
        elif c == '"':
            # 普通字符串（含转义）；raw 字符串少见，按普通处理并如实接受偏差
            i += 1
            while i < n and src[i] != '"':
                i += 2 if src[i] == "\\" else 1
            i += 1
            out.append(" STR ")
        elif c == "'":
            i += 1
            while i < n and src[i] != "'":
                i += 2 if src[i] == "\\" else 1
            i += 1
            out.append(" CHR ")
        else:
            out.append(c)
            i += 1
    return "".join(out)


_ID_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_NUM_RE = re.compile(r"\b(?:0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][+-]?\d+)?[fFuUlL]*)\b")
_PREPROC_RE = re.compile(r"^[ \t]*#.*$", re.MULTILINE)


def normalize(src: str) -> str:
    """去注释/字面量 → 去预处理指令 → 标识符归一化 → 去空白。"""
    t = strip_comments_and_literals(src)
    t = _PREPROC_RE.sub(" ", t)

    def _id(m: re.Match) -> str:
        return m.group(0) if m.group(0) in CPP_KEYWORDS else "ID"

    t = _ID_RE.sub(_id, t)
    t = _NUM_RE.sub("NUM", t)
    t = re.sub(r"\s+", "", t)
    return t


_NUM_TOK_RE = re.compile(r"0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][+-]?\d+)?[fFuUlL]*")
_OP_RE = re.compile(r"[{}()\[\];,.<>=!+\-*/%&|^~?:]+")
# 单次扫描：标识符优先（int8_t 整体成 token，不被数字切碎），其次数字，其次运算符
_TOK_RE = re.compile(
    r"[A-Za-z_][A-Za-z_0-9]*"
    r"|0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][+-]?\d+)?[fFuUlL]*"
    r"|[{}()\[\];,.<>=!+\-*/%&|^~?:]+"
)


def tokenize(src: str) -> list[str]:
    """语义层 token：注释/字面量已处理；标识符与**数字字面量**均保留原形。

    保留数字是刻意的：否则「p[0]」与「p[7]」这类仅常量不同的近克隆会被算成完全一致，
    相似度被人为抬高。保留后仍 ≥0.9 的对才是真正值得人工复核的近克隆。
    """
    t = strip_comments_and_literals(src)
    t = _PREPROC_RE.sub(" ", t)
    return _TOK_RE.findall(t)


# --------------------------------------------------------------------------- #
# 数据装载
# --------------------------------------------------------------------------- #
def to_a5_id(batch: str, sample_id: str) -> str:
    """把 blindspot 清单的 sample_id 映射到 A5 清单的 sample_id（两清单命名体系不同）。

    实证映射（逐批核对过）：
      expA sample_001 -> A001 ；expB sample_B001 -> B001 ；expC sample_001 -> C001
      expD D001 -> D001        ；expE sample_E001 -> E001 ；expF F001 -> F001
      expG sample_G001 -> G001 ；holdout h41 -> h41        ；corpus d3-08 -> d3-08
    """
    s = sample_id
    if batch == "expA":
        return "A" + s[len("sample_"):]
    if batch == "expB":
        return s[len("sample_"):]
    if batch == "expC":
        return "C" + s[len("sample_"):]
    if batch == "expD":
        return s
    if batch == "expE":
        return s[len("sample_"):]
    if batch == "expF":
        return s
    if batch == "expG":
        return s[len("sample_"):]
    return s


def load_samples() -> list[dict]:
    bs = json.load(open(BLINDSPOT, encoding="utf-8"))
    a5 = json.load(open(A5MANIFEST, encoding="utf-8"))
    a5_md5 = {s["sample_id"]: s.get("content_md5") for s in a5["samples"]}

    samples = []
    for e in bs["samples"]:
        batch = e["source_batch"]
        d = e.get("dir") or ""
        files = e.get("files") or []
        cpp = []
        for f in files:
            p = os.path.join(ROOT, d, f) if d else os.path.join(ROOT, f)
            if os.path.exists(p):
                try:
                    cpp.append((f, open(p, encoding="utf-8", errors="replace").read()))
                except OSError:
                    pass
        rec = {
            "uid": e["uid"],
            "sample_id": e["sample_id"],
            "batch": batch,
            "defect_type": e.get("defect_type"),
            "planted": e.get("planted"),
            "expected_verdict": e.get("expected_verdict"),
            "dir": d,
            "files": files,
            "n_cpp": len(cpp),
            "has_source": bool(cpp),
            "a5_id": to_a5_id(batch, e["sample_id"]),
        }
        rec["content_md5_a5"] = a5_md5.get(rec["a5_id"])
        if cpp:
            cpp_sorted = sorted(cpp, key=lambda x: x[0])
            joined = "\n".join(t for _, t in cpp_sorted)
            rec["src_text"] = joined
            rec["exact_md5"] = hashlib.md5(joined.encode("utf-8", "replace")).hexdigest()
            rec["norm_sha256"] = hashlib.sha256(
                normalize(joined).encode("utf-8", "replace")
            ).hexdigest()
        else:
            rec["src_text"] = None
            rec["exact_md5"] = None
            rec["norm_sha256"] = None
        samples.append(rec)
    return samples


def load_annotations() -> dict:
    """扩展批次标注 .json 的 md5（按 <batch>/<file> 键）。"""
    out = {}
    for b in EXP_BATCHES:
        d = os.path.join(EXPDIR, b)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".json") and fn != "INDEX.json":
                p = os.path.join(d, fn)
                raw = open(p, "rb").read()
                out[f"{b}/{fn}"] = hashlib.md5(raw).hexdigest()
    return out


# --------------------------------------------------------------------------- #
# 三层
# --------------------------------------------------------------------------- #
def layer1(samples: list[dict], ann_md5: dict) -> dict:
    by_md5 = collections.defaultdict(list)
    for s in samples:
        if s["exact_md5"]:
            by_md5[s["exact_md5"]].append(s)
    cpp_dups = [
        {
            "md5": h,
            "members": [{"uid": x["uid"], "batch": x["batch"], "files": x["files"]} for x in v],
            "cross_batch": len({x["batch"] for x in v}) > 1,
        }
        for h, v in by_md5.items()
        if len(v) > 1
    ]
    cpp_dups.sort(key=lambda d: -len(d["members"]))

    by_ann = collections.defaultdict(list)
    for k, h in ann_md5.items():
        by_ann[h].append(k)
    ann_dups = [
        {"md5": h, "members": sorted(v)} for h, v in by_ann.items() if len(v) > 1
    ]
    ann_dups.sort(key=lambda d: -len(d["members"]))

    # 登记层：A5 content_md5
    by_a5 = collections.defaultdict(list)
    for s in samples:
        if s["content_md5_a5"]:
            by_a5[s["content_md5_a5"]].append(s)
    a5_dups = [
        {
            "content_md5": h,
            "members": [{"uid": x["uid"], "batch": x["batch"]} for x in v],
            "cross_batch": len({x["batch"] for x in v}) > 1,
        }
        for h, v in by_a5.items()
        if len(v) > 1
    ]
    a5_dups.sort(key=lambda d: -len(d["members"]))

    return {"cpp_groups": cpp_dups, "annotation_groups": ann_dups, "content_md5_groups": a5_dups}


def layer2(samples: list[dict]) -> dict:
    by_h = collections.defaultdict(list)
    for s in samples:
        if s["norm_sha256"]:
            by_h[s["norm_sha256"]].append(s)
    groups = [
        {
            "sha256": h,
            "members": [{"uid": x["uid"], "batch": x["batch"], "files": x["files"]} for x in v],
            "cross_batch": len({x["batch"] for x in v}) > 1,
        }
        for h, v in by_h.items()
        if len(v) > 1
    ]
    groups.sort(key=lambda d: -len(d["members"]))
    return {"groups": groups}


def _tfidf_vectors(docs: list[list[str]]) -> list[dict]:
    n = len(docs)
    df: collections.Counter[str] = collections.Counter()
    for d in docs:
        for t in set(d):
            df[t] += 1
    vecs = []
    for d in docs:
        tf = collections.Counter(d)
        v = {}
        for t, c in tf.items():
            sub = 1.0 + math.log(c)
            idf = math.log(n / df[t]) + 1.0
            v[t] = sub * idf
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs


def tokenize_structure(src: str) -> list[str]:
    """结构层 token：在 tokenize 基础上把数字字面量统一为 NUM。

    用途：跨批次「常量微调型近克隆」——如 `a[6]=1` 与 `a[10]=42` 是同一个缺陷模板，
    仅常量不同。保留数字会把这些对压到 0.9 以下而漏报，故结构层单独算一次。
    """
    return ["NUM" if _NUM_TOK_RE.fullmatch(t) else t for t in tokenize(src)]


def _cos(a: dict, b: dict) -> float:
    if len(a) > len(b):
        a, b = b, a
    return float(sum(w * b.get(t, 0.0) for t, w in a.items()))


def layer3(samples: list[dict]) -> dict:
    """defect_type 分组内 TF-IDF 余弦；跨组不算（分组与语义层要求一致）。"""
    groups = collections.defaultdict(list)
    for s in samples:
        if s["src_text"] is not None:
            groups[s["defect_type"] or "?"].append(s)

    pairs = []
    for dt, members in groups.items():
        if len(members) < 2:
            continue
        vecs = _tfidf_vectors([tokenize(m["src_text"]) for m in members])
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                c = _cos(vecs[i], vecs[j])
                if c >= SEM_THRESHOLD:
                    pairs.append(
                        {
                            "similarity": round(c, 6),
                            "defect_type": dt,
                            "a": {"uid": members[i]["uid"], "batch": members[i]["batch"]},
                            "b": {"uid": members[j]["uid"], "batch": members[j]["batch"]},
                            "same_batch": members[i]["batch"] == members[j]["batch"],
                        }
                    )
    pairs.sort(key=lambda p: -p["similarity"])
    return {"threshold": SEM_THRESHOLD, "n_pairs": len(pairs), "pairs": pairs}


def layer3b_structure(samples: list[dict]) -> dict:
    """结构层：常量归一后的 TF-IDF 余弦，**只统计跨批次对**（批次内近克隆另见 L2）。

    这是对「跨批次有没有重复」最直接的答案：同一缺陷模板换常量后跨批复用即为近克隆。
    """
    docs = {s["uid"]: tokenize_structure(s["src_text"]) for s in samples if s["src_text"]}
    uids = sorted(docs)
    vecs = _tfidf_vectors([docs[u] for u in uids])
    meta = {s["uid"]: s for s in samples}
    pairs = []
    for i in range(len(uids)):
        for j in range(i + 1, len(uids)):
            a, b = uids[i], uids[j]
            if meta[a]["batch"] == meta[b]["batch"]:
                continue
            c = _cos(vecs[i], vecs[j])
            if c >= SEM_THRESHOLD:
                pairs.append(
                    {
                        "similarity": round(c, 6),
                        "a": {"uid": a, "batch": meta[a]["batch"], "defect_type": meta[a]["defect_type"]},
                        "b": {"uid": b, "batch": meta[b]["batch"], "defect_type": meta[b]["defect_type"]},
                        "same_defect_type": meta[a]["defect_type"] == meta[b]["defect_type"],
                    }
                )
    pairs.sort(key=lambda p: -p["similarity"])
    return {"threshold": SEM_THRESHOLD, "n_cross_batch_pairs": len(pairs), "pairs": pairs}


# --------------------------------------------------------------------------- #
# 矩阵
# --------------------------------------------------------------------------- #
def batch_matrix(dup_groups: list[list[dict]]) -> dict:
    """按批次对统计重复对数（无序对，含同批）。"""
    m: collections.Counter[tuple[str, str]] = collections.Counter()
    for members in dup_groups:
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i]["batch"], members[j]["batch"]
                k = tuple(sorted([a, b]))
                m[k] += 1
    return {f"{a}|{b}": v for (a, b), v in sorted(m.items())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="写机器可读结果到该路径")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    samples = load_samples()
    ann_md5 = load_annotations()

    l1 = layer1(samples, ann_md5)
    l2 = layer2(samples)
    l3 = layer3(samples)
    l3b = layer3b_structure(samples)

    by_batch = collections.Counter(s["batch"] for s in samples)
    covered = collections.Counter(s["batch"] for s in samples if s["has_source"])
    n_covered = sum(covered.values())

    result: dict[str, Any] = {
        "schema": "queyi-audit-676k-dedup/v1",
        "generated_by": "tools/audit_676k_dedup.py",
        "source_manifest": "data/blindspot_676g_sample_manifest.json",
        "n_total": len(samples),
        "by_batch": dict(by_batch),
        "n_text_covered": n_covered,
        "by_batch_covered": dict(covered),
        "n_uncovered_no_source": len(samples) - n_covered,
        "n_a5_id_matched": sum(1 for s in samples if s["content_md5_a5"]),
        "n_dup_sample_id_collisions": len(
            [k for k, v in collections.Counter(s["sample_id"] for s in samples).items() if v > 1]
        ),
        "layer1_exact": {
            "cpp_dup_groups": len(l1["cpp_groups"]),
            "cpp_dup_samples": sum(len(g["members"]) for g in l1["cpp_groups"]),
            "annotation_dup_groups": len(l1["annotation_groups"]),
            "content_md5_dup_groups": len(l1["content_md5_groups"]),
            "content_md5_dup_samples": sum(len(g["members"]) for g in l1["content_md5_groups"]),
            "details": l1,
        },
        "layer2_normalized": {
            "dup_groups": len(l2["groups"]),
            "dup_samples": sum(len(g["members"]) for g in l2["groups"]),
            "details": l2,
        },
        "layer3_semantic": {
            "threshold": l3["threshold"],
            "n_pairs": l3["n_pairs"],
            "top": l3["pairs"][:TOP_N],
            "all_pairs": l3["pairs"],
        },
        "layer3b_cross_batch_structure": {
            "threshold": l3b["threshold"],
            "n_cross_batch_pairs": l3b["n_cross_batch_pairs"],
            "pairs": l3b["pairs"],
        },
        "matrix_normalized": batch_matrix([g["members"] for g in l2["groups"]]),
        "matrix_semantic": batch_matrix(
            [[{"batch": p["a"]["batch"]}, {"batch": p["b"]["batch"]}] for p in l3["pairs"]]
        ),
        "clone_rate": {
            "n_text_covered": n_covered,
            "n_in_normalized_dup_group": sum(len(g["members"]) for g in l2["groups"]),
            "n_unique_structures": len(l2["groups"]) + (n_covered - sum(len(g["members"]) for g in l2["groups"])),
        },
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)

    if not args.quiet:
        print(f"样本总数 {len(samples)}  文本层可覆盖 {n_covered}  无源文件 {len(samples)-n_covered}")
        print(f"L1 精确：cpp 重复组 {result['layer1_exact']['cpp_dup_groups']}，"
              f"涉及样本 {result['layer1_exact']['cpp_dup_samples']}；"
              f"标注 .json 重复组 {result['layer1_exact']['annotation_dup_groups']}；"
              f"content_md5 重复组 {result['layer1_exact']['content_md5_dup_groups']}")
        print(f"L2 归一化：重复组 {result['layer2_normalized']['dup_groups']}，"
              f"涉及样本 {result['layer2_normalized']['dup_samples']}")
        print(f"L3 语义(≥{SEM_THRESHOLD})：相似对 {l3['n_pairs']}")
        for p in l3["pairs"][:10]:
            print(f"   {p['similarity']:.4f}  {p['a']['uid']}({p['a']['batch']}) ~ "
                  f"{p['b']['uid']}({p['b']['batch']})  [{p['defect_type']}]")
        print(f"L3b 跨批结构近克隆(≥{SEM_THRESHOLD}，常量归一)：{l3b['n_cross_batch_pairs']} 对")
        for p in l3b["pairs"][:10]:
            print(f"   {p['similarity']:.4f}  {p['a']['uid']}({p['a']['batch']}) ~ "
                  f"{p['b']['uid']}({p['b']['batch']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
