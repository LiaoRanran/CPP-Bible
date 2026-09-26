# probes/ — _arch_v20 只读探针目录

> 全部纯 Python 标准库；只读访问仓内数据，不修改 tools/evidence/atoms/tests/data 任何正式文件；
> 输出仅写入本目录 output/。固定随机种子 20260921，可复算。
> 运行方式（仓库根目录）：`python _arch_v20/probes/p0X_*.py`

| 脚本 | 服务方向 | 数据来源 | 性质 |
|---|---|---|---|
| p01_arggraph_robustness.py | 11 网络科学 / 12 信息论 / 7 独立性 | data/attack_edges_609.json、attack_edges_candidates.jsonl、human_attack_edge_annotations.jsonl | 仓内真实数据 |
| p02_confidence_sequence.py | 5 序贯分析 | n=1406,x=1 口径（v7 权威基线数字）+ Monte Carlo | 数学复算 + 合成模拟 |
| p03_conformal_abstention.py | 自由方向 A / 12 信息论 | tools/poison_surface_map.json（Part1）；合成 Monte Carlo（Part2） | 半实仓半合成，输出内已标注 |

## 关键结果摘要（详见各 output 文件）

### p01 论证图鲁棒性（output/p01_output.txt）
- 117 节点（42 MIS + 75 命题）、388 边（194 refutation + 194 related_atom 成对）。
- 度熵 2.858 bit；确定性名次（度,名称）定点移除 top5 节点 LCC 80→31（0.388，随机 100 次均值→71.2）；top12→20（0.250，随机→56.8）。
- 介数咽喉（取整）：MIS-MEM-024（4085）等。
- 可复现性：名次按（度降序, 节点名）确定性打破并列；介数浮点求和跨进程有 ±0.1 末位抖动故取整显示；两次独立进程输出逐字节一致。
- **镜像边 128 条、占 33.0%**（66 个"同 ATOM 多 prop→同 MIS"组），量化 v19 G9。
- 人审 388：approve 354 / modify 34 / reject 0（复核 v19 G1）。

### p02 置信序列 vs 固定 CP（output/p02_output.txt）
- CP 双侧 95% CI [0.0018%, 0.3956%]、单侧 95% 上界 0.3370%（复算 v19 G13 一致）。
- Beta 混合 e-process 置信序列 anytime 上界 0.9062%（宽 2.69 倍）。
- Monte Carlo（3000 次，p=0.01，每 20 样本偷看）：CP 经验虚报 13.80%，e-process 0.00%（理论 ≤5%，实测偏保守）。
- 0 逃逸下达到 0.5% 上界：CP n=598 vs CS n=2127（3.56 倍样本换任意时合法性）。

### p03 保形弃权 + 攻击面熵（output/p03_output.txt）
- 毒样例攻击面（83 个有分类/124 总）：H=2.879 bit，H/Hmax=0.832，2^H=7.4 类；A3+A1 占 48.2%。
- 合成机制演示（非仓内实证）：可交换下覆盖 96.7%（名义 90%）；OOD 漂移降到 86.5%；conformal p 值筛查以 11.4% 弃权率拉回 90.2%。

## 已知局限（不夸大）

1. p01 LCC 为无向指标，未按 W2 可信度权重加权（609 文件中 confidence 字段均为 low，权重语义不在该文件）。
2. p02 的 0.00% 是保守均匀 Beta 混合 + 定向计数的观测值，不代表零风险。
3. p03 Part2 全部为合成数据，仅演示机制；保形保证在阙疑的真实可迁移性未验证（需外部校准集）。
4. 未运行任何 gate/poison/tool_integrity 的 --check；结论不依赖监工工具的当次输出。
