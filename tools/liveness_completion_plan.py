"""611 D2 · 命题活性锚补全计划（**只读** · 不补字段）。

问题：607 审计发现 50 条 observation 命题**全缺** `liveness`（gate `OBSERVATION-LIVENESS` 必报 warn）。
补什么 `fixture_symbol` 是**人审权力**（要判"哪个夹具符号真能证伪这条命题"）。
本工具**不补字段**，只产出一份"补全计划"：把每条缺锚的 observation 命题、它的证据（evidence）
和它**可能**对应的夹具符号建议列出来，供人逐条裁定。

口径（与 607 `proposition_liveness_audit` 同源，复用其审计）：
  * 只动 `missing` / `missing_symbol` / `unknown_kind` 的 observation 命题；
  * `fixture_symbol` 建议 = 该命题 `evidence` 字段里**第一个**可作为工件引用的 token（ATOM-*/EV-*/example-*）；
    若 evidence 为空 ⇒ 标记"待人裁定"，不硬猜。

CLI：`--stats`（JSON）/ `--write`（写 `data/liveness_completion_plan_611.md`）/ `--check`。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "liveness_completion_plan_611.md"

_KW_RX = re.compile(r"(?:ATOM|EV|example|EXAMPLE)-[A-Za-z0-9][A-Za-z0-9_-]*")

# 611 D2 锁定：缺锚 observation 命题总数（607 实测 50，论证图/卡冻结前不变）
KNOWN_MISSING = 50


def _suggest_symbol(evidence: list) -> str:
    """从 evidence 里取第一个可当工件引用的 token 作为**建议**（非裁决）。"""
    for e in (evidence or []):
        toks = _KW_RX.findall(str(e))
        if toks:
            return toks[0]
    return "待人裁定"


def build_plan(atoms_root=None) -> dict:
    import proposition_liveness_audit as pla  # noqa: E402
    res = pla.audit(Path(atoms_root) if atoms_root else None)
    rows: list[dict] = []
    total = 0
    for c in res["cards"]:
        for e in c["missing"]:
            if e["status"] == "missing_symbol":
                sug = e.get("symbol") or _suggest_symbol(e.get("evidence"))
                status_label = "`symbol` 空"
            else:
                sug = _suggest_symbol(e.get("evidence"))
                status_label = "缺 `liveness`" if e["status"] == "missing" else f"未知 kind `{e['kind']}`"
            rows.append({"card": c["card"], "prop_id": e["id"], "status": status_label,
                         "suggested_symbol": sug, "statement": e.get("statement", ""),
                         "evidence": e.get("evidence", [])})
            total += 1
    rows.sort(key=lambda r: (r["card"], r["prop_id"]))
    return {"total_missing": total, "rows": rows,
            "note": "只读：不补字段；suggested_symbol 仅为建议，是否采用由人裁定（须判真能证伪）"}


def render_report(p: dict) -> str:
    lines = [
        "# 611 D2 · 命题活性锚补全计划（只读 · 不补字段）", "",
        "> 仅生成「补全计划」：把每条缺锚 observation 命题、它的 evidence、以及**建议**的 `fixture_symbol` 列出。"
        "是否采用、补哪个符号是**人审权力**。", "",
        "## 一、总览", "",
        f"- 缺锚 observation 命题 **{p['total_missing']}** 条（607 实测 50，已锁定）；",
        "- 建议符号取自该命题 `evidence` 里第一个工件引用（ATOM-/EV-/example-）；evidence 空 ⇒ 待人裁定；", "",
        "## 二、补全计划明细", "",
        "| 卡 | 命题 id | 状态 | 建议 fixture_symbol | 证据 | 内容（截断） |",
        "|---|---|---|---|---|---|",
    ]
    for r in p["rows"][:60]:
        st = " ".join(str(x) for x in (r["evidence"] or [])) or "—"
        stmt = " ".join(str(r["statement"]).split())
        stmt = stmt[:40] + ("…" if len(stmt) > 40 else "")
        lines.append(f"| `{r['card']}` | `{r['prop_id']}` | {r['status']} | "
                     f"`{r['suggested_symbol']}` | {st} | {stmt} |")
    if len(p["rows"]) > 60:
        lines.append(f"| … | 其余 {len(p['rows']) - 60} 条见 JSON | | | | |")
    lines += ["", "## 三、口径与边界", "",
              "- 复用 607 `proposition_liveness_audit.audit` 的判定（同源、不重实现）；",
              "- `needs_review`（external_basis）不进本计划（那类由人决定改标 inference 或补夹具锚）；",
              "- 绝不写命题卡、绝不自动补 `liveness`；本文件只是人审工作台。", ""]
    return "\n".join(lines)


def check(p: dict) -> list[str]:
    problems: list[str] = []
    if p["total_missing"] != KNOWN_MISSING:
        problems.append(f"缺锚 observation 命题应为 {KNOWN_MISSING}（实测 {p['total_missing']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="liveness_completion_plan",
                                 description="611 D2 活性锚补全计划（只读）")
    ap.add_argument("--version", action="version", version=f"liveness_completion_plan {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--atoms-root", default=None, help="测试注入：只扫该目录")
    a = ap.parse_args(argv)
    plan = build_plan(a.atoms_root)
    if a.stats:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(plan)
        if problems:
            for p in problems:
                print(f"[D2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[D2] ✓ 活性锚补全计划锁定（缺锚 {plan['total_missing']} 条）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render_report(plan), encoding="utf-8", newline="\n")
        print(f"[D2] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（缺锚 {plan['total_missing']} 条）")
        return 0
    print(f"缺锚 observation 命题 {plan['total_missing']} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
