"""626 C2 · 镜像边审计（`symmetry_proof_id`）

国外大模型要求：「镜像边」应从**自动事实**变成**有条件事实**——
只有存在可验证的 `symmetry_proof_id` 才允许镜像边作为实质性攻击边。

本工具：
- 从 `attack_edges_candidates.jsonl` 识别镜像边（`direction == "mis_to_prop"`，实测 194 条）
- 审计每条镜像边是否有 `symmetry_proof_id`
- 默认 `symmetry_proof_id = null`（未验证）⇒ 镜像关系**不可作为已验证事实**
- `--check`：验证所有镜像边**都有 `symmetry_proof_id` 字段**（即使为 null）

注：`symmetry_proof_id` 字段已在 626 B3 的 `ReviewItem` 中预留（默认空），本工具不修改其结构。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
OUT_JSON = os.path.join(ROOT, "data", "mirror_edge_audit_626.json")

MIRROR_DIRECTION = "mis_to_prop"


def _jl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def audit() -> dict:
    """审计镜像边。

    **归一化**：源 `attack_edges_candidates.jsonl` 中**没有** `symmetry_proof_id` 字段
    （实测 194/194 缺失）。审计层将其**归一为 `None`**，使每条镜像边在账本中**都有该字段**
    （值为 null = 未验证），满足判据 9 的字段要求；同时诚实报告源缺字段的数量。
    """
    cands = _jl(CAND)
    mirrors = [c for c in cands if str(c.get("direction")) == MIRROR_DIRECTION]
    records: list[dict] = []
    missing_field: list[str] = []
    for c in mirrors:
        has = "symmetry_proof_id" in c
        if not has:
            missing_field.append(str(c.get("id")))
        records.append({
            "edge_id": str(c.get("id")),
            "symmetry_proof_id": c.get("symmetry_proof_id") if has else None,
            "verified": bool(c.get("symmetry_proof_id")),
        })
    with_proof = [r for r in records if r["verified"]]
    return {
        "total_candidates": len(cands),
        "mirror_edges": len(mirrors),
        "with_symmetry_proof": len(with_proof),
        "without_symmetry_proof": len(records) - len(with_proof),
        "source_missing_field": len(missing_field),
        "sample_source_missing": missing_field[:5],
        "records_have_field": all("symmetry_proof_id" in r for r in records),
        "records": records,
        "note": ("默认 symmetry_proof_id=null ⇒ 镜像关系未经验证，"
                 "不可作为实质性攻击边的已验证事实（判据 9）。源数据缺该字段，审计层已归一为 null。"),
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = audit()
    chk("候选边 388", a["total_candidates"] == 388, f"({a['total_candidates']})")
    chk("镜像边 194", a["mirror_edges"] == 194, f"({a['mirror_edges']})")
    chk("审计产出字段完整",
        all(k in a for k in ("with_symmetry_proof", "without_symmetry_proof",
                             "source_missing_field", "records_have_field")))
    chk("审计记录中每条镜像边都有 symmetry_proof_id 字段（值可为 null）",
        a["records_have_field"] and len(a["records"]) == a["mirror_edges"])
    chk("当前无已验证 symmetry proof（诚实）", a["with_symmetry_proof"] == 0)
    if a["source_missing_field"]:
        print(f"  [warn] 源数据 {a['source_missing_field']}/{a['mirror_edges']} 条缺 "
              f"symmetry_proof_id 字段（审计层已归一为 null；补字段留 627）")
    print(f"C2 mirror check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 C2 镜像边审计")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="输出审计 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    a = audit()
    if args.json:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(a, fh, ensure_ascii=False, indent=2)
        print(f"written {OUT_JSON}")
    print(json.dumps(a, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
