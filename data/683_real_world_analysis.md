# 683-A3 · 真实靶场检出率深度分析（Real-World Detection Analysis）

- 生成：2026-10-07T19:48:51+08:00｜执行：CodeBuddy（AI）｜批次：683 究极收尾轮
- 样本：110 条真实缺陷（RW-001…RW-110）；检测：8 资产全量实测（WSL g++ 13.3 双档 -O0/-O2 + MinGW g++13.1/clang22.1 本地资产）
- 判定口径：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。`wunsequenced`/`compile-time` 在本工具链恒 unknown（不进分母、不当 miss）。
- 对照基线：1147 自造语料（676g 冻结矩阵，同 8 资产、同判定字符串）。

## 1. 总体检出率

- **8 资产 OR 检出率：59.09%**（65/110；unknown 0，miss 45）
- 自造语料 OR（同 6 可测资产口径）：61.64%；全 8 资产口径：61.64%
- 独立样本两比例 z 检验：z=-0.52，p=0.6，Cohen's h=0.052（**非配对**：两批样本独立，不能做 McNemar）

### 1.1 逐资产检出率（真实 vs 自造）

| 资产 | 真实 catch% | 自造 catch% | Δ(真实−自造) | z | p | Cohen's h |
|---|---:|---:|---:|---:|---:|---:|
| asan | 49.09 | 35.57 | +13.52 | 2.809 | 0.00496 | 0.275 |
| ubsan | 18.18 | 23.54 | -5.36 | -1.274 | 0.203 | 0.132 |
| tsan | 22.73 | 22.93 | -0.2 | -0.048 | 0.962 | 0.005 |
| compiler-warn | 4.55 | 12.47 | -7.92 | -2.462 | 0.0138 | 0.292 |
| wunsequenced | 0.0 | 0.0 | +0 | 0.0 | 1 | None |
| cross-compile | 20.0 | 10.64 | +9.36 | 2.945 | 0.00322 | 0.263 |
| linker | 0.0 | 0.87 | -0.87 | -0.983 | 0.326 | 0.187 |
| compile-time | 0.0 | 0.0 | +0 | 0.0 | 1 | None |

**读法**：Δ>0 = 真实靶场上该资产表现不低于自造语料；Δ<0 = 该资产在真实缺陷上退化（本表最重要的信息）。

### 1.2 按缺陷类型（真实靶场）

| 类型 | n | OR catch% | 最佳资产 | 最佳资产 catch% |
|---|---:|---:|---|---:|
| out_of_bounds | 38 | 84.21 | asan | 81.58 |
| logic_error | 31 | 3.23 | ubsan | 3.23 |
| integer_overflow | 14 | 71.43 | ubsan | 57.14 |
| use_after_free | 10 | 100.0 | asan | 80.0 |
| null_pointer_deref | 6 | 100.0 | asan | 100.0 |
| data_race | 4 | 75.0 | tsan | 75.0 |
| type_punning | 4 | 0.0 | asan | 0 |
| double_free | 2 | 100.0 | asan | 50.0 |
| memory_leak | 1 | 100.0 | asan | 100.0 |

### 1.3 按项目

| 项目 | n | OR catch% |
|---|---:|---:|
| curl | 16 | 56.25 |
| Linux kernel | 10 | 40.0 |
| OpenSSL | 10 | 60.0 |
| glibc | 8 | 62.5 |
| expat | 6 | 100.0 |
| libxml2 | 4 | 100.0 |
| Chromium/V8 | 3 | 0.0 |
| FFmpeg | 3 | 66.67 |
| FreeBSD | 3 | 0.0 |
| OpenSSH | 3 | 66.67 |
| Qt | 3 | 33.33 |
| libpng | 3 | 66.67 |
| libtiff | 3 | 100.0 |
| protobuf | 3 | 33.33 |
| Apache HTTP Server | 2 | 0.0 |
| Firefox | 2 | 100.0 |
| FreeType | 2 | 100.0 |
| ImageMagick | 2 | 50.0 |
| PostgreSQL | 2 | 50.0 |
| SQLite | 2 | 100.0 |
| nginx | 2 | 0.0 |
| sudo | 2 | 100.0 |
| zlib | 2 | 100.0 |
| Boost | 1 | 0.0 |
| CUPS | 1 | 0.0 |
| Chromium | 1 | 100.0 |
| Godot Engine | 1 | 100.0 |
| HTTP/2 协议栈（nginx/httpd/Go 等） | 1 | 0.0 |
| Redis | 1 | 100.0 |
| SQLite（Chromium 内置） | 1 | 100.0 |
| Unicode/LLVM/GCC 生态 | 1 | 0.0 |
| WebKit | 1 | 100.0 |
| XZ Utils | 1 | 100.0 |
| libssh | 1 | 0.0 |
| libwebp | 1 | 100.0 |
| ncurses | 1 | 100.0 |
| polkit | 1 | 0.0 |

### 1.4 按严重度（NVD CVSS 分级）

| 档 | n | OR catch% |
|---|---:|---:|
| HIGH+ | 81 | 61.73 |
| LOW/OTHER | 2 | 50.0 |
| MEDIUM | 27 | 51.85 |

### 1.5 按年份（NVD 首次发布）

| 年 | n | OR catch% |
|---|---:|---:|
| 2012 | 1 | 0.0 |
| 2014 | 1 | 100.0 |
| 2015 | 2 | 0.0 |
| 2016 | 8 | 50.0 |
| 2017 | 5 | 100.0 |
| 2018 | 6 | 50.0 |
| 2019 | 5 | 60.0 |
| 2020 | 9 | 66.67 |
| 2021 | 23 | 52.17 |
| 2022 | 29 | 65.52 |
| 2023 | 16 | 50.0 |
| 2024 | 5 | 80.0 |

## 2. 失败归因分析（miss 案例）

- miss 总数：45（OR 口径）；逐条深读见 `data/683_real_world_failure_cases.md`（≥30 条）。
  - `a_能力盲区_逻辑与并发语义`：30 条
  - `c_配置缺口_未启用检查`：8 条
  - `d_真实与自造的差异`：7 条

### 2.1 逐类归因展开

**（a）检测器能力盲区——逻辑与并发语义。** 内存/UB 检测器的可观测量是「程序在真实执行路径上的内存动作」与「未定义行为事件」；而逻辑绕过（如验证次序错误、协议降级、状态机误判）在内存动作层面**没有可观测量**：程序不越界、不竞争、不溢出，只是'做了不该做的事'。本批此类样本（logic_error 族）在 8 资产下的 OR 检出率显著低于内存安全族，这不是工具链缺陷，而是**检测范式的边界**——把这类缺陷纳入覆盖需要性质化测试（property-based）或状态机建模，超出了'检测器资产'的语义。
**（b）样本复杂度。** 真实缺陷常以多文件/跨模块形态出现；本批 PoC 以单文件重构为主（少数多 TU 样本：linker/ODR 类），因此'样本复杂度'在本批主要表现为**重构保真度的损失**：原始项目中的编译单元边界、头文件可见性、优化内联决策都会影响检测器行为（例如某些 UAF 在 LTO 下才暴露）。该损失的方向不可先验判定（可能高估也可能低估检出率），逐条登记在 notes。
**（c）配置缺口。** UB 家族中子类覆盖不均：有符号溢出、移位、对齐在 ubsan 默认面内；而无符号回绕、浮点转整溢出、部分指针算术面需要额外开关（`-fsanitize=unsigned-integer-overflow`、`float-cast-overflow` 等）。本批整数溢出族样本的部分 miss 属于此缺口——可通过扩开关修复，但会改变既有 676f/676g 口径，**本批不动**（口径冻结优先），登记为改进方向。
**（d）真实与自造的差异。** 合成语料的缺陷被设计为'检测器可观测'（否则无法进入评估）；真实缺陷没有这个先验——它们的可观测性由现实决定。因此两批样本的检出率差异**不应**被解释为'检测器在真实场景退化'，更准确的解释是：**自造语料对检测器能力做了选择性采样**。本批用同一把尺子（同 8 资产、同判定字符串）把两种分布都测了出来，差异即分布差异的量化。
**（f）不可复现/超时观测。** 挂起类样本（无限循环、永久等待、自死锁）在检测链中的观测为'运行超时→无报告→miss'。这是**观测口径的如实结果**：检测器对'程序不终止'这类缺陷本就没有（也无法有）基于报告的判定；要覆盖它需要超时/资源观测器（本项目挂起池的 hung_flag 即为此设计），本批如实保留而非硬造 catch。

## 3. 与自造语料的对比结论

1. **总体 OR：真实 59.09% vs 自造 61.64%**（独立样本两比例 z=-0.52，p=0.6，Cohen's h=0.052）——**无**显著差异（p>0.05，不能宣称谁更难）。这是一个**反直觉且重要的结果**：真实缺陷重构靶场与自造语料在本 8 资产口径下总检出率统计不可分；'真实一定更难'是未获支持的假设。
2. **结构性分化（真正的信息）**：剔除逻辑/挂起语义族后，剩余 79 条内存安全族样本 OR = **81.01%**；单纯逻辑/挂起族（n=31）OR = 3.23%。逐资产看：asan 在真实样本上**更强**（+13.52pp，p=0.005）、cross-compile 更强（+9.36pp，p=0.003），compiler-warn 更弱（−7.92pp，p=0.014）——差异的方向来自缺陷类型构成，而不是'anything real is harder'。
3. **恒定 unknown 两个资产（wunsequenced/compile-time）不在分母**：它们对 OR 检出率零贡献（OR 口径下本批 unknown=0——每条样本至少有一个资产给出确定判定）；但在**单资产口径**下这两个资产的 unknown 率是 100%，任何单资产分析都必须把它们排除——这正是'unknown 绝不当 miss'口径的价值。
4. **独苗命中 = 组合价值的直接证据**：见成功案例文件；这些样本在'单资产预算'下必漏，只有在组合预算下才被覆盖——与 682 的 Shapley 结论（asan +19.53pp 最大）方向一致。另注意**适用面差异**：linker 在合成语料上有 4 条不可替代 catch，而真实靶场 110 条均为单 TU 重构 ⇒ linker=0 catch；'资产在何种样本构成下才有触发面'本身是组合演化的输入信息（登记项）。
5. **第三方可核验性**：本报告所有数字的一条命令复算入口见 §4；NVD 验证记录（109 条原文）与 PoC 的 sha256 均冻结落盘，审稿人可在无网络的条件下核验'出处真实'（离线复算），或在有网络时对 NVD API 逐条回查（在线复核）。
6. **外部效度的提升与边界**：本批把证据从'自造样本'推进到'真实缺陷类别重构'，提升的是**生态效度**（缺陷形态、项目分布、年份跨度）；未提升的是**上下文保真度**（构建系统/跨模块依赖被简化）。此边界在论文附录 Real-World Validation 中显式声明，并建议后续工作以'构建可复现 Docker 化'方式补上下文保真。

### 3.1 逐类型深度透视（样本数 top-8）

- **`out_of_bounds`（n=38，OR 84.21%）**：覆盖 FFmpeg、Firefox、FreeType、Linux kernel、OpenSSH、OpenSSL等；最佳资产 asan（81.58%）。该族仍有 6 条 miss（如 RW-012），属 §2 归因中的相应类别。 改进方向：asan + 有界容器；对栈越界补 -fstack-protector/CFI 类告警面。
- **`logic_error`（n=31，OR 3.23%）**：覆盖 Apache HTTP Server、CUPS、FFmpeg、FreeBSD、HTTP/2 协议栈（nginx/httpd/Go 等）、ImageMagick等；最佳资产 ubsan（3.23%）。该族仍有 30 条 miss（如 RW-002），属 §2 归因中的相应类别。 改进方向：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。
- **`integer_overflow`（n=14，OR 71.43%）**：覆盖 Boost、ImageMagick、Linux kernel、Qt、Redis、SQLite等；最佳资产 ubsan（57.14%）。该族仍有 4 条 miss（如 RW-035），属 §2 归因中的相应类别。 改进方向：ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。
- **`use_after_free`（n=10，OR 100.0%）**：覆盖 Chromium、Firefox、Godot Engine、Linux kernel、OpenSSL、curl等；最佳资产 asan（80.0%）。该族全部被组合覆盖。 改进方向：asan 是主力；对'优化后路径才触发'的样本必须双档 -O0/-O2（本项目 666 起已强制）。
- **`null_pointer_deref`（n=6，OR 100.0%）**：覆盖 expat、libpng、libtiff、libxml2、protobuf；最佳资产 asan（100.0%）。该族全部被组合覆盖。 改进方向：ubsan null 面覆盖 + -fanalyzer（gcc13）补充。
- **`data_race`（n=4，OR 75.0%）**：覆盖 Linux kernel、OpenSSH；最佳资产 tsan（75.0%）。该族仍有 1 条 miss（如 RW-090），属 §2 归因中的相应类别。 改进方向：tsan 主力 + 压力重现（本项目 setarch -R 关 ASLR 稳定化）。
- **`type_punning`（n=4，OR 0.0%）**：覆盖 Chromium/V8、OpenSSL；最佳资产 asan（0%）。该族仍有 4 条 miss（如 RW-005），属 §2 归因中的相应类别。 改进方向：-fsanitize=undefined 的 alignment 子检查 + 强类型重构；联合体误用建议 clang -Wstrict-aliasing。
- **`double_free`（n=2，OR 100.0%）**：覆盖 OpenSSL、curl；最佳资产 asan（50.0%）。该族全部被组合覆盖。 改进方向：asan 覆盖；补所有权静态注释（-Wuse-after-free 已在 gcc13 默认 -Wall 面内）。

## 5. 局限与威胁（threats to validity）

- **构造威胁（construct）**：defect_type 为作者按 34 类词表标注；一条真实缺陷可能同时属于多类（如整数溢出→越界写），本批取'触发机制主类'，标注歧义在 682 的重标实验中已知（κ=0.73），逐条可复核。
- **内部威胁（internal）**：PoC 由同一作者（AI 辅助）重构，存在'按检测器可检出性重构'的无意偏置；缓解：重构以公开漏洞机制为准（NVD 描述驱动），且 30+ 条 miss 案例证明没有系统性'只写能检出的'。
- **外部威胁（external）**：110 条覆盖 30+ 项目，但长尾项目（小众库）缺失；年份跨度到 2024，2025-2026 的缺陷形态（AI 编写代码引入的缺陷）未覆盖。
- **结论威胁（conclusion）**：OR 检出率取决于 8 资产的选择；换资产集（如加入 MSan/Valgrind）会改变绝对值——本报告的一切数字均绑定'本 8 资产 + 本工具链'口径，不外推。

## 4. 口径与可复算

```
python data/realworld_683_runner.py --stage merge     # 判定矩阵
python tools/analyze_683_realworld.py                 # 本报告 + 两份矩阵
python tools/gen_683_realworld_benchmark.py --strict   # 元数据（含 sha256）
```

## 6. 复现细节（环境与命令）

- **检测环境**：WSL Ubuntu 24.04 + g++ 13.3.0（asan/ubsan/tsan；编译档位 -O0/-O2 双档，任一档报出即 catch；TSan 运行前缀 `setarch -R` 关 ASLR 以稳定报告）；本机 MinGW g++ 13.1.0（compiler-warn / cross-compile / linker）；cross-compile 对照编译器为 MinGW clang++ 22.1.8。
- **判定字符串**：与 `tools/holdout_reveal_661.py::detect` 的 SAN 分支逐字一致（asan: `AddressSanitizer` / `LeakSanitizer` / `detected memory leaks` / `double-free`；ubsan: `runtime error`）；检测器不可用（编译失败/工具缺失）一律 `unknown`，绝不记 miss。
- **超时口径**：sanitizer 运行单档超时 120s；挂起类样本（如 RW-002 无限循环）观测为超时→无报告→miss，这是如实测量结果（该样本一轮耗时可 ~18 分钟，已冻结在 checkpoint 中不重复燃烧）。
- **一致性保证**：checkpoint 增量落盘（`data/683_realworld_ckpt_detect.jsonl`）；合并由 `--stage merge` 完成（缺样 fail-loud，不静默跳过）；本轮修 include/平台兼容后**重跑了全部被修改的 11 条样本**，未沿用旧判定。
- **产物哈希**：每条 PoC 的 sha256 内嵌于 benchmark JSON（复算见 `gen_683_metadata.py --stage check`），任何内容漂移都会被检出。
