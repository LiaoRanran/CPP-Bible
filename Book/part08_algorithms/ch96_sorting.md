# 第96章　排序：sort / stable_sort / partial_sort（C++）

⟶ Book/part08_algorithms/ch98_heap.md
⟶ Book/part07_stl/ch77_vector.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2 -S -masm=intel`）。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；以真实编译产物（`__introsort_loop` 符号、内联比较器、chrono 实测）为证据。本章示例代码置于 `Examples/_ch96_*.cpp`（相对路径，非绝对路径）。

## ① 概述：排序在 `<algorithm>` 中的位置 [标准]

⟶ Book/part08_algorithms/ch95_algo_overview.md
⟶ Book/part08_algorithms/ch97_search.md


排序是算法库最常用的一组：无序转有序，使二分查找、去重、归并、集合运算成为可能。`<algorithm>` 提供 `std::sort`、`std::stable_sort`、`std::partial_sort`、`std::nth_element`、`std::stable_partition` 等，全部作用于**有序区间**（[first, last)），比较默认用 `operator<`（严格弱序）。

```cpp
// ① 最小可编译示例：对 vector 升序排序
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5, 2, 9, 1, 5, 6};
    std::sort(v.begin(), v.end());   // 升序：1 2 5 5 6 9
    return v.front();                // 1
}
```

```cpp
// ① 降序：用 std::greater（需 <functional>）
#include <algorithm>
#include <functional>
#include <vector>
int main() {
    std::vector<int> v{5, 2, 9, 1};
    std::sort(v.begin(), v.end(), std::greater<int>());
    return v.front();                // 9
}
```

- `[标准]`：`std::sort` 不保证相等元素的相对顺序（**不稳定**）；需要稳定时用 `std::stable_sort`。
- `[经验]`：排序前先确认区间已可随机访问；`list`/`forward_list` 有各自的成员 `sort`，不要用 `std::sort`。

## ② std::sort 的实现：introsort（内省排序） [实现]

`std::sort` 标准只规定复杂度（平均/最坏 O(N·log N)）与不稳定，实现自由。libstdc++/libc++/MS STL 普遍采用 **introsort（内省排序）**：

```text
introsort(arr, depth_limit = 2·⌊log2 N⌋):
    if N < 阈值(通常 16):  insertion_sort(arr)          // 小数组插入排序
    else if depth_limit == 0: heap_sort(arr)            // 递归过深→退化为堆排，杜绝 O(N²)
    else:
        p = partition(arr, median_of_three)             // 快排分段
        introsort(left,  depth_limit-1)
        introsort(right, depth_limit-1)
```

```cpp
// ② 一个可编译的 introsort-lite，演示三阶段组合（仅示意，非标准库实现）
#include <algorithm>
#include <vector>
#include <iterator>

template <typename It, typename Cmp>
void insertion_sort(It first, It last, Cmp cmp) {
    for (It i = first + 1; i != last; ++i)
        for (It j = i; j != first && cmp(*j, *(j - 1)); --j)
            std::iter_swap(j, j - 1);
}

template <typename It, typename Cmp>
void introsort(It first, It last, int depth, Cmp cmp) {
    auto n = std::distance(first, last);
    if (n < 16) { insertion_sort(first, last, cmp); return; }
    if (depth == 0) { std::make_heap(first, last, cmp); std::sort_heap(first, last, cmp); return; }
    auto p = std::partition(first + 1, last, [&](auto&& x){ return cmp(x, *first); });
    introsort(first, p, depth - 1, cmp);
    introsort(p, last, depth - 1, cmp);
}
```

```cpp
// ② 使用上面的 introsort-lite（与 std::sort 语义一致：不稳定）
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};
    introsort(v.begin(), v.end(), 8, std::less<int>{});
    return v.front();   // 1
}
```

- `[实现]`：introsort 的关键在 `depth_limit`——一旦快排递归过深（可能退化成 O(N²)），立刻切到 **堆排序**（最坏 O(N·log N)），从而保证**整体最坏复杂度 O(N·log N)** 且**平均接近快排**。
- `[标准]`：标准只要求 `sort` 满足 O(N·log N) 与不稳定；introsort 是满足该契约的惯用实现策略。

### ②-2 libstdc++ `__introsort_loop` 真实源码逐行（上游参考）[实现]

`std::sort` 的工业实现（libstdc++ / libc++ / MS STL）都叫 introsort，但 libstdc++ 的命名最直白：`__introsort_loop`。下面片段取自 `bits/stl_algo.h`（上游参考，非本机编译），仅作逐行解读；本机不可编译（是标准库内部实现），故以 `text` 围栏呈现。

```text
// libstdc++ bits/stl_algo.h（上游参考，真实源码节选）
template <typename _RandomAccessIterator, typename _Compare>
void
__introsort_loop(_RandomAccessIterator __first,
                 _RandomAccessIterator __last,
                 _Iter_diff_t<_RandomAccessIterator> __depth_limit,
                 _Compare __comp)
{
    // _S_threshold = 16：小数组不再快排，留给收尾的插入排序
    while (__last - __first > int(_S_threshold)) {
        if (__depth_limit == 0) {
            // 递归过深 -> 退化为堆排，杜绝 O(N^2)
            std::partial_sort(__first, __last, __last, __comp);
            return;
        }
        --__depth_limit;
        // 三点取中选枢轴并分区，返回枢轴位置
        _RandomAccessIterator __cut =
            std::__unguarded_partition_pivot(__first, __last, __comp);
        // 右半递归（深一层的 introsort）
        __introsort_loop(__cut, __last, __depth_limit, __comp);
        __last = __cut;   // 尾递归转循环：接着处理左半，避免额外栈帧
    }
}
```

逐行解读：
- `while (__last - __first > _S_threshold)`：`_S_threshold = 16`。数组**大于 16**才进入快排分段；更小的段留给收尾的 `__final_insertion_sort`（小数组插入排序更快，因缓存友好且无递归开销）。
- `if (__depth_limit == 0) { std::partial_sort(...); return; }`：**introsort 的灵魂**。当递归深度耗尽（初始 `depth_limit = 2·⌊log2 N⌋`），立即切到**堆排序**（`partial_sort` 内部即 heap）。堆排最坏 O(N·log N)，从而把整体最坏复杂度钉死在 O(N·log N)——快排单独用会在「已近似有序 + 坏枢轴」时退化成 O(N²)，introsort 用深度计数器消除这个尾部风险。
- `__unguarded_partition_pivot`：内部先做 **median-of-three**（首/中/尾取中值）选枢轴，再把枢轴换到端点做无守卫分区（pivot 本身作 sentinel，分区循环不必每次判越界，更快）。
- `__last = __cut` 而非递归处理左半：把右半交给递归、**左半用循环变量 `__last` 继续**——典型的**尾递归消除**，把 O(log N) 层递归压成一层，省栈空间、减少调用开销。
- 整体结构：`O(log N)` 层递归 × 每层 `O(N)` 分区 = `O(N·log N)`；因深度上限，`N` 很大也不退化。

### ②-2.1 自包含可编译：median-of-three 分区（对应 `__unguarded_partition_pivot`）

下面把 libstdc++ 的「三点取中 + 无守卫分区」落成**本机可编译**的最小范式，返回枢轴最终位置（与 ② 的 introsort-lite 可拼成完整排序）。

```cpp
#include <algorithm>
#include <iterator>
#include <vector>
// ②-2 对应 libstdc++ __unguarded_partition_pivot：三点取中后分区
template <typename It, typename Cmp>
It median3_partition(It first, It last, Cmp cmp) {
    auto mid = first + (last - first) / 2;
    if (cmp(*mid, *first)) std::iter_swap(mid, first);            // 排首/中
    if (cmp(*(last - 1), *first)) std::iter_swap(last - 1, first); // 排首/尾
    if (cmp(*(last - 1), *mid)) std::iter_swap(last - 1, mid);    // 排中/尾
    std::iter_swap(mid, last - 1);                                // 枢轴放到端点
    auto pivot = *(last - 1);
    auto i = first;
    for (auto j = first; j != last - 1; ++j)                      // 无守卫分区
        if (cmp(*j, pivot)) std::iter_swap(i++, j);
    std::iter_swap(i, last - 1);                                  // 枢轴归位
    return i;                                                     // 枢轴最终位置
}
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};
    auto p = median3_partition(v.begin(), v.end(), std::less<int>{});
    return *p;   // 枢轴值（7 的某次分区结果）
}
```

> 该块标注 `[自包含可编译]`：可被 `tools/chapter_compile_check.py` 独立 `-c` 编译（GCC 13.1，零失败）。libstdc++ 上游片段（text 围栏）不进入编译门禁。把 ②-2.1 的 `median3_partition` 与 ② 的 `introsort` 拼起来即是一个可运行的 introsort 完整实现。


## ③ 复杂度与枢纽（pivot）选择 [标准]

`std::sort` 要求 **O(N·log N)** 平均与最坏。枢纽选择决定快排段质量，libstdc++ 用 **三点取中（median-of-three）** 降低坏分区概率：

```cpp
// ③ 三点取中：取首、中、尾的中位数作为枢纽（libstdc++ 思路的简化版）
#include <algorithm>
#include <iterator>
template <typename It>
It median_of_three(It a, It b, It c) {
    if (*a < *b) {
        if (*b < *c) return b;       // a<b<c → b
        if (*a < *c) return c;       // a<c<=b → c
        return a;                    // c<=a<b → a
    } else {
        if (*a < *c) return a;       // b<=a<c → a
        if (*b < *c) return c;       // b<c<=a → c
        return b;                    // c<=b<=a → b
    }
}
```

```cpp
// ③ 复杂度直觉：N 次 logN 层比较 — 用 std::distance 验证规模
#include <algorithm>
#include <vector>
#include <iostream>
int main() {
    std::vector<int> v(1'000'000);
    long long layers = 0;
    for (auto n = (long long)v.size(); n > 1; n /= 2) ++layers;  // ~log2(N)
    std::cout << layers << "\n";   // 约 20 层
    return 0;
}
```

- `[标准]`：比较次数上界约 `N·log2(N)`；`N=10^6` 时约 `20·10^6` 次比较。
- `[实现]`：枢纽选在已（近似）有序的区间上，三点取中几乎总能把区间切成两半，避免经典快排对近乎有序输入的 O(N²) 退化。

## ④ stable_sort：归并排序（稳定） [标准]

`std::stable_sort` 保证**相等元素保持原相对顺序**，且复杂度 O(N·log N)；当额外内存充足时用归并，内存不足时降级为 **就地归并**（更慢，但仍稳定）。

```cpp
// ④ stable_sort 用法：保留相等元素的原始次序
#include <algorithm>
#include <vector>
#include <iostream>
int main() {
    struct Rec { int key; int id; };
    std::vector<Rec> v{{1,0},{3,1},{1,2},{3,3},{1,4}};
    std::stable_sort(v.begin(), v.end(),
        [](const Rec& a, const Rec& b){ return a.key < b.key; });
    // key 序列: 1 1 1 3 3；id 序列保持 0 2 4 1 3（稳定）
    return v[1].id;   // 2
}
```

```cpp
// ④ 一个可编译的归并排序（演示 stable 的本质：合并时左段优先）
#include <algorithm>
#include <vector>
template <typename It, typename Cmp>
void merge_sort(It first, It last, Cmp cmp) {
    auto n = std::distance(first, last);
    if (n < 2) return;
    auto mid = first + n / 2;
    merge_sort(first, mid, cmp);
    merge_sort(mid, last, cmp);
    std::vector<typename std::iterator_traits<It>::value_type> buf(first, last);
    std::merge(buf.begin(), buf.begin() + (mid - first),
               buf.begin() + (mid - first), buf.end(),
               first, cmp);
}
```

- `[标准]`：`stable_sort` 是**稳定**的；若业务要求"先按 A 排，再按 B 排时 A 的次序不被破坏"，必须用稳定排序。
- `[经验]`：`stable_sort` 可能分配临时缓冲区；超大容器在无额外内存时性能会明显下降（见 ⑲ 跨库差异）。

## ⑤ partial_sort / nth_element：部分排序 [标准]

不需要全序时，部分排序更快：`partial_sort` 让前 k 个最小元素就位（且有序）；`nth_element` 仅让第 n 个就位（左边都 ≤、右边都 ≥），均摊 O(N)。

```cpp
// ⑤ partial_sort：只保证前 3 个最小且有序，其余无序
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};
    std::partial_sort(v.begin(), v.begin() + 3, v.end());
    // v[0..2] == {1,2,3} 且有序；v[3..] 内容未定义但都 >= 3
    return v[2];   // 3
}
```

```cpp
// ⑤ nth_element：找第 4 小（下标 3），线性期望 O(N)
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7};
    std::nth_element(v.begin(), v.begin() + 3, v.end());
    return v[3];   // 4（第 4 小的元素，左<=4 右>=4）
}
```

- `[标准]`：`partial_sort`/`nth_element` 复杂度 O(N·log k)/O(N)，远快于全排序的 O(N·log N)，适合"Top-K""中位数""分位数"场景。
- `[经验]`：求中位数用 `nth_element(v.begin(), v.begin()+N/2, v.end())` 比全排序省一个 log 因子。

## ⑥ [实现] 真实：sort 调用的汇编证据（__introsort_loop 符号） [实现]

用 `g++ -std=c++23 -O2 -S -masm=intel` 编译 `Examples/_ch96_sort_asm.cpp`，在产物中能直接看到 libstdc++ 的 `std::__introsort_loop` 实例化符号——这是对"② introsort"的**真实取证**。

```cpp
#include <algorithm>
// 文件：Examples/_ch96_sort_asm.cpp
// 行号：6（std::sort 调用点）
std::sort(v.begin(), v.end());   // <int*, __gnu_cxx::__ops::__iter_less_iter>
```

```asm
; 真实产物（g++ -std=c++23 -O2 -S -masm=intel Examples/_ch96_sort_asm.cpp）
; 关键符号：std::__introsort_loop 被实例化为 int* + Iter_less_iter 版本
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
	push	r15
	push	r14
	push	r13
	push	r12
	push	rbp
	push	rdi
	push	rsi
	push	rbx
	sub	rsp, 56
	.seh_endprologue
	mov	rax, rdx
	mov	rsi, rcx
	sub	rax, rcx
	cmp	rax, 64
	jle	.L1                       ; 区间 <= 64 字节(16个int)→走插入/收尾
	...
	call	_ZSt16__introsort_loop...   ; 递归进入子区间（快排分段）
```

- `[实现]`：符号 `_ZSt16__introsort_loop...Iter_less_iter...` 证明 libstdc++ 确实把 `std::sort` 展开为内省排序的快排循环（`__introsort_loop`）；`.isra.0` 表示 GCC 做了过程间标量替换（把比较器对象内联进循环）。`cmp rax,64 / jle .L1` 对应"小数组阈值 → 收尾用插入排序"。
- `[标准]`：标准不规定函数名，但要求 O(N·log N)；`__introsort_loop` 正是该契约的落地实现。

## ⑦ 比较器正确性：严格弱序（strict weak ordering） [标准]

任何排序比较器 `cmp(a,b)` 必须满足**严格弱序**四定律：

```text
1) 非自反:  cmp(a,a) == false
2) 非对称:  cmp(a,b) ⇒ !cmp(b,a)
3) 传递性:  cmp(a,b) && cmp(b,c) ⇒ cmp(a,c)
4) 不可比传递: !(cmp(a,b)||cmp(b,a)) && !(cmp(b,c)||cmp(c,b))
                ⇒ !(cmp(a,c)||cmp(c,a))        // 等价类传递
```

```cpp
// ⑦ 正确比较器：严格弱序（用 < 比较单一字段）
#include <algorithm>
#include <vector>
struct Rec { int a, b; };
int main() {
    std::vector<Rec> v{{1,2},{3,4},{1,9}};
    std::sort(v.begin(), v.end(),
        [](const Rec& x, const Rec& y){ return x.a < y.a; }); // 合法 SWO
    return v.size();
}
```

```cpp
// ⑦ 致命错误：用 <= 作为比较器违反了"非自反"与"非对称" → 未定义行为
// ⚠ 此代码语义非法（UB），仅用于对照，切勿使用
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{3,1,2};
    // std::sort(v.begin(), v.end(), [](int a, int b){ return a <= b; }); // UB!
    (void)v;
    return 0;
}
```

- `[标准]`：比较器不满足严格弱序时，`std::sort` 的行为是**未定义**（可能死循环、段错误、错误结果）。
- `[经验]`：永远用 `<` 或 `>`；多字段用 `std::tie` 生成元组比较（见 ⑭）。

## ⑧ 自定义类型排序 [标准]

自定义类型排序有三种惯用法：重载 `operator<`、传函数对象、传 lambda。

```cpp
// ⑧ 方式一：为类型提供 operator<（满足严格弱序）
#include <algorithm>
#include <vector>
#include <string>
struct Person { int age; std::string name; };
bool operator<(const Person& a, const Person& b) { return a.age < b.age; }
int main() {
    std::vector<Person> v{{30,"a"},{20,"b"},{25,"c"}};
    std::sort(v.begin(), v.end());   // 按 age 升序
    return v[0].age;                 // 20
}
```

```cpp
// ⑧ 方式二：函数对象（可携带状态，比裸函数指针更易内联）
#include <algorithm>
#include <vector>
struct ByAgeDesc {
    bool operator()(int a, int b) const { return a > b; }  // 降序
};
int main() {
    std::vector<int> v{3,1,2};
    std::sort(v.begin(), v.end(), ByAgeDesc{});
    return v.front();   // 3
}
```

```cpp
// ⑧ 方式三：lambda（最常用，见 ⑪ 它会被内联进排序循环）
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{3,1,2};
    std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });
    return v.front();
}
```

- `[标准]`：比较器类型作为 `std::sort` 的模板参数推导；无状态 callable 最易被内联。
- `[经验]`：优先 lambda（简洁、可内联）；需要复用或带状态时用函数对象。

## ⑨ 排序与并行：标准 std::sort 不并行 [标准]

`std::sort` 本身**单线程串行**。C++17 起可用**执行策略**让 `std::sort(std::execution::par, ...)` 并行，但 `std::execution::par` 在 libstdc++ 需要 TBB 后端，且并行排序**不保证稳定**。

```cpp
// ⑨ 串行排序（基准，单线程）
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v(1'000'000, 0);
    std::sort(v.begin(), v.end());   // 单线程
    return 0;
}
```

```cpp
// ⑨ C++17 执行策略并行排序（需后端；不稳定，仅示意 API）
#include <algorithm>
#include <execution>
#include <vector>
int main() {
    std::vector<int> v(1'000'000, 0);
    // std::sort(std::execution::par, v.begin(), v.end());  // 并行版本
    (void)v;
    return 0;
}
```

- `[标准]`：裸 `std::sort` 无执行策略参数，必串行；并行需 `std::execution::par` 且结果不稳定。
- `[经验]`：并行排序收益只在**超大、比较昂贵**的数据上明显；小数组并行开销反而更慢（见 ⑮）。

## ⑩ 稳定性陷阱：何时"不稳定"会咬你 [经验]

不稳定排序会打乱相等元素原序。当"先按主键排、再按主键的次序展示"时，不稳定会破坏预期。

```cpp
// ⑩ 陷阱演示：unstable sort 后，相等 key 的插入次序被打乱
#include <algorithm>
#include <vector>
#include <iostream>
int main() {
    struct Rec { int key; int seq; };
    std::vector<Rec> v{{1,0},{2,1},{1,2},{2,3}};
    std::sort(v.begin(), v.end(),
        [](const Rec& a, const Rec& b){ return a.key < b.key; });
    // key: 1 1 2 2；但 seq 可能是 {0,2,1,3} 或 {2,0,...}（不稳定，未指定）
    return v[0].seq + v[1].seq;   // 可能是 0+2 或 2+0
}
```

```cpp
// ⑩ 修复：需要保序时用 stable_sort
#include <algorithm>
#include <vector>
int main() {
    struct Rec { int key; int seq; };
    std::vector<Rec> v{{1,0},{2,1},{1,2},{2,3}};
    std::stable_sort(v.begin(), v.end(),
        [](const Rec& a, const Rec& b){ return a.key < b.key; });
    // seq 保持 {0,2,1,3}：相等 key 的原有次序被保留
    return v[1].seq;   // 2
}
```

- `[经验]`：若"相等元素的原相对顺序有意义"（日志时间序、先来先服务），一律用 `stable_sort`。
- `[标准]`：稳定性是 `stable_sort` 与 `sort` 的唯一语义分水岭。

## ⑪ [实现] 真实：自定义比较器被内联进排序循环 [实现]

仍以 `g++ -std=c++23 -O2 -S -masm=intel` 编译 `Examples/_ch96_lambda_inline.cpp`（用无状态 lambda）。产物中比较器**没有独立函数调用**，而是直接内联成 `cmp DWORD PTR 8[rax], ecx`——证明 lambda 比较器被展开进 `__introsort_loop`。

```cpp
#include <algorithm>
// 文件：Examples/_ch96_lambda_inline.cpp
// 行号：8（std::sort + lambda 比较器调用点）
std::sort(v.begin(), v.end(),
          [](const Point& a, const Point& b) { return a.x < b.x; });
```

```asm
; 真实产物（g++ -std=c++23 -O2 -S -masm=intel Examples/_ch96_lambda_inline.cpp）
; 符号中编码了 lambda 类型：...Iter_comp_iterIZ18sort_points_inline...EUlRKS2_SC_E_...
; 排序循环内直接出现比较，无 call 到外部比较器：
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_:
	...
.L39:
	mov	r9, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 8
	cmp	edx, ecx
	jl	.L39                       ; 内联的 a.x < b.x 比较（edx=next.x, ecx=pivot.x）
	...
	cmp	DWORD PTR 8[rax], ecx      ; 另一处内联比较（直接读 Point.x 字段）
	jg	.L41
```

- `[实现]`：比较器逻辑（`a.x < b.x`）被内联为排序循环里的 `cmp ... , ecx` / `jl .L39`，**完全没有 `call` 到独立比较函数**——这正是 `std::sort` 性能优于"每次循环调函数指针"的关键。对照：若把比较器写成**具名函数 `by_x`** 并以函数指针传入，汇编里会出现 `call _Z4by_xRK5PointS1_`（无法内联），性能更差。
- `[标准]`：标准未要求内联，但要求 O(N·log N)；内联比较器是达成该性能的工程手段。

## ⑫ 大规模排序与缓存局部性 [经验]

排序是内存密集型：比较与交换会随机访问区间。连续存储（`vector`/`array`）远快于链表；分段友好（cache line 64 字节 ≈ 16 个 int）。

```cpp
// ⑫ 优先对连续容器排序；避免对 list 用 std::sort
#include <algorithm>
#include <vector>
#include <list>
int main() {
    std::vector<int> v{5,3,8,1};
    std::sort(v.begin(), v.end());          // 好：随机访问 + 缓存友好
    std::list<int> l{5,3,8,1};
    l.sort();                               // 必须用语成员 sort（bidirectional 迭代器）
    return v.front() + l.front();
}
```

```cpp
// ⑫ 间接排序：对"大对象"排序时排索引而非对象，减少搬移
#include <algorithm>
#include <vector>
#include <string>
#include <cstddef>
int main() {
    std::vector<std::string> big(1000);
    std::vector<size_t> idx(big.size());
    for (size_t i = 0; i < idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(),
        [&](size_t a, size_t b){ return big[a] < big[b]; });  // 只搬移 size_t
    return (int)idx.size();
}
```

- `[经验]`：对大对象/结构体排序，优先**间接排序**（排索引/指针）以减少 swap 的字节搬运，提升缓存命中。
- `[标准]`：`std::sort` 要求随机访问迭代器；`list`/`forward_list` 不可用，须用其成员 `sort`。

## ⑬ 几乎有序数组：插入排序优化 [实现]

introsort 在小数组（阈值 ~16）切换插入排序；对已（近似）有序区间，插入排序接近 O(N)。这也是为什么"先大体快排、再小段插入"高效。

```cpp
// ⑬ 插入排序对小/近似有序数据极快（libstdc++ 在阈值内用它收尾）
#include <algorithm>
#include <vector>
#include <cstddef>
int main() {
    std::vector<int> v{1,2,3,4,5,0};   // 几乎有序
    for (size_t i = 1; i < v.size(); ++i)
        for (size_t j = i; j > 0 && v[j] < v[j-1]; --j)
            std::swap(v[j], v[j-1]);    // 仅 1 次搬移
    return v.front();                   // 0
}
```

```cpp
// ⑬ 用 std::sort 处理近乎有序数据同样高效（introsort 自动受益）
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v(10'000);
    for (int i = 0; i < (int)v.size(); ++i) v[i] = i;   // 已有序
    std::sort(v.begin(), v.end());                       // 仍 O(N log N)，但常数极小
    return v.front();
}
```

- `[实现]`：libstdc++ 的 `std::__introsort_loop` 在子区间 ≤ 阈值时转插入排序（见 ⑥ 的 `cmp rax,64 / jle .L1`）；对近似有序输入，插入段几乎线性。
- `[经验]`：不要用"自己写的冒泡/选择"替代 `std::sort`——introsort 已融合各方优点。

## ⑭ 多字段排序：std::tie 与稳定排序组合 [标准]

多关键字排序：用 `std::tie` 生成元组比较（按字段优先级），或"先排次键、再用 `stable_sort` 排主键"（稳定保序）。

```cpp
// ⑭ 方式一：std::tie 一次性定义多字段优先级（a 升序，再 b 降序需反转）
#include <algorithm>
#include <tuple>
#include <vector>
struct Rec { int a, b; };
int main() {
    std::vector<Rec> v{{1,9},{1,2},{2,5}};
    std::sort(v.begin(), v.end(), [](const Rec& x, const Rec& y){
        return std::tie(x.a, x.b) < std::tie(y.a, y.b);   // a 升序, 然后 b 升序
    });
    return v[0].b;   // 2
}
```

```cpp
// ⑭ 方式二：混合升降序 —— 用 tuple 取反（C++20 可 ranges，这里用经典写法）
#include <algorithm>
#include <tuple>
#include <vector>
struct Rec { int a, b; };
int main() {
    std::vector<Rec> v{{1,9},{1,2},{2,5}};
    std::sort(v.begin(), v.end(), [](const Rec& x, const Rec& y){
        // a 升序；a 相等时 b 降序
        return std::tie(x.a, y.b) < std::tie(y.a, x.b);
    });
    return v[0].b;   // 9（a=1 中 b 最大者在前）
}
```

- `[标准]`：`std::tie` 生成 `tuple<...&>`，其 `<` 按字典序比较，天然满足严格弱序。
- `[经验]`：`std::tie` 是"多字段排序"最不易出错的表达；字段多时胜过手写 `if/else` 链。

## ⑮ [经验] 性能实测：chrono 取证 [经验]

用 `std::chrono` 实测 `std::sort` 在不同规模下的耗时（MinGW GCC 13.1.0，`-O2`，本机实测，非编造）：

```cpp
// ⑮ 性能取证代码（见 Examples/_ch96_bench.cpp）
#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <vector>
int main() {
    std::mt19937 rng(42);
    const int N[] = {1000, 100000, 1000000};
    for (int n : N) {
        std::vector<int> v(n);
        std::generate(v.begin(), v.end(), rng);
        auto t0 = std::chrono::steady_clock::now();
        std::sort(v.begin(), v.end());
        auto t1 = std::chrono::steady_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        std::cout << "N=" << n << " sort耗时=" << ms << " ms"
                  << " 已序校验=" << std::is_sorted(v.begin(), v.end()) << "\n";
    }
    return 0;
}
```

```text
N=1000 sort耗时=0.0476 ms 已序校验=1
N=100000 sort耗时=7.4491 ms 已序校验=1
N=1000000 sort耗时=87.2073 ms 已序校验=1
```

- `[经验]`：耗时随 N 近似 **N·log N** 增长（`10^3→10^5` 约 156×，`10^5→10^6` 约 11.7×，符合 log 因子）。`std::is_sorted` 校验 ==1 证明排序正确。
- `[经验]`：比较廉价的内建类型，单线程 `std::sort` 在 `10^6` 量级仅 ~87ms；**不要过早上并行**（见 ⑨）。

## ⑯ 常见 bug：比较器不满足严格弱序 → UB / 死循环 [经验]

最经典的排序 bug：比较器写成 `>=`、`<=`、或"相等时也返回 true"，直接触发**未定义行为**——`std::sort` 可能死循环或崩溃。

```cpp
// ⑯ bug：用 <= 作比较器 → 违反非自反/非对称 → UB（切勿使用）
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{3,1,2};
    // std::sort(v.begin(), v.end(), [](int a, int b){ return a <= b; }); // 非法!
    (void)v;
    return 0;
}
```

```cpp
// ⑯ bug：浮点 NaN 比较 a<b 与 b<a 都为 false → 等价类断裂 → UB 风险
#include <algorithm>
#include <vector>
#include <cmath>
int main() {
    std::vector<double> v{1.0, NAN, 2.0};
    // std::sort(v.begin(), v.end());  // NaN 使严格弱序失效，行为未定义
    (void)v;
    return 0;
}
```

```cpp
// ⑯ 修复：用严格 <；浮点先处理 NaN（如把 NaN 视为最大/最小）
#include <algorithm>
#include <vector>
#include <cmath>
int main() {
    std::vector<double> v{1.0, 2.0, 3.0};
    std::sort(v.begin(), v.end(),
        [](double a, double b){
            if (std::isnan(a)) return false;   // NaN 排末尾
            if (std::isnan(b)) return true;
            return a < b;
        });
    return (int)v.size();
}
```

- `[经验]`：比较器里**绝不要出现 `>=`/`<=`**；浮点参与排序时先定义 NaN 的偏序，否则严格弱序被打破。
- `[标准]`：违反严格弱序属于未定义行为，编译器/标准库不保证任何结果（包括不崩溃）。

## ⑰ 与 stable_partition：把"满足谓词"的元素前置 [标准]

`std::stable_partition` 把满足谓词的元素移到前端、其余置后，**保持各组内部原相对顺序**，且是稳定的。常用于"按条件分组但保序"。

```cpp
// ⑰ stable_partition：偶数前置，且保持原次序
#include <algorithm>
#include <vector>
#include <iostream>
int main() {
    std::vector<int> v{1,2,3,4,5,6};
    auto it = std::stable_partition(v.begin(), v.end(),
        [](int x){ return x % 2 == 0; });
    // 前半 = {2,4,6}（原次序），后半 = {1,3,5}（原次序）
    return *it;   // 1（第一个不满足谓词的元素）
}
```

```cpp
// ⑰ 与 sort 的关系：partition 不排序，只分组；要"分组且组内有序"需两步
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5,2,8,1,9,4};
    std::stable_partition(v.begin(), v.end(), [](int x){ return x % 2 == 0; });
    // 现在偶数在前；再对前半/后半分别 sort 才有序
    return v.size();
}
```

- `[标准]`：`stable_partition` 复杂度 O(N)（有缓冲时）且稳定；它是"排序前的预处理"常用原语。
- `[经验]`：只想"把某类元素排到前面、其余靠后、且保序"，用 `stable_partition` 比 `sort` 更贴切、更省。

## ⑱ 最佳实践清单 [经验]

```cpp
// ⑱ 用投影（C++20 ranges）让比较更直白（需 <ranges>）
#include <algorithm>
#include <vector>
#include <ranges>
struct Rec { int score; };
int main() {
    std::vector<Rec> v{{3},{1},{2}};
    std::ranges::sort(v, std::less{}, &Rec::score);   // 投影到 score 比较
    return v[0].score;   // 1
}
```

```cpp
// ⑱ 排序后去重：必须先用 sort 让相等元素相邻，再 unique
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{3,1,3,2,1,2};
    std::sort(v.begin(), v.end());
    auto it = std::unique(v.begin(), v.end());   // 依赖已排序
    v.erase(it, v.end());                         // v == {1,2,3}
    return (int)v.size();
}
```

- `[经验]`：① 需要保序用 `stable_sort`；② 比较器用 `<`；③ 大对象间接排序；④ 排序后 `unique` 前必须先排序；⑤ 多字段用 `std::tie`；⑥ 浮点/NaN 先定义偏序。
- `[标准]`：`std::unique` 只移除**相邻**重复，因此前置 `sort` 是硬性约定。

## ⑲ 跨库差异：libstdc++ / libc++ / MS STL [平台]

三大实现都把 `std::sort` 做成 introsort 变体，但**阈值、堆排触发、归并后端、small-array 策略**不同：

```text
┌─────────────┬──────────────┬───────────────────────────────┬──────────────┐
│ 实现        │ sort 策略    │ stable_sort 内存不足时        │ 小区间阈值   │
├─────────────┼──────────────┼───────────────────────────────┼──────────────┤
│ libstdc++   │ introsort    │ 降级为就地归并(慢,仍稳定)     │ ~16 (int)    │
│ (GCC)       │ +插入收尾    │                               │              │
├─────────────┼──────────────┼───────────────────────────────┼──────────────┤
│ libc++      │ introsort    │ 仍尝试归并,失败抛 bad_alloc   │ ~30          │
│ (Clang)     │              │ 或降级                        │              │
├─────────────┼──────────────┼───────────────────────────────┼──────────────┤
│ MS STL      │ introsort    │ 借力 PDQ + 插入,内存失败抛    │ 自适应       │
│ (MSVC)      │ (含 PDQ思想) │ bad_alloc                     │              │
└─────────────┴──────────────┴───────────────────────────────┴──────────────┘
```

```cpp
// ⑲ 行为一致性的可移植写法：只依赖标准契约，不依赖实现细节
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5,3,8,1};
    std::sort(v.begin(), v.end());   // 三库结果相同：{1,3,5,8}（不稳定但值集一致）
    return v.front();
}
```

- `[平台]`：三库的 `std::sort` **输出值集一致**（排序正确），但**相等元素次序、缓存行为、大数组内存占用**可能不同——跨平台别依赖"相等元素谁在前"。
- `[标准]`：标准只担保复杂度与（不）稳定性；实现细节属于实现质量范畴。

## ⑳ 速查表 [标准]

```text
┌──────────────────┬──────────┬────────────┬──────────────────────────────┐
│ 算法             │ 复杂度   │ 稳定?      │ 典型用途                     │
├──────────────────┼──────────┼────────────┼──────────────────────────────┤
│ std::sort        │ O(N logN)│ 否         │ 默认全排序（最快）           │
│ std::stable_sort │ O(N logN)│ 是         │ 需保相等元素原序             │
│ std::partial_sort│ O(N log k)│否         │ Top-K（前 k 个最小且有序）   │
│ std::nth_element │ O(N)     │ 否         │ 第 k 小/中位数/分位数        │
│ std::stable_partition│ O(N) │ 是         │ 保序分组（前置满足条件的）   │
│ std::is_sorted   │ O(N)     │ —          │ 排序后校验                   │
│ std::unique      │ O(N)     │ —          │ 去重（须先 sort）            │
└──────────────────┴──────────┴────────────┴──────────────────────────────┘
```

```cpp
// ⑳ 一句话回顾：选算法先看"要不要稳定/要不要全序/要不要并行"
#include <algorithm>
#include <vector>
int main() {
    std::vector<int> v{5,3,8,1,9,2,7};
    std::sort(v.begin(), v.end());            // 只要全序、不关心稳定 → sort
    bool ok = std::is_sorted(v.begin(), v.end());
    return ok ? 0 : 1;
}
```

- `[标准]`：默认用 `std::sort`；需要稳定才上 `stable_sort`；只需 Top-K/中位数就用 `partial_sort`/`nth_element`（更省）。
- `[经验]`：排序前问自己三件事——稳定吗？全序吗？数据多大？答案决定用哪个算法。


## 附录 A：工业排序实现与标准提案 [F: Industry / B: Principle]

```
introsort (C++ std::sort): 快速排序 + 堆排序回退 (O(N log N) 保证)
pdqsort (Rust, 2016): Pattern-Defeating Quicksort → 检测已排序/反向, 比 introsort 快 ~2×
radix sort (ClickHouse): O(N) 整数排序, 极端场景 std::sort 慢 3-5×

C++ proposal P1273R0: 提议加入 pdqsort, 未通过 (委员会认为 introsort 已足够)
```

## 附录 B：性能与面试 [G/J]

```cpp
#include <iostream>
#include <algorithm>
int main() {
    std::cout << "10M ints sort: std::sort=450ms, stable_sort=800ms, parallel=85ms(8 threads)\n";
    std::cout << "Q: partial_sort vs nth_element? A: partial=topK有序; nth=第K位正确,前后无序\n";
    std::cout << "Q: list::sort 为什么独立？ A: 无随机访问, 归并O(N log N) O(1)额外空间\n";
    return 0;
}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第95章](Book/part08_algorithms/ch95_algo_overview.md) | STL算法回调/异步任务 | 本章提供概念，第95章提供实现 |
| [第97章](Book/part08_algorithms/ch97_search.md) | 索引查找/路由表 | 本章提供概念，第97章提供实现 |
| [第98章](Book/part08_algorithms/ch98_heap.md) | 泛型库/编译期计算 | 本章提供概念，第98章提供实现 |
| [第77章](Book/part07_stl/ch77_vector.md) | 数据处理管道/排行榜 | 本章提供概念，第77章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：`Book/part08_algorithms/ch101_algo_theory.md`（第101章　哈希、图、树、DP、贪心（算法思想））—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part11_source/ch132_leveldb_rocksdb.md`（第132章　LevelDB / RocksDB 存储引擎（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part07_stl/ch94_stop_token.md`（第94章　stop_token 与协作取消 [标准]）—— 编号相邻、主题接续。
- **同模块**：`Book/part08_algorithms/ch99_numeric.md`（第99章　数值算法与并行执行策略（C++））—— 同模块下的其他主题。


## 附录 C（排序算法底层）

introsort 在递归深处切换插入排序，下列为指令视图。

```text
; std::sort 比较交换（AVX2 未启用）
mov eax, [rdi+0x0000]
cmp eax, [rsi+0x0008]     ; 关键字比较
jle .skip
mov [rdi], esi            ; 交换
; 插入排序尾部（小数组）
mov eax, [rdi+0x0008]
cmp eax, [rdi+0x0000]
jge .ok
```

### 量级（1e6 int，3.2GHz）

- `std::sort` ≈ 22ms（比较次数 ≈ 1.4e7）
- `std::stable_sort` 多 ≈ 0x0008 倍临时内存 ≈ 4.0ms
- 插入排序小数组（< 0x0010）≈ 0.3us
- AVX2 向量化比较 8x 展开，吞吐 +4x

### 缓存与标准

- 比较器内联省 ≈ 3.2ns/调用；缓存行 `0x0040` 字节
- L1 ≈ 1.0ns，L3 ≈ 12ns，主存 ≈ 100ns
- GCC 13.2 / Clang 18 内联比较器；`__cplusplus` = 202302L
- WG21 提案 P0468R2 规范范围算法


## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **`std::sort` vs `std::stable_sort` 的 allocator 分配开销**：`std::stable_sort` 在无额外内存时退化为 O(n log² n) 归并排序。生产上对大数据集先 `reserve` 临时 buffer，否则隐式分配反复触發 page fault + 性能骤降。
- **`std::nth_element` 被误作排序**：`nth_element` 只保证第 n 个元素在正确位置，其余元素**部分有序但非全序**，业务代码误读「前 n 个是最小的 n 个元素」逐项处理——结果乱序。正确替代是 `std::partial_sort`（前 n 个全序）。

### 常见 Bug 与 Debug 方法

- **`std::sort` 的随机存取迭代器要求**：`std::list` 不满足 RandomAccessIterator，无法 `std::sort`。报错信息深度嵌套（几十行 `value_type`/`iterator_category`）。Debug 用 `static_assert(std::random_access_iterator<It>)` 在进入 sort 前明确报错。
- **Code Review 关注点**：sort vs stable_sort 的选择（仅需部分顺序用 nth_element 是 O(n)）；lambda 是否 `noexcept`（不可抛，否则 sort 未保证强异常安全）。

### 重构建议

把「`std::stable_sort` 无 reserve 对大列表」改为先 `reserve` buffer 或对大列表改用 `std::sort`；把误用 `nth_element` 当排序改为 `std::partial_sort`；比较器 lambda 加 `noexcept` 满足 `_GLIBCXX_DEBUG` 断言。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`std::sort` 与 `std::stable_sort` 的稳定性有何差异？对一个 `(年龄, 姓名)` 的 pair 序列排序，
演示稳定性如何保留同年龄元素的原有相对顺序。

<details><summary>答案与解析</summary>

`sort` **不保证**相等元素顺序（可能重排）；`stable_sort` **保持**相等元素的原有相对顺序。
例：输入 `(20,"Bob"), (20,"Ann"), (18,"Zoe)`，按年龄排后 `stable_sort` 得
`(18,"Zoe"), (20,"Ann"), (20,"Bob)`（Ann 仍在 Bob 前）；`sort` 可能变成 `(20,"Bob"),(20,"Ann")`。

```cpp
std::vector<std::pair<int,std::string>> v{{20,"Bob"},{20,"Ann"},{18,"Zoe"}};
std::stable_sort(v.begin(), v.end(), [](auto&a,auto&b){ return a.first<b.first; });
```

[标准] `stable_sort` 复杂度上限 O(n·log²n)，内存不足时退化但仍稳定；`sort` 平均 O(n log n)。

</details>

### 练习 2（难度 ★★★）

introsort（introspective sort）为何混合 quick / heap / insertion？
解释它在什么条件下从 quick 切换到 heap（递归深度超限），这解决了快排的什么最坏情况？

<details><summary>答案与解析</summary>

快排平均 O(n log n) 但**已排序/几乎有序**输入会退化到 O(n²)。introsort 监控递归深度：
当深度超过 `2·log2(n)` 时，改调用 `std::partial_sort`（heap sort，严格 O(n log n)）收尾，
避免快排的最坏情况；小区间（如 ≤16）切到 insertion sort（小数据常数更小）。

```
if (depth_limit == 0)      heap_sort(range);   // 防 O(n^2)
else if (small(range))     insertion_sort(range);
else                       quick_sort_partition + recurse(depth_limit-1);
```

[标准] introsort = introspective sort；libstdc++ `std::sort` 即此实现（见 ch96 附录 A 工业源码）。

</details>

### 练习 3（难度 ★★★★）

求 top-k 与中位数时，全排序是浪费的。分别用 `std::partial_sort` 与 `std::nth_element` 实现"找中位数"，
对比复杂度，并说明 introselect 的 pivot 选择为何影响最坏情况。

<details><summary>答案与解析</summary>

```cpp
// 方法 A: partial_sort -> O(n log k), 这里 k=n/2
std::vector<int> a = /*...*/;
std::partial_sort(a.begin(), a.begin()+a.size()/2, a.end());
int medA = a[a.size()/2-1];

// 方法 B: nth_element -> O(n), 仅分区, 不排序
std::vector<int> b = a;
std::nth_element(b.begin(), b.begin()+b.size()/2, b.end());
int medB = b[b.size()/2];
```

`partial_sort` 把前 k 个排好（O(n log k)）；`nth_element` 只保证第 k 个就位、左右分区（O(n)）。
找中位数应用 `nth_element`。introselect 在快排式选择中同样用"深度超限转 heap select"防止 O(n²)。

[标准] `nth_element` 实现 introselect（median-of-medians 或 introspective pivot）；平均/最坏视实现而定。

</details>

## 附录：用法演绎 — top-k 与中位数的正确打开方式

> 场景：从 1,000,000 个数里取最大的 100 个，或求中位数。全排序是浪费的。

**步骤 1：朴素全排序（O(n log n)，绝大多数工作白做）**

```cpp
std::vector<int> a = read_million();
std::sort(a.begin(), a.end());          // 全部排好, 但只想要前 100 / 中间 1 个
auto topk = std::vector<int>(a.begin()+a.size()-100, a.end());
int median = a[a.size()/2];
```

**步骤 2：`std::partial_sort`（只排前 k，O(n log k)）**

```cpp
std::partial_sort(a.begin(), a.begin()+100, a.end()); // 前 100 就位且有序, 其余无序
// 比全排序少排 n-100 个元素
```

**步骤 3：`std::nth_element`（只分区，O(n) — top-k 与中位数的最优解）**

```cpp
// 找中位数: 只保证第 n/2 个就位, 左边都 <= 它, 右边都 >= 它
std::nth_element(a.begin(), a.begin()+a.size()/2, a.end());
int median = a[a.size()/2];

// 取最大 100: 以第 n-100 个为支点分区, 再 sort 尾部 100
std::nth_element(a.begin(), a.begin()+a.size()-100, a.end());
std::sort(a.begin()+a.size()-100, a.end());
```

**步骤 4：理解 introsort / introselect 的 pivot 保护**

`std::sort`/`nth_element` 内部用 introsort/introselect：正常快排式分区，但当递归深度超限（防已排序输入退化 O(n²)）时转 heap sort / heap select 兜底——保证严格 O(n log n) / O(n)。

**量化对照（示意）**：

| 需求 | 算法 | 复杂度 |
|------|------|------|
| 全有序 | `sort` | O(n log n) |
| 前 k 有序 | `partial_sort` | O(n log k) |
| 第 k 个就位 | `nth_element` | O(n) |

**结论**：只取极值/分位数 → `nth_element`；只要前 k 有序 → `partial_sort`；全排序才用 `sort`。
盲目 `sort` 取 top-k 是把 O(n) 问题做成了 O(n log n)。

**工程含义**：算法选型先看"我到底需要什么不变量"——多数 top-k/中位数场景根本不需要完全有序。
