#!/usr/bin/env python3
"""405 闪卡导出（423）：原子 claim + 误解反例 → Anki CSV / Markdown。

让生产出来的知识第一次被学习者消费：闪卡背面不是"教材式讲解"，而是
**实测读数 + 反例**（这是本库与传统学习资料的根本区别）。

用法：
  python tools/flashcard_export.py export --format both --outdir data/flashcards [--json]
  python tools/flashcard_export.py stats --json

卡型：
  A 原子 claim 卡（每颗原子 1 张）：Front=论断问题化；Back=claim 边界+证据 verdict+误解
  B 误解反例卡（每条误解 1 张）：Front=误解说法；Back=反例（refutations）+关联原子

零风险：只读 atoms/misconceptions/evidence，输出只写 data/flashcards/。
实际规模（2026-09-13）：27 颗原子 + 79 条误解 = 106 张（423 文档的 107 为估算基线）。
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v7.0"
OUT_DEFAULT = ge.ROOT / "data" / "flashcards"


def _first(x: Any) -> str:
    if isinstance(x, list):
        return str(x[0]) if x else ""
    return str(x or "")


def _lines(x: Any, n: int = 3) -> list[str]:
    if isinstance(x, list):
        return [str(v) for v in x[:n] if str(v).strip()]
    return [str(x)] if str(x or "").strip() else []


def atom_claim_card(meta: dict[str, Any], verdicts: dict[str, str]) -> dict[str, str]:
    """类型 A：原子 claim 卡。"""
    aid = str(meta.get("id") or "")
    claim = str(meta.get("claim") or "").strip()
    front = (f"【{meta.get('domain')}】{aid}\n"
             f"以下论断是否成立？依据是什么？\n{claim}")
    ev = [f"{eid}: {verdicts.get(str(eid), '?')}"
          for eid in ge._as_list(meta.get("evidence"))]
    mis = []
    ped = meta.get("pedagogy") or {}
    for m in (ped.get("misconception") if isinstance(ped, dict) else []) or []:
        if isinstance(m, dict) and m.get("text"):
            mis.append(str(m["text"]))
    mis += [str(v) for v in ge._as_list(meta.get("misconceptions"))]
    back = "\n".join(
        [f"论断：{claim}",
         f"边界：{str(meta.get('claim_boundary') or '').strip()}"]
        + (["关键证据：", *[f"  - {e}" for e in ev]] if ev else [])
        + (["常见误解：", *[f"  - {m}" for m in mis[:3]]] if mis else []))
    return {"type": "atom_claim", "id": aid, "front": front, "back": back,
            "domain": str(meta.get("domain") or "").lower(),
            "tags": f"{meta.get('domain')} atom {aid} {meta.get('status')}"}


def misconception_card(meta: dict[str, Any]) -> dict[str, str]:
    """类型 B：误解反例卡。"""
    mid = str(meta.get("id") or "")
    triggers = _lines(meta.get("trigger_patterns"), 1)
    refs = _lines(meta.get("refutations"), 3)
    related = [str(v) for v in ge._as_list(meta.get("related_atoms"))]
    front = (f"【误解】{mid} {meta.get('name')}"
             + (f"\n触发说法：{triggers[0]}" if triggers else ""))
    back = "\n".join(
        ["为什么错：" + (refs[0] if refs else "（见反例）")]
        + [f"反例 {i + 1}：{r}" for i, r in enumerate(refs[1:] if refs else [])]
        or ["为什么错：（缺反例）"]
    ) if refs else "为什么错：（缺反例）"
    if related:
        back += "\n关联原子：" + " ".join(related)
    return {"type": "misconception", "id": mid, "front": front, "back": back,
            "domain": str(meta.get("domain") or "").lower(),
            "tags": f"{meta.get('domain')} misconception {mid} {meta.get('level')}"}


def build_cards() -> list[dict[str, str]]:
    verdicts = {str(ge._meta(p).get("id") or p.stem): str(ge._meta(p).get("verdict") or "")
                for p in ge._cards(ge.EVIDENCE, "EV-*.md")}
    cards = [atom_claim_card(ge._meta(p), verdicts)
             for p in ge._cards(ge.ATOMS, "ATOM-*.md")]
    cards += [misconception_card(ge._meta(p))
              for p in ge._cards(ge.MISCONCEPTIONS, "MIS-*.md")]
    return cards


def _anki_csv(cards: list[dict[str, str]]) -> str:
    """Anki 导入格式：Front, Back, Tags, Deck（双引号包裹，内部 " 转义为 ""）。"""
    import io
    buf = io.StringIO()
    w = csv.writer(buf, quoting=csv.QUOTE_ALL, lineterminator="\n")
    w.writerow(["Front", "Back", "Tags", "Deck"])
    for c in cards:
        w.writerow([c["front"], c["back"], c["tags"],
                    f"CPP-Bible::{c['domain']}"])
    return buf.getvalue()


def _markdown(c: dict[str, str]) -> str:
    return (f"# {c['id']}（{c['type']}）\n\n## 正面\n\n{c['front']}\n\n"
            f"## 背面\n\n{c['back']}\n")


def _display(p: Path) -> str:
    try:
        return p.relative_to(ge.ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def export(outdir: Path, fmt: str = "both") -> dict[str, Any]:
    cards = build_cards()
    outdir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    if fmt in ("anki", "both"):
        (outdir / "anki.csv").write_text(_anki_csv(cards), encoding="utf-8")
        outputs.append(_display(outdir / "anki.csv"))
    if fmt in ("markdown", "both"):
        md = outdir / "markdown"
        md.mkdir(exist_ok=True)
        for c in cards:
            safe = re.sub(r"[^\w.-]", "_", c["id"])
            (md / f"{c['type']}_{safe}.md").write_text(_markdown(c), encoding="utf-8")
        outputs.append(_display(md))
    by_type: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    empty = [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()]
    for c in cards:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
        by_domain[c["domain"]] = by_domain.get(c["domain"], 0) + 1
    return {
        "tool": "flashcard_export", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "total_cards": len(cards),
        "by_type": by_type, "by_domain": by_domain,
        "empty_front_or_back": empty,
        "output_files": outputs,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="闪卡导出（405：原子+误解→Anki CSV）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export")
    ex.add_argument("--format", choices=["anki", "markdown", "both"], default="both")
    ex.add_argument("--outdir", default=str(OUT_DEFAULT.relative_to(ge.ROOT)))
    sub.add_parser("stats")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "export":
        data = export(ge.ROOT / a.outdir, a.format)
    else:  # stats
        cards = build_cards()
        data = {"tool": "flashcard_export", "version": VERSION,
                "total_cards": len(cards),
                "by_type": {t: sum(1 for c in cards if c["type"] == t)
                            for t in {c["type"] for c in cards}}}
    if a.json:
        print(json.dumps(data, ensure_ascii=False, indent=1))
    else:
        print(f"[flashcards] 共 {data['total_cards']} 张 "
              f"({data.get('by_type')}) → {data.get('output_files')}")
        if data.get("empty_front_or_back"):
            print(f"[flashcards] ⚠️ Front/Back 为空：{data['empty_front_or_back']}")
    return 1 if data.get("empty_front_or_back") else 0


if __name__ == "__main__":
    main()
