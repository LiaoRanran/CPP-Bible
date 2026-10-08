# 692-C · LLM-as-evidence-asset 审计迁移协议（**先于任何一次 LLM 调用落盘**）

- 批次：692｜执行：CodeBuddy（AI）｜写盘时间：2026-10-08（协议先落盘）
- 上游建议（690）：**不要追 LLM judge 的热点**，而是证明 **audit protocol 是 modality-independent 的**——
  把 LLM 当作一个 **failure topology 与 sanitizer 完全不同的 evidence generator**。
- 定位（写死）：LLM **不是 oracle**，是**第 4 类 evidence asset**，服从同一条链条：
  `provenance → caliber → blind eval → human reference → audit`。

---

## 1. 样本（与 692-B 同框架，理由见 §6 偏差登记）

| 项 | 取值 |
|---|---|
| 池 | `data/a5_676f_detection_matrix.json`，`split == "evaluation"` 且有源文件者 **538** |
| N | **80**（任务书 80–120 下界；成本/时间约束下取最保守值） |
| 抽样 | 分层固定：`expected_verdict == "catch"` 抽 **40**、`== "miss"` 抽 **40**；`random.Random(6921).sample`（Mersenne Twister 跨机稳定），排序键 = `sample_id` 升序 ⇒ 任何人可复现同一 80 条 |
| 输入 | 单文件源码（剥注释，见 §3），**不给文件名、不给 detector、不给 planted 标签、不给 sanitizer 输出** |
| 截断 | 代码 > 400 行 ⇒ 取前 400 行并加标记 `/*[truncated]*/`（逐条记录是否被截断） |

## 2. 模型（两个家族，failure topology 不同）

| 槽 | model ID（精确字符串） | 家族特征 |
|---|---|---|
| **Model A** | `glm-4.5` | 推理型（返回 `reasoning_tokens`），长思考后作答 |
| **Model B** | `glm-4-flash` | 非推理轻量型，直接作答 |

- 端点：`ZHIPU_BASE_URL` + `/chat/completions`（OpenAI 兼容），凭据自 `.env` 读取，**不落盘、不打印**。
- `temperature = 0`；`max_tokens = 700`；每条调用记录 `prompt_tokens/completion_tokens/latency`。
- 可用性事实（本批实测）：`glm-4 / glm-4-flash / glm-4.5 / glm-4-plus / glm-4-air / glm-4-flashx` 均 PONG 通过；
  `DEEPSEEK_API_KEY` 存在但 API 返回 **401（密钥无效）** ⇒ 不构成第二家族，如实登记。

## 3. Prompt 设计（两个语义等价变体，p1/p2）

共同部分：
- 角色：C++ 代码审查者；
- 任务：判断这段代码是否含**会造成未定义行为 / 内存错误 / 并发错误 / 明显 API 误用**的缺陷；
- 只输出 JSON：`{"has_defect": bool, "category": str, "confidence": 0-1, "reason": str}`（p1）/ 字段同义重排（p2）；
- **禁止猜测文件名/来源/工具**。

答案泄漏控制：
1. **剥离全部注释**（夹具头注释直接写「故意双重释放（ASan 取证）」⇒ 不剥就是喂答案）；
2. 不提供文件名、detector 名、planted 标签、sanitizer 输出、预期判决；
3. 样本顺序 = `sample_id` 升序；不设随机性（temperature=0）。

p1 与 p2 的差别**只在措辞与字段顺序**（p1 先给角色再给任务；p2 先给任务再给角色，并要求 `confidence` 先于 `has_defect` 输出）。**不改变任何判据**。

## 4. 四态判定（与 Queyi 四态对齐）

| 态 | 判据（**写死在脚本里，不看结果再改**） |
|---|---|
| `catch` | JSON 解析成功且 `has_defect == true` |
| `miss` | JSON 解析成功且 `has_defect == false` 且**理由文本与判决不冲突** |
| `unknown` | API 失败 / 截断导致 JSON 不可解析 / 模型拒答（`has_defect` 缺失或非布尔） |
| `contradiction` | 结构化字段自相矛盾：`has_defect == false` 但 `reason` 含固定缺陷词表（double free / use after free / out of bounds / data race / leak / uninitialized / dangling / overflow / null deref）中的词；或 `has_defect == true` 但 `category` 为空/`none` |

> `contradiction` 的判据是**操作性启发式**（固定词表），标**探索性**；这是把 Queyi 四态平移到语言模态的最小可用版本，不是它的等价物。

## 5. 四个指标（预注册）

1. **Accuracy / 三组件**：`catch` = 四态为 catch ∧ `expected_verdict == "catch"`；`miss` = 四态为 miss ∧ 期望 catch；
   `unknown` = unknown/contradiction（**从分母剔除并逐条列出**）；同时报 `false_report_rate = catch / expected == "miss"`。
2. **Prompt invariance**：`P(V(p1) = V(p2))`（逐模型；同时报 Cohen's κ 与不一致条数）。
3. **Confidence calibration**：5 桶（[0,0.6),[0.6,0.7),[0.7,0.8),[0.8,0.9),[0.9,1.0]）经验正确率 + **ECE**（分母只含可判定样本；unknown 逐条列出）。
4. **Cross-asset disagreement**：`V_LLM`（p1/p2 多数票，平票则取 p1 并记录） vs `V_sanitizer`（冻结矩阵 asan/ubsan/tsan 的 OR）。
   报 2×2 一致性、**谁对谁错**（以 `expected_verdict` 为参照）、以及两类的 `defect_group` 分布。

**audit transfer 判据（预注册）**：若 (i) prompt invariance ≥ 0.9、(ii) 四态可完整落盘、(iii) `V_LLM ≠ V_sanitizer` 的样本**成规模存在且方向可解释**，
则称「audit 链条在语言模态上**可迁移**」；三项任一不成立则如实写不成立。**不比较谁更准，不声称 LLM 是 oracle。**

## 6. 诚实边界（含偏差登记）

1. **任务书原定「41 holdout + 64 external corpus 随机抽 80」不可执行**：673e 记录里的 76 条 corpus 源路径
   **已不在盘上**（实测：`data/673e_*_raw.json` 的 corpus `src` 批量指向已删除的临时路径），且 reveal 明细
   **不内联源码**。⇒ 改用与 692-B 完全相同的 A5 evaluation 帧（538 有源），**偏差已登记**，并因此获得
   「与 sanitizer 逐样本对照」的额外好处。holdout 60 条（41 error + 11 control + 7 unknown）源在盘上，
   作为**附加子集**单独报（不进主表，避免两个框架混算）。
2. 人类 IAA 仍为 **0**：本批的「正确」只对 `expected_verdict`（声明可检出性）口径，**不引入任何人工标注**。
3. API 若中途不可用：已知部分照写，剩余逐条记为 `unknown` 并在报告中列出；**不编造**。
4. 不把 LLM 当 ground truth；不做大规模 benchmark（N ≤ 120 已满足）。
5. `contradiction` 与 `confidence` 都依赖模型自述，属**自报告**指标，只可用于校准与一致性分析，不可当证据强度。

---

复算：`python tools/run_692_llm_audit.py`（`run` 跑 API，`--analyze` 只从 raw jsonl 汇总）。

---

## 7. 修订 A1（**执行中发现，2026-10-08，落盘于 A 槽第二轮之前**）

**事实**：按 §2 的 `max_tokens = 700` 跑完 Model A（`glm-4.5`）第一轮后，观察到
`finish_reason == "length"` 占相当比例（推理 token 吃掉了补全预算），导致 JSON 被截断 ⇒
按 §4 判据记 `unknown`。这不是"模型拒答"，而是**补全预算与推理型模型的交互**。

**修订（只改预算，不改任何判据/样本/指标）**：

1. **Model A 增跑一轮**，`max_tokens = 2000`（记录 `run_tag = a2000`）；
2. 第一轮记录（`run_tag = default`）**保留不删**；
3. 结果必须**并排报告两轮**（`A@700` vs `A@2000`），并把两者的 `unknown` 差异作为
   **「补全预算敏感性」**的单独一节 —— 它本身就是一个 caliber 敏感性发现；
4. Model B（非推理型）不再重复跑（其 `finish_reason` 未出现 `length` 主导）；
5. **主表口径**：Model A 用 `a2000` 轮，Model B 用 `default` 轮；`A@700` 作为敏感性行同表出现；
6. 本修订**先落盘再执行**；若两轮结论方向相反，按实测并排报告，**不得只留好看的一轮**。

**为什么这不是"事后挑口径"**：修改的是**模型可见的令牌预算**（能力条件），不是判决阈值、
样本集、prompt 或指标定义；且两轮**都被报告**。判据（四态、四指标、迁移三条件）一字未改。
