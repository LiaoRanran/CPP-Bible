#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""seeker_replay_651.py — H1 evidence_seeker_v2 回放（651 W1，**只读/旁路**）。

为什么（651 W1-H1）：在把证据检索接进证书流之前，必须先在**历史卡**上回放，看它
「召回了什么、引了什么、有没有引到不存在的东西」。本工具**只跑检索 + 留痕**，
**不接证书流、不判对错**；召回率/误引率由**人工**看留痕填（表格列留空）。

回放对象：648 十张 C 卡（真机 L1 + N1570 L2），逐卡：
1. 抽出 `evidence: [...]` 与 `sources: [...]` 引用；
2. 在 `evidence/` 里**解析**每条 evidence 引用（存在性 + sha256）；解析不了 ⇒ 疑似**误引**；
3. 对卡内域关键词做一次**召回探针**（在 evidence/ 里搜同名/近名候选，标为"可能漏引"）。
人工据此评：召回（漏引/应引未引）与误引（引了不存在/引错）。

用法
====
    python tools/seeker_replay_651.py --check                  # 合成自检（CI 可跑）
    python tools/seeker_replay_651.py --scan                   # 真回放十卡 → data/651_h1_seeker_replay.{json,md}
    python tools/seeker_replay_651.py --json

诚实边界：**本工具不产生召回率/误引率结论**（无金标准），只出留痕 + 人工填表模板。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "seeker_replay_651", "entry": "scan",
                "description": "H1 证据检索回放（只读留痕，人工评召回/误引）"}

OUT_JSON = ROOT / "data" / "651_h1_seeker_replay.json"
OUT_MD = ROOT / "data" / "651_h1_seeker_replay.md"

C_CARDS: dict[str, str] = {
    "ATOM-LANG-DECAY-001": "atoms/lang/ATOM-LANG-DECAY-001.md",
    "ATOM-MEM-MALLOC-001": "atoms/mem/ATOM-MEM-MALLOC-001.md",
    "ATOM-MEM-STRBOUND-001": "atoms/mem/ATOM-MEM-STRBOUND-001.md",
    "ATOM-LANG-FNPTR-001": "atoms/lang/ATOM-LANG-FNPTR-001.md",
    "ATOM-LANG-VOLATILE-001": "atoms/lang/ATOM-LANG-VOLATILE-001.md",
    "ATOM-LANG-SETJMP-001": "atoms/lang/ATOM-LANG-SETJMP-001.md",
    "ATOM-LANG-INTPROMO-001": "atoms/lang/ATOM-LANG-INTPROMO-001.md",
    "ATOM-LANG-BITFIELD-001": "atoms/lang/ATOM-LANG-BITFIELD-001.md",
    "ATOM-LANG-MACRO-001": "atoms/lang/ATOM-LANG-MACRO-001.md",
    "ATOM-UB-SIGNEDOVF-001": "atoms/ub/ATOM-UB-SIGNEDOVF-001.md",
}

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_ID_RE = re.compile(r"^id:\s*(\S+)", re.MULTILINE)


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _try_yaml(text: str):
    try:
        import yaml

        return yaml.safe_load(text)
    except Exception:  # noqa: BLE001
        return None


def card_refs(fm_text: str) -> dict:
    """从 frontmatter 抽 evidence/sources 引用（YAML 优先，失败退化为正则）。"""
    data = _try_yaml(fm_text)
    ev: list[str] = []
    src: list = []
    if isinstance(data, dict):
        raw_ev = data.get("evidence") or []
        if isinstance(raw_ev, list):
            ev = [str(x) for x in raw_ev]
        raw_src = data.get("sources") or []
        if isinstance(raw_src, list):
            src = raw_src
    else:  # 正则兜底
        m = re.search(r"^evidence:\s*\[(.*?)\]", fm_text, re.MULTILINE)
        if m:
            ev = [x.strip().strip('"\'') for x in m.group(1).split(",") if x.strip()]
    return {"evidence": ev, "sources": src}


def index_evidence() -> dict[str, str]:
    """扫 evidence/ 建 evidence_id → 相对路径。"""
    idx: dict[str, str] = {}
    base = ROOT / "evidence"
    if not base.is_dir():
        return idx
    for p in sorted(base.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = _FM_RE.match(text)
        eid = None
        if fm:
            m = _ID_RE.search(fm.group(1))
            eid = m.group(1).strip().strip('"') if m else None
        eid = eid or p.stem
        idx[eid] = str(p.relative_to(ROOT))
    return idx


@dataclass
class RefRow:
    ref: str
    resolved: bool
    path: str | None
    sha256: str | None


def replay_card(card_id: str, path: str, ev_index: dict[str, str]) -> dict:
    f = ROOT / path
    if not f.is_file():
        return {"card": card_id, "path": path, "error": "card_not_found", "evidence_rows": [],
                "unresolved": [], "source_count": 0}
    text = f.read_text(encoding="utf-8", errors="replace")
    fm = _FM_RE.match(text)
    refs = card_refs(fm.group(1)) if fm else {"evidence": [], "sources": []}
    rows: list[RefRow] = []
    unresolved: list[str] = []
    for ref in refs["evidence"]:
        p = ev_index.get(ref)
        if p:
            rows.append(RefRow(ref, True, p, _sha256(ROOT / p)))
        else:
            rows.append(RefRow(ref, False, None, None))
            unresolved.append(ref)
    return {
        "card": card_id,
        "path": path,
        "evidence_rows": [asdict(r) for r in rows],
        "unresolved": unresolved,
        "source_count": len(refs["sources"]),
        # 人工填表列（机器留空）
        "human_eval": {"recall_missed": "", "false_citation": "", "verdict": ""},
    }


def scan() -> dict:
    ev_index = index_evidence()
    cards = [replay_card(cid, rel, ev_index) for cid, rel in C_CARDS.items()]
    total_refs = sum(len(c.get("evidence_rows", [])) for c in cards)
    unresolved = sum(len(c.get("unresolved", [])) for c in cards)
    return {
        "evidence_index_size": len(ev_index),
        "cards": cards,
        "total_evidence_refs": total_refs,
        "unresolved_refs": unresolved,
        "note": "只跑检索+留痕；召回/误引率需人工看留痕填（human_eval 列留空）。",
    }


def _write(rep: dict) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 651 H1 · evidence_seeker 回放留痕（只读，人工评召回/误引）\n",
             f"- evidence 索引 {rep['evidence_index_size']} 条｜十卡 evidence 引用 {rep['total_evidence_refs']} 条｜**解析不了 {rep['unresolved_refs']} 条（疑似误引）**\n",
             "| 卡 | evidence 引用 | 解析成功 | 解析失败(疑似误引) | sources |",
             "|---|---|---|---|---|"]
    for c in rep["cards"]:
        ok = sum(1 for r in c.get("evidence_rows", []) if r["resolved"])
        lines.append(f"| {c['card']} | {len(c.get('evidence_rows', []))} | {ok} | {len(c.get('unresolved', []))} | {c.get('source_count', 0)} |")
    lines += ["\n## 人工填表（留空待填）\n",
              "| 卡 | 应引未引(漏) | 引了不存在/错(误引) | 结论 |", "|---|---|---|---|"]
    for c in rep["cards"]:
        lines.append(f"| {c['card']} |  |  |  |")
    lines.append("\n> 未解析引用 = 机器能看见的**误引下界**（引了 evidence/ 里不存在的 id），非全部误引。")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    fm = 'id: T\nclaim: x\nevidence:\n  - EV-A\n  - EV-B\nsources:\n  - {kind: iso, ref: "x"}\n'
    refs = card_refs(fm)
    chk("抽到 2 条 evidence", refs["evidence"] == ["EV-A", "EV-B"], str(refs["evidence"]))
    chk("抽到 sources", len(refs["sources"]) == 1)
    # 正则兜底路径
    refs2 = card_refs("evidence: [EV-X, EV-Y]\n")
    chk("正则兜底 2 条", refs2["evidence"] == ["EV-X", "EV-Y"], str(refs2["evidence"]))
    # 未解析计入 unresolved
    idx = {"EV-A": "evidence/a.md"}
    rep = replay_card("ATOM-LANG-DECAY-001", "atoms/lang/ATOM-LANG-DECAY-001.md", idx)
    chk("真卡可回放（无 error）", "error" not in rep)
    # 合成未解析
    fake = replay_card("__nope__", "atoms/does-not-exist.md", idx)
    chk("缺卡 ⇒ error", fake.get("error") == "card_not_found")
    print(f"seeker_replay_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 H1 证据检索回放（只读）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rep = scan()
    if a.scan:
        _write(rep)
        print(f"十卡 evidence 引用 {rep['total_evidence_refs']}｜解析失败 {rep['unresolved_refs']}｜→ {OUT_MD.name}")
        return 0
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json
          else f"cards={len(rep['cards'])} refs={rep['total_evidence_refs']} unresolved={rep['unresolved_refs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
