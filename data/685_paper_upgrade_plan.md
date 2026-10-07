# 685 · D1 理论升级整合方案

- **批次**：685 ｜ **承接**：684 C2（治理+子模形式化为新增贡献 2）、683（真实靶场+附录）
- **配套**：`685_paper_modification_checklist.md`、`685_coordination_with_683_684.md`
- **约束**：正文已 9 页满；新增内容须 ≤1 页或进附录。

---

## 1. 本批产物的「落点」分配

| 本批产物 | 落点 | 篇幅 | 理由 |
|---|---|---|---|
| 子模形式化（684 已提）| 正文 Method 小节 | 1 段 | 684 C2 已规划 |
| **方向 1 自适应天花板**（定理 1/2 + +2.3pp 实验）| **附录 B.2** | ½ 页 | 定理+实验较深，正文满页；附录可容纳 |
| **方向 2 鲁棒稳定性**（引理 1/2 + 0.11pp 掉点）| **附录 B.3** | ½ 页 | 同上 |
| AGEA 框架（创新点 1）| 正文 Contribution / Introduction | 融入 684 贡献 2 措辞 | 已是论文最强资产，不需新页 |
| 能力边界量化器（创新点 3）| 附录脚注/正文 capability boundary 段 | 1 句 | 一行量，轻量 |
| 文献（S1–S39）| 正文 Related Work | 补 4–6 条 | 见 D2 |
| 候选方向（cost-aware/收敛/Pareto）| **Future Work** | 1 段 | 受数据缺失约束（684/685 红线）|

---

## 2. 与 684 子模框架的衔接

- 684 已把「资产选择 = 子模最大化 + (1-1/e) 保证 + 贪心=最优」作为贡献 2 的骨架。
- 685 在其上叠加两层**理论补丁**：
  1. **自适应天花板**（方向 1）：说明「贪心=静态最优」之后，自适应至多 +2.3pp，闭合 684 B3 悬念。
  2. **鲁棒稳定性**（方向 2）：说明该最优对 5% 检测器噪声稳健，闭合 676m 风险。
- 二者都**不**动摇 684 的核心 claim，而是加固「FD 是稳健、近最优、无需花哨算法」的叙事。

---

## 3. 与 683 的协调

- 683 在做**真实靶场（real-world defect reconstruction）+ 附录修改**。685 的附录 B.2/B.3 应与 683 的附录**合并章节**，避免重复/冲突（见 `685_coordination_with_683_684.md`）。
- 685 不触碰 683 的真实靶场数字，只在「理论附录」区增补方向 1/2。

---

## 4. 论文最终影响（预判）

- **贡献 2 升级**：从「子模形式化」扩为「子模形式化 + 自适应天花板 + 鲁棒稳定性 + 能力边界量化」，厚度与严谨度提升，仍保持「形式化而非新算法」的克制定位（684 C2 / 685 C3 诚实评估）。
- **Related Work 加强**：补 adaptive submodular（S4）、robust submodular（S7/S8）、HELM（S6）、Reward Hacking（S9），使治理框架有更强文献锚。
- **风险降低**：自适应天花板 (+2.3pp) 与鲁棒 (0.11pp) 把两个可能的审稿质疑（"为什么不用自适应？""对噪声稳健吗？"）提前用数据堵死。

---

## 5. 正文 ≤1 页的落地建议

正文只加**一句**总结性陈述（在 Method 末或 Experiments 末）：
> *"We further show (Appendix B.2–B.3) that the adaptive-selection ceiling is only +2.3pp above the static optimum and that the greedy choice is stable under 5% detector noise (≤0.11pp coverage drop), so no adaptive or robust optimization is required."*

其余细节全进附录。这样正文不超页，且把两个卖点挂到附录。
