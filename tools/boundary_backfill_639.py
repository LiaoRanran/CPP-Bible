#!/usr/bin/env python3
"""639 D1 · 23 张 verified 卡边界三元组回填（**不污染受控目录**）

**债务（638 3.1）**：`four_state_verdict_638.audit()` 实测 23 张 atoms verified 卡
`cards_with_boundary=0`——全部因缺 `mutation_set_hash/mutation_count/generator_version`
落入 `unknown`。

**方法（诚实三层核查，绝不编造）**：
1. 卡文本自查：卡内是否有三元组字段（classify_card 同款正则）；
2. mutation 基线反查：`data/mutation/full_baseline_v*.json` 的 `by_card` 键实测
   **只覆盖 evidence/ 83 卡，不含 atoms 卡** ⇒ 对 atoms verified 卡不可考；
3. 结论分层：`derived`（真取到三元组）/ `unverifiable`（边界不可考，附原因）。

**输出**：overlay `data/639_boundary_backfill.json`（卡 → 三元组或"边界不可考"）
+ 报告 `data/639_boundary_backfill.md`（含四态重跑分布）。
**受控目录零写入**：回填结果落 data/ overlay，不改 atoms/ 任何文件。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "639_boundary_backfill.md")
OUT_JSON = os.path.join(ROOT, "data", "639_boundary_backfill.json")

FIELDS = ("mutation_set_hash", "mutation_count", "generator_version")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def verified_cards() -> list[str]:
    """atoms/ 下全部 verified 卡（与 four_state_verdict_638.audit 同口径）。"""
    out: list[str] = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(r, f)
            if re.search(r"^status:\s*verified\s*$",
                         open(p, encoding="utf-8", errors="replace").read(), re.MULTILINE):
                out.append(p)
    return sorted(out)


def baseline_by_card_keys() -> set[str]:
    """全部 mutation 基线 `by_card` 覆盖的卡（相对路径，/ 分隔）。"""
    keys: set[str] = set()
    for f in sorted(os.listdir(os.path.join(ROOT, "data", "mutation"))):
        if not (f.startswith("full_baseline_v") and f.endswith(".json")):
            continue
        try:
            d = json.load(open(os.path.join(ROOT, "data", "mutation", f),
                               encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        bc = d.get("by_card")
        if isinstance(bc, dict):
            keys.update(str(k).replace(os.sep, "/") for k in bc)
    return keys


def newest_baseline_for(card_rel: str) -> tuple[str, list[dict[str, Any]], dict[str, Any]] | None:
    """返回覆盖该卡的**最新**基线：(版本名, 该卡 per-variant 记录, by_card 统计)。

    per-variant 记录取自 `results`（card/op/point/verdict…），是该卡**真实应用过的
    变异集合**——三元组的权威依据。
    """
    found: list[tuple[int, str, list[dict[str, Any]], dict[str, Any]]] = []
    for f in sorted(os.listdir(os.path.join(ROOT, "data", "mutation"))):
        if not (f.startswith("full_baseline_v") and f.endswith(".json")):
            continue
        try:
            d = json.load(open(os.path.join(ROOT, "data", "mutation", f),
                               encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        bc = d.get("by_card")
        if not (isinstance(bc, dict) and card_rel in
                {str(k).replace(os.sep, "/") for k in bc}):
            continue
        m = re.search(r"full_baseline_v(\d+)", f)
        ver = int(m.group(1)) if m else 0
        rows = [r for r in (d.get("results") or [])
                if isinstance(r, dict)
                and str(r.get("card", "")).replace(os.sep, "/") == card_rel]
        found.append((ver, f, rows, bc[card_rel]))
    if not found:
        return None
    ver, name, rows, stats = max(found, key=lambda t: t[0])
    return name, rows, stats


def derive(card_path: str, by_card: set[str]) -> dict[str, Any]:
    """逐卡核查三层证据，返回 derived/unverifiable 结论（不编造）。

    `derived` 口径（诚实登记）：三元组从**最新覆盖基线**重算——
    - `mutation_set_hash` = sha256(该卡 per-variant 记录的规范 JSON)（**回填时
      重算**，非运行时哈希；同一基线可复现）；
    - `mutation_count` = 该卡变异数（= blocked+escaped+n_a）；
    - `generator_version` = 基线版本名（closest proxy，登记为口径）。
    """
    rel = os.path.relpath(card_path, ROOT).replace(os.sep, "/")
    text = open(card_path, encoding="utf-8", errors="replace").read()
    tri: dict[str, str] = {}
    for k in FIELDS:
        m = re.search(rf"^{k}:\s*(\S+)\s*$", text, re.MULTILINE)
        if m:
            tri[k] = m.group(1).strip().strip("\"'")
    if len(tri) == len(FIELDS) and _HASH_RE.match(tri["mutation_set_hash"]) \
            and tri["mutation_count"].isdigit():
        return {"card": rel, "status": "derived", "triplet": tri,
                "reason": "卡文本自带完整三元组"}
    hit = newest_baseline_for(rel)
    if hit is not None:
        name, rows, _stats = hit
        canon = json.dumps(
            [{k: r.get(k) for k in ("op", "point", "verdict", "kind")}
             for r in rows], ensure_ascii=False, sort_keys=True)
        return {"card": rel, "status": "derived",
                "triplet": {"mutation_set_hash": hashlib.sha256(
                    canon.encode("utf-8")).hexdigest(),
                    "mutation_count": str(len(rows)),
                    "generator_version": name},
                "reason": f"由最新覆盖基线 `{name}` 重算（{len(rows)} 个变异；"
                          "哈希为回填时按内容重算，非运行时哈希）"}
    return {"card": rel, "status": "unverifiable", "triplet": tri,
            "reason": "边界不可考：卡文本无三元组；无任何 mutation 基线覆盖"
                      "（by_card 与 results 均无该卡）"}


def run() -> dict[str, Any]:
    by_card = baseline_by_card_keys()
    rows = [derive(c, by_card) for c in verified_cards()]
    dist = {"derived": 0, "partial": 0, "unverifiable": 0}
    for r in rows:
        dist[r["status"]] += 1
    # 四态重跑（复用 638 工具，读真实卡）
    four_state = None
    try:
        import four_state_verdict_638 as fs
        a = fs.audit()
        four_state = {"card_dist": a["card_dist"],
                      "cards_with_boundary": a["cards_with_boundary"],
                      "n_cards": len(a["cards"])}
    except Exception as exc:  # noqa: BLE001
        four_state = {"error": repr(exc)}
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "n_cards": len(rows), "dist": dist, "rows": rows,
            "baseline_by_card_n": len(by_card), "four_state_rerun": four_state}


def write_report() -> dict[str, str]:
    r = run()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    L = ["# 639 D1 · 23 张 verified 卡边界三元组回填报告", "",
         f"> 生成：{r['generated']}。**受控目录零写入**：结论落本 overlay，"
         "不改 atoms/ 任何文件。", "",
         "## 一、逐卡核查结果", "",
         f"- verified 卡总数：**{r['n_cards']}** 张；",
         f"- `derived`（真取到完整三元组）：**{r['dist']['derived']}** 张；",
         f"- `partial`（基线覆盖但缺哈希）：**{r['dist']['partial']}** 张；",
         f"- `unverifiable`（**边界不可考**）：**{r['dist']['unverifiable']}** 张。", "",
         "| 卡 | 状态 | 已有字段 | 原因 |", "|---|---|---|---|"]
    for x in r["rows"]:
        have = ", ".join(x["triplet"]) or "无"
        L.append(f"| `{x['card']}` | {x['status']} | {have} | {x['reason']} |")
    fsr = r["four_state_rerun"]
    L += ["", "## 二、四态分类重跑（补完后）", ""]
    if "error" in fsr:
        L.append(f"- four_state 审计异常：`{fsr['error']}`")
    else:
        L += [f"- verified 卡：**{fsr['n_cards']}** 张，分布 `{fsr['card_dist']}`；",
              f"- 有边界卡：**{fsr['cards_with_boundary']}** 张（**overlay 口径**，"
              "四态工具尚未接入 overlay，卡内仍无三元组；接入后 unknown 可翻案）。", "",
              "> **诚实口径**：三元组由最新覆盖基线**重算**——`mutation_set_hash` 为"
              "回填时按该卡 per-variant 记录内容计算的哈希（非运行时哈希），"
              "`generator_version` 取基线版本名（closest proxy）。两者均可复现、"
              "非编造；与「运行时原生三元组」的差异已在此登记。"]
    L += ["", "## 三、交人项", "",
          "- 是否接受「基线重算哈希 + 基线版本名」作为历史卡边界的合法口径；",
          "- 接受后可将 overlay 接入 four_state_verdict_638（下一步），"
          "23 张卡从 unknown 翻案为对应四态；",
          "- 若要求原生运行时三元组，需对 23 卡逐张重跑 mutation 验证（大工程）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    r = run()
    chk("verified 卡 23 张", r["n_cards"] == 23)
    chk("三层结论分布和 = 卡数",
        sum(r["dist"].values()) == r["n_cards"])
    chk("derived 卡必有合法 64hex 三元组",
        all(_HASH_RE.match(x["triplet"]["mutation_set_hash"])
            for x in r["rows"] if x["status"] == "derived"))
    chk("unverifiable 卡不携带编造哈希",
        all("mutation_set_hash" not in x["triplet"] or not _HASH_RE.match(
            x["triplet"]["mutation_set_hash"])
            for x in r["rows"] if x["status"] == "unverifiable"))
    chk("derived 卡 count>0 且 version 为基线名",
        all(x["triplet"]["mutation_count"].isdigit()
            and int(x["triplet"]["mutation_count"]) > 0
            and x["triplet"]["generator_version"].startswith("full_baseline_v")
            for x in r["rows"] if x["status"] == "derived"))
    chk("基线 by_card 同时覆盖 evidence/ 与 atoms/（639 实测修正 638 认知）",
        any(k.startswith("atoms/") for k in baseline_by_card_keys())
        and any(k.startswith("evidence/") for k in baseline_by_card_keys()))
    chk("受控目录零写入：本工具只写 data/",
        all(os.path.relpath(p, ROOT).startswith("data")
            for p in (OUT_MD, OUT_JSON)))
    chk("四态重跑有结果", "error" not in r["four_state_rerun"])
    print(f"D1 backfill selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="639 D1 边界三元组回填")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--report", action="store_true", help="写报告")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(json.dumps(write_report(), ensure_ascii=False))
        return 0
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
