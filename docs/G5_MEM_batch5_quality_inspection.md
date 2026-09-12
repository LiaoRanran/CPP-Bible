# G5 MEM 第五批质检报告（ALLOC-002 / LEAK-002 / PERF-004）

> 2026-09-12 · 本批 3 颗原子、6 张证据卡、3 条误解、4 个夹具。门禁全绿（replay 双平台 48/48、gate block=0、poison 8/8）。本报告聚焦三个方向性案例——它们是本批最有价值的方法论沉淀。

---

## 一、批次概览

| 原子 | type | claim 核心 | 证据卡 | 误解 | 红队 |
|---|---|---|---|---|---|
| ALLOC-002 | mechanism | 元数据开销与是否支持单块释放绑定：arena 32B ≪ bitmap 181B ≪ pool 8056B（统一口径） | EV-MEM-040/041 | MIS-MEM-030 | 1 阻断 / 6 高 / 4 建议 |
| LEAK-002 | contrast | 泄漏检测工具的报告与否高度依赖被测代码形态：同一真泄漏夹具，加一个无关 volatile 计数器即从零报告翻转为报告 64B/2 allocs | EV-MEM-042/043 | MIS-MEM-031 | 2 阻断 / 7 高 / 6 建议 |
| PERF-004 | pitfall | 多线程"独立变量"因共享缓存行可慢约一个数量级（实测 8.78×）；结构前提可用地址确定性判定；padding 有空间代价（16×） | EV-MEM-044/045 | MIS-MEM-032 | 3 阻断 / 15 高 / 8 建议 |

**门禁自证**：
- replay Windows 6/6 + WSL 48/48 confirm
- gate block=0 · 33 规则 · warn=9（全预期债）
- poison 8/8 · pytest 84 passed
- golden_lock 基线 sync {atoms:20, evidence:48, verified:20, replay:48}
- WSL ci_local_precheck 31 步全过

---

## 二、三个方向性案例（本批核心价值）

### 案例 1：ALLOC-002 —— 口径不统一导致结论方向反转

**问题**：初版夹具的三个分配器用了三种不同的"元数据"定义：
- `Arena::meta()` 只算 `sizeof(size_t)`（连 buf 向量头都不算）
- `Pool::meta()` 只算 `sizeof(free_list)+8`（漏掉 free-list 堆数组 1024×8 = 8192 B）
- `Bitmap::meta()` 含数据结构本体

**后果**：卡内 claim 写成"pool 元数据 32 B、最省"，并断言"线性增长是 bitmap 与 pool 的关键差异"——双双失真。"元数据换灵活性"的教学结论被指到了相反方向。

**红队发现方式**：两段式盲读（P1-1 纪律生效）——红队不读卡的自述，直接读夹具源码和工件，发现 `Pool` 构造函数里 `free_list = new void*[num_blocks]` 分配了 8000 B 堆数组，而 `meta()` 完全没算它。

**修复**：统一口径为"元数据 = 分配器自身占用且不承载用户数据的全部字节"，拆为 `struct_bytes + bookkeeping_bytes` 两栏逐项列出。夹具 v3 数据最终化（sha 4f482fdc…）：

| 策略 | struct | bookkeeping (n=1000) | total (n=1000) | total (n=8000) |
|---|---|---|---|---|
| arena | 32 | 0 | **32** | **32**（活性对照：不随规模变） |
| bitmap | 56 | 125（1 bit/块） | **181** | **1056** |
| pool | 56 | 8000（8 B/块指针） | **8056** | **64056** |

**方向反转**：pool 从"最省 32 B"变为"最贵 8056 B"（比 bitmap 大 44 倍）；pool 与 bitmap 的元数据都随块数增长（7.95× 与 5.83× @8× 规模），"线性增长是关键差异"被证伪。

**方法论沉淀**：
- 同一实验中的多个对象必须用同一口径测量，否则比较无意义
- 红队两段式盲读（先读夹具/工件，再读卡）能抓出"卡自述与源码不符"的问题
- 活性对照（arena 32→32 不变 vs pool/bitmap 随规模变）证明读数是算出来的，不是写死的常量

---

### 案例 2：LEAK-002 —— 无关改动翻转工具结论

**问题**：初版 claim 是"真泄漏 + LSan 零报告"，以此证明"没报≠没泄漏"。

**红队发现**：
1. 夹具的 `cycle_is_leak` 与 `cycle_dtor_count` 是同一位（`sete dl`）——一 bit 两计，对"泄漏"零判别力
2. `run_cycle` 内无活性对照，而同一工件已证编译器会消除不可观测构造（Scoped 构造被整体消除）——"dtor=0"无法区分"泄漏"与"分配被消除"

**修复动作**：给 Node 加 `volatile` 构造计数（证明分配真发生），删除同源派生的 `cycle_is_leak`，改为三条不同源指标（`cycle_allocated=2` / `cycle_destroyed=0` / `cycle_live_objects=2`）。

**意外反转**：加了这个与泄漏无关的 `volatile` 计数器后，LSan 从"零报告"变为"报告 64 byte(s) leaked in 2 allocation(s)"（stderr 从 0 字节变为 1258 字节）。

| 版本 | 夹具差异 | stderr | LSan 结论 |
|---|---|---|---|
| 改前 | 无构造计数 | 0 字节 | 零报告 |
| 改后 | 加 volatile g_cycle_ctor | 1258 字节 | 64 B leaked in 2 allocs |

唯一变量 = 一个与泄漏无关的计数器；且报告数值自洽（64 B = 2 × 32 B，与 .asm 的 Node 尺寸一致）——证明它本来就是真泄漏，先前"零报告"是工具没看到。

**比原结论更强**：不是"LSan 有结构性漏报"，而是"泄漏检测工具的报告与否高度依赖被测代码的具体形态"——连"加一个计数器"这种与泄漏无关的改动都能翻转结论。这与 LEAK-001 的"优化档/存活位置敏感"同族，但新增了一条更细的证据。

**方法论沉淀**：
- "先证分配真发生"这个验证要求本身产出了更强的对照实验（红队 H2 的价值不只是"找对了错"）
- 错误预测命中率 = "哪条假设的验证动作产出了新证据"，不是"猜中比例"
- 工具报告是补充证据，零依赖观测（构造/析构计数、存活对象数）才是定性判据

---

### 案例 3：EV-MEM-040/041 —— 跨编译器断言未在 Linux 工件实测

**问题**：证据卡的 `artifact_assert` 写的是 `arena_n1_meta_total_bytes=`（具体标签），但夹具用 `report(tag, …)` 函数，标签是运行时拼接的，工件里只有格式串模板 `%s_meta_total_bytes=`。

**为什么 Windows 侧没发现**：编译器匹配 ⇒ 走 `artifact_sha256` 强校验，根本不检查 `artifact_assert` ⇒ 断言里的错字面量被静默跳过。

**暴露时机**：WSL 全量 replay（跨编译器路径）才 refute:artifact_assert_failed——因为 Linux 侧编译器不同，不走 sha 路径，必须检查 artifact_assert。

**修复**：断言改为 `contains_any: ["%s_meta_total_bytes=", "%s_meta_bookkeeping_bytes="]`（格式串模板），两平台 2/2 confirm。

**方法论沉淀**：
- 断言候选必须在 Linux 工件中 grep 验证（Windows 的 sha 路径覆盖不到 artifact_assert）
- 这条已升级为 298 第六批提示词的环节 3 自检项："actual 中的每个标签在 Linux .asm 中 grep 得到？"
- 与 EV-MEM-038 的 `heap_at_len%zu=` 教训同类复发——说明需要机械检查项，不能靠记忆

---

## 三、红队拦截统计

| 原子 | 阻断 | 高级 | 建议 | 最有价值拦截 |
|---|---|---|---|---|
| ALLOC-002 | 1 | 6 | 4 | 元数据口径不统一（方向反转级） |
| LEAK-002 | 2 | 7 | 6 | 一 bit 两计 + 消除与失败不可区分 |
| PERF-004 | 3 | 15 | 8 | padded_shares_line 恒真 0 / self_same_line 自比 / 空间翻倍矛盾 |

**红队质量趋势**：第三批抓"断言自证"（机械可查的形式问题）→ 第五批抓"口径不统一导致方向反转"（语义级问题）。浅层问题已被 P4–P7 规则固化拦住，红队被迫往更深的地方挖。

**P1-1 两段式盲读生效**：ALLOC-002 的口径问题是红队不读卡自述、直接读夹具源码发现的——如果先读卡，会被"pool 元数据 32 B"的自述带偏。

---

## 四、PERF-004 倍数波动实证

修复红队阻断（padded_shares_line 恒真 0）后重跑，倍数从 18.86× 变成 8.78×（同机、同夹具、只改了断言行）——这不是 bug，而是**"不锚倍数"的直接实证**：同一台机器跨运行就能波动 2×+。

已写进 EV-MEM-045，让"锚方向不锚倍数"从"纪律"变成"被数据逼出来的结论"。

---

## 五、人审问题（每颗 2-3 点）

### ALLOC-002（DAL B——教学结论方向，需人审）
1. claim 的"arena ≪ bitmap ≪ pool"排序是否足够直观？是否需要在正文开头加一个"直觉 vs 实测"对照框？
2. "元数据换灵活性"这个教学主线是否清晰？arena 用放弃单块释放换零 bookkeeping，这个 trade-off 是否需要更多篇幅？
3. 与 ALLOC-001（pmr 分配器）的 relations 是否足够？是否需要在正文中明确串联？

### LEAK-002（DAL C——红队通过即可，抽查 20%）
1. "三层信号分级"（退出码/stderr → 内置观测 → sanitizer 报告）是否需要画一个决策流程图？
2. 与 LEAK-001 的增量对照表是否足够区分两者？（LEAK-001 是优化档/存活位置，LEAK-002 是无关代码改动）

### PERF-004（DAL C——红队通过即可，抽查 20%）
1. 断言锚只锚"方向"（sharing_is_slower=1）不锚倍数，是否需要补一个"量级档位"字段（如 >=5x）？
2. `hardware_destructive_interference_size` 是提示值，是否应在原子内补"回退与实测确认"一节？
3. 与 PERF-001（移动性能）/ PERF-003（分配策略性能）的 relations 是否合适？

---

## 六、待办与遗留

- [ ] 三颗原子化（git mv → frontmatter 签署 → golden_lock sync → 门禁复跑 → commit + push）
- [ ] ALLOC-002 DAL B 需人审签署；LEAK-002/PERF-004 DAL C 红队通过即可（按 G6 四级状态体系）
- [ ] G6 工具改动（gate_engine/golden_lock/poison_drill）单独提交
- [ ] S6 工具债 P4–P7 盲区收紧（EV-MATRIX-UNBACKED 豁免过宽，需带可核对锚）
- [ ] 第六批方向：A（MEM 收尾 ALLOC-003/PERF-005/VALUE-003）或 B（转 CONC 域）

---

*本报告是第五批的方法论沉淀。三个案例（口径不统一 / 无关改动翻转结论 / 跨编译器断言未实测）均已写入 288 第六批提示词的纪律检查项，确保下批不会重犯。*
