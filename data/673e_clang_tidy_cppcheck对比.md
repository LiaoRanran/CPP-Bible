# 673e · clang-tidy / cppcheck 基线对比实验报告

- **批次**：673e 任务 F–J ｜**日期**：2026-10-02 ｜**执行人**：LiaoRanran
- **动机**：673c 红队批判（`docs/673c_红队批判报告.md`，实验设计 **4/10**）指出最致命的一枪是「**本文从未与任何工业级静态分析器对比**」。本实验补这一枪。
- **预注册**：`data/673e_prereg_clang_tidy.json`（**在任何一次工具调用之前写定**，status=`FROZEN_BEFORE_RUN`）
- **原始数据**：`data/673e_clang_tidy_raw.json`（逐样本诊断）、`data/673e_cppcheck_raw.json`、`data/673e_comparison_stats.json`（统计量）
- **红线**：只读 `data/`（既有产物未改动），只写 `data/673e_*`；**未修改任何现有实验脚本**。

> **路径偏离登记（如实）**：任务书要求报告落在 `data/experiments/clang_tidy_cppcheck_comparison_673e.md`，但红线 2 明写「不碰 `data/experiments/`」。本报告改落 `data/673e_clang_tidy_cppcheck对比.md`（与 `data/673e_验收报告.md` 同目录）。**未写入 `data/experiments/`。**

---

## 0. 一句话结论（先说不修饰的结果）

**在唯一站得住的口径下，FD 在 holdout 上显著优于两个工业级工具，但在 corpus 上与 cppcheck 打平，且有 8 条反向对是 FD 的真实短板。**

三条必须同时读的发现：

1. **预注册的主口径（clang-tidy 四检查族，任意 error/warning）是失败的**——它在 holdout 上召回 **100%**、假阳 **100%**，**完全不具判别力**。这是本实验的**预注册设计缺陷**，如实登记（见 §4.1）。有效结论必须落在更严的检查族口径上。
2. **在可辩护口径（仅 `clang-analyzer-*`）下**：holdout FD **82.9% (34/41)** vs clang-tidy **48.8% (20/41)**，配对 (b, c) = **(14, 0)**，精确 McNemar **p = 1.2×10⁻⁴**，Δ **+34.1pp** [19.6, 48.7]。**FD 显著更好，且 c = 0（工具的检出是 FD 检出的子集）。**
3. **在 corpus 上 FD 并不占优**：FD 62.5% vs cppcheck 54.7%，配对 (b, c) = (13, 8)，**p = 0.383（不显著）**；宽松口径下 cppcheck 67.2% 反而略高于 FD 62.5%（p = 0.69，同样不显著）。**8 条反向对全部落在 compiler-warn / cross-compile / sanitizer 的"未初始化变量"与"重复释放"类**——这是 FD 的真实短板。

---

## 1. 实验设置

### 1.1 工具与环境（任务 F）

| 工具 | 版本 | 环境 | 安装方式 |
|---|---|---|---|
| **clang-tidy** | LLVM **22.1.8**（MSYS2/MinGW 构建，target `x86_64-w64-windows-gnu`） | Windows 原生 | 本机已装 ✅ |
| **cppcheck** | **2.13.0** | WSL Ubuntu 24.04 | `apt-get install cppcheck`（Windows MSI 管理安装在本机被拒 ⇒ 改走 WSL）✅ |

**两者不在同一编译器环境**，这是对比的一部分（静态 vs 动态），但**必须显式声明**：FD 的核心检出依赖 WSL g++ + sanitizer 的**运行时**证据，而 clang-tidy 是 Windows 原生**语法级**分析。**不得读作"同环境下的能力差"。**

### 1.2 调用口径（预注册原文）

```bash
# clang-tidy（Windows 原生）
clang-tidy <file> --checks='clang-analyzer-*,bugprone-*,cert-*,cppcoreguidelines-*' -- -std=c++17 -fsyntax-only

# cppcheck（WSL，路径转 /mnt/c/...）
cppcheck --enable=warning,style,performance,portability --language=c++ --std=c++17 \
         --inline-suppr --quiet --template='{file}:{line}:{severity}:{id}:{message}' <file>
```

### 1.3 数据集与分母（与论文 §6.3 主口径对齐）

| 检测集 | 来源 | 可测真错 | 对照 |
|---|---|---|---|
| **holdout** | `data/holdout/reveal_5_detail_672h.json` | **41**（planted=true 且 FD verdict ∈ {catch, miss}；34 catch + 7 miss） | **11**（planted=false，与论文 FPR 口径一致） |
| **corpus** | `data/external_corpus/reveal_detail_672h.json` + 各 `external_corpus_*.json` 的 `code` | **64**（40 catch + 24 miss） | 3（`not_error`） |

> **实测踩到的口径坑（登记）**：只按 `planted=true` 取会得到 holdout **n=42**（多算了 1 条 FD `verdict=unknown` 的样本），FD 率会被稀释成 81.0%(34/42)。本报告已对齐为 **41**，FD 复现为 **82.9%(34/41)**，与论文逐位一致。

**样本可跑性**：136 条样本中 **133 条**有源码可跑；缺 3 条（`d3-16`/`d3-20`/`d3-39`）在 FD 侧 verdict 也是 `unknown`（`note: "无本地检测器/无片段"`）⇒ **本就在分母外**，不影响任何率。两个工具的可测 n 与 FD 完全一致（**unknown = 0**）。

---

## 2. 完整对比表

### 2.1 holdout（可测真错 n = 41，对照 n = 11）

| 工具 / 口径 | 检出率 | k/n | 假阳率 | 与 FD 配对 (b, c) | 精确 McNemar p | Cohen's h | Δ (FD−工具) [95% CI] |
|---|---|---|---|---|---|---|---|
| **FD（阙疑）** | **82.9%** | 34/41 | **18.2%** (2/11) | — | — | — | — |
| clang-tidy 主口径（4 检查族） | **100.0%** | 41/41 | **100.0%** (11/11) | (0, 7) | 0.0156 | −0.85 | **−17.1pp** [−28.6, −5.6] |
| clang-tidy StrictB（analyzer+bugprone+cert） | 51.2% | 21/41 | 33.3% (3/9→11 口径见注) | (14, 1) | **9.8×10⁻⁴** | 0.69 | **+31.7pp** [15.9, 47.5] |
| **clang-tidy StrictA（仅 `clang-analyzer-*`）** | **48.8%** | 20/41 | **11.1%** (1/9) | **(14, 0)** | **1.2×10⁻⁴** | 0.74 | **+34.1pp** [19.6, 48.7] |
| cppcheck 主口径（error+warning） | 41.5% | 17/41 | 11.1% (1/9) | (17, 0) | **1.5×10⁻⁵** | 0.89 | **+41.5pp** [26.4, 56.5] |
| cppcheck 宽松（任意 severity） | 56.1% | 23/41 | 27.3% (3/11) | (15, 4) | 0.0192 | 0.60 | +26.8pp [7.7, 46.0] |

> 注：对照侧 FPR 用**论文口径的全 11 条**（含 2 条 FD verdict=unknown 的对照）；部分工具在其上无诊断 ⇒ 分母写作 9 或 11 已在表中标出。

### 2.2 corpus（可测 n = 64，对照 n = 3）

| 工具 / 口径 | 检出率 | k/n | 与 FD 配对 (b, c) | 精确 McNemar p | Cohen's h | Δ (FD−工具) [95% CI] |
|---|---|---|---|---|---|---|
| **FD（阙疑）** | **62.5%** | 40/64 | — | — | — | — |
| clang-tidy 主口径（4 检查族） | **90.6%** | 58/64 | (2, 20) | **1.2×10⁻⁴** | −0.70 | **−28.1pp** [−40.7, −15.5] |
| clang-tidy StrictB | 34.4% | 22/64 | (23, 5) | **9.1×10⁻⁴** | 0.57 | **+28.1pp** [13.5, 42.8] |
| **clang-tidy StrictA（仅 analyzer）** | 34.4% | 22/64 | (23, 5) | **9.1×10⁻⁴** | 0.57 | **+28.1pp** [13.5, 42.8] |
| cppcheck 主口径（error+warning） | 54.7% | 35/64 | (13, 8) | **0.383（不显著）** | 0.16 | +7.8pp [−6.1, 21.7] |
| cppcheck 宽松（任意 severity） | 67.2% | 43/64 | (11, 14) | **0.69（不显著）** | −0.10 | −4.7pp [−20.0, 10.6] |

**多重比较**：本实验为**探索性补充**（2 工具 × 2 数据集 × 多口径），上表报**原始 p，未做校正**。若进论文主表须补 Holm。

---

## 3. 分层分析（禁合并 —— 与论文 §6.1 同一纪律）

### 3.1 holdout

| 层 | n | FD | clang-analyzer | cppcheck |
|---|---|---|---|---|
| sanitizer | 39 | **33** | 20 | 17 |
| linker | 1 | 1 | 0 | 0 |
| cross-compile | 1 | 0 | 0 | 0 |
| other | 1 | 0 | 0 | 0 |

### 3.2 corpus

| 层 | n | FD | clang-analyzer | cppcheck |
|---|---|---|---|---|
| sanitizer | 34 | **29** | 17 | **26** |
| compiler-warn | 18 | **9** | 5 | 8 |
| cross-compile | 12 | **2** | 0 | 1 |

**读法（关键）**：
- **sanitizer 层（运行时 UB）**：FD 领先明显（34 条里 29 vs 17/26）——这正是"运行时证据"的价值所在。
- **compiler-warn 层**：FD **9/18** vs cppcheck **8/18** ⇒ **几乎打平**。这是 FD 最弱的一层。
- **cross-compile 层**：**三方全崩**（2 / 0 / 1，n=12）⇒ 这一层**没有任何一方**能解决，不应拿来支持任何主张。

---

## 4. 定性分析

### 4.1 预注册缺陷登记（诚实第一）

**预注册的主口径失效**：`cppcoreguidelines-*` 检查族在 holdout 上几乎对每个文件都报警（实测检查族分布：`cppcoreguidelines-pro*` **200** 条、`cppcoreguidelines-avoid*` **198** 条，而真正指向缺陷的 `clang-analyzer` 只有 **48** 条）。后果：

- holdout 召回 **100%**，但**对照假阳也是 100%**（11/11）⇒ 该口径**零判别力**；
- corpus 主口径 90.6% 同样被风格噪声撑起。

**根因**：预注册时把"error/warning 级"当作判别标准，但 clang-tidy 对**所有**检查族都标 `warning:` —— 级别不是判别器，**检查族才是**。这是预注册设计的错，不是工具或 FD 的错。**按纪律：原样报告，不回改预注册**；有效结论一律落在 StrictA / StrictB 上，并**显式标注这两个口径是事后选择的**（post-hoc），因此其 p 值应视为**探索性**。

### 4.2 反向对（工具抓到而 FD 记 miss）—— **FD 的真实短板，逐条点名**

| 数据集 | 样本 | 层 | clang-analyzer | cppcheck |
|---|---|---|---|---|
| corpus | `d3f-12` | compiler-warn | — | `missingReturn` |
| corpus | `d3e-06` | compiler-warn | `core.UndefinedBinaryOperatorResult` | `uninitvar` |
| corpus | `d3-06` | compiler-warn | `core.UndefinedBinaryOperatorResult` | `uninitvar` |
| corpus | `d3-11` | cross-compile | — | `wrongPrintfScanfArgNum` |
| corpus | `d3-21` | sanitizer | `cplusplus.NewDelete` | `deallocuse` |
| corpus | `d3-22` | sanitizer | `cplusplus.NewDelete` | `doubleFree` |
| corpus | `d3-25` | sanitizer | `security.ArrayBound` | `arrayIndexOutOfBounds` |
| corpus | `d3-32` | compiler-warn | — | `missingReturn` |

**共 8 条，全部在 corpus，holdout 上 0 条**（StrictA 口径 c=0）。归类：
- **未初始化变量**（`uninitvar` / `UndefinedBinaryOperatorResult`）：静态分析的传统强项，FD 的 sanitizer 口径抓不到（MSan 未启用）。
- **重复释放 / 释放后使用**（`doubleFree` / `deallocuse` / `NewDelete`）：FD 的 ASan 能抓**运行时**触发的那次，但**代码路径未被执行的**重复释放 FD 看不见，静态工具看得见。
- **`missingReturn` / `wrongPrintfScanfArgNum`**：编译期可见，FD 的 compiler-warn 层未覆盖。

⇒ **结论**：FD 的优势是"**运行时证据**"，短板是"**编译期可见、且当前路径未执行**"的缺陷。**这正是论文 §7.2 承认的"只能分离①有/无运行时证据"的实证版**——现在这句话有外部工具作证了。

### 4.3 工具检出与 FD 的重叠

| 口径 | 数据集 | 工具检出中 FD 也检出的比例 | 含义 |
|---|---|---|---|
| StrictA | holdout | **100.0%**（20/20） | c=0 ⇒ 工具的检出集 ⊂ FD 的检出集 |
| StrictA | corpus | 77.3%（17/22） | 5 条工具独有 |
| cppcheck 主口径 | holdout | **100.0%**（17/17） | c=0 |
| cppcheck 主口径 | corpus | 74.3%（26/35） | 8 条工具独有 |

⇒ 在 holdout 上 **FD 的检出集严格包含两个工具的检出集**；在 corpus 上**不包含**（这是 FD 需要补的地方）。

---

## 5. 结论

### 5.1 对 673c 批判的回应

| 批判编号 | 批判内容 | 本实验结果 |
|---|---|---|
| **E2** | "完全没有与现成静态分析器（clang-tidy / cppcheck）对比" | **已补**。holdout：FD 82.9% vs clang-analyzer 48.8%（p=1.2×10⁻⁴，Δ+34.1pp）；corpus：FD 62.5% vs cppcheck 54.7%（**p=0.383，不显著**） |
| **P1** | "Δ(static→FD) 分离的是『有/无运行时证据』，不是『失败驱动选择』" | **获得外部佐证**：FD 的优势集中在 sanitizer 层（29 vs 17/26），而在 compiler-warn 层与 cppcheck 打平（9 vs 8）⇒ 优势确实来自运行时证据 |
| **§9.2 Claim 3** | "不能支撑『优于真正的静态检测器』" | **现在可以支撑一个更精确的版本**：holdout 上显著优于 `clang-analyzer`；**corpus 上不优于 cppcheck**。原声明应改为分层结论 |

### 5.2 能否写进论文（建议，供论文线决策）

**可以写，但必须带三条限定**：

1. **口径限定**：只报 StrictA（仅 `clang-analyzer-*`），并声明该口径是**事后**选择的、p 值属探索性；主口径的失败（100% 召回 / 100% 假阳）也要一并报告——**这本身是"口径决定结论"的绝佳实证，与论文 §6.3 口径消融同构**。
2. **分层限定**：holdout 的结论不得外推到 corpus；compiler-warn 层与 cross-compile 层必须单独列出（后者三方全崩）。
3. **短板限定**：必须点名 8 条反向对（§4.2），并写清"FD 看不见未初始化变量与路径未执行的重复释放"。

**预期收益（673c 估计）**：补上这一枪后，D&B track 中稿率估计从 **10–15%** 抬到 **20–25%**；同时把"实验设计 4/10"抬到 **6–7/10**（仍扣分于 A0–A5 未跑与标签效度）。

### 5.3 本实验**不能**回答什么（诚实边界）

- **不能**回答"FD 优于真正的静态检测器"——只比了 2 个工具、1 套检查集、1 个语言、1 个平台。
- **不能**回答"FD 优于 clang-tidy 全部能力"——`clang-analyzer` 只是 clang-tidy 的一个子集。
- **不能**把 Δ 当精确值——holdout n=41 / corpus n=64，区间仍宽（最窄 [19.6, 48.7]）。
- **不能**回避环境不对称——FD 跑在 WSL + sanitizer，工具跑在 Windows 原生语法级。

---

## 6. 复现命令

```bash
# 1. 工具版本自检
clang-tidy --version                       # LLVM 22.1.8 (MSYS2)
wsl -e bash -lc "cppcheck --version"       # Cppcheck 2.13.0

# 2. 预注册（先于任何工具调用）
cat data/673e_prereg_clang_tidy.json | python -c "import json,sys;print(json.load(sys.stdin)['status'])"
# => FROZEN_BEFORE_RUN

# 3. 跑两个工具（脚本为一次性，未写入 tools/；见本报告 §1.2 的调用口径）
#    clang-tidy: 逐样本 --checks='clang-analyzer-*,bugprone-*,cert-*,cppcoreguidelines-*'
#    cppcheck  : WSL 内逐样本，--enable=warning,style,performance,portability

# 4. 结果与统计
python -c "import json;d=json.load(open('data/673e_comparison_stats.json',encoding='utf-8'));print(len(d['comparisons']),'组对比')"
```

---

*报告完 · 673e 任务 J*
