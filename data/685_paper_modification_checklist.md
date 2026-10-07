# 685 · D2 论文修改清单（逐节：旧文 → 新文 → 理由 → 来源）

- **批次**：685 ｜ **对象**：`research/latex/queyi_neurips2027_v1.1.tex`（v1.3 / 677d）
- **前提**：行号基于 684 读取快照；合并前须与 683 最终版 `git diff` 复核（见 `685_coordination_with_683_684.md`）。**本批不改正文**（红线：只读共享产物）。

---

## 1. Abstract（L76–99）

| 行 | 当前旧文（摘）| 建议新文 | 理由 | 来源 |
|---|---|---|---|---|
| L94–96 | 「non-degenerate selection effect +7–12pp … A5 isolates 'do not fund assets that cannot inform'」| 末尾补：「; we further prove the adaptive-selection ceiling is only +2.3pp above the static optimum and the greedy choice is stable under 5% detector noise.」| 把 685 两结论挂到摘要 | D1 §5 |

## 2. Contributions（L145–167）

| 行 | 当前旧文 | 建议新文 | 理由 | 来源 |
|---|---|---|---|---|
| L145–151(贡献1) | 「evolution operator」| 维持但保持 instantiation 语气（684 C3 已改）| 与 684 一致 | 684 C3 |
| L164–167(新增贡献4) | （684 已加子模形式化）| 在贡献 4 末尾补：「including an adaptive-selection ceiling (+2.3pp) and a robustness bound (≤0.11pp drop under 5% noise).」| 把 685 定量结论并入贡献 2/4 | D1 §1 |

## 3. Method — Selection as submodular（L1052 之后，684 已加段落）

| 位置 | 建议新增段落 | 理由 | 来源 |
|---|---|---|---|
| 684 子模段落之后 | 「**Adaptive ceiling.** The adaptive optimum (knowing the defect group) exceeds the static optimum by at most the *conditional-diversity gap*; on our data this gap is +2.3pp (Appendix B.2). **Robustness.** Coverage is 1-Lipschitz in the verdict matrix, so the greedy choice is stable under detector noise (Jaccard 0.96 at 5%; ≤0.11pp coverage drop; Appendix B.3).」| 把方向 1/2 的论文挂点写进 Method | D1 §1 |

## 4. Experiments（新增附录 B.2 / B.3）

| 位置 | 建议新增（附录）| 理由 | 来源 |
|---|---|---|---|
| 新 Appendix B.2 | 方向 1 全文：定理 1/2 + 表（Static 59.33 / Ceiling 61.62 / Actual 57.75）+ 条件多样性解读 | 完整理论+实验 | 685_direction1_theory/report |
| 新 Appendix B.3 | 方向 2 全文：引理 1/2 + 表（ε=0.01–0.10 的 Jaccard 与掉点）+ 噪声自洽率为假象说明 | 完整理论+实验 | 685_direction2_theory/report |

## 5. Related Work（L205 之后）

| 位置 | 建议新增文献 | 理由 | 来源 |
|---|---|---|---|
| L205 后 | 补 4 条：adaptive submodular (Golovin & Krause 2011, S4)；robust submodular (Orlin-Saha 2018 S7 / Mitrović 2017 S8)；HELM (Liang 2023 S6)；Reward Hacking (Skalse 2022 S9) | 支撑方向 1/2 与治理框架 | A1 文献矩阵 |

## 6. Conclusion

| 位置 | 当前旧文 | 建议新文 | 理由 | 来源 |
|---|---|---|---|---|
| 结论段 | 「robust, submodular-greedy selector … directional」| 补：「—a claim now backed by a quantified adaptive ceiling (+2.3pp) and noise stability (≤0.11pp).」| 闭合结论 | D1 §4 |

---

## 7. 合并纪律（与 683/684 协调）

- 本清单所有修改**不在此批提交**；等 683 完成附录后，由统一批次（建议 686/合并批）按本清单 + 684 C3 清单落地。
- 落地前用 `git diff` 复核行号漂移；所有新增数字必须从 `685_direction*_experiment.json` / `684_*` 取，**不得手写**。
- 真实靶场数字（683）与理论附录（685）在附录章节合并，避免重复。
