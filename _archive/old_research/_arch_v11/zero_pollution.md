# zero_pollution · 590 异族调研全程零污染自证

> 任务 590 · 2026-09-19 · HEAD 开工/收工均为 d36d5c8（未变）
> 结论先行：**本轮唯一新增文件全部落在 `_arch_v11/`；正式目录零内容改动。**

---

## 一、纪律执行清单

| 禁止项 | 执行情况 |
|---|---|
| 不改 tools/evidence/atoms/Examples/data 正式文件 | ✅ `git diff` 内容空（见下证据） |
| 不跑 pytest / poison_drill / mutation_fuzz | ✅ 未跑；活数字仅以 `CPPBIBLE_OBS=0` 的只读探针跑 gate 的纯函数 |
| 不跑 git commit/checkout/reset/add | ✅ 仅用 log/status/diff/show（--help 未用） |
| 不跑 tool_integrity --update | ✅ 只跑 `--check`：输出"OK：5 个核心工具与基准一致" |
| 产出仅入 _arch_v11 | ✅ 见文件清单 |

## 二、基线对比证据

1. **开工基线**：`probes/head_before.txt`（d36d5c8，2026-09-19 13:33:54）、
   `probes/git_status_before.txt`（开工时全量 status）。
2. **收工状态**：`probes/git_status_after_filtered.txt`（排除 _arch_v11）。
3. **集合比对（本轮命令输出原文）**：
   > `IDENTICAL: before/after status excluding _arch_v11 = 0 differences`

   即：开工前存在的全部条目（tracked 标志、untracked 文件）在收工后逐条相同。
4. **tracked 内容差异**：收工时 `git diff --stat` 输出为**空**——无任何 tracked
   文件内容变化。

## 三、两个预存 `M` 标志的说明（非本轮造成）

开工首次 `git status` 即显示：

```
 M data/mutation/full_baseline_v4.json
 M evidence/conc/EV-CONC-001.md
```

- 该两标志在开工基线文件中已存在（非本轮引入）；
- `git diff` 对两文件内容零输出——属 **stat-dirty**（索引记录的 stat 与磁盘
  不一致，内容相同），非内容修改；
- 本轮未触碰两文件，也未运行 `update-index` 等改索引命令；标志在收工状态原样
  保留。

## 四、_arch_v11 产出清单（17 件：16 文件 + probes 证据目录）

| # | 路径 | 说明 |
|---|---|---|
| 1 | 00_总览_维度上限与差距矩阵.md | 矩阵 + 开头两句话 |
| 2-13 | 01-12 各维度探测文件 | 当前态/上限/差距/卡点/自由探索 |
| 14 | 13_自由探索_新维度新攻击面新技术.md | 新维度/A1-A5/T1-T5/新度量/新范式 |
| 15 | 14_拉满路线图建议.md | R1-R10 批次与解冻条件 |
| 16 | zero_pollution.md | 本文件 |
| 17 | probes/ | 只读探针与证据（见下） |

probes/ 内容：
- probe_v6_stats.py / probe_v6_stats.out（v6 基线全量统计，1593 变体逐条口径）；
- probe_gate_live.py / probe_gate_live.out（活 gate：191 命中、规则元数据）；
- head_before.txt、git_status_before.txt、git_status_after_filtered.txt（基线证据）。

探针纪律：两个探针只读文件/调用纯函数；gate 探针以 `CPPBIBLE_OBS=0` 关闭日志
写入，全脚本无写盘调用（除 stdout）。

## 五、收工结论

- 正式目录（tools/ evidence/ atoms/ Examples/ data/ 正式文件、根文档）：**零改动**；
- 新增内容：**仅 `_arch_v11/`**；
- HEAD：未变（d36d5c8）；
- 遗留风险无新增。验收可直接复跑本文件第二、三节的命令复核。
