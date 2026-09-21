# 614 C2：in-toto 真签名可行性评估

> 铁律：不改受控目录；诚实标注；**不臆造"已签名"**。评估时间 2026-09-21。

## 一、当前状态（实地核验）
| 项 | 实测值 | 结论 |
|---|---|---|
| link 文件 | `data/supply_chain/link_613_verify.json`（791 B） | 存在 |
| `signature.scheme` | **`hmac-sha256-not-in-toto-standard`** | ⚠ **非标准 in-toto** |
| 签名类型 | **HMAC-SHA256（对称）** | 完整性 + 持有证明 |
| 能力边界 | 能证「未篡改 + 持钥者生成」 | ❌ **不能**提供 in-toto 要求的**公钥可验 / 非否认** |
| keyid | `ea5c9a0c146cdb09` | 对称密钥派生（非公钥指纹） |

⇒ 现状与 613 `tools/in_toto_link.py` 注释一致：**这不是标准 in-toto 签名**，是 HMAC 替代。

## 二、标准 in-toto 真签名前提（实测）
| 前提 | 实测 | 结论 |
|---|---|---|
| `in_toto` Python 库 | `import in_toto` → **ModuleNotFoundError** | ❌ 缺 |
| 非对称加密库（cryptography/nacl/ecdsa/rsa） | 613 实测**全 False** | ❌ 缺 |
| `gpg`（GPG 签名路径） | `Get-Command gpg` → **NOT FOUND** | ❌ 缺 |
| 签名密钥（ed25519 / GPG key） | 无（仓内无密钥、无 keyring） | ❌ 缺 |
| `ssh-keygen`（可生成 ed25519） | ✅ 存在（`C:\WINDOWS\System32\OpenSSH\ssh-keygen.exe`） | △ 但 ssh key 非 in-toto 标准签名格式 |

⇒ **技术上可行**（装 `in-toto` + `securesystemslib[crypto]` 即可），但需要**签名密钥**。

## 三、为何本批**不自动执行**（诚实障碍清单）
1. **密钥托管 = 人类秘密**：签名密钥的生成/保管/授权属人；仓内自造密钥会引入**托管歧义**（谁持有？可否吊销？）。
2. **交人项**：613 已明确「真正非对称签名是**交人项**（装 cryptography 后换 ed25519，或人工 gpg 签）」。
3. **门禁解释器污染风险**：`.venv` 为门禁唯一可信解释器，装 `in-toto`/`securesystemslib[crypto]` 可能引发依赖漂移。
4. **标准格式细则**：in-toto 的 `signature` 字段需 `keyid` 为**公钥指纹**（非对称），当前对称 keyid 不满足。
5. **失败代价**：手搓非标准"签名"会制造**看似已签的假象**，比"诚实标注 HMAC"更危险。

## 四、交人执行 Runbook（精确命令）
```bash
# 1) 装 in-toto + 加密后端
pip install in-toto securesystemslib[crypto]
# 2) 生成 ed25519 签名密钥（密钥交人保管，绝不入库）
in-toto-keygen supply_chain_key   # 或 securesystemslib 的 generate_and_write_ed25519_keypair
# 3) 用私钥签 link（in-toto 标准 schema，signature.keyid=公钥指纹）
in-toto-run --step-name 613-trust-root --signing-key supply_chain_key \
            --materials data/supply_chain/merkle_roots.json \
            --products data/ots_anchor_613.md \
            -- python tools/ots_anchor_613.py
# 4) 用公钥验证（非否认）
in-toto-verify --layout root.layout --layout-key <pubkey> ...
```
> 注：标准 link 的 `signature` 应为 `{keyid: <公钥指纹>, sig: <ed25519>}`，与当前 HMAC scheme 不兼容 ⇒ 需**替换** `link_613_verify.json` 的签名段（经人授权）。

## 五、结论
- **当前状态**：HMAC-SHA256 完整性证据（**非标准 in-toto**、无公钥可验/非否认）——诚实标注，不被误用。
- **真签名**：**技术上可行**（装库即可），但受制于「**密钥托管/授权 + 交人项 + 解释器卫生**」，本批**不自动执行**。
- **后续**：由人按第四节 Runbook 生成密钥并签名；C3 的 `trust_root_status_check` 将按 `scheme` 标注是否标准。

## 六、诚实边界
- 未安装 `in-toto`、未生成任何密钥、未修改 `data/supply_chain/link_613_verify.json`。
- 本次仅只读探针（import / `Get-Command`），无任何签名/发布副作用。
