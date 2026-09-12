# 第六批 CONC 域首批原子生产 — 执行提示词

> 投喂给执行 Agent。先完整读取 312 提示词，再按本提示词的执行顺序推进。
> 核心纪律：每颗独立完成全流程再开始下一颗；不压缩红队；未人审不置 verified；提交交 Agent（本机不 push）。

---

## 〇、前置：G6 三件入库（第一步，必须先做）

docs/kernel/G6_status_levels.md + tests/test_gate_engine.py + 300 注记仍在工作树，但已入库的 gate_engine.py fix_hint 直接指向该规范——不入库就是悬空引用。

**动作**：
1. `git add docs/kernel/G6_status_levels.md tests/test_gate_engine.py References/architecture_架构演进/300_四级状态自动化体系_从人审驱动到机器自治.md`
2. `git commit -m "G6: 四级状态规范+回归测试+300注记入库（修复悬空引用）"`
3. 提交后 push（你负责 push，本机不动）

---

## 一、读取 312 提示词

完整读取：`References/architecture_架构演进/312_第六批CONC域首批原子生产提示词.md`（v3.1，32KB）

重点消化：
- §一 13 条铁律（含本批新增：编译器行为钉版本、描述与工件一致、并发用编译器行为做证据）
- §二 G6 四级状态契约（status_history 用 `{level,at,by}`，by 带前缀）
- §四~六 三颗原子的完整实验设计（含夹具代码骨架、断言锚写法、终止性保证）
- §七 工具链（TSan 必须 `setarch -R`；riscv64 用 `__atomic_*` 内建）
- §八 门禁命令（golden_lock.py sync；poison 7/7；规则数以 --list 为准）
- §九 证据卡必填字段（EV_REQUIRED，缺一即 block）
- §十一 13 条 can't-miss

---

## 二、执行顺序（严格串行，不并行）

### 阶段 1：CONC-001 屏障≠原子类型（DAL B，强制人审）

**夹具**：`Examples/atoms/_atom_fence_vs_atomic.cpp`
- 六个 noinline 函数（writer_plain/signal_fence/thread_fence + spin_plain/spin_with_fence/spin_volatile）
- main() 先 `g_b=1` 再调 spin（终止性保证）
- spin_volatile 加 `bound=1000000` 双重保险
- 用 `__atomic_*` 内建，不用 `<atomic>` 头（riscv64 bare-metal 兼容）

**工件**（三平台）：
- Windows g++ 15.3 MinGW -O2 -masm=intel .asm（主工件）
- WSL g++-14 -O2 -masm=intel .asm（跨编译器）
- WSL riscv64-unknown-elf-g++ 13.2 -O2 .asm（跨架构）

**断言锚**（必须在 Linux 工件中 grep 验证）：
- spin_plain/spin_with_fence 函数体区间内 absent `g_b` 符号引用
- spin_volatile 函数体区间内 contains_any `g_b`
- writer_thread_fence 函数体区间内 contains_any 屏障指令
- writer_signal_fence 函数体区间内 absent 屏障指令

**证据卡**：EV-CONC-001（判据卡）+ EV-CONC-002（移植性卡，x86 vs RISC-V + PG f8ccab0e 外部锚点）

**误解**：先读 MIS-CONC-001..010，引用匹配的；没有才新建 MIS-CONC-011

**红队**：独立子 agent，两段式盲读（先读夹具/工件不读卡）

---

### 阶段 2：CONC-002 同步原语代价分层（DAL C，豁免须人签）

**夹具**：`Examples/atoms/_atom_sync_cost.cpp`
- 四种实现：mutex / fetch_add / CAS 自旋锁 / atomic+退避
- **双构建同源宏门控**：`#ifdef BENCH_FULL` 包裹性能测试
- actual 只放方向量（`fetch_add_1thread_fastest=1`、`cas_4thread_degrades=1` 或 `insufficient_cores=1`）
- 逐轮纳秒放 .out，不入断言锚

**断言锚**：
- fetch_add 工件 contains_any `lock xadd`/`lock add`
- CAS 工件 contains_any `lock cmpxchg`
- mutex 工件 contains_any `__gthread_mutex_lock`/`pthread_mutex_lock`
- 性能卡 `contains_any: ["cas_4thread_degrades=1", "insufficient_cores=1"]`

**证据卡**：EV-CONC-003（指令级对比卡）+ EV-CONC-004（性能方向卡）

**误解**：引用 MIS-CONC-002 或新建 MIS-CONC-012

---

### 阶段 3：CONC-003 数据竞争的编译器优化（DAL A，强制人审）

**夹具**：`Examples/atoms/_atom_data_race.cpp`
- reader_noatomic（有界循环 `iterations < 1000000`）+ reader_atomic
- **绝对不写无限循环**（replay 超时 600s→rc=124→refute）
- side effect 返回值防止完全消除

**工件**：
- -O2 .asm 作 artifact（主工件，锚消除/提升）
- -O0 只在证据卡正文留痕（单 artifact 原则）
- TSan .out（WSL `setarch -R g++ -O1 -fsanitize=thread`）

**断言锚**：
- reader_noatomic -O2 函数体区间内 absent `g_flag` 符号引用
- reader_atomic -O2 函数体区间内 contains_any atomic load
- TSan 输出 contains_any "data race"（非原子版）/ absent（原子版）
- `expected_sanitizer: [thread]`

**证据卡**：EV-CONC-005（判据卡）+ EV-CONC-006（对照卡）

**误解**：引用 MIS-CONC-003 或新建 MIS-CONC-013

---

## 三、每颗的完整流程（缺一不可）

```
夹具编写 → 三平台编译 → 工件生成 → sha256 锚定
  → 证据卡 ×2（EV_REQUIRED 字段全填）
  → 误解（引用既有或新建）
  → 原子草稿（goldens/conc/，draft，自评 ≤4/5）
  → 红队（独立子 agent，两段式盲读，修复循环 ≤2 轮）
  → 门禁（replay/gate/poison/pytest/WSL 跨编译器验证）
  → 下一颗
```

**全批完成后**：
1. `python tools/golden_lock.py sync`
2. WSL `python3 tools/ci_local_precheck.py`（31 步全过）
3. consistency / metrics / whitespace
4. 质检报告 `docs/G5_CONC_batch1_quality_inspection.md`

---

## 四、铁律（违反即返工）

1. claim/actual 不编造；断言锚只锚常量+活性对照
2. 夹具不重载 operator new/delete
3. 断言候选必须在 Linux 工件中 grep 验证
4. 红队两段式盲读，修复循环 ≤2 轮
5. 未人审不置 verified、不原子化、不 commit
6. 性能数据锚方向不锚倍数
7. 同一实验多对象同一口径测量
8. 并发实验用编译器行为做证据，不用运行时调度
9. 编译器行为钉到版本粒度
10. 描述与工件一致（写"消除或提升（以工件为准）"）
11. 有界循环防止 replay 超时
12. 双构建同源宏门控
13. misconceptions/MIS-CONC-* 扁平命名，不新建子目录

---

## 五、提交与推送

- 每颗完成后不单独 commit（攒全批）
- 全批门禁全绿后：`git add` 只挑本批产物（atoms/conc/、evidence/conc/、goldens/conc/、Examples/_atom_*、misconceptions/MIS-CONC-*、质检报告）
- `git commit -F` UTF-8 提交信息
- **push 由你执行**（本机不动）
- 不含 References/（铁律）

---

## 六、遇到问题怎么办

- 夹具编译失败 → 读报错，修夹具，重编译，换 sha，同步卡
- replay refute → 先看是 artifact_assert_failed 还是 run_mismatch 还是 sanitizer；artifact_assert 先在 Linux 工件 grep 验证断言字面量
- gate block → 读 fix_hint，按提示修；规则名以 `--list` 为准
- 红队抓出方向性错误 → 不硬扛，按红队建议改 claim/夹具，记录修订史
- 上下文耗尽 → 把所有数据（sha、读数、红队处置）写入 2026-09-12.md，下一窗口续作，不做未完成的原子化

---

*开始前先确认：G6 三件已入库、312 已读完、目录 atoms/conc/ evidence/conc/ goldens/conc/ 已创建、MIS-CONC-001..010 已读。*
