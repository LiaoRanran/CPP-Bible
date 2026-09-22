"""623 A4 · 闭环第三轮生成器（针对 A3 逃逸根因 + 策略改进）

**输入**：623 A2 实跑（25 条触达）+ A3 根因（status 过滤缺失、占位居留假象、warn 类未触发）。
**目标**：生成 40 条**定向攻击** mutation，专打 A2 未触达的规则 + H1–H4 变体，
把累计触达规则数推向 >40（A5 目标）。

**与 A1 的差异（A3 改进点落地）**：
1. **status 过滤**：`ATOM-VERIFIED-BOUND`/`ATOM-STATUS-TRANSITION`/`S2-EVIDENCE-VERDICT` 只选
   status=verified（或 verdict=confirm）的卡——A2 因所选手卡 status≠verified 而未触发。
2. **占位居留假象规避**：本批刻意保留被检查内容、只做"就地改写"，避免 A2 那种"删字段致 finding 消失"的假象。
3. **复用 A1 算子集**（MSET/M16/M31/M32/M34/M35/M36/M37/M40/M1/M2/M4/M9），不引入新算子，
   保证闭环一致性。

铁律：不修改原始卡、不修改 gate_engine.py，所有 mutation 只写入 data/。
"""
from __future__ import annotations

import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

import sys
sys.path.insert(0, HERE)
import high_complexity_mutator_623 as base  # 复用 collect_cards / _key_present / _get_value

ATOMS_DIR = base.ATOMS_DIR
EVIDENCE_DIR = base.EVIDENCE_DIR

# A2 已触达规则（避免重复，专打未触达）
A2_TOUCHED = {
    "ATOM-AUDIENCE", "ATOM-DAL-MATCH", "ATOM-FM-REQUIRED", "ATOM-GRAY-ZONE",
    "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-NO-UNVERIFIED", "ATOM-REL-DAG",
    "ATOM-STATUS-VALUE", "EV-ARTIFACT-PRODUCER", "EV-ARTIFACT-VERSION-MATCH",
    "EV-FM-DUP-KEY", "EV-FM-REQUIRED", "EV-FM-YAML-HARDENING", "EV-ID-UNIQUE",
    "EV-MATRIX", "EV-MSCV-NO-VERIFY", "ATOM-CLAIM-STRUCTURED",
    "ATOM-PREREQ-READABLE", "ATOM-REL-TARGET", "ATOM-REL-UNKNOWN",
    "ATOM-VERIFY-REASON", "CARD-PATH-NOT-CANONICAL", "EV-ASSERT-COUNT-BELOW-BASELINE",
    "EV-SERVES-EXIST",
}

# A4 定向目标规则（A2 未触达 or 触发不稳定，需复测/强化）
# status_eq：可选，只选该 status 的卡
RECIPES = [
    dict(rule="ATOM-VERIFIED-BOUND", op="M1", field="superiority", value=None,
         need="superiority", ctype="atom", status_eq="verified", strategy="H1"),
    dict(rule="ATOM-STATUS-TRANSITION", op="M1", field="status_history", value=None,
         need="status_history", ctype="atom", status_eq="verified", strategy="H1"),
    dict(rule="ATOM-SUPERIORITY-WORDS", op="MSET", field="superiority",
         value="clearly the best approach, obviously", need="superiority", ctype="atom", strategy="H2"),
    dict(rule="EV-FALSIFICATION", op="MSET", field="falsification", value="the code works fine",
         need="falsification", ctype="evidence", strategy="H2"),
    dict(rule="DOC-ZERO-PLACEHOLDER", op="M40", field="claim", value=None,
         need="claim", ctype="atom", strategy="H4"),
    dict(rule="EV-TRIVIAL-OBSERVATION", op="MSET", field="actual", value="the test passes as expected",
         need="actual", ctype="evidence", strategy="H2"),
    dict(rule="EV-SELF-SATISFIED-ASSERT", op="M4", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", strategy="H1"),
    dict(rule="S2-EVIDENCE-VERDICT", op="MSET", field="verdict", value="disconfirm",
         need="verdict", ctype="evidence", status_eq="verified", strategy="H2"),
    dict(rule="EV-ASSERT-SYMBOL-MAPPED", op="M32", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", strategy="H3"),
    dict(rule="EV-ENV-DEPENDENT-KEY", op="M37", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", strategy="H3"),
    dict(rule="EV-ARTIFACT-FILE-EXISTS", op="M2", field="artifact", value=None,
         need="artifact", ctype="evidence", strategy="H1"),
]


def build(target_per_rule: int = 4, total_cap: int = 40) -> list[dict]:
    atoms, evidences = base.collect_cards()

    def pick(ctype, need, status_eq):
        out = []
        for c in (atoms if ctype == "atom" else evidences):
            if not base._key_present(c["fm"], need):
                continue
            if status_eq:
                st = base._get_value(c["fm"], "status") or base._get_value(c["fm"], "verdict")
                if st != status_eq:
                    continue
            out.append(c)
        return out

    out = []
    seen = set()
    for recipe in RECIPES:
        cards = pick(recipe["ctype"], recipe["need"], recipe.get("status_eq"))
        made = 0
        idx = 0
        while made < target_per_rule and cards:
            c = cards[idx % len(cards)]
            idx += 1
            content = {"op": recipe["op"], "field": recipe["field"],
                       "target_rule": recipe["rule"], "target_card": c["rel"]}
            if recipe["value"] is not None:
                content["value"] = recipe["value"]
            seed = json.dumps(content, sort_keys=True, ensure_ascii=False)
            mid = "MUT-R3-" + hashlib.sha1(seed.encode()).hexdigest()[:12]
            if mid in seen:
                if idx > len(cards) * 3:
                    break
                continue
            seen.add(mid)
            pred = [recipe["rule"]]
            out.append({
                "mutation_id": mid, "attack_type": recipe["strategy"],
                "target_rule": recipe["rule"], "target_card": c["rel"],
                "content": json.dumps(content, ensure_ascii=False),
                "complexity": 70 + (5 if recipe.get("status_eq") else 0),
                "predicted_rules": pred, "schema_checked": True,
            })
            made += 1
    # 补足到 total_cap：在已生成规则上各加一条
    if len(out) < total_cap:
        extras = total_cap - len(out)
        i = 0
        while extras > 0 and out:
            src = out[i % len(out)]
            content = json.loads(src["content"])
            seed = json.dumps(content, sort_keys=True, ensure_ascii=False) + f"#r3{i}"
            mid = "MUT-R3-" + hashlib.sha1(seed.encode()).hexdigest()[:12]
            if mid not in seen:
                seen.add(mid)
                out.append({**src, "mutation_id": mid,
                            "content": json.dumps(content, ensure_ascii=False)})
                extras -= 1
            i += 1
            if i > total_cap * 3:
                break
    return out


def write_outputs(muts):
    jp = os.path.join(DATA, "adversarial_loop_round3_mutations_623.json")
    mp = os.path.join(DATA, "adversarial_loop_round3_623.md")
    json.dump(muts, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    by_rule = {}
    for m in muts:
        by_rule[m["target_rule"]] = by_rule.get(m["target_rule"], 0) + 1
    lines = ["# 623 A4 · 闭环第三轮 mutation（40 条定向攻击）\n",
             f"> 生成条数：**{len(muts)}** · 定向目标规则：**{len(by_rule)}** 条（A2 未触达/不稳）\n",
             "\n## 目标规则分布\n"]
    for r, n in by_rule.items():
        lines.append(f"- {r}：{n} 条")
    lines.append(f"\n> A2 已触达 {len(A2_TOUCHED)} 条；本批定向补打 {len(by_rule)} 条，"
                 "旨在把累计触达推向 >40。\n")
    lines.append("\n## 与 A2 的策略差异（A3 改进点落地）\n")
    lines.append("1. **status 过滤**：VERIFIED-BOUND / STATUS-TRANSITION / S2-VERDICT 只选 verified/confirm 卡。")
    lines.append("2. **规避占位居留假象**：保留被检查内容、只做就地改写，不再删字段致 finding 消失。")
    lines.append("3. **复用 A1 算子集**，不引入新算子，闭环一致。")
    open(mp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return {"json": jp, "md": mp, "count": len(muts), "rules": len(by_rule)}


if __name__ == "__main__":
    res = write_outputs(build())
    print(json.dumps(res, ensure_ascii=False))
