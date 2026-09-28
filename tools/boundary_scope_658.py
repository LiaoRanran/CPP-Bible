#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""boundary_scope_658.py — C 段：boundary 概念拆分（provenance vs semantic scope）。

红线约束：atoms/ 是受控目录，**零改动**。657 的 26 张边界三元组已落在
data/657_boundary_backfill.json（data/ 非受控），本工具**只读**它提取 provenance，
绝不写 atoms frontmatter。C4 的"卡 frontmatter 显式拆两组字段"本批不执行（受控零改动）。

provenance（验证来源边界）= 你在什么实验范围内得到结论：
  mutation_set_hash / mutation_count / generator_version / 证据 SHA256 / 证据条数 / 编译器版本
semantic scope（知识语义边界）= 结论在什么条件下成立：
  C++ 标准版本 / 编译器·优化级 / 平台 / 输入域假设 / 前置条件

用法：
    python tools/boundary_scope_658.py --emit      # 提取 provenance → data/boundary_provenance_658.json
    python tools/boundary_scope_658.py --report    # 每卡 provenance 完整度 + semantic scope 缺失
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKFILL = os.path.join(ROOT, "data", "657_boundary_backfill.json")
OUT = os.path.join(ROOT, "data", "boundary_provenance_658.json")
COMPILERS = ["gcc 13.1.0", "clang 22.1.8"]


def gather():
    d = json.load(open(BACKFILL, encoding="utf-8"))
    cards = []
    for r in d.get("rows", []):
        triplet = r.get("triplet") or {}
        if not triplet:
            continue  # draft 无边界，跳过
        card_path = os.path.join(ROOT, r["card"])
        ev_sha = ""
        if os.path.isfile(card_path):
            ev_sha = hashlib.sha256(open(card_path, "rb").read()).hexdigest()[:16]
        cards.append({
            "card": r["card"],
            "status": r.get("status"),
            "provenance": {
                "mutation_set_hash": triplet.get("mutation_set_hash"),
                "mutation_count": triplet.get("mutation_count"),
                "generator_version": triplet.get("generator_version"),
                "evidence_sha256": ev_sha,
                "evidence_count": r.get("variants"),
                "compiler_versions": COMPILERS,
            },
            # semantic scope 当前数据未含 → 交人补（C4 需 Authority 批准才动 atoms）
            "semantic_scope": {},
            "scope_complete": False,
        })
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    cards = gather()
    if a.emit:
        json.dump({"schema": "queyi-boundary-provenance/v1", "cards": cards,
                   "note": "只读提取自 data/657_boundary_backfill.json，未改 atoms；"
                           "semantic_scope 全空，待 C4 显式补充（受控零改动）"},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"已提取 {len(cards)} 张边界卡的 provenance → {os.path.relpath(OUT, ROOT)}")
    if a.report or not a.emit:
        prov_ok = sum(1 for c in cards if all(c["provenance"].values()))
        print(f"边界卡总数：{len(cards)}")
        print(f"provenance 完整：{prov_ok}/{len(cards)}")
        print(f"semantic scope 完整：0/{len(cards)}（全部缺失，待 C4 补标准/编译器/平台）")
        print("provenance 字段：mutation_set_hash / mutation_count / generator_version / 证据SHA256 / 证据条数 / 编译器版本。")


if __name__ == "__main__":
    main()
