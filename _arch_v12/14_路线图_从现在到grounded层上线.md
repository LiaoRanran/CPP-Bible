# 14 · 路线图：从现在到 grounded 层上线

## 阶段 0 · 现状（本次调研已完成）
- ✅ 手搓纯标准库 grounded 求解器（`probes/grounded_probe.py`）
- ✅ 79 命题 / 27 卡 / 116 支持边 / 79 MIS 实测
- ✅ 证明：纯 Dung grounded 在当前数据下**必然退化**（S0/S1/S2）
- ✅ 复杂度结论：grounded 微秒级，瓶颈在攻击边缺位

## 阶段 1 · N（现在就能做，已部分完成）
- [x] 求解器 + 实测
- [ ] 攻击边密度 / 退化指数度量脚本（13.5）
- [ ] MIS→候选攻击边自动生成脚本（N 段，零 Oracle 风险）

## 阶段 2 · D（攒数据，需人审/写作工序）
- [ ] 定义权重来源（verified/machine_verified > MIS level）→ 加权 AF schema
- [ ] 人审裁决 MIS 自动生成的候选攻击边
- [ ] 在加权 AF 下重测：IN/OUT/UNDEC 真实分布 + suspect 级联（维度 2/4 第二探针）
- [ ] 人审样本：undecided 裁决（维度 11 比例实测）

## 阶段 3 · 上线（W 触发条件满足后）
- [ ] grounded 层接入 `replay` 三分类映射（维度 7）+ golden_lock 闸门
- [ ] 辩护链可视化（Argdown，维度 6）
- [ ] 收敛曲线接 573 monotone_convergence（维度 8）
- [ ] 仅当语义需要：clingo 跑 preferred/stable（维度 5）
- [ ] 仅当解冻信号触发：概率/模糊扩展（维度 9）

## 发布门槛（建议）
1. 攻击边密度 > 0（当前 0）；
2. 退化指数 < 0.9 且 OUT 非空（排除 S0 全接受）；
3. 加权后 IN 命题与现有 confirmed 一致性 ≥ 某阈值（排除 S1 倒置）。

## 一句话
**算法已免费就位，路线图的核心是推动 D 段（造可信加权攻击边），而非继续研究语义。**
