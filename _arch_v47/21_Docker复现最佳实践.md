# 方向 21：Docker 复现最佳实践

## 核心结论

1. **Docker 不等于可复现——这是 2026 年有实测论文背书的结论，不是经验之谈。** Malka、Zacchiroli、Zimmermann（LTCI, Télécom Paris, Institut Polytechnique de Paris）的 *Docker Does Not Guarantee Reproducibility*（arXiv:2601.12811，2026-01）对 **5298 个 2023 年 7–10 月成功构建的 GitHub Actions Docker 构建**做了重放：不到两年后**只有 3836 个仍能构建成功，可重建率 72%**；并且**没有任何一个镜像与其历史版本输出哈希相同**（*"none of the images we built have the same output hash as their historical counterpart"*），原因是全部工作流都**没有使用 `SOURCE_DATE_EPOCH`**。

2. **"能构建"和"逐位一致"之间的鸿沟大到必须分开声明。** 同一论文的四档指标（分母 1096 个可比对镜像）：**文件级逐位一致仅 4 个**；**包版本完全一致仅 70 个**；minor 版本一致 **271 个**；major 版本一致 **406 个**；仅包名一致 **573 个**。且在成功重建的镜像中，**一半镜像有超过 34.4% 的文件哈希不同**。对阙疑的启示：论文里必须明确说"我们保证的是哪一档"，否则审稿人会按最严档要求。

3. **提高可复现性的最大杠杆是"减少外部可变输入"，而不是"写更漂亮的 Dockerfile"。** 论文中的官方镜像对照组（`docker-library/official-images`，121 个 2023 年 Dockerfile）重建成功率 **106/121 = 88%**，比宽生态的 72% **高出 16 个百分点**。官方镜像的做法就是：基础镜像受控、依赖显式、构建上下文完整。反例是论文里总结的失败模式——*"temporal failures that emerge over time due to dynamic changes in external dependencies, such as updates to base images, third-party libraries, or environmental settings—occurring without any modifications to the Dockerfile itself"*。

---

## 精确数字与案例

### 一、Docker 构建失败率的历史基线（三个独立研究）

| 研究 | 样本 | 失败率 | 出处 |
|---|---|---|---|
| Cito et al. | 随机抽取 **560** 个 Dockerfile | **34%** | MSR 2017，DOI 10.1109/MSR.2017.67；另统计 **7914 个含 Dockerfile 的 GitHub 仓库** |
| Shabani et al. | 约 **18 000** 个 Dockerfile | **55%** | 经 arXiv:2601.12811 Related Work 转引（本次未直读原文） |
| *An Empirical Study of Build Failures in the Docker Context* | **857 086** 次 Docker 构建，来自 **3828** 个开源项目 | **17.8%** 整体构建失败率；**85.2%** 的项目至少出现过一次构建失败 | MSR 2020，DOI 10.1145/3379597.3387483 |
| Malka et al.（重放） | 5298 个曾成功构建的 job | 两年后 **28% 无法重建**（即 72% 可重建） | arXiv:2601.12811，2026-01 |

注意口径差异：17.8% 是"单次构建失败率"（含开发期试错），34%/55% 是"随机抽样 Dockerfile 能否跑通"，28% 是"曾经成功过、后来失败"。**向论文里引用时必须写清口径**，否则会被认为夸大。

Malka 等人的失败归因很反直觉：**5298 个失败 job 里只有 43 个可归因于基础镜像不可用**（其中仅 2 例可能是私有镜像）。也就是说，"Docker Hub 删镜像"不是主因，**真正的主因是依赖解析在时间轴上漂移**。这与 SC8 那条被引原文一致：*"images that are not pulled by anyone from Docker Hub for extended periods of time get purged, and Dockerfiles are not guaranteed to build indefinitely"*。

### 二、逐位可复现（bit-for-bit）的实测比例

arXiv:2601.12811 给出的完整漏斗（分母 1096 个"两版都拿到"的镜像）：

| 复现严格度 | 达标镜像数 | 占比 | 逐字依据 |
|---|---|---|---|
| 输出哈希完全相同 | **0** | 0% | *"none of the images we built have the same output hash as their historical counterpart."* |
| 全部文件逐位一致 | **4** | 0.4% | *"only 4 images have all their files bitwise reproducible with their historical version"* |
| 包版本完全一致 | **70** | 6.4% | *"only 70 of the compared images achieve full reproducibility"* |
| minor 版本一致 | **271** | 24.7% | *"still only a minority of 271 out of 1096 images are reproducible under this prism."* |
| major 版本一致 | **406** | 37.0% | *"406 images are reproducible, with a median of 1% packages changing major version."* |
| 仅包名一致 | **573** | 52.3% | *"573 images out of 1096 contain the same packages as their counterpart, without accounting for versions."* |

另一半数据同样刺眼：*"half of the images that were successfully rebuilt in our dataset have more than 34.4% of files with differing hashes"*，以及 *"at least 22.6% of packages changing version between the original and rebuilt images in half of the cases"*。

回归模型拟合度（RQ3）：**R² = 0.05（可重建性）/ 0.27（文件可复现）/ 0.12（精确版本）/ 0.10（minor）/ 0.08（major）**，所有模型 p < 0.05，但 *"some pinning rules appearing to contribute negatively to the reproducibility rate for some metrics, but with very small effect size (below 3%)"*——**"钉版本"本身不是万能药**，效应量小于 3%。

另外：**3620 个历史镜像中 2079 个在分析时已无法访问**（仅取回 1541 个）。这直接说明"把镜像推到 Docker Hub 就完事"是不成立的长期归档策略。

### 三、`SOURCE_DATE_EPOCH`：唯一被官方标准化的"时间戳锁"

reproducible-builds.org 的规范（https://reproducible-builds.org/docs/source-date-epoch/ ）逐字定义：*"`SOURCE_DATE_EPOCH` is a standardised environment variable that distributions can set centrally and have build tools consume this in order to produce reproducible output. In practice, `SOURCE_DATE_EPOCH` specifies the last modification of something, usually the source code, measured in the number seconds since the Unix epoch, ie. `January 1st 1970, 00:00:00 UTC`."* 语义：*"if the user has set `SOURCE_DATE_EPOCH` then they are taking a position that 'this **is** the current time; please use this instead of whatever clock you normally use'."*

官方支持清单里与本项目直接相关的是 **`docker buildx >= 0.10`**（完整支持）、**`gcc >= 7`**、**`clang >= 16.0.0`**、**`cmake >= 3.8.0`**。C++ 侧的关键点：**GCC 从 7 起、Clang 从 16 起才完整支持 `SOURCE_DATE_EPOCH`**——若阙疑的镜像用 `gcc-11`/`clang-15` 以下版本，`__DATE__`/`__TIME__` 宏和调试段里的时间戳会让编译产物不可复现。

Docker 官方文档（https://docs.docker.com/build/ci/github-actions/reproducible-builds/ ）给出的标准写法：*"Setting the environment variable for a build makes the timestamps in the image index, config, and file metadata reflect the specified Unix time."* 两种推荐值——**固定 0**（Unix epoch）或**取 Git commit 时间戳**：

```yaml
      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV
      - name: Build
        uses: docker/build-push-action@v7
        with:
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

规范还给出一个**容易被忽略的坑**：Debian binNMU 场景下 `SOURCE_DATE_EPOCH` 会被**加 1**，因为 *"Not increasing the date breaks `rsync` without the `--checksum` option"*。并**强烈不推荐** `FORCE_SOURCE_DATE`（*"We **strongly discourage** the usage of such variable"*）。

### 四、多阶段构建 + BuildKit：能拿到什么，拿不到什么

**BuildKit 自 Docker 23.0+ 起为默认构建器**，legacy builder 已实质废弃。它带来三项对复现性有直接作用的能力：

1. **惰性阶段解析**：BuildKit 只构建目标阶段依赖的阶段。因此可以安全地把 `test` 阶段夹在 `builder` 与 `production` 之间：CI 跑 `docker build --target test .` 做验证，发布跑 `docker build --target production .`，**生产构建不会执行测试阶段**。
2. **并行阶段执行**：互不依赖的阶段并发构建。
3. **缓存挂载（cache mount）**：官方文档（https://docs.docker.com/build/cache/optimize/ ）给的 Python/apt 写法是 `RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt` 与 `RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt update && apt-get --no-install-recommends install -y gcc`。文档同时警告：*"Mounted files are not persisted in the final image. Only the output of the RUN instruction is persisted in the final image."*

**必须清醒的边界**：缓存挂载是**性能**手段，**不是复现性手段**——它只影响速度，不改变解析到的版本。真正影响复现性的是版本锁定（方向 23）与 digest 钉死（方向 22）。

**多阶段构建对"复现"的唯一硬价值**是：把构建工具链与运行环境分离，使**运行镜像的输入集合变小**。官方最佳实践清单（社区整理，非 Docker 官方文本，需谨慎引用）：*"Use specific base image tags"*、*"Order stages by stability"*、*"Minimize the number of COPY instructions"*、*"Use the smallest possible base image for your final stage (e.g., alpine, distroless, or scratch)"*、*"Leverage BuildKit's cache mounts for package managers in build stages"*。

### 五、常见反模式（可直接做 lint 规则）

| 反模式 | 后果 | 检出方式 |
|---|---|---|
| `FROM ubuntu:latest` / 只用 tag 不钉 digest | tag 可变，同一 Dockerfile 在不同时间产出不同镜像 | 正则扫 `FROM .*:(latest\|[^@]*)$`（无 `@sha256:`） |
| `RUN apt-get update && apt-get install -y gcc` 不钉版本 | 解析到当时最新版，随仓库更新漂移 | 检查 `apt-get install` 是否带 `=` |
| `pip install -r requirements.txt` 用无哈希的宽约束 | 上游发新版即漂移 | 见方向 23 的 `--require-hashes` |
| 未设 `SOURCE_DATE_EPOCH` | 镜像 index/config/文件 mtime 每次不同，哈希永不一致 | CI 中 `docker inspect` 比对 mtime |
| 以 root 运行最终进程 | 安全告警 + 权限相关的非确定性行为 | 缺 `USER` 指令即报 |
| 把 secret 写进 `ARG`/`ENV`/中间层 | 层不会被删除，`docker history` 可读 | 用 `--mount=type=secret` 替代 |
| `ADD` 远程 URL | 内容随上游变化，且不可缓存校验 | 禁止 `ADD http` |
| 把构建上下文整目录 `COPY . .` | 上下文含 `.git`、测试数据、大文件；缓存频繁失效 | 需 `.dockerignore` |
| 镜像只推 Docker Hub 不另存 | 长期不可用（实测 3620 → 2079 失联） | 需 DOI/Zenodo/Software Heritage 备份 |

Docker Hub 的可用性约束也是反模式的现实基础：官方文档（https://docs.docker.com/docker-hub/usage/pulls/ ）说明未认证与 Docker Personal 用户受 **6 小时拉取速率限制**（社区实测 2026 年未认证 **100 次/6 小时**、免费账户 **200 次/6 小时**，本组未逐字核实官方页数值）。审稿人若在受限网络下复现，很容易撞上。

**离线性测试**是检验"是否真的自包含"的最狠手段：`docker build --network=none .` 与 `docker run --network=none <img>`。若构建必须联网（几乎总是如此，因为要装依赖），正确做法是**分两段验证**：构建阶段允许联网但必须钉死 digest/版本；运行阶段强制 `--network=none`，证明**运行时不偷偷下载任何东西**。这一条对阙疑尤其关键——"第三方可不信任内核地复算"要求运行期完全离线可算。

---

## 对阙疑的 3 条具体行动

1. **在仓库根目录新增 `Dockerfile` + `docker/verify_repro.sh`，采用"钉 digest 的两段式"结构（2026-11 前完成）**：第一段 `FROM python:3.12-slim@sha256:<digest> AS base` 用于构建，第二段 `FROM gcr.io/distroless/python3-debian12@sha256:<digest>` 或同样钉 digest 的 slim 作为运行段，`COPY --from=base` 只搬 `gate_engine.py` 与锁定依赖。运行段必须写 `USER 65532:65532`（非 root）、`ENV PYTHONHASHSEED=0`、`ENV SOURCE_DATE_EPOCH=0`。`verify_repro.sh` 内容固定为：`docker buildx build --load -t queyi:verify .` → `docker run --rm --network=none queyi:verify python -m pytest -q` → `docker run --rm --network=none queyi:verify python gate_engine.py --replay fixtures/ledger_452.jsonl --print-merkle-root` 并把输出与仓库内 `fixtures/expected_merkle_root.txt` 做 `diff`。**脚本退出码必须作为 CI 的判定依据**。

2. **修好 sanitizer 并把它纳入镜像（2026-12 前）**：当前 GCC `cannot find -lubsan`、Clang 缺 `libclang_rt.asan_dynamic_runtime_thunk.a`。在 Dockerfile 里显式装 `apt-get install -y --no-install-recommends gcc-13 g++-13 libubsan1 libasan8`（版本号须用 `=` 钉死具体补丁号，如 `gcc-13=13.2.0-23`），并在 `docker/verify_repro.sh` 中增加一步 `docker run --rm --network=none queyi:verify bash -c "g++-13 -fsanitize=undefined,address -shared-libsan ... && ./a.out"`。**理由**：Docker 是绕过"本机缺库"的最干净路径，而"本机跑不起来"在 E&D 的 *"documented and executable"* 口径下是 desk-reject 风险（方向 20 结论 1）。同时在 `README.md` 增加 `## Reproduce in one command` 一节，把上面那条 `docker run` 原样贴出。

3. **在 `research/` 下新增 `21_container_reproducibility.md`，写清"我们保证到哪一档"，并做一次自测（2027-02 前）**：内容包含 (i) 一张与 arXiv:2601.12811 表 4 同构的声明表——逐行填"哈希一致 / 文件一致 / 包版本一致 / minor 一致 / 包名一致"，**诚实标注阙疑实际达到的档位**（账本哈希链天然应能到"哈希一致"，但 Python 依赖树大概率只能到"minor 一致"）；(ii) 一条 `docker buildx imagetools inspect queyi:verify` 记录的 digest，写进论文附录作为"本文使用的确切镜像"；(iii) 镜像另存一份到 Zenodo 取 DOI（规避 Docker Hub 镜像失联：实测 3620 个历史镜像中 2079 个已不可访问）。**论文正文只声明已验证的那一档**，不要在缺少证据时写 "fully reproducible"。

---

## 盲区（诚实标注）

- **arXiv:2601.12811 是 2026-01 的新预印本，未见同行评审确认**。论文标题本身即结论（"Docker Does Not Guarantee Reproducibility"），可能存在选题偏向（作者是 Debian/Software Heritage 社区成员，Zacchiroli 是 Software Heritage 联合创始人，可能有推动归档工具的立场）。引用时应写明"预印本，未经同行评审"。
- **"Shabani et al. 55% 失败率 / 18 000 个 Dockerfile" 未直读原文**，仅通过 arXiv:2601.12811 的 Related Work 转引，作者与年份未核实。
- **`An Empirical Study of Build Failures in the Docker Context` 的 17.8% / 85.2% 来自搜索结果摘要**（DOI 10.1145/3379597.3387483），本次未逐字打开全文，失败类别分布未获取。
- **Docker Hub 2026 年的具体拉取限额未逐字核实**（官方文档只说"6-hour pull rate limit"，100/200 的数字来自第三方博客）。
- **`docker build --network=none` 能否成功取决于依赖是否已在缓存中**；本组未实测阙疑项目在该模式下是否可构建。**"运行段 `--network=none` 必过"是建议目标，不是已验证事实**。
- **Docker Hardened Images（SLSA Level 3）的信息来自第三方博客**，未在 Docker 官方页核实；引用需谨慎。
- **多阶段构建"最佳实践清单"部分来自第三方聚合站（dockerbuild.com、sesamedisk.com）**，非 Docker 官方文本，本次未找到官方等价清单，引用时应降级为"社区实践"。
- 未核实：`distroless` 镜像是否适合含 C++ 编译产物的运行段（glibc vs musl 兼容性）；阙疑当前 Python 版本与 distroless 的匹配情况。

---

## 来源

1. Docker Does Not Guarantee Reproducibility — https://arxiv.org/abs/2601.12811 （HTML 版 https://arxiv.org/html/2601.12811v1 ；另见 https://upsilon.cc/~zack/research/publications/tr-2025-docker-reproducibility.pdf 与 https://hal.science/hal-05381097v1/document ） — 逐字：*"less than two years later only 3836 are still building successfully, hence resulting in a 72% rebuildability rate"*；*"none of the images we built have the same output hash as their historical counterpart"*；*"only 4 images have all their files bitwise reproducible"*；*"only 70 of the compared images achieve full reproducibility"*；*"half of the images … have more than 34.4% of files with differing hashes"*；*"only 43 failed jobs can be attributed to an unavailable base image"*；*"successfully rebuilding 106, that is 88%… 16 percentage points increase"*；样本 5298 个构建 / 3620 个历史镜像 / 2079 个已失联 / SLR 60 篇 — Julien Malka, Stefano Zacchiroli, Théo Zimmermann，LTCI, Télécom Paris, Institut Polytechnique de Paris — 2026-01-19
2. An Empirical Analysis of the Docker Container Ecosystem on GitHub — https://dl.acm.org/doi/10.1109/MSR.2017.67 — 7914 个含 Dockerfile 的 GitHub 仓库；560 个随机样本 34% 失败率 — Jürgen Cito et al. — MSR 2017
3. An Empirical Study of Build Failures in the Docker Context — https://dl.acm.org/doi/10.1145/3379597.3387483 — 逐字摘要：*"the overall build failure rate in the Docker context is 17.8% and most of Docker projects (85.2%)"*；样本 857 086 次构建 / 3828 个项目 — MSR 2020（作者未核实）
4. Reproducible builds with GitHub Actions — https://docs.docker.com/build/ci/github-actions/reproducible-builds/ — 逐字：*"Setting the environment variable for a build makes the timestamps in the image index, config, and file metadata reflect the specified Unix time."*；YAML 示例含 `docker/build-push-action@v7`、`docker/bake-action@v7`、`SOURCE_DATE_EPOCH: 0` 与 `$(git log -1 --pretty=%ct)` — Docker Inc. — 持续更新
5. SOURCE_DATE_EPOCH specification — https://reproducible-builds.org/docs/source-date-epoch/ — 逐字定义与各语言读取示例；完整支持工具表含 `docker buildx >= 0.10`、`gcc >= 7`、`clang >= 16.0.0`、`cmake >= 3.8.0`；*"We **strongly discourage** the usage of such variable [FORCE_SOURCE_DATE]"*；Debian binNMU 加 1 的说明 — reproducible-builds.org 社区 — 持续更新
6. Optimize cache usage in builds — https://docs.docker.com/build/cache/optimize/ — 逐字：*"Mounted files are not persisted in the final image. Only the output of the RUN instruction is persisted in the final image."*；apt/pip/go/cargo cache mount 官方示例 — Docker Inc. — 持续更新
7. Docker Hub pull usage and limits — https://docs.docker.com/docker-hub/usage/pulls/ — 逐字：*"Unauthenticated and Docker Personal users are subject to a 6-hour pull rate limit on Docker Hub."* — Docker Inc. — 持续更新
8. Docker Multi-stage Builds Reference（社区整理）— https://dockerbuild.com/reference/multi-stage-builds — 多阶段最佳实践清单与 `--target` 用法；`DOCKER_BUILDKIT=1` — 第三方 — 未标注日期（**非官方，引用需降级**）
9. Docker Multi-Stage Builds in 2026（第三方分析）— https://sesamedisk.com/docker-multi-stage-builds-2026 — 逐字：*"BuildKit has become the default builder. Docker 23 and later ship with BuildKit enabled out of the box, and the legacy builder … is effectively deprecated."*；Docker Hardened Images 声称 SLSA Level 3 — 第三方 — 2026
10. Docker Hub 未认证拉取限制仍为 100/6hr — https://bex.co/blog/2026/07/31/docker-hub-pull-limits-self-hosted-registry — 未认证 100 次/6 小时、免费账户 200 次/6 小时 — 第三方博客 — 2026-07-31（**数值未在官方页核实**）
11. Tips for Publishing Research Code（依赖声明形态参考）— https://github.com/paperswithcode/releasing-research-code — 逐字：*"you might want to consider using Docker and upload a Docker image of your environment into Dockerhub"* — Papers with Code — 2021-03-19
