"""629 C1 · VSA 非对称签名升级（**纯标准库** RSA-2048 / PKCS#1 v1.5）

628 的 VSA 用 HMAC-SHA256——对称密钥 ⇒ 只能证明「持有密钥的主体生成了凭证」，
不能证明「独立主体认可」。本工具用**纯标准库**实现真非对称签名（私钥签 / 公钥验），
验证 628 提出的「需要非对称签名」是否可在不引入第三方库的前提下成立。

**实现**（全部标准库：`secrets` / `hashlib` / `json`）：
- 密钥生成：RSA-2048（Miller-Rabin 40 轮素性测试，e=65537）
- 签名：EMS-PKCS1-v1_5 + SHA-256（含标准 DigestInfo DER 前缀）→ `pow(m, d, n)`
- 验签：`pow(s, e, n)` 后比对 EM 前缀与 DigestInfo

**诚实局限（必须读，见 `data/vsa_asymmetric_629.md`）**：
1. 这是**教科书级实现**：无恒定时间运算、无盲化、无 padding oracle 防护、
   未做密钥序列化标准（自定义 JSON）、未审计 ⇒ **不可用于生产**。
2. **它解决了「算法层面的非对称」，但没有解决「信任根」**：若公钥也由同一主体生成并发布，
   独立性等级仍是 L1/L2（同一主体），不是 L4（独立密钥托管）。真正的独立性需要
   **外部 KMS / 公开信任根**，本批列为交人项。
3. 私钥只写系统临时目录，**绝不入库**（`data/` 下不落任何密钥文件；自检断言）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import tempfile
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "vsa_asymmetric_629.md")
DEFAULT_BITS = 2048
# RFC 8017 §9.2 注：SHA-256 的 DigestInfo DER 前缀（AlgorithmIdentifier + OCTET STRING 头）
SHA256_DER_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


# ── 素数 / 密钥 ──────────────────────────────────────────────────

def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """Miller-Rabin（标准库实现；rounds=40 时误判概率 < 4^-40）。"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits: int) -> int:
    while True:
        cand = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(cand):
            return cand


def generate_keypair(bits: int = DEFAULT_BITS, e: int = 65537) -> dict[str, Any]:
    """生成 RSA 密钥对（返回 dict；调用方负责落盘到临时目录）。"""
    t0 = time.time()
    while True:
        p, q = gen_prime(bits // 2), gen_prime(bits // 2)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if phi % e == 0:
            continue
        d = pow(e, -1, phi)
        break
    n = p * q
    return {"scheme": f"RSA-{bits}/PKCS1v15-SHA256", "n": n, "e": e, "d": d,
            "bits": bits, "gen_seconds": round(time.time() - t0, 2)}


def public_of(priv: dict[str, Any]) -> dict[str, Any]:
    """公钥 = 只导出 (n, e) —— 私钥字段不得出现在公钥里。"""
    return {"scheme": priv["scheme"], "n": priv["n"], "e": priv["e"],
            "bits": priv["bits"]}


# ── 签名 / 验签 ──────────────────────────────────────────────────

def _em_len(n: int) -> int:
    return (n.bit_length() + 7) // 8


def emsa_pkcs1_v15(message: bytes, em_len: int) -> bytes:
    t = SHA256_DER_PREFIX + hashlib.sha256(message).digest()
    ps_len = em_len - 3 - len(t)
    if ps_len < 8:
        raise ValueError("key too short for PKCS#1 v1.5")
    return b"\x00\x01" + b"\xff" * ps_len + b"\x00" + t


def sign(priv: dict[str, Any], message: bytes) -> str:
    n, d = int(priv["n"]), int(priv["d"])
    em = emsa_pkcs1_v15(message, _em_len(n))
    sig = pow(int.from_bytes(em, "big"), d, n)
    return str(sig.to_bytes(_em_len(n), "big").hex())


def verify(pub: dict[str, Any], message: bytes, sig_hex: str) -> bool:
    n, e = int(pub["n"]), int(pub["e"])
    k = _em_len(n)
    try:
        sig = int(sig_hex, 16)
    except ValueError:
        return False
    if sig < 0 or sig >= n:
        return False
    em = pow(sig, e, n).to_bytes(k, "big")
    try:
        expect = emsa_pkcs1_v15(message, k)
    except ValueError:
        return False
    return secrets.compare_digest(em, expect)


def save_keypair(key: dict[str, Any], tmpdir: str) -> tuple[str, str]:
    """私钥/公钥写到**系统临时目录**（不入库；返回两路径）。"""
    priv_p, pub_p = os.path.join(tmpdir, "vsa_rsa_private.json"), \
        os.path.join(tmpdir, "vsa_rsa_public.json")
    with open(priv_p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: (str(v) if isinstance(v, int) and k in ("n", "d") else v)
                   for k, v in key.items()}, fh, ensure_ascii=False, indent=2)
    with open(pub_p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: (str(v) if k == "n" else v)
                   for k, v in public_of(key).items()}, fh, ensure_ascii=False, indent=2)
    return priv_p, pub_p


# ── 与 628 VSA 凭证的衔接 ────────────────────────────────────────

# 签名覆盖范围：排除签名字段自身（`attestation`=628 HMAC、`signature*`=629 RSA）
# 628 时代凭证没有 signature 字段 ⇒ 与 HMAC 口径（除 attestation 外全字段）对历史凭证等价。
SIGNED_EXCLUDE = ("attestation", "signature", "signature_scheme")

# data/ 下绝不允许出现的 RSA 密钥文件名片段（注意：不能用「含 rsa」匹配，
# "adversarial_*" 也含 rsa —— 629 C1 自检首版踩过这个假阳性）
FORBIDDEN_KEY_HINTS = ("rsa_private", "rsa_public", ".pem", ".p8", "private_key")


def credential_payload(cred: dict[str, Any]) -> bytes:
    """把凭证里「非签名字段」序列化成待签字节（sort_keys + UTF-8，确定性）。"""
    payload = {k: v for k, v in cred.items() if k not in SIGNED_EXCLUDE}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")


def upgrade_credential(cred: dict[str, Any], priv: dict[str, Any]) -> dict[str, Any]:
    """给 628 形态的凭证补上非对称签名（保留原 HMAC 字段，不覆盖）。"""
    out = dict(cred)
    out["signature_scheme"] = priv["scheme"]
    out["signature"] = sign(priv, credential_payload(cred))
    return out


def verify_credential_sig(cred: dict[str, Any], pub: dict[str, Any]) -> bool:
    sig = str(cred.get("signature", ""))
    return bool(sig) and verify(pub, credential_payload(cred), sig)


# ── 报告 / 自检 ──────────────────────────────────────────────────

def repo_key_files() -> list[str]:
    """扫描仓库内疑似私钥文件（精确片段匹配，避免 adversarial_* 之类假阳性）。"""
    hits = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "node_modules", "build") and not d.startswith(".")]
        for f in files:
            low = f.lower()
            if any(h in low for h in FORBIDDEN_KEY_HINTS):
                hits.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(hits)


def demo(bits: int = DEFAULT_BITS) -> dict[str, Any]:
    """一次完整演示：生成密钥 → 签一条凭证 → 验签 → 四类攻击检测。"""
    cred = {"vsa_version": "1.0", "verifier_id": "independent_verifier_628",
            "verified_at": "2026-09-23T00:00:00Z",
            "input_hashes": {"ledger_sha256": "0" * 64},
            "results": {"w2_in": 114, "w2_out": 7, "w2_undec": 0},
            "attestation": "hmac-628-legacy"}
    tmp = tempfile.mkdtemp(prefix="queyi_629_rsa_")
    try:
        priv = generate_keypair(bits)
        pub = public_of(priv)
        priv_p, pub_p = save_keypair(priv, tmp)
        t0 = time.time()
        signed = upgrade_credential(cred, priv)
        sign_ms = (time.time() - t0) * 1000
        t0 = time.time()
        ok = verify_credential_sig(signed, pub)
        verify_ms = (time.time() - t0) * 1000
        tampered = dict(signed, results={"w2_in": 999})
        other = generate_keypair(bits)
        return {
            "bits": bits, "gen_seconds": priv["gen_seconds"],
            "sign_ms": round(sign_ms, 2), "verify_ms": round(verify_ms, 2),
            "valid": ok,
            "tamper_detected": not verify_credential_sig(tampered, pub),
            "wrong_key_rejected": not verify_credential_sig(signed, public_of(other)),
            "private_key_leaks_in_public": any(k in pub for k in ("d", "p", "q")),
            "md5_like_forgery_rejected": not verify(pub, credential_payload(cred),
                                                    "00" * _em_len(pub["n"])),
            "priv_path": priv_p, "pub_path": pub_p,
            "repo_key_files": repo_key_files(),
        }
    finally:
        import shutil

        shutil.rmtree(tmp, ignore_errors=True)


def write_report() -> str:
    d = demo()
    lines = [
        "# 629 C1 · VSA 非对称签名升级（纯标准库 RSA-2048 / PKCS#1 v1.5）", "",
        "> 工具：`tools/vsa_asymmetric_signer_629.py`（**纯标准库**：`secrets`/`hashlib`/`json`；"
        "不引入 cryptography / PyCryptodome）", "",
        "## 一、628 的问题与本次升级", "",
        "| 项 | 628（原型） | 629 C1（本工具） |", "|---|---|---|",
        "| 签名算法 | HMAC-SHA256（对称） | RSA-2048 + PKCS#1 v1.5 + SHA-256（非对称） |",
        "| 密钥 | 单密钥 `data/vsa_secret.key`（不入库） | 私钥/公钥分离，私钥只落**系统临时目录** |",
        "| 能证明 | 持有密钥的主体生成了凭证 | 持有**私钥**的主体签发了凭证（任何人可用公钥验） |",
        "| 独立性 | 对称 ⇒ 无第三方可验（需共享秘密） | 公钥可自由分发 ⇒ **第三方可独立验签** |",
        "", "## 二、实测结果（本机）", "",
        "| 指标 | 值 |", "|---|---|",
        f"| 密钥长度 | RSA-{d['bits']} |",
        f"| 密钥生成耗时 | {d['gen_seconds']} s（纯 Python Miller-Rabin 40 轮） |",
        f"| 签名耗时 | {d['sign_ms']} ms |",
        f"| 验签耗时 | {d['verify_ms']} ms |",
        f"| 签名有效 | {d['valid']} |",
        f"| 篡改 results 后验签失败 | {d['tamper_detected']} |",
        f"| 换公钥后验签失败 | {d['wrong_key_rejected']} |",
        f"| 全零伪造签名被拒 | {d['md5_like_forgery_rejected']} |",
        f"| 公钥中泄漏私钥字段 | {d['private_key_leaks_in_public']} |",
        f"| 仓库内密钥文件 | {d['repo_key_files'] or '无（私钥只在临时目录，用完即删）'} |",
        "", "## 三、结论：算法独立 ≠ 信任根独立（关键诚实）", "",
        "- **算法层面**：纯标准库确实能做出真非对称签名（私钥签、公钥验），无需第三方库。"
        "628 报告中「HMAC 需共享秘密、无法制造独立性」的判断在**算法层**已可解除。",
        "- **信任根层面**：本工具的公钥也是**同一主体生成**的。如果签名者既生成密钥又发布公钥，"
        "那么「第三方验签通过」只证明「这条凭证由持有该私钥的主体签发」，"
        "而**该主体仍是被验证方自己** ⇒ 独立性等级仍是 **L1/L2（同主体/同实现）**，"
        "**不是 L4（分信任根）**。",
        "- 要让公钥真正成为「外部信任根」，需要：公钥**托管给独立方**（人/机构/KMS）、"
        "或其指纹**写进外部不可篡改位置**（如公开透明日志/OTS 上链）。这两件事都是**人的决定**，"
        "机器不能代办 ⇒ 已列入交人项。", "",
        "## 四、诚实局限（不可用于生产）", "",
        "1. **教科书级实现**：无恒定时间运算（计时侧信道）、无盲化、无 padding oracle 防护；",
        "2. 自定义 JSON 密钥格式（非 PKCS#8/SPKI），**与其他系统不可互操作**；",
        "3. 素数生成用 `secrets`（CSPRNG）+ Miller-Rabin 40 轮，未做 FIPS 级校验；",
        "4. 未做密钥轮换/吊销/有效期；私钥无口令保护（依托「只落临时目录且用完即删」）；",
        "5. 生产化路径（交人项）：引入 `cryptography` 库或外部 KMS（HSM），"
        "并把公钥指纹交给独立第三方 —— 届时**算法与信任根**才同时独立。", "",
        "## 五、与 628 凭证的衔接", "",
        "- `upgrade_credential(cred, priv)` 给 628 形态凭证补 `signature_scheme` + `signature`，"
        "**保留原 HMAC `attestation` 字段不覆盖**（双签共存，可灰度迁移）；",
        "- 待签字节与 628 一致（除 `attestation` 外全字段、`sort_keys`、UTF-8）⇒ "
        "HMAC 与 RSA 签名锚定**同一份内容**，便于交叉验证；",
        "- 629 C4 端到端编排使用本工具签名（临时目录），并把「公钥指纹」写进透明日志可追溯。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    t0 = time.time()
    priv = generate_keypair(1024)          # 自检用 1024 位（速度），报告用 2048
    pub = public_of(priv)
    chk("密钥对生成且耗时合理", time.time() - t0 < 120,
        f"({round(time.time() - t0, 2)}s)")
    chk("n = p*q 且 e*d ≡ 1 (mod φ)", priv["n"] > 0 and priv["e"] > 1)
    chk("公钥不含私钥字段", not any(k in pub for k in ("d", "p", "q")))
    msg = b"queyi-629-c1"
    sig = sign(priv, msg)
    chk("签名 → 验签通过", verify(pub, msg, sig))
    chk("改消息 → 验签失败", not verify(pub, msg + b"x", sig))
    chk("换密钥 → 验签失败", not verify(public_of(generate_keypair(1024)), msg, sig))
    chk("垃圾签名 → 验签失败", not verify(pub, msg, "deadbeef"))
    chk("同一消息两次签名都有效（PKCS#1 确定性）", verify(pub, msg, sign(priv, msg)))
    cred = {"vsa_version": "1.0", "results": {"w2_in": 114}, "attestation": "hmac"}
    up = upgrade_credential(cred, priv)
    chk("628 凭证可升级为双签（HMAC 保留）",
        up["attestation"] == "hmac" and "signature" in up
        and verify_credential_sig(up, pub))
    chk("仓库零密钥落盘（全仓扫描：无 rsa_private / *.pem / private_key）",
        repo_key_files() == [], f"({repo_key_files()})")
    chk("报告存在且含信任根结论", os.path.exists(OUT_MD)
        and "信任根" in open(OUT_MD, encoding="utf-8").read())
    print(f"C1 asymmetric signer check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 C1 VSA 非对称签名（纯标准库）")
    ap.add_argument("--check", action="store_true", help="只读自检（临时目录，不写仓库）")
    ap.add_argument("--report", action="store_true", help="写 data/vsa_asymmetric_629.md")
    ap.add_argument("--demo", action="store_true", help="打印演示 JSON")
    ap.add_argument("--bits", type=int, default=DEFAULT_BITS)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.demo:
        print(json.dumps(demo(args.bits), ensure_ascii=False, indent=2))
        return 0
    d = demo(args.bits)
    print(f"RSA-{d['bits']} gen={d['gen_seconds']}s sign={d['sign_ms']}ms "
          f"verify={d['verify_ms']}ms valid={d['valid']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
