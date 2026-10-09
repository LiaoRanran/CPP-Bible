# REPO_METADATA_696 · GitHub 仓库描述与 topics 建议

> **为什么有这份文件**：GitHub 的仓库描述（Description）与 topics 只能在网页端或 API 设置，
> 无法从本地工作树直接修改。本文件把**建议文案**落盘，供维护者一键复制到
> `Settings → General → Description / Topics`。
> 本文件为**建议稿**，非既成事实；数字来源与 `README.md` §2 一致。

---

## 1. 建议仓库描述（Description）

GitHub 描述字段上限 **350 字符**。下面给出两版，任选其一。

### 版本 A（中文，~150 字）

```
Queyi（阙疑）：C++ 缺陷检测器组合的「失败驱动演化」研究线 —— 1147×8 冻结判定矩阵、110 条可溯源真实缺陷靶场、四态判决账本与可复现工具链；数字可独立复算、结论可被攻击。同时收录《现代 C++ 终极圣经》147 章教程。
```

### 版本 B（英文，~230 字符）

```
Queyi: failure-driven evolution of C++ defect-detector portfolios — a 1147x8 frozen detection matrix, a 110-case traceable real-world benchmark, four-state verdicts with Merkle integrity, and a reproducible toolchain. Also hosts a 147-chapter modern C++ tutorial.
```

> 选型建议：若主要面向国际研究者/审稿人，用版本 B；若面向中文读者，用版本 A。

---

## 2. 建议 topics（10 个）

GitHub topics 只允许小写字母、数字与连字符。下列 10 个按「先领域、后方法、再产出」排序：

| # | topic | 覆盖的内容 |
|---:|---|---|
| 1 | `cpp` | 语言：C++ 缺陷与教程主体 |
| 2 | `c-plus-plus` | 语言别名（GitHub 上两个都常被检索） |
| 3 | `defect-detection` | 核心任务：缺陷检测 |
| 4 | `sanitizers` | 八资产主力：ASan/UBSan/TSan |
| 5 | `static-analysis` | 编译器告警 / 跨工具链差分 / clang-tidy / cppcheck 对比 |
| 6 | `benchmark` | 冻结判定矩阵与真实靶场基准 |
| 7 | `reproducibility` | 一键复现、sha256 冻结清单、环境锁定 |
| 8 | `datasets` | NeurIPS D&B 定位；Croissant/RAI 元数据 |
| 9 | `program-analysis` | 评测器审计（evaluator audit）所属方法域 |
| 10 | `research` | 研究仓库定位（论文 + 数据集 + 工具链） |

> 说明：`verification`、`llm-evaluation`、`evaluator-audit` 也是本仓库切题的关键词，
> 但 topics 上限建议控制在 10 个以内以保持检索聚焦；如需替换，可优先替换 #10 `research`。

---

## 3. 其他建议（可选，供维护者裁决）

| 项 | 现状 | 建议 |
|---|---|---|
| Website | 静态站 `web/`，可经 GitHub Pages 发布 | 在 Description 右侧 Website 填 Pages 地址（若已启用 `pages.yml`） |
| Social preview | 未见专用图 | 可用 `docs/figures/` 下的图做社交预览图 |
| Topics 之外 | 已有 `CITATION.cff` / badges | 无需改动 |

---

_本文件由批次 696（线 C：开源线）新建。描述文案中的数字（1147×8、110 条、147 章）均与 `README.md` 一致，未新增任何未经取证的断言。_
