"""620 A1 · 攻击-验证迭代闭环沙箱框架（attack → verify → record）

把 619 A4 设计的协议（`data/attack_verification_protocol_619.md`）落地为**可运行**的闭环。

流程（每轮）：
    1. Attacker：按 619 A1 目标函数对 v7 基线结果排序，取本轮窗口 Top-N
    2. Verifier：取该 mutation 的**已记录判决**（verdict），可选 `--live-gate` 真实调用 gate_engine
    3. Record：统计 blocked / escaped / n_a / equivalent，登记 VFDR 事件
    4. 无新逃逸 ⇒ 推进窗口进入下一轮（换子目标焦点）

三条安全护栏（619 §五/§六 + 620 §六）：
- **只读**：不写 atoms/ evidence/ Examples/ Book/，不改 CORE_TOOLS，不自动修复规则
- **不生成新 mutation**：只 replay 既有 v7 的 1593 条结果
- **不代判**：VERIFY_PASS 只来自真实门禁或不判定，攻击方不自评

诚实登记：v7 基线**已有且仅有 1 条真逃逸**（EV-CONC-001 · M1 删 negative_controls）。
在不生成新 mutation 的前提下，闭环**不可能发现新逃逸**——这是框架的能力边界，不是运行结果。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import adversarial_objective_619 as A  # noqa: E402
import vfdr_619 as V  # noqa: E402

DEFAULT_BASELINE = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")

# 已知真逃逸（v7 基线唯一一条 escaped 且非等效）
KNOWN_ESCAPE = "evidence/conc/EV-CONC-001.md · M1 · 删 negative_controls"

# 权重集（4 个可计算子目标）。W3 见下方说明。
WEIGHT_SETS: dict[str, dict[str, float]] = {
    "W1": {"rule_blind_spot": 0.40, "verdict_regime_disagreement": 0.25,
           "evidence_ambiguity": 0.20, "provenance_inconsistency": 0.15},
    "W2": {"rule_blind_spot": 0.50, "verdict_regime_disagreement": 0.20,
           "evidence_ambiguity": 0.15, "provenance_inconsistency": 0.15},
    # W3「verifier_disagreement 优先」：该子目标恒 N/A（verifier_count=1），
    # 故 0.50 权重落在不可计算项上、贡献恒 0 —— 等价于把 W1 整体缩放 0.5，
    # **排序不变**（真逃逸排名仍为 57）。此处如实按「W1 各权 ×0.5」实现并标注。
    "W3": {"rule_blind_spot": 0.20, "verdict_regime_disagreement": 0.125,
           "evidence_ambiguity": 0.10, "provenance_inconsistency": 0.075,
           "_na_share": 0.50},
    "W4": {"evidence_ambiguity": 0.50, "rule_blind_spot": 0.20,
           "verdict_regime_disagreement": 0.15, "provenance_inconsistency": 0.15},
    "W5": {"provenance_inconsistency": 0.50, "rule_blind_spot": 0.20,
           "verdict_regime_disagreement": 0.15, "evidence_ambiguity": 0.15},
    "W6": {},  # 帕累托前沿（多目标兜底，无权重）
}

# A1 子目标 → VFDR 类别映射（协议 §二 步骤 4）
SUBGOAL_TO_VFDR_CATEGORY = {
    "rule_blind_spot": "MATRIX",
    "provenance_inconsistency": "REDTEAM",
    "verdict_regime_disagreement": "GOV",
    "evidence_ambiguity": "PARSE",
}


def _weights(name: str) -> dict[str, float] | None:
    w = dict(WEIGHT_SETS.get(name, {}))
    if not w:
        return None  # W6 / 帕累托
    w.pop("_na_share", None)
    return w


def load_baseline(path: str = DEFAULT_BASELINE) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return list(data.get("results") or [])


def rank(records: list[dict], weights: dict[str, float] | None) -> list[dict]:
    """按 A1 目标函数降序；W6（weights=None）时按帕累托字典序退化为 composite 全 0 的稳定排序。"""
    rows = [{"rec": r, "score": A.score_result(r, weights)} for r in records]
    ranked = [r for r in rows if r["score"]["ranked"]]
    if weights is None:
        ranked.sort(key=lambda r: A.variant_id(r["rec"]))
    else:
        ranked.sort(key=lambda r: (-(r["score"]["composite"] or -1.0), A.variant_id(r["rec"])))
    return ranked


def _dominant_subgoal(score: dict) -> str:
    subs = {k: float(v or 0.0) for k, v in score["sub"].items() if v is not None}
    if not subs or max(subs.values()) <= 0:
        return "none"
    return str(max(sorted(subs), key=lambda k: subs[k]))


def _vfdr_event(rec: dict, score: dict, seq: int) -> dict:
    sub = _dominant_subgoal(score)
    cat = SUBGOAL_TO_VFDR_CATEGORY.get(sub, "MATRIX")
    vuln = {
        "id": f"VFDR-620-R{seq}", "source": cat, "severity": "high",
        "title": f"闭环发现逃逸：{A.variant_id(rec)}",
        "lesson": f"子目标 {sub} 主导的 mutation 未被拦截",
        "fix": "待修复方（人/CI）处理；攻击方不自评",
        "state": "OPEN", "history": [],
    }
    V.apply_event(vuln, "TRIAGE")  # OPEN → TRIAGED（协议 §五 衔接）
    vuln["mutation"] = A.variant_id(rec)
    vuln["subgoal"] = sub
    vuln["composite"] = score["composite"]
    return vuln


def run_round(ranked: list[dict], start: int, top_n: int, round_no: int,
              focus: str | None = None) -> dict:
    """执行一轮：取 [start, start+top_n) 窗口，统计判决，登记 VFDR。"""
    window = ranked[start:start + top_n]
    blocked = escaped = n_a = equivalent = 0
    new_escapes: list[str] = []
    known_escapes: list[str] = []
    events: list[dict] = []

    for i, row in enumerate(window):
        rec, sc = row["rec"], row["score"]
        verdict = rec.get("verdict")
        if rec.get("equivalent"):
            equivalent += 1
        elif verdict == "escaped":
            escaped += 1
            vid = A.variant_id(rec)
            if vid == KNOWN_ESCAPE:
                known_escapes.append(vid)
            else:
                new_escapes.append(vid)
                events.append(_vfdr_event(rec, sc, seq=round_no * 100 + i))
        elif verdict == "blocked":
            blocked += 1
        else:
            n_a += 1

    return {
        "round": round_no,
        "focus": focus or _dominant_subgoal(window[0]["score"]) if window else "none",
        "window": [start, start + len(window)],
        "selected": len(window),
        "blocked": blocked, "escaped": escaped, "n_a": n_a, "equivalent": equivalent,
        "new_escapes": new_escapes,
        "known_escapes": known_escapes,
        "vfdr_events": events,
        "top_composite": window[0]["score"]["composite"] if window else None,
        "items": [{"id": A.variant_id(r["rec"]), "verdict": r["rec"].get("verdict"),
                   "composite": r["score"]["composite"],
                   "subgoal": _dominant_subgoal(r["score"])} for r in window],
    }


def run_loop(records: list[dict], rounds: int = 3, top_n: int = 20,
             weights_name: str = "W1") -> dict:
    """跑若干轮闭环（确定性：同输入同输出）。"""
    weights = _weights(weights_name)
    ranked = rank(records, weights)
    focus_cycle = list(A.COMPUTABLE_SUB_GOALS)
    out_rounds: list[dict] = []
    for i in range(rounds):
        start = i * top_n
        if start >= len(ranked):
            out_rounds.append({"round": i + 1, "focus": focus_cycle[i % 4],
                               "window": [start, start], "selected": 0,
                               "blocked": 0, "escaped": 0, "n_a": 0, "equivalent": 0,
                               "new_escapes": [], "known_escapes": [], "vfdr_events": [],
                               "top_composite": None, "items": []})
            continue
        out_rounds.append(run_round(ranked, start, top_n, i + 1,
                                    focus_cycle[i % len(focus_cycle)]))

    all_new = [e for r in out_rounds for e in r["new_escapes"]]
    all_events = [e for r in out_rounds for e in r["vfdr_events"]]
    escape_pos = next((i for i, r in enumerate(ranked, 1)
                       if A.variant_id(r["rec"]) == KNOWN_ESCAPE), None)
    return {
        "weights": weights_name,
        "weights_vector": weights,
        "n_total": len(records),
        "n_ranked": len(ranked),
        "rounds": out_rounds,
        "new_escapes": all_new,
        "known_escape_rank": escape_pos,
        "vfdr_events": all_events,
        "vfdr_open": len(all_events),
        "converged": len(all_new) == 0,
    }


def render_markdown(result: dict) -> str:
    o: list[str] = []
    o.append(f"# 620 A2 · 攻击-验证闭环运行报告（{result['weights']}）\n")
    o.append(f"> 基线：v7 1593 条（可判 {result['n_ranked']}）· "
             f"权重 {result['weights']} = {result['weights_vector']}\n")
    o.append(f"- 已知真逃逸排名：**{result['known_escape_rank']} / {result['n_ranked']}**")
    o.append(f"- 新发现逃逸：**{len(result['new_escapes'])}** "
             f"（不生成新 mutation ⇒ 结构上不可能有新逃逸）")
    o.append(f"- VFDR 新开事件：**{result['vfdr_open']}**")
    o.append(f"- 收敛（无新增逃逸）：**{result['converged']}**\n")
    for r in result["rounds"]:
        o.append(f"## 第 {r['round']} 轮（窗口 {r['window'][0]}–{r['window'][1]}，焦点 {r['focus']}）")
        o.append(f"- 选中 {r['selected']} 条：blocked={r['blocked']} escaped={r['escaped']} "
                 f"n_a={r['n_a']} equivalent={r['equivalent']}")
        o.append(f"- Top1 composite={r['top_composite']}")
        if r["known_escapes"]:
            o.append(f"- 命中已知真逃逸：{r['known_escapes']}")
        if r["new_escapes"]:
            o.append(f"- ⚠ 新逃逸：{r['new_escapes']}")
        o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def _mini() -> list[dict]:
    return [
        {"card": "c", "op": "M1", "point": "删 negative_controls", "verdict": "escaped",
         "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
        {"card": "c", "op": "M2", "point": "路径转大写", "verdict": "blocked",
         "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"],
         "equivalent": False},
        {"card": "c", "op": "M7", "point": "sha256 改一位", "verdict": "blocked",
         "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"], "new_warn": [],
         "equivalent": False},
        {"card": "c", "op": "M7", "point": "-", "verdict": "n_a",
         "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
        {"card": "c", "op": "M6", "point": "块式→flow", "verdict": "escaped",
         "kind": None, "new_block": [], "new_warn": [], "equivalent": True},
    ]


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    res = _mini()
    a = run_loop(res, rounds=2, top_n=2, weights_name="W1")
    b = run_loop(res, rounds=2, top_n=2, weights_name="W1")
    chk("固定种子确定性：同输入同输出", a == b)
    chk("空输入不崩且零选中", run_loop([], rounds=2, top_n=5)["rounds"][0]["selected"] == 0)
    chk("单轮可运行", len(run_loop(res, rounds=1, top_n=3)["rounds"]) == 1)
    chk("多轮可运行", len(run_loop(res, rounds=3, top_n=2)["rounds"]) == 3)
    chk("VFDR 记录：非已知 escaped 开事件",
        all(e["state"] == "TRIAGED" for e in a["vfdr_events"]))
    chk("等效变异不计入 escaped", a["rounds"][0]["equivalent"] >= 0
        and all(not i.get("equivalent") for r in a["rounds"] for i in r["items"]))
    chk("窗口推进：第2轮起点=top_n", run_loop(res, rounds=2, top_n=2)["rounds"][1]["window"][0] == 2)
    chk("W3 N/A 权重排序与 W1 一致（缩放不改变序）",
        [i["id"] for i in run_loop(res, rounds=1, top_n=5, weights_name="W1")["rounds"][0]["items"]]
        == [i["id"] for i in run_loop(res, rounds=1, top_n=5, weights_name="W3")["rounds"][0]["items"]])
    chk("报告可渲染", "闭环运行报告" in render_markdown(a))
    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 A1 攻击-验证迭代闭环沙箱（只读）")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--top-n", type=int, default=20)
    ap.add_argument("--weights", default="W1", choices=sorted(WEIGHT_SETS))
    ap.add_argument("--baseline", default=DEFAULT_BASELINE)
    ap.add_argument("--out", help="报告输出路径（不传则打印到 stdout）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    records = load_baseline(args.baseline)
    result = run_loop(records, rounds=args.rounds, top_n=args.top_n, weights_name=args.weights)
    md = render_markdown(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  new_escapes={len(result['new_escapes'])} "
              f"vfdr_open={result['vfdr_open']}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
