# 688 · C4 投稿时间线建议

- **批次**：688 ｜ **基准日**：2026-10-07 ｜ **约束**（已核实）：
  - NeurIPS 2026 E&D 截止为 2026-05-06（**已过期**）→ 目标 **NeurIPS 2027**（CFP 预计 2027-01~02 发布，截止预计 2027-05 AOE）。
  - arXiv 个人背书门槛阻塞（2026-01 政策）→ 需背书人或 TechRxiv 绕开。
  - TMLR rolling、**无需 endorsement**、可先发可引用。
  - 687 批次正在合并论文（v1.3+真实靶场+批判修订），**最终稿尚未定**。

## 1. 推荐顺序（为何如此）
**TMLR（先发可引用+评审反馈） → arXiv/TechRxiv（并行可见性） → NeurIPS 2027（旗舰目标）**
- TMLR 无 endorsement、rolling，能最快拿到同行评审与 DOI，其反馈可反哺 NeurIPS 稿。
- arXiv 当前阻塞，用 **TechRxiv**（IEEE，无门槛，给 DOI）作保底可见性；背书到位后再补 arXiv。
- NeurIPS 2027 为最终旗舰；TMLR 在审不影响投会议（须声明，TMLR 允许 conference 版）。

## 2. 时间线表

| 节点 | 时间窗 | 交付物 / 动作 | 依赖 |
|---|---|---|---|
| **P0 论文定稿** | 2026-10 ~ 11 | 687 合并完成；吸收 686/688 建议：1137/1147 脚注、摘要 +24pp 并排 +7-12pp、演化算子降级、E9 观察性化、Croissant+RAI 随稿 | 当前进行中 |
| **P1 匿名化 + 复现清单** | 2026-11 ~ 12 | 移除 LiaoRanran/GitHub 身份；匿名代码托管；TMLR Reproducibility checklist；REPRODUCE.md+fail-loud 复核 | P0 |
| **P2 投 TMLR** | 2026-12 ~ 2027-01 | 提交 TMLR（rolling）；附 Croissant+RAI、匿名代码、复现清单 | P1 |
| **P3 预印本可见性** | 2026-12 ~ 2027-3 | 并行：post **TechRxiv**（无门槛 DOI）；联系 arXiv 背书人，到位后 post arXiv(cs.SE) | P1 |
| **P4 NeurIPS 2027 CFP 复核** | 2027-01 ~ 02 | CFP 发布后核验页数/双盲/截止/分类；按 E&D 要求精修（双盲匿名、Croissant+RAI、code_justification）| P0 |
| **P5 NeurIPS 2027 投稿** | 2027-05 (AOE 预计) | 全文+数据+代码截止；声明 TMLR 在审状态；双盲提交 | P4 |
| **P6 评审/录用** | 2027-09 预计 | 收审稿意见；rebuttal 用 686 弹药库 + 688 真实靶场细分 | P5 |

## 3. 关键截止与风险
- **NeurIPS 2027 截止为预测**（以 CFP 为准）——CFP 发布后立即锁定真实日期，本表 2027-05 为估计。
- **arXiv 背书**是非技术阻塞：若 P3 拿不到背书，TechRxiv 保底仍保证可见性，不阻断 NeurIPS 投稿（会议不要求预印本）。
- **TMLR × NeurIPS 重叠**：TMLR 允许投会议版，但 NeurIPS 要求工作未发表；TMLR 在审（未录用/未在线发表）通常兼容，投稿时须声明——**不可已在线发表于 TMLR 后再投 NeurIPS**。
- **条件复现（686 #9）**：NeurIPS/TMLR 均查可复现性；须确保 fail-loud + 匿名托管 + B2 量化已写入 Limitations。

## 4. 投稿前必做清单（Pre-submission TODO）
- [ ] 1137/1147 脚注（686 #1）
- [ ] 摘要 +24pp 与 +7-12pp 并排（686 #4）
- [ ] 演化算子贡献降级为可证伪框架（686 #2 / 688 B1 确认无增益）
- [ ] E9 改为 cross-regime observational（688 B3）
- [ ] Croissant+RAI 随稿（682 已备）
- [ ] 匿名代码托管 + Reproducibility checklist
- [ ] 双盲匿名（移除身份/GitHub 直链）
- [ ] 真实靶场细分（688 A1-A5）补入论文 external validity 段

## 5. 诚实边界
- NeurIPS 2027 具体日期/页数/分类为**预测**，CFP 发布后必须复核；不得把预测当事实。
- arXiv 背书能否落地依赖社区关系，非技术可控；故 TechRxiv 保底必做。
- 时间线假设 687 在 2026-11 前定稿；若 687 延迟，P1-P5 整体顺延。
