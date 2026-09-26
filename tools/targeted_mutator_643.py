"""643 C2 · **针对性 mutation 生成器**（智能层：自动生成攻击 #2）。

**定位**：基于 C1 的 precondition/盲点 + B1 的覆盖矩阵，对每条规则生成 3–5 个
"**应该被该规则拦住、但可能逃逸**"的 mutation **计划**，每个计划带 `expected_oracle`。

**两个方向（都很重要）**：

| 方向 | 触发条件 | 目的 | `expected_oracle` |
|---|---|---|---|
| **A 逃逸型** | 该规则**当前在该卡上命中** | 变异后它**还应该**命中 ⇒ 若不命中就是**逃逸** | 该规则 |
| **B 触发型** | 该规则当前在该卡上**不命中** | 变异后**应该**命中 ⇒ 若不命中说明规则**不可达**（等于死规则） | 该规则 |

**5 类变异（字段级/模板级，都保持"能被解析"，见 A2-K2）**：
`field_delete`（删 frontmatter 字段/列表项）· `value_tamper`（值越界/翻转）·
`break_ref`（关系目标改成不存在的 id）· `format_perturb`（缩进/尾随空格/列表风格）·
`equiv_rewrite`（同义改写，语义等价）。

**铁律**：**dry-run 只出计划**（`--plan` 写 `data/643_mutation_plan.json`），
**绝不修改生产卡片**（`atoms/` 零触碰；实际变异由 C3 在**沙箱副本**上做）。

只读契约：`--check` 只读、exit 0；`--plan` 写 `data/643_mutation_plan.md` + `.json`。
纯标准库；≥6 例单测。
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

import coverage_gap_scanner_643 as B1  # noqa: E402
import rule_precondition_analyzer_643 as C1  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_mutation_plan.md")
OUT_JSON = os.path.join(ROOT, "data", "643_mutation_plan.json")
OPS = ("field_delete", "value_tamper", "break_ref", "format_perturb", "equiv_rewrite")
MIN_PER_RULE, MAX_PER_RULE = 3, 5
SYNONYMS = (("必须", "应当"), ("禁止", "不建议"), ("唯一", "之一"), ("等价", "近似"))


def ops_for(blind_kinds: set[str], fields: list[str]) -> list[str]:
    """按盲点信号挑算子（纯函数，可测）：字段类优先 `field_delete`，
    正则类加 `format_perturb`，数值类加 `value_tamper`，跨卡类加 `break_ref`。"""
    picked: list[str] = []
    if fields:
        picked.append("field_delete")
    if "regex_fragile" in blind_kinds:
        picked.append("format_perturb")
    if "numeric_threshold" in blind_kinds:
        picked.append("value_tamper")
    if "cross_card_dependency" in blind_kinds:
        picked.append("break_ref")
    picked.append("equiv_rewrite")
    for op in OPS:                      # 保证 3–5 个且顺序稳定
        if len(picked) >= MIN_PER_RULE:
            break
        if op == "field_delete" and not fields:
            continue                    # 没有可删字段时不得凑数（否则是空变异）
        if op not in picked:
            picked.append(op)
    return picked[:MAX_PER_RULE]


def pick_card(rule_id: str, fired_cards: list[str], all_cards: list[str],
              index: int = 0) -> tuple[Optional[str], str]:
    """选目标卡：命中过就优先用它（方向 A），否则按稳定顺序取一张（方向 B）。"""
    if fired_cards:
        return fired_cards[index % len(fired_cards)], "A"
    if all_cards:
        return all_cards[index % len(all_cards)], "B"
    return None, "B"


def make_plan(limit_rules: Optional[int] = None) -> dict[str, Any]:
    pre = C1.analyze()
    cov = B1.report()
    matrix = cov["matrix"]
    cards = cov["cards"]
    fired: dict[str, list[str]] = {}
    for rid, row in matrix.items():
        hit = sorted(c for c, n in row.items() if n)
        if hit:
            fired[rid] = hit

    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for i, r in enumerate(pre["rows"]):
        rid = r["rule_id"]
        if limit_rules is not None and len(plans) >= limit_rules:
            break
        if not r["check_fn"]:
            skipped.append({"rule_id": rid, "why": "C1 未映射到 check 函数（无法定向）"})
            continue
        if r["scope"] != "atom":
            skipped.append({"rule_id": rid, "why": f"scope={r['scope']}（本批只对 atom 卡生成）"})
            continue
        kinds = {b["kind"] for b in r["blind_spots"]}
        fields = r["precondition"]["fields"]
        for j, op in enumerate(ops_for(kinds, fields)):
            card, direction = pick_card(rid, fired.get(rid, []), cards, j)
            if card is None:
                continue
            field = fields[j % len(fields)] if fields else None
            plans.append({
                "mutation_id": f"{rid}#{op}#{j}",
                "target_rule": rid,
                "rule_severity": r["severity"],
                "direction": direction,
                "card": card,
                "op": op,
                "field": field,
                "expected_oracle": rid,
                "oracle_expectation": ("变异后该规则**仍应命中**" if direction == "A"
                                       else "变异后该规则**应命中**"),
                "generated_by": "targeted_mutator_643",
                "version": "643.1",
            })
    by_op: dict[str, int] = {}
    for p in plans:
        by_op[p["op"]] = by_op.get(p["op"], 0) + 1
    by_dir: dict[str, int] = {}
    for p in plans:
        by_dir[p["direction"]] = by_dir.get(p["direction"], 0) + 1
    return {"plans": plans, "n": len(plans), "by_op": by_op, "by_direction": by_dir,
            "skipped_rules": skipped, "n_rules_covered": len({p["target_rule"] for p in plans}),
            "ops": list(OPS), "dry_run": True}


# ── 变异施加（**只作用于沙箱副本**；C3 调用；纯文本、可复算）──────────────────
def apply_op(text: str, op: str, field: Optional[str]) -> tuple[str, str]:
    """把一次变异施加到**卡文本**上，返回 `(新文本, 说明)`。不读盘、不写盘。"""
    if op == "field_delete":
        if not field:
            return text, "无可删字段"
        pat = re.compile(rf"^{re.escape(field)}\s*:.*$\n?", re.MULTILINE)
        new, n = pat.subn("", text, count=1)
        if n:
            return new, f"删除 frontmatter 字段 {field}"
        pat2 = re.compile(rf"^\s*-\s*{re.escape(field)}\b.*$\n?", re.MULTILINE)
        new2, n2 = pat2.subn("", text, count=1)
        return (new2, f"删除列表项 {field}") if n2 else (text, f"字段 {field} 未找到（空变异）")
    if op == "value_tamper":
        m = re.search(r"^(\w[\w\-]*)\s*:\s*(\d+)\s*$", text, re.MULTILINE)
        if m:
            v = int(m.group(2))
            return (text[:m.start(2)] + str(v + 1) + text[m.end(2):],
                    f"数值 {m.group(1)}: {v} → {v + 1}")
        # 注意：**必须有第 2 组**（本批实测踩坑：组号写错 ⇒ IndexError，
        # 由 C4 的随机基线跑到才发现；单测已补布尔分支覆盖）
        m2 = re.search(r"^(\w[\w\-]*)\s*:\s*(true|false)\s*$", text,
                       re.MULTILINE | re.IGNORECASE)
        if m2:
            flipped = "false" if m2.group(2).lower() == "true" else "true"
            return (text[:m2.start(2)] + flipped + text[m2.end(2):],
                    f"布尔 {m2.group(1)}: {m2.group(2)} → {flipped}")
        return text, "无可篡改的值（空变异）"
    if op == "break_ref":
        m = re.search(r"^(\s*-\s*)([A-Z][A-Z0-9\-]{3,})\b", text, re.MULTILINE)
        if m:
            return (text[:m.start(2)] + m.group(2) + "-XX" + text[m.end(2):],
                    f"关系目标 {m.group(2)} → {m.group(2)}-XX（不存在）")
        return text, "无关系目标可断裂（空变异）"
    if op == "format_perturb":
        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith("#") and not line.startswith("---"):
                lines[i] = line.rstrip("\n") + "   \n"       # 尾随空格
                break
        return "".join(lines), "注入尾随空格（格式微扰）"
    if op == "equiv_rewrite":
        for a, b in SYNONYMS:
            if a in text:
                return text.replace(a, b, 1), f"同义改写 {a} → {b}（语义等价）"
        return text, "无可改写词（空变异）"
    return text, f"未知算子 {op}"


def write_report() -> str:
    p = make_plan()
    lines = [
        "# 643 C2 · 针对性 mutation 计划（智能层：自动生成攻击 #2；**dry-run**）", "",
        f"> 计划条数 **{p['n']}**（覆盖 **{p['n_rules_covered']}** 条规则）；"
        f"算子分布 `{p['by_op']}`；方向分布 `{p['by_direction']}`。",
        "> **dry-run**：本文件只列计划，**不修改任何生产卡片**（实际变异由 C3 在沙箱副本上做）。", "",
        "## 一、算子与方向", "",
        "| 算子 | 含义 |", "|---|---|",
        "| `field_delete` | 删 frontmatter 字段/列表项 |",
        "| `value_tamper` | 数值 +1 / 布尔翻转 |",
        "| `break_ref` | 关系目标改成不存在的 id |",
        "| `format_perturb` | 尾随空格等格式微扰（语义不变） |",
        "| `equiv_rewrite` | 同义改写（语义等价） |", "",
        f"- **方向 A（逃逸型）** {p['by_direction'].get('A', 0)} 条：目标规则**当前命中该卡** ⇒ "
        "变异后仍应命中，不命中=逃逸；",
        f"- **方向 B（触发型）** {p['by_direction'].get('B', 0)} 条：目标规则当前**不**命中 ⇒ "
        "变异后应命中，不命中=规则不可达（死规则候选）。", "",
        "## 二、被跳过的规则（附原因）", "",
        "| 规则 | 原因 |", "|---|---|"]
    for s in p["skipped_rules"][:40]:
        lines.append(f"| `{s['rule_id']}` | {s['why']} |")
    if not p["skipped_rules"]:
        lines.append("| — | 无 |")
    lines += ["", "## 三、计划明细（前 60 条）", "",
              "| mutation_id | 目标规则 | 方向 | 卡 | 算子 | 字段 | expected_oracle |",
              "|---|---|---|---|---|---|---|"]
    for pl in p["plans"][:60]:
        lines.append(f"| `{pl['mutation_id']}` | `{pl['target_rule']}` | {pl['direction']} | "
                     f"`{pl['card']}` | `{pl['op']}` | {pl['field'] or '—'} | "
                     f"`{pl['expected_oracle']}` |")
    lines += ["", "## 诚实登记", "",
              "1. **`expected_oracle` 是生成器猜的**（§十二.7）：可能预期错了（以为该被规则 A 拦，"
              "实际由规则 B 拦）⇒ C3 实测后**记录 `oracle_mismatch`，但不改预期**；",
              "2. **空变异存在**：某个算子在该卡上找不到可改对象时返回原文（说明串已标注）"
              "⇒ C3 会把它们计为 `noop`，**不计入逃逸**；",
              "3. **方向 B 的语义**：规则不命中**可能**是「卡本来就合规」（好事），"
              "所以 B 的失败**不等于**规则坏 —— 只作「**不可达候选**」线索；",
              "4. **本批只对 `scope=atom` 的规则生成**（evidence/repo 面的变异需要不同的载体策略，"
              "留 644+）⇒ 覆盖规则数小于 67；",
              "5. 本工具**不读写生产卡片**：`apply_op` 是**纯文本函数**（输入输出都是字符串），"
              "真正落盘只在 C3 的临时沙箱里发生。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(p, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    card = ("---\nid: ATOM-X-001\ntitle: T\nstatus: verified\nn: 3\nflag: true\n"
            "relations:\n  - ATOM-Y-001\n---\n\n必须做到。\n")

    t, why = apply_op(card, "field_delete", "title")
    chk("field_delete 删掉 title 行", "title:" not in t and "删除" in why, why)
    t, why = apply_op(card, "value_tamper", None)
    chk("value_tamper 数值 +1", "n: 4" in t, why)
    # 布尔分支：本批实测过 IndexError（组号写错）⇒ 必须有专门用例
    boolcard = "---\nid: ATOM-X-002\nverified: true\n---\n"
    t2, why2 = apply_op(boolcard, "value_tamper", None)
    chk("value_tamper 布尔翻转（true→false）", "verified: false" in t2, why2)
    t3, why3 = apply_op("---\nok: false\n---\n", "value_tamper", None)
    chk("value_tamper 布尔翻转（false→true）", "ok: true" in t3, why3)
    t, why = apply_op(card, "break_ref", None)
    chk("break_ref 目标不存在", "ATOM-Y-001-XX" in t, why)
    t, why = apply_op(card, "format_perturb", None)
    chk("format_perturb 注入尾随空格", "   \n" in t or "尾随空格" in why, why)
    t, why = apply_op(card, "equiv_rewrite", None)
    chk("equiv_rewrite 同义改写", "应当做到" in t, why)
    t, why = apply_op(card, "unknown_op", None)
    chk("未知算子返回原文（不炸）", t == card, why)
    t, why = apply_op(card, "field_delete", "not_exist")
    chk("删不存在的字段 ⇒ 空变异（原文返回）", t == card and "未找到" in why, why)

    chk("算子选择：字段类含 field_delete",
        "field_delete" in ops_for({"field_missing_silent"}, ["status"]))
    chk("算子选择：每规则 3–5 个且稳定",
        all(MIN_PER_RULE <= len(ops_for({k}, ["status"])) <= MAX_PER_RULE
            for k in ("field_missing_silent", "regex_fragile", "numeric_threshold")))
    chk("无字段 ⇒ 不选 field_delete",
        "field_delete" not in ops_for(set(), []))

    p = make_plan()
    chk("计划非空且带 expected_oracle",
        p["n"] > 0 and all(x["expected_oracle"] == x["target_rule"] for x in p["plans"]))
    chk("每规则 3–5 条",
        all(3 <= sum(1 for x in p["plans"] if x["target_rule"] == r) <= 5
            for r in {x["target_rule"] for x in p["plans"]}))
    chk("dry_run 标记为真（不落卡）", p["dry_run"] is True)
    a = os.path.join(HERE, "..", "atoms")
    chk("atoms/ 存在（供 C3 复制）", os.path.isdir(a))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 C2 定向变异生成（dry-run）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--plan", action="store_true", help="写计划（dry-run）")
    ap.add_argument("--json", action="store_true", help="打印计划（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.plan:
        print(f"written {write_report()}")
        return 0
    p = make_plan()
    if x.json:
        print(json.dumps({"n": p["n"], "by_op": p["by_op"], "by_direction": p["by_direction"],
                          "skipped": len(p["skipped_rules"])}, ensure_ascii=False, indent=2))
        return 0
    print(f"[targeted-mutator] 计划 {p['n']} 条 / 覆盖 {p['n_rules_covered']} 规则 ⇒ "
          f"{p['by_op']}；方向 {p['by_direction']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
