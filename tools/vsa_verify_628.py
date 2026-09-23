"""628 B2 · VSA 凭证**独立验证端**——他验三件套 #2 的验证侧

设计要点：**零 import 本项目工具**（含**不 import 签发端** `vsa_attestation_628`）。
验证端自己重实现全部校验逻辑，只依赖标准库与凭证文件本身：

1. 重算 HMAC-SHA256 与凭证 `attestation` 对比 —— 签名有效（密钥读 `data/vsa_secret.key`）
2. 重算 ledger / grounded_labels / PCK 目录摘要，与凭证 `input_hashes` 对比 —— 输入未漂移
3. 子进程运行 `independent_verifier_628.py`，与凭证 `results` 对比 —— 结论未漂移

若验证端直接 import 签发端，则"签发代码写错"会同时让验证端也写错（同源耦合），
独立性就只是名义上的。

`--check`：验证日志在册的最新凭证 + 全部凭证签名有效（只读，不写任何文件）。
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
SECRET = os.path.join(ROOT, "data", "vsa_secret.key")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
LOG = os.path.join(ROOT, "data", "transparency_log.jsonl")
VERIFIER = os.path.join(HERE, "independent_verifier_628.py")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _dir_digest(path: str) -> str:
    lines = []
    for name in sorted(os.listdir(path)):
        fp = os.path.join(path, name)
        if os.path.isfile(fp):
            lines.append(f"{name}:{_sha256_file(fp)}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _read_key() -> Optional[bytes]:
    """读密钥；**缺失即返回 None，绝不新建**（新建密钥会让历史凭证假失败）。"""
    if os.path.exists(SECRET):
        with open(SECRET, "rb") as fh:
            return fh.read()
    return None


def _hmac_of(cred: dict, key: bytes) -> str:
    """按凭证格式独立重实现：除 attestation 外全字段、sort_keys、utf-8。"""
    payload = {k: v for k, v in cred.items() if k != "attestation"}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hmac.new(key, blob, hashlib.sha256).hexdigest()


def current_input_hashes() -> dict:
    return {"ledger_sha256": _sha256_file(LEDGER),
            "grounded_labels_sha256": _sha256_file(GROUNDED),
            "pck_dir_sha256": _dir_digest(CERT_DIR)}


def independent_results() -> dict:
    """子进程跑 B1 独立验证者；验证端不复用其代码，只取结论。"""
    p = subprocess.run([sys.executable, VERIFIER], capture_output=True, text=True,
                       cwd=ROOT, timeout=300, check=False)
    iv = json.loads(p.stdout.strip().splitlines()[-1])
    return {"w2_in": iv["w2"]["summary"]["IN"],
            "w2_out": iv["w2"]["summary"]["OUT"],
            "w2_undec": iv["w2"]["summary"]["UNDEC"],
            "pck_authorized": iv["pck"]["authorized"],
            "ledger_hash_chain": ("valid" if iv["ledger_chain"]["chain_valid"]
                                  else "BROKEN"),
            "unique_review_items": iv["unique"]["unique"]}


def verify(path: str) -> dict:
    """独立验证一张凭证：签名 / 输入锚定 / 结论，三者全过才算有效。"""
    with open(path, encoding="utf-8") as fh:
        cred = json.load(fh)
    key = _read_key()
    res = {"path": os.path.relpath(path, ROOT), "verifier_id": cred.get("verifier_id"),
           "verified_at": cred.get("verified_at"), "key_present": key is not None,
           "hmac_valid": False, "input_hashes_valid": False, "results_valid": False}
    if key is None:
        res["error"] = "secret key not found（不入库；缺密钥时无法验证 HMAC）"
        res["valid"] = False
        return res
    res["hmac_valid"] = hmac.compare_digest(str(cred.get("attestation", "")),
                                            _hmac_of(cred, key))
    cur = current_input_hashes()
    res["input_hashes_valid"] = all(cred.get("input_hashes", {}).get(k) == v
                                    for k, v in cur.items())
    res["results_valid"] = cred.get("results") == independent_results()
    res["valid"] = bool(res["hmac_valid"] and res["input_hashes_valid"]
                        and res["results_valid"])
    return res


def credentials() -> list:
    if not os.path.isdir(VSA_DIR):
        return []
    return [os.path.join(VSA_DIR, f) for f in sorted(os.listdir(VSA_DIR))
            if f.startswith("attestation_") and f.endswith(".json")]


def logged_credentials() -> list:
    """日志在册的凭证路径（按登记顺序）。"""
    if not os.path.exists(LOG):
        return []
    out = []
    for line in open(LOG, encoding="utf-8"):
        if line.strip():
            e = json.loads(line)
            out.append(os.path.join(ROOT, str(e.get("vsa_file", ""))))
    return out


def verify_all() -> list:
    return [verify(p) for p in credentials()]


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("零 import 本项目工具（含不 import 签发端）", not _project_imports(),
        f"({_project_imports()})")
    creds = credentials()
    chk("存在至少一张凭证", bool(creds), f"({len(creds)} 张)")
    if creds:
        allr = verify_all()
        chk("全部凭证 HMAC 签名有效", all(r["hmac_valid"] for r in allr),
            f"({len(allr)} 张)")
        chk("全部凭证输入哈希锚定有效", all(r["input_hashes_valid"] for r in allr))
        chk("全部凭证结论与独立重算一致", all(r["results_valid"] for r in allr))
        # 篡改探测：改一个数字后签名必须失败
        c = json.load(open(creds[-1], encoding="utf-8"))
        key = _read_key()
        if key:
            tampered = dict(c, results=dict(c["results"], w2_in=999))
            chk("篡改结果后签名验证失败",
                not hmac.compare_digest(str(tampered.get("attestation", "")),
                                        _hmac_of(tampered, key)))
        # 日志在册凭证（尾部）必须有效
        logged = logged_credentials()
        if logged:
            tail = logged[-1]
            chk("日志尾部凭证存在", os.path.exists(tail),
                f"({os.path.relpath(tail, ROOT)})")
            if os.path.exists(tail):
                chk("日志尾部凭证验证通过", verify(tail)["valid"])
    print(f"B2 verify check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _project_imports() -> list:
    """静态自检：本文件 import 的项目工具模块（应为空）。"""
    import re
    local = {os.path.splitext(f)[0] for f in os.listdir(HERE) if f.endswith(".py")}
    found = []
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)", line.strip())
            if m and m.group(1) in local:
                found.append(m.group(1))
    return sorted(set(found))


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B2 VSA 独立验证端")
    ap.add_argument("--check", action="store_true", help="自检（验证在册凭证）")
    ap.add_argument("--all", action="store_true", help="验证全部凭证")
    ap.add_argument("--path", metavar="CRED", help="验证指定凭证文件")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.all:
        print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
        return 0
    if args.path:
        r = verify(args.path)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["valid"] else 1
    logged = logged_credentials()
    if not logged:
        print(json.dumps({"valid": False, "error": "no logged credential"},
                         ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(verify(logged[-1]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
