#!/usr/bin/env python3
"""676h · 数据完整性检查（A5 全量样本清单）。

检查项（任一失败即非零退出）：
  1. manifest.n_total == len(samples)（缺一不可）；
  2. 去重不变式：保留样本的 content_md5 无重复；
  3. 切分不变式：derivation + evaluation == n_total，且与 676f 结果文件登记的一致；
  4. planted 计数与 676f 结果登记一致；
  5. 能力边界矩阵样本数 == n_total（1147 是含历史批次的并集，单独记录不相等原因）；
  6. 可选：对仍能定位到源文件的样本，重算 md5 比对。

只读；不修改任何 data/ 产物（只写自己的报告）。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = "data/a5_676f_sample_manifest.json"
RESULTS = "data/a5_676f_results.json"
BLINDSPOT = "data/blindspot_676g_stats.json"
OUT_JSON = "data/676h_data_integrity.json"


def load(rel):
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_files(base, names):
    """与 data/676f_pipeline.py::_md5_files 同口径：先写文件名，再写字节，按文件名排序。"""
    h = hashlib.md5()
    for name in sorted(names):
        h.update(name.encode("utf-8"))
        with open(os.path.join(base, name), "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                h.update(chunk)
    return h.hexdigest()


def main() -> int:
    man = load(MANIFEST)
    res = load(RESULTS) or {}
    bl = load(BLINDSPOT) or {}
    checks = []

    def check(cid, name, ok, detail):
        checks.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})

    if not man:
        check("D0", "676f 样本清单存在", False, f"缺失 {MANIFEST}")
        report = {"schema": "queyi-data-integrity/676h", "checks": checks, "verdict": "fail"}
        with open(os.path.join(ROOT, OUT_JSON.replace("/", os.sep)), "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=1)
        print("[integrity] FAIL 清单缺失")
        return 1

    samples = man.get("samples", [])
    n_total = man.get("n_total")
    check("D1", "清单条目数 == n_total",
          n_total == len(samples), f"n_total={n_total} len(samples)={len(samples)}")

    md5s = [s.get("content_md5") for s in samples]
    dup = len(md5s) - len(set(md5s))
    check("D2", "保留样本 content_md5 无重复（去重不变式）", dup == 0,
          f"唯一 {len(set(md5s))} / 条目 {len(md5s)}；重复 {dup}")

    n_der = sum(1 for s in samples if s.get("split") == "derivation")
    n_eval = sum(1 for s in samples if s.get("split") == "evaluation")
    ss = (res.get("sample_stats") or {})
    expect_der, expect_eval = ss.get("n_derivation"), ss.get("n_evaluation")
    check("D3", "切分计数与 676f 结果登记一致",
          n_der == expect_der and n_eval == expect_eval and n_der + n_eval == len(samples),
          f"manifest {n_der}/{n_eval}；results 登记 {expect_der}/{expect_eval}")

    n_true = sum(1 for s in samples if s.get("planted") is True)
    n_false = sum(1 for s in samples if s.get("planted") is False)
    check("D4", "planted 计数与 676f 结果登记一致",
          n_true == ss.get("n_planted_true") and n_false == ss.get("n_planted_false"),
          f"manifest true={n_true} false={n_false}；results 登记 "
          f"true={ss.get('n_planted_true')} false={ss.get('n_planted_false')}")

    # 盲区矩阵样本数（并集口径：含历史批次，与 A5 的 1137 不等是正常的）
    bl_n = (bl.get("total") or {}).get("n")
    bl_n_ok = isinstance(bl_n, int) and bl_n >= len(samples)
    check("D5", "盲区地图样本数已登记且 ≥ A5 清单", bl_n_ok,
          f"blindspot n={bl_n}；A5 n={len(samples)}（并集含历史批次，差异属预期）")

    # md5 重算：按 676f_pipeline 的 _md5_files 口径（文件名 + 字节，按文件名排序）
    verified = skipped = mismatched = 0
    mismatch_list: list[str] = []
    for s in samples:
        files = s.get("files") or []
        if not files or not s.get("content_md5"):
            skipped += 1
            continue
        base = s.get("dir") or ""
        base_abs = base if os.path.isabs(base) else os.path.join(ROOT, str(base).replace("/", os.sep))
        if not os.path.isdir(base_abs) or any(
                not os.path.exists(os.path.join(base_abs, f)) for f in files):
            skipped += 1
            continue
        if md5_files(base_abs, files) == s.get("content_md5"):
            verified += 1
        else:
            mismatched += 1
            if len(mismatch_list) < 5:
                mismatch_list.append(s.get("sample_id"))
    check("D6", "可定位源文件的 md5 重算无失配", mismatched == 0,
          f"重算一致 {verified}；跳过（内联 / 文件不在库内）{skipped}；失配 {mismatched} {mismatch_list}")

    # ingest 指纹：只读快照，便于他人比对
    digest = hashlib.sha256(
        "".join(f"{s.get('sample_id')}:{s.get('content_md5')}\n" for s in samples).encode()
    ).hexdigest()[:16]

    verdict = "pass" if all(c["ok"] for c in checks) else "fail"
    report_full: dict[str, Any] = {
        "schema": "queyi-data-integrity/676h",
        "generated_by": "tools/data_integrity_676h.py",
        "manifest": MANIFEST,
        "n_samples": len(samples),
        "split": {"derivation": n_der, "evaluation": n_eval},
        "planted": {"true": n_true, "false": n_false},
        "fingerprint_sha256_16": digest,
        "md5_recheck": {"verified": verified, "skipped": skipped, "mismatched": mismatched},
        "blindspot_n": bl_n,
        "checks": checks,
        "verdict": verdict,
    }
    with open(os.path.join(ROOT, OUT_JSON.replace("/", os.sep)), "w", encoding="utf-8") as fh:
        json.dump(report_full, fh, ensure_ascii=False, indent=1)

    for c in checks:
        print(f"[integrity] {'OK  ' if c['ok'] else 'FAIL'} {c['id']} {c['name']} — {c['detail']}")
    print(f"[integrity] 指纹 sha256[:16] = {digest}；判定 {verdict}")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
