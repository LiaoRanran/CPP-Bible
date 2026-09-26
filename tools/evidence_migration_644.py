"""644 阶段 C · C4 证据库迁移工具（只读迁移，不修改原文件）。

把现有 evidence/ 文件的关键事实迁移到头部层证据库 `data/evidence_store/`：
- 提取每条证据的内容（关键字段 + 正文）
- 计算 EvidenceID（内容寻址）
- 存入 evidence_store（grade 由 B1 启发式；acquisition_method=migration_644）
- 建立卡片-证据关联

**只读迁移**：只读取证据原文件、向 store 追加写入，**绝不修改** evidence/ 或 atoms/ 原文件。
输出迁移报告（迁移了多少条、多少条失败、失败原因）。
`--check` 只读幂等（dry-run）；`--migrate` 真正写入 store；`--report` 写迁移报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_migration_report.md")


def extract_content(meta: dict[str, Any], body: str) -> str:
    """把证据关键字段 + 正文规范化为内容寻址用的 canonical 文本。"""
    keys = ("id", "kind", "hypothesis", "command", "expected", "actual",
            "verdict", "artifact_sha256", "serves")
    parts = []
    for k in keys:
        v = meta.get(k)
        if v is not None:
            parts.append(f"{k}: {v}")
    parts.append("---BODY---")
    parts.append(body.strip())
    return "\n".join(parts)


def migrate_all(dry_run: bool = True) -> dict[str, Any]:
    """对现有 evidence/ 全量迁移（dry_run=True 不写 store）。返回报告。"""
    migrated = 0
    failed: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    for e in base.list_existing_evidence():
        meta, body = e["meta"], e["body"]
        if not meta.get("id"):
            failed.append({"id": e["rel"], "reason": "缺 id"})
            continue
        content = extract_content(meta, body)
        st = base.source_type_from_ev(meta.get("kind", ""))
        compilers = len(meta.get("matrix", {}).get("compiler", [])) or 1
        indep = 2 if st == "multi_blog" else 1
        grade, cred = base.grade_evidence_record(st, compilers=compilers, independent_sources=indep)
        try:
            if not dry_run:
                base.store_evidence(
                    content, source_type=st, grade=grade, credibility=cred,
                    acquired_at="legacy", acquisition_method="migration_644",
                    source_url=None, meta={"origin": e["rel"], "kind": meta.get("kind")})
            migrated += 1
            for card in (meta.get("serves") or []):
                links.append({"evidence_id": base.sha256_text(content),
                              "card_id": str(card), "relation": "support"})
        except Exception as exc:  # noqa: BLE001
            failed.append({"id": str(meta.get("id")), "reason": f"{type(exc).__name__}: {exc}"})
    return {"migrated": migrated, "failed": failed, "n_links": len(links),
            "total": len(base.list_existing_evidence()), "dry_run": dry_run}


def render_md(r: dict[str, Any]) -> str:
    lines = ["# 644 C4 · 证据库迁移报告", "",
             f"- 现有证据总量：**{r['total']}**",
             f"- 成功迁移：**{r['migrated']}**  失败：**{len(r['failed'])}**",
             f"- 建立关联：**{r['n_links']}**  （dry_run={r['dry_run']}）", "",
             "## 失败项", "", "| 证据 | 原因 |", "|---|---|"]
    for f in r["failed"]:
        lines.append(f"| {f['id']} | {f['reason']} |")
    if not r["failed"]:
        lines.append("| — | 无 |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    r = migrate_all(dry_run=True)
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(r))
    return OUT_MD


def selftest() -> int:
    # 纯函数 extract_content 稳定
    c1 = extract_content({"id": "E1", "kind": "run", "verdict": "confirm"}, "body text")
    c2 = extract_content({"id": "E1", "kind": "run", "verdict": "confirm"}, "body text")
    assert base.sha256_text(c1) == base.sha256_text(c2)
    # dry-run 不写 store：迁移前/后 store 条目数不变
    before = len(base.iter_stored())
    r = migrate_all(dry_run=True)
    after = len(base.iter_stored())
    assert before == after
    assert r["migrated"] == r["total"] and r["failed"] == []
    # 原文件未被修改：读取一个 evidence 文件，迁移后再读，内容一致
    evs = base.list_existing_evidence()
    p = evs[0]["path"]
    with open(p, encoding="utf-8") as fh:
        original = fh.read()
    migrate_all(dry_run=True)
    with open(p, encoding="utf-8") as fh:
        after_text = fh.read()
    assert original == after_text
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 C4 证据库迁移工具")
    ap.add_argument("--check", action="store_true", help="只读自检（默认，dry-run）")
    ap.add_argument("--migrate", action="store_true", help="真正写入 store")
    ap.add_argument("--report", action="store_true", help="写迁移报告（dry-run）")
    a = ap.parse_args(argv)
    if a.migrate:
        r = migrate_all(dry_run=False)
        print(f"migrated {r['migrated']}/{r['total']} (failed {len(r['failed'])})")
        return 0
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
