# 方向 75：存储格式选型（JSON / JSONL / Parquet / Arrow / Avro / Protobuf / MessagePack）——以"可 diff / 可人工审阅"为第一判据

> 调研时间：2026-09-29｜调研员：方向 68–79 组｜真实搜索 12 次（含 3 次 WebFetch 逐字取数）
> 关键前提：**阙疑的判决账本要给审稿人看。** 因此本文的选型判据不是"最小 / 最快"，而是**"审稿人能否用 `git diff` 逐行审阅，并独立复算出同一个哈希"**。

---

## 核心结论

1. **在阙疑的数据规模上，二进制格式的全部优势都是零，而它们的代价是"审稿人无法审阅"。** 实测数字（dataarchitect.studio, 2026-07-26，3,000,000 行 × 11 列，未压缩 322 MB）：Parquet+zstd 只有 **56.6 MB**，是 CSV（342.6 MB）的 **6.1 倍**压缩；DuckDB 上一条过滤聚合查询 **13.8 倍**快（0.064s vs 0.879s）。**但阙疑的账本是 452 条判决，估计体积在几百 KB 到几 MB 之间**——把 1 MB 压到 200 KB，省下的 800 KB **没有任何意义**；而代价是 `git diff` 只会输出 *"Binary files differ"*，**审稿人无法审阅任何一条判决**。这是一笔极差的交易。
2. **JSONL（JSON Lines）是唯一同时满足"可 diff"与"可追加"的格式，而"可追加"恰好是 append-only 账本的定义。** 每条判决占一行，新增一条判决在 `git diff` 里就是**精确的一行 `+`**；如果用 JSON 数组（`[{...}, {...}]`），新增一条会同时改动"最后一条的逗号"和"闭合括号"，**diff 里出现 3 处改动而其中 2 处是噪声**。**这不是审美问题**：审稿人判断"这次提交是否只追加了一条判决、没有篡改历史"的成本，从"扫一眼"变成"逐字符核对"。
3. **必须把"哈希用的字节"和"给人看的字节"分开，用 RFC 8785（JCS）把前者标准化。** 一个致命的陷阱：`{"a":1,"b":2}` 与 `{"b":2,"a":1}` **语义相同但 SHA-256 完全不同**（JCS 指南逐字：*"semantically identical but hash to different values without canonicalization"*）。如果阙疑直接对"格式化后的 JSON 文本"取哈希，那么**任何人只要用不同的 JSON 库重新序列化一次，账本哈希就会变**——这会直接摧毁"判决可复算"的根基。**解法**：哈希必须对 **JCS 规范化后的字节**计算；人看的版本可以任意美化。**RFC 8785 于 2020 年 8 月发布，是第一个标准化的规范化 JSON 格式。**

---

## 精确数字与案例

### 一、六种格式的实测横评（两个独立 benchmark）

**Benchmark A**：`github.com/vineetkukreti/data-format-comparison`（首次提交 2025-03-17，脚本 `comparision_analysis.py` 公开）。数据集规模仓库未在 README 中明确说明（**这是该 benchmark 的局限**）。

| 格式 | 文件大小 (MB) | 写入 (s) | 读取 (s) | 过滤 (s) | 分组 (s) | 内存 (MB) |
|---|---|---|---|---|---|---|
| CSV | 319.94 | 10.82 | 5.38 | 0.062 | 0.177 | 577.20 |
| **JSON** | **447.49** | 5.91 | 7.58 | 0.120 | 0.206 | **1995.02** |
| Apache Parquet (PyArrow) | **121.15** | 2.34 | 2.17 | 0.072 | 0.226 | 736.29 |
| Parquet (fastparquet) | 123.40 | 2.85 | **1.20** | 0.087 | 0.204 | 503.92 |
| Apache ORC | 249.50 | **2.02** | 2.50 | 0.071 | 0.194 | 635.38 |
| Apache Arrow / Feather | 138.49 | 2.33 | 2.11 | **0.045** | **0.142** | **440.45** |

关键比率（仓库逐字）：
- Parquet (PyArrow) **121.15 MB ≈ JSON 的 27%、CSV 的 38%**
- **JSON 内存占用 1995.02 MB ≈ 1.95 GB**，是最高效格式（Arrow 440.45 MB）的 **4 倍以上**
- JSON 读取 7.58s，比最快的 fastparquet（1.20s）**慢 6 倍以上**
- CSV 写入 10.82s，比最快的 ORC（2.02s）**慢 5 倍以上**

**Benchmark B**：dataarchitect.studio *Parquet vs ORC vs Avro Benchmark*（2026-07-26 发布，2026-08-08 更新）。**这个 benchmark 的方法学质量显著高于 A**：数据集 **3,000,000 行 × 11 列 / 未压缩 322 MB**，**固定随机种子**，脚本（`benchmarks/file-format-benchmark.py`）与原始结果（`benchmarks/results-2026-07-26.json`）**均公开**，作者明确声明"绝对值无意义，比率才是结论"。

| 格式 | 磁盘大小 | vs CSV | 写入 (s) | 全表扫描 (s) | 2/11 列扫描 (s) |
|---|---|---|---|---|---|
| CSV | 342.6 MB | 1.0× | 1.80 | 1.398 | 0.499 |
| CSV + gzip | 92.1 MB | 3.7× | 13.40 | — | — |
| ORC (snappy) | 96.2 MB | 3.6× | 1.84 | 0.676 | 0.109 |
| Parquet (snappy) | 72.3 MB | 4.7× | 1.35 | 0.420 | 0.055 |
| ORC (zlib) | 68.1 MB | 5.0× | 4.67 | 1.289 | 0.262 |
| **Parquet (zstd)** | **56.6 MB** | **6.1×** | **1.32** | **0.377** | **0.054** |

**列裁剪（column pruning）——本文最重要的实测发现（逐字）**：

| 格式 | 只读 2/11 列的加速比 |
|---|---|
| Parquet | **6.9×** 更快（0.377s → 0.054s） |
| ORC | **4.9×** 更快（1.289s → 0.262s） |
| CSV | **2.8×** 更快（1.398s → 0.499s）——**但这是假象**：*"CSV still reads and parses every byte of every row; all it saves is converting the columns you didn't ask for."* |
| **Avro** | **0.96×——即慢 4%**。作者逐字：*"asking for two fields out of eleven was marginally slower than taking all eleven, since the whole record is decoded either way and then you throw most of it away. That is not a defect. It is what row-based means."* |

**DuckDB 查询（同一查询、同一数据、直接读文件）**：CSV **0.879s** vs Parquet (zstd) **0.064s** = **13.8 倍**。

**匹配编解码器的公平比较（1,000,000 行，逐字）**：

| 编解码器 | Parquet | ORC | 差异 |
|---|---|---|---|
| Snappy | **24.3 MB** | 32.9 MB | Parquet 小 **26%** |
| DEFLATE (gzip/zlib) | **17.8 MB** | 23.1 MB | Parquet 小 **23%** |

作者诚实说明：*"It does not show that ORC compresses worse than Parquet in general... ORC's reputation was built in tuned Hive stacks on different data."* 并**自我纠正**了自己之前的文章。

**Avro 在行式布局上的代价（300,000 行子集，逐字）**：

| 格式 | 大小 |
|---|---|
| Avro 未压缩 | 24.2 MB |
| Avro + snappy | 13.7 MB |
| Avro + deflate | 10.6 MB |
| ORC + zlib | 6.8 MB |
| **Parquet + zstd** | **6.5 MB** |

**Avro 即使最优压缩也比 Parquet 大 63%**。作者逐字解释原因：*"Row-based layouts interleave values of different types and cardinalities, which is exactly the arrangement that defeats the run-length, dictionary, and delta encodings columnar formats depend on. You accept that cost to get cheap appends and schema evolution."*

**zstd vs gzip（1,000,000 行，逐字）**：zstd **19.3 MB / 0.54s**；gzip **17.8 MB / 16.00s**。**gzip 只换来 8% 的体积收益，写入慢 30 倍。**

### 二、MessagePack / Protobuf：体积收益的实测数字与"压缩后收益塌陷"

来源：jsonic.io *JSON vs MessagePack*（2026-05-12）。**注意：该来源是 JSON 工具站的推广文章，数字为自测近似值，无公开 benchmark 仓库，属较低可信度来源**（详见盲区）。

| 载荷类型 | JSON 大小 | MessagePack 大小 | 节省 |
|---|---|---|---|
| 小对象（5 字段，短键） | ~120 B | ~75 B | **38%** |
| 100 个整数的数组 | ~350 B | ~210 B | **40%** |
| 嵌套 API 响应（10 KB） | 10,240 B | ~6,500 B | **36%** |
| **长文本字段（文章正文）** | ~5,000 B | ~4,900 B | **2%** |
| 二进制载荷（1 KB 缩略图） | ~1,368 B（Base64） | ~1,026 B | **25%** |
| **gzip 压缩后（10 KB JSON）** | ~2,100 B | ~1,800 B | **14%** |

**决定性的一条（逐字）**：*"the wire-size benefit of switching to MessagePack drops from **~35% to ~10–15%**"*（启用 gzip/Brotli 后）。

**字节级算例（逐字）**：`{"name":"Alice","age":30}` → JSON **23 字节**，MessagePack **14 字节**（`82 a4 6e616d65 a5 416c696365 a3 616765 1e`），**节省 9 字节 / 39%**。

**吞吐实测（Node.js 20 / Apple M2 单线程，10 KB 代表性 API 响应）**：

| 库 | 编码吞吐 | 解码吞吐 | 输出大小（输入 10 KB JSON） |
|---|---|---|---|
| `JSON.stringify` / `JSON.parse` | ~200 MB/s | ~250 MB/s | 10,240 B |
| `msgpackr` | ~400 MB/s | ~500 MB/s | ~6,500 B |
| `@msgpack/msgpack` | ~180 MB/s | ~220 MB/s | ~6,500 B |
| `msgpackr`（useRecords: true） | ~600 MB/s | ~700 MB/s | ~4,000 B |

**Python（CPython 3.12，逐字）**：`msgpack.packb()` **~150 MB/s** vs `json.dumps()` **~60 MB/s**（**2.5×**）。

**Protobuf**：jsonic.io 另一篇指南（转引）称 Protobuf 通常比 JSON 小 **5–10×**（**我未核实原始基准**）。

### 三、可 diff 性的结构性分析：为什么行式 + 文本是唯一解

**Git 对二进制文件的行为**：Git 内置的文本处理只对**被判定为文本的文件**生效；`.gitattributes` 官方文档逐字说明某些编码（如 UTF-16）*"are interpreted as binary and consequently built-in Git text processing"* 不适用。对真正的二进制文件，`git diff` 的输出是 *"Binary files differ"*（这一行为在多处技术问答中被反复提到，如 CSDN 问答 *"Git GUI 中 'rescan' 总提示 'binary files differ'"*）。

**推论**：**Parquet / Arrow / Avro（二进制编码）/ Protobuf / MessagePack 全部落在这条线上。** 它们的格式设计目标是"给程序读"，**不是"给人读"**。`.gitattributes` 的 `textconv` 机制可以配置"用某个外部程序把二进制转成文本再 diff"，**但这需要审稿人本地装好你的转换器**——这违背了"第三方可不信任内核地复算"的前提（第三方应当**只需要一个 JSON 解析器和你的规范文档**）。

**JSONL vs JSON 的 diff 差异（结构性论证）**：

| 场景 | JSON 数组 | JSONL |
|---|---|---|
| 新增第 453 条判决 | diff 出现 **3 处改动**：① 第 452 条的 `}` 后加 `,`；② 插入新对象；③ 闭合 `]` 位置不变但上下文变 | diff 出现 **1 处改动**：在文件末尾追加 **1 行** |
| 审稿人核对"是否只追加、未篡改" | 需要**逐字符**确认前 452 条未被动过 | **看 diff 只有 `+` 没有 `-`，一眼确认** |
| 流式读取 | 必须解析整个数组 | 逐行解析，可并行 |
| 单条损坏的影响 | 整个文件不可解析 | 只有那一行不可解析 |

**"diff 只有 `+` 没有 `-`"这一条本身就是 append-only 的可视化证明。** 这对阙疑有超出工程的意义：**它把一个"不变量"从文档声明变成了审稿人可自行验证的视觉事实。**

### 四、RFC 8785（JCS）：把"哈希用的字节"标准化

来源：jsonic.io *JSON Canonicalization (JCS, RFC 8785)*（2026-05-13）；规范本体为 RFC 8785（**2020 年 8 月发布**，`rfc-editor.org/rfc/rfc8785.pdf`）。

**四条核心规则（逐字）**：

| 规则 | 内容 | 示例 |
|---|---|---|
| **1. 键排序** | 按键的 **UTF-16 码元序列**排序（**不是**字母序、**不是** locale 感知排序） | `{"Z":1,"a":2}`：`"Z"`(U+005A) 在 `"a"`(U+0061) **之前** |
| **2. 数字序列化** | IEEE 754 双精度；采用 **ES2019 `Number::toString`**（Grisu3/Dragon4/Ryu），**最多 17 位有效数字**；整数不带小数点/指数；无尾随零 | `1.5e10` → `15000000000`；`1.50` → `1.5`；`1.0` → `1` |
| **3. 无空白** | token 之间无空格、制表符、换行 | `{"a":1}` 而非 `{ "a": 1 }` |
| **4. 字符串转义** | **只转义控制字符 U+0000–U+001F**，其余不转义 | Tab → `\t`，换行 → `\n` |

**必须报错的输入（逐字）**：`Infinity` 和 `NaN` *"are not valid JSON values. RFC 8785 requires implementations to reject them; a canonical JSON serializer must throw an error rather than silently producing null or a string representation."*

**最关键的规范性说明（逐字）**：
> *"JCS canonicalizes the **actual** floating-point value, not the value you intended. If your data has floating-point precision issues, they will be **locked into the canonical form**."*

示例：`0.1 + 0.2` 的规范化输出是 **`0.30000000000000004`**。

**这个例子对阙疑是一个真实威胁**：如果账本条目里存了任何**浮点数**（例如"检出率 0.667"、"p 值 0.03"），那么 JCS 会把它锁成最短可往返表示。**如果不同平台的浮点计算结果有末位差异，规范化后的字节就不同，哈希就不同。** **应对**：**账本里禁止出现浮点数**——所有数值以**整数**（分子/分母）或**十进制字符串**存储。这条纪律必须写进 schema 定义，并在 CI 里断言（正则检查所有账本数值字段不匹配 `\d+\.\d+`）。

**JCS 与其他方案对比（逐字）**：

| 方案 | 键排序 | 数字处理 | 状态 |
|---|---|---|---|
| **JCS (RFC 8785)** | UTF-16 码元顺序 | IEEE 754 / ES2019 最短 | **IETF 标准（2020）** |
| JSON-LD Canonicalization | Unicode 码点 | 未指定（透传） | W3C，用于可验证凭证 |
| Gibson's Canonical JSON | 字节序（UTF-8） | **仅整数（无浮点）** | 非标准，早于 RFC 8785 |
| `sort_keys` + 去空白 | Python/JS 默认排序 | 语言相关 | 临时方案，未标准化 |

逐字建议：*"For new systems, always use RFC 8785."*

### 五、Parquet 的版本兼容性（若有人主张用 Parquet，这些是反驳材料）

来源：Parquet 官方 *Format Versions* 页（2026-07-15 更新）。

**官方用 "forward compatible / forward incompatible" 而非 "backward compatible" 框架**（逐字）：
- **Forward compatible**：*"remain readable by older readers, with a possibly degraded experience... but the reader does not fail."* 例：bloom filters、`VARIANT` 逻辑类型注解。
- **Forward incompatible**：*"make the data unreadable to older software."* 例：新编码（`DELTA_*`、`BYTE_STREAM_SPLIT`、`RLE_DICTIONARY`）、Data Page V2 头。

**按版本的向前不兼容特性（逐字节选）**：

| parquet-format 发布版 | 向前不兼容特性 |
|---|---|
| **1.0.0** | INT96、PLAIN、Data Page V1、RLE、SNAPPY、GZIP 等基础 |
| **2.0.0** | **Data Page V2、RLE_DICTIONARY、DELTA_BINARY_PACKED、DELTA_BYTE_ARRAY、DELTA_LENGTH_BYTE_ARRAY** |
| **2.4.0** | **ZSTD、LZ4（已弃用）、BROTLI** |
| 2.7.0 | Modular encryption |
| 2.8.0 | BYTE_STREAM_SPLIT |
| 2.9.0 | LZ4_RAW |
| 2.14.0 | ALP（Preview） |

**两条对选型极重要的官方警告（逐字）**：
> *"Each Parquet file has a `version` field in the thrift FileMetadata. This field has historically been used **inconsistently**: writers populate `1` or `2` **without a consistent relationship to the features actually used**."*
> *"Note that release numbering **DOES NOT FOLLOW** semantic versioning: minor releases (e.g. `2.10.0` to `2.11.0`) sometimes contain **forward incompatible** features."*

**推论**：**如果阙疑用 Parquet 存账本，那么"这份账本在 2030 年还能被读出来"这件事依赖于 parquet 生态的实现状态，而不只依赖于格式规范。** 对一个目标是"十年后可复算"的账本，这是不必要的风险。**JSON 的 RFC 8259 + JCS 的 RFC 8785 都是 IETF 标准，且可以用 50 行 Python 实现。**

---

## 对阙疑的 3 条具体行动

1. **【2026-11 前】把账本存储格式固定为 `JSONL + JCS`，并在 `docs/ledger_format.md` 里写死规格。** 具体规格：
   - **文件**：`ledger/judgments.jsonl`，**每行一个判决对象**，行尾 `\n`（LF，不用 CRLF——用 `.gitattributes` 强制 `*.jsonl text eol=lf`）；
   - **哈希**：`entry_hash_n = SHA256( JCS(entry_n) || entry_hash_{n-1} )`，其中 `JCS()` 严格按 RFC 8785；**哈希输入绝不包含格式化空白**；
   - **禁止浮点数**：所有数值字段必须是整数或十进制字符串（正则 `^-?\d+(\.\d+)?$` 用于字符串形式，且**不得是 JSON number 类型的浮点**）；在 `tests/test_ledger_format.py` 中断言：账本中不存在任何"含 `.` 的 JSON number"；
   - **字段名不得重命名**：遵循方向 74 的结论（Confluent 官方该页**没有**给出字段重命名的兼容规则，重命名在 FULL 兼容下不成立）；
   - **理由引用**：JCS 指南逐字 *"semantically identical but hash to different values without canonicalization"* + *"JCS canonicalizes the actual floating-point value, not the value you intended"*。
   - **验收**：`tools/ledger_hash.py` 用 **两种不同的 JSON 库**（如 Python 标准 `json` 与 `orjson`）各自实现 JCS 序列化，对全部 452 条判决计算哈希，**必须逐条一致**——这是"跨库可复算"的最小验证。

2. **【2026-12 前】产出"双视图"账本：机器视图（canonical JSONL）+ 人视图（pretty-printed）。** 具体做法：
   - **机器视图**：`ledger/judgments.jsonl`（canonical，单行、无空白、键排序），**这是哈希的输入**；
   - **人视图**：`ledger/review/judgments_pretty.jsonl`（缩进 2 空格、键保持可读顺序），**这是给审稿人看的**，由 `tools/render_review_view.py` 从机器视图生成；
   - **一致性断言**：CI 里断言 `render_review_view(canonical) 的 JCS 结果 == canonical 的 JCS 结果`（即两个视图规范化后**必须同字节**）；
   - **为什么必须两份**：canonical JSONL 的可读性很差（无缩进、键按 UTF-16 排序），**审稿人读不了**；而 pretty 版本的字节不稳定，**不能用于哈希**。**两份是唯一同时满足"可审阅"与"可复算"的方案。**
   - **在 README 中给出审稿人操作指南**（3 行）：`git clone` → `python tools/verify_ledger.py` → 看输出 `{"entries": 452, "chain_ok": true, "merkle_root": "..."}`。

3. **【2027-02 前】在论文的 Reproducibility 小节里写一段"格式选择论证"，并附一张实测表。** 内容要求：
   - **主动承认二进制格式更快更小**，并**引用实测数字**：Parquet+zstd 是 CSV 的 **6.1×** 压缩、DuckDB 查询 **13.8×** 快（dataarchitect.studio, 2026-07-26，3M 行 × 11 列）；MessagePack 比 JSON 小 **20–50%**、解析快 **2–4×**（jsonic.io, 2026-05-12）；
   - **然后给出拒绝理由**，用**三条可验证的事实**而不是主观判断：
     (a) **规模事实**：阙疑账本 452 条判决，**估计体积 < 1 MB**（须实测后填入真实值），二进制格式节省的绝对体积可忽略；
     (b) **diff 事实**：二进制文件在 `git diff` 中只输出 *"Binary files differ"*，**审稿人无法审阅任何一条判决**；
     (c) **标准事实**：Parquet 官方文档逐字承认其 `FileMetadata.version` 字段 *"has historically been used inconsistently"*，且发布编号 *"DOES NOT FOLLOW semantic versioning"*——**对一个目标十年可复算的账本，这是不必要的格式风险**；
   - **结论句建议写法**：*"We choose JSONL with RFC 8785 canonicalization not because it is the most efficient format — measured benchmarks show Parquet+zstd achieves 6.1× compression and 13.8× faster analytical queries on a 3M-row dataset — but because reviewability is a first-class requirement of our evaluation protocol. A binary ledger cannot be audited by a reviewer with `git diff`, and our central claim is that the ledger is independently auditable."*
   - **时间点**：2027-02 前实测阙疑账本的真实字节数并填入。

---

## 盲区（诚实标注）

- **Benchmark A（vineetkukreti/data-format-comparison）的数据集规模、列数、数据类型分布均未在仓库 README 中说明。** 该仓库只有一个 `comparision_analysis.py`（Mar 17, 2025 提交）和 `requirement.txt`，**没有数据集说明、没有版本号、没有机器规格**。因此它给出的绝对数字（319.94 MB / 447.49 MB 等）**无法被解读为"某种数据上的典型值"**。我在正文中只用它做**格式间的相对比较**，并已标注这一局限。
- **Benchmark B（dataarchitect.studio）的作者自己也声明了五条局限**（逐字）：只有一个数据集形状、只用了 pyarrow 的 ORC writer 默认设置、完全没做调优、热缓存（**低估了小文件的优势**）、慢速双核笔记本 CPU（*"The absolute seconds mean nothing to you. The ratios are the deliverable."*）。**这是一份诚实的 benchmark，但仍是 n=1 数据集。**
- **MessagePack 的数字全部来自 jsonic.io（一个 JSON 工具站的推广文章）**，文中多处嵌入其自身工具链接，**且未提供可复现的 benchmark 仓库**。我逐字核对了它的数字，发现**其内部存在不一致**：正文称总缩减为 *"20–40%"*，而开头与 FAQ 均称 *"20–50%"*。**这些数字应被视为"量级参考"而非"精确测量"**，论文中引用必须标注来源性质。
- **"Protobuf 通常比 JSON 小 5–10×"这一数字来自 jsonic.io 另一篇指南的转引，我没有核实原始基准。** Protobuf 官方文档（`protobuf.dev`）我**没有打开**核对体积数据。
- **`git diff` 对二进制文件输出 "Binary files differ" 这一行为，我引用的是技术问答与 `.gitattributes` 官方文档的间接证据**，**没有找到 Git 官方文档中"二进制文件 diff 输出格式"的权威描述**。此外，`textconv` 与 `--text` 选项确实允许对二进制文件做文本 diff（需要配置转换器）——**我在正文中承认了这一点，并论证它不满足"第三方无需额外工具"的要求**。
- **RFC 8785 的具体规则我引用的是 jsonic.io 的解读，不是 RFC 原文。** 我确认了 RFC 8785 存在（`rfc-editor.org/rfc/rfc8785.pdf`，2020 年 8 月）**但没有逐页阅读 RFC 正文**。其中"数字用 ES2019 `Number::toString`"、"最多 17 位有效数字"、"UTF-16 码元排序"三条**必须回溯 RFC 原文核对**，因为它们是哈希正确性的基础。
- **JSON-LD Canonicalization（W3C）与 RFC 8785 的差异我未核实**，只从 jsonic.io 的对比表转引。
- **阙疑账本的真实体积我没有测量**，正文中的"几百 KB 到几 MB"是估计。行动 3 要求实测后填入——**在实测之前，论文里不能写任何体积数字**。
- **"审稿人会用 `git diff` 审阅"这个前提本身是一个假设。** NeurIPS E&D 的实际审稿流程我没有调研，**没有任何证据表明审稿人会去 clone 仓库看 diff**。因此行动 3 中"reviewability is a first-class requirement"这个论证**存在被审稿人反问"谁说的"的风险**。**更稳的表述**是把它与项目自身的核心卖点绑定："我们的核心主张是账本可被独立审计，而审计的最小成本路径是逐行文本 diff"——**这样论证的是"自洽性"，而不是"审稿人偏好"**。
- **样本偏差**：所有 benchmark 都在 10⁵–10⁷ 行量级、多列、分析型查询场景。**没有任何 benchmark 覆盖"452 行、每行 1 KB、只有追加没有查询"的场景**，因此本文对阙疑的建议是**从格式性质（行式 vs 列式、文本 vs 二进制）推理**，不是实测。

---

## 来源

1. `vineetkukreti/data-format-comparison` — *Performance Analysis of Modern Data Formats*（首次提交 2025-03-17） — https://github.com/vineetkukreti/data-format-comparison — 逐字表格：CSV 319.94 MB / JSON 447.49 MB / Parquet(PyArrow) 121.15 MB / Parquet(fastparquet) 123.40 MB / ORC 249.50 MB / Arrow-Feather 138.49 MB；写入 ORC 2.02s 最快、CSV 10.82s 最慢；读取 fastparquet 1.20s 最快、JSON 7.58s 最慢；过滤 Arrow 0.045s 最快、JSON 0.120s 最慢；内存 Arrow 440.45 MB 最低、**JSON 1995.02 MB 最高**；*"about 27% of the size of JSON and 38% of CSV"*
2. dataarchitect.studio — *Parquet vs ORC vs Avro Benchmark: Compression and Read Speed*（2026-07-26 发布 / 2026-08-08 更新） — https://dataarchitect.studio/essays/parquet-vs-orc-vs-avro-benchmark/ — 数据集 **3,000,000 行 × 11 列 / 未压缩 322 MB**；CSV 342.6 MB → Parquet+zstd **56.6 MB（6.1×）**；DuckDB 查询 **13.8×** 快（0.064s vs 0.879s）；列裁剪 Parquet **6.9×** / ORC **4.9×** / CSV **2.8×** / **Avro 0.96×（慢 4%）**；匹配编解码器 Snappy Parquet 小 **26%**、DEFLATE 小 **23%**；Avro 300k 行最优压缩仍比 Parquet 大 **63%**；zstd 19.3 MB/0.54s vs gzip 17.8 MB/16.00s；脚本与原始结果均公开
3. jsonic.io — *JSON vs MessagePack: Size, Speed, and When to Use Each*（2026-05-12） — https://jsonic.io/guides/json-msgpack — 逐字：*"20–50% fewer bytes"*、*"parses 2–4× faster"*；`{"name":"Alice","age":30}` JSON 23 B → MessagePack 14 B（**39%**）；10 KB 嵌套响应 → ~6,500 B（**36%**）；长文本仅 **2%**；gzip 后仅 **14%**，*"drops from ~35% to ~10–15%"*；msgpackr ~400/500 MB/s vs JSON ~200/250 MB/s（Node.js 20 / Apple M2）；Python CPython 3.12 `msgpack.packb()` ~150 MB/s vs `json.dumps()` ~60 MB/s（**2.5×**）
4. jsonic.io — *JSON Canonicalization (JCS, RFC 8785): Deterministic Serialization*（2026-05-13） — https://jsonic.io/guides/json-canonicalization — 逐字：*"`{"a":1,"b":2}` and `{"b":2,"a":1}` are semantically identical but hash to different values without canonicalization"*；四条规则（UTF-16 码元键排序 / ES2019 `Number::toString` 最多 17 位有效数字 / 无空白 / 只转义 U+0000–U+001F）；*"JCS canonicalizes the actual floating-point value, not the value you intended"*；`0.1+0.2` → `0.30000000000000004`；`Infinity`/`NaN` 必须报错；RFC 8785 发布于 **2020 年 8 月**
5. RFC 8785 — *JSON Canonicalization Scheme (JCS)* — https://www.rfc-editor.org/rfc/rfc8785.pdf（IETF, 2020-08） — **规范本体，未逐页核对**
6. Parquet 官方 — *Parquet format versions*（2026-07-15 更新） — https://parquet.apache.org/docs/file-format/versions/ — 逐字：forward compatible vs forward incompatible 框架；**1.0.0** 基础类型 + Data Page V1；**2.0.0** Data Page V2 / RLE_DICTIONARY / DELTA_*；**2.4.0** ZSTD / BROTLI（**向前不兼容**）；**2.6.0** UUID + 纳秒 TIME/TIMESTAMP（向前兼容）；*"This field has historically been used inconsistently: writers populate 1 or 2 without a consistent relationship to the features actually used."*；*"release numbering DOES NOT FOLLOW semantic versioning"*
7. Apache Arrow 官方 — *Reading and Writing the Apache Parquet Format*（2026-08-11 更新） — https://arrow.apache.org/docs/python/parquet.html — 逐字：*"Apache Arrow is an ideal in-memory transport layer for data that is being read or written with Parquet files."*（**说明 Arrow 是内存传输层，不是持久化格式**）
8. Git 官方 — *gitattributes Documentation* — https://git-scm.com/docs/gitattributes — 逐字：*"Files encoded in certain other encodings (e.g. UTF-16) are interpreted as binary and consequently built-in Git text processing"* 不适用
9. 博客园 Snail-0304 — *gitattributes*（2022-03-12） — https://www.cnblogs.com/snail-0304/p/15997884.html — 逐字：*"Performing text diffs of binary files：git diff 以文本的形式显示二进制文件"*（**说明 textconv 机制存在，但需额外配置**）
10. CSDN 问答 — *Git GUI 中 "rescan" 总提示 "binary files differ"*（2025-09-10） — https://ask.csdn.net/questions/8731876（**二手，佐证二进制 diff 的行为**）
11. jsonl.co — *JSON vs JSONL: What's the Difference? Complete Guide* — https://jsonl.co/guide/json-vs-jsonl — 结构、流式解析、用例对比（**二手，本文的 JSONL vs JSON diff 分析为本文自行推导**）
12. CSDN — *大数据常见存储格式对比：Parquet、ORC、Avro、Arrow 与 Lance*（2026-07-31） — https://blog.csdn.net/helianxiaoye/article/details/157261798（二手综述，**本文未深入使用**）
13. CSDN — *JSON 与 JSONL 比较*（知乎转载，2024-05-01） — https://zhuanlan.zhihu.com/p/1965438531926225357（二手，JSON/JSONL 核心区别）
