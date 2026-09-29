# 方向 37：CI/CD 最小配置（GitHub Actions 三编译器矩阵）

> 调研时间：2026-09-29（GMT+8）｜联网搜索 10 次 + 5 次 WebFetch 读官方文档
> 锚点项目：阙疑 / queyi（Python 内核 `tools/gate_engine.py` 3826 行 + C++ 夹具 + 67 条规则）
> 关联：方向 36（pre-push 钩子本地绕过 → 必须由 CI 兜底）、方向 40（性能回归门禁）

---

## 核心结论

1. **阙疑的 CI 应当只有一个 workflow、三个 job，且必须在"公开仓库"上跑**：GitHub 官方文档明确"Use of the standard GitHub-hosted runners is free and unlimited on public repositories"，公开仓库的 Linux 4 核 16 GB runner 完全免费；而私有仓库 GitHub Free 每月只有 **2000 分钟**。把 `queyi` 仓库设为 public 是**零成本把 CI 从"稀缺资源"变成"无限资源"的唯一杠杆**。
2. **`if` 跳过（skipped）的 job 状态是 "Success"，即使它是 required check 也不会阻止合并**——这是官方文档原文的坑。所以"门禁"绝不能靠 `if` 跳过实现，必须靠"job 失败"实现。这一条直接决定阙疑 67 条规则 / 44 block 的 CI 该怎么摆。
3. **`actions/cache` 的缓存是"不可变 + 7 天未访问即删 + 每仓库 10 GB 硬上限 + 200 次上传/分钟限流"**，且缓存内容**不签名不校验**，低信任触发器（`pull_request_target` 等）只能只读。对阙疑而言，缓存只值得缓存 `pip` 依赖与 `ccache`，**绝不能在缓存里放 `.revealed` 标记或 holdout 数据**——否则独立验收者拿到的是被污染的缓存。

---

## 精确数字与案例

### 1. 免费额度：公开仓库无限，私有仓库 2000 分钟/月

一手来源 `https://docs.github.com/en/billing/concepts/product-billing/github-actions`（WebFetch 读原文）与 `https://docs.github.com/en/actions/reference/limits`：

| 计划 | 每月免费分钟 | 制品存储 | 缓存存储/仓库 |
|---|---|---|---|
| GitHub Free | **2,000** | **500 MB** | 10 GB |
| GitHub Pro | **3,000** | **1 GB** | 10 GB |
| GitHub Free for orgs | **2,000** | **500 MB** | 10 GB |
| GitHub Team | **3,000** | **2 GB** | 10 GB |
| GitHub Enterprise Cloud | **50,000** | **50 GB** | 10 GB |

标准托管运行器每分钟费率：Linux 1 核 `$0.002`、**Linux 2 核 `$0.006`**、Linux 2 核 arm64 `$0.005`、Windows 2 核 `$0.010`、**macOS 3/4 核 `$0.062`**。存储超额：制品 `$0.25/GB/月`，缓存 `$0.07/GB/月`。

**关键原文（公共仓库）**：standard GitHub-hosted runners 在**公共仓库上"free and unlimited"**；例外是 **larger runners 永远收费**（即使公共仓库、即使配额有剩）。GitHub Pages 与 Dependabot 也免费。

**对阙疑的算术**：一个"三编译器矩阵"（GCC + Clang + MSVC）每次跑约 3 个 job × 3–6 分钟。若为私有仓库、按 Linux 2 核 $0.006/分钟算，一天推 10 次 = 3 job × 5 min × 10 = 150 分钟/天 → 一个月约 **4,500 分钟**，**远超 GitHub Free 的 2,000 分钟**，必须付费。改为 public 仓库：**$0**。这不是省钱问题，是"能不能把 CI 设成每次 push 都跑"的问题。

### 2. Runner 硬件：公开仓库 4 核 16 GB，私有仓库 2 核 8 GB

一手来源 `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`（WebFetch 读原文）：

| 标签 | 公共仓库 | 私有仓库 | 存储 |
|---|---|---|---|
| `ubuntu-latest`（= `ubuntu-24.04` / `ubuntu-22.04` / `ubuntu-26.04`） | **4 CPU / 16 GB RAM** | **2 CPU / 8 GB RAM** | 14 GB SSD x64 |
| `windows-latest`（= `windows-2025` / `windows-2022`） | 4 CPU / 16 GB | 2 CPU / 8 GB | 14 GB SSD |
| `macos-latest`（arm64 M1） | **3 CPU / 7 GB RAM** | 3 CPU / 7 GB | 14 GB SSD |
| `ubuntu-slim`（单核容器） | 1 CPU / 5 GB | 1 CPU / 5 GB | 14 GB |

**重要差异**：同一个 `ubuntu-latest` 标签，公开仓库给 **4 核 16 GB**，私有仓库只给 **2 核 8 GB**——差了整整一倍。这意味着"公开 vs 私有"不仅影响钱，还直接影响三编译器矩阵的并行墙钟时间。

`ubuntu-slim` 是容器而非 VM，**job 超时上限只有 15 分钟**（其他标准 runner 是 6 小时），且不支持 Docker-in-Docker。

### 3. 超时与硬上限（容易踩的坑）

来自 `https://docs.github.com/en/actions/reference/limits`：

- **`timeout-minutes` 默认值 = 360**（6 小时）。第三方教程（`https://dev.to/suzukishunsuke/set-github-actions-timeout-minutes-1jkk`）原文吐槽："The default value of timeout-minutes is 360, but this is too long for most GitHub Actions jobs."——**卡死的 job 会白烧 6 小时额度**（私有仓库）或占着并发槽（公开仓库）。
- **job matrix 上限 = 256 jobs / 一次 workflow run**（官方文档原文："A job matrix can generate a maximum of 256 jobs per workflow run"）。
- **workflow 文件大小上限 = 500 KB**，超过则**不启动**。
- **一次 workflow run 最多 re-run 50 次**。
- **workflow run 总时长上限 35 天**（含等待审批）。
- **job 并发**：GitHub Free **20**、Pro **40**、Team **60**、Enterprise **500**（其中 macOS 最多 5）。
- **缓存限流**：上传 **200 次/分钟**、下载 **1500 次/分钟**、删除 **400 次/分钟**（每仓库）。
- `GITHUB_TOKEN` 限流 **1000 请求/小时/仓库**。

### 4. 矩阵（matrix）：三编译器的正确写法

一手语法来自 `https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations`：

```yaml
strategy:
  fail-fast: false          # 关键：一个编译器挂了，其他继续跑完
  max-parallel: 3
  matrix:
    include:
      - { os: ubuntu-latest, cxx: g++-14,   cc: gcc-14 }
      - { os: ubuntu-latest, cxx: clang++-18, cc: clang-18 }
      - { os: windows-latest, cxx: cl.exe,  cc: cl.exe }
    exclude: []             # 需要时剔除组合
```

`fail-fast` 默认是 **`true`**——默认行为是"一个 matrix 分支失败就取消其他所有分支"。对三编译器交叉验证场景这是错的：**你需要知道"是 GCC 特有还是三个都错"**，所以必须显式 `fail-fast: false`。同理 `continue-on-error: true` 可用于"允许实验性编译器失败但不阻断整体"。

### 5. 条件 job 与 `needs`：skipped 是 "Success" 的坑

一手来源 `https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions`（WebFetch 读原文）。官方原文警示：

> "Note: A job that is skipped will report its status as **'Success'**. It will **not** prevent a pull request from merging, **even if it is a required check**."

这对阙疑是致命设计点：如果写成

```yaml
gate-block-rules:
  if: ${{ contains(github.event.head_commit.message, 'release') }}
```

那么**非 release 提交时这个 job 显示绿色 Success**，分支保护形同虚设。正确做法：**门禁 job 永远运行，用退出码决定成败**（fail-closed，见方向 39）：

```yaml
- name: gate --check（必须失败即失败）
  run: python tools/gate_engine.py --check
```

`needs.<job>.result` 的取值是 `success` / `failure` / `cancelled` / `skipped`；`if: always()`、`if: failure()`、`if: success()` 是三个常用修饰。**默认语义**：前一个 step 失败后，后续 step 会被跳过（除 `if: always()`）。

### 6. 缓存：10 GB、7 天、不可变

一手来源 `https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching`（WebFetch 读原文）：

- **恢复顺序**：精确匹配 `key` → `key` 前缀匹配 → 按顺序尝试 `restore-keys`；当前分支全未命中则去**默认分支**重试。
- **不可变**：缓存一旦创建**无法修改**，只能换新 key 建新缓存。因此 key 里必须带 `hashFiles(...)`。
- **`key` 最大长度 512 字符**，超长直接失败。
- **驱逐**：**超过 7 天未被访问**的缓存被移除；仓库总量超过 **10 GB** 时按"最后访问日期最旧优先"删除。
- **作用域隔离**：只能恢复**当前分支**或**默认分支**的缓存；**子分支/兄弟分支的缓存不可见**；不同 tag 之间也不共享。
- **安全原文警示**："**Do not store any credentials or tokens in the cache paths.** Anyone with read access can create a pull request on a repository and access the contents of the cache."
- **投毒风险**：`pull_request_target`、`issue_comment`、`workflow_run` 这类低信任触发器**默认只有只读缓存权限**；显式写 `cache-mode: write` 会重新引入投毒风险。

`setup-python` 内置 pip 缓存，**比手写 `actions/cache` 更稳**：

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'          # 一行搞定
    cache-dependency-path: requirements-dev.txt
```

`setup-python` 的缓存 ADR（`https://github.com/actions/setup-python/blob/main/docs/adrs/0000-caching-dependencies.md`）说明其设计动机就是"和 `actions/cache` 一起用能显著加速依赖安装"。

### 7. Artifact：v4 是破坏性重写

一手来源 `https://github.com/actions/upload-artifact`（README）+ `https://deepwiki.com/actions/upload-artifact/4.1-key-changes`：**`upload-artifact@v4` 是后端架构的完全重写**，引入 **immutable artifacts（不可变制品）**。v3 → v4 的关键变化：

- 同一 workflow run 内**不能再用同一个 name 上传多次**（v3 允许追加），v4 会报错——需要改用 matrix 变量区分 name。
- v4 目前**不支持 GHES**，GHES 用户必须用 v3。
- 制品存储与 GitHub Packages **共享同一配额池**（Free 500 MB 很紧）。

**对阙疑的直接影响**：`gate_engine.py --check` 的输出 JSON、覆盖率报告、`--check` 日志都适合作为 artifact，但**必须给每次上传一个唯一 name**：

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: gate-report-${{ matrix.cxx }}-${{ github.run_id }}
    path: out/gate_report.json
    retention-days: 30
```

### 8. 并发控制：`concurrency` + `cancel-in-progress`

一手来源 `https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency`：

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

对单人项目这是**最有性价比的一行配置**：连推 5 次时，前 4 次的 CI 自动取消，只跑最后一次。注意 `cancel-in-progress` 可配表达式，例如只在 PR 上取消、在 `master` 上不取消：

```yaml
cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

注意限制：`concurrency` group 队列上限 **100 个 workflow run**。

### 9. 可直接抄的完整 YAML

以下为阙疑可用的最小三编译器 + 门禁配置（放在 `.github/workflows/ci.yml`）：

```yaml
name: queyi CI

on:
  push:
    branches: [master]
    tags: ['v*']
  pull_request:
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

permissions:
  contents: read          # 最小权限；建 Release 时单独 job 提权

jobs:
  # ---------- Job 1：内核门禁（fail-closed，永不 skip） ----------
  gate:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0            # git describe 需要完整历史
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - name: 内核自检（67 规则 / 44 block）
        run: python tools/gate_engine.py --check
      - name: 独立对账器复算哈希链
        run: python tools/reconcile.py --verify-ledger --json out/ledger.json
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: gate-report-${{ github.run_id }}
          path: out/
          retention-days: 30

  # ---------- Job 2：C++ 三编译器矩阵 ----------
  build-matrix:
    needs: gate
    runs-on: ${{ matrix.os }}
    timeout-minutes: 30
    strategy:
      fail-fast: false
      max-parallel: 3
      matrix:
        include:
          - { os: ubuntu-latest,  cxx: g++-14,     cc: gcc-14 }
          - { os: ubuntu-latest,  cxx: clang++-18, cc: clang-18 }
          - { os: windows-latest, cxx: cl,         cc: cl }
    steps:
      - uses: actions/checkout@v4
      - name: 安装编译器（Linux）
        if: runner.os == 'Linux'
        run: sudo apt-get update && sudo apt-get install -y ${{ matrix.cxx }}
      - name: 配置 + 构建夹具
        run: |
          cmake -S cpp -B build -DCMAKE_CXX_COMPILER=${{ matrix.cxx }}
          cmake --build build -j 4
      - name: 跑缺陷夹具（15 条，期望重注入检出 100%）
        run: python tools/run_fixtures.py --build-dir build --expect-detect-rate 1.0
      - name: 上传失败样本
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: fixture-failures-${{ matrix.cxx }}-${{ github.run_id }}
          path: build/failures/
          retention-days: 14

  # ---------- Job 3：仅在 tag 上发布 ----------
  release:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: [gate, build-matrix]
    runs-on: ubuntu-latest
    permissions:
      contents: write        # 建 Release 需要写权限
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: gate-report-${{ github.run_id }}
          path: dist/
      - uses: softprops/action-gh-release@v2
        with:
          files: dist/**
          generate_release_notes: true
```

**三条设计要点**：(1) `gate` job **没有 `if`**，永远跑，失败即红；(2) `build-matrix` 用 `fail-fast: false` 保证能同时看到三个编译器的结果；(3) `release` job 的 `if` 是**允许跳过**的（跳过即 Success 在这里是正确语义），且它单独提权 `contents: write`，符合最小权限。

### 10. 权限、密钥与 Artifact 保留：三个容易被忽略的默认值

**（1）`GITHUB_TOKEN` 的默认权限是"宽"的，必须显式收窄。**
GitHub Actions 每个 job 自动获得一个 `GITHUB_TOKEN`。官方文档（`https://docs.github.com/en/actions/reference/limits`）明确其限流为 **1000 请求/小时/仓库**。默认权限在仓库设置里可配，**历史默认是 read-write**（对多数 workflow 过宽）。对阙疑的正确做法：

```yaml
permissions:
  contents: read          # 顶层默认最小化
jobs:
  release:
    permissions:
      contents: write     # 只有需要建 Release 的 job 单独提权
```

理由：阙疑的 `gate` 与 `build-matrix` 只需读代码，**没有任何理由持有写权限**。一旦某个第三方 Action 被投毒，宽权限会直接把仓库写入能力交出去。

**（2）密钥一律走 `secrets`，绝不写进 YAML，也绝不进缓存。**
方向 38 引用的官方缓存文档原文警告："**Do not store any credentials or tokens in the cache paths.** Anyone with read access can create a pull request on a repository and access the contents of the cache." 阙疑如果将来接入任何外部 API（如 CI 里调 LLM 做对比实验），密钥必须放 `Settings → Secrets and variables → Actions`，通过 `${{ secrets.XXX }}` 引用。**同时注意**：`pull_request` 事件触发的 workflow **不会**拿到 secrets（fork PR 尤其如此），这是刻意的安全设计，不是 bug。

**（3）Artifact 的默认保留期是 90 天，可显式缩短。**
`actions/upload-artifact@v4` 的 `retention-days` 默认 **90 天**，而 GitHub Free 的制品存储只有 **500 MB**（与 Packages 共享配额）。阙疑的 `gate_report.json` 每跑一次都会产生一个 artifact，若不设 `retention-days`，90 天后才自动清理，**期间会持续占用 500 MB 配额并可能触发超额计费（$0.25/GB/月）**。建议：

```yaml
retention-days: 30      # gate 报告
retention-days: 14      # 失败样本（只用于排查，不需长期保留）
```

**（4）`actions/checkout` 的 `fetch-depth` 默认是 1，会破坏 `git describe`。**
`actions/checkout` 默认做**浅克隆（`fetch-depth: 1`）**，只取最近一次提交。这会导致：(a) `git describe --tags` 失败或给出错误结果；(b) `git log` 的历史分析（如方向 36 的批次号一致性检查）看不到历史。**阙疑必须显式写 `fetch-depth: 0`**（如 §9 的 YAML 所示），否则"用 tag 钉住版本"的整个方案在 CI 里会静默失效。

**（5）"required status check" 的配置位置不在 YAML 里。**
GitHub 的分支保护规则（required status checks）是在 **仓库 Settings → Branches** 里配的，**不在 workflow 文件里**。必须同时满足两个条件门禁才真正生效：(a) YAML 里的 job 会**失败**（而不是 skip，见 §5）；(b) 该 job 名字被加进 required status checks 列表。**只做 (a) 不做 (b)，红叉只是一个装饰**。

### 11. 与替代方案的对比（为什么选 GitHub Actions）

| 方案 | 免费额度 | 三编译器支持 | 配置成本 | 对阙疑的适配度 |
|---|---|---|---|---|
| **GitHub Actions** | 公开仓库无限 / 私有 2000 分钟 | 原生 `ubuntu-latest` + `windows-latest`，macOS 可选 | 一个 YAML | **最高**（仓库已在 GitHub） |
| GitLab CI | 免费 400 分钟/月（共享 runner） | 需自备 macOS runner | `.gitlab-ci.yml` | 低（要迁移仓库） |
| Travis CI | 免费额度已大幅收缩 | 支持 | `.travis.yml` | 低 |
| 自建（Jenkins/Drone） | 无（电费 + 维护） | 完全自由 | 最高 | 最低（单人项目无运维预算） |
| 本地 Makefile + 手动跑 | 0 | 自由 | 0 | **不够**（不可被独立验收者复现） |

**关键判断**：阙疑的核心主张是"**可被独立验收**"。这意味着 CI 配置的价值不只是"自动化"，而是"**给独立验收者一个可以照着跑一遍的、公开可见的流程**"。GitHub Actions 的日志是公开可查的（公开仓库），这本身就是"可验收性"的一部分——**换成自建 Jenkins，审稿人就无法自己复现 CI**。这一条比免费额度更重要。

---

## 对阙疑的 3 条具体行动

**行动 1：把仓库设为 public，并立刻加 `.github/workflows/ci.yml`（抄上面 §9 的 YAML）。**
具体：`gh repo edit --visibility public`（或网页 Settings）。理由：公开仓库 standard runner **免费无限 + 4 核 16 GB**，私有仓库只有 2000 分钟/月 + 2 核 8 GB。阙疑的核心主张是"可被独立验收"，public 是这一主张的**前提条件**，不是可选项。验收标准：第一次 push 后 Actions 页面出现 `gate` / `build-matrix` 两个 job，且 `build-matrix` 显示 3 个分支全部运行（不是 1 个）。

**行动 2：把"本地 pre-push 跑 `--check`"与"CI 跑 `--check`"绑定为同一个命令字符串，并在 CI 里禁止任何 `if` 跳过的门禁。**
具体：新增 `Makefile` 目标 `make check`（内容就是 `python tools/gate_engine.py --check`），`.githooks/pre-push` 调 `make check`，CI 的 `gate` job 也调 `make check`。**明确不写** `if:` 在 `gate` job 上——因为官方文档已证实 skipped job 报 "Success" 且不阻止合并。验收标准：故意提交一个违反 block 规则的夹具，本地 push 被拒、且强行 `--no-verify` push 后 CI 变红。

**行动 3：把 `_auto/status.json` 的批次号一致性做成 CI 断言，直接封堵"元状态漂移"。**
具体：新增 job `meta-consistency`，步骤为：读 `_auto/status.json` 的 `active_batch`，读 `git log -1 --format=%s` 的首个数字 token，若 `active_batch < 实际批次` 则 `exit 1`。理由：`00_仓库扫描.md` 已实测 `active_batch=660` vs 实际 `665` 的漂移；把它变成 CI 门禁后，"元状态不可信"从"论文里的一个抱怨"变成"每次 push 都被自动检查的不变量"。验收标准：这个 job 在修复 `status.json` 前是红的，修复后变绿。同时把 `actions/upload-artifact@v4` 的 name 全部改成带 `${{ github.run_id }}`（v4 不可变，重名会报错）。

---

## 盲区（诚实标注）

1. **2026-01-01 起 Actions 计费规则是否变更，未核实**。搜索结果中 `https://stacktrack.com/posts/understanding-github-actions-runner-costs-in-2026/` 与 `https://www.toutiao.com/article/7586612342629155368/` 都提到"2026 年 1 月 1 日有变化"，但**官方文档 `docs.github.com/en/billing/concepts/product-billing/github-actions` 我读到的仍是 2000/3000/50000 分钟口径**，两处说法是否冲突**未定论**，建议 2027 投稿前重读官方计费页。
2. **`ubuntu-latest` 具体映射到哪个 Ubuntu 版本会随时间变**：官方文档列为 `ubuntu-24.04` / `ubuntu-22.04` / `ubuntu-26.04`，而搜索结果显示 GitHub 于 **2026-09-17** 宣布 Ubuntu 26.04 runner 正式支持（`https://blog.dante.company/zh-CN/articles/ubuntu-26-runner-migration-2026-09-22-zh-cn`）。`ubuntu-latest` 的**当前**指向我未核实，建议 CI 里**显式写 `ubuntu-24.04`** 而非 `-latest`（可复现性要求）。
3. **`softprops/action-gh-release@v2` 的确切最新版本号未核实**（我未读其 README）。同样 `actions/checkout@v4`、`actions/setup-python@v5` 的版本号来自搜索结果的示例，**官方文档示例里已出现 `actions/checkout@v6` 与 `actions/setup-node@v7`**（见 §5 的官方 YAML），说明主版本已推进；写 YAML 时应以官方 README 的最新 tag 为准。
4. **`clang-18` / `g++-14` 在 `ubuntu-24.04` 上的 apt 包名未逐一核实**（`clang++-18` 可能需从 apt.llvm.org 装）。这一条需要本地实测。
5. **MSVC 在 `windows-latest` 上跑 C++ 需要 `ilammy/msvc-dev-cmd` 或 `microsoft/setup-msbuild` 之类的前置 Action**，我在 §9 的 YAML 里简化成了 `cl.exe`，**未验证该写法在干净 runner 上能直接工作**，需实测修正。
6. **三编译器矩阵的实际墙钟时间未测**。上面的"3 job × 3–6 分钟"是我基于经验值的估算，**不是实测**。

---

## 来源

1. GitHub Docs, *GitHub Actions billing* — https://docs.github.com/en/billing/concepts/product-billing/github-actions （一手；免费分钟数/存储/费率全表）
2. GitHub Docs, *Actions limits* — https://docs.github.com/en/actions/reference/limits （一手；360 分钟默认、256 matrix、500 KB workflow、缓存限流、并发表）
3. GitHub Docs, *GitHub-hosted runners reference* — https://docs.github.com/en/actions/reference/runners/github-hosted-runners （一手；4C/16G vs 2C/8G 差异、ubuntu-slim 15 分钟超时）
4. GitHub Docs, *Dependency caching reference* — https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching （一手；10 GB、7 天驱逐、512 字符 key、作用域隔离、投毒）
5. GitHub Docs, *Using conditions to control job execution* — https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions （一手；"skipped job reports Success"原文）
6. GitHub Docs, *Running variations of jobs in a workflow* — https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations （一手；matrix 语法）
7. GitHub Docs, *Control the concurrency of workflows and jobs* — https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency （一手）
8. GitHub, *actions/upload-artifact* — https://github.com/actions/upload-artifact （一手；v4 不可变、GHES 不支持）
9. DeepWiki, *Key Changes | actions/upload-artifact* — https://deepwiki.com/actions/upload-artifact/4.1-key-changes （v3→v4 架构重写说明）
10. GitHub, *actions/setup-python caching ADR* — https://github.com/actions/setup-python/blob/main/docs/adrs/0000-caching-dependencies.md
11. *Set GitHub Actions timeout-minutes* — https://dev.to/suzukishunsuke/set-github-actions-timeout-minutes-1jkk （2024-07-03；"360 太长"）
12. *GitHub Actions Matrix 矩阵构建：多平台多版本并行测试* — https://eastondev.com/blog/zh/posts/dev/20260428-github-actions-matrix/ （2026-04-28；fail-fast/exclude/include 实战）
13. *GitHub Actions 迁移至 Ubuntu 26.04* — https://blog.dante.company/zh-CN/articles/ubuntu-26-runner-migration-2026-09-22-zh-cn （2026-09-22）
14. 本仓库内部锚点：`_arch_v46/00_仓库扫描.md` §2（227 项漂移）、§5（`gate_engine.py` 3826 行）、§13（元状态漂移案例）。
