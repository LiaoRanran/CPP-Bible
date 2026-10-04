#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_676k_source.py — 676k 任务D：planted=false 样本来源核查。

对 expG 的 74 条 planted=false 样本：
  1) 抽取 source.type / source.id / source.url / source.simplification；
  2) **ID 格式校验**：CVE → `CVE-YYYY-NNNN`；github_issue → `owner/repo#NNNN`；
  3) **存在性与 URL 可达性核查**：
     - CVE：查 NVD API 2.0（`totalResults` 是硬证据，比 HTTP 状态码可靠，
       因为 nvd.nist.gov 的详情页是 SPA，任意 ID 都返回 200）
     - github_issue：查 GitHub REST API
  4) **内容匹配核查**：把官方描述与样本的 `simplification` 做关键词重叠度比较；
  5) 抽样 20 条（种子 6761）单独出结论。

只读：不修改任何样本的 source 字段。网络不可达时如实记 "unreachable"，不编造。

用法：
  python tools/audit_676k_source.py --collect       # 收集 74 条来源清单
  python tools/audit_676k_source.py --probe         # 联网核查（带缓存，可重跑）
  python tools/audit_676k_source.py --json OUT
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPG = os.path.join(ROOT, "data", "holdout_expansion", "expG")
COLLECT = os.path.join(ROOT, "data", "676k_source_inventory.json")
CACHE = os.path.join(ROOT, "data", "676k_source_probe_cache.json")
RESULT = os.path.join(ROOT, "data", "676k_source_results.json")
SEED = 6761
SAMPLE_N = 20

CVE_RE = re.compile(r"^CVE-(\d{4})-(\d{4,7})$")
GH_RE = re.compile(r"^([\w.\-]+)/([\w.\-]+)#(\d+)$")
UA = {"User-Agent": "Mozilla/5.0 (audit-676k source verifier)"}

# 与样本 simplification 做关键词重叠用的停用词
STOP = set("""a an the of in on to for and or is are be with by from that this it its as at
into not no use uses used using via when where which while after before than then so such
can may will would should could do does did has have had""".split())


def collect() -> dict:
    rows = []
    for fn in sorted(os.listdir(EXPG)):
        if not fn.endswith(".json") or fn == "INDEX.json":
            continue
        d = json.load(open(os.path.join(EXPG, fn), encoding="utf-8"))
        if d.get("planted") is not False:
            continue
        s = d.get("source") or {}
        rows.append({
            "sample_id": d.get("sample_id"),
            "file": fn,
            "defect_type": d.get("defect_type"),
            "expected_verdict": d.get("expected_verdict"),
            "src_type": s.get("type"),
            "src_id": s.get("id"),
            "url": s.get("url"),
            "project": s.get("project"),
            "commit": s.get("commit"),
            "simplification": s.get("simplification"),
            "trigger_condition": d.get("trigger_condition"),
        })
    out = {
        "schema": "queyi-audit-676k-source-inventory/v1",
        "generated_by": "tools/audit_676k_source.py",
        "n": len(rows),
        "by_type": dict(collections.Counter(r["src_type"] for r in rows)),
        "rows": rows,
    }
    json.dump(out, open(COLLECT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def fmt_check(rows: list[dict]) -> dict:
    bad = []
    for r in rows:
        sid = r["src_id"] or ""
        if r["src_type"] == "cve":
            m = CVE_RE.match(sid)
            ok = bool(m)
            r["id_format_ok"] = ok
            r["cve_year"] = int(m.group(1)) if m else None
            if not ok:
                bad.append({"sample_id": r["sample_id"], "src_id": sid, "why": "不符合 CVE-YYYY-NNNN"})
        elif r["src_type"] == "github_issue":
            ok = bool(GH_RE.match(sid))
            r["id_format_ok"] = ok
            if not ok:
                bad.append({"sample_id": r["sample_id"], "src_id": sid, "why": "不符合 owner/repo#NNNN"})
        else:
            r["id_format_ok"] = None
            bad.append({"sample_id": r["sample_id"], "src_id": sid, "why": f"未知 src_type={r['src_type']}"})
    return {"n_bad": len(bad), "bad": bad}


def _get(url, params=None, timeout=25):
    import requests
    try:
        r = requests.get(url, params=params, timeout=timeout, headers=UA)
        return r.status_code, r.text
    except Exception as e:  # 网络不可达 / 超时 / DNS 失败
        return None, f"{type(e).__name__}: {e}"


def probe(rows: list[dict], sleep_s: float = 7.0) -> dict:
    """NVD API 2.0 无 API key 时限流为 5 次/30s ⇒ 请求间隔取 7s。

    只对 `api_status == "ok"` 的条目做缓存命中（429/超时不缓存），便于重跑补齐。
    """
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))

    for r in rows:
        key = r["src_id"]
        if key in cache and cache[key].get("api_status") == "ok":
            continue
        rec = {"sample_id": r["sample_id"], "src_id": r["src_id"], "url": r["url"]}
        if r["src_type"] == "cve":
            # 1) 存在性：NVD API 2.0
            st, body = _get("https://services.nvd.nist.gov/rest/json/cves/2.0",
                            {"cveId": r["src_id"]})
            rec["api_http"] = st
            if st == 200:
                try:
                    d = json.loads(body)
                    rec["api_status"] = "ok"
                    rec["total_results"] = d.get("totalResults")
                    vs = d.get("vulnerabilities") or []
                    if vs:
                        cve = vs[0]["cve"]
                        descs = [x["value"] for x in cve.get("descriptions", [])
                                 if x.get("lang") == "en"]
                        rec["official_desc"] = (descs[0] if descs else "")[:1200]
                        rec["published"] = cve.get("published")
                        rec["last_modified"] = cve.get("lastModified")
                        rec["vuln_status"] = cve.get("vulnStatus")
                except Exception as e:
                    rec["api_status"] = "parse_error"
                    rec["api_error"] = str(e)[:200]
            else:
                rec["api_status"] = "unreachable" if st is None else f"http_{st}"
                rec["api_error"] = body[:200]
            time.sleep(sleep_s)
        else:  # github_issue
            m = GH_RE.match(r["src_id"] or "")
            if m:
                owner, repo, num = m.group(1), m.group(2), m.group(3)
                st, body = _get(f"https://api.github.com/repos/{owner}/{repo}/issues/{num}")
                rec["api_http"] = st
                if st == 200:
                    d = json.loads(body)
                    rec["api_status"] = "ok"
                    rec["official_desc"] = ((d.get("title") or "") + " :: " +
                                            (d.get("body") or ""))[:1200]
                    rec["state"] = d.get("state")
                    rec["created_at"] = d.get("created_at")
                else:
                    rec["api_status"] = "unreachable" if st is None else f"http_{st}"
                    rec["api_error"] = body[:200]
            else:
                rec["api_status"] = "bad_id"
            time.sleep(sleep_s)
        cache[key] = rec
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return cache


def keywords(text: str) -> set:
    ws = re.findall(r"[A-Za-z_][A-Za-z_0-9]{2,}", (text or "").lower())
    return {w for w in ws if w not in STOP}


def match_score(official: str, simp: str) -> dict:
    a, b = keywords(official), keywords(simp)
    if not a or not b:
        return {"overlap": None, "jaccard": None, "shared": []}
    shared = sorted(a & b)
    return {"overlap": len(shared), "jaccard": round(len(shared) / len(a | b), 4),
            "shared": shared[:40]}


# --------------------------------------------------------------------------- #
# 概念级匹配：官方英文描述是否支持样本声明的缺陷类别
# --------------------------------------------------------------------------- #
CONCEPT_EN = {
    "heap_overread": ["out-of-bounds read", "out-of-bound read", "over-read", "overread",
                      "read past", "read beyond", "buffer over-read", "buffer overread",
                      "buffer overrun", "overrun", "out of bounds read", "out-of-bound",
                      "out-of-bounds", "process memory"],
    "heap_overflow": ["heap buffer overflow", "heap-based buffer overflow", "buffer overflow",
                      "out-of-bounds write", "out of bounds write", "buffer over-write",
                      "overrun", "buffer overrun", "overwrite", "out-of-bound", "overflow"],
    "heap_underflow": ["underflow", "before the beginning", "preceding the buffer",
                       "out-of-bound"],
    "stack_overread": ["stack buffer over-read", "out-of-bounds read", "buffer over-read",
                       "overrun", "out-of-bound"],
    "stack_overflow_write": ["stack buffer overflow", "stack-based buffer overflow",
                             "buffer overflow", "overrun"],
    "global_overflow": ["global buffer overflow", "buffer overflow", "out-of-bounds",
                        "out-of-bound", "overrun"],
    "out_of_bounds": ["out-of-bounds", "out-of-bound", "buffer overflow", "over-read",
                      "buffer over-read", "overrun"],
    "use_after_free": ["use-after-free", "use after free", "after it has been freed",
                       "dangling pointer", "pointer pointing into already", "freed",
                       "erroneously keep"],
    "double_free": ["double free", "double-free", "freed twice", "twice", "clean up"],
    "memory_leak": ["memory leak", "resource leak", "leak of memory", "memory exhaustion",
                    "leak memory"],
    "resource_leak": ["memory leak", "resource leak", "leak"],
    "null_deref": ["null pointer", "null-pointer", "nullptr", "dereference",
                   "segmentation fault", "segfault", "crash", "null"],
    "null_pointer_deref": ["null pointer", "null-pointer", "nullptr", "dereference",
                           "segmentation fault", "segfault", "crash", "null"],
    "integer_overflow": ["integer overflow", "integer underflow", "signed integer overflow",
                         "arithmetic overflow", "overflow"],
    "pointer_overflow": ["pointer overflow", "integer overflow", "overflow"],
    "division_by_zero": ["divide by zero", "division by zero", "divide-by-zero",
                         "division-by-zero", "divide by-zero"],
    "infinite_loop": ["infinite loop", "infinite recursion", "denial of service",
                      "loop with no exit", "infinite"],
    "timing_side_channel": ["side channel", "side-channel", "timing", "cryptographic",
                            "constant time", "constant-time"],
    "info_leak": ["information disclosure", "information leak", "disclose", "expose",
                  "leak of information", "sensitive information"],
    "resource_exhaustion": ["resource exhaustion", "denial of service", "memory exhaustion",
                            "uncontrolled resource"],
    "logic_error": ["logic", "incorrect", "improper", "does not", "missing check",
                    "insufficient validation", "fails to", "wrongly", "erroneously",
                    "improperly", "trick", "malicious", "bypass", "wrong"],
    "api_misuse": ["improper", "incorrect", "does not properly", "fails to", "missing validation"],
    "state_machine": ["state", "handshake", "improper", "protocol"],
    "type_confusion": ["type confusion", "improper type", "cast"],
    "data_race": ["race condition", "data race", "concurrent"],
    "race_condition": ["race condition", "data race", "concurrent"],
    "alignment": ["alignment", "aligned", "misaligned"],
    "endianness": ["endian", "byte order"],
    "uninitialized_read": ["uninitialized", "uninitialised", "not initialized"],
    "double_free_alt": [],
    "memory_lifetime": ["use-after-free", "double free", "memory leak", "freed"],
}

# 通用兜底：官方描述里出现任一缺陷类词，就算"提到了缺陷类别"
GENERIC_DEFECT_TERMS = [
    "overflow", "over-read", "overread", "use-after-free", "use after free", "double free",
    "null pointer", "null-pointer", "out-of-bounds", "out-of-bound", "out of bounds",
    "denial of service", "memory leak", "leak", "infinite loop", "side channel", "side-channel",
    "uninitialized", "race condition", "type confusion", "integer overflow", "underflow",
    "dereference", "improper", "incorrect", "does not", "fails to", "missing", "insufficient",
    "buffer", "read past", "beyond the end", "excessive", "infinite", "erroneously", "wrongly",
    "improperly", "incorrectly", "vulnerability", "security issue", "allows", "before validating",
    "without validating", "not properly", "wrong",
]


def concept_match(defect_type: str, official: str) -> dict:
    txt = (official or "").lower()
    if not txt:
        return {"verdict": "no_data", "hits": []}
    terms = CONCEPT_EN.get(defect_type) or []
    hits = [t for t in terms if t in txt]
    if hits:
        return {"verdict": "match", "hits": hits}
    gen = [t for t in GENERIC_DEFECT_TERMS if t in txt]
    if gen:
        return {"verdict": "partial", "hits": gen[:8]}
    return {"verdict": "mismatch", "hits": []}


def url_check(rows: list[dict], cache: dict) -> dict:
    """对 source.url 本体做可达性核查（GET，浏览器 UA）。

    注意：nvd.nist.gov 的详情页是 SPA，**任意** CVE ID 都返回 200 ⇒ HTTP 状态码只能证明
    "站点可达"，不能证明 "该 CVE 存在"。存在性以 §NVD API 的 totalResults 为准。
    """
    for r in rows:
        key = r["src_id"]
        rec = cache.setdefault(key, {"sample_id": r["sample_id"], "src_id": r["src_id"]})
        if rec.get("url_status"):
            continue
        st, _ = _get(r["url"], timeout=20)
        rec["url_status"] = st if st is not None else "unreachable"
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(0.5)
    return cache


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.collect:
        out = collect()
        print(f"收集 {out['n']} 条 → {COLLECT}；类型分布 {out['by_type']}")
        return 0
    if args.probe:
        inv = json.load(open(COLLECT, encoding="utf-8"))
        rows = inv["rows"]
        fc = fmt_check(rows)
        cache = probe(rows)
        cache = url_check(rows, cache)
        for r in rows:
            c = cache.get(r["src_id"], {})
            r.update({k: c.get(k) for k in
                      ("api_status", "api_http", "total_results", "official_desc",
                       "published", "vuln_status", "state", "created_at", "api_error",
                       "url_status")})
            r["match"] = match_score(c.get("official_desc", ""), r.get("simplification"))
            r["concept"] = concept_match(r["defect_type"], c.get("official_desc", ""))
        # 抽样 20（种子 6761）
        rng = random.Random(SEED)
        samp = sorted(rng.sample(rows, min(SAMPLE_N, len(rows))), key=lambda x: x["sample_id"])
        out = {
            "schema": "queyi-audit-676k-source/v1",
            "generated_by": "tools/audit_676k_source.py",
            "seed": SEED,
            "n": len(rows),
            "format_check": fc,
            "api_status_counts": dict(collections.Counter(r["api_status"] for r in rows)),
            "url_status_counts": dict(collections.Counter(str(r["url_status"]) for r in rows)),
            "concept_verdict_counts": dict(collections.Counter(r["concept"]["verdict"] for r in rows)),
            "concept_verdict_counts_sampled20": dict(
                collections.Counter(r["concept"]["verdict"] for r in samp)),
            "sampled_20": [r["sample_id"] for r in samp],
            "rows": rows,
        }
        json.dump(out, open(RESULT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"核查完成 n={len(rows)}；api_status={out['api_status_counts']}")
        print(f"格式问题 {fc['n_bad']} 条 → {RESULT}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
