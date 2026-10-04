# 677c · Evolution Operator 算法化设计报告

## 1. 算法定义（可执行、可比较、可证伪）

```
score(a_j | F_t, C_t) = w1*failure_coverage + w2*novel_coverage - w3*cost_norm - w4*redundancy

failure_coverage : |{s ∈ F_t : a_j catches s}| / |F_t|，F_t=派生集上 C_t 未抓到的样本

novel_coverage  : literal = |{s ∈ F_t : a_j catches s 且 C_t 无资产抓 s}| / |F_t| ≡ failure_coverage（F_t 定义使第二条件恒真；如实记录）

                  unique  = 探索性变体：|{s ∈ F_t : a_j catches s 且其他候选都抓不到 s}| / |F_t|（不可替代残余覆盖）（探索性）

cost_norm       : wall_seconds(a)/max_wall（676f 矩阵实测墙钟；全量 1137 样本口径）

redundancy      : mean_{c ∈ C_t} Jaccard(catch 集；派生集)

默认权重          : {"w_failure": 0.3, "w_novel": 0.4, "w_cost": 0.1, "w_redundancy": 0.2}（不是学习值）
a* = argmax score（同分 id 升序）；C_{t+1} = C_t ∪ {a*}；迭代至 k 个
```

## 2. novel_coverage 的数学坍缩（如实披露）

规格原文里 F_t 的定义就是「C_t 没抓到的样本」，于是 novel_coverage 的第二个条件「C_t 中没有资产抓到 s」对一切 s ∈ F_t **恒真** ⇒ literal 模式下 novel ≡ failure。这不是实现错误，是规格本身的性质；推论：**消融中 fd_novel 与 fd_only 的选择完全一致**（下方等价表逐 (pool,k) 验证）。要让 novelty 成为独立信号，需要改参考集——本批提供探索性 unique 变体（不可替代残余覆盖）作对照，不擅自替换默认定义。

## 3. 与既有方法的关系

- **fd_only(w1=1) ≡ 迭代式残余覆盖贪心**（= 任务 B 的 greedy 基线）：单步内 |F_t| 是常数，argmax failure_coverage = argmax 新增覆盖。
- **676f 的 FD（全局频率 top-k）既不是贪心也不是 E**：它是按派生集 catch 总数的一次性排序。
- E-full 在 fd_only 之上叠加 novel（≡failure，只改权重分配）、redundancy 与 cost 两个真 惩罚项 ⇒ full 与 fd_only 的选择差异只能来自 redundancy/cost。

## 4. 消融与等价验证（每池每 k）

| 池 | k | FD(676f) | greedy | evo_fd_only | evo_full | evo_full_unique | evo_full vs FD(676f) 检出率 |
|---|---|---|---|---|---|---|---|
| A | 1 | asan | asan | asan | asan | asan | 33.04 vs 33.04 (+0.00pp, p=1) |
| A | 2 | asan,ubsan | asan,ubsan | asan,ubsan | asan,compiler-warn | asan,compiler-warn | 41.34 vs 45.05 (-3.71pp, p=0.02203) |
| A | 3 | asan,ubsan,tsan | asan,ubsan,tsan | asan,ubsan,tsan | asan,compiler-warn,tsan | asan,compiler-warn,tsan | 48.06 vs 51.06 (-3.00pp, p=0.06037) |
| A | 4 | asan,ubsan,tsan,cross-compile | asan,ubsan,tsan,compiler-warn | asan,ubsan,tsan,compiler-warn | asan,compiler-warn,tsan,ubsan | asan,compiler-warn,tsan,ubsan | 56.01 vs 54.59 (+1.41pp, p=0.302) |
| B | 1 | asan | asan | asan | asan | asan | 33.04 vs 33.04 (+0.00pp, p=1) |
| B | 2 | asan,ubsan | asan,ubsan | asan,ubsan | asan,compiler-warn | asan,compiler-warn | 41.34 vs 45.05 (-3.71pp, p=0.02203) |
| B | 3 | asan,ubsan,tsan | asan,ubsan,tsan | asan,ubsan,tsan | asan,compiler-warn,tsan | asan,compiler-warn,tsan | 48.06 vs 51.06 (-3.00pp, p=0.06037) |
| B | 4 | asan,ubsan,tsan,cross-compile | asan,ubsan,tsan,compiler-warn | asan,ubsan,tsan,compiler-warn | asan,compiler-warn,tsan,ubsan | asan,compiler-warn,tsan,ubsan | 56.01 vs 54.59 (+1.41pp, p=0.302) |
| B | 5 | asan,ubsan,tsan,cross-compile,compiler-warn | asan,ubsan,tsan,compiler-warn,cross-compile | asan,ubsan,tsan,compiler-warn,cross-compile | asan,compiler-warn,tsan,ubsan,linker | asan,compiler-warn,tsan,ubsan,linker | 56.71 vs 59.36 (-2.65pp, p=0.002599) |
| C | 1 | asan | asan | asan | asan | asan | 33.04 vs 33.04 (+0.00pp, p=1) |
| C | 2 | asan,ubsan | asan,ubsan | asan,ubsan | asan,compiler-warn | asan,compiler-warn | 41.34 vs 45.05 (-3.71pp, p=0.02203) |
| C | 3 | asan,ubsan,tsan | asan,ubsan,tsan | asan,ubsan,tsan | asan,compiler-warn,tsan | asan,compiler-warn,tsan | 48.06 vs 51.06 (-3.00pp, p=0.06037) |
| C | 4 | asan,ubsan,tsan,cross-compile | asan,ubsan,tsan,compiler-warn | asan,ubsan,tsan,compiler-warn | asan,compiler-warn,tsan,ubsan | asan,compiler-warn,tsan,ubsan | 56.01 vs 54.59 (+1.41pp, p=0.302) |
| C | 5 | asan,ubsan,tsan,cross-compile,compiler-warn | asan,ubsan,tsan,compiler-warn,cross-compile | asan,ubsan,tsan,compiler-warn,cross-compile | asan,compiler-warn,tsan,ubsan,linker | asan,compiler-warn,tsan,ubsan,linker | 56.71 vs 59.36 (-2.65pp, p=0.002599) |

- full 检出率 > FD(676f) 的 (pool,k)：3/14。
- 等价性断言（JSON equivalence 字段）：fd_only≡greedy 应全真；fd_novel≡fd_only 应全真（literal 坍缩）；full 与 FD(676f) 的选择差异即 redundancy/cost 的贡献。

## 5. 诚实边界

- 权重是默认值，消融只展示敏感性，不是调参优化；cost 用全量 1137 样本墙钟归一（跨资产相对比较，不是单样本成本）；unique-novel 是探索性修复，不进默认定义。
- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage operator`；机读 `data/677c_evolution_operator_results.json`。
