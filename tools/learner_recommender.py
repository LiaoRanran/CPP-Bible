#!/usr/bin/env python3
"""612 线 D · D4：基于掌握度的内容推荐原型（**只读**）。

综合「用户掌握度（learner_state）+ KC 台账（kc_inventory）」推荐下一张学习卡。
四维加权：
  1. 掌握度最低优先（权重 0.40）
  2. 前置依赖已满足（权重 0.30，**硬约束**：未满足则不推荐）
  3. 同难度递进（与已学 KC 平均难度差 ≤1，权重 0.15）
  4. 关联 MIS 多优先（学习收益大，权重 0.15）

CLI：
  python tools/learner_recommender.py            # 输出 Top 5 推荐（含各维得分与理由）
  python tools/learner_recommender.py --top <N>  # 输出 Top N
  python tools/learner_recommender.py --path      # 输出学习路径建议（拓扑序，未来 5 张）
  python tools/learner_recommender.py --check     # 自验证（exit 0=通过）

约束（spec）：只读，不修改掌握度数据或 KC 台账；推荐是「建议」；前置依赖不满足的 KC 不得推荐
（硬约束）；所有 KC 掌握度 > 0.9 时输出「已掌握」提示。

用法备注：KC 清单+依赖来自 `kc_inventory.build()`；掌握度来自 `learner_state.latest_by(store)`。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE = ROOT / "data" / "learner_state_612.jsonl"

W_MASTERY = 0.40
W_PREREQ = 0.30
W_DIFF = 0.15
W_MIS = 0.15
PREREQ_THRESHOLD = 0.5
MASTERED_THRESHOLD = 0.9


def _kc_inventory() -> dict:
    import kc_inventory as d1  # noqa: E402
    return d1.build()


def _mastery(store: Path) -> dict[str, float]:
    import learner_state as d3  # noqa: E402
    return {k[1]: r["mastery_prob"] for k, r in d3.latest_by(store).items()}


def recommend(store: Path, top_n: int = 5) -> dict:
    inv = _kc_inventory()
    kcs = inv["kcs"]
    mast = _mastery(store)
    studied = {k for k in mast}  # 有记录的 KC（已 init 即视为已纳入学习集）
    studied_diff = [k["difficulty"] for k in kcs if k["id"] in studied] or [2.0]
    avg_diff = sum(studied_diff) / len(studied_diff)
    max_mis = max((k["n_related_mis"] for k in kcs), default=1) or 1

    candidates: list[dict] = []
    for k in kcs:
        m = mast.get(k["id"], 0.1)
        # 硬约束：前置依赖必须已掌握（>0.5）
        prereqs = k["prerequisites"]
        prereq_ok = all(mast.get(p, 0.1) > PREREQ_THRESHOLD for p in prereqs)
        if not prereq_ok:
            continue
        mastery_score = 1.0 - m
        diff_term = 1.0 - min(1.0, abs(k["difficulty"] - avg_diff))
        mis_term = (k["n_related_mis"] / max_mis) if max_mis else 0.0
        score = (W_MASTERY * mastery_score + W_PREREQ * 1.0
                 + W_DIFF * diff_term + W_MIS * mis_term)
        reasons = {
            "mastery": round(m, 4), "mastery_score": round(mastery_score, 4),
            "prereq_ok": True, "prereqs": prereqs,
            "diff": k["difficulty"], "diff_term": round(diff_term, 4),
            "n_mis": k["n_related_mis"], "mis_term": round(mis_term, 4),
        }
        candidates.append({"kc": k["id"], "title": k["title"], "domain": k["domain"],
                           "difficulty": k["difficulty"], "mastery": round(m, 4),
                           "score": round(score, 4), "reasons": reasons})
    candidates.sort(key=lambda x: (-x["score"], x["kc"]))
    return {"top_n": top_n, "recommendations": candidates[:top_n],
            "avg_studied_diff": round(avg_diff, 3), "n_candidates": len(candidates)}


def learning_path(store: Path, top_n: int = 5) -> list[dict]:
    rec = recommend(store, top_n=len(_kc_inventory()["kcs"]))
    rec_ids = {r["kc"] for r in rec["recommendations"]}
    # 在推荐集 + 其（已推荐）前置的闭包上做 Kahn 拓扑排序
    inv = _kc_inventory()
    by_id = {k["id"]: k for k in inv["kcs"]}
    # 闭包：推荐集 ∪ 它们的已推荐前置
    closure = set(rec_ids)
    changed = True
    while changed:
        changed = False
        for cid in list(closure):
            for p in by_id[cid]["prerequisites"]:
                if p in rec_ids and p not in closure:
                    closure.add(p)
                    changed = True
    # 入度 = 闭包内前置数量
    indeg = {c: sum(1 for p in by_id[c]["prerequisites"] if p in closure) for c in closure}
    ready = sorted([c for c in closure if indeg[c] == 0])
    ordered: list[str] = []
    while ready:
        nxt = ready.pop(0)
        ordered.append(nxt)
        for c in closure:
            if nxt in by_id[c]["prerequisites"]:
                indeg[c] -= 1
                if indeg[c] == 0:
                    ready.append(c)
    return [{"kc": c, "title": by_id[c]["title"], "difficulty": by_id[c]["difficulty"],
             "mastery": round(_mastery(store).get(c, 0.1), 4),
             "prereqs": by_id[c]["prerequisites"]} for c in ordered[:top_n]]


def render(rec: dict) -> str:
    L = ["# 612 D4 · 基于掌握度的内容推荐（原型 · 只读）", "",
         f"> 候选 KC 数（前置已满足）：**{rec['n_candidates']}** ｜ 已学平均难度 "
         f"{rec['avg_studied_diff']}", "", "## Top 推荐", "",
         "| 排名 | KC | 领域 | 难度 | 掌握度 | 综合分 | 理由 |", "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rec["recommendations"], 1):
        rs = r["reasons"]
        reason = (f"掌握{mastery_pct(r['mastery'])}·前置✓·难度差{diff_gap(rs['diff'], rec['avg_studied_diff'])}"
                  f"·MIS{rs['n_mis']}")
        L.append(f"| {i} | `{r['kc']}` | {r['domain']} | {r['difficulty']} | "
                 f"{mastery_pct(r['mastery'])} | {r['score']} | {reason} |")
    L += ["", "> 四维加权：掌握度最低 0.40 / 前置满足 0.30（硬约束）/ 同难度递进 0.15 / 关联MIS多 0.15。",
          "> 推荐为「建议」，非最优学习路径；前置依赖未达 0.5 的 KC 一律不推荐。"]
    return "\n".join(L) + "\n"


def mastery_pct(m: float) -> str:
    return f"{m*100:.0f}%"


def diff_gap(d: int, avg: float) -> str:
    g = d - avg
    return f"+{g:.1f}" if g >= 0 else f"{g:.1f}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 D4 · 基于掌握度的内容推荐（原型）")
    ap.add_argument("--top", type=int, default=5, help="输出 Top N")
    ap.add_argument("--path", action="store_true", help="输出学习路径建议")
    ap.add_argument("--store", default=None, help="测试注入：掌握度 jsonl 路径")
    ap.add_argument("--check", action="store_true", help="自验证")
    a = ap.parse_args(argv)
    store = Path(a.store) if a.store else DEFAULT_STORE

    # 所有 KC 掌握度 > 0.9 ⇒ 已掌握提示
    mast = _mastery(store)
    inv = _kc_inventory()
    if mast and all(v > MASTERED_THRESHOLD for v in mast.values()) and len(mast) >= inv["total_kc"]:
        print("[D4] 所有 KC 已掌握（掌握度均 > 0.9），建议复习或进入下一阶段。")
        return 0

    if a.check:
        problems: list[str] = []
        rec = recommend(store, top_n=5)
        if not rec["recommendations"]:
            problems.append("至少应有 1 张推荐卡（前置已满足的 KC 应非空）")
        # 硬约束：被推荐的 KC 前置必须已满足
        for r in rec["recommendations"]:
            for p in r["reasons"]["prereqs"]:
                if mast.get(p, 0.1) <= PREREQ_THRESHOLD:
                    problems.append(f"推荐了前置未满足的 KC：{r['kc']} 的前置 {p}")
        # --path 不应抛错
        try:
            learning_path(store, 5)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"learning_path 异常：{exc}")
        if problems:
            print("[D4] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print(f"[D4] ✅ 自验证通过：候选 {rec['n_candidates']} / 推荐 "
              f"{len(rec['recommendations'])} / 硬约束（前置>0.5）生效")
        return 0

    if a.path:
        for step, item in enumerate(learning_path(store, a.top), 1):
            unmet = [p for p in item["prereqs"] if mast.get(p, 0.1) <= PREREQ_THRESHOLD]
            note = f"（前置未达 0.5：{unmet}）" if unmet else ""
            print(f"{step}. `{item['kc']}` {item['title']} · 难度{item['difficulty']} · "
                  f"掌握{mastery_pct(item['mastery'])} {note}")
        return 0

    rec = recommend(store, top_n=a.top)
    print(render(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
