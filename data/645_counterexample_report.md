# 645 反例搜索报告（B4，语义级，只搜不判）

- 卡片总数：27
- **有反例候选的卡：20**（B4 目标 ≥10）
- 反例候选总数：27

## 逐卡反例候选（语义关联，需人审判定）
### ATOM-CONC-FENCE-001
- 主题 `thread` → 标准章节 [thread.condition]/[thread.mutex] 边界=impl-defined：线程/互斥量行为部分是实现定义（内存模型保证需原子/互斥） （需人审（只搜不判））
### ATOM-CONC-LOCK-001
- 主题 `thread` → 标准章节 [thread.condition]/[thread.mutex] 边界=impl-defined：线程/互斥量行为部分是实现定义（内存模型保证需原子/互斥） （需人审（只搜不判））
### ATOM-CONC-RACE-001
- 主题 `race` → 标准章节 [intro.races]/[atomics.order] 边界=UB：数据竞争（无同步的并发读写）是 UB （需人审（只搜不判））
- 主题 `thread` → 标准章节 [thread.condition]/[thread.mutex] 边界=impl-defined：线程/互斥量行为部分是实现定义（内存模型保证需原子/互斥） （需人审（只搜不判））
### ATOM-HIST-AUTOPTR-001
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-ALIGN-001
- 主题 `aliasing` → 标准章节 [basic.lval]/[class.mem] 边界=UB：严格别名规则：通过不兼容类型访问对象是 UB （需人审（只搜不判））
### ATOM-MEM-ALLOC-001
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-MOVE-002
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-NEW-001
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-PERF-001
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-PERF-003
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-RAII-001
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-RAII-002
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
### ATOM-MEM-RVREF-001
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
### ATOM-MEM-SHARED-001
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-SHARED-002
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `thread` → 标准章节 [thread.condition]/[thread.mutex] 边界=impl-defined：线程/互斥量行为部分是实现定义（内存模型保证需原子/互斥） （需人审（只搜不判））
### ATOM-MEM-UNIQUE-001
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-UNIQUE-002
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
- 主题 `new` → 标准章节 [basic.stc.dynamic]/[expr.new] 边界=UB：new/delete 与 new[]/delete[] 混用是 UB；malloc/free 与 new/delete 混用是 UB （需人审（只搜不判））
### ATOM-MEM-VALUE-001
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
### ATOM-MEM-VALUE-002
- 主题 `move` → 标准章节 [class.copy.elision]/[lib.move] 边界=UB：move 后源对象处于有效但未指定状态，再次使用其值是 UB/未指定 （需人审（只搜不判））
### ATOM-UB-GRAY-001
- 主题 `aliasing` → 标准章节 [basic.lval]/[class.mem] 边界=UB：严格别名规则：通过不兼容类型访问对象是 UB （需人审（只搜不判））
