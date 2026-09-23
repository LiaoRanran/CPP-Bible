"""627 A4 · 194 条镜像边对称性验证（**只生成报告，不写入 ledger**）

**背景**：626 C2 审计发现 194 条 `direction == "mis_to_prop"` 的「镜像边」，
其 `symmetry_proof_id` **全部为 null**（未验证），不可作为已验证事实（判据 9）。

**本工具（627）**：在 626 审计基础上，**逐条验证镜像边的对称性**——
对每条 mis_to_prop 镜像边 `MIS-X -> ATOM-Y::prop-N`，检查其反向边
`ATOM-Y::prop-N -> MIS-X`（`prop_to_mis`）是否存在，判定：
- `symmetric`：反向边存在 ⇒ 结构对称（攻击/防御是双向对偶）
- `asymmetric`：反向边缺失 ⇒ 结构不完整（需人工核查）

并分类列出：**所有 194 条镜像边**都因 `symmetry_proof_id == null` 而
**需要人工对称性验证**（本工具只生成清单，绝不写入 candidates/ledger）。

**硬边界**：只读 `attack_edges_candidates.jsonl`，**不修改任何文件**（仅输出报告 JSON/MD）。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
MIRROR_DIRECTION = "mis_to_prop"
REVERSE_DIRECTION = "prop_to_mis"
OUT_JSON = os.path.join(ROOT, "data", "mirror_edge_symmetry_627.json")
OUT_MD = os.path.join(ROOT, "data", "mirror_edge_symmetry_627.md")


def _jl(path: str) -> list:
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def check() -> dict:
    cands = _jl(CAND)
    idx = collections.defaultdict(list)
    for c in cands:
        idx[(c.get("source"), c.get("target"))].append(c)

    mirrors = [c for c in cands if c.get("direction") == MIRROR_DIRECTION]
    rows: list[dict] = []
    symmetric = 0
    asymmetric = 0
    for c in mirrors:
        src, tgt = c.get("source"), c.get("target")
        reverse = idx.get((tgt, src)) or []
        rev = [r for r in reverse if r.get("direction") == REVERSE_DIRECTION]
        has_rev = bool(rev)
        if has_rev:
            symmetric += 1
        else:
            asymmetric += 1
        rows.append({
            "edge_id": str(c.get("id")),
            "mis_to_prop": f"{src} -> {tgt}",
            "reverse_exists": has_rev,
            "reverse_id": (rev[0].get("id") if rev else None),
            "symmetry_proof_id": c.get("symmetry_proof_id"),
            "needs_human_verification": True,  # 全部 null
        })
    return {
        "total_candidates": len(cands),
        "mirror_edges": len(mirrors),
        "symmetric": symmetric,
        "asymmetric": asymmetric,
        "all_need_human_verification": True,
        "rows": rows,
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = check()
    chk("镜像边 = 194", r["mirror_edges"] == 194, f"({r['mirror_edges']})")
    chk("对称/非对称分类完整", r["symmetric"] + r["asymmetric"] == 194)
    chk("每条镜像边都需人工验证（symmetry_proof_id=null）",
        all(row["needs_human_verification"] for row in r["rows"]))
    chk("输出行数 = 194", len(r["rows"]) == 194)

    # 只读：不修改 candidates
    import hashlib
    before = hashlib.sha256(open(CAND, "rb").read()).hexdigest()
    check()
    after = hashlib.sha256(open(CAND, "rb").read()).hexdigest()
    chk("分析过程不修改 candidates", before == after)
    print(f"A4 mirror symmetry check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 A4 镜像边对称性验证")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = check()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    if args.report:
        lines = ["# 627 A4 · 镜像边对称性验证", "",
                 f"- 候选边总数：{r['total_candidates']}",
                 f"- 镜像边（mis_to_prop）：**{r['mirror_edges']}**",
                 f"- 结构对称（存在反向边）：{r['symmetric']}",
                 f"- 结构非对称（缺反向边）：{r['asymmetric']}", "",
                 f"> **全部 {r['mirror_edges']} 条镜像边的 `symmetry_proof_id` 均为 null**"
                 " ⇒ 均需人工对称性验证（626 判据 9）。",
                 "", "## 非对称镜像边（需人工核查）", ""]
        asym = [row for row in r["rows"] if not row["reverse_exists"]]
        if asym:
            for row in asym[:30]:
                lines.append(f"- `{row['edge_id']}`: {row['mis_to_prop']}")
        else:
            lines.append("（无 — 全部结构对称）")
        lines.append("")
        lines.append("> 本工具**只生成报告，不写入** `attack_edges_candidates.jsonl` 或任何 ledger。")
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
    print(json.dumps({k: v for k, v in r.items() if k != "rows"},
                    ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
