# 600 异族深度调研：供应链溯源证明 —— in-toto/SLSA/OpenTimestamps 在阙疑项目的落地路径与封堵 585 三 meta 攻击的具体方案

> 你是异族调研者（seed evolving），不是苦力建设者。任务是**深度调研供应链溯源证明的具体落地路径**，不是泛泛介绍概念。597 已确认这是"只再引 1 个让可用→令人信服"的选择（P0 缺口，纯标准库可落），你的任务是把它从"概念"变成"可施工的详细方案"。
> 全程只读：不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件；不跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update/git commit|checkout|reset|push；可以跑 git log/status/diff/show/--help/只读 --check/python 只读脚本。
> 产出全落 `C:\CodeLearnling\note\note\C++\CPP-Bible\_arch_v16\`。

---

## 项目背景（先核实再用，不要凭记忆）

阙疑（CPP-Bible）是一个**机器可核验、错误率有上界、可换验证者**的 C++ 知识生产系统。

### 信任根现状（591 后，开工先量）

- `tool_integrity.py`：CORE 5 文件（gate_engine.py / atom_evidence_replay.py / poison_drill.py / toolchain.py / cppbible.py）+ test_config 2 文件（conftest.py / pyproject.toml）的 sha256 基准，存储在 `tools/.tool_checksums`
- `enforce()` 入口闸门：三个真入口（gate_engine.main / atom_evidence_replay.main / poison_drill __main__）第一句强制自检，缺基准/文件缺失/校验异常一律拒绝运行（fail-closed）
- `conftest.py` 启动自检：pytest 收集前校验 test_config 完整性
- `governance_doc_guard.py`：治理文档 manifest + 弱化指令扫描（591）
- `overturned_events.py`：推翻事件通道，human 须过 git 作者绑定（冒名拒写，fail-closed）

### 585 红队实锤的三个 meta 层攻击（必须封堵的目标）

1. **规则供给链攻击**：进程内把命中最多的规则 check 置空，141→64，77 条 finding 静默消失，gate 零告警。tool_integrity 的 sha 基准能检出篡改但 gate 不自我调用、`--update` 重签无需身份——信任根最终只是 git 留痕+人眼。
2. **毒样例自证攻击**：覆盖率 covered 是正则在 poison_drill 自己源码里 grep 文本——注入 0 个真载荷、一行注释即谎报覆盖+1；豁免台账自写一条 id 即被原样接受。
3. **人签文本自证攻击**：直接键入 `human:liaoranran` 即 principal_ok=True——名册挡拼写不挡身份。

### 597 的结论（本次调研的起点）

597 异族巨型调研（_arch_v15/）从 10 个外部领域评估后结论：
- **价值最大 3 理论**：(1) in-toto/SLSA/OpenTimestamps 供应链溯源证明；(2) TLA+/翻译验证；(3) PAC/统计学习
- **只再引 1 个让"可用→令人信服"**：选供应链溯源证明——直击已被攻破的信任根、纯库可落、无需硬件/LLM
- **手搓探针验证**：Merkle 完整性层纯标准库即可落地（108 个 .md，Merkle 根 27c2…、树高 7、篡改检测通过）
- **缺口排序**：P0 信任根 > P1 证明/规约 > P2 统计 > P3 人审 > P4 哲学

**你的任务是把 597 的"供应链溯源证明"从"概念推荐"变成"可施工的详细方案"**——具体到数据结构、文件格式、工具接口、与现有 tool_integrity 的集成方案、封堵 585 三个攻击的具体机制、落地步骤和验收标准。

---

## 调研方向（6 个，每个独立成文件）

### 方向 1：in-toto 深度调研与本项目落地设计

**调研问题**：
- in-toto 的核心概念：layout（布局）、step（步骤）、inspection（检查）、link（链接元数据）、functionary（执行者）、public key（公钥）
- in-toto 的 link 格式：每个步骤产出什么文件、消耗什么文件、命令是什么、材料 hash（materials）、产品 hash（products）、环境信息、签名
- in-toto 的 layout 格式：授权哪些 functionary 执行哪些 step、step 的顺序和依赖、inspection 的命令和期望、layout 的签名和有效期
- in-toto 的验证流程：layout 签名验证 → link 签名验证 → materials/products hash 验证 → step 顺序验证 → inspection 执行
- in-toto 与 SLSA 的关系：SLSA 级别（L0-L4）与 in-toto 的对应关系，SLSA 的 provenance 格式
- **本项目落地设计**：
  - 本项目的"构建步骤"是什么？（卡面编写 → gate 校验 → replay 验证 → poison 攻击测试 → mutation 变异测试 → metrics 采集 → 人审确认）
  - 每个步骤的 functionary 是谁？（人/机器/苦力）
  - 每个步骤的 materials/products 是什么？（输入文件/输出文件的 hash）
  - layout 怎么设计？（步骤顺序、依赖关系、inspection 检查点）
  - link 存在哪里？（data/supply_chain/links/ 目录？）
  - 与现有 tool_integrity 的集成：tool_integrity 是 in-toto 的一个 inspection 吗？还是一个 step？
  - 纯标准库实现 in-toto 的最小子集（不需要完整 in-toto 框架，只实现本项目需要的 link/layout/验证）
  - 签名问题：单用户阶段没有密钥对，用什么替代？（git commit hash + 时间戳？OpenTimestamps？）

**本项目现状**：没有 in-toto，没有 link，没有 layout。tool_integrity 是单点 sha 校验，没有步骤间的溯源链。

**产出要求**：
- in-toto 核心概念的准确解释（附官方文档链接和检索日期）
- 本项目的"构建步骤"清单（每个步骤的 functionary/materials/products/命令）
- layout 设计草案（步骤顺序、依赖、inspection 点）
- link 格式设计（JSON schema，字段定义，示例）
- 纯标准库实现方案（哪些 in-toto 功能需要实现，哪些可以简化/跳过）
- 签名替代方案（单用户阶段，无密钥对）
- 与现有 tool_integrity 的集成方案
- 落地步骤（分阶段，每阶段的交付物和验收标准）
- 成本-收益分析（实现成本 vs 信任根提升）
- 反例：in-toto 的哪些功能不适用本项目（说明原因）
- 外部一手来源（in-toto 官方文档/SLSA 官方文档/论文），标注【已查证】或【一方称】

---

### 方向 2：SLSA 深度调研与本项目级别评估

**调研问题**：
- SLSA（Supply-chain Levels for Software Artifacts）的核心概念：级别（L0-L4）、要求（build/源/依赖/通用）、provenance（溯源证明）
- SLSA 每个级别的具体要求：
  - L0：无要求
  - L1：构建过程有文档，provenance 可用
  - L2：构建服务托管，provenance 经服务签名
  - L3：构建服务不可篡改，provenance 经服务签名且不可伪造
  - L4：所有依赖都达到 L4，双人员审批，可复现构建
- SLSA provenance 格式：build type、builder id、invocation（命令、参数、环境）、build config、metadata（开始时间、完成时间、completeness）、materials（依赖文件的 hash 和 uri）、products（输出文件的 hash）
- SLSA 与 in-toto 的关系：SLSA provenance 是 in-toto link 的一种特定格式
- **本项目 SLSA 级别评估**：
  - 当前本项目达到 SLSA 几级？（逐项评估：构建过程是否有文档？provenance 是否可用？构建是否托管？provenance 是否签名？是否可复现？）
  - 达到 L1 需要做什么？（构建过程文档 + provenance 可用）
  - 达到 L2 需要做什么？（构建服务托管 + provenance 签名——单用户阶段可能达不到，因为没有托管构建服务）
  - 本项目的"SLSA 等价物"是什么？（单用户、本地构建、git 托管，如何定义适合本项目的"供应链安全级别"？）
- **本项目 provenance 设计**：
  - 每个"构建步骤"的 provenance 怎么生成？（苦力批次的 worklog？git commit？tool_integrity 的 sha？）
  - provenance 存在哪里？（data/supply_chain/provenance/ 目录？）
  - provenance 格式（JSON schema，基于 SLSA provenance v1 但适配本项目）
  - 与 in-toto link 的关系（provenance 是 link 的子集？还是 link 是 provenance 的子集？）

**本项目现状**：没有 SLSA 评估，没有 provenance。构建过程是"苦力批次 + git commit + worklog"，没有标准化的 provenance 格式。

**产出要求**：
- SLSA 各级别的准确解释（附官方文档链接和检索日期）
- 本项目当前 SLSA 级别评估（逐项，附证据）
- 达到 L1 的具体行动清单（本项目能达到 L1 吗？需要做什么？）
- L2 及以上的可行性分析（单用户阶段能达到 L2 吗？如果不能，瓶颈是什么？）
- 本项目的"SLSA 等价物"定义（适合单用户本地构建的供应链安全级别）
- provenance 格式设计（JSON schema + 示例）
- provenance 生成方案（每个步骤的 provenance 怎么自动生成？）
- 与 in-toto link 的集成方案
- 成本-收益分析
- 反例：SLSA 的哪些要求不适用本项目（说明原因）
- 外部一手来源，标注【已查证】或【一方称】

---

### 方向 3：OpenTimestamps 深度调研与本项目落地设计

**调研问题**：
- OpenTimestamps 的核心概念：时间戳（timestamp）、日历服务器（calendar server）、Bitcoin 锚定（Bitcoin anchoring）、Merkle 树、证明（proof）
- OpenTimestamps 的工作流程：
  1. 客户端计算文件 hash
  2. 客户端提交 hash 到日历服务器
  3. 日历服务器把多个 hash 组成 Merkle 树
  4. 日历服务器把 Merkle 根写入 Bitcoin 交易（OP_RETURN）
  5. 客户端获取时间戳证明（.ots 文件）
  6. 验证时：客户端用 Bitcoin 区块链验证 Merkle 根，用 Merkle 证明验证文件 hash
- OpenTimestamps 的证明格式（.ots 文件）：header、hash type、Merkle 证明路径、Bitcoin 区块高度、交易 hash
- OpenTimestamps 的验证流程：解析 .ots → 验证 Merkle 证明 → 查询 Bitcoin 区块 → 验证 Merkle 根在区块中 → 验证时间
- OpenTimestamps 的日历服务器：公共服务器列表（https://finney.calendar.eternitywall.com/ 等）、自建日历服务器的方法
- OpenTimestamps 的局限性：需要联网、依赖 Bitcoin、时间精度（约 1 小时，因为 Bitcoin 出块时间）、证明文件大小
- **本项目落地设计**：
  - 哪些文件需要时间戳？（.tool_checksums？governance manifest？overturned_events.jsonl？metrics.jsonl？基线文件 full_baseline_v*.json？）
  - 时间戳证明存在哪里？（data/supply_chain/timestamps/ 目录？与原文件同名加 .ots 后缀？）
  - 什么时候打时间戳？（每个 commit 后？每个批次完成后？关键数据变更后？）
  - 怎么验证时间戳？（CLI 命令：`python tools/timestamp_verify.py <file>`）
  - 纯标准库实现（不需要 ots 客户端，自己实现 .ots 格式解析和验证？还是调用 ots CLI？）
  - 与现有 tool_integrity 的集成：tool_integrity --check 时同时验证时间戳？
  - 与 in-toto/SLSA 的集成：时间戳是 provenance/link 的一个字段？还是独立的证明？
  - 联网问题：本项目环境有 VPN（Hentai VPN），能访问 Bitcoin 节点和日历服务器吗？
  - 单用户阶段的价值：时间戳能证明"这个文件在这个时间之前存在"，对本项目的信任根有什么提升？

**本项目现状**：没有 OpenTimestamps，没有时间戳证明。590 已修正 585 Q6（"可信时间戳结构性无意义"对 OpenTimestamps 不成立），但未实施。

**产出要求**：
- OpenTimestamps 核心概念的准确解释（附官方文档链接和检索日期）
- .ots 文件格式的详细说明（字段定义、二进制格式、示例）
- 验证流程的详细说明（每一步做什么，怎么验证）
- 本项目需要时间戳的文件清单（按优先级排序，说明为什么需要）
- 时间戳证明的存储方案（目录结构、命名规范）
- 打时间戳的时机和频率
- 纯标准库实现方案（自己实现 .ots 解析/验证 vs 调用 ots CLI，对比分析）
- 与 tool_integrity / in-toto / SLSA 的集成方案
- 联网可行性分析（本项目环境能否访问日历服务器和 Bitcoin 节点）
- 时间精度分析（Bitcoin 出块时间约 1 小时，对本项目够用吗？）
- 成本-收益分析（实现成本 vs 信任根提升）
- 反例：OpenTimestamps 的哪些局限性对本项目影响大（说明原因和缓解方案）
- 外部一手来源（OpenTimestamps 官方文档/论文/Bitcoin 相关），标注【已查证】或【一方称】

---

### 方向 4：Merkle 树与哈希链深度调研（597 已手搓探针，本次深化）

**调研问题**：
- Merkle 树的核心概念：叶节点（文件 hash）、内部节点（子节点 hash 的拼接 hash）、根节点（Merkle root）、Merkle 证明（从叶到根的路径）
- Merkle 树的变体：Merkle DAG（有向无环图，IPFS 使用）、Patricia Trie（Ethereum 使用）、Bucket Tree（Certificate Transparency 使用）
- Merkle 证明的验证流程：给定叶节点 hash + 证明路径 + 根节点 hash，验证叶节点在树中
- 哈希链（Hash Chain）的核心概念：H0 = hash(data), H1 = hash(H0), H2 = hash(H1), ...，验证时从 Hn 反推
- Merkle 树 vs 哈希链：适用场景对比（Merkle 树适合集合验证，哈希链适合序列验证）
- Certificate Transparency（CT）的 Merkle 树设计：append-only 日志、Merkle 根定期发布、一致性证明（consistency proof）
- **本项目落地设计**（597 已手搓探针 probes/probe_merkle_integrity.py，108 个 .md，Merkle 根 27c2…、树高 7）：
  - 哪些目录/文件需要 Merkle 树？（atoms/ evidence/ Examples/ Book/ data/mutation/ 基线文件？）
  - Merkle 根存在哪里？（data/supply_chain/merkle_roots.json？每个目录一个根？还是全库一个根？）
  - 什么时候更新 Merkle 根？（每个 commit 后？每个批次完成后？关键数据变更后？）
  - Merkle 证明怎么生成和验证？（CLI 命令：`python tools/merkle_prove.py <file>` / `python tools/merkle_verify.py <file> <proof>`）
  - 与 tool_integrity 的集成：tool_integrity 是单点 sha，Merkle 树是集合完整性，两者什么关系？
  - 与 in-toto 的集成：Merkle 根是 link 的 products 字段？还是独立的完整性证明？
  - 与 OpenTimestamps 的集成：Merkle 根上链（OpenTimestamps），这样整个目录的完整性都有时间戳证明
  - append-only 设计：Merkle 树是否应该是 append-only 的？（文件只能新增，不能修改/删除？如果修改，旧根和新根的关系怎么记录？）
  - 一致性证明（consistency proof）：两个版本的 Merkle 根之间的一致性证明，证明新版本包含旧版本的所有内容
- **597 探针的升级方案**：从手搓探针升级为正式工具（tools/merkle_integrity.py），需要增加什么功能？

**本项目现状**：597 手搓了 Merkle 探针（只读，108 个 .md），但没有正式工具，没有 Merkle 根存储，没有证明生成/验证。

**产出要求**：
- Merkle 树核心概念的准确解释（附原始论文/官方文档链接和检索日期）
- Merkle 证明的格式和验证流程（详细到每一步）
- Merkle DAG / Patricia Trie / Bucket Tree 的对比分析（各自适用场景，本项目适合哪种）
- 哈希链与 Merkle 树的对比（本项目哪些场景适合哈希链？）
- Certificate Transparency 的 append-only 设计对本项目的启发
- 本项目需要 Merkle 树的目录/文件清单（按优先级）
- Merkle 根存储方案（格式、位置、更新时机）
- 正式工具设计（tools/merkle_integrity.py 的接口、命令、输入输出）
- 与 tool_integrity / in-toto / OpenTimestamps 的集成方案
- append-only 设计与一致性证明
- 597 探针的升级方案（从探针到正式工具的差距清单）
- 成本-收益分析
- 反例：Merkle 树的哪些特性不适用本项目（说明原因）
- 外部一手来源，标注【已查证】或【一方称】

---

### 方向 5：封堵 585 三个 meta 攻击的具体方案

**调研问题**：

基于方向 1-4 的调研，设计封堵 585 三个 meta 攻击的具体方案：

#### 攻击 1：规则供给链攻击
- 攻击方式：进程内把命中最多的规则 check 置空，141→64，77 条 finding 静默消失，gate 零告警
- 当前防护：tool_integrity 的 sha 基准能检出篡改，但 gate 不自我调用、--update 重签无需身份
- **封堵方案设计**：
  - in-toto layout：把"规则编写"作为一个 step，functionary 必须是人（git 作者绑定），products 是 gate_engine.py 的 hash
  - in-toto inspection：每次 gate 运行前，inspection 验证 gate_engine.py 的 hash 与 layout 中记录的一致
  - Merkle 树：gate_engine.py + 所有规则定义文件的 Merkle 根，篡改任何一个都会改变根
  - OpenTimestamps：Merkle 根上链，证明"这个规则集在这个时间之前存在"
  - 签名替代：git commit hash + OpenTimestamps 时间戳，作为"规则集版本"的唯一标识
  - 具体机制：gate 运行时，除了 tool_integrity 的 sha 校验，还要验证 Merkle 根和时间戳？还是只验证 sha 就够了？
  - 重签防护：--update 必须经过人审（git 作者绑定 + 理由必填 + 记录到 overturned 通道？）
  - 进程内篡改防护：in-toto 的 inspection 能检测进程内篡改吗？（不能，因为进程内篡改不改变文件 hash。需要其他机制：规则自检？规则间交叉验证？）

#### 攻击 2：毒样例自证攻击
- 攻击方式：覆盖率 covered 是正则在 poison_drill 自己源码里 grep 文本——注入 0 个真载荷、一行注释即谎报覆盖+1；豁免台账自写一条 id 即被原样接受
- 当前防护：581 已改为行为级 covered（真实 gate 命中规则 ID），但豁免台账仍然是自写自验
- **封堵方案设计**：
  - in-toto layout：把"毒样例编写"作为一个 step，functionary 必须是人，products 是 poison_drill.py + 豁免台账的 hash
  - in-toto inspection：每次 poison 运行前，inspection 验证毒样例文件和豁免台账的 hash
  - 豁免台账的人审绑定：新增豁免必须经过人审（git 作者绑定 + 理由必填 + 记录到 supply chain link）
  - 行为级 covered 的强化：581 已改，是否还需要更多防护？（如 covered 规则必须有对应的毒样例测试，测试必须真实触发该规则）
  - Merkle 树：poison_drill.py + 所有毒样例定义 + 豁免台账的 Merkle 根
  - 具体机制：poison 运行时，验证豁免台账的每条豁免都有对应的人审记录和 supply chain link

#### 攻击 3：人签文本自证攻击
- 攻击方式：直接键入 `human:liaoranran` 即 principal_ok=True——名册挡拼写不挡身份
- 当前防护：git 作者绑定（573/592），但单用户阶段 git 作者=自设
- **封堵方案设计**：
  - in-toto layout：把"人审确认"作为一个 step，functionary 的公钥必须在 layout 中授权
  - 单用户阶段没有密钥对，用什么替代身份认证？（OpenTimestamps 时间戳 + git commit hash + 理由文本的组合？）
  - 人审记录的 Merkle 树：所有人审记录的 Merkle 根，篡改任何一条都会改变根
  - 人审记录上链：Merkle 根用 OpenTimestamps 上链，证明"这个人审记录在这个时间之前存在"
  - 身份绑定的强化：git 作者绑定 + OpenTimestamps 时间戳 + 理由文本的 hash，作为"人审身份"的证明
  - 具体机制：人审确认时，生成一条 supply chain link（包含人审者 git 作者、时间、理由、被确认边的 hash），link 的 Merkle 根上链
  - 单用户阶段的局限性：没有真正的身份认证（git 作者可自设），OpenTimestamps 只能证明"存在时间"不能证明"身份"，这是结构性上限

**产出要求**：
- 每个攻击的当前防护评估（哪些已经封堵，哪些没有）
- 每个攻击的封堵方案（具体到工具、文件格式、验证流程、与现有系统的集成）
- 封堵方案的优先级排序（哪些先做，哪些后做，哪些做不到）
- 封堵后的剩余风险（哪些攻击即使封堵后仍然可能，为什么）
- 单用户阶段的结构性上限（哪些防护在单用户阶段无法真正实现）
- 成本-收益分析（每个封堵方案的实现成本 vs 安全提升）
- 验收标准（怎么验证封堵方案有效？可以用 585 的攻击脚本做回归测试）
- 外部一手来源，标注【已查证】或【一方称】

---

### 方向 6：落地路线图与分阶段实施方案

**调研问题**：

基于方向 1-5 的调研，制定供应链溯源证明的落地路线图：

#### 阶段划分

- **阶段 0：基线与评估**（无代码改动）
  - 评估当前信任根现状（tool_integrity 的覆盖范围、sha 基准的管理方式、入口闸门的覆盖率）
  - 评估 585 三个攻击的当前防护状态
  - 评估本项目的 SLSA 级别
  - 产出：信任根现状评估报告 + 攻击防护状态矩阵

- **阶段 1：Merkle 完整性层**（纯标准库，最小落地）
  - 实现 tools/merkle_integrity.py（Merkle 树生成、证明生成、验证）
  - 覆盖目录：atoms/ evidence/ Examples/ Book/ data/mutation/ 基线文件
  - Merkle 根存储：data/supply_chain/merkle_roots.json
  - 与 tool_integrity 集成：tool_integrity --check 时同时验证 Merkle 根
  - 验收：篡改任何一个被覆盖文件，Merkle 验证失败；585 攻击脚本回归测试
  - 预计工作量：小（597 已手搓探针，升级为正式工具）

- **阶段 2：in-toto 风格溯源链**（纯标准库，最小子集）
  - 实现 tools/supply_chain.py（link 生成、layout 验证、inspection 执行）
  - 定义本项目的"构建步骤"（卡面编写 → gate 校验 → replay 验证 → poison 测试 → mutation 测试 → metrics 采集 → 人审确认）
  - 每个步骤生成 link（materials/products hash、命令、functionary、时间戳）
  - layout 设计（步骤顺序、依赖、inspection 点）
  - 与 tool_integrity 集成：tool_integrity 是一个 inspection
  - 签名替代：git commit hash + 时间戳
  - 验收：每个步骤的 link 可验证；篡改任何步骤的 products，后续 inspection 失败
  - 预计工作量：中

- **阶段 3：OpenTimestamps 外部时间锚**（需要联网）
  - 实现 tools/timestamp.py（时间戳生成、验证）
  - 覆盖文件：.tool_checksums、Merkle 根、关键 link、基线文件
  - 时间戳证明存储：data/supply_chain/timestamps/
  - 与 Merkle 树集成：Merkle 根上链（一次时间戳证明整个目录的存在时间）
  - 与 in-toto 集成：时间戳是 link 的一个字段
  - 验收：关键文件的时间戳可验证；篡改文件后，时间戳验证仍然通过（因为时间戳证明的是"旧文件存在时间"，不是"新文件完整性"——需要与 Merkle 根配合）
  - 预计工作量：中（需要联网，可能需要处理 VPN 问题）

- **阶段 4：SLSA L1 等价物 + 封堵 585 攻击**（集成与强化）
  - 实现 provenance 生成（每个构建步骤的 provenance，基于 SLSA provenance v1 格式）
  - 封堵 585 攻击 1（规则供给链）：Merkle 树 + in-toto inspection + 重签人审绑定
  - 封堵 585 攻击 2（毒样例自证）：豁免台账人审绑定 + Merkle 树
  - 封堵 585 攻击 3（人签自证）：人审记录 Merkle 树 + OpenTimestamps + git 作者绑定
  - 本项目的"SLSA L1 等价物"定义与达成
  - 验收：585 三个攻击脚本全部无法再攻破；信任根从"自签"变"可独立验证"
  - 预计工作量：大

#### 每阶段的交付物、验收标准、依赖关系、风险

**产出要求**：
- 阶段 0-4 的详细实施方案（每个阶段的目标、交付物、工具、文件格式、验收标准）
- 阶段间的依赖关系（哪些阶段必须按顺序，哪些可以并行）
- 每个阶段的预计工作量（小/中/大，基于代码行数和复杂度估算）
- 每个阶段的风险（技术风险、依赖风险、环境风险）
- 每个阶段的成本-收益分析
- 关键决策点（哪些决策需要用户裁决，如签名替代方案、SLSA 级别目标）
- 与现有系统的集成方案（tool_integrity / gate_engine / poison_drill / overturned_events）
- 测试策略（怎么验证每个阶段的交付物有效？585 攻击脚本的回归测试）
- 外部一手来源，标注【已查证】或【一方称】

---

## 交付物清单（12 件）

1. `00_总览_供应链溯源证明落地路径_封堵585三meta攻击.md`——总览矩阵 + 核心结论 + 阶段路线图 + "如果只做一件事先做什么"
2. `01_in-toto深度调研与本项目落地设计.md`
3. `02_SLSA深度调研与本项目级别评估.md`
4. `03_OpenTimestamps深度调研与本项目落地设计.md`
5. `04_Merkle树与哈希链深度调研.md`
6. `05_封堵585三个meta攻击的具体方案.md`
7. `06_落地路线图与分阶段实施方案.md`
8. `07_数据结构与文件格式设计.md`——link/layout/provenance/Merkle根/时间戳证明的 JSON schema
9. `08_工具接口设计.md`——merkle_integrity.py / supply_chain.py / timestamp.py 的 CLI 接口设计
10. `09_与现有系统集成方案.md`——与 tool_integrity / gate_engine / poison_drill / overturned_events 的集成
11. `probes/`——如有手搓实验（如 in-toto link 的最小实现、Merkle 证明的验证），放这里
12. `zero_pollution.md`——git 自证

---

## 调研纪律

1. **先核实再用**：项目现状以实跑为准，不要凭记忆或 560-597 的旧结论。开工先跑 `gate_engine.py --check`、`tool_integrity.py --check` 记录基线。
2. **所有判断附证据**：文件路径+行号/命令输出/外部链接+检索日期，区分"已查证"和"一方称"，算不出的明说缺什么，不编数字。
3. **发现旧调研错了直接指出来**：附证据，不要客气。特别是 597 的结论（如果 600 深入调研后发现 597 有错误或遗漏）。
4. **深度调研，不是泛泛介绍**：每个方向都要具体到"本项目怎么落地"，包括数据结构、文件格式、工具接口、验收标准。不要只说"in-toto 是一个供应链安全框架"就完了。
5. **成本-收益分析必须诚实**：不要只说"这个方案好"，要说"实现成本是多少（代码行数/学习成本/时间）、收益是什么（封堵哪些攻击/信任根提升多少）、是否值得"。
6. **反例必须写**：每个方向至少写 2 个"看似相关但实际不适用"的反例，说明原因。避免盲目引入。
7. **单用户阶段的结构性上限必须明说**：没有密钥对、git 作者可自设、没有托管构建服务——这些是单用户阶段无法真正解决的，必须明说，不能假装能解决。
8. **全程只读**：不修改任何正式文件，不跑会写盘的命令，不 commit/checkout/reset/push。
9. **收尾 git status 自证**：仅新增 _arch_v16/，既有 modified（full_baseline_v4.json、EV-CONC-001.md 的 CRLF 假脏）原状未动。

---

## 00 总览开头必须写的两句话

完成 12 件交付物后，在 `00_总览` 开头写两句话贴回：

① **供应链溯源证明的四个阶段（Merkle → in-toto → OpenTimestamps → 封堵585）中，哪个阶段性价比最高、哪个阶段在单用户环境下有结构性上限、最意外的发现是什么**；

② **如果只允许先做一个阶段（最小落地），选哪个、为什么、做完后能封堵 585 的几个攻击**。
