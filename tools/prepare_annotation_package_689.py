#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""prepare_annotation_package_689.py — 689-C2：人类标注材料包生成（去标签 + 注释净化）。

目标
====
为"独立盲目标注"（验证项目作者标签的 construct validity）准备**去标签**材料包：
第二标注者拿到 ``data/annotation_package/`` 后即可开做，无需接触任何原始标签。

抽样（评审建议口径）
====================
* D2 blind holdout 全部 41 条（最暴露于 reviewer scrutiny）；
* D3 external corpus 全部 64 条；
* A5 分层层：从 676g 的 expA–expG 池按 **family8 家族**分层抽 40 条
  （8 家族 × 5，hung_flag=True 排除并登记；固定种子 6892）。
* 合计 145 条（落于评审建议 135–155 区间）。

去标识化纪律（三重）
====================
1. **匿名 ID + 顺序打乱**：源码复制为 ``sources/S###.cpp``（种子 6892）；
2. **注释净化**：对材料包**副本**（不改动任何源文件）删除/遮盖"泄露原始标签"的注释
   （类型名、检测器名、planted/故意/越界/泄漏等中英文词、文件名）；中性技术注释保留；
3. **本地依赖**：``#include "x.h"`` 的本地头文件同步复制并重命名（防文件名泄露），
   include 行改写。

包外产物
========
* ``data/689_annotation_key_mapping.json``（协调者专用）：anon ↔ uid ↔ 源路径 ↔ 原始标签；
* ``data/689_annotation_leakage_scan.json``：净化后复扫（应为空）+ 净化记录。

用法
====
    python tools/prepare_annotation_package_689.py
"""
from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SYN_MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
EXP_DIR = ROOT / "data" / "holdout_expansion"
CORPUS_DIR = ROOT / "data" / "external_corpus"
PKG_DIR = ROOT / "data" / "annotation_package"
SRC_DIR = PKG_DIR / "sources"
MAPPING = ROOT / "data" / "689_annotation_key_mapping.json"
LEAK_SCAN = ROOT / "data" / "689_annotation_leakage_scan.json"

SEED = 6892
N_STRAT_PER_FAMILY = 5  # A5 分层：8 家族 × 5 = 40

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
TYPE_TO_FAMILY: dict[str, str] = {t: f for f, ts in FAMILY8.items() for t in ts}

#: 英文泄露词（**故意不加词边界**：``defect_type``/``bug_id`` 这类下划线复合词必须命中；
#:  代价是 ``debug``/``trace`` 等中性词也会被过度遮盖——过严优于漏网，红删注释无科学代价）
EN_LEAK = re.compile(
    r"(planted|defect|bug|asan|ubsan|tsan|sanitizer|leak|oob|overflow|underflow|"
    r"deadlock|uninitialized|dangling|punning|vptr|odr|crash|segfault|"
    r"intentional|deliberate|inject|cve|poc|misuse|violation|antipattern|wrong)"
    r"|\bub\b|\brace\b",
    re.IGNORECASE,
)
EN_LEAK2 = re.compile(r"(use[- ]after[- ]free|double[- ]free|out[- ]of[- ]bound|strict alias|"
                      r"undefined behavior|data race|heap-buffer|stack-buffer)", re.IGNORECASE)
FILE_LEAK = re.compile(r"[A-Za-z0-9_./\\-]+\.(cpp|h|hpp|c)\b")
CN_LEAK = ("故意", "缺陷", "注入", "越界", "泄漏", "泄露", "悬垂", "竞争", "死锁",
           "未初始化", "未定义", "二次释放", "重复释放", "未解锁", "野指针", "错配",
           "不匹配", "应报", "会报", "判据", "检测器", "命中", "注入的", "构造的缺陷",
           "第二次", "错误", "误用", "错用", "非法", "无效", "不合法", "违反", "不符",
           "已经释放", "已释放", "释放了", "未释放", "陷阱", "反面", "教训", "本应", "不该",
           "浅拷贝", "深拷贝", "两次析构", "重复析构", "双析构", "所有权")

#: 标识符泄露（用于**确定性重命名**：材料包副本上执行，保持代码可编译）
ID_LEAK_CORE = re.compile(r"plant|buggy|defect|intentional|broken|bad_|_bad|wrong",
                          re.IGNORECASE)


def _neutral_name(name: str, idx: int) -> str:
    low = name.lower()
    if "buggy" in low:
        base = "holder"
    elif "defect" in low:
        base = "flag"
    else:
        base = "alt"
    if name[:1].isupper():
        base = base.capitalize()
    return base if idx == 1 else f"{base}_{idx}"


def _rename_leaky_identifiers(code: str) -> tuple[str, dict[str, str]]:
    """把代码中泄露性标识符（跳过注释/字符串）确定性重命名；返回 (新代码, 映射)。"""
    mapping: dict[str, str] = {}
    idx = 0
    out: list[str] = []
    i, n = 0, len(code)
    quote = ""
    while i < n:
        ch = code[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(code[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "/":
            j = code.find("\n", i)
            j = n if j == -1 else j
            out.append(code[i:j])
            i = j
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "*":
            j = code.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(code[i:j])
            i = j
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (code[j].isalnum() or code[j] == "_"):
                j += 1
            name = code[i:j]
            if ID_LEAK_CORE.search(name):
                new = mapping.get(name)
                if new is None:
                    idx += 1
                    new = _neutral_name(name, idx)
                    mapping[name] = new
                out.append(new)
            else:
                out.append(name)
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out), mapping


def _string_hits(code: str) -> list[str]:
    """收集字符串字面量中命中泄露词的片段（报告用；依赖文件名误报已过滤）。"""
    hits: list[str] = []
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        if ch in "\"'":
            quote = ch
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = code[j]
                if c == "\\" and j + 1 < n:
                    buf.append(code[j:j + 2])
                    j += 2
                    continue
                if c == quote or c == "\n":
                    break
                buf.append(c)
                j += 1
            text = "".join(buf)
            if _leaky(text) and not text.endswith((".h", ".hpp", ".c", ".cpp")):
                hits.append(text[:100])
            i = j + 1
            continue
        i += 1
    return hits


#: 字符串内软化映射（只动字符串字面量；会改程序输出，故严格限于强泄露词）
STRING_SOFTEN = {"buggy": "variantA", "leaked": "total", "defect": "flag"}


def _soften_strings(code: str) -> tuple[str, list[str]]:
    """把字符串字面量内的强泄露词替换为中性词；返回 (新代码, 替换记录)。"""
    out: list[str] = []
    repl: list[str] = []
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        if ch in "\"'":
            quote = ch
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = code[j]
                if c == "\\" and j + 1 < n:
                    buf.append(code[j:j + 2])
                    j += 2
                    continue
                if c == quote or c == "\n":
                    break
                buf.append(c)
                j += 1
            text = "".join(buf)
            new_text = text
            for src, dst in STRING_SOFTEN.items():
                if src in new_text:
                    new_text = new_text.replace(src, dst)
                    repl.append(f'{src}->{dst}')
            out.append(quote + new_text + (quote if j < n and code[j] == quote else ""))
            i = j + 1 if j < n and code[j] == quote else j
            continue
        out.append(ch)
        i += 1
    return "".join(out), repl


def _scan_identifiers(code: str) -> list[str]:
    """跳过注释与字符串，扫描代码标识符中的泄露残留。"""
    found: set[str] = set()
    i, n = 0, len(code)
    quote = ""
    while i < n:
        ch = code[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            continue
        if ch == "/" and i + 1 < n and code[i + 1] in "/*":
            if code[i + 1] == "/":
                j = code.find("\n", i)
                i = n if j == -1 else j
            else:
                j = code.find("*/", i + 2)
                i = n if j == -1 else j + 2
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (code[j].isalnum() or code[j] == "_"):
                j += 1
            name = code[i:j]
            if ID_LEAK_CORE.search(name):
                found.add(name)
            i = j
            continue
        i += 1
    return sorted(found)


def _skeleton(code: str) -> str:
    """代码骨架（去注释 + 行尾规范化）；用于断言"净化只动注释、不动代码"。"""
    parts: list[str] = []
    in_block = False
    for line in code.splitlines():
        code_part, _comment, in_block = _strip_and_scan(line, in_block)
        parts.append(code_part.rstrip())
    return "\n".join(parts)


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _leaky(text: str) -> bool:
    return bool(EN_LEAK.search(text) or EN_LEAK2.search(text) or FILE_LEAK.search(text)
                or any(w in text for w in CN_LEAK))


def _strip_and_scan(line: str, in_block: bool) -> tuple[str, str, bool]:
    """引号感知地把一行拆成 (code_part, comment_part, new_in_block)。"""
    out_code: list[str] = []
    out_comment: list[str] = []
    i, n = 0, len(line)
    block = in_block
    quote = ""
    while i < n:
        ch = line[i]
        if block:
            j = line.find("*/", i)
            if j == -1:
                out_comment.append(line[i:])
                i = n
            else:
                out_comment.append(line[i:j])
                block = False
                i = j + 2
            continue
        if quote:
            out_code.append(ch)
            if ch == "\\" and i + 1 < n:
                out_code.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out_code.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and line[i + 1] == "/":
            out_comment.append(line[i + 2:])
            i = n
            continue
        if ch == "/" and i + 1 < n and line[i + 1] == "*":
            block = True
            i += 2
            continue
        out_code.append(ch)
        i += 1
    return "".join(out_code), "".join(out_comment), block


def _comment_spans(code: str) -> list[tuple[int, int, str, str]]:
    """字符级提取注释片段 [(start, end, text, kind)]，kind∈{'line','block'}。

    注意：不识别 C++ 原始字符串 R"(...)"（材料包样本已扫描确认不含；见 out 报告）。
    """
    spans: list[tuple[int, int, str, str]] = []
    i, n = 0, len(code)
    quote = ""
    while i < n:
        ch = code[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "/":
            j = code.find("\n", i)
            j = n if j == -1 else j
            spans.append((i, j, code[i:j], "line"))
            i = j
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "*":
            j = code.find("*/", i + 2)
            j = n if j == -1 else j + 2
            spans.append((i, j, code[i:j], "block"))
            i = j
            continue
        i += 1
    return spans


def sanitize(code: str) -> tuple[str, list[str]]:
    """净化注释（**只替换注释内容，保留 // /* */ 定界符与行结构**）。

    返回 (净化后代码, 被净化的位置摘要)。跨行块注释以 "/* [redacted]\\n\\n*/" 形式
    保留换行数 ⇒ 行号稳定，代码骨架严格不变（main 中 assert 验证）。
    """
    spans = _comment_spans(code)
    out = code
    redacted: list[str] = []
    for start, end, text, kind in reversed(spans):
        if not _leaky(text):
            continue
        line_no = code.count("\n", 0, start) + 1
        first = text.splitlines()[0].strip()[:110] if text.splitlines() else text.strip()[:110]
        redacted.append(f"L{line_no}: {first}")
        if kind == "line":
            rep = "// [redacted]"
        else:
            closed = text.endswith("*/")
            inner = text[2:-2] if closed else text[2:]
            newlines = "\n" * inner.count("\n")
            rep = ("/* [redacted]" + newlines + "*/") if closed else ("/* [redacted]" + newlines)
        out = out[:start] + rep + out[end:]
    return out, redacted


def _load_matrix() -> dict[str, dict[str, Any]]:
    doc: dict[str, Any] = json.loads(SYN_MATRIX.read_text(encoding="utf-8"))
    return {str(s["uid"]): s for s in doc["samples"]}


def _corpus_code() -> dict[str, str]:
    """合并 external corpus 三代（d3-xx / d3e-xx / d3f-xx）→ {id: code}。"""
    out: dict[str, str] = {}
    for name in ("external_corpus_665.json", "external_corpus_669d.json", "external_corpus_672h.json"):
        doc: dict[str, Any] = json.loads((CORPUS_DIR / name).read_text(encoding="utf-8"))
        for s in doc.get("samples", []):
            sid = str(s["id"])
            code = s.get("code")
            if code:
                out[sid] = str(code)
    return out


def _build_file_cache() -> dict[str, str]:
    """holdout 源码分散在 4 个目录（Appendix/ub, data/cards_665/fixtures, Examples{,/atoms}）。"""
    doc: dict[str, Any] = json.loads(SYN_MATRIX.read_text(encoding="utf-8"))
    wanted: set[str] = set()
    for s in doc["samples"]:
        if s["source_batch"] == "holdout":
            wanted.update(str(f) for f in s["files"])
    roots = [ROOT / "Appendix" / "ub", ROOT / "data" / "cards_665" / "fixtures",
             ROOT / "Examples", ROOT / "Examples" / "atoms"]
    cache: dict[str, str] = {}
    for r in roots:
        if not r.is_dir():
            continue
        for p in r.iterdir():
            if p.name in wanted and p.is_file():
                cache.setdefault(p.name, str(p))
    return cache


def _extract_exp_code(uid: str, files: list[str]) -> str | None:
    batch, _, _sid = uid.partition(":")
    for f in files:
        p = EXP_DIR / batch / str(f)
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def _rewrite_local_includes(code: str, src_dir: Path | None, anon: str,
                            dep_map: dict[str, str]) -> tuple[str, list[str]]:
    """把本地 #include "x" 复制为匿名依赖文件并改写。返回 (新代码, 依赖文件列表)。"""
    deps: list[str] = []

    def _repl(m: re.Match[str]) -> str:
        name = m.group(1)
        if src_dir is None:
            return m.group(0)
        p = src_dir / name
        if not p.is_file():
            return m.group(0)
        if name in dep_map:
            new_name = dep_map[name]
        else:
            h = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
            new_name = f"{anon}_dep_{h}.h"
            dep_map[name] = new_name
        if new_name not in deps:
            deps.append(new_name)
        return f'#include "{new_name}"'

    return re.sub(r'#include\s+"([^"]+)"', _repl, code), deps


def main() -> None:
    rng = random.Random(SEED)
    matrix = _load_matrix()
    file_cache = _build_file_cache()
    corpus = _corpus_code()

    rows: list[dict[str, Any]] = []
    for uid, s in matrix.items():
        if s["source_batch"] != "holdout":
            continue
        fname = str(s["files"][0])
        path = file_cache.get(fname)
        assert path, f"holdout 源文件未找到：{fname}"
        rows.append({"uid": uid, "source_batch": "holdout", "src_path": path,
                     "src_dir": str(Path(path).parent),
                     "code": Path(path).read_text(encoding="utf-8", errors="replace"),
                     "defect_type": s["defect_type"], "expected_verdict": s["expected_verdict"],
                     "planted": s.get("planted")})
    n_holdout = sum(1 for r in rows if r["source_batch"] == "holdout")

    n_corpus = 0
    for uid, s in matrix.items():
        if s["source_batch"] != "corpus":
            continue
        sid = str(s["sample_id"])
        code = corpus.get(sid)
        assert code, f"corpus 源码未找到：{sid}"
        rows.append({"uid": uid, "source_batch": "corpus", "src_path": f"external_corpus::{sid}",
                     "src_dir": "", "code": code, "defect_type": s["defect_type"],
                     "expected_verdict": s["expected_verdict"], "planted": s.get("planted")})
        n_corpus += 1

    used = {r["uid"] for r in rows}
    pool: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for uid, s in matrix.items():
        if s["source_batch"] in ("holdout", "corpus") or uid in used:
            continue
        if s.get("hung_flag"):
            continue
        fam = TYPE_TO_FAMILY[str(s["defect_type"])]
        pool.setdefault(fam, []).append((uid, s))
    excluded_hung = sum(1 for s in matrix.values()
                        if s["source_batch"] not in ("holdout", "corpus") and s.get("hung_flag"))
    n_exp = 0
    for fam in FAMILY8:
        cands = sorted(pool.get(fam, []), key=lambda kv: kv[0])
        rng.shuffle(cands)
        for uid, s in cands[:N_STRAT_PER_FAMILY]:
            code = _extract_exp_code(uid, [str(f) for f in s["files"]])
            assert code is not None, f"exp 源码未找到：{uid} {s['files']}"
            batch = uid.partition(":")[0]
            rows.append({"uid": uid, "source_batch": "exp_stratified", "src_path": uid,
                         "src_dir": str(EXP_DIR / batch), "code": code,
                         "defect_type": s["defect_type"], "expected_verdict": s["expected_verdict"],
                         "planted": s.get("planted")})
            n_exp += 1

    rng.shuffle(rows)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    for old in SRC_DIR.glob("*"):
        if old.is_file():
            old.unlink()
    mapping_rows: list[dict[str, Any]] = []
    id_flags: list[dict[str, Any]] = []
    string_flags: list[dict[str, Any]] = []
    raw_flags: list[str] = []
    used_dep_names: set[str] = set()
    n_redacted_total = 0
    n_redacted_samples = 0
    n_renamed_total = 0
    for i, r in enumerate(rows, 1):
        anon = f"S{i:03d}"
        code = str(r["code"])
        if not code.endswith("\n"):
            code += "\n"
        src_dir = Path(str(r["src_dir"])) if r["src_dir"] else None
        dep_map: dict[str, str] = {}
        code, deps = _rewrite_local_includes(code, src_dir, anon, dep_map)
        code, renamed = _rename_leaky_identifiers(code)
        code, string_repl = _soften_strings(code)
        clean, redacted = sanitize(code)
        assert _skeleton(code) == _skeleton(clean), f"净化破坏了代码骨架：{anon}"
        if not clean.endswith("\n"):
            clean += "\n"
        if 'R"' in code:
            raw_flags.append(f"{anon}.cpp")
        id_tokens = _scan_identifiers(clean)
        if id_tokens:
            id_flags.append({"file": f"{anon}.cpp", "uid": r["uid"], "tokens": id_tokens[:8]})
        str_hits = _string_hits(clean)
        if str_hits:
            string_flags.append({"file": f"{anon}.cpp", "uid": r["uid"], "hits": str_hits[:5]})
        out_path = SRC_DIR / f"{anon}.cpp"
        out_path.write_text(clean, encoding="utf-8", newline="\n")
        if redacted:
            n_redacted_samples += 1
            n_redacted_total += len(redacted)
        # 依赖：复制 + 净化（防文件名/注释泄露）
        for name, new_name in dep_map.items():
            assert src_dir is not None
            raw = (src_dir / name).read_text(encoding="utf-8", errors="replace")
            dep_clean, dep_red = sanitize(raw)
            if dep_red:
                n_redacted_total += len(dep_red)
            (SRC_DIR / new_name).write_text(dep_clean, encoding="utf-8", newline="\n")
            used_dep_names.add(new_name)
        mapping_rows.append({
            "anon_id": anon, "uid": r["uid"], "source_batch": r["source_batch"],
            "src_path": r["src_path"], "file": f"sources/{anon}.cpp", "deps": deps,
            "n_redacted_lines": len(redacted), "redacted_lines": redacted[:20],
            "renamed_identifiers": renamed, "softened_strings": string_repl,
            "defect_type": r["defect_type"], "expected_verdict": r["expected_verdict"],
            "planted": r["planted"],
        })
        n_renamed_total += len(renamed)

    PKG_DIR.mkdir(parents=True, exist_ok=True)
    with (PKG_DIR / "sample_list.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["anon_id", "file", "deps", "note"])
        for m in mapping_rows:
            w.writerow([m["anon_id"], m["file"], ";".join(m["deps"]), ""])
    with (PKG_DIR / "annotation_template.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["anon_id", "expected_verdict(catch/miss)", "defect_type_family",
                    "defect_type_free_text", "planted(true/false/unsure)", "severity(low/medium/high)",
                    "confidence(1-5)", "notes"])
        for m in mapping_rows:
            w.writerow([m["anon_id"], "", "", "", "", "", "", ""])

    MAPPING.write_text(json.dumps({
        "schema": "queyi-689-annotation-key-mapping/v1",
        "generated_by": "tools/prepare_annotation_package_689.py",
        "generated_at": _now(),
        "seed": SEED,
        "warning": "协调者专用；不得交给第二标注者（含原始标签与来源批次）",
        "n_total": len(mapping_rows),
        "counts": {"holdout": n_holdout, "corpus": n_corpus, "exp_stratified": n_exp,
                   "excluded_hung_in_exp_pool": excluded_hung},
        "sanitization": {"n_samples_with_redacted_lines": n_redacted_samples,
                         "n_redacted_lines_total": n_redacted_total,
                         "n_dep_files": len(used_dep_names)},
        "rows": mapping_rows,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

    # ---------------- 校准练习集（10 条，独立于主集；答案公开用于口径统一） ----------------
    cal_rng = random.Random(SEED + 1)
    used_all = used | {m["uid"] for m in mapping_rows}
    cal_rows: list[tuple[str, dict[str, Any]]] = []
    for fam in FAMILY8:
        cands = sorted((uid, s) for uid, s in pool.get(fam, []) if uid not in used_all)
        cal_rng.shuffle(cands)
        if cands:
            cal_rows.append(cands[0])
    extra_pool = sorted((uid, s) for uid, s in matrix.items()
                        if uid not in used_all and not s.get("hung_flag")
                        and uid not in {u for u, _ in cal_rows})
    cal_rng.shuffle(extra_pool)
    cal_rows.extend(extra_pool[:2])
    CAL_DIR = PKG_DIR / "calibration"
    CAL_SRC = CAL_DIR / "sources"
    CAL_SRC.mkdir(parents=True, exist_ok=True)
    for old in CAL_SRC.glob("*.cpp"):
        old.unlink()
    cal_answers: list[dict[str, Any]] = []
    for k, (uid, s) in enumerate(cal_rows, 1):
        anon = f"C{k:02d}"
        code = _extract_exp_code(uid, [str(f) for f in s["files"]])
        assert code is not None, f"校准样本源码未找到：{uid}"
        batch = uid.partition(":")[0]
        src_dir_c = EXP_DIR / batch
        dep_map_c: dict[str, str] = {}
        code, _deps = _rewrite_local_includes(code, src_dir_c, anon, dep_map_c)
        code, _rn = _rename_leaky_identifiers(code)
        code, _sr = _soften_strings(code)
        clean, _re = sanitize(code)
        (CAL_SRC / f"{anon}.cpp").write_text(clean if clean.endswith("\n") else clean + "\n",
                                             encoding="utf-8", newline="\n")
        cal_answers.append({"anon_id": anon, "uid": uid,
                            "expected_verdict": s["expected_verdict"],
                            "defect_type_family": TYPE_TO_FAMILY[str(s["defect_type"])],
                            "defect_type": s["defect_type"], "planted": s.get("planted")})
    with (CAL_DIR / "answers.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["anon_id", "expected_verdict", "defect_type_family", "defect_type", "planted"])
        for a in cal_answers:
            w.writerow([a["anon_id"], a["expected_verdict"], a["defect_type_family"],
                        a["defect_type"], a["planted"]])
    (CAL_DIR / "README_校准说明.md").write_text(
        "# 校准练习集使用说明（第二标注者）\n\n"
        "- 本目录 10 条样本（C01–C10）为**校准练习**，不属于正式标注集，也不会进入主分析。\n"
        "- 请先独立判定全部 10 条（方法同正式标注：先只读代码，再填写判定表），然后打开 "
        "`answers.csv` 对答案。\n"
        "- 对齐口径后再开始 `../annotation_template.csv` 的正式标注；如某条校准题与答案分歧较大，"
        "请在正式标注前与协调者讨论判定规则。\n"
        "- 说明：校准集刻意混合了 `catch`（可捕获缺陷）与 `miss`（不构成可捕获缺陷）两类，"
        "用于校准\"什么算缺陷、什么算可捕获\"这条底线。\n",
        encoding="utf-8", newline="\n")

    print(f"[689-C2] 校准集 {len(cal_rows)} 条 → {CAL_SRC}（answers.csv 供对答案）")

    # 净化后复扫（对包内所有 .cpp/.h）
    residual: list[dict[str, Any]] = []
    for p in sorted(SRC_DIR.iterdir()):
        if p.suffix not in (".cpp", ".h"):
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        in_block = False
        bad: list[str] = []
        for ln, line in enumerate(txt.splitlines(), 1):
            _c, comment, in_block = _strip_and_scan(line, in_block)
            if comment and _leaky(comment):
                bad.append(f"L{ln}: {line.strip()[:110]}")
        if bad:
            residual.append({"file": p.name, "hits": bad[:10]})
    LEAK_SCAN.write_text(json.dumps({
        "schema": "queyi-689-annotation-leakage-scan/v1",
        "generated_at": _now(),
        "note": "净化后复扫；residual 应为空（非空则需人工处理后再交付标注者）；"
                "identifier_flags 为标识符级疑似泄露，交协调者人工复核",
        "n_residual_files": len(residual),
        "residual": residual,
        "n_identifier_flags": len(id_flags),
        "identifier_flags": id_flags,
        "n_string_flags": len(string_flags),
        "string_flags": string_flags,
        "raw_string_files": raw_flags,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

    print(f"[689-C2] 材料包 {len(mapping_rows)} 条 = holdout {n_holdout} + corpus {n_corpus} + 分层 {n_exp}")
    print(f"[689-C2] exp 池排除 hung {excluded_hung} 条；净化 {n_redacted_samples} 样本 / "
          f"{n_redacted_total} 处；标识符重命名 {n_renamed_total} 个；依赖文件 {len(used_dep_names)} 个")
    print(f"[689-C2] 复扫 residual 文件数 = {len(residual)}；标识符残余 {len(id_flags)} 文件；"
          f"字符串疑似 {len(string_flags)} 文件；含原始字符串 {len(raw_flags)} 文件")


if __name__ == "__main__":
    main()
