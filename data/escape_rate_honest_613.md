# 613 · 逃逸率诚实化（F1）

> 生成：`python tools/escape_rate_honest_613.py` ｜ 时间：2026-09-21T00:08:10
> 基线：`data/mutation/full_baseline_v7.json`（frozen_at_commit `d36d5c8`）
> 纪律（565）：比率一律「分子/分母 + 点估计 + **双侧** Wilson 95% CI」。

## 一、原始计数

| 项 | 值 |
|---|---|
| results（变体总数） | 1593 |
| blocked | 1405 |
| escaped | **1** |
| n_a（不适用） | 179 |
| equivalent | 8 |
| equivalent_invalid | **8** |
| out_of_scope | 69 |
| strict_blocked / strict_rate | 811 / 0.5768 |
| treated_rate | 0.9993 |

## 二、多口径逃逸率（分母摊开）

| 口径 | 分子/分母 | 点估计 | 双侧 Wilson 95% CI |
|---|---|---|---|
| ① 官方契约（可判分母） | **1/1406** | 0.071% | [0.013%, 0.402%] |
| ② +等价变异（equivalent 算未杀） | **9/1414** | 0.636% | [0.335%, 1.205%] |
| ③ +n_a（n_a 算未杀） | **180/1585** | 11.356% | [9.887%, 13.013%] |
| ④ 最保守上界（n_a+equivalent 全算未杀） | **188/1593** | 11.802% | [10.308%, 13.479%] |
| ⑤ strict 口径（1 − strict_rate） | — | 42.32% | — |

## 三、诚实披露（必读）

- 唯一 escaped 条目：[{'card': 'evidence/conc/EV-CONC-001.md', 'op': 'M1', 'point': '删 negative_controls', 'reproduce': '.venv\\Scripts\\python.exe tools/mutation_fuzz.py --cards evidence/conc/EV-CONC-001.md --operators M1 --limit 1', 'verdict': 'escaped', 'new_block': [], 'new_warn': [], 'replay': 'confirm', 'equivalent': False}]；基线 notes 记为**冻结 TCE** ⇒ 已知且冻结的例外，**不是新逃逸**，但它确实未被杀死。
- `equivalent_invalid = 8` 与 `equivalent = 8` **相等** ⇒ 全部等价判定本身无效；把它们当等价而排除**有争议**，故口径 ②④ 算回未杀。
- 官方口径（①）与最保守上界（④）相差**两个数量级** ⇒ 任何引用都必须标清分母，不得只报 1/1406。
- 基线 notes：M2 可判 141→168 系 589 T2 注释净化 un-mask 真实 fixture 路径变异，非回归；唯一 escaped=1 = M1 / EV-CONC-001 / 删 negative_controls（冻结 TCE）

> 本工具只读基线 JSON，**不跑 mutation、不改基线**（铁律：不跑全量 mutation）。
