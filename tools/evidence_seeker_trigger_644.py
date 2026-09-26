"""644 阶段 E · E2 自动求索触发器。

对 E1 检出的不足卡片，自动调用 D5 获取证据；获取后重新判定充分性；
记录：求索前 / 求索后的证据变化。

**只获取和保存，不修改卡片**——人审后才关联（§九.6）。由于未关联，卡片的充分性
（基于既有证据）不会因本次求索而改变；变化体现在「新获取证据包」的体量（诚实记录）。
只读/追加：不修改受控目录。`--check` 只读幂等；`--run` 触发求索（受网络/编译器限制）。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_acquisition_orchestrator_644 as d5
import evidence_base_644 as base
import evidence_gap_scanner_644 as e1
import evidence_sufficiency_644 as b2

OUT_MD = os.path.join(base.ROOT, "data", "644_seeker_report.md")


def _topic_for(card_id: str) -> str:
    for a in base.list_atoms():
        if a["id"] == card_id:
            return str(a["meta"].get("title", a["id"]))
    return card_id


def seek(gaps: list[dict[str, Any]] | None = None,
         orchestrate_fn: Callable[..., dict] = d5.orchestrate) -> dict[str, Any]:
    """对不足卡片触发 D5 求索；记录前/后变化（不修改卡片）。"""
    gaps = gaps if gaps is not None else e1.scan()["gaps"]
    rows: list[dict[str, Any]] = []
    still_insufficient = 0
    new_evidence_total = 0
    for g in gaps:
        cid = g["card"]
        before = b2.judge(cid, _card_evidence(cid))
        r = orchestrate_fn(_topic_for(cid), max_rounds=2)
        pkg = r.get("evidence_package", [])
        new_evidence_total += len(pkg)
        after = b2.judge(cid, _card_evidence(cid))  # 未关联 → 与 before 同判定（诚实）
        rows.append({"card": cid, "before_verdict": before["verdict"],
                     "after_verdict": after["verdict"], "new_evidence": len(pkg),
                     "changed": before["verdict"] != after["verdict"]})
        if after["verdict"] != "充分":
            still_insufficient += 1
    return {"n_triggered": len(rows), "still_insufficient": still_insufficient,
            "new_evidence_total": new_evidence_total, "rows": rows,
            "cards_untouched": True}


def _card_evidence(card_id: str) -> list[dict[str, Any]]:
    m = base.card_evidence_map()
    fal = {e["id"]: bool(e["meta"].get("falsification"))
           for e in base.list_existing_evidence()}
    return [dict(e, falsification=fal.get(e["id"], False)) for e in m.get(card_id, [])]


def render_md(r: dict[str, Any]) -> str:
    lines = ["# 644 E2 · 自动求索触发器报告", "",
             f"- 触发卡片：**{r['n_triggered']}**  仍不足：**{r['still_insufficient']}**",
             f"- 新获取证据总量：**{r['new_evidence_total']}**", "",
             "> 仅获取与保存，未修改任何卡片（cards_untouched=True）。",
             "> 未关联前卡片充分性不变；变化体现在新证据包体量（人审后才关联）。", "",
             "| 卡片 | 求索前 | 求索后 | 新证据 | 变化 |", "|---|---|---|---|---|"]
    for row in r["rows"]:
        lines.append(f"| {row['card']} | {row['before_verdict']} | {row['after_verdict']} | "
                     f"{row['new_evidence']} | {'是' if row['changed'] else '否'} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(seek()))
    return OUT_MD


def selftest() -> int:
    def stub_orch(topic, snippet=None, max_rounds=3):
        return {"topic": topic, "rounds": max_rounds, "max_rounds": max_rounds,
                "evidence_package": [], "sufficiency": {}, "log": [], "cards_untouched": True}

    # 改前快照一张卡
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    r = seek(orchestrate_fn=stub_orch)
    # 触发正确（对不足卡片触发；若全充分则 0 触发也合法，但结构正确）
    assert "n_triggered" in r and "still_insufficient" in r and "new_evidence_total" in r
    assert r["cards_untouched"] is True
    # 不修改卡片
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 E2 自动求索触发器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--run", action="store_true", help="触发求索（受网络/编译器限制）")
    ap.add_argument("--report", action="store_true", help="写求索报告（基于现有不足卡片）")
    a = ap.parse_args(argv)
    if a.run or a.report:
        r = seek()
        print(f"triggered={r['n_triggered']} still_insufficient={r['still_insufficient']} new={r['new_evidence_total']}")
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
