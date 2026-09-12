# 327_第六批CONC域收口与工具链优化_综合执行提示词

> 2026-09-12 · 三线并行 · 覆盖 CONC-002/003 生产 + ccache 优化 + 工具提交 + 文档入库
> 前置：CONC-001（ATOM-CONC-FENCE-001）已 verified 入库（10b9d05 + 85978cc）

---

## 〇、全局约束（所有线必须遵守）

### 0.1 铁律（违反即阻断）
1. **不原子化未过红队的草稿**：草稿在 goldens/conc/，红队通过后才移 atoms/conc/
2. **不提交未过门禁的产物**：gate block=0 + replay confirm + poison 全过才提交
3. **不混提交**：工具改动、原子产物、References 文档分别提交
4. **不编造数据**：所有数字来自实测，未采集的如实标注
5. **断言锚只锚常量+活性对照**：性能数据不入 actual，放 .out
6. **断言候选必须在 Linux 工件中 grep 验证**（Windows sha 路径覆盖不到 artifact_assert）
7. **有界循环**：任何自旋/循环必须有终止条件，防止 replay 超时 600s
8. **夹具不重载 operator new/delete**（避 P4 自证断言）

### 0.2 frontmatter 完整模板（不是简化版！）
```yaml
id: ATOM-CONC-{TOPIC}-{NNN}        # 必须含 TOPIC 段，如 ATOM-CONC-LOCK-001
domain: conc
type: mechanism|pitfall|contrast|tool   # 10 类之一，无 perf/concurrency
status: draft
dal: A|B|C|D|E
human_review: required|optional|exempt   # DAL A/B 必须 required
status_history:
  - {level: draft, at: "YYYY-MM-DD", by: machine:writer}
audience: beginner|intermediate|advanced
cognitive_load: low|medium|high
claim: >-
  {单句可证伪，≤50字}
claim_boundary:
  standard: [C++11, ...]
  compilers: [GCC 15.3.0 (MinGW-w64), ...]
  opt: [-O2]
  platform: [x86-64]
relations: []
evidence: [EV-CONC-XXX, EV-CONC-YYY]
sources: [...]
first_hand: true
pedagogy:
  motivation: "..."
  misconception:
    - {level: surface|deep, text: "...", refutations: [EV-CONC-XXX]}
  socratic: "..."
  predict_first: "..."
  misconceptions: [MIS-CONC-XXX]
misconceptions: [MIS-CONC-XXX]
```

### 0.3 证据卡必填字段（EV_REQUIRED，缺一即 block）
fixture / command / artifact / artifact_sha256 / artifact_compiler / actual / expected / falsification / matrix / controlled_vars

### 0.4 环境事实
- Windows g++ = `C:\Qt\Tools\mingw1530_64\bin\g++.exe`（15.3.0）
- WSL g++-13.3 / g++-14.2；riscv64-unknown-elf-g++ 13.2（bare-metal，无 <atomic>，用 __atomic_* 内建）
- TSan 仅 WSL/Linux 可用，**必须 `setarch -R` 前缀**（否则 FATAL: unexpected memory mapping）
- MinGW 无 TSan（cannot find -ltsan）
- Windows replay 与 WSL ci_local_precheck **禁止并行**（同写 Examples/*.asm 出假 refute）
- golden_lock.py 命令：{sync, check, show}，**无 --accept**
- gate_engine.py 规则数以 `--list` 实跑为准

---

## 一、线 A（已完成，仅作参考）

CONC-001 已收口：atoms/conc/ATOM-CONC-FENCE-001.md（verified，人签）
- 夹具：Examples/atoms/_atom_fence_vs_atomic.cpp（sha 8dd19bc6…）
- 证据卡：EV-CONC-001（12 条断言）+ EV-CONC-002（9 条断言）
- 红队：阻断 0 / 高级 1 / 建议 3，全部处置
- 提交：10b9d05 + 85978cc

**关键教训（后续批次避雷）**：
- 320 给的 frontmatter 模板是简化版，gate 真实要求 ATOM_REQUIRED 全字段
- ID 须 ATOM-{DOMAIN}-{TOPIC}-{NNN}（ATOM-CONC-001 缺 TOPIC → 改 ATOM-CONC-FENCE-001）
- 文件名以实际文件为准（_atom_conc_fence.* 过时，实际是 _atom_fence_vs_atomic.*）

---

## 二、线 B：CONC-002（锁代价）+ CONC-003（数据竞争 UB）生产

### 2.1 CONC-002 · 锁的代价与无锁的代价

**主题**：mutex 与原子操作的性能代价分层，以及"无锁不一定更快"

**claim 方向（需实测验证后收窄）**：
- 无竞争 mutex fast path ≈ 30-60ns（仅作参考数据，不入 claim）
- 有竞争 mutex：1-10μs（阻塞唤醒 10-100μs）
- 原子 RMW（fetch_add）：无竞争 ~10ns，高竞争可退化到 >1μs
- CAS 在高竞争下可能比 mutex 慢（CAS 重试风暴）

**夹具设计要求**：
1. **双构建同源宏门控**：`-DBENCH_FULL` 只给 .out 生成用，actual.run_* 只放方向量与常量
   - 原因：逐轮纳秒会进入 run_match 逐字比对，使卡任何机器上必然 refute（EV-MEM-045 教训）
2. **唯一变量**：同步原语种类（mutex / atomic fetch_add / atomic CAS）
3. **活性对照**：单线程无同步基线
4. **反例对照**：CAS 在高竞争下退化（cas_4thread_degrades）
5. **核数检查**：夹具先打印 nproc，断言用 `contains_any: ["cas_4thread_degrades=1", "insufficient_cores=1"]`
   - 原因：≤2 核环境 cas_4thread_degrades 会合法翻转为 0
6. **性能数据锚方向不锚倍数**：同机跨运行可波动 2x+（PERF-003 教训：18.86×→8.78×）
7. **Windows/MinGW 的 -pthread**：可用，但 TSan 不可用（性能与 sanitizer 列不能混谈）

**证据卡（2 张）**：
- EV-CONC-003（判据卡）：方向量断言（mutex_fastpath_exists=1, atomic_rmw_exists=1, cas_retry_observed=1）
- EV-CONC-004（性能卡）：完整 7 轮逐样本 + min/max + 比值，双平台（Windows + WSL）
  - .out 含完整复跑命令 + 逐轮数据
  - actual 只锚方向（sharing_is_slower=1 类），不锚倍数

**误解**：MIS-CONC-002（"无锁一定比有锁快"）

**红队重点**：
- 断言是否覆盖 claim 全部范围？
- 对照组是否真的只有一个变量？
- 性能数据是否误入 actual？
- cas_4thread_degrades 在低核环境的处理？

### 2.2 CONC-003 · 数据竞争的 UB 与工具检测

**主题**：数据竞争是 UB（不是"可能出错"，而是"程序无意义"），TSan 可以检测但有开销

**claim 方向（需实测验证后收窄）**：
- 数据竞争 = 未同步的并发写 + 读/写 = UB（C++ [intro.races]）
- UB 的后果：编译器可以假设不发生，从而做激进优化（消除/重排）
- TSan 可以检测数据竞争，开销 5-15x 慢、5-10x 内存，几乎零误报

**夹具设计要求**：
1. **有界循环**：数据竞争演示必须有界，防止 replay 超时
2. **双工件落卡**：-O2 作 artifact（展示编译器优化消除），-O0 只在正文留痕
   - 原因：全库 48 张卡都是单 artifact，零 artifacts 复数先例
3. **TSan 列**：仅 WSL/CI，命令必须 `setarch -R g++ -fsanitize=thread`
   - Windows 侧只出 .asm，不跑 TSan
4. **sanitizer 判定**：按类型归并（[thread]），别按子串（LeakSanitizer 复用 SUMMARY 的坑已在案）
5. **expected_sanitizer**：含真数据竞争演示的卡必须声明 `expected_sanitizer: [thread]`
   - 否则 replay sanitizer 步报 data race 会判 refute

**证据卡（2 张）**：
- EV-CONC-005（UB 卡）：-O2 工件中数据竞争访问被优化/消除的符号证据
- EV-CONC-006（TSan 卡）：WSL setarch -R 下 TSan 报告的完整 stderr 留痕
  - .out 含完整命令行 + stdout + stderr 原文 + 字节数 + grep -c -i "data race"

**误解**：MIS-CONC-003（"数据竞争只是偶尔读到旧值，不是大问题"）

**红队重点**：
- 夹具是否有界？（无限循环→600s→rc=124→refute）
- TSan 命令是否有 setarch -R 前缀？
- expected_sanitizer 是否声明？
- -O0 工件是否只在正文留痕（不入 artifact_assert）？
- 描述是否写"消除或提升（以工件为准）"，不写死"缓存在寄存器"？

### 2.3 线 B 执行顺序
1. CONC-002 夹具 → 双平台实测 → 2 卡 → 红队 → 修复 → 草稿
2. CONC-003 夹具 → 双平台实测（含 WSL TSan）→ 2 卡 → 红队 → 修复 → 草稿
3. 全批门禁（replay/gate/poison/pytest/golden_lock/WSL 预检）
4. 原子化（人审签署后）→ 提交

---

## 三、线 C：ccache + WSL /tmp 工具链优化

### 3.1 ccache 安装（需用户授权后执行）
- WSL：`sudo apt-get install ccache`
- Windows：下载 ccache 二进制（https://ccache.dev/download.html）或 `winget install ccache`
- 验证：`ccache --version`

### 3.2 配置
- WSL：`export CCACHE_DIR=/tmp/ccache`，`export CC="ccache g++"`
- Windows：设置 CCACHE_DIR 环境变量
- 配置 ccache.conf：`max_size = 5G`，`sloppiness = include_file_mtime`

### 3.3 replay 工具改造
- 修改 tools/atom_evidence_replay.py：编译命令前缀加 `ccache`
- WSL 构建目录改 `/tmp/cppbible_build/`（避免 /mnt/c 慢 15-20x）
- 实测：replay 编译从 2min → 5s（24x 预期）

### 3.4 验证
- 清空 ccache 缓存后首次编译（冷启动）
- 二次编译（命中缓存）
- 对比耗时，写入 docs/kernel/工具链性能基准.md

---

## 四、线 D：工具改动分离提交

### 4.1 已修改未提交的工具文件
- `tools/atom_evidence_replay.py`：三分类（confirm/refute/infra_error）+ run_match_file 支持 + compiler_missing 前置检查
- `tests/test_atom_evidence_replay.py`：回归测试
- `tools/golden_state.json`：golden_lock 基线

### 4.2 提交要求
- 单独提交，不混原子产物
- 提交信息：`feat(replay): 三分类分流 + run_match_file 支持 + compiler_missing 前置检查`
- 提交前跑：pytest tests/test_atom_evidence_replay.py + replay 全量复算（confirm 不降）

---

## 五、线 E：架构调研文档入库

### 5.1 待入库文档
References/architecture_架构演进/301-326 共 26 份（300 已入库）

### 5.2 提交要求
- 单独提交，不混工具/原子
- 提交信息：`docs(architecture): 入库 301-326 架构调研（三十学科理论底座）`
- 入库前检查：文件名规范、无空文件、无敏感信息

---

## 六、执行优先级与停止条件

### 6.1 优先级
1. **线 D（工具提交）**：最快，先清工作树
2. **线 B（CONC-002/003）**：核心生产任务
3. **线 E（文档入库）**：可与线 B 并行（纯文档，不影响门禁）
4. **线 C（ccache）**：需用户授权安装，授权后执行

### 6.2 停止条件（满足任一即停手汇报）
1. 线 B 任一颗原子的红队出现阻断级问题，需用户裁决
2. 线 C ccache 安装失败或需要额外授权
3. 门禁出现非预期 block（非历史存量 warn）
4. 上下文耗尽（如实汇报进度，不做未完成的原子化）
5. 发现新的系统性问题（如 gate 规则 bug、replay 工具 bug）

### 6.3 汇报格式
每完成一条线，按以下格式汇报：
```
线 X 完成：
- 产物：[文件列表]
- 门禁：replay confirm=X / gate block=X / poison X/X
- 关键发现：[实测中发现的新事实/教训]
- 待用户决策：[如有]
```

---

## 七、红队两段式盲读规范（线 B 必须执行）

### 7.1 第一段：盲读（不读原子卡正文）
- 只读：夹具源码 + .asm 工件 + 证据卡 actual 字段
- 任务：独立判断 claim 是否成立、断言是否可证伪、对照是否有效
- 输出：阻断/高级/建议，每条配工件证据（行号/符号）

### 7.2 第二段：对照（读原子卡正文）
- 对比第一段判断与卡内自述
- 重点查：卡是否掩盖了第一段发现的问题？claim 是否与工件矛盾？

### 7.3 can't-miss 清单（每条必须检查）
1. 断言自证（夹具自定义函数 + 断言只做存在性匹配）
2. 恒真观测（actual 只有纯存在性判断）
3. 口径不统一（同一实验多对象不同测量口径）
4. 夹具被内联（-O2 工件中函数符号消失）
5. 断言候选未在 Linux 工件实测
6. 性能数据误入 actual
7. 对照组多变量同变
8. 与已有原子实质重复（先例检查）
9. claim 与证据矛盾
10. 无限循环/无终止条件

---

## 八、元认知监控（每轮结束时记录）

- 本轮工具调用数
- 本轮修订轮次（红队→修复→复跑的循环次数）
- warn 趋势（新增/减少）
- 瓶颈分析（哪一步最耗时）
- 新发现的教训（写入 docs/kernel/教训库.md）

---

**开始执行。先做线 D（工具提交），再做线 B（CONC-002/003），线 E 可并行，线 C 等授权。**
