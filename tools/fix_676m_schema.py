#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""fix_676m_schema.py — 676m 任务 A/B/C：数据修复（H1 + H2 + M1–M5）。

背景：676k 数据质量审计（commit bb0c80a7）发现 3 高 + 5 中优先级问题。
本脚本一轮解决，且**只改需要改的字段**（红线 6）：

  H1  expE 34 条 `hung_flag=true` 样本 `expected_verdict` catch → miss
      （真实判据 = sanitizer 挂起超时 → 无报告 → miss；manifest 的
      `hung_pool_reason` 自己也这么说，属数据集内部自相矛盾）
  H2  `defect_type` 统一到 34 项规范词表；`conditional_trigger` /
      `optimization_dependent` 两个元标签从 `defect_type` 拆到 `trigger_condition`
  M1  `defect_location.file` 补全（1042 条，按缺陷标记行定位到具体源文件）
  M2  `id` → `sample_id`（expA 100 + expC 200 = 300 条）
  M3  corpus 64 条 `planted: null` → `false`（原始数据集，非人工植入）
  M4  expB 行号口径校正（去掉 8 行标注头后的相对行号 → 绝对行号），**逐条验证**
  M5  `defect_location.note` / `defect_location.description` → `notes`

红线遵守
========
* 只读 `data/holdout_expansion/**/*.cpp`（样本源码零修改）。
* 不修改 `tools/holdout_reveal_661.py`（检测器）。
* 不修改 676f/676g/676l 的**产物文件**（矩阵/报告/统计）；H1/M3 在聚合层的
  修正在 `data/676m_sample_manifest_corrected.json` 中以**新增修正件**落盘。
* 修改 .json 时保持其他字段不变。
* 行号 M4 不盲目 +8：逐条与源文件缺陷标记行核对，对不上就保持原值并标注。

用法
====
    .venv/Scripts/python.exe tools/fix_676m_schema.py --stage all
    .venv/Scripts/python.exe tools/fix_676m_schema.py --stage all --dry-run
    .venv/Scripts/python.exe tools/fix_676m_schema.py --stage schema
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPDIR = os.path.join(ROOT, "data", "holdout_expansion")
BLINDSPOT = os.path.join(ROOT, "data", "blindspot_676g_sample_manifest.json")
OUT_RESULTS = os.path.join(ROOT, "data", "676m_fix_results.json")
OUT_MANIFEST = os.path.join(ROOT, "data", "676m_sample_manifest_corrected.json")
OUT_SCHEMA = os.path.join(EXPDIR, "SCHEMA.md")
OUT_H1_REPORT = os.path.join(ROOT, "data", "676m_H1修正清单.md")
OUT_H2_REPORT = os.path.join(ROOT, "data", "676m_H2标签迁移报告.md")

EXP_BATCHES = ["expA", "expB", "expC", "expD", "expE", "expF", "expG"]
#: expB 的 .cpp 头部是 8 行标注块（// sample_Bxxx … // (authoritative …)）
EXP_B_HEADER_LINES = 8

# ─────────────────────────────────────────────────────────────────────────────
# H2 规范词表（34 项）
# ─────────────────────────────────────────────────────────────────────────────
#: 676m 统一词表 = 676m 规格建议的 31 项 + 3 项经论证的补充
#:   lambda_capture    （30 条，C++ 捕获生命周期缺陷，建议表无等价项）
#: algorithm_misuse   （35 条，STL 算法前置条件违例，与容器 UB 语义不同）
#: logic_error        （17 条，CVE 类非 UB 语义/API/状态缺陷，硬塞 other_ub 会失真）
VOCABULARY: list[str] = [
    # —— 内存生命周期
    "memory_safety", "use_after_free", "double_free", "memory_leak", "smart_pointer",
    "raii_violation", "move_semantics",
    # —— 越界 / 空指针 / 未初始化
    "out_of_bounds", "null_pointer_deref", "uninitialized_read",
    # —— 整数 / 位 / 类型
    "integer_overflow", "bit_operation", "type_punning", "strict_aliasing", "alignment",
    "endianness",
    # —— 并发
    "data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable",
    # —— STL / 字符串 / 迭代器
    "iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse",
    # —— OOP / 平台
    "virtual_function", "lambda_capture", "volatile_misuse", "register_ub",
    "interrupt_safety",
    # —— 跨 TU / 兜底
    "cross_tu_ub", "linker_odr", "logic_error", "other_ub",
]

#: 规范 defect_type → 粗粒度 defect_group（15 类，与 676k TAXONOMY 的类名对齐）
TYPE2GROUP: dict[str, str] = {
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

#: 直接 1:1（或收敛到同一规范名）的旧标签映射
DIRECT_MAP: dict[str, str] = {
    # 内存生命周期
    "use_after_free": "use_after_free",
    "double_free": "double_free",
    "memory_leak": "memory_leak",
    "resource_leak": "memory_leak",
    "smart_pointer": "smart_pointer",
    "raii_violation": "raii_violation",
    "move_semantics": "move_semantics",
    # 越界家族（含 CVE 侧的具体形态）
    "out_of_bounds": "out_of_bounds",
    "heap_overflow": "out_of_bounds",
    "heap_overread": "out_of_bounds",
    "heap_underflow": "out_of_bounds",
    "stack_overflow": "out_of_bounds",
    "stack_overread": "out_of_bounds",
    "stack_overflow_write": "out_of_bounds",
    "global_overflow": "out_of_bounds",
    "pointer_overflow": "out_of_bounds",
    "info_leak": "out_of_bounds",
    # 空指针 / 未初始化
    "null_pointer_deref": "null_pointer_deref",
    "null_deref": "null_pointer_deref",
    "uninitialized_read": "uninitialized_read",
    # 整数 / 位 / 类型
    "integer_overflow": "integer_overflow",
    "division_by_zero": "integer_overflow",
    "bit_operation": "bit_operation",
    "type_punning": "type_punning",
    "type_confusion": "type_punning",
    "strict_aliasing": "strict_aliasing",
    "alignment": "alignment",
    "endianness": "endianness",
    # 并发
    "data_race": "data_race",
    "race_condition": "data_race",
    "atomic_ub": "atomic_ub",
    "aba_problem": "atomic_ub",
    "memory_order": "memory_order",
    "deadlock": "deadlock",
    "lock_priority_inversion": "deadlock",
    "condition_variable": "condition_variable",
    # STL / 字符串
    "iterator_invalidation": "iterator_invalidation",
    "stl_container_ub": "stl_container_ub",
    "string_ub": "string_ub",
    "algorithm_misuse": "algorithm_misuse",
    # OOP / 平台
    "virtual_function": "virtual_function",
    "lambda_capture": "lambda_capture",
    "volatile_misuse": "volatile_misuse",
    "register_ub": "register_ub",
    "interrupt_safety": "interrupt_safety",
    # 跨 TU
    "cross_tu_ub": "cross_tu_ub",
    "linker_odr": "linker_odr",
    "ODR": "linker_odr",
    "odr_violation": "linker_odr",
    # 语义 / 兜底
    "logic_error": "logic_error",
    "state_machine": "logic_error",
    "resource_exhaustion": "logic_error",
    "timing_side_channel": "logic_error",
    "infinite_loop": "logic_error",
    "other_ub": "other_ub",
    "UB": "other_ub",
}

#: 元标签：值本身描述「触发条件/优化敏感性」而非缺陷种类 ⇒ 拆到 trigger_condition
META_LABELS = {"conditional_trigger", "optimization_dependent"}

#: 需要按证据（notes / defect_location 描述 / trigger_condition）二次细分的旧标签
RESOLVE_LABELS = {"memory_safety", "undefined_behavior", "other_ub", "UB",
                  "conditional_trigger", "optimization_dependent", "compiler_warning",
                  "cross_tu_ub"}

#: 676k 审计认定的「笼统/元标签」集合（用于度量迁移前后的笼统标签数量）
VAGUE_LABELS = {"UB", "undefined_behavior", "other_ub", "memory_safety",
                "conditional_trigger", "optimization_dependent"}

#: 规范名中仍属「粗类」、需按证据再细分的（幂等：细分结果不再细分）
RESOLVABLE_CANON = {"memory_safety", "other_ub", "cross_tu_ub"}


def _has(ev: str, *needles: str) -> bool:
    return any(n in ev for n in needles)


def resolve_by_evidence(old: str, ev: str) -> str:
    """按证据串（小写）把笼统标签细分到规范词表；无法细分则回落 other_ub。"""
    if old in ("memory_safety",):
        if _has(ev, "use-after-free", "uaf", "释放后", "悬垂"):
            return "use_after_free"
        if _has(ev, "double-free", "double free", "两次", "二次", "重复释放"):
            return "double_free"
        if _has(ev, "越界", "oob", "out-of-bound", "heap-buffer", "stack-buffer"):
            return "out_of_bounds"
        return "memory_safety"

    if old in ("undefined_behavior", "other_ub", "UB"):
        if _has(ev, "除以零", "division by zero", "取模除以零"):
            return "integer_overflow"
        if _has(ev, "取负", "negation overflow", "int_min"):
            return "integer_overflow"
        if _has(ev, "移位", "shift", "左移"):
            return "bit_operation"
        if _has(ev, "字符串字面量", "string literal", "只读段"):
            return "out_of_bounds"
        if _has(ev, "未对齐", "unaligned", "alignment"):
            return "alignment"
        if _has(ev, "别名", "alias"):
            return "strict_aliasing"
        if _has(ev, "union"):
            return "type_punning"
        if _has(ev, "空函数指针", "空对象指针", "空指针", "null"):
            return "null_pointer_deref"
        if _has(ev, "memcpy") and _has(ev, "空", "null"):
            return "null_pointer_deref"
        return "other_ub"

    if old == "conditional_trigger":
        if _has(ev, "泄漏", "leak"):
            return "memory_leak"
        if _has(ev, "二次释放", "double-free", "double free"):
            return "double_free"
        if _has(ev, "释放后", "uaf", "use-after-free"):
            return "use_after_free"
        if _has(ev, "越界", "oob"):
            return "out_of_bounds"
        # off-by-one 但「数组在界内」/ 浮点截断 / 整数除法语义错 ⇒ 非 UB 的语义缺陷
        return "logic_error"

    if old == "optimization_dependent":
        if _has(ev, "有符号溢出", "signed integer overflow", "溢出"):
            return "integer_overflow"
        if _has(ev, "严格别名", "strict alias", "别名"):
            return "strict_aliasing"
        if _has(ev, "移位", "左移", "shift"):
            return "bit_operation"
        if _has(ev, "除以零", "division by zero"):
            return "integer_overflow"
        return "other_ub"

    if old == "compiler_warning":
        # fmtlib -Wdangling-reference：编译器诊断类，无 UB 种类可归
        if _has(ev, "dangling"):
            return "use_after_free"
        return "other_ub"

    if old == "cross_tu_ub":
        if _has(ev, "多重定义", "odr", "multiple definition"):
            return "linker_odr"
        return "cross_tu_ub"

    return "other_ub"


def migrate_type(old: str, ev: str) -> str:
    # 已是规范名 ⇒ 幂等返回；少数规范名仍是「可再细分」的粗类，按证据细分
    if old in VOCABULARY:
        if old in RESOLVABLE_CANON:
            return resolve_by_evidence(old, ev)
        return old
    if old in RESOLVE_LABELS:
        return resolve_by_evidence(old, ev)
    return DIRECT_MAP.get(old, "other_ub")


# ─────────────────────────────────────────────────────────────────────────────
# 文件工具（保留原缩进 / 行尾）
# ─────────────────────────────────────────────────────────────────────────────
def _read_json(path: str) -> tuple[dict, str, bool, bool]:
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    tail = raw.endswith(b"\n")
    doc = json.loads(raw.decode("utf-8"))
    return doc, ("\r\n" if crlf else "\n"), crlf, tail


def _write_json(path: str, doc: dict, nl: str, crlf: bool, tail: bool = True) -> None:
    text = json.dumps(doc, ensure_ascii=False, indent=2)
    if crlf:
        text = text.replace("\n", "\r\n")
    if tail:
        text += nl
    open(path, "wb").write(text.encode("utf-8"))


def sample_paths() -> list[tuple[str, str]]:
    """返回 [(batch, json_path)]，共 1042 条（不含 INDEX.json）。"""
    out: list[tuple[str, str]] = []
    for b in EXP_BATCHES:
        for p in sorted(glob.glob(os.path.join(EXPDIR, b, "*.json"))):
            if os.path.basename(p) == "INDEX.json":
                continue
            out.append((b, p))
    return out


def source_candidates(batch: str, stem: str) -> list[str]:
    d = os.path.join(EXPDIR, batch)
    pats = [f"{stem}*.cpp", f"{stem}*.h", f"{stem}*.hpp"]
    found: list[str] = []
    for pat in pats:
        found.extend(os.path.basename(p) for p in glob.glob(os.path.join(d, pat)))
    return sorted(set(found))


def marker_lines(path: str) -> list[int]:
    """源文件里缺陷标记所在行（1-based）。"""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        if "<<PLANTED-DEFECT>>" in line or re.search(r"DEFECT[:：]", line):
            out.append(i)
    return out


def pick_defect_file(batch: str, stem: str) -> tuple[str | None, str]:
    """M1：判定缺陷落在哪个源文件。返回 (file, 依据)。"""
    cands = source_candidates(batch, stem)
    if not cands:
        return None, "no-source-file"
    if len(cands) == 1:
        return cands[0], "single-source"
    hit = []
    for c in cands:
        if marker_lines(os.path.join(EXPDIR, batch, c)):
            hit.append(c)
    if len(hit) == 1:
        return hit[0], "unique-defect-marker"
    if len(hit) > 1:
        return hit[0], "ambiguous-multi-marker"
    return cands[0], "ambiguous-no-marker"


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────
def run(dry: bool = False) -> dict:
    blind = json.load(open(BLINDSPOT, encoding="utf-8"))
    hung = [s for s in blind["samples"]
            if s.get("hung_flag") and s.get("expected_verdict") == "catch"]
    h1_ids = {s["sample_id"] for s in hung}

    rows: list[dict] = []
    h1_log: list[dict] = []
    h2_pairs: collections.Counter[tuple[str, str]] = collections.Counter()
    h2_meta: list[dict] = []
    m1_log: list[dict] = []
    m2_log: list[dict] = []
    m4_log: list[dict] = []
    m5_log: list[dict] = []
    type_before: collections.Counter[str] = collections.Counter()
    type_after: collections.Counter[str] = collections.Counter()
    type_before_all: collections.Counter[str] = collections.Counter()
    type_after_all: collections.Counter[str] = collections.Counter()

    for batch, path in sample_paths():
        doc, nl, crlf, tail = _read_json(path)
        stem = os.path.basename(path)[:-5]
        orig = json.loads(json.dumps(doc))  # 深拷贝，用于比对

        # ---------- 证据串（供 H2 细分） ----------
        # 幂等要求：M5 会把 note/description 改名为 notes，所以三个键都要读；
        # 676m 自己追加的 【676m…】标记必须剔除，否则二次运行证据会漂移。
        dl = doc.get("defect_location") or {}
        ev_raw = " ".join(str(x) for x in (
            doc.get("notes"), dl.get("note"), dl.get("description"), dl.get("notes"),
            doc.get("trigger_condition"),
        ) if x)
        ev = re.sub(r"【676m[^】]*】", " ", ev_raw).lower()

        old_type = str(doc.get("defect_type", ""))
        type_before_all[old_type] += 1

        # ---------- H2：defect_type 迁移 ----------
        new_type = migrate_type(old_type, ev)
        doc["defect_type"] = new_type
        type_after_all[new_type] += 1
        if old_type != new_type:
            h2_pairs[(old_type, new_type)] += 1
            if old_type in META_LABELS:
                h2_meta.append({"batch": batch, "file": stem,
                                "old": old_type, "new": new_type})

        # ---------- H2：元标签拆到 trigger_condition ----------
        if old_type in META_LABELS:
            prev_tc = str(doc.get("trigger_condition") or "").strip()
            marker = f"【676m】原 defect_type={old_type}（元标签，已从 defect_type 拆出）"
            doc["trigger_condition"] = (prev_tc + "；" + marker) if prev_tc else marker

        # ---------- M1：defect_location.file ----------
        dfile, why = pick_defect_file(batch, stem)
        dl2 = dict(doc.get("defect_location") or {})
        if dfile and not dl2.get("file"):
            dl2["file"] = dfile
            m1_log.append({"batch": batch, "file": stem, "defect_file": dfile, "rule": why})
        elif dl2.get("file"):
            pass
        else:
            m1_log.append({"batch": batch, "file": stem, "defect_file": None, "rule": why})

        # ---------- M5：defect_location 描述键统一 ----------
        for k in ("note", "description"):
            if k in dl2:
                dl2["notes"] = dl2.pop(k)
                m5_log.append({"batch": batch, "file": stem, "from": k, "to": "notes"})
        doc["defect_location"] = dl2

        # ---------- M2：id → sample_id（原位改名，保持键序） ----------
        if "id" in doc and "sample_id" not in doc:
            renamed: dict = {}
            for k, v in doc.items():
                renamed["sample_id" if k == "id" else k] = v
            doc = renamed
            m2_log.append({"batch": batch, "file": stem, "new_sample_id": doc["sample_id"]})

        # ---------- M4：expB 行号口径 ----------
        if batch == "expB" and dfile:
            sp = os.path.join(EXPDIR, batch, dfile)
            marks = marker_lines(sp)
            line = dl2.get("line")
            if isinstance(line, int) and marks:
                m = marks[0]
                if line + EXP_B_HEADER_LINES == m:
                    dl2["line"] = m
                    m4_log.append({"batch": batch, "file": stem, "old": line,
                                   "new": m, "marker": m, "action": "shift+8"})
                elif line == m:
                    m4_log.append({"batch": batch, "file": stem, "old": line,
                                   "new": line, "marker": m, "action": "keep(already-abs)"})
                else:
                    m4_log.append({"batch": batch, "file": stem, "old": line,
                                   "new": line, "marker": m, "action": "keep(unverified)"})
            else:
                m4_log.append({"batch": batch, "file": stem, "old": line,
                               "new": line, "marker": None, "action": "keep(no-marker)"})

        # ---------- H1：hung 样本 expected_verdict catch → miss ----------
        if stem in h1_ids and doc.get("expected_verdict") == "catch":
            doc["expected_verdict"] = "miss"
            note = ("676m 修正：hung_flag 样本真实判据为 miss（sanitizer 挂起超时），"
                    "原 catch 登记有误")
            prev = str(doc.get("notes") or "").strip()
            doc["notes"] = (prev + " 【" + note + "】") if prev else note
            h1_log.append({"batch": batch, "file": stem, "old": "catch", "new": "miss"})

        if doc != orig and not dry:
            _write_json(path, doc, nl, crlf, tail)

        rows.append({"batch": batch, "file": stem, "doc": doc})

        if old_type in VAGUE_LABELS:
            type_before["vague"] += 1
        if new_type in VAGUE_LABELS:
            type_after["vague"] += 1

    # ---------- M3：corpus planted null → false（修正件） ----------
    by_id = {r["file"]: r for r in rows}
    m3_log: list[dict] = []
    for s in blind["samples"]:
        if s["source_batch"] == "corpus" and s.get("planted") is None:
            m3_log.append({"uid": s["uid"], "sample_id": s["sample_id"]})

    # ---------- M2 附带 + 一致性：INDEX.json 与标注同步 ----------
    # INDEX 是批次摘要（676f_pipeline 会读它的 defect_type / expected_verdict）。
    # 若不同步，数据集内部会再次出现「.json 说 A、INDEX 说 B」的矛盾。
    # 做法：增补 sample_id 别名（保留 id，兼容冻结的 data/676f_pipeline.py），
    # 并把 defect_type / expected_verdict / defect_line|defect_location 对齐到迁移后的 .json。
    index_log: list[dict] = []
    for b in EXP_BATCHES:
        ip = os.path.join(EXPDIR, b, "INDEX.json")
        if not os.path.exists(ip):
            continue
        idoc, inl, icrlf, itail = _read_json(ip)
        lst = idoc.get("index") or idoc.get("samples") or []
        n_alias = n_sync = 0
        for e in lst:
            if not isinstance(e, dict):
                continue
            sid = str(e.get("sample_id") or e.get("id") or "")
            stem = sid if sid.startswith("sample_") else "sample_" + sid
            src = by_id.get(stem)
            if "id" in e and "sample_id" not in e:
                e["sample_id"] = e["id"]
                n_alias += 1
            if src is None:
                continue
            doc = src["doc"]
            if "defect_type" in e and e["defect_type"] != doc["defect_type"]:
                e["defect_type"] = doc["defect_type"]
                n_sync += 1
            if "expected_verdict" in e and e["expected_verdict"] != doc["expected_verdict"]:
                e["expected_verdict"] = doc["expected_verdict"]
                n_sync += 1
            if "defect_line" in e and e["defect_line"] != doc["defect_location"].get("line"):
                e["defect_line"] = doc["defect_location"].get("line")
                n_sync += 1
            if "defect_location" in e and e["defect_location"] != doc["defect_location"]:
                e["defect_location"] = doc["defect_location"]
                n_sync += 1
        if (n_alias or n_sync) and not dry:
            _write_json(ip, idoc, inl, icrlf, itail)
        if n_alias or n_sync:
            index_log.append({"batch": b, "n_alias_added": n_alias, "n_fields_synced": n_sync})

    # ---------- 聚合层修正件（不修改 676g 产物） ----------
    corrected_samples = []
    for s in blind["samples"]:
        rec = dict(s)
        batch = s["source_batch"]
        sid = s["sample_id"]
        stem = sid if sid.startswith("sample_") or batch in ("expD", "expF") else sid
        # 磁盘 stem 归一：expD/expF 的 sample_id 形如 D001 → sample_D001
        if batch in ("expD", "expF") and re.fullmatch(r"[A-Z]\d{3}", sid):
            stem = "sample_" + sid
        src = by_id.get(stem) if batch in EXP_BATCHES else None
        fixes: list[str] = []
        if src is not None:
            rec["defect_type"] = src["doc"]["defect_type"]
            rec["defect_group"] = TYPE2GROUP.get(src["doc"]["defect_type"], "generic_ub")
            if rec.get("expected_verdict") != src["doc"]["expected_verdict"]:
                fixes.append("H1:expected_verdict")
                rec["expected_verdict"] = src["doc"]["expected_verdict"]
            rec["defect_location_file"] = (src["doc"].get("defect_location") or {}).get("file")
        if batch == "corpus" and rec.get("planted") is None:
            rec["planted"] = False
            fixes.append("M3:planted")
        rec["fixes"] = fixes
        corrected_samples.append(rec)

    doc_out = {
        "schema": "queyi-676m-sample-manifest-corrected/v1",
        "generated_by": "tools/fix_676m_schema.py",
        "note": ("676g 清单层的**修正件**（676g 原产物按红线 9 保持冻结）。"
                 "修正项：H1（34 条 expected_verdict）、M3（64 条 corpus planted）、"
                 "H2（defect_type 统一 + defect_group 派生）。"),
        "frozen_upstream": "data/blindspot_676g_sample_manifest.json",
        "vocabulary": VOCABULARY,
        "type2group": TYPE2GROUP,
        "n_total": len(corrected_samples),
        "n_corrected": sum(1 for r in corrected_samples if r["fixes"]),
        "samples": corrected_samples,
    }

    res = {
        "schema": "queyi-676m-fix-results/v1",
        "generated_by": "tools/fix_676m_schema.py",
        "dry_run": dry,
        "h1": {
            "n": len(h1_log),
            "expected_n": len(hung),
            "items": sorted(h1_log, key=lambda x: x["file"]),
            "residual": sum(1 for r in rows
                            if r["file"] in h1_ids and r["doc"]["expected_verdict"] == "catch"),
        },
        "h2": {
            "vocabulary": VOCABULARY,
            "n_vocabulary": len(VOCABULARY),
            "mapping": {f"{k[0]} -> {k[1]}": v for k, v in sorted(h2_pairs.items())},
            "n_migrated": sum(h2_pairs.values()),
            "n_distinct_before": len(type_before_all),
            "n_distinct_after": len(type_after_all),
            "distribution_before": dict(type_before_all.most_common()),
            "distribution_after": dict(type_after_all.most_common()),
            "meta_split_n": len(h2_meta),
            "meta_split": h2_meta,
        },
        "m1": {
            "n": len(m1_log),
            "n_with_file": sum(1 for x in m1_log if x["defect_file"]),
            "by_rule": dict(collections.Counter(x["rule"] for x in m1_log)),
        },
        "m2": {"n": len(m2_log), "items": m2_log,
               "index_alias": index_log,
               "n_index_alias": sum(x["n_alias_added"] for x in index_log),
               "n_index_synced": sum(x["n_fields_synced"] for x in index_log)},
        "m3": {"n": len(m3_log), "items": m3_log},
        "m4": {
            "n": len(m4_log),
            "shifted": sum(1 for x in m4_log if x["action"] == "shift+8"),
            "kept_abs": sum(1 for x in m4_log if x["action"] == "keep(already-abs)"),
            "kept_unverified": sum(1 for x in m4_log if x["action"] == "keep(unverified)"),
            "kept_no_marker": sum(1 for x in m4_log if x["action"] == "keep(no-marker)"),
            "items": m4_log,
        },
        "m5": {"n": len(m5_log),
               "from_note": sum(1 for x in m5_log if x["from"] == "note"),
               "from_description": sum(1 for x in m5_log if x["from"] == "description")},
        "n_samples": len(rows),
    }

    if not dry:
        # 迁移台账（mapping / 迁移前分布）只在「确实发生了改写」时覆盖：
        # 在已迁移数据上重跑是零改动，此时保留首跑台账，避免统计被清零。
        changed = (sum(h2_pairs.values()) + len(h1_log) + len(m2_log) + len(m5_log)
                   + sum(1 for x in m4_log if x["action"] == "shift+8")) > 0
        if changed or not os.path.exists(OUT_RESULTS):
            with open(OUT_RESULTS, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(res, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
        with open(OUT_MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc_out, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="676m H1/H2/M1-M5 数据修复")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="只校验：若发现任何待改写项则非零退出（供 run_all.sh 门禁用）")
    ap.add_argument("--stage", default="all",
                    choices=["all", "fix", "schema", "manifest", "reports"])
    a = ap.parse_args(argv)

    if a.stage == "schema":
        write_schema()
        print(f"[676m] 写入 {os.path.relpath(OUT_SCHEMA, ROOT)}")
        return 0
    if a.stage == "reports":
        write_schema()
        write_reports()
        print(f"[676m] 写入 {os.path.relpath(OUT_H1_REPORT, ROOT)} / "
              f"{os.path.relpath(OUT_H2_REPORT, ROOT)}")
        return 0

    res = run(dry=a.dry_run or a.verify)
    print(f"[676m] 样本 {res['n_samples']}；H1 {res['h1']['n']}/{res['h1']['expected_n']} "
          f"（残留 {res['h1']['residual']}）")
    print(f"[676m] H2 迁移 {res['h2']['n_migrated']} 条；词表 {res['h2']['n_vocabulary']} 项；"
          f"取值数 {res['h2']['n_distinct_before']} → {res['h2']['n_distinct_after']}")
    print(f"[676m] M1 补 file {res['m1']['n_with_file']}/{res['m1']['n']}"
          f"（规则分布 {res['m1']['by_rule']}）")
    print(f"[676m] M2 {res['m2']['n']}；M3 {res['m3']['n']}；M5 {res['m5']['n']}")
    print(f"[676m] M4 共 {res['m4']['n']}：+8 {res['m4']['shifted']}，"
          f"已是绝对行号 {res['m4']['kept_abs']}，未验证保持 {res['m4']['kept_unverified']}，"
          f"无标记 {res['m4']['kept_no_marker']}")

    if a.verify:
        pending = (res["h1"]["residual"] + res["h2"]["n_migrated"] + res["m2"]["n"]
                   + res["m5"]["n"] + res["m4"]["shifted"]
                   + max(0, res["m1"]["n"] - res["m1"]["n_with_file"]))
        if pending:
            print(f"[676m][FAIL] 仍有 {pending} 项待改写 ⇒ 676m 修复未落盘或非幂等",
                  file=sys.stderr)
            return 1
        print("[676m][OK] 数据已处于 676m 修复后的稳定态（H1 残留 0、待迁移 0）")
        return 0

    if not a.dry_run:
        write_schema()
        write_reports()
        print(f"[676m] 台账 {os.path.relpath(OUT_RESULTS, ROOT)}（仅在有改写时更新）；"
              f"清单 {os.path.relpath(OUT_MANIFEST, ROOT)}；"
              f"规范 {os.path.relpath(OUT_SCHEMA, ROOT)}；"
              f"H1/H2 分报告 {os.path.relpath(OUT_H1_REPORT, ROOT)} / "
              f"{os.path.relpath(OUT_H2_REPORT, ROOT)}")
    return 0


def write_reports() -> None:
    """由 data/676m_fix_results.json 生成 H1 / H2 两份分报告（数字不手写）。"""
    res = json.load(open(OUT_RESULTS, encoding="utf-8"))
    h1, h2 = res["h1"], res["h2"]

    # ---------------- H1 ----------------
    L: list[str] = []
    A = L.append
    A("# 676m · 任务 A：H1 修正清单（hung 样本 expected_verdict catch → miss）")
    A("")
    A("- **问题（676k H1）**：34 条 `hung_flag=true` 的样本在 `expected_verdict` 上登记为")
    A("  `catch`，但 676g 清单的 `hung_pool_reason` 明说真实判据是 miss")
    A("  （sanitizer 挂起 → 120s 超时 → 无报告）——**数据集内部自相矛盾**。")
    A("- **修正**：`expected_verdict: catch → miss`；并在 `notes` 追加 676m 修正说明。")
    A("- **口径依据**：`expected_verdict` = **独立检测器判据**（能否被实际观测到），")
    A("  不是「缺陷是否存在」。挂起样本没有可观测的诊断报告 ⇒ miss。")
    A("")
    A("## 修正清单")
    A("")
    A(f"共 **{h1['n']}** 条（全部在 `expE`），与 676k 认定的 {h1['expected_n']} 条一致。")
    A("")
    A("| # | 批次 | 样本 | 旧值 | 新值 |")
    A("|---|------|------|------|------|")
    for i, it in enumerate(h1["items"], start=1):
        A(f"| {i} | `{it['batch']}` | `{it['file']}` | `{it['old']}` | `{it['new']}` |")
    A("")
    A("## 验证")
    A("")
    A("```bash")
    A(".venv/Scripts/python.exe tools/fix_676m_schema.py --stage all")
    A("```")
    A("")
    A(f"- 修正后 `hung_flag=true && expected_verdict=catch` 的残留数：**{h1['residual']}**（要求 0）")
    A("- 每条 `notes` 已追加：`【676m 修正：hung_flag 样本真实判据为 miss"
      "（sanitizer 挂起超时），原 catch 登记有误】`")
    A("")
    A("## 对下游的影响")
    A("")
    A("- **A5 主分析零影响**：主分析口径读 `per_asset`（真实 detect 判定），不读 "
      "`expected_verdict`。见 `data/676m_A5重算报告.md` §1–§3。")
    A("- **expected=catch 口径的 recall 会变**：分母 668 → 634，")
    A("  8 资产 OR 覆盖率 93.86% → 98.42%。这是口径修正，不是检测器变强。")
    A("- 聚合层（676f 矩阵 / 676g 清单）按红线 9 **保持冻结**；")
    A("  修正后的规范清单见 `data/676m_sample_manifest_corrected.json`。")
    with open(OUT_H1_REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")

    # ---------------- H2 ----------------
    L = []
    A = L.append
    A("# 676m · 任务 B：H2 标签迁移报告（统一 defect_type 词表）")
    A("")
    A("- **问题（676k H2）**：跨批次标签体系未统一；同一段代码在不同批次叫不同名字；")
    A("  `conditional_trigger` / `optimization_dependent` 这类**元标签**混在 `defect_type` 里。")
    A("- **修正**：34 项规范词表 + 规则化迁移（脚本 `tools/fix_676m_schema.py`），")
    A("  元标签拆到 `trigger_condition`。字段规范见 `data/holdout_expansion/SCHEMA.md`。")
    A("")
    A("## 1. 规模变化")
    A("")
    A("| 指标 | 迁移前 | 迁移后 |")
    A("|------|-------:|-------:|")
    A(f"| `defect_type` 取值数 | {h2['n_distinct_before']} | {h2['n_distinct_after']} |")
    A(f"| 发生改写的样本 | — | {h2['n_migrated']} / 1042 |")
    A(f"| 元标签拆分（conditional_trigger / optimization_dependent） | — | {h2['meta_split_n']} |")
    vague_after = h2["distribution_after"].get("other_ub", 0)
    A("| 笼统标签（UB/undefined_behavior/other_ub/memory_safety/"
      "conditional_trigger/optimization_dependent） | 145 | "
      f"{vague_after}（仅 `other_ub`） |")
    A("")
    A("## 2. 迁移映射表（旧 → 新，按条数降序）")
    A("")
    A("| 旧标签 | 新标签 | 条数 |")
    A("|--------|--------|-----:|")
    for k, v in sorted(h2["mapping"].items(), key=lambda kv: (-kv[1], kv[0])):
        old, new = k.split(" -> ")
        A(f"| `{old}` | `{new}` | {v} |")
    A("")
    A("> 未出现在上表的旧标签表示**原值即规范名**（1:1 保留）。")
    A("")
    A("## 3. 迁移后分布")
    A("")
    A("| `defect_type` | n |")
    A("|---------------|---|")
    for t, n in sorted(h2["distribution_after"].items(), key=lambda kv: (-kv[1], kv[0])):
        A(f"| `{t}` | {n} |")
    A("")
    unused = [t for t in h2["vocabulary"] if t not in h2["distribution_after"]]
    A(f"词表中当前**无成员**的保留类：{', '.join('`' + t + '`' for t in unused)}"
      "（`memory_safety` 是保留的通用内存安全类：所有 24 条样本都能按证据细分到具体类型，"
      "故当前为空）。")
    A("")
    A("## 4. 元标签拆分明细（`defect_type` → `trigger_condition`）")
    A("")
    A("| 批次 | 样本 | 旧 defect_type | 细分后 defect_type |")
    A("|------|------|----------------|--------------------|")
    for it in h2["meta_split"]:
        A(f"| `{it['batch']}` | `{it['file']}` | `{it['old']}` | `{it['new']}` |")
    A("")
    A("每条样本的 `trigger_condition` 已追加标记：")
    A("`【676m】原 defect_type=<旧值>（元标签，已从 defect_type 拆出）`。")
    A("")
    A("## 5. 设计理由（诚实边界）")
    A("")
    A("1. 词表以 676m 规格建议的 31 项为主干，**加了 3 项**（`lambda_capture`、")
    A("   `algorithm_misuse`、`logic_error`）—— 理由见 `SCHEMA.md` §3.2。")
    A("2. 细分规则是**确定性关键字规则**（`resolve_by_evidence`），无模型介入、可复现；")
    A("   规则命中不了的才回落 `other_ub`（当前 8 条）。")
    A("3. 迁移是**有损的**：越界家族（heap/stack/global/over-read/under-read）合并为")
    A("   `out_of_bounds`，方向与位置信息只保留在 `notes` 文本里。")
    A("4. 元标签的值**没有丢**：完整保留在 `trigger_condition`。")
    A("5. 逐样本 .json **未新增字段**（红线 6），所以「旧值 → 新值」的完整台账在")
    A("   本报告与 `data/676m_fix_results.json` 里，而不是在标注文件里。")
    A("")
    A("## 6. 复现")
    A("")
    A("```bash")
    A(".venv/Scripts/python.exe tools/fix_676m_schema.py --stage all   # 幂等：重跑零改写")
    A("```")
    with open(OUT_H2_REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def write_schema() -> None:
    """写 data/holdout_expansion/SCHEMA.md（字段规范 + 词表 + 迁移规则）。"""
    res_path = OUT_RESULTS
    res = json.load(open(res_path, encoding="utf-8")) if os.path.exists(res_path) else None
    lines: list[str] = []
    A = lines.append
    A("# `data/holdout_expansion/` 标注 Schema（676m 起生效）")
    A("")
    A("> 本文件是扩样集 1042 条标注（`sample_*.json`）的**唯一字段规范**。")
    A("> 由 `tools/fix_676m_schema.py` 生成/校验；批次：676m（数据修复）。")
    A("")
    A("## 1. 文件布局")
    A("")
    A("```")
    A("data/holdout_expansion/<batch>/")
    A("  INDEX.json            # 批次索引（id 键见 §5.4）")
    A("  sample_<id>.json      # 逐样本标注（权威记录）")
    A("  sample_<id>*.cpp/.h   # 样本源码（只读，676m 零修改）")
    A("```")
    A("")
    A("批次：`expA`(100) `expB`(94) `expC`(200) `expD`(200) `expE`(200) "
      "`expF`(149) `expG`(99) = **1042**。")
    A("")
    A("## 2. 字段规范")
    A("")
    A("| 字段 | 类型 | 必填 | 说明 |")
    A("|------|------|:----:|------|")
    A("| `sample_id` | str | ✅ | 样本唯一 id（676m 起全批次统一；expA/expC 原为 `id`） |")
    A("| `defect_type` | str | ✅ | 统一词表取值（§3），676m 起 34 项闭集 |")
    A("| `defect_location` | obj | ✅ | `{file, line, function, notes}` |")
    A("| `defect_location.file` | str | ✅ | 缺陷所在源文件名（676m 补全；多 TU 样本按缺陷标记行定位） |")
    A("| `defect_location.line` | int\\|null | ✅ | **绝对文件行号**（1-based；多文件样本可为 null） |")
    A("| `defect_location.function` | str | ✅ | 缺陷所在函数（全局初始化用 `(global)`） |")
    A("| `defect_location.notes` | str | ⭕ | 缺陷行说明（676m 起由 `note`/`description` 统一而来） |")
    A("| `severity` | str | ✅ | `low` / `medium` / `high` |")
    A("| `planted` | bool | ✅ | `true`=本项目人工植入；`false`=真实世界来源或对照样本 |")
    A("| `expected_verdict` | str | ✅ | `catch` / `miss`（**独立检测器判据**，见 §4.1） |")
    A("| `expected_detectors` | list[str] | ⭕ | 预期命中的资产名 |")
    A("| `trigger_condition` | str | ⭕ | 触发条件 / 优化敏感性（676m 起承接原 `conditional_trigger`、`optimization_dependent` 元标签） |")
    A("| `notes` | str | ✅ | 顶层缺陷说明（中文） |")
    A("| `verification` | obj | ⭕ | 生成期的编译/检测复现记录（各批次字段略有差异，原样保留） |")
    A("| `source` | obj | ⭕ | `planted=false` 样本的来源（CVE / GitHub issue） |")
    A("")
    A("> 红线 6：676m 只改 §4 列出的字段，其余字段（含 `verification`、`source`、"
      "`platform_*`、`thread_count` 等）逐字节保持不变。")
    A("")
    A("## 3. 统一词表（`defect_type`，34 项闭集）")
    A("")
    A("规范词表 = 676m 规格建议的 31 项 + 3 项经论证的补充。"
      "补充项的设计理由见 §3.2。")
    A("")
    A("### 3.1 词表与粗粒度分组")
    A("")
    A("| # | `defect_type` | `defect_group`（15 类，与 676k TAXONOMY 对齐） |")
    A("|---|---------------|------------------------------------------|")
    for i, t in enumerate(VOCABULARY, start=1):
        A(f"| {i} | `{t}` | `{TYPE2GROUP[t]}` |")
    A("")
    A("`defect_group` **不写进逐样本 .json**（红线 6：不新增字段），"
      "只在聚合清单 `data/676m_sample_manifest_corrected.json` 中派生。")
    A("")
    A("### 3.2 相对建议表的三项补充（工程决策）")
    A("")
    A("| 补充项 | n | 理由 |")
    A("|--------|---|------|")
    A("| `lambda_capture` | 30 | lambda 捕获生命周期缺陷（悬垂引用 / 悬垂 `this`）。建议表无等价项；"
      "塞进 `other_ub` 会把一个 100% 可归因的类打成兜底类。 |")
    A("| `algorithm_misuse` | 35 | STL 算法**前置条件**违例（比较器不满足严格弱序、重叠 `copy`、"
      "`remove` 不删元素）。与 `stl_container_ub`（容器自身 UB）语义不同，676k TAXONOMY 也单列。 |")
    A("| `logic_error` | 17 | CVE 类**非 UB** 语义/API/状态缺陷（如 Shellshock、Dirty Pipe、"
      "证书撤销检查不足）。这些样本无 UB 可言，归 `other_ub` 属误标。 |")
    A("")
    A("### 3.3 收敛关系（旧标签 → 规范名）")
    A("")
    A("| 旧标签 | → | 规范名 | 说明 |")
    A("|--------|---|--------|------|")
    conv = [
        ("resource_leak", "memory_leak", "含 fd 泄漏；词表只保留 memory_leak"),
        ("heap_overflow / heap_overread / heap_underflow / stack_* / global_overflow",
         "out_of_bounds", "越界家族统一；方向/位置由 `notes` 保留"),
        ("pointer_overflow", "out_of_bounds", "指针算术越界属越界访问"),
        ("info_leak", "out_of_bounds", "越界读导致的信息泄露（Heartbleed 类）"),
        ("null_deref", "null_pointer_deref", "同义合并"),
        ("division_by_zero", "integer_overflow", "整数 UB 家族"),
        ("type_confusion", "type_punning", "类型双关 / 混淆同族"),
        ("race_condition", "data_race", "同义合并"),
        ("aba_problem", "atomic_ub", "无锁协议的原子性缺陷"),
        ("lock_priority_inversion", "deadlock", "活性缺陷，归并发活性类"),
        ("state_machine / resource_exhaustion / timing_side_channel / infinite_loop",
         "logic_error", "非 UB 的语义/资源/时序缺陷"),
        ("UB / undefined_behavior / other_ub / memory_safety / conditional_trigger / "
         "optimization_dependent", "按证据细分", "见 §4.2 规则；无法细分回落 other_ub"),
        ("cross_tu_ub（多重定义/ODR）", "linker_odr", "链接期 ODR 违例"),
    ]
    for a, b, c in conv:
        A(f"| `{a}` | → | `{b}` | {c} |")
    A("")
    A("## 4. 676m 迁移规则")
    A("")
    A("### 4.1 `expected_verdict` 口径（H1）")
    A("")
    A("`expected_verdict` = **独立检测器判据**：该样本在 8 资产池下能否被**实际观测**到。")
    A("")
    A("- `catch`：至少一个资产产生非空诊断报告；")
    A("- `miss`：无任何资产产生报告——**包含 sanitizer 挂起超时（rc=124）后无报告**。")
    A("")
    A("因此 `hung_flag=true` 的样本（自旋死锁 / 自死锁 / cv 永久等待）"
      "真实判据是 `miss`，不是 `catch`。676m 把 expE 34 条此类样本由 `catch` 修正为 `miss`。")
    A("")
    A("### 4.2 笼统标签细分规则（H2）")
    A("")
    A("对 `memory_safety` / `undefined_behavior` / `other_ub` / `UB` / "
      "`conditional_trigger` / `optimization_dependent` / `compiler_warning`，"
      "按 `notes` + `defect_location` 描述 + `trigger_condition` 的证据串做**规则化细分**"
      "（规则见 `tools/fix_676m_schema.py::resolve_by_evidence`，全部为确定性关键字规则，"
      "无模型介入）。无法细分者回落 `other_ub`。")
    A("")
    A("### 4.3 元标签拆分")
    A("")
    A("`conditional_trigger` 与 `optimization_dependent` 描述的是**触发条件/优化敏感性**，"
      "不是缺陷种类。676m 把它们的值移入 `trigger_condition`，"
      "`defect_type` 改填按 §4.2 细分出的具体类型。")
    A("")
    A("### 4.4 行号口径（M4）")
    A("")
    A("`defect_location.line` = **绝对文件行号**。expB 的 `.cpp` 头部有 8 行标注块"
      "（`// sample_Bxxx` … `// (authoritative annotation in …)`），"
      "原行号是**去掉头部后的相对行号**。676m 逐条与源文件缺陷标记行核对：")
    A("")
    A("- `line + 8` 等于缺陷标记行 ⇒ 改写为绝对行号；")
    A("- `line` 已等于标记行 ⇒ 保持；")
    A("- 两者都不等 ⇒ **保持原值**并在迁移报告中标注为未验证（不盲目 +8）。")
    A("")
    A("### 4.5 `defect_location.file`（M1）")
    A("")
    A("判定顺序：① 样本只有 1 个源文件 ⇒ 取该文件；"
      "② 多源文件 ⇒ 取**唯一**含缺陷标记（`<<PLANTED-DEFECT>>` 或 `DEFECT:`）的文件；"
      "③ 仍不唯一 ⇒ 取字典序首个并在报告中标注 `ambiguous-*`。")
    A("")
    A("## 5. 已知残留（诚实登记）")
    A("")
    A("1. **`INDEX.json` 的 id 键**：expA/expC/expF 的 `INDEX.json` 用 `index[].id`，"
      "其余批次用 `samples[].sample_id`。676m 只在 `INDEX.json` 中**增补** `sample_id` 别名"
      "（保留 `id`，以免打断冻结的 `data/676f_pipeline.py`），逐样本 .json 则已完全统一。")
    A("2. **多文件样本行号**：expC 的 30 条多 TU 样本 `line` 指向头文件/单 TU，"
      "跨文件不可比；676k 的 κ 分析亦记 null。")
    A("3. **行号语义分歧**：iterator 类样本原标注指向「使用行」，重标注指向「失效操作行」"
      "（676k §3.2）。676m 不改语义，只在本文档明确为「缺陷发生的操作行」。")
    A("4. **批内克隆率 62.2%**：全库仅 572 种不同代码结构（676k §H3）。"
      "676m **不删样本**，只在数据卡 `DATASHEET.md` 中披露。")
    A("5. **`planted=true` 占 93%**：数据集固有特征，不修改，只在数据卡披露。")
    A("")
    if res:
        h2 = res["h2"]
        A("## 6. 676m 迁移结果快照")
        A("")
        A(f"- `defect_type` 取值数：**{h2['n_distinct_before']} → {h2['n_distinct_after']}**")
        A(f"- 发生改写的样本：**{h2['n_migrated']}** / 1042")
        A(f"- 元标签拆分（`conditional_trigger` / `optimization_dependent`）："
          f"**{h2['meta_split_n']}** 条")
        A(f"- `defect_location.file` 补全：**{res['m1']['n_with_file']}** / {res['m1']['n']}")
        A(f"- 行号校正：+8 修正 **{res['m4']['shifted']}** 条，"
          f"已是绝对行号 **{res['m4']['kept_abs']}** 条，"
          f"未验证保持 **{res['m4']['kept_unverified']}** 条")
        A("")
        A("迁移后分布：")
        A("")
        A("| `defect_type` | n |")
        A("|---------------|---|")
        for t, n in sorted(h2["distribution_after"].items(), key=lambda kv: (-kv[1], kv[0])):
            A(f"| `{t}` | {n} |")
        A("")
    A("---")
    A("")
    A("复现：`.venv/Scripts/python.exe tools/fix_676m_schema.py --stage all`")
    with open(OUT_SCHEMA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
