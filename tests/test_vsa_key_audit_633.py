# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""633 C1 · vsa_key_audit 单测（纯标准库，≥5 例）。编号 C1-1..C1-6。"""
from __future__ import annotations

import os

import pytest

import tools.vsa_key_audit_633 as m

#: 674a：`data/vsa/` 是**运行时凭证目录**（`.gitignore` 第 113-114 行排除密钥及其备份/变体）
#: ⇒ 干净检出与 CI 上**根本没有密钥文件**，依赖它的 3 例必然红。这不是代码缺陷，而是
#: "密钥绝不入库"这一设计的**必然后果**（633 C1 的意图正是如此）。
#: 故这三例只在**有密钥**的环境真跑；其余环境显式跳过并写清原因（不改成"缺密钥也绿"——
#: 那会把"密钥没被提交"这件事本身变成不可见）。
_KEY_PRESENT = os.path.exists(m.KEY)
_NO_KEY = pytest.mark.skipif(
    not _KEY_PRESENT,
    reason="674a：data/vsa/ 为运行时凭证目录（密钥与备份均被 .gitignore 排除）⇒ 干净检出/CI 无密钥；"
           "本用例只在开发者本机（已生成密钥）真跑。密钥不入库是设计红线，不为此改断言。",
)


# C1-1：密钥存在 + sha256 前缀稳定（相同文件两次一致）
@_NO_KEY
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
@_NO_KEY
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
@_NO_KEY
def test_selftest_passes():
    assert m.selftest() == 0
