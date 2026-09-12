# 资料研究第十一轮：STL 域第二批源码——红黑树 / optional / function / pmr / variant

> 2026-09-11，底层工程资料研究员。主题：STL 第二批源码实现（std::map 红黑树 / optional / function 类型擦除 / pmr 内存资源 / variant）。
> 检索方式：general_search + GitHub 源码（gcc-mirror/gcc）+ CppCon 演讲 + eel.is 标准草案。

---

## 一、核心资料（S/A+ 级）

### 1. std::map / set：红黑树（_Rb_tree）

- **类型**：标准库容器源码
- **来源**：libstdc++ `bits/stl_tree.h`
- **核心结构**：
  ```cpp
  enum _Rb_tree_color { _S_red = false, _S_black = true };
  struct _Rb_tree_node_base {
      _Rb_tree_color  _M_color;
      _Rb_tree_node_base* _M_parent;
      _Rb_tree_node_base* _M_left;
      _Rb_tree_node_base* _M_right;
  };
  ```
  派生节点 `_Rb_tree_node<_Tp>` 额外存值。map 和 set 复用同一棵 `_Rb_tree`。
- **插入修复**：最多 2 次旋转 + 向上回溯的重染色（Case 1: 叔叔红 → 重染色上溯；Case 2/3: 叔叔黑 → 旋转后结束）
- **删除修复**：最多 3 次旋转
- **关键特性**：删除时节点被 **relinked（重新链接）而非 copied**——只有指向被删节点的迭代器失效，其他迭代器不受影响
- **红黑树 vs AVL 树**：
  - 红黑树放松平衡条件：最长路径 ≤ 2× 最短路径（不是严格平衡）
  - 插入/删除旋转更少（红黑树插入最多 2 次、删除最多 3 次；AVL 删除可能 O(log n) 次）
  - 适合频繁修改的场景（标准库选择）
  - AVL 更平衡，查找略快，但修改代价高
- **与 CPP-Bible 的关系**：STL 域"map/set"原子；ALGO 域"自平衡 BST 对比"；CASE 域"为什么标准库选红黑树不选 AVL"
- **可以设计什么实验**：红黑树 vs AVL 在插入密集/查找密集/混合负载下的性能对比
- **可信度**：S（libstdc++ 源码可直接读）
- **教材价值**：S

### 2. std::optional：零堆分配的判别联合

- **类型**：标准库工具类源码
- **来源**：libstdc++ `std/optional` + N3672 提案
- **核心实现**：
  ```cpp
  struct _Empty_byte { };
  union {
      _Empty_byte  _M_empty;    // 空状态的 dummy 成员
      _Stored_type _M_payload;  // 值状态
  };
  bool _M_engaged = false;
  ```
- **关键约束**：**标准明确禁止动态分配**——"Implementations are not permitted to use additional storage, such as dynamic memory, to allocate its contained value"
- **空状态的巧妙处理**：
  - union 必须始终有一个活跃成员
  - engaged 时活跃成员是 `_M_payload`
  - disengage 时析构 `_M_payload`，然后激活 `_M_empty`（一个字节的 dummy）
  - 2026 年 4 月还有 bug 修复（PR124910）：disengage 后 union 没有活跃成员，需要 `std::construct_at` 激活 `_M_empty`
- **trivial 特化**：T 是 trivially destructible 时，optional 也提供 trivial 析构（满足 triviality 传播要求）
- **与 CPP-Bible 的关系**：STL 域"optional"原子；LANG 域"union 的活跃成员规则"；MEM 域"零分配的栈上可选值"
- **可以设计什么实验**：sizeof(optional<T>) 实测 + optional 空状态的汇编（确认无堆分配）
- **可信度**：S（libstdc++ 源码 + 标准草案 + 真实 bug 修复记录）
- **教材价值**：A+

### 3. std::function：类型擦除 + 小对象优化

- **类型**：标准库工具类源码
- **来源**：libstdc++ `bits/std_function.h`
- **核心机制——类型擦除（Concept-Model）**：
  ```
  std::function 内部持有一个 vtable 指针
  vtable 包含：_M_clone / _M_destroy / _M_invoke（调用）
  每次 operator() 都走间接分发（无法内联）
  ```
- **小对象优化（SBO/SOO）**：
  - `_M_max_size = sizeof(_Nocopy_types)`（约 3 个指针大小，即 16-24 字节）
  - `__stored_locally` 编译期判断：callable ≤ _M_max_size 且对齐满足 → 存在内部缓冲区（零堆分配）
  - 大 callable → 堆分配，只存指针
- **代价**：
  - 每次调用一次虚调用（间接分发）
  - 大 callable 有堆分配
  - 要求 callable **可拷贝**（move-only lambda 存不了，如捕获 unique_ptr）
- **与 CPP-Bible 的关系**：TMPL 域"类型擦除"原子；PERF 域"std::function 开销实测"；PAT 域"Concept-Model 设计模式"
- **可以设计什么实验**：std::function vs 直接 lambda vs 函数指针的调用开销对比 + SBO 阈值实测
- **可信度**：S（libstdc++ 源码）
- **教材价值**：S

### 4. std::pmr：多态内存资源（分配策略与容器类型分离）

- **类型**：标准库内存管理（C++17）
- **来源**：N3816 提案 + Pablo Halpern CppCon 2017 "Allocators: The Good Parts" + libstdc++ `std/memory_resource`
- **核心抽象**：
  ```cpp
  class memory_resource {
      virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
      virtual void  do_deallocate(void* p, size_t bytes, size_t alignment) = 0;
      virtual bool  do_is_equal(const memory_resource& other) const = 0;
  };
  ```
  `polymorphic_allocator<T>` 是 `memory_resource*` 的包装器，给它 C++11 allocator 接口。
- **关键创新**：**分离分配策略与容器类型**——两个 `vector<int, pmr::polymorphic_allocator<int>>` 类型相同，但可以用不同的分配器（传统 allocator 是模板参数，不同分配器 = 不同类型）
- **三种内置资源**：

| 资源 | 机制 | 线程安全 | 适用场景 |
|---|---|---|---|
| `monotonic_buffer_resource` | bump allocator（指针前移），只进不出，析构一次性释放 | 不安全 | 临时 arena、极快分配 |
| `unsynchronized_pool_resource` | 池分配（按大小分桶），减少碎片 | 不安全 | 单线程大量小分配 |
| `synchronized_pool_resource` | 池分配 + 内部锁 | 安全 | 多线程共享 |

- **`null_memory_resource()`**：任何分配都抛 `bad_alloc`，用于测试"确保不分配"
- **与 CPP-Bible 的关系**：MEM 域"allocator 体系"原子；PERF 域"monotonic_buffer 性能实测"；ENG 域"分配策略与类型分离的设计"
- **可以设计什么实验**：pmr::monotonic_buffer vs 默认分配器在大量小对象场景的性能对比
- **可信度**：S（标准提案 + CppCon 经典演讲 + libstdc++ 源码）
- **教材价值**：S

### 5. std::variant：判别联合 + visit 调度

- **类型**：标准库工具类源码（C++17）
- **来源**：libstdc++ `std/variant` + GCC 12 switch 优化分析
- **核心结构**：`index`（当前活跃类型索引）+ `union` storage（大小 = max(alternatives)）
- **零堆分配**，大小 = max(sizeof(T_i)) + sizeof(index) + 对齐填充
- **std::visit 实现**：
  - 编译期：展开 `Types...` 为「类型-索引」映射表，生成 visitor 对每个类型的调用代码
  - 运行期：根据 `variant.index()` 跳转到对应分支
  - **GCC 12 优化**：单 variant 且 ≤11 个候选时用 **switch 快速路径**——直接生成 switch(index)，visitor 体内联到每个 case，而非函数指针表间接调用
  - 多 variant visit 是多维跳转表
- **比虚函数快的原因**：跳转表局部紧凑、visitor 体内联、分支预测友好（虚函数的 vtable 调用是间接跳转，分支预测器容易猜错）
- **C++20 后 constexpr**（P2231R1）
- **与 CPP-Bible 的关系**：TMPL 域"variant 与类型安全联合"原子；LANG 域"union 的安全替代"；PERF 域"visit vs 虚函数调度对比"
- **可以设计什么实验**：std::visit vs virtual 调用的性能对比 + GCC 12 switch 优化验证
- **可信度**：S（libstdc++ 源码 + GCC 优化分析）
- **教材价值**：A+

---

## 二、STL 类型擦除与内存管理全景

```
类型擦除谱系
├── std::function：Concept-Model + vtable + SBO
│   ├── 小 callable 内联（≤3 指针）
│   ├── 大 callable 堆分配
│   └── 要求可拷贝
├── std::any：Concept-Model + SBO（类似 function，但无调用接口）
├── std::shared_ptr：控制块类型擦除（deleter/allocator 擦除）
└── std::variant：不是类型擦除，是判别联合（编译期已知类型集合）

内存管理谱系
├── std::allocator<T>：模板参数，不同分配器=不同类型
├── std::pmr::polymorphic_allocator<T>：运行期多态，同类型可换分配器
│   ├── monotonic_buffer_resource（bump，最快）
│   ├── unsynchronized_pool_resource（池，单线程）
│   └── synchronized_pool_resource（池+锁，多线程）
└── 自定义 allocator：allocate/deallocate/construct/destroy 分离
```

---

## 三、知识网络

```
STL 第二批
├── 关联容器
│   └── map/set = _Rb_tree 红黑树
│       ├── 插入最多 2 旋转 / 删除最多 3 旋转
│       ├── 删除 relinked 不 copied（迭代器失效规则）
│       └── 红黑 vs AVL：修改友好 vs 查找友好
│
├── 工具类
│   ├── optional = union + bool（零堆分配）
│   │   ├── _M_empty dummy 成员保证 union 活跃
│   │   └── trivial 特化传播
│   ├── variant = index + union（判别联合）
│   │   ├── visit：switch 快速路径（≤11 候选）
│   │   └── 比虚函数快（内联 + 紧凑跳转表）
│   └── function = 类型擦除 + SBO
│       ├── vtable 间接调用（无法内联）
│       ├── 小对象内联 / 大对象堆分配
│       └── 要求可拷贝
│
└── 内存管理
    ├── std::allocator（模板参数，类型绑定）
    └── std::pmr（运行期多态，类型分离）
        ├── monotonic_buffer（bump，只进不出）
        ├── pool（按大小分桶，减少碎片）
        └── null_memory（测试用，抛 bad_alloc）
```

---

## 四、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | libstdc++ _Rb_tree 红黑树源码 | S | map/set 共用实现 + 旋转修复 |
| 2 | std::optional union + _M_empty 实现 | S | 零堆分配 + union 活跃成员规则 |
| 3 | std::function 类型擦除 + SBO | S | Concept-Model + 小对象内联阈值 |
| 4 | std::pmr memory_resource 体系 | S | 分配策略与类型分离 + 三种资源 |
| 5 | std::variant visit switch 优化 | A+ | GCC 12 ≤11 候选内联快速路径 |
| 6 | Pablo Halpern CppCon 2017 "Allocators: The Good Parts" | S | pmr 设计动机与最佳实践 |
| 7 | N3816 Polymorphic Memory Resources 提案 | A+ | pmr 原始设计文档 |
| 8 | N3672 optional 提案 | A | optional 原始设计与 nullopt 模型 |
| 9 | optional PR124910 bug 修复 | A | union 活跃成员的真实工程细节 |
| 10 | 红黑树 vs AVL 对比 | A | 标准库选择红黑树的工程理由 |

## 五、强烈建议深入研究的 5 个资料

1. **libstdc++ `bits/stl_tree.h`**——读红黑树插入/删除修复的完整实现
2. **Pablo Halpern CppCon 2017 演讲 PDF**——理解 pmr 的设计动机和三种资源的适用场景
3. **libstdc++ `bits/std_function.h`**——读类型擦除的 Concept-Model 实现和 SBO 判断
4. **libstdc++ `std/variant` 的 `__do_visit`**——理解 switch 快速路径和函数指针表的选择
5. **N3816 pmr 提案**——理解"分配策略与类型分离"为什么是重要创新

## 六、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| 红黑树实现 | "map/set 为什么用红黑树" | STL/ALGO 交叉 |
| optional union 实现 | "零堆分配的可选值" | STL/LANG 交叉 |
| function 类型擦除 | "Concept-Model 模式与 SBO" | TMPL/PAT 交叉 |
| pmr 三种资源 | "分配策略与类型分离" | MEM/ENG 交叉 |
| variant visit | "判别联合与 switch 调度" | TMPL/PERF 交叉 |

## 七、对 CPP-Bible 的工程升级建议

1. **TMPL 域新增"类型擦除"专题**——std::function / std::any / shared_ptr 控制块 / 自定义 type-erasure，这是现代 C++ 核心设计模式
2. **MEM 域新增"pmr 分配器"原子**——monotonic_buffer 是性能优化利器，现有教材普遍不讲
3. **"union 活跃成员"作为核心概念**——optional/variant 的实现基础，也是 C++ 生命周期规则的难点
4. **std::function 开销必须实测**——虚调用 + 堆分配的代价，以及 SBO 阈值
5. **variant vs 继承多态对比**——visit（内联+紧凑）vs virtual（间接+预测失败）的性能差异

## 八、发现的知识空白

1. **类型擦除完全空白**——std::function/any 的实现原理无内容
2. **pmr 分配器完全空白**——C++17 重要特性，性能优化利器
3. **红黑树实现细节无源码级讲解**——只讲性质不讲实现
4. **optional/variant 的 union 实现无讲解**——零堆分配的工程细节
5. **visit vs virtual 性能对比无内容**——现代 C++ 偏好 variant 的核心理由

## 九、下一轮推荐搜索方向

1. **STL 域第三批**——std::list、std::priority_queue/heap、std::tuple 实现、std::span、std::expected（C++23）
2. **C++23/26 新特性**——expected / mdspan / print / reflection / contracts
3. **编译器优化与 UB**——GCC/LLVM 怎么利用 UB 优化，-O2 吃掉实验的原理
4. **abseil / folly 容器对比**——flat_hash_map、fbvector、F14Map 等工业级替代
5. **CMake 构建系统**——大型 C++ 项目的构建配置（换域到工程工具链）

---

*本轮新增知识节点：_Rb_tree、红黑树旋转修复、relinked vs copied、optional union 活跃成员、_M_empty dummy、类型擦除、Concept-Model、SBO/SOO、pmr、memory_resource、monotonic_buffer、pool_resource、variant discriminant union、visit switch 快速路径。补齐了 STL 域"工具类实现 + 内存管理 + 类型擦除"三大空白。STL 域两轮覆盖：核心容器算法（第十轮）+ 工具类与内存管理（第十一轮）。*
