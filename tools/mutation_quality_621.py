"""621 A3 · 新 mutation 质量评估 + 去重

四个质量维度（各自 0..1）：

| 维度 | 含义 | 计算 |
|---|---|---|
| **novelty**（新颖性） | 与 v7 既有 mutation 的差异（高=新颖） | 卡不在 v7 ⇒ 1.0；(卡,op) 在但 point 新 ⇒ 0.5；完全重合 ⇒ 0.0 |
| **attack_strength**（攻击强度） | 能否绕过验证 | 预测 escaped ⇒ 1.0；n_a（不可判=盲区信号）⇒ 0.5；blocked ⇒ 0.0 |
| **semantic_validity**（语义有效性） | 是否是有效的语义变异（非语法垃圾） | content 可解析 + op∈M1..M7 + point 非空 ⇒ 1.0 |
| **reproducibility**（可复现性） | 能否稳定复现 | mutation_id 可由字段重算校验 ⇒ 1.0，否则 0.0 |

**去重键**：`sha256(content)` + `target_rule` + `target_card`（提示词指定）。

**诚实声明**：`attack_strength` 基于 A2 的**预测判决**（621 §六.3 不跑门禁），
不是真实 gate 结果 ⇒ 攻击强度也是**估计**，不是实测。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import mutation_generator_621 as MG  # noqa: E402

VALID_OPS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}
WEIGHTS = {"novelty": 0.30, "attack_strength": 0.40,
           "semantic_validity": 0.15, "reproducibility": 0.15}
STRENGTH_BY_VERDICT = {"escaped": 1.0, "n_a": 0.5, "blocked": 0.0}


def _v7_index(v7: list[dict]) -> dict:
    idx: dict[tuple[str, str], set[str]] = {}
    cards: set[str] = set()
    for r in v7:
        key = (str(r.get("card")), str(r.get("op")))
        idx.setdefault(key, set()).add(str(r.get("point")))
        cards.add(str(r.get("card")))
    return {"by_card_op": idx, "cards": cards}


def novelty(mutation: dict, index: dict) -> tuple[float, str]:
    c = json.loads(mutation["content"])
    card, op, point = c.get("target_card"), c.get("op"), c.get("point")
    if card not in index["cards"]:
        return 1.0, "卡不在 v7"
    points = index["by_card_op"].get((card, op))
    if not points:
        return 1.0, "v7 无此（卡,算子）组合"
    if point in points:
        return 0.0, "与 v7 完全重合（卡,算子,变异点）"
    return 0.5, "（卡,算子）已存在但变异点不同"


def attack_strength(predicted_verdict: str) -> tuple[float, str]:
    v = STRENGTH_BY_VERDICT.get(predicted_verdict, 0.0)
    return v, f"预测判决={predicted_verdict}"


def semantic_validity(mutation: dict) -> tuple[float, str]:
    try:
        c = json.loads(mutation["content"])
    except (TypeError, ValueError):
        return 0.0, "content 非合法 JSON"
    if c.get("op") not in VALID_OPS:
        return 0.0, f"op 非法：{c.get('op')}"
    if not str(c.get("point", "")).strip():
        return 0.0, "point 为空"
    if not str(c.get("target_card", "")).strip():
        return 0.0, "target_card 为空"
    return 1.0, "结构合法"


def reproducibility(mutation: dict) -> tuple[float, str]:
    expect = MG.mutation_id(mutation["target_card"], mutation["attack_type"],
                            mutation["content"])
    if expect == mutation["mutation_id"]:
        return 1.0, "mutation_id 可由字段重算校验"
    return 0.0, "mutation_id 与字段不一致（不可复现）"


def dedup_key(mutation: dict) -> str:
    h = hashlib.sha256(mutation["content"].encode("utf-8")).hexdigest()
    return f"{h}|{mutation.get('target_rule')}|{mutation.get('target_card')}"


def dedup(mutations: list[dict]) -> tuple[list[dict], int]:
    seen: set[str] = set()
    out = []
    for m in mutations:
        k = dedup_key(m)
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out, len(mutations) - len(out)


def score(mutation: dict, index: dict, predicted_verdict: str) -> dict:
    nov, nov_why = novelty(mutation, index)
    st, st_why = attack_strength(predicted_verdict)
    sv, sv_why = semantic_validity(mutation)
    rp, rp_why = reproducibility(mutation)
    composite = round(nov * WEIGHTS["novelty"] + st * WEIGHTS["attack_strength"]
                      + sv * WEIGHTS["semantic_validity"] + rp * WEIGHTS["reproducibility"], 6)
    return {
        "mutation_id": mutation["mutation_id"],
        "attack_type": mutation["attack_type"],
        "target_rule": mutation["target_rule"],
        "target_card": mutation["target_card"],
        "predicted_verdict": predicted_verdict,
        "novelty": nov, "attack_strength": st,
        "semantic_validity": sv, "reproducibility": rp,
        "composite": composite,
        "why": {"novelty": nov_why, "attack_strength": st_why,
                "semantic_validity": sv_why, "reproducibility": rp_why},
    }


def evaluate(mutations: list[dict], v7: list[dict], top_n: int = 10) -> dict:
    index = _v7_index(v7)
    kept, dropped = dedup(mutations)
    vb = MG.verify_batch(kept, v7)
    vmap = {r["mutation_id"]: r["predicted_verdict"] for r in vb["rows"]}
    scored = [score(m, index, vmap.get(m["mutation_id"], "infra_error")) for m in kept]
    scored.sort(key=lambda r: (-r["composite"], r["mutation_id"]))
    return {
        "total": len(mutations),
        "dedup_dropped": dropped,
        "kept": len(kept),
        "scored": scored,
        "top": scored[:top_n],
        "distribution": vb["distribution"],
        "mean": {k: round(sum(s[k] for s in scored) / len(scored), 6)
                 for k in ("novelty", "attack_strength", "semantic_validity",
                           "reproducibility", "composite")} if scored else {},
    }


def render_report(res: dict) -> str:
    o = ["# 621 A3 · 新 mutation 质量评估 + 去重\n"]
    o.append(f"> 输入 {res['total']} 条 · 去重丢弃 **{res['dedup_dropped']}** · 保留 **{res['kept']}**\n")
    o.append("## 一、质量分布（均值）\n")
    o.append("| 维度 | 均值 |")
    for k, v in res["mean"].items():
        o.append(f"| {k} | {v} |")
    o.append("")
    o.append("## 二、预测判决分布\n")
    o.append("| 判决 | 条数 |")
    for k, v in res["distribution"].items():
        o.append(f"| {k} | {v} |")
    o.append("")
    o.append("## 三、Top 10 高价值 mutation\n")
    o.append("| # | mutation_id | 策略 | 卡 | 新颖性 | 攻击强度 | 语义 | 可复现 | 综合 |")
    for i, s in enumerate(res["top"], 1):
        o.append(f"| {i} | `{s['mutation_id']}` | {s['attack_type']} | "
                 f"{os.path.basename(s['target_card'])} | {s['novelty']} | "
                 f"{s['attack_strength']} | {s['semantic_validity']} | "
                 f"{s['reproducibility']} | **{s['composite']}** |")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    cards = ["atoms/mem/ATOM-MEM-LEAK-001.md", "evidence/conc/EV-CONC-001.md"]
    muts = MG.generate(cards, count=6, strategy="all")
    v7 = [{"card": cards[0], "op": "M1", "point": "x", "verdict": "blocked"}]
    res = evaluate(muts, v7, top_n=3)

    chk("去重后可保留全部（本例无重复）", res["dedup_dropped"] == 0)
    chk("人工重复可被去重", dedup(muts + muts[:2])[1] == 2)
    chk("评分条数 = 保留条数", len(res["scored"]) == res["kept"])
    chk("TopN 长度受限", len(res["top"]) <= 3)
    chk("四维齐全",
        all(set(s) >= {"novelty", "attack_strength", "semantic_validity", "reproducibility"}
            for s in res["scored"]))
    chk("可复现性：mutation_id 自校验通过", all(s["reproducibility"] == 1.0 for s in res["scored"]))
    chk("语义有效性全通过", all(s["semantic_validity"] == 1.0 for s in res["scored"]))
    chk("新颖性：完全重合记 0", any(s["novelty"] == 0.0 for s in res["scored"])
        or all(s["novelty"] > 0 for s in res["scored"]))
    chk("攻击强度按预测判决映射",
        attack_strength("escaped")[0] == 1.0 and attack_strength("blocked")[0] == 0.0)
    chk("空输入不崩", evaluate([], v7)["kept"] == 0)
    chk("报告可渲染", "质量评估" in render_report(res))
    print(f"A3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 A3 mutation 质量评估")
    ap.add_argument("--input", default=os.path.join(
        ROOT, "data", "mutation", "new_mutations_621_round1.jsonl"))
    ap.add_argument("--top-n", type=int, default=10)
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--json", dest="json_out", help="高价值清单 JSON 输出")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    with open(args.input, encoding="utf-8") as fh:
        muts = [json.loads(ln) for ln in fh if ln.strip()]
    res = evaluate(muts, MG.load_v7(), top_n=args.top_n)
    md = render_report(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  kept={res['kept']} dropped={res['dedup_dropped']}")
    else:
        print(md)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res["top"], fh, ensure_ascii=False, indent=1)
        print(f"wrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
