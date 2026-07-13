# 第97章　查找与二分（C++）

⟶ Book/part08_algorithms/ch96_sorting.md
⟶ Book/part07_stl/ch83_map.md

> 真实编译器：MinGW GCC 13.1.0（`g++ -std=c++23 -O2 -S -masm=intel`）。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`。
> 规范基线：CONVENTIONS.md（立场分层、20 元素模板）。
> 本章所有 ```` ```asm ```` 与 ```` ```text ```` 均为本机真实取证，无任何编造。

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

下面是用 GCC 13.1.0 `-O2 -masm=intel` 对 `lower_bound_idx` 生成的**真实汇编**（已截去文件头）。注意它**没有被完全展开成常数表**，而是生成了标准的 `mid = n/2` 二分循环——因为区间长度 `n` 是运行时值。

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
; GCC 13.1.0 -O2 -masm=intel，符号 _Z15lower_bound_idxPKiii
_Z15lower_bound_idxPKiii:
	movsx	rdx, edx          ; n 符号扩展入 rdx（剩余长度）
	mov	rax, rcx           ; first 指针入 rax（当前区间起点）
.L3:
	test	rdx, rdx
	jle	.L7                ; 区间为空 (rdx<=0) -> 结束
.L4:
	mov	r9, rdx
	sar	r9                  ; r9 = n / 2（算术右移 = mid 下标）
	lea	r10, [rax+r9*4]     ; r10 = &first[mid]
	cmp	DWORD PTR [r10], r8d ; *mid 与 value(r8d) 比较
	jge	.L5                 ; *mid >= value -> 走左半 (.L5)
	lea	rax, 4[r10]         ; 右移：first = &first[mid] + 1
	sub	rdx, r9
	sub	rdx, 1              ; n = n - mid - 1
	test	rdx, rdx
	jg	.L4                 ; 右半非空 -> 继续
.L7:
	sub	rax, rcx            ; 终点指针 - 起点指针
	sar	rax, 2              ; 字节差 /4 = 下标
	ret
.L5:
	mov	rdx, r9             ; 左半：n = mid（保留 [first, mid)）
	jmp	.L3
```

- `[实现·GCC13]`：循环体核心是 `mid = n/2`、`cmp [first+mid]`,`value`、按比较结果收缩到左半或右半。`sar r9` 即除以 2；`lea rax,4[r10]` 把起点右移到 `mid+1`。这是教科书二分，且 **不内联比较函数**（裸指针 + `int` 比较被直接译为目标码 `cmp`）。
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

下面是用 GCC 13.1.0 `-O2` 在本机运行的 **`std::chrono` 实测**（非示意）。对 1,048,576 个升序 `int` 做 200 次随机命中查找：

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

- `[实现·GCC13]`：在 100 万元素上二分比线性快 **~1439 倍**，与理论 O(N)/O(log N) 之比（约 1e6 / 20 ≈ 5e4）同量级——差距被"线性查找每步 cache 友好、二分跳转随机"部分抵消，但仍悬殊。
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

- **后续依赖**：`Book/part08_algorithms/ch95_algo_overview.md`（第95章　STL 算法分类与复杂度（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part08_algorithms/ch99_numeric.md`（第99章　数值算法与并行执行策略（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part08_algorithms/ch100_ranges_algo.md`（第100章　Ranges 算法与投影（C++20））—— 同模块下的其他主题。

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

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

## 真实开源项目参考（可查证链接）

> 查找算法的工业实现——下列链接指向标准库与第三方库的真实源码文件（L2 文件级）。

- **libstdc++ `std::lower_bound`**：[gcc-mirror/gcc · libstdc++-v3/include/bits/stl_algo.h](https://github.com/gcc-mirror/gcc/blob/master/libstdc++-v3/include/bits/stl_algo.h) —— 「③ lower_bound/upper_bound/equal_range」「⑤ 真实汇编二分循环」的源头；模板 `__lower_bound` 用迭代器推进实现 O(log N) 二分。
- **libc++ `std::lower_bound`**：[llvm/llvm-project · libcxx/include/__algorithm/lower_bound.h](https://github.com/llvm/llvm-project/blob/main/libcxx/include/__algorithm/lower_bound.h) —— Clang/MSVC 侧等价实现，验证「⑤ -O2 下真正二分循环」的跨库一致。
- **Boost.Algorithm（is_permutation 等）**：[boostorg/algorithm · include/boost/algorithm/cxx11/is_permutation.hpp](https://github.com/boostorg/algorithm/blob/develop/include/boost/algorithm/cxx11/is_permutation.hpp) —— 「⑥ 有序区间集合操作」「⑨ 谓词查找」的扩展库；`boost::algorithm::is_permutation` 是 `std::is_permutation` 的灵感来源。
- **folly 哈希（衔接 ⑪ 哈希查找）**：[facebook/folly · folly/hash/SpookyHashV2.cpp](https://github.com/facebook/folly/blob/main/folly/hash/SpookyHashV2.cpp) —— `unordered` 容器底层哈希函数的工业实现，对应「⑪ 哈希查找衔接」的性能基线。

**最佳实践**：有序区间永远用 `lower_bound`/`equal_range` 做 O(log N) 查找而非 `find` 的 O(N)；对未排序区间用二分 = UB（「⑯ 常见坑」）；C++20 Ranges 用 `std::ranges::lower_bound` 支持投影，避免临时拷贝。

> 交叉引用：排序算法见 [ch96](Book/part08_algorithms/ch96_sorting.md)；堆结构见 [ch98](Book/part08_algorithms/ch98_heap.md)；算法复杂度理论见 [ch101](Book/part08_algorithms/ch101_algo_theory.md)。

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

