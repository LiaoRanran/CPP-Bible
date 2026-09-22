"""625 B1 · 闭环第 7 轮（稳定验证轮，~100 条）

**目的**：验证雷2 闭环是否进入**稳定期**（第 3 连续轮，623-625）。策略：
- **Y1 盲区定向**：对 624 后仍未触达的**盲区规则**，每条造 2 条定向 mutation（尽力命中；编译/复算/git 类
  盲区预期仍不可达 ⇒ 如实记录）。
- **Y2 已触达回归**：对**已触达规则**复用 623/624 的已知触发原语，验证规则仍能挡住（回归通过率）。
- **Y3 随机混合**：Y1/Y2 混合抽样。

**复用**：624 的跨卡沙箱（`cross_card_attack_624`，已修 apply_multi 备份去重）。
铁律：只读生成 + 沙箱临时改（备份+还原）；不改 gate_engine；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cross_card_attack_624 as cc  # noqa: E402
import gate_engine as GE  # noqa: E402
import high_complexity_mutator_623 as H623  # noqa: E402

# 624 A5 热力图 v2 的累计触达集（34 条，624 末）
TOUCHED = {
    "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-NO-UNVERIFIED",
    "ATOM-STATUS-VALUE", "ATOM-DAL-MATCH", "ATOM-REL-DAG", "ATOM-AUDIENCE",
    "ATOM-PREREQ-READABLE", "ATOM-GRAY-ZONE", "ATOM-CLAIM-STRUCTURED", "EV-FM-REQUIRED",
    "EV-ID-UNIQUE", "EV-MATRIX", "EV-ARTIFACT-VERSION-MATCH", "EV-MSCV-NO-VERIFY",
    "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING", "EV-ARTIFACT-PRODUCER",
    "EV-ASSERT-COUNT-BELOW-BASELINE", "EV-ASSERT-SYMBOL-MAPPED", "ATOM-REL-TARGET",
    "ATOM-REL-UNKNOWN", "ATOM-VERIFY-REASON", "CARD-PATH-NOT-CANONICAL", "EV-SERVES-EXIST",
    "ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS", "ATOM-MISCONCEPTION-REF",
    "ATOM-VERIFIED-BOUND", "OBSERVATION-NEEDS-ARTIFACT", "S2-EVIDENCE-VERDICT",
    "ATOM-SUPERIORITY-WORDS", "EV-FALSIFICATION",
}

# Y1 盲区定向的字段猜测表（可命中的词表/字段类盲区）；其余用通用扰动
GUESS = {
    "DOC-ZERO-PLACEHOLDER": ("MSET", "claim", "TODO"),
    "ATOM-SUPERIORITY-WORDS": ("MSET", "superiority", "clearly the best approach, obviously superior"),
    "EV-FALSIFICATION": ("MSET", "falsification", "the code works fine"),
    "EV-TRIVIAL-OBSERVATION": ("MSET", "actual", "the test passes as expected"),
    "EV-FALSIFICATION-QUANT": ("MSET", "falsification", "works"),
    "EV-SELF-SATISFIED-ASSERT": ("MSET", "artifact_assert", "x equals x"),
    "EV-MATRIX-UNBACKED": ("M1", "artifact_sha256", None),
    "EV-OUT-UNDECLARED-KEY": ("MSET", "actual", "undeclared_key_xyz=1"),
    "ATOM-MISCONCEPTION-LEVELS": ("M1", "pedagogy", None),
    "MIS-LIBRARY": ("MSET", "object", "the thing"),
    "S3-EXPECTED-HARDCODED": ("MSET", "expected", "42"),
    "EV-ZERO-DIAG-WERROR": ("MSET", "flags", "-Wall"),
    "EV-WERROR-DECL-BIND": ("MSET", "compile_flags", "-Wall"),
    "EV-RUN-KEY-DECLARED-EXISTS": ("MSET", "actual", "foo=1"),
    "EV-ASSERT-COUNT-BELOW-BASELINE": ("M1", "artifact_assert", None),
    "EV-ENV-DEPENDENT-KEY": ("MSET", "actual", "nproc=4"),
    "S1-AUTHOR-SELF-VERIFY": ("MSET", "verified_by", "machine"),
    "S1-GIT-AUTHOR-BINDING": ("MSET", "author", "unknown"),
    "ATOM-STATUS-TRANSITION": ("MSET", "status_history", "verified"),
    "ATOM-VERIFIED-BOUND": ("M1", "first_hand", None),
    "INFERENCE-NOT-MACHINE-VERIFIED": ("MSET", "basis", "machine"),
    "OBSERVATION-LIVENESS": ("M1", "liveness", None),
    "EV-OUT-STALE-MTIME": ("MSET", "actual", "stale=1"),
    "EV-FIXTURE-NO-ECHO-DATA": ("M1", "fixture", None),
    "ATOM-CLAIM-CONCEPT-NORMALIZED": ("MSET", "object", "A sentence describing something."),
}


def all_rules() -> list[str]:
    return [r.id for r in GE.RULES]


def blind_rules() -> list[str]:
    return [r for r in all_rules() if r not in TOUCHED]


def _generic_edit(card: str, idx: int) -> dict:
    return {"card": card, "op": "MSET", "field": "status", "value": f"probe_{idx}"}


def generate_round7(inv: dict, y1_per_rule: int = 2, y2_n: int = 20, y3_n: int = 22) -> list[dict]:
    atoms = inv["atoms"]
    evid = inv["evidence"]
    pool = atoms + evid
    out: list[dict] = []

    # ---- Y1：盲区定向（每条盲区 y1_per_rule 条）----
    for j, rule in enumerate(blind_rules()):
        op, field, val = GUESS.get(rule, ("MSET", "status", None))
        for k in range(y1_per_rule):
            card = pool[(j * y1_per_rule + k) % len(pool)]["card"]
            edit = {"card": card, "op": op, "field": field}
            if val is not None:
                edit["value"] = val
            out.append({"mutation_id": f"Y1-{rule}-{k+1}", "strategy": "Y1",
                        "attack_type": f"盲区定向:{rule}", "complexity": 78,
                        "predicted_rules": [rule], "edits": [edit]})

    # ---- Y2：已触达回归（复用 623 RECIPES 的已知触发原语）----
    recipes = list(H623.RECIPES)
    i = 0
    while len([m for m in out if m["strategy"] == "Y2"]) < y2_n and recipes:
        r = recipes[i % len(recipes)]
        card = pool[i % len(pool)]["card"]
        edit = {"card": card, "op": r["op"], "field": r["field"]}
        if r["value"] is not None:
            edit["value"] = r["value"]
        out.append({"mutation_id": f"Y2-{i+1:03d}", "strategy": "Y2",
                    "attack_type": f"回归:{r['rule']}", "complexity": 70,
                    "predicted_rules": [r["rule"]], "edits": [edit]})
        i += 1

    # ---- Y3：随机混合 ----
    y1 = [m for m in out if m["strategy"] == "Y1"]
    y2 = [m for m in out if m["strategy"] == "Y2"]
    for k in range(y3_n):
        src = (y1 + y2)[k % max(len(y1) + len(y2), 1)]
        out.append({"mutation_id": f"Y3-{k+1:03d}", "strategy": "Y3",
                    "attack_type": "混合:" + src["attack_type"], "complexity": 74,
                    "predicted_rules": list(src["predicted_rules"]), "edits": list(src["edits"])})
    return out


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("规则总数为 67", len(all_rules()) == 67)
    blind = blind_rules()
    chk("盲区非空且 < 40", 0 < len(blind) < 40)
    inv = cc.load_inventory()
    muts = generate_round7(inv)
    chk("生成 ~100 条（≥95 且 ≤110）", 95 <= len(muts) <= 110)
    chk("Y1/Y2/Y3 均存在", {m["strategy"] for m in muts} == {"Y1", "Y2", "Y3"})
    chk("每条含 edits", all(m["edits"] for m in muts))
    chk("Y1 覆盖全部盲区", {m["predicted_rules"][0] for m in muts if m["strategy"] == "Y1"} == set(blind))
    print(f"B1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 B1 闭环第 7 轮")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--gen", action="store_true", help="生成并打印")
    ap.add_argument("--run", action="store_true", help="沙箱实跑（真跑 gate）")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    inv = cc.load_inventory()
    muts = generate_round7(inv)
    if args.gen:
        print(json.dumps(muts, ensure_ascii=False, indent=2))
        return 0
    if args.run:
        res = cc.run_batch(muts, sb=cc.CrossCardSandbox())
        res["predicted_rules"] = sorted({r for m in muts for r in m["predicted_rules"]})
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump({"mutations": muts, **res}, fh, ensure_ascii=False, indent=2)
        print(json.dumps({k: v for k, v in res.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
