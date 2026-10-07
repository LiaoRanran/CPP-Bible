# 679 批次验收报告 · Cover Letter 升级与一致性修复

- **批次**：679（LaTeX cover letter 升级 v1.2→v1.3 + 双版本一致性终检 + 编译 + 同步确认）
- **日期**：2026-10-07
- **范围**：A LaTeX 版升级 / B 双版本一致性 / C arxiv 同步 / D 报告+DCO
- **红线遵守**：只改 `research/latex/cover_letter.tex` 与本报告；未动论文正文 `queyi_neurips2027_v1.1.tex`、检测器、样本；所有数字来自 `data/current_numbers.json`；诚实优先（局限未弱化）；DCO 签名。

---

## A. LaTeX 版 cover_letter.tex 升级

| 项 | 升级前 (v1.2 / 677a) | 升级后 (v1.3 / 677d) |
|----|----------------------|----------------------|
| 版本头 | v1.2 (677a) | **v1.3 (677d)**，补 677d 变更说明 |
| 贡献条数 | 3 条 | **5 条**（对齐 `research/cover_letter.md`） |
| Headline 随机代理 | 仅 Static 对比 | **新增 Random proxy 9.8%/21.9%（Δ+73.2/+40.6pp，p=1.9e-9/3.0e-8，h≥0.85）** |
| A5 Δ | +24.0pp | **+24.03pp**（JSON 精确值） |
| 能力边界地图 | 仅 38.4% 盲区 | **补 61.6% 检出率** |
| Limitations | 缺 ~5% 跑间不稳定、有效 n | **补 ~5% run-to-run instability（676f 自证）+ 有效 n≈133–140（design effect≈4）** |
| Prior work | 无 MiniCheck | **补 MiniCheck（evolve judge weights）** + 核心区分补 "and self-falsifiable" |

新增 5 条贡献（逐字对齐 markdown v1.3）：①失败驱动演化形式化+否证协议（A0–A5）+可审计性（Merkle 5 目录/452 账本/不依赖内核对账器）；②大规模实证资产（1147×70，7 批 expA–G，provenance 968/74/0，四态口径移动 9.9pp）；③A5 全量否证+稳健性（1137×8=9096 次 detect，FD 54.6% vs Random 30.6% +24.03pp p=2.3e-41 vs Static 24.7% +29.9pp，并列 0.0pp⇒direction-only，选择效应 +7–12pp，clone-family +23.0–+26.7pp，有效 n≈133–140）；④能力边界地图（1147×8：61.6% 检出 / 38.4% 盲区 / 18/70>50% / instrument-boundary）；⑤开源可复现（Apache-2.0+DCO、fail-loud 脚本、单命令复算、Croissant/RAI 待办）。

---

## B. 双版本一致性终检（tex vs md，JSON 为权威）

逐 token 交叉核对 39 项（headline / A5 / 盲区 / provenance / 样本量 / 术语）：
- **结果：100% 一致。** 两版均含 82.9/34/41、62.5/40/64、2.4/17.2、+80.5/+45.3、54.6/30.6/24.7/+24.03/+29.9、0.0pp、+7–12pp、+23.0–+26.7pp、133–140、38.4/18-70/61.6、968/74/0、1147/1137/9096、Merkle 5/452、9.8/21.9/+73.2/+40.6、MiniCheck、self-falsifiable、instrument-boundary、source-derived-reconstruction、evidence-acquisition。
- **两处"伪不一致"（核对工具 token 转义假阳性，非内容差异）**：
  - `2.4%`/`17.2%` 在 tex 中以 `\textbf{2.4\%}`（LaTeX 转义 `%`）存储，字面 "2.4%" 不在 tex → 实为一致。
  - `+7–12pp`：tex 用 ASCII `--` 排版 en-dash（`+7--12pp`），md 用真 en-dash `–` → 语义一致。
- **唯一编辑性差异（双方均 JSON 自洽，非错误）**：p 值/Cohen's h 的呈现口径。
  - tex：精确主对比 holdout/corpus vs Static `p=2.3e-10/3.7e-9`、`h≥0.97`；并补随机代理 `p=1.9e-9/3.0e-8`、`h≥0.85`。
  - md：仅给较松下界 `p≤3.0e-8`、`h≥0.85`（对应随机代理 corpus）。
  - **结论**：两版均 ≤ JSON 真值（JSON: holdout p=2.33e-10、corpus p=3.73e-9、corpus-random p=2.98e-8；cohen holdout 1.98/corpus 0.97/corpus-random 0.85），无矛盾。建议后续批次把 md 头条也补回随机代理对比 + 精确主对比值，使两版完全同口径（非阻塞）。

---

## C. arxiv_submission 同步

- `research/latex/arxiv_submission/` 目录清单：`neurips_2025.sty`、`queyi_neurips2027_v1.1.tex`、`queyi_neurips2027_v1.1.tex.bak677e`、`queyi_refs.bib`、`README.txt`。
- **无独立 `cover_letter.tex`**（arXiv 投稿包通常不收 cover letter，cover letter 仅投会议系统用）。
- **结论：C1 无需同步**——主版本升级已落地，arxiv 包未含也不需含 cover letter。

---

## B3. 编译验证

- 命令：`tectonic --keep-logs --outdir . cover_letter.tex`（standalone，`article` 类 + 标准包，无 bib）。
- **结果：0 错误、0 未定义引用/未定义 citation**（log 中无 `!` 行；rerunfilecheck 为包加载信息，非错误）。
- **PDF 生成成功**：`cover_letter.pdf` ≈ 42 KB。
- **页数：3 页**（内容含 5 贡献 + 完整 Headline + 详尽 Limitations，偏长但可接受；cover letter 常规 1–2 页，此处因完整性对齐 markdown 而扩展）。
- 两条 `Overfull \hbox` 警告（line 67 / 88，段落略宽）为**排版美观性警告，非错误**，不影响 PDF 正确性。
- `Fontconfig error: Cannot load default config file` 为本机 Windows 缺 fontconfig 默认配置的环境告警（与 678 批次同），**非代码错误**，tectonic 仍正常写出 PDF；CI/ubuntu 不受影响。

---

## 仍存在的问题（非本批引入，建议后续）

1. **md v1.3 头条 p 值/h 为较松下界**（p≤3.0e-8、h≥0.85），与 tex 精确值（p=2.3e-10/3.7e-9、h≥0.97）口径不同——两版 JSON 自洽但 md 信息偏少，建议补回随机代理对比使完全同口径。
2. **cover letter 3 页偏长**：若会议系统有页数限制，可压缩贡献条描述或合并 Prior work/Limitations 小段（非阻塞）。
3. **Overfull \hbox 警告**：可在长行插入 `\linebreak[0]` 或微调，纯美观优化。
4. **本地 tectonic fontconfig 告警**：仅本地 Windows 环境；CI 无需编译 cover letter（不在 CI 路径），无关。

---

## D. 本批提交文件（仅本批，未裹挟其他批次）

- `research/latex/cover_letter.tex`（A1–A5 升级，modified）
- `data/679_cover_letter升级报告.md`（本报告，new）

> 说明：`cover_letter.pdf` / `cover_letter.log` / `.aux` / `.xdv` 等为编译产物，未纳入提交（与论文 PDF 同属 gitignore 的构建产物）。arxiv 目录无变动。

## DCO 与 push

- 提交方式：`git add` 仅上述两文件 → `git commit -s`（author=SOB 一致，身份 `674d-ci`）。
- **未 push**（按验收末条「等用户确认后再 push」）；当前本地未 push 提交累计为 25（678）+ 1（679）= 26。
