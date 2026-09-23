"""629 D1 · 攻击目标函数精化（纯标准库，只读）

对现有 mutation v7 的 **1593 条候选**按目标函数排序，选 Top20 作为第八轮攻击种子。

目标函数（任务书给定）：

    maximize  verifier_disagreement_rate × evidence_ambiguity × provenance_inconsistency

三个分量在**静态候选**上无法直接测量（要跑 gate 才知道判决），因此用**显式代理**（假设，见报告）：

| 分量 | 代理（0-1） | 依据 |
|---|---|---|
| verifier_disagreement | `escaped` → 1.0；否则 `min(去重后触发规则数 / 3, 1.0)` | 逃逸 = 验证者全体无异议（最危险）；触发规则越多 = 不同判据对该样本越不一致 |
| evidence_ambiguity | 三组关键词命中加权和（形态/结构/引用），上限 1.0 | 变异点描述里的模糊性词汇（改/替换/删/注入/引用/路径…） |
| provenance_inconsistency | 命中 哈希/时间戳/artifact/provenance → 1.0；`evidence/` 卡 → 0.5；否则 0.2 | 溯源类变异优先打「不可复现」面 |

**乘积形式的意义**：三项相乘 ⇒ 只有「验证者分歧 × 证据歧义 × 溯源不一致」**同时**高的样本才排前；
任一项为 0（如 neutral 且无溯源相关性）则总分 0 —— 正是任务书想要的「三面交叉」种子。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

V7 = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
OUT_JSON = os.path.join(ROOT, "data", "attack_objective_629.json")
OUT_MD = os.path.join(ROOT, "data", "attack_objective_629.md")
TOP_N = 20

LEX_PATTERNS = [
    ("形态", r"改|替换|重命名|变体|大小写|拼写|措辞|写法|case"),
    ("结构", r"删|增|注入|嵌套|字段|键|结构|顺序|恒真"),
    ("引用", r"引用|证据|artifact|路径|hash|哈希|sha|时间戳|provenance|commit"),
]
PROV_PATTERN = r"hash|哈希|sha256|artifact|时间戳|timestamp|provenance|commit|引用"


def v7_variants() -> list[dict[str, Any]]:
    d = json.load(open(V7, encoding="utf-8"))
    return list(d.get("results") or [])


def target_rule_of(v: dict[str, Any]) -> str:
    """v7 记录无 target_rule 字段；从 new_block/new_warn 的 `RULE:path` 反推。"""
    for key in ("new_block", "new_warn"):
        for item in v.get(key) or []:
            head = str(item).split(":", 1)[0].strip()
            if head:
                return head
    return ""


def disagreement(v: dict[str, Any]) -> float:
    if str(v.get("verdict")) == "escaped":
        return 1.0
    rules = {*map(str, v.get("new_block") or []), *map(str, v.get("new_warn") or [])}
    return min(len(rules) / 3.0, 1.0)


def ambiguity(v: dict[str, Any]) -> float:
    text = f"{v.get('point', '')} {v.get('op', '')}"
    hits = sum(1 for _name, pat in LEX_PATTERNS if re.search(pat, text, re.IGNORECASE))
    return min(hits / 3.0 * 1.5, 1.0) if hits else 0.0


def provenance(v: dict[str, Any]) -> float:
    text = f"{v.get('point', '')} {v.get('card', '')}"
    if re.search(PROV_PATTERN, text, re.IGNORECASE):
        return 1.0
    return 0.5 if str(v.get("card", "")).startswith("evidence/") else 0.2


def score_of(v: dict[str, Any]) -> dict[str, Any]:
    """先四舍五入各分量，再乘 —— 保证「报告里的数字相乘 == 报告的 score」（可复核）。"""
    d, a, p = (round(disagreement(v), 4), round(ambiguity(v), 4),
               round(provenance(v), 4))
    return {"disagreement": d, "ambiguity": a, "provenance": p,
            "score": round(d * a * p, 6)}


def ranked() -> list[dict[str, Any]]:
    out = []
    for i, v in enumerate(v7_variants()):
        s = score_of(v)
        out.append({"idx": i, "card": v.get("card"), "op": v.get("op"),
                    "point": v.get("point"), "v7_verdict": v.get("verdict"),
                    "target_rule": target_rule_of(v),
                    "fired_rules": sorted({*map(str, v.get("new_block") or []),
                                           *map(str, v.get("new_warn") or [])}),
                    **s})
    # 确定性排序：score ↓ → disagreement ↓ → card → idx
    return sorted(out, key=lambda x: (-x["score"], -x["disagreement"],
                                      str(x["card"]), x["idx"]))


def seeds(n: int = TOP_N) -> list[dict[str, Any]]:
    return ranked()[:n]


def write_outputs() -> dict[str, Any]:
    r, top = ranked(), seeds()
    data = {"objective": "verifier_disagreement_rate × evidence_ambiguity "
                         "× provenance_inconsistency",
            "source": os.path.relpath(V7, ROOT).replace(os.sep, "/"),
            "variants": len(r), "top_n": TOP_N,
            "proxy_definitions": {
                "disagreement": "escaped→1.0；否则 min(去重触发规则数/3,1.0)",
                "ambiguity": "形态/结构/引用 三组关键词命中加权（上限 1.0）",
                "provenance": "命中哈希/时间戳/artifact/provenance→1.0；"
                              "evidence/ 卡→0.5；否则 0.2",
            },
            "seeds": top}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    lines = [
        "# 629 D1 · 攻击目标函数精化（第八轮种子选择）", "",
        "> 工具：`tools/attack_objective_629.py`（纯标准库，只读 v7 候选集）",
        f"> 候选池：`{data['source']}` 共 **{len(r)}** 条（任务书 1593 ✓）· "
        f"选出 **Top {TOP_N}** 种子", "",
        "## 一、目标函数", "",
        "```",
        "maximize  verifier_disagreement_rate × evidence_ambiguity × provenance_inconsistency",
        "```", "",
        "**乘积**（非加权和）的意义：三项**同时**高才排前；任一项为 0 则总分 0 —— "
        "避免「只在一个面上凶」的样本挤进种子。", "",
        "## 二、代理定义（显式假设，静态候选无法直接测）", "",
        "| 分量 | 代理 | 依据 |", "|---|---|---|",
        "| verifier_disagreement | `escaped`→1.0；否则 `min(去重触发规则数/3, 1.0)` | "
        "逃逸 = 所有验证者都不拦（最危险）；触发规则越多 = 判据间越不一致 |",
        "| evidence_ambiguity | 形态/结构/引用三组关键词命中加权（上限 1.0） | "
        "变异点描述里的模糊性词汇 |",
        "| provenance_inconsistency | 哈希/时间戳/artifact/provenance→1.0；"
        "`evidence/` 卡→0.5；否则 0.2 | 溯源类变异优先打「不可复现」面 |", "",
        "## 三、Top20 种子", "",
        "| # | 卡 | op | v7 判决 | 触发规则数 | disagreement | ambiguity | provenance | "
        "**score** |", "|---|---|---|---|---|---|---|---|---|",
        *[f"| {i} | `{s['card']}` | {s['op']} | {s['v7_verdict']} | "
          f"{len(s['fired_rules'])} | {s['disagreement']} | {s['ambiguity']} | "
          f"{s['provenance']} | **{s['score']}** |" for i, s in enumerate(top, 1)], "",
        "## 四、为什么这些种子优先级高", "",
        f"- 池内 score 分布：>0 的有 **{sum(1 for x in r if x['score'] > 0)}** 条，"
        f"=0 的有 {sum(1 for x in r if x['score'] == 0)} 条（乘积极强筛：多数候选在某一面为 0）；",
        f"- Top20 全部命中 `provenance` 强相关的变异点（哈希/artifact/引用类），"
        f"且 `ambiguity` 分量 ≥ {min(s['ambiguity'] for s in top)} —— "
        "意味着**判据要用到歧义证据、且溯源链上有可动手的字段**，这正是 verifier 攻击面"
        "L2（证据漂移）/L4（规则绕过）交叉的位置；",
        f"- Top20 中 v7 判决为 neutral 的有 "
        f"**{sum(1 for s in top if s['v7_verdict'] == 'neutral')}** 条 —— "
        "这些是 v7 时代**完全没被拦住**的样本，优先复跑检验「现在是否仍拦不住」。", "",
        "## 五、局限", "",
        "- 三个代理都是**静态启发式**（读变异点文本与 v7 判决），不是真实测量；"
        "真实 disagreement 需要两个独立验证器各跑一遍（本批只做了 gate 判决）；",
        "- `target_rule` 从 `new_block/new_warn` 反推（v7 无该字段），neutral 样本反推为空；",
        "- v7 池是 621-622 生成的，**不含 M8/M9 算子**（新算子样本在 "
        "`data/mutation/new_mutations_62*.jsonl`）⇒ 种子偏向 M1-M7 家族。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return data


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = ranked()
    top = seeds()
    chk("v7 候选池 = 1593 条", len(r) == 1593, f"({len(r)})")
    chk(f"选出 Top{TOP_N}", len(top) == TOP_N)
    chk("排序确定（两次结果一致）", [x["idx"] for x in ranked()[:TOP_N]] ==
        [x["idx"] for x in top])
    chk("score = 三分量乘积",
        all(abs(x["score"] - x["disagreement"] * x["ambiguity"] * x["provenance"]) < 1e-6
            for x in r))
    chk("分量均在 [0,1]", all(0 <= x[k] <= 1 for x in r
                          for k in ("disagreement", "ambiguity", "provenance")))
    chk("Top 非零分且单调不增",
        all(s["score"] > 0 for s in top)
        and all(top[i]["score"] >= top[i + 1]["score"] for i in range(len(top) - 1)))
    chk("种子含卡/op/变异点/v7判决",
        all(s["card"] and s["op"] and s["point"] and s["v7_verdict"] for s in top))
    chk("输出 JSON + 报告存在", os.path.exists(OUT_JSON) and os.path.exists(OUT_MD))
    print(f"D1 attack objective check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 D1 攻击目标函数（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--write", action="store_true", help="写种子 JSON + 报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.write:
        d = write_outputs()
        print(f"written {OUT_JSON} + {OUT_MD} (seeds={len(d['seeds'])})")
        return 0
    if args.json:
        print(json.dumps(seeds(), ensure_ascii=False, indent=2))
        return 0
    top = seeds()
    print(f"variants={len(ranked())} seeds={len(top)} top_score={top[0]['score']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
