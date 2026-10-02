# 673i · arXiv 投稿清单（NeurIPS 2027 E&D → arXiv 预印本）

> **批次**：673i 论文投稿准备 ｜ **目标**：把 v1.1 推到 arXiv 可投稿状态
> **范围**：匿名化、自引检查、tarball 结构、图片可编译性、投稿步骤、endorser 查找、FAQ
> **红线**：本清单只写 `data/673i_*`；不修改任何既有实验数据 / 工具 / 测试。

---

## 0. 前置结论（先说结果）

- 英文稿 `research/latex/queyi_neurips2027_v1.1.tex` 已修复：**9 个浮动体全部被正文引用（0 孤儿）**；`\ref{fig:data}` 的未定义引用已修复（改为正文叙述，无独立图）。脚本核验：`floats never referenced = 0`、`undefined fig/tab refs = 0`。
- 新增内容（均在正文，附录不限页）：**§6.9 / E9 外部工具对比（clang-tidy / cppcheck）**；**§7 标签效度复核流程设计（仅设计不复核）**；**§10 未来工作把 A5 列为最高优先级**。附录新增 `app:clangtidy`（完整表 + 8 条反向对 + 三 caveat）。
- **编译警告**：本机**无 LaTeX 工具链**（`pdflatex` / `tectonic` 均不可用），故「页数 ≤ 9」「0 未定义引用（读 `.aux`/`.log`）」**必须由用户在 TeX 环境或 CI 复验**。本清单 §8 给出命令。

---

## 1. 匿名化检查（Anonymity）

- [x] 作者块 = `Anonymous Author(s)`；正文无姓名 / 邮箱 / 单位。
- [x] 正文无仓库 URL、用户名、本地绝对路径、机构名（`anonymity_check` MAIN/STRICT 历史命中 0）。
- [x] `.bib` 中唯一 URL = `https://opentimestamps.org`（公开协议站，非身份链接）。
- [ ] 补充材料（代码 / 数据链接）若随 arXiv 上传，须确认**匿名可访问**（D&B 双盲情形）。
- [ ] 2027 官方样式发布后替换 `neurips_2025.sty` → `neurips_2027.sty`（CFP 未发布，须复核）。
- [⚠] 文件头注释「Migrated from v0.7; all numbers match that draft」已过期，投稿前建议改为 v1.1 + 权威源说明。

---

## 2. 自引 / 参考文献检查（Self-citation & bib）

- [x] `queyi_refs.bib` 条目均为真实文献（673a 已核验 4 条 2026 文献真实；无占位 / 假引用）。
- [x] **无自我引用泄露身份**：bib 中无作者姓名 / 个人主页；正文 Related Work 为对比性，不指向可识别作者。
- [ ] arXiv 预印本若填 `comments` 或上传与作者相关的引用，须避免泄露身份。
- [ ] 编译后 grep `.aux`/`.log`：无 `??` 未解析引用（含 `app:clangtidy`、`tab:*`、`fig:*`）。

---

## 3. tarball（源码包）结构

arXiv 源码包 `queyi_neurips2027_v1.1.tar.gz` 应包含：

```
queyi_neurips2027_v1.1.tex      # 主稿（英文）
queyi_refs.bib                  # 参考文献
neurips_2025.sty                # 样式（2027 出后替换）
queyi_neurips2027_v1.1.pdf      # 编译产物（必备）
```

- [x] **无外部图片文件**：Fig.1 / Fig.3 / Fig.4 均为内联 TikZ / pgfplots；原 `fig:data` 已改为正文叙述（无独立图文件）。
  ⇒ 无需 `figures/` 目录、无需 `\graphicspath`、无 EPS / PDF 外部图。
- [x] 附录表均为 `tabular` 内联。
- [⚠] 若未来加入外部图（PNG/PDF），须一并打包并设置 `\graphicspath`。

---

## 4. 图片可编译性（Figure compilability）

- [x] TikZ + pgfplots 已在导言区 / `.sty` 启用。
- [x] Fig.4 `symbolic x coords` 已含 `672h`（673a 修复）。
- [x] 所有 `\ref{fig:*}` / `\ref{tab:*}` 均可解析（脚本核验 0 `??`）。
- [ ] 在目标 TeX Live（推荐 2024/2025）或 tectonic 0.15+ 验证编译。

---

## 5. 投稿步骤（arXiv）

1. 注册 / 登录 arXiv 账号（若无）。
2. 准备源码包（见 §3），上传 `.tar.gz` 或单 `.tex`（arXiv 自动处理 bib）。
3. 选分类（category）：主类建议 **cs.LG**（机器学习）/ **cs.AI** / **cs.SE**（软件工程）；交叉可加 **stat.ML**。NeurIPS E&D 偏 D&B，cs.LG / cs.AI 最常见。
4. 填标题（保持与投稿一致）、摘要（**注意**：arXiv 摘要为公开且永久，确认不含未公开数据或身份）、comments（**仅在被接收或 under review 时**才可写 "under review / accepted at NeurIPS 2027 D&B"；纯预印本不要谎称接收）。
5. 提交 → 自动 + 偶发人工审核 → 获得 arXiv ID（通常数小时至 1 天）。

---

## 6. Endorser 查找（关键）

- **是否需要 endorser**：若你的 arXiv 账号在该 category **无自动提交权限**（新账号或该领域首次提交），需一位**已在该 category 发过论文的 endorser** 背书。
- **如何找**：
  - 在合作者 / 导师 / 同行中找**已在 cs.LG / cs.AI / cs.SE / stat.ML 发过 ≥1 篇**的人，请其在 arXiv「Endorsement」页面为你背书。
  - 若无合适人选：arXiv 提供 "request endorsement" 链接，填一段研究说明，系统可能自动匹配或要求等待。
  - 注意：**endorser 不审内容**，只确认你确实做相关研究。
- **备选**：若账号已有该 category 提交权限（如既往发过），直接提交，无需 endorser。
- **建议**：截稿前 1–2 周确认 endorser，避免卡审。

---

## 7. FAQ

- **Q：arXiv 有 9 页限制吗？** 没有。arXiv 对页数宽松（单 PDF 建议 ≤ ~50 页，过大需拆分）。**9 页限制是 NeurIPS 的**，与 arXiv 无关；预印本可保留完整附录。
- **Q：必须匿名吗？** 否。arXiv 预印本通常**署名**；匿名版仅在双盲投稿系统需要。若先投双盲再挂 arXiv，注意 arXiv 会公开作者（可设延迟公开，或先发匿名预印本）。
- **Q：图片是 TikZ 怎么办？** arXiv 的 TeX 编译（TeX Live）支持 TikZ / pgfplots；内联即可，无需外部图。
- **Q：编译失败常见原因？** `.sty` 缺失（务必打包进去）、bib 未编译（用 `pdflatex + bibtex + pdflatex×2` 或 tectonic）、`hyperref` 冲突、字体缺失。
- **Q：comments 字段能写什么？** 仅接收 / under-review 状态；不要写未发生的接收。
- **Q：双盲 + arXiv 冲突？** NeurIPS 双盲评审期（review 期间）挂署名 arXiv 可能破盲；建议 review 结束后再挂，或使用匿名预印本。

---

## 8. 投稿前「必做」复查（静态 / 编译）

| 项 | 谁做 | 命令 |
|---|---|---|
| 0 孤儿浮动体 / 0 未定义 `fig:tab` 引用 | ✅ 本机已脚本核验 | `python analyze_refs.py`（见 `queyi_neurips2027_v1.1.tex`） |
| 0 个 `??`（含 appendix 引用） | 🔴 需编译 | `grep -c "??" queyi_neurips2027_v1.1.log` → 期望 0 |
| 主文 ≤ 9 页（NeurIPS） | 🔴 需编译 | 读 `.aux` 中 `page:endmain` 落在第 9 页；或 `pdfinfo … \| grep Pages` |
| 匿名化 grep | 本机可做 | `grep -Rni "author\|university\|github.com/<user>" research/latex/*.tex` |
| bib 自引泄露 | 本机可做 | 人工核对 `queyi_refs.bib` 无作者姓名 |

---

*本清单由 673i 批次生成，仅写 `data/673i_*`；未触碰 `tools/ tests/ web/ data/（既有实验数据）/ research/latex/*.sty` 等红线文件以外的既有产物。*
