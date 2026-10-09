# 712 批次 — GitHub Release v1.0 准备材料（queyi-audit）

> 本文件是发布前的"作战手册"。所有材料保持双盲匿名，不出现作者姓名、学校、邮箱。
> 发布动作由你本人在 GitHub 网页端完成，本文件只提供文案与清单。

---

## 1. Release Title 与 Tag 建议

**Tag（建议打在匿名仓库的 main 分支上）：**
```
v1.0.0
```
语义化版本号，首次公开发布。不要在 tag 里带任何日期或作者缩写。

**Release title（三选一，推荐 A）：**

- **A（推荐）**：`Queyi Audit v1.0.0 — Caliber Drift and Capability Boundaries (double-blind release)`
- B：`v1.0.0 — First public release: reproducibility package for measurement-drift audit`
- C：`Caliber Drift Audit Protocol v1.0`

选 A 的理由：标题里直接点出核心概念 "Caliber Drift"，方便被搜索；同时标注 "double-blind release" 主动声明匿名身份，避免审稿人/读者误以为是漏写作者。

---

## 2. Release Notes 正文（英文，直接粘贴）

```markdown
# Queyi Audit v1.0.0

This is the first public release of an anonymous, double-blind reproducibility
package for auditing the *evaluator* of a C/C++ software-verification apparatus.
It accompanies two companion papers:

- **Paper 1 — Caliber Drift and Capability Boundaries: An Audit Protocol for
  Software-Verification Evaluation** (empirical audit, 1147-sample controlled
  environment study + 40-CVE case library).
- **Paper 2 — The Boundary of Evaluator Auditing: Identifiability,
  Correctability and Sample Complexity of Measurement Drift** (theoretical
  boundaries: 8-axiom algebra, information-theoretic sample complexity).

## Headline findings (all numbers are reproducible from this release)

- **Environment drift is silent and large.** On the same detection apparatus,
  the observed detection rate moves from **60.07% (WSL, E1)** to **24.74%
  (native Windows, E2)** — a 35.33-point gap — while the discordance count
  against the "unknown" bucket stays at zero. McNemar paired test:
  **p = 1.24e-60**. The evaluator never flagged this as a failure; it just
  quietly changed what "correct" means.
- **Structural Goodhart, four types, one curve.** We classify structural
  (passive, no optimizer-pressure) Goodhart into four types and fit the
  apparent-gain surface
  `g_app(d) = 5.47 + 5.28 d − 0.26 d²` with **R² = 0.9997**.
- **Measurement-drift algebra, 8 axioms, 3 independent.** Over the axiom set,
  only **A2 (removal monotonicity), A5 (super-additivity) and A8** are
  independent; A1/A3/A4/A6/A7 collapse to theorems T1–T6. The system is
  incomplete w.r.t. label drift.
- **Information-theoretic lower bounds on audit sample size.** Under a paired
  design: **Type I drift requires ≥ 849 samples**, **Type II requires ≥ 17**,
  and **Type III / Type IV paired-design power is identically 0 at any n** —
  no amount of paired sampling will detect them.
- **Capability-boundary predictor.** A logistic-style boundary model reaches
  **AUC = 0.7551** on held-out cases, i.e. it can predict *where* an auditor
  should look before running the experiment.
- **F1 causal decomposition of an apparent +24.03 gain.** A naive "+24.03"
  headline breaks down as: −9.55 (caliber / definition change), −8.27 (two
  zero-yield components), −4.65 (linker behavior), +10.74 (k-sweep tier) =
  **net +12.30**. More than half of the "improvement" was measurement drift.
- **Real-world anchor.** A case library of **40 real NVD CVE cases** ships in
  `data/raw_external/`; **14 of them compile cleanly** as PoCs under the frozen
  matrix.

## What you can do with this release

1. Recompute every headline number above from frozen detection matrices
   (`data/frozen_matrix/`) — no re-running of the detector is needed.
2. Run the number-traceability gate:
   `python tools/verify_paper_numbers.py --tex paper/paper1/queyi_neurips2027_v1.1.tex ...`
3. Run the pytest suite (`python -m pytest tests/ -q`).
4. Compile both papers with tectonic (sources included).

## Honest limitations (not hidden)

- **Human inter-annotator agreement (IAA) = 0.** All κ values in the papers
  are AI self-consistency, not human agreement. The annotation package
  (`data/annotation_package/`, 145 items) is shipped unexecuted; this is a
  known, declared weakness, not an oversight.
- Docker recipes are not build-tested in the authors' own environment.
- One asset's PoCs are English-only; the CVE benchmark uses reconstructed
  contexts, not original project histories.

## License

Apache-2.0. DCO sign-off required for contributions.

This release is **double-blind**: it contains no author name, affiliation,
email, or personal identifier. Please do not attempt to deanonymize; if you
cite it, cite it as "Anonymous, Queyi Audit, v1.0.0".
```

---

## 3. 附带资产（Assets）清单

在 GitHub Release 页面的 "Attach binaries by dropping them here" 区域上传以下文件。**文件名全部小写、连字符分隔，不要带作者名**：

| # | 资产文件名（建议） | 内容 | 来源路径 |
|---|---|---|---|
| 1 | `paper1-caliber-drift-audit-protocol.pdf` | 论文1编译后的 PDF | `paper/paper1/`  tectonic 产物 |
| 2 | `paper2-boundary-of-evaluator-auditing.pdf` | 论文2编译后的 PDF | `paper/paper2/` tectonic 产物 |
| 3 | `REPRODUCTION.md` | 复现步骤、环境、期望输出（仓库根目录已有，直接随 release 挂一份） | `REPRODUCTION.md` |
| 4 | `data-highlights.md` | 一页纸数据亮点（见下方模板） | 新建，放入 release root |
| 5 | `frozen-matrix-snapshot.tar.gz` | `data/frozen_matrix/` 打包，让不 clone 仓库的人也能看到原始矩阵 | `data/frozen_matrix/` |
| 6 | `cve-case-library-40.tar.gz` | `data/raw_external/` 打包（40个CVE案例，14个可编译） | `data/raw_external/` |

**不要上传**：`.git/`、构建中间产物、`paper/paper*/cover_letter/`（双盲投稿信里可能有邮箱残留，发布前 grep 一遍）。

### data-highlights.md 模板（新建后随 release 上传）

```markdown
# Data Highlights — Queyi Audit v1.0.0

| Quantity | Value | Where to reproduce |
|---|---|---|
| Environment drift E1 (WSL) | 60.07% | data/frozen_matrix/, tools/ |
| Environment drift E2 (native) | 24.74% | data/frozen_matrix/, tools/ |
| McNemar p (E1 vs E2) | 1.24e-60 | tools/ |
| Apparent-gain fit g_app(d) | 5.47 + 5.28d − 0.26d², R²=0.9997 | tools/ |
| Independent axioms | A2, A5, A8 | paper/paper2/ |
| Type I audit sample lower bound | 849 | paper/paper2/ |
| Type II audit sample lower bound | 17 | paper/paper2/ |
| Type III/IV paired-design power | 0 (any n) | paper/paper2/ |
| Capability-boundary AUC | 0.7551 | tools/ |
| F1 apparent gain decomposition | +24.03 → net +12.30 | tools/ |
| Real CVE case library | 40 cases, 14 compile | data/raw_external/ |
| Human IAA (honest) | 0 (AI self-consistency only) | — |
```

---

## 4. README.md 改进建议（只读建议，不要直接改文件）

当前 README 整体已经很扎实（双盲声明、quick start、honest limitations 都在）。以下是针对 **v1.0 Release 后的公开流量** 做的小修，按优先级排序：

### P0 — 必须加（Release 发布当天就改）

1. **在最顶部加一行"Latest release"徽章**，指向 v1.0.0：
   ```markdown
   [![Release](https://img.shields.io/badge/release-v1.0.0-blue.svg)](https://github.com/<your-anonymous-repo>/releases/tag/v1.0.0)
   ```
   匿名仓库的 URL 用你的匿名 org/account，不要填个人名。

2. **在 "Core findings" 区块补三个具体数字**，现在这一段偏定性。建议在现有 bullet 后面追加：
   - `Environment drift: 60.07% (WSL) → 24.74% (native), McNemar p=1.24e-60.`
   - `Apparent-gain surface: g_app(d)=5.47+5.28d−0.26d², R²=0.9997.`
   - `Sample-complexity lower bounds: Type I ≥ 849, Type II ≥ 17, Type III/IV = 0 under paired design.`
   理由：别人在 GitHub 搜索结果页只看得到 README 前几行，必须把最硬的数字堆在前面。

3. **在 "Honest limitations" 里把 "Human IAA = 0" 这条加粗并放到第一条**（现在它已经是第一条，但可以再强化一句："This is a declared limitation, not a hidden one — we ship the annotation package unexecuted rather than fabricate human agreement."）。这反而是这个仓库的**可信度卖点**。

### P1 — 建议加

4. **加一段 "Who is this for?"**（3 行）：
   - 做 SBOM / SAST / 形式化验证工具评测的人
   - 给 ML/系统论文做 reviewer 的人（想知道 "这个数字到底靠不靠谱"）
   - 做元研究 / 可复现性研究的人

5. **Quick start 里把 "number traceability" 那一步改成默认第一步**，并标注 expected output：
   ```bash
   python tools/verify_paper_numbers.py --tex paper/paper1/queyi_neurips2027_v1.1.tex \
       --out-json data/paper1_numbers.json --out-md data/paper1_numbers_report.md
   # Expected: all headline numbers (60.07, 24.74, 1.24e-60, R²=0.9997, ...) PASS
   ```
   让路人 30 秒内看到"数字真的能复现"。

6. **Citation 区块加一段 "For anonymous double-blind citing"**：
   ```markdown
   When citing during double-blind review, use: Anonymous (2027). Queyi Audit
   v1.0.0. https://github.com/<your-anonymous-repo>. Do not deanonymize.
   ```

### P2 — 可选

7. 加一个 `docs/` 目录放一两篇博客链接（见 712_技术博客草稿.md），但博客发布时**不要写学校名**。
8. 在 "Repository layout" 里补一行 `releases/` 说明 release 资产清单。
9. 考虑加一个 `.github/ISSUE_TEMPLATE/`，但双盲期不要开 Discussions。

---

## 5. 让 Release 被搜到：关键词 / 描述 / Topics

### 5.1 仓库 Description（GitHub 主页那一行，150字符内）

```
Double-blind reproducibility package for auditing software-verification evaluation: caliber drift, structural Goodhart, measurement-drift axioms, sample-complexity bounds.
```

### 5.2 Topics（GitHub repo 右侧 "About → gear → Topics"，最多 20 个）

按优先级：
1. `software-verification`
2. `measurement-drift`
3. `goodharts-law`
4. `reproducibility`
5. `evaluation-methodology`
6. `c-plus-plus`
7. `static-analysis`
8. `cve`
9. `empirical-software-engineering`
10. `audit-protocol`
11. `information-theory`
12. `sample-size`
13. `double-blind`
14. `open-science`
15. `frozen-data`

### 5.3 Release 页面的 "Describe this release" 字段（SEO 用）

```
First public double-blind release of an audit framework for C/C++ software-verification evaluation. Contains frozen detection matrices, analysis tools, LaTeX sources for two companion papers, a 40-case real-CVE library (14 compilable PoCs), and a number-traceability gate. Headline: environment drift 60.07%→24.74% (McNemar p=1.24e-60), structural Goodhart g_app(d)=5.47+5.28d−0.26d² R²=0.9997, Type I audit sample ≥849, Type II ≥17, Type III/IV paired power=0, boundary AUC=0.7551.
```

### 5.4 被外部搜到的其他小动作

- 把 release URL 贴到你那两篇博客的"项目主页"链接里（博客里不放学校名）。
- 在 papers with code / Zenodo 上**用匿名方式**同步一份（Zenodo 会给 DOI，但会要作者名 —— 双盲期先不要上 Zenodo，等解除双盲再上）。
- Hacker News / Reddit 的 r/programming 发帖**等论文中稿后再发**，现在发会被审稿人扒出来破盲。

---

## 6. Release 发布检查清单（发布前逐项打勾）

### 匿名性检查（最关键）
- [ ] `grep -ri "合肥\|hefei\|HFUU\|@.*\.edu" paper/ data/ tools/` 无命中
- [ ] `grep -ri "LiaoRanran\|1026708211" paper/ data/ tools/` 无命中
- [ ] git log 里 author 字段全部是 `Anonymous <anonymous@anonymous>`，不是你真实邮箱
- [ ] 两篇 PDF 的 metadata（作者、标题、主题）里没有个人信息：
      `exiftool paper1.pdf` / `exiftool paper2.pdf` 检查 Author / Creator 字段
- [ ] PDF 内文 grep 一遍 "university" / "school" / "advisor" 无具体名
- [ ] cover letter 目录**不**打包进 release assets
- [ ] GitHub repo 的 Settings → Actions → 检查没有 workflows 里 hardcode 了你的邮箱
- [ ] GitHub account 本身是匿名小号，不要绑定你常用邮箱/手机号到公开 profile

### 数据完整性检查
- [ ] 在干净 clone 上跑 `python tools/verify_paper_numbers.py` 全部 PASS
- [ ] `python -m pytest tests/ -q` 全绿
- [ ] 两篇 PDF 用 tectonic 在干净环境编译成功
- [ ] frozen matrix 里的 60.07 / 24.74 / 1.24e-60 / R²=0.9997 / 849 / 17 / 0 / 0.7551 / +12.30 全部能在 `data/paper1_numbers_report.md` 里对上
- [ ] `data/raw_external/` 里 40 个 CVE 案例，`14` 个确实能编译（在 Linux/WSL 下跑一遍编译脚本）

### Release 工程检查
- [ ] tag `v1.0.0` 打在 main 分支最新 commit
- [ ] Release title、release notes 复制粘贴自本文件第 2 节（不要手改数字）
- [ ] 6 个 assets 全部上传完成（见第 3 节表格）
- [ ] "Set as the latest release" 勾选
- [ ] "This is a pre-release" **不要勾**（这是正式版）
- [ ] Discussion 选项：双盲期不要开

### 发布后 5 分钟自检
- [ ] 无痕窗口打开 release 页面，确认看不到作者信息
- [ ] 无痕窗口 clone 仓库，跑 quick start 第一步
- [ ] 把 release URL 贴到 incognito 浏览器确认可访问
- [ ] 截图存证（万一以后破盲纠纷时能证明你 v1.0 时是匿名的）

---

## 7. 不要做的事（红线）

- 不要在 release notes 里写 "I" / "we" 之外的身份线索（不要提 undergraduate / solo / 合肥学院）。
- 不要 @ 任何真实人物或机构。
- 不要在 release 里附 cover letter / submission response（那些是给审稿人的，不是给公众的）。
- 不要现在就去 Twitter/X / 知乎实名宣传 —— 等论文 decision 出来再动。
- 不要 push 到你个人 GitHub 主账号；用匿名 org。
