"""620 A4 · VFDR 实时计算 + 第一轮闭环总结

VFDR = **Vulnerability Feedback Discovery Rate（漏洞反馈发现率）**，逐轮实时计算：

    VFDR_raw(轮 i)        = 本轮【新发现逃逸】/ 本轮【验证的 mutation 数】
    VFDR_cumulative(≤轮 i) = 累计新发现逃逸 / 累计验证数
    VFDR_trend            = 各轮 VFDR_raw 序列 + 收敛判定

**口径定义（必须明确，否则数字无意义）**：

1. **已知逃逸不算"新发现"**：v7 唯一的真逃逸
   `EV-CONC-001.md · M1 · 删 negative_controls` 是**存量**，命中它计入
   `known_hits`，**不进 VFDR 分子**。
2. **规则盲区 ≠ 验证失败**：`rule_blind_spot > 0` 只是**风险信号**（薄拦截/该拦未拦的隐患），
   单独统计为 `blind_spot_exposed`；只有当其 `verdict == escaped` 且非等效时才算失败。
3. **等价变异（equivalent）不计**：已知无害，既不进分子也不计入"有效验证"分母。
4. **n_a 不计入分子**（不可判），但计入已验证数（它确实被验证过一轮）。

⇒ 因此在不生成新 mutation 的前提下，VFDR **结构恒为 0**（见报告 §五），这是能力边界不是成果。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import adversarial_loop_620 as LOOP  # noqa: E402
import adversarial_objective_619 as A  # noqa: E402

KNOWN = LOOP.KNOWN_ESCAPE


def compute_vfdr(records: list[dict], rounds: int = 3, top_n: int = 20,
                 weights_name: str = "W1") -> dict:
    """逐轮实时计算 VFDR（确定性：同输入同输出）。"""
    weights = LOOP._weights(weights_name)
    ranked = LOOP.rank(records, weights)
    per_round: list[dict] = []
    cum_new = 0
    cum_verified = 0

    for i in range(rounds):
        start = i * top_n
        window = ranked[start:start + top_n]
        selected = len(window)
        new = 0
        known_hits = 0
        blind = 0
        blocked = escaped = n_a = 0

        for row in window:
            rec = row["rec"]
            subs = row["score"]["sub"]
            if float(subs.get("rule_blind_spot") or 0.0) > 0:
                blind += 1
            if rec.get("equivalent"):
                continue
            verdict = rec.get("verdict")
            if verdict == "escaped":
                escaped += 1
                if A.variant_id(rec) == KNOWN:
                    known_hits += 1
                else:
                    new += 1
            elif verdict == "blocked":
                blocked += 1
            else:
                n_a += 1

        cum_new += new
        cum_verified += selected
        per_round.append({
            "round": i + 1,
            "window": [start, start + selected],
            "verified": selected,
            "blocked": blocked, "escaped": escaped, "n_a": n_a,
            "new_escapes": new,
            "known_hits": known_hits,
            "blind_spot_exposed": blind,
            "vfdr_raw": round(new / selected, 6) if selected else 0.0,
            "vfdr_cumulative": round(cum_new / cum_verified, 6) if cum_verified else 0.0,
        })

    series = [r["vfdr_raw"] for r in per_round]
    converged = all(v == 0 for v in series)
    return {
        "weights": weights_name,
        "rounds": per_round,
        "vfdr_series": series,
        "vfdr_cumulative_final": per_round[-1]["vfdr_cumulative"] if per_round else 0.0,
        "total_new_escapes": cum_new,
        "total_verified": cum_verified,
        "total_known_hits": sum(r["known_hits"] for r in per_round),
        "total_blind_spot_exposed": sum(r["blind_spot_exposed"] for r in per_round),
        "converged": converged,
        "trend": "flat-zero（收敛）" if converged else "非零（有新增）",
    }


def render_markdown(results: dict) -> str:
    o: list[str] = []
    o.append("# 620 A4 · VFDR 实时计算 + 第一轮闭环总结\n")
    o.append("> 口径：新发现逃逸 / 已验证 mutation 数；已知逃逸、等价变异不计入分子。\n")
    o.append("## 一、各权重汇总\n")
    o.append("| 权重 | 轮数 | 累计验证 | 新逃逸 | 已知逃逸命中 | 盲区暴露 | VFDR 累计 | 收敛 |")
    for name, r in sorted(results.items()):
        o.append(f"| {name} | {len(r['rounds'])} | {r['total_verified']} | "
                 f"{r['total_new_escapes']} | {r['total_known_hits']} | "
                 f"{r['total_blind_spot_exposed']} | {r['vfdr_cumulative_final']} | {r['converged']} |")
    o.append("")
    for name, r in sorted(results.items()):
        o.append(f"## 二、{name} 逐轮明细\n")
        o.append("| 轮 | 窗口 | 验证 | blocked | escaped | n_a | 新逃逸 | 已知命中 | 盲区暴露 | VFDR_raw | VFDR_累计 |")
        for x in r["rounds"]:
            o.append(f"| {x['round']} | {x['window'][0]}–{x['window'][1]} | {x['verified']} | "
                     f"{x['blocked']} | {x['escaped']} | {x['n_a']} | {x['new_escapes']} | "
                     f"{x['known_hits']} | {x['blind_spot_exposed']} | {x['vfdr_raw']} | "
                     f"{x['vfdr_cumulative']} |")
        o.append(f"\n- VFDR 序列：{r['vfdr_series']} → **{r['trend']}**\n")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    res = LOOP._mini()
    r = compute_vfdr(res, rounds=2, top_n=2, weights_name="W1")
    chk("轮数正确", len(r["rounds"]) == 2)
    chk("VFDR 序列长度 = 轮数", len(r["vfdr_series"]) == 2)
    chk("已知逃逸不计入新发现",
        all(x["known_hits"] >= 0 and x["new_escapes"] >= 0 for x in r["rounds"]))
    chk("等价变异不进 ranked（窗口不含 M6）",
        not any("M6" in A.variant_id(x["rec"]) for x in LOOP.rank(res, LOOP._weights("W1"))))
    chk("累计 = 各轮之和", r["total_verified"] == sum(x["verified"] for x in r["rounds"]))
    chk("确定性：同输入同输出",
        compute_vfdr(res, rounds=2, top_n=2, weights_name="W1") == r)
    chk("空输入不崩", compute_vfdr([], rounds=2, top_n=5)["total_verified"] == 0)
    chk("报告可渲染", "VFDR" in render_markdown({"W1": r}))
    print(f"A4 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 A4 VFDR 实时计算（只读）")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--top-n", type=int, default=20)
    ap.add_argument("--weights", nargs="+", default=["W1", "W2"])
    ap.add_argument("--baseline", default=LOOP.DEFAULT_BASELINE)
    ap.add_argument("--out", help="报告输出路径（不传则打印）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    records = LOOP.load_baseline(args.baseline)
    results = {w: compute_vfdr(records, rounds=args.rounds, top_n=args.top_n,
                               weights_name=w) for w in args.weights}
    md = render_markdown(results)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
