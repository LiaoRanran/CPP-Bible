# 670d 批次验收报告

- **批次**：670d（论文 v0.7 打磨 · 实验设计细化 · 相关工作深化 · 投稿准备）
- **分支**：master　**日期**：2026-09-30
- **执行者**：LiaoRanran（DCO）
- **性质**：在 670a（改 tests/ + data/experiments/）与 670c（改 web/ + queyi-verifier）**并行**期间独立完成；**只写 `research/` 新文件**（+ 本验收报告）。
- **对象论文**：`research/paper_v0.6.md`（670b 产出）。

---

## 0. 一句话

> 12 份建议/设计文件全部产出；**658 门禁无回归（L0 5/5）**；未碰 670a/670c 与受控目录。**本批为"投稿准备"性质，不新增实验数字**；顺带发现主文一处**数字不一致**（§6.4 的 block/warn/advice 计数 vs 现算）。

---

## 1. 任务 A · 论文 v0.7 打磨（4 文件）

| 文件 | 内容 | 关键结论 |
|---|---|---|
| `research/670d_结构优化建议.md` | 逐章问题 + 建议 | 主链（§1→§10）**逻辑正确无需重构**；真正缺口=**四张图全缺** + **每章缺引导句** |
| `research/670d_文字润色建议.md` | AI 腔/术语/被动/精简 | **AI 腔仅 1 处**（第 30 行"本文提出"）；真问题是**术语不一致：检测器(28) vs 探测器(3)** |
| `research/670d_图表设计spec.md` | Fig.1–4 设计 spec | 每图给数据来源/坐标轴/图例/标注/占位符；Fig.3 baseline 列全为 `{{TODO_670a}}` |
| `research/670d_摘要结论打磨.md` | 修改版 + 理由 | 摘要**补局限**（WSL/样本量/baseline）；结论**加证据边界**；关键词"度量治理"→"provenance 审计" |

> **红线 5 遵守**：全部为**建议清单/修改版**，**未改动** `paper_v0.6.md`。

---

## 2. 任务 B · 实验设计细化（3 文件）

| 文件 | 内容 |
|---|---|
| `research/670d_baseline实验设计.md` | B1/B2/B3 **命令级**实现、I/O schema、budget-matched 保证、McNemar 配对表 |
| `research/670d_数据扩样方案.md` | holdout≥30（**须建新盲集**，现集不可回盲）/ corpus≥60（**分散检测器**对冲 WSL）/ 反事实≥30（**标签独立于判据**） |
| `research/670d_独立复现协议.md` | 环境/命令/判定标准/失败模式/报告模板；**勘误 `REPLICATION.md` 三处** |

**关键诚实点**：
- 扩样目标（30/60/30）**仍不足以支撑 Δ=15pp 显著性**（需 n≈102–172）——只把点估计变窄。
- 缺 WSL 时**必须判 `UNVERIFIED`**，不得判 FAIL（防"环境缺失"被误读为"能力不足"）。
- `REPLICATION.md` 仍写"holdout 20 样本"（实为 30）、标 WSL"可选"（实为硬依赖）——**建议勘误**。

---

## 3. 任务 C · 相关工作深化（2 文件）

| 文件 | 内容 |
|---|---|
| `research/670d_邻近工作对比表.md` | **6 工作 × 6 维**（Benchmark Self-Evolving / ArenaBencher / Meta ACH+MUTGEN / SWE-bench Verified+Pro / MiniCheck / LiveBench） |
| `research/670d_引用补充建议.md` | **6 条**建议（4 条本轮 general_search 已核）：LLM 代码错误分类 ×2、污染综述 ×2、mutation 综述、备选 |

**核心结论**：6 个邻近工作中 **5 个在换"被测物"**，**没有一个在换"尺子"并证明换尺子可被外部度量**——这正是祈易的位置。

---

## 4. 任务 D · 投稿准备（3 文件）

| 文件 | 内容 |
|---|---|
| `research/670d_投稿格式检查.md` | NeurIPS E&D 逐条对照；**三条硬阻塞**：页数（30+→9）、匿名（仓库路径外泄）、baseline 缺失 |
| `research/670d_cover_letter草稿.md` | 英文投稿版 + 中文对照；**主动声明 baseline 缺口** |
| `research/670d_附录设计.md` | 附录 A–E（数据集 schema / 67 规则 / 逐样本明细 / 复现命令 / AI 声明） |

---

## 5. 任务 E · 收工

| 检查 | 结果 |
|---|---|
| 产出 research/ 新文件 | **12 个**（A4 + B3 + C2 + D3） |
| 658 门禁无回归 | **`overall=PASS  L0 5/5  L1_fail=0`**（S0–S6 全 PASS） |
| 是否碰 670a（tests/、data/experiments/） | **否** |
| 是否碰 670c（web/、queyi-verifier） | **否** |
| 是否碰受控目录（atoms/ evidence/ Examples/ Book/ 452 账本） | **否** |
| 提交 | `git commit -s`（DCO），**不 push** |

---

## 6. 诚实登记（本批发现的问题）

1. **主文数字不一致（重要）**：`paper_v0.6.md` §6.4 写"67（**block 0 / warn 176 / advice 55**）"，而现算 `gate_engine.RULES` 为 **block 44 / warn 16 / advice 7**。二者不符——**请主文作者核对**（见 `670d_附录设计.md` 附录 B）。
2. **术语不一致**：全文"检测器"28 处 vs "探测器"3 处（第 300/701/751 行）——建议统一。
3. **四张图全缺**：Fig.1–4 均未插入、无引用、无图注。
4. **`REPLICATION.md` 过期**：holdout 20→30、WSL"可选"→硬依赖、缺 `env` 字段。
5. **页数硬阻塞**：主文 30+ 页 → E&D 限 9 页，需"主文压缩 + 附录承载"。
6. **本批不新增实验数字**：所有数字来自 v0.6 已有产物；baseline/ablation 仍待 670a。

---

## 7. 新增文件清单（670d）

**research/**：`670d_结构优化建议.md`、`670d_文字润色建议.md`、`670d_图表设计spec.md`、`670d_摘要结论打磨.md`、`670d_baseline实验设计.md`、`670d_数据扩样方案.md`、`670d_独立复现协议.md`、`670d_邻近工作对比表.md`、`670d_引用补充建议.md`、`670d_投稿格式检查.md`、`670d_cover_letter草稿.md`、`670d_附录设计.md`
**data/**：`670d_acceptance_report.md`（本文件）

> `research/paper_v0.6.md` **未被修改**（红线 5：本批只给建议）。
