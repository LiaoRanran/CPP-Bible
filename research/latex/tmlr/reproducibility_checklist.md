# Reproducibility Checklist（TMLR 备选 · Queyi）

> 基于 TMLR 作者指南「鼓励上传提高可复现性材料」精神，结合 ML 标准复现清单与 Queyi 实验实际产物整理。
> 每个条目给出**当前状态**与**权威产物路径**（均已在 `data/` 落盘，详见 `data/current_numbers.json::a5_experiments`）。

## A. 数据集（Dataset）

- [x] **描述**：holdout 41 可测真错样本（`planted=true`）+ corpus 64 可测样本；外部锚定 50 条；A5 全量 1137×8 矩阵；盲区地图 1147×8。
  - 来源：`data/holdout_reveal_5_672h.json`、`data/external_corpus_reveal_672h.json`、`data/a5_676f_matrix_*.jsonl`、`data/blindspot_676g_stats.json`
- [x] **获取方式**：上述 JSON/JSONL 已随仓库提供（匿名快照）。
- [x] **许可证 / 来源标注**：样本 `provenance` 三值枚举（`self-authored` / `source-derived-reconstruction` / `original-external-artifact=0`）；真实来源 74/74 已核查。
  - 来源：`data/holdout_expansion/SCHEMA.md`、`DATASHEET.md`
- [x] **划分**：holdout/corpus 口径与分母明确（catch+miss；unknown/not_error 不计）；A5 并列分析剔除 3 个退化资产（8→5）。

## B. 代码（Code）

- [x] **可用**：检测器、八资产基准、A5 重算、clone-aware、非退化池、演化算子全部脚本在 `tools/`（含 `analyze_677b_clone_aware.py`、`analyze_677c_nondegenerate.py`）。
- [x] **运行方式**：`REPRODUCE.md` + `bash docker/paper/run_all.sh`（fail-loud）；单条复算见 `tools/verify_paper_numbers.py`。
- [x] **依赖**：`requirements.txt` / `uv.lock`（python + pyyaml + hypothesis + ruff==0.6.9 + mypy==2.3.1）。
- [~] **随机种子**：A5 主端点 seed = `20260930`（落盘）；但**实验类未固定种子计数 = 0**（种子审计 `tools/seed_audit_676h.py` 结论）→ 如实登记，非所有随机步均固定。见 `data/current_numbers.json` 注释。

## C. 计算（Compute）

- [x] **硬件**：本地 x64 + g++/clang + WSL（sanitizer 分支依赖 WSL；缺 WSL 时 15 条样本静默降级 `unknown`，已登记为已知环境偏差）。
- [x] **时间**：A5 全量重算 / cluster bootstrap / 非退化池重算均有记录；复现脚本可在单机上跑通。

## D. 评估（Evaluation）

- [x] **指标**：holdout recall、corpus measurable recall、三臂对照 Δ（FD vs Static/Random）、McNemar p、效应量 h、e-value、盲区比、8 资产并集/单资产 catch 率。
- [x] **协议**：预注册对照（`uninterpretable` 条款：并列分析 Δ 跨 0 即触发）；精确 McNemar + Wilson CI + BH/Holm 多重比较校正。
- [x] **逐条溯源**：`tools/verify_paper_numbers.py` = 118 条检察 / 113 一致 / 0 硬伤；图表数据与 `reveal_update_672h.json` 逐字对账。

## E. 模型 / 配置（Model & Config）

- [x] **检测器配置**：8 资产（asan/ubsan/compiler-warn/cross-compile/…）固定；`compile_exempt.json` 豁免清单。
- [x] **故障驱动演化算子**：可执行形式（`Evolution operator: executable form (677c)`）四分量 score + 两处坍缩披露。

## F. 治理 / 信任锚（Queyi 专属）

- [x] **四态判决 + append-only 账本**：452 事件 Merkle 根（`tools/tool_integrity.py`），受控目录零写。
- [x] **失败驱动演化**：FD 81.0% vs Static 4.8%（历史三臂实验）作为方法有效性内证。

> 注：TMLR 指南页**无强制复现清单**，本清单为「鼓励性」补充，提升审稿可信度；不替代 TMLR 投稿系统的元数据表单。
