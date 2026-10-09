# 702 · 预提交清单（Pre-Submission Checklist）

> 投稿前最后一遍核对。**每一项打勾（✅）前必须实际验证**，不要凭记忆。
> 配套：`702_submission_checklist.md`、`702_cover_letter_check.md`、`702_rebuttal_index.md`。

---

## A. 匿名化是否干净（double-blind）

- [ ] 论文正文、补充材料、cover letter 中**无作者真名 / 机构 / 邮箱 / GitHub 用户名**
      （当前署名 "The Authors"、GitHub 用户名 `LiaoRanran` 仅在仓库 URL，**不得**进投稿包）
- [ ] 致谢中若提人类标注者，使用其**选择的形式**（实名/化名/匿名），不含作者可反推线索
- [ ] 数据中无可反推样本来源/批次的泄露（标注包已去标识化；`leak_suspected=yes` 的 13 条已声明）
- [ ] 匿名 PDF 由 TeX 编译产出（非含元数据的 Word/PDF）

## B. 数字是否一致

- [ ] 论文正文 ↔ cover letter ↔ README 的核心数字一致：
      1147×8、38.4% 盲区、13/34 类 >50%、asan 61.65%、60.07%→24.74%、+24.03pp、110 CVE @ 59.09%
- [ ] `tools/verify_paper_numbers.py` 复算 **0 missing / 0 policy_violation**（当前 130 条口径）
- [ ] 冻结矩阵分母统一为 **catch 640 / miss 507**（非陈旧的 676l 口径 catch 674）
- [ ] 所有百分比标注分母（如 200/426、200/340）逐项可复算

## C. TODO 是否清零

- [ ] 论文 TeX 中**无残留 `{{TODO_*` / `TODO` / `FIXME` / `XXX`** 占位符
- [ ] 数据卡 / 补充材料中无 `{{TODO_ablation_A0..A4}}` 类占位（见 676l 报告已知坑）
- [ ] 所有 `⬜ 未闭合` 项已显式标注，未伪装成"已确认/安全"

## D. 引用是否完整

- [ ] 题名统一为 *"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"*
      ——**全仓搜索 "Evolving Verifiers" 旧题名并清除**（已知残留：根 `README.md` §6 BibTeX、
      `CITATION.cff`、`docker/paper/Dockerfile`、`preview_package*/`、`research/latex/archive/` 等）
- [ ] 贡献数措辞统一：**Four contributions**（非旧版 "Three contributions"）——全仓搜索并修正
- [ ] 参考文献条目与正文 `\cite` 一一对应，无悬空引用
- [ ] BibTeX 中邻居工作（DeepFact / Who Grades the Grader / Sengupta / SV-COMP 2026）齐备且年份正确

## E. 编译是否通过

- [ ] 论文 TeX `tectonic` / `pdflatex` 编译**无错无警告**（或仅已知无害警告）
- [ ] cover letter 同环境编译通过（v1.7，461 词 ≤500）
- [ ] 匿名 PDF 与源 TeX 内容一致（无缓存旧版）
- [ ] 复现脚本 `python tools/verify_paper_numbers.py` 与 `gen_693_manifest.py --check` 全绿

---

## F. 声明类（来自 `702_submission_checklist.md` 的待做项）

- [ ] **数据可用性声明**：一句话说明数据集 + 代码获取方式（Apache-2.0 + GitHub）
- [ ] **伦理声明**：人类标注者自愿/知情同意/匿名选项/无报酬（NeurIPS E&D 要求）
- [ ] **利益冲突声明**：独立无基金，一句话
- [ ] **附录页数**：正文 8 + 附录 23 ≤ 26（据 692 同步项 7）

---

## 验证命令速查（现算）

```bash
# 数字复算
python tools/verify_paper_numbers.py
# 冻结产物完整性
python tools/gen_693_manifest.py --check
# 旧题名残留扫描（投稿前必做）
grep -rl "Evolving Verifiers" --include=*.md --include=*.tex --include=*.bib .
# TODO 残留扫描
grep -rn "{{TODO_\|TODO\|FIXME" research/latex/queyi_neurips2027_v1.1.tex
```

> 本清单为**检查模板**。打勾 ≠ 自动通过；每项需实际跑命令或读文件确认。
