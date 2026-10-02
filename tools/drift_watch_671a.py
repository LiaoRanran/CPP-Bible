#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""drift_watch_671a.py — 671a B：漂移检测增强（论文 / 前端 / baseline 三臂 / 门禁规则）。

670g 留下的第二个缺口
====================
`drift_watch_670c.py` 只盯**六个核心数字**（卡数 / 规则数 / 账本 / holdout 率 / corpus 率 / 变异率）
的**跨时间相对变化**。可 670a/670g 之后最容易悄悄错的地方换到了另外四处：

  1. **论文 ↔ 产物**：论文里的 `87.5%（14/16` 与产物现算脱钩（reviewer 只看论文，看不见产物）；
  2. **前端 ↔ 产物**：前端只渲染自己的 JSON，产物改了前端没重跑 ⇒ 页面显示旧数；
  3. **baseline 三臂**：三臂必须跑在**同一批样本**上（否则"配对可比"这句话就不成立），
     且率必须能从 k/n 复算出来（写死一个数就是不可复现）；
  4. **门禁规则**：`gate_engine.RULES` 与 `data/_gate_rules.json` / 前端/文档声明必须一致
     （规则数变了而文档没跟上，读者会按错的数量理解覆盖范围）。

判据分两类（这个区分很重要）
==========================
* **确定式不一致**（论文↔产物、前端↔产物、三臂样本数、门禁规则数）：
  这类不是"数字随时间变了"，而是"同一时刻两处对不上" ⇒ **一律 DRIFT，不接受实验记录豁免**
  （实验记录只能解释"变化有据可查"，解释不了"两处互相矛盾"）。
* **跨时间漂移**（六个核心数字、前端扫描到的率）：
  沿用 670c 的协议 —— 超过阈值（默认 ±10%）**且** `data/experiments/` 下无更新的记录 ⇒ DRIFT；
  有记录 ⇒ justified（**仍然打印**，供人复核）。

三方比对的容差：率类默认 **±0.5pp**（论文写 43.8，产物算 43.75，属同一数字的不同写法）。

用法
====
    python tools/drift_watch_671a.py                    # 采集 + 对比 + 写报告（exit 1=有漂移）
    python tools/drift_watch_671a.py --json             # 机读
    python tools/drift_watch_671a.py --tolerance-pp 1   # 三方容差 1pp
    python tools/drift_watch_671a.py --no-write         # 只读
    python tools/drift_watch_671a.py --selftest

产品与责任人分离（诚实登记）
============================
本工具**只读**（除写自己的报告）。论文/前端的数字更新不在本工具射程内 —— 它只负责
**把不一致变成显式的 DRIFT**，让"谁该改"变成必须回答的问题（本批owner = 671b）。

已知限制
========
* 论文侧只认 `pct%（k/n` 这种成对写法；孤立百分比（如引用外部文献的 76%）不判漂移。
* 论文里的 (k,n) 必须**能在某个声明的产物里找到**才参与比对；找不到的记为 `unmatched`
  （可见但不判红）—— 这是刻意选择：宁可见而不红，不可凭空猜一个"对应产物"。
* 前端扫描按**键名**（`*rate_pct` / `*pct`）识别率；改了键名的新数字本轮看不见（登记为限制）。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

SCHEMA = "queyi-drift-report/671a"
DEFAULT_OUT = "data/drift_report_671a.json"
DEFAULT_THRESHOLD = 0.10                    # 跨时间：±10%
DEFAULT_TOL_PP = 0.5                        # 三方：±0.5pp
EPS = 1e-9
PASS, DRIFT, FIRST_RUN = "PASS", "DRIFT", "FIRST_RUN"

PAPER_GLOB = "research/paper_v*.md"
WEB_DIRS = ("web/data", "web/data/experiments")
ARTIFACT_CFG = "data/guard_artifacts_671a.json"
ARMS = ("fd", "static", "random")
ARM_FILES = {a: f"data/experiments/baseline_{a}.json" for a in ARMS}

#: 论文里的 `87.5%（14/16` / `87.5% (14/16)` 两种写法
CITE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*[（(]\s*(\d+)\s*/\s*(\d+)(?!\d)")
#: 前端里"像率"的键名
RATE_KEY_RE = re.compile(r"(rate_pct|_pct|pct)$", re.IGNORECASE)


def load_json(p: Path) -> Any | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def rel_change(base: Any, cur: Any) -> float | None:
    """相对变化（与 670c 同款）：任一侧缺失 ⇒ None；base=0 且 cur≠0 ⇒ inf。"""
    if not isinstance(base, (int, float)) or not isinstance(cur, (int, float)):
        return None
    if base == 0:
        return 0.0 if cur == 0 else math.inf
    return abs(float(cur) - float(base)) / abs(float(base))


def over_threshold(pct: float | None, threshold: float) -> bool:
    if pct is None:
        return False
    if math.isinf(pct):
        return True
    return pct > threshold + EPS


def finite_or_none(x: Any) -> Any:
    """672h：把 inf/nan 收敛成 None —— 报告要能被**严格 JSON 解析器**读。

    病根：`base=0 且 cur≠0` 时相对变化是 inf，直接 round 后写进 JSON 会序列化成
    `Infinity`（Python 方言，`JSON.parse` 直接抛错）⇒ 下游前端/审计工具会静默拿不到报告。
    """
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def num_or_none(x: Any) -> float | None:
    """673b A2：把「JSON 里取到的值」收敛成**有限浮点**；None / 字符串 / 布尔 / 非有限 ⇒ None。

    病根：`int(k)` / `float(val)` 直接作用在 `resolve_pointer` 的结果上——
    JSON 里写 `null`、或键名对了但类型写成字符串时，会抛 TypeError/ValueError，
    于是**漂移报告变成工具崩溃**（门禁只看退出码 ⇒ 崩溃既可能假红也可能假绿，最危险）。
    这里统一收口：取不到数就是 None，由调用方显式登记为缺口。
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    v = float(x)
    return v if math.isfinite(v) else None


def pct_display(pct: float | None) -> str:
    """人类可读的相对变化（不写进 JSON 数值字段）。"""
    if pct is None:
        return "n/a（基线值缺失）"
    if math.isinf(pct):
        return "∞（基线为 0，相对变化不可定义）"
    if math.isnan(pct):
        return "n/a（0/0）"
    return f"{round(pct * 100, 4)}%"


def sanitize_json(obj: Any) -> Any:
    """递归把非有限浮点收敛成 None（含 dict/list）。"""
    if isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_json(v) for v in obj]
    return finite_or_none(obj)


def resolve_pointer(obj: Any, pointer: str) -> tuple[bool, Any]:
    cur = obj
    for seg in [s for s in str(pointer).split(".") if s != ""]:
        if isinstance(cur, dict):
            if seg not in cur:
                return False, None
            cur = cur[seg]
        elif isinstance(cur, list):
            if not seg.lstrip("-").isdigit():
                return False, None
            i = int(seg)
            if i < 0 or i >= len(cur):
                return False, None
            cur = cur[i]
        else:
            return False, None
    return True, cur


# ─────────────────────────────────────────────────────────────────────────────
# ① 论文数字漂移
# ─────────────────────────────────────────────────────────────────────────────

def paper_candidates(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """声明式候选：{(k,n) → 现算率} 的清单 + 取数过程中的问题。

    来源三处（都是**已有产物**，不新造口径）：
      * `data/guard_artifacts_671a.json` 里 kind=rate 的指标；
      * baseline 三臂的 holdout/corpus 可测口径 k/n；
      * corpus 分层产物 `corpus_layered_670a.json` 各层。
    """
    cands: list[dict[str, Any]] = []
    problems: list[str] = []
    cfg = load_json(root / ARTIFACT_CFG)
    if isinstance(cfg, dict):
        for m in (cfg.get("metrics") or []):
            if str(m.get("kind", "rate")) != "rate":
                continue
            spec = m.get("artifact") or {}
            d = load_json(root / str(spec.get("path", "")))
            if d is None:
                problems.append(f"产物缺失：{spec.get('path')}")
                continue
            fk, k_raw = resolve_pointer(d, str(spec.get("k", "")))
            k_val = num_or_none(k_raw) if fk else None       # 673b A2：非数值/None 不再抛异常
            n = 0
            ok = k_val is not None
            for p in (spec.get("n_sum") or []):
                f, v = resolve_pointer(d, str(p))
                vv = num_or_none(v) if f else None
                if vv is None:
                    ok = False
                    break
                n += int(vv)
            if not ok or k_val is None or n <= 0:
                problems.append(f"{m.get('key')}：k/n 取不到（缺失 / 非数值 / 分母为 0）")
                continue
            cands.append({"product": f"{spec['path']}#{m.get('key')}", "k": int(k_val), "n": n,
                          "pct": round(k_val / n * 100, 4), "group": "guard_artifacts"})
    else:
        problems.append(f"三方配置缺失：{ARTIFACT_CFG}")

    for arm, rel in ARM_FILES.items():
        d = load_json(root / rel)
        if not isinstance(d, dict):
            problems.append(f"baseline 臂缺失：{rel}")
            continue
        for name in ("holdout", "corpus"):
            blk = d.get(name) or {}
            meas = blk.get("measurable") or {}
            k_raw = meas.get("numerator", meas.get("k"))
            n_raw = meas.get("denominator", meas.get("n"))
            # 672h：显式收窄类型（Any|None ⇒ int），避免裸 Any 传播进门禁判定
            if isinstance(k_raw, int) and isinstance(n_raw, int) and n_raw > 0:
                k, n = int(k_raw), int(n_raw)
                cands.append({"product": f"{rel}::{name}.measurable", "k": k, "n": n,
                              "pct": round(k / n * 100, 4), "group": "baseline_arm"})

    lay = load_json(root / "data/experiments/corpus_layered_670a.json")
    if isinstance(lay, dict):
        for name, blk in (lay.get("layers") or {}).items():
            if not isinstance(blk, dict):
                continue
            k_raw, n_raw = blk.get("numerator"), blk.get("denominator")
            if isinstance(k_raw, int) and isinstance(n_raw, int) and n_raw > 0:
                k, n = int(k_raw), int(n_raw)
                cands.append({"product": f"corpus_layered_670a.json::layers.{name}", "k": k,
                              "n": n, "pct": round(k / n * 100, 4), "group": "corpus_layer"})
    return cands, problems


def paper_files(root: Path, all_versions: bool = False) -> tuple[list[Path], list[str]]:
    """论文版本选择：默认**只判当前稿**（版本号最大的那一份）。

    为什么不判历史稿：v0.1–v0.7 是**已冻结的测量留痕**，它们的数字本来就与今天的产物不同
    （口径变更、分母扩大、假绿更正都写在里面）。把它们拉进来判漂移，等于要求历史必须与现状一致 ——
    那是噪音，而且是"看起来很像真问题"的噪音。历史版本只列出来（可见），不参与判红。
    """
    found = sorted(p for p in root.glob(PAPER_GLOB) if p.is_file())

    def ver(p: Path) -> tuple:
        m = re.search(r"paper_v(\d+(?:\.\d+)*)", p.name)
        return tuple(int(x) for x in m.group(1).split(".")) if m else (0,)

    if all_versions or len(found) <= 1:
        return found, []
    found.sort(key=ver)
    return [found[-1]], [p.name for p in found[:-1]]


def check_paper(root: Path, tol: float, all_versions: bool = False) -> dict[str, Any]:
    """论文里的 `pct%（k/n` 与声明产物现算比对（默认只判当前稿，历史稿只列出）。"""
    files, ignored = paper_files(root, all_versions)
    cands, problems = paper_candidates(root)
    by_kn: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for c in cands:
        by_kn.setdefault((c["k"], c["n"]), []).append(c)

    out: dict[str, Any] = {"status": PASS,
                           "files": [str(p.relative_to(root).as_posix()) for p in files],
                           "ignored_versions": ignored,
                           "ignored_note": ("历史稿（v0.1–v0.n-1）是冻结留痕，其数字本就与今天的产物不同 ⇒ "
                                            "只列出不判红；要全版本扫描用 --all-papers") if ignored else "",
                           "candidates": len(cands), "matched": [], "unmatched": [],
                           "drifts": [], "problems": problems}
    for p in files:
        txt = p.read_text(encoding="utf-8", errors="replace")
        for m in CITE_RE.finditer(txt):
            pct, k, n = float(m.group(1)), int(m.group(2)), int(m.group(3))
            hits = by_kn.get((k, n)) or []
            if not hits:
                out["unmatched"].append({"file": p.name, "k": k, "n": n, "pct": pct,
                                         "why": "没有声明产物的 (k,n) 与之对应 ⇒ 只登记不判红"})
                continue
            for c in hits:
                ok = abs(pct - c["pct"]) <= tol + EPS
                rec = {"file": p.name, "k": k, "n": n, "paper_pct": pct,
                       "product": c["product"], "product_pct": c["pct"],
                       "diff": round(abs(pct - c["pct"]), 4), "ok": ok}
                out["matched"].append(rec)
                if not ok:
                    out["drifts"].append({
                        "kind": "paper_vs_product", "level": "block",
                        "where": f"{p.name}（{pct}%（{k}/{n}）） vs {c['product']}（{c['pct']}%）",
                        "message": f"论文与产物差 {round(abs(pct - c['pct']), 4)}pp > 容差 {tol}pp",
                    })
    if out["drifts"]:
        out["status"] = DRIFT
    return out


# ─────────────────────────────────────────────────────────────────────────────
# ② 前端数字漂移
# ─────────────────────────────────────────────────────────────────────────────

def scan_web_rates(root: Path) -> tuple[dict[str, Any], dict[str, float]]:
    """扫前端 JSON 里"像率"的键（`*rate_pct` / `*pct`），返回 (明细, 扁平表)。"""
    rows: dict[str, Any] = {}
    flat: dict[str, float] = {}

    def walk(node: Any, prefix: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                key = f"{prefix}.{k}" if prefix else str(k)
                if isinstance(v, (int, float)) and not isinstance(v, bool) \
                        and RATE_KEY_RE.search(str(k)):
                    rows[key] = v
                    flat[key] = float(v)
                else:
                    walk(v, key)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{prefix}.{i}")

    for d in WEB_DIRS:
        dd = root / d
        if not dd.is_dir():
            continue
        for p in sorted(dd.glob("*.json")):
            data = load_json(p)
            if data is None:
                continue
            rel = str(p.relative_to(root).as_posix())
            before = len(flat)
            walk(data, rel)
            _ = before
    return rows, flat


def check_web(root: Path, tol: float, prev_values: dict[str, Any] | None,
              threshold: float, fresh: list[dict[str, Any]]) -> dict[str, Any]:
    """两层：声明的指针 ↔ 产物（确定式）；扫描到的率 ↔ 上次报告（跨时间）。"""
    out: dict[str, Any] = {"status": PASS, "declared": [], "drifts": [], "scan": {},
                           "changed": [], "justified": []}
    cfg = load_json(root / ARTIFACT_CFG)
    if isinstance(cfg, dict):
        for m in (cfg.get("metrics") or []):
            spec = m.get("artifact") or {}
            d = load_json(root / str(spec.get("path", "")))
            if d is None:
                continue
            if str(m.get("kind", "rate")) == "count":
                if spec.get("len") and isinstance(d, list):
                    expect: Any = len(d)
                else:
                    f, v = resolve_pointer(d, str(spec.get("pointer", "")))
                    expect = v if f else None
            else:
                # 673b A2：k/n 一律先收敛成有限浮点（JSON 里写 null / 字符串不再抛 TypeError）
                fk, k_raw = resolve_pointer(d, str(spec.get("k", "")))
                k_val = num_or_none(k_raw) if fk else None
                n = 0
                for p in (spec.get("n_sum") or []):
                    f, v = resolve_pointer(d, str(p))
                    vv = num_or_none(v) if f else None
                    n += int(vv) if vv is not None else 0
                expect = round(k_val / n * 100, 4) if (k_val is not None and n) else None
            for w in (m.get("web") or []):
                wd = load_json(root / str(w.get("path", "")))
                if wd is None:
                    out["drifts"].append({"kind": "web_missing_file", "level": "block",
                                          "where": str(w.get("path")),
                                          "message": "前端文件缺失 ⇒ 前端数字无从核对"})
                    continue
                found, val = resolve_pointer(wd, str(w.get("pointer", "")))
                if not found:
                    out["drifts"].append({"kind": "web_missing_pointer", "level": "block",
                                          "where": f"{w.get('path')}::{w.get('pointer')}",
                                          "message": "前端指针取不到（键名改了或被删）"})
                    continue
                # 673b A2：前端值可能是 null / 字符串 ⇒ 显式登记为缺口，不崩
                val_num, exp_num = num_or_none(val), num_or_none(expect)
                if exp_num is None or val_num is None:
                    out["declared"].append({"where": f"{w.get('path')}::{w.get('pointer')}",
                                            "value": val, "expected": expect, "ok": None})
                    if val_num is None and exp_num is not None:
                        out["drifts"].append({
                            "kind": "web_non_numeric", "level": "warn",
                            "where": f"{w.get('path')}::{w.get('pointer')}={val!r}",
                            "message": "前端该键不是数值（null/字符串）⇒ 无从对账，登记为缺口",
                        })
                    continue
                ok = abs(val_num - exp_num) <= tol + EPS
                out["declared"].append({"where": f"{w.get('path')}::{w.get('pointer')}",
                                        "value": val, "expected": expect, "ok": ok})
                if not ok:
                    out["drifts"].append({
                        "kind": "web_vs_product", "level": "block",
                        "where": f"{w.get('path')}::{w.get('pointer')}={val} vs {expect}",
                        "message": f"前端与产物差 {round(abs(float(val) - float(expect)), 4)}pp > 容差 {tol}pp",
                    })
    rows, flat = scan_web_rates(root)
    out["scan"] = {"count": len(rows), "values": flat}
    prev_flat = (prev_values or {}).get("web_rates") or {}
    for key, val in sorted(flat.items()):
        if key not in prev_flat:
            continue
        pct = rel_change(prev_flat.get(key), val)
        if over_threshold(pct, threshold):
            # 672h：数值字段只允许有限浮点（inf/nan → None），人话放 display（防 Infinity 进 JSON）
            rec = {"key": key, "baseline": prev_flat.get(key), "current": val,
                   "pct_change_pct": finite_or_none(None if pct is None else round(pct * 100, 4)),
                   "pct_change_display": pct_display(pct),
                   "source": "web/data 扫描"}
            if fresh:
                rec["evidence"] = fresh
                out["justified"].append(rec)
            else:
                out["changed"].append(rec)
                out["drifts"].append({
                    "kind": "web_rate_changed", "level": "block", "where": key,
                    "message": f"前端率 {prev_flat.get(key)} → {val}（{pct_display(pct)} > "
                               f"±{round(threshold * 100, 2)}%）且无实验记录",
                })
    if out["drifts"]:
        out["status"] = DRIFT
    return out


# ─────────────────────────────────────────────────────────────────────────────
# ③ baseline 三臂一致性
# ─────────────────────────────────────────────────────────────────────────────

def check_baseline_arms(root: Path) -> dict[str, Any]:
    """三臂必须：① 跑在同一批样本上（total 一致）；② 率能从 k/n 复算。

    「三臂一个都不在」属**未进射程**（不是"三臂不齐"）：非本仓的临时根、或 670a 尚未跑过的
    仓库不该因此判红。**有一个但不齐**才是真问题（"我有一个臂，另两个不知去向"）。
    """
    arms: dict[str, Any] = {}
    drifts: list[dict[str, Any]] = []
    present = [a for a, rel in ARM_FILES.items() if (root / rel).is_file()]
    if not present:
        return {"status": PASS, "in_scope": False, "arms": {},
                "drifts": [],
                "note": "三个 baseline 臂都不存在 ⇒ 本检查未进射程（670a 未跑过的仓库不判红）"}
    for arm, rel in ARM_FILES.items():
        d = load_json(root / rel)
        if not isinstance(d, dict):
            arms[arm] = {"available": False, "path": rel}
            continue
        rec: dict[str, Any] = {"available": True, "path": rel, "arm": d.get("arm")}
        for name in ("holdout", "corpus"):
            blk = d.get(name) or {}
            meas = blk.get("measurable") or {}
            alls = blk.get("all_samples") or {}
            k = meas.get("numerator", meas.get("k"))
            n = meas.get("denominator", meas.get("n"))
            point = meas.get("point")
            catch, miss, total = blk.get("catch"), blk.get("miss"), blk.get("total")
            rec[name] = {"k": k, "n": n, "point": point, "catch": catch, "miss": miss,
                         "unknown": blk.get("unknown"), "not_error": blk.get("not_error"),
                         "total": total, "all_n": alls.get("n")}
            if isinstance(k, int) and isinstance(n, int) and n > 0 and isinstance(point, (int, float)):
                if abs(k / n - float(point)) > 1e-9:
                    drifts.append({"kind": "baseline_rate_not_reproducible", "level": "block",
                                   "where": f"{rel}::{name}.measurable",
                                   "message": f"点估计 {point} ≠ k/n = {k}/{n}"})
            if isinstance(n, int) and isinstance(catch, int) and isinstance(miss, int) \
                    and n != catch + miss:
                drifts.append({"kind": "baseline_denominator_mismatch", "level": "block",
                               "where": f"{rel}::{name}.measurable",
                               "message": f"分母 {n} ≠ catch+miss = {catch}+{miss}"})
            if isinstance(total, int) and isinstance(alls.get("n"), int) and alls["n"] != total:
                drifts.append({"kind": "baseline_all_samples_mismatch", "level": "block",
                               "where": f"{rel}::{name}.all_samples",
                               "message": f"全样本口径 {alls['n']} ≠ total {total}"})
        arms[arm] = rec

    have = [a for a, r in arms.items() if r.get("available")]
    if len(have) < 3:
        drifts.append({"kind": "baseline_arm_missing", "level": "block",
                       "where": "data/experiments",
                       "message": f"三臂不齐（只有 {have}）⇒ 配对可比的前提不成立"})
    for name in ("holdout", "corpus"):
        totals = {a: (arms[a].get(name) or {}).get("total") for a in have}
        uniq = {t for t in totals.values() if t is not None}
        if len(uniq) > 1:
            drifts.append({"kind": "baseline_sample_mismatch", "level": "block",
                           "where": f"baseline_*::{name}.total",
                           "message": f"三臂样本数不一致 {totals} ⇒ 不是同一批样本，配对比较无效"})
    return {"status": DRIFT if drifts else PASS, "arms": arms, "drifts": drifts}


# ─────────────────────────────────────────────────────────────────────────────
# ④ 门禁规则漂移
# ─────────────────────────────────────────────────────────────────────────────

def load_engine_rules(root: Path) -> tuple[Any, str]:
    """读 gate_engine.RULES（执行权威）。按 root 惰性载入，避免跨仓库串味。"""
    p = root / "tools" / "gate_engine.py"
    if not p.is_file():
        return None, f"gate_engine.py 不存在：{p}"
    if str(root / "tools") not in sys.path:
        sys.path.insert(0, str(root / "tools"))
    try:
        name = "gate_engine_under_test_" + str(abs(hash(str(root))))[:8]
        spec = importlib.util.spec_from_file_location(name, p)
        m = importlib.util.module_from_spec(spec)     # type: ignore[arg-type]
        # 必须先登记进 sys.modules：gate_engine 用 @dataclass，dataclass 解析注解时会
        # 反查 sys.modules[cls.__module__]（不登记就会拿到 None ⇒ AttributeError）
        sys.modules[name] = m
        spec.loader.exec_module(m)                    # type: ignore[union-attr]
        return list(getattr(m, "RULES", [])), ""
    except Exception as e:                      # noqa: BLE001
        return None, f"导入 gate_engine 失败：{type(e).__name__}: {e}"


def check_gate_rules(root: Path) -> dict[str, Any]:
    """规则数 / severity 分布：执行权威（engine）↔ 缓存（_gate_rules.json）↔ 文档声明（前端）。

    两者都不在 ⇒ 未进射程（临时根不判红）；**有一个但读不到**才是真问题。
    """
    drifts: list[dict[str, Any]] = []
    has_engine = (root / "tools" / "gate_engine.py").is_file()
    has_dump = (root / "data" / "_gate_rules.json").is_file()
    if not has_engine and not has_dump:
        return {"status": PASS, "in_scope": False, "engine_rules": None, "dump_rules": None,
                "severity": {}, "severity_engine": {}, "claimed": {}, "drifts": [],
                "note": "gate_engine.py 与 _gate_rules.json 都不在 ⇒ 本检查未进射程"}
    engine, err = load_engine_rules(root)
    dump = load_json(root / "data" / "_gate_rules.json")
    status = load_json(root / "web/data/status.json")
    claimed_total = claimed_block = None
    if isinstance(status, dict):
        rules = status.get("rules") or {}
        claimed_total = rules.get("rules_total")
        claimed_block = rules.get("rules_block")

    sev_engine: dict[str, int] = {}
    if isinstance(engine, list):
        for r in engine:
            # gate_engine.RULES 的条目是 Rule 对象（有 .severity）；dict/tuple 形态也一并认
            if isinstance(r, dict):
                sev = r.get("severity")
            elif isinstance(r, (list, tuple)):
                sev = r[1] if (len(r) > 1 and isinstance(r[1], str)) else None
            else:
                sev = getattr(r, "severity", None)
            key = str(sev or "unspecified")
            sev_engine[key] = sev_engine.get(key, 0) + 1
    sev_dump: dict[str, int] = {}
    if isinstance(dump, list):
        for r in dump:
            sev = str((r or {}).get("severity", "unspecified")) if isinstance(r, dict) else "unspecified"
            sev_dump[sev] = sev_dump.get(sev, 0) + 1

    n_engine = len(engine) if isinstance(engine, list) else None
    n_dump = len(dump) if isinstance(dump, list) else None
    if err:
        drifts.append({"kind": "gate_engine_unreadable", "level": "block", "where": err,
                       "message": "执行权威读不到 ⇒ 规则数无从核对"})
    if n_engine is not None and n_dump is not None and n_engine != n_dump:
        drifts.append({"kind": "gate_rules_count_mismatch", "level": "block",
                       "where": "tools/gate_engine.py vs data/_gate_rules.json",
                       "message": f"engine.RULES={n_engine} ≠ 缓存 {n_dump}"})
    if claimed_total is not None and n_dump is not None and int(claimed_total) != n_dump:
        drifts.append({"kind": "gate_rules_doc_mismatch", "level": "block",
                       "where": "web/data/status.json::rules.rules_total",
                       "message": f"文档/前端声明 {claimed_total} ≠ 实际 {n_dump}"})
    if claimed_block is not None and sev_dump:
        actual_block = sev_dump.get("block", 0)
        if int(claimed_block) != actual_block:
            drifts.append({"kind": "gate_severity_doc_mismatch", "level": "block",
                           "where": "web/data/status.json::rules.rules_block",
                           "message": f"文档/前端声明 block={claimed_block} ≠ 实际 {actual_block}"})
    if sev_engine and sev_dump and sev_engine != sev_dump:
        drifts.append({"kind": "gate_severity_distribution_mismatch", "level": "block",
                       "where": "engine.RULES vs data/_gate_rules.json",
                       "message": f"severity 分布不一致 engine={sev_engine} dump={sev_dump}"})
    return {"status": DRIFT if drifts else PASS, "engine_rules": n_engine, "dump_rules": n_dump,
            "severity": sev_dump, "severity_engine": sev_engine,
            "claimed": {"rules_total": claimed_total, "rules_block": claimed_block},
            "drifts": drifts}


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 跨时间核心数字（复用 670c 的采集器）
# ─────────────────────────────────────────────────────────────────────────────

def unpoison_engine_cache(root: Path) -> str | None:
    """把 `sys.modules["gate_engine"]` 里"别人的"模块清掉，返回被清掉的来源路径。

    为什么需要（实测踩到的坑）：`drift_watch_670c.metric_rules()` 用 **按名字** 的
    `import gate_engine` 读规则数，而它读的 tools 目录取决于当时的 sys.path。测试里跑过
    「tmp 仓库的假 gate_engine（2 条规则）」之后，全局模块缓存里就留下了那个假模块
    ⇒ 真实仓库再算 rules_total 会读到 **2**（67 → 2 = -97%），漂移监控立刻误报 DRIFT。
    这是**跨测试的 import 污染**，不是数字真的变了；护栏放在调用 670c 采集器之前。
    """
    want = (root / "tools" / "gate_engine.py")
    mod = sys.modules.get("gate_engine")
    if mod is None:
        return None
    got = Path(str(getattr(mod, "__file__", "") or "")).resolve()
    try:
        same = got == want.resolve()
    except OSError:
        same = False
    if not same:
        sys.modules.pop("gate_engine", None)
        return str(got)
    return None


def core_metrics(root: Path) -> list[dict[str, Any]]:
    try:
        import drift_watch_670c as D670  # noqa: PLC0415
    except Exception as e:                   # noqa: BLE001
        return [{"key": "core_metrics", "label": "670c 采集器不可用", "value": None, "unit": "?",
                 "source": "?", "formula": "?", "available": False,
                 "error": f"{type(e).__name__}: {e}"}]
    poisoned = unpoison_engine_cache(root)
    metrics = D670.collect_metrics(root)
    if poisoned:
        for m in metrics:
            if m.get("key") == "rules_total":
                m["cache_note"] = f"清除过被污染的 gate_engine 缓存（来源：{poisoned}）"
    return metrics


def fresh_experiments(root: Path, since: float | None) -> list[dict[str, Any]]:
    d = root / "data" / "experiments"
    out: list[dict[str, Any]] = []
    if not d.is_dir():
        return out
    for p in sorted(d.rglob("*.json")):
        try:
            mt = p.stat().st_mtime
        except OSError:
            continue
        if since is None or mt > since:
            out.append({"path": p.relative_to(root).as_posix(),
                        "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt))})
    return out


def load_previous(out_path: Path) -> dict[str, Any] | None:
    d = load_json(out_path)
    if not isinstance(d, dict) or not isinstance(d.get("values"), dict):
        return None
    return d


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(root: Path = ROOT, out_path: Path | None = None,
             threshold: float = DEFAULT_THRESHOLD, tol_pp: float = DEFAULT_TOL_PP,
             write: bool = True, all_papers: bool = False) -> dict[str, Any]:
    op = out_path if out_path is not None else (root / DEFAULT_OUT)
    prev = load_previous(op)
    since = None
    if isinstance(prev, dict):
        s = prev.get("generated_at_epoch")
        if isinstance(s, (int, float)):
            since = float(s)
        else:
            try:
                since = op.stat().st_mtime
            except OSError:
                since = None
    fresh = fresh_experiments(root, since)

    metrics = core_metrics(root)
    values = {m["key"]: m["value"] for m in metrics if m.get("available")}

    paper = check_paper(root, tol_pp, all_papers)
    web = check_web(root, tol_pp, prev, threshold, fresh)
    arms = check_baseline_arms(root)
    gates = check_gate_rules(root)

    # 跨时间：核心数字（协议同 670c）
    ok: list[dict[str, Any]] = []
    unjustified: list[dict[str, Any]] = []
    justified: list[dict[str, Any]] = []
    base_values = (prev or {}).get("values") or {}
    for m in metrics:
        k = m["key"]
        if not m.get("available") or k not in base_values:
            continue
        pct = rel_change(base_values.get(k), m.get("value"))
        rec = {"key": k, "label": m.get("label"), "baseline": base_values.get(k),
               "current": m.get("value"),
               "pct_change_pct": (None if (pct is None or math.isinf(pct)) else round(pct * 100, 4)),
               "source": m.get("source")}
        if over_threshold(pct, threshold):
            if fresh:
                rec["evidence"] = fresh
                justified.append(rec)
            else:
                unjustified.append(rec)
        else:
            ok.append(rec)
    for rec in web["changed"]:
        unjustified.append({**rec, "key": rec["key"], "label": "前端扫描率"})
    for rec in web["justified"]:
        justified.append({**rec, "label": "前端扫描率"})

    deterministic = {"paper": paper, "web_declared": [d for d in web["declared"]],
                     "baseline_arms": arms, "gate_rules": gates}
    det_drifts = (paper["drifts"] + [d for d in web["drifts"] if d["level"] == "block"]
                  + arms["drifts"] + gates["drifts"])
    first = prev is None
    overall = FIRST_RUN if first else (DRIFT if (det_drifts or unjustified) else PASS)

    report: dict[str, Any] = {
        "schema": SCHEMA,
        "tool": "drift_watch_671a",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at_epoch": round(time.time(), 3),
        "threshold": threshold,
        "threshold_pct": round(threshold * 100, 4),
        "tolerance_pp": tol_pp,
        "output": str(op),
        "overall": overall,
        "baseline_found": not first,
        "metrics": metrics,
        "values": values,
        "unavailable": [m["key"] for m in metrics if not m.get("available")],
        "checks": {"paper": paper, "web": web, "baseline_arms": arms, "gate_rules": gates},
        "deterministic": deterministic,
        "deterministic_drifts": det_drifts,
        "ok": ok,
        "drifted_unjustified": unjustified,
        "drifted_justified": justified,
        "experiments": {"dir": "data/experiments", "fresh": fresh,
                        "considered_since_epoch": since},
        "pending_owner_671b": [m for m in (paper.get("problems") or []) if False],
        "notes": [],
        "baseline_values_for_next_run": values,
        "web_rates_for_next_run": (web["scan"] or {}).get("values", {}),
    }
    if first:
        report["notes"].append("未找到上一次基线报告 ⇒ 本次只标定基线，不做跨时间判定（不判红）；"
                               "确定式检查（论文/前端/三臂/门禁）仍然判。")
    if det_drifts:
        report["notes"].append(f"{len(det_drifts)} 条**确定式不一致**（同一时刻两处对不上，"
                               "不接受实验记录豁免）—— 这类必须有人改数字，不是「有据可查」就放行。")
    if fresh:
        report["notes"].append(f"发现 {len(fresh)} 份更新的实验记录 ⇒ 跨时间漂移记为 justified（仍打印）。")
    else:
        report["notes"].append("data/experiments/ 下无更新的实验记录 ⇒ 跨时间漂移一律判红。")
    report["notes"].append("论文/前端的数字更新不在本工具射程内；它只把不一致变成显式 DRIFT。")
    report["values"] = values                       # 供下次跨时间比对
    report["web_rates"] = report["web_rates_for_next_run"]
    _ = report["pending_owner_671b"]
    if write:
        op.parent.mkdir(parents=True, exist_ok=True)
        # 672h：落盘前统一收敛非有限浮点（inf/nan ⇒ None），保证严格 JSON 可解析
        report = sanitize_json(report)
        op.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def render(rep: dict[str, Any]) -> str:
    c = rep["checks"]
    L = [f"[drift-watch-671a] overall={rep['overall']}  跨时间阈值=±{rep['threshold_pct']}%  "
         f"三方容差=±{rep['tolerance_pp']}pp  报告={rep['output']}",
         f"  论文  <- {', '.join(c['paper']['files']) or '(无)'}："
         f"匹配 {len(c['paper']['matched'])}，未匹配 {len(c['paper']['unmatched'])}，"
         f"drift {len(c['paper']['drifts'])}",
         f"  前端  声明 {len(c['web']['declared'])} 条，扫描到 {c['web']['scan']['count']} 个率，"
         f"drift {len([d for d in c['web']['drifts']])}",
         f"  三臂  样本数 holdout={ {a: (r.get('holdout') or {}).get('total') for a, r in c['baseline_arms']['arms'].items()} }"
         f" corpus={ {a: (r.get('corpus') or {}).get('total') for a, r in c['baseline_arms']['arms'].items()} }"
         f"  drift {len(c['baseline_arms']['drifts'])}",
         f"  门禁  engine={c['gate_rules']['engine_rules']} 缓存={c['gate_rules']['dump_rules']} "
         f"{c['gate_rules']['severity']} drift {len(c['gate_rules']['drifts'])}",
         f"  跨时间 核心数字 {len(rep['values'])} 项：ok={len(rep['ok'])} "
         f"越阈值(有据)={len(rep['drifted_justified'])} 越阈值(无据)={len(rep['drifted_unjustified'])}"]
    for d in rep["deterministic_drifts"][:12]:
        L.append(f"  [DRIFT] {d['kind']}: {d['where']} — {d['message']}")
    for d in rep["drifted_unjustified"][:8]:
        L.append(f"  [DRIFT] {d.get('key')}: {d.get('baseline')} → {d.get('current')}")
    for d in rep["drifted_justified"][:8]:
        L.append(f"  [just.] {d.get('key')}: {d.get('baseline')} → {d.get('current')}")
    for n in rep["notes"]:
        L.append(f"  [note] {n}")
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# 自检
# ─────────────────────────────────────────────────────────────────────────────

def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("相对变化：+10% 正好不判漂移", over_threshold(rel_change(100, 110), 0.10) is False)
    chk("相对变化：+10.01% 判漂移", over_threshold(rel_change(100, 110.01), 0.10) is True)
    chk("相对变化：缺一侧 ⇒ 不判", rel_change(None, 5) is None)
    chk("相对变化：0 → 非 0 ⇒ inf 判漂移", over_threshold(rel_change(0, 3), 0.10) is True)
    # 672h：非有限浮点不得进 JSON（Python 的 Infinity/NaN 不是合法 JSON）
    chk("inf ⇒ 数值字段落 None", finite_or_none(math.inf) is None)
    chk("nan ⇒ 数值字段落 None", finite_or_none(math.nan) is None)
    chk("显示值：inf 说人话", "∞" in pct_display(math.inf) and "基线为 0" in pct_display(math.inf))
    _j = json.dumps(sanitize_json({"a": math.inf, "b": [math.nan, 1.0]}), ensure_ascii=False)
    chk("sanitize 后 json.dumps 无 Infinity/NaN", "Infinity" not in _j and "NaN" not in _j)
    triples = CITE_RE.findall("**87.5%（14/16）** 与 43.8% (14/32)")
    chk("论文三元组：全角/半角都认",
        triples == [("87.5", "14", "16"), ("43.8", "14", "32")] or len(triples) == 2)
    chk("论文三元组：不吞相邻数字", CITE_RE.findall("35.0%–43.8% 间") == [])
    chk("前端率键名识别", bool(RATE_KEY_RE.search("rate_pct")) and bool(RATE_KEY_RE.search("pct"))
        and not RATE_KEY_RE.search("rate_count"))
    chk("指针解析", resolve_pointer({"a": {"b": [1, 2]}}, "a.b.1") == (True, 2))
    chk("指针缺失", resolve_pointer({"a": 1}, "a.b") == (False, None))
    # 673b A2：空值 / 非数值**不得**把报告变成崩溃（崩溃 ⇒ 门禁只看退出码，假红假绿都危险）
    chk("num_or_none：null ⇒ None", num_or_none(None) is None)
    chk("num_or_none：字符串 ⇒ None（不猜）", num_or_none("81.2") is None)
    chk("num_or_none：bool ⇒ None（True 不是 1）", num_or_none(True) is None)
    chk("num_or_none：inf/nan ⇒ None",
        num_or_none(math.inf) is None and num_or_none(math.nan) is None)
    chk("num_or_none：正常数 ⇒ float", num_or_none(17) == 17.0 and num_or_none(0.0) == 0.0)
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "data").mkdir(parents=True, exist_ok=True)
        (t / "web" / "data").mkdir(parents=True, exist_ok=True)
        (t / ARTIFACT_CFG).write_text(json.dumps({"metrics": [
            {"key": "holdout_rate_pct", "kind": "rate",
             "artifact": {"path": "data/prod.json", "k": "k", "n_sum": ["n"]},
             "web": [{"path": "web/data/m.json", "pointer": "rate"}]}]}), encoding="utf-8")
        # ① 产物 k=null、前端 rate=null ⇒ 不抛异常，且登记缺口
        (t / "data" / "prod.json").write_text(json.dumps({"k": None, "n": 41}), encoding="utf-8")
        (t / "web" / "data" / "m.json").write_text(json.dumps({"rate": None}), encoding="utf-8")
        r1 = check_web(t, DEFAULT_TOL_PP, None, DEFAULT_THRESHOLD, [])
        chk("产物 k=null：不崩且给出 declared 记录", isinstance(r1, dict) and bool(r1["declared"]))
        # ② 产物正常、前端写成字符串 ⇒ 登记 web_non_numeric（warn），不崩
        (t / "data" / "prod.json").write_text(json.dumps({"k": 34, "n": 41}), encoding="utf-8")
        (t / "web" / "data" / "m.json").write_text(json.dumps({"rate": "82.9"}), encoding="utf-8")
        r2 = check_web(t, DEFAULT_TOL_PP, None, DEFAULT_THRESHOLD, [])
        kinds = [d["kind"] for d in r2["drifts"]]
        chk("前端写成字符串 ⇒ web_non_numeric 缺口", "web_non_numeric" in kinds)
        # ③ 正常数值 ⇒ 一致（不得因加固而误报）
        (t / "web" / "data" / "m.json").write_text(json.dumps({"rate": 82.9}), encoding="utf-8")
        r3 = check_web(t, DEFAULT_TOL_PP, None, DEFAULT_THRESHOLD, [])
        chk("正常数值仍判一致（加固未误报）",
            r3["status"] == PASS and all(d["ok"] for d in r3["declared"]))
    cands, probs = paper_candidates(ROOT)
    chk("本仓论文候选非空", len(cands) >= 8)
    chk("候选都带 k/n/pct", all(c["k"] and c["n"] and c["pct"] is not None for c in cands))
    got = check_paper(ROOT, DEFAULT_TOL_PP)
    chk("本仓论文扫描：至少匹配上一条", len(got["matched"]) >= 4)
    chk("本仓论文扫描：无 drift（论文与产物一致）", got["status"] == PASS)
    arms = check_baseline_arms(ROOT)
    chk("本仓三臂：样本数一致、率可复算", arms["status"] == PASS)
    gates = check_gate_rules(ROOT)
    chk("本仓门禁规则：engine=缓存=文档", gates["status"] == PASS and gates["engine_rules"] == 67)
    chk("本仓 severity 分布（block 44）", gates["severity"].get("block") == 44)
    rows, flat = scan_web_rates(ROOT)
    chk("本仓前端扫描到率", len(flat) >= 5)
    print(f"drift_watch_671a selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671a B：漂移检测增强（论文/前端/三臂/门禁）")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件上级目录；测试用）")
    ap.add_argument("--out", default=None, help=f"报告路径（默认 {DEFAULT_OUT}）")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="跨时间相对变化阈值（默认 0.10；>1 视为百分数）")
    ap.add_argument("--tolerance-pp", type=float, default=DEFAULT_TOL_PP,
                    help=f"三方比较容差（百分点，默认 {DEFAULT_TOL_PP}）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--all-papers", action="store_true",
                    help="连历史稿一起扫（默认只判当前稿：历史稿是冻结留痕，不判漂移）")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    root = Path(a.root).resolve() if a.root else ROOT
    out = Path(a.out) if a.out else None
    th = a.threshold / 100.0 if a.threshold > 1 else a.threshold
    rep = evaluate(root, out, th, a.tolerance_pp, write=not a.no_write,
                   all_papers=a.all_papers)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    return 1 if rep["overall"] == DRIFT else 0


if __name__ == "__main__":
    raise SystemExit(main())
