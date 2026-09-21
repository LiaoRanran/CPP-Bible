#!/usr/bin/env python3
"""614 线E E1 · oracle 验证优先级（离线排序 · 只读 · 建议）。

在 612 C2 `oracle_priority.py` 的五维加权基线上，叠加 **614 维度**，使「危险卡」更优先：

  612 基线：score = 类型(证据2/原子1)×2 + 命题数×1 + 逃逸×3 + 覆盖缺口×2 + 关联MIS×1
  614 叠加：+ **known_tce×5**（`data/mutation/known_tce.jsonl` 中登记为结构性逃逸的卡——最该先验）
            + **kc_related×1**（该卡是本仓 KC 图（`kc_inventory`）的核心 KC——联动学习者镜像）

⇒ 优先级是**建议**，最终验证顺序由人审决定（oracle 对人审负责，非自动裁决）。

CLI：
  python tools/oracle_priority_614.py [--top N]   # 写 data/oracle_priority_614.md
  python tools/oracle_priority_614.py --stats     # 打印 JSON
  python tools/oracle_priority_614.py --check     # 自验证（exit 0=通过）

铁律：**只读**（不改任何受控文件/卡）；不重跑监工门禁；优先级≠裁决。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import oracle_priority as op612  # noqa: E402

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "oracle_priority_614.md"
KNOWN_TCE = ROOT / "data" / "mutation" / "known_tce.jsonl"


def _known_tce_cards() -> set[str]:
    """登记为 known-structural 逃逸的卡（相对路径）。"""
    if not KNOWN_TCE.is_file():
        return set()
    out: set[str] = set()
    for line in KNOWN_TCE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("status") == "known-structural" and rec.get("card"):
            out.add(str(rec["card"]))
    return out


def _kc_ids() -> set[str]:
    import kc_inventory as d1  # noqa: E402
    return {k["id"] for k in d1.build()["kcs"]}


def score_cards() -> list[dict]:
    rows = op612.score_cards()
    tce = _known_tce_cards()
    kcs = _kc_ids()
    for r in rows:
        kc_related = r["id"] in kcs
        known = r["path"] in tce
        r["base_score"] = r["score"]
        r["kc_related"] = kc_related
        r["known_tce"] = known
        r["score"] = r["base_score"] + (5 if known else 0) + (1 if kc_related else 0)
    rows.sort(key=lambda d: (-d["score"], d["id"]))
    return rows


def render(rows: list[dict], top: int | None) -> str:
    shown = rows if top is None else rows[:top]
    L = ["# 614 E1 · oracle 验证优先级（只读 · 建议）", "",
         "> 612 五维基线 + **614 叠加**（known_tce×5 + kc_related×1）。"
         "优先级是**建议**，最终验证顺序由**人审**决定。", "",
         "## 一、优先级清单", "",
         "| 排名 | 卡 | 类型 | 命题 | 逃逸 | 缺口 | MIS | known_tce | KC | 614 得分 | 基线得分 |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(shown, 1):
        L.append(f"| {i} | `{r['id']}` | {r['type']} | {r['props']} | {r['escaped']} | "
                 f"{r['coverage_gap']} | {r['related_mis']} | {'⚠' if r['known_tce'] else ''} | "
                 f"{'●' if r['kc_related'] else ''} | **{r['score']}** | {r['base_score']} |")
    L += ["", "## 二、Top 20 理由", ""]
    for i, r in enumerate(rows[:20], 1):
        why = []
        if r["known_tce"]:
            why.append("**已知结构性逃逸（TCE）**")
        if r["escaped"]:
            why.append("历史逃逸")
        if r["kc_related"]:
            why.append("核心 KC")
        why.append(f"命题 {r['props']}")
        why.append(f"关联MIS {r['related_mis']}")
        L.append(f"{i}. `{r['id']}` 得分 {r['score']}（基线 {r['base_score']}）：" + " · ".join(why))
    L += ["", "## 三、口径与边界", "",
          "- 612 基线五维见 `tools/oracle_priority.py`；614 叠加 known_tce×5、kc_related×1；",
          "- `known_tce` 读 `data/mutation/known_tce.jsonl`（status=known-structural）；",
          "- `kc_related` 读 `kc_inventory`（本仓 KC 图，联动学习者镜像线）；",
          "- **只读**、**建议**；不重跑任何监工门禁；**优先级≠裁决**（裁决权在人）。", ""]
    return "\n".join(L) + "\n"


def check(rows: list[dict]) -> list[str]:
    problems: list[str] = []
    if len(rows) != 83:
        problems.append(f"卡数应为 83（实测 {len(rows)}）")
    if rows:
        if rows[0]["score"] != max(r["score"] for r in rows):
            problems.append("Top 1 不是最高分")
        if any(rows[i]["score"] < rows[i + 1]["score"] for i in range(len(rows) - 1)):
            problems.append("排序未按得分降序")
    for r in rows:
        need = {"id", "path", "type", "props", "escaped", "coverage_gap",
                "related_mis", "base_score", "kc_related", "known_tce", "score"}
        if not need <= set(r):
            problems.append(f"卡 {r.get('id')} 字段不全")
            break
        if r["score"] != r["base_score"] + (5 if r["known_tce"] else 0) + (1 if r["kc_related"] else 0):
            problems.append(f"卡 {r.get('id')} 614 叠加公式不符")
            break
    # known_tce 卡必须存在且被加分
    tce = [r for r in rows if r["known_tce"]]
    if not tce:
        problems.append("应至少有一张 known_tce 卡（TCE-614-001）")
    elif tce[0]["score"] <= tce[0]["base_score"]:
        problems.append("known_tce 卡未被加分")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oracle_priority_614", description="614 E1 oracle 优先级")
    ap.add_argument("--version", action="version", version=f"oracle_priority_614 {VERSION}")
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
                print(f"[E1] ❌ {p}", file=sys.stderr)
            return 1
        tce = [r for r in rows if r["known_tce"]]
        print(f"[E1] ✅ 优先级锁定（{len(rows)} 张；Top1 {rows[0]['id']}={rows[0]['score']}；"
              f"known_tce {len(tce)} 张）")
        return 0
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(rows, a.top), encoding="utf-8", newline="\n")
    print(f"[E1] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（{len(rows)} 张；"
          f"Top1 {rows[0]['id']}={rows[0]['score']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
