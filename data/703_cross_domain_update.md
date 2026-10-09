# 703-D · 699 / 700-D 跨领域发现写进论文 —— 具体改动

- **批次**：703 ｜ **任务**：D ｜ **日期**：2026-10-09
- **被改文件**：`research/latex/queyi_neurips2027_v1.1.tex`
- **落点**：① 附录 Related Work（`\label{app:related}`）新增
  `\paragraph{(10) Cross-domain transfer to LLM-as-a-judge evaluation (added in 703).}`；
  ② 正文 §6 Synthesis 新增 `\paragraph{Do the rules travel?}`
- **diff hunk**：`@@ -1277,0 +1293,20 @@`（附录 20 行）＋ `@@ -557,0 +565,8 @@`（正文 8 行）
- **数据源**：`data/699_transferability_test.md`（699-C）、`data/700_cross_domain_empirical.md`（700-D）
- **红线**：`detect_calls = 0`；未改检测器/样本/冻结矩阵；未改 `queyi_refs.bib`。

---

## 1. 加了什么

### 1.1 附录 Related Work（20 行）

```
\paragraph{(10) Cross-domain transfer to LLM-as-a-judge evaluation (added in 703).}
  · 结构性 Goodhart 非 C++ 专属：240 条实时下载样本上，"更长=更好"懒惰裁判与人类
    偏好侧在 JudgeBench 仅一致 44.17%（55.83% 上"长度"是自信但错误的代理）；
    RewardBench 100% 一致，因其策展让长度成为混淆变量
  · 降级版跨领域复现：迁移分 55.84/100（口径 15.62 / 环境 16.25 / 标签 21.39 / 聚合 2.58）
  · 四轴中三轴同构；聚合轴**不同构**：换聚合规则仅移动 LLM 报告 1.03pp vs C++ 的 33.33pp
  · 静默签名**反转**：C++ 丢失写成 miss（静默），LLM judge 写成 unknown（响亮）
  · 诚实边界：降级版非预注册；240 条实时下载但 invariance **未实测**；
    迁移分权重与 50/100 阈值自定无外部标定；人类侧是策展偏好标签 ⇒ 无 IAA 时
    "judge 错"与"标签错"不可分
```

### 1.2 正文 §6 Synthesis（8 行）

```
\paragraph{Do the rules travel?}
A degradation-grade replication in LLM-as-a-judge evaluation scores 55.84/100 on a
four-component transfer scale: caliber, environment and label drift transfer, while the
\emph{aggregation} axis does not (a rule change moves the LLM report by 1.03pp against
33.33pp here), and the silence signature \emph{inverts} (a lost measurement becomes
\texttt{unknown} rather than \texttt{miss}). The protocol travels; its diagnostic signatures do
not travel unchanged (Appendix~\ref{app:related}).
```

**位置理由**：任务书说"在论文的 Related Work 或 Discussion 加一段"。论文**没有** Discussion 节，
Related Work 的**完整版在附录** `app:related`（正文只保留压缩段）⇒ 主体落附录。
但 §6 Synthesis 的第 5 条规则明确说 R1–R5 "transfer beyond C++ verification, e.g. to LLM
evaluation"，**该处正是"可迁移性"论断的正文位置** ⇒ 在正文补 8 行给出**证据**（而非新增节）。

---

## 2. 逐条对照：写进论文的数字 vs 699 / 700-D

| 论文表述 | 上游原文 | 一致性 |
|---|---|---|
| "240 samples downloaded live" | `699_transferability_test.md` §0："在真实下载的 **240 条**数据上计算"；`699_批次完成报告.md`："**240 条实时真实下载样本**（HuggingFace datasets-server，非编造）" | ✅ |
| "agrees with the human-preferred side only **44.17%** of the time on JudgeBench" | §1 表：JudgeBench n=120，**长度裁判一致率 0.4417** | ✅ |
| "on **55.83%** of samples length is a confident but wrong proxy" | §1 表：JudgeBench **结构性 Goodhart 率 0.5583** | ✅ |
| "RewardBench agrees **100%** because its curation makes length a confounder rather than a signal" | §1 表：RewardBench 一致率 **1.0000**，结构性 Goodhart 率 0.0000；§1 解读："chosen 被策展为'更好且更长'…… **长度偏置混淆**" | ✅ |
| "scores **55.84/100** on a four-component transfer scale (caliber **15.62**, environment **16.25**, label **21.39**, aggregation **2.58**)" | `700_cross_domain_empirical.md` §4：C1 口径 **15.62** / C2 环境 **16.25** / C3 聚合 **2.58** / C4 标签 **21.39** / 总分 **55.84** | ✅（和 = 55.84 ✓） |
| "changing the aggregation rule moves the LLM report by only **1.03pp** against **33.33pp** in C++" | §4.1："LLM 领域的聚合规则变化只造成 **1.03 pp** 的效应，而 C++ 领域同轴可达 **33.33 pp**（698-A §4）" | ✅ |
| "in C++ a lost measurement is written as \texttt{miss} (silent), whereas the LLM judge writes \texttt{unknown} (loud)" | §5 总表："**静默/响亮**：C++ **静默**（丢失写成 miss） / LLM **响亮**（丢失写成 unknown）" | ✅ |
| "because an LLM aggregation rule acts on a single judge's verdicts and offers no ``zero-capability component'' to pad with" | §4.1："LLM 的聚合规则（多数票 vs 资产一致 OR）作用在**同一个 judge 的裁决**上，**没有'掺入零能力组件'的操作空间**" | ✅ |
| "this is a degradation-grade replication, not a pre-registered cross-domain study" | §0.1："**699 未完成 ⇒ 按任务书降级条款**使用仓库内数据"；§6 边界 7："本批未下载 JudgeBench / RewardBench …… **未执行**，已如实登记" | ✅ |
| "their prompt/model invariance was \emph{not} measured (no judge endpoint was available)" | `699_transferability_test.md` §0："**口径漂移（prompt invariance）与环境漂移（model invariance）需要真实 LLM 裁判**…… 本环境未配置可用 key，故这两项返回 `None`" | ✅ |
| "the transfer-scale weights and its $50/100$ threshold are ours with no external calibration" | §6 边界 5："**迁移性分数的阈值（50）与分量权重（各 25）、满分标定（20%/10pp）都是本批自定的**，无外部标定" | ✅ |
| "``judge wrong'' and ``label wrong'' remain inseparable without human IAA" | §6 边界 3："**真值参照是声明标签**，人类 IAA = 0 ⇒ 「judge 错」与「标签错」**不可分**" | ✅ |

---

## 3. 与 700-D 的"四条诚实边界"的对齐

任务书要求"诚实声明：699 的 240 条样本是实时下载的，invariance 未实测"。本批把
700-D §6 的 7 条边界里与论文相关的 **4 条**写进了论文：

| 700-D 边界 | 是否进论文 |
|---|---|
| 1. 699 未完成 ⇒ 用 692 的 LLM 臂，样本量/模型数偏小 | 部分（表述为 "degradation-grade replication"） |
| 2. 环境轴配对表不可靠（轮次推断极差 39.19pp）⇒ 改用已发布聚合量 | ❌ 未进（细节过深，属附录技术债） |
| 3. 真值参照是声明标签，IAA=0 ⇒ judge 错/标签错不可分 | ✅ 进论文 |
| 4. 只有 2 个 prompt、2 个模型 ⇒ 控制点各只有 2 个 | ❌ 未进 |
| 5. 迁移分阈值/权重/满分标定自定，无外部标定 | ✅ 进论文 |
| 6. 跨领域结论只覆盖 LLM-as-a-Judge 一种形态 | 部分（标题即限定 "LLM-as-a-judge evaluation"） |
| 7. 未下载 JudgeBench / RewardBench | ✅ 进论文（"240 samples downloaded live" + "invariance was not measured"） |

---

## 4. 引用处理

本段**未新增** `queyi_refs.bib` 条目（红线：本批不动 bib）。可选用的既有键
（`zheng2023judging` LLM-as-a-judge、`norman2026reliabilityvalidity` 可靠性≠效度、
`han2025judgesverdict`、`lv2026whoevaluates`）本批**未使用**——因为 699/700-D 的
LLM 数据来自**本仓库自己的 692 臂 + HuggingFace 实时下载**，不是这些论文的数据源；
**避免"用别人的引用给自家数据背书"**。这一点在正文/附录里以纯文本表述，不用 `\cite`。

---

## 5. 复算与核验命令

```bash
sed -n '1,40p' data/699_transferability_test.md                 # JudgeBench 0.4417 / RewardBench 1.0000
sed -n '155,175p' data/700_cross_domain_empirical.md            # 迁移分四分项 = 55.84
grep -n "44.17\|55.84\|1.03\|33.33\|240" research/latex/queyi_neurips2027_v1.1.tex
cd research/latex && tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex
```

---

## 6. 诚实边界

1. **240 条样本是实时下载的**，但它们的 **prompt/model invariance 未实测**（无 judge 端点）——
   论文已显式声明；不要把本段读成"跨领域实验已完成"。
2. **JudgeBench / RewardBench 的许可证与 NVD/CVSS 复核仍在 699 的待办清单里**（699 §后续待办 3）；
   本批**未**复核许可证 ⇒ 论文里只引用**统计量**，不声称数据可分发性。
3. 迁移分 55.84 的**四个分量权重与阈值均为自定**，论文已声明"no external calibration"。
4. 本批**未**把 700-D 的"环境轴轮次推断极差 39.19pp"这一测量陷阱写进论文
   （它更像是本仓库的数据治理债务，不是论文结论）。
5. 人类侧是**策展偏好标签**（非独立人类标注）⇒ 44.17% 一致率**不能**直接解读为
   "judge 准确率 44%"；论文用 "agrees with the human-preferred side" 这一措辞规避该误读。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 D ｜ `detect_calls` = 0 ｜ 未 push*
