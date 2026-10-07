# 684 · B3 自适应选择策略（轻量实验）

- **批次**：684 ｜ **机读**：`data/684_adaptive_experiment.json`
- **红线**：不跑真实 `detect()`；仅用 676f 矩阵模拟；train/test 用 677b clone-aware `strict_stratified` split，**无泄漏**。
- **种子**：20260930（与 676f/677c 一致，可复现）。

---

## 1. 实验设定

- **样本**：1137；clone-aware strict split 后 **train(derivation)=569 / test(evaluation)=568**（克隆对跨越 = 0，见 677b）。
- **训练（train）**：仅用 train 估计 ① 缺陷组先验 $P(g)$；② $P(\text{asan 判定}\mid g)$；③ $P(\text{catch}\mid a, g)$（类型×资产有效性矩阵）。**测试样本的其他资产判定在训练阶段绝不参与**。
- **测试（test）**：对每个 test 样本，仅允许观测 `asan` 判定（模拟「先跑 asan」），其余判定在选臂阶段不可见。
- **预算**：每样本最多 4 资产（与 $k=4$ 主口径一致）。

### 五策略定义

| 策略 | 选择规则 | 是否在 test 泄漏 |
|---|---|---|
| **Static** | 固定静态资产 `{compiler-warn, cross-compile, linker, compile-time}` | 否（字典序固定）|
| **FD_greedy** | 在 train 上残差贪心选 4（= A2/A3 子模贪心）| 否（train 选，test 评）|
| **FD_frequency** | 在 train 上 catch 计数降序 top-4（= 676f 实际方法）| 否 |
| **Random_single** | 种子固定单次随机 4 | 否 |
| **Random_mean2000** | 2000 次随机 4 的均值（期望口径）| 否 |
| **Oracle** | 在 test 上穷举最优 4（上界参考）| **是（泄漏，仅作上界）** |
| **Adaptive_1p3** | 先跑 `asan` → 贝叶斯预测缺陷组 → 选该组 top-3 有效资产（不含 asan）| 否（仅用 asan 观测 + train 模型）|

---

## 2. 结果（test 集覆盖率）

| 策略 | 选中资产 / 描述 | test 覆盖率 |
|---|---|---:|
| Static | 固定静态 4 | **29.05%** |
| Random_single | 单次随机（种子）| 31.87% |
| Random_mean2000 | 2000 次期望 | 43.52% |
| FD_frequency | `{asan, ubsan, tsan, cross-compile}` | 57.57% |
| **Adaptive_1p3** | asan + 3（贝叶斯预测组）| **57.75%** |
| FD_greedy | `{asan, tsan, ubsan, compiler-warn}` | **59.33%** |
| Oracle | `{asan, compiler-warn, tsan, ubsan}` | **59.33%** |

> Oracle = FD_greedy：在本 split 上贪心再次等于穷举最优（与 A2 全池结论一致），故上界 = 59.33%。

---

## 3. 关键问题：自适应是否优于非自适应 FD？

**结论：否——Adaptive（57.75%）略低于 FD_greedy（59.33%），约 −1.6pp；但远优于 Random（43.52%，+14.2pp）。**

### 为什么自适应没有赢？

1. **目标本质是全局并集覆盖**：覆盖率 $f(S)$ 是 test 全集上的并集大小。FD_greedy 已在 train 上优化此全局目标并达到最优（=Oracle）。Adaptive 把预算拆成「asan 必选 + 3 个按预测组选」，约束更强、且依赖组预测正确性，无法超越全局最优固定集。
2. **组预测信号太弱**（B1 的直接后果）：贝叶斯预测缺陷组的准确率仅 **28.35%**（11 组随机基线 ≈ 9%，即仅 3× 随机）。根因是 B1 的发现——单个资产判定对缺陷类型互信息最高仅 0.30 bits（消除 9.3% 不确定性）。信号不足 → 预测的 top-3 资产对许多样本并非其真正被 catch 的资产。
3. **asan 必选的桎梏**：Adaptive 强制第 1 槽位给 asan（33% catch），挤占了可能为特定样本更优的资产位。

---

## 4. 对 Framing 的含义（命中任务卡预期分支）

任务卡列出三分支：Adaptive>FD / ≈FD / <FD。本实验落在 **「≈FD（略低于）」** 分支：

> **Adaptive ≈ FD ⇒ 贪心已经接近最优，强化 FD 的合理性。**

这正是论文想要的——它从实验上证明「非自适应的全局贪心选择已几乎不可改进」，为 FD 作为治理框架下的**稳健默认选择**提供了额外证据，而不需要 claim「FD 比自适应更聪明」（那会是过度主张）。同时，Adaptive 显著优于 Random（+14pp）说明「按数据选择」远胜「随机/固定」，与 A3 结论呼应。

---

## 5. 局限（诚实声明）

- 轻量模拟：用 676f 矩阵代替真实 `detect()`（红线要求），未计入 ~5% 跑间不稳定（676m）。
- `asan` 作为 phase-1 资产是人为约定；换其他 phase-1 资产可能改变 Adaptive 绝对数值，但不改「Adaptive 受限于弱组信号、难超全局贪心」的结构结论。
- 贝叶斯分类器为最简实现；更复杂的自适应（如直接学习 per-sample 最优 4 子集）理论上可逼近 Oracle，但其收益受 B1 信息天花板约束，预期有限。

---

## 6. 验收对照（任务卡验收标准 6）

✅ 自适应实验：5 种策略（Static/FD/Random/Adaptive/Oracle）+ FD_frequency 桥接，全部在 clone-aware split 上、train/test 不泄漏；Adaptive 与 FD 对比结论明确（≈FD，略低），并给出信息论层面的原因（B1）。
