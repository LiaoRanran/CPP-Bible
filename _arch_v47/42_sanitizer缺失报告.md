# 方向 42：sanitizer 缺失时的诚实报告

## 核心结论

1. **阙疑本机缺失的两类 sanitizer 运行时是"可恢复的环境缺陷"而非"能力缺陷"**：GCC 报 `cannot find -lubsan` 是因为系统没装 `libubsan`（UBSan 运行时库），Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a` 是 Windows/clang-cl 工具链未随附 ASan 动态 thunk 库（见来源 9/10）；二者都不影响"阙疑能否对某个 C++ 知识卡做出判决"，只影响"判决过程是否经过运行时内存/UB 校验"。这意味着它必须写进 `Threats to Validity`，但可作为可复现性声明中的"环境约束"而非"方法失效"。

2. **四种主流 sanitizer 的可用性并不完全相等，必须分档声明**：AddressSanitizer（ASan，典型开销 **2x**，Clang 文档逐字：*"Typical slowdown introduced by AddressSanitizer is 2x"*）、UndefinedBehaviorSanitizer（UBSan，依赖 `libubsan` 但可用 `-fsanitize-trap` 完全免库）、MemorySanitizer（MSan，**Clang only**，开销 **3x**，且要求"所有代码含 libc 均被插桩"）、ThreadSanitizer（TSan，检测 data race，GCC≥4.8/Clang 均支持，但 GCC 文档逐字规定 *"-fsanitize=address ... cannot be combined with -fsanitize=thread"*）。阙疑若只宣称覆盖了 ASan+UBSan，而把 MSan/TSan 列在未覆盖边界，是诚实且可接受的。

3. **NeurIPS 官方 Checklist 明确鼓励"诚实声明局限"，并写明"不要因诚实而惩罚作者"**：NeurIPS Paper Checklist 第 2 条（Limitations）逐字：*"We understand that authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection ... Reviewers will be specifically instructed to not penalize honesty concerning limitations."* 这为阙疑把 sanitizer 缺失写进 Limitations/Threats to Validity 提供了直接合规依据；同时 Checklist 第 4/5 条要求给出"复现路径与精确命令/环境"，正好可用一个带 sanitizer 的 Docker 镜像来闭环。

---

## 精确数字与案例

### 一、四种 sanitizer 的检测能力与可用性对照（含逐字引文）

下表整合 Clang 官方文档与 GCC 文档的逐字表述，是阙疑在论文里声明"覆盖了什么、没覆盖什么"的事实底座。

| Sanitizer | 检测目标（逐字/近逐字） | 支持编译器 | 典型开销 | 关键可用性约束 |
|---|---|---|---|---|
| ASan | *"Out-of-bounds accesses to heap, stack and globals; Use-after-free; Use-after-return; Use-after-scope; Double-free, invalid free; Memory leaks (experimental)"* | GCC≥4.8、Clang | **2x**（Clang 文档逐字 *"Typical slowdown introduced by AddressSanitizer is 2x"*） | 不能和 `-fsanitize=thread` 或 `-fsanitize=hwaddress` 同用（GCC 文档逐字） |
| UBSan | `-fsanitize=undefined` 组（alignment/bool/enum/shift/signed-integer-overflow/null/return/vla-bound 等，排除 float-divide-by-zero、unsigned-integer-overflow、implicit-conversion、local-bounds、vptr、nullability-*） | GCC、Clang | 低（编译期插桩为主） | 普通模式依赖 `libubsan`；Trap 模式 *"doesn't require UBSan run-time support"*（Clang 文档） |
| MSan | *"detector of uninitialized memory use"*：未初始化值用于分支/指针/函数参数/返回值等 | **仅 Clang** | **3x**（Clang 文档逐字 *"Typical slowdown introduced by MemorySanitizer is 3x"*）；真实内存 **2x** | *"MemorySanitizer requires that all program code is instrumented ... even libc"*；静态链接不支持 |
| TSan | *"ThreadSanitizer is a tool that detects data races"*（默认另开 `detect_deadlocks`，exitcode 默认 **66**） | GCC≥4.8、Clang | 高（常单独 job） | 与 ASan、MSan 互斥；GCC 文档逐字：`-fsanitize=address` 不能与 `-fsanitize=thread` 组合 |

**逐字引文（ASan 检测清单，Clang 官方文档）：**
> "The tool can detect the following types of bugs: Out-of-bounds accesses to heap, stack and globals; Use-after-free; Use-after-return ...; Use-after-scope ...; Double-free, invalid free; Memory leaks (experimental)."

**逐字引文（MSan 全插桩约束，Clang 官方文档）：**
> "MemorySanitizer requires that all program code is instrumented. This also includes any libraries that the program depends on, even libc. Failing to achieve this may result in false reports."

这意味着：阙疑若想用 MSan 校验"未初始化读取"类知识卡，必须把被测片段依赖的整个工具链（含 libc++/libstdc++）都换成 MSan 插桩版——对单工具链本机环境而言代价极高，正是"诚实声明未覆盖"的合理理由。

### 二、本机缺失错误的根因：GCC `cannot find -lubsan` 与 Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a`

阙疑共享上下文中记录的两条硬伤，根因分别是：

- **GCC `cannot find -lubsan`**：`-fsanitize=undefined` 的普通报告模式需要链接 `libubsan` 运行时库（GCC 文档逐字：*"-fsanitize-trap= ... report ... using __builtin_trap rather than a libubsan library routine"*，反向说明普通模式是走 `libubsan`）。在 Debian/Ubuntu 上该库通常来自 `libubsan1`（或 `libubsan` dev 包）未安装，或交叉/最小化镜像未含；修复只需 `apt-get install libubsan1`（发行版相关，具体包名未逐一核实，列入盲区）。这**不是**编译器不支持 UBSan，而是链接期找不到共享库。

- **Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a`**：这是 Windows + clang-cl 工具链下 ASan 的"动态运行时 thunk"库，用于把 ASan 运行时注入最终可执行文件；该 `.a` 属于 LLVM `compiler-rt` 运行时组件，在部分 clang-cl 安装（尤其未勾选 ASan 组件、或 MinGW/clang 混合环境）会缺失（来源 10 的 Tencent Cloud / LLVM Discourse 讨论均指向 Windows 下 ASan 运行时配套不全）。这是**工具链安装不完整**，不是 ASan 本身不可用。

两条的共同点是：**方法层面 sanitizer 可用，环境层面本机缺库**。因此论文措辞应是"本评估机未配置 sanitizer 运行时，故 X 类校验未在运行时层面执行"，而非"阙疑不具备检测内存错误的能力"。

### 三、UBSan Trap 模式 / Minimal Runtime——运行时缺失时的零库降级路径

Clang 与 GCC 文档都给出了一条**不依赖运行时库**的降级通道，恰好可缓解本机 `libubsan` 缺失：

- **Trap 模式（零库）**：GCC 文档逐字：*"The -fsanitize-trap= option instructs the compiler to report ... using __builtin_trap rather than a libubsan library routine. The advantage of this is that the libubsan library is not needed and is not linked in, so this is usable even in freestanding environments."* 即 `g++ -fsanitize=undefined -fsanitize-trap=all` 在缺 `libubsan` 的机器上仍可编译运行，UB 触发时直接 `__builtin_trap`（SIGILL/SIGTRAP）中止。代价是**没有人类可读的 `runtime error:` 报告**，只有 abort。

- **Minimal Runtime（小体积、生产可用）**：Clang 文档逐字：*"There is a minimal UBSan runtime available suitable for use in production environments. This runtime has a small attack surface. It only provides very basic issue logging and deduplication ... To use the minimal runtime, add -fsanitize-minimal-runtime"*。它仍需链接，但体积小、攻击面小，适合 CI 中的"快速 UB 闸门"。注意 *"does not support -fsanitize=vptr checking"*。

对阙疑的含义：**即便本机修不好 `libubsan`，也可以用 `-fsanitize-trap=undefined` 对知识卡做"UB 是否触发"的二值判决**（触发=卡中代码有 UB，未触发=在该检查下未观测到 UB）。这条路径应写进论文的"降级校验协议"，并诚实标注它牺牲了错误定位信息。

### 四、诚实声明模板 + Docker 干净环境 + CI 最小配置

**（A）论文声明模板（基于 NeurIPS Checklist 第 2 条）。** NeurIPS 逐字要求：*"The authors are encouraged to create a separate 'Limitations' section ... point out any strong assumptions and how robust the results are to violations"*，并举例 *"if the approach was only tested on a few datasets or with a few runs"*。阙疑可写：*"T1：本评估机（合肥，AMD64，GCC/Clang 本地安装）未配置 ASan/UBSan 运行时库，故对内存安全类与未定义行为类知识卡的判决未由 sanitizer 运行时交叉验证；复现镜像 `queyi/san:bookworm` 提供带 `-fsanitize=address,undefined` 的对照环境（见 Appendix X）。"*

NeurIPS 还逐字给出安心条款：*"We understand that authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection ... Reviewers will be specifically instructed to not penalize honesty concerning limitations."*

**（B）Docker 干净环境（实践来源：eddelbuettel 预构建 SAN 容器）。** 权威实践逐字：*"As an easier alternative, the pre-built Docker containers available via my Docker Hub repository can be used on Linux, and via boot2docker on Windows and OS X"*，且其结论 *"Using Docker ... deployment of such tests becomes as easy as invocation of single shell command"*。对阙疑建议的最小 Dockerfile 骨架（写进 `research/` 或仓库 `docker/`）：

```dockerfile
FROM debian:bookworm
RUN apt-get update && apt-get install -y \
    g++ clang libubsan1 libasan8 python3 git cmake
# 验证：
# g++ -fsanitize=address,undefined -g -O1 card.cpp -o card && ./card
# clang++ -fsanitize=memory -g -O1 card.cpp -o card_msan  # MSan（Clang only）
```

**（C）CI 最小配置（来自 sanitizer 工程实践文档）。** 实践要点：ASan+UBSan 合并跑、TSan 单独 job、用 `-fno-sanitize-recover=all`（CI 中首次错误即中止）、设置 `ASAN_OPTIONS=abort_on_error=1:detect_leaks=1` 与 `UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1`，再以 `ctest --output-on-failure` 执行。工程文档逐字：*"ASan and TSan usually run separately. Their runtime instrumentation mechanisms are not suited to run together."* 这与 GCC 文档的"禁止组合"条款一致。

| 实践项 | 推荐值 | 出处 |
|---|---|---|
| ASan+UBSan 合并 | `-fsanitize=address,undefined -fno-sanitize-recover=all` | 工程 SKILL 文档 |
| TSan 独立 job | `-fsanitize=thread`，不与 ASan 同构建 | GCC/Clang 文档 + 工程文档 |
| 环境变量闸门 | `ASAN_OPTIONS=abort_on_error=1:detect_leaks=1; UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1` | 工程 SKILL 文档 |
| 运行 | `ctest --test-dir build --output-on-failure` | 工程 SKILL 文档 |
| 降级（无 libubsan） | `-fsanitize=undefined -fsanitize-trap=all` | GCC 文档逐字 |

---

## 对阙疑的 3 条具体行动

1. **在论文新增独立 `Threats to Validity / Limitations` 小节 T1，并落地到仓库文件**：在 `_arch_v47/` 之外（属论文素材）建议新增 `research/42_threats_to_validity.md`（或在既有 threats 文档追加 T1 段），写入逐字声明："本评估机未配置 ASan/UBSan/MSan/TSan 运行时，故内存安全类与未定义行为类知识卡的判决未由 sanitizer 运行时交叉验证；复现镜像 `queyi/san:bookworm` 提供对照环境。"时间点：**2027-05 前**（投稿前 4–5 个月），与 227 项工作树漂移清理（方向 16）并行。

2. **提交一个带 sanitizer 的可复现 Dockerfile 到仓库 `docker/` 目录并接入 CI**：以 `debian:bookworm` 为基础，安装 `g++ clang libubsan1 libasan8`，附加一条 `g++ -fsanitize=address,undefined -g -O1` 冒烟测试，确保审阅者 `docker build` 后即能复现"带 sanitizer 的判决"；同时在 `.github/workflows/` 增加 `sanitizer` job（ASan+UBSan 合并、`-fno-sanitize-recover=all`、TSan 单独 job）。命令原型见上文第四节（B）（C）。时间点：**2027-03 前**完成并跑通一次 green CI。

3. **用 UBSan Trap 模式为本机做一次"零库降级校验"并补记到判决账本**：在本机执行 `g++ -fsanitize=undefined -fsanitize-trap=all -O1` 对 37 实卡中的内存/UB 相关卡重编译运行，将"触发 trap=有 UB 嫌疑 / 未触发=未观测到 UB"的结果以新字段（如 `ub_trap_check`）写入 append-only 哈希链账本，并在论文标注这是**降级校验、不替代完整 sanitizer 报告**。时间点：**2027-04 前**，与方向 31（43.8% 算术不自洽修复）同一冲刺。

---

## 盲区（诚实标注）

- **具体发行版修复包名未逐一核实**：GCC `cannot find -lubsan` 在 Debian/Ubuntu 上对应 `libubsan1` 还是 `libubsan`（或 `libgcc-*-dev`）随版本不同，我未逐发行版 `apt` 实测，仅依据 GCC 文档"普通模式走 libubsan 库例程"推断；论文中若写具体包名须另行核实（列入盲区）。
- **Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a` 的精确触发条件未 100% 复现**：来源 10 的 Tencent Cloud 问答与 LLVM Discourse 指向 Windows/clang-cl 下 ASan 运行时配套缺失，但我未在阙疑同款机器上实地复现该链接错误，无法确认是 clang-cl 组件未装还是 MinGW 混用导致；"根因"表述为"工具链安装不完整"属合理推断而非实证。
- **MSan 是否真能在阙疑的工具链下对 C++ 卡全插桩（含 libc++）未实测**：Clang 文档要求"even libc"全插桩，否则有 false report；我未验证 Debian bookworm + clang 的 MSan-instrumented libc++ 是否 readily 可得，故论文对 MSan 仅建议"列为未覆盖边界"，不承诺可开。
- **TSan 与 ASan 互斥的"官方逐字"仅来自 GCC 文档**：GCC 文档明确 `-fsanitize=address` 不能组合 `-fsanitize=thread`；Clang TSan 文档本身未直接写该互斥句（来源 8 的 WebFetch 未命中），互斥性由 GCC 文档 + 工程实践间接佐证，建议论文引 GCC 文档而非 Clang 文档作依据。
- **eddelbuettel 预构建 SAN 容器年代较旧（页面 2014）**：该 Docker 实践示例使用 `g++-4.8/-4.9`，对阙疑仅作"思路借鉴"，不应直接照搬其镜像标签；具体 `queyi/san:bookworm` 须自建并锁定版本（见方向 22/23 依赖锁定）。
- **NeurIPS 2027 E&D 的 Checklist 是否为同一版本未核实**：上述 Limitations/Reproducibility 条款引自 NeurIPS 现行 Paper Checklist（2024–2026 通用版），2027 年若改版需重新核对第 2/4/5 条原文，避免引用过期措辞。

---

## 来源

1. **AddressSanitizer — Clang 官方文档** — https://clang.llvm.org/docs/AddressSanitizer.html — 逐字："The tool can detect ... Out-of-bounds accesses ... Use-after-free ... Memory leaks (experimental)"；"Typical slowdown introduced by AddressSanitizer is 2x"；"make sure to use clang (not ld) for the final link step" — LLVM/Clang — 2026-09 访问
2. **UndefinedBehaviorSanitizer — Clang 官方文档** — https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html — 逐字："-fsanitize-trap=...: execute a trap instruction (doesn't require UBSan run-time support)"；"There is a minimal UBSan runtime available suitable for use in production environments" — LLVM/Clang — 2026-09 访问
3. **MemorySanitizer — Clang 官方文档** — https://clang.llvm.org/docs/MemorySanitizer.html — 逐字："MemorySanitizer is a detector of uninitialized memory use"；"Typical slowdown ... is 3x"；"requires that all program code is instrumented ... even libc"；"2x more real memory" — LLVM/Clang — 2026-09 访问
4. **ThreadSanitizer — Clang 官方文档** — https://clang.llvm.org/docs/ThreadSanitizer.html — 逐字："ThreadSanitizer is a tool that detects data races"；默认 exitcode 66 — LLVM/Clang — 2026-09 访问
5. **GCC Instrumentation Options（`-fsanitize=address`/`-fsanitize=undefined`/`-fsanitize-trap`）** — https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html — 逐字："-fsanitize=address ... cannot be combined with -fsanitize=thread or -fsanitize=hwaddress"；"-fsanitize-trap= ... using __builtin_trap rather than a libubsan library routine ... libubsan library is not needed and is not linked in" — Free Software Foundation (GCC) — 2026-09 访问
6. **NeurIPS Paper Checklist（Limitations / Reproducibility 条款）** — https://neurips.cc/public/guides/PaperChecklist — 逐字："The authors are encouraged to create a separate 'Limitations' section"；"We understand that authors might fear that complete honesty about limitations ... Reviewers will be specifically instructed to not penalize honesty"；第 4/5 条可复现性与开放数据代码 — NeurIPS Foundation — 2026-09 访问
7. **eddelbuettel, "sanitizers"（Docker 预构建 SAN 容器实践）** — https://dirk.eddelbuettel.com/code/sanitizers.html — 逐字："pre-built Docker containers available via my Docker Hub repository can be used on Linux ... deployment of such tests becomes as easy as invocation of single shell command"；指出 Windows 上 sanitizer 工具链"not available at all (via the common Rtools mechanism)" — Dirk Eddelbuettel（R Foundation / Debian）— 页面 2014-08-06
8. **Sanitizers 工程 SKILL（ASan+UBSan 合并 / TSan 单独 / CI 闸门）** — https://github.com/mohitmishra786/low-level-dev-skills/blob/HEAD/skills/runtimes/sanitizers/SKILL.md — 逐字："ASan and TSan usually run separately. Their runtime instrumentation mechanisms are not suited to run together"；`ASAN_OPTIONS=abort_on_error=1:detect_leaks=1`、`UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1`、`-fno-sanitize-recover=all` — 开源社区 SKILL 文档 — 2026-09 访问
9. **Tencent Cloud 开发者问答：`'clang_rt.asan_dynamic_runtime_thunk-x86_64.lib'：致命...`** — https://cloud.tencent.com/developer/ask/sof/106454598 — 描述 Windows + clang-cl 开启 ASan 时缺失 `asan_dynamic_runtime_thunk` 库导致链接失败 — 腾讯云社区 — 2021-09-16（访问 2026-09）
10. **LLVM Discourse：`ASAN with MinGW`** — https://discourse.llvm.org/t/asan-with-mingw/55887 — 讨论 Windows/MinGW 下 ASan 运行时支持有限、需完整 compiler-rt 配套 — LLVM 社区 — 2020-07-13（访问 2026-09）
11. **Google Sanitizers Wiki（AddressSanitizer 概览）** — https://github.com/google/sanitizers/wiki/AddressSanitizer — 概览：用 clang 带 `-fsanitize=address` 编译链接即可启用；错误以非零退出码中止 — Google / LLVM — 2026-09 访问
12. **Sanitizers 工具集（中文综述，含 ASan/UBSan/MSan/TSan 角色）** — https://www.cnblogs.com/kongzimengzixiaozhuzi/p/18364129 — 中文背景：Sanitizers 是 Google 发起的开源工具集，含 ASan/TSan/MSan/LeakSanitizer — 博客园 — 2024-08-17（访问 2026-09）
