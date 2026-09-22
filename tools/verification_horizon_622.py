"""622 E1 · Verification Horizon 测量工具（雷7）

定义见 `data/verification_horizon_definition_622.md`：
> **Verification Horizon = 验证器能够可靠处理的最大攻击复杂度**

四个复杂度维度（加权 0.25/0.30/0.20/0.25）：
语法 / 语义 / 证据 / 规则，合成分数 0–100；按 20 分一档分桶；
**Horizon = 检出率仍 ≥ 阈值（默认 0.5）的最高桶**。

输入：沙箱实跑的判决结果（`blocked/escaped/neutral/detected_nonblock/infra_error`）
     + 对应 mutation 列表（取 op / attack_type / 目标卡类型）。

**诚实声明**：复杂度是**启发式代理**（按算子类型映射），不是 AST/语义精确度量；
检出率依赖本仓严格 `escaped` 口径 ⇒ Horizon 可能偏乐观。详见定义文档 §五。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

WEIGHTS = {"syntax": 0.25, "semantic": 0.30, "evidence": 0.20, "rule": 0.25}
DETECT_THRESHOLD = 0.5
BAND = 20

# 算子 → (语法, 语义) 代理分
OP_SYNTAX = {"M1": 0.2, "M6": 0.3, "M5": 0.3, "M2": 0.5, "M3": 0.5,
             "M7": 0.6, "M4": 0.6, "M8": 0.7, "M9": 0.8}
OP_SEMANTIC = {"M6": 0.3, "M1": 0.4, "M2": 0.4, "M5": 0.5, "M8": 0.5,
               "M7": 0.6, "M4": 0.7, "M3": 0.8, "M9": 0.9}

R2 = os.path.join(ROOT, "data", "mutation_sandbox_run_622_results.json")
R3 = os.path.join(ROOT, "data", "mutation_sandbox_run_622_round2_results.json")
M2 = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")
M3 = os.path.join(ROOT, "data", "mutation", "new_mutations_622_round2.jsonl")


def _content(m: dict) -> dict:
    try:
        return json.loads(m.get("content") or "null") or {}
    except ValueError:
        return {}


def rule_complexity(n_rules: int) -> float:
    if n_rules <= 0:
        return 0.0
    if n_rules == 1:
        return 0.3
    if n_rules == 2:
        return 0.6
    return 1.0


def complexity(row: dict, mutation: dict) -> dict:
    """单条 mutation 的四维复杂度 + 合成分数（0–100）。"""
    c = _content(mutation)
    op = str(c.get("op") or "")
    card = str(row.get("card") or c.get("target_card") or "")
    n_rules = len(set((row.get("new_block_rules") or [])
                      + (row.get("new_nonblock_rules") or [])
                      + (row.get("lost_rules") or [])))
    ev = 1.0 if op == "M9" else (0.7 if card.startswith("evidence/") else 0.3)
    dims = {
        "syntax": OP_SYNTAX.get(op, 0.5),
        "semantic": OP_SEMANTIC.get(op, 0.5),
        "evidence": ev,
        "rule": rule_complexity(n_rules),
    }
    score = round(100 * sum(WEIGHTS[k] * dims[k] for k in WEIGHTS), 2)
    return {**dims, "complexity_score": score, "n_rules": n_rules, "op": op}


def band_of(score: float) -> str:
    lo = min(int(score // BAND) * BAND, 80)
    return f"{lo}-{lo + BAND}"


def is_detected(verdict: str) -> bool | None:
    """检出判定：blocked=检出；escaped=漏判；neutral=未击发；infra_error 不计入。"""
    if verdict == "infra_error":
        return None
    return verdict == "blocked"


def measure(rows: list[dict], mutations_by_id: dict,
            threshold: float = DETECT_THRESHOLD) -> dict:
    """计算复杂度分布 + 分桶检出率 + Horizon。"""
    scored = []
    for r in rows:
        m = mutations_by_id.get(r.get("mutation_id")) or {}
        cx = complexity(r, m)
        scored.append({**r, **cx})

    bands: dict[str, dict] = {}
    for s in scored:
        det = is_detected(s.get("verdict"))
        b = bands.setdefault(band_of(s["complexity_score"]),
                             {"n": 0, "applicable": 0, "blocked": 0, "escaped": 0,
                              "neutral": 0, "detected_nonblock": 0})
        b["n"] += 1
        if det is None:
            continue
        b["applicable"] += 1
        if det:
            b["blocked"] += 1
        elif s.get("verdict") == "escaped":
            b["escaped"] += 1
        elif s.get("verdict") == "neutral":
            b["neutral"] += 1
        elif s.get("verdict") == "detected_nonblock":
            b["detected_nonblock"] += 1

    for b in bands.values():
        b["detect_rate"] = round(b["blocked"] / b["applicable"], 4) if b["applicable"] else None

    horizon = None
    for key in sorted(bands, key=lambda k: int(k.split("-")[0])):
        dr = bands[key]["detect_rate"]
        if dr is not None and dr >= threshold:
            horizon = key
    return {
        "bands": dict(sorted(bands.items(), key=lambda kv: int(kv[0].split("-")[0]))),
        "horizon_band": horizon,
        "horizon_score": int(horizon.split("-")[1]) if horizon else 0,
        "threshold": threshold,
        "total": len(scored),
        "applicable": sum(b["applicable"] for b in bands.values()),
        "scored": scored,
    }


def load_rounds() -> tuple[list[dict], dict]:
    rows: list[dict] = []
    by_id: dict[str, dict] = {}
    for res_p, mut_p in ((R2, M2), (R3, M3)):
        if os.path.exists(res_p):
            rows.extend(json.load(open(res_p, encoding="utf-8"))["rows"])
        if os.path.exists(mut_p):
            for ln in open(mut_p, encoding="utf-8"):
                if ln.strip():
                    m = json.loads(ln)
                    by_id[m.get("mutation_id")] = m
    return rows, by_id


def render(res: dict) -> str:
    o = ["# 622 E1 · Verification Horizon 测量\n"]
    o.append(f"> 样本 {res['total']} 条（可施加 {res['applicable']}）· "
             f"检出阈值 {res['threshold']}\n")
    o.append("## 一、复杂度分桶检出率\n")
    o.append("| 复杂度桶 | 条数 | 可施加 | blocked | escaped | neutral | nonblock | 检出率 |")
    for k, b in res["bands"].items():
        o.append(f"| {k} | {b['n']} | {b['applicable']} | {b['blocked']} | {b['escaped']} | "
                 f"{b['neutral']} | {b['detected_nonblock']} | {b['detect_rate']} |")
    o.append("")
    o.append("## 二、Horizon\n")
    o.append(f"- **Horizon 桶 = {res['horizon_band']}**"
             f"（≈ 复杂度 ≤ **{res['horizon_score']}**）")
    o.append(f"- 含义：复杂度超过该值后，检出率跌破 {res['threshold']} ⇒ 可能漏判")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("权重和为 1.0", round(sum(WEIGHTS.values()), 10) == 1.0)
    chk("规则复杂度单调", rule_complexity(1) < rule_complexity(2) < rule_complexity(3))
    chk("规则复杂度 0 条 = 0", rule_complexity(0) == 0.0)

    row = {"mutation_id": "x", "card": "atoms/a.md", "verdict": "blocked",
           "new_block_rules": ["R1"]}
    mut = {"mutation_id": "x", "content": json.dumps({"op": "M1", "target_card": "atoms/a.md"})}
    cx = complexity(row, mut)
    chk("四维齐全", set(cx) >= {"syntax", "semantic", "evidence", "rule", "complexity_score"})
    chk("分数在 0-100", 0 <= cx["complexity_score"] <= 100)

    chk("band_of 分桶", band_of(0) == "0-20" and band_of(85) == "80-100")
    chk("is_detected：blocked=真", is_detected("blocked") is True)
    chk("is_detected：escaped=假", is_detected("escaped") is False)
    chk("is_detected：infra_error=None", is_detected("infra_error") is None)

    rows = [{"mutation_id": "a", "card": "atoms/a.md", "verdict": "blocked",
             "new_block_rules": ["R1"]},
            {"mutation_id": "b", "card": "atoms/a.md", "verdict": "escaped"}]
    by = {"a": {"mutation_id": "a", "content": json.dumps({"op": "M1"})},
          "b": {"mutation_id": "b", "content": json.dumps({"op": "M9"})}}
    res = measure(rows, by)
    chk("样本数正确", res["total"] == 2)
    chk("可施加数正确", res["applicable"] == 2)
    chk("Horizon 为字符串或 None", res["horizon_band"] is None or "-" in res["horizon_band"])
    chk("报告可渲染", "Verification Horizon" in render(res))
    print(f"E1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 E1 Verification Horizon 测量")
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--json", dest="json_out", help="结果 JSON 输出")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    rows, by_id = load_rounds()
    res = measure(rows, by_id)
    md = render(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  horizon={res['horizon_band']}")
    else:
        print(md)
    if args.json_out:
        slim = {k: v for k, v in res.items() if k != "scored"}
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(slim, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
