"""620 A3 · 攻击目标函数权重校准实验（6 种权重对比，供人拍板）

对 619 A1 定义的 4 个可计算子目标，系统比较 6 种权重取向：

| 权重集 | 取向 | 说明 |
|---|---|---|
| W1 | 保守默认 | 619 默认（rbs 0.40） |
| W2 | rule_blind_spot 优先 | 619 校准锚定建议 |
| W3 | verifier_disagreement 优先 | **该子目标恒 N/A** ⇒ 等价于 W1 缩放，排序不变 |
| W4 | evidence_ambiguity 优先 | 解析/判别力取向 |
| W5 | provenance_inconsistency 优先 | 溯源/供应链取向 |
| W6 | 帕累托前沿 | 无权重，多目标兜底（无单一排名） |

每套权重给出：Top20 清单、真逃逸排名、与 W1 的 Top20 重叠率、攻击强度分布。

**诚实声明**：本工具只提供数据，**不替人选择权重**。最终权重是人拍板项。

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

import adversarial_loop_620 as LOOP  # noqa: E402
import adversarial_objective_619 as A  # noqa: E402

DEFAULT_BASELINE = LOOP.DEFAULT_BASELINE
KNOWN = LOOP.KNOWN_ESCAPE
WEIGHT_SETS = LOOP.WEIGHT_SETS


def _clean_weights(name: str) -> dict[str, float] | None:
    w = dict(WEIGHT_SETS.get(name, {}))
    w.pop("_na_share", None)
    return w or None


def distribution(ranked: list[dict]) -> dict:
    vals = [float(r["score"]["composite"] or 0.0) for r in ranked]
    if not vals:
        return {"n": 0, "mean": 0.0, "max": 0.0, "min": 0.0, "gt_0_4": 0}
    mean = sum(vals) / len(vals)
    return {
        "n": len(vals),
        "mean": round(mean, 6),
        "max": round(max(vals), 6),
        "min": round(min(vals), 6),
        "gt_0_4": sum(1 for v in vals if v > 0.4),
    }


def pareto_membership(records: list[dict]) -> dict:
    """W6：真逃逸向量是否在帕累托前沿上。"""
    keys = A.COMPUTABLE_SUB_GOALS
    target = None
    for r in records:
        if A.variant_id(r) == KNOWN:
            target = tuple(float(A.score_result(r)["sub"][k] or 0.0) for k in keys)
            break
    front = A.pareto_front_vectors(records)
    return {
        "on_front": bool(target is not None and target in set(front)),
        "front_size": len(front),
        "target_vector": target,
    }


def calibrate(records: list[dict], top_n: int = 20) -> dict:
    out: dict[str, dict] = {}
    w1_top: set[str] | None = None

    for name in sorted(WEIGHT_SETS):
        if name == "W6":
            pm = pareto_membership(records)
            out[name] = {
                "weights": None, "orient": "帕累托前沿（多目标）",
                "ranked_n": len([r for r in records
                                 if A.score_result(r)["ranked"]]),
                "top20": [], "escape_rank": None, "overlap_with_w1": None,
                "dist": {}, "pareto": pm,
            }
            continue

        weights = _clean_weights(name)
        ranked = LOOP.rank(records, weights)
        ids = [A.variant_id(r["rec"]) for r in ranked]
        top20 = ids[:top_n]
        if w1_top is None and name == "W1":
            w1_top = set(top20)
        rank_pos = next((i for i, v in enumerate(ids, 1) if v == KNOWN), None)
        # 注意：w1_top 可能是空 set（空输入），必须用 `is not None` 判定，不能用真值判定
        overlap = (len(set(top20) & w1_top) / top_n) if w1_top is not None else None
        out[name] = {
            "weights": weights,
            "orient": _orient(name),
            "ranked_n": len(ranked),
            "top20": top20,
            "escape_rank": rank_pos,
            "overlap_with_w1": None if name == "W1" else round(overlap, 4),
            "dist": distribution(ranked),
            "pareto": None,
        }
    return out


def _orient(name: str) -> str:
    return {
        "W1": "保守默认（rule_blind_spot 0.40）",
        "W2": "rule_blind_spot 优先（0.50）",
        "W3": "verifier_disagreement 优先（N/A ⇒ 等价 W1 缩放）",
        "W4": "evidence_ambiguity 优先（0.50）",
        "W5": "provenance_inconsistency 优先（0.50）",
        "W6": "帕累托前沿（多目标兜底）",
    }.get(name, name)


def render_markdown(result: dict) -> str:
    o: list[str] = []
    o.append("# 620 A3 · 攻击目标函数权重校准实验\n")
    o.append("> 6 种权重取向对比；**最终权重选择是人拍板项**，本工具只给数据。\n")
    o.append("## 一、总览对比\n")
    o.append("| 权重集 | 取向 | 可判数 | 真逃逸排名 | 与 W1 Top20 重叠率 | 均值 | 最大 | >0.4 条数 |")
    for name in sorted(result):
        r = result[name]
        er = "—（多目标无单一排名）" if r["escape_rank"] is None else r["escape_rank"]
        ov = "—（基准）" if r["overlap_with_w1"] is None else f"{r['overlap_with_w1']:.0%}"
        d = r["dist"]
        mean = d.get("mean", "—")
        o.append(f"| {name} | {r['orient']} | {r['ranked_n']} | {er} | {ov} | "
                 f"{mean} | {d.get('max', '—')} | {d.get('gt_0_4', '—')} |")
    o.append("")
    o.append("## 二、各权重 Top20 首位与真逃逸命中\n")
    for name in sorted(result):
        r = result[name]
        if name == "W6":
            p = r["pareto"]
            o.append(f"- **W6**：帕累托前沿 {p['front_size']} 个非支配向量；"
                     f"真逃逸向量在前沿上 = **{p['on_front']}**")
            continue
        first = r["top20"][0] if r["top20"] else "—"
        o.append(f"- **{name}**：Top1 = `{first}`；真逃逸排名 **{r['escape_rank']} / {r['ranked_n']}**")
    o.append("")
    o.append("## 三、结论与建议（供人拍板）")
    o.append("- 若目标是**最快打到已知真逃逸** ⇒ 选 W2（第 1 名）。")
    o.append("- 若目标是**不过度拟合已知逃逸、保守稳健** ⇒ 选 W1（619 默认）。")
    o.append("- W3 因 verifier_disagreement 恒 N/A 而等价于 W1，**不能**实现「验证器分歧优先」。")
    o.append("- W6 无单一排名，适合做多目标兜底与 trade-off 展示，不适合做主排序。")
    o.append("- **最终权重由人拍板**，本工具不代决。")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    res = LOOP._mini()
    cal = calibrate(res, top_n=3)
    chk("6 种权重全覆盖", set(cal) == {"W1", "W2", "W3", "W4", "W5", "W6"})
    chk("W1 Top20 长度 ≤ top_n", len(cal["W1"]["top20"]) <= 3)
    chk("W1 重叠率为基准（None）", cal["W1"]["overlap_with_w1"] is None)
    chk("W3 与 W1 排序一致（N/A 权重不改变序）", cal["W3"]["top20"] == cal["W1"]["top20"])
    chk("分布统计含均值/最大/最小", set(cal["W1"]["dist"]) >= {"mean", "max", "min"})
    chk("W6 为帕累托且无排名", cal["W6"]["escape_rank"] is None
        and cal["W6"]["pareto"] is not None)
    chk("确定性：同输入同输出", calibrate(res, top_n=3) == cal)
    chk("报告可渲染", "权重校准实验" in render_markdown(cal))
    print(f"A3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 A3 攻击目标函数权重校准（只读）")
    ap.add_argument("--baseline", default=DEFAULT_BASELINE)
    ap.add_argument("--top-n", type=int, default=20)
    ap.add_argument("--out", help="报告输出路径（不传则打印）")
    ap.add_argument("--json", dest="json_out", help="结果 JSON 输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    with open(args.baseline, encoding="utf-8") as fh:
        records = list((json.load(fh).get("results")) or [])
    result = calibrate(records, top_n=args.top_n)
    md = render_markdown(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}")
    else:
        print(md)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)
        print(f"wrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
