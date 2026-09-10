# ADR-0003：知识域 ≠ 出版 part（3 处重归类）

- 状态：**已接受**（2026-09-10，G1）
- 决策人：架构师提议，随 G1 交付报人确认

## 背景

`Book/` 的 16 个 `part*` 是**出版顺序**：先历史、再工具链、再语言……但原子化需要的是**知识结构**。二者不重合，若直接拿 part 当域，会导致：
- G4 样板 A（移动语义）落在 part10(MOD)，而它依赖的值类别/生命周期知识在 part03/part04 → 学习路径跨三个"域"，DAG 表达别扭；
- 样板 B（灰色地带）所需内容散在 part03(ch28)、part04(ch42)、part09(ch108/109) → 没有一个域能承载。

## 决策（3 处重归类）

1. `ch115_move` / `ch116_perfect_forwarding` / `ch117_copy_elision`：part10(MOD) → **MEM**。
   理由：值语义三兄弟的知识依赖是"对象生命周期 + 值类别"，属对象模型；归"现代特性"是按**发布时间**而非**知识结构**分类，会污染 DAG。
2. `ch28_lifetime_ub` / `ch30_volatile` / `ch42_strict_aliasing`：part03/part04 → **UB** 横切域。
   理由：UB 是横切关注点（cross-cutting），其判据是"是否 pending 标准判定"，与它在书里哪一 part 无关。样板 B 需要一个域来承载。
3. `ch93_thread_async` / `ch94_stop_token`：part07(STL) → **CONC**。
   理由：目录位置是历史原因（STL 大 part 内），主题属并发。

## 候选与否决

**候选：直接用 16 个 part 当域。**
否决：part 是出版视图，其划分依据包含"篇幅均衡""读者阅读顺序"等非知识因素；用它当域会让学习路径 DAG 出现大量跨域依赖，且样板 A/B/C 无法落地到单一域。

**候选：完全重划（不参考 part）。**
否决：与存量 147 章脱节，G5 迁移时无法做章→域的机械映射，代价过大。

## 后果

- 正面：样板 A/B/C 各落单一域（MEM / UB / MEM+HIST），DAG 可表达；域统计可算（见 `tools/atom_coverage_map.py`）。
- 负面：13 章的"目录位置 ≠ 域"，需在地图里标 `[P]`（已标），否则后续执行 Agent 会按目录机械归类。
- 约束：`tools/atom_coverage_map.py` 的 `DOMAIN_OF_PREFIX` 是**唯一权威映射**；改映射必须同步 `docs/kernel/G1_knowledge_map.md`，并由 `--check` 保证覆盖率 100%。
- 待确认：PERF 域 VERIFIED=0 / UNVERIFIED=31，是我据"最薄弱优先"额外提的 P0（样板未点名），请人确认是否接受。
