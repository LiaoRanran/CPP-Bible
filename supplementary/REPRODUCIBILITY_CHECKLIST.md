# 可复现性检查清单（Reproducibility Checklist）

本清单对照会议（NeurIPS/系统领域）通用的可复现性标准，逐项给出本工作的满足状态与证据位置。
对应详细指南见 `supplementary/REPRODUCTION.md`；最小复现脚本见 `docker/minimal_repro.sh`。

## A. 环境（Environment）

- [x] **依赖完整声明**：`requirements.txt`（仅 min 依赖 pyyaml，复算脚本 stdlib-only）、`supplementary/environment.yml`、`docker/paper/Dockerfile`。
- [x] **运行时版本固定**：Python 3.13 venv、`docker/paper/Dockerfile` 固定 g++-13.3 / clang-18 / WSL2；复算不依赖外部版本。
- [~] **容器镜像**：`docker/` 下提供完整配置（`docker-compose.yml`、`Dockerfile`、`run_all.sh`），但**作者本机未实际构建镜像**（无 Docker 环境）。这是已知的诚实局限，非阻断项——所有论文数字可由冻结产物 + stdlib 脚本在任意 Python 环境复算，无需容器。

## B. 数据（Data）

- [x] **数据集可获得性**：1147 样本语料（构造夹具 + 110 真实 CVE 重构）的冻结结果全部入库 `data/*.json`，见 `supplementary/DATA_AVAILABILITY.md`。
- [x] **数据生成可复现**：构造夹具由 `tools/*.py` 确定性生成；真实 CVE 由 `tools/collect_realworld_683.py --stage verify` 重构（需网络，非阻断）。
- [x] **随机种子审计**：`tools/seed_audit_676h.py` 审计实验类脚本未固定种子数 = **0**（所有随机化步骤均已固定或显式声明）。

## C. 代码（Code）

- [x] **论文核心数字可复算入口**：`tools/verify_paper_numbers.py`（130 条数字逐条溯源，fail-closed）、`tools/recompute_a5_676f.py`（R1–R7 复算）。
- [x] **完整脚本索引**：`supplementary/scripts_index.md`（745 个 `tools/*.py` 自动生成索引，含模块 docstring）。
- [x] **冻结产物审计**：`data/704_verify_paper_numbers_report.md` 显示 130 条检察一致率 100%、硬缺失 0。

## D. 评估协议（Evaluation Protocol）

- [x] **统计检验可复现**：A5 主结果的 McNemar 检验 `p=2.30e-41`、95% CI `[20.51, 27.55]pp` 可从 `data/a5_676f_results.json` 直接复算（见 `supplementary/all_numbers.md`）。
- [x] **口径统一**：盲区率、环境感知、真实 CVE 均按统一统计口径（见 `data/blindspot_676g_stats.json` 的 `caliber` 字段），论文与数据卡一致。

## E. 计算（Compute）

- [~] **算力需求低**：复算仅需 Python + 读取 JSON，秒级完成；完整检测矩阵生成需 WSL + 编译器（g++/clang/msan/tsan 等），作者已在本机完成并冻结。
- [x] **耗时记录**：各资产 `wall_seconds` 记录在冻结 JSON（`wall_seconds_by_asset`）中，可供成本估算。

## F. 已知局限（逐项诚实登记）

1. **Docker 未实际构建**：镜像配置完整但未在本机构建验证——复算数字不依赖容器，故不影响数字可复现性。
2. **人类标注一致性 = 0**：标注由 AI 完成，κ 等指标标注者身份已在正文披露，未冒称人类 IAA。
3. **部分复算需网络**：683 真实靶场"联网重构"步骤需访问 NVD/GitHub，本机未执行；但其**结果**（65/110 = 59.09%）已冻结入 `data/683_real_world_detection_matrix.json`，可直接复算该数字。
4. **跨工具比较非同环境**：clang-tidy/cppcheck 与 Queyi（WSL+sanitizer）环境本质不同，结论仅作能力分歧参考。

> 本清单结论：除"容器镜像未实际构建"与"人类 IAA=0"两项已知的诚实局限外，论文所有数字均可独立、确定性复算，满足可复现性核心要求。
