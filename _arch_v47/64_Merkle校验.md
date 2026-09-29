# 方向 64：Merkle 树与账本完整性校验（Merkle tree, append-only ledger integrity）

> 项目锚点：阙疑 / queyi 用 append-only 哈希链账本 + Merkle checkpoint 保证"判决不可篡改、可独立复算"，并配套**不依赖内核的独立对账器**。本方向调研 Merkle 树原理（RFC 6962 Certificate Transparency）、哈希链、Merkle root 作为全局完整性摘要、第三方不信任内核即可复算 root、与区块链/证书透明度的类比，并落到阙疑当前 **452 条判决账本**、`gate_engine.py`（3826 行）与 37 实卡 / 67 规则 / 9 保护器的实测规模上。

---

## 核心结论

1. **一个 32 字节 Merkle root 即可作为阙疑 452 条账本的全局完整性摘要。** RFC 6962（Laurie、Langley、Kasper，Google，IETF 2013/2014）定义的二进制 Merkle 哈希树以 SHA-256 为固定哈希算法，叶子哈希加 `0x00` 前缀、内部节点加 `0x01` 前缀做域分离（防二次原像攻击），递归归约出"a single 32-byte Merkle Tree Hash"。对阙疑而言，452 条账本叶仅需约 `log2(452)≈8.8`（即 9 阶）树高，任何单条判决的包含证明仅约 9 个 32 字节哈希节点（≈288 字节），第三方无需下载全量账本即可验证某条判决确实落入账本。

2. **"不信任内核即可对账"与区块链 PoW 无关，而是证书透明度（CT）的 checkpoint + proof 模型。** CT 要求日志周期性发布由日志私钥签名的 **Signed Tree Head（STH）/ checkpoint**，任何人仅凭 checkpoint + inclusion proof / consistency proof 即可验证账本未被篡改与"仅追加"属性，无需信任日志服务器本身。Google《Verifiable Data Structures》白皮书原话："allowing an ecosystem to evolve from pure trust, to trust but verify"。阙疑的"独立对账器"正与该模型同构——对账器只消费账本导出的 checkpoint 与证明，不 import `gate_engine.py` 任何内部状态。

3. **Merkle 只保证"账本不可篡改"，不保证"判决正确"——阙疑必须显式区分两层断言。** 一致性证明（consistency proof）只能证明"先前的 m 条记录在新树中一字未动且顺序不变"，无法证明某条四态判决（verified/red-team/draft/block）的事实真值。若论文把"root 一致"等同于"判决可信"，将落入过度主张，在 NeurIPS E&D 的 threat model / limitations 一节会被 reviewer 抓住。阙疑应仿照 CT 的"trust but verify"措辞，把"可复算性（integrity）"与"正确性（validity）"拆成两条独立可证主张。

---

## 精确数字与案例

> 本节把抽象原理落到可核验的数字与逐字引文上。先说明一个通用直觉：Merkle 树的价值不在于"加密"，而在于"把对数级的验证成本转嫁给第三方"。传统做法是让审计者下载全量账本逐条比对，成本随规模线性增长；而 Merkle 树让审计者只需拿到根哈希与一条长度 O(log n) 的证明路径，即可在本地完成包含性验证。这正是阙疑"可独立复算"声称在数学上成立的根本原因——不是因为内核可信，而是因为根哈希与证明路径构成了一个任何人都能本地校验的承诺。

### 一、RFC 6962 二进制 Merkle 哈希树：哈希算法、前缀字节与 root 计算

RFC 6962 是证书透明度的奠基性实验性协议，其第 2.1 节精确定义了 Merkle 树构造。关键点如下（逐字引文均取自 rfc-editor.org/rfc/rfc6962.txt）：

- 哈希算法固定为 SHA-256：
  > "Logs use a binary Merkle Hash Tree for efficient auditing. The hashing algorithm is SHA-256 [FIPS.180-4] (note that this is fixed for this experiment, but it is anticipated that each log would be able to specify a hash algorithm)."

- 叶子与内部节点使用不同前缀做**域分离（domain separation）**，这是二次原像抵抗的关键：
  > "The hash of a list with one entry (also known as a leaf hash) is: MTH({d(0)}) = SHA-256(0x00 || d(0))."
  > "Note that the hash calculations for leaves and nodes differ. This domain separation is required to give second preimage resistance."

- 内部节点递归定义（k 为小于 n 的最大 2 的幂）：
  > "MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))."

- 最终输出是**单个 32 字节**摘要：
  > "The output is a single 32-byte Merkle Tree Hash."

需要特别强调的是，RFC 6962 选择"实验性协议"定位（文档明确写 "This document is not an Internet Standards Track specification"），说明 Merkle 日志格式本身仍在演进；这反而给阙疑一个机会：不必死守 v1 的字节细节，而可在论文中声明自己的账本格式"受 RFC 6962 启发、针对知识判决做了字段定制"。但定制的前提是公开字段定义，否则独立对账器无法复算——这是阙疑最容易翻车的地方：若 entry 序列化方式只写在内核代码里、不对账器不掌握，则"独立复算"名存实亡。

下表归纳 RFC 6962 的精确构造参数，可直接作为阙疑账本格式的对齐基准：

| 构造项 | RFC 6962 规定 | 阙疑账本可采用的值 |
|---|---|---|
| 哈希算法 | SHA-256（固定） | SHA-256（建议固定，便于复算） |
| 叶子前缀字节 | `0x00` | `0x00`（entry 序列化字节前加 0x00） |
| 内部节点前缀 | `0x01` | `0x01` |
| 叶子内容 | MerkleTreeLeaf 结构（timestamp/entry_type/…） | 判决 entry（卡 id + 四态 + 证据指纹 + 时间戳） |
| 树根长度 | 32 字节 | 32 字节 |
| 排序依据 | 提交顺序（append-only） | 账本 entry_index 递增 |

### 二、Signed Tree Head / Checkpoint：32 字节 root 周期性签名发布

CT 的不可篡改并非靠"人人都存全量"，而是靠日志**周期性发布并签名一个 checkpoint**。RFC 6962 第 3.5 节定义 Signed Tree Head（STH），其签名结构逐字为：

> "digitally-signed struct { Version version; SignatureType signature_type = tree_hash; uint64 timestamp; uint64 tree_size; opaque sha256_root_hash[32]; } TreeHeadSignature;"

并且对新鲜度有硬约束：

> "Each log MUST produce on demand a Signed Tree Head that is no older than the Maximum Merge Delay."

这里的 **Maximum Merge Delay（MMD）** 是日志在收到新条目后必须将其并入树并发布新 STH 的最长时间窗，是"仅追加且及时可见"的可审计保证。

Google《Verifiable Data Structures》白皮书（TrustFabric 团队，2021-05 最后更新）把这套机制抽象为通用"可验证日志"，逐字写道：

> "Periodically the log publishes a *checkpoint* that includes a commitment to all entries for a given log size. Clients of the log can: 1. Enumerate all entries held in the log. 2. Verify that a specific entry is included in the log, given just a checkpoint and an inclusion proof. 3. Verify the append-only property of the log, given two checkpoints and a consistency proof."

**与阙疑的直接对应**：阙疑的"Merkle checkpoint"概念正是此处 checkpoint——把 452 条账本的 32 字节 root、tree_size（=452）、签名时间戳写入一个独立 checkpoint 文件，并用项目签名密钥签名。独立对账器只需要这个 checkpoint，无需运行内核。这里有一个工程要点：签名密钥必须与内核部署密钥**分离**。若两者同一把密钥，则"不信任内核"在密码学上不成立——内核既能写账本又能签 checkpoint，对账器无从区分"合法追加"与"内核作弊后的重签"。CT 用独立的 log 私钥签 STH，阙疑应同理准备一把专用账本签名密钥，并在论文中明示其保管与轮换策略。

**更强的产业佐证来自 Pixel Binary Transparency**（Google，Android 固件透明度）。其技术详情页逐字说明 checkpoint 与公钥验证：

> "The log's Merkle tree root hash (included in a *checkpoint*) is located at …/checkpoint.txt. … The checkpoint's signature can be verified using the following public key:"

并给出具体验证语义：

> "Pixel owners can … recompute the root hash and compare it against the root hash contained in the published checkpoint. If they match, then Pixel owners can be assured of some protections…"

一致性证明由第三方主动执行：

> "The append-only behaviour of the transparency log is actively checked by third parties … anyone can monitor the log's consistency. Google has published an open-source implementation of a witness…"

这正是阙疑"不依赖内核的独立对账器"的现成范本：**见证者（witness）只持有 checkpoint 与公钥，不持有内核**。

### 三、包含证明与一致性证明：O(log n) 验证与不信任服务器

两类证明是 CT 可验证性的核心，RFC 6962 第 2.1.1 / 2.1.2 节逐字定义：

- **包含证明（audit / inclusion proof）**——证明某叶确实在树中：
  > "A Merkle audit path for a leaf in a Merkle Hash Tree is the shortest list of additional nodes in the Merkle Tree required to compute the Merkle Tree Hash for that tree. … If the root computed from the audit path matches the true root, then the audit path is proof that the leaf exists in the tree."

- **一致性证明（consistency proof）**——证明"仅追加"、旧记录未被改写/重排：
  > "Merkle consistency proofs prove the append-only property of the tree. A Merkle consistency proof for a Merkle Tree Hash MTH(D[n]) and a previously advertised hash MTH(D[0:m]) of the first m leaves, m <= n, is the list of nodes in the Merkle Tree required to verify that the first m inputs D[0:m] are equal in both trees."

白皮书进一步指出一致性证明还能防御**分视图攻击（split-view attack）**：

> "Furthermore, the fact that it is possible to efficiently check that a log is append-only makes it efficient to detect *split-view attacks*, assuming a sufficient *gossip protocol* is in place for the log checkpoints."

下表归纳三类结构的能力差异（摘自白皮书 Summary 表，逐字整合）：

| 操作 | 可验证日志（Log） | 可验证映射（Map） | 日志派生映射（VLDM） |
|---|---|---|---|
| 证明值包含 | 是，高效 | 是，高效 | 是，高效 |
| 证明值不包含 | 不实际 | 是，高效 | 是，高效 |
| 证明仅追加 | 是，高效 | 否 | 是，高效（需全量审计验证完整正确） |
| 枚举全部条目 | 需全量审计 | 需全量审计 | 需全量审计 |
| 检测分视图 | 是，高效 | 否 | 是，高效 |

**对阙疑的成本含义**：452 条账本，包含证明长度约为树高 `⌈log2(452)⌉ = 9` 个哈希节点（≤ 9×32 = 288 字节），一致性证明长度同样为 O(log n) 量级。这意味着对账器即便是离线、资源受限环境也能在毫秒级完成单条判决的完整性复算——这正是"可独立复算"主张可落地的技术前提。值得提醒：这个 O(log n) 只覆盖"完整性验证"，并不覆盖"正确性验证"。评测者常混淆二者，阙疑若在论文图注或摘要里写"第三方可在毫秒级验证每条判决"，务必补一句"验证的是该判决是否被忠实记录，而非其内容真伪"，否则会被认为偷换概念。RFC 6962 自身也谨慎地只声称审计路径"is proof that the leaf exists in the tree"，从未声称叶内容为真。

### 四、与区块链 / 证书透明度的类比及产业规模（阙疑 452 条账本对照）

Merkle 树既被区块链（比特币、以太坊用 Merkle 证明做轻客户端 SPV 验证）采用，也被证书透明度大规模工业部署。厘清三者差异对阙疑定位至关重要：**区块链用 Merkle 是为了在"无中央信任"前提下让轻客户端验证交易包含性，它用共识（PoW/PoS）替代了中央日志**；而证书透明度与阙疑都保留了"一个被签名的可信 checkpoint"这一中心化锚点，只是把"信任服务器"降级为"只需信任其公钥"。换句话说，阙疑的技术血缘更靠近 CT 而非比特币——它不提供去中心化共识，而是提供"单点诚实签名 + 多方见证"的可审计账本。这与项目"单人科研、双非本科、合肥"的资源现实是匹配的：引入一条公链既无必要也无算力，CT 式的轻量 checkpoint 才是可负担且可发表的方案。

| 维度 | 区块链（PoW） | 证书透明度（RFC 6962/9162） | 阙疑 queyi 账本 |
|---|---|---|---|
| 不可篡改来源 | 算力竞争 + 最长链 | 日志私钥签名 checkpoint + 见证 gossip | 项目签名密钥 checkpoint + 独立对账器 |
| root 含义 | 区块 Merkle root | 32 字节 Merkle Tree Hash（STH） | 32 字节账本 Merkle root |
| 第三方信任假设 | 不信任任何节点，信任多数算力 | 不信任日志服务器，信任公钥+证明 | 不信任内核，信任账本 checkpoint+证明 |
| 规模 | 比特币全量 ~数百 GB | CT 全量"billions of TLS certificates"（certificate.transparency.dev 表述，具体整数**未核实**） | 452 条判决账本（2026-09 实测） |
| 验证成本 | 轻客户端 O(log n) | O(log n) 包含/一致性证明 | 预期 O(log n)，约 288 字节/证明 |

产业规模佐证：
- certificate.transparency.dev 官方站表述 CT "Built using Merkle trees, logs are …" 且是分布式生态，依赖独立可靠日志；ctlogs.dev 直接标榜 "Search **billions** of TLS certificates from all public Certificate Transparency logs"。（精确证书整数未核实，见盲区。）
- Google Trillian（github.com/google/trillian，Apache-2.0）是 CT 的生产级实现，"implements a Merkle tree whose contents are served from a data storage layer, to allow scalability to extremely large trees"，其 Log mode "is now being used in production by several organizations"。这证明 Merkle 日志在亿级规模下工程可行，阙疑 452 条仅是极小子集。
- IEEE/MDPI 2024 论文《Efficient and Universal Merkle Tree Inclusion Proofs via OR Logic》（arXiv:2405.07941）继续优化包含证明的聚合，说明该方向仍是活跃研究热点，阙疑若以"可复算性基准"投稿 E&D 有立足空间。

**落到阙疑的具体数字**：当前 452 条账本若按 entry_index 排序建树，树高 9；即便未来扩到 10 万条，树高也仅约 17，证明体积仍 < 1 KB。这支撑论文"判决可复算"的可扩展性主张——但前提是账本严格 append-only，且 checkpoint 签名密钥与内核部署密钥分离（否则"不信任内核"失去意义）。

---

## 对阙疑的 3 条具体行动

1. **在账本模块落地 Merkle checkpoint 序列化（2027-05 前）。** 于 `gate_engine.py` 或独立 `ledger/` 模块新增函数：将 452 条账本 entry 按 `entry_index` 升序，对每条取 `SHA-256(0x00 || entry_bytes)` 作叶，按 RFC 6962 递归 `SHA-256(0x01 || left || right)` 生成 root；将 `{root(32B), tree_size=452, timestamp, signature}` 写入 `research/ledger_checkpoint_v1.txt`（checkpoint 格式参照 transparency-dev/formats）。在 README 与 REPLICATION.md 写明复算命令，使第三方可不运行内核得到同一 root。

2. **发布"独立对账器"最小实现（参照 Transparency Dev witness 模型）。** 新增 `verify_ledger.py`：**禁止 import `gate_engine` 任何内部符号**，仅输入 checkpoint 文件 + 单条判决 entry，输出 `OK` / `FAILURE`（仿 Pixel verifier 语义）。在 `REPLICATION.md` 给出 `python verify_ledger.py --checkpoint ledger_checkpoint_v1.txt --entry <某判决>` 的端到端示例，证明"不依赖内核即可复算 root"。这直接回应 E&D 对"可复现/可审计"的偏好，也是对抗 NeurIPS AI 生成筛查（Pangram 3.3.2 已 desk reject 18.4% 投稿）的"真代码证据"。

3. **在论文 §5 threat model / limitations 显式区分"账本不可篡改"与"判决正确性"两层断言。** 套用《Verifiable Data Structures》"trust but verify"措辞：root 一致只能证"该判决确实被记录且未被改"（integrity），不能证"判决的事实真值"（validity）。同时把独立对账器文档化进 `research/` 目录，并在论文中明示"我们不声称判决正确，只声称判决可复算、可追、不可回盲"。避免把 Merkle 的完整性保证偷换为内容正确性保证。

---

## 盲区（诚实标注）

- **CT 全量已记录证书精确整数未核实**：certificate.transparency.dev/logs 页面为动态加载（显示 `Loading logs...`），未给出整数；ctlogs.dev 仅写 "billions"。具体如"截至 2024 年 X 亿张"本文未核实，写作"billions"并标注。
- **RFC 9162（v2，2021）对叶子前缀的修订未逐字核实**：v2 将 Merkle Tree Leaf 输入结构与 v1 的 `0x00` 前缀规则做了调整（引入 `0x00`/`0x01` 区分 leaf 与 leaf-input 的哈希前导），阙疑若要声称"对齐 RFC 9162"需 WebFetch 9162 原文确认 §2.1.3 字节；本文未抓取 9162 原文，该处待核实。
- **"不信任内核"在阙疑工程上的确切边界未核实**：是独立进程？独立仓库？脱机复算？项目内尚未文档化。本文按"独立对账器 consumption-only"假设展开，具体部署形态需作者确认，以免论文主张与实现不符。
- **工作树 227 项漂移是否包含账本/checkpoint 文件未核实**：若漂移项含账本或 checkpoint，会直接破坏"append-only"承诺。需作者核查 `git status` 中是否涉及账本路径后再投稿。
- **反事实算子 P=R=F1=0（方向 31 待修）与账本完整性无直接关系，但削弱"判决可复算"整体可信度**：复算的是"已记录判决"，而反事实缺失意味着"未记录判决"无法被证伪，作者应在 limitations 同时披露。
- **Merkle 无法防"日志一开始就把假判决写进账本"**：一致性证明只保证"写进的没被改"，不保证"写进的是真"。阙疑的 guard/protector（9 个）与四态机制才是正确性层面的防线，不应与 Merkle 完整性混为一谈。
- **MMD（最大合并延迟）概念在阙疑尚未定义**：RFC 6962 要求 STH 新鲜度不超过 MMD，阙疑若宣称"账本可被及时发现篡改"，需定义自己的 checkpoint 发布周期（例如每次判决追加即重签，或每日离线批量重签）并写入 REPLICATION.md；否则"及时可见性"只是口头主张。
- **独立对账器的"独立"程度需第三方可核验**：若 `verify_ledger.py` 与内核同仓库、同密钥、同进程调用，reviewer 有理由质疑其独立性。建议对账器以独立仓库/子模块发布，并在 README 用命令演示"仅克隆对账器仓库、不接触内核源码"即可完成复算。

---

## 来源

1. RFC 6962 — Certificate Transparency — Laurie B., Langley A., Kasper E.（Google），IETF 2013/2014 — https://www.rfc-editor.org/rfc/rfc6962.txt — 关键引文："MTH({d(0)}) = SHA-256(0x00 || d(0))"、"MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))"、"The output is a single 32-byte Merkle Tree Hash"、"Each log MUST produce on demand a Signed Tree Head that is no older than the Maximum Merge Delay"。
2. RFC 9162 — Certificate Transparency Version 2.0 — IETF 2021 — https://www.rfc-editor.org/rfc/rfc9162.pdf — CT v2，定义新 Merkle Tree Leaf 结构（具体字节本文未逐字核实）。
3. Verifiable Data Structures（白皮书）— Google TrustFabric 团队，最后更新 2021-05 — https://google.github.io/trillian/docs/papers/VerifiableDataStructures.pdf （及 GitHub Markdown 版 https://github.com/google/trillian/blob/master/docs/VerifiableDataStructures-Latest.md）— 关键引文："allowing an ecosystem to evolve from pure trust, to trust but verify"、"Periodically the log publishes a *checkpoint* that includes a commitment to all entries for a given log size"、"efficiently check that a log is append-only makes it efficient to detect split-view attacks"。
4. Certificate Transparency 官方站 — https://certificate.transparency.dev/ — "Built using Merkle trees, logs are append-only and publicly-auditable ledgers"。
5. Pixel Binary Transparency 技术详情（Android）— Google — https://developers.google.cn/android/binary_transparency/pixel_tech_details?hl=zh-cn — 关键引文："The log's Merkle tree root hash (included in a checkpoint) is located at …/checkpoint.txt … verified using the following public key"、"recompute the root hash and compare it against the root hash contained in the published checkpoint. If they match…"、"The append-only behaviour … is actively checked by third parties … Google has published an open-source implementation of a witness"。
6. Trillian（CT 生产级实现）— Google，Apache-2.0 — https://github.com/google/trillian — "implements a Merkle tree whose contents are served from a data storage layer, to allow scalability to extremely large trees"；Log mode "used in production by several organizations"。
7. RFC 6962 中文翻译 — RFCinfo — https://rfcinfo.com/zh-Hans/rfc-6962/3-4-merkle-tree/ — 中文语境下 0x00 前缀与 MerkleTreeLeaf 结构说明。
8. Efficient and Universal Merkle Tree Inclusion Proofs via OR Logic — arXiv:2405.07941，MDPI 2024 — https://arxiv.org/abs/2405.07941 — 包含证明聚合的近期研究，证明确为活跃方向。
9. QMDB: Quick Merkle Database — arXiv:2501.05262，2025 — https://arxiv.org/html/2501.05262v3 — append-only Merkle tree + Addressable Merkle Tree 的工程实现参考。
10. CTLogs.dev — https://ctlogs.dev/ — "Search billions of TLS certificates from all public Certificate Transparency logs"（具体整数未核实，标注 billions）。
11. Let's Encrypt CT Logs 文档 — https://letsencrypt.org/zh-cn/docs/ct-logs/ — CT 作为关键基础设施、所有证书录入日志的运营侧说明。
12. 二进制 Merkle 哈希树与证书透明度中文综述 — https://gm.okpki.com/wiki/certificate-transparency — RFC 6962 协议与审计架构中文解析（辅助理解，非一手规范）。
