# 667 批次验收报告

> **【668 结清】** §6.1（81.2% 裁决）与 §6.2（反事实未重跑）**已由 668 批解决**：
> 重跑落盘后 holdout = **87.5%（14/16）**、反事实 F1 = **1.0（分母 10，上界）**；
> `web_metrics_666 --check` 的射程已补齐（三个率都比对 + 射程自检）。
> §6.3（external 分母）已加 `denominator` 字段。本报告保留当时判断，不追改。

> 执行对象：用户 brief「667 夜间大包：全量大复盘 → 究极大规划 → 前端继续加强」
> 执行时间：2026-09-30　｜　执行者：Agent（AI 参与；**有人工复核项未完成**，见 §6）
> 本报告的目标不是"报喜"，而是**让下一批知道哪些数字被作废、哪些检查是假的、哪些必须人做**。

---

## 0. 一句话结论

- **阶段 0/1a/1b 全部交付**：三份文档（复盘 / 反思 / 规划），其中规划是**带月度里程碑、四象限、止损线与冻结清单**的可执行版本。
- **阶段 2 前端交付**：新增判决页（仪表盘 + 判决历史表 + 数据对比表）、星图加强、琉璃质感令牌、
  表格/空状态/44px 触控；并**修掉一个真缺陷**（对比度检查只验了浅色主题）。
- **阶段 3 收工门禁绿**：`run_658_gate` **PASS**（L0 5/5 / L1 0 失败）、`status_reconciler --check` **OK**。
- **本批最重的产出其实是一个坏消息**：`web/data/metrics_666.json` 里的 **holdout 检出率 81.2% 当前无法复现**
  （现算 66.7%），而守护它的 `--check` **根本没查这个字段** ⇒ 报绿。同族第二个：反事实 F1。
  这两条已登记为 **P0/P1 缺陷并交人裁决**，机器**没有**自行把数字改回去。

---

## 1. 阶段 0 · 全量复盘（`docs/667_全量复盘.md`）

### 1.1 现算锚点（全部脚本现算，不是抄来的）

| 锚点 | 值 | 复算方式 |
|---|---|---|
| HEAD / 分支 | `4ae457d2` / `master`，ahead 0 behind 0 | `git log` + `status_reconciler_658 --check` |
| 实卡 / 草稿 / 卡总数 | **37 / 10 / 47** | `counts_659.ATOMS_REAL / ATOMS_DRAFT / ATOMS_TOTAL` |
| `atoms/**/*.md` | **48**（= 47 卡 + `README.md`） | `glob` ⇒ **48 不是卡数**，已登记为口径差 |
| 规则 | **67**（两源一致） | `len(gate_engine.RULES)` == `data/_gate_rules.json` |
| 保护器 | **9**（镜像自拆仓 `queyi-core`） | `web/data/status.json` |
| 内核 | **813 行**（`queyi-core/tools/queyi_core_v10_641.py`） | 本机行数实测 |
| 账本 | **452** 事件（红线零改） | jsonl 非空行数 |
| 图 | 178 节点 / 1093 边 | `status_reconciler_658 --check` |
| 变异 | core **97.3%**（on_scored）/ 74.8%（全部变异体） | `data/656_mutation_report_core.json` |
| 逃逸 | **0.0711%**（1/1406，616 冻结契约） | `web/data/status.json` |
| holdout | 30 样本 / 真错 17 / 对照 9；**现算检出率 66.7%（10/15）** | `data/holdout_reveal_3_665.json` |
| external | 40 条 / catch 14 / miss 18；**43.8%（14/32）** | `data/external_corpus_reveal_665.json` |

### 1.2 口径差登记（8 项，逐个定位到权威源，不静默替换）

见文档 §2。要点：卡数 **47 vs 48**、规则 **67 vs 63**、节点 **178 vs 121**、holdout **81.2 vs 66.7**、
external **分母 32 vs 40**、变异 **on_scored vs 全部**、反事实 **1.0 vs 0.0**、时间线 state 语义。

### 1.3 调研盘点（v37 → v47）

- 实扫 8 个目录（10 / 18 / 24 / 14 / 35 / 60 / 100 / 150 份）。
- 跨目录**去重后**只剩 **12 条**可落地行动（R1–R12），其中**已落地的只有 2 条半**。
- **冻结 9 类**：Rust/Verus、ASM 指令级、WASM 重前端、完整形式化、规则架构重写、数据库换型、
  自动科学发现/NAS/RL、v47 的 61–135 号方向、新增调研目录。
- 统计建议已摘录进规划 §4.4：Clopper–Pearson / Wilson / Fisher / 精确 McNemar / BH / Holm /
  ICC·DEFF·n_eff / Cohen's κ · Krippendorff's α / random-budget 对照。

### 1.4 债务盘点

- 台账 4 票（DEBT-001/002/003/005，负债率 20% > 15% ⇒ **仍在停线**）；
- 666 遗留 3 项（debt 停线 / evidence 648 重定向口径 / slow 6 红）+ 三个链路自污染未根治；
- 665 结转（拆仓写死去债 33 项、Book 拆卡、86 条版本漂移红）；
- **667 新增 7 项**（N1–N7），其中 **N1/N6 是同族**：改了口径/判据但**没重跑落盘**。

---

## 2. 阶段 1a · 回溯反思（`docs/667_回溯反思.md`）

- 逐批回顾 **655 → 666**（12 个批次）：目标 / 实际 / 未达成 / 根因，逐格填。
- 六条关键失误，每条带产物级证据：
  ① 656 变异"没进射程"（`--check` 射程自检首版存活）；
  ② 660 seed 标签过度声称（20 样本仅 7 真错）；
  ③ 665 分母未声明（**纠正了 brief 的说法**：43.8% 算术自洽，真缺陷是分母没写）；
  ④ 666 三个链路自污染；
  ⑤ B3 去写死盲替危险（同一个字面量在不同上下文指不同量）；
  ⑥ 标签本身是最大误差源（反事实判据与标签同源）。
- 四条**做对了**的决策：Protocol 提前写、断言换不变量、边界拆分、门禁分层。
- 六类反复踩坑（写死值 ≥9 次 / CRLF / push 人签 / 假红 / 口径差 / 用词过宽）。
- ⇒ 固化 **R1–R12 避坑规则**，每条带"怎么算遵守"的判据；1b 的每个任务都声明了它遵守哪些规则。

---

## 3. 阶段 1b · 究极大规划（`docs/667_究极大规划.md`）

| 章节 | 内容 |
|---|---|
| 总目标 | 三条可验收终态：**数字可信 / 有对照 / 有人验**；投稿 NeurIPS 2027 E&D（日程 **[待核]**，按 2027-06 窗口倒排） |
| 路线图 | 2026-10 → 2027-09 共 **11 个月度里程碑**，每月一个 `git tag`，**没有"理论完善"型阶段** |
| 任务拆解 | 四象限：Q1 紧急重要 **6 条**、Q2 主线 **8 条**、Q3 可等 **6 条**、Q4 冻结 **9 类**；每条带交付物/验收/时长/依赖/规则 |
| 数据扩展 | **47 → 80 → 150**：**先补边界三元组**（47 卡 0 边界 ⇒ 四态恒 unknown），再拆卡；单卡 1.5–2h，33 张 ≈ 50–66h |
| 实验计划 | ablation **A–F**（含 random-budget）、budget-matched 四 baseline、盲态/非盲态/external 三层**不许合并** |
| 统计口径 | Clopper–Pearson + Wilson 敏感性、Fisher/Boschloo、精确 McNemar、BH/Holm、效应量+CI、ICC/n_eff、κ/α；**样本量反算：±10pp 需 n≈93–104** |
| 论文计划 | v0.5→v1.0 六版，Claim 边界表三条规定（数字变必同步、答不出复算命令就不进表、❌ 项不许删） |
| 防烂尾 | 每阶段 tag / ACTIVE·FROZEN·ABANDONED 三状态 / **外部复现硬节点（2027-04）** / 四条止损线 / 周最小格 |
| 风险 Plan B | 范围膨胀、基础设施替代研究、单人 burnout、**2027-04 考研分岔**、复现者找不到、第二标注者找不到 |

---

## 4. 阶段 2 · 前端深化（`docs/667_frontend.md`）

### 4.1 交付

| 类别 | 文件 |
|---|---|
| 新增 | `web/verdicts.html`、`web/verdicts.js`、`web/verdicts_core.js`、`web/data/verdicts_667.json`、`tools/web_verdicts_667.py`、`tools/web_logic_check_667.mjs`、`tools/web_smoke_667.mjs`、`tests/test_web_verdicts_667.py`、`docs/667_frontend.md` |
| 修改 | `web/css/design-tokens.css`（琉璃组 + `--touch-min`）、`web/style.css`（667 段）、`web/starmap.html`、`web/starmap.js`、`web/components/qy-nav.js`（加"判决与数字"入口）、`tools/web_data_pipeline_656.py` |

### 4.2 七项要求逐项

| 要求 | 结果 |
|---|---|
| ① 琉璃质感 | ✅ 毛玻璃 + **不透明回退** + 节点辉光（pass/fail/unknown）+ 渐变；辉光只给小语义元素 |
| ② 表格美化 | ✅ 判决历史（时间倒序/色标/搜索/3 筛选/6 排序/空状态）+ 对比表 + 空状态设计 |
| ③ 星图加强 | ✅ 聚类分色（展示层小写归一）+ 连线按**派生**权重 + 搜索 + 聚类筛选 + 缩放 + cluster 展开 + hover 微发光 |
| ④ 层级与留白 | ✅ 标题大而松 / 正文小而密 / 注释淡；桌面端 section 留白 48→64px |
| ⑤ 仪表盘 | ✅ 8 个大数字，**脚本现算**；漂移格自己标红 |
| ⑥ 动效 | ✅ 数字滚动 / hover 辉光 / 尊重 `prefers-reduced-motion`（reduce 下**关掉**而非变快） |
| ⑦ WCAG AA 现算 | ✅ **26 对（13 组 × 深浅两主题）全过** + 移动端 44px |

### 4.3 修掉的真缺陷（顺手）

`tools/web_data_pipeline_656.py` 的 `parse_tokens()` 对同名变量**取最后一次出现**，
而 `design-tokens.css` 里浅色块写在后面 ⇒ `--check` **实际只验了浅色主题**，
深色主题从未被算过（666 B1 却声称"深浅两套都过"）。
改为 `parse_token_blocks()` **分主题解析**，并新增 5 组"四态色当文字用"的规则（阈值 3.0 → 4.5）。

### 4.4 验收实测

| 检查 | 结果 |
|---|---|
| `pytest tests/test_web_verdicts_667.py`（+ 666 的 web 测试） | **18 passed** |
| `pytest -k "web or pipeline or frontend or starmap or tokens" -m "not slow"` | **35 passed** |
| `node tools/web_logic_check_667.mjs`（Node 真求值） | **28 passed / 0 failed** |
| `node tools/web_smoke_667.mjs`（jsdom **真跑 DOM**） | **23 passed / 0 failed**（本机 Node 18 + jsdom 实测可跑，**未 SKIP**） |
| `ruff` / `mypy`（新工具 + 管线） | **0 / 0** |
| `node --check`（verdicts.js / verdicts_core.js / starmap.js） | 全过 |
| `tools/web_data_pipeline_656.py --check` | **PASS**（含 26 对对比度） |
| `tools/web_verdicts_667.py --selftest / --check` | **PASS / 与现算一致** |

### 4.5 判决历史只有 31 条（故意的）

只收**有逐条 verdict** 的产物：机器卡 16 + 缺陷夹具 15。
holdout 30 / external 40 **只有聚合数** ⇒ 编不出来也不编；反事实 10 条**算子改了产物没重跑** ⇒ 不进表。
两者都写进 JSON 的 `excluded` 与页面「为什么只有这些条目」。

---

## 5. 阶段 3 · 收工

| 项 | 结果 | 命令 / 现场 |
|---|---|---|
| 658 门禁 | **PASS**（L0 5/5，L1 失败 0） | `python tools/run_658_gate.py` |
| 元状态对账 | **OK** | `python tools/status_reconciler_658.py --check` |
| 全量非 slow | ❌ **未跑完**（后台串行跑了 ~15 分钟仍未结束，收工时按"未跑完"登记） | `pytest -m "not slow" -n0 -q`（输出原计划写 `data/667_fast.txt`，未生成） |
| `_auto/status.json` | ✅ 已更新（`active=667 / next=668 / last_completed=667`，666 归档进 `prev_current_task_666`） | 未代签 |
| 提交 / push | ❌ **未做**（改动留在工作树，待人复核） | 见 §6.4 |

### 5.1 红线核对

| 红线 | 结果 |
|---|---|
| 受控目录 `atoms/ evidence/ Examples/ Book/` 零改动 | ✅（本批只读） |
| `data/646_authority_rule_annotation.jsonl` 452 事件零改 | ✅（只读计数） |
| `verified` 唯人签 | ✅（本批未给任何卡/命题加签名） |
| 不代签（golden_lock `--accept` / debt_ledger 停线 / OTS） | ✅ 未代签 |
| 不擅自 push | ✅ 未 push |
| 不许"为了绿"改断言或阈值 | ✅ 新增测试的断言锁的是**不变量**（如 `drift == (stored != fresh)`），不是当前数字 |
| 不写死数字 | ✅ 前端新页 100% 读现算 JSON；对比度 26 对现算 |

---

## 6. 交人项（**都需要人**，机器不代做）

### 6.1 P0 · 81.2% 裁决（最紧）

`web/data/metrics_666.json` 的 holdout 检出率 **81.2%（13/16）** 无现算来源；
现算 **66.7%（10/15）**，且产物 `honest_addendum` 自述是 **-O1 单档**口径。
`web_metrics_666.py --check` 只比对 5 个字段，**不比对 holdout/external** ⇒ 假绿。

二选一（**人定**，机器不自行改）：

```powershell
# 看清楚差在哪
.venv\Scripts\python.exe -c "import sys,json;sys.path.insert(0,'tools');import web_metrics_666 as w;print(w.collect()['metrics']['holdout'])"
.venv\Scripts\python.exe -c "import json;d=json.load(open('data/holdout_reveal_3_665.json',encoding='utf-8'));print(d['error_subset']);print(d['honest_addendum'])"
# 路线甲：重跑双档 pipeline，拿回 13/16 并落盘（然后 --write）
.venv\Scripts\python.exe tools\holdout_reveal_3_665.py
# 路线乙：承认 66.7%，把 81.2% 标为「旧值作废」，同步改 paper_v0.4 与 metrics_666
```

**顺带**：`tests/test_web_metrics_666.py::test_holdout_rate_is_dual_opt_caliber` 断言的是
`"双档" in h["caliber"]`，而 `caliber` 是工具里**写死的字符串**（不是从产物读的）
⇒ 这个测试锁的是**标签**而不是数据源，属于同类"标签自证"假绿，建议一并改成读产物口径。

### 6.2 P1 · 反事实：改了代码没重跑

第三判据 `_MACHINE_MARKERS` 已在 `tools/counterfactual_citation_658.py:32/44/66`，
但 `data/counterfactual_cases_665.json` 仍是旧算子（10 条 / `f1: 0.0`），论文 v0.4 写 20 条 / F1=1.0。

```powershell
.venv\Scripts\python.exe tools\counterfactual_extend_665.py     # 重跑落盘
```
未重跑前，**F1=1.0 不得对外引用**。

### 6.3 P1 · external 分母字段

产物与前端都写"40 条 43.8%"，实际分母是 32（14/32），按 40 算是 35.0%。
667 的新页已经两个都显示；**老产物与 paper_v0.4 仍需补 `denominator` 字段**。

### 6.4 其余

- **提交与 push**：本批改动仍在 **工作树**（含 666 遗留的 24 项脏文件，其中 20 个是 `_arch_v47` 未跟踪文件）。
  建议分两组提交：① 667 批次文件；② `_arch_v47` 未跟踪调研稿（或明确声明不入版本控制）。
  push 仍会被 `pre-push` 的 quality 拦（666 的三项：golden_lock / evidence_replay / debt_ledger 停线）。
- **工作树里 `tools/golden_state.json` 已改未提交**（666 遗留），需人决定采用或还原。
- **dist 超预算**：24 个资源 158,305B → **136,986B**（666 是 92.8KB / 13 个）。是否接受、是否压缩，人定。
- **OTS 真锚定**（`ots stamp`）仍需人执行。

---

## 7. 诚实登记：本批**没做到**的

1. **屏幕阅读器（NVDA/VoiceOver）实测、全站键盘走查、200%/400% 缩放重排、axe 扫描 —— 全未做**
   ⇒ **不能声称"WCAG 2.2 AA 通过"**，只能说"能自动验的部分现算通过（26 对）"。
2. **真浏览器控制台未看**：本机 Node 18，Playwright 要求 ≥20 ⇒ 星图的新控件只过了 `node --check` 与人工复核步骤。
3. **星图未在 jsdom 验**：canvas `getContext` 在 jsdom 返回 null（会崩）；新增的聚类/权重函数无自动断言覆盖。
4. **dist 超 100KB 预算**（见 6.4）。
5. **学习页（B4）未深化**：自测仍是朴素形态，无错题本 / 间隔重复。
6. **全量非 slow 套件未跑完**：后台串行启动后 ~15 分钟仍未结束（本仓既有记录：fast 约 50 分钟量级），
   收工时按**未跑完**登记，**不假设它绿**。已跑的替代口径：
   `tests/test_web_verdicts_667.py + test_web_metrics_666.py` **18 passed**、
   `-k "web or pipeline or frontend or starmap or tokens"` **35 passed**。
   需要完整结论时请人跑：`.venv\Scripts\python.exe -m pytest -m "not slow" -n0 -q`（**串行**，别用 `-n auto`：666 实测并行会冒 35 条假红）。
7. **slow 套件未跑**（666 的 6 红仍是 6 红，本批未动）。
8. **论文未更新**：paper 仍在 v0.4；v0.5 的数字修订**依赖 6.1/6.2 的人裁决**，机器不先改。
9. **人工复核未做**：本批新增/修改了前端渲染路径与一个既有工具（管线），**尚未**逐条人工确认；
   `research/AI_USAGE_LOG.md` 应补一条本批条目（**本批未自动写入**，交人）。
10. **未提交、未 push**（见 6.4）。

---

## 8. 本批新增债（登记，不隐藏）

| 债 | 性质 | 建议 |
|---|---|---|
| N1 holdout 81.2% 无现算来源 + `--check` 不查 | 数据可信度 | P0，见 6.1 |
| N2 external 分母未声明（老产物/论文） | 表述不自洽 | P1，补字段 |
| N3 `_arch_v47` 20 个文件未入版本控制 | 调研资产不可复算 | P2 |
| N4 主仓无法独立复算拆仓的 9 保护器 / 813 行内核 | 复现缺口 | P1，见规划 §7 |
| N5 工作树脏 24 项（含 `tools/golden_state.json`） | 门禁判脏 | P1 |
| N6 反事实产物未重跑 | 同 R6 违反 | P1，见 6.2 |
| N7 对比度检查只验浅色主题 | 检查器假绿 | ✅ **本批已修**（分主题解析，26 对全过） |
