"""611 D3 · oracle 验证计划（**只读** · 不跑任何 --check）。

问题：583/610 实测 `verified_by_oracle` **83 张卡 0 张填**（56 证据卡 + 27 原子卡）。
机器无从细分归属 ⇒ 保守按"全体强制重验"（fail-closed）。本工具**不跑** gate/replay/poison/mutation，
只把 83 张卡逐张映射到一个**建议验证 oracle**（按卡类型/主题启发式）并标出"已验/未验"，
产出一份"验证计划清单"，供人/编排层逐张执行。

口径：
  * 复用 `oracle_rotation._load_cards`（与 `metrics_collector.oracle_report()` 同源输入）；
  * 建议 oracle 仅作**启发式提示**（如 EV 卡主用 replay、ATOM 卡主用 gate），不裁决；
  * 诚实标注：0 张填 `verified_by_oracle` ⇒ 当前**全部**需重验，非"版本齐备"。

CLI：`--stats`（JSON）/ `--write`（写 `data/oracle_verification_plan_611.jsonl` + `.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
PLAN_OUT = ROOT / "data" / "oracle_verification_plan_611.jsonl"
REPORT_OUT = ROOT / "data" / "oracle_verification_plan_611.md"

# 611 D3 锁定分母（与 611 基线 §7 一致：83 = 56 证据卡 + 27 原子卡；已验 0 张）
KNOWN = {"cards_total": 83, "evidence": 56, "atoms": 27, "verified": 0}

# 主题 → 建议主 oracle（启发式；仅提示）。EV 卡主用 replay，ATOM 卡主用 gate。
_TOPIC_ORACLE = {
    "LANG": "gcc_compile", "MEM": "valgrind_memcheck", "UB": "ubsan",
    "CONC": "tsan", "FENCE": "tsan", "LOCK": "tsan",
}


def _suggest(card_id: str, kind: str) -> dict:
    topic = card_id.split("-")[1] if "-" in card_id else ""
    primary = _TOPIC_ORACLE.get(topic, "replay" if kind == "evidence" else "gate")
    return {"primary_oracle": primary,
            "kind": kind,
            "note": "启发式建议；按 583 fail-closed 立场，建议同时跑 gate/replay/poison/mutation 全套"}


def build_plan() -> dict:
    import oracle_rotation as orot  # noqa: E402
    cards = orot._load_cards()
    rows: list[dict] = []
    for c in cards:
        cid = c["id"]
        kind = "evidence" if cid.startswith("EV-") else ("atom" if cid.startswith("ATOM-") else "other")
        vo = c.get("verified_by_oracle")
        verified = bool(vo)
        sug = _suggest(cid, kind)
        rows.append({"card": cid, "path": c["path"], "kind": kind,
                     "verified_by_oracle": vo, "verified": verified,
                     "suggested_primary_oracle": sug["primary_oracle"],
                     "oracle_note": sug["note"]})
    rows.sort(key=lambda r: r["path"])
    cnt = Counter(r["kind"] for r in rows)
    verified_n = sum(1 for r in rows if r["verified"])
    return {"version": VERSION, "cards_total": len(rows), "by_kind": dict(cnt),
            "verified": verified_n, "unverified": len(rows) - verified_n,
            "rows": rows,
            "note": "只读：不跑任何 --check；0 张填 verified_by_oracle ⇒ 全部需重验（fail-closed）"}


def render_report(p: dict) -> str:
    lines = [
        "# 611 D3 · oracle 验证计划（只读 · 不跑验证）", "",
        "> 83 张卡（56 证据卡 + 27 原子卡）逐张映射到**建议**验证 oracle 并标「已验/未验」。"
        "本工具**不跑** gate/replay/poison/mutation，只列计划。", "",
        "## 一、总览", "",
        f"- 卡 **{p['cards_total']}** 张：证据卡 {p['by_kind'].get('evidence', 0)} · "
        f"原子卡 {p['by_kind'].get('atom', 0)} · 其它 {p['by_kind'].get('other', 0)}",
        f"- **已填 `verified_by_oracle`：{p['verified']} 张** ⇒ 未验 **{p['unverified']}** 张"
        "（保守 fail-closed：全体强制重验）", "",
        "## 二、按主题的建议 oracle 分布", "",
    ]
    from collections import Counter as _C  # noqa: E402
    dist = _C(r["suggested_primary_oracle"] for r in p["rows"])
    lines.append("| 建议主 oracle | 卡数 |")
    lines.append("|---|---|")
    for k, v in dist.most_common():
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## 三、逐卡计划（节选 Top 40）", "",
              "| 卡 | 类型 | 已验 | 建议主 oracle |", "|---|---|---|---|"]
    for r in p["rows"][:40]:
        lines.append(f"| `{r['card']}` | {r['kind']} | {'✅' if r['verified'] else '—'} | "
                     f"`{r['suggested_primary_oracle']}` |")
    if len(p["rows"]) > 40:
        lines.append(f"| … | | | 其余 {len(p['rows']) - 40} 张见 jsonl |")
    lines += ["", "## 四、口径与边界", "",
              "- 复用 `oracle_rotation._load_cards`（与 `metrics_collector.oracle_report()` 同源）；",
              "- 建议 oracle 为**启发式**（按卡主题/类型），非裁决；真实采用由人/编排层决定；",
              "- **绝不跑** gate/replay/poison/mutation（跑了会改基线，属另一批）；",
              "- 诚实：0 张填 `verified_by_oracle` = 缺口未补的代价，不是「版本齐备」。", ""]
    return "\n".join(lines)


def check(p: dict) -> list[str]:
    problems: list[str] = []
    if p["cards_total"] != KNOWN["cards_total"]:
        problems.append(f"卡总数应为 {KNOWN['cards_total']}（实测 {p['cards_total']}）")
    if p["by_kind"].get("evidence", 0) != KNOWN["evidence"]:
        problems.append(f"证据卡应为 {KNOWN['evidence']}（实测 {p['by_kind'].get('evidence', 0)}）")
    if p["by_kind"].get("atom", 0) != KNOWN["atoms"]:
        problems.append(f"原子卡应为 {KNOWN['atoms']}（实测 {p['by_kind'].get('atom', 0)}）")
    if p["verified"] != KNOWN["verified"]:
        problems.append(f"已验卡应为 {KNOWN['verified']}（实测 {p['verified']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oracle_verification_plan",
                                 description="611 D3 oracle 验证计划（只读）")
    ap.add_argument("--version", action="version", version=f"oracle_verification_plan {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {PLAN_OUT.name} + {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    plan = build_plan()
    if a.stats:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(plan)
        if problems:
            for p in problems:
                print(f"[D3] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[D3] ✓ oracle 验证计划锁定（{plan['cards_total']} 卡 · 已验 {plan['verified']} · "
              f"证据 {plan['by_kind'].get('evidence', 0)} / 原子 {plan['by_kind'].get('atom', 0)}）")
        return 0
    if a.write:
        PLAN_OUT.parent.mkdir(parents=True, exist_ok=True)
        PLAN_OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in plan["rows"]) + "\n",
                            encoding="utf-8", newline="\n")
        REPORT_OUT.write_text(render_report(plan), encoding="utf-8", newline="\n")
        print(f"[D3] 已写 {PLAN_OUT.relative_to(ROOT).as_posix()}（{plan['cards_total']} 张）"
              f" + {REPORT_OUT.relative_to(ROOT).as_posix()}")
        return 0
    print(f"卡 {plan['cards_total']} · 已验 {plan['verified']} · 未验 {plan['unverified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
