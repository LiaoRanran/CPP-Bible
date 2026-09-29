# 方向 40：性能优化 profile（cProfile / py-spy / perf / hyperfine / callgrind）

> 调研时间：2026-09-29（GMT+8）｜联网搜索 10 次 + 6 次 WebFetch 读官方文档/手册
> 锚点项目：阙疑 / queyi（Python 内核 `tools/gate_engine.py` **3826 行**、67 条规则、595 个 `.py`、C++ 夹具 15 条）
> 关联：方向 37（CI 里加性能门禁）、方向 39（fail-closed 的性能代价）

---

## 核心结论

1. **"测错"比"没测"更危险**：Python 官方文档明确写着分析器**只为 Python 代码引入开销、不为 C 层函数引入开销**，因此"用 cProfile 的耗时去比较 Python 实现与 C 实现"是**方法论错误**；同理，Google Benchmark 官方文档列出**6 类系统性方差来源**（Turbo Boost、SMT、NUMA、缓存效应等）。**在阙疑这种"数字就是论文"的项目里，测量方法本身必须写进论文。**
2. **工具选择由"是否可重启"和"是否要精确调用次数"决定**：cProfile 是**确定性**分析器（每次函数调用进出都插钩子，精确但开销大）；py-spy 是**采样**分析器（Rust 实现、**不在被分析进程内运行**、官方称 "extremely low overhead"、**可安全用于生产**）。阙疑的 gate run 是短时批处理，**两个都要用**：cProfile 定位精确热点，py-spy 做 `--native` 下钻到 C 扩展。
3. **性能回归门禁不能用"单次时间"做判据**：hyperfine 默认**至少跑 10 次、至少 3 秒**，并做**离群点检测**；CI 里的性能门禁应当用 `github-action-benchmark` 之类的工具对**多次运行的统计量**做阈值判断，否则噪声会直接把门禁变成"随机红灯"。

---

## 精确数字与案例

### 1. cProfile：确定性分析器的精确能力与精确边界

一手来源 `https://docs.python.org/3/library/profile.html`（Python 官方文档，3.14.7）。原文要点：

- **定义**："A *profile* is a set of statistics that describes **how often and how long** various parts of the program executed." 确定性分析会监控**所有函数调用、函数返回、异常**事件，并"对这些事件之间的时间间隔进行精确计时"。
- **开销（定性，无数字）**：cProfile 是"a C extension with **reasonable overhead** that makes it suitable for profiling long-running programs"；`profile` 是"a pure Python module … but which **adds significant overhead**"。**官方文档没有给出百分比或倍数**——这一点必须诚实标注（网上流传的"cProfile 慢 2–3 倍"是经验值，非官方数字）。
- **`cProfile` vs `profile`**：`cProfile` 基于 `lsprof`（C 扩展，推荐大多数用户）；`profile` 是纯 Python（"significant overhead"，但更易扩展）。`profile.Profile` **支持校准（calibration）**，`cProfile.Profile` **无法校准**。
- **致命 Note（原文意思）**：分析器"旨在提供执行概况，**而非用于基准测试**——若需基准测试应使用 `timeit`"。原因："**分析器只会给 Python 代码引入开销，而不会给 C 层函数引入开销**，因此 C 代码会显得比任何 Python 代码都快。"
- **计时精度限制（原文）**：底层"时钟"通常仅以约 **0.001 秒**跳动，因此"任何测量都不会比底层时钟更精确"。第二类误差来自"事件被分发到分析器实际读取时钟状态之间的延迟"，**调用次数多、调用函数多的函数会累积这类误差**，"可能累积得非常大"。该问题在 `profile` 中比在低开销的 `cProfile` 中更严重。
- **负数警告（原文）**："Do **not** be alarmed by negative numbers in the profile."（校准后可能出现负数，属正常，结果实际比未校准时更好。）

**`pstats` 的排序键**（用于定位热点）：`'calls'`、`'cumulative'`/`'cumtime'`、`'tottime'`/`'time'`、`'pcalls'`、`'name'`、`'nfl'`、`'stdname'`、`'line'`、`'file'`。**时间类统计按降序，名称/文件/行号按升序**。向后兼容的数值参数：`-1`=`stdname`、`0`=`calls`、`1`=`time`、`2`=`cumulative`。

**列含义（关键区分）**：

- `tottime` = 函数自身耗时，**不含**调用子函数的时间。
- `cumtime` = 函数**及其所有子函数**的耗时，**即使对递归函数也是准确的**。
- `ncalls` 形如 `3/1` 表示递归：前为总调用数，后为原始调用数（primitive calls）。

**阙疑怎么用**：

```bash
python -m cProfile -o gate.prof tools/gate_engine.py --check
python -c "import pstats; p=pstats.Stats('gate.prof'); p.sort_stats('tottime').print_stats(25)"
```

**先看 `tottime` 前 25 名**（真正自己耗时的函数），再看 `cumtime`（找出"虽然自己快但拖着一大坨子调用"的入口）。3826 行的 `gate_engine.py` 若把 67 条规则写成 67 个函数，`tottime` 榜会直接指出哪几条规则最贵。

### 2. py-spy：采样分析器，可安全用于生产

一手来源 `https://github.com/benfred/py-spy`（README）。原文要点：

- **"py-spy is extremely low overhead"**；"it is written in **Rust** for speed and **doesn't run in the same process** as the profiled Python program"；"This means py-spy is **safe to use against production Python code**."
- **附加机制（原文）**：Linux 用 `process_vm_readv` 系统调用；OSX 用 `vm_read`；Windows 用 `ReadProcessMemory`。
- **权限**：OSX **始终需要 root**；Linux 默认"require root permissions when attaching to a process that isn't a child"（可用 `ptrace_scope` sysctl 放宽）；py-spy 自己创建进程则无需 root。
- **三种子命令**：`record`（输出文件）、`top`（类 Unix `top` 的实时视图）、`dump`（打印每个线程当前调用栈，支持 `--locals`）。
- **输出格式**（`record --format`）：`flamegraph`（默认，交互式 SVG）、`speedscope`、`raw`。
- **`--native`**：官方 FAQ 原文 "**Yes!** py-spy supports profiling native python extensions written in languages like C/C++ or Cython, on some platforms"，并建议"compile your Python extension with symbols"。Cython 需要生成的 C/C++ 文件才能回到 `.pyx` 行号。

**⚠️ 诚实标注**：README **没有给出默认采样率的 Hz 数值**，也**没有在正文列出 `--rate` 选项名**，只说"See `py-spy record --help` for information on other options including **changing the sampling rate**"。网上常见的"默认 100 Hz"我**未从一手文档核实**。

**阙疑怎么用**（attach 到长跑的全量 gate，不中断）：

```bash
py-spy record --native --format flamegraph -o gate-flame.svg -- python tools/gate_engine.py --check --all
py-spy top -- python tools/gate_engine.py --check          # 实时看最热函数
py-spy dump --locals --pid <PID>                            # 卡住时抓栈+局部变量
```

`--native` 对阙疑尤其关键：阙疑的 C++ 夹具通过 subprocess 或扩展调用，纯 Python 火焰图会显示"时间花在 subprocess/扩展里"但看不到 C 侧热点。

### 3. Callgrind：指令计数，不是时间

一手来源 `https://valgrind.org/docs/manual/cl-manual.html`（Valgrind 官方手册，Callgrind 章节）。要点：

- **默认测量什么**：**指令数（Ir, Instruction Read）**、指令与源码行的对应关系、**调用者/被调用者关系**、**调用次数**。**注意：默认测的是指令数，不是墙上时间。** 这对"消除机器噪声"极有价值——指令数与 CPU 频率无关。
- **可选扩展（默认关闭）**：`--cache-sim=yes`（缓存模拟，类似 Cachegrind）、`--branch-sim=yes`（分支预测）。启用后额外计数器：`I1mr`/`ILmr`、`Dr`、`D1mr`/`DLmr`、`Dw`、`D1mw`/`DLmw`、`Bc`/`Bcm`、`Bi`/`Bim`。
- **减速倍数（手册给出的具体数字）**：
  - 用 `--instr-atstart=no`（不插桩）→ **约 4 倍**（"at most a slowdown of around 4, which is the minimum Valgrind overhead"）。
  - 关闭事件聚合/关闭插桩 → **约 2 倍**（与 `valgrind --tool=none` 相同）。
  - 额外开缓存模拟或分支预测 → **再增加约 2 倍**。
- **命令**：`valgrind --tool=callgrind [callgrind options] your-program [program options]`；编译建议用 `-g` 并**开启优化**。默认输出文件名 `callgrind.out.<pid>`，可用 `--callgrind-out-file=<file>` 指定（支持 `%p`=PID、`%q`=环境变量）。
- **`callgrind_annotate`**：打印按**独占（exclusive）成本**排序的函数列表；`--inclusive=yes` 切到包含式；`--threshold=<0–100>` **默认 99%**；`--show-percs=yes` 显示百分比。**重要限制（原文）**：`callgrind_annotate` **不做任何循环检测**，"can print nonsense inclusive costs way above 100%"（递归时可能打出超过 100% 的无意义包含式成本）。
- **KCachegrind**（GUI）：**做循环检测**，把循环内所有函数折叠为名为 `Cycle 1` 的合成函数；是**唯一**能显示 `--dump-instr=yes` 产生的指令级/汇编级注释的工具。手册明确建议：**若成本很大部分位于循环中，必须用 KCachegrind**。

**阙疑怎么用**：阙疑的 C++ 夹具（15 条缺陷）跑 callgrind，**看指令数而不是看时间**——这样即使 CI 机器是共享的、有噪声，指令数依然稳定可比。命令：

```bash
valgrind --tool=callgrind --cache-sim=yes --callgrind-out-file=cg.out ./build/fixture_runner
callgrind_annotate --threshold=95 --show-percs=yes cg.out | head -60
```

**⚠️ 注意**：手册开头说明 Callgrind"works best on x86 and amd64, and unfortunately currently does not work so well on PowerPC, ARM, Thumb or MIPS code"。阙疑若涉及 ARM 嵌入式目标，**callgrind 在 ARM 上效果不佳**，需要换工具（如 `perf` 或目标板上的硬件计数器）。

### 4. perf + 火焰图：采样型系统级分析

一手来源 `https://github.com/CarsonKiibi/flamegraph`（README 摘录）与多篇教程（`https://www.cnblogs.com/yghr/p/18239897`、`https://www.php.cn/faq/2289193.html`）。要点：

- **关键命令**：`perf record -e cpu-clock --call-graph dwarf [-t 线程id] [程序]`，采集后在当前目录生成 `perf.data`。
- **必须加 `--call-graph dwarf`（或 `-g`）**：`--call-graph dwarf` 用 **DWARF 调试信息**展开调用栈。中文教程（`https://www.php.cn/faq/2289193.html`）原文强调："关键在**采样真实性、调用栈完整性和符号正确解析**；perf record 必须加 `-g` 和 `--call-graph dwarf`，**二进制需带调试信息**。"
- **三种用法**：`perf top`（实时 CPU 监控）、`perf record`（录制）、火焰图生成。
- 生成火焰图的标准链路：`perf record` → `perf script` → `stackcollapse-perf.pl` → `flamegraph.pl` → `.svg`。

**对阙疑的映射**：阙疑的 Python 内核在 `perf` 下会显示大量时间在 CPython 解释器循环里（`_PyEval_EvalFrameDefault`），**这是正常的、不是 bug**——所以 Python 侧优先用 cProfile/py-spy，`perf` 主要用于**C++ 夹具**和**验证"Python 之外"的开销**（如 subprocess 启动、磁盘 I/O）。

### 5. hyperfine：命令行基准的正确姿势

一手来源 `https://github.com/sharkdp/hyperfine`（README）。精确默认值：

- **默认至少运行 10 次、且至少测量 3 秒**（原文："By default, it will perform *at least* 10 benchmarking runs and measure for at least 3 seconds."）。用 `-r`/`--runs` 覆盖。
- **`-w`/`--warmup N`**：正式基准前先跑 N 次（用于磁盘缓存预热）。
- **`-p`/`--prepare <cmd>`**：**每次**计时前运行（用于冷缓存，如 `sync; echo 3 | sudo tee /proc/sys/vm/drop_caches`）。
- **`-N`/`--shell=none`**：不经过中间 shell。原文说明这是为 **< 5 ms** 的极快命令准备的，因为"the shell startup overhead correction would produce a significant amount of noise"。
- **shell 启动时间会被校正**：hyperfine 会用一个空命令多次运行来测 shell 启动时间并**减掉**它。
- **统计与离群点**：官方特性列表含"**Statistical outlier detection** to detect interference from other programs and caching effects"（检测来自其他程序与缓存效应的干扰）。
- **导出格式**：CSV、JSON、Markdown、AsciiDoc。`--export-markdown` 生成对比表，README 给的示例表（`find` vs `fd`）：

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|---|---|---|---|---|
| `find . -iregex '.*[0-9]\.jpg$'` | 2.275 ± 0.046 | 2.243 | 2.397 | 9.79 ± 0.22 |
| `find . -iname '*[0-9].jpg'` | 1.427 ± 0.026 | 1.405 | 1.468 | 6.14 ± 0.13 |
| `fd -HI '.*[0-9]\.jpg$'` | 0.232 ± 0.002 | 0.230 | 0.236 | 1.00 |

**参数扫描**：`-P`/`--parameter-scan`（数值区间，如 `--parameter-scan num_threads 1 12`）、`-D`/`--parameter-step-size`、`-L`/`--parameter-list`（枚举，如 `-L compiler gcc,clang`）。

**阙疑怎么用**：

```bash
hyperfine --warmup 3 -r 20 \
  'python tools/gate_engine.py --check' \
  'python tools/gate_engine.py --check --parallel 4'
```

注意：**不要用 hyperfine 去测单个 Python 函数**（进程启动开销会淹没信号），那用 `pytest-benchmark`。

### 6. 避免测错：Google Benchmark 列出的 6 类方差来源

一手来源 `https://google.github.io/benchmark/reducing_variance.html`（Google Benchmark 官方文档）。原文列出的方差来源：

1. **多核机器上不同核/线程速度不同**，跑两次可能落到不同核上。
2. **Turbo Boost / AMD Turbo Core / Precision Boost** 会"temporarily change the CPU frequency **even when using the 'performance' governor**"。
3. **CPU 之间的上下文切换**，或基准所在 CPU 上的调度竞争。
4. **Intel Hyperthreading / AMD SMT** 造成与上一条相同的问题。
5. **其他 CPU 上运行的代码造成的缓存效应**。
6. **NUMA（非统一内存访问）**。

官方给出的两个警告消息（原文）：

```
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
***WARNING*** ASLR is enabled, the results may have unreproducible noise in them.
```

官方推荐的 7 条降噪手段（含**可直接抄的命令**）：

1. 设为 performance governor：`sudo cpupower frequency-set --governor performance`；验证：`cpupower frequency-info -o proc`。
2. 关闭 CPU boost：`echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost`。
3. 绑核：`taskset -c 0 ./mybenchmark`。
4. 提高调度优先级：`sudo nice -n -20 ./mybenchmark` 或 `sudo chrt -f 80 ./mybenchmark`。
5. 关闭 Hyperthreading/SMT（BIOS 或 `/sys`）。
6. 关掉按定时器干活的程序（浏览器、桌面环境等）。
7. 把工作集缩到 L1 缓存内（但官方提醒"may lead you to optimize for an unrealistic situation"）。

**ASLR 相关**：`echo 0 > /proc/sys/kernel/randomize_va_space`（全局）；`setarch \`uname -m\` -R ./a_benchmark`（单次）；或在 `main()` 首行调 `benchmark::MaybeReenterWithoutASLR(argc, argv)`。

**多次重复**：官方提到方差可能出现在单次运行的**重复之间**（`--benchmark_repetitions=N`）或**多次程序运行之间**。

**`DoNotOptimize`**：`https://github.com/google/benchmark` 与 `https://blog.csdn.net/GrayOnDream/article/details/138390258` 说明 `benchmark::DoNotOptimize(...)` 用于"防止编译器把一个值或表达式优化掉"——**不写它，编译器可能把你测的整个计算删掉，测出来是 0 ns**。另一个常见错误（`https://www.php.cn/faq/1969321.html`）是"在 `Benchmark::State` 循环内用 `std::chrono::high_resolution_clock` 手动测单次耗时再除以迭代次数"——这是错的，应让框架管循环。

### 7. 性能回归门禁：CI 里怎么做才不误报

- **`github-action-benchmark`**（`https://github.com/benchmark-action/github-action-benchmark`）：官方描述是"a GitHub Action for continuous benchmarking"，"collects data from the benchmark outputs and monitor the results on GitHub Actions workflow"，并"can detect possible performance regressions"。它把结果可视化在项目的 GitHub Pages 上，并可按阈值告警。
- **Bencher**（`https://bencher.dev/zh/docs/how-to/github-actions/`）：另一套持续基准测试服务，README 提到 `hyperfine` 的 JSON 输出可直接喂给它（`https://github.com/sharkdp/hyperfine` 的 "Integration with other tools" 一节列出 Bencher 与 Chronologer）。
- **`pytest-benchmark`**（`https://pytest-benchmark.readthedocs.io/`，文档版本 5.3.0）：提供 `benchmark` fixture，"will benchmark any function passed to it"；支持 pedantic 模式、保存/对比基线。
- **一个必须避开的坑**（`https://www.php.cn/faq/2862859.html`）："性能测试不准的根源在于 **setup 混入 benchmark 调用路径**，必须将数据构造等非算法逻辑**移出测量链**"。

**阙疑的回归门禁建议**：

- **Python 侧**：`pytest-benchmark` 测"单条规则的判定函数"（纯计算，无 I/O），把基线 JSON 提交进仓库，CI 里用 `--benchmark-compare` + 阈值（如超过基线 **20%** 即失败）。
- **端到端**：`hyperfine` 测整个 gate 命令，**只做记录不做硬门禁**（因为 GitHub runner 是共享 VM，噪声大；官方文档自己也说 CPU 频率与 SMT 不可控）。
- **C++ 侧**：**callgrind 的指令数**做硬门禁（与频率无关，可复现），**时间**只做记录。这是本方向最重要的一条工程判断。

---

## 对阙疑的 3 条具体行动

**行动 1：给 `gate_engine.py`（3826 行）做一次完整的热点测绘，并产出可提交的基线。**
具体：(a) `python -m cProfile -o gate.prof tools/gate_engine.py --check`，用 `pstats` 按 `tottime` 打前 25 名，**把 67 条规则按自身耗时排序**——这一步会直接告诉你哪几条规则拖慢了整体。(b) `py-spy record --native -o gate-flame.svg -- python tools/gate_engine.py --check --all`，检查是否有时间花在 subprocess/扩展的 C 侧。(c) 把两份结果存进 `_arch_v46/` 之外的 `perf/` 目录（并加进 `.gitignore` 或明确提交）。验收标准：**能说出"前 3 条最贵的规则是哪 3 条，各占总 tottime 的百分比"**——如果说不出来，说明还没测。

**行动 2：建立"指令数硬门禁 + 时间软记录"的双轨性能回归机制。**
具体：C++ 夹具侧，CI（方向 37）里加一个 job：`valgrind --tool=callgrind --callgrind-out-file=cg-${{ github.run_id }}.out ./build/fixture_runner`，再用 `callgrind_annotate` 抓 `Ir` 总数，与仓库里提交的 `perf/callgrind_baseline.txt` 比较，**超过 5% 则失败**（指令数是确定性的，可以设紧阈值）。Python 侧用 `pytest-benchmark` + 基线 JSON，阈值 **20%**（因为 Python 侧有 GC、解释器版本差异等额外噪声）。**时间**类指标（hyperfine）只存 JSON 不设阈值。验收标准：故意在一条规则里加一个 O(n²) 循环，CI 必须变红。

**行动 3：把"测量方法"写进论文的 Evaluation 章节，并在 CI 机器上跑一次噪声体检。**
具体：(a) 在 `research/05_evaluation_protocol.md` 或 `research/11_reproducibility.md` 里新增一节 "Measurement Methodology"，明确写：**Python 侧用 cProfile（确定性）+ py-spy（采样，`--native`）双工具交叉验证；C++ 侧用 callgrind 指令数而非墙上时间；端到端用 hyperfine `--warmup 3 -r 20`；已知未控制的方差来源包括 Turbo Boost、SMT、NUMA、共享 runner 噪声（引 Google Benchmark 官方文档的 6 条）**。(b) 在 CI 里跑一次 `hyperfine --warmup 3 -r 20 'python tools/gate_engine.py --check'` 并记录 `Mean ± σ`，**如果 σ/Mean > 10%，就在论文里注明该测量不可用于跨机器比较**。验收标准：论文里能回答"审稿人问：你怎么保证时间数字可复现？"

---

## 盲区（诚实标注）

1. **cProfile 的开销倍数没有官方数字**。Python 官方文档只说 "reasonable overhead"，**未给百分比或倍数**。网上常见的"2–3 倍""5–10 倍"我**未从一手来源核实**，故不引用。
2. **py-spy 的默认采样率未从一手文档核实**。README **没有列出 Hz 数值**，也没在正文列出 `--rate` 选项名，只说"changing the sampling rate"需查 `--help`。网上常见的"默认 100 Hz"我**未验证**。
3. **py-spy 的 "extremely low overhead" 是定性表述，无数字**。所谓"1% 开销"我**未在一手文档中找到**。
4. **`perf` 的具体采样频率、`--call-graph dwarf` 与 `--call-graph fp` 的精度差异、以及 dwarf 带来的额外开销，我未从 `perf` 官方 man page 逐字核实**；引用的中文教程（`php.cn`、`cnblogs`）是二手来源。
5. **`hyperfine` 的"至少 10 次、至少 3 秒"是 README 原文**，但 README **未说明这两个条件如何交互**（是取 max 还是先满足哪个）；`--runs` 与自动判定的优先级我未细读源码。
6. **`github-action-benchmark` 的默认阈值、告警机制、以及它对 GitHub runner 噪声的处理方式我未读其 README 细节**（只读到官方描述）。**建议实现前先读它的 README 全文**。
7. **Callgrind 在 ARM 上"效果不佳"是 Valgrind 手册的原文表述**，但**未说明具体差到什么程度**；阙疑若面向 ARM 嵌入式，需另测。
8. **Callgrind 的减速倍数（4x / 2x / +2x）是手册给出的量级**，不是精确测量值。
9. **阙疑的实际性能数据我一概没有**：`gate_engine.py` 3826 行的运行时间、67 条规则各自的耗时、C++ 夹具的运行时间，**全部未知**。本方向的所有"怎么用"都是方法建议，**不含任何实测数字**。
10. **"5% 指令数阈值""20% 时间阈值"是我提的工程建议值，没有权威来源支撑**。合理阈值应通过实际测量 CI 机器上的噪声水平来定。
11. **`pytest-benchmark` 5.3.0 的具体 API（`--benchmark-compare` 的确切参数名、`pedantic` 模式语义）我未读文档正文**，只读到官方描述与第三方教程。

---

## 来源

1. Python 官方文档, *The Python Profilers* — https://docs.python.org/3/library/profile.html （一手；确定性分析定义、"reasonable overhead"、0.001 秒时钟精度、"不为 C 函数引入开销"、pstats 排序键与列含义、负数警告）
2. Google Benchmark 官方文档, *Reducing Variance* — https://google.github.io/benchmark/reducing_variance.html （一手；6 类方差来源、cpupower/taskset/nice/chrt 命令、ASLR 警告）
3. Google Benchmark 官方文档, *User Guide* — https://google.github.io/benchmark/user_guide.html （`--benchmark_repetitions`、输出格式）
4. GitHub, *google/benchmark* — https://github.com/google/benchmark （`DoNotOptimize`）
5. Valgrind 官方手册, *Callgrind* — https://valgrind.org/docs/manual/cl-manual.html （一手；Ir 事件、4x/2x/+2x 减速、`--callgrind-out-file`、`--cache-sim`、`callgrind_annotate --threshold` 默认 99%、无循环检测、KCachegrind 的 `Cycle 1`）
6. Valgrind 官方手册, *Cachegrind* — https://valgrind.org/docs/manual/cg-manual.html
7. GitHub, *benfred/py-spy* — https://github.com/benfred/py-spy （一手；"extremely low overhead"、"doesn't run in the same process"、process_vm_readv/vm_read/ReadProcessMemory、`--native`、record/top/dump、flamegraph/speedscope/raw）
8. GitHub, *sharkdp/hyperfine* — https://github.com/sharkdp/hyperfine （一手；"at least 10 runs and at least 3 seconds"、`-w`/`-p`/`-N`、离群点检测、示例对比表、参数扫描、Bencher/Chronologer 集成）
9. GitHub, *benchmark-action/github-action-benchmark* — https://github.com/benchmark-action/github-action-benchmark
10. Bencher 文档, *如何在 GitHub Actions 中使用 Bencher* — https://bencher.dev/zh/docs/how-to/github-actions/
11. pytest-benchmark 文档 — https://pytest-benchmark.readthedocs.io/
12. *利用 perf 进行性能分析* — https://www.cnblogs.com/yghr/p/18239897 （2024-06-09；`perf record -e cpu-clock --call-graph dwarf`）
13. *怎么在 Linux 利用 Flame-Graph 生成性能分析火焰图* — https://www.php.cn/faq/2289193.html （2026-04-04；"必须加 -g 和 --call-graph dwarf"）
14. *正确对你的 C++ 代码进行性能测试——DoNotOptimize 实现原理* — https://blog.csdn.net/GrayOnDream/article/details/138390258 （2026-08-11）
15. *Python 性能剖析工具链：cProfile、py-spy 与 memray* — https://devpress.csdn.net/v1/article/detail/161871862 （2026-07-12；确定性 vs 采样剖析对比）
16. *如何使用 pytest-benchmark 对 Python 函数进行性能基准测试* — https://www.php.cn/faq/2862859.html （2026-07-22；"setup 混入 benchmark 路径"的坑）
17. *测量陷阱与环境就绪: 16 条 checklist* — https://awesome-embedded-learning-studio.github.io/Tutorial_AwesomeModernCPP/vol6-performance/ch01-benchmark-methodology/03-pitfalls-and-env （2026-07-20；Turbo Boost 与锁频）
18. 本仓库内部锚点：`_arch_v46/00_仓库扫描.md` §5（`gate_engine.py` 3826 行）、§4（`tools/` 640 条目 / 595 个 `.py`）、§8（缺陷夹具 15 条）。
