"""644 C4 证据库迁移工具单测（M4-1..M4-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_migration_644 as c4


# M4-1：extract_content 稳定（同输入同 hash）
def test_extract_stable():
    c1 = c4.extract_content({"id": "E1", "kind": "run", "verdict": "confirm"}, "b")
    c2 = c4.extract_content({"id": "E1", "kind": "run", "verdict": "confirm"}, "b")
    assert base.sha256_text(c1) == base.sha256_text(c2)


# M4-2：dry-run 不写 store（迁移前后 store 条目数不变）
def test_dry_run_no_write():
    before = len(base.iter_stored())
    r = c4.migrate_all(dry_run=True)
    after = len(base.iter_stored())
    assert before == after
    assert r["migrated"] == r["total"]


# M4-3：原文件未被修改（迁移后内容一致）
def test_originals_unchanged():
    evs = base.list_existing_evidence()
    p = evs[0]["path"]
    with open(p, encoding="utf-8") as fh:
        original = fh.read()
    c4.migrate_all(dry_run=True)
    with open(p, encoding="utf-8") as fh:
        after = fh.read()
    assert original == after


# M4-4：selftest 通过
def test_selftest():
    assert c4.selftest() == 0
