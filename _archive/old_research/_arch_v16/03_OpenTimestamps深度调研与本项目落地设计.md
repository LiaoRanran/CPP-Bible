# 03 · 方向 3：OpenTimestamps 深度调研与本项目落地设计

> 来源：【已查证】OpenTimestamps 官网 opentimestamps.org（检索 2026-05-22：默认公共 calendar 列表；"At the end of stamp operation, the ots proof download starts automatically"）；OpenTimestamps Calendar Server GitHub opentimestamps/opentimestamps-server（提供聚合、Bitcoin 时间戳、远程日历）；其余为本调研设计。

## 3.1 核心概念（准确解释）
- **时间戳证明（.ots）**：证明"某文件哈希在时刻 T 之前已存在"，锚定到 Bitcoin 区块链。
- **日历服务器（calendar server）**：接收客户端哈希，聚合成 Merkle 树，把树根写入 Bitcoin 交易的 `OP_RETURN`，返回 `.ots` 证明。
- **Bitcoin 锚定**：Merkle 根进 Bitcoin 区块 → 利用 Bitcoin 的不可篡改历史证明时间。
- **证明（proof）**：含从文件哈希到 Bitcoin 区块根的 Merkle 路径 + 区块高度 + 交易哈希。

## 3.2 工作流程
1. 客户端算文件 hash。
2. 提交 hash 到日历服务器。
3. 服务器把多个 hash 聚合成 Merkle 树。
4. 树根写入 Bitcoin `OP_RETURN` 交易。
5. 客户端获取 `.ots` 证明。
6. 验证：用 Bitcoin 区块验证树根 → 用 Merkle 证明验证文件 hash 在树中 → 得出"该 hash 在区块时间前已存在"。

## 3.3 .ots 格式（概念；诚实说明）
`.ots` 是二进制格式，含：文件头、哈希类型、到 Bitcoin 根的 Merkle 证明路径、中间日历证明（若有）、Bitcoin 区块高度与交易 ID。**精确二进制解析需 Bitcoin 区块数据**（完整验证要连 Electrum/Blockstream 或本地节点）。本阶段建议**优先调用 `ots` CLI（opentimestamps-client）**而非手搓完整解析器——手搓仅适合"验证已有 .ots"的轻量场景（见 3.8）。

## 3.4 验证流程（每一步）
解析 .ots → 验证 Merkle 证明（文件 hash → 中间日历根）→ 验证中间根 → Bitcoin 区块根 → 查询区块时间 → 结论"该 hash 于 <区块时间> 前存在"。

## 3.5 本项目需时间戳的文件（按优先级）
| 优先级 | 文件 | 为什么 |
|---|---|---|
| P0 | `tools/.tool_checksums` | 信任根本身，需钉死"此基准于 T 前存在" |
| P0 | `data/supply_chain/merkle_roots.json` | 全量完整性根，钉时间即钉全库 |
| P1 | `data/supply_chain/links/*.json` | 关键步骤溯源链 |
| P1 | `data/governance_docs_manifest.json` | 治理文档 manifest（补 governance_doc_guard 的"manifest 不进校验"缺口）|
| P2 | `data/overturned_events.jsonl` | 人审/推翻通道存在性 |
| P2 | `data/mutation/full_baseline_v*.json` | 知识基线版本 |

**关键设计**：**只对 Merkle 根 + `.tool_checksums` + governance manifest 打时间戳**——一次戳覆盖全库（因为根已代表所有被覆盖文件），避免对上百文件逐一戳（成本/体积）。

## 3.6 存储方案
`data/supply_chain/timestamps/<原文件名>.ots`（同名 + .ots 后缀）。根与戳的映射记 `data/supply_chain/timestamp_index.json`。

## 3.7 打戳时机
- 每次 `git commit` 后（pre-commit 或 post-commit 钩子，纯 stdlib 脚本触发）。
- 每个苦力批次完成后。
- 关键数据变更后（基线/推翻通道）。

## 3.8 纯标准库实现 vs 调 CLI（对比）
- **调 `ots` CLI**：最稳，完整 Bitcoin 验证，但引入外部依赖（需装 opentimestamps-client）。
- **手搓最小验证器**：仅解析已下载的 .ots、验证 Merkle 路径到"已知锚点"（跳过 Bitcoin 区块查询）→ 轻量但需信任锚点。
- **本阶段建议**：N 档先用 `ots` CLI 封装（薄壳 `tools/timestamp.py` 调 subprocess），W 档（确需零依赖）再手搓最小验证器。**诚实**：纯 stdlib 完整实现 .ots + Bitcoin 验证不现实（需区块解析），不假装能做。

## 3.9 与现有系统集成
- `tool_integrity --check`：同时验 `.tool_checksums` 的 .ots（存在且未过期）。
- in-toto/SLSA：时间戳是 link 的一个字段（`environment.ts_proof`）或独立证明；验证 link 时可附带验戳。
- Merkle：`merkle_roots.json` 上链（一次戳代表整个目录）。

## 3.10 联网可行性（本项目环境）
- 环境有 VPN（Hentai VPN）。公共日历（finney.calendar.eternitywall.com 等）可能可达，但 **Bitcoin 区块验证需 Electrum/Blockstream API**——联网可达性不确定，列为**环境风险**（见 06）。
- 缓解：自建日历服务器（opentimestamps-server）或仅用"哈希发布到公开 append-only 日志"的降级方案。

## 3.11 时间精度
Bitcoin 出块 ~10 分钟（非 1 小时；"约 1 小时"是旧认知，实际是多次确认后的强保证）。对本项目"存在性时间"需求足够（我们要的是"某基准在攻击前已存在"，分钟级足够）。

## 3.12 成本-收益 + 反例
- 成本：中（需联网 + 外部 CLI 或降级方案 + 钩子）。收益：把"信任根"钉上不可篡改时间轴，使**事后篡改可被独立证明**（配合 Merkle 根）。
- **反例 1（局限性大）**：**离线构建**场景——无网则无法打戳，需降级（本地日志）。
- **反例 2（结构性）**：**身份**——OTS 只证"存在时间"不证"谁"，单用户阶段身份仍靠 git 作者（自设），这是阶段 3 不可逾越的上限（见 00 ①）。

## 3.13 探针/实证
本调研探针未跑真实 .ots（需联网/外部 CLI，违反只读纪律的"不装依赖"精神）；但探针的 Merkle 根 `35ad…` 即为"待上链对象"，证明**根已就绪、上链只是封装**。
