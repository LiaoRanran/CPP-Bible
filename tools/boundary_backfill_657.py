#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""boundary_backfill_657.py — 657 B 段：把边界三元组**真正写进卡**（让四态判决跑起来）。

为什么需要这一步
================
638 §3.1 定下规矩：`pass` / `pass_with_exception` / `fail` **必须**附带
**边界三元组**（`mutation_set_hash` 64hex + `mutation_count` >0 + `generator_version`），
缺任一 ⇒ 自动降级 `unknown`。实测 47 张卡 **0 张**有边界 ⇒ 四态**全部** `unknown`
⇒ 判决系统等于没跑。639 D1 已把 23 张 verified 卡的边界**重算**成 overlay
（`data/639_boundary_backfill.json`，当时红线=受控目录零写入），本批（657）红线明确
允许"受控目录**只加边界三元组**、不改内容" ⇒ 本工具负责**落地写入**。

三元组从哪来（诚实口径，绝不编造）
================================
权威依据 = `data/mutation/full_baseline_v*.json` 里**该卡真实应用过的变异集合**
（`results` 中 `card == 本卡` 的 per-variant 记录）：

- `mutation_set_hash` = `sha256(该卡 per-variant 记录的规范 JSON)`（**本次现算**，可复现）；
- `mutation_count`  = 该卡变异条数（`len(rows)`，必然 >0）；
- `generator_version` = 基线文件名（如 `full_baseline_v7.json`）。

**这不是"运行时原生三元组"**：运行时从未产出过卡级三元组，历史卡只能重算。
差异已逐卡登记在报告 §三；若不接受该口径，唯一替代是对每张卡重跑变异验证（大工程）。

只加不改
========
本工具**只在 frontmatter 的 `status:` 行之后插入三行**；卡内正文、其它字段、
换行风格（本仓同时存在 LF / CRLF 两种卡）**逐字节保留**。幂等：已有合法三元组的卡跳过。

用法
====
    python tools/boundary_backfill_657.py --check      # 只读自检（含"未写盘"断言）
    python tools/boundary_backfill_657.py --dry-run    # 打印将写入的内容，不落盘
    python tools/boundary_backfill_657.py --apply      # 写入受控 atoms/（只加三元组）
    python tools/boundary_backfill_657.py --report     # 写 data/657_boundary_backfill.{md,json}
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
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

OUT_MD = os.path.join(ROOT, "data", "657_boundary_backfill.md")
OUT_JSON = os.path.join(ROOT, "data", "657_boundary_backfill.json")
OVERLAY_639 = os.path.join(ROOT, "data", "639_boundary_backfill.json")
MUT_DIR = os.path.join(ROOT, "data", "mutation")

FIELDS = ("mutation_set_hash", "mutation_count", "generator_version")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
_FIELD_RE = {k: re.compile(rf"^{k}:\s*(\S+)\s*$", re.MULTILINE) for k in FIELDS}
_FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)

#: 参与回填的卡状态（与 four_state_verdict_638 审计口径一致：verified；
#: red-team-verified 走同一张卡状态轴的另一档，也同样有真实基线覆盖，一并回填）。
TARGET_STATUSES = ("verified", "red-team-verified")


# ── 基线反查 ────────────────────────────────────────────────────────────
def _baseline_files() -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for f in sorted(os.listdir(MUT_DIR)):
        m = re.match(r"full_baseline_v(\d+)\.json$", f)
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out)


def newest_baseline_for(card_rel: str) -> tuple[str, list[dict[str, Any]]] | None:
    """返回覆盖该卡的**最新**基线：(文件名, 该卡 per-variant 记录)。没有 ⇒ None。"""
    found: list[tuple[int, str, list[dict[str, Any]]]] = []
    for ver, f in _baseline_files():
        try:
            d = json.load(open(os.path.join(MUT_DIR, f), encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = [r for r in (d.get("results") or [])
                if isinstance(r, dict)
                and str(r.get("card", "")).replace(os.sep, "/") == card_rel]
        if rows:
            found.append((ver, f, rows))
    if not found:
        return None
    ver, f, rows = max(found, key=lambda t: t[0])
    return f, rows


def triplet_for(rows: list[dict[str, Any]], baseline: str) -> dict[str, str]:
    """由 per-variant 记录**现算**边界三元组（确定性：同一输入必得同一哈希）。"""
    canon = json.dumps(
        [{k: r.get(k) for k in ("op", "point", "verdict", "kind")} for r in rows],
        ensure_ascii=False, sort_keys=True)
    return {"mutation_set_hash": hashlib.sha256(canon.encode("utf-8")).hexdigest(),
            "mutation_count": str(len(rows)),
            "generator_version": baseline}


# ── 卡扫描 ──────────────────────────────────────────────────────────────
def cards() -> list[str]:
    out: list[str] = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        out += [os.path.join(r, f) for f in fs if f.endswith(".md") and f != "README.md"]
    return sorted(out)


def card_status(text: str) -> str:
    m = _STATUS_RE.search(text)
    return m.group(1) if m else ""


def existing_triplet(text: str) -> dict[str, str]:
    tri: dict[str, str] = {}
    for k in FIELDS:
        m = _FIELD_RE[k].search(text)
        if m:
            tri[k] = m.group(1).strip().strip("\"'")
    return tri


def triplet_ok(tri: dict[str, str]) -> bool:
    return (len(tri) == len(FIELDS)
            and bool(_HASH_RE.match(tri.get("mutation_set_hash", "")))
            and tri.get("mutation_count", "").isdigit()
            and int(tri["mutation_count"]) > 0
            and bool(tri.get("generator_version", "").strip()))


def plan() -> list[dict[str, Any]]:
    """逐卡算计划（**只算不写**）。

    `action` 只有两种：`write`（该写而卡里还没有）/ `skip`（已有 / 不在范围 / 无覆盖）。
    落盘后重跑应当**没有** `write` ⇒ 天然幂等。
    """
    rows: list[dict[str, Any]] = []
    for p in cards():
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        raw = open(p, "rb").read()
        text = raw.decode("utf-8", errors="replace")
        st = card_status(text)
        have = existing_triplet(text)
        ok_have = triplet_ok(have)
        row: dict[str, Any] = {"card": rel, "status": st, "already": ok_have}
        hit = newest_baseline_for(rel) if st in TARGET_STATUSES else None
        if hit is not None:
            baseline, vr = hit
            row["triplet"] = triplet_for(vr, baseline)
            row["variants"] = len(vr)
        else:
            row["triplet"] = have if ok_have else {}
        if ok_have:
            row.update({"action": "skip", "reason": "卡内已有合法三元组（幂等跳过）"})
        elif st not in TARGET_STATUSES:
            row.update({"action": "skip",
                        "reason": f"卡状态 `{st}` 不在回填范围 {TARGET_STATUSES}"
                                  "（判决未定，不预先写边界）"})
        elif hit is None:
            row.update({"action": "skip", "triplet": {},
                        "reason": "无任何 mutation 基线覆盖该卡 ⇒ 照实留空（unknown）"})
        else:
            row.update({"action": "write",
                        "reason": f"由 `{row['triplet']['generator_version']}` 的 "
                                  f"{row['variants']} 条 per-variant 记录现算"})
        rows.append(row)
    return rows


def derived_rows(rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """目标状态且**确有**基线覆盖的卡（不管当前是否已写）——审计/自检用。"""
    rows = plan() if rows is None else rows
    return [r for r in rows if r["status"] in TARGET_STATUSES and r.get("variants")]


# ── 写入（只加三行）────────────────────────────────────────────────────
def patched_text(text: str, tri: dict[str, str]) -> str:
    """在 frontmatter 的 `status:` 行后插入三行；换行风格跟随文件自身。"""
    m = _FM_RE.match(text)
    if not m:
        raise ValueError("找不到 frontmatter")
    block = m.group(1)
    nl = "\r\n" if "\r\n" in text[: m.end()] else "\n"
    add = "".join(f"{nl}{k}: {tri[k]}" for k in FIELDS)
    lines = block.split(nl)
    for i, ln in enumerate(lines):
        if re.match(r"^status:\s*\S+\s*$", ln):
            lines[i] = ln + add
            break
    else:
        raise ValueError("frontmatter 内找不到 status: 行")
    new_block = nl.join(lines)
    return text[: m.start(1)] + new_block + text[m.end(1):]


def apply_writes(rows: list[dict[str, Any]]) -> int:
    """只写 `action == write` 的卡。返回写入数。"""
    n = 0
    for row in rows:
        if row["action"] != "write":
            continue
        p = os.path.join(ROOT, row["card"].replace("/", os.sep))
        raw = open(p, "rb").read()
        text = raw.decode("utf-8")
        new = patched_text(text, row["triplet"])
        # 只加不改：把新增的三行去掉必须与原文件逐字节相同
        nls = [ln for ln in new.splitlines() if ln.startswith(FIELDS)]
        stripped = "\n".join(ln for ln in new.splitlines()
                             if not ln.startswith(FIELDS))
        orig = "\n".join(text.splitlines())
        if stripped != orig or len(nls) != len(FIELDS):
            raise RuntimeError(f"只加不改断言失败：{row['card']}")
        open(p, "wb").write(new.encode("utf-8"))
        n += 1
    return n


def cross_check_639(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """与 639 overlay 交叉校验（同源重算 ⇒ 应当一致；不一致必须报出来）。"""
    if not os.path.isfile(OVERLAY_639):
        return {"available": False}
    ov = json.load(open(OVERLAY_639, encoding="utf-8"))
    mine = {r["card"]: r["triplet"] for r in derived_rows(rows)}
    same, diff, only639 = 0, [], 0
    for o in ov.get("rows", []):
        c = str(o.get("card", "")).replace(os.sep, "/")
        if o.get("status") != "derived":
            continue
        if c not in mine:
            only639 += 1
            continue
        if mine[c] == o.get("triplet"):
            same += 1
        else:
            diff.append({"card": c, "657": mine[c], "639": o.get("triplet")})
    return {"available": True, "same": same, "diff": diff, "only_639": only639,
            "overlay_n": ov.get("n_cards")}


# ── 四态重跑 ────────────────────────────────────────────────────────────
def four_state() -> dict[str, Any]:
    try:
        import four_state_verdict_638 as fs
        a = fs.audit()
        return {"n_cards": len(a["cards"]), "card_dist": a["card_dist"],
                "cards_with_boundary": a["cards_with_boundary"]}
    except Exception as exc:  # noqa: BLE001
        return {"error": repr(exc)}


def run() -> dict[str, Any]:
    rows = plan()
    writes = [r for r in rows if r["action"] == "write"]
    der = derived_rows(rows)
    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "n_cards": len(rows),
        "derived": len(der),
        "to_write": len(writes),
        "on_disk": sum(1 for r in der if r["already"]),
        "skipped": len(rows) - len(writes),
        "by_status": {s: sum(1 for r in rows if r["status"] == s)
                      for s in sorted({r["status"] for r in rows})},
        "rows": rows,
        "cross_check_639": cross_check_639(rows),
        "four_state": four_state(),
    }


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report() -> dict[str, str]:
    r = run()
    json.dump(r, open(OUT_JSON, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2)
    W = derived_rows(r["rows"])
    S = [x for x in r["rows"] if x["action"] == "skip" and not x["already"]]
    L = ["# 657 B · 边界三元组回填报告", "",
         f"> 生成：{r['generated']}。工具：`tools/boundary_backfill_657.py`。", "",
         "## 一、总览", "",
         f"- 扫描卡：**{r['n_cards']}** 张（status 分布 `{r['by_status']}`）；",
         f"- **可回填（目标状态 + 有真实变异基线覆盖）**：**{r['derived']}** 张；",
         f"  - 其中**已写入卡内**：**{r['on_disk']}** 张（`action=write` 待写入 {r['to_write']} 张）；",
         f"- 照实留空（无覆盖 / 状态不在回填范围）：**{len(S)}** 张。", "",
         "## 二、逐卡（回填对象：边界三元组）", "",
         "| 卡 | status | 变异数 | hash 前 12 | generator_version | 已落卡 |",
         "|---|---|---:|---|---|---|"]
    for x in W:
        t = x["triplet"]
        L.append(f"| `{x['card']}` | {x['status']} | {t['mutation_count']} | "
                 f"`{t['mutation_set_hash'][:12]}…` | `{t['generator_version']}` | "
                 f"{'是' if x['already'] else '否'} |")
    L += ["", "## 三、照实留空（诚实：没证据就是没证据）", "",
          "| 卡 | status | 原因 |", "|---|---|---|"]
    for x in S:
        L.append(f"| `{x['card']}` | {x['status']} | {x['reason']} |")
    cc = r["cross_check_639"]
    L += ["", "## 四、与 639 overlay 交叉校验", ""]
    if not cc.get("available"):
        L.append("- 639 overlay 不存在 ⇒ 跳过。")
    else:
        L += [f"- 同源重算一致：**{cc['same']}** 张；不一致：**{len(cc['diff'])}** 张；"
              f"仅 639 有：{cc['only_639']} 张（639 口径 `n_cards={cc['overlay_n']}`）。"]
        for d in cc["diff"]:
            L.append(f"  - ⚠️ `{d['card']}`：657 `{d['657']}` vs 639 `{d['639']}`")
    f = r["four_state"]
    L += ["", "## 五、四态重跑（写盘后口径）", ""]
    if "error" in f:
        L.append(f"- 审计异常：`{f['error']}`")
    else:
        L += [f"- verified 卡：**{f['n_cards']}** 张；分布 `{f['card_dist']}`；",
              f"- 有边界卡：**{f['cards_with_boundary']}** 张。", "",
              "> 说明：`unknown` 里剩下的卡**没有**任何变异基线覆盖 ⇒ 按 657 红线"
              "「没证据的卡照实留空」，**不补假边界**。"]
    L += ["", "## 六、诚实边界（口径）", "",
          "1. 三元组由 `data/mutation/full_baseline_v*.json` 的**历史** per-variant 记录"
          "**现算**，**不是卡生成时的运行时原生三元组**（历史卡从未产出过）；",
          "2. `generator_version` 取基线文件名，是**最接近的代理**，不是生成器自报版本；",
          "3. 迁移 #1（`unknown → pass/fail`）在规格里还要求「**证据复验非 infra**」；"
          "本批只补了**边界**这一半，证据复验的逐卡留痕在 651 H1 只覆盖 10 张 draft 卡 ⇒ "
          "23 张 verified 卡的这一半**未逐卡留痕**（登记为交人项）；",
          "4. 写入**只加三行**，卡正文与其它字段逐字节不变（`--apply` 内置断言）。"]
    open(OUT_MD, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def _atoms_fp() -> str:
    h = hashlib.sha256()
    for p in cards():
        h.update(os.path.relpath(p, ROOT).encode())
        h.update(hashlib.sha256(open(p, "rb").read()).digest())
    return h.hexdigest()


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    before = _atoms_fp()
    rows = plan()
    D = derived_rows(rows)
    chk("扫到 47 张卡", len(rows) == 47, f"{len(rows)}")
    chk("有可回填对象（目标状态 + 真实基线覆盖）", len(D) > 0, f"{len(D)} 张")
    chk("回填对象三元组合法（64hex / count>0 / version 非空）",
        all(triplet_ok(r["triplet"]) for r in D))
    chk("回填对象全部有 per-variant 记录",
        all(int(r["triplet"]["mutation_count"]) == r["variants"] for r in D))
    chk("无覆盖 / 非目标状态的卡不携带编造哈希",
        all(not r["triplet"] for r in rows if not r["already"] and not r.get("variants")))
    chk("draft 卡一律无边界（不越权替未定的判决背书）",
        all(not r["triplet"] for r in rows if r["status"] == "draft"))
    # 卡内三元组必须能由基线**独立重算**（不是手填的）
    chk("卡内三元组 == 独立重算结果",
        all(triplet_ok(existing_triplet(
            open(os.path.join(ROOT, r["card"].replace("/", os.sep)),
                 encoding="utf-8").read()))
            and existing_triplet(open(os.path.join(
                ROOT, r["card"].replace("/", os.sep)), encoding="utf-8").read())
            == r["triplet"]
            for r in D if r["already"]))
    # 确定性：同一输入两次现算必须同哈希
    hit = newest_baseline_for(D[0]["card"])
    assert hit is not None
    chk("哈希确定性（同一输入两次现算一致）",
        triplet_for(hit[1], hit[0]) == triplet_for(hit[1], hit[0]) == D[0]["triplet"])
    chk("空变异集不会产生合法三元组（fail-closed）",
        not triplet_ok(triplet_for([], "full_baseline_v7.json")))
    # 只加不改 + 换行风格保留：在**剥掉三元组的副本**上验证（落盘后卡里已有三元组）
    seen_nl: set[str] = set()
    for r in D:
        p = os.path.join(ROOT, r["card"].replace("/", os.sep))
        text = open(p, encoding="utf-8").read()
        stripped = "\n".join(ln for ln in text.splitlines()
                             if not ln.startswith(FIELDS))
        new = patched_text(stripped + "\n" if not stripped.endswith("\n") else stripped,
                           r["triplet"])
        if "\n".join(ln for ln in new.splitlines() if not ln.startswith(FIELDS)) \
                != "\n".join(stripped.splitlines()):
            chk(f"只加不改（{r['card']}）", False)
            break
        seen_nl.add("crlf" if "\r\n" in text else "lf")
    else:
        chk("只加不改（全部回填对象）", True)
        chk("换行风格保留（逐张与实际一致）",
            all(("\r\n" in patched_text(
                open(os.path.join(ROOT, r["card"].replace("/", os.sep)),
                     encoding="utf-8").read(), r["triplet"]))
                == ("\r\n" in open(os.path.join(
                    ROOT, r["card"].replace("/", os.sep)), encoding="utf-8").read())
                for r in D), f"实际风格 {sorted(seen_nl)}")
    # 机制层：CRLF 合成样本必须仍产 CRLF（本批回填对象全是 LF，机制单独锁）
    _crlf = "---\r\nstatus: verified\r\n---\r\n\r\nbody\r\n"
    chk("CRLF 合成样本：patch 后仍为 CRLF",
        "\r\n" in patched_text(_crlf, D[0]["triplet"])
        and "\n" not in patched_text(_crlf, D[0]["triplet"]).replace("\r\n", ""))
    same_after = _atoms_fp()
    chk("--check 只读（atoms 指纹不变）", before == same_after)
    chk("输出落在 data/ 下",
        all(os.path.relpath(p, ROOT).replace(os.sep, "/").startswith("data/")
            for p in (OUT_MD, OUT_JSON)))
    cc = cross_check_639(rows)
    if cc.get("available"):
        chk("与 639 overlay 重算一致（0 处不一致）", len(cc["diff"]) == 0,
            f"same={cc['same']} diff={len(cc['diff'])}")
    print(f"boundary_backfill_657 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="657 B 边界三元组回填（只加不改）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--dry-run", action="store_true", help="打印计划，不落盘")
    ap.add_argument("--apply", action="store_true", help="写入受控 atoms/（只加三行）")
    ap.add_argument("--report", action="store_true", help="写 data/657_boundary_backfill.{md,json}")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.apply:
        rows = plan()
        n = apply_writes(rows)
        print(f"[backfill657] 已写入 {n} 张卡（只加三元组，正文逐字节不变）")
        return 0
    if a.report:
        print(json.dumps(write_report(), ensure_ascii=False))
        return 0
    r = run()
    if a.dry_run or a.json:
        print(json.dumps({k: v for k, v in r.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        for x in r["rows"]:
            if x["action"] == "write":
                print(f"  WRITE {x['card']}  count={x['triplet']['mutation_count']} "
                      f"hash={x['triplet']['mutation_set_hash'][:12]}… "
                      f"ver={x['triplet']['generator_version']}")
        return 0
    print(f"[backfill657] 可回填 {r['to_write']} / 扫描 {r['n_cards']}；"
          f"四态 {r['four_state'].get('card_dist')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
