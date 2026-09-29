# 方向 23：依赖锁定（pip / pip-tools / poetry / uv / conda-lock）

## 核心结论

1. **`requirements.txt` 不是锁文件，它只是"按惯例支持的格式"。** PEP 751 的 Motivation 逐字写道：*"The closest the community has to a standard are pip's requirements files… Unfortunately, the format is not a standard but is supported by convention. It's also designed very much for pip's needs, limiting its flexibility and ease of use (e.g. it's a bespoke file format). Lastly, **it is not secure by default** (e.g. file hash support is entirely an opt-in feature…)."* PEP 751 已于 **2025-03-31 被接受（Status: Final）**，标准化格式是 `pylock.toml`，规范正文现维护在 PyPA packaging specs 页。对阙疑的直接含义：**论文里应声明使用哪个锁文件、哪个格式、哪个工具版本，而不是笼统写 "requirements.txt"**。

2. **uv 的核心差异化是"通用（universal）锁文件"，这正是科研复现需要的性质。** uv 官方文档逐字：*"`uv.lock` is a *universal* or *cross-platform* lockfile that captures the packages that would be installed across all possible Python markers such as operating system, architecture, and Python version."* 对照之下，`pip freeze` 与 pip-tools 只生成"当前环境"的单次锁（PEP 751 原文：*"`pip freeze` and pip-tools only generate single-use lock files for the current environment while PDM, Poetry, and uv can/try to lock for multiple environments and use-cases at once"*）。**审稿人用 macOS、作者用 Windows 是最常见的复现失败场景**，通用锁文件是唯一能提前消灭它的手段。

3. **锁文件保证"解析结果一致"，不保证"安装结果一致"——这是必须写进论文 Limitations 的边界。** PEP 751 明确警告：*"Lock files that follow this PEP can be installed by any installer that implements the specification… **But it is not the case that using a different locker will lead to the same result.** This could be for various reasons, including using different algorithms to determine what to lock."* 并且该 PEP **明确不锁 sdist 的构建依赖**（Rejected Ideas: *"An earlier version of this PEP tried to lock the build requirements for sdists under a `packages.build-requires` key… it confused enough people… Instead, a future PEP could propose a solution."*）。也就是说：**任何含 C 扩展的包（numpy/scipy/pandas）若走 sdist 编译，锁文件管不到它编译时用了什么**。阙疑若依赖含 C 扩展的包，必须显式要求 wheel（`--only-binary :all:`，见方向 22）。

---

## 精确数字与案例

### 一、五种方案横向对比

| 维度 | pip + requirements.txt | pip-tools | Poetry | uv | conda-lock |
|---|---|---|---|---|---|
| 锁文件 | 无（手写） | `requirements.txt`（由 `requirements.in` 编译） | `poetry.lock` | `uv.lock`（TOML） | `conda-lock.yml` |
| 是否跨平台 | 否（须手写 markers） | 否（单环境） | 可锁多环境 | **是（universal）** | **是（多平台）** |
| 默认含哈希 | **否（opt-in）** | 是（`--generate-hashes`） | 是 | 是 | 是（`name=version=build_hash`） |
| 官方速度声明 | 基准 | 基准 | 基准 | **"10-100x faster than `pip`"** | 未声明 |
| 锁构建依赖 | 否 | 否 | 部分 | 否 | 部分 |
| 当前版本（查阅日） | pip 26.2.1 | pip-tools 7.6.1 | — | — | — |

**pip-tools 的工作流**（官方 pip-compile 文档，v7.6.1）：`pip-compile --generate-hashes requirements.in -o requirements.txt` 生成带哈希的锁；`pip-sync` 把环境精确对齐到锁文件。官方建议"To compile from scratch, first delete the existing requirements.txt file"。**优点**：输出就是标准 `requirements.txt`，任何工具都能用（含 Dockerfile 里的 `pip install --require-hashes`）。**缺点**：单环境，且需要手工维护 `requirements.in` 与 `.txt` 两份文件。

**uv 的工作流**（官方文档逐字）：`uv lock` 生成/更新 `uv.lock`；`uv sync` 安装；`uv run` 会自动 lock + sync。**uv.lock 的关键性质**：*"`uv.lock` is a human-readable TOML file but is managed by uv and should not be edited manually. The `uv.lock` format is specific to uv and not usable by other tools."* 若要跨工具，用 `uv export`：*"you can export `uv.lock` to different formats including `requirements.txt`, `pylock.toml` (PEP 751), and CycloneDX SBOM"*，命令为 `uv export --format requirements.txt` / `--format pylock.toml` / `--format cyclonedx1.5`。

**conda-lock**：*"Conda lock is a lightweight library that can be used to generate fully reproducible lock files for conda environments. It does this by performing a conda solve for each platform you desire a lockfile for."* CLI 描述：*"Generate fully reproducible lock files for conda environments. By default, a multi-platform lock file is written to conda-lock.yml"*。锁项精确到 `name=version=build_hash`——**这是五种方案里唯一钉到 conda build 号的**，对需要系统级 C 库（BLAS/LAPACK）的科学计算最稳。缺点是重、慢、生态绑定。

### 二、速度数字：哪些是官方、哪些是第三方

**官方口径（可引用）**：uv 文档首页 Highlights 第一条是 *"A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more."*，第二条逐字：*"**10-100x faster** than `pip`."*（该链接指向 astral-sh/uv 的 `BENCHMARKS.md`）。官方首页给出的可复制终端输出包括：

```
$ uv add ruff
Resolved 2 packages in 170ms
Prepared 2 packages in 627ms
Installed 2 packages in 1ms
$ uv lock
Resolved 2 packages in 0.33ms
$ uv pip compile requirements.in --universal --output-file requirements.txt
Resolved 43 packages in 12ms
$ uv pip sync requirements.txt
Resolved 43 packages in 11ms
Installed 43 packages in 208ms
```

**必须诚实标注的坑**：uv 的 `BENCHMARKS.md` **只有四张图片（warm install / cold install / warm resolution / cold resolution），正文没有任何数字**。文档自己列了两条 caveat：*"Benchmark performance may vary dramatically across different operating systems and filesystems."* 与 *"Benchmark performance may vary dramatically depending on the set of packages being installed. For example, a resolution that requires building a single intensive source distribution may appear very similar across tools, since the bottleneck is tool-agnostic."* 基准对象是 **Trio 的 `docs-requirements.in`**，在 **macOS + Python 3.12.4** 上跑。**"10-100x" 是厂商自报的营销数字，不能当独立结论引用。**

第三方独立对比（本组检索到多篇 2026 年博客，均声称 uv 比 pip 快 8–100x、比 Poetry 快约 10x），但**这些是博客而非同行评审基准，样本与硬件条件未公开**，只能作为"普遍观察"引用，不能写具体倍数。

### 三、`--locked` / `--frozen`：CI 里必须用对的两个开关

uv 官方 *Locking and syncing* 页逐字：

- 默认行为：*"Locking and syncing are *automatic* in uv. For example, when `uv run` is used, the project is locked and synced before invoking the requested command."*
- `--locked`：*"To disable automatic locking, use the `--locked` option… **If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile.**"*
- `--frozen`：*"To use the lockfile without checking if it is up-to-date, use the `--frozen` option."*
- `--no-sync`：*"to run a command without checking if the environment is up-to-date"*
- 检查命令：*"You can check if the lockfile is up-to-date by passing the `--check` flag to `uv lock`… This is equivalent to the `--locked` flag for other commands."*
- **"最新版本发布不会让锁文件过期"**：*"uv will not consider lockfiles outdated when new versions of packages are released — the lockfile needs to be explicitly updated if you want to upgrade dependencies."* 升级用 `uv lock --upgrade` 或 `uv lock --upgrade-package <pkg>==<ver>`。
- Git 依赖也会被锁：*"if a Git dependency references the `main` branch, uv will prefer the locked commit SHA in an existing `uv.lock` file over the latest commit on the `main` branch, unless the `--upgrade` or `--upgrade-package` flags are used."*——**这对"复现某次提交"极关键**。
- 精确同步：*"`uv sync` performs 'exact' syncing by default, which means it will remove any packages that are not present in the lockfile."*（对比 `uv run` 默认是 inexact）
- 附带安全功能（preview）：`audit.malware-check = true` 会用 **OSV** 检查锁文件中的包是否命中恶意包数据库，命中则终止同步。

**CI 里的正确写法**是 `uv sync --frozen --no-dev`（复现安装，不检查、不装 dev 组）或 `uv lock --check`（作为独立 lint 步骤，锁文件过期就 fail）。

### 四、格式细节：哈希怎么算、markers 怎么写

pip 的哈希校验模式（方向 22 已展开，此处给格式对照）：`--hash=sha256:<64位十六进制>`，**all-or-nothing**，传递依赖也必须逐个列出并哈希。

PEP 751 `pylock.toml` 的哈希表结构（逐字）：*"A table listing known hash values of the file where the key is the hash algorithm and the value is the hash value. The table MUST contain at least one entry. Hash algorithm keys SHOULD be lowercase. At least one secure algorithm from `hashlib.algorithms_guaranteed` SHOULD always be included (at time of writing, sha256 specifically is recommended)."* 示例：`hashes = {sha256 = 'c75a69e28a550a7e93789579c22aa26b0f5b83b75dc4e08fe092980051e1090a'}`。

**版本与 markers 的规则**（逐字）：
- *"The version SHOULD be specified when the version is known to be stable (i.e. when an sdist or wheels are specified). The version MUST NOT be included when it cannot be guaranteed to be consistent with the code used (i.e. when a source tree is used)."*
- VCS 依赖：*"If the VCS supports commit-hash based revision identifiers, such a commit-hash MUST be used as the commit ID in order to reference an immutable version of the source code."*
- markers：*"A list of Environment Markers for which the lock file is considered compatible with. Tools SHOULD write exclusive/non-overlapping environment markers to ease in understanding."*
- 新增两个 marker：`extras` 与 `dependency_groups`。
- **必须支持 wheel**：*"Tools MUST support wheel files, both from a locking and installation perspective."* 但 archive/VCS/directory/sdist 都是 *"MAY choose to not support"*。
- **依赖图仅用于审计**：*"Tools MUST NOT use this information when doing installation; it is purely informational for auditing purposes."*

**这最后一条对阙疑特别有用**：`pylock.toml` 里可以带完整的 `[[packages.dependencies]]` 依赖图供人工审计，但不影响安装——**等于免费获得一份机器可读的依赖审计记录**，可以直接作为论文附录的"依赖可核验证据"。

### 五、迁移成本与选型建议

| 从 → 到 | 主要成本 | 风险 |
|---|---|---|
| 手写 requirements.txt → pip-tools | 拆出 `.in`，跑一次 `pip-compile --generate-hashes` | 极低；输出仍是 requirements.txt，Dockerfile 不用改 |
| requirements.txt → uv pip 接口 | 几乎为零（`uv pip compile` / `uv pip sync` 是 drop-in） | 低；但 `uv.lock` 格式不通用 |
| requirements.txt → uv 项目模式 | 需建 `pyproject.toml`，把依赖搬进去 | 中；`uv sync` 默认 exact 会删掉锁文件外的包，可能误删手工装的调试工具 |
| pip-tools → Poetry | 需 `pyproject.toml` + `poetry.lock`，Poetry 有自己的构建后端 | 中高；Poetry 对非打包项目支持较绕 |
| 任意 → conda-lock | 需接受 conda 生态与体积 | 高；但科学计算场景收益最大 |

**对单人科研项目的最优解**（本组判断，非引用）：**uv + `uv.lock` 作为主锁文件，同时用 `uv export --format requirements.txt --generate-hashes` 导出一份供 Docker 与审稿人使用的 `requirements.lock`**。这样既拿到通用锁文件与速度，又保住"任何人用 `pip install --require-hashes` 都能装"的可移植性。代价是两份文件需在 CI 里做一致性检查（`uv export` 后 `git diff --exit-code`）。

---

## 对阙疑的 3 条具体行动

1. **建立双锁文件并写进论文（2026-11 前）**：在仓库根建 `pyproject.toml`（`[project]` 声明 `requires-python = ">=3.12,<3.13"`，`[dependency-groups]` 放 dev 依赖），运行 `uv lock` 生成 `uv.lock` 并**提交进版本控制**；再运行 `uv export --format requirements.txt --no-dev --output-file requirements.lock`（若该 flag 组合不支持，改用 `uv export --format requirements.txt` 后人工裁剪）得到含哈希的 `requirements.lock`。**两个文件都必须进 git**，并在 `README.md` 的 "Reproduce" 一节写清：*"Environment is pinned by `uv.lock` (universal, cross-platform) and `requirements.lock` (hashes, for pip/Docker)."* 论文附录给出一张表：锁文件路径 / 格式 / 工具与版本 / 哈希算法。

2. **在 CI 里加"锁文件不许漂移"的门（2026-12 前）**：`.github/workflows/lock-check.yml` 中加三步：① `uv lock --check`（锁文件与 `pyproject.toml` 不一致就 fail）；② `uv export --format requirements.txt -o /tmp/req.check && diff /tmp/req.check requirements.lock`（防止两份锁文件分叉）；③ `uv sync --frozen --no-dev` 后跑 `python gate_engine.py --replay fixtures/ledger_452.jsonl --print-merkle-root`，与 `fixtures/expected_merkle_root.txt` 比对。**第 ③ 步是把"依赖锁定"和"判决可复算"绑在一起的关键断言**——它同时证明了环境可复现和结果可复算。

3. **在 `research/` 下新增 `23_dependency_pinning.md`，明确写清三件"锁文件管不到"的事（2027-01 前）**：(i) **sdist 构建依赖不受锁文件约束**（PEP 751 明确不锁 `build-requires`）——因此列出所有含 C 扩展的依赖，并声明 `PIP_ONLY_BINARY=:all:` 或 `--only-binary :all:`；(ii) **不同 locker 结果可能不同**（PEP 751 原文）——因此论文必须声明"使用 uv X.Y.Z 生成"而不只是"有锁文件"；(iii) **Python 解释器本身的版本**需单独钉（`requires-python` + `.python-version` + Docker base digest）。同时在 `research/` 的 Threats to Validity 里加一条："若审稿人使用 pip 而非 uv 安装，哈希校验可保证包内容一致，但 wheel 平台差异可能导致 C 扩展的二进制不同，进而影响含浮点运算的规则输出。" 并给出 `pip install --require-hashes --only-binary :all: -r requirements.lock` 的验证命令。

---

## 盲区（诚实标注）

- **uv 的 `BENCHMARKS.md` 正文没有任何数字**，只有四张 GitHub user-attachments 图片。"10-100x" 是 uv 官方文档首页的自述，**未在独立基准上复核**；本组无法核实该倍数对应的具体硬件、包集合与测量方法。
- **第三方对比博客的倍数（8x、10x、100x 等）来源不明、样本未公开**，多篇内容高度雷同，**疑似 AI 生成的 SEO 内容**，本组不建议引用其具体数字。
- **Poetry 的当前版本号与 `poetry.lock` 的 `content-hash` 字段细节未逐字核实**。本组未打开 Poetry 官方文档，上表 Poetry 一行的"是/部分"标注为推断。
- **pip-tools 的 `--generate-hashes` 是否会为所有传递依赖生成哈希、以及多平台 wheel 的多哈希行为，未逐字核实**（方向 22 的 pip 官方文档只说"多哈希是可能的"，未说明 pip-compile 默认行为）。
- **conda-lock 的"multi-platform by default"来自官方 CLI 文档摘要**，本组未打开 `conda-lock.yml` 格式规范；`name=version=build_hash` 的说法来自中文博客，**未在官方页逐字核实**。
- **PEP 751 已 Final 但生态落地程度未知**：本组未核实 PyPI 上有哪些安装器已实现 `pylock.toml` 的读取；uv 文档只说"supports `pylock.toml` as an export target and in the `uv pip` CLI"。
- **`uv export --format requirements.txt --no-dev` 的确切 flag 组合未验证**；uv export 的完整选项未逐字读取，上述命令可能在真实环境中报错，**须实测**。
- **未核实**：阙疑 `gate_engine.py`（3826 行）与 595 个 `.py` 工具当前实际依赖了哪些第三方包、其中多少含 C 扩展。这直接决定"锁文件管不到"的风险有多大。
- **未核实**：uv 的 `audit.malware-check` 在查阅日是否已脱离 preview；官方页明确标注 *"On-sync malware checking is in preview, and is subject to change until stabilized."*

---

## 来源

1. PEP 751 – A file format to record Python dependencies for installation reproducibility — https://peps.python.org/pep-0751/ — 逐字：*"no standard exists to create an immutable record, such as a lock file"*；*"The closest the community has to a standard are pip's requirements files… it is not secure by default"*；*"`pip freeze` and pip-tools only generate single-use lock files for the current environment"*；*"But it is not the case that using a different locker will lead to the same result."*；`[packages.archive.hashes]` 规范；*"Tools MUST support wheel files"*；*"Tools MUST NOT use this information when doing installation; it is purely informational for auditing purposes."*；**Status: Final, Resolution: 31-Mar-2025** — Brett Cannon 等 — Created 2024-07-24
2. Structure and files | uv — https://docs.astral.sh/uv/concepts/projects/layout/ — 逐字：*"`uv.lock` is a *universal* or *cross-platform* lockfile that captures the packages that would be installed across all possible Python markers such as operating system, architecture, and Python version."*；*"The `uv.lock` format is specific to uv and not usable by other tools."*；与 `pylock.toml` 的关系（`uv export -o pylock.toml`、`uv pip compile requirements.in -o pylock.toml`）— Astral — 2026-07-21
3. Locking and syncing | uv — https://docs.astral.sh/uv/concepts/projects/sync/ — 逐字：`--locked` *"If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile."*；`--frozen` *"To use the lockfile without checking if it is up-to-date"*；`uv lock --check` *"equivalent to the `--locked` flag"*；*"uv will not consider lockfiles outdated when new versions of packages are released"*；Git 依赖锁 commit SHA；*"`uv sync` performs 'exact' syncing by default, which means it will remove any packages that are not present in the lockfile."*；`uv export --format requirements.txt / pylock.toml / cyclonedx1.5`；`audit.malware-check` 走 OSV（preview）— Astral — 2026-08-05
4. uv（首页 Highlights）— https://docs.astral.sh/uv/ — 逐字：*"A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more."*；*"**10-100x faster** than `pip`."*；终端示例 `Resolved 43 packages in 12ms` / `Installed 43 packages in 208ms` / `Resolved 2 packages in 170ms`；`uv pip compile requirements.in --universal` — Astral — 2026-03-13
5. uv/BENCHMARKS.md — https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md — 逐字：*"Benchmark performance may vary dramatically across different operating systems and filesystems."*；*"Benchmark performance may vary dramatically depending on the set of packages being installed. For example, a resolution that requires building a single intensive source distribution may appear very similar across tools"*；基准对象 Trio `docs-requirements.in`，macOS + Python 3.12.4；**正文仅四张图片，无数字** — Astral — 2026-03-02
6. pip-compile — pip-tools documentation v7.6.1 — https://pip-tools.readthedocs.io/en/stable/reference/pip-compile/ — `pip-compile [OPTIONS] [SRC_FILES]...`；*"To compile from scratch, first delete the existing requirements.txt file"* — Jazzband — v7.6.1，2026-08-11
7. conda-lock — https://github.com/conda/conda-lock 与 CLI Reference https://conda.github.io/conda-lock/cli/gen/ — 逐字：*"Conda lock is a lightweight library that can be used to generate fully reproducible lock files for conda environments. It does this by performing a conda solve for each platform you desire a lockfile for."*；*"Generate fully reproducible lock files for conda environments. By default, a multi-platform lock file is written to conda-lock.yml"* — conda 社区 — 2026-08-12
8. Secure installs — pip documentation v26.2.1 — https://pip.pypa.io/en/stable/topics/secure-installs/ — 哈希校验模式的 all-or-nothing 语义、`--require-hashes`、`--only-binary :all:`、sha256 推荐、`--no-require-hashes`（26.2 新增） — PyPA — 2026-08-04
9. pylock.toml Specification — Python Packaging User Guide — https://packaging.python.org/en/latest/specifications/pylock-toml/ — PEP 751 的现行规范正文位置 — PyPA — 2026-09-22
10. What is PEP 751? — pydevtools — https://pydevtools.com/handbook/explanation/what-is-pep-751/ — 逐字：*"Tools that maintain their own native lockfile often treat pylock.toml as an export target rather than a replacement"* — pydevtools — 2026-09-07（**第三方，非官方**）
11. uv vs pip vs Poetry: Python Package Manager Comparison — https://pkglog.com/en/blog/python-package-manager-comparison-pip-uv-poetry/ 与 https://www.danilchenko.dev/posts/uv-vs-pip-vs-poetry/ — 声称 uv 比 pip 快 10–100x、比 Poetry 快约 10x — **第三方博客，样本与硬件未公开，本组不建议引用其具体数字** — 2026-04 ~ 2026-07
12. Python Package Management in 2026: uv, Poetry, or pip? — https://michael.vu/post/post-2026-02-08-python-packaging-uv-poetry-pip.html — 速度 / 锁文件 / 迁移路径对比 — 第三方 — 2026-02-08（**未逐字核实**）
13. Managing Dependencies in Scientific Python — https://matforge.org/managing-dependencies-scientific-python-lockfiles-environments/ — 逐字：*"If a simulation depends on external APIs or databases that change, reproducibility can break even when the Python [environment is locked]"* — matforge — 2026-06-26（**第三方**）
