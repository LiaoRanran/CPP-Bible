"""601 任务 0.4 · 治理 manifest 自校验（`self_hash`）回归锁。

病（591 自承的信任边界）：manifest 是信任根的一部分，却**自身不在校验范围内** —— 谁改基准谁自签。
本文件锁：manifest 内容的 hash 写回自身；`verify`/`preflight` **先**校它，不符即
`manifest self-hash mismatch`。正直性提示：**这不是签名**（单用户阶段无密钥对，攻击者可同改两者），
它挡的是"改了内容忘了/不想改 hash 的单点篡改"，并与 `tool_integrity` 的 SUPPLY_CHAIN_FILES 形成两条独立检出路径。
"""
from __future__ import annotations

import json
from pathlib import Path

import governance_doc_guard as gd
import pytest


def _mk(tmp_path: Path, text: str = "正常内容。\n") -> tuple[Path, Path]:
    docs = tmp_path / "References" / "architecture_架构演进"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "x.md").write_text(text, encoding="utf-8")
    return docs, tmp_path / "data" / "manifest.json"


# ── 正例 ───────────────────────────────────────────────────────────────────────
def test_update_writes_self_hash_and_verify_passes(tmp_path: Path):
    docs, man = _mk(tmp_path)
    wrote, _ = gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert wrote
    m = json.loads(man.read_text(encoding="utf-8"))
    assert m[gd.SELF_HASH_KEY] == gd.compute_self_hash(m)
    assert gd.verify_self_hash(man) == (True, "")
    assert gd.verify_manifest(man, docs) == (True, [])


def test_real_manifest_has_valid_self_hash():
    """真库：manifest 必须有合法 self_hash 且文档逐条一致。"""
    ok, why = gd.verify_self_hash()
    assert ok, why
    assert gd.verify_manifest() == (True, [])


# ── 反例 ───────────────────────────────────────────────────────────────────────
def test_tamper_content_without_updating_hash_is_caught(tmp_path: Path):
    docs, man = _mk(tmp_path)
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    m = json.loads(man.read_text(encoding="utf-8"))
    m["files"][0]["sha256"] = "0" * 64            # 偷偷改内容（不动 self_hash）
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    ok, why = gd.verify_self_hash(man)
    assert ok is False and "self-hash mismatch" in why, why
    ok2, diffs = gd.verify_manifest(man, docs)
    assert ok2 is False and any("self-hash mismatch" in d for d in diffs), diffs


def test_tamper_self_hash_itself_is_caught(tmp_path: Path):
    docs, man = _mk(tmp_path)
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    m = json.loads(man.read_text(encoding="utf-8"))
    m[gd.SELF_HASH_KEY] = "f" * 64
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    ok, why = gd.verify_self_hash(man)
    assert ok is False and "self-hash mismatch" in why, why


def test_old_format_manifest_without_self_hash_is_refused(tmp_path: Path):
    docs, man = _mk(tmp_path)
    man.parent.mkdir(parents=True, exist_ok=True)
    man.write_text(json.dumps({"generated_at": "x", "git_commit": "y",
                               "files": [{"path": "a", "sha256": "b", "size": 1}]},
                              ensure_ascii=False), encoding="utf-8")
    ok, why = gd.verify_self_hash(man)
    assert ok is False and "self_hash" in why, why
    assert gd.verify_manifest(man, docs)[0] is False


def test_missing_or_broken_manifest_fails_loud(tmp_path: Path):
    assert gd.verify_self_hash(tmp_path / "nope.json")[0] is False
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    ok, why = gd.verify_self_hash(bad)
    assert ok is False and "JSON" in why, why


# ── 幂等 / CLI ─────────────────────────────────────────────────────────────────
def test_update_is_idempotent_apart_from_timestamps(tmp_path: Path):
    docs, man = _mk(tmp_path)
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    first = json.loads(man.read_text(encoding="utf-8"))
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    second = json.loads(man.read_text(encoding="utf-8"))
    assert first["files"] == second["files"], "连续 update 的文件清单必须逐字一致"
    assert second[gd.SELF_HASH_KEY] == gd.compute_self_hash(second)
    # `self_hash` 覆盖 generated_at/git_commit（它们是 manifest 内容的一部分）⇒ 时间戳一变 hash 必变；
    # 把时间戳归一后必须逐字相等 —— 这证明"除时间戳外"确实幂等。
    norm = dict(second, generated_at=first["generated_at"], git_commit=first["git_commit"])
    assert first[gd.SELF_HASH_KEY] == gd.compute_self_hash(norm)


def test_cli_verify_detects_tamper_and_exit_codes(tmp_path: Path, monkeypatch, capsys):
    docs, man = _mk(tmp_path)
    scan = tmp_path / "data" / "scan.json"
    monkeypatch.setattr(gd, "DOCS_ROOT", docs)
    monkeypatch.setattr(gd, "MANIFEST_PATH", man)
    monkeypatch.setattr(gd, "SCAN_PATH", scan)
    gd.update_manifest(force=True)
    assert gd.main(["verify"]) == 0
    m = json.loads(man.read_text(encoding="utf-8"))
    m["files"].append({"path": "假文档.md", "sha256": "0" * 64, "size": 1})
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    assert gd.main(["verify"]) == 1
    err = capsys.readouterr().err
    assert "self-hash mismatch" in err, err
    # 重签后 ⇒ 绿（把上面那条假文档真写进磁盘才算一致）
    (docs / "假文档.md").write_text("内容\n", encoding="utf-8")
    gd.update_manifest(force=True)
    assert gd.main(["verify"]) == 0


def test_update_diffs_report_document_changes_not_self_hash(tmp_path: Path):
    """update 的"变更 N 处"必须数**文档**差异，不能被自校验信息冲掉。"""
    docs, man = _mk(tmp_path)
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    (docs / "y.md").write_text("新文档\n", encoding="utf-8")
    wrote, diffs = gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert wrote and len(diffs) == 1 and "y.md" in diffs[0], diffs


def test_self_hash_not_counted_in_content_digest():
    """`compute_self_hash` 必须**排除** self_hash 字段本身（否则递归无解）。"""
    base = {"generated_at": "t", "git_commit": "c", "files": []}
    with_hash = dict(base, **{gd.SELF_HASH_KEY: "whatever"})
    assert gd.compute_self_hash(base) == gd.compute_self_hash(with_hash)


@pytest.mark.parametrize("cmd", ["verify", "preflight"])
def test_self_hash_gate_runs_before_doc_comparison(tmp_path: Path, monkeypatch, cmd):
    """自校验是**第一道**：manifest 被改而 hash 未同步 ⇒ 无论文档是否一致都必须红。"""
    docs, man = _mk(tmp_path)
    monkeypatch.setattr(gd, "DOCS_ROOT", docs)
    monkeypatch.setattr(gd, "MANIFEST_PATH", man)
    monkeypatch.setattr(gd, "SCAN_PATH", tmp_path / "scan.json")
    gd.update_manifest(force=True)
    m = json.loads(man.read_text(encoding="utf-8"))
    m["files"][0]["sha256"] = "0" * 64
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    # 文档本身没动（如果只看文档差异会判绿）——自校验必须拦下
    assert gd.main([cmd]) == 1
