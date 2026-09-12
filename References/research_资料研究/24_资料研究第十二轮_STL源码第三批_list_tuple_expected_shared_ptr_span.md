# 资料研究第十二轮：STL 域第三批源码——list / tuple / expected / shared_ptr / span

> 2026-09-11，底层工程资料研究员。主题：STL 第三批源码实现（std::list / tuple / expected / shared_ptr 控制块 / span）。
> 检索方式：general_search + GitHub 源码（gcc-mirror/gcc）+ 标准提案（P0122/P0323/P2505）。

---

## 一、核心资料（S/A+ 级）

### 1. std::list：双向链表 + 哨兵节点 + splice O(1)

- **类型**：标准库容器源码
- **来源**：libstdc++ `bits/stl_list.h` + `bits/list.tcc`
- **核心结构**：
  - 每个元素单独堆分配节点：`prev` 指针 + `next` 指针 + 值
  - **哨兵节点（sentinel）**：`end()` 指向哨兵，不是空指针——哨兵的 next 指向首元素、prev 指向尾元素，形成环形
  - list 对象只存哨兵节点（不需要单独的 head/tail 指针）
- **splice 操作 O(1)**：只改指针（把一段节点从一个链表摘下来接到另一个），不移动/复制元素
- **迭代器失效规则**：
  - 插入和 splice **不使任何迭代器失效**
  - 只有 erase 被删元素的迭代器失效
  - LWG 250：splice 后源列表的迭代器"迁移"到目标列表（不是失效，是归属变更）
- **局限**：无随机访问（operator[]），查找 O(n)，双向迭代器（不是随机访问），cache 极差（节点分散在堆上）
- **与 CPP-Bible 的关系**：STL 域"list"原子；"迭代器失效规则"对比表；PERF 域"list vs vector 性能陷阱"
- **可以设计什么实验**：list splice O(1) vs vector 插入 O(n) 的实测对比 + 迭代器失效验证
- **可信度**：S（libstdc++ 源码）
- **教材价值**：A+

### 2. std::tuple：递归继承 + 空基类优化（EBCO）

- **类型**：标准库工具类源码
- **来源**：libstdc++ `include/tuple`
- **核心实现**：
  ```
  tuple<int, Empty, double>
    └── _Tuple_impl<0, int, Empty, double>  ← 存 int（最派生）
        └── _Tuple_impl<1, Empty, double>   ← 存 Empty（作为基类，EBCO 大小 0）
            └── _Tuple_impl<2, double>      ← 存 double
                └── _Tuple_impl<3>          ← 空基类
  ```
  递归继承层次，每个层级存一个元素，`Idx` 参数实现 O(1) `get<I>()`。
- **空基类优化（EBCO）**：空类型作为基类时大小为 0——`tuple<int, Empty, double>` 的大小 = sizeof(int) + sizeof(double)，Empty 不占空间
- **`make_tuple`**：用 `__decay_and_strip` 处理参数，`std::ref`/`std::cref` 自动转为引用
- **结构化绑定**：通过 `tuple_size` / `tuple_element` / `get<I>` 接口实现——任何提供这三个的类型都支持结构化绑定（C++23 tuple-like 接口）
- **2021 年优化**：`tuple_element` 从递归特化改为一次性计算（减少编译期递归深度）
- **与 CPP-Bible 的关系**：TMPL 域"tuple 与变参模板"原子；LANG 域"EBCO 与 [[no_unique_address]]"；PAT 域"递归继承设计模式"
- **可以设计什么实验**：sizeof(tuple<int, Empty, double>) 实测验证 EBCO + 手写最小 tuple
- **可信度**：S（libstdc++ 源码 + 标准提案）
- **教材价值**：S

### 3. std::expected（C++23）：值或错误的判别联合 + monadic 操作

- **类型**：标准库工具类（C++23）
- **来源**：P0323R11 提案 + P2505R1 monadic 操作 + libstdc++ `std/expected`
- **核心结构**：判别联合——`T`（值）或 `unexpected<E>`（错误），零堆分配
- **monadic 操作（链式错误处理）**：

| 操作 | 输入 | 行为 |
|---|---|---|
| `and_then(f)` | f: T → expected<U,E> | 有值则调用 f（返回 expected），错误则短路 |
| `transform(f)` | f: T → U | 有值则 f 转换值，错误则短路 |
| `or_else(f)` | f: E → expected<T,E> | 有错误则调用 f，有值则短路 |
| `transform_error(f)` | f: E → F | 有错误则 f 转换错误，有值则短路 |

- **实现细节**：`and_then` 用 `static_assert` 检查 f 返回类型必须是 expected 且 error_type 相同
- **设计哲学**："错误作为值"——不展开栈、性能可预测、错误类型在签名中可见
- **`unexpected` 名称趣闻**：C++11 的 `std::unexpected`（异常规范违例回调）被 deprecated，C++17 移除——P0323 复用了这个"僵尸名称"
- **与 CPP-Bible 的关系**：LANG 域"错误处理谱系"（异常 vs error_code vs expected）；PAT 域"monadic 链式设计"
- **可以设计什么实验**：expected 链式调用 vs 异常 vs error_code 的性能对比 + 可读性对比
- **可信度**：S（标准提案 + libstdc++ 源码）
- **教材价值**：S

### 4. std::shared_ptr 控制块：类型擦除 + 双引用计数

- **类型**：标准库智能指针源码
- **来源**：libstdc++ `bits/shared_ptr_base.h` + `bits/shared_ptr.h`
- **核心结构**：
  ```
  shared_ptr<T>
  ├── T* _M_ptr              ← 指向对象
  └── __shared_count _M_refcount
      └── _Sp_counted_base*   ← 指向控制块
          ├── strong count    ← shared_ptr 数量（原子）
          ├── weak count      ← weak_ptr 数量（原子）
          ├── deleter         ← 类型擦除（不在 shared_ptr 签名中）
          └── allocator       ← 类型擦除
  ```
- **类型擦除**：deleter 和 allocator 的类型不在 `shared_ptr<T>` 签名中——`shared_ptr<int>` 可以用任何 deleter 构造，类型不变
- **生命周期**：
  - strong count → 0：析构对象（调用 deleter）
  - weak count → 0：释放控制块
  - 两者独立——对象析构后控制块可能还在（有 weak_ptr 时）
- **`make_shared` 优化**：对象和控制块**一次分配**（连续内存）——省一次分配、cache 友好；但代价是 weak_count 到 0 才释放整个块（对象已析构但内存不释放）
- **线程安全**：引用计数增减是原子操作（`_Sp_counted_base<__gnu_cxx::_S_atomic>`）
- **与 CPP-Bible 的关系**：MEM 域"shared_ptr 控制块"原子；TMPL 域"类型擦除"（与 function 呼应）；PERF 域"make_shared 单次分配优化"
- **可以设计什么实验**：shared_ptr vs make_shared 的分配次数对比 + weak_ptr 锁存后控制块生命周期验证
- **可信度**：S（libstdc++ 源码）
- **教材价值**：S

### 5. std::span（C++20）：非拥有视图

- **类型**：标准库视图类（C++20）
- **来源**：P0122R6 提案 + libstdc++ `std/span`
- **核心结构**：`T* _M_ptr` + `size_t _M_extent`（动态）或仅 `T*`（静态）
- **静态 vs 动态**：
  - `span<T, N>`：编译期固定大小，只存指针（sizeof = 指针大小）
  - `span<T>` = `span<T, dynamic_extent>`：运行期大小，存指针+长度
- **非拥有**：不分配、不释放、不管理生命周期——只是"观察"连续内存
- **边界安全设计**：
  - `operator[]` **不做运行时边界检查**（和 vector 一样），越界是 UB
  - 提案原文："conceptually range-checked... failure is undefined behavior, effectively fatal"
  - 静态 span 的 `first<N>()` 用 `static_assert` 编译期检查
  - 动态 span 的 `first(n)` 用 `__glibcxx_assert`（debug 模式检查）
- **LLVM SafeBuffers**：用 span 改进边界安全——视图类型让边界信息显式传递，比裸指针好
- **与 CPP-Bible 的关系**：STL 域"span/string_view 视图"原子；LANG 域"非拥有语义"；SEC 域"边界安全改进"
- **可以设计什么实验**：sizeof(span<T,N>) vs sizeof(span<T>) 实测 + span 越界 UB 演示
- **可信度**：S（标准提案 + libstdc++ 源码）
- **教材价值**：A+

---

## 二、STL 三批源码总览

```
STL 源码三批
├── 第一批（第十轮）：核心容器与算法
│   ├── std::sort = introsort（快排+堆排+插入排序）
│   ├── vector = 连续数组 + 2x/1.5x 扩容
│   ├── unordered_map = 开链法哈希表（引用稳定性）
│   ├── string = SSO + 堆（15B/22B/15B）
│   └── deque = 分段数组（512B/块）
│
├── 第二批（第十一轮）：工具类与内存管理
│   ├── map/set = 红黑树（_Rb_tree）
│   ├── optional = union + bool（零堆分配）
│   ├── function = 类型擦除 + SBO
│   ├── pmr = 多态内存资源（分配策略与类型分离）
│   └── variant = 判别联合 + visit switch 优化
│
└── 第三批（第十二轮）：链表 / 异构容器 / 错误处理 / 智能指针 / 视图
    ├── list = 双向链表 + 哨兵节点 + splice O(1)
    ├── tuple = 递归继承 + EBCO
    ├── expected = 判别联合 + monadic 操作（C++23）
    ├── shared_ptr = 控制块 + 类型擦除 + 双计数
    └── span = 非拥有视图（指针+长度）
```

---

## 三、知识网络

```
STL 第三批
├── 节点式容器
│   ├── list：双向链表 + 哨兵 + splice O(1)
│   │   └── 迭代器失效：插入/splice 不失效，erase 仅被删失效
│   └── map/set：红黑树（第二批）
│       └── 删除 relinked 不 copied
│
├── 异构容器
│   ├── tuple：递归继承 + EBCO
│   │   ├── get<I>() O(1)（Idx 参数）
│   │   └── 结构化绑定 = tuple_size/tuple_element/get
│   └── variant：判别联合（第二批）
│       └── visit switch 快速路径
│
├── 错误处理
│   ├── expected（C++23）：值或错误 + monadic 链式
│   │   ├── and_then / transform / or_else / transform_error
│   │   └── 错误作为值，不展开栈
│   └── optional：值或空（第二批）
│
├── 智能指针
│   ├── shared_ptr：控制块 + 类型擦除 + 双计数
│   │   ├── strong count → 0 析构对象
│   │   ├── weak count → 0 释放控制块
│   │   └── make_shared 单次分配优化
│   └── unique_ptr：零开销（第一批相关）
│
└── 视图
    ├── span（C++20）：非拥有，指针+长度
    │   ├── 静态 extent 只存指针
    │   └── operator[] 不检查（UB）
    └── string_view：类似，只读字符视图
```

---

## 四、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | libstdc++ list 哨兵节点 + splice 源码 | S | O(1) 接合 + 迭代器失效规则 |
| 2 | tuple 递归继承 + EBCO 实现 | S | 变参模板经典实现 + 空基类优化 |
| 3 | std::expected monadic 操作（P2505） | S | 错误作为值 + 链式处理 |
| 4 | shared_ptr 控制块类型擦除 | S | deleter/allocator 不在签名中 + 双计数 |
| 5 | std::span 非拥有视图（P0122） | A+ | 指针+长度 + 边界安全设计 |
| 6 | P0323R11 expected 提案 | A+ | 原始设计 + unexpected 僵尸名称 |
| 7 | make_shared 单次分配优化 | A | 连续内存 + weak_count 延迟释放代价 |
| 8 | tuple 结构化绑定接口 | A | tuple-like 协议的通用性 |
| 9 | LWG 250 splice 迭代器迁移 | A | 迭代器失效规则的微妙细节 |
| 10 | LLVM SafeBuffers span 边界安全 | A | 视图类型改进内存安全的工业实践 |

## 五、强烈建议深入研究的 5 个资料

1. **libstdc++ `bits/stl_list.h` 的 `_M_transfer`**——读 splice 的指针操作实现
2. **libstdc++ `include/tuple` 的 `_Tuple_impl`**——读递归继承和 EBCO 的完整实现
3. **P0323R11 expected 提案**——理解 expected 的设计动机和 monadic 操作
4. **libstdc++ `bits/shared_ptr_base.h` 的 `_Sp_counted_base`**——读控制块和引用计数的原子操作
5. **P0122R6 span 提案**——理解"conceptually range-checked"的设计哲学

## 六、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| list splice + 迭代器失效 | "为什么 list 的 splice 是 O(1)" | STL 域原子 |
| tuple 递归继承 + EBCO | "变参模板的经典实现" | TMPL 域原子 |
| expected monadic 操作 | "错误处理的第三种选择" | LANG 域原子 |
| shared_ptr 控制块 | "类型擦除的另一个范例" | MEM/TMPL 交叉 |
| span 非拥有视图 | "指针+长度的安全抽象" | STL/SEC 交叉 |

## 七、对 CPP-Bible 的工程升级建议

1. **STL 域新增"迭代器失效规则"专题**——vector/deque/list/map/unordered_map 的失效规则对比表，这是最容易出错的知识点
2. **LANG 域新增"错误处理谱系"**——异常 vs error_code vs expected（C++23），含性能和可读性对比
3. **TMPL 域"EBCO 与 [[no_unique_address]]"**——tuple 的实现是 EBCO 的最佳教学案例
4. **MEM 域"shared_ptr 控制块"独立原子**——类型擦除 + 双计数 + make_shared 优化，与 function 的类型擦除呼应
5. **"非拥有语义"作为核心概念**——span/string_view/weak_ptr 都是非拥有，统一讲解

## 八、发现的知识空白

1. **std::list 实现细节空白**——splice O(1) 和哨兵节点无讲解
2. **tuple 递归继承实现空白**——EBCO 无源码级讲解
3. **std::expected 完全空白**——C++23 重要特性，错误处理新范式
4. **shared_ptr 控制块类型擦除空白**——deleter 不在签名中的原理
5. **span 边界安全设计空白**——"conceptually range-checked"的设计哲学

## 九、下一轮推荐搜索方向

> STL 域三轮覆盖核心容器/算法/工具类/内存管理/视图，**STL 域基本饱和。下一轮建议换域。**

1. **编译器优化与 UB（强烈推荐换域）**——GCC/LLVM 怎么利用 UB 优化、-O2 吃掉实验的原理、strict aliasing、常量折叠、死代码消除
2. **C++26 新特性**——reflection、contracts、flat_map/flat_set、hazard_pointer/RCU
3. **CMake 构建系统**——大型 C++ 项目的构建配置（换域到工程工具链）
4. **abseil / folly 容器对比**——flat_hash_map、fbvector、F14Map 工业级替代
5. **数据库存储引擎**——B+ 树、LSM 树、缓冲池（换域到系统软件）

---

*本轮新增知识节点：哨兵节点、splice O(1)、LWG 250 迭代器迁移、递归继承、EBCO、tuple-like 接口、expected、monadic 操作、and_then/transform/or_else、unexpected 僵尸名称、控制块、strong/weak count、make_shared 单次分配、span、非拥有视图、dynamic_extent。补齐了 STL 域"链表/异构容器/错误处理/智能指针/视图"五大空白。STL 域三轮正式饱和：核心容器算法（第十轮）+ 工具类与内存管理（第十一轮）+ 链表/异构/错误/智能指针/视图（第十二轮）。*
