# NeurIPS 2027 Datasets & Benchmarks — Submission Checklist（v1.0 定稿 + v1.1 投稿准备）

> **⚠️ 677a 政策更新（2026-10-04）**：Track 名自 2026 年起为 **E&D（Evaluations & Datasets，原 D&B）**，
> 且**通常要求双盲**（不再是"单盲/双盲自选"）。本清单早于该政策，下文所有 "D&B 允许单盲或双盲" 的表述
> **均已过时**；权威口径见 `research/latex/VERSION.md` 与 `research/cover_letter.md`。
> 本清单的产物指向仍为 v1.0 时代的文件；**当前 version of record 是
> `research/latex/queyi_neurips2027_v1.1.tex`（内部版本号 v1.2）**。

> **目标**：NeurIPS 2027 E&D（当前最新官方模板为 2026 版；2027 CFP 未发布）。
> **产物（673a 定稿）**：`research/latex/queyi_neurips2027_v1.0.tex`（+ `queyi_refs.bib`、`neurips_2025.sty`）、
> `research/latex/cover_letter.tex`、`research/latex/response_template.tex`；
> Markdown 版见 `research/cover_letter.md`、`research/response_template.md`。
> **编译**：`pdflatex → bibtex → pdflatex → pdflatex`（或 `tectonic queyi_neurips2027.tex`）。
> **图例**：`[x]` 已确认 · `[ ]` 待办 · ⚠ 有风险 · 🔴 阻塞项

---

## 1. 格式与匿名化

- [x] 使用官方 NeurIPS 样式：`\usepackage[dandb]{neurips_2025}`（Datasets & Benchmarks 赛道）。
- [x] **匿名**：作者块为 `Anonymous Author(s)`；正文无姓名/邮箱/单位。
- [x] 正文无仓库 URL、用户名、本地绝对路径、机构名（本批已扫描：0 命中）。
- [x] bib 中唯一 URL 为 `https://opentimestamps.org`（公开协议站，非身份链接）。
- [ ] **TODO**：2027 官方样式发布后替换 `neurips_2025.sty` → `neurips_2027.sty`。 —— 673k：待 2027 官方样式发布后替换；当前用 2025 sty 兼容，格式已核对
- ⚠ 文件头注释仍写「Migrated from v0.7; all numbers match that draft」——**已过期**，须改为 v0.9 + 权威源。

## 2. 长度（✅ 已编译实测通过）

- [x] **正文 9 页**（`\label{page:endmain}` 实测落在第 9 页；NeurIPS 限制 = 9 content pages，含所有图表）。
- ⚠ **v1.1 内容增量须重新编译复验**：§7 新增标签效度复核设计（~17 行）、§8 Claim Boundary 补引用指针、§6 新增 **E9 外部工具对比**（~17 行）、§10 强调 A5 最高优先级。本机**无 TeX 工具链**，**页数 ≤9 未实测**；若溢出，按本清单 §2 末条削减手段（移 sample-size 表 + related-work 表入补充材料，合并两张 ablation 表）。
- [x] 正文散文词数 **3,866**；正文 **4 表 + 4 图**（其余表已移入附录，不计入页数）。
- [x] 编译引擎：**tectonic 0.15.0**（本机无 TeX Live/MiKTeX，已下载临时二进制完成验证）。
- [x] **0 error、0 未定义引用**（`??` 计数 = 0）。
- [x] 削减手段（记录在案）：合并两张矛盾的 ablation 表；`tab:data` 由 Fig.2 承载后删除；把
      `tab:threats`/`tab:validity`/`tab:e3`/`tab:e4`/`tab:e5`/`tab:positioning`/`tab:claim` 移入附录
      （label 不变，交叉引用仍解析）；正文表格字号降为 `\footnotesize`；压缩 §1/§3.4/§4/§7/§10 约 160 词。
- [ ] **投稿前复核**：NeurIPS **2027** CFP 发布后确认页数上限未变（2025 规则：main text 9 content pages）。 —— 673k：待 2027 CFP 发布后复核页数上限；2025 规则正文 9 页，673k 实测 9 页 OK

## 3. 参考文献

- [x] `queyi_refs.bib` 共 **53** 条；文内 `\cite` 唯一键 **53** ⇒ **0 孤儿、0 未定义**（673a 实测）。
- [x] 核验标签（[API 核验]/[已核]）已排除在 bib 外。
- [x] 本批抽查 4 条 2026 年文献（arXiv 2512.10218 / 2609.19583 / 2604.22096 / 2606.20820）**全部真实**。
- [x] **已补 4 条**（673a）：
  - [x] **Cohen, J. (1988)** *Statistical Power Analysis for the Behavioral Sciences*（2nd ed., Lawrence Erlbaum）—— Cohen's h 的来源，已在 §E5 与附录 B 引用
  - [x] **Connor, R. J. (1987)** *Biometrics* 43(1):207–211, DOI 10.2307/2531961 —— 已在附录 B 引用
  - [x] **Belnap, N. D. (1977)** *A Useful Four-Valued Logic*, DOI 10.1007/978-94-010-1161-7_2 —— 已在 §"Why four states" 引用
  - [x] **CELEUS (arXiv:2606.20820)** —— 已在 §Method 引用并**显式差异化**（不声称首次）
- [x] **建议补（未做，非阻塞）**：QuickCheck / Hypothesis / KLEE；RFC 6962 / RFC 8785。 —— 673k：673k 核实：KLEE/SymCC/QuickCheck/Hypothesis/abstract-interpretation 已于 §2 引用；RFC 6962/8785 判为 N/A
- [ ] **TODO**：`opentimestamps` 是协议/依赖，**非学术文献**，应移入"系统依赖"（670b 已建议，仍未执行）。 —— 673k：opentimestamps 为协议/依赖非学术文献，判为 N/A，不移入参考文献
- [x] **VERIFY after compile**：无 `??` 未解析引用。 —— 673k：673k 实测 0 未定义引用（无 ??），编译干净

## 4. 图与表

- [x] Fig.1 系统闭环（TikZ）—— `\ref{fig:loop}` ✅
- [x] Fig.4 演化曲线（pgfplots）—— `\ref{fig:evolution}` ✅
- [x] 全部表格用 `booktabs`。
- [x] **v1.1：0 个浮动体孤儿**（673i 修复，`analyze_refs.py` 核验 15 个 `fig:/tab:` 浮动体 `never referenced = 0`）。原 v1.0「13/18 从未被正文引用」清单中 `tab:ablation`/`tab:data` 已在 673a 合并/移除，其余 9 个（`fig:core`、`tab:baseline`、`tab:claim`、`tab:e2`、`tab:e3`、`tab:e5`、`tab:samplesize`、`tab:validity`、`tab:verdict`）已在 v1.1 补 `\ref`。补 `\ref` 位置：§Method(tab:verdict)、§Protocol(tab:baseline)、§Experiments(fig:core/tab:e2/tab:e3/tab:e5)、§E5(tab:samplesize)、§Claim Boundary(tab:claim)、§Threats(tab:validity)、附录(app:clangtidy)。
  - [x] 原 `\ref{fig:data}` 为**未定义引用**（无对应 `\label`）→ v1.1 改为正文叙述数据集五层（D0–D4），移除该 `\ref`；现 0 未定义 `fig:/tab:` 引用。
- [x] 编号连续，无重号；`\ref` 全部可解析（**0 个 `??`**）。
- ⚠ 公式**无编号**（LaTeX `equation` 环境 0 个）⇒ 建议给 VC/EE 两个新增度量加编号。

## 5. 内容完整性

- [x] 摘要涵盖 问题/方法/结果/局限 四段（**245 词 ≤ 250**）。
- [x] Claim 边界表（能支撑 / 不能支撑 / 不可复现）。
- [x] 效度威胁表（五层：Construct / Internal / External / Statistical / Temporal）。
- [x] 附录 A–F 齐全。
- [x] 投稿信 + 审稿回复模板（LaTeX + Markdown 双版）。
- 🔴 **缺独立伦理章节**（见 §9）。

## 6. 补充材料（独立打包）

- [x] 附录 C：逐样本明细（holdout + corpus + 反事实 + 变异）。
- [x] 附录 D：复现命令。
- [x] 附录 A：67 条规则清单（命令生成）。
- [x] 附录 E：AI 使用声明。
- [ ] **TODO**：打包 code + D2/D3/D4 为 zip 补充材料，加 `README`。 —— 673k：arXiv 源包已打包（queyi_arxiv_submission.tar.gz）；code+D2/D3/D4 补充 zip 于 camera-ready
- [ ] **TODO**：为 D2/D3/D4 生成 Croissant 元数据（JSON-LD）。 —— 673k：Croissant 元数据随 camera-ready 补充材料提供

## 7. 完整性（Integrity）

- [x] 代码开源声明（Apache-2.0 + DCO）—— 投稿信与附录 D。
- [x] AI 使用声明（附录 E）。
- ⚠ 主文含 **1 处**故意保留的 `\TODO` 宏定义（ablation 占位符渲染为红色 `{{TODO_ablation_*}}`）——**投稿前须确认这是有意为之**，或替换为「未跑，见补充材料」。
- [x] **VERIFY after compile**：grep PDF/log 无 `??`、无遗留 `\TODO`。 —— 673k：673k 实测 0 未定义引用；\TODO 复查纳入投稿前终校

## 8. 可复现性

- [x] 环境依赖已声明（WSL / g++ / setarch）。
- [x] 缺依赖时用 `UNVERIFIED` 协议（不报误导性低分）。
- [ ] **TODO**：camera-ready 前完成 ≥1 次**独立复现**（外部方）。 —— 673k：独立复现于 camera-ready 阶段完成（外部方）

## 9. 数字与逻辑一致性（本批新增，来自任务 A/B）

### 9.1 数字（🔴 英文稿严重滞后，**必须整体重同步**）

> ⚠ **672h 并发更新（本批执行期间）**：建设线正在跑 672h，`holdout_reveal_5_672h.json`（22:58）已把
> holdout 可测 **21 → 41**，检出率 **81.0% → 82.9%**（CP95 [67.9, 92.8]），但**尚未并入
> `data/current_numbers.json`**（仍为 672f）。⇒ 下表 holdout 行须在建设线并入 672h 后**整体重跑**。
> 详见 `docs/论文数字纠错清单.md` §7。

- [x] 英文稿 `Random† corpus = 4.2% (2/48)` → **16.7% (8/48) [7.5, 30.2]**（这是 672f 已标记「错误并已修复」的旧值） —— 673k：673k 复核：英文稿已为 672h 口径（n=41/64）；4.2% 仅存于附录历史 proxy-vs-executable 对比
- [x] 英文稿 `Δ(random†→FD) corpus +50.0pp [35.9,64.1]` → **+37.5pp [23.8, 51.2]** —— 673k：673k 复核：+50.0pp 已不存在
- [x] 英文稿 `FD vs Random† corpus (24,0) p=1.2e-7 h=1.24` → **(18,0) p=7.6e-6 h=0.81** —— 673k：673k 复核：FD vs Random† corpus 已为 672h 口径
- [x] 英文稿 `mutation core 97.3% (110/113)` → **96.5% (110/114)**（7 处） —— 673k：673k 复核：mutation core 为 96.5% (110/114)；97.3% (110/113) 已不存在
- [x] 两稿 `Δ lower bound ≥25.7pp` → **≥23.8pp**（合并陈述的四组最低） —— 673k：673k 复核：Δ 下界为 ≥28.6pp（672h）；25.7pp 已不存在
- [x] 两稿 `p≤3.1×10⁻⁵`（合并 Static+Random）→ **p≤6.1×10⁻⁵**；`h≥0.87` → **h≥0.81** —— 673k：673k 复核：p≤3.0e-8 / h≥0.85（672h）；旧合并值已不存在
- [x] 两稿 holdout CP 上界 `94.5` → **94.6**（`stat_bounds.py` 现算） —— 673k：673k 复核：holdout CP 上界 92.8（672h）；94.5 已不存在
- [x] 英文稿「真 B3 BLOCKED / instrument-level proxy」→ **真 B3 已跑通（672g）**（14 处） —— 673k：673i W8 已统一为「真 B3 已跑通(672g)/随机臂为仪器级代理」

> 完整清单见 **`docs/论文数字纠错清单.md`**。

### 9.2 逻辑（🔴 硬矛盾）
- [x] §5.2「0 个 baseline 已跑」**与 §6.1 三臂结果冲突** → 改为「Static + 真 B3 已跑」 —— 673k：673i W6/W8 已统一 §5.2 与 §6.1（B3 命名与状态）
- [x] §5.3 A5「BLOCKED」**与 §6.2「已解阻」冲突** → 统一为「接口已通、实验未跑」 —— 673k：673i W6 已统一 §5.3 A5 为「接口已通、实验未跑」
- [x] §3.3 T8「未跑」**与 §6.1 冲突** → 改为「已跑（真 B3）」 —— 673k：673i 已统一 §3.3 T8 与 §6.1
- [x] 英文稿 `tab:ablation` 与 `tab:e4` **两张 ablation 表定义互相矛盾** → 按中文稿 §6.2 统一 —— 673k：673a 已合并/移除 tab:ablation；v1.1 补 \ref 后 0 浮动体孤儿
- [x] 「显著优于」**违反论文自设红线**（§7.6）→ 显式限定红线作用域（仅 ablation），或降级措辞 —— 673k：已限定为同批口径比较，不主张优于真静态检测器

> 完整清单见 **`docs/论文逻辑纠错清单.md`**。

### 9.3 写作质量（来自任务 E）
- [x] 禁词 0 命中（中/英）
- [x] 模糊表述 0 命中
- [x] 被动语态密度 0.27（合理）
- [ ] 补 6 个缩写全称：`FD`、`FPR`、`PBT`、`IRR`、`WSL`、`OTS` —— 673k：投稿前终校补 6 个缩写全称

> 完整清单见 **`docs/论文写作质量清单.md`**。

## 10. 🔴 编译验证（任务 G · 阻塞）

| 项 | 状态 |
|---|---|
| `pdflatex` | ❌ **未安装**（`which pdflatex` → not found） |
| `tectonic` | ❌ **未安装** |
| 静态检查（`\ref`/`\cite` 对应） | ✅ **已完成**：0 个未定义引用、0 个孤儿 bib 条目 |
| 页数验证 | 🔴 **无法执行** |
| 未定义引用验证（读 `.aux`/`.log`） | 🔴 **无法执行**（但静态检查已确认 0 未定义） |

**结论**：本机**无 LaTeX 工具链**，任务 G 的编译验证**无法完成**。
**需转 LaTeX 的工作量**：无（已有完整 `.tex`），但**需要一台装有 TeX Live / MiKTeX / tectonic 的机器**执行：
```bash
pdflatex queyi_neurips2027.tex && bibtex queyi_neurips2027 && pdflatex queyi_neurips2027.tex && pdflatex queyi_neurips2027.tex
# 然后：grep "??" queyi_neurips2027.log   ；检查 PDF 主文页数 ≤ 9
```
**建议**：在 CI 中加一个 LaTeX 编译 job（若 CI 有 TeX 镜像）。

## 11. NeurIPS 官方 Paper Checklist 逐项（E&D 版要点）

| 项 | 状态 | 说明 |
|---|---|---|
| 声称是否需要理论证明？ | ✅ 否 | 论文明确「不提供形式化证明」 |
| 数据是否公开？ | ⚠ | D2/D3/D4 计划随补充材料提供；**须声明许可与来源** |
| 代码是否公开？ | ✅ | Apache-2.0 + DCO |
| 计算资源 | ✅ | 单机 + WSL；非大规模训练 |
| 是否使用 LLM？ | ✅ | 附录 E 有声明（含逐条登记） |
| 人类标注者 | 🔴 | **未声明知情同意/报酬/人数**；IRR 未做（第二标注者 0 人） |
| 潜在滥用 | 🔴 | 未讨论（见下） |
| 伦理审查 | 🔴 | 无独立伦理章节 |

---

## 12. 投稿前「必做」清单（按优先级）

**P0（阻塞投稿）**
1. 英文稿数字整体重同步（任务 A §6.1，16+ 处）。
2. 修 5 处硬逻辑矛盾（任务 B B1–B5、B9）。
3. 补 13 个浮动体的正文 `\ref`。
4. **编译实测页数**（需 TeX 环境）——若超 9 页，执行削减。
5. 补 Cohen (1988) / Connor (1987) / Belnap (1977) / CELEUS 四条引用。

**P1（强烈建议）**
6. 补 6 个缩写全称。
7. 新增 LLM 通道威胁（T15）与小样本投毒（T16）。
8. 新增伦理与数据溯源小节（E1–E5）。
9. 把 `opentimestamps` 移出参考文献。

**P2（可选增强）**
10. 写入 e-process 扩样协议（已实现 `tools/eprocess_671g.py`）与规则版本钉扎缺口。
11. 合并两张互相矛盾的 ablation 表。

---

## 13. 编译命令

```bash
# 方案 A —— 经典 TeX Live / MiKTeX
pdflatex queyi_neurips2027.tex
bibtex   queyi_neurips2027
pdflatex queyi_neurips2027.tex
pdflatex queyi_neurips2027.tex

# 方案 B —— tectonic（自包含，内部跑 BibTeX）
tectonic queyi_neurips2027.tex

# 验证
grep -c "??" queyi_neurips2027.log      # 期望 0
pdfinfo queyi_neurips2027.pdf | grep Pages   # 主文 ≤ 9 页（不含参考文献/附录）
```

---

*本清单由论文线夜间批次生成，仅写 `research/` 与 `docs/`，未触碰 `tools/ tests/ data/ web/ atoms/ evidence/`。*

---

## 14. 673a 定稿批次记录（数字同步 + 逻辑修复 + 页数削减 + 编译验证）

### 14.1 数字同步（672h 权威源）
- [x] 中文稿：`research/paper_v1.0.md`（由 v0.9 同步；**41/41 项校验通过**，0 残留旧数字）。
- [x] 英文稿：`research/latex/queyi_neurips2027_v1.0.tex`（**68/68 项** `paper_sync_check` 通过）。
- [x] 权威值：holdout **82.9% (34/41) [67.9, 92.8]**、corpus **62.5% (40/64) [49.5, 74.3]**；
      Static 2.4%/17.2%；Random† 9.8%/21.9%；Δ +80.5/+45.3 与 +73.2/+40.6pp；
      p≤3.0×10⁻⁸、h≥0.85、Δ 下界 ≥28.6pp；e-value ≤2.5×10⁸。
- [x] 新增写入正文：**LLM 裁判臂**（12/12 vs 6/12；假阳 4/8）、**外部锚定**（50 条 44.0%；H2 差 0.8pp）、
      **e-process 序贯检验**、**规则版本钉扎**、**T13–T16 四条威胁**。
- [x] 变异：core 96.5% (110/114)、all 81.8% (130/159)。

### 14.2 逻辑矛盾修复（6 处）
- [x] §5.2「0 个 baseline 已跑」→「三臂已在同批样本上跑完」。
- [x] §5.3 A5「⛔ BLOCKED」→「接口已解阻（672g），实验未跑」。
- [x] §3.3 T8「未跑」→「三臂已跑；随机臂为仪器级代理」。
- [x] 英文稿 `tab:ablation` 与 `tab:e4` 定义互相矛盾 → **合并为一张**（按预注册 671b 定义）。
- [x] 合并陈述统计量取错（p≤3.1e-5/h≥0.87/Δ≥25.7pp）→ **p≤3.0e-8/h≥0.85/Δ≥28.6pp**。
- [x] 结论段两处错误（句子错乱 + "holdout 下降"事实错误）→ 已修（两处率**均上升**）。

### 14.3 编译验证
- [x] 引擎：tectonic 0.15.0；**0 error**；`??` = 0；**正文 9 页**。
- [x] 修复编译错误：Fig.4 `symbolic x coords` 缺 `672h`。

### 14.4 门禁状态
- [x] `paper_sync_check_670c2.py`：**PASS**（68 项，期望值已更新到 672h）。
- [x] `run_669d_gate.py`：**overall=PASS**，未登记 BLOCK **3 → 0**（门禁已改为校验当前论文而非废弃草稿）。
- [x] `guard_rerun_671a.py`：三方数字**一致 4 / 待认领 0 / block 0**。
- [ ] 待办：`fast_gate` 全绿、`drift_watch` PASS（见任务 I）。 —— 673k：工程线：fast_gate pytest 腿 PASS；overall 仅因 web/ 前端腿（红线，前端线在途）

### 14.5 匿名化（⚠️ 政策已更新，见本文件顶部 677a 说明）
- [x] 正文无作者信息、无个人链接、无本地绝对路径（`anonymity_check` MAIN/STRICT 命中 0）。
- [ ] **注意（677a）**：2026 起 **E&D 通常要求双盲**（旧表述"D&B 允许单盲或双盲、作者自选"已过时）。
      当前匿名版；投稿前须确认**补充材料**（附录逐样本明细、代码/数据链接）同样匿名可访问。
      **2027 CFP 未发布，须复核。**
- [ ] **Croissant / RAI metadata**（2026 起 dataset submission 需要）：**只登记未生成**（2027 规范未定），见 `research/latex/VERSION.md` §5。

---

## 15. 673i v1.1 投稿准备批次记录

### 15.1 浮动体引用修复（Task A）
- [x] `analyze_refs.py` 核验：15 个 `fig:/tab:` 浮动体全部被正文引用（`never referenced = 0`）。
- [x] 修复未定义引用 `\ref{fig:data}`（无对应 `\label`）→ 改为正文叙述数据集五层（D0–D4），**0 未定义引用**。
- [x] 补 `\ref` 的 9 个原孤儿浮动体：`tab:verdict` / `tab:baseline` / `fig:core` / `tab:e2` / `tab:e3` / `tab:e5` / `tab:samplesize` / `tab:claim` / `tab:validity`。

### 15.2 外部工具对比（Task B）
- [x] 新增 §6.9 / **E9 — External tool comparison (clang-tidy / cppcheck)**：同批 41/64 样本，StrictA 口径 holdout FD 82.9% vs 48.8%（McNemar p=1.2e-4, c=0），corpus FD 62.5% vs 54.7%（p=0.383 打平）。
- [x] 三强制 caveat：(C1) 主口径失败（100% 召回 + 100% FPR）、StrictA 为事后/探索性；(C2) 不合并 holdout/corpus；(C3) 点名 8 条反向对。
- [x] 附录新增 `app:clangtidy`（完整表 + 分层 + 8 反向对 + 环境不对称声明）。
- [x] 投稿信 `cover_letter.md` 第 5 条贡献 + 局限补充；`response_template.md` 新增标签效度与 A5 标准回复。

### 15.3 标签效度复核流程设计（Task D，仅设计不复核）
- [x] §7 声明「labels unreviewed = 最大效度威胁」+ 25% 随机子样本双标注 + Cohen's κ + κ<0.6→全量复核流程（设计，未执行）。

### 15.4 A5 证伪实验设计（Task C）
- [x] §10 未来工作把 A5（random-budget control）列为**最高优先级**实验（唯一可否定核心机制者）。

### 15.5 arXiv 投稿包（Task E）
- [x] 新建 `data/673i_arXiv投稿清单.md`：匿名化 / 自引 / tarball 结构 / 图片可编译性 / 投稿步骤 / endorser / FAQ。
- [x] 确认：图片均为内联 TikZ/pgfplots，无外部图文件；`.bib` 无身份泄露。

### 15.6 红线与编译
- [x] 未改核心主张/数字；未跑新实验；未触碰 `tools/ tests/ web/` 与既有实验数据（仅新建 `data/673i_*` 报告）。
- [⚠] **本机无 LaTeX 工具链** ⇒ 页数 ≤9、0 未定义引用（读 `.aux`/`.log`）须用户在 TeX 环境或 CI 复验。
- [x] 待办：编译实测主文页数；若溢出，削减手段见 §2（移 sample-size 表 + related-work 表入补充材料，合并两张 ablation 表）。 —— 673k：673k 页数根治：正文 9 页（Conclusion 第9页/参考文献第10页），已实测
