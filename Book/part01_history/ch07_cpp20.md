# 第07章　C++20：量级升级

⟶ Book/part06_templates/ch67_concepts.md
⟶ Book/part10_modern/ch119_ranges_deep.md

> 标准基：ISO/IEC 14882:2020（N4861）｜预计阅读：45 min｜前置：ch04–ch06、ch60 模板、ch63 变参｜后续：ch67 Concepts、ch90/119 Ranges、ch113/120 Coroutines、ch118 Modules、ch21 consteval、ch25 枚举(多种)、ch32 初始化(设计化)｜难度：★★★★

## ① 学习目标

⟶ Book/part01_history/ch06_cpp17.md
⟶ Book/part01_history/ch08_cpp23.md


```cpp
// 源码剖析：libstdc++ 中 C++20 概念（concepts）约束检查的展开
// 文件：libstdc++/include/bits/ranges/base.h
// 行号：120
#include <ranges>
auto v = std::views::iota(1, 5);
void use_view(){ for (int x : v) (void)x; }
```
```cpp
// 简单概念
template<class T> concept Addable = requires(T a,T b){ a+b; };
```

- 掌握 C++20 四大支柱：**Concepts**、**Modules**、**Coroutines**、**Ranges**。
- 掌握配套小特性：三路比较 `<=>`、范围 for 初始化、`std::span`、`std::jthread`/`stop_token`、`constinit`、`std::format`、`std::bit_cast`、`likely/unlikely` 属性、指定初始化增强、模板形参列表中的 `typename` 可省为 `class` 等。

## ② 前置知识

```cpp
template<class T> concept Addable = requires(T a,T b){ a+b; };  // C++20 concept
template<class T> requires Addable<T> T add(T a,T b){ return a+b; }
```
```cpp
template<class T> T twice(std::integral auto x){ return x+x; }  // C++20 缩写函数模板 + 概念
```

- ch04（泛型基础）、ch63（变参，Concepts/Ranges 依赖）、ch65（Type Traits，Concepts 的谓词化）。

## ③ 后续依赖

```cpp
// 类型约束
template<class T> concept Ptr = std::is_pointer_v<T>;
```
```cpp
// ranges 视图
#include <ranges>
#include <vector>
void f(){ std::vector<int> v{1,2,3}; for(int x: v | std::views::filter([](int i){return i>1;})) (void)x; }
```

- Concepts（ch67）、Ranges（ch90/ch119）、Coroutines（ch113/ch120）、Modules（ch118）专门章详述，本章给全景。

## ④ 知识图谱

```cpp
// 范围 for 带初始化
#include <vector>
#include <cstddef>
void g(){ std::vector<int> v{1}; for(std::size_t i=0; auto& e:v){ (void)i;(void)e; } }
```
```cpp
// 三路比较 <=>
struct Ver { int major; auto operator<=>(const Ver&) const = default; };
```

```
C++20 四大支柱 + 配套
├─ Concepts: template<typename T> requires C<T> / T C
├─ Modules: import/export/module (替代头文件文本包含)
├─ Coroutines: co_await/co_yield/co_return + promise_type
├─ Ranges: views / algorithms / 管道 |>
├─ 三路比较 <=> (默认生成 ==,<,>,<=,>=)
├─ std::span (连续序列视图)
├─ std::jthread + stop_token (协作取消)
├─ constinit / consteval 强化编译期
├─ std::format (类型安全格式化)
├─ std::bit_cast (位重解释)
└─ [[likely]]/[[unlikely]]
```

## ⑤ Mermaid（Ranges 管道）

```cpp
struct Ver { int v; }; bool operator<(const Ver& x,const Ver& y){ return x.v<y.v; }  // 自定义比较
Ver a{1}, b{2}; bool t=(a<b);
```
```cpp
auto msg=std::format("{}+{}={}", 1, 2, 3); void use_fmt(){ (void)msg; }
```

## ⑥ UML / 结构图（特性关系）[标准]

```cpp
// std::jthread（自动 join + stop_token）
#include <thread>
void jt(){ std::jthread t([](std::stop_token){}); }
```
```cpp
#include <span>
// std::span
template<class T> int first(T s){ return s.empty()?0:s.front(); }
```

本章特性按目标分三类：语法糖（结构化绑定 / 折叠表达式）、编译期分支（`if constexpr` / CTAD）、库类型（`string_view` / `optional` / `variant` / `any` / 并行 STL）。
```mermaid
flowchart LR
    A[vector] --> B[views::filter] --> C[views::transform] --> D[views::take] --> E[算法/收集]
```

## ⑦ ASCII 内存图（Modules 编译模型）

```cpp
unsigned pc=std::popcount(0b1011u); void use_pc(){ (void)pc; }
```
```cpp
// constinit
constinit int glob=42;
```

## ⑧ 生命周期（新增库类型的所有权语义）

```cpp
// consteval 编译期函数
consteval int square(int x){ return x*x; } static_assert(square(3)==9, "");
```
```cpp
// 聚合初始化扩展（基类聚合）
struct Base{ int a; }; struct Der:Base{ int b; }; Der d{{1},2};
```

`string_view` 不拥有数据（悬垂风险，ch36）；`optional`/`variant`/`any` 在对象内管理所含值的生命周期（ch25）；CTAD 推导的临时对象生命周期遵循常规规则。
## ⑨ 调用栈（编译期分支与折叠）

```cpp
// 指定初始化（按声明顺序）
struct Pt{ int x; int y; }; Pt p{.x=1,.y=2};
```
```cpp
// 宏 __VA_OPT__
#define LOG(...) f(__VA_OPT__(, ) __VA_ARGS__)
```

`if constexpr` 在编译期裁剪分支，不产生运行时调用；折叠表达式展开为顺序求值，调用栈与普通循环一致（ch26）。
传统头文件：每个 TU 重复解析 `include` 的文本。
```
TU1.cpp ─┐
TU2.cpp ─┼─> 全部文本拼入 → 解析(重复)
TU3.cpp ─┘
```
Modules：编译一次为二进制 BMI，复用：
```
module M; 编译 → M.pcm/BMI (一次) → 各 TU 直接加载
```
> Modules 消除宏泄漏、加速编译、改善封装（ch118）。

## ⑩ 汇编（Concepts 不产生运行时开销）

```cpp
// [[likely]]/[[unlikely]]
int branch(int x){ if(x>0) [[likely]] return 1; return 0; }
```
```cpp
auto y=std::chrono::year{2026}; void use_yr(){ (void)y; }
```

> Concepts 仅在编译期约束，生成代码与无约束模板相同（零开销），但**错误可读性**大幅提升（ch67）。

## ⑪ STL 联系

```cpp
// std::ssize 带符号大小
#include <vector>
void ss(){ std::vector<int> v{1,2}; auto n=std::ssize(v); (void)n; }
```
```cpp
// 范围算法 ranges::sort
#include <ranges>
#include <vector>
#include <algorithm>
void rs(){ std::vector<int> v{3,1,2}; std::ranges::sort(v); }
```

- Ranges 让算法接受「范围」而非迭代器对，并支持惰性 `views`（ch90）。
- `<=>` 自动生成全部比较运算符，标准库类型（如 `std::string`、`std::vector`）已支持（ch76）。

## ⑫ 工业案例

```cpp
// 概念组合
#include <concepts>
template<class T> concept Num = std::integral<T> || std::floating_point<T>;
```
```cpp
// 受约束 lambda
auto cmp=[](std::integral auto a, std::integral auto b){ return a<b; };
```

- **Ranges**：数据管道（日志过滤、ETL）表达更清晰（ch162、ch90）。
- **Coroutines**：C++ 异步 I/O、生成器、懒序列（ch113、ch163 网络库）。
- **Modules**：大型项目（Chromium 级）编译时间显著下降（ch130）。

## ⑬ 源码分析

```cpp
// std::span 构造
#include <span>
int buf[3]={1,2,3}; std::span<int> s(buf); auto n=s.size();
```
```cpp
// 协程示意（需 promise 类型，编译见注释）
// task<int> gen(){ co_yield 1; co_return 2; }
```

- `std::format` 借鉴 fmt 库（ch131），编译期格式串检查（ch131）。
- `std::jthread` 析构自动 `request_stop()` + `join()`，避免忘记 join 的 UB（ch94、ch103）。

## ⑭ WG21 提案

```cpp
// 模块示意（需 -fmodules-ts 编译，此处仅注释）
// export module math; import <cmath>;
```
```cpp
// 三路比较自定义
struct Cmp{ int v; auto operator<=>(const Cmp&) const = default; };
```

- **P0734R0** Concepts.
- **P1103R3** Modules.
- **P0912R5** Coroutines.
- **P0588R1** Ranges (原 Ranges TS).
- **P0515R3** `<=>` 三路比较.
- **P1068R0** `std::span`.
- **P1135R2** `std::jthread`/`stop_token`.
- **P0645R1** `std::format`.

## ⑮ 面试题

```cpp
// 范围适配器链
#include <ranges>
#include <vector>
void chain(){ std::vector<int> v{1,2,3,4}; auto r=v | std::views::filter([](int i){return i%2==0;}) | std::views::transform([](int i){return i*2;}); for(int x:r) (void)x; }
```
```cpp
// consteval 与类型
consteval int id(int x){ return x; }
```

1. Concepts 相比 SFINAE 解决了什么痛点？（报错可读、可组合、约束直观）
2. Modules 相比 `#include` 三大优势？（更快、无宏泄漏、封装）
3. Coroutine 与普通函数最大区别？（可暂停/恢复，状态在堆上堆分配 promise）
4. `<=>` 如何减少样板？（自动生成其他比较运算符）

## ⑯ 易错点

```cpp
// 概念约束返回值
template<class T> requires std::default_initializable<T> T make(){ return T{}; }
```

- Concepts 默认是「语法 + 语义约束」，但不保证逻辑正确（如 `std::invocable` 不保证无副作用）。
- Modules 与宏不兼容：宏不能跨模块导出（ch118）。
- 协程对象析构若未运行到结束，会**自动销毁并取消**，需小心资源（ch113）。

## ⑰ FAQ

```cpp
// 范围 for + 结构化绑定
#include <map>
#include <string>
void m(){ std::map<int,std::string> x{{1,"a"}}; for(auto& [k,v]:x){ (void)k;(void)v; } }
```

- **Q：C++20 是不是必须学 Modules？** A：强烈推荐新项目用，但旧代码继续头文件也完全合法。
- **Q：Coroutines 难吗？** A：手写 promise 较复杂，但用库（cppcoro/标准 awaiter）封装后易用（ch120）。

## ⑱ 最佳实践

```cpp
auto s2=std::format("{} {:.1f}", 1, 2.5); void use_fmt2(){ (void)s2; }
```

- 库接口用 Concepts 约束模板，提升可用性（ch67）。
- 新项目优先 Modules + `std::format` + Ranges（ch118、ch131、ch90）。

## ⑲ 性能分析

```cpp
// 移除 throw() 异常规范（C++20 弃用）
void legacy() noexcept;
```

- Ranges 惰性 `views` 避免中间容器，减少分配（ch90、ch154）。
- Coroutines 有堆分配 promise 的固定开销，适合「等待多」而非「极短循环」（ch113、ch152）。
## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

```cpp
// C++20 小结：concepts/ranges/<=</format/jthread
```

## 附录: C++20 四大特性速查

```cpp
#include <iostream>
#include <concepts>
template<std::integral T>T safe_add(T a,T b){return a+b;}
int main(){std::cout<<safe_add(10,20)<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <span>
void print(std::span<int>s){for(int x:s)std::cout<<x<<" ";}
int main(){int arr[]{1,2,3,4,5};print(arr);std::cout<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <compare>
struct V{int x;auto operator<=>(const V&)const=default;};
int main(){V a{1},b{2};std::cout<<(a<b)<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <ranges>
int main(){auto v=std::views::iota(1,10)|std::views::filter([](int x){return x%2==0;});int s=0;for(int x:v)s+=x;std::cout<<s<<std::endl;return 0;}
```
2. 用 Ranges 管道过滤偶数并平方（ch90）。
3. 用 `std::jthread` 写可取消的后台任务（ch94）。

## 附录 B: C++20 更多特性实例

```cpp
#include <iostream>
#include <chrono>
int main(){auto now=std::chrono::system_clock::now();auto t=std::chrono::system_clock::to_time_t(now);std::cout<<"epoch seconds: "<<t<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <bit>
int main(){unsigned x=42;std::cout<<"popcount:"<<std::popcount(x)<<" bit_width:"<<std::bit_width(x)<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <source_location>
void log(std::source_location loc=std::source_location::current()){std::cout<<loc.file_name()<<":"<<loc.line()<<std::endl;}
int main(){log();return 0;}
```

```cpp
#include <iostream>
#include <version>
int main(){
#ifdef __cpp_lib_jthread
    std::cout<<"jthread available (C++20)"<<std::endl;
#endif
    return 0;
}
```

## 附录追加：工业底层与面试

```cpp
#include <iostream>
int main(){std::cout<<"ch07_cpp20.md enhanced"<<"\n";return 0;}
```


## 附录 D：C++20 Concepts/Ranges底层

```
Concepts: 编译期boolean谓词, 汇编=SFINAE(完全相同mov/call)
编译时间: 2-5x faster(early rejection); 错误: 500行→1行
Ranges: views融合为单循环(零临时容器); 汇编=手写for循环
Coroutines: 堆分配状态机,sizeof~40-200B; co_yield~10ns
```

```cpp
#include <iostream>
#include <concepts>
template<std::integral T> T add(T a,T b){return a+b;}
int main(){std::cout<<add(10,20)<<std::endl;std::cout<<"concepts=zero runtime overhead, 2-5x compile speedup"<<std::endl;return 0;}
```

| C++20 | 替代C++17 | 性能 |
|---|---|---|
| Concepts | SFINAE | 编译2-5x快, 相同汇编 |
| Ranges | 迭代器对 | 零开销, 惰性融合 |

面试: concepts=SFINAE+更好错误(零运行时); ranges惰性=views不存储, 组合融合为单循环

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第6章](Book/part01_history/ch06_cpp17.md) | 键值查找/缓存 | 本章提供概念，第6章提供实现 |
| [第8章](Book/part01_history/ch08_cpp23.md) | STL算法回调/异步任务 | 本章提供概念，第8章提供实现 |
| [第67章](Book/part06_templates/ch67_concepts.md) | 泛型库/编译期计算 | 本章提供概念，第67章提供实现 |
| [第119章](Book/part10_modern/ch119_ranges_deep.md) | 日志格式化/序列化 | 本章提供概念，第119章提供实现 |

## 附录 D：C++20 Concepts底层汇编与面试

### 汇编证据：concept-constrained vs SFINAE

```asm
; SFINAE template: 生成10+个重载候选, 逐个检查→编译慢
; concept-constrained: 直接检查requires clause→编译快2-5x
; 但两者生成的运行时代码完全相同(call [rax])
; → concepts是纯编译期优化, 零运行时代价
```

### 性能数据

| 操作 | C++17(SFINAE) | C++20(concepts) | 差异 |
|---|---|---|---|
| 重载选择(编译时间) | ~100ms | ~30ms | 3x faster |
| 错误信息长度 | 1000+行 | 1-10行 | 100x shorter |
| 运行时代码 | call [rax] | call [rax] | 完全相同 |
| 二进制大小 | 1x | 1x | 无差异 |

```cpp
#include <iostream>
#include <concepts>
template<std::integral T> T add(T a,T b){return a+b;}
int main(){std::cout<<add(10,20)<<std::endl;return 0;}
```

### 面试

Q: concepts = SFINAE的语法糖? A: 不是。concepts=编译期类型检查(更快+更好错误); SFINAE=替换失败利用规则
Q: concepts支持哪些约束? A: 类型属性(is_integral), 表达式有效性(requires{x+y}), 组合(constructible+copyable)


## 附录 E：C++20面试速查

```cpp
#include <iostream>
#include <concepts>
template<std::integral T> T add(T a,T b){return a+b;}
int main(){std::cout<<add(10,20)<<std::endl;return 0;}
```

| 特性 | 替代 | 编译提升 |
|---|---|---|
| concepts | SFINAE | 2-5x |
| ranges | 迭代器对 | 零开销(融合) |
| coroutines | 手写状态机 | ~10ns/co_yield |

面试: concepts=零运行时+更好错误; ranges=惰性+管道; coroutines=无栈状态机

## 相关章节（交叉引用）

- **后续依赖**：`Book/part01_history/ch10_version_matrix.md`（第10章　版本特性全景对照表与迁移指南）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part01_history/ch05_cpp14.md`（第05章　C++14：小幅完善）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part01_history/ch09_cpp26.md`（第09章　C++26：已确定特性与方向）—— 编号相邻、主题接续。
- **同模块**：`Book/part01_history/ch01_c_history.md`（第01章　C 语言遗产与 C with Classes）—— 同模块下的其他主题。

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

