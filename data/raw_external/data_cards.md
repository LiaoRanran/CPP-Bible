# Data Cards (699 批外部数据)

> 参考 Croissant 风格（682 批已做过 Croissant+RAI）；每张卡含：来源、规模、许可证、标注方式、已知偏差。

## Card 1 — 原始项目真实缺陷 (699-A)
- **source**: 真实开源项目 git history（NVD + 项目官方安全公告）
- **size**: 22 条（12 个项目：libwebp, curl, OpenSSL×6, zlib, polkit, libxml2×3, xz, GnuTLS, glibc×3, Linux kernel, FFmpeg, SQLite）
- **license**: 各项目自身许可证（数据本身为事实汇编，可引用）
- **annotation**: CVE / 受影响版本 / 修复版本 / 修复 commit（5 个 verified）/ 缺陷家族
- **known bias**: 构建未实测（WSL 无出口）；修复 commit 仅 5 个 verified；CVSS 为 nvd-reported
- **location**: `data/699_original_project_defects.json` + `original_projects/<CVE>/`

## Card 2 — JudgeBench
- **source**: ScalerLab / University of Washington — https://huggingface.co/datasets/ScalerLab/JudgeBench
- **size**: 数千 pairwise（数学/推理/代码/梗概等困难样本）
- **license**: **需复核**（HF 页面未明示；疑似 MIT/Apache-2.0）
- **annotation**: 人类专家判定两回答中更优者（label: A>B / B>A）
- **known bias**: 困难样本偏多；长度裁判一致率仅 0.44（强长度 Goodhart）
- **location**: 统一文件 `data/699_llm_eval_unified_format.json`（source_dataset=JudgeBench）

## Card 3 — RewardBench
- **source**: AllenAI — https://huggingface.co/datasets/allenai/reward-bench
- **size**: ~23k preference pairs（Chat / Reasoning / Safety / Instruction）
- **license**: **ODC-BY**（须遵守下游各子集许可）
- **annotation**: 策展的 chosen vs rejected 偏好对
- **known bias**: chosen 被策展为"更好且更长" → 长度混淆变量（长度裁判一致率 1.0）
- **location**: 统一文件（source_dataset=RewardBench）

## Card 4 — MT-Bench
- **source**: LMSYS — https://huggingface.co/datasets/lmsys/mt_bench_human_judgments
- **size**: 80 题 × 多模型两轮回答 + GPT-4/人类评判（评分 1–10）
- **license**: **CC-BY / lmsys 条款**
- **annotation**: GPT-4 评判 + 人类评判
- **known bias**: LLM 评判偏置（位置/长度/风格）；需 prompt 改写测口径漂移
- **location**: 仅目录收录（metadata），未在统一文件抽样；download_llm_eval.py 可扩展接入

## Card 5 — AlpacaEval
- **source**: LMSYS / Stanford — https://github.com/tatsu-lab/alpaca_eval
- **size**: 805 条指令 + 模型回答 + 胜率（长度偏差校正）
- **license**: **MIT（代码）/ 数据 CC**
- **annotation**: LLM 裁判 pairwise 胜率（带长度校正）
- **known bias**: 长度偏置最典型（正是结构性 Goodhart 的教科书案例）
- **location**: 仅目录收录（metadata）；download_llm_eval.py 可扩展接入
