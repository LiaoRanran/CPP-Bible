"""628 B2 · VSA 凭证验证器——他验三件套 #2 的独立验证端

读取 VSA 凭证：
1. 重算 HMAC 与凭证 attestation 对比（签名有效）
2. 凭证 input_hashes 与当前文件重算哈希对比（输入未漂移）
3. 凭证 results 与当前独立重算结果对比（结论未漂移）
`--check`：验证最近一张凭证有效。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import vsa_attestation_628 as V  # noqa: E402


def verify_latest() -> dict:
    p = V.latest_credential()
    if not p:
        return {"valid": False, "error": "no credential found"}
    return V.verify_credential(p)


def verify_all() -> list[dict]:
    vsa_dir = V.VSA_DIR
    out: list[dict] = []
    if not os.path.isdir(vsa_dir):
        return out
    for name in sorted(os.listdir(vsa_dir)):
        if name.startswith("attestation_") and name.endswith(".json"):
            out.append(V.verify_credential(os.path.join(vsa_dir, name)))
    return out


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    p = V.latest_credential()
    chk("存在至少一张凭证", p is not None)
    if p:
        r = V.verify_credential(p)
        chk("最近凭证 HMAC 有效", r["hmac_valid"])
        chk("最近凭证输入哈希有效", r["input_hashes_valid"])
        chk("最近凭证结果有效", r["results_valid"])
        chk("凭证整体有效", r["valid"])
        allr = verify_all()
        chk("全部凭证签名有效", all(x["hmac_valid"] for x in allr),
            f"({len(allr)} 张)")
    print(f"B2 verify check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B2 VSA 验证器")
    ap.add_argument("--check", action="store_true", help="自检（验证最近凭证）")
    ap.add_argument("--all", action="store_true", help="验证全部凭证")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.all:
        print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(verify_latest(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
