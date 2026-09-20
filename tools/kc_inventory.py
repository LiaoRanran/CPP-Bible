#!/usr/bin/env python3
"""612 线 D · D1：KC（知识组件）台账工具（**只读**）。

从 27 张原子卡（ATOM-*.md）抽取 KC 台账，作为「学习者镜像」原型的知识图谱底座：
  * 卡 ID / 标题 / 路径 / 领域
  * 命题列表（observation / inference，含 id 与 statement）
  * 关联 MIS（反向索引 `data/flashcards/markdown/misconception_*.md` 的「关联原子：ATOM-XXX」）
  * 难度等级（1-5 级，**自动估算的建议**，按 spec 的命题数 / 关联 MIS 数分档）
  * 前置依赖 / 后继依赖（来自卡面 `relations` 的 `prerequisite` 关系）

口径与边界（诚实）：
  * 只读：不修改任何卡面。
  * 难度是「建议」估算，非客观难度；分档公式直接套用任务书 bands（命题数 / 关联 MIS 数）。
  * 前置依赖来自 `relations`（任务书称「基于 evidence 引用关系推导」；但本仓 evidence 指向 EV 卡、
    不是 ATOM 卡，故以 `relations.prerequisite` 为权威来源，并标注「自动推导，待人工复核」）。
  * 复用的卡面解析 = `gate_engine._meta`（已在门禁中反复验证可解析本仓卡面）。

用法：
  python tools/kc_inventory.py           # 生成台账（JSON + MD 报告）
  python tools/kc_inventory.py --check    # 自验证（exit 0=通过）
  python tools/kc_inventory.py --stats    # 输出统计（难度分布 / 平均命题数 / 平均关联 MIS 数）
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATOMS = ROOT / "atoms"
FLASH_DIR = ROOT / "data" / "flashcards" / "markdown"
JSON_OUT = ROOT / "data" / "kc_inventory_612.json"
REPORT_OUT = ROOT / "data" / "kc_inventory_612.md"

KNOWN_KC_COUNT = 27  # 611/612 锁定的原子卡数


def _gate():
    import gate_engine as g  # noqa: E402
    return g


# ── MIS 反向索引 ──────────────────────────────────────────────────────────
def mis_reverse_index(flash_dir: Path = FLASH_DIR) -> dict[str, list[str]]:
    """ATOM id → 关联 MIS id 列表（扫 misconception_*.md 的「关联原子：ATOM-XXX」）。"""
    idx: dict[str, list[str]] = {}
    if not flash_dir.is_dir():
        return idx
    rx = re.compile(r"关联原子[:：]\s*(ATOM-[\w-]+)")
    for p in sorted(flash_dir.glob("misconception_*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        for atom in rx.findall(text):
            idx.setdefault(atom.strip(), []).append(p.stem)
    return idx


# ── 难度分档（套用任务书 bands）──────────────────────────────────────────
def difficulty_level(n_props: int, n_mis: int) -> int:
    """任务书 D1 bands：命题数 或 关联 MIS 数 任一落入即定级（取较高档）。"""
    def from_props(n: int) -> int:
        if n <= 2:
            return 1
        if n <= 4:
            return 2
        if n <= 6:
            return 3
        if n <= 8:
            return 4
        return 5

    def from_mis(n: int) -> int:
        if n <= 1:
            return 1
        if n <= 3:
            return 2
        if n <= 5:
            return 3
        if n <= 7:
            return 4
        return 5
    return max(from_props(n_props), from_mis(n_mis))


def build(atoms_root: Path = ATOMS, flash_dir: Path = FLASH_DIR) -> dict:
    g = _gate()
    mis_idx = mis_reverse_index(flash_dir)
    kcs: list[dict] = []
    prereq_edges: list[tuple[str, str]] = []  # (kc, prereq)
    for p in g._cards(atoms_root, "ATOM-*.md"):
        meta = g._meta(p)
        cid = str(meta.get("id") or p.stem)
        title = str(meta.get("title") or "")
        domain = str(meta.get("domain") or "")
        props_raw = meta.get("claim_structured") or []
        props: list[dict] = []
        for pr in props_raw:
            if not isinstance(pr, dict):
                continue
            props.append({
                "id": str(pr.get("id") or "?"),
                "claim_type": str(pr.get("claim_type") or ""),
                "statement": str(pr.get("statement") or pr.get("brief") or ""),
                "evidence": [str(x) for x in (pr.get("evidence") or []) if str(x).strip()],
            })
        n_obs = sum(1 for x in props if x["claim_type"] == "observation")
        n_inf = sum(1 for x in props if x["claim_type"] == "inference")
        rels = meta.get("relations") or []
        prereqs: list[str] = []
        for r in rels:
            if not isinstance(r, dict):
                continue
            if str(r.get("type") or "").lower() in ("prerequisite", "prereq", "requires"):
                t = str(r.get("target") or "").strip()
                if t:
                    prereqs.append(t)
                    prereq_edges.append((cid, t))
        mis = sorted(set(mis_idx.get(cid, [])))
        n_props_all = len(props)
        kcs.append({
            "id": cid, "title": title, "domain": domain,
            "path": p.relative_to(ROOT).as_posix(),
            "propositions": props, "n_propositions": n_props_all,
            "n_observation": n_obs, "n_inference": n_inf,
            "prerequisites": sorted(set(prereqs)),
            "related_mis": mis, "n_related_mis": len(mis),
            "difficulty": difficulty_level(n_props_all, len(mis)),
        })
    # 后继依赖（反向 prereq 边）
    succ: dict[str, list[str]] = {}
    for kc, pre in prereq_edges:
        succ.setdefault(pre, []).append(kc)
    for k in kcs:
        k["successors"] = sorted(set(succ.get(k["id"], [])))
    kcs.sort(key=lambda x: x["id"])
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_kc": len(kcs),
        "kcs": kcs,
        "note": ("只读台账：难度为自动估算建议（套用任务书分档）；前置依赖来自卡面 "
                 "`relations.prerequisite`（自动推导，待人工复核）；关联 MIS 为 "
                 "`misconception_*.md`「关联原子」反向索引。"),
    }


def render(d: dict) -> str:
    kcs = d["kcs"]
    diff = Counter(k["difficulty"] for k in kcs)
    avg_props = sum(k["n_propositions"] for k in kcs) / max(1, len(kcs))
    avg_mis = sum(k["n_related_mis"] for k in kcs) / max(1, len(kcs))
    with_pre = sum(1 for k in kcs if k["prerequisites"])
    L: list[str] = []
    L.append("# 612 D1 · KC 知识组件台账（只读）")
    L.append("")
    L.append(f"> 生成时间：{d['generated_at']} ｜ 命令：`python tools/kc_inventory.py`")
    L.append(">")
    L.append("> 27 张原子卡 = 27 个 KC。难度为**自动估算建议**（套用任务书分档），"
             "前置依赖来自卡面 `relations.prerequisite`（自动推导，待人工复核）。")
    L.append("")
    L.append("## 1 · 总览")
    L.append("")
    L.append(f"- KC 总数：**{d['total_kc']}**")
    L.append(f"- 平均命题数：{avg_props:.2f} ｜ 平均关联 MIS 数：{avg_mis:.2f}")
    L.append(f"- 有前置依赖的 KC：**{with_pre}** 张")
    L.append("")
    L.append("**难度分布**（1=易 … 5=难）：")
    L.append("")
    L.append("| 等级 | KC 数 |")
    L.append("|---|---|")
    for lv in range(1, 6):
        L.append(f"| {lv} | {diff.get(lv, 0)} |")
    L.append("")
    L.append("## 2 · KC 台账")
    L.append("")
    L.append("| KC | 领域 | 难度 | 命题(观/推) | 关联MIS | 前置依赖 | 后继 |")
    L.append("|---|---|---|---|---|---|---|")
    for k in kcs:
        pre = ", ".join(k["prerequisites"]) or "—"
        suc = ", ".join(k["successors"]) or "—"
        L.append(f"| `{k['id']}` | {k['domain']} | {k['difficulty']} | "
                 f"{k['n_propositions']}({k['n_observation']}/{k['n_inference']}) | "
                 f"{k['n_related_mis']} | {pre} | {suc} |")
    L.append("")
    L.append("## 3 · 依赖关系（前置 → 后继，自动推导）")
    L.append("")
    edges: list[str] = []
    for k in kcs:
        for pre in k["prerequisites"]:
            edges.append(f"- `{pre}` → `{k['id']}`")
    if edges:
        L.extend(edges)
    else:
        L.append("（无前置依赖边）")
    L.append("")
    L.append("## 4 · 口径与边界（诚实）")
    L.append("")
    L.append("- **难度是建议**：分档公式直接套用任务书 bands（命题数 / 关联 MIS 数取较高档），"
             "不声称客观难度。")
    L.append("- **前置依赖来源**：任务书写「基于 evidence 引用关系推导」，但本仓 evidence 指向 EV 卡而非 "
             "ATOM 卡，故以卡面 `relations.prerequisite` 为权威；可能与「真正应先学的卡」有出入，标注待复核。")
    L.append("- **关联 MIS**：`data/flashcards/markdown/misconception_*.md` 反向索引；未关联 MIS 的 KC 记 0。")
    L.append("- **只读**：不修改任何卡面 / 闪卡文件。")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 D1 · KC 知识组件台账（只读）")
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    ap.add_argument("--stats", action="store_true", help="输出统计 JSON")
    ap.add_argument("--atoms-root", default=None, help="测试注入：只扫该目录")
    ap.add_argument("--flash-dir", default=None, help="测试注入：MIS 闪卡目录")
    a = ap.parse_args(argv)
    d = build(Path(a.atoms_root) if a.atoms_root else ATOMS,
              Path(a.flash_dir) if a.flash_dir else FLASH_DIR)

    problems: list[str] = []
    if d["total_kc"] != KNOWN_KC_COUNT:
        problems.append(f"KC 数应为 {KNOWN_KC_COUNT}（实测 {d['total_kc']}）")
    if any(not (1 <= k["difficulty"] <= 5) for k in d["kcs"]):
        problems.append("存在难度等级不在 1-5 范围")
    if not any(k["prerequisites"] for k in d["kcs"]):
        problems.append("至少应有 1 张 KC 有前置依赖")
    for k in d["kcs"]:
        if k["n_propositions"] == 0:
            problems.append(f"KC {k['id']} 无命题（台账应有命题）")
    if problems:
        print("[D1] ❌ 自检失败：", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1

    if a.stats:
        stats = {
            "total_kc": d["total_kc"],
            "difficulty_distribution": dict(Counter(k["difficulty"] for k in d["kcs"])),
            "avg_propositions": round(sum(k["n_propositions"] for k in d["kcs"]) / d["total_kc"], 2),
            "avg_related_mis": round(sum(k["n_related_mis"] for k in d["kcs"]) / d["total_kc"], 2),
            "with_prerequisite": sum(1 for k in d["kcs"] if k["prerequisites"]),
        }
        print(json.dumps(stats, ensure_ascii=False, indent=1))
        return 0

    if a.check:
        print(f"[D1] ✅ 自验证通过：KC={d['total_kc']} / 有前置依赖={sum(1 for k in d['kcs'] if k['prerequisites'])} "
              f"/ 难度均∈[1,5]")
        return 0

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(d), encoding="utf-8")
    print(f"[D1] 已写 {JSON_OUT.relative_to(ROOT).as_posix()} 与 "
          f"{REPORT_OUT.relative_to(ROOT).as_posix()}（KC={d['total_kc']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
