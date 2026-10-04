# 676j · arXiv 投稿准备清单（v1.1 → 预印本）

> **批次**：676j（投稿材料准备）｜ **日期**：2026-10-04
> **目标**：把论文最终版推到 arXiv 可投稿状态；**本批只写清单，不打包、不改论文**。
> **红线**：不碰 `research/latex/queyi_neurips2027_v1.1.tex`（676h 在改）、`research/paper_shturl.md`、`research/latex/queyi_refs.bib`、`research/latex/arxiv_submission/`。
> **前置**：论文 v1.1 正文 9 页（676e 终修）；676f（A5 全量）/ 676g（盲区地图）的数字**必须**先由 676h 落进正文，arXiv 才能打包。
> **姊妹文件**：`data/673i_arXiv投稿清单.md`（673i 旧版，本文件为其 676j 更新/超集）。

---

## 0. 现状快照（先看这个再动手）

| 文件 | 大小 / 时间 | 状态 |
|---|---|---|
| `research/latex/queyi_neurips2027_v1.1.tex` | 119 KB / **2026-10-04 08:44** | **正在被 676h 改**（含 A5/盲区地图新数字） |
| `research/latex/queyi_refs.bib` | 21 KB / 2026-10-04 08:43 | 676h 可能在补相关工作 |
| `research/latex/queyi_neurips2027_v1.1.pdf` | 246 KB / 2026-10-04 08:45 | 编译产物，**与 .tex 同步中** |
| `research/latex/arxiv_submission/` | tex 101 KB / **2026-10-03 18:56** | ⛔ **已过期**（676f/676g 之前），**禁止在本批打包** |
| `research/latex/queyi_arxiv_submission.tar.gz` | 48 KB / 2026-10-03 19:00 | ⛔ 同上，过期 |
| 本机 LaTeX 工具链 | — | **不可用**（673i 记录：`pdflatex` / `tectonic` 均缺）⇒ 编译验证须由用户/CI 执行 |

> **结论**：arXiv 打包的**唯一前置**是「676h 把论文最终版落盘」。在此之前，本清单只做**可操作的检查项**，不产出 tarball。

---

## 1. 论文最终版确认（Final-version gate）

| # | 检查项 | 判定方法（可执行） | 通过标准 |
|---:|---|---|---|
| 1.1 | 正文 **≤ 9 页**（编译后**实测**，不是换算） | `pdfinfo queyi_neurips2027_v1.1.pdf \| grep Pages`；再读 `.aux` 中正文末尾 `\label` 的页码 | 正文（不含 references/appendix）≤ 9 页 |
| 1.2 | **0 undefined 引用** | `grep -c "??" queyi_neurips2027_v1.1.log` → 0；`grep -i "undefined" queyi_neurips2027_v1.1.log` → 空 | 0 |
| 1.3 | **0 undefined citation** | `grep -c "Citation.*undefined" queyi_neurips2027_v1.1.log` → 0 | 0 |
| 1.4 | 所有图表完整且被引用 | `grep -c "never referenced" queyi_neurips2027_v1.1.log` → 0 | 0 孤儿浮动体 |
| 1.5 | **数字全部更新**：A5 全量（1137 样本 / Δ+24.03pp / p=2.3e-41 / 并列 0.0pp）、盲区地图（1147×8 / 38.4% / **18 of 70**）、FPR **0.0% (0/11)** | `grep -nE "55\.0|43\.8|n=20|n=16|840|93\.75|18\.2|15 of 70" research/latex/queyi_neurips2027_v1.1.tex` → **应为空** | 无旧数字 |
| 1.6 | 中英文稿一致 | 抽查 A5 段 / 盲区段 / 局限段：`.tex` ↔ `paper_shturl.md` 数字逐位一致 | 一致 |
| 1.7 | A5 段落按 `data/676f_论文更新位置清单.md` **整段改写**（A1–A14、B1–B8） | 逐条勾选该清单 | 全勾 |
| 1.8 | 盲区地图按 `data/676g_论文更新建议.md` 落位（T20 威胁 + 能力边界小节 + 未来工作） | 逐条勾选 | 全勾 |
| 1.9 | 样式文件 | `grep -n "neurips_2025\|neurips_2027" *.tex` | 2027 sty 未发布前用 2025，并在文件头注明 |

---

## 2. 匿名化检查（Anonymity）

| # | 检查项 | 判定方法 | 通过标准 |
|---:|---|---|---|
| 2.1 | 无作者名 / 单位 / 邮箱 | `grep -nEi "author|university|institute|@[a-z]+\.(com|edu|org)" research/latex/queyi_neurips2027_v1.1.tex` | 仅 `Anonymous Author(s)` |
| 2.2 | 无本地路径 | `grep -nE "C:\\\\\\\\|/home/|/Users/|\\\\\\\\Users\\\\\\\\" research/latex/*.tex` | 空 |
| 2.3 | 无 TODO / FIXME / 内部链接 | `grep -nEi "TODO|FIXME|XXX|见 data/|internal link" research/latex/queyi_neurips2027_v1.1.tex` | 仅保留**故意**的 `\TODO{670a}` 占位（红字） |
| 2.4 | 无指向非匿名仓库的 GitHub 链接 | `grep -nEi "github\.com" research/latex/*.tex research/latex/queyi_refs.bib` | 若有，改为匿名链接或删除 |
| 2.5 | `.bib` 无自引泄露 | 人工核对 `queyi_refs.bib` 无作者姓名 / 个人主页 | 唯一 URL = `https://opentimestamps.org`（公开协议站） |
| 2.6 | **cover_letter 不放入 arXiv 包** | 打包前 `tar tzf *.tar.gz \| grep -i cover` | 空 |
| 2.7 | 补充材料（若挂代码/数据）匿名可访问 | 检查链接是否需登录 / 含用户名 | 匿名可访问，或用匿名镜像 |
| 2.8 | 双盲冲突：review 期挂署名 arXiv 会破盲 | 策略确认（见 §7 FAQ） | 匿名预印本 或 review 后再挂 |

---

## 3. 文件清单（tarball 应含）

```
queyi_neurips2027_v1.1.tex      # 主文件（唯一入口；无 \input/\include 子文件）
queyi_refs.bib                  # 参考文献（BibTeX）
neurips_2025.sty                # 样式文件（2027 官方发布后替换）
```

- [x] **无外部图片文件**：Fig.1 / Fig.3 / Fig.4 全部内联 TikZ / pgfplots；原 `fig:data` 已改为正文叙述 ⇒ 无需 `figures/`、无需 `\graphicspath`。
- [x] 所有表格内联 `tabular` / `booktabs`。
- [ ] **附录文件**：附录 A–F 均在主 `.tex` 内（无独立附录文件）⇒ 确认 `grep -c "\\\\input\|\\\\include" *.tex` = 0。
- [ ] **不打包**：`*.aux/*.log/*.out/*.bbl/*.blg`（arXiv 自己生成；只上传 `.tex + .bib + .sty`）、`cover_letter.*`、`response_template.*`、`.pdf`（arXiv 可选上传 PDF，但以源码为准）。
- [ ] 若未来加入外部图（PNG/PDF），须一并打包并设 `\graphicspath`。

---

## 4. 编译验证（干净目录独立编译）

```bash
# 1) 建干净目录，只放 §3 三个文件
mkdir -p /tmp/arxiv_check && cp queyi_neurips2027_v1.1.tex queyi_refs.bib neurips_2025.sty /tmp/arxiv_check/
cd /tmp/arxiv_check

# 2) Option A — tectonic（自包含，内部跑 bib）
tectonic -X compile queyi_neurips2027_v1.1.tex --keep-logs --keep-intermediates

# 3) Option B — TeX Live / MiKTeX
pdflatex queyi_neurips2027_v1.1.tex && bibtex queyi_neurips2027_v1.1 \
  && pdflatex queyi_neurips2027_v1.1.tex && pdflatex queyi_neurips2027_v1.1.tex

# 4) 验收
pdfinfo queyi_neurips2027_v1.1.pdf | grep Pages        # 与主稿页数一致
grep -c "??" queyi_neurips2027_v1.1.log                # 0
grep -ci "undefined" queyi_neurips2027_v1.1.log        # 0
```

| # | 检查项 | 通过标准 |
|---:|---|---|
| 4.1 | 干净目录独立编译通过 | 0 error |
| 4.2 | 页数与主稿一致 | 与 `research/latex/` 下编译结果同页数 |
| 4.3 | 0 undefined / 0 `??` | 见上命令 |
| 4.4 | 无缺失字体 / 宏包 | `.log` 无 `Font ... not found` |
| 4.5 | 本机无工具链 | ⇒ **须由用户或 CI 执行**（673i 已登记） |

---

## 5. arXiv 特定要求

| # | 要求 | 阈值 / 说明 | 检查方法 |
|---:|---|---|---|
| 5.1 | 源码包大小 | 通常 **≤ 10 MB**（本包 ~48 KB，远低于） | `du -h queyi_arxiv_submission.tar.gz` |
| 5.2 | 不支持的宏包 | arXiv 用 TeX Live 全量；`tectonic` 亦覆盖 TikZ/pgfplots | 编译通过即支持（§4） |
| 5.3 | 图片格式 | **PDF 优先**，PNG/JPG 亦可；**本稿无外部图** | `find . -name "*.eps"` → 空（EPS 不推荐） |
| 5.4 | 编码 | **UTF-8** | `file -i *.tex` → `charset=utf-8` |
| 5.5 | 分类（category） | 主类 **cs.SE**，副类 **cs.PL**；可 cross-list cs.AI | 提交时选择（673i 已定） |
| 5.6 | 摘要字段 | 公开且永久；确认不含未公开数据 / 身份 | 人工复核 |
| 5.7 | comments 字段 | **仅**在 under review / accepted 时填；纯预印本勿谎称接收 | 人工复核 |
| 5.8 | 提交入口 | `https://arxiv.org/submit`（新账号可能需 endorser，见 §6） | — |

---

## 6. Endorser 准备

- **是否需要**：若账号在 **cs.SE** category **无自动提交权限**（新账号 / 该领域首次提交），需一位已在该 category 发过论文的 endorser 背书。**若既往在该 category 发过，可直接提交。**
- **候选来源**：导师、同事、领域内研究者（须在 cs.SE / cs.PL 发过 ≥1 篇）；arXiv "request endorsement" 链接亦可自动匹配。
- **注意**：endorser **不审内容**，只确认你确实做相关研究；建议**截稿前 1–2 周**确认，避免卡审。
- **话术模板**（可直接改）：

```
Subject: arXiv endorsement request — cs.SE

Dear Prof. / Dr. <NAME>,

I am preparing an arXiv preprint in cs.SE and would be grateful if you could endorse me
for that category. The paper is "Evolving Verifiers: Failure-Driven Evidence Acquisition
with Auditable Provenance" — an evaluation-methodology paper with a reproducible artifact
(C++ evidence-acquisition verifier; A5 budget-matched ablation over 1137 samples) and an
explicit capability-boundary analysis of the instrument.

arXiv will send you an endorsement request link after I list you. I understand endorsing
only confirms that the work is in your area and does not imply review or agreement.

Thank you for your time.
<YOUR NAME>
```

---

## 7. 时间节点

- **arXiv 无 deadline**，**现在就可以占坑**；占坑后**可随时更新版本**（`v2`、`v3`…），不影响后续期刊/会议投稿。
- **但**：占坑的**前置**是论文最终版（676h 落地）；**不要**用过期包（`arxiv_submission/` 是 10-03 的旧版）占坑。
- 建议节奏：
  1. 676h 论文最终版落盘 + §1 全绿 →
  2. §4 干净目录编译通过 →
  3. §2 匿名化全绿 →
  4. 打包 `queyi_arxiv_submission.tar.gz`（**重建**，不用旧包）→
  5. 确认 endorser（若需要）→
  6. 上传，获 arXiv ID（数小时–1 天）→
  7. **TMLR 投稿前**确保 arXiv 版本是最新的（TMLR 允许同时挂 arXiv）。

### FAQ（继承 673i §7，逐条复核）

- **Q：arXiv 有 9 页限制吗？** 没有。9 页是 **NeurIPS** 的；arXiv 页数宽松（单 PDF 建议 ≤ ~50 页）。
- **Q：必须匿名吗？** arXiv 预印本通常**署名**；匿名版仅双盲投稿系统需要。双盲 review 期挂**署名** arXiv 可能破盲 ⇒ 用匿名预印本或 review 后再挂。
- **Q：TikZ 图怎么办？** arXiv TeX Live 支持 TikZ / pgfplots；内联即可。
- **Q：编译失败常见原因？** `.sty` 缺失（务必打包）、bib 未编译、`hyperref` 冲突、字体缺失。
- **Q：双盲 + arXiv 冲突？** 见上；本稿当前为匿名版，与 D&B 单/双盲自选策略需一致（`research/cover_letter.md` §3 提醒）。

---

## 8. 本批不做 / 待办

| 项 | 状态 | 谁做 |
|---|---|---|
| 重建 `arxiv_submission/` 与 tarball | ⛔ **本批不做**（等论文最终版） | 下一批（676k?） |
| `neurips_2027.sty` 替换 | ⛔ 待官方发布（CFP 通常 5–6 月） | 用户 |
| 本机 LaTeX 编译验证 | ⛔ 本机无工具链 | 用户 / CI |
| 论文最终版（含 A5/盲区数字） | 🔄 676h 进行中 | 676h |
| 匿名化 grep | ✅ 本机可做（本批已在 §2 给出命令） | 676j / 用户 |
| **发现项**：`research/latex/cover_letter.tex` 的 "Honest limitations" 段写 **"15 of 70 defect types exceed 50% blind"**，应为 **18 of 70** | ⚠️ 本批不改（不在允许文件清单内） | 提请 676h / 用户修正 |
