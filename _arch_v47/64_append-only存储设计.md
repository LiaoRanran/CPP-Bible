# 方向64：Append-only存储设计——用不可变日志为452条判决建立可重放的信任底座

## 一、问题定位：判决为什么只能被追加，不能被覆盖

阙疑verifier当前有37张实卡、67条规则、9个保护器、452条append-only账本记录，内核约3826行；它在30条盲测holdout（含17条真错）上检出率66.7%，在40条外部corpus上检出率43.8%且存在算术不自洽。这个系统的学术目标是NeurIPS 2027 E&D赛道，而它最需要向审稿人证明的不是某条规则多聪明，而是：每一次判决从何而来、被什么证据触发、后来为何改变，全部可以独立重放和审计。

原地更新（in-place update）是这个目标的对立面。若一条判决从 block 被直接改写成 warn，旧状态在存储介质上消失，事后将无法回答四个问题：旧判决是否存在过、改写发生在什么时间、改写由哪次规则变更触发、改写者是谁。覆盖式写入还把两类完全不同的事故混在一起：崩溃恢复时的页撕裂（torn page）和人为篡改。Append-only 存储的核心立场因此不是"性能"，而是把"状态"重新定义为"事件流的折叠结果"——当前判决永远等于从第一条事件开始按确定性函数回放（replay）得到的派生物，原始事件一旦写入即不可变。

本方向要回答三个工程问题：第一，不可变日志如何在崩溃后恢复，即 WAL/ARIES 的遗产；第二，不可变日志如何检测篡改，即哈希链与校验；第三，不可变日志如何支持独立对账，即 replay 架构。方向62已经深入讨论了 SQLite 的具体配置（WAL 模式、synchronous=FULL、3.51.3 修复的 WAL-reset bug），本篇不重复配置细节，聚焦设计范式本身及其与452条账本的映射；方向65、66分别讨论 Merkle 树与完整性校验，可互为参照。

## 二、技术谱系：从ARIES到LSM-tree的五十年

**1. WAL 与 ARIES：先写日志，再改数据。** Mohan、Haderle、Lindsay、Pirahesh 与 Schwarz 在 1992 年发表于 ACM Transactions on Database Systems（17卷1期，94–162页）的 ARIES 论文，确立了现代数据库崩溃恢复的标准范式[1]。其三条核心原则是：write-ahead logging（任何页修改落盘前，对应的日志记录必须先落盘）、repeating history（重启时先用 redo 把所有已记录更新重做一遍，精确重现崩溃前状态，再对未提交事务做 undo）、以及记录日志序列号 LSN（每个页头部保存最近修改它的日志 LSN，redo 时据此跳过已生效的记录，保证幂等）。ARIES 还支持 fuzzy checkpoint：检查点本身不要求刷完所有脏页，只记录脏页表与最老 LSN，恢复因而有界。关键洞察是：日志不只是"备份"，它是按时间全序排列、只能追加的真相源；数据页反而是可以从日志重建的派生缓存。

**2. LSM-tree：把随机写变成顺序追加。** O'Neil、Cheng、Gawlick 与 O'Neil 1996 年发表于 Acta Informatica（33卷4期，351–385页）的 Log-Structured Merge-Tree 论文，针对 B+ 树随机写代价高的问题提出：写入先进内存结构（memtable），满了以后整体 flush 成磁盘上不可变的有序文件；查询时合并各层结果；后台 compaction 将多层有序文件归并、清除过期与删除项[2]。LevelDB、RocksDB、HBase、Cassandra 均为其后裔。LSM 的代价是写放大（write amplification）：一条逻辑记录在多层 compaction 中被反复重写，工程系统常见放大约 10 倍量级；读放大则表现为一次查询可能要访问多个层。这个权衡对阙疑几乎不构成问题——452条记录总量按每条约数百到数千字节估算仅 MB 级，任何放大都可忽略；真正值得继承的是"不可变文件 + 后台归并"的分层思想。

**3. SQLite WAL 模式。** SQLite 自 3.7.0（2010-07-21）起提供 WAL：写操作追加到 WAL 文件尾部，读操作继续读主库文件，读写互不阻塞；默认当 WAL 达到 1000 页（约4MB）时自动 checkpoint 回主库[3]。方向62已记录其官方文档的关键安全性质与 WAL-reset bug（3.7.0–3.51.2，2026-03 的 3.51.3 修复），此处只强调一条架构结论：对账本这类数据，应当配置 WAL + synchronous=FULL，并且内核引擎与独立对账器若共用同一数据库，必须保证单写者或升级到 3.51.3，否则竞态可能损坏库文件。

**4. Kafka：分段日志与 offset。** Kafka 的官方实现文档把分区存储描述为"有序、不可变、持续追加的提交日志"[5][6]。具体机制包括：日志串行追加到当前段文件，达到配置大小（segment.bytes 默认 1073741824，即1 GiB）后滚动新段；每条消息用一个64位 offset 唯一标识；每个段文件以其首条消息的 offset 命名（如 00000000000000000000.log）；删除以整段为单位按时间或大小执行。持久化强度由两个旋钮控制：每 M 条消息或每 S 秒强制 flush，崩溃时最多损失 M 条或 S 秒。offset 设计尤其有启发：消息标识不靠中心化分配的 GUID，而靠分区内单调递增的位置整数——这与判决账本需要的"序号即身份"完全同构。

**5. Bitcoin：区块哈希链。** Nakamoto 2008 年白皮书设计了另一种 append-only 结构：交易打包进区块，每个区块头包含前一区块的哈希，形成哈希链；SHA-256双重哈希、工作量证明使历史重写在算力上不可行[7]。创世块于 2009-01-03 挖出，区块头仅80字节，难度每2016块（约两周）调整以维持约10分钟的平均出块时间。篡改任何旧区块都会改变其哈希，从而断裂之后全部链接——篡改检测不需要信任任何中心节点，只靠逐链验证即可。阙疑不需要工作量证明（账本不面对拜占庭节点），但"每条记录包含前驱哈希"是其直接可借的结构。

**6. CRC32C：记录级校验。** CRC32C 使用 Castagnoli 多项式 0x1EDC6F41，定义于 iSCSI 标准 RFC 3720 第12.1节，SCTP 也在 RFC 3309 中改用它[8]。相较传统 CRC-32（ISO 3309 多项式），CRC32C 在相同位长下对短数据的检错能力更强，且自 Intel Nehalem 起有 SSE4.2 指令级硬件加速，单条记录校验是纳秒级开销。它只防意外损坏（位翻转、截断、拼接错误），不防蓄意篡改——攻击者可以重算校验，因此完整性必须哈希链负责，二者分层。

**7. fsync 与落盘语义。** fsync 的名义语义是"返回成功后，该文件此前所有写操作都已到达持久介质"，man-pages 与 PostgreSQL 文档都警告：操作系统页缓存、磁盘控制器易失写缓存、消费级 SSD 没有掉电保护（PLP）都会使该语义打折[9][11]。2018 年的 "fsyncgate" 事件是真实案例：Linux 内核在异步写回失败时标记错误页，PostgreSQL 首次 fsync 收到 EIO，但该次 fsync 同时清除了错误标志；重试 fsync 成功，而数据其实从未落盘，造成静默丢失[10]。此外只 fsync 文件并不保证目录项持久，创建或 rename 后还需 fsync 父目录。工程教训是：fsync 失败必须按致命错误处理（停服、靠日志重做），绝不盲目重试。

## 三、对阙疑452条账本的具体映射

**映射1：判决更新只能追加"判决事件"，当前状态由回放得到。** 账本中禁止 UPDATE 语义。一次规则对一张卡的判决落盘为一条不可变事件，建议字段包括：`seq`（账本内单调递增整数，仿 Kafka offset）、`ts_utc`、`card_id`、`rule_id` 与规则版本、`protector_id`、`verdict`（四态之一）、`evidence_ref`（编译器版本、编译选项、sanitizer 报告、夹具 ID）、`input_content_hash`（被审代码/卡片快照哈希）、`crc32c`、`prev_event_hash` 以及本事件自身哈希。判决从 block 变 warn 不是修改旧记录，而是追加一条新事件；查询"当前判决"= 对该 card_id 的事件流按 seq 回放取最后状态。这样任何历史时刻的判决集合都可通过"回放至 seq=N"精确重建——审稿人若质疑某条 holdout 判决何时产生，账本可以给出确定性答案。

**映射2：previous_verdict_hash 构成账本内哈希链。** 仿 Bitcoin 区块头，每条事件的 `prev_event_hash` 指向前一条事件（或按 card 维度为 `prev_verdict_hash`）的 SHA-256 哈希。任一条记录被改写，其哈希变化立刻断裂后续全部链接；检测程序从创世事件重放链即可定位第一个断点。注意哈希链的能力边界写在前面：它检测改写，不证明原始内容正确，也不阻止持有写权限者重算整条链（链尾重写仍需外部锚点，见映射4）。因此哈希链是篡改检测的必要件，不是充分件。

**映射3：独立 replay 对账，仿 ARIES 的 repeating history。** 阙疑应保持一个与内核 gate_engine 物理隔离的独立对账器：它不信任内核输出的当前判决表，只读原始事件流，从 seq=1 开始按确定性规则重放全部452条记录，重算每张卡当前状态，再与内核状态表逐字段比对。这正是 ARIES "重放历史"思想的工程化——redo 逻辑必须幂等（同一条事件重放任意次结果一致），对账差异本身构成最高优先级警报。方向62记录的 WAL-reset bug 说明双进程并发写同一 SQLite 文件有真实风险，所以对账器应使用只读连接、读事件文件的离线副本，或严格保证单写者。崩溃恢复走同一条路径：重启即重放，未形成完整事件（无哈希、无 CRC 校验通过）的尾部记录丢弃。

**映射4：外部锚点防链尾重写。** 哈希链防得住单点改记录，防不住有权限者从某条起重算整链。低成本对策是定期把账本链顶哈希（chain tip hash）写到带外位置：每次发布前打印到发布记录、写入离线备份文件、或作为 artifact 的一部分分发。这样事后可独立验证"当时的链顶"与"现在的历史"一致。每次 checkpoint 还应固化一个只读快照：在 SQLite 上先做 checkpoint、关闭全部连接，再分发单文件（方向62已记录 WAL 下需同时处理 -wal/-shm 的陷阱）。

**映射5：compaction 的位置必须划清。** LSM 的 compaction 优化的是存储引擎内部表示；阙疑的原始判决日志永不 compaction、永不删除——它是法律意义上的原始凭证。可以在原始日志之上维护"当前判决表"这类物化视图，视图随时可由重放重建，重建等价于 ARIES 恢复与 LSM compaction 的合体，但任何 compaction 结果不得回流覆盖原始日志。以452条、MB 级的规模，根本没有做物理 compaction 的必要；真正要防的是未来图省事引入的"归档时删旧日志"。

**映射6：holdout 与外部 corpus 的判决同等记账。** 30条 holdout 的每次判决与判决变化也必须走同一 append-only 通道，并标注 `batch=holdout`、盲测轮次。这样可以防止"看完答案改规则再重测"的污染：规则版本、预测时间、揭盲时间全部在事件流上可查，检出率66.7%才是可审计数字而非可调数字。外部40条 corpus 判决及算术不自洽的修正过程同理，修正前后的差额必须留痕。

## 四、失败模式与类比边界

第一，append-only 保证可追溯，不保证内容正确。一条错误判决、一条投毒事件同样可以被完美地永久记录；哈希回答"是否与写入时一致"，回答不了"写入时是否为真"。第二，fsync 语义依赖完整存储栈：fsyncgate 证明应用层无法完全获知异步写失败，控制器易失缓存和无 PLP 的 SSD 会让"已提交"在掉电后消失；正确姿势是 fsync 失败即 PANIC、重做日志，而非重试。第三，哈希链不防内部合法写入者重写链尾，必须有带外锚点。第四，单调序号依赖时钟与单写者：单机批量追加场景风险低，但仍需用逻辑 seq 而非墙钟作为主键，以防时钟回拨。第五，LSM 写放大在本规模无需考虑，不要为想象中的性能问题提前引入 compaction，那反而破坏原始日志。

## 五、对阙疑的三条具体行动、盲区与来源

**对阙疑的三条具体行动：**

1. **2026-12 前**，完成账本事件 schema 升级：为452条历史记录一次性回填 `seq`、`crc32c`、`prev_event_hash`，写幂等迁移脚本并保留迁移前完整备份；内核写入路径改为只追加，代码层禁用任何 UPDATE 判决状态的接口。
2. **2027-02 前**，交付独立 replay 对账器（只读、离线副本、与内核不同进程）：每次规则发布前重放全量账本并与内核状态表逐字段比对，差异即阻断发布；同时在崩溃恢复路径上复用同一重放逻辑，完成至少3次断电/杀进程注入演练。
3. **2027-04 前**（NeurIPS 2027 摘要节点之前），产出可分发的账本审计 artifact：checkpoint 后的单文件快照、链顶哈希带外记录、以及"从空库重放到452条"的一键脚本与耗时报告，作为论文补充材料提交。

**盲区：**

1. 本文引用的写放大约10倍等工程数字来自通用 LSM 系统经验，阙疑未在自有负载上实测，只能作量级参考。
2. CRC32C 与 SHA-256 的残余碰撞概率在本规模下可忽略，但论文中若声称"密码学保证"仍需限定为检测而非证明。
3. 单机单写者是当前架构假设；若未来内核与对账器并发模型改变，WAL-reset 类竞态需重新评估。
4. 带外锚点的安全性依赖发布渠道本身，若发布记录与账本同机失守，锚定失效。
5. 历史回填无法恢复"迁移前已被覆盖删除"的判决——若旧账本曾被原地修改，那段历史在物理上已不可考。

**来源：**

1. Mohan, C., Haderle, D., Lindsay, B., Pirahesh, H. & Schwarz, P. (1992), *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging*, ACM TODS 17(1):94–162：https://people.eecs.berkeley.edu/~prabal/teaching/resources/eecs582/mohan92aries.pdf
2. O'Neil, P., Cheng, E., Gawlick, D. & O'Neil, E. (1996), *The Log-Structured Merge-Tree (LSM-Tree)*, Acta Informatica 33(4):351–385：https://link.springer.com/article/10.1007/s002360050048
3. SQLite 官方文档，*Write-Ahead Logging*：https://www.sqlite.org/wal.html
4. SQLite 官方文档，*Atomic Commit In SQLite*：https://www.sqlite.org/atomiccommit.html
5. Apache Kafka，*Log（Implementation）*：https://kafka.apache.org/42/implementation/log/
6. Apache Kafka 0.8 文档，*Topics and Logs*：https://kafka.apache.org/08/documentation.html
7. Nakamoto, S. (2008), *Bitcoin: A Peer-to-Peer Electronic Cash System*：https://bitcoin.org/bitcoin.pdf
8. IETF RFC 3720，*Internet Small Computer Systems Interface (iSCSI)*，CRC32C 见第12.1节：https://datatracker.ietf.org/doc/html/rfc3720
9. Linux man-pages，*fsync(2)*：https://man7.org/linux/man-pages/man2/fsync.2.html
10. Dan Luu，*Fsyncgate: errors on fsync are unrecoverable*（2018 邮件档归档）：https://danluu.com/fsyncgate/
11. PostgreSQL 文档，*Reliability and the Write-Ahead Log*：https://www.postgresql.org/docs/current/wal-reliability.html
12. Google LevelDB，*LevelDB Design Doc*：https://github.com/google/leveldb/blob/main/doc/design.md
