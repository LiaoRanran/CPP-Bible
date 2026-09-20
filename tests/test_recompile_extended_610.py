"""610 E3 · 编译可复现性加严检查回归锁（跨时间窗口 + 符号表 + 段 + 字符串表）。

**CORE 改动纪律**：本批只**追加** `_recompile_invariant_extended` 与两个辅助函数，
`_recompile_invariant` 与 replay 的 confirm/refute 判决语义**一行未动**（第 4 例专门锁这点）。

锁四件事（任务书 E3 的 4 例）：
  1. 可复现的卡（`.asm` 工件）：扩展检查 `status=ok`、`sha_match=True`、`strings` 一致，
     **`nm`/`objdump` 因工件是汇编文本 ⇒ 如实标 `skipped`**（不算失败也不算通过）；
  2. **跨时间窗口**：`gap_seconds ≥ 1.1`（真跨秒），并对 PE exe 抓到**时间窗口漂移**；
  3. 工具不可用（monkeypatch `shutil.which` ⇒ None）：`nm`/`objdump`/`strings` 三个字段全 `skipped`；
  4. **向后兼容**：`_recompile_invariant` 行为不变（sha 一致 ⇒ ok；给错卡值 ⇒ tampered）。

⚠️ 全部标 `slow`（要真调 g++ 编译）：fast 门禁不受影响，本文件需显式跑。
实测（2026-09-20，MinGW g++ 15.3.0）：
  * EV-CONC-001 的 `.asm`：跨 1.1s 两次独立编译 sha 一致（`8dd19bc6…`）；
  * 同卡的 PE exe：跨 1.1s sha **不同**，但只差 **2 字节**（偏移 0x88 与 0xd8，PE 头
    `TimeDateStamp` + debug 目录同族字段），且 `nm`/`objdump`/`strings` **全一致**；
    加 `-Wl,--no-insert-timestamp` 后跨窗口**字节一致** ⇒ 判 `time_window_drift`（取证而非猜测）。
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as aer  # noqa: E402

# 全部标 slow（要真调 g++ 编译）：fast 门禁不受影响，本文件需显式跑。
# CI 上跳过：依赖本地 MinGW 编译的 .asm 工件 sha，CI Ubuntu g++ 重编译产物必然不同。
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(
        os.environ.get("CI") == "true",
        reason="依赖本地 MinGW 编译环境（.asm 工件 sha），CI Ubuntu g++ 产物 sha 必然不同",
    ),
]

CARD = aer.run_root() / "evidence" / "conc" / "EV-CONC-001.md"
ASM_REL = "Examples/atoms/_atom_fence_vs_atomic.asm"


def _card() -> dict:
    return aer.parse_frontmatter(CARD.read_text(encoding="utf-8", errors="replace"))


def _gpp() -> str:
    env = aer._compiler_env()
    return shutil.which("g++", path=env.get("PATH")) or "g++"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_recompile_invariant_extended_reproducible():
    meta = _card()
    res = aer._recompile_invariant_extended(str(meta["command"]), ASM_REL, gap_s=1.1)
    assert res["status"] == "ok", res["details"]
    assert res["sha_match"] is True and res["within_match"] is True
    assert res["strings_match"] is True
    # 汇编文本工件：nm/objdump 不适用 ⇒ 必须如实标 skipped（不许伪造成 True）
    assert res["nm_match"] == "skipped" and res["objdump_match"] == "skipped"
    assert res["cross_time"]["gap_seconds"] == 1.1
    assert str(meta["artifact"]) == ASM_REL


def test_cross_time_window(tmp_path: Path, monkeypatch):
    """真跨秒：`.asm` 跨 1.1s 仍一致；PE exe 跨 1.1s 只差时间戳 ⇒ 判 time_window_drift。"""
    meta = _card()
    asm = aer._recompile_invariant_extended(str(meta["command"]), ASM_REL, gap_s=1.1)
    assert asm["sha_match"] is True, "汇编产物跨 1.1s 应字节一致"
    assert asm["cross_time"]["sha_a"] == asm["cross_time"]["sha_b"]

    # PE exe：在 tmp 里造同形态工件（真 g++ 编译），把"仓库根"指向 tmp
    env = dict(aer._compiler_env())
    (tmp_path / "t.cpp").write_text(
        "int add(int a,int b){return a+b;}\nint main(){return add(1,2);}\n", encoding="utf-8")
    subprocess.run([_gpp(), "-O2", "t.cpp", "-o", "t.exe"], cwd=str(tmp_path), check=True,
                   env=env)
    monkeypatch.setattr(aer, "run_root", lambda: tmp_path)
    res = aer._recompile_invariant_extended("g++ -O2 t.cpp -o t.exe", "t.exe", gap_s=1.1)
    assert res["status"] == "time_window_drift", res["details"]
    assert res["sha_match"] is False, "PE 跨秒必然改变时间戳字节"
    assert res["diff"]["diff_bytes"] <= 8 and res["diff"]["timestamp_only"] is True
    assert res["cross_time"]["timestamp_proof"] == "no_insert_timestamp_pair_identical"
    assert res["nm_match"] is True and res["objdump_match"] is True
    assert res["strings_match"] is True, "差异只在时间戳 ⇒ 语义维度必须全一致"
    assert "no-insert-timestamp" in res["diff"]["recipe"]


def test_tool_unavailable(monkeypatch):
    """nm/objdump/strings 不可用 ⇒ 三个字段全 skipped（不影响 sha 判定）。"""
    meta = _card()
    monkeypatch.setattr(aer.shutil, "which", lambda *a, **k: None)
    res = aer._recompile_invariant_extended(str(meta["command"]), ASM_REL, gap_s=1.1)
    assert res["nm_match"] == "skipped"
    assert res["objdump_match"] == "skipped"
    assert res["strings_match"] == "skipped"
    assert res["tools"] == {"nm": "missing", "objdump": "missing", "strings": "missing"}
    assert res["status"] == "ok", "缺工具不该把可复现的工件判成不可复现"


def test_backward_compatibility():
    """`_recompile_invariant` 语义不变：sha 一致 ⇒ ok；给错卡值 ⇒ tampered；无编译行 ⇒ unavailable。"""
    meta = _card()
    want = _sha(aer.run_root() / ASM_REL)
    status, detail = aer._recompile_invariant(str(meta["command"]), ASM_REL, want)
    assert (status, "卡值" in detail) == ("ok", True), detail
    bad, detail2 = aer._recompile_invariant(str(meta["command"]), ASM_REL, "0" * 64)
    assert bad == "tampered" and "≠" in detail2, detail2
    miss, _ = aer._recompile_invariant("true", "no/such/artifact.exe", want)
    assert miss == "unavailable"
    # 扩展函数是**新**入口：不改动 replay 判决路径（源码里 replay_card 仍只调旧函数）
    src = Path(aer.__file__).read_text(encoding="utf-8")
    assert "rc_status, rc_detail = _recompile_invariant(" in src
    assert "_recompile_invariant_extended(" in src
