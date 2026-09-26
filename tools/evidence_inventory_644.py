"""644 阶段 0 · 任务 0.2 现有证据盘点。

扫描所有原子卡（28 张）的 `evidence` 引用与现有 `evidence/` 下证据文件，
统计来源类型 / 数量 / 完整度（artifact_sha256 是否齐备），产出
`data/644_evidence_inventory.md`。

只读：不修改 atoms/、evidence/ 或任何受控目录。

`--check` 只读幂等（selftest）；`--report` 写盘点文档。
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_evidence_inventory.md")


def inventory() -> dict[str, Any]:
    atoms = base.list_atoms()
    evs = base.list_existing_evidence()
    ev_by_id = {e["id"]: e for e in evs}

    cards_with_ev = 0
    total_refs = 0
    kind_counter: Counter[str] = Counter()
    missing_sha = 0
    missing_serves = 0
    domain_counter: Counter[str] = Counter()
    ref_to_missing = 0

    for a in atoms:
        rid = a["id"]
        domain = rid.split("-")[1] if "-" in rid else "?"
        domain_counter[domain] += 1
        refs = a["evidence_refs"]
        if refs:
            cards_with_ev += 1
        total_refs += len(refs)
        for r in refs:
            ev = ev_by_id.get(r)
            if ev is None:
                ref_to_missing += 1
                kind_counter["<缺失文件>"] += 1
                continue
            kind = str(ev["meta"].get("kind", "unknown"))
            kind_counter[kind] += 1
            if not ev["meta"].get("artifact_sha256"):
                missing_sha += 1
            if not ev["meta"].get("serves"):
                missing_serves += 1

    n_ev = len(evs)
    completeness = (n_ev - missing_sha) / n_ev if n_ev else 0.0

    return {
        "n_atoms": len(atoms),
        "n_evidence_files": n_ev,
        "cards_with_evidence": cards_with_ev,
        "total_refs": total_refs,
        "refs_to_missing_file": ref_to_missing,
        "kind_distribution": dict(kind_counter),
        "missing_sha256": missing_sha,
        "missing_serves": missing_serves,
        "completeness_ratio": round(completeness, 4),
        "domain_distribution": dict(domain_counter),
        "ev_by_id_keys": list(ev_by_id.keys()),
    }


def render_md(inv: dict[str, Any]) -> str:
    lines = [
        "# 644 阶段 0 · 现有证据盘点（`data/644_evidence_inventory.md`）",
        "",
        f"- 原子卡总数：**{inv['n_atoms']}**",
        f"- 现有证据文件（`evidence/`）：**{inv['n_evidence_files']}**",
        f"- 含证据引用的卡：**{inv['cards_with_evidence']}**",
        f"- 卡→证据引用总数：**{inv['total_refs']}**",
        f"- 引用指向缺失文件的次数：**{inv['refs_to_missing_file']}**",
        f"- 证据文件缺 `artifact_sha256`：**{inv['missing_sha256']}**",
        f"- 证据文件缺 `serves`：**{inv['missing_serves']}**",
        f"- 完整度（有 sha256 / 总量）：**{inv['completeness_ratio']:.2%}**",
        "",
        "## 来源类型（kind）分布",
        "",
        "| kind | 数量 |",
        "|---|---|",
    ]
    for k, v in sorted(inv["kind_distribution"].items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines += ["", "## 领域（domain）分布", "", "| domain | 卡数 |", "|---|---|"]
    for k, v in sorted(inv["domain_distribution"].items()):
        lines.append(f"| {k} | {v} |")
    lines += ["", "> 本盘点为只读扫描，未修改任何受控目录。",
              "> 头部层（644）将在 `data/evidence_store/` 建立**独立**的内容寻址证据库，",
              "> 与现有 `evidence/` 解耦，不迁移、不改动既有文件。"]
    return "\n".join(lines) + "\n"


def write_report() -> str:
    inv = inventory()
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(inv))
    return OUT_MD


def _expected_atom_count() -> int:
    n = 0
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(base.ATOMS_DIR, domain)
        if os.path.isdir(d):
            n += sum(1 for fn in os.listdir(d) if fn.endswith(".md"))
    return n


def selftest() -> int:
    inv = inventory()
    # 注意：计划书称「28 张卡」，实测当前仓库为 27 张（计划书数字偏旧，已在验收报告登记）。
    # 自检用文件系统实际数量，避免硬编码导致假红。
    assert inv["n_atoms"] == _expected_atom_count(), inv["n_atoms"]
    assert inv["n_evidence_files"] > 0
    assert 0.0 <= inv["completeness_ratio"] <= 1.0
    # 渲染不抛错且含关键统计
    md = render_md(inv)
    assert str(inv["n_atoms"]) in md and "完整度" in md
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 现有证据盘点")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写盘点文档")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
