# 方向 67：存储选型决策框架与成本优化（Storage Selection Decision Framework & Cost）

> 承接方向 61（SQLite 应用层）、62（SQLite 本体）、66（时序存储）、75（JSON/Parquet/Arrow）。这四个方向回答"某个存储怎么用"；本方向回答**"什么时候该用哪个"**——给阙疑一张可落地的决策树 + 一张平台配额成本表 + 一套冷温热分层方案，全部以 NeurIPS E&D 数据托管硬约束为终点。

---

## 核心结论

1. **NeurIPS E&D 四大首选托管平台配额已逐字核实，容量对阙疑完全不构成瓶颈**：Harvard Dataverse **1TB/数据集（单文件 2.5GB）**、Kaggle **200GB/数据集**、Hugging Face **300GB/数据集（public）**、OpenML **200GB/数据集**（来源：NeurIPS 2025 Data Hosting Guidelines 官方页面逐字核实）。阙疑 2026-09 的全部数据（37 实卡 + 67 规则 + 452 条判决账本 + 3826 行内核）打包后预计 **< 100MB**，只占最小配额（Kaggle/OpenML 200GB）的 **0.05%**。所以存储选型的真正决策轴不是容量，而是**判决可复算性（append-only + 哈希链）与审稿人可访问性（Croissant 元数据）**。
2. **引擎决策主轴只有两条**：需要 ACID + 追加写 + 篡改证据 → **SQLite（WAL 模式）**；需要列式扫描分析 → **Parquet + DuckDB**。量化依据：MotherDuck 2026-09 基准（DuckDB v1.5.5，1119 万行 NYC 出租车数据）显示 Parquet/ZSTD 比 CSV **小 6.8 倍**（164MB vs 1.09GB）、查询快 **22–60 倍**（公平下界 22 倍，`count(*)` 因走 row-group 元数据可达 ~160 倍）；而 SQLite 官方 limits.html 逐字确认默认页大小 4096 字节时上限约 **17.5TB**、最大页 65536 字节时约 **281TB**——对单人科研项目，SQLite 容量上限事实上不存在。
3. **冷温热分层的最优解是"本地热 + Zenodo 冷"而非上云**：S3 us-east-1 Standard **$0.023/GB/月** vs Glacier Deep Archive **$0.00099/GB/月**（约 **23 倍**差距，第三方来源，官方页未逐字核实），检索费与 180 天最短存储时长使冷层不适合"偶尔翻账本"的科研访问模式；而 **Zenodo 免费 50GB/record（上限 100 文件）且自带 DOI**，是学术冷归档的零成本最优解。HF 免费私有仓库仅 **100GB**、公开仓库是 **"Best-effort"（尽力而为，无固定数字）**，不能当作可靠冷备。

---

## 精确数字与案例

### 一、NeurIPS E&D 托管平台配额：官方逐字核实（决策终点）

NeurIPS 2025 起要求 Datasets & Benchmarks（2026 更名 E&D）投稿必须提供数据集 URL + **Croissant 机器可读元数据文件**，并给出四个首选平台。官方页面（neurips.cc/Conferences/2025/DataHostingGuidelines）的核心表格逐字转录如下：

| 平台 | Croissant 自动生成 | 配额 | 文件类型 | 私有预览 URL | 门控访问 | DOI |
|---|---|---|---|---|---|---|
| Harvard Dataverse | ✅ | **1TB per dataset (2.5GB per file)** | Any | ✅ | ✅ | ✅ |
| Kaggle | ✅ | **200GB per dataset** | Any | ✅ | ❌ | ✅ |
| Hugging Face | ✅ | **300GB per dataset public** | Any | ❌ | ✅ | ✅ |
| OpenML | ✅ | **200GB per dataset** | Any | ❌ | ❌ | ❌ |

关键逐字引文：

> "**Harvard Dataverse, Kaggle, Hugging Face, and OpenML platforms are the preferred hosting platforms for datasets.**"

> "If your dataset is accepted, **you will be required to make it public by the camera ready deadline. Failure to do so may result in removal from the conference and proceedings.**"

> "After submissions are closed, **if your Croissant file is invalid or if your data is not accessible, your submission may be desk-rejected.**"

三条硬约束直接决定存储拓扑的顶层设计：(a) 必须能生成 Croissant（四个平台自动生成；自托管要手动生成）；(b) 录用后必须在 camera-ready 前公开；(c) Croissant 无效或数据不可访问会**直接 desk reject**——这与方向 02/07 讨论的 Pangram AI 检测 desk reject 是两条独立的毙稿路径。

### 二、引擎层判据：SQLite vs Parquet vs CSV 的量化边界

**案例 1：MotherDuck CSV vs Parquet 基准**（Jacob Matson，MotherDuck，2026-09 更新；DuckDB v1.5.5，Apple M3 Max 36GB RAM，11,198,026 行 NYC TLC 2025 Q1 黄色出租车数据，20 列）：

| 格式 | 大小 | 相对 CSV |
|---|---|---|
| CSV | 1,172,769,059 字节（1.09 GB） | — |
| Parquet (Snappy) | 228,421,875 字节（218 MB） | **5.1x 更小** |
| Parquet (ZSTD) | 172,016,004 字节（164 MB） | **6.8x 更小** |

查询速度（中位数，3 次运行）：`count(*)` **~160x**（0.485s → 0.003s，走 row-group 元数据不扫数据）；单列聚合 `avg(trip_distance)` **~60x**；全 20 列 Top-5 **~22x**。作者明确警告公平口径：

> "The fair lower-bound headline is **22x**, not 160x. DuckDB's parallel CSV reader is already fast (~0.5 s over 1.1 GB)."

同时该基准诚实指出了 Parquet 的失效条件：row-group skipping 在该数据上"never fires"（过滤列与行组顺序不相关时，min/max 统计无用于是跳段机制失效）。这提示阙疑：**账本数据若按时间序追加、按规则名过滤，列裁剪有效，但跳段过滤未必**。

**案例 2：SQLite 容量与形态边界**（sqlite.org/limits.html，2026-07 更新版，逐字）：

> "The largest possible setting for SQLITE_MAX_PAGE_COUNT is **4294967294 (2³²-2)**. Since version 3.45.0 (2024-01-15), 4294967294 is also the default value."

> "When used with the default page size of 4096 bytes, this gives a maximum database size of about **17.5 terabytes**." / "If the page size is increased to the maximum of 65536 bytes, then the database file can grow to be as large as about **281 terabytes**."

> "This particular upper bound is untested since the developers do not have access to hardware capable of reaching this limit."

结论：对阙疑这种"452 条账本、预计三年内 < 10 万条判决"的规模，SQLite 的上限问题**不存在**；真正要关注的是形态问题——SQLite 是行式 B-tree，做"67 条规则 × 452 条判决 × 时间窗"这类聚合分析时，每次都要整行解码，这正是方向 75（Parquet/Arrow）要补的位置。

**决策树（可直接写进论文的 implementation details 小节）**：

| 判据 | 是 → | 否 → |
|---|---|---|
| 写入是否需要 ACID 事务 + 崩溃安全？ | SQLite（WAL） | 文件 + 哈希校验 |
| 写模式是否几乎纯追加（append-only 账本）？ | SQLite 触发器强制 append-only | 可用 Parquet 分区文件 |
| 是否需要第三方不信任内核地复算？ | SQLite 单文件 + 独立对账器（可拷走整个 .db） | — |
| 读模式是否为列扫描聚合（读写比 > 100:1 的分析）？ | Parquet + DuckDB | SQLite |
| 单文件是否 > 2.5GB（Dataverse 上限）？ | 必须分片或换平台 | 无所谓 |
| 是否需人类可读 diff / git 版本管理？ | JSONL/CSV | 二进制格式 |
| 数据是否写入后不再变（冷归档）？ | Zenodo / Parquet 静态文件 | SQLite 热库 |

### 三、冷温热分层与云存储成本

**S3 各存储类**（us-east-1 口径；单价来自第三方 costimizer.ai 2026-05 文章与 hidekazu-konishi.com 对比工具，AWS 官方页未逐字核实，见盲区）：

| 存储类 | 月价（$/GB） | 检索费 | 最短存储时长 | 适用层 |
|---|---|---|---|---|
| S3 Standard | $0.023 | 无 | 无 | 热 |
| S3 Intelligent-Tiering | ~$0.023 + 监控费 | 无 | 无 | 温热自动 |
| S3 Standard-IA | $0.0125 | $0.01/GB | 30 天 | 温 |
| Glacier Instant Retrieval | $0.004 | $0.03/GB | 90 天 | 冷（需即时读） |
| Glacier Flexible | $0.0036 | 按量+分钟级延迟 | 90 天 | 冷 |
| Glacier Deep Archive | $0.00099 | 高+小时级延迟 | 180 天 | 深冷 |

hidekazu 工具的一个典型场景输出（该工具自带数字，非官方）：1TB 级别月成本 Standard $23.90 vs Deep Archive $6.39。但对科研数据还有两条隐藏成本：(a) **取出费**——Deep Archive 检索 $0.02/GB 起且要等数小时，审稿人不可能等；(b) **最小存储时长罚则**——数据存 1 个月就删，Deep Archive 仍按 180 天计费。所以"审稿人可能随时访问"的数据**永远不该进 Glacier 层**。

**Zenodo（学术冷层最优解）**：官方帮助页逐字——"We currently accept up to **50GB per record with a maximum of 100 files**"，"Each record comes with a **default storage quota of 50GB** and you can upload an **unlimited number of records**"；且"if you would like to upload up to **200GB** of data"可申请（help.zenodo.org/docs/deposit/manage-files/）。Zenodo 免费提供 **DOI**，与方向 19（匿名化仓库）可配合。

**Hugging Face 精确配额**（huggingface.co/docs/hub/storage-limits 逐字核实）：

| 项目 | 免费用户 | PRO |
|---|---|---|
| 公开仓库 | **"Best-effort*"**（"Beyond the first few gigabytes, please use this resource responsibly"） | Up to 10TB included |
| 私有仓库 | **100GB** | 1TB + pay-as-you-go |
| 单文件硬上限 | **500GB**（"no single file will exceed 500GB"），推荐每块 < 200GB | 同左 |
| 私有超量计费 | — | **$18/TB/月**（50TB+ 降至 $16） |

附加硬限制：单仓库文件数建议 < **100k**；单文件夹 **10k 文件硬上限**；单次提交建议 50–100 文件。这些数字直接影响阙疑的导出策略：**452 条账本绝不能导出成 452 个小 JSON 文件上传 HF**（撞 100k/10k 限制且 Git 提交数爆炸），必须打包或合并。

### 四、判据合成：阙疑视角的"何时选哪种"完整框架

把方向 61/62/66/75 的局部结论收束成一张总表（每行都对应上文核实过的数字或平台条款）：

| 数据类型 | 数据量（现估） | 写模式 | 读模式 | 选型 | 归档去向 |
|---|---|---|---|---|---|
| 判决账本（452 条，哈希链） | < 10MB | 纯追加 + ACID | 点查 + 链验证 | **SQLite WAL**（61/62） | Zenodo record（含 DOI） |
| 知识卡/规则（37+67 条） | < 5MB | 偶尔修改 | 全量加载 | JSON/SQLite 均可，建议 SQLite 单源 | 随账本一起 |
| 实验指标时序 | < 50MB | 批量追加 | 时间窗聚合 | 方向 66：SQLite 表 + 时间索引；> 千万行再考虑列式 | Parquet 快照 |
| 复现实验/分析查询 | 派生 | 只读重算 | 列扫描 | **Parquet(ZSTD) + DuckDB**（75） | 不归档（可再生） |
| 对外发布数据集 | 打包 < 100MB | 冻结 | 审稿人下载 | **Dataverse 主托管**（唯一同时有私有预览+门控+DOI+1TB 的平台） | 双托管：Kaggle/HF 镜像 |
| 论文附属日志/工具 | — | 冻结 | 偶发 | Zenodo（50GB/record，DOI） | 同左 |

分层命名建议（冷温热的科研版语义，参考 JavaGuide 冷热分离思想但按"审稿可访问性"重定义）：**热** = 本机 SQLite/Parquet（每日读写）；**温** = GitHub 仓库内小文件（< 100MB/仓库配额内）+ HF 公开仓库；**冷** = Zenodo（DOI 化、不可变）+ Dataverse（E&D 指定平台）。**不要把"冷"定义成 S3 Glacier**——科研冷数据的语义是"不可变且可被第三方引用"，而不是"我自己很少读"。

---

## 对阙疑的 3 条具体行动

1. **写一份 `research/storage_topology.md`（2026-11 前），把上面第四节的总表落成唯一权威文档**：明确 `queyi.db`（SQLite WAL，判决账本 + 知识卡 + 规则）为唯一热源；每次 Merkle checkpoint 后由脚本导出 `ledger_snapshot_<n>.parquet`（ZSTD 压缩，与 MotherDuck 基准同参数 `COMPRESSION ZSTD`）到 `snapshots/`；在文件中记录每张表的行数与文件字节数，纳入方向 16 的 README 口径治理，避免再次出现 227 项漂移式的文档滞后。
2. **2027-05 前完成"双托管 + Croissant"演练**（对齐方向 18）：主托管选 Harvard Dataverse（1TB/2.5GB 配额最宽裕，且是四平台中唯一同时具备私有预览 URL + 门控访问 + DOI 的，适合盲态协议的 controlled access 需求）；镜像托管选 Kaggle（200GB，上传门槛最低）。用 `huggingface.co/spaces/MLCommons/croissant-editor` 或 `mlcroissant` Python 库生成 Croissant 文件，并用 NeurIPS 官方指定 checker（`huggingface.co/spaces/JoaquinVanschoren/croissant-checker`）验证通过——注意官方警告"Croissant 无效或数据不可访问 → desk reject"。导出时把账本合并成单文件（< 2.5GB），不要按条拆分。
3. **给 append-only 加存储层强制而非应用层纪律**（补强方向 61）：参考 GitHub 开源项目 `MuhammadAbdullah80/sqlite-audit-log`（"An append-only audit log for SQLite, **enforced by triggers and constraints rather than by application discipline**"）与 `tabenius/nostoi`（tamper-evident audit chains，"SQLite has no SHA-256" 故需注册自定义 digest 函数），在 `gate_engine.py` 之外为 452 条账本的 SQLite 表加 `CREATE TRIGGER ... BEFORE UPDATE/DELETE RAISE(ABORT)` 触发器，使账本不可回改成为数据库物理性质而非 `gate_engine.py` 3826 行代码里的一个约定——这直接服务于核心卖点"判决可复算 + 盲态协议不可回盲"。

---

## 盲区（诚实标注）

- **OpenML 200GB 配额未从 OpenML 官方文档逐字核实**：本数字仅来自 NeurIPS 官方 Data Hosting Guidelines 页面的转述；fetch OpenML 官方 data 文档页（docs.openml.org/data/）未取得配额数字正文（页面正文为空壳导航）。GitHub 上 openml 组织 2026 年的 S3 上传接口重构文档暗示其存储架构在变动，配额可能调整。
- **S3 各档单价（$0.023 / $0.0125 / $0.00099 等）未在 AWS 官方定价页逐字核实**：来自 costimizer.ai（2026-05）与 infratally.com（2026-04）两个第三方文章及 hidekazu-konishi.com 对比工具（其自述"pricing data is bundled and may be outdated"）。AWS 官方页为动态渲染，未成功抓取。数字量级可信（多来源一致），用于论文前应在官方页人工复核。
- **DuckDB vs SQLite 的直接性能倍数未取得可靠基准**：搜索到的中文实测文章（duckdblab.org 等）与 CSDN 文章未逐字核实其方法论，不敢引用具体倍数；本文仅引用了 MotherDuck 的 CSV vs Parquet 基准（方法论完整可复现）。SQLite 做 OLAP 聚合比 DuckDB 慢多少，阙疑应自己用真实账本测，而非引用二手数字。
- **Kaggle 200GB 公告时效性存疑**：该公告（"Doubling of Private Quota and Public File Size Limit"）发布于约 2024 年（页面标注"2 years ago"），本轮仅核到 NeurIPS 2025 指南仍写 200GB，但 Kaggle 现行 technical specifications 页未单独核实；私有配额翻倍前的旧数字是 20GB/100GB（Kaggle 讨论区旧帖），说明该平台配额历史上多次变动，投稿前需再查一次。
- **NeurIPS 2027 E&D 的托管指南可能变化**：本文全部平台条款核实自 NeurIPS **2025** Data Hosting Guidelines；2026/2027 届是否沿用四平台清单与 Croissant 强制要求，属于未来信息，未核实，2026-12 NeurIPS 2026 结束后应重查 CFP。

---

## 来源

1. NeurIPS 2025 Data Hosting Guidelines — https://neurips.cc/Conferences/2025/DataHostingGuidelines — "1TB per dataset (2.5GB per file)"（Dataverse）、"200GB per dataset"（Kaggle/OpenML）、"300GB per dataset public"（HF）、Croissant 无效即 desk reject — NeurIPS 官方 — 2025
2. Hugging Face Storage Limits — https://huggingface.co/docs/hub/storage-limits — 免费私有 100GB、公开 "Best-effort"、单文件 500GB 硬上限、$18/TB/月、10k 文件/文件夹硬限制 — Hugging Face 官方文档 — 2026 访问
3. Kaggle 官方公告：Doubling of Private Quota and Public File Size Limit — https://www.kaggle.com/discussions/product-announcements/512322 — "Users now have a limit of 200GB for private models and 200GB for private datasets... doubled the maximum upload size of public models and datasets from 100GB to 200GB" — Prathamesh Bang / Kaggle — 约 2024
4. Implementation Limits For SQLite — https://sqlite.org/limits.html — SQLITE_MAX_PAGE_COUNT 4294967294（3.45.0 起默认）；默认页 4096 → 约 17.5TB；最大页 65536 → 约 281TB；"This particular upper bound is untested" — SQLite 官方 — 2026-07 版
5. CSV vs Parquet Benchmark: 6.8x Smaller, 22-60x Faster — https://motherduck.com/learn/csv-vs-parquet-benchmark/ — 11,198,026 行；Parquet/ZSTD 164MB vs CSV 1.09GB（6.8x）；查询 22–60x（count(*) ~160x）；DuckDB v1.5.5 — Jacob Matson / MotherDuck — 2026-09 更新
6. Zenodo 官方帮助：Manage storage quota / Manage files — https://help.zenodo.org/docs/deposit/manage-quota/ 与 https://help.zenodo.org/docs/deposit/manage-files/ — "up to 50GB per record with a maximum of 100 files"；"unlimited number of records"；可申请至 200GB — Zenodo / CERN — 2026-09 访问
7. AWS S3 Pricing（第三方解读）— https://costimizer.ai/blogs/aws-s3-storage — "S3 Standard costs $0.023/GB-month in us-east-1. Glacier Deep Archive costs $0.00099/GB, a 23x difference" — costimizer.ai — 2026-05（未在 AWS 官方页核实）
8. S3 Storage Class Cost Comparison Tool — https://hidekazu-konishi.com/tools/s3_storage_class_cost_comparison_tool.html — 七档存储类对比、30/90/180 天最短时长、128KB/40KB 最小计费对象、典型场景 Standard $23.90/月 vs Deep Archive $6.39/月 — hidekazu-konishi — 2026-04 首发 / 2026-07 更新
9. 数据冷热分离详解 — https://javaguide.cn/high-performance/data-cold-hot-separation.html — 冷热分离按访问频率与业务重要性划分存储的思想框架 — JavaGuide — 2026-06 访问
10. sqlite-audit-log（触发器强制 append-only）— https://github.com/MuhammadAbdullah80/sqlite-audit-log — "enforced by triggers and constraints rather than by application discipline"；nostoi（篡改可见审计链）https://github.com/tabenius/nostoi — "SQLite has no SHA-256, so any SQLite client can read and verify the file" — GitHub 开源项目 — 2026 访问
