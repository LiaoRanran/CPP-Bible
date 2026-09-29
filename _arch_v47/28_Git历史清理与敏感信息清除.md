# 方向 28：Git 历史清理与敏感信息清除（匿名化与防泄露的底层操作）

## 核心结论

1. **GitHub 官方已弃用 `git filter-branch`，明确推荐 `git filter-repo` 作为重写历史的唯一首选工具；重写历史是"双盲匿名"的底层保障（擦除 `git log` 里的 author email/name），也是"防泄露"的兜底（删掉误提交的密钥/大文件）。** GitHub 文档（Removing sensitive data from a repository）逐字建议：用 *"tools such as git-filter-repo"* 更改历史；并强调 *"重写历史记录需要与所有协作者协调，并且会在所有协作者的仓库中重写历史"*。对阙疑（单人项目，无协作者协调负担）而言，filter-repo 是最干净的匿名化手段——它不仅能改文件内容，还能用 `--mailmap` 把 `author.email` 整体改写为匿名占位（方向 19 的"身份面第 4 类"）。

2. **清除敏感信息有两条主力命令：`--replace-text`（按字符串/正则批量替换文件内容，如密钥、邮箱）与 `--mailmap`（重写提交者身份，不影响文件内容）。** git-filter-repo 官方能力：① `--replace-text expressions.txt` 把文件中匹配的文本替换为 `***REMOVED***`（常用于 AWS key、`.env` 里的 token）；② `--mailmap mailmap.txt` 把 `Old Name <old@email>` 映射成 `New Name <new@email>`，重写全部 commit 的 author/committer。**对阙疑的匿名化**：用 mailmap 把真实邮箱 `queyi@ahtu.edu.cn` 映射到 `anon@anonymous.4open.science`，一次性重写全部历史，使 `git log` 不再泄露身份。

3. **BFG Repo-Cleaner 是 filter-repo 之外更快的备选（Scala 写，专为"删大文件/删密码"优化），但 filter-repo 更灵活、是 GitHub 官方首选；两者都要求"先备份、再强制推送、再让协作者重新 clone"。** BFG 官方（rtyley.github.io/bfg-repo-cleaner）说明：*"Removes large or troublesome blobs like git-filter-branch does, but faster"*，且第一步是 *"First clone a fresh copy of your repo, using the --mirror flag … make a backup of it"*。关键流程共识（GitHub + BFG）：① 备份；② 用工具重写；③ `git push --force` 到远端；④ **所有协作者必须删旧克隆、重新 clone**（旧历史仍在他们本地）；⑤ 清理 GitHub 端的缓存引用（Protection/PR/forks）。阙疑虽单人，但匿名镜像基于 GitHub 仓库，强制推送后镜像需重新生成。

---

## 精确数字与案例

### 一、GitHub 官方流程（逐字口径）

来自 GitHub Docs *Removing sensitive data from a repository*：

| 步骤 | 官方要点 | 阙疑对应 |
|---|---|---|
| 适用工具 | *"tools such as git-filter-repo"*（明确替代 filter-branch） | 用 filter-repo |
| 历史重写代价 | *"重写历史记录需要与所有协作者协调 … 在所有协作者仓库中重写历史"* | 单人项目无此负担 |
| 事后清理 | 用 filter-repo 删除敏感数据并 push 后，"必须再采取几步才能完全清除" | 强制 push + 重新克隆镜像 |
| 大文件 | 误提交的大文件需用 filter-repo 或 BFG 从所有分支/标签清除 | 清理 227 项工作树漂移（方向 16） |

**GitHub 明确警告**：即使重写了历史，敏感数据若曾公开，**应视为已泄露、立即轮换凭证**（密钥作废），因为 forks/PR/缓存可能已留存副本。对阙疑：若历史里从未提交过真实密钥（仅邮箱/学校名），风险较低，但仍需按匿名化标准处理。

### 二、git filter-repo 两条主力命令实操

**场景 A：清除误提交的文件/字符串（如 `.env`、`@ahtu.edu.cn` 出现在历史文件里）**
```
git filter-repo --replace-text expressions.txt
# expressions.txt 内容示例：
# ahtu.edu.cn==>REMOVED
# password123==>REMOVED
```
filter-repo 会把匹配文本替换为 `***REMOVED***`（默认），保留文件结构。注意：它作用于**所有分支与标签**的历史。

**场景 B：重写提交者身份（匿名化核心）**
```
echo "Queyi Real <queyi@ahtu.edu.cn> => Anon Queyi <anon@anonymous.4open.science>" > mailmap.txt
git filter-repo --mailmap mailmap.txt
```
这会把全部 commit 的 `author`/`committer` 改为匿名占位。**这是方向 19 匿名化的"历史层"保障**——anonymous.4open.science 镜像只剥显示名，不剥 `git log` 的 email 字段。

**场景 C：删除整个文件（如误提交的凭据文件）**
```
git filter-repo --path credentials.json --invert-paths
```

### 三、BFG Repo-Cleaner 对比

| 维度 | git filter-repo | BFG Repo-Cleaner |
|---|---|---|
| 官方地位 | GitHub 首选推荐 | 备选（更快） |
| 语言 | Python | Scala/JVM |
| 核心用途 | 灵活重写（内容+身份+路径） | 专删大文件/密码（快） |
| 典型命令 | `--replace-text`/`--mailmap`/`--path` | `bfg --delete-files credentials.json` / `bfg --replace-text` |
| 第一步 | 备份 | `git clone --mirror`（裸仓库）+ 备份 |
| 速度 | 快 | 更快（专为 blob 清理优化） |

BFG 官方教程强调：*"This is a bare repo … make a backup of it to ensure you don't lose data"*——**两个工具都要求先备份**，这是重写历史不可逆性的体现。

### 四、重写后的"收尾四步"（决定匿名化是否真的干净）

GitHub 与 BFG 共同指出的收尾：

1. **强制推送**：`git push --force --all` 与 `git push --force --tags`（filter-repo 默认已帮你设好，但需确认远端接受 force）。
2. **协作者重克隆**：所有旧克隆作废，必须删掉重新 `git clone`——否则旧历史（含敏感数据）仍在本地。
3. **清理 GitHub 缓存**：PR、forks、issue 附件、Actions 缓存可能仍含旧数据，需逐一检查/删。
4. **重新生成匿名镜像**：anonymous.4open.science 的镜像基于特定 commit，历史重写后必须重新生成链接（方向 19）。

**对阙疑的具体风险点**：227 项工作树漂移（方向 16）若部分已被 commit 进历史，重写时要用 `--invert-paths` 或 `--replace-text` 一并清理；本机 sanitizer 缺失等"硬伤"信息若曾写进 commit message，也会被 reviewer 看到——应在 `--replace-text` 里一并脱敏（如把学校名替换）。

### 五、不可逆性警告与"孤儿分支"替代方案

重写历史**不可逆**：一旦 force push，旧 commit 在远端消失（虽可在 reflog/备份找回一段时间）。另有"孤儿分支"方案（新建 `git checkout --orphan clean && git commit`）可保留工作区内容但丢弃全部历史——适合"不想暴露任何提交记录"的极端匿名需求，但会丢失 contributorship 证据（对学术贡献证明不利）。**阙疑建议用 filter-repo 的 mailmap 改写（保留开发时间线但匿名化身份），而非孤儿分支（丢失时间线）**——因为论文需要展示"持续开发"的可信度，完全无历史反而可疑。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前用 `git filter-repo --mailmap` 把全部历史的 author/committer 改为匿名占位，并 `git filter-repo --replace-text` 清除历史文件里的 `@ahtu.edu.cn`、学校名、任何疑似凭据字符串。** 具体：写 `mailmap.txt`（`Real Name <real@ahtu.edu.cn> => Anon <anon@anonymous.4open.science>`）、写 `expressions.txt`（逐行 `ahtu.edu.cn==>REMOVED`、学校拼音 `hefei==>REMOVED` 等）；先 `cp -r repo repo.bak` 备份；执行两条命令；`git push --force --all --tags`。理由：anonymous.4open.science 只剥 GitHub 用户名，不剥 `git log` 的 email/提交信息，这是方向 19 自查清单第 4 类的真正落地。

2. **2026-12 同步清理 227 项工作树漂移中已被误 commit 的文件（见方向 16），并核查本机是否曾把 sanitizer 报错信息/个人路径写进 commit message 或 `.env` 类文件。** 用 `git log --all -p -S 'ahtu'` 与 `git log --all --grep='sanitizer'` 全文搜历史，把命中的 commit 用 `--replace-text`/重新改写处理。** 重写后强制推送，并通知（若有）任何协作者重克隆。理由：历史里的学校名/路径是双盲匿名最易遗漏的盲区（提交信息不显示于 GitHub UI 但可由 `git log` 看到）。

3. **2027-01 前把"重写后的干净仓库"作为匿名镜像的唯一源，并在 `research/28_git_history.md` 记录备份 sha 与命令序列；camera-ready 阶段如需恢复真实身份，用新的 mailmap 再跑一次（保留旧备份以便回滚）。** 关键：备份目录 `repo.bak` 必须**不进**匿名镜像、不放公开处（否则备份含真实身份等于白做）。理由：重写不可逆，备份是唯一种子；且录用后可能需要在保留开发时间线的前提下回填真实作者（用新 mailmap 改写比孤儿分支更稳妥）。

---

## 盲区（诚实标注）

- **GitHub 文档的逐字引文（"tools such as git-filter-repo" / "重写历史记录需要…协调"）来自检索摘要**，未逐字打开正文核对完整段落；提交前建议 WebFetch 复核其最新步骤（尤其 force push 后的缓存清理细节）。
- **`git filter-repo` 的 `--replace-text` 默认替换词是 `***REMOVED***`（本组引用），但具体默认标记是否随版本变化未逐字核实**（仅从多份教程一致表述推断）。
- **BFG 的"更快"是相对 filter-branch 还是也包括 filter-repo 未量化**（BFG 官方只说比 filter-branch 快），本组表格写"更快"指其相对 filter-branch 的定位，filter-repo 与 BFG 的速度对比未实测。
- **未核实**：NeurIPS/匿名镜像是否会对"重写过历史的仓库"做异常检测（如 commit 时间突变）。单人项目重写在匿名期属正常操作，但无官方口径。
- **"227 项工作树漂移中是否有文件已被 commit"未实际核查**（方向 16 的待办），若全部漂移都未 commit，则本方向第 2 条行动可简化。
- **孤儿分支方案对"学术贡献时间线证明"的利弊是本组推断**，无引用支撑；实际会议对"无历史仓库"的接受度未知。
- **未核实**：git filter-repo 是否处理 `committer` 与 `author` 之外的 `tagger`（标签签名者）身份——若用了带签名的 tag，tagger email 也可能泄露，需额外 `--replace-text` 或 tag 重写。

---

## 来源

1. Removing sensitive data from a repository — GitHub Docs — https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository — 逐字：*"tools such as git-filter-repo"*；*"重写历史记录需要与所有协作者协调"*；force push 后需额外清理 — GitHub — 持续更新
2. git-filter-repo (official) — https://github.com/newren/git-filter-repo — `--replace-text` / `--mailmap` / `--path --invert-paths` 用法；替代 filter-branch — Elijah Newren — 持续更新
3. BFG Repo-Cleaner — https://rtyley.github.io/bfg-repo-cleaner/ — 逐字：*"Removes large or troublesome blobs like git-filter-branch does, but faster"*；*"First clone … using the --mirror flag … make a backup"* — Roberto Tyley — 持续更新
4. BFG Repo-Cleaner (GitHub) — https://github.com/rtyley/bfg-repo-cleaner — Scala 实现；删大文件/密码 — Roberto Tyley — 2026-07-18
5. 使用 git filter-repo 统一提交作者信息 — https://jishuzhan.net/article/2008518000816209922 — mailmap 以邮箱为唯一判据重写身份、常见逻辑问题 — 技术博客 — 2026-01-06
6. 清理 repo 中敏感信息（完整流程）— https://blog.mrchi.cc/posts/removing-sensitive-data-from-repo/ — 本地重写 + 远端清理 + 团队协同流程 — 2025-10-14
7. Anonymous GitHub — https://anonymous.4open.science/ — 镜像只剥显示名不剥 git log email（方向 19 已引）— 4open.science — 持续更新
8. Git 提交者信息修正：从 amend 到 filter-repo 的 5 个脚本 — https://devpress.csdn.net/v1/article/detail/94082820 — 批量 filter-repo 实战 — 2026-07-11
9. orphan branch 方案（历史隔离）— https://wenku.csdn.net/column/il7nwsc0svs — 孤儿分支 vs filter-branch vs BFG 三方案对比 — 2026-07-12（**作为"极端匿名备选"参考，非推荐**）
10. GitHub Docs（中文）：从存储库中删除敏感数据 — https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository — 同上英文文档的中文版 — GitHub — 持续更新
