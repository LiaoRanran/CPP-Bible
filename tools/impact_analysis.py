#!/usr/bin/env python3
"""425 上游依赖遍历（415 L2 最小闭环）：改一颗原子前，先看谁依赖它。

问题（415 调研）：改一颗原子，哪些原子受影响？当前靠人记，应该机器算。
最小可行闭环 = 给定原子 A，列出所有「prerequisite/specializes/realizes 指向 A」的原子。
不做加权、不做影响优先级——先解决 80% 的问题（改之前先看谁依赖我）。

用法：
  python tools/impact_analysis.py upstream ATOM-MEM-RAII-001 [--json]
  python tools/impact_analysis.py downstream ATOM-MEM-RAII-001 [--json]

关系语义（与 gate_engine 同源，单点复用 `_relations_norm`，417 已归一双写法）：
  * 依赖（DEP_REL）：prerequisite / specializes / realizes —— 改被依赖方须检查依赖方；
  * 引用（其余）：contrasts / see_also / contradicts / conflicts_with / evolved_from
    —— 对照/参见/冲突/演化，不构成「改了会坏」的依赖。

零风险：只读 atoms/*.md 的 frontmatter，不修改任何文件。
JSON 输出与四工具 --json 风格一致（tool/version/timestamp + 结果体）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v7.0"
# 依赖型关系：415 L2 口径（evolved_from 属演化链引用，不计入「改了会坏」）
DEP_REL = {"prerequisite", "specializes", "realizes"}


def _relpath(p: Path) -> str:
    """相对 ROOT 的显示路径（沙箱等 ROOT 外路径原样返回，不抛 ValueError）。"""
    try:
        return p.relative_to(ge.ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def _all_rels(meta: dict[str, Any]) -> list[dict[str, str]]:
    """全类型 relations 归一（含 contrasts/see_also 等引用型）。

    gate_engine._relations_norm 只归一 DAG_REL ∪ CONFLICT_REL（门禁视野），
    mapping-form 的 contrasts/see_also 会被它丢弃——本工具需要**全类型**，
    故本地做同构归一（只读，不影响门禁判据）。
    """
    out: list[dict[str, str]] = []
    for rel in ge._as_list(meta.get("relations")):
        if not isinstance(rel, dict):
            continue
        if rel.get("type") or rel.get("target"):
            out.append({"type": str(rel.get("type") or ""),
                        "target": str(rel.get("target") or "")})
            continue
        for k, v in rel.items():
            if str(k) in ("type", "target"):
                continue
            out.append({"type": str(k), "target": str(v)})
    return [e for e in out if e["type"] and e["target"]]


def _atom_index() -> tuple[dict[str, Path], dict[str, dict[str, Any]]]:
    """{id: 路径} 与 {id: frontmatter}（单次扫描，调用方复用）。"""
    paths: dict[str, Path] = {}
    metas: dict[str, dict[str, Any]] = {}
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        meta = ge._meta(p)
        aid = str(meta.get("id") or p.stem)
        paths[aid] = p
        metas[aid] = meta
    return paths, metas


def _rel_of(metas: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    """{id: [{type, target}]}——归一后的关系边（全类型，见 _all_rels）。"""
    return {aid: _all_rels(meta) for aid, meta in metas.items()}


def upstream(atom_id: str, rel_types: set[str] | None = None) -> list[dict[str, str]]:
    """列出所有直接依赖 atom_id 的原子（谁声明了指向它的依赖型关系）。"""
    deps = rel_types or DEP_REL
    paths, metas = _atom_index()
    rels = _rel_of(metas)
    out = [
        {"atom": aid, "rel_type": e["type"],
         "path": _relpath(paths[aid])}
        for aid, edges in rels.items() for e in edges
        if e["type"] in deps and e["target"] == atom_id
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def references(atom_id: str) -> list[dict[str, str]]:
    """列出所有**引用** atom_id 的原子（contrasts/see_also 等——不构成依赖）。"""
    paths, metas = _atom_index()
    rels = _rel_of(metas)
    out = [
        {"atom": aid, "rel_type": e["type"],
         "path": _relpath(paths[aid])}
        for aid, edges in rels.items() for e in edges
        if e["type"] not in DEP_REL and e["target"] == atom_id
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def downstream(atom_id: str) -> list[dict[str, str]]:
    """列出 atom_id 直接依赖的原子（它的依赖型关系指向谁）。"""
    paths, metas = _atom_index()
    out = [
        {"atom": e["target"], "rel_type": e["type"],
         "path": (_relpath(paths[e["target"]])
                  if e["target"] in paths else "（不存在）")}
        for e in _rel_of(metas).get(atom_id, []) if e["type"] in DEP_REL
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def report(direction: str, atom_id: str) -> dict[str, Any]:
    """组装单次查询的完整结果（deps + refs/下游，JSON 与人读共用）。"""
    paths, _ = _atom_index()
    if atom_id not in paths:
        raise SystemExit(f"[impact] 原子不存在：{atom_id}（现存 {len(paths)} 颗）")
    deps = upstream(atom_id) if direction == "upstream" else downstream(atom_id)
    refs = references(atom_id) if direction == "upstream" else []
    return {
        "tool": "impact_analysis", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "direction": direction, "atom": atom_id,
        "deps": deps, "refs": refs,
        "summary": {"deps": len(deps), "refs": len(refs)},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="上游/下游依赖遍历（425：改原子前先看谁依赖它）")
    ap.add_argument("direction", choices=["upstream", "downstream"])
    ap.add_argument("atom_id", help="目标原子 id（如 ATOM-MEM-RAII-001）")
    ap.add_argument("--json", action="store_true", help="输出 JSON（与四工具风格一致）")
    a = ap.parse_args(argv)

    data = report(a.direction, a.atom_id)
    if a.json:
        print(json.dumps(data, ensure_ascii=False, indent=1))
        return 0
    print(f"[impact] {data['atom']} 的{'上游依赖者' if a.direction == 'upstream' else '下游依赖'}"
          f"（{len(data['deps'])}）：")
    for d in data["deps"]:
        print(f"  - {d['rel_type']:<14} {d['atom']}  ({d['path']})")
    if a.direction == "upstream":
        print(f"[impact] 引用（不构成依赖，{len(data['refs'])}）：")
        for r in data["refs"]:
            print(f"  - {r['rel_type']:<14} {r['atom']}  ({r['path']})")
    return 0


if __name__ == "__main__":
    main()
