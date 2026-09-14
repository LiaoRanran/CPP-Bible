"""EV-ARTIFACT-VERSION-MATCH 回归锁（498 任务 2.3，**台账方案**）。

语义（三级）：卡版本 ≠ 台账登记 ⇒ **block**（真漂移）；卡缺 `artifact_version` 或
台账未登记该工件 ⇒ **warn**（迁移期）；无 artifact 字段的卡（纯 run_match 形态）不适用。

⚠️ 版本号载体是**旁路台账** `Examples/atoms/artifact_versions.json`，**不改工件字节**：
`.asm` 的字节同时受两处硬契约约束——replay 的「删旧工件→重跑生成命令→比卡值 sha256」
与 writer_selfcheck `WC-01` 的「磁盘工件 sha256 == 卡值」。首版按 498 §2.1 给 .asm
插注释，实测 WC-01 全库 fail（56/56）；反向同步卡值则 replay 全库 refute:sha256_mismatch。
故测试 monkeypatch `ge._ARTIFACT_LEDGER` 指向 tmp，不碰真实台账与工件。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import gate_engine as ge


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(ge, "_ARTIFACT_LEDGER",
                        tmp_path / "Examples" / "atoms" / "artifact_versions.json")
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    return tmp_path


def _ledger(sb: Path, mapping: dict[str, int]) -> None:
    p = sb / "Examples" / "atoms" / "artifact_versions.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(mapping), encoding="utf-8")


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
    """卡 2 ≠ 台账 1 ⇒ block（真漂移，必须人处理）。"""
    _ledger(sb, {"Examples/atoms/a.asm": 1})
    _card(sb, "EV-T-V1", "Examples/atoms/a.asm", "2")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "block", hits
    assert hits[0].rule_id == "EV-ARTIFACT-VERSION-MATCH"


def test_version_match_passes(sb: Path):
    _ledger(sb, {"Examples/atoms/a.asm": 1})
    _card(sb, "EV-T-V2", "Examples/atoms/a.asm", "1")
    assert ge.check_artifact_version_match() == []


def test_missing_card_version_warns(sb: Path):
    """卡有 artifact 但缺 artifact_version ⇒ warn（迁移期不 block）。"""
    _ledger(sb, {"Examples/atoms/a.asm": 1})
    _card(sb, "EV-T-V3", "Examples/atoms/a.asm", None)
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits


def test_unregistered_artifact_warns(sb: Path):
    """台账缺该工件 ⇒ warn（提示跑迁移脚本），不得静默放行。"""
    _ledger(sb, {"Examples/atoms/other.asm": 1})
    _card(sb, "EV-T-V4", "Examples/atoms/a.asm", "1")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits


def test_missing_ledger_file_warns(sb: Path):
    """台账文件整体缺失（未跑迁移）⇒ 同样按「未登记」warn，不抛异常、不静默通过。"""
    _card(sb, "EV-T-V5", "Examples/atoms/a.asm", "1")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits


def test_no_artifact_field_skipped(sb: Path):
    """纯 run_match 形态（无 artifact 字段）不受本规则约束。"""
    _card(sb, "EV-T-V6", None, None)
    assert ge.check_artifact_version_match() == []


def test_corrupt_ledger_treated_as_unregistered(sb: Path):
    """台账损坏（非 JSON）⇒ 按未登记 warn（fail-loud 于规则层，而非抛栈）。"""
    p = sb / "Examples" / "atoms" / "artifact_versions.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{ 坏 json", encoding="utf-8")
    _card(sb, "EV-T-V7", "Examples/atoms/a.asm", "1")
    hits = ge.check_artifact_version_match()
    assert len(hits) == 1 and hits[0].severity == "warn", hits
