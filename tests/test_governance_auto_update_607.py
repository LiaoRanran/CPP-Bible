"""607 任务 3 · `governance_doc_guard.auto_update()` 回归锁（增量机械登记）。

锁的是**四条行为契约**（不是"跑通就行"）：
  1. 发现扫描面里新出现的文档 ⇒ 追加（带 sha256/size），并被 `verify` 接受；
  2. **不删除**任何历史条目；
  3. 磁盘上消失的文档 ⇒ 标 `status: "missing"`，**保留**原 sha256；
  4. **绝不刷新既有条目的 hash** ⇒ 内容被改过时 `verify` 依旧报红（fail-closed，人审 `update --force` 才接受）。

全部在 `tmp_path` 假仓里跑：`monkeypatch` 把模块级 `ROOT/DOCS_ROOT/MANIFEST_PATH/SCAN_PATH`
指向假仓 ⇒ **不碰真实仓**（`iter_governed_docs()` 的默认扫描面是相对 `ROOT` 展开的，不注入就
会扫到真实仓的 `_arch_*` / `_auto/inbox` / `PM_*.md`，测试将不再隔离）。
"""
from __future__ import annotations

import json
from pathlib import Path

import governance_doc_guard as gd

ARCH = "References/architecture_架构演进"


def _fake_repo(tmp_path: Path, monkeypatch) -> tuple[Path, Path]:
    """建一个只有一份投喂词的假仓，并把模块级路径全部重定向过去。"""
    root = tmp_path / "repo"
    docs = root / ARCH
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "base.md").write_text("投喂词 1。\n", encoding="utf-8")
    monkeypatch.setattr(gd, "ROOT", root)
    monkeypatch.setattr(gd, "DOCS_ROOT", docs)
    monkeypatch.setattr(gd, "MANIFEST_PATH", root / "data" / "governance_docs_manifest.json")
    monkeypatch.setattr(gd, "SCAN_PATH", root / "data" / "governance_weakening_scan.json")
    return root, docs


def _files() -> dict[str, dict]:
    man = json.loads(gd.MANIFEST_PATH.read_text(encoding="utf-8"))
    return {f["path"]: f for f in man["files"]}


# ── 契约 1：发现并追加新文档（含 607 扩边后的三类新位置）─────────────────────
def test_auto_update_discovers_new_docs(tmp_path: Path, monkeypatch):
    root, _ = _fake_repo(tmp_path, monkeypatch)
    assert gd.update_manifest(force=True)[0] is True          # 基线：只登记 base.md
    assert set(_files()) == {f"{ARCH}/base.md"}

    (root / "_arch_v12").mkdir()
    (root / "_arch_v12" / "note.md").write_text("调研笔记。\n", encoding="utf-8")
    (root / "_auto" / "inbox").mkdir(parents=True)
    (root / "_auto" / "inbox" / "701.md").write_text("投喂词。\n", encoding="utf-8")
    (root / "PM_进度.md").write_text("PM 文档。\n", encoding="utf-8")

    stats, diffs = gd.auto_update()
    assert stats["wrote"] is True, stats
    assert stats["added"] == 3, stats
    assert stats["missing"] == 0 and stats["reappeared"] == 0, stats
    assert len(diffs) == 3 and all(d.startswith("新增：") for d in diffs), diffs

    files = _files()
    assert {"_arch_v12/note.md", "_auto/inbox/701.md", "PM_进度.md"} <= set(files)
    rec = files["_arch_v12/note.md"]
    assert len(rec["sha256"]) == 64 and rec["size"] > 0, rec
    assert "status" not in rec, "新条目不该带 missing 标记"
    assert gd.verify_self_hash()[0] is True, "写盘必须同步重算 self_hash"


# ── 契约 2 + 3：只标记、不删除；历史 hash 原样保留 ────────────────────────────
def test_auto_update_marks_missing_but_keeps_history(tmp_path: Path, monkeypatch):
    root, docs = _fake_repo(tmp_path, monkeypatch)
    gone = docs / "gone.md"
    gone.write_text("旧投喂词。\n", encoding="utf-8")
    assert gd.update_manifest(force=True)[0] is True
    before = _files()
    assert f"{ARCH}/gone.md" in before
    old_sha = before[f"{ARCH}/gone.md"]["sha256"]

    gone.unlink()                                             # 文档消失（不是内容变更）
    stats, diffs = gd.auto_update()
    assert stats["missing"] == 1 and stats["added"] == 0, stats
    assert stats["wrote"] is True, stats
    assert diffs == [f"标记 missing：{ARCH}/gone.md"], diffs

    after = _files()
    assert set(before) <= set(after), "既有条目一条都不许消失"
    rec = after[f"{ARCH}/gone.md"]
    assert rec["status"] == "missing", rec
    assert rec["sha256"] == old_sha, "历史 hash 必须保留（否则历史被抹平）"
    # 已经标记过的条目再跑一次不会重复计数（幂等）
    stats2, _ = gd.auto_update()
    assert stats2["missing"] == 0 and stats2["wrote"] is False, stats2


# ── 契约 1 + 收工门禁：auto-update 后 verify 必须 exit 0，且幂等不写盘 ─────────
def test_cli_auto_update_then_verify_exit0(tmp_path: Path, monkeypatch):
    root, _ = _fake_repo(tmp_path, monkeypatch)
    assert gd.update_manifest(force=True)[0] is True
    (root / "MATRIX_矩阵.md").write_text("矩阵。\n", encoding="utf-8")

    assert gd.main(["auto-update"]) == 0
    assert gd.main(["verify"]) == 0

    raw = gd.MANIFEST_PATH.read_bytes()
    assert gd.main(["auto-update"]) == 0                       # 无变更
    assert gd.MANIFEST_PATH.read_bytes() == raw, "无变更时不许写盘（幂等）"


# ── 契约 4：增量通道**绝不**刷新既有 hash ⇒ 内容变更仍然 fail-closed ───────────
def test_auto_update_never_refreshes_existing_hash(tmp_path: Path, monkeypatch):
    root, docs = _fake_repo(tmp_path, monkeypatch)
    assert gd.update_manifest(force=True)[0] is True
    (docs / "base.md").write_text("被改过的内容。\n", encoding="utf-8")   # 内容变更
    (root / "INDEX_台账.md").write_text("索引。\n", encoding="utf-8")     # 新增（触发写盘）

    stats, diffs = gd.auto_update()
    assert stats["added"] == 1 and stats["changed"] == 1 and stats["wrote"] is True, stats
    assert any("update --force" in d for d in diffs), diffs
    rec = _files()[f"{ARCH}/base.md"]
    assert rec["sha256"] != gd._sha256(docs / "base.md"), "增量通道不许顺手重签"
    assert gd.main(["verify"]) == 1, "内容变更仍须报红（fail-closed）"


def test_auto_update_reports_changed_even_without_write(tmp_path: Path, monkeypatch):
    """只有内容变更（无新增/无消失）⇒ 不写盘，但 `changed` 必须如实计数、`verify` 仍红。

    这是**已知语义边界**（如实记录，不是缺陷）：`auto-update` 的 exit 码表达的是
    "本次机械登记是否干净执行"，内容变更的判决权在 `verify` / 人审 `update --force`。
    """
    root, docs = _fake_repo(tmp_path, monkeypatch)
    assert gd.update_manifest(force=True)[0] is True
    (docs / "base.md").write_text("被改过的内容。\n", encoding="utf-8")
    stats, diffs = gd.auto_update()
    assert stats["changed"] == 1 and stats["added"] == 0 and stats["wrote"] is False, stats
    assert diffs == [], "不写盘时无登记动作（变更仍由 verify 报红）"
    assert gd.main(["verify"]) == 1
