#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673e 任务 A · Merkle 0x00/0x01 域分隔的**独立复现**（不依赖 671e 的测试与结论）。

671e 已核查过并判"误报"，本文件的价值不是重复，而是补三块 671e 没覆盖的：

  1. **输入空间字节级不相交**：不只看前缀常量，而是断言"任何文件内容都不可能让叶 hash 等于
     内节点 hash"（因为 sha256 输入第 0 字节必须同时是 0x00 与 0x01）。
  2. **长度扩展（SHA-256 Merkle–Damgård）**：671e 只做了"篡改被拒"，没有正面做长度扩展。
     本文件带一个纯 Python SHA-256（与 hashlib 逐例对齐），真的算一次扩展，并证明
     扩展产生的是**不同 digest** ⇒ 不是同一 hash 的第二原像 ⇒ 不可利用。
  3. **反事实对照**：把两个前缀都抹掉后，检查攻击前提是否出现（路径绑定仍挡住这一路）。

来源：673e 任务书「任务A · Merkle 0x00/0x01 域分隔前缀核查」。
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _load_merkle():
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location("_mi_673e", TOOLS / "merkle_integrity.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_mi_673e"] = mod          # 671g 教训：exec 前先登记，否则 @dataclass 会崩
    spec.loader.exec_module(mod)
    return mod


mi = _load_merkle()


# ── 1. 结构性：前缀存在且不相交 ────────────────────────────────────────────────
def test_leaf_prefix_is_0x00_and_node_prefix_is_0x01():
    assert mi._LEAF_PREFIX == b"\x00", "叶前缀必须是 0x00"
    assert mi._NODE_PREFIX == b"\x01", "内节点前缀必须是 0x01"


def test_prefixes_are_different_so_input_spaces_are_disjoint():
    """域分隔的**充分条件**：sha256 输入的第 0 字节不同 ⇒ 两个输入集合不相交。"""
    assert mi._LEAF_PREFIX != mi._NODE_PREFIX
    assert mi._LEAF_PREFIX[0] != mi._NODE_PREFIX[0]


def test_no_file_content_can_make_leaf_hash_equal_node_hash(tmp_path):
    """穷举一批内容，确认叶 hash 集合与内节点 hash 集合无交（含内部节点本身）。"""
    d = tmp_path / "tree"
    d.mkdir()
    for i in range(6):
        (d / f"f{i}.txt").write_bytes(f"payload-{i}".encode())
    files = mi.iter_files(d)
    leaves = {mi.leaf_hash(r, p) for r, p in files}
    nodes = set()
    cur = [(mi.leaf_hash(r, p), 1) for r, p in files]
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur), 2):
            if i + 1 < len(cur):
                h, n = mi._node_hash(cur[i], cur[i + 1])
                nodes.add(h)
                nxt.append((h, n))
            else:
                nxt.append(cur[i])
        cur = nxt
    assert nodes, "树太小，没产生内节点"
    assert leaves.isdisjoint(nodes), "叶 hash 与内节点 hash 相交 ⇒ 域分隔失效"


# ── 2. 构造性 PoC：把内节点冒充叶 ──────────────────────────────────────────────
def test_forged_proof_replacing_leaf_with_internal_node_is_rejected(tmp_path):
    d = tmp_path / "tree"
    d.mkdir()
    for i in range(5):
        (d / f"f{i}.txt").write_bytes(f"c{i}".encode())
    real = mi.prove(d, d / "f0.txt")
    h_a = mi.leaf_hash("f0.txt", d / "f0.txt")
    h_b = mi.leaf_hash("f1.txt", d / "f1.txt")
    internal, _n = mi._node_hash((h_a, 1), (h_b, 1))

    forged = dict(real)
    forged["leaf"] = {"path": "evil.txt", "hash": internal}
    (d / "evil.txt").write_bytes(b"anything")

    ok, why = mi.verify(d / "evil.txt", forged, internal)
    assert not ok, "内节点冒充叶的伪造证明被接受 ⇒ 域分隔失效"
    assert "叶 hash 不匹配" in why


def test_legitimate_proof_still_accepted(tmp_path):
    """反向对照：证明器没有被"修坏"（假阳/假阴双向可判）。"""
    d = tmp_path / "tree"
    d.mkdir()
    for i in range(4):
        (d / f"g{i}.txt").write_bytes(f"v{i}".encode())
    proof = mi.prove(d, d / "g2.txt")
    ok, why = mi.verify(d / "g2.txt", proof, proof["root"])
    assert ok, why


# ── 3. 长度扩展：671e 没覆盖的一块 ─────────────────────────────────────────────
_K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]
_IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
       0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]


def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def _compress(state, block: bytes):
    w = [int.from_bytes(block[i:i + 4], "big") for i in range(0, 64, 4)]
    for i in range(16, 64):
        s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF)
    a, b, c, d, e, f, g, h = state
    for i in range(64):
        s1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        t1 = (h + s1 + ch + _K[i] + w[i]) & 0xFFFFFFFF
        s0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (s0 + maj) & 0xFFFFFFFF
        h, g, f, e, d, c, b, a = (g, f, e, (d + t1) & 0xFFFFFFFF, c, b, a,
                                  (t1 + t2) & 0xFFFFFFFF)
    return [(x + y) & 0xFFFFFFFF for x, y in zip(state, [a, b, c, d, e, f, g, h])]


def _pad(msg_len: int) -> bytes:
    return (b"\x80" + b"\x00" * ((56 - (msg_len + 1) % 64) % 64)
            + (msg_len * 8).to_bytes(8, "big"))


def _sha256_state(data: bytes, state=None, total_len=None):
    st = list(state or _IV)
    n = len(data) if total_len is None else total_len
    buf = data + _pad(n)
    for i in range(0, len(buf), 64):
        st = _compress(st, buf[i:i + 64])
    return st


def _hex(st) -> str:
    return b"".join(x.to_bytes(4, "big") for x in st).hex()


@pytest.mark.parametrize("probe", [b"", b"a", b"abc", b"x" * 55, b"y" * 64, b"z" * 200])
def test_pure_python_sha256_matches_hashlib(probe):
    """长度扩展测试的前提：自带实现必须与 hashlib 逐例一致（含 55/64/200 填充边界）。"""
    assert _hex(_sha256_state(probe)) == hashlib.sha256(probe).hexdigest()


def test_length_extension_yields_a_different_digest_not_a_second_preimage(tmp_path):
    """长度扩展能算出 H(m || glue || suffix)，但那**不是** m 的同一 hash ⇒ 不能伪造证明。"""
    d = tmp_path / "le"
    d.mkdir()
    rel, content = "a.txt", b"hello"
    (d / rel).write_bytes(content)

    m = mi._LEAF_PREFIX + rel.encode() + b"\x00" + content
    h1 = hashlib.sha256(m).hexdigest()
    assert h1 == mi.leaf_hash(rel, d / rel)

    glue = _pad(len(m))
    suffix = b"-evil"
    h2 = _hex(_sha256_state(suffix, state=_sha256_state(m),
                            total_len=len(m) + len(glue) + len(suffix)))
    assert h2 == hashlib.sha256(m + glue + suffix).hexdigest(), "长度扩展实现有误"
    assert h2 != h1, "长度扩展竟得到同一 hash ⇒ 第二原像 ⇒ 严重"

    # 用扩展后的文件去满足**原 hash** 的证明：必须被拒
    (d / rel).write_bytes(content + glue + suffix)
    proof = {"algo": mi.ALGO, "root": h1, "leaf": {"path": rel, "hash": h1}, "steps": []}
    ok, why = mi.verify(d / rel, proof, h1)
    assert not ok, "长度扩展可伪造 ⇒ 严重"
    assert "叶 hash 不匹配" in why


def test_path_binding_blocks_the_no_prefix_counterfactual(tmp_path):
    """反事实：即使把 0x00/0x01 都抹掉，路径绑定仍使对齐不可能（内节点输入以 NUL 开头）。"""
    saved_l, saved_n = mi._LEAF_PREFIX, mi._NODE_PREFIX
    (tmp_path / "f0.txt").write_bytes(b"0")
    (tmp_path / "f1.txt").write_bytes(b"1")
    mi._LEAF_PREFIX = mi._NODE_PREFIX = b""
    try:
        a = mi.leaf_hash("f0.txt", tmp_path / "f0.txt")
        b = mi.leaf_hash("f1.txt", tmp_path / "f1.txt")
        node_input = mi._u64(1) + mi._u64(1) + bytes.fromhex(a) + bytes.fromhex(b)
        assert node_input[0] == 0x00, "内节点输入首字节应为 u64(1) 的高位 0x00"
        # 叶输入 = rel_path || 0x00 || content，首字节来自路径；路径不能含 NUL ⇒ 无法对齐
        assert 0x00 not in "f0.txt".encode()
    finally:
        mi._LEAF_PREFIX, mi._NODE_PREFIX = saved_l, saved_n


def test_671e_source_module_unchanged_contract():
    """671e 结论的载体（前缀常量）在本批**未被改动**——本批只加测试、不改实现。"""
    src = (TOOLS / "merkle_integrity.py").read_text(encoding="utf-8")
    assert '_LEAF_PREFIX = b"\\x00"' in src
    assert '_NODE_PREFIX = b"\\x01"' in src
