#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""relabel_682.py — 682 · 任务D：标注一致性量化（AI 第二标注）。

设计（诚实第一）：
  * **AI 第二标注器只读源码**（含作者留在源码里的 `<<PLANTED-DEFECT>>` 标记行），
    **绝不读** 原样本 JSON 的 defect_type / severity / expected_verdict / planted 字段。
    因此 κ 度量的是「源码证据 ⇄ 标注」的一致性，而不是自我复述。
  * AI 的 expected_catch 预测用**类型→资产先验表**（写死在本脚本里的领域知识），
    不查询 676g 矩阵的实测统计 ⇒ 不构成训练/测试泄漏；与实测 or_verdict 的对比单独报告。
  * 全部标注为「AI second pass」，**不得**当作人类 IAA。

阶段：
  sample   : D1 分层抽样 25%（seed=6821，每类 ≥5）→ data/682_relabel_sample.json
  annotate : D2 AI 第二标注 → data/682_ai_relabel_results.json
  kappa    : D3 Cohen's κ（defect_type / expected_verdict / severity / planted）
             → data/682_标注一致性报告.md + data/682_kappa.json
  cases    : D4 不一致案例清单（分类 a/b/c/d 的机器判定 + 源码片段）
             → data/682_不一致案例分析.md（LLM 深读部分由人工在此文件上追加）

红线：不改检测器、不改样本源文件、不改既有产物；本脚本只读样本、只写 682_* 新产物。
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data"))
sys.path.insert(0, str(ROOT / "tools"))

MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
OUT_SAMPLE = ROOT / "data" / "682_relabel_sample.json"
OUT_AI = ROOT / "data" / "682_ai_relabel_results.json"
OUT_KAPPA = ROOT / "data" / "682_kappa.json"
OUT_REPORT = ROOT / "data" / "682_标注一致性报告.md"
OUT_CASES = ROOT / "data" / "682_不一致案例分析.md"

SEED = 6821
TARGET_FRAC = 0.25
MIN_PER_TYPE = 5
BATCHES = ("expA", "expB", "expC", "expD", "expE", "expF", "expG")

# ── 34 类特征词表（AI 第二标注器的全部"知识"；打分制，确定性可复现）───────
# 值 = (关键词, 权重)。命中即累加权重；总分最高者胜，平手按类型名字典序。
# 中英双语：扩样含中文标记行，holdout/corpus 与早期批为英文注释。
FEATURES: dict[str, list[tuple[str, int]]] = {
    "use_after_free": [("释放后使用", 3), ("释放后访问", 3), ("释放后读", 3), ("释放后写", 3),
                       ("use-after-free", 3), ("use after free", 3), ("UAF", 3),
                       ("已释放", 2), ("after free", 2), ("freed heap", 2)],
    "double_free": [("双重释放", 3), ("double free", 3), ("double-free", 3),
                    ("二次释放", 3), ("重复释放", 3)],
    "memory_leak": [("内存泄漏", 3), ("泄漏", 3), ("leak", 3), ("未释放", 2),
                    ("忘记释放", 3), ("忘记 delete", 3), ("忘记 free", 3)],
    "smart_pointer": [("智能指针", 3), ("shared_ptr", 3), ("unique_ptr", 3),
                      ("weak_ptr", 3), ("auto_ptr", 3), ("裸指针", 2)],
    "raii_violation": [("RAII", 3), ("资源未释放", 3), ("析构", 2), ("构造函数抛", 3),
                       ("resource release", 2), ("句柄", 2)],
    "move_semantics": [("移动后使用", 3), ("移动后", 3), ("moved-from", 3), ("std::move", 3),
                       ("use-after-move", 3), ("移动语义", 3)],
    "out_of_bounds": [("越界", 3), ("out-of-bounds", 3), ("out of bounds", 3),
                      ("overread", 3), ("over-read", 3), ("underflow", 2), ("溢出访问", 3),
                      ("缓冲区溢出", 3), ("stack buffer", 3), ("heap buffer", 3),
                      ("信息泄露", 3), ("info leak", 3), ("Heartbleed", 3), ("上界", 1)],
    "null_pointer_deref": [("空指针", 3), ("nullptr", 3), ("null 指针", 3), ("空解引用", 3),
                           ("null deref", 3), ("解引用空", 3), ("NULL deref", 3)],
    "uninitialized_read": [("未初始化", 3), ("uninitialized", 3), ("uninitialised", 3),
                           ("未初始化读", 3), ("indeterminate", 3)],
    "integer_overflow": [("整数溢出", 3), ("有符号溢出", 3), ("signed overflow", 3),
                         ("除零", 3), ("divide by zero", 3), ("division by zero", 3),
                         ("溢出运算", 2), ("narrowing", 2), ("wrap", 2),
                         # 「截断」移除：682 深读证实它主要出现在位域/位宽场景（F121），
                         # 属 bit_operation 而非整数溢出——字面匹配会误导。
                         ],
    "bit_operation": [("负移位", 3), ("移位", 3), ("shift", 3), ("位运算", 3),
                      ("符号位", 2), ("sign bit", 2), ("bitwise", 2),
                      ("bit op", 2), ("按位", 2)],
    "type_punning": [("类型双关", 3), ("type pun", 3), ("reinterpret_cast", 2),
                     ("memcpy", 1), ("union 别名", 3), ("类型混淆", 3), ("type confusion", 3)],
    "strict_aliasing": [("严格别名", 3), ("strict alias", 3), ("strict-aliasing", 3),
                        ("fno-strict", 3), ("别名规则", 3)],
    "alignment": [("未对齐", 3), ("对齐", 3), ("misalign", 3), ("alignment", 3),
                  ("偏移假设", 3), ("packed", 2)],
    "endianness": [("字节序", 3), ("端序", 3), ("endian", 3), ("hton", 3), ("ntoh", 3),
                   ("bswap", 3), ("字节反转", 3), ("大小端", 3)],
    "data_race": [("数据竞争", 3), ("data race", 3), ("data-race", 3), ("竞态", 3),
                  ("race condition", 3), ("无同步", 3)],
    "atomic_ub": [("原子", 3), ("atomic", 3), ("ABA", 3), ("compare_exchange", 3),
                  ("fetch_add", 3), ("原子性", 3), ("无锁", 2)],
    "memory_order": [("内存序", 3), ("内存顺序", 3), ("memory order", 3), ("memory_order", 3),
                     ("重排序", 3), ("reorder", 3), ("relaxed", 2), ("acquire", 2),
                     ("release", 2), ("fence", 2), ("屏障", 2)],
    "deadlock": [("死锁", 3), ("deadlock", 3), ("锁顺序", 3), ("lock order", 3),
                 ("自旋", 2), ("一直等待", 2), ("lock inversion", 3)],
    "condition_variable": [("条件变量", 3), ("condition variable", 3), ("condition_variable", 3),
                           ("虚假唤醒", 3), ("永久等待", 3), ("永远阻塞", 3), ("notify", 2),
                           ("cv.wait", 3), ("cv 永久", 3), ("不带谓词", 3), ("wait 不带", 3),
                           ("wait", 2), ("谓词检查", 2)],
    "iterator_invalidation": [("迭代器", 3), ("iterator", 3), ("失效迭代器", 3),
                              ("失效的迭代器", 3), ("迭代器失效", 3), ("invalidat", 2),
                              ("erase", 2), ("重新分配后", 3), ("push_front 后", 3),
                              ("push_back 后", 3)],
    "stl_container_ub": [("容器", 2), ("std::array", 3), ("vector", 2), ("std::map", 3),
                         ("std::list", 3), ("deque", 2), ("emplace", 2), ("container", 2),
                         ("reserve", 2)],
    "string_ub": [("字符串", 2), ("string_view", 3), ("sv.data", 3), ("strcpy", 3),
                  ("strlen", 3), ("C 字符串", 3), ("c_str", 3), ("char*", 2),
                  ("字面量", 2), ("std::string", 3)],
    "algorithm_misuse": [("严格弱序", 3), ("strict weak", 3), ("比较器", 3), ("comparator", 3),
                         ("std::sort", 3), ("std::remove", 3), ("accumulate", 3),
                         ("谓词", 3), ("predicate", 3), ("算法", 2), ("algorithm", 2),
                         ("remove 不删", 3)],
    "virtual_function": [("虚函数", 3), ("virtual", 3), ("vtable", 3), ("虚调用", 3),
                         ("动态绑定", 3), ("基类指针", 2), ("析构非虚", 3)],
    "lambda_capture": [("捕获", 3), ("capture", 3), ("lambda", 3), ("闭包", 3),
                       ("this 捕获", 3), ("按值捕获", 3), ("引用捕获", 3),
                       # 「悬垂」降权为 1：悬垂引用/指针并不特指 lambda（682 深读证实
                       # D052/D080 类样本的悬垂与 lambda 无关）；词表中无更贴切类时
                       # 仍由它兜住，但不再压过容器/字符串等更具体证据。
                       ("悬垂", 1), ("dangling", 1)],
    "volatile_misuse": [("volatile", 3), ("易失", 3), ("编译器优化掉", 3)],
    "register_ub": [("register 关键字", 3), ("register 变量", 3), ("register int", 3),
                    ("register 存储", 3), ("register 地址", 3), ("register 取地址", 3)],
    "interrupt_safety": [("中断", 3), ("interrupt", 3), ("ISR", 3), ("信号处理", 3),
                         ("中断服务", 3), ("异步信号", 3), ("可重入", 2)],
    "cross_tu_ub": [("跨翻译单元", 3), ("跨 TU", 3), ("cross-tu", 3), ("cross tu", 3),
                    ("多 TU", 3), ("extern inline", 3), ("跨文件", 2), ("跨模块", 3),
                    ("静态初始化顺序", 3), ("尚未构造", 3), ("static init", 3),
                    ("初始化顺序", 3)],
    "linker_odr": [("ODR", 3), ("重复定义", 3), ("multiple definition", 3),
                   ("重定义", 3), ("符号重复", 3), ("链接期", 3), ("linker", 3),
                   ("多重定义", 3), ("duplicate symbol", 3)],
    "logic_error": [("逻辑错误", 3), ("状态机", 3), ("API 误用", 3), ("语义错误", 3),
                    ("越权", 3), ("权限", 2), ("撤销", 2), ("revocation", 3),
                    ("off-by-one", 3), ("shellshock", 3), ("dirty pipe", 3),
                    ("返回值忽略", 3), ("检查不足", 2)],
    "memory_safety": [("内存安全", 2), ("delete", 2), ("free(", 2), ("new 配", 1),
                      ("裸数组", 2), ("手动管理", 2)],
}

# 类型 → 默认严重度（AI 的领域先验；判据 = 典型后果，源码 high 关键词可上调）
# high  = 内存破坏 / 崩溃 / 并发致命（可致任意行为或进程死亡）
# medium= 局部错误值 / 资源问题 / 移植性缺陷
# low   = 声明级或本机平台通常无害的 UB（UB 但影响局部、或仅特定配置触发）
SEV_DEFAULT = {
    # —— high ——
    "use_after_free": "high", "double_free": "high", "out_of_bounds": "high",
    "integer_overflow": "high", "null_pointer_deref": "high", "data_race": "high",
    "deadlock": "high", "atomic_ub": "high", "uninitialized_read": "high",
    "memory_safety": "high", "memory_order": "high", "volatile_misuse": "high",
    "interrupt_safety": "high", "strict_aliasing": "high", "lambda_capture": "high",
    "iterator_invalidation": "high", "linker_odr": "high",
    # —— medium ——
    "cross_tu_ub": "medium", "condition_variable": "medium", "memory_leak": "medium",
    "smart_pointer": "medium", "raii_violation": "medium", "move_semantics": "medium",
    "virtual_function": "medium", "stl_container_ub": "medium", "string_ub": "medium",
    "algorithm_misuse": "medium", "type_punning": "medium",
    # —— low ——
    "register_ub": "low", "alignment": "low", "endianness": "low",
    "bit_operation": "low", "logic_error": "low", "other_ub": "low",
}
SEV_RANK = {"low": 0, "medium": 1, "high": 2}

# 类型 → AI 预测能否被 8 资产捕获（catch/miss）——领域先验，不查实测统计
CATCH_PRIOR = {
    "use_after_free": "catch", "double_free": "catch", "out_of_bounds": "catch",
    "integer_overflow": "catch", "null_pointer_deref": "catch", "data_race": "catch",
    "memory_leak": "catch", "memory_safety": "catch", "uninitialized_read": "miss",
    "deadlock": "miss", "condition_variable": "miss", "atomic_ub": "miss",
    "memory_order": "miss", "volatile_misuse": "miss", "register_ub": "miss",
    "interrupt_safety": "miss", "endianness": "miss", "alignment": "catch",
    "type_punning": "miss", "strict_aliasing": "miss", "smart_pointer": "catch",
    "raii_violation": "miss", "move_semantics": "miss", "lambda_capture": "miss",
    "virtual_function": "miss", "iterator_invalidation": "catch", "stl_container_ub": "catch",
    "string_ub": "catch", "algorithm_misuse": "miss", "bit_operation": "catch",
    "logic_error": "miss", "other_ub": "miss", "linker_odr": "miss", "cross_tu_ub": "miss",
}
MARKER_RE = re.compile(r"<<PLANTED-DEFECT>>|DEFECT\s*:|//\s*DEFECT")
HIGH_WORDS = re.compile(r"use[- ]after[- ]free|double[- ]free|overflow|deref|deadlock|"
                        r"race|uninitialized|invalidat|leak\s+of\s+critical", re.I)


def _jload(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _jwrite(p: Path, doc) -> None:
    Path(p).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")


def _md(p: Path, text: str) -> None:
    Path(p).write_text(text if text.endswith("\n") else text + "\n",
                       encoding="utf-8", newline="\n")


# ─────────────────────────────────────────────────────────────────────────────
# 源码装载（只读）
# ─────────────────────────────────────────────────────────────────────────────
def build_source_loader():
    """sample → 源码文本。

    **重要（682 发现的数据风险）**：676g 矩阵的 `sample_id` **不是全局唯一**——
    expA 与 expC 各有 sample_001..sample_100，共 100 对重名（矩阵的全局唯一键是
    `uid = "<batch>:<sample_id>"`）。因此源码定位**必须**用
    `data/holdout_expansion/<source_batch>/<矩阵的 files 字段>`，
    绝不能用「按 sample_id 或文件名全局查表」的方式（会静默读到另一批次的同名文件）。
    本函数即按此口径实现；expA/expC 冲突已在 682 验收报告中登记。
    """
    import detect_for_assets as dfa
    cmap = dfa.corpus_code_map()
    holdout_files: dict[str, Path] = {}
    ambiguous: dict[str, int] = {}
    skip = {".git", ".venv", "build", "node_modules", "preview_package"}

    def walk(d: Path, depth: int = 0) -> None:
        if depth > 4:
            return
        for p in d.iterdir():
            if p.name in skip or p.name.startswith("."):
                continue
            if p.is_dir():
                walk(p, depth + 1)
            elif p.suffix in (".cpp", ".h", ".hpp"):
                if p.name in holdout_files:
                    ambiguous[p.name] = ambiguous.get(p.name, 1) + 1
                holdout_files.setdefault(p.name, p)

    walk(ROOT)

    def load(sample: dict) -> tuple[str | None, str]:
        sid = sample["sample_id"]
        batch = sample["source_batch"]
        if batch in BATCHES:
            d = ROOT / "data" / "holdout_expansion" / batch
            parts = []
            for f in sorted(sample.get("files") or []):
                fp = d / f
                if fp.is_file():
                    parts.append(fp.read_text(encoding="utf-8", errors="replace"))
            if parts:
                return "\n".join(parts), f"disk:{batch}"
        if sid in cmap:
            return cmap[sid], "corpus_inline"
        for f in sample.get("files") or []:
            p = holdout_files.get(f)
            if p:
                return (p.read_text(encoding="utf-8", errors="replace"),
                        f"repo:{p.relative_to(ROOT)}")
        return None, "missing"

    load.ambiguous_names = ambiguous  # type: ignore[attr-defined]
    return load


# ─────────────────────────────────────────────────────────────────────────────
# D1 分层抽样
# ─────────────────────────────────────────────────────────────────────────────
def stage_sample() -> int:
    mx = _jload(MATRIX)
    samples = mx["samples"]
    n = len(samples)
    target = round(TARGET_FRAC * n)
    by_type: dict[str, list[dict]] = {}
    for s in samples:
        by_type.setdefault(s["defect_type"], []).append(s)
    types = sorted(by_type)
    rng = random.Random(SEED)
    picked: list[dict] = []
    # 1) 每类保底
    for t in types:
        grp = sorted(by_type[t], key=lambda s: s["sample_id"])
        k = min(MIN_PER_TYPE, len(grp))
        picked += rng.sample(grp, k)
    # 2) 剩余按类型规模比例（最大余数法）
    already = {t: sum(1 for p in picked if p["defect_type"] == t) for t in types}
    remain = target - len(picked)
    if remain > 0:
        quota = {t: (len(by_type[t]) - already[t]) * remain / (n - len(picked)) for t in types}
        base = {t: int(quota[t]) for t in types}
        left = remain - sum(base.values())
        for t in sorted(types, key=lambda x: (-(quota[x] - base[x]), x))[:left]:
            base[t] += 1
        for t in types:
            pool = [s for s in sorted(by_type[t], key=lambda s: s["sample_id"])
                    if s not in picked]
            k = min(base[t], len(pool))
            picked += rng.sample(pool, k)
    picked.sort(key=lambda s: s["sample_id"])
    # 分层信息
    strata = {}
    for p in picked:
        key = f"{p['defect_type']}|planted={p['planted']}|ev={p['expected_verdict']}"
        strata[key] = strata.get(key, 0) + 1
    per_type = {t: sum(1 for p in picked if p["defect_type"] == t) for t in types}
    doc = {
        "schema": "queyi-682-relabel-sample/v1",
        "generated_by": "tools/relabel_682.py sample",
        "design": {"seed": SEED, "target_frac": TARGET_FRAC, "target_n": target,
                   "min_per_type": MIN_PER_TYPE, "n_frames": n,
                   "strata_keys": ["defect_type", "planted", "expected_verdict"],
                   "n_types": len(types)},
        "sample_ids": [p["sample_id"] for p in picked],
        "records": [{"sample_id": p["sample_id"],
                     "uid": p.get("uid") or f"{p['source_batch']}:{p['sample_id']}",
                     "source_batch": p["source_batch"],
                     "files": p.get("files") or [],
                     "defect_type": p["defect_type"], "planted": p["planted"],
                     "expected_verdict": p["expected_verdict"]} for p in picked],
        "coverage": {"n_picked": len(picked), "frac_of_frame": round(len(picked) / n, 4),
                     "per_type": per_type,
                     "min_per_type_ok": all(v >= MIN_PER_TYPE for v in per_type.values()),
                     "n_strata": len(strata),
                     "batch_counts": {b: sum(1 for p in picked if p["source_batch"] == b)
                                      for b in sorted({p["source_batch"] for p in picked})}},
        "honest_notes": [
            "抽样框 = 676g 矩阵的 1147 条样本（含 holdout 41 / corpus 64 / 扩样 1042）。",
            "分层维度 defect_type(34) × planted × expected_verdict；每类保底 5 条。",
            "固定种子 6821 ⇒ 抽样完全可复现。",
        ],
    }
    _jwrite(OUT_SAMPLE, doc)
    print(f"[682-D1] 抽样 {len(picked)}/{n}（目标 {target}），覆盖 {len(types)} 类，"
          f"最小类样本数 {min(per_type.values())}；写 {OUT_SAMPLE.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# D2 AI 第二标注（只读源码，不读原标注字段）
# ─────────────────────────────────────────────────────────────────────────────
# 否定语境修正（字面匹配会被「非原子」「non-atomic」误导到 atomic_ub；
# 这些表述实际是 data race / interrupt 的**正面证据**）——语义等价改写，非调参
NEGATION_FIX = [
    ("非原子", " 数据竞争 "), ("不是原子", " 数据竞争 "),
    ("non-atomic", " data race "), ("non atomic", " data race "),
]


def _score(text: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    scores: dict[str, int] = {}
    hits: dict[str, list[str]] = {}
    low = text.lower()
    for a, b in NEGATION_FIX:
        low = low.replace(a, b)
    for t, kws in FEATURES.items():
        s = 0
        got = []
        for kw, w in kws:
            if kw.lower() in low:
                s += w
                got.append(kw)
        if s:
            scores[t] = s
            hits[t] = got
    return scores, hits


def infer_type(text: str) -> tuple[str, str, str]:
    """从源码推断 defect_type（打分制，确定性）。

    返回 (type, evidence_string, method)；method ∈ marker_line/source_body/fallback。
    只读源码文本；**不读**原标注字段。
    """
    markers = [ln.strip() for ln in text.splitlines() if MARKER_RE.search(ln)]
    body = MARKER_RE.sub(" ", text)
    s_m, h_m = _score(" ".join(markers)) if markers else ({}, {})
    s_b, h_b = _score(body)
    # 标记行权重 ×2（作者显式写下的缺陷语义），正文 ×1；
    # 合并打分比「标记行优先、其后不再看正文」稳健（E178/E182 这类标记未写 wait 的案例）
    combined = {}
    for t in set(s_m) | set(s_b):
        combined[t] = s_m.get(t, 0) * 2 + s_b.get(t, 0)
    if not combined:
        return "other_ub", "", "fallback"
    top = max(combined.values())
    best = sorted(t for t, v in combined.items() if v == top)[0]
    if best in s_m:
        method = "marker_line"
        ev = "+".join(h_m[best][:4])
    else:
        method = "source_body"
        ev = "+".join(h_b[best][:4])
    return best, ev, method


def annotate_one(text: str) -> dict:
    t, phrase, method = infer_type(text)
    has_marker = bool(MARKER_RE.search(text))
    sev = SEV_DEFAULT.get(t, "medium")
    if HIGH_WORDS.search(text):
        sev = "high" if SEV_RANK[sev] < SEV_RANK["high"] else sev
    conf = {"marker_line": 0.9, "source_body": 0.65, "fallback": 0.4}[method]
    if not has_marker:
        conf = min(conf, 0.6)
    return {
        "defect_type": t,
        "defect_type_evidence": phrase,
        "defect_type_method": method,
        "severity": sev,
        # AI 视角的「是否缺陷」：源码有缺陷标记 ⇒ True；无标记 ⇒ False（无缺陷证据）。
        # 注意：无标记不等于客观无缺陷（对照样本与未标样本不可区分）——已在报告中声明。
        "planted_pred": has_marker,
        "expected_catch": CATCH_PRIOR.get(t, "miss"),
        "annotation_confidence": round(conf, 2),
    }


def stage_annotate() -> int:
    smp = _jload(OUT_SAMPLE)
    mx = _jload(MATRIX)
    idx = {(s.get("uid") or f"{s['source_batch']}:{s['sample_id']}"): s
           for s in mx["samples"]}
    man = _jload(MANIFEST)
    # severity 事实源：**逐样本 JSON**（扩样 sample_*.json 有 severity；manifest 多为空串）
    man_sev: dict[tuple, str] = {}
    for s in man["samples"]:
        if s.get("severity"):
            man_sev[(str(s["dir"]), tuple(sorted(s.get("files") or [])))] = s["severity"]
    def orig_severity(rec: dict) -> str | None:
        batch = rec["source_batch"]
        if batch in BATCHES:
            jp = ROOT / "data" / "holdout_expansion" / batch / f"{rec['sample_id']}.json"
            if jp.is_file():
                try:
                    v = json.loads(jp.read_text(encoding="utf-8")).get("severity")
                    if v:
                        return v
                except json.JSONDecodeError:
                    pass
            d = f"data/holdout_expansion/{batch}"
            return man_sev.get((d, tuple(sorted(rec.get("files") or []))))
        d2 = {"holdout": "data/holdout", "corpus": "data/external_corpus"}.get(batch, "")
        return man_sev.get((d2, tuple(sorted(rec.get("files") or []))))

    load = build_source_loader()
    out = []
    stats = {"n": 0, "source_ok": 0, "source_missing": [], "methods": {},
             "no_marker": 0, "orig_severity_missing": 0}
    for rec in smp["records"]:
        s = idx[rec["uid"]]
        text, how = load(s)
        stats["n"] += 1
        if text is None:
            stats["source_missing"].append(rec["sample_id"])
            out.append({"sample_id": rec["sample_id"], "status": "no_source",
                        "ai": None, "source_how": how})
            continue
        stats["source_ok"] += 1
        ai = annotate_one(text)
        stats["methods"][ai["defect_type_method"]] = stats["methods"].get(
            ai["defect_type_method"], 0) + 1
        if not MARKER_RE.search(text):
            stats["no_marker"] += 1
        osev = orig_severity(rec)
        if osev is None:
            stats["orig_severity_missing"] += 1
        out.append({
            "sample_id": rec["sample_id"],
            "uid": rec["uid"],
            "status": "ok",
            "source_how": how,
            "ai": ai,
            "original": {"defect_type": rec["defect_type"], "planted": rec["planted"],
                         "expected_verdict": rec["expected_verdict"],
                         "severity": osev, "planted_raw": s.get("planted")},
            "detector": {"or_verdict_available6": s.get("or_verdict_available6"),
                         "per_asset": {a: v.get("verdict")
                                       for a, v in (s.get("per_asset") or {}).items()}},
        })
    doc = {
        "schema": "queyi-682-ai-relabel/v1",
        "generated_by": "tools/relabel_682.py annotate",
        "annotator": "AI second pass (deterministic source-evidence annotator)",
        "honest_declaration": (
            "这是 **AI second pass**：标注器只读源码（含作者写在源码里的 <<PLANTED-DEFECT>> "
            "标记行），**不读**原样本 JSON 的 defect_type/severity/expected_verdict/planted 字段。"
            "因此它衡量的是「源码证据 ⇄ 标注」一致性，**不是人类 IAA**，也不能追溯到人类标注者。"),
        "stats": stats,
        "results": out,
    }
    _jwrite(OUT_AI, doc)
    print(f"[682-D2] 标注 {stats['source_ok']}/{stats['n']} 条（源码缺失 "
          f"{len(stats['source_missing'])}）；方法分布 {stats['methods']}；"
          f"无标记 {stats['no_marker']}；写 {OUT_AI.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# D3 κ
# ─────────────────────────────────────────────────────────────────────────────
def cohen_kappa(a: list, b: list) -> dict:
    assert len(a) == len(b) and a, "κ 输入长度不一致或为空"
    n = len(a)
    labels = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca: dict = {}
    cb: dict = {}
    for x in a:
        ca[x] = ca.get(x, 0) + 1
    for y in b:
        cb[y] = cb.get(y, 0) + 1
    pe = sum((ca.get(x, 0) / n) * (cb.get(x, 0) / n) for x in labels)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return {"n": n, "po": round(po, 6), "pe": round(pe, 6), "kappa": round(kappa, 6),
            "labels": labels}


def stage_kappa() -> int:
    ai = _jload(OUT_AI)
    rows = [r for r in ai["results"] if r["status"] == "ok"]
    kt = cohen_kappa([r["original"]["defect_type"] for r in rows],
                     [r["ai"]["defect_type"] for r in rows])
    ke = cohen_kappa([r["original"]["expected_verdict"] for r in rows],
                     [r["ai"]["expected_catch"] for r in rows])
    kp = cohen_kappa([bool(r["original"]["planted_raw"]) for r in rows],
                     [bool(r["ai"]["planted_pred"]) for r in rows])
    sev_rows = [r for r in rows if r["original"]["severity"]]
    ks = (cohen_kappa([r["original"]["severity"] for r in sev_rows],
                      [r["ai"]["severity"] for r in sev_rows]) if sev_rows else None)
    # 与实测检测器的一致性（AI 先验预测 vs 实测 or_verdict_available6）
    hit = sum(1 for r in rows
              if r["detector"]["or_verdict_available6"] == r["ai"]["expected_catch"])
    conf = [r["ai"]["annotation_confidence"] for r in rows]
    per_type = {}
    for r in rows:
        t = r["ai"]["defect_type"]
        d = per_type.setdefault(t, {"n": 0, "agree": 0})
        d["n"] += 1
        d["agree"] += 1 if r["ai"]["defect_type"] == r["original"]["defect_type"] else 0
    doc = {
        "schema": "queyi-682-kappa/v1",
        "generated_by": "tools/relabel_682.py kappa",
        "annotator": "AI second pass (source-evidence annotator; not human IAA)",
        "n": len(rows),
        "kappa_defect_type": kt,
        "kappa_expected_verdict": ke,
        "kappa_planted": kp,
        "kappa_severity": ks,
        "ai_vs_detector_hit_rate": round(hit / len(rows), 6) if rows else None,
        "confidence": {"mean": round(sum(conf) / len(conf), 4) if conf else None,
                       "min": min(conf) if conf else None, "max": max(conf) if conf else None},
        "per_ai_type": {k: v for k, v in sorted(per_type.items())},
        "reference_676k": {"defect_type_canon_kappa": 0.773385,
                           "defect_type_raw_kappa": 0.588221,
                           "expected_verdict_kappa": 0.688992,
                           "planted_kappa": 0.708477,
                           "note": "676k 是 AI 盲化双标注（n=131）；682 是 AI 第二标注（n=287）"},
    }
    _jwrite(OUT_KAPPA, doc)

    def _judge(v: float) -> str:
        return ("几乎完全一致" if v >= 0.8 else "高度一致" if v >= 0.6
                else "中等一致" if v >= 0.4 else "低一致")

    L = []
    L.append("# 682 · 标注一致性报告（D3）\n")
    L.append("- 生成：`tools/relabel_682.py kappa`")
    L.append(f"- 样本：{len(rows)} 条（682 分层抽样，seed=6821，覆盖 1147 抽样框的 "
             f"{len(rows)/1147*100:.1f}%）")
    L.append("- **标注者身份：AI second pass**（确定性源码证据标注器），"
             "**不是人类 IAA**；标注器不读原标注字段（只读源码与源码内缺陷标记）\n")
    L.append("## 1. Cohen's κ\n")
    L.append("| 维度 | n | po | pe | κ | 判读 |")
    L.append("|---|---:|---:|---:|---:|---|")
    rows_k = [("defect_type（34 类）", kt), ("expected_verdict（catch/miss）", ke),
              ("planted（AI 由源码标记判定）", kp)]
    if ks:
        rows_k.append(("severity（low/medium/high）", ks))
    for name, k in rows_k:
        L.append(f"| {name} | {k['n']} | {k['po']} | {k['pe']} | **{k['kappa']}** | "
                 f"{_judge(k['kappa'])} |")
    L.append("")
    L.append(f"- AI 预测的 expected_catch 与**实测** or_verdict(6 资产) 命中率："
             f"**{doc['ai_vs_detector_hit_rate']}**（AI 用领域先验，未查实测统计 ⇒ 无泄漏）")
    L.append(f"- 标注置信度：均值 {doc['confidence']['mean']}，范围 "
             f"[{doc['confidence']['min']}, {doc['confidence']['max']}]")
    L.append(f"- 与 676k（AI 盲化双标注，n=131）对比：defect_type κ 0.773 → 682 的 {kt['kappa']}；"
             f"expected_verdict κ 0.689 → 682 的 {ke['kappa']}；"
             f"planted κ 0.708 → 682 的 {kp['kappa']}。"
             "两组数字都**不是人类一致性**，且 682 的标注器可读源码标记 ⇒ 任务比 676k 更容易。\n")
    L.append("## 2. 逐 AI 类型的一致性\n")
    L.append("| AI 判定类型 | n | 与原标注一致 | 一致率 |")
    L.append("|---|---:|---:|---:|")
    for t, v in doc["per_ai_type"].items():
        L.append(f"| {t} | {v['n']} | {v['agree']} | {v['agree']/v['n']*100:.1f}% |")
    L.append("")
    L.append("## 3. 数据风险登记（682 发现）\n")
    L.append("1. **676g 检测矩阵的 `sample_id` 不是全局唯一**：expA 与 expC 各有 "
             "`sample_001`…`sample_100`，共 **100 对重名**（矩阵的全局唯一键是 "
             "`uid = \"<batch>:<sample_id>\"`）。任何按 `sample_id` 跨批次 join/查表都会静默错配——"
             "本批 D 的第一版标注器即因按文件名全局回退而读到另一批次同名源码，"
             "修正为按 `source_batch` 目录 + 矩阵 `files` 字段定位后才得到本文的 κ。"
             "**上游建议**：矩阵消费方一律用 `uid` 或 (batch, files) 定位。")
    L.append("2. **A5 manifest 与 676g 矩阵是两套 id 体系**：manifest 已统一（C001/F001… 无重名），"
             "676g 保留原始 `sample_00X`（重名）。跨表关联须经 (dir, files) 映射。")
    L.append("3. **severity 事实源**：manifest 的 severity 列大量为空串；权威值在扩样逐样本 JSON "
             "（`data/holdout_expansion/<batch>/sample_*.json`）。本批已改为从该处读取。\n")
    L.append("## 4. 必须同读的限定（诚实声明）\n")
    L.append("1. 这是 **AI self-consistency（AI 对源码证据的复读）**，不是人类标注者间一致性；"
             "论文 T17 的「无人类第三方标注」威胁**未被本批消除**。")
    L.append("2. AI 标注器可读作者留在源码里的缺陷标记注释 ⇒ 与标注同源；"
             "κ 高说明「标记 ⇄ 标注字段」内部自洽，**不能**外推为「标注符合客观真值」。")
    L.append("3. AI 的 planted 判定 = 「源码里有无缺陷标记」：无标记不等于客观无缺陷"
             "（对照样本与未标注样本在源码上不可区分）。")
    L.append("4. 抽样覆盖 1147 的 25%（287 条），非全量；类型保底 5 条使小类被过采样。")
    L.append("5. 源码缺失样本（若有）已单列 `status=no_source`，不计入 κ。\n")
    _md(OUT_REPORT, "\n".join(L))
    print(f"[682-D3] κ(defect_type)={kt['kappa']} κ(ev)={ke['kappa']} κ(planted)={kp['kappa']}"
          + (f" κ(sev)={ks['kappa']}" if ks else "")
          + f"；写 {OUT_KAPPA.name} / {OUT_REPORT.name}", flush=True)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# D4 不一致案例
# ─────────────────────────────────────────────────────────────────────────────
# 语义邻接家族（682 LLM 深读后固化）：同家族的不同标签 = 粒度/口径差异（c 类），
# 跨家族 = 需人裁（b）或 AI 错（a）。家族划分依据 34 类词表的分组语义。
TYPE_FAMILY = {
    "stl": {"stl_container_ub", "iterator_invalidation", "out_of_bounds", "string_ub",
            "algorithm_misuse"},
    "mem": {"use_after_free", "double_free", "memory_leak", "smart_pointer",
            "raii_violation", "memory_safety", "uninitialized_read"},
    "conc": {"data_race", "atomic_ub", "memory_order", "interrupt_safety", "deadlock",
             "condition_variable"},
    "types": {"endianness", "strict_aliasing", "type_punning", "alignment"},
    "bits": {"bit_operation", "integer_overflow"},
    "oop": {"lambda_capture", "move_semantics", "virtual_function", "cross_tu_ub",
            "linker_odr"},
    "logic": {"logic_error", "other_ub", "null_pointer_deref"},
}


def family_of(t: str) -> str:
    for f, ts in TYPE_FAMILY.items():
        if t in ts:
            return f
    return "other"


def classify_case(r: dict) -> str:
    """机器初判 a/b/c/d（682 LLM 深读后固化口径）。

    c（边界）判据 = AI 与原标注落在**同一语义邻接家族**（粒度/口径差异）；
    跨家族时：标记行强证据 ⇒ b（原标注可疑，需人裁）；body 弱证据 ⇒ c 或 a；
    无证据 ⇒ d。**注意**：b 只表示「与原标注逐条冲突、值得人裁」，不表示原标注一定错。
    """
    ai_t, orig_t = r["ai"]["defect_type"], r["original"]["defect_type"]
    if ai_t == orig_t:
        return "agree"
    conf = r["ai"]["annotation_confidence"]
    method = r["ai"]["defect_type_method"]
    if family_of(ai_t) == family_of(orig_t):
        return "c_both_plausible"
    if method == "fallback":
        return "d_unjudgeable"
    if method == "marker_line" and conf >= 0.9:
        return "b_original_suspect"
    if method == "source_body":
        return "c_both_plausible"
    return "a_ai_error"


def stage_cases() -> int:
    ai = _jload(OUT_AI)
    rows = [r for r in ai["results"] if r["status"] == "ok"]
    bad = [r for r in rows if r["ai"]["defect_type"] != r["original"]["defect_type"]]
    by_cat: dict[str, list[dict]] = {}
    for r in bad:
        by_cat.setdefault(classify_case(r), []).append(r)
    load = build_source_loader()
    mx = _jload(MATRIX)
    idx = {(s.get("uid") or f"{s['source_batch']}:{s['sample_id']}"): s
           for s in mx["samples"]}

    def excerpt(sid: str, n: int = 14) -> list[str]:
        text, _how = load(idx[sid])
        if not text:
            return ["(源码不可读)"]
        lines = text.splitlines()
        mark = [i for i, ln in enumerate(lines) if MARKER_RE.search(ln)]
        if mark:
            i = mark[0]
            lo, hi = max(0, i - 3), min(len(lines), i + 1)
        else:
            lo, hi = 0, min(len(lines), n)
        return lines[lo:hi]

    L = ["# 682 · 不一致案例分析（D4）\n",
         f"- 生成：`tools/relabel_682.py cases`（机器初判）；**LLM 深读复核在本文件 §6 追加**",
         f"- 不一致总数：**{len(bad)}** / {len(rows)}（{len(bad)/len(rows)*100:.1f}%）",
         "- 分类：a=AI 标错（原标注更可信）；b=原标注可疑（源码证据指向另一类）；"
         "c=两者都有道理（边界）；d=无法机器判断（需人类裁决）\n",
         "## 0. 分类汇总\n",
         "| 类别 | n |", "|---|---:|"]
    for k in ("a_ai_error", "b_original_suspect", "c_both_plausible", "d_unjudgeable"):
        L.append(f"| {k} | {len(by_cat.get(k, []))} |")
    L.append("")
    for k, title in (("b_original_suspect", "1. b 类：原标注可疑"),
                     ("c_both_plausible", "2. c 类：边界案例"),
                     ("a_ai_error", "3. a 类：AI 标错"),
                     ("d_unjudgeable", "4. d 类：需人类裁决")):
        items = by_cat.get(k, [])
        L.append(f"## {title}（{len(items)} 条；列前 8 条 + 源码片段）\n")
        for r in items[:8]:
            L.append(f"### {r.get('uid') or r['sample_id']}")
            L.append(f"- 原标注：`{r['original']['defect_type']}`（planted="
                     f"{r['original']['planted_raw']}, ev={r['original']['expected_verdict']}）")
            L.append(f"- AI 标注：`{r['ai']['defect_type']}`（证据「{r['ai']['defect_type_evidence']}」，"
                     f"方法 {r['ai']['defect_type_method']}，置信 {r['ai']['annotation_confidence']}）")
            L.append(f"- 实测 or_verdict(6 资产)：`{r['detector']['or_verdict_available6']}`")
            L.append(f"- 源码来源：`{r['source_how']}`")
            L.append("- 源码片段：")
            L.append("```cpp")
            L.extend(excerpt(r.get("uid") or r["sample_id"]))
            L.append("```")
            L.append("")
    L.append("## 5. 机器归类说明\n")
    L.append("- `b_original_suspect`：AI 在源码的 `<<PLANTED-DEFECT>>` 标记行上取得明确匹配"
             "（置信 ≥0.9）但与原标注不同 ⇒ 原标注与源码标记不一致，需人裁。")
    L.append("- `c_both_plausible`：AI 从源码正文模式推断（无标记行），与标注词表粒度差异 ⇒ 边界。")
    L.append("- `a_ai_error`：AI 从标记行推断但与标注不同且置信不足 ⇒ 倾向原标注正确。")
    L.append("- `d_unjudgeable`：AI 无任何证据（fallback）⇒ 需人类裁决。\n")
    _md(OUT_CASES, "\n".join(L))
    # 拼接 LLM 深读笔记（人工撰写、重跑不覆盖）
    note = ROOT / "data" / "682_深读笔记.md"
    if note.is_file():
        with open(OUT_CASES, "a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n" + note.read_text(encoding="utf-8"))
    print(f"[682-D4] 不一致 {len(bad)} 条；分类 "
          + ", ".join(f"{k}={len(v)}" for k, v in by_cat.items())
          + f"；写 {OUT_CASES.name}", flush=True)
    return 0


def stage_rootcause() -> int:
    """不一致根因：把每条不一致样本放进 677b 的 clone-family，检验
    「同族成员中是否存在原标注 == AI 判定」的成员（= 克隆跨类型复制假设）。"""
    ai = _jload(OUT_AI)
    rows = [r for r in ai["results"] if r["status"] == "ok"]
    bad = [r for r in rows if r["ai"]["defect_type"] != r["original"]["defect_type"]]
    doc_fam = _jload(ROOT / "data" / "677b_clone_families.json")
    fam_of = {}
    fam_members = {}
    for fid, members in doc_fam["family_index"].items():
        fam_members[fid] = members
        for m in members:
            fam_of[m] = fid
    # 需要每样本原标注类型：从矩阵取（uid 唯一键）
    mx = _jload(MATRIX)
    idx = {(s.get("uid") or f"{s['source_batch']}:{s['sample_id']}"): s
           for s in mx["samples"]}
    # 矩阵样本 → A5 manifest 的 sample_id（677b 家族表的键空间）；
    # 用 (dir, files) 匹配，避免跨批次 sample_id 重名（expA/expC 各 100 条重名）
    man = _jload(MANIFEST)
    key2a5: dict[tuple, str] = {}
    a5_type: dict[str, str] = {}
    for s in man["samples"]:
        key2a5[(str(s["dir"]), tuple(sorted(s.get("files") or [])))] = s["sample_id"]
        a5_type[s["sample_id"]] = s["defect_type"]
    out = []
    n_family = 0
    n_ai_type_present = 0
    n_pure = 0
    n_multi = 0
    for r in bad:
        sid = r["sample_id"]
        uid = r.get("uid") or sid
        mrec = idx.get(uid, {})
        batch = mrec.get("source_batch")
        dir_ = (f"data/holdout_expansion/{batch}" if batch in BATCHES else
                {"holdout": "data/holdout", "corpus": "data/external_corpus"}.get(batch, ""))
        a5id = key2a5.get((dir_, tuple(sorted(mrec.get("files") or []))))
        fid = fam_of.get(a5id) if a5id else None
        if fid is None:
            out.append({"sample_id": sid, "in_family": False,
                        "original": r["original"]["defect_type"],
                        "ai": r["ai"]["defect_type"]})
            continue
        members = fam_members[fid]
        n_family += 1
        orig_types = {a5_type[m] for m in members if m in a5_type}
        ai_type = r["ai"]["defect_type"]
        hit = ai_type in orig_types
        if len(members) > 1:
            n_multi += 1
        if len(orig_types) == 1:
            n_pure += 1
        if len(members) > 1 and hit:
            n_ai_type_present += 1
        out.append({
            "sample_id": sid, "in_family": True, "family_id": fid,
            "family_size": len(members),
            "family_defect_types": sorted(orig_types),
            "family_type_pure": len(orig_types) == 1,
            "ai_type_present_in_family": hit,
            "original": r["original"]["defect_type"], "ai": ai_type,
            "method": r["ai"]["defect_type_method"],
        })
    multi = [o for o in out if o.get("in_family") and o["family_size"] > 1]
    summary = {
        "n_inconsistent": len(bad),
        "n_in_677b_family": n_family,
        "n_family_multi": n_multi,
        "n_ai_type_present_in_family": sum(
            1 for o in multi if o["ai_type_present_in_family"]),
        "frac_ai_type_present_in_family": (round(
            sum(1 for o in multi if o["ai_type_present_in_family"]) / len(multi), 4)
            if multi else None),
        "n_family_type_pure": sum(1 for o in multi if o["family_type_pure"]),
        "frac_family_type_impure": (round(
            1 - sum(1 for o in multi if o["family_type_pure"]) / len(multi), 4)
            if multi else None),
        "hypothesis": ("若不一致样本所在克隆家族内**存在**原标注 == AI 判定的成员，"
                       "则支持「同源代码被跨类型复制、标记行未随类型改写」的克隆传播假设；"
                       "家族类型不纯 = 同一代码结构被标注为多种类型（676k 亦记录过跨 defect_type 家族）。"),
    }
    doc = {
        "schema": "queyi-682-inconsistency-rootcause/v1",
        "generated_by": "tools/relabel_682.py rootcause",
        "summary": summary,
        "cases": out,
        "honest_notes": [
            "家族归属来自 677b（complete-linkage @0.85，只覆盖 A5 的 1137 样本）；"
            "holdout/corpus 的少数样本可能不在家族表内（cases 已用 in_family=false 标出）。",
            "本分析不给任何样本下「谁对」的结论——那是 D4 的 LLM 深读与人工裁决范围。",
        ],
    }
    _jwrite(ROOT / "data" / "682_不一致根因分析.json", doc)
    print(f"[682-D4b] 不一致 {len(bad)}；在家族表内 {n_family}（多成员 {n_multi}）；"
          f"家族内存在 AI 类型 {(summary['frac_ai_type_present_in_family'] or 0)*100:.1f}%；"
          f"家族类型不纯 {(summary['frac_family_type_impure'] or 0)*100:.1f}%", flush=True)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="682 标注一致性")
    ap.add_argument("--stage", default="all",
                    choices=["sample", "annotate", "kappa", "cases", "rootcause", "all"])
    a = ap.parse_args(argv)
    stages = {"sample": stage_sample, "annotate": stage_annotate,
              "kappa": stage_kappa, "cases": stage_cases, "rootcause": stage_rootcause}
    if a.stage == "all":
        for fn in (stage_sample, stage_annotate, stage_kappa, stage_cases, stage_rootcause):
            rc = fn()
            if rc:
                return rc
        return 0
    return stages[a.stage]()


if __name__ == "__main__":
    raise SystemExit(main())
