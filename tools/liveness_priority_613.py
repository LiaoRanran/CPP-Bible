#!/usr/bin/env python3
"""613 任务A1 · 活性锚候选生成与优先级排序（只读，不改受控目录）。

复用 612 B1 的候选（data/liveness_candidates_612.jsonl，50 命题 / 96 候选 / A9·B26·C15），
叠加 KC 台账（data/kc_inventory_612.json）的命题重要性，按
「命题重要性 × 证据卡可用性 × 补全成本」排序，输出优先级清单。

评分口径（写死在文档里，便于复核）：
  重要性 importance = difficulty + min(n_related_mis,5)*0.4 + len(successors)*0.3
      —— 难卡、关联 MIS 多、下游依赖多的命题优先补。
  可用性 availability = class_w(A3/B2/C1) + conf_w(high2/medium1) + min(n_cand,3)*0.2
      —— 候选锚唯一且可观测、置信度高 ⇒ 可用性高。
  成本 cost（越低越先做）：
      low    = class A，或 class B 且 confidence=high（锚可直接引用）
      medium = class B 且 confidence=medium
      high   = class C（无候选 / 需人工判定）
      cost_w = low 3 / medium 2 / high 1
  priority = importance * availability * cost_w（降序 = 先做）

CLI：
  python tools/liveness_priority_613.py            # 生成 data/liveness_priority_613.md
  python tools/liveness_priority_613.py --stats    # 只打印统计
  python tools/liveness_priority_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "data" / "liveness_candidates_612.jsonl"
KC = ROOT / "data" / "kc_inventory_612.json"
OUT = ROOT / "data" / "liveness_priority_613.md"

CLASS_W = {"A": 3.0, "B": 2.0, "C": 1.0}
CONF_W = {"high": 2.0, "medium": 1.0, "low": 0.5}
COST_W = {"low": 3.0, "medium": 2.0, "high": 1.0}


def load_candidates() -> list[dict]:
    if not CAND.is_file():
        return []
    rows = []
    for ln in CAND.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            rows.append(json.loads(ln))
    return rows


def load_all_props() -> list[dict]:
    """枚举**全部**缺锚 observation 命题（612 已知坑③：C 类命题在候选 jsonl 无行，
    故不能只按 jsonl 的 proposition_id 去重，必须从审计真源 load_missing_props() 枚举）。"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import liveness_candidate_generator as lcg  # noqa: E402
    return lcg.load_missing_props()


def load_kc() -> dict[str, dict]:
    if not KC.is_file():
        return {}
    d = json.loads(KC.read_text(encoding="utf-8"))
    return {k["id"]: k for k in d.get("kcs", [])}


def cost_of(cls: str, conf: str) -> str:
    c = (cls or "").upper()
    cf = (conf or "").lower()
    if c == "A" or (c == "B" and cf == "high"):
        return "low"
    if c == "B":
        return "medium"
    return "high"


def build() -> list[dict]:
    cands = load_candidates()
    kcs = load_kc()
    by_prop: dict[str, list[dict]] = {}
    for c in cands:
        by_prop.setdefault(c["proposition_id"], []).append(c)

    rows = []
    for prop in load_all_props():
        pid = prop["proposition_id"]
        card = prop["card"]
        cs = by_prop.get(pid, [])
        kc = kcs.get(card, {})
        difficulty = float(kc.get("difficulty", 1) or 1)
        n_mis = float(kc.get("n_related_mis", 0) or 0)
        succ = float(len(kc.get("successors", []) or []))

        importance = difficulty + min(n_mis, 5) * 0.4 + succ * 0.3

        # 最佳候选：class 高优先，其次 confidence 高
        if cs:
            best = sorted(cs, key=lambda c: (CLASS_W.get((c.get("class") or "C").upper(), 1.0),
                                             CONF_W.get((c.get("confidence") or "low").lower(), 0.5)),
                          reverse=True)[0]
            cls = (best.get("class") or "C").upper()
            conf = (best.get("confidence") or "low").lower()
            symbol = best.get("symbol", "")
            kind = best.get("kind", "")
            src = best.get("source_file", "")
        else:
            # 无候选行 ⇒ C 档（612 已知坑③）：无可用锚，成本最高
            cls, conf, symbol, kind, src = "C", "low", "", "", ""
        availability = (CLASS_W.get(cls, 1.0) + CONF_W.get(conf, 0.5)
                        + min(len(cs), 3) * 0.2)
        cost = cost_of(cls, conf)
        score = importance * availability * COST_W[cost]

        rows.append({
            "proposition_id": pid, "card": card,
            "domain": kc.get("domain", ""), "difficulty": int(difficulty),
            "n_related_mis": int(n_mis), "n_successors": int(succ),
            "class": cls, "confidence": conf, "n_candidates": len(cs),
            "best_symbol": symbol, "best_kind": kind, "source_file": src,
            "importance": round(importance, 2),
            "availability": round(availability, 2),
            "cost": cost, "priority": round(score, 3),
        })
    rows.sort(key=lambda r: (-r["priority"], r["proposition_id"]))
    return rows


def render(rows: list[dict]) -> str:
    by_cost = {c: [r for r in rows if r["cost"] == c] for c in ("low", "medium", "high")}
    L = ["# 613 · 活性锚补全优先级清单（A1）", "",
         f"> 生成：`python tools/liveness_priority_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 依据：612 B1 候选 `data/liveness_candidates_612.jsonl` + KC 台账 `data/kc_inventory_612.json`。",
         "> 评分 = 命题重要性 × 证据可用性 × 补全成本权重（见 tools/liveness_priority_613.py 文档串）。",
         "> **只读**：本工具不写入受控目录；实际写卡需人授权（见 A2）。", "",
         "## 汇总", "",
         "| 成本档 | 命题数 | 说明 |", "|---|---|---|",
         f"| low | {len(by_cost['low'])} | class A / B+high ⇒ 锚可直接引用，优先批量补 |",
         f"| medium | {len(by_cost['medium'])} | class B+medium ⇒ 可补但需复核 |",
         f"| high | {len(by_cost['high'])} | class C（无候选/需人工）⇒ 留作人审 |",
         f"| **合计** | **{len(rows)}** | observation 命题总数 |", "",
         "## 优先级清单（降序）", "",
         "| # | 命题 | 卡 | 域 | 难度 | 档 | 置信 | 候选数 | 最佳锚符号 | 来源 | 优先级 |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        L.append(f"| {i} | `{r['proposition_id']}` | {r['card']} | {r['domain']} | {r['difficulty']} "
                 f"| {r['class']} | {r['confidence']} | {r['n_candidates']} | `{r['best_symbol']}` "
                 f"| {r['source_file']} | {r['priority']} |")
    L += ["", "## 低成本可批量补全集合（A2 输入）", ""]
    if by_cost["low"]:
        L.append("| 命题 | 卡 | 锚类型 | 锚符号 | 来源 |")
        L.append("|---|---|---|---|---|")
        for r in by_cost["low"]:
            L.append(f"| `{r['proposition_id']}` | {r['card']} | {r['best_kind']} "
                     f"| `{r['best_symbol']}` | {r['source_file']} |")
    else:
        L.append("- （无 low 档命题）")
    L += ["", "> 注：C 档命题在候选工件中无行（612 已知坑），其 class 由生成器回填；"
               "此处按「无可用锚」计入 high 成本。"]
    return "\n".join(L) + "\n"


def check(rows: list[dict]) -> list[str]:
    errs = []
    if len(rows) != 50:
        errs.append(f"命题数应为 50，实测 {len(rows)}")
    for r in rows:
        if r["class"] not in CLASS_W:
            errs.append(f"{r['proposition_id']} class 非法: {r['class']}")
        if r["cost"] not in COST_W:
            errs.append(f"{r['proposition_id']} cost 非法: {r['cost']}")
        if not r["proposition_id"]:
            errs.append("存在空命题 id")
    # 确定性：重算一遍应完全一致
    if rows != build():
        errs.append("重算不一致（非确定性）")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 A1 · 活性锚优先级排序")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    rows = build()
    if a.check:
        errs = check(rows)
        for e in errs:
            print(f"[A1] ✗ {e}")
        print("[A1] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    if a.stats:
        for c in ("low", "medium", "high"):
            print(f"[A1] cost={c}: {len([r for r in rows if r['cost'] == c])}")
        print(f"[A1] 合计 {len(rows)}")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows), encoding="utf-8")
    print(f"[A1] 写入 {OUT.relative_to(ROOT).as_posix()}（{len(rows)} 命题）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
