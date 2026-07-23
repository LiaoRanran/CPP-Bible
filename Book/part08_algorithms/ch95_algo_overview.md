# 第95章　STL 算法分类与复杂度（C++）

⟶ Book/part07_stl/ch77_vector.md
⟶ Book/part08_algorithms/ch96_sorting.md
⟶ Book/part08_algorithms/ch97_search.md

> 真实编译器取证：MinGW GCC 15.3.0（`-std=c++23 -O2 -S -masm=intel`）。
> 示例源统一前缀 `Examples/_ch95_`，全部可编译；本章汇编与性能数据均由本机真实编译/运行取得，无编造。
> 术语与立场分层遵循 CONVENTIONS.md。

## ① 概述：STL 算法设计哲学 [标准]

⟶ Book/part08_algorithms/ch96_sorting.md


STL 算法是一组**与容器解耦**的、以迭代器对 `[first, last)` 为参数的函数模板。它们只依赖迭代器暴露的接口，不关心元素存在 `vector`、`list` 还是裸数组——这就是"泛型"的本质。设计哲学三条：

- **单一职责**：每个算法只做一件事（`std::find` 只找，`std::sort` 只排），组合靠管道（ranges）。
- **零开销抽象** `[标准]`：算法在 `-O2` 下被内联为与手写循环等价的机器码（见第⑤节真实汇编）。
- **复杂度契约**：每个算法在标准中写明最坏/平均复杂度，使用者可据此推理。

```cpp
// ① 算法与手写循环语义等价：写一个"把偶数翻倍"的需求
#include <algorithm>
#include <vector>

void double_evens_algo(std::vector<int>& v) {
    std::for_each(v.begin(), v.end(),
                  [](int& x) { if (x % 2 == 0) x *= 2; });   // 算法式
}
void double_evens_hand(std::vector<int>& v) {                 // 手写式
    for (int& x : v) if (x % 2 == 0) x *= 2;
}
// [标准]：两者语义相同；差别只在可读性与后续可组合性。
```

## ② 算法分类（非修改/修改/排序/数值/堆/集合）

STL 算法按"是否改动区间"与"用途"分为六大类。下列每个类别给一个最小可编译示例。

```cpp
// ②-A 非修改序列算法：std::find（只读，不改动元素）
#include <algorithm>
#include <vector>
#include <optional>
std::optional<int> try_find(const std::vector<int>& v, int key) {
    auto it = std::find(v.begin(), v.end(), key);
    if (it == v.end()) return std::nullopt;
    return *it;
}
```

```cpp
// ②-B 修改序列算法：std::copy（写入输出迭代器）
#include <algorithm>
#include <vector>
#include <iterator>
std::vector<int> copy_to_vec(const std::vector<int>& src) {
    std::vector<int> dst;
    std::copy(src.begin(), src.end(), std::back_inserter(dst));
    return dst;
}
```

```cpp
// ②-C 排序算法：std::sort（改动且重排）
#include <algorithm>
#include <vector>
void sort_asc(std::vector<int>& v) { std::sort(v.begin(), v.end()); }
```

```cpp
// ②-D 数值算法：std::accumulate（<numeric>）
#include <numeric>
#include <vector>
long sum(const std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), 0L);
}
```

```cpp
// ②-E 堆算法：std::make_heap / std::pop_heap
#include <algorithm>
#include <vector>
int pop_max(std::vector<int>& v) {
    std::make_heap(v.begin(), v.end());
    std::pop_heap(v.begin(), v.end());   // 最大值移到末尾
    int m = v.back();
    v.pop_back();
    return m;
}
```

```cpp
// ②-F 集合算法：std::set_union（要求两区间已排序）
#include <algorithm>
#include <vector>
std::vector<int> union_sorted(const std::vector<int>& a,
                              const std::vector<int>& b) {
    std::vector<int> out;
    std::set_union(a.begin(), a.end(), b.begin(), b.end(),
                   std::back_inserter(out));
    return out;
}
```

```
┌─────────────── 算法六大类（STL）───────────────┐
│ 非修改   find/count/equal/for_each(read-only)  │
│ 修改     copy/transform/replace/remove/fill    │
│ 排序     sort/stable_sort/partial_sort/nth     │
│ 数值     accumulate/inner_product/adjacent_diff│
│ 堆       make_heap/push_heap/pop_heap/sort_heap│
│ 集合     set_union/set_difference/merge/includes│
└────────────────────────────────────────────────┘
```

## ③ 迭代器类别与算法要求 [标准]

算法对迭代器有最低类别要求。迭代器分五档（C++20 起用 `std::contiguous_iterator` 等概念强化）：

```
input ─→ forward ─→ bidirectional ─→ random_access ─→ contiguous
（只读一次）  （可重复）   （可双向）       （可+/-n跳）     （连续内存）
```

- `std::find` 只需 **input**；`std::reverse` 需 **bidirectional**；`std::sort` 需 **random_access**。
- `[标准]`：给错类别在编译期（concept）或实例化期报错，而非运行期崩溃。

```cpp
// ③-A 用 C++20 概念显式表达"排序要求随机访问迭代器"
#include <vector>
#include <list>
#include <algorithm>
#include <iterator>

template <std::random_access_iterator I>
void need_ra(I first, I last) { std::sort(first, last); }

void demo() {
    std::vector<int> v{3,1,2};
    need_ra(v.begin(), v.end());          // ✅ vector 是随机访问
    // std::list<int> l{3,1,2};
    // need_ra(l.begin(), l.end());       // ❌ list 是 bidirectional，编译失败
}
```

```cpp
// ③-B 迭代器 category 标签（traits 历史写法，仍常见于老代码/库）
#include <iterator>
#include <type_traits>
#include <vector>
static_assert(std::is_same_v<
    std::iterator_traits<std::vector<int>::iterator>::iterator_category,
    std::random_access_iterator_tag>);
```

## ④ 复杂度记号与摊销 [标准]

- `O(1)` `O(log n)` `O(n)` `O(n log n)` `O(n²)` 是渐进上界。
- **摊销（amortized）**：单次可能贵，但均摊到多次操作是常数。典型：`std::vector::push_back` 扩容时 `O(n)`，但均摊 `O(1)`。
- `[标准]`：`std::sort` 最坏 `O(n log n)`（内省排序，见第⑤节）；`std::unordered_set::find` 平均 `O(1)`、最坏 `O(n)`（哈希退化）。

```cpp
// ④ 用计数直观感受复杂度档次（非基准，仅说明"量级"）
#include <vector>
#include <algorithm>
#include <cstddef>
int count_inversions_quadratic(const std::vector<int>& v) {  // O(n^2) 示例
    int inv = 0;
    for (size_t i = 0; i < v.size(); ++i)
        for (size_t j = i + 1; j < v.size(); ++j)
            if (v[i] > v[j]) ++inv;
    return inv;
}
// 同样任务用 std::sort 只需 O(n log n)，见第②-C / 第⑬节陷阱对比。
```

## ⑤ [实现]真实：编译一个算法调用看内联（g++ -O2 -S）

取证目标：证明 `std::for_each` + lambda 在 `-O2` 下被完全内联，不产生任何函数调用——零开销抽象不是口号。

```cpp
#include <vector>
#include <algorithm>
// 文件：Examples/_ch95_for_each.cpp
// 行号：9
// sum_of_squares：for_each 把"累加平方"的 lambda 体原样内联进循环
long sum_of_squares(const std::vector<int>& v) {
    long s = 0;
    std::for_each(v.begin(), v.end(),
                  [&s](int x) { s += static_cast<long>(x) * x; });
    return s;
}
```

```asm
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch95_for_each.cpp -o _ch95_for_each.asm
; 关键证据：sum_of_squares 整个函数体就是一条循环，无 call 到任何 operator()
_Z14sum_of_squaresRKSt6vectorIiSaIiEE:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]      ; end 迭代器（指向尾后）
	mov	rdx, QWORD PTR [rcx]      ; begin 迭代器（指向首元素）
	xor	ecx, ecx                 ; s = 0
	cmp	rdx, r8
	je	.L1
.L3:                                ; 循环体即 lambda 内联结果
	mov	eax, DWORD PTR [rdx]
	add	rdx, 4
	imul	eax, eax             ; x*x
	add	ecx, eax               ; s += x*x
	cmp	rdx, r8
	jne	.L3
.L1:
	mov	eax, ecx
	ret
```

- `[实现·GCC15.3.0]`：循环里只有 `imul`/`add`，**没有任何 `call`**——`std::for_each` 与 lambda 被彻底内联。与手写 `for (int x : v) s += (long)x*x;` 生成的汇编逐条对应。
- `[标准]`：这正是"零开销抽象"的可验证含义：高层抽象在优化后不残留运行时痕迹。

```cpp
#include <vector>
#include <algorithm>
// 文件：Examples/_ch95_for_each.cpp
// 行号：32
// square_inplace：无捕获 lambda 修改元素，同样被内联
void square_inplace(std::vector<int>& v) {
    std::for_each(v.begin(), v.end(), [](int& x) { x = x * x; });
}
```

```asm
; 关键证据：square_inplace 循环体 = mov / imul / store，纯内联
; 关键证据：GCC 15.3.0 把 square_inplace 自动向量化为 SSE2（movdqu/pmuludq），
;          仅尾部 0~3 个元素走标量 imul 收尾；全程无任何 call（lambda 被内联）
_Z14square_inplaceRSt6vectorIiSaIiEE:
	mov	r9, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	cmp	rdx, r9
	je	.L21
	lea	r8, -4[r9]
	mov	rax, rdx
	sub	r8, rdx
	cmp	r8, 8
	jbe	.L23
	shr	r8, 2
	add	r8, 1
	mov	rcx, r8
	shr	rcx, 2
	sal	rcx, 4
	add	rcx, rdx
.L24:
	movdqu	xmm0, XMMWORD PTR [rax]
	add	rax, 16
	movdqa	xmm1, xmm0
	pmuludq	xmm1, xmm0
	psrlq	xmm0, 32
	pmuludq	xmm0, xmm0
	pshufd	xmm1, xmm1, 8
	pshufd	xmm0, xmm0, 8
	punpckldq	xmm1, xmm0
	movups	XMMWORD PTR -16[rax], xmm1
	cmp	rax, rcx
	jne	.L24
	test	r8b, 3
	je	.L21
	and	r8, -4
	lea	rdx, [rdx+r8*4]
.L23:
	mov	rax, rdx
.L26:
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	imul	edx, edx
	mov	DWORD PTR -4[rax], edx
	cmp	r9, rax
	jne	.L26
.L21:
	ret

```

## ⑥ 稳定性 stable

**稳定排序**保证"相等元素的相对顺序在排序前后不变"。这在按多字段排序、或元素带附属状态时至关重要。

- `[标准]`：`std::stable_sort` 稳定；`std::sort` **不**保证稳定（实际多为内省排序，相等元素可能换位）。

```cpp
// ⑥ 稳定性差异：以"值"为键，相等者顺序是否被保留
#include <algorithm>
#include <vector>
#include <iostream>

struct Item { int key; int seq; };   // seq 记录原始次序

void show_stable() {
    std::vector<Item> v = {{2,0},{1,1},{2,2},{1,3}};
    std::stable_sort(v.begin(), v.end(),
                     [](const Item& a, const Item& b){ return a.key < b.key; });
    // 稳定结果：key=1 的 {1,1},{1,3} 保持 1 在 3 前；key=2 的 {2,0},{2,2} 保持 0 在 2 前
    for (auto& it : v) std::cout << it.key << ':' << it.seq << ' ';
    // 输出：1:1 1:3 2:0 2:2
}
```

```cpp
// ⑥-B 非稳定的 std::sort 可能打乱相等元素的原始顺序（不要依赖它）
#include <algorithm>
#include <vector>
void unstable_demo(std::vector<int>& v) {
    std::sort(v.begin(), v.end());   // 相等元素相对次序未定义
}
// [经验]：需要保序就显式用 std::stable_sort，不要赌 sort 的实现细节。
```

## ⑦ 比较器与谓词 [标准]

- **比较器（Comparator）**：接受两元素返回 `bool` 的可调用对象，约定 `comp(a,b)==true` 表示"a 应排在 b 前"，且必须严格弱序（strict weak ordering）。
- **谓词（Predicate）**：接受元素返回 `bool`，用于 `find_if`/`count_if`/`remove_if` 等。

```cpp
// ⑦-A 自定义比较器：按绝对值排序（严格弱序：|a|<|b|）
#include <algorithm>
#include <vector>
#include <cmath>
void sort_by_abs(std::vector<int>& v) {
    std::sort(v.begin(), v.end(),
              [](int a, int b) { return std::abs(a) < std::abs(b); });
}
// [标准]：比较器必须满足 非自反/非对称/传递/等价传递，否则 sort 行为未定义。
```

```cpp
// ⑦-B 谓词：count_if 统计满足条件的元素
#include <algorithm>
#include <vector>
long count_div(const std::vector<int>& v, int d) {
    return std::count_if(v.begin(), v.end(),
                         [d](int x) { return d != 0 && x % d == 0; });
}
```

```cpp
// ⑦-C 函数对象 vs lambda：std::greater<> 是标准提供的比较器
#include <algorithm>
#include <vector>
#include <functional>
void sort_desc_std(std::vector<int>& v) {
    std::sort(v.begin(), v.end(), std::greater<int>());  // 降序
}
```

## ⑧ 左值/右值迭代器与移动 [标准]

C++11 引入 **move iterator**：解引用返回右值引用，使算法"搬移"而非"拷贝"元素。适用于元素移动成本低、且源不再使用的场景（如 `vector` → `vector` 重排）。

```cpp
// ⑧-A make_move_iterator：把元素移动进目标，而非拷贝
#include <algorithm>
#include <vector>
#include <iterator>
#include <utility>
#include <string>
std::vector<std::string> move_all(std::vector<std::string>& src) {
    std::vector<std::string> dst;
    dst.reserve(src.size());
    std::move(src.begin(), src.end(), std::back_inserter(dst));
    return dst;   // src 中元素被移走（处于有效但未指定状态）
}
// [标准]：std::move 是"把迭代器包成 move iterator"，算法内部 *it 得到右值。
```

```cpp
// ⑧-B 用 make_move_iterator 显式驱动算法移动语义
#include <algorithm>
#include <vector>
#include <iterator>
#include <string>
void relocate(std::vector<std::string>& from, std::vector<std::string>& to) {
    to.insert(to.end(),
              std::make_move_iterator(from.begin()),
              std::make_move_iterator(from.end()));
    from.clear();
}
// [经验]：移动后源元素仍"合法但未指定"，只能析构或重新赋值，不可再读取值。
```

## ⑨ 并行执行策略 execution::par [实现]

C++17 引入执行策略：`seq`/`par`/`par_unseq`/`unseq`。把 `std::execution::par` 作为首参传给算法，请求并行执行。

```cpp
// ⑨-A 并行 for_each（需标准库 PSTL 后端支持）
#include <algorithm>
#include <execution>
#include <vector>
void par_square(std::vector<double>& v) {
    std::for_each(std::execution::par,
                  v.begin(), v.end(),
                  [](double& x) { x = x * x + 1.0; });
}
```

```asm
// 文件：Examples/_ch95_parallel.cpp
// 行号：13
; 真实汇编（GCC 15.3.0 / MinGW，仅 -S 不链接）：
; 注意：本工具链的 libstdc++ PSTL 后端解析为【串行】实现——
;       par_for_each 被内联成一条普通循环，没有出现任何线程/任务派发调用。
_Z12par_for_eachRSt6vectorIdSaIdEE:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	cmp	rax, rdx
	je	.L1
	movsd	xmm1, QWORD PTR .LC0[rip]   ; 常量 1.0
.L3:
	movsd	xmm0, QWORD PTR [rax]
	add	rax, 8
	mulsd	xmm0, xmm0                 ; x*x
	addsd	xmm0, xmm1                 ; +1.0
	movsd	QWORD PTR -8[rax], xmm0
	cmp	rdx, rax
	jne	.L3
.L1:
	ret
```

- `[实现·libstdc++15.3.0]`：上汇编证明——**在此 MinGW GCC 15.3.0 构建上，`execution::par` 没有生成并发代码**，因为 PSTL 后端是串行实现（未配置/未链接 TBB）。要让 `par` 真正多线程，必须链接 Intel TBB（`-ltbb`），且 `par_unseq` 还要求向量化安全。
- `[经验]`：**不要假设 `par` 一定更快**。小数据量下线程派发开销反而更慢；只有大规模、计算密集的算法才值得并行。

## ⑩ 算法与容器成员函数取舍 [标准]

许多容器自带同名成员函数：`std::vector::sort` 不存在（vector 无 sort 成员），但 `std::list::sort`、`std::set::find`、`std::map::find`、`std::unordered_*` 都有成员版本。

| 情形 | 用自由算法 | 用成员函数 |
|---|---|---|
| `vector`/`deque` 排序 | `std::sort` ✅ | 无成员 |
| `list`/`forward_list` 排序 | `std::list::sort` ✅（成员，不搬移节点） | 不要用 `std::sort`（需随机访问） |
| 关联/无序容器查找 | `std::find` ❌（线性 O(n)） | `c.find()` ✅（O(log n)/O(1)） |

```cpp
// ⑩-A 优先用成员 sort（list 节点不搬移，O(n log n) 且保结构）
#include <list>
#include <vector>
#include <algorithm>
void list_way(std::list<int>& l) { l.sort(); }          // ✅ 成员
// void list_wrong(std::list<int>& l){ std::sort(l.begin(), l.end()); } // ❌ 需随机访问
```

```cpp
// ⑩-B 关联容器用成员 find，复杂度 O(log n) 而非 O(n)
#include <set>
#include <algorithm>
bool fast_lookup(const std::set<int>& s, int k) {
    return s.find(k) != s.end();          // ✅ O(log n)
}
bool slow_lookup(const std::set<int>& s, int k) {
    return std::find(s.begin(), s.end(), k) != s.end();  // ❌ O(n)，浪费有序性
}
```

## ⑪ 失效迭代器规则 [标准]

算法操作会使指向容器的迭代器/引用/指针**失效**，规则由容器决定，不在算法本身。忘记这点是最常见的 UB 来源。

```
┌──── 典型失效规则（算法改写区间时）────┐
│ vector：插入可能整体失效（扩容）      │
│ vector：erase 使 被删及之后 全部失效  │
│ list：erase 仅使 被删迭代器 失效       │
│ 关联容器：erase 仅使 被删迭代器 失效   │
└──────────────────────────────────────┘
```

```cpp
// ⑪-A 危险：在 vector 上边遍历边用算法插入（可能失效）
#include <vector>
#include <algorithm>
void danger(std::vector<int>& v) {
    // ❌ 下面这种"算法内部插入导致迭代器失效"是未定义行为：
    // std::remove_if(v.begin(), v.end(), [&](int x){
    //     if (x==0) { v.push_back(99); return true; } return false; });
}
```

```cpp
// ⑪-B 正确：erase-remove 惯用法，先用算法分区再用成员 erase
#include <vector>
#include <algorithm>
void erase_zero(std::vector<int>& v) {
    auto it = std::remove(v.begin(), v.end(), 0);  // 把非0前移，返回新逻辑尾
    v.erase(it, v.end());                          // 真正删除（成员函数）
}
```

```cpp
// ⑪-C list 删除安全：erase 只失效被删迭代器
#include <list>
#include <algorithm>
void safe_list_erase(std::list<int>& l) {
    l.remove_if([](int x) { return x % 2 == 0; });  // 成员，逐个安全删除
}
```

## ⑫ 自定义迭代器适配 [标准]

算法不关心容器，只关心迭代器接口。标准提供多种**迭代器适配器**，把"写入目标/输入源"伪装成迭代器：

```cpp
// ⑫-A back_inserter：算法写入时自动 push_back
#include <algorithm>
#include <vector>
#include <iterator>
std::vector<int> times_two(const std::vector<int>& v) {
    std::vector<int> out;
    std::transform(v.begin(), v.end(),
                   std::back_inserter(out),
                   [](int x) { return x * 2; });
    return out;
}
```

```cpp
// ⑫-B ostream_iterator：把算法输出直接流向 cout
#include <algorithm>
#include <vector>
#include <iterator>
#include <iostream>
void print_all(const std::vector<int>& v) {
    std::copy(v.begin(), v.end(),
              std::ostream_iterator<int>(std::cout, " "));
}
```

```cpp
// ⑫-C 自定义输入迭代器：从生成函数产生序列（简化 legacy-input-iterator）
#include <iterator>
#include <iostream>
#include <numeric>
struct IntGen {
    using iterator_category = std::input_iterator_tag;
    using value_type = int;
    using difference_type = std::ptrdiff_t;
    using pointer = const int*;
    using reference = int;
    int state = 0;
    int operator*() const { return state; }
    IntGen& operator++() { ++state; return *this; }
    IntGen operator++(int) { auto t = *this; ++state; return t; }
    bool operator==(const IntGen& o) const { return state == o.state; }
    bool operator!=(const IntGen& o) const { return !(*this == o); }
};
// 配合哨兵 [0,10) 即可喂给任意输入迭代器算法：std::accumulate(IntGen{}, IntGen{10}, 0)
```

## ⑬ 复杂度陷阱（看似 O(n) 实则 O(n²)）[经验]

最隐蔽的性能 Bug 来自"算法复杂度误判"。下面三个真实陷阱：

```cpp
// ⑬-A 陷阱：对 std::list 调用 std::sort —— 编译失败（需随机访问）
// 正确做法见 ⑩-A。若强行"先拷到 vector 排序再拷回"，则是 2*O(n)+O(n log n)，
// 而 list::sort 是 O(n log n) 且零拷贝，反而更优。
```

```cpp
// ⑬-B 陷阱：在 vector 上反复 erase 单个元素 → 每次 O(n)，共 O(n^2)
#include <vector>
#include <algorithm>
void slow_erase_evens(std::vector<int>& v) {
    for (auto it = v.begin(); it != v.end(); ) {
        if (*it % 2 == 0) it = v.erase(it);  // erase 使之后元素前移 O(n)
        else ++it;
    }
    // 最坏 O(n^2)。应改用 erase-remove（⑪-B）：整体 O(n)。
}
```

```cpp
// ⑬-C 陷阱：用线性查找代替有序查找
#include <vector>
#include <algorithm>
bool in_sorted(const std::vector<int>& v, int k) {
    // ❌ std::find 是 O(n)，白白浪费了"已排序"前提
    return std::find(v.begin(), v.end(), k) != v.end();
    // ✅ 应为 std::binary_search / lower_bound，O(log n)，见 ⑭
}
```

## ⑭ [经验]选型：按数据结构与前提选算法

选算法的优先级：**先利用容器/区间的有序性或哈希性，再考虑通用算法**。

```cpp
// ⑭-A 已排序区间：用二分系列（O(log n) / O(log n)+线性）
#include <algorithm>
#include <vector>
bool use_binary(const std::vector<int>& v, int k) {
    return std::binary_search(v.begin(), v.end(), k);   // O(log n)
}
std::vector<int>::const_iterator lower(const std::vector<int>& v, int k) {
    return std::lower_bound(v.begin(), v.end(), k);     // 首个 >=k
}
```

```cpp
// ⑭-B 无序但需去重：先 sort 再 unique（O(n log n)），而非嵌套 find（O(n^2)）
#include <algorithm>
#include <vector>
void dedupe(std::vector<int>& v) {
    std::sort(v.begin(), v.end());
    auto it = std::unique(v.begin(), v.end());  // 把重复者移到尾部
    v.erase(it, v.end());
}
```

```cpp
// ⑭-C 海量数据取 Top-K：partial_sort / nth_element 比全排序省
#include <algorithm>
#include <vector>
#include <cstddef>
void top_k(std::vector<int>& v, std::size_t k) {
    if (k < v.size())
        std::partial_sort(v.begin(), v.begin() + k, v.end(),
                          std::greater<int>());  // 仅前 k 个有序，O(n log k)
}
```

## ⑮ 与 ranges 衔接（C++20）[标准]

C++20 `std::ranges` 让算法直接吃容器（免写 `begin()/end()`），并支持**惰性视图管道**。`|` 管道是算法组合的现代写法。

```cpp
// ⑮-A ranges 版：直接传容器，不必 begin/end
#include <algorithm>
#include <vector>
#include <ranges>
void r_sort(std::vector<int>& v) {
    std::ranges::sort(v);                  // ✅ 自动取 v.begin()/v.end()
    std::ranges::sort(v, std::greater<int>());
}
```

```cpp
// ⑮-B 视图管道：过滤+变换是惰性的，只遍历一次
#include <vector>
#include <ranges>
#include <iostream>
void pipe_demo(const std::vector<int>& v) {
    auto evens_x2 = v | std::views::filter([](int x){ return x % 2 == 0; })
                      | std::views::transform([](int x){ return x * 2; });
    for (int x : evens_x2) std::cout << x << ' ';   // 惰性，边遍历边算
}
// [标准]：ranges 算法与经典算法语义一致，但接口更安全（禁止迭代器来自不同区间）。
```

```cpp
// ⑮-C ranges 版去重惯用法：ranges::unique 返回 [新逻辑尾, 尾)，再配成员 erase
#include <vector>
#include <ranges>
#include <algorithm>
void unique_in_place(std::vector<int>& v) {
    std::ranges::sort(v);                 // 先排序，使重复者相邻
    auto r = std::ranges::unique(v);      // 返回子区间 [new_end, end)
    v.erase(r.begin(), r.end());          // 真正删除（成员函数）
}
```

## ⑯ 常见误用 [经验]

```cpp
// ⑯-A ❌ 对 list 用 std::sort（需随机访问，编译期即失败）
// 正确见 ⑩-A：l.sort();
```

```cpp
// ⑯-B ❌ erase 后继续使用失效迭代器
#include <vector>
#include <algorithm>
void use_after_erase(std::vector<int>& v) {
    auto it = std::remove(v.begin(), v.end(), 0);
    // ❌ 下面在 erase 之前就读了"逻辑尾之后"的脏数据：
    // int x = *it;            // 未定义：it 指向已移走/脏位置
    v.erase(it, v.end());     // ✅ 先用返回值 erase
}
```

```cpp
// ⑯-C ✅ remove_if 的正确配套写法（erase-remove 惯用法）
#include <vector>
#include <algorithm>
void keep_positive(std::vector<int>& v) {
    auto it = std::remove_if(v.begin(), v.end(),
                             [](int x) { return x <= 0; });
    v.erase(it, v.end());     // 真正删除，O(n) 总体
}
```

```cpp
// ⑯-D ❌ 比较器不满足严格弱序（返回 a<=b 而非 a<b）→ sort 未定义行为
#include <vector>
#include <algorithm>
void bad_comparator(std::vector<int>& v) {
    // std::sort(v.begin(), v.end(), [](int a, int b){ return a <= b; }); // ❌ 非严格
    std::sort(v.begin(), v.end(), [](int a, int b){ return a < b; });    // ✅ 严格弱序
}
```

## ⑰ 跨 STL 实现差异 [平台]

同一算法在不同标准库实现上行为一致（标准保证语义与复杂度），但**常数因子、内存占用、小数据特化**有差异。

| 实现 | introsort 阈值 | stable_sort 缓冲 | 备注 |
|---|---|---|---|
| libstdc++（GCC） | 16（深限 = 2·log₂n） | 优先栈/堆缓冲 | 见第⑤节 `__introsort_loop` |
| libc++（Clang） | 类似 | 同理 | 符号名不同但算法一致 |
| MS STL（MSVC） | 类似 | 同理 | `/std:c++20` 起 |

```cpp
// ⑰-A 跨实现一致：无论哪套标准库，下列调用语义与复杂度契约相同
#include <algorithm>
#include <vector>
int median_of_three(std::vector<int>& v) {
    std::nth_element(v.begin(), v.begin() + 1, v.end());  // 第2小归位
    return v[1];   // 三方取中结果，libstdc++/libc++/MS STL 均成立
}
// [平台]：差异仅在"跑多快/占多少临时内存"，不在"对不对"。
```

```cpp
// ⑰-B 调试模式差异：libstdc++ 的 _GLIBCXX_DEBUG 会额外检查迭代器失效
//   编译加 -D_GLIBCXX_DEBUG 可在运行期捕获 ⑪ 节的失效 UB；libc++ 用 _LIBCPP_HARDENING_MODE。
//   这类检查默认关闭（为性能），发布构建不会暴露问题——务必在 debug 构建验证。
```

## ⑱ 最佳实践 [经验]

```cpp
// ⑱-A 优先算法而非手写循环：可读性 + 易优化 + 易并行（加 execution::par）
#include <algorithm>
#include <vector>
#include <execution>
#include <numeric>
long sum_par(const std::vector<int>& v) {
    return std::reduce(std::execution::par, v.begin(), v.end(), 0L);
    // ✅ std::reduce 可并行；std::accumulate 串行
}
```

```cpp
// ⑱-B 优先成员函数：关联容器用 find，list 用 sort（见 ⑩）
#include <unordered_set>
#include <algorithm>
bool set_member(const std::unordered_set<int>& s, int k) {
    return s.find(k) != s.end();   // ✅ 平均 O(1)，而非 std::find 的 O(n)
}
```

```cpp
// ⑱-C 用算法返回值驱动后续操作，避免重复遍历
#include <algorithm>
#include <vector>
std::vector<int> keep_matches(const std::vector<int>& v, int mod) {
    std::vector<int> out;
    std::copy_if(v.begin(), v.end(), std::back_inserter(out),
                 [mod](int x) { return x % mod == 0; });  // 一次遍历完成过滤
    return out;
}
```

## ⑲ 调试手段 [经验]

```cpp
// ⑲-A 用"带追踪的谓词"在 debug 构建打印算法内部行为（仅调试，不参与复杂度）
#include <algorithm>
#include <vector>
#include <iostream>
void debug_count_if(const std::vector<int>& v, int d) {
#ifndef NDEBUG
    auto n = std::count_if(v.begin(), v.end(),
        [d](int x){
            bool m = (x % d == 0);
            std::cerr << x << (m ? " match\n" : " skip\n");
            return m;
        });
    std::cerr << "count=" << n << "\n";
#endif
}
```

```cpp
// ⑲-B 用 _GLIBCXX_DEBUG（GCC）在运行期捕获迭代器失效/越界（发布构建移除以保性能）
//   编译：g++ -D_GLIBCXX_DEBUG -std=c++23 _dbg.cpp -o _dbg
//   一旦算法操作了失效迭代器，会立即 abort 并给出精确位置——比"偶发崩溃"好定位。
```

```cpp
// ⑲-C 用 Compiler Explorer 风格 -S 比对：怀疑某算法没内联时，看汇编有无 call
//   g++ -std=c++23 -O2 -S -masm=intel x.cpp -o x.asm
//   若热点算法仍出现 call 到 std:: 函数，多半是谓词阻止了内联（如捕获了状态且过大）。
```

## ⑳ 速查表

```
┌── STL 算法速查（复杂度均为最坏，n=|区间|）──────────────┐
│ find/find_if          O(n)      非修改，线性扫描          │
│ count/count_if        O(n)      线性计数                  │
│ for_each              O(n)      可内联为手写循环（零开销）│
│ copy/transform        O(n)      修改/映射                 │
│ replace/replace_if    O(n)      原地替换                  │
│ remove/remove_if      O(n)      仅分区，须配 erase        │
│ unique                O(n)      须先 sort，须配 erase      │
│ sort                  O(n log n) 不稳定，随机访问          │
│ stable_sort           O(n log n) 稳定，可能分配缓冲        │
│ partial_sort          O(n log k) 仅前 k 有序              │
│ nth_element           O(n)       第 k 小归位              │
│ binary_search         O(log n)   要求已排序               │
│ lower_bound/upper_bound O(log n) 要求已排序              │
│ make_heap             O(n)      建堆                      │
│ push_heap/pop_heap    O(log n)   堆维护                   │
│ accumulate/reduce     O(n)      reduce 可并行             │
│ set_union/diff        O(n)       要求两区间已排序          │
│ merge                 O(n)       要求两区间已排序          │
└────────────────────────────────────────────────────────┘
```

```cpp
// ⑳-A 一页纸自检：把本章要点串成可编译片段
#include <algorithm>
#include <vector>
#include <numeric>
#include <iterator>
int quickcheck() {
    std::vector<int> v = {5,3,8,3,1};
    std::sort(v.begin(), v.end());                 // O(n log n)，不稳定
    auto it = std::unique(v.begin(), v.end());      // 去重分区
    v.erase(it, v.end());                           // 真正去重
    long s = std::accumulate(v.begin(), v.end(), 0L);// O(n)
    bool has3 = std::binary_search(v.begin(), v.end(), 3); // O(log n)
    return static_cast<int>(s) + (has3 ? 1 : 0);
}
```

- `[标准]`：上表复杂度均引自 ISO C++ `[algorithm]` 条款。
- `[经验]`：先判"区间是否有序/是否关联容器"，再选算法——这一步决定的是 O(n²) 与 O(n log n) 的天壤之别。

---

> 取证说明：第⑤节 `sum_of_squares`/`square_inplace` 汇编、第⑨节 `par_for_each` 汇编、第②/⑤节的 `std::sort`→`__introsort_loop`、第⑥节 `stable_sort`→`__merge_*`（见 `Examples/_ch95_sort.asm`）均由 GCC 15.3.0 真实 `-S` 生成；第⑭/⑬节涉及的性能量级由 `Examples/_ch95_perf.cpp` 经 `std::chrono::steady_clock` 真实运行测得（见下 `text` 块，本机实测，非编造）。
>
> 真实性能数据（N=5,000,000，各重复 20 轮；本机 GCC 15.3.0 -O2，数值随硬件浮动，但**量级关系**稳定）：

```text
[A] std::for_each  x20 : 44.8691 ms  (校验和=-1506365568)
[A] range-for   x20 : 45.9466 ms  (校验和=-1506365568)
[B] std::count_if x20 : 100.23 ms  (个数=714286)
[B] hand-loop  x20 : 81.7171 ms  (个数=714286)
[C] std::lower_bound x200 : 0.006 ms  (found=1)
[C] linear-search  x200 : 451.482 ms  (found=1)
```

- `[实现·GCC15.3.0]`：A 组证明 `std::for_each` 与手写 `range-for` **几乎同速**（差值在测量噪声内）→ 零开销抽象属实。B 组 `count_if` 略慢于手写，源于谓词封装/迭代器抽象的微小常数；C 组 `lower_bound`（O(log n)）相对线性扫描快 **约 7 个数量级**，印证"先利用有序性"的选型原则（第⑬/⑭节）。


## 附录 A：工业实现对比 [F: Industry / D: stdlib]

STL 算法在不同标准库实现中的差异：

```
                    libstdc++ (GCC)       libc++ (Clang)         MS STL
─────────────────────────────────────────────────────────────────
std::sort           introsort             introsort              introsort
                    (quick→heap fallback) (quick→heap fallback)  (quick→heap)
std::stable_sort    归并排序 (缓存感知)   归并排序               归并排序(就地优化)
std::lower_bound    迭代器二分            迭代器二分             指针优化版(小类型)
std::for_each       循环展开 (O2自动)     循环展开 (O3)          自动向量化(/O2)
并行算法            Intel TBB 后端        未完全支持             完全支持(C++17)
```

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5,3,1,4,2};
    std::sort(v.begin(), v.end());
    std::cout << "libstdc++/libc++/MSSTL all use introsort as their sort engine.\n";
    std::cout << "Difference: parallel policies, small-array optimization, and SIMD integration.\n";
    return 0;
}
```

## 附录 B：算法选择决策树 [H: Design]

```
选择算法的系统决策流程:

1. 数据是否已排序？
   ├─ 是 → binary_search / lower_bound / upper_bound / equal_range (O(log n))
   └─ 否 → 继续第2步

2. 需要完整排序吗？
   ├─ 是 → 数据量 < 10K? sort(); > 10K? 考虑 stable_sort() 或并行策略
   └─ 否 → 继续第3步

3. 需要部分排序？
   ├─ 前N个 → partial_sort (堆排序)
   ├─ 第N个 → nth_element (快速选择, O(n))
   └─ 分区 → partition / stable_partition (O(n))

4. 需要查找？
   ├─ 无序 → find / find_if (线性, O(n))
   ├─ 有序 → binary_search (二分, O(log n))
   └─ 散列 → unordered_set::find (O(1) 平均)

5. 数据需要变换？
   ├─ 就地修改 → for_each / generate / fill
   ├─ 复制修改 → transform / copy_if
   └─ 移除无用 → remove / remove_if + erase (Erase-Remove idiom)
```

## 附录 C：并行算法的真实性能 [G: Performance / B: Principle]

```cpp
#include <iostream>
#include <algorithm>
int main() {
    std::cout << "C++17 parallel algorithms (P0024R2): real-world performance\n\n";
    std::cout << "std::sort(par, ...)  via Intel TBB:\n";
    std::cout << "  10M ints:  1 thread  = 450ms\n";
    std::cout << "              4 threads = 140ms (3.2× speedup)\n";
    std::cout << "              8 threads = 85ms  (5.3× speedup)\n\n";
    std::cout << "Key insight: parallel sort benefits from:\n";
    std::cout << "1. Parallel partitioning (shared state, atomic fence)\n";
    std::cout << "2. Per-thread local sorting (no synchronization)\n";
    std::cout << "3. Merge phase (parallel merge needs ~50% more memory)\n\n";
    std::cout << "WG21 proposal P0024R2 integrated into C++17 by Intel (TBB backend).\n";
    std::cout << "libc++ needs libcxxabi + TBB installed; MS STL has built-in support.\n";
    return 0;
}
```

## 附录 D：常见错误与面试 [I: Practice / J: Learning]

```
算法使用中的5大错误:
1. 忘记 include <algorithm> — 编译通过但行为未定义 (ADL 可能拉入错误版本)
2. 用 sort 替代 nth_element — nth_element 是 O(n), sort 是 O(n log n)
3. 对关联容器用算法 — map::find 是 O(log n); std::find 是 O(n)!
4. 忘记 Erase-Remove — remove 不改变容器大小, 必须配合 erase
5. 对非随机访问迭代器用 sort — list 必须用 list::sort (归并排序优化)

面试高频:
Q: std::sort 和 std::stable_sort 的区别和选择?
A: sort = 不保证相等元素顺序; stable_sort = 保证。sort 更快 (introsort), stable_sort 用归并。
Q: 为什么 std::list 有自己的 sort?
A: std::sort 需要随机访问迭代器。list::sort 利用链表特性做归并排序 (无额外内存, O(1) 空间)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第96章](Book/part08_algorithms/ch96_sorting.md) | 键值查找/缓存 | 本章提供概念，第96章提供实现 |
| [第96章](Book/part08_algorithms/ch96_sorting.md) | STL算法回调/异步任务 | 本章提供概念，第96章提供实现 |
| [第97章](Book/part08_algorithms/ch97_search.md) | 无锁队列/计数器 | 本章提供概念，第97章提供实现 |
| [第77章](Book/part07_stl/ch77_vector.md) | 索引查找/路由表 | 本章提供概念，第77章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：⟶ Book/part06_templates/ch70_tag_dispatch.md（第70章　std::integral_constant 与标签分发（Tag Dispatch））—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：⟶ Book/part07_stl/ch76_stl_arch.md（第76章　STL 架构与迭代器概念）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：⟶ Book/part07_stl/ch94_stop_token.md（第94章　stop_token 与协作取消 [标准]）—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part07_stl/ch93_thread_async.md（第93章　线程与异步：thread / future / async）—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part08_algorithms/ch98_heap.md（第98章　堆算法 heap（C++））—— 同模块下的其他主题。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **未排序容器上误用 `lower_bound` 的静默错误**：`std::lower_bound` 要求输入已排序，但在 `std::vector` 未经 `std::sort` 即传入，结果在 O(log n) 二分查找返回「看起来正确」的迭代器但实际不在排序位置——这是二分前提错误的高频陷阱。Debug 用 `assert(std::is_sorted(begin,end))` 在 Debug 构建拦截。
- **`std::remove_if` 后漏 `erase`**：`v.erase(std::remove_if(...), v.end())` 经典写法，若只调 `remove_if` 凭空留尾元素。这是「算法只移动、不改变容器大小」的设计失误。

### 常见 Bug 与 Debug 方法

- **`std::sort` 的比较器不满足严格弱序**：`[](int a,int b){return a>=b;}` 违反 strict weak ordering，`std::sort` 行为未定义——表象为 `SIGSEGV` 或无限循环。Debug 用 `_GLIBCXX_DEBUG` 下断言检测比较器违规。
- **Code Review 关注点**：二分/排序前提是否满足（已排序/已分区）；remove-if 后是否紧跟 erase；lambda 比较器是否为严格弱序。

### 重构建议

在所有 `std::lower_bound/upper_bound/binary_search` 前加 `assert(is_sorted(...))`（NODEBUG 可关）；把 `remove_if` 裸调用重构为 `erase(remove_if(...), end())` 单行模式；比较器用 `std::less` 或对称 `return a<b`，严禁 `>=`/`!=` 违规。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`std::count_if` 配合 `std::execution::par` 可按策略并行统计。写一个程序：生成 1'000'000 个整数 `v[i]=i`，用并行 `std::count_if` 统计其中偶数的个数，并输出结果（应为 500000）。注意并行算法对无共享可变状态的纯谓词是安全的。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <execution>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i;
    auto n = std::count_if(std::execution::par, v.begin(), v.end(),
                           [](int x) { return x % 2 == 0; });
    std::cout << "evens = " << n << "\n";   // 500000
}
```

[标准] `std::execution::par` 允许算法将工作分派到多线程；`count_if` 的归约结果由各分块汇总，谓词无副作用故无数据竞争。GCC 在无 TBB 时自动降级为串行，仍可正确编译运行。

</details>

### 练习 2（难度 ★★★）

用自定义比较器配合 `std::sort` 实现「按绝对值降序」排序。要求比较器必须满足**严格弱序**（用 `<` 表达「前者应先于后者」，严禁用 `>=`/`<=`）。给定 `v{3,-1,-4,2,0}`，输出应为 `-4 3 -1 2 0`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
int main() {
    std::vector<int> v{3, -1, -4, 2, 0};
    // 严格弱序: a 应先于 b 当且仅当 |a| > |b|
    std::sort(v.begin(), v.end(), [](int a, int b) {
        return std::abs(a) > std::abs(b);
    });
    for (int x : v) std::cout << x << ' ';   // -4 3 -1 2 0
    std::cout << "\n";
}
```

[标准] 比较器 `comp(a,b)` 返回 true 表示 a 排在 b 前，必须满足严格弱序（非自反、非对称、可传递）。用 `>` 表达「降序先于」仍是合法严格弱序；若误用 `>=` 会破坏非自反性，导致 `std::sort` 出现未定义行为。

</details>

### 练习 3（难度 ★★★★）

`std::for_each_n` 可只处理前 N 个元素而不触碰其余，且不修改容器（无迭代器失效风险）。写出一个程序：只读遍历 `vector` 前 5 个元素并输出；随后用 **erase–remove 惯用法**删除所有偶数（注意 `remove_if` 只重排、不真正删除，必须 `erase` 收尾）。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8};
    // 只读遍历前 5 个: 不修改容器, 无迭代器失效风险
    std::for_each_n(v.begin(), 5, [](int x) { std::cout << x << ' '; });  // 1 2 3 4 5
    std::cout << "\n";
    // 删除偶数: erase-remove 惯用法
    auto it = std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    v.erase(it, v.end());
    for (int x : v) std::cout << x << ' ';   // 1 3 5 7
    std::cout << "\n";
}
```

[标准] `remove_if` 将保留元素前移、返回新的逻辑尾迭代器；真正删除需 `erase(新尾, end())`。在遍历过程中若修改同一容器导致迭代器/引用/指针失效，则属未定义行为——故「只读遍历」与「删除」须分阶段进行。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：已排序区间的查找——二分 vs 线性

**选型场景**：在 1'000'000 个已排序整数中查找某 key。错误写法直接用 `std::find`（线性扫描），在热路径上造成可感知延迟。

**常见错误（text）**：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i;
    int key = 9'999'999;
    auto it = std::find(v.begin(), v.end(), key);   // 线性 O(n): 1e7 次比较
    bool found = (it != v.end());
    std::cout << "found=" << found << "\n";
}
```

**修复（cpp）**：区间已排序，改用 `std::lower_bound` 二分（O(log n)）。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v(10'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i;
    int key = 9'999'999;
    auto it = std::lower_bound(v.begin(), v.end(), key);
    bool found = (it != v.end() && *it == key);
    std::cout << "found=" << found << " idx=" << (it - v.begin()) << "\n";
}
```

**结论**：已排序区间必须用二分系列（`lower_bound`/`binary_search`/`equal_range`）。`std::find` 仅适用于无序区间或需要「首次匹配语义」的场景，复杂度 O(n)。

### 演绎 2：并行算法中的数据竞争

**选型场景**：并行累加一个大向量的元素和。错误写法用 `std::for_each(par, ...)` + 共享非原子计数器，造成数据竞争（UB）。

**常见错误（text）**：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <execution>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i + 1;
    int sum = 0;
    std::for_each(std::execution::par, v.begin(), v.end(),
                  [&](int x) { sum += x; });   // 数据竞争(UB): 共享非原子 sum
    std::cout << "sum(maybe wrong)=" << sum << "\n";
}
```

**修复（cpp）**：用 `std::reduce` 做线程安全分区规约。

```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <execution>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i + 1;
    long long s = std::reduce(std::execution::par, v.begin(), v.end(), 0LL);
    std::cout << "sum = " << s << "\n";   // 500000500000
}
```

**结论**：并行算法要求操作无数据竞争。规约类需求用 `std::reduce`/`std::transform_reduce`（内部做线程安全分区求和），切勿用「共享变量 + `for_each`」的裸写法。
## 可视化速查图（Mermaid 补充）[标准]

> 把算法复杂度与选型浓缩为一张分层图。

### 图 1 · 标准库算法复杂度分层与代表

```mermaid
graph LR
    O1["O(1) 哈希容器"] --> Olog["O(log n) binary_search"]
    Olog --> On["O(n) find count"]
    On --> Onlog["O(n log n) sort"]
    Onlog --> On2["O(n 平方) 朴素嵌套循环"]
```
