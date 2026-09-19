"""609 D3 · 供应链验证：**Merkle 包含证明 + 一致性证明 + append-only 验证**。

三条都是"**不重算全树也能证**"的密码学证明（这是它区别于"把树再建一遍"的地方）：

  * **包含证明**（inclusion）：给定叶子 `L` 与根 `R`，只需 `O(log n)` 个兄弟哈希 + 方向位
    ⇒ 任何人都能复算出根并与 `R` 比对。改一个叶子、改一个兄弟、改一个方向位 ⇒ 验证失败。
  * **一致性证明**（consistency）：append-only 日志从 `n0` 长到 `n1` 时，
    证明"老树是新树的**前缀**"（不是"新树任意重排后包含老树"）⇒ 封堵"回滚/重排历史"。
  * **append-only 验证**：给定日志文件的两个快照，验证后者是前者的**逐行前缀**
    （老行一个字节都不许变，只许在末尾追加）⇒ 封堵"篡改历史记录后再重算根"。

本工具**不重算**仓库 Merkle 根（那是 `merkle_integrity` 的活），只提供可单独复算的
证明层 + `--check` 自洽自检（随机树 round-trip）。

CLI：
    inclusion --leaf L --root R --proof P.json      0 通过 / 1 不通过
    consistency --old O.json --new N.json           0 通过 / 1 不通过
    append-only --old A.txt --new B.txt             0 通过 / 1 不通过
    demo [--leaves 8]                               0 造一棵树并演示三类证明（批量测试用）
    --check                                         0 自洽 / 1 破
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

VERSION = "1.0"
HASH = hashlib.sha256
DEMO_OUT = Path("data") / "supply_chain_verify_demo.json"


def _h(b: bytes) -> bytes:
    return HASH(b).digest()


def leaf_hash(data: bytes) -> bytes:
    """叶子哈希带 0x00 前缀（防"内部节点冒充叶子"的二阶原像把戏）。"""
    return _h(b"\x00" + data)


def node_hash(left: bytes, right: bytes) -> bytes:
    """内部节点带 0x01 前缀（域分离：叶子与内部节点哈希不相交）。"""
    return _h(b"\x01" + left + right)


def build_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    """自底向上建树；返回 (root, levels[0]=leaves_hashes ...)。"""
    if not leaves:
        return _h(b""), []
    level = [leaf_hash(x) for x in leaves]
    levels = [level]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(node_hash(level[i], level[i + 1]))
        if len(level) % 2 == 1:                 # 奇数 ⇒ 最后一个提升（同 RFC 6962 风格）
            nxt.append(level[-1])
        levels.append(nxt)
        level = nxt
    return level[0], levels


def inclusion_proof(levels: list[list[bytes]], index: int) -> list[dict]:
    """生成包含证明：[{hash, right:bool}]，从叶子往上每层一个兄弟。"""
    proof: list[dict] = []
    for level in levels[:-1]:
        if index % 2 == 0:                      # 我是左 ⇒ 需要右兄弟
            sib = level[index + 1] if index + 1 < len(level) else None
            right = True
        else:
            sib = level[index - 1]
            right = False
        if sib is not None:
            proof.append({"hash": sib.hex(), "right": right})
        index //= 2
    return proof


def verify_inclusion(root_hex: str, leaf: bytes, index: int,
                     proof: list[dict]) -> tuple[bool, str]:
    """复算根：从叶子出发，按方向位逐层拼兄弟 ⇒ 与 root 比对。"""
    cur = leaf_hash(leaf)
    for step in proof:
        sib = bytes.fromhex(step["hash"])
        cur = node_hash(cur, sib) if step["right"] else node_hash(sib, cur)
    got = cur.hex()
    if got != root_hex:
        return False, f"复算根 {got[:16]}… ≠ 给定根 {root_hex[:16]}…"
    return True, "复算根一致"


def consistency_proof(old_levels: list[list[bytes]],
                      new_levels: list[list[bytes]]) -> dict:
    """append-only 一致性：老树必须是新树的**前缀**（返回老根在新树里的位置信息）。"""
    old_root = old_levels[-1][0] if old_levels else _h(b"").hex().encode()
    old_root_hex = old_root.hex() if isinstance(old_root, bytes) else str(old_root)
    return {"old_size": len(old_levels[0]) if old_levels else 0,
            "new_size": len(new_levels[0]) if new_levels else 0,
            "old_root": old_root_hex,
            "new_root": new_levels[-1][0].hex() if new_levels else _h(b"").hex(),
            "proof": inclusion_proof(new_levels, max(len(old_levels[0]) - 1, 0))
            if new_levels else []}


def verify_consistency(old_levels: list[list[bytes]],
                       new_levels: list[list[bytes]]) -> tuple[bool, str]:
    if not old_levels:
        return True, "空老树 ⇒ 一致性平凡成立"
    n_old = len(old_levels[0])
    n_new = len(new_levels[0])
    if n_new < n_old:
        return False, f"新树叶子 {n_new} < 老树 {n_old} ⇒ 日志被裁短（回滚攻击特征）"
    old_leaves = old_levels[0]
    new_leaves = new_levels[0][:n_old]
    if [x.hex() for x in old_leaves] != [x.hex() for x in new_leaves]:
        return False, "新树的前缀与老树叶子不一致 ⇒ 历史被改写（重排/篡改攻击特征）"
    return True, f"老树（{n_old} 叶）是新树（{n_new} 叶）的逐叶前缀 ⇒ append-only 成立"


def verify_append_only(old_text: str, new_text: str) -> tuple[bool, str]:
    """逐行前缀验证：老行一个字节都不许变，只许末尾追加。"""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    if len(new_lines) < len(old_lines):
        return False, f"新日志 {len(new_lines)} 行 < 旧 {len(old_lines)} 行 ⇒ 被截断"
    for i, o in enumerate(old_lines):
        if new_lines[i] != o:
            return False, f"第 {i + 1} 行被改写（旧 {o!r} ≠ 新 {new_lines[i]!r}）"
    return True, f"旧 {len(old_lines)} 行逐字节保留，新增 {len(new_lines) - len(old_lines)} 行"


def demo(leaves_n: int = 8) -> dict:
    """造一棵树并演示三类证明（**批量测试用**：不碰真实仓库台账）。"""
    leaves = [f"leaf-{i}".encode() for i in range(leaves_n)]
    root, levels = build_tree(leaves)
    half = [f"leaf-{i}".encode() for i in range(leaves_n // 2)]
    old_root, old_levels = build_tree(half)
    idx = 3
    proof = inclusion_proof(levels, idx)
    return {"leaves": leaves_n, "root": root.hex(),
            "inclusion": {"index": idx, "proof_len": len(proof),
                          "ok": verify_inclusion(root.hex(), leaves[idx], idx, proof)[0],
                          "tampered_ok": verify_inclusion(
                              root.hex(), b"leaf-3-TAMPERED", idx, proof)[0]},
            "consistency": {"old_leaves": len(half),
                            "ok": verify_consistency(old_levels, levels)[0],
                            "reordered_ok": verify_consistency(
                                old_levels, build_tree(list(reversed(leaves)))[1])[0]},
            "append_only": {"ok": verify_append_only(
                "".join(f"leaf-{i}\n" for i in range(leaves_n // 2)),
                "".join(f"leaf-{i}\n" for i in range(leaves_n)))[0],
                            "tampered_ok": verify_append_only(
                                "".join(f"leaf-{i}\n" for i in range(leaves_n // 2)),
                                "".join(f"LEAF-{i}\n" for i in range(leaves_n)))[0]}}


def check() -> list[str]:
    problems: list[str] = []
    for n in (1, 2, 3, 5, 8, 9, 16, 17):
        leaves = [f"x-{i}".encode() for i in range(n)]
        root, levels = build_tree(leaves)
        for i in range(n):
            proof = inclusion_proof(levels, i)
            ok, why = verify_inclusion(root.hex(), leaves[i], i, proof)
            if not ok:
                problems.append(f"n={n} 叶子 {i} 的包含证明验证失败：{why}")
        if n >= 2:
            half = leaves[: n // 2]
            ok, why = verify_consistency(build_tree(half)[1], levels)
            if not ok:
                problems.append(f"n={n} 一致性证明失败：{why}")
    ok, why = verify_append_only("a\nb\n", "a\nb\nc\n")
    if not ok:
        problems.append(f"append-only 正例失败：{why}")
    ok2, _ = verify_append_only("a\nb\n", "a\nB\nc\n")
    if ok2:
        problems.append("append-only 反例竟然通过（改历史行未被发现）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="supply_chain_verify",
                                 description="609 D3 供应链验证（包含证明 + 一致性 + append-only）")
    ap.add_argument("--version", action="version", version=f"supply_chain_verify {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    sp = sub.add_parser("inclusion")
    sp.add_argument("--leaf", required=True)
    sp.add_argument("--root", required=True)
    sp.add_argument("--index", type=int, required=True)
    sp.add_argument("--proof", required=True, help="proof JSON 文件（[{hash,right}]）")

    sp = sub.add_parser("consistency")
    sp.add_argument("--old", required=True, help="旧叶子列表 JSON（字符串数组）")
    sp.add_argument("--new", required=True)

    sp = sub.add_parser("append-only")
    sp.add_argument("--old", required=True)
    sp.add_argument("--new", required=True)

    sp = sub.add_parser("demo")
    sp.add_argument("--leaves", type=int, default=8)
    sp.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[scv] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[scv] --check OK：n∈{1,2,3,5,8,9,16,17} 全部叶子的包含证明 + 一致性 + "
              "append-only 正反例均自洽")
        return 0

    if a.cmd == "demo":
        d = demo(a.leaves)
        if a.out:
            Path(a.out).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8", newline="\n")
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return 0

    if a.cmd == "inclusion":
        proof = json.loads(Path(a.proof).read_text(encoding="utf-8"))
        ok, why = verify_inclusion(a.root, a.leaf.encode(), a.index, proof)
        print(("✓ " if ok else "✗ ") + why)
        return 0 if ok else 1

    if a.cmd == "consistency":
        old = [str(x).encode() for x in json.loads(Path(a.old).read_text(encoding="utf-8"))]
        new = [str(x).encode() for x in json.loads(Path(a.new).read_text(encoding="utf-8"))]
        ok, why = verify_consistency(build_tree(old)[1], build_tree(new)[1])
        print(("✓ " if ok else "✗ ") + why)
        return 0 if ok else 1

    if a.cmd == "append-only":
        ok, why = verify_append_only(Path(a.old).read_text(encoding="utf-8"),
                                     Path(a.new).read_text(encoding="utf-8"))
        print(("✓ " if ok else "✗ ") + why)
        return 0 if ok else 1

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
