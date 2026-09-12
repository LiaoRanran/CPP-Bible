# 320_第六批CONC域收口与工具链P0优化_执行提示词

> 2026-09-12 · 投喂给执行 Agent · 三线并行 · 每条线有独立验收标准
> 前置：314 已执行（CONC-001 两张卡建成，双平台 confirm）；315-319 架构调研已就绪

---

## 〇、角色与总原则

你是「阙疑」系统的执行 Agent。本提示词覆盖三条独立工作线，按优先级排序：

- **线 A（最高）**：CONC-001 收口（门禁→红队→修复→原子化→提交）
- **线 B**：CONC-002 / CONC-003 生产（夹具→卡→红队→门禁）
- **线 C**：工具链 P0 优化（ccache + WSL /tmp 构建目录）

**铁律（不可违反）**：
1. 不原子化未过红队的草稿，不提交未过门禁的产物
2. claim 必须是"冒险预测"（具体、可证伪、可能失败），不可模糊
3. 断言候选必须在 Linux 工件中 grep 验证（Windows sha 路径覆盖不到 artifact_assert）
4. 工具改动与内容卡分离提交
5. 性能数据锚方向不锚倍数（同机跨运行可波动 2x+）
6.  misconceptions/MIS-CONC-* 扁平命名，不新建子目录
7. 单 artifact 原则（全库零 artifacts 复数先例）
8. 红队必须两段式盲读（先读夹具/工件，不读卡）

---

## 一、线 A：CONC-001 收口

### 当前状态

- `evidence/conc/EV-CONC-001.md`（判据卡，12 条符号区间断言）✅ 双平台 confirm
- `evidence/conc/EV-CONC-002.md`（对照卡，9 条断言）✅ 双平台 confirm
- 共用 artifact sha `8dd19bc6…`，新形态 `actual.run_match_file + run_match_keys`
- `goldens/conc/ATOM-MEM-CONC-001_draft.md` —— **待写**（卡已就绪，原子卡还没写）

### A1. 写原子草稿

路径：`goldens/conc/ATOM-CONC-001_draft.md`

**claim（≤50 字，冒险预测）**：
> 任何内存屏障（含零指令的 atomic_signal_fence）只要落在循环体内，就能阻止编译器消除该循环；但屏障不提供数据竞争安全——屏障≠原子类型。

**frontmatter 必填**：
```yaml
id: ATOM-CONC-001
domain: conc
type: mechanism
status: draft
dal: A
claim: "任何内存屏障（含零指令的 atomic_signal_fence）只要落在循环体内，就能阻止编译器消除该循环；但屏障不提供数据竞争安全——屏障≠原子类型。"
rubric_self: 4/5
verified_by: null
verified_at: null
relations:
  prereq: []
  contrasts: []
  serves: [EV-CONC-001, EV-CONC-002]
misconceptions: [MIS-CONC-XXX]  # 引用已存在的 MIS-CONC-001..010 中匹配的，不新建
status_history:
  - {level: draft, at: "2026-09-12", by: machine:writer}
```

**正文结构**：
1. 一句话直觉（"屏障是'别乱动'的编译器指令，不是'别人别动'的运行时保护"）
2. 三层分解：消除层（编译器能不能删）· 指令层（产生什么 CPU 指令）· 同步层（能不能保护数据竞争）
3. 证据摘要（引用 EV-CONC-001/002 的关键断言，不复制 full actual）
4. 教学要点：为什么需要 `std::atomic` 而不是只加屏障
5. 边界与限制：riscv 平台 3 条 x86 专有助记符断言不适用（如实标注）
6. 修订记录：v1 口径"屏障拦不住消除"被三平台实测推翻 → v2 修正为"循环体内阻止消除"

### A2. 门禁全跑

```bash
python tools/gate_engine.py --check
python -m pytest tests/ -q
python tools/golden_lock.py check
python tools/atom_evidence_replay.py --check  # 确认 evidence/conc/ 被扫描
```

**验收**：gate block=0、pytest 全过、golden_lock 无恶化、replay confirm=50（48 旧 + 2 新）。

若 gate 报 `EV-SERVES-EXIST` 或 `ATOM-REL-TARGET`——这是预期债（草稿在 goldens/ 不被扫描，原子化后自动清零），记录即可，不阻断。

### A3. 红队两段式盲读

启动独立子 agent 做红队，**不给草稿全文**，只给：
- 夹具源码 `Examples/_atom_conc_fence.cpp`
- 工件 `Examples/_atom_conc_fence.asm`（sha 8dd19bc6…）
- 两张证据卡的 actual 部分

红队 must-check（can't-miss）：
1. claim 与工件是否一致？（重点："循环体内"这个前提是否在工件中可验证）
2. 12 条符号区间断言是否真的在函数体区间内？会不会被其他函数的符号污染？
3. `signal_fence 零指令`这个结论——工件中 `writer_signal_fence` 函数体是否真的没有屏障指令？
4. `屏障挪出循环即无效`——`spin_fence_outside` 是否真的被消除？
5. 活性观测：有没有断言是编译期折叠常量？（functions_present=7 已标注，还有没有其他？）
6. 跨编译器：riscv 9/12 的 3 条失败是否真的只是 x86 助记符差异？会不会掩盖了真实的行为差异？

红队输出：阻断级 / 高级 / 建议，每条带工件行号证据。

### A4. 修复（循环上限 2 轮）

按红队结果修复，每轮修复后重跑 replay 确认 sha 变化（若改了夹具）或不变（若只改卡）。

### A5. 原子化 + 签署 + 提交

```bash
# 移动（草稿是 untracked，用文件系统移动）
move goldens/conc/ATOM-CONC-001_draft.md atoms/conc/ATOM-CONC-001.md

# frontmatter 签署
status: verified
verified_by: human:liaoranran
verified_at: 2026-09-12
# 删除 rubric_self，正文加「5 分锚定依据」三条

# 门禁复跑（铁律：原子化后立即跑 gate）
python tools/gate_engine.py --check

# golden_lock sync
python tools/golden_lock.py sync

# 提交（内容卡，不含工具改动）
git add atoms/conc/ evidence/conc/ Examples/_atom_conc_fence* misconceptions/MIS-CONC*
git commit -F commit_msg.txt
```

**验收**：verified_atoms 20→21、evidence 48→50、replay confirm=50、gate block=0。

---

## 二、线 B：CONC-002 / CONC-003 生产

### CONC-002：锁的代价与无锁的代价

**claim（冒险预测，≤50 字）**：
> 无竞争时 std::mutex 快路径为用户态原子操作（~30-60ns）；高竞争下 CAS 自旋可退化至比 mutex 更慢——"无锁更快"不成立。

**夹具设计**：
- 双构建同源宏门控（`-DBENCH_FULL` 只给 .out 生成用，actual 只放方向量与常量）
- 三组对照：mutex 保护 / atomic CAS 自旋 / 无保护（数据竞争，仅作基线）
- 打印 `nproc`、`cas_degrades=1` 或 `insufficient_cores=1`（用 contains_any）
- **不锚倍数**（同机跨运行可波动 2x+），只锚方向

**证据卡**：EV-CONC-003（判据卡：mutex fast path 有 cmpxchg）、EV-CONC-004（性能卡：方向量 + 完整 7 轮逐样本放 .out）

**注意**：Windows/MinGW 的 `-pthread` 可用但 TSan 不可用；TSan 只作 WSL/CI 列且命令必须 `setarch -R` 前缀。

### CONC-003：数据竞争的 UB 与工具检测

**claim（冒险预测，≤50 字）**：
> 数据竞争是未定义行为——编译器可消除/提升竞争访问；TSan 能检测但开销 5-15x，且 MinGW 不支持。

**夹具设计**：
- **有界循环**（防止 replay 超时 600s→rc=124→refute）
- -O0 vs -O2 双工件：-O2 作 artifact，-O0 只在正文留痕（单 artifact 原则）
- 描述写"消除或提升（以工件为准）"，不写死"缓存在寄存器导致死循环"
- TSan 列：WSL `setarch -R g++ -fsanitize=thread`，如实标注 MinGW 不可本地复现

**证据卡**：EV-CONC-005（编译器行为卡：-O2 工件中竞争访问被消除/提升）、EV-CONC-006（TSan 检测卡：expected_sanitizer: [thread]）

### 线 B 通用流程

每颗原子：夹具 → 双平台工件 → 2 证据卡 → 原子草稿 → 门禁 → 红队两段式盲读 → 修复 → 原子化 → 提交。

**两颗可以流水线并行**：CONC-002 红队时，CONC-003 可以写卡。

---

## 三、线 C：工具链 P0 优化（ccache + WSL /tmp）

### C1. ccache 集成

**目标**：replay 全量编译从 ~2 分钟降到 ~5 秒。

**步骤**：
1. 检查 ccache 是否可用（Windows: `where ccache`；WSL: `which ccache`）
2. 若不可用，记录安装命令（不自动安装，等用户确认）
3. 修改 `tools/atom_evidence_replay.py`：编译器调用从 `g++ ...` 改为 `ccache g++ ...`（若 ccache 可用）
4. 加环境变量开关 `CPPBIBLE_CCACHE=0` 可禁用
5. CI 加 `actions/cache@v4` 缓存 `~/.ccache`

**验收**：
- 首次 replay：编译时间不变（缓存冷）
- 第二次 replay（无代码变化）：编译时间 <10 秒（缓存命中）
- `ccache -s` 显示 hit rate >80%

**注意**：ccache 哈希包含编译器版本，GCC 升级后缓存自动失效——这是正确行为。

### C2. WSL 构建目录放 /tmp

**目标**：WSL replay 从 ~3 分钟降到 ~10 秒（消除 /mnt/c 9P 税）。

**步骤**：
1. 修改 `tools/atom_evidence_replay.py`：WSL 侧运行时，编译产物输出到 `/tmp/cppbible_build/`（而非 Examples/）
2. 编译/运行都在 /tmp 里完成
3. 只有最终需要 git 跟踪的 .asm/.out 才复制回 `Examples/`
4. 加清理逻辑：replay 结束后删除 /tmp/cppbible_build/（或保留供 ccache）

**验收**：
- WSL replay 全量时间 <15 秒（ccache 热缓存）
- Examples/ 下的 .asm/.out 与 /tmp 构建产物逐字一致
- Windows 侧 replay 不受影响（仍用 Examples/）

### C3. 工具改动分离提交

```bash
# 提交 1：工具改动
git add tools/atom_evidence_replay.py .github/workflows/ci.yml
git commit -m "perf(replay): ccache integration + WSL /tmp build dir"

# 提交 2：内容卡（线 A/B 的产物）
git add atoms/conc/ evidence/conc/ Examples/ ...
git commit -m "feat(conc): CONC-001/002/003 atoms and evidence cards"
```

---

## 四、元认知监控（每批结束时填写）

在质检报告中增加：
```yaml
metacognition:
  redteam_tool_calls: {avg: __, max: __, min: __}
  writer_revision_rounds: {avg: __, max: __}
  gate_warn_trend: [4, 8, 10, __]  # 近四批
  replay_time_seconds: {before_ccache: __, after_ccache: __}
  bottleneck_analysis: "__"
  action_items: ["__"]
```

---

## 五、交付物清单

### 线 A
- [ ] `atoms/conc/ATOM-CONC-001.md`（verified）
- [ ] `evidence/conc/EV-CONC-001.md`、`EV-CONC-002.md`（已 confirm）
- [ ] 红队报告（含阻断/高/建议）
- [ ] 提交哈希

### 线 B
- [ ] `atoms/conc/ATOM-CONC-002.md`、`ATOM-CONC-003.md`（verified）
- [ ] `evidence/conc/EV-CONC-003..006.md`（4 张）
- [ ] 夹具 + 工件 + .out
- [ ] 红队报告 ×2
- [ ] 提交哈希

### 线 C
- [ ] `tools/atom_evidence_replay.py`（ccache + /tmp 支持）
- [ ] `.github/workflows/ci.yml`（ccache 缓存）
- [ ] 性能对比数据（before/after）
- [ ] 提交哈希

### 全局
- [ ] `docs/G5_CONC_batch1_quality_inspection.md`（含元认知监控）
- [ ] golden_lock 基线 {atoms: 23, evidence: 54, verified: 23, replay: 54}

---

## 六、停止条件

以下任一情况发生时，停止并报告监工：
1. 红队阻断级问题修复超过 2 轮
2. gate block >0 且无法在 1 轮内修复
3. 夹具实测推翻了 claim（需要重新设计，不是修修补补）
4. 工具改动导致 replay 回归（confirm 数下降）
5. ccache 安装需要用户授权（不自动安装）

**不要**：为了赶进度压缩红队步骤、跳过门禁、把未验证的 claim 写进原子卡。
