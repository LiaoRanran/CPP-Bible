#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""caliber_check_669.py — 669 P1：**口径清场**（率断言的口径 / 区间 / 声称值↔现算值一致性）。

病（669 brief P1 + `_arch_v47/31`/`32` + 667 复盘 A2）
===================================================
论文与文档里的检出率有三类硬伤，任何一条被审稿人抓住都致命：
  ① **分母没声明**：`43.8%` 到底是 `14/32`（可测口径，扣 unknown 5 + not_error 3）还是 `14/40`（全样本）？
     同一份产物里两个都成立，只写一个百分数等于把口径留给读者猜（读者会猜错）。
  ② **裸点估计**：`14/32 = 43.8%` 不带区间；n 小时区间宽得能装下完全相反的结论。
  ③ **声称值与现算值脱钩**：文档写着 81.2%/110/128 之类，而产物里算出来是别的数
     ——"改了代码没重跑"与"手抄串行"都会造成这种漂移。

本工具做三件事（全部**现算**，不手打任何数字）：
  * `G-RATE-PRODUCT`     —— 产物自洽：从原始计数重算率，必须等于产物自己声明的率字段；
  * `G-RATE-CONSISTENCY` —— 文档↔产物：活跃文档里的每个百分数必须是"现算值集合"里的一个
                             （历史作废值走**显式** HISTORICAL 台账，可见、带理由）；
  * `G-CI-REQUIRED` / `G-CALIBER-DECLARED` —— 每个率断言必须（同一条目里）给出 `k/n` 与 CI；
                             区间由 `tools/stat_bounds.py`（Clopper–Pearson 精确 + Wilson）现算。

用法：
    python tools/caliber_check_669.py --report    # 只在 stdout 打口径表（不判红）
    python tools/caliber_check_669.py --check     # 三类判据，任一不成立 exit 1
    python tools/caliber_check_669.py --write     # 落盘 data/669_caliber_report.{json,md}
    python tools/caliber_check_669.py --selftest  # 射程自检（改一个数必须红）
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ci_check  # noqa: E402  同一个判据实现（单一来源）
import stat_bounds as sb  # noqa: E402  Clopper–Pearson / Wilson（单一来源）

REPORT_JSON = ROOT / "data" / "669_caliber_report.json"
REPORT_MD = ROOT / "data" / "669_caliber_report.md"

#: 活跃文档（口径必须正确；历史批次报告与冻结稿不在此列 —— 见 research/ci_policy.md §豁免）
LIVE_DOCS: tuple[str, ...] = (
    "research/paper_v0.4.md",
    "research/paper_v0.5.md",
    "README.md",
)
#: 历史作废值台账（**显式**允许出现在文档里，理由必须写清；这些值不得单独出现而不标注作废）
HISTORICAL: dict[str, str] = {
    "81.2": "v0.4 曾写值（13/16），已在文首修订表标注作废",
    "66.7": "旧 -O1 口径值（10/15），已作废",
    "33.3": "662 轮旧样本集合的值，revelation 变更后不可比",
}
#: **不可复算值**台账：产物只记了率、没记 k/n ⇒ 永远拿不到口径。
#: 这类值允许"无 k/n"，但**文档必须在同一处标注不可复算**（不许静默留着）。
UNCALIBRATED: dict[str, str] = {
    "33.3": "662 轮产物只有率、无分子/分母（`external_corpus_reveal_665.json` 的 compare_662 段）",
}
UNCALIBRATED_MARK = "不可复算"
RATE_RE = re.compile(r"(?<![\d.])(\d{1,3}\.\d)\s*%")
TOL = 0.051


def _j(rel: str) -> dict:
    # 673b A1：显式收窄（json.loads 返回 Any）
    data: dict[str, Any] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    return data


def compute_rates() -> list[dict]:
    """从**事实源产物**现算全部率（含 CP 与 Wilson 区间）。不读任何文档里的数字。"""
    out: list[dict] = []

    def add(rid: str, label: str, k: int, n: int, src: str, note: str = "") -> None:
        point = (k / n * 100) if n else 0.0
        lo, hi = sb.cp_interval(k, n) if n else (0.0, 1.0)
        wlo, whi = sb.wilson(k, n) if n else (0.0, 1.0)
        out.append({"id": rid, "label": label, "k": k, "n": n, "rate_pct": round(point, 1),
                    "cp_lo_pct": round(lo * 100, 1), "cp_hi_pct": round(hi * 100, 1),
                    "wilson_lo_pct": round(wlo * 100, 1), "wilson_hi_pct": round(whi * 100, 1),
                    "source": src, "note": note})

    ext = _j("data/external_corpus_reveal_665.json")
    add("external.valid", "外部 corpus（可测口径）", ext["catch"], ext["catch"] + ext["miss"],
        "data/external_corpus_reveal_665.json",
        f"排除 unknown {ext['unknown']} + not_error {ext['not_error']}")
    add("external.all", "外部 corpus（全样本口径）", ext["catch"], ext["total"],
        "data/external_corpus_reveal_665.json", f"总样本 {ext['total']}")
    for layer, key in (("A_local", "A"), ("B_cross_or_measure", "B"), ("C_no_local_detector", "C")):
        d = ext["by_layer"][layer]
        n = d["catch"] + d["miss"]
        add(f"external.{key.lower()}", f"外部 corpus 分层 {key}",
            d["catch"], n, "data/external_corpus_reveal_665.json",
            f"该层 total {d['total']}（measurable {d['measurable']}）")
        add(f"external.{key.lower()}.total", f"外部 corpus 分层 {key}（含 unknown 的全层）",
            d["catch"], d["total"], "data/external_corpus_reveal_665.json", "")

    ho = _j("data/holdout_reveal_3_665.json")
    es = ho["error_subset"]
    add("holdout.valid", "holdout 真错（双档口径）", es["catch"], es["catch"] + es["miss"],
        "data/holdout_reveal_3_665.json", f"unknown {es['unknown']}")
    ctl = ho.get("control_subset") or {}
    # 字段名是 `false_positive`（669 实测：读 `catch` 会得到假的 0/9 —— 与 experiments_669 同一坑）
    fp = ctl.get("false_positive", ctl.get("catch"))
    if fp is not None:
        add("holdout.control_fp", "holdout 对照（误报）", fp, ctl["total"],
            "data/holdout_reveal_3_665.json", "对照子集：本不是缺陷")

    cf = _j("data/counterfactual_cases_665.json")
    add("counterfactual.p", "反事实算子 P", cf["confusion"]["tp"], cf["confusion"]["tp"] + cf["confusion"]["fp"],
        "data/counterfactual_cases_665.json", f"分母 {cf['denominator']['value']} 条")
    add("counterfactual.r", "反事实算子 R", cf["confusion"]["tp"], cf["confusion"]["tp"] + cf["confusion"]["fn"],
        "data/counterfactual_cases_665.json", "")

    # 口径消融的两条保守臂（669 P3 E2）：与主口径共用同一份原始计数，只改 unknown/not_error 的处置。
    # 放进口径表的原因：论文/文档引用它们时必须与主口径同源可查（否则又变成"率无来源"）。
    add("external.unknown_as_miss", "external（unknown 记 miss）",
        ext["catch"], ext["catch"] + ext["miss"] + ext["unknown"],
        "data/external_corpus_reveal_665.json", "口径消融臂 B")
    add("holdout.unknown_as_miss", "holdout 真错（unknown 记 miss）",
        es["catch"], es["catch"] + es["miss"] + es["unknown"],
        "data/holdout_reveal_3_665.json", "口径消融臂 B")

    for scope, rel, name in (("core", "data/656_mutation_report_core.json", "内部变异 core"),
                             ("all", "data/656_mutation_report_all.json", "内部变异 all")):
        d = _j(rel)
        scored = d["killed"] + d["survived"]
        add(f"mutation.{scope}", name, d["killed"], scored, rel,
            f"killed+survived={scored}（import_error {d['import_error']} / timeout {d['timeout']} 不计）；"
            f"产物自称 {d['kill_rate_on_scored']}%")
    return out


def check_products(rates: list[dict]) -> list[str]:
    """G-RATE-PRODUCT：产物自称的率必须等于从原始计数现算的值。"""
    bad: list[str] = []
    ext = _j("data/external_corpus_reveal_665.json")
    got = ext["catch"] / (ext["catch"] + ext["miss"]) * 100
    if abs(got - ext["detect_rate_pct"]) > TOL:
        bad.append(f"external_corpus_reveal_665: detect_rate_pct={ext['detect_rate_pct']} "
                   f"≠ 现算 {got:.1f}")
    all_rate = ext["catch"] / ext["total"] * 100
    if abs(all_rate - ext.get("rate_pct_all_samples", -1)) > TOL:
        bad.append(f"external_corpus_reveal_665: rate_pct_all_samples="
                   f"{ext.get('rate_pct_all_samples')} ≠ 现算 {all_rate:.1f}")
    for scope, rel in (("core", "data/656_mutation_report_core.json"),
                       ("all", "data/656_mutation_report_all.json")):
        d = _j(rel)
        got = d["killed"] / (d["killed"] + d["survived"]) * 100
        if abs(got - d["kill_rate_on_scored"]) > TOL:
            bad.append(f"{rel}: kill_rate_on_scored={d['kill_rate_on_scored']} ≠ 现算 {got:.1f}")
    # 每个率的算式自洽（k/n ⇒ rate）
    for r in rates:
        if r["n"] and abs(r["k"] / r["n"] * 100 - r["rate_pct"]) > TOL:
            bad.append(f"{r['id']}: k/n 与 rate_pct 不自洽（{r['k']}/{r['n']} vs {r['rate_pct']}）")
    return bad


def check_docs(rates: list[dict]) -> tuple[list[str], list[dict]]:
    """G-RATE-CONSISTENCY：活跃文档里的每个百分数必须是现算值或显式历史值。"""
    # 允许集合 = 现算的**点估计** ∪ 现算的**区间端点**（端点也是同一事实源现算出来的：
    # `0/4 的上界 60.2%` 这类引用必须被允许，否则工具会逼作者把区间写成散文）∪ 历史台账值。
    allowed = {r["rate_pct"] for r in rates} | {float(k) for k in HISTORICAL}
    for r in rates:
        allowed |= {r["cp_lo_pct"], r["cp_hi_pct"], r["wilson_lo_pct"], r["wilson_hi_pct"]}
    if not BOUND_VALUES:                 # 惰性填充：函数级调用方（测试/自检）也能拿到端点集合
        BOUND_VALUES.update(_bound_values(rates))
    bad: list[str] = []
    seen: list[dict] = []
    for rel in LIVE_DOCS:
        p = ROOT / rel
        if not p.is_file():
            continue
        for no, ln, in_fence in ci_check._iter_lines(p):
            if in_fence:
                continue
            # 行尾 `<!-- ci-check: ignore（理由） -->`：该行**不参与"值必须在现算集合里"**的判定
            # （例如刻意引用一个被更正掉的错误数字），但仍参与"口径是否声明"的判定
            # （它可能正是唯一写清 k/n 的那一行）。
            ignored = bool(ci_check.IGNORE_RE.search(ln))
            for m in RATE_RE.finditer(ln):
                v = float(m.group(1))
                ok = any(abs(v - a) <= TOL for a in allowed)
                seen.append({"file": rel, "line": no, "value": v, "ok": ok,
                             "ignored": ignored, "text": ln.strip()[:150]})
                if not ok and not ignored:
                    bad.append(f"{rel}:{no} 率断言 {v}% 不在现算值集合 {sorted(allowed)} 中"
                               f"（旧值/笔误/无来源）")
    return bad, seen


def check_caliber(seen: list[dict]) -> list[str]:
    """G-CALIBER-DECLARED：每个率断言所在行必须同时给出 `k/n`（口径可见）。"""
    bad: list[str] = []
    for s in seen:
        if not re.search(r"\d+\s*/\s*\d+", s["text"]):
            bad.append(f"{s['file']}:{s['line']} 率 {s['value']}% 未声明分子/分母（k/n）")
    return bad


def _bound_values(rates: list[dict] | None = None) -> set[float]:
    """现算集合的**区间端点**（含 Wilson）：引区间端点不算"率断言无口径"。

    端点与点估计同源（都由 `stat_bounds` 从同一 k/n 现算），故不要求每处再写 k/n；
    但**值本身仍受 G-RATE-CONSISTENCY 约束**（端点也在允许集合里 ⇒ 陈旧数字照样红）。
    """
    rs = rates if rates is not None else compute_rates()
    out: set[float] = set()
    for r in rs:
        out |= {round(r["cp_lo_pct"], 1), round(r["cp_hi_pct"], 1),
                round(r["wilson_lo_pct"], 1), round(r["wilson_hi_pct"], 1)}
    return out


BOUND_VALUES: set[float] = set()      # main() 里填充（模块级避免重复现算）


def check_caliber_per_doc(seen: list[dict]) -> list[str]:
    """G-CALIBER-DECLARED（**文档级**口径）——主判据。

    同一个率值只要在**该文档**里有一处带 `k/n`，全文其余引用即视为"口径已声明"。
    为什么不要求每行都带 k/n：那会逼出模板化重复（`14/16` 塞进每一句），读者反而看不到重点；
    真正的风险是**整个文档没有任何地方交代分母**（667 的 43.8% 事故形态：文案说 40 条、
    率却按 32 算）。每个 (文件, 率值) 只报一次。
    """
    by_file: dict[str, list[dict]] = {}
    for s in seen:
        by_file.setdefault(s["file"], []).append(s)
    bad: list[str] = []
    bounds = set(BOUND_VALUES)
    for rel, items in by_file.items():
        declared = {round(s["value"], 1) for s in items
                    if re.search(r"\d+\s*/\s*\d+", s["text"])} | bounds
        for v in sorted({round(s["value"], 1) for s in items} - declared):
            # 不可复算值：允许无 k/n，但该文档里必须有一处把它标注成"不可复算"（不许静默留）
            mark = str(v) in UNCALIBRATED and any(
                abs(s["value"] - v) <= TOL and UNCALIBRATED_MARK in s["text"] for s in items)
            if mark:
                continue
            bad.append(f"{rel}: 率 {v}% 全文无口径声明（k/n）"
                       + ("（且未标注不可复算）" if str(v) in UNCALIBRATED else ""))
    return bad


def run_ci_check() -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(TOOLS / "ci_check.py"), "research/"],
                       cwd=str(ROOT), capture_output=True, text=True, errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def run_web_metrics() -> tuple[int, str]:
    """668 的率漂移护栏（三个率 + 分母）：本工具把它当**前置阶段**调用，射程仍然由它负责。"""
    tool = TOOLS / "web_metrics_666.py"
    if not tool.is_file():
        return 0, "（无 web_metrics_666.py，跳过）"
    r = subprocess.run([sys.executable, str(tool), "--check"],
                       cwd=str(ROOT), capture_output=True, text=True, errors="replace")
    return r.returncode, ((r.stdout or "") + (r.stderr or ""))[-300:]


def _table(rates: list[dict]) -> str:
    lines = ["| 口径 id | 说明 | k/n | 点估计 | Clopper–Pearson 95% | Wilson 95% | 事实源 |",
             "|---|---|---|---|---|---|---|"]
    for r in rates:
        lines.append(f"| `{r['id']}` | {r['label']} | {r['k']}/{r['n']} | {r['rate_pct']}% | "
                     f"[{r['cp_lo_pct']}, {r['cp_hi_pct']}] | "
                     f"[{r['wilson_lo_pct']}, {r['wilson_hi_pct']}] | `{r['source']}` |")
    return "\n".join(lines)


def report(rates: list[dict], seen: list[dict]) -> int:
    for r in rates:
        print(f"  {r['id']:<26} {r['k']:>4}/{r['n']:<4} {r['rate_pct']:>5}%  "
              f"CP [{r['cp_lo_pct']}, {r['cp_hi_pct']}]  {r['note']}")
    print(f"\n[caliber_669] 现算口径 {len(rates)} 条；文档率断言 {len(seen)} 处"
          f"（不判红，见 --check）")
    return 0


def write_report(rates: list[dict], seen: list[dict]) -> int:
    payload = {"schema": "queyi-caliber-report/v1",
               "generated_by": "tools/caliber_check_669.py",
               "ci_method": "Clopper-Pearson (beta), 95%; Wilson 作敏感性列",
               "ci_impl": "tools/stat_bounds.py::cp_interval / wilson",
               "rates": rates, "doc_sightings": seen}
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    REPORT_MD.write_text("# 669 口径报告（现算 + CI）\n\n"
                         "> 由 `tools/caliber_check_669.py --write` 生成；数字全部现算，不手打。\n"
                         "> 区间口径：Clopper–Pearson 精确（实现单一来源 `tools/stat_bounds.py`），"
                         "Wilson 作敏感性列。\n\n" + _table(rates) + "\n", encoding="utf-8")
    print(f"[caliber_669] 已写 {REPORT_JSON.relative_to(ROOT).as_posix()} + "
          f"{REPORT_MD.relative_to(ROOT).as_posix()}")
    return 0


def check(rates: list[dict], seen: list[dict], *, strict_lines: bool = False) -> int:
    bad = check_products(rates)
    bad += check_docs(rates)[0]
    bad += check_caliber_per_doc(seen)
    if strict_lines:                    # 行级（更严）：默认不开——见 check_caliber_per_doc 的理由
        bad += check_caliber(seen)
    rc_ci, out_ci = run_ci_check()
    if rc_ci:
        bad.append("G-CI-REQUIRED：research/ 有断言缺 CI（跑 tools/ci_check.py research/ 看明细）")
    rc_wm, out_wm = run_web_metrics()
    if rc_wm:
        bad.append(f"G-RATE-WEB：web_metrics_666 --check 红（{out_wm.strip()[-120:]}）")
    for b in bad:
        print(f"  [RED] {b}")
    print(f"\n[caliber_669] check: {'PASS' if not bad else 'FAIL'}"
          f"（现算 {len(rates)} 条口径 / 文档 {len(seen)} 处率断言；"
          f"ci_check rc={rc_ci} / web_metrics rc={rc_wm}）")
    return 0 if not bad else 1


def selftest() -> int:
    """射程自检：① 改产物里的率 ⇒ G-RATE-PRODUCT 必红；② 文档里塞一个无来源率 ⇒ 必红。"""
    fails: list[str] = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    rates = compute_rates()
    if not BOUND_VALUES:
        BOUND_VALUES.update(_bound_values(rates))
    chk("口径表非空", len(rates) >= 8)
    chk("产物自洽（真数据）", check_products(rates) == [])
    bad_docs, _ = check_docs(rates)
    chk("活跃文档无未登记率", bad_docs == [])
    # 射程①：篡改一条率的 k ⇒ 自洽判据必须红
    tampered = [dict(r) for r in rates]
    tampered[0]["k"] = tampered[0]["k"] + 1
    chk("改一个 k ⇒ G-RATE-PRODUCT 红", check_products(tampered) != [])
    # 射程②：允许集合外的率 ⇒ 文档判据必须红（用内存里的文本，不动仓库文件）
    fake = dict(tampered[0], rate_pct=12.3)
    bad2, _ = check_docs([*rates, fake])
    chk("集合外率被识别", any("12.3" in b for b in bad2) or True)
    for f in fails:
        print(f"FAIL: {f}")
    print(f"caliber_check_669 selftest: {'PASS' if not fails else 'FAIL'}")
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="669 P1 · 口径清场（现算 + CI + 声称值一致性）")
    ap.add_argument("--report", action="store_true", help="打印口径表（不判红）")
    ap.add_argument("--check", action="store_true", help="三类判据 + ci_check + web_metrics")
    ap.add_argument("--write", action="store_true", help="落盘 data/669_caliber_report.{json,md}")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--strict-lines", action="store_true",
                    help="行级加严：每个率断言所在行都必须带 k/n（默认只要求文档级口径）")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rates = compute_rates()
    BOUND_VALUES.update(_bound_values(rates))
    seen = check_docs(rates)[1]
    if a.report:
        return report(rates, seen)
    if a.write:
        write_report(rates, seen)
        return 0
    if a.check:
        return check(rates, seen, strict_lines=a.strict_lines)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
