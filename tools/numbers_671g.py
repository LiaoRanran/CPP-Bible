#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""numbers_671g.py — 671g A2：全量实验数字的**单一复算源**（禁止手抄）。

为什么要有它
============
671g A1 发现：同一个指标在不同文件里同时存在"盲测冻结值"与"扩样累计值"
（holdout 87.5%(14/16) vs 81.0%(17/21)；corpus 43.8%(14/32) vs 54.2%(26/48)）。
数字**各自都能从产物复算**，但读者（和论文）很容易拿错口径。本工具把仓库里所有
声称的实验数字**逐个从其事实源现算**，产出一份带分母/口径/CI/env 的机读表：

  * 盲测值（reveal_3 / 665）与累计值（671a reveal_4 / 671a corpus）**并列登记**，
    不互相覆盖——前者支撑外部效度 claim，后者只描述样本构成（新样本非盲，见 honest_note）；
  * 凡能从**逐样本明细**现算的（holdout/corpus），一律从 ``per_sample[]`` 独立重数，
    不信任汇总 JSON 里的 catch/miss 字段（防止"汇总改了明细没改"）；
  * 率的 95% 区间统一走 :mod:`stat_bounds.cp_interval`（Clopper–Pearson）。

用法
====
    python tools/numbers_671g.py                 # 打印摘要
    python tools/numbers_671g.py --json          # 机读
    python tools/numbers_671g.py --check          # 每个可得指标内部自洽才 exit 0
    python tools/numbers_671g.py --out data/671g_verified_numbers.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from stat_bounds import cp_interval  # Clopper–Pearson 单一实现
except Exception:                           # noqa: BLE001  非本仓根时
    cp_interval = None                     # type: ignore[assignment]

SCHEMA = "queyi-verified-numbers/671g"


def _load(root: Path, rel: str) -> Any | None:
    p = root / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _rate(k: int, n: int) -> dict[str, Any]:
    """率 + CP95，分母为 0 ⇒ 拒绝给率（fail-loud，返回 null 而非 0.0）。"""
    if not isinstance(k, int) or not isinstance(n, int) or n <= 0:
        return {"k": k, "n": n, "rate_pct": None, "cp95": None,
                "note": "分母为 0 或非整数 ⇒ 拒绝给率"}
    out: dict[str, Any] = {"k": k, "n": n, "rate_pct": round(k / n * 100, 4)}
    if cp_interval is not None:
        lo, hi = cp_interval(k, n, 0.95)
        out["cp95"] = [round(lo * 100, 4), round(hi * 100, 4)]
    return out


def _tally(rows: list[dict[str, Any]], verdict_key: str = "verdict") -> dict[str, int]:
    """从逐样本行独立重数 catch/miss/unknown/not_error（不信任任何预聚合字段）。"""
    t = {"catch": 0, "miss": 0, "unknown": 0, "not_error": 0}
    for r in rows:
        v = str(r.get(verdict_key, ""))
        t[v] = t.get(v, 0) + 1
    return t


# ─────────────────────────────────────────────────────────────────────────────────────
# 结构类数字
# ─────────────────────────────────────────────────────────────────────────────────────

def metric_ledger(root: Path) -> dict[str, Any]:
    rel = "data/authority/decision_event_v2_ledger.jsonl"
    p = root / rel
    if not p.is_file():
        return {"key": "ledger_events", "available": False, "value": None, "source": rel}
    n = sum(1 for line in p.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip())
    return {"key": "ledger_events", "label": "452 权威账本事件数", "available": True,
            "value": n, "unit": "条", "source": rel,
            "formula": "非空行数", "claimed": 452, "match": n == 452}


_ENGINE_CACHE: dict[str, Any] = {}            # 已按文件路径载入的真引擎（同路径只 exec 一次）


def _load_gate_engine(root: Path):
    """载入真实 tools/gate_engine.py。

    优先按文件路径**强制载入**（唯一模块名，绕开 sys.modules 里被其它批次最小仓夹具
    注入的 namespace 桩——与 drift_watch_671a.load_engine_rules 同口径）；
    非本仓根（tmp 最小仓没有该文件）回退普通 import。

    踩过的坑（2026-10-01 实测）：`module_from_spec` 之后**必须先把模块登记进
    `sys.modules[唯一名]` 再 `exec_module`**。`gate_engine.py` 用 `@dataclass`，
    Python 3.13 的 `dataclasses._is_type()` 建类时会反查
    `sys.modules[cls.__module__].__dict__`；不登记 ⇒ 查到 None ⇒
    `AttributeError: 'NoneType' object has no attribute '__dict__'`（exec 阶段炸，
    表现为 rules_total 恒 unavailable）。登记用的是**唯一名**，canonical 的
    `gate_engine` 键一动不动 ⇒ 既不读别人的桩，也不污染别人的夹具。
    """
    import hashlib
    import importlib.util
    p = root / "tools" / "gate_engine.py"
    if not p.is_file():
        sys.path.insert(0, str(root / "tools"))
        import gate_engine
        return gate_engine
    real = p.resolve()
    cached = _ENGINE_CACHE.get(str(real))
    if cached is not None:
        return cached
    # ① sys.modules 里已是**同一个真文件** ⇒ 直接复用（省一次 exec）
    cur = sys.modules.get("gate_engine")
    cur_file = getattr(cur, "__file__", None)
    if cur is not None and cur_file:
        try:
            same = Path(str(cur_file)).resolve() == real
        except OSError:
            same = False
        if same and hasattr(cur, "RULES"):
            _ENGINE_CACHE[str(real)] = cur
            return cur
    # ② 按文件路径强制载入
    name = "_671g_gate_engine_" + hashlib.sha256(str(real).encode("utf-8")).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(name, real)
    if spec is None or spec.loader is None:
        raise ImportError(f"spec_from_file_location 无法为 {real} 构造可执行 spec")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod                        # ← @dataclass 建类反查用，勿删此步
    try:
        spec.loader.exec_module(mod)
    except BaseException:
        sys.modules.pop(name, None)                # exec 失败不留半成品
        raise
    _ENGINE_CACHE[str(real)] = mod
    return mod


def metric_rules(root: Path) -> dict[str, Any]:
    try:
        engine = _load_gate_engine(root)
        _n = len(engine.RULES)                    # 桩/缺失在此抛 ⇒ unavailable
    except Exception as e:                      # noqa: BLE001
        return {"key": "rules_total", "available": False, "value": None,
                "source": "tools/gate_engine.py", "error": f"{type(e).__name__}: {e}"}
    sev: dict[str, int] = {}
    for r in engine.RULES:
        s = getattr(r, "severity", None)
        sev[s] = sev.get(s, 0) + 1
    return {"key": "rules_total", "label": "判决规则数", "available": True, "value": _n,
            "unit": "条", "source": "tools/gate_engine.py::RULES", "formula": "len(RULES)",
            "severity": sev, "claimed": 67, "match": _n == 67 and sev.get("block") == 44}


def metric_cards(root: Path) -> dict[str, Any]:
    try:
        import counts_659
        snap = counts_659.snapshot()
    except Exception as e:                      # noqa: BLE001
        return {"key": "cards", "available": False, "value": None,
                "source": "tools/counts_659.py", "error": f"{type(e).__name__}: {e}"}
    return {"key": "cards", "label": "卡数（三口径并列）", "available": True,
            "value": snap, "source": "tools/counts_659.py::snapshot",
            "formula": "atoms_real/atoms_draft/evidence_total 现算",
            "claimed": {"atoms_real": 42},
            "match": snap.get("atoms_real") == 42,
            "caliber_note": "论文头部的『42 张实卡』= atoms_real（非 cards_total=123）"}


# ─────────────────────────────────────────────────────────────────────────────────────
# holdout：盲测冻结（reveal_3） vs 累计（671a reveal_4，逐样本独立重数）
# ─────────────────────────────────────────────────────────────────────────────────────

def metric_holdout(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"key": "holdout", "label": "holdout 检出率（双口径并列）",
                              "available": False, "checks": []}
    blind = _load(root, "data/holdout_reveal_3_665.json")
    if isinstance(blind, dict):
        es = blind.get("error_subset") or {}
        c, m = es.get("catch"), es.get("miss")
        if isinstance(c, int) and isinstance(m, int):
            r = _rate(c, c + m)
            out["blind_reveal3"] = {
                **r, "source": "data/holdout_reveal_3_665.json",
                "caliber": "盲测：reveal_3 h1–h30 真错可测分母 catch+miss",
                "claimed_pct": 87.5, "match": abs((r["rate_pct"] or 0) - 87.5) < 0.05}
            out["checks"].append(out["blind_reveal3"]["match"])
            out["available"] = True
    detail = _load(root, "data/holdout/reveal_3_detail_671a.json")
    if isinstance(detail, dict) and isinstance(detail.get("per_sample"), list):
        # 独立重数：只认真错样本（planted=True），unknown 不进分母
        err = [x for x in detail["per_sample"] if x.get("planted") is True]
        t = _tally(err)
        r = _rate(t["catch"], t["catch"] + t["miss"])
        # 对照样本（planted=False）被 catch ⇒ 误报
        ctrl = [x for x in detail["per_sample"] if x.get("planted") is False]
        fp = sum(1 for x in ctrl if x.get("verdict") == "catch")
        out["cumulative_671a"] = {
            **r, "tally": t, "control_total": len(ctrl), "false_positive": fp,
            "source": "data/holdout/reveal_3_detail_671a.json::per_sample",
            "caliber": "累计：盲 h1–h30 + 非盲 h31–h40；真错可测分母；逐样本独立重数",
            "blind": False,
            "honest_note": "h31–h40 为 reveal 后并入，非盲 ⇒ 不得据此 claim 外部效度提升",
            "claimed_pct": 81.0, "match": abs((r["rate_pct"] or 0) - 81.0) < 0.05
                              and r["k"] == 17 and r["n"] == 21}
        out["checks"].append(out["cumulative_671a"]["match"])
    return out


# ─────────────────────────────────────────────────────────────────────────────────────
# corpus：盲测冻结（665） vs 累计（671a，逐样本独立重数，分层）
# ─────────────────────────────────────────────────────────────────────────────────────

def metric_corpus(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"key": "corpus", "label": "外部 corpus 检出率（双口径+分层）",
                              "available": False, "checks": []}
    blind = _load(root, "data/external_corpus_reveal_665.json")
    if isinstance(blind, dict):
        c, m, u, ne = (blind.get(k) for k in ("catch", "miss", "unknown", "not_error"))
        if isinstance(c, int) and isinstance(m, int):
            meas = _rate(c, c + m)
            alln = c + m + (u or 0) + (ne or 0)
            out["blind_665"] = {
                "measurable": {**meas, "source": "data/external_corpus_reveal_665.json"},
                "all_samples": _rate(c, alln),
                "caliber": "盲测 665 reveal：可测 catch+miss=32；全样本 40",
                "claimed_pct": 43.8,
                "match": abs((meas["rate_pct"] or 0) - 43.8) < 0.05 and meas["k"] == 14
                              and meas["n"] == 32}
            out["checks"].append(out["blind_665"]["match"])
            out["available"] = True
    detail = _load(root, "data/external_corpus/reveal_detail_671a.json")
    if isinstance(detail, dict) and isinstance(detail.get("per_sample"), list):
        rows = detail["per_sample"]
        t = _tally(rows)
        denom = t["catch"] + t["miss"]
        r = _rate(t["catch"], denom)
        layers: dict[str, Any] = {}
        for x in rows:
            lay = str(x.get("layer"))
            layers.setdefault(lay, {"catch": 0, "miss": 0, "unknown": 0, "not_error": 0})
            v = str(x.get("verdict"))
            if v in layers[lay]:
                layers[lay][v] += 1
        layer_rates = {lay: _rate(d["catch"], d["catch"] + d["miss"])
                        for lay, d in sorted(layers.items())}
        out["cumulative_671a"] = {
            **r, "tally": t, "layers": layer_rates,
            "source": "data/external_corpus/reveal_detail_671a.json::per_sample",
            "caliber": "累计 60 条：盲 d3-01–40 + 非盲 d3e-01–20；逐样本独立重数",
            "blind": False,
            "caliber_change": "新样本 -O0/-O2 双档 + setarch -R（665 为单档 -O1 未关 ASLR）⇒ 不可直接比大小",
            "claimed_pct": 54.2,
            "match": abs((r["rate_pct"] or 0) - 54.2) < 0.05 and r["k"] == 26 and r["n"] == 48
                              and layer_rates["sanitizer"]["k"] == 19
                              and layer_rates["compiler-warn"]["k"] == 6
                              and layer_rates["cross-compile"]["k"] == 1}
        out["checks"].append(out["cumulative_671a"]["match"])
    return out


# ─────────────────────────────────────────────────────────────────────────────────────
# 变异 / 反事实 / 重注入
# ─────────────────────────────────────────────────────────────────────────────────────

def metric_mutation(root: Path) -> dict[str, Any]:
    out = {"key": "mutation", "label": "变异击杀率（core / all）", "available": False, "checks": []}
    for name, rel, claim in (("core", "data/656_mutation_report_core.json", 97.3),
                                ("all", "data/656_mutation_report_all.json", 81.5)):
        d = _load(root, rel)
        if not isinstance(d, dict):
            continue
        k, s = d.get("killed"), d.get("survived")
        if isinstance(k, int) and isinstance(s, int):
            r = _rate(k, k + s)
            r.update(source=rel, internal_metric=True, claimed_pct=claim,
                    match=abs((r["rate_pct"] or 0) - claim) < 0.05)
            out[name] = r
            out["checks"].append(r["match"])
            out["available"] = True
    return out


def _f1(tp: int, fp: int, fn: int) -> dict[str, float]:
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"precision": round(prec, 6), "recall": round(rec, 6), "f1": round(f1, 6)}


def metric_counterfactual(root: Path) -> dict[str, Any]:
    out = {"key": "counterfactual", "label": "反事实算子 P/R/F1（两套不重叠样本）",
           "available": False, "checks": []}
    for name, rel in (("cf_665_10", "data/counterfactual_cases_665.json"),
                        ("cf_669d_20", "data/counterfactual_cases_669d.json")):
        d = _load(root, rel)
        if not isinstance(d, dict):
            continue
        cm = d.get("confusion") or {}
        tp, fp, fn = cm.get("tp"), cm.get("fp"), cm.get("fn")
        if isinstance(tp, int) and isinstance(fp, int) and isinstance(fn, int):
            scores = _f1(tp, fp, fn)
            scores.update(source=rel, confusion=cm, match=scores["f1"] == 1.0)
            out[name] = scores
            out["checks"].append(scores["match"])
            out["available"] = True
    return out


def metric_defect_injection(root: Path) -> dict[str, Any]:
    rel = "data/defect_injection_661.json"
    d = _load(root, rel)
    if not isinstance(d, dict):
        return {"key": "defect_reinject", "available": False, "source": rel}
    ca, n = d.get("reinject_caught"), d.get("reinjectable")
    if not isinstance(ca, int) or not isinstance(n, int):
        return {"key": "defect_reinject", "available": False, "source": rel}
    r = _rate(ca, n)
    r.update(source=rel, total_defects=d.get("total_defects"), not_reinjectable=d.get("not_reinjectable"),
             static_judgment=True, claimed_pct=100.0, match=ca == 6 and n == 6)
    return {"key": "defect_reinject", "label": "缺陷重注入检出", "available": True, **r}


# ─────────────────────────────────────────────────────────────────────────────────────

COLLECTORS = (metric_ledger, metric_rules, metric_cards, metric_holdout, metric_corpus,
               metric_mutation, metric_counterfactual, metric_defect_injection)


def per_sample_export(root: Path = ROOT, env: dict[str, Any] | None = None) -> dict[str, Any]:
    """671g A3：把四个数据集的**逐样本/逐变异明细**汇成一份带 env 的留痕（只读抽取，不重跑）。

    各类只搬运事实源已有的逐行字段，不重新判决：
      * holdout / corpus：671a reveal 明细（3 轮 verdict）；
      * counterfactual：每案的真值标注、算子预测、是否一致 + 汇总混淆矩阵；
      * mutation：每个变异体的 target/op/status（killed/survived/其他）。
    """
    out: dict[str, Any] = {
        "schema": "queyi-per-sample-audit/671g",
        "generated_by": "tools/numbers_671g.py::per_sample_export",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "caliber": "真错分母=catch+miss；unknown/not_error 不进分母；率的口径见各数据集说明",
        "env": env or {},
        "datasets": {},
    }
    hd = _load(root, "data/holdout/reveal_3_detail_671a.json")
    if isinstance(hd, dict):
        out["datasets"]["holdout"] = {
            "n": len(hd.get("per_sample", [])),
            "rows": [{k: r.get(k) for k in ("id", "detector", "verdict", "planted",
                                                "source", "reproducible")}
                      for r in hd.get("per_sample", [])],
            "source": "data/holdout/reveal_3_detail_671a.json",
            "note": "h1–h30 盲测复用 reveal_3；h31–h40 非盲（669d 扩样）",
        }
    cd = _load(root, "data/external_corpus/reveal_detail_671a.json")
    if isinstance(cd, dict):
        out["datasets"]["corpus"] = {
            "n": len(cd.get("per_sample", [])),
            "rows": [{k: r.get(k) for k in ("id", "layer", "detector", "verdict",
                                                "source", "reproducible")}
                      for r in cd.get("per_sample", [])],
            "source": "data/external_corpus/reveal_detail_671a.json",
            "note": "d3-01–40 盲测（665，单档 -O1）；d3e-* 非盲（双档 setarch -R，口径变更）",
        }
    cf_rows: list[dict[str, Any]] = []
    for rel in ("data/counterfactual_cases_665.json",
                 "data/counterfactual_cases_669d.json"):
        d = _load(root, rel)
        if not isinstance(d, dict):
            continue
        for c in d.get("cases", []):
            cf_rows.append({"id": c.get("id"), "ground_truth": c.get("ground_truth"),
                          "operator_prediction": c.get("operator_prediction"),
                          "agree": c.get("agree"), "source": rel})
        out["datasets"][Path(rel).stem] = {
            "confusion": d.get("confusion"), "scores": d.get("scores"),
            "denominator": d.get("denominator"), "source": rel}
    if cf_rows:
        out["datasets"]["counterfactual_cases"] = {"n": len(cf_rows), "rows": cf_rows}
    mut_rows: list[dict[str, Any]] = []
    for arm, rel in (("core", "data/656_mutation_report_core.json"),
                        ("all", "data/656_mutation_report_all.json")):
        d = _load(root, rel)
        if not isinstance(d, dict):
            continue
        rows = [{"arm": arm, "target": r.get("target"), "op": r.get("op"),
                  "status": r.get("status")} for r in d.get("results", [])]
        mut_rows.extend(rows)
        out["datasets"][f"mutation_{arm}"] = {
            "n": len(d.get("results", [])), "killed": d.get("killed"),
            "survived": d.get("survived"), "seed": d.get("seed"),
            "generated_at": d.get("generated_at"), "source": rel}
    if mut_rows:
        out["datasets"]["mutation_cases"] = {"n": len(mut_rows), "rows": mut_rows}
    return out


def collect(root: Path = ROOT) -> dict[str, Any]:
    metrics = [fn(root) for fn in COLLECTORS]
    problems = []
    for m in metrics:
        for chk in (m.get("checks") or []):
            if chk is False:
                problems.append(m["key"])
    return {
        "schema": SCHEMA,
        "generated_by": "tools/numbers_671g.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": str(root),
        "metrics": {m["key"]: m for m in metrics},
        "order": [m["key"] for m in metrics],
        "self_inconsistent": sorted(set(problems)),
        "caliber_principle": "盲测冻结值与扩样累计值并列；引用外部效度只能用盲测值；新样本非盲",
    }


def render(rep: dict[str, Any]) -> str:
    L = [f"[671g verified numbers]  自洽指标={len(rep['order']) - len(rep['self_inconsistent'])}"
         f"/{len(rep['order'])}  不自洽={rep['self_inconsistent']}"]
    for k in rep["order"]:
        m = rep["metrics"][k]
        if not m.get("available"):
            L.append(f"  N/A {k:16}（产物缺失）")
            continue
        if k == "holdout":
            b, c = m.get("blind_reveal3"), m.get("cumulative_671a")
            if b:
                L.append(f"  OK holdout 盲测  {b['rate_pct']}%（{b['k']}/{b['n']}）CP95 {b.get('cp95')}")
            if c:
                L.append(f"  OK holdout 累计  {c['rate_pct']}%（{c['k']}/{c['n']}）CP95 {c.get('cp95')} [非盲]")
        elif k == "corpus":
            b, c = m.get("blind_665"), m.get("cumulative_671a")
            if b:
                mm = b["measurable"]
                L.append(f"  OK corpus 盲测可测 {mm['rate_pct']}%（{mm['k']}/{mm['n']}）全样本 {b['all_samples']['rate_pct']}%")
            if c:
                L.append(f"  OK corpus 累计  {c['rate_pct']}%（{c['k']}/{c['n']}）[非盲+口径变更]")
        elif k == "mutation":
            for arm in ("core", "all"):
                if arm in m:
                    L.append(f"  OK mutation.{arm:4} {m[arm]['rate_pct']}%（{m[arm]['k']}/{m[arm]['n']}）[内部指标]")
        elif k == "counterfactual":
            for arm in ("cf_665_10", "cf_669d_20"):
                if arm in m:
                    a = m[arm]
                    L.append(f"  OK {arm:11} F1={a['f1']} P={a['precision']} R={a['recall']}")
                    L.append(f"               {a['confusion']}")
        else:
            L.append(f"  OK {k:16} {m.get('value') if 'value' in m else m.get('rate_pct')}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g A2：全量实验数字单一复算源")
    ap.add_argument("--root", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--per-sample-out", default=None,
                    help="把 A3 逐样本/逐变异汇总（带 env）写到指定 JSON")
    ap.add_argument("--check", action="store_true", help="所有可得指标内部自洽才 exit 0")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    rep = collect(root)
    if a.out:
        Path(a.out).write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    if a.per_sample_out:
        try:
            import env_probe_671g as Env
            env = Env.probe()
        except Exception:                      # noqa: BLE001  环境探测失败不阻塞明细落盘
            env = {"probe_error": "env_probe_671g 不可用 ⇒ 该明细标 UNVERIFIED"}
        det = per_sample_export(root, env=env)
        Path(a.per_sample_out).write_text(
            json.dumps(det, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 1 if rep["self_inconsistent"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
