# 611 C1 · 论证图连通分量分析（碎片化定量化）

> 纯读生成，复用 610 `argument_audit.detect_isolated_subgraphs`（BFS，忽略方向），同一真源 = 候选边 388 + 用户授权人审 388 + W2 辩护链。

## 一、总览

- 节点 **121** · 边 **388**
- 连通分量 **11** 个 · 孤立节点（仅 1 节点分量）**4** 个
- **最大分量 80 节点 = 覆盖 66.1%**（其余 {c['components'] - 1} 个分量合计仅 41 节点）

## 二、各分量大小

- 大小降序：
  - 80 节点
  - 12 节点
  - 8 节点
  - 5 节点
  - 4 节点
  - 4 节点
  - 4 节点
  - 1 节点
  - 1 节点
  - 1 节点
  - 1 节点

## 三、孤立节点（断联论证）

- 全部是**命题**（无误解指向、也无误解被它攻击）：
  - `ATOM-CONC-FENCE-001::prop-1`
  - `ATOM-CONC-FENCE-001::prop-2`
  - `ATOM-CONC-LOCK-001::prop-1`
  - `ATOM-CONC-LOCK-001::prop-2`

## 四、最大分量构成

- 节点数 80：其中proposition 57 · misconception 23
- 含（节选）：`ATOM-MEM-ALLOC-001::prop-1`、`ATOM-MEM-ALLOC-001::prop-2`、`ATOM-MEM-ALLOC-001::prop-3`、`ATOM-MEM-ALLOC-001::prop-4`、`ATOM-MEM-ALLOC-002::prop-1`、`ATOM-MEM-ALLOC-002::prop-2`、`ATOM-MEM-ALLOC-002::prop-3`、`ATOM-MEM-LEAK-001::prop-1`、`ATOM-MEM-LEAK-001::prop-2`、`ATOM-MEM-LEAK-001::prop-3`、`ATOM-MEM-LEAK-002::prop-1`、`ATOM-MEM-LEAK-002::prop-2`

## 五、结论（碎片化）

- 论证图被切成 **11 块**，最大块只覆盖 66.1%**——说明本仓的论证是**一堆互不相连的孤岛**，跨主题的辩护链在结构上无法成立；
- 这与 610 C 线 `argument_audit` 的 P1「论证图碎片化」结论一致，**数字同源**；
- 是否要补「桥接攻击边」把孤岛连起来，是 C2/C3 的议题；本工具只定量、不擅自连。

> 数字可由 `tools/argument_graph_analysis.py --stats` 复算；`--check` 锁定上表事实。

