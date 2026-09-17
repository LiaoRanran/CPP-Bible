"""472 P0-4（452 E13/N4）回归锁：工件快照落盘 + 幂等还原 + 无残留。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as replay  # noqa: E402


def test_snapshot_and_restore_idempotent(tmp_path: Path):
    """工件被删（进程被杀）后，快照必须能还原出原字节。"""
    art = tmp_path / "a.asm"
    art.write_text("ORIGINAL-BYTES", encoding="utf-8")
    bak = replay._snapshot_artifact(art)
    assert bak and bak.is_file()
    art.unlink()                                    # 模拟中断
    assert replay._restore_artifact(art, bak)
    assert art.read_text(encoding="utf-8") == "ORIGINAL-BYTES"


def test_restore_is_idempotent_not_overwriting(tmp_path: Path):
    """阴性：工件正常时还原不得覆盖（幂等，不是强制回滚）。"""
    art = tmp_path / "b.asm"
    art.write_text("ORIGINAL", encoding="utf-8")
    bak = replay._snapshot_artifact(art)
    art.write_text("NEW-VALID", encoding="utf-8")    # 正常生成的新工件
    assert not replay._restore_artifact(art, bak)    # 不应动手
    assert art.read_text(encoding="utf-8") == "NEW-VALID"


def test_empty_artifact_gets_restored(tmp_path: Path):
    """工件被清空（E13 实测形态）→ 必须从备份重建。"""
    art = tmp_path / "c.asm"
    art.write_text("ORIGINAL", encoding="utf-8")
    bak = replay._snapshot_artifact(art)
    art.write_text("", encoding="utf-8")             # 模拟被清空
    assert replay._restore_artifact(art, bak)
    assert art.read_text(encoding="utf-8") == "ORIGINAL"


def test_no_bak_residue_after_drop(tmp_path: Path):
    """正常路径结束不得留下 .bak（否则仓库污染 / 下次误恢复）。"""
    art = tmp_path / "d.asm"
    art.write_text("X", encoding="utf-8")
    bak = replay._snapshot_artifact(art)
    replay._drop_snapshot(bak)
    assert not bak.exists()
    assert not list(tmp_path.glob("*.bak"))


def test_missing_source_no_snapshot(tmp_path: Path):
    """工件原本不存在（新卡首跑）→ 无快照、还原无操作（不凭空造文件）。"""
    art = tmp_path / "e.asm"
    assert replay._snapshot_artifact(art) is None
    assert not replay._restore_artifact(art, None)
    assert not art.exists()
