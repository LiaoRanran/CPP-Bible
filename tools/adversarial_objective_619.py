"""619 A1 · 攻击目标函数 v1（可计算代理，纯标准库、只读、确定性）

定义与权重理由见 `data/adversarial_objective_619.md`；本文件只做**计算**。

输入：`data/mutation/full_baseline_v7.json` 的**单条** `results[]` 记录（dict）
输出：`score_result(rec) -> dict`
    {"sub": {...}, "composite": float|None, "judgeable": bool,
     "known_equivalent": bool, "ranked": bool, "severity": str}

三条硬约束（619 §六）：只读（--check 亦不写盘）、不 import mutation_fuzz、纯函数（无随机/时间/IO）。

子目标口径（逐条可复算，全部来自 v7 既有字段）：
- `verifier_disagreement`：**N/A**（verifier_count=1）⇒ 权重 0，不计分
- `verdict_regime_disagreement`（**替身**，≠ 多 verifier 分歧）：
  `kind == "warn_only"`（严格口径不拦、treated 口径才拦）⇒ 1.0；`strict` / `escaped` ⇒ 0.0
- `evidence_ambiguity`：`equivalent` 0.60 + `op ∈ {M4,M6}` 0.25 + `replay_skipped` 非空 0.15，截断 1.0
- `rule_blind_spot`：`escaped` 1.0；`blocked` 且命中规则**全属结构性 GENERIC 集** 0.6；
  `blocked` 且恰好命中 1 条规则 0.3；其余 0.0
- `provenance_inconsistency`：按 `point` 关键词分级（sha256/signed_by 1.0、run_match 0.8、
  路径类 0.7、artifact/fixture 0.6、否则 0.0）

双计避免：`warn_only` 记录 `new_block` 为空 ⇒ `rule_blind_spot` 记 0.0，其风险只由
`verdict_regime_disagreement` 承担。
"""
from __future__ import annotations

import argparse
import json
import sys

DECLARED_SUB_GOALS: tuple[str, ...] = (
    "verifier_disagreement",
    "verdict_regime_disagreement",
    "evidence_ambiguity",
    "rule_blind_spot",
    "provenance_inconsistency",
)
COMPUTABLE_SUB_GOALS: tuple[str, ...] = (
    "verdict_regime_disagreement",
    "evidence_ambiguity",
    "rule_blind_spot",
    "provenance_inconsistency",
)
WEIGHTS: dict[str, float] = {
    "verdict_regime_disagreement": 0.25,
    "evidence_ambiguity": 0.20,
    "rule_blind_spot": 0.40,
    "provenance_inconsistency": 0.15,
}
GENERIC_RULES: frozenset[str] = frozenset({
    "EV-FM-REQUIRED", "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING",
    "EV-ID-UNIQUE", "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE",
})
PARSE_OPS: frozenset[str] = frozenset({"M4", "M6"})
SEVERITY_BANDS: tuple[tuple[float, str], ...] = (
    (0.60, "critical"), (0.40, "high"), (0.20, "medium"), (0.0, "low"),
)
PROVENANCE_TIERS: tuple[tuple[str, float], ...] = (
    ("sha256", 1.0), ("signed_by", 1.0),
    ("run_match", 0.8),
    ("路径", 0.7), ("\\", 0.7), ("Examples/", 0.7),
    ("artifact", 0.6), ("fixture", 0.6),
)


def weights_sum() -> float:
    return round(sum(WEIGHTS.values()), 10)


def severity(composite: float | None) -> str:
    if composite is None:
        return "not_judgeable"
    for lo, name in SEVERITY_BANDS:
        if composite >= lo:
            return name
    return "none"


def _rule_ids(rec: dict) -> set[str]:
    return {str(r).split(":")[0] for r in (rec.get("new_block") or [])}


def sub_verdict_regime_disagreement(rec: dict) -> float | None:
    """严格口径 vs treated 口径的判决分歧（替身指标，不是多 verifier 分歧）。"""
    kind = rec.get("kind")
    if kind == "warn_only":
        return 1.0
    if kind in ("strict", "escaped") or rec.get("verdict") == "escaped":
        return 0.0
    return None


def sub_evidence_ambiguity(rec: dict) -> float:
    s = 0.0
    if rec.get("equivalent"):
        s += 0.60
    if rec.get("op") in PARSE_OPS:
        s += 0.25
    if rec.get("replay_skipped"):
        s += 0.15
    return round(min(1.0, s), 4)


def sub_rule_blind_spot(rec: dict) -> float:
    verdict = rec.get("verdict")
    if verdict == "escaped":
        return 1.0
    if verdict != "blocked":
        return 0.0
    ids = _rule_ids(rec)
    if not ids:
        return 0.0
    if ids <= GENERIC_RULES:
        return 0.6
    if len(ids) == 1:
        return 0.3
    return 0.0


def sub_provenance_inconsistency(rec: dict) -> float:
    point = str(rec.get("point") or "")
    for kw, tier in PROVENANCE_TIERS:
        if kw in point:
            return tier
    return 0.0


def sub_verifier_disagreement(rec: dict) -> None:
    """当前恒为 N/A：verifier_count = 1 ⇒ 无"多个 verifier"可分歧。"""
    return None


def score_result(rec: dict, weights: dict[str, float] | None = None) -> dict:
    """把单条 mutation 结果映射为目标函数分数（纯函数、确定性）。

    `weights` 省略时用 `WEIGHTS`（提议默认权重）；传入其它权重用于 A1 的**敏感度分析**
    （子目标分数 `sub` 与权重无关，只有 `composite` / `severity` 随之变化）。
    """
    w = weights or WEIGHTS
    subs: dict[str, float | None] = {
        "verifier_disagreement": sub_verifier_disagreement(rec),  # type: ignore[func-returns-value]  # 该子评分按设计恒 N/A（返回 None），此处显式取 None
        "verdict_regime_disagreement": sub_verdict_regime_disagreement(rec),
        "evidence_ambiguity": sub_evidence_ambiguity(rec),
        "rule_blind_spot": sub_rule_blind_spot(rec),
        "provenance_inconsistency": sub_provenance_inconsistency(rec),
    }
    judgeable = rec.get("verdict") != "n_a"
    if judgeable:
        composite: float | None = round(
            sum(float(w.get(k, 0.0)) * float(subs[k] or 0.0) for k in COMPUTABLE_SUB_GOALS), 6)
    else:
        composite = None
    known_equivalent = bool(rec.get("equivalent"))
    return {
        "sub": subs,
        "composite": composite,
        "judgeable": judgeable,
        "known_equivalent": known_equivalent,
        "ranked": bool(judgeable and not known_equivalent),
        "severity": severity(composite),
    }


def variant_id(rec: dict) -> str:
    """v7 无稳定 mutation_id ⇒ 用 `(card, op, point)` 三元组作标识（只读派生）。"""
    return f"{rec.get('card')} · {rec.get('op')} · {rec.get('point')}"


def pareto_rows(records: list[dict]) -> list[dict]:
    """把 mutation 记录包装成 (记录, 分数) 行，供 `pareto_front` / A2 报告使用。"""
    return [{"rec": r, "score": score_result(r)} for r in records]


def pareto_front(rows: list[dict]) -> list[str]:
    """4 个可计算子目标上的非支配集（最大化语义），返回 variant_id 列表（字典序）。

    `rows` 每项形如 `{"rec": <mutation 结果>, "score": score_result(rec)}`（`pareto_rows()` 产出）。
    """
    keys = COMPUTABLE_SUB_GOALS
    vecs = [(variant_id(r.get("rec", r)),
             tuple(float(r["score"]["sub"][k] or 0.0) for k in keys)) for r in rows]
    front: list[str] = []
    for i, (vi, a) in enumerate(vecs):
        dom = False
        for j, (_vj, b) in enumerate(vecs):
            if i == j:
                continue
            if all(y >= x for x, y in zip(a, b)) and any(y > x for x, y in zip(a, b)):
                dom = True
                break
        if not dom:
            front.append(vi)
    return sorted(set(front))


def pareto_front_vectors(records: list[dict]) -> list[tuple[float, ...]]:
    """去重后的非支配 4-向量集合（A2 报告用，避免重复向量爆炸）。

    与 `pareto_front` 同一支配定义，但按「子目标向量」去重返回 —— 409 个重复点坍缩为少量
    不同向量，便于人类阅读。注意：等效变异体的向量会支配真逃逸向量（它同时拉高歧义与盲区），
    故真逃逸向量**不在**前沿里 —— 这正是 A1 §五「W1 低估盲区」的交叉印证，属预期。"""
    keys = COMPUTABLE_SUB_GOALS
    vecs = sorted({(tuple(float(score_result(r)["sub"][k] or 0.0) for k in keys)) for r in records})
    front: list[tuple[float, ...]] = []
    for i, a in enumerate(vecs):
        dominated = False
        for j, b in enumerate(vecs):
            if i == j:
                continue
            if all(y >= x for x, y in zip(a, b)) and any(y > x for x, y in zip(a, b)):
                dominated = True
                break
        if not dominated:
            front.append(a)
    return front


def pareto_members(records: list[dict]) -> dict[tuple[float, ...], list[str]]:
    """向量 → 该向量上的 variant_id 列表（供报告展示每个前沿点有多少 mutation）。"""
    keys = COMPUTABLE_SUB_GOALS
    members: dict[tuple[float, ...], list[str]] = {}
    for r in records:
        v = tuple(float(score_result(r)["sub"][k] or 0.0) for k in keys)
        members.setdefault(v, []).append(variant_id(r))
    return members


def summarize(records: list[dict]) -> dict:
    """按算子/按严重度聚合（A2 报告数据面；只读、确定性）。"""
    by_op: dict[str, dict] = {}
    sev: dict[str, int] = {}
    for rec in records:
        sc = score_result(rec)
        bucket = by_op.setdefault(str(rec.get("op")), {
            "n": 0, "judged": 0, "sum": 0.0,
            "sub_sum": {k: 0.0 for k in COMPUTABLE_SUB_GOALS}})
        bucket["n"] += 1
        sev[sc["severity"]] = sev.get(sc["severity"], 0) + 1
        if sc["judgeable"]:
            bucket["judged"] += 1
            bucket["sum"] += float(sc["composite"] or 0.0)
            for k in COMPUTABLE_SUB_GOALS:
                bucket["sub_sum"][k] += float(sc["sub"][k] or 0.0)
    for b in by_op.values():
        n = b["judged"] or 1
        b["mean_composite"] = round(b["sum"] / n, 6)
        b["mean_sub"] = {k: round(v / n, 6) for k, v in b["sub_sum"].items()}
        del b["sum"], b["sub_sum"]
    return {"by_operator": by_op, "by_severity": dict(sorted(sev.items()))}


# ── 自检（只读，不写盘；exit 0 = 通过）──────────────────────────────────────────
_SYNTHETIC: tuple[dict, ...] = (
    {"card": "c", "op": "M1", "point": "删 negative_controls",
     "verdict": "escaped", "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M2", "point": "路径转大写（A → B）",
     "verdict": "blocked", "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"],
     "equivalent": False},
    {"card": "c", "op": "M7", "point": "sha256 改一位（abc → abd）",
     "verdict": "blocked", "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"],
     "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M7", "point": "sha256 改一位（abc → abd）",
     "verdict": "n_a", "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("权重和为 1.0", weights_sum() == 1.0)
    chk("声明的 5 个子目标中 4 个可计算", len(DECLARED_SUB_GOALS) == 5 and len(COMPUTABLE_SUB_GOALS) == 4)

    a, b, c, d = (score_result(r) for r in _SYNTHETIC)
    chk("确定性：同输入同输出", score_result(_SYNTHETIC[0]) == a)
    chk("真逃逸排第一（高于 warn_only 路径变形）", a["composite"] > b["composite"])
    chk("verifier_disagreement 恒 N/A", a["sub"]["verifier_disagreement"] is None)
    chk("n_a 不进分母（composite is None）", d["composite"] is None and not d["judgeable"])
    chk("n_a 严重度 = not_judgeable", d["severity"] == "not_judgeable")
    chk("warn_only ⇒ 口径分歧 1.0", b["sub"]["verdict_regime_disagreement"] == 1.0)
    chk("warn_only ⇒ 盲区不双计 0.0", b["sub"]["rule_blind_spot"] == 0.0)
    chk("sha256 篡改触溯源 1.0", c["sub"]["provenance_inconsistency"] == 1.0)
    chk("真逃逸 ⇒ 盲区 1.0", a["sub"]["rule_blind_spot"] == 1.0)
    chk("severe 分级可用", a["severity"] in ("high", "critical", "medium", "low"))

    front = pareto_front(pareto_rows(list(_SYNTHETIC)))
    chk("pareto 前沿非空且含真逃逸", bool(front) and variant_id(_SYNTHETIC[0]) in front)
    summed = summarize(list(_SYNTHETIC))
    chk("summarize 覆盖 2 个算子", set(summed["by_operator"]) == {"M1", "M2", "M7"})

    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 A1 攻击目标函数（只读计算）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    ap.add_argument("--baseline", help="可选：对 full_baseline_v7.json 跑一遍并打印摘要（只读）")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()
    if args.baseline:
        with open(args.baseline, encoding="utf-8") as fh:
            data = json.load(fh)
        recs = data.get("results") or []
        print(json.dumps(summarize(recs), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
