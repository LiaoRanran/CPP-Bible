# 683-C1 · Operator 四分量全枚举消融（16 literal + 16 unique 配置）

- 判定矩阵：676f 冻结（1137×8）；原语：673p（未改动）；operator：677c（未改动）。
- 16 配置 = w_failure/w_novel/w_cost/w_redundancy ∈ {0,1} 全枚举（等权）。

## 关键结论（literal 模式，Pool A）

k=4（主预算）检出率排名（前 8）：

| 配置 | selection | rate% | Δ vs random(pp) | p vs random |
|---|---|---:|---:|---:|
| `xxcx` | compiler-warn,asan,ubsan,tsan | 56.0071 | 1.4134 | 0.302 |
| `xxcr` | compiler-warn,tsan,asan,ubsan | 56.0071 | 1.4134 | 0.302 |
| `xnxx` | asan,ubsan,tsan,compiler-warn | 56.0071 | 1.4134 | 0.302 |
| `xncx` | compiler-warn,asan,tsan,ubsan | 56.0071 | 1.4134 | 0.302 |
| `xncr` | compiler-warn,asan,tsan,ubsan | 56.0071 | 1.4134 | 0.302 |
| `fxxx` | asan,ubsan,tsan,compiler-warn | 56.0071 | 1.4134 | 0.302 |
| `fxcx` | compiler-warn,asan,tsan,ubsan | 56.0071 | 1.4134 | 0.302 |
| `fxcr` | compiler-warn,asan,tsan,ubsan | 56.0071 | 1.4134 | 0.302 |

## 等价性观察（跨全部池与 k）

- 块数：14
- `alloff_is_id_sorted`：14/14 块成立
- `fd_only_equals_greedy`：14/14 块成立
- `fd_only_equals_fd_topk`：9/14 块成立
- `fnxx_equals_fxxx`：14/14 块成立
- `novel_shift_equivalence`：14/14 块成立
- `u_fxxx_equals_fd`：9/14 块成立
- `unique_novel_changes_choice`：11/14 块成立

> honest note：literal 模式下 novel≡failure 是**规格的数学性质**（F_t 定义使第二条件恒真，一行证明见 677c 设计报告）；`unique` 模式是本批给出的修复变体，它让 novel 成为独立信号 —— 上表 `u_` 前缀为 unique 模式结果。
