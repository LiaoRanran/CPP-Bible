# 614 · 信任根状态（诚实标注）

> 生成：`python tools/trust_root_status_check.py` ｜ 时间：2026-09-21T11:58:11
> 只读检查；**绝不**把占位/替代证据说成已锚定。

## 一、逐项状态

| # | 证据 | 存在 | 诚实状态 |
|---|---|---|---|
| 1 | Merkle 根 | ✅ | `47c330c9dca15032d80b7f78fd20024a94faabca70935dbdb53d6bd77f6e0db5` |
| 2 | OTS 时间戳 | ✅ | ⚠ pending（占位零，未上链） |
| 3 | in-toto link | ✅ | ⚠ 非标准替代（scheme=hmac-sha256-not-in-toto-standard） |
| 4 | tool_integrity | ✅ | `tools/.tool_checksums` |
| 5 | golden lock | ✅ | `tools/golden_state.json` |
| 6 | governance | ✅ | `data/governance_docs_manifest.json` |

## 二、总判定

- ⚠ partially_anchored（部分锚定：存在 pending/HMAC 替代）

## 三、能力边界（诚实）

- OTS：⚠ pending（占位零，未上链） ⇒ 可证「.ots 绑定此摘要」，**不能**证「某时刻已存在」。
- in-toto：⚠ 非标准替代（scheme=hmac-sha256-not-in-toto-standard） ⇒ 完整性 + 持有证明；**无**公钥可验/非否认。

> 真上链 / 真签名仍为**交人项**（见 `data/ots_real_chain_evaluation_614.md`、`data/in_toto_real_signing_evaluation_614.md`）。
