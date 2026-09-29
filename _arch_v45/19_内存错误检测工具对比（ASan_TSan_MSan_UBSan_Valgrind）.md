# 方向 19：内存错误检测工具对比（ASan / TSan / MSan / UBSan / Valgrind）

## 核心结论
1. 这 5 个工具覆盖不同的"错误空间"，**不能互相替代**：ASan 抓越界/use-after-free，TSan 抓数据竞争，MSan 抓未初始化读，UBSan 抓 UB，Valgrind 抓泄漏/通用内存错。QueYi 应说明它验证的是"语义正确"，这些工具验证的是"运行时内存安全"——互补不重叠。
2. 开销与可用性决定使用场景：ASan/UBSan 编译期插桩（~2x）、TSan ~10–20x、MSan 需全量插桩、Valgrind 无需重编但 ~20x 且不支持所有平台。QueYi 可在 CI 用 ASan+UBSan 保 813 行内核无内存 UB。
3. 对审稿人：展示 QueYi 内核"过 ASan+UBSan+Valgrind 三关零报错"是极强的可复现性/质量证据，成本极低。

## 精确数字与案例（对比表）
| 工具 | 抓什么 | 插桩 | 开销 | 平台 | 备注 |
|---|---|---|---|---|---|
| **ASan** | 堆/栈/全局越界、UAF、double-free | 编译期 | ~2x | GCC/Clang（MSVC 有 ASan 实验） | 最常用，LeakSanitizer 内建 |
| **LSan** | 内存泄漏 | 编译期 | 极低 | 同 ASan | 常随 ASan 开 |
| **TSan** | 数据竞争 | 编译期 | 10–20x | GCC/Clang | 不支持 MSVC |
| **MSan** | 未初始化内存读 | 编译期（需全程序插桩） | ~3x | 仅 Clang | 要求所有依赖也插桩，难 |
| **UBSan** | 有符号溢出/移位/类型双关等 UB | 编译期 | ~1.5x | GCC/Clang | `-fsanitize=undefined` |
| **Valgrind(memcheck)** | 泄漏/越界/未初始化（二进制插桩） | 无需重编 | ~20x | Linux/macOS | 不支持 Windows 原生，不抓竞争 |

- **案例**：Heartbleed 类漏洞靠 Valgrind/ASan 可发现；数据竞争类靠 TSan（如 C++ 标准库曾有多处 TSan 发现 bug）。
- **组合实践**：CI 跑 `ASan+UBSan`（快）做常规门禁，TSan 跑独立 nightly，MSan 仅在 Clang 专门 job。

## 对阙疑的 3 条具体行动
1. **CI 三关门禁（方向 26）**：QueYi 内核编译加 `-fsanitize=address,undefined`，每晚加 TSan job；0.59ms/卡的基准测试在 sanitized 构建下也跑通，证明无内存 UB。
2. **稿里加"工具覆盖"段**：列 ASan/TSan/MSan/UBSan/Valgrind 各自验证 QueYi 的哪层，澄清"验证器本身被正确测试"，挡"你自己的代码也有 UB"质疑。
3. **区分验证层次**：在 related work 说明 QueYi 验证*生成代码的知识正确性*，而上述工具验证*运行时内存安全*，二者互补——避免 reviewer 混淆。

## 盲区（诚实标注）
- 开销数字为典型经验值，随程序与编译器变化；应你仓库实测填精确值。
- MSan 全量插桩在实际项目难落地（第三方库未插桩），QueYi 若依赖外部库需评估。
- MSVC 的 ASan 支持程度随版本变化，写稿时需确认 2027 时点状态。

## 来源
- [1] ASan — https://github.com/google/sanitizers/wiki/AddressSanitizer
- [2] TSan — https://github.com/google/sanitizers/wiki/ThreadSanitizer
- [3] MSan — https://github.com/google/sanitizers/wiki/MemorySanitizer
- [4] UBSan — https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
- [5] Valgrind — https://valgrind.org/
