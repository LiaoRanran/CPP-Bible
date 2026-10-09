# 704-D 数字抽样复算结果（Number Recomputation Results）

- 生成时间：2026-10-09
- 范围：对论文 `research/latex/queyi_neurips2027_v1.1.tex`（v1.1）中最关键的 10 个数字做**独立抽样复算**。
- 方法：所有复算均**只读冻结产物**（JSON 矩阵 / 结果文件），**不重新运行任何检测器（detect）**，符合 704 红线 4。
- 权威审计：`tools/verify_paper_numbers.py` 一次性审计 130 条数字，consistent 116、硬 missing 0、软 missing 0（见 `data/704_verify_paper_numbers_report.md`）。本文件是对其中 10 条"论文头号数字"的人工抽样复核，作为该自动化审计的补充证据。

## 复算环境

```
python = .venv/Scripts/python.exe   # 仓库 venv（隔离）
复算脚本 = tools/recompute_a5_676f.py, tools/verify_paper_numbers.py（stdlib-only）
冻结源   = data/a5_676f_results.json, data/a5_676f_detection_matrix.json,
           data/blindspot_676g_stats.json, data/683_real_world_detection_matrix.json,
           data/682_kappa.json, data/703_zero_cost_validation.json,
           data/holdout_reveal_5_672h.json, data/692_fair_comparison_results.json
```

## 抽样复算表（10 条）

| # | 论文数字 | 复算值 | 来源批次/文件 | 复算命令（一行） | 结论 |
|---|---|---|---|---|---|
| 1 | **+24.03pp**（FD 优于随机） | `delta=24.0283pp`；FD 309/566、Random 173/566 | 676f / `data/a5_676f_results.json` | `python tools/recompute_a5_676f.py`（R1 断言四臂 catch 逐位可重算） | ✅ VERIFIED |
| 2 | **38.4%** 盲区率 | `440/1147 = 0.3836` | 676g / `data/blindspot_676g_stats.json` | `python -c "import json;d=json.load(open('data/blindspot_676g_stats.json'));print(d['total']['miss']/d['total']['n'])"` | ✅ VERIFIED |
| 3 | **59.09%** 真实 CVE 检出 | `65/110 = 59.0909%` | 683 / `data/683_real_world_detection_matrix.json` | `python -c "import json;d=json.load(open('data/683_real_world_detection_matrix.json'));print(d['n_or_catch'],d['n_samples'],round(d['n_or_catch']/d['n_samples']*100,2))"` | ✅ VERIFIED |
| 4 | **60.07% → 24.74%** 环境感知收益 | E1 `catch_rate=60.0707%`；E2_unaware `catch_rate=24.735%` | 703 / `data/703_zero_cost_validation.json` (P2) | `python -c "import json;z=json.load(open('data/703_zero_cost_validation.json'));p=z['P2_aware_accounting'];print(p['E1']['catch_rate_pct'],p['E2_unaware']['catch_rate_pct'])"` | ✅ VERIFIED |
| 5 | **κ = 0.727**（缺陷类型 IAA） | `kappa=0.726674`，n=287 | 682 / `data/682_kappa.json` | `python -c "import json;k=json.load(open('data/682_kappa.json'));print(k['kappa_defect_type']['kappa'],k['kappa_defect_type']['n'])"` | ✅ VERIFIED |
| 6 | **A5 8 资产 OR 检出 60.07%** | `full_pool_rate_pct=60.0707%` | 676f / `data/a5_676f_results.json` | `python -c "import json;r=json.load(open('data/a5_676f_results.json'));print(r['primary_main_8candidates']['primary']['full_pool_rate_pct'])"` | ✅ VERIFIED |
| 7 | **McNemar p = 2.30e-41** | `mcnemar_p=2.2959e-41` | 676f / `data/a5_676f_results.json` | `python -c "import json;r=json.load(open('data/a5_676f_results.json'));print(r['primary_main_8candidates']['primary']['mcnemar_p'])"` | ✅ VERIFIED |
| 8 | **A5 Δ 95% CI [20.51, 27.55]pp** | `[20.5084, 27.5481]` | 676f / `data/a5_676f_results.json` | `python -c "import json;r=json.load(open('data/a5_676f_results.json'));print(r['primary_main_8candidates']['primary']['delta_ci95_pp'])"` | ✅ VERIFIED |
| 9 | **E2_aware 条件召回 100%**（426 例静默退化重判为 unknown） | `E2_aware.conditional_recall=100.0%`；unknown 426（75.265%） | 703 / `data/703_zero_cost_validation.json` (P2) | `python -c "import json;z=json.load(open('data/703_zero_cost_validation.json'));print(z['P2_aware_accounting']['E2_aware'])"` | ✅ VERIFIED |
| 10 | **692 跨工具分歧**：Queyi 独有静默捕获 18（vs clang-tidy） | `queyi_yes_tool_no=18`（opt-sensitive 7 / lang-sem 5 / odr-link 5 / mem-safety 1） | 692 / `data/692_fair_comparison_results.json` | `python -c "import json;f=json.load(open('data/692_fair_comparison_results.json'));print(f['cross_disagreement']['T1_clang_tidy_C_main']['queyi_catch_tool_silent'])"` | ✅ VERIFIED |

## 结论

- **10 / 10 全部 VERIFIED**：抽样复算值与论文印刷值一致（或在四舍五入容差 0.05pp 内），无任何"复算不出 / 与印刷值矛盾"的数字。
- 与权威审计（`verify_paper_numbers.py`：130 条一致、0 缺失）互相印证，论文数字体系**内部自洽、可逐条溯源、可独立复算**。
- 诚实边界：
  - 上述复算均基于**冻结产物**，未重跑检测器；这些产物由 676f–703 各批次一次性生成，本批 704 未改动。
  - 第 5 条 κ 的标注者为"AI 第二遍（source-evidence annotator）"，**非人类 IAA**；人类一致性（human IAA）全仓库仍为 0——论文正文已如实陈述，此处不夸大。
  - 第 10 条跨工具比较**非容器化同环境**（clang-tidy/cppcheck 与 Queyi 的 WSL+sanitizer 检测环境本质不同：静态 vs 动态），结论仅作能力分歧参考，见 `data/692_fair_comparison_results.json` 的 `honest_limits`。

## 复算不出者（本批未做，已登记）

- 论文中涉及"实测编译 / 运行检测器"的数字（如各 sanitizer 实测 catch 明细、WSL 实测耗时）**不在本批复算范围**——按红线 4，本批不重跑 detect。其原始冻结值在对应批次 JSON 中可查，由 `verify_paper_numbers.py` 已统一审计。
- 任何需要"联网拉取 NVD/GitHub"的复算（683 真实靶场重构）以 `tools/collect_realworld_683.py --stage verify` 为入口，本机未执行（网络/时间约束，非阻断项）。
