# 方向 29：性能优化 profile（cProfile / py-spy）

## 核心结论
1. QueYi 标称 **0.59ms/卡** 是核心卖点之一，但必须用 profiler 证明"这 0.59ms 花在哪、是否含编译调用"——否则审稿人会疑"是验证快还是只是计时了缓存"。
2. C++ 侧性能工具才是主角：**perf / callgrind / VTune / google-benchmark**；Python 侧 cProfile/py-spy 只用于外围编排（方向 22）。QueYi 应报告"纯判决 CPU 时间"与"含编译器调用总时间"两个数字，分开才诚实。
3. 优化铁律：**先测后改（measure before optimize）**；QueYi 的热点大概率在"编译器子进程启动"而非算法——用持久进程 / 缓存编译结果可降耗时，但需在稿里透明说明（否则被疑作弊）。

## 精确数字与案例
- **C++ 工具**：`perf record/stat`（Linux 采样）、`valgrind --tool=callgrind`（调用图，慢）、Intel VTune（微架构）、`google/benchmark`（微基准）。QueYi 用 `benchmark` 测单卡延时分布（p50/p99，不只均值）。
- **Python 工具**：`cProfile`（确定性，看函数耗时）、`py-spy`（采样，不侵入，看外围）、`line_profiler`（逐行）。仅当编排层是瓶颈才用。
- **案例**：编译器调用（fork+exec GCC）单次 ~50–200ms，远大于 0.59ms 算法；若 QueYi 的 0.59ms 不含编译，需说明"判决"指"拿到编译结果后的分析"——这反而是合理定义，但要写清。
- **优化手段**：编译器持久守护进程（clangd/gcc 无原生，可用 `ccache` 加速重编译）、结果缓存、并行卡片（方向 26 矩阵）。

## 对阙疑的 3 条具体行动
1. **拆两个计时**：测"仅分析（不含编译）"与"端到端（含编译）"分别延时，稿里都报，防 reviewer 质疑。
2. **上 google-benchmark**：对判决函数写微基准，报告 p50/p99（不只均值 0.59ms），证明稳定；p99 高说明有长尾（编译器冷启动）需处理。
3. **perf 火焰图入附录**：附一张 QueYi 热点火焰图，展示热点在算法而非 IO，作为"性能诚实"证据。

## 盲区（诚实标注）
- "0.59ms/卡"是否含编译器调用未知（盲点，行动 1）；若含则优于预期，若不含需透明。
- google-benchmark 需引入依赖，增加构建复杂度；若不愿加，可用简单 `std::chrono` 自测但需说明方法。
- cProfile/py-spy 对纯 C++ 内核无效，仅在外围 Python 有用，勿误用。

## 来源
- [1] perf — https://perf.wiki.kernel.org/
- [2] callgrind — https://valgrind.org/docs/manual/cl-manual.html
- [3] google/benchmark — https://github.com/google/benchmark
- [4] py-spy — https://github.com/benfred/py-spy
- [5] cProfile — https://docs.python.org/3/library/profile.html
