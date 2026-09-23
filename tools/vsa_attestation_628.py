"""628 B2 · VSA 验证凭证（Verification Statement Attestation）—— 他验三件套 #2

为 B1 独立验证结果生成可验证凭证：
- 凭证 JSON：vsa_version / verifier_id / verifier_sha256（验证者脚本自身哈希）/
  verified_at / input_hashes（ledger、grounded、PCK 目录摘要）/ results / attestation
- attestation = HMAC-SHA256(上述全部字段)，密钥 `data/vsa_secret.key`
  **不入库**（已加入 .gitignore）
- 凭证写入 `data/vsa/attestation_<timestamp>.json`
- `--check`：验证已有凭证的 HMAC 签名有效

**诚实局限**（写入报告）：HMAC 只能证明"持有密钥的主体生成了凭证"，
不能证明"独立主体认可"——真正的独立性需非对称签名 + 独立密钥托管，留后续批次。
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
SECRET = os.path.join(ROOT, "data", "vsa_secret.key")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
OUT_MD = os.path.join(ROOT, "data", "vsa_attestation_report_628.md")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def dir_digest(path: str) -> str:
    """目录摘要（简单 Merkle 式）：对排序后的 `name:sha256` 行串联再 sha256。"""
    lines = []
    for name in sorted(os.listdir(path)):
        fp = os.path.join(path, name)
        if os.path.isfile(fp):
            lines.append(f"{name}:{_sha256_file(fp)}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def load_or_create_key() -> bytes:
    if os.path.exists(SECRET):
        return open(SECRET, "rb").read()
    key = hashlib.sha256(os.urandom(32)).digest()
    with open(SECRET, "wb") as fh:
        fh.write(key)
    return key


def compute_attestation(cred: dict[str, Any], key: bytes) -> str:
    payload = {k: v for k, v in cred.items() if k != "attestation"}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hmac.new(key, blob, hashlib.sha256).hexdigest()


def build_credential() -> dict[str, Any]:
    """运行 B1 独立验证者（子进程，保持验证者独立），以其输出构建凭证。"""
    import subprocess
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "independent_verifier_628.py")],
        capture_output=True, text=True, cwd=ROOT, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(f"independent verifier failed: {proc.stderr[-300:]}")
    iv = json.loads(proc.stdout.strip().splitlines()[-1])
    cred: dict[str, Any] = {
        "vsa_version": "1.0",
        "verifier_id": "independent_verifier_628",
        "verifier_sha256": _sha256_file(os.path.join(HERE,
                                                     "independent_verifier_628.py")),
        "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "input_hashes": {
            "ledger_sha256": _sha256_file(LEDGER),
            "grounded_labels_sha256": _sha256_file(GROUNDED),
            "pck_dir_sha256": dir_digest(CERT_DIR),
        },
        "results": {
            "w2_in": iv["w2"]["summary"]["IN"],
            "w2_out": iv["w2"]["summary"]["OUT"],
            "w2_undec": iv["w2"]["summary"]["UNDEC"],
            "pck_authorized": iv["pck"]["authorized"],
            "ledger_hash_chain": ("valid" if iv["ledger_chain"]["chain_valid"]
                                  else "BROKEN"),
            "unique_review_items": iv["unique"]["unique"],
        },
    }
    cred["attestation"] = compute_attestation(cred, load_or_create_key())
    return cred


def save_credential(cred: dict[str, Any], out_dir: Optional[str] = None) -> str:
    """写入凭证。`out_dir` 默认生产目录；同名冲突加序号后缀（同秒多次生成不互相覆盖）。"""
    d = out_dir or VSA_DIR
    os.makedirs(d, exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = os.path.join(d, f"attestation_{ts}.json")
    n = 2
    while os.path.exists(path):
        path = os.path.join(d, f"attestation_{ts}_{n}.json")
        n += 1
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cred, fh, ensure_ascii=False, indent=2)
    return path


def verify_credential(path: str, key: Optional[bytes] = None) -> dict:
    """验证凭证：HMAC 签名 + 输入哈希与当前文件一致 + 结果与当前独立重算一致。

    **不自动新建密钥**：密钥缺失时直接判无效（否则新建密钥会让历史凭证"假失败"，
    把"密钥丢失"误报成"签名被篡改"）。
    """
    cred = json.load(open(path, encoding="utf-8"))
    if key is None and os.path.exists(SECRET):
        key = open(SECRET, "rb").read()
    if key is None:
        return {"path": os.path.relpath(path, ROOT), "hmac_valid": False,
                "input_hashes_valid": False, "results_valid": False, "valid": False,
                "verifier_id": cred.get("verifier_id"),
                "verified_at": cred.get("verified_at"),
                "error": "secret key not found（data/vsa_secret.key 不入库，缺失时无法验证 HMAC）"}
    att_ok = hmac.compare_digest(cred.get("attestation", ""),
                                 compute_attestation(cred, key))
    cur_hashes = {
        "ledger_sha256": _sha256_file(LEDGER),
        "grounded_labels_sha256": _sha256_file(GROUNDED),
        "pck_dir_sha256": dir_digest(CERT_DIR),
    }
    inputs_ok = all(cred.get("input_hashes", {}).get(k) == v
                    for k, v in cur_hashes.items())
    # 结果与当前独立重算对比
    import subprocess
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "independent_verifier_628.py")],
        capture_output=True, text=True, cwd=ROOT, timeout=120)
    iv = json.loads(proc.stdout.strip().splitlines()[-1])
    cur_results = {
        "w2_in": iv["w2"]["summary"]["IN"],
        "w2_out": iv["w2"]["summary"]["OUT"],
        "w2_undec": iv["w2"]["summary"]["UNDEC"],
        "pck_authorized": iv["pck"]["authorized"],
        "ledger_hash_chain": ("valid" if iv["ledger_chain"]["chain_valid"]
                              else "BROKEN"),
        "unique_review_items": iv["unique"]["unique"],
    }
    results_ok = cred.get("results") == cur_results
    return {"path": os.path.relpath(path, ROOT), "hmac_valid": bool(att_ok),
            "input_hashes_valid": inputs_ok, "results_valid": results_ok,
            "valid": att_ok and inputs_ok and results_ok,
            "verifier_id": cred.get("verifier_id"),
            "verified_at": cred.get("verified_at")}


def latest_credential() -> Optional[str]:
    if not os.path.isdir(VSA_DIR):
        return None
    files = sorted(f for f in os.listdir(VSA_DIR)
                   if f.startswith("attestation_") and f.endswith(".json"))
    return os.path.join(VSA_DIR, files[-1]) if files else None


def _listed() -> list[str]:
    return sorted(f for f in os.listdir(VSA_DIR)
                  if f.startswith("attestation_")) if os.path.isdir(VSA_DIR) else []


def selftest() -> int:
    """自检**只读生产凭证目录**：新凭证写临时目录，验证生产目录里的最新凭证。"""
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import tempfile
    before = _listed()
    with tempfile.TemporaryDirectory() as td:
        path = save_credential(build_credential(), out_dir=td)
        chk("凭证已生成（含 attestation）", os.path.exists(path))
        cred = json.load(open(path, encoding="utf-8"))
        chk("凭证格式字段齐全",
            all(k in cred for k in ("vsa_version", "verifier_id", "verifier_sha256",
                                    "verified_at", "input_hashes", "results",
                                    "attestation")))
        r = verify_credential(path)
        chk("HMAC 签名验证通过", r["hmac_valid"])
        chk("输入哈希锚定验证通过", r["input_hashes_valid"])
        chk("结果与当前独立重算一致", r["results_valid"])
        # 篡改凭证 ⇒ HMAC 失败
        bad = dict(cred)
        bad["results"] = dict(cred["results"], w2_in=999)
        key = load_or_create_key()
        bad_ok = hmac.compare_digest(bad.get("attestation", ""),
                                     compute_attestation(bad, key))
        chk("篡改凭证后 HMAC 验证失败", not bad_ok)
        # 同秒重复生成不覆盖（文件名冲突加序号）
        p2 = save_credential(build_credential(), out_dir=td)
        chk("同秒重复生成不覆盖（冲突加序号）", p2 != path and os.path.exists(p2))
    chk("--check 不污染生产凭证目录", _listed() == before, f"({len(before)} 张)")
    # 生产目录里的最新凭证仍应有效（验证端契约）
    latest = latest_credential()
    if latest:
        chk("生产最新凭证验证通过", verify_credential(latest)["valid"],
            f"({os.path.basename(latest)})")
    # 密钥不入库
    gi = os.path.join(ROOT, ".gitignore")
    gi_txt = open(gi, encoding="utf-8").read() if os.path.exists(gi) else ""
    chk("密钥文件已加入 .gitignore", "vsa_secret.key" in gi_txt)
    print(f"B2 VSA check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B2 VSA 凭证")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--generate", action="store_true", help="生成新凭证")
    ap.add_argument("--verify", action="store_true", help="验证最近凭证")
    ap.add_argument("--verify-path", metavar="CRED", help="验证指定凭证文件")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.generate:
        print(f"written {save_credential(build_credential())}")
        return 0
    if args.report:
        # 报告**只读**：针对最新已有凭证，不新签（新签会产生未入册凭证，破坏一致性）
        path = latest_credential()
        if not path:
            print("no credential")
            return 1
        r = verify_credential(path)
        cred = json.load(open(path, encoding="utf-8"))
        lines = [
            "# 628 B2 · VSA 验证凭证报告（他验三件套 #2）", "",
            f"- 凭证：`{os.path.relpath(path, ROOT)}`（{cred['verified_at']}）",
            f"- HMAC 验证：{r['hmac_valid']} · 输入哈希锚定：{r['input_hashes_valid']}"
            f" · 结果一致：{r['results_valid']}",
            f"- verifier_sha256：`{cred['verifier_sha256'][:16]}…`"
            "（凭证可追溯到验证者脚本版本）",
            "- input_hashes：ledger/grounded/PCK 目录三重锚定（凭证绑定输入版本）",
            "",
            "## 与 Sigstore/Rekor 的对比", "",
            "- 本项目用 **HMAC-SHA256**（对称）：单用户阶段无独立密钥托管，"
            "非对称签名的私钥仍在同一主体手中，无法制造独立性。",
            "- **诚实局限**：HMAC 只能证明「持有密钥的主体生成了凭证」，"
            "不能证明「独立主体认可」——真正的独立性需非对称签名 + 独立密钥托管，留后续批次。",
            "- 密钥 `data/vsa_secret.key` **不入库**（.gitignore）。",
        ]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
        return 0
    if args.verify_path:
        if not os.path.exists(args.verify_path):
            print(json.dumps({"valid": False, "error": "not found"},
                             ensure_ascii=False))
            return 1
        r = verify_credential(args.verify_path)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["valid"] else 1
    if args.verify:
        p = latest_credential()
        if not p:
            print("no credential")
            return 1
        print(json.dumps(verify_credential(p), ensure_ascii=False, indent=2))
        return 0
    print("用法：--check | --generate | --verify [--verify-path CRED] | --report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
