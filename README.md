# Queyi (阙疑) · C++ 缺陷检测器组合演化 —— 研究仓库 + 现代 C++ 圣经

[![CI](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml)
[![DCO](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/dco.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/dco.yml)
[![Docker Reproduce](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/docker.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/docker.yml)
[![Pages](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/pages.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/pages.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Citation](https://img.shields.io/badge/Citation-CITATION.cff-green)](CITATION.cff)

> 本仓库装**两样东西**：
> ① **Queyi（阙疑）** —— "失败驱动演化检测器组合"的 C++ 缺陷检测研究线与可复现基准；
> ② **《现代 C++ 终极圣经》** —— 147 章硬核教程与其知识验证基础设施。
>
> 研究线入口就是本文件 §1–§6；书籍线见 [§7](#7-书籍线现代-c-终极圣经)。

---

## 1. 一句话

**Queyi 把"用哪些检测器"本身当作可以在失败中演化的对象**：四态判决
（`pass / fail / unknown / contradict`）+ append-only 判决账本 + Merkle 完整性 +
确定性组合算子 **E**（failure / novelty / cost / redundancy 四分量）。
它不发明新的缺陷检测算法，它回答的是**"给定一堆检测器，怎么选、怎么证明选得对、
怎么证明结论不依赖测量环境"**。

---

## 2. 五个核心发现（都带数字与取证入口）

| # | 发现 | 数字 | 取证 |
|---:|---|---|---|
| 1 | **八资产并集远大于任一单检测器**：单检测器 recall 最高的 asan 也只有 **61.65%**，而八资产并集达 **99.22%**（分母 expected=catch 640，当前冻结标签） | asan 61.65% > ubsan 40.25% > tsan 38.03% > compiler-warn 20.16% > cross-compile 16.48% > linker **1.41%** | `data/693_defect_type_deep_analysis.json::stale_metric_crosscheck_vs_676l` |
| 2 | **但 38.4% 的缺陷仍是全资产盲区**：1147 样本 × 8 资产冻结矩阵，OR 口径检出 **61.6%**、盲区 **38.4%** | 707/1147 catch，440/1147 blind | `data/681_type_stats_normalized.json` |
| 3 | **盲区高度不均匀**：34 类缺陷里 **13 类盲区率 >50%**，最差的 `algorithm_misuse` 达 **77.1%**（27/35） | 13/34 类 >50% | `data/681_type_stats_normalized.json` |
| 4 | **环境是测量的坐标，不是复现细节**：同一批样本在 WSL/g++13.3（6 资产）下 catch **60.07%**，Windows-native（3 资产）下 **24.74%**；unaware 协议会把"没测"和"测了没中"写成同一种记录 | 配对 McNemar (b,c)=(200,0)，p=1.24×10⁻⁶⁰；E1 的捕获有 **58.82%**（200/340）在 E2 **从未被测量** | `data/692_environment_report.md` |
| 5 | **组合算子的选择效应显著，但必须并报并列分析**：主分析（8 候选、k=4）FD **54.59%** vs Random **30.57%**，Δ=**+24.03pp**，95% CI [+20.51, +27.55]，精确 McNemar **p=2.3×10⁻⁴¹**（n=566） | ⚠ **并列分析 Δ=+0.00pp**；本项目**不宣称**"FD 选择策略优于 Random" | `data/676f_A5重跑报告.md` |

> **发现 5 的限定必须一起读**：主分析的 +24.03pp 与并列分析的 +0.00pp 是**同一个实验的两种口径**，
> 只报前者是选择性报告。完整口径见 `data/676f_A5重跑报告.md` §并列分析。

> ⚠ **发现 1 的数值与 `data/676l_单检测器性能报告.md` 不一致，这是刻意的。**
> 676l 的报告在 **676m 标签修复之前**生成（其 ground truth 为 catch 674 / miss 473），
> 之后**从未重算**；当前冻结矩阵是 catch 640 / miss 507。TP/FP/TN 逐位不变，
> 只有 FN 与分母变了 ⇒ 676l 的 recall 列系统性偏低 1–3pp。
> 上表是**用当前冻结标签重算**的值。详见 `data/693_paper_revision_suggestions.md` §1。

**真实世界侧**：683 批次新增 **110 条真实缺陷重构靶场**，每条可追溯（CVE / issue / commit），
**109/109** 经 NVD 在线验证 FOUND，应答原文已冻结。

---

## 3. 三步跑通

```bash
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible

# ① 环境体检（明确告诉你哪些资产在本机不可用，不静默降级）
bash Scripts/verify_environment.sh --report

# ② 纯 Python 数据链（不需要任何编译器）—— 论文数字对账 + 完整性
python tools/verify_paper_numbers.py         # 数字 vs 权威源，fail-closed
python tools/gen_693_manifest.py --check     # 14 项冻结产物 sha256 完整性

# ③ 一键复现（环境体检 → 完整性 → 数字复算 → 门禁 → 报告）
bash Scripts/reproduce_all.sh --out out/693_reproduce
```

完整检测链（需要 WSL g++ 13.3 + MinGW g++ 13.1 + clang++）：

```bash
python tools/collect_realworld_683.py --stage verify        # NVD 在线验证（需网络）
python data/realworld_683_runner.py --stage detect          # 110 × 8 真实检测（增量 checkpoint）
python data/realworld_683_runner.py --stage merge
```

容器复现（**需要本机装 Docker**；693 执行环境未装，镜像**未实测构建**）：

```bash
docker compose -f docker/reproduce/docker-compose.yml build
docker compose -f docker/reproduce/docker-compose.yml run --rm verify-env
docker compose -f docker/reproduce/docker-compose.yml run --rm reproduce
```

> ⚠ **WSL 用户必读**：开启 Windows 系统代理时，`wsl.exe` 会向 stderr 写一条 UTF-16LE 横幅，
> 导致 Python 解码失败 ⇒ ASan/UBSan 报告**全部静默丢失**（系统性假 miss）。
> 调用前必须 `export WSL_UTF8=1` 且 `export WSLENV=WSL_UTF8/u`。详见 `docs/ENVIRONMENT.md` §2。

---

## 4. 项目结构

| 路径 | 内容 |
|---|---|
| `research/latex/` | 论文主稿 `queyi_neurips2027_v1.1.tex`（tectonic 编译） |
| `data/` | 全部**产物**与账本：1147×8 冻结矩阵、真实靶场、判决账本、逐批验收报告 |
| `data/holdout_expansion/` | 评测集（1042 条扩样 + 1094 个源文件），规范见 `SCHEMA.md`、数据卡见 `DATASHEET.md` |
| `data/annotation_package/` | **人类标注材料包**（145 条去标识化样本 + 标注指南 + 校准题） |
| `tools/` | 门禁、判决、分析、复现脚本（均带 `--check` 自检） |
| `Scripts/` | `reproduce_all.sh` / `verify_environment.sh`（693-B 一键复现） |
| `docker/reproduce/` | 复现镜像（多阶段构建；**未实测**） |
| `docs/` | `ENVIRONMENT.md`（环境锁定）与研究报告 |
| `tests/` | pytest 套件（fast / slow 两阶段） |
| `Book/` `Examples/` `atoms/` `evidence/` `web/` | **书籍线**（见 §7） |

---

## 5. 数据一览

| 数据 | 规模 | 位置 |
|---|---|---|
| 合成语料判定矩阵 | **1147 × 8**（真实编译/运行，-O0/-O2 双档） | `data/blindspot_676g_detection_matrix.json` |
| 真实靶场 PoC + 元数据 | **110 条**（可追溯，PoC 单文件 <200 行） | `data/real_world/RW-*.cpp` |
| 真实靶场判定矩阵 | **110 × 8** | `data/683_real_world_detection_matrix.json` |
| CVE 在线验证 | **109/109 FOUND**（NVD 应答原文冻结） | `data/683_real_world_candidates_verified.json` |
| `defect_type` 词表 | **34 项闭集** | `data/676m_sample_manifest_corrected.json` |
| 权威判决账本 | **452 条事件** | `data/authority/decision_event_v2_ledger.jsonl` |
| 机器可读元数据 | Croissant core 1.0 + RAI 1.0（官方校验通过） | `data/croissant.json`、`data/rai_metadata.json` |

---

## 6. 引用

```bibtex
@misc{liao2027queyi,
  title        = {Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection},
  author       = {Liao, Ran},
  year         = {2027},
  note         = {Manuscript in preparation (NeurIPS 2027 Datasets \& Benchmarks track)},
  howpublished = {\url{https://github.com/LiaoRanran/CPP-Bible}},
  license      = {Apache-2.0}
}
```

机器可读引用：[`CITATION.cff`](CITATION.cff)。

---

## 7. 书籍线（现代 C++ 终极圣经）

> **147 章 · 16 part · 约 25.6 万行 · 7,515 个 cpp 代码块**
> （数字派生自 `build/metrics.json`，由 `tools/gen_metrics.py --check` 门禁守护）
> 密度审计 v3 均分 **25.7/30**，浅章（<15 分）**0** 个

面向**系统 / 嵌入式 / 高性能**方向的现代 C++ 硬核教程（C++11 → C++26），
同时是一套**可执行知识的验证基础设施**：正文、知识卡、证据、攻击记录与判决共用同一个信任根，
**每个数字都能被独立复算，每条结论都能被攻击**。

```
  Book/ 147 章 ──► atoms/ 知识卡 ──► evidence/ 证据卡 ──► tools/ 门禁与判决 ──► web/ 静态站
  (可编译的示例)    (37 实卡 + 10 draft)  (47 卡，L1-L5)   (67 规则 / 9 保护器)  (星图 / 验哈希)
                        ▲                    ▲                   ▲
              data/supply_chain/     data/authority/       透明日志哈希链
              (Merkle 目录根)        (452 条判决账本)
```

| 门禁 | 命令 | 当前结果 |
|---|---|---|
| 一致性检查 | `python tools/consistency_check.py` | ERROR=0 / WARN=0 |
| 编译门禁 | `python tools/compile_gate.py` | 0 真实语法/类型回归（58 设计性豁免块） |
| `//@` 输出断言 | `python tools/run_expected.py --all --check` | 65 块全 PASS |
| 信任根哈希面 | `python tools/tool_integrity.py --check` | 34 条，缺失即 FAIL |
| 批次快速门禁 | `python tools/fast_gate.py --tests tests/test_<本批>.py` | <5 分钟 |

打开静态站：`python -m http.server 8099 --directory web` → http://127.0.0.1:8099/

> **逃逸率口径（勿误读）**：前端"逃逸率 0.0711%（1/1406）"是**对自造变异分布（v7）的漏检率**，
> **不是本书的真实错误率**；Clopper-Pearson 95% 单侧上界 0.337%，且仅对该变异分布成立。
> 详见 `docs/metric_layers_658.md`。

书籍线的路线图与约定另见 [`ROADMAP_v3.md`](ROADMAP_v3.md)、[`CONVENTIONS.md`](CONVENTIONS.md)、
[`AGENT.md`](AGENT.md)（红线宪法）、[`NEXT_LLM.md`](NEXT_LLM.md)（接手速览）。

---

## 8. 贡献与治理

- 贡献流程与 PR 清单：[`CONTRIBUTING.md`](CONTRIBUTING.md)
- 行为准则：[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- 原创声明 DCO（**提交必须用 `git commit -s`**）：[`DCO.md`](DCO.md)
- 安全策略：[`SECURITY.md`](SECURITY.md)（不接收武器化利用链；靶场样本只收"缺陷最小重构"）
- 环境问题排查：[`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md)

**我们正在招募标注者**：31 条 C++ 裁决题，1–2 小时，可署名致谢。
见 [`data/693_github_recruitment_issue.md`](data/693_github_recruitment_issue.md)。

---

## 9. 诚实边界（必读，不要跳过）

1. **人类 IAA 仍为 0。** 所有标签都有交叉验证，但交叉验证的一方是 **AI**。
   693 批次已备齐人类裁决材料包（AI 双标 raw agreement **78.6%** / κ=**0.495**，31 条分歧清单），
   但**真人还没标**。κ=0.77 那类数字是 **AI 自洽性，不是人类一致性**。
   另外自曝一个材料包缺陷：**145 条里有 13 条**源码注释残留 `expected_verdict` 原文
   （689 净化脚本漏了），裁决表已标 `leak_suspected=yes`，κ 带/不带各报一次
   （77.3% / κ=0.458）。
2. **样本主体是合成/半合成**：92.9% 为人工植入；真实靶场以**重构**方式引入，
   不等价于原始项目上下文。测的是**仪器**，不是真实缺陷分布。
3. **批内模板克隆率 62.2%**（674/1083）⇒ 有效独立样本量远小于 1042，且**不可用于训练模型**。
4. **A5 的 +24.03pp 必须与并列分析 +0.00pp 并报**；不宣称 FD 优于 Random。
5. **Docker 复现镜像未实测构建**（693 执行环境未安装 Docker）。
6. **复现硬依赖 WSL**：论文数字必须在 `REPRODUCE.md` 声明的环境
   （Ubuntu 24.04.4 + g++ 13.3）内执行；错误环境下脚本 fail-loud 抛错，不再静默降分。
7. **未被证据支持的项一律保留 `⬜ 未闭合`**，绝不写成"安全/已确认"。

---

## 10. 许可证

[Apache-2.0](LICENSE) —— 内容与示例代码均以 Apache-2.0 许可发布。
贡献即表示同意以同一许可证分发，并在 commit 上签署 [`DCO.md`](DCO.md)。
平台侧版权（含 C++ 提案译文）归各版权方所有，本仓库仅作引用与评注。
