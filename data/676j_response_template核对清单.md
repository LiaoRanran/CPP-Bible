# 676j · `response_template.md` 逐条核对清单

- **批次**：676j（投稿材料准备）｜ **日期**：2026-10-04 ｜ **对象**：`research/response_template.md`
- **数字基线**：`data/current_numbers.json`（672h）、`data/a5_676f_results.json`（A5 全量）、`data/blindspot_676g_stats.json`（盲区地图）
- **纪律**：只改 `response_template.md`（本批允许的三个 research/ 文件之一）；**不碰论文正文 / 中文稿 / 参考文献 / arXiv 包**。

---

## 1. 关键词扫描（规格任务 C 步骤 2）——逐组结果

| 关键词组 | 命中位置 | 判定 | 处置 |
|---|---|---|---|
| `A5` / `ablation` | L5, L12, L14, L25, L49, L50, L53, L61, L69, L77, L80, L95, L102, L103, L119, L143 | **全部为「已跑」语境** | L25/L53/L61/L69/L77/L80/L103 **重写**为全量结果；L102 标题保持 |
| `not yet run` / `unrun` / `BLOCKED` / `has not been rerun` / `registered as open` | **0 处**（修复前：L23 有 "registered as open"、L51 有 "has not been rerun"） | ✅ 已清零 | L23→L25、L51→L53 重写 |
| `is blocked` | L52（**审稿人原话引用**：`"The paper says the random baseline is blocked…"`） | 保留（引用不可改） | 不改；对应回复 L53 已说明 blocker **已解决** |
| `FPR` / `false positive` / `18.2%` / `2/11` | L11（现为 **0.0% (0/11)**）、L125（**4/8 false positives** = LLM 臂，另一件事） | ✅ 无 18.2% / 2/11 | L11 改写：删掉 "18.2% (2/11)" 字面，改为「早期草案曾报 2 例对照假阳性」 |
| `82.9%` / `62.5%` / `34/41` / `40/64` | L11, L26, L27, L33 | 与 672h 权威源一致（**未被 676f/676g 污染**） | 保留 |
| `n=20` / `n=16` / `n=105` | **0 处**（修复前：L23/L51/L67 有 `n=21/48`） | ✅ 已清零 | 删除 |
| `n≥138` / `n=138` | L61, L77, L80, L103, L119（均改为「**已达标**」语境） | ✅ | L59/L61/L75/L77/L78/L80/L111–120 重写 |
| `1137` / `1147` / `9096` / `n=566` | L5, L12, L13, L25, L53, L61, L69, L77, L80, L103, L120 | ✅ 新增，口径正确（1147 数据集 / 1137 A5） | — |
| `97.3%` / `mutation` / `96.5%` | L32, L33（**96.5%** + 注明 676i 修复中） | ⚠️ 676i **未完成**（本批核对时仓库无 `data/676i_*`、无 676i 提交） | **保持 96.5%**，并加注「修复中（676i: 96.5%→97.3%）」 |
| `wunsequenced` / `恒 catch` | L11, L103 | ✅ 仅作为「已修复缺陷」的说明出现 | 保留 |

---

## 2. 逐条数字核对（与权威产物对照）

| # | 位置 | 文件中的数字 | 权威源 | 一致性 |
|---:|---|---|---|---|
| 1 | L11 | holdout 82.9% (34/41) | `current_numbers.json::holdout` | ✅ |
| 2 | L11 | corpus 62.5% (40/64) | `current_numbers.json::corpus` | ✅ |
| 3 | L11 | 对照 FPR 0.0% (0/11) | `current_numbers.json::control_false_positive` | ✅ |
| 4 | L12/L25/L53/L103 | A5：1137 样本 / 派生 571 / 评估 566 / 9096 次 detect | `a5_676f_results.json::sample_stats` + 报告 §2.1 | ✅ |
| 5 | L12/L25/L103 | FD 54.6% (309/566) / Random 30.6% (173/566) / Static 24.7% (140/566) | `a5_676f_results.json::primary_main_8candidates.by_k[k=4]` | ✅ |
| 6 | L12/L25/L103 | Δ(FD−Random) +24.0pp，p=2.3×10⁻⁴¹，b=136/c=0 | `paired_tests.fd_vs_random` | ✅（精确值 24.0283pp / 2.296e-41） |
| 7 | L12/L25/L103 | Δ(FD−Static) +29.9pp，p=1.9×10⁻³¹ | `paired_tests.fd_vs_static` | ✅（精确值 29.8587pp / 1.892e-31） |
| 8 | L103 | 并列分析 Δ=0.0pp（p=1.0）；Static 增至 +30.6pp（p=8.1×10⁻³⁴） | `co_primary_excl_degenerate` | ✅（精确值 0.0 / 30.5654pp / 8.05e-34） |
| 9 | L103 | 并列 k=1–3：+11.31/+7.42/+7.42pp | `co_primary_excl_degenerate.by_k` | ✅ |
| 10 | L103 | 2000 次里 FD 更优 97.6% | 报告 §3.1 | ✅ |
| 11 | L13/L103 | 盲区 38.4% / 检出 61.6% / 18 of 70 / 家族 memory 15.2%→link/ODR 67.7% | `blindspot_676g_stats.json` | ✅（**修复前误写 15/70**） |
| 12 | L103 | ~5% 跑间翻转 | 报告 §2.5（369 格 → 18 翻） | ✅ |
| 13 | L26/L27 | FD 82.9%/62.5% vs Static 2.4%/17.2% vs Random 9.8%/21.9% | `current_numbers.json::baseline_arms` | ✅ |
| 14 | L33 | mutation core 96.5% (110/114) / all-scope 81.8% (130/159) | `current_numbers.json::mutation_core` | ✅（676i 修复中，保持） |

---

## 3. 修复清单（before → after）

| # | 位置 | before（过时） | after（本批） |
|---:|---|---|---|
| 1 | L5 数字基线 | 仅 `current_numbers.json`（672h） | + `a5_676f_results.json`、`blindspot_676g_stats.json` |
| 2 | L11 | 「旧值 18.2% (2/11)」 | 「**0.0% (0/11)**；一个早期草案曾报 2 例对照假阳性，系 `wunsequenced` 恒 catch 缺陷所致，673u 已修复」 |
| 3 | L12 | 「真 B3 仅在 672g 旧分母 21/48 上跑过」 | 「**A5 已在全量池上跑完**（1137/571/566，k=4，Δ+24.0pp，p=2.3×10⁻⁴¹；并列 k=4 归零 ⇒ direction-only）」 |
| 4 | L13 | （无） | 新增「检测器能力边界地图（1147×8，61.6%/38.4%/18 of 70）+ ~5% 跑间不稳定」 |
| 5 | L14 | 「真 B3 仅在 672g…」 | 「A5 的全量预算匹配对照已补上；Static 臂仍为口径重分箱」 |
| 6 | L23（R1.1） | 「true B3 … its rerun on the expanded samples is registered as open」 | 「**A5 has now run at full scale** … direction-only（并列 Δ=0.0pp）」 |
| 7 | L51（R2.3） | 「the true B3 … **has not been rerun** … register the rerun as future work」 | 「blocker **resolved**：A5 已跑（Δ+24.0pp）；理由由「臂缺失」改为「池构成」」 |
| 8 | L59（R3.1） | 「Sample expansion to **n≥138** … is the first item of future work」 | 「A5 功效缺口**已关闭**（n=566≫138）；余留 = 非退化池 1<k<|A|−1」 |
| 9 | L67（R3.3） | 「the true B3 ran once at 672g on the older n=21/48」 | 「true B3 现也以 A5 全量跑（1137 样本）；dagger 标记的是**头条臂仍是代理**，不是「臂缺失」」 |
| 10 | L75/L77（sample size 模板） | 「Expansion to n≥138 is the first future-work item」 | 「A5 扩展**已发生**（n=566≫138）；余留 = 池几何」 |
| 11 | L78/L80（baseline 模板） | 「the true B3 ran only at 672g on the older denominator … B3 rerun as **open items**」 | 「A5 已跑，该项**不再 open**；仅 `detect_static` 仍 open」 |
| 12 | L101→L103（On A5） | 已由前序同步改为全量，但含 **15 of 70** 笔误 | 修正为 **18 of 70**；补「并列 k=1–3 钉住选择效应 ≈+7–11pp」「~5% 跑间不稳定」 |
| 13 | L111（高频 Q1 标题） | 「5 条，672h 版」 | 「5 条，**676f 版**」；正文补「A5 已扩展 n=566」 |
| 14 | L33（R1.2） | mutation core 96.5%（无备注） | 保持 **96.5%**，加注「**676i 修复中：96.5%→97.3%**，落地前以 96.5% 为准」 |

---

## 4. 验收对照（规格任务 C 验收）

| # | 验收标准 | 结果 |
|---:|---|---|
| 1 | 无 "A5 not yet run" / "unrun" / "BLOCKED"（指 A5 的） | ✅ 0 处（仅保留审稿人原话引用 "is blocked"） |
| 2 | A5 数字为 676f 全量结果 | ✅ L12/L25/L53/L61/L77/L80/L103 全部对齐 |
| 3 | FPR 为 0.0% (0/11) | ✅ L11 |
| 4 | 无 18.2% / 2/11 旧 FPR | ✅ 字面已清除（L11 改为「早期草案曾报 2 例」） |
| 5 | mutation 保持 96.5% 并注明「修复中」 | ✅ L33（676i 未完成） |
| 6 | 核对清单完整 | ✅ 本文件 |

---

## 5. 遗留问题（等 676h / 676i 落地后需同步）

1. **mutation 96.5% → 97.3%**：676i 完成后，本文件 L33 须改为 97.3%（含新分母），并复核 `current_numbers.json::mutation_core`。
2. **A5 论文口径**：`response_template.md` 的 §E4 引用与论文正文需与 676h 改写后的 A5 段落**逐字一致**（本批已给出一致口径，但论文侧由 676h 落地）。
3. **`research/latex/cover_letter.tex`**（LaTeX 孪生版，**不在本批 git add 清单**）：其"Honest limitations"段仍含 **"15 of 70 defect types exceed 50% blind"**，应为 **18 of 70**。属**发现项**，本批不改（不在允许文件清单内），提请 676h/用户修正。
4. **`detect_static` 缺位**：仍为 open item，回复口径未变。
