# Queyi (阙疑) — Failure-Driven Verifier Evolution for C++ Defect Detection

[![CI](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/ci.yml)
[![DCO](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/dco.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/dco.yml)
[![Pages](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/pages.yml/badge.svg)](https://github.com/LiaoRanran/CPP-Bible/actions/workflows/pages.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

> 本文件是**研究线（Queyi）**的 README。书籍正文（147 章现代 C++ 教程）见
> 主 [README.md](README.md)；研究报告官网见 [docs/](docs/)。

**Queyi** 把"用哪些检测器"本身当作可在失败中演化的对象：四态判决
（`pass / fail / unknown / contradict`）+ append-only 账本 + Merkle 完整性 +
确定性组合算子 **E**（failure / novelty / cost / redundancy 四分量）。
在 1,147 样本 × 8 资产的**全量真实检测矩阵**上，E 的选择在评估集取得
**+24.03pp**（vs 预注册随机单点预算，McNemar p≈2e-41），并对 split、5,000 次种子、
255 个资产子集稳健；683 批次新增 **110 条真实缺陷重构靶场**（全部可追溯 + NVD 在线验证）
与 **跨工具链一致性**（clang 18 vs g++ 13.3）。

## 快速开始

```bash
# ① 纯 Python 数据链（无需编译器）：数字对账 + 消融 + 站点数据
python tools/verify_paper_numbers.py          # 论文/仓库数字一致性（fail-closed）
python tools/analyze_683_oc.py --stage all    # operator 16+16 配置消融 + 7 基线
python tools/site_683_data.py                 # 再生成 docs/ 站上数据（同源）

# ② 真实靶场全链（需要 WSL g++ 13.3 + MinGW g++ 13.1 + clang++）
python tools/collect_realworld_683.py --stage verify    # NVD API 在线验证（需网络）
python data/realworld_683_runner.py --stage detect      # 110 × 8 真实检测（增量 checkpoint）
python data/realworld_683_runner.py --stage merge

# ③ 跨工具链 / 跨平台
python tools/cross_toolchain_683.py --stage b1 --limit 5   # 冒烟
python tools/cross_toolchain_683.py --stage b1             # 200 分层抽样
python tools/cross_toolchain_683.py --stage b2             # ≥50 并发类样本
```

## 数据

| 数据 | 规模 | 位置 |
|---|---|---|
| 真实靶场 PoC + 元数据 | 110 条（CVE/issue/commit 可追溯，PoC 单文件 <200 行） | `data/real_world/RW-*.cpp`、`data/683_real_world_benchmark.json` |
| 真实靶场判定矩阵 | 110 × 8（真实编译/运行） | `data/683_real_world_detection_matrix.json` |
| CVE 在线验证 | 109/109 FOUND（NVD 应答原文冻结） | `data/683_real_world_candidates_verified.json` |
| 合成语料判定矩阵 | 1147 × 8（两次克隆族切分复验） | `data/blindspot_676g_detection_matrix.json` |
| 机器可读元数据 | Croissant core + RAI（官方校验通过） | `data/croissant.json`、`data/rai_metadata.json` |

## 论文

- 主稿：`research/latex/queyi_neurips2027_v1.1.tex`（tectonic 编译；正文 ≤9 页门禁）
- 数字对账：`tools/verify_paper_numbers.py`；页数/摘要门禁：`tools/paper_quality_gate_670c2.py`
- 683 附录：Real-World Validation / Toolchain Sensitivity / Operator Ablation (16 Configurations)

## 复现与容器

- 环境：WSL Ubuntu g++ 13.3（sanitizer 双档 -O0/-O2）+ MinGW g++ 13.1（本地资产）+ clang 17+/18+
- 容器：`docker compose build queyi`（数据链）/ `docker compose run --rm paper`（论文编译）
  > 注：683 执行环境无 Docker，compose/Dockerfile 已过语法校验、未实测构建（详见验收报告）。

## 贡献与治理

- 提交规范：DCO 签名（`git commit -s`），见 [DCO.md](DCO.md) 与 [CONTRIBUTING.md](CONTRIBUTING.md)
- 安全策略：[SECURITY.md](SECURITY.md)（不接收武器化利用链；靶场样本只收"缺陷最小重构"）
- 引用：[CITATION.cff](CITATION.cff)
- AI 使用声明：本仓库工具/分析由作者主导、AI 辅助；人类作者对一切结论与数字负责
  （每条 AI 产出按验收协议逐项检查，见 `data/*验收报告*.md`）。

## 诚实边界（必读）

1. 检测器组合演化是**工程化形式化 + 治理**贡献，不是新算法理论；
   novelty 的字面定义与 failure **数学等价**（已证明并公开），unique 变体为探索性修复。
2. 样本主体为合成/半合成；真实靶场以**重构**方式引入（不等价于原始项目上下文）。
3. 未被证据支持的项一律保留 `⬜ 未闭合`，绝不写成"安全/已确认"。
