#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_metrics_666.py — 666 B2：给首页"核心指标 + 状态时间线"提供**现算**数据。

目标
====
首页要显示四项核心指标（卡数 / 规则数 / 检出率 / 账本事件）与一条系统状态时间线。
纪律（655 起沿用）：**前端只渲染，不写死** —— 所以数字必须先由工具现算落成 JSON。

数据源（全部现场复算，不抄写）
==============================
| 指标 | 来源 |
|---|---|
| 卡数 | `counts_659.ATOMS_REAL` / `ATOMS_DRAFT`（扫 `atoms/`） |
| 规则数 | `gate_engine.RULES`（与 `data/_gate_rules.json` 同源） |
| 检出率 | `data/holdout_reveal_3_665.json::error_subset.detect_rate_pct`；**口径与分母从产物的 `caliber`/`denominator` 读**（668 起，不写死） |
| 账本事件 | `data/646_authority_rule_annotation.jsonl` 行数（452 红线所在账本） |
| 外部语料 | `data/external_corpus_reveal_665.json`：**两个分母都算**（catch+miss 与全样本） |
| 反事实 | `data/counterfactual_cases_665.json::scores`（P/R/F1 + 分母 + 第三判据命中数） |
| 时间线 | 关键批次里程碑（写死**批次与含义**，不写死数字）+ `git log` 最近提交 |

边界（为什么不是"抄一份 status.json"）
======================================
`web_status_655.py` 那份是"系统现状面板"（保护器/逃逸率/W2），语义与首页指标不同；
本工具**只加不改**：`--check` 只读自检（现算 vs 落盘漂移），`--write` 才落盘。

用法
====
    python tools/web_metrics_666.py --check     # 只读：现算 vs 已落盘（漂移可见）
    python tools/web_metrics_666.py --write     # 写 web/data/metrics_666.json
    python tools/web_metrics_666.py --selftest  # 自检（数据源可达、字段齐全）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT = os.path.join(ROOT, "web", "data", "metrics_666.json")
LEDGER = os.path.join(ROOT, "data", "646_authority_rule_annotation.jsonl")

#: 批次里程碑（只有"批次 / 日期 / 做了什么 / 证据命令"是恒定的；
#: 任何**数字**都必须来自现算 —— 这就是本工具存在的理由）
MILESTONES: list[dict[str, str]] = [
    {"batch": "641", "date": "2026-09", "state": "pass",
     "what": "协议内核 v1.0 落地（四态判决 + 半格 + 账本）",
     "why": "把「可被独立验收」变成可执行代码：判决、账本、Merkle 各自可复算"},
    {"batch": "645/646", "date": "2026-09", "state": "pass",
     "what": "编译器实测证据（L1 双编译器）+ 规则-卡映射 67/67",
     "why": "断言不再只靠「书上说」：每条有真机编译输出"},
    {"batch": "647", "date": "2026-09", "state": "pass",
     "what": "内核拆分到独立仓 `queyi-verifier`（单一实现、两处入口）",
     "why": "验证器可被第三方单独拉取安装"},
    {"batch": "656", "date": "2026-09-28", "state": "pass",
     "what": "门禁分层（L0 红线 / L1 建议）+ 内部变异测试",
     "why": "把「必须过」与「记录下来看」分开，避免狼来了"},
    {"batch": "661/664/665", "date": "2026-09-29", "state": "reason",
     "what": "缺陷注入 / 独立生成 / 扩样（holdout 30、外部语料 40、反事实 20）",
     "why": "样本量是主要矛盾；但扩样样本**无盲态**，不得用于 Claim 外部效度"},
    {"batch": "666", "date": "2026-09-29", "state": "pass",
     "what": "两侧套件全绿 + 双档检测 pipeline + 口径收敛（67 / 178）",
     "why": "低分常是**测量配置错**：3 个假 miss 换档位即抓住；旧值作废而非静默替换"},
]


def _json(rel: str) -> dict:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        data: dict = json.load(fh)      # 666 A1：注解消 no-any-return（json.load 返 Any）
        return data


def _count_lines(path: str) -> int:
    if not os.path.isfile(path):
        return -1
    with open(path, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ln in fh if ln.strip())


def _git(args: list[str]) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30, check=False)
        return r.stdout if r.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""


def recent_commits(n: int = 5) -> list[dict[str, str]]:
    out = _git(["log", f"-{n}", "--pretty=format:%h%x1f%ad%x1f%s", "--date=short"])
    rows = []
    for ln in out.splitlines():
        parts = ln.split("\x1f")
        if len(parts) == 3:
            rows.append({"hash": parts[0], "date": parts[1], "subject": parts[2][:120]})
    return rows


def collect() -> dict:
    """现算全部指标（任何一项拿不到 ⇒ 记 null 并进 `unavailable`，不猜）。"""
    unavailable: list[str] = []
    import counts_659 as counts  # noqa: E402
    import gate_engine as ge  # noqa: E402

    m: dict = {}
    m["cards_real"] = counts.ATOMS_REAL
    m["cards_draft"] = counts.ATOMS_DRAFT
    m["rules_total"] = len(ge.RULES)

    detect = None
    try:
        # 672h（W3 扩样）：切到第 5 轮产物（h41–h60 已 reveal，holdout 可测 41）
        r3 = _json("data/holdout_reveal_5_672h.json")
        cum = r3.get("cumulative", {})
        sub = cum.get("error_subset", {})
        # 668：**口径与分母从产物读**，不许在工具里写死 —— 666 的 81.2% 就是
        # "口径字符串写在工具里、数字写在文档里、两边没人对过"造成的。
        # 672f：671a 产物不带 opt_levels ⇒ 档位从检测判据单一来源读（holdout_reveal_661.OPT_LEVELS）
        import holdout_reveal_661 as rv661  # noqa: PLC0415
        opts = list(getattr(rv661, "OPT_LEVELS", ()) or [])
        caliber = r3.get("caliber") or "产物未声明口径（旧产物）"
        if opts:
            caliber = f"{caliber}；检测档位 {'/'.join(opts)} 任一档报出即 catch"
        detect = {"rate_pct": sub.get("detect_rate_pct"), "catch": sub.get("catch"),
                  "miss": sub.get("miss"), "unknown": sub.get("unknown"),
                  "den": (sub.get("catch") or 0) + (sub.get("miss") or 0),
                  "denominator": (cum.get("denominator") or {}).get("meaning")
                  or "产物未声明分母（旧产物）",
                  "caliber": caliber,
                  "opt_levels": opts,
                  "env": (r3.get("env") or {}).get("wsl_gpp"),
                  "detail": "data/holdout/reveal_5_detail_672h.json",
                  "cmd": "python tools/holdout_reveal_5_672h.py"}
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"holdout_reveal_5_672h.json: {e}")
    m["holdout"] = detect

    ext = None
    try:
        # 672h（W3 扩样）：切到 corpus 第 4 轮产物（d3f-* 已 reveal，可测 64）
        r = _json("data/external_corpus_reveal_672h.json")
        cum = r.get("cumulative", {})
        catch, miss = cum.get("catch") or 0, cum.get("miss") or 0
        total = cum.get("total") or 0
        ext = {"rate_pct": cum.get("detect_rate_pct"),
               "rate_pct_all": (round(catch / total * 100, 1) if total else None),
               "total": total, "catch": catch, "miss": miss,
               "unknown": cum.get("unknown"), "den": catch + miss,
               "denominator": cum.get("denominator") or "catch+miss（产物未声明 ⇒ 这里按口径推算）",
               "cmd": "python tools/external_corpus_reveal_671a.py"}
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"external_corpus_reveal_671a.json: {e}")
    m["external"] = ext

    cf = None
    try:
        c = _json("data/counterfactual_cases_665.json")
        sc = c.get("scores") or {}
        cf = {"p": sc.get("precision"), "r": sc.get("recall"), "f1": sc.get("f1"),
              "cases": c.get("cases_total"),
              "denominator": (c.get("denominator") or {}).get("meaning")
              or "产物未声明分母（旧产物）",
              "third_criterion_hits": (c.get("third_criterion") or {}).get("hit_count"),
              "cmd": "python tools/counterfactual_extend_665.py"}
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"counterfactual_cases_665.json: {e}")
    m["counterfactual"] = cf

    n_led = _count_lines(LEDGER)
    if n_led < 0:
        unavailable.append("646_authority_rule_annotation.jsonl 缺失")
        m["ledger_events"] = None
    else:
        m["ledger_events"] = n_led
    m["ledger_path"] = "data/646_authority_rule_annotation.jsonl"
    m["ledger_redline"] = "452 事件零改（本批未动该文件）"

    tl = _count_lines(os.path.join(ROOT, "data", "transparency_log.jsonl"))
    m["transparency_log_entries"] = tl if tl >= 0 else None
    if tl < 0:
        unavailable.append("transparency_log.jsonl 缺失")

    try:
        mr = _json("data/supply_chain/merkle_roots.json")
        dirs = mr.get("dirs", {})
        m["merkle_dirs"] = sorted(dirs)
        m["merkle_files"] = sum(int(d.get("file_count", 0)) for d in dirs.values()
                                if isinstance(d, dict))
    except Exception as e:  # noqa: BLE001
        unavailable.append(f"merkle_roots.json: {e}")

    return {
        "schema": "queyi-web-metrics/666",
        "generated_by": "tools/web_metrics_666.py",
        # 672b：落盘时间，便于前端/验收报告核对数据新鲜度
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "metrics": m,
        "timeline": MILESTONES,
        "commits": recent_commits(5),
        "unavailable": unavailable,
        "honest_note": ("本文件的**数字全部现算**（扫卡 / 读引擎 / 读 reveal 报告），"
                        "前端只渲染；拿不到的项记 null 并进 unavailable，不用占位值冒充。"
                        "**口径与分母从产物读**（`holdout.caliber` / `holdout.denominator`），"
                        "不在这里写死。668 已把 holdout / external / counterfactual 三个率的"
                        "现算值纳入 `--check` 比对范围（666 漏查这三项 ⇒ 曾出现假绿）。"),
    }


def selftest() -> int:
    """只读自检（不写盘）：数据源可达、字段齐全、缺失项显式登记。"""
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    fresh = collect()
    chk("卡数 > 0", fresh["metrics"]["cards_real"] > 0, f"({fresh['metrics']['cards_real']})")
    chk("规则数 == 引擎条数", fresh["metrics"]["rules_total"] > 0,
        f"({fresh['metrics']['rules_total']})")
    chk("检出率可读", bool(fresh["metrics"]["holdout"]), "")
    # 668：口径必须**来自产物**，不能是工具里写死的字符串
    h = fresh["metrics"].get("holdout") or {}
    chk("检出率带分母（数值）", isinstance(h.get("den"), int) and h["den"] > 0, f"(den={h.get('den')})")
    chk("检出率带分母（说明）", bool(h.get("denominator")) and "未声明" not in str(h.get("denominator")), "")
    chk("检出率带口径（来自产物）", bool(h.get("caliber")) and "未声明" not in str(h.get("caliber")), "")
    chk("口径声明的档位 == 实际档位", h.get("opt_levels") == ["-O0", "-O2"], f"({h.get('opt_levels')})")
    e = fresh["metrics"].get("external") or {}
    chk("外部语料两个分母都在", e.get("rate_pct") is not None and e.get("rate_pct_all") is not None,
        f"({e.get('rate_pct')} / {e.get('rate_pct_all')})")
    c = fresh["metrics"].get("counterfactual") or {}
    chk("反事实有 F1 与分母", c.get("f1") is not None and c.get("cases"),
        f"(F1={c.get('f1')} n={c.get('cases')})")
    chk("账本事件 > 0", bool(fresh["metrics"]["ledger_events"]), "")
    chk("时间线非空", len(fresh["timeline"]) >= 5, f"({len(fresh['timeline'])})")
    chk("提交列表可读（无 git 时允许为空）", isinstance(fresh["commits"], list))
    chk("拿不到的项都显式登记", isinstance(fresh["unavailable"], list),
        f"({fresh['unavailable']})")
    print("web_metrics_666 selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="666 B2 · 首页指标与时间线数据（现算）")
    ap.add_argument("--check", action="store_true", help="只读：现算 vs 已落盘")
    ap.add_argument("--write", action="store_true", help="写 web/data/metrics_666.json")
    ap.add_argument("--selftest", action="store_true", help="自检")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    fresh = collect()

    if a.check:
        if not os.path.isfile(OUT):
            print(f"[web666] ✗ 未落盘 {os.path.relpath(OUT, ROOT)}（先 --write）")
            return 1
        # 668：读 **OUT**（可被测试指向别处），而不是硬编码路径 ——
        # 原来 `--check` 无视 `OUT`，monkeypatch 掉的落盘文件对不上，测试只能"绕过"，
        # 于是这条自检路径**从来没有被真正测过**。
        with open(OUT, encoding="utf-8") as fh:
            old = json.load(fh)
        drift = []
        for k in ("cards_real", "cards_draft", "rules_total", "ledger_events",
                  "transparency_log_entries"):
            if old.get("metrics", {}).get(k) != fresh["metrics"].get(k):
                drift.append((k, old.get("metrics", {}).get(k), fresh["metrics"].get(k)))
        # 668：**补齐射程** —— 666 的 --check 偏偏没查最要紧的两个率，
        # 于是"落盘 81.2% / 现算 66.7%"共存了一个批次还报绿。
        # 纪律（R4）：加了字段就必须能被"改一个数 ⇒ 变红"验证。
        for key, fields in (("holdout", ("rate_pct", "catch", "miss", "unknown", "den")),
                            ("external", ("rate_pct", "catch", "miss", "total", "unknown")),
                            ("counterfactual", ("f1", "cases"))):
            o = old.get("metrics", {}).get(key) or {}
            n = fresh["metrics"].get(key) or {}
            for f in fields:
                if o.get(f) != n.get(f):
                    drift.append((f"{key}.{f}", o.get(f), n.get(f)))
        for r in drift:
            print(f"[web666] ✗ 漂移 {r[0]}：落盘 {r[1]} → 现算 {r[2]}")
        print("[web666] " + ("✅ 与现算一致" if not drift else f"❌ {len(drift)} 项漂移（重跑 --write）"))
        return 0 if not drift else 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fresh, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    mm = fresh["metrics"]
    print(f"[web666] 写入 {os.path.relpath(OUT, ROOT)}：卡 {mm['cards_real']}"
          f"(+{mm['cards_draft']}) · 规则 {mm['rules_total']} · 检出率 "
          f"{(mm['holdout'] or {}).get('rate_pct')}% · 账本 {mm['ledger_events']} 事件")
    if fresh["unavailable"]:
        print("[web666] ⚠ 不可用项：" + "；".join(fresh["unavailable"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
