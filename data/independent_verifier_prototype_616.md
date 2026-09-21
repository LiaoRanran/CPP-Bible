# 616 D2 · 独立复核原型报告（最小可行版本）

> 原型**非生产**；HMAC **测试密钥**（`CPPBIBLE_VSA_KEY` 缺省用 `cppbible-616-test-key-NOT-FOR-PRODUCTION`）。

## 一、功能与限制
- **功能**：对证据卡用**独立实现**（`ev_matrix_unbacked_v2.py`，不 import/copy gate_engine）复核
  `EV-MATRIX-UNBACKED`，产出 **VSA 凭证**（verifier_id / verified_at / 输入 sha256 / 结果 verdict / HMAC-SHA256 签名）。
- **CLI**：`--make <card>` / `--verify <vsa.json>` / `--samples` / `--check`。
- **限制**：
  1. 只复核**1 条规则**（EV-MATRIX-UNBACKED）；
  2. 仅 **HMAC 对称签名**——能证"未篡改 + 持钥"，**无公钥可验/非否认**；
  3. 无透明日志（D3 阶段 2）、无多验证者共识（阶段 4）。

## 二、示例凭证（5 张卡）
`data/independent_verifier_samples_616/`：
`EV-CONC-001.vsa.json`、`EV-CONC-002.vsa.json`、`EV-MEM-001.vsa.json`、
`EV-HIST-001.vsa.json`、`EV-LANG-001.vsa.json`。

示例（结构）：
```json
{"vsa_version":"1.0","verifier_id":"ev_matrix_unbacked_v2","verified_at":"...",
 "input":{"path":"evidence/conc/EV-CONC-001.md","sha256":"<64hex>"},
 "result":{"rule":"EV-MATRIX-UNBACKED","verdict":"UNBACKED","anchors":N},
 "signature":{"scheme":"hmac-sha256","keyid":"a208db4ef3690b9f","sig":"<64hex>"}}
```

## 三、可验证性验证结果
| 场景 | 结果 |
|---|---|
| 合法凭证（`--verify`） | ✅ 通过（签名一致 + 输入哈希一致） |
| **篡改** verdict 后 | ❌ 失败（签名不符） |
| 用**错密钥**验证 | ❌ 失败（keyid 不匹配） |
| 卡内容变更后 | ❌ 失败（输入哈希不符） |

- 自验证：`python tools/independent_verifier_prototype.py --check` ⇒ exit 0。

## 四、与完整他验架构的差距
| 维度 | 原型 | 完整（D1） |
|---|---|---|
| 覆盖规则 | 1 / 63 | 63 / 63 |
| 签名 | HMAC（对称） | ed25519（非对称，公钥可验） |
| 透明日志 | 无 | append-only + Merkle + 外部锚 |
| 验证者 | 1（本项目） | 多验证者 + 第三方共识 |

## 五、下一步建议
1. **阶段 2（617+）**：扩到 10 条规则 + 加 **Merkle 透明日志** + 与官方对比报告；
2. **签名升级**：引入 ed25519（需密钥托管，交人审）；
3. **接 metrics**：他验一致率/分歧数入 `metrics_collector`（接 B3 锁）。

## 六、边界
- 未修改任何现有工具；**不自动接受任何判决**（人审权力）；示例凭证只读。
