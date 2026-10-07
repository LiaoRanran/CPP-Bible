# TMLR 投稿准备清单（678 批次 · C3）

> 与 `data/677e_arxiv_投稿清单.md` 同源风格。TMLR 为**备选（backup）轨道**，以下为投前核对表。
> 状态图例：✅ 已就绪  ⬜ 待执行  ⚠️ 需注意

## 1. 材料（Materials）

- [x] **主稿 TMLR 版 tex**：`research/latex/tmlr/queyi_tmlr.tex`（待 `tmlr.sty` 就位后由 v1.1 生成，见 `ADAPTATION_NOTES.md` 机械步骤）
- [x] **复现清单**：`reproducibility_checklist.md` + `reproducibility_checklist.tex`
- [x] **数据可用性声明**：`data_availability_statement.tex`
- [x] **投稿陈述 / cover letter**：`tmlr_cover_letter.md`（双盲口径）
- [x] **版本一致性**：基于 version of record v1.3（677d），未改科学结论
- [⬜] **tmlr.sty / tmlr.bst**：从 TMLR 作者指南 / OpenReview 获取（第三方文件，**不纳入本仓**）
- [⬜] **匿名快照仓库**：剥离 `CPP-Bible` 仓库名、作者、机构、内部绝对路径后的 supplementary ZIP（≤100MB，匿名）

## 2. 双盲匿名（Double-blind Anonymity）

- [⬜] 主文 0 命中作者/机构/`CPP-Bible`/内部路径（`tools/anonymity_check_670c2.py` 当前 v1.1 有 2 处 `data/`/`research/` MAIN 命中待清）
- [⬜] 参考文献不泄露作者既往工作身份（保留 [Anonymous, 2026] 式或移除自引线索）
- [⬜] 投稿 PDF **不回链**具名 arXiv v1.3
- [⬜] 补充材料同样匿名

## 3. 政策符合（Policy Conformance）

- [x] 双盲评审（TMLR 强制）
- [x] 长度：正文 8 页（建议 9–12，符合"异常长会拖慢审稿"红线以下）
- [⬜] 用 TMLR LaTeX 样式生成 PDF（替换 NeurIPS 样式）
- [x] 鼓励性复现清单 + 代码/数据可用性声明已附
- [x] 不与已发表工作重叠（arXiv v1.3 为预印本，TMLR 允许；但投稿物本身须匿名且不指名）

## 4. 时间线（Timeline，建议）

| 阶段 | 动作 | 负责人 | 备注 |
|------|------|--------|------|
| T0 | 获取 `tmlr.sty`，生成 `queyi_tmlr.tex` | 工程批次 | 依赖第三方样式 |
| T0+1d | 匿名化复核 0 命中 + 本地 tectonic 编译通过 | 作者 | 见 §2 |
| T0+2d | 打包匿名 supplementary ZIP（≤100MB） | 作者 | 数据/代码快照 |
| T0+3d | OpenReview 建稿 + 填元数据表单 + 上传 | 作者 | 双盲，不链具名 arXiv |
| T0+3d | 建议 action editor / 回避审稿人 | 作者 | 不向审稿人披露 |
| 评审中 | 滚动审稿；按 TMLR "fast turnaround" 预期数周内首轮 | TMLR | 无具体月数承诺 |

## 5. 与 NeurIPS E&D 主线的关系

- E&D 为主线（2027 CFP 发布后投）；TMLR 为本批准备好的**备选**。
- 两者共享 v1.3 内容与复现包；差异仅在样式文件、复现清单段、投稿陈述口径。
- endorsement 请求（6 位学者）服务于 E&D；TMLR 走 OpenReview 自建稿，无需 endorsement。

## 6. 红线（与 678 批次一致）

- 不修改 `neurips_2025.sty` / 不修改检测器 / 不修改样本 / 不改动实验结论。
- 不 force push；DCO 签名（`git commit -s`，author=SOB 一致）。
