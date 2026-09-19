"""609 D1 · OpenTimestamps 锚定回归锁（**只生成待上链、只离线校验**）。

锁四件事（任务书 4 例 + 2 例自加）：
  1. `stamp` 生成的字节":[magic + version(0x01) + body]"，且 magic 与 OTS 文档一致；
  2. `.ots` 里记的 file digest == `sha256(file)`（**没有 classroom 上链也能验的那一环**）；
  3. `verify` 文件被改一个字节 ⇒ digest_matches=False（**必须失败**，不许"看起来通过"）；
  4. `--check` 结构自洽（round-trip），且默认产物一定是 `attestation_pending`；
  +. 结构非法的 `.ots` ⇒ exit 3（不静默、不当'通过'）；
  +. **不 submit**：任何入口都不发起网络（本次断言：工具源码里没有 requests/urllib 调用）。
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import opentimestamps_anchor as ots


def _file(tmp_path: Path, name: str = "m.md", body: bytes = b"hello anchor") -> Path:
    p = tmp_path / name
    p.write_bytes(body)
    return p


def test_stamp_bytes_layout(tmp_path: Path):
    f = _file(tmp_path)
    ots_path = tmp_path / "m.md.ots"
    assert ots.main(["stamp", str(f), "--out", str(ots_path)]) == 0
    raw = ots_path.read_bytes()
    assert raw.startswith(ots.HEADER), "magic 头不对（不是 OTS 布局）"
    assert raw[len(ots.HEADER)] == 1, "version 字节应为 0x01"
    parsed = ots.parse_ots(raw)
    assert parsed["ops"] == ["sha256", "append"]
    assert parsed["file_digest"] == hashlib.sha256(b"hello anchor").hexdigest()


def test_default_product_is_pending_not_claimed_anchor(tmp_path: Path):
    f = _file(tmp_path)
    o = tmp_path / "p.ots"
    ots.main(["stamp", str(f), "--out", str(o)])
    parsed = ots.parse_ots(o.read_bytes())
    assert parsed["attestation_pending"] is True, "默认产物必须承认'还没上链'"
    assert parsed["attestation_kind"] == "bitcoin"
    res = ots.verify(f, o)
    assert res["digest_matches"] and res["attestation_pending"]
    assert res["verdict"] == "digest_ok_pending_anchor"


def test_verify_detects_one_byte_tamper(tmp_path: Path):
    f = _file(tmp_path)
    o = tmp_path / "t.ots"
    ots.main(["stamp", str(f), "--out", str(o)])
    assert ots.verify(f, o)["digest_matches"] is True
    f.write_bytes(b"hello anchor!")                 # 改一个字节
    res = ots.verify(f, o)
    assert res["digest_matches"] is False, "改了文件还ripcord通过 ⇒ 时间戳形同伪造"
    assert res["verdict"] == "digest_mismatch"


def test_cli_verify_exit_codes(tmp_path: Path):
    f = _file(tmp_path)
    o = tmp_path / "v.ots"
    ots.main(["stamp", str(f), "--out", str(o)])
    assert ots.main(["verify", str(f), "--ots", str(o)]) == 0
    f.write_bytes(b"tampered")
    assert ots.main(["verify", str(f), "--ots", str(o)]) == 1


def test_malformed_ots_exits_3(tmp_path: Path):
    """结构非法 ⇒ exit 3，且明确说'结构非法'（不是'通过'也不是'摘要不符'）。"""
    f = _file(tmp_path)
    bad = tmp_path / "bad.ots"
    bad.write_bytes(b"NOT-AN-OTS-FILE-AT-ALL")
    rc = ots.main(["verify", str(f), "--ots", str(bad)])
    assert rc == 3, f"非法 .ots 的退出码应为 3，实得 {rc}"


def test_no_network_egress(tmp_path: Path):
    """609 铁律：不实际上链 ⇒ 源码里不许有联网调用（这里是静态断言，便宜且有效）。"""
    src = (Path(ots.__file__)).read_text(encoding="utf-8")
    for bad in ("requests.", "urllib.request", "socket.create_connection", "http.client"):
        assert bad not in src, f"源码出现联网调用 {bad} ⇒ 有 import 就会有submit风险"


def test_check_is_green():
    assert ots.check() == []
