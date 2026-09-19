"""592 任务2 · 推翻事件通道初始化（空文件 + schema 校验 + fail-closed）。

573 设计了 CLI 与 schema，但 `data/overturned_events.jsonl` **从未被创建** ⇒ 通道不存在，
曲线里的 0 是"没有通道"而不是"没有推翻"（两者含义相反）。本文件锁三件事：
  * 通道**建得起来**（幂等、空文件合法）；
  * 写入**只接显式的人/异族动作**，且 human 须过 git 作者绑定；
  * 校验不过 ⇒ **拒绝写入且不落行**（连空文件都不建 —— 不做半个动作）。

系统**绝不自动产生推翻**：本文件没有任何"自动检测 ⇒ append"的路径，也不许以后加。
"""
from __future__ import annotations

import json
from pathlib import Path

import gate_engine as ge
import overturned_events as oe
import pytest

CARD = "ATOM-LANG-INLINE-001"       # 真实存在的卡（卡解析要落到文件；与 573 回归锁同卡）


@pytest.fixture(autouse=True)
def _git_author(monkeypatch: pytest.MonkeyPatch):
    """默认把"该卡最后一次提交作者"钉成 LiaoRanran，测试离线可复现。"""
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("LiaoRanran", "liao@example.com"))


def _valid(**over) -> dict:
    ev = {"target": f"{CARD}/prop-1", "card": CARD, "old_verdict": "confirm",
          "new_verdict": "refute:new_evidence", "by": "adversary:redteam-v1",
          "reason": "异族实测推翻"}
    ev.update(over)
    return ev


# ── 通道初始化（幂等 + 空文件合法）───────────────────────────────────────────────
def test_ensure_channel_creates_empty_file_and_is_idempotent(tmp_path: Path):
    p = tmp_path / "ev.jsonl"
    assert not p.exists(), "前置：文件不该存在"
    assert oe.ensure_channel(p) == p
    assert p.is_file() and p.read_bytes() == b"", "空文件 = 合法的'通道已就绪'状态"
    oe.ensure_channel(p)                     # 第二次不得报错、不得改写内容
    assert p.read_bytes() == b""
    assert oe.count(p) == 0


def test_missing_channel_is_distinguishable_from_empty_channel(tmp_path: Path):
    """关键口径：「没有通道」与「通道已建但零事件」必须可区分（同 573 的 0/None 之辨）。"""
    missing = tmp_path / "nope.jsonl"
    assert oe.read_events(missing) == [] and oe.count(missing) == 0
    assert oe.channel_state(missing)["initialized"] is False
    oe.ensure_channel(missing)
    st = oe.channel_state(missing)
    assert st["initialized"] is True and st["events"] == 0


# ── 写入路径 ────────────────────────────────────────────────────────────────────
def test_append_valid_event_writes_one_line(tmp_path: Path):
    p = tmp_path / "ev.jsonl"
    oe.ensure_channel(p)
    ev = oe.append(_valid(), p)
    assert oe.count(p) == 1
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1
    assert p.read_text(encoding="utf-8").endswith("\n"), "jsonl 契约：每行以换行结尾"
    back = json.loads(lines[0])
    assert back == ev
    assert back["ts"] and ev["ts"].count("T") == 1        # ts 自动补齐（ISO8601）
    assert back["card"] == CARD and back["by"] == "adversary:redteam-v1"


def test_append_defaults_card_to_target(tmp_path: Path):
    """`card` 缺省 ⇒ 取 `target`（把 target 当卡用）。

    注意 fail-closed 的边界：target 是**命题 id**（`<卡>/prop-1`）而没给 card 时，
    卡解析不到 ⇒ **拒绝写入**（573 的设计：要核签名必须能落到卡文件）。
    """
    p = tmp_path / "ev.jsonl"
    ev = oe.append(_valid(target=CARD, card=None), p)
    assert ev["card"] == ev["target"] == CARD
    with pytest.raises(ValueError, match="卡解析不到"):
        oe.append(_valid(card=None), p)          # target=<卡>/prop-1 无法落到卡文件


def test_append_human_signed_is_logged(tmp_path: Path):
    p = tmp_path / "ev.jsonl"
    ev = oe.append(_valid(by="human:LiaoRanran"), p)
    assert ev["by"] == "human:LiaoRanran" and oe.count(p) == 1


# ── fail-closed（拒绝写入且不落行）───────────────────────────────────────────────
def test_append_missing_field_refused_without_creating_file(tmp_path: Path):
    p = tmp_path / "ev.jsonl"
    bad = _valid()
    bad.pop("reason")
    with pytest.raises(ValueError, match="均不可为空"):
        oe.append(bad, p)
    assert not p.exists(), "校验不过时**连空文件都不许建**（不做半个动作）"


def test_append_impersonated_human_refused(tmp_path: Path):
    """冒名（不是该卡 git 作者）⇒ 拒绝写入，且**已有通道内容一字不动**。"""
    p = tmp_path / "ev.jsonl"
    oe.ensure_channel(p)
    oe.append(_valid(), p)
    before = p.read_bytes()
    with pytest.raises(ValueError, match="不是该卡最后一次 git 提交的作者"):
        oe.append(_valid(by="human:Attacker"), p)
    assert p.read_bytes() == before and oe.count(p) == 1


def test_append_git_unavailable_bad_by_bad_card_bad_ts_refused(tmp_path: Path, monkeypatch):
    p = tmp_path / "ev.jsonl"
    oe.ensure_channel(p)
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: None)
    with pytest.raises(ValueError, match="git 不可用"):
        oe.append(_valid(by="human:LiaoRanran"), p)
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("LiaoRanran", "x@y"))
    with pytest.raises(ValueError, match="human:|adversary:"):
        oe.append(_valid(by="bot:someone"), p)
    with pytest.raises(ValueError, match="卡解析不到"):
        oe.append(_valid(card="ATOM-NOT-EXIST", target="ATOM-NOT-EXIST/prop-1"), p)
    with pytest.raises(ValueError, match="ISO8601"):
        oe.append(_valid(ts="昨天下午"), p)
    assert oe.count(p) == 0, "所有失败路径都不得落行"


def test_corrupt_channel_line_fails_loud(tmp_path: Path):
    """坏行**不静默跳过**（事件流是审计证据）：ensure/read/count 一律显形 + 带行号。"""
    p = tmp_path / "ev.jsonl"
    p.write_text('{"ok": 1}\n{not json\n', encoding="utf-8")
    with pytest.raises(ValueError, match="第 2 行"):
        oe.ensure_channel(p)
    with pytest.raises(ValueError, match="第 2 行"):
        oe.count(p)


# ── 真实通道（只读校验；不写真实 data/）──────────────────────────────────────────
def test_real_channel_exists_and_valid():
    """592 任务2 验收：`data/overturned_events.jsonl` 存在、可幂等 ensure、每行合法 JSON。"""
    p = oe.DEFAULT_PATH
    assert p.is_file(), "通道文件必须存在（本任务创建）"
    oe.ensure_channel(p)                       # 存在 ⇒ 只校验、不写
    events = oe.read_events(p)
    assert oe.count(p) == len(events)
    assert all(isinstance(e, dict) for e in events)
    # 当前应为空通道（0 条）；若将来有人真写了推翻事件，这里只要求"计数自洽"
    assert oe.channel_state(p)["initialized"] is True
