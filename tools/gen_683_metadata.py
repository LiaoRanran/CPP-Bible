#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gen_683_metadata.py — 683-A4.3：Croissant 元数据扩展（加入真实靶场 recordSet）。

设计原则（守 682 的五条实修经验）：
  * 字段级 `source` 必须带 fileObject；内联 data 的键为字段全 id；
  * `contentSize` 为字符串；`prov:*` 用纯文本；
  * 扩展**只增不改**既有 recordSet / distribution（原 4 个 recordSet 与 13 个
    FileObject 一字不动；新增内容以 `683` 前缀可识别）。

用法：
    python tools/gen_683_metadata.py --stage extend   # 扩展 data/croissant.json + 自检
    python tools/gen_683_metadata.py --stage check    # 只自检（sha256 复算等）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROISSANT = ROOT / "data" / "croissant.json"
BENCH = ROOT / "data" / "683_real_world_benchmark.json"
MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
RW_DIR = ROOT / "data" / "real_world"
ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
          "cross-compile", "linker", "compile-time"]


def _now() -> str:
    return _dt.datetime.now().astimezone().date().isoformat()


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _field(fid: str, name: str, dtype: str, desc: str, source: dict | None = None,
           refs: str | None = None) -> dict:
    f: dict = {"@type": "cr:Field", "@id": fid, "name": name,
               "description": desc, "dataType": dtype}
    if source:
        f["source"] = source
    if refs:
        f["references"] = {"@id": refs}
    return f


def stage_extend() -> int:
    doc = json.loads(CROISSANT.read_text(encoding="utf-8"))
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = bench["samples"]
    det = {s["rw_id"]: s for s in matrix["samples"]}

    # 幂等：先移除本脚本上次写入的 683 内容（recordSet / distribution 双清洗）
    doc["recordSet"] = [r for r in doc.get("recordSet", [])
                        if "rwsamples683" not in r.get("@id", "")
                        and "rwmatrix683" not in r.get("@id", "")]
    doc["distribution"] = [
        d for d in doc.get("distribution", [])
        if str(d.get("queyi:group", "")) != "realworld683"
        and "realworld683" not in str(d.get("@id", ""))
        and "real_world/RW-" not in str(d.get("@id", ""))]

    # ① FileSet + FileObject（110 个 PoC；规范对齐 682 既有写法：
    #    FileObject @id/contentUrl = 仓库相对路径；FileSet 用 includes glob）
    for r in rows:
        rel = r["poc_file"]
        p = ROOT / rel
        doc["distribution"].append({
            "@type": "cr:FileObject", "@id": rel, "name": Path(rel).name,
            "contentUrl": rel, "encodingFormat": "text/x-c++src",
            "sha256": _sha256(p) if p.is_file() else None,
            "contentSize": str(p.stat().st_size) if p.is_file() else None,
            "queyi:group": "realworld683",
        })
    doc["distribution"].append({
        "@type": "cr:FileSet", "@id": "data/real_world", "name": "real-world PoCs (683)",
        "description": "110 条真实缺陷最小重构（RW-*.cpp，单文件、可编译）",
        "includes": ["data/real_world/RW-*.cpp"],
        "encodingFormat": "text/x-c++src",
        "queyi:group": "realworld683",
    })

    # ② RecordSet：真实靶场样本（110）
    fields = [
        _field("rwsamples683/rw_id", "rw_id", "sc:Text", "样本编号 RW-001…"),
        _field("rwsamples683/cve_id", "cve_id", "sc:Text", "CVE 编号（来源主键）"),
        _field("rwsamples683/source_url", "source_url", "sc:Text", "出处 URL（NVD/项目公告）"),
        _field("rwsamples683/project", "project", "sc:Text", "上游项目"),
        _field("rwsamples683/defect_type", "defect_type", "sc:Text", "34 类规范词表"),
        _field("rwsamples683/year", "year", "sc:Integer", "NVD 首次发布年"),
        _field("rwsamples683/severity", "severity", "sc:Text", "CVSS 分级（NVD 原文）"),
        _field("rwsamples683/poc_file", "poc_file", "sc:Text", "PoC 相对路径"),
        _field("rwsamples683/poc_sha256", "poc_sha256", "sc:Text", "PoC 内容 SHA-256"),
    ]
    data = []
    for r in rows:
        data.append({
            "rwsamples683/rw_id": r["rw_id"], "rwsamples683/cve_id": r["cve_id"],
            "rwsamples683/source_url": r["source_url"], "rwsamples683/project": r["project"],
            "rwsamples683/defect_type": r["defect_type"], "rwsamples683/year": r.get("year"),
            "rwsamples683/severity": r.get("severity") or "",
            "rwsamples683/poc_file": r["poc_file"],
            "rwsamples683/poc_sha256": r.get("poc_sha256") or "",
        })
    doc["recordSet"].append({
        "@type": "cr:RecordSet", "@id": "rwsamples683", "name": "真实靶场样本索引（683）",
        "description": "110 条真实缺陷最小重构（source-derived）；CVE 元数据经 NVD API 在线验证",
        "field": fields, "data": data,
    })

    # ③ RecordSet：真实靶场判定矩阵（110 × 8）
    mfields = [
        _field("rwmatrix683/uid", "uid", "sc:Text", "唯一键 realworld:<rw_id>"),
    ]
    for a in ASSETS:
        mfields.append(_field(f"rwmatrix683/verdict_{a}", f"verdict_{a}", "sc:Text",
                              f"{a} 判定 catch/miss/unknown"))
    mfields.append(_field("rwmatrix683/or_verdict", "or_verdict", "sc:Text",
                          "8 资产 OR：任一 catch⇒catch；全 unknown⇒unknown；否则 miss"))
    mdata = []
    for r in matrix["samples"]:
        row = {"rwmatrix683/uid": r["uid"]}
        for a in ASSETS:
            row[f"rwmatrix683/verdict_{a}"] = r["per_asset"][a]["verdict"]
        row["rwmatrix683/or_verdict"] = r["or_verdict"]
        mdata.append(row)
    doc["recordSet"].append({
        "@type": "cr:RecordSet", "@id": "rwmatrix683", "name": "真实靶场检测矩阵（110×8，683）",
        "description": "真实检测（WSL g++ 13.3 双档 + MinGW 本地资产）；"
                       "wunsequenced/compile-time 恒 unknown（工具链事实）",
        "field": mfields, "data": mdata,
    })

    # ④ stats 增量（只增不改）
    st = doc.setdefault("queyi:stats", {})
    st["realworld683"] = {
        "n_samples": len(rows), "n_projects": len({r["project"] for r in rows}),
        "n_types": len({r["defect_type"] for r in rows}),
        "nvd_verified": bench["stats"]["nvd_found"],
        "or_catch_rate_pct": matrix.get("or_catch_rate_pct"),
        "generated_at": _now(),
    }
    doc["dateModified"] = _now()
    doc["description"] = str(doc.get("description", "")) + \
        " [683] Extended with a real-world benchmark recordSet: 110 reconstructed C++ defects " \
        "with NVD-verified provenance and an 110x8 detection matrix."
    CROISSANT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8", newline="\n")
    print(f"[683-A4.3] croissant.json 已扩展：+2 recordSet、+{len(rows)} FileObject、+1 FileSet")
    return stage_check()


def stage_check() -> int:
    doc = json.loads(CROISSANT.read_text(encoding="utf-8"))
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 原 4 recordSet 仍在
    ids = [r.get("@id") for r in doc["recordSet"]]
    chk("既有 4 个 recordSet 保留", len([i for i in ids if i and "683" not in i]) >= 4,
        f"({ids})")
    chk("683 recordSet 就位", "rwsamples683" in ids and "rwmatrix683" in ids)
    # 110 FileObject sha256 复算
    bad = 0
    n = 0
    for d in doc["distribution"]:
        if d.get("@type") == "cr:FileObject" and str(d.get("queyi:group")) == "realworld683":
            p = ROOT / str(d["contentUrl"])
            n += 1
            if not p.is_file() or _sha256(p) != d.get("sha256"):
                bad += 1
    chk("110 个 PoC 的 sha256 与磁盘一致", bad == 0 and n == 110, f"(n={n}, bad={bad})")
    # 判定矩阵行数
    rs = next(r for r in doc["recordSet"] if r.get("@id") == "rwmatrix683")
    chk("判定矩阵 110 行 × 8 资产字段", len(rs["data"]) == 110 and
        len([f for f in rs["field"] if f["name"].startswith("verdict_")]) == 8)
    chk("sample 记录数与矩阵一致",
        len(next(r for r in doc["recordSet"] if r.get("@id") == "rwsamples683")["data"]) == 110)
    print(f"gen_683_metadata check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("extend", "check"), default="check")
    a = ap.parse_args()
    return stage_extend() if a.stage == "extend" else stage_check()


if __name__ == "__main__":
    sys.exit(main())
