# 方向 32：PBT 属性测试最佳实践

> 调研日期：2026-09-29　联网搜索 14 次（1 次 524 超时失败）　WebFetch 4 次　curl+PDF 提取 3 份原文
> 锚点：阙疑 / queyi（C++ 知识验证器；67 条判决规则，block 44；holdout 30 真错 17，检出 66.7%）

## 核心结论

1. **PBT 的性价比不是"多跑几个用例"，而是"把断言从具体值提升为不变式"**——OOPSLA 2025 的 Python 实证给出最硬的反直觉结论：PBT 只占测试总数的 **1.6%**（350 条 PBT vs 21,222 条单测），却杀死 **15.3%** 的变异体（单测占 98.4% 的用例、杀死 84.7%），**按单条测试计的杀伤效率 PBT 显著高于单测**。对阙疑而言，这意味着"再加 100 条手写 holdout"的边际收益，可能低于"写 10 条真属性"。
2. **收缩（shrinking）是 PBT 唯一的、不可替代的差异化能力，但它的成本必须被显式预算**：Hypothesis 官方称其"test-case reduction is among the best in the world"；Jane Street 的开发者原话却是"**hate writing shrinkers**"（ICSE 2024, P4）。C++ 侧若用 RapidCheck/FuzzTest，自定义生成器必须自己写 shrink，这是最容易低估的工作量。
3. **PBT 与 sanitizer/UB 检测不是"叠加"关系而是"分工"关系**：PBT 提供**输入的多样性**，sanitizer 提供**判决的 oracle**。关键警告——UBfuzz（arXiv:2401.04538, 2024）证明**sanitizer 自身的实现也有 bug**，因此不能把"ASan 没报错"当作"无 UB"的充分证据；阙疑的四态判决（真/假/未知/错误）恰好是这个问题的正确抽象。

---

## 精确数字与案例

### 1. 起源：QuickCheck（2000）定下的三条契约

**论文**：Koen Claessen, John Hughes, *"QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs"*，**ICFP 2000**，DOI **10.1145/351240.351266**（ACM SIGPLAN Notices 35(9): 268–279）。PDF 镜像：https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf

QuickCheck 确立了 PBT 的三条契约，此后 26 年无人改动：
1. **属性 = 关于程序输入输出的、对所有合法输入都应成立的关系**，写成可执行的布尔函数；
2. **默认测试次数 100**（`Test.QuickCheck` 的 `stdArgs` 中 `maxSuccess = 100`，`maxDiscardRatio` 控制被 `==>` 前置条件丢弃的比例）；
3. **反例收缩 + size 参数**：官方手册（https://www.cse.chalmers.se/~rjmh/QuickCheck/manual.html ，2007）原文："**The purpose of size control is to ensure that test cases are large enough to reveal errors, while remaining small enough to debug**"——即"大到能暴露错误，小到能调试"，这句话就是 shrinking 的完整设计哲学。

QuickCheck 论文中最著名的教学案例是 `reverse . reverse == id` 与"插入排序漏了相等元素"的 bug：随机输入自动生成 `[0,1,2]` 级别的最小反例，而手写测试几乎不可能猜到。

### 2. Python 侧：Hypothesis 的默认值与"失败回放"机制（工程落地的全部细节）

**官方文档**：https://hypothesis.readthedocs.io/en/latest/tutorial/settings.html （2026-09 版本 6.168.3）。原文与默认值：

| 设置 | 默认 | 语义 |
|---|---|---|
| `max_examples` | **100** | 文档原文："**By default, Hypothesis will stop after generating 100 test cases**" |
| `deadline` | **200 ms** | 单个用例墙钟时间上限；超时触发 `deadline` 失败（**此 200 为社区与文档常见值，本次未逐字抓取 reference 页确认，见盲区**） |
| `phases` | `explicit, reuse, generate, shrink, explain` | 五个阶段；`explicit` 跑 `@example`、`reuse` 回放数据库、`generate` 生成、`shrink` 收缩、`explain` 解释 |
| `database` | `.hypothesis/examples/` | 失败用例持久化目录；**第二次运行会立即复现第一次的失败** |
| `derandomize` | `False` | 置 `True` 后 Hypothesis 变确定性（配合 `--hypothesis-seed`） |
| `verbosity` | `normal` | 调试时置 `verbose` |

**Profile 机制（CI 落地的关键）**：文档给出三段式写法——

```python
from hypothesis import settings
settings.register_profile("fast", max_examples=10)
settings.register_profile("long", max_examples=1000)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))
```
配合 `pytest --hypothesis-profile fast` 即可在本地跑 10 例、在 CI 跑 1000 例。**建议存放位置**：文档原文指定 `conftest.py`（"the standard location to place this code is in a `confest.py` file"，原文有拼写错误）。

**健康检查（health checks）与 flaky 处理**——Hypothesis 用健康检查把"慢/无效"的 PBT 显式暴露为错误，而非默默变慢。已知检查项包括 `too_slow`、`filter_too_much`、`data_too_large`、`function_scoped_fixture`、`return_value`、`differing_executors`、`large_initialization`。官方立场（https://hypothesis.readthedocs.io/en/latest/how-to/suppress-healthchecks.html ）原文："**We strongly recommend that you suppress health checks as you encounter them, rather than using a blanket suppression**"——即**禁止全局一刀切 suppress**，必须逐条说明理由。这是审稿人检查"你是否在掩盖问题"的直接证据点。

> 第三方博客（python-testing-debugging.com）给出 `filter_too_much` / `data_too_large` 的判定阈值来自 `conjecture/engine.py`，并提到 `max_valid_draws = 10` 一类的内部常数。**该内部常数未经我逐行核实**，仅作线索登记（见盲区）。

### 3. JavaScript 侧：fast-check 的三条默认与"种子可复现"

**官方文档**：https://fast-check.dev/docs/introduction/what-is-property-based-testing/ 与 `/docs/introduction/getting-started`。原文要点：

- **默认 100 次/属性**："**fast-check will sample 100 inputs per test by default. This value is configurable globally and per-test.**"；可 `fc.assert(prop, { numRuns: 1000 })`。
- **种子化随机数生成器**："fast-check's arbitraries use a **seeded** random number generator... providing a seed can ensure that they are still deterministic and repeatable"；失败时会打印 seed。
- **`fc.pre(condition)` 优于 `.filter`**：前者跳过不满足前置条件的输入且**不计入测试次数**，后者会触发"过滤过多"的浪费。
- **Arbitrary 架构**（DeepWiki 对源码的整理）：`Arbitrary` 基类同时负责 `generate(mrng, biasFactor)` 与 `shrink(value, context)`；`Value` 类**携带 shrinking 上下文**，使得收缩无需重建整条生成路径。这是"高效收缩"的工程实现范式，值得抄。
- **内置 arbitraries 清单**（节选）：`integer/nat/float/double/bigInt`、`string/base64String/lorem/stringMatching`、`date/ulid/uuid`、`ipV4/ipV6/domain/webUrl/emailAddress`、`json/jsonValue`、`letrec/memo/entityGraph`、`func/compareFunc/compareBooleanFunc`。

**Stryker 家族的 regex 变异**（见方向 31）用的是 `weapon-regex`，只生成 Level 1 变异——**这提示 PBT 生成器也应有"最小生成"原则**：不要一次生成过于复杂的值。

### 4. 实证：PBT 到底能不能找 bug（三篇硬论文）

**（A）OOPSLA 2025《An Empirical Evaluation of Property-Based Testing in Python》**——Savitha Ravi, Michael Coblenz（UCSD），Proc. ACM Program. Lang. **Vol. 9, No. OOPSLA2, Article 412, 2025-10**。全文 PDF 已提取，核心数字：

- **语料**：从 Boa 数据集（截至 2024-10 快照）筛出 **426 个 import Hypothesis 的 Python 项目**，占 Boa 全量项目的 **0.42%**；项目平均 **29,972 行 Python**。
- **属性分类学**：归纳出 **12 类**属性断言，静态分析工具可覆盖语料中 **94%** 的 PBT（另一处写 "around 95%"），分类**互斥**。
- **12 类及占比**（Corpus / Test Set）：

| 类别 | 语料占比 | 测试集占比 |
|---|---|---|
| Constant Equality（与常量比相等） | **41.25%** | 38.71% |
| Commutative Paths（交换路径） | **23.40%** | 13.98% |
| Typechecking（其它类型检查） | 7.21% | 3.22% |
| Partial Roundtrip（部分往返） | 7.03% | 0% |
| Roundtrip（往返） | 6.99% | **29.03%** |
| Constant Bounds Checking（常量边界） | 6.05% | 1.08% |
| Generated-Expression Bounds Checking | 4.08% | 4.09% |
| Inclusion（包含关系） | 2.71% | 6.45% |
| Constant Inclusion | 1.79% | 0% |
| Generated-Expression Non-Equality | 1.26% | 1.08% |
| Constant Non-Equality | 0.84% | 1.08% |
| Exception Raising（抛异常） | 0.28% | 0% |

  语料与测试集分布差异经 **Fisher 精确检验 p = 0.0005**。**最强配对相关性**：constant bounds checking 与 constant inclusion，**相关系数 0.63**；roundtrip 与 partial roundtrip，**0.33**。
- **变异测试结论（RQ2）**：对 **40 个项目**做变异测试，每项目随机取 **100 个变异体**（共 4,000 个量级）。数据集含 **350 条 PBT + 21,222 条单测**。结果：单测占 **98.4%** 用例、杀死 **84.7%** 变异体；PBT 占 **1.6%** 用例、杀死 **15.3%** 变异体——**按单条测试平均，PBT 效率更高**。最有效的三类属性是 **Exception Raising、Inclusion、Typechecking**。
- **需要多少输入才能抓到 bug（RQ3）**：**55% 的变异体用 1 个输入就被抓住，76% 在前 20 个输入内被抓住**。实验把 Hypothesis 的默认输入数从 **100 提到 500**。
- **采用率数据（原文引 2023 年 25,000 名 Python 开发者调查）**：**5%** 的开发者使用 Hypothesis，排名**第 6 常用测试框架**。
- 原文的诚实结论：因为单测数量压倒性多，**总体上单测找的 bug 更多**（"unit tests found more bugs than PBTs"）。

**（B）ICSE 2024《Property-Based Testing in Practice》**——Harrison Goldstein, Joseph W. Cutler, Daniel Dickstein, Benjamin C. Pierce, Andrew Head（UPenn + Jane Street），DOI **10.1145/3597503.3639581**。方法：在 **Jane Street**（OCaml 为主）做 **30 场深度访谈**。关键发现：

- PBT 被用在"**high-leverage**"（高杠杆）场景，而非全量覆盖；
- **最常见的失败模式是"不知道该测什么属性"**——原文："the most common failure mode is actually not knowing what properties to test"；
- 开发者**讨厌写 shrinker**："[we] hate writing shrinkers"（P4）；
- Jane Street 的构建系统有 **1 分钟/库的超时**，PBT 常因超时被打断；
- 论文把 PBT 与 **expect tests**（快照测试）对比，认为二者强弱互补；
- PBT 与 fuzz testing 在 Jane Street 并存。

**（C）ICSE 2023 NIER《How Developers Implement Property-Based Tests》**——Matheus et al.，UFMG，DOI 见 IEEE Xplore 10336336。为 PBT 使用模式的初步研究，PDF：https://homepages.dcc.ufmg.br/~mtov/pub/2023-icsme-nier-pbt.pdf

### 5. 收缩（shrinking）的工程细节

- **定义**：Hypothesis 官方指南 `guides/strategies-that-shrink.rst` 原文："**Hypothesis' test-case reduction is among the best in the world, and our built-in strategies are carefully designed to [shrink]**"。
- **目标性质**：收缩目标是**极小反例**（1-minimal：删掉任一元素后不再失败）。fast-check 的表述更直观：失败输入 `[17, -3, 99, 42, 0, 5, 23]` 会被收缩到"仍能触发 bug 的最短列表"。
- **必须自己写 shrink 的两种情形**：(1) 自定义 `Arbitrary`（fast-check 需实现 `Arbitrary` 类的 `shrink` 方法）；(2) 用 `.map`/`.chain` 时**继承**源 arbitrary 的 shrink，但**语义可能错位**（map 后的值再收缩可能落到非法域）。**这条是 PBT 最常见的隐性 bug 来源**。
- **成本**：收缩需要**反复重跑属性**，因此 PBT 的"最坏用例耗时"≈ `max_examples × (1 + 收缩候选数)`。这是 Jane Street "1 分钟/库超时"被打断的根因。

### 6. C++ 侧：三条可选路线与各自的边界

| 工具 | 定位 | 关键事实 |
|---|---|---|
| **RapidCheck** | C++ 版 QuickCheck 克隆 | https://github.com/emil-e/rapidcheck ；"QuickCheck clone for C++"；自带 shrink |
| **FuzzTest**（Google） | **覆盖率引导 fuzzing + PBT 的融合** | https://github.com/google/fuzztest ；README 原文："a **first-of-its-kind** tool that bridges the gap between fuzzing and property-based testing, as it is **both**"；"Currently, **only C++ is supported**"；被定位为 **libFuzzer 的继任者**；README **未给出** FuzzTest 自身的 bug 计数与性能数字（原文"数万个 bug"是泛指整个 fuzzing 领域，链向 OSS-Fuzz trophies） |
| **libFuzzer** | 覆盖率引导 fuzzer（非 PBT） | https://llvm.org/docs/LibFuzzer.html |

**关键区分**（OOPSLA 2025 原文）：fuzzer 检测的是**预定义的错误行为**（crash、安全 bug），PBT 检测的是**开发者写下的任意属性**；且"property-based tests run on a **set number** of inputs"（Hypothesis 是 100），而 fuzzer 是持续运行的。**二者不可互相替代**。

### 6. 生成器设计：PBT 里真正会翻车的地方

OOPSLA 2025 的 12 类属性分类告诉我们"写什么属性"，但**属性写对了、生成器写错了，测试依然无效**。四条具体的生成器陷阱：

1. **前置条件用 `.filter()` 而非 `fc.pre()`**：fast-check 官方明确指出 `fc.pre(condition)` **跳过不满足条件的输入且不计入测试次数**，而 `.filter()` 会把被丢弃的输入计入 `numRuns`。后果：如果你过滤掉 90% 的输入，`numRuns = 100` 实际上只测了 10 个有效输入，而**你从报告上完全看不出来**。Hypothesis 侧对应的问题是 `filter_too_much` 健康检查——它会**主动报错**而不是默默变慢，这是 Hypothesis 相对 fast-check 的一个明确工程优势。
2. **`map`/`chain` 之后的收缩语义错位**：fast-check 的 `.map`/`.chain` **继承**源 arbitrary 的 shrink 能力，但**收缩后的值可能落回 `map` 之前的定义域**，导致"收缩出的反例其实不满足你想要的形态"。例如 `fc.integer().map(x => x * 2)` 会收缩出奇数候选。**修法**：要么用 `.filter()` 兜底（但见第 1 条），要么直接实现自定义 `Arbitrary` 的 `shrink`。
3. **无种子不可复现**：fast-check 与 Hypothesis 都默认随机（Hypothesis 用 `derandomize=False`），失败时会打印 seed。**CI 里的正确做法**是：本地 `derandomize=True` 求快，CI 用 `--hypothesis-seed=0` 固定，另设一条**无种子**的定时任务每周跑一次——否则你会永远只跑同一批输入，而 PBT 的全部价值就在于"换输入"。
4. **状态化测试（stateful / model-based testing）的成本被低估**：Hypothesis 提供 `RuleBasedStateMachine`（文档原文："This module provides support for a stateful style of testing, where tests attempt to find a sequence of operations that [violates an invariant]"）。它的输入不是值而是**操作序列**，因此收缩必须收缩**序列**（删掉某些操作后是否仍失败）——**收缩复杂度从"元素级"升到"序列级"**。对阙疑来说，这恰好是验证"append-only 哈希链"最自然的 PBT 形态：把"追加一条记录"建模成一个 rule，"链不可回滚""哈希可复算"建模成 invariant，让 Hypothesis 去搜违反不变式的操作序列。**建议先用小状态机试水**，因为它对收缩成本的要求最高。

### 7. Ghostwriter：把"从零写属性"的门槛降到接近零

Hypothesis 内置 `hypothesis.extra.ghostwriter` 模块，官方定位（https://hypothesis.readthedocs.io/en/latest/reference/integrations.html ）："The idea is to provide an **easy way to start property-based testing, and a seamless transition to more complex test**"。它能为已有函数**自动生成**属性测试骨架（包括往返、等价、幂等等常见属性），开发者再人工确认/补强。

**对阙疑的用法**：`gate_engine.py` 有 3826 行，其中大量是纯函数（规则判定、哈希计算、四态判决的聚合）。**先用 ghostwriter 对纯函数批量生成属性测试骨架，再人工筛掉无意义的**，这是把 3826 行代码快速纳入 PBT 覆盖的最低成本路径。**注意**：ghostwriter 生成的是**骨架**，不是**正确的属性**——它无法替你判断"这个函数的不变式应该是什么"。这与 ICSE 2024 的核心发现一致：**最常见的失败模式是"不知道该测什么属性"**，而 ghostwriter 只能解决"不知道怎么写"。

### 8. 与 UB 检测结合：一个必须写进 Threats to Validity 的警告

- **分工模型**：PBT/生成器负责"**输入覆盖**"，ASan/UBSan/TSan 负责"**判决 oracle**"。典型工程写法是"PBT 生成随机输入 → 目标程序在 sanitizer 下运行 → 任何 sanitizer 报告即为反例 → 收缩输入 → 固化回归用例"。
- **警告（本次调研最重要的负面证据）**：**UBfuzz**（arXiv:**2401.04538**, 2024）证明**sanitizer 实现自身存在 bug**——该论文的框架专门用于验证编译器 sanitizer 实现的正确性。因此：
  - "UBSan 没报错" **≠** "无 UB"；
  - 阙疑的四态判决（真/假/未知/错误）在这里不是设计洁癖，而是**必需的诚实性**；
  - 反过来说，阙疑可以把"sanitizer 报告"作为**一条证据**而非**唯一证据**，这与论文 v0.3 的"证据带 provenance"主张一致。
- **编译档依赖**：`00_仓库扫描.md` 记录了论文 v0.3 的实测量化——"**`-O1`→`-O0` 使 3/5 miss 被同一 sanitizer 抓住**"。这说明 PBT+sanitizer 的组合对编译档**高度敏感**，必须在方法节声明编译档。
- **差分测试（differential testing）**：把 PBT 生成器接到"同一代码在 GCC/Clang/MSVC 三档编译"上，比较行为差异——这是阙疑"知识卡验证"最自然的 PBT 应用（对应 ROADMAP 方向 27）。

---

## 对阙疑的 3 条具体行动

1. **把 holdout 的"数量扩充"换成"属性化改写"，并做一次 OOPSLA 式的对照**。
   具体：从现有 **37 实卡（verified 23 / red-team 3 / draft 11）**中挑 10 张"语义型"卡片（如整数提升、序列点、`std::vector` 迭代器失效），把"手写期望输出"改写成 **12 类属性中的 3 类**：Roundtrip（`parse(print(x)) == x`）、Constant Bounds Checking（如 `size_t` 下溢必为极大值）、Exception Raising。然后对同一批被变异的核心逻辑跑两轮变异测试：**(a) 只用手写用例；(b) 手写 + PBT**，报告两组 kill 率与**每用例效率**。**预期与 OOPSLA 一致：PBT 用例数少但单位效率高**。这一条直接回应审稿人"你只是堆了 30 个样本"的质疑。

2. **建立"PBT 三件套"配置模板，落到 `_arch_v46/` 内的设计稿（不动仓库）**。
   具体三件套：(i) `settings.register_profile("ci", max_examples=500, deadline=None)` + `register_profile("fast", max_examples=10)`，用 `pytest --hypothesis-profile` 切换（**依据**：OOPSLA 论文把默认 100 提到 500 才抓到 76% 的变异体；Jane Street 有 1 分钟/库超时，所以 CI 档必须显式设 `deadline`）；(ii) **健康检查逐条登记表**（`too_slow` / `filter_too_much` / `data_too_large` / `function_scoped_fixture`），每条写"为什么抑制 + 替代措施"，**禁止 blanket suppress**（Hypothesis 官方立场）；(iii) **种子策略**：本地 `derandomize=True`，CI 用 `--hypothesis-seed=0` 固定 + 定期无种子跑一轮，并把失败种子写进 `.hypothesis/examples/` 的等价物（对 C++ 侧对应 RapidCheck 的 seed 输出）。**产出物**：`32_PBT配置模板.md`（写在 `_arch_v46/`），含可直接复制的 `conftest.py` 片段。

3. **给"收缩成本"设硬预算，并把"收缩失败"作为独立指标上报**。
   具体：在评测协议里新增一个指标 **`shrink_ratio = 收缩后反例规模 / 原始反例规模`**，以及 **`shrink_timeout_count`**（收缩超时次数）。**依据**：Jane Street 开发者明确"hate writing shrinkers"，且构建系统 1 分钟/库超时会打断 PBT——说明收缩是真实的工程瓶颈，而非细节。**执行**：对 C++ 侧用 RapidCheck，其自定义生成器需实现 `shrink`；对每张卡的自定义生成器，必须**同时提交一个"收缩正确性测试"**（构造一个已知反例，断言收缩结果是 1-minimal）。若做不到，就在论文中**诚实声明"本工作不做自定义收缩，只用内置生成器"**——这比虚报收缩能力安全得多。

---

## 盲区（诚实标注）

1. **Hypothesis 的 `deadline` 默认 200 ms 未逐字核实**：本次只抓到 tutorial/settings 页（未提默认毫秒数）与 GitHub Issue #1900（讨论 deadline 单位是毫秒），200 ms 是社区通行值。**写稿前必须抓 `hypothesis.readthedocs.io/en/latest/reference/api.html` 的 `settings.deadline` 条目确认**。
2. **Hypothesis 健康检查的完整清单与内部阈值（如 `max_valid_draws`）未逐行核实**：来自第三方博客（python-testing-debugging.com / blog.gitcode.com）与 `_modules/hypothesis/_settings.html` 的间接引用，**未读 `conjecture/engine.py` 源码**。
3. **OOPSLA 2025 论文的"12 类"中有 2 类的名称我未能完整确认**（表格中 `Test of Equality` / `Test of Inequality` 是分组表头还是类别名，PDF 文本流存在串行）；上表 12 行是按占比数值复原的，**类别名可能有个别偏差**。
4. **QuickCheck 的 `maxSuccess = 100` 默认值**：本次未抓到 hackage 的 `Test.QuickCheck` 源码页逐字确认，属"公认常识 + 手册旁证"，标为待核实。
5. **FuzzTest 的实测效果（找 bug 数、吞吐）完全未查到**：README 无数据，需读 `doc/overview.md` 或相关论文（本次未做）。
6. **RapidCheck 的维护活跃度、C++20/23 支持情况未核实**：本次只确认仓库存在与定位，未看 commit 时间线。
7. **未查到**：PBT 在 C++ 项目上的大规模实证研究（现有实证几乎全在 Python/Haskell/OCaml）；PBT 与 sanitizer 组合的量化收益研究；PBT 的 flaky 率统计数据。
8. **ICSE 2024 论文的 30 场访谈中，Jane Street 要求不披露实现细节**（原文："At Jane Street's request, we do not [disclose]..."），因此其结论的**可迁移性受限**（OCaml + 金融场景）。
9. 本文未跑任何 PBT，未修改仓库任何文件。

---

## 来源

1. Claessen, K.; Hughes, J. *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs*. **ICFP 2000**, ACM SIGPLAN Notices 35(9): 268–279. DOI **10.1145/351240.351266**（另一 DOI 10.1145/357766.351266）。PDF: https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf
2. QuickCheck 官方手册（R. J. M. Hughes, Chalmers, 2007）. https://www.cse.chalmers.se/~rjmh/QuickCheck/manual.html （"size control"原文出处）
3. Hypothesis 官方文档. *Configuring test settings*. https://hypothesis.readthedocs.io/en/latest/tutorial/settings.html （本次已抓全文；max_examples=100 原文出处）
4. Hypothesis 官方文档. *Suppress a health check everywhere*. https://hypothesis.readthedocs.io/en/latest/how-to/suppress-healthchecks.html
5. Hypothesis 官方指南. *strategies-that-shrink.rst*. https://github.com/HypothesisWorks/hypothesis/blob/master/guides/strategies-that-shrink.rst
6. Hypothesis 官方模块. *hypothesis.database / hypothesis._settings*. https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/database.html
7. Hypothesis 官方模块. *hypothesis.extra.ghostwriter（自动生成属性测试）*. https://hypothesis.readthedocs.io/en/latest/reference/integrations.html
8. Ravi, S.; Coblenz, M. *An Empirical Evaluation of Property-Based Testing in Python*. **Proc. ACM Program. Lang. 9(OOPSLA2), Article 412, 2025-10**. PDF: https://cseweb.ucsd.edu/~mcoblenz/assets/pdf/OOPSLA_2025_PBT.pdf （本次已 curl 下载并提取全文 32 页）
9. Goldstein, H.; Cutler, J. W.; Dickstein, D.; Pierce, B. C.; Head, A. *Property-Based Testing in Practice*. **ICSE 2024**. DOI **10.1145/3597503.3639581**. PDF: https://www.cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice （本次已 curl 下载并提取全文 13 页）
10. Matheus et al. *How Developers Implement Property-Based Tests*. **ICSME 2023 NIER**. IEEE Xplore 10336336. PDF: https://homepages.dcc.ufmg.br/~mtov/pub/2023-icsme-nier-pbt.pdf
11. fast-check 官方文档. *What is Property-Based Testing?* https://fast-check.dev/docs/introduction/what-is-property-based-testing/ （本次已抓全文；默认 100 次原文出处）
12. fast-check 官方文档. *Getting Started*. https://fast-check.dev/docs/introduction/getting-started
13. DeepWiki（对 fast-check 源码的整理）. *Arbitraries（Arbitrary/Value 类、generate/shrink 生命周期）*. https://deepwiki.com/dubzzz/fast-check/2.2-scheduler
14. Google. *FuzzTest*. https://github.com/google/fuzztest （本次已抓 README 全文）
15. emil-e. *RapidCheck — QuickCheck clone for C++*. https://github.com/emil-e/rapidcheck
16. LLVM. *libFuzzer — a library for coverage-guided fuzz testing*. https://llvm.org/docs/LibFuzzer.html
17. *UBfuzz: Finding Bugs in Sanitizer Implementations*. arXiv:**2401.04538**, 2024-01-09. https://arxiv.org/abs/2401.04538
18. python-testing-debugging.com. *Fixing Hypothesis FlakyHealthCheck Failures*（健康检查阈值线索，二手来源）. https://www.python-testing-debugging.com/property-based-fuzz-testing-strategies/hypothesis-framework-fundamentals/fixing-hypothesis-flaky-health-check-failures/
