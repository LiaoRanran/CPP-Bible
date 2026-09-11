---
id: EV-MEM-039
serves: [ATOM-MEM-PERF-003]
kind: run
hypothesis: >-
  小对象分配策略的开销**必须实测，且"谁更快"本身就是平台/实现相关的**：同一夹具、同一工作量
  （10000 次 64 字节分配+释放 × 7 轮取中位数）在 MinGW/libstdc++ 上单调缓冲与池都胜过全局 new
  （约 4.4× 与 2.0×），而在 Linux/glibc 上**三者全部翻转**——全局 new 最快，两种资源反而慢
  （约 1.9× 与 1.37×）。故"池分配器更快"不是可移植结论；可移植的是因果链（回收与否）
  与"必须实测"这条方法论。
controlled_vars: 同一夹具源码、同一读写模式（每次分配写入并读回，volatile 累加防优化）、同一迭代数/轮数/块大小；唯一变量 = 分配策略（global / monotonic / pool）；跨平台对照时**夹具与策略定义不变**，只换平台（Windows/MinGW 与 WSL/Linux）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++ ×2 平台（MinGW 与 glibc/Linux）]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 双平台对照的 Linux 列为**外部复跑留痕**（WSL g++-14，仓内无 Linux 工件）；两列的夹具与断言
  #   完全同一份，故这是"平台差异"而不是"夹具差异"的对照。
  # 断言锚与留痕分离（两轮红队逼出来的纪律）：默认输出**只留跨环境稳定量**（常量 + 活性对照）；
  #   时序数据与**对比结论**都在 `-DBENCH_FULL` 下打印并落 .out（对比结论在 Linux 上会翻转，
  #   见下方双平台表）。
fixture: Examples/_atom_allocator_bench.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_allocator_bench.cpp -o Examples/_atom_allocator_bench.asm
  g++ -std=c++23 -O2 Examples/_atom_allocator_bench.cpp -o build/_replay_alloc_bench.exe && ./build/_replay_alloc_bench.exe
artifact: Examples/_atom_allocator_bench.asm
artifact_sha256: bf7d01826185a168c385702b3cc0c2def902601312052bffaa47c6d4e2c629f9
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["iters_per_round=", "rounds="]}        # 迭代常量（.rodata 格式串）
  - {kind: contains_any, texts: ["block_bytes=", "sink_nonzero="]}      # 块大小 + 观测通路活性对照
expected:
  run: >-
    迭代常量：每轮 10000 次、7 轮、块 64 字节；观测通路活性对照 `sink_nonzero=1`
    （读回累加非零 ⇒ 分配-写入-读回链路真的执行了，未被 -O2 消掉）。
    **绝对耗时、比值、以及"谁更快"的对比结论都不在本卡断言内**——它们在两个平台上会翻转（见下）。
  asm: 迭代常量与活性对照的打印格式串在工件 `.rodata` 中可见（断言不依赖任何 mangled 符号）
actual:
  run_bench_O2: "iters_per_round=10000|rounds=7|block_bytes=64|sink_nonzero=1"
verdict: confirm
falsification: >-
  **真对照（唯一变量 = 分配策略，同一平台内）**：若"小对象分配一定更快"成立，两种资源都该胜过
  全局 new —— 在 MinGW 上确实如此（`both_pools_beat_global=1`），但**同一份夹具在 Linux/glibc 上
  该位为 0**（全局 new 最快）⇒ 该结论被实测证伪为平台相关，而不是被"更强地确认"。
  **双平台实测对照（同夹具，唯一变量 = 平台）**，中位数 ns，10k×7，块 64 B：

  | 平台 / 分配器 | global | monotonic | pool | 最快者 | 资源 vs global |
  |---|---|---|---|---|---|
  | MinGW 15.3.0 / libstdc++（Windows） | 498200 | **112700** | 253900 | monotonic | 快 4.4× / 2.0× |
  | GCC 14.2.0 / glibc（WSL Linux） | **182055** | 349220 | 249782 | **global** | **慢 1.9× / 1.37×** |

  比值 ×1000（Windows）：`monotonic/global=226`、`pool/global=509`、`pool/monotonic=2252`；
  （Linux）：`monotonic/global=1918`、`pool/global=1372`、`pool/monotonic=715`。
  **连排序都翻转**：Windows 是 `monotonic < pool < global`，Linux 是 `global < pool < monotonic`。
  逐轮样本见 `Examples/_atom_allocator_bench.out`（Windows，`-DBENCH_FULL`）。
  **为什么不当断言**：同一次运行里 Windows 的 global max（771200）已是 min（476700）的 1.6 倍、
  monotonic 的 max/min 差 1.56 倍——方差本身就说明这些数携带"当时机器状态"；
  跨平台更是量级翻转。可复现的是**因果链**与**方法论**，不是数字。
  **反例对照（"不该假设"清单）**：`monotonic` 的快建立在**不回收**上（`deallocate` 空操作，
  内存只在资源析构时整体释放）；用在长期反复分配释放的场景会让内存持续增长 ⇒ 速度不是普适优势。
depth_layer: runtime
drill_note: >-
  三个策略的差异只来自**一件事**：每次分配要不要走全局分配器、释放要不要维护可复用结构。
  bump 把释放变成"什么都不做"（代价是不回收）；池维护 free-list（可复用）；全局 new 的代价
  取决于它的实现——glibc 的 tcache 让"全局 new"在 Linux 上极快（本实测里它是最快的那个），
  而 MinGW 上的全局 new 慢得多。**这就是"必须实测"的完整含义**：不仅数字要测，
  连"谁更快"都要测——它在两个平台上给出了相反的答案。
---

# EV-MEM-039 · 小对象分配器：开销与"谁更快"都必须实测

## 双平台实测（同夹具，10k 次/轮 × 7 轮，块 64 B，-O2，取中位数）

| 平台 / 分配器 | global (ns) | monotonic (ns) | pool (ns) | 最快者 |
|---|---|---|---|---|
| MinGW 15.3.0 / libstdc++（Windows，仓内工件） | 498200 | **112700** | 253900 | monotonic |
| GCC 14.2.0 / glibc（WSL Linux，外部复跑留痕） | **182055** | 349220 | 249782 | **global** |

**结论的方向在两平台上相反**：Windows 上两种资源都胜过全局 new；Linux 上全局 new 最快。
这不是矛盾，而是 `glibc` 的 `tcache` 快路径与 MinGW 全局分配器差异的直接体现——
也正说明"池分配器更快"不是可移植结论。

## 三层结论（从稳到不稳）

1. **语义层（跨平台稳定）**：monotonic 的 `deallocate` 是空操作；pool 维护 free-list；
   全局 new 的代价取决于其实现（glibc tcache vs MinGW）。这层不依赖平台。
2. **平台层（需逐平台实测）**：谁更快——Windows 是 `monotonic < pool < global`，
   Linux 是 `global < pool < monotonic`（连排序都不同）。
3. **数值层（跨机器不可复现）**：绝对纳秒与比值——只作留痕。

## 方法论：为什么 run_match 只锚常量与活性对照

`run_match` 是**全量逐字比对**：任何携带"当时机器状态"的读数写进 `actual`，都会让证据卡在
另一台机器上 refute。本卡初版（时序数据入断言）与第二版（对比结论入断言）**都栽过**，
第三版才收敛到"常量 + 活性对照"这一层。这条纪律是**被两次真实失败逼出来的**。

## 完整原始输出（人审裁决 1：不得只留摘要）

**Windows / MinGW 15.3.0 / libstdc++ / -O2 / 10000×7**（`-DBENCH_FULL`，同时落盘 `Examples/_atom_allocator_bench.out`）

| 策略 | 逐轮样本 (ns) | 中位数 | min | max |
|---|---|---|---|---|
| global | 771200, 516000, 496700, 498200, 484200, 476700, 540000 | 498200 | 476700 | 771200 |
| monotonic | 154700, 155000, 99500, 112700, 152800, 106100, 108200 | 112700 | 99500 | 155000 |
| pool | 253900, 251200, 257400, 251300, 251100, 259500, 282200 | 253900 | 251100 | 282200 |

比值 ×1000：`monotonic/global=226`、`pool/global=509`、`pool/monotonic=2252`；`fastest_median=monotonic`。

**Linux / GCC 14.2.0 / glibc / -O2 / 10000×7**（WSL 现场复跑，外部留痕）

| 策略 | 中位数 (ns) | 相对 global |
|---|---|---|
| global | 182055 | 基准（最快） |
| monotonic | 349220 | 慢 1.9× |
| pool | 249782 | 慢 1.37× |

比值 ×1000：`monotonic/global=1918`、`pool/global=1372`、`pool/monotonic=715`；`fastest_median=global`。
**Linux 侧逐轮样本未采集**（复跑时只取了中位数与比值）——如实标注，不编造（铁律 7）。

**断言锚**（`actual` 字段，供 run_match 逐字比对）： `iters_per_round=10000 | rounds=7 | block_bytes=64 | sink_nonzero=1`
—— 锚不扩大（人审裁决 1）；完整原始数据保留在本节与 `.out` 中，**不以摘要代替**。

## 修订记录

- **2026-09-11 · v1 → refute:run_mismatch（时序数据入断言）**
  夹具默认输出 22 行（含每轮纳秒与比值），而 `actual` 只写了 4 行稳定量；replay 报
  `refute:run_mismatch`（期望 4 行 vs 实际 22 行），且时序数据每次运行都变。
- **2026-09-11 · v2 → 红队阻断 1（中位数基数不一致）**
  夹具用**原始插入序**的第 4 个样本参与"谁更快"的比较，而打印的 `_median_ns` 是**排序后**的中位数
  ⇒ 卡里列出的中位数与卡里引用的比值不是同一基数（读者永远算不出）。已改为 `run()` 回传排序后中位数，
  两者共用同一基数。
- **2026-09-11 · v3 → 红队高级 6（"稳定层"实为平台相关）**
  v2 把 `both_pools_beat_global` 等对比结论当"跨机器稳定量"放进断言锚；在 WSL/Linux 实测
  **三位全部翻转为 0** ⇒ 该结论是平台相关的，已移入 `-DBENCH_FULL` 留痕层。断言锚最终只保留
  常量与活性对照。夹具两次改动后**均重生成 asm 工件并更换 `artifact_sha256`**
  （`6cad79bf…` → `f9b582bc…` → `bf7d0182…`，遵守"工件与断言同代"纪律）。
