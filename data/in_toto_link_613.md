# 613 · in-toto link 元数据（E2）

> 生成：`python tools/in_toto_link.py` ｜ 时间：2026-09-21T00:02:46
> 产物：`data/supply_chain/link_613_verify.json`

## 一、步骤

| 项 | 值 |
|---|---|
| name | 613-trust-root |
| command | python tools/ots_anchor_613.py |
| materials | 1 |
| products | 1 |
| signature scheme | **hmac-sha256-not-in-toto-standard** |
| keyid | ea5c9a0c146cdb09 |

## 二、⚠ 签名口径（必读）

- 标准 in-toto 要求**非对称签名**（ed25519/rsa）。本仓 venv 实测无 `cryptography`/`nacl`/`ecdsa`/`rsa` ⇒ 本工具退化为 **HMAC-SHA256（对称）**。
- 可提供：完整性（未篡改）+ 持钥证明；**不可**提供：非否认 / 公钥可验。
- ⇒ 真正非对称签名是**交人项**。

## 三、校验结果

- ✅ 通过

