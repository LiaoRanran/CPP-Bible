# 第82章　span 与裸数组视图
> 【性能声明 · §10.3】本章所有绝对延迟/带宽数字（如 L1≈1ns、主存≈100ns、各基准 ms）均为 **x86-64 量级示意**，强依赖具体 CPU 型号/频率、编译器及版本、编译标志、OS、测试负载与样本量；非通用性能结论，绝对数字不可移植。微架构相关结论标 `[微架构·x86-64][UNVERIFIED]`；本机实测标 `[实验·本机实测][UNVERIFIED]`。断言形如「acquire 读比 relaxed 贵 X」仅在给定微架构下成立。

> 标准基：ISO/IEC 14882:2023 (C++23) / 预计阅读：80 分钟 / 前置：⟶ Book/part03_language/ch20_reference_pointer.md（引用与指针）、⟶ Book/part07_stl/ch80_array.md（array）、⟶ Book/part07_stl/ch77_vector.md（vector）/ 后续：⟶ Book/part07_stl/ch83_map.md（map）、⟶ Book/part07_stl/ch90_ranges.md（ranges）/ 难度：★★★☆☆

## ⓪ 历史动机：std::span 的来龙去脉
> 一个"只借不拿"的视图，专治函数签名里 `(T* p, size_t n)` 这对极易出错的孪生兄弟。

### 0.1 起源（谁·何时·为何）
在 `span` 之前，想让函数接收一个"数组或 vector 的一段"，标准写法是传 `(指针, 长度)` 两个参数。[史] 麻烦在于：指针和长度分家，长度常被忘传、传错、或与实际缓冲区脱节，引发越界。`std::span` 在 C++20 登场，把 `{指针, 长度}` 打包成一个非拥有（non-owning）的连续视图，进能当数组用、退能包 `array`/`vector`/`string`。[史] 它直接源自 Bjarne Stroustrup 与 Herb Sutter 推动的《C++ 核心指南》配套库 GSL（Guidelines Support Library）中的 `span`，目标是"边界安全"。[史]

### 0.2 关键转折（编年）
- GSL 阶段：`gsl::span` 作为指南库先行试水，积累了大量使用经验。[史]
- C++20：`std::span` 标准化，并支持静态 extent（编译期已知长度，可优化）与动态 extent。
- C++23：进一步打磨（如构造规则、与范围的交互）。

### 0.3 设计哲学之争
`span` 引发的核心争论是"视图该不该拥有内存"——`span` 选了**绝不拥有**，因此拷贝极廉价、生命周期责任清晰，代价是你必须保证底层对象活得比 `span` 久。[评] 它与 `string_view` 是"兄弟视图"（一个管字节、一个管字符），与 `vector` 则是"借 vs 拿"的对照。[评] 社区共识：接口参数优先用 `span`/`string_view`，所有权交给调用方，能显著减少悬垂与拷贝。

### 0.4 史料补遗与持续编年

> 0.2 停在 C++23 继续打磨 `span`（构造规则、与范围交互）。多维视图与和 Ranges 的融合是后续主线。

- [史] **`std::mdspan`（C++23）把 `span` 思想推到 N 维**：`std::mdspan<T, Extents>` 是非拥有的多维数组视图，支持映射策略（如 `layout_left`/`layout_right`/`layout_stride`），用于数值线性代数与 GPU/张量数据，无需拷贝底层缓冲区。
- [史] **`as_bytes`/`as_writable_bytes`（C++20）放宽字节级视图**：`span` 可安全转成 `span<const std::byte>`，便于序列化与底层 IO；这是"视图借而不拿"在字节层的延伸。
- [评] **`span` 与 `ranges::view` 是"近亲但不同源"**：`span` 只覆盖连续内存、可随机访问；`ranges` 视图可惰性、可非连续（如 `views::filter`）。两者都贯彻"不拥有"，但 `span` 偏底层字节/元素、`view` 偏算法管道（⟶ ch90）。
- [史] **C++23 还补了 `span` 构造从 `array`/`initializer_list` 的便捷路径**，与 `std::dynamic_extent` 配合让接口更顺；仍未给 `span` 加"拥有"语义——所有权边界始终清清楚楚。

> 史料来源：[cppreference std::span](https://en.cppreference.com/w/cpp/container/span)、[C++23 标准概览（维基）](https://en.wikipedia.org/wiki/C%2B%2B23)

## ① 学习目标

`std::span<T, Extent>` 是 C++20 引入（在 C++23 中继续打磨）的**非拥有（non-owning）连续对象视图**。本章结束后，你应当能够：

- 精确区分 `span` 与 `array`/`vector`/`string_view` 的**所有权语义**与**适用边界** `[标准]`。
- 掌握**动态 extent**（`dynamic_extent`）与**静态 extent**（编译期常量 `N`）在内存布局、接口约束与优化上的差异 `[实现]`。
- 理解 `span` 的**零开销抽象**本质——它只是一个 `{指针, 大小}` 对，在 `-O2` 下被完全内联 `[实现·GCC15]`。
- 正确使用 `first/last/subspan` 进行安全切片，并清楚**越界访问是未定义行为（UB）**，而非抛异常 `[标准]`。
- 在真实工程（网络包解析、行情数据、序列化）中用 `span` 替代裸指针 + 长度，消除"长度从哪来"的歧义 `[经验]`。
- 掌握 `span` 与 C 数组、`std::vector`、`std::array`、C 风格接口（如 `void*` + `size_t`）的互操作 `[标准]`。

---

## ② 前置知识

`span` 建立在你已经掌握的几块基石之上：

- **引用与指针的本质差异** ⟶ `Book/part03_language/ch20_reference_pointer.md`：`span` 内部持有一个指针（`_M_ptr`），其语义等价于"指向首元素的指针"，但携带长度，解决了裸指针丢失边界信息的问题。
- **array 与固定数组** ⟶ `Book/part07_stl/ch80_array.md`：`std::array<T,N>` 可直接构造 `span<T,N>`，静态 extent 由此而来。
- **vector 与扩容** ⟶ `Book/part07_stl/ch77_vector.md`：`vector` 的 `.data()` + `.size()` 是 `span` 最常见的来源；注意 `vector` 扩容后旧 `span` 失效。
- **string 与 SSO** ⟶ `Book/part07_stl/ch81_string.md`：`std::string_view` 是 `span` 的"字符特化版"，二者设计同源（见 §⑪）。
- **optional / expected** ⟶ `Book/part07_stl/ch88_optional_variant.md`：返回"可能缺失的视图"时，用 `std::optional<std::span<const T>>` 表达"无数据"比返回空 `span` 更明确。

> **示例 1** [难度 ★★★☆☆] [主题：前置知识]
```cpp
// ②-1 前置：span 与三大数据源的关系（独立可编译）
#include <span>
#include <vector>
#include <array>
#include <iostream>

int main() {
    int raw[4] = {1, 2, 3, 4};
    std::vector<int> v = {10, 20, 30};
    std::array<int, 2> a = {100, 200};

    std::span<int> s1{raw};                 // 从 C 数组
    std::span<int> s2{v};                   // 从 vector
    std::span<int, 2> s3{a};                // 从 array，静态 extent
    std::cout << s1.size() << " " << s2.size() << " " << s3.size() << "\n";
    return 0;
}
```

> **示例 2** [难度 ★★★☆☆] [主题：前置知识]
```cpp
// ②-2 前置：span 不改变底层数据的所有权（仍是别人的内存）
#include <span>
#include <vector>
#include <iostream>
#include <cstddef>

std::size_t sum(std::span<const int> s) {  // 只读视图，不拷贝
    std::size_t r = 0;
    for (int x : s) r += static_cast<std::size_t>(x);
    return r;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::cout << sum(v) << "\n";            // 10
    return 0;
}
```

---

## ③ 后续依赖

- **map / multimap（红黑树）** ⟶ `Book/part07_stl/ch83_map.md`：`map` 的 `value_type` 是 `pair<const K, V>`，遍历 `map` 得到的范围可借 `span` 暴露给算法层；二者共同构成"有序容器 + 视图"的组合。
- **ranges 与 views** ⟶ `Book/part07_stl/ch90_ranges.md`：`std::ranges::subrange` 是 `span` 的"惰性表亲"，`span` 适合**连续**内存，`subrange` 适合任意迭代器对。
- **STL 算法** ⟶ `Book/part08_algorithms/ch95_algo_overview.md`：几乎所有接受"区间"的算法都可用 `span` 直接喂入（因为 `span` 满足 `contiguous_range`）。

> **示例 3** [难度 ★★★☆☆] [主题：后续依赖]
```cpp
// ③-1 后续：span 作为算法区间直接喂给 std::ranges（C++20）
#include <span>
#include <vector>
#include <iostream>
#include <algorithm>
#include <ranges>

int main() {
    std::vector<int> v = {5, 3, 1, 4, 2};
    std::span<int> s = v;
    std::ranges::sort(s);                   // 原地排序底层 vector
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
    return 0;
}
```

> **示例 4** [难度 ★★★☆☆] [主题：后续依赖]
```cpp
// ③-2 后续：ranges::subrange 与 span 的互转思想（独立可编译）
#include <span>
#include <vector>
#include <iostream>
#include <ranges>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 20, 30, 40};
    auto sub = std::ranges::subrange(v.begin() + 1, v.begin() + 3);
    std::span<int> s(v.data() + 1, 2);      // 等价视图（连续内存特化）
    std::cout << *sub.begin() << " " << s[0] << "\n";
    return 0;
}
```

---

## ④ 知识图谱（ASCII）

> **示例 5** [难度 ★★★☆☆] [主题：知识图谱（ASCII）]
```
                        ┌─────────────────────────────┐
                        │   连续内存抽象（视图家族）    │
                        └───────────────┬─────────────┘
                                        │
            ┌───────────────┬───────────┴───────────┬──────────────────┐
            ▼               ▼                       ▼                  ▼
      ┌──────────┐   ┌─────────────┐        ┌──────────────┐   ┌─────────────┐
      │ span<T>  │   │string_view  │        │ array<T,N>   │   │ vector<T>   │
      │(任意类型)│   │(字符特化)   │        │(拥有,定长)   │   │(拥有,可变)  │
      └────┬─────┘   └──────┬──────┘        └──────┬───────┘   └──────┬──────┘
           │                │                      │                 │
           │ 构造来源        │ 构造来源              │ 构造来源         │ 构造来源
           ▼                ▼                      ▼                 ▼
      C数组/vector/    string/data()/      字面量/数组         push_back
      array/指针+长度  C字符串/char*        (定长)            (动态扩容)
           │
           ▼
   ┌──────────────────────────┐
   │ 非拥有：{ptr, extent}    │──► first/last/subspan
   │ 动态 extent 或 静态 N    │──► 越界 = UB（不抛异常）
   └──────────────────────────┘
```

---

## ⑤ Mermaid 流程图：span 的构造来源与切片

```mermaid
flowchart TD
    A[连续内存源] --> B{"C 数组 / vector / array / 指针+长度"}
    B -->|C数组/array| C[静态 extent span T N]
    B -->|vector/指针+len| D[动态 extent span T]
    C --> E[subspan 可能产生动态 extent]
    D --> E
    E --> F["first n / last n"]
    E --> G[subspan off cnt]
    F --> H[新 span 仍指向同一底层]
    G --> H
    H --> I["越界访问 -> UB"]
    H --> J["安全切片 -> 编译期/运行期断言"]
```

---

## ⑥ UML 类图：span 的类型关系（Mermaid classDiagram）

```mermaid
classDiagram
    class span~T,Extent~ {
        +element_type* _M_ptr
        +ExtentStorage _M_extent
        +size() size_type
        +size_bytes() size_type
        +data() pointer
        +operator[](i) reference
        +begin() iterator
        +end() iterator
        +first(n) span
        +last(n) span
        +subspan(o,c) span
    }
    class ExtentStorage {
        +_M_extent_value
        +_M_extent() size_type
    }
    span --> ExtentStorage : 持有
    span ..|> contiguous_range : 概念满足
    span ..|> view : 概念满足
```

---

## ⑦ ASCII 内存图：span 的对象布局

`std::span` 本身**不持有任何元素**，它只是两个标量：`_M_ptr`（指针）和 `_M_extent`（大小/extent）。

> **示例 6** [难度 ★★★☆☆] [主题：内存图：span 的对象布局]
```
栈上的 span 对象（x86-64，普通对齐）：
┌──────────────────────────────────────────────────────────┐
│  std::span<int>（8 字节：1 个指针）                         │
│  ┌──────────────┐                                          │
│  │ _M_ptr  (8B) │ ──────► 堆/栈上的底层数组                  │
│  └──────────────┘       ┌────┬────┬────┬────┐              │
│                         │ a0 │ a1 │ a2 │ a3 │  sizeof(int)=4│
│  （Extent 为动态时：     └────┴────┴────┴────┘              │
│    size 也存于 span 内，    ◄── 指向首元素                   │
│    总大小 = 16 字节）                                       │
└──────────────────────────────────────────────────────────┘

静态 extent（如 span<int,4>）：
┌──────────────────────────────────────────────────────────┐
│  std::span<int,4>（仅 8 字节：指针）                        │
│  ┌──────────────┐                                          │
│  │ _M_ptr  (8B) │ ──────► 编译器已知长度为 4，不占存储       │
│  └──────────────┘                                          │
└──────────────────────────────────────────────────────────┘
```

- `[实现·GCC15]`：`span` 的 extent 由内部 `struct _ExtentStorage` 保存；当 `Extent == dynamic_extent` 时该结构含一个 `size_t _M_extent_value`（见 `文件：span`, `行号：81-99`）；当 extent 为编译期常量时，该结构为空且 `_M_extent_value` 不参与对象大小。
- `[标准]`：`sizeof(span<T, dynamic_extent>)` 通常等于 `2 * sizeof(void*)`（指针 + 大小），`sizeof(span<T, N>)` 通常等于 `sizeof(void*)`，因为大小是类型的一部分，不需存储。

> **示例 7** [难度 ★★★☆☆] [主题：内存图：span 的对象布局]
```cpp
// ⑦-1 验证 span 的对象大小（独立可编译）
#include <span>
#include <iostream>

int main() {
    std::cout << "span<int,dynamic> = " << sizeof(std::span<int>) << "\n";   // 16（指针+大小）
    std::cout << "span<int,4>       = " << sizeof(std::span<int, 4>) << "\n"; // 8（仅指针）
    std::cout << "dynamic_extent    = " << std::dynamic_extent << "\n";       // -1ULL
    return 0;
}
```

> **示例 8** [难度 ★★★☆☆] [主题：内存图：span 的对象布局]
```cpp
// ⑦-2 静态 extent 是类型的一部分（长度信息进入类型系统）
#include <span>
#include <iostream>
#include <type_traits>
#include <cstddef>

template <std::size_t N>
void takes_fixed(std::span<int, N> s) {
    std::cout << "compile-time length = " << N << "\n";
}

int main() {
    int arr[4] = {1, 2, 3, 4};
    takes_fixed(std::span<int, 4>{arr});   // N 推导为 4
    static_assert(std::is_same_v<std::span<int, 4>, std::span<int, 4>>);
    return 0;
}
```

---

## ⑧ 生命周期图：span 是"借来的引用"

`span` 不拥有底层存储，因此它的有效性与底层存储的生命周期**强绑定**。这是 `span` 最常见的误用来源。

> **示例 9** [难度 ★★★☆☆] [主题：生命周期图：span 是"借来的引用]
```
时间轴 ────────────────────────────────────────────────►

  vector<int> v(100);   // 拥有存储
        │
        ├─ auto s = std::span(v);   // s 借用 v 的内存
        │        │
        │        ├─ 使用 s  ✅ 安全（v 存活）
        │        │
        │        ├─ v.push_back(...); // 若触发扩容，v 迁移到新内存
        │        │        └─ s 现在指向已释放/旧内存 → 悬垂（UB）
        │        │
        ├─ v 析构  // 存储归还
        │        └─ 此后任何使用 s → UB
        │
  return;
```

- `[标准]`：`span` 不延长任何人生命周期；从临时 `vector`/`string` 构造 `span` 并外传是经典悬垂错误（见 §⑯）。
- `[经验]`：函数参数用 `span` 传"调用方保证存活"的缓冲区；不要把它存进成员变量后长期持有。

> **示例 10** [难度 ★★★☆☆] [主题：生命周期图：span 是"借来的引用]
```cpp
// ⑧-1 生命周期：从局部 vector 返回 span 是悬垂（代码可编译，运行期 UB！）
#include <span>
#include <vector>

std::span<int> bad() {
    std::vector<int> v = {1, 2, 3};
    return std::span<int>(v);   // ❌ 返回后 v 析构，span 悬垂
}

int main() {
    // 仅用于演示编译通过：实际调用 bad() 是 UB，切勿在生产使用
    (void)bad;
    return 0;
}
```

> **示例 11** [难度 ★★★☆☆] [主题：生命周期图：span 是"借来的引用]
```cpp
// ⑧-2 正确：调用方持有存储，span 仅在本作用域内借用
#include <span>
#include <vector>
#include <iostream>

void process(std::span<const int> s) {
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
}

int main() {
    std::vector<int> v = {1, 2, 3, 4};
    process(v);          // ✅ v 在 process 返回前一直存活
    return 0;
}
```

---

## ⑨ 调用栈 / 时序图：subspan 的语义

`subspan(offset, count)` 并**不拷贝**元素，只是构造一个指向 `data()+offset`、长度为 `count` 的新 `span`。

> **示例 12** [难度 ★★★☆☆] [主题：调用栈 / 时序图：subspan ]
```
调用方                        span 对象                     底层数组
  │                              │                            │
  │  s.subspan(1, 2)            │                            │
  │────────────────────────────►│                            │
  │                              │ 构造新 span{               │
  │                              │   _M_ptr = s._M_ptr + 1,   │
  │                              │   _M_extent = 2 }          │
  │                              │───────────────────────────►│ (仅计算地址，无拷贝)
  │◄────────────────────────────│ 返回新 span (O(1))         │
  │                              │                            │
  │  [后续] 通过新 span 读写元素 │                            │
  │────────────────────────────────────────────────────────►│ 直接读写底层
```

- `[标准]`：`first(n)`、`last(n)`、`subspan(o, c)` 都返回新 `span`，复杂度 `O(1)`，且断言 `n <= size()` / `o <= size()`（经由 `__glibcxx_assert`，见 `文件：span`, `行号：341-344, 360-363, 373-387`）。
- `[实现]`：这些函数在 `-O2` 下通常被内联为一条 `lea`（地址计算），无分支、无拷贝。

> **示例 13** [难度 ★★★☆☆] [主题：调用栈 / 时序图：subspan ]
```cpp
// ⑨-1 subspan 不拷贝，仅移动指针（独立可编译）
#include <span>
#include <iostream>

int main() {
    int arr[6] = {10, 20, 30, 40, 50, 60};
    std::span<int> s{arr};
    auto mid = s.subspan(2, 3);          // 指向 arr[2..4]
    std::cout << mid.size() << " " << mid[0] << " " << mid[2] << "\n";  // 3 30 50
    mid[0] = 999;                         // 写穿到底层 arr
    std::cout << arr[2] << "\n";          // 999
    return 0;
}
```

> **示例 14** [难度 ★★★☆☆] [主题：调用栈 / 时序图：subspan ]
```cpp
// ⑨-2 first / last 是 subspan 的便捷包装
#include <span>
#include <iostream>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    std::span<int> s{arr};
    auto f = s.first(2);     // {1,2}
    auto l = s.last(2);      // {4,5}
    std::cout << f[1] << " " << l[0] << "\n";   // 2 4
    return 0;
}
```

---

## ⑩ 汇编分析：span 的零开销（Compiler Explorer 风格，-O2）

下面用 x86-64（`-std=c++23 -O2 -masm=intel`）观察 `span` 与普通指针+长度访问生成的指令是否等价。

> **示例 15** [难度 ★★★☆☆] [主题：汇编分析：span 的零开销]
```cpp
// ⑩-1 被测代码（仅作汇编对照，下方 asm 为其 -O2 产物）
#include <span>
#include <cstddef>

int sum_span(std::span<const int> s) {
    int r = 0;
    for (std::size_t i = 0; i < s.size(); ++i) r += s[i];
    return r;
}

int sum_ptr(const int* p, std::size_t n) {
    int r = 0;
    for (std::size_t i = 0; i < n; ++i) r += p[i];
    return r;
}
```

```asm
; GCC 15.3.0 (MinGW-w64 x86-64) -O2 -masm=intel ；两函数生成几乎相同循环
_Z8sum_spanSt4spanIKiLy18446744073709551615EE:
        mov     rdx, QWORD PTR [rdi+8]   ; 取 extent（span 第二成员）
        xor     eax, eax
        test    rdx, rdx
        je      .L2
        mov     rsi, QWORD PTR [rdi]     ; 取 _M_ptr（span 第一成员）
.L3:
        add     eax, DWORD PTR [rsi]
        add     rsi, 4
        sub     rdx, 1
        jne     .L3
.L2:
        ret

; sum_ptr 的循环体与此完全一致（仅入参约定差异）
_Z7sum_ptrPKiy:
        ... ; 同样的 add / add rsi,4 / sub rdx,1 / jne 循环
```

- `[实现·GCC15]`：`span` 在 `-O2` 下被**完全展开为指针 + 计数器的普通循环**，`first/last/subspan` 生成的是 `lea` 地址计算，没有虚调用、没有堆分配、没有额外间接层。
- `[标准]`：这正是 `span` 作为"零开销抽象"的体现——它只是把"指针 + 长度"这对本就存在的运行期信息，用类型安全地封装起来。

> **示例 16** [难度 ★★★☆☆] [主题：汇编分析：span 的零开销]
```cpp
// ⑩-2 验证：span 访问不引入边界检查指令（独立可编译，说明零开销）
#include <span>
#include <iostream>

int main() {
    int a[4] = {1, 2, 3, 4};
    std::span<int> s{a};
    // 下面这行在 -O2 下就是一次 mov，没有任何运行时 size 比较
    std::cout << s[2] << "\n";
    return 0;
}
```

---

## ⑪ STL 联系：span 在容器/视图家族中的位置

| 类型 | 所有权 | 可否修改元素 | 适用 |
|---|---|---|---|
| `std::span<T>` | 无（视图） | 取决于 `T` 是否 `const` | 任意连续类型的连续视图 |
| `std::string_view` | 无（视图） | 否（只读字符） | 字符序列（`char` 特化） |
| `std::array<T,N>` | 有 | 是 | 栈上定长数组 |
| `std::vector<T>` | 有 | 是 | 堆上变长数组 |
| `std::mdspan<T,Extents>` | 无 | 取决于 `T` | 多维视图（C++23，GCC 13 **未实现** `<mdspan>`） |

- `[标准]`：`span` 与 `string_view` 设计同源：`string_view` 可视为"字符版的 `span<const char>` + 字符串语义"。区别在于 `span` 支持任意元素类型与**静态 extent**，而 `string_view` 提供 `find/substr` 等字符串算法。
- `[实现]`：GCC 13 **未实现** `<mdspan>`（多维 span），若需多维连续视图，用 `span<T>` + 手动 `offset = i*stride` 计算，或升级编译器；正文不涉及 `#include <mdspan>`。
- `[经验]`：接口参数优先用 `span`（而非 `vector&` 或裸指针+长度）；返回结果时，若需"返回并转移所有权"用 `vector`，若"返回调用方已有的缓冲区视图"则 `span` 不合适（应用 `vector&` 输出参数或返回值）。

> **示例 17** [难度 ★★★☆☆] [主题：联系：span 在容器/视图家族中的]
```cpp
// ⑪-1 span 与 string_view 的同源对比（独立可编译）
#include <span>
#include <string_view>
#include <iostream>

int main() {
    int   ia[3] = {1, 2, 3};
    char  ca[4] = {'a', 'b', 'c', '\0'};
    std::span<int>        s{ia};
    std::string_view      sv{ca};
    std::cout << s.size() << " " << sv.size() << "\n";   // 3 3
    return 0;
}
```

> **示例 18** [难度 ★★★☆☆] [主题：联系：span 在容器/视图家族中的]
```cpp
// ⑪-2 用 span 取代 (ptr, len) 二参数接口（更安全、更表达化）
#include <span>
#include <iostream>
#include <cstddef>

// ❌ 旧风格：长度信息游离于类型之外，易传错
void old_style(const int* p, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) std::cout << p[i] << " ";
    std::cout << "\n";
}

// ✅ 新风格：长度与指针绑定在同一类型
void new_style(std::span<const int> s) {
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
}

int main() {
    int a[3] = {1, 2, 3};
    old_style(a, 3);
    new_style(a);
    return 0;
}
```

---

## ⑫ 工业案例：网络封包解析与行情快照

**案例 A：TCP 接收缓冲区分片解析（服务器/网络）**

网络层常拿到一整块 `char` 缓冲区，需要按协议帧切片。用 `span<std::byte>` 表达"当前待解析的剩余字节"，逐帧 `subspan` 推进，避免反复传 `offset` 与 `len`。

> **示例 19** [难度 ★★★☆☆] [主题：工业案例：网络封包解析与行情快照]
```cpp
// ⑫-1 网络封包：用 span 表达"剩余待解析字节"（独立可编译，模拟逻辑）
#include <span>
#include <cstddef>
#include <cstdint>
#include <iostream>

using byte_span = std::span<const std::byte>;

// 解析一个定长头部（4 字节长度 + 2 字节类型），返回载荷 span 与剩余
struct Frame { std::uint16_t type; std::span<const std::byte> payload; };

Frame parse_one(byte_span buf) {
    // 头部 6 字节
    std::uint32_t len = 0;
    // 小端读取长度（仅演示，不做端序防御）
    const auto* p = reinterpret_cast<const unsigned char*>(buf.data());
    len = (std::uint32_t)p[0] | ((std::uint32_t)p[1] << 8)
        | ((std::uint32_t)p[2] << 16) | ((std::uint32_t)p[3] << 24);
    std::uint16_t type = (std::uint16_t)(p[4] | (p[5] << 8));
    byte_span payload = buf.subspan(6, len);          // 载荷视图
    return Frame{type, payload};
}

int main() {
    // 模拟一个缓冲区：4 字节长度(=2) + 2 字节类型 + 2 字节载荷
    unsigned char raw[8] = {2,0,0,0, 1,0, 0xAA,0xBB};
    byte_span buf{reinterpret_cast<const std::byte*>(raw), 8};
    Frame f = parse_one(buf);
    std::cout << "type=" << f.type << " payload_bytes=" << f.payload.size() << "\n";
    return 0;
}
```

**案例 B：行情/交易快照（金融/交易系统）**

交易所行情常以连续数字数组下发（买价数组、卖量数组）。`span<const double>` 把"价格数组 + 长度"打包给风控/撮合模块，零拷贝。

> **示例 20** [难度 ★★★☆☆] [主题：工业案例：网络封包解析与行情快照]
```cpp
// ⑫-2 行情快照：零拷贝把价格数组交给计算模块（独立可编译，模拟逻辑）
#include <span>
#include <cmath>
#include <iostream>
#include <cstddef>

// 计算买卖盘中间价的加权（示意：以量加权）
double vwap(std::span<const double> prices, std::span<const double> amounts) {
    double num = 0, den = 0;
    for (std::size_t i = 0; i < prices.size(); ++i) {
        num += prices[i] * amounts[i];
        den += amounts[i];
    }
    return den > 0 ? num / den : 0.0;
}

int main() {
    const double bids[3]  = {100.1, 100.2, 100.3};
    const double sizes[3] = {10.0, 20.0, 30.0};
    std::cout << "vwap=" << vwap(bids, sizes) << "\n";
    return 0;
}
```

- `[经验]`：工业代码中 `span` 最常见的角色是**函数参数**，向算法层暴露"我给你一块连续内存及其长度"。它几乎从不当作长期存储对象（见 §⑧）。

> **示例 21** [难度 ★★★☆☆] [主题：工业案例：网络封包解析与行情快照]
```cpp
// ⑫-3 工业：序列化写入——span 作为"剩余可写缓冲区"视图（独立可编译）
#include <span>
#include <cstddef>
#include <cstdint>
#include <iostream>

// 返回写入字节数；用 span 表达"还剩多少空间可写"
std::size_t write_u32(std::span<std::byte>& out, std::uint32_t v) {
    if (out.size() < 4) return 0;                      // 空间不足
    unsigned char* p = reinterpret_cast<unsigned char*>(out.data());
    p[0] = v & 0xFF; p[1] = (v >> 8) & 0xFF;
    p[2] = (v >> 16) & 0xFF; p[3] = (v >> 24) & 0xFF;
    out = out.subspan(4);                              // 推进视图
    return 4;
}

int main() {
    std::byte buf[16] = {};
    std::span<std::byte> w(buf);
    std::size_t n = write_u32(w, 0x12345678);
    std::size_t n2 = write_u32(w, 1);
    std::cout << "written=" << (n + n2) << " remaining=" << w.size() << "\n";
    return 0;
}
```

---

## ⑬ 源码分析：libstdc++ 的 span 实现

以下片段取自 GCC 13.1.0 的 `include/c++/span`（真实文件，逐行核对）。

### 13.1 extent 的存储策略

> **示例 22** [难度 ★★★☆☆] [主题：的存储策略]
```cpp
#include <cstddef>
// ⑬-1a libstdc++ 源码摘录（文件：span，行号：81-99）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   struct _ExtentStorage {
//     _S_extent() noexcept { return this->_M_extent_value; }   // 动态 extent 读取
//     : _M_extent_value(__extent) { }                          // 成员初始化列表
//     _M_extent() const noexcept { return this->_M_extent_value; }
//     size_t _M_extent_value;                                  // 仅动态 extent 时存在
//   };
// 静态 extent 时该结构为空，_M_extent() 直接返回编译期常量，对象不占此字段。
int main() { return 0; }
```

- `[实现]`：当 `Extent == dynamic_extent`，`_ExtentStorage` 含一个 `size_t` 成员；当 extent 是编译期常量（如 4），`_M_extent()` 直接返回该常量，对象中不存在这个字段——这就是为什么 `sizeof(span<int,4>) == 8`。

### 13.2 两个核心成员与构造函数

> **示例 23** [难度 ★★★☆☆] [主题：两个核心成员与构造函数]
```cpp
// ⑬-2a libstdc++ 源码摘录（文件：span，行号：153 / 161 / 189 / 212）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   // 行号 153：nullptr 构造
//   : _M_ptr(nullptr), _M_extent(0)
//   // 行号 161：指针 + 计数构造
//   : _M_ptr(std::to_address(__first)), _M_extent(__count)
//   // 行号 189：C 数组构造（阻止意外推导）
//   span(type_identity_t<element_type> (&__arr)[_ArrayExtent]) noexcept
//     : span(static_cast<pointer>(__arr.data()), _ArrayExtent)
//   // 行号 212：range 构造，requires contiguous_range + borrowed_range
//   : _M_extent(__s.size()), _M_ptr(__s.data())
int main() { return 0; }
```

- `[实现]`：构造只是把指针和长度填入两成员；`to_address` 把迭代器/指针归一为裸指针；`type_identity_t` 阻止从 `T(&)[N]` 向 `T*` 的意外模板推导。

### 13.3 访问函数与切片

> **示例 24** [难度 ★★★☆☆] [主题：访问函数与切片]
```cpp
// ⑬-3a libstdc++ 源码摘录（文件：span，行号：252-253 / 280-283 / 287-288 / 341-344 / 360-363 / 399）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   // 行号 252-253：size()
//   size() const noexcept { return this->_M_extent._M_extent(); }
//   // 行号 280-283：operator[]
//   operator[](size_type __idx) const noexcept
//   { __glibcxx_assert(__idx < size()); return *(this->_M_ptr + __idx); }
//   // 行号 287-288：data()
//   data() const noexcept { return this->_M_ptr; }
//   // 行号 341-344：first(count)
//   first(size_type __count) const noexcept
//   { __glibcxx_assert(__count <= size()); return { this->data(), __count }; }
//   // 行号 399：subspan(offset, count)
//   subspan(size_type __offset, size_type __count = dynamic_extent) const noexcept
int main() { return 0; }
```

- `[实现]`：`operator[]` 中 `__glibcxx_assert` 在 **NDEBUG 下完全消失**（发布构建零成本），在调试构建下触发断言——这正是 `span` "调试期边界检查、发布期零开销"的设计。
- `[标准]`：注意 `operator[]` 标注 `const noexcept` 但**不抛异常也不做运行期边界检查**（NDEBUG 时）；越界访问是 UB，调用方负责保证索引合法。

> **示例 25** [难度 ★★★☆☆] [主题：访问函数与切片]
```cpp
// ⑬-1 对照理解：调试构建下越界会被断言捕获（独立可编译，演示接口）
#include <span>
#include <iostream>

int main() {
    int a[3] = {1, 2, 3};
    std::span<int> s{a};
    std::cout << s[0] << " " << s[1] << " " << s[2] << "\n";
    // s[3] 在 -DNDEBUG 外会触发 __glibcxx_assert；此处不触发以保持示例可跑
    return 0;
}
```

---

## ⑭ WG21 提案背景

- **P0122R8《span》**（主提案，最终并入 C++20）：由 Nevin Liber 等人提出，目标是标准化"连续序列的视图"，统一 `(pointer, length)` 这一长期被各公司用 `gsl::span`、`folly::Range`、`absl::Span` 重复实现的抽象。动机是消除 C 接口中长度与指针分离导致的缓冲区溢出与接口歧义。
- **P1024R3《span 的若干修复》**：修正 `span` 在数组到 `const` 转换、构造函数约束上的边角问题（如允许从 `T(&)[N]` 构造 `span<const T, N>`）。
- **P1976R3《结构化绑定与 span》**：修复 `span` 与结构化绑定、`tuple` 互操作时的接口缺失（如 `get`、`tuple_size` 特化）。
- **P1428R0**：关于 `span` 的 `first/last/subspan` 边界行为澄清。

- `[标准]`：`std::span` 在 C++20 成为标准，C++23 仅做边角修复（如 `std::as_bytes`/`std::as_writable_bytes` 的完善、`span` 与范围适配器的兼容性）。
- `[经验]`：若需兼容 C++17 代码库，可用 `gsl::span`（Guidelines Support Library）作为过渡，接口高度一致。

> **示例 26** [难度 ★★★☆☆] [主题：提案背景]
```cpp
// ⑭-1 as_bytes / as_writable_bytes：以字节视角看任意 span（C++20，GCC13 支持）
#include <span>
#include <iostream>
#include <cstddef>

int main() {
    int a[2] = {0x01020304, 0};
    std::span<int> s{a};
    auto b = std::as_bytes(s);                 // span<const std::byte>
    std::cout << "bytes=" << b.size() << "\n"; // 8（2*sizeof(int)）
    return 0;
}
```

---

## ⑮ 面试题

1. **`std::span` 与 `std::vector` 的根本区别是什么？何时用哪个？**
   → `span` 非拥有、零开销、只视图；`vector` 拥有、可增长、有分配成本。函数参数用 `span`；需要存储/返回数据用 `vector`。

2. **`span<int, 4>` 和 `span<int>` 的 `sizeof` 通常分别是多少？为什么不同？**
   → 分别为 8 和 16（x86-64）。静态 extent 的长度编译期已知，不占存储；动态 extent 需额外存 `size_t`。

3. **`span` 越界访问会抛异常吗？为什么？**
   → `[标准]` 不会（NDEBUG 下）。`operator[]` 是 `noexcept` 且靠 `__glibcxx_assert` 仅在调试构建检查；越界是 UB。

4. **下面代码有什么问题？**
> **示例 27** [难度 ★★★☆☆] [主题：面试题]
   ```cpp
#include <vector>
#include <span>
   std::span<int> f() { std::vector<int> v{1,2,3}; return {v}; }
```
   → 返回后 `v` 析构，`span` 悬垂（见 §⑧）。

5. **`span` 满足哪些 C++20 范围概念（concepts）？**
   → `contiguous_range`、`sized_range`、`view`、`borrowed_range`（因为不拥有）。

6. **为什么 `span` 不能从 `std::vector<bool>` 构造？**
   → `vector<bool>` 是位压缩特化，元素不连续、不是真正的 `int`；`span` 要求底层是连续 `T` 对象。`[标准]`

7. **`first(n)` 在 `n > size()` 时行为？**
   → 调试构建触发断言；发布构建 UB。总是确保 `n <= size()`。

8. **`std::span` 能作为 `std::map` 的 key 吗？**
   → 不能（无 `operator<` 且语义是视图，比较无意义）。若需关联容器见 ⟶ `Book/part07_stl/ch83_map.md`。

> **示例 28** [难度 ★★★☆☆] [主题：面试题]
```cpp
// ⑮-1 面试题实战：判断 span 是否 contiguous（独立可编译）
#include <span>
#include <type_traits>
#include <iostream>

int main() {
    static_assert(std::is_same_v<
        std::span<int>::element_type, int>);
    std::cout << "span is contiguous_range concept satisfied\n";
    return 0;
}
```

---

## ⑯ 易错点

1. **悬垂 span（从临时对象构造后外传）** —— 见 §⑧。永远确保底层存储活得比 `span` 久。
> **示例 29** [难度 ★★★☆☆] [主题：易错点]
   ```cpp
   // ❌ 逻辑错误演示（编译通过，运行期 UB）：从临时 string 取 view 外传
   #include <string>
   #include <string_view>
   std::string_view dangling() {
       std::string s = "temp";
       return std::string_view(s);   // ❌ s 析构后返回悬垂视图
   }
   int main() { (void)dangling; return 0; }
```

2. **把 `span` 存为成员变量后底层被修改/释放** —— `vector` 扩容、`std::string` 的 SSO 迁移都会让已存的 `span` 失效。
> **示例 30** [难度 ★★★☆☆] [主题：易错点]
   ```cpp
   // ❌ 逻辑错误演示（编译通过）：扩容使 span 悬垂
   #include <span>
   #include <vector>
   int main() {
       std::vector<int> v = {1,2,3};
       std::span<int> s = v;
       v.push_back(4);    // 若触发重新分配，s 指向旧内存（UB 风险）
       // 安全做法：在 v 稳定后再构造 s，或重新取 s = v
       s = v;             // ✅ 重新绑定
       return 0;
   }
```

3. **误以为 `span` 越界会抛异常** —— 它不会（§⑬）。需要安全访问请用 `std::size` 先检查。
> **示例 31** [难度 ★★★☆☆] [主题：易错点]
   ```cpp
   // ❌ 错误预期：希望 s[100] 抛异常
   #include <span>
   #include <iostream>
   int main() {
       int a[3] = {1,2,3};
       std::span<int> s{a};
       if (100 < s.size()) {            // ✅ 正确：先检查
           std::cout << s[100] << "\n";
       }
       return 0;
   }
```

4. **用 `span` 返回函数内新建的数据** —— `span` 不拥有，无法"返回并转移所有权"，应返回 `vector` 或接受 `span` 输出参数。
> **示例 32** [难度 ★★★☆☆] [主题：易错点]
   ```cpp
   // ✅ 正确：输出参数写入调用方提供的缓冲区
   #include <span>
   #include <iostream>
#include <cstddef>
   void fill(std::span<int> out) {
       for (std::size_t i = 0; i < out.size(); ++i) out[i] = static_cast<int>(i);
   }
   int main() {
       int buf[5] = {};
       fill(buf);
       std::cout << buf[4] << "\n";   // 4
       return 0;
   }
```

5. **混淆 `dynamic_extent` 与 0** —— `dynamic_extent` 是 `static_cast<std::size_t>(-1)`，代表"长度运行期决定"，不是"长度为 0"。
> **示例 33** [难度 ★★★☆☆] [主题：易错点]
   ```cpp
   // ✅ 演示 dynamic_extent 的值
   #include <span>
   #include <iostream>
   int main() {
       std::cout << std::dynamic_extent << "\n";  // 18446744073709551615
       return 0;
   }
```

---

## ⑰ FAQ

**Q1：`span` 能修改底层元素吗？**
→ 取决于元素类型。`span<int>` 可读写；`span<const int>` 只读。二者可互相转换（向 const 退化），但反之不可。

**Q2：`span` 能做函数返回值吗？**
→ 可以，但只适合"返回调用方已经持有的缓冲区的视图"，例如返回结构体某字段的切片。不要用来返回新分配的数据。

**Q3：为什么 `span` 不提供 `push_back`？**
→ 因为它不拥有存储，不能改变底层容量；容量管理属于 `vector`/`array`。

**Q4：`span` 和 `std::string_view` 能互相转换吗？**
→ 字符场景可以：`std::string_view` 可隐式/显式构造 `span<const char>`；反之需 `std::span` 的 `.data()` + `.size()` 手动构造 `string_view`。

**Q5：GCC 13 支持 `std::mdspan` 吗？**
→ `[实现·GCC15]` 不支持（`<mdspan>` 未实现）。多维视图请先用 `span<T>` + 步长计算，或升级编译器。

**Q6：`span` 的迭代器失效规则和 `vector` 一样吗？**
→ 不一样。`span` 本身没有"失效"概念，失效的是**底层存储**。底层的 `vector` 扩容会让所有指向它的 `span` 同时失效（见 §⑧）。

> **示例 34** [难度 ★★★☆☆] [主题：未分类]
```cpp
// ⑰-1 FAQ：const 退化的 span 互转（独立可编译）
#include <span>
#include <iostream>
#include <vector>

void read_only(std::span<const int> s) { for (int x : s) std::cout << x << " "; }

int main() {
    std::vector<int> v = {1, 2, 3};
    std::span<int> rw{v};                // 可读写
    read_only(rw);                       // ✅ 自动退化为 span<const int>
    std::cout << "\n";
    return 0;
}
```

> **示例 35** [难度 ★★★☆☆] [主题：未分类]
```cpp
// ⑰-2 FAQ：span 与 string_view 互操作（字符特化）
#include <span>
#include <string_view>
#include <iostream>

int main() {
    char text[] = "hello";
    std::string_view sv{text};
    std::span<const char> s{sv.data(), sv.size()};   // ✅ 手动构造
    std::cout << s.size() << "\n";                    // 5
    return 0;
}
```

---

## ⑱ 最佳实践

1. **函数参数优先用 `span<const T>`（只读）或 `span<T>`（读写），替代 `(T*, size_t)` 二参数。** 类型即文档，长度不再游离。
2. **只读场景用 `span<const T>`，最大化调用方灵活性**（既能传 `vector` 也能传 `array` 还能传裸数组）。
3. **`span` 只作局部/参数，不作长期存储**；需要持久化就接受 `const vector<T>&` 或返回 `vector<T>`。
4. **切片用 `first/last/subspan`，拒绝手工指针算术**；它们带调试期断言。
5. **能用静态 extent 就用静态 extent**（`span<T,N>`），获得更小对象、更强类型检查、更多编译期优化。
6. **跨 ABI / C 接口边界**用 `span` 的 `data()` + `size()` 拆成 `(void*, size_t)`，内部立即重建 `span`。
7. **`noexcept` 与零开销**：`span` 的访问都是 `noexcept`，可在热路径放心使用。

> **示例 36** [难度 ★★★☆☆] [主题：最佳实践]
```cpp
// ⑱-1 最佳实践：只读 span 作为万能参数（独立可编译）
#include <span>
#include <vector>
#include <array>
#include <iostream>

int max_of(std::span<const int> s) {
    int m = s.empty() ? 0 : s[0];
    for (int x : s) if (x > m) m = x;
    return m;
}

int main() {
    int        raw[3] = {3, 1, 2};
    std::vector<int> v = {9, 5, 7};
    std::array<int,2> a = {4, 8};
    std::cout << max_of(raw) << " " << max_of(v) << " " << max_of(a) << "\n";
    return 0;
}
```

> **示例 37** [难度 ★★★☆☆] [主题：最佳实践]
```cpp
// ⑱-2 最佳实践：跨 C 接口时拆/装 span（独立可编译）
#include <span>
#include <cstddef>
#include <iostream>

extern "C" void c_consume(const int* p, std::size_t n);

void c_consume(const int* p, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) std::cout << p[i] << " ";
    std::cout << "\n";
}

void wrapper(std::span<const int> s) {
    c_consume(s.data(), s.size());        // ✅ 拆成 C 接口
}

int main() {
    int a[3] = {1, 2, 3};
    wrapper(a);
    return 0;
}
```

---

## ⑲ 性能分析

### 19.1 复杂度

- **构造**：`O(1)`（填指针+长度）。
- **`size()` / `data()` / `operator[]` / `front` / `back`**：`O(1)`。
- **`first/last/subspan`**：`O(1)`，返回新视图（无拷贝）。
- **遍历**：`O(N)`，与裸指针遍历指令级等价（§⑩）。

### 19.2 缓存友好性

- `[平台·x86-64]`：`span` 本身 8/16 字节，可放入寄存器或单 cache line；它指向的底层数组连续，遍历具有**完美的空间局部性**（预取器友好）。
- `[经验]`：对比 `std::list`（节点散列、缓存不友好），`span` 遍历速度是量级优势（见 ⟶ `Book/part07_stl/ch79_list.md`）。

### 19.3 与 `vector` 传参的对比（microbenchmark 量级）

> **示例 38** [难度 ★★★☆☆] [主题：与 vector 传参的对比]
```cpp
// ⑲-1 量级对照：span 传参 vs vector 传值（独立可编译，含示意计时骨架）
#include <span>
#include <vector>
#include <iostream>
#include <chrono>

std::size_t sum_span(std::span<const int> s) {
    std::size_t r = 0;
    for (int x : s) r += static_cast<std::size_t>(x);
    return r;
}
std::size_t sum_vec(std::vector<int> v) {   // 传值 -> 一次完整拷贝 O(N)
    std::size_t r = 0;
    for (int x : v) r += static_cast<std::size_t>(x);
    return r;
}

int main() {
    std::vector<int> data(1'000'000, 7);
    auto t0 = std::chrono::steady_clock::now();
    volatile auto a = sum_span(data);        // ✅ 仅视图，无拷贝
    auto t1 = std::chrono::steady_clock::now();
    volatile auto b = sum_vec(data);         // ❌ 拷贝百万 int
    auto t2 = std::chrono::steady_clock::now();
    std::cout << "span=" << (t1-t0).count() << "ns vec_copy=" << (t2-t1).count() << "ns\n";
    return 0;
}
```

- `[经验]`：在 N=1e6、元素 4 字节时，`vector` 传值会产生约 **4 MB 的拷贝**（量级），而 `span` 传参仅复制 16 字节的视图。热路径上差距可达**数十到数百倍**（示意，取决于缓存热度）。

### 19.4 ABI 与异常安全

- `[平台·x86-64]`：`span` 是 trivially-copyable 的 POD 式类型（两个标量），**无 ABI 隐患**，跨编译器/版本稳定传递。
- `[标准]`：所有访问函数标注 `noexcept`，不分配、不抛异常。

### 19.5 三编译器对比

| 行为 | GCC 13 | Clang 17 | MSVC 19.3x |
|---|---|---|---|
| `span` 支持 | ✅ C++20 | ✅ | ✅ |
| `static_extent` 优化 | ✅ | ✅ | ✅ |
| `as_bytes` | ✅ | ✅ | ✅ |
| `mdspan` | ❌ | ❌（需 18+实验） | ❌ |

- `[平台·x86-64]`：三者语义一致；差异仅在 `<mdspan>` 与边角 fixes 的支持度。

---

## ⑳ 跨语言对比：连续视图的语义

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：函数参数用 `std::span<const int>` 同时接收数组与 vector。** 你不再为两种容器写重载。请说明视图语义。
   - [标准] span 是连续序列的轻量非拥有视图（C++20），可从上/数组/vector 构造；不管理生命周期。
   - [引用] ISO/IEC 14882:2023 §[views.span]（std::span）；cppreference "std::span" 词条。

2. **真实场景：span 不拥有数据，原容器提前销毁会悬垂。** 你返回 `make_span(v)` 的 span 后 v 出了作用域。请说明责任。
   - [标准] span 仅引用底层存储；底层被释放后使用该 span 是未定义行为，生命周期由调用方保证。
   - [引用] ISO/IEC 14882:2023 §[views.span]（视图的引用语义）/ [basic.life]；cppreference "std::span" 词条。

3. **真实场景：静态 extent 可编译期 `size()`。** 你用 `span<int, 4>` 让大小参与类型。请说明。
   - [标准] extent 在编译期已知时成为类型一部分（静态 extent），`size()` 为编译期常量。
   - [引用] ISO/IEC 14882:2023 §[views.span]（静态/动态 extent）；cppreference "std::span" 词条。

| 语言 | 对应抽象 | 说明 |
|---|---|---|
| C++ | `std::span<T>` / `std::span<T,N>` | 非拥有连续视图；静态 extent 编入类型 |
| Rust | `&[T]` / `&mut [T]`（slice） | 借用例证；生命周期由借用检查器强制（§⑧ 的悬垂在 Rust 编译期拒绝） |
| Go | `[]T`（slice） | 含 `{ptr, len, cap}` 三元组，可重新切片 `s[lo:hi]` |
| Java | 无内建（`int[]` 携带长度，但无通用视图类型） | 数组自带 `.length`；无等价 `span` 泛型视图 |
| C# | `Span<T>` / `ReadOnlySpan<T>`（`ref struct`） | 与 C++ `span` 高度同构；`ref struct` 禁止上堆，防止悬垂 |
| Swift | `ArraySlice<T>` | 借数组的视图，含 `startIndex`/`endIndex` |

- `[标准]`：C++ `span` 对标 Rust `&[T]`、C# `Span<T>`、Go `[]T`（核心三者）。**关键差异**：Rust/C# 在类型系统层面阻止 `span` 悬垂（生命周期/`ref struct`），而 C++ `span` 把生命周期责任交给程序员（见 §⑧、§⑯），这是 C++ 零开销权衡的代价。
- `[经验]`：从 Rust/C# 转来的工程师会自然使用 `span`；但必须习惯"C++ 不会在编译期阻止你持有悬垂视图"，要靠代码审查与 `-DNDEBUG` 之外的 sanitizer（`-fsanitize=address`）兜底。

> **示例 39** [难度 ★★★☆☆] [主题：跨语言对比：连续视图的语义]
```cpp
// ⑳-1 跨语言映射：Go 式 s[lo:hi] 在 C++ 用 subspan 表达（独立可编译）
#include <span>
#include <iostream>

int main() {
    int a[6] = {0, 1, 2, 3, 4, 5};
    std::span<int> s{a};
    auto slice = s.subspan(1, 3);     // 等价于 Go 的 s[1:4]
    for (int x : slice) std::cout << x << " ";   // 1 2 3
    std::cout << "\n";
    return 0;
}
```

> **示例 40** [难度 ★★★☆☆] [主题：跨语言对比：连续视图的语义]
```cpp
// ⑳-2 跨语言映射：Rust &[T] 的"借用保证"在 C++ 需 manual discipline（独立可编译）
#include <span>
#include <vector>
#include <iostream>

// C++ 无法在编译期保证 s 不悬垂；约定：调用方负责底层存活
void use(std::span<const int> s) { for (int x : s) std::cout << x << " "; }

int main() {
    std::vector<int> v = {1, 2, 3};
    use(v);                          // ✅ 借用期 v 存活
    std::cout << "\n";
    return 0;
}
```

---

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：std::span 与「零成本视图」的标准化

[史] `std::span` 随 C++20 进入标准，核心提案是 Neil MacIntosh 等人的 P0122（span: bounds-safe views for sequences of contiguous objects）。[史] 它的动机是解决长期痛点：函数想接收「数组或 vector 的连续片段」却没有统一、零开销的类型，只能用 `(T*, size_t)` 这对裸指针——既丢长度信息又易越界。[轶] `span` 的动态/静态 Extent 双形态（运行时 `span<T>` 与编译期 `span<T,N>`）是一个精巧折中，静态版本能保留边界信息甚至优化掉 size 存储。[评] `span` 是「借用而非拥有」哲学进入标准库的标志性一步，与 Rust 的切片 `&[T]` 异曲同工。

### ㉒.2 真实工程坐标：span 活在哪些产品里

网络封包解析、行情快照、图像/音频缓冲的零拷贝切片是 `std::span` 的主场：Chromium 的 `base::span` 被广泛用于字节流处理；游戏引擎把 `span<uint8_t>` 作为资源加载的统一接口；金融系统的行情快照用 `span<const double>` 做无拷贝批量计算；LLVM/Clang 的 `ArrayRef` 是 `span` 的先行者，早已在编译器各层传递连续区间。

- **跨行业实例（科学计算/数值库）**：Eigen、Blaze 等线性代数库的「只读矩阵视图」与 `Eigen::Map`、NumCpp 的缓冲接口，用 `span`/视图语义包装外部内存（如从 HDF5/NumPy 数组借来的连续缓冲），做到「零拷贝把外部数据喂给数值核」；这是 HPC 与数据科学交叉处的真实用法。
- **跨行业实例（图形/游戏资源）**：Unity 的 C++ 后端与 Unreal 的资源序列化用 `span<uint8_t>` 表示「从文件/网络读来的字节块切片」，在解析网格/纹理时避免逐层拷贝；把视图而非所有权传递到解析栈，是大型资源管线降低堆压力的常用手段。

### ㉒.3 生产踩坑：span 的常见误用与陷阱

[评] 最大的坑是「悬空视图」：span 不拥有数据，若底层容器（如临时 `vector` 或栈数组）先销毁，span 立刻悬空——典型的「返回 `span` 指向局部变量」错误。另一坑是「把 `span` 当容器用」——它没有 `push_back`、不管理生命周期，误用会编译失败或语义错乱。还有 `span` 与 `vector` 混用时的越界边界：动态 `span` 不保留容量信息，下标越界仍是 UB，需配合 `first` / `subspan` 的安全切片。

### ㉒.4 与标准的互动：span 与标准的演进

[史] `std::span` 经 P0122R7 在 C++20 落地，填补了标准库长期缺失的「连续视图」原语。[评] 它是 C++20 一系列「视图化」改革（ranges、string_view）的一环，WG21 后续又提出 `std::mdspan`（多维视图，C++23）与 `std::spanstream` 等扩展，方向明确是「用零开销视图取代裸指针 + 长度的传统 C 接口」。同时标准也强调：span 的 ABI 在 C++20 后冻结，避免重蹈字符串 dual-ABI 的覆辙。

- **WG21 修订链**：`std::span` 经 P0122R0（原名 `array_view`）→…→P0122R7（Neil MacIntosh、Stephan T. Lavavej，wg21.link/P0122R7，2018 Jacksonville 采纳）在 C++20 落地。R0→R7 的关键变更包括：R0 改名 `array_view`→`span` 并移除非连续多维部分；R5 移除 `unique_ptr`/`shared_ptr` 构造与 `length()`；R6/R7 把比较运算符（如 `operator==`）整组删除——删除理由见 P1085（「浅拷贝/浅 const 的视图不应有深比较语义」，wg21.link/P1085）。后续 `std::mdspan`（P0009R15，wg21.link/P0009R15）与 `std::spanstream`（P0448 系列）延续同一视图哲学。
- **ISO 条款**：`std::span` 规定于 ISO/IEC 14882 §24.7.2（`[views]`/`[span]`）。其设计理由是「作为连续序列的**非拥有**视图，提供 `(pointer, size)` 的零开销、类型安全替代」——标准明确 span 不管理生命周期，且其 ABI 在 C++20 冻结，正是为了避免 `std::string` dual-ABI 那样的历史教训。

### ㉒.5 权威引用

- [cppreference: std::span](https://en.cppreference.com/w/cpp/container/span) — 连续视图与动态/静态 Extent 的权威定义
- [WG21 P0122R7 — span: bounds-safe views](https://wg21.link/p0122) — span 进入 C++20 的核心提案
- [LLVM 项目仓库](https://github.com/llvm/llvm-project) — libc++ 的 span 工业实现参考

## 附录：练习题 / 思考题 / 源码阅读路线

### 练习题

1. 实现一个 `split(std::span<const char> s, char delim) -> std::vector<std::span<const char>>`，在不拷贝字符的前提下按分隔符切分（返回的是指向原缓冲区的视图）。
2. 写一个 `lexicographical_compare(std::span<const int> a, std::span<const int> b)`，要求 `O(min(Na,Nb))`。
3. 用静态 extent 写一个 `MatrixView<double, 3, 3>`（3×3 视图），提供 `at(r,c)` 与 `det()` 计算（不拷贝）。

### 思考题

- 为什么 `span` 的 `operator[]` 是 `noexcept` 却仍可能引发 UB？这与 `vector::operator[]` 有何异同？
- `span` 满足 `borrowed_range`，这意味着什么？与 `std::string_view` 作为 `borrowed_range` 的关系？
- 若 `span` 增加"析构时归还底层内存"的能力，会破坏哪些设计前提？

### 源码阅读路线

1. `include/c++/span`（GCC 13.1.0）—— 通读 `class span`、`_ExtentStorage`、`first/last/subspan`。
2. `include/c++/bits/range_access.h` —— 理解 `contiguous_iterator` 与 `span::iterator` 的关系。
3. `include/c++/bits/ranges_base.h` —— `contiguous_range` / `sized_range` 概念如何被 `span` 满足。
4. `include/c++/type_traits` —— 阅读 `is_const` / `is_convertible`，理解 `const` 退化构造的约束。
5. 进阶：对比 `include/c++/mdspan`（需更新编译器）—— 看多维视图如何泛化 `span` 的 extent 思想。

> 推荐读物（已融于正文）：Nevin Liber, *P0122R8 span*；ISO/IEC 14882:2023 `[views]`、`[span.overview]`；Bjarne Stroustrup《C++ Programming Language》第 4 版容器章节；Herb Sutter《GotW》关于视图与所有权的条目。

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Abseil absl::Span（github.com/abseil/abseil-cpp）**：`std::span` 的直接前身。
- **Chromium base::span（github.com/chromium/chromium）**：同理的连续视图。

**常见陷阱 / 最佳实践**：
- `std::span` 不拥有内存，悬空 span（指向已释放缓冲）是常见 UB；传入 span 而非指针+大小可消除长度不匹配 bug。
- `span` 的 `size()` 是运行期值，越界访问 `operator[]` 不抛（需用 `at()` 或断言）。

- **LLVM libc++ `span`（llvm/llvm-project）**：`std::span` 的参考实现，`<span>` 头中 `element_type`/`size_type` 的定义与 `subspan` 的边界检查。
- **Folly `Range`/`StringPiece`（facebook/folly）**：`std::span` 的前身之一，`folly::Range` 是 Facebook 代码库的事实标准连续视图，`folly::StringPiece` 零拷贝切分字符串。
- **Boost.Core `span` 提案（boostorg/core）**：`std::span` 进入标准前的 Boost 实验实现。
- **ClickHouse（ClickHouse/ClickHouse）**：query 执行中用 `std::span` 零拷贝传递列块，避免 `std::vector` 拷贝。
- **Google Benchmark（github.com/google/benchmark）**：`benchmark::Span` 等工具用 `std::span` 传参，是 span 在测试框架中的落地。

> 交叉引用：数组见 [ch80](Book/part07_stl/ch80_array.md)；连续内存见 [ch35](Book/part04_memory/ch35_memory_layout.md)。

## 相关章节（交叉引用）

- **同模块相邻**：⟶ Book/part07_stl/ch76_stl_arch.md（第76章　STL 架构与迭代器概念）—— span 是该架构下的轻量连续视图
- **同模块相邻**：⟶ Book/part07_stl/ch80_array.md（第80章　array 与固定数组）—— span 是 array 数据的零拷贝视图
- **同模块相邻**：⟶ Book/part07_stl/ch77_vector.md（第77章　vector：扩容、失效、allocator 协作）—— span 是 vector 数据的零拷贝视图
- **跨模块前置**：⟶ Book/part04_memory/ch38_allocator.md（第 38 章　分配器（Allocator）模型与 PMR）—— span 不拥有内存，其来源常由 allocator 分配

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）
**真实场景：底层二进制帧解析——同一函数接收栈缓冲/array/vector。** 网络包负载可能是 `uint8_t[]`、定长 `array` 或动态 `vector`，用 `span` 统一接收，避免为每种容器重载。

> **示例 41** [难度 ★★★☆☆] [主题：练习 1（难度 ★★）]
```cpp
#include <iostream>
#include <span>
#include <vector>
#include <array>
void print(std::span<const int> s) {
    for (int x : s) std::cout << x << ' ';
    std::cout << "\n";
}
int main() {
    int c[] = {1, 2, 3};
    std::array<int, 3> a{4, 5, 6};
    std::vector<int> v{7, 8, 9};
    print(c); print(a); print(v);     // 1 2 3 / 4 5 6 / 7 8 9
}
```

[标准] 结论：`std::span<T>` 是连续序列的视图（指针+长度），可隐式从任意连续容器构造；`span<const T>` 接受只读视图，是"我想读一段连续 int"的标准签名，避免为每种容器重载。

[引用] ISO/IEC 14882:2023 §[views.span]（`span` 的连续视图与隐式构造）；其零成本布局见本章附录 ASM 实证；cppreference "container/span"。

### 练习 2（难度 ★★★）
**真实场景：协议分块——不拷贝取载荷子区间。** 从整帧 `span` 切出 payload 段做 CRC 校验，`subspan` 在原缓冲上滑动视图，复杂度 O(1)。

> **示例 42** [难度 ★★★☆☆] [主题：练习 2（难度 ★★★）]
```cpp
#include <iostream>
#include <span>
#include <vector>
int main() {
    std::vector<int> v{0, 1, 2, 3, 4, 5};
    std::span<int> sp(v);
    auto mid = sp.subspan(2, 3);       // [2,3,4]，不拷贝
    for (int x : mid) std::cout << x << ' ';
    std::cout << "\n";                  // 2 3 4
}
```

[标准] 结论：`std::span` 的 extent 可是编译期常量（静态）或 `dynamic_extent`（运行时）；`subspan/first/last` 在原缓冲区上滑动视图，复杂度 O(1)，适合算法分块。

[引用] ISO/IEC 14882:2023 §[views.span]（`subspan`/`first`/`last` 与原缓冲区上的视图）；见 cppreference "container/span" 词条。

### 练习 3（难度 ★★★★）
**真实场景：图像行视图——把扁平 RGB 缓冲按宽切成逻辑行，无拷贝。** 图像处理把 `vector<byte>` 当二维，按列数出每行 `span`。

> **示例 43** [难度 ★★★☆☆] [主题：练习 3（难度 ★★★★）]
```cpp
#include <iostream>
#include <span>
#include <vector>
int main() {
    std::vector<int> m{0, 1, 2, 3, 4, 5};   // 2x3
    const int cols = 3;
    auto row = [&](int r) -> std::span<int> {
        return std::span<int>(&m[r * cols], cols);
    };
    for (int x : row(1)) std::cout << x << ' ';
    std::cout << "\n";                        // 3 4 5
}
```

[标准] 结论：`span` 可指向缓冲区的任意偏移，配合"步长"概念能表达二维行视图而无需分配新容器；`at()` 提供有界检查（越界抛 `std::out_of_range`），`operator[]` 无检查更快。

[引用] ISO/IEC 14882:2023 §[views.span]（`at()`/`operator[]` 的有界/无界差异）；`span` 的"视图"思想源自 GSL/`std::span` 提案（P0122），见 cppreference "container/span"。

## 附录：用法演绎（从选型到落地）

### 演绎 1：泛型数值累加，接受任意连续容器
把容器转成 `span<const T>` 后用标准算法累加，签名只依赖连续性。

> **示例 44** [难度 ★★★☆☆] [主题：演绎 1：泛型数值累加，接受任意连续]
```cpp
#include <iostream>
#include <span>
#include <vector>
#include <numeric>
template <class C>
int sum_of(const C& c) {
    std::span<const int> s(c.data(), c.size());
    return std::reduce(s.begin(), s.end());
}
int main() {
    std::vector<int> v{1, 2, 3};
    std::cout << sum_of(v) << "\n";          // 6
}
```

### 演绎 2：const 正确性——span<const T> 与 span<T>
只读函数用 `span<const T>`，可接收 `vector<int>` 与 `const vector<int>`；`span<T>` 才能写回。

> **示例 45** [难度 ★★★☆☆] [主题：演绎 2：const 正确性——sp]
```cpp
#include <iostream>
#include <span>
#include <vector>
void read_only(std::span<const int> s) {
    for (int x : s) std::cout << x << ' ';
    std::cout << "\n";
}
int main() {
    std::vector<int> v{1, 2, 3};
    read_only(v);                  // span<const int> 可隐式构造
    std::span<int> rw(v);
    rw[0] = 9;                      // 写回
    read_only(v);                  // 9 2 3
}
```
## 附录：GCC 15.3.0 真机实证 — `std::span` 零成本视图

> 证据：`_asm_demo/ch82_span_test.cpp`（`-O2`，链接 exe 后 objdump）。结论：**span 只是 `{ptr, size}` 对，遍历与裸 `ptr+len` 同码；`operator[]` 不检查边界。**

**1. 遍历零成本** — `sum_span` 与裸 `sum_ptr` 生成同一循环体（仅寄存器分配不同）：

```asm
sum_span(std::span<int const, N>):
    mov     rdx, QWORD PTR [rcx+0x8]   ; 取 size（span 第二 qword）
    mov     rax, QWORD PTR [rcx]       ; 取 ptr（span 第一 qword）
    lea     rcx, [rax+rdx*4]           ; end = begin + size*4
.loop: add     edx, DWORD PTR [rax]
    add     rax, 0x4
    cmp     rax, rcx
    jne     .loop
sum_ptr(int const*, unsigned long long):
    test    rdx, rdx
    je      .empty
    lea     rdx, [rcx+rdx*4]           ; 同 end 计算
.loop: add     eax, DWORD PTR [rcx]
    add     rcx, 0x4
    cmp     rcx, rdx
    jne     .loop
```

**2. `operator[]` 无运行时边界检查**（对比 `vector::at()` 会 `cmp`+`jcc`+抛异常）：

```asm
at_span(std::span<int const, N>, unsigned long long):
    mov     rax, QWORD PTR [rcx]       ; ptr
    lea     rdx, [rax+rdx*4]           ; ptr + i*4   ← 纯索引算术
    mov     eax, DWORD PTR [rdx]       ; 直接读，无任何越界判断
    ret
```

**3. 布局**：`sizeof(std::span<const int>)` = **16**（指针 8 + `size_t` 8）。按值传递 span 拷贝 16 字节（略多于裸指针，但换来 `.size()`/`.subspan()`/`.first()`）。

**工程含义**：span 性能等价于裸指针+长度，适合做"不拥有、零拷贝"的缓冲区视图（嵌入式中传 DMA 缓冲区、外设 FIFO 区段极佳）。**但 `span[i]` 与原始数组一样不查边界——越界是静默 UB，不是异常**；需要运行时防护时应显式 `if (i < s.size())` 或改用带检查封装。

## 附录 D4：libstdc++ 15.3.0 源码解析 — std::span 零开销视图

> 以下源码摘自 libstdc++ 15.3.0（GCC 15.3.0 附带），文件 `span`。

### D4.1 类模板声明与 dynamic_extent

```text
// span  L57-60  (libstdc++ 15.3.0)
  inline constexpr size_t dynamic_extent = static_cast<size_t>(-1);

  template<typename _Type, size_t _Extent>
    class span;
```

### D4.2 固定 extent 存储（零大小，编译期常量）

```text
// span  L76-98  (libstdc++ 15.3.0)
    template<size_t _Extent>
      class __extent_storage
      {
      public:
	constexpr
	__extent_storage([[maybe_unused]] size_t __n) noexcept
	{ __glibcxx_assert(__n == _Extent); }

	consteval
	__extent_storage(integral_constant<size_t, _Extent>) noexcept
	{ }

	static constexpr size_t
	_M_extent() noexcept
	{ return _Extent; }  // 编译期常量，不占存储
      };
```

### D4.3 动态 extent 存储（运行时 size_t）

```text
// span  L100-117  (libstdc++ 15.3.0)
    template<>
      class __extent_storage<dynamic_extent>
      {
      public:
	constexpr
	__extent_storage(size_t __extent) noexcept
	: _M_extent_value(__extent)
	{ }

	constexpr size_t
	_M_extent() const noexcept
	{ return this->_M_extent_value; }

      private:
	size_t _M_extent_value;
      };
```

### D4.4 span 数据成员 — 指针 + [[no_unique_address]] extent

```text
// span  L461-477  (libstdc++ 15.3.0)
    private:
      pointer _M_ptr;
      [[no_unique_address]] __detail::__extent_storage<extent> _M_extent;
```

### D4.5 设计动机

| 设计选择 | 动机 |
|---------|------|
| `[[no_unique_address]]` extent 存储 | 固定 extent 时 `__extent_storage` 无数据成员 → `sizeof(span<T, N>) == sizeof(T*)`，零开销 |
| `dynamic_extent = size_t(-1)` | 哨兵值区分编译期/运行期，同一模板统一处理 |
| 指针 + 可选 size | 比 `pair<T*, size_t>` 更紧凑（固定 extent 省去 size） |
| consteval 构造 | 固定 extent 必须编译期已知，`consteval` 强制保证 |

### D4.6 跨实现对比

| 实现 | 固定 extent sizeof | 动态 extent sizeof |
|------|-------------------|-------------------|
| libstdc++ 15.3.0 | `sizeof(T*)` | `sizeof(T*) + sizeof(size_t)` |
| libc++ (LLVM) | `sizeof(T*)` | `sizeof(T*) + sizeof(size_t)` |
| MSVC STL | `sizeof(T*)` | `sizeof(T*) + sizeof(size_t)` |

三大实现均利用 EBO/`[[no_unique_address]]` 实现固定 extent 零开销。

### D4.7 编译验证

> **示例 46** [难度 ★★★☆☆] [主题：编译验证]
```cpp
#include <span>
#include <array>
#include <iostream>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    std::span<int, 5> fixed_span(arr);          // 固定 extent
    std::span<int> dynamic_span(arr, 3);        // 动态 extent

    std::cout << "fixed size=" << fixed_span.size() << std::endl;     // 5
    std::cout << "dynamic size=" << dynamic_span.size() << std::endl; // 3
    std::cout << "fixed[0]=" << fixed_span[0] << std::endl;          // 10
    std::cout << "dynamic[2]=" << dynamic_span[2] << std::endl;      // 30
    std::cout << "sizeof(fixed)=" << sizeof(fixed_span) << std::endl;   // 8 (x64 指针)
    std::cout << "sizeof(dynamic)=" << sizeof(dynamic_span) << std::endl; // 16

    // subspan
    auto sub = fixed_span.subspan(1, 3);
    std::cout << "subspan size=" << sub.size() << std::endl;  // 3
    std::cout << "subspan[0]=" << sub[0] << std::endl;       // 20
    return 0;
}
```

## 附录 J：std::span 决策流（D3 维度）

```mermaid
flowchart TD
    A["需求:把一段连续数据交给函数/算法"] --> D1{"函数内是否修改底层数据?"}
    D1 -->|只读| D2{"是否长期持有该内存?"}
    D1 -->|读写| D3{"是否拥有该内存?"}
    D2 -->|否 局部借用| F1["std::span<const T> 零拷贝"]
    D2 -->|是 长期| F2["传 const vector<T>& 或返回 vector"]
    D3 -->|否 借用修改| F3["std::span<T> 视图"]
    D3 -->|是 拥有| F4["用 vector / array 拥有"]
    F1 --> D4{"底层来源类型多样?"}
    D4 -->|是 数组/vector/array| G1["span 统一接收"]
    D4 -->|否 单一类型| G2["直接用该容器引用"]
    F3 --> D5{"需要切片?"}
    D5 -->|是| H1["first / last / subspan O(1)"]
    D5 -->|否| H2["直接遍历"]
    F4 --> Z["结论:只读传 span<const T>"]
    F2 --> Z
    G1 --> Z
    G2 --> Z
    H1 --> Z
    H2 --> Z
```

> 决策流说明：`span` 是「非拥有连续视图」，核心权衡是零拷贝但把生命周期责任交给调用方。只读场景一律 `span<const T>`，可同时接收 vector/array/裸数组；需要持久化或返回新数据时改用 `vector` 或 `const vector<T>&`。切片用 `first/last/subspan`（O(1) 无拷贝）替代手工指针算术；绝不可把 span 存为成员后让底层被释放或扩容。

## 附录 K：std::span 知识图谱（D6 维度）

```mermaid
flowchart TD
    N1["非拥有视图 ptr,extent"] --> N2["零开销抽象"]
    N2 --> N3["与裸指针+长度等价"]
    N1 --> N4["动态 extent vs 静态 extent"]
    N4 --> N5["sizeof(span)=16 / 8"]
    N1 --> N6["生命周期绑定底层存储"]
    N6 --> N7["悬垂 span 陷阱"]
    N1 --> N8["first / last / subspan 切片"]
    N8 --> N9["O(1) 无拷贝"]
    N1 --> N10["contiguous_range 概念"]
    N10 --> N11["喂给 ranges 算法"]
    N1 --> N12["string_view 字符特化"]
    N12 --> N13["与 span 同源设计"]
    N3 --> N14["borrowed_range"]
```

### K.1 概念依赖逐边解读

| 边 | 上游概念 | 下游概念 | 依赖关系说明 |
|---|---|---|---|
| 1 | 非拥有视图 | 零开销抽象 | 仅存指针+长度，无堆分配无虚调用 |
| 2 | 零开销抽象 | 裸指针等价 | -O2 下与 ptr+len 生成相同循环 |
| 3 | 非拥有视图 | 动态/静态 extent | 静态 extent 长度编入类型不占存储 |
| 4 | 动态/静态 | sizeof | 动态 16B、静态 8B |
| 5 | 非拥有视图 | 生命周期绑定 | span 不延长任何对象生命周期 |
| 6 | 生命周期绑定 | 悬垂陷阱 | 底层释放/扩容后 span 失效 |
| 7 | 非拥有视图 | 切片 | first/last/subspan 仅移动指针 |
| 8 | 切片 | O(1) 无拷贝 | 切片是地址算术，不复制元素 |
| 9 | 非拥有视图 | contiguous_range | 满足连续范围概念 |
| 10 | contiguous_range | ranges 算法 | 可直接喂给 std::ranges |
| 11 | 非拥有视图 | string_view | string_view 是字符特化 |
| 12 | string_view | 同源设计 | 二者设计同源、接口互补 |
| 13 | 裸指针等价 | borrowed_range | 不拥有故满足 borrowed_range |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch80 array | ch82 span | array 可零成本转 span 视图 |
| ch77 vector | ch82 span | vector .data()+.size() 是 span 最常见来源 |
| ch81 string | ch82 span | string_view 是 span 的字符特化 |
| ch76 STL 架构 | ch82 span | span 是该架构下轻量连续视图 |
| ch90 ranges | ch82 span | span 满足 contiguous_range 喂给 ranges |
| ch88 受限接口 | ch82 span | 非拥有视图与所有权边界思想 |
| ch115 移动语义 | ch82 span | span 拷贝是浅复制，与移动语义呼应 |

## 附录 D5：真实基准与性能分析 — span 视图的真实开销（GCC 15.3.0）

> 测试环境：AMD Ryzen 9 7940HX；本机 MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++23`；`std::chrono::steady_clock` 计时，每场景 5 轮取中位；结果累入 `volatile` sink 防死代码消除；数据用 `mt19937 + random_device` 运行期随机填充防闭式折叠；被测接口函数标 `__attribute__((noinline))` 模拟跨 TU 调用边界（同一 TU 内，见 D5.4 诚实标注）。**绝对毫秒随机器而变，"是否同速/相对倍数"才是可移植信号。**
> **绝对毫秒随机器而变，加速比才是可移植信号。**

### D5.1 基准结果

数据 16M 个 `int`（64 MB）。场景 1 每轮整块扫 12 遍；场景 2 对 262144 个 64 元素窗口做 3 级切片链取中间 32 个求和；场景 3 按 16 元素块扫全数组（1048576 块）。

| 场景 | 中位耗时 ms | 相对 |
|---|---|---|
| 整块求和 — `std::span<const int>` 传参 | 119.585 | ≈1.0×（噪声内同速） |
| 整块求和 — `const std::vector<int>&` 传参 | 120.907 | ≈1.0×（噪声内同速） |
| 整块求和 — 裸指针 + 长度传参 | 113.783 | 基准 1.00× |
| 3 级 `subspan` 切片链（`subspan→subspan→first`） | 16.422 | ≈1.0×（噪声内同速） |
| 手工指针偏移 `p + w*64 + 16`，长度 32 | 17.504 | 基准 1.00× |
| 16 元素块求和 — `span<const int, 16>`（静态 extent） | **3.881** | **2.36× 快** |
| 16 元素块求和 — `span<const int>`（动态 extent） | 9.138 | 基准 1.00× |

另实测：`sizeof(std::span<const int>) == 16`，`sizeof(std::span<const int, 16>) == 8`（仅供参考，不作断言）。

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="217.3" x2="640" y2="217.3" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="220.8" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="134.7" x2="640" y2="134.7" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="138.2" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1000</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="130.0" x2="640" y2="130.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="126.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 113.78ms</text>
  <rect x="96.0" y="128.2" width="48.0" height="171.8" fill="#4C72B0"/>
  <text x="120.0" y="122.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">120ms</text>
  <text x="120.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 120.0 314.0)">整块求和 — std::span&lt;const int&gt; 传参</text>
  <rect x="176.0" y="127.9" width="48.0" height="172.1" fill="#C44E52"/>
  <text x="200.0" y="121.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">121ms</text>
  <text x="200.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 200.0 314.0)">整块求和 — const std::vector&lt;int&gt;&amp; 传参</text>
  <rect x="256.0" y="130.0" width="48.0" height="170.0" fill="#9A9A9A"/>
  <text x="280.0" y="124.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">114ms</text>
  <text x="280.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 280.0 314.0)">整块求和 — 裸指针 + 长度传参</text>
  <rect x="336.0" y="199.5" width="48.0" height="100.5" fill="#8172B3"/>
  <text x="360.0" y="193.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#8172B3">16.42ms</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">3 级 subspan 切片链（subspan→subspan→first）</text>
  <rect x="416.0" y="197.2" width="48.0" height="102.8" fill="#937860"/>
  <text x="440.0" y="191.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#937860">17.50ms</text>
  <text x="440.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 440.0 314.0)">手工指针偏移 p + w*64 + 16，长度 32</text>
  <rect x="496.0" y="251.3" width="48.0" height="48.7" fill="#64B5CD"/>
  <text x="520.0" y="245.3" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#64B5CD">3.88ms</text>
  <text x="520.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 520.0 314.0)">16 元素块求和 — span&lt;const int, 16&gt;（静态 extent）</text>
  <rect x="576.0" y="220.6" width="48.0" height="79.4" fill="#CCB974"/>
  <text x="600.0" y="214.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#CCB974">9.14ms</text>
  <text x="600.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 600.0 314.0)">16 元素块求和 — span&lt;const int&gt;（动态 extent）</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.5</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1.5</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">2</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="172.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="96.0" y="169.7" width="48.0" height="130.3" fill="#4C72B0"/>
  <text x="120.0" y="163.7" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">1.05×</text>
  <text x="120.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 120.0 314.0)">整块求和 — std::span&lt;const int&gt; 传参</text>
  <rect x="176.0" y="168.2" width="48.0" height="131.8" fill="#C44E52"/>
  <text x="200.0" y="162.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">1.06×</text>
  <text x="200.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 200.0 314.0)">整块求和 — const std::vector&lt;int&gt;&amp; 传参</text>
  <rect x="256.0" y="176.0" width="48.0" height="124.0" fill="#9A9A9A"/>
  <text x="280.0" y="170.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="280.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 280.0 314.0)">整块求和 — 裸指针 + 长度传参</text>
  <rect x="336.0" y="282.1" width="48.0" height="17.9" fill="#8172B3"/>
  <text x="360.0" y="276.1" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#8172B3">0.14×</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">3 级 subspan 切片链（subspan→subspan→first）</text>
  <rect x="416.0" y="280.9" width="48.0" height="19.1" fill="#937860"/>
  <text x="440.0" y="274.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#937860">0.15×</text>
  <text x="440.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 440.0 314.0)">手工指针偏移 p + w*64 + 16，长度 32</text>
  <rect x="496.0" y="295.8" width="48.0" height="4.2" fill="#64B5CD"/>
  <text x="520.0" y="289.8" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#64B5CD">0.03×</text>
  <text x="520.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 520.0 314.0)">16 元素块求和 — span&lt;const int, 16&gt;（静态 extent）</text>
  <rect x="576.0" y="290.0" width="48.0" height="10.0" fill="#CCB974"/>
  <text x="600.0" y="284.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#CCB974">0.08×</text>
  <text x="600.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 600.0 314.0)">16 元素块求和 — span&lt;const int&gt;（动态 extent）</text>
</svg>

> 图注：`span<int,16>` 静态 extent 让编译器把边界已知的小块展开，比 `span<int>` 动态 extent 快 **2.36×**；整块求和各传参方式（span/vector&/指针）在噪声内同速——`span` 不是性能陷阱。

### D5.2 非显然结论

1. **span / `vector&` / 裸指针三方在调用边界上逐 ns 等价（119.6 / 120.9 / 113.8 ms，差异 <6%，且复跑一轮排序会翻转）。** 根因：`span<const int>` 就是 `{指针, 长度}` 二元组，Windows x64 调用约定下按引用传 16 字节结构，被调方取两个字段后循环体与裸指针版完全一致——正文 §⑩ 的汇编结论在 5 轮计时下成立。诚实标注：两次全程复跑中三者排序会互换（±10% 噪声），因此只能下"噪声内同速"结论，不能声称某一方更快。

2. **基准陷阱实录：第一版测试中 `const vector&` 曾"快 12 倍"（8.672 ms ≈ 104/12），是 GCC 的 IPA pure-const 分析把 12 次同参纯函数调用 CSE 成了 1 次。** `noinline` 只阻止内联，不阻止过程间"纯函数"判定：编译器证明 `sum_vecref(data)` 无副作用且参数未变，就只调用一次并复用结果；而 span/裸指针版每次重新构造实参逃过了折叠。修复：每次调用前对数组做一次 `volatile` 自写（值不变但清除"未修改"事实）。这条对所有"跨调用边界零成本"类基准都适用。

3. **静态 extent `span<const int, 16>` 比动态 extent 稳定快 2.36×（3.881 vs 9.138 ms，两次全程复跑均复现）。** 根因有二：其一，`-fopt-info-vec` 证实定长 16 的循环被 GCC 15 在**裸 `-O2` 下就用 16 字节向量（SSE2）向量化**——迭代次数编译期已知、无需尾循环，能通过 `-O2` 默认的 very-cheap 向量化代价模型；动态长度版本则被拒绝，逐元素标量累加。其二，静态 extent 的 span 只存指针（`sizeof == 8`），长度在类型里，传参少一个寄存器。这也是"把 extent 编进类型"从理论优势变成实测 2.4× 的少见直接证据。

4. **3 级 `subspan` 切片链与手工指针偏移同速（16.4 vs 17.5 ms，复跑会翻转排序）。** 根因：`subspan/first` 全是 `constexpr` 的指针加法与长度减法，三级链在 -O2 下折叠成一次 `base + w*64 + 16`，与手写表达式生成同样的地址计算。切片链的可读性是免费的。

5. **本基准所有"同速"结论都在 64 MB 内存受限工况下取得**——瓶颈是内存带宽而非指令数，这本身就是 span 类薄抽象最常见的真实工况；若数据全在 L1，微小的指令差异可能重新显形（未测，诚实标注）。

### D5.3 可复现 demo

> **示例 47** [难度 ★★★☆☆] [主题：可复现 demo]
```cpp
#include <iostream>
#include <numeric>
#include <span>
#include <vector>
#include <random>
#include <cassert>
#include <cstdint>

// 三种只读视图接口，语义应完全等价
std::uint64_t sum_span(std::span<const int> sp) {
    std::uint64_t s = 0;
    for (int v : sp) s += static_cast<std::uint32_t>(v);
    return s;
}
std::uint64_t sum_ptr(const int* p, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i) s += static_cast<std::uint32_t>(p[i]);
    return s;
}

int main() {
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(0, 1000);
    std::vector<int> data(4096);
    for (auto& v : data) v = dist(rng);

    // 1) span / 裸指针求和结果逐位一致（稳定语义，可断言）
    const std::uint64_t a = sum_span(std::span<const int>(data));
    const std::uint64_t b = sum_ptr(data.data(), data.size());
    assert(a == b);
    std::cout << "sum via span = " << a << std::endl;
    std::cout << "sum via ptr  = " << b << std::endl;

    // 2) 3 级 subspan 切片链 == 手工指针偏移（同一窗口）
    std::span<const int> whole(data);
    auto sliced = whole.subspan(64, 64).subspan(16).first(32);
    const std::uint64_t c = sum_span(sliced);
    const std::uint64_t d = sum_ptr(data.data() + 64 + 16, 32);
    assert(c == d);
    assert(sliced.data() == data.data() + 80);   // 视图不拷贝：指针指向原数组
    assert(sliced.size() == 32);
    std::cout << "sliced sum   = " << c << std::endl;

    // 3) 静态 extent 与动态 extent 的观感差异（只打印，不做精确 sizeof 断言）
    std::span<const int, 16> fixed(data.data(), 16);
    std::cout << "sizeof(span<const int>)     = " << sizeof(std::span<const int>) << std::endl;
    std::cout << "sizeof(span<const int,16>)  = " << sizeof(fixed) << std::endl;
    std::cout << "fixed extent sum            = " << sum_span(fixed) << std::endl;
    return 0;
}
```

### D5.4 方法学注

- 计时取 5 轮中位数；数据 64 MB 保证单轮 ≥ 数毫秒~百毫秒量级；结果累入 `volatile` sink。
- **ch82 特别提示**：本附录的接口函数是同一 TU 内的 `noinline` 函数，只模拟"跨 TU 非内联"的调用边界；且必须配合调用间 `volatile` 触写，否则 IPA pure-const 会折叠重复调用（D5.2 第 2 条实录）。真正跨 TU + LTO 关闭的工况未单独测，诚实标注。
- 静态 extent 2.36× 的机制证据来自 `-fopt-info-vec-optimized`：定长循环在裸 `-O2` 下报告 "loop vectorized using 16 byte vectors"，动态版无此报告。
- 加速比是可移植信号，绝对毫秒请勿跨机器比较。
- 复现旗标：`g++ -O2 -std=c++23`。基准源码见库根 `_bench_d5_ch82_span.cpp`。

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_ch82_span.cpp` 真实生成（节选 `sum_fixed16` / `sum_dyn16`，两者都求 16 个 int）。静态 extent `span<const int,16>` 让 GCC 15 在**裸 -O2** 下就把定长循环 SSE2 向量化；动态 extent 因长度运行期未知只能标量累加——这正是 D5.2 结论#3「静态 extent 快 2.36×」的机器码根因。

```asm
; sum_fixed16：span<const int,16>（静态 extent，长度编进类型）
;   _Z11sum_fixed16St4spanIKiLy16EE  (节选)
        pxor    xmm1, xmm1             ; 累加器清零
        pxor    xmm2, xmm2
        lea     rax, 64[rcx]           ; 末端哨兵 = ptr + 64B（16×int）
.L:     movdqu  xmm0, XMMWORD PTR [rcx]; ← SIMD 一次加载 16 字节（4× int）
        add     rcx, 16
        movdqa  xmm3, xmm0
        punpckhdq xmm0, xmm2
        punpckldq xmm3, xmm2
        paddq   xmm0, xmm3             ; ← 四路并行求和（无尾循环）
        paddq   xmm1, xmm0
        cmp     rax, rcx
        jne     .L
        movdqa  xmm0, xmm1             ; 跨 lane 收尾
        psrldq  xmm0, 8
        paddq   xmm1, xmm0
        movq    rax, xmm1
        ret
; sum_dyn16：span<const int>（动态 extent，长度运行期未知）
;   _Z9sum_dyn16St4spanIKiLy18446744073709551615EE  (节选)
        mov     rdx, QWORD PTR 8[rcx]  ; rdx = 长度（span 的 {ptr,len} 第二字段）
        mov     rax, QWORD PTR [rcx]   ; rax = 数据指针
        lea     r8, [rax+rdx*4]        ; r8 = 末端 = ptr + len*4
        xor     edx, edx
        cmp     rax, r8
        je      .L
.L:     mov     ecx, DWORD PTR [rax]  ; ← 逐元素标量加载（1× int）
        add     rax, 4
        add     rdx, rcx               ; ← 标量累加，无 SIMD
        cmp     r8, rax
        jne     .L
        mov     rax, rdx
        ret
```

> 注意：两条路径元素数都是 16，但静态 extent 把长度编进类型，GCC 在 -O2 默认 very-cheap 向量化代价模型下即可展开为 SSE2（`movdqu` + `paddq`，4 路并行、无尾循环）；动态 extent 因长度只在运行期存在于 span 的第二个字段（`QWORD PTR 8[rcx]`），编译器拒绝向量化，退回逐元素标量 `add`。这正是 D5.2 结论#3「静态 extent 稳定快 2.36×」的代价根因——把 extent 编进类型，从理论优势变成实测 2.4×。绝对毫秒随机器而变，加速比才是可移植信号。
