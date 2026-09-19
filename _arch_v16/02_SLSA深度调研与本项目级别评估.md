# 02 · 方向 2：SLSA 深度调研与本项目级别评估

> 来源：【已查证】SLSA 官方规范 slsa.dev/spec/v1.0/provenance（检索 2026-09-19，provenance 字段：buildType / builder.id / invocation{entryPoint,parameters,environment} / buildConfig / metadata{invocationId,startedOn,finishedOn,completeness} / materials[{uri,digest}] / products[{uri,digest}]）；SLSA 官网 slsa.dev（Supply-chain Levels for Software Artifacts，L0-L4）。其余为本调研评估。

## 2.1 SLSA 各级别（准确解释）
- **L0**：无要求（默认）。
- **L1**：构建过程有文档、provenance 可用（可查"这个产物怎么来的"）。
- **L2**：构建服务**托管**、provenance 经服务**签名**（构建与签名分离，防本地伪造）。
- **L3**：构建服务**不可篡改**、provenance 经服务签名且**不可伪造**（强隔离）。
- **L4**：所有依赖达 L4 + **双人审批** + **可复现构建**。

## 2.2 provenance v1 格式（适配本项目，见 07 完整 schema）
SLSA v1 由 `buildDefinition`（这次构建的定义）+ `runDetails`（这次如何运行）组成；关键字段 `invocation`（命令/参数/环境）、`metadata`（起止时间、completeness）、`materials`（输入依赖的 uri+digest）、`products`（输出产物的 uri+digest）。

## 2.3 本项目当前 SLSA 级别评估（逐项，附证据）
| 要求 | 当前状态 | 证据 | 达标？ |
|---|---|---|---|
| 构建过程有文档 | 部分（前序 _arch_v* 调研记录，非正式 build doc） | 各 _arch_v*/00 总览 | 接近 L1 文档 |
| provenance 可用 | 否（仅有 `.tool_checksums` 散列，无步骤级 provenance） | tool_integrity.py line 37 | 未达 L1 |
| 构建服务托管 | 否（本地单用户） | 仓库结构 | 未达 L2 |
| provenance 签名 | 否（`.tool_checksums` 不进校验、自签） | governance_doc_guard.py line 14-16 | 未达 L2 |
| 不可篡改构建 | 否 | 本地 | 未达 L3 |
| 双人审批/可复现 | 否 | 单用户 | 未达 L4 |

**结论：当前约为 L0（至多"接近 L1 文档"）**。根因与 585 攻击同源——信任根靠 git 留痕 + 人眼，无结构化、可验、签名的 provenance。

## 2.4 达到 L1 的具体行动（本项目能做到吗？）
**能（N 档）**：阶段 1-2 产出每个构建步骤的 link（= provenance 记录），存 `data/supply_chain/links/` + `layout.json`；写一份 `docs/build_process.md` 描述步骤链。即满足"过程有文档 + provenance 可用" → **达 SLSA L1 等价物**。

## 2.5 L2 及以上可行性（瓶颈）
- **L2**：需"托管构建服务 + 服务签名"。单用户本地构建无托管服务 → **结构性不可达**。
- **L3**：需不可篡改构建环境（TEE/CI 隔离）→ 单用户无 → 不可达。
- **L4**：双人审批 + 可复现 → 单用户无第二人、环境不可复现 → 不可达。
- **瓶颈**：不是代码问题，是"单用户 + 本地 + 无托管 CI"的部署模型。强行做 L2+ 是过度工程（见 2.9 反例）。

## 2.6 本项目的"SLSA 等价物"定义
> **Local-Provenance L1（本仓自定义级别）**：每个构建步骤产出一条由 `git HEAD + 作者` 签署（模拟签名）的 link；所有 link 的 Merkle 根覆盖全部产物；根经 OpenTimestamps 钉时间。它**对应 SLSA L1 的"provenance 可用 + 防事后篡改"意图**，但不声称 L2（托管签名）或 L3/L4（隔离/双人）。在单用户阶段，这是诚实可达到的最高等价级别。

## 2.7 provenance 生成方案
- 每个 step 完成时由 `supply_chain.py record` 自动生成 link（含 materials/products 真实哈希、命令、git 环境）。
- provenance = link 的超集；本项目的 link 直接复用 SLSA v1 字段（`builder.id="local:git:<head>"`, `invocation.command`, `materials[].digest`, `products[].digest`）。
- 存 `data/supply_chain/links/<step>.json`；全局 Merkle 根存 `data/supply_chain/merkle_roots.json`。

## 2.8 与 in-toto link 的集成
SLSA provenance 是 in-toto link 的特化：**link 是载体，SLSA 字段是内容**。本项目用同一份 link 文件同时满足"in-toto 溯源链"（01）与"SLSA L1 provenance"（02）——不重复造 schema（见 07）。

## 2.9 成本-收益 + 反例
- 成本（L1 等价物）：~中（复用 01 的 link 机制 + 一份 build doc）。收益：把"自签 checksum"升级为"结构化、可验、可时间戳的 provenance"，封堵 585 攻击 1 的溯源空白。
- **反例 1（不适用）**：照搬 SLSA L3"托管不可篡改构建"——需 CI/TEE 基础设施，单用户零收益。
- **反例 2（不适用）**：强制"双人审批"——单用户无第二人，只能退化成"二次自审"，不增信反添摩擦。

## 2.10 探针/实证
本调研探针生成的 `probes/layout.json` + `probes/links/*.json` 即为"SLSA L1 等价物"的最小原型（含 materials/products/command/functionary/timestamp），证明纯库可生成。
