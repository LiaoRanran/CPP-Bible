# 714-D · AI-vs-AI IAA 试点 —— **未执行登记**

> ⚠ **本文件不是结果，是"未执行"的登记。**
> 714 任务 4 要求"用两个不同模型独立标注 30 条、计算 Cohen's kappa"。本批**没有生成任何新的 IAA 统计量**。
> 本文件记录：为什么没做、做了什么尝试、以及仓库里已有的替代证据是什么。

---

## 1. 为什么没做

| 检查项 | 结果 |
|---|---|
| 环境里是否存在 LLM API key？ | 存在 `DEEPSEEK_API_KEY`（长度 23） |
| 该 key 是否可用？ | ❌ **不可用**。实测 `GET https://api.deepseek.com/models` 返回 **HTTP 401 Authorization Required** |
| 是否存在第二个模型的 API？ | ❌ 未发现。环境变量中只有 DeepSeek 一个 LLM 端点，无 OpenAI / Anthropic / 智谱 / Moonshot 等 |

**两个阻断条件同时成立**：
1. **无可用 API** —— 唯一的 key 返回 401（未授权 / 已失效 / 占位值，无法区分）。
2. **即使 API 可用，也凑不出"两个不同模型"** —— 任务要求两个**不同**模型独立标注；本环境只有一个端点。用同一个模型跑两遍得到的是**自洽性**（self-consistency），不是 IAA，且这正是 693 批次已经做过的事（见 §2）。

**登记结论**：`未执行，原因：无可用 LLM API（唯一端点 DeepSeek 返回 401；且只有一个端点，无法构成"两个不同模型"的双标注设计）`。

---

## 2. 仓库里已有的替代证据（**不可**当作人类 IAA）

`data/693_ai_double_label.json`（schema `queyi-693-ai-double-label/v1`，2026-10-08 生成，`tools/annotate_693_b.py`）：

| 字段 | 值 |
|---|---|
| `n_samples` | **145** |
| `raw_agreement_pct` | **78.62** |
| `cohen_kappa` | **0.4949** |
| 排除泄漏样本后（`n=132`） | raw agreement 77.27，**κ = 0.4578** |
| `n_disagreements` | 31 |
| `leak_exposed` | 13 条（S021, S022, S033, S034, S035, S039, S051, S055, S058, S074, S111, S120, S133） |

**该产物自带的诚实声明**（`honest_status` 字段，原文）：

> `human_iaa: 0`，`annotator_a_is_human: false`，`annotator_a_semantics: "声明可检出性（八资产实测 OR），非人类审读真值"`
> `note: "Annotator B 为 AI 模拟第二标注者；人类 IAA 在本批之后仍为 0。本产物只用于跑通流程 + 产出分歧清单，不能充当人类一致性证据。"`
> 已知偏差 `known_biases`：① B 执行前已知材料包总体分布（catch 96 / miss 49）——**锚定风险**；② 13 条样本源码残留 `expected_verdict` 注释 ⇒ **B 标签被污染**；③ B 的 compiler-warn 判据按 `-Wall -Wextra` **推定，未实测**。

**⚠ 三个必须记住的限制**：
1. **Annotator A 不是人**，是"八资产实测 OR 裁决"——即**仪器读数**，不是审读真值。
2. **Annotator B 是 AI 模拟的第二标注者**，不是独立人类，也不是独立模型族。
3. **人类 IAA 仍为 0**（`data/693_human_iaa.json`：`n_filled = 0`，`status = "pending"`，31 行裁决表**一行未填**）。

⇒ **κ = 0.4949 只能读作"一个 AI 标注者与一个仪器读数之间的折间一致率"，在任何材料中都不得写成 IAA、不得写成人类一致性、也不得写成跨模型一致性。**

---

## 3. 如果要做，最小可行设计（留给后续批次）

不执行，只登记设计，供有 API 时使用：

1. **样本**：从 `data/693_human_adjudication_package.csv` 抽 30 条，**只导出 `sample_id` + `source_code` 两列**（屏蔽 `annotator_A` / `annotator_B` / `b_reason`，保证两个标注者都盲）。
2. **标注者**：模型甲（API A）、模型乙（API B），**必须不同模型族**；同一 prompt（沿用 693 的 `annotator_b_prompt` 以保证口径可比）。
3. **四态**：catch / miss / unknown / contradiction。
4. **统计**：Cohen's κ（四态多分类，无权重）+ 原始一致率 + 逐类混淆矩阵；并**另算** κ(甲, A) 与 κ(乙, A) 作为参考（A 是仪器读数，不是真值）。
5. **必须声明的三件事**：
   - "这是 **AI-vs-AI**，不是人类 IAA"；
   - 两个模型的身份（若匿名投稿，可用"两个商用 LLM，不同厂商"）；
   - 已知污染风险（693 已识别的 13 条 `expected_verdict` 残留应**排除或单独报告**）。

---

## 4. 对论文的影响

- 论文1 §T1（行 613–628）已声明："All rates rest on single-annotator labels; there is **no human inter-annotator agreement**. Every $\kappa$ in this paper is **AI self-consistency, not human IAA**, and must not be cited as validation."
- **该声明仍然成立，本批不改变它。**
- 本批**未产生**任何可以替代人类 IAA 的新证据。**人类标注仍是论文1 §Future work 里"the single most important pending item"。**
