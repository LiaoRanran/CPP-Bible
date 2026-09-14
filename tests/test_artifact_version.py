"""EV-ARTIFACT-VERSION-MATCH 回归锁（498 任务 2.3）。

语义（三级）：版本不一致 ⇒ **block**（真漂移）；缺卡字段 / 缺工件注解 ⇒ **warn**（迁移期）；
工件缺失 ⇒ **跳过**（由 replay 判 artifact_absent；同时防 replay 运行期的中间态误报）。
测试须把 `ge.ROOT` 一并指向 tmp_path——规则读 `ROOT / artifact`（否则会读真实仓库工件）。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    return tmp_path


def _asm(sb: Path, rel: str, ver: str | None) -> Path:
    p = sb / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    head = f"; artifact_version: {ver}\n" if ver else ""
    p.write_text(head + '\t.file\t"x.cpp"\n', encoding="utf-8")
    return p


def _card(sb: Path, cid: str, art: str | None, ver: str | None = None) -> Path:
    p = sb / "evidence" / f"{cid}.md"
    lines = [f"id: {cid}", "serves: []", "hypothesis: h", "kind: asm",
             "command: g++ -S x.cpp -o x.asm"]
    if art:
        lines.append(f"artifact: {art}")
    if ver is not None:
        lines.append(f"artifact_version: {ver}")
    lines += ["artifact_sha256: " + "0" * 64, "verdict: confirm", "falsification: f"]
    p.write_text("---\n" + "\n".join(lines) + "\n---\n", encoding="utf-8")
    return p


def test_version_mismatch_blocks(sb: Path):
    """卡 2 ≠ 工件 1 ⇒ block（真漂移，必须人处理）。"""
    _asm(sb, "Examples/atoms/a.asm", "1")
    _card(sb, "EV-T-V1", "Examples/atoms/a.asm", "2")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "block", hits
    assert hits[0].rule_id == "EV-ARTIFACT-VERSION-MATCH"


def test_version_match_passes(sb: Path):
    _asm(sb, "Examples/atoms/a.asm", "1")
    _card(sb, "EV-T-V2", "Examples/atoms/a.asm", "1")
    assert ge.check_artifact_version_match() == []


def test_missing_card_version_warns(sb: Path):
    """卡有 artifact 但缺 artifact_version ⇒ warn（迁移期不 block）。"""
    _asm(sb, "Examples/atoms/a.asm", "1")
    _card(sb, "EV-T-V3", "Examples/atoms/a.asm", None)
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits


def test_missing_asm_comment_warns(sb: Path):
    _asm(sb, "Examples/atoms/a.asm", None)
    _card(sb, "EV-T-V4", "Examples/atoms/a.asm", "1")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits


def test_missing_artifact_file_skips(sb: Path):
    """工件不存在 ⇒ 跳过（replay 判 artifact_absent；并防 replay 运行期中间态误报）。"""
    _card(sb, "EV-T-V5", "Examples/atoms/nope.asm", "1")
    assert ge.check_artifact_version_match() == []


def test_no_artifact_field_skipped(sb: Path):
    """纯 run_match 形态（无 artifact 字段）不受本规则约束。"""
    _card(sb, "EV-T-V6", None, None)
    assert ge.check_artifact_version_match() == []
