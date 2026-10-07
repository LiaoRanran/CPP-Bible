# 687 · 统一合并批次修改方案（683-686 并入论文）

- **批次**：687（统一合并：683-686 结果并入 + 硬伤修复 + Framing 重构 + 定稿）
- **对象**：`research/latex/queyi_neurips2027_v1.1.tex`（683 已改过附录；本批在其上修改）
- **前置实测（本批编译基线）**：正文结束于第 8 页（`page:endmain=9`，第 9 页起为参考文献）；
  **全稿 35 页（已到上限）**；摘要 246 词。
- **红线遵守**：不改 `tools/holdout_reveal_661.py`；不改 `data/holdout_expansion/**/*.cpp`；
  不改核心数字（A5 Δ=+24.03pp、盲区 38.4% 等，只补充新数字）；不 force push；全部 `git commit -s`；
  只 add 本批文件；论文正文 ≤9 页；修改前 `git diff` 已确认（工作区无未提交 tex 改动，HEAD=266d6cdf）；
  匿名版保持 `Anonymous Author(s)`；所有数字可追溯。

---

## 0. 冲突检测与裁定（A2）

| # | 冲突点 | 684 建议 | 685 建议 | 现状（683 后） | 687 裁定 | 理由 |
|---|---|---|---|---|---|---|
| X1 | **Abstract 空间** | 形式化前置 + 把 +24pp 降级为"+7-12pp 机制效应" | 末尾追加"+2.3pp 天花板 + 5% 噪声稳定"句 | 246 词，上限 250 | **采纳 684 主改**（重写领起句式 + 并排数字 + 子模最优 + 110 真实缺陷）；**拒绝 685 摘要追加句** | 仅余 4 词余量，685 句需 ~18 词；685 内容改投附录 B.2/B.3 与结论，不损失信息 |
| X2 | **贡献列表** | 新增第 (4) 条（子模形式化） | 第 (4) 条末尾补"+2.3pp 天花板 + 鲁棒界" | 3 条（定义/标定/审计） | **重构为 4 条**（治理框架 / 子模形式化＋天花板与鲁棒一句 / 大规模实证 / 能力边界地图）；685 定量并入贡献 2 括号 | 4 条对应 687 任务 B2 结构；避免 5+ 条稀释 |
| X3 | **Method 子模段落** | 提供可粘贴段落（L1052 后） | 其后加"Adaptive ceiling + Robustness"段 | 无子模段 | **采纳 684 段落（压缩版）** + 685 内容压成末尾一句（指向附录） | 正文零余量，685 的 1 段压为 1 句 |
| X4 | **附录编号** | 称"B.1 子模" | 称"B.2 天花板 / B.3 鲁棒" | 附录为 `\section` 自动字母编号；683 已落 3 节 | **不硬编码 B.x**：按顺序新增 6 个 `\section`；任务卡 B.1-B.7 的映射见 §3 表 | LaTeX 自动编号，硬编码会与 683 节冲突 |
| X5 | **真实靶场落点** | （未涉及） | （未涉及） | 683 附录三节已落地 | 正文补 **1 句**（110 样本 / 59.09% / p=0.60 指向附录）；**不重复**建节 | 正文零余量；683 附录已完整 |
| X6 | **盲区类型数** | — | — | 正文 13/34（正确）；686 元评估引 18/70（归一化前旧值）；docs 徽章 18/34 | **以 `data/681_type_stats_normalized.json` 权威值 13/34 为准**；686 的 18/70 在并入附录时改写为 13/34；docs 徽章不属本批（登记遗留） | 681 已把 70/18 归一化为 34/13；两个旧值不得进入论文 |
| X7 | **κ 口径** | — | — | 摘要/结论已标 AI；683 附录 `\kappa=0.73` 未标 AI；676m 表 κ=0.77 (n=131) | **所有 κ 出现处标注 AI self-consistency（非人类 IAA）**；683 附录补 "(AI second pass; not human IAA)"；Limitations 强调人类 IAA=0 | 686 #8；防"标签已验证"误读 |
| X8 | **1137/1147** | — | — | 无脚注 | E4（1137 首现）加**脚注**：1137=去重后 A5 矩阵；676g 能力边界全集 1147（含 64 corpus-null + 74 source-derived）；同一总体两种口径 | 686 #1；脚注最小成本 |
| X9 | **E9 对比** | — | — | 正文已写 "StrictA, chosen after results, hence exploratory" | 保留正文；**核验并同步** `app:clangtidy` 的 exploratory 标注；移入附录结论句微调 | 686 #13；正文已合规 |
| X10 | **页数（硬约束）** | — | — | 正文 8 页满 + 全稿 35 页满 | **净零/负编辑**：正文新增 ≈ 等量删除；附录新增 ~75 行 → 压缩既有附录 ≥85 行（见 §4） | 红线 7 + 任务 C3"重复内容合并" |

### 0.1 显式裁定记录

1. **X1 摘要**：684 的"smarter ranking"降级与 687 的"治理框架"定位同向，合并执行；685 摘要句不执行（空间），但其数字
   （+2.29pp、Jaccard 0.96、≤0.11pp）仍进附录与结论。**理由**：摘要字数红线优先，信息零损失（附录+结论承接）。
2. **X2 贡献**：684"新增 (4)"与 687"4 条重构"冲突——以 687 四条结构为准，把 684 的子模形式化并入贡献 2，并把
   685 的定量压进贡献 2 的括号句。**理由**：避免同一条贡献被两个批次分别增补造成列表膨胀。
3. **X6 盲区**：686 元评估表中的"18/70"是 681 归一化前的旧口径，**不得进论文**；统一用 13/34。
4. **X7 κ**：论文中的 κ 有两组数字——676m 表的 κ=0.77 (n=131, defect_type) 与 682 的 κ=0.73 (n=287)。
   它们不是同一量，**不得合并/相减**；两处都必须标"AI second annotator"。这是"数字口径"纪律的延续。

---

## 1. 修改清单总表（按论文章节排序，A3 优先级）

| 优先级 | 位置 | 修改 | 来源批次 | 净行数（估） |
|---|---|---|---|---|
| P0 | Abstract L93-98 | 形式化前置 + +24pp/+7-12pp 并排 + 子模最优 + 110 真实缺陷 + 治理框架定位 | 684/683/686#4 | ~0（重写，≤250 词） |
| P0 | Intro 贡献列表 L145-167 | 重构 4 条；"evolution=治理迭代"明确；不 claim 算子更优 | 684/685/686#2 | +1 |
| P0 | Intro "What we do not claim" L169-171 | 补一句：不 claim "演化算子召回更优"（3/14 档、p=0.302） | 686#2 | +1（需从别处省） |
| P1 | Method L1052 后 | 新增 `\paragraph{Selection as submodular maximization}`（压缩 684 段） | 684 | +8 |
| P1 | Method L1042-1044 后 | 补 1 句：operator 数学上=子模贪心，故不称新算法 | 684 | +1 |
| P1 | Experiments E4 L517-533 | 脚注 1137/1147；补 682 敏感性 1 句（4 split 全显著 + 97.3 百分位） | 686#1/682 | +3（含脚注） |
| P1 | Experiments（E9 后） | 新增 1 句真实靶场（110 / 59.09% / p=0.60，→附录） | 683 | +2 |
| P1 | Related Work | 新增 (6) 子模 + 主动测试 + 治理/Goodhart 短段；引用 10-15 新文献 | 684/685 | +6 |
| P1 | Threats L587-607 | 补 686 反事实 1 句 + κ/AI 澄清 + 条件复现 1 句 | 686/685 | +3 |
| P1 | Conclusion L653-668 | 补：子模最优 + 真实靶场 + "演化即期增益不显著、价值在治理" 1-2 句 | 684/683/686 | +3 |
| P2 | Analysis L562-577 | 微调（与 686 反事实衔接） | 686 | ~0 |
| P2 | 正文各处 | 净压缩 ~25-30 行（见 §4.1） | — | −28 |
| P1 | 附录新增 6 节 | 子模 / 天花板 / 鲁棒 / 反事实 / 元评估 / 真实失败案例 | 684/685/686/683 | +70 |
| P1 | 附录压缩 | 见 §4.2（humanize/repro/a5full 等） | — | −85 |

---

## 2. 各节修改明细（可直接执行版）

### 2.1 Abstract（≤250 词）
- 领起改：「Asset selection is formalized as monotone submodular maximization; our greedy carries the
  $(1-1/e)$ guarantee and attains the optimum on our instance.」
- 并排：保持 «FD 54.6% vs Random 30.6% (+24.0pp full pool, p=2.3e-41) … k≤3 keeps +7.4-+11.3pp»，
  并在其后补 «(the full-pool figure is dominated by degenerate-asset avoidance)» 语义已存在，不重复加。
- 新增 2 句（~22 词）：真实靶场 «110 real CVE-derived defects reconstruct a 59.09% OR detection, statistically
  indistinguishable from the synthetic corpus (p=0.60)» + 子模 «greedy attains the optimum».
- 压缩来源：口径句（29 词 → ~18 词）、Limitations 句（30 词 → ~24 词）、Queyi 资产句（24 词 → ~20 词）。

### 2.2 Contributions（4 条）
1. **An auditable evolution-governance framework**（四态判定 + Merkle 链 + 失败驱动迭代 + 三可检查性质）——
   强调 evolution = 治理框架的迭代演化（非算子性能）。
2. **Asset selection as submodular maximization**（684）：$f(S)=|\bigcup C_a|$ 单调子模（全枚举 0 违反）、
   FD 贪心 ≡ 标准贪心、$(1-1/e)$ 保证、本例达最优（比值 1.0）；附 685：自适应天花板 +2.3pp、5% 噪声 ≤0.11pp。
3. **Large-scale empirical study**（1147 + 110 真实缺陷、clone-aware split、4-split/k/seed 敏感性、跨工具链 κ≥0.84）。
4. **A capability-boundary map**（38.4% 盲区、13/34 类型 >50%）。

### 2.3 Method 子模段（814 字压至 ~450）
采用 684 §3 段落，删去已在他处的细节，保留：定义、全枚举 17,496 组 0 违反、greedy≡标准贪心 ≡ Nemhauser、
本例 greedy=最优、闭式 Random 期望（$k{=}4$ ⇒ 42.1%）、退化资产 $\Delta\approx c\,kd/n$、685 一句
（adaptive ceiling +2.29pp；ε=5% Jaccard 0.96、干净掉点 0.11pp；→附录）。
**63.2% 是比值地板不是覆盖率目标** 一句保留（正本清源）。

### 2.4 Experiments
- E4 段加脚注（\footnote）："1137 = A5 matrix after de-duplication (10 content duplicates dropped);
  676g capability-boundary uses the pre-dedup superset 1147 (1009 planted + 74 source-derived + 64 corpus-null).
  Same population, two counting calibers, not a contradiction."
- E4 段末补 682 句：「Four additional split variants give Δ=+23.0–+26.7pp (all p<1e-28); across 5000 random
  re-draws FD sits at the 97.3rd percentile (median gain +13.25pp).」
- 新 \paragraph{Real-world validation (683).} 1-2 句（110 / 59.09% / vs synthetic p=0.60 / 27 solo catches → 附录）。

### 2.5 Related Work 新增段（正文）
`\paragraph{(6) Submodular maximization, active testing, measurement governance (added in 687).}`
三句 + 引用：Nemhauser 1978（(1-1/e)）；Krause & Golovin 2014（曲率）；Golovin & Krause 2010/2011（active/adaptive）；
Feige 1998（不可近似性）；治理：Raji 2021 / Shankar 2025（leaderboard illusion）/ Skalse 2022（reward hacking，已引）。
**附录** app:related 七方向表补第 8 行（子模与主动测试）。

### 2.6 Threats / Limitations 补充
- 反事实：「Four counterfactual perturbations (sample size≥100 / asset removal / ≤15% label flips / ≤15-20%
  detector noise) leave the direction of the FD-vs-Random contrast unchanged (Appendix B.4).」
- κ：「κ=0.73/0.77 are AI self-consistency only; human IAA remains 0, the largest validity threat (T17).」
- 条件复现：保留 35%→10%；补 fail-loud 已落地措辞（已在 Analysis，写入 Threats 表定稿核验）。

### 2.7 Conclusion 调整
- 「we establish an auditable evolution-governance framework, prove the greedy choice's optimality on our
  instance, and empirically delimit the capability boundary over 1147 synthetic + 110 real defects.」
- 演化算子诚实句：「the operator's immediate recall gain is not significant (3/14 tiers, best +1.41pp,
  p=0.302); its contribution is falsifiability and governance, not a recall improvement.」
- Future work：人类 IAA、真实项目扩展、自适应策略（低天花板下探索）、跨语言。

---

## 3. 附录新增 6 节 ↔ 任务卡 B.1-B.7 映射

| 任务卡 | 本批 `\section` 标题（自动字母编号） | 来源 | 状态 |
|---|---|---|---|
| B.1 | Submodular Formulation and Approximation Guarantees (684) | 684_submodular_formulation + approximation_guarantee + degenerate_assets | 新增 |
| B.2 | Adaptive Selection Ceiling (685) | 685_direction1_theory/report | 新增 |
| B.3 | Robustness to Detector Noise (685/686) | 685_direction2 + 686_noise_report（扩展到 ε=0.5） | 新增 |
| B.4 | Counterfactual Robustness (686) | 686_sample_size/asset_set/label_quality/noise + counterfactual_summary | 新增 |
| B.5 | Meta-Evaluation Framework (686) | 686_meta_evaluation_framework（校准/区分/稳定/公平/效率） | 新增 |
| B.6 | Operator Ablation (All 16 Configurations) (683) | 683 已落地 | **已存在，不重复** |
| B.7 | Full Real-World Failure Cases (683) | 683_real_world_failure_cases（40 条摘要，压缩并入 app:realworld683） | 新增（并入） |

---

## 4. 页数策略（红线 7 + C3）

### 4.1 正文净压缩点（≥28 行）
1. L414-420 "How to read our intervals"（7 行→4 行，−3）
2. L562-577 Analysis 五点（16 行→12 行，−4）
3. L587-607 Threats 两段（16 行→13 行，−3）
4. L626-632 Claim Boundary（7 行→5 行，−2）
5. L646-668 Conclusion 一/二段（16 行→14 行，−2）
6. L670-679 "What this changes"（10 行→8 行，−2）
7. L105-117 / L128-136 Intro 两段（−2）
8. L203-211 Related (5)（9 行→7 行，−2）
9. L325-330 / L339-341 / L375-384 Method（−3）
10. L392-406 Protocol（15 行→13 行，−2）
11. E1-E9 各微压（−4）
12. Abstract 词内压缩（0 行影响）
合计 ≈ −29 行（对新增 ≈ +29 行：贡献+2、子模段+9、实验+5、RW+6、Threats+3、Conclusion+3、脚注+1.5）

### 4.2 附录净压缩点（≥85 行）
1. app:humanize "E4 673p-era superseded"（L1302-1324，23 行→8 行，−15）
2. app:humanize 其他冗余（engineering incidents/failure cases 去重，−10）
3. app:repro（L1158-1207，−8）
4. app:a5full（L1480-1680，重复句压缩，−15）
5. app:threats_quantified（L1681-1720，与正文重复，−8）
6. app:blindspot（L1722-1766，−6）
7. app:datasheet + app:metadata（L1934-2006，−10）
8. app:stats（L1060-1124）与 tab 密度微调（−8）
9. 其他杂项（−5）
合计 ≈ −85 行；附录新增 ≈ +70 行 → 净 −15 行，缓冲页数波动。

### 4.3 压缩纪律
- 所有压缩**只删文字/合句**，不改数字、不改表格数值、不删任何 `\label`；
- 被压缩段若含核心口径（instrument-boundary/caliber/unknown≠miss），**优先保留口径句**；
- 压缩后必须 `grep` 检查 label/ref 完好。

---

## 5. 硬伤修复专项（E 任务，落点表）

| # | 硬伤 | 落点 | 具体动作 |
|---|---|---|---|
| E1 | 1137/1147 | E4 段脚注 + blindspot 段脚注 | 各加 1 条 `\footnote`（同上文文本） |
| E2 | "Evolving Verifiers" 题名 | 贡献 1 + "What we do not claim" | 明确 evolution=治理迭代；不 claim 算子更优 |
| E3 | κ=0.727 误读 | 摘要/结论/683 附录/676m 表 | 统一 "(AI self-consistency; not human IAA)"；Limitations 强调 IAA=0 |
| E4 | E9 不公平 | 正文 E9 + app:clangtidy | 核验 exploratory 标注齐备；必要时补 1 句 |
| E5 | 条件复现 | Threats + README | Threats 保留 35%→10% + fail-loud；README 明确 WSL 硬依赖 |

---

## 6. 投稿材料同步（D 任务）
- **D1 cover_letter.md/.tex**：贡献段 5 条 → 更新为「治理框架 / 子模形式化 / 大规模实证（含 110 真实）/ 边界地图 / 开源」；
  补真实靶场段；叙述体 ≤500 词。
- **D2 rebuttal_prep_v2.md**：并入 686 arsenal 25 问（新增 Q12/15/20/3/9 强化）+ 683 真实靶场回应。
- **D3 response_template.md/.tex**：清理 18/70 → 13/34、更新 A5/新数字；同步子模/真实靶场回应。
- **D4 arXiv 实名版**：整文件同步匿名版内容（保持实名作者块），重新打包 `queyi_arxiv_v1.4.tar.gz`。

## 7. 验证（F 任务）
1. tectonic 编译：0 错、0 undefined；正文 ≤9 页、全稿 ≤35 页、摘要 ≤250 词。
2. `verify_paper_numbers` 数字对照 + `data/687_数字一致性检查表.md`。
3. 匿名化：匿名版 0 身份泄漏（姓名/单位/邮箱/GitHub）；实名版作者块正确。
4. 引用完整性：`\ref`↔`\label`、`\cite`↔bib 全匹配。
5. 门禁：`paper_quality_gate` 6/6、`data_integrity`、`fast_gate`。

## 8. 提交（G 任务，4 个 DCO 提交）
1. 论文正文修改（B）→ 2. 附录修改（C）→ 3. 投稿材料（D）→ 4. 硬伤修复+验证+验收报告（E/F/G）。
