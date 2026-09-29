# 方向 25：单人项目 CI/CD 最小配置

## 核心结论

1. **对公开仓库，GitHub Actions 是"免费且不限量"的，这直接决定了单人项目的架构选择。** GitHub 官方计费文档逐字：*"GitHub Actions usage is **free** for **self-hosted runners** and for **public repositories** that use standard GitHub-hosted runners."* 并明确列出免费范围：*"The use of standard GitHub-hosted runners is free: In public repositories / For GitHub Pages / For Dependabot."* 唯一例外是 *"Larger runners are always charged for, even when used by public repositories or when you have quota available from your plan."* **对阙疑的直接含义：把 CPP-Bible 与 queyi-verifier 设为公开仓库，CI 成本为零**，可以把"每次 push 都跑完整复现验证"当成默认行为，而不必精打细算。

2. **CI 是"无资源访问时唯一可提交的可复现性证据"——这是 2025 年一篇专门论文的核心论点。** arXiv:2508.21289 *Addressing Reproducibility Challenges in HPC with Continuous Integration* 摘要逐字：*"The uniqueness of HPC infrastructure and software, coupled with strict access requirements, may limit opportunities for reproducibility. **In the absence of resource access, we believe that regular documented testing, through continuous integration (CI), coupled with complete provenance information, can be used as a substitute.**"* 第 4 节：*"CI is important in the context of reproducibility, as it can track how code changes impact behavior in different environments."* 该文还指出会议徽章流程中 CI 的定位：*"conferences like CCGrid recommend Continuous Integration (CI) for automated software testing as part of their badge awarding process"*，且第二级徽章的理想状态是 *"it also includes an automated test suite using CI systems."* **对阙疑而言，CI 绿标 + 可公开访问的运行日志，是把"判决可复算"从声明变成证据的最低成本手段。**

3. **单人项目 CI 的第一原则是"总时长最短、噪声最低"，而不是覆盖率最高。** 三条具体设计：(i) **矩阵只保留有信息量的维度**（Python 3.12 × {gcc-13, clang-16}），不要盲目堆 OS——macOS runner 单价 **$0.062/分钟**，是 Linux 2-core（**$0.006/分钟**）的 **10.3 倍**；(ii) **`concurrency` + `cancel-in-progress: true`** 让连续 push 时旧任务自动取消，避免排队烧额度；(iii) **所有 job 设 `timeout-minutes`**，防止挂死任务跑满 6 小时上限。**注意 GitHub artifact 只保留 90 天**（该论文逐字：*"As GitHub artifacts remain available for only 90 days…"*），所以账本与判决结果**必须另行持久化到 Zenodo/Software Heritage**，不能只靠 CI artifact。

---

## 精确数字与案例

### 一、免费额度与费率（GitHub 官方计费文档逐字）

**私有仓库**（公开仓库不适用，无限免费）：

| 计划 | 制品存储 | 分钟/月 | 缓存存储/仓库 | 自定义镜像存储 |
|---|---|---|---|---|
| GitHub Free | 500 MB | **2,000** | 10 GB | 不适用 |
| GitHub Pro | 1 GB | **3,000** | 10 GB | 不适用 |
| GitHub Free for organizations | 500 MB | **2,000** | 10 GB | 不适用 |
| GitHub Team | 2 GB | **3,000** | 10 GB | 75 GB |
| GitHub Enterprise Cloud | 50 GB | **50,000** | 10 GB | 150 GB |

> *"At the start of each month, the minutes used by the account are reset to zero."*

**存储口径的两条关键区别**：
- 制品存储是**共享**的：*"The artifact storage amounts shown are **shared** with GitHub Packages. This means your total storage across Actions artifacts and GitHub Packages storage cannot exceed the included amount for your plan."*
- 缓存存储是**独立**的：*"Actions cache storage is a separate allowance of **10 GB per repository**. Cache storage is not shared with artifacts or GitHub Packages."* 且计费按**每小时峰值**：*"For a given hour, if a repository has a peak cache usage of 15 GB, then the repository owner will be charged for the 5 GB of usage above the 10 GB included for that repository."*

**超量单价**：

| 运行器 | Billing SKU | 每分钟 |
|---|---|---|
| Linux 1-core (x64) | `actions_linux_slim` | **$0.002** |
| Linux 2-core (x64) | `actions_linux` | **$0.006** |
| Linux 2-core (arm64) | `actions_linux_arm` | **$0.005** |
| Windows 2-core (x64) | `actions_windows` | **$0.010** |
| Windows 2-core (arm64) | `actions_windows_arm` | **$0.010** |
| macOS 3/4-core (M1 或 Intel) | `actions_macos` | **$0.062** |

存储：共享存储（artifact + Packages）**$0.25/GB/月**；Actions cache **$0.07/GB/月**；自定义镜像存储 **$0.07/GB/月**。

**算一笔账**：公开仓库 0 成本。若不小心用了私有仓库，一次 5 分钟的 Linux 2-core 任务 = **$0.03**；同样的任务在 macOS 上是 **$0.31**（10.3 倍）。**结论：能用 ubuntu-latest 就别用 macos-latest；能用公开仓库就别用私有仓库。**

### 二、最小可用工作流（官方 YAML，逐字）

GitHub 官方 *Building and testing Python* 给的最小矩阵示例（逐字）：

```yaml
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["pypy3.10", "3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v6
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Display Python version
        run: python -c "import sys; print(sys.version)"
```

**带缓存的版本**（逐字）：

```yaml
steps:
- uses: actions/checkout@v6
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
- run: pip install -r requirements.txt
- run: pip test
```

**缓存行为（逐字）**：*"By default, the `setup-python` action searches for dependency files in the entire repository: pip uses `requirements.txt`, pipenv uses `Pipfile.lock`, poetry uses `poetry.lock`."* 若使用 `uv.lock`（方向 23 推荐），需**显式指定** `cache-dependency-path: uv.lock`（本组未逐字核实该参数在 setup-python@v5 中的确切名称，见盲区）。

**为什么必须用 setup-python**（官方逐字，三条）：*"Using the `setup-python` action is the recommended way of using Python with GitHub Actions because it ensures consistent behavior across different runners and different versions of Python."*；*"We recommend using `setup-python` to configure the version of Python used in your workflows because it helps make your dependencies explicit."*；*"If you don't use `setup-python`, the default version of Python set in `PATH` is used in any shell when you call `python`. The default version of Python varies between GitHub-hosted runners, which may cause unexpected changes or use an older version than expected."*

**矩阵排除**（逐字，`exclude` 关键字）：

```yaml
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.11", "3.13", "pypy3.10"]
        exclude:
          - os: macos-latest
            python-version: "3.11"
          - os: windows-latest
            python-version: "3.11"
```

**测试结果归档**（逐字，含 `if: ${{ always() }}` 这个易漏细节）：

```yaml
      - name: Test with pytest
        run: pytest tests.py --doctest-modules --junitxml=junit/test-results-${{ matrix.python-version }}.xml
      - name: Upload pytest test results
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results-${{ matrix.python-version }}
          path: junit/test-results-${{ matrix.python-version }}.xml
        # Use always() to always run this step to publish test results when there are test failures
        if: ${{ always() }}
```

### 三、状态徽章：把 CI 结果变成论文里可引用的证据

**GitHub 原生徽章 URL 格式**（官方文档逐字）：*"You can build the URL for a workflow status badge using the name of the workflow file: `HOSTNAME/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg`"*，可加 `?branch=BRANCH-NAME` 与 `?event=push`。

**shields.io 等价写法**（第三方，格式已被广泛采用）：`https://img.shields.io/github/actions/workflow/status/owner/repo/ci.yml`。

**一个必须注意的陷阱（官方逐字）**：*"Workflow badges in a **private** repository are not accessible externally, so you won't be able to embed them or link to them from an external site."*——**若仓库私有，徽章在论文/OpenReview 里无法显示**。这与结论 1 的"用公开仓库"是同一个决定。

**把 CI 当作可复现性证据的正确做法**（结合 arXiv:2508.21289 的论点）：
1. 徽章放 README 顶部（审稿人第一眼就看到）；
2. 在论文附录给出**具体 workflow 文件路径**（如 `.github/workflows/repro.yml`）与**一次成功运行的公开 URL**（Actions 页面在公开仓库对所有人可见）；
3. 在 `REPRODUCTION.md` 里贴出 CI 的**关键 step 输出片段**（哈希比对结果、pytest 汇总行），而不是只说"CI 通过"；
4. 该论文强调的核心是 **"regular documented testing"** ——"documented"是关键词：**没有记录的绿标不算证据**，必须有可追溯的运行历史。

### 四、单人项目的降噪配置：concurrency、timeout、permissions

**并发控制**（官方逐字）：*"To also cancel any currently running jobs or workflows in the same concurrency group, specify `cancel-in-progress: true`."* 典型写法：

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**超时**：`jobs.<job_id>.timeout-minutes` 与 `jobs.<job_id>.steps[*].timeout-minutes` 均为官方支持的字段。对单人项目，建议 job 级 `timeout-minutes: 20`，避免一个挂死的构建吃掉整月额度（私有仓库场景）。

**最小权限**（方向 24 已引 GitHub 官方原文）：*"It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents."* 写法：

```yaml
permissions:
  contents: read
```

**触发面收窄**：单人项目不需要 `on: [push]` 全开。推荐 `on: { push: { branches: [main] }, pull_request: {}, workflow_dispatch: {} }`。`workflow_dispatch` 让审稿人能手动触发一次复现验证（**这是给 artifact 评审的实用钩子**）。

**C++ 侧的矩阵**：`cpp-best-practices/cmake_template` 是社区维护的 CMake 项目模板，用 GitHub Actions 作为主要 CI/CD 平台（本组未逐字核实其 workflow 内容）。自建时建议矩阵维度取 `{gcc-13, clang-16}` × `{Release, Debug}`，用 `CMakePresets.json` 承载配置而非在 YAML 里堆 flag。

### 五、CI 做不到什么（必须写进论文的限制）

| 限制 | 依据 | 对阙疑的影响 |
|---|---|---|
| artifact 只存 **90 天** | arXiv:2508.21289 逐字 | 账本/判决结果必须另存 Zenodo/Software Heritage |
| CI 绿 ≠ 结果可复现 | CI 只证明"当前代码在当前 runner 上跑通" | 不能替代 Merkle root 比对 |
| runner 环境本身会漂移 | `ubuntu-latest` 指向滚动更新的镜像 | 需配合容器 + digest 钉死（方向 22） |
| 私有仓库徽章不可外链 | GitHub 官方文档逐字 | 论文里无法展示 |
| 缓存可能掩盖问题 | cache hit 时跳过依赖安装 | 关键验证 job 应加 `--no-cache` 或独立跑一次冷启动 |
| 审稿人不会看 CI 配置 | 无依据，属经验判断 | 必须在论文正文用一句话点明"CI 配置见 X，运行日志见 Y" |

该论文还提到一个有用的量化约束：**审稿人通常只有约 8 小时或一个工作日来复现实验**（逐字：*"Reviewers are usually given a limited amount of time, typically about eight hours or one business day, to reproduce the experiments."*）。**这决定了 CI 的单次运行时间预算：最好在 10 分钟以内**，否则审稿人不会等。

---

## 对阙疑的 3 条具体行动

1. **2026-11 前建立 `.github/workflows/repro.yml`，把"判决可复算"做成 CI 断言**。内容包含四个 job：
   - `lint`：`hadolint Dockerfile`（方向 22）+ `uv lock --check`（方向 23）+ `gitleaks git --baseline-path research/security/gitleaks-baseline.json`（方向 24）；
   - `unit`：矩阵 `python-version: ["3.12"]` × `os: [ubuntu-latest]`，`actions/setup-python@v5` + `cache: 'pip'` + `cache-dependency-path: uv.lock`，跑 `pytest -q --junitxml=junit/test-results.xml`，并用 `actions/upload-artifact@v4` + `if: ${{ always() }}` 归档；
   - `repro`：`uv sync --frozen` 后跑 `python gate_engine.py --replay fixtures/ledger_452.jsonl --print-merkle-root`，与 `fixtures/expected_merkle_root.txt` 做 `diff`，**不一致即 fail**；
   - `docker`：`docker buildx build --no-cache --build-arg SOURCE_DATE_EPOCH=1704067200 -t queyi:ci .` 后 `docker run --rm --network=none queyi:ci python -m pytest -q`。
   顶层加 `permissions: { contents: read }`、`concurrency: { group: ..., cancel-in-progress: true }`、每个 job 加 `timeout-minutes: 20`。

2. **2026-11 前完成"公开仓库 + 徽章 + 持久化"三件套**：(i) 确认两个仓库为**公开**（否则徽章无法在 OpenReview 外链，且 CI 开始计费）；(ii) README 顶部加一行徽章，用原生格式 `https://github.com/<OWNER>/<REPO>/actions/workflows/repro.yml/badge.svg?branch=main`，或 shields.io 的 `https://img.shields.io/github/actions/workflow/status/<OWNER>/<REPO>/repro.yml?branch=main`；(iii) **在 `repro` job 末尾增加一步**：把 Merkle root、时间戳、commit SHA 写入 `artifacts/repro-receipt.json` 并 `actions/upload-artifact@v4`——同时在 `REPRODUCTION.md` 里注明 *"GitHub Actions artifacts expire after 90 days; the canonical receipt is archived at Zenodo DOI: 10.5281/zenodo.XXXXXXX"*，并真的把回执推到 Zenodo（避免 90 天后证据消失）。

3. **在 `research/` 下新增 `25_ci_as_evidence.md`，把 CI 明确定位为"可复现性证据的一种"，并写清边界（2027-02 前）**：内容引用 arXiv:2508.21289 的三句原文（"can be used as a substitute"、"CI is important in the context of reproducibility"、"Reviewers are usually given a limited amount of time, typically about eight hours"），并据此论证：(i) 阙疑的 CI 单次运行目标 **< 10 分钟**（对齐审稿人 8 小时预算）；(ii) 论文里给出**一次成功运行的公开 URL** 与 workflow 文件路径，而不是只写"code is available"；(iii) 在 Threats to Validity 里加一条 **T-CI**："CI 通过仅表明在 GitHub 托管 runner 的特定镜像上可执行；本文通过同时提供钉 digest 的 Dockerfile 与 `--network=none` 的运行期验证来降低 runner 漂移风险。CI artifact 仅保留 90 天，永久回执存于 Zenodo。" 并附一张表：证据类型 / 位置 / 可核验方式（CI 徽章 → Actions 页面；Merkle root → fixtures 文件；镜像 → digest；依赖 → `uv.lock` + `requirements.lock`）。

---

## 盲区（诚实标注）

- **`setup-python@v5` 是否支持 `cache-dependency-path: uv.lock`、以及该参数的确切拼写未逐字核实**。官方文档只列出默认搜索的三种文件（`requirements.txt` / `Pipfile.lock` / `poetry.lock`），未提 uv。**须实测后再写进 CI**。
- **`actions/checkout@v6` 是官方文档当前示例中的版本**，本组未核实 v6 的发布时间与是否有破坏性变更（历史上有过 v3→v4 的 Node 运行时升级）。
- **arXiv:2508.21289 未提供任何量化统计**（该文自述为立场/综述性质）。"CI 提升可复现率 X%"这类数字**在原文中不存在**，不可编造。文中提到的 "Continuous Reproducibility" 一词归于 Fernández-Prades et al. 2018，本组未核实该原始出处。
- **公开仓库 CI 是否真的"完全无限"存在实践边界**：官方文本说免费，但另有并发限制与滥用防护（abuse rate limits）条款未逐字核实；有第三方博客提到 2026 年 GitHub Actions 计费政策"反转"，本组未核实真伪，**建议按官方文档为准**。
- **GitHub 官方文档中文版与英文版可能存在版本差异**；本组读取的是英文页。**部分页面标注的日期（如 2026-04-14）为文档更新日期，非政策生效日期。**
- **`cpp-best-practices/cmake_template` 的 workflow 内容未逐字读取**（仅从 DeepWiki 摘要得知其"uses GitHub Actions as its primary CI/CD platform"）。C++ 矩阵的具体推荐（gcc/clang 版本组合）属本组建议，非引用。
- **未核实**：`ubuntu-latest` 当前具体指向的 Ubuntu 版本与预装 GCC/Clang 版本。这对 C++ 项目是实质风险——若 runner 默认 GCC 版本低于 8，方向 22 的 `-ffile-prefix-map` 不可用。
- **"审稿人 8 小时"来自 arXiv:2508.21289 对 HPC 会议徽章评审的描述**，向 NeurIPS E&D 外推属推断；NeurIPS 官方未公布评审时间预算。
- 未核实：GitHub Actions 的 job 级 `timeout-minutes` 默认值（官方文档说默认 360 分钟，本组未逐字确认）。

---

## 来源

1. GitHub Actions billing — https://docs.github.com/en/billing/concepts/product-billing/github-actions — 逐字：*"GitHub Actions usage is **free** for **self-hosted runners** and for **public repositories** that use standard GitHub-hosted runners."*；*"The use of standard GitHub-hosted runners is free: In public repositories / For GitHub Pages / For Dependabot"*；*"Larger runners are always charged for"*；私有仓库配额表（Free **2,000** 分钟 / 500 MB；Pro **3,000** / 1 GB；Team **3,000** / 2 GB；Enterprise Cloud **50,000** / 50 GB）；*"Actions cache storage is a separate allowance of **10 GB per repository**."*；峰值计费示例；费率表（Linux 2-core **$0.006**、Windows **$0.010**、macOS **$0.062**、Linux 1-core slim **$0.002**、arm64 **$0.005**）；存储 **$0.25** / **$0.07** / **$0.07** per GB-month — GitHub Docs — 持续更新
2. Building and testing Python — https://docs.github.com/en/actions/tutorials/build-and-test-code/python — 逐字：完整矩阵 YAML（`python-version: ["pypy3.10", "3.9", "3.10", "3.11", "3.12", "3.13"]`）；`cache: 'pip'` 示例；*"Using the `setup-python` action is the recommended way of using Python with GitHub Actions because it ensures consistent behavior across different runners and different versions of Python."*；*"If you don't use `setup-python`, the default version of Python set in `PATH` is used… The default version of Python varies between GitHub-hosted runners"*；`exclude` 示例；`upload-artifact@v4` + `if: ${{ always() }}`；默认搜索 `requirements.txt` / `Pipfile.lock` / `poetry.lock` — GitHub Docs — 持续更新
3. Adding a workflow status badge — https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge — 逐字：*"HOSTNAME/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg"*；`?branch=` 与 `?event=` 参数；*"Workflow badges in a **private** repository are not accessible externally, so you won't be able to embed them or link to them from an external site."*；*"By default, badges display the status of your default branch."* — GitHub Docs — 持续更新
4. Control the concurrency of workflows and jobs — https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency — 逐字：*"To also cancel any currently running jobs or workflows in the same concurrency group, specify `cancel-in-progress: true`."* — GitHub Docs — 持续更新
5. Workflow syntax for GitHub Actions — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax — `jobs.<job_id>.timeout-minutes`、`jobs.<job_id>.steps[*].timeout-minutes`、`permissions`、`on` 的可用键 — GitHub Docs — 持续更新
6. Secure use reference — https://docs.github.com/en/actions/reference/security/secure-use — 逐字：*"It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents."* — GitHub Docs — 持续更新（方向 24 同源）
7. Addressing Reproducibility Challenges in HPC with Continuous Integration — https://arxiv.org/html/2508.21289v1 — 逐字：*"In the absence of resource access, we believe that regular documented testing, through continuous integration (CI), coupled with complete provenance information, can be used as a substitute."*；*"CI is important in the context of reproducibility, as it can track how code changes impact behavior in different environments."*；*"conferences like CCGrid recommend Continuous Integration (CI) for automated software testing as part of their badge awarding process"*；*"it also includes an automated test suite using CI systems"*；*"Reviewers are usually given a limited amount of time, typically about eight hours or one business day, to reproduce the experiments."*；*"As GitHub artifacts remain available for only 90 days…"*；*"Continuous reproducibility, or automation through continuous integration, is a promising approach to ensure the reproducibility of scientific code; however, at present most approaches are limited to a single site."*；*"Continuous Reproducibility"* 一词归于 Fernández-Prades et al. 2018 — arXiv:2508.21289 — 2025-08-29（**无量化统计**）
8. Adding Custom GitHub Badges to Your Repo — https://www.positioniseverything.net/adding-custom-github-badges-to-your-repo/ — shields.io 格式 `https://img.shields.io/github/actions/workflow/status/owner/repo/ci.yml`；`?branch=main` 参数；*"For a small project, three to five badges are usually enough: build status, version, license, coverage, and documentation"* — 第三方 — **未标注日期（非官方，页面含大量广告）**
9. CMake Action — GitHub Marketplace — https://github.com/marketplace/actions/cmake-action — CMake 项目在 Actions 中的配置/构建示例 — 第三方 action — 2024-08-05
10. cpp-best-practices/cmake_template — GitHub Actions（DeepWiki 摘要）— https://deepwiki.com/cpp-best-practices/cmake_template/4.1-github-actions — *"The cmake_template repository uses GitHub Actions as its primary CI/CD platform to automate testing, code quality…"* — 社区 — 2025-04-23（**未逐字读原文**）
11. Reproducibility Report for SC25 Paper — https://dl.acm.org/doi/epdf/10.1145/3712285.3769443 — 会议可复现性报告的实例 — ACM — 2025-11-12
12. ACM SIGMOD Availability & Reproducibility Initiative — reports — https://reproducibility.sigmod.org/reports.html — *"Following is the list of papers that passed the reproducibility test, the functionality test, and/or have made their [artifacts available]"* — ACM SIGMOD — 2026-04-01
13. GitHub Actions 使用限制、计费和管理 — https://docs.github.com/en/actions/administering-github-actions/usage-limits-billing-and-administration — 使用上限与计费管理入口 — GitHub Docs — 持续更新
