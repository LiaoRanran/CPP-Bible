# CPP-Bible 全量仓库审计与路线图

> 审计日期：2026-08-30  
> 审计对象：`C:\CodeLearnling\note\note\C++\CPP-Bible`  
> Git 基线：`master` / `a941c4ae98631cdfbec194a4a131580f084a8240`  
> 关联文档：《[UPGRADE_PLAN_2026-08-30.md](UPGRADE_PLAN_2026-08-30.md)》为本报告的升级执行路线（7 目标矩阵、阶段 A-D、资源清单）。  
> 说明：数据以当前工作树为准；审计开始时存在 122 个已修改文件和 1 个未跟踪文件，均未被清理或回滚。审计后已按路线图立即处置项应用下述修复（详见 §5/§7/§8）：空白门禁、`ch92` Mermaid 单块、CI 发布依赖图、3 个 legacy 审计工具、`fix_ch36.py` 语法；修复均在工作树，未提交、未推送。

## 1. 执行摘要

仓库已完成仓库外全量备份、SHA-256 复算、全量解包对比、Git bundle 校验和恢复仓库 `git fsck`。备份可以恢复，但当前唯一存储卷是 `C:`，因此只实现了路径和 ACL 隔离，尚未实现异盘、异机或离线故障域隔离。

项目是“C++ 技术书稿 + 大量可执行示例/汇编证据 + Python 质量与发布工具链”。内容规模大、自动化门禁覆盖广，链接、结构、密度、表格、D5 和已绑定汇编证据总体健康。审计后已应用立即处置修复：空白硬门禁、`ch92` Mermaid 单块、CI 发布依赖图、3 个 legacy 审计工具、`fix_ch36.py` 语法；当前 unified quality 已 16/16、Mermaid 511/511、unified compile 5/5，但发布就绪仍受工作树未收口、部分软门禁积债、统计工具口径错误和本地构建依赖不完整制约。

综合判断：**内容资产成熟度较高，工程治理成熟度中等，当前状态为黄色，不应直接发布。**

## 2. 备份与恢复验证

备份目录：`C:\RepositoryBackups\CPP-Bible\20260830-090558`

| 产物 | 大小（字节） | SHA-256 |
|---|---:|---|
| `CPP-Bible-full-20260830-090558.tar.zst` | 67,900,087 | `4c882ab5c762b59be0e3cc606f1bbbf11737322abf55e525c4e284e987408da1` |
| `CPP-Bible-git-20260830-090558.bundle` | 13,938,136 | `988ae03497dc3656030e42f8da3181ed0d1b715212cd3731dfa816d81e44470f` |
| `SHA256SUMS.txt` | 210 | 哈希清单 |
| `backup-metadata.json` | 1,204 | 备份和恢复元数据 |

验证结果：

| 检查 | 结果 |
|---|---|
| 备份期间源稳定性 | 通过 |
| 源清单 | 5,726 文件、1,014 目录、239,128,920 字节 |
| 归档目录项 | 6,741 |
| SHA-256 现场复算 | 两个主产物均与清单一致 |
| 全量恢复文件差异 | 0 |
| 全量恢复目录差异 | 0 |
| 恢复仓库 `git fsck` | 退出码 0；仅报告 4 个可回收 dangling commit，不属于损坏 |
| `git bundle verify` | 通过；9 个 refs，完整历史 |
| ACL | 继承已关闭；仅当前用户、SYSTEM、Administrators 有权限 |

残余风险：

- 机器只有一个文件系统卷，备份与源仓库同机同盘；磁盘损坏、整机丢失和勒索软件仍可同时破坏两者。
- 归档未加密；虽然当前树和 Git 历史的常见令牌/私钥特征扫描均为 0，但本机未安装 `gitleaks`，不能等同于完整秘密扫描。
- 下一步应把两个主产物和校验文件复制到加密外置介质或带版本保留的对象存储，再从该副本做一次独立恢复演练。

## 3. 仓库结构与规模

### 3.1 内容规模

| 指标 | 当前值 |
|---|---:|
| Git 跟踪文件 | 2,034 |
| Git 跟踪内容大小 | 29.52 MiB |
| 正式章节 | 147 章 / 16 part |
| 正式章节行数 | 236,528 |
| `Book` Markdown 总数 | 151（147 章 + 4 个索引/清单文件） |
| C++ 围栏 | 7,530 |
| 含 `main` 的 C++ 围栏 | 4,138（54.9%） |
| 含 `#include` 的 C++ 围栏 | 5,523（73.4%） |
| Mermaid / ASM 围栏 | 511 / 485 |
| 练习 | 705，章中位数 5，零练习章 0 |

主要目录：

| 目录 | 文件数 | 磁盘占用 |
|---|---:|---:|
| `build/` | 2,819 | 152.12 MiB |
| `Examples/` | 1,709 | 28.13 MiB |
| `.git/` | 272 | 22.74 MiB |
| `Book/` | 186 | 13.38 MiB |
| `tools/` | 348 | 3.70 MiB |
| `_asm_demo/` | 166 | 1.57 MiB |

Git 跟踪文件以 1,204 个 `.cpp`、273 个 `.asm`、240 个 `.md`、115 个 `.py` 和 79 个 `.s` 为主。没有跟踪 `.exe` 或 `.pyc`，但仍跟踪 9 个 `.o`、8 个 `.out`、2 个 `.i` 和一个时间戳式日志文件。`build/` 的 152 MiB 已被忽略，说明主要体积是可再生产物，不是 Git 历史膨胀。

### 3.2 目录职责

- `Book/part01_*` 至 `Book/part16_*`：147 个正式章节。
- `Examples/`：章节对应的可编译示例、汇编、输出和部分第三方库示例。
- `_asm_demo/`：用于汇编证据的新鲜度校验的固定编译产物。
- 根目录 `_bench_d5_*.cpp`：D5 性能附录的可复现实验源。
- `Appendix/ub/`：UB 与 sanitizer 反例。
- `tools/`：质量、编译、发布、索引和指标工具；59 个顶层 Python 工具。
- `tools/legacy/`：43 个遗留 Python 工具；其中 3 个（`audit_py_tools.py`、`audit_cpp_defects.py`、`chapter_number_audit.py`）已修复根路径与零输入退出码（见 §5.3）。
- `build/`：站点、报告和临时编译产物，已忽略。
- `.github/workflows/ci.yml`：质量、编译、站点、PDF、EPUB 和 Pages 部署的单一工作流。

## 4. 技术栈与依赖关系

### 4.1 技术栈

- 内容与示例：Markdown、C++17/20/23、少量 C、Rust、Go、Java、C#、Lua 和构建 DSL 示例。
- 主编译器：MinGW-w64 GCC 15.3.0；工具链由 `toolchain.toml` 选择。
- 自动化：Python 3.11+，核心脚本主要使用标准库。
- 站点：MkDocs Material、`mkdocs-mermaid2-plugin`、PageFind。
- 出版：Pandoc、XeLaTeX、`mermaid-filter`、Puppeteer/Chromium。
- CI/CD：GitHub Actions；GCC 15.3.0 容器为主门禁，Clang 19 为软性交叉验证。
- 开发环境：Dockerfile 和 devcontainer 固定 GCC 15.3.0，但镜像未钉 digest。

本机可用 GCC 15.3.0；当前 `python` 是 3.14.5，配置路径名为 3.13.12 的托管解释器实际报告 3.13.14。`cmake`、`pandoc`、`mkdocs`、`ruff`、`mypy` 均不可用。

### 4.2 依赖链

```text
Book/*.md
  -> Examples/*、_asm_demo/*、_bench_d5_*.cpp、Appendix/*、WG21/*
  -> SUMMARY / GLOSSARY / PREREQUISITES / knowledge_graph

tools/cppbible.py
  -> 内容、结构、链接、密度、D5、ASM、空白门禁
  -> compile_all.py -> GCC 15.3.0 -> compile_report.json
  -> compile_gate.py + compile_exempt.json

.github/workflows/ci.yml
  -> quality
  -> compile(GCC hard / Clang soft)
  -> publish-check（链接/资产自检）
  -> site / PDF / EPUB
  -> deploy（Pages）
```

C++ 示例绝大多数只依赖标准库；第三方或平台头以教学案例形式散布，涉及 Boost、fmt、spdlog、nlohmann/json、Qt、Google Benchmark、GoogleTest、LevelDB、RocksDB、Windows 和 POSIX API。仓库没有统一 CMake 工程，当前设计依赖“从 Markdown 抽取代码块并隔离编译”，第三方/多文件/平台示例则通过显式豁免管理。

Python 包声明只有下界，没有锁文件；站点、PDF、Node/Chromium 和系统包也没有统一锁定。这使本地与 CI 的长期复现依赖上游最新版本。

## 5. 质量与文档审计

### 5.1 当前门禁

| 检查 | 结果 | 判断 |
|---|---|---|
| `cppbible.py check --stage quality` | 修复后 16 通过 / 0 失败（审计初为 15/16） | 已全绿 |
| Preflight、索引、术语、结构、围栏 | 通过 | 健康 |
| 一致性 | `ERROR=0 / WARN=30`（口径修正为 147 章后），工具仍退出 0 | 有债务且状态表达偏乐观 |
| 密度 | 平均 25.7/30（147 章），shallow=0 | 通过；已剔除索引文件，口径统一 |
| 交叉引用 | 1,513 条 part 引用、0 断链 | 通过 |
| 完整 xref | 2,775 内部链接、752 外链、0 断链、0 孤儿/孤岛 | 通过 |
| 空白 | 修复后 0 缺陷（审计初 11 文件、12 个 W2 连续空行，已 `--apply` 清理） | 硬门禁已通过 |
| Mermaid | 修复后 511/511 通过（审计初 `ch92_chrono.md:147` 第 4 块无边，已补一条语义边） | 软失败已清零 |
| 表格 | 154 文件、0 问题 | 通过 |
| D5 附录 | 113/147，结构 `ERROR=0 / WARN=0` | 通过 |
| ASM 证据 | 485 块，67 已锚定准确、0 漂移、27 空、391 未锚定 | 已绑定证据健康，覆盖率有限 |
| ASM 新鲜度 | 154 个绑定小节，0 过期 | 通过 |
| §10 验证标记 | 147/147 章有标记 | 通过 |

一致性警告主要来自缺少工具可识别的立场标签；`verification_audit.py` 又报告 137/147 章存在真相标签，说明两个工具的识别规则并不一致。

### 5.2 编译与断言

- 全量主块报告：151 个 Markdown 对象、4,165 块、61 个失败块。
- 校正口径：151 包含 4 个非章节文件，真实结果是 147 章中 114 章无失败、33 章存在失败块。
- 61 个失败块全部被显式豁免覆盖，`compile_gate.py` 为 0 新回归，`exempt_audit` 为 `OK=61`。
- 豁免构成：`CROSS_BLOCK=21`、`MULTI_FILE=17`、`EXT_LIB=6`、`INTENTIONAL_ERROR=6`、`MODULE=6`、`MSVC=2`、`POSIX=2`、`GUARDED_COMPILE=1`。
- 主块编译只覆盖约 55% 的 C++ 围栏，其余片段依赖其他验证方式或尚未独立编译。
- 断言门禁检查 487 块：430 个可验证块通过、2 个预期教学失败、55 个 WARN、0 个真实声明失败。
- 修复后复跑 `cppbible.py check --stage compile`：`Compile All`、`Compile Gate`、`Exempt Audit`、`D5 Compile Gate`、`Assertions` 全部 PASS，5/5。
- 运行期/sanitizer 和 Clang 在 CI 中仍是软门禁，不能据此声称全量运行正确或跨编译器零风险。

### 5.3 Python 工具质量

- `tools/` 与 `Scripts/` 的 Python 文件均通过语法编译。
- 未跟踪的 `fix_ch36.py` 原本在第 16 行存在 `SyntaxError: invalid character '：'`（外层原始三引号字符串被内层 `r'''` 提前结束）；已改为外层 `"""` + 内层 `r'''`，`py_compile` 通过。该脚本未执行，不改变章节。
- `ruff` 和 `mypy` 未安装，因此没有当前静态类型/规范结果。
- 2026-08-13 的旧报告显示 86 个工具文件未发现高危 AST 模式，但该报告已落后于当前 102 个 `tools`/`tools/legacy` Python 文件。
- `audit_py_tools.py`、`audit_cpp_defects.py`、`chapter_number_audit.py` 原本在移入 `tools/legacy/` 后仍按旧目录层级计算仓库根，导致运行时写入不存在的 `tools/tools/`、扫描 0 文件却退出 0（静默假绿）。已修复：仓库根按 `__file__` 的实际位置（`legacy/` 上一级）推导，且扫描集合为空时以非零退出码失败。
- 修复验证：三个工具均通过语法编译；在任意 cwd 下均能正确定位仓库根并产出报告；在空仓库副本上运行均退出码 2（原为 0）。
- 修复后实测（仓库根）：`audit_py_tools.py` 扫描 59 个 `.py` 文件，无裸 except/eval/exec/通配导入，`broad_except_pass=5`、`rm_rf_or_git_clean=8`；`audit_cpp_defects.py` 扫描 7,540 个 cpp 块（593 个教学性错误示例已排除；口径为 `Book/**/ch*.md` 内全部 cpp/c++ 围栏，与 consistency 的 7,530 略有差异），给出 10 个不安全 C API、94 个裸 `new`、101 个 `reinterpret_cast`、7 个潜在缺 virtual 析构、2 个全局 `using namespace std`、749 个 `std::endl` 候选项——这些是启发式审阅线索，需人工复核，不自动判定为缺陷。
- 本轮还修复两个 Windows 中文控制台（GBK）编码缺陷：`xref_check.py` 打印 `⟶` 时抛 `UnicodeEncodeError`（已在入口 `reconfigure` 为 UTF-8）；`cppbible.py` 以 `text=True` 按 GBK 解码子进程 UTF-8 输出导致 runner 日志线程崩溃（已显式 `encoding="utf-8", errors="replace"`，并在 main 入口统一 UTF-8 输出）。两者在 Linux CI 无影响，但令 Windows 本机可复现跑通 unified quality。

### 5.4 文档完整性

优势：

- README、贡献指南、变更日志、发布说明、治理规范、交接文档、路线图和审计报告齐全。
- 147 章均有练习和验证状态标记；标准链接完整性较好。
- D5 与汇编证据已有机器门禁，且当前已绑定证据没有漂移。

问题：

- `README.md`、`AGENT.md`、`PROJECT_HANDBOOK.md`、`STATE.json`、`ISSUES.md`、`NEXT_LLM.md` 的阶段、HEAD、章节/代码块/豁免数量互相冲突。
- `STATE.json` 最后更新时间为 2026-07-17，明显落后于当前 HEAD；`ISSUES.md` 最后更新为 2026-07-09，列出的多项问题已被后续提交改变。
- `compile_all.py`、`density_audit.py` 曾把 `Book/` 下全部 Markdown 当章节，导致 151 而非 147；`consistency_check.py` 曾把 `assets/history/MANIFEST.md` 当章节。本轮三个工具均已统一过滤规则：只扫描 `chNN_*.md`（跳过 `SUMMARY/GLOSSARY/PREREQUISITES/INDEX/MANIFEST`），章节口径固定为 147。
- D5 覆盖在 `d5_gap_scanner.py` 中为 113，在 `metrics_snapshot.py` 中为 119，定义未统一。
- 55 处文本章号引用指向 13 个保留空号；前置元数据只有 41 章可检查，含 6 处拓扑倒置和 1 处悬空前置。
- `pyproject.toml` 声明 MIT，但仓库没有 `LICENSE` 文件；也没有 `SECURITY.md`、CODEOWNERS 或 Dependabot 配置。

## 6. Git 历史与协作风险

| 指标 | 结果 |
|---|---|
| 提交总数 | 493 |
| 历史跨度 | 47.2 天（2026-07-13 至 2026-08-29） |
| 月度提交 | 2026-07：305；2026-08：188 |
| 作者 | 1 人，493/493 |
| merge commit | 1 |
| tags | `v1.0.0` 至 `v1.3.0`，共 4 个 |
| 当前距 `v1.3.0` | 210 commits |
| 本地与远端 | 实时远端 `master=eb89ae9`；本地 `master` 在其上领先 7 commits，无分叉 |
| 提交签名 | 493 个均无签名状态 |

历史从 `v1.0.0` 发布提交开始，缺少更早的创作演进；提交频率高且几乎完全线性，适合个人高速迭代，但审阅、职责隔离、回滚粒度和人员替代性较弱。审计开始时 120 个章节及两个报告文件被修改，合计约 `+9,283/-873` 行；本轮修复又在工作树新增了 11 章空白清理、`ch92` 一处 Mermaid、`ci.yml`、3 个 legacy 工具和 `fix_ch36.py` 的改动（均未提交）。当前工作树仍较脏，继续叠加工作会显著增加审阅和恢复成本。

### 6.1 GitHub 在线核验

2026-08-30 通过公开 GitHub 页面/API 和 `git fetch` 做只读核验：

- 仓库为 public，默认分支 `master`；远端 HEAD 为 `eb89ae9`，且是本地 HEAD `a941c4a` 的祖先。
- `master` 未启用分支保护，required status checks 为 off。
- 共 373 次 Actions 运行；最近 15 次中 13 次成功，`#372`、`#373` 失败。
- 最新 `#373` 的 quality、GCC、Clang、site、PDF、publish-check 和 deploy 作业成功，EPUB 失败，工作流总体失败。
- `#373` 中 deploy 于 10:08:14Z 完成，而 GCC 编译到 10:38:33Z 才完成；说明部署确实没有等待编译，且在 EPUB 最终失败的工作流中仍发布了 Pages。
- 本轮已在工作树修改 `.github/workflows/ci.yml`：`site/pdf/epub` 等待 `compile + publish-check`，`deploy` 等待 `site + pdf + epub`。该修复尚未推送，需以新的 Actions 运行验收。

## 7. 风险清单

| 优先级 | 风险 | 影响 | 建议控制 |
|---|---|---|---|
| P0 | 备份与源同机同盘 | 单点故障可同时丢失源和备份 | 立即制作加密异盘/异机副本并恢复演练 |
| P0 | `site/pdf/epub` 原先只依赖 `quality`，不依赖 `compile` | C++ 编译或其他出版物失败时仍可能部署 | ✅ 工作树已修复依赖图（`site/pdf/epub` 等待 `compile+publish-check`，`deploy` 等待三产物）；推送后用 Actions 验收 |
| P0 | 大规模脏工作树且本地领先远端 7 提交 | 丢失、误合并和不可审阅风险 | 冻结新增工作，按主题拆分分支/提交/PR |
| P0 | 空白硬门禁失败 | 当前 CI quality 会阻断 | ✅ 已修复 11 文件 12 处 W2，quality 复跑 16/16 |
| P1 | 工具扫描范围错误与指标定义漂移 | 报告假绿或指标不可比较 | 建立唯一 `is_chapter()` 与指标 schema |
| P1 | 55 个悬空章号引用、7 个前置关系问题 | 学习路径误导 | 建立旧章号到现章号映射并转硬门禁 |
| P1 | 主块编译覆盖约 55%，55 个断言 WARN | 大量片段未获独立验证 | 给片段标注可执行类别并提高可验证率 |
| P1 | 3 个 legacy 审计工具已坏且有静默假绿 | 审计结论不可信 | ✅ 已修复根路径与零输入退出码；空输入退出码 2，任意 cwd 结果一致 |
| P1 | 依赖无锁文件，本机构建工具缺失 | 本地/CI 随时间漂移 | 锁 Python/Node 依赖，提供 bootstrap/self-check |
| P1 | 缺少 `LICENSE` 文件 | 分发和复用授权不明确 | 添加与声明一致的 MIT 正文 |
| P2 | 391 个 ASM 块未锚定，314 个 UNVERIFIED 标记 | 证据覆盖仍偏低 | 只对高风险结论逐步补可复现证据 |
| P2 | 跟踪二进制/输出和根目录一次性脚本较多 | 仓库噪声、职责不清 | 迁移到 fixtures/artifacts/archive 并写保留策略 |
| P2 | 单作者、几乎无合并审阅，`master` 无保护 | 知识集中、质量盲区且可绕过门禁直推 | 引入至少一名技术审阅者并启用分支保护/required checks |
| P2 | 无完整秘密/依赖漏洞扫描 | 供应链风险不可见 | CI 加 `gitleaks`、依赖审计和 SBOM |

## 8. 分阶段路线图

### 8.1 立即处置：2026-08-30 至 2026-09-02

| 优先级 | 任务 | 资源 | 预期成果/验收 |
|---|---|---|---|
| P0 | 将备份复制到加密外置盘或对象存储 | 维护者 0.5 人日；约 100 MiB 空间 | 第二故障域副本；哈希一致；空目录恢复后 `git fsck` 通过 |
| P0 | 冻结并拆分当前工作树 | 维护者 1 人日 | 120 章内容、报告更新、辅助脚本分开提交；无未知未跟踪文件 |
| P0 | 修复空白、Mermaid 和 `fix_ch36.py` | 内容维护者 0.5 人日 | ✅ 已完成：quality 16/16、Mermaid 511/511、`fix_ch36.py` 语法通过 |
| P0 | 修复 CI 依赖图（工作树已完成，待远端验收） | CI 工程师 0.5 人日 | ✅ 工作树已改 `needs`；推送后由新 Actions 运行验收 |
| P0 | 修正三个扫描器的章节筛选 | Python 工程师 1 人日 | ✅ 已完成并验证：`compile_all`/`density_audit`/`consistency_check` 统一按 `chNN_*.md` 过滤，章节数固定 147；quality 复跑 16/16 |

### 8.2 短期：2026-09-03 至 2026-09-13

| 优先级 | 任务 | 资源 | 预期成果/验收 |
|---|---|---|---|
| P1 | 清理 55 个悬空章号引用和 7 个前置问题 | 编辑 2 人日 + C++ 审阅 1 人日 | dangling=0、topology=0；旧编号映射有迁移记录 |
| P1 | 统一指标与事实源 | Python 工程师 2 人日 | README/STATE/ISSUES/NEXT_LLM 从同一 metrics schema 生成或校验 |
| P1 | 修复 legacy 工具并补最小测试 | Python 工程师 2 人日 | ✅ 根路径与零输入退出码已修复；建议将 3 个工具并入 `tools/` 顶层并有 fixtures |
| P1 | 建立可复现开发环境 | CI 工程师 2 人日 | 锁文件、bootstrap 命令、`ruff`/`mypy`/MkDocs 可复现安装 |
| P1 | 补齐治理文件 | 维护者 0.5 人日 | MIT `LICENSE`、`SECURITY.md`、CODEOWNERS 落库 |

阶段出口：工作树可审阅、主门禁全绿、统计口径一致、发布不会绕过编译、仓库可在第二台机器按文档恢复和构建。

### 8.3 中期：2026-09-14 至 2026-10-31

| 优先级 | 任务 | 资源 | 预期成果/验收 |
|---|---|---|---|
| P1 | 建立工具链单元/集成测试 | Python 工程师 2 至 3 周 | 核心解析器有 fixtures；覆盖错误范围、围栏、链接、豁免和退出码 |
| P1 | 提高 C++ 片段验证率 | C++ 工程师 2 周 | 可独立验证覆盖率从约 55% 提升到至少 80%；WARN 有明确原因码 |
| P1 | 收敛 61 个豁免 | C++ 工程师 1 周 | 每项有 owner、原因、平台和复核日期；可修项转为真实工程/fixture |
| P1 | 将成熟软门禁转硬 | CI 工程师 1 周 | Mermaid、章号、拓扑无基线债务后转硬；Clang 失败可追踪 |
| P2 | 仓库卫生治理 | 维护者 2 人日 | 清理无用途空目录；二进制/输出仅保留可解释 fixture；根脚本归档 |
| P2 | 发布复现性 | CI 工程师 1 周 | 容器 digest、依赖版本、构建 manifest、产物 checksum 和保留策略齐备 |

阶段出口：所有门禁有测试、指标不会静默假绿、跨平台构建可重现，内容变更可以通过小批次 PR 审阅。

### 8.4 长期：2026-11-01 至 2027-02-28

| 优先级 | 任务 | 资源 | 预期成果/验收 |
|---|---|---|---|
| P2 | 高风险内容证据化 | 2 名 C++ 领域审阅者，各 1 至 2 周/月 | 并发、内存模型、UB、ABI、性能结论优先；关键 ASM/运行结果均有锚点 |
| P2 | 运行期与跨编译器门禁升级 | C++/CI 工程师 2 至 3 周 | sanitizer、运行断言、Clang 从观察转为分级硬门禁 |
| P2 | 3-2-1 备份制度 | 运维 0.5 人日/月 | 3 份、2 种介质、1 份异地；每季度随机恢复并留证 |
| P2 | 发布与供应链治理 | CI 工程师 1 至 2 周 | 依赖审计、秘密扫描、SBOM、签名 tag/产物、可追溯 release |
| P3 | 降低单人知识集中 | 维护者 + 技术编辑 | 至少双人评审关键变更；维护手册以可执行检查代替手工状态 |

长期目标不是机械地让所有示例“独立编译”，而是让每个代码块都有明确类别：可独立运行、同章组合、多文件工程、平台专用或故意失败，并由对应门禁验证其真实承诺。

## 9. 推荐实施路径

1. 建立 `audit/fix-gates` 分支，只处理门禁自身：章节筛选、零输入失败、CI `needs`、空白和 Mermaid。
2. 建立 `audit/fix-references` 分支，按“旧编号 -> 现章节”映射批量修复，再人工抽查语义，不直接按数字猜测。
3. 建立 `audit/reproducible-toolchain` 分支，加入锁文件、bootstrap 和工具版本自检；Windows 与 Linux 输出同一 schema。
4. 把当前 120 章内容改动按 part 或主题拆成小批次，每批跑 quality、compile、exempt audit 和 assertions。
5. 所有报告记录 `commit`、工作树是否干净、工具版本、扫描集合和 schema 版本；没有这些字段的历史快照仅作参考。
6. 每个阶段先清零既有债务，再把对应软门禁转硬，禁止用扩大豁免清单换取绿色状态。

## 10. 验收指标

| 指标 | 当前 | 短期目标 | 中长期目标 |
|---|---:|---:|---:|
| 第二故障域备份 | 0 | 1 份并恢复验证 | 3-2-1 + 季度演练 |
| quality 主门禁 | ✅ 16/16（审计初 15/16） | 16/16 | 持续 16/16 |
| 一致性 WARN | ✅ 0（30 处为徽章载体误报，已修工具） | 0 | 0 |
| 悬空章号 / 前置问题 | ✅ 0 / 0（55 引用映射清零 + 7 前置清零，门禁已转硬） | 0 / 0 | 0 / 0 |
| Mermaid 静态错误 | ✅ 0（审计初 1，已修） | 0 | 0 |
| 编译报告章节口径 | ✅ 147（已修正，审计初 151） | 147 | 147 |
| C++ 可独立验证覆盖 | 约 55% | 不下降 | 至少 80%，长期按分类逼近 95% |
| 断言不可验证 WARN | 55 | 全部分类 | 降至 15 以下或逐项有合理豁免 |
| Python lint/type | 未运行 | 环境可运行 | CI 强制 |
| 文档事实源冲突 | 多处 | 0 | 自动防回归 |
| 发布对编译依赖 | ✅ 工作树已强制；待推送验收 | 强制依赖 | 持续强制 |

## 11. 审计边界

- 审计期遵循“不改用户现有工作”原则；审计后按立即处置项对工作树应用了最小修复：空白 11 章、`ch92` Mermaid 单块、`ci.yml` 依赖图、3 个 legacy 工具、`fix_ch36.py` 语法。除上述外未修改其他章节内容、未推送远端。
- 因本机缺少 Pandoc、XeLaTeX、MkDocs、ruff、mypy 和 CMake，本轮没有在本机重建 PDF/EPUB/站点，也没有完成 Python lint/type check。
- 已联网只读查询 GitHub Actions、远端 HEAD 和分支保护状态；未推送、未触发工作流、未改变 GitHub 远端 refs。
- 秘密检查采用常见令牌/私钥特征扫描，不替代 `gitleaks` 全规则审计。
- 编译结论基于 GCC 15.3.0 当前工作树报告；Clang、Linux sanitizer 和第三方依赖示例仍需 CI 或容器复核。
