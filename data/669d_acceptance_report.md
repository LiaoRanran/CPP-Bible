# 669d 批次验收报告（Acceptance Report）

- **批次**：669d（独立复现审计 · 新门禁落地 · 论文深化 · 数据攒集）
- **分支**：master　**日期**：2026-09-30
- **执行者**：LiaoRanran（DCO 署名）
- **性质**：在 669 工程**并行推进**期间，由 669d 独立完成；**不改动 669 工程正在改的文件**，全部新增物带 `669d` 后缀。

---

## 0. 一句话结论

> A 段 8/8 数字独立复现一致、corpus 差异根因钉死为**环境依赖（非造假）**；B 段 6 条 P0 门禁落地、29 测试全绿、门禁 `overall=PASS`；C 段 §2 补 3 个方向、§8 五层补映射、引用核验成报告；D 段四类数据扩样 + 统计口径冻结；E 段 658/669d 双门禁全绿、受控目录零改动、452 账本零改。**未发现造假；发现的均为口径/环境/门禁射程问题，已诚实登记。**

---

## 1. A 段 · 独立复现审计（只读）

| 项 | 声明值 | 独立重算值 | 结论 |
|---|---|---|---|
| holdout 检出率（planted=True 子集） | 87.5% | 14/16 = 87.5% | ✅ 一致 |
| 反事实引文算子 F1 | 1.0 | 1.0（tp=2/fp=0/fn=0） | ✅ 一致（上界） |
| external corpus 检出率 | 35.0% | 14/40 = 35.0%（WSL 可用） | ✅ 一致 |
| 变异测试 core 口径 | 97.3% | 97.3% | ✅ 一致 |
| 变异测试 all 口径 | 81.5% | 81.5% | ✅ 一致 |
| 实卡数 | 42 | 42 | ✅ 一致 |
| 门禁规则数 | 67 | `len(gate_engine.RULES)=67` | ✅ 一致 |
| 台账事件数 | 452 | `wc -l = 452` | ✅ 一致 |

- **A2 根因（最重要）**：外部 corpus 35.0% ↔ 10.0% 差异 = **WSL sanitizer 检测器缺位**导致 15 条 sanitizer 样本降级 `unknown`（真机 14/40=35.0%；模拟缺 WSL 4/40=10.0%），**护栏仍绿** ⇒ 属环境依赖，非造假。见 `docs/669d_corpus差异根因.md`。
- **A3 门禁真实性**：写保护 harness 零写入跑通 7 阶段；改数实验 **5/5 变红**；确认 `drift_guard` 有射程、`caliber_check` 对明细**无射程**、前端零射程。见 `docs/669d_门禁真实性.md`。
- **A4 受控目录完整性**：`atoms/ evidence/ Examples/ Book/ data/authority/` **零差异**；452 账本零改。
- **产出**：`docs/669d_复现审计.md`、`docs/669d_corpus差异根因.md`、`docs/669d_门禁真实性.md`。

---

## 2. B 段 · 新门禁规则落地

- **实现**：`tools/gate_rules_669d.py`（6 条规则）+ `tools/gate_tiers_669d.json`（层级登记）+ `tools/run_669d_gate.py`（一键编排）。
- **规则**：

| ID | 层级 | 作用 |
|---|---|---|
| G-RATE-CONSISTENCY | L0 | 检出率产物/前端/论文三处同源，不一致即 BLOCK |
| G-DENOMINATOR | L0 | 比率必带 denominator、k≤den、可从明细重算（容差 0.001） |
| G-STATS-FROZEN | L0 | 冻结口径须有 `tools/` 实现 |
| G-BOUNDARY-REQUIRED | L0 | verified 卡须有 provenance 三元组，草稿卡须显式 `boundary: unknown` |
| G-BASELINE-EXISTS | L0 | 实验率指标须有同指标 baseline |
| G-IRR | L1 | 人工标注卡须有 IRR（≥2 人、κ≥0.6），当前 0 条 ⇒ 只 WARN |

- **测试**：`tests/test_gate_rules_669d.py` —— **29 passed**（每条规则 ≥1 正例 + ≥1 反例）。
- **一键门禁**：`python tools/run_669d_gate.py` → `overall=PASS  未登记BLOCK=0  已登记=4  WARN=13`。
- **known_gaps**：`data/669d_known_gaps.json` 登记 **19 条**（G-BOUNDARY-REQUIRED ×15、G-STATS-FROZEN ×3、G-BASELINE-EXISTS ×1），**每条含真实 reason，不静默**。

---

## 3. C 段 · 论文相关工作深化

- **C1**：`research/paper_draft_v0.5.md` §2 新增 3 个方向子节（**2.5 形式化验证+LLM / 2.6 LLM 代码错误分类 / 2.7 溯源审计**，各 3 篇 arXiv-API 核验文献），原 §2.5 定位顺延为 **§2.8**；参考文献追加 **37–45**（[API 核验]）。
- **C2**：`research/669d_引用核验.md` —— 15 条 `[待核]` 逐条核验：**9 条 CrossRef/arXiv 通过**，6 条需人工（8 EU 法规 / 21 Goodhart+Strathern / 26 Pineau / 28 Fisher / 31 Holm / 32 Krippendorff / 33 Shadish / 36 OTS）；其中 3 处 Crossref **误命中**已手工定位正确出处；**Huang 2303.17651↔2310.01798 错引未进入本稿**（仅在 `_arch_v4x` 旧稿）。
- **C3**：§8 五层（construct/internal/external/statistical/temporal）保留，新增 **§8.6 残余风险 ↔ 669d 门禁映射表**。

---

## 4. D 段 · 数据攒集

| 文件 | 内容 | 关键口径 |
|---|---|---|
| `data/holdout/holdout_extension_669d.json` | holdout **+10**（h31–h40） | planted=true 5 / false 2 / unknown 3；atom_ref **全部为真实存在**的 atom |
| `data/counterfactual_cases_669d.json` | 反事实 **+20**（cf21–cf40） | dependent 7 / independent 13；P/R/F1=1.0（**上界**，判据同源）；`measured_out` 置空待 669 基座现跑 |
| `data/external_corpus/external_corpus_669d.json` | 外部 corpus **+20**（d3e-01–20） | **刻意分散检测器**（sanitizer 8 / compiler-warn 5 / cross-compile 3 / perf 2 / compile-time 2）以对冲 WSL 单点依赖；须分层报告 |
| `research/669d_统计口径.md` | 统计口径**冻结** | CP 主报 / Wilson 敏感性 / Fisher / 精确 McNemar / BH / Holm；**现算+CI 必报**；含现有三数 95% CI 现算表 |

- **现有三数 CI（本次现算，Clopper–Pearson）**：87.5% → [61.7%, 98.4%]；35.0% → [20.6%, 51.7%]；F1=1.0 → P/R 各 [15.8%, 100%]。
- **样本量目标**：±10pp 需 n≈93–104（现 D2/D3 仅 16/40，只能点估计）。

---

## 5. E 段 · 收工验收

| 检查 | 结果 |
|---|---|
| 669d 一键门禁 | `overall=PASS  未登记BLOCK=0` |
| 669d 单测 | **29 passed**（`tests/test_gate_rules_669d.py`） |
| 658 门禁无回归 | `overall=PASS  L0 5/5  L1_fail=0`（S0–S6 全 PASS） |
| 受控目录 | `atoms/ evidence/ Examples/ Book/ data/authority/` **零差异** |
| 452 账本 | **零改**（仍 452 行） |
| 新增文件 | 全部带 `669d` 后缀；未改动 669 工程在改文件 |
| 提交 | `git commit -s`（DCO），**不 push** |

---

## 6. 诚实清单（残余风险 / 已知缺口，不静默）

1. **环境依赖**：external corpus 检出率强依赖 WSL sanitizer（A2）；D3 已分散检测器对冲，但仍须**分层报告**。
2. **判据同源**：反事实 F1=1.0 是**上界**（真值标签与判据 3 同源），不称"已校准"。
3. **样本量小**：D2/D3 为 16/40，均点估计；±10pp 需 n≈93–104。
4. **门禁射程缺口**：`caliber_check_669` 对明细无射程、前端零射程（A3 已登记）。
5. **门禁射程**：护栏只比"产物↔前端"，不重跑探测器 ⇒ 666 事故形态仍可重演（审计 P0-2，建议补登 known_gap）。
6. **未工具化**：`tools/stats_667.py` 未建成，统计口径暂靠人工（G-STATS-FROZEN ×3）。
7. **IRR 缺失**：第二标注者 0 人（G-IRR，L1 WARN）。
8. **OTS 占位**：时间锚为零 attestation 占位符，真锚定未做。
9. **基线/消融为空**：baseline 0、ablation 0 组 ⇒ 无法回答"比别的方法好在哪"（G-BASELINE-EXISTS ×1）。

---

## 7. 本批新增文件清单（669d）

**审计/报告**：`docs/669d_复现审计.md`、`docs/669d_corpus差异根因.md`、`docs/669d_门禁真实性.md`、`docs/669d_gate_report.md`、`research/669d_引用核验.md`、`research/669d_统计口径.md`、`data/669d_acceptance_report.md`
**门禁实现**：`tools/gate_rules_669d.py`、`tools/gate_tiers_669d.json`、`tools/run_669d_gate.py`、`tests/test_gate_rules_669d.py`、`data/669d_gate_status.json`、`data/669d_known_gaps.json`
**数据扩样**：`data/holdout/holdout_extension_669d.json`、`data/counterfactual_cases_669d.json`、`data/external_corpus/external_corpus_669d.json`

> 另：`research/paper_draft_v0.5.md` 的 §2/§8 修订为**工作树改动**（该文件属 669 工程在改范围，669d 不代为提交，留待 669 工程合并）。
