# 692-B · 公平外部对比协议（**先于任何一次工具调用落盘**）

- 批次：692｜执行：CodeBuddy（AI）｜写盘时间：2026-10-08（**协议先落盘，跑之前**）
- 上游：`data/689_fair_comparison_protocol.md`（方案）、`data/673e_clang_tidy_cppcheck对比.md`（673e 既有对照）
- 本批在 689 §5 预注册草案基础上**执行 P1–P5 的第一步**：同一台机器、同一批样本、同一 truth labels、
  同一超时、逐样本落盘。**仍不是容器化同环境**（见 §6 诚实边界）。

---

## 0. 一句话定位（写死，不得在报告中松动）

> 本对比是 **convergent validity / cross-regime stress-testing**：
> 看三方在**哪些缺陷族收敛、哪些发散**。**不是 leaderboard，不 claim superiority over mature verifiers。**
> Queyi 的审计对象是**评估装置**（evaluation apparatus），不是另一个 verifier 的检出率。

---

## 1. 样本框架（F1/F2 公平性要求）

| 项 | 取值 |
|---|---|
| 帧 | `data/a5_676f_detection_matrix.json` 的 `split == "evaluation"`，n = **566** |
| 可跑子集 | 有源文件且文件在盘上者 **538**（534 `.cpp` + 4 `.h`） |
| 不可跑 | 28 条 legacy `(inline_code)` 样本无源文件 ⇒ **记 unknown，不记 miss** |
| truth labels | 冻结矩阵 `expected_verdict ∈ {catch, miss}`（**声明可检出性**标签，非「是否存在缺陷」标签；与 689 §2 F2 一致，单标注者威胁 T1 不变） |
| 附带上游标签 | `defect_group`（family8 归一化口径）、`or_verdict`（Queyi 8 资产 OR，比较基准） |
| 抽样 | **全量**（不是抽样）：566 全部进帧，能跑的 538 全跑，无可跑者如实登记 |

## 2. 工具与口径（**F4：先声明，禁止事后选最好的口径**）

本机实测可用（`--version` 已记录）：

| 工具 | 版本 | 路径 |
|---|---|---|
| clang-tidy | LLVM **22.1.8**（MSYS2/MinGW） | `C:\msys64\mingw64\bin\clang-tidy.exe` |
| cppcheck | **2.21.0**（MSYS2/MinGW，本批新装：`pacman -S mingw-w64-x86_64-cppcheck`） | `C:\msys64\mingw64\bin\cppcheck.exe` |

四个**同时报告**的口径（全部先声明；T1 与 T3 为预注册主口径，T2/T4 为宽口径敏感性）：

| 口径 | 命令（逐样本，**Windows native，不用 WSL**） | 记「有报告」的判据 |
|---|---|---|
| **T1** clang-tidy · C-main | `clang-tidy <file> --checks="-*,clang-analyzer-*,bugprone-*,cert-*,cppcoreguidelines-*" -- -std=c++17 -fsyntax-only` | 任一 `warning`/`error` 诊断 |
| **T2** clang-tidy · C-A | 同一次运行，**事后按 check 名前缀过滤** `clang-analyzer-*`（等价于只开这族，省一次运行；已声明为 673e 的事后口径 ⇒ 本批标**探索性**） | 任一 `clang-analyzer-*` 诊断 |
| **T3** cppcheck · warning | `cppcheck --enable=warning --std=c++17 --quiet --template="{file}:{line}:{severity}:{id}:{message}" <file>` | 任一 `severity ∈ {error, warning}` |
| **T4** cppcheck · broad | `cppcheck --enable=warning,performance,portability --std=c++17 ...`（同一次运行取全量） | 任一诊断（含 performance/portability） |

**T2 ⊆ T1、T3 ⊆ T4 是自明的包含关系**，报告里必须并排给，不允许只报好看的那一档。

## 3. 三组件记账（F5/F6）

- 超时：**60 s/样本/工具**（超时 ⇒ unknown）；不设 CPU/内存硬限。
- **unknown ≠ miss**：以下情形记 `unknown`（从分母剔除并逐条列出）：
  1. 源文件缺失（28 条 legacy）；
  2. 工具进程超时；
  3. 工具以**解析级致命错误**退出（cppcheck `--error-exitcode` 未用；以输出里 `syntaxError` / clang-tidy `error: unable to handle compilation` 判据），
  - 判据写死在脚本 `tool_status()` 里，**不看结果再改**。
- 指标（逐口径、逐工具）：
  - `catch = 有报告 ∧ expected_verdict == "catch"`；`miss = 无报告 ∧ expected == "catch"`；`unknown` 如上述；
  - `catch_rate = catch/total`、`unknown_rate = unknown/total`、`conditional_recall = catch/(catch+miss)`；
  - **另有反向指标**：`false_report_rate = 有报告 / expected == "miss"` 的样本数（F8：不对称性必须显式——Queyi 侧有 11 条对照的 FP 控制与四态，外部工具**无 unknown 概念**，其「无报告」在真错样本上就是 miss）；
  - `coverage = (total - unknown)/total`（哪一方能覆盖更多样本，本身就是公平性事实）。
- 交叉分歧（convergent validity 的核心表）：Queyi `or_verdict` × 工具报告 → 2×2（b/c 双向），
  并逐条列出 **Queyi 命中而工具静默** 与 **工具命中而 Queyi 未命中** 的 `defect_group` 分布。

## 4. 逐样本落盘（P2）

`data/692_fair_comparison_raw.jsonl`：每行 = `{uid, sample_id, file, tool, caliber_inputs, rc, seconds, status, diags[{line,severity,id,msg}], raw_head}`。
可断点续跑（重跑命中已完成行则跳过）。汇总由 `data/692_fair_comparison_results.json` 现算，**不允许手抄**。

## 5. 判定标准（预注册）

| # | 判据 | 说明 |
|---|---|---|
| J1 | 四口径三组件全部落盘，且 `coverage` 逐口径报出 | 缺一即本批不完整 |
| J2 | 若某口径的 `false_report_rate` ≥ 95%（即几乎全报）⇒ 判定**该口径零判别力**并如实保留（673e 已出现此形态，不得因难看而撤） | 预注册失败是结果，不是事故 |
| J3 | 结论只写「收敛/发散 + 族分布」，**不得**出现「优于/胜过/超过」 | 语气红线 |
| J4 | 与 673e 的结果若不一致，**两者并排**报，找原因（版本变 / 样本框架变 / 口径变），不得只留新的 | 621 口径纪律 |

## 6. 诚实边界（不得省略）

1. **不是容器化同环境**：clang-tidy 与 cppcheck 虽同在本机 Windows native 进程内运行，但二者**不是同一编译环境**
   （clang-tidy 用 LLVM 22 的前端与 MinGW 头文件，cppcheck 无编译期）；且与 Queyi 的检测环境（WSL g++13.3 + sanitizer）
   **本质不同**（静态 vs 动态）。"完全同一环境"在本研究对象上**不可达**，只能把四方各自的环境指纹一并报出（692-A 的 EnvironmentProfile）。
2. **T2 是 673e 的事后口径**：本批在跑之前声明它，只把「事后选」降级为「自报的事后口径」，**不洗成预注册**。
3. **truth labels 是 `expected_verdict`（声明可检出性）**，不是「人审过的真值」；人类 IAA 仍为 0（本批不伪造，不补）。
4. 外部工具**无 unknown 概念**：其「无报告」在真错样本上记 miss —— 这是**已知不对称**，不是疏漏。
5. 673e 的 136 条框架（60 holdout + 76 corpus）与 692 的 566 框架不同 ⇒ 两批数字**不可直接比**，只可并排看方向。

---

复算：`python tools/run_692_fair_comparison.py`（`run` 模式会真跑工具；`--analyze` 只从 raw jsonl 汇总）。
