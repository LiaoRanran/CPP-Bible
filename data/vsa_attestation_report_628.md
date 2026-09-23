# 628 B2 · VSA 验证凭证报告（他验三件套 #2）

- 凭证：`data\vsa\attestation_20260923T030008Z.json`
- HMAC 验证：True · 输入哈希锚定：True · 结果一致：True
- verifier_sha256：`a85cad4faa914506…`（凭证可追溯到验证者脚本版本）
- input_hashes：ledger/grounded/PCK 目录三重锚定（凭证绑定输入版本）

## 与 Sigstore/Rekor 的对比

- 本项目用 **HMAC-SHA256**（对称）：单用户阶段无独立密钥托管，非对称签名的私钥仍在同一主体手中，无法制造独立性。
- **诚实局限**：HMAC 只能证明「持有密钥的主体生成了凭证」，不能证明「独立主体认可」——真正的独立性需非对称签名 + 独立密钥托管，留后续批次。
- 密钥 `data/vsa_secret.key` **不入库**（.gitignore）。
