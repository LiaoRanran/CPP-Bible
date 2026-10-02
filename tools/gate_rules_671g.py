#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gate_rules_671g.py — 671g 纪律门禁注册表（数字真实性 / 口径 / 方法学 / 跨学科）。

设计约定与 `gate_rules_670g.py` 一致
=====================================
* 每条规则 `check_*(root: Path) -> list[dict]`，finding = {rule,severity,target,message,fix_hint}；
* severity ∈ {block, warn}；本模块**只判读、只复用各 671g 工具的纯函数，不写盘**；
* 规则表可扩张：主门禁（run_master_gate_670c.py）从 RULES 现读条数，新规则默认 L0（fail-closed）。

规则总览（随 D/E 批次扩张）
============================
B 数字真实性/口径
  G-NUMBER-CONSISTENCY     率三元组算术自洽 + 同(k,n)同率
  G-DENOMINATOR-COMPLETE  结果率必须带分母(k/n)+口径（本批纪律文档/671g产物）
  G-VERIFIED-NUMBERS       全部实验数字必须能从事实源自洽复现
  G-TERMINOLOGY            工程文档术语统一（祈易/留出集/缺陷语境探测器 禁止）
D 方法学（在下方注册）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def finding(rule: str, severity: str, target: str, message: str,
          fix_hint: str = "") -> dict[str, Any]:
    return {"rule": rule, "severity": severity, "target": target,
            "message": message, "fix_hint": fix_hint}


def _import(mod: str):
    __import__(mod)
    return sys.modules[mod]


def _gate_from_results(modname: str, rid: str, call: str) -> Callable[[Path], list[dict[str, Any]]]:
    """把一个 671g 工具的 check/evaluate 结果接进门禁 finding。

    统一语义：工具结果里 **block/rejected ⇒ block**；**warn/inconclusive/unarmed ⇒ warn（未进射程
    要显形但不阻断）**；**pass/ok/空 ⇒ 无 finding**。工具执行异常 ⇒ fail-closed block。
    """
    def _fn(root: Path) -> list[dict[str, Any]]:
        try:
            M = _import(modname)
            res = getattr(M, call)(root)
        except Exception as e:                  # noqa: BLE001
            return [finding(rid, "block", modname, f"{call} 执行异常：{type(e).__name__}: {e}")]
        # dict + status（poison 工具）：整体一个结论
        if isinstance(res, dict) and "status" in res and "findings" not in res:
            st = str(res.get("status"))
            if st in ("block", "rejected"):
                return [finding(rid, "block", rid, str(res.get("why") or res))]
            if st in ("warn", "inconclusive", "unarmed", "unknown"):
                return [finding(rid, "warn", rid, f"未进射程（{st}）：{res.get('why', '')}")]
            return []
        rows: list[dict[str, Any]] = res if isinstance(res, list) else res.get("findings", [])
        out: list[dict[str, Any]] = []
        for r in rows:
            sev = str(r.get("severity", "block"))
            stt = str(r.get("status", ""))
            if sev == "ok" or stt == "pass":
                continue
            if sev not in ("block", "warn"):
                sev = "warn" if stt in ("inconclusive", "unarmed") else "block"
            if sev == "warn" and stt not in ("block", "warn", "inconclusive", "unarmed", "rejected"):
                # 工具的 pass 明细（thymus 逐条）不当 finding
                continue
            out.append(finding(rid, sev, str(r.get("target") or r.get("id") or modname),
                             str(r.get("message") or r.get("why") or ""),
                             str(r.get("fix_hint", ""))))
        return out
    return _fn


# ── B1：率三元组一致性 ─────────────────────────────────────────────────────────
def check_number_consistency(root: Path) -> list[dict[str, Any]]:
    try:
        S = _import("number_consistency_scan_671g")
    except Exception as e:                      # noqa: BLE001
        return [finding("G-NUMBER-CONSISTENCY", "block", "tools/number_consistency_scan_671g.py",
                       f"扫描器导入失败：{type(e).__name__}: {e}")]
    rep = S.scan(root)
    out = []
    for r in rep["arithmetic_inconsistencies"]:
        out.append(finding("G-NUMBER-CONSISTENCY", "block", r["file"], r["why"],
                          "按 (k,n) 现算改 pct，或改正 k/n；禁止为绿改断言"))
    for r in rep["conflicting_calibers"]:
        sites = ", ".join(f"{s['file']}={s['pct']}%" for s in r["sites"][:5])
        out.append(finding("G-NUMBER-CONSISTENCY", "block",
                          f"(k,n)=({r['k']},{r['n']})",
                          f"同一分母分子被写成不同率 {r['pcts']}：{sites}",
                          "以 tools/numbers_671g.py 现算值为准统一"))
    return out


# ── B3：率必须带分母+口径 ───────────────────────────────────────────────────────
def check_denominator(root: Path) -> list[dict[str, Any]]:
    try:
        S = _import("number_consistency_scan_671g")
    except Exception as e:                      # noqa: BLE001
        return [finding("G-DENOMINATOR-COMPLETE", "block", "number_consistency_scan_671g",
                       f"导入失败：{e}")]
    out: list[dict[str, Any]] = S.check_denominator_complete(root)
    return out


# ── A2：全部实验数字自洽复现 ─────────────────────────────────────────────────
def check_verified_numbers(root: Path) -> list[dict[str, Any]]:
    try:
        N = _import("numbers_671g")
    except Exception as e:                      # noqa: BLE001
        return [finding("G-VERIFIED-NUMBERS", "block", "tools/numbers_671g.py",
                       f"复算工具导入失败：{e}")]
    rep = N.collect(root)
    out = []
    for key in rep["self_inconsistent"]:
        out.append(finding("G-VERIFIED-NUMBERS", "block", key,
                           f"{key} 的声称值无法从事实源自洽复现",
                           "见 data/671g_数字真实性核查.md；定位口径/脚本/产物问题，禁改断言"))
    return out


# ── B2：术语 ────────────────────────────────────────────────────────────────────
def check_terminology(root: Path) -> list[dict[str, Any]]:
    try:
        T = _import("terminology_scan_671g")
    except Exception as e:                      # noqa: BLE001
        return [finding("G-TERMINOLOGY", "block", "tools/terminology_scan_671g.py",
                       f"扫描器导入失败：{e}")]
    rep = T.scan(root)
    return [finding("G-TERMINOLOGY", "block", f"{b['file']}:{b['line']}",
                    f"{b['why']}（{b['canonical']}）", b["text"]) for b in rep["blocks"]]


#: 规则注册表（(id, check_fn)；主门禁与 --rule 都从这里取）
RULES: list[tuple[str, Callable[[Path], list[dict[str, Any]]]]] = [
    ("G-NUMBER-CONSISTENCY", check_number_consistency),
    ("G-DENOMINATOR-COMPLETE", check_denominator),
    ("G-VERIFIED-NUMBERS", check_verified_numbers),
    ("G-TERMINOLOGY", check_terminology),
]


# ─────────────────────────────────────────────────────────────────────────────────────
# D 方法学 / E 跨学科门禁（规则实现见各 *_671g 工具，这里只接线，复用纯函数）
# ─────────────────────────────────────────────────────────────────────────────────────

def check_rules_pinned(root: Path) -> list[dict[str, Any]]:
    """D1 G-RULES-PINNED：manifest 与现行规则一致 + 671g 判决目录全部钉扎。"""
    try:
        import rules_manifest_671g as M
    except Exception as e:                      # noqa: BLE001
        return [finding("G-RULES-PINNED", "block", "rules_manifest_671g", f"导入失败：{e}")]
    out = []
    # 无 manifest ⇒ 未武装（warn），与其它 671g 门禁 fail-soft 一致；
    # 真实仓已生成 manifest（armed），manifest 存在才对不一致/判决失配 fail-closed。
    if M.load_manifest(root) is None:
        return [finding("G-RULES-PINNED", "warn", "data/rules_manifest_671g.json",
                       "manifest 缺失：规则钉扎未武装（最小仓/历史仓不阻断；新仓需 --generate）")]
    for p in M.verify(root):
        out.append(finding("G-RULES-PINNED", "block", "data/rules_manifest_671g.json", p,
                            "规则变了：bump rules_version、重生成 manifest、旧判决显式归档"))
    for f in M.verify_verdicts(root, "data/671g/verdicts"):
        out.append(finding("G-RULES-PINNED", f["severity"], f["target"], f["message"]))
    return out


def check_ledger_invariants(root: Path) -> list[dict[str, Any]]:
    """D6 G-LEDGER-INVARIANTS：671g 账本过 10 条不变式。"""
    try:
        import ledger_invariants_671g as L
        import rules_manifest_671g as M
    except Exception as e:                      # noqa: BLE001
        return [finding("G-LEDGER-INVARIANTS", "block", "ledger_invariants_671g", f"导入失败：{e}")]
    man = M.load_manifest(root)
    ver = str(man["rules_version"]) if man else None
    out = []
    for v in L.validate_file(root, L.LEDGER_PATH, ver):
        out.append(finding("G-LEDGER-INVARIANTS", "block",
                          f"seq={v['seq_idx']}", f"{v['inv']}: {v['why']}"))
    return out


RULES.extend([
    ("G-RULES-PINNED", check_rules_pinned),
    ("G-FP-THYMUS", _gate_from_results("false_positive_thymus_671g", "G-FP-THYMUS", "evaluate")),
    ("G-PAP-REGISTERED", _gate_from_results("pap_register_671g", "G-PAP-REGISTERED", "check")),
    ("G-LLM-CHANNEL", _gate_from_results("llm_channel_defense_671g", "G-LLM-CHANNEL", "check")),
    ("G-POISON-DETECT", _gate_from_results("poison_detection_671g", "G-POISON-DETECT", "evaluate")),
    ("G-TRAJECTORY-FLOOR", _gate_from_results("trajectory_floor_check_671g",
                                              "G-TRAJECTORY-FLOOR", "check")),
    ("G-LEDGER-INVARIANTS", check_ledger_invariants),
    ("G-ITT-DISCIPLINE", _gate_from_results("itt_discipline_671g", "G-ITT-DISCIPLINE", "check")),
    ("G-NO-OVERFITTING", _gate_from_results("overfitting_defense_671g", "G-NO-OVERFITTING", "check")),
    ("G-EVIDENCE-CHAIN", _gate_from_results("evidence_chain_671g", "G-EVIDENCE-CHAIN", "check")),
])


def run_all(root: Path = ROOT) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for name, fn in RULES:
        try:
            out.extend(fn(root))
        except Exception as e:                  # noqa: BLE001  门禁自身异常 fail-closed 判红
            out.append(finding(name, "block", str(name),
                             f"规则执行异常：{type(e).__name__}: {e}"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g 纪律门禁（数字真实性/口径/方法学）")
    ap.add_argument("--root", default=None)
    ap.add_argument("--rule", default=None, help="只跑一条规则")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.rule:
        rules = [(n, f) for n, f in RULES if n == a.rule]
        if not rules:
            print(f"未知规则：{a.rule}；现有：{[n for n, _ in RULES]}")
            return 2
        findings = rules[0][1](root)
    else:
        findings = run_all(root)
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"[671g gates] PASS（{len(RULES)} 条规则 0 finding）")
        for f in findings:
            print(f"  [{f['severity'].upper()}] {f['rule']} {f['target']}: {f['message']}")
    return 1 if any(f["severity"] == "block" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
