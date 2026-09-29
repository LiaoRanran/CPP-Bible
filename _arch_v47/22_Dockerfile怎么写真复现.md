# 方向 22：Dockerfile 怎么写才真复现

## 核心结论

1. **"钉 tag"不算钉版本，只有 `@sha256:` digest 才算。** Docker 官方 Building best practices 用 `ubuntu:24.04` 举例并逐字说明：*"Over time, that tag may resolve to a different underlying version of the `ubuntu` image, as the publisher rebuilds the image with security patches and updated libraries."* 该页专设 "Pin base image versions" 一节，与 `--pull`（取新基础镜像）、`--no-cache`（重跑所有步骤）明确区分——**`--pull` 与 `--no-cache` 是为了"刷新"，不是"复现"**，两者目标相反，不能混用为可复现手段。

2. **BuildKit 提供了完整的"可复现构建"原语，但默认全部关闭。** `SOURCE_DATE_EPOCH` 自 **BuildKit v0.11** 起被 Dockerfile frontend 作为特殊 build arg 支持；`buildctl >= v0.13` 与 **Docker Buildx >= 0.10** 会自动把宿主机的 `$SOURCE_DATE_EPOCH` 透传为 build arg。它控制的是 OCI Image Config 的 `created`、`history` 里的 `created`、Image Index 的 `org.opencontainers.image.created` 注解，以及 `local`/`tar` exporter 的文件时间戳——**但要让镜像内文件时间戳也统一，必须额外加 `rewrite-timestamp=true`（BuildKit v0.13 起）**。另有一个几乎无人使用的杀手级开关：`compatibility-version`，可把"影响 digest 的镜像组装行为"钉到历史路径（`10` = v0.13/0.14，`20` = v0.15–v0.31，`30` = 当前）。

3. **C++ 侧的确定性有三个必须加的编译选项，缺一个就白干。** reproducible-builds.org 明确列出：`-fdebug-prefix-map=OLD=NEW`（所有 GCC 版本、Clang 3.8 起）、`-fmacro-prefix-map=OLD=NEW`（GCC 8、Clang 10 起，解决 `__FILE__`/`assert` 里的路径）、`-ffile-prefix-map=OLD=NEW`（是前两者的别名，GCC 8、Clang 10 起）。**开 LTO 时还必须加 `-frandom-seed`**，否则 GCC 会往目标文件写随机标识符。这三个 flag 是"同一份源码在不同目录下编译出同一二进制"的充要前提，对阙疑这种要在审稿人机器上复算判决的系统是刚需。

---

## 精确数字与案例

### 一、基础镜像：tag vs digest

| 写法 | 可复现性 | 说明 |
|---|---|---|
| `FROM python:latest` | 最差 | tag 指向滚动更新 |
| `FROM python:3.12-slim` | 差 | 同一 tag 会随安全补丁重建而变（Docker 官方明示） |
| `FROM python:3.12.7-slim` | 中 | 钉到 patch，但 publisher 仍可重推同一 tag |
| `FROM python:3.12.7-slim@sha256:...` | **最好** | 钉到内容寻址摘要，理论上不可变 |

取 digest 的命令（社区通行做法，本组未在 Docker 官方页逐字核实）：
```bash
docker pull python:3.12-slim
docker inspect --format='{{index .RepoDigests 0}}' python:3.12-slim
# 或
docker images --digests python
```
代价：**钉 digest 后不再自动接收安全补丁**，需要一条定期更新 digest 的流程（Renovate / Dependabot）。对科研复现而言，这个代价是值得付的——**论文要的是"两年后还能跑出同样的数"，不是"永远最新"**。可折中：论文正文声明"复现使用 digest X"，同时另开一个不定期的 `main` 分支跟随最新。

BuildKit 还提供了**不改 Dockerfile 也能钉源**的机制：`--source-policy-file policy.json`（自 BuildKit v0.11 起支持"Reproducing the pinned dependencies"）。policy.json 逐字示例：
```json
{
  "rules": [
    {
      "action": "CONVERT",
      "selector": { "identifier": "docker-image://docker.io/library/alpine:latest" },
      "updates": { "identifier": "docker-image://docker.io/library/alpine:latest@sha256:4edbd2beb5f78b1014028f4fbb99f3237d9561100b6881aabbf5acce2c4f9454" }
    },
    {
      "action": "CONVERT",
      "selector": { "identifier": "https://raw.githubusercontent.com/moby/buildkit/v0.10.1/README.md" },
      "updates": { "attrs": {"http.checksum": "sha256:6e4b94fc270e708e1068be28bd3551dc6917a4fc5a61293d51bb36e6b75c4b53"} }
    }
  ]
}
```
调用：`buildctl build --frontend dockerfile.v0 --local dockerfile=. --local context=. --source-policy-file policy.json`。文档说明：*"Any source type is supported, but how to pin a source depends on the type."* 这意味着 **HTTP 拉取的源码也能钉 checksum**——对阙疑从上游下载 C++ 单头文件库（如 doctest、json.hpp）的场景直接可用。

### 二、apt 版本锁定：语法、通配符与"包被删了怎么办"

Docker 官方 best practices 给的 apt 模板（注意 `--no-install-recommends`、`rm -rf /var/lib/apt/lists/*`、多行按字母序排列）：
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```
但**这个模板本身不可复现**——它没有钉版本。要复现必须写 `=`：

```dockerfile
FROM ubuntu:22.04@sha256:<digest>
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl=7.81.0-1ubuntu1.24 \
      ca-certificates=20240203~22.04.1 \
      git=1:2.34.1-1ubuntu1.17 \
    && rm -rf /var/lib/apt/lists/*
```

**通配符折中**（可维护性更好，复现性稍弱）：`curl=7.81.*`。查可用版本：
```bash
docker run --rm ubuntu:22.04 bash -c "apt-get update && apt-cache policy curl"
```

**最容易被忽略的坑：钉死版本后，该版本可能从仓库被移除。** 一旦 `apt-get update` 的索引里不再有 `curl=7.81.0-1ubuntu1.24`，构建会以 `Version '...' for 'curl' was not found` 失败。标准解法是改用 **snapshot 归档源**（`snapshot.debian.org` / Ubuntu 的 snapshot 服务），把 `sources.list` 指向某个历史时间点。**本组未逐字取到 Debian snapshot 的官方 pin 文档**，此项标为盲区；社区有工具 **dockpin**（https://github.com/Jille/dockpin ）可生成 `dockpin-apt.lock`，其中"contains the URLs and size/hash of each .deb file"，等价于 apt 侧的哈希锁。

**Alpine 侧**：`apk add --no-cache curl=8.14.1-r2 git=2.43.7-r0`。**RPM 侧**：`dnf install -y curl-minimal-7.76.1-40.el9`。

**自动检出**：**hadolint**（https://github.com/hadolint/hadolint ）的四条规则直接覆盖本方向最容易犯的错：
- **DL3006** — Always tag the version of an image explicitly
- **DL3008** — Pin versions in apt-get install
- **DL3013** — Pin versions in pip install
- **DL3018** — Pin versions in apk add

用法：`docker run --rm -i hadolint/hadolint < Dockerfile`，可直接接进 CI 并在有 `DL3xxx` 报错时 fail。

### 三、pip 侧：`--require-hashes` 的真实约束（官方逐字）

pip 官方文档 *Secure installs*（https://pip.pypa.io/en/stable/topics/secure-installs/ ）给出的"安全安装"两件套是 `--require-hashes` + `--only-binary :all:`。哈希校验模式（Hash-checking Mode，pip 8.0 起）的关键约束逐字如下：

- *"Note that hash-checking is an all-or-nothing proposition. Specifying `--hash` against *any* requirement will activate this mode globally."*
- *"Hashes are required for *all* requirements."* 理由：*"a partially-hashed requirements file is of little use and thus likely an error: a malicious actor could slip bad code into the installation via one of the unhashed requirements."*
- *"Hashes are required for *all* dependencies."*（传递依赖也必须逐个列出并哈希，否则直接报错）
- *"Requirements must be pinned (either to a URL, filesystem path or using `==`)."* 理由：*"This prevents a surprising hash mismatch upon the release of a new version that matches the requirement specifier."*
- 推荐算法：**sha256**；*"weaker ones such as md5, sha1, and sha224 are excluded to avoid giving a false sense of security."*
- 多平台需多哈希：*"It is possible to use multiple hashes for each package. This is important when a package offers binary distributions for a variety of platforms"*
- 注意 pip 26.2 起新增 `--no-require-hashes` 用于"只想部分校验"的场景。
- 反模式警告：*"Be careful not to nullify all your security work by installing your actual project by using setuptools' deprecated interfaces directly: for example, by calling `python setup.py install`… These will happily go out and download, unchecked, anything you missed in your requirements file"*。**正确做法**：`python -m pip install --no-deps .`

requirements.txt 里的形态：
```
FooProject == 1.2 \
  --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 \
  --hash=sha256:486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7
```
生成方式（方向 23 会展开对比）：`pip-compile --generate-hashes requirements.in -o requirements.txt`；Dockerfile 里 `RUN pip install --no-cache-dir --require-hashes -r requirements.txt`。

**其他语言的一行对照**（社区整理，非官方）：Node 用 `npm ci` 而非 `npm install`；Go 用 `go.sum` + `go mod download`；Rust 用 `cargo fetch --locked`；Ruby 用 `bundle config set frozen true`。

### 四、C++ 侧的确定性：三个 prefix-map 加一个 seed

reproducible-builds.org *Build path* 页逐字给出编译器侧解法（原文还解释为什么"后处理"不可行）：*"For the specific case of debug symbols, there is currently no good post-processing tool to change them to a pre-determined value… Certain compiler flags can work around the issue"*：

| flag | 作用 | 可用版本（逐字） |
|---|---|---|
| `-fdebug-prefix-map=OLD=NEW` | *"can strip directory prefixes from debug info"* | *"available in all GCC versions, Clang 3.8"* |
| `-fmacro-prefix-map=OLD=NEW` | *"similar to `-fdebug-prefix-map`, but addresses unreproducibility due to the use of `__FILE__` macros in `assert` calls for example"* | *"available since GCC 8 and Clang 10"* |
| `-ffile-prefix-map=OLD=NEW` | *"an alias for both `-fdebug-prefix-map` and `-fmacro-prefix-map`"* | *"available since GCC 8 and Clang 10"* |

Debian 侧的对应开关（dpkg ≥ 1.19.1，Debian Buster 起）：`export DEB_BUILD_MAINT_OPTIONS = hardening=+all reproducible=+fixfilepath`。

**随机性**页逐字给出 LTO 的坑：*"When Link-Time Optimizations are turned on, GCC users will write random identifiers to binary objects they create. Using `-frandom-seed` can be used for this particular case. As it will hash arbitrary data, passing the file name should work in most cases."* 另有通用原则：*"Random data will make builds unreproducible and must be avoided. If random-like input is required, the solution is to use a predetermined value to seed a pseudo-random number generator."*

**这直接对应阙疑的 `PYTHONHASHSEED` 问题**：Python 默认对 str 的 `hash()` 加随机盐，若 `gate_engine.py` 有任何依赖 `set` 迭代顺序的输出（例如 67 条规则的触发顺序、判决理由的拼接顺序），**必须设 `ENV PYTHONHASHSEED=0`**，否则同一账本在不同容器里可能算出不同的哈希链。

### 五、层顺序、非 root 与 CI 验证脚本

**层顺序**（官方 Optimize cache 页明确："Order your layers: Putting…"）：依赖清单先 COPY、源码后 COPY，使依赖层在源码改动时不被失效。
```dockerfile
COPY requirements.lock ./          # 变得少 → 放前面
RUN pip install --no-cache-dir --require-hashes -r requirements.lock
COPY . .                           # 变得多 → 放后面
```
配 `.dockerignore` 排除 `.git`、`__pycache__`、`*.md`、测试夹具的大文件——官方逐字：*"To exclude files not relevant to the build, without restructuring your source repository, use a `.dockerignore` file."*

**非 root**：官方 userns-remap 文档的原则是 *"The best way to prevent privilege-escalation attacks from within a container is to configure your container's applications to run as unprivileged users."* 社区通行写法：
```dockerfile
RUN addgroup --gid 1001 --system appgroup \
 && adduser  --uid 1001 --system --ingroup appgroup --no-create-home appuser
COPY --chown=appuser:appgroup . .
USER 1001:1001
```
坑：**非 root 不能绑 1024 以下端口**（须改 8080 等）；**写入目录必须提前 `chown`**，否则运行期崩。运行期加固：`--security-opt no-new-privileges:true`、`--cap-drop=ALL`。

**CI 里的可复现性验证**（把"声明"变成"证据"）：连续构建两次并比对镜像 ID/digest：
```bash
docker buildx build --no-cache --load -t queyi:build1 .
docker buildx build --no-cache --load -t queyi:build2 .
docker inspect --format='{{.Id}}' queyi:build1 > /tmp/a
docker inspect --format='{{.Id}}' queyi:build2 > /tmp/b
diff /tmp/a /tmp/b && echo "REPRODUCIBLE" || echo "NOT REPRODUCIBLE"
```
**必须诚实标注的边界**：即使全部钉死，*"层中的时间戳、包管理器的非确定性行为以及构建上下文元数据仍会导致无法逐字节复现"*（社区结论，非官方）。Malka 等人在 1096 个真实镜像上测得**文件级逐位一致仅 4 个**（方向 21），所以**目标应设为"功能可复现 + 产物哈希可复现"，而非"镜像 digest 可复现"**。对阙疑而言，真正要钉的是**账本 Merkle root**（自己算的量，可控），而不是整个镜像 digest。

另外两个值得加进 CI 的动作：**hadolint 静态检查**（上面四条规则）与 **attestation 生成**（`docker buildx build --provenance=true --sbom=true`，Docker 官方 Build attestations 页说明可在 `docker buildx build` 时附加 provenance/SBOM 记录，配合 `BUILDKIT_SBOM_SCAN_CONTEXT` 可扫描构建上下文）。SBOM 是"依赖清单可核验"的机器可读形式，比 README 里的表格更硬。

**最后一条容易被忽视的钉法**：Dockerfile 语法本身。首行写 `# syntax=docker/dockerfile:1.7.0`（而不是 `:1`），避免 BuildKit frontend 行为随版本漂移。

---

## 对阙疑的 3 条具体行动

1. **新建 `Dockerfile`（两段式、全钉 digest）+ `.dockerignore` + `requirements.lock`（2026-11 前）**。骨架：
   - `# syntax=docker/dockerfile:1.7.0` 首行；
   - `ARG SOURCE_DATE_EPOCH=1704067200`（全局作用域默认值，BuildKit 官方支持的写法）；
   - `FROM python:3.12-slim@sha256:<填入> AS deps` → `COPY requirements.lock ./` → `RUN pip install --no-cache-dir --require-hashes -r requirements.lock`；
   - `FROM python:3.12-slim@sha256:<同上> AS runtime` → `apt-get install -y --no-install-recommends g++-13=13.2.0-23 libubsan1=<ver> libasan8=<ver>` → `COPY --from=deps /usr/local/lib/python3.12/site-packages ...` → `COPY --chown=1001:1001 . .` → `USER 1001:1001` → `ENV PYTHONHASHSEED=0 SOURCE_DATE_EPOCH=1704067200`。
   - **digest 填入方式**：`docker inspect --format='{{index .RepoDigests 0}}' python:3.12-slim`，把结果整串写进 `FROM`。

2. **新增 `docker/verify_repro.sh` 与 `.github/workflows/repro.yml`（2026-12 前）**，把"可复现"变成 CI 断言。脚本内容：(i) `hadolint` 扫 Dockerfile，**任何 DL3006/DL3008/DL3013/DL3018 报错即 exit 1**；(ii) `docker buildx build --no-cache --build-arg SOURCE_DATE_EPOCH=1704067200 --output type=image,rewrite-timestamp=true -t queyi:r1 .`，再跑一次 `-t queyi:r2`，比对两次的 `docker inspect --format='{{.Id}}'`；(iii) 关键一步——**比对账本 Merkle root**：`docker run --rm --network=none queyi:r1 python gate_engine.py --replay fixtures/ledger_452.jsonl --print-merkle-root`，与 `fixtures/expected_merkle_root.txt` 做 `diff`。**账本 root 一致是本项目的核心复现声明**（哈希链是精确量，天然可做到逐位一致），镜像 digest 一致只是加分项。

3. **在 `research/` 下新增 `22_deterministic_cpp_build.md`，并在 `Makefile`/`CMakeLists.txt` 落地三个 prefix-map（2027-01 前）**：在 C++ 编译选项中加 `-ffile-prefix-map=$(CURDIR)=/build -frandom-seed=queyi-$(shell git rev-parse --short HEAD)`（若开 LTO 则 `-frandom-seed` 必加）。文档里逐条记录：当前 GCC/Clang 版本是否满足 prefix-map 的最低版本要求（GCC 8 / Clang 10）；若使用 GCC 7 以下则 `-ffile-prefix-map` 不可用、只能退到 `-fdebug-prefix-map`（且 `__FILE__` 问题无解）。同时在 `Makefile` 里加一个 `make repro-check` 目标：连续编译两次到不同临时目录，比对 `sha256sum`，输出 PASS/FAIL。**注意 227 项工作树漂移必须先清掉**（方向 28），否则"两次构建输入不同"会让这个检查永远失败。

---

## 盲区（诚实标注）

- **Debian/Ubuntu snapshot 归档的官方 pin 用法未逐字核实**。本组只取到社区工具 dockpin 的描述，未打开 snapshot.debian.org 的官方文档；"钉死版本后包被移除导致构建失败"的失败率数字也未找到。
- **`compatibility-version` 三个取值（10/20/30）与 BuildKit 版本的对应关系来自 moby/buildkit 的 build-repro.md**，该文件为仓库文档而非发布说明，**可能随 master 变动**；引用时应写"截至查阅日"。
- **`rewrite-timestamp=true` 需要 BuildKit v0.13+**；本组未核实阙疑所用 Docker Desktop / buildx 的实际版本，也**未实测该选项对镜像 digest 的影响**。
- **"hadolint 四条规则编号"来自官方 README 与第三方整理**，本组未逐条打开 hadolint 的 wiki 原文核对措辞（DL3006/DL3008/DL3013/DL3018 的描述为概括，非逐字）。
- **Docker Hub 上的镜像 digest 是否真的不可变，存在理论争议**：摘要寻址原则上不可变，但仓库可被删除/私有化。方向 21 的实测（3620 个历史镜像中 2079 个失联）说明**可用性比不可变性更脆弱**。
- **C++ 侧未核实**：阙疑实际使用的 GCC/Clang 版本是否 ≥ GCC 8 / Clang 10（决定 `-ffile-prefix-map` 是否可用）；`-frandom-seed` 在未开 LTO 时是否仍有必要（文档只说 LTO 场景）。
- **`PYTHONHASHSEED=0` 是否真的影响阙疑的账本哈希，未做实测**。这是基于"Python str 哈希默认加盐"的通用推断；若 `gate_engine.py` 全程用 `sorted()` 或有序结构，则影响为零。**须实测后再写进论文**。
- **"层中的时间戳…仍会导致无法逐字节复现"这句来自第三方博客**（oneuptime），非 Docker 官方文本；但方向 21 的 arXiv:2601.12811 实测（1096 个镜像中文件级一致仅 4 个）从经验上支持该结论。
- 未核实：`--only-binary :all:` 与含 C 扩展的 Python 包（如 numpy/scipy）在无网络环境下的兼容性。

---

## 来源

1. Building best practices — https://docs.docker.com/build/building/best-practices/ — 逐字：*"Over time, that tag may resolve to a different underlying version of the `ubuntu` image, as the publisher rebuilds the image with security patches and updated libraries."*；"Pin base image versions" 专节；`--pull` 与 `--no-cache` 的语义区分；apt 多行排序模板；*"To exclude files not relevant to the build, without restructuring your source repository, use a `.dockerignore` file."* — Docker Inc. — 持续更新
2. Build reproducibility（moby/buildkit `docs/build-repro.md`）— https://github.com/moby/buildkit/blob/master/docs/build-repro.md — 逐字：*"Reproducing the pinned dependencies is supported since BuildKit v0.11."*；`policy.json` 完整示例；*"The Dockerfile frontend supports consuming the `SOURCE_DATE_EPOCH` value as a special build arg, since BuildKit 0.11."*；`ARG SOURCE_DATE_EPOCH=1704067200`；`SOURCE_DATE_EPOCH=context`；*"The `buildctl` CLI (>= v0.13) and Docker Buildx (>= 0.10) automatically propagate…"*；`rewrite-timestamp=true`（BuildKit v0.13）；`compatibility-version` 10/20/30 — BuildKit 项目 — 截至查阅日
3. SOURCE_DATE_EPOCH specification — https://reproducible-builds.org/docs/source-date-epoch/ — 定义与各语言读取示例；完整支持工具含 `docker buildx >= 0.10`、`gcc >= 7`、`clang >= 16.0.0` — reproducible-builds.org — 持续更新
4. Build path — https://reproducible-builds.org/docs/build-path/ — 逐字：`-fdebug-prefix-map` *"available in all GCC versions, Clang 3.8"*；`-fmacro-prefix-map` *"available since GCC 8 and Clang 10"*；`-ffile-prefix-map` *"an alias for both… available since GCC 8 and Clang 10"*；Debian `reproducible=+fixfilepath` — reproducible-builds.org — 持续更新
5. Randomness — https://reproducible-builds.org/docs/randomness/ — 逐字：*"When Link-Time Optimizations are turned on, GCC users will write random identifiers to binary objects they create. Using `-frandom-seed` can be used for this particular case."* — reproducible-builds.org — 持续更新
6. Secure installs — pip documentation v26.2.1 — https://pip.pypa.io/en/stable/topics/secure-installs/ — 逐字：*"hash-checking is an all-or-nothing proposition"*；*"Hashes are required for *all* requirements."*；*"Hashes are required for *all* dependencies."*；*"Requirements must be pinned"*；sha256 推荐；`--no-require-hashes`（26.2 新增）；*"Be careful not to nullify all your security work by installing your actual project by using setuptools' deprecated interfaces directly"* — Python Packaging Authority — v26.2.1，2026-08-04
7. Optimize cache usage in builds — https://docs.docker.com/build/cache/optimize/ — 逐字：*"Mounted files are not persisted in the final image."*；apt/pip/go/cargo cache mount 示例 — Docker Inc. — 持续更新
8. hadolint — https://github.com/hadolint/hadolint — DL3006 / DL3008 / DL3013 / DL3018 规则；`docker run --rm -i hadolint/hadolint < Dockerfile` 用法 — hadolint 项目 — 持续更新
9. dockpin — https://github.com/Jille/dockpin — 逐字：*"you can run dockpin apt pin which generates dockpin-apt.lock, which contains the URLs and size/hash of each .deb file"* — Jille Timmermans — 未标注日期
10. How to Pin Package Versions in Dockerfiles for Reproducible Builds — https://oneuptime.com/blog/post/2026-02-08-how-to-pin-package-versions-in-dockerfiles-for-reproducible-builds/view — digest pinning / apt `=` 与通配符 / apk / dnf / pip `--generate-hashes` / `# syntax=docker/dockerfile:1.7.0` / 构建两次比对 `.Id` 的验证脚本；*"目标是功能可复现（行为一致），而非位级一致"* — OneUptime — 2026-02-08（**第三方博客，非官方**）
11. Build attestations — https://docs.docker.com/build/metadata/attestations/ — `--provenance` / `--sbom` / `BUILDKIT_SBOM_SCAN_CONTEXT` 说明 — Docker Inc. — 持续更新
12. Isolate containers with a user namespace — https://docs.docker.com/engine/security/userns-remap/ — 逐字：*"The best way to prevent privilege-escalation attacks from within a container is to configure your container's applications to run as unprivileged users."* — Docker Inc. — 持续更新
13. How to Run Docker Containers as Non-Root Users — https://oneuptime.com/blog/post/2026-01-16-docker-run-non-root-user/view — `USER` / `COPY --chown` / 非 root 端口限制 / `no-new-privileges` — OneUptime — 2026-01-16（**第三方博客**）
14. Reproducible Builds（总站与文档索引）— https://reproducible-builds.org/ 与 https://reproducible-builds.org/docs/ — 文档树含 SOURCE_DATE_EPOCH、build-path、randomness、stable-outputs、locales、timezones 等条目 — reproducible-builds.org — 持续更新
