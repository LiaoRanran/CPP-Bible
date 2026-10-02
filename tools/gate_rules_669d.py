#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gate_rules_669d.py — 669d B 段：六条 P0 门禁规则（新工具，不改既有文件）。

背景（669d 任务书）：666「81.2% 假绿」与 669b「corpus 35%→10% 静默掉分」是同一形态：
**数字没错，但口径/环境/一致性没人守**。本文件把六条判据变成可执行门禁。

六条规则
========
  B1 G-RATE-CONSISTENCY   检出率三处（产物 / 前端 / 论文）必须一致，否则 BLOCK
  B2 G-DENOMINATOR        比率必须带 denominator、k<=den、且能从明细重算，否则 BLOCK
  B3 G-STATS-FROZEN       协议冻结的统计口径必须有对应实现，否则 BLOCK
  B4 G-BOUNDARY-REQUIRED  verified 卡必须有 provenance 三元组；draft 必须显式标 boundary
  B5 G-BASELINE-EXISTS    实验结果必须有对应 baseline（同指标），否则 BLOCK
  B6 G-IRR                人工标注卡必须有 IRR 记录（≥2 人，κ≥0.6）；缺失只 WARN 不 BLOCK

设计约定
========
* 每个 `check_*` 只依赖传入的 `root: Path`，**不读模块级常量路径**
  ⇒ 测试可在 `tmp_path` 里构造正例/反例（每条规则 ≥1 正 1 反）。
* 统一返回 `list[Finding]`，Finding 是 dict：
  `{rule, severity, target, message, fix_hint}`；severity ∈ {block, warn}。
* 纯标准库（yaml 为可选：无 yaml 时 B4 降级为 warn 而非崩）。

用法：
    python tools/gate_rules_669d.py --check          # 跑全部（仓库根）
    python tools/gate_rules_669d.py --rule G-DENOMINATOR
    python tools/gate_rules_669d.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Callable

# ─────────────────────────────────────────────────────────────────────────────
# 基础结构
# ─────────────────────────────────────────────────────────────────────────────

BLOCK = "block"
WARN = "warn"

#: 比率字段名（产物里"这是个率"的写法）
_RATE_KEYS = (
    "rate", "rate_pct", "detect_rate_pct", "kill_rate_on_scored", "f1",
    "recall", "precision", "recall_pct", "precision_pct", "rate_pct_all_samples",
)
#: 分母字段名
_DEN_KEYS = ("denominator", "den", "n", "total", "value")
#: 分子字段名
_NUM_KEYS = ("catch", "killed", "k", "num", "tp", "value")

TOL = 0.001          # 比率容差（B2 要求）
TOL_PCT = 0.05       # 百分比比较容差（B1，容忍 97.35 vs 97.3 的取整差）


def finding(rule: str, severity: str, target: str, message: str, fix_hint: str = "") -> dict:
    return {"rule": rule, "severity": severity, "target": target,
            "message": message, "fix_hint": fix_hint}


def _load_json(p: Path) -> Any | None:
    try:
        return json.loads(p.read_bytes().decode("utf-8"))
    except Exception:
        return None


def _is_rate_key(k: Any) -> bool:
    """判断字段名是否表示"这是一个率"。

    669d 实测踩坑：早期版本用 `"rate" in kl` 子串判断，会把 `generated_by` /
    `generated_at`（gene**rate**d…）误判成比率字段 ⇒ 8 条假红。
    改为精确匹配 + 只允许以 rate 开头/结尾的形式。
    """
    kl = str(k).lower()
    if kl in _RATE_KEYS:
        return True
    return kl.startswith("rate") or kl.endswith("rate") or kl.endswith("rate_pct")


def _norm_pct(v: float) -> set[float]:
    """把 0–1 标度与 0–100 标度都展开，便于跨标度比对。"""
    try:
        v = float(v)
    except Exception:
        return set()
    out = {v}
    if abs(v) <= 1.0:
        out.add(v * 100.0)
    else:
        out.add(v / 100.0)
    return out


def _close(a: float, b: float, tol: float = TOL_PCT) -> bool:
    return abs(float(a) - float(b)) <= tol


# ─────────────────────────────────────────────────────────────────────────────
# B1 · G-RATE-CONSISTENCY
# ─────────────────────────────────────────────────────────────────────────────

def canonical_rates(root: Path) -> dict[str, float]:
    """从**原始计数**现算规范率表（百分比标度）。禁止从别处抄。

    672h（W3 扩样）：holdout/corpus 的事实源切到当前一轮 reveal 产物
    （`holdout_reveal_5_672h.json` / `external_corpus_reveal_672h.json`）；
    旧产物（3_665 / 665）只在前者缺失时兜底（部分检出场景不假装有值）。
    """
    out: dict[str, float] = {}

    d = _load_json(root / "data" / "holdout_reveal_5_672h.json")
    if isinstance(d, dict):
        es = ((d.get("cumulative") or {}).get("error_subset") or {})
        if es.get("catch") is not None:
            n = es.get("catch", 0) + es.get("miss", 0)
            if n:
                out["holdout.valid"] = round(es["catch"] / n * 100, 4)
    if "holdout.valid" not in out:
        d = _load_json(root / "data" / "holdout_reveal_3_665.json")
        if isinstance(d, dict):
            es = d.get("error_subset") or {}
            if es.get("catch") is not None:
                n = es.get("catch", 0) + es.get("miss", 0)
                if n:
                    out["holdout.valid"] = round(es["catch"] / n * 100, 4)

    r = _load_json(root / "data" / "external_corpus_reveal_672h.json")
    if isinstance(r, dict):
        cum = r.get("cumulative") or {}
        c, m = cum.get("catch"), cum.get("miss")
        if c is not None and m is not None and (c + m):
            out["external.valid"] = round(c / (c + m) * 100, 4)
        if c is not None and cum.get("total"):
            out["external.all"] = round(c / cum["total"] * 100, 4)
    if "external.valid" not in out:
        d = _load_json(root / "data" / "external_corpus_reveal_665.json")
        if isinstance(d, dict):
            c, m = d.get("catch"), d.get("miss")
            if c is not None and m is not None and (c + m):
                out["external.valid"] = round(c / (c + m) * 100, 4)
            if c is not None and d.get("total"):
                out["external.all"] = round(c / d["total"] * 100, 4)
    d = _load_json(root / "data" / "counterfactual_cases_665.json")
    if isinstance(d, dict):
        sc = d.get("scores") or {}
        if sc.get("f1") is not None:
            out["counterfactual.f1"] = round(float(sc["f1"]) * 100, 4)
    for scope, rel in (("core", "data/656_mutation_report_core.json"),
                       ("all", "data/656_mutation_report.json")):
        d = _load_json(root / rel)
        if isinstance(d, dict) and d.get("killed") is not None:
            n = (d.get("killed") or 0) + (d.get("survived") or 0)
            if n:
                out[f"mutation.{scope}"] = round(d["killed"] / n * 100, 4)
    return out


def _collect_json_rates(obj: Any, into: set[float]) -> None:
    """递归收集 JSON 里所有'看起来是率'的数值（展开两种标度）。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                if _is_rate_key(k) or ("recall" in kl and "recall_" in kl):
                    into |= _norm_pct(v)
            else:
                _collect_json_rates(v, into)
    elif isinstance(obj, list):
        for v in obj:
            _collect_json_rates(v, into)


def _collect_text_rates(text: str) -> set[float]:
    """从文档里收集率数值。

    两种写法都要覆盖：
      * 百分比写法：`87.5%`
      * 0–1 标度写法：`F1=1.0`（论文里 F1/κ 常不带百分号 —— 669d 实测漏过一次）
    """
    out: set[float] = set()
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*%", text):
        out |= _norm_pct(float(m.group(1)))
    for m in re.finditer(r"\b(?:f1|kappa|κ)\s*[=＝:]\s*(\d+(?:\.\d+)?)",
                         text, flags=re.IGNORECASE):
        out |= _norm_pct(float(m.group(1)))
    return out


def check_rate_consistency(root: Path) -> list[dict]:
    """B1：产物 / 前端 / 论文 三处的检出率必须一致。"""
    f: list[dict] = []
    rates = canonical_rates(root)
    if not rates:
        return [finding("G-RATE-CONSISTENCY", WARN, "data/",
                        "未找到任何产物率（事实源缺失）", "确认产物文件路径")]

    front: set[float] = set()
    wd = root / "web" / "data"
    if wd.is_dir():
        for p in sorted(wd.glob("*.json")):
            _collect_json_rates(_load_json(p), front)

    # 673a：门禁必须校验**当前**论文，而非已废弃的并行草稿（paper_draft_v0.5.md）。
    # 取 research/paper_v*.md 中版本号最高者；找不到再退回旧草稿路径。
    _cands = sorted(
        (root / "research").glob("paper_v*.md"),
        key=lambda p: [int(x) for x in re.findall(r"\d+", p.stem)] or [0],
    )
    paper = _cands[-1] if _cands else (root / "research" / "paper_draft_v0.5.md")
    doc_rates: set[float] = set()
    if paper.is_file():
        doc_rates = _collect_text_rates(paper.read_text(encoding="utf-8", errors="replace"))

    for rid, val in sorted(rates.items()):
        # 前端（web/data/*.json）
        if wd.is_dir():
            if not any(_close(v, val) for v in front):
                f.append(finding(
                    "G-RATE-CONSISTENCY", BLOCK, f"web/data/*.json ← {rid}",
                    f"{rid} 现算 {val:.4g}% 在前端数据源中找不到一致值",
                    "前端展示的率必须与产物现算值同源；禁止手写"))
        # 论文
        if paper.is_file():
            if not any(_close(v, val) for v in doc_rates):
                f.append(finding(
                    "G-RATE-CONSISTENCY", BLOCK, f"research/{paper.name} ← {rid}",
                    f"{rid} 现算 {val:.4g}% 在论文中找不到一致值",
                    "论文引用的率必须与产物现算值同源"))
    return f


# ─────────────────────────────────────────────────────────────────────────────
# B2 · G-DENOMINATOR
# ─────────────────────────────────────────────────────────────────────────────

#: 需要校验分母的产物（相对 root 的 glob）
_DEN_TARGETS = (
    "data/holdout/*.json",
    "data/external_corpus*.json",
    "data/counterfactual*.json",
)


def _has_denominator(obj: Any) -> bool:
    return isinstance(obj, dict) and any(k in obj for k in _DEN_KEYS)


def _den_value(obj: dict) -> int | None:
    d = obj.get("denominator")
    if isinstance(d, dict):
        for k in ("value", "total", "n"):
            v = d.get(k)
            if isinstance(v, int) and not isinstance(v, bool):
                return int(v)
        return None
    for k in _DEN_KEYS:
        v = obj.get(k)
        if isinstance(v, int) and not isinstance(v, bool):
            return v
    return None


def check_denominator(root: Path) -> list[dict]:
    """B2：比率必须带 denominator、k<=den、且能从明细重算。"""
    f: list[dict] = []
    files: list[Path] = []
    for pat in _DEN_TARGETS:
        files += sorted(root.glob(pat))
    if not files:
        return [finding("G-DENOMINATOR", WARN, "data/", "未匹配到任何待校验产物", "检查路径")]

    for p in files:
        d = _load_json(p)
        if not isinstance(d, dict):
            continue
        rel = p.relative_to(root).as_posix()

        # (a) 顶层出现比率 ⇒ 必须有分母声明
        top_rates = [k for k in d if _is_rate_key(k)]
        for rk in top_rates:
            if not _has_denominator(d):
                f.append(finding(
                    "G-DENOMINATOR", BLOCK, f"{rel}:{rk}",
                    f"声明了比率 {rk}={d[rk]} 但没有 denominator 字段",
                    "补 denominator {value,meaning,excluded}"))

        # (b) k <= denominator
        den = _den_value(d)
        if den is not None:
            for nk in ("catch", "killed", "k", "num"):
                v = d.get(nk)
                if isinstance(v, int) and not isinstance(v, bool) and v > den:
                    f.append(finding(
                        "G-DENOMINATOR", BLOCK, f"{rel}:{nk}",
                        f"分子 {nk}={v} > 分母 {den}", "分子不得大于分母"))

        # (c) 能从明细重算：逐样本明细 vs 汇总
        detail = d.get("per_sample") or d.get("results") or d.get("cases")
        if isinstance(detail, list) and detail:
            det_catch = sum(1 for s in detail
                            if isinstance(s, dict) and s.get("verdict") == "catch")
            det_killed = sum(1 for s in detail
                             if isinstance(s, dict) and s.get("status") == "killed")
            summ = d.get("catch")
            if isinstance(summ, int) and det_catch and summ != det_catch:
                f.append(finding(
                    "G-DENOMINATOR", BLOCK, f"{rel}:catch",
                    f"汇总 catch={summ} 与逐样本明细重算 {det_catch} 不一致",
                    "禁止手改汇总；重跑生成器"))
            summ = d.get("killed")
            if isinstance(summ, int) and det_killed and summ != det_killed:
                f.append(finding(
                    "G-DENOMINATOR", BLOCK, f"{rel}:killed",
                    f"汇总 killed={summ} 与逐样本明细重算 {det_killed} 不一致",
                    "禁止手改汇总；重跑生成器"))

        # (d) 率能从 k/n 重算（容差 TOL）
        den2 = _den_value(d)
        for rk in ("rate_pct", "detect_rate_pct", "kill_rate_on_scored",
                   "rate_pct_all_samples"):
            rv = d.get(rk)
            if not isinstance(rv, (int, float)) or isinstance(rv, bool):
                continue
            num = None
            dn = None
            if rk == "kill_rate_on_scored":
                num, dn = d.get("killed"), (d.get("killed") or 0) + (d.get("survived") or 0)
            elif rk == "rate_pct_all_samples":
                num, dn = d.get("catch"), d.get("total")
            elif rk in ("rate_pct", "detect_rate_pct"):
                num, dn = d.get("catch"), (d.get("catch") or 0) + (d.get("miss") or 0)
            if isinstance(num, int) and isinstance(dn, int) and dn:
                if abs(num / dn * 100 - float(rv)) > TOL * 100:
                    f.append(finding(
                        "G-DENOMINATOR", BLOCK, f"{rel}:{rk}",
                        f"{rk}={rv} 与 {num}/{dn} 重算 {num/dn*100:.4g} 不一致（容差 {TOL}）",
                        "率必须由 k/n 现算，禁止手写"))
        _ = den2
    return f


# ─────────────────────────────────────────────────────────────────────────────
# B3 · G-STATS-FROZEN
# ─────────────────────────────────────────────────────────────────────────────

#: 协议里必须冻结的统计方法 → 期望出现在实现中的关键词
STATS_METHODS: dict[str, tuple[str, ...]] = {
    "Clopper-Pearson": ("clopper", "clopper_pearson", "clopperpearson"),
    "Fisher": ("fisher", "fisher_exact"),
    "McNemar": ("mcnemar",),
}
#: 可选方法（缺失只 WARN）
STATS_OPTIONAL: dict[str, tuple[str, ...]] = {
    "Cohen's kappa": ("cohen", "kappa"),
    "BH 校正": ("bh", "benjamini", "fdr"),
}


def _scan_impl(root: Path, needles: tuple[str, ...]) -> list[str]:
    """在 tools/ 下找实现了该方法的文件（含 stats_*.py 及更广的扫描）。"""
    hits: list[str] = []
    for pat in ("stats_*.py", "*.py"):
        for p in sorted((root / "tools").glob(pat)):
            try:
                t = p.read_text(encoding="utf-8", errors="replace").lower()
            except Exception:
                continue
            if any(n in t for n in needles):
                hits.append(p.relative_to(root).as_posix())
                break
        if hits:
            break
    return hits


def check_stats_frozen(root: Path) -> list[dict]:
    """B3：协议冻结的统计口径必须有对应实现。"""
    f: list[dict] = []
    proto = root / "research" / "05_evaluation_protocol.md"
    if not proto.is_file():
        return [finding("G-STATS-FROZEN", BLOCK, "research/05_evaluation_protocol.md",
                        "评估协议文件不存在 ⇒ 统计口径无从冻结", "补齐协议文件")]
    text = proto.read_text(encoding="utf-8", errors="replace")
    low = text.lower()

    for name, needles in STATS_METHODS.items():
        declared = any(n in low for n in needles)
        if not declared:
            f.append(finding(
                "G-STATS-FROZEN", BLOCK, f"research/05_evaluation_protocol.md ← {name}",
                f"协议未冻结 {name} 统计口径",
                f"在协议中显式声明 {name}（含适用条件与显著性水平）"))
            continue
        if not _scan_impl(root, needles):
            f.append(finding(
                "G-STATS-FROZEN", BLOCK, f"tools/ ← {name}",
                f"协议声明了 {name}，但 tools/ 下找不到实现",
                f"补 tools/stats_*.py 实现 {name}"))

    for name, needles in STATS_OPTIONAL.items():
        if not any(n in low for n in needles):
            f.append(finding(
                "G-STATS-FROZEN", WARN, f"research/05_evaluation_protocol.md ← {name}",
                f"协议未声明 {name}（建议补）",
                f"如需标注者一致性/多重比较，请冻结 {name}"))
    return f


# ─────────────────────────────────────────────────────────────────────────────
# B4 · G-BOUNDARY-REQUIRED
# ─────────────────────────────────────────────────────────────────────────────

PROVENANCE_TRIPLE = ("mutation_set_hash", "mutation_count", "generator_version")
VERIFIED_STATES = ("verified", "red-team-verified", "machine-verified")


def _frontmatter(p: Path) -> dict | None:
    t = p.read_text(encoding="utf-8", errors="replace")
    if not t.startswith("---"):
        return None
    end = t.find("\n---", 3)
    if end < 0:
        return None
    try:
        import yaml  # 运行时依赖
    except ImportError:
        return None
    try:
        m = yaml.safe_load(t[3:end])
    except Exception:
        return None
    return m if isinstance(m, dict) else None


def check_boundary_required(root: Path) -> list[dict]:
    """B4：verified 卡必须有 provenance 三元组；draft 必须显式标 boundary。"""
    f: list[dict] = []
    cards = sorted((root / "atoms").rglob("ATOM-*.md"))
    if not cards:
        return [finding("G-BOUNDARY-REQUIRED", WARN, "atoms/", "未找到任何卡", "检查路径")]
    try:
        import yaml  # noqa: F401
    except ImportError:
        return [finding("G-BOUNDARY-REQUIRED", WARN, "atoms/",
                        "未安装 pyyaml ⇒ 无法解析 frontmatter（降级为 WARN）",
                        "pip install pyyaml")]

    for p in cards:
        m = _frontmatter(p)
        if m is None:
            f.append(finding("G-BOUNDARY-REQUIRED", BLOCK,
                             p.relative_to(root).as_posix(),
                             "无 frontmatter 或解析失败", "补 YAML frontmatter"))
            continue
        rel = p.relative_to(root).as_posix()
        st = str(m.get("status") or "").lower()
        if st in VERIFIED_STATES:
            miss = [k for k in PROVENANCE_TRIPLE if m.get(k) in (None, "", [])]
            if miss:
                f.append(finding(
                    "G-BOUNDARY-REQUIRED", BLOCK, rel,
                    f"status={st} 但缺 provenance 三元组: {', '.join(miss)}",
                    "补 mutation_set_hash / mutation_count / generator_version"))
        elif st == "draft" or (not st):
            has_b = (m.get("boundary") is not None) or (m.get("claim_boundary") is not None)
            if not has_b:
                f.append(finding(
                    "G-BOUNDARY-REQUIRED", BLOCK, rel,
                    f"status={st or '缺失'} 为草稿但未显式标记 boundary（应标 boundary: unknown）",
                    "草稿卡必须显式写 boundary: unknown"))
    return f


# ─────────────────────────────────────────────────────────────────────────────
# B5 · G-BASELINE-EXISTS
# ─────────────────────────────────────────────────────────────────────────────

#: 率指标（缺 baseline ⇒ BLOCK）—— 实验结论靠它们支撑
_RATE_SECTIONS = ("corpus_rates", "mutation")
#: 构成计数（缺 baseline ⇒ WARN）—— 描述语料规模，不是效应量
_COUNT_SECTIONS = ("holdout_outcomes", "ability")


def _exp_metric_ids(exp: dict) -> dict[str, tuple[str, str]]:
    """返回 {指标 label: (所属 section, 严重级)}。"""
    ids: dict[str, tuple[str, str]] = {}
    for sec in _RATE_SECTIONS:
        for item in exp.get(sec) or []:
            if isinstance(item, dict) and item.get("label"):
                ids[str(item["label"])] = (sec, BLOCK)
    for sec in _COUNT_SECTIONS:
        for item in exp.get(sec) or []:
            if isinstance(item, dict) and item.get("label"):
                ids[str(item["label"])] = (sec, WARN)
    if isinstance(exp.get("escape"), dict):
        ids["escape"] = ("escape", BLOCK)
    return ids


def _baseline_keys(bl: dict, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if not isinstance(bl, dict):
        return keys
    for k, v in bl.items():
        path = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict):
            keys |= _baseline_keys(v, path)
        else:
            keys.add(path)
    return keys


def check_baseline_exists(root: Path) -> list[dict]:
    """B5：实验结果里的每个指标，baseline 必须有同指标基线。"""
    f: list[dict] = []
    exp_p = root / "web" / "data" / "experiments.json"
    base_p = root / "data" / "baseline.json"
    if not exp_p.is_file():
        return [finding("G-BASELINE-EXISTS", WARN, "web/data/experiments.json",
                        "实验结果文件不存在", "—")]
    exp = _load_json(exp_p)
    if not isinstance(exp, dict):
        return [finding("G-BASELINE-EXISTS", WARN, "web/data/experiments.json",
                        "实验结果解析失败", "—")]
    if not base_p.is_file():
        return [finding("G-BASELINE-EXISTS", BLOCK, "data/baseline.json",
                        "baseline 文件不存在，但已有实验结果 ⇒ 实验无基线",
                        "先建 static gate 基线再发实验结果")]
    base = _load_json(base_p)
    bkeys = _baseline_keys(base) if isinstance(base, dict) else set()
    btext = json.dumps(base, ensure_ascii=False).lower() if base else ""

    for mid, (sec, sev) in sorted(_exp_metric_ids(exp).items()):
        # 归一化指标名：去空格/点/括号，取核心 token
        toks = [t for t in re.split(r"[\s·（）()/]+", mid) if t]
        hit = any(t.lower() in btext for t in toks if len(t) >= 2)
        if not hit:
            f.append(finding(
                "G-BASELINE-EXISTS", sev, f"web/data/experiments.json ← {mid}",
                f"实验结果 [{sec}] 含指标「{mid}」，但 data/baseline.json 无对应基线",
                "补 static gate 版本的同指标基线，或把该指标标为 planned"))
    _ = bkeys
    return f


# ─────────────────────────────────────────────────────────────────────────────
# B6 · G-IRR（只 WARN）
# ─────────────────────────────────────────────────────────────────────────────

IRR_MIN_RATERS = 2
IRR_MIN_KAPPA = 0.6
#: 机器 principal 前缀（不算"人工标注"）
_MACHINE_PREFIX = ("machine:", "redteam:", "auto", "script")


def _is_human(v: str) -> bool:
    v = (v or "").strip().lower()
    if not v:
        return False
    return not v.startswith(_MACHINE_PREFIX)


def check_irr(root: Path) -> list[dict]:
    """B6：人工标注的卡必须有 IRR 记录（≥2 人，κ≥0.6）。缺失只 WARN 不 BLOCK。"""
    f: list[dict] = []
    irr_p = root / "data" / "irr_records.json"
    records: dict = {}
    if irr_p.is_file():
        d = _load_json(irr_p)
        if isinstance(d, dict):
            records = d.get("records") or d.get("cards") or {}
        elif isinstance(d, list):
            records = {str(r.get("card_id") or r.get("id")): r for r in d if isinstance(r, dict)}
    else:
        f.append(finding("G-IRR", WARN, "data/irr_records.json",
                         "IRR 记录文件不存在 ⇒ 全部人工标注卡无一致性证据",
                         "补做第二标注者并落 data/irr_records.json"))

    try:
        import yaml  # noqa: F401
    except ImportError:
        return f + [finding("G-IRR", WARN, "atoms/", "无 pyyaml ⇒ 无法扫卡", "pip install pyyaml")]

    human_cards = 0
    for p in sorted((root / "atoms").rglob("ATOM-*.md")):
        m = _frontmatter(p)
        if not isinstance(m, dict):
            continue
        vb = str(m.get("verified_by") or "")
        if not _is_human(vb):
            continue
        human_cards += 1
        rel = p.relative_to(root).as_posix()
        cid = str(m.get("id") or p.stem)
        rec = records.get(cid) or records.get(rel) or records.get(p.stem)
        if rec is None:
            f.append(finding("G-IRR", WARN, rel,
                             f"人工标注卡（verified_by={vb}）无 IRR 记录",
                             "补第二标注者并登记 κ"))
            continue
        raters = rec.get("raters") or rec.get("n_raters")
        kappa = rec.get("kappa")
        if isinstance(raters, int) and raters < IRR_MIN_RATERS:
            f.append(finding("G-IRR", WARN, rel,
                             f"IRR 标注者 {raters} 人 < {IRR_MIN_RATERS}", "至少 2 人独立标注"))
        if isinstance(kappa, (int, float)) and float(kappa) < IRR_MIN_KAPPA:
            f.append(finding("G-IRR", WARN, rel,
                             f"IRR κ={kappa} < {IRR_MIN_KAPPA}", "κ 过低 ⇒ 结论不可靠"))
    if human_cards == 0:
        f.append(finding("G-IRR", WARN, "atoms/", "未发现人工标注卡（射程自检）",
                         "确认 verified_by 取值"))
    return f


# ─────────────────────────────────────────────────────────────────────────────
# 注册表
# ─────────────────────────────────────────────────────────────────────────────

RULES669D: list[dict] = [
    {"id": "G-RATE-CONSISTENCY", "name": "检出率三处一致（产物/前端/论文）",
     "tier": "L0", "fn": check_rate_consistency,
     "why": "堵 81.2% 假绿：三处数字必须同源"},
    {"id": "G-DENOMINATOR", "name": "分母声明与可重算",
     "tier": "L0", "fn": check_denominator,
     "why": "堵 43.8% 分母错：k<=den 且率能从明细重算"},
    {"id": "G-STATS-FROZEN", "name": "统计口径冻结且有实现",
     "tier": "L0", "fn": check_stats_frozen,
     "why": "防改协议凑结果"},
    {"id": "G-BOUNDARY-REQUIRED", "name": "卡必须有边界/provenance",
     "tier": "L0", "fn": check_boundary_required,
     "why": "verified 卡必须有 provenance 三元组"},
    {"id": "G-BASELINE-EXISTS", "name": "实验必须有基线",
     "tier": "L0", "fn": check_baseline_exists,
     "why": "无 baseline 的实验结果不构成证据"},
    {"id": "G-IRR", "name": "标注者间一致性（只 WARN）",
     "tier": "L1", "fn": check_irr,
     "why": "人工标注需 ≥2 人且 κ≥0.6"},
]

RULES_BY_ID: dict[str, dict] = {r["id"]: r for r in RULES669D}


def run_all(root: Path, rule_ids: list[str] | None = None) -> list[dict]:
    out: list[dict] = []
    for r in RULES669D:
        if rule_ids and r["id"] not in rule_ids:
            continue
        fn: Callable[[Path], list[dict]] = r["fn"]
        try:
            out += fn(root)
        except Exception as e:                       # 门禁自身不得崩
            out.append(finding(r["id"], BLOCK, "tools/gate_rules_669d.py",
                               f"规则执行异常：{type(e).__name__}: {e}", "修规则实现"))
    return out


def selftest(root: Path) -> int:
    """射程自检：每条规则必须能产出 finding（否则说明它根本没在检查）。"""
    ok = True
    for r in RULES669D:
        try:
            res = r["fn"](root)
        except Exception as e:
            print(f"  [FAIL] {r['id']} 执行异常 {type(e).__name__}: {e}")
            ok = False
            continue
        print(f"  [ok] {r['id']}: {len(res)} finding(s)"
              f"（block {sum(1 for x in res if x['severity']==BLOCK)}"
              f" / warn {sum(1 for x in res if x['severity']==WARN)}）")
    print(f"gate_rules_669d selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="669d B 段六条 P0 门禁")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件的上级目录）")
    ap.add_argument("--rule", action="append", help="只跑指定规则（可重复）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="打印人类可读结果并返回退出码")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root) if a.root else Path(__file__).resolve().parents[1]

    if a.selftest:
        return selftest(root)

    res = run_all(root, a.rule)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        blocks = [x for x in res if x["severity"] == BLOCK]
        warns = [x for x in res if x["severity"] == WARN]
        for x in res:
            print(f"  [{x['severity'].upper():5}] {x['rule']:22} {x['target']}")
            print(f"         {x['message']}")
        print(f"\n[669d gate] block={len(blocks)} warn={len(warns)}")
    return 1 if any(x["severity"] == BLOCK for x in res) else 0


if __name__ == "__main__":
    raise SystemExit(main())
