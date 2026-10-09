# 人类标注材料包 · 保姆级使用说明（README）

> 本文件是**入口**。第一次拿这个包的人，请**从头读到尾**，大约 10 分钟。
> 配套文件：`annotation_guidelines.md`（判定规则手册，必读）、`annotation_template.csv`（145 条盲标表）、
> `calibration/`（10 道校准题 + 答案）、`sources/`（145 个去标识化源码）、`TABLE_GUIDE.md`（表格字段逐条解释）。
> 31 条"AI 分歧裁决集"见仓库根 `data/702_annotation_table.csv`（难度已排序，含留空的 `your_verdict` / `your_notes` 两列）。

---

## 0. 一句话：你到底要干什么

你有 **145 个去标识化的 C++ 小程序**（每个 2–40 行，没有文件名、没有作者、没有"正确答案"）。
对每一个，你要回答**一个问题**：

> **在下面规定的"检测条件"下，8 个检测设施里，有没有任意一个会报出诊断（警告 / 报错 / 运行时报告）？**

- 有 ⇒ 填 `catch`
- 没有 ⇒ 填 `miss`
- 拿不准 ⇒ 仍要选 `catch` 或 `miss`，但把 `confidence` 调低、在 `notes` 写清卡点

**最重要的认知（也是本论文的核心发现之一）：**
"检测器没报"（`miss`）**不等于**"代码没问题"。
很多真缺陷——逻辑错误、协议缺陷、调度 bug——在 8 个设施下**一个报告都没有**，
那它就该填 `miss`。你如实填 `miss` 不是判错，是在帮我们证明"仪器的能力边界"。

---

## 1. 标注什么（字段清单）

你主要填的是 `annotation_template.csv` 里的 **8 个字段**（逐条解释见 `TABLE_GUIDE.md`）：

| 字段 | 你填什么 |
|---|---|
| `expected_verdict` | `catch` 或 `miss`（核心判定） |
| `defect_type_family` | 8 大家族里选 1 个（memory / bounds / integer / alias_type / concurrency / stl / language_oop / embedded_link） |
| `defect_type_free_text` | 具体机制，中英文均可（如 `double_free`、`missing return`） |
| `planted` | 这是"人工构造的教学代码"吗？`true` / `false` / `unsure` |
| `severity` | 若在真实系统触发，后果多大：`low` / `medium` / `high` |
| `confidence` | 你有多确定：1–5（5 最确定） |
| `notes` | 判定依据、不确定点、发现的残留提示 |
| `your_verdict` / `your_notes` | **（仅 31 条裁决集 `data/702_annotation_table.csv` 有）** 你填的判定 / 备注，留空待填 |

> 注意：145 条盲标用 `annotation_template.csv`；31 条"AI 分歧裁决"用 `data/702_annotation_table.csv`。
> 两套表**不要混**：前者是完整盲标，后者是 AI 已经分歧、需要你拍板的难题。

---

## 2. 怎么标（四步流程）

1. **通读** `annotation_guidelines.md`（约 15 分钟，判定口径的唯一来源）。
2. **先做校准**：打开 `calibration/sources/C01.cpp … C10.cpp`，独立判完 10 道，
   再打开 `calibration/answers.csv` 对答案。分歧 ≥2 条 → 回读手册 §1 / §3，必要时问协调者。
3. **正式标注**：逐条填 `annotation_template.csv`。建议顺序与 `sample_list.csv` 一致：
   先读代码 → 写下判定 → 再填表。**不要猜**：不确定就用低 `confidence` + `notes`。
4. **交回**：把填好的 CSV 发给协调者（**不要改名、不要改列顺序、不要删行**）。

---

## 3. 标错了怎么办（不会扣你分，但有规矩）

- **标错本身不是问题**：本研究的 κ 阈值衡量的是"人机一致性"，不要求你和任何人事先一致。
- **交回后发现有错**：直接告诉协调者"某行我想改"，或在 `notes` 补一句即可，**不要偷偷改原始判定逻辑**。
- **`confidence` 低 + `notes` 写清** 比"硬选一个高置信"更有价值。不确定就诚实地说不确定。
- **盲性红线**：`sample_list.csv` 之外的任何"原始标签 / 来源 / 批次"信息**不要问、不要查**；
  发现的残留提示（如被 `[redacted]` 遮盖处）写进 `notes`，不要据此反推答案。
- **中途退出 OK**：交回已完成部分即可，退出样本标记为"未标注"，不进一致性统计。

---

## 4. 有问题找谁

| 问题类型 | 找谁 | 能不能问 |
|---|---|---|
| 判定规则疑问（可讨论口径） | 协调者（项目作者） | ✅ 欢迎 |
| 某个样本的原始标签 / 它到底是不是缺陷 | — | ❌ 盲性红线，任何情况不给 |
| 流程 / 交回方式 | 协调者 | ✅ |
| 隐私 / 署名 / 退出 | 协调者 | ✅ |

联系渠道：GitHub Issue 评论、邮件（`1026708211@qq.com`）、或直接消息协调者。

---

## 5. 常见问题（FAQ）

**Q1. 我不是 C++ 专家，能标吗？**
能，只要你满足招募页"Who we are looking for"里至少 3 条（写过 nontrivial C/C++、用过 sanitizer、
知道 `-Wall -Wextra` 大致报什么等）。看不懂的代码就 `confidence=1` + `notes` 写"看不懂"，不要硬编。

**Q2. 我可以编译运行这些样本吗？**
可以（依赖文件已随包提供）。但你的判定**必须基于 `annotation_guidelines.md` 的判据**，
而不是"我本地跑出来怎样"——设施的配置（-O0/-O2 双档、8 资产、特定判据字符串）和你的本地环境可能不同。

**Q3. 注释被 `[redacted]` 盖住了，影响判断吗？**
不影响核心判定（代码结构自足）。若某处被盖导致你无法判断，写 `notes` 并把 `confidence` 降 1。

**Q4. `miss` 太多是不是我判错了？**
不是。该语料约四成样本在 8 资产下无报告（38.4% 是已发表口径的一部分）；你的任务就是如实判定。

**Q5. `severity` 和 `catch/miss` 有关系吗？**
没有。`severity` 是"若在真实系统触发后果多大"，与"能否被检测到"完全独立。
一个 `high` 缺陷完全可能 `miss`（比如一个严重的逻辑错误，任何工具都不报）。

**Q6. `planted` 是问"有没有缺陷"吗？**
不是。它问的是"这段代码是不是为演示缺陷而人工构造的"（看结构是否极度最小、是否只为一个单点缺陷而写）。
干净的正常代码也算 `false`。这是"是否人工构造"的判断，不是"有没有缺陷"的判断。

**Q7. 时间不够怎么办？**
宁可少标、每条认真标，也不要疲劳赶工。交回时注明已完成的范围即可。

**Q8. 我的标注会怎么用？会以真名出现吗？**
结果以汇总统计形式用于论文。致谢中可按你要求**实名 / 化名 / 完全匿名**，你的选择。
你随时可以中途退出并交回已完成部分。

---

## 6. 标注示例（含正确答案 + 典型错误答案）

下面 3 个例子取自真实样本风格。**先盖住"正确答案"，自己判一遍，再对照。**

### 例 1 — 二次 `delete`（应判 `catch`）

```cpp
int main(){ int* p = new int(1); delete p; delete p; return 0; }
```

- ✅ **正确答案**：`expected_verdict = catch`，`defect_type_family = memory`，`defect_type_free_text = double_free`。
  AddressSanitizer 会直接报 `double-free`。
- ❌ **典型错误**：看到"代码能编译"就填 `miss`。错在——判据是"检测器报不报"，不是"能不能编译"。

### 例 2 — 函数实参求值顺序 unspecified（应判 `miss`）

```cpp
int g(){ printf("g"); return 1; }
int h(){ printf("h"); return 2; }
void f(int, int){}
int main(){ f(g(), h()); }
```

- ✅ **正确答案**：`expected_verdict = miss`，`defect_type_family = language_oop`。
  求值顺序是 *unspecified*（不是 UB），**任何 sanitizer / 编译器告警都不会报**。
- ❌ **典型错误**：觉得"这代码有隐患"就填 `catch`。错在——隐患 ≠ 检测器会报。`miss` 正是我们要你如实记下的"能力边界"。

### 例 3 — 对齐 UB（边界模糊，应判 `miss` 但需低置信 + notes）

```cpp
struct alignas(8) L { long long v; };
int main(){ alignas(2) char buf[sizeof(L)+8]; L* p = reinterpret_cast<L*>(buf); p->v = 1; }
```

- ✅ **正确答案**：`expected_verdict = miss`，`defect_type_family = alias_type`，`confidence = 2`，
  `notes = "alignas(2) 缓冲实际地址可能偶然 8 字节对齐，UB 是否触发不确定；-Wcast-align 不在 -Wall"`.
- ❌ **典型错误**：凭直觉填 `catch` 并给高置信。错在——这是"可能触发也可能不触发"的边界案例，
  诚实做法是低置信 + 写清不确定性，而不是硬选。

> 更多校准练习（带答案）见 `calibration/` 目录；10 道做完再开始正式标注。

---

## 7. 文件清单（你拿到了什么）

| 文件 | 说明 |
|---|---|
| `README.md`（本文件） | 保姆级入口 |
| `annotation_guidelines.md` | 判定规则手册（**开始前必读**） |
| `annotation_template.csv` | 145 条盲标表（你要填的） |
| `TABLE_GUIDE.md` | 表格字段逐条解释 + 难度排序说明 |
| `sample_list.csv` | 145 条样本清单（匿名 ID、文件、配套依赖） |
| `sources/S001.cpp … S145.cpp` | 去标识化源码（2 个配套 `.h`） |
| `calibration/` | 10 道校准题（C01–C10）+ 参考答案 `answers.csv` |
| `../702_annotation_table.csv` | 31 条 AI 分歧裁决集（难度排序 + 留空 `your_verdict`/`your_notes`） |

---

*本说明由 702 批次整理，配套 693-A 材料包。所有"建议"均为建议，最终判定以你的独立判断 + `annotation_guidelines.md` 口径为准。*
