# CPP-Bible 全面升级与优化方案

> 制定日期：2026-08-30
> 关联文档：[REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md](REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md)（现状与风险基线）
> 原则：规范化、严谨化、极致化、工程化。所有动作可验证、可回滚、可追溯；每阶段先清零债务再加固。

## 0. 目标总览

| # | 目标 | 现状基线 | 理想终态 |
|---|------|----------|----------|
| 1 | 整体质量与成熟度 | quality 16/16、compile 5/5、Mermaid 511/511，但有 30 WARN、55+7 引用/拓扑债务、事实源冲突 | 门禁全绿且无基线债务；所有指标由单一事实源生成；零静默假绿 |
| 2 | UI / 交互体验 | MkDocs Material indigo，明暗主题 + 徽章 CSS 已就位；无品牌资产、首页与时文搜索优化弱 | 品牌化主题、信息密度与可读性俱佳、导航/搜索/阅读体验达到领先文档站点水准 |
| 3 | 工具链升级 | GCC 15.3.0 已钉；Actions 版本滞后（Node20 弃用）；依赖无锁文件；镜像未钉 digest | 依赖锁定 + 容器 digest 固定 + Actions 全最新 + pre-commit/自动格式化链 |
| 4 | 技术债务 | 见审计报告 §7（P0 剩余：备份第二故障域、工作树收口；P1/P2 多项） | 债务清零或全部显式分级豁免，且有自动防回归 |
| 5 | 环境配置 | toolchain.toml 唯一事实源（优）；devcontainer/Dockerfile 存在但未钉 digest；无 bootstrap、无环境矩阵文档 | 一键 bootstrap（win/wsl/linux/ci）；开发/测试/发布环境可复现切换并留档 |
| 6 | 参考优秀项目前端 | 站点已含徽章/明暗主题 | 首页 hero、搜索增强、阅读体验组件对齐头部文档项目，并归档参考清单 |
| 7 | 规范与流程 | AGENT/CONVENTIONS/CONTRIBUTING/GOVERNANCE 已存在 | PR/Issue 模板、分支与发布流程、代码审查清单、维护手册全部制度化 |

## 1. 现状-差距-行动矩阵

### 1.1 目标 1：整体质量与成熟度（P0）

| 差距 | 行动 | 验收 |
|------|------|------|
| README/STATE/ISSUES/AGENT 指标互相冲突 | 建立 `metrics.schema.json` 单一事实源；生成器统一产出 README 徽章表、STATE、ISSUES | 五份文档指标一致；`gen_metrics --check` 进 CI |
| 30 个一致性 WARN（立场标签缺失） | 逐章补 `[标准]/[实现]/[平台]/[经验]` 或显式豁免 | WARN=0 或全部显式分级 |
| 55 悬空章号 + 7 前置问题 | 旧编号→现章号映射表 + 批量回填 + 人工语义抽查 | dangling=0、topology=0，转硬门禁 |
| 编译覆盖仅约 55%、55 断言 WARN | 片段分类（可独立/同章组合/多文件/平台/故意失败）并逐项建 gate | 覆盖 ≥80%；WARN 全分类 |
| 缺 LICENSE/SECURITY/CODEOWNERS | 按用户裁决的许可条款落地 LICENSE + SECURITY.md + CODEOWNERS | 文件落库且与 pyproject 一致 |
| 1380 条 legacy 审计候选项未复核 | audit_cpp_defects 报告按 part 分派人工复核，逐项留 owner/日期 | 高风险项清零或显式豁免 |

### 1.2 目标 2 + 6：UI 与参考项目（P1）

| 差距 | 行动 | 验收 |
|------|------|------|
| 无品牌资产（logo/favicon/配色语义） | 定制 primary/accent 主色 + SVG logo + favicon；统一 bad 体系 | 站点有品牌一致性 |
| 首页为默认列表，无 hero | 设计 hero：简介 + 快速开始 + 统计徽章 + 章节导览 | 首页可一眼获取信息 |
| 搜索仅靠 pagefind 默认 | 启用 `search` 插件 + 快捷键 + 高亮；评估离线全文检索 | 全文搜索体验对齐 docs 站 |
| 导航深度不足 | 启用 `navigation.sections`/`navigation.expand`，右侧 TOC 折叠优化 | 长章节导航不迷失 |
| 代码阅读体验 | 行号、高亮主题（暗色适配）、复制按钮已有，加 block caption 与可折叠 | 代码区可读性提升 |
| 无明显参考归档 | 建立 `docs/design/references.md`：docs.rs/Bazel/TensorFlow/LearnCpp/Material Showroom 逐组件对照 | 参考清单 + 截图归档（用户协助收集） |

### 1.3 目标 3：工具链升级（P0）

| 差距 | 行动 | 验收 |
|------|------|------|
| Actions 版本滞后触发 Node20 弃用 | `checkout@v5`、`upload-artifact@v5`（setup-python@v5、deploy-pages@v4、upload-pages-artifact@v3 保留） | CI 无 Node20 弃用告警 |
| 依赖无锁文件 | 以 uv 或 pip-tools 生成锁定文件（含 markdown/pandoc/动态约束）；`toolchain.toml` 保持路径事实源 | `pip install -r requirements.lock` 可复现 |
| 容器镜像浮动 | Dockerfile/CI 钉 `gcc:15.3.0@sha256:...` | digest 固定 |
| 无静态检查链 | 安装 ruff/mypy + pre-commit hooks（ruff/mypy/trailing-whitespace/end-of-file） | `pre-commit run --all-files` 全绿 |
| python>=3.11 未锁定解析器 | toolchain.toml 增加版本校验，CI 与本地同一 3.13.x | 版本漂移即失败 |

### 1.4 目标 4：技术债务（承接审计报告 §7/§8）

| 优先级 | 行动 |
|--------|------|
| P0 | 备份复制到加密外置介质/对象存储并做独立恢复演练 |
| P0 | 冻结工作树：把「审计修复」「内容批改」「报告/工具」拆分为可审阅 commits（分支+PR） |
| P1 | ✅ 统一 D5 覆盖口径（113 vs 119 → 119/147，标题正则收口）；章节筛选已修正（147） |
| P1 | ✅ 解锁发布依赖：`deploy` 等待 site/pdf/epub 全成功（已推送，远端验收中） |
| P2 | 仓库卫生：清理跟踪的二进制/输出、归档根目录一次性脚本 |
| P2 | CI 增加 gitleaks、pip-audit、SBOM 动作 |

### 1.5 目标 5：环境配置（P1）

| 差距 | 行动 | 验收 |
|------|------|------|
| 无一键 bootstrap | `bootstrap.ps1` + `bootstrap.sh`：探测工具链→建 venv→装锁定依赖→自检→提示 | 新机器 ≤5min 就绪 |
| dev/test/prod 切换未文档化 | 建立 `docs/engineering/environments.md`：DEV(本机)/CI/RELEASE 三态差异矩阵 | 文档可对照执行 |
| devcontainer 未钉 digest、缺扩展 | Dockerfile 钉 digest；devcontainer 补 Python/C++/CMake 扩展与 postCreate 脚本 | VS Code 容器 1 键就绪 |
| 无环境变量约定 | `.env.example` + `toolchain.toml` 预留 `CPPBIBLE_*` 覆盖 | 行为与文档一致 |

### 1.6 目标 7：规范与流程（P1）

| 行动 | 验收 |
|------|------|
| `.github/PULL_REQUEST_TEMPLATE.md`：变更描述/门禁自检/风险/测试勾选 | 每个 PR 强制结构 |
| `.github/ISSUE_TEMPLATE/`：bug / 内容勘误 / 章节新增 / 性能议题 | 可分类流转 |
| `docs/engineering/branching.md` + `releasing.md`：分支策略、发布 checklist（tag/CHANGELOG/资产/双门禁） | 发布可逐步照做 |
| `docs/engineering/review-checklist.md`：代码+内容双轨审查清单 | 评审标准统一 |

## 2. 分阶段实施

### 阶段 A（立即，2026-08-30 ~ 09-02）：基础设施与合规【进行中】
1. ✅ Actions 版本升级、pre-commit、PR/Issue 模板、SECURITY.md、bootstrap 脚本、`.env.example`。
2. ✅ LICENSE 按用户裁决（MIT）落地并消除 README/pyproject 冲突。
3. ✅ 依赖锁定：`uv.lock` + `requirements.lock.txt`，CI site job 改为锁定安装。
4. ⬜ 指标事实源 `metrics.schema.json` + 生成器（将 README/STATE 接入）。
5. ⬜ 备份第二故障域（需用户提供介质/对象存储）。
出口：门禁无新增告警；新机器可一键 bootstrap；合规文件齐备。

### 阶段 A+（追加，2026-08-30）工具栈升级 · 门禁 · 前端工具
1. ✅ 新门禁 `cppbible env`（工具链自检，接入 bootstrap）。
2. ✅ 前端工具 `tools/site_audit.py`（站点产物健康自检，接入 CI site job，含 fixture 自测）。
3. ✅ 内容债任务单 `docs/references/content_debt_tasklist.md`（55 悬空 + 7 前置 + 30 WARN 明细与执行顺序，作为"接手干活"的落地分析产物）。
4. ✅ CI 所述变更经远端 Actions 验收（`b90fa5d` run 33304567016：quality / GCC-15 / Clang-19 / publish-check / site / pdf / epub / deploy 八 job 全绿，#373 起绕过发布的 P0 风险闭环）。

### 阶段 B（短期，09-03 ~ 09-30）：债务清零与指标统一【提前推进中】
1. ✅ 30 WARN 清零（徽章载体误报，修工具）、55+7 引用/拓扑清零并转硬门禁。
2. ✅ 依赖锁文件（uv.lock + requirements.lock.txt）；D5 口径统一（113/119 → 119/147，标题正则收口）；容器 digest 待钉。
3. ⬜ legacy 审计候选项分批人工复核（每批提交 + 记录）。
4. ✅ 工作树按主题拆分提交并推送验收 CI 新依赖图（`b90fa5d` 八 job 全链路真绿，含 epub OOM 根因修复：13MB 单本 pandoc 峰值>7GB → --by-part 分册）。
出口：门禁全绿且无基线债务；CI 无可复现漂移。

### 阶段 C（中期，10-01 ~ 11-15）：内容深化与质量收口【经用户裁决：内容优先，UI 延后】
1. 30 WARN 立场标签清零、55+7 引用/拓扑债务清零并转硬门禁（从阶段 B 承接）。
2. legacy 审计候选项（10 unsafe C / 94 裸 new / 101 reinterpret_cast 等）逐批人工复核并留档。
3. 示例/练习内容深化：可独立编译覆盖率 55%→80%；断言 WARN 分类与豁免收敛。
4. D5 覆盖口径统一（113/119）、README/STATE/ISSUES 接入单一指标事实源。
5. UI 轻量精修（品牌配色/logo/首页 hero/搜索增强）仅在不影响内容质量前提下并行。
出口：内容与质量指标到达目标值；界面做轻量统一不阻塞内容工作。

### 阶段 D（长期，11-16 ~ 2027-02）：工程化收口
1. 运行期/sanitizer/Clang 转分级硬门禁；跨平台构建复现。
2. 3-2-1 备份制度；发布供应链治理（SBOM/签名）。
3. 维护手册以可执行检查代替手工状态。
出口：工程成熟度达到行业领先，可持续演进。

## 3. 资源需求清单（请协助收集）

### 3.1 参考书目（可按需提供关键章节/笔记）【✅ 已收集 6 本，登记见 docs/references/INDEX.md】
| 用途 | 书籍 | 状态 |
|------|------|------|
| 内容权威校准（C++ 语义复审） | Scott Meyers《Effective Modern C++》；Bjarne Stroustrup《A Tour of C++》 | ✅ 已收集（Effective C++ / A Tour of C++ / C++ Primer 5th / 3rd 中文 / C++(Will)） |
| 工程实践 | 《The Pragmatic Programmer》；《Software Engineering at Google》（中文版《谷歌软件工程》） | ✅ 已收集（Software Engineering at Google 英文版） |
| 文档工程 | 《Docs for Developers》（Jared Bhatti 等）；《Writing ...》→ 以 docs-as-code 范式为主 | ⬜ 未收集 |
| 设计 / UI | 《Refactoring UI》(Adam Wathan)；《Designing Interfaces》 | ⬜ 未收集 |

### 3.2 参考项目 / 网站（站点 UI 与交互对照）【⚠️ 已收到 6 张截图，来源待标注】
- 文档导航与搜索：docs.rs（Rust）、Bazel Docs、TensorFlow Docs、python.org 文档、cppreference（密度参照）
- 主题与组件：squidfunk/mkdocs-material Showroom、pymdown-extensions 用例站、VitePress/VuePress 文档站
- 内容组织：LearnCpp（进阶教程站）、C++ Core Guidelines（Github pages 站点）
- 具体需求：以上每个站点的「首页、章节页导航、代码块、搜索框、暗色模式」截图各 1-2 张 —— **6 张截图已收到并登记（docs/references/INDEX.md），来源暂未标注；因 UI 阶段延后，待后续阶段再逐一识别与归档对照表**

### 3.3 设计素材 / 授权
- 品牌 logo 源文件或设计需求；官方 CJK 字体（如 Noto Sans SC / Misans / HarmonyOS Sans）授权确认
- 首页 Hero 配图（可接受自绘矢量图）

### 3.4 基础设施
- 第二故障域目标：加密外置盘 / 对象存储（S3/OSS）凭证与空间（约 100 MiB）
- npm/pip 镜像可达性（用于锁定文件与安装验证）

## 4. 关键决策（已裁决）

| 项 | 裁决 | 状态 |
|----|------|------|
| 1. 许可证 | **MIT 开源**（与 pyproject 一致；README 同步，消除 CC BY-NC-SA 冲突） | ✅ 已落地：新增 `LICENSE`（MIT），README 许可行已改 |
| 2. 依赖锁定工具 | **uv**（uv.lock + `uv sync --extra dev --extra ci`） | ✅ 已生成 `uv.lock`（45 包），bootstrap 已改 uv 优先 |
| 3. UI 升级深度 | **先搞内容**：内容/质量优先，UI 延后至内容质量收口后 | 🔄 阶段 C 调整为"内容深化与质量收口"，UI 顺延 |
| 4. 推进优先级 | **工具链→质量→环境→规范→UI**（同方案默认） | ✅ 按此顺序执行 |

## 5. 风险与护栏

- 工作树大量未提交：任何升级动作先分支、先提交隔离，禁止直接改 120 章内容。
- 所有自动修改必须可逆：脚本幂等 + `--check` 模式 + pre-commit。
- 涉及合规（LICENSE/SECURITY）先裁决再落库。
- UI 改动必须双主题（明/暗）回归 + 打印产物无回归。
- 每个阶段出口都有明确验收指标，未达标不进入下一阶段。