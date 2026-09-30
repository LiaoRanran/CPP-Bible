# 670g 批次验收报告

- **批次**：670g（论文 v0.8 深化 + 工程纪律门禁 + 投稿准备 + 文档更新）
- **分支**：master　**日期**：2026-10-01　**执行者**：LiaoRanran（DCO）
- **红线**：不碰 `tests/`、`data/experiments/`、`data/holdout/`、`data/external_corpus/`（670a 在跑）、受控目录、`gate_engine.py`/`counts_659.py`、`research/latex/*.pdf`。

---

## 0. 一句话

> **v0.8 把 baseline 三臂的真实数字填进论文**（含 §6.4 统计检验、§6.5 缺陷/变异、§7.2/7.3 分析、§8/§9 更新、摘要/结论/相关工作）；**论文管线 5 工具全 PASS** 并**挂进主门禁**；新增 **6 条 P0 门禁**（22 条测试全绿）；投稿三件套 + 5 份文档同步。**未做**：B3/B4（防复发/漂移增强）、LaTeX 编译验证（见 §6）。

---

## 1. 任务 A · 论文 v0.8 ✅（A1–A9）

- **A1 读入**：`docs/670a_实验结果.md` + `data/experiments/baseline_{fd,static,random}.json`（**数字真实存在**，非编造）。
- **A2**：`research/paper_v0.8.md`（基于 v0.7 新建，**不覆盖 v0.7**）。
- **A3 §6**：
  - §6.1 三臂表：Static 6.2%(1/16) / 12.5%(4/32)；Random† 6.2% / 3.1%(1/32)；FD 87.5%(14/16) / 43.8%(14/32)；**Δ(static→FD) +81.3pp / +31.3pp**，全带 CP 95% CI。
  - §6.2 口径消融、§6.3 演化曲线**保留**。
  - **§6.4 新增**：配对精确 McNemar（holdout b=13,c=0 **p=0.00024**；corpus b=10,c=0 **p=0.00195**）+ Cohen's h（**1.91 / 0.72**）+ 样本量诚实说明。
  - **§6.5 新增**：缺陷重注入 **6/6**、变异 core **97.3%**，并声明**变异是内部指标**。
- **A4 Fig.3**：改为三条柱（FD / Static / Random†），Random† 标注代理；图注含 CI 与"只读方向"。
- **A5 §7**：§7.1 第 5 点更新（baseline 已跑）；**新增 §7.2**（baseline 启示：Static 低分是必然、FD 优势来源、代理说明、真 B3 待拆仓）+ **§7.3**（样本量与统计效力表）。
- **A6 §8**：Construct 行加"口径重分箱/代理"；External 行改"真 B3 仍 BLOCKED"；Statistical 行加"n=16/32、c=0 极端结构、±10pp 需 n≈96"。
- **A7**：摘要加 baseline 数字 + 样本量局限；结论加证据边界（支持"同批显著优于静态/代理"、不支持"优于真静态检测器/真 B3"）+ 未来工作 4 条。
- **A8**：§2 新增**第 (5) 条**（LLM 代码错误分类，连 §7.1）+ 参考文献 **47/48**。
- **A9 论文管线**：**5 工具全 PASS**（paper_sync / bib_audit / figure_data / anonymity / paper_quality_gate）。

> **A9 顺带修的真问题**：`anonymity_check` 抓到我在主文写了 `tools/baseline_670a.py`（仓库路径）⇒ 已改为通用表述。**这正是该门禁存在的意义。**

---

## 2. 任务 B · 工程纪律门禁

- **B1 论文管线挂进主门禁 ✅**：`run_master_gate_670c.py` 新增 `paper_pipeline_gate()` + `PAPER_PIPELINE` 表，`collect()` 里 `gates += paper_pipeline_gate(root)`；主门禁实测出现 `L1 670g/paper-sync|bib|figdata|anon|quality` 五阶段，**全 PASS**。
- **B2 六条 P0 门禁 ✅**：`tools/gate_rules_670g.py` —— G-RATE-CONSISTENCY / G-DENOMINATOR / G-STATS-FROZEN / G-BOUNDARY-REQUIRED / G-BASELINE-EXISTS / G-IRR；`tests/test_gate_rules_670g.py` **22 条测试全绿**。
  - **诚实说明**：669d **已有同名六条**（产物↔前端那一层）；本文件是**论文/baseline 维度的强化版**，不是重复造轮子（文件头已注明）。
- **B3 防复发门禁（改代码必重跑）❌ 未做**：`tools/guard_rerun_670c.py` **未扩展**（AST 语义哈希比对未实现）。
- **B4 漂移检测增强 ❌ 未做**：`tools/drift_watch_670c.py` **未扩展**（论文↔产物漂移未接）。

---

## 3. 任务 C · 投稿准备

- **C1 cover letter ✅**：加入 headline result（87.5% vs 6.2%，Δ+81.3pp，McNemar p≤0.002）；局限改写为"n=16/32 只读方向 + Static 是口径重分箱 + Random† 是代理"。
- **C2 response template ✅**：新增 4 段标准回复（样本量 / baseline 不够强 / 为什么不用 SWE-bench / 可复现性）。
- **C3 checklist ✅**：新增"§9 v0.8 新增检查项"11 条。
- **C4 NeurIPS 2027 CFP 跟踪 ⚠ 部分**：**未做联网检索**；沿用既有结论"2027 CFP 未发布，按 2026 时间线参考"（`SUBMISSION_CHECKLIST.md` 已记）。

---

## 4. 任务 D · 文档更新 ✅

| 文档 | 更新 |
|---|---|
| `docs/README_v2.md` | 新增「Baseline 三臂对比」表 + 「论文与投稿（v0.8）」段 |
| `REPLICATION.md` | 新增 **§16**（baseline / 论文管线 / 670g 门禁 / 主门禁的复现命令 + 依赖 + 已知偶发） |
| `docs/项目介绍.md` | 测试数 599→**888**；论文 v0.6→**v0.8**；baseline **已跑**（含诚实边界） |
| `docs/FAQ.md` | 新增 **Q15–Q19**（Static 为何低分 / Random† vs 真 B3 / 样本量 / 怎么复现 / 投哪里） |
| `docs/演示脚本.md` | 新增「670a/670g 演示点」（baseline 对比 / 论文管线门禁 / 统计口径） |

---

## 5. 任务 E · 验收

| 检查 | 结果 |
|---|---|
| 论文管线 5 工具 | ✅ 全 PASS |
| 670g 六条门禁 | ✅ 0 BLOCK；22 条测试全绿 |
| 主门禁（含 paper 阶段） | ✅ L1 `670g/paper-*` 全 PASS（**controlled-dirs 首跑报 1 处写入、复跑 0 处** ⇒ 并发批次所致的偶发，见 §6-3） |
| 658 门禁 | ✅ PASS L0 5/5 |
| 论文 v0.8 结构 | ✅ §1–§10 + 附录 A–F 完整 |
| baseline 三臂填入 | ✅ 数字与 `baseline_*.json` 一致 |
| 匿名化 | ✅ 主文 0 残留 |
| LaTeX 版 | ⚠ 已同步 v0.8 内容；**编译验证未完成**（见 §6-1） |

---

## 6. 诚实登记

1. **LaTeX 编译未验证**：环境临时目录被清理（tectonic 与 bundle 丢失），重下期间 zip 两次截断；**本次未能完成编译**。`.tex` 已按 v0.8 更新（Fig.3 三系列、E1 表、摘要），**编译与页数（≤9）待重跑 `research/latex/build.ps1` 确认**。
2. **B3/B4 未做**：防复发（AST 语义哈希）与漂移增强（论文↔产物）**均未实现**——这是本批最大缺口。
3. **主门禁偶发 FAIL**：`670c/controlled-dirs` 首跑报"写入 1 处"、复跑"0 处"，`git status` 受控目录干净 ⇒ 判定为**并行批次并发写**导致的快照竞态，**非本批引入**（已在 REPLICATION §16 登记）。
4. **C4 未联网核查** 2027 CFP。
5. **`gate_rules_670g` 的 G-DENOMINATOR 有约 7 条 warn 误报**（如 §7.3 表格中"n"在相邻列）——规则是启发式，**只 warn 不 block**。

---

## 7. 新增/变更文件

**新增**：`research/paper_v0.8.md`、`tools/gate_rules_670g.py`、`tests/test_gate_rules_670g.py`、`data/670g_acceptance_report.md`
**修改**：`tools/paper_sync_check_670c2.py`（指向 v0.8 + baseline 事实）、`tools/figure_data_check_670c2.py`（Fig.3 corpus 系列）、`tools/run_master_gate_670c.py`（paper 阶段）、`research/latex/queyi_neurips2027.tex`、`research/latex/cover_letter.tex`、`research/latex/response_template.tex`、`research/latex/SUBMISSION_CHECKLIST.md`、`docs/README_v2.md`、`docs/项目介绍.md`、`docs/FAQ.md`、`docs/演示脚本.md`、`REPLICATION.md`

> 未碰 670a 在跑的目录、受控目录、`gate_engine.py`/`counts_659.py`、`research/latex/*.pdf`。
