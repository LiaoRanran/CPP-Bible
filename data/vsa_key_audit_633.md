# 633 C1 · vsa_secret.key 备份 + 影响评估（默认不轮换）

## 一、影响评估：谁在用这把钥

- 引用 `vsa_secret.key` 的位置：**53** 处

| 文件 | 行 | 片段 |
|---|---|---|
| `tools/baseline_632.py` | 5 | `data/vsa/vsa_secret.key 是否存在。` |
| `tools/baseline_632.py` | 77 | `"""data/vsa 下是否存在密钥文件（*.key 或 vsa_secret.key）。"""` |
| `tools/baseline_632.py` | 81 | `return (d / "vsa_secret.key").exists() or any(d.glob("*.key"))` |
| `tools/baseline_632.py` | 97 | `f"- `data/vsa/vsa_secret.key` 存在：`{key}`",` |
| `tools/baseline_632.py` | 113 | `print("632 任务0 --check OK：CI剩余 %d 项，代理 %s，vsa_secret.key %s"` |
| `tools/e2e_attestation_629.py` | 179 | `"| 密钥 | 生产 `data/vsa_secret.key` | 临时目录（用完即删；仓库零落盘） |", "",` |
| `tools/run_632_gate.py` | 158 | `"5. `baseline_632 --check` 仍报「vsa_secret.key 不存在」——其探针指向"` |
| `tools/run_632_gate.py` | 159 | `"`data/vsa/vsa_secret.key`（错误路径）；真实密钥在 `data/vsa_secret.key`"` |
| `tools/vsa_asymmetric_signer_629.py` | 242 | `"| 密钥 | 单密钥 `data/vsa_secret.key`（不入库） | 私钥/公钥分离，私钥只落**系统临时目录** |",` |
| `tools/vsa_attestation_628.py` | 6 | `- attestation = HMAC-SHA256(上述全部字段)，密钥 `data/vsa_secret.key`` |
| `tools/vsa_attestation_628.py` | 31 | `SECRET = os.path.join(ROOT, "data", "vsa_secret.key")` |
| `tools/vsa_attestation_628.py` | 131 | `"error": "secret key not found（data/vsa_secret.key 不入库，缺失时无法验证 HMAC）"}` |
| `tools/vsa_attestation_628.py` | 219 | `chk("密钥文件已加入 .gitignore", "vsa_secret.key" in gi_txt)` |
| `tools/vsa_attestation_628.py` | 259 | `"- 密钥 `data/vsa_secret.key` **不入库**（.gitignore）。",` |
| `tools/vsa_key_audit_633.py` | 1 | `"""633 C1 · vsa_secret.key 备份 + 影响评估（**默认不轮换**）` |
| `tools/vsa_key_audit_633.py` | 6 | `- 影响评估：扫全仓找出引用 `data/vsa_secret.key` 的工具；统计 `data/vsa/` 下已签发的` |
| `tools/vsa_key_audit_633.py` | 9 | `- **gitignore 加固**（632 G1 发现 ignore 过窄）：覆盖 `data/vsa_secret.key*` 与 `data/vsa/*.key*`。` |
| `tools/vsa_key_audit_633.py` | 29 | `KEY = os.path.join(ROOT, "data", "vsa_secret.key")` |
| `tools/vsa_key_audit_633.py` | 35 | `REQUIRED_IGNORES = ("data/vsa_secret.key*", "data/vsa/*.key*")` |
| `tools/vsa_key_audit_633.py` | 49 | `"""扫全仓（tools/ + data/）找出引用 vsa_secret.key 的位置。"""` |
| `tools/vsa_key_audit_633.py` | 80 | `"note": "data/vsa_secret.key 原来已忽略（窄）；需加宽到 key* 与 data/vsa/*.key*"}` |
| `tools/vsa_key_audit_633.py` | 113 | `"# 633 C1 · vsa_secret.key 备份 + 影响评估（默认不轮换）", "",` |
| `tools/vsa_key_audit_633.py` | 115 | `f"- 引用 `vsa_secret.key` 的位置：**{len(refs)}** 处", "",` |
| `tools/vsa_key_audit_633.py` | 124 | `"硬编码路径 `data/vsa_secret.key`，不自动读备份）。",` |
| `tools/vsa_key_audit_633.py` | 169 | `ap = argparse.ArgumentParser(description="633 C1 vsa_secret.key 备份+影响评估")` |
| `tools/vsa_verify_628.py` | 6 | `1. 重算 HMAC-SHA256 与凭证 `attestation` 对比 —— 签名有效（密钥读 `data/vsa_secret.key`）` |
| `tools/vsa_verify_628.py` | 32 | `SECRET = os.path.join(ROOT, "data", "vsa_secret.key")` |
| `data/628_baseline.md` | 58 | `| VSA 凭证 | HMAC 基础概念已有（613/625 用过 HMAC） | `vsa_attestation_628.py` + `vsa_verify_628.py`（密` |
| `data/630_baseline.json` | 34 | `"b8303d04 632 [G1] vsa_secret.key 安全审计：实测密钥存在于 data/vsa_secret.key（32字节、gitignored、未入库）；更正` |
| `data/630_baseline.md` | 58 | `b8303d04 632 [G1] vsa_secret.key 安全审计：实测密钥存在于 data/vsa_secret.key（32字节、gitignored、未入库）；更正 ` |

## 二、轮换影响

- `data/vsa/` 下已签发 VSA 凭证：**36** 张（`attestation_*.json`）。
- **若轮换**：这些旧凭证的 HMAC 用旧钥签发，换钥后**新钥验证会失败**；旧钥保留在备份中即可用于**历史凭证验证**——但需验证端支持指定旧钥（当前工具硬编码路径 `data/vsa_secret.key`，不自动读备份）。
- 结论：**轮换会导致历史凭证默认不可验**（需人工把备份钥放回或改验证端支持 key_id）⇒ 影响评估判定为**较高**，**默认不轮换**（交人裁决）。

## 三、备份状态

- 密钥存在：**True**；sha256 前 12 位：`2ae8d6a001a3`
- 备份目标：`data/vsa/vsa_secret.key.backup_20260924`（本次为只读评估，未写）
- 备份动作由 `--backup` 执行（复制 + sha256 一致性校验）。

## 四、gitignore 加固（632 G1 发现过窄）

| 需覆盖模式 | 当前是否存在 |
|---|---|
| `data/vsa_secret.key*` | ✅ |
| `data/vsa/*.key*` | ✅ |

## 五、轮换决策

- **默认不轮换**（§零.14）。`--rotate` 才会执行：先备份 → 再写 32 字节新钥。
- 是否轮换交人裁决（见 §交人项）。

## 六、诚实登记

1. **未轮换密钥**（默认关闭，符合 §零.14）；
2. **密钥内容全程未打印**，只输出 sha256 前 12 位用于一致性核对；
3. 影响评估为**静态**（按文件引用 + 凭证计数），未实跑「换钥后旧凭证验证失败」的端到端复现；
4. gitignore 加宽后需复核 `git check-ignore` 对真实密钥生效。
