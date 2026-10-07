#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""gen_682_metadata.py — 682 · 任务A：Croissant（core+RAI）与 RAI metadata 生成。

输入（只读）：
  data/blindspot_676g_detection_matrix.json   1147×8 逐格 verdict（681 修复后）
  data/blindspot_676g_stats.json              676g 盲区统计（6710 口径）
  data/681_type_stats_normalized.json         681 修复后的 34 类归一化统计
  data/a5_676f_sample_manifest.json           1137 样本清单（A5 切分）
  data/holdout_expansion/**/                  1042 条扩样标注 + 源码（只读）

产物：
  data/croissant.json        Croissant core 1.1 + RAI 扩展（NeurIPS 2026 E&D 要求 core+RAI 同一文件）
  data/rai_metadata.json     RAI 元数据的展开版（人类可读 + 机器可读；与 croissant.json 内 RAI 字段同源）

自校验（任一失败即非零退出）：
  C1 JSON 可解析 + Croissant 必填字段齐（@context/@type/conformsTo/name/description/url/license/
     creator/datePublished/distribution/recordSet）
  C2 统计数字与源文件逐位一致（1147 / 34 / 8 / 61.6 / 38.4）
  C3 每个 FileObject 的 sha256/contentSize 从磁盘复算并比对
  C4 distribution 中列出的路径全部存在
  C5 RAI 8 个最小字段（NeurIPS 2026 Hosting）全部在场

红线：不改检测器、不改样本源文件、不改 676f/677b/681 既有产物、不 push。
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_676G = ROOT / "data" / "blindspot_676g_detection_matrix.json"
STATS_676G = ROOT / "data" / "blindspot_676g_stats.json"
TYPE_STATS_681 = ROOT / "data" / "681_type_stats_normalized.json"
MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
OUT_CROISSANT = ROOT / "data" / "croissant.json"
OUT_RAI = ROOT / "data" / "rai_metadata.json"

GITHUB = "https://github.com/LiaoRanran/CPP-Bible"
CREATOR = {"@type": "sc:Person", "name": "Ran Liao",
           "affiliation": {"@type": "sc:Organization", "name": "Hefei University"}}
BATCHES = ("expA", "expB", "expC", "expD", "expE", "expF", "expG")


def _now() -> str:
    import datetime as _dt
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jload(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _jwrite(p: Path, doc: dict) -> None:
    Path(p).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")


def _sha_size(rel: str) -> tuple[str, int]:
    p = ROOT / rel.replace("/", "/")
    data = p.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def file_object(rel: str, fmt: str, desc: str, group: str) -> dict:
    sha, size = _sha_size(rel)
    return {
        "@type": "cr:FileObject", "@id": rel, "name": Path(rel).name,
        "contentUrl": rel, "encodingFormat": fmt,
        "sha256": sha, "contentSize": str(size),   # schema.org Text（mlcroissant 校验要求）
        "queyi:group": group, "description": desc,
    }


FO_OF = {"queyi-sample-index": "data/a5_676f_sample_manifest.json",
         "queyi-detection-matrix": "data/blindspot_676g_detection_matrix.json"}


def field(rs: str, name: str, dtype: str, jsonpath: str | None, desc: str,
          repeated: bool = False, value=None) -> dict:
    """构造 cr:Field。字段级 source 必须显式带 fileObject（mlcroissant 要求）。"""
    d = {"@type": "cr:Field", "@id": f"{rs}/{name}", "name": name,
         "dataType": dtype, "description": desc}
    if repeated:
        d["repeated"] = True
    if value is not None:
        d["value"] = value
    elif jsonpath is not None:
        d["source"] = {"fileObject": {"@id": FO_OF[rs]},
                       "extract": {"jsonPath": jsonpath}}
    return d


# ─────────────────────────────────────────────────────────────────────────────
# 统计（全部从数据现算，不从别处抄）
# ─────────────────────────────────────────────────────────────────────────────
def compute_stats() -> dict:
    mx = _jload(MATRIX_676G)
    st = _jload(STATS_676G)
    ts = _jload(TYPE_STATS_681)
    man = _jload(MANIFEST)
    samples = mx["samples"]
    n = len(samples)
    if n != 1147:
        raise ValueError(f"676g 矩阵样本数 {n} != 1147 ⇒ fail-loud")
    if ts["n_samples"] != n or ts["n_types"] != 34:
        raise ValueError("681 类型统计与 676g 不一致 ⇒ fail-loud")
    per_type = ts["per_type"]
    if len(per_type) != 34:
        raise ValueError(f"per_type 计数 {len(per_type)} != 34 ⇒ fail-loud")
    n_planted_true = sum(1 for s in samples if s.get("planted") is True)
    n_planted_false = sum(1 for s in samples if s.get("planted") is False)
    n_planted_null = sum(1 for s in samples if s.get("planted") is None)
    n_hung = sum(1 for s in samples if s.get("hung_flag"))
    tot = st["total"]
    ratio = tot["blindspot_ratio"]
    if abs(ratio - ts["sample_level"]["blind_pct"] / 100) > 5e-3:
        raise ValueError("676g stats 与 681 类型统计的盲区率口径不一致 ⇒ fail-loud")
    env = mx["environment"]
    exp_batches = set(BATCHES)
    exp = [s for s in samples if s.get("source_batch") in exp_batches]
    return {
        "n_samples": n, "n_types": 34, "n_detectors": len(mx["assets"]),
        "expansion_n": len(exp),
        "expansion_planted_true": sum(1 for s in exp if s.get("planted") is True),
        "expansion_planted_false": sum(1 for s in exp if s.get("planted") is False),
        "assets": mx["assets"],
        "catch": tot["catch"], "miss": tot["miss"], "unknown": tot["unknown"],
        "detect_pct": ts["sample_level"]["detect_pct"],
        "blind_pct": ts["sample_level"]["blind_pct"],
        "blind_ratio": ratio,
        "types_gt50_blind": ts["types_gt50_blind"],
        "types_gt50_blind_list": ts["types_gt50_blind_list"],
        "per_type": per_type,
        "family8": ts["family8"],
        "n_planted_true": n_planted_true, "n_planted_false": n_planted_false,
        "n_planted_null": n_planted_null,
        "planted_true_pct_all": round(100.0 * n_planted_true / n, 2),
        "planted_true_pct_labelled": round(
            100.0 * n_planted_true / (n_planted_true + n_planted_false), 2),
        "n_hung": n_hung,
        "environment": env,
        "a5_n": man["n_total"], "a5_split": man["stats"]["by_split"],
        "batch_sizes": {b: sum(1 for s in samples if s["source_batch"] == b)
                        for b in sorted({s["source_batch"] for s in samples})},
        "repair_681": mx.get("repair_681", {}),
    }


def build_croissant_stats() -> dict:
    s = compute_stats()
    ts = _jload(TYPE_STATS_681)
    per_type_rows = []
    for t, v in sorted(ts["per_type"].items(), key=lambda kv: (-kv[1]["blind_pct"], kv[0])):
        per_type_rows.append({
            "defect_type": t, "defect_group": v["group"], "n_samples": v["n"],
            "blind": v["blind"], "blind_pct": v["blind_pct"],
            "gt50_blind": v["blind_pct"] > 50.0})
    return {"stats": s, "per_type_rows": per_type_rows, "ts": ts}


# ─────────────────────────────────────────────────────────────────────────────
# Croissant 文档
# ─────────────────────────────────────────────────────────────────────────────
def a5_summary() -> dict:
    """A5 主端点从 682 B1 产物读取（不硬编码论文数字；产物缺失时如实标注）。"""
    p = ROOT / "data" / "682_a5_split_comparison.json"
    if not p.is_file():
        return {"status": "missing", "note": "data/682_a5_split_comparison.json 未生成"}
    d = _jload(p)["results"]["original"]
    return {"n": d["n_derivation"] + d["n_evaluation"], "split": "676f original",
            "n_derivation": d["n_derivation"], "n_evaluation": d["n_evaluation"],
            "primary_k": 4, "fd_assets": d["main_k4"]["fd"]["assets"],
            "fd_rate_pct": d["main_k4"]["fd"]["rate_pct"],
            "random_rate_pct": d["main_k4"]["random"]["rate_pct"],
            "delta_fd_minus_random_pp": d["delta_fd_random_pp"],
            "mcnemar_p": d["mcnemar_p_fd_random"],
            "source": "data/682_a5_split_comparison.json（682 B1 产物）"}


def build_croissant() -> dict:
    built = build_croissant_stats()
    s, rows, ts = built["stats"], built["per_type_rows"], built["ts"]
    a5 = a5_summary()

    distribution = [
        file_object("data/holdout_expansion/DATASHEET.md", "text/markdown",
                    "数据卡（Gebru 九节格式，676m 版 + 677a 来源三分类）", "docs"),
        file_object("data/holdout_expansion/SCHEMA.md", "text/markdown",
                    "逐样本标注的唯一字段规范（34 类闭集、行号口径、provenance 枚举）", "docs"),
        file_object("data/a5_676f_sample_manifest.json", "application/json",
                    "A5 实验样本清单（1137 条：defect_type/defect_group/planted/"
                    "expected_verdict/split 等；含确定性分层切分规则）", "index"),
        file_object("data/blindspot_676g_detection_matrix.json", "application/json",
                    "1147×8 检测判定矩阵（每格为真实 detect() 调用结果；681 修复标签后）", "matrix"),
        file_object("data/blindspot_676g_stats.json", "application/json",
                    "676g 盲区统计（total/by_type/by_asset/complementarity；6710 口径）", "stats"),
        file_object("data/681_type_stats_normalized.json", "application/json",
                    "681 修复后的 34 类归一化统计（盲区率、family8 聚合；本文件统计字段的事实源）",
                    "stats"),
    ]
    for b in BATCHES:
        distribution.append({
            "@type": "cr:FileSet",
            "@id": f"data/holdout_expansion/{b}",
            "name": f"holdout_expansion/{b}",
            "description": f"扩样批次 {b}：逐样本标注（sample_*.json）与源码（*.cpp/*.h，只读）",
            "includes": [f"data/holdout_expansion/{b}/**"],
            "encodingFormat": "application/json + text/x-c++src",
            "queyi:group": "corpus",
        })

    rs_index = {
        "@type": "cr:RecordSet", "@id": "queyi-sample-index",
        "name": "样本索引（A5 清单）",
        "description": ("1137 条 A5 实验样本的元数据（来源清单 data/a5_676f_sample_manifest.json）。"
                        "split 为 676f 原 split（分层 sha256 奇偶，确定性）。"),
        "key": ["queyi-sample-index/sample_id"],
        "source": [{"fileObject": {"@id": "data/a5_676f_sample_manifest.json"},
                    "extract": {"jsonPath": "$.samples[*]"}}],
        "field": [
            field("queyi-sample-index", "sample_id", "sc:Text", "sample_id", "样本唯一 id"),
            field("queyi-sample-index", "source_batch", "sc:Text", "source_batch",
                  "来源批次（expA–expG / holdout / corpus_672h）"),
            field("queyi-sample-index", "defect_type", "sc:Text", "defect_type",
                  "缺陷类型（34 项闭集，词表见 data/holdout_expansion/SCHEMA.md §3）"),
            field("queyi-sample-index", "defect_group", "sc:Text", "defect_group",
                  "缺陷粗分组（15 类，与 676k TAXONOMY 对齐）"),
            field("queyi-sample-index", "planted", "sc:Boolean", "planted",
                  "是否本项目人工植入（true）/ 非自造（false）"),
            field("queyi-sample-index", "expected_verdict", "sc:Text", "expected_verdict",
                  "独立检测器判据：catch=至少一资产有诊断报告；miss=无报告（含挂起）"),
            field("queyi-sample-index", "expected_detectors", "sc:Text", "expected_detectors",
                  "预期命中的资产名列表", repeated=True),
            field("queyi-sample-index", "severity", "sc:Text", "severity", "严重度 low/medium/high"),
            field("queyi-sample-index", "split", "sc:Text", "split",
                  "676f 原 split：derivation（571）/ evaluation（566）"),
        ],
    }

    verdict_fields = []
    for a in ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker",
              "wunsequenced", "compile-time"):
        verdict_fields.append(field(
            "queyi-detection-matrix", f"verdict_{a.replace('-', '_')}", "sc:Text",
            f"per_asset.{a}.verdict",
            f"资产 {a} 的真实判定（catch/miss/unknown；unknown 绝不当 miss）"))
    rs_matrix = {
        "@type": "cr:RecordSet", "@id": "queyi-detection-matrix",
        "name": "检测判定矩阵（1147×8）",
        "description": ("每条样本在 8 个检测资产下的真实 verdict（每格一次真实 detect() 调用，"
                        "execution_model=real_per_asset_detect）。聚合口径：OR——任一 catch ⇒ catch；"
                        "全 unknown ⇒ unknown。"),
        "key": ["queyi-detection-matrix/sample_id"],
        "source": [{"fileObject": {"@id": "data/blindspot_676g_detection_matrix.json"},
                    "extract": {"jsonPath": "$.samples[*]"}}],
        "field": [
            field("queyi-detection-matrix", "sample_id", "sc:Text", "sample_id", "样本唯一 id"),
            field("queyi-detection-matrix", "defect_type", "sc:Text", "defect_type",
                  "缺陷类型（681 修复后，34 项闭集）"),
            field("queyi-detection-matrix", "expected_verdict", "sc:Text", "expected_verdict",
                  "独立检测器判据（681 修复后）"),
            field("queyi-detection-matrix", "planted", "sc:Boolean", "planted",
                  "人工植入标记（可缺失 ⇒ null）"),
            field("queyi-detection-matrix", "hung_flag", "sc:Boolean", "hung_flag",
                  "样本是否挂起（自旋死锁/自死锁/cv 永久等待 ⇒ 判据为 miss）"),
            *verdict_fields,
            field("queyi-detection-matrix", "platform_notes", "sc:Text", None,
                  "运行平台注记（常量字段）：本机检测环境为 WSL Ubuntu g++ 13.3.0 "
                  "（sanitizer 类资产）、MinGW g++ 13.1.0、clang 22.1.8；"
                  "缺 WSL 时 sanitizer 类降级 unknown——这是环境依赖，不是能力变化",
                  value=(f"WSL {s['environment']['wsl_gcc']} / local {s['environment']['local_gcc']} "
                         f"/ clang {s['environment']['local_clang']}")),
        ],
        "queyi:note": ("platform_notes 为常量字段（value 而非抽取）：矩阵无逐样本平台注记，"
                       "以环境常量如实表达，不虚构逐样本值。verdict_* 字段的 jsonPath 指向 "
                       "per_asset.<asset>.verdict；诊断摘要（note）与墙钟保留在矩阵文件内。"),
    }

    rs_taxonomy = {
        "@type": "cr:RecordSet", "@id": "queyi-defect-taxonomy",
        "name": "缺陷类型词表与盲区统计（34 类）",
        "description": ("681 修复后的 34 类缺陷类型：粗分组、样本数、盲区数与盲区率"
                        "（盲区 = 6 个可用资产的并集未捕获）。内联 data ⇒ 自包含，无外部依赖。"),
        "key": ["queyi-defect-taxonomy/defect_type"],
        "data": [
            {"queyi-defect-taxonomy/defect_type": r["defect_type"],
             "queyi-defect-taxonomy/defect_group": r["defect_group"],
             "queyi-defect-taxonomy/n_samples": r["n_samples"],
             "queyi-defect-taxonomy/blind": r["blind"],
             "queyi-defect-taxonomy/blind_pct": r["blind_pct"],
             "queyi-defect-taxonomy/gt50_blind": r["gt50_blind"]}
            for r in rows
        ],
        "field": [
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/defect_type", "name": "defect_type",
             "dataType": "sc:Text", "description": "缺陷类型（34 项闭集）"},
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/defect_group", "name": "defect_group",
             "dataType": "sc:Text", "description": "粗分组（15 类）"},
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/n_samples", "name": "n_samples",
             "dataType": "sc:Integer", "description": "该类型样本数"},
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/blind", "name": "blind",
             "dataType": "sc:Integer", "description": "该类型盲区样本数（并集未捕获）"},
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/blind_pct", "name": "blind_pct",
             "dataType": "sc:Float", "description": "盲区率（%）"},
            {"@type": "cr:Field", "@id": "queyi-defect-taxonomy/gt50_blind", "name": "gt50_blind",
             "dataType": "sc:Boolean", "description": "盲区率是否 >50%"},
        ],
    }

    fam = s["family8"]
    rs_family = {
        "@type": "cr:RecordSet", "@id": "queyi-family8-stats",
        "name": "家族聚合盲区统计（8 族）",
        "description": "type→group→family 的聚合层：8 个家族各自的样本数与盲区率（681 修复后）。",
        "key": ["queyi-family8-stats/family"],
        "data": [{"queyi-family8-stats/family": k,
                  "queyi-family8-stats/n_samples": v["n"],
                  "queyi-family8-stats/blind": v["blind"],
                  "queyi-family8-stats/blind_pct": v["blind_pct"]} for k, v in fam.items()],
        "field": [
            {"@type": "cr:Field", "@id": "queyi-family8-stats/family", "name": "family",
             "dataType": "sc:Text", "description": "家族名（memory/bounds/integer/alias_type/"
             "concurrency/stl/language_oop/embedded_link）"},
            {"@type": "cr:Field", "@id": "queyi-family8-stats/n_samples", "name": "n_samples",
             "dataType": "sc:Integer", "description": "家族样本数"},
            {"@type": "cr:Field", "@id": "queyi-family8-stats/blind", "name": "blind",
             "dataType": "sc:Integer", "description": "家族盲区样本数"},
            {"@type": "cr:Field", "@id": "queyi-family8-stats/blind_pct", "name": "blind_pct",
             "dataType": "sc:Float", "description": "家族盲区率（%）"},
        ],
    }

    doc = {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            "sc": "https://schema.org/",
            "cr": "http://mlcommons.org/croissant/",
            "rai": "http://mlcommons.org/croissant/RAI/",
            "dct": "http://purl.org/dc/terms/",
            "prov": "http://www.w3.org/ns/prov#",
            "queyi": "https://github.com/LiaoRanran/CPP-Bible/vocab#",
            "citeAs": "cr:citeAs",
            "column": "cr:column",
            "conformsTo": "dct:conformsTo",
            "data": {"@id": "cr:data", "@type": "@json"},
            "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
            "examples": {"@id": "cr:examples", "@type": "@json"},
            "equivalentProperty": "cr:equivalentProperty",
            "extract": "cr:extract",
            "field": "cr:field",
            "fileProperty": "cr:fileProperty",
            "fileObject": "cr:fileObject",
            "fileSet": "cr:fileSet",
            "format": "cr:format",
            "includes": "cr:includes",
            "isLiveDataset": "cr:isLiveDataset",
            "jsonPath": "cr:jsonPath",
            "key": "cr:key",
            "md5": "cr:md5",
            "parentField": "cr:parentField",
            "path": "cr:path",
            "recordSet": "cr:recordSet",
            "references": "cr:references",
            "regex": "cr:regex",
            "repeated": "cr:repeated",
            "replace": "cr:replace",
            "samplingRate": "cr:samplingRate",
            "separator": "cr:separator",
            "source": "cr:source",
            "subField": "cr:subField",
            "transform": "cr:transform",
        },
        "@type": "sc:Dataset",
        "dct:conformsTo": ["http://mlcommons.org/croissant/1.0",
                           "http://mlcommons.org/croissant/RAI/1.0"],
        "name": "queyi-detector-blindspot-corpus",
        "alternateName": "阙疑 · C++ 检测器能力边界语料库（1147 样本 × 8 资产）",
        "description": (
            f"C++ 未定义行为与并发/嵌入式缺陷的检测器能力边界评测语料库：{s['n_samples']} 条可编译片段 × "
            f"{s['n_detectors']} 个检测资产 = {s['n_samples'] * s['n_detectors']} 个**真实执行**的判定格，"
            f"无模拟分数。每条样本带 {s['n_types']} 项闭集缺陷类型、人工植入标记、独立检测器判据"
            f"（expected_verdict）与源码。全池 OR 口径检出率 **{s['detect_pct']}%**、"
            f"盲区率 **{s['blind_pct']}%**；34 类中 {s['types_gt50_blind']} 类盲区率 >50%。"
            "本数据集服务于「验证器能力边界能否被外部度量」这一评测问题：它同时给出"
            "①逐格真实判定；②跨批次统一的标签词表；③来源三分类（自撰/真源重写/外部原物=0）。"
            "五个 Croissant recordSet：样本索引（1137）、检测判定矩阵（1147×8）、"
            "34 类词表与盲区统计（内联）、8 族聚合（内联）。"
            "RAI 字段（NeurIPS 2026 E&D 要求）包括数据局限、偏差、预期用例、社会影响、"
            "合成数据声明与来源溯源。"),
        "version": "682.1",
        "datePublished": "2026-10-07",
        "dateModified": _now(),
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "url": GITHUB,
        "sameAs": "https://liaoranran.github.io/CPP-Bible",
        "creator": CREATOR,
        "publisher": {"@type": "sc:Organization", "name": "CPP-Bible / Queyi Project"},
        "keywords": ["C++", "undefined behavior", "sanitizer", "static analysis",
                     "detector blind spots", "dataset", "evaluation", "Croissant",
                     "reproducibility", "four-state verdict"],
        "isAccessibleForFree": True,
        "citeAs": ("Liao, R. (2026). queyi-detector-blindspot-corpus: C++ detector capability "
                   "boundary dataset (1147 samples x 8 assets) [Data set]. "
                   f"{GITHUB}"),
        "queyi:stats": {
            "n_samples": s["n_samples"],
            "n_defect_types": s["n_types"],
            "n_detectors": s["n_detectors"],
            "detection_rate_pct": s["detect_pct"],
            "blindspot_rate_pct": s["blind_pct"],
            "blindspot_ratio": s["blind_ratio"],
            "or_catch": s["catch"], "or_miss": s["miss"], "or_unknown": s["unknown"],
            "types_gt50_blind": s["types_gt50_blind"],
            "detectors": s["assets"],
            "usable_detectors": ["asan", "ubsan", "tsan", "compiler-warn",
                                 "cross-compile", "linker"],
            "degenerate_detectors": {
                "compile-time": "无本地检测器 ⇒ 恒 unknown",
                "wunsequenced": "本机 MinGW g++ 13.1 不认 -Wunsequenced ⇒ 恒 unknown"},
            "a5_subset": a5,
        },
        "queyi:labelProvenance": {
            "source_breakdown_expansion_batches": {
                "self-authored": s["expansion_planted_true"],
                "source-derived-reconstruction": s["expansion_planted_false"],
                "original-external-artifact": 0,
                "n_expansion": s["expansion_n"],
                "derivation_rule": "planted=true ⇒ self-authored；planted=false ⇒ "
                                   "source-derived-reconstruction（SCHEMA.md §2.1.2）"},
            "planted_true": s["n_planted_true"], "planted_false": s["n_planted_false"],
            "planted_null": s["n_planted_null"],
            "planted_true_pct_all": s["planted_true_pct_all"],
            "planted_true_pct_labelled": s["planted_true_pct_labelled"],
            "label_agreement": ("AI self-consistency only: Cohen's kappa = 0.77 (defect_type, "
                                "unified 15-class canon), 0.69 (expected_verdict), 0.71 (planted) "
                                "on n=131 blind re-annotation; NOT human IAA."),
            "repair_681": s["repair_681"],
        },
        "queyi:environment": s["environment"],
        "queyi:platformNotes": (
            "全部判定在本机 Windows + WSL Ubuntu 环境实测（sanitizer 类资产走 WSL g++ 13.3.0）；"
            "该环境三元组是判定矩阵的前提条件。缺 WSL 时 sanitizer 类样本降级 unknown ⇒ "
            "检出率下降（属环境依赖，不是能力变化）。"),
        "queyi:reproduction": ("data/holdout_expansion/SCHEMA.md（标注规范）；"
                               "仓库 README「评测数据集与数据质量」节（门禁命令）。"),
        "distribution": distribution,
        "recordSet": [rs_index, rs_matrix, rs_taxonomy, rs_family],
    }

    # RAI（NeurIPS 2026 E&D 最小字段集，8 项）
    doc.update({
        "rai:dataLimitations": [
            "语言限 C++（无其他语言样本）。",
            f"语料以自撰教学化片段为主：{s['planted_true_pct_all']}%（全体口径）的样本为人工植入；"
            f"非自撰的 {s['n_planted_false']} 条是从真实 CVE/GitHub issue **等价重写**的单文件片段"
            "（source-derived-reconstruction），**不含任何原始外部代码原物**；"
            f"另有 {s['n_planted_null']} 条 planted 未定。",
            "不能用于估计真实世界缺陷分布：样本构造偏向可演示性，批内克隆率 62.2%（仅 572 种代码结构）。",
            "类型分布不均衡：最大类 out_of_bounds 92 条，最小类 cross_tu_ub 7 条。",
            f"判定矩阵绑定本机环境（{s['environment']['wsl_gcc']} / "
            f"{s['environment']['local_gcc']}）与 8 个具体资产；不推荐外推到其他工具链组合。"
            "wunsequenced / compile-time 两个资产恒为 unknown（本机无对应检测器）⇒ "
            "任何以 8 资产为分母的「未知率」都被这两个常量资产抬高。",
            "所有「检出率」都必须在 OR 口径（任一资产 catch）与 unknown 不当 miss 的前提下读数；"
            "单独引用某一资产的 catch 率时须带该资产名与分母。",
        ],
        "rai:dataBiases": [
            f"植入偏差：{s['planted_true_pct_labelled']}%（有标签口径）/ "
            f"{s['planted_true_pct_all']}%（全体口径）为人工植入 —— 人工构造的缺陷往往比真实缺陷"
            "更「典型」，会系统性抬升可检出性。",
            "构造偏差：样本为可直接编译运行的最小片段（无构建系统、无第三方依赖、无跨进程场景），"
            "真实工程中的构建期/链接期/运行期耦合被剥离。",
            "克隆偏差：全库仅 572 种不同代码结构（批内克隆率 62.2%）；跨批近克隆 103 对（676k）。"
            "统计时若不按 clone-family 切分，会在家族内泄漏（677b 已给出 clone-aware split 对照）。",
            "类别失衡：34 类中 13 类盲区率 >50%（最高四类 100%：cross_tu_ub / strict_aliasing / "
            "uninitialized_read 及 volatile_misuse 92.9%）⇒ 类别级结论只在该类样本数（20–92）内成立。",
            "来源偏差：74 条 CVE 重写样本经教学化简化（剥离原始上下文），其「真实感」弱于原物；"
            "本库不能声称覆盖 CVE 分布。",
            "标签不确定性：单标注者 + AI self-consistency（kappa=0.77）；未经人类第三方 IAA。"
            "676k 统一 15 类词表后 kappa 从 0.59（原始词表）升至 0.77，说明词表定义本身影响一致性读数。",
        ],
        "rai:personalSensitiveInformation": (
            "None. 样本为 C++ 代码片段与缺陷标注，不含个人数据、人口统计属性、地理位置、"
            "健康/政治/宗教信息或用户行为数据。少量样本的来源字段引用公开 CVE 编号与开源项目名"
            "（如 Shellshock、Dirty Pipe 的公开记录），不含个人信息。"),
        "rai:dataUseCases": [
            "已确立效度：检测器/净化器能力边界审计 —— 度量「给定资产组合能覆盖哪类缺陷、在哪些类型上"
            "系统性失明」，以及资产互补性与边际贡献（Shapley/LOO 可直接在判定矩阵上复算）。",
            "已确立效度：验证器选择策略的评测 —— failure-driven 选择 vs 随机 vs 静态基线的同预算对照"
            "（预注册 k=4；1137 子集，详见仓库 682 敏感性分析）。",
            "已确立效度：标签质量与词表研究 —— 跨批标签统一、κ 一致性、近克隆检测的方法学案例。",
            "未确立效度：训练缺陷分类器/LLM —— 语料为教学化片段、类别失衡、标签经 AI 自洽性校验"
            "而非人类 IAA，不构成监督学习基准。",
            "未确立效度：推断真实世界缺陷率、评估生产代码质量、跨语言泛化。",
        ],
        "rai:dataSocialImpact": (
            "正面：把「检测器到底能看见什么」变成可复现、可打断、可否证的公开证据；"
            "揭示 sanitizer/静态分析的系统性盲区（38.4%），有助于抵制「上工具即安全」的错觉；"
            "全部源码与判定可离线复现，不依赖付费服务。"
            "风险：把盲区率误读为「代码质量差」或「工具无用」；把自撰语料的表现误读为真实工程表现；"
            "把 AI self-consistency 的 κ=0.77 误当人类标注者一致性。"
            "缓解：数据卡与 README 明确 scope；所有率均带分母与口径；本 RAI 字段逐条声明局限。"),
        "rai:hasSyntheticData": True,
        "rai:hasSyntheticDataNote": (
            "True：样本为人工编写或对公开缺陷记录的等价重写（无生成模型合成、无数据增强）。"
            "「合成」在这里指由作者构造而非从现有代码库采样。"),
        "prov:wasDerivedFrom": [
            f"{GITHUB} —— 主仓：样本、检测器与判定矩阵的产生地（本数据集随仓库分发）。",
            "data/holdout_expansion/DATASHEET.md —— 数据卡：含 74 条 source-derived 样本的 "
            "CVE/GitHub issue 来源字段（source.{type,id,url,project,commit,simplification}）。",
        ],
        "prov:wasGeneratedBy": [
            "corpus-construction：扩样生成 data/expansion_676c*/**（676c 批次，expA–expG 共 1042 条）；"
            "每条含 sample_*.json 标注 + 可编译源码；固定种子见各自脚本。",
            "label-migration：676m 标签迁移（56→33 类词表 + 行号/文件定位修正，308/1042 改写）→ "
            "677a 增补 provenance → 681 跨源标签修复（413 行 defect_type + 34 行 expected_verdict "
            "重派生，已落盘 data/681_标签修复日志.json）。",
            "detection-run：8 资产真机检测 tools/holdout_reveal_661.py::detect（673u 修复版，"
            "sha256_16=4c7a9e3d8a35faa6），每样本×每资产一次真实调用，"
            "execution_model=real_per_asset_detect；矩阵 1147×8，零缺失格。",
            "label-quality-audit：676k AI 盲化双标注（n=131）：Cohen's kappa —— defect_type 0.77"
            "（统一 15 类）/0.59（原始词表）、expected_verdict 0.69、planted 0.71；"
            "此为 AI self-consistency，非人类 IAA。",
        ],
        "rai:dataCollection": (
            "样本由项目作者编写（自撰）或从公开缺陷记录（CVE/GitHub issue）等价重写为单文件可编译片段；"
            "无爬取、无用户数据、无众包。判定矩阵由本机 8 个检测资产真实执行产生（非人工打分）。"),
        "rai:dataCollectionType": ["Manual Human Curation", "Document analysis",
                                   "Direct measurement", "Software Collection"],
        "rai:dataAnnotationProtocol": (
            "单标注者（作者）依 SCHEMA.md 的 34 类闭集与行号口径标注 defect_type/位置/严重度/植入标记；"
            "expected_verdict 为独立检测器判据（catch=至少一资产有报告；挂起=miss）。"
            "676k 以 AI 盲化双标注做自洽性审计（κ 见上），人类第三方 IAA 仍未做（开放威胁 T17）。"),
        "rai:dataAnnotationPlatform": ["Local annotation files (JSON, one per sample)",
                                       "tools/fix_676m_schema.py (deterministic label migration)"],
        "rai:annotationsPerItem": "1 (single annotator) + AI blind re-annotation for agreement audit",
        "rai:dataReleaseMaintenancePlan": (
            "随论文仓库长期维护（GitHub LiaoRanran/CPP-Bible）；判定矩阵与统计按批次版本化"
            "（676f/676g/681/682…）；每次标签或检测器变更产生新批次文件而不原地覆盖；"
            "弃用策略：旧批次保留在仓库内并在 VERSION.md 登记，不做静默替换。"),
    })
    return doc


# ─────────────────────────────────────────────────────────────────────────────
# RAI 展开版
# ─────────────────────────────────────────────────────────────────────────────
def build_rai() -> dict:
    cro = build_croissant()
    keys = ["rai:dataLimitations", "rai:dataBiases", "rai:personalSensitiveInformation",
            "rai:dataUseCases", "rai:dataSocialImpact", "rai:hasSyntheticData",
            "prov:wasDerivedFrom", "prov:wasGeneratedBy"]
    minimal = {k: cro[k] for k in keys}
    return {
        "schema": "queyi-682-rai-metadata/v1",
        "generated_by": "tools/gen_682_metadata.py",
        "generated_at": _now(),
        "purpose": ("RAI 元数据展开版：与 data/croissant.json 内 RAI 字段**同源同值**，"
                    "补齐 Croissant RAI 规范（v1.0）中的其他维度和人类可读说明。"
                    "NeurIPS 2026 E&D 要求 RAI 最小字段集嵌入 Croissant 文件（已满足）；"
                    "本文件用于论文附录引用与审稿快速阅读。"),
        "conformance": {
            "croissant_core": "http://mlcommons.org/croissant/1.0",
            "croissant_rai": "http://mlcommons.org/croissant/RAI/1.0",
            "neurips_2026_minimal_rai_fields_required": keys,
            "note_on_hasSyntheticData": (
                "rai:hasSyntheticData 出现在 NeurIPS 2026 Hosting Guidelines 的最小字段表中，"
                "但不在 Croissant RAI v1.0 的 20 属性表内（后者发布于 2024-03，此后可能已扩展）——"
                "本文件按 NeurIPS 指南保留该字段名。"),
        },
        "minimal_rai_fields": minimal,
        "croissant_rai_v1_extra_dimensions": {
            "rai:dataCollection": cro["rai:dataCollection"],
            "rai:dataCollectionType": cro["rai:dataCollectionType"],
            "rai:dataAnnotationProtocol": cro["rai:dataAnnotationProtocol"],
            "rai:dataAnnotationPlatform": cro["rai:dataAnnotationPlatform"],
            "rai:annotationsPerItem": cro["rai:annotationsPerItem"],
            "rai:dataReleaseMaintenancePlan": cro["rai:dataReleaseMaintenancePlan"],
        },
        "structured": {
            "data_sources": {
                "self_authored": {"n": 968, "scope": "1042 扩样中的自撰片段"},
                "source_derived_reconstruction": {"n": 74,
                    "scope": "CVE/GitHub issue 等价重写（单文件教学化）"},
                "original_external_artifact": {"n": 0,
                    "scope": "本库不含原始外部代码；若将来收录须附许可与来源"},
                "legacy_and_holdout": "105 条（holdout 41 + corpus 64）为早期批次，口径同上",
                "authoritative": "data/holdout_expansion/SCHEMA.md §2.1（provenance 枚举）",
            },
            "annotation_process": {
                "annotators": 1,
                "second_pass": "AI blind re-annotation (676k, n=131) + 682 批次 25% AI re-annotation",
                "agreement": {"defect_type_canon_15class_kappa": 0.773385,
                              "defect_type_raw_kappa": 0.588221,
                              "expected_verdict_kappa": 0.688992,
                              "planted_kappa": 0.708477,
                              "caliber": "AI self-consistency, NOT human IAA"},
                "label_migrations": ["676m: 56→33 类 + 定位修正（308/1042 改写）",
                                     "677a: provenance 派生",
                                     "681: 跨源标签修复（413 + 34 行）"],
                "open_threat": "T17 —— 人类第三方标注复核仍未做",
            },
            "known_biases": {
                "planted_share": "93.2%（有标签口径 1009/1083）；全体口径 88.0%（含 64 条 null）",
                "language": "C++ only",
                "environment": "WSL g++ 13.3.0 / MinGW g++ 13.1.0 / clang 22.1.8（win32）",
                "clone_rate_pct": 62.2, "distinct_structures": 572,
                "class_imbalance": "n∈[7, 92]；13 类盲区率>50%",
                "teaching_fragments": "无构建系统/无第三方依赖；构建期与运行期耦合被剥离",
            },
            "privacy_and_ethics": {
                "personal_data": "none",
                "sensitive_attributes": "none",
                "consent": "not applicable（无人类受试者）",
                "ethics_review": "not required（不含人类受试者/动物/敏感数据）",
                "dual_use": "低风险：缺陷语料可被用于改进检测器（正向）或被误读为代码质量指标（已在局限声明）",
            },
            "scope_and_limits": {
                "valid_for": ["检测器能力边界审计", "资产互补性/边际贡献分析",
                              "验证器选择策略评测", "标签词表方法学研究"],
                "invalid_for": ["真实世界缺陷率推断", "生产代码质量评分",
                                "缺陷分类器训练基准", "跨语言泛化声明"],
                "key_numbers_disclaimer": "所有比例须带分母与口径（OR、unknown 不当 miss、"
                                          "6 可用资产 vs 8 资产池）",
            },
            "maintenance": {
                "repository": GITHUB,
                "versioning": "批次式（676f/676g/681/682…）；不原地覆盖既有产物",
                "update_policy": "标签或检测器变更 ⇒ 新批次文件 + VERSION.md 登记",
                "contact": "1026708211@qq.com",
            },
        },
        "honest_notes": [
            "本文件由脚本生成（tools/gen_682_metadata.py）；minimal_rai_fields 与 "
            "data/croissant.json 的同名字段由同一次运行产生 ⇒ 不可能漂移。",
            "Croissant 官方验证器（mlcroissant）与在线 RAI 编辑器的实测结果登记在 "
            "data/682_规范调研摘要.md 与验收报告中。",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 自校验
# ─────────────────────────────────────────────────────────────────────────────
REQUIRED_CORE = ["@context", "@type", "dct:conformsTo", "description", "license", "name",
                 "url", "creator", "datePublished", "distribution", "recordSet"]
REQUIRED_RAI = ["rai:dataLimitations", "rai:dataBiases", "rai:personalSensitiveInformation",
                "rai:dataUseCases", "rai:dataSocialImpact", "rai:hasSyntheticData",
                "prov:wasDerivedFrom", "prov:wasGeneratedBy"]


def self_check() -> int:
    cro = _jload(OUT_CROISSANT)
    rai = _jload(OUT_RAI)
    s = compute_stats()
    checks = []

    def ck(cid, name, ok, detail=""):
        checks.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})

    ck("C1a", "croissant.json 必填字段齐", all(k in cro for k in REQUIRED_CORE),
       f"缺：{[k for k in REQUIRED_CORE if k not in cro]}")
    ck("C1b", "RAI 8 最小字段齐", all(k in cro for k in REQUIRED_RAI),
       f"缺：{[k for k in REQUIRED_RAI if k not in cro]}")
    ck("C1c", "@type == sc:Dataset", cro.get("@type") == "sc:Dataset")
    ck("C1d", "recordSet ≥4 且含 key/field", len(cro["recordSet"]) >= 4 and all(
        "field" in rs and len(rs["field"]) > 0 for rs in cro["recordSet"]))
    st = cro["queyi:stats"]
    ck("C2a", "样本数 1147", st["n_samples"] == s["n_samples"] == 1147)
    ck("C2b", "类型数 34", st["n_defect_types"] == 34 == s["n_types"])
    ck("C2c", "检测器数 8", st["n_detectors"] == 8 == s["n_detectors"])
    ck("C2d", "检出率 61.6 / 盲区率 38.4",
       st["detection_rate_pct"] == 61.6 and st["blindspot_rate_pct"] == 38.4,
       f"{st['detection_rate_pct']}/{st['blindspot_rate_pct']}")
    bad = []
    for fo in [d for d in cro["distribution"] if d["@type"] == "cr:FileObject"]:
        sha, size = _sha_size(fo["contentUrl"])
        if sha != fo["sha256"] or str(size) != str(fo["contentSize"]):
            bad.append(fo["contentUrl"])
    ck("C3", "FileObject sha256/contentSize 复算一致", not bad, f"不一致：{bad}")
    missing = [d["@id"] for d in cro["distribution"]
               if d["@type"] == "cr:FileObject" and not (ROOT / d["contentUrl"]).is_file()]
    fs_missing = []
    for d in cro["distribution"]:
        if d["@type"] == "cr:FileSet":
            base = ROOT / d["@id"]
            if not base.is_dir():
                fs_missing.append(d["@id"])
    ck("C4", "distribution 路径全部存在", not missing and not fs_missing,
       f"缺：{missing + fs_missing}")
    ck("C5", "RAI 字段非空", all(bool(cro[k]) for k in REQUIRED_RAI))
    ck("C6", "rai_metadata.json 与 croissant RAI 同源",
       all(json.dumps(rai["minimal_rai_fields"][k], sort_keys=True)
           == json.dumps(cro[k], sort_keys=True) for k in REQUIRED_RAI))
    ck("C7", "关键免责在场（AI self-consistency / 非人类 IAA）",
       "AI self-consistency" in json.dumps(cro, ensure_ascii=False)
       and "NOT human IAA" in json.dumps(cro, ensure_ascii=False))

    # C8：官方 mlcroissant 校验（库缺失时如实记 skip，不假装通过）
    official = {"status": "skipped", "why": "mlcroissant 不在环境"}
    try:
        import contextlib
        import io as _io
        import mlcroissant as mlc
        buf = _io.StringIO()
        with contextlib.redirect_stderr(buf):
            ds = mlc.Dataset(jsonld=str(OUT_CROISSANT))
        official = {"status": "loaded", "name": ds.metadata.name,
                    "n_record_sets": len(ds.metadata.record_sets),
                    "warnings": buf.getvalue().strip().splitlines()[-3:]}
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001 —— 校验失败要如实上报
        official = {"status": "error", "type": type(e).__name__, "message": str(e)[:1500]}
    ck("C8", "官方 mlcroissant 校验（loaded 且无 error）", official["status"] == "loaded",
       json.dumps({k: v for k, v in official.items() if k != "warnings"}, ensure_ascii=False))

    verdict = "pass" if all(c["ok"] for c in checks) else "fail"
    for c in checks:
        print(f"[682-A] {'OK  ' if c['ok'] else 'FAIL'} {c['id']} {c['name']}"
              + (f" — {c['detail']}" if c['detail'] else ""), flush=True)
    print(f"[682-A] 自校验判定 {verdict}", flush=True)
    _jwrite(ROOT / "data" / "682_metadata_selfcheck.json",
            {"schema": "queyi-682-metadata-selfcheck/v1", "generated_at": _now(),
             "checks": checks, "verdict": verdict})
    return 0 if verdict == "pass" else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="682 Croissant/RAI 元数据生成")
    ap.add_argument("--stage", default="all", choices=["croissant", "rai", "check", "all"])
    a = ap.parse_args(argv)
    if a.stage in ("croissant", "all"):
        _jwrite(OUT_CROISSANT, build_croissant())
        raw = OUT_CROISSANT.read_text(encoding="utf-8")
        assert json.loads(raw), "回读失败"
        print(f"[682-A] 写 {OUT_CROISSANT.name}（{len(raw)} bytes）", flush=True)
    if a.stage in ("rai", "all"):
        _jwrite(OUT_RAI, build_rai())
        raw = OUT_RAI.read_text(encoding="utf-8")
        assert json.loads(raw), "回读失败"
        print(f"[682-A] 写 {OUT_RAI.name}（{len(raw)} bytes）", flush=True)
    if a.stage in ("check", "all"):
        return self_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
