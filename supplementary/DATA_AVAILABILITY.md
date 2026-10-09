# 数据可用性声明（Data Availability Statement）

**论文：** Queyi: 零成本静态感知的 C++ 缺陷检测资产选择
**版本：** v1.1（NeurIPS 2027 投稿稿）
**日期：** 2026-10-09

## 1. 公开释放的内容

本投稿释放以下全部内容于项目仓库（公开镜像，地址待填：`https://github.com/<owner>/CPP-Bible`，投稿时替换为实际仓库 URL）：

| 类别 | 路径 | 说明 |
|---|---|---|
| 补充材料包 | `supplementary/` | 本目录：README、REPRODUCTION.md、environment.yml、脚本索引、全部声明 |
| 冻结实验结果 | `data/*.json`（a5_676f / 676g / 682 / 683 / 692 / 700 / 703 等） | 所有论文数字的权威源，复算只读这些产物，**不含任何检测器运行时产物** |
| 复算脚本 | `tools/*.py`（recompute_a5_676f.py、verify_paper_numbers.py 等） | stdlib-only，无需第三方依赖即可复算论文数字 |
| 复现配置 | `docker/`（paper/queyi/reproduce）、`docker-compose.yml`、`Dockerfile`、`requirements.txt` | 从零复现环境与最小复现脚本 `docker/minimal_repro.sh` |
| 论文源 | `research/latex/queyi_neurips2027_v1.1.tex` + 附录 | 完整 LaTeX 源 |

## 2. 数据集构成与可用性

- **缺陷语料库**：1147 个 C++ 缺陷样本（corpus + holdout + 真实靶场）。其中：
  - 构造性夹具（synthetic fixtures）由本仓库脚本生成，可完全复现；
  - **真实 CVE 重构集（110 例）**：来自公开 NVD / GitHub Advisory，按 `tools/collect_realworld_683.py` 重构为最小复现夹具，保留原始 CVE 编号与来源链接（去标识化，不含任何非公开信息）。
- **可用性分级（证据口径，遵循项目自检标准）**：
  - *已核实*：所有论文引述数字对应的冻结 JSON 均已入库，可逐条复算（见 `supplementary/all_numbers.md` 与 `data/704_verify_paper_numbers_report.md`）。
  - *待核实*：人类标注一致性（human IAA）全仓库为 0——标注由 AI 第二遍（source-evidence annotator）完成，非人类标注；论文正文已如实披露。

## 3. 不释放的内容与理由

- **检测器运行时中间产物**（各 sanitizer/编译器日志、WSL 实测耗时原始输出）：体积大且可由冻结 JSON + 脚本确定性重算，故不入库。
- **任何个人数据 / 第三方专有代码**：语料库均为构造夹具或已公开的 CVE 最小复现，**不含个人身份信息或专有闭源代码**。

## 4. 许可

代码与脚本以仓库声明许可证释放；数据集（缺陷夹具）以同等许可释放，真实 CVE 重构归属原始上游项目并附来源链接。

## 5. 获取方式

投稿接收后，所有上述材料随论文开源仓库公开。最小复现三步见 `supplementary/REPRODUCTION.md` 与 `docker/minimal_repro.sh`（无需 Docker 亦可复算 3 个核心实验的数字）。
