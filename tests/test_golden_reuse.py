"""568 任务 2 回归锁：golden 复用 replay 增量结论必须是 **fail-closed**。

背景：`golden_lock.measure()` 过去逐卡直调 `replay.replay_card()`，把 replay 刚做过的真编译
整权重放（560 实测 replay 126.9s + golden 131s）。现在把"该跑 / 该复用"的判定**原样交给**
replay 自己的纯函数 `select_incremental`（不自造规则）。

本组锁死四种"拿不准 ⇒ 必须真编译"：无记录 / 指纹变了 / 上次非 confirm / 指纹 MISSING；
只有"指纹一致 **且** 上次 verdict == confirm"才复用；`--no-reuse` 时全量真编译。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay   # noqa: E402
import golden_lock as gl                # noqa: E402

CARD = ROOT / "evidence" / "conc" / "EV-CONC-001.md"


@pytest.fixture(autouse=True)
def _restore_flag():
    yield
    gl.REUSE_REPLAY_MANIFEST = True     # 全局开关必须还原，免得污染同进程的其他用例


def _entry(card: Path, verdict: str) -> dict:
    return {replay._manifest_key(card): {"fingerprint": replay.card_fingerprint(card),
                                         "verdict": verdict}}


def test_568_reuse_only_when_fingerprint_matches_and_confirm(monkeypatch):
    monkeypatch.setattr(replay, "load_manifest", lambda: _entry(CARD, "confirm"))
    run, skip = gl._select_replay([CARD], replay)
    assert run == [] and skip == [CARD]


def test_568_non_confirm_entry_forces_recompile(monkeypatch):
    monkeypatch.setattr(replay, "load_manifest",
                        lambda: _entry(CARD, "refute:compile_error"))
    assert gl._select_replay([CARD], replay) == ([CARD], [])


def test_568_stale_fingerprint_forces_recompile(monkeypatch):
    """输入变了（指纹对不上）⇒ 真编译：绝不把过期结论当新基线。"""
    monkeypatch.setattr(replay, "load_manifest",
                        lambda: {replay._manifest_key(CARD): {"fingerprint": "deadbeef",
                                                              "verdict": "confirm"}})
    assert gl._select_replay([CARD], replay) == ([CARD], [])


def test_568_missing_or_corrupt_manifest_forces_recompile(monkeypatch, tmp_path):
    monkeypatch.setattr(replay, "load_manifest", lambda: {})           # 文件不在 ⇒ {}
    assert gl._select_replay([CARD], replay) == ([CARD], [])
    bad = tmp_path / "replay_manifest.json"
    bad.write_text("{坏 JSON", encoding="utf-8")
    monkeypatch.setattr(replay, "MANIFEST", bad)
    assert replay.load_manifest() == {}      # 真实读法：损坏 ⇒ {}（宁可多跑不可漏跑）
    assert gl._select_replay([CARD], replay) == ([CARD], [])


def test_568_missing_fingerprint_never_reuses(monkeypatch):
    """指纹 MISSING（夹具/工件读不到）⇒ 强制重跑，不许沿用旧结论。"""
    monkeypatch.setattr(replay, "load_manifest",
                        lambda: {replay._manifest_key(CARD): {"fingerprint": "MISSING",
                                                              "verdict": "confirm"}})
    assert gl._select_replay([CARD], replay) == ([CARD], [])
    monkeypatch.setattr(replay, "card_fingerprint", lambda _c: "MISSING")   # 真·读不到
    monkeypatch.setattr(replay, "load_manifest", lambda: _entry(CARD, "confirm"))
    assert gl._select_replay([CARD], replay) == ([CARD], [])


def test_568_no_reuse_flag_forces_full_recompile(monkeypatch):
    monkeypatch.setattr(replay, "load_manifest", lambda: _entry(CARD, "confirm"))
    gl.REUSE_REPLAY_MANIFEST = False
    assert gl._select_replay([CARD], replay) == ([CARD], [])
