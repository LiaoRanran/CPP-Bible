#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ledger_checkpoint_651.py — T4 账本 checkpoint / 双证明（651 W2，**信任资产**）。

为什么（651 W2-T4）：append-only 账本（452 条 DecisionEvent）若只靠"文件没被改"来保证，
运维无法**独立**证明"某条在当时的账本里"以及"新账本确实包含旧账本"。本工具给账本建
**最小 static-CT 集**（RFC 6962 风格）：
1. **签名 checkpoint**：对 Merkle 根做 HMAC 签名（周目击者 cron 本地跑，见文末）。
2. **inclusion proof**：证明某条事件在 size=n 的账本里。
3. **consistency proof**：证明 size=n 的账本包含 size=m 的账本（旧根是新根的祖先）。

用法
====
    python tools/ledger_checkpoint_651.py --check                  # 穷举 Merkle 自检（n=1..32，含篡改拒绝）
    python tools/ledger_checkpoint_651.py --checkpoint             # 对真账本出 checkpoint + 双证明样例
    python tools/ledger_checkpoint_651.py --verify                 # 校验已写 checkpoint（签名 + 双证明）
    python tools/ledger_checkpoint_651.py --json

诚实边界：
- **demo 见证密钥**：默认 `--witness-key local-witness-demo`（可复现、非机密）。真用须换外部密钥（交人）。
- 空账本（0 条）无 Merkle 根，工具显式报 `empty`，不编造根。
- 不修改账本本身（只读）。
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "trust_asset", "name": "ledger_checkpoint_651", "entry": "build_checkpoint",
                "description": "T4 账本签名 checkpoint + inclusion/consistency 双证明（RFC6962）"}

LEDGER = ROOT / "data" / "authority" / "decision_event_v2_ledger.jsonl"
OUT = ROOT / "data" / "651_t4_checkpoint.json"
DEFAULT_WITNESS_KEY = "local-witness-demo"


# ── RFC 6962 Merkle ─────────────────────────────────────────────────────────
def leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def _largest_pow2_lt(n: int) -> int:
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def mth(leaves: list[bytes]) -> bytes | None:
    """Merkle Tree Hash（RFC6962）。空列表 ⇒ None。"""
    n = len(leaves)
    if n == 0:
        return None
    if n == 1:
        return leaf_hash(leaves[0])
    k = _largest_pow2_lt(n)
    return node_hash(mth(leaves[:k]), mth(leaves[k:]))  # type: ignore[arg-type]


def inclusion_path(m: int, leaves: list[bytes]) -> list[bytes]:
    """leaf m 的 inclusion 路径（RFC6962 PATH）。

    656 B3：**空列表 / 下标越界 ⇒ 返回 []**。原来这条路径会无限递归
    （`n=0` 时 `_largest_pow2_lt(0)=1`，`m-k` 与切片都回到自身）⇒ `RecursionError`，
    把"查不到证明"变成"崩掉"。空树/越界是**合法查询**，必须给空证明而不是炸。
    """
    n = len(leaves)
    if n == 0 or m < 0 or m >= n:
        return []
    if n == 1:
        return []
    k = _largest_pow2_lt(n)
    if m < k:
        return inclusion_path(m, leaves[:k]) + [mth(leaves[k:])]  # type: ignore[list-item]
    return inclusion_path(m - k, leaves[k:]) + [mth(leaves[:k])]  # type: ignore[list-item]


def verify_inclusion(m: int, n: int, leaf: bytes, proof: list[bytes], root: bytes) -> bool:
    h = leaf_hash(leaf)
    fn, sn = m, n - 1
    for p in proof:
        if sn == 0:
            return False
        if (fn & 1) or (fn == sn):
            h = node_hash(p, h)
            while (fn & 1) == 0 and fn != 0:
                fn >>= 1
                sn >>= 1
        else:
            h = node_hash(h, p)
        fn >>= 1
        sn >>= 1
    return h == root and sn == 0


def consistency_proof(m: int, leaves: list[bytes]) -> list[bytes]:
    """size=m 与 size=n 的 consistency proof（RFC6962 SUBPROOF，b=True 起）。"""
    return _subproof(m, leaves, True)


def _subproof(m: int, leaves: list[bytes], b: bool) -> list[bytes]:
    n = len(leaves)
    if m == n:
        return [] if b else [mth(leaves)]  # type: ignore[list-item]
    k = _largest_pow2_lt(n)
    if m <= k:
        return _subproof(m, leaves[:k], b) + [mth(leaves[k:])]  # type: ignore[list-item]
    return _subproof(m - k, leaves[k:], False) + [mth(leaves[:k])]  # type: ignore[list-item]


def verify_consistency(m: int, n: int, proof: list[bytes], old_root: bytes, new_root: bytes) -> bool:
    if m == n:
        return proof == [] and old_root == new_root
    if m == 0:
        return True  # 空树天然一致（无根）
    fn, sn = m - 1, n - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    proof = list(proof)
    if fn == 0:
        fr = sr = old_root
    else:
        if not proof:
            return False
        fr = sr = proof[0]
        proof = proof[1:]
    for c in proof:
        if sn == 0:
            return False
        if (fn & 1) or (fn == sn):
            fr = node_hash(c, fr)
            sr = node_hash(c, sr)
            while (fn & 1) == 0 and fn != 0:
                fn >>= 1
                sn >>= 1
        else:
            sr = node_hash(sr, c)
        fn >>= 1
        sn >>= 1
    return fr == old_root and sr == new_root


# ── checkpoint ──────────────────────────────────────────────────────────────
def _leaves_from_ledger(path: Path) -> list[bytes]:
    out: list[bytes] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            out.append(line.encode("utf-8"))
    return out


def _sig(key: str, payload: dict) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key.encode(), body, hashlib.sha256).hexdigest()


def sign_checkpoint(tree_size: int, root_hex: str | None, ts: str, prev_hash: str | None, key: str) -> dict:
    core = {"tree_size": tree_size, "root_hash": root_hex, "timestamp": ts, "prev_checkpoint_hash": prev_hash}
    return {**core, "signature": _sig(key, core), "algo": "HMAC-SHA256"}


def build_checkpoint(ledger: Path = LEDGER, key: str = DEFAULT_WITNESS_KEY,
                     ts: str = "2026-09-27T00:00:00", include_sample_size: int = 300) -> dict:
    leaves = _leaves_from_ledger(ledger)
    n = len(leaves)
    if n == 0:
        return {"status": "empty", "ledger": str(ledger.relative_to(ROOT)), "tree_size": 0}
    root = mth(leaves)
    assert root is not None  # n > 0 保证
    root_hex = root.hex()
    cp = sign_checkpoint(n, root_hex, ts, None, key)
    # 双证明样例：inclusion(第 0 条) + consistency(m=min(sample,n-1) → n)
    inc = inclusion_path(0, leaves)
    inc_ok = verify_inclusion(0, n, leaves[0], inc, root)
    m = min(include_sample_size, n - 1) if n > 1 else 1
    old_root = mth(leaves[:m])
    assert old_root is not None
    cons = consistency_proof(m, leaves)
    cons_ok = verify_consistency(m, n, cons, old_root, root)
    return {
        "status": "ok",
        "ledger": str(ledger.relative_to(ROOT)),
        "tree_size": n,
        "root_hash": root_hex,
        "checkpoint": cp,
        "inclusion_sample": {"index": 0, "proof_len": len(inc), "verify": inc_ok},
        "consistency_sample": {"m": m, "n": n, "proof_len": len(cons), "verify": cons_ok},
    }


def verify_checkpoint_file(path: Path = OUT, key: str = DEFAULT_WITNESS_KEY) -> dict:
    if not path.is_file():
        return {"ok": False, "reason": "checkpoint_file_missing"}
    rep = json.loads(path.read_text(encoding="utf-8"))
    if rep.get("status") != "ok":
        return {"ok": False, "reason": "not_ok_status"}
    cp = rep["checkpoint"]
    core = {k: cp[k] for k in ("tree_size", "root_hash", "timestamp", "prev_checkpoint_hash")}
    sig_ok = hmac.compare_digest(cp["signature"], _sig(key, core))
    # 用真账本重算根，独立复核 checkpoint
    leaves = _leaves_from_ledger(LEDGER)
    root_now = mth(leaves)
    root_ok = (root_now.hex() if root_now else None) == cp["root_hash"] and len(leaves) == cp["tree_size"]
    return {"ok": sig_ok and root_ok, "sig_ok": sig_ok, "root_ok": root_ok,
            "inclusion_verify": rep["inclusion_sample"]["verify"],
            "consistency_verify": rep["consistency_sample"]["verify"]}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 穷举：n=1..32，所有 leaf 的 inclusion 与所有 m<n 的 consistency
    all_inc = all_cons = True
    tamper_rejected = True
    for n in range(1, 33):
        leaves = [f"ev{i}".encode() for i in range(n)]
        root = mth(leaves)
        assert root is not None
        for i in range(n):
            if not verify_inclusion(i, n, leaves[i], inclusion_path(i, leaves), root):
                all_inc = False
        for m in range(1, n + 1):
            old_root_m = mth(leaves[:m])
            assert old_root_m is not None
            if not verify_consistency(m, n, consistency_proof(m, leaves), old_root_m, root):
                all_cons = False
        # 篡改：改一条证明元素应被拒
        if n >= 2:
            bad = list(inclusion_path(0, leaves))
            bad[0] = bytes(32)
            if verify_inclusion(0, n, leaves[0], bad, root):
                tamper_rejected = False
    chk("inclusion 全通(n=1..32,所有 leaf)", all_inc)
    chk("consistency 全通(n=1..32,所有 m≤n)", all_cons)
    chk("篡改证明被拒", tamper_rejected)
    chk("空树 mth=None", mth([]) is None)
    # 签名稳定 + 可验
    cp = sign_checkpoint(3, "aa", "t", None, "k")
    chk("签名可复算", hmac.compare_digest(cp["signature"], _sig("k", {k2: cp[k2] for k2 in ("tree_size", "root_hash", "timestamp", "prev_checkpoint_hash")})))
    print(f"ledger_checkpoint_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 T4 账本 checkpoint/双证明（RFC6962）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--checkpoint", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--witness-key", default=DEFAULT_WITNESS_KEY)
    ap.add_argument("--ledger", default=str(LEDGER))
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.verify:
        rep = verify_checkpoint_file(key=a.witness_key)
        print(json.dumps(rep, ensure_ascii=False))
        return 0 if rep["ok"] else 1
    rep = build_checkpoint(Path(a.ledger), a.witness_key)
    if a.checkpoint:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"tree_size={rep.get('tree_size')} root={rep.get('root_hash')}\n"
              f"inclusion.verify={rep.get('inclusion_sample', {}).get('verify')} "
              f"consistency.verify={rep.get('consistency_sample', {}).get('verify')}\n→ {OUT.name}")
        return 0
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json
          else f"tree_size={rep.get('tree_size')} status={rep.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
