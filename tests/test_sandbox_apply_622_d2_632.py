"""632 [D2] L2 沙箱强制还原的单测。

聚焦新增的 `_git_checkout` 兜底逻辑：字节级还原失败时，仅对**被变异的那一张卡**
`git checkout -- <card>` 还原（最小爆炸半径，不 `git checkout -- atoms` 误伤合法未提交改动），
还原后再 sha256 复验，仍不符则判 `restore_failed`。

铁律：纯标准库 + 至少 5 例。编号 D2-1..D2-6。
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess

import pytest

import tools.sandbox_apply_622 as m

HAS_GIT = shutil.which("git") is not None


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _make_card_text() -> str:
    # 含 id / status frontmatter，足以让 M1 删除 id 字段生效
    return "---\nid: ATOM-X-001\nstatus: verified\n---\n\nbody\n"


def _mutation() -> dict:
    return {
        "mutation_id": "M1",
        "content": json.dumps({"op": "M1", "target_rule": "ATOM-FM-REQUIRED"}),
    }


# ── D2-1：git checkout 命中单卡命令（最小爆炸半径）────────────────────────────
def test_git_checkout_targets_single_card(monkeypatch):
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = list(cmd)
        captured["cwd"] = kw.get("cwd")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    sb = m.Sandbox(root="/tmp/root", lock_path="/tmp/root/.lock")
    sb._git_checkout("atoms/x/ATOM-X-001.md")
    assert captured["cmd"] == ["git", "checkout", "--", "atoms/x/ATOM-X-001.md"], \
        "L2 必须只 checkout 单卡，而非整个 atoms 目录"
    assert captured["cwd"] == "/tmp/root"


# ── D2-2：路径归一（./ 与反斜杠不作为爆炸半径放大的来源）─────────────────────
def test_git_checkout_uses_normed_path(monkeypatch):
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = list(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    sb = m.Sandbox(root="R", lock_path="R/.lock")
    sb._git_checkout(".\\atoms\\x\\ATOM-X-001.md")
    assert captured["cmd"] == ["git", "checkout", "--", "atoms/x/ATOM-X-001.md"]


# ── D2-3：字节级还原成功时，L2 不被触发（git 调用 0 次）──────────────────────
def test_apply_and_run_skips_git_when_byte_restore_ok(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kw):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)

    card = "atoms/ATOM-X-001.md"
    p = tmp_path / card
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_make_card_text().encode("utf-8"))

    sb = m.Sandbox(root=str(tmp_path), lock_path=str(tmp_path / ".lock"))
    sb.run_gate = lambda card_rel, **k: {"findings": [], "status": "ok"}

    res = sb.apply_and_run(_mutation(), card)
    assert res["verdict"] == "neutral"
    assert calls == [], "字节还原成功时不应调用 git checkout"


# ── D2-4：字节还原失败 → git checkout 兜底还原成功（需真实 git）──────────────
@pytest.mark.skipif(not HAS_GIT, reason="需要一个可执行的 git 以验证 L2 兜底")
def test_apply_and_run_l2_fallback_restores_from_git(monkeypatch, tmp_path):
    # 建一个孤立的临时 git 仓库，提交原始卡
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    card = "atoms/ATOM-X-001.md"
    p = tmp_path / card
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_make_card_text().encode("utf-8"))
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)

    sb = m.Sandbox(root=str(tmp_path), lock_path=str(tmp_path / ".lock"))
    sb.run_gate = lambda card_rel, **k: {"findings": [], "status": "ok"}
    # 强制字节级还原失败，逼出 L2 git checkout
    sb.restore = lambda card_rel, backup: {"restored": False, "reason": "sim"}

    res = sb.apply_and_run(_mutation(), card)
    assert res["verdict"] == "neutral", res
    # 还原后文件应等于 git 提交的原始内容
    assert p.read_text(encoding="utf-8") == _make_card_text()


# ── D2-5：字节还原失败 且 git 也失败 → 判 restore_failed（fail-closed）────────
def test_apply_and_run_restore_failed_when_git_also_fails(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, **kw):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 0, "", "")  # 假装成功但啥也没做

    monkeypatch.setattr(subprocess, "run", fake_run)

    card = "atoms/ATOM-X-001.md"
    p = tmp_path / card
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_make_card_text().encode("utf-8"))

    sb = m.Sandbox(root=str(tmp_path), lock_path=str(tmp_path / ".lock"))
    sb.run_gate = lambda card_rel, **k: {"findings": [], "status": "ok"}
    sb.restore = lambda card_rel, backup: {"restored": False, "reason": "sim"}

    res = sb.apply_and_run(_mutation(), card)
    assert res["verdict"] == "infra_error"
    assert "restore_failed" in res["reason"]
    assert any(c[:3] == ["git", "checkout", "--"] for c in calls), \
        "失败路径仍应尝试 L2 git checkout"


# ── D2-6：还原后 sha256 复验口径与原始备份一致（正常路径可复算）──────────────
def test_backup_sha256_roundtrip(monkeypatch, tmp_path):
    card = "atoms/ATOM-X-001.md"
    p = tmp_path / card
    p.parent.mkdir(parents=True, exist_ok=True)
    original = _make_card_text()
    p.write_bytes(original.encode("utf-8"))

    sb = m.Sandbox(root=str(tmp_path), lock_path=str(tmp_path / ".lock"))
    sb.run_gate = lambda card_rel, **k: {"findings": [], "status": "ok"}

    bak = sb.apply_mutation(_mutation(), card)
    assert bak["applied"] is True
    assert bak["backup_sha256"] == _sha(original.encode("utf-8"))
    rest = sb.restore(card, bak)
    assert rest["restored"] is True
    assert rest["sha256"] == bak["backup_sha256"]
