#!/usr/bin/env python3
"""615 C1 · warn 不增锁机制（**新建独立工具，不改 golden_lock.py / 不改现有基线**）。

背景（_arch_v19/03/08）：warn 被 golden 锁**周期性采纳为 legacy**（136→186），27 条毒样例豁免全 legacy
⇒ Goodhart 漂移。本工具设计并实现「warn 不增锁」：

  1. **新出现的 warn 不自动进入 golden 基线**；
  2. warn 须经**观察期**（默认 3 个批次）才可被考虑采纳为 legacy；
  3. 采纳为 legacy 必须**显式人审授权**（acceptance 记录），**不自动采纳**；
  4. 已采纳 legacy 必须有**到期日**（默认 10 个批次后重新评估）。

输入：`tools/golden_state.json`（acceptance 批次记录 + `warn_classify`）+ `data/metrics.jsonl`（warn 趋势）。
**不重跑 gate --check**（615 铁律）。

CLI：`--check`（自验证）/ `--report`（写报告）/ 默认打印分类。
铁律：只做**分类和提醒**；**不自动修改 golden 基线**、不自动采纳/删除任何 warn。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

GOLDEN = ROOT / "tools" / "golden_state.json"
METRICS = ROOT / "data" / "metrics.jsonl"
REPORT = ROOT / "data" / "warn_governance_615.md"

OBSERVATION_BATCHES = 3      # 观察期（批次）
EXPIRY_BATCHES = 10          # 采纳后到期（批次）

#: 五个分类桶
BUCKETS = ("new", "observation", "considerable", "adopted_legacy", "expired_reassess")
_ADOPTED_CLASSES = ("legacy", "accepted")


def load_state() -> dict:
    if not GOLDEN.is_file():
        return {}
    return cast("dict[str, Any]", json.loads(GOLDEN.read_text(encoding="utf-8")))


def batches(state: dict) -> list[dict]:
    """acceptance 批次记录（按 ts 升序；每条 = 一次采纳/分类事件）。"""
    acc = cast("list[dict[str, Any]]", state.get("accepted") or [])
    return sorted(acc, key=lambda r: str(r.get("ts") or ""))


def rule_first_seen(state: dict) -> dict[str, int]:
    """规则→**首次出现**的批次下标（在 `classify` 映射或 reason 文本中出现）。"""
    out: dict[str, int] = {}
    bs = batches(state)
    for i, rec in enumerate(bs):
        cls = rec.get("classify") or {}
        reason = str(rec.get("reason") or "")
        names = set(cls.keys())
        # reason 里出现的规则名（粗粒度；仅用于 first_seen，不用于分类）
        for rid in (state.get("warn_classify") or {}):
            if rid in reason:
                names.add(rid)
        for rid in names:
            if rid not in out:
                out[rid] = i
    return out


def classify(state: dict | None = None, observation: int = OBSERVATION_BATCHES,
             expiry: int = EXPIRY_BATCHES) -> dict[str, str]:
    """规则→桶。纯函数（可注入 state 供测试）。"""
    st = state if state is not None else load_state()
    wc: dict[str, str] = cast("dict[str, str]", st.get("warn_classify") or {})
    if not wc:
        return {}
    bs = batches(st)
    last = len(bs) - 1
    seen = rule_first_seen(st)
    out: dict[str, str] = {}
    for rid, klass in wc.items():
        idx = seen.get(rid, last)          # 未知 ⇒ 视为最新出现
        age = last - idx
        adopted = klass in _ADOPTED_CLASSES
        if adopted:
            out[rid] = "expired_reassess" if age >= expiry else "adopted_legacy"
        elif age < observation:
            out[rid] = "new" if age <= 0 else "observation"
        else:
            out[rid] = "considerable"
    return out


def approvals_ok(state: dict | None = None) -> list[str]:
    """校验：每条被采纳(legacy/accepted)的规则都能对应到一条**显式 acceptance 记录**。"""
    st = state if state is not None else load_state()
    wc: dict[str, str] = cast("dict[str, str]", st.get("warn_classify") or {})
    bs = batches(st)
    approved: set[str] = set()
    for rec in bs:
        for rid in (rec.get("classify") or {}):
            approved.add(rid)
        # 无 classify 字段的早期记录：reason 里含规则名亦视为其授权留痕
    problems: list[str] = []
    for rid, klass in wc.items():
        if klass in _ADOPTED_CLASSES and rid not in approved:
            problems.append(f"已采纳 {rid}（{klass}）缺 acceptance 记录")
    return problems


def warn_trend() -> list[dict]:
    """从 metrics.jsonl 取 gate_warn_count 趋势（若存在）。"""
    if not METRICS.is_file():
        return []
    out: list[dict] = []
    for ln in METRICS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            d = cast("dict[str, Any]", json.loads(ln))
        except ValueError:
            continue
        m = d.get("metrics") or {}
        if "gate_warn_count" in m:
            out.append({"ts": d.get("timestamp"), "warn": m.get("gate_warn_count")})
    return out


def summarize(state: dict | None = None) -> dict:
    st = state if state is not None else load_state()
    buckets = classify(st)
    counts = {b: sum(1 for v in buckets.values() if v == b) for b in BUCKETS}
    m = cast("dict[str, Any]", st.get("metrics") or {})
    return {"warn_total": m.get("warn_findings"),
            "classified_rules": len(buckets), "buckets": counts,
            "buckets_by_rule": buckets, "trend": warn_trend()}


def render(s: dict) -> str:
    b = s["buckets"]
    L = ["# 615 C1 · warn 治理（不增锁机制）", "",
         "> **只分类与提醒**；不自动修改 golden 基线、不自动采纳/删除任何 warn。"
         "不重跑 gate --check（615 铁律）。", "",
         "## 一、现状", "",
         f"- `golden_state.warn_findings` = **{s['warn_total']}**（standing baseline）；"
         f"已分类规则 **{s['classified_rules']}** 条。", "",
         "## 二、warn 分类（五桶）", "",
         "| 桶 | 规则数 |", "|---|---|",
         f"| 新出现 new | {b['new']} |",
         f"| 观察期中 observation | {b['observation']} |",
         f"| 可考虑采纳 considerable | {b['considerable']} |",
         f"| 已采纳legacy adopted_legacy | {b['adopted_legacy']} |",
         f"| 已到期需重评估 expired_reassess | {b['expired_reassess']} |", "",
         "### 逐规则", "", "| 规则 | 桶 |", "|---|---|",
         *[f"| `{rid}` | {bk} |" for rid, bk in sorted(s["buckets_by_rule"].items())],
         "", "## 三、不增锁机制设计", "",
         "1. **新出现的 warn 不自动进入 golden 基线**（永不自动采纳）；",
         f"2. warn 须经**观察期 {OBSERVATION_BATCHES} 个批次**才可被**考虑**采纳为 legacy；",
         "3. 采纳为 legacy 必须**显式人审授权**（`accepted[]` 留痕），**不自动采纳**；",
         f"4. 已采纳 legacy 有**到期日**（{EXPIRY_BATCHES} 个批次后**重新评估**，见 `expired_reassess`）。", "",
         "### 参数与理由", "",
         f"- `OBSERVATION_BATCHES = {OBSERVATION_BATCHES}`：3 批足以观察「新 warn 是否自愈」（历史多为例行漂移）；",
         f"- `EXPIRY_BATCHES = {EXPIRY_BATCHES}`：10 批后强制重评估，防 legacy 永久沉淀（Goodhart）。", "",
         "## 四、warn 趋势（metrics.jsonl）", "",
         "| 时间 | warn 数 |", "|---|---|",
         *([f"| {t['ts']} | {t['warn']} |" for t in s["trend"]] or ["| （无 metrics 记录） | — |"]),
         "", "> **重要声明**：本机制只做分类和提醒，**不自动修改 golden 基线**，"
         "**不自动采纳或删除任何 warn**；采纳/解冻均需人审授权。", "", ""]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    st = load_state()
    if not st:
        return ["golden_state.json 缺失"]
    # 1) 分类逻辑（合成）：新规则默认不采纳
    fake = {"warn_classify": {"R-NEW": "real"},
            "accepted": [{"ts": "2026-01-01", "reason": "batch0"}]}
    c = classify(fake)
    if c.get("R-NEW") != "new":
        problems.append("最新出现的规则应判 new（不自动采纳）")
    # 2) 观察期：age<3 ⇒ observation
    fake2 = {"warn_classify": {"R1": "real"},
             "accepted": [{"ts": f"2026-01-0{i}", "reason": "b", "classify": {"R1": "real"}}
                          for i in range(1, 3)]}
    if classify(fake2).get("R1") != "observation":
        problems.append("age<观察期应判 observation")
    # 3) 已采纳必须有 acceptance 记录
    fake3 = {"warn_classify": {"R2": "legacy"}, "accepted": [{"ts": "2026-01-01", "reason": "b0"}]}
    if not approvals_ok(fake3):
        problems.append("已采纳但无 acceptance 记录应报错")
    # 4) 到期检测
    fake4 = {"warn_classify": {"R3": "legacy"},
             "accepted": [{"ts": "2026-01-01", "reason": "b", "classify": {"R3": "legacy"}}]
                         + [{"ts": f"2026-02-{i:02d}", "reason": "b"} for i in range(1, 12)]}
    if classify(fake4).get("R3") != "expired_reassess":
        problems.append("age≥到期批次应判 expired_reassess")
    # 5) 真实数据：已采纳规则都有授权
    problems.extend(approvals_ok(st))
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="warn_governance",
                                 description="615 C1 warn 不增锁机制（只分类与提醒）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[C1] ❌ {p}", file=sys.stderr)
            return 1
        print("[C1] ✅ 自验证通过：新 warn 不自动采纳 / 观察期 / 已采纳须授权 / 到期检测 均一致")
        return 0
    s = summarize()
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(s), encoding="utf-8", newline="\n")
        print(f"[C1] 已写 {REPORT.relative_to(ROOT).as_posix()}")
        return 0
    print(json.dumps(s, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
