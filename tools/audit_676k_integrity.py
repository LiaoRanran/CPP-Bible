#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_676k_integrity.py — 676k 任务E：INDEX.json 一致性 + 标注字段完整性。

只读。两部分：
  E1 INDEX 一致性：对 expA..expG 的 INDEX.json
     - 声明的样本数 vs 实际 .json 文件数
     - INDEX 中每个样本是否有对应 .cpp / .json
     - 磁盘上有文件但不在 INDEX 中
     - INDEX 的类型分布 vs 实际 .json 的 defect_type 分布
  E2 字段完整性：对所有扩展批次的 .json（1042 个）+ 清单层（105 个 legacy）
     - 必填字段是否存在（兼容各批次不同的字段命名）
     - defect_location.line 是否越界
     - expected_verdict 是否只取 catch/miss/unknown
     - planted 是否只取 true/false
     - planted=false 是否有 source.url

用法：
  python tools/audit_676k_integrity.py --json OUT
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPDIR = os.path.join(ROOT, "data", "holdout_expansion")
BLINDSPOT = os.path.join(ROOT, "data", "blindspot_676g_sample_manifest.json")
A5MANIFEST = os.path.join(ROOT, "data", "a5_676f_sample_manifest.json")
EXP_BATCHES = ["expA", "expB", "expC", "expD", "expE", "expF", "expG"]

# 各批次对同一语义字段使用了不同键名 —— 兼容表（这本身就是一条发现）
ID_KEYS = ["sample_id", "id"]
LOCATION_KEYS = ["defect_location", "location"]
NOTES_KEYS = ["detector_notes", "notes", "note", "description"]


def norm_id(batch: str, sid: str) -> str:
    """统一成磁盘文件名的 stem（expD 的 'D013' → 'sample_D013'）。"""
    if not sid:
        return sid
    if sid.startswith("sample_"):
        return sid
    if batch in ("expD", "expF") and re.fullmatch(r"[A-Z]\d{3}", sid):
        return "sample_" + sid
    return sid


def list_samples(batch: str) -> dict:
    """从 INDEX.json 抽取声明的样本 id 列表（各批次结构不同，逐个适配）。"""
    p = os.path.join(EXPDIR, batch, "INDEX.json")
    d = json.load(open(p, encoding="utf-8"))
    ids, src_key = [], None
    if isinstance(d.get("index"), list):
        ids = [e.get("id") or e.get("sample_id") for e in d["index"]]
        src_key = "index[].id"
    elif isinstance(d.get("samples"), list):
        ids = [e.get("sample_id") or e.get("id") for e in d["samples"]]
        src_key = "samples[].sample_id"
    elif isinstance(d.get("sample_ids"), list):
        ids = list(d["sample_ids"])
        src_key = "sample_ids[]"
    # INDEX 自报的类型分布
    by_type = None
    for k in ("by_type", "type_distribution"):
        if isinstance(d.get(k), dict):
            by_type = d[k]
            break
    if by_type is None and isinstance(d.get("stats"), dict):
        for k in ("by_type", "type_distribution"):
            if isinstance(d["stats"].get(k), dict):
                by_type = d["stats"][k]
                break
    declared = None
    for k in ("count", "pooled", "total", "generated"):
        if isinstance(d.get(k), int):
            declared = d[k]
            break
    return {"index": d, "ids": ids, "ids_key": src_key,
            "declared_count": declared, "declared_by_type": by_type}


def e1() -> dict:
    out = {}
    for b in EXP_BATCHES:
        info = list_samples(b)
        d = os.path.join(EXPDIR, b)
        json_files = sorted(f[:-5] for f in os.listdir(d)
                            if f.endswith(".json") and f != "INDEX.json")
        cpp_files = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".cpp"))

        declared_ids = [norm_id(b, i) for i in info["ids"]]
        declared_set = set(declared_ids)

        # 实际 .json 对应的样本 stem
        actual_json = set(json_files)
        # 多文件样本：sample_107_a.cpp / _main.cpp 归属 sample_107
        actual_cpp = set()
        for cf in cpp_files:
            m = re.match(r"^(sample_[A-Z]?\d+)(_[a-z]+)?$", cf)
            actual_cpp.add(m.group(1) if m else cf)

        missing_json = sorted(declared_set - actual_json)
        extra_json = sorted(actual_json - declared_set)
        missing_cpp = sorted(declared_set - actual_cpp)

        # 实际类型分布
        actual_by_type: collections.Counter[str] = collections.Counter()
        for stem in actual_json:
            p = os.path.join(d, stem + ".json")
            try:
                j = json.load(open(p, encoding="utf-8"))
                actual_by_type[j.get("defect_type")] += 1
            except Exception:
                actual_by_type["<parse_error>"] += 1

        type_diff = {}
        if info["declared_by_type"]:
            for k in sorted(set(info["declared_by_type"]) | set(actual_by_type)):
                a = info["declared_by_type"].get(k, 0)
                c = actual_by_type.get(k, 0)
                if a != c:
                    type_diff[k] = {"index": a, "actual": c}
        # 重复 id
        dup = [k for k, v in collections.Counter(declared_ids).items() if v > 1]

        out[b] = {
            "index_ids_key": info["ids_key"],
            "declared_count_field": info["declared_count"],
            "declared_count": len(declared_ids),
            "actual_json": len(actual_json),
            "actual_cpp_samples": len(actual_cpp),
            "count_match": info["declared_count"] == len(declared_ids) == len(actual_json),
            "dup_ids": dup,
            "missing_json": missing_json,
            "missing_cpp": missing_cpp,
            "extra_json_not_in_index": extra_json,
            "type_dist_mismatch": type_diff,
        }
    return out


REQUIRED = {
    "sample_id": ID_KEYS,
    "defect_type": ["defect_type"],
    "defect_location": LOCATION_KEYS,
    "expected_verdict": ["expected_verdict"],
    "planted": ["planted"],
    "notes": NOTES_KEYS,
}


def e2() -> dict:
    missing_field = []
    line_oob = []
    bad_verdict = []
    bad_planted = []
    planted_false_no_url = []
    loc_missing_parts = []
    n_checked = 0
    field_presence: collections.Counter[str] = collections.Counter()

    for b in EXP_BATCHES:
        d = os.path.join(EXPDIR, b)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn == "INDEX.json":
                continue
            n_checked += 1
            p = os.path.join(d, fn)
            try:
                j = json.load(open(p, encoding="utf-8"))
            except Exception as e:
                missing_field.append({"batch": b, "file": fn, "field": "<parse>", "why": str(e)[:120]})
                continue
            uid = f"{b}:{fn[:-5]}"
            for field, keys in REQUIRED.items():
                if not any(k in j for k in keys):
                    missing_field.append({"batch": b, "file": fn, "field": field,
                                          "why": f"缺失，尝试过 {keys}"})
                else:
                    field_presence[field] += 1

            loc = j.get("defect_location") or j.get("location") or {}
            if isinstance(loc, dict):
                if "file" not in loc:
                    loc_missing_parts.append({"batch": b, "file": fn, "part": "file"})
                line = loc.get("line")
                if line is None:
                    loc_missing_parts.append({"batch": b, "file": fn, "part": "line"})
                else:
                    # 行号越界检查：对该样本的所有 .cpp 取最大行数
                    stem = fn[:-5]
                    cands = [f for f in os.listdir(d)
                             if f.endswith(".cpp") and (f[:-4] == stem or f.startswith(stem + "_"))]
                    if cands:
                        maxlines = 0
                        for c in cands:
                            txt = open(os.path.join(d, c), encoding="utf-8",
                                       errors="replace").read()
                            maxlines = max(maxlines, len(txt.splitlines()))
                        try:
                            if int(line) > maxlines or int(line) < 1:
                                line_oob.append({"uid": uid, "line": line,
                                                 "file_lines": maxlines, "file": cands[0]})
                        except (TypeError, ValueError):
                            line_oob.append({"uid": uid, "line": line, "file_lines": maxlines,
                                             "file": cands[0], "why": "非整数"})

            v = j.get("expected_verdict")
            if v is not None and v not in ("catch", "miss", "unknown"):
                bad_verdict.append({"uid": uid, "value": v})
            pl = j.get("planted")
            if pl is not None and not isinstance(pl, bool):
                bad_planted.append({"uid": uid, "value": pl})
            if pl is False:
                src = j.get("source") or {}
                if not src.get("url"):
                    planted_false_no_url.append({"uid": uid})

    return {
        "n_checked_expansion_json": n_checked,
        "field_presence": dict(field_presence),
        "missing_field": missing_field,
        "line_out_of_range": line_oob,
        "bad_expected_verdict": bad_verdict,
        "bad_planted_type": bad_planted,
        "planted_false_without_url": planted_false_no_url,
        "defect_location_missing_parts": loc_missing_parts,
    }


def e2_manifest() -> dict:
    """清单层（holdout + corpus，105 条）的字段完整性 —— 它们没有独立 .json。"""
    bs = json.load(open(BLINDSPOT, encoding="utf-8"))
    a5 = json.load(open(A5MANIFEST, encoding="utf-8"))
    a5map = {s["sample_id"]: s for s in a5["samples"]}
    rows = []
    for e in bs["samples"]:
        if e["source_batch"] not in ("holdout", "corpus"):
            continue
        rows.append({
            "uid": e["uid"],
            "has_defect_type": e.get("defect_type") is not None,
            "has_expected_verdict": e.get("expected_verdict") is not None,
            "verdict": e.get("expected_verdict"),
            "planted": e.get("planted"),
            "has_files": bool(e.get("files")),
            "in_a5": e["sample_id"] in a5map,
        })
    bad_v = [r["uid"] for r in rows if r["verdict"] not in ("catch", "miss", "unknown")]
    return {
        "n": len(rows),
        "no_defect_type": [r["uid"] for r in rows if not r["has_defect_type"]],
        "no_expected_verdict": [r["uid"] for r in rows if not r["has_expected_verdict"]],
        "bad_verdict": bad_v,
        "planted_null": [r["uid"] for r in rows if r["planted"] is None],
        "planted_false": [r["uid"] for r in rows if r["planted"] is False],
        "no_files": [r["uid"] for r in rows if not r["has_files"]],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()
    res: dict[str, Any] = {
        "schema": "queyi-audit-676k-integrity/v1",
        "generated_by": "tools/audit_676k_integrity.py",
        "E1_index_consistency": e1(),
        "E2_field_completeness": e2(),
        "E2_manifest_layer": e2_manifest(),
    }
    if args.json:
        json.dump(res, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("== E1 INDEX 一致性 ==")
    for b, v in res["E1_index_consistency"].items():
        flag = "OK " if (v["count_match"] and not v["missing_json"] and not v["missing_cpp"]
                         and not v["extra_json_not_in_index"] and not v["type_dist_mismatch"]) else "!! "
        print(f" {flag}{b}: INDEX声明={v['declared_count']} 实际json={v['actual_json']} "
              f"cpp样本={v['actual_cpp_samples']} 缺json={len(v['missing_json'])} "
              f"缺cpp={len(v['missing_cpp'])} 多余={len(v['extra_json_not_in_index'])} "
              f"类型不符={len(v['type_dist_mismatch'])} 重复id={len(v['dup_ids'])}")
    print()
    e2r = res["E2_field_completeness"]
    print("== E2 字段完整性 ==")
    print(f" 检查 .json 数：{e2r['n_checked_expansion_json']}")
    print(f" 字段缺失：{len(e2r['missing_field'])}")
    print(f" 行号越界：{len(e2r['line_out_of_range'])}")
    print(f" 非法 expected_verdict：{len(e2r['bad_expected_verdict'])}")
    print(f" planted 非布尔：{len(e2r['bad_planted_type'])}")
    print(f" planted=false 缺 source.url：{len(e2r['planted_false_without_url'])}")
    print(f" defect_location 缺 file/line：{len(e2r['defect_location_missing_parts'])}")
    print()
    m = res["E2_manifest_layer"]
    print("== E2 清单层（holdout+corpus） ==")
    print(f" n={m['n']} 无 defect_type={len(m['no_defect_type'])} "
          f"无 expected_verdict={len(m['no_expected_verdict'])} planted=null={len(m['planted_null'])} "
          f"planted=false={len(m['planted_false'])} 无源文件={len(m['no_files'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
