#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""card_split_668.py — 668 P1-2：把 664/665 的**真机实测**机器卡拆成正式原子卡（实卡 37 → 42）。

上游：`data/cards_665/index_665.json`（665 B1 的 16 张机器卡，全部带**真机夹具 + 实测输出**）。
本批取其中 5 张「有可复现真 UB」的，写成 `atoms/` 下的原子卡：

| 来源 | 新卡 | 域 | 误解（卡面 assertion_under_test 的反面） |
|---|---|---|---|
| ig-01 | ATOM-UB-WRAP-001 | ub | 「有符号溢出会回绕」——标准里是 UB，回绕是实现的偶然 |
| ig-02 | ATOM-UB-OOB-001 | ub | 「越界一定会崩」——不崩也已经是 UB |
| ig-07 | ATOM-UB-NULLDEREF-001 | ub | 「解引用空指针一定段错误」——不保证 |
| ig-08 | ATOM-UB-DIVZERO-001 | ub | 「除零会抛 C++ 异常」——是 UB/信号，catch(...) 抓不到 |
| ig-14 | ATOM-MEM-NEWARR-001 | mem | 「new[] 的数组能用 delete 释放」——必须 delete[] |

纪律（本工具不可越过的线）
==========================
1. **不代签**：新卡 `status: machine-verified`、`human_review: required`、**不写 `verified_by`**。
   机器只能证明"它跑了并读到了这个输出"，不能证明"这个断言是对的"。
2. **证据来自产物**：检测器 / 夹具路径 / 夹具 sha256 / 实测输出 / 签名 / 测量时间，
   全部从 `index_665.json` **读**，不手打、不编造。
3. **不写边界三元组**：三元组必须由真实 mutation 基线现算（`boundary_backfill_657.triplet_for`）；
   新卡在跑过变异之前**留空**，四态因此是 `unknown` —— 这是正确输出，不是缺陷。
4. 只写 `atoms/ub/` 与 `atoms/mem/` 下的 5 个新文件；已存在则跳过（幂等）。

用法
====
    python tools/card_split_668.py --check     # 只读：计划 + 冲突检查
    python tools/card_split_668.py --apply     # 写 5 张新卡
    python tools/card_split_668.py --report    # 写 data/668_card_split.{json,md}
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

INDEX = os.path.join(ROOT, "data", "cards_665", "index_665.json")
OUT_JSON = os.path.join(ROOT, "data", "668_card_split.json")
OUT_MD = os.path.join(ROOT, "data", "668_card_split.md")

#: 来源 id → (新卡 id, 域目录, 标题, 正确表述)
PLAN: dict[str, tuple[str, str, str, str]] = {
    "ig-01": (
        "ATOM-UB-WRAP-001", "ub",
        "有符号整数溢出不是「回绕」：回绕是实现偶然，标准里是 UB",
        "有符号整数运算超出可表示范围是**未定义行为**；「回绕」只是 x86-64 上 gcc/clang 的**实现选择**，"
        "优化器有权假设它不发生并据此改写程序。",
    ),
    "ig-02": (
        "ATOM-UB-OOB-001", "ub",
        "数组越界不是「会崩溃」：不崩也已经是 UB",
        "越界访问的**判定依据是访问是否落在对象边界内**，与是否崩溃无关；"
        "「没崩所以没事」是把可观测现象当成了语义保证。",
    ),
    "ig-07": (
        "ATOM-UB-NULLDEREF-001", "ub",
        "解引用空指针不保证段错误：它是 UB，不是「一定崩」",
        "解引用空指针是**未定义行为**；「一定 SIGSEGV」是平台巧合，"
        "优化器可以在假设它不发生的前提下删除整段代码。",
    ),
    "ig-08": (
        "ATOM-UB-DIVZERO-001", "ub",
        "整数除零不是 C++ 异常：它是 UB / 信号，catch(...) 抓不到",
        "整数除零在 C++ 中不是异常，而是 UB（x86-64 上表现为 `SIGFPE`）；"
        "`try { … } catch (...) { … }` 抓不到它 —— 异常只覆盖 `std::exception` 体系。",
    ),
    "ig-14": (
        "ATOM-MEM-NEWARR-001", "mem",
        "new[] 的数组不能用 delete 释放：分配与释放形式必须配对",
        "`new[]` 必须配 `delete[]`；用标量 `delete` 释放数组是 UB（x86-64 上 ASan 报 "
        "`alloc-dealloc-mismatch`），因为数组分配可能带 cookie，标量 delete 不会跳过它。",
    ),
}


def load_index() -> dict[str, dict[str, Any]]:
    d = json.load(open(INDEX, encoding="utf-8"))
    return {c["source_id"]: c for c in d.get("cards", [])}


def _fm_str(v: Any) -> str:
    s = str(v)
    return '"' + s.replace('"', '\\"').replace("\n", " ") + '"' if (":" in s or s.strip() != s) else s


def card_text(src: dict[str, Any], cid: str, domain: str, title: str, right: str) -> str:
    """由机器卡的真实字段渲染原子卡（frontmatter + 正文）。"""
    today = datetime.date.today().isoformat()
    b = src.get("boundary") or {}
    measured = str(src.get("measured_out") or "").strip().replace("\r", "")
    measured_short = "\n".join(measured.splitlines()[:6])
    return f"""---
schema_version: 1
id: {cid}
title: {title}
domain: {domain}
type: mechanism
status: machine-verified
cpp_standard: [{b.get('standard', 'C++17')}]
compiler: [{b.get('compiler', 'unknown')}]
platform: [{b.get('platform', 'unknown')}]
input_domain: {b.get('input_domain', 'unknown')}
dal: B
human_review: required
audience: intermediate
cognitive_load: low
claim: >-
  {right}
claim_structured:
  - id: prop-1
    subject: {cid}
    predicate: 实测判定
    object: {src.get('detector')} 在夹具上的真实输出
    claim_type: observation
    statement: {src.get('detector')} 对该夹具判定为 {src.get('verdict')}（信号：{src.get('signature')}）。
    evidence_668: [IG-668-{src.get('id')}]
    extracted_by: machine:card_split_668
  - id: prop-2
    subject: {cid}
    predicate: 边界
    object: 该判定成立的编译/平台条件
    claim_type: inference
    statement: 本判定在 {b.get('compiler', 'unknown')} / {b.get('platform', 'unknown')} 上、以 {src.get('detector')} 观测得到；
              换编译器或换平台不保证同样的可观测结果。
    external_basis: "ISO/IEC 14882（未定义行为条款）"
    extracted_by: machine:card_split_668
claim_boundary:
  standard: [{b.get('standard', 'C++17')}]
  compilers: [{b.get('compiler', 'unknown')}]
  opt: [-O0, -O2]
  platform: [{b.get('platform', 'unknown')}]
evidence_668:
  - id: IG-668-{src.get('id')}
    detector: {src.get('detector')}
    fixture_rel: {src.get('fixture_rel')}
    fixture_sha256: {src.get('fixture_sha256')}
    runs: {src.get('runs')}
    measured_at: {src.get('measured_at')}
    signature: {_fm_str(src.get('signature'))}
    verdict: {src.get('verdict')}
    expectation: {src.get('expect')}
    reproduce: "python tools/ig_cards_665.py --check"
relations: []
sources:
  - {{kind: iso, ref: "ISO/IEC 14882（未定义行为 / 分配释放配对相关条款）", independent: true}}
first_hand: true
status_history:
  - {{level: machine-verified, at: "{today}", by: machine:card_split_668}}
---

# {cid} · {title}

一句话直觉：**「实测到 X」和「标准规定 X」是两件事** —— 这张卡只声明前者，后者请人签。

## 1. 误解（来自 664/665 独立生成的断言）

`{src.get('assertion_under_test')}`

## 2. 真机实测（不是推理）

| 项 | 值 |
|---|---|
| 检测器 | `{src.get('detector')}` |
| 夹具 | `{src.get('fixture_rel')}`（sha256 `{str(src.get('fixture_sha256'))[:16]}…`） |
| 测量时间 | {src.get('measured_at')} |
| 运行次数 | {src.get('runs')} |
| 判定 | **{src.get('verdict')}**（期望 `{src.get('expect')}`；签名 `{src.get('signature')}`） |

实测输出（前几行，完整见夹具复跑）：

```
{measured_short}
```

复算：`python tools/ig_cards_665.py --check`（在 `-O0` 与 `-O2` 两档下都跑，任一档报出即 `catch`）。

## 3. 正确表述

{right}

## 4. 边界（这张卡**不**声明什么）

- 不声明"换了编译器/平台/标准版本仍然如此"：上表只覆盖 `{b.get('compiler', 'unknown')}` / `{b.get('platform', 'unknown')}` / `{b.get('standard', 'C++17')}`。
- 不声明**语义级**结论：检测器报出的是"在这个夹具上观测到了该行为"，不是"所有同类写法都被检测器覆盖"。
- **无边界三元组**：本卡尚未跑过完整 mutation 基线 ⇒ 四态判决按规则降级 `unknown`（`four_state_verdict_638`），
  这不是缺陷，是"判决未定不预写边界"的正确输出。
- `status: machine-verified` + `human_review: required`：**未经人签**，不计入 `verified` 口径。
"""


def plan_rows() -> list[dict[str, Any]]:
    idx = load_index()
    rows: list[dict[str, Any]] = []
    for src_id, (cid, domain, title, right) in PLAN.items():
        src = idx.get(src_id)
        path = os.path.join(ROOT, "atoms", domain, f"{cid}.md")
        exists = os.path.isfile(path)
        dup = [c for c in idx.values() if c["id"] == cid]
        rows.append({
            "source_id": src_id,
            "card_id": cid,
            "domain": domain,
            "path": os.path.relpath(path, ROOT).replace(os.sep, "/"),
            "source_verdict": (src or {}).get("verdict"),
            "detector": (src or {}).get("detector"),
            "fixture": (src or {}).get("fixture_rel"),
            "fixture_sha256": (src or {}).get("fixture_sha256"),
            "exists": exists,
            "action": "skip(已存在)" if exists else ("write" if src else "skip(上游缺该样本)"),
            "has_upstream": bool(src),
            "dup_in_index": len(dup),
        })
    return rows


def apply() -> int:
    idx = load_index()
    n = 0
    for src_id, (cid, domain, title, right) in PLAN.items():
        src = idx.get(src_id)
        if not src:
            print(f"[split668] skip {src_id}：上游 index_665 无此样本")
            continue
        path = os.path.join(ROOT, "atoms", domain, f"{cid}.md")
        if os.path.isfile(path):
            print(f"[split668] skip {cid}：已存在（幂等）")
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(card_text(src, cid, domain, title, right))
        n += 1
        print(f"[split668] 写入 atoms/{domain}/{cid}.md（源 {src_id}，检测器 {src.get('detector')}）")
    print(f"[split668] 共写入 {n} 张新卡")
    return n


def summarize() -> dict[str, Any]:
    import counts_659 as counts

    rows = plan_rows()
    return {
        "schema": "queyi-card-split/668",
        "generated_by": "tools/card_split_668.py",
        "rule": ("新卡只能 `machine-verified`（**不代签**）；证据字段全部从 "
                 "data/cards_665/index_665.json 读；**不写边界三元组**（留给真实 mutation 基线）。"),
        "atoms_real_now": counts.ATOMS_REAL,
        "planned_writes": len([r for r in rows if r["action"] == "write"]),
        "rows": rows,
    }


def render_md(d: dict[str, Any]) -> str:
    lines = [
        "# 668 · B2 断言拆卡（ig → 原子卡）",
        "",
        "> 由 `python tools/card_split_668.py --report` 生成，**禁止手改**。",
        "",
        f"当前实卡数（counts_659 现算）：**{d['atoms_real_now']}**；本批计划写入 **{d['planned_writes']}** 张。",
        "",
        "| 源样本 | 新卡 | 域 | 检测器 | 夹具 | 夹具 sha256（前 16） | 动作 |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in d["rows"]:
        lines.append(f"| {r['source_id']} | `{r['card_id']}` | {r['domain']} | {r['detector']} | "
                     f"`{r['fixture']}` | `{str(r['fixture_sha256'])[:16]}…` | {r['action']} |")
    lines += [
        "",
        "## 纪律",
        "",
        "1. **不代签**：`status: machine-verified` + `human_review: required`，无 `verified_by`。",
        "2. 证据（检测器 / 夹具 / sha256 / 实测输出 / 签名 / 时间）**全部读自** `index_665.json`。",
        "3. **不写边界三元组** ⇒ 新卡四态为 `unknown`（规则的正确输出，见 `668_boundary_backfill.md`）。",
        "4. 写卡后必须重钉 Merkle（`atoms/` 在供应链覆盖内）并重跑门禁。",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="668 P1-2 · 断言拆卡（ig 机器卡 → 原子卡）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)

    if a.apply:
        apply()
        return 0
    if a.report:
        d = summarize()
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_md(d))
        print(f"[split668] 已写 {os.path.relpath(OUT_JSON, ROOT)} / {os.path.relpath(OUT_MD, ROOT)}")
        return 0

    d = summarize()
    ok = True
    for r in d["rows"]:
        flag = "ok " if r["has_upstream"] else "!! "
        print(f"  [{flag}] {r['source_id']} → {r['card_id']}（{r['action']}）")
        ok = ok and r["has_upstream"] and r["dup_in_index"] <= 1
    print(f"[split668] --check：{'PASS' if ok else 'FAIL'} · 实卡 {d['atoms_real_now']} → "
          f"{d['atoms_real_now'] + d['planned_writes']}（计划）")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
