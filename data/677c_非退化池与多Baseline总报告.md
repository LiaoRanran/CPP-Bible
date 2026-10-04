# 677c · 非退化池与多 Baseline 总报告

- 生成：2026-10-04T12:19:30+08:00（tools/analyze_677c_nondegenerate.py --stage all；随机臂 2000 次）
- 红线遵守：不修改 holdout_reveal_661.py / 样本源码 / 676f 产物 / 论文；未重跑 detect()；不 push。

## 1. 退化资产分析（8 资产）

| 资产 | unknown% | catch% | 恒unknown | 预注册退化 |
|---|---|---|---|---|
| asan | 0.88 | 35.09 | 否 | 否 |
| compile-time | 100.00 | 0.00 | 是 | 是 |
| compiler-warn | 0.00 | 12.58 | 否 | 否 |
| cross-compile | 3.34 | 14.95 | 否 | 否 |
| linker | 0.00 | 0.88 | 否 | 是 |
| tsan | 0.88 | 22.43 | 否 | 否 |
| ubsan | 0.88 | 23.57 | 否 | 否 |
| wunsequenced | 100.00 | 0.00 | 是 | 是 |

关键：wunsequenced/compile-time 恒 unknown（100%）；**linker unknown=0%** 但 catch 率 0.88%<5%（预注册规则判退化）——卡片预估的「linker 高 unknown」与数据不符，池定义据此修正（详见 677c_pool_design_report.md）。

## 2. 非退化池设计（3 池）

- **Pool A（严格，5 资产）**：unknown<30% 且 catch≥5% —— asan, compiler-warn, cross-compile, tsan, ubsan；与 676f 预注册并列分析候选集一致（对账通过：True）。
- **Pool B（中等，6 资产）**：unknown<50% 且 catch≥0.5% —— A + linker。
- **Pool C（宽松，6 资产）**：仅剔恒 unknown —— ≡ Pool B（如实记录）。
- 单点选择差异验证：Pool A 在 k=1、2、3 不同; Pool B 在 k=1、2、3、4、5 不同; Pool C 在 k=1、2、3、4、5 不同；Pool A 的 k=4 单点恰巧与 FD 同集——正是被评审抓住的病理（结构碰撞概率 1/C(5,4)=0.2，随机分布层面 Random 与 FD 仍可分）。

## 3. Baseline 实现（7 个）

Random(2000)/FD/Static/Frequency/Greedy-coverage/Oracle(上界)/Info-gain(探索)；全部同矩阵同切分；**发现：frequency ≡ fd**（676f fail_hits 就是派生集 catch 计数）⇒ 当前 FD 缺少超越频率基线的机制，这正是任务 C 要补的。逐表见 677c_baseline_comparison.md。

## 4. Evolution Operator 算法化

- score 四分量实现 + 确定性迭代选择 + 5 配置消融（含探索性 unique-novel）。
- **披露：literal novel ≡ failure**（规格字面坍缩，一行证明见设计报告 §2）⇒ fd_novel≡fd_only；full 与 fd_only 的差异来自 redundancy/cost。
- fd_only ≡ greedy 贪心（等价断言全真）；full 检出率优于 676f FD 的档位：3/14。详见 677c_operator_design_report.md。

## 5. 非退化池上的 A5 结果

- Pool A：最优 k=1，FD 33.04% vs Random 单点 21.73%（均值 20.78%），Δ单点 +11.31pp（p=6.02e-08），Δvs均值 +12.26pp；显著 k：1、2、3
- Pool B：最优 k=1，FD 33.04% vs Random 单点 0.71%（均值 17.64%），Δ单点 +32.33pp（p=3.50e-50），Δvs均值 +15.39pp；显著 k：1、2、3、4、5
- Pool C：最优 k=1，FD 33.04% vs Random 单点 0.71%（均值 17.64%），Δ单点 +32.33pp（p=3.50e-50），Δvs均值 +15.39pp；显著 k：1、2、3、4、5

## 6. 核心机制 isolate 评估

核心机制被 isolate：在无预注册退化资产的 Pool A 上，FD 在 k=1、2、3 仍显著优于 Random（最优 k=1，Δ单点 +11.31pp，p=6.02e-08；Δvs 2000 均值 +12.26pp）⇒ 选择效应真实存在，但量级被原池 +24.03pp 放大，退化资产贡献见 §4。论文可升格为「去掉退化资产后 FD 仍以 +11.31pp（单点配对）/+12.26pp（vs 2000 均值）优于 Random（k=1）」。

## 7. 退化资产贡献量化

- 原池 k=4：Δ单点 +24.03pp（Δvs均值 +14.42pp）。
- Pool A（严格） k=4：Δ单点 +0.00pp ⇒ 退化贡献（原池−本池）+24.03pp（均值口径 +12.81pp）。
- Pool B（中等） k=4：Δ单点 +15.19pp ⇒ 退化贡献（原池−本池）+8.83pp（均值口径 +8.23pp）。
- Pool C（宽松） k=4：Δ单点 +15.19pp ⇒ 退化贡献（原池−本池）+8.83pp（均值口径 +8.23pp）。

## 8. 对论文的影响与更新建议

- 摘要/E4/表行/claims/结论 7 处锚点级建议见 677c_论文更新建议.md（P1–P8）；统一措辞：主端点 +24.0pp 必须与「非退化池最优 k Δ」并排；k=|A|-1 的 0 是选集碰撞不是机制反证。
- operator 叙事从 governance 换成算法规格（score 公式 + 消融 + 坍缩披露）。

## 9. 和 677b 的关系

- 独立互补：677b 修样本侧（clone-aware split），本批修池侧（退化资产）；本批全程用 676f 原 split，未与 677b 混。合并实验（clone-aware × 非退化池）留待两批落定后。

## 10. 未解决项和局限

- literal novel≡failure 的坍缩是规格缺陷：修复需改参考集（unique 变体已给探索性对照，是否转正由下一批决定）。
- 权重未学习；cost 用全量墙钟代理单样本成本；池阈值是工程决策。
- Pool B/C 含 linker ⇒ 预注册 uninterpretable 条款在这两池仍触发；只有 Pool A 完全脱敏。
- 单回合判定的 ~5% 跑间不稳定（676m 实测）照常适用于本批全部逐格结论。
- Random 单点配对 Δ 依赖抽样运气；已并报 2000 均值口径（期望效应）。

## 11. 提交信息

- 只 add 本批文件：tools/evolution_operator_677c.py、tools/analyze_677c_nondegenerate.py、data/677c_*.json、data/677c_*.md。
- DCO：`git commit -s`；不 push；commit hash 用 `git log --oneline -1` 查（不自指回填）。
- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage all` （随机臂 2000 次，seed=20260930）；自检：`python tools/evolution_operator_677c.py --check`。
