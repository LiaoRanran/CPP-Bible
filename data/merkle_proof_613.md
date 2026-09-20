# 613 · Merkle 包含证明（E3）

> 生成：`python tools/merkle_proof_613.py` ｜ 时间：2026-09-21T00:05:25
> 来源：`data/supply_chain/merkle_roots.json`（目录级 Merkle 根）+ `merkle_integrity.prove/verify`。

## 一、总览

| 项 | 值 |
|---|---|
| 证明条数 | 10 |
| 验证通过 | **10** |
| 验证失败 | 0 |
| 覆盖目录 | atoms, evidence, Examples, Book, mutation_baselines |

## 二、逐条证明

| 目录 | 文件 | 证明步数 | 根（前16） | 验证 |
|---|---|---|---|---|
| atoms | `atoms/README.md` | 5 | `11c0b3d982017229…` | ✅ |
| atoms | `atoms/conc/ATOM-CONC-FENCE-001.md` | 5 | `11c0b3d982017229…` | ✅ |
| evidence | `evidence/README.md` | 6 | `bfc1d80e19a9a75e…` | ✅ |
| evidence | `evidence/conc/EV-CONC-001.md` | 6 | `bfc1d80e19a9a75e…` | ✅ |
| Examples | `Examples/README.md` | 11 | `2e8063fe0d1aee5c…` | ✅ |
| Examples | `Examples/_asm_constexpr.asm` | 11 | `2e8063fe0d1aee5c…` | ✅ |
| Book | `Book/GLOSSARY.md` | 8 | `0a36f80b46c4d317…` | ✅ |
| Book | `Book/PREREQUISITES.md` | 8 | `0a36f80b46c4d317…` | ✅ |
| mutation_baselines | `data/mutation/full_baseline_v1.json` | 3 | `42829d7851991a3f…` | ✅ |
| mutation_baselines | `data/mutation/full_baseline_v2.json` | 3 | `42829d7851991a3f…` | ✅ |

## 三、证明能做/不能做什么

- ✅ 能证明：**该文件（含其相对路径）确实被计入该目录的 Merkle 根**。
- ❌ 不能证明：文件内容「正确」、或该根在某个时刻已存在（后者需 E1 的 OTS 上链，而 E1 当前 attestation 仍 pending）。
- 叶 hash 绑定相对路径 ⇒ 无法把 A 文件的证明套到 B 文件上。
