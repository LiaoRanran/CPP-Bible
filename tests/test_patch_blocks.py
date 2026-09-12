"""锁定 patch_blocks 的真实回归：多块 stale-span 错isplaced + 行尾伪 diff。"""
from pathlib import Path

import patch_blocks as pb


def _md(body: str) -> str:
    return body


def test_multi_block_patch_does_not_shift(tmp_path):
    """事故：多块补丁按升序处理会违反自身「从大到小」契约，导致 stale-span 错位
    ——后面的块写到了错误位置（含 cpp→bash 转换时更严重）。"""
    md = tmp_path / "chX.md"
    md.write_bytes(
        b"intro\r\n\r\n```cpp\r\nA1\r\n```\r\n\r\n```cpp\r\nB1\r\n```\r\n\r\n"
        b"```cpp\r\nC1\r\n```\r\n")
    patch = [
        {"block": 1, "fence": "cpp", "body": "A2"},
        {"block": 3, "fence": "bash", "body": "# C2"},
    ]
    pb.apply_patch(md, patch, do_write=True)
    out = md.read_bytes().decode("utf-8")
    assert "A2" in out, "blk1 应被替换"
    assert "B1" in out, "blk2 必须原样保留（不得被串位污染）"
    assert "# C2" in out and "```bash" in out, "blk3 应被替换且围栏转为 bash"
    assert "A1" not in out and "C1" not in out


def test_crlf_preserved_after_patch(tmp_path):
    """R4 铁律：回写不得把 CRLF 翻成 LF，否则整文件伪 diff（曾一次 362 行）。"""
    md = tmp_path / "chY.md"
    md.write_bytes(b"t\r\n\r\n```cpp\r\nX1\r\n```\r\n")
    pb.apply_patch(md, [{"block": 1, "fence": "cpp", "body": "X2\nY2"}], do_write=True)
    raw = md.read_bytes()
    assert b"\r\n" in raw
    assert raw.count(b"\n") == raw.count(b"\r\n"), "不得出现裸 LF 行尾（行尾翻转）"


def test_dry_run_does_not_write(tmp_path):
    md = tmp_path / "chZ.md"
    original = b"t\r\n\r\n```cpp\r\nZ1\r\n```\r\n"
    md.write_bytes(original)
    pb.apply_patch(md, [{"block": 1, "fence": "cpp", "body": "Z2"}], do_write=False)
    assert md.read_bytes() == original, "do_write=False 必须零副作用"


def test_split_blocks_counts_only_cpp_fences():
    """_split_blocks 只认 ```cpp / ```c++（bash 块不参与 block 编号，与 compile_all 一致）。"""
    text = "a\n```cpp\nx\n```\nmid\n```bash\ny\n```\n```cpp\nz\n```\n"
    spans = pb._split_blocks(text)
    assert len(spans) == 2, "bash 块不计入，cpp 块应为 2"


def test_load_patch_rejects_bad_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    try:
        pb.load_patch(bad)
    except SystemExit:
        return
    raise AssertionError("非法 patch JSON 应 SystemExit 而非静默继续")


def test_patch_on_missing_file_is_safe(tmp_path):
    missing: Path = tmp_path / "nope.md"
    try:
        pb.apply_patch(missing, [{"block": 1, "fence": "cpp", "body": "x"}], True)
    except SystemExit:
        return
    raise AssertionError("目标文件缺失应 SystemExit")
