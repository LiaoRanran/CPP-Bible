---
id: EV-MEM-040
serves: [ATOM-MEM-ALLOC-002]
kind: run
hypothesis: >-
  **统一口径**下（元数据 := 为管理这批分配、分配器自身占用且不承载用户数据的全部字节，
  逐项拆为 struct_bytes + bookkeeping_bytes），三种分配策略的真实开销排序是
  **arena 32 B < bitmap 181 B ≪ pool 8056 B**（n=1000），n=8000 时为
  **arena 32 B < bitmap 1056 B ≪ pool 64056 B** —— 即 pool 的 free-list 堆数组
  （8 B/块）使它的 bookkeeping **远超** bitmap 的位图（1 bit/块）；
  且 pool 与 bitmap 的元数据**都随块数增长**（7.95× 与 5.83× @8× 规模），
  arena 则恒为 32 B（它不维护任何 bookkeeping）。
controlled_vars: 同一夹具、同一请求大小（24 B）、同一定长块（32 B）、同一 workload 序列（分配 n 次 → 单块释放 → 全量重置 → 再分配 n 次）；唯一变量 = 分配策略与被扫规模（n ∈ {1000, 8000}）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 跨平台确定性对照（**外部复跑留痕**，可核对锚）：
  #   `g++-14 -std=c++23 -O2 Examples/atoms/_atom_alloc_strategies.cpp` ⇒ 输出与 Windows 侧逐字相同
  # 本卡数据为**统一口径重写后的最终值**（v1 的 "pool 元数据 32 B、最省" 系漏算 free-list 堆数组，
  #   已在 v2 修正，见文末修订记录）。
fixture: Examples/atoms/_atom_alloc_strategies.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_alloc_strategies.cpp -o Examples/atoms/_atom_alloc_strategies.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_alloc_strategies.cpp -o build/_replay_alloc_strategies.exe && ./build/_replay_alloc_strategies.exe
artifact: Examples/atoms/_atom_alloc_strategies.asm
artifact_sha256: 4f482fdcdb7ec335d833422dec2a9b2cce85d0e7a45b9550c1e176308c415510
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["%s_meta_total_bytes=", "%s_meta_bookkeeping_bytes="]}
  - {kind: contains_any, texts: ["%s_meta_struct_bytes=", "scale_ratio="]}
  # 注：标签由 `report(tag, …)` 运行时拼接 ⇒ 工件里存在的是**格式串模板**（`%s_meta_…`）而非
  #   `arena_n1_meta_…` 这类具体标签。该断言在 Linux 侧（跨编译器路径）曾因写成具体标签而 refute，
  #   是"断言里的字面量必须来自工件实测"的又一实例（同 EV-MEM-038 的 heap_at_len%zu= 教训）。
expected:
  run: >-
    arena：struct 32 B、bookkeeping 0、total 32 B（n=1000 与 n=8000 **同为 32 B**——无 bookkeeping 的
    直接后果）；pool：struct 56 B、bookkeeping 8000 B（n=1000）/ 64000 B（n=8000）、total 8056 / 64056 B；
    bitmap：struct 56 B、bookkeeping 125 B / 1000 B、total 181 / 1056 B。
    三策略的 `*_served_second` 均为 1000 / 8000（workload 真实执行且 reset 语义统一）。
  asm: 元数据的打印格式串在工件 `.rdata` 中可见（断言不依赖任何 mangle 符号）
actual:
  run_final_O2: "req_bytes=24|block_bytes=32|internal_frag_per_block=8|scale_n1=1000|scale_n2=8000|arena_single_free_supported=0|arena_n1_served_first=1000|arena_n1_served_second=1000|arena_n1_peak_after_first=24000|arena_n1_meta_struct_bytes=32|arena_n1_meta_bookkeeping_bytes=0|arena_n1_meta_total_bytes=32|arena_n2_served_first=8000|arena_n2_served_second=8000|arena_n2_peak_after_first=192000|arena_n2_meta_struct_bytes=32|arena_n2_meta_bookkeeping_bytes=0|arena_n2_meta_total_bytes=32|pool_n1_served_first=1000|pool_n1_served_second=1000|pool_n1_peak_after_first=32000|pool_n1_meta_struct_bytes=56|pool_n1_meta_bookkeeping_bytes=8000|pool_n1_meta_total_bytes=8056|pool_n2_served_first=8000|pool_n2_served_second=8000|pool_n2_peak_after_first=256000|pool_n2_meta_struct_bytes=56|pool_n2_meta_bookkeeping_bytes=64000|pool_n2_meta_total_bytes=64056|bitmap_n1_served_first=1000|bitmap_n1_served_second=1000|bitmap_n1_peak_after_first=32000|bitmap_n1_meta_struct_bytes=56|bitmap_n1_meta_bookkeeping_bytes=125|bitmap_n1_meta_total_bytes=181|bitmap_n2_served_first=8000|bitmap_n2_served_second=8000|bitmap_n2_peak_after_first=256000|bitmap_n2_meta_struct_bytes=56|bitmap_n2_meta_bookkeeping_bytes=1000|bitmap_n2_meta_total_bytes=1056|scale_ratio=8"
verdict: confirm
falsification: >-
  **真对照（唯一变量 = 策略，同一口径）**：若 pool 的元数据真的只有"容器头"那么大，
  它的 bookkeeping 应接近 0 —— 实测 **8000 B**（= 1000 块 × 8 B 指针），
  且 n=8000 时为 **64000 B**（8× 规模 → 8× bookkeeping）。
  反方向：若 bitmap 的元数据不随块数变（如 O(1)），n=8000 时应仍为 181 B —— 实测 **1056 B**。
  **活性对照（证明读数是算出来的，不是写死的常量）**：arena 的 total 在 n=1000 与 n=8000 下
  **同为 32 B**（因它不维护 bookkeeping）；pool 与 bitmap 的 total 则随规模变化
  （8056→64056、181→1056）。若这些数是编译期常量，两组规模必然相同。
  **可复算**：pool 的 bookkeeping = 块数 × `sizeof(void*)`（1000×8=8000、8000×8=64000 ✅）；
  bitmap 的 = `ceil(块数/8)`（ceil(1000/8)=125、ceil(8000/8)=1000 ✅）。
depth_layer: runtime
drill_note: >-
  本卡的教学结论是**元数据开销与"是否支持单块释放"绑定**：arena 用**放弃单块释放**换来零 bookkeeping
  （32 B 恒定）；pool 用**最大 bookkeeping**（8 B/块）换来 O(1) 分配与回收；bitmap 居中
  （1 bit/块 = 0.125 B/块），代价是分配时需要扫描位图。
  另一条同样重要的教训来自本卡的**修订史**：v1 的三个 `meta()` 口径不一致（分别算标量、容器头、
  数据结构本体），导致"pool 最省"这一**方向相反**的结论 —— 口径不统一的量化比没有量化更危险。
---

# EV-MEM-040 · 三种分配策略的元数据与内部碎片（统一口径，n=1000 / 8000）

## 统一口径

元数据 := **为管理这批分配，分配器自身占用且不承载用户数据的全部字节**，
拆为 `struct_bytes`（容器头 + 标量计数器）+ `bookkeeping_bytes`（bookkeeping 数组的堆内存）。

## 观测（Windows/MinGW 与 WSL/g++-14 逐字相同）

| 策略 | struct (B) | bookkeeping (B) | **total n=1000** | **total n=8000** |
|---|---|---|---|---|
| arena | 32 | 0 | **32** | **32** |
| pool | 56 | 8000 / 64000 | **8056** | **64056** |
| bitmap | 56 | 125 / 1000 | **181** | **1056** |

**关键反转**：pool 的元数据 **8056 B ≫ bitmap 181 B**（n=1000）——
free-list 每个块一个指针（8 B/块）**远大于**位图的 1 bit/块（0.125 B/块）。
因此 pool **不是**元数据最小的策略；"元数据换灵活性"的正确排序是
**arena（零 bookkeeping，但不能单块释放）< bitmap < pool**。

## 前提（不可省略）

1. **arena 的"零内部碎片 / 32 B 元数据"只在"批量申请 + 整体释放"模式下成立**：
   夹具的 `Arena::release_all()` 只能重置偏移（`arena_single_free_supported=0` 如实声明），
   **中途释放单块时 bump 指针无法回退 ⇒ 跳过处不可复用**（MIS-MEM-030）。
2. 本卡请求尺寸固定 24 B 且**不做对齐处理**（步进恰为 24、偏移 ≡8 mod 16）；
   真实分配器把 24 取整到 32 的首要理由正是对齐与 size-class —— 而 pool/bitmap 的
   内部碎片 8 B（`internal_frag_per_block=8` × 块数）正是这一取整的代价。
3. 时间维度（分配/回收延迟）**不在本卡**（时序数据跨机器不可复现，见 ATOM-MEM-PERF-003）。

## 修订记录

- **2026-09-12 · v1 → v2（红队 B1：元数据口径不一致，结论方向反转）**
  v1 的三个 `meta()` 分别只算 `sizeof(size_t)`（arena，连容器头都不算）、
  `sizeof(free_list)+8`（pool，**漏掉 free-list 的堆数组**）、`bits.size()+8`（bitmap，含本体）
  ⇒ 得出"pool 元数据 32 B、最省"的**方向相反**结论。v2 统一为本文口径、逐项拆解，
  **方向反转为 pool ≫ bitmap**。同时按红队 H4 加"两规模 × 三策略"活性对照、
  按 H5 把 workload 改为真实执行（`*_served_first/second`）、按 H2 把断言从"夹具自写标签"
  扩展到**含数值的读数标签**、把 H6 的对齐前提写入上面第 2 条。
  夹具两次改动均重编译并更换 `artifact_sha256`（`4a853c66…` → `467b69bd…` → **`4f482fdc…`**）。
