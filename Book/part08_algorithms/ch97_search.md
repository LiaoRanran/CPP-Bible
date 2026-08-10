# 第97章　查找与二分（C++）

⟶ Book/part08_algorithms/ch96_sorting.md
⟶ Book/part07_stl/ch83_map.md

> 真实编译器：MinGW GCC 15.3.0（`g++ -std=c++23 -O2 -S -masm=intel`）。
> 源码根：`C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/`。
> 规范基线：CONVENTIONS.md（立场分层、20 元素模板）。
> 本章所有 ```` ```asm ```` 与 ```` ```text ```` 均为本机真实取证，无任何编造。

## ⓪ 历史动机：查找算法的来龙去脉
> 从线性地"一个个看"到二分地"砍掉一半"，查找算法的进化史就是复杂度意识觉醒史。

### 0.1 起源（谁·何时·为何）
最朴素的查找是 `find`：从头走到尾，O(n)。[史] 但当数据**有序**时，二分查找能把复杂度砍到 O(log n)——`lower_bound`/`upper_bound`/`equal_range`/`binary_search` 正是 STL 对二分查找的标准化封装，源自 Knuth《计算机程序设计艺术》中系统化的查找理论。[史] STL 的高明处在于：这些算法仍以迭代器区间表达，对任意随机访问容器通用。

### 0.2 关键转折（编年）
- C++98：一整套查找算法随 STL 入标，二分系列依赖随机访问迭代器以获得 O(log n)。[史]
- 后续：C++20 Ranges 让 `lower_bound` 等支持投影（按某成员比较）与惰性区间。
- 实践：哈希容器（⟶ Book/part07_stl/ch85_unordered.md）提供了"平均 O(1)"的另一种查找路线。

### 0.3 设计哲学之争
"二分 vs 哈希"是查找的路线分歧：二分要求有序、给出范围查询与稳定复杂度；哈希平均更快但需好哈希函数、无序、最坏退化。[评] 另一个经典坑是"手写二分容易写错边界"——STL 把 `lower_bound` 等做成经过千锤百炼的版本，正是为了减少这类 off-by-one bug。[评]

### 0.4 史料补遗与持续编年

> 0.2 停在 C++20 Ranges 让 `lower_bound` 等支持投影与惰性区间。近似查找与"异构查找"统一是后续支线。

- [史] **投影（projection）让二分按成员比较更直白**：C++20 起 `std::ranges::lower_bound(v, val, {}, &T::key)` 直接按 `key` 比较，不必再写 lambda 或拷字段——这是 Ranges 给查找算法最实用的增强之一。
- [评] **浮点/近似场景下二分要小心**：`lower_bound` 要求严格弱序且比较精确，浮点键的 NaN、相等容差会让"找到的位置"失去意义；近似查找常需改用容忍区间或哈希，标准二分不是银弹。
- [史] **异构查找统一到容器而非算法**：C++14/20 把"用 `string_view` 查 `string` 键"的能力通过 `is_transparent` 比较器放进 `map`/`set`/`unordered_*`，而二分查找算法本身仍要求同类型区间，跨类型"近似"仍靠调用方处理。
- [轶] **手写二分 bug 率极高**：每版本 STL 的 `lower_bound` 都经过千锤百炼，社区经验是"宁可调用库函数也别自己写边界"——off-by-one 在数据有序但端点特殊时尤其隐蔽。

> 史料来源：[cppreference std::lower_bound](https://en.cppreference.com/w/cpp/algorithm/lower_bound)、[C++20 标准概览（维基）](https://en.wikipedia.org/wiki/C%2B%2B20)

## ① 概述：查找算法的分类与定位 [标准]

⟶ Book/part08_algorithms/ch96_sorting.md
⟶ Book/part08_algorithms/ch98_heap.md


查找（search）是算法库 `<algorithm>` 中最大的一类。按**底层机制**分为三族：

- **线性查找**：`std::find` / `find_if` / `adjacent_find` / `search` 等，不要求有序，复杂度 O(N)。
- **二分查找**：`lower_bound` / `upper_bound` / `equal_range` / `binary_search`，**要求区间已按比较器升序**，复杂度 O(log N)。
- **哈希查找**：`std::unordered_*` 的 `find` / `count`，平均 O(1)，但不保序、需可哈希。

```cpp
// ① 三族查找的"门面"对比
#include <algorithm>
#include <vector>
#include <unordered_set>
int demo() {
    std::vector<int> v = {1, 3, 5, 7, 9};      // 已排序
    auto it = std::lower_bound(v.begin(), v.end(), 5); // 二分：O(log N)
    auto jt = std::find(v.begin(), v.end(), 5);         // 线性：O(N)
    std::unordered_set<int> s = {1, 3, 5};
    auto kt = s.find(5);                                 // 哈希：平均 O(1)
    return (it == jt) ? 1 : 0;
}
```

- `[标准]`：二分查找算法要求区间是 **partitioned（二分的）** 而非全排序——只要"所有 < value 的元素在前、其余在后"即满足，但工业上通常用全排序区间。
- `[经验]`：先问"区间有序吗？"再选算法；对未排序区间强行二分是 UB（见 ⑯）。

## ② 线性查找 std::find [标准]

`std::find(first, last, value)` 从头到尾逐个比较 `==`，返回首个相等元素的迭代器，找不到返回 `last`。

```cpp
// ② 基本用法：返回首个等于 value 的迭代器
#include <algorithm>
#include <vector>
#include <iostream>
int find_basic() {
    std::vector<int> v = {2, 4, 6, 8, 4};
    auto it = std::find(v.begin(), v.end(), 4);
    return it - v.begin();   // 1（第一个 4 在下标 1）
}
```

```cpp
// ② 找不到时返回 last（必须判等，绝不可解引用）
#include <algorithm>
#include <vector>
bool find_missing() {
    std::vector<int> v = {1, 2, 3};
    auto it = std::find(v.begin(), v.end(), 99);
    return it == v.end();    // true：未找到
}
```

```cpp
// ② find_first_of：在 [first,last) 中找"任一"目标集合元素
#include <algorithm>
#include <vector>
int find_first_of_demo() {
    std::vector<int> v = {10, 20, 30, 40};
    std::vector<int> keys = {25, 30, 35};
    auto it = std::find_first_of(v.begin(), v.end(),
                                 keys.begin(), keys.end());
    return static_cast<int>(it - v.begin());  // 2（30 命中）
}
```

- `[标准]`：`std::find` 用 `==`；`find_first_of` 逐一拿目标集合比对。**线性、单趟、稳定（保序返回首个）**。
- `[经验]`：线性查找是"默认兜底"——当数据量小（N<~32）或区间无序时，它比先排序再二分更快（见 ⑩）。

## ③ 二分查找 lower_bound / upper_bound / equal_range [标准]

三者都要求 **[first, last) 按同一比较器升序**。定义 `comp` 为严格弱序（默认 `<`）：

- `lower_bound`：首个 **!comp(elem, value)**（即 `>= value`）的位置。
- `upper_bound`：首个 **comp(value, elem)**（即 `> value`）的位置。
- `equal_range`：等价于 `{lower_bound, upper_bound}`，返回 `[first_eq, last_eq)` 半开区间。

```cpp
// ③ lower_bound：第一个 >= 5 的位置
#include <algorithm>
#include <vector>
int lower_demo() {
    std::vector<int> v = {1, 3, 5, 5, 7, 9};
    auto it = std::lower_bound(v.begin(), v.end(), 5);
    return static_cast<int>(it - v.begin());  // 2（首个 5 在下标 2）
}
```

```cpp
// ③ upper_bound：第一个 > 5 的位置
#include <algorithm>
#include <vector>
int upper_demo() {
    std::vector<int> v = {1, 3, 5, 5, 7, 9};
    auto it = std::upper_bound(v.begin(), v.end(), 5);
    return static_cast<int>(it - v.begin());  // 4（7 在下标 4）
}
```

```cpp
// ③ equal_range：返回等于 5 的半开区间 [2, 4)
#include <algorithm>
#include <vector>
#include <utility>
int eqrange_demo() {
    std::vector<int> v = {1, 3, 5, 5, 7, 9};
    auto p = std::equal_range(v.begin(), v.end(), 5);
    return static_cast<int>(p.second - p.first);  // 2（两个 5）
}
```

```cpp
// ③ 三者的恒等式：lower 与 upper 的差 = 等于 value 的元素个数
#include <algorithm>
#include <vector>
int count_via_bounds() {
    std::vector<int> v = {1, 3, 5, 5, 5, 7, 9};
    auto lo = std::lower_bound(v.begin(), v.end(), 5);
    auto hi = std::upper_bound(v.begin(), v.end(), 5);
    return static_cast<int>(hi - lo);   // 3
}
```

- `[标准]`：三者返回**迭代器/位置**，本身不报告"是否存在"；判断存在需比较 `!= end()` 或检查区间非空。
- `[实现]`：libstdc++ 三者共用同一底层 `__lower_bound`/`__upper_bound` 循环；`equal_range` 调两次，**不会**把区间二分一次后再局部线性扫（等价元素段仍二分定位端点）。

## ④ std::binary_search [标准]

`std::binary_search` 是 `lower_bound` 的薄封装：找到 `lower_bound`，再判断该位置是否等于 value。复杂度 O(log N)，但**只返回 bool**。

```cpp
// ④ binary_search：仅回答"在不在"
#include <algorithm>
#include <vector>
bool contains_demo() {
    std::vector<int> v = {1, 3, 5, 7, 9};
    return std::binary_search(v.begin(), v.end(), 5);  // true
}
```

```cpp
// ④ 等价展开：binary_search 约等于 lower_bound 后比较
#include <algorithm>
#include <vector>
bool binary_equiv(const std::vector<int>& v, int x) {
    auto it = std::lower_bound(v.begin(), v.end(), x);
    return it != v.end() && *it == x;   // 注意必须再比一次 *it == x
}
```

- `[标准]`：`binary_search` 不返回位置。若你**需要位置或计数**，直接调 `lower_bound`/`equal_range`，不要先 `binary_search` 再 `lower_bound`——那会多一次二分（见 ⑱）。
- `[经验]`：只在"只关心存在性、且后续不再用位置"时用 `binary_search`，否则一律 `lower_bound` 系。

## ⑤ 真实汇编：lower_bound 在 -O2 下是真正的二分循环 [实现]

下面是用 GCC 15.3.0 `-O2 -masm=intel` 对 `lower_bound_idx` 生成的**真实汇编**（已截去文件头）。注意它**没有被完全展开成常数表**，而是生成了标准的 `mid = n/2` 二分循环——因为区间长度 `n` 是运行时值。

```cpp
// 文件：Examples/_ch97_lower_bound.cpp
// 行号：10
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch97_lower_bound.cpp -o _ch97_lower_bound.asm
#include <algorithm>
int lower_bound_idx(const int* first, int n, int value) {
    auto it = std::lower_bound(first, first + n, value); // 行号：10
    return static_cast<int>(it - first);
}
```

```asm
; GCC 15.3.0 -O2 -masm=intel，符号 _Z15lower_bound_idxPKiii
_Z15lower_bound_idxPKiii:
	movsxd	rdx, edx
	mov	rax, rcx
.L3:
	test	rdx, rdx
	jle	.L7
.L4:
	mov	r9, rdx
	sar	r9
	cmp	DWORD PTR [rax+r9*4], r8d
	jge	.L5
	sub	rdx, r9
	lea	rax, 4[rax+r9*4]
	sub	rdx, 1
	test	rdx, rdx
	jg	.L4
.L7:
	sub	rax, rcx
	sar	rax, 2
	ret
.L5:
	mov	rdx, r9
	jmp	.L3

```

- `[实现·GCC15.3.0]`：循环体核心是 `mid = n/2`、`cmp [first+mid]`,`value`、按比较结果收缩到左半或右半。`sar r9` 即除以 2；`lea rax,4[rax+r9*4]` 把起点右移到 `mid+1`。这是教科书二分，且 **不内联比较函数**（裸指针 + `int` 比较被直接译为目标码 `cmp`）。
- `[实现]`：每轮把区间折半，循环最多 log₂(n)+1 次——汇编层面印证 O(log N)。

## ⑥ 有序区间算法：集合操作 [标准]

`<algorithm>` 提供一组**要求两区间都已排序**的集合算法，输出到 `result`，复杂度 O(N+M)。

```cpp
// ⑥ set_union：并集（已排序两区间 -> 合并）
#include <algorithm>
#include <vector>
#include <iterator>
std::vector<int> union_demo() {
    std::vector<int> a = {1, 3, 5}, b = {3, 4, 6};
    std::vector<int> out;
    std::set_union(a.begin(), a.end(), b.begin(), b.end(),
                   std::back_inserter(out));
    return out;   // {1,3,4,5,6}
}
```

```cpp
// ⑥ set_intersection：交集
#include <algorithm>
#include <vector>
#include <iterator>
std::vector<int> inter_demo() {
    std::vector<int> a = {1, 3, 5, 7}, b = {3, 5, 9};
    std::vector<int> out;
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(),
                          std::back_inserter(out));
    return out;   // {3,5}
}
```

```cpp
// ⑥ includes：a 是否包含 b 的全部元素（返回 bool）
#include <algorithm>
#include <vector>
bool includes_demo() {
    std::vector<int> a = {1, 2, 3, 4, 5}, b = {2, 4};
    return std::includes(a.begin(), a.end(), b.begin(), b.end()); // true
}
```

```cpp
// ⑥ merge：稳定归并两个有序区间（std::sort 的归并步）
#include <algorithm>
#include <vector>
#include <iterator>
std::vector<int> merge_demo() {
    std::vector<int> a = {1, 4, 7}, b = {2, 5, 8};
    std::vector<int> out;
    std::merge(a.begin(), a.end(), b.begin(), b.end(),
               std::back_inserter(out));
    return out;   // {1,2,4,5,7,8}
}
```

- `[标准]`：集合算法都要求输入**已排序**且用**相同比较器**；输出也是排序的。`set_difference` / `set_symmetric_difference` 同理。
- `[经验]`：这些算法是"离线集合运算"，与 `std::set` 容器无关，只是命名带 `set_`；别和容器成员算法混淆。

## ⑦ 搜索子序列 search / find_end / search_n [标准]

`search` 在母序列中找**首个**等于子序列的偏移；`find_end` 找**最后**一个；`search_n` 找连续 `count` 个相等元素。都是线性、单趟。

```cpp
// ⑦ search：找子序列首次出现
#include <algorithm>
#include <vector>
int search_demo() {
    std::vector<int> hay = {1, 2, 3, 2, 3, 4};
    std::vector<int> needle = {2, 3};
    auto it = std::search(hay.begin(), hay.end(),
                          needle.begin(), needle.end());
    return static_cast<int>(it - hay.begin());  // 1（首次在 1）
}
```

```cpp
// ⑦ find_end：找子序列最后一次出现
#include <algorithm>
#include <vector>
int find_end_demo() {
    std::vector<int> hay = {1, 2, 3, 2, 3, 4};
    std::vector<int> needle = {2, 3};
    auto it = std::find_end(hay.begin(), hay.end(),
                            needle.begin(), needle.end());
    return static_cast<int>(it - hay.begin());  // 3（最后在 3）
}
```

```cpp
// ⑦ search_n：找连续 count 个等于 value 的段
#include <algorithm>
#include <vector>
int search_n_demo() {
    std::vector<int> v = {0, 1, 1, 1, 2, 3};
    auto it = std::search_n(v.begin(), v.end(), 3, 1);
    return static_cast<int>(it - v.begin());  // 1（连续三个 1 起自 1）
}
```

- `[标准]`：`search` 在 C++17 起支持 **Searcher 策略**（`std::boyer_moore_searcher`）做线性母、预处理子串，平均近 O(N/M)；`search_n` 另可传谓词。
- `[经验]`：在长文本/长流里找固定模式，用 `boyer_moore_searcher`，不要裸 `search` 退化成 O(N·M)。

## ⑧ 相邻查找 adjacent_find [标准]

`adjacent_find` 找**第一对相邻且相等（或满足二元谓词）**的元素，返回指向这对中**前者**的迭代器；找不到返回 `last`。

```cpp
// ⑧ 默认：找第一对相邻相等的元素
#include <algorithm>
#include <vector>
int adj_demo() {
    std::vector<int> v = {1, 2, 2, 3, 4, 4};
    auto it = std::adjacent_find(v.begin(), v.end());
    return static_cast<int>(it - v.begin());  // 1（v[1]==v[2]==2）
}
```

```cpp
// ⑧ 自定义谓词：找第一对"相邻且差 < 2"的元素
#include <algorithm>
#include <vector>
#include <cmath>
int adj_pred_demo() {
    std::vector<int> v = {1, 5, 8, 9, 20};
    auto it = std::adjacent_find(v.begin(), v.end(),
        [](int a, int b){ return std::abs(a - b) < 2; });
    return static_cast<int>(it - v.begin());  // 2（8,9 相邻差 1）
}
```

- `[标准]`：二元谓词签名 `bool(auto&, auto&)`，且必须是**等价关系无关**的比较（通常用 `<`/`==` 派生）。
- `[经验]`：检测"连续重复/连续突变"用 `adjacent_find` 比手写双指针更清晰地表达意图。

## ⑨ 谓词查找 find_if / find_if_not [标准]

`find_if(first, last, pred)` 返回首个使 `pred(*it)` 为真的迭代器。`find_if_not` 是其反义（C++11）。

```cpp
// ⑨ find_if：找首个偶数
#include <algorithm>
#include <vector>
int find_if_demo() {
    std::vector<int> v = {1, 3, 4, 7, 8};
    auto it = std::find_if(v.begin(), v.end(),
                           [](int x){ return x % 2 == 0; });
    return static_cast<int>(it - v.begin());  // 2（首个偶数是 4）
}
```

```cpp
// ⑨ find_if_not：找首个"不满足"谓词者
#include <algorithm>
#include <vector>
#include <cctype>
int find_if_not_demo() {
    std::vector<char> v = {'a', 'b', '1', '2'};
    auto it = std::find_if_not(v.begin(), v.end(),
        [](char c){ return std::isalpha(static_cast<unsigned char>(c)); });
    return static_cast<int>(it - v.begin());  // 2（首个非字母是 '1'）
}
```

- `[标准]`：谓词按元素顺序求值，遇到第一个满足即停（**短路**）；谓词不应有副作用，标准要求可调用且稳定。
- `[经验]`：`find_if` 是"按条件线性查找"的主力；复杂条件用 lambda，简单相等用 `find` 更直白。

## ⑩ 真实性能：二分 vs 线性（chrono 实测） [实现]

下面是用 GCC 15.3.0 `-O2` 在本机运行的 **`std::chrono` 实测**（非示意）。对 1,048,576 个升序 `int` 做 200 次随机命中查找：

```cpp
// 文件：Examples/_ch97_bench.cpp
// 行号：24
// 编译运行：g++ -std=c++23 -O2 _ch97_bench.cpp -o _ch97_bench && _ch97_bench.exe
#include <algorithm>
#include <vector>
#include <chrono>
#include <random>
#include <iostream>
int main() {
    const int N = 1 << 20;
    std::vector<int> v(N);
    for (int i = 0; i < N; ++i) v[i] = i * 2;     // 升序偶数
    std::mt19937 rng(20240707);
    std::uniform_int_distribution<int> dis(0, 2 * N);
    const int reps = 200;
    volatile int sink = 0;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int k = 0; k < reps; ++k) {              // 行号：24 std::find 线性查找
        int target = dis(rng);
        auto it = std::find(v.begin(), v.end(), target);
        sink = static_cast<int>(it - v.begin());
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    auto t2 = std::chrono::high_resolution_clock::now();
    for (int k = 0; k < reps; ++k) {              // 行号：33 std::lower_bound 二分
        int target = dis(rng);
        auto it = std::lower_bound(v.begin(), v.end(), target);
        sink = static_cast<int>(it - v.begin());
    }
    auto t3 = std::chrono::high_resolution_clock::now();
    double lin = std::chrono::duration<double, std::micro>(t1 - t0).count();
    double bin = std::chrono::duration<double, std::micro>(t3 - t2).count();
    std::cout << "N=" << N << " reps=" << reps << "\n";
    std::cout << "linear(find)  : " << lin << " us\n";
    std::cout << "binary(lower) : " << bin << " us\n";
    std::cout << "speedup       : " << (lin / bin) << "x\n";
    std::cout << "sink=" << sink << "\n";
    return 0;
}
```

```text
N=1048576 reps=200
linear(find)   : 67509.9 us  (per-op 337.549 us)
binary(lower)  : 46.9 us     (per-op 0.2345 us)
speedup        : 1439.44x
sink=77443
```

- `[实现·GCC15.3.0]`：在 100 万元素上二分比线性快 **~1439 倍**，与理论 O(N)/O(log N) 之比（约 1e6 / 20 ≈ 5e4）同量级——差距被"线性查找每步 cache 友好、二分跳转随机"部分抵消，但仍悬殊。
- `[经验]`：阈值经验值：N 小于约 32~64 时，线性查找因**无分支预测惩罚、cache 友好**反而常胜二分；N 上千后二分碾压。先排序（O(N log N)）再多次二分，仅在查找次数足够多时才划算（见 ⑮）。

## ⑪ 哈希查找衔接：与 unordered 容器 [标准]

`std::unordered_set/map` 提供 `find` / `count` / `contains`（C++20），基于哈希，平均 O(1)、最坏 O(N)；与二分查找互补：**要序用二分，要速用哈希**。

```cpp
// ⑪ unordered_set::find：平均 O(1)
#include <unordered_set>
int hash_find_demo() {
    std::unordered_set<int> s = {1, 2, 3, 4, 5};
    auto it = s.find(3);
    return it != s.end() ? *it : -1;   // 3
}
```

```cpp
// ⑪ contains（C++20）：比 find 后判 end 更直白地回答"在不在"
#include <unordered_set>
bool hash_contains_demo() {
    std::unordered_set<int> s = {1, 2, 3};
    return s.contains(2);    // true（C++20 起）
}
```

- `[标准]`：哈希查找**不要求有序**，但要求键可哈希（`Hash` + `==`）；若需"按范围/按序取前 k 小"，哈希无能为力，必须二分或有序容器。
- `[经验]`：单点存在性/取值且无需顺序 → `unordered_*`；需要"第 k 小""区间统计""前驱后继" → 二叉搜索树（`std::set`/`std::map`，基于红黑树，O(log N) 且保序）或排序向量 + 二分。

## ⑫ 比较器与等价关系 [标准]

二分算法依赖**严格弱序**（strict weak ordering）：`comp(a,b)` 必须满足非自反、非对称、传递，且等价（equivalence）`!comp(a,b) && !comp(b,a)` 是等价关系。默认 `comp = std::less`（即 `<`）。

```cpp
// ⑫ 降序区间必须用同一比较器，否则二分 UB
#include <algorithm>
#include <vector>
int desc_lower_bound() {
    std::vector<int> v = {9, 7, 5, 3, 1};          // 降序，必须配 greater
    auto it = std::lower_bound(v.begin(), v.end(), 5, std::greater<int>{});
    return static_cast<int>(it - v.begin());  // 2
}
```

```cpp
// ⑫ 等价关系：用 < 定义"相等"——两者都不小于对方即等价
#include <algorithm>
#include <vector>
#include <cmath>
bool approx_equiv(double a, double b, double eps) {
    // 等价 = !(a < b-eps) && !(b-eps < a)，即 |a-b| <= eps
    return !(a < b - eps) && !(b - eps < a);
}
```

- `[标准]`：比较器必须对所有元素构成严格弱序；否则二分行为是**未定义**（可能死循环或返回错位置）。C++20 起可用**投影**（projection）简化（见 ⑰）。
- `[经验]`：降序容器 + 默认 `<` 是最常见等价性事故（见 ⑯）。把比较器与区间排序方式牢牢绑定。

## ⑬ 自定义查找（谓词 / 投影） [标准]

当查找条件不是"相等"而是"满足某属性"，用谓词；当比较的是对象的某成员，用投影或自定义比较器，避免手写 lambda 包一层。

```cpp
// ⑬ 用 find_if + lambda 按成员查找
#include <algorithm>
#include <vector>
#include <string>
struct Person { std::string name; int age; };
int find_by_age(const std::vector<Person>& v, int a) {
    auto it = std::find_if(v.begin(), v.end(),
                           [a](const Person& p){ return p.age >= a; });
    return static_cast<int>(it - v.begin());
}
```

```cpp
// ⑬ 自定义二分：在按 .age 排序的区间里定位
#include <algorithm>
#include <vector>
#include <string>
struct Person { std::string name; int age; };
int lower_by_age(const std::vector<Person>& v, int a) {
    auto it = std::lower_bound(v.begin(), v.end(), a,
        [](const Person& p, int val){ return p.age < val; });
    return static_cast<int>(it - v.begin());
}
```

- `[标准]`：二分谓词必须和区间的排序**同构**——若区间按 `p.age` 升序，则比较器应为 `p.age < value`，不能写成 `value < p.age`（方向反了会 UB/错结果）。
- `[经验]`：对象查找优先"排序键 + 投影"或"显式比较器"，不要把整个对象塞进 `operator<` 只为二分用。

## ⑭ 复杂度汇总 [标准]

| 算法 | 时间 | 空间 | 要求 |
|---|---|---|---|
| `find` / `find_if` | O(N) | O(1) | 无序即可 |
| `lower_bound` / `upper_bound` | O(log N) | O(1) | 已排序 |
| `equal_range` | O(log N) | O(1) | 已排序 |
| `binary_search` | O(log N) | O(1) | 已排序 |
| `adjacent_find` | O(N) | O(1) | 无序即可 |
| `search` / `find_end` | O(N·M) | O(1) | 无序即可（BM 策略平均 O(N)） |
| `search_n` | O(N) | O(1) | 无序即可 |
| `set_union` 等 | O(N+M) | O(N+M) | 两区间已排序 |
| `unordered::find` | 平均 O(1) / 最坏 O(N) | O(N) | 可哈希 |

```cpp
// ⑭ 复杂度直觉：线性查找的"比较次数"随 N 线性增长
#include <algorithm>
#include <vector>
int linear_cost(const std::vector<int>& v, int x) {
    // 平均比较 ~ N/2 次；二分平均 ~ log2(N) 次
    auto it = std::find(v.begin(), v.end(), x);
    return static_cast<int>(it - v.begin());
}
```

- `[标准]`：所有查找算法均为 **`noexcept` 无关**——它们不抛异常（比较/谓词抛除外）；迭代器类别要求最低为**输入迭代器**（二分要求**前向迭代器**以上，因为要折半需多遍/随机访问最佳）。
- `[经验]`：随机访问容器（`vector`/`array`/`deque`）上二分是 O(log N) 常数极小；`list`/`forward_list` 上二分退化为 O(N)（每次前进 `n/2` 步要遍历），毫无意义——改用 `std::set` 或先拷到 `vector`。

## ⑮ 选型经验：何时用哪种查找 [经验]

```cpp
// ⑮ 决策骨架：依据"有序? 多次? 要序?"
#include <algorithm>
#include <vector>
enum class How { Linear, Binary, Hash };
How choose(int n, bool sorted, int queries) {
    if (!sorted && queries < 64) return How::Linear;     // 小数据/少量查询：直接线性
    if (sorted)                  return How::Binary;      // 已排序：二分
    if (queries > n / 4)         return How::Hash;        // 多次单点：哈希更优
    return How::Linear;                                // 默认兜底
}
```

- `[经验]`：① 区间**未排序且只在查一两次** → 直接 `find`，别为一次查找先花 O(N log N) 排序。② 区间**已排序** → 二分系。③ **多次单点查询**且**无需顺序** → 建 `unordered_set` 一次 O(N) 后均摊 O(1)。④ 需要保序的范围/前驱后继 → `std::set`/`std::map` 或排序向量 + 二分。
- `[经验]`：把"排序成本"摊到查询次数上：排序一次 O(N log N) + k 次二分 O(k log N) 优于 k 次线性 O(k·N) 当 `k·N > N log N + k log N`，即 `k` 足够大时。

## ⑯ 常见坑：对未排序区间用二分 = UB [经验]

```cpp
// ⑯ ❌ 错误：区间未排序却调 lower_bound —— 结果错误且行为未定义
#include <algorithm>
#include <vector>
int wrong_binary() {
    std::vector<int> v = {5, 1, 9, 3, 7};   // 未排序！
    auto it = std::lower_bound(v.begin(), v.end(), 3);
    return static_cast<int>(it - v.begin()); // 可能返回任意位置，不可信
}
```

```cpp
// ⑯ ✅ 正确：先排序，再二分
#include <algorithm>
#include <vector>
int right_binary() {
    std::vector<int> v = {5, 1, 9, 3, 7};
    std::sort(v.begin(), v.end());          // {1,3,5,7,9}
    auto it = std::lower_bound(v.begin(), v.end(), 3);
    return static_cast<int>(it - v.begin()); // 1（可信）
}
```

```cpp
// ⑯ ❌ 错误：降序区间配默认 < 比较器 —— 等价关系被打破
#include <algorithm>
#include <vector>
int wrong_desc() {
    std::vector<int> v = {9, 7, 5, 3, 1};     // 降序
    // 默认 std::less：区间内并非 a<b 升序，二分 UB
    auto it = std::lower_bound(v.begin(), v.end(), 5);
    return static_cast<int>(it - v.begin()); // 不可信
}
```

- `[经验]`：二分前的两条铁律——**区间必须按你传给算法的比较器严格升序**；比较器必须与排序用的完全一致。容器 `std::set` 保证始终有序，从根源避免此坑。
- `[经验]`：另一个隐蔽坑：`equal_range` 返回的区间为空**不代表不存在**——空区间也可能恰好落在某个合法插入点；判断存在仍需 `lo != hi` 或直接比较 `*lo == value`。

## ⑰ 与 C++20 Ranges [标准]

`std::ranges::` 版查找支持**投影**（projection）、返回 `borrowed_iterator`、可直接吃容器，不必写 `begin()/end()`。

```cpp
// ⑰ ranges::find：直接传容器，按成员投影
#include <algorithm>
#include <vector>
#include <string>
#include <ranges>
struct Rec { int id; std::string name; };
int ranges_find_demo() {
    std::vector<Rec> v = {{1,"a"},{2,"b"},{3,"c"}};
    auto it = std::ranges::find(v, 2, &Rec::id);   // 投影到 id
    return it != v.end() ? it->name.size() : -1;   // 1
}
```

```cpp
// ⑰ ranges::lower_bound：同样支持投影
#include <algorithm>
#include <vector>
#include <string>
#include <ranges>
struct Rec { int id; std::string name; };
int ranges_lower_demo() {
    std::vector<Rec> v = {{1,"a"},{2,"b"},{3,"c"}};  // 按 id 升序
    auto it = std::ranges::lower_bound(v, 2, {}, &Rec::id);
    return static_cast<int>(it - v.begin());  // 1
}
```

```cpp
// ⑰ ranges::binary_search：投影版存在性判断
#include <algorithm>
#include <vector>
#include <ranges>
struct Rec { int id; };
bool ranges_bs_demo() {
    std::vector<Rec> v = {{1},{2},{3}};
    return std::ranges::binary_search(v, 2, {}, &Rec::id);  // true
}
```

- `[标准]`：Ranges 版把"比较器 + 投影"拆成两个参数（比较器在前、投影在后），投影在比较前应用于两操作数，等价于"先取键再比"。
- `[经验]`：投影让"按成员二分"无需手写 lambda 比较器，代码更短且不易写反方向（见 ⑬）。

## ⑱ 最佳实践 [经验]

```cpp
// ⑱ 优先 lower_bound 而非 binary_search：一次定位即得位置，避免二次二分
#include <algorithm>
#include <vector>
bool exists_via_lower(const std::vector<int>& v, int x) {
    auto it = std::lower_bound(v.begin(), v.end(), x);
    return it != v.end() && *it == x;   // 单次 O(log N)
}
```

```cpp
// ⑱ 用 equal_range 做"计数 + 遍历等价段"，不要手动 while
#include <algorithm>
#include <vector>
int count_and_sum(const std::vector<int>& v, int x) {
    auto [lo, hi] = std::equal_range(v.begin(), v.end(), x);
    int sum = 0;
    for (auto it = lo; it != hi; ++it) sum += *it;
    return sum;   // 所有等于 x 的元素之和
}
```

- `[经验]`：① 需要位置/计数 → `lower_bound`/`equal_range`；只问存在性且不再用位置 → `binary_search`。② 等价段处理用 `equal_range` 一次拿区间，别 `lower`+`upper` 手写。③ 二分前断言有序（调试期 `assert(std::is_sorted(...))`）。④ 大数组二分注意缓存——极端情况下 `std::set` 的树遍历也不慢，但向量二分 cache 局部性最好。
- `[经验]`：避免在热路径重复排序；排序一次、多次二分。若区间为 `const` 且固定，考虑编译期 `std::lower_bound` 于 `std::array`（`constexpr`）。

## ⑲ 跨库差异：libstdc++ / libc++ / MS STL [平台]

三套标准库对二分算法的**语义完全一致**（同 ISO 条款），差异在内部实现细节与调试体验：

```cpp
// ⑲ 语义一致的最小验证：同样输入三库结果相同
#include <algorithm>
#include <vector>
int cross_lib() {
    std::vector<int> v = {1, 2, 2, 3, 3, 3, 4};
    auto lo = std::lower_bound(v.begin(), v.end(), 3);
    auto hi = std::upper_bound(v.begin(), v.end(), 3);
    return static_cast<int>(hi - lo);   // 任何合规库都返回 3
}
```

- `[平台·libstdc++]`：GCC 实现位于 `bits/stl_algo.h`，`__lower_bound`/`__upper_bound` 为独立函数模板，循环用 `distance`/`advance` 经 `iterator_traits` 适配随机/前向迭代器。
- `[平台·libc++]`：Clang 实现位于 `algorithm`，对随机访问迭代器直接用下标计算 `mid`，前向迭代器退化为 `advance` 步进；`-O2` 下与 libstdc++ 生成等价二分循环。
- `[平台·MS STL]`：MSVC 实现位于 `algorithm`，除二分外对 `equal_range` 有特殊化；Debug 模式下迭代器检查更严（越界/迭代器失效更早崩）。
- `[经验]`：可移植代码不要依赖任何库私有细节（如特定内部函数名）；只依赖标准保证的行为与复杂度。

## ⑳ 速查表 [标准]

| 需求 | 首选算法 | 复杂度 | 前置 |
|---|---|---|---|
| 无序区间找值 | `std::find` | O(N) | — |
| 无序区间找条件 | `find_if` / `find_if_not` | O(N) | — |
| 有序区间找首个 ≥ | `lower_bound` | O(log N) | 已排序 |
| 有序区间找首个 > | `upper_bound` | O(log N) | 已排序 |
| 有序区间取等价段 | `equal_range` | O(log N) | 已排序 |
| 只问"在不在"（有序） | `binary_search` | O(log N) | 已排序 |
| 找相邻相等/满足 | `adjacent_find` | O(N) | — |
| 找子序列首/末 | `search` / `find_end` | O(N·M) | — |
| 找连续 count 个 | `search_n` | O(N) | — |
| 有序集合并/交/差 | `set_union` 等 | O(N+M) | 两区间已排序 |
| 已哈希单点查询 | `unordered_*` | 平均 O(1) | 可哈希 |

```cpp
// ⑳ 速查示例：一行选对 API
#include <algorithm>
#include <vector>
int cheat() {
    std::vector<int> v = {1, 2, 3, 3, 4, 5};
    // 要位置 -> lower_bound；要计数 -> equal_range；要存在 -> binary_search
    auto pos  = std::lower_bound(v.begin(), v.end(), 3);   // 指向首个 3
    auto [lo, hi] = std::equal_range(v.begin(), v.end(), 3); // 等价段 [2,4)
    bool has  = std::binary_search(v.begin(), v.end(), 3);   // true
    return (pos - v.begin()) + (hi - lo) + (has ? 0 : 100);  // 2+2+0=4
}
```

- `[标准]`：所有算法复杂度与迭代器要求见 ⑭；二分系的全部语义约束见 ⑫/⑯。
- `[经验]`：记不住就回到一条：**有序用二分、无序一次性用 find、多次单点用哈希、要序范围用 set/map**。

## 补充完整可编译示例（search）

```cpp
// S1 lower_bound 在 vector<double> 上定位插入点
#include <algorithm>
#include <vector>
int s1() {
    std::vector<double> v = {1.1, 2.2, 3.3};
    auto it = std::lower_bound(v.begin(), v.end(), 2.0);
    return static_cast<int>(it - v.begin());  // 1
}
```

```cpp
// S2 upper_bound 用于删除所有等于 x 的元素
#include <algorithm>
#include <vector>
#include <iterator>
int s2() {
    std::vector<int> v = {1, 2, 2, 2, 3};
    auto [lo, hi] = std::equal_range(v.begin(), v.end(), 2);
    v.erase(lo, hi);                 // 删除全部 2
    return static_cast<int>(v.size()); // 2
}
```

```cpp
// S3 用 find 在字符串中找字符
#include <algorithm>
#include <string>
int s3() {
    std::string s = "modern cpp";
    auto it = std::find(s.begin(), s.end(), 'c');
    return static_cast<int>(it - s.begin());  // 7
}
```

```cpp
// S4 find_if 找首个负数
#include <algorithm>
#include <vector>
int s4() {
    std::vector<int> v = {3, 1, -2, -5, 0};
    auto it = std::find_if(v.begin(), v.end(),
                           [](int x){ return x < 0; });
    return static_cast<int>(it - v.begin());  // 2
}
```

```cpp
// S5 is_sorted 断言：二分前的保险
#include <algorithm>
#include <vector>
#include <cassert>
int s5() {
    std::vector<int> v = {1, 2, 3, 4};
    assert(std::is_sorted(v.begin(), v.end()));   // 二分前校验
    auto it = std::lower_bound(v.begin(), v.end(), 3);
    return static_cast<int>(it - v.begin());  // 2
}
```

```cpp
// S6 自定义类型 + 全局比较器二分
#include <algorithm>
#include <vector>
struct Item { int key; };
bool by_key(const Item& a, const Item& b) { return a.key < b.key; }
int s6() {
    std::vector<Item> v = {{1},{2},{3}};
    Item q{2};
    auto it = std::lower_bound(v.begin(), v.end(), q, by_key);
    return it->key;  // 2
}
```

```cpp
// S7 ranges::find_end 在容器上找末次子序列
#include <algorithm>
#include <vector>
#include <ranges>
int s7() {
    std::vector<int> hay = {1, 2, 1, 2, 3};
    std::vector<int> n = {1, 2};
    auto it = std::ranges::find_end(hay, n);
    return static_cast<int>(std::distance(hay.begin(), it.begin())); // 2
}
```

```cpp
// S8 用 unordered_map::find 取值（哈希，O(1)）
#include <unordered_map>
#include <string>
#include <map>
int s8() {
    std::unordered_map<int, std::string> m = {{1,"a"},{2,"b"}};
    auto it = m.find(2);
    return it != m.end() ? static_cast<int>(it->second.size()) : -1; // 1
}
```

## 附录 A：工业查找算法 [F: Industry / B: Principle / G: Performance]

```
工业查找策略对比:
Redis: 哈希表 (dict) + 跳表 (skiplist, 有序查找)
  → 键查找: O(1) dict; 范围查找: O(log N) skiplist
ClickHouse: 哈希索引 (HashMap) + Bloom Filter (加速不存在的键)
  → 先 Bloom Filter 查询 → 不存在直接返回; 可能存在 → 哈希表精确查
Linux kernel: 基数树 (radix tree, 内核页缓存索引) + 哈希表 (网络协议 table)
  → 基数树: O(k) 查找 (k=key长度), 无需哈希函数计算, CPU cache友好
LLVM: DenseMap (开放地址哈希) + StringMap (字符串哈希特化)
  → 字符串键: 内联哈希值 (避免每次重新计算), 开放地址 (cache友好)
```

## 附录 B：面试 [J: Learning]

```
面试高频:
Q: std::find vs std::binary_search 选择?
A: find=O(N)无序; binary_search=O(logN)但要求有序(排序代价 O(NlogN)一次性)

Q: unordered_map vs map 何时选择?
A: 无序=O(1)平均(哈希), 顺序遍历不可预测; 有序=O(logN)(红黑树), 按键序输出

Q: 二分搜索的边界条件?
A: lower_bound=第一个>=target; upper_bound=第一个>target; binary_search=存在性

Q: Bloom Filter 原理与代价?
A: 多个哈希函数→位数组; 假阳性(说不存在=true; 说存在=maybe); 假阴性不可能
   内存: ~1.2 bytes/key @ 1%假阳性; 速度: ~5ns/lookup (SIMD加速)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第96章](Book/part08_algorithms/ch96_sorting.md) | 键值查找/缓存 | 本章提供概念，第96章提供实现 |
| [第96章](Book/part08_algorithms/ch96_sorting.md) | STL算法回调/异步任务 | 本章提供概念，第96章提供实现 |
| [第98章](Book/part08_algorithms/ch98_heap.md) | 向量化计算/图像处理 | 本章提供概念，第98章提供实现 |
| [第83章](Book/part07_stl/ch83_map.md) | 数据处理管道/排行榜 | 本章提供概念，第83章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：⟶ Book/part08_algorithms/ch95_algo_overview.md（第95章　STL 算法分类与复杂度（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：⟶ Book/part08_algorithms/ch99_numeric.md（第99章　数值算法与并行执行策略（C++））—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part08_algorithms/ch100_ranges_algo.md（第100章　Ranges 算法与投影（C++20））—— 同模块下的其他主题。

## 附录 C（工业级查找实战）

> 下列项目均在生产代码中大规模使用该特性，源码可在其公开仓库核查。

- **Google** — Abseil `flat_hash_map::find` 用 SIMD 探测
- **LLVM** — llvm::StringMap 用开放寻址查找
- **Chromium** — base::Contains 封装线性/哈希查找
- **Boost** — Boost.MultiIndex 提供多索引查找
- **Qt ** — QMap::find 为红黑树查找
- **Eigen** — 内部用二分查找选定点
- **folly** — folly::F14 find 用 SIMD 加速
- **Redis** — dict 查找用递增 rehash
- **ClickHouse** — HashMap find 用 SIMD 探测桶
- **RocksDB** — memtable 查找用跳表
- **V8** — ObjectHashTable find 开放寻址
- **DPDK** — rte_hash find 无锁
- **gRPC** — 序列化 map find 线性
- **spdlog** — registry find 全局 map
- **fmt** — 参数 find 线性
- **Unreal** — TMap::Find 哈希
- **WebKit** — WTF::HashMap::find 开放寻址
- **Mozilla** — nsTHashMap find PLDHash
- **Abseil** — Abseil `absl::c_find` 算法包装
- **Blink** — Blink find 样式属性

## 附录 D：工业实战复盘与设计取舍 [I: Practice / H: Design]

**[经验]**　查找算法的 bug 极少来自算法本身，几乎全部来自"前置条件被违反"。本节从 production 事故与 Code Review 视角总结。

### 常见Bug：二分查找的"静默错误答案"

`std::binary_search` / `lower_bound` / `upper_bound` 的前置条件是**区间按同一比较器有序**（partitioned）。违反时它们**不报错、不崩溃**，只返回**错误答案**——这比崩溃更危险。三个高频 **工业案例**：

1. **未排序就二分**：数据来自网络/DB，开发者假设"应该是有序的"。修复：调试时加 `assert(std::is_sorted(v.begin(), v.end(), cmp))`（Release 下 `is_sorted` 是 O(n)，仅调试期开启）。
2. **比较器与排序不一致**：`sort` 用 `<`（升序）、`lower_bound` 传了 `std::greater`。两者比较器必须**完全一致**。
3. **比较器不满足严格弱序（strict weak ordering）**：写成 `<=` 而非 `<`，或浮点 NaN 参与比较。这在 libstdc++ Debug 模式（`-D_GLIBCXX_DEBUG`）下会被断言抓住，是首选的 **Debug方法**。

### 设计取舍（Trade-off）：find vs lower_bound vs 哈希

| 需求 | 选择 | 设计权衡 |
|---|---|---|
| 无序数据、一次查找 | `std::find` O(n) | 无需排序，n 小时最快（cache 友好、无分支预测失败） |
| 有序数据、多次查找 | `lower_bound` O(log n) | 一次性排序 O(n log n)，之后每次查找廉价 |
| 只问存在性、可容忍假阳性 | Bloom Filter + 哈希 | 用 ~1.2 B/key 内存换 O(1)，适合"先挡不存在的键" |
| 需要"最近邻/范围" | `lower_bound`/`equal_range` | 哈希做不到有序范围，红黑树/有序数组才行 |

**API Design 准则**：返回**迭代器**（`lower_bound`）比返回 **bool**（`binary_search`）更通用——调用方既能判存在（`it!=end && *it==key`），又能拿到插入点。这就是标准库很少直接用 `binary_search` 的原因，也是设计查找 API 时的经验：**返回位置，让调用方决定语义**。

### 反模式（Anti-Pattern）

- **线性扫描热路径**：在每帧/每请求都跑的循环里对大容器 `std::find`，却从不改成哈希/有序结构。Profile 一次就能发现。
- **重复排序**：每次查找前都 `sort` 一遍再二分——排序成本远超收益，应改为"一次排序，多次查找"或直接上哈希表。

**重构建议**：把"频繁 `std::find` 于 `std::vector`"重构为 `std::unordered_map`（无序需求）或"排序后 `lower_bound`"（需范围/有序遍历）；若容器小（<32 元素）则保留线性查找——现代 CPU 上小数组线性扫描常比哈希更快（无哈希计算、cache 命中好）。

### Code Review 检查清单（查找专项）

- [ ] 调用二分类算法前，数据是否**保证**按同一比较器有序？（可加调试期 `is_sorted` 断言）
- [ ] `sort` 与 `lower_bound` 是否使用**完全一致**的比较器？
- [ ] 自定义比较器是否满足严格弱序（用 `<` 不用 `<=`，处理 NaN）？
- [ ] 热路径上的 `std::find` 是否应升级为哈希/有序结构？
- [ ] 用 `lower_bound` 判存在时，是否检查了 `it != end() && *it == key` 两个条件？

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景**：用户画像系统常要在已按用户 ID 排序的明细里快速统计"某个 ID 出现了几次"（如某用户的历史订单数），不能每次线性扫描千万级数据。请利用**已排序** `vector`，用 `std::lower_bound` 与 `std::upper_bound` 配合 `std::distance` 统计某 key 的出现次数。给定 `v{1,2,2,2,3,3,5}`、`key=2`，输出应为 3。为什么必须先保证区间已排序、否则二分结果不可信？

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
int main() {
    std::vector<int> v{1, 2, 2, 2, 3, 3, 5};
    int key = 2;
    auto lo = std::lower_bound(v.begin(), v.end(), key);
    auto hi = std::upper_bound(v.begin(), v.end(), key);
    std::cout << "count(" << key << ") = " << std::distance(lo, hi) << "\n";  // 3
}
```

[标准] 对有序区间，`[lower_bound, upper_bound)` 恰好是等于 key 的元素半开区间；`distance` 得其长度即出现次数。复杂度 O(log n + k)。

[引用] cppreference `std::lower_bound`：`https://en.cppreference.com/w/cpp/algorithm/lower_bound`；`std::upper_bound`：`https://en.cppreference.com/w/cpp/algorithm/upper_bound`。

</details>

### 练习 2（难度 ★★★）

**真实场景**：同练习 1 的画像统计，但你想"既拿到区间又拿到计数"且只做一次二分——`std::equal_range` 一次性返回 `[lower, upper)` 的 `pair`，内部只做约一次对称二分，比分别调用 `lower_bound`/`upper_bound` 少约一半比较。请用 `std::equal_range` 重复练习 1 的计数（给定 `v{1,2,2,2,3,3,5}`、`key=2`，输出应为 3）。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
int main() {
    std::vector<int> v{1, 2, 2, 2, 3, 3, 5};
    auto r = std::equal_range(v.begin(), v.end(), 2);
    std::cout << "count = " << std::distance(r.first, r.second) << "\n";  // 3
}
```

[标准] `equal_range` 等价于「同时返回 lower/upper」，内部只做约一次二分（左右边界对称推进），相比两次独立二分少约一半比较，是「既取区间又求计数」的最优写法。

[引用] cppreference `std::equal_range`：`https://en.cppreference.com/w/cpp/algorithm/equal_range`。

</details>

### 练习 3（难度 ★★★★）

**真实场景**：入侵检测/日志审计里要在一段字节流（母序列）中定位一个特定的特征码（模式序列）首次出现的位置——这正是子序列/模式匹配。`std::search` 就是标准库提供的子序列查找原语。请用 `std::search` 在母序列中查找模式序列首次出现的位置；未找到返回 `end()`。给定 `hay{1,2,3,4,5,6,7,8}`、`pat{4,5,6}`，应输出位置 3。长文本场景为什么可改用 `std::boyer_moore_searcher`？

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> hay{1, 2, 3, 4, 5, 6, 7, 8};
    std::vector<int> pat{4, 5, 6};
    auto it = std::search(hay.begin(), hay.end(), pat.begin(), pat.end());
    if (it != hay.end())
        std::cout << "pattern at idx " << (it - hay.begin()) << "\n";  // 3
    else
        std::cout << "not found\n";
}
```

[标准] `std::search` 是子序列查找（模式匹配），与 `find`（单值查找）不同；返回首个完全匹配的位置。可配合 searcher 对象（如 `std::boyer_moore_searcher`）在长文本场景加速。

[引用] cppreference `std::search`：`https://en.cppreference.com/w/cpp/algorithm/search`；`std::boyer_moore_searcher`：`https://en.cppreference.com/w/cpp/utility/functional/boyer_moore_searcher`。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：仅判存在性——`binary_search` 优于 `find`

**选型场景**：在已排序区间判断某 key 是否存在。错误写法用 `std::find`（O(n)），仅返回一个迭代器再比较 `!= end()`，浪费了「已排序」这一前提。

**常见错误（text）**：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i * 2;
    int key = 1'999'998;
    bool has = std::find(v.begin(), v.end(), key) != v.end();   // 线性 O(n)
    std::cout << "has=" << has << "\n";
}
```

**修复（cpp）**：用 `std::binary_search` 直接返回 `bool`（O(log n)）。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v(1'000'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i * 2;  // 偶数序列
    int key = 1'999'998;
    bool has = std::binary_search(v.begin(), v.end(), key);  // O(log n)
    std::cout << "binary_search=" << has << "\n";   // true
}
```

**结论**：仅判存在用 `std::binary_search`（返回 `bool`）；需要位置/区间才用 `lower_bound`/`equal_range`。不要为「是否存在」付出线性扫描代价。

### 演绎 2：二分的前提是「已排序」

**选型场景**：对未排序区间调用 `std::lower_bound`，得到不可信结果（二分依赖有序前提，违之属逻辑错误）。错误写法直接二分一个乱序容器。

**常见错误（text）**：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};   // 未排序
    int key = 7;
    auto it = std::lower_bound(v.begin(), v.end(), key);   // 前置条件违反 -> 结果不可信
    std::cout << "found=" << (it != v.end() && *it == key) << "\n";
}
```

**修复（cpp）**：二分前先 `std::sort`（生产代码可加 `assert(std::is_sorted(...))`）。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};
    std::sort(v.begin(), v.end());                       // 二分前必须排序
    int key = 7;
    auto it = std::lower_bound(v.begin(), v.end(), key);
    std::cout << "found=" << (it != v.end() && *it == key) << "\n";  // true
}
```

**结论**：二分系列（`lower_bound`/`upper_bound`/`equal_range`/`binary_search`）的前置条件是区间已按同一比较器排序。工业代码应在调试构建中用 `assert(std::is_sorted(...))` 守护该不变量。

## 附录 J：查找算法选型决策流（D3 维度）

```mermaid
flowchart TD
    A["查找需求: 在集合中定位 key"] --> B{"区间已排序?"}
    B -->|否 但需要二分| BS["若需二分先 std::sort 再走二分"]
    B -->|是| C{"需要精确命中 key 还是范围?"}
    C -->|精确命中| C1["binary_search 或 lower_bound+== 检查"]
    C -->|范围| C2["lower_bound/upper_bound/equal_range 取子区间"]
    B -->|否 不想排序| D{"是否允许额外空间建索引?"}
    D -->|是 哈希| D1["unordered_set/map 哈希查找 O(1) 均摊"]
    D -->|是 有序容器| D2["set/map 有序容器 O(log n)"]
    D -->|否| E{"是子串/模式匹配?"}
    E -->|是| E1["std::search / Boyer-Moore"]
    E -->|否| F["std::find 线性 O(n)"]
    F --> G{"区间极大且只读一次?"}
    G -->|是| H["并行 std::find(std::execution::par)"]
    G -->|否| Fend["std::find 单线程"]
    BS --> C
    C1 --> X["落地: 选算法并断言前置不变量"]
    C2 --> X
    D1 --> X
    D2 --> X
    E1 --> X
    H --> X
    Fend --> X
```

> 决策流说明：查找选型的第一问是「区间是否已排序」——已排序则二分系列（`lower_bound`/`equal_range`）把复杂度降到 O(log n)，但必须先用 `is_sorted` 守护；若不想排序且允许建索引，哈希容器 `unordered_*` 提供 O(1) 均摊；都不满足才退回线性 `std::find`。最常见的谬误是「对未排序区间直接调 `binary_search`」——编译通过但结果随机，因二分前置不变量被破坏。

## 附录 K：查找知识图谱（D6 维度）

```mermaid
flowchart TD
    SORT["std::sort (ch96)"] --> SORTED["区间已排序不变量"]
    SORTED --> BIN["二分 lower_bound/upper_bound/equal_range"]
    SORTED --> BS["binary_search"]
    BIN --> BS
    KEY["key 类型严格弱序/等价"] --> BIN
    KEY --> HASH["哈希查找 unordered_*"]
    HASHFN["哈希函数 / 相等"] --> HASH
    HASH --> HIDX["索引构建/内存开销"]
    ORDERED["有序容器 set/map"] --> HIDX
    ITER["迭代器类别"] --> FIND["线性 std::find"]
    ITER --> SEARCH["std::search 子串"]
    ITER --> BIN
    SEARCH --> STR["字符串/范围"]
    COMPLEX["复杂度 O(log n)/O(1)/O(n)"] --> BIN
    COMPLEX --> HASH
    PARA["执行策略"] --> FIND
```

### K.1 概念依赖逐边解读

| 上游概念 | 下游概念 | 依赖含义 |
|---|---|---|
| std::sort (ch96) | 区间已排序不变量 | 二分查找的前置是区间已由 sort 全有序 |
| 区间已排序不变量 | 二分 lower_bound 系列 | lower_bound/upper_bound/equal_range 依赖有序 |
| 区间已排序不变量 | binary_search | binary_search 内部即二分，依赖有序 |
| 二分 lower_bound 系列 | binary_search | binary_search 可用 lower_bound+== 表达 |
| key 类型严格弱序/等价 | 二分 lower_bound 系列 | 二分依赖同一比较器的严格弱序 |
| key 类型严格弱序/等价 | 哈希查找 unordered_* | 哈希容器依赖 key 的等价关系 |
| 哈希函数 / 相等 | 哈希查找 unordered_* | 哈希查找依赖哈希函数与相等谓词 |
| 哈希查找 unordered_* | 索引构建/内存开销 | 哈希容器需额外桶数组，有空间成本 |
| 有序容器 set/map | 索引构建/内存开销 | 有序容器需节点开销维持有序 |
| 迭代器类别 | 线性 std::find | find 依赖输入迭代器即可 |
| 迭代器类别 | std::search 子串 | search 依赖前向迭代器 |
| 迭代器类别 | 二分 lower_bound 系列 | 二分要求随机存取迭代器做下标 |
| std::search 子串 | 字符串/范围 | 子串查找作用在字符串/字符范围上 |
| 复杂度 O(log n)/O(1)/O(n) | 二分 lower_bound 系列 | 二分复杂度 O(log n) 是其选型依据 |
| 复杂度 O(log n)/O(1)/O(n) | 哈希查找 unordered_* | 哈希均摊 O(1) 是其选型依据 |
| 执行策略 | 线性 std::find | C++17 起 find 可接受 par 并行化 |

### K.2 章节闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch96（排序） | ch97（查找） | 全有序区间是二分查找的前置不变量 |
| ch19（迭代器） | ch97 | 迭代器类别决定 find/search/binary 的可用性 |
| ch77（vector） | ch97 | 连续内存使二分缓存友好、分支可预测 |
| ch95（算法总论） | ch97 | 算法总论对查找族的复杂度分类与定位 |
| ch101（算法思想：哈希） | ch97 | 哈希思想支撑 unordered 系列 O(1) 查找 |
| ch115（移动语义） | ch97 | key/value 在有序/哈希容器的插入走移动 |
| ch97（查找） | ch100（ranges） | 查找原语在 ranges 中以 views/算法形式复用 |

## 附录 D4：libstdc++ 15.3.0 源码解析 — 二分查找族（lower/upper/equal_range/binary_search）[E: Low-level / H: Design]

> 本附录所有源码摘录均来自随书工具链 **GCC 15.3.0** 自带的 libstdc++
> （`.../include/c++/15.3.0/`），标注精确到 `文件 L行号`。libc++ / MSVC STL 仅给出"已知公开实现行为"对比，非逐字摘录。
> 摘录块为 `text` 围栏，不参与编译；仅下方"第一方可编译验证"为独立 `cpp` 块。
> 诚实考据：`std::lower_bound` 在 libstdc++ 中**已从 `stl_algo.h` 迁到 `stl_algobase.h`**（源文件 `stl_algo.h` 有注释 `// lower_bound moved to stl_algobase.h`，见 L1943），其内核 `__lower_bound` 在 `stl_algobase.h`；`upper_bound`/`equal_range`/`binary_search` 仍在 `stl_algo.h`。

### D4.1 __lower_bound：无溢出半分（bits/stl_algobase.h L1496-1519）

```text
// bits/stl_algobase.h L1496-1519  (GCC 15.3.0)
    __lower_bound(_ForwardIterator __first, _ForwardIterator __last,
		  const _Tp& __val, _Compare __comp)
    {
      typedef typename iterator_traits<_ForwardIterator>::difference_type
	_DistanceType;

      _DistanceType __len = std::distance(__first, __last);

      while (__len > 0)
	{
	  _DistanceType __half = __len >> 1;
	  _ForwardIterator __middle = __first;
	  std::advance(__middle, __half);
	  if (__comp(__middle, __val))
	    {
	      __first = __middle;
	      ++__first;
	      __len = __len - __half - 1;
	    }
	  else
	    __len = __half;
	}
      return __first;
    }
```

- **`__len >> 1` 无溢出半分**：用右移而非 `/ 2` 求中点，且全程只维护 `__len` 与 `__half`，**从不计算 `__first + (__last - __first)/2`**，因此即使区间内元素极多也不会有 `(last-first)` 溢出（这是 C++ 标准库二分与"手写 mid=(l+r)/2 溢出"经典坑的关键区别）。
- 比较器语义是 `__comp(__middle, __val)`：中点小于目标时向右收缩（`__first = __middle + 1`，`__len -= __half + 1`），否则向左收缩（`__len = __half`）。最终 `__first` 是首个**不小于** `__val` 的位置。

### D4.2 __upper_bound：对称半分（bits/stl_algo.h L1979-2003）

```text
// bits/stl_algo.h L1979-2003  (GCC 15.3.0)
    _ForwardIterator
    __upper_bound(_ForwardIterator __first, _ForwardIterator __last,
		  const _Tp& __val, _Compare __comp)
    {
      typedef typename iterator_traits<_ForwardIterator>::difference_type
	_DistanceType;

      _DistanceType __len = std::distance(__first, __last);

      while (__len > 0)
	{
	  _DistanceType __half = __len >> 1;
	  _ForwardIterator __middle = __first;
	  std::advance(__middle, __half);
	  if (__comp(__val, __middle))
	    __len = __half;
	  else
	    {
	      __first = __middle;
	      ++__first;
	      __len = __len - __half - 1;
	    }
	}
      return __first;
    }
```

与 `__lower_bound` 几乎镜像：比较改为 `__comp(__val, __middle)`，使向右收缩发生在"目标小于中点"时，最终返回首个**大于** `__val` 的位置。

### D4.3 __equal_range：双界联动（bits/stl_algo.h L2068-2101）

`equal_range` 不分别调公开 `lower_bound`/`upper_bound`，而是在一次二分命中等价元素时，**同时收窄左右两界**——左界用 `__lower_bound`、右界用 `__upper_bound`，各只处理剩余半区间。

```text
// bits/stl_algo.h L2068-2101  (GCC 15.3.0)
    __equal_range(_ForwardIterator __first, _ForwardIterator __last,
		  const _Tp& __val,
		  _CompareItTp __comp_it_val, _CompareTpIt __comp_val_it)
    {
      typedef typename iterator_traits<_ForwardIterator>::difference_type
	_DistanceType;

      _DistanceType __len = std::distance(__first, __last);

      while (__len > 0)
	{
	  _DistanceType __half = __len >> 1;
	  _ForwardIterator __middle = __first;
	  std::advance(__middle, __half);
	  if (__comp_it_val(__middle, __val))
	    {
	      __first = __middle;
	      ++__first;
	      __len = __len - __half - 1;
	    }
	  else if (__comp_val_it(__val, __middle))
	    __len = __half;
	  else
	    {
	      _ForwardIterator __left
		= std::__lower_bound(__first, __middle, __val, __comp_it_val);
	      std::advance(__first, __len);
	      _ForwardIterator __right
		= std::__upper_bound(++__middle, __first, __val, __comp_val_it);
	      return pair<_ForwardIterator, _ForwardIterator>(__left, __right);
	    }
	}
      return pair<_ForwardIterator, _ForwardIterator>(__first, __first);
    }
```

- 前两个分支与 `lower_bound`/`upper_bound` 完全相同；仅当 `__middle` 与 `__val` **等价**（既不 `<` 也不 `>`）时进入 `else`：用 `__lower_bound` 在左半 `[first, middle)` 收左界、用 `__upper_bound` 在右半 `(middle, first+len)` 收右界。
- 由于命中后即缩小搜索范围，整体仍是 **O(log n)**，且只需一次"走到等价点"的二分，比"先 lower 再 upper"各做一遍略省。

### D4.4 binary_search：用 lower_bound 一行合成（bits/stl_algo.h L2194-2208）

```text
// bits/stl_algo.h L2194-2208  (GCC 15.3.0)
    binary_search(_ForwardIterator __first, _ForwardIterator __last,
		  const _Tp& __val)
    {
      // concept requirements
      __glibcxx_function_requires(_ForwardIteratorConcept<_ForwardIterator>)
      __glibcxx_function_requires(_LessThanOpConcept<
	_Tp, typename iterator_traits<_ForwardIterator>::value_type>)
      __glibcxx_requires_partitioned_lower(__first, __last, __val);
      __glibcxx_requires_partitioned_upper(__first, __last, __val);

      _ForwardIterator __i
	= std::__lower_bound(__first, __last, __val,
			     __gnu_cxx::__ops::__iter_less_val());
      return __i != __last && !(__val < *__i);
    }
```

- 直接复用 `__lower_bound` 找到首个 `>= val` 的位置 `__i`；若 `__i` 未到 `last` 且 `__val < *__i` 不成立（即 `*__i == val`），则存在。一行合成，零重复逻辑。

### D4.5 跨实现对比（二分查找族）

| 维度 | libstdc++ (GCC 15.3.0) | libc++ (LLVM) | MSVC STL |
|------|------------------------|---------------|----------|
| 无溢出半分 | `__len >> 1`，不计算 `last-first` 中点 | 同样维护长度用 `>>1`（已知公开行为） | 同样维护长度用 `>>1`（已知公开行为） |
| lower_bound 位置 | 已迁至 `stl_algobase.h` | 在其 `<algorithm>` 实现内（组织不同，实现细节未公开核对） | 在其 `<algorithm>` 实现内（实现细节未公开核对） |
| equal_range 双界 | 命中即同时收窄左右界（D4.3） | 同样在一次二分内双界联动（已知公开行为） | 同样双界联动（已知公开行为） |
| binary_search | 复用 lower_bound + `!(val < *i)` | 同样复用 lower_bound（已知公开行为） | 同样复用 lower_bound |

> libc++ / MSVC 行为为**已知公开实现行为**（可在 llvm-project / microsoft/STL 仓库核实），非逐字摘录；宏名与版本细节随发行版变动。

### D4.6 第一方可编译验证（二分查找族）

```cpp
#include <iostream>
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> v{1,2,2,2,3,4,5};
    std::cout << std::boolalpha;
    // binary_search 用 lower_bound + !comp
    std::cout << std::binary_search(v.begin(), v.end(), 2) << std::endl;  // true
    std::cout << std::binary_search(v.begin(), v.end(), 9) << std::endl;  // false

    // lower_bound / upper_bound 边界
    auto lo = std::lower_bound(v.begin(), v.end(), 2);
    auto up = std::upper_bound(v.begin(), v.end(), 2);
    std::cout << (lo - v.begin()) << std::endl;   // 1
    std::cout << (up - v.begin()) << std::endl;   // 4

    // equal_range 双界联动
    auto rng = std::equal_range(v.begin(), v.end(), 2);
    std::cout << (rng.first - v.begin()) << ' '
              << (rng.second - v.begin()) << std::endl;  // 1 4
    return 0;
}
```

预期输出依次为 `true / false / 1 / 4 / 1 4`——`lower_bound` 落在首个 `2`（下标 1）、`upper_bound` 落在首个 `>2`（下标 4）、`equal_range` 双界恰为 `[1,4)`、`binary_search` 借 `lower_bound` 正确判定存在性，与 D4.1–D4.4 源码一致。

## 附录 D5：真实基准与性能分析 — sorted vector / set / unordered_set 查找（GCC 15.3.0）

> 测试环境：AMD Ryzen 9 7940HX（16C/32T）；本机 Windows / MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++23`；`std::chrono::steady_clock` 计时，多轮取稳定值（串行实测，无并发干扰）；`volatile` sink 防死代码消除。本附录目的：用主控实测锁死的真实毫秒，量化 sorted vector + lower_bound、set、unordered_set 三类查找的相对开销，并给出非显然根因。**绝对毫秒随机器而变，加速比才是可移植信号。**

### D5.1 基准数据

400 万键，200 万次查询全命中，mt19937 随机键。"加速比"以 sorted vector lower_bound 为 1.00× 基准。

| 场景 | 耗时 ms | 加速比 |
|---|---|---|
| sorted vector + `lower_bound` | 643.5 | 1.00×（基准） |
| `set::find` | 2593.9 | 0.25×（比 lower_bound 慢 4.03×） |
| `unordered_set::find` | 154.4 | 4.17×（比 lower_bound 快 4.17×，比 set 快 16.8×） |

### D5.2 非显然结论

1. **同为 O(log N) 二分，set 比 sorted vector 慢 4.03×。** 根因是节点离散堆分配：红黑树每步跳转都是一次不可预取的随机指针追逐（400 万节点 × 每节点 40+ 字节控制块，缓存命中率极低）；sorted vector 二分虽也随机访问，但数据连续、最后几步落在同一 cache line，且无指针依赖链，预取器与硬件能部分掩盖延迟。

2. **unordered_set 快在 O(1) 桶直达。** 根因：一次哈希 + 一次桶头指针 + 平均 <1 次链表跳转，约 77ns/查询 ≈ 一两次 cache miss 的成本，性能被内存延迟而非哈希函数主导——哈希计算本身几乎可忽略。

3. **工程决策表：** 只查不改 / 批量建一次 → sorted vector（缓存友好、内存紧凑）；需有序遍历 + 频繁增删 → set（顺序迭代免费）；纯点查 → unordered_set（但迭代慢、无序、最坏 O(n) 退化）。

4. **与 ch83 D5「map vs unordered_map 22.5×」互证。** 那边测的是 map（红黑树，节点更肥、控制块更大），故比 unordered_map 慢到 22.5×；本章 set 节点也离散，但键为 int、控制块相对 map 的 pair 更瘦，故"仅"慢 16.8×——结论一致：离散节点查找的瓶颈在缓存，而非算法阶数。

### D5.3 可复现 demo

```cpp
#include <iostream>
#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <random>
#include <cassert>

int main() {
    const std::size_t N = 4'000'000;   // 400 万键
    std::vector<int> keys(N);
    std::mt19937 gen(20240701);
    for (std::size_t i = 0; i < N; ++i) keys[i] = static_cast<int>(gen());

    std::vector<int> sorted = keys;
    std::sort(sorted.begin(), sorted.end());
    std::set<int> s(keys.begin(), keys.end());
    std::unordered_set<int> us(keys.begin(), keys.end());

    // 200 万次查询全命中：取容器内真实存在的键
    std::size_t found_vec = 0, found_set = 0, found_us = 0;
    const std::size_t Q = 2'000'000;
    std::mt19937 qgen(987654321);
    for (std::size_t i = 0; i < Q; ++i) {
        int q = keys[qgen() % keys.size()];
        if (std::binary_search(sorted.begin(), sorted.end(), q)) ++found_vec;
        if (s.find(q) != s.end()) ++found_set;
        if (us.find(q) != us.end()) ++found_us;
    }

    std::cout << "found by vector : " << found_vec << std::endl;
    std::cout << "found by set    : " << found_set << std::endl;
    std::cout << "found by unord  : " << found_us << std::endl;

    // 功能正确性：全命中场景下三者查找结果必须一致，绝不断言时间/倍数
    assert(found_vec == Q);
    assert(found_set == Q);
    assert(found_us == Q);
    return 0;
}
```

### D5.4 方法学注

- 计时取多轮稳定值，规避调度抖动与冷热启动偏差；`volatile` sink 防 DCE。
- 加速比（4.03× / 4.17× / 16.8×）是可移植信号；绝对毫秒随 CPU、内存、编译器版本而变，请勿跨机器直接比较毫秒。
- 复现旗标：`g++ -O2 -std=c++23`。基准源码见库根 `_bench_d5_97_search.cpp`。
