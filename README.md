# 现代 C++ 终极圣经 (The Ultimate Modern C++ Bible)

[![CI](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml)

> **147 章 · 16 part · 约 25.6 万行 · 7515 个 cpp 代码块**（数字派生自 `build/metrics.json`，由 `tools/gen_metrics.py --check` 门禁守护）
> 密度审计 v3 均分 **25.7/30**，浅章（<15 分）**0** 个

一本面向**系统 / 嵌入式 / 高性能**方向的现代 C++ 硬核教程（C++11 → C++26），
同时是一套**可执行知识的验证基础设施**：正文、知识卡、证据、攻击记录与判决共用同一个信任根，
**每个数字都能被独立复算，每条结论都能被攻击**。

```
                     ┌──────────────────────── 可复核的信任根 ────────────────────────┐
  Book/ 147 章  ──►  atoms/ 知识卡 ──► evidence/ 证据卡 ──► tools/ 门禁与判决 ──► web/ 静态站
  (可编译的示例)      (37 张实卡 +           (47 卡，            (67 规则 / 9 保护器 /    (星图 / 现场验哈希 /
                      10 张 draft)            L1-L5 获取级)       34 条哈希面)            复现清单)
                     └──────────▲──────────────▲───────────────▲──────────────▲───────────┘
                                │              │               │              │
                        data/supply_chain/  data/authority/  透明日志     独立验证器 + VSA 凭证
                        (Merkle 目录根)     (452 条判决账本)  (哈希链)     (零 import 本项目)
```

## 它是什么 / 不是什么

| 是 | 不是 |
|---|---|
| 一本 147 章的现代 C++ 教程，**每个 ```cpp 块都要能独立编译** | 不是速查手册 / 面试八股合集 |
| 一套**知识验证基础设施**：知识卡 + 证据卡 + 攻击 + 四态判决 + 保护器 | 不是"AI 自动写书"的项目（判决与签名永远留给人） |
| 一份**可独立复算**的账本：工具/规则/配置全部进哈希面，现场可验 | 不承诺"绝对正确"：unknown / 未达成的目标一律显式登记 |

## 现状指标（本机实测，非目标值）

| 维度 | 现状 | 取证入口 |
|---|---|---|
| 教程正文 | **147 章**，16 part，255,897 行，7,515 个 cpp 块 | `python tools/gen_metrics.py` |
| 知识卡 | **37** 张实卡（`verified 23 / red-team-verified 3 / draft 11`）+ 10 张 `draft650` 草稿 | `atoms/**/ATOM-*.md` |
| 判决规则 | **67** 条（其中 `severity=block` 44 条），规范清单见 `data/_gate_rules.json`（= `gate_engine.RULES`；661 A2 裁定） | `len(gate_engine.RULES)` / `len(_gate_rules.json)` |
| 保护器 | **9** 个（冲突检测 / anti-windup / 盲化 / 校准追踪 / MDL 准入 / 工具级门 / shadow / 熔断 / 预算） | `queyi-core/tools/*_64*.py` |
| 逃逸率 | **1 / 1406 = 0.0711%**（v7 变异基线；统计上界 0.9062%，已用 e-process 复算） | `data/616_baseline.md` |
| 盲化 holdout 检出 | **34 / 41 = 82.9%**（W3 扩样后可测口径；unknown 1 不进分母） | `data/holdout_reveal_5_672h.json` |
| 外部 corpus 检出 | **40 / 64 = 62.5%**（W3 扩样后；unknown 9 不进分母） | `data/external_corpus_reveal_672h.json` |
| 接地模型 | W2 加权论辩求解：**131 节点**（IN 89 / OUT 42 / UNDEC 0） | `data/grounded_labels_w2.json` |
| 前端星图 | 178 节点 / 1,093 边（攻击 388、击败 194）/ 全部由真实台账生成 | `web/data/graph.json` |

## 质量门禁

本项目用一套"本地 + CI 双跑"的自动化校验，保证**不注水、不破链、可编译**：

| 门禁 | 命令 | 当前结果 |
|------|------|----------|
| 一致性检查 | `python tools/consistency_check.py` | ERROR=0 / WARN=0 |
| 全量编译 | `python tools/compile_all.py --main-only` | 147 章，115 章自包含通过 |
| 编译门禁 | `python tools/compile_gate.py` | 0 真实语法/类型回归（58 设计性豁免块） |
| `//@` 输出断言 | `python tools/run_expected.py --all --check` | 65 块全 PASS（关键块运行期输出与注释逐字比对） |
| 覆盖状态机 | `python tools/l2_state.py check` | 57 章 / 139 块纯注释全为审计保留 C 类，无漂移 |
| 编译回归 triage | `python tools/compile_triage.py --check` | 预存坏块 vs 新增回归自动分账，NEW=0 |
| 密度审计 v3 | `python tools/density_audit.py --json` | 均分 25.7/30，浅章 0 |
| 交叉引用 | `python tools/crossref_audit.py` | 0 断链 |
| D5 性能附录 | `python tools/d5_gap_scanner.py` | 127/147 章（86%，口径已统一），结构 ERROR=0 / WARN=3（措辞建议，不阻断） |
| 信任根哈希面 | `python tools/tool_integrity.py --check` | 34 条（工具 27 + 测试配置 2 + 供应链台账 5），缺失即 FAIL |
| 许可证头 | `python tools/license_header_check_655.py` | 活跃源码全过（新增 `.py` 强制 SPDX 头） |
| 本地 pre-push | `python tools/prepush_check.py` | push 前一键复跑上述快校验 + 仓库卫生（`--install-hook` 可装钩子） |
| 结构审计 | `python tools/structure_audit.py --check` | 标题大纲缺陷（stray H1 / 跳级）+ 参差表格：0 命中 |
| 星级格 / H2 | `python tools/star_h2_audit.py check --star` | 示例头星级格 100% 统一（span 5 格制）+ H2 基线防恶化 |

**批次回归用快速门禁（672h 起，默认）**：

```bash
python tools/fast_gate.py --tests tests/test_<本批>.py   # 658+669d+671a guard+本批测试，<5 分钟
python tools/fast_gate.py --all                          # 门禁 + 全部非 slow 测试（xdist 并行）
python tools/fast_gate.py --all --skip-frontend          # 只动后端时
```

慢档（`@pytest.mark.slow`：WSL 编译 / 全量变异 / 全量重跑，单测 >10s）本地默认跳过，
**全量回归只在 CI 跑**（CI 为 `-m "not slow" -n 16` + `-m slow -n0` 两阶段）。

> **豁免说明**：`tools/compile_exempt.json` 中的 58 个失败块均为**设计性不可单编**内容
> （多文件示例、C++20 Modules、POSIX / Windows 专用 API、外部库、故意展示的错误 / UB、
> 跨块依赖），**非**内容 bug。真实语法 / 类型错误一旦出现，CI 编译门禁立即变红。
> 豁免并非"挂起即忘"：`python tools/exempt_audit.py` 会用与基线相同的命令逐块重编，
> 任何一条豁免失效（STALE）或正文漂移（DRIFT）都会显形（673b 复核：58/58 仍有效）。

**汇编证据口径（如实披露）**：全书 513 个 ```` ```asm ```` 展示块中，**203 个已锚定**
真实机器产物（与 `Examples/*.asm` 逐一符号比对，DRIFT=0，由 `verify_asm_evidence.py`
门禁守护）；其余 310 个为**教学示意 / 节选**（含 27 个空占位块），不承担"真实产物"
承诺，演进目标见 metrics 看板的 `asm_anchor_rate`。各章"本章所有汇编均为真实产物"
的全称声明均经机校——所在章的全部 asm 块均已锚定，**0 矛盾**。

## 评测数据集与数据质量（676m）

论文的评测集是 `data/holdout_expansion/`（**1042 条扩样标注** + 1094 个 C++ 源文件），
加上历史层 holdout 41 / corpus 64。**字段规范见 [`data/holdout_expansion/SCHEMA.md`](data/holdout_expansion/SCHEMA.md)，
数据卡见 [`data/holdout_expansion/DATASHEET.md`](data/holdout_expansion/DATASHEET.md)。**

| 指标 | 值 | 出处 |
|------|----|------|
| 扩样样本 | **1042**（expA–expG 七批） | `data/holdout_expansion/*/INDEX.json` |
| `defect_type` 词表 | **34 项规范词表**（在用 33 项；676m 前是 56 个取值） | `tools/fix_676m_schema.py` |
| `planted=true` 占比 | **92.9%**（968/1042） | 同上 |
| 跨批**字节级**重复 | **0** | `data/676k_dedup_results.json` |
| 跨批**结构近克隆** | **103 对**（4 个批对） | 同上 |
| 批内**模板克隆率** | **62.2%**（674/1083）⇒ 全库仅 **572** 种结构 | 同上 |
| 盲化双标注 Cohen's κ | **0.77**（`defect_type`）/ **0.69**（`expected_verdict`）/ **0.71**（`planted`）——**AI 自洽性，非人类 IAA** | `data/676k_relabel_score.json` |
| 编译抽检 | **217/217 = 100%** | `data/676k_compile_results.json` |
| 真实来源可追溯 | **74/74**（全部 HTTP 200） | `data/676k_source_results.json` |
| 检测器盲区 | **38.4%**（1147 样本 × 8 资产） | `data/blindspot_676g_stats.json` |

**检测器深度 Benchmark（676l）摘要**：单检测器 recall **asan 58.5% > ubsan 38.2% > tsan 36.1%
> compiler-warn 19.1% > cross-compile 15.1% > linker 1.3%**（`wunsequenced` / `compile-time`
恒 `unknown`）；8 资产**并集 94.21%**；k=1…8 穷举最佳 k=4 = **92.58%**，拐点 **k=5**；
FD 在 k=4 选到 **86.94%**（比穷举最佳低 5.64pp，对 2000 次随机抽样的百分位 96.6）；
`linker` 的 10 个 catch **全部**落在 asan/ubsan/tsan 的 10 个 `unknown` 里（**低边际但不可替代**）。
详见 `data/676l_检测器Benchmark总报告.md`。

**复现命令**：

```bash
# 数据修复自检（幂等门禁：H1 残留 0、待迁移 0）
.venv/Scripts/python.exe tools/fix_676m_schema.py --verify

# A5 重算门禁（修正标签后主端点须与 676f 逐位一致）
.venv/Scripts/python.exe tools/recompute_a5_676m.py --check

# 一键全链路（含上述两步 + 676k 只读审计 + 论文编译）
bash docker/paper/run_all.sh
```

> **两个必须同读的限定**：① 92.9% 的样本是人工植入，本数据集测的是**仪器**而非真实缺陷分布；
> ② 62.2% 的批内模板克隆率意味着**有效独立样本量远小于 1042**，且**不可用于训练模型**。

## 快速开始

```bash
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible
python -m pip install -r requirements.lock.txt

# 1) 一句话自检：指标、门禁、信任根
python tools/gen_metrics.py --check          # 文档数字与事实源一致
python tools/consistency_check.py            # 全文一致性
python tools/tool_integrity.py --check       # 信任根哈希面（缺失即 FAIL）
python tools/license_header_check_655.py     # 许可证头

# 2) 跑测试 —— 批次回归默认走快速门禁（门禁三件套 + 本批测试，<5 分钟）
python tools/fast_gate.py --tests tests/test_<本批>.py    # 或 --all 跑全部非 slow 测试
python tools/fast_gate.py --all --skip-frontend           # 只动后端时
node web/run_tests.mjs                                    # 前端自测（~14s，23 个测试文件）

# 全量两阶段（CI 同口径；本地全量很慢，一般不跑）
python -m pytest -m "not slow" -n auto
python -m pytest -m slow -n0

# 3) 打开前端静态站（无后端、无构建；数据由真实台账生成）
python -m http.server 8099 --directory web   # 然后访问 http://127.0.0.1:8099/
```

贡献流程、测试分类约定与 PR 检查清单见 [`CONTRIBUTING.md`](CONTRIBUTING.md)；
贡献者原创声明（DCO）见 [`DCO.md`](DCO.md)；行为准则见 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)。

## 目录结构

| 路径 | 内容 |
|------|------|
| `Book/` | 147 章正文（16 part，编号连续；`.md` 里引用的外部根在 `docs/`、`Appendix/`） |
| `Examples/` `Benchmarks/` `Appendix/` | 真实可编译示例、汇编产物（`.asm`）、UB 反例库 |
| `atoms/` `evidence/` | 知识卡（原子命题）与证据卡（L1 实测 / L2 标准 / L3 文档 …） |
| `tools/` | 门禁、判决、证据、保护器、发布脚本（556 个 `.py`，均带 `--check` 自检） |
| `tests/` | pytest 套件（两阶段 fast / slow，~4000 例） |
| `data/` | 所有**产物**与账本：判决账本、基线报告、变异库、供应链台账、验收报告 |
| `docs/` | 规范文档（内核、判决 schema、双轴词表、接口规范）与站点素材 |
| `web/` | 静态站（`index.html` 总览 / `starmap.html` 星图 / `verify.html` 现场验哈希） |
| `status/` `_auto/` | 逐批验收报告与自动化协议（inbox 任务书 / outbox 收工报告） |

## 本地构建（EPUB / PDF / 站点）

> 构建依赖 `pandoc` + `texlive-xetex`（PDF），建议在本机 WSL 或 CI 中执行；本地 Windows
> 缺依赖时脚本会明确报错并给出安装指引，**不产出半成品**。

```bash
bash tools/generate_epub.sh            # EPUB3
bash tools/generate_pdf.sh             # PDF（单卷全书）
bash tools/generate_pdf.sh --by-part   # PDF（分卷）
```

## 路线图

1. **第一年四件地基**（`_arch_v34` 战略结论）
   - ✅ 许可与协作包（本文件 + `LICENSE` + `DCO.md` + `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` + `.github/` 模板）
   - ✅ 判决形式规格 v1（[`docs/verdict_formal_spec_v1.md`](docs/verdict_formal_spec_v1.md)）——为后续 Rust + Verus 形式化做准备
   - ✅ 元验证论文（NeurIPS 2027 Datasets & Benchmarks 投稿稿 v1.1）：`research/latex/queyi_neurips2027_v1.1.tex`（正文 9 页 / 全稿 30 页）；同批交付可复现化改造——一键复算 `bash docker/paper/run_all.sh`、手册 [`REPRODUCE.md`](REPRODUCE.md)、数字审计 `tools/verify_paper_numbers.py`（118 条检察 / 0 硬伤）、种子审计 `tools/seed_audit_676h.py`（实验类未固定种子 0）
   - ✅ 数据修复 + 实验重算（676m）：34 条挂起样本判据修正、56→34 项统一词表、字段完整性（M1–M5）全过；A5 主端点**逐位不变**（标签修正对主分析零影响），数据质量与检测器 Benchmark 已写入论文附录
   - ✅ 门禁三杠杆（增量选例 / 结果缓存 / 分片）：`tools/test_selector_655.py`、`tools/result_cache_655.py`
2. **信任根继续独立化**：外部锚（OpenTimestamps 上链）、第三方盲评、独立性从 L2 走向 L3
3. **知识面扩展**：`draft650` 草稿卡 → 补证据升 `verified`；C 语言与嵌入式域适配
4. **内容侧**：汇编锚定率提升、D5 性能附录补到全覆盖、`Interview/` 与 `misconceptions/` 同步更新

## 约定与治理

- 红线宪法见 [`AGENT.md`](AGENT.md)：准确性＞速度、完整性＞简洁、禁注水、禁增章、禁幻觉、源只读只写 `build/`。
- 写作 / 工程约定见 [`CONVENTIONS.md`](CONVENTIONS.md)、[`GOVERNANCE.md`](GOVERNANCE.md)；
  接手者请先读 [`NEXT_LLM.md`](NEXT_LLM.md)（30 秒速览当前阶段）。
- 安全与漏洞报告见 [`SECURITY.md`](SECURITY.md)；发布与质量快照见 [`RELEASE.md`](RELEASE.md)。

## 许可

[Apache-2.0](LICENSE) —— 内容与示例代码均以 Apache-2.0 许可发布。
贡献即表示同意以同一许可证分发，并在 commit 上签署 [`DCO.md`](DCO.md)。

## 逃逸率口径（重要，勿误读）

前端"逃逸率 0.0711%（1/1406）"是**对自造变异分布（v7）的漏检率**，**不是本书的真实错误率**。

- Clopper-Pearson 95% 单侧上界 = **0.337%**，且仅对该变异分布成立；
- `mutation score`（core 96.5% = 110/114，95% CI 91.3–99.0；all 81.8% = 130/159，95% CI 74.9–87.4）衡量的是**测试充分度（Test adequacy）**，
  **不等于外部效度**——详见 [`docs/metric_layers_658.md`](docs/metric_layers_658.md)；
- 真实世界错误检测能力由盲化 holdout（[`data/holdout/`](data/holdout/)）与外部 corpus
  （[`data/external_corpus_658.md`](data/external_corpus_658.md)）另行评估。
