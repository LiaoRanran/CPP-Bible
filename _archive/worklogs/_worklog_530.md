# 530 批次H 施工日志 · 让已建结构兑现承诺

> 依据：`References/architecture_架构演进/530_批次H施工提示词_让已建结构兑现承诺_最终施工版.md`
> 纪律：一任务一 commit；不 push；不 golden accept；改核心工具跑全量 pytest；数字实测为准。

## 幂等进度看板（新会话从这里续）

```
- [x] T1 增量指纹补 .out（commit=5eabcf4 + 基线 a36d71d）
- [x] T2 帧/伪指令断言收口（commit=3616799）
- [x] T3 拆 contrasts/contradicts + 概念连通指标 + concept-islands + ATOM-CLAIM-CONCEPT-NORMALIZED warn（commit=9942d8c）
- [x] T4 OBSERVATION-LIVENESS 活性判据 warn（commit=2c19aaf）
- [x] T5 warn 会计制度（accept 强制分类）（commit=da85a2e）
- [x] T6 CPVA 补 redteam/revision/human_review 阶段（commit=f3025b4）
- [x] T7 task_queue.py SQLite 最小队列（commit=d976170）
- [x] 收工全量门禁（2026-09-15 fresh run，全部实测，见 §8）
```

---

## 0. 开工实测（2026-09-15，HEAD=`3319d2c`）

| 项 | 实测输出 |
|---|---|
| `git rev-parse --short HEAD` | `3319d2c`（`fix(prepush): hook优先.venv解释器 + 刷新tool_integrity基准`） |
| `gate_engine.py --check` | `[gate] 规则 58 条 · 命中 64 (block=0 warn=59 advice=5)`，exit 0 |
| `poison_drill.py` | `[poison] 86/86`；`RULE-COVERAGE: 33/58 注册规则被毒样例覆盖（另登记豁免 27 条）`；`零覆盖攻击面：无` |
| `knowledge_graph.py build/stats` | `节点 323（其中卡节点 165）· 边 291 · 概念 157 / 命题边 79`；节点分布 MISCONCEPTION=79、RULE=58、EVIDENCE=56、ARTIFACT=51、FIXTURE=49、ATOM=30；边分布 REFERENCES=67、ASSERTS=60、SERVES=58、USES=56、PREREQUISITE=27、**CONTRADICTS=23** |
| `knowledge_graph.py conflicts` | **候选矛盾 19 组**（全部为"仅凭声明的 CONTRADICTS 边 → 多半是对照"，无极性相反对） |
| `git status --porcelain -- Examples/atoms/ atoms/ evidence/ tools/golden_state.json` | 空（受控目录干净） |
| 并发 python 进程 | 2 个（`33436` / `38168`）；`build/.replay_lock` 存在（未验证是否活跃，replay 未跑） |
| golden_lock | 基线漂移已于 `67c1962` 由人 accept（warn 54→59），非本批事项 |

### 开工异常记录（诚实记录，不掩盖）
- **首跑 poison = 85/86**：失败项为阴性对照被污染（`gate block=5`，详情含 `[DOC-ZERO-PLACEHOLDER] 占位符 xxx`）。
  该首跑与 `gate_engine --check`、`knowledge_graph build` **同批并行执行**。
- **复测**：随后 4 次串行运行全部 `86/86`（含 3 连跑专测），**未复现**。
- 判定：非本批代码引入；沙箱为 `tempfile.mkdtemp(prefix="poison_")` 独立目录，理论互不污染。
- 遗留改进（低优先，待办）：阴性对照失败详情只打印 `[rule_id] message`，**不含文件路径**，导致无法定位污染源；后续可在 detail 中追加 `f.file`。
- 纪律执行：本批所有门禁一律**串行**跑，不再与其它同仓命令并行。

---

## 3. T3 拆 contrasts/contradicts + 概念连通指标 + concept-islands + 新规则（2026-09-15）

### 3.1 kg 改动（`tools/knowledge_graph.py`）
- `REL_MAP`：`contrasts → CONTRASTS`、`contradicts → CONTRADICTS`（原二者都归 CONTRADICTS，
  对照噪声淹没真矛盾）。
- `conflicts()`：`CONTRADICTS` 边 → 进 `items`（冲突候选，须人工裁决）；`CONTRASTS` 边 →
  只进 `browse`（对照浏览清单，不报警）。返回新增 `contrast_pairs` / `browse` 键（旧契约
  `{"candidates":0,"items":[]}` 的既有测试 `test_conflicts_no_false_positive_on_neutral_props`
  已同步更新）。
- `stats()`：新增 `concepts_multi_atom`（跨原子概念数）、`max_component`（概念最大连通分量，
  union-find 无向）。
- 新增 `concept_islands()`（只出现在 1 颗原子的概念，回填 backlog）+ 子命令 `concept-islands`。

### 3.2 gate 新规则（`tools/gate_engine.py`）
- `ATOM-CLAIM-CONCEPT-NORMALIZED`（warn，命题级）：claim 命题 `object` 须属规范概念集 =
  `kg concepts 表中作过 subject 的概念 ∪ concept_aliases.txt 规范名 ∪ 可枚举观测值白名单
  (true/false/数值/编译器版本)`。object 只是句子的 → warn「无法与图谱连通」。
- 关键设计：`_concept_normalized_set()` 只认 `as_subject>=1` 的概念——若用"全部 concepts"
  则恒真（build 把每个 subject/object 都写进 concepts）。白名单分支覆盖 true/false/数值/c++NN/
  编译器版本。
- 护栏 5：warn 级，存量零新增 block。

### 3.3 实测基线（T3 收工，真实仓库）
| 项 | 实测 |
|---|---|
| `kg stats` 边分布 | CONTRASTS=**22**、CONTRADICTS=**1**（原 CONTRADICTS=23 全量） |
| `kg conflicts` | **候选矛盾 1 组**（C×D 真矛盾）；另 **18 组 CONTRASTS 对照对**仅入浏览清单、不报警（原 19 组全进候选） |
| `kg stats` 概念连通 | 跨原子概念 **0** / 最大连通分量 **3**（首跑预期≈0，符合提示词） |
| `kg concept-islands` | 概念孤岛 **157** 个（只出现在 1 颗原子） |
| `gate --check` | 规则 **59** 条 · 命中 141（block=0 warn=136 advice=5）→ **warn 59→136（+77，其中 ~70 来自新规则，属预期债务：多数 mem 命题 object 未归一化成 subject 概念；护栏 5 仅要求 block=0）** |
| `poison` | **88/88**；RULE-COVERAGE 34/59；零覆盖攻击面：无（P67/P67-阴 + ATTACK_TYPES 映射 A1） |

### 3.4 测试
- `tests/test_knowledge_graph.py`：+3 例（conflicts 分流 / 概念孤岛 / 连通度指标）；既有
  `test_conflicts_no_false_positive_on_neutral_props` 因返回契约扩展同步更新。全 14 例通过。
- `tests/test_gate_engine.py`：T2 已覆盖（伪指令断言）。新 gate 规则由 `poison_drill.py` P67 端到端覆盖（RULE-COVERAGE 硬门禁）。

---

## 4. T3 存量 warn 命中清单（交人判读，**未改任何 atom 文件**）

`ATOM-CLAIM-CONCEPT-NORMALIZED` 在真实仓库命中 **79 条命题 / 27 张卡**（gate 侧计入 warn 的
为 77 条，另 2 条 object 落在白名单/规范集）。**成因单一**：这批 527/528 回填的
`claim_structured.object` 写的是**读数串或整句**（`single_result=200000；…`、
`阻止编译器消除该循环`），不是概念名 ⇒ 图谱连通性为零（T3 量得跨原子概念 0）。

| 卡 id | 命中命题 | object 形态（截断） |
|---|---|---|
| ATOM-CONC-FENCE-001 | prop-1,prop-2 | 阻止编译器消除该循环… |
| ATOM-CONC-LOCK-001 | prop-1,prop-2 | single_result=200000；mutex/atomic/… |
| ATOM-CONC-RACE-001 | prop-1,prop-2,prop-3 | single_total=100000、race_ops_total… |
| ATOM-HIST-AUTOPTR-001 | prop-1,prop-2,prop-3,prop-4 | 转移而非拷贝（拷贝后源为空、目标值=42… |
| ATOM-LANG-INLINE-001 | prop-1,prop-2,prop-3 | -O0 下 ab_tu_a=ab_tu_b=1、ba_tu_a=ba… |
| ATOM-MEM-ALIGN-001 | prop-1,prop-2,prop-3 | sizeof(Padded)=8（大于成员大小之和）… |
| ATOM-MEM-ALLOC-001 | prop-1,prop-2,prop-3,prop-4 | allocate 路径 allocs=1 / ctors=0；con… |
| ATOM-MEM-ALLOC-002 | prop-1,prop-2,prop-3 | arena 32B / bitmap 181B / pool 805… |
| ATOM-MEM-LEAK-001 | prop-1,prop-2,prop-3 | constructed=3、destroyed after scop… |
| ATOM-MEM-LEAK-002 | prop-1,prop-2,prop-3 | cycle_allocated=2 / cycle_destroye… |
| ATOM-MEM-MOVE-002 | prop-1,prop-2,prop-3 | 构造分配=1、拷贝分配=1、移动分配=0… |
| ATOM-MEM-NEW-001 | prop-1,prop-2,prop-3 | after new alloc=1 ctor=1；after del… |
| ATOM-MEM-PERF-001 | prop-1,prop-2 | Value32 sizeof=32 时 move_eq_copy_b… |
| ATOM-MEM-PERF-002 | prop-1,prop-2 | max_zero_alloc_len=15 / first_heap… |
| ATOM-MEM-PERF-003 | prop-1,prop-2,prop-3 | sizeof_string=32、sso_capacity=15、f… |
| ATOM-MEM-PERF-004 | prop-1,prop-2,prop-3 | tight_same_line=1 / padded_same_li… |
| ATOM-MEM-RAII-001 | prop-1,prop-2,prop-3 | RAII 路径后 g_live=0；裸 new/delete 路径后… |
| ATOM-MEM-RAII-002 | prop-1,prop-2,prop-3,prop-4 | unique_ptr 成员拷贝被删除（copy_constructi… |
| ATOM-MEM-RVREF-001 | prop-1,prop-2,prop-3 | 直接用（as_is）copy=1 move=0；std::move… |
| ATOM-MEM-SHARED-001 | prop-1,prop-2,prop-3 | make 后 use_count=1、copy 后=2… |
| ATOM-MEM-SHARED-002 | prop-1,prop-2,prop-3 | sizeof(shared_ptr)=16、copy 后 use_c… |
| ATOM-MEM-UNIQUE-001 | prop-1,prop-2,prop-3 | 裸指针（sizeof(unique_ptr<Big>)=8… |
| ATOM-MEM-UNIQUE-002 | prop-1,prop-2,prop-3 | default=8、stateless=8（EBO 吸收）… |
| ATOM-MEM-VALUE-001 | prop-1,prop-2,prop-3 | decltype((x))⇒lvalue（glvalue ∧ ¬rv… |
| ATOM-MEM-VALUE-002 | prop-1,prop-2,prop-3 | T& &⇒int&、T& &&⇒int&、T&& &⇒int&… |
| ATOM-MEM-WEAK-001 | prop-1,prop-2,prop-3 | 有 weak 时 use_count=1（不增计数）… |
| ATOM-UB-GRAY-001 | prop-1,prop-2 | GCC 15.3/13.1 × -O0/-O2（cxx17）四组… |

> **处置建议（人裁，本批不做）**：把 `object` 收敛成"概念名"（读数/对照值搬去
> `falsification` 或 `statement`），并把这 79 条里的概念名逐个登记进
> `tools/concept_aliases.txt`；或反向承认"命题不是三元组"、改 `claim_type: inference`。
> 单纯 `--accept` 不解决连通性（T3 的 stats 仍会显示跨原子概念 0）。

---

## 5. T4 OBSERVATION-LIVENESS 活性判据（2026-09-15）

### 5.1 改点（`tools/gate_engine.py`，新增于 `OBSERVATION-NEEDS-ARTIFACT` 之后）
新规则 `OBSERVATION-LIVENESS`（**warn**，规则级同）：`claim_type=observation` 的命题，
其 evidence 卡除"有工件断言"外，须**至少满足其一**，否则 warn：
① `_falsification_quantified()`（复用 EV-FALSIFICATION-QUANT 正则口径，取反用）；
② `_has_fixture_specific_assert_symbol()`（复用 EV-ASSERT-SYMBOL-MAPPED 的 `_assert_targets`
/ `_assert_haystack` / `symbol_map` / `_is_universal_symbol` 全套出处判定）；
③ `_has_non_env_run_key()`（复用 EV-ENV-DEPENDENT-KEY 的 `_is_env_key` 键表）。

三个判定抽成模块级单点函数（规则与 pytest 共用一套，不重写第二遍）。

**收窄了一处自己先写的偏移**：③ 初版在"未声明 `run_match_keys` 时回落读 `.out` 键行"，
实测（50 条 observation 命题）与"只看声明键"**零差异**，却给伪造留后门——往 `.out` 多写
一行非环境量键就能把死观测洗成活观测 ⇒ 改为**只认已声明键**（未声明读数本就是
`EV-OUT-UNDECLARED-KEY` 的辖区）。

**不重复报警**：命题无证据卡、或证据卡均无工件断言 → 交 `OBSERVATION-NEEDS-ARTIFACT`（block）。

### 5.2 实测（T4 收工）
| 项 | 实测 |
|---|---|
| 存量命中 | **0 条**（全仓 **50 条 observation 命题**，逐条查三条件：C1/C2/C3 至少一条成立） |
| 逐命题诊断抽样 | FENCE-001 prop-1 C1/C2/C3 全真；LOCK-001/RACE-001 两条 prop-1 各 C1+C3 真；INLINE-001 prop-1 C1+C2+C3 真（即验收 §1 的正例形态） |
| `gate --check` | 规则 **60** 条 · 命中 141（block=0 warn=136 advice=5）→ 新规则 **0 命中**（与上一致） |
| `poison` | **90/90** · RULE-COVERAGE **35/60** · 零覆盖攻击面：无（P68/P68-阴） |
| pytest | `tests/test_gate_engine.py -k observation`：**7 passed**（含 T4 三例） |

> **诚实说明（为什么是 0）**：T4 要堵的是「把推断自标 observation」这条路，而**现有 27 卡里
> 没有靠这招混进来的样本**——50 条 observation 命题挂的卡都带真对照（量化证伪或特有符号）。
> 换句话说本批的 observation 存量**已饱和**、未发现真漏网，不是规则没生效（P68 毒样例证明
> 它能拦）。故无命中清单可填。

### 5.3 测试与覆盖
- `tests/test_gate_engine.py`：+3 例（死观测须 warn **且断言 severity=="warn"**〔护栏 2〕/
  有活性对照须放行 / 无工件断言时不越界）。
- `poison_drill.py`：+P68（只挂 run_match 卡的 observation → warn，含 severity 断言 与
  `"OBSERVATION-LIVENESS" in who` 字面量）/ +P68-阴（特有符号 + 量化证伪 → 放行）；
  `ATTACK_TYPES` 登记 `("P68 ", "A1")`；`poison_surface_map.json` 台账重算。

### 5.4 ⚠️ golden_lock 漂移（**按铁律未 accept，留红作人审信号**）
- 基线 `tools/golden_state.json` = `1b0232d`（528 收工，warn 59）；现状 **warn 136**。
- `golden_lock.py check` → `[golden] 恶化 1 · 改善 0 / WORSE warn_findings: 59 → 136`（exit 1）。
- 故 **`tests/test_json_output.py::test_golden_lock_json`（slow）转红**——与 528 同型，
  是 S4 人审信号，非缺陷（收工门禁只要求 `-m fast`，该阶段全绿）。
- 漂移构成（**逐条可解释**）：+77 = T3 `ATOM-CLAIM-CONCEPT-NORMALIZED`（§4 的 79 条真债务）；
  +0 = T4（存量 0 命中）。**无一条来自内容退化**。
- 人审 accept 命令（**本苦力未执行**；⚠️ **形态已被 T5 收紧**：无 `--classify` 一律 exit 2，
  见 §6）：
  ```powershell
  .venv\Scripts\python.exe tools/golden_lock.py check --accept "530 批次H：规则 59->60，warn 59->136。增量 +77 全为 T3 新规则 ATOM-CLAIM-CONCEPT-NORMALIZED 对存量 79 条命题的统计（object 写成读数串/整句，非概念名，属 527/528 回填期真债务，清单见 _worklog_530.md §4）；T4 OBSERVATION-LIVENESS 存量 0 命中。block 仍为 0，非内容退化" --classify "ATOM-CLAIM-CONCEPT-NORMALIZED=real,INFERENCE-NOT-MACHINE-VERIFIED=legacy,EV-MATRIX-UNBACKED=real"
  ```
  （`--classify` 只是**本苦力的建议值，不是分类**——分类是人审动作，须人复核后自行签署，
  见 §6.2/§6.4。）

---

## 6. T5 warn 会计制度（2026-09-15）：停止"整体 accept" + 四桶盘点

### 6.1 改点（`tools/golden_lock.py`）

| 改点 | 内容 |
|---|---|
| `--accept` 强制分类 | 必须同时给 `--classify 规则ID=real\|false_positive\|legacy\|accepted[,...]`；**无分类 exit 2**，且**先验分类再测量**（0.2s 快速失败，不留痕、不动基线） |
| 四桶 | `real`（真债·须修内容）/ `false_positive`（规则过宽·须修规则）/ `legacy`（口径迁移期名单）/ `accepted`（明确认可的长期现状）；**未分类不是桶**——显式单独可见，不得并入任何桶 |
| 审计留痕 | `accepted[]` 每条带 `classify`（逐规则）；同时合并进快照 `warn_classify`，供下轮复算 |
| 新只读命令 | `buckets`（exit 恒 0：**盘点**不是门禁）；`check` 也恒打印四桶 + 逐规则明细 |
| 单次测量 | `measure(findings=None)`：`check` 只跑一次 gate，测指标与分桶**共用同一批命中** |
| 向后兼容 | 老 `golden_state.json` 无 `warn_classify` 键 → 全落未分类，不崩（pytest 钉死） |

### 6.2 验收（命令 / 退出码 / 输出）

```powershell
.venv\Scripts\python.exe tools/golden_lock.py buckets                       # 只读四桶
.venv\Scripts\python.exe tools/golden_lock.py check --accept "理由"           # → EXIT=2（拒绝）
.venv\Scripts\python.exe tools/golden_lock.py check --accept "理由" --classify "RID=real"   # 合法
```

| 验收项 | 实测 |
|---|---|
| 无 `--classify` | `EXIT=2`，**0.2s** 返回，`git status tools/golden_state.json` 空（基线分毫未动） |
| 非法分类（`RID=maybe`/缺 `=`/空串） | `EXIT=2`，无审计记录 |
| 真实 `check` | `恶化 1 · 改善 0`（`WORSE warn_findings: 59 → 136`）+ 四桶 `real 0 · false_positive 0 · legacy 0 · accepted 0 · 未分类 136` + 逐规则明细（9 行） |
| pytest | `tests/test_golden_classify.py` **9 passed**；`tests/test_s1_s6.py` **25 passed**（含 S4 两例 accept 用例同步为带分类） |
| 规范同步 | `docs/kernel/S1_S6_controls.md` §S4 三行（手段/判定/处置）写入四桶与强制分类 |

`buckets` 实测（136 warn 逐规则）：`ATOM-CLAIM-CONCEPT-NORMALIZED 77`、`INFERENCE-NOT-MACHINE-VERIFIED 28`、
`EV-MATRIX-UNBACKED 16`、`EV-OUT-UNDECLARED-KEY 6`、`EV-FALSIFICATION-QUANT 4`、
`ATOM-REL-TARGET 2`、`EV-ASSERT-SYMBOL-MAPPED 2`、`EV-SERVES-EXIST 1`。

### 6.3 一次性只读盘点：`EV-MATRIX-UNBACKED` 16 条（**不改卡、不 accept**）

判据（`check_evidence_matrix_backed`）：卡声明 ≥2 个编译器，但卡内可核对留痕
（`Examples|build/*.out` 路径 + `run #N`/10+ 位 run 号）**< 2** ⇒ warn。

**先给结论：16 条里没有一条有 CI/WSL 留痕。** 逐卡核实（`_t530_t5inv.py`，只读）：

| 卡 | 声明编译器 | 规则计留痕 | 核实到的"留痕" | 判读 |
|---|---|---|---|---|
| EV-CONC-001 | 3（MinGW 15.3 + WSL g++-14.2 + WSL g++-13.3） | 1 | `Examples/atoms/_atom_fence_vs_atomic.out`（**入库**、本夹具）；WSL 侧只有 `build/_conc_gpp14.s` / `build/_conc_gpp13.s` | A |
| EV-CONC-002 | 3（同上） | 1 | 同上（与 001 **共用同一处** .out，同夹具双卡） | A |
| EV-CONC-003 | 3 | 0 | 无（卡内只记 CI runner 上 `nproc` 读数） | B |
| EV-CONC-004 | 3 | 0 | 无（同上） | B |
| EV-CONC-005 | 3 | 0 | 无 | B |
| EV-CONC-006 | 3 | "1" | `0x555555559020` —— **ThreadSanitizer 报的访存地址**，被 `\d{10,}` 误判成 CI run 号（同一地址读/写两次，集合去重后仍计 1） | C（假锚） |
| EV-LANG-001 | 3 | "1" | `…46453925221103530…` —— **sha256 十六进制串里的连续 10 位数字**，被误判成 run 号 | C（假锚） |
| EV-LANG-002 | 3 | "1" | 同上 sha 片段 | C（假锚） |
| EV-MEM-001 | 3（15.3.0 / 13.1.0 / 8.1.0，**均为本地 MinGW，非 WSL**） | 0 | 无 | B |
| EV-MEM-039 | 3 | 1 | `Examples/atoms/_atom_allocator_bench.out`（入库、本夹具） | A |
| EV-MEM-040 | 3 | 0 | 无 | B |
| EV-MEM-041 | 3 | 0 | 无 | B |
| EV-MEM-042 | 3 | 1 | `Examples/atoms/_atom_leak_detection.out`（入库、本夹具） | A |
| EV-MEM-043 | 3 | 1 | 同上（与 042 **共用同一处**） | A |
| EV-MEM-044 | 3 | 0 | 无 | B |
| EV-MEM-045 | 3 | 1 | `Examples/atoms/_atom_false_sharing_perf.out`（入库、本夹具） | A |

**归口（本苦力建议，签署权在人）**：

- **A 类 6 卡**（CONC-001/002、MEM-039/042/043/045）：有 1 处**入库可复算**的同夹具 `.out`，
  但**仅 MinGW 单平台**；多平台（WSL g++-14.2/13.3）读数在卡里只是表格文字，物证
  `build/*.s` **被 `.gitignore:9` 忽略**（本地残渣、不可追溯）。⇒ 记
  **"待补外部留痕锚后转 `false_positive`"**：补 WSL/CI 侧的 `.out`（或可核对的 run 号）即可转正。
- **B 类 7 卡**（CONC-003/004/005、MEM-001、MEM-040/041/044）：**零留痕**，多平台结论纯靠文字。
  ⇒ 按提示词口径 **`real` 挂债**（补留痕锚）。
- **C 类 3 卡**（CONC-006、LANG-001/002）：名义"1 处留痕"经核实是**假锚**（TSan 地址 / sha 片段），
  真实留痕 **0**。⇒ 按"无留痕"处理 = **`real` 挂债**（并触发 §6.4 缺陷）。
- **严格按提示词字面**（"是否真有 CI/WSL 外部留痕"）：**16/16 皆无**（无 run 号域、`build/` 未入库、
  `ci.yml` 无 g++-14/13 的 fence 复算步）⇒ 若采用最严口径，应全部 `real` 挂债。两种口径的差
  仅在 A 类 6 卡（"有单平台留痕" vs "无外部平台留痕"），本苦力**不代人裁**。

### 6.4 ⚠️ 盘点副产物缺陷（P1，**本任务未修**，交人裁决）

`check_evidence_matrix_backed` 的"CI run 号裸写形态" `_run_no_re = \d{10,}` **无上下文约束**，
把**任意 10 位以上数字**都算留痕，实测误收三类：

| 形态 | 卡 | 实际身份 |
|---|---|---|
| `0x555555559020` | EV-CONC-006 | TSan 访存地址（十六进制，非 run 号） |
| `…46453925221103530…` | EV-LANG-001/002 | sha256 串里的数字片段 |
| `1073741824` / `2147483648` | EV-UB-002 | 数值常量 2^30 / 2^31 |

**危害**：单张卡凑够**两处**假锚（如两个不同 TSan 地址、两个 sha 片段）即被判"留痕 ≥2 ⇒ 已撑起"
⇒ **多编译器声明恒绿**（373-N3"删命令锚"同型病根；该规则当年正是为此删掉了 g++ 命令行锚）。
**当前无实际漏网**：EV-UB-002 只声明 1 个编译器（`compiler: [GCC 15.3.0]`，`len(comps) > 1` 才判）
⇒ 规则跳过它；其余假锚卡各自只有 1 处 ⇒ 仍落 warn（仅计数被抬高 1）。
**为何本任务不改**：改 gate 规则口径须配 poison 端到端毒样例（护栏 3）+ 全量 pytest + 独立 commit，
**不属 T5（golden_lock 会计）范围**；且本批护栏 5 要求"存量紧缩走 warn 观察期、不新增 block"。
**建议修法（供人开独立小任务）**：把裸写数字收窄为**带 run 语境的形态**（如
`run\s*#?\s*\d{7,}` / `actions/runs/\d+` 前缀），并补 P69 毒样例（假锚卡不得恒绿）。

### 6.5 INFERENCE 卡级 warn = "命题签署回填"债务单（28 条 / 26 卡）

`INFERENCE-NOT-MACHINE-VERIFIED` 的**卡级兜底** warn（528 任务3 的精度设计：命题级 `signed_by`
放行、卡级人签兜底），逐卡：

`ATOM-CONC-FENCE-001×2`、`ATOM-CONC-LOCK-001×2`、`ATOM-CONC-RACE-001×2`、`ATOM-HIST-AUTOPTR-001×2`、
`ATOM-LANG-INLINE-001×2`、`ATOM-MEM-ALIGN-001×2`、`ATOM-MEM-ALLOC-001×2`、`ATOM-MEM-ALLOC-002×2`、
`ATOM-MEM-LEAK-001×2`、`ATOM-MEM-LEAK-002×2`、`ATOM-MEM-MOVE-002×2`、`ATOM-MEM-NEW-001×2`、
`ATOM-MEM-PERF-001×2`、`ATOM-MEM-PERF-002×2`、`ATOM-MEM-PERF-003×1`、`ATOM-MEM-PERF-004×2`、
`ATOM-MEM-RAII-001×2`、`ATOM-MEM-RAII-002×2`、`ATOM-MEM-RVREF-001×2`、`ATOM-MEM-SHARED-001×2`、
`ATOM-MEM-SHARED-002×2`、`ATOM-MEM-UNIQUE-001×2`、`ATOM-MEM-UNIQUE-002×2`、`ATOM-MEM-VALUE-001×2`、
`ATOM-MEM-VALUE-002×2`、`ATOM-MEM-WEAK-001×2`、`ATOM-UB-GRAY-001×2`（PERF-003 为 ×1；合计 28）

> **性质**：**不是误报，也不是内容退化**——是 526/528 把 inference 命题"命题化 + 逐条签署"这件事
> 做到一半的**中间态**：这些卡已有 `claim_structured`，但**卡级**仍缺人级签署。
> **归口建议 `legacy`**（口径迁移期名单），清零动作 = 逐条命题补 `signed_by`（人级名册
> `HUMAN_PRINCIPALS`），**不是** `--accept` 一下了事（accept 只冻结现状、不推进签署）。
> 与 §4 的 77 条 `ATOM-CLAIM-CONCEPT-NORMALIZED` 同源（同一批 527/528 回填卡），**两笔债应合批清**。

### 6.6 测试与覆盖

- `tests/test_golden_classify.py`（新，fast）：9 例 —— 无分类拒绝且**基线未动**（参数化 5 种非法形态）/
  合法分类留痕（`accepted[].classify` + `warn_classify`）/ 四桶复算（未分类不得并入任何桶）/
  老快照无 `warn_classify` 不崩。**隔离纪律**：`gl.STATE` 一律指向 tmp，绝不碰真实黄金基线。
- `tests/test_s1_s6.py`：S4 两例 accept 用例同步为"带 `--classify`"，并适配 `measure(findings)`
  新签名（5 处零参替身 → 收参替身）。
- 规范件：`docs/kernel/S1_S6_controls.md` §S4。
- `tools/.tool_checksums` **不含** `golden_lock.py` ⇒ 本任务无需 `tool_integrity --update`。

**CI ruff 硬门禁（钉定 0.6.9）归属核对**：`uv tool run --from ruff==0.6.9 ruff check tools/` 得 **15 项**
（注：本地 `ruff 0.16.5` 因规则集/默认值漂移会虚增到 803 项，**不可用于判 CI 口径**）。逐项核归属：

| 归属 | 项数 | 明细与依据 |
|---|---|---|
| 本任务新增/改动文件 | **0** | `tools/golden_lock.py` + `tests/test_golden_classify.py` → `All checks passed!` |
| 本批改过的文件内 | 4 | `gate_engine.py:2076 F541` / `:3100 E741`、`poison_drill.py:1193 E741` / `:1806 E401`；对 `1b0232d`（528 收工）同文件复跑（`git show 1b0232d:tools/…` 落盘后过 ruff）得**同规则、同代码行** 4 项（仅行号平移 1970/2882/1193/1723）⇒ **存量** |
| 本批未改文件 | 11 | `artifact_version_stamp.py` F401、`backup.py` F401、`book_atom_sync.py` F541×3、`cost_tracker.py` E731+F841、`env_check.py` E401+E741×2、`metrics_collector.py` F401 |

结论：**15/15 皆为 528 起的存量技术债，T3/T4/T5 未引入新 ruff 错误**；按本批护栏不扩范围，
清债另开独立小任务（其中 9 项 `--fix` 可自动修）。

### 6.7 golden_lock 漂移（**仍留红，未 accept**）

`warn 59 → 136` 的漂移与 T5 无关（T5 只改会计制度、不改任何规则），仍按铁律留红作人审信号；
`tests/test_json_output.py::test_golden_lock_json`（slow）保持红——**这是 T5 的输出之一**
（四桶里 136 条全为"未分类"，正是要把这笔账摆到人面前）。`-m fast` 阶段不受影响。

### 6.8 ⚠️ 副产物发现：CI 的 ruff **硬门禁当前为红**（15 项存量债），本地无任何门禁覆盖

T5 为判定"15 项 ruff 是否本批引入"而顺带查出的**跨批真实缺口**（诚实记录，**本任务未修**）：

| 事实 | 证据 |
|---|---|
| CI ruff 是**硬门禁** | `.github/workflows/ci.yml:37-46`：`ruff==0.6.9` 钉版本 + `ruff check tools/` + `continue-on-error: false` |
| 该硬门禁**当前失败** | `uv tool run --from ruff==0.6.9 ruff check tools/` → **15 项 / EXIT=1** |
| 债务是**累积**的（非 T5 引入） | 见 §6.6 归属表：本任务文件 0 项、本批改过的文件 4 项同为 `1b0232d` 存量、其余 11 项文件本批未改 |
| 本地**无**门禁覆盖它 | `tools/prepush_check.py:41-50` 的 `CORE` 七项（quality/consistency/metrics/compile_gate/exempt_audit/expected/star_h2）**不含 ruff**；其 docstring 自称"复用 CI 的「快」校验" ⇒ **声明与实现不一致** |
| 另有一处**版本踩空** | `tools/handover_check.py:104-113` 有 ruff 检查但**优先 `shutil.which("ruff")`**（本地 0.16.5 → 803 项虚警），只在无 PATH ruff 时才回退 `uvx ruff==0.6.9`；与 CI 已钉版本的口径冲突 |
| 为何一直没爆 | 401→530 **全部未 push**（沙箱 `git push` exit 141）⇒ CI 从未真正跑过；一旦 push，**第一个 ruff job 立即红**，与 §6.7 的 golden 红叠加 |

**为何本任务不修**：①不属 T5（T5 只改 `golden_lock.py` 会计制度）范围；②护栏 7 要求一任务一 commit、
不在本任务夹带；③`ci.yml` 注释载明上轮清债是"逐个确认语义后手改、未用 `--unsafe-fixes` 批量糊"，
15 项中 6 项（E741×3 / E731 / F841 / E741）需逐个判语义，是需独立评审的小任务。

**建议修法（供人开独立小任务，防"push 后 CI 双红"）**：
1. 清 15 项（9 项 `--fix` 安全自动修；6 项手改并逐个在 PR 说明语义）；
2. 把 ruff 补进 `prepush_check.py` 的 `CORE`，**并钉 0.6.9**（与 `.pre-commit-config.yaml` / `ci.yml` 同版本），
   否则用 PATH 的 0.16.5 会 803 项假红；
3. 修 `handover_check.check_ruff()` 的"PATH 优先"逻辑 → 一律走钉版本（与 CI 单一口径）。

---

## 7. T7 task_queue.py · L2 调度最小骨架（2026-09-15，commit=`d976170`）

### 7.1 交付物（新文件，零新依赖：标准库 sqlite3）

| 项 | 内容 |
|---|---|
| `tools/task_queue.py` | 表结构按规格钉定（id/type/payload_ref/status/priority/deps/claimed_*/attempts/result_ref/error/created_at/updated_at），**不加列**；子命令 `init/enqueue/claim/next/heartbeat/done/fail/blocked/list` |
| `tests/test_task_queue.py` | **8 例**（规格验收 6 条 + 空队列/只读 next/优先级方向/CLI 契约），全绿 |
| `.gitignore` | **无需改**：`/data/tasks/` 早在 `.gitignore:76`；`git check-ignore -v data/tasks/queue.db` 实测命中 |
| 不入 `.tool_checksums` | task_queue 非 replay/gate 链核心工具，无需 `tool_integrity --update`（实测 5 文件表未动） |

### 7.2 关键设计（与 task_state 的分工勿混）

- **分工**：`task_state.py` = 长任务进度笔记本（任务内部走到哪）；`task_queue.py` = 队列（谁该干什么/干完没）。
  v1 由人执行 `task_queue next` 手动派活，**不写自动 Supervisor Loop**（无数据支撑自动路由，529 P2）。
- **幂等键**：`id = "<type>-<sha256(payload_ref)[:12]>"`（可 `--id` 覆盖）；重复 enqueue 打印"已存在"并 exit 0。
- **并发安全**：`BEGIN IMMEDIATE` 原子事务 + WAL + busy_timeout；选中后 `UPDATE ... WHERE status='queued'` 双保险。
- **认领者绑定**：`heartbeat/done/fail/blocked` 必须本人（`claimed_by` 一致）且状态 claimed，否则 exit 1——"谁干的谁签收"单点。
- **stale 接管**：heartbeat 超 600s ⇒ 下次 claim 回收回 queued（attempts 保留）；attempts>3 自动 blocked。
- **deps 门**：deps 全 done 才可 claim；坏 deps JSON 视为未满足（fail-closed）；enqueue 时 dep 不存在 ⇒ stderr 可见提示。
- **实施中固化的两个坑**（均有回归锁）：①`SystemExit` 落进 `except BaseException: ROLLBACK` 会二次抛
  "no transaction is active" 盖掉真报错 ⇒ `_rollback()` 容错回滚；②`--json/--db` 只挂主解析器时
  后置形态 unrecognized（T6 同款坑）⇒ 挂到各子命令且 `default=SUPPRESS`。

### 7.3 验收实测（护栏 6：全部本机重测，非照抄草稿）

| 验收项 | 实测 |
|---|---|
| ①enqueue 幂等（含显式 --id） | `test_enqueue_is_idempotent` ✅；CLI 两次 enqueue 第二次"已存在"exit 0 |
| ②两连接争抢同一行 | 两线程 Barrier 同抢，**只 1 个 claim 成功**且 attempts==1 ✅ |
| ③deps 未完成不可 claim | 高优先级也压不住依赖；`next` 报 `blocked_by_deps`；dep 不存在⇒永不满足 ✅ |
| ④非 claim 者 done 被拒 | exit 1、状态零变化、result_ref 写不进；终态后连本人也被拒 ✅ |
| ⑤heartbeat 超时可接管 | attempts 保留累加（1→2）、原主失权（done 被拒）✅ |
| ⑥attempts>3 进 blocked | 第 5 次 claim 不发活、error 含 MAX_ATTEMPTS、attempts==4 可追溯 ✅ |
| 空队列 `list`/`next` 不崩 | `0 条` / `无可派任务`，exit 0 ✅ |
| ruff 0.6.9（CI 口径） | 两文件 `All checks passed!` ✅ |
| 全量 fast pytest | **185 passed**（点数实测，无 fail/skip 异常；其中 T7 `test_task_queue.py` 贡献 8 例；较 T6 收工 168 的 +17 中另 9 例为 T5 `test_golden_classify.py` 纳入统计的时点差） |

---

## 8. 收工全量门禁（fresh run，2026-09-15，HEAD=`d976170`，串行执行）

| 门禁 | 实测 | 判定 |
|---|---|---|
| `gate_engine.py --check` | `[gate] 规则 60 条 · 命中 141 (block=0 warn=136 advice=5)`，exit 0 | ✅（与 T5 收工一致，T6/T7 未动任何规则） |
| `golden_lock.py buckets` | `real 0 · false_positive 0 · legacy 0 · accepted 0 · 未分类 136`（逐规则：CONCEPT-NORMALIZED 77 / INFERENCE 28 / EV-MATRIX 16 / EV-OUT 6 / FALSIFICATION 4 / REL-TARGET 2 / ASSERT-SYMBOL 2 / SERVES 1） | ⚠ 136 条全未分类＝**等人审 `--accept --classify`**（§6.7 留红纪律不变） |
| `poison_drill.py` | **90/90**；RULE-COVERAGE **35/60**（豁免 27）；**零覆盖攻击面：无**；exit 0 | ✅ |
| `atom_evidence_replay.py --check --no-sanitizer` | **confirm=56 / refute=0 / infra_error=0**；artifact_sha 与独立重编译复现均一致 | ✅ |
| `pytest -m "not slow"` | **185 passed**（无 fail/skip 异常；含 T7 新 8 例） | ✅ |
| `knowledge_graph.py build` | 325 节点（RULE=60）/ 291 边；CONTRASTS=22 / CONTRADICTS=1；未知关系名 1 条已归 REFERENCES | ✅ |
| `kg stats` | 概念连通：跨原子概念 0 / 最大连通分量 3（与 T3 首跑口径一致，回填 backlog 未动） | ✅（字段在） |
| `kg conflicts` | **候选矛盾 1 组**（ATOM-MEM-MOVE-002 × ATOM-MEM-PERF-001，仅声明边、无极性相反，语义裁决归人） | ✅（较开工 19 → 1） |
| `task_queue.py list` | `0 条`，exit 0（空队列不崩） | ✅ |
| `git status --porcelain -- Examples/atoms/ atoms/ evidence/ tools/golden_state.json` | **空**（受控目录干净） | ✅ |
| `consistency_check.py` | 147 章 ERROR=0 WARN=0，评分 100/100 | ✅ |
| `gen_metrics.py --check` | 全部文档数字与事实源一致 | ✅ |

### 8.1 未做 / 留给人的（诚实清单）

1. **golden_lock 136 条未分类 warn**：`--accept --classify` 是人审动作，命令形态见 §5.4（含本苦力的建议分类值）。
2. **§6.8 CI ruff 硬门禁 15 项存量债**：未修（不属 T7；防 push 后 CI 双红，修法见 §6.8）。
3. **§6.4 假锚缺陷（`_run_no_re=\d{10,}`）**：未修，建议独立小任务（收窄 run 号语境 + P69 毒样例）。
4. **§4 的 79 条 object 非概念名**：内容债，未改任何 atom 文件（T3 处置建议待人裁）。
5. T7 未接 `cppbible.py` 转发子命令（规格未要求；`task_queue` 独立 CLI 即可，v1 人手动派活）。

### 8.2 本批 commit 链（T1–T7，全部未 push）

`5eabcf4`(T1) → `a36d71d`(T1 基线) → `3616799`(T2) → `9942d8c`(T3) → `2c19aaf`(T4) → `da85a2e`(T5) → `f3025b4`(T6) → `d976170`(T7)

---
