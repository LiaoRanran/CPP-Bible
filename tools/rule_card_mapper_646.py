"""646 · 阶段 A1 · 规则→卡显式映射（清债 1，最核心）。

目标（646 §三 A1）：建 67 规则 × 27 卡的多对多映射表，让智能层发现的**规则问题**能自动找到
对应**卡片**的证据，从而打通三层耦合（645 债 1 的根因=规则↔卡非 1:1、无显式映射）。

匹配信号（三路，可解释）：
1. **适用性子句（property）**：按规则主题判定它作用于「具备某属性的卡」——如 EV-* → 有证据的卡、
   `*REL*` → 有 relations 的卡、`*GRAY*` → UB 域卡、`*MISCONCEPTION*` → 有 misconceptions 的卡、
   `*CLAIM*/OBSERVATION/INFERENCE` → 有 claim_structured 的卡、`S1-*/VERIFY/GOLDEN` → 已 verified 卡。
2. **关键词重叠**：规则 id 去掉通用词后的 token 与卡片 id/title/claim 的英文 token 重叠数。
3. **域信号**：规则 token 与卡片 domain 一致（mem/conc/hist/lang/ub）。

强度：`high`（专属属性命中 或 关键词重叠 ≥2 或 域+任一）> `medium`（宽属性/单关键词/域）> `low`（全局结构规则的兜底）。

**只读**：不改规则、不改卡片、不改账本。卡片域 = 真实 `evidence_base_644.list_atoms()`（27 张，见 646 §三.1
幻影卡修正）。`--check` 只读自检；`--map` 真实映射，写 `data/646_rule_card_mapping.json` + `.md`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_JSON = os.path.join(DATA, "646_rule_card_mapping.json")
REPORT_MD = os.path.join(DATA, "646_rule_card_mapping.md")

# 规则 id 中的通用词（不参与关键词匹配）
GENERIC = {
    "ATOM", "EV", "MIS", "DOC", "META", "S1", "S2", "S3", "HC", "REQUIRED", "EXISTS",
    "FORMAT", "VALUE", "UNIQUE", "MATCH", "LEVELS", "SERVES", "DECLARED", "BOUND",
    "TRANSITION", "VERSION", "HARDENING", "DEPENDENT", "CANONICAL", "NOT",
}
# 规则 → 适用属性（按主题，顺序敏感，先命中先定）
PROPERTY_RULES = [
    ("GRAY", "domain_ub", "high", "灰色地带规则 → UB 域卡"),
    ("MISCONCEPTION", "has_misconceptions", "high", "误解类规则 → 有 misconceptions 的卡"),
    ("REL", "has_relations", "high", "关系类规则 → 有 relations 的卡"),
    ("ARTIFACT", "has_evidence", "medium", "工件/证据类规则 → 有证据的卡"),
    ("EVIDENCE", "has_evidence", "medium", "证据类规则 → 有证据的卡"),
    ("OBSERVATION", "has_claim_structured", "medium", "observation 命题规则 → 有 claim_structured 的卡"),
    ("INFERENCE", "has_claim_structured", "medium", "inference 命题规则 → 有 claim_structured 的卡"),
    ("CLAIM", "has_claim_structured", "medium", "命题类规则 → 有 claim_structured 的卡"),
    ("PREREQ", "has_prereq", "high", "前置规则 → 有 prerequisites_readable 的卡"),
    ("AUDIENCE", "has_audience", "medium", "认知适切规则 → 有 audience 的卡"),
    ("PED", "has_pedagogy", "medium", "教学规则 → 有 pedagogy 的卡"),
    ("SUPERIORITY", "has_superiority", "medium", "洞见规则 → 有 superiority 的卡"),
    ("HYBRID", "has_superiority", "medium", "混合评审规则 → 有 superiority 的卡"),
    ("GOLDEN", "verified", "medium", "Golden 规则 → 已 verified 的卡"),
    ("VERIFY", "verified", "medium", "签收规则 → 已 verified 的卡"),
    ("DAL", "has_dal", "medium", "DAL 规则 → 有 dal 的卡"),
    ("EV-", "has_evidence", "medium", "证据类通用规则 → 有证据的卡"),
    ("STATUS", "has_status", "medium", "状态规则 → 有 status 的卡"),
    ("ID-", "all", "low", "身份/格式规则 → 适用全部卡"),
    ("FM-", "all", "low", "字段完整性规则 → 适用全部卡"),
]


def _rule_tokens(rid: str) -> set[str]:
    """规则 id 的有意义 token（去通用词/纯数字）。"""
    toks = {t.lower() for t in re.split(r"[-_\s]", rid) if t}
    return {t for t in toks if t.upper() not in GENERIC and not t.isdigit()}


def _card_tokens(atom: dict) -> set[str]:
    """卡片 token：id 段 + title/claim/domain/type 中的英文词（含 CamelCase 拆分）。"""
    m = atom["meta"]
    toks = {t.lower() for t in atom["id"].split("-")
            if t.upper() != "ATOM" and not t.isdigit()}
    text = " ".join(str(m.get(k, "")) for k in ("title", "claim", "domain", "type"))
    toks |= {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text)}
    return toks


def _card_caps(atom: dict, ev_by_card: dict) -> dict:
    """卡片能力（供适用性子句判定）。"""
    m = atom["meta"]
    return {
        "domain": str(m.get("domain", "")).lower(),
        "domain_ub": str(m.get("domain", "")).upper() == "UB",
        "has_evidence": bool(ev_by_card.get(atom["id"])),
        "has_relations": bool(m.get("relations")),
        "has_claim_structured": bool(m.get("claim_structured")),
        "has_misconceptions": bool(m.get("misconceptions")),
        "has_audience": bool(m.get("audience")),
        "has_pedagogy": bool(m.get("pedagogy")),
        "has_prereq": bool(m.get("prerequisites_readable")),
        "has_superiority": bool(m.get("superiority")),
        "has_dal": bool(m.get("dal")),
        "has_status": bool(m.get("status")),
        "verified": str(m.get("status", "")).lower() == "verified",
    }


def _applicability(rid: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """返回 (属性名, 强度, 依据)；未命中属性规则返回 (None, None, None)。"""
    up = rid.upper()
    for key, prop, strength, basis in PROPERTY_RULES:
        if key in up:
            return prop, strength, basis
    return None, None, None


def build_mapping() -> dict:
    """真实构建 67 规则 × 27 卡映射。"""
    import gate_engine as ge
    import perf_646 as perf  # A3：进程内记忆化（只读），消除重复读盘
    atoms = list(perf.atoms())
    # 证据→卡（真实 card_evidence_map + 落库记录 meta.card，均为缓存读）
    ev_by_card: dict[str, list] = {}
    for card, evs in perf.card_evidence_map().items():
        ev_by_card.setdefault(card, []).extend(evs)
    for eid, _grade, _cred, _src, card in perf.stored_records():
        if card:
            ev_by_card.setdefault(card, []).append(eid)

    caps = {a["id"]: _card_caps(a, ev_by_card) for a in atoms}
    ctok = {a["id"]: _card_tokens(a) for a in atoms}

    rules_out: dict[str, dict] = {}
    strength_count = {"high": 0, "medium": 0, "low": 0}
    for rule in ge.RULES:
        rid = rule.id
        rtok = _rule_tokens(rid)
        prop, pstrength, pbasis = _applicability(rid)
        cards = []
        for aid, cap in caps.items():
            bases = []
            rank = 0  # 0 无 / 1 low / 2 medium / 3 high
            if prop == "all":
                bases.append("全局规则适用全部卡")
                rank = max(rank, 1)
            elif prop is not None and cap.get(prop):
                bases.append(pbasis or f"属性 {prop}")
                rank = max(rank, 3 if pstrength == "high" else 2)
            # 关键词重叠
            overlap = rtok & ctok[aid]
            if len(overlap) >= 2:
                bases.append(f"关键词重叠 {sorted(overlap)}")
                rank = 3
            elif len(overlap) == 1:
                bases.append(f"关键词命中 {sorted(overlap)}")
                rank = max(rank, 2)
            # 域信号
            if cap["domain"] and cap["domain"] in rtok:
                bases.append(f"域匹配 {cap['domain']}")
                rank = max(rank, 2)
            if rank == 0:
                continue
            strength = {1: "low", 2: "medium", 3: "high"}[rank]
            cards.append({"card": aid, "strength": strength, "basis": "；".join(bases)})
            strength_count[strength] += 1
        if not cards:
            # 兜底：未分类规则按全局规则处理（low × 全部卡），保证无孤儿规则
            for aid in caps:
                cards.append({"card": aid, "strength": "low",
                              "basis": "未分类规则全局兜底"})
                strength_count["low"] += 1
        rules_out[rid] = {
            "title": getattr(rule, "title", ""),
            "severity": getattr(rule, "severity", ""),
            "card_count": len(cards),
            "cards": cards,
        }
    # 覆盖率：每张卡被多少规则命中
    card_hits: dict[str, int] = {a["id"]: 0 for a in atoms}
    for r in rules_out.values():
        for c in r["cards"]:
            card_hits[c["card"]] += 1
    return {
        "rule_count": len(rules_out),
        "card_count": len(atoms),
        "strength_count": strength_count,
        "rules_with_mapping": sum(1 for r in rules_out.values() if r["cards"]),
        "card_hits": card_hits,
        "rules": rules_out,
    }


def write_report(result: dict) -> None:
    """写 `data/646_rule_card_mapping.json`（全量）+ `.md`（摘要）。"""
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)
    lines = ["# 646 规则→卡映射报告（A1，清债 1）", "",
             f"- 规则数：{result['rule_count']}",
             f"- 卡片数：{result['card_count']}（真实原子卡，见 646 §三.1）",
             f"- 有映射的规则：{result['rules_with_mapping']}",
             f"- 映射条目强度分布：{result['strength_count']}",
             f"- 每卡被命中规则数（min/max）："
             f"{min(result['card_hits'].values())}/{max(result['card_hits'].values())}", ""]
    lines.append("## 每规则映射卡数（前 25）")
    for rid, info in list(result["rules"].items())[:25]:
        lines.append(f"- `{rid}`（{info['severity']}）：{info['card_count']} 卡")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def selftest() -> int:
    """只读自检：已知关联必命中（GRAY→UB 卡 high；MISCONCEPTION→有误解的卡）。"""
    m = build_mapping()
    assert m["card_count"] == 27, m["card_count"]
    # GRAY 规则 → UB 卡 high
    gray = m["rules"].get("ATOM-GRAY-ZONE")
    assert gray and any(c["card"] == "ATOM-UB-GRAY-001" and c["strength"] == "high"
                        for c in gray["cards"]), gray
    # MISCONCEPTION 规则 → 至少一张有 misconceptions 的卡
    mis = m["rules"].get("ATOM-MISCONCEPTION-LEVELS")
    assert mis and mis["cards"], mis
    # 每条规则都应至少映射到 1 张卡（无孤儿规则）
    assert m["rules_with_mapping"] == m["rule_count"]
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--map` 真实构建映射。"""
    ap = argparse.ArgumentParser(description="646 规则→卡映射（A1）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--map", action="store_true", help="真实构建映射")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = build_mapping()
    write_report(result)
    print(f"[646 mapper] 规则={result['rule_count']} 卡={result['card_count']} "
          f"强度={result['strength_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
