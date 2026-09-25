# 613 · 信任根 OTS 上链凭据（E1）

> 生成：`python tools/ots_anchor_613.py` ｜ 时间：2026-09-25T14:44:39
> **attestation 仍 pending**：本工具不 submit 日历 ⇒ 比特币证明段是占位零，
> **不得当作时间戳证明**（609 铁律）。真正上链由人执行 submit（交人）。

## 一、锚定对象

| 项 | 值 |
|---|---|
| 文件 | `data/supply_chain/merkle_roots.json` |
| sha256 | `d155486902d44a07d3d1f88c4b19fd1ff5f16deedb51d2ee928138783930c1f6` |
| .ots | `data/supply_chain/merkle_roots.json.ots`（131 B） |
| 生成时间 | 2026-09-25T14:44:39+08:00 |

## 二、结构校验

| 项 | 值 |
|---|---|
| OTS 版本 | 1 |
| 操作序列 | sha256 → append |
| .ots 内 digest | `d155486902d44a07d3d1f88c4b19fd1ff5f16deedb51d2ee928138783930c1f6` |
| 文件当前 digest | `d155486902d44a07d3d1f88c4b19fd1ff5f16deedb51d2ee928138783930c1f6` |
| **digest 一致** | ✅ |
| attestation 类型 | bitcoin |
| **attestation pending** | ⚠ 是（未上链） |

## 三、状态判定

- ✅ **凭据已生成且结构合法**：文件摘要与 .ots 内承诺一致，可被任何 OTS 客户端解析。
- ⚠ **尚未上链**：需 `ots submit`（或等价日历提交）后才有比特币区块时间戳。
- ⇒ 当前可证明「**该 .ots 绑定此摘要**」，**不能**证明「此摘要在某时刻已存在」。

> 交人：执行 submit 并回填 `.ots`，届时本报告的 pending 列自动变 ✅。
