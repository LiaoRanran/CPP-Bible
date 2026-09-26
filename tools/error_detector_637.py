"""637 B · 误差检测器（ErrorDetector）——从体检报告里挑 top 5 异常

输入：SelfObserver 的 JSON（默认 `data/637_observer.json`）。
输出：**top 5 异常/瓶颈**，每个含 名称/当前值/阈值/严重程度/为什么是问题。

**纯规则检测，不调 LLM**。`--check` 只读、不写盘、exit 0；`--report` 才落盘。
≥5 例单测（tests/test_error_detector_637.py）。
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

DEFAULT_IN = os.path.join(ROOT, "data", "637_observer.json")
OUT_JSON = os.path.join(ROOT, "data", "637_errors.json")
OUT_MD = os.path.join(ROOT, "data", "637_errors.md")

SEV_RANK: dict[str, int] = {"P0": 3, "P1": 2, "P2": 1}
TOP_N = 5


def _exceed(cur: float, thr: float, direction: str) -> float:
    if thr == 0:
        return float(cur)
    if direction == "lt":
        return (thr - cur) / thr
    return (cur - thr) / thr


def _anomaly(name: str, key: str, current: Any, threshold: Any,
             direction: str, severity: str, why: str) -> dict[str, Any]:
    return {
        "name": name, "key": key, "current": current, "threshold": threshold,
        "direction": direction, "severity": severity, "why": why,
        "exceedance": round(_exceed(float(current), float(threshold), direction), 4),
    }


def detect(obs: dict[str, Any]) -> list[dict[str, Any]]:
    m: dict[str, Any] = obs.get("metrics", {}) or {}
    found: list[dict[str, Any]] = []

    g = m.get("grounding_pct")
    if isinstance(g, (int, float)) and g < 50:
        found.append(_anomaly("接地率低", "grounding_pct", g, 50, "lt", "P1",
                              "未接地规则缺外部实验/标准支撑，验证结论无法回溯到事实。"))

    op = m.get("observation_pct")
    if isinstance(op, (int, float)) and op > 30:
        found.append(_anomaly("观察态规则多", "observation_pct", op, 30, "gt", "P1",
                              "规则缺 known_error_rate，无法校准，判决可信度未量化。"))

    pf = m.get("pytest_failures")
    if isinstance(pf, (int, float)) and pf > 5:
        found.append(_anomaly("pytest 失败多", "pytest_failures", pf, 5, "gt", "P0",
                              "回归测试红意味着既有不变量被破坏，是最高的正确性风险。"))

    ruff = m.get("ruff_errors")
    mypy = m.get("mypy_errors")
    if isinstance(ruff, int) and isinstance(mypy, int) and (ruff + mypy) > 0:
        found.append(_anomaly("静态检查有错误", "static_errors", ruff + mypy, 0, "gt", "P1",
                              "ruff/mypy 报错会掩盖真实缺陷，且污染「全绿」契约。"))

    tc = m.get("taint_cards")
    if isinstance(tc, (int, float)) and tc > 5:
        found.append(_anomaly("taint=true 卡多", "taint_cards", tc, 5, "gt", "P1",
                              "高污染卡一旦判错会连锁影响多条下游卡，需优先复核。"))

    ec = m.get("exception_clauses")
    if isinstance(ec, (int, float)) and ec > 100:
        found.append(_anomaly("例外条款多", "exception_clauses", ec, 100, "gt", "P2",
                              "例外越多，规则的实际约束越弱，口子可能被漂移利用。"))

    ah = m.get("ahead")
    if isinstance(ah, (int, float)) and ah > 20:
        found.append(_anomaly("ahead 过多", "ahead", ah, 20, "gt", "P2",
                              "大量未 push 的 commit 增加丢失/冲突风险，也拖慢他人同步。"))

    tt, ts = m.get("tools_total"), m.get("tests_total")
    if isinstance(tt, int) and isinstance(ts, int) and ts > 0:
        ratio = tt / ts
        if ratio > 1.05:
            found.append(_anomaly("工具增长快于测试增长", "tools_per_test", round(ratio, 3),
                                  1.05, "gt", "P2",
                                  "工具多而测试少，新增能力可能缺回归护栏（代理指标，缺历史序列）。"))

    found.sort(key=lambda a: (-SEV_RANK.get(str(a["severity"]), 0), -float(a["exceedance"])))
    return found[:TOP_N]


def load_observer(path: str) -> dict[str, Any]:
    try:
        data: Any = json.loads(open(path, encoding="utf-8").read())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_report(in_path: str) -> dict[str, str]:
    obs = load_observer(in_path)
    anomalies = detect(obs)
    out = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": os.path.relpath(in_path, ROOT).replace(os.sep, "/"),
        "heavy": bool(obs.get("heavy", False)),
        "n_detected": len(anomalies),
        "n_reported": len(anomalies),
        "anomalies": anomalies,
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    lines = ["# 637 · 误差检测报告（ErrorDetector 自动生成）", "",
             f"> 来源：{out['source']}；检出异常：**{out['n_detected']}** 项（报告 top {TOP_N}）。", "",
             "| # | 问题 | 严重 | 当前值 | 阈值 | 为什么是问题 |", "|---|---|---|---|---|---|"]
    for i, a in enumerate(anomalies, 1):
        lines.append(f"| {i} | {a['name']} | {a['severity']} | {a['current']} | "
                     f"{a['threshold']} | {a['why']} |")
    if not anomalies:
        lines.append("| - | 未检出异常 | - | - | - | 阈值内 |")
    lines += ["", "---", "本报告由 error_detector_637 自动生成 · 只读检测，不改系统。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def _bad_obs() -> dict[str, Any]:
    return {"metrics": {"grounding_pct": 35.8, "observation_pct": 100.0, "pytest_failures": 9,
                        "ruff_errors": 2, "mypy_errors": 1, "taint_cards": 8,
                        "exception_clauses": 227, "ahead": 30, "tools_total": 417,
                        "tests_total": 400}}


def _good_obs() -> dict[str, Any]:
    return {"metrics": {"grounding_pct": 90.0, "observation_pct": 5.0, "pytest_failures": 0,
                        "ruff_errors": 0, "mypy_errors": 0, "taint_cards": 0,
                        "exception_clauses": 10, "ahead": 3, "tools_total": 100,
                        "tests_total": 100}}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    bad = detect(_bad_obs())
    chk("坏样本检出 5 项", len(bad) == 5)
    chk("P0 排第一", bad[0]["severity"] == "P0")
    good = detect(_good_obs())
    chk("好样本 0 异常", len(good) == 0)
    chk("接地边界：49.9 命中", len(detect({"metrics": {"grounding_pct": 49.9}})) == 1)
    chk("接地边界：50 不命中", len(detect({"metrics": {"grounding_pct": 50.0}})) == 0)
    chk("缺重指标不误报", len(detect({"metrics": {"ruff_errors": None, "mypy_errors": None,
                                                  "pytest_failures": None,
                                                  "grounding_pct": 90.0,
                                                  "observation_pct": 1.0,
                                                  "taint_cards": 0,
                                                  "exception_clauses": 1,
                                                  "ahead": 1}})) == 0)
    chk("输出路径在 data 下",
        OUT_JSON.startswith(os.path.join(ROOT, "data")) and OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 B 误差检测器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--in", dest="inp", default=DEFAULT_IN)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report(args.inp)
        print(f"written {out['json']} {out['md']}")
        return 0
    anomalies = detect(load_observer(args.inp))
    if args.json:
        print(json.dumps(anomalies, ensure_ascii=False, indent=2))
        return 0
    for a in anomalies:
        print(f"{a['severity']} {a['name']}: {a['current']} (阈值 {a['threshold']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
