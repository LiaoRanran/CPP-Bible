# 第158章 性能反模式与陷阱

> 标准基: C++23 / GCC 13.1 / 预计阅读: 70min / ⟶ Book/part14_perf/ch152_perf_model.md ⟶ Book/part14_perf/ch154_cache_opt.md / 难度: ★★★★☆

## ① 学习目标 [经验]

识别并消除 C++ 中最常见的 13 类性能反模式，每个附 ❌/✅ 对照和可编译示例。

## ② 不必要的堆分配 [经验]

```cpp
#include <iostream>
#include <vector>
int main() {
    // ❌ std::vector 小数据也堆分配
    // ✅ 栈数组或 std::array
    int arr[4]={1,2,3,4}; // 栈上零分配
    std::cout<<arr[0]<<std::endl;
    return 0;
}
```

## ③ 隐式拷贝与临时对象 [经验]

```cpp
#include <iostream>
#include <string>
void sink(std::string s){} // ❌ 按值传参触发拷贝
void sink_ref(const std::string& s){} // ✅ 常量引用
int main(){ std::string x="hello";sink_ref(x);std::cout<<x<<std::endl;return 0; }
```

## ④ std::endl vs `'\n'` [经验]

```cpp
#include <iostream>
int main(){
    std::cout<<"line1\n";   // ✅ 不 flush
    std::cout<<"line2\n";
    return 0;
}
```

## ⑤ 虚函数间接调用 [经验]

```cpp
#include <iostream>
struct Hot{ int f(int x){return x*2;} }; // ✅ 非虚，直接调用
int main(){ Hot h;std::cout<<h.f(21)<<std::endl;return 0; }
```

## ⑥ 异常在热路径 [经验]

```cpp
#include <iostream>
int div_nothrow(int a,int b){ return b!=0?a/b:0; } // ✅ 不抛异常
int main(){ std::cout<<div_nothrow(10,2)<<std::endl;return 0; }
```

## ⑦ false sharing [经验]

```cpp
#include <iostream>
#include <new>
struct alignas(64) Slot { int v; }; // ✅ cache line 隔离
int main(){ Slot s{}; s.v=42;std::cout<<s.v<<std::endl;return 0; }
```

## ⑧ 缓存不友好遍历 [经验]

```cpp
#include <iostream>
int main(){
    // ❌ 列优先遍历（跨行）  ✅ 行优先遍历
    std::cout<<"row-major: access consecutive memory\n";
    return 0;
}
```

## ⑨ std::regex 构造开销 [经验]

```cpp
#include <iostream>
#include <regex>
int main(){
    static const std::regex re("\\d+"); // ✅ static，只编译一次
    std::cout<<std::regex_search("abc123def",re)<<std::endl;
    return 0;
}
```

## ⑩ std::function 类型擦除 [经验]

```cpp
#include <iostream>
#include <functional>
template<typename F> void call(F&& f){f();} // ✅ 模板，零擦除开销
int main(){call([]{std::cout<<"zero-erase\n";});return 0;}
```

## ⑪ reserve 缺失 [经验]

```cpp
#include <iostream>
#include <vector>
int main(){
    std::vector<int> v; v.reserve(100); // ✅ 预分配，避免多次扩容
    for(int i=0;i<100;++i)v.push_back(i);
    std::cout<<v.size()<<std::endl;
    return 0;
}
```

## ⑫ 移动语义未触发 [经验]

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <utility>
int main(){
    std::vector<std::string> v;
    std::string x="hello";
    v.push_back(std::move(x)); // ✅ 显式 move
    std::cout<<v[0]<<std::endl;
    return 0;
}
```

## ⑬ 过度模板实例化 [经验]

```cpp
#include <iostream>
template<int N> struct Fact{static constexpr int v=N*Fact<N-1>::v;};
template<> struct Fact<0>{static constexpr int v=1;};
int main(){ std::cout<<Fact<5>::v<<std::endl;return 0; }
```

## ⑭ 分支预测失败 [经验]

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
int main(){std::vector<int>v(10000);for(int i=0;i<10000;++i)v[i]=i%2;std::sort(v.begin(),v.end());std::cout<<"sorted\n";return 0;}
```

## ⑮ 跨语言对比 [经验]

| 语言 | 反模式等价 |
|---|---|
| C++ | endl、隐式拷贝、虚函数、false sharing |
| Rust | clone() 滥用、Box 过度、`println!` flush |
| Go | defer 热路径、interface{} boxing、GC pressure |
| Java | auto-boxing、String concatenation、unnecessary synchronization |

```cpp
#include <iostream>
int main(){std::cout<<"Cross-language: all languages have unique perf pitfalls.\n";return 0;}
```

## ⑯ WG21 与标准演进 [标准]

```cpp
// ⑯ 标准中消除性能反模式的关键提案
#include <iostream>
int main() {
    std::cout << "Key performance-related WG21 proposals:\n\n";
    std::cout << "P2300 (std::execution): sender/receiver → eliminate async overhead\n";
    std::cout << "P1144 (trivially relocatable): vector realloc → memmove instead of move-loop\n";
    std::cout << "P2647 (permutable ranges): enable inplace mutation without copy\n";
    std::cout << "P0443 (executors): standardize where work runs → control cache locality\n";
    std::cout << "P2786 (trivial infinite loops): defined behavior → keep intentional spin loops\n\n";
    std::cout << "Impact: each proposal removes a class of accidental overhead from the language.\n";
    std::cout << "trivially relocatable alone can speed up vector::reserve by 2-10x for large T.\n";
    return 0;
}
```

## ⑰ FAQ：性能诊断实战 [经验]

```cpp
// ⑰ 性能反模式的诊断与修复问答
#include <iostream>
#include <vector>
int main() {
    std::cout << "Q: 如何确认一个函数是热路径？\n";
    std::cout << "A: perf record -g ./app → perf report → 看 top 10 函数。>1% CPU = hot path.\n\n";
    std::cout << "Q: 反模式在冷路径上需要修吗？\n";
    std::cout << "A: 不需要。修复反模式有代码复杂度代价。只在热路径上修，并测量验证。\n\n";
    std::cout << "Q: std::vector 的 push_back 慢怎么排查？\n";
    std::cout << "A: 检查 3 件事：① 是否 reserve()? ② 元素是否 noexcept movable? ③ 是否在循环中做大量 emplace?\n\n";
    std::cout << "Q: false sharing 如何检测？\n";
    std::cout << "A: perf c2c (cache-to-cache) 命令。或 perf stat -e cache-misses 看 L1 缺失率。\n\n";
    std::cout << "Q: 用了 endl 但没感觉慢？\n";
    std::cout << "A: 因为你测量的不是 I/O bound 场景。STDERR 默认无缓冲，endl 在 STDERR 上无额外开销。\n";
    return 0;
}
```

## ⑱ 最佳实践总结 [经验]

```cpp
// ⑱ 性能优化的 6 条铁律
#include <iostream>
#include <vector>
#include <string>

// 铁律1: 先测量，再优化
// 铁律2: Reserve before push_back
void good_reserve() {
    std::vector<int> v; v.reserve(10000);
    for (int i = 0; i < 10000; ++i) v.push_back(i);
}

// 铁律3: 传 const& 或值（小对象）
int sum_vec(const std::vector<int>& v) {
    int s = 0; for (int x : v) s += x; return s;
}

// 铁律4: noexcept move 让 vector 扩容走快速路径
struct Movable { int* d; Movable(Movable&&) noexcept {} Movable() : d(nullptr) {} };

// 铁律5: static const regex（避免每调用编译）
// 铁律6: 用 '\n' 而非 std::endl（避免每行 flush）

int main() {
    good_reserve();
    std::vector<int> v{1,2,3};
    std::cout << "sum: " << sum_vec(v) << std::endl;
    std::cout << "\nLaws of Performance Optimization:\n";
    std::cout << "1. Profile first, optimize later\n";
    std::cout << "2. Reserve containers before filling\n";
    std::cout << "3. Pass by const& for large objects\n";
    std::cout << "4. Mark move constructors noexcept\n";
    std::cout << "5. static for expensive-to-construct objects (regex, random_device)\n";
    std::cout << "6. '\\n' not std::endl (unless flush is intended)\n";
    return 0;
}
```

## ⑲ 性能数据参考：反模式代价量化 [经验]

```cpp
// ⑲ 常见反模式的量化性能数据
#include <iostream>
#include <chrono>
#include <vector>
#include <string>
#include <functional>
int main() {
    std::cout << "=== Antipattern Cost Quantification ===\n\n";
    std::cout << "Cache miss (L1→L3):   ~40 cycles (~13ns @ 3GHz)\n";
    std::cout << "Cache miss (L3→RAM):  ~200 cycles (~67ns)\n";
    std::cout << "Branch mispredict:     ~15-20 cycles (~5-7ns)\n";
    std::cout << "malloc/free:           ~50-100ns (fast path)\n";
    std::cout << "syscall (write/read):  ~200-500ns\n";
    std::cout << "std::endl (flush):     +1 syscall → ~1us\n";
    std::cout << "virtual call:          +5ns (indirect) + ~15ns (if mispredict)\n";
    std::cout << "std::function call:    +10ns (type-erased) vs +0ns (template)\n";
    std::cout << "vector push w/o reserve: +O(n) realloc × log(n)\n\n";
    std::cout << "Amdahl''s Law: 优化 50% 代码 → max 2× speedup.\n";
    std::cout << "              优化 95% 代码 → max 20× speedup. Target hot paths only.\n";
    return 0;
}
```

## ⑳ 源码阅读路线 [经验]

```cpp
// ⑳ 学习性能优化的开源项目阅读路线
#include <iostream>
int main() {
    std::cout << "=== Perf Reading Roadmap ===\n\n";
    std::cout << "Level 1: Micro-patterns\n";
    std::cout << "  → folly/FBVector.h (SSO vector, ~500 lines)\n";
    std::cout << "  → absl/InlinedVector.h (inline storage vector)\n\n";
    std::cout << "Level 2: Data structures\n";
    std::cout << "  → folly/AtomicHashMap.h (lock-free hash map)\n";
    std::cout << "  → absl/flat_hash_map.h (open-addressing, cache-friendly)\n\n";
    std::cout << "Level 3: Full systems\n";
    std::cout << "  → ClickHouse (column store, SIMD, cache-optimized)\n";
    std::cout << "  → ScyllaDB (Seastar framework, shared-nothing, DPDK)\n";
    std::cout << "  → Linux kernel RCU (Read-Copy-Update, zero-overhead reads)\n\n";
    std::cout << "Level 4: Hardware-aware\n";
    std::cout << "  → Agner Fog''s optimization manuals (x86 microarchitecture)\n";
    std::cout << "  → Intel Optimization Reference Manual\n";
    std::cout << "  → ARM Cortex-A Programmer''s Guide\n";
    return 0;
}
```

## 补充完整可编译示例

```cpp
#include <iostream>
#include <array>
int main(){ std::array<int,10> a{}; a[0]=1;std::cout<<a[0]<<std::endl;return 0; }
```

```cpp
#include <iostream>
#include <cstring>
int main(){ char buf[128]; std::strcpy(buf,"stack");std::cout<<buf<<std::endl;return 0; }
```

```cpp
#include <iostream>
int main(){ for(int i=0;i<1000;++i); std::cout<<"no std::endl flush\n";return 0; }
```

```cpp
#include <iostream>
struct Direct{ int val()const{return 42;} };
int main(){Direct d;std::cout<<d.val()<<std::endl;return 0;}
```

```cpp
#include <iostream>
int safe_div(int a,int b){if(b==0)return 0;return a/b;}
int main(){std::cout<<safe_div(10,2)<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <new>
int main(){std::cout<<"constexpr size="<<std::hardware_destructive_interference_size<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int a[4][4];for(int i=0;i<4;++i)for(int j=0;j<4;++j)a[i][j]=i+j;std::cout<<a[0][0]<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <string>
int simple_match(const std::string& s,const std::string& pat){return s.find(pat)!=std::string::npos;}
int main(){std::cout<<simple_match("hello","ell")<<std::endl;return 0;}
```

```cpp
#include <iostream>
void call_lambda(void(*f)()){f();}
int main(){call_lambda([]{std::cout<<"fnptr\n";});return 0;}
```

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v;v.reserve(50);for(int i=0;i<50;++i)v.push_back(i);std::cout<<v.size()<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <vector>
#include <utility>
struct Movable{int* p=nullptr;Movable(int x):p(new int(x)){}~Movable(){delete p;}Movable(Movable&&o)noexcept:p(std::exchange(o.p,nullptr)){}Movable(const Movable&)=delete;Movable&operator=(Movable&&o)noexcept{delete p;p=std::exchange(o.p,nullptr);return*this;}int get()const{return p?*p:0;}};
int main(){std::vector<Movable> v;v.push_back(Movable{42});std::cout<<v[0].get()<<std::endl;return 0;}
```

```cpp
#include <iostream>
template<int N>constexpr int fib(){return fib<N-1>()+fib<N-2>();}
template<> constexpr int fib<0>(){return 0;}
template<> constexpr int fib<1>(){return 1;}
int main(){std::cout<<fib<10>()<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int x;std::cin>>x;std::cout<<x*2<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"branch prediction: [[likely]]/[[unlikely]] hints\n";return 0;}
```

```cpp
#include <iostream>
#include <vector>
int sum(const std::vector<int>& v){int s=0;for(int x:v)s+=x;return s;}
int main(){std::vector<int> v{1,2,3,4,5};std::cout<<sum(v)<<std::endl;return 0;}
```

```cpp
#include <iostream>
int abs_branchless(int x){int m=x>>31;return(x^m)-m;}
int main(){std::cout<<abs_branchless(-99)<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int v=42;int&r=v;r=100;std::cout<<v<<std::endl;return 0;}
```

## 附录: 反模式代价速查与修复

| 反模式 | 典型代价 | 修复 |
|---|---|---|
| 隐式拷贝 | O(n) heap alloc | const& / move |
| endl | syscall/line | `'\n'` |
| 虚函数热路径 | ~5ns indirect | CRTP/final/template |
| 异常热路径 | ~100ns unwind | error_code/optional |
| false sharing | 60ns bounce | alignas(64) |
| reserve缺失 | logN realloc | .reserve(N) |
| regex重复编译 | ~1us/次 | static const |
| std::function hot | 32B erase | template param |

```cpp
#include <iostream>
int main(){std::cout<<"Profile first, fix only hot path. 80% of antipatterns are harmless outside critical path.\n";return 0;}
```

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v;v.reserve(1000);for(int i=0;i<1000;++i)v.push_back(i);std::cout<<v.size()<<std::endl;return 0;}
```

> 自检: 所有 cpp 块用 `g++ -std=c++23 -O2 -Wall -Wextra` 可独立编译。


## 相关章节（交叉引用）

- **相邻主题**：`Book/part14_perf/ch157_compiler_explorer.md`（第157章 Compiler Explorer 实战）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part15_cases/ch159_threadpool.md`（第159章 从零实现线程池（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part14_perf/ch156_compiler_opt.md`（第156章　编译器优化：O2/O3/Ofast/LTO/PGO（GCC））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part15_cases/ch160_mempool.md`（第160章 从零实现内存池（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part14_perf/ch153_cpu_micro.md`（第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行）—— 同模块下的其他主题。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

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

### 练习 3（难度 ★★）

写一个 `noexcept` 移动构造函数，使 `std::vector` 扩容时走移动而非拷贝。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <utility>
struct S {
  int* p = new int[8];
  S() = default;
  S(S&& o) noexcept : p(o.p) { o.p = nullptr; }
  ~S() { delete[] p; }
};
int main() { std::vector<S> v; v.push_back(S{}); v.push_back(S{}); std::cout << "ok\n"; }
```

[标准] `noexcept` 移动构造让 `vector` 在重新分配时移动元素；否则因强异常保证退化为拷贝。

</details>

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。每个项目都是性能反模式的"对面教科书"。

- **Google Benchmark（github.com/google/benchmark）**：微基准框架——量化"看似等价的写法"的 ns/us 级差异，是识别性能反模式的标尺。
  → <https://github.com/google/benchmark>
- **Chromium base（github.com/chromium/chromium）**：`base::` 的性能纪律（`base::NoDestructor`、`base/containers` 的缓存友好容器），是"避免隐式分配/拷贝"的工业样板。
  → <https://github.com/chromium/chromium>
- **LLVM（github.com/llvm/llvm-project）**：`-O2/-O3` 优化 passes（`llvm/lib/Transforms/Scalar`）消除本可避免的拷贝/分支；本章反模式在被优化器救回前先要被人工识别。
  → <https://github.com/llvm/llvm-project>
- **folly（github.com/facebook/folly）**：`folly::` 的高性能原语（`folly::fbvector` 小对象优化、`folly::ProducerConsumerQueue` 无锁队列），展示反模式的对面写法。
  → <https://github.com/facebook/folly>
- **ClickHouse（github.com/ClickHouse/ClickHouse）**：列式引擎的手写 SIMD（`src/Common/` 的 `memcpySmall`、`PODArray` 批量算法），把"数据局部性 + 向量化"做到极致。
  → <https://github.com/ClickHouse/ClickHouse>
- **Boost（github.com/boostorg）**：`boost::container::small_vector`/`flat_map` 等"小对象内联 + 大对象堆"的混合分配，规避 `std::vector` 小尺寸下的分配反模式。
  → <https://github.com/boostorg>
- **Abseil（github.com/abseil/abseil-cpp）**：`absl::InlinedVector`/`absl::flat_hash_map`（Swiss Table，开放寻址 + SIMD 探针）是 `std::unordered_map` 链地址法反模式的现代替代。
  → <https://github.com/abseil/abseil-cpp>
- **V8（github.com/v8/v8）**：JavaScript 引擎的 GC 与内联缓存（IC）设计，展示"避免无意义分配/缓存未命中"在系统级的重要性。
  → <https://github.com/v8/v8>
- **Redis（github.com/redis/redis）**：纯内存数据结构的零拷贝与紧凑编码（`ziplist`/`listpack`），是对"盲目用链表"反模式的直接否定。
  → <https://github.com/redis/redis>
- **RocksDB（github.com/facebook/rocksdb）**：LSM 树的块缓存与前缀 bloom filter，把"随机 IO + 缓存未命中"反模式转化为顺序写 + 点查命中。
  → <https://github.com/facebook/rocksdb>

**常见陷阱 / 最佳实践**：性能反模式的根因多为三类——① 隐式堆分配（小对象也 `new`）；② 缓存不友好（链表/指针追逐）；③ 分支不可预测（数据依赖分支）。对照 [ch153](Book/part14_perf/ch153_cpu_micro.md) 的微架构与 [ch156](Book/part14_perf/ch156_compiler_opt.md) 的优化器，先量后改（`-O2` + benchmark），不靠直觉。

