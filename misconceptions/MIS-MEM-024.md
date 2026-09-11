---
id: MIS-MEM-024
name: "unique_ptr 与 shared_ptr 的差别只是'独占 vs 共享'（删除器机制相同）"
level: deep
domain: MEM
trigger_patterns:
  - "两个智能指针就是独占和共享的区别，删除器用法差不多"
  - "写自定义删除器时，unique_ptr 和 shared_ptr 一样写"
refutations:
  - "语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1)`；而 `std::unique_ptr<T, D>` 合法。删除器对 unique_ptr 是**类型参数**，对 shared_ptr 只能经构造函数按值注入并被类型擦除进控制块"
  - "量化（EV-MEM-032 / EV-MEM-033，同 TU 同 -O2）：unique_ptr 的 sizeof 随删除器变化（普通空删除器 8 / 空但 final 16 / 有状态 16），shared_ptr 恒 16（三种删除器完全一样）。汇编层：删除器出现在 unique_ptr 的 mangled 类型名 `unique_ptrIi12StatelessDelE` 中（MinGW 7 次 / gcc-13、14 各 12 次），而 shared_ptr 的类名里没有删除器——删除器在控制块类型 `_Sp_counted_deleterIPi6TagDel...` 里"
  - "运行期代价可数（EV-MEM-033）：`shared_ptr<T>(new T)` 触发 **2 次堆分配**（对象 + 控制块），`make_shared<T>` 合并为 1 次，unique_ptr 对照恒为 1 次（只有对象本身）；且同一静态类型 `shared_ptr<int>` 的变量可先后持有 tag=11 / tag=22 两份不同删除器——类型系统看不见删除器"
source: G5 第三批指令（UNIQUE-002）；ATOM-MEM-UNIQUE-002 / EV-MEM-032 / EV-MEM-033
related_atoms: [ATOM-MEM-UNIQUE-002, ATOM-MEM-UNIQUE-001, ATOM-MEM-SHARED-001]
---

# MIS-MEM-024 · "unique_ptr 与 shared_ptr 只差'独占 vs 共享'"

**层级**：deep —— 结构性误解：把两者的差异压缩成"引用计数有无"一条，忽略了删除器在**类型系统**中的位置差异（类型参数 vs 类型擦除）。后果不是记错一个细节，而是解释不了两者的 sizeof、分配代价与可写语法，写代码时会撞上"`shared_ptr<T, D>` 不存在"的编译错误却不知所以然。

## 触发模式（学习者常这么说 / 这么写）
- "两个智能指针就是独占和共享的区别，删除器用法差不多"
- "写自定义删除器时，unique_ptr 和 shared_ptr 一样写"

## 为什么它不成立
1. 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1)`；而 `std::unique_ptr<T, D>` 合法。删除器对 unique_ptr 是**类型参数**，对 shared_ptr 只能经构造函数按值注入并被类型擦除进控制块
2. 量化（EV-MEM-032 / EV-MEM-033，同 TU 同 -O2）：unique_ptr 的 sizeof 随删除器变化（普通空删除器 8 / 空但 final 16 / 有状态 16），shared_ptr 恒 16（三种删除器完全一样）。汇编层：删除器出现在 unique_ptr 的 mangled 类型名 `unique_ptrIi12StatelessDelE` 中（MinGW 7 次 / gcc-13、14 各 12 次），而 shared_ptr 的类名里没有删除器——删除器在控制块类型 `_Sp_counted_deleterIPi6TagDel...` 里
3. 运行期代价可数（EV-MEM-033）：`shared_ptr<T>(new T)` 触发 **2 次堆分配**（对象 + 控制块），`make_shared<T>` 合并为 1 次，unique_ptr 对照恒为 1 次（只有对象本身）；且同一静态类型 `shared_ptr<int>` 的变量可先后持有 tag=11 / tag=22 两份不同删除器——类型系统看不见删除器

## 正确理解
- 差异有两条正交轴：**所有权模型**（独占 / 共享）× **删除器位置**（类型参数 / 类型擦除）。只记住前者会在自定义删除器、sizeof、性能分析三个场景连续踩空。
- 判据（可操作）：问"这个删除器类型能不能写进模板参数？"——能（`unique_ptr<T, D>`）就会影响对象大小与类型；不能（`shared_ptr<T>`）就必然多一次控制块堆分配，且对象大小恒定。
- 边界：unique_ptr 侧"空删除器零开销"是 **libstdc++ 的实现优化**（门槛为"空且非 final"，实测空但 `final` 的删除器 sizeof=16），不是语言保证——不要把它当成可依赖的普遍规则。

## 出处与关联
- 出处：G5 第三批指令（UNIQUE-002）；ATOM-MEM-UNIQUE-002 / EV-MEM-032 / EV-MEM-033
- 关联原子：ATOM-MEM-UNIQUE-002、ATOM-MEM-UNIQUE-001、ATOM-MEM-SHARED-001
