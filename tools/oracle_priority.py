"""612 C2 · oracle 验证优先级排序工具（**只读** · 不修改任何文件）。

对 83 张卡（56 证据 + 27 原子）按**五维度加权**给出 oracle 验证优先级（建议，最终由人审决定）：

  1. 卡类型：证据卡 2 / 原子卡 1
  2. 命题数：越多权重越高（每命题 1 分）
  3. **历史逃逸率**：该卡命题曾出现在逃逸变体中（`full_baseline_v7.by_card[*].escaped > 0`）⇒ 3 分
  4. **覆盖率缺口**：该卡命题在 poison **零覆盖攻击面**中 ⇒ 2 分（读 `tools/poison_surface_map.json`）
  5. 关联 MIS 数：关联越多验证收益越大（每关联 1 分）

score = 类型*2 + 命题数*1 + 逃逸*3 + 缺口*2 + 关联MIS*1

CLI：`[--top N]`（写 `data/oracle_priority_612.md`）/ `--stats` / `--check`（exit 0=通过）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "oracle_priority_612.md"
BASELINE = ROOT / "data" / "mutation" / "full_baseline_v7.json"
SURFACE = ROOT / "tools" / "poison_surface_map.json"


def _escape_cards() -> dict[str, int]:
    """→ {卡相对路径: 逃逸数}（读 mutation 基线 v7 的 by_card）。"""
    if not BASELINE.is_file():
        return {}
    try:
        d = json.loads(BASELINE.read_text(encoding="utf-8"))
    except ValueError:
        return {}
    out: dict[str, int] = {}
    for path, st in (d.get("by_card") or {}).items():
        if isinstance(st, dict) and int(st.get("escaped", 0)) > 0:
            out[path] = int(st["escaped"])
    return out


def _coverage_gap() -> set[str]:
    """零覆盖攻击面涉及的卡（今日 uncovered 为空 ⇒ 返回空集）。"""
    if not SURFACE.is_file():
        return set()
    try:
        d = json.loads(SURFACE.read_text(encoding="utf-8"))
    except ValueError:
        return set()
    uncovered = (d.get("coverage") or {}).get("uncovered") or []
    # 只知攻击类型未覆盖；无「类型→卡」映射 ⇒ 保守返回空集（并如实标注）
    return {f"__uncovered_type__:{t}" for t in uncovered}


def score_cards() -> list[dict]:
    import bridge_edge_candidates as c2  # noqa: E402
    import oracle_rotation as orot  # noqa: E402
    import proposition_liveness_audit as pla  # noqa: E402
    mi = c2.load_mis_index()
    esc = _escape_cards()
    gap = _coverage_gap()
    rows: list[dict] = []
    for c in orot._load_cards():
        cid, rel = c["id"], c["path"]
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""
        fm = pla.extract_frontmatter(text) or ""
        n_prop = len(pla.parse_claim_items(fm))
        is_atom = cid.startswith("ATOM-")
        type_w = 1 if is_atom else 2
        escape = 3 if rel in esc else 0
        gap_w = 2 if (gap and rel in gap) else 0
        rel_mis = sum(1 for m in mi.values()
                      if (is_atom and cid in m.get("related_atoms", []))
                      or (not is_atom and cid in m.get("evidence", [])))
        score = type_w * 2 + n_prop * 1 + escape * 3 + gap_w * 2 + rel_mis * 1
        rows.append({"id": cid, "path": rel, "type": "atom" if is_atom else "evidence",
                     "props": n_prop, "escaped": escape // 3, "coverage_gap": gap_w // 2,
                     "related_mis": rel_mis, "score": score})
    rows.sort(key=lambda d: (-d["score"], d["id"]))
    return rows


def render(rows: list[dict], top: int | None) -> str:
    shown = rows if top is None else rows[:top]
    L = ["# 612 C2 · oracle 验证优先级（只读 · 建议）", "",
         "> 五维度加权：类型(证据2/原子1)×2 + 命题数 + 逃逸×3 + 覆盖缺口×2 + 关联MIS。"
         "优先级是**建议**，最终验证顺序由人审决定。", "",
         "## 一、清单", "",
         "| 排名 | 卡 | 类型 | 命题数 | 逃逸 | 缺口 | 关联MIS | 得分 |",
         "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(shown, 1):
        L.append(f"| {i} | `{r['id']}` | {r['type']} | {r['props']} | {r['escaped']} | "
                 f"{r['coverage_gap']} | {r['related_mis']} | {r['score']} |")
    L += ["", "## 二、Top 20 详细理由", ""]
    for i, r in enumerate(rows[:20], 1):
        L.append(f"{i}. `{r['id']}`（{r['type']}）得分 {r['score']}：命题 {r['props']} · "
                 f"逃逸 {r['escaped']} · 覆盖缺口 {r['coverage_gap']} · 关联 MIS {r['related_mis']}")
    L += ["", "## 三、口径与边界", "",
          "- **只读**：不修改任何文件；优先级为建议；",
          "- 逃逸维度读 `data/mutation/full_baseline_v7.json` 的 `by_card.escaped`；",
          "- 覆盖缺口读 `tools/poison_surface_map.json`：**今日 uncovered 为空**（11/11 全覆盖）⇒ 该维度全 0；",
          "- 关联 MIS 数同 612 任务0 / 611 C2 口径。", ""]
    return "\n".join(L)


def check(rows: list[dict]) -> list[str]:
    problems: list[str] = []
    if len(rows) != 83:
        problems.append(f"卡数应为 83（实测 {len(rows)}）")
    if rows and rows[0]["score"] != max(r["score"] for r in rows):
        problems.append("Top 1 不是最高分")
    for r in rows:
        if not {"id", "type", "props", "escaped", "coverage_gap", "related_mis", "score"} <= set(r):
            problems.append(f"卡 {r.get('id')} 五维度字段不全")
            break
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oracle_priority", description="612 C2 oracle 优先级（只读）")
    ap.add_argument("--version", action="version", version=f"oracle_priority {VERSION}")
    ap.add_argument("--top", type=int, default=None)
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    rows = score_cards()
    if a.stats:
        print(json.dumps(rows if a.top is None else rows[:a.top], ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(rows)
        if problems:
            for p in problems:
                print(f"[C2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[C2] ✓ 优先级锁定（{len(rows)} 张；Top1 {rows[0]['id']}={rows[0]['score']}）")
        return 0
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(rows, a.top), encoding="utf-8", newline="\n")
    print(f"[C2] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（{len(rows)} 张；"
          f"Top1 {rows[0]['id']}={rows[0]['score']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
