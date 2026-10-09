# data/raw_external — 699 批外部数据目录

> 本目录存放 699 批从公开来源收集的**外部数据**及其复用说明。所有数据均为真实来源，无任何编造。

## 结构

```
raw_external/
├── README.md                      # 本文件：来源与使用说明
├── original_projects/             # 699-A：22 个真实项目缺陷，每 CVE 一个子目录
│   └── <CVE>/
│       ├── clone_build.sh         # clone + checkout + build 脚本（未在本环境执行）
│       └── README.md              # 该缺陷的元数据卡
├── llm_eval/                      # 699-B：LLM 评估公开数据集
│   ├── download_llm_eval.py       # 在可联网环境重跑即可取全量
│   └── README.md                  # 数据集清单与许可证
└── (data cards 见下方)
```

## 数据卡 (Data Cards)

| 数据集 | 类型 | 规模 | 许可证 | 标注方式 | 已知偏差 |
|--------|------|------|--------|----------|----------|
| 原始项目缺陷 (22 CVE) | C/C++ 真实漏洞 | 22 | 各项目自身许可 | 官方 advisory / CVE | 构建未实测（无 WSL 出口） |
| JudgeBench | LLM judge 基准 | 数千 pairwise | 需复核 (HF) | 人类专家 A/B | 困难样本偏多 |
| RewardBench | 偏好对 | ~23k | ODC-BY | 策展 chosen/rejected | 长度偏置混淆 |
| MT-Bench | 多轮对话评判 | 80 题×多模型 | CC-BY/lmsys | GPT-4 + 人类 | LLM 评判偏置 |
| AlpacaEval | 指令遵循胜率 | 805 条 | MIT/CC | LLM pairwise（长度校正） | 长度偏置最典型 |


## 701 批更新（2026-10-09）

- **699 的 22 个项目已在 WSL 实测编译**：14 built:true / 8 built:false（详见 `../../701_build_results.md`）。699 记录的“构建未实测（无 WSL 出口）”**已过期**——701 实测 WSL 可联网。
- **新增 18 个真实 C/C++ 缺陷**（`../../../data/701_new_project_defects.json`），`original_projects/` 下新增对应 `<CVE>/README.md` + `clone_build.sh`。
- **统一索引**：`raw_external/index.json`（40 个案例）。**一键构建**：`original_projects/build_all.sh`。
- 案例库规模：**40 个已提供构建脚本，其中 14 个经 701 实测编译通过**。

## 复用接口

```python
from tools.data_loader_699 import (
    load_original_project_defects,
    load_llm_eval_data,
    get_original_project_defects_by_family,
)
defects = load_original_project_defects()["defects"]   # 22 条
llm = load_llm_eval_data()["records"]                  # 240 条真实样本
```

## 已知偏差与限制（诚实记录）

1. ~~构建未实测~~ **已由 701 批修正**：22 个在 WSL 实测，14 built:true / 8 built:false（见 `../../701_build_results.md`）。新增 18 个仍为 script-provided-not-executed。
2. **修复 commit 核实**：5 个 verified=true（短 SHA 取自官方公告）；其余仅以公告 URL 引用，完整 SHA 须在该环境解析。
3. **CVSS 标注**：值为 `nvd-reported`，发表前须用 NVD 2.0 API 复核。
4. **LLM 数据集样本**：统一文件中的 240 条为实时下载的真实抽样；全量（数千/数万）须在有出口环境重跑 `download_llm_eval.py`。
5. **许可证**：JudgeBench 许可证在可检索来源未明示，发表前须到 HF 仓库确认。

## 来源 URL

- 原始缺陷：各 CVE 见 `nvd.nist.gov/vuln/detail/<CVE>` 及项目官方安全公告（详见各 `original_projects/<CVE>/README.md`）。
- LLM 数据集：
  - JudgeBench — https://github.com/ScalerLab/JudgeBench · https://huggingface.co/datasets/ScalerLab/JudgeBench
  - RewardBench — https://github.com/allenai/reward-bench · https://huggingface.co/datasets/allenai/reward-bench
  - MT-Bench — https://github.com/lm-sys/FastChat · https://huggingface.co/datasets/lmsys/mt_bench_human_judgments
  - AlpacaEval — https://github.com/tatsu-lab/alpaca_eval
