# 祈易（queyi）：一个"可被独立验收"的 C++ 知识验证器 —— 外部效度优先的评估设计（v0.1 骨架）

> 状态：**初稿骨架**（661 D1）。数据截至 2026-09-28（HEAD `96ac3b2e` 之后）。不追求完美，先把可站住的 claim 写下来。

---

## 摘要（Abstract，~150 词）

LLM 时代，C++ 教材与知识库的"错误"越来越多地由机器生成，而**验证器本身也可能是错的**：用自造变异分布证明自己有效，外部世界未必认。本文提出祈易（queyi）——一个面向 C++ 知识卡的验证器，其核心主张不是"检测率多高"，而是**"可被独立验收"**：判决规则内嵌引擎（67 条，44 block），边界结论由四态判决（pass/fail/unknown/unknown）给出，证据带 provenance，元状态由**不依赖验证器内核**的独立对账器核对。
我们给出四层外部效度的评估协议（真实缺陷注入 / 盲化 holdout / 独立生成 / 外部 corpus），并报告首轮实测：**真实缺陷重注入 6/6 命中**、**盲化 holdout 首次 reveal 为 catch 7 / miss 9 / unknown 4 / fp 0**。我们**不**把内部变异检出率（97.3%）当作缺陷检测率，并显式登记当前证据**尚不足以**支撑的 claim。

## 1. 引言（Introduction，半页）

C++ 的"事实"高度依赖**上下文**：同一段代码在 GCC/Clang/MSVC、不同标准版本、不同优化级别下，可能是 UB、unspecified 或完全合法。因此对 C++ 知识卡"断言对错"的验证，必须把**边界**（标准版本 / 编译器 / 平台 / 输入域）显式化，否则"验证通过"只是"在某个未声明的配置下通过"。

现有做法多止步于**自我诊断**：验证器自报覆盖、自报质量、自报元状态。问题在于——
1. **自证风险**：仪表盘由同一工具链自报；
2. **分布偏差**：变异算子由我们设计，验证器"熟悉"该分布；
3. **度量混淆**：把 mutation score 当缺陷检测率。

祈易的设计回应这三点：把验证器拆成"**执行权威**（gate_engine）"与"**独立对账器**（status_reconciler，不依赖内核）"；把评估写成**先定 Protocol、再跑**的流程（`research/05`）；把数据集按外部效度分层（D0–D4）。

本文贡献：(1) 一套可验收的验证器架构与 67 条判决规则；(2) 一套四层外部效度评估协议；(3) 首批诚实实测数据与明确的 claim 边界。

## 2. 方法（Method，一页）

**2.1 判决规则（Rule Engine）**：`tools/gate_engine.py` 内嵌 **67 条**规则（severity：44 block / 16 warn / 7 advice），全部 `automated` 且带 check 函数。规则按 scope 分 atom / evidence / repo / card 等；其中 4 条 `-HC`（高复杂度兜底：`EV-SERVES-EXIST-HC`、`ATOM-REL-TARGET-HC`、`ATOM-REL-UNKNOWN-HC`、`CARD-PATH-NOT-CANONICAL-HC`）为 block 级，实际会拦卡（661 A2 裁定：引擎为口径权威）。

**2.2 四态判决（four_state_verdict）**：边界结论不只有对/错，而有 `pass / fail / unknown / unknown` 四态；"unknown"是**一等公民**（检测器无能为力时诚实弃权，而非默认通过）。

**2.3 证据 provenance 与账本**：每条断言绑定可 replay 的证据（复现命令 + 期望输出 + 哈希）；`data/pck/` 台账 + `web/data/manifest.json` 记录派生产物 sha256，`web_logic_check_655.mjs` 现场校验台账一致性（660 B4-1 修复了 3 个证书哈希漂移）。

**2.4 独立对账器**：`tools/status_reconciler_658.py` **不 import 验证器内核**，只读 git 实际状态 + 文档陈述，核对元状态（HEAD / ahead / 质量 / dirty / 规则数 / 图节点数）是否漂移（661 A2 后：规则 67、节点 178 全对齐）。

**2.5 门禁分层与红线**：门禁分 L0（硬红）/L1（advisory）；受控目录（atoms/evidence/Examples/Book）与 452 条历史账本为**零改红线**。

## 3. 评估协议（Evaluation Protocol，半页）

**数据集（D0–D4 冻结，见 `research/05`）**：D0 开发（`Examples/atoms/` 147 夹具）、D1 历史（真实缺陷夹具）、D2 盲化 holdout、D3 外部 corpus、D4 独立生成。
**流程（Phase 0–7）**：0 元状态快照 → 1 构建 D0 → 2 历史回归（D1）→ 3 盲化 reveal（D2，不可逆）→ 4 预算匹配对照（失败驱动 vs 随机）→ 5 消融 → 6 外部 corpus（D3）→ 7 对账 + 分层指标报告。
**纪律**：D2/D4 在 Phase 3/6 前绝不可用于训练/调参；违反即实验作废。

## 4. 当前数据能支撑什么 claim（诚实边界）

| Claim | 支撑证据 | 强度 |
|---|---|---|
| 前端台账一致性可现场校验 | `web_logic_check_655.mjs` 4/4 绿（含 3 证书哈希） | 强（可复现） |
| 真实缺陷可被门禁重注入检出 | 6/6 可机械重注入子集命中（661 B2） | 中（子集小；9 条不可重注入） |
| 元状态可独立对账 | `status_reconciler --check` [OK]；规则 67/节点 178 对齐（661 A2） | 中强 |
| 盲化 holdout 首轮泛化 | catch 7 / miss 9 / unknown 4 / fp 0（661 B1，20 样本） | **弱**（见 §5） |
| 检测率高 | mutation core 97.3% / all 81.5% | **不得**当作缺陷检测率（内部效度） |

## 5. 威胁与效度（Threats to Validity，半页）

1. **自证**：仪表盘与内核同源 → 已用独立对账器对冲，但对账器本身仍需人核。
2. **自造分布偏差**：变异算子由我们设计 → 以盲化 holdout / 外部 corpus 对冲；当前 holdout 仅 20 样本，统计功效不足。
3. **holdout 标签可靠性（本轮新发现）**：661 B1 揭示多条 "miss" 实为**对照 atom**（自洽、无植入错）→ 660 C2 的 seed 标签存在**过度声称**，泛化结论暂不可下（须先复核标签）。
4. **环境依赖**：TSan 在 WSL 出现 `FATAL: memory mapping`（检测器不可用），sanitizer 检出与平台强相关 → 记为 unknown 而非 miss。
5. **选择偏差**：失败驱动选资可能只是"测得多" → 需 Phase 4 预算匹配对照（未跑）。
6. **度量混淆**：mutation score ≠ 缺陷检测率 → 指标分层（`research/08`）。
7. **复现危机**：编译器版本 / OS 差异 → OTS 锚 + 版本锁定（`research/11`）。
8. **AI 署名**：LLM 贡献须登记（`research/13` + AI_USAGE_LOG）。

> **本稿不做的 claim**：不声称"检测率 X% 的通用有效性"；不声称"holdout 泛化已成立"；不把内部变异率外推。
