"""571 任务 4 回归锁：命题级 `signed_by` 最小骨架（schema + 与卡级同一套 git 作者绑定核查）。

只锁四件事：
  ① 命题级署名**合法**（实名 == 该文件 git 作者）⇒ 不报；
  ② 命题级**冒名**（名字与 git 作者不符）⇒ warn（与卡级同款观察期口径，warn 起步）；
  ③ **缺省**（不签）⇒ 不报，仍由卡级 `verified_by` 兜底；
  ④ **存量 79 命题不因新字段变红**（真实仓库跑一遍 = 0 条命题级命中）。
**不自动签任何命题**：本骨架只提供"能签 + 能校验 + 能查"，签署动作永远由人做。
"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge

BASE = """---
id: ATOM-TEST-001
domain: mem
title: t
type: atom
status: draft
claim: c
claim_boundary: b
claim_structured:
  - prop-id: prop-1
    claim_type: observation
    statement: s
%s
---
正文
"""


def _probe(monkeypatch, tmp_path: Path, block: str):
    p = tmp_path / "ATOM-TEST-001.md"
    p.write_text(BASE % block, encoding="utf-8")
    monkeypatch.setattr(ge, "ATOMS", tmp_path)
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("LiaoRanran", "liao@example.com"))
    return [f for f in ge.check_git_author_binding() if "ATOM-TEST-001" in str(f.target)]


def test_571_prop_signed_by_legal_passes(monkeypatch, tmp_path: Path):
    """命题级署名 = 该文件 git 作者 ⇒ 合法，不报。"""
    assert _probe(monkeypatch, tmp_path, "    signed_by: human:LiaoRanran") == []


def test_571_prop_signed_by_impersonation_warns(monkeypatch, tmp_path: Path):
    """冒名（不是该文件的 git 作者）⇒ warn（同卡级观察期口径），且文案点明是**命题级**。"""
    hits = _probe(monkeypatch, tmp_path, "    signed_by: human:Attacker")
    assert len(hits) == 1, hits
    assert hits[0].rule_id == "S1-GIT-AUTHOR-BINDING" and hits[0].severity == "warn"
    assert "命题级 signed_by" in hits[0].message and "Attacker" in hits[0].message
    assert "卡级" in hits[0].message            # 文案必须说清与卡级的关系（兜底语义）


def test_571_prop_signed_by_default_is_quiet(monkeypatch, tmp_path: Path):
    """缺省不签 ⇒ 不报（仍由卡级 verified_by 兜底；命题签名是**可选**字段）。"""
    assert _probe(monkeypatch, tmp_path, "") == []
    # 卡级签名仍走原路径：卡级冒名照旧 warn（命题级新逻辑不许把卡级判断弄丢）
    hits = _probe(monkeypatch, tmp_path,
                  "    signed_by: human:LiaoRanran\nverified_by: human:Attacker")
    assert len(hits) == 1 and "人级签收" in hits[0].message, hits


def test_571_stock_propositions_do_not_turn_red():
    """存量（79 命题，命题级署名 0 条）**不因新字段变红**：真实仓库跑一遍必须无命题级命中。"""
    msgs = [f.message for f in ge.check_git_author_binding()]
    assert not [m for m in msgs if "命题级 signed_by" in m], msgs
