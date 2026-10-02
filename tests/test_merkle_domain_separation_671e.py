# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671e-B · Merkle 树域分隔核查测试。

**核查结论（先复现，再下结论）**：
671c 调研把"Merkle 树缺域分隔、存在第二原像攻击"列为 *硬缺陷候选*。
本批经代码阅读 + PoC 复现，结论是 **false positive（非缺陷）**：

  * `tools/merkle_integrity.py` 第 56-57 行已定义
    `_LEAF_PREFIX = b"\\x00"`、`_NODE_PREFIX = b"\\x01"`；
  * 叶子 `leaf_hash = sha256(0x00 || rel_path || 0x00 || content)`（路径绑定）；
  * 内部节点 `_node_hash = sha256(0x01 || u64(左叶数) || u64(右叶数) || 左 || 右)`
    （子树规模绑定）；
  * 奇数节点**提升**（非复制），杜绝 CVE-2012-2459 类歧义；
  * 空目录根 = `sha256(b"")`（明确定义）。

因为叶/内节点输入的**首字节固定不同**（0x00 vs 0x01），二者 SHA-256 输入空间
不相交 ⇒ 一个内部节点的 hash 永远不可能等于任何叶子的 hash ⇒ 第二原像/伪造证明
在 `verify()` 的叶 hash 复核阶段就被拒。本测试集：
  (1) 锁定域分隔前缀确实为 0x00/0x01；
  (2) 写 PoC 证明"伪造一个内部节点值当叶子"无法得逞；
  (3) 锁定空树/单节点/路径绑定/规模绑定等边界行为。
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

_OP = importlib.util.spec_from_file_location("merkle_integrity_671e", os.path.join(TOOLS, "merkle_integrity.py"))
mi = importlib.util.module_from_spec(_OP)
_OP.loader.exec_module(mi)


def _write(dirp, rel, content: bytes):
    p = os.path.join(str(dirp), rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(content)


def _leaf_manual(rel: str, content: bytes, prefix: bytes = b"\x00") -> str:
    h = hashlib.sha256()
    h.update(prefix)
    h.update(rel.encode("utf-8"))
    h.update(b"\x00")
    h.update(content)
    return h.hexdigest()


def _node_manual(left: tuple[str, int], right: tuple[str, int], prefix: bytes = b"\x01") -> str:
    h = hashlib.sha256()
    h.update(prefix)
    h.update(left[1].to_bytes(8, "big"))
    h.update(right[1].to_bytes(8, "big"))
    h.update(bytes.fromhex(left[0]))
    h.update(bytes.fromhex(right[0]))
    return h.hexdigest()


def test_leaf_prefix_is_0x00():
    assert mi._LEAF_PREFIX == b"\x00"


def test_internal_node_prefix_is_0x01():
    assert mi._NODE_PREFIX == b"\x01"


def test_leaf_hash_uses_0x00_prefix_behaviorally():
    # 用 0x00 前缀重算，必须与模块输出一致；换 0x01 必须不一致。
    rel, content = "a.txt", b"hello"
    got = mi.leaf_hash(rel, _bytes_file(content))
    assert got == _leaf_manual(rel, content, b"\x00")
    assert got != _leaf_manual(rel, content, b"\x01")


def test_internal_node_hash_uses_0x01_prefix_behaviorally():
    left, right = ("aa" * 32, 1), ("bb" * 32, 1)
    got, _ = mi._node_hash(left, right)
    assert got == _node_manual(left, right, b"\x01")
    assert got != _node_manual(left, right, b"\x00")


def _bytes_file(content: bytes):
    import pathlib
    import tempfile
    p = pathlib.Path(tempfile.gettempdir()) / f"_cf_671e_leaf_{hashlib.sha256(content).hexdigest()[:8]}.bin"
    p.write_bytes(content)
    return p


def test_second_preimage_poc_cannot_collide_leaf_and_internal():
    """PoC（B3）：构造一个内部节点，试图让其 hash 等于某叶子 hash。
    因为前缀 0x00(叶) != 0x01(内)，二者 SHA-256 输入空间不相交 ⇒ 不可能相等。"""
    import tempfile
    from pathlib import Path
    d = Path(tempfile.mkdtemp())
    try:
        _write(d, "f1", b"alpha")
        _write(d, "f2", b"beta")
        tree = mi.build_tree(d)
        # 两叶 → 根即一个内部节点（_node_hash）
        internal = tree["root"]
        assert internal == mi._node_hash((tree["leaves"][0]["hash"], 1),
                                         (tree["leaves"][1]["hash"], 1))[0]
        # 攻击者能操控的"叶子内容"都带 0x00 前缀；穷举若干候选，绝不等于 internal(0x01)
        candidates = [b"", b"alpha", b"beta", internal.encode(),
                      bytes.fromhex(internal), b"\x01" + bytes.fromhex(internal)]
        for c in candidates:
            # 任一路徑下算出的叶子 hash 都不可能是带 0x01 前缀的内部节点值
            assert mi.leaf_hash("attacker", _bytes_file(c)) != internal
            assert mi.leaf_hash("f1", _bytes_file(c)) != internal
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_forged_membership_proof_rejected(tmp_path):
    """PoC（B3）：伪造"某文件在树中"的证明 —— 把内部节点值塞进 leaf.hash。
    verify() 会用 0x00 前缀重算叶 hash，与伪造的 0x01 值不符 ⇒ 拒绝。"""
    _write(tmp_path, "real.txt", b"real content")
    tree = mi.build_tree(tmp_path)
    root = tree["root"]
    internal_like = root  # 它本是 _node_hash 产物（0x01 前缀）
    proof = {"algo": mi.ALGO, "root": root,
             "leaf": {"path": "forged.txt", "hash": internal_like},
             "leaf_count": 1, "tree_height": 0, "steps": []}
    # 用一个真实存在的文件去 verify（内容由 0x00 前缀算出），必然 ≠ internal_like
    _write(tmp_path, "forged.txt", b"forged")
    ok, why = mi.verify(str(tmp_path / "forged.txt"), proof, root)
    assert ok is False
    assert "叶 hash" in why or "根 hash" in why


def test_valid_proof_accepted(tmp_path):
    _write(tmp_path, "a.txt", b"aaa")
    _write(tmp_path, "b.txt", b"bbb")
    _write(tmp_path, "c.txt", b"ccc")
    tree = mi.build_tree(tmp_path)
    root = tree["root"]
    for rel in ("a.txt", "b.txt", "c.txt"):
        proof = mi.prove(tmp_path, rel)
        ok, why = mi.verify(str(tmp_path / rel), proof, root)
        assert ok, why


def test_prove_verify_roundtrip_every_file(tmp_path):
    for i in range(5):
        _write(tmp_path, f"f{i}.txt", f"data-{i}".encode())
    tree = mi.build_tree(tmp_path)
    for i in range(5):
        proof = mi.prove(tmp_path, f"f{i}.txt")
        ok, _ = mi.verify(str(tmp_path / f"f{i}.txt"), proof, tree["root"])
        assert ok


def test_empty_tree_root_is_sha256_empty():
    import tempfile
    from pathlib import Path
    d = Path(tempfile.mkdtemp())
    try:
        tree = mi.build_tree(d)
        assert tree["root"] == mi.EMPTY_ROOT == hashlib.sha256(b"").hexdigest()
        assert tree["file_count"] == 0
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_single_file_tree_root_equals_leaf(tmp_path):
    _write(tmp_path, "only.txt", b"x")
    tree = mi.build_tree(tmp_path)
    assert tree["tree_height"] == 0
    assert tree["root"] == tree["leaves"][0]["hash"]


def test_root_is_deterministic_and_idempotent(tmp_path):
    _write(tmp_path, "a", b"1")
    _write(tmp_path, "b", b"2")
    r1 = mi.build_tree(tmp_path)["root"]
    r2 = mi.build_tree(tmp_path)["root"]
    assert r1 == r2


def test_path_binding_changes_root_on_rename(tmp_path):
    """路径绑定：同内容换名 ⇒ 根必须变（否则可"换名骗根"）。"""
    _write(tmp_path, "a.txt", b"same")
    r1 = mi.build_tree(tmp_path)["root"]
    _write(tmp_path, "b.txt", b"same")  # 同内容不同名
    os.remove(str(tmp_path / "a.txt"))
    r2 = mi.build_tree(tmp_path)["root"]
    assert r1 != r2


def test_internal_node_subtree_count_binding():
    """规模绑定：子树叶数不同（即使子 hash 相同）内部节点必须不同 ⇒ 形状歧义无解。"""
    h = "ab" * 32
    n_same = mi._node_hash((h, 1), (h, 1))[0]
    n_diff = mi._node_hash((h, 1), (h, 2))[0]   # 右子树叶数不同
    assert n_same != n_diff


def test_odd_node_promotion_no_duplicate_ambiguity(tmp_path):
    """3 叶树经"提升"折叠，且每个不同路径都能独立出有效证明。"""
    for i in range(3):
        _write(tmp_path, f"f{i}.txt", f"v{i}".encode())
    tree = mi.build_tree(tmp_path)
    root = tree["root"]
    for i in range(3):
        proof = mi.prove(tmp_path, f"f{i}.txt")
        ok, why = mi.verify(str(tmp_path / f"f{i}.txt"), proof, root)
        assert ok, why


def test_verify_rejects_wrong_algo(tmp_path):
    _write(tmp_path, "a.txt", b"a")
    proof = mi.prove(tmp_path, "a.txt")
    proof["algo"] = "evil-algo"
    ok, why = mi.verify(str(tmp_path / "a.txt"), proof, mi.build_tree(tmp_path)["root"])
    assert ok is False
    assert "算法" in why


def test_verify_rejects_tampered_leaf_hash(tmp_path):
    _write(tmp_path, "a.txt", b"a")
    tree = mi.build_tree(tmp_path)
    proof = mi.prove(tmp_path, "a.txt")
    proof["leaf"]["hash"] = "00" * 32
    ok, why = mi.verify(str(tmp_path / "a.txt"), proof, tree["root"])
    assert ok is False
    assert "叶 hash" in why


def test_consistency_append_only_holds(tmp_path):
    old = mi.build_tree(_dir_with(tmp_path, {"a": b"1", "b": b"2"}))
    new = mi.build_tree(_dir_with(tmp_path, {"a": b"1", "b": b"2", "c": b"3"}))
    proof = mi.consistency_prove(old, new)
    ok, why = mi.consistency_verify(proof)
    assert ok, why


def test_consistency_rejects_removed_file(tmp_path):
    old = mi.build_tree(_dir_with(tmp_path, {"a": b"1", "b": b"2"}))
    new = mi.build_tree(_dir_with(tmp_path, {"a": b"1"}))   # b 被删
    proof = mi.consistency_prove(old, new)
    ok, why = mi.consistency_verify(proof)
    assert ok is False
    assert "删" in why or "少" in why


def _dir_with(base, mapping: dict):
    import tempfile
    from pathlib import Path
    d = Path(tempfile.mkdtemp())
    for rel, content in mapping.items():
        _write(d, rel, content)
    return d
