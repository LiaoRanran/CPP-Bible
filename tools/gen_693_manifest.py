#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gen_693_manifest.py — 693-B2：生成权威冻结产物的 sha256 清单。

用途
====
``scripts/reproduce_all.sh`` 的 S1 阶段会逐条比对本清单；**缺一条或错一条即 FAIL**，
不静默跳过。这样"复现"才真的能发现数据被改动，而不是走过场。

覆盖范围（**只收权威冻结产物**，不收中间/临时文件）
====================================================
* 冻结检测矩阵（1147×8）
* A5 主端点与盲区矩阵
* 真实世界基准三类矩阵
* 互补性 / 文献矩阵
* 标签归一化统计与标注密钥
* reveal 产物与权威账本

用法
====
    python tools/gen_693_manifest.py                 # 写 data/693_data_manifest.sha256
    python tools/gen_693_manifest.py --check         # 只校验，不重写
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "693_data_manifest.sha256"

# (相对路径, 说明)
TARGETS: tuple[tuple[str, str], ...] = (
    ("data/blindspot_676g_detection_matrix.json", "冻结检测矩阵 1147×8（681 修复后）"),
    ("data/676m_a5_matrix_corrected.json", "676m A5 修正矩阵"),
    ("data/a5_676f_detection_matrix.json", "A5 全量检测矩阵"),
    ("data/676m_sample_manifest_corrected.json", "34 类规范词表 + 样本清单"),
    ("data/681_type_stats_normalized.json", "34 类归一化类型统计（n=1147）"),
    ("data/683_real_world_detection_matrix.json", "真实世界检测矩阵"),
    ("data/683_real_world_project_matrix.json", "真实世界项目矩阵"),
    ("data/683_real_world_type_matrix.json", "真实世界类型矩阵"),
    ("data/684_complementarity_matrix.json", "资产互补性矩阵"),
    ("data/685_literature_matrix.json", "文献对照矩阵"),
    ("data/689_annotation_key_mapping.json", "人类标注密钥（anon_id → 原始标签）"),
    ("data/holdout_reveal_5_672h.json", "holdout reveal 产物"),
    ("data/external_corpus_reveal_672h.json", "外部语料 reveal 产物"),
    ("data/authority/decision_event_v2_ledger.jsonl", "权威判决账本（452 事件）"),
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验已有清单，不重写")
    args = ap.parse_args()

    rows: list[tuple[str, str, int]] = []
    missing: list[str] = []
    for rel, _desc in TARGETS:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
            continue
        rows.append((_sha256(p), rel, p.stat().st_size))

    if args.check:
        if not OUT.exists():
            raise SystemExit(f"[693-B2] 清单不存在：{OUT}")
        bad = 0
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            exp, rel = line.split("  ", 1)
            p = ROOT / rel
            if not p.exists() or _sha256(p) != exp:
                print(f"  MISMATCH {rel}")
                bad += 1
        print(f"[693-B2] 校验完成：{len(rows)} 项，失配 {bad} 项，缺失 {len(missing)} 项")
        if bad or missing:
            raise SystemExit(1)
        return

    header = [
        "# 693-B2 · 权威冻结产物 sha256 清单",
        f"# generated_at: {_dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
        "# generated_by: tools/gen_693_manifest.py",
        "# 格式：<sha256><两个空格><相对路径>（与 sha256sum -c 兼容）",
        f"# 覆盖 {len(rows)} 项；登记缺失 {len(missing)} 项（见下）",
        "#",
        "# 校验：python tools/gen_693_manifest.py --check",
        "#      sha256sum -c data/693_data_manifest.sha256",
    ]
    for m in missing:
        header.append(f"# MISSING: {m}")
    body = [f"{h}  {rel}" for h, rel, _sz in rows]
    OUT.write_text("\n".join(header + body) + "\n", encoding="utf-8", newline="\n")

    meta = {
        "schema": "queyi-693-data-manifest/v1",
        "generated_by": "tools/gen_693_manifest.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "n_files": len(rows),
        "n_missing": len(missing),
        "missing": missing,
        "files": [{"path": rel, "sha256": h, "bytes": sz} for h, rel, sz in rows],
    }
    (ROOT / "data" / "693_data_manifest.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"[693-B2] 清单已生成：{len(rows)} 项；缺失 {len(missing)} 项 {missing}")


if __name__ == "__main__":
    main()
