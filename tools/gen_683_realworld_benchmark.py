#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gen_683_realworld_benchmark.py — 683-A1/A4：真实靶场基准元数据（单一事实源合成）。

输入（三份冻结产物，全部先于本脚本存在）：
  1. data/683_real_world_sample_manifest.json      PoC 头部元数据（每条 RW 文件内嵌）
  2. data/683_real_world_candidates_verified.json  NVD API 在线验证记录（应答原文冻结）
  3. data/683_real_world_detection_matrix.json     110 × 8 真实检测判定

输出：
  data/683_real_world_benchmark.json   每条样本的完整元数据（≥100 条）
  data/683_real_world_source_matrix.md 来源矩阵覆盖表（CVE/GHSA/issue/commit/pwn）

诚实边界：CVE 描述/评分/时间/references 一律取自 NVD 应答原文；无匹配 NVD 记录的
条目（如有）显式标注 nvd.found=false，绝不补写。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "683_real_world_sample_manifest.json"
VERIFIED = ROOT / "data" / "683_real_world_candidates_verified.json"
MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
OUT = ROOT / "data" / "683_real_world_benchmark.json"
OUT_SRC = ROOT / "data" / "683_real_world_source_matrix.md"
RW_DIR = ROOT / "data" / "real_world"

RE_COMMIT = re.compile(r"github\.com/[^/]+/[^/]+/commit/")
RE_ISSUE = re.compile(r"github\.com/[^/]+/[^/]+/issues/")
RE_PR = re.compile(r"github\.com/[^/]+/[^/]+/pull/")
RE_GHSA = re.compile(r"github\.com/advisories/GHSA")
GHSA_SOURCE = "security-advisories@github.com"


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="要求矩阵覆盖全部样本")
    a = ap.parse_args()

    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ver = {it["cve"]: it for it in json.loads(VERIFIED.read_text(encoding="utf-8"))["items"]}
    mat = json.loads(MATRIX.read_text(encoding="utf-8"))
    det = {s["rw_id"]: s for s in mat["samples"]}

    rows = []
    stats = {"n": 0, "nvd_found": 0, "ghsa_source": 0, "refs_commit": 0, "refs_issue": 0,
             "refs_pr": 0, "refs_ghsa": 0, "det_n": 0, "or_catch": 0}
    for m in man["samples"]:
        cve = m["cve_id"].strip()
        v = ver.get(cve, {})
        nvd = v.get("nvd", {})
        refs = nvd.get("references", []) or []
        r_commit = [r["url"] for r in refs if RE_COMMIT.search(r.get("url") or "")]
        r_issue = [r["url"] for r in refs if RE_ISSUE.search(r.get("url") or "")]
        r_pr = [r["url"] for r in refs if RE_PR.search(r.get("url") or "")]
        r_ghsa = [r["url"] for r in refs if RE_GHSA.search(r.get("url") or "")]
        fields = m.get("fields", {})
        year = None
        if nvd.get("published"):
            year = int(str(nvd["published"])[:4])
        elif fields.get("year"):
            try:
                year = int(fields["year"])
            except ValueError:
                year = None
        cvss = nvd.get("cvss") or {}
        d = det.get(m["rw_id"])
        poc_path = RW_DIR / m["file"]
        row = {
            "rw_id": m["rw_id"],
            "cve_id": cve,
            "source_type": fields.get("source_type", "cve"),
            "source_url": fields.get("source_url",
                                     f"https://nvd.nist.gov/vuln/detail/{cve}"),
            "project": m["project"],
            "project_url": fields.get("project_url", ""),
            "defect_type": m["defect_type"],
            "severity": (cvss.get("baseSeverity") or fields.get("severity") or ""),
            "cvss": cvss or None,
            "year": year,
            "poc_file": f"data/real_world/{m['file']}",
            "poc_sha256": _sha256(poc_path) if poc_path.is_file() else None,
            "mechanism": fields.get("mechanism", ""),
            "notes": fields.get("notes", ""),
            "nvd": {
                "found": bool(nvd.get("found")),
                "description_en": nvd.get("description_en", ""),
                "published": nvd.get("published"),
                "source_identifier": nvd.get("source_identifier"),
                "vuln_status": nvd.get("vuln_status"),
            },
            "refs_commit": r_commit[:4],
            "refs_issue": r_issue[:4],
            "refs_pr": r_pr[:4],
            "refs_ghsa": r_ghsa[:4],
            "detection": ({"or_verdict": d["or_verdict"], "caught_by": d.get("caught_by_all", []),
                           "per_asset": {k: vv["verdict"] for k, vv in d["per_asset"].items()}}
                          if d else None),
        }
        rows.append(row)
        stats["n"] += 1
        stats["nvd_found"] += int(bool(nvd.get("found")))
        stats["ghsa_source"] += int(nvd.get("source_identifier") == GHSA_SOURCE)
        stats["refs_commit"] += int(bool(r_commit))
        stats["refs_issue"] += int(bool(r_issue))
        stats["refs_pr"] += int(bool(r_pr))
        stats["refs_ghsa"] += int(bool(r_ghsa))
        if d:
            stats["det_n"] += 1
            stats["or_catch"] += int(d["or_verdict"] == "catch")

    doc = {
        "schema": "queyi-683-realworld-benchmark/v1",
        "generated_at": _now(), "generated_by": "tools/gen_683_realworld_benchmark.py",
        "provenance": {
            "cve_verification": "NVD API v2.0 在线查询（应答原文冻结于 "
                                "data/683_real_world_candidates_verified.json）",
            "detection": "data/683_real_world_detection_matrix.json（110×8，真实检测）",
            "poc": "data/real_world/RW-*.cpp（最小重构；头部注释=元数据单一事实源）",
            "honest_note": "PoC 为 source-derived 重构，非原始项目代码；用于检测器基准，"
                           "不含武器化利用链。",
        },
        "stats": stats,
        "n_samples": len(rows),
        "samples": rows,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"[683-A1] benchmark: {len(rows)} 条 → {OUT.relative_to(ROOT).as_posix()}")
    print(f"[683-A1] NVD 在线确认 {stats['nvd_found']}/{stats['n']}；"
          f"含 commit 链接 {stats['refs_commit']}、issue {stats['refs_issue']}、"
          f"PR {stats['refs_pr']}、GHSA {stats['refs_ghsa']}；"
          f"检测覆盖 {stats['det_n']}，OR-catch {stats['or_catch']}")

    # 来源矩阵表（任务卡要求：CVE ≥40 / GHSA ≥20 / Issues ≥20 / Commits ≥15 / CTF ≥5）
    by_type: dict[str, int] = {}
    for r in rows:
        by_type[r["source_type"]] = by_type.get(r["source_type"], 0) + 1
    lines = ["# 683-A1 · 来源矩阵覆盖（真实靶场）", "",
             "| 来源渠道 | 目标 | 实际 | 判定依据 |", "|---|---:|---:|---|",
             f"| CVE（NVD 在线验证） | ≥40 | {stats['nvd_found']} | "
             f"每条 nvd.found=true 且冻结 NVD 应答原文 |",
             f"| GitHub Security Advisory 主来源 | ≥20 | {stats['ghsa_source']} | "
             f"NVD sourceIdentifier=security-advisories@github.com（客观字段） |",
             f"| GitHub Issues 链接 | ≥20 | {stats['refs_issue']} | "
             f"NVD references 中 github.com/*/issues/* 链接 |",
             f"| Bug-fix Commits 链接 | ≥15 | {stats['refs_commit']} | "
             f"NVD references 中 github.com/*/commit/* 链接 |",
             f"| GHSA advisory 链接 | ≥0 | {stats['refs_ghsa']} | references 中 /advisories/GHSA |",
             f"| Pwn/CTF 场景（source_type=pwn） | ≥5 | {by_type.get('pwn', 0)} | "
             f"竞赛/靶场常考的真实漏洞（Pwn2Own 等） |", ""]
    lines.append("## 按 source_type 分布\n")
    for t, c in sorted(by_type.items()):
        lines.append(f"- `{t}`: {c}")
    lines.append("\n## 诚实登记\n")
    lines.append("- 来源矩阵是**收集渠道统计**，同一条样本可能同时具备多种链接（如同时有 "
                 "commit 与 issue 链接）；各行计数按'有该类链接的样本数'计。")
    lines.append("- GHSA 主来源条数若显著低于 20：这是**如实数据**（NVD 记录中 C++ 生态 CVE "
                 "以项目公告为主），不凑数、不伪造；GHSA advisory 链接与 commit/issue "
                 "链接的覆盖已一并报告。")
    OUT_SRC.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"[683-A1] 来源矩阵 → {OUT_SRC.relative_to(ROOT).as_posix()}")

    if a.strict and stats["det_n"] < len(rows):
        print(f"[683-A1] STRICT FAIL: 检测覆盖 {stats['det_n']} < {len(rows)}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
