#!/usr/bin/env python3
"""M5 质量度量：北极星指标口径 + 三级 DoD（原子/章/全书）。

聚合**既有事实源**，不重复实现：
    gate_engine（规则命中）· golden_state（黄金锁）· debt_ledger（负债）
    build/metrics.json（Book 存量：ASM 锚定率 / 验证标记 / 教学标记 / 自含率）
    atoms/ + evidence/（原子体系：五剖面字段完整率）

三级 DoD（M4 §6 评分聚合的判定面）：
    原子级 = 五剖面全绿（多源≥1 · 证据非空+一手 · superiority 非空非禁词 · depth.layer · 教学4字段）
    章级   = 该章原子全部原子级 DoD（原子化章逐步达成，G5 迁移）
    全书级 = 全部章级 + 冲突清零 + 黄金锁无恶化 + 负债率合规

用法：
    python tools/quality_dashboard.py            # 打印北极星指标 + DoD 对照
    python tools/quality_dashboard.py --json build/dashboard.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge               # noqa: E402

METRICS_JSON = ROOT / "build/metrics.json"
BANNED = ("讲解更详细", "更通俗易懂", "更全面", "更加深入", "帮助读者理解", "结合实际")
PED_FIELDS = ("motivation", "misconception", "socratic", "predict_first")


def _meta(p: Path) -> dict[str, Any]:
    try:
        return replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return {}


def _scan(root: Path, pattern: str) -> list[Path]:
    return sorted(root.rglob(pattern)) if root.exists() else []


def _book_metrics() -> dict[str, Any]:
    if not METRICS_JSON.exists():
        return {}
    return cast(dict[str, Any], json.loads(METRICS_JSON.read_text(encoding="utf-8")))


def dashboard() -> dict[str, Any]:
    findings = ge.run(include_advice=False)
    block = sum(1 for f in findings if f.severity == "block")
    warn = sum(1 for f in findings if f.severity == "warn")

    atoms = _scan(Path(ge.ATOMS), "ATOM-*.md")
    metas = [(_meta(p), p) for p in atoms]
    n = len(metas) or 1

    def pct(cnt: int) -> str:
        return f"{cnt}/{len(metas)} ({cnt / n:.0%})" if metas else "n/a（原子库为空）"

    five_prof = 0
    contradictions = 0
    for meta, _p in metas:
        depth = meta.get("depth") or {}
        ok = bool(_as_list_nonempty(meta.get("sources"))
                  and _as_list_nonempty(meta.get("evidence"))
                  and meta.get("first_hand") is True
                  and _nonempty_no_ban(meta.get("superiority"))
                  and isinstance(depth, dict) and depth.get("layer"))
        ped = meta.get("pedagogy") or {}
        ok = ok and isinstance(ped, dict) and all(ped.get(f) for f in PED_FIELDS)
        five_prof += bool(ok)
        raw_rels = meta.get("relations")
        rels: list[Any] = raw_rels if isinstance(raw_rels, list) else []
        for rel in rels:
            if isinstance(rel, dict) and rel.get("type") == "contradicts":
                contradictions += 1

    bm = _book_metrics()
    bm_content = bm.get("content", {})
    verify = bm_content.get("verification", {})
    asm = bm.get("asm", {})
    golden = cast(dict[str, Any], json.loads(
        (ROOT / "tools/golden_state.json").read_text(encoding="utf-8"))) \
        if (ROOT / "tools/golden_state.json").exists() else {}
    debt = cast(dict[str, Any], json.loads(
        (ROOT / "tools/debt_ledger.json").read_text(encoding="utf-8"))) \
        if (ROOT / "tools/debt_ledger.json").exists() else {"tickets": []}

    return {
        "north_star": {
            "证据完备度(原子)": pct(sum(1 for m, _ in metas if _as_list_nonempty(m.get("evidence")))),
            "一手实证覆盖(原子)": pct(sum(1 for m, _ in metas if m.get("first_hand") is True)),
            "原创占比(原子,非禁词)": pct(sum(1 for m, _ in metas
                                          if _nonempty_no_ban(m.get("superiority")))),
            "教学达标(原子,4字段)": pct(sum(1 for m, _ in metas
                                          if isinstance(m.get("pedagogy"), dict)
                                          and all((m["pedagogy"] or {}).get(f) for f in PED_FIELDS))),
            "纵深锚定率(Book ASM)": f"{asm.get('accurate', 0)}/{asm.get('total', 0)}"
                                    f" = {asm.get('anchor_rate', 0):.1%}" if asm else "n/a",
            "Book 验证标记": f"verified {verify.get('verified', '?')} / "
                             f"unverified {verify.get('unverified', '?')}",
            "冲突清零(contradicts 未仲裁)": str(contradictions),
            "活体漂移(黄金锁恶化)": str(golden.get("last_worse", 0)),
            "规则命中": f"block={block} warn={warn}",
            "债务负债率": f"{len(debt.get('tickets', []))}/{ge_len()}",
        },
        "dod": {
            "原子级(五剖面全绿)": pct(five_prof),
            "章级(原子化章全绿)": "0/147（G5 迁移未开始）" if not metas else "随迁移计数",
            "全书级": "未达成（依赖章级）" if five_prof < len(metas) or not metas else "待冲突清零+黄金锁复核",
        },
    }


def ge_len() -> int:
    return 23          # quality 门禁项数（与 cppbible/cmd_check 一致，meta-manifest 已锁）


def _as_list_nonempty(v: Any) -> bool:
    if v is None or v == "" or v == []:
        return False
    return bool(v if isinstance(v, list) else [v])


def _nonempty_no_ban(v: Any) -> bool:
    s = str(v or "").strip()
    return bool(s) and not any(w in s for w in BANNED)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="M5 质量度量仪表盘")
    ap.add_argument("--json", dest="json_path")
    a = ap.parse_args(argv)
    data = dashboard()
    print("[dashboard] 北极星指标（口径见 docs/kernel/M5_metrics.md）")
    for k, v in data["north_star"].items():
        print(f"  {k:28} {v}")
    print("[dashboard] 三级 DoD")
    for k, v in data["dod"].items():
        print(f"  {k:28} {v}")
    if a.json_path:
        Path(a.json_path).write_text(json.dumps(data, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
        print(f"[dashboard] → {a.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
