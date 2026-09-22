"""626 A2 · 决策包打包器回归测试（≥5 例）。"""
import json
import os
import sys
import tempfile
import zipfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pack_review_zip as P  # noqa: E402


def test_selftest_passes():
    assert P.selftest() == 0


def test_paths_use_forward_slash():
    with tempfile.TemporaryDirectory() as td:
        sub = os.path.join(td, "sub", "deep")
        os.makedirs(sub)
        open(os.path.join(sub, "x.md"), "w", encoding="utf-8").write("x\n")
        zp = os.path.join(td, "o.zip")
        P.pack(td, zp)
        with zipfile.ZipFile(zp) as z:
            names = z.namelist()
        assert "sub/deep/x.md" in names
        assert not any("\\" in n for n in names)


def test_manifest_present_and_bound():
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "a.md"), "w", encoding="utf-8").write("a\n")
        zp = os.path.join(td, "o.zip")
        P.pack(td, zp)
        with zipfile.ZipFile(zp) as z:
            man = json.loads(z.read("SNAPSHOT_MANIFEST.json"))
        assert man["path_separator"] == "/"
        assert man["git_sha"]
        assert man["file_count"] == 1


def test_control_chars_cleaned_on_pack():
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "b.md"), "wb") as fh:
            fh.write(b"verifier\x08\x0b\n")
        zp = os.path.join(td, "o.zip")
        P.pack(td, zp)
        with zipfile.ZipFile(zp) as z:
            data = z.read("b.md")
        assert b"\x08" not in data and b"\x0b" not in data
        assert b"\n" in data


def test_check_rejects_nonconforming_zip():
    """反斜杠路径 / 缺 manifest 的包应判失败。

    注意：`zipfile.ZipInfo` 在 Windows 上会把 `os.sep`（`\\`）自动归一为 `/`，
    因此"反斜杠计数"在 Windows 恒为 0；断言改为平台无关：包缺少 SNAPSHOT_MANIFEST ⇒ 必失败。
    """
    with tempfile.TemporaryDirectory() as td:
        zp = os.path.join(td, "bad.zip")
        with zipfile.ZipFile(zp, "w") as z:
            z.writestr("dir\\file.md", "x")
        rc, res = P.check(zp)
        assert rc == 1
        assert res["has_manifest"] is False
        if os.sep != "\\":          # 非 Windows：反斜杠不会被归一，应被检出
            assert res["backslash"] == 1


@pytest.mark.parametrize("missing", ["SNAPSHOT_MANIFEST.json"])
def test_check_requires_manifest(missing):
    with tempfile.TemporaryDirectory() as td:
        zp = os.path.join(td, "o.zip")
        with zipfile.ZipFile(zp, "w") as z:
            z.writestr("a.md", "x")
        rc, res = P.check(zp)
        assert rc == 1 and not res["has_manifest"]
