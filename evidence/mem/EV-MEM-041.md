---
id: EV-MEM-041
serves: [ATOM-MEM-ALLOC-002]
kind: run
hypothesis: >-
  **pool 与 bitmap 的 bookkeeping 都随块数线性增长**，差异只在**单位粒度**：
  pool 每块一个指针（8 B/块）、bitmap 每块一位（1/8 B/块）⇒ **系数约 64×**
  ——这直接决定了两者在同一规模下的绝对开销（n=8000：pool 64000 B vs bitmap 1000 B）。
  而 arena 的元数据**不随规模变**（恒 32 B），因为**它放弃单块释放、不维护任何 bookkeeping**。
  教学点因此不是"谁线性谁不线性"，而是"**bookkeeping 的单位粒度决定增长系数**"。
controlled_vars: 同一夹具、同一块大小（32 B）、同一 workload 序列；唯一变量 = 块数规模（1000 vs 8000），三策略在同一口径（struct_bytes + bookkeeping_bytes）下并列对照
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 跨平台确定性对照（**外部复跑留痕**，可核对锚）：
  #   `g++-14 -std=c++23 -O2 Examples/atoms/_atom_alloc_strategies.cpp` ⇒ 输出与 Windows 侧逐字相同
fixture: Examples/atoms/_atom_alloc_strategies.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_alloc_strategies.cpp -o Examples/atoms/_atom_alloc_strategies.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_alloc_strategies.cpp -o build/_replay_alloc_strategies.exe && ./build/_replay_alloc_strategies.exe
artifact: Examples/atoms/_atom_alloc_strategies.asm
artifact_sha256: 4f482fdcdb7ec335d833422dec2a9b2cce85d0e7a45b9550c1e176308c415510
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["%s_meta_bookkeeping_bytes=", "%s_meta_total_bytes="]}
  - {kind: contains_any, texts: ["%s_meta_struct_bytes=", "scale_n2="]}
  # 同 EV-MEM-040：标签为运行时拼接，工件中是格式串模板（`%s_meta_…`）。
expected:
  run: >-
    8× 规模（1000 → 8000）下：pool 的 bookkeeping 8000 → **64000 B**（**8×**，即严格线性）、
    bitmap 的 bookkeeping 125 → **1000 B**（**8×**，同样线性）、arena 的 total **32 → 32 B**
    （不变，因为它没有 bookkeeping）。
    绝对量级：同规模下 pool 的 bookkeeping 是 bitmap 的 **64 倍**（n=8000：64000 vs 1000）——
    这个 64× 正是"8 B/块 vs 1 bit/块"的粒度比。
  asm: 两组 bookkeeping 与 arena total 的打印格式串在工件 `.rdata` 中可见
actual:
  run_final_O2: "req_bytes=24|block_bytes=32|internal_frag_per_block=8|scale_n1=1000|scale_n2=8000|arena_single_free_supported=0|arena_n1_served_first=1000|arena_n1_served_second=1000|arena_n1_peak_after_first=24000|arena_n1_meta_struct_bytes=32|arena_n1_meta_bookkeeping_bytes=0|arena_n1_meta_total_bytes=32|arena_n2_served_first=8000|arena_n2_served_second=8000|arena_n2_peak_after_first=192000|arena_n2_meta_struct_bytes=32|arena_n2_meta_bookkeeping_bytes=0|arena_n2_meta_total_bytes=32|pool_n1_served_first=1000|pool_n1_served_second=1000|pool_n1_peak_after_first=32000|pool_n1_meta_struct_bytes=56|pool_n1_meta_bookkeeping_bytes=8000|pool_n1_meta_total_bytes=8056|pool_n2_served_first=8000|pool_n2_served_second=8000|pool_n2_peak_after_first=256000|pool_n2_meta_struct_bytes=56|pool_n2_meta_bookkeeping_bytes=64000|pool_n2_meta_total_bytes=64056|bitmap_n1_served_first=1000|bitmap_n1_served_second=1000|bitmap_n1_peak_after_first=32000|bitmap_n1_meta_struct_bytes=56|bitmap_n1_meta_bookkeeping_bytes=125|bitmap_n1_meta_total_bytes=181|bitmap_n2_served_first=8000|bitmap_n2_served_second=8000|bitmap_n2_peak_after_first=256000|bitmap_n2_meta_struct_bytes=56|bitmap_n2_meta_bookkeeping_bytes=1000|bitmap_n2_meta_total_bytes=1056|scale_ratio=8"
verdict: confirm
falsification: >-
  **真对照（唯一变量 = 规模）**：若 pool 的 bookkeeping 是常量（O(1)），8× 规模下它应仍为 8000 B
  —— 实测 **64000 B**（8×）；若 bitmap 的也是常量，应仍为 125 B —— 实测 **1000 B**（8×）。
  **反方向（"谁不线性"的对照）**：arena 的 total 在 n=1000 与 n=8000 下**同为 32 B**
  —— 它不是"增长得慢"，而是**不增长**（`bookkeeping_bytes=0`），因为夹具的 Arena
  **没有单块释放接口**（`arena_single_free_supported=0` 如实声明）⇒ 无需任何 bookkeeping。
  **可复算**：pool = 块数 × `sizeof(void*)`（8000×8 = 64000 ✅）；bitmap = `ceil(块数/8)`
  （ceil(8000/8) = 1000 ✅）；系数比 = 8 ÷ 0.125 = **64** ✅ 与实测 64000/1000 = 64 吻合。
  **活性对照（证明读数是算出来的）**：三档并列（arena 32→32、pool 8056→64056、
  bitmap 181→1056）——若这些数是编译期写死的常量，三档不可能同时呈现"两变一不变"的模式。
depth_layer: runtime
drill_note: >-
  本卡的结论可以用一个比值记住：**pool 的 bookkeeping 是 bitmap 的 64 倍**（同规模），
  因为维护"每块一个可复用指针"比维护"每块一位占用标记"贵 64 倍——而 bitmap 用这一位
  换到的是"分配时需要扫描"（本夹具的 alloc 从 bit 0 起扫）。
  另一条结论更容易被忽略：**arena 的元数据恒定不是因为"它更高效"，而是因为它放弃了单块释放**。
  三条策略因此构成一个清晰的三段式：不回收（零 bookkeeping）→ 位图回收（0.125 B/块）→
  指针链表回收（8 B/块）。
---

# EV-MEM-041 · bookkeeping 的单位粒度决定增长系数（同样是 8×，差 64 倍）

## 观测（8× 规模，三策略并列）

| 策略 | bookkeeping n1 | bookkeeping n2 | 倍数 | 单位粒度 | total n1 → n2 |
|---|---|---|---|---|---|
| arena | 0 | 0 | — | **无**（不回收单块） | 32 → **32**（恒定） |
| pool | 8000 | **64000** | **8×** | 8 B/块（可复用指针） | 8056 → 64056 |
| bitmap | 125 | **1000** | **8×** | 0.125 B/块（1 bit） | 181 → 1056 |

**系数差**：8 ÷ 0.125 = **64×**（与实测 64000/1000 = 64 吻合）。

## 结论（本卡与 EV-MEM-040 的分工）

- **040** 回答"同一规模下三种策略怎么权衡"（横向）；
- **041** 回答"元数据**随规模**怎么变"（纵向）：**pool 与 bitmap 同阶线性，差异只在系数**；
  arena 不增长，因为它**不维护 bookkeeping**（代价是放弃单块释放）。
- ❌ **旧表述已删除**（v1 曾写"线性增长是 bitmap 与 pool 的关键差异"）——实测证伪：
  pool 同样线性（8000 → 64000，7.95~8×）。

## 前提与边界

1. 只测两个规模点（1000 / 8000）；"线性"由**两点比 + 逐项复算**（块数 × 单位粒度）支撑，
   未做多点回归；
2. 元数据口径与 EV-MEM-040 一致（`struct_bytes` + `bookkeeping_bytes`）；
3. 分配侧的时间代价（bitmap 每次 alloc 需扫位图）**不在本卡**（时序数据不入锚）。

## 修订记录

- **2026-09-12 · v1 → v2（红队 B1 的连带修正）**
  v1 的数据（133 / 1008 / 7578‰）建立在**口径不一致**的 `meta()` 上（pool 漏算 free-list 堆数组），
  并据此写出"线性增长是 bitmap 与 pool 的关键差异"——**该结论已被统一口径后的实测证伪**：
  pool 的 bookkeeping 同样随块数线性增长（8000 → 64000，**8×**），只是系数比 bitmap 大 64 倍。
  v2 按最终数据整体重写（新 sha `4f482fdc…`，旧 `4a853c66…` 作废），claim 改为
  "**单位粒度决定增长系数**"，并补三档活性对照（arena 恒定 / pool、bitmap 同阶线性）。
