# 636 V26-补2 · 四态判决模拟（影子）

## 一、四态定义

| 态 | 含义 |
|---|---|
| pass | 完全通过，无例外 |
| pass_with_exception | 有例外条款但整体通过 |
| fail | 被 block/拒绝 |
| unknown | 证据不足，无法判决 |

## 二、34 份 baseline 重分类（实际 36 份）

| 文件 | 四态 |
|---|---|
| `609_baseline.md` | fail |
| `611_baseline.md` | fail |
| `612_baseline.md` | pass |
| `613_baseline_argumentation.md` | pass |
| `613_baseline_ci.md` | pass |
| `613_baseline_d5_debt.md` | pass |
| `613_baseline_learner_twin.md` | pass |
| `614_baseline.md` | fail |
| `615_baseline.md` | fail |
| `616_baseline.md` | fail |
| `617_baseline.md` | fail |
| `618_baseline.md` | pass |
| `619_baseline.md` | fail |
| `620_baseline.md` | fail |
| `621_baseline.md` | fail |
| `622_baseline.md` | fail |
| `623_baseline.md` | fail |
| `624_baseline.md` | fail |
| `625_baseline.md` | fail |
| `626_baseline.md` | fail |
| `627_baseline.md` | fail |
| `628_baseline.md` | fail |
| `629_baseline.md` | fail |
| `630_baseline.json` | fail |
| `630_baseline.md` | fail |
| `631_baseline.json` | fail |
| `631_baseline.md` | fail |
| `632_baseline.md` | fail |
| `634_baseline.md` | pass |
| `634_soft_baseline.json` | fail |
| `635_baseline.json` | pass |
| `635_baseline.md` | fail |
| `636_baseline.json` | unknown |
| `636_baseline.md` | pass_with_exception |
| `autoimmune_rate_baseline.md` | fail |
| `ev_matrix_dual_impl_baseline_616.json` | pass |

## 三、分布对比（二态 vs 四态）

| 态 | 数量 |
|---|---|
| pass | 9 |
| pass_with_exception | 1 |
| fail | 25 |
| unknown | 1 |

- 二态口径（pass/fail/unknown）：`{'pass': 10, 'fail': 25, 'unknown': 1}`

## 四、假 pass 识别

- **假 pass**（二态下算 pass、四态下应为 pass_with_exception）：**1** 份
- 占 pass-like（10）的 10.0%

## 诚实登记

1. **影子模拟**：不改任何历史判决，仅离线重分类；
2. 分类为**关键词启发式**（按文件中是否出现 失败/豁免/无数据 等词），非逐条判读；
3. 635 追加的字段小节（边界字段/两栏）**也在文件内**，可能影响关键词命中——如实说明；
4. 四态是**表示法**，是否采用交人（§八）。
