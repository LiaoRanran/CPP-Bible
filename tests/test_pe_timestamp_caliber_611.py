"""611 A3 · PE 时间戳口径正式化（610 交人项 ③）。

把 610 E3 的实测结论**写进正式报告并锁住**，同时把"改哪份报告、为什么不改另一份"钉成测试。

口径落点（决策 + 理由）：
  * **改** `data/build_reproducibility_deep.md`（609 E2 的编译可复现报告，有 §1–§5 结构，
    由 `tools/build_reproducibility_deep.py` 生成、`--check` 可自洽校验）⇒ 新增 **§五 PE 时间戳口径**；
  * **不改** `data/build_reproducibility_report.md`：实测它是 **UTF-16LE**（674 B，头 `ff fe`；
    工作树与 git blob 都是），是 PowerShell 重定向的捕获产物、**全仓无人引用**（仅本测试读它），
    往里追加 UTF-8 章节会制造编码/CRLF 假脏（本仓已有两条此类假脏文件的教训）⇒ 只登记不改。

锁五件事：
  1. deep 报告含 §五 与全部 PE 事实条目（含新状态名 `time_window_drift` 与 `--no-insert-timestamp` 配方）；
  2. 生成器的 `--check` 自洽（删条目即报红 ⇒ 文档即代码）；
  3. 603 捕获报告**保持 UTF-16 且未被本批改动**（记录决策，防后人误改）；
  4. 代码侧：`_pe_timestamp_offsets` 在真 PE 上给出 `0x88`（e_lfanew+8），在 `.asm` 上给出 `[]`；
  5. 端到端：真 PE 跨 1.1s 编译 ⇒ `time_window_drift` + 取证配方（真调 g++，标 slow）。
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as aer  # noqa: E402
import build_reproducibility_deep as brd  # noqa: E402

DEEP = ROOT / "data" / "build_reproducibility_deep.md"
CAPTURE = ROOT / "data" / "build_reproducibility_report.md"


def test_deep_report_has_pe_section():
    text = DEEP.read_text(encoding="utf-8")
    assert "## 五、PE 时间戳口径" in text, "编译可复现报告缺 PE 章节"
    for key, val in brd.PE_TIMESTAMP_FACTS:
        assert f"| {key} | {val} |" in text, f"报告缺 PE 口径条目：{key}"
    for must in ("time_window_drift", "-Wl,--no-insert-timestamp", "0x88", "0xd8",
                 "2 字节", "`nm` 符号表", "56 张证据卡", "SOURCE_DATE_EPOCH"):
        assert must in text, f"PE 章节缺事实：{must}"
    # 判读规则四档齐（ok / drift / not_reproducible / tampered）
    for status in ("`ok`", "`time_window_drift`", "`not_reproducible`", "`tampered`"):
        assert status in text, f"缺判读档位：{status}"


def test_generator_check_is_green_and_doc_locked():
    assert brd.check() == [], "生成器自检不过（PE 条目与报告不同步）"
    rows = [k for k, _ in brd.PE_TIMESTAMP_FACTS]
    assert len(rows) >= 8 and "新状态名" in rows and "可复现配方" in rows


def test_603_capture_untouched_by_this_batch():
    """603 捕获报告：**未**被 611 改动（决策留痕，防后人误改制造编码假脏）。

    注：该文件字节为「UTF-16 BOM(ff fe) + UTF-8 正文」的错配（PowerShell 捕获产物），
    故按 UTF-8 读正文（632 A2 #4 修复：定位编码问题→按 UTF-8 解码），不应按 UTF-16 解码。
    """
    raw = CAPTURE.read_bytes()
    assert raw[:2] in (b"\xff\xfe", b"\xfe\xff"), "前提变了：该文件不再是 UTF-16 BOM 开头"
    # 跳过 BOM，按 UTF-8 读正文；捕获产物偶有孤立坏字节，errors="replace" 容错（632 A2 #4）。
    text = raw[2:].decode("utf-8", errors="replace")
    assert "611 A3" not in text, "不许往捕获产物里混入 UTF-8 章节"
    assert "build_reproducibility" in text
    blob = subprocess.run(["git", "cat-file", "-p",
                           "HEAD:data/build_reproducibility_report.md"],
                          cwd=str(ROOT), capture_output=True).stdout
    assert blob == raw, "该文件与 HEAD 不一致（被谁改了？本批不改它）"


def test_pe_timestamp_offsets_detector():
    """纯函数：真 PE → 含 0x88（e_lfanew+8）；文本（.asm）→ 空。"""
    import struct
    pe = bytearray(0x200)
    pe[0:2] = b"MZ"
    e_lfanew = 0x80
    struct.pack_into("<I", pe, 0x3C, e_lfanew)
    pe[e_lfanew:e_lfanew + 4] = b"PE\0\0"
    struct.pack_into("<I", pe, e_lfanew + 8, 1789883907)
    pe[0xD8:0xDC] = struct.pack("<I", 1789883907)      # debug 目录同族副本
    offs = aer._pe_timestamp_offsets(bytes(pe))
    assert 0x88 in offs, offs
    assert aer._pe_timestamp_offsets(b"not a pe file") == []
    asm = ROOT / "Examples" / "atoms" / "_atom_fence_vs_atomic.asm"
    if asm.is_file():
        assert aer._pe_timestamp_offsets(asm.read_bytes()[:200000]) == [], "文本产物不该被判成 PE"


@pytest.mark.slow
@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="CI Ubuntu g++ 跨 1.1s 编译 PE  sha 一致（不插入时间戳），与本地 MinGW 行为不同",
)
def test_real_pe_is_time_window_drift_with_proof(tmp_path: Path, monkeypatch):
    """端到端（真调 g++）：PE 跨 1.1s ⇒ time_window_drift + 差异仅时间戳 + 取证通过。"""
    env = dict(aer._compiler_env())
    gpp = shutil.which("g++", path=env.get("PATH")) or "g++"
    (tmp_path / "t.cpp").write_text(
        "int add(int a,int b){return a+b;}\nint main(){return add(1,2);}\n", encoding="utf-8")
    subprocess.run([gpp, "-O2", "t.cpp", "-o", "t.exe"], cwd=str(tmp_path), check=True, env=env)
    monkeypatch.setattr(aer, "run_root", lambda: tmp_path)
    res = aer._recompile_invariant_extended("g++ -O2 t.cpp -o t.exe", "t.exe", gap_s=1.1)
    assert res["status"] == "time_window_drift", res["details"]
    assert res["diff"]["diff_bytes"] <= 8 and res["diff"]["timestamp_only"] is True
    assert res["cross_time"]["timestamp_proof"] == "no_insert_timestamp_pair_identical"
    assert "0x88" in res["diff"]["pe_timestamp_offsets"]
