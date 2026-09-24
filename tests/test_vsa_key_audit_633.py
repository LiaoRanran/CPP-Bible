"""633 C1 · vsa_key_audit 单测（纯标准库，≥5 例）。编号 C1-1..C1-6。"""
from __future__ import annotations

import os

import tools.vsa_key_audit_633 as m


# C1-1：密钥存在 + sha256 前缀稳定（相同文件两次一致）
def test_key_exists_and_hash_stable():
    assert os.path.exists(m.KEY)
    assert m.sha256_head(m.KEY) == m.sha256_head(m.KEY)
    assert len(m.sha256_head(m.KEY)) == 12


# C1-2：不存在的文件 sha 为空
def test_missing_file_hash_empty():
    assert m.sha256_head(os.path.join(m.ROOT, "__no_such_key__")) == ""


# C1-3：默认不轮换（force=False）
def test_default_no_rotate():
    r = m.rotate(force=False)
    assert r["rotated"] is False and "默认不轮换" in r["reason"]


# C1-4：备份评估结构（dry 只读）
def test_backup_assessment_structure():
    b = m.backup(dry=True)
    assert set(b) >= {"ok", "backup", "consistent"}


# C1-5：引用扫描非空 + gitignore 覆盖必需模式
def test_refs_and_gitignore():
    assert len(m.find_references()) >= 1
    g = m.gitignore_coverage()
    assert set(g) >= {"patterns", "covered"}
    assert set(g["patterns"]) == set(m.REQUIRED_IGNORES)


# C1-6：--check 自检通过
def test_selftest_passes():
    assert m.selftest() == 0
