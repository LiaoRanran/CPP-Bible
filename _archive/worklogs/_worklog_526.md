# 526 批次E 交接 · claim 结构化 v0.3（L3 智能层点火）

> 仓库 `C:\CodeLearnling\note\note\C++\CPP-Bible`　性质：**命题级知识结构**的首批落地。
> 铁律遵守：不 push、不 golden accept；一规则一 commit + 毒样例 + pytest；存量零误伤；
> 不编造（拿不准的标 inference 并写明）；`extracted_by` 字段保留。

---

## Step 1：样板回填（commit `7602058`）

`ATOM-CONC-FENCE-001` 的 claim 拆成两条原子命题（**原自然语言 `claim` 原样保留**，并列补充）：

| 命题 | 类型 | 三元组 | 支撑 |
|---|---|---|---|
| prop-1 | **observation** | 内存屏障(fence) · 落在循环体内时 · 阻止编译器消除该循环 | EV-CONC-001 + EV-CONC-002（两张卡都实测了消除/保留方向） |
| prop-2 | **inference** | 内存屏障(fence) · 不提供 · 数据竞争原子性/不建立happens-before | EV-CONC-002 + `external_basis`=ISO/IEC 14882:2023 [atomics.order] / cppreference |

* 两条均带 `extracted_by: writer`（铁律 6：不许删——将来模型自动抽取写 `model`）。
* 与提示词示例的**一处偏差**：prop-1 的 evidence 由 `[EV-CONC-001]` 扩为
  `[EV-CONC-001, EV-CONC-002]`。理由：两条命题的"消除/保留"判据两张卡都实测了
  （EV-CONC-002 的 `signal_fence` 零指令保循环正是 prop-1 的关键一环），只挂一张会漏掉
  另一半机器闭环。**若监工认为该按原样只挂一张，改这一处即可**（不影响任何规则）。
* 验证：`parse_frontmatter` 正确读出块序列+块映射嵌套；gate BLOCK=0/WARN=31 无回归。

### 概念名体检（铁律 5 要求"新造别名前先 grep"）

| 写法 | 出现次数 | 层面 |
|---|---|---|
| `内存屏障` | 50 | 原子卡 / 证据卡（规范名，本批采用 `内存屏障(fence)`） |
| `栅栏` | 51 | `Book/` 章节口语（ch108/ch109 等，如"选 relaxed 省了栅栏""全栅栏"） |

⇒ **同一概念两种写法**：概念层已按原子层写法统一为 `内存屏障(fence)`；
`Book/` 的"栅栏"本批**不改**（属教材行文，改动面大且不在本批范围）。
**这是概念图谱的一个已知缺口**：将来若做概念别名归一（concept alias），应把
`栅栏 → 内存屏障(fence)` 登记为别名，否则图谱里同一概念会分裂成两个节点。

---

## Step 2：三条规则

### 规则1 `ATOM-CLAIM-STRUCTURED`（commit 待填）

* **新卡**（不在 STAGING）无 `claim_structured` → **block**。
* **存量**（`tools/claim_structured_staging.txt` 27 张）→ **warn**，人逐批回填。
* 结构校验（任一不满足 → block）：必填六字段；`claim_type ∈ {observation, inference}`；
  命题 `id` 卡内唯一；`extracted_by` 命题级或卡级至少一处。

**为何用名单而不是"按 status 判新老"**：`status=draft` 的老卡会被误 block，
`status=verified` 的新卡会被误放行——名单是显式的。名单**不需要维护**：
回填是加法，卡带上 `claim_structured` 后第一条不再触发，自然退出 STAGING。

**`extracted_by` 的两种读法**：526 §二 写"末尾保留 `extracted_by: writer`"，
既可读作"每条命题末尾"也可读作"列表末尾（卡级）"。判据**两级都收**（宁松勿错杀），
样板卡按命题级写，测试覆盖卡级回退。

**实测**：规则 55→56；存量命中 **26 warn / 0 block**（27 卡 − 已回填样板卡）；
gate BLOCK=0 / **WARN 31→57** / ADVICE=5（exit 0）；poison **76/76** exit 0；
RULE-COVERAGE 30/55→**31/56**；tests +4（另有元测试 `test_advice_rules_never_block`
的干净卡同步补命题——新卡强制项出现后，"最小合法原子"定义变了）。

### 规则2 `OBSERVATION-NEEDS-ARTIFACT`（commit 待填）

* observation 命题的 `evidence` 里**至少一张**卡要带工件断言，否则 **block**（零容忍）。
* 工件断言口径（`_has_artifact_assertion`）：`artifact_assert` 非空 **或**
  `actual.run_match_file` 非空。**不**把 `actual.run_match_keys` 单独存在算进来
  ——没有留痕文件时它无载体（与 500 规则 EV-RUN-KEY-DECLARED-EXISTS 同口径）。
* 引用**不存在**的证据卡也算无支撑（消息里区分"卡不存在"与"卡存在但无断言"）。
* 修法提示写明退路："拿不出工件说明它其实是 inference——改 claim_type 并补
  `external_basis`/人签"，而不是让人硬凑一张假证据卡。

**实测**：规则 56→57；**存量命中 0**（样板卡 prop-1 挂的 EV-CONC-001/002 都带
`artifact_assert`）；gate BLOCK=0 / WARN=57 不变；poison RULE-COVERAGE 31/56→**32/57**；
tests +4。元测试 `test_advice_rules_never_block` 的干净卡改用 **inference** 命题
（observation 会要求证据卡，而该沙箱无证据卡——用 inference 才不会让失败原因
偏离该测试的本意）。

> **环境真相（非本规则引入）**：本轮复跑 poison 时 P2（唯一真编译的样例）报
> `infra_error:replay_busy` —— 同仓有**其他进程**在并发跑 `tools/prepush_check.py`、
> `tools/adversarial_regression.py`、`_adv_v80/probe_core2.py`（非本会话启动），
> 持有 replay 锁。**未杀他人进程**，收工复跑确认。

### 规则3 `INFERENCE-NOT-MACHINE-VERIFIED`（commit 待填）

* 判据：卡上有 inference 命题 且 `status ∈ VERIFIED_STATUSES`，但 `status_history` 里
  **没有合法人级签署** ⇒ **block**（核心放权闸：机器复算再绿，也证明不了"这层解释对"）。
* **降级唯一通道**：该命题带 `external_basis` 且该基准已登记在 `sources` 的
  `independent: true` 来源 ⇒ warn（标准源视同独立佐证）。
* `_has_human_signoff()` **复用 `principal_ok` 单点**，没写 `startswith("human:")`：
  后者会把 `human:`（空名）、`human:随便谁` 当有效签署——那正是 P13 空名签收漏洞。
  测试与毒样例都钉了这条（P65-阴3）。
* `_basis_registered()` 的匹配口径：取基准里的**标准标识 token**（≥5 位数字 / ≥6 字符英文
  标识 / 提交哈希），命中任一 independent 来源的 ref 即算登记。
  **不认 4 位数字**（`2023` 这类年份会与任何引用该年标准的来源撞车 ⇒ 闸门形同失效）；
  也不做精确串比（基准写法天然碎片化，精确比会把已登记的判成未登记 ⇒ 逼人重写措辞）。

**判据作用在卡级签署上的边界（记下来待下一批）**：G6 的 `verified` 是**卡级**状态，
命题级签署尚无载体 ⇒ 本规则只能问"整卡有没有人签"。因此一张卡上若只有一条 inference
命题有人签、其余靠 `external_basis`，也会放行。**要细化到命题级**需要新字段
（如每条命题带 `signed_by`），属下一批的 schema 变更——本批不擅自扩 schema
（526 §七"明确不做"）。

**实测**：规则 57→58；**存量命中 0**（样板卡 prop-2 有 `human:liaoranran` 在册签署）；
gate BLOCK=0 / WARN=57 不变；poison **83/83** exit 0；RULE-COVERAGE 32/57→**33/58**；
tests +5。

> **自查抓到的样例缺陷（值得记住）**：P65 与 block 用例最初用的载荷**同时**带
> `external_basis: ISO/IEC 14882:2023` 与含 `14882` 的 independent 来源 ⇒ 实际走的是
> "已登记 ⇒ 降级 warn"分支；只因样例只断言"规则 id ∈ who"（不看 severity）而**假通过**。
> 已补"无基准 / 基准未登记"两个变体让 block 路径真正被覆盖。
> 教训：**含降级分支的规则，positive 样例必须断言 severity，且载荷要避开降级条件**。

---

## Step 3：存量扫描（27 张，**只扫不改**）

### 3.1 规则实测命中

| 规则 | 命中 | 说明 |
|---|---|---|
| `ATOM-CLAIM-STRUCTURED` | **26**（warn 26 / block 0） | 27 卡 − 已回填的样板卡；**零 block**（存量零误伤） |
| `OBSERVATION-NEEDS-ARTIFACT` | **0** | 判据只在"卡有 claim_structured"后生效，现只有样板卡有，且它已合规 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | **0** | 同上；样板卡有 `human:liaoranran` 在册签署 |

> ⚠️ **规则2/3 的 0 命中是"结构性 0"**，不是"全库干净"——它只说明**回填尚未发生**。
> 只看这个数会得到假安全感，故补 §3.2 的前瞻体检。

### 3.2 前瞻体检（回填后会撞哪条规则）

对每张卡预先算"它回填成 observation / inference 后会不会被拦"：

| 体检项 | 结果 |
|---|---|
| **observation 回填安全性** | **27 张全部安全**：所有卡引用的证据都解析得到，且**每张证据卡都带工件断言**（`artifact_assert` 或 `actual.run_match_file`）⇒ 它们拆成 observation 不会撞规则2 |
| **inference 回填风险** | **3 张无人级签署** ⇒ 回填 inference 命题会被规则3 **block**：`ATOM-MEM-ALLOC-002`、`ATOM-MEM-LEAK-002`、`ATOM-MEM-PERF-004`（三张均为 `red-team-verified`：有 redteam 签署，**不是**人级） |
| 另 1 张无人签 | `ATOM-LANG-INLINE-001`（`draft`）——尚未晋升 verified，规则3 现在不拦；但它若回填 inference 命题，**将来晋升 verified 时**同样需要人签或已登记基准 |

**结论（给回填者的路线）**：
1. **observation 可以放心拆**——本库证据底座是干净的（工件断言 100% 覆盖）。
2. **inference 拆之前先看两件事**：这张卡有没有人签？没有的话，这条命题是否有
   ISO/cppreference 级的独立基准可登记进 `sources(independent: true)`？
   两者都无 ⇒ 该命题现在**不该**进库（这正是 526 想暴露的"站不住的 claim"）。
3. 三张 `red-team-verified` 卡是**第一批要看**的：它们的 claim 里若有解释性论断，
   G6 的放权链决定了"红队验过"≠"人签过"。

### 3.3 本批未做（按提示词"明确不做"）

* **未批量改存量卡**：只 warn，人逐批回填（提示词 §七 第 1 条）。
* **未自动给存量卡分类** observation/inference：铁律 4 要求"拿不准的标 inference 并请人
  定夺"——由机器猜分类再批量写进卡，等于把人的判断伪造成机器的判断。
* 未改现有 `claim` 自然语言字段（并列补充，不替换）。

---

## Step 4：知识图谱 concept 层（commit 待填）

### 4.1 设计取舍

| 点 | 决定 | 理由 |
|---|---|---|
| 存储 | **独立 `concepts` / `concept_edges` 两表**，不塞进 `nodes`/`edges` | `nodes.id` 是"身份"（带 path/status），概念名是自然语言短语（无 path/status）；混进去会让 `orphans` 把概念全判成孤立、并污染 `deps`/`impact` 的遍历语义 |
| 边语义 | `subject → object`，**边上带 atom/prop/predicate/claim_type/statement** | 命题不能脱离卡存在：任何概念结论都要能回到原子卡找它的证据与命题类型。这是本图谱不做"纯概念库"的底线 |
| 谁进概念层 | **只有带 `claim_structured` 的原子** | 缺字段是"还没拆"（gate 的 ATOM-CLAIM-STRUCTURED 在 warn），不是"错"。图谱只如实反映"目前有多少命题可推理"，不替门禁判合规 |
| 幂等 | build 时 DROP 两表重建 | 与 nodes/edges 同法；重复跑不产生残影 |

### 4.2 实测（真实仓库）

| 项 | 数值 |
|---|---|
| 节点 / 边 | **323 / 291**（节点 320→323 是 RULE 55→58 之故；边数不变） |
| **概念 / 命题边** | **3 / 2** |
| 概念清单 | `内存屏障(fence)`（2 条，主 2）、`阻止编译器消除该循环`（1 条，宾 1）、`数据竞争原子性/不建立happens-before`（1 条，宾 1） |
| `concepts "内存屏障(fence)"` | 回 2 条命题（`observation` 1 / `inference` 1），带 `ATOM-CONC-FENCE-001:prop-*` |
| `concepts "栅栏"` | **显式"没有该概念"**（exit 1）——这正是 §概念名体检 里那个缺口的可观测后果 |

> 概念 3 个而不是 2 个：两条命题各贡献 subject+object，其中 subject 都是"内存屏障(fence)"
> 去重后为 3 个不同名字（1 主 + 2 宾）。**这解释了为何"概念数是 3"不是错**。

### 4.3 一个直接可用的推论

`concepts "内存屏障(fence)"` 现在能回答"**这个概念的哪些部分是观测、哪些是推断**"
（上例 observation 1 / inference 1）。526 §八 说的"图谱能问：哪些命题在谈内存屏障"
已经可用；下一步（**不在本批**）是"两条命题是不是互相矛盾"——那需要命题级的可比对结构
（同一 subject 下的 predicate 冲突检测），本批只把数据摆进图，不擅自下判断。

---

## 收工验收（提示词 §六，fresh run）

| # | 命令 | 实测 | 与基线对比 |
|---|---|---|---|
| 1 | `gate_engine.py --check` | exit 0 · BLOCK=0 / **WARN 31→57** / ADVICE=5 · 规则 **58** | +3 规则（526 三条）；+26 warn 全是规则1 的存量 STAGING |
| 2 | `atom_evidence_replay.py --check` | exit 0 · **confirm=56 / refute=0 / infra_error=0** | 与基线一致 |
| 3 | `poison_drill.py` | exit 0 · **83/83** · RULE-COVERAGE **30/55 → 33/58** | +11 样例（P63×4 / P64×3 / P65×4） |
| 4 | `pytest -m fast` | exit 0 · **150 点全绿** | 新增测试都在 fast 组 |
| 5 | `knowledge_graph.py stats` | **323 节点 / 291 边 · 概念 3 / 命题边 2** | 节点 320→323（RULE 55→58） |

**测试点数**：`tests/test_gate_engine.py` 107→112（+5 规则3 用例，规则1/2 的 8 个已在各自
commit 计入）、`tests/test_knowledge_graph.py` 4→6（概念层 2 个）。
权威口径仍取 `.pytest_cache/v/cache/nodeids`，**不数进度点**（508 的教训）。

### 交付清单

| 类型 | 文件 |
|---|---|
| 数据（样板） | `atoms/conc/ATOM-CONC-FENCE-001.md`（+`claim_structured` 2 条命题） |
| 门禁 | `tools/gate_engine.py`（3 规则 + 4 helper） |
| 毒样例 | `tools/poison_drill.py`（P63–P65 共 11 样例 + `_atom_who` 探针 + 攻击面映射） |
| 迁移名单 | `tools/claim_structured_staging.txt`（27 张存量，只 warn） |
| 图谱 | `tools/knowledge_graph.py`（concepts/concept_edges + `concepts` 查询） |
| 测试 | `tests/test_gate_engine.py`（+13）、`tests/test_knowledge_graph.py`（+2） |

### 给下一批的 handoff（本批只扫不改，故这些是**开放项**）

1. **26 张卡待回填 `claim_structured`**（gate 会一直 warn 到回填完）。
   回填路线见 §3.2：observation 安全；inference 先看人签/独立基准。
2. **3 张 `red-team-verified` 卡**（`ATOM-MEM-ALLOC-002`/`LEAK-002`/`PERF-004`）无人级签署：
   它们的 claim 里若有解释性论断，回填 inference 会被规则3 拦——**这正是本批要暴露的**。
3. **概念名归一（`栅栏` ↔ `内存屏障(fence)`）**：Book/ 层 51 处口语写法，概念层现在只认
   原子层写法。要做别名表就得改概念层 schema（本批不擅自扩）。
4. **命题级签署**：规则3 目前只能判"整卡有没有人签"（G6 的 verified 是卡级状态）。
   要精确到"这条 inference 谁背的书"，需要新字段（如每命题 `signed_by`）。
5. **概念冲突检测**：同 subject 下 predicate 打架（如 A"提供"X 与 A"不提供"X）——
   数据已进图，判据未写。属"自我审计知识质量"的下一步。
6. **`_adv_v80/` 与 `_worklog_*.md`** 仍未跟踪（既有惯例，未动）。
