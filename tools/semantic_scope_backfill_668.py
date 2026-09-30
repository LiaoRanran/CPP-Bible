#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""semantic_scope_backfill_668.py — 668 P1-1：逐卡「provenance / semantic scope / evidence / 四态」总账。

为什么要这个工具（而不是再写一份回填逻辑）
==========================================
667 阶段的规划把这一项写成"47 卡补边界三元组，四态从全 unknown 翻成有意义分布"。
**实测后前提不成立**：

* 26 张卡（`verified` / `red-team-verified`）**早就有**合法三元组 ⇒ 四态 = `pass`；
* 21 张卡缺三元组，但**它们全部是 `draft`**（11 张实卡 + 10 张 draft650）——
  而 657 的既定规则是"**判决未定，不预先写边界**"（`TARGET_STATUSES`）。
  所以这 21 个 `unknown` **不是缺陷，是规则的正确输出**。

⇒ 668 不做"把 unknown 强行翻成 pass"（那会违反 657 的规则、也会造出假边界），
而是产出一份**逐卡总账**：每张卡的 provenance（三元组 + 来源基线 + 变体数）、
semantic scope（663 的四个字段）、evidence 列表、四态与**理由**。

零改动保证
==========
本工具**默认只读**（`--check` / `--report`）。`--mutate` 只在"卡在回填范围内**且**
确实没有基线覆盖"时跑变异生成器，当前该集合为 **0 张**（见 `--check` 输出）——
即"没有可补的卡"本身就是本批的结论之一。
产物只写 `data/668_*`，**不写受控目录**。

用法
====
    python tools/semantic_scope_backfill_668.py --check     # 只读：逐卡判定 + 缺口
    python tools/semantic_scope_backfill_668.py --report    # 写 data/668_boundary_backfill.{json,md}
    python tools/semantic_scope_backfill_668.py --json      # 打印自检 JSON
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:  # 控制台编码（Windows 下中文输出）
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

import boundary_backfill_657 as B657  # noqa: E402  三元组派生/基线反查的**唯一实现**
import counts_659 as counts  # noqa: E402  基数唯一权威源
import four_state_verdict_638 as F638  # noqa: E402  四态分类的**唯一实现**

OUT_JSON = os.path.join(ROOT, "data", "668_boundary_backfill.json")
OUT_MD = os.path.join(ROOT, "data", "668_boundary_backfill.md")
MUT_V8 = os.path.join(ROOT, "data", "mutation", "full_baseline_v8.json")

#: 663 回填的语义范围四字段（"semantic scope" 在本文档里就指这四个）
SCOPE_FIELDS = ("cpp_standard", "compiler", "platform", "input_domain")
_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
_REDTEAM = "red-team-verified"


def card_rows() -> list[dict[str, Any]]:
    """逐卡总账（只读）。"""
    rows: list[dict[str, Any]] = []
    for p in B657.cards():
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        raw = open(p, "rb").read()
        text = raw.decode("utf-8", errors="replace")
        m = _STATUS_RE.search(text)
        status = m.group(1) if m else ""
        have = B657.existing_triplet(text)
        tri_ok = B657.triplet_ok(have)
        hit = B657.newest_baseline_for(rel) if status in B657.TARGET_STATUSES else None
        baseline, variants = (hit[0], len(hit[1])) if hit else (
            have.get("generator_version", ""), int(have["mutation_count"]) if have.get("mutation_count", "").isdigit() else 0)
        scope = {}
        for k in SCOPE_FIELDS:
            mm = re.search(rf"^{k}:\s*(.+?)\s*$", text, re.MULTILINE)
            scope[k] = mm.group(1) if mm else None
        ev = re.findall(r"^(?:evidence|refutations):\s*\[?([^\]]*)\]?\s*$", text, re.MULTILINE)
        ev_ids = sorted({x.strip().strip("'\"") for chunk in ev for x in chunk.split(",") if x.strip()})
        fs = F638.classify_card(p)
        rows.append({
            "card": rel,
            "status": status,
            "in_backfill_scope": status in B657.TARGET_STATUSES,
            "triplet_ok": tri_ok,
            "baseline_source": baseline,
            "variants": variants,
            "scope": scope,
            "scope_missing": [k for k in SCOPE_FIELDS if not scope[k]],
            "evidence": ev_ids,
            "four_state": fs["state"],
            "four_state_reason": "; ".join(fs.get("reasons") or []),
        })
    return rows


def gaps(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """缺口清单：**每条都写清为什么是缺口 / 为什么不是**。"""
    no_tri = [r for r in rows if not r["triplet_ok"]]
    return {
        "no_triplet": len(no_tri),
        "no_triplet_and_in_scope": len([r for r in no_tri if r["in_backfill_scope"]]),
        "no_triplet_because_draft": len([r for r in no_tri if not r["in_backfill_scope"]]),
        "scope_missing_any": len([r for r in rows if r["scope_missing"]]),
        "scope_missing_within_scope": len([r for r in rows if r["scope_missing"] and r["in_backfill_scope"]]),
        "verdict": ("没有可补的卡：回填范围内（verified / red-team-verified）且缺三元组的卡 = "
                    f"{len([r for r in no_tri if r['in_backfill_scope']])} 张；"
                    f"其余 {len([r for r in no_tri if not r['in_backfill_scope']])} 张全是 `draft`，"
                    "按 657 既定规则『判决未定，不预先写边界』**不应**回填。"),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["four_state"]] = dist.get(r["four_state"], 0) + 1
    real = [r for r in rows if not r["card"].startswith("atoms/draft650/")]
    dist_real: dict[str, int] = {}
    for r in real:
        dist_real[r["four_state"]] = dist_real.get(r["four_state"], 0) + 1
    return {
        "atoms_real": len(real),
        "atoms_draft650": len(rows) - len(real),
        "four_state_all": dist,
        "four_state_real": dist_real,
        "with_boundary": len([r for r in rows if r["triplet_ok"]]),
        "counts_659_atoms_real": counts.ATOMS_REAL,
        "counts_659_atoms_draft": counts.ATOMS_DRAFT,
    }


def collect() -> dict[str, Any]:
    rows = card_rows()
    return {
        "schema": "queyi-boundary-backfill/668",
        "generated_by": "tools/semantic_scope_backfill_668.py",
        "rule": ("三元组只由**真实** mutation 基线现算（复用 boundary_backfill_657.triplet_for），"
                 "四态只由 four_state_verdict_638.classify_card 判定；本工具**不新增**任何判据。"),
        "summary": summarize(rows),
        "gaps": gaps(rows),
        "rows": rows,
    }


def render_md(d: dict[str, Any]) -> str:
    s, g = d["summary"], d["gaps"]
    lines = [
        "# 668 · 逐卡边界总账（provenance / semantic scope / evidence / 四态）",
        "",
        "> 由 `python tools/semantic_scope_backfill_668.py --report` 生成，**禁止手改**。",
        "> 三元组与四态都不在这里造：分别复用 `boundary_backfill_657` 与 `four_state_verdict_638`。",
        "",
        "## 0. 一句话",
        "",
        f"实测**推翻**了规划里的前提（原文假设『47 卡 0 边界 ⇒ 全 unknown』）："
        f"**{s['with_boundary']} 张已有真边界**（四态 `pass`），"
        f"{g['no_triplet']} 张缺边界 —— 其中"
        f"**{g['no_triplet_because_draft']} 张是 `draft`**（按 657 规则不该预写边界），"
        f"回填范围内真正缺边界的 = **{g['no_triplet_and_in_scope']} 张**。",
        "",
        "## 1. 四态分布（现算）",
        "",
        "| 口径 | 卡数 | 四态分布 |\n|---|---:|---|",
        f"| 实卡（不含 draft650） | {s['atoms_real']} | `{s['four_state_real']}` |",
        f"| 草稿卡（draft650） | {s['atoms_draft650']} | `{s['four_state_all']}`（含实卡） |",
        "",
        f"与 `counts_659` 对账：实卡 {s['atoms_real']} vs {s['counts_659_atoms_real']}（应相等）、"
        f"草稿 {s['atoms_draft650']} vs {s['counts_659_atoms_draft']}（应相等）。",
        "",
        "## 2. 缺口清单",
        "",
        f"- 缺三元组：**{g['no_triplet']}** 张（{g['no_triplet_because_draft']} 张为 `draft`）",
        f"- 在回填范围内却缺三元组：**{g['no_triplet_and_in_scope']}** 张",
        f"- semantic scope 有缺字段：**{g['scope_missing_any']}** 张（其中回填范围内 {g['scope_missing_within_scope']} 张）",
        "",
        f"> {g['verdict']}",
        "",
        "## 3. 逐卡总账",
        "",
        "| 卡 | 状态 | 边界 | 来源基线 | 变体 | scope 缺 | 证据数 | 四态 |",
        "|---|---|:--:|---|---:|---|---:|---|",
    ]
    for r in d["rows"]:
        lines.append(
            f"| `{r['card']}` | {r['status']} | {'✅' if r['triplet_ok'] else '❌'} | "
            f"{r['baseline_source'] or '—'} | {r['variants']} | "
            f"{','.join(r['scope_missing']) or '—'} | {len(r['evidence'])} | {r['four_state']} |")
    lines += [
        "",
        "## 4. 口径说明",
        "",
        "- **provenance** = 边界三元组（`mutation_set_hash` / `mutation_count` / `generator_version`）"
        "＋它的来源基线文件；哈希由该卡的 per-variant 记录现算（确定性）。",
        "- **semantic scope** = `cpp_standard` / `compiler` / `platform` / `input_domain`（663 回填的四个字段）。",
        "- **evidence** = 卡面 `evidence:` / `refutations:` 里引用的证据卡 id。",
        "- **四态** = `four_state_verdict_638.classify_card` 的输出（缺边界一律降级 `unknown`，这是设计而非缺陷）。",
    ]
    return "\n".join(lines) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    d = collect()
    s = d["summary"]
    chk("卡数与 counts_659 对账（实卡）", s["atoms_real"] == s["counts_659_atoms_real"],
        f"({s['atoms_real']})")
    chk("卡数与 counts_659 对账（草稿）", s["atoms_draft650"] == s["counts_659_atoms_draft"],
        f"({s['atoms_draft650']})")
    chk("每条都有四态", all(r["four_state"] in F638.STATES for r in d["rows"]))
    chk("每条都有理由", all(r["four_state_reason"] for r in d["rows"]))
    chk("缺三元组的卡全部不在回填范围（draft）", d["gaps"]["no_triplet_and_in_scope"] == 0,
        f"(in_scope_missing={d['gaps']['no_triplet_and_in_scope']})")
    chk("有边界的卡四态都不是 unknown",
        all(r["four_state"] != "unknown" for r in d["rows"] if r["triplet_ok"]))
    chk("无变体的卡不留假基线名", all(r["baseline_source"] == "" or r["variants"] > 0
                                      for r in d["rows"] if not r["triplet_ok"]))
    print(f"semantic_scope_backfill_668 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="668 P1-1 · 逐卡边界总账（只读）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.json:
        print(json.dumps(collect(), ensure_ascii=False, indent=2))
        return 0

    if a.report:
        d = collect()
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_md(d))
        print(f"[bb668] 已写 {os.path.relpath(OUT_JSON, ROOT)} / {os.path.relpath(OUT_MD, ROOT)}")
        print(f"[bb668] 四态（实卡）：{d['summary']['four_state_real']}；"
              f"有边界 {d['summary']['with_boundary']}/{len(d['rows'])}")
        print(f"[bb668] {d['gaps']['verdict']}")
        return 0

    # 默认 / --check：只读自检
    return selftest()


if __name__ == "__main__":
    raise SystemExit(main())
