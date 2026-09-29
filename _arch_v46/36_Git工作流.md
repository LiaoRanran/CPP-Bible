# 方向 36：Git 工作流（单人项目怎么用 branch / release / tag）

> 调研时间：2026-09-29（GMT+8）｜联网搜索 13 次（另有 1 次因服务端超时失败）+ 3 次 WebFetch 读一手原文
> 锚点项目：阙疑 / queyi（`C:/CodeLearnling/note/note/C++/CPP-Bible/`）
> 前置口径（取自 `00_仓库扫描.md`）：分支 `master`；工作树 **227 项漂移**（203 M + 24 ??）；`_auto/status.json` 的 `active_batch=660` 落后于实际 **665**；历史提交中 **660 批曾 `push` 走 `--no-verify`**。

---

## 核心结论

1. **单人项目应当采用 trunk-based development（主干开发），但必须配"每日合入 + 3 条以内活动分支 + 无 code freeze"三条 DORA 量化判据**——DORA 的能力页原文明确给出这三条目标值，而不是笼统的"少开分支"。
2. **commit 规范用 Conventional Commits 1.0.0 是"零成本、可被机器校验"的选择**：它只有 **16 条 RFC 2119 规范条款**，且 `feat`→MINOR、`fix`→PATCH、`BREAKING CHANGE`→MAJOR 三条映射与 SemVer 2.0.0 一一对应，可以支撑自动生成 CHANGELOG 和自动定版本号。
3. **阙疑当前最紧迫的 Git 问题不是"用哪种分支模型"，而是"227 项工作树漂移 + `--no-verify` 绕过钩子"**：这两件事直接破坏了"可被独立验收"这一核心主张——如果连自己的工作树都不可复现，独立验收者 clone 下来的东西与论文数字就对不上。

---

## 精确数字与案例

### 1. trunk-based vs git-flow：不是风格之争，是有量化判据的

DORA（Google Cloud 的 DevOps 研究项目）在其能力页 `https://dora.dev/capabilities/trunk-based-development/` 中给出了三种版本控制工作模式的定义与**可测量目标**：

- **feature branch 模式**：从 trunk 拉分支、隔离开发数天到数周，完成后合回。原文描述其代价是"bigger and more complex merge events"、"additional stabilizing efforts and **code lock / code freeze** periods"。
- **trunk-based 模式**：每位开发者把自己的工作拆成小批量，**至少每天合入 trunk 一次（也可能一天多次）**；分支生命周期"typically last no more than a few hours"；当发布频率达到每天多次时，**release branch 根本不需要**，直接从 trunk 部署。
- **DORA 基于 2016 / 2017 报告的原始数据分析给出三条目标值**（原文措辞，非我概括）：
  1. **"Have three or fewer active branches in the application's code repository."**（应用仓库活动分支 ≤ 3 条）
  2. **"Merge branches to trunk at least once a day."**（每天至少合入一次）
  3. **"Don't have code freezes and don't have integration phases."**（不做代码冻结、不设集成阶段）

这三条对单人项目极其友好：**单人项目天然只有 0–1 条活动分支**，天然满足第 1 条；难点在第 2 条（要每天有可提交的东西）和第 3 条（不要积压成"大爆炸式提交"）。

git-flow 的问题在于它假设"多人 + 多环境 + 有 QA 阶段"。git-flow 定义了 `feature/*`、`develop`、`release/*`、`hotfix/*`、`master` 五类长期/短期分支，对单人项目是纯粹的管理税：`develop` 和 `master` 会长期分叉，`release/*` 分支只有一个人合，收益为零、成本是每次发布要做两次合并。**阙疑目前直接 `master` 单分支，方向是对的**，但缺少量化纪律。

### 2. 227 项工作树漂移：这是 trunk-based 的反面教材

`00_仓库扫描.md` §2 实测：`git status --porcelain` 共 **227** 条 = **203 M + 24 ??**。其中已修改集中在 `_adv_v80/probes/*`（33 个探针文件）+ `_auto/status.json`；未跟踪项包含 `_arch_v35/`、`_arch_v37/`–`_arch_v45/` 各目录及 `_arch_v36_brief.md` … `_arch_v46_brief.md`。

DORA 原文对"不跑提交前测试"的批评可以直接套用：

> "**Not running automated tests before committing code.** In order to ensure trunk is kept in a working state, it's essential that tests are run against code changes before commit."

227 项漂移意味着：**任何人（包括三个月后的作者自己）`git clone` 出来的仓库，与产生论文数字 `holdout 66.7%` / `corpus 43.8%` 的那个状态不是同一个状态**。这在 NeurIPS E&D 的 "reproducibility" 审稿维度上是硬伤。

更糟的是历史记录：`00_仓库扫描.md` §1 的 `git log` 里，提交 `a18fb201 660：验收报告登记 push 走 --no-verify（既有漂移非本批引入）` 明确记载了 `--no-verify` 绕过钩子。`--no-verify`（`-n`）会跳过 `pre-commit` 与 `commit-msg` 钩子；`git push --no-verify` 会跳过 `pre-push`。**一旦这个口子被打开，钩子就退化成"建议"而不是"门禁"**——这与方向 39 的 fail-closed 原则直接冲突。

### 3. Conventional Commits 1.0.0：16 条规则，可机械校验

一手来源 `https://www.conventionalcommits.org/en/v1.0.0/`（WebFetch 读原文）。结构：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

16 条规范条款（RFC 2119，节选与阙疑最相关的）：

- **01**：提交**必须（MUST）**以 type 开头（名词，如 `feat`、`fix`），后跟可选 scope、可选 `!`、**必需的终止冒号加空格**。
- **02/03**：`feat` **必须**用于新增功能；`fix` **必须**用于修 bug。
- **05**：描述**必须**紧跟冒号+空格，是简短摘要。
- **09**：footer token **必须**用 `-` 代替空格（如 `Acked-by`）；`BREAKING CHANGE` 是唯一例外。
- **11/12/13**：破坏性变更**必须**在 type/scope 前缀中用 `!` 标注，或在 footer 中写大写 `BREAKING CHANGE: `。
- **15**：除 `BREAKING CHANGE` 必须大写外，规范实现者**不得**把各单元视为大小写敏感。

与 SemVer 的映射（原文 FAQ 直引）：`fix` → `PATCH`，`feat` → `MINOR`，含 `BREAKING CHANGE`（任意 type）→ `MAJOR`。

规范允许扩展 type，官方推荐（基于 Angular convention）包括 `build:`、`chore:`、`ci:`、`docs:`、`style:`、`refactor:`、`perf:`、`test:`。阙疑现有提交信息形如 `665 E/F/G/H：轨迹 5→10、论文 v0.3…`，属于"批次号 + 中文摘要"，**机器不可解析**（无法自动定版本号、无法自动生成 CHANGELOG），但人读性尚可。建议保留批次号作为 scope：`feat(665): 轨迹 5→10 + 论文 v0.3`。

### 4. SemVer 2.0.0 与 tag 选择

`https://semver.org/`（含官方简体中文版 `https://semver.org/lang/zh-CN/`）规定版本号 `MAJOR.MINOR.PATCH`：MAJOR 是不兼容 API 变更，MINOR 是向后兼容的功能新增，PATCH 是向后兼容的缺陷修复。规范还有一条常被忽略的条款：**"一旦发现破坏了语义化版本规范，立刻修问题并发布一个新的 MINOR 版本"**——即版本号一旦发出不得原地篡改。

tag 的两种形态（多篇教程一致，如 `https://qadrlabs.com/post/git-tags-explained-annotated-vs-lightweight-versioning-and-remote-tags`）：

- **lightweight tag**：`git tag v1.0.0`，只是指向某个 commit 的引用，无额外对象。
- **annotated tag**：`git tag -a v1.0.0 -m "release"`，生成独立 tag 对象，含 tagger 名、邮箱、时间戳、消息，可被 GPG 签名。

**结论：release 必须用 annotated tag（甚至签名 tag）**，因为它携带"谁在何时为什么打了这个版本"的元数据，且 `git describe` 在 annotated tag 上才能给出稳定的 `v1.0.0-3-gabc1234` 形式描述。lightweight tag 适合临时的本地标记。

推送 tag 必须显式：`git push origin v1.0.0` 或 `git push origin --tags`（默认 `git push` **不会**推 tag）。

### 5. pre-push 钩子：单人项目的最后一道闸

`git` 的钩子位于 `.git/hooks/`，默认全部是 `.sample` 后缀（不生效）。`pre-push` 接收两个参数：`$1` = remote name，`$2` = remote URL；stdin 传入形如 `<local ref> <local sha> <remote ref> <remote sha>` 的行。**钩子以非零退出码结束即中止 push**。

最小可用 `pre-push`（放 `.git/hooks/pre-push`，`chmod +x`）：

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "[pre-push] 运行 gate 自检…"
python tools/gate_engine.py --check || { echo "❌ gate --check 失败，push 已中止"; exit 1; }
echo "[pre-push] ✅ 通过"
```

关键工程点（多篇 pre-push 教程如 `https://www.slingacademy.com/article/git-pre-push-hook-a-practical-guide-with-examples/` 与 `https://www.geekcoder.org/blog/git-pre-push-hook/` 都强调）：

- `.git/hooks/` **不进版本控制**，必须配套一个 `hooks/` 目录 + `git config core.hooksPath hooks`，否则 clone 后钩子丢失。
- `pre-push` 里要判断"是否推送到受保护分支"（读 stdin 的 remote ref），只在推 `master` 时跑重测试。
- **禁止 `--no-verify`**：可用 `git config --global alias.push 'push'` 之外的手段无强制力，唯一可靠的是"CI 侧也跑同样的检查"（见方向 37），让本地绕过不产生收益。

Node 生态的对应物是 `husky`（管理钩子安装）+ `lint-staged`（只对暂存文件跑 linter）；Python 生态是 `pre-commit` 框架（`https://pre-commit.com/`），它用一个 `.pre-commit-config.yaml` 声明钩子、自动管理版本、只对改动文件运行。对阙疑（Python 内核 + C++ 夹具）建议直接用 `pre-commit` 而非手写钩子。

### 6. 原子提交与可回滚：`bisect` 是原子提交的真正回报

原子提交的定义（`https://dev.to/playfulprogramming/the-power-of-atomic-commits-in-git-how-and-why-to-do-it-54mn`、`https://www.compilenrun.com/docs/devops/git/git-best-practices/git-atomic-commits/` 一致）：**每个 commit 只做一件事、能独立编译、能独立通过测试、能独立回滚**。Conventional Commits 官方 FAQ 也给了同向建议：当一个改动同时符合多个 type 时，"**Go back and make multiple commits whenever possible.**"

原子提交换来的能力是 `git bisect`。`git bisect run <script>` 可以全自动二分：

```bash
git bisect start
git bisect bad v0.3.0
git bisect good v0.2.0
git bisect run python tools/gate_engine.py --check
```

脚本退出码语义（`https://blog.csdn.net/kqzodj_214/article/details/162327730`）：`0` = good，`1–127`（除 125）= bad，**`125` = 跳过该 commit**（如编译不过或依赖缺失）。若提交是"一次改 50 个文件的大爆炸"，bisect 定位到的那一个 commit 仍然无法给出根因——**原子提交是 bisect 有效的前提**。

`reset` vs `revert`（`https://www.geekcoder.org/blog/git-hui-gun-ming-ling-reset-revert-de-qu-bie/`）：

- `git reset --hard <sha>`：**移动分支指针**，重写历史。仅限未推送的本地提交。`--soft`（只动 HEAD）、`--mixed`（默认，动 HEAD + 暂存区）、`--hard`（三者全动）。
- `git revert <sha>`：**生成一个反向提交**，历史只增不减。已推送的提交必须用 revert。

对阙疑的映射：**已推送到 `origin/master` 的提交一律用 `git revert`**（符合其 append-only 的哲学——哈希链账本也是只增不减）；未推送的本地提交可以用 `reset`。

### 7. `git worktree`：单人并行开发的低成本工具

`git worktree` 自 **Git 2.6（2015-09-28 发布）**引入（`https://juejin.cn/post/7614026189313835060` 等多篇一致）。它允许**同一个仓库对象库**挂载多个工作目录，每个目录检出不同分支，共享 `.git`，无需重复 clone。

```bash
git worktree add ../queyi-hotfix v0.3.0
git worktree list
git worktree remove ../queyi-hotfix
```

对阙疑的用途：**在 `_arch_v46/` 调研进行中，仍能并行修 665 批的 bug 而不污染工作树**——这正是解决 227 项漂移的一个具体手段：调研产物、实验产物、论文产物各自一个 worktree，互不干扰。

### 8. release 自动化（与方向 37 衔接）

GitHub Actions 可在 tag push 时自动建 Release，典型触发：

```yaml
on:
  push:
    tags: ['v*.*.*']
```

`https://github.com/marketplace/actions/create-tag-release` 是 Marketplace 上的封装 Action；更稳的是直接用官方 `gh` CLI 或 `softprops/action-gh-release`。关键坑：**`GITHUB_TOKEN` 默认权限不足以建 Release，需要 workflow 里声明 `permissions: contents: write`**（详见方向 37）。

### 9. 三种分支模型的正面对比（给阙疑的选型依据）

把三篇中文对比文章（`https://xtechtools.com/learn/git-workflow-2026/`、`https://juejin.cn/post/7680938642576392226`、`https://zzqdeco.github.io/blog/git-branching-workflows/`）的结论收敛成一张表：

| 维度 | Git Flow | GitHub Flow | Trunk-Based |
|---|---|---|---|
| 长期分支数 | 2（`master` + `develop`） | 1（`main`） | 1（`trunk`/`main`） |
| 短期分支 | `feature/*`、`release/*`、`hotfix/*` | `feature/*` | 可选、**生命周期以小时计** |
| 发布方式 | 从 `release/*` 发布 | 从 `main` 发布 | 从 trunk 发布，高频时**不需要 release 分支** |
| 合并频率 | 数天到数周一次 | 每个 PR 一次 | **至少每天一次** |
| 是否需 code freeze | 是（`release/*` 稳定期） | 否 | **明确禁止** |
| 适用规模 | 多人 + 多环境 + 有 QA | 小团队 + 持续部署 | 任何规模，**但要求测试自动化到位** |
| 单人项目成本 | **高**（两次合并、两条长期分支） | 中（PR 流程对单人冗余） | **低**（直接提交 trunk） |

`https://juejin.cn/post/7680938642576392226` 对 trunk-based 的一句话概括很准："所有人往 main（trunk）上提交代码，**不搞长期存在的开发分支**"。这正是阙疑现状（单 `master`）——**方向已经对了，缺的只是量化纪律**。

**单人项目里 GitHub Flow 的隐性成本**：GitHub Flow 要求"每个改动开一个分支 + 开 PR + 等 CI + 合并"。对单人项目，PR 的评审者是作者本人，等于自己给自己写检查清单——**只有在需要 CI 在合并前跑门禁时才有价值**。阙疑的正确组合是：**trunk-based（直接推 master）+ CI 在 push 后跑门禁**，而不是"开分支 + 开 PR"。

### 10. CHANGELOG 自动生成与 `--no-verify` 的真实代价

Conventional Commits 官方列出的第一项收益就是 "**Automatically generating CHANGELOGs**"，第二项是 "Automatically determining a semantic version bump"。对应工具链（`https://blog.gitcode.com/424450f82b94d6c95830cd70e5c98857.html`）：

- **`commitlint` + `@commitlint/config-conventional`**：校验 commit message 是否符合 1.0.0 规范。官方规范第 4 条明确点名了这个配置（"for example [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)"），并给出它推荐的 type 列表：`build`、`chore`、`ci`、`docs`、`style`、`refactor`、`perf`、`test`。
- **`standard-version` / `semantic-release` / `conventional-changelog`**：根据 commit 历史自动生成 CHANGELOG 并自动升版本号。
- **`conventional-pre-commit`**：把校验放进 `pre-commit` 阶段。

**为什么 `--no-verify` 的代价被严重低估**：它跳过的是 `pre-commit`、`commit-msg`、`pre-push` **三个**钩子。对阙疑而言：

1. 跳过 `commit-msg` 校验 → commit 历史变成不可解析的批次号，CHANGELOG 与版本号自动生成**永久失效**（历史一旦写坏无法回溯修复，除非 `rebase` 重写已推送历史，而那会破坏"append-only"哲学）。
2. 跳过 `pre-push` 的 `--check` → **未通过门禁的代码进了 `origin/master`**，而论文声称的所有数字都锚定在 master 的某个状态上。
3. 一旦有一次"绕过成功"，后续每次 CI 变红时都会有人（包括作者自己）想"再绕一次"——**门禁的威慑力是不可逆地衰减的**。

**替代方案**（既保效率又保门禁）：把重检查放进 `pre-push` 而不是 `pre-commit`（`pre-commit` 只跑快速 lint），并让 `pre-push` 只对 `master` 生效。这样日常 WIP 提交不被阻塞，但**推送**必须过关。

---

## 对阙疑的 3 条具体行动

**行动 1：把 227 项漂移"分类固化"，而不是一次性 `git add -A` 提交。**
具体：在 `_arch_v46/` 之外**不动任何文件**，但产出一份 `_arch_v46/36_漂移分类建议.md`（本方向附带的建议清单，非仓库文件），把 203 M + 24 ?? 分成四类：(a) `_arch_v35`–`_arch_v45` 调研产物 → 建议加进 `.gitignore` 或单独 tag 归档；(b) `_adv_v80/probes/*` 33 个探针 → 属于实验产物，应进 `data/` 或加 ignore；(c) `_auto/status.json` 元状态漂移 → 必须提交，因为它本身就是论文 Threats to Validity 的实证；(d) 其余批次产物 → 按批次逐个原子提交。**验收标准：`git status --porcelain | wc -l` 从 227 降到 ≤ 10**，且每个残留项都有明确归属说明。

**行动 2：建立 `.pre-commit-config.yaml` + `core.hooksPath`，并把 `--no-verify` 写进"禁止清单"。**
具体：在仓库根新增 `.pre-commit-config.yaml`，至少三条钩子：`conventional-pre-commit`（校验 commit message 符合 1.0.0）、`trailing-whitespace`/`end-of-file-fixer`、以及自定义 `python tools/gate_engine.py --check`。然后 `git config core.hooksPath .githooks` 并把钩子脚本提交进 `.githooks/`（`.git/hooks` 不进版本控制）。**同时**：既然本地钩子可被 `--no-verify` 绕过，必须在方向 37 的 CI 里跑**同一套 `--check`**，让绕过的收益为零。验收标准：CI 与本地跑的是同一个命令字符串。

**行动 3：给 665 批（及后续批）打 annotated tag，并让 `git describe` 成为论文里的"版本指纹"。**
具体：`git tag -a v0.3.0-665 -m "holdout 30 / corpus 40 / 论文 v0.3"` + `git push origin v0.3.0-665`。之后论文 `research/paper_v0.3.md` 的 reproducibility 段应写清"所有数字对应 `git describe --tags` 输出的 `v0.3.0-665` 状态"。**理由**：DORA 判据第 2 条要求"每天至少合入一次"，tag 是把"某个可复算状态"钉死的唯一轻量手段；同时 annotated tag 自带 tagger 与时间戳，可对抗"元状态不可信"（`_auto/status.json` 落后 665 就是这个病的现成案例）。

---

## 盲区（诚实标注）

1. **DORA 2024 报告正文的精确百分比未逐字核对**。我读到的是一手能力页（`dora.dev/capabilities/trunk-based-development/`）与 2024 报告落地页（`dora.dev/research/2024/dora-report/`）的**关键发现摘要**；摘要里**没有**给出 elite/high/medium/low 四档的 deployment frequency / change failure rate 具体百分比。搜索结果中 `https://www.libertify.com/interactive-library/state-of-devops-2024-dora/` 声称"127x faster change lead time、182x more deployments per year、8x lower change failure rate"，但这些倍数更接近 2018 报告口径，**我未能下载 2024 报告 PDF 逐字核实，故不作为精确数字引用**。
2. **"三名以内活动分支"是 DORA 对 2016/2017 数据的分析结论**，能力页明确写了出处年份；它是否在 2024/2025 数据上仍成立，**未核实**。
3. **阙疑的 227 项漂移未逐项归类**（沿用 `00_仓库扫描.md` 的口径），本方向的四分类是**建议方案**，不是我核实过的实际分布。
4. **`git worktree` 的确切引入版本**：多篇中文教程称 Git 2.6 引入，我**未从 git 官方 release notes 逐字核对**。
5. **Conventional Commits 条款条数**：官方页面编号到 **16**，但第三方中文解读有的写"15 条"、有的写"16 条"；我按官方页面的 01–16 计数，**以官方页为准**。
6. **GitHub Actions 的 `create-tag-release` Action 与 `permissions: contents: write` 的关系**未在本方向实测，留待方向 37 验证。

---

## 来源

1. DORA, *Capabilities: Trunk-based development* — https://dora.dev/capabilities/trunk-based-development/ （一手；含"three or fewer active branches""merge at least once a day""no code freezes"三条目标值与 2016/2017 报告出处）
2. DORA, *Accelerate State of DevOps Report 2024* — https://dora.dev/research/2024/dora-report/ （一手；关键发现摘要 + 多语言 PDF 下载入口，含简体中文版）
3. Conventional Commits, *Conventional Commits 1.0.0* — https://www.conventionalcommits.org/en/v1.0.0/ （一手；16 条 RFC 2119 规范条款全文）
4. Semantic Versioning, *Semantic Versioning 2.0.0* — https://semver.org/ ；中文版 https://semver.org/lang/zh-CN/ （一手）
5. *Git Pre-Push Hook: A Practical Guide (with Examples)* — https://www.slingacademy.com/article/git-pre-push-hook-a-practical-guide-with-examples/ （2024-01-27）
6. *Git Pre-Push Hook 详解：从原理到实践* — https://www.geekcoder.org/blog/git-pre-push-hook/ （2026-08-22）
7. *Git Tags Explained: Annotated vs Lightweight, Versioning, and Remote Tags* — https://qadrlabs.com/post/git-tags-explained-annotated-vs-lightweight-versioning-and-remote-tags （2026-09-19）
8. *The Power of Atomic Commits in Git: How and Why to Do It* — https://dev.to/playfulprogramming/the-power-of-atomic-commits-in-git-how-and-why-to-do-it-54mn （2023-12-22）
9. *Git Atomic Commits* — https://www.compilenrun.com/docs/devops/git/git-best-practices/git-atomic-commits/ （2026-07-12）
10. *Git 回滚命令 reset、revert 的区别* — https://www.geekcoder.org/blog/git-hui-gun-ming-ling-reset-revert-de-qu-bie/ （2026-05-12）
11. *用 git bisect run 自动化定位引入 Bug 的提交* — https://blog.csdn.net/kqzodj_214/article/details/162327730 （2026-06-26；含退出码 125 语义）
12. *Git Worktree：多分支并行开发的利器* — https://juejin.cn/post/7614026189313835060 （2026-03-07；Git 2.6 引入说法）
13. *Husky vs lint-staged: Which Pre-commit Hook Tool is Better for 2025?* — https://toolhunt.cc/2026/07/husky-vs-lint-staged-which-pre-commit-hook-tool-is-better-for-2025/ （2026-07-28）
14. *Create Tag Release · Actions · GitHub Marketplace* — https://github.com/marketplace/actions/create-tag-release
15. 本仓库内部锚点：`_arch_v46/00_仓库扫描.md` §1（`git log`，含 `a18fb201 ... push 走 --no-verify`）、§2（227 项漂移）。
