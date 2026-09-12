# 第六批 CONC 域首批原子生产提示词（v3.1 实测修正版）

> 投喂给执行 Agent。本版经过独立审查（实测 GCC 15.3 MinGW x86-64 + WSL g++-14/13 + riscv64-unknown-elf-g++ 13.2），所有 claim 均以本地产物可证伪为前提。
> v2 因路径错误未落盘，本版直接覆盖 312。
> **v3.1（2026-09-12）**：§4.1/§4.2 的 claim 方向被三平台实测**推翻并改正**——原句「屏障拦不住消除」错误，正确口径是「**屏障在循环体内阻止消除，但屏障≠原子类型**」；§4.3 断言锚改写为 `contains_in`/`absent_in` 区间语义共 12 条（三平台已核验）；PG commit 降为移植性论据。
> 核心原则：用确定性的编译器行为做证据，不用不确定的运行时调度；用真实工业案例做锚点，不用抽象假设；所有断言锚必须在 Linux 工件中 grep 验证。

---

## 〇、选题论证（为什么是这三颗）

CONC 域零原子，但有 8 份调研资料 + 10 条既有误解（MIS-CONC-001..010）。首批选这三颗：

| 原子 | 为什么是第一批 | 真实案例锚点 | 本地产物可证 |
|---|---|---|---|
| CONC-001 屏障≠原子类型 | 展示"为什么需要原子类型而不只是加屏障"——屏障在**循环体内**能保住循环（零指令的 signal_fence 也保得住），挪到体外则无效，但屏障≠原子类型 | PostgreSQL f8ccab0e（C11 fence 只为原子访问定义语义，**仅作移植性论据**） | ✅ 三平台（MinGW 15.3 / g++-14.2 / riscv64 13.2）确定；x86 侧 12/12 断言可机器核验 |
| CONC-002 同步原语代价分层 | 打破"无锁一定更快"，展示高竞争下 CAS 退化 | sync-shootout / Travis Downs | ✅ 双构建宏门控 |
| CONC-003 数据竞争的编译器优化 | 数据竞争是 UB 的最确定证据——编译器消除/提升，不是运行时崩溃 | Boehm PLDI'05 | ✅ 有界循环 + artifact_assert |

---

## 一、通用铁律（13 条，含本批新增）

1. claim/actual 不编造；断言锚只锚常量+活性对照，时序数据不入断言锚
2. 夹具不重载 operator new/delete（避 P4 自证断言）
3. 对照单变量、基数一致
4. **断言候选必须在 Linux 工件中 grep 验证**（Windows sha 路径覆盖不到 artifact_assert——EV-MEM-040/041 教训）
5. 红队两段式盲读（先读夹具/工件不读卡，再对照卡）
6. 修复循环≤2轮，超限升级人审
7. 未原子化、未 commit、未 push 前不报"完成"
8. 性能数据锚方向不锚倍数，多轮中位数（同机跨运行可波动 2x+——PERF-004 实测 18.86×→8.78×）
9. 同一实验中的多个对象必须用同一口径测量（ALLOC-002 教训）
10. S3-EXPECTED-HARDCODED：夹具注释里不要写带双引号的完整取值串
11. **并发实验优先用编译器行为做证据，不用运行时调度做证据**（编译器行为确定，运行时调度不确定）
12. **编译器行为钉到版本粒度**：卡内必须写全"编译器+版本+优化档+架构"（GCC 15.3 MinGW / 13.3·14.2 WSL / riscv64-elf 13.2 实测已有指令差异）
13. **描述与工件一致**：写"消除或提升（以工件为准）"，不写死"缓存在寄存器导致死循环"——GCC 实测是把循环整段删掉

---

## 二、G6 四级状态契约（必须遵守）

每颗原子的 frontmatter 必须包含：
```yaml
status: draft              # 起点，不允许直接置 verified
dal: A|B|C|D|E             # 必填，并发/内存模型"错用即 UB 且难复现"⇒ A/B 强制人审
dal_reviewed_by:           # 免人审须人签（A/B 级不允许免人审）
human_review: required|optional|exempt  # A/B=required，C/D=optional，E=exempt
status_history:            # 三点：创建→红队→人审（或机器自治）
  - { level: draft, at: "2026-09-12", by: machine:writer }
  - { level: red-team-verified, at: "2026-09-12", by: redteam:<agent_id> }
  # 第三点人审后补：{ level: verified, at: "2026-09-12", by: human:liaoranran }
```

> **schema 注意**：gate_engine.py 读的是 `level` 键（不是 from/to），`by` 必须带前缀 `machine:` / `redteam:` / `human:`（LEVEL_PRINCIPALS 强制），否则 ATOM-STATUS-TRANSITION block。

**DAL 定级口径**（本批）：
- CONC-001：B（教学结论方向——屏障理解错了会写出并发缺陷，但不直接崩溃）
- CONC-002：C（性能定量结论，不改变方向）
- CONC-003：A（读者写出数据竞争 = 并发缺陷，崩溃/数据错误/无限循环）

**人审规则**：
- A/B 级：`human_review: required`，必须人审，不允许 Writer 自封 verified
- C/D/E 级：`human_review: optional`，红队通过即可，但**豁免须人签**——`dal_reviewed_by: human:<监工>` 必须填写，否则 ATOM-DAL-MATCH block

---

## 三、三权分立交付物切分

| 角色 | 交付物 | 禁止 |
|---|---|---|
| Writer | 夹具 + 工件 + 证据卡 + 误解 + 原子草稿（draft） | 不置 verified、不原子化、不 commit |
| RedTeamer（独立子 agent） | 红队报告（阻断/高/建议）+ 修订建议 | 不改文件，只出报告 |
| Gatekeeper | 门禁全跑（replay/gate/poison/pytest/golden_lock/WSL） | 不改内容，只出 pass/fail |
| 人审 | 签署 verified + 三点锚定依据 | — |

**红队两段式盲读**：
1. 第一段：只读夹具源码 + 工件（.asm/.out），不读证据卡和原子草稿——独立发现结构缺陷
2. 第二段：对照证据卡和原子草稿，找 claim 与工件的矛盾

---

## 四、CONC-001：屏障≠原子类型（屏障位置决定消除）

### 4.1 核心洞察（v3.1：原「屏障拦不住消除」已被实测推翻）

v3.0 写的「屏障拦不住消除」方向写反了：实测显示**屏障在循环体内就能保住循环**（连零指令的 `signal_fence` 也保得住）。必须区分三个层面——原版把第 1 层与第 3 层混为一谈，才得出反向结论：

1. **消除层（编译器）**：`atomic_signal_fence` / `atomic_thread_fence` 只要落在**循环体内**，就可阻止 GCC 把 `while (!b) {}`（b 为非原子非 volatile 全局变量）整段消除；**屏障挪到循环体外则与不放屏障完全等价**（照样被消除）。
2. **指令层（硬件）**：`signal_fence` 是**纯编译器屏障**——实测自旋侧与写入侧两条路径均为**零机器指令**；`thread_fence` 才有硬件屏障：x86-64 `lock or QWORD PTR [rsp], 0`，riscv64 `fence iorw,iorw`。
3. **同步层（数据竞争）**：两者都**不为普通 `int` 提供原子性与跨线程 happens-before** ⇒ **屏障≠原子类型**（屏障不能把普通 `int` 变成数据竞争安全的类型）。

三平台实测（`-O2`，主证据 `Examples/atoms/_atom_fence_vs_atomic.asm`，sha `8dd19bc6…`，5165 B）：

| 函数 | 屏障位置 | x86-64（MinGW 15.3；g++-14.2 / 13.3 同形） | riscv64 13.2 | 结论 |
|---|---|---|---|---|
| `spin_plain` | 无 | `mov eax, s_p_a[rip]; ret` | `lw a0, %lo(s_p_a); ret` | **整段消除**，标志读一并消失 |
| `spin_signal_fence` | **体内** | 循环回边保留，读 `s_sf_b`，**区间内零 `lock`** | 循环回边保留（`beq`），**区间内无 `fence`** | **保留**（零指令也保得住） |
| `spin_with_fence` | **体内** | 循环内 `lock or QWORD PTR [rsp], 0` ×1 | 循环内 `fence iorw,iorw` | **保留**，产硬件屏障 |
| `spin_volatile` | 体内（volatile） | 有界循环保留（`bound=1e6`） | 同 | 活性对照（**不是同步原语**） |
| `spin_fence_outside` | **体外** | `mov eax, s_o_a[rip]; ret` | 同 | **与不放屏障等价：被消除** |
| `writer_signal_fence` | — | 区间内 `lock` = **0** | 区间内 `fence` = **0** | signal_fence 零指令 |
| `writer_thread_fence` | — | 区间内 `lock` = **1** | 区间内 `fence iorw,iorw` = 1 | thread_fence 才有硬件屏障 |

**教学价值**：直指"为什么需要原子类型，而不只是加屏障"——屏障确实能改变编译器对循环的处理，但**位置敏感**（体内有效、体外无效），且不给普通变量提供原子性与可见性；把屏障当同步手段用是错的。

### 4.2 claim（单句，≤50 字，本地产物可证）

> **屏障在循环体内阻止消除，但屏障≠原子类型。**

展开版（供原子 `claim` 字段）：`while (!b) {}`（b 为非原子非 volatile 全局 `int`）在 `-O2` 下会被整段消除（`spin_plain` / `spin_fence_outside` 实测区间内**零** `s_*_b` 符号引用）；把 `atomic_signal_fence`（实测**零机器指令**）或 `atomic_thread_fence`（x86-64 实测 `lock or QWORD PTR [rsp], 0` ×1）放进**循环体内**即可保住循环；但两者都不提供原子性与跨线程 happens-before——要安全同步必须改用原子类型/锁。PostgreSQL f8ccab0e（2025-11-07，REL_18_STABLE，backpatch-through 13）为「C11 fence 只为原子访问定义语义」打补丁，**仅作移植性论据**（外部留痕），不作本地产物断言、不作主 claim。

### 4.3 实验设计

**夹具**：`Examples/atoms/_atom_fence_vs_atomic.cpp`（7 个 `noinline` 函数 + 1 个 setter；**零 `#include`**，用 `__atomic_*` 内建与 `extern "C"` 声明 `printf`，riscv64 bare-metal 工具链同样能编译）

**唯一变量 = 有屏障 / 无屏障（体内 vs 体外）的单变量阶梯**；每个函数**独占**自己的全局变量，确保"某符号出现在某函数区间内"只可能来自该函数体（第一层保险是 `_symbol_body` 的区间语义，独占命名是第二层）：

| 函数 | 独占全局 | 台阶 |
|---|---|---|
| `spin_plain` | `s_p_a` / `s_p_b` | 无屏障（基线） |
| `spin_signal_fence` | `s_sf_a` / `s_sf_b` | **循环体内** `__atomic_signal_fence(SEQ_CST)` |
| `spin_with_fence` | `s_f_a` / `s_f_b` | **循环体内** `__atomic_thread_fence(SEQ_CST)` |
| `spin_volatile` | `s_v_a` / `s_v_b` | 循环体内 volatile 读 + 有界 `1e6`（活性对照；**不是同步原语**） |
| `spin_fence_outside` | `s_o_a` / `s_o_b` | **屏障在循环体外**（机制隔离对照：用来证明"体内"才是因） |
| `writer_signal_fence` | `w_s_a` / `w_s_b` | 写入侧：纯编译器屏障（零指令） |
| `writer_thread_fence` | `w_t_a` / `w_t_b` | 写入侧：硬件屏障 |

> 摘录（全局名/函数名与工件**逐字一致**；完整源码见夹具文件）：

```cpp
int s_p_a = 0,  s_p_b = 0;    // spin_plain 独占
int s_sf_a = 0, s_sf_b = 0;   // spin_signal_fence 独占
int s_f_a = 0,  s_f_b = 0;    // spin_with_fence 独占
int s_v_a = 0,  s_v_b = 0;    // spin_volatile 独占
int s_o_a = 0,  s_o_b = 0;    // spin_fence_outside 独占

__attribute__((noinline)) int spin_plain() {
    while (!s_p_b) {}
    return s_p_a;
}

__attribute__((noinline)) int spin_signal_fence() {           // 屏障在体内，但零指令
    while (!s_sf_b) { __atomic_signal_fence(__ATOMIC_SEQ_CST); }
    return s_sf_a;
}

__attribute__((noinline)) int spin_with_fence() {             // 屏障在体内，产硬件屏障
    while (!s_f_b) { __atomic_thread_fence(__ATOMIC_SEQ_CST); }
    return s_f_a;
}

__attribute__((noinline)) int spin_volatile() {               // 有界！防 replay 超时
    volatile int* vb = &s_v_b;
    int bound = 1000000;
    while (!*vb && --bound > 0) {}
    return s_v_a;
}

__attribute__((noinline)) int spin_fence_outside() {          // 屏障在体外 ⇒ 无效
    __atomic_thread_fence(__ATOMIC_SEQ_CST);
    while (!s_o_b) {}
    return s_o_a;
}

// main 顺序：set_all_flags(1) 先把全部标志置 1，再依次调用 5 个 spin 函数
```

**终止性保证**：`main()` 先 `set_all_flags(1)`，5 个 spin 函数的循环条件**首次即为假** ⇒ 不进入循环体；`spin_volatile` 另有 `bound=1e6` 上界双保险 ⇒ replay 执行 command 必然终止，不撞 600s 超时。

**确定性打印（留痕 `.out` = 程序 stdout 原文，3 行）**：
- `spin_plain_ret=7|spin_signal_fence_ret=8|spin_with_fence_ret=9|spin_volatile_ret=10`
- `spin_fence_outside_ret=11|writer_signal_fence_ret=3|writer_thread_fence_ret=3`
- `functions_present=7|spin_volatile_engaged=1`

**工件**（**单 artifact 原则**：只提交主证据）：
- 主证据：`Examples/atoms/_atom_fence_vs_atomic.asm`（MinGW g++ 15.3.0 `-O2 -S -masm=intel`，sha `8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3`，5165 B）
- 留痕：`Examples/atoms/_atom_fence_vs_atomic.out`（供 `run_match_file` 复跑比对）
- 跨编译器对照：WSL `g++-14` / `g++-13` `-O2 -S -masm=intel`（**不提交**，读数写进卡）
- 跨架构对照：WSL `riscv64-unknown-elf-g++` 13.2 `-O2 -S`（**不提交**，读数写进卡）

**断言锚（12 条，`contains_in` / `absent_in` 符号区间语义；已三平台 grep 核验）**：

| # | 断言 | MinGW 15.3 | g++-14.2 | g++-13.3 | riscv 13.2 |
|---|---|---|---|---|---|
| 1 | `absent_in` `_Z10spin_plainv` `s_p_b` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 2 | `absent_in` `_Z10spin_plainv` `je` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 3 | `contains_in` `_Z17spin_signal_fencev` `s_sf_b` | 2 ✅ | 1 ✅ | 1 ✅ | 3 ✅ |
| 4 | `contains_in` `_Z17spin_signal_fencev` `je` | 1 ✅ | 1 ✅ | 1 ✅ | 0 ❌（riscv 用 `beq`） |
| 5 | `absent_in` `_Z17spin_signal_fencev` `lock` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 6 | `contains_in` `_Z15spin_with_fencev` `s_f_b` | 2 ✅ | 1 ✅ | 1 ✅ | 3 ✅ |
| 7 | `contains_in` `_Z15spin_with_fencev` `lock` | 1 ✅ | 1 ✅ | 1 ✅ | 0 ❌（riscv 用 `fence`） |
| 8 | `contains_in` `_Z13spin_volatilev` `s_v_b` | 1 ✅ | 1 ✅ | 1 ✅ | 2 ✅ |
| 9 | `absent_in` `_Z18spin_fence_outsidev` `s_o_b` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 10 | `absent_in` `_Z18spin_fence_outsidev` `je` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 11 | `absent_in` `_Z19writer_signal_fencev` `lock` | 0 ✅ | 0 ✅ | 0 ✅ | 0 ✅ |
| 12 | `contains_in` `_Z19writer_thread_fencev` `lock` | 1 ✅ | 1 ✅ | 1 ✅ | 0 ❌（riscv 用 `fence`） |

**核验口径**：`#4 / #7 / #12` 是 **x86-64 专有助记符**（`je` / `lock`），riscv 上是 9/12——故 `artifact_assert` 只放这 12 条并声明 `claim_boundary.platform: [x86-64]`；riscv 的 9/12 与指令差异如实写进卡内正文/falsification 作跨架构佐证，**不写死进断言**（"不写死"铁律）。
符号缺失时 `_symbol_body` 返回 `None` ⇒ 该条直接判失败（fail-closed），因此 `functions_present=7` 不是唯一的存在性保障。

**注意**：
- 不锚"重排方向"（x86 把 load 提到 store 之前，riscv 没有——方向是脆的）
- 锚"屏障在不在循环体内"与"标志读还在不在"（确定、两条 x86 工具链逐字一致）
- PG 案例只作外部锚点（commit hash + branch + 日期），不作 artifact 断言

**证据卡（三层分离：卡只留判据，原始输出留在 `.out`）**：
- EV-CONC-001（判据卡）：`actual.run_match_file` + `run_match_keys` + 12 条区间断言（消除分界）
- EV-CONC-002（对照卡）：写入侧对照 + 零指令实证（signal_fence 零指令 vs thread_fence 产 `lock`）

**误解**：引用既有 **MIS-CONC-001**（"volatile 可以用于线程间同步 / 当数据就绪标志"，与本原子同属"把非同步原语当同步手段"家族）；如后续需独立条目，**新建 MIS-CONC-011**，不得新建子目录
- **严禁新建 misconceptions/conc/ 子目录**——MIS-CONC-* 是扁平命名，在 misconceptions/ 根目录下
- 先读 MIS-CONC-001..010，找主题匹配的引用；没有匹配才新建 MIS-CONC-011+
- 本批（314）口径收紧为"只引用既有 ID"，故本轮**只引用 MIS-CONC-001、不新建**

### 4.4 技术风险与缓解

| 风险 | 缓解 |
|---|---|
| GCC 版本差异导致消除行为不同 | 钉到版本粒度（GCC 15.3 / 14.2 / 13.3 / riscv 13.2），卡内写全；两条 x86 工具链实测**同形** |
| **断言里 `je` / `lock` 是 x86-64 专有助记符** | riscv 实测 9/12（用 `beq` / `fence`）⇒ 断言锚限定 `platform: [x86-64]`，riscv 差异只写在卡内正文，**不写死进断言** |
| riscv64 工具链没有 `<atomic>` 头 | 夹具零 `#include`，用 `__atomic_*` 内建 + `extern "C"` 声明 `printf` |
| 读者混淆 volatile 和 atomic | 卡内明确：volatile 只演示"不可消除"，不是同步原语，不能替代 atomic |
| **读者把"屏障能保住循环"读成"屏障能当同步用"** | claim 单句收口在"**但屏障≠原子类型**"；`falsification` 里给出反例方向（屏障不给普通 `int` 原子性） |
| PG 案例本地无法复现（需要 Clang） | PG 只作外部锚点（commit hash f8ccab0e + branch + 日期），不作 artifact 断言，**不作主 claim** |

### 4.5 DAL：B（强制人审）

---

## 五、CONC-002：同步原语代价分层

### 5.1 核心洞察

"无锁一定更快"是误解。同步原语的代价是分层体系：

1. **原子 RMW（fetch_add）**：单条 `lock xadd`，最快但只能做单值操作
2. **CAS 自旋锁**：`lock cmpxchg` 重试循环，高竞争下严重退化（缓存行弹跳 + 空转）
3. **std::mutex**：futex 快速路径（无竞争 30-60ns）+ 内核等待（有竞争 1-10μs），高竞争下反而稳定

**反直觉发现**：高竞争下 CAS 自旋锁可能比 mutex 慢（自旋空转浪费 CPU vs 睡眠让出 CPU）。但在低核数/单核 CI/无超线程环境可能反向——必须声明变量域与证伪条件。

### 5.2 claim（单句可证伪，本地产物可证）

同步原语的代价不是"有锁 vs 无锁"的二元对立——fetch_add（lock xadd 单指令）在单值递增上最快，CAS 自旋锁在高竞争下因缓存行弹跳和空转而退化（4 线程吞吐 < 2 线程，需 ≥4 核环境），std::mutex 有竞争时通过睡眠让出 CPU 反而稳定；"无锁一定更快"只在低竞争单值操作上成立，在高竞争或多变量保护场景不成立。

> claim 中不写外部数字（30-60ns / 27M ops/s 等）——那些放 §5.x「关键参考数据」，claim 只写本地产物可证的方向。

### 5.3 实验设计

**夹具**：`Examples/atoms/_atom_sync_cost.cpp`

**关键：双构建同源、宏门控**（同 EV-MEM-045 范式）：
```cpp
// 核心逻辑（无性能打印，用于 .asm 工件和 replay）
void increment_mutex() { ... }
void increment_fetch_add() { ... }
void increment_cas_lock() { ... }
void increment_atomic_with_backoff() { ... }  // 第 4 列：atomic + 退避

#ifdef BENCH_FULL
// 性能测试（只给 .out 生成用，不进入 replay 的 run_match）
int main() {
    // 1/2/4 线程，1e7 次递增，7 轮中位数
    // 打印方向量与常量，不打印逐轮纳秒（逐轮纳秒会进入 run_match 逐字比对→必然 refute）
}
#endif
```

**四种实现**：
1. std::mutex（lock_guard 包裹 ++counter）
2. atomic fetch_add（seq_cst）
3. CAS 自旋锁（compare_exchange_weak 循环，无退避）
4. atomic + 退避（CAS 循环 + `std::this_thread::yield()` 或 `_mm_pause()`）——第 4 列，防止学生得出"原子永远最优"

**性能测试**：
- 1/2/4 线程，各跑 1e7 次递增
- 7 轮中位数
- **actual.run_* 只放方向量与常量**，不放逐轮纳秒
- 逐轮纳秒放 .out（`-DBENCH_FULL` 构建生成），不入断言锚

**工件**：
- .asm（非 BENCH_FULL 构建）：对比 `lock xadd` / `lock cmpxchg` / `__gthread_mutex_lock`
- .out（BENCH_FULL 构建）：含完整 7 轮逐样本 + min/max + 比值

**断言锚**：
- fetch_add 工件包含 `lock` 前缀指令（contains_any: `lock xadd` / `lock add`）
- CAS 工件包含 `lock cmpxchg`（contains_any）
- mutex 工件包含 `__gthread_mutex_lock` 或 `pthread_mutex_lock`（contains_any）
- 性能卡只锚方向：
  - `fetch_add_1thread_fastest=1`（单线程下 fetch_add 最快）
  - 夹具先打印 `nproc=<核数>`；CAS 退化断言用 `contains_any: ["cas_4thread_degrades=1", "insufficient_cores=1"]`（≤2 核环境合法翻转为 insufficient_cores，不判 refute）
  - **不锚具体倍数**（同机跨运行可波动 2x+）
  - **声明变量域**：核数 ≥4 才观测退化、竞争度高（1e7 次共享递增）、迭代数固定

**反例条件**（必须写入卡内）：
- 在单核 CI 上，CAS 退化可能不明显（无真正并行）
- 在低竞争场景（如每次操作间隔长），mutex 快速路径可能比 CAS 循环更快
- Windows/MinGW 的 -pthread 实现与 Linux glibc futex 不同，性能数据不可跨平台直接比较

**关键参考数据**（用于 claim 锚定，不用于断言）：
- sync-shootout：atomic 8 线程 27M ops/s，mutex 8.3M，ticket lock 32 线程 ~0
- Travis Downs：高竞争下 fetch_add 显著优于 CAS，mutex 在 3+ 核不差
- mutex fast path：30-60ns（无竞争，纯用户态 CAS）

**误解**：引用既有 MIS-CONC-002（如果主题匹配）或新建 MIS-CONC-012

### 5.4 技术风险与缓解

| 风险 | 缓解 |
|---|---|
| 性能数据波动大 | 7 轮中位数 + 锚方向不锚倍数 + 双构建宏门控 |
| 逐轮纳秒进入 run_match → 必然 refute | BENCH_FULL 宏门控，actual 只放方向量 |
| CAS 自旋锁可能被优化掉 | 计数器全局 + side effect（返回值），防止优化 |
| 4 线程在 CI 上可能只有 2 核 | 用 1/2/4 线程，退化趋势仍在；卡内声明变量域 |
| Windows/MinGW -pthread 与 Linux 差异 | 双平台实测，如实标注；性能列不混谈 TSan |
| TSan 不可用（MinGW） | TSan 只在 WSL/Linux 列，Windows 侧只做编译期工件对比 |

### 5.5 DAL：C（红队通过即可，但豁免须人签 dal_reviewed_by: human:*）

---

## 六、CONC-003：数据竞争的编译器优化

### 6.1 核心洞察

数据竞争是 C++ 的未定义行为。最确定的证据不是"跑出错"（不确定，依赖调度），而是**编译器做出了单线程假设下的激进优化**（确定的，每次编译都一样）。

实测（GCC 15.3 MinGW x86-64，-O2）：
- `while (!g_flag) {}`（非原子）→ **循环被整段消除**（不是"缓存在寄存器"，是直接删掉）
- 用 `std::atomic<bool>` 后 → 循环内每次都从内存读，不被消除
- 这正是 Boehm 2005 论文"Threads cannot be implemented as a library"的核心论点

**关键**：replay 会真的执行 command，如果写无限循环 → 超时 600s → rc=124 → refute，CI 白挂十分钟。**必须改成有界循环**。

### 6.2 claim（单句可证伪）

数据竞争是 C++ 的未定义行为——编译器可以假设"非原子变量不会被并发修改"，从而在 -O2 下消除或提升共享变量的内存访问（以工件为准：GCC 15.3 实测为整段消除循环）；用 `std::atomic` 后编译器每次从内存读，访问不被消除。ThreadSanitizer 可以检测数据竞争（5-15x 慢、5-10x 内存，几乎零误报），但"TSan 没报"不等于"没有数据竞争"（受调度和输入影响），且 MinGW 无 TSan（只能 CI/WSL 列）。

### 6.3 实验设计

**夹具**：`Examples/atoms/_atom_data_race.cpp`

**关键：有界循环，不写无限循环**：
```cpp
// 非原子版本（数据竞争 UB）
bool g_flag = false;
int g_data = 0;

__attribute__((noinline)) void writer() {
    g_data = 42;
    g_flag = true;
}

// 有界忙等（非原子）—— -O2 下循环可能被消除/提升
__attribute__((noinline)) int reader_noatomic() {
    int iterations = 0;
    while (!g_flag && iterations < 1000000) {  // 有界！
        ++iterations;
    }
    return g_data + iterations;  // side effect，防止完全消除
}

// 原子版本（无数据竞争）
std::atomic<bool> a_flag{false};
std::atomic<int> a_data{0};

__attribute__((noinline)) int reader_atomic() {
    int iterations = 0;
    while (!a_flag.load(std::memory_order_acquire) && iterations < 1000000) {
        ++iterations;
    }
    return a_data.load(std::memory_order_acquire) + iterations;
}
```

**关键观测**：
- -O2 编译后，`reader_noatomic` 的循环体中，`g_flag` 的读可能被提升到循环外或消除
- `reader_atomic` 的循环体中，`a_flag.load` 每次都读（atomic load 隐含 compiler barrier）
- 活性对照：两个 reader 函数都存在于 .asm 中

**TSan 验证**（WSL/Linux only，MinGW 不可用——MinGW 链接即失败 `cannot find -ltsan`）：
- WSL 命令必须前缀 `setarch -R`（否则 `FATAL: ThreadSanitizer: unexpected memory mapping`）：
  ```bash
  setarch -R g++ -O1 -fsanitize=thread -o atom_dr _atom_data_race.cpp && setarch -R ./atom_dr
  ```
- CI（ubuntu-latest）同样需要 `setarch -R` 前缀
- `-fsanitize=thread` 编译运行非原子版本（writer + reader 并发），TSan 报 data race
- 原子版本 TSan 不报
- .out 含完整 TSan 输出（stderr 原文）
- sanitizer 判定按类型归并（`expected_sanitizer: [thread]`），不按子串（LeakSanitizer 复用 SUMMARY: AddressSanitizer 的坑已在案）

**工件与落卡方式**：
- **单 artifact 原则**：全库 48 张卡都是单 artifact + 单 artifact_sha256，零 artifacts 复数先例
- -O2 那份作 `artifact`（主工件，锚消除/提升）
- -O0 那份**只在证据卡正文留痕**（贴关键汇编片段），不进 artifact 字段
- .asm 用 `-masm=intel`
- .out 含 TSan 完整输出（WSL/Linux 生成，Windows 侧只出 .asm）

**断言锚**（写法必须可机器实现）：
- `reader_noatomic` -O2 **函数体标签区间内**不出现 `g_flag` 符号引用（absent：被消除/提升）——同 CONC-001 写法，不用"循环体"（消除后没有循环体标签）
- `reader_atomic` -O2 **函数体标签区间内**出现 atomic load（contains_any：`__atomic_load` 或 `mov` + 屏障）
- TSan 输出包含 "data race"（contains_any）——非原子版本
- TSan 输出不包含 "data race"（absent）——原子版本
- 活性对照：两个 reader 函数都存在于 .asm 中

**expected_sanitizer**：EV-CONC-005 声明 `expected_sanitizer: [thread]`（同 EV-MEM-014 的 leak 口径——有意演示数据竞争，TSan 报到属正确检测）

**注意**：
- 描述写"消除或提升（以工件为准）"，不写死"缓存在寄存器导致死循环"
- 如果 GCC 15.3 -O2 没有消除（太保守），用 -O3 或更复杂的代码模式；如实标注，不编造
- 数据竞争的运行时结果不确定，不用"跑出错"做证据，用编译器汇编做证据

**证据卡**：
- EV-CONC-005（判据卡）：-O0 vs -O2 汇编对比 + TSan 报告
- EV-CONC-006（对照卡）：atomic 版本无数据竞争（TSan 不报 + 循环内有 load）

**误解**：引用既有 MIS-CONC-003（如果主题匹配）或新建 MIS-CONC-013

### 6.4 技术风险与缓解

| 风险 | 缓解 |
|---|---|
| 无限循环打爆 replay（超时 600s→rc=124→refute） | **有界循环**（iterations < 1000000），绝对不写 while(1) |
| GCC 15.3 可能不消除（太保守） | 用 -O3 或更复杂代码模式；如实标注；用 Clang 对照 |
| 数据竞争运行时结果不确定 | 不用运行时结果做证据，用编译器汇编做证据 |
| TSan 在 MinGW 不可用 | 只用 WSL/Linux 跑 TSan，Windows 侧只做编译期工件对比 |
| 忙等循环可能被完全消除 | reader 返回 g_data + iterations，有 side effect，不会被完全消除 |
| 描述与工件不符 | 写"消除或提升（以工件为准）"，不写死具体优化形态 |

### 6.5 DAL：A（强制人审）

---

## 七、工具链与环境契约

### 编译器（钉到版本粒度）
| 平台 | 编译器 | 版本 | 用途 |
|---|---|---|---|
| Windows | g++ (MinGW) | 15.3.0 | 主要工件 + replay |
| WSL | g++ | 13.3 / 14.2 | Linux 侧工件 + TSan + 跨编译器对照 |
| WSL | riscv64-unknown-elf-g++ | 13.2 | 跨架构 asm 对照（CONC-001） |
| CI | g++ (ubuntu-latest) | 14.2 | CI 验证 |

### 关键约束
- TSan 仅 WSL/Linux 可用（MinGW 链接即失败 `cannot find -ltsan`）；Windows 侧只出 .asm
- TSan 命令必须前缀 `setarch -R`（否则 `FATAL: ThreadSanitizer: unexpected memory mapping`）——WSL 和 CI 都需要
- Windows replay 与 WSL ci_local_precheck **禁止并行**（同写 Examples/*.asm 出假 refute）
- riscv64 工具链用 `__atomic_*` 内建，不用 `<atomic>` 头（bare-metal 无该头）
- .asm 用 `-masm=intel`
- 中文提交用 `git commit -F` UTF-8 文件

### CI 适配
- TSan 在 CI（ubuntu-latest）上可用，但命令必须 `setarch -R` 前缀
- 并发测试控制迭代次数（1e7 次递增约 1-2 秒/线程）
- 有界循环防止 CI 超时

---

## 八、门禁要求（每颗独立跑）

每颗原子完成后必须跑：
1. `python tools/atom_evidence_replay.py --check`（新卡 confirm）
2. `python tools/gate_engine.py --check`（规则数以 `--list` 为准，block=0）
3. `python tools/poison_drill.py`（7/7：P1–P7 全拦截 + 阴性放行；RULE-COVERAGE 单独看）
4. `python -m pytest tests/`（全过）
5. **WSL 侧 replay 跨编译器验证**（断言候选在 Linux 工件中 grep 验证）

全批完成后跑：
6. `python tools/golden_lock.py sync`（无 --accept 参数；用 `check` 查看状态、`show` 查看快照）
7. WSL `python3 tools/ci_local_precheck.py`（31 步全过）
8. consistency / metrics / whitespace

### 规则 checklist（以 `gate_engine.py --list` 为准，不写死数字）
- [ ] MIS-LIBRARY（误解库引用合规——注意：规则名是 MIS-LIBRARY，不是 MIS-ID-FORMAT）
- [ ] EV-SERVES-EXIST（证据卡 serves 的原子必须存在）
- [ ] ATOM-REL-TARGET（relations 指向的原子必须存在）
- [ ] S3-EXPECTED-HARDCODED（注释里不写带双引号的完整取值串）
- [ ] EV-SELF-SATISFIED-ASSERT（不自证断言）
- [ ] EV-FALSIFICATION-QUANT（falsification 有量化取值）
- [ ] EV-TRIVIAL-OBSERVATION（actual 不只有存在性判断）
- [ ] EV-MATRIX-UNBACKED（多编译器有外部留痕）
- [ ] ATOM-STATUS-TRANSITION（status_history 的 level/by 前缀合规）
- [ ] ATOM-DAL-MATCH（dal 与 dal_reviewed_by 匹配）
- [ ] G6 status/dal/status_history 合规
- [ ] 三条铁律：claim 可证伪 / 证据可复算 / 未人审不置 verified

---

## 九、输出格式与编号

### 目录（先创建）
- `atoms/conc/`（新建）
- `evidence/conc/`（新建）
- `goldens/conc/`（新建）
- **misconceptions/ 根目录**（不新建子目录！MIS-CONC-* 扁平命名）

### 编号
- 原子：ATOM-CONC-001 / 002 / 003
- 证据卡：EV-CONC-001..006（每颗 2 张）
- 误解：**先读 MIS-CONC-001..010，引用既有 ID；没有匹配才新建 MIS-CONC-011+**
- 夹具：_atom_fence_vs_atomic.cpp / _atom_sync_cost.cpp / _atom_data_race.cpp

**先做重名检查**：确认这些名字没有被占用。

### 每颗交付物
- `Examples/atoms/_atom_<name>.cpp`（夹具）
- `Examples/atoms/_atom_<name>.asm`（工件，Windows，-masm=intel）
- `Examples/atoms/_atom_<name>.out`（运行输出，含完整原始数据）
- `evidence/conc/EV-CONC-XXX.md`（证据卡 ≥2 张）
- `misconceptions/MIS-CONC-XXX.md`（误解，引用既有或新建）
- `goldens/conc/ATOM-CONC-XXX_draft.md`（原子草稿，draft 状态，自评 ≤4/5）

### 证据卡必填字段（EV_REQUIRED，缺一即 block）

每张证据卡 frontmatter 必须包含：
```yaml
fixture: Examples/atoms/_atom_xxx.cpp        # 夹具路径
command: g++ -O2 ... -o ... && ./...          # 复跑命令（可复制粘贴执行）
artifact: Examples/atoms/_atom_xxx.asm       # 主工件路径（单 artifact，不用复数）
artifact_sha256: <sha256>                     # 工件哈希
artifact_compiler: gcc 15.3 MinGW x86-64 -O2  # 编译器+版本+架构+优化档
actual: |                                    # 确定性输出（逐字匹配）
  line1=...
  line2=...
expected: ...                                # 预期结果
falsification: ...                           # 可证伪条件（必须有量化取值）
matrix:                                      # 多编译器矩阵
  - compiler: gcc 15.3 MinGW
    artifact_sha256: ...
  - compiler: gcc 14.2 WSL
    artifact_sha256: ...
controlled_vars: [优化档, 线程数, 迭代数]     # 控制变量列表
```

> 缺任一字段 → gate block。`actual` 只放确定性行（方向量+常量），不放逐轮纳秒或时序数据。

---

## 十、与 MEM 域的关系

- CONC-001 prerequisites: [PERF-004]（缓存行是内存序的硬件基础）
- CONC-001 contrasts: [UB-GRAY-001]（编译器优化导致的 UB）
- CONC-002 contrasts: [SHARED-002]（锁 vs 原子 RMW）
- CONC-003 contrasts: [UB-GRAY-001]（数据竞争是 UB 的一种）
- CONC-003 builds_on: [NEW-001]（编译器优化的基础）

---

## 十一、红队 can't-miss（13 条，每条挂可机器检测的反例）

| # | 检查项 | 可机器检测的反例 | 来源教训 |
|---|---|---|---|
| 1 | 口径不统一 | 不同原语的代价用不同口径测量 | ALLOC-002 |
| 2 | 消除与失败不可区分 | 计数器异常是"数据竞争"还是"被优化消除" | LEAK-001/002 |
| 3 | 自证断言 | 夹具自定义函数使断言恒真 | UNIQUE-002 |
| 4 | 派生重复读数 | 两个指标是同一 bit 的不同表述 | LEAK-002 |
| 5 | 编译期折叠常量冒充活性观测 | actual 行是编译期常量 | ALLOC-002 |
| 6 | 载体口径不同变 | 对照组和实验组变量在不同存储位置 | PERF-004 |
| 7 | 对照被值类别污染 | 传右值 vs 传左值只反映实参类别 | — |
| 8 | 恒真观测 | actual 只有存在性判断，对关键变量零响应 | SHARED-002 |
| 9 | 基数不一致 | 比值的分子分母来自不同轮/不同排序 | PERF-003 |
| 10 | 与既有证据实质重复 | rglob 查同主题已有原子/证据卡 | LEAK-001 |
| 11 | 断言候选未在 Linux 工件实测 | Windows sha 路径覆盖不到 artifact_assert | EV-MEM-040/041 |
| 12 | 性能数据锚方向不锚倍数 | 同机跨运行可波动 2x+ | PERF-003/004 |
| 13 | 编译器行为不可复现 | g++ 没重排/没消除时如实标注，不编造 | 本批新增 |

---

## 十二、执行顺序

1. **先做 CONC-001**（屏障≠原子类型，地基——展示"为什么需要原子类型"）
2. **再做 CONC-002**（同步原语代价，性能对比，复用 PERF-003/004 方法论 + 双构建宏门控）
3. **最后做 CONC-003**（数据竞争 UB，需要 TSan + 编译器优化分析 + 有界循环）

每颗独立完成夹具→工件→证据卡→误解→草稿→红队→门禁，再开始下一颗。不要三颗并行。

---

## 十三、真实案例锚点（必须写入原子卡的 sources）

### CONC-001
- PostgreSQL commit f8ccab0e9701117a80385bf134ad2ce5c1dc68e8（2025-11-07，REL_18_STABLE，backpatch-through 13）：「Fix generic read and write barriers for Clang」——C11 fence 只为原子访问定义语义，Clang 严格解释下不保证阻止普通访存重排
- 2026-09-10 PostgreSQL hackers 邮件列表：need atomic_signal_fence() AND atomic_thread_fence()
- Boehm "Threads cannot be implemented as a library" PLDI 2005
- Linux Kernel memory-barriers.txt（David Howells、Paul McKenney）

### CONC-002
- sync-shootout benchmark（atomic/mutex/ticket lock 对比数据）
- Travis Downs "A Concurrency Cost Hierarchy"（2020）
- mutex fast path 30-60ns 数据（futex 快速路径）

### CONC-003
- Boehm "Threads cannot be implemented as a library" PLDI 2005
- Boehm & Adve "Foundations of the C++ Concurrency Memory Model" PLDI 2008
- Clang ThreadSanitizer 文档（5-15x 慢、5-10x 内存、零误报）
- TSan WBIA'09 论文

---

## 十四、关键设计决策说明（给 Agent 的背景）

### 为什么 CONC-001 不用"六档内存序指令对照"？
x86 上六档中五档都是 MOV（TSO 免费），只有 seq_cst store 有差异，教学价值有限。而"屏障≠原子类型（屏障位置决定消除）"展示了内存模型的本质——编译器优化是所有架构都有的问题，且本地 100% 可复现（GCC 15.3 / g++-14 / riscv64 13.2 均确定）。

### 为什么 CONC-001 不锚"编译器重排方向"？
x86 把 load 提到 store 之前，RISC-V 没有——方向是脆的。锚"屏障在不在循环体内"和"标志读还在不在"是确定的（两条 x86 工具链逐字一致，riscv 除助记符外结构同形）。PG 案例只作外部锚点（commit hash），不作 artifact 断言（本机无 Clang，无法复现 PG 的 Clang 特定行为）。

### 为什么 CONC-002 要双构建宏门控？
command 里的构建不能含性能打印，否则逐轮纳秒会进入 run_match 的逐字比对，使本卡在任何机器上必然 refute（EV-MEM-045 教训）。BENCH_FULL 宏只给 .out 生成用，actual.run_* 只放方向量与常量。

### 为什么 CONC-003 要用有界循环？
replay 会真的执行 command，无限循环 → 超时 600s → rc=124 → refute，CI 白挂十分钟。有界循环（iterations < 1000000）+ side effect（返回值）既能展示编译器消除，又能保证 replay 终止。

### 为什么不新建 misconceptions/conc/ 子目录？
MIS-CONC-001..010 已存在且是扁平命名（在 misconceptions/ 根目录下）。新建子目录会导致 gate 的 MIS-LIBRARY 或引用解析失败。必须引用既有 ID，或新建 MIS-CONC-011+（扁平命名）。

### 操作提醒：G6 三件先入库
docs/kernel/G6_status_levels.md + tests/test_gate_engine.py + 300 注记仍在工作树，但已入库的 gate_engine.py fix_hint 直接指向该规范。这批开工第一步先入库这三件（提交交 Agent），否则推送后是悬空引用。

---

*本提示词经过独立审查（实测 GCC 15.3 MinGW x86-64 + riscv64-unknown-elf-g++ 13.2），所有 claim 均以本地产物可证伪为前提。v2 因路径错误未落盘，本版直接覆盖 312。核心原则：用确定性的编译器行为做证据，用真实工业案例做锚点，用反直觉发现做教学钩子。*
