# Datasheet — `queyi-holdout-expansion`（676m 版 + 677a 来源三分类）

> 按 **Gebru et al. (2021), "Datasheets for Datasets"** 的九节格式编写。
> 本数据卡描述 `data/holdout_expansion/`（**1042 条扩样标注** + 对应 C++ 源码），
> 以及它们在论文中的两套上层切片（A5 的派生/评估切分、676g 的盲区地图并集清单）。
>
> - **版本**：676m（数据修复 + 实验重算）
> - **权威字段规范**：`data/holdout_expansion/SCHEMA.md`
> - **机器可读清单**：`data/676m_sample_manifest_corrected.json`、`data/a5_676f_sample_manifest.json`
> - **许可证**：Apache-2.0（与主仓一致）
> - **生成脚本**：`data/expansion_676c*/**`（生成） / `tools/fix_676m_schema.py`（676m 迁移）

---

## 1. 动机（Motivation）

**为什么创建？** 论文要回答的问题不是"某个检测器抓到了几个 bug"，而是
"**一个验证器的能力边界能不能被外部度量、被第三方打断、被自己否证**"。
这需要一个**每个格子都是真实检测器调用的判定矩阵**，而不是模拟分数。

**要解决什么？** 已有的 C++ UB 数据集要么是**纯变异体**（只证明工具能跑），
要么是**单检测器样本**（无法回答"多资产互补"），要么**没有跨批次标签统一**
（同一段代码在不同批次叫不同名字）。本数据集同时给出：

1. 每条样本的**缺陷种类、位置、是否人工植入、真实来源**；
2. 每条样本在 **8 个检测资产**（asan / ubsan / tsan / compiler-warn /
   cross-compile / linker / wunsequenced / compile-time）下的**真实判定**；
3. 明确的**观测口径**（`expected_verdict` = 独立检测器判据，挂起 = miss）。

**谁创建的？** 本仓作者（见 §8 维护）。**谁出资？** 无外部资助。

---

## 2. 组成（Composition）

### 2.1 规模

| 项 | 值 |
|----|----|
| 扩样样本 | **1042**（expA 100 / expB 94 / expC 200 / expD 200 / expE 200 / expF 149 / expG 99） |
| 每条样本文件 | 1 个 `.json` 标注 + 1 个或多个 `.cpp`/`.h` 源文件（expC 有 30 条多 TU 样本） |
| 源文件总数 | 1094 个 `.cpp`/`.h` |
| 历史层（不在本卡主体内） | holdout 41（`data/holdout/`）、corpus 64（`data/external_corpus/`） |
| A5 判定矩阵 | 1137 样本 × 8 资产 = **9096 格**真实 `detect`（676f） |
| 盲区地图矩阵 | 1147 样本 × 8 资产 = **9176 格**（676g） |

### 2.2 `provenance`（来源三分类；677a 新增，取代布尔 `planted` 的读法）

> **`planted=false` ≠ "真实世界样本"。** 677a 把来源细化为**三值枚举**（规范见
> `SCHEMA.md` §2.1）；`planted` 保留为兼容字段，二者是**确定性映射**。

| `provenance` | `planted` | n | 占比 | 定义与构造过程 |
|---|:---:|---:|---:|---|
| `self-authored` | `true` | **968** | 92.9% | 本项目为演示某类缺陷而**自撰**的可编译片段 |
| `source-derived-reconstruction` | `false` | **74** | 7.1% | 全部来自 **expG**。构造路径：**真实 CVE / GitHub issue → 定位缺陷 → 缩减为最小可编译单文件片段 → 重新标注**；剥离内容逐条记录在 `source.simplification` |
| `original-external-artifact` | —— | **0** | 0% | **当前语料中不存在**。**No original external artifacts are included in the current corpus.** |

> ⚠️ **这是本数据集最大的外部效度限制**：92.9% 的样本是自造的，且剩下 7.1% 也是**重构**而非
> 原始产物 ⇒ 它测的是**仪器**，**不是真实缺陷分布**（见 §9）。
> 复现：`.venv/Scripts/python.exe -c "import json;d=json.load(open('data/676m_sample_manifest_corrected.json',encoding='utf-8'));print(len(d))"`（按 `planted` 聚合即得三分类计数）。

### 2.3 缺陷类型（`defect_type`）

676m 起使用 **34 项规范词表**（当前在用 **33** 项；`memory_safety` 为保留的通用类，
其 24 条样本已全部按证据细分到具体类型）。词表与 15 类粗粒度 `defect_group`
的对应关系见 `SCHEMA.md` §3。

| `defect_group`（15 类） | n | | `defect_group` | n |
|-------------------------|--:|-|-----------------|--:|
| `memory_lifetime` | 156 | | `out_of_bounds` | 89 |
| `stl_iterator` | 140 | | `embedded_platform` | 68 |
| `type_alias_alignment` | 113 | | `virtual_or_oop` | 60 |
| `integer_ub` | 108 | | `logic_or_api` | 38 |
| `concurrency_order` | 105 | | `null_deref` | 24 |
| `liveness` | 95 | | `uninitialized_read` | 20 |
| | | | `data_race` | 18 |
| | | | `generic_ub` | 8 |

（676m 迁移前是 **56 个取值**、无统一词表；迁移映射表见
`data/676m_H2标签迁移报告.md` §2。）

### 2.4 `expected_verdict`（独立检测器判据）

| 值 | n | 含义 |
|----|---:|------|
| `catch` | **566** | 至少一个资产产生非空诊断报告 |
| `miss` | **476** | 无任何资产产生报告——**包含 sanitizer 挂起超时后无报告** |

> 676m 把 34 条 `hung_flag=true` 的样本由 `catch` 修正为 `miss`（挂起不产生报告）。

### 2.5 `severity`

`high` 721 / `medium` 229 / `low` 92（自评，非外部标准）。

### 2.6 来源重写（`provenance = source-derived-reconstruction` 的 74 条）

> **表述纪律（677a）**：这 74 条是**基于真实漏洞的重构**（single-file teaching reconstruction），
> **不是** original external artifacts，**也不是** naturalistic production code。论文与任何下游文档
> 一律写 "74 source-derived reconstructions based on real CVEs and GitHub issues"，
> **不得**写 "74 real defects" / "74 real-world samples"。

| 来源类型 | n | 示例项目（前 6） |
|----------|---|------------------|
| `cve` | **67** | openssl 24、curl 23、sqlite 6、php 3、tinyxml2 3、jsoncpp 3 |
| `github_issue` | **7** | libpng / libxml2 / openssh / libwebp / nginx / sudo / fmtlib 等 |
| **合计（全部有 `source.url`）** | **74/74** | 676k 逐条联网核查，**全部 HTTP 200** |

（另：expG 还有 **25 条 `planted=true`** 样本，它们的 `source` 记录的是
**缺陷类别的公开出处**，代码本身是本仓自撰的复现，故不计入"真实来源"。）

每条含 `source.{type,id,url,project,commit,simplification}`，
其中 `simplification` 记录**从真实漏洞到可编译单文件片段**做了哪些剥离。

### 2.7 已知的"不该有"的东西

- **不含**个人信息、用户数据、网络流量、凭据。
- **不含**可直接利用的完整漏洞（CVE 样本是**等价重写的教学片段**，
  不是原始可利用代码）。
- **不含**多文件工程（expC 的 30 条多 TU 样本最多 5 个文件）。

---

## 3. 采集过程（Collection Process）

### 3.1 生成流程（676c 各批次）

每个批次（expA–expG）走同一条流水线：
**选题 → 自撰/改写单文件片段 → 语法与编译验证 → 目标检测器实测 →
入池（`.cpp` + `.json` + `INDEX.json`）**。

| 批次 | 主题 | n | 特点 |
|------|------|---|------|
| expA | 内存安全基础 | 100 | 每条带 `<<PLANTED-DEFECT>>` 行内标记 |
| expB | 数据竞争 / 并发 | 94 | `.cpp` 头部有 8 行标注块；行号原为相对值（676m 已校正） |
| expC | 语言语义 / STL / 链接 | 200 | 含 30 条多 TU 样本；含 `conditional_trigger` / `optimization_dependent` 元标签 |
| expD | 迭代器 / STL 容器 | 200 | 每样本 3 资产实测记录 |
| expE | 并发高级（内存序 / 死锁 / CV） | 200 | 含 34 条挂起样本；带 `thread_count` / `timeout_seconds` |
| expF | 平台相关（对齐 / 端序 / volatile） | 149 | 带 `platform_dependent` 标记 |
| expG | 真实世界（CVE / issue 重写） | 99 | 74 条 `planted=false`；**0% 模板克隆** |

### 3.2 标注流程

- **单标注者**：本项目作者 + AI 标注代理共同完成（`generator` 字段记录生成器）。
- **标注字段**：`defect_type` / `defect_location{file,line,function,notes}` /
  `severity` / `planted` / `expected_verdict` / `trigger_condition` / `notes`。
- **行号口径**：**缺陷发生的操作行**（失效操作 / 越界访问 / 释放行），**绝对文件行号**。
  多文件样本可为 `null`（跨文件不可比）。
- **验证记录**：每条样本的 `verification` 子对象记录生成期的语法 / 编译 / 检测器复现结果。

### 3.3 双标注复核（676k）

| 项 | 值 |
|----|----|
| 抽样 | 分层（`source_batch` × `defect_type`，75 层），种子 6761，抽 144 条 |
| 可重标 | 131 条（13 条 corpus 无源码，不可重标） |
| **盲化协议** | 只读源码，**注释全部抹为等长空白**（保留行号）——因为 expB/expG 的 `.cpp` 头部直接写着标注字段 |
| **重标注者** | **AI Agent（非人类）** |
| Cohen's κ（`defect_type`，15 类） | **0.77** |
| Cohen's κ（`expected_verdict`） | **0.69** |
| Cohen's κ（`planted`） | **0.71** |
| 行号精确一致率 | 47.9%（±3 行容差 81.5%） |

> ⚠️ **κ 反映的是 AI 自洽性，不是人类标注者间一致性（IAA）**。
> 人类第三方复核**仍未做**（论文中登记为威胁 T17）。

---

## 4. 预处理 / 清洗（Preprocessing）

### 4.1 676m 已执行

| 步骤 | 规模 | 说明 |
|------|------|------|
| H1 挂起样本判据修正 | 34 条 | `expected_verdict: catch → miss`（挂起不产生报告） |
| H2 词表统一 | 308 条改写，56 → 34 项 | 元标签 `conditional_trigger`/`optimization_dependent` 拆到 `trigger_condition`（80 条） |
| M1 补 `defect_location.file` | 1042 条 | 多 TU 样本按缺陷标记行定位到具体文件 |
| M2 `id` → `sample_id` | 300 条 | expA 100 + expC 200；`INDEX.json` 增补 `sample_id` 别名 |
| M3 corpus `planted` 补全 | 64 条 | `null → false`（见 §9 的层级分歧说明） |
| M4 expB 行号口径校正 | 94 条 | 相对行号 → **绝对行号**，逐条与源文件缺陷标记核对，**94/94 验证通过** |
| M5 描述键统一 | 948 条 | `defect_location.note`/`description` → `notes` |

### 4.2 去重（676k，三层）

| 层 | 判据 | 重复组 | 涉及样本 | **跨批** |
|----|------|-------:|---------:|---------:|
| L1 精确 | 源文件字节 md5（文本模式，CRLF/LF 不敏感） | 91 | 321 | **0** |
| L2 归一化 | 去注释/去空白/标识符→`ID`/数字→`NUM` 后 sha256 | 163 | 674 | 7 |
| L3 语义 | `defect_type` 组内 token TF-IDF 余弦 ≥0.9 | — | 1029 对 | **0** |
| L3b 结构 | 同 L3 但常量归一，**只统计跨批** | — | — | **103 对** |

### 4.3 编译抽检（676k）

分层抽样 230 条 → 可编译子集 **217 条**，**217/217 = 100% 通过**
（含无源码的 13 条 corpus 时 94.3%）。48 个被抽中的 `defect_type` 全部 100% 通过。

### 4.4 未做（诚实登记）

- **未删除任何样本**（红线）：62.2% 的批内模板克隆率只披露，不清理。
- **未做人类第三方标注复核**。
- **未做语义层（semantic scope）回填**（0/26）。

---

## 5. 用途（Uses）

### 5.1 适合

- **检测器能力边界映射**：多资产 × 多样本的逐格真实判定（676g / 676l）。
- **预算分配 / 资产选择策略**的对照实验（A5 的 FD vs Random vs Static）。
- **跨批次标签体系**研究（统一词表前后的 κ 变化）。
- **检测器互补性与边际贡献**分析（留一法、穷举组合）。
- **编译器 / sanitizer 行为差异**研究（cross-compile 资产）。

### 5.2 **不**适合

- **估计真实世界缺陷分布**：92.9% 是人工植入，`planted=false` 只有 74 条。
- **训练缺陷检测模型**：62.2% 模板克隆率 ⇒ 训练集与测试集极易同源泄漏。
- **断言"某检测器优于另一检测器"**：单回合判定带 ~5% 跑间噪声（§9）。
- **跨语言泛化**：全部是 C++（且依赖 g++ 13.x 的具体行为）。
- **安全评估**：CVE 样本是教学等价重写，不可直接利用。

---

## 6. 分布（Distribution）

### 6.1 文件布局

```
data/holdout_expansion/<batch>/
  INDEX.json              # 批次索引（含每样本的 defect_type / expected_verdict / defect_line）
  sample_<id>.json        # 逐样本标注（权威记录）
  sample_<id>*.cpp|.h     # 样本源码
```

### 6.2 A5 的派生 / 评估切分（676f）

| 切分 | n | 规则 |
|------|--:|------|
| derivation | 571 | 每个 (`source_batch`, `defect_group`) 层内按 `sha256('20260930':sample_id)` 升序，**偶数位** |
| evaluation | 566 | 同上层内**奇数位** |

切分是**确定性**的（不依赖文件系统顺序），且**派生集不含评估集信息**——
FD（failure-driven）的 fail_hits 只许用派生集，避免 oracle。

### 6.3 其它切片

| 切片 | 定义 | n |
|------|------|---:|
| `planted=true` | 自造 | 968（扩样）/ 1063（A5 含 legacy） |
| `planted=false` | 真实来源 | 74 |
| expG 真实子集 | `planted=false` 且 `source_batch=expG` | 74 |
| 盲区地图并集 | 1147（含 holdout 41 + corpus 64） | 1147 |

---

## 7. 隐私与合规（Privacy）

- **不含个人信息**：所有样本是自撰代码或公开 CVE/issue 的**等价重写**。
- **真实来源是公开漏洞**：CVE 与 GitHub issue 均为公开信息，
  `source.url` 逐条登记（74/74 可追溯，全部 HTTP 200）。
- **许可证**：仓库 Apache-2.0；CVE 重写片段不逐字复制任何网页代码
  （`external_corpus_672h.json` 的 `source_policy` 明确写 `verified_source=false`）。
- **无敏感数据**：无网络流量、无凭据、无用户数据。

---

## 8. 维护（Maintenance）

| 项 | 值 |
|----|----|
| 维护者 | 本仓作者（DCO 签署：`git log --signoff`） |
| 联系方式 | 仓库 issue 跟踪（arXiv 版匿名期间见论文的匿名说明） |
| 更新频率 | 按批次（`data/prompts/676*.md`），每批一个 DCO 提交 |
| 版本控制 | 标注与源码**均在 git 内**；`data/holdout_expansion/**/*.cpp` 为**只读**（676m 零修改） |
| 复现入口 | `docker/paper/run_all.sh`、`tools/fix_676m_schema.py`、`tools/recompute_a5_676m.py`、`tools/recompute_a5_676f.py` |
| 变更纪律 | 每批只 `git add` 自己的文件；不 push（等确认） |

---

## 9. 已知局限（Known Limitations）——**必须与任何引用同读**

1. **`self-authored` 占 92.9%**：数据集测的是**仪器**，不是真实缺陷分布。
   用 `source-derived-reconstruction`（n=74）做外部效度时，区间很宽（盲区比 21.6%，CI [13.8, 32.3]）。
   **677a 补充**：这 74 条是**重构**而非原始外部产物，因此**外部效度主张不能建立在其上**；
   当前 `original-external-artifact` 计数为 **0**。
2. **批内模板克隆率 62.2%**：674/1083 条样本落在结构完全相同的组里，
   全库只有 **572** 种不同代码结构。⇒ **有效独立样本量远小于 1042**，
   所有率的区间应据此读宽；且**不可用于训练**。
3. **103 对跨批结构近克隆**：676m 修正前这 103 对的 `defect_type` **0 对相同**。
   ⇒ 跨批标签不一致曾系统性拉低 κ；676m 已统一词表，但**近克隆本身未删除**。
4. **单标注者 + AI 复核**：κ=0.77/0.69/0.71 是 **AI 自洽性**，不是人类 IAA。
   人类第三方复核仍未做（论文威胁 T17）。
5. **~5% 跑间不稳定**：无竞争条件下的干净重测 **18/369 格（4.9%）翻转**；
   TSan 三轮抽检 **4/80 样本（5.0%）出现过翻转**。⇒ 单回合逐格判定带噪声，
   **排序稳健、逐格结论不稳健**。
6. **检测器盲区 38.4%（instrument-boundary 统计）**：1147 样本上 catch 707 / miss 440 ⇒ 38.4%
   的样本在**本库 + 这 8 个资产**下完全不可见；**18/70** 个类型盲区 >50%。
   **口径纪律（677a）**：这是**仪器边界**统计，**不**意味着"真实世界 C++ 缺陷有 38.4% 不可检测"；
   换语料或换资产池该值即变。权威产物 `data/blindspot_676g_stats.json`。
7. **平台依赖**：sanitizer 走 **WSL Ubuntu 24.04.4 + g++ 13.3.0**（含 `setarch`）；
   本地资产走 **MinGW g++ 13.1.0 / clang 22.1.8**。换环境（如 macOS 无 `setarch`、
   Windows 原生无 UBSan 运行库）**不可复现**。
8. **`planted` 的层级分歧（未解决项）**：676f 的 A5 矩阵把 `corpus` 记为
   `planted=true`；676g 清单记为 `null`；676m 的 M3 修正件记为 `false`
   （依据：corpus 是"原始数据集，非人工植入"）。本批**只修 676g 层**，
   **未改 A5 层**（论文的 planted 子组分析仍按 `true` 计算）。
   这一分歧已登记在 `data/676m_数据修复总报告.md` 的"未解决项"。
9. **行号语义**：676m 明确为"缺陷发生的操作行"，但 iterator 类样本
   原标注指向**使用行**（`*it`），重标注指向**失效操作行**（`erase`/`push_back`）。
   行号精确一致率仅 47.9%（±3 行 81.5%）。
10. **多文件样本行号不可比**：expC 的 30 条多 TU 样本，`line` 只对 `defect_location.file`
    指向的那个文件有意义。

---

## 10. 引用（Citation）

引用本数据集时请同时引用论文与数据卡，并**带上限定语**：

> … on a 1042-sample C++ UB pool of which **92.9% are self-authored** and whose
> **within-batch template-clone rate is 62.2%** (572 distinct structures);
> labels carry **AI self-consistency κ=0.77**, not human IAA; per-cell verdicts
> carry a **~5% run-to-run instability** floor and **38.4%** of samples are
> invisible to the 8-asset pool.
