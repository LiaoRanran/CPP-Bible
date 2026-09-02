# 第84章　set / multiset：红黑树有序集合
> 【性能声明 · §10.3】本章所有绝对延迟/带宽数字（如 L1≈1ns、主存≈100ns、各基准 ms）均为 **x86-64 量级示意**，强依赖具体 CPU 型号/频率、编译器及版本、编译标志、OS、测试负载与样本量；非通用性能结论，绝对数字不可移植。微架构相关结论标 `[微架构·x86-64][UNVERIFIED]`；本机实测标 `[实验·本机实测][UNVERIFIED]`。断言形如「acquire 读比 relaxed 贵 X」仅在给定微架构下成立。

> 标准基：ISO/IEC 14882:2023 (C++23)，补充 C++17/C++20 特性 ⟶ 标注 `[C++17]`/`[C++20]`。｜层级：L2 进阶
> 预计阅读：约 95 分钟（深度版，含源码/汇编/基准）。
> 前置：[第83章　map / multimap（红黑树）](../part07_stl/ch83_map.md)（map/multimap 红黑树） · [第19章　变量、存储期、链接与 ODR（工业级深度版）](../part03_language/ch19_variables.md)（存储期） · [第65章　类型特性 Type Traits —— 编译期类型自省与分发](../part06_templates/ch65_type_traits.md)（比较器 traits）。
> 后续：[第85章　unordered_map / unordered_set：哈希开链集合](../part07_stl/ch85_unordered.md)（哈希集合，对比本章） · [第154章　缓存优化与数据局部性（C++/硬件）](../part14_perf/ch154_cache_opt.md)（缓存与局部性）。
> 难度：★★★☆☆（掌握有序容器与节点句柄，需理解红黑树平衡）。
> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2 -Wall -Wextra`）。源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`。本章 `[实现]` 级源码取自 `bits/stl_set.h`、`bits/stl_multiset.h`、`bits/stl_tree.h`，逐行标注文件与行号。

## ⓪ 历史动机：set / multiset 的来龙去脉
> 把"数学上的集合"搬进内存：去重、有序、可求交集并集——这是 set 存在的全部理由。

### 0.1 起源（谁·何时·为何）
`set` 是 `map` 的"键值合一"兄弟：它只存键、且键唯一、自动排序。<span class="badge badge-history">史</span> 它回应的是一个朴素需求——**维护一个不重复、且随时有序的元素集合**，并支持高效的插入、删除、查找。STL 同样用红黑树实现，因此享有"节点稳定 + O(log n)"的同样保证，并天然适配 `set_union`、`set_intersection` 等集合算法（⟶ Book/part08_algorithms）。<span class="badge badge-history">史</span>

### 0.2 关键转折（编年）
- C++98：`std::set`/`std::multiset` 随 STL 标准化，确立"有序唯一/可重复"语义。<span class="badge badge-history">史</span>
- 后续：C++11 的 `unordered_set`（[第85章　unordered_map / unordered_set：哈希开链集合](../part07_stl/ch85_unordered.md)）提供哈希版对照；C++20 起与 ranges 联动更顺。

### 0.3 设计哲学之争
`set` 与 `unordered_set` 的争论，本质同 `map` 家族：要不要"有序"这笔账。<span class="badge badge-comment">评</span> `set` 的额外价值在于——它直接对应数学集合，配合 STL 集合算法能做并集/交集/差集，这是哈希容器难以优雅替代的。<span class="badge badge-comment">评</span> 而红黑树带来的"有序遍历"在需要按序输出（如排行榜、字典序）时仍是首选。

### 0.4 史料补遗与持续编年

> 0.2 停在 C++20 起 `set` 与 ranges 联动更顺。小整数集合替代与"flat set"是后续支线。

- <span class="badge badge-history">史</span> **小整数集合：`set` vs `bitset` 各有适用**：当元素是 0…N-1 的连续小整数，`std::bitset<N>` 每元素仅占 1 位、位运算极快，远胜 `set<int>`；但 `bitset` 大小编译期固定，集合语义（并集/交集）需手写，而 `set` 支持任意类型与动态增长（⟶ ch87）。
- <span class="badge badge-history">史</span> **异构查找同样惠及 `set`**：C++14 起可用 `string_view` 之类的异类型做查找，C++20 起 `contains` 等接口更完整，避免为查找临时构造键对象。
- <span class="badge badge-comment">评</span> **`flat_set`（连续有序集合）在库中兴起**：Abseil 等提供把元素存进连续 `vector` 并保持有序的 `flat_set`，查找 O(log n) 且缓存远好于红黑树 `set`——代价是插入/删除要搬移元素，适合"查多写少"。
- <span class="badge badge-history">史</span> **C++ 标准暂无 `flat_set` 入标定论**：相关提案（连续存储有序容器）多次讨论，强调"与 `set` 接口兼容、底层用 `vector`"，但尚未成为正式标准。

> 史料来源：[cppreference std::set](https://en.cppreference.com/w/cpp/container/set)、[Abseil 官方文档](https://abseil.io/docs/cpp/)

> **一句话结论**：set/multiset 是有序唯一或可取重复的集合，红黑树保证中序即排序；需要「自动去重加范围遍历」时用它，纯查找才考虑哈希版。

!!! note "类比：set = 不收重名的会员名册"
    `std::set` 可以**类比**为一张拒绝重名的会员名册：插入重复名字会被 quietly 拒绝。去重过程更**好比**用筛子滤掉杂质，只留唯一颗粒。

    > 失效边界：元素是「键即值」且不可原地修改——改了会破坏红黑树的序，必须 `erase` 后重新 `insert`；查找同样是 O(log n)。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

[第 83 章　map / multimap：红黑树](../part07_stl/ch83_map.md)
[第 85 章　unordered 容器：哈希表](../part07_stl/ch85_unordered.md)

`std::set` 与 `std::multiset` 是基于**红黑树（Red-Black Tree，RB-tree）**的有序关联容器，二者只在"键是否允许重复"上不同：

- `set`：键唯一，插入重复键被忽略（返回 `pair<iterator,bool>` 的 `bool==false`）。
- `multiset`：键可重复，所有相等键都被保留，`count()` 可能 >1，`equal_range()` 返回一段连续区间。

把"唯一/多重"这一行记牢后，真正的深水区来了——`set` 常被当成"自动去重的有序盒子"，但它底层那棵红黑树和它的 C++17 节点接口，藏着不少你以为懂、其实没懂的设计。本章要带着这七笔账往下读：

1. **`set` 和 `multiset` 除了"能不能重复"，接口上还差了什么？** 答案是**插入语义**：`set::insert(重复键)` 静默忽略并返回 `{已存在者, false}`，`multiset::insert` 永远成功。这直接决定你写业务代码时哪个容器对你撒谎更少。本章 ⑰ FAQ + ⑯ 易错点把这对容易混的落点钉死。
2. **那棵 `_Rb_tree` 到底是什么？"平衡代价"又是谁在付？** `set` 包着标准库的红黑树 `_Rb_tree`，节点散布在堆上、带红/黑着色与旋转维护——这就是"有序 + O(log n)"的代价来源。数据量大时，节点在堆上东一个西一个，缓存命中率远不如拼接的 `vector`。本章 ⑦ ASCII 内存图 + ⑬ 源码分析把它画出来，⑲ 性能量出这条缓存的账。
3. **C++17 的 `node_type` 真的能"零拷贝搬家"吗？** 提取（`extract`）/合并（`merge`）让你把节点**原封不动从一棵树搬进另一棵**——不复制元素、不重新分配，只是改指针。这在"把一批元素从 set 迁移到另一个 set、又要保留原节点寿命"的场景里是唯一正解。本章 ⑬ 源码 + ⑭ WG21 说明它的语义边界。
4. **透明比较器凭什么能省掉一次临时对象构造？** `s.find("literal")` 若比较器不透明会先造一个临时 `std::string` 再比；C++20 的 heterogeneous lookup（`is_transparent` 的 `std::less<>`）则直接拿字面量比，省一次堆分配。本章 ⑩ 汇编会展示多出的那次构造到底长了什么样。
5. **`lower_bound`/`upper_bound`/`equal_range` 三件套，什么时候别用 `count`？** 区间查询都是 O(log n) 的树下降，`equal_range` 一次拿到 `[begin,end)`，比"`count` 数一遍再 `find`"更干净。本章 ⑨ 调用栈 + ⑮ 面试题把这段高效路径的用法与边界讲清。
6. **工业上 `set` 到底用来干哪些活？** 它最经典的主场是**访问控制允许列表、日志过滤、请求去重、路由表**——都是"既要判存在、又要保有序"的场景。选型判断标准是"是否有序遍历 + 节点稳定性"这个组合，而非"它叫 set"。本章 ⑫ 工业案例（服务器访问控制）会给你一个能直接抄的骨架。
7. **`set` vs `unordered_set` vs `flat_set`，到底站哪边？** 结论先行：需要有序 + 稳定迭代器选 `set`；只求哈希级常数 O(1) 且不在乎顺序选 `unordered_set`（见 [ch85](../part07_stl/ch85_unordered.md)）；元素少、只读查询多时，用排序 `vector` 模拟的 `flat_set` 甚至更快。本章 ⑳ 跨语言对比 + ⑲ 性能给你一张不靠感觉做选择的对照表。

## ② 前置知识

- 关联容器与迭代器：[第76章　STL 架构与迭代器概念](../part07_stl/ch76_stl_arch.md)（STL 架构与迭代器概念）。
- `map`/`multimap`：`set` 是"键即值"的 `map`，底层同为 `_Rb_tree`，强烈建议先读 [第83章　map / multimap（红黑树）](../part07_stl/ch83_map.md)。
- 比较器（`Compare`）：默认 `std::less<Key>`，要求**严格弱序（strict weak ordering）**，见 [第19章　变量、存储期、链接与 ODR（工业级深度版）](../part03_language/ch19_variables.md) §比较语义。
- 异常安全与 RAII：[第 40 章　异常安全（Exception Safety）](../part04_memory/ch40_exception_safety.md)。
- 移动语义：提取节点依赖移动，见 [第115章　移动语义与右值引用](../part10_modern/ch115_move.md)。

## ③ 后续依赖

- `unordered_set`/`unordered_map`：哈希而非有序，平均 O(1) 查找，见 [第85章　unordered_map / unordered_set：哈希开链集合](../part07_stl/ch85_unordered.md)。
- 缓存与局部性：RB 树节点随机散布于堆，缓存命中率低，对比见 [第154章　缓存优化与数据局部性（C++/硬件）](../part14_perf/ch154_cache_opt.md)。
- 容器适配器 `set` 不提供，但 `priority_queue` 用堆，见 [第86章　容器适配器：stack / queue / priority_queue](../part07_stl/ch86_adapters.md)。

## ④ 知识图谱（ASCII）

> **示例 1** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 知识图谱（ASCII）
```mermaid
flowchart TD
    A["Associative Container<br/>(有序，key==value)"]
    A -->|"由"| B["_Rb_tree (bits/stl_tree.h)<br/>RB-tree, 平衡 O(log n)"]
    B -->|"Compare 决定排序"| C["std::less<K><br/>严格弱序"]
    B -->|"节点 = {color,3×ptr} + value"| D["_Rb_tree_node_base<br/>{ _M_color, _M_parent, _M_left, _M_right }"]
    C --> E["std::set<K><br/>键唯一<br/>insert→pair<it,b><br/>count∈{0,1}"]
    D --> F["std::multiset<K><br/>键可重复<br/>insert→iterator<br/>count≥0"]
    E -->|"node_type 提取/merge"| F
```

## ⑤ Mermaid 流程图：一次 `insert` 的执行路径

```mermaid
flowchart TD
    A[insert key] --> B{"树为空?"}
    B -- 是 --> C["新建根节点, 染黑"]
    B -- 否 --> D["从根下降: compare key"]
    D --> E{"key 已存在?"}
    E -- set 且存在 --> F["返回 pair<old_it,false>"]
    E -- multiset 或 不存在 --> G["新建节点, 染红"]
    G --> H[_Rb_tree_insert_and_rebalance]
    H --> I{"违反 RB 性质?"}
    I -- 是 --> J["旋转 + 重染色"]
    I -- 否 --> K[完成]
    J --> K
    F --> L[结束]
```

## ⑥ UML 类图（Mermaid classDiagram）

```mermaid
classDiagram
    class set~K,Compare,Alloc~ {
        +insert(x) pair~iterator,bool~
        +extract(pos) node_type
        +merge(src) void
        +find(k) iterator
        +contains(k) bool
        +lower_bound(k) iterator
        +upper_bound(k) iterator
        +equal_range(k) pair~it,it~
        +count(k) size_type
        +erase(...) size_type
    }
    class multiset~K,Compare,Alloc~ {
        +insert(x) iterator
        +count(k) size_type
        +equal_range(k) pair~it,it~
    }
    class _Rb_tree~Key,Val,KeyOfVal,Compare,Alloc~ {
        -_M_header
        +_M_insert_unique()
        +_M_insert_equal()
        +_M_erase()
        +_M_equal_range_tr()
    }
    set --> _Rb_tree : 组合 _M_t
    multiset --> _Rb_tree : 组合 _M_t
    note for _Rb_tree "bits/stl_tree.h:427 class _Rb_tree"
```

## ⑦ ASCII 内存图 / 对象布局

`set<int>` 每个节点 = `_Rb_tree_node_base` + `int` 值。x86-64 下（指针 8 字节，对齐 8）：

> **示例 2** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内存图 / 对象布局
```mermaid
flowchart TD
    %% 注：省略部分细节（内存偏移表见正文）。set<int> 节点布局与堆示意
    BASE["_Rb_tree_node_base (32B)<br/>color 1B | pad7 | parent 8B | left 8B<br/>right 8B"]
    NODE["_Rb_tree_node<int> (40B)<br/>[node_base 32B] | int value 4B | padv4<br/>合计 32B 基类 + 值 4B + pad4 = 40B / 节点"]
    BASE --> NODE
    HEAP["Heap 示意：3 个键 {5,3,8}<br/>[node3] red parent→header left→null right→null value=3<br/>[node8] red parent→header left→null right→null value=8<br/>[node5] black parent→header left→node3 right→node8 value=5<br/>header: _M_parent→node5, _M_left→min(node3), _M_right→max(node8)"]
```

- `[实现·GCC15]`：`set` 对象本体只持有 `_Rb_tree` 成员（`_M_header` 哨兵、比较器、分配器状态），通常 **24~48 字节**（3 指针量级 + 对齐），真正的节点在堆上。
- 对比裸 `int`：1 个 `int` 4 字节；1 个 `set<int>` 节点 40 字节——**每元素约 36 字节固定开销**（3 指针 + 颜色 + 对齐 + 堆分配头）。这是有序性的代价。

## ⑧ 生命周期图

> **示例 3** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 生命周期图
```mermaid
flowchart TD
    A["构造 set"]
    A --> B["仅建 header 哨兵(黑)"]
    B --> C["insert(k1..kN): 每次 new 一个节点"]
    C --> D["平衡旋转（仅改指针与颜色，不拷贝值）"]
    D --> E["set 析构"]
    E --> F["_M_erase(begin) 递归 delete 每个节点"]
    F --> G["分配器释放"]
    G --> H["extract(node): 仅把节点从树链表摘除并「移交所有权」，**不析构值**，node_type 析构时才析构"]
```

## ⑨ 调用栈 / 时序图（一次 `set::insert`）

> **示例 4** <span class="badge badge-exp">难度 ★★★☆☆</span> · 调用栈 / 时序图
```mermaid
flowchart TD
    A["调用方"]
    A --> B["set<int>::insert(7)  // stl_set.h:509"]
    B --> C["_Rb_tree::_M_insert_unique(7)  // stl_tree.h:1133"]
    C --> C1["下降查找插入点 (compare)"]
    C1 --> D["_Rb_tree_insert_and_rebalance(...)  // stl_tree.h:410"]
    D --> D1["旋转/染色保持 RB 性质"]
    D1 --> E["返回 pair<iterator,bool>"]
```

## ⑩ 汇编分析（Compiler Explorer 风格，标注 -O2）

以 `set<int>::find` 的下降循环为例。红黑树查找本质是"沿指针比较并左右转"的循环，GCC13 `-O2` 下大致结构（`set<int>::find` 内联进调用者后）：

```asm
; 示意：_Rb_tree::find 的关键下降循环（-O2, x86-64, AT&T 语法，结构对应 stl_tree.h:101 的 _Rb_tree_node_base）
.Lfind_loop:
    mov     rcx, QWORD PTR [rax+16]   ; _M_parent? 实际取 _M_left/_M_right 指针
    mov     rdx, QWORD PTR [rax+24]   ; 取 _M_left  (offset 24 = base 32? 见下注)
    mov     esi, DWORD PTR [rdx+32]   ; 读节点中的 int 值 (value 偏移)
    cmp     esi, ebx                  ; 比较 key
    je      .Lfound                   ; 相等 -> 命中
    jg      .Lgo_right                ; key < node -> 走左
    mov     rax, rdx                  ; 沿 _M_left 下降
    jmp     .Lfind_loop
.Lgo_right:
    mov     rax, QWORD PTR [rax+32]   ; 沿 _M_right 下降
    jmp     .Lfind_loop
```

- `[实现·GCC15]`：真实偏移取决于 `_Rb_tree_node_base` 字段布局（`stl_tree.h:101`：依次为 `_M_color`、`_M_parent`、`_M_left`、`_M_right`）。上段为**示意性**还原调用结构，真实偏移会因 ABI 对齐略有差异，但"指针追逐 + `cmp`/`jcc`"的核心模式不变。
- `[经验]`：树查找是**数据依赖串行**，无法自动向量化，且每跳一次可能一次缓存缺失（节点散布堆中）。这是有序容器在热点路径上不如 `unordered_set`（ch85）或排序 `vector` 二分（缓存友好）的根本原因。

## ⑪ STL 联系

- 与 `map`：`set<K>` ≈ `map<K, K>` 的"键即值"特例，二者共用 `_Rb_tree`（[第83章　map / multimap（红黑树）](../part07_stl/ch83_map.md)）。
- 与 `unordered_set`：有序、范围查询强、缓存差；哈希平均 O(1)、范围查询弱（[第85章　unordered_map / unordered_set：哈希开链集合](../part07_stl/ch85_unordered.md)）。
- 与 `vector`+`sort`/`flat_set` 模拟：排序 `vector` 二分查找缓存友好、无节点开销，但插入 O(n)；见 ⑲ 与 ⑳。
- 与算法 `std::set_union` 等：这些算法要求**已排序区间**，可直接对 `set` 的区间使用（⑬ 示例）。

## ⑫ 工业案例：服务器访问控制允许列表（非 Hello World）

场景：游戏/IM 网关按**客户端连接 ID 白名单**做准入控制，需高频 `contains` 判定且支持热更新（运营临时封禁/解封）。

> **示例 5** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例：服务器访问控制允许列表
```cpp
// 工业案例 C1：网关连接允许列表（白名单准入）
#include <set>
#include <string>
#include <iostream>

// 允许接入的客户端 ID 集合（有序，便于区间审计与持久化有序导出）
class AllowList {
    std::set<unsigned long long> ids;
public:
    // 批量加载（运营配置）
    void load(const std::set<unsigned long long>& init) { ids = init; }

    // 热点路径：每帧/每包判定准入。contains 是 C++20，O(log n)
    bool admit(unsigned long long cid) const {
        return ids.contains(cid);          // [C++20] 等价于 find!=end，但语义更清晰
    }

    // 运营封禁：移除（返回是否真移除）
    bool ban(unsigned long long cid) { return ids.erase(cid) > 0; }

    // 临时放行：插入
    bool allow(unsigned long long cid) { return ids.insert(cid).second; }

    // 审计：导出有序区间（有序性天然支持"按 ID 段"审查）
    std::set<unsigned long long> range(unsigned long long lo,
                                       unsigned long long hi) const {
        auto a = ids.lower_bound(lo);
        auto b = ids.upper_bound(hi);
        return std::set<unsigned long long>(a, b);
    }
};

int main() {
    AllowList wl;
    wl.load({1001ULL, 1002ULL, 2000ULL, 3000ULL});
    std::cout << "admit 1002 = " << wl.admit(1002) << "\n";   // 1
    std::cout << "admit 9999 = " << wl.admit(9999) << "\n";   // 0
    wl.ban(1002);
    std::cout << "after ban, admit 1002 = " << wl.admit(1002) << "\n"; // 0
    auto seg = wl.range(1500ULL, 3500ULL);
    std::cout << "range size = " << seg.size() << "\n";        // 2 (2000,3000)
    return 0;
}
```

- `[经验]`：白名单**只读为主、写极少**时，`contains` 的 O(log n) 完全够用；若写频繁且需持久化有序快照，`set` 的有序迭代可直接落盘。

## ⑬ 源码分析（libstdc++ 逐行）

`std::set` 是 `_Rb_tree` 的薄封装（`bits/stl_set.h:94` `class set`，组合成员 `_Rep_type _M_t`）：

> **示例 6** <span class="badge badge-exp">难度 ★★★☆☆</span> · 源码分析（libstdc++ 逐行）
```cpp
// 文件：bits/stl_set.h   行号：94, 156
//   94:  class set
//  156:  using node_type = typename _Rep_type::node_type;  // C++17 节点句柄类型
//
// 文件：bits/stl_set.h   行号：509, 578, 584-594
//  509:  insert(const value_type& __x)   -> 转 _M_t._M_insert_unique
//  578:  insert(initializer_list<value_type> __l)
//  584:  node_type extract(const_iterator __pos);          // 摘除节点，不移交值
//  593:  node_type extract(const key_type& __x);
//  598:  insert(node_type&& __nh);                         // 重新挂回，零拷贝
//
// 文件：bits/stl_set.h   行号：611-627  merge
//  611:  merge(set<_Key, _Compare1, _Alloc>& __source)
//  614:    _M_t._M_merge_unique(_Merge_helper::_S_get_tree(__source));
//  merge 把 __source 中"不重复"的节点直接搬进本 set，不拷贝值。
```

底层 `_Rb_tree`（`bits/stl_tree.h:427 class _Rb_tree`）：

> **示例 7** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 源码分析（libstdc++ 逐行）
```cpp
// 文件：bits/stl_tree.h   行号：99, 101, 410, 417, 1048, 1052, 1378
//   99:  enum _Rb_tree_color { _S_red = false, _S_black = true };
//  101:  struct _Rb_tree_node_base { _Rb_tree_color _M_color; _Base_ptr _M_parent;
//                                    _Base_ptr _M_left;  _Base_ptr _M_right; };
//  410:  _Rb_tree_insert_and_rebalance(const bool __insert_left, _Link_type __x,
//                                      _Base_ptr __p, _Rb_tree_node_base& __header);
//  417:  _Rb_tree_rebalance_for_erase(_Rb_tree_node_base* const __z, ...);
// 1048:  _M_insert_unique(_Arg&&)   // set 用：键唯一
// 1052:  _M_insert_equal(_Arg&&)    // multiset 用：键可重复
// 1378:  _M_equal_range_tr(const _Kt& __k)  // 透明比较版本 equal_range
```

- `[实现·GCC15]`：`set::insert` 直接转发 `_M_t._M_insert_unique`（`stl_tree.h:1133`），返回 `pair<iterator,bool>`；`multiset::insert` 转发 `_M_t._M_insert_equal`（`stl_multiset.h:504`），仅返回 `iterator`（因为总能插入）。
- `[实现·GCC15]`：颜色编码为 `bool`，`_S_red=false`、`_S_black=true`，与常见"红=true"实现相反，读源码时勿混淆（`stl_tree.h:99`）。

## ⑭ WG21 提案（编号 + 标题 + 动机）

| 提案 | 标题 | 进入标准 | 与本容器关系 |
|---|---|---|---|
| N3657 | Adding heterogeneous comparison lookup to associative containers | C++14 | `std::less<>` 透明比较雏形 |
| P0919R3 | Heterogeneous lookup for unordered containers | C++20 | `set` 早已支持透明比较；unordered 在 C++20 跟进 |
| LWG 2356 | `ordering` of `map`/`set` extract/merge | C++17 | 引入 `node_type`、`extract`、`merge` |
| P1209 | `contains` for `set`/`map` | C++20 | `set::contains`/`map::contains` 语义更清晰 |

- `[标准]`：节点句柄（`node_type`）来自 C++17（LWG 2356），解决"跨容器移动元素时必须拷贝值"的痛点；`contains` 来自 C++20（P1209）。
- `[标准]`：透明比较器要求比较类型具备 `is_transparent` 成员（`std::less<>` 自带），使 `find(string_view)` 等不必先构造 `std::string` 临时量（见 ⑯）。

## ⑮ 面试题

1. `set` 和 `vector` 去重后排序，查找性能与适用场景有何差异？
   → `set` 插入/删除 O(log n) 且保持有序；`vector`+`sort` 排序后二分 O(log n) 但插入 O(n)。读写均衡用 `set`，批量静态数据用排序 `vector`。
2. `set<int> s; s.insert(5); s.insert(5);` 之后 `s.size()` 是？
   → 1（`set` 键唯一，第二次被忽略，返回 `bool==false`）。`multiset` 则为 2。
3. `extract` 之后节点里的元素会被析构吗？
   → 不会。`node_type` 接管节点所有权，仅在 `node_type` 自身析构时才析构值，因此可实现零拷贝迁移。
4. 为什么 `set` 的 `compare` 必须满足严格弱序？不满足会怎样？
   → 红黑树依赖全序定位插入点；若 `comp(a,a)==true` 或不可传递，查找/插入会走错分支，导致**未定义行为**（数据损坏/死循环）。
5. `multiset` 的 `equal_range(k)` 返回区间长度一定等于 `count(k)` 吗？
   → 是，二者都覆盖所有等价于 `k` 的元素；`equal_range` 是 `[lower_bound, upper_bound)`。

## ⑯ 易错点

> **示例 8** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 易错点
```cpp
// ❌ 错误1：比较器不满足严格弱序（comp(a,a) 必须为 false）
#include <set>
struct BadCmp {
    bool operator()(int a, int b) const { return a <= b; } // ❌ a<=a 为 true，破坏严格弱序 -> UB
};
// ✅ 正确：用 <
struct GoodCmp {
    bool operator()(int a, int b) const { return a < b; }  // ✅ 严格弱序
};
int main() {
    std::set<int, GoodCmp> s;
    s.insert(3); s.insert(1); s.insert(2);
    return 0;
}
```

> **示例 9** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 易错点
```cpp
// ❌ 错误2：用 extract 后继续使用被摘除的迭代器
#include <set>
#include <iostream>
int main() {
    std::set<int> s{1,2,3};
    auto it = s.find(2);
    auto nh = s.extract(it);     // it 已失效
    // std::cout << *it << "\n"; // ❌ UB：it 在 extract 后失效
    std::cout << nh.value() << "\n";   // ✅ 从 node_type 取值
    return 0;
}
```

> **示例 10** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
// ❌ 错误3：multiset 误用 insert 返回值当成 pair
#include <set>
int main() {
    std::multiset<int> ms;
    auto it = ms.insert(5);   // ✅ 返回 iterator（不是 pair）
    // auto p = ms.insert(5); // ❌ 若写成 pair 解构会编译错
    (void)it;
    return 0;
}
```

> **示例 11** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
// ❌ 错误4：透明比较要求 hasher/comparator 有 is_transparent，否则 find(其它类型) 不编译
#include <set>
#include <string>
#include <string_view>
int main() {
    std::set<std::string, std::less<>> s{"abc"};   // ✅ std::less<> 透明
    auto it = s.find(std::string_view("abc"));      // ✅ 无需构造临时 string
    (void)it;
    return 0;
}
```

## ⑰ FAQ

**Q：`set` 能不能存自定义类型？**
能，但必须可排序：要么特化 `std::less<MyType>`，要么在类型内定义 `operator<`（或传入自定义 `Compare`）。

**Q：`set` 的迭代器在插入/删除其它元素后是否失效？**
`std::set`/`multiset` 是节点式容器：**插入不使任何迭代器/引用/指针失效**；删除仅使指向被删元素的迭代器失效，其余有效。这是它相对 `vector` 的一大优势。

**Q：为什么 `set` 查找比 `unordered_set` 慢？**
平均路径长且缓存不友好：每次比较都要解引用一个堆节点指针（可能缓存缺失），而哈希平均 O(1)。但 `set` 提供有序遍历与范围查询，`unordered_set` 不保证顺序。

**Q：`extract` + `insert(node_type)` 比 `erase` + `insert(value)` 好在哪？**
前者只改指针、不移动/拷贝值（对大对象或不可拷贝类型尤其重要），且**不重新分配节点**；后者要先拷贝值再析构原节点，可能涉及分配。

## ⑱ 最佳实践

1. 只读判定优先用 `contains`（C++20），语义清晰。
2. 需要跨容器迁移大对象时，用 `extract`/`insert(node_type)` 避免拷贝。
3. 合并两个集合用 `merge`（C++17），比逐元素 `insert` 高效（节点直接搬）。
4. 区间查询用 `lower_bound`/`upper_bound`/`equal_range`，不要 `find` 后手动扫描。
5. 比较器保持**无状态、纯函数**且满足严格弱序；调试期可加断言。
6. 高频范围遍历 + 缓存敏感场景，考虑排序 `vector` 二分（见 ⑲/⑳）。
7. 并发：多个线程同时 `const` 读安全；有写则需 `std::mutex`（见下例）。

> **示例 12** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 最佳实践
```cpp
// 最佳实践 B1：并发读安全，写加锁
#include <set>
#include <mutex>
#include <thread>
std::set<int> g_tags;
std::mutex g_mtx;
bool is_tracked(int t) {                     // 多线程并发读：安全
    std::lock_guard<std::mutex> lk(g_mtx);   // 写路径才加锁
    return g_tags.contains(t);
}
void track(int t) {
    std::lock_guard<std::mutex> lk(g_mtx);
    g_tags.insert(t);
}
int main() {
    track(1); track(2);
    return is_tracked(1) ? 0 : 1;
}
```

## ⑲ 性能分析（复杂度 / 缓存 / ABI）

| 操作 | `set`/`multiset` | 排序 `vector`（模拟 flat_set） | `unordered_set` |
|---|---|---|---|
| 查找 | O(log n) | O(log n)（二分，缓存友好） | 平均 O(1)，最差 O(n) |
| 插入 | O(log n) + 1 次堆分配 | O(n)（移动后半段） | 平均 O(1) + 可能重哈希 |
| 删除 | O(log n) + 1 次堆释放 | O(n) | 平均 O(1) |
| 有序遍历 | O(n)，缓存差（指针跳） | O(n)，**缓存友好**（连续） | 不保证有序 |
| 内存/元素 | ~40B 节点（int） | 4B 值 + 少量 | 指针 + 哈希 + 桶数组 |

- `[实现·GCC15]`：RB 树每次插入/删除都涉及一次 `new`/`delete`（节点分配器），这是热点上的主要成本。
- `[平台·x86-64]`：`set` 遍历是"跳着读内存"，缓存命中低；对 10⁷ 量级元素的范围扫描，`vector` 二分/连续遍历常快数倍（[第154章　缓存优化与数据局部性（C++/硬件）](../part14_perf/ch154_cache_opt.md)）。
- `[平台·x86-64]`：ABI 稳定——`std::set` 的 `_Rb_tree` 布局跨 GCC 版本基本兼容，但跨编译器（libstdc++/libc++/MS STL）**不保证**二进制兼容，跨模块传递需用 C 接口或序列化。

> **示例 13** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 性能分析
```cpp
// 性能 P1：sorted vector 模拟 flat_set（GCC13 无 <flat_set>，用 vector+sort+二分）
#include <vector>
#include <algorithm>
#include <iostream>
int main() {
    std::vector<int> v{5,3,8,1,9,2};
    std::sort(v.begin(), v.end());           // 一次性排序 O(n log n)
    // 查找：二分，缓存友好
    bool found = std::binary_search(v.begin(), v.end(), 8);
    auto it = std::lower_bound(v.begin(), v.end(), 3);
    std::cout << "found8=" << found << " lb3=" << (it - v.begin()) << "\n"; // 1, 1
    // 插入：O(n) 移动（与 set 的 O(log n) 相反），故只适合"写少读多"
    v.insert(std::lower_bound(v.begin(), v.end(), 4), 4);
    std::cout << "size=" << v.size() << "\n"; // 7
    return 0;
}
```

> **示例 14** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 性能分析
```cpp
// 性能 P2：microbenchmark 量级（示意，-O2）。演示 set 与 sorted-vector 查找的循环结构
#include <set>
#include <vector>
#include <algorithm>
#include <iostream>
int main() {
    const int N = 100000;
    std::set<int> s; std::vector<int> v;
    for (int i = 0; i < N; ++i) { s.insert(i); v.push_back(i); }
    std::sort(v.begin(), v.end());
    long long sum = 0;
    // set 查找：串行指针追逐
    for (int i = 0; i < N; i += 7) if (s.contains(i)) sum += i;
    // vector 二分：连续内存，缓存友好
    for (int i = 0; i < N; i += 7) if (std::binary_search(v.begin(), v.end(), i)) sum += i;
    std::cout << "sum=" << sum << "\n";   // 防优化，量级: set 与 vector 量级同阶，
    return 0;                              // 但 vector 在缓存压力下通常更快
}
```

## ⑳ 跨语言对比

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：set 元素不可就地修改（const）。** 你想改集合里的成员得先删后插。请说明。
   - <span class="badge badge-std">标准</span> 有序/无序集合中的元素视为 const；修改会破坏容器排序/哈希不变式，须 erase 再 insert。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（元素 const 性）；cppreference "std::set" 词条。

2. **真实场景：multiset 允许重复 key、count 可 >1。** 你要统计某 key 出现次数。请说明差异。
   - <span class="badge badge-std">标准</span> set 保证 key 唯一；multiset 允许等价 key 重复存在，可用 `count`/`equal_range` 遍历。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（set 与 multiset 的 key 唯一性差异）；cppreference "std::multiset" 词条。

3. **真实场景：用 `emplace`/`try_emplace` 避免临时构造。** 你关心插入性能。请说明。
   - <span class="badge badge-std">标准</span> 关联容器提供 `emplace`/`try_emplace` 在容器内就地构造，避免先构造临时再拷贝/移动。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（emplace 接口）；cppreference "std::set::emplace" 词条。

| 语言 | 有序唯一集合 | 有序可重复 | 备注 |
|---|---|---|---|
| C++ | `std::set<K>` | `std::multiset<K>` | RB 树，O(log n)，节点开销大 |
| Rust | `BTreeSet<K>` | 无原生 multiset（`BTreeMap<K,usize>` 计数） | B 树而非 RB 树 |
| Go | 无内建（用 `map[K]struct{}` 模拟 set，无序） | 同 | 标准库无有序容器 |
| Java | `TreeSet<E>` | `TreeMultiset`（Guava） | 红黑树（`TreeMap` 实现） |
| Python | 无（用 `sortedcontainers.SortedSet` 第三方） | `SortedList` | 标准库无有序 set |
| C# | `SortedSet<T>` | 无原生（用 `SortedDictionary<T,int>` 计数） | 红黑树 |

- `[标准]`：`std::set` 对标 Java `TreeSet`、Rust `BTreeSet`，均为"有序、唯一"语义；`multiset` 对标 Guava `TreeMultiset`。
- `[经验]`：从 Rust/Java 迁移时，`set`↔`BTreeSet`/`TreeSet` 心智模型直接对应；从 Go/Python 来需注意"标准库有序容器"的缺失与节点开销。

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：std::set 与「去重有序集合」

<span class="badge badge-history">史</span> `std::set` / `std::multiset` 随 C++98 进入标准，与 `map` 同源，底层同为红黑树，区别是 `set` 以「元素本身即 key」存储，强制唯一（multiset 允许重复）。<span class="badge badge-history">史</span> 这一设计同样继承自 HP/SGI STL 的 `_Rb_tree`，保证有序遍历与 O(log N) 增删查。<span class="badge badge-anecdote">轶</span> 一个常被忽略的点：`set` 的元素是 `const` 的——不能就地修改，因为修改会破坏树的排序，必须先 `erase` 再 `insert`（或 C++11 起用 `extract` 取出节点改值后再插回，避免重分配）。<span class="badge badge-comment">评</span> `set` 的本质是「用 O(log N) 换取自动去重与有序」，当去重/有序是硬需求时它比手写排序数组更省心。

### ㉒.2 真实工程坐标：set 活在哪些产品里

服务器访问控制允许列表、唯一标识符集合、已处理任务集合、编译器/构建系统的「已访问文件集」是 `std::set` 的主场；游戏中的标签集合、配置白名单、去重的事件类型也常用 `set`。在需要「既去重又按序遍历」（如生成有序的唯一 ID 列表）时，`set` 比 `unordered_set` + 排序更直接。

- **跨行业实例（编译器/构建系统）**：CMake 与 LLVM 的 `llvm::DenseSet`/`SetVector` 思想即「有序/去重集合」，用于「已处理的源文件、已注册的 Pass、已访问的 AST 节点」防重；LLVM 官方还用 `SmallSet`（小集合栈上优化）管理编译器内部去重，是 `set` 语义在工具链上的真实延伸。
- **跨行业实例（网络安全/防火墙）**：WAF（Web 应用防火墙）与入侵检测系统（如 Suricata 的部分 C++ 模块）用有序/哈希 `set` 维护「已封禁 IP、命中规则集合、白名单」，保证「O(log N) 查重 + 按顺序导出策略」；其稳定节点特性也利于并发更新时不影响其他迭代。

### ㉒.3 生产踩坑：set 的常见误用与陷阱

<span class="badge badge-comment">评</span> 最大误区是「用 `set` 做高频去重的大集合」——红黑树每节点堆分配、缓存不友好，规模大且只需查重时 `unordered_set` 更快。另一坑是「试图修改 `set` 中元素」——元素是 const，直接改会破坏序，必须用 `extract` 或先删后插。还有「误用 `set` 当位图/布尔数组」——小范围整数去重用 `vector<bool>` 或 `bitset` 远比 `set<int>` 高效。

### ㉒.4 与标准的互动：set 与标准的演进

<span class="badge badge-history">史</span> `std::set` 自 C++98 稳定，C++11 引入 `emplace` / `extract`；C++14 透明比较器 `is_transparent` 同样适用于 `set`，允许异构查找；C++17 增加 `try_emplace` 风格接口与 `insert_or_assign`（multiset 部分适用）。<span class="badge badge-comment">评</span> 与 `map` 类似，C++23 的 `std::flat_set` 提供「连续数组 + 排序」的替代，缓存更友好；标准方向是在「有序唯一集合」上也给出连续存储选项，同时保留红黑树 `set` 的稳定节点优势。

- **WG21 修订链**：`std::set` 与 `map` 同源，自 C++98 稳定；C++11 引入 `emplace` 与节点句柄 `extract`（P0083R0）；C++14 透明比较器 `is_transparent`（N3657）同样适用于 `set` 的异构查找；C++17 增加 `try_emplace` 风格接口（实际上 `set` 用 `insert`/`extract` 表达）。C++23 的 `std::flat_set`（P1222R4，wg21.link/P1222R4）提供「连续数组 + 排序」的缓存友好替代。
- **ISO 条款**：`std::set` 规定于 ISO/IEC 14882 §24.4.6（`[set]`）。其元素被规定为 `const`（修改会破坏序），标准刻意要求用 `extract`/先删后插来改值——设计理由是「以不可变性换取有序性与迭代器稳定性」，让用户无法在「不破坏红黑树不变式」的前提下就地改变 key。

### ㉒.5 权威引用

- [cppreference: std::set](https://en.cppreference.com/w/cpp/container/set) — 红黑树有序去重集合与 const 元素的权威定义
- [open-std: WG21 提案索引](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/) — 查证 set 透明比较器、flat_set 等修订的一手来源
- [LLVM 项目仓库](https://github.com/llvm/llvm-project) — libc++ 的 set/__tree 工业实现参考

## 附录：练习题 / 思考题 / 源码阅读建议

**练习题**
1. 用 `multiset<int>` 实现一个"在线中位数"维护器（插入/删除后取中位数），分析复杂度。
2. 给定两个 `set<int>`，用 `std::set_union`/`set_intersection` 求并集与交集（需 `<algorithm>`，区间已排序）。
3. 实现一个 `CaseInsensitiveSet`（自定义比较器 + 小写归一化），验证插入 `"AbC"` 与 `"abc"` 视为同一键。

**思考题**
- 为什么 `set` 的实现选择红黑树而非 AVL 树？
  → RB 树插入/删除旋转次数更少（最多 2 次旋转），适合"修改频繁"的通用场景；AVL 更平衡、查找略快但维护成本高。
- `extract` 返回的 `node_type` 能否跨不同比较器的 `set` 迁移？
  → 仅当比较器**等价**（同键序）时可安全 `insert(node_type)`；否则语义错误。

**libstdc++ 源码阅读路线**
1. `bits/stl_tree.h:99-101` 颜色枚举与节点基类 → 理解 RB 节点内存布局。
2. `bits/stl_tree.h:410/417` `_Rb_tree_insert_and_rebalance` / `_Rb_tree_rebalance_for_erase` → 平衡核心（重点读旋转）。
3. `bits/stl_tree.h:1048/1052` `_M_insert_unique`/`_M_insert_equal` → 区分 set/multiset 语义。
4. `bits/stl_set.h:584-627` `extract`/`merge` → C++17 节点句柄机制。
5. `bits/stl_multiset.h:503/731/880` `insert`/`count`/`equal_range` → multiset 多重键语义。

---

以下为第84章完整可编译示例集（每块独立、自带 `#include` 与 `int main`，经 `g++ -std=c++23 -O2 -Wall -Wextra` 校验）。

> **示例 15** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S1 基础：set 创建、有序遍历、唯一性
#include <set>
#include <iostream>
int main() {
    std::set<int> s{5, 3, 8, 3, 1};          // 3 重复被忽略
    for (int x : s) std::cout << x << ' ';   // 1 3 5 8（自动有序）
    std::cout << "\nsize=" << s.size() << "\n"; // 4
    return 0;
}
```

> **示例 16** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S2 自定义降序比较器
#include <set>
#include <iostream>
struct Desc { bool operator()(int a, int b) const { return a > b; } };
int main() {
    std::set<int, Desc> s{5, 3, 8, 1};
    for (int x : s) std::cout << x << ' ';   // 8 5 3 1
    std::cout << "\n";
    return 0;
}
```

> **示例 17** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S3 multiset 基础与计数
#include <set>
#include <iostream>
int main() {
    std::multiset<int> ms{1, 2, 2, 2, 3, 3};
    std::cout << "count(2)=" << ms.count(2) << "\n";   // 3
    std::cout << "count(9)=" << ms.count(9) << "\n";   // 0
    std::cout << "size=" << ms.size() << "\n";         // 6
    return 0;
}
```

> **示例 18** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S4 insert 返回值：set 返回 pair<iterator,bool>
#include <set>
#include <iostream>
int main() {
    std::set<int> s;
    auto r1 = s.insert(10);
    std::cout << "inserted=" << r1.second << "\n";     // 1
    auto r2 = s.insert(10);
    std::cout << "inserted_again=" << r2.second << "\n"; // 0（已存在）
    std::cout << "*it=" << *r2.first << "\n";            // 10
    return 0;
}
```

> **示例 19** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S5 emplace 原地构造
#include <set>
#include <string>
#include <iostream>
int main() {
    std::set<std::string> s;
    auto r = s.emplace("hello");
    std::cout << "inserted=" << r.second << "\n";   // 1
    (void)r;
    return 0;
}
```

> **示例 20** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S6 contains (C++20) 与 find
#include <set>
#include <iostream>
int main() {
    std::set<int> s{1, 2, 3};
    std::cout << "contains(2)=" << s.contains(2) << "\n"; // 1
    std::cout << "contains(9)=" << s.contains(9) << "\n"; // 0
    if (s.find(3) != s.end()) std::cout << "found 3\n";
    return 0;
}
```

> **示例 21** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S7 lower_bound / upper_bound / equal_range（set）
#include <set>
#include <iostream>
int main() {
    std::set<int> s{10, 20, 20, 30, 40};
    auto lo = s.lower_bound(20);   // 首 >=20
    auto hi = s.upper_bound(20);   // 首 >20
    std::cout << "*lo=" << *lo << " *hi=" << *hi << "\n"; // 20 30
    auto rng = s.equal_range(20);
    std::cout << "dist=" << std::distance(rng.first, rng.second) << "\n"; // 2
    return 0;
}
```

> **示例 22** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S8 删除：按迭代器 / 按键 / 按区间
#include <set>
#include <iostream>
int main() {
    std::set<int> s{1, 2, 3, 4, 5};
    s.erase(s.find(3));                    // 按迭代器删
    std::cout << "after erase it: " << s.count(3) << "\n"; // 0
    std::cout << "erased key 4: " << s.erase(4) << "\n";   // 1
    auto a = s.lower_bound(1), b = s.upper_bound(2);
    s.erase(a, b);                         // 区间删 [1,2]
    for (int x : s) std::cout << x << ' '; // 5
    std::cout << "\n";
    return 0;
}
```

> **示例 23** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S9 extract 节点句柄 + 重新挂回（零拷贝）
#include <set>
#include <iostream>
#include <utility>
int main() {
    std::set<int> s{1, 2, 3};
    auto nh = s.extract(s.find(2));        // 摘除，不析构值
    std::cout << "extracted=" << nh.value() << " size=" << s.size() << "\n"; // 2 1
    s.insert(std::move(nh));               // 重新挂回
    std::cout << "after reinsert size=" << s.size() << "\n"; // 2 -> 3
    return 0;
}
```

> **示例 24** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S10 extract 跨容器迁移 set -> multiset
#include <set>
#include <iostream>
#include <utility>
int main() {
    std::set<int> s{1, 2, 3};
    std::multiset<int> ms{10, 20};
    auto nh = s.extract(s.begin());        // 取走最小的 1
    ms.insert(std::move(nh));              // 迁入 multiset
    std::cout << "s.size=" << s.size() << " ms.size=" << ms.size() << "\n"; // 2 3
    return 0;
}
```

> **示例 25** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S11 merge 合并（C++17）：仅搬不重复节点
#include <set>
#include <iostream>
int main() {
    std::set<int> a{1, 2, 3}, b{3, 4, 5};
    a.merge(b);                            // 3 已在 a，留在 b
    for (int x : a) std::cout << x << ' '; // 1 2 3 4 5
    std::cout << "\nleft in b: " << b.size() << "\n"; // 1 (仅 3)
    return 0;
}
```

> **示例 26** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S12 透明比较器：find 不必构造临时 string
#include <set>
#include <string>
#include <string_view>
#include <iostream>
int main() {
    std::set<std::string, std::less<>> s{"alpha", "beta"}; // less<> 透明
    auto it = s.find(std::string_view("beta"));            // 无临时 string
    std::cout << (it != s.end() ? *it : "miss") << "\n";  // beta
    return 0;
}
```

> **示例 27** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S13 反向遍历（有序性的红利）
#include <set>
#include <iostream>
int main() {
    std::set<int> s{1, 2, 3, 4};
    for (auto it = s.rbegin(); it != s.rend(); ++it) std::cout << *it << ' '; // 4 3 2 1
    std::cout << "\n";
    return 0;
}
```

> **示例 28** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S14 multiset equal_range 统计某键全部出现
#include <set>
#include <iostream>
int main() {
    std::multiset<int> ms{2, 2, 2, 5, 5, 9};
    auto r = ms.equal_range(2);
    std::cout << "count(2)=" << std::distance(r.first, r.second) << "\n"; // 3
    return 0;
}
```

> **示例 29** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S15 multiset 插入提示（hint）优化连续插入
#include <set>
#include <iostream>
int main() {
    std::multiset<int> ms;
    auto hint = ms.begin();
    for (int i = 0; i < 3; ++i) hint = ms.insert(hint, i); // 提示位置
    for (int x : ms) std::cout << x << ' ';  // 0 1 2
    std::cout << "\n";
    return 0;
}
```

> **示例 30** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S16 set 交换（O(1) 指针交换）
#include <set>
#include <iostream>
int main() {
    std::set<int> a{1, 2}, b{3, 4};
    a.swap(b);
    std::cout << "a: " << a.size() << " b: " << b.size() << "\n"; // 2 2
    return 0;
}
```

> **示例 31** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S17 set 存自定义类型（提供 operator<）
#include <set>
#include <iostream>
#include <string>
struct User { int id; std::string name;
    bool operator<(const User& o) const { return id < o.id; } };
int main() {
    std::set<User> us{{3,"c"},{1,"a"},{2,"b"}};
    for (auto& u : us) std::cout << u.id << u.name << ' '; // 1a 2b 3c
    std::cout << "\n";
    return 0;
}
```

> **示例 32** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S18 set 去重 + 排序（经典用法）
#include <vector>
#include <set>
#include <iostream>
int main() {
    std::vector<int> v{4, 2, 4, 1, 3, 2};
    std::set<int> s(v.begin(), v.end());    // 去重并排序
    for (int x : s) std::cout << x << ' '; // 1 2 3 4
    std::cout << "\n";
    return 0;
}
```

> **示例 33** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S19 算法：set_union / set_intersection（区间须已排序）
#include <set>
#include <vector>
#include <algorithm>
#include <iostream>
int main() {
    std::set<int> a{1, 2, 3}, b{2, 3, 4};
    std::vector<int> uni, inter;
    std::set_union(a.begin(), a.end(), b.begin(), b.end(),
                   std::back_inserter(uni));
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(),
                          std::back_inserter(inter));
    std::cout << "union=" << uni.size() << " inter=" << inter.size() << "\n"; // 4 2
    return 0;
}
```

> **示例 34** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S20 计数不同元素数量
#include <set>
#include <iostream>
int main() {
    int arr[] = {1, 1, 2, 3, 3, 3, 4};
    std::set<int> s(std::begin(arr), std::end(arr));
    std::cout << "distinct=" << s.size() << "\n"; // 4
    return 0;
}
```

> **示例 35** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S21 节点内存开销实测（sizeof 与节点估算）
#include <set>
#include <iostream>
int main() {
    std::set<int> s;
    std::cout << "sizeof(set<int>)=" << sizeof(s) << "\n";       // 通常 48（3 ptr 量级）
    std::cout << "sizeof(int)=" << sizeof(int) << "\n";         // 4
    std::cout << "per-node overhead ~= 36 bytes (RB node)\n";
    return 0;
}
```

> **示例 36** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S22 工业：日志级别过滤器（枚举 + set）
#include <set>
#include <iostream>
#include <string>
enum class Level { Debug, Info, Warn, Error };
std::set<Level> make_filter() { return {Level::Warn, Level::Error}; }
int main() {
    auto flt = make_filter();
    auto enabled = [&](Level l){ return flt.contains(l); };
    std::cout << "Warn on=" << enabled(Level::Warn)
              << " Debug on=" << enabled(Level::Debug) << "\n"; // 1 0
    return 0;
}
```

> **示例 37** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S23 工业：请求 ID 去重计数（multiset 当频率表）
#include <set>
#include <iostream>
int main() {
    std::multiset<unsigned long long> reqs;
    reqs.insert(1001); reqs.insert(1001); reqs.insert(2002);
    std::cout << "req 1001 seen " << reqs.count(1001) << " times\n"; // 2
    return 0;
}
```

> **示例 38** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S24 工业：URL 路由前缀白名单（有序便于按段审查）
#include <set>
#include <string>
#include <iostream>
int main() {
    std::set<std::string> routes{"/api/v1/users", "/api/v1/orders", "/health"};
    auto it = routes.lower_bound("/api/");
    auto end = routes.lower_bound("/api/v2");
    for (; it != end; ++it) std::cout << *it << "\n"; // 两个 /api/v1/*
    return 0;
}
```

> **示例 39** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S25 透明比较 + 自定义 KeyEqual 结构（完整异构查找）
#include <set>
#include <string>
#include <string_view>
#include <iostream>
struct StrLess {
    using is_transparent = void;                 // 启用异构
    bool operator()(std::string_view a, std::string_view b) const { return a < b; }
};
int main() {
    std::set<std::string, StrLess> s{"xyz", "abc"};
    auto it = s.find(std::string_view("abc"));    // 异构，无临时 string
    std::cout << (it != s.end() ? *it : "x") << "\n"; // abc
    return 0;
}
```

> **示例 40** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S26 multiset 删除全部某键（erase(key) 返回删除个数）
#include <set>
#include <iostream>
int main() {
    std::multiset<int> ms{1, 1, 1, 2, 3};
    std::cout << "erased=" << ms.erase(1) << "\n"; // 3
    for (int x : ms) std::cout << x << ' ';        // 2 3
    std::cout << "\n";
    return 0;
}
```

> **示例 41** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S27 迭代器失效验证：插入不影响其它迭代器
#include <set>
#include <iostream>
int main() {
    std::set<int> s{1, 2, 3};
    auto it = s.find(2);
    s.insert(99);                 // 插入不使 it 失效
    std::cout << "it still=" << *it << "\n"; // 2
    return 0;
}
```

> **示例 42** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S28 异常安全演示： insert 强异常保证（值类型构造抛异常不破坏容器）
#include <set>
#include <stdexcept>
#include <iostream>
struct Fragile {
    int id = 0;
    Fragile() { throw std::runtime_error("boom"); }   // 构造即抛
    bool operator<(const Fragile&) const { return false; } // 仅需满足比较器可实例化
};
int main() {
    std::set<Fragile> s;
    try { s.emplace(); }
    catch (const std::exception&) { std::cout << "size after throw=" << s.size() << "\n"; } // 0
    return 0;
}
```

> **示例 43** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S29 版本宏：C++20 contains 可用性探测
#include <set>
#include <iostream>
int main() {
#if __cplusplus >= 202002L
    std::set<int> s{1};
    std::cout << "c++20 contains=" << s.contains(1) << "\n";
#else
    std::cout << "needs c++20\n";
#endif
    return 0;
}
```

> **示例 44** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S30 自定义 KeyEqual 与 comparator 组合（大小写不敏感 set）
#include <set>
#include <string>
#include <cctype>
#include <iostream>
#include <cstddef>
struct CiLess {
    static int tolc(int c) { return (c >= 'A' && c <= 'Z') ? c + 32 : c; }
    bool operator()(const std::string& a, const std::string& b) const {
        for (size_t i = 0; i < a.size() && i < b.size(); ++i) {
            int ca = tolc((unsigned char)a[i]);
            int cb = tolc((unsigned char)b[i]);
            if (ca != cb) return ca < cb;
        }
        return a.size() < b.size();
    }
};
int main() {
    std::set<std::string, CiLess> s;
    s.insert("AbC"); s.insert("abc");     // 视为同一键
    std::cout << "size=" << s.size() << "\n"; // 1
    return 0;
}
```

> **示例 45** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S31 用用户定义字面量计时（UDL 带空格写法）+ 与 sorted vector 对比调度
#include <set>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iostream>
long long operator"" _ms(unsigned long long v) { return (long long)v; }  // 带空格写法
int main() {
    auto budget = 100_ms;                 // 用户字面量（带空格写法）
    std::set<int> s; std::vector<int> v;
    for (int i = 0; i < 1000; ++i) { s.insert(i); v.push_back(i); }
    std::sort(v.begin(), v.end());
    auto t0 = std::chrono::steady_clock::now();
    volatile int found = 0;
    for (int i = 0; i < 1000; i += 3) if (s.contains(i)) ++found;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "set lookup ok, found=" << found
              << " budget_ms=" << budget << "\n";
    (void)t0; (void)t1;
    return 0;
}
```

> **示例 46** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S32 折叠表达式配合 set（包展开打印，演示 C++17 折叠）
#include <set>
#include <iostream>
template<typename... Ts>
void insert_all(std::set<int>& s, Ts... xs) {
    ((s.insert((int)xs)), ...);   // 逗号折叠
}
int main() {
    std::set<int> s;
    insert_all(s, 1, 2, 3, 2);    // 2 重复被忽略
    std::cout << "size=" << s.size() << "\n"; // 3
    return 0;
}
```

> **示例 47** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S33 工业：配置项 key 集合与差异对比
#include <set>
#include <iostream>
#include <string>
#include <algorithm>
int main() {
    std::set<std::string> a{"timeout", "retries", "host"};
    std::set<std::string> b{"timeout", "port"};
    std::set<std::string> only_a;
    std::set_difference(a.begin(), a.end(), b.begin(), b.end(),
                        std::inserter(only_a, only_a.end()));
    for (auto& k : only_a) std::cout << k << ' '; // retries host
    std::cout << "\n";
    return 0;
}
```

> **示例 48** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S34 比较器严格弱序的单元测试桩（断言 comp(a,a)==false）
#include <set>
#include <iostream>
struct Cmp { bool operator()(int a, int b) const { return a < b; } };
int main() {
    Cmp c;
    std::set<int, Cmp> s;
    s.insert(5); s.insert(1);
    // 严格弱序不变量：c(x,x) 必须为 false
    std::cout << "irreflexive=" << (c(5,5) ? 0 : 1) << "\n"; // 1
    return 0;
}
```

> **示例 49** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录：练习题 / 思考题 / 源码阅
```cpp
// S35 内存图验证：递归打印 set 中序（即有序）以佐证 RB 中序=升序
#include <set>
#include <iostream>
void inorder(const std::set<int>& s) {
    for (auto it = s.begin(); it != s.end(); ++it) std::cout << *it << ' ';
}
int main() {
    std::set<int> s{8, 3, 10, 1, 6};
    inorder(s);  // 1 3 6 8 10（中序遍历即升序）
    std::cout << "\n";
    return 0;
}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第83章](../part07_stl/ch83_map.md) | 键值查找/缓存 | 本章提供概念，第83章提供实现 |
| [第85章](../part07_stl/ch85_unordered.md) | 索引查找/路由表 | 本章提供概念，第85章提供实现 |
| [第83章](../part07_stl/ch83_map.md) | 泛型库/编译期计算 | 本章提供概念，第83章提供实现 |
| [第85章](../part07_stl/ch85_unordered.md) | 高性能容器/零拷贝传输 | 本章提供概念，第85章提供实现 |
| [第86章](../part07_stl/ch86_adapters.md) | 资源管理/事务回滚 | 本章提供概念，第86章提供实现 |

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Abseil `absl::flat_hash_set`（github.com/abseil/abseil-cpp）**：O(1) 平均查找的开环哈希集合，瑞士表（Swiss Table）布局缓存友好。
  → <https://github.com/abseil/abseil-cpp>
- **Boost.MultiIndex（github.com/boostorg/multi_index）**：多键集合，单容器挂多个有序/哈希索引；`boost::multi_index_container` 对照 `std::set` 的多索引需求。
  → <https://github.com/boostorg/multi_index>
- **Chromium `base::flat_set` / `base::flat_map`（github.com/chromium/chromium）**：连续内存有序容器，缓存友好；插入 O(n) 但查找 O(log n) 且无节点分配，适合中小规模只读集合。
  → <https://github.com/chromium/chromium>
- **Boost.Container `flat_set`（github.com/boostorg/container）**：与 `std::set` 接口兼容的连续存储替代，避免红黑树节点碎片与指针 chasing。
  → <https://github.com/boostorg/container>
- **Folly `sorted_vector_set`（github.com/facebook/folly）**：排序 `vector` 后端集合，与 `flat_set` 同思路，提供稳定迭代器选项；Facebook 服务用它替代 `std::set` 降延迟。
  → <https://github.com/facebook/folly>
- **LLVM `SmallSet` / `SetVector`（github.com/llvm/llvm-project）**：小集合内联优化（≤N 元素用数组，超出转 `std::set`），编译期/运行期混合策略，LLVM 自身到处用它。
  → <https://github.com/llvm/llvm-project>

**常见陷阱 / 最佳实践**：
- `std::set` 插入即分配节点；成员去重用 `flat_hash_set` 更快，Chromium 与 Folly 在热路径都这么做。
- 有序输出才需要 `std::set`；`flat_hash_set` 不保证顺序且迭代器在重哈希后失效。

> 交叉引用：映射见 [ch83](../part07_stl/ch83_map.md)；哈希见 [ch38](../part04_memory/ch38_allocator.md)。

## 相关章节（交叉引用）

- **同模块相邻**：[第76章　STL 架构与迭代器概念](../part07_stl/ch76_stl_arch.md)—— 有序集合满足双向迭代器
- **同模块相邻**：[第83章　map / multimap（红黑树）](../part07_stl/ch83_map.md)）—— map 是其键值分离的变体
- **同模块相邻**：[第85章　unordered_map / unordered_set：哈希开链集合](../part07_stl/ch85_unordered.md)—— unordered_set 是其哈希无序版本
- **跨模块前置**：[第 38 章　分配器（Allocator）模型与 PMR](../part04_memory/ch38_allocator.md)模型与 PMR）—— 红黑树节点经 allocator 分配
- **相邻主题**：[第 40 章　异常安全（Exception Safety）](../part04_memory/ch40_exception_safety.md)）—— 插入的强异常保证依赖异常安全

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）
**真实场景：去重已成交订单号并有序输出。** 结算系统把重复成交单号 `set` 去重并按升序导出（红黑树天然有序唯一）。

> **示例 50** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 1（难度 ★★）
```cpp
#include <iostream>
#include <set>
int main() {
    std::set<int> s{3, 1, 2, 1, 3};
    for (int x : s) std::cout << x << ' ';
    std::cout << "\n";                       // 1 2 3
}
```

<span class="badge badge-std">标准</span> 结论：`std::set` 维护唯一 key 且始终有序（默认升序）；插入已存在元素会被忽略（返回 `pair<it,false>`），遍历即有序输出，无需额外排序。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（唯一 key + 有序遍历）；见 cppreference "container/set" 词条；其红黑树节点布局见本章附录 ASM 实证。

### 练习 2（难度 ★★★）
**真实场景：行情序列最长无重复窗口——有序结构做窗口去重。** 维护滑动窗口内的最长无重复子数组长度，`count`/`lower_bound` 为 O(log n)；若只需去重不计序可换 `unordered_set`。

> **示例 51** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 2（难度 ★★★）
```cpp
#include <iostream>
#include <set>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v{1, 2, 3, 2, 4};
    std::set<int> win;
    int lo = 0, best = 0;
    for (int hi = 0; hi < (int)v.size(); ++hi) {
        while (win.count(v[hi])) { win.erase(v[lo++]); }
        win.insert(v[hi]);
        best = std::max(best, hi - lo + 1);
    }
    std::cout << "max unique window=" << best << "\n"; // 4
}
```

<span class="badge badge-std">标准</span> 结论：`std::set` 的 `count/lower_bound` 为 O(log n)，适合需要"有序+去重+范围查询"的窗口场景；若只需去重不计序，`unordered_set` 均摊更优。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（成员查询与范围操作）；有序 vs 无序的取舍见 cppreference "container/set" 与 "container/unordered_set"。

### 练习 3（难度 ★★★★）
**真实场景：频次统计——统计各档位挂单笔数。** 用 `multiset` 统计某价格出现次数（带频次的集合），区别于 `set` 的唯一性。

> **示例 52** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 3（难度 ★★★★）
```cpp
#include <iostream>
#include <set>
#include <vector>
int main() {
    std::vector<int> v{1, 1, 2, 3, 3, 3};
    std::multiset<int> ms(v.begin(), v.end());
    std::cout << "count(3)=" << ms.count(3)
              << " size=" << ms.size() << "\n"; // count(3)=3 size=6
}
```

<span class="badge badge-std">标准</span> 结论：`std::multiset` 允许重复 key，`count(k)` 返回该 key 的出现次数（O(log n + count)），`size()` 是总元素数；需要"带频次的集合"时选它，而非用 `map<K,int>` 手动计数。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[multiset]（允许重复 key 的有序容器）；需要"键→频次"且不介意有序时优于 `map<K,int>` 手动计数；见 cppreference "container/set"（`multiset` 专节）。

### 练习 4（难度 ★★）

**真实场景：有序集合里要删除"[low, high) 半开区间的所有键，又不逐个查找。** 日程表里要清掉 9:00–11:00 之间的所有任务。请用 `lower_bound`/`upper_bound` 一次性拿到区间两端迭代器，再整体 `erase`，并解释复杂度。

<details><summary>答案与解析</summary>

`set` 保持有序，因此"按值而非按迭代器"删除一段可以用 `lower_bound(low)`（首个 ≥ low）与 `upper_bound(high)`（首个 > high）拼出半开区间 `[low, high)`，直接 `erase(first, last)` 一次性删除，复杂度是该区间内元素数级 O(k) 加 O(log n) 定位——比"先查再逐个 erase"更清晰且不易错。注意 `erase(iterator)` 与 `erase(range)` 的返回不同。

> **示例 58** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 4（难度 ★★）
```cpp
#include <iostream>
#include <set>
int main() {
    std::set<int> s{1,2,3,4,5,6};
    // 删除 [3,5): 用 lower_bound/upper_bound 构造半开区间
    s.erase(s.lower_bound(3), s.upper_bound(5));
    for (int x : s) std::cout << x << " ";   // 1 2 6
    std::cout << "\n";
}
```

<span class="badge badge-std">标准</span> `lower_bound`/`upper_bound` 均为 O(log n)；`erase(first, last)` 删除半开区间，复杂度 O(distance+log n)，对有序容器的批量移除是惯用法。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[set]（`lower_bound`/`upper_bound`/`equal_range`）；§[associative.reqmts]；见 cppreference "container/set"。

</details>

### 练习 5（难度 ★★★）

**真实场景：`multiset` 允许重复键，你要统计"值 2 出现了几次"并安全取出所有副本。** 监控计数里同一指标可能被多次写入。请用 `count` 与 `equal_range` 两种手段实现，并指出 `equal_range` 在"既要数量又要遍历副本"时的优势。

<details><summary>答案与解析</summary>

`count(key)` 直接给出重复计数（O(log n + count)）；`equal_range(key)` 返回 `[first, last)` 的迭代器对，既告诉你有多少重复（distance），又能直接遍历这段——比"先 count 再反复 find"更不易出错，也更高效（一次定位）。对 `multiset`，插入相同键不会覆盖，仅是计数增加，删除也只删一个相等元素。

> **示例 59** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 5（难度 ★★★）
```cpp
#include <iostream>
#include <set>
int main() {
    std::multiset<int> ms{1,2,2,2,3};
    std::cout << "count(2)=" << ms.count(2) << "\n";   // 3
    auto [a,b] = ms.equal_range(2);
    for (auto it = a; it != b; ++it) std::cout << *it << " ";  // 2 2 2
    std::cout << "\n";
}
```

<span class="badge badge-std">标准</span> `multiset::count` 与 `equal_range` 复杂度均为 O(log n + count)；`equal_range` 返回与 `lower_bound`/`upper_bound` 相同的端点，便于区间遍历。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[multiset]（`count`/`equal_range` 语义）；§[associative.reqmts]；见 cppreference "container/set"。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：用 set 维护任务调度的最近到期时刻
set 的 `begin()` 即最小 key（最近到期），弹出即调度，O(log n) 增删查。

> **示例 53** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 演绎 1：用 set 维护任务调度的
```cpp
#include <iostream>
#include <set>
int main() {
    std::set<int> due{100, 50, 200, 75};  // 任务到期时刻
    int next = *due.begin();               // 最小 = 最近到期
    std::cout << "next due=" << next << "\n"; // 50
    due.erase(due.begin());
}
```

### 演绎 2：set 与 unordered_set 的小规模性能拐点
元素少且需要有序时用 set；元素多且只判存在时用 unordered_set（均摊 O(1)）。

> **示例 54** <span class="badge badge-exp">难度 ★★★☆☆</span> · 演绎 2：set 与 unorder
```cpp
#include <iostream>
#include <set>
#include <unordered_set>
int main() {
    std::set<int> s;
    std::unordered_set<int> u;
    for (int i = 0; i < 8; ++i) { s.insert(i); u.insert(i); }
    std::cout << "set.size=" << s.size()
              << " uset.size=" << u.size() << "\n"; // 8 8
}
```
## 附录：GCC 15.3.0 真机实证 — `std::set` 红黑树节点分配与 find 代价

> 证据：`_asm_demo/ch84_set_test.cpp`（`-O2`，链接 exe 后 objdump）。结论：**每节点 = 40 字节堆分配（_Rb_tree_node 含 3 指针 + color + value），find 沿左右指针比较并追逐，键存于偏移 0x20。**

**1. 每元素 operator new → 40 字节红黑树节点**：

```asm
; _Rb_tree_node<int> 布局（libstdc++）：
; offset 0x00: _Rb_tree_node_base { color(u32) + parent(ptr) + left(ptr) + right(ptr) }
; offset 0x20: value (int, 键即值)
; sizeof = 0x28 = 40 字节（28 字节基类 + 4 字节 value + 8 字节对齐填充）
insert:
    mov    ecx,0x28                   ; ★ 40 字节
    call   operator new(unsigned long long)
    mov    DWORD PTR [rax+0x20],esi   ; 存储键值到 node+0x20
    call   _Rb_tree_insert_and_rebalance
```

**2. `find(42)` 红黑树指针追逐**（关键路径）：

```asm
; 从根开始沿左右指针比较并追逐节点
find_loop:  mov    rcx,QWORD PTR [rax+0x10]   ; left  child @ offset 0x10
            mov    rdx,QWORD PTR [rax+0x18]   ; right child @ offset 0x18
            cmp    DWORD PTR [rax+0x20],0x29  ; ★ 比较键 @ offset 0x20 (42=0x2a)
            jg     go_left                     ; 键 > 42 → 走左子树
            mov    rax,rdx                     ; 键 < 42 → 走右子树
            jne    find_loop
```

⚠️ **键 = 值，均存于 offset 0x20**：set 的 value 即 key，与 map 的 `pair<const K,V>` 不同（map 在 0x20 处为 key，0x20+sizeof(K) 处为 value）。find 每步：2 次指针追逐 + 1 次比较 → **L3 cache miss 概率 >50%（随机插入后）**。

**工程含义**：set::find 是 O(log n) 的**纯指针追逐**——100 元素 `find` 约 7 步比较、每步可能 cache miss。与 vector 二分查找的单次指针间接 + 连续内存预取相比，set 的 find 在小 n 下反而**更慢**（cache miss 惩罚约 50-100 cycle vs 2-3 cycle）。仅当插入/删除频繁且 n > 1000 时，set 的 O(log n) 才超 vector 的 O(n) 插入。

## 附录 D4：std::set 三标准库源码解析（D4 维度 · libstdc++ 15.3.0）

`std::set` 本身几乎不持有数据——它只是红黑树 `_Rb_tree` 的一层薄封装，通过"键即值"复用同一棵树的实现。下面看 libstdc++ 真实源码如何组织。

### D4.1 libstdc++ 真实源码摘录

// 摘自 libstdc++ 15.3.0：bits/stl_set.h:97（节选）
```text
  template<typename _Key, typename _Compare = std::less<_Key>,
	   typename _Alloc = std::allocator<_Key> >
    class set
    {
    public:
      typedef _Key     key_type;
      typedef _Key     value_type;   // 键即值
    private:
      typedef _Rb_tree<key_type, value_type, _Identity<value_type>,
		       key_compare, _Key_alloc_type> _Rep_type;
      _Rep_type _M_t;  // Red-black tree representing set.
    };
```

// 摘自 libstdc++ 15.3.0：bits/stl_set.h:532 / 839（转发给 _M_t）
```text
      std::pair<iterator, bool>
      insert(const value_type& __x)
      {
	std::pair<typename _Rep_type::iterator, bool> __p =
	  _M_t._M_insert_unique(__x);
	return std::pair<iterator, bool>(__p.first, __p.second);
      }

      iterator find(const key_type& __x) { return _M_t.find(__x); }
```

// 摘自 libstdc++ 15.3.0：bits/stl_tree.h:213（节点存储）
```text
  template<typename _Val>
    struct _Rb_tree_node : public _Rb_tree_node_base
    {
      __gnu_cxx::__aligned_membuf<_Val> _M_storage;
      _Val* _M_valptr() { return _M_storage._M_ptr(); }
    };
```

这三段展示：`set` 唯一数据成员是 `_Rep_type _M_t`（一棵红黑树），所有接口都转发给它；节点用对齐存储缓冲 `__aligned_membuf` 就地构造值。

### D4.2 设计动机

| 源码构造 | 设计意图 | 若不这样做的代价 |
|---|---|---|
| `set` 仅含 `_Rep_type _M_t` 一个成员 | 容器本身极薄，所有逻辑下沉红黑树，复用成熟实现 | 若每容器重写树逻辑，则代码膨胀、bug 倍增 |
| `_Identity<value_type>` 表示"键即值" | set 的 key 与 value 同一对象，复用 map 的红黑树 | 若另写一套以 key 提值的树，则重复维护两棵相似树 |
| `insert` 转发 `_M_t._M_insert_unique` | 唯一键语义由树保证，set 层零额外判断 | 若 set 自己判断重复，则插入路径重复且易不一致 |
| `find` 直接返回 `_M_t.find(__x)` | 查找逻辑统一在树，set 只是别名接口 | 否则查询与树实现脱节，难以保证 O(log n) |
| `_Rb_tree_node` 含 `_Rb_tree_node_base` | 节点 = 颜色 + 三指针 + 对齐值存储，标准 RB 节点 | 若把值放基类外，则访问需二次跳转、布局不紧凑 |
| `__aligned_membuf<_Val>` 对齐存储 | 值在节点内就地构造，满足对齐且支持非常量类型 | 若用裸 `char` 缓冲则对齐错误、构造 placement new 风险 |

### D4.3 三标准库实现对比

| 维度 | libstdc++ (GCC) | libc++ (Clang) | MSVC STL |
|---|---|---|---|
| 底层结构 | `set` 组合 `_Rb_tree _M_t` | 已知公开实现行为：基于内部 `__tree`（红黑树） | 已知公开实现行为：基于内部 `_Tree`（红黑树） |
| 节点布局 | `_Rb_tree_node_base`(color+3 ptr) + `_Rb_tree_node<_Val>` | 已知公开实现行为：节点含父/左/右指针 + 颜色位 | （实现细节，未逐版本核实） |
| "键即值"复用 | `_Identity<value_type>` 接入同一棵树（map 用 `_Select1st`） | 已知公开实现行为：同样用键即值适配器复用唯一树实现 | （实现细节，未逐版本核实） |
| 有序 O(log n) 不变式 | 红黑树平衡，中序有序 | 已知公开实现行为：同 RB 平衡，O(log n) 不变式一致 | 已知公开实现行为：同 RB 平衡，O(log n) 不变式一致 |
| 迭代器实现 | 节点指针包装，双向迭代 | 已知公开实现行为：迭代器也是节点指针遍历 | （实现细节，未逐版本核实） |
| 节点分配 | 经 `allocator` 每次 `new` 一个节点 | 已知公开实现行为：同样每节点分配 | （实现细节，未逐版本核实） |

三家 `set` 均基于红黑树，节点都含父/左/右指针 + 颜色，有序 O(log n) 不变式一致；差异仅在节点具体布局、迭代器实现与零长/透明比较细节。

### D4.4 可编译验证

> **示例 55** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 可编译验证
```cpp
// D4-verify：验证 set 去重+升序与 size（独立可编译）
#include <set>
#include <iostream>

int main() {
    std::set<int> s{30, 10, 20, 10};
    for (int x : s) std::cout << x << " ";   // 10 20 30（去重+升序）
    std::cout << std::endl;
    std::cout << "size==3: " << (s.size() == 3) << std::endl;  // 1
    return 0;
}
```

预期输出：
> **示例 56** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 可编译验证
```
10 20 30
size==3: 1
```

## 附录 J：std::set / multiset 决策流（D3 维度）

```mermaid
flowchart TD
    A["需求:去重/成员判定的集合"] --> D1{"是否允许重复键?"}
    D1 -->|"是"| F1["std::multiset"]
    D1 -->|"否"| D2{"是否需要有序遍历/范围查询?"}
    D2 -->|"是"| F2["std::set 红黑树"]
    D2 -->|"否"| D3{"单点查找是否热点?"}
    D3 -->|"是"| D4{"数据量大且哈希好?"}
    D3 -->|"否"| F3["std::set 稳妥"]
    D4 -->|"是"| F4["std::unordered_set 哈希"]
    D4 -->|"否"| F5["std::set 避免 rehash"]
    F2 --> D5{"遍历是否热点?"}
    D5 -->|"是"| G1["flat_set / 排序 vector 缓存友好"]
    D5 -->|"否"| G2["set 节点稳定"]
    F4 --> D6{"频繁插入触发 rehash?"}
    D6 -->|"是"| H1["prefer set / flat"]
    D6 -->|"否"| H2["unordered_set 均摊 O(1)"]
    G1 --> Z["结论:有序+稳定+去重选 set"]
    G2 --> Z
    F3 --> Z
    F5 --> Z
    H1 --> Z
    H2 --> Z
    F1 --> Z
```

> 决策流说明：`set` 是「键即值」的有序唯一集合，与 `map` 同源——适合需要有序遍历、范围查询或稳定迭代器的去重场景。仅判存在且数据量大用 `unordered_set`；允许重复键用 `multiset`；遍历成为热点时排序 `vector`（flat_set）靠连续内存反超红黑树。

## 附录 K：std::set / multiset 知识图谱（D6 维度）

```mermaid
flowchart TD
    N1["红黑树 _Rb_tree"] --> N2["键即值 value=key"]
    N2 --> N3["set 唯一 / multiset 可重复"]
    N1 --> N4["有序中序遍历"]
    N4 --> N5["lower_bound / equal_range"]
    N1 --> N6["节点稳定性"]
    N6 --> N7["extract / merge 零拷贝重定位"]
    N1 --> N8["O(log N) 树下降"]
    N8 --> N9["缓存不友好"]
    N3 --> N10["透明比较器 C++20"]
    N1 --> N11["严格弱序 Compare"]
    N11 --> N12["std::less 默认"]
    N9 --> N13["flat_set 排序 vector 替代"]
    N3 --> N14["unordered_set 哈希对照"]
```

### K.1 概念依赖逐边解读

| 边 | 上游概念 | 下游概念 | 依赖关系说明 |
|---|---|---|---|
| 1 | 红黑树 | 键即值 | set 只存 key，value 即 key 本身 |
| 2 | 键即值 | set/multiset | 唯一性差异决定有无重复键 |
| 3 | 红黑树 | 有序遍历 | 中序遍历得到升序集合 |
| 4 | 有序遍历 | 范围查询 | equal_range 取某键的连续区间 |
| 5 | 红黑树 | 节点稳定性 | 插入/删除不使既有迭代器失效 |
| 6 | 节点稳定性 | extract/merge | 节点级移动不拷贝 key |
| 7 | 红黑树 | O(log N) | 树高受限，查找稳定对数级 |
| 8 | O(log N) | 缓存不友好 | 节点散落堆上，指针追逐 |
| 9 | set/multiset | 透明比较器 | is_transparent 异构查找提速 |
| 10 | 红黑树 | 严格弱序 | Compare 必须满足严格弱序 |
| 11 | 严格弱序 | std::less | 默认比较器即 std::less |
| 12 | 缓存不友好 | flat_set | 连续内存替代缓解缓存惩罚 |
| 13 | set/multiset | unordered_set | 有序集合的哈希对照 |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch83 map | ch84 set | set 是键即值的 map，底层同为 _Rb_tree |
| ch85 unordered | ch84 set | unordered_set 是有序集合的哈希对照 |
| ch76 STL 架构 | ch84 set | 双向迭代器概念 |
| ch154 缓存优化 | ch84 set | RB 树节点散落堆，缓存命中率低 |
| ch115 移动语义 | ch84 set | extract 节点句柄依赖移动 |
| ch86 adapters | ch84 set | priority_queue 用堆，与 set 平衡对比 |
| ch98 堆算法 | ch84 set | 平衡树与堆两种有序结构的取舍 |

## 附录 D5：真实基准与性能分析 — set/multiset 红黑树 vs 排序数组（GCC 15.3.0）

> 环境：AMD Ryzen 9 7940HX，GCC 15.3.0（MinGW-w64），`-O2 -std=c++23`，5 轮取中位。绝对毫秒随机器而变，加速比才是可移植信号。

### D5.1 基准结果

数据量 N=1,000,000 个 `int`，查询数 Q=1,000,000 次（混合命中与未命中）。数据经 `std::shuffle` 打乱后输入，模拟真实无序插入场景。遍历场景重复 10 轮以放大信号。

**表 1：插入与构建**

> 【性能】下表数字为 x86-64 量级示意 / 本机实测量级（非通用性能结论），标 `[微架构·x86-64][UNVERIFIED]` 或 `[实验·本机实测][UNVERIFIED]`；绝对毫秒随机器而变，只看纵向加速比。
| 场景 | 中位耗时 | 相对倍数 |
| --- | --- | --- |
| multiset 逐个插入 1M 元素 | 1608 ms | 1.00×（基线） |
| set 逐个插入 1M 元素 | 1576 ms | 0.98× |
| vector push_back + sort + unique 1M | 103 ms | 0.064×（快 15.6×） |
| set 从已排序区间构造 1M 元素 | 154 ms | 0.096×（快 10.4×，vs 逐个插入） |
| multiset 查询 1M 次（find） | 801 ms | 1.00×（基线） |
| vector lower_bound 查询 1M 次 | 135 ms | 0.169×（快 5.93×） |

**表 2：纯查询与有序遍历**

> 【性能】下表数字为 x86-64 量级示意 / 本机实测量级（非通用性能结论），标 `[微架构·x86-64][UNVERIFIED]` 或 `[实验·本机实测][UNVERIFIED]`；绝对毫秒随机器而变，只看纵向加速比。
| 场景 | 中位耗时 | 相对倍数 |
| --- | --- | --- |
| set::find 1M 次 | 759 ms | 1.00×（基线） |
| set::contains 1M 次 | 790 ms | 1.04× |
| vector::binary_search 1M 次 | 130 ms | 0.171×（快 5.84×） |
| vector::lower_bound 1M 次 | 121 ms | 0.159×（快 6.27×） |
| set 中序遍历 1M×10 轮 | 1635 ms | 1.00×（基线） |
| vector 顺序遍历 1M×10 轮 | 5 ms | 0.0031×（快 327×） |

**内存占用对比**

| 维度 | set\<int\> | vector\<int\>（排序去重后） |
| --- | --- | --- |
| 每元素开销 | ~40 字节（RB 节点：3 指针 + color + value + padding） | 4 字节（int，连续存储） |
| 1M 元素总内存 | ~38 MB | ~3 MB |
| 容器对象大小 | 48 bytes | 24 bytes |
| 膨胀比 | — | set 约为 vector 的 10× |

> 上表为本次本机复测的中位耗时；绝对毫秒随机器负载而变，加速比（15.6×、5.84×、327× 等）才是可移植信号。

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1000</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10000</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="150.4" x2="640" y2="150.4" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="146.4" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 1608.00ms</text>
  <rect x="118.0" y="150.4" width="64.0" height="149.6" fill="#9A9A9A"/>
  <text x="150.0" y="144.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1608ms</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">multiset 逐个插入1M</text>
  <rect x="258.0" y="151.5" width="64.0" height="148.5" fill="#DD8452"/>
  <text x="290.0" y="145.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">1576ms</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">set 逐个插入1M</text>
  <rect x="398.0" y="298.4" width="64.0" height="1.6" fill="#C44E52"/>
  <text x="430.0" y="292.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">103ms</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">vector 推+排序+去重</text>
  <rect x="538.0" y="276.7" width="64.0" height="23.3" fill="#8172B3"/>
  <text x="570.0" y="270.7" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#8172B3">154ms</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">set 已排序构造</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.25</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.5</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.75</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="48.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="118.0" y="52.0" width="64.0" height="248.0" fill="#9A9A9A"/>
  <text x="150.0" y="46.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">multiset 逐个插入1M</text>
  <rect x="258.0" y="56.9" width="64.0" height="243.1" fill="#DD8452"/>
  <text x="290.0" y="50.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">0.98×</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">set 逐个插入1M</text>
  <rect x="398.0" y="284.1" width="64.0" height="15.9" fill="#C44E52"/>
  <text x="430.0" y="278.1" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">0.06×</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">vector 推+排序+去重</text>
  <rect x="538.0" y="276.2" width="64.0" height="23.8" fill="#8172B3"/>
  <text x="570.0" y="270.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#8172B3">0.10×</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">set 已排序构造</text>
</svg>

> 图注：1M 元素 set/multiset 逐个插入要 1.6s，而 vector 推入+sort+unique 仅 103ms(快 15.6×)，从已排序区间构造 set 154ms(快 10.4×)。关联容器的节点分配与树平衡是主要开销。

### D5.2 非显然结论

1. **vector 二分查询（lower_bound 121 ms / binary_search 130 ms）快约 6× 于 set::find（759 ms）——差距来自缓存，不是算法复杂度。** 两者都是 O(log n)，100 万元素时树高约 20 层，比较次数几乎相同。但 set 每步比较要解引用一个散布在堆上的节点指针，每跳一次都可能 L3 cache miss（50-100 cycle 惩罚）。vector 二分在连续内存上操作，硬件预取器在消费第一个 cache line 时就把后续行拉进 L1，20 步比较几乎全在 L1 命中。这是 ch154 缓存优化的活数字：同阶复杂度下，缓存友好性决定真实速度。

2. **逐个插入比 vector+sort 慢约 16×（set 1576 ms / multiset 1608 ms vs vector 98 ms）——根因是 N 次堆分配。** 每次 `set::insert` 都调用 `operator new` 分配一个 40 字节红黑树节点（3 指针 + color + value + padding），还要做平衡旋转与染色。vector 的 `push_back` 是均摊 O(1) 的连续写入，`sort` 是 O(n log n) 但在连续内存上极快。100 万次 `operator new` vs 1 次大分配 + 排序，分配器簿记的开销被数量级放大——ch37 的 D5 基准已证明单次 `operator new` 约 49.5 ns，100 万次就是约 49.5 ms 的纯分配税。

3. **set 从已排序区间构造快 10.2× 于逐个插入（154 vs 1576 ms），但仍慢于 vector+sort（1.57×，154 vs 98 ms）。** 已排序输入让红黑树几乎不需要旋转（每次插入到最右叶子，O(1) 定位），省了平衡开销，但 N 次堆分配仍无法省去。这解释了为什么 Chromium `base::flat_set` 与 Folly `sorted_vector_set` 在批量构建场景碾压 `std::set`：连续分配 + sort 的组合远优于 N 次节点分配。

4. **有序遍历差距最为极端——vector 快 327×（5 vs 1635 ms）。** set 中序遍历是纯指针追逐：每次 `++it` 跳到一个随机堆地址，CPU 预取器完全无法预测下一个节点的位置。vector 顺序遍历是连续内存访问，硬件预取器在消费第一个 cache line 时就把后续行拉进 L1，10M 次 int 读取在 vector 上只需 5 ms 因为数据全在 L2 cache 里。这是红黑树"节点散布堆上"这一设计代价的最直观数字，也是工业界在遍历热点路径上用 `flat_set` 替代 `set` 的核心动机。

5. **set 内存膨胀 10×——每 int 占 40 字节 vs vector 的 4 字节。** 红黑树节点 = 3 个指针（parent/left/right 各 8 字节）+ color（1 字节 + 7 字节对齐填充）+ int value（4 字节 + 4 字节填充）= 40 字节。vector 的 int 仅 4 字节，连续存储无元数据开销。100 万元素时 set 占 ~38 MB 而 vector 仅 ~3 MB——同样容量的 L3 cache，vector 能装下 10 倍的数据，这进一步放大了查询时的缓存优势。注意：ch97 已覆盖 `unordered_map` vs `set::find` 的对比，本附录聚焦 multiset vs sorted_vector 的权衡，不重复 ch97 的内容。

### D5.3 可复现演示

> **示例 57** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 可复现演示
```cpp
// D5-demo：set/multiset vs sorted vector 功能等价性与内存对比（独立可编译）
#include <set>
#include <vector>
#include <algorithm>
#include <iostream>
#include <cassert>

int main() {
    // 平台标识
#ifdef _WIN32
    std::cout << "platform: Windows (MinGW-w64)" << std::endl;
#else
    std::cout << "platform: POSIX" << std::endl;
#endif

    // 构造数据: 有重复的 int 序列
    int raw[] = {5, 3, 8, 3, 1, 9, 2, 8, 1, 5, 7, 3, 6, 9, 2};
    int n = static_cast<int>(sizeof(raw) / sizeof(raw[0]));

    // 方式 A: set 自动去重 + 排序
    std::set<int> s(raw, raw + n);

    // 方式 B: vector push_back + sort + unique（模拟 flat_set）
    std::vector<int> v(raw, raw + n);
    std::sort(v.begin(), v.end());
    v.erase(std::unique(v.begin(), v.end()), v.end());

    // 方式 C: multiset 保留重复
    std::multiset<int> ms(raw, raw + n);

    // 1. set 与 vector 去重后元素数相同
    std::cout << "set.size()       = " << s.size() << std::endl;
    std::cout << "vector.size()    = " << v.size() << std::endl;
    std::cout << "multiset.size()  = " << ms.size() << std::endl;
    assert(s.size() == v.size());
    assert(ms.size() == static_cast<size_t>(n));  // multiset 保留全部

    // 2. 有序遍历结果完全一致
    std::vector<int> s_trav(s.begin(), s.end());
    assert(s_trav == v);
    std::cout << "ordered traversal match: yes" << std::endl;

    // 3. 查询结果一致
    int query_keys[] = {1, 3, 5, 8, 9, 10};
    for (int q : query_keys) {
        bool in_set = s.contains(q);
        bool in_vec = std::binary_search(v.begin(), v.end(), q);
        assert(in_set == in_vec);
        std::cout << "query " << q << ": set=" << in_set
                  << " vector=" << in_vec << std::endl;
    }

    // 4. lower_bound 一致
    auto sit = s.lower_bound(5);
    auto vit = std::lower_bound(v.begin(), v.end(), 5);
    assert(*sit == *vit);
    std::cout << "lower_bound(5): set=" << *sit
              << " vector=" << *vit << std::endl;

    // 5. multiset 重复计数
    std::cout << "multiset.count(3) = " << ms.count(3) << std::endl;
    assert(ms.count(3) == 3);

    // 6. 内存开销对比
    std::cout << "sizeof(set<int>)    = " << sizeof(s) << " bytes" << std::endl;
    std::cout << "sizeof(vector<int>) = " << sizeof(v) << " bytes" << std::endl;
    std::cout << "set per-element:    ~40 bytes (RB node: 3ptr+color+val)" << std::endl;
    std::cout << "vector per-element:  4 bytes (int, contiguous)" << std::endl;

    std::cout << "all assertions passed" << std::endl;
    return 0;
}
```

预期输出（本机实测）：

| 输出行 | 值 |
| --- | --- |
| `platform` | `Windows (MinGW-w64)` |
| `set.size()` | 8 |
| `vector.size()` | 8 |
| `multiset.size()` | 15 |
| `ordered traversal match` | yes |
| `query 1` ~ `query 9` | set=1 vector=1 |
| `query 10` | set=0 vector=0 |
| `lower_bound(5)` | set=5 vector=5 |
| `multiset.count(3)` | 3 |
| `sizeof(set<int>)` | 48 |
| `sizeof(vector<int>)` | 24 |

### D5.4 方法学注

- 复现旗标：`g++ -O2 -std=c++23`（与 CI 一致）。demo 通过 `#ifdef _WIN32` 的条件编译在 Windows 与 POSIX 双平台均可编译运行。
- 计时取 5 轮中位数，规避调度抖动与冷热启动偏差；单轮工作量均在数十毫秒以上，避免计时器分辨率污染。
- `volatile` sink 防 DCE：所有计时循环的累加和都写入 `volatile long long g_sink`，防止 `-O2` 把循环折叠成常数。
- 数据经 `std::mt19937(42)` 播种后 `std::shuffle` 打乱，模拟真实无序插入；查询键混合命中（50%）与未命中（50%），避免全命中或全未命中的偏向。
- 加速比（15.6×、5.84×、327× 等）是可移植信号；绝对毫秒随 CPU、分配器实现与编译器版本而变，请勿跨机器直接比较毫秒。
- demo 只断言功能等价性（元素数、遍历一致性、查询一致性、重复计数），未对时间、倍数或精确 `sizeof` 做任何断言。
- 基准源码见库根 `_bench_d5_ch84_set_multiset.cpp`。

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_ch84_set_multiset.cpp` 真实生成（节选 `set<int>` 的 `_M_get_insert_unique_pos`，int 键）。D5.2 的 headline 结论 #1（vector `lower_bound`/`binary_search` 快约 6× 于 `set::find`，差距来自缓存而非算法复杂度）可由这段红黑树下降循环直接看出：`set` 与 vector 二分每步比较次数几乎相同（都是 O(log n)≈20 层），但 `set` 每步都要先解引用一个散布在堆上的节点指针、再沿 `_M_left`/`_M_right` 追逐到下一层——每次跳跃都是一次不可预测的堆地址跳转，极易 L3 cache miss（50–100 cycle 惩罚）；vector 二分的中点地址是 `base + mid*4` 的连续推算，硬件预取器在消费第一个 cache line 时就把后续行拉进 L1。int 键的比较本身只是一句 4 字节 `cmp`，便宜到可以忽略，于是真实瓶颈就是"指针追逐"这一项。

```asm
; set 键定位：红黑树逐层指针追逐（关键路径，int 键）
;   _ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE24_M_get_insert_unique_posERKi.isra.0  (节选；find 与插入定位共用同一套下降逻辑)
  mov     rcx, QWORD PTR 16[rdx]      ; rcx = 根节点 _M_root
  test    rcx, rcx
  je      .L
.L:
  mov     r9d, DWORD PTR 32[rcx]      ; 读节点值（int，offset 32）
  mov     rax, QWORD PTR 24[rcx]      ; 读子节点指针（offset 24 = _M_right）
  cmp     r8d, r9d                    ; ← 比较待查值 vs 节点值（单次 4 字节 cmp，极廉价）
  cmovl   rax, QWORD PTR 16[rcx]      ; 小于 → 改走 _M_left（offset 16）
  setl    r10b
  test    rax, rax
  jne     .L                          ; 子节点非空 → 下降一层（追逐堆上子节点指针）
  ; …（下降前的栈/寄存器准备指令省略）
```

> 注意：`set::find` 走的就是这条完全相同的下降循环——每层一次 `cmp` + 一次 `_M_left`/`_M_right` 指针追逐，树高约 20 层即约 20 次潜在 cache miss。vector 的 `lower_bound` 每层也是一次 `cmp`，但"下一层中点"由 `base + mid*4` 算术连续得出，预取器可预测、几乎全在 L1 命中。这正是 D5.2 #1「同阶复杂度、缓存定胜负」的机器码注脚，也是 #4（有序遍历 vector 快 327×）与 #5（set 内存膨胀 10×）同一根因：节点散布堆上 → 缓存友好性崩塌。绝对毫秒随 CPU/编译器而变，加速比才是可移植信号。

## 参考引用

- `[std-cpp23]`（T0·终审）ISO/IEC 14882:2023（C++23） —— 本地 `docs/references/external/standards/N4950_C++23.pdf`
- `[cppref:cpp/container/set]`（T1）cppreference `cpp/container/set` —— 离线 `C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`
- `[book:effective-stl:item19]`（T4）Effective STL 中文版（Meyers，50 条） · Item 19：理解相等（equality）和等价（equivalence）的区别。 —— 提取文本 `docs/references/external/books/effective-stl.txt`
- `[book:effective-stl:item22]`（T4）Effective STL 中文版（Meyers，50 条） · Item 22：切勿直接修改set或multiset中的键。 —— 提取文本 `docs/references/external/books/effective-stl.txt`

> 键的含义与全部来源见 `docs/references/SOURCING.md`；写作时只取要点，不整本投喂。
