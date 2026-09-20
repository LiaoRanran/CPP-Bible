"""609 E2 · 编译可复现性深化回归锁（12 宏 + 4 nm + 4 objdump + diff 替代品）。

锁四件事（任务书 4 例 + 3 例自加）：
  1. 12 个跨时间窗口宏齐全，每条都有类别（time/path/counter/env）与理由，**8 条必须屏蔽**；
  2. nm 4 参数与 objdump 4 参数齐全，每条都写了"为什么必须这么取"；
  3. diff 替代品：相同文件 ⇒ identical；改 1 字节 ⇒ 精确报出首个差异偏移 + 差异字节数；
     只在一侧追加 ⇒ 判为差异且 size 不同（**不许**因为前缀相同就说"一致"）；
  4. `--check` 结构自洽（条数 + diff 自检）；
  +. `-j <段名>` 与"只比长度的段"清单都在（防把 .comment 卷进逐字节比对）；
  +. CLI 退出码：diff 相同 0 / 有差异 1 / 缺文件 2。
"""
from __future__ import annotations

from pathlib import Path

import build_reproducibility_deep as e2
import pytest


def test_twelve_macros_with_classification():
    assert len(e2.MACROS) == 12
    kinds = {m[1] for m in e2.MACROS}
    assert kinds == {"time", "path", "counter", "env"}, f"类别不全：{kinds}"
    for name, kind, mask, why in e2.MACROS:
        assert name.startswith("__") and name.endswith("__")
        assert isinstance(mask, bool) and why.strip(), f"{name} 缺理由"
    must_mask = [m[0] for m in e2.MACROS if m[2]]
    # 实测口径：time 3（__DATE__/__TIME__/__TIMESTAMP__）+ path 2（__FILE__/__BASE_FILE__）
    # + env 2（__STDC_VERSION__/__GNUC__）= 7；__FILE_NAME__ 只含文件名 ⇒ 跨窗口稳定，不屏蔽
    assert len(must_mask) == 7, f"必须屏蔽的宏应为 7 条，实得 {len(must_mask)}：{must_mask}"
    assert "__DATE__" in must_mask and "__TIME__" in must_mask
    assert "__FILE_NAME__" not in must_mask
    assert "__LINE__" not in must_mask, "__LINE__ 同源码同值 ⇒ 不该要求屏蔽"


def test_nm_and_objdump_params():
    assert len(e2.NM_PARAMS) == 4 and len(e2.OBJDUMP_PARAMS) == 4
    for p, what, why in e2.NM_PARAMS + e2.OBJDUMP_PARAMS:
        assert p and what and why, f"参数条目不完整：{p}"
    nm_flags = " ".join(p for p, _w, _y in e2.NM_PARAMS)
    for flag in ("--defined-only", "--extern-only", "-P", "--no-demangle"):
        assert flag in nm_flags, f"缺 nm 参数 {flag}"
    od_flags = " ".join(p for p, _w, _y in e2.OBJDUMP_PARAMS)
    assert "-h" in od_flags and "-s" in od_flags and "-j <段名>" in od_flags
    assert ".comment" in e2.LEN_ONLY_SECTIONS, "必须把工具链版本印记段排除在逐字节比对之外"


def test_diff_identical_and_one_byte_change(tmp_path: Path):
    a = tmp_path / "a.bin"
    a.write_bytes(bytes(range(64)))
    assert e2.diff_bytes(a, a)["identical"] is True

    b = tmp_path / "b.bin"
    raw = bytearray(range(64))
    raw[37] = 0xFF
    b.write_bytes(bytes(raw))
    res = e2.diff_bytes(a, b, context=4)
    assert res["identical"] is False
    assert res["first_diff"] == 37, f"首个差异偏移应为 37，实得 {res['first_diff']}"
    assert res["differing_bytes"] == 1
    assert res["sha256_a"] != res["sha256_b"]
    assert res["context_a"] != res["context_b"]


def test_diff_detects_length_only_divergence(tmp_path: Path):
    a = tmp_path / "a.bin"
    a.write_bytes(b"prefix-only")
    b = tmp_path / "b.bin"
    b.write_bytes(b"prefix-only-plus")
    res = e2.diff_bytes(a, b)
    assert res["identical"] is False and res["first_diff"] == len(b"prefix-only")
    assert res["size_a"] == 11 and res["size_b"] == 16
    assert res["differing_bytes"] == 5


def test_cli_exit_codes_and_missing_file(tmp_path: Path):
    a = tmp_path / "a.bin"
    a.write_bytes(b"x" * 8)
    b = tmp_path / "b.bin"
    b.write_bytes(b"x" * 8)
    assert e2.main(["diff", str(a), str(b)]) == 0
    b.write_bytes(b"y" * 8)
    assert e2.main(["diff", str(a), str(b)]) == 1
    with pytest.raises(SystemExit):
        e2.diff_bytes(a, tmp_path / "nope.bin")


def test_kernel_macros_are_not_env_noise():
    """`__FILE_NAME__/__LINE__/__func__/__INCLUDE_LEVEL__/__COUNTER__` 不随窗口变 ⇒ 不屏蔽。"""
    stable = {n for n, _k, mask, _w in e2.MACROS if not mask}
    assert stable == {"__FILE_NAME__", "__LINE__", "__func__", "__INCLUDE_LEVEL__", "__COUNTER__"}


def test_check_and_report():
    assert e2.check() == []
    report = e2.render_report()
    assert "12 宏" in report and "nm 4 参数" in report and "objdump 4 参数" in report
    assert report.count("| `__") == 12, "报告里应逐个列出 12 个宏"
