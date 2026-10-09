# 702 · README 改进建议（根 README.md 检查）

> 受检文件：根 `README.md`（**只读，未修改**）
> 检查时间：2026-10-09｜方法：通读 + 交叉核对 cover letter / 692 / 697 题名纪律

---

## 一、总体评价

根 README 质量**很高**：一句话定位清晰、五核心发现带数字与取证入口、诚实边界（§9）坦诚（human IAA=0、模板克隆率、Docker 未实测、WSL 硬依赖）。以下为**投稿前必须修**与**可选增强**两类建议。

---

## 二、🔴 必须修（投稿前阻塞项）

### 1. §6 BibTeX 仍用**旧题名**
- 现状（§6，约 125–132 行）：
  ```bibtex
  title = {Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection},
  ```
- 问题：692/697 红线条令明确**"题名已不再是 'Evolving Verifiers'；任何材料中出现旧题名即为缺陷"**。
  论文正文、cover letter（v1.7）、rebuttal 已全部改用新题名
  *"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"*。
  README 引用是**公开的旧题名残留**，投稿前必须改。
- 建议：title 改为新题名；同时检查 `CITATION.cff`、`docker/paper/Dockerfile`、`preview_package*/` 等（见 `702_pre_submission_checklist.md` §D）。

### 2. §6 note 的 track 名称与封面不一致
- 现状：`note = {Manuscript in preparation (NeurIPS 2027 Datasets \& Benchmarks track)}`
- 问题：cover letter 与目标 track 为 **"Evaluations & Datasets (E&D) track"**（2026 由 Datasets & Benchmarks 改名）。
- 建议：统一为 "Evaluations & Datasets (E&D) track"。

---

## 三、🟡 可选增强（提升开源体验）

3. **§8 招募指针**：当前指向 `data/693_github_recruitment_issue.md`。本批已产出优化版
   `data/702_github_iaa_recruitment_issue.md`（含 badge、ASCII 示例、更强 FAQ）。
   建议：改为指向 702 版，或同时列出两版（693 为历史、702 为拟用）。
4. **§4 项目结构**对 `docs/` 的描述过简（仅"ENVIRONMENT.md 与研究报告"）。建议补一句
   "文档按 入门/教程/参考/开发 分组，见 `data/702_docs_index.md`"。
5. **标注包路径**已在 §4 正确列出 `data/annotation_package/`，但 §8 的招募说明可顺带提一句
   "145 条盲标 + 31 条裁决，详见包内 README.md / QUICKSTART.md"。
6. **首屏 badges**：CI/DCO/Docker/Pages/Citation 齐全，专业度高，保持即可。

---

## 四、一致性交叉核对（已通过项）

- §2 五核心发现数字（asan 61.65%、38.4% 盲区、13/34 类 >50%、60.07%→24.74%、+24.03pp）与
  cover letter v1.7、仓库 frozen 矩阵一致。✅
- §9 诚实边界（human IAA=0、模板克隆率 62.2%、Docker 未实测、WSL 硬依赖）与投稿材料一致。✅
- §3 复现命令、`docs/ENVIRONMENT.md` WSL UTF-16LE 横幅坑提示，与仓库实测环境记录一致。✅

---

## 五、结论

README **内容扎实、诚实度高**，仅有 **2 处题名/track 一致性缺陷需在投稿前修**（均已定位到具体段落）。
其余为开源体验增强，不阻塞投稿。

> 本检查未改动 `README.md` 任何字节（红线）；建议项供作者决策。
