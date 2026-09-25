"""640 B3 · auto_executor 安全审计（攻击用例 + 六重护栏触发验证，≥8 例）。"""
from __future__ import annotations

import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
_SPEC = importlib.util.spec_from_file_location(
    "auto_executor_640", os.path.join(ROOT, "tools", "auto_executor_640.py"))
AX = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(AX)  # type: ignore[union-attr]


# ── 护栏①：白名单 ────────────────────────────────────────────────────────────
def test_attack_non_whitelist_category_rejected():
    r = AX.execute([{"category": "gate_rule_edit", "path": "data/x.md"},
                    {"category": "ledger_edit", "path": "data/authority/y.jsonl"},
                    {"category": "human_signoff", "path": "atoms/a.md"}],
                   apply=True)
    assert r["n_rejected"] == 3 and r["n_applied"] == 0
    assert all("不在白名单" in x["detail"] for x in r["results"])


def test_attack_protected_paths_rejected():
    protected = ["tools/gate_engine.py", "tools/weighted_af_solver.py",
                 "data/authority/decision_event_v2_ledger.jsonl",
                 "data/transparency_log.jsonl",
                 "atoms/mem/ATOM-MEM-LEAK-001.md",
                 "evidence/conc/EV-CONC-001.md"]
    r = AX.execute([{"category": "trailing_ws", "path": p} for p in protected],
                   apply=True)
    assert r["n_rejected"] == len(protected) and r["n_applied"] == 0


# ── 护栏⑤：批量上限 ─────────────────────────────────────────────────────────
def test_batch_over_limit_truncated():
    actions = [{"category": "trailing_ws", "path": f"data/fake_{i}.md"}
               for i in range(15)]
    r = AX.execute(actions, apply=False, max_n=10)
    assert r["n_plan"] == 15 and r["n_truncated"] == 5
    assert len(r["results"]) <= 10


# ── 护栏②③④：备份 / 验证 / 回滚 ────────────────────────────────────────────
def test_apply_then_verify_pass(tmp_path, monkeypatch):
    monkeypatch.setattr(AX, "LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(AX, "BACKUP_ROOT", str(tmp_path / "bak"))
    f = tmp_path / "t.md"
    f.write_bytes(b"a\x00b  \nc")
    # 一次含 3 类的 action 只会按单类别处理 ⇒ 分三个 action 依次验
    r1 = AX.execute([{"category": "control_chars", "path": str(f)}], apply=True)
    assert r1["n_applied"] == 1 and b"\x00" not in f.read_bytes()
    r2 = AX.execute([{"category": "trailing_ws", "path": str(f)}], apply=True)
    assert r2["n_applied"] == 1
    r3 = AX.execute([{"category": "final_newline", "path": str(f)}], apply=True)
    assert r3["n_applied"] == 1 and f.read_bytes().endswith(b"\n")


def test_verify_failure_triggers_rollback(tmp_path, monkeypatch):
    monkeypatch.setattr(AX, "LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(AX, "BACKUP_ROOT", str(tmp_path / "bak"))
    f = tmp_path / "t.md"
    f.write_bytes(b"hello\x00")
    monkeypatch.setattr(AX, "_verify", lambda a: False)   # 强制验证失败
    r = AX.execute([{"category": "control_chars", "path": str(f)}], apply=True)
    assert r["n_rolled_back"] == 1
    assert f.read_bytes() == b"hello\x00", "回滚后必须与改前字节一致"


def test_rollback_restores_exact_bytes(tmp_path, monkeypatch):
    monkeypatch.setattr(AX, "LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(AX, "BACKUP_ROOT", str(tmp_path / "bak"))
    f = tmp_path / "t.md"
    original = b"line1  \nline2\x07\n"
    f.write_bytes(original)
    monkeypatch.setattr(AX, "_verify", lambda a: False)
    AX.execute([{"category": "trailing_ws", "path": str(f)}], apply=True)
    assert f.read_bytes() == original


# ── dry-run 零改动 ───────────────────────────────────────────────────────────
def test_dry_run_makes_no_changes(tmp_path, monkeypatch):
    monkeypatch.setattr(AX, "LOG_PATH", str(tmp_path / "log.jsonl"))
    f = tmp_path / "t.md"
    f.write_bytes(b"hello\x00  \n")
    r = AX.execute([{"category": "control_chars", "path": str(f)},
                    {"category": "trailing_ws", "path": str(f)}], apply=False)
    assert all(x["status"] == "would-apply" for x in r["results"])
    assert f.read_bytes() == b"hello\x00  \n", "dry-run 不得改文件"


# ── 护栏⑥：日志 ─────────────────────────────────────────────────────────────
def test_every_action_logged(tmp_path, monkeypatch):
    monkeypatch.setattr(AX, "LOG_PATH", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(AX, "BACKUP_ROOT", str(tmp_path / "bak"))
    f = tmp_path / "t.md"
    f.write_bytes(b"x  \n")
    AX.execute([{"category": "trailing_ws", "path": str(f)},
                {"category": "push", "path": "origin"}], apply=True)
    log = [json.loads(ln) for ln in open(tmp_path / "log.jsonl", encoding="utf-8")
           if ln.strip()]
    assert len(log) == 2
    assert {e["status"] for e in log} == {"applied", "rejected"}
    assert all("ts" in e for e in log)


# ── B2：夹具试运行 ≥3 项 ─────────────────────────────────────────────────────
def test_fixture_trial_applies_at_least_three():
    r = AX.fixture_trial()
    assert r["n_applied"] >= 3
    assert r["n_rejected"] >= 2          # 非白名单 + 保护路径都被拒
    assert all(r["fixture_file_states"].values())
