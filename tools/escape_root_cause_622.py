"""622 A3 · 新逃逸根因分析（有逃逸则根因+修复建议；0 逃逸则深度分析+策略改进）

两条分支：

**分支 1（有逃逸）** —— 对每条逃逸做 4 维根因定位：
| 维度 | 判据 |
|---|---|
| 规则盲区 | 逃逸的 `lost_rules` 为空 ⇒ 不是靠绕规则，而是规则**根本没覆盖**该字段 |
| 证据歧义 | 目标卡是 `evidence/` 且 op ∈ {M4, M6} ⇒ 解析层歧义 |
| provenance 不一致 | 逃逸项命中 `artifact`/`sha256`/路径类规则名 |
| 隐性预处理 | 逃逸的编辑目标字段属于「被规则隐性剥字段」类（如 artifact_sha256） |

**分支 2（0 逃逸，本批实际）** —— 三个"为什么 0"的量化分析：
1. **生成策略够不够强**：逐策略的"可施加率 / 被拦率"
2. **v7 是否已覆盖**：(卡, 算子) 与 v7 的重叠度
3. **gate 规则是否已足够强**：变异触发的规则分布

并给出**下一轮生成策略的改进建议**（可执行、可验证）。

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

RESULTS = os.path.join(ROOT, "data", "mutation_sandbox_run_622_results.json")
MUTS = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")

PROVENANCE_KEYWORDS = ("artifact", "sha256", "path", "canonical", "producer")
PARSE_OPS = ("M4", "M6")


def _content(m: dict) -> dict:
    try:
        return json.loads(m.get("content") or "null") or {}
    except ValueError:
        return {}


def root_cause(row: dict, mutations_by_id: dict) -> dict:
    """对有逃逸的单条做 4 维根因定位。"""
    m = mutations_by_id.get(row.get("mutation_id")) or {}
    c = _content(m)
    op = c.get("op")
    card = str(row.get("card") or "")
    lost = row.get("lost_rules") or []
    rules = " ".join(str(r) for r in (row.get("lost_rules") or []) + (row.get("new_block_rules") or []))

    dims = []
    if not lost:
        dims.append("规则盲区（并非绕规则，而是规则未覆盖该字段）")
    if card.startswith("evidence/") and op in PARSE_OPS:
        dims.append("证据歧义（解析层：恒真注入 / YAML 变形）")
    if any(k in rules.lower() for k in PROVENANCE_KEYWORDS):
        dims.append("provenance 不一致（工件/哈希/路径绑定被绕过）")
    if "sha256" in str(row.get("edit") or "").lower():
        dims.append("隐性预处理（artifact_sha256 类字段被规则剥离）")
    if not dims:
        dims.append("未归类（需人工复核）")
    return {"mutation_id": row.get("mutation_id"), "card": card, "op": op,
            "lost_rules": lost, "dimensions": dims}


def strategy_coverage(rows: list[dict], mutations_by_id: dict) -> dict:
    """逐策略：可施加率 / 被拦率 / neutral 率。"""
    out: dict[str, dict] = {}
    for r in rows:
        m = mutations_by_id.get(r.get("mutation_id")) or {}
        strat = m.get("attack_type") or r.get("attack_type") or "unknown"
        b = out.setdefault(strat, {"n": 0, "applicable": 0, "blocked": 0,
                                   "neutral": 0, "escaped": 0, "infra_error": 0})
        b["n"] += 1
        v = r.get("verdict")
        if v in b:
            b[v] += 1
        if v != "infra_error":
            b["applicable"] += 1
    for b in out.values():
        b["applicable_rate"] = round(b["applicable"] / b["n"], 4) if b["n"] else None
        b["block_rate"] = round(b["blocked"] / b["applicable"], 4) if b["applicable"] else None
    return dict(sorted(out.items()))


def v7_overlap(mutations: list[dict], v7: list[dict]) -> dict:
    pairs = {(str(r.get("card")), str(r.get("op"))) for r in v7}
    cards = {str(r.get("card")) for r in v7}
    tot = len(mutations)
    op_hit = 0
    card_hit = 0
    for m in mutations:
        c = _content(m)
        if (str(c.get("target_card")), str(c.get("op"))) in pairs:
            op_hit += 1
        if str(c.get("target_card")) in cards:
            card_hit += 1
    return {"total": tot, "card_op_overlap": op_hit, "card_overlap": card_hit,
            "card_op_overlap_rate": round(op_hit / tot, 4) if tot else None,
            "card_overlap_rate": round(card_hit / tot, 4) if tot else None}


def rule_coverage(rows: list[dict]) -> dict:
    fired: dict[str, int] = {}
    for r in rows:
        for rule in (r.get("new_block_rules") or []) + (r.get("lost_rules") or []):
            fired[rule] = fired.get(rule, 0) + 1
    return dict(sorted(fired.items(), key=lambda kv: -kv[1]))


def suggestions(cov: dict, overlap: dict, rules: dict, dist: dict) -> list[str]:
    s: list[str] = []
    bad = [k for k, v in cov.items() if (v.get("applicable_rate") or 0) < 0.8]
    if bad:
        s.append("① **生成器必须 schema-aware**：先读目标卡的 frontmatter 实际字段，再决定 op。"
                 f"当前不适用率最高的策略：{bad}（可施加率 <80%）。")
    if (overlap.get("card_op_overlap_rate") or 0) > 0.8:
        s.append("② **提高组合新颖性**：当前 (卡,算子) 与 v7 重叠 {:.0%} ⇒ "
                 "应显式排除 v7 已有的 (卡,op) 对，或引入 v7 没有的算子（M8+）。"
                 .format(overlap["card_op_overlap_rate"]))
    if not rules:
        s.append("③ **无一条变异触发新规则** ⇒ 变异没打到规则面；"
                 "应针对每条规则的**检查边界**（regex 边界值、必填 vs 空值、大小写）构造针对性变异。")
    else:
        s.append(f"③ 已有变异触发的规则：{list(rules)[:8]} ⇒ 下一轮应优先攻击**未触发**的规则。")
    if dist.get("neutral", 0) > 0:
        s.append("④ **neutral 需细分**：{} 条 neutral 既未触发 block 也未削弱检测 ⇒ "
                 "说明这些编辑（如 status→draft、恒真断言）**对规则判定无影响**，"
                 "应改用能改变规则输入语义的编辑。".format(dist["neutral"]))
    s.append("⑤ **两段式验证**：本批只跑 gate（规则层）；"
             "下一轮应叠加 replay 复算层，才能发现「规则过但复算不过」的逃逸。")
    return s


def analyze(results_path: str = RESULTS, muts_path: str = MUTS,
            v7_path: str | None = None) -> dict:
    with open(results_path, encoding="utf-8") as fh:
        res = json.load(fh)
    rows = res["rows"]
    with open(muts_path, encoding="utf-8") as fh:
        muts = [json.loads(ln) for ln in fh if ln.strip()]
    by_id = {m.get("mutation_id"): m for m in muts}

    v7: list[dict] = []
    try:
        import mutation_generator_621 as MG
        v7 = MG.load_v7(v7_path) if v7_path else MG.load_v7()
    except Exception:  # noqa: BLE001
        v7 = []

    escaped = [r for r in rows if r.get("verdict") == "escaped"]
    if escaped:
        return {"mode": "escapes", "escapes": escaped,
                "root_causes": [root_cause(r, by_id) for r in escaped]}
    cov = strategy_coverage(rows, by_id)
    overlap = v7_overlap(muts, v7)
    rules = rule_coverage(rows)
    return {"mode": "zero", "distribution": res.get("distribution", {}),
            "strategy_coverage": cov, "v7_overlap": overlap,
            "rule_coverage": rules,
            "suggestions": suggestions(cov, overlap, rules, res.get("distribution", {}))}


def render(res: dict) -> str:
    if res["mode"] == "escapes":
        o = ["# 622 A3 · 新逃逸根因分析\n", f"> 发现 **{len(res['escapes'])}** 条逃逸\n"]
        for rc in res["root_causes"]:
            o.append(f"## `{rc['mutation_id']}`（{rc['card']}）")
            o.append(f"- 算子：{rc['op']} · 丢失检测：{rc['lost_rules']}")
            o.append(f"- 根因维度：{'；'.join(rc['dimensions'])}\n")
        return "\n".join(o)

    o = ["# 622 A3 · 0 逃逸深度分析（为什么是 0）\n"]
    o.append(f"> 判决分布：{res['distribution']}\n")
    o.append("## 一、生成策略够不够强（可施加率 / 被拦率）\n")
    o.append("| 策略 | 条数 | 可施加 | 可施加率 | blocked | neutral | infra_error | 被拦率 |")
    for k, v in res["strategy_coverage"].items():
        o.append(f"| {k} | {v['n']} | {v['applicable']} | {v['applicable_rate']} | "
                 f"{v['blocked']} | {v['neutral']} | {v['infra_error']} | {v['block_rate']} |")
    o.append("")
    ov = res["v7_overlap"]
    o.append("## 二、v7 是否已覆盖这些变异\n")
    o.append(f"- (卡, 算子) 与 v7 重叠：**{ov['card_op_overlap']}/{ov['total']}"
             f"（{ov['card_op_overlap_rate']}）**")
    o.append(f"- 卡与 v7 重叠：**{ov['card_overlap']}/{ov['total']}"
             f"（{ov['card_overlap_rate']}）**\n")
    o.append("## 三、gate 规则是否已足够强（变异触发的规则）\n")
    if res["rule_coverage"]:
        o.append("| 规则 | 触发次数 |")
        for k, v in res["rule_coverage"].items():
            o.append(f"| {k} | {v} |")
    else:
        o.append("- **没有任何变异触发规则**（无新增 block、也无检测消失）")
    o.append("")
    o.append("## 四、下一轮生成策略改进建议\n")
    for s in res["suggestions"]:
        o.append(f"- {s}")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    rows = [
        {"mutation_id": "a", "card": "atoms/x.md", "verdict": "blocked",
         "new_block_rules": ["ATOM-FM-REQUIRED"], "lost_rules": []},
        {"mutation_id": "b", "card": "evidence/y.md", "verdict": "neutral",
         "new_block_rules": [], "lost_rules": []},
        {"mutation_id": "c", "card": "evidence/y.md", "verdict": "infra_error",
         "reason": "无法施加 op=M7"},
    ]
    by_id = {"a": {"mutation_id": "a", "attack_type": "rule_blind_spot",
                   "content": json.dumps({"op": "M1", "target_card": "atoms/x.md"})},
             "b": {"mutation_id": "b", "attack_type": "evidence_ambiguity",
                   "content": json.dumps({"op": "M4", "target_card": "evidence/y.md"})},
             "c": {"mutation_id": "c", "attack_type": "evidence_ambiguity",
                   "content": json.dumps({"op": "M7", "target_card": "evidence/y.md"})}}
    cov = strategy_coverage(rows, by_id)
    chk("策略覆盖：rule_blind_spot 1 条", cov["rule_blind_spot"]["n"] == 1)
    chk("可施加率 = 1 - infra/n", cov["evidence_ambiguity"]["applicable_rate"] == 0.5)
    chk("被拦率按可施加算", cov["rule_blind_spot"]["block_rate"] == 1.0)

    ov = v7_overlap([by_id["a"], by_id["b"]],
                    [{"card": "atoms/x.md", "op": "M1"}, {"card": "z", "op": "M2"}])
    chk("v7 重叠：卡+算子命中 1 条", ov["card_op_overlap"] == 1)
    chk("v7 重叠：卡命中 1 条", ov["card_overlap"] == 1)

    rc = root_cause({"mutation_id": "x", "card": "evidence/y.md",
                     "lost_rules": [], "new_block_rules": []},
                    {"x": {"content": json.dumps({"op": "M6"})}})
    chk("根因：无 lost ⇒ 判规则盲区", any("规则盲区" in d for d in rc["dimensions"]))
    chk("规则覆盖可统计", rule_coverage(rows)["ATOM-FM-REQUIRED"] == 1)
    chk("建议非空", len(suggestions(cov, ov, rule_coverage(rows),
                                  {"neutral": 1})) >= 3)
    chk("escape 分支可渲染", "根因分析" in render(
        {"mode": "escapes", "escapes": [{"mutation_id": "x"}],
         "root_causes": [{"mutation_id": "x", "card": "c", "op": "M1",
                          "lost_rules": ["R"], "dimensions": ["d"]}]}))
    print(f"A3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 A3 新逃逸根因分析")
    ap.add_argument("--results", default=RESULTS)
    ap.add_argument("--mutations", default=MUTS)
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = analyze(args.results, args.mutations)
    md = render(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  mode={res['mode']}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
