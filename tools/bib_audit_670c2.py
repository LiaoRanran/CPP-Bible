#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""bib_audit_670c2.py — BibTeX 完整性审计（670c2 B2）。

对 `research/latex/queyi_refs.bib` 逐条检查：
  1. 必填字段非空（title / author / year / venue 之一）
  2. 所有 `\\cite{}` 的 key 在 bib 中存在（0 未定义）
  3. 所有 bib 条目至少被 `\\cite` 一次（未引用只标记，不删）
  4. DOI / arXiv ID 格式校验
  5. 与 `research/670b_引用核验_终稿.md` 对账（该报告里出现的 DOI/arXiv ID 应能在 bib 命中）

只读 bib/tex/md，写 `data/bib_audit_670c2.json`。
退出码：0 = 无 error（unused 只算 warning）；1 = 有 error。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(ROOT, "research", "latex", "queyi_refs.bib")
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027_v1.1.tex")
REPORT = os.path.join(ROOT, "research", "670b_引用核验_终稿.md")
OUT = os.path.join(ROOT, "data", "bib_audit_670c2.json")

VENUE_FIELDS = ("journal", "booktitle", "publisher", "howpublished", "note")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})")


def parse_bib(text: str) -> list[dict]:
    """极简 BibTeX 解析：@type{key, field = {..} / ".." / bare, ...}"""
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", text):
        etype, key = m.group(1).lower(), m.group(2).strip()
        # 截取该条目正文（到下一个 @ 或文件末）
        start = m.end()
        nxt = text.find("\n@", start)
        body = text[start: nxt if nxt != -1 else len(text)]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)", body):
            fname = fm.group(1).lower()
            raw = fm.group(2).strip()
            if raw.startswith("{") and raw.endswith("}"):
                raw = raw[1:-1]
            elif raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            fields[fname] = re.sub(r"\s+", " ", raw).strip()
        entries.append({"type": etype, "key": key, "fields": fields})
    return entries


def audit() -> dict:
    bib_text = open(BIB, encoding="utf-8").read()
    tex_text = open(TEX, encoding="utf-8").read()
    rep_text = open(REPORT, encoding="utf-8").read() if os.path.isfile(REPORT) else ""

    entries = parse_bib(bib_text)
    bib_keys = {e["key"] for e in entries}

    cite_keys: set[str] = set()
    for m in re.findall(r"\\cite\{([^}]+)\}", tex_text):
        cite_keys.update(k.strip() for k in m.split(","))

    errors, warnings = [], []

    # 1. 必填字段（@misc 允许无 author/year：法规、协议、软件等非论文条目）
    for e in entries:
        f = e["fields"]
        if not f.get("title"):
            errors.append(f"{e['key']}: 缺字段 title")
        if e["type"] != "misc":
            for req in ("author", "year"):
                if not f.get(req):
                    errors.append(f"{e['key']}: 缺字段 {req}")
        if not any(f.get(v) for v in VENUE_FIELDS):
            errors.append(f"{e['key']}: 缺 venue（journal/booktitle/publisher/howpublished/note 全空）")

    # 2. cite -> bib
    for k in sorted(cite_keys - bib_keys):
        errors.append(f"\\cite{{{k}}} 在 bib 中不存在（未定义引用）")

    # 3. bib -> cite
    unused = sorted(bib_keys - cite_keys)
    for k in unused:
        warnings.append(f"{k}: bib 条目从未被 \\cite")

    # 4. DOI / arXiv 格式
    for e in entries:
        f = e["fields"]
        doi = f.get("doi", "")
        if doi and not DOI_RE.match(doi):
            errors.append(f"{e['key']}: DOI 格式可疑 -> {doi}")
        note = f.get("note", "")
        if "arxiv" in note.lower() and not ARXIV_RE.search(note):
            warnings.append(f"{e['key']}: note 含 arXiv 但 ID 格式未识别 -> {note}")

    # 5. 与 670b 核验报告对账（报告里出现的 DOI / arXiv ID 应能在 bib 命中）
    rep_dois = {d.rstrip("`).,;") for d in re.findall(r"10\.\d{4,9}/[^\s`（），,;]+", rep_text)}
    bib_dois = {e["fields"].get("doi", "") for e in entries}
    bib_text_l = bib_text.lower()
    rep_miss = []
    for d in rep_dois:
        d_norm = d.rstrip(".")
        if d_norm not in bib_dois and d_norm.lower() not in bib_text_l:
            rep_miss.append(d_norm)
    for d in rep_miss:
        warnings.append(f"670b 报告中的 DOI 未在 bib 命中: {d}")

    return {
        "bib_entries": len(entries),
        "cite_keys": len(cite_keys),
        "errors": errors,
        "warnings": warnings,
        "unused_keys": unused,
        "report_dois_checked": len(rep_dois),
        "report_dois_missing": rep_miss,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="BibTeX 完整性审计（670c2 B2）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true", help=f"写 {os.path.relpath(OUT, ROOT)}")
    args = ap.parse_args()

    res = audit()
    if args.write:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[bib-audit] entries={res['bib_entries']}  cite_keys={res['cite_keys']}  "
              f"errors={len(res['errors'])}  warnings={len(res['warnings'])}")
        for e in res["errors"]:
            print("  [ERR]", e)
        for w in res["warnings"]:
            print("  [warn]", w)
        print("[bib-audit] " + ("PASS" if not res["errors"] else "FAIL"))
    return 0 if not res["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
