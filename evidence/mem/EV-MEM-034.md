---
id: EV-MEM-034
serves: [ATOM-MEM-SHARED-002]
kind: asm
hypothesis: >-
  shared_ptr 的控制块引用计数用**原子 RMW** 修改——汇编层带 `lock` 前缀（MinGW 工件 `lock add` ×3 /
  `lock sub` ×5；gcc-14 工件 `lock add` ×3 / `lock xadd` ×5），且这些指令全部落在控制块符号的作用域
  内（夹具自身**不含**任何原子计数器）；因此多线程**各持副本**时的并发拷贝/销毁是安全的：实测
  4 线程 × 2000 次拷贝后引用计数收敛回 1、被指对象值完好。
controlled_vars: 同一 TU、同一编译器、同一 -O2（另跑 -O0 复核）；唯一变量 = 是否发生引用计数增减（镜像对照见 EV-MEM-035：unique_ptr 工件全文零 lock）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
  sanitizer: [TSan 待 Linux/WSL 侧补跑（MinGW 无 TSan）；本卡以确定性的控制块锚点断言承担主证]
fixture: Examples/_atom_shared_atomic.cpp
command: |
  g++ -std=c++23 -O2 -pthread -S -masm=intel Examples/_atom_shared_atomic.cpp -o Examples/_atom_shared_atomic.asm
  g++ -std=c++23 -O2 -pthread Examples/_atom_shared_atomic.cpp -o build/_replay_shared_atomic.exe && ./build/_replay_shared_atomic.exe
artifact: Examples/_atom_shared_atomic.asm
artifact_sha256: 2f8097b8b0b7e21636c419f19934225093440bbdf57a7396311e41d70d72a97f
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv", "_M_release_last_use_coldEv", "_Sp_counted_base"]}   # 控制块锚点：把 lock 绑到"谁在改计数"上（本工件 9–10 次）
  - {kind: contains_any, texts: ["lock add", "lock sub", "lock xadd", "lock cmpxchg", "lock inc", "lock dec"]}   # 原子 RMW 全形态（MinGW add/sub；Linux add/xadd；weak 提升路径另有 cmpxchg 先例）
  - {kind: contains_any, texts: ["use_count after one copy=", "copies observed="]}    # 活性：观测代码在工件里
expected:
  run: 4 线程 × 2000 次 ⇒ copies observed=8000；单次拷贝后 use_count=2（确定性）；join 后 use_count=1；值 42 完好；sizeof=16；shared_ptr 可拷贝=1、unique_ptr 可拷贝=0
  asm: 控制块符号作用域内出现 lock 前缀原子 RMW；夹具自身无原子计数器（故每条 lock 都可归因控制块）
actual:
  run_cxx23_O2: "threads=4 iterations=2000|sizeof shared_ptr=16|shared_ptr copyable=1|unique_ptr copyable=0|use_count before copies=1|use_count after one copy=2|copies observed=8000|use_count after join=1|value=42"
  run_cxx23_O0: "threads=4 iterations=2000|sizeof shared_ptr=16|shared_ptr copyable=1|unique_ptr copyable=0|use_count before copies=1|use_count after one copy=2|copies observed=8000|use_count after join=1|value=42"
verdict: confirm
falsification: >-
  **主证（指令级，确定性）**：① 若引用计数不是原子的，工件里就不会有 `lock` 前缀 RMW 落在控制块
  符号的作用域内——实测 `lock add`/`lock sub`（MinGW）与 `lock add`/`lock xadd`（gcc-14）全部出现在
  `_Sp_counted_base` / `_Sp_counted_ptr_inplace` 相关函数中；② 夹具**自身不含任何原子计数器**
  （每线程写各自 `std::vector` 槽位、join 后求和），故这些 lock 无法被归因于夹具代码——把 shared_ptr
  换成手工非原子计数后，上述两条断言都会失败。
  **辅助（运行级，烟测）**：`use_count after join=1` 与 `copies observed=8000` **只作烟测**，不作原子性
  证据——join 之后所有副本都已销毁，任何"增减成对配平"的执行（包括几乎无重叠的执行）都会读到 1；
  竞态窗口不保证必定发生重叠。原子性的判定责任完全在指令级主证与标准条文，**本夹具不是竞态检测器**
  （TSan 才是；其缺口已在矩阵 sanitizer 维显式声明）。
  **确定性对照**：`use_count after one copy=2` 把"拷贝会改变引用计数"钉住（定值、直接绑定拷贝动作，
  是运行级能给出的最强观测）。
depth_layer: asm
drill_note: >-
  libstdc++ 的 `_Sp_counted_base::_M_add_ref_copy` / `_M_release` 用原子 RMW 实现引用计数：MinGW 上
  表现为 `lock add DWORD PTR [..], 1` 与 `lock sub DWORD PTR [..], 1`，Linux/gcc-14 上低位计数器走
  `lock xadd`（`_M_release` 一次性取回旧值再判零）。于是"各持副本并发拷贝"安全；但**被指对象**与
  **同一个 shared_ptr 实例**都不受这层保护——前者要靠对象自己的同步，后者要靠外部锁或 C++20 的
  `std::atomic<std::shared_ptr<T>>`。`make_shared` 的控制块 `_Sp_counted_ptr_inplace` 同时承载对象
  与控制块（分配计数见 EV-MEM-033）。
reproduce: 见 command 两行（-pthread 必需：MinGW posix 线程模型），无外部依赖
---

## 为什么这个证据可信

1. **锁指令的归属可判**：夹具按红队要求彻底去掉了自带原子计数器（每线程写各自 vector 槽位），
   于是工件里每一条 `lock` 都可归因 shared_ptr 控制块——这把"编译器到处撒 lock"和"引用计数需要
   原子"两种解释分开了。配套的控制块符号锚点（`_M_releaseEv` / `_Sp_counted_base`）进一步把
   指令绑到"谁在改计数"上。
2. **指令级与运行级分工明确**：原子性由**指令级主证**（LOCK 前缀 + 控制块锚点，确定性、可跨平台
   复算）承担；运行级只作烟测与确定性对照（`use_count after one copy=2`），并**明确声明**竞态
   测试不是竞态检测器——不用"没观察到异常"冒充"永远不出异常"。
3. **镜像对照**：EV-MEM-035 用同优化档、同工具链给出 unique_ptr 工件全文零 `lock`，把"这些原子
   代价是 shared_ptr 特有的"钉死。
4. **有界声称**：本卡只声称"控制块引用计数原子 ⇒ 各持副本并发拷贝/销毁安全"，边界（同一实例、
   被指对象、`use_count()` 近似性）写进「机器口径与边界诚实说明」，避免被读成"shared_ptr 万能安全"。

## 机器口径与边界诚实说明

- **哪些是编译期常量**：`sizeof shart_ptr=16`、`shared_ptr copyable=1`、`unique_ptr copyable=0`
  在工件里是立即数（编译期常量）；`use_count before/after`、`copies observed`、`value` 是运行期读。
- **lock 统计口径**：`grep -oE 'lock[[:space:]]+[a-z]+' <工件> | sort | uniq -c` ⇒ MinGW
  `3 lock add / 5 lock sub`、gcc-14 `3 lock add / 5 lock xadd`。**gcc-14 数字为外部复跑留痕，仓内无
  该工件**（不参与断言，仅作跨编译器形态说明）。
- **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`（replay 机器口径沿 EV-MEM-008 先例），
  `run_cxx23_O0` 由同一会话用 `-O0 -pthread` 复跑填入，两档输出逐字一致。
- **线程安全的边界（本卡最重要的限制）**：控制块计数原子 ⇒ **各持副本**并发拷贝/销毁安全；
  **被指对象本身**不原子，**同一个 shared_ptr 实例**的并发读写也不原子。
- **`use_count()` 在并发下只是近似值**：libstdc++ 实现为一次无锁 32 位读；本卡在 `join()` 之后
  读取，故 1 是确定值，但不要把它当同步原语。
- **TSan 缺口**：并发类卡按 M2 §2 应加 TSan 维；MinGW 无 TSan，本卡在矩阵 `sanitizer` 维显式声明
  该缺口（Linux/WSL 侧待补跑），并以确定性更强的指令级锚点承担主证。
