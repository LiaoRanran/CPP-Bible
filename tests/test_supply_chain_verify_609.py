"""609 D3 · 供应链验证回归锁（包含证明 + 一致性 + append-only）。

锁五件事（任务书 5 例 + 2 例自加）：
  1. 包含证明：正例通过；**改叶子 / 改兄弟哈希 / 翻方向位** ⇒ 全部失败；
  2. 一致性：老树是新树逐叶前缀 ⇒ 通过；**新树更短 / 老树重排** ⇒ 失败（封堵回滚与重排）；
  3. append-only：只追加 ⇒ 通过；**改历史行 / 截断** ⇒ 失败；
  4. `demo` 批量：8 叶树的三类证明结果可复算（含各自的反例）；
  5. `--check`：n∈{1,2,3,5,8,9,16,17} 全叶覆盖，正反例都自洽；
  +. CLI 退出码（inclusion/consistency/append-only 各 0/1）。
"""
from __future__ import annotations

import json
from pathlib import Path

import supply_chain_verify as scv


def _tree(n: int, prefix: str = "leaf"):
    leaves = [f"{prefix}-{i}".encode() for i in range(n)]
    return leaves, scv.build_tree(leaves)


def test_inclusion_proof_ok_and_three_tamper_modes():
    leaves, (root, levels) = _tree(8)
    idx = 3
    proof = scv.inclusion_proof(levels, idx)
    assert scv.verify_inclusion(root.hex(), leaves[idx], idx, proof)[0] is True

    assert scv.verify_inclusion(root.hex(), b"leaf-3-BUT-DIFFERENT", idx, proof)[0] is False
    flipped = [dict(p, right=not p["right"]) for p in proof]        # 翻方向位
    assert scv.verify_inclusion(root.hex(), leaves[idx], idx, flipped)[0] is False
    bad_sib = [dict(proof[0], hash="00" * 32)] + proof[1:]           # 改兄弟哈希
    assert scv.verify_inclusion(root.hex(), leaves[idx], idx, bad_sib)[0] is False


def test_consistency_prefix_ok_rollback_and_reorder_fail():
    leaves, (_, new_levels) = _tree(8)
    half, (_, old_levels) = _tree(4)
    assert scv.verify_consistency(old_levels, new_levels)[0] is True

    short, (_, short_levels) = _tree(2)
    ok, why = scv.verify_consistency(old_levels, short_levels)
    assert ok is False and "裁短" in why

    reordered, (_, re_levels) = _tree(8, prefix="leaf")
    rev = list(reversed(list(reordered)))
    ok2, why2 = scv.verify_consistency(old_levels, scv.build_tree(rev)[1])
    assert ok2 is False and "改写" in why2


def test_append_only_append_ok_rewrite_fail():
    old = "".join(f"leaf-{i}\n" for i in range(4))
    assert scv.verify_append_only(old, old + "leaf-4\nleaf-5\n")[0] is True
    ok, why = scv.verify_append_only(old, "".join(f"LEAF-{i}\n" for i in range(6)))
    assert ok is False and "被改写" in why
    ok2, why2 = scv.verify_append_only(old, "leaf-0\nleaf-1\n")
    assert ok2 is False and "截断" in why2


def test_demo_is_recomputable():
    d = scv.demo(8)
    assert d["leaves"] == 8
    assert d["inclusion"]["ok"] is True and d["inclusion"]["tampered_ok"] is False
    assert d["consistency"]["ok"] is True and d["consistency"]["reordered_ok"] is False
    assert d["append_only"]["ok"] is True and d["append_only"]["tampered_ok"] is False


def test_check_covers_odd_sizes():
    assert scv.check() == []
    leaves, (root, levels) = _tree(9)          # 奇数叶子（最后一叶提升路径）
    for i in range(9):
        p = scv.inclusion_proof(levels, i)
        assert scv.verify_inclusion(root.hex(), leaves[i], i, p)[0] is True


def test_cli_exit_codes(tmp_path: Path):
    leaves, (root, levels) = _tree(8)
    proof = tmp_path / "proof.json"
    proof.write_text(json.dumps(scv.inclusion_proof(levels, 3)), encoding="utf-8")
    assert scv.main(["inclusion", "--leaf", "leaf-3", "--root", root.hex(),
                     "--index", "3", "--proof", str(proof)]) == 0
    assert scv.main(["inclusion", "--leaf", "leaf-3-X", "--root", root.hex(),
                     "--index", "3", "--proof", str(proof)]) == 1

    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps([f"leaf-{i}" for i in range(4)]), encoding="utf-8")
    new.write_text(json.dumps([f"leaf-{i}" for i in range(8)]), encoding="utf-8")
    assert scv.main(["consistency", "--old", str(old), "--new", str(new)]) == 0

    a, b = tmp_path / "a.txt", tmp_path / "b.txt"
    a.write_text("x\ny\n", encoding="utf-8")
    b.write_text("x\ny\nz\n", encoding="utf-8")
    assert scv.main(["append-only", "--old", str(a), "--new", str(b)]) == 0
    b.write_text("X\ny\nz\n", encoding="utf-8")
    assert scv.main(["append-only", "--old", str(a), "--new", str(b)]) == 1


def test_check_is_green():
    assert scv.main(["--check"]) == 0
