"""备份/恢复回归锁（508 任务7）。

提示词要求 2 个测试（snapshot 不崩溃 / restore 不崩溃）；本文件再加 2 个把两条安全纪律钉住：
①**恢复不删原件**（覆盖前留 .bak）；②`cleanup` **只删自己产的目录**（白名单制备份最怕
误删别人的东西）。所有测试 `monkeypatch backup.ROOT` 到 tmp，绝不碰真实仓库。
"""
from __future__ import annotations

import json
from pathlib import Path

import backup as bk


def _mk_repo(root: Path) -> None:
    """造一个只含白名单子集的假仓库（含 1 个故意缺失项）。"""
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(parents=True, exist_ok=True)
    (root / "Examples" / "atoms").mkdir(parents=True, exist_ok=True)
    (root / "data" / "metrics.jsonl").write_text('{"m":1}\n', encoding="utf-8")
    (root / "tools" / "golden_state.json").write_text('{"metrics":{"atoms_total":27}}',
                                                      encoding="utf-8")
    (root / "Examples" / "atoms" / "artifact_versions.json").write_text("{}", encoding="utf-8")


def test_snapshot_copies_whitelist_and_marks_skipped(tmp_path: Path,
                                                     monkeypatch):
    """① snapshot 正常产出：白名单存在的都拷了，不存在的记入 skipped（不报错）。"""
    monkeypatch.setattr(bk, "ROOT", tmp_path)
    _mk_repo(tmp_path)
    base = tmp_path / "backups"
    d = bk.snapshot(base, tag="2026-09-14-000000")
    man = json.loads((d / bk.MANIFEST).read_text(encoding="utf-8"))
    got = {f["path"] for f in man["files"]}
    assert got == {"data/metrics.jsonl", "tools/golden_state.json",
                   "Examples/atoms/artifact_versions.json"}
    assert "data/knowledge_graph.db" in man["skipped"]
    assert (d / "data" / "metrics.jsonl").read_text(encoding="utf-8") == '{"m":1}\n'
    assert all(len(f["sha256"]) == 64 for f in man["files"]), "每条须带 sha256"


def test_restore_recovers_content_and_keeps_bak(tmp_path: Path, monkeypatch):
    """② restore 正常恢复；**覆盖前把现有文件另存 .bak**（恢复动作本身可回退）。"""
    monkeypatch.setattr(bk, "ROOT", tmp_path)
    _mk_repo(tmp_path)
    base = tmp_path / "backups"
    bk.snapshot(base, tag="2026-09-14-000000")
    (tmp_path / "data" / "metrics.jsonl").write_text('{"m":999}\n', encoding="utf-8")
    res = bk.restore("2026-09-14-000000", base)
    assert "data/metrics.jsonl" in res["restored"]
    assert (tmp_path / "data" / "metrics.jsonl").read_text(encoding="utf-8") == '{"m":1}\n'
    bak = tmp_path / "data" / "metrics.jsonl.bak"
    assert bak.is_file(), "覆盖前必须留 .bak（不删原件）"
    assert "999" in bak.read_text(encoding="utf-8")
    assert res["missing_in_backup"] == [] or isinstance(res["missing_in_backup"], list)


def test_restore_refuses_dir_without_manifest(tmp_path: Path, monkeypatch):
    """③ 无 MANIFEST 的目录拒绝盲恢复（宁可不恢复，也不猜着覆盖）。"""
    monkeypatch.setattr(bk, "ROOT", tmp_path)
    base = tmp_path / "backups"
    (base / "2026-01-01-000000").mkdir(parents=True)
    try:
        bk.restore("2026-01-01-000000", base)
    except SystemExit as exc:
        assert "MANIFEST" in str(exc)
    else:
        raise AssertionError("无 manifest 时必须拒绝恢复")


def test_cleanup_keeps_recent_and_skips_foreign_dirs(tmp_path: Path, monkeypatch):
    """④ cleanup：保留最近 N 份；**非本工具产物不删**（只有 manifest 或日期名才动）。"""
    monkeypatch.setattr(bk, "ROOT", tmp_path)
    base = tmp_path / "backups"
    for i in range(12):
        d = base / f"2026-09-{i + 1:02d}-000000"
        d.mkdir(parents=True)
        (d / bk.MANIFEST).write_text('{"files":[]}', encoding="utf-8")
    foreign = base / "someone_elses_data"
    foreign.mkdir(parents=True)
    removed = bk.cleanup(keep=10, base=base)
    assert len(removed) == 2, removed
    assert foreign.is_dir(), "无 manifest 且非日期命名的目录不得被删"
    assert len([p for p in base.iterdir() if p.is_dir()]) == 11  # 10 份 + foreign
