#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""drift_watch_670c.py — 670c D3：关键数字漂移监控（无实验记录就标红）。

为什么要有它
============
669d 的六条规则守的是「同一时刻三处数字一致」；但**跨时间**的漂移没人守：
今天的卡数 53、明天 113，检出率从 87.5% 掉到 66.7%——每一个单独看上去都「自洽」，
合起来却是「悄悄换了口径 / 悄悄回退」。本工具把关键数字记在一份基线报告里，
下次跑时比较；**变化超过阈值（默认 ±10%）且没有对应的实验记录**就标红。

为什么「没有实验记录」才红（而不是任何变化都红）
==============================================
数字**本来就会变**：补卡、加规则、扩容语料都会动这些量。判据不是「变了」，而是
「变了却查无实据」——若 data/experiments/ 下有比上次基线更新的实验记录，说明这次
变化有据可查（有人做了实验/重跑并落盘），记为 justified（**仍然打印**，供人复核），
不判红。反之，无人认领的数字漂移就是本工具要抓的形态（666「81.2% 假绿」同源）。

关键数字与**真实来源**（逐个核实，禁止手抄）
==========================================
| 键 | 含义 | 事实源文件 | 现算公式 |
|---|---|---|---|
| cards_total | 卡数（全量口径） | tools/counts_659.py（659 A/B3 唯一权威源） | 原子全量 + 证据卡 |
| rules_total | 规则数 | tools/gate_engine.py::RULES（661 A2 口径裁定） | len(RULES)，并与 data/_gate_rules.json 交叉核对 |
| ledger_events | 账本数（452 账本） | data/authority/decision_event_v2_ledger.jsonl | 非空行数 |
| holdout_rate_pct | holdout 检出率（可测口径） | data/holdout_reveal_3_665.json | catch/(catch+miss) |
| corpus_rate_pct | corpus 检出率（可测口径） | data/external_corpus_reveal_665.json | catch/(catch+miss) |
| mutation_core_pct | 变异率（core 击杀率） | data/656_mutation_report_core.json | killed/(killed+survived) |

用法
====
    python tools/drift_watch_670c.py                    # 采集 + 对比 + 写报告（exit 1=有无人认领漂移）
    python tools/drift_watch_670c.py --json             # 只打印机读 JSON（仍写报告）
    python tools/drift_watch_670c.py --threshold 5      # 阈值 5%（>1 视为百分数）
    python tools/drift_watch_670c.py --no-write         # 不写报告（只读）

已知限制（诚实登记）
==================
* 「有实验记录」用的是**目录 mtime 粗判**：只看 data/experiments/*.json 里有没有比上次
  基线更新的文件，不校验该实验是否**真的覆盖**了漂移的那个指标。属保守放行（宁可少红），
  在报告的 experiments.fresh 里逐条列出供人复核。
* 基线就是**上一次的报告文件本身**（data/drift_report_670c.json）。若该文件被删/改坏，
  下次跑会退化为 FIRST_RUN（重新标定，不判红）——这是刻意选择：宁可漏报一次，不可崩。
* 阈值对**相对变化**生效；基线值为 0 时相对变化无定义（记为 inf，只要变了就判漂移）。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-drift-report/v1"
DEFAULT_OUT = "data/drift_report_670c.json"
DEFAULT_THRESHOLD = 0.10          # ±10%
EPS = 1e-9                        # 浮点边界容差：正好等于阈值 ⇒ 不算漂移（「超过」才红）

PASS, DRIFT, FIRST_RUN = "PASS", "DRIFT", "FIRST_RUN"


# ─────────────────────────────────────────────────────────────────────────────
# 采集器（每个都只读、缺失即 unavailable，绝不臆造数字）
# ─────────────────────────────────────────────────────────────────────────────

def _load_json(root: Path, rel: str) -> Any | None:
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _cards_fallback(root: Path) -> int | None:
    """非本仓根时的兜底计数（与 counts_659 口径一致，但**非权威源**，见报告 source 字段）。"""
    atoms = draft = 0
    for p in sorted((root / "atoms").rglob("ATOM-*.md")):
        if p.parent.name == "draft650":
            draft += 1
        else:
            atoms += 1
    ev = sum(1 for _ in (root / "evidence").rglob("EV-*.md")) if (root / "evidence").is_dir() else 0
    if atoms + draft + ev == 0:
        return None
    return atoms + draft + ev


def metric_cards(root: Path) -> dict[str, Any]:
    rel = "tools/counts_659.py"
    if (root / rel).is_file():
        sys.path.insert(0, str(root / "tools"))
        try:
            import counts_659 as counts  # noqa: PLC0415  (惰性导入：避免模块级耦合)
            snap = counts.snapshot()
            return {"key": "cards_total", "label": "卡数（全量口径）", "value": snap["cards_total"],
                    "unit": "张", "source": rel, "formula": "原子卡全量 + 证据卡（counts_659 现算）",
                    "available": True}
        except Exception as e:                      # noqa: BLE001  采集失败不得让门禁崩
            fb = _cards_fallback(root)
            return {"key": "cards_total", "label": "卡数（全量口径）", "value": fb, "unit": "张",
                    "source": "atoms/ 与 evidence/ 文件计数", "formula": "兜底计数（counts_659 导入失败）",
                    "available": fb is not None, "error": f"{type(e).__name__}: {e}"}
    fb = _cards_fallback(root)
    return {"key": "cards_total", "label": "卡数（全量口径）", "value": fb, "unit": "张",
            "source": "atoms/ 与 evidence/ 文件计数",
            "formula": "兜底计数（非本仓根；权威源 tools/counts_659.py 不在）",
            "available": fb is not None}


def metric_rules(root: Path) -> dict[str, Any]:
    """规则数：gate_engine.RULES 为执行权威；data/_gate_rules.json 为同步缓存，两者必须一致。"""
    engine_n: int | None = None
    if (root / "tools" / "gate_engine.py").is_file():
        sys.path.insert(0, str(root / "tools"))
        try:
            import gate_engine  # noqa: PLC0415
            engine_n = len(gate_engine.RULES)
        except Exception:                           # noqa: BLE001
            engine_n = None
    dump = _load_json(root, "data/_gate_rules.json")
    dump_n = len(dump) if isinstance(dump, list) else None
    if engine_n is None and dump_n is None:
        return {"key": "rules_total", "label": "规则数", "value": None, "unit": "条",
                "source": "tools/gate_engine.py", "formula": "len(RULES)", "available": False}
    value = engine_n if engine_n is not None else dump_n
    return {"key": "rules_total", "label": "规则数", "value": value, "unit": "条",
            "source": "tools/gate_engine.py", "formula": "len(RULES)",
            "cross_check": {"data/_gate_rules.json": dump_n,
                            "consistent": (engine_n == dump_n) if (engine_n and dump_n) else None},
            "available": True}


def metric_ledger(root: Path) -> dict[str, Any]:
    rel = "data/authority/decision_event_v2_ledger.jsonl"
    p = root / rel
    if not p.is_file():
        return {"key": "ledger_events", "label": "账本数（452 账本）", "value": None, "unit": "条",
                "source": rel, "formula": "非空行数", "available": False}
    n = sum(1 for line in p.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())
    return {"key": "ledger_events", "label": "账本数（452 账本）", "value": n, "unit": "条",
            "source": rel, "formula": "非空行数", "available": True}


def metric_holdout(root: Path) -> dict[str, Any]:
    rel = "data/holdout_reveal_3_665.json"
    d = _load_json(root, rel)
    es = (d or {}).get("error_subset") if isinstance(d, dict) else None
    if isinstance(es, dict):
        c, m = es.get("catch"), es.get("miss")
        if isinstance(c, int) and isinstance(m, int) and (c + m):
            return {"key": "holdout_rate_pct", "label": "holdout 检出率（可测口径）",
                    "value": round(c / (c + m) * 100, 4), "unit": "%", "source": rel,
                    "formula": f"catch/(catch+miss) = {c}/{c + m}", "available": True}
    return {"key": "holdout_rate_pct", "label": "holdout 检出率（可测口径）", "value": None,
            "unit": "%", "source": rel, "formula": "catch/(catch+miss)", "available": False}


def metric_corpus(root: Path) -> dict[str, Any]:
    rel = "data/external_corpus_reveal_665.json"
    d = _load_json(root, rel)
    if isinstance(d, dict):
        c, m = d.get("catch"), d.get("miss")
        if isinstance(c, int) and isinstance(m, int) and (c + m):
            return {"key": "corpus_rate_pct", "label": "corpus 检出率（可测口径）",
                    "value": round(c / (c + m) * 100, 4), "unit": "%", "source": rel,
                    "formula": f"catch/(catch+miss) = {c}/{c + m}", "available": True}
    return {"key": "corpus_rate_pct", "label": "corpus 检出率（可测口径）", "value": None,
            "unit": "%", "source": rel, "formula": "catch/(catch+miss)", "available": False}


def metric_mutation(root: Path) -> dict[str, Any]:
    rel = "data/656_mutation_report_core.json"
    d = _load_json(root, rel)
    if isinstance(d, dict):
        k, s = d.get("killed"), d.get("survived")
        if isinstance(k, int) and isinstance(s, int) and (k + s):
            return {"key": "mutation_core_pct", "label": "变异率（core 击杀率）",
                    "value": round(k / (k + s) * 100, 4), "unit": "%", "source": rel,
                    "formula": f"killed/(killed+survived) = {k}/{k + s}", "available": True}
    return {"key": "mutation_core_pct", "label": "变异率（core 击杀率）", "value": None,
            "unit": "%", "source": rel, "formula": "killed/(killed+survived)", "available": False}


COLLECTORS = (metric_cards, metric_rules, metric_ledger, metric_holdout, metric_corpus, metric_mutation)


def collect_metrics(root: Path = ROOT) -> list[dict[str, Any]]:
    """采集全部关键数字（只读；单个采集器异常不影响其它）。"""
    out: list[dict[str, Any]] = []
    for fn in COLLECTORS:
        try:
            out.append(fn(root))
        except Exception as e:                      # noqa: BLE001  门禁自身不得崩
            out.append({"key": getattr(fn, "__name__", "?"), "label": "?", "value": None,
                        "unit": "?", "source": "?", "formula": "?", "available": False,
                        "error": f"{type(e).__name__}: {e}"})
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 漂移判定
# ─────────────────────────────────────────────────────────────────────────────

def pct_change(base: float | None, cur: float | None) -> float | None:
    """相对变化 |cur-base|/|base|；任一侧缺 ⇒ None；base=0 且 cur≠0 ⇒ inf。"""
    if base is None or cur is None:
        return None
    if base == 0:
        return 0.0 if cur == 0 else math.inf
    return abs(float(cur) - float(base)) / abs(float(base))


def is_drift(pct: float | None, threshold: float) -> bool:
    """超过阈值才算漂移。

    * 任一侧缺失（None）⇒ 不判漂移（不可比 ≠ 漂移）；
    * 正好等于阈值 ⇒ 不判漂移（D3 要求「**超过** ±10% 才标红」，边界含在容忍内）；
    * 基线为 0 而现值非 0 ⇒ pct=inf ⇒ 判漂移（从无到有本身就是大变化，见 docstring 限制第 3 条）。
    """
    if pct is None:
        return False
    if math.isinf(pct):
        return True
    return pct > threshold + EPS


def fresh_experiments(root: Path, since_epoch: float | None) -> list[dict[str, Any]]:
    """data/experiments/ 下比基线更新的记录（粗判；不校验是否覆盖具体指标）。"""
    d = root / "data" / "experiments"
    out: list[dict[str, Any]] = []
    if not d.is_dir():
        return out
    for p in sorted(d.rglob("*.json")):
        try:
            mt = p.stat().st_mtime
        except OSError:
            continue
        if since_epoch is None or mt > since_epoch:
            out.append({"path": p.relative_to(root).as_posix(),
                        "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt)),
                        "mtime_epoch": round(mt, 3)})
    return out


def load_previous(out_path: Path) -> dict[str, Any] | None:
    try:
        d = json.loads(out_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(d, dict) or not isinstance(d.get("values"), dict):
        return None
    return d


def evaluate(root: Path = ROOT, out_path: Path | None = None,
             threshold: float = DEFAULT_THRESHOLD, write: bool = True) -> dict[str, Any]:
    """采集 → 与上次报告对比 →（可选）写报告。返回机读 dict。"""
    op = out_path if out_path is not None else (root / DEFAULT_OUT)
    metrics = collect_metrics(root)
    values = {m["key"]: m["value"] for m in metrics if m["available"]}
    unavailable = [m["key"] for m in metrics if not m["available"]]
    prev = load_previous(op)

    report: dict[str, Any] = {
        "schema": SCHEMA,
        "tool": "drift_watch_670c",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at_epoch": round(time.time(), 3),
        "threshold": threshold,
        "threshold_pct": round(threshold * 100, 4),
        "output": str(op),
        "metrics": metrics,
        "values": values,
        "unavailable": unavailable,
        "notes": [],
    }

    if prev is None:
        report.update(overall=FIRST_RUN, baseline_found=False, baseline={},
                      baseline_generated_at_epoch=None,
                      ok=[], drifted_unjustified=[], drifted_justified=[],
                      experiments={"dir": "data/experiments", "fresh": [],
                                   "considered_since_epoch": None})
        report["notes"].append("未找到上一次基线报告 ⇒ 本次只标定基线，不做漂移判定（不判红）。")
    else:
        base_values = {k: v for k, v in (prev.get("values") or {}).items()}
        since = prev.get("generated_at_epoch")
        if not isinstance(since, (int, float)):
            try:
                since = op.stat().st_mtime
            except OSError:
                since = None
        fresh = fresh_experiments(root, float(since) if isinstance(since, (int, float)) else None)
        ok: list[dict[str, Any]] = []
        drifted: list[dict[str, Any]] = []
        justified: list[dict[str, Any]] = []
        for m in metrics:
            k = m["key"]
            if not m["available"]:
                continue
            if k not in base_values:
                report["notes"].append(f"基线无 {k} 记录 ⇒ 本次只记录，不判定。")
                continue
            b, c = base_values.get(k), m["value"]
            pct = pct_change(b if isinstance(b, (int, float)) else None,
                             c if isinstance(c, (int, float)) else None)
            rec = {"key": k, "label": m["label"], "baseline": b, "current": c,
                   "pct_change": (None if pct is None else (round(pct, 6) if not math.isinf(pct) else "inf")),
                   "pct_change_pct": (None if pct is None or math.isinf(pct) else round(pct * 100, 4)),
                   "threshold": threshold, "source": m["source"]}
            if is_drift(pct, threshold):
                if fresh:
                    rec["evidence"] = fresh
                    justified.append(rec)
                else:
                    drifted.append(rec)
            else:
                ok.append(rec)
        report.update(overall=(DRIFT if drifted else PASS), baseline_found=True,
                      baseline=base_values,
                      baseline_generated_at_epoch=since,
                      ok=ok, drifted_unjustified=drifted, drifted_justified=justified,
                      experiments={"dir": "data/experiments", "fresh": fresh,
                                   "considered_since_epoch": since})
        if not fresh:
            report["notes"].append("data/experiments/ 下无更新的实验记录 ⇒ 越阈值的变化一律判红。")
        else:
            report["notes"].append(
                f"发现 {len(fresh)} 份更新的实验记录 ⇒ 越阈值变化记为 justified（不判红，但仍打印供复核）。")

    # 新基线 = 本次采集值
    report["baseline_values_for_next_run"] = values
    if write:
        op.parent.mkdir(parents=True, exist_ok=True)
        op.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def render(rep: dict[str, Any]) -> str:
    L = [f"[drift-watch] overall={rep['overall']}  阈值=±{rep['threshold_pct']}%  "
         f"指标={len(rep['values'])}/{len(rep['metrics'])} 可得  报告={rep['output']}"]
    for m in rep["metrics"]:
        v = m["value"]
        L.append(f"  {'OK ' if m['available'] else 'N/A'} {m['key']:20} = {v} {m['unit']}"
                 f"   ← {m['source']}")
    for d in rep["drifted_unjustified"]:
        L.append(f"  [DRIFT] {d['key']}: {d['baseline']} → {d['current']} "
                 f"（{d['pct_change_pct']}% > ±{rep['threshold_pct']}%，且无实验记录）")
    for d in rep["drifted_justified"]:
        L.append(f"  [just.] {d['key']}: {d['baseline']} → {d['current']} "
                 f"（{d['pct_change_pct']}%，有 {len(d.get('evidence') or [])} 份新实验记录）")
    for n in rep["notes"]:
        L.append(f"  [note] {n}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="670c D3：关键数字漂移监控")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件上级目录；测试用）")
    ap.add_argument("--out", default=None, help=f"报告路径（默认 {DEFAULT_OUT}）")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="相对变化阈值（默认 0.10；>1 视为百分数，如 10 = 10%%）")
    ap.add_argument("--json", action="store_true", help="打印机读 JSON")
    ap.add_argument("--no-write", action="store_true", help="只读：不写报告文件")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve() if a.root else ROOT
    out = Path(a.out) if a.out else None
    th = a.threshold / 100.0 if a.threshold > 1 else a.threshold

    rep = evaluate(root, out, th, write=not a.no_write)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    return 1 if rep["overall"] == DRIFT else 0


if __name__ == "__main__":
    raise SystemExit(main())
