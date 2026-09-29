# 方向 25：Git 工作流（单人项目怎么用 branch / release）

## 核心结论
1. 单人项目最容易犯的错是**所有东西堆在 main、无 tag、无分支**——一旦改崩无法回滚。QueYi 必须有"main 稳定 + 实验分支 + 发布 tag"的最小纪律，才能支撑方向 11 的版本管理。
2. 推荐单人模型：**main（永远可跑）+ feature/实验分支 + 发布 tag（v0.1…）+ paper 分支（论文与代码同步）**；配合 Conventional Commits 让历史可读。
3. 对审稿人：一个干净的 Git 历史 + 带 tag 的 release + 可复现 `git clone && make` 是 artifact 评测（方向 05）的硬门槛；凌乱仓库会被直接打"不可复现"。

## 精确数字与案例
- **分支模型**：`main`（CI 绿）+ `dev`（集成）+ `exp/xxx`（实验，可弃）+ `paper-2027`（论文配套代码冻结）。QueYi 当前 48 卡增长应在 `dev` 上，稳定后合 `main` 并打 tag。
- **tag 规范**：`git tag -a v0.3 -m "48 cards, core mutation 97.3%"`；与方向 11 的论文版本一一对应。
- **Conventional Commits**：`feat:`, `fix:`, `docs:`, `test:`, `chore:`；QueYi 提交如 `test: add 15 re-injection fixtures`。
- **案例**：顶会 artifact 评测要求"一条命令复现"；Git tag + `README` 的 `git checkout v0.3 && ./run_benchmark.sh` 是标配。
- **发布**：GitHub Releases 附预编译二进制 + 校验和；Zenodo/software heritage 存档拿 DOI（方向 57/99）。

## 对阙疑的 3 条具体行动
1. **建分支纪律**：立即把 QueYi 改为 `main`(稳定)+`dev`(增长)+`paper-2027`(冻结)；48 卡增长在 dev，合 main 即打 tag。
2. **每版打 tag + Release**：v0.3 时 GitHub Release 附 `run_benchmark.sh` + 校验和，供 reviewer 一键复现 0.59ms/卡。
3. **论文分支冻结**：投稿前从 v0.4 切 `paper-2027` 分支并冻结，rebuttal 期间只在该分支补，避免 corpus 漂移导致数字对不上（方向 04）。

## 盲区（诚实标注）
- "一条命令复现"若 QueYi 当前需复杂环境（特定编译器/依赖），需先容器化（方向 26 CI 含 Docker）才能满足 artifact 评测。
- 单人项目常忽略 `CHANGELOG`；QueYi 应补 `CHANGELOG.md` 记录每 tag 变更。
- 若历史已混乱（全在 main），应现在 `git tag` 当前为 v0.2 并从此规范，不必重写历史。

## 来源
- [1] Git Branching — https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
- [2] Conventional Commits — https://www.conventionalcommits.org/
- [3] GitHub Releases — https://docs.github.com/en/repositories/releasing-projects-on-github
- [4] Zenodo 存档 — https://zenodo.org/
