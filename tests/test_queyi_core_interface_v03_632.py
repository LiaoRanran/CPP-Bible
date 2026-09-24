"""632 F1 · Core 接口 v0.3 单测（纯标准库，≥5 例）。

聚焦 `queyi_core_interface_v03_632`：Evidence 接口的真实适配（EvidenceAdapter）。
编号 F1-1..F1-6。
"""
from __future__ import annotations

import os

import tools.queyi_core_interface_v02_631 as v02
import tools.queyi_core_interface_v03_632 as m


def _make_card(card_path: str, artifact_path: str, sha: str) -> None:
    os.makedirs(os.path.dirname(card_path), exist_ok=True)
    with open(artifact_path, "wb") as fh:
        fh.write(b"payload")
    real = m._sha256_file(artifact_path)
    declared = sha if sha else real
    with open(card_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            f"---\nid: EV-Demo-001\nartifact: {artifact_path}\n"
            f"artifact_sha256: {declared}\ncommand: echo hi\nfixture: x\n"
            "artifact_assert:\n - {kind: exists, text: \"main\"}\n---\nbody\n")


# F1-1：adapter.id() 返回真实 id
def test_adapter_id(tmp_path):
    art = str(tmp_path / "a.out")
    card = str(tmp_path / "EV-Demo-001.md")
    _make_card(card, art, "")
    assert m.EvidenceAdapter(card).id() == "EV-Demo-001"


# F1-2：verify_hash 匹配时 True
def test_verify_hash_match(tmp_path):
    art = str(tmp_path / "a.out")
    card = str(tmp_path / "EV-Demo-001.md")
    _make_card(card, art, "")
    assert m.EvidenceAdapter(card).verify_hash() is True


# F1-3：verify_hash 不匹配时 False
def test_verify_hash_mismatch(tmp_path):
    art = str(tmp_path / "a.out")
    card = str(tmp_path / "EV-Demo-001.md")
    _make_card(card, art, "0" * 64)
    assert m.EvidenceAdapter(card).verify_hash() is False


# F1-4：artifact_assert 解析出块值
def test_artifact_assert_block(tmp_path):
    art = str(tmp_path / "a.out")
    card = str(tmp_path / "EV-Demo-001.md")
    _make_card(card, art, "")
    aa = m.EvidenceAdapter(card).artifact_assert()
    assert len(aa) == 1 and aa[0].get("kind") == "exists"


# F1-5：replay 返回三态 dict（委托真实复算或 infra 兜底）
def test_replay_returns_three_state(tmp_path):
    art = str(tmp_path / "a.out")
    card = str(tmp_path / "EV-Demo-001.md")
    _make_card(card, art, "")
    res = m.EvidenceAdapter(card).replay()
    assert isinstance(res, dict)
    assert res.get("status") in ("confirm", "refute", "infra")


# F1-6：v0.2 抽象契约未被破坏 + --check 自检通过
def test_v02_contract_and_selftest():
    # v0.2 Evidence 抽象方法仍 raise NotImplementedError
    assert m._raises(v02.Evidence, "verify_hash")
    # v0.3 --check 通过
    assert m.selftest() == 0
