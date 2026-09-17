"""ATOM-VERIFY-REASON 回归锁（494 任务 5 / 491 决策日志）。

语义：status ∈ {verified, human-verified} 的原子必须有非空 `verified_reason`——
人级签署只签名不写理由，决策不可回溯（491 §一：确认偏误/权威偏误的最大落点）。

两级语义须分清（勿混）：
* **名单豁免**（`tools/verify_reason_exempt.txt`）= 迁移期存量，缺字段**不报**（补一颗删一行）；
* **有 reason 或非人级状态** = 天然放行。
级别固定 warn（存量 23 颗全缺，block 会恒红；理由内容需人判断，铁律 4 不得逼人编造）。
"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import pytest

EXEMPT_ID = "ATOM-MEM-RVREF-001"          # 存量名单内的一颗（勿改成非名单 id）


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "atoms").mkdir()
    return tmp_path


def _atom(sb: Path, cid: str, status: str = "verified", extra: str = "") -> Path:
    p = sb / "atoms" / f"{cid}.md"
    p.write_text(f"---\nid: {cid}\nstatus: {status}\ntitle: t\ndomain: MEM\n"
                 "type: mechanism\nclaim: c\nclaim_boundary: b\nrelations: []\n"
                 "evidence: [EV-MEM-X]\nsources: [{kind: iso, ref: X, independent: true}]\n"
                 "first_hand: true\nsuperiority: 真实增量\ndepth: asm\npedagogy: p\n"
                 f"{extra}---\n", encoding="utf-8")
    return p


def test_missing_reason_warns_outside_exempt(sb: Path):
    """名单外的 verified 缺 reason → 命中，且级别 warn（不阻断）。"""
    _atom(sb, "ATOM-TEST-NOREASON")
    hits = ge.check_verify_reason()
    assert len(hits) == 1, hits
    assert hits[0].rule_id == "ATOM-VERIFY-REASON" and hits[0].severity == "warn"


def test_exempt_list_member_passes(sb: Path):
    """存量名单内的原子缺 reason → 放行（迁移期语义：补一颗删一行）。"""
    assert EXEMPT_ID in ge._verify_reason_exempt_ids(), "预置 id 必须真在名单里"
    _atom(sb, EXEMPT_ID)
    assert ge.check_verify_reason() == []


def test_reason_present_passes(sb: Path):
    """有 reason → 放行（无论是否在名单内）。"""
    _atom(sb, "ATOM-TEST-HASREASON",
          extra="verified_reason: 红队 R 报告 + replay confirm\n")
    assert ge.check_verify_reason() == []


def test_human_verified_also_covered(sb: Path):
    """human-verified（G6 现名）与 verified（历史别名）同受约束。"""
    _atom(sb, "ATOM-TEST-HUMAN", status="human-verified")
    hits = ge.check_verify_reason()
    assert len(hits) == 1 and hits[0].severity == "warn"


@pytest.mark.parametrize("status", ["draft", "red-team-verified"])
def test_non_human_status_not_covered(sb: Path, status: str):
    """非人级状态（draft / red-team-verified）不受本规则约束（人级才需要写理由）。"""
    _atom(sb, "ATOM-TEST-OTHER", status=status)
    assert ge.check_verify_reason() == []


def test_rule_registered_as_warn():
    r = next((x for x in ge.RULES if x.id == "ATOM-VERIFY-REASON"), None)
    assert r is not None and r.severity == "warn", r


def test_blank_reason_treated_as_missing(sb: Path):
    """空白 reason（纯空格）不算填写——否则"填个空格"即绕过。"""
    _atom(sb, "ATOM-TEST-BLANK", extra='verified_reason: "   "\n')
    assert len(ge.check_verify_reason()) == 1
