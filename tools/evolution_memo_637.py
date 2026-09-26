"""637 E · 进化建议书（EvolutionMemo）——"我觉得下一步该做什么"

输入：CostBenefit 的排序结果（默认 `data/637_scored.json`），
另读 `data/637_observer.json`（体检）与 `data/637_errors.json`（top 5 问题）。
输出：固定格式的 Markdown 建议书 `data/637_evolution_memo.md`，人 5 分钟读完。

**影子**：本报告只输出给人看，**不自动执行任何建议**。
`--check` 只读、不写盘、exit 0；`--report` 才落盘。
≥5 例单测（tests/test_evolution_memo_637.py）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DEFAULT_IN = os.path.join(ROOT, "data", "637_scored.json")
OBSERVER = os.path.join(ROOT, "data", "637_observer.json")
ERRORS = os.path.join(ROOT, "data", "637_errors.json")
OUT_MD = os.path.join(ROOT, "data", "637_evolution_memo.md")
OUT_JSON = os.path.join(ROOT, "data", "637_evolution_memo.json")

# 体检表（10 项）：标签 / 指标键 / 阈值显示
BODY: list[tuple[str, str, str]] = [
    ("规则数", "rules", "-"),
    ("工具数", "tools_total", "-"),
    ("测试数", "tests_total", "-"),
    ("接地率", "grounding_pct", "≥50%"),
    ("击败器覆盖率", "defeater_coverage_pct", "≥90%"),
    ("taint=true 卡数", "taint_cards", "≤5"),
    ("例外条款条目", "exception_clauses", "≤100"),
    ("观察态比例(%)", "observation_pct", "≤30%"),
    ("ahead 数", "ahead", "≤20"),
    ("pytest 失败数", "pytest_failures", "≤5"),
]
MEDALS = ["🥇", "🥈", "🥉"]


def load(path: str) -> dict[str, Any]:
    try:
        data: Any = json.loads(open(path, encoding="utf-8").read())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _status(key: str, val: Any, anomaly_keys: set[str]) -> str:
    if key in anomaly_keys:
        return "⚠️"
    if val is None:
        return "❓"
    return "✅"


def _unsure(obs: dict[str, Any], anomalies: list[dict[str, Any]]) -> list[str]:
    keys = {str(a.get("key", "")) for a in anomalies}
    out = [
        "我全部是**规则匹配**，不懂语义——建议可能答非所问。",
        "我的阈值来自 635/636 现状经验值，**未经统计校准**：我对「什么算异常」没有硬依据。",
        "我没有**跨轮记忆**——不知道上个批次已经做过什么，可能重复提建议。",
    ]
    if not obs.get("heavy", False):
        out.append("本次**未采集** pytest/ruff/mypy，我对代码健康一无所知（重指标为 ❓）。")
    if "tools_per_test" in keys:
        out.append("「工具增长 vs 测试增长」用**当前比值代理**，缺历史序列，可能误判。")
    if "observation_pct" in keys:
        out.append("观察态规则缺 known_error_rate，我只能数条数、**无法判断它们到底准不准**。")
    if "grounding_pct" in keys:
        out.append("「补实验」的成本我估不准——需多少实验、多难，我给不出真实工作量。")
    return out


def build_memo(obs: dict[str, Any], errors: dict[str, Any], scored: dict[str, Any]) -> str:
    m: dict[str, Any] = obs.get("metrics", {}) or {}
    anomalies = list(errors.get("anomalies", []) or [])
    anomaly_keys = {str(a.get("key", "")) for a in anomalies}
    top = list(scored.get("top3", []) or [])
    lines = [
        "# 阙疑进化建议书 · 自动生成", "",
        f"> 生成时间：{datetime.datetime.now().isoformat(timespec='seconds')}；"
        f"数据来源：self_observer → error_detector → candidate_generator → cost_benefit。",
        "> **影子建议**：本报告只输出给人看，人审批后才执行。", "",
        "## 系统体检（10 项指标）", "",
        "| 指标 | 当前值 | 阈值 | 状态 |", "|---|---|---|---|",
    ]
    for label, key, thr in BODY:
        val = m.get(key)
        lines.append(f"| {label} | {'—' if val is None else val} | {thr} | {_status(key, val, anomaly_keys)} |")
    lines += ["", "## 我发现的 top 5 问题", "",
              "| # | 问题 | 严重程度 | 当前值 | 阈值 |", "|---|---|---|---|---|"]
    for i, a in enumerate(anomalies, 1):
        lines.append(f"| {i} | {a.get('name')} | {a.get('severity')} | {a.get('current')} | {a.get('threshold')} |")
    if not anomalies:
        lines.append("| - | 未检出异常 | - | - | - |")
    lines += ["", "## 我建议下一步做什么", ""]
    if not top:
        lines.append("（无候选方案）")
    for i, r in enumerate(top):
        medal = MEDALS[i] if i < len(MEDALS) else f"第 {i + 1} 优先"
        lines += [f"### {medal} 第 {i + 1} 优先：{r.get('candidate')}", "",
                  f"- 为什么：{r.get('reason', '（未提供）')}",
                  f"- 做什么：{r.get('action')}",
                  f"- 成本/收益：{r.get('cost')}/{r.get('benefit')}",
                  f"- 风险：{r.get('risk_class')}（系数 {r.get('risk_factor')}）", ""]
    lines += ["## 我觉得不靠谱的地方", ""]
    for s in _unsure(obs, anomalies):
        lines.append(f"- {s}")
    lines += ["", "---", "本报告由 self_evolution_loop 自动生成 · 人审批后才执行"]
    return "\n".join(lines) + "\n"


def write_report(in_path: str, obs_path: str = OBSERVER,
                 err_path: str = ERRORS) -> dict[str, str]:
    memo = build_memo(load(obs_path), load(err_path), load(in_path))
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(memo)
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
                   "source": os.path.relpath(in_path, ROOT).replace(os.sep, "/"),
                   "sections": ["系统体检", "top 5 问题", "建议下一步", "不靠谱的地方"]},
                  fh, ensure_ascii=False, indent=2)
    return {"md": OUT_MD, "json": OUT_JSON}


def _demo() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    obs = {"heavy": True, "metrics": {"rules": 67, "tools_total": 417, "tests_total": 416,
                                      "grounding_pct": 35.8, "defeater_coverage_pct": 100.0,
                                      "taint_cards": 8, "exception_clauses": 227,
                                      "observation_rules": 67, "ahead": 9,
                                      "pytest_failures": 0}}
    errs = {"anomalies": [{"key": "grounding_pct", "name": "接地率低", "severity": "P1",
                           "current": 35.8, "threshold": 50}]}
    scored = {"top3": [{"candidate": "标记暂不使用", "reason": "低成本低风险",
                        "action": "把未接地规则标为暂不使用", "cost": "低", "benefit": "中",
                        "risk_class": "report", "risk_factor": 0.5}]}
    return obs, errs, scored


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    memo = build_memo(*_demo())
    chk("含标题", "# 阙疑进化建议书 · 自动生成" in memo)
    chk("含体检表", "系统体检（10 项指标）" in memo)
    chk("含 top5 表", "我发现的 top 5 问题" in memo)
    chk("含建议章", "我建议下一步做什么" in memo)
    chk("含奖牌标记", "🥇" in memo)
    chk("含诚实章", "我觉得不靠谱的地方" in memo)
    chk("含审批声明", "人审批后才执行" in memo)
    chk("无候选也不崩", "无候选方案" in build_memo(*_demo()[:2], {"top3": []}))
    chk("输出路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 E 进化建议书")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--in", dest="inp", default=DEFAULT_IN)
    ap.add_argument("--observer", default=OBSERVER)
    ap.add_argument("--errors", default=ERRORS)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report(args.inp, args.observer, args.errors)
        print(f"written {out['md']} {out['json']}")
        return 0
    memo = build_memo(load(args.observer), load(args.errors), load(args.inp))
    if args.json:
        print(json.dumps({"chars": len(memo)}, ensure_ascii=False))
        return 0
    print(memo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
