#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""teach_card_656.py — 656 D：把系统变成"学生能用的东西"的**数据侧**。

任务书的 D 是"学习 MVP：星图选卡 → 卡页面（3 段：前置/学习/自测）+ 前置依赖查询 + 学习进度本地存储"。
本工具负责其中**唯一需要真数据**的部分：把一张卡的"可教内容"从真实台账里抽出来，
产出 `web/data/card.json`（单卡）与 `web/data/cards_index.json`（选卡用索引）。

数据来源（全部现算，缺项标 null，**不编内容**）
===============================================
- 卡本体：`atoms/**/<id>.md` 的 YAML frontmatter（claim / claim_structured / claim_boundary / relations / status…）
- 四态判决：`four_state_verdict_638.classify_card`（边界优先，缺边界降级 unknown）
- 命题：`claim_structured[]`（id/subject/predicate/object/claim_type/statement/evidence/external_basis/liveness）
- 证据：命题引用的 `EV-*` 卡（verdict / hypothesis / fixture / **复现命令 command** / artifact 路径+sha256）
- 误解：`data/grounded_labels_w2.json`（W2 接地图）里**指向本卡命题**的 attack 边
- 前置：卡 frontmatter 的 `relations[].prerequisite`（**真实存在**，非本工具推测）
- 自测题：由上述真实字段**机械生成**（问题+答案+出处），不写任何"AI 生成的题目内容"

诚实边界
========
- 自测题是"字段回忆题"，不是教学法意义上的好题；它的价值是**答案必然可回溯到台账**（每题带 `source`）。
- 前置只做 **1 跳展开**（prereq 的 prereq 不再展开），避免把一张卡变成整本书。

用法
====
    python tools/teach_card_656.py --list                       # 写 cards_index.json 并打印候选卡
    python tools/teach_card_656.py --card ATOM-CONC-RACE-001     # 写 card.json（默认挑一张内容最全的卡）
    python tools/teach_card_656.py --check                       # 自检（schema + 引用完整性）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEB_DATA = ROOT / "web" / "data"
CARD_JSON = WEB_DATA / "card.json"
INDEX_JSON = WEB_DATA / "cards_index.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

import four_state_verdict_638 as fs  # noqa: E402


# ── 读卡 ────────────────────────────────────────────────────────────────────
def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    try:
        d = yaml.safe_load(text[3:end])
        return d if isinstance(d, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def all_cards() -> dict[str, Path]:
    """真实卡 id → 路径（`atoms/**/ATOM-*.md`；draft650 也算卡，但索引里标出来）。"""
    out: dict[str, Path] = {}
    for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
        out[p.stem] = p
    return out


def all_evidence() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in sorted((ROOT / "evidence").rglob("EV-*.md")):
        out[p.stem] = p
    return out


def graph_attacks() -> list[dict[str, Any]]:
    p = WEB_DATA / "graph.json"
    if not p.is_file():
        return []
    d = json.loads(p.read_text(encoding="utf-8"))
    return [ln for ln in d.get("links", []) if ln.get("kind") == "attack"]


# ── 组装 ────────────────────────────────────────────────────────────────────
def card_entry(cid: str, path: Path) -> dict[str, Any]:
    fm = _frontmatter(path)
    verdict = fs.classify_card(str(path))
    props = fm.get("claim_structured") or []
    rel = fm.get("relations") or []
    prereqs = [r.get("prerequisite") for r in rel
               if isinstance(r, dict) and r.get("prerequisite")]
    evidence = set()
    for pr in props:
        for e in (pr.get("evidence") or []):
            evidence.add(str(e))
    return {
        "id": cid,
        "title": str(fm.get("title") or "").strip(),
        "domain": fm.get("domain"),
        "type": fm.get("type"),
        "status": fm.get("status"),
        "dal": fm.get("dal"),
        "audience": fm.get("audience"),
        "cognitive_load": fm.get("cognitive_load"),
        "draft": path.parent.name == "draft650",
        "verdict_state": verdict.get("state"),
        "downgraded": bool(verdict.get("downgraded")),
        "props": len(props),
        "evidence": sorted(evidence),
        "prereqs": prereqs,
    }


def evidence_entry(eid: str, path: Path) -> dict[str, Any]:
    fm = _frontmatter(path)
    cmd = fm.get("command")
    if isinstance(cmd, list):
        cmd = "\n".join(str(x) for x in cmd)
    return {
        "id": eid,
        "path": path.relative_to(ROOT).as_posix(),
        "exists": True,
        "verdict": fm.get("verdict"),
        "type": fm.get("type"),
        "kind": fm.get("kind"),
        "dal": fm.get("dal"),
        "status": fm.get("status"),
        "hypothesis": (str(fm.get("hypothesis") or "").strip() or None),
        "fixture": fm.get("fixture"),
        "replay_command": (str(cmd).strip() if cmd else None),
        "artifact": fm.get("artifact"),
        "artifact_sha256": fm.get("artifact_sha256"),
        "serves": fm.get("serves") or [],
        "controlled_vars": fm.get("controlled_vars") or [],
    }


def build_card(cid: str, cards: dict[str, Path], evid: dict[str, Path]) -> dict[str, Any]:
    path = cards[cid]
    fm = _frontmatter(path)
    verdict = fs.classify_card(str(path))
    props = fm.get("claim_structured") or []
    rel = fm.get("relations") or []
    prereq_ids = [str(r.get("prerequisite")) for r in rel
                  if isinstance(r, dict) and r.get("prerequisite")]

    ev_ids: list[str] = []
    for pr in props:
        for e in (pr.get("evidence") or []):
            if str(e) not in ev_ids:
                ev_ids.append(str(e))
    ev_rows = []
    for e in ev_ids:
        if e in evid:
            ev_rows.append(evidence_entry(e, evid[e]))
        else:
            ev_rows.append({"id": e, "exists": False,
                            "note": "命题引用了该证据卡，但 evidence/ 下找不到 ⇒ 按缺失登记"})

    prereq_rows = []
    for pid in prereq_ids:
        if pid in cards:
            e = card_entry(pid, cards[pid])
            prereq_rows.append({k: e[k] for k in ("id", "title", "domain", "status",
                                                  "verdict_state", "props")})
        else:
            prereq_rows.append({"id": pid, "title": None, "note": "relations 声明的前置卡不存在"})

    attacks = graph_attacks()
    prop_ids = {str(pr.get("id")) for pr in props}
    misconceptions = []
    for ln in attacks:
        tgt = str(ln.get("target"))
        if tgt in prop_ids or ln.get("target") == cid:
            misconceptions.append({
                "misconception": ln.get("source"),
                "target": tgt,
                "defeated": bool(ln.get("defeated")),
            })

    domain = fm.get("domain")
    related = [c for c, p in cards.items()
               if c != cid and _frontmatter(p).get("domain") == domain
               and _frontmatter(p).get("status") == "verified"][:8]

    selfcheck = selfcheck_items(cid, fm, props, ev_rows, prereq_rows, verdict)

    return {
        "id": cid,
        "path": path.relative_to(ROOT).as_posix(),
        "meta": {
            "title": str(fm.get("title") or "").strip(),
            "domain": domain,
            "type": fm.get("type"),
            "status": fm.get("status"),
            "dal": fm.get("dal"),
            "audience": fm.get("audience"),
            "cognitive_load": fm.get("cognitive_load"),
            "prerequisites_readable": fm.get("prerequisites_readable"),
            "verified_by": fm.get("verified_by"),
            "verified_at": fm.get("verified_at"),
        },
        "claim": str(fm.get("claim") or "").strip(),
        "boundary": {
            "mutation_set_hash": fm.get("mutation_set_hash"),
            "mutation_count": fm.get("mutation_count"),
            "generator_version": fm.get("generator_version"),
            "claim_boundary": fm.get("claim_boundary") or {},
        },
        "verdict": verdict,
        "prerequisites": prereq_rows,
        "props": [{
            "id": pr.get("id"),
            "subject": pr.get("subject"),
            "predicate": pr.get("predicate"),
            "object": pr.get("object"),
            "claim_type": pr.get("claim_type"),
            "statement": str(pr.get("statement") or "").strip(),
            "evidence": pr.get("evidence") or [],
            "external_basis": pr.get("external_basis"),
            "liveness": pr.get("liveness"),
            "signed_by": pr.get("signed_by"),
        } for pr in props],
        "evidence": ev_rows,
        "misconceptions": misconceptions,
        "related_verified_same_domain": related,
        "selfcheck": selfcheck,
        "generated_from": [
            "atoms/**/<id>.md frontmatter",
            "evidence/**/EV-*.md frontmatter（含复现命令）",
            "tools/four_state_verdict_638.classify_card（四态现算）",
            "web/data/graph.json（W2 攻击边）",
        ],
        "note": ("全部字段来自真实台账；自测题由字段机械生成（每题带 source），"
                 "不是 AI 生成的题目内容。缺项一律 null 并保留原因。"),
    }


def selfcheck_items(cid: str, fm: dict[str, Any], props: list[dict[str, Any]],
                    ev_rows: list[dict[str, Any]], prereq_rows: list[dict[str, Any]],
                    verdict: dict[str, Any]) -> list[dict[str, Any]]:
    """**机械生成**自测题：答案 = 台账字段，`source` = 字段出处（可自查）。"""
    items: list[dict[str, Any]] = []
    items.append({
        "q": "这张卡的判决四态是什么？为什么是这个态？",
        "a": f"{verdict.get('state')}（boundary_ok={verdict.get('boundary_ok')}，"
             f"downgraded={verdict.get('downgraded')}）——理由：{'；'.join(verdict.get('reasons') or ['—'])}",
        "source": "tools/four_state_verdict_638.classify_card（现算）",
    })
    b = fm.get("claim_boundary") or {}
    if b:
        items.append({
            "q": "这张卡的结论在什么边界内成立？（标准 / 编译器 / 优化 / 平台）",
            "a": f"标准 {b.get('standard')}；编译器 {b.get('compilers')}；"
                 f"优化 {b.get('opt')}；平台 {b.get('platform')}",
            "source": "卡 frontmatter.claim_boundary",
        })
    if props:
        p0 = props[0]
        items.append({
            "q": f"命题 {p0.get('id')} 的断言类型（claim_type）是什么？它引用哪几张证据卡？",
            "a": f"{p0.get('claim_type')}；证据 {p0.get('evidence')}",
            "source": "卡 frontmatter.claim_structured[0]",
        })
        inf = [p for p in props if p.get("claim_type") == "inference"]
        if inf:
            items.append({
                "q": f"命题 {inf[0].get('id')} 是 inference（推断），它的外部依据是什么？",
                "a": str(inf[0].get("external_basis") or "（该命题未填 external_basis）"),
                "source": "卡 frontmatter.claim_structured[].external_basis",
            })
    cmds = [e for e in ev_rows if e.get("replay_command")]
    if cmds:
        items.append({
            "q": "这一条结论要怎么**自己跑一遍**复现？（写出命令）",
            "a": "　//　".join(str(e["replay_command"]).replace("\n", " && ") for e in cmds[:2]),
            "source": "证据卡 frontmatter.command（真实可跑命令）",
        })
    if ev_rows:
        items.append({
            "q": "这些证据卡各自的机器判决（verdict）是什么？",
            "a": "；".join(f"{e.get('id')}={e.get('verdict')}" for e in ev_rows),
            "source": "证据卡 frontmatter.verdict",
        })
    if prereq_rows:
        items.append({
            "q": "读这张卡之前，本仓声明的**前置卡**是哪一张（或哪几张）？",
            "a": "；".join(f"{p.get('id')}（{p.get('title')}）" for p in prereq_rows),
            "source": "卡 frontmatter.relations[].prerequisite（真实声明，非推测）",
        })
    else:
        items.append({
            "q": f"{cid} 在本仓**没有**声明前置卡，这意味着什么？",
            "a": "relations 里没有 prerequisite 条目 ⇒ 本仓未声明先修链（不代表不需要基础）",
            "source": "卡 frontmatter.relations（空）",
        })
    return items


# ── 入口 ────────────────────────────────────────────────────────────────────
def write_index() -> dict[str, Any]:
    cards = all_cards()
    entries = [card_entry(cid, p) for cid, p in cards.items()]
    # 排序：非 draft 优先、命题多优先、id 字典序（稳定可复现）
    entries.sort(key=lambda e: (e["draft"], -int(e["props"] or 0), e["id"]))
    payload = {
        "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": "tools/teach_card_656.py",
        "count": len(entries),
        "drafts": sum(1 for e in entries if e["draft"]),
        "cards": entries,
    }
    # `default=str`：YAML 会把 `verified_at: 2026-09-12` 解析成 `datetime.date`，
    # 不兜底会在 json.dumps 处炸（本批实测撞到）。
    INDEX_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
                          encoding="utf-8", newline="\n")
    return payload


def pick_default(payload: dict[str, Any]) -> str:
    """挑一张"内容最全"的卡：非 draft、命题 ≥3、证据 ≥2。

    注意：**不**用四态筛选——本批实测 47 张卡里 0 张带边界三元组 ⇒ 四态全部 `unknown`
    （这是台账现状，不是挑选逻辑的问题）。
    """
    for e in payload["cards"]:
        if not e["draft"] and e["props"] >= 3 and len(e["evidence"]) >= 2:
            return str(e["id"])
    return str(payload["cards"][0]["id"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 D：学习 MVP 的真数据生成器")
    ap.add_argument("--card", default=None, help="卡 id（默认自动挑一张内容最全的）")
    ap.add_argument("--all", action="store_true",
                    help="写 web/data/cards.json（全部卡的完整内容，供页面客户端切卡）")
    ap.add_argument("--list", action="store_true", help="只写 cards_index.json")
    ap.add_argument("--check", action="store_true", help="自检：schema + 引用完整性")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    cards, evid = all_cards(), all_evidence()
    idx = write_index()

    if a.all:
        payload = {c: build_card(c, cards, evid) for c in sorted(cards)}
        p = WEB_DATA / "cards.json"
        p.write_text(json.dumps({
            "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
            "tool": "tools/teach_card_656.py",
            "count": len(payload),
            "cards": payload,
        }, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8", newline="\n")
        missing = sum(1 for c in payload.values() for e in c["evidence"] if not e.get("exists"))
        print(f"[teach656] cards.json：{len(payload)} 张卡，缺证据引用 {missing} 处"
              f"（{p.stat().st_size // 1024} KB）")
        return 0

    if a.list:
        print(f"[teach656] cards_index.json：{idx['count']} 张卡（其中 draft {idx['drafts']}）")
        for e in idx["cards"][:12]:
            print(f"   {e['id']:<28} {e['verdict_state']:<20} 命题 {e['props']} 证据 {len(e['evidence'])}"
                  f" 前置 {len(e['prereqs'])}　{e['title'][:36]}")
        return 0

    cid = a.card or pick_default(idx)
    if cid not in cards:
        print(f"[teach656] 找不到卡 {cid}", file=sys.stderr)
        return 2
    card = build_card(cid, cards, evid)
    CARD_JSON.write_text(json.dumps(card, ensure_ascii=False, indent=2, default=str) + "\n",
                         encoding="utf-8", newline="\n")

    if a.check:
        ok = True
        problems = []
        for k in ("id", "meta", "claim", "boundary", "verdict", "prerequisites",
                  "props", "evidence", "selfcheck"):
            if k not in card:
                problems.append(f"缺字段 {k}")
                ok = False
        if not card["props"]:
            problems.append("该卡没有 claim_structured（自测题会退化）")
        for e in card["evidence"]:
            if not e.get("exists"):
                problems.append(f"证据卡缺失：{e.get('id')}")
        for s in card["selfcheck"]:
            if not s.get("q") or not s.get("a") or not s.get("source"):
                problems.append("自测题缺 q/a/source")
                ok = False
        print(f"  [{'ok' if not problems else 'FAIL'}] 卡 {cid}：命题 {len(card['props'])}"
              f"｜证据 {len(card['evidence'])}｜自测 {len(card['selfcheck'])}"
              f"｜误解 {len(card['misconceptions'])}｜前置 {len(card['prerequisites'])}")
        for prob in problems:
            print(f"  [FAIL] {prob}")
        print(f"teach_card_656 selftest: {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1

    if a.json:
        print(json.dumps(card, ensure_ascii=False, indent=2))
    else:
        print(f"[teach656] card.json ← {cid}：命题 {len(card['props'])}｜证据 {len(card['evidence'])}"
              f"｜自测 {len(card['selfcheck'])}｜四态 {card['verdict']['state']}"
              f"｜前置 {len(card['prerequisites'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
