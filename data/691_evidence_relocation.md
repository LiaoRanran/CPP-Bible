# 691 证据搬运（B1）：机制级显著性从附录 → 正文 §5.1

- 原则：**搬运而非补做**（红线 3：不跑新 detect）。数据源 `data/677c_a5_nondegenerate_results.json`（冻结矩阵复算）

---

## 1. 证据原本在哪、长什么样

`data/677c_a5_nondegenerate_results.json` 中的 Pool A（严格池，5 个信息资产：asan / compiler-warn /
cross-compile / tsan / ubsan），FD 选择 vs 预算匹配随机单抽、同切分（派生 571 / 评估 566）、同种子：

| k | FD 选择 | FD rate | 随机单抽（seed 20260930） | 随机 rate | **Δ 单点** | McNemar p | Δ vs 2000 次均值 |
|---:|---|---:|---|---:|---:|---:|---:|
| 1 | asan | 33.0389% | tsan | 21.7314% | **+11.31pp** | **6.02×10⁻⁸** | +12.2566pp |
| 2 | asan, ubsan | 45.0530% | tsan, ubsan | 37.6325% | **+7.42pp** | 7.69×10⁻⁵ | +10.0576pp |
| 3 | asan, ubsan, tsan | 51.0601% | tsan, ubsan, cross-compile | 43.6396% | **+7.42pp** | 3.71×10⁻⁶ | +5.7794pp |
| 4 | asan, ubsan, tsan, cross-compile | 54.5936% | 同一集合 | 54.5936% | **0.00pp** | 1.0 | +1.6074pp |

（$k{=}4$ 归零的机制：Pool A 只有 5 个候选，随机抽 4 个必然覆盖 FD 的 4 个 ⇒ 结构性碰撞概率
$1/\binom{5}{4}=0.2$。）

## 2. 689 正文的实际状态（问题诊断）

689 的 Finding 1 只写：*"the mechanism-level effect survives at $+7.4$--$11.3$pp ($k\le3$) with
effective $n\approx133$--$140$"*——**没有**具体档位、**没有** p 值、**没有**说 $k{=}4$ 为何归零。
具体数字只存在于附录算子节 ⇒ 评审在正文看不到"机制确实有效"的**强度**，只看到一个区间。

## 3. 691 搬运内容（正文 §5.1，原文摘录）

> What \emph{survives} is a smaller but significant mechanism-level effect that the collapsed
> headline had hidden: on the degenerate-free pool (Pool A, five informative assets, same split,
> same seed) the executable selection beats a budget-matched random draw at $k{=}1$: **+11.31pp
> ($p{=}6.0\times10^{-8}$)**; $k{=}2$ and $k{=}3$: **+7.42pp each** ($p{=}7.7\times10^{-5}$ and
> $3.7\times10^{-6}$); and $k{=}4$: **0.00pp ($p{=}1.0$)**, where the random draw is forced onto the
> same four assets (a set collision, structural probability $1/\binom{5}{4}{=}0.2$). Against the
> 2000-draw random mean the same tiers read **+12.26, +10.06, +5.78, +1.61pp**. Effective
> $n\approx133$--$140$ … *Reading:* a seemingly very large evaluator improvement was substantially an
> artifact of measurement-pool composition, **and the residue is real but an order of magnitude
> smaller than advertised**.

**附录保留**：完整 per-tier 表（`app:operator683`）+ JSON（`data/677c_a5_nondegenerate_results.json`）。

## 4. 前后对比

| 项 | 689 | 691 |
|---|---|---|
| 正文是否给出机制级 p 值 | ❌（仅区间 +7.4–11.3pp） | ✅ k=1 +11.31pp p=6.0e-8；k=2/3 +7.42pp |
| 是否解释 k=4 归零机制 | ❌ | ✅ 集碰撞 $1/\binom54$ |
| 是否给均值口径对照 | ❌ | ✅ +12.26 / +10.06 / +5.78 / +1.61pp |
| 是否同时给出"衰减幅度"判断 | 部分（"mostly composition"） | ✅ 显式："an order of magnitude smaller than advertised" |
| 数据来源 | 同（677c 冻结产物） | 同（**无新实验**） |

**副作用**：正文增加约 1 页内的一半段落；正文由 7 页变 8 页（仍 ≤9），附录同步减法，净页数 36→35。
