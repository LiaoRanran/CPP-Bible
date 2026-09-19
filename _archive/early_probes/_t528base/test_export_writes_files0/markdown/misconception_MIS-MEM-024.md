# MIS-MEM-024（misconception）

## 正面

【误解】MIS-MEM-024 unique_ptr 与 shared_ptr 的差别只是'独占 vs 共享'（删除器机制相同）
触发说法：两个智能指针就是独占和共享的区别，删除器用法差不多

## 背面

为什么错：语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1)`；而 `std::unique_ptr<T, D>` 合法。删除器对 unique_ptr 是**类型参数**，对 shared_ptr 只能经构造函数按值注入并被类型擦除进控制块
反例 1：量化（EV-MEM-032 / EV-MEM-033，同 TU 同 -O2）：unique_ptr 的 sizeof 随删除器变化（普通空删除器 8 / 空但 final 16 / 有状态 16），shared_ptr 恒 16（三种删除器完全一样）。汇编层：删除器出现在 unique_ptr 的 mangled 类型名 `unique_ptrIi12StatelessDelE` 中（MinGW 7 次 / gcc-13、14 各 12 次），而 shared_ptr 的类名里没有删除器——删除器在控制块类型 `_Sp_counted_deleterIPi6TagDel...` 里
反例 2：运行期代价可数（EV-MEM-033）：`shared_ptr<T>(new T)` 触发 **2 次堆分配**（对象 + 控制块），`make_shared<T>` 合并为 1 次，unique_ptr 对照恒为 1 次（只有对象本身）；且同一静态类型 `shared_ptr<int>` 的变量可先后持有 tag=11 / tag=22 两份不同删除器——类型系统看不见删除器
关联原子：ATOM-MEM-UNIQUE-002 ATOM-MEM-UNIQUE-001 ATOM-MEM-SHARED-001
