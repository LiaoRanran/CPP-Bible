# 方向 68：向量数据库与 embedding 检索（HNSW / IVF-PQ 原理、实测权衡、选型、在「知识卡去重与相似断言检索」上的最小可行方案）

> 调研时间：2026-09-29｜调研员：方向 68–79 组｜真实搜索 14 次（含 4 次 WebFetch 逐字取数）
> 本文服务两个目的：(a) 阙疑的 37 实卡 / 452 判决到底该不该上向量库；(b) 若上，用什么、用什么指标证明它有效。

---

## 核心结论

1. **在阙疑的规模上，ANN 索引的「召回率–延迟权衡」是一个伪问题，真问题是「阈值标定」。** HNSW 的价值来自对数级复杂度缩放（Malkov & Yashunin, *IEEE TPAMI* 42(4):824–836, 2020-04-01, DOI 10.1109/TPAMI.2018.2889473 原文：*"allows a logarithmic complexity scaling"*），但阙疑只有 **37 实卡 + 452 判决**，暴力精确检索在 384 维下的开销是微秒级——**ANN 在 n≈10³ 以下不省时间，只引入近似误差**。pgvector 官方调优文档（ParadeDB, *Tuning pgvector Performance*）明确写：*"Without an index, pgvector falls back to a sequential scan... That is fine for tens of thousands of vectors and untenable beyond that."* 阙疑离"tens of thousands"还差两个数量级。
2. **如果一定要选，嵌入式场景的正确答案是 sqlite-vec，但它自己都还是 pre-v1。** `sqlite-vec` 仓库 README 逐字写 *"⚠️ sqlite-vec is a pre-v1, so expect breaking changes!"*，最新版本 **v0.1.10-alpha.4（commit 04d28bd, 2026-05-18）**，纯 C、零依赖、*"runs anywhere SQLite runs (Linux/MacOS/Windows, in the browser with WASM, Raspberry Pis, etc.)"*；ANN 支持（flat / IVF / DiskANN）是后来以 PR #273/#279 加进去的。**结论：把它当作"可替换的实验性组件"，不要写进论文的核心贡献路径**——审稿人会问"你的核心可复算性依赖一个 alpha 库？"
3. **真正值得写进论文的不是"我们用了向量库"，而是"我们用 embedding 做了一次可审计的相似断言检索，并给出了召回率的精确二项置信区间"。** SemDeDup（Abbas, Tirumala, Simig, Ganguli, Morcos, arXiv:2303.09540, 2023-03-16）证明 embedding 去重能在移除 **50%** 数据的同时"minimal performance loss"、训练时间减半——这是一个**可复现的、有数字的**方法学先例。阙疑应当照抄它的**评测骨架**（阈值扫描 + 保留集性能曲线），而不是照抄它的规模。

---

## 精确数字与案例

### 一、HNSW 与 IVF-PQ 的机制与官方参数默认值（逐字）

**HNSW**：论文摘要逐字——*"Hierarchical NSW incrementally builds a multi-layer structure consisting of a hierarchical set of proximity graphs (layers) for nested subsets of the stored elements. The maximum layer in which an element is present is selected randomly with an exponentially decaying probability distribution."* 关键点：**层号随机（指数衰减）**，因此不需要额外粗筛结构；*"Similarity of the algorithm to the skip list structure allows straightforward balanced distributed implementation."*

**pgvector 的 HNSW 三个旋钮**（ParadeDB 官方调优文，pgvector 0.8.x 语义）：

| 参数 | 默认值 | 合法范围 | 作用与调法（逐字要点） |
|---|---|---|---|
| `m` | **16** | 2–100 | 每节点双向链接数；`16` 是强默认，仅在 recall 不够时提到 24 或 32 |
| `ef_construction` | **64** | 4–100（必须 ≥ 2×m） | 建图时候选列表大小；可用区间 64–200 |
| `hnsw.ef_search` | **40** | 查询期 | *"the main recall/latency dial you actually turn in production"*，成本随该值**近似线性**增长 |

第三方调优博客（queryplane.com，*Tuning HNSW Indexes in pgvector*）给出经验区间：*"set ef_search between 100 and 200, which typically yields 95%+ recall at sub-5ms query times on real embeddings."* 另一个来源（GitHub `adrianhajdin/podcast-sujata` 的 pgvector skill 参考）给出更细的近似表，**该表来源不明，标注为"未核实"**：

| ef_search | 近似召回 | 相对速度 |
|---|---|---|
| 40 | 较低（某些 benchmark 约 95%） | 1×（基线） |
| 100 | 较高 | 约慢 2× |
| 200 | 很高 | 约慢 4× |
| 400 | 近精确 | 约慢 8× |

**pgvector 的 IVFFlat 参数**：`lists` 的常用起点是 *"rows / 1000 up to one million rows, and sqrt(rows) beyond that"*；`ivfflat.probes` 默认 **1**，合理起点是 `sqrt(lists)`。**关键警告（逐字）**：*"IVFFlat indexes should be built after representative data is loaded. Building on an empty or small table produces poor clusters that hurt recall even after more data arrives."* 这条对阙疑的启示是**决定性的**：知识卡是会持续新增的（37 → 未来 100+），IVFFlat 的聚类中心在建库时冻结，**随数据增长 recall 会退化**；HNSW 无训练步骤，可在空表上建。

**pgvector 0.8.0 新增**（逐字）：`halfvec`（*"50% smaller storage and indexes with minimal recall loss"*）、`binary_quantize`、`iterative_scan`（三档 `off` / `strict_order` / `relaxed_order`，用于带 WHERE 过滤的向量查询——**这正好对应阙疑"按卡号/标签过滤后再找相似断言"的场景**）。

**IVF-PQ（Milvus 官方文档逐字）**：

| 参数 | 默认 | 范围 | 官方调优建议（逐字） |
|---|---|---|---|
| `nlist` | **128** | [1, 65536] | *"In most cases, we recommend you set a value within this range: [32, 4096]"* |
| `m`（子向量数） | 无默认 | [1, 65536] | 必须整除 D；*"A commonly recommended value is m = D/2"*；建议区间 [D/8, D] |
| `nbits` | **8** | [1, 24] | 每子空间码本含 2^nbits 个质心；建议区间 [1, 16] |
| `nprobe` | **8** | [1, nlist] | 查询时搜索的簇数；越大 recall 越高、延迟越大 |

**压缩比算例（逐字）**：D=128、m=64、nbits=8 时，原始向量 128×32 = **4096 bits**，PQ 压缩后 64×8 = **512 bits**，即 **8× 压缩**。注意这是官方给的**保守算例**；中文技术博客常引用"20–50 倍"（CSDN 2026-09-15），**该数字未在 Milvus 官方页出现，标注为未核实**。

**一个 2024-12 的反向结果值得记录**：arXiv:2412.01940《Down with the Hierarchy: The 'H' in HNSW Stands for "Hubs"》（v3 2025-07-03）声称 *"a flat navigable small world graph retains all of the benefits of HNSW on high-dimensional datasets"*——**层级可能不是必需的，真正起作用的是 hub 节点**。这意味着"HNSW 是最优图索引"不是定论。

### 二、召回率–延迟实测：Qdrant 官方 benchmark 的逐字数字

来源：`qdrant.tech/benchmarks/`，单节点 benchmark 标注 *"Updated: January/June 2024"*；过滤搜索 benchmark 标注 *"Updated: Feb 2023"*。测试环境逐字：**Server = 8 vcpus / 32 GiB / 64 GiB（Azure Standard D8s v3）**，**Client = 8 vcpus / 16 GiB（Standard D8ls v5）**，所有引擎跑在 Docker 内并限制 **25 GB 内存**。

数据集逐字：

| 数据集 | 向量数 | 维度 | 距离 |
|---|---|---|---|
| `dbpedia-openai-1M-angular` | 1M | 1536 | cosine |
| `deep-image-96-angular` | 10M | 96 | cosine |
| `gist-960-euclidean` | 1M | 960 | euclidean |
| `glove-100-angular` | 1.2M | 100 | cosine |

`dbpedia-openai-1M-1536-angular`、100 搜索线程下的聚合结果（逐字）：

| 引擎配置 | 上传(min) | 上传+建索引(min) | 延迟(ms) | P95(ms) | P99(ms) | RPS | Precision |
|---|---|---|---|---|---|---|---|
| qdrant `sq-rps-m-64-ef-512` | 3.51 | 24.43 | **3.54** | 4.95 | 8.62 | **1238.00** | 0.99（原页排版为 160.99） |
| weaviate `m32` | 13.94 | 13.94 | 4.99 | 7.16 | 11.33 | 1142.13 | 0.97 |
| elasticsearch `m-32-ef-128` | 19.18 | 83.72 | 22.10 | 72.53 | 135.68 | 716.80 | 0.98 |
| redis `m-32-ef-256` | 92.49 | 92.49 | 140.65 | 160.85 | 167.35 | 625.27 | 0.97 |
| milvus `m-16-ef-128` | 0.27 | **1.16** | 393.31 | 441.32 | 576.65 | 219.11 | 0.99 |

**Qdrant 自己的方法论声明（逐字，值得阙疑在论文里引用）**：
> *"Select a precision threshold that would be satisfactory for your usecase. This is important because ANN search is all about trading precision for speed. This means in any vector search benchmark, two results must be compared only when you have similar precision. However most benchmarks miss this critical aspect."*
> *"There is one important thing - the speed of the vector search engines should to be compared only if they achieve the same precision."*

**过滤搜索下 HNSW 会「精度崩塌」（逐字）**：
> *"Accuracy collapse - some engines are losing accuracy dramatically under some filters. It is related to the fact that the HNSW graph becomes disconnected, and the search becomes unreliable."*

**这一条对阙疑是硬约束**：如果将来在向量检索上加 `WHERE card_id IN (...)` 或 `WHERE status='verified'` 之类的过滤（阙疑**必然**要加，因为只有 verified 卡才该参与断言相似性比对），HNSW 的图可能被过滤条件切断，recall 会**断崖式下跌而不是平滑下降**。pgvector 0.8.0 的 `iterative_scan` 正是为此而设。**在 n=37 的场景里，唯一稳妥的做法是不建索引、暴力精确检索。**

### 三、五个候选引擎的横评（版本号 / 体积 / 是否需 server）

| 引擎 | 形态 | 需要独立 server | 版本锚点 | 关键限制 |
|---|---|---|---|---|
| **pgvector** | PostgreSQL 扩展 | **需要**（PostgreSQL 进程） | 0.8.0 起有 `halfvec` / `binary_quantize` / `iterative_scan`（0.8.x 语义） | 引入一个完整 PG 部署；单人科研机上属重型依赖 |
| **sqlite-vec** | SQLite 扩展（纯 C） | **不需要** | **v0.1.10-alpha.4**（commit `04d28bd`, 2026-05-18） | **pre-v1，官方明示会有破坏性变更**；ANN（flat/IVF/DiskANN）为后加功能 |
| **Chroma** | 嵌入式 + Cloud | 本地模式不需要 | **1.0.0**（官方公告：本地版 **4× faster**，写/查 **3–5×**） | Rust 重写核心；公告基准为 **1M 条 OpenAI 1536 维向量 / 12 核 M2 MacBook**（注意：该基准**不是** 37 条向量的场景） |
| **Qdrant** | Rust server | **需要** | 官方 benchmark 页 2024-01/06 更新 | 功能最强，但对 37 条数据是巨大过度工程 |
| **LanceDB** | 嵌入式（Lance 列存） | **不需要** | 未取到官方版本号（标注未核实） | 磁盘型 IVF_PQ；适合"数据在对象存储、进程内查询" |

**Chroma 1.0.0 公告逐字**：*"local Chroma is **4× faster** for common write and query workflows, thanks to a new core written in Rust"*、*"Write speed - 3-5x faster writes"*、*"Query speed - 3-5x faster queries"*、*"True multithreading - No more waiting for the GIL"*；安装方式 `pip install chromadb --pre`；公告提到 *"30+ million downloads"*。**中文技术媒体（腾讯云社区/CSDN）把发布日期记为 2025-04-05**，官方页未标日期，**标注为间接来源**。

**sqlite-vec 的删除代价（提交记录逐字，罕见的诚实数字）**：
> *"Tradeoff: O(N) scan per delete adds ~1ms/row at 10k vectors, ~10ms at 100k. Recall and query latency are unaffected."*

**这条对阙疑特别重要**：append-only 账本**不做删除**，因此恰好避开了 sqlite-vec 唯一的已知 O(N) 退化点。

### 四、embedding 去重的真实先例：SemDeDup 的数字

**SemDeDup**（Amro Abbas, Kushal Tirumala, Dániel Simig, Surya Ganguli, Ari S. Morcos；arXiv:2303.09540，v1 2023-03-16，v3 2023-03-22；后发表于 ICLR 2023 workshop）。摘要逐字：

> *"Here, we introduce SemDeDup, a method which leverages embeddings from pre-trained models to identify and remove semantic duplicates: data pairs which are semantically similar, but not exactly identical. Removing semantic duplicates preserves performance and speeds up learning. Analyzing a subset of LAION, we show that **SemDeDup can remove 50% of the data with minimal performance loss, effectively halving training time**. Moreover, performance increases out of distribution."*

**可迁移到阙疑的三点**：
1. 它区分了 **exact duplicate**（精确重复）与 **semantic duplicate**（语义重复）——**阙疑的 37 实卡里，"同一断言的两种措辞"就是 semantic duplicate，这正是 embedding 能抓到而字符串哈希抓不到的东西**。
2. 它用**保留集性能曲线**而非单一阈值来证明去重没害处——阙疑对应地应画"去重阈值 vs 盲 holdout 检出率"曲线。
3. 它报告的是**下游性能**，不是 recall@k。**阙疑也应报告下游（判决一致性/检出率），而不是向量检索的 recall@k。**

**embedding 模型选择**：`all-MiniLM-L6-v2` 输出 **384 维**、Apache-2.0、在 1B sentence pairs 上微调（HuggingFace / ModelScope 模型卡）。对 37 条 C++ 断言，384 维足够；若要在本机离线跑，模型本体约几十 MB（**具体体积未核实**）。

### 五、对「知识卡去重 + 相似断言检索」的最小可行方案

**规模现实**：37 实卡 + 10 草稿 = 47 条文本；452 条判决账本。**numpy 暴力 cosine 相似度矩阵 47×47 = 2209 次点积，在 384 维下约 3.4×10⁶ 次乘加，现代 CPU 上是亚毫秒级。**

**MVP 设计（不引入任何向量库）**：

```
# 阶段 1：离线生成 embedding（一次性，可复算）
tools/embed_cards.py
  输入: cards/*.md（37 实卡 + 10 草稿）
  模型: all-MiniLM-L6-v2 (384-dim, Apache-2.0)
  输出: ledger/embeddings/cards.npz  (float32, 47×384)
        并写入 sha256(模型权重) + sha256(输入文本拼接) 到 manifest.json

# 阶段 2：精确检索（无索引）
tools/similar_assertions.py
  - 读 cards.npz，L2 归一化后算 full cosine 矩阵
  - 输出: 相似对清单 (card_a, card_b, cosine, 判定=DUPLICATE/RELATED/DISTINCT)
  - 对每个相似对，输出"人工可读证据"：两卡断言的逐字 diff

# 阶段 3：阈值标定（这才是可发表的部分）
tools/calibrate_dedup_threshold.py
  - 在 [0.80, 1.00] 上以 0.01 步长扫阈值
  - 对每个阈值输出: 判为重复的对数 / 人工标注真重复的对数 → precision / recall
  - 用 Clopper-Pearson 给 recall 的 95% 精确二项置信区间（与方向 32 一致）
```

**评测指标（必须报告的四项）**：
1. **Duplicate Precision / Recall**，并给 **Clopper-Pearson 精确区间**（小样本必用，不能用 Wald 区间）。
2. **阈值敏感性曲线**（0.80–1.00 步长 0.01），报告"平台区"宽度——若平台区很窄，说明结论不稳健。
3. **可复算性检查**：`manifest.json` 里记录的 embedding sha256 是否与重跑一致（**浮点非确定性是真实风险**：不同 BLAS 后端、不同线程数会给出末位差异；建议存 `round(x, 6)` 并在论文中声明容差）。
4. **人工抽检**：所有被判 DUPLICATE 的对，100% 人工过一遍并记录在 `research/dedup_audit.md`——**n 很小，全查得起，这是小样本相对大数据的唯一优势**。

**为什么这是"最小可行"而不是"将就"**：NeurIPS E&D 的定位是 *"evaluation itself becomes an object of scientific study"*，**一个在 n=47 上把阈值标定做到可复算、可审计、带精确置信区间的方案，比一个在 n=10⁶ 上跑 Qdrant 但说不清阈值怎么来的方案，更符合赛道定位。**

---

## 对阙疑的 3 条具体行动

1. **【2026-11 前】建 `tools/embed_cards.py` + `tools/similar_assertions.py`，走精确检索路线，明确放弃 ANN 索引。** 在 `research/decisions/ADR-00x_vector_retrieval.md` 里写下拒绝理由，并**逐字引用**本条调研中的三句话作为依据：(a) pgvector 文档 *"Without an index, pgvector falls back to a sequential scan... That is fine for tens of thousands of vectors"*；(b) Qdrant 官方 *"two results must be compared only when you have similar precision"*；(c) Qdrant 官方 *"Accuracy collapse... the HNSW graph becomes disconnected, and the search becomes unreliable"*。**ADR 里要写清"未来触发重评的条件"**（例如"实卡数 > 5,000 时重新评估 ANN"），这样审稿人看到的是有意识的工程判断，不是能力不足。

2. **【2027-03 前】把"阈值标定 + 精确二项区间"做成一个独立小节 `research/12_threats_to_validity.md` 的 `T3_semantic_dedup`，并产出 `figs/dedup_threshold_curve.pdf`。** 具体做法：对 37 实卡两两配对（C(37,2) = 666 对）全部人工标注为 {DUPLICATE, RELATED, DISTINCT} 三档，写入 `data/dedup_gold_666.csv`，字段 `card_a,card_b,label,annotator,date,note`。**666 对全标注是可行的**（这是 n=37 的红利）。然后按 `calibrate_dedup_threshold.py` 扫阈值出曲线。**注意：666 对里真正的 DUPLICATE 可能只有个位数——此时 Clopper-Pearson 区间会非常宽，这本身就是一个诚实且有价值的 negative result**，直接呼应 E&D 赛道欢迎的 "negative results"。

3. **【2027-05 前】在简历与论文中把"向量检索"降级为工具、把"可审计的语义去重协议"升级为贡献。** 简历措辞建议：*"Design and implement an auditable semantic deduplication protocol for a 47-item C++ knowledge-assertion corpus: exact cosine retrieval over 384-dim MiniLM embeddings, threshold calibration over 666 human-labeled pairs, Clopper-Pearson exact 95% CI reporting, and a sha256-manifested embedding artifact enabling third-party recomputation."* **不要写"使用向量数据库做 RAG"**——那是 2023 年的通用叙事，与本项目"判决可复算"的卖点无关，且会触发审稿人"这就是普通 RAG 工程"的判断。

---

## 盲区（诚实标注）

- **Qdrant benchmark 表的 Precision 列存在明显的页面排版错误**：qdrant 行显示 `160.99`，而其他行是 0.97–0.99。我推测这是 `1`（并发数）+ `0.99`（precision）被拼成了 `160.99`（因为"1001"这类粘连在该页也出现过）。**该数值本身未核实**，正文表格中我按 0.99 处理并已注明。
- **Qdrant 的 benchmark 由其自己发布**，且页面自述 *"Qdrant achieves highest RPS and lowest latencies in almost all the scenarios"*——**这是厂商自评，存在利益冲突**。我引用的目的是取它的**方法论警告**（必须同精度比较、过滤下精度崩塌），不是取它的排名结论。
- **Milvus 的"20–50 倍 PQ 压缩"数字未核实**：官方页给的算例是 **8×**（D=128, m=64, nbits=8）。中文博客的 20–50× 可能对应 nbits=8 且 D 更大、m 更小的组合，但我**没有找到官方出处**。
- **LanceDB 的官方版本号与官方 benchmark 数字未取到**，只找到第三方（CSDN/DeepWiki）二手描述，正文已标注。
- **`all-MiniLM-L6-v2` 的模型文件体积、以及它在 C++ 专业文本上的语义质量，均未核实**。C++ 断言是高度形式化的短文本（如"`std::vector` 的 `push_back` 在扩容时使所有迭代器失效"），**通用句向量模型在这类文本上的相似度是否可靠，是本方案最大的未验证假设**。建议在 T3 小节里明确列为威胁：若人工标注发现模型给出的相似度与人类判断相关性低（例如 Spearman ρ < 0.5），整个方案应被否决。
- **Chroma 1.0.0 的发布日期来自中文技术媒体（2025-04-05），官方公告页无日期**，属间接来源。
- **"pgvector 0.8.0 引入 iterative_scan"这一版本归属来自第三方 skill 文档**（`adrianhajdin/podcast-sujata` 仓库），**我未打开 pgvector 官方 CHANGELOG 核实**。若论文要引用，必须先查 `pgvector` GitHub 的 `CHANGELOG.md`。
- **样本偏差**：Qdrant/Milvus/pgvector 的所有公开 benchmark 都在 10⁵–10⁷ 量级、96–1536 维、1–100 线程。**没有任何一个公开 benchmark 覆盖 n < 10³ 的场景**，因此"在 37 条数据上暴力检索足够快"这句话，我是从复杂度分析推出的，**不是从实测数字推出的**——这条必须在论文里如实写成"基于复杂度分析"而非"实测"。

---

## 来源

1. Malkov, Yu A.; Yashunin, D. A. — *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs* — https://pubmed.gov/30602420/ ；DOI 10.1109/TPAMI.2018.2889473；IEEE TPAMI 42(4):824–836, 2020-04-01（Epub 2018-12-28）；arXiv:1603.09320 — 逐字：*"allows a logarithmic complexity scaling"*、*"selected randomly with an exponentially decaying probability distribution"*
2. ParadeDB — *Tuning pgvector Performance* — https://www.paradedb.com/learn/postgresql/tuning-pgvector — 逐字：`m` 默认 16（2–100）、`ef_construction` 默认 64（4–100，必须 ≥2×m）、`hnsw.ef_search` 默认 40；*"Without an index, pgvector falls back to a sequential scan... That is fine for tens of thousands of vectors and untenable beyond that."*；IVFFlat `lists` 起点 rows/1000、`probes` 默认 1
3. QueryPlane — *Tuning HNSW Indexes in pgvector* — https://queryplane.com/docs/blog/pgvector-hnsw-tuning-guide — 逐字：*"set ef_search between 100 and 200, which typically yields 95%+ recall at sub-5ms query times on real embeddings"*
4. Qdrant 官方 — *Vector Search Benchmarks* — https://qdrant.tech/benchmarks/ — 数据集表、5 引擎对比表（qdrant 1238 RPS / 3.54ms / P99 8.62ms；milvus 219.11 RPS / 393.31ms；建索引 1.16min 最快）、环境（Server 8vcpu/32GiB，25GB 内存限制）、*"two results must be compared only when you have similar precision"*、*"Accuracy collapse... the HNSW graph becomes disconnected"*；单节点更新于 2024-01/06
5. Milvus 官方文档 — *IVF_PQ* — https://milvus.io/docs/zh/ivf-pq.md — `nlist` 默认 128、`nbits` 默认 8、`nprobe` 默认 8；D=128/m=64/nbits=8 时 4096 bits → 512 bits（**8×** 压缩）；*"A commonly recommended value is m = D/2"*
6. asg017 — *sqlite-vec* GitHub — https://github.com/asg017/sqlite-vec — 版本 **v0.1.10-alpha.4**，commit `04d28bd`，2026-05-18；逐字：*"An extremely small, 'fast enough' vector search SQLite extension that runs anywhere! A successor to sqlite-vss"*、*"⚠️ sqlite-vec is a pre-v1, so expect breaking changes!"*、*"Tradeoff: O(N) scan per delete adds ~1ms/row at 10k vectors, ~10ms at 100k. Recall and query latency are unaffected."*；ANN 支持见 PR #273/#279
7. Chroma 官方 — *Chroma, now 4x faster*（v1.0 公告） — https://www.trychroma.com/project/1.0.0 — 逐字：*"local Chroma is 4× faster... thanks to a new core written in Rust"*、*"Write speed - 3-5x faster writes"*、*"Query speed - 3-5x faster queries"*、*"30+ million downloads later"*；基准环境 *"Dataset of 1M OpenAI 1536 dimensional embeddings... on a 12 core M2 Macbook"*
8. Abbas, A.; Tirumala, K.; Simig, D.; Ganguli, S.; Morcos, A. S. — *SemDeDup: Data-efficient learning at web-scale through semantic deduplication* — https://arxiv.org/abs/2303.09540 — arXiv:2303.09540v3, 2023-03-22（v1 2023-03-16）— 逐字：*"SemDeDup can remove 50% of the data with minimal performance loss, effectively halving training time"*
9. arXiv:2412.01940v3 — *Down with the Hierarchy: The 'H' in HNSW Stands for "Hubs"* — https://arxiv.org/html/2412.01940v3（2025-07-03） — 逐字：*"a flat navigable small world graph retains all of the benefits of HNSW on high-dimensional datasets"*
10. ANN-Benchmarks（Martin Aumueller / Erik Bernhardsson） — https://ann-benchmarks.com/index.html — 逐字：*"Recall (the fraction of true nearest neighbors found, on average over all queries) against Queries per second"*；glove-100-angular k=100 结果页 https://ann-benchmarks.com/glove-100-angular_100_angular.html（页面为可视化图，**未取到逐点数值**）
11. HuggingFace / ModelScope 模型卡 — `sentence-transformers/all-MiniLM-L6-v2` — https://www.modelscope.cn/models/sentence-transformers/all-MiniLM-L6-v2 — 逐字：*"maps sentences & paragraphs to a 384 dimensional dense vector space"*；Apache-2.0；1B sentence pairs 微调
12. CSDN 技术博客（二手，仅作交叉参考，**不作为论文引用**） — *IVF_PQ 的详细解析*（2025-08-08）、*大规模语义检索的近似算法*（2026-09-15，"压缩 20-50 倍"，**未核实**）；*LanceDB 分区策略*（2025-09-19）
