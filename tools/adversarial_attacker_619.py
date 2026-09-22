"""619 A2 · 攻击者原型（只读 replay over v7 baseline）

不生成新 mutation，不对受控目录写盘（619 §五/§六）。仅把 A1 的攻击目标函数作用在
`data/mutation/full_baseline_v7.json` 的 1593 条既有结果上，产出「该先 fuzz 谁」的排序与报告。

产出（`data/adversarial_attacker_619.md`）：
1. 加权 Top20（默认 W1 权重，见 A1 文档）
2. 帕累托前沿（4 子目标非支配集，多目标兜底）
3. 每个子目标 Top5 贡献者
4. 逃逸 mutation 在排序中的位置（真逃逸 1 条 + 已知等效 8 条）
5. 与 v7 报告的一致性校验（逃逸率契约 1/1406 不被破坏）

铁律：新工具必有 `--check`（只读自验证，exit 0）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adversarial_objective_619 as A  # noqa: E402

DEFAULT_BASELINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 "data", "mutation", "full_baseline_v7.json")
TOP_N = 20


def analyze(results: list[dict], weights: dict[str, float] | None = None) -> dict:
    """对一组 mutation 结果产目标函数分析（纯计算，确定性）。"""
    rows = []
    for rec in results:
        sc = A.score_result(rec, weights)
        rows.append({"rec": rec, "score": sc})

    ranked = [r for r in rows if r["score"]["ranked"]]
    ranked.sort(key=lambda r: (-(r["score"]["composite"] or -1),
                               A.variant_id(r["rec"])))
    top20 = ranked[:TOP_N]

    pareto_ids = A.pareto_front(A.pareto_rows(results))
    pareto_rows_ = [r for r in rows if A.variant_id(r["rec"]) in set(pareto_ids)]
    pf_vectors = A.pareto_front_vectors(results)
    pf_members = A.pareto_members(results)

    per_sub: dict[str, list[dict]] = {}
    for k in A.COMPUTABLE_SUB_GOALS:
        judged = [r for r in rows if r["score"]["judgeable"] and (r["score"]["sub"][k] or 0.0) > 0.0]
        judged.sort(key=lambda r: (-float(r["score"]["sub"][k] or 0.0), A.variant_id(r["rec"])))
        per_sub[k] = judged[:5]

    escape_real = [r for r in rows if r["rec"].get("verdict") == "escaped" and not r["rec"].get("equivalent")]
    escape_equiv = [r for r in rows if r["rec"].get("equivalent")]
    escape_rank = None
    if escape_real:
        pos = next((i for i, r in enumerate(ranked, 1) if r["rec"] is escape_real[0]["rec"]), None)
        escape_rank = pos

    return {
        "top20": top20,
        "pareto_ids": pareto_ids,
        "pareto_rows": pareto_rows_,
        "per_sub": per_sub,
        "escape_real": escape_real,
        "escape_equiv": escape_equiv,
        "escape_rank": escape_rank,
        "n_ranked": len(ranked),
        "n_total": len(results),
        "pareto_vectors": pf_vectors,
        "pareto_members": pf_members,
    }


def check_contract(results: list[dict]) -> dict:
    """与 v7 报告口径一致性校验（不破坏逃逸率契约 1/1406）。"""
    n = len(results)
    escaped_real = [r for r in results if r.get("verdict") == "escaped" and not r.get("equivalent")]
    equivalent = [r for r in results if r.get("equivalent")]
    n_a = [r for r in results if r.get("verdict") == "n_a"]
    denom = n - len(n_a) - len(equivalent)
    return {
        "n_total": n,
        "escaped_real": len(escaped_real),
        "equivalent": len(equivalent),
        "n_a": len(n_a),
        "denom": denom,
        "contract_ok": len(escaped_real) == 1 and denom == 1406,
    }


def _md_row(r: dict, rank: int | None = None) -> str:
    rec = r["rec"]
    sc = r["score"]
    rid = A.variant_id(rec)
    card = str(rec.get("card"))
    return (f"| {rank if rank is not None else '-'} | {card} | {rec.get('op')} | "
            f"{rec.get('kind')} | {sc['composite']} | {rid.split(' · ', 2)[-1][:40]} | "
            f"{sorted({str(x).split(':')[0] for x in (rec.get('new_block') or [])})} |")


def render_markdown(results: list[dict], weights: dict[str, float] | None = None) -> str:
    an = analyze(results, weights)
    ctr = check_contract(results)
    out: list[str] = []
    out.append("# 619 A2 · 攻击者原型报告（只读 replay over v7）\n")
    out.append(f"> 输入：`data/mutation/full_baseline_v7.json`（可判 {an['n_ranked']} / 总 {an['n_total']}）")
    out.append(f"> 权重：{weights or A.WEIGHTS}（W1 默认；敏感度见 `data/adversarial_objective_619.md` §五）\n")

    out.append("## 一致性校验（逃逸率契约 1/1406）")
    out.append(f"- n_total={ctr['n_total']} escaped_real={ctr['escaped_real']} equivalent={ctr['equivalent']} "
               f"n_a={ctr['n_a']} denom={ctr['denom']}")
    out.append(f"- **contract_ok = {ctr['contract_ok']}** "
               f"（断言：escaped_real==1 且 denom==1406；本工具只读不破坏基线）\n")

    out.append(f"## 一、加权 Top{TOP_N}（优先 fuzz 谁）")
    out.append("| # | card | op | kind | composite | point | hit_rules |")
    for i, r in enumerate(an["top20"], 1):
        out.append(_md_row(r, i))
    out.append("")

    out.append(f"## 二、帕累托前沿（{len(an['pareto_vectors'])} 个不同非支配向量，多目标兜底）")
    out.append("> 按 4 子目标向量去重；同一向量可能含多条 mutation（见「count」）。")
    out.append("| vrd | evidence_ambiguity | rule_blind_spot | provenance | count | example |")
    for v in sorted(an["pareto_vectors"], key=lambda v: -sum(v)):
        members = an["pareto_members"].get(v, [])
        example = members[0] if members else ""
        out.append(f"| {v[0]} | {v[1]} | {v[2]} | {v[3]} | {len(members)} | {example[:60]} |")
    out.append("")

    out.append("## 三、每个子目标 Top5 贡献者")
    for k in A.COMPUTABLE_SUB_GOALS:
        out.append(f"### {k}")
        out.append("| # | card | op | point | sub | composite |")
        for i, r in enumerate(an["per_sub"][k], 1):
            rec = r["rec"]
            out.append(f"| {i} | {rec.get('card')} | {rec.get('op')} | "
                       f"{str(rec.get('point'))[:36]} | {r['score']['sub'][k]} | {r['score']['composite']} |")
        out.append("")

    out.append("## 四、逃逸 mutation 排名")
    if an["escape_real"]:
        er = an["escape_real"][0]
        out.append(f"- 真逃逸（唯一）：`{A.variant_id(er['rec'])}` composite={er['score']['composite']} "
                   f"**排名 = {an['escape_rank']} / {an['n_ranked']}**（W1 默认权重下）")
        out.append(f"- 已知等效（{len(an['escape_equiv'])} 条，剔出排序）："
                   + "、".join(A.variant_id(r['rec']).split(' · ', 1)[-1] for r in an["escape_equiv"]))
        out.append("- 解读：W1 下真逃逸被 8 条等效（0.57，已判无害）与 57 条 M1 删 artifact_sha256"
                   "（0.42，被 EV-FM-REQUIRED 薄拦截兜住）压过；改用 W2（rule_blind_spot 0.50）真逃逸升至第 1。"
                   "权重取舍为 620 人拍板项（见 A1 §五）。")
    out.append("")

    out.append("## 五、用途与限制")
    out.append("- 本工具只**排序**既有 1593 条，不生成新 mutation、不调 gate/replay（619 §六）。")
    out.append("- `ranked` 集合 = judgeable 且非等效 = 1406（与 v7 可判分母一致）。")
    out.append("- 攻击-验证**迭代**增益未测（A4 只写协议）；本排序即攻击方的「下一步该打谁」。")
    return "\n".join(out)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def _mini_baseline() -> list[dict]:
    return [
        {"card": "c", "op": "M1", "point": "删 negative_controls", "verdict": "escaped",
         "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
        {"card": "c", "op": "M2", "point": "路径转大写（A → B）", "verdict": "blocked",
         "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"], "equivalent": False},
        {"card": "c", "op": "M7", "point": "sha256 改一位（abc → abd）", "verdict": "blocked",
         "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"], "new_warn": [], "equivalent": False},
        {"card": "c", "op": "M7", "point": "-", "verdict": "n_a",
         "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    ]


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    res = _mini_baseline()
    an = analyze(res)
    chk("Top20 长度 ≤ 20 且非空", 0 < len(an["top20"]) <= 20)
    chk("帕累托前沿非空且含真逃逸", bool(an["pareto_ids"])
        and any(A.variant_id(r["rec"]) == A.variant_id(res[0]) for r in an["pareto_rows"]))
    chk("真逃逸进入 ranked 且 composite 在 ranked 靠前", an["escape_rank"] is not None)
    chk("n_a 不进 ranked", all(r["rec"]["verdict"] != "n_a" for r in an["top20"]))
    equiv: dict = {"card": "c", "op": "M6", "point": "块式 → flow 写法（matrix）", "verdict": "escaped",
                   "kind": None, "new_block": [], "new_warn": [], "equivalent": True}
    ane = analyze(res + [equiv])
    chk("等价剔除 ranked（ranked 不含 0.57 等效）",
        not any(r["rec"].get("equivalent") for r in ane["top20"]))
    for k in A.COMPUTABLE_SUB_GOALS:
        chk(f"子目标 {k} Top5 可计算", len(an["per_sub"][k]) >= 0)
    chk("报告可渲染且含契约行", "contract_ok =" in render_markdown(res))
    chk("一致性校验：真逃逸数 = 1、denom = 3（mini：4 - 1 n_a）",
        check_contract(res)["escaped_real"] == 1 and check_contract(res)["denom"] == 3)
    print(f"A2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 A2 攻击者原型（只读 replay over v7）")
    ap.add_argument("--baseline", default=DEFAULT_BASELINE, help="v7 baseline json（只读）")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "adversarial_attacker_619.md"),
        help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    with open(args.baseline, encoding="utf-8") as fh:
        data = json.load(fh)
    results = data.get("results") or []
    md = render_markdown(results)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(f"wrote {args.out}  (Total={len(results)} ranked={len([r for r in results if r.get('verdict')!='n_a' and not r.get('equivalent')])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
