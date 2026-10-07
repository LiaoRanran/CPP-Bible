#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""repair_681_labels.py — 681 A：跨源标签修复 + legacy 归一化（派生件修复，权威 JSON 只读）。

修复对象（派生件，非权威记录）：
  1. data/blindspot_676g_detection_matrix.json  samples[].defect_type / expected_verdict
     - 扩样 1042 行：以权威逐样本 JSON（data/holdout_expansion/<batch>/sample_*.json）为准
       （根因：676m 迁移改写了 308 条权威值，但矩阵未重派生 —— 见 SCHEMA.md §6「改写样本 308/1042」）
     - 原始 105 行（holdout 41 + corpus 64）：按 SCHEMA §3.3 收敛表 + §4.2/§4.3 证据规则归一化
  2. data/holdout_expansion/expA/INDEX.json  index[].defect_type / expected_verdict / by_type
  3. data/676m_sample_manifest_corrected.json  仅 expA 100 行的 defect_type / expected_verdict

不修改（红线）：权威逐样本 .json、样本源码 *.cpp、matrix 的 per_asset 真实观测与
or_verdict_all8、hung_flag、qa_rerun、tsan_stability 等观测字段。

证据来源（红线 7）：
  - 扩样：权威 JSON 自身（676m 已按 SCHEMA §4.2 证据规则迁移）
  - holdout：磁盘源文件（缺陷标记行 + 头部说明）
  - corpus：data/external_corpus/external_corpus_{662,665,669d,672h}.json 的 description/code/source

用法：
  python tools/repair_681_labels.py            # dry-run（只报差异，不写盘）
  python tools/repair_681_labels.py --apply    # 写盘（矩阵 / expA INDEX / 676m manifest + 日志）
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPDIR = os.path.join(ROOT, "data", "holdout_expansion")
MATRIX = os.path.join(ROOT, "data", "blindspot_676g_detection_matrix.json")
MANIFEST = os.path.join(ROOT, "data", "676m_sample_manifest_corrected.json")
INDEX_EXPA = os.path.join(EXPDIR, "expA", "INDEX.json")
OUT_LOG = os.path.join(ROOT, "data", "681_标签修复日志.json")
OUT_STATS = os.path.join(ROOT, "data", "681_type_stats_normalized.json")

CORPUS_EVIDENCE_FILES = [
    os.path.join(ROOT, "data", "external_corpus", f"external_corpus_{tag}.json")
    for tag in ("662", "665", "669d", "672h")
]

# SCHEMA §3.1 的 15 类粗粒度分组（用于 A4 家族级汇总；不写进逐样本 JSON）
GROUP_OF: dict[str, str] = {
    "memory_safety": "memory_lifetime", "use_after_free": "memory_lifetime",
    "double_free": "memory_lifetime", "memory_leak": "memory_lifetime",
    "smart_pointer": "memory_lifetime", "raii_violation": "memory_lifetime",
    "move_semantics": "memory_lifetime",
    "out_of_bounds": "out_of_bounds",
    "null_pointer_deref": "null_deref",
    "uninitialized_read": "uninitialized_read",
    "integer_overflow": "integer_ub", "bit_operation": "integer_ub",
    "type_punning": "type_alias_alignment", "strict_aliasing": "type_alias_alignment",
    "alignment": "type_alias_alignment", "endianness": "type_alias_alignment",
    "linker_odr": "type_alias_alignment",
    "data_race": "data_race",
    "atomic_ub": "concurrency_order", "memory_order": "concurrency_order",
    "deadlock": "liveness", "condition_variable": "liveness",
    "iterator_invalidation": "stl_iterator", "stl_container_ub": "stl_iterator",
    "string_ub": "stl_iterator", "algorithm_misuse": "stl_iterator",
    "virtual_function": "virtual_or_oop", "lambda_capture": "virtual_or_oop",
    "volatile_misuse": "embedded_platform", "register_ub": "embedded_platform",
    "interrupt_safety": "embedded_platform",
    "cross_tu_ub": "logic_or_api", "logic_error": "logic_or_api",
    "other_ub": "generic_ub",
}

# A4 家族级粗分组（论文用的 8 家族）
FAMILY8: dict[str, tuple[str, ...]] = {
    "memory": ("memory_safety", "use_after_free", "double_free", "memory_leak",
               "smart_pointer", "raii_violation", "move_semantics", "uninitialized_read"),
    "bounds": ("out_of_bounds", "null_pointer_deref"),
    "integer": ("integer_overflow", "bit_operation"),
    "alias_type": ("type_punning", "strict_aliasing", "alignment", "endianness"),
    "concurrency": ("data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable"),
    "stl": ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"),
    "language_oop": ("virtual_function", "lambda_capture", "logic_error", "cross_tu_ub", "other_ub"),
    "embedded_link": ("volatile_misuse", "register_ub", "interrupt_safety", "linker_odr"),
}


def _has(ev: str, *keys: str) -> bool:
    return any(k in ev for k in keys)


def resolve_memory(ev: str) -> str:
    """MEM/`memory` 家族细分（与 fix_676m_schema.resolve_by_evidence 同款关键字规则）。"""
    if _has(ev, "use-after-free", "use after free", "uaf", "释放后", "悬垂", "dangling"):
        return "use_after_free"
    if _has(ev, "double free", "double-free", "两次释放", "二次释放", "重复释放"):
        return "double_free"
    if _has(ev, "越界", "out-of-bound", "out of bound", "heap-buffer", "stack-buffer",
            "overread", "overflow", "underflow", "oob"):
        return "out_of_bounds"
    if _has(ev, "leak", "泄漏"):
        return "memory_leak"
    if _has(ev, "未初始化", "uninitialized", "uninit"):
        return "uninitialized_read"
    return "memory_safety"


def resolve_ub(ev: str) -> str:
    """UB 家族细分；无法细分回落 other_ub（SCHEMA §4.2）。"""
    if _has(ev, "除以零", "division by zero", "div by zero", "modulo by zero"):
        return "integer_overflow"
    if _has(ev, "取负", "negation overflow", "int_min", "有符号溢出", "signed overflow"):
        return "integer_overflow"
    if _has(ev, "移位", "shift"):
        return "bit_operation"
    if _has(ev, "未对齐", "unaligned", "对齐"):
        return "alignment"
    if _has(ev, "严格别名", "strict alias", "别名"):
        return "strict_aliasing"
    if _has(ev, "union"):
        return "type_punning"
    if _has(ev, "空指针", "null pointer", "nullptr", "deref null"):
        return "null_pointer_deref"
    if _has(ev, "字符串字面量", "string literal", "只读段", "read-only"):
        return "out_of_bounds"
    return "other_ub"


def resolve_conc(ev: str) -> str:
    """CONC 家族细分；无法细分回落 data_race（该码在本语料中均为并发竞态/可见性类）。"""
    if _has(ev, "死锁", "deadlock", "锁序", "优先级反转", "priority inversion"):
        return "deadlock"
    if _has(ev, "条件变量", "condition variable", "cv 等待", "永久等待"):
        return "condition_variable"
    if _has(ev, "内存序", "memory_order", "acquire", "release", "relaxed", "seq_cst", "可见性"):
        return "memory_order"
    if _has(ev, "原子", "atomic", "aba"):
        return "atomic_ub"
    return "data_race"


DIRECT_MAP: dict[str, tuple[str, str]] = {
    "leak": ("memory_leak", "SCHEMA §3.3：resource_leak→memory_leak（含 fd 泄漏）；`leak` 为其简写"),
    "RAII/UB": ("raii_violation", "词表 #6 raii_violation（RAII 释放/析构违例）"),
    "ODR": ("linker_odr", "SCHEMA §3.3：cross_tu_ub（多重定义/ODR）→ linker_odr"),
    "memory-order": ("memory_order", "词表 #19 memory_order（连字符为拼写变体）"),
    "API": ("logic_error", "SCHEMA §3.2：logic_error 覆盖「非 UB 语义/API/状态缺陷」"),
    "unspecified": ("other_ub", "SCHEMA §4.2 回落规则；证据 expected_detector=wunsequenced（未指定求值顺序）"),
}

FAMILY_MAP: dict[str, str] = {
    "MEM": "memory", "memory": "memory",
    "UB": "ub", "undefined_behavior": "ub", "other_ub": "ub",
    "CONC": "conc", "race_condition": "conc",
}

# 逐样本证据不足以细分时的落地（SCHEMA §4.2「无法细分回落 other_ub」的同类应用）
EVIDENCE_FALLBACK: dict[str, tuple[str, str]] = {
    "historical": ("other_ub", "历史登记样本（un-pinned）；证据不足细分，按 §4.2 回落 other_ub"),
    "compiler-diff": ("other_ub", "SCHEMA §4.3：meta 标签（编译器差异）按证据细分；证据不足回落 other_ub"),
    "ambiguity": ("other_ub", "歧义标注；证据不足细分，按 §4.2 回落 other_ub"),
    "compiler-bug": ("other_ub", "编译器缺陷类（非本仓缺陷）；按 §4.2 回落 other_ub"),
}


def load_auth_types() -> dict[tuple[str, str], dict[str, str]]:
    """权威逐样本 JSON：(batch, sample_id) → {defect_type, expected_verdict}。"""
    out: dict[tuple[str, str], dict[str, str]] = {}
    for p in glob.glob(os.path.join(EXPDIR, "exp*", "sample_*.json")):
        batch = os.path.basename(os.path.dirname(p))
        if batch == "expA" and os.path.basename(p).startswith("sample_A"):
            pass
        try:
            with open(p, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        sid = d.get("sample_id")
        if isinstance(sid, str) and sid:
            out[(batch, sid)] = {
                "defect_type": str(d.get("defect_type") or ""),
                "expected_verdict": str(d.get("expected_verdict") or ""),
            }
    return out


def load_corpus_evidence() -> dict[str, dict[str, str]]:
    """corpus 证据（后波次覆盖前波次）：id → {category, description, code, source}。"""
    out: dict[str, dict[str, str]] = {}
    for f in CORPUS_EVIDENCE_FILES:
        if not os.path.exists(f):
            continue
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        for r in d.get("samples") or []:
            sid = r.get("id")
            if isinstance(sid, str):
                out[sid] = {k: str(r.get(k) or "") for k in ("category", "description", "code", "source")}
    return out


def holdout_evidence(row: dict[str, Any]) -> str:
    """holdout 源文件证据：头部注释 + 缺陷标记行（红线 7：源码级）。"""
    d = str(row.get("dir") or "")
    files = [str(x) for x in (row.get("files") or [])]
    chunks: list[str] = []
    for fn in files[:2]:
        p = os.path.join(ROOT, d.replace("/", os.sep), fn)
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue
        chunks.append("\n".join(lines[:20]))
        chunks.extend(ln for ln in lines if any(
            k in ln for k in ("PLANTED-DEFECT", "DEFECT:", "UB", "double free", "use-after-free",
                              "leak", "race", "override", "unsequenced")))
    return "\n".join(chunks).lower()


def map_original(label: str, ev: str) -> tuple[str, str]:
    """原始 105 条的 legacy 标签 → 规范词表取值（含证据规则说明）。"""
    if label in DIRECT_MAP:
        return DIRECT_MAP[label]
    fam = FAMILY_MAP.get(label)
    if fam == "memory":
        return resolve_memory(ev), f"§3.3/§4.2 MEM 家族证据细分（label={label}）"
    if fam == "ub":
        return resolve_ub(ev), f"§4.2 UB 家族证据细分（label={label}）"
    if fam == "conc":
        return resolve_conc(ev), f"§3.3/§4.2 并发家族证据细分（label={label}）"
    if label in EVIDENCE_FALLBACK:
        return EVIDENCE_FALLBACK[label]
    if label == "other_ub":
        return resolve_ub(ev), "§4.2 笼统标签证据细分"
    return "other_ub", f"未知 legacy 标签 `{label}`；按 §4.2 回落 other_ub（待人工复核）"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="写盘（默认 dry-run）")
    args = ap.parse_args()

    auth = load_auth_types()
    corpus_ev = load_corpus_evidence()
    with open(MATRIX, encoding="utf-8") as fh:
        mx = json.load(fh)
    with open(MANIFEST, encoding="utf-8") as fh:
        man = json.load(fh)
    man_by_uid = {r["uid"]: r for r in man.get("samples") or []}

    rows = mx["samples"]
    type_changes: list[dict[str, str]] = []
    verdict_changes: list[dict[str, str]] = []
    unresolved: list[str] = []

    for r in rows:
        batch = str(r.get("source_batch") or "")
        sid = str(r.get("sample_id") or "")
        uid = str(r.get("uid") or f"{batch}:{sid}")
        old_type = str(r.get("defect_type") or "")
        old_verdict = str(r.get("expected_verdict") or "")

        if batch.startswith("exp"):
            a = auth.get((batch, sid))
            if a is None:
                unresolved.append(f"{uid}: 权威 JSON 缺失")
                continue
            new_type = a["defect_type"] or old_type
            new_verdict = a["expected_verdict"] or old_verdict
            rule = "A2：以权威逐样本 JSON 为准（676m 迁移后）"
            ev_excerpt = f"authoritative sample_{sid}.json"
        else:
            if batch == "holdout":
                ev = holdout_evidence(r)
            else:
                ce = corpus_ev.get(sid) or {}
                ev = " ".join(ce.get(k, "") for k in ("category", "description", "code", "source")).lower()
            new_type, rule = map_original(old_type, ev)
            m = man_by_uid.get(uid) or {}
            new_verdict = str(m.get("expected_verdict") or old_verdict)
            ev_excerpt = ev[:220].replace("\n", " ")

        if new_type != old_type:
            type_changes.append({
                "uid": uid, "batch": batch, "old": old_type, "new": new_type,
                "rule": rule, "evidence": ev_excerpt,
            })
            r["defect_type"] = new_type
        if new_verdict != old_verdict:
            verdict_changes.append({
                "uid": uid, "batch": batch, "old": old_verdict, "new": new_verdict,
                "rule": "A2/A5：与权威 JSON / 676m 修正件对齐（含 expE 34 条 hung 口径）",
            })
            r["expected_verdict"] = new_verdict

    # A5 校验：矩阵 expected_verdict 与 676m 修正件一致
    v_diffs = [r["uid"] for r in rows
               if str(r.get("expected_verdict")) != str((man_by_uid.get(r["uid"]) or {})
                                                        .get("expected_verdict") or r.get("expected_verdict"))]

    # 修复后类型统计（A4）
    dist = collections.Counter(str(r["defect_type"]) for r in rows)
    per_type: dict[str, dict[str, Any]] = {}
    for t in sorted(dist):
        sub = [r for r in rows if str(r["defect_type"]) == t]
        bl = sum(1 for r in sub if str(r.get("or_verdict_all8")) == "miss")
        det = sum(1 for r in sub if str(r.get("or_verdict_all8")) == "catch")
        per_type[t] = {
            "n": len(sub),
            "blind": bl,
            "blind_pct": round(100.0 * bl / len(sub), 1) if sub else 0.0,
            "detect": det,
            "detect_pct": round(100.0 * det / len(sub), 1) if sub else 0.0,
            "group": GROUP_OF.get(t, "unmapped"),
        }
    gt50 = sorted([t for t, v in per_type.items() if v["blind_pct"] > 50.0],
                  key=lambda t: -per_type[t]["blind_pct"])
    sample_blind = sum(1 for r in rows if str(r.get("or_verdict_all8")) == "miss")
    fam: dict[str, dict[str, float]] = {}
    for name, types in FAMILY8.items():
        sub = [r for r in rows if str(r["defect_type"]) in types]
        bl = sum(1 for r in sub if str(r.get("or_verdict_all8")) == "miss")
        fam[name] = {"n": len(sub), "blind": bl,
                     "blind_pct": round(100.0 * bl / len(sub), 1) if sub else 0.0}

    stats: dict[str, Any] = {
        "schema": "queyi-681-type-stats-normalized/v1",
        "generated_by": "tools/repair_681_labels.py",
        "source_matrix": "data/blindspot_676g_detection_matrix.json（681 修复后）",
        "n_samples": len(rows),
        "n_types": len(dist),
        "types_gt50_blind": len(gt50),
        "types_gt50_blind_list": gt50,
        "sample_level": {
            "blind": sample_blind,
            "blind_pct": round(100.0 * sample_blind / len(rows), 1),
            "detect_pct": round(100.0 * (len(rows) - sample_blind) / len(rows), 1),
        },
        "per_type": per_type,
        "family8": fam,
        "repair_summary": {
            "defect_type_changes": len(type_changes),
            "expected_verdict_changes": len(verdict_changes),
            "by_batch": dict(collections.Counter(c["batch"] for c in type_changes)),
            "verdict_by_batch": dict(collections.Counter(c["batch"] for c in verdict_changes)),
        },
    }

    log: dict[str, Any] = {
        "schema": "queyi-681-label-repair-log/v1",
        "generated_by": "tools/repair_681_labels.py",
        "n_type_changes": len(type_changes),
        "n_verdict_changes": len(verdict_changes),
        "type_changes": type_changes,
        "verdict_changes": verdict_changes,
        "unresolved": unresolved,
        "matrix_vs_676m_expected_diffs": len(v_diffs),
    }

    print("== 修复统计 ==")
    print(f"  defect_type 变更 {len(type_changes)}（按批 {dict(collections.Counter(c['batch'] for c in type_changes))}）")
    print(f"  expected_verdict 变更 {len(verdict_changes)}（按批 {dict(collections.Counter(c['batch'] for c in verdict_changes))}）")
    print(f"  未解析 {len(unresolved)}；矩阵 vs 676m 期望差异 {len(v_diffs)}")
    print("== 修复后类型统计 ==")
    print(f"  类型数 {len(dist)}；>50% 盲区类型 {len(gt50)}：{gt50}")
    print(f"  样本级盲区 {sample_blind}/{len(rows)} = {stats['sample_level']['blind_pct']}%")

    if args.apply:
        # A2b/A2c：expA INDEX.json
        with open(INDEX_EXPA, encoding="utf-8") as fh:
            idx = json.load(fh)
        idx_fixed = 0
        for e in idx.get("index") or []:
            sid = str(e.get("sample_id") or e.get("id") or "")
            a = auth.get(("expA", sid))
            if not a:
                continue
            if e.get("defect_type") != a["defect_type"]:
                e["defect_type"] = a["defect_type"]
                idx_fixed += 1
            if e.get("expected_verdict") != a["expected_verdict"]:
                e["expected_verdict"] = a["expected_verdict"]
        idx["by_type"] = dict(collections.Counter(
            str(e.get("defect_type")) for e in (idx.get("index") or [])))
        # A2b：676m manifest 的 expA 行
        man_fixed = 0
        for m in man.get("samples") or []:
            if str(m.get("source_batch")) != "expA":
                continue
            a = auth.get(("expA", str(m.get("sample_id"))))
            if not a:
                continue
            if m.get("defect_type") != a["defect_type"]:
                m["defect_type"] = a["defect_type"]
                man_fixed += 1
            if m.get("expected_verdict") != a["expected_verdict"]:
                m["expected_verdict"] = a["expected_verdict"]
        mx["repair_681"] = {
            "generated_by": "tools/repair_681_labels.py",
            "type_changes": len(type_changes),
            "expected_verdict_changes": len(verdict_changes),
            "note": "仅重派生 defects_type/expected_verdict 两列；per_asset/or_verdict_all8 等观测字段未改",
        }
        with open(MATRIX, "w", encoding="utf-8") as fh:
            json.dump(mx, fh, ensure_ascii=False, indent=1)
        with open(INDEX_EXPA, "w", encoding="utf-8") as fh:
            json.dump(idx, fh, ensure_ascii=False, indent=1)
        with open(MANIFEST, "w", encoding="utf-8") as fh:
            json.dump(man, fh, ensure_ascii=False, indent=1)
        with open(OUT_LOG, "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
        with open(OUT_STATS, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, ensure_ascii=False, indent=1)
        print(f"  WROTE matrix / expA INDEX（{idx_fixed} 条 defect_type 修正）/ 676m manifest（{man_fixed} 条）")
        print(f"  WROTE {os.path.relpath(OUT_LOG, ROOT)} / {os.path.relpath(OUT_STATS, ROOT)}")
    else:
        print("  (dry-run：未写盘；加 --apply 生效)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
