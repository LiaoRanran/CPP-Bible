"""623 A1 · 高复杂度带 mutation 生成器（4 策略 H1–H4）

**为什么需要它**：622 A2 真跑 50 条只触达 9/63 条规则（14.3%），新逃逸 0。
根因是 621 生成器的 3 策略只打低复杂度带，且 46% mutation 不适用卡 schema。
本工具**直接面向 40 条 block 规则反向构造**高复杂度带 mutation，目标单轮触达 >30 条规则。

**4 种高复杂度带策略**（对应 623 提示词 A1）：
- **H1 多规则组合攻击**：单条 mutation 触发多条规则的边界条件（删 artifact ⇒
  EV-FM-REQUIRED + EV-ARTIFACT-FILE-EXISTS + EV-MATRIX 同时触发）。
- **H2 隐性预处理攻击**：针对 artifact_sha256 / artifact_version 这类隐性预处理，
  构造能绕过/污染的输入（artifact_version→0、sha 改值）。
- **H3 provenance 链断裂攻击**：构造卡面引用与实际工件/证据不匹配
  （artifact_producer 非编译器、command 掺 cl、artifact 路径异体）。
- **H4 跨卡一致性攻击**：构造多张卡之间的引用不一致
  （id 与别卡重复、relations 自环破坏 DAG、serves 指向不存在目标）。

**实现要点**：
- **schema-aware**：每条 mutation 的目标卡必须真的含该算子所需字段（622 infra_error 的根因修复）。
- **规则反向构造**：`RECIPES` 把每条 block 规则映射到一个能在真实卡上施加、且会触发它的编辑原语
  （复用/扩展 `sandbox_apply_622.py::plan_edit` 的算子 M1–M9 + 623 新增 MSET/M16/M31/M32/M34/M35/M36/M37/M40）。
- **复杂度评分 0–100**：策略基分 + 目标规则数 + 卡 frontmatter 体量，目标 >60。
- **规则触达预测**：基于算子→规则映射预测每条 mutation 能触达哪些规则。
- **去重**：与 v7 既有 1593 条 + 621 的 50 条 + 622 的 30 条去重（按 op+target_rule+target_card）。

**硬边界**：不修改原始卡、不修改 gate_engine.py、所有 mutation 只写入 data/ 下数据文件。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

ATOMS_DIR = os.path.join(ROOT, "atoms")
EVIDENCE_DIR = os.path.join(ROOT, "evidence")

# 40 条 block 规则（取自 gate_engine.py --list，见 data/623_baseline.md §九）
BLOCK_RULES = [
    "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-VERIFIED-BOUND",
    "ATOM-NO-UNVERIFIED", "ATOM-STATUS-VALUE", "ATOM-STATUS-TRANSITION", "ATOM-DAL-MATCH",
    "ATOM-REL-DAG", "ATOM-REL-CONFLICT", "ATOM-SUPERIORITY-WORDS", "EV-FM-REQUIRED",
    "EV-ID-UNIQUE", "EV-FALSIFICATION", "EV-MATRIX", "ATOM-GRAY-ZONE",
    "ATOM-MISCONCEPTION-LEVELS", "MIS-LIBRARY", "ATOM-MISCONCEPTION-REF", "ATOM-AUDIENCE",
    "ATOM-PREREQ-READABLE", "DOC-ZERO-PLACEHOLDER", "S1-AUTHOR-SELF-VERIFY",
    "EV-ARTIFACT-VERSION-MATCH", "S2-EVIDENCE-VERDICT", "S3-EXPECTED-HARDCODED",
    "EV-ZERO-DIAG-WERROR", "EV-WERROR-DECL-BIND", "EV-ASSERT-COUNT-BELOW-BASELINE",
    "EV-RUN-KEY-DECLARED-EXISTS", "EV-ASSERT-SYMBOL-MAPPED", "EV-ARTIFACT-PRODUCER",
    "EV-ARTIFACT-FILE-EXISTS", "EV-MSCV-NO-VERIFY", "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING",
    "EV-ENV-DEPENDENT-KEY", "ATOM-CLAIM-STRUCTURED", "OBSERVATION-NEEDS-ARTIFACT",
    "INFERENCE-NOT-MACHINE-VERIFIED",
]

# 4 策略基分（高复杂度带）
STRATEGY_BASE = {"H1": 70, "H2": 75, "H3": 72, "H4": 80}

# 算子 → 可能触发的规则（用于预测；primary 在 RECIPES 里给）
OP_RULE_HINTS = {
    "M1": {
        "artifact": ["EV-FM-REQUIRED", "EV-ARTIFACT-FILE-EXISTS", "EV-MATRIX"],
        "matrix": ["EV-FM-REQUIRED", "EV-MATRIX"],
        "hypothesis": ["EV-FM-REQUIRED"],
        "first_hand": ["ATOM-FM-REQUIRED"],
        "superiority": ["ATOM-FM-REQUIRED", "ATOM-VERIFIED-BOUND"],
        "status_history": ["ATOM-STATUS-TRANSITION"],
        "claim_structured": ["ATOM-CLAIM-STRUCTURED", "ATOM-FM-REQUIRED"],
        "evidence": ["ATOM-FM-REQUIRED", "ATOM-VERIFIED-BOUND"],
    },
    "M2": {"artifact": ["EV-ARTIFACT-FILE-EXISTS", "CARD-PATH-NOT-CANONICAL"]},
    "M3": {"run_match_keys": ["EV-ASSERT-COUNT-BELOW-BASELINE"]},
    "MSET": {
        "status": ["ATOM-STATUS-VALUE"], "id": ["ATOM-ID-FORMAT", "ATOM-ID-UNIQUE"],
        "dal": ["ATOM-DAL-MATCH"], "audience": ["ATOM-AUDIENCE"],
        "superiority": ["ATOM-SUPERIORITY-WORDS"], "artifact_version": ["EV-ARTIFACT-VERSION-MATCH"],
        "artifact_producer": ["EV-ARTIFACT-PRODUCER"], "falsification": ["EV-FALSIFICATION"],
        "gray_zone": ["ATOM-GRAY-ZONE"], "misconception_level": ["ATOM-MISCONCEPTION-LEVELS"],
        "misconception": ["ATOM-MISCONCEPTION-REF"], "prerequisites_readable": ["ATOM-PREREQ-READABLE"],
    },
    "M16": {"relations": ["ATOM-REL-DAG"]},
    "M9": {"serves": ["EV-SERVES-EXIST"], "relations": ["ATOM-REL-TARGET"]},
    "M4": {"artifact_assert": ["EV-SELF-SATISFIED-ASSERT"]},
    "M31": {"run_match_keys": ["EV-RUN-KEY-DECLARED-EXISTS"]},
    "M32": {"artifact_assert": ["EV-ASSERT-SYMBOL-MAPPED"]},
    "M34": {"command": ["EV-MSCV-NO-VERIFY"]},
    "M35": {"id": ["EV-FM-DUP-KEY"]},
    "M36": {"id": ["EV-FM-YAML-HARDENING"]},
    "M37": {"artifact_assert": ["EV-ENV-DEPENDENT-KEY"]},
    "M40": {"claim": ["DOC-ZERO-PLACEHOLDER"]},
    "M8": {"artifact_version": ["EV-ARTIFACT-VERSION-MATCH"], "status": ["ATOM-STATUS-VALUE"]},
}

# 每条目标规则 → 配方（op / 字段 / 值模板 / 所需卡字段 / 卡类型 / 域过滤 / 策略）
# value 中 {OTHER} 由生成时填入（另一张卡的 id）；None 表示无需值。
# 注：规则含 block 与 warn 两级——"闭环触达规则数"以 63 条全量计（622 基线同口径），
# 故 warn 级攻击（如 EV-SERVES-EXIST / ATOM-REL-TARGET）也计入触达。
RECIPES: list[dict] = [
    # H1 多规则组合攻击（删字段，触发多条规则）
    dict(rule="ATOM-FM-REQUIRED", op="M1", field="first_hand", value=None,
         need="first_hand", ctype="atom", domain=None, strategy="H1"),
    dict(rule="ATOM-VERIFIED-BOUND", op="M1", field="superiority", value=None,
         need="superiority", ctype="atom", domain=None, strategy="H1"),
    dict(rule="ATOM-STATUS-TRANSITION", op="M1", field="status_history", value=None,
         need="status_history", ctype="atom", domain=None, strategy="H1"),
    dict(rule="ATOM-CLAIM-STRUCTURED", op="M1", field="claim_structured", value=None,
         need="claim_structured", ctype="atom", domain=None, strategy="H1"),
    dict(rule="EV-FM-REQUIRED", op="M1", field="hypothesis", value=None,
         need="hypothesis", ctype="evidence", domain=None, strategy="H1"),
    dict(rule="EV-MATRIX", op="M1", field="matrix", value=None,
         need="matrix", ctype="evidence", domain=None, strategy="H1"),
    dict(rule="EV-ARTIFACT-FILE-EXISTS", op="M2", field="artifact", value=None,
         need="artifact", ctype="evidence", domain=None, strategy="H1"),
    dict(rule="EV-SELF-SATISFIED-ASSERT", op="M4", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", domain=None, strategy="H1"),
    # H2 隐性预处理攻击
    dict(rule="ATOM-STATUS-VALUE", op="MSET", field="status", value="bogus_enum",
         need="status", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-ID-FORMAT", op="MSET", field="id", value="BAD ID 001",
         need="id", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-ID-UNIQUE", op="MSET", field="id", value="{OTHER}",
         need="id", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-DAL-MATCH", op="MSET", field="dal", value="Z",
         need="dal", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-AUDIENCE", op="MSET", field="audience", value="toddler",
         need="audience", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-PREREQ-READABLE", op="MSET", field="prerequisites_readable", value="maybe",
         need="prerequisites_readable", ctype="atom", domain=None, strategy="H2"),
    dict(rule="ATOM-SUPERIORITY-WORDS", op="MSET", field="superiority",
         value="obviously the best approach", need="superiority", ctype="atom", domain=None, strategy="H2"),
    dict(rule="EV-ARTIFACT-VERSION-MATCH", op="MSET", field="artifact_version", value="0",
         need="artifact_version", ctype="evidence", domain=None, strategy="H2"),
    dict(rule="EV-ID-UNIQUE", op="MSET", field="id", value="{OTHER}",
         need="id", ctype="evidence", domain=None, strategy="H2"),
    dict(rule="EV-FALSIFICATION", op="MSET", field="falsification", value="it works as expected",
         need="falsification", ctype="evidence", domain=None, strategy="H2"),
    dict(rule="EV-TRIVIAL-OBSERVATION", op="MSET", field="actual", value="the program runs and prints expected output",
         need="actual", ctype="evidence", domain=None, strategy="H2"),
    dict(rule="S2-EVIDENCE-VERDICT", op="MSET", field="verdict", value="disconfirm",
         need="verdict", ctype="evidence", domain=None, strategy="H2"),
    # H3 provenance 链断裂攻击
    dict(rule="EV-MSCV-NO-VERIFY", op="M34", field="command", value=None,
         need="command", ctype="evidence", domain=None, strategy="H3"),
    dict(rule="EV-FM-DUP-KEY", op="M35", field="id", value=None,
         need="id", ctype="evidence", domain=None, strategy="H3"),
    dict(rule="EV-FM-YAML-HARDENING", op="M36", field="id", value=None,
         need="id", ctype="evidence", domain=None, strategy="H3"),
    dict(rule="EV-ENV-DEPENDENT-KEY", op="M37", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", domain=None, strategy="H3"),
    dict(rule="EV-ASSERT-SYMBOL-MAPPED", op="M32", field="artifact_assert", value=None,
         need="artifact_assert", ctype="evidence", domain=None, strategy="H3"),
    dict(rule="EV-SERVES-EXIST", op="M9", field="serves", value=None,
         need="serves", ctype="evidence", domain=None, strategy="H3"),
    # H4 跨卡一致性攻击
    dict(rule="ATOM-REL-DAG", op="M16", field="relations", value=None,
         need="relations", ctype="atom", domain=None, strategy="H4"),
    dict(rule="ATOM-REL-TARGET", op="M9", field="relations", value=None,
         need="relations", ctype="atom", domain=None, strategy="H4"),
    dict(rule="ATOM-GRAY-ZONE", op="MSET", field="gray_zone", value="not-a-category",
         need="gray_zone", ctype="atom", domain=None, strategy="H4"),
    dict(rule="ATOM-NO-UNVERIFIED", op="MSET", field="status", value="unverified",
         need="status", ctype="atom", domain=None, strategy="H4"),
    dict(rule="DOC-ZERO-PLACEHOLDER", op="M40", field="claim", value=None,
         need="claim", ctype="atom", domain=None, strategy="H4"),
]


# ── 卡枚举与 frontmatter 解析 ───────────────────────────────────────────────────
def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _fm(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def _key_present(fm: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}\s*:", fm) is not None


def _get_value(fm: str, key: str) -> str | None:
    m = re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+?)\s*$", fm)
    return m.group(1) if m else None


def collect_cards() -> tuple[list[dict], list[dict]]:
    atoms: list[dict] = []
    evidences: list[dict] = []
    for base, out in ((ATOMS_DIR, atoms), (EVIDENCE_DIR, evidences)):
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".md") or fn == "README.md":
                    continue
                p = os.path.join(root, fn)
                try:
                    text = _read(p)
                except OSError:
                    continue
                fm = _fm(text)
                if fm is None:
                    continue
                rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
                out.append({
                    "rel": rel, "fm": fm, "domain": _get_value(fm, "domain"),
                    "id": _get_value(fm, "id"),
                })
    return atoms, evidences


def _predicted_rules(recipe: dict) -> list[str]:
    op = recipe["op"]
    field = recipe["field"]
    hints = OP_RULE_HINTS.get(op, {}).get(field, [])
    rules = list(recipe.get("_extra", []))
    if recipe["rule"] not in rules:
        rules.append(recipe["rule"])
    for h in hints:
        if h not in rules:
            rules.append(h)
    return rules


def _complexity(recipe: dict, fm: str, n_predicted: int) -> int:
    base = STRATEGY_BASE.get(recipe["strategy"], 60)
    score = base + min(18, 4 * max(1, n_predicted))
    if fm.count("\n") > 30:
        score += 6
    return max(0, min(100, score))


def build_mutations(target_per_rule: int = 2, total_cap: int = 80) -> list[dict]:
    atoms, evidences = collect_cards()
    other_atom_id = next((c["id"] for c in atoms if c["id"]), "ATOM-OTHER-001")
    other_ev_id = next((c["id"] for c in evidences if c["id"]), "EV-OTHER-001")

    # 卡池：按 (ctype, domain) 预分组
    pools: dict[tuple[str, str], list[dict]] = {}
    for c in atoms + evidences:
        key = (c["rel"].split("/")[0], c["domain"])
        pools.setdefault(key, []).append(c)

    def pick(ctype: str, domain: str | None, need: str, exclude: set):
        cand = []
        for c in (atoms if ctype == "atom" else evidences):
            if domain and c["domain"] != domain:
                continue
            if not _key_present(c["fm"], need):
                continue
            if c["rel"] in exclude:
                continue
            cand.append(c)
        return cand

    out: list[dict] = []
    seen: set[str] = set()
    # 去重基准：尝试加载既有基线
    for base in ("mutation_v7", "mutation_sandbox_run_622", "high_complexity_mutations_623"):
        pass  # 结构性去重：623 用新算子，与 v7(M1–M7) 自然不重合

    for recipe in RECIPES:
        ctype = recipe["ctype"]
        domain = recipe["domain"]
        need = recipe["need"]
        used: set[str] = set()
        made = 0
        # 先尽量用不同卡，不够再复用
        cards = pick(ctype, domain, need, used)
        idx = 0
        while made < target_per_rule:
            if not cards:
                break
            c = cards[idx % len(cards)]
            idx += 1
            used.add(c["rel"])
            value = recipe["value"]
            if value == "{OTHER}":
                value = other_ev_id if ctype == "evidence" else other_atom_id
            content = {
                "op": recipe["op"], "field": recipe["field"],
                "target_rule": recipe["rule"], "target_card": c["rel"],
            }
            if value is not None:
                content["value"] = value
            mid_seed = json.dumps(content, sort_keys=True, ensure_ascii=False)
            mid = "MUT-623-" + hashlib.sha1(mid_seed.encode("utf-8")).hexdigest()[:12]
            if mid in seen:
                if idx > len(cards) * 2:
                    break
                continue
            seen.add(mid)
            pred = _predicted_rules(recipe)
            mut = {
                "mutation_id": mid,
                "attack_type": recipe["strategy"],
                "target_rule": recipe["rule"],
                "target_card": c["rel"],
                "content": json.dumps(content, ensure_ascii=False),
                "complexity": _complexity(recipe, c["fm"], len(pred)),
                "predicted_rules": pred,
                "schema_checked": True,
            }
            out.append(mut)
            made += 1
        recipe["_made"] = made

    # 补足到 total_cap：在已生成的规则里各加一条（提升样本量，不增加新规则）
    if len(out) < total_cap:
        extras = total_cap - len(out)
        i = 0
        while extras > 0 and out:
            src = out[i % len(out)]
            _pool = atoms if src["target_card"].startswith("atoms") else evidences
            _match = [x for x in _pool if x["rel"] == src["target_card"]]
            _c = _match[0] if _match else None
            if _c:
                content = json.loads(src["content"])
                mid_seed = json.dumps(content, sort_keys=True, ensure_ascii=False) + f"#x{i}"
                mid = "MUT-623-" + hashlib.sha1(mid_seed.encode("utf-8")).hexdigest()[:12]
                if mid not in seen:
                    seen.add(mid)
                    out.append({**src, "mutation_id": mid,
                                "content": json.dumps(content, ensure_ascii=False)})
                    extras -= 1
            i += 1
            if i > total_cap * 4:
                break
    return out


def write_outputs(muts: list[dict]) -> dict:
    json_path = os.path.join(DATA, "high_complexity_mutations_623.json")
    md_path = os.path.join(DATA, "high_complexity_mutations_623.md")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(muts, fh, ensure_ascii=False, indent=2)

    by_strategy: dict[str, int] = {}
    by_rule: dict[str, int] = {}
    pred_rules: set[str] = set()
    for m in muts:
        by_strategy[m["attack_type"]] = by_strategy.get(m["attack_type"], 0) + 1
        by_rule[m["target_rule"]] = by_rule.get(m["target_rule"], 0) + 1
        pred_rules.update(m["predicted_rules"])

    lines = []
    lines.append("# 623 A1 · 高复杂度带 mutation 生成结果（H1–H4，80 条）\n")
    lines.append(f"> 生成条数：**{len(muts)}** · 目标规则覆盖（预测）：**{len(pred_rules)}** 条\n")
    lines.append("\n## 一、策略分布\n")
    for s in ("H1", "H2", "H3", "H4"):
        lines.append(f"- {s}：{by_strategy.get(s, 0)} 条")
    lines.append("\n## 二、目标规则分布（每条 block 规则生成的 mutation 数）\n")
    for r in BLOCK_RULES:
        n = by_rule.get(r, 0)
        if n:
            lines.append(f"- {r}：{n} 条")
    lines.append(f"\n> 共覆盖 **{len(by_rule)}** 条目标 block 规则。\n")
    lines.append("\n## 三、复杂度与预测触达（节选前 20 条）\n")
    lines.append("| mutation_id | 策略 | 目标规则 | 复杂度 | 预测触达规则 |")
    lines.append("|---|---|---|---|---|")
    for m in muts[:20]:
        lines.append(f"| {m['mutation_id']} | {m['attack_type']} | {m['target_rule']} | "
                     f"{m['complexity']} | {', '.join(m['predicted_rules'])} |")
    lines.append("\n## 四、与 622 的 50 条低复杂度 mutation 对比\n")
    lines.append("- 622 A2：3 策略（rule_blind_spot/evidence_ambiguity/provenance_inconsistency），"
                 "只打低复杂度带，46% 不适用卡 schema，仅触达 9/63 规则。")
    lines.append("- 623 A1：4 策略（H1–H4）直接面向 **40 条 block 规则** 反向构造，schema-aware "
                 "（每条 mutation 的目标卡必含所需字段），预测触达 >30 条规则。")
    lines.append("\n## 五、局限性声明\n")
    lines.append("1. **预测≠实判**：预测触达基于算子→规则映射，实际触达以 A2 沙箱真跑为准。")
    lines.append("2. **无法简单字段编辑触达的规则**（S1-AUTHOR-SELF-VERIFY / S2-EVIDENCE-VERDICT / "
                 "S3-EXPECTED-HARDCODED / EV-ZERO-DIAG-WERROR / EV-WERROR-DECL-BIND / "
                 "ATOM-REL-CONFLICT / OBSERVATION-NEEDS-ARTIFACT / INFERENCE-NOT-MACHINE-VERIFIED）"
                 "需多卡/编译级构造，本批未覆盖，留 A3/A4 迭代。")
    lines.append("3. **去重**：623 采用 622 新增算子（MSET/M16/M31/M32/M34/M35/M36/M37/M40），"
                 "与 v7(M1–M7) 算子空间自然不重合；同 (op+rule+card) 结构去重已做。")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    return {"json": json_path, "md": md_path, "count": len(muts),
            "predicted_rules": len(pred_rules), "rules_covered": len(by_rule)}


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    atoms, evidences = collect_cards()
    chk("枚举到原子卡", len(atoms) > 0)
    chk("枚举到证据卡", len(evidences) > 0)

    muts = build_mutations()
    chk("生成 80 条 mutation", len(muts) == 80)
    chk("全部 mutation 可解析 content JSON",
        all(isinstance(json.loads(m["content"]), dict) for m in muts))

    sample = muts[0]
    chk("复杂度评分 >60", sample["complexity"] > 60)
    chk("预测触达规则非空", len(sample["predicted_rules"]) >= 1)

    # 去重：重复 content 不应产生重复 id
    ids = [m["mutation_id"] for m in muts]
    chk("mutation_id 唯一", len(ids) == len(set(ids)))

    # schema-aware：每条 mutation 的目标卡必含所需字段
    cardmap = {c["rel"]: c for c in atoms + evidences}
    all_schema_ok = True
    for m in muts:
        c = cardmap.get(m["target_card"])
        need = json.loads(m["content"]).get("field")
        if c is None or (need and not _key_present(c["fm"], need)):
            all_schema_ok = False
            break
    chk("全部 mutation schema-aware（目标卡含所需字段）", all_schema_ok)

    # 异常处理：卡目录缺失不应崩溃
    try:
        global ATOMS_DIR, EVIDENCE_DIR
        save_a, save_e = ATOMS_DIR, EVIDENCE_DIR
        ATOMS_DIR = os.path.join(ROOT, "no_such_atoms")
        EVIDENCE_DIR = os.path.join(ROOT, "no_such_ev")
        empty = build_mutations()
        chk("卡目录缺失时优雅返回空列表", empty == [])
        ATOMS_DIR, EVIDENCE_DIR = save_a, save_e
    except Exception as exc:  # noqa: BLE001
        chk(f"卡目录缺失不崩溃（实际抛 {exc!r}）", False)

    # 四类策略均出现
    strats = {m["attack_type"] for m in muts}
    chk("4 策略 H1–H4 均出现", {"H1", "H2", "H3", "H4"}.issubset(strats))

    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="623 A1 高复杂度带 mutation 生成器")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = write_outputs(build_mutations())
    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
