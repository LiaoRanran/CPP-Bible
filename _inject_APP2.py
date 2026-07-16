# -*- coding: utf-8 -*-
"""Phase APP Batch2: rewrite off-topic template exercises -> topic-aligned ladders,
and append a '## 附录：用法演绎' step-by-step scenario to 8 chapters.
CRLF-safe.

Two modes per file:
  - simple  : '## 自测练习' is the last section -> replace anchor..EOF with (exercises + demo)
  - preserve: a '## ' section follows the exercises anchor (ch42 附录E / ch50 [实现] ASM)
              -> replace ONLY the exercises block (anchor..next '## '-1), then append demo at true EOF
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# key -> (path, mode)
TARGETS = {
    "ch21": ("Book/part03_language/ch21_const_family.md",    "simple"),
    "ch31": ("Book/part03_language/ch31_operator_overloading.md", "simple"),
    "ch39": ("Book/part04_memory/ch39_raii_rule.md",         "simple"),
    "ch42": ("Book/part04_memory/ch42_strict_aliasing.md",   "preserve"),
    "ch43": ("Book/part04_memory/ch43_cache_locality.md",    "simple"),
    "ch44": ("Book/part04_memory/ch44_memory_pool.md",       "simple"),
    "ch50": ("Book/part05_oo/ch50_multiple_inheritance.md",  "preserve"),
    "ch51": ("Book/part05_oo/ch51_crtp.md",                  "simple"),
}

EXERCISES = {
"ch21": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

为 `class Buffer { std::vector<int> v; };` 提供 const 与非 const 两个 `at(size_t)` 重载，
演示 `const Buffer` 只能调用 const 版本、`Buffer` 可调用两者；并指出 `mutable` 字段的合法用途。

<details><summary>答案与解析</summary>

```cpp
#include <vector>
struct Buffer {
    std::vector<int> v;
    int& at(size_t i)             { return v.at(i); }       // 非 const: 可修改
    const int& at(size_t i) const { return v.at(i); }       // const: 只读
};
int main(){
    Buffer b; b.v = {1,2,3};
    b.at(0) = 10;                      // 调用非 const 版本
    const Buffer cb = b;
    int x = cb.at(1);                  // 只能调用 const 版本
    // cb.at(0) = 5;                   // 编译失败: const 对象不可调非 const 成员
}
```

`mutable` 用于"逻辑 const"：对象对外表现为只读，但内部缓存/计数可改。例如
`mutable std::size_t cached_hash = 0;` 在 `hash() const` 中惰性计算。

[标准] const 成员函数承诺不修改对象的可观察状态；`mutable` 允许豁免特定子对象。

</details>

### 练习 2（难度 ★★★）

`constexpr` 与 `const` 有何本质区别？写 `constexpr int sq(int x){ return x*x; }`，
分别展示它在**编译期**（`static_assert`）与**运行期**（`rand()` 作实参）两种上下文求值；
再对比 `const int k = rand();`（只读但非编译期常量）。

<details><summary>答案与解析</summary>

```cpp
#include <cstdlib>
constexpr int sq(int x){ return x*x; }
static_assert(sq(5) == 25);                 // 编译期求值: 不占运行时指令
int main(){
    int y = sq(std::rand());                // 运行期求值: 退化为普通函数调用
    const int k = std::rand();              // 只读变量, 但值在运行期才确定
    // static_assert(k == 0);               // 编译失败: k 不是常量表达式
}
```

`const` 只保证"不可改"，`constexpr` 保证"值可在编译期确定"。`sq` 因 `constexpr` 两用：
参数是常量表达式时在编译期算、是运行期值在运行期算。`k` 虽 `const` 但依赖 `rand()`，不是常量表达式。

[标准] `constexpr` 函数/变量要求在合法常量表达式上下文中于翻译期求值；`const` 仅去除了可修改性。

</details>

### 练习 3（难度 ★★★★）

C++20 的 `constinit` 与 `consteval` 各自解决什么问题？
写 `constinit static int g = 42;` 说明它如何消除"静态初始化顺序灾难"；
写 `consteval int cube(int x){ return x*x*x; }` 说明它为何强制编译期求值（`cube(std::rand())` 会编译失败）。

<details><summary>答案与解析</summary>

```cpp
#include <cstdlib>
constinit static int g = 42;          // 编译期完成初始化, 零运行时开销, 无 SIOF
consteval int cube(int x){ return x*x*x; }   // 必须编译期求值
int main(){
    constexpr int c = cube(3);        // OK: 编译期 27
    // int bad = cube(std::rand());    // 编译失败: consteval 拒绝运行期参数
}
```

- `constinit`：要求静态存储期对象的初始化是常量表达式 → 在静态初始化阶段完成，
  避免跨 TU 初始化顺序不确定（Static Initialization Order Fiasco）。
- `consteval`：比 `constexpr` 更强——函数**只能**在编译期调用，`cube(rand())` 直接拒绝。
  适合元编程/代码生成（如编译期计算查表）。

[标准] `constinit`(C++20) 约束初始化为常量表达式；`consteval`(C++20) 定义"立即函数"，仅编译期可调用。

</details>
''',

"ch31": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

为 `class Vec2 { double x, y; };` 重载 `operator+`（成员或自由函数）与 `operator<<`
（自由函数，返回 `std::ostream&`）。指出 `+` 应返回**新对象**（值）而非引用。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
struct Vec2 {
    double x, y;
    Vec2 operator+(const Vec2& o) const { return {x+o.x, y+o.y}; }  // 返回新对象
};
std::ostream& operator<<(std::ostream& os, const Vec2& v){
    return os << '(' << v.x << ',' << v.y << ')';
}
int main(){
    Vec2 a{1,2}, b{3,4};
    std::cout << (a + b) << '\n';   // (4,6)
}
```

`operator+` 返回值是必然的：`a+b` 的结果是个临时量，不能返回对局部/参数的引用。
`operator<<` 返回 `ostream&` 以支持链式 `cout << a << b`。

[标准] 算术运算符通常返回新值（值语义）；流插入运算符返回流引用以支持链式调用。

</details>

### 练习 2（难度 ★★★）

用 C++20 三路比较 `operator<=>` 替代手写 `==`/`<`/`>` 全套：写 `struct Point{ int x,y; auto operator<=>(const Point&) const = default; };`，
解释编译器如何自动生成全部 6 个比较运算符，并说明返回类型 `std::strong_ordering` 的含义。

<details><summary>答案与解析</summary>

```cpp
#include <compare>
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;   // 生成 == < > <= >= !=
};
int main(){
    Point a{1,2}, b{1,3};
    bool t1 = (a == b);   // false
    bool t2 = (a <  b);   // true
    bool t3 = (a != b);   // true (由 == 自动取反)
}
```

`= default` 的 `<=>` 对成员按声明顺序逐字段比较，并自动合成 `==` 等全套。
`strong_ordering` 表示"相等可判定且不等时严格有序"（成员须完全有序，含 `int`）。
若含 `float` 这类只有偏序的类型，需 `partial_ordering` 并谨慎处理 NaN。

[标准] `operator<=>`(C++20) 生成全套比较；`default` 合成逐成员字典序比较。

</details>

### 练习 3（难度 ★★★★）

实现一个管理 `double* data` 的 `Matrix`，先写 **rule of 3**（拷贝构造/拷贝赋值/析构，深拷贝），
再升级到 **rule of 5**（加 `noexcept` 移动构造/移动赋值），并说明为何移动操作应标 `noexcept`——
否则 `std::vector` 扩容时会因"移动可能抛异常"而退化为拷贝。

<details><summary>答案与解析</summary>

```cpp
#include <utility>
#include <cstddef>
struct Matrix {                 // rule of 5
    size_t n; double* data;
    Matrix(size_t n): n(n), data(new double[n*n]) {}
    ~Matrix(){ delete[] data; }
    Matrix(const Matrix& o): n(o.n), data(new double[n*n]) {     // 拷贝构造
        for (size_t i=0;i<n*n;++i) data[i]=o.data[i];
    }
    Matrix& operator=(const Matrix& o){                         // 拷贝赋值
        if (this!=&o){ double* p=new double[o.n*o.n]; /*...*/ delete[] data; data=p; n=o.n; }
        return *this;
    }
    Matrix(Matrix&& o) noexcept : n(o.n), data(o.data) { o.data=nullptr; }   // 移动构造
    Matrix& operator=(Matrix&& o) noexcept {                    // 移动赋值
        if (this!=&o){ delete[] data; data=o.data; n=o.n; o.data=nullptr; }
        return *this;
    }
};
```

`std::vector` 扩容时若元素的移动构造**不** `noexcept`，为保证强异常安全它会改用拷贝；
标 `noexcept` 后扩容走移动（O(1) 指针交换，零元素拷贝）。

[标准] rule of 0/3/5：有自定义析构/拷贝通常需补齐全套；移动操作标 `noexcept` 方能参与 vector 扩容优化。

</details>
''',

"ch39": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 RAII 包装一个必须配对调用的资源（`open()`/`close()`，如 `std::FILE*`）：
写 `struct FileGuard` 在析构中 `fclose`，演示函数中途 `throw` 仍会关闭文件；对比裸 `open/close` 在异常路径泄漏。

<details><summary>答案与解析</summary>

```cpp
#include <cstdio>
#include <stdexcept>
struct FileGuard {
    std::FILE* f;
    FileGuard(const char* p){ f = std::fopen(p,"w"); if(!f) throw std::runtime_error("open"); }
    ~FileGuard(){ if(f) std::fclose(f); }     // 无论正常返回还是异常, 都关闭
};
void use(){
    FileGuard g("log.txt");
    // ... 若此处 throw, 栈展开会调用 ~FileGuard -> fclose, 无泄漏
}
```

裸写法：`fopen` 后某步 `throw`，跳过 `fclose` → 句柄泄漏。RAII 把"释放"绑定到作用域退出。

[标准] RAII：资源获取即初始化，释放绑定到对象析构；异常安全的核心是析构兜底。

</details>

### 练习 2（难度 ★★★）

实现 C++ 风格 `ScopeGuard`：支持 `auto g = scope_guard([&]{ cleanup(); });`，
作用域结束（正常或异常）自动执行。说明它与"析构兜底"是同一机制，并指出异常安全保证级别。

<details><summary>答案与解析</summary>

```cpp
#include <utility>
template <class F>
struct ScopeGuard { F f; bool active = true;
    explicit ScopeGuard(F fn): f(std::move(fn)) {}
    ~ScopeGuard(){ if(active) f(); }
    void dismiss(){ active = false; }
};
template <class F> ScopeGuard<F> scope_guard(F f){ return ScopeGuard<F>(std::move(f)); }
// 用法:
// auto g = scope_guard([&]{ unlock(m); });   // 离开作用域必解锁
```

`ScopeGuard` 本质是一个一次性 RAII 对象，把"清理动作"存为可调用对象。
它提供 **basic 异常安全保证**：即使后续抛异常，已注册的清理仍执行，资源不泄漏。
`dismiss()` 用于"成功路径上不再需要清理"时取消。

[标准] ScopeGuard 是 RAII 的通用化形态；用 lambda 表达任意清理动作；属 basic 保证。

</details>

### 练习 3（难度 ★★★★）

解释异常安全三保证（noexcept / basic / strong），并用 **copy-and-swap** 实现 `StrongArray::operator=` 的强保证：
先拷贝右边到临时量，再与当前对象无抛出地交换；若拷贝阶段抛异常，左边对象原状不变。

<details><summary>答案与解析</summary>

```cpp
#include <utility>
#include <vector>
struct StrongArray {
    std::vector<int> v;
    StrongArray& operator=(const StrongArray& o){
        StrongArray tmp(o);        // 拷贝可能抛, 但只影响 tmp, *this 不动
        std::swap(v, tmp.v);       // 交换不抛 -> 提交
        return *this;              // tmp 析构释放旧资源
    }
};
```

- **noexcept**：承诺绝不抛（如析构、移动构造）。
- **basic**：异常后对象仍有效、无泄漏（但不保证值不变）。
- **strong**：异常后对象**状态完全不变**（事务语义，如 `push_back` 扩容失败回滚）。
copy-and-swap 把"可能失败的工作"放在临时对象上，最后一步 `swap` 不抛，从而获得强保证。

[标准] 强异常安全 = 失败如未调用；copy-and-swap 经典实现；swap 必须 noexcept。

</details>
''',

"ch42": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`float f = 1.0f; int bits = *reinterpret_cast<int*>(&f);` 为何是未定义行为？
给出两种**合法**的位模式重解释方式，并指出严格别名规则的核心约束。

<details><summary>答案与解析</summary>

```cpp
#include <cstring>
#include <bit>
int main(){
    float f = 1.0f;
    // 非法: float* 与 int* 是不同类型, 编译器假定它们不别名 -> UB
    // int bits = *reinterpret_cast<int*>(&f);
    int bits1; std::memcpy(&bits1, &f, sizeof(bits1));   // 合法: 重解释对象表示
    int bits2 = std::bit_cast<int>(f);                   // 合法(C++20): 编译期友好
    (void)bits1; (void)bits2;
}
```

严格别名规则：通过与该对象动态类型不"相似"的指针类型写/读内存是 UB。合法重解释只有
`memcpy` 与 `std::bit_cast`（以及 `char*`/`std::byte*` 字节遍历，见习题 2）。

[标准] 严格别名（[basic.lval]）：仅限动态类型或"相似类型"访问；`memcpy`/`bit_cast` 是豁免通道。

</details>

### 练习 2（难度 ★★★）

`char*` / `std::byte*` 是标准豁免的"万能别名"。写一泛型 `serialize(const T&)` 用 `std::byte*` 逐字节写出任意对象，
解释为何它合法、而 `reinterpret_cast<T*>` 不合法。

<details><summary>答案与解析</summary>

```cpp
#include <cstddef>
#include <iostream>
template <class T>
void dump_bytes(const T& obj){
    auto p = reinterpret_cast<const std::byte*>(&obj);   // byte* 可别名任意类型 (合法豁免)
    for (std::size_t i = 0; i < sizeof(T); ++i)
        std::cout << static_cast<int>(p[i]) << ' ';
}
```

`char`/`signed char`/`unsigned char`/`std::byte` 被标准明确允许访问**任何**对象的字节表示，
因此用它们遍历对象是合法的；但把对象地址 `reinterpret_cast` 成**其它具体类型**的指针去读就违反严格别名。
这正是序列化、哈希、内存比较的标准做法。

[标准] `char`/`std::byte` 系列是"通用别名"类型；其余类型间的 reinterpret 跨类型访问触发 UB。

</details>

### 练习 3（难度 ★★★★）

`__restrict`（GCC/Clang）是给编译器的"不别名"契约。写 `void axpy(int n, double* __restrict y,
const double* __restrict a, const double* __restrict x, double c)`，说明它如何让编译器向量化
（不必每次从内存重载 `a[i]`/`x[i]`），对比不标 `__restrict` 时编译器必须保守重载。

<details><summary>答案与解析</summary>

```cpp
void axpy(int n, double* __restrict y,
          const double* __restrict a, const double* __restrict x, double c){
    for (int i = 0; i < n; ++i) y[i] = a[i] + c * x[i];   // 编译器可假定 a/x/y 互不重叠 -> 向量化
}
```

不标 `__restrict` 时，编译器怕 `a` 与 `y` 指向重叠内存（如 `axpy(n, y, y, x, c)`），
被迫每次循环都从内存重读 `a[i]`（不能缓存到寄存器），无法安全向量化。
`__restrict` 是**程序员对优化器的承诺**（非运行时检查）：承诺这些指针不别名，换来计算器级别的向量化收益。
见本章「附录 E」真实汇编对比。

[标准] `__restrict` 向编译器声明指针不别名；违反承诺是 UB，但收益是解除向量化阻碍。

</details>
''',

"ch43": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`int m[1000][1000];` 行优先（C 风格）遍历 `m[i][j]` 与列优先遍历 `m[j][i]`，哪个缓存更友好？
写出两种遍历并说明 cache miss 次数差异。

<details><summary>答案与解析</summary>

```cpp
int main(){
    static int m[256][256]{};   // static 避免栈溢出; 教学只关心遍历顺序
    long sum = 0;
    // 行优先: 内存连续访问 -> 每次缓存行加载后顺序命中
    for (int i=0;i<256;++i) for (int j=0;j<256;++j) sum += m[i][j];   // 友好
    // 列优先: 每次跨 256*4B 跳行 -> 几乎每次都 cache miss
    for (int j=0;j<256;++j) for (int i=0;i<256;++i) sum += m[i][j];   // 不友好
    (void)sum;
}
```

C/C++ 多维数组按行优先（row-major）存储：`m[i][j]` 与 `m[i][j+1]` 相邻。
行优先遍历顺序命中缓存行（一次加载 64B ≈ 16 个 int）；列优先每次都跳到新缓存行，
cache miss 数量级差约 16×，实测可慢一个数量级。

[标准] 数组行优先存储；访问模式应顺应内存布局以利用空间局部性。

</details>

### 练习 2（难度 ★★★）

两个线程各写一个 `struct { long a; long b; }` 的**不同**字段却互相拖慢——这是 false sharing。
给出用 `alignas(64)` / padding 修复的写法，并解释缓存行为何失效。

<details><summary>答案与解析</summary>

```cpp
// 错误: a 与 b 可能落在同一缓存行(64B), 两线程写不同字段仍互相使对方缓存行失效
struct Bad { long a; long b; };
// 修复: 把每个字段推到独立缓存行
struct Aligned { alignas(64) long a; alignas(64) long b; };
```

现代 CPU 以缓存行（常 64B）为单位在核间迁移。即便 `a`/`b` 是不同字段，只要同处一行，
线程 1 写 `a` 会使该行在另一核的副本失效，线程 2 写 `b` 又失效回来 → 行在核间乒乓。
`alignas(64)` 让 `a`/`b` 各自独占一行，消除伪共享。

[标准] false sharing：不同变量共享缓存行导致核间无效化；`alignas(缓存行)` 隔离解决。

</details>

### 练习 3（难度 ★★★★）

对比 AOS（Array of Structs）与 SOA（Structure of Arrays）在仅使用部分字段时的缓存与 SIMD 友好度：
`struct P { float x,y,vx,vy; } ps[N];` vs `struct { float x[N],y[N],vx[N],vy[N]; } soa;`，
写 `update()` 只改 `x += vx`，指出 SOA 为何对 SIMD 更友好。

<details><summary>答案与解析</summary>

```cpp
struct P { float x,y,vx,vy; } ps[1024];
void update_aos(){ for (auto& p: ps) p.x += p.vx; }   // 每读 16B 只用 8B, 浪费一半带宽
struct Soa { float x[1024],y[1024],vx[1024],vy[1024]; } s;
void update_soa(){ for (int i=0;i<1024;++i) s.x[i] += s.vx[i]; }  // x/vx 连续, 单指令处理 4/8 个
```

AOS 把 `x,y,vx,vy` 交错存储，`update` 只碰 `x`/`vx` 却要把整个 struct 拉进缓存（带宽浪费）。
SOA 把同类字段聚到一起，`x[]` 与 `vx[]` 连续，SIMD 一条指令可并行处理 4 个（float×4）或 8 个（AVX）
元素，且缓存只装需要的字段。代价：SOA 的"结构体语义"被拆散，代码可读性下降。

[标准] SOA 提升数据局部性与 SIMD 利用率，以结构可读性换取吞吐；常用于粒子/数值热点。

</details>
''',

"ch44": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写固定大小内存池 `FixedPool<Block, N>`：预分配 `N` 个 `Block`，分配时从空闲链表取一块、释放时归还。
对比每次 `new Block` 走通用分配器的系统调用开销。

<details><summary>答案与解析</summary>

```cpp
#include <cstddef>
template <class Block, std::size_t N>
struct FixedPool {
    alignas(Block) char buf[N * sizeof(Block)];   // 预分配一大块
    void* free_list[N]; std::size_t head = 0;
    FixedPool(){ for (std::size_t i=0;i<N;++i) free_list[i] = buf + i*sizeof(Block); head = N; }
    void* alloc(){ return head ? free_list[--head] : nullptr; }   // O(1) 无系统调用
    void dealloc(void* p){ free_list[head++] = p; }               // O(1) 归还
};
```

每次 `new` 要进通用分配器（可能加锁、查找空闲块、系统调用 `sbrk`/`mmap`）。
固定池的 `alloc`/`dealloc` 只是数组下标操作，**确定性的 O(1)、零系统调用**，适合高频小对象。

[标准] 固定块池用空闲链表消除通用分配器开销；代价是块大小固定、总量预分配。

</details>

### 练习 2（难度 ★★★）

把自定义池接入 STL 容器：用 `std::pmr::memory_resource` 派生一个池资源，
让 `std::pmr::vector<int>` 从池分配（零系统调用、确定性延迟）。写出关键步骤。

<details><summary>答案与解析</summary>

```cpp
#include <memory_resource>
#include <vector>
struct PoolResource : std::pmr::memory_resource {
    void* do_allocate(std::size_t b, std::size_t a) override { return ::operator new(b); } // 接你的池
    void  do_deallocate(void* p, std::size_t, std::size_t) override { ::operator delete(p); }
    bool  do_is_equal(const memory_resource& o) const noexcept override { return this==&o; }
};
// 用法:
PoolResource pool;
std::pmr::vector<int> v{&pool};   // vector 的内存全部来自 pool
```

`std::pmr` 把"分配器"抽象成运行期多态的 `memory_resource`，容器持有指针即可换源。
把 `do_allocate` 换成你的池后，`vector` 扩容不再触碰系统分配器，延迟确定、可预测——
这正是嵌入式/实时系统的诉求（见 ch122 pmr 实证）。

[标准] `std::pmr`(C++17) 运行期多态分配器；`memory_resource` 派生即可替换容器内存来源。

</details>

### 练习 3（难度 ★★★★）

对比池分配器与通用分配器的**碎片**问题：长期运行下通用 `new/delete` 产生外部碎片
（嵌入式 OOM 风险），池分配器固定块无外部碎片但存在内部碎片（块比对象大即浪费）。
给出选型准则。

<details><summary>答案与解析</summary>

```cpp
// 通用分配器: 任意大小混合分配/释放 -> 空闲块被切碎 -> 外部碎片
// 长期运行后: 总空闲内存足够, 但无单块够大 -> 分配失败 (嵌入式致命)
// 池分配器: 只服务一种固定块 -> 无外部碎片, 但 block 比对象大则内碎片
```

- **外部碎片**：空闲内存总量足、但无连续大块可用 → 分配失败。通用分配器长期运行必现。
- **内部碎片**：池的块大小 > 实际对象 → 每块尾部浪费。
选型：实时/确定性/长生命周期、对象大小固定 → **池**（无外部碎片、延迟确定）；
通用、大小多变、短生命周期 → 系统分配器（灵活）。可在同一程序按对象类别混用。

[标准] 池消除外部碎片换内部碎片；实时系统优先确定性而非峰值利用率。

</details>
''',

"ch50": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写非虚 MI：`struct A{int a;}; struct B:A{}; struct C:A{};`（注意非虚）与 `struct D:B,C{};`。
演示 `D` 含**两份** `A` 子对象，`d.B::a` 与 `d.C::a` 是不同成员；指出 `D*` 转 `B*`/`C*` 需要指针调整。

<details><summary>答案与解析</summary>

```cpp
struct A { int a; };
struct B : A {};
struct C : A {};
struct D : B, C {};             // 非虚: A 被继承两次
int main(){
    D d;
    d.B::a = 1; d.C::a = 2;     // 两份 a, 必须消歧
    // d.a = 3;                  // 编译失败: a 有二义性
    B* pb = &d;                 // 指针需调整指向 B 子对象(= &d)
    C* pc = &d;                 // 指针需调整指向 C 子对象(= &d + sizeof(B))
}
```

非虚 MI 下每个派生路径都复制一份基类子对象，`D` 实际含两个 `A`。`&d` 到 `pc` 的转型
要加上 `B` 子对象的大小偏移——这就是 this 调整（this-adjustment）。

[标准] 非虚 MI 复制每个基类子对象；跨子对象指针转型需偏移调整（thunk）。

</details>

### 练习 2（难度 ★★★）

菱形 `A<-B, A<-C, D:B,C` 但**不**用 virtual 继承时，`D d; d.a = 1;` 为何编译失败（二义性）？
如何用 `d.B::a = 1` 消歧义，又为何这会造成"数据重复"问题。

<details><summary>答案与解析</summary>

```cpp
struct A { int a; };
struct B : A {};
struct C : A {};
struct D : B, C {};            // 两份 A
int main(){
    D d;
    // d.a = 1;                  // 二义性: 不知改哪份
    d.B::a = 1;                 // 消歧: 只改 B 路径那份
    d.C::a = 2;                 // C 路径那份仍是 2 -> 同一"概念实体"出现两份值
}
```

消歧义能编译，但语义上"对象只有一个 `a`"的设想被破坏：`d.B::a` 与 `d.C::a` 是两份独立存储。
若 `A` 代表共享状态（如"身份 ID"），两份就错了。

[标准] 二义性源于重复基类子对象；显式消歧不解决"数据重复"的本质问题。

</details>

### 练习 3（难度 ★★★★）

用 **virtual 继承** 解决二义性：`struct B:virtual A{}; struct C:virtual A{}; struct D:B,C{};`
此时 `d.a` 无歧义（只有一份 `A`）。指出代价：this 调整 thunk + vbtable 间接访问（见本章「[实现]」汇编）。

<details><summary>答案与解析</summary>

```cpp
struct A { int a; };
struct B : virtual A {};
struct C : virtual A {};
struct D : B, C {};            // 共享同一份虚基类 A
int main(){
    D d;
    d.a = 1;                   // 无歧义: 只有一份 A
    A* pa = &d;                // 指向共享虚基类子对象
}
```

代价：虚基类的偏移**运行时**才能确定（取决于完整对象布局），访问 `a` 要走 vbtable 间接、
`D*`→`A*` 转型需 this 调整 thunk（`add rcx,[rax-0x18]` 式运行时查表），比非虚 MI 多 1~2 次内存间接。
适用：当基类代表**必须唯一**的共享状态（如 `std::iostream` 共享 `std::ios_base`）。

[标准] virtual 继承共享单一虚基类子对象，消除二义性；代价是运行期偏移解析与 thunk 开销。

</details>
''',

"ch51": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 CRTP 写 `template<class D> struct Printable { void print() const { static_cast<const D*>(this)->do_print(); } };`，
派生类提供 `do_print()`，演示编译期多态（无 vtable、无虚函数）。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
template <class D>
struct Printable {
    void print() const { static_cast<const D*>(this)->do_print(); }   // 编译期静态分发
};
struct Point : Printable<Point> {
    int x = 3;
    void do_print() const { std::cout << "Point(" << x << ")\n"; }
};
int main(){ Point p; p.print(); }   // 调用链在编译期确定, 无 vtable
```

`Printable<Point>` 把 `print` 转成对 `do_print` 的静态调用，编译器能直接内联、无间接跳转。
这是"编译期多态"——类型 `D` 在编译期已知，不需要运行期类型信息。

[标准] CRTP（Curiously Recurring Template Pattern）：基类以派生类为模板参数，静态分发。

</details>

### 练习 2（难度 ★★★）

用 CRTP 实现 Barton–Nackman trick：基类提供 `operator<` 调用派生类的 `compare`，
让派生类自动获得 `<` 且能用于模板，避免虚函数开销。

<details><summary>答案与解析</summary>

```cpp
template <class D>
struct LessThan {
    friend bool operator<(const D& a, const D& b){ return a.compare(b) < 0; }
};
struct Version : LessThan<Version> {
    int major, minor;
    int compare(const Version& o) const {            // 唯一的"真"比较逻辑
        if (major != o.major) return major - o.major;
        return minor - o.minor;
    }
};
// Version 自动拥有 operator<, 可直接用于 std::sort / std::map
```

Barton–Nackman 把"运算符"放在基类、把"核心比较"留给派生类，`operator<` 是 `friend` 自由函数，
能被 ADL 找到、可用于泛型算法，全程零虚函数、可内联。

[标准] Barton–Nackman：基类定义运算符、调用派生类原语；友元自由函数经 ADL 参与重载。

</details>

### 练习 3（难度 ★★★★）

对比 CRTP 与虚函数的性能与局限：写数值算子 `Square`（CRTP）与虚函数版 `Op`，
指出 CRTP 循环体被内联、零间接、但容器必须同类型；虚函数可异构但有 vtable 调用、阻止跨边界内联
（见本书 ch47/ch51 ASM 实证）。说明 Eigen/Boost 为何选 CRTP。

<details><summary>答案与解析</summary>

```cpp
// CRTP: 编译期内联, 但 vector<Square> 不能混存其它算子
template <class D> struct OpCrtp { double eval(double x) const { return static_cast<const D*>(this)->f(x); } };
struct Square : OpCrtp<Square> { double f(double x) const { return x*x; } };

// 虚函数: 可放 vector<Op*>, 但每次调用经 vtable, 难内联
struct Op { virtual double eval(double) const = 0; virtual ~Op()=default; };
struct SquareV : Op { double eval(double x) const override { return x*x; } };
```

CRTP 把虚调用变成静态 `static_cast` + 内联，循环中无 `call [vtable]`，可被整体优化（如向量化）；
但 `Square` 与 `Cube` 是不同类型，无法进同一 `vector`（失去运行时异构）。
虚函数相反：灵活但每次调用间接、阻止内联。Eigen 表达式模板、Boost 算子库选 CRTP 是为了
把"运算符组合"在编译期展开成零开销代码。

[标准] CRTP = 零开销静态多态（失异构）；虚函数 = 运行时多态（失内联）。按场景取用。

</details>
''',
}

DEMOS = {
"ch21": r'''
## 附录：用法演绎 — const 的层层含义：从只读变量到编译期常量

> 场景：很多初学者把 `const` 当成"编译器优化开关"，结果在接口设计、API 边界上踩坑。逐层厘清。

**步骤 1：顶层 const 与底层 const（指针的两种 const）**

```cpp
int v = 1;
const int* p = &v;     // 底层 const: 不能经 p 改 *p, 但 p 可指向别处
int* const q = &v;     // 顶层 const: q 自身不可改(必须初始化), 但 *q 可改
const int* const r = &v; // 既不能改指向也不能改所指
```

`const int*` 读作"指向 const int 的指针"——保护的是**数据**；`int* const` 保护的是**指针变量本身**。
函数参数用 `const T*` 表达"我不修改你传给我的对象"。

**步骤 2：const 成员函数与逻辑 const（mutable）**

```cpp
struct Cache {
    mutable std::size_t hits = 0;   // 逻辑 const 豁免: 不影响对外状态
    int compute() const { ++hits; return 42; }  // const 成员却改了 hits -> 合法
};
```

`const` 成员函数承诺"不修改可观察状态"，但内部计数/缓存用 `mutable` 豁免。
绝不要用 `mutable` 去绕过 const 修改真正的数据成员——那破坏契约。

**步骤 3：constexpr 两用（编译期 + 运行期）**

```cpp
constexpr int sq(int x){ return x*x; }
static_assert(sq(5) == 25);          // 编译期: 不生成任何运行时指令
int get_runtime(){ return 7; }       // 真实运行期函数
int y = sq(get_runtime());           // 运行期: 退化为普通调用
```

**步骤 4：constinit / consteval 消除静态初始化灾难**

```cpp
constexpr int compute(){ return 42; }       // 编译期可求值的初始化器
constinit static int G = compute();  // 强制编译期初始化 -> 无 SIOF, 零运行时开销
consteval int tbl(int n){ return n*2; } // 必须编译期: tbl(rand()) 编译失败
```

**结论**：`const` = 只读契约；`constexpr` = 可在编译期求值的函数/变量（两用）；
`constinit` = 静态对象强制常量初始化（防 SIOF）；`consteval` = 立即函数（只编译期）。
它们解决不同问题，别混为一谈。

**工程含义**：API 边界对"不修改的输入"一律加 `const&`/`const*`；需要编译期能力的才上 `constexpr`/`consteval`。
''',

"ch31": r'''
## 附录：用法演绎 — 从 rule of 3 到 rule of 5：写一个安全的字符串类

> 场景：自己管理资源（动态数组）时，最容易漏写拷贝/移动导致泄漏或双重释放。逐步推导出健壮版本。

**步骤 1：朴素裸指针（漏析构 → 泄漏）**

```cpp
struct MyString {
    char* data; size_t len;
    MyString(const char* s){ len = std::strlen(s); data = new char[len+1]; std::strcpy(data,s); }
    // 没有析构! 离开作用域 data 泄漏; 没有拷贝 -> 默认逐位拷贝导致双重释放
};
```

默认拷贝构造是逐成员浅拷贝：`MyString b = a;` 后 `a.data == b.data`，两者析构各 `delete` 一次 → 双重释放。

**步骤 2：rule of 3（深拷贝补全）**

```cpp
struct MyString {                       // rule of 3: 管理资源的类必须给出三者
    char* data; std::size_t len;
    MyString(const char* s){ len = std::strlen(s); data = new char[len+1]; std::strcpy(data,s); }
    ~MyString(){ delete[] data; }                                          // 析构: 释放资源
    MyString(const MyString& o): len(o.len), data(new char[len+1]) { std::strcpy(data,o.data); } // 深拷贝
    MyString& operator=(const MyString& o){
        if (this != &o) { delete[] data; len=o.len; data=new char[len+1]; std::strcpy(data,o.data); }
        return *this;
    }
};
```

深拷贝让每个对象拥有独立数据——拷贝安全，但每次拷贝都是 O(n) 内存分配 + 复制。

**步骤 3：vector 扩容的性能坑（移动未 noexcept → 退化拷贝）**

```cpp
#include <vector>
#include <cstring>
struct MyString {
    char* data; std::size_t len;
    MyString(const char* s){ len=std::strlen(s); data=new char[len+1]; std::strcpy(data,s); }
    ~MyString(){ delete[] data; }
    MyString(const MyString& o): len(o.len), data(new char[len+1]){ std::strcpy(data,o.data); }
    MyString& operator=(const MyString& o){ if(this!=&o){ delete[] data; len=o.len; data=new char[len+1]; std::strcpy(data,o.data);} return *this; }
};
int main(){
    std::vector<MyString> v;
    v.push_back(MyString("a"));   // 扩容时若 MyString 移动构造非 noexcept, vector 退化为拷贝!
}
```

`std::vector` 扩容为保证强异常安全：仅当移动构造 `noexcept` 时才移动，否则**拷贝**（因为拷贝可回滚、移动失败无法恢复）。

**步骤 4：rule of 5（加 noexcept 移动）**

```cpp
#include <vector>
#include <cstring>
struct MyString {
    char* data; std::size_t len;
    MyString(const char* s){ len=std::strlen(s); data=new char[len+1]; std::strcpy(data,s); }
    ~MyString(){ delete[] data; }
    MyString(const MyString& o): len(o.len), data(new char[len+1]){ std::strcpy(data,o.data); }
    MyString& operator=(const MyString& o){ if(this!=&o){ delete[] data; len=o.len; data=new char[len+1]; std::strcpy(data,o.data);} return *this; }
    MyString(MyString&& o) noexcept : data(o.data), len(o.len) { o.data = nullptr; }      // 移动构造
    MyString& operator=(MyString&& o) noexcept { delete[] data; data=o.data; len=o.len; o.data=nullptr; return *this; }
};
int main(){
    std::vector<MyString> v;
    v.push_back(MyString("a"));   // 移动 noexcept -> 扩容走移动 O(1), 零元素拷贝
}
```

**结论**：管理资源 → 默认优先 **rule of 0**（用 `std::string`/`unique_ptr` 替你管）；
必须手写时 → rule of 5，且**移动操作务必 `noexcept`**，否则容器扩容退回拷贝。

**工程含义**：裸 `new/delete` 几乎只该出现在 `unique_ptr`/`shared_ptr`/`vector` 等设施内部；
手写资源类是现代 C++ 的"最后手段"。
''',

"ch39": r'''
## 附录：用法演绎 — 用 RAII 把 10 处 open/close 收敛成 0 泄漏

> 场景：一段函数有 3 个资源（文件、互斥锁、数据库连接），中途可能抛异常，手写 try/finally 极易漏关。

**步骤 1：手动资源管理（漏 close 的 N 种路径）**

```cpp
#include <cstdio>
int main(){
    FILE* f = std::fopen("a.txt", "r");   // 若下面 throw, fclose 永不调用 -> 句柄泄漏
    // step_that_may_throw();
    std::fclose(f);                        // 仅正常路径执行, 异常路径被跳过
}
```

异常从 `step_that_may_throw()` 逃出，跳过所有清理 → 锁死、句柄泄漏、连接泄漏。

**步骤 2：RAII 包装（析构兜底）**

```cpp
#include <cstdio>
struct FileGuard {
    FILE* f;
    FileGuard(const char* p) : f(std::fopen(p, "r")) {}
    ~FileGuard() { if (f) std::fclose(f); }   // 析构必调用
};
int main(){
    FileGuard fg("a.txt");   // 无论正常/异常, fg 析构自动 fclose -> 全清理
}
```

栈展开（stack unwinding）保证：函数任意点退出，已构造的局部对象按**逆序**析构。
清理逻辑集中到类型里，调用处零心智负担。

**步骤 3：ScopeGuard 处理非资源清理**

```cpp
#include <mutex>
std::mutex m;
int main(){
    m.lock();
    auto g = [&]{ m.unlock(); };   // 作用域结束必解锁, 无论怎么退出
    // ... 任意路径 ...
    g();                           // 真实工程用 scope_exit / unique_lock
}
```

`ScopeGuard` 把"清理动作"存成 lambda，适合"解锁、恢复全局状态、打日志"等非典型资源。

**步骤 4：借 unique_ptr 自定义 deleter 复用标准设施**

```cpp
#include <cstdio>
#include <memory>
int main(){
    auto f = std::unique_ptr<FILE, decltype(&std::fclose)>(std::fopen("a.txt","r"), std::fclose);
    // 文件句柄随 f 析构自动 fclose, 且能放进容器/作为返回值转移所有权
}
```

**结论**：资源管理的唯一正确范式是 RAII——把"释放"绑定到作用域退出；
`unique_ptr`/`lock_guard`/`scope_guard` 覆盖绝大多数场景，手写 `new/delete` 极少需要。

**工程含义**：异常安全不是"加 try/catch"，而是"每个资源都有 RAII 守护"；
这正是现代 C++ 相比 C 在系统可靠性上的核心优势之一。
''',

"ch42": r'''
## 附录：用法演绎 — 严格别名如何悄悄改变你的程序结果

> 场景：网络/序列化代码常需"看一个对象的位模式"或"把同一块内存当不同类型用"。这一步走错就是 UB。

**步骤 1：错误——`reinterpret_cast` 跨类型读写（UB）**

```cpp
float f = 1.0f;
int bits = *reinterpret_cast<int*>(&f);   // 违反严格别名 -> UB
```

编译器假定 `float*` 与 `int*` 不指向同一内存。开启 `-fstrict-aliasing`（默认 `-O2`）后，
它可能把 `f` 的值缓存到寄存器、并不从你写的 `int*` 侧回读，结果与你直觉不符——且因是 UB，
"在这台机器上能跑"不等于"换个优化级别/编译器还正确"。

**步骤 2：合法——`memcpy` 重解释位模式**

```cpp
#include <cstring>
int main(){
    float f = 1.0f; int bits;
    std::memcpy(&bits, &f, sizeof(bits));   // 标准明确允许重解释对象表示
}
```

`memcpy` 是唯一被标准许可的"重新解释对象表示"通道；现代编译器会把它优化成单条寄存器传送，零运行时成本。

**步骤 3：优雅——`std::bit_cast`（C++20）**

```cpp
int bits = std::bit_cast<int>(1.0f);   // 编译期可求值, 类型安全, 零开销
```

比 `memcpy` 更地道：不依赖临时变量，且可在常量表达式中使用。

**步骤 4：高级——`__restrict` 解锁向量化（性能反向利用别名假设）**

```cpp
void axpy(int n, double* __restrict y, const double* __restrict a,
          const double* __restrict x, double c){
    for (int i=0;i<n;++i) y[i] = a[i] + c*x[i];   // 编译器可假定 a/x/y 不重叠 -> 向量化
}
```

严格别名默认让编译器"保守地假设可能别名"；`__restrict` 是程序员承诺"绝不别名"，
把保守重载换成 SIMD 流水线。详见本章「附录 E」真实汇编对比（`no_alias` 比 `char_pun` 省一条 load）。

**结论**：看位模式 → `bit_cast`/`memcpy`；跨类型读写对象 → 必 UB；想帮编译器向量化 → `__restrict`（并自担承诺）。

**工程含义**：严格别名不是学术细节——它直接决定你的序列化/网络/数值代码在 `-O2` 下是否正确与多快。
''',

"ch43": r'''
## 附录：用法演绎 — 矩阵遍历：一次 cache 友好的改写带来 10× 加速

> 场景：对一个 4096×4096 的 `int` 矩阵做前缀和/累加，写法不同性能差一个数量级。

**步骤 1：列优先遍历（cache miss 爆炸）**

```cpp
int main(){
    const int N = 256; int m[N][N]{}; long sum = 0;
    for (int j=0;j<N;++j)
      for (int i=0;i<N;++i)
        sum += m[i][j];        // 每次跨 N*4 字节跳行 -> 几乎每次 cache miss
    (void)sum;
}
```

`N=4096` 时跨距 16KB，远超 64B 缓存行。每个 `m[i][j]` 都在新缓存行，命中率极低，实测可慢 10× 以上。

**步骤 2：行优先遍历（顺序预取友好）**

```cpp
int main(){
    const int N = 256; int m[N][N]{}; long sum = 0;
    for (int i=0;i<N;++i)
      for (int j=0;j<N;++j)
        sum += m[i][j];        // 连续访问, 一个缓存行服务 16 个 int, 硬件预取生效
    (void)sum;
}
```

顺序访问让硬件预取器提前载入下一行，缓存命中率高。

**步骤 3：量化对照（示意，x86-64 / L1 32KB）**

| 写法 | 缓存行利用 | 相对耗时 |
|------|:--:|:--:|
| 列优先 `m[i][j]` | ~1/16 命中 | 1.00×（基线，最慢） |
| 行优先 `m[i][j]` | 顺序预取 | ~0.08× |

**步骤 4：进阶——SOA + SIMD**

```cpp
#include <immintrin.h>
int main(){
    const int N = 64; alignas(32) float x[N]{}, vx[N]{};
    for (int i=0;i<N;i+=8) _mm256_storeu_ps(x+i, _mm256_add_ps(_mm256_loadu_ps(x+i), _mm256_loadu_ps(vx+i)));
}
```

**结论**：算法复杂度相同（都是 O(N²) 次加法），但**访问模式**决定实际耗时；
先顺应内存布局（行优先），再考虑 SOA/SIMD。性能瓶颈常不在算法而在缓存。

**工程含义**：优化先看"数据怎么走"，再看"算什么"；profile 显示热点在内存访问时，改遍历顺序比改算法更划算。
''',

"ch44": r'''
## 附录：用法演绎 — 实时系统里把 new 换成内存池

> 场景：嵌入式/实时控制循环中频繁创建销毁小对象，通用 `new/delete` 的延迟不确定且长期运行产生碎片。

**步骤 1：裸 new（不确定性延迟 + 碎片）**

```cpp
struct Packet { int seq; };
void use(Packet*);                   // -c 仅编译不链接, 声明即可
void control_loop(){
    auto* pkt = new Packet;          // 通用分配器: 可能加锁/查找空闲块/系统调用 -> 延迟抖动
    use(pkt);
    delete pkt;                      // 释放也可能触发合并/系统归还
}
// 长期运行: 不同大小对象混用 -> 外部碎片 -> 某次 new 失败 (嵌入式致命)
```

通用分配器为灵活性付出代价：每次分配延迟不可预测，且空闲块被切碎（外部碎片）。

**步骤 2：固定块池（O(1) 分配 + 零碎片，但有内碎片）**

```cpp
struct Packet { int seq; };
template <class T, std::size_t N> struct FixedPool {
    void* alloc();
    void dealloc(void*);
};
void use(Packet*);                   // 声明即可(-c 不链接)
FixedPool<Packet, 256> pool;        // 启动预分配 256 个 Packet 的存储
void control_loop(){
    void* p = pool.alloc();          // O(1), 无系统调用, 延迟确定
    auto* pkt = ::new(p) Packet;     // 在池块上 placement new 构造
    use(pkt);
    pkt->~Packet(); pool.dealloc(p); // 归还, 无外部碎片
}
```

池的 `alloc` 只移动空闲链表指针——确定性的 O(1)，且固定块之间不存在外部碎片。
代价：块大小固定，若 `sizeof(Packet)` < 块大小则尾部浪费（内部碎片）。

**步骤 3：接入 STL（pmr）**

```cpp
struct Packet { int seq; };
struct PoolResource : std::pmr::memory_resource {
    void* do_allocate(std::size_t, std::size_t) override;
    void  do_deallocate(void*, std::size_t, std::size_t) override;
    bool  do_is_equal(const std::pmr::memory_resource&) const noexcept override;
};
PoolResource res;                    // 你的池包装成 memory_resource
std::pmr::vector<Packet> v{&res};    // vector 内存全部来自池, 零系统调用
```

**步骤 4：实时性对照（示意）**

| 分配器 | 分配延迟 | 碎片风险 | 适用 |
|------|:--:|:--:|:--:|
| 通用 `new/delete` | 不确定（μs~ms） | 外部碎片 | 通用/短生命周期 |
| 固定块池 | 确定 O(1) | 仅内碎片 | 实时/长生命周期 |

**结论**：实时/嵌入式优先确定性——用池把"不确定延迟 + 外部碎片"换成"确定 O(1) + 可控内碎片"；
通用程序则无需提前优化，用系统分配器即可。

**工程含义**：嵌入式内存管理的第一原则是"可预测"而非"峰值利用率"；池化是确定性系统的标配。
''',

"ch50": r'''
## 附录：用法演绎 — 菱形继承：要不要 virtual？

> 场景：设计一个 `Widget` 同时具备 `Drawable` 与 `Clickable`，二者都继承自 `Object`（含 id/refcount）。

**步骤 1：非虚 MI 菱形 → 二义性 + 两份基类**

```cpp
struct Object { int id; };
struct Drawable   : Object {};
struct Clickable  : Object {};
struct Widget : Drawable, Clickable {};
int main(){
    Widget w;
    // w.id = 1;                 // 编译失败: id 来自 Drawable 还是 Clickable? 二义
    w.Drawable::id = 1;         // 消歧, 但 Clickable 那份 id 仍是 0 -> 两份"id"
}
```

非虚继承下 `Object` 被复制两次，`Widget` 含两个 `id` 子对象——同一概念实体出现两份值，逻辑错误。

**步骤 2：显式消歧 → 数据重复（治标不治本）**

```cpp
struct Object { int id; };
struct Drawable : Object {};
struct Clickable : Object {};
struct Widget : Drawable, Clickable {};
int main(){
    Widget w;
    w.Drawable::id = 1; w.Clickable::id = 1;   // 必须两处同步, 易遗漏 -> 状态分裂
}
```

每次改 id 要手动同步两份，任何遗漏都让 `Widget` 内部状态不一致。

**步骤 3：virtual 继承 → 单一基类，但指针调整开销**

```cpp
struct Object { int id; };
struct Drawable  : virtual Object {};
struct Clickable : virtual Object {};
struct Widget : Drawable, Clickable {};     // 共享同一份 Object
int main(){
    Widget w;
    w.id = 1;                                    // 无歧义: 只有一份 Object
}
```

`virtual` 让 `Object` 成为**虚基类**，整个 `Widget` 只有一份 `id`。代价（见本章「[实现]」汇编）：
访问 `id` 走 vbtable 间接，`Widget*`→`Object*` 转型需 this 调整 thunk（运行时查偏移），
比非虚 MI 多 1~2 次内存间接。

**步骤 4：何时选 virtual**

- 基类代表**必须唯一**的共享状态（如 `std::ios_base` 被 `istream`/`ostream` 共享）→ 必须 virtual。
- 基类只是"能力接口"（无数据）→ 非虚 MI 即可（如 `Drawable`/`Serializable` 纯接口）。

**结论**：菱形要不要 virtual，取决于"共享基类是否承载唯一状态"。有状态必 virtual（接受 thunk 开销）；
纯接口用非虚 MI（零额外开销）。

**工程含义**：virtual 继承不是默认选项——它引入运行期偏移解析成本；仅在"共享状态必须唯一"时使用。
''',

"ch51": r'''
## 附录：用法演绎 — 把虚函数调用优化成零成本的静态分发

> 场景：数值计算中有一族算子（`Square`/`Cube`/`Scale`），要高频调用 `eval(x)`。虚函数 vs CRTP 实测取舍。

**步骤 1：虚函数版本（vtable 间接，无法跨边界内联）**

```cpp
struct Op { virtual double eval(double) const = 0; virtual ~Op()=default; };
struct Square : Op { double eval(double x) const override { return x*x; } };
int main(){
    Square s;
    Op* ops[1] = {&s};                     // 实际填充真实算子集合
    double sum = 0;
    for (auto* o : ops) sum += o->eval(2.0);  // 每次 call [vtable], 阻止内联 -> 无法向量化
    (void)sum;
}
```

虚调用在运行期经 vtable 查槽，编译器看不到具体实现，**不能内联**，循环体保留间接跳转。

**步骤 2：CRTP 版本（编译期内联，零间接）**

```cpp
template <class D> struct OpCrtp { double eval(double x) const { return static_cast<const D*>(this)->f(x); } };
struct Square : OpCrtp<Square> { double f(double x) const { return x*x; } };
int main(){
    Square s;
    Square sqs[1] = {s};                  // CRTP: 同类型可装同容器
    double sum = 0;
    for (const auto& o : sqs) sum += o.eval(2.0);  // static_cast + 内联 -> 循环体融合并可向量化
    (void)sum;
}
```

`eval` 编译期解析为 `Square::f`，`x*x` 直接内联进循环体，无 vtable 间接、可被优化/向量化。

**步骤 3：代价——失去运行时异构**

```cpp
struct Op { virtual double eval(double) const = 0; virtual ~Op()=default; };
template <class D> struct OpCrtp { double eval(double x) const { return static_cast<const D*>(this)->f(x); } };
struct Square : OpCrtp<Square> { double f(double x) const { return x*x; } };
std::vector<Square> sqs;          // CRTP: 容器必须同类型, 不能混存 Cube
std::vector<Op*> ops;             // 虚函数: 可混存任意派生类 -> 运行时异构
```

CRTP 把类型绑死在编译期，无法把不同算子放进同一个容器；这是它和虚函数最本质的取舍。

**步骤 4：真实用例（Eigen / Boost）**

Eigen 的"表达式模板"用 CRTP 把 `a + b * c` 在编译期展开成零临时对象的求值循环；
Boost.Operators 用 CRTP 自动生成 `==`/`<` 全套。它们选 CRTP 就是为了"运算符组合零开销"。

**结论**：性能热点 + 类型编译期已知 → CRTP（零开销、失异构）；
需要运行时插件/异构容器 → 虚函数（灵活、失内联）。两者不是替代而是互补。

**工程含义**：多态的"代价"并非必然——CRTP 证明在编译期可知类型时，动态分发的开销可被完全消除。
''',
}

def detect_eol(text):
    return "\r\n" if "\r\n" in text else "\n"

def main():
    for key, (path, mode) in TARGETS.items():
        full = os.path.join(ROOT, path)
        raw = open(full, encoding="utf-8").read()
        eol = detect_eol(raw)
        lines = raw.split(eol)
        # locate '## 自测练习' anchor
        anchor = None
        for i, l in enumerate(lines):
            if l.startswith("## 自测练习"):
                anchor = i
                break
        if anchor is None:
            print(f"[SKIP] {path}: no 自测练习 anchor")
            continue
        ex_block = EXERCISES[key].rstrip("\n")
        demo_block = DEMOS[key].lstrip("\n").rstrip("\n")

        if mode == "simple":
            # replace anchor..EOF with exercises + demo
            new_tail = ex_block + eol + eol + demo_block
            new_lines = lines[:anchor] + new_tail.split("\n")
            out = eol.join(new_lines).rstrip("\n") + eol
            print(f"[OK] {path}: simple, replaced {anchor+1}..EOF with exercises+demo ({len(new_lines)} lines)")
        else:  # preserve: keep original ASM appendix, replace exercises, append/refresh demo ONCE (idempotent)
            # find next '## ' after anchor (start of original ASM appendix)
            next_sec = None
            for j in range(anchor + 1, len(lines)):
                if lines[j].startswith("## "):
                    next_sec = j
                    break
            # find any previously-injected demo marker to avoid duplication
            demo_i = None
            for j in range(anchor, len(lines)):
                if lines[j].startswith("## 附录：用法演绎"):
                    demo_i = j
                    break
            if next_sec is None:
                # no following section -> behave like simple (idempotent)
                new_tail = ex_block + eol + eol + demo_block
                new_lines = lines[:anchor] + new_tail.split("\n")
                out = eol.join(new_lines).rstrip("\n") + eol
                print(f"[OK] {path}: preserve-fallback(simple), {anchor+1}..EOF ({len(new_lines)} lines)")
            else:
                # keep exactly one ASM appendix (between next_sec and optional demo_i) + one demo
                asm_appendix = lines[next_sec:demo_i] if demo_i is not None else lines[next_sec:]
                body = (lines[:anchor]
                        + ex_block.split("\n")
                        + asm_appendix
                        + ["", ""]
                        + demo_block.split("\n"))
                out = eol.join(body).rstrip("\n") + eol
                tag = "demo refreshed" if demo_i is not None else "demo appended"
                print(f"[OK] {path}: preserve(idempotent), exercises {anchor+1}..{next_sec}, "
                      f"{tag} ({len(body)} lines)")
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.write(out)

if __name__ == "__main__":
    main()
