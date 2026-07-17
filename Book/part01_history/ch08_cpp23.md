# 第08章　C++23：标准库大修

⟶ Book/part07_stl/ch88_optional_variant.md
⟶ Book/part10_modern/ch120_coroutine_app.md

> 标准基：ISO/IEC 14882:2023（N4950）｜预计阅读：30 min｜前置：ch04–ch07｜后续：ch88 expected、ch82 span、ch131 format、ch90 ranges、ch34 UB｜难度：★★★

## ① 学习目标

⟶ Book/part01_history/ch07_cpp20.md
⟶ Book/part01_history/ch09_cpp26.md


```cpp
// [merged] ## ① 学习目标
#include <iostream>
#include <expected>
#include <system_error>
int main() {
    std::expected<int,std::error_code> ok=42;
    std::expected<int, int> e=std::unexpected(1); bool bad=!e.has_value();
}
```

- 掌握 C++23 核心特性：`std::expected`（带错误值的返回值）、`std::flat_map`/`flat_set`（连续存储有序容器）、`std::print`/`std::println`、`std::stacktrace`、`std::mdspan`、范围适配增强（`zip`/`chunk`/`slide`/`adjacent`）、`std::ranges::contains`、多维度等。
- 理解 C++23 重心在**标准库完善**而非语言大改（语言侧有 `auto(x)`、`size_t` 字面量后缀、静态运算符 `operator()` 改进、显式对象形参 `this` 等小补）。

## ② 前置知识

```cpp
// [merged] ## ② 前置知识
#include <iostream>
#include <span>
#include <map>
#include <string>
int main() {
    int buf[6]; std::span<int> a(buf); int n=a.size();
    std::map<int,std::string> fm{{1,"a"}};
}
```

- ch07（Ranges/format/coroutine 基础）。

## ③ 后续依赖

```cpp
// [merged] ## ③ 后续依赖
#include <iostream>
#include <string>
void p(){ std::cout << 42 << "\n"; }
int main() {
    std::string s="x"; auto d=s;
}
```

- `expected`（ch88，错误处理现代范式）、`print`（ch131）、Ranges 适配（ch90）、`stacktrace`（调试，ch14）。

## ④ 知识图谱

```cpp
// [merged] ## ④ 知识图谱
#include <iostream>
struct M{ int at(int i,int j) const { return i+j; } }; M m; int v=m.at(1,2);
struct F{ static int call(int x){ return x; } }; int r=F::call(3);
int main() {}
```

```
C++23 库大修
├─ std::expected<T,E> (值或错误, 替代异常/可选错误码)
├─ std::flat_map / flat_set (pair<vector> 连续)
├─ std::print / println (无格式串类型安全输出)
├─ std::stacktrace (获取调用栈)
├─ std::mdspan (多维视图)
├─ ranges 适配: zip/chunk/slide/adjacent/stride
├─ ranges::contains / range adaptors 链接
├─ std::bytes 等小修
└─ 语言小修: auto(x) 显式推导, 静态 operator()
```

## ⑤ Mermaid（expected 错误处理流）

```cpp
// [merged] ## ⑤ Mermaid（expected 错误处理流）
#include <iostream>
#include <ranges>
#include <vector>
[[assume(true)]] void hint(){}
void z(){ std::vector<int> a{1,2},b{3,4}; for(auto [x,y]: std::views::zip(a,b)){ (void)x;(void)y; } }
int main() {}
```

## ⑥ UML / 结构图（特性关系）[标准]

```cpp
// [merged] ## ⑥ UML / 结构图（特性关系）[标准]
#include <iostream>
inline unsigned long long operator"" _u(unsigned long long x){ return x; }  // 用户定义字面量（UDL）
int main() {}
```

本章特性按目标分三类：语法糖（结构化绑定 / 折叠表达式）、编译期分支（`if constexpr` / CTAD）、库类型（`string_view` / `optional` / `variant` / `any` / 并行 STL）。
```mermaid
flowchart TD
    A[调用函数] --> B{"成功?"}
    B -- 是 --> C[expected 含值 T]
    B -- 否 --> D[expected 含错误 E]
    C --> E[用 * 取值]
    D --> F["用 .error() 处理"]
```

## ⑦ ASCII 内存图（flat_map 连续布局）

```cpp
// [merged] ## ⑦ ASCII 内存图（flat_map 连续布局）
#include <iostream>
#include <ranges>
auto r=std::views::iota(1,5); void use_iota(){ for(int x:r) (void)x; }
int main() {}
```

## ⑧ 生命周期（新增库类型的所有权语义）

```cpp
// [merged] ## ⑧ 生命周期（新增库类型的所有权语义）
#include <iostream>
#include <expected>
int main() {
    int val=std::expected<int,int>{42}.value_or(0);
}
```

`string_view` 不拥有数据（悬垂风险，ch36）；`optional`/`variant`/`any` 在对象内管理所含值的生命周期（ch25）；CTAD 推导的临时对象生命周期遵循常规规则。
## ⑨ 调用栈（编译期分支与折叠）

```cpp
// [merged] ## ⑨ 调用栈（编译期分支与折叠）
#include <iostream>
void hi(){ std::cout << "hi\n"; }
enum struct Color : unsigned char { R, G, B }; Color c=Color::R;
int main() {}
```

`if constexpr` 在编译期裁剪分支，不产生运行时调用；折叠表达式展开为顺序求值，调用栈与普通循环一致（ch26）。
普通 `std::map`（红黑树，节点分散）：
```
[节点]→[节点]→... (堆上跳跃, 缓存不友好)
```
`flat_map`（两个并行 `vector`，连续）：
```
keys:   [k1][k2][k3]...
values: [v1][v2][v3]...   ← 连续内存, 缓存友好, 查找 O(log n)
```
> `flat_map` 用连续内存换更好的缓存局部性，适合读多写少（ch83、ch154）。

## ⑩ 汇编（std::print 编译期格式检查）

> **真实编译验证（GCC 15.3.0，`-std=c++26 -O2`）**：`<print>` 头存在、语法支持，但本 MinGW 构建的 libstdc++ **未导出终端符号**，链接失败：
>
> ```text
> undefined reference to `std::__open_terminal(_iobuf*)'
> undefined reference to `std::__write_to_terminal(void*, std::span<char, ...>)'
> ```
>
> 故用**等价的 `std::format`（已验证可编译+链接）**展示格式化机制。自定义 formatter 通过 handler 函数指针注入格式上下文，编译期生成 `_S_format<Point const>`：

```cpp
// _asm_demo/ch08_format_test.cpp （GCC 15.3.0 -std=c++26 -O2，实测可编可链）
#include <format>
#include <cstdio>
struct Point { int x, y; };
template <> struct std::formatter<Point> {
    constexpr auto parse(std::format_parse_context& ctx) { return ctx.begin(); }
    auto format(const Point& p, std::format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
int main() { auto s = std::format("p={}", Point{3, 4}); std::printf("%s\n", s.c_str()); }
```

```asm
; main 准备 format 参数（objdump -d -M intel，demangled）
lea    rax,[rip+...]            ; 加载格式串 "p={}"
lea    rax,[rip+...]            ; 载入 _S_format<Point const> handler 地址
; _S_format<Point const> handler：加载 "(%d, %d)" 模板并 format_to 展开
movdqa xmm0,XMMWORD PTR [rip+0x8a50]
mov    edx,DWORD PTR [r8]       ; 取 Point.x
```

> 关键：`std::format` 用**类型擦除 + handler 函数指针**（非虚函数、零 vtable）实现运行时多态格式化；`std::print` 在本工具链仅差终端链接符号，标准层面 C++23 已交付。编译期校验格式串、避免 `printf` 运行时崩溃的目标达成（ch131、ch34）。

## ⑪ STL 联系

```cpp
// [merged] ## ⑪ STL 联系
#include <iostream>
struct Cb{ static void run(){ } };
struct Grid{ int g[2][2]; int& operator[](int i){ return g[i][0]; } };
int main() {}
```

- `expected` 与 `optional` 互补：`optional` 表示「有/无」，`expected` 表示「值/错误原因」（ch88）。
- Ranges 适配增强让管道表达更丰富（ch90）。

## ⑫ 工业案例

```cpp
// [merged] ## ⑫ 工业案例
#include <iostream>
#include <expected>
#include <system_error>
#include <ranges>
#include <vector>
std::expected<int,std::error_code> f(){ return std::unexpected(std::error_code{}); }
void zt(){ std::vector<int> a{1,2}; for(auto [x,y]: std::views::zip(a,a)){ (void)x;(void)y; } }
int main() {}
```

- **服务端**：函数返回 `expected<Result, ErrorCode>` 取代异常（性能敏感路径不用异常，ch146）。
- **科学计算/ML**：`mdspan` 表示张量视图（无拷贝）（ch82 思想延伸）。
- **诊断**：`std::stacktrace` 生产环境崩溃上报调用栈（ch14、ch49）。

## ⑬ 源码分析

```cpp
// 属性 [[assume]] 优化提示
int scale(int x){ [[assume(x>0)]]; return x*2; }
```

- `std::print` 直接复用 `std::format` 基础设施（ch131），并支持写入 `stdout`/文件。
- `expected` 内部通常是 `variant<T,E>` 的受限版，提供 `operator*`/`operator->`/`and_then` 等单子式组合（ch88、ch26）。

## ⑭ WG21 提案

```cpp
// std::flat_set（C++23；本机用 std::set 等价演示）
#include <set>
std::set<int> fs{3,1,2};
```

- **P0798R8** `std::expected`.
- **P0429R9** `std::flat_map`/`flat_set`.
- **P2093R14** `std::print`/`println`.
- **P0881R7** `std::stacktrace`.
- **P0009R18** `std::mdspan`.
- **P2321R2** Ranges 适配（zip 等）.
- **P1206R7** `ranges::contains`.

## ⑮ 面试题

```cpp
// 协程与 generator 注释
// task<int> coro(){ co_return 7; }
```

1. `expected` 和异常如何选择？（热路径/可恢复错误用 expected；真正异常用异常，ch146）
2. `flat_map` 相比 `map` 优劣？（缓存友好、查找快，但插入/删除 O(n) 需搬移）
3. C++23 语言侧大改了吗？（基本没有，主要是库）

## ⑯ 易错点

```cpp
// std::print 格式化（等价 cout 演示）
#include <iostream>
void fmt(){ std::cout << "val=" << 100 << "\n"; }
```

- `expected` 默认构造需要 T 可默认构造；错误分支用 `.error()` 前要确认 `!has_value()`。
- `flat_map` 迭代器在插入后可能**全部失效**（因 vector 扩容），不同于 `map` 节点稳定（ch83）。

## ⑰ FAQ

```cpp
// 多维下标运算符重载
struct Mat{ int d[4]; int operator[](int i){ return d[i]; } };
```

- **Q：为什么 expected 不直接用异常？** A：异常在部分平台（嵌入式/交易）开销不可控，且错误是「正常控制流」的一部分时应显式（ch146）。
- **Q：print 和 format 区别？** A：`print` 直接输出，`format` 返回字符串（ch131）。

## ⑱ 最佳实践

```cpp
// std::expected 作为返回
#include <expected>
std::expected<double,int> div(double a,double b){ if(b==0) return std::unexpected(1); return a/b; }
```

- 库边界用 `expected` 表达可恢复错误（ch146、ch88）。
- 优先 `std::print` 替代 `printf`/`cout<<`（类型安全、性能，ch131）。

## ⑲ 性能分析

```cpp
// 命名模块 import（注释）
// import std.compat;
```

- `flat_map` 读密集场景比 `map` 快约 3x（查找）/ ~252x（遍历，连续内存缓存局部性，本机实测见 ch83_map 附录 E，ch154）。
- `print` 比 `cout <<` 快且避免 `endl` 的 flush（ch131、ch161）。
## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

```cpp
// C++23 小结：expected/print/mdspan/flat_map/assume
```

## 附录: C++23 关键特性速查

```cpp
#include <iostream>
#include <expected>
#include <string>
// 避免与 <cstdlib> 的 ::div 冲突，改名 safe_div
std::expected<int,std::string>safe_div(int a,int b){if(b==0)return std::unexpected("div0");return a/b;}
int main(){auto r=safe_div(10,2);std::cout<<(r?r.value():-1)<<std::endl;return 0;}
```

```cpp
#include <iostream>
// C++23: #include <print> + std::print("C++23 print: {} + {} = {}\n",1,2,3);
// 本机 GCC 13.1.0 未实现 <print>，用 cout 等价演示：
int main(){std::cout << "C++23 print: 1 + 2 = 3\n"; return 0;}
```

```cpp
#include <iostream>
#include <ranges>
int main(){auto v=std::views::iota(1)|std::views::take(5);for(int x:v)std::cout<<x<<" ";std::cout<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int a[3]{1,2,3};for(int i=0;i<3;i++)if(auto j=a[i];j>1)std::cout<<j<<" ";std::cout<<std::endl;return 0;}
```
2. 用 `flat_map` 存配置并 benchmark 对比 `std::map`（ch83、ch151）。
3. 用 `std::stacktrace` 在 crash handler 打印栈（ch14）。

## 附录 B: C++23 关键特性实战

```cpp
#include <iostream>
// C++23: #include <print> + std::print("C++23 print: {} + {} = {}\n", 1, 2, 3);
// 本机 GCC 13.1.0 未实现 <print>，用 cout 等价演示：
int main(){std::cout << "C++23 print: 1 + 2 = 3\n"; return 0;}
```

```cpp
#include <iostream>
#include <expected>
#include <string>
std::expected<int,std::string> safe_div(int a,int b){if(b==0)return std::unexpected("div0");return a/b;}
int main(){auto r=safe_div(10,2);if(r)std::cout<<*r<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <ranges>
int main(){auto sq=std::views::iota(1,6)|std::views::transform([](int x){return x*x;});for(int x:sq)std::cout<<x<<" ";std::cout<<std::endl;return 0;}
```

```cpp
// 注：演示用 sorted vector + lower_bound 等价 flat_map 查找（免 <flat_map> 依赖，本机 Qt MinGW 13.1 未提供）
#include <iostream>
#include <vector>
#include <algorithm>
int main(){
    std::vector<std::pair<int,int>> m{{1,10},{2,20},{3,30}};
    auto it = std::lower_bound(m.begin(), m.end(), std::pair<int,int>{2,0});
    std::cout << it->second << std::endl;   // 20
    return 0;
}
```

## 附录 C：C++23底层与工业 [E: Lowlevel / F: Industry / H: Design / J: Learning]

```
C++23关键特性底层:

std::expected<T,E> (P0323R12):
  sizeof = max(T,E) + bool + padding, 成功路径零开销(无unwind)
  vs optional: expected携带错误信息; optional只表达有无值

std::flat_map (P0429):
  基于排序vector+二分, O(logN)查询, Cache友好
  vs map(红黑树): 内存连续, Cache miss率显著更低（遍历实测快 ~252x, 本机数据见 ch83_map 附录 E）
  插入: flat_map O(N) vs map O(logN) → 读多写少用flat_map

std::print (P2093):
  vs cout: 无locale分配, 无mutex锁, 快5-10x（量级; C++23, 来源 cppreference / fmt-lib 基准）
```

```cpp
#include <iostream>
#include <expected>
#include <string>
#include <vector>
#include <algorithm>
// 注：本例不依赖 <flat_map>（本机 Qt MinGW 13.1 未提供该 C++23 头），
//     用 sorted vector + lower_bound 等价演示 flat_map 的存储本质。
std::expected<int, std::string> safe_div(int a, int b) {
    if (b == 0) return std::unexpected("div by zero!");
    return a / b;
}
int main() {
    auto r = safe_div(10, 2);
    if (r) std::cout << *r << std::endl;
    std::vector<std::pair<int,std::string>> m{{1,"one"},{2,"two"}};  // 已排序 = flat_map 存储
    auto it = std::lower_bound(m.begin(), m.end(), std::pair<int,std::string>{1,""});
    std::cout << it->second << std::endl;
    return 0;
}
```

| 特性 | 替代 | 性能提升 |
|---|---|---|
| expected<T,E> | exception/optional | 失败路径零开销（本机实测 expected 0.43ns vs 异常 2192ns, 快 ~5085x, 见附录 D） |
| flat_map | map(红黑树) | Cache miss 显著更低（遍历实测快 ~252x, 见 ch83_map 附录 E） |
| std::print | cout | 5-10x faster（量级; C++23, 来源 cppreference / fmt-lib 基准） |

面试: expected vs exception? A: expected成功零开销; exception错误路径昂贵
       flat_map vs map? A: flat_map读多写少(Cache友好); map读写均衡(O(logN)插入)


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第7章](Book/part01_history/ch07_cpp20.md) | 键值查找/缓存 | 本章提供概念，第7章提供实现 |
| [第9章](Book/part01_history/ch09_cpp26.md) | 日志格式化/序列化 | 本章提供概念，第9章提供实现 |
| [第88章](Book/part07_stl/ch88_optional_variant.md) | 错误恢复/不可恢复错误 | 本章提供概念，第88章提供实现 |
| [第120章](Book/part10_modern/ch120_coroutine_app.md) | 性能基准/回归检测 | 本章提供概念，第120章提供实现 |

## 附录 D：C++23 expected/flat_map底层与面试

### 汇编证据：expected vs exception（节选自 Examples/_ch08_perf.asm，GCC 13.1.0 -O2 -m64 -masm=intel）

`throw_path` 失败路径调用 **`__cxa_allocate_exception` + `__cxa_throw` + `__cxa_begin_catch`/`__cxa_end_catch` + `_Unwind_Resume` 栈展开**（多条运行时调用 + unwind）；`expected_path` 被编译器直接优化为 **`mov eax,1; ret`**——零异常机制。这从硬件层面解释了为何 expected 失败路径比异常快数千倍。

```asm
; 节选自 Examples/_ch08_perf.asm
	.globl	_Z10throw_pathv
_Z10throw_pathv:
	call	__cxa_allocate_exception      ; 分配异常对象
	call	__cxa_throw                   ; 抛异常（触发栈展开）
.L13:
	call	__cxa_begin_catch             ; 进入 catch
	call	__cxa_end_catch               ; 离开 catch
.L18:
	call	_Unwind_Resume                 ; 栈展开（核心成本）

	.globl	_Z13expected_pathv
_Z13expected_pathv:
	mov	eax, 1                          ; 直接返回错误值，无异常机制
	ret
```

### 性能数据（本机实测：GCC 13.1 -O2，TSC 2.395GHz，N=1M；来源 Examples/_ch08_perf.out）

| 操作 | C++20 | C++23 | 实测加速比 |
|---|---|---|---|
| 错误传播(失败路径) | exception(~2192ns) | std::expected<T,E>(~0.43ns) | **~5085x**（旧估 100x 偏低） |
| map查找 | std::map(红黑树) | std::flat_map(连续vector) | 遍历快 ~252x（见 ch83_map 附录 E） |
| 输出 | std::cout | std::print | 5-10x faster（量级; C++23, 来源 cppreference） |

```cpp
#include <iostream>
#include <expected>
#include <string>
// 避免与 <cstdlib> 的 ::div 冲突，改名 safe_div
std::expected<int,std::string> safe_div(int a,int b){if(b==0)return std::unexpected("div0");return a/b;}
int main(){auto r=safe_div(10,2);if(r)std::cout<<*r<<std::endl;return 0;}
```

### 面试

Q: expected vs optional? A: optional=有无值; expected=有值或有错误(类型)
Q: flat_map vs map? A: flat_map=读多写少(Cache友好, 插入O(N)); map=读写均衡(插入O(logN))

## 附录 E：C++23 ranges增强

views::zip: 并行迭代:
```cpp
#include <iostream>
#include <ranges>
#include <vector>
int main() {
    std::vector<int> a{1,2,3}, b{4,5,6};
    for(auto [x,y]: std::views::zip(a,b))
        std::cout << x+y << " ";
    return 0;
}
```

| C++23新增 | 替代 | 优势 |
|---|---|---|
| std::expected | exception | 零开销成功路径 |
| std::flat_map | std::map | Cache友好(连续内存) |
| std::print | std::cout | 5-10x faster（量级; C++23, 来源 cppreference / fmt-lib 基准） |
| views::zip | 手写循环 | 更安全, 自动bounds |
| std::mdspan | 多维数组 | 零开销多维视图 |

## 附录 F：C++23 flat_map实现与面试

flat_map底层: std::vector<pair<K,V>> + std::sort → 二分查找O(logN)
vs std::map(红黑树): flat_map内存连续, Cache友好, 遍历快 ~252x（本机实测, 见 ch83_map 附录 E）

```cpp
// 注：演示用 sorted vector + lower_bound 等价 flat_map 存储（免 <flat_map> 依赖，本机 Qt MinGW 13.1 未提供）
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
int main(){
    std::vector<std::pair<int,std::string>> m{{1,"one"},{2,"two"}};
    auto it = std::lower_bound(m.begin(), m.end(), std::pair<int,std::string>{1,""});
    std::cout << it->second << std::endl;
    return 0;
}
```

| 操作 | map | flat_map(排序 vector) | 胜者(本机实测, N=1M) |
|---|---|---|---|
| 查找 (随机 key) | 670ns | 213ns | flat_map(3.1x) |
| 插入 (base=20k) | 94ns | 12.9µs(O(N)移位) | map(写多更优) |
| 遍历 (每元素) | 111ns | 0.44ns | flat_map(**252x**, 连续内存) |
| 内存 (1M pair) | 38.1MB | 7.6MB | flat_map(5.0x节省) |

- `[实测]`：上表为 ch83_map 附录 E 本机实测值（GCC 13.1 -O2，TSC 2.395GHz，来源 `Examples/_ch83_map_perf.out`）。旧版"~200/~150ns、~300/~500ns、~50/~10ns/elem、~40/~16MB、遍历5x"为早期估算，已按实测校正（flat 遍历实测 252x 而非 5x；flat 内存 7.6MB 而非 16MB）。

面试: 选map还是flat_map? 读多→flat_map; 写多→map; 内存紧→flat_map
      flat_map为何快? 连续内存=Cache友好+无指针chasing


## 附录 G：C++23 特性真机汇编实证（GCC 15.3.0 实测）

> 工具链：GCC 15.3.0（MinGW-w64 x86_64-msvcrt，built by Brecht Sanders r1），`-std=c++26 -O2`。实证源码：`_asm_demo/ch08_*.cpp`，真实编译 + `objdump -d -M intel`。

### G.1 std::expected：零开销 tagged union

`std::expected<int, const char*>` 的返回对象（sret 隐藏指针 `rax`）在 `parse_digit` 中布局：

```cpp
// _asm_demo/ch08_expected_test.cpp （GCC 15.3.0 -std=c++26 -O2，实测）
std::expected<int, const char*> parse_digit(const char* s) {
    if (!s || !*s) return std::unexpected("empty");
    if (*s < '0' || *s > '9') return std::unexpected("not digit");
    return static_cast<int>(*s - '0');
}
```

关键指令（节选，`objdump -d -M intel`，demangled）：

```asm
; 失败路径：错误指针写入 [rax]（偏移0），[rax+8] 写 0（error 标记）
lea    rcx,[rip+0x98da]        ; 错误字符串地址
mov    QWORD PTR [rax+0x8],0x0 ; 偏移8 = 1字节 has_value 标记：0=error
mov    QWORD PTR [rax],rcx     ; 偏移0 = union 存错误指针
ret
; 成功路径：int 值写入 [rax]（偏移0 低32位），[rax+8] 写 1
sub    edx,0x30
mov    BYTE PTR [rax+0x8],0x1  ; has_value=1
mov    DWORD PTR [rax],edx     ; union 存 int 值
ret
```

结论：expected 是**单返回对象的 tagged union**——偏移 0 是值/错误指针的 union，偏移 8 是 1 字节 `has_value` 标志；无 vtable、无堆分配，零运行时开销（对比异常路径 ch40）。

### G.2 std::generator：堆分配协程帧

```cpp
// _asm_demo/ch08_generator_test.cpp （GCC 15.3.0 -std=c++26 -O2，实测）
std::generator<int> iota(int n) { for (int i = 0; i < n; ++i) co_yield i; }
```

`iota(int)` 入口为协程帧堆分配（非栈上）：

```asm
; iota(int) 入口：operator new(0x68=104B) 分配协程帧
mov    ecx,0x68
call   operator new(unsigned long long)   ; 堆分配 104 字节协程帧
mov    DWORD PTR [rbx+0x30],ebp           ; 帧[0x30] 存 n（上限）
mov    DWORD PTR [rbx+0x34],0x10000       ; 帧[0x34] 初始协程状态
mov    BYTE PTR [rbx+0x20],0x0            ; 帧[0x20] yield 索引初值
```

结论：`std::generator` 每次调用 `iota(n)` 都 `operator new` 一个 104 字节协程帧——**生成器有堆分配开销**，循环内高频 yield 时需警惕（对比 `std::views::iota` 的无分配惰性范围 ch77）。

### G.3 std::mdspan：本工具链不可用（诚实标注）

本 MinGW 构建的 libstdc++ **未提供 `<mdspan>` 头**：

```text
ch08_mdspan_test.cpp:3:10: fatal error: mdspan: No such file or directory
```

多维→一维偏移的地址计算（如 `a[1,2]` → `data[1*extent1+2]`）由编译器在后端完成；在无 `<mdspan>` 时可用手写下标计算等价表达（见 ch82_span）。C++23 标准已规定 `std::mdspan`，但**编译器实测支持滞后**——这正是 WG21 跟踪表（WG21/TRACKER.md）记录"标准 vs 实测"差距的价值。

### G.4 优化等级对比：-O0 / -O2 / -Os（嵌入式视角）

> 嵌入式固件普遍用 `-Os` 压缩 flash，本实证回答"零开销抽象在 `-Os` 下是否仍零开销"。
> 手法：`[[gnu::noinline]]` 强制 `parse_digit` 独立成符号，使三个等级对比的是同一函数。
> 源码：`_asm_demo/ch08_opt_expected.cpp`，编译：
> `g++ -std=c++26 -O0|-O2|-Os -c ch08_opt_expected.cpp -o ox.o`

实测函数体积与构造方式：

| 等级 | 函数体积 | 栈帧 | 构造函数调用 | 构造方式 |
|---|---|---|---|---|
| `-O0` | 182 B | 64 B `rsp` + `rbp` | 3 次 `call` | 经 value/unexpected 构造函数 |
| `-O2` | 99 B | 无 | **0** | 直接写 `[rax]`(值)+`[rax+0x8]`(has_value=1) |
| `-Os` | 74 B | 无 | **0** | 尾合并存储（最紧凑） |

`-O2` 下构造函数被彻底消除，tagged union 原地构建（零开销成立）：

```asm
parse_digit(char) @ -O2:
    mov    rax,rcx              ; rcx=隐藏 this 指针 (expected& 经隐藏指针返回)
    lea    ecx,[rdx-0x30]      ; rdx=char c; ecx=c-'0'
    cmp    cl,0x9
    ja     20                  ; 非 '0'..'9' → 跳 0x20
    movsx  edx,dl
    mov    BYTE PTR [rax+0x8],0x1  ; 原地置 has_value 标志=1 (偏移 8)
    sub    edx,0x30
    mov    DWORD PTR [rax],edx     ; 原地写值 (偏移 0)
    ret                         ; 无构造函数调用！
 20: lea    ecx,[rdx-0x61]      ; 'a'..'f' 分支: c-'a'
    ...
 50: lea    rcx,[rip+0x0]       ; "not a hex digit" 字符串地址
    mov    QWORD PTR [rax+0x8],0x0  ; has_value=0
    mov    QWORD PTR [rax],rcx      ; 错误指针存偏移 0
    ret
```

`-Os` 进一步**尾合并**了三路分支的存储序列（74 B < 99 B），对 flash 受限 MCU 最友好：

```asm
parse_digit(char) @ -Os (74 B):
    mov    rax,rcx
    lea    ecx,[rdx-0x30]
    cmp    cl,0x9
    ja     13
    movsx  edx,dl
    sub    edx,0x30
    jmp    31                  ; 尾合并到统一存储
 13: lea    ecx,[rdx-0x61]      ; 'a'..'f'
    ...
 31: mov    DWORD PTR [rax],edx     ; 统一写值
    mov    BYTE PTR [rax+0x8],0x1  ; 统一置 has_value=1
    jmp    49
 39: xor    edx,edx             ; 错误分支
    lea    rcx,[rip+0x0]
    mov    QWORD PTR [rax+0x8],rdx ; has_value=0
    mov    QWORD PTR [rax],rcx
 49: ret
```

**结论**：`std::expected` 的零开销承诺在 `-O2` 与 `-Os` 下均成立——构造函数被消除、tagged union 原地构建；`-Os` 反而最小（74 B）。`-O0`（调试/未优化）是唯一有构造函数调用开销的等级，印证"发布构建务必开优化"。

### G.5 std::ranges 零成本抽象实证

> 破除"Ranges 慢"迷思。源码：`_asm_demo/ch08_ranges_test.cpp`，编译：
> `g++ -std=c++26 -O2 -c ch08_ranges_test.cpp -o ranges.o`

**(1) `std::ranges::sort` ≡ `std::sort` 同一套 introsort**

两者最终都调用 libstdc++ 的同一实例化：

```text
void std::__introsort_loop<
    __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >,
    long long,
    __gnu_cxx::__ops::_Iter_less_iter
>(...) [clone .isra.0]
```

本例中 `sort_std` 用 `call` 引用该共享克隆，`sort_ranges` 将其内联进自身主体（GCC 启发式），但**排序内核完全相同**：阈值 `cmp rdi,0x40`（>64 元素才进快排）、插入排序尾、末趟单遍。ranges 层唯一的额外成本是 prologue 中构造 range 的 begin/end 对：

```asm
sort_ranges @ -O2 prologue:
    mov    rsi,QWORD PTR [rcx+0x8]   ; end()
    mov    rbp,QWORD PTR [rcx]       ; begin()
    lea    rdx,[rsp+0x3e]
    lea    rax,[rsp+0x3f]
    xchg   rdx,rax                   ; 在栈上构造 std::ranges::sort 的 range 参数(begin/end 对)
```

这是一次性常量开销，调用点被内联进调用者时即消失。

**(2) `std::views::filter` 谓词被内联为单条 `test`+`jne`**

`count_even` 用 `v | views::filter([](int x){ return (x&1)==0; })` 过滤偶数并求和，`-O2` 下 filter 闭包与 lambda **完全消失**，退化成与手写循环一致的紧致循环（仅 98 B）：

```asm
count_even(const std::vector<int>&) @ -O2 (98 B):
    mov    r8,QWORD PTR [rcx+0x8]   ; end()
    mov    rcx,QWORD PTR [rcx]      ; begin()
    cmp    r8,rcx
    jne    659
 659: mov    edx,DWORD PTR [rcx]    ; *it
    test   dl,0x1                   ; (x & 1) == 0 ? 偶数判定
    jne    650                      ; 奇数 → 跳过 (650: add rcx,4 取下一元素)
    add    r9d,edx                  ; 偶数 → 累加
    ...
```

**结论**：`std::ranges` 是零成本抽象——`ranges::sort` 与 `std::sort` 生成同一 introsort；`views::filter` 的谓词被编译成循环内的 `test`+`jne`，无迭代器包装、无间接调用。Ranges 的可读性提升不以运行时性能为代价。

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **LLVM/Clang（llvm.org）**：实现 `std::print` / `std::flat_map` / `std::mdspan` 等 C++23 特性（trunk）。
- **GCC 镜像（github.com/gcc-mirror/gcc）**：跟进实现。

**常见陷阱 / 最佳实践**：
- C++23 特性需编译器版本支持（Clang 17+ / GCC 13+）；`std::print` 替代 `printf` 但仍走格式化，迁移注意 locale 差异。
- `<flat_map>` 是连续存储的有序容器，查找优于 `std::map` 但插入慢于哈希。

> 交叉引用：C++11 见 [ch04](Book/part01_history/ch04_cpp11.md)；范围见 [ch82](Book/part07_stl/ch82_span.md)。

## 工业实现参考：C++23 特性的真实采用 [B: Principle]

[标准·可查证] C++23 多项特性源自工业库：
- `std::print` / `std::format` 吸收 `{fmt}`（Victor Zverovich，广泛采用的格式化库）；
- `std::ranges` 受 range-v3（Eric Niebler）影响；
- `std::expected` 借鉴 `Boost.Outcome`（Boost）；
- `std::mdspan` 来自 Kokkos（与 `LLVM`/HPC 社区协作）；
- `std::generator` / 协程被 `folly`（Facebook）等异步栈采用；
- Chromium、Qt 6 已逐步启用 C++20/23 特性。

`GCC 13.1.0` / `Clang 17` / `MSVC 19.3` 对 C++23 特性支持度不同（部分需 `-std=c++23` 与实验开关）；`constexpr` 在 C++23 进一步扩展。`fmt` 与 `range-v3` 是 `LLVM`/Chromium 构建链常见依赖。


## 相关章节（交叉引用）

- **相邻主题**：⟶ Book/part01_history/ch07_cpp20.md（第07章　C++20：量级升级）—— 编号相邻、主题接续（C++20 → C++23 演进链）。
- **相邻主题**：⟶ Book/part01_history/ch09_cpp26.md（第09章　C++26：已确定特性与方向）—— 编号相邻、主题接续（C++23 → C++26 方向）。
- **同模块**：⟶ Book/part01_history/ch01_c_history.md（第01章　C 语言遗产与 C with Classes）—— 同模块下的其他主题。
- **跨part主题**：⟶ Book/part07_stl/ch82_span.md（第82章　span 与裸数组视图）—— C++23 核心库特性 `std::span` 的演进源头，跨 part 延伸。
- **跨part主题**：⟶ Book/part07_stl/ch88_optional_variant.md（第88章　optional / expected / variant：可空与可辨别联合）—— C++23 `std::optional`/`std::variant` 增强的对应章节，跨 part 延伸。
- **跨part主题**：⟶ Book/part10_modern/ch120_coroutine_app.md（第120章 Coroutine 应用模式）—— C++23 协程应用的落地章节，跨 part 延伸。

## 叙事补遗 [J: Learning]

- **标准库之年**：`std::expected`（用值/错代替异常）、`std::flat_map`（缓存友好的有序容器）、`std::mdspan`（多维视图）、`std::print`（终于有类型安全的打印）集中交付。
- **语言层补完**：显式对象参数（deducing `this`）、多维下标、`if consteval`、`std::size_t` 字面量后缀，把 C++20 未及的边角补齐。
- **稳定节奏确立**：C++23 之后固定三年一版，并首次批量交付"上一版未及"的库特性，社区终于有了可预期的进化曲线。
## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

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

### 练习 3（难度 ★★★）

用折叠表达式写一个 `sum` 可变参数函数，计算任意个数实参之和。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
template <typename... Ts> auto sum(Ts... ts) { return (0 + ... + ts); }
int main() { std::cout << sum(1, 2, 3, 4) << '\n'; }
```

[标准] 一元左折叠 `(init + ... + ts)` 展开为 `((((0+1)+2)+3)+4)`。

</details>

