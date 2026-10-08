# 692-B · 公平外部对比结果（观察性 · convergent validity）

- 批次：692｜执行：CodeBuddy（AI）｜生成：2026-10-08
- 协议（**跑之前落盘**）：`data/692_fair_comparison_protocol.md`
- 现算产物：`data/692_fair_comparison_results.json`；逐样本原始：`data/692_fair_comparison_raw.jsonl`（1132 行）
- 复算：`python tools/run_692_fair_comparison.py --analyze`

**定位（写死）：本批是 convergent validity / cross-regime stress-testing。不是 leaderboard，不 claim superiority。**
Queyi 审计的对象是**评估装置**，不是另一个 verifier 的检出率。

---

## 1. 实况（先报执行事实，再报数字）

| 项 | 值 |
|---|---|
| 样本帧 | A5 `split == evaluation`，n = **566**（`expected_verdict=catch` **322** / `miss` **244**；其中 `miss` 层含 **232** 条 planted + **12** 条干净对照，见 §2.1） |
| 实际跑 | 有源文件 **538**；28 条 legacy `(inline_code)` 无源 ⇒ **unknown（不记 miss）** |
| clang-tidy | **LLVM 22.1.8**（MSYS2/MinGW，Windows native）· 537 跑完 + **1 超时**（`D018`，60s 上限）· 中位耗时 0.16s |
| cppcheck | **2.21.0**（MSYS2/MinGW，Windows native，本批新装 `pacman -S mingw-w64-x86_64-cppcheck`）· **538 跑完**、0 超时 · 中位耗时 0.03s |
| 口径 | T1/T2 = clang-tidy 主口径族 / 探索族；T3/T4 = cppcheck warning / broad；**四档全报**（包含关系自明：T2⊆T1、T3⊆T4） |
| 未跑 | 无（先声明的口径一个不留；超时样本如实登记为 unknown） |

## 2. 四口径 + Queyi 参照（同一帧、同一 truth labels、同一 60s 超时）

**分层记账**（不分层合并分母）：`catch/miss/unknown` 计在**声明正例层** \(n=322\)（`expected_verdict == catch`）；
`false-report rate` 计在**声明负例层** \(n=244\)；`coverage` 计在**整帧** \(n=566\)。

| 口径 | catch | miss | unknown | conditional recall | false-report rate | coverage |
|---|---:|---:|---:|---:|---:|---:|
| **T1** clang-tidy · C-main（预注册主口径） | 288 | 18 | 16 | 94.12% | **97.40%**（225/231） | 94.88% |
| **T2** clang-tidy · C-A（探索性） | 107 | 199 | 16 | 34.97% | 13.85%（32/231） | 94.88% |
| **T3** cppcheck · warning | 152 | 154 | 16 | 49.67% | 18.10%（42/232） | 95.05% |
| **T4** cppcheck · broad | 155 | 151 | 16 | 50.65% | 19.40%（45/232） | 95.05% |
| 参照：**Queyi 8 资产 OR**（冻结矩阵 `or_verdict`） | 302 | 20 | 0 | 93.79% | 15.57%（38/244） | 100% |

- `conditional recall = catch/(catch+miss)`（分母只含**可判定**的正例）；`false-report rate = 有报告 / 可判定的声明负例`；
- 各口径的整帧 unknown 数：clang-tidy **29**（28 条无源 + 1 条 60s 超时，分摊到两层为 16 正 / 13 负）、cppcheck **28**（全为无源）；
- Queyi 的 `coverage = 100%` 是**帧内自明**（它没有"跑不起来"的样本），对外部工具**不可比**（后者按 60s 超时与源文件可得性记账）；
  这条不对称性本身就是协议 F5/F6 要求报出的内容，**不是 Queyi 的优势**。

### 2.1 一个必须写明的口径事实：declared negatives ≠ 干净样本

`expected_verdict == miss` 的 **244** 条里，**232 条是 `planted=true`**（植入的缺陷，只是落在参考协议
声称可检出区之外），只有 **12 条**是 `planted=false` 且参考也不期望检出。因此：

- §2 表的 `false-report rate` **只能读作「能力分歧率」**（工具说有问题、参考说不指望检出），
  **不能读作误报率**——对那 232 条来说，工具"报出来"未必错，只是与参考的能力声明不一致；
- 真正的 FP 只能看**最干净的一层**（`planted=false ∧ expected=miss`，n=12）：

| 口径 | 干净对照上出报告 | FP 率（12 条） |
|---|---:|---:|
| T1 clang-tidy · C-main | **12/12** | **100.0%** |
| T2 clang-tidy · C-A | 0/12 | 0.0% |
| T3/T4 cppcheck | 3/12 | 25.0% |
| 参照：Queyi 8 资产 OR | 3/12 | 25.0% |

⇒ **同一份测量的两种读法差别很大**：T1 在「能力分歧」口径下是 97.40%，在「干净对照」口径下是 **100%**；
T2 从 13.85% 掉到 **0%**。这正是本批要证明的那件事：**指标随口径移动，口径必须随数字一起报。**

## 3. 预注册判据 J2 命中：T1 零判别力（**保留，不撤**）

`T1` 的 false-report rate = **97.40%**（231 条可判定的 `expected==miss` 里 225 条也被报"有问题"），
同时 conditional recall 94.12%，且在**干净对照层上是 12/12 = 100%**（§2.1）。
即：`T1` 的输出几乎与标签无关（537 次可判定运行里 **513 次出报告**）——
**这是「零判别力」（输出近似常量、无法区分标签）的统计学陈述，不是「报得都不对」的断言**。这不是事故，是**预注册口径的失败形态**：

- 673e 在 136 条框架上首次出现该形态（"主口径 100%/100%"，当时记为预注册设计缺陷）；
- 本批在 **566 框架、口径先声明**的条件下**复现**（94.12% / 97.40%）⇒ 该形态不是小样本噪声；
- 结论：`cppcoreguidelines-* + cert-* + bugprone-*` 这一族在这批样本上不是判别器，近似"是否由人写 C++"的分类器。
  **不得因为难看而剔除**；论文里它必须与 T2 并排出现。

`T2`（仅 `clang-analyzer-*`，673e 的**事后口径**）给出 34.97% / 13.85% —— 有判别力但召回低。
**T2 是本批先声明的事后口径，不得洗成预注册**（协议 §2 已写死）。

## 4. 交叉分歧（convergent validity 的核心证据）

以 Queyi `or_verdict` × 工具报告做 2×2（剔除 unknown）：

| 口径 | Queyi∩工具 | **Queyi∩¬工具** | **¬Queyi∩工具** | 都不报 |
|---|---:|---:|---:|---:|
| T1 | 300 | 18 | 213 | 6 |
| T2 | 109 | **209** | **30** | 189 |
| T3 | 158 | **160** | **36** | 184 |
| T4 | 161 | **157** | **39** | 181 |

**双向分歧的族结构（T2/T3 为主对照）**：

- **Queyi 抓到而静态工具静默**：T2 共 209 条，集中 `stl` 60 / `concurrency` 57 / `undefined_behavior` 22 / `embedded` 17 / `real_world` 15；
  T3 共 160 条，集中 `concurrency` 58 / `stl` 27 / `real_world` 25 ——
  ⇒ **`concurrency` 是静态工具的整片盲区**：cppcheck 在本帧 59 条 concurrency 上 **0 命中**，clang-analyzer 仅中 2 条。
  这与检测机制一致（数据竞争需运行期交织，静态工具只能做语法/数据流近似），**不是 Queyi 的"胜利"**，
  而是"两种 regime 看到的东西不同"。
- **静态工具报到而 Queyi 的 OR 未命中**：T2 30 条、T3 36 条，集中 `memory_safety`（14 / 10）、
  `language_semantics`（11 / 1）、`optimization_sensitive`（T3 8）——
  ⇒ 静态层覆盖了部分需要**触发条件**才报的缺陷（未初始化路径、语义误用），以及 `odr_link` 族的一部分。

**读法（三条，不得升级为"优于"）**：
1. 三方分歧**按族结构分化**：运行时层垄断 concurrency 与动态内存；静态层补上部分未初始化/语义误用；
2. 本帧没有任何一方同时取得高召回与低误报（T2 低误报但召回 35%；T1 高召回但误报 97%）；
3. Queyi 的 93.79% / 15.57% 是在 **8 资产、跨两个 OS** 的环境下取得的（3 个 sanitizer 依赖 WSL）；
   环境一撤退化为 24.74% 且可信负例归零（692-A）。**报 Queyi 的数字必须同时报它的环境前提。**

## 5. 对 SV-COMP 定位的回应（"为什么这又不是一个 verifier 排行榜"）

| 排行榜问题 | 本批的回应 |
|---|---|
| 同任务格式？ | 不是。样本是 **C++ 缺陷夹具**（外加真实靶场 110 条），不是 SV-COMP 的 C 验证任务 + 属性规范 |
| 同环境？ | **不可达**（静态 vs 动态；MinGW vs WSL）。本批只能把四方环境指纹一并报出（692-A 的 15 字段 `EnvironmentProfile`） |
| 同口径预注册？ | 本批做到了"先声明再跑"（T1–T4 全部先写死），但**不能**替成熟 verifier 规定口径 |
| 那你的主张是什么？ | **审计评估装置**：本批真正证明的是「换口径/换环境会改变结论」——T1↔T2 之间召回从 94.12% 变 34.97%，**同一份测量、同一批样本** |
| 结论口径 | 三方在**哪些族收敛（静态层与运行时层在 memory_safety 上重叠）、哪些族发散（concurrency）**；不写"优于" |

## 6. 与 673e 的并排（J4 口径纪律）

| 维度 | 673e（上一批） | 692（本批） | 处理 |
|---|---|---|---|
| 框架 | 136（60 holdout + 76 corpus） | 566（A5 evaluation，538 可跑） | **不可直接比**，只并排看方向 |
| clang-tidy 主口径 | 100% / 100%（零判别力） | 94.12% / 97.40%（零判别力） | 形态**复现**，幅度随框架移动；两值都留 |
| clang-analyzer 口径 | FD 82.9% vs 48.8%（holdout），p=1.2e-4 | Queyi OR 93.79% vs C-A 34.97%（不同帧，不做检验） | 方向一致（运行时 > 静态），**本批不引 673e 的 p 值** |
| cppcheck | corpus FD 62.5% vs 54.7%，p=0.383 | T3 49.67% / T4 50.65% | 方向一致（静态工具在中段），不同帧不做检验 |

## 7. 诚实边界（不得省略）

1. **不是容器化同环境**：clang-tidy 与 cppcheck 同在本机 Windows native 运行，但二者不是同一编译环境
   （cppcheck 无编译期），且与 Queyi 的 WSL + sanitizer 检测环境**本质不同**（静态 vs 动态）。
2. **T2 是事后口径**（673e 选出来的），本批在跑之前声明它，把"事后选"降级为"自报的事后口径"，**不洗成预注册**。
3. **truth labels = `expected_verdict`（声明可检出性），不是人审真值**；人类 IAA 仍为 **0**，本批不伪造。
4. **外部工具无 unknown 概念**：其"无报告"在真错样本上记 miss —— 已知不对称，逐条体现在 §2 的 coverage 列。
5. clang-tidy 有 **1 条超时**（`D018`，60s）——如实记 unknown，未调参重跑（调参=事后口径变更）。
6. 本批**没有**跑 SV-COMP 类工具（任务格式/基础设施不同），只做定位；**没有**改任何 verifier 配置；
   **没有**调用 Queyi 的 `detect()`（红线 1）。

---

复算：`python tools/run_692_fair_comparison.py --analyze`
