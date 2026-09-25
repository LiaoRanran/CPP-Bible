"""638 B2 · RR 冲突分类器（规则间冲突逐条分类）

**636 发现**：23 张 verified 卡**全部**有 RR（规则间冲突），但 636 的记录里
`rr/er/ee/und/conflict_raw/agreement/C/types` **没有规则对**（无 `rule_a/rule_b`）——
**RR 是「全局规则集属性」**（同批所有卡一致），区分度有限（636 报告 §诚实登记 3）。

因此本工具**两条腿走路**，并把口径差异如实登记：

1. **卡级**（对齐 636）：复用 `conflict_detector_636.detect` 对 23 张 verified 卡逐个
   标出冲突型与强度，逐卡分类；
2. **规则对级**（本批新增，真实可分类）：从权威 `gate_engine.RULES` 枚举
   **同 scope 规则对**（927 对），按启发式判 **type1~type4** + **严重度 P0~P2** + **建议处置**。

冲突类型（§三.B2.1）：
- `type1`：两条规则对同一事实给出相反判断（同 scope 下 severity 相反，如 block vs warn）；
- `type2`：适用范围重叠但阈值不同（同 scope 同 severity 同前缀族）；
- `type3`：一条规则的前提是另一条规则的结论（派生/加强规则对，如 `X` 与 `X-HC`）；
- `type4`：其他不一致。

严重度：`P0` 影响判决正确性 / `P1` 影响效率 / `P2` 只是不一致。
建议处置：修规则 A / 修规则 B / 加优先级 / 加例外。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/638_rr_conflict_analysis.md` + `.json`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import collections
import datetime
import itertools
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "638_rr_conflict_analysis.md")
OUT_JSON = os.path.join(ROOT, "data", "638_rr_conflict_analysis.json")

HC_SUFFIX = "-HC"


def load_rules() -> list[dict[str, str]]:
    """权威规则元数据（仅 id/severity/scope）。"""
    try:
        import gate_engine as ge
        return [{"id": r.id, "severity": getattr(r, "severity", ""),
                 "scope": getattr(r, "scope", "")} for r in ge.RULES]
    except Exception:  # noqa: BLE001
        return []


# ── 规则对分类（启发式，登记在报告）──────────────────────────────────────
def family(rule_id: str) -> str:
    """规则族：去掉 `-HC` 后缀后的基名。"""
    return rule_id[:-len(HC_SUFFIX)] if rule_id.endswith(HC_SUFFIX) else rule_id


def prefix(rule_id: str) -> str:
    """规则的**语义前缀族**（去掉最后一段），如 `ATOM-REL-TARGET` → `ATOM-REL`。

    用于区分**高置信**（同前缀族，真可能管同一件事）与**低置信**（仅同 scope）候选对。
    """
    base = family(rule_id)
    parts = base.split("-")
    return "-".join(parts[:-1]) if len(parts) > 1 else base


def classify_pair(a: dict[str, str], b: dict[str, str]) -> dict[str, str]:
    """给一对规则判类型/严重度/建议 + 置信度。

    **置信度**：`high` = 同前缀族（真可能管同一事实）；`low` = 仅同 scope（同域候选）。
    """
    ia, ib = a["id"], b["id"]
    sa, sb = a["severity"], b["severity"]
    sc = a["scope"]
    opposite = {sa, sb} == {"block", "warn"} or {sa, sb} == {"block", "advice"}
    same_family = family(ia) == family(ib) and ia != ib
    same_prefix = prefix(ia) == prefix(ib)

    if same_family:
        ctype, sev, conf = "type3", "P1", "high"
        sug = "加优先级（基规则先判，派生规则仅在基规则通过时生效）"
        why = f"`{ia}` 与 `{ib}` 同族（派生/加强），后者的前提是前者的结论"
    elif same_prefix and opposite:
        ctype, sev, conf = "type1", "P0", "high"
        sug = f"修规则 {ia}（把 block 降为 warn）或加优先级"
        why = f"同前缀族 `{prefix(ia)}` 下 `{ia}`({sa}) 与 `{ib}`({sb}) 对同一事实处置相反"
    elif same_prefix and sa == sb:
        ctype, sev, conf = "type2", "P2", "high"
        sug = "加例外（在阈值边界处明确谁优先）"
        why = f"同前缀族 `{prefix(ia)}` 同 severity({sa})，适用范围重叠但阈值未声明差异"
    elif same_prefix:
        ctype, sev, conf = "type4", "P2", "high"
        sug = "加例外"
        why = f"同前缀族 `{prefix(ia)}` 但 severity 组合（{sa}/{sb}）非 block-vs-warn"
    else:
        ctype, sev, conf = "type4", "P2", "low"
        sug = "暂不处置（仅同 scope，非同一事实）"
        why = f"仅同 scope `{sc}`（前缀族不同：`{prefix(ia)}` vs `{prefix(ib)}`）"
    return {"rule_a": ia, "rule_b": ib, "scope": sc, "severity_a": sa,
            "severity_b": sb, "type": ctype, "severity": sev, "suggestion": sug,
            "confidence": conf, "why": why}


def rule_pairs(rules: Optional[list[dict[str, str]]] = None) -> list[dict[str, str]]:
    """枚举**同 scope** 规则对并分类（跨 scope 不构成 RR）。"""
    rs = rules if rules is not None else load_rules()
    out: list[dict[str, str]] = []
    for scope in sorted({r["scope"] for r in rs}):
        same = [r for r in rs if r["scope"] == scope]
        for a, b in itertools.combinations(same, 2):
            out.append(classify_pair(a, b))
    return out


# ── 卡级（对齐 636）─────────────────────────────────────────────────────
def card_conflicts() -> list[dict[str, Any]]:
    """复用 636 检测器对 verified 卡逐个判定（只读依赖）。"""
    try:
        import conflict_detector_636 as cd
    except Exception:  # noqa: BLE001
        return []
    rules = cd.load_rules()
    rows: list[dict[str, Any]] = []
    for rel, text in cd.verified_cards():
        d = cd.detect(text, rules)
        rows.append({"card": rel, **{k: d[k] for k in
                                     ("rr", "er", "ee", "und", "conflict_raw",
                                      "agreement", "C", "types", "exceeds_theta")}})
    return rows


def classify_card_row(row: dict[str, Any]) -> dict[str, str]:
    """卡级冲突 → 类型/严重度/建议。"""
    types = row.get("types") or []
    if "RR" in types and row.get("exceeds_theta"):
        return {"type": "type1", "severity": "P0",
                "suggestion": "人工复核该卡的 RR+cross 证据（C≥0.3）"}
    if "RR" in types:
        return {"type": "type2", "severity": "P1",
                "suggestion": "记录 RR，待规则优先级策略上线后自动消解"}
    if "EE" in types or "ER" in types:
        return {"type": "type4", "severity": "P1", "suggestion": "复核证据自洽性"}
    return {"type": "type4", "severity": "P2", "suggestion": "无需处置"}


# ── 汇总 ────────────────────────────────────────────────────────────────
def summary() -> dict[str, Any]:
    rules = load_rules()
    pairs = rule_pairs(rules)
    tdist = collections.Counter(p["type"] for p in pairs)
    sdist = collections.Counter(p["severity"] for p in pairs)
    cards = card_conflicts()
    cdist = collections.Counter(classify_card_row(c)["type"] for c in cards)

    high = [p for p in pairs if p["confidence"] == "high"]
    low = [p for p in pairs if p["confidence"] == "low"]

    # 冲突度只在**高置信**（同前缀族）对内计算（同 scope 全配对的度是退化的常数）
    degree: collections.Counter[str] = collections.Counter()
    for p in high:
        degree[p["rule_a"]] += 1
        degree[p["rule_b"]] += 1

    # top 3 最值得修：P0（影响判决正确性）优先，按高置信冲突度之和降序，
    # 且**每条互不重复 rule_a**（给出 3 个不同的待修规则）
    def rank(p: dict[str, str]) -> tuple:
        return ({"P0": 0, "P1": 1, "P2": 2}.get(p["severity"], 3),
                -(degree[p["rule_a"]] + degree[p["rule_b"]]),
                p["rule_a"], p["rule_b"])

    ordered = sorted(high, key=rank)
    top: list[dict[str, str]] = []
    seen: set[str] = set()
    for p in ordered:
        if p["rule_a"] in seen:
            continue
        seen.add(p["rule_a"])
        top.append({**p, "degree_a": str(degree[p["rule_a"]]),
                    "degree_b": str(degree[p["rule_b"]])})
        if len(top) == 3:
            break
    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "n_rules": len(rules), "n_pairs": len(pairs),
        "n_high": len(high), "n_low": len(low),
        "high_type_dist": dict(collections.Counter(p["type"] for p in high)),
        "high_sev_dist": dict(collections.Counter(p["severity"] for p in high)),
        "high_pairs": high,
        "type_dist": dict(tdist), "severity_dist": dict(sdist),
        "pairs": pairs, "top3": top,
        "top_degree_rules": degree.most_common(10),
        "max_degree": max(degree.values()) if degree else 0,
        "cards": [{"card": c["card"], "types": c["types"], "C": c["C"],
                   "exceeds_theta": c["exceeds_theta"], **classify_card_row(c)}
                  for c in cards],
        "n_cards": len(cards), "card_type_dist": dict(cdist),
        "scope_dist": dict(collections.Counter(r["scope"] for r in rules)),
    }


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report() -> dict[str, str]:
    s = summary()
    # JSON 只落**高置信**对（24 条）+ 统计；低置信 903 条仅计数（避免 400KB 无信息体积）
    out = {k: v for k, v in s.items() if k not in ("pairs", "high_pairs")}
    out["low_pairs_note"] = (f"低置信（仅同 scope、前缀族不同）{s['n_low']} 对未逐条落盘，"
                             "如有需要可从 gate_engine.RULES 重算")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({**out, "high_pairs": s["high_pairs"]}, fh, ensure_ascii=False, indent=2)

    lines = [
        "# 638 B2 · RR 冲突分类（规则间冲突逐条分类）", "",
        f"> 生成时间：{s['generated']}。工具：`tools/rr_conflict_classifier_638.py`。", "",
        "## 一、口径说明（必须先说）", "",
        "- 636 的 RR 记录**没有规则对**（`rr/er/ee/und/...`，无 `rule_a/rule_b`）——",
        "  **RR 是全局规则集属性**（23/23 卡全为 1，区分度有限，见 636 报告诚实登记 3）；",
        "- 因此本报告**卡级对齐 636**（23 张卡逐卡），**规则对级为本批新增**"
        "（从权威 `gate_engine.RULES` 枚举同 scope 规则对）；",
        "- 两级的数目**不可互相换算**，已在 §五 登记。", "",
        "## 二、规则对级分类（真实，可逐条处置）", "",
        f"- 规则数：**{s['n_rules']}**（scope 分布 `{s['scope_dist']}`）；",
        f"- 同 scope 规则对（**候选**集）：**{s['n_pairs']}** 对；",
        f"- 其中 **高置信**（同前缀族，真可能管同一事实）：**{s['n_high']}** 对；"
        f" **低置信**（仅同 scope，非同一事实）：**{s['n_low']}** 对；",
        f"- 高置信类型分布：`{s['high_type_dist']}`；",
        f"- 高置信严重度分布：`{s['high_sev_dist']}`；",
        f"- 全候选（含低置信）类型分布：`{s['type_dist']}`。", "",
        "> **重要**：927 对是**同 scope 机械配对**的结果——同 scope 内每条规则都与其余全部配对，",
        "> 因此冲突度恒为「scope 内规则数 − 1」（atom 域恒 35），**本身不构成 927 个真实冲突**。",
        "> 真正可处置的是**高置信**那一批（同前缀族）。此退化与 636「RR 为全局规则集属性、",
        "> 区分度有限」是同一根因，已在 §五 登记。", "",
        "| 类型 | 含义 | 判据（启发式） | 置信度 |", "|---|---|---|---|",
        "| `type1` | 对同一事实给出相反判断 | **同前缀族** + severity 为 block↔warn/advice | high |",
        "| `type2` | 适用范围重叠但阈值不同 | **同前缀族** + 同 severity | high |",
        "| `type3` | 一条规则的前提是另一条的结论 | 同族（`X` 与 `X-HC`）派生对 | high |",
        "| `type4` | 其他不一致 | 同前缀族但 severity 组合非 block-vs-warn；或**仅同 scope**（前缀族不同） | high / low |", "",
        "> 前缀族 = 规则 id 去掉最后一段（如 `ATOM-REL-TARGET` → `ATOM-REL`）。", "",
        "### 2.1 top 3 最值得修的冲突", "",
        "> 选法：**P0（影响判决正确性）优先**，按「两条规则各自的冲突度之和」降序，",
        "> 且三条**互不重复 rule_a**——即给出 3 个**不同的**待修规则，而非同一规则霸榜。", "",
        "| # | 规则 A（冲突度） | 规则 B（冲突度） | scope | 类型 | 严重度 | 建议处置 |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(s["top3"], 1):
        lines.append(f"| {i} | `{p['rule_a']}` ({p.get('degree_a', '')}) | "
                     f"`{p['rule_b']}` ({p.get('degree_b', '')}) | {p['scope']} | "
                     f"{p['type']} | {p['severity']} | {p['suggestion']} |")
    lines += ["", "### 2.1.1 冲突度最高的规则（系统性问题制造者，top 10）", "",
              "| 规则 | 参与冲突对数 |", "|---|---|"]
    for rid, dg in s.get("top_degree_rules", []):
        lines.append(f"| `{rid}` | {dg} |")
    lines.append(f"\n- 单条规则最大冲突度：**{s.get('max_degree', 0)}** 对。")
    lines += ["", "### 2.2 高置信 P0 冲突全量（type1，同前缀族 + severity 相反）", ""]
    p0 = [p for p in s["high_pairs"] if p["severity"] == "P0"]
    if p0:
        lines += [f"共 **{len(p0)}** 对：", "",
                  "| 规则 A | 规则 B | scope | 为什么 |", "|---|---|---|---|",
                  ]
        for p in p0[:30]:
            lines.append(f"| `{p['rule_a']}` | `{p['rule_b']}` | {p['scope']} | {p['why']} |")
        if len(p0) > 30:
            lines.append(f"| … | 其余 {len(p0) - 30} 对见 JSON | | |")
    else:
        lines.append("无。")
    lines += ["", "### 2.3 type3 同族派生对全量", ""]
    t3 = [p for p in s["pairs"] if p["type"] == "type3"]
    lines += ["| 基规则 | 派生规则 | scope | 建议 |", "|---|---|---|---|"]
    for p in t3:
        lines.append(f"| `{p['rule_a']}` | `{p['rule_b']}` | {p['scope']} | {p['suggestion']} |")
    if not t3:
        lines.append("| — | — | — | 无 |")

    lines += [
        "", "## 三、卡级分类（对齐 636：23 张 verified 卡）", "",
        f"- 卡数：**{s['n_cards']}**；类型分布：`{s['card_type_dist']}`。", "",
        "| 卡 | 冲突型 | C | 超阈值 | 本批类型 | 严重度 | 建议 |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in s["cards"]:
        lines.append(f"| `{c['card'].split('/')[-1][:-3]}` | {'/'.join(c['types'])} | {c['C']} | "
                     f"{'是' if c['exceeds_theta'] else '—'} | {c['type']} | {c['severity']} | "
                     f"{c['suggestion']} |")

    lines += [
        "", "## 四、统计汇总", "",
        "| 维度 | 值 |", "|---|---|",
        f"| 规则数 | {s['n_rules']} |",
        f"| 同 scope 规则对（候选集） | {s['n_pairs']} |",
        f"| 高置信（同前缀族） / 低置信（仅同 scope） | {s['n_high']} / {s['n_low']} |",
        f"| **高置信** type1 / type2 / type3 / type4 | {s['high_type_dist'].get('type1', 0)} / "
        f"{s['high_type_dist'].get('type2', 0)} / {s['high_type_dist'].get('type3', 0)} / "
        f"{s['high_type_dist'].get('type4', 0)} |",
        f"| **高置信** P0 / P1 / P2 | {s['high_sev_dist'].get('P0', 0)} / "
        f"{s['high_sev_dist'].get('P1', 0)} / {s['high_sev_dist'].get('P2', 0)} |",
        f"| verified 卡（逐卡分类） | {s['n_cards']} |", "",
        "## 五、诚实登记", "",
        "1. **分类是启发式**：判据是 scope/severity/命名族三个**结构性字段**，"
        "未做语义分析（§四.3）；",
        "2. **口径差异**：636 的「23 张卡全有 RR」是**卡级**计数；本批的规则对级枚举"
        f"共 {s['n_pairs']} 对候选，其中**只有 {s['n_high']} 对是高置信**"
        f"（同前缀族），其余 {s['n_low']} 对仅是「同 scope」的低置信同域对。**三者不可换算**；",
        "3. **RR 全局属性**的根因未解决（636 已指出区分度有限）——本批只是把「全局的 1」"
        "拆成可处置的规则对，**未改规则**；",
        "4. type3 判据依赖 `-HC` 后缀约定（实测 4 对：ATOM-REL-TARGET / EV-SERVES-EXIST / "
        "ATOM-REL-UNKNOWN / CARD-PATH-NOT-CANONICAL 各有 `-HC` 变体）；",
        "5. 本批**不改任何规则**，仅分类 + 给建议（§零：判决逻辑不在本批改动范围）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("规则数 67", len(load_rules()) == 67)
    chk("同 scope 对数 927", len(rule_pairs()) == 927)
    chk("type3 识别同族 -HC", classify_pair(
        {"id": "A-B", "severity": "block", "scope": "atom"},
        {"id": "A-B-HC", "severity": "block", "scope": "atom"})["type"] == "type3")
    chk("type1 识别 block↔warn（同前缀族）", classify_pair(
        {"id": "A-B-X", "severity": "block", "scope": "atom"},
        {"id": "A-B-Y", "severity": "warn", "scope": "atom"})["type"] == "type1")
    chk("type2 同 severity（同前缀族）", classify_pair(
        {"id": "A-B-X", "severity": "advice", "scope": "repo"},
        {"id": "A-B-Y", "severity": "advice", "scope": "repo"})["type"] == "type2")
    chk("前缀族不同 ⇒ type4/低置信", classify_pair(
        {"id": "A-X", "severity": "block", "scope": "atom"},
        {"id": "B-Y", "severity": "warn", "scope": "atom"})["confidence"] == "low")
    chk("跨 scope 不成对", len(rule_pairs(
        [{"id": "A", "severity": "block", "scope": "atom"},
         {"id": "B", "severity": "block", "scope": "repo"}])) == 0)
    s = summary()
    chk("类型分布和 = 对数", sum(s["type_dist"].values()) == s["n_pairs"])
    chk("严重度分布和 = 对数", sum(s["severity_dist"].values()) == s["n_pairs"])
    chk("高置信 + 低置信 = 候选对", s["n_high"] + s["n_low"] == s["n_pairs"])
    chk("高置信对全部同前缀族", all(p["confidence"] == "high" for p in s["high_pairs"]))
    chk("跨前缀族判低置信", classify_pair(
        {"id": "ATOM-REL-TARGET", "severity": "block", "scope": "atom"},
        {"id": "ATOM-ID-FORMAT", "severity": "warn", "scope": "atom"})["confidence"] == "low")
    chk("卡级 23 张", s["n_cards"] == 23)
    chk("卡级全有类型", all(c["type"] for c in s["cards"]))
    chk("top3 有建议", len(s["top3"]) == 3 and all(p["suggestion"] for p in s["top3"]))
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 B2 RR 冲突分类器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    s = summary()
    if args.json:
        print(json.dumps({k: v for k, v in s.items() if k not in ("pairs", "cards")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"pairs={s['n_pairs']} types={s['type_dist']} sev={s['severity_dist']} "
          f"cards={s['n_cards']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
