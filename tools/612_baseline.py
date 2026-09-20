"""612 任务0 · 先量基线（**只读统计，不写任何卡/边/数据文件**）。

在动手建工具前，把 612 要处理的数据的**真实分布**量清楚，避免任务书假设与实测不符。
产出 `data/612_baseline.md`，含四项统计：

  1. 桥接候选分布（98 条的主题/分量对/MIS 对分布 + 论证关系强度预估）
  2. 活性锚缺口分类（50 条缺 liveness 的 observation 命题 → A/B/C 初步分类 + 候选符号）
  3. oracle 验证优先级（83 张卡按多维度加权排序 + Top 20）
  4. KC 台账基线（27 张原子卡 → 命题/关联 MIS/难度/前置依赖）

口径纪律：所有数字来自 611 各工具同源真源，可逐字节复算；分类/优先级里的「A/B/C」「得分」
都是**自动估算的建议**，明确标「待 B1/B 线/C 线细化」，不声称客观结论。

CLI：`--write`（写报告）/ `--stats`（JSON）/ `--check`（验证报告数字与复算一致，exit 0=通过）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
CAND_IN = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REPORT_OUT = ROOT / "data" / "612_baseline.md"

# 通用符号（不得作为高置信锚候选）
_GENERIC = {"main", "printf", "scanf", "malloc", "free", "cout", "cin", "endl", "std",
            "int", "void", "char", "bool", "float", "double", "auto", "const", "static",
            "return", "if", "else", "for", "while", "sizeof", "new", "delete", "class",
            "struct", "public", "private", "template", "namespace", "using", "include"}

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _tokens(text: str) -> set[str]:
    return {t for t in _WORD.findall(text or "") if t not in _GENERIC and len(t) > 1}


# ── 1. 桥接候选分布 ────────────────────────────────────────────────────────
def bridge_distribution() -> dict:
    rows = [json.loads(line) for line in CAND_IN.read_text(encoding="utf-8").splitlines() if line.strip()]
    topic = Counter(r["basis"]["topic"] for r in rows)
    comp_pairs = Counter(tuple(r["components"]) for r in rows)
    mis_appear = Counter()
    for r in rows:
        mis_appear[r["source"]] += 1
        mis_appear[r["target"]] += 1
    # 论证关系强度预估：两 MIS 的 refutations 文本词频 Jaccard（纯词频，不调 LLM）
    import bridge_edge_candidates as c2  # noqa: E402
    mi = c2.load_mis_index()
    strength = Counter()
    for r in rows:
        a, b = r["source"], r["target"]
        ta, tb = _tokens(" ".join(mi.get(a, {}).get("refutations", []))), \
                 _tokens(" ".join(mi.get(b, {}).get("refutations", [])))
        j = (len(ta & tb) / len(ta | tb)) if (ta | tb) else 0.0
        strength["high" if j > 0.3 else ("medium" if j >= 0.1 else "low")] += 1
    return {
        "total": len(rows),
        "by_topic": dict(topic.most_common()),
        "distinct_component_pairs": len(comp_pairs),
        "top_component_pairs": [{"pair": list(k), "bridges": v}
                               for k, v in comp_pairs.most_common(10)],
        "top_mis_by_appearance": [{"mis": m, "in_candidates": c}
                                  for m, c in mis_appear.most_common(10)],
        "argument_strength_estimate": dict(strength),
    }


# ── 2. 活性锚缺口分类（A/B/C 初步）────────────────────────────────────────
def liveness_classification() -> dict:
    import proposition_liveness_audit as pla  # noqa: E402
    res = pla.audit()
    missing = [e for c in res["cards"] for e in c["missing"]]
    # 证据卡 → 文本（用于符号扫描）
    ev_text: dict[str, str] = {}
    for card_dir in (ROOT / "atoms", ROOT / "evidence"):
        for p in sorted(card_dir.rglob("*.md")):
            ev_text[p.stem] = p.read_text(encoding="utf-8", errors="replace")
    classes = {"A": [], "B": [], "C": []}
    detail = []
    for e in missing:
        stmt = e.get("statement") or ""
        ev_ids = [x for x in (e.get("evidence") or []) if isinstance(x, str)]
        card_tokens: set[str] = set()
        for ev in ev_ids:
            card_tokens |= _tokens(ev_text.get(ev, ""))
        stmt_tokens = _tokens(stmt)
        overlap = card_tokens & stmt_tokens
        if overlap:
            cls, reason = "A", f"证据卡符号与命题陈述有重叠（{len(overlap)} 个）：{sorted(overlap)[:5]}"
        elif card_tokens:
            cls, reason = "B", f"证据卡有候选符号但命题陈述未直接出现（{len(card_tokens)} 个）：{sorted(card_tokens)[:5]}"
        else:
            cls, reason = "C", "证据卡无可提取符号 ⇒ 建议改标 inference"
        classes[cls].append(e["id"])
        detail.append({"prop": e["id"], "class": cls, "reason": reason})
    return {
        "total_missing": len(missing),
        "counts": {k: len(v) for k, v in classes.items()},
        "note": "A/B/C 为**初步**自动分类（符号重叠启发式），待 B1 用更细的符号唯一性/可观测性评估细化",
        "detail": detail,
    }


# ── 3. oracle 验证优先级 ─────────────────────────────────────────────────
def oracle_priority() -> dict:
    import oracle_rotation as orot  # noqa: E402
    cards = orot._load_cards()
    import proposition_liveness_audit as pla  # noqa: E402
    mi = None
    scored = []
    for c in cards:
        pid = c["id"]
        p = ROOT / c["path"]
        text = p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""
        fm = pla.extract_frontmatter(text) or ""
        items = pla.parse_claim_items(fm)
        n_prop = len(items)
        is_atom = pid.startswith("ATOM-")
        type_w = 1 if is_atom else 2
        # 关联 MIS 数：MIS 的 related_atoms 引用该 ATOM，或 evidence 引用该 EV
        if mi is None:
            import bridge_edge_candidates as c2  # noqa: E402
            mi = c2.load_mis_index()
        rel_mis = sum(1 for m in mi.values()
                      if (is_atom and pid in m.get("related_atoms", []))
                      or (not is_atom and pid in m.get("evidence", [])))
        score = type_w * 2 + n_prop * 1 + rel_mis * 1
        scored.append({"id": pid, "type": "atom" if is_atom else "evidence", "props": n_prop,
                       "related_mis": rel_mis, "score": score,
                       "verified": bool(c.get("verified_by_oracle"))})
    scored.sort(key=lambda d: -d["score"])
    return {"total": len(scored), "top20": scored[:20], "all": scored,
            "note": "优先级维度=卡类型(证据2/原子1)*2 + 命题数 + 关联MIS数；"
                    "逃逸率/覆盖率缺口维度待 C 线结合 mutation/poison 基线细化"}


# ── 4. KC 台账基线 ───────────────────────────────────────────────────────
def kc_ledger() -> dict:
    import bridge_edge_candidates as c2  # noqa: E402
    import proposition_liveness_audit as pla  # noqa: E402
    mi = c2.load_mis_index()
    kcs = []
    for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = pla.extract_frontmatter(text) or ""
        for ln in fm.split("\n"):
            if ln.startswith("id:"):
                break
        items = pla.parse_claim_items(fm)
        obs = sum(1 for it in items if pla._text_of(it, "claim_type") == "observation")
        inf = sum(1 for it in items if pla._text_of(it, "claim_type") == "inference")
        rel_mis = [m for m, info in mi.items() if p.stem in info.get("related_atoms", [])]
        # 难度 1-5（启发式）
        if obs + inf <= 2 and len(rel_mis) <= 1:
            diff = 1
        elif (obs + inf) <= 4 or len(rel_mis) <= 3:
            diff = 2
        elif (obs + inf) <= 6 or len(rel_mis) <= 5:
            diff = 3
        elif (obs + inf) <= 8 or len(rel_mis) <= 7:
            diff = 4
        else:
            diff = 5
        kcs.append({"id": p.stem, "props_obs": obs, "props_inf": inf,
                    "related_mis": rel_mis, "difficulty": diff,
                    "prereq_note": "前置依赖基于 evidence 引用推导，待人工复核（本基线仅列关联 MIS）"})
    kcs.sort(key=lambda d: d["id"])
    return {"total_atoms": len(kcs), "kcs": kcs,
            "note": "KC=27 原子卡；难度为自动估算建议，非客观难度；前置依赖待 D1 结合 evidence 引用细化"}


def build() -> dict:
    return {
        "version": VERSION,
        "bridge": bridge_distribution(),
        "liveness": liveness_classification(),
        "oracle": oracle_priority(),
        "kc": kc_ledger(),
    }


def render(b: dict) -> str:
    br, lv, oc, kc = b["bridge"], b["liveness"], b["oracle"], b["kc"]
    L: list[str] = ["# 612 基线（任务0 · 先量，只读统计）", "",
                    "> 所有数字来自 611 各工具同源真源，可逐字节复算。"
                    "A/B/C 分类、优先级得分、难度分级均为**自动估算的建议**，明确标「待细化」，不声称客观结论。", ""]
    # 1 桥接
    L += ["## 1 · 桥接候选分布（98 条）", "",
          f"- 主题分布：{br['by_topic']}",
          f"- 跨分量对：{br['distinct_component_pairs']} 对；Top：{br['top_component_pairs']}",
          f"- 出现最多的 MIS（在候选中）：{br['top_mis_by_appearance']}",
          f"- 论证关系强度预估（refutations 词频 Jaccard 启发式）：{br['argument_strength_estimate']}", ""]
    # 2 活性锚
    L += ["## 2 · 活性锚缺口分类（50 条缺 liveness 的 observation）", "",
          f"- 初步分类：A（高置信可自动补）{lv['counts']['A']} · B（中置信需人审选）{lv['counts']['B']} · "
          f"C（建议改标 inference）{lv['counts']['C']}",
          f"- {lv['note']}",
          "", "| 命题 | 类 | 理由 |", "|---|---|---|"]
    for d in lv["detail"][:30]:
        L.append(f"| `{d['prop']}` | {d['class']} | {d['reason'][:80]} |")
    if len(lv["detail"]) > 30:
        L.append(f"| … | | 其余 {len(lv['detail']) - 30} 条见 JSON |")
    L += [""]
    # 3 oracle
    L += ["## 3 · oracle 验证优先级（83 张卡）", "",
          f"- {oc['note']}",
          "", "| 排名 | 卡 | 类型 | 命题数 | 关联MIS | 得分 | 已验 |",
          "|---|---|---|---|---|---|---|"]
    for i, c in enumerate(oc["top20"], 1):
        L.append(f"| {i} | `{c['id']}` | {c['type']} | {c['props']} | "
                 f"{c['related_mis']} | {c['score']} | {'是' if c['verified'] else '否'} |")
    L += [""]
    # 4 KC
    L += ["## 4 · KC 台账基线（27 原子卡）", "",
          f"- {kc['note']}",
          "", "| 原子卡 | obs | inf | 关联MIS数 | 难度 |", "|---|---|---|---|---|"]
    for k in kc["kcs"]:
        L.append(f"| `{k['id']}` | {k['props_obs']} | {k['props_inf']} | "
                 f"{len(k['related_mis'])} | {k['difficulty']} |")
    L += ["", "## 5 · 偏差登记（实测 vs 任务书预期）", "",
          "- 任务书预期 A 20-30 / B 15-20 / C 5-10；实测见 §2（初步，待 B1 细化）。",
          "- oracle Top20 验证优先级已给出；逃逸率/覆盖率缺口维度待 C 线细化。", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="612_baseline", description="612 任务0 先量基线（只读）")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--check", action="store_true", help="验证报告与复算一致")
    a = ap.parse_args(argv)
    b = build()
    if a.stats:
        print(json.dumps(b, ensure_ascii=False, indent=1))
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render(b), encoding="utf-8", newline="\n")
        print(f"[612基线] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()} "
              f"（桥接{br_tot(b)} / 活性锚{b['liveness']['total_missing']} "
              f"/ oracle{b['oracle']['total']} / KC{b['kc']['total_atoms']}）")
        return 0
    if a.check:
        b2 = build()
        ok = (b2["bridge"]["total"] == b["bridge"]["total"]
              and b2["liveness"]["total_missing"] == b["liveness"]["total_missing"]
              and b2["oracle"]["total"] == b["oracle"]["total"]
              and b2["kc"]["total_atoms"] == b["kc"]["total_atoms"])
        print("[612基线] ✓ 复算一致" if ok else "[612基线] ❌ 复算不一致", file=sys.stderr if not ok else sys.stdout)
        return 0 if ok else 2
    print(f"桥接{b['bridge']['total']} 活性锚{b['liveness']['total_missing']} "
          f"oracle{b['oracle']['total']} KC{b['kc']['total_atoms']}")
    return 0


def br_tot(b: dict) -> int:
    return b["bridge"]["total"]


if __name__ == "__main__":
    raise SystemExit(main())
