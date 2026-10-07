# 691 题名评估（S2）：撞名核查 → 决策 → 全文件同步

- 日期：2026-10-07（在线核查当日）· 触发：690 指出 "Auditing the Evaluator" 可能进入他人命名区

---

## 1. 撞名核查（联网，2026-10-07）

| 来源 | 题名 / 机制用语 | 关系 | URL |
|---|---|---|---|
| **PROPOR 2026**（ACL Anthology） | *Auditing the Evaluators: How Far Can Automatic Evaluation Go in Assessing Portuguese Financial Texts?* | **近乎同名的第三方题名**（"Auditing the Evaluator**s**"） | aclanthology.org/2026.propor-1.22 |
| **ACL Findings 2026** / arXiv 2507.05619 | *Detecting Proxy Gaming in RL and LLM Alignment via **Evaluator Stress Test** (EST)* | 我们的旧副标题 "**Stress-Testing** Evidence-Based…" 与其核心术语高度重合 | aclanthology.org/2026.findings-acl.513 |
| **DeepFact**（ACL 2026 long 1586 / arXiv 2603.05912） | 核心机制名 **"Audit-then-Score" (AtS)** | "audit" 已是其机制名 | aclanthology.org/2026.acl-long.1586 |
| **BabelJudge**（arXiv 2606.22329） | 自述为 "open-source benchmark and **reliability audit framework**" | "audit framework" 已被占用 | arxiv.org/abs/2606.22329 |
| arXiv 2607.08535 | *When the Judge Changes, So Does the Measurement: **Auditing** LLM-as-Judge Reliability* | 同向命名 | — |
| arXiv 2606.19714 | *AURA: Adaptive Uncertainty-aware Refinement for LLM-as-Judge **Auditing*** | 同向命名 | — |
| **Who Grades the Grader?**（arXiv 2607.12790） | Co-Evolving Evaluation Metrics and Skills… | 仅作近邻定位，无撞名 | arxiv.org/abs/2607.12790 |

**判定**：689 的新题名 **同时**踩中两个 2026 年高密度用语（"Auditing the Evaluator(s)" 与
"Evaluator Stress-Test"），且 "audit" 在 2026 年评估方向**至少四篇**工作用作核心定位词。
690 的 E-1 判断**成立**。

> 但同时必须承认：689 的结构性重构（不承诺演化增益、把失败写成 Finding 5）**是必要且正确的**，
> 690 建议"回到 Evolving Verifiers"在当前证据下不可行（该 claim 已被自身实验否证）。因此本批
> **不推倒骨架，只退出命名拥挤区**。

## 2. 候选与决策

| 方案 | 内容 | 评估 |
|---|---|---|
| A 保留旧题名 | "Auditing the Evaluator: Stress-Testing…" | ✗ 两个用语都被占；可检索性受损 |
| B 全新题名 | 见下 | **✓ 采纳** |
| C 只改副标题 | 保留 "Auditing the Evaluator" 主标题 | ✗ 主标题正是撞名处 |

**采纳题名**：

> ### Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation

**理由（按权重）**：
1. **主标题由自有术语构成**：`caliber drift`（8 类失败模式之一，论文的签名概念）与
   `capability boundaries`（Finding 2）——在线检索未见他人以此为题名（"caliber drift" 无同题命中）；
2. **不再使用被占用的完整短语**："Auditing the Evaluator(s)"（PROPOR 2026）与
   "Evaluator Stress Test"（EST, ACL Findings 2026）均避免；
3. **保留方法名而非定位词**：副标题用 "An Audit Protocol …"（我们 §3 的方法名
   *The Evaluator-Audit Protocol*），属于**方法声明**，不是抢占方向命名；
4. **领域可检索性**："Software-Verification Evaluation" 明确对象与领域；
5. **与正文结构一致**：§3（协议）/§5（5 个发现，含 caliber drift 与能力边界）直接呼应，
   读者不会遇到"题名承诺 ≠ 正文内容"。

## 3. 同步清单（全部完成）

| 文件 | 状态 |
|---|---|
| `research/latex/queyi_neurips2027_v1.1.tex`（`\title` + 文件头） | ✅ |
| `research/latex/arxiv_submission/queyi_neurips2027_v1.1.tex` | ✅ **从 canonical 重新派生**（含全部 691 修正），实名版 34 页独立编译通过 |
| `research/latex/arxiv_submission/README.txt` | ✅ 题名 + 691 repack 段 + 页数更新 |
| `research/cover_letter.md` / `research/latex/cover_letter.tex` | ✅（tex 编译通过） |
| `research/response_template.md` / `research/latex/response_template.tex` | ✅（tex 编译通过；689 题名保留为历史项） |
| `research/latex/VERSION.md` | ✅ v1.5 + §5sexies 变更清单 |
| `queyi_arxiv_v1.6_realname.tar.gz` | ✅ 4 文件顶层、摘要 1776 字符 ≤1920 |

**未改**：`data/689_究极重构验收报告.md`（历史记录，保留 689 当时的题名与结论），
由 691 报告说明后续变更——不重写历史文件。
