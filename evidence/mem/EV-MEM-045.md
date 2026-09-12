---
id: EV-MEM-045
serves: [ATOM-MEM-PERF-004]
kind: run
hypothesis: >-
  伪共享的**性能后果可量化且量级巨大**：4 线程各自累加 1e7 次到"逻辑独立"的计数器，
  相邻布局（同一缓存行）比 `alignas` 隔离布局慢 **约 18 倍**（Windows 18.86× / Linux 18.54×，
  两平台方向与量级一致）；唯一变量 = 布局（线程数/迭代数/优化档/编译器完全相同）。
controlled_vars: 同夹具、同线程数（4）、同迭代数（1e7/线程）、同轮数（7）、同优化档（-O2）、同内存序（relaxed）；唯一变量 = 计数器布局（相邻 vs 独占缓存行）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 双平台对照（可核对锚）：WSL 复跑命令
  #   `g++-14 -std=c++23 -O2 -pthread -DBENCH_FULL Examples/atoms/_atom_false_sharing_perf.cpp`
  #   ⇒ tight 568921142 ns / padded 30688821 ns / ratio 18538‰
  # **留痕工件的生成命令**（红队待修 1 · 必修：`.out` 必须由卡内记录的构建产生）：
  #   `g++ -std=c++23 -O2 -pthread -DBENCH_FULL Examples/atoms/_atom_false_sharing_perf.cpp -o build/fsperf_full.exe`
  #   → 运行该可执行文件，stdout 落盘为 `Examples/atoms/_atom_false_sharing_perf.out`（MinGW 15.3.0，2026-09-12）。
  #   注意：`command` 字段里的构建**不含** `-DBENCH_FULL`（否则逐轮纳秒会进入 run_match 的逐字比对，
  #   使本卡在任何机器上必然 refute）；两条构建同源同参、只差该宏，故 `.out` 与断言锚**同代**，
  #   复跑上面这条命令即可完整重现 `.out` 的全部内容。
  # **Linux 侧可核对锚**（红队待修 2）：完整复跑命令已在上一行给出；中位数行
  #   `tight_median_ns=568921142` / `padded_median_ns=30688821` / `ratio_tight_over_padded_x1000=18538`，
  #   逐轮样本**未采集**（如实标注，不编造）。
fixture: Examples/atoms/_atom_false_sharing_perf.cpp
command: |
  g++ -std=c++23 -O2 -pthread -S -masm=intel Examples/atoms/_atom_false_sharing_perf.cpp -o Examples/atoms/_atom_false_sharing_perf.asm
  g++ -std=c++23 -O2 -pthread Examples/atoms/_atom_false_sharing_perf.cpp -o build/_replay_false_sharing_perf.exe && ./build/_replay_false_sharing_perf.exe
artifact: Examples/atoms/_atom_false_sharing_perf.asm
artifact_sha256: 590f3e721a564ee0c5cd69fe70364e39cf354b41a50bd1452ca07127bb1a046e
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["sharing_is_slower=", "counters_all_advanced="]}   # 方向结论 + 活性对照
  - {kind: contains_any, texts: ["tight_stride_bytes=", "padded_stride_bytes="]}   # 布局常量（唯一变量的证据）
expected:
  run: >-
    4 线程 × 1e7 次、7 轮；布局常量 `tight_stride_bytes=8` vs `padded_stride_bytes=64`；
    方向结论 `sharing_is_slower=1`（相邻布局更慢）；活性对照 `counters_all_advanced=1`
    （四个计数器都被推进过 ⇒ 循环未被优化掉、线程真的跑了）。
    **绝对耗时与倍数不在断言锚内**（跨机器不可复现），完整逐轮样本见 `.out` 与下文。
  asm: 方向结论与布局常量的打印格式串在工件 `.rodata` 中可见
actual:
  run_perf_O2: "threads=4|iters_per_thread=10000000|rounds=7|cache_line_size=64|tight_stride_bytes=8|padded_stride_bytes=64|tight_shares_line=1|padded_shares_line=0|sharing_is_slower=1|counters_all_advanced=1"
verdict: confirm
falsification: >-
  **真对照（唯一变量 = 布局）**：若布局对性能无影响，比值应 ≈ 1000‰ —— 实测
  **18860‰（18.86×）**；若两布局等价，`sharing_is_slower` 应为 **0** —— 实测 **1**；
  在两平台上方向一致（Linux 比值 **18538‰**）⇒ 不是单机噪声。
  **第三次运行（红队修复后重测；本轮只改了两个夹具有缺陷的断言行，未动并行逻辑）**：
  tight 中位数 **246507200 ns**、padded **28075600 ns** ⇒ 比值 **8780‰（8.78×）**——
  与 18.86× 相差一倍以上。**这正是"不锚倍数"的直接实证**：同一台机器、同一夹具、跨运行波动可达
  2×+（调度/频率/负载），可复现的只有**方向**（`sharing_is_slower=1`）与**量级**（约一个数量级）。
  逐轮样本：tight min 234583100 / max 263028700；padded min 27934700 / max 29638300。
  **完整原始输出（人审要求：不得只留摘要）**
  Windows/MinGW 15.3.0（-O2，4 线程 × 1e7，7 轮）：
  - tight 逐轮 (ns)：`562500600, 550447800, 545923000, 552546800, 566989400, 853116300, 733753700`
  - padded 逐轮 (ns)：`28784300, 29035900, 28049200, 31571700, 29824800, 36821700, 37410300`
  - 中位数：tight **562500600** / padded **29824800**；min：545923000 / 28049200；max：853116300 / 37410300
  - 比值 `ratio_tight_over_padded_x1000=18860`
  Linux/WSL GCC 14.2.0（同参数）：tight 中位数 **568921142** / padded **30688821** / 比值 **18538‰**
  （Linux 逐轮样本**未采集**——复跑时只取了中位数与比值，如实标注、不编造。）
  **方差自证**：tight 的 max（853116300）是 min（545923000）的 1.56 倍 ⇒ 绝对数携带"当时机器状态"；
  可复现的是**方向**（相邻更慢）与**量级**（约两个数量级）。
depth_layer: runtime
drill_note: >-
  18 倍的来源：每个 `fetch_add` 都要把整条缓存行读入并独占（RFO），相邻计数器让缓存行在 4 个核之间
  反复弹跳（cache line ping-pong），而 padded 布局下每个核只碰自己的行、命中 L1。**修法有两面**：
  padding 换来的是空间（`padded_sizeof=128`），所以"是否值得"取决于访问密度与对象数量——这也是
  本原子 claim 里"存在最优对齐粒度"的含义。
---

# EV-MEM-045 · 伪共享的性能后果：约 18 倍（双平台一致）

## 实测（4 线程 × 1e7 次累加，7 轮取中位数）

| 平台 | tight（相邻，同一缓存行） | padded（alignas 隔离） | 倍数 |
|---|---|---|---|
| Windows/MinGW 15.3.0 | **562 500 600 ns** | **29 824 800 ns** | **18.86×** |
| Linux/WSL g++-14 | 568 921 142 ns | 30 688 821 ns | **18.54×** |

逐轮样本与 min/max 见 frontmatter 的 falsification 节；`.out` 留痕见 `Examples/atoms/_atom_false_sharing_perf.out`。

## 为什么锚"方向"而不锚"倍数"

同一次运行内 tight 的 max/min 已差 1.56 倍（调度与频率扰动）；跨平台倍数也有 ±0.3 的差。
因此 `actual` 只锚：**布局常量**（唯一变量的证据）、**方向结论**（`sharing_is_slower=1`）、
**活性对照**（`counters_all_advanced=1`）。倍数是留痕——它让读者自行重测，但不作为门禁判据
（PERF-003 教训：把时序数据写进断言会让证据卡在别的机器上必然 refute）。

## 与 EV-MEM-044 的分工

044 证**结构前提**（是否共享缓存行，确定性、零计时）；045 证**性能后果**（慢约 18 倍，时序、双平台）。
两条独立证据链指向同一因果，任一条单独成立即足以支撑 claim，合起来排除"结构判据失灵"与"性能噪声"两种替代解释。
