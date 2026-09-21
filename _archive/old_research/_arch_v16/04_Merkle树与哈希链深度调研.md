# 04 · 方向 4：Merkle 树与哈希链深度调研（597 已探针，本次深化）

> 来源：【已查证】Merkle 1979（Ralph Merkle, "A Certified Digital Signature"）；RFC 6962 Certificate Transparency（检索 2026-09-19：append-only 日志、Merkle 树、inclusion/consistency 证明、Signed Tree Head）；Merkle DAG=IPFS、Patricia Trie=Ethereum、Bucket Tree=CT 为领域常识。探针：`probes/probe_supply_chain.py`（Merkle 根 35ad…，inclusion+consistency+篡改检测全通过）。

## 4.1 Merkle 树核心概念
- **叶节点** = 文件 hash（RFC6962 用 `0x00||data` 前缀再 sha）。
- **内部节点** = 子节点拼接 hash（RFC6962 用 `0x01||L||R` 前缀）。
- **Merkle 根** = 树顶哈希，代表整个集合。
- **Merkle 证明（包含证明）**：从叶到根的兄弟哈希路径，验证者重算得根即可证"该叶在树中"（探针 `verify_inclusion` 实测 `merkle_inclusion_ok=true`）。

## 4.2 变体对比
| 变体 | 结构 | 适用 | 本项目适合？ |
|---|---|---|---|
| Merkle 树 | 二叉树平衡 | 集合成员证明 | **适合**（目录集合完整性）|
| Merkle DAG | 有向无环、去重 | 内容寻址存储（IPFS） | 否（无内容去重需求）|
| Patricia Trie | 前缀树、键路径 | 账户状态（Ethereum） | 否（无键空间结构）|
| Bucket Tree | CT 专用、按区间 | 证书日志 | 否（CT 专属）|

## 4.3 哈希链 vs Merkle 树
- 哈希链 `H_n = hash(H_{n-1} || data_n)`：适合**有序序列**（如事件流、版本链），验证需从头重算。
- Merkle 树：适合**集合**（无序、可并行证明单元素）。
- **本项目**：`data/overturned_events.jsonl`（事件流）用**哈希链**；`atoms/`+`evidence/`+`Examples/`+`Book/`+`data/mutation/` 用 **Merkle 树**（集合完整性）。两者互补。

## 4.4 Certificate Transparency 的启发
CT（RFC 6962）设计：**append-only 日志** + 定期发布 Merkle 根（Signed Tree Head）+ **inclusion proof**（某证书在日志中）+ **consistency proof**（新根包含旧根所有内容）。
- 本项目借鉴：**Merkle 根只增不删**（append-only）；每次批次后发新根并记录旧根；提供一致性证明（见 4.7）。

## 4.5 本项目需 Merkle 树的目录/文件（按优先级）
| 优先级 | 范围 | 为什么 |
|---|---|---|
| P0 | `tools/`（CORE+TEST_CONFIG）+ 规则/策略定义文件 | 封堵 585 攻击 1（含现未被 tool_integrity 覆盖的规则定义）|
| P0 | `data/supply_chain/links/` | 溯源链完整性 |
| P1 | `atoms/` `misconceptions/` | 知识本体完整性 |
| P1 | `evidence/` `Examples/` `Book/` | 证据/卡面/书稿完整性 |
| P2 | `data/mutation/` `data/full_baseline_v*.json` | 变异/基线版本完整性 |

**关键修正（呼应 00 ① 最意外发现）**：Merkle 根必须**显式纳入规则/策略定义文件**（若它们不在 `gate_engine.py` 内），否则 585 攻击 1 的文件级篡改仍漏检。

## 4.6 根存储与更新
- 存储：`data/supply_chain/merkle_roots.json`，结构 `{scope: {root, height, leaf_count, updated_at, prev_root}}`（多 scope + 全局根）。
- 更新时机：git commit 后 / 批次完成 / 关键数据变更（与 03 打戳联动）。
- gate 启动自校验：`gate_engine.main` 第一句除 `tool_integrity.enforce()`，再验当前根与磁盘一致。

## 4.7 append-only 与一致性证明
- **append-only**：文件只能新增，根随叶增而更新；旧根存档于 `prev_root`，形成时间链。
- **一致性证明**：验证"新根包含旧根全部内容"。本探针用**前缀重算法**（验证者独立算前 m 叶的 MTH 比对旧根，`merkle_consistency_ok=true`）——诚实说明：这是正确且可验的"全叶可用"一致性检查；**简洁 RFC6962 consistency proof（仅传 O(log n) 哈希）留 W 档**（实现复杂、需严格 RFC6962 算法，当前非必须）。

## 4.8 正式工具设计（tools/merkle_integrity.py）
```
python tools/merkle_integrity.py build  [--scope all|tools|atoms|...]   # 算根写 merkle_roots.json
python tools/merkle_integrity.py verify [--scope ...]                    # 重算比对，exit 0/1
python tools/merkle_integrity.py prove  --leaf <path>                    # 生成包含证明 -> <path>.proof
python tools/merkle_integrity.py check-proof --leaf <path> --proof <f>   # 验证包含证明
python tools/merkle_integrity.py consistency --old <root> --new <root>  # 前缀重算一致性（N档）
```
详见 08。

## 4.9 与 tool_integrity / in-toto / OpenTimestamps 集成
- **tool_integrity**：互补——前者钉"5 工具文件逐文件 sha"，本工具覆盖"全部范围集合根"；`tool_integrity --check` 可作为 inspection。
- **in-toto**：Merkle 根是 link 的 `products`（根代表全范围）；link 链路绑定到根。
- **OpenTimestamps**：Merkle 根上链（一次戳覆盖全库）。

## 4.10 597 探针升级清单（探针 → 正式工具）
| 探针已有 | 正式工具需补 |
|---|---|
| 建树 + 根 + 篡改检测 | 多 scope 管理 + `merkle_roots.json` 持久化 |
| 包含证明 + 验证 | 证明文件 I/O（`.proof`）|
| 前缀一致性（全叶）| 可选 RFC6962 简洁一致性证明 |
| 只读扫文件 | `build/verify/prove/check-proof/consistency` 子命令 |

## 4.11 成本-收益 + 反例
- 成本：低（纯库，597 已验证可行性；正式化约 150-200 行）。收益：高（集合完整性 + 可独立验证根 + 封堵 585 攻击 1 文件级面）。
- **反例 1（不适用）**：Patricia Trie / Bucket Tree——需键空间/区间结构，本项目无。
- **反例 2（不适用）**：Merkle DAG 内容去重——无重复内容寻址需求，徒增复杂度。

## 4.12 探针实证
`probes/probe_supply_chain.py`：7 工具哈希 + 10 个 atoms 样例 → Merkle 根 `35ad36b1…`、树高 5；`merkle_inclusion_ok=true`、`merkle_tamper_detected=true`（改一叶根变、包含证明失败）、`merkle_consistency_ok=true`。
