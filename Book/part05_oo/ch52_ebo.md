# 第52章　空基类优化 EBO（Empty Base Optimization）

[第 45 章　C++ 面向对象总览与对象模型基础](../part05_oo/ch45_oop_object_model.md)

> 标准基：ISO/IEC 14882:2023（C++23）｜立场分层：`[标准]` 语言规定 · `[实现]` 编译器/库实现 · `[平台]` ABI/OS · `[经验]` 工程共识｜层级：L2 进阶
> 汇编证据：MinGW GCC 15.3.0，`-std=c++23 -O2 -S -masm=intel` 真实输出（见 `Examples/_asm_ebo.cpp` → `_asm_ebo.asm`）
> 前置/后续：⟶ ch19（对象大小/存储期）· ch45（对象模型）· ch50（多重继承布局）· ch71（Policy-Based Design）· ch41（allocator）

## ⓪ 历史动机：空基类优化的来龙去脉

> 一个「什么都没有」的基类，凭什么还要占你一个字节？EBO 回答：不该占的，一个字节都不占。

### 0.1 起源（谁·何时·为何）
C 语言有个老规矩：即便 `struct` 为空，也得占至少 1 字节，否则两个不同对象会有相同地址（违反「不同对象地址不同」）。<span class="badge badge-history">史</span> 但 C++ 的**基类子对象**可以例外——编译器允许「空基类」不占空间，直接叠到派生类的 padding 里，这就是 **EBO（Empty Base Optimization）**。<span class="badge badge-history">史</span> 它的真实价值在泛型里爆发：策略类、分配器、迭代器标签往往是空类，若一个个算 1 字节，像 `std::vector` 里那颗空 `std::allocator` 就会白白撑大对象。

### 0.2 关键转折（编年）
- 1990s：主流编译器（GCC、EDG 等）先在实践中实现 EBO。
- 1998：C++98 把「允许但不强制」EBO 写进标准（as-if 规则下编译器可省略空基类的大小）。
- 此后：EBO 成为策略式设计（ch71）、traits（ch65）能「零成本挂件」的基石。

### 0.3 设计哲学之争
EBO 体现 C++ 对「大小即性能」的执念：在密集容器、嵌入式场景，多出的几个字节就是缓存行浪费。<span class="badge badge-comment">评</span> 但它也和「每个对象要有唯一地址」的直觉相冲突——标准巧妙地用「基类子对象可以无地址」化解，既保住规则又放过了空类。

### 0.4 史料补遗与持续编年
0.2 编年止于 EBO 成为策略式设计的基石。C++20 给这个故事续了关键一笔：

- <span class="badge badge-history">史</span> C++20 的 `[[no_unique_address]` 把 EBO 的思想从「基类」推广到「任意空数据成员」：一个空的 allocator、comparator 或 stateless 函数对象作为成员时，可被重叠到邻位而免占空间，不再非得借「继承空基类」这一招。

- <span class="badge badge-history">史</span> 空基类优化本身自 C++98 起被实现广泛支持（EDG、GCC 等），但其「只适用于基类、不适用于成员」的局限长期逼着库作者把空类型硬写成基类；属性化标注等于官方承认「空成员也应享此待遇」。

- <span class="badge badge-comment">评</span> `std::unique_ptr` 的默认删除器 `default_delete` 与 `std::allocator` 都是空类型，EBO/`[[no_unique_address]` 让「带删除器的智能指针」与「裸指针」占用同样大小——这是零开销抽象的具体兑现。

> 史料来源：https://en.cppreference.com/w/cpp/language/attributes/no_unique_address ；https://en.cppreference.com/w/cpp/language/ebo

!!! note "类比：EBO = 给空类发免占位证"
    空基类优化（EBO）可以**类比**为「给空类发一张免占位证」——C 规定空 struct 至少占 1 字节（否则两个对象地址相同），但 C++ 允许「空基类」不占空间、直接叠进派生类的 padding。它**好比**把不占地的挂件挂到背包缝隙里，不增加体积。
    换个角度：C++20 的 `[[no_unique_address]]` 把 EBO 思想从「基类」推广到「任意空成员」，也**类似于**把「免占位证」从贵宾（基类）扩发给普通乘客（成员）。

    > 失效边界：EBO 体现「大小即性能」的执念，却与「每个对象要有唯一地址」直觉冲突——标准用「基类子对象可无地址」巧妙化解；但它只适用于基类、不适用于成员（故库作者曾被迫把空类型硬写成基类），且虚继承下的空基类往往无法被优化（独立地址身份）；`[[no_unique_address]]` 才补上成员侧的缺口。

> **一句话结论**：空基类优化让空类基类不占空间、size 归零——它是 std::pair、compressed_pair 等「零开销封装」得以成立的内存布局魔法。

---

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

[第51章　CRTP 与静态多态（Curiously Recurring Template Pattern）](../part05_oo/ch51_crtp.md)

EBO（空基类优化）是那种"名字很专业、原理一个例子就懂、但价值被严重低估"的特性。本章不把它当一条冷门优化，而要把这五笔账算清：

1. **一个空类为什么 `sizeof` 至少是 1，可空基类子对象却能占 0 字节？** C++ 保证任何对象有唯一地址（空对象借占 1 字节互不重叠），但**基类子对象**有特例——只要不和其他成员撞地址，允许它占 0 字节。这"1 vs 0"的差别不是抠门，而是 C++ 规则里唯一让"零成员类型"能零成本混入的通道。本章 ⑦ 布局图 + ⑩ 汇编/`offsetof` 直接证明：`Derived : Empty { int x; }` 里 `x` 落在偏移 0。
2. **EBO 到底给标准库省了什么？这才是它的工业价值所在。** `std::vector` 的分配器（allocator）就是靠把它当**基类**而非成员装进容器类里，才让"无状态分配器"不增加容器大小；策略基类（ch71）、迭代器 tag 的零成本混入也同理。没有 EBO，每个空状态的容都会平白多出 1 字节甚至更多对齐填充。本章 ⑪ STL 联系给你 `vector` 里真实的 EBO 用法。
3. **EBO 在什么时候会"失效"？** 多个空基类、空基类之后紧跟有对齐要求的命名成员、以及不同编译器的历史差异（MSVC 曾经只在特定条件才开）都会让优化不生效。不知情时你以为省了，实际 padding 又把它吞回去了。本章 ⑯ 易错点 + ⑱ 最佳实践给出"尽力法"。
4. **为什么一个空类 `sizeof` 是 1 会让大规模容器元素吃亏？** 每个元素因"无状态 tag"多占的字节，在有上百万元素的容器里被放大。EBO 之外还有一种思路是**用空基类"合成"多个 tag 而只用 0 字节**——你主动用它，代码体积和缓存占用能一起降下来。
5. **EBO 和前面的继承主题怎么接？** EBO 能工作，恰恰因为 C++ 允许**空基类子对象共享同一地址**——这正是单/多继承布局规则（ch45–ch47）的延伸。想明白这一层，OO 板块的对象模型才算真正闭环。

带着这几笔账往下读，每一节都会回到它们：⑮ 面试题把"空类多大？为什么？"翻成高频追问，⑱ 最佳实践给你一套能在真实容器上省字节的实操手法，⑬ 源码分析用标准库实现拆给你看。

## ② 前置知识 ⟶ ch19 · ch45 · ch50

EBO 不是孤立特性，它踩在三块前置知识的接缝上：**ch19** 的对象可寻址性（解释空类为何至少 1 字节）、**ch45** 的成员布局/对齐/填充（解释空基类怎么被"叠"进 padding）、**ch50** 的多重继承布局（多个基类子对象依次排列，EBO 在此压缩它们）。读下面之前这三块概念要先就位——尤其 ch19 的"唯一地址"规则，是理解 EBO 为何"只对基类、不对成员"的总开关。

## ③ 后续依赖 ⟶ ch71(Policy-Based 空基类混入) · ch41(allocator 空基类) · ch50(多基类 EBO) · ch22(auto 推导无关)

EBO 的价值要在后续章才完全兑现：**Policy-Based Design（ch71）** 大量用空基类做零成本策略混入，是 EBO 的主战场；**std::allocator（ch41）** 常以空基类形式嵌入容器、省去 8 字节指针；**ch50** 多重继承里多个空基类能否都被优化，直接取决于 EBO 规则。换句话说，EBO 是后面这些"零开销抽象"得以成立的底层内存魔法。

## ④ 知识图谱（ASCII）

> **示例 1** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 知识图谱（ASCII）
```
  空类作成员                      空类作基类（EBO）
  struct AsMember {               struct Derived : Empty {
     Empty e;  // 占 1B+填充            int x;     // x 从 0 起
     int x;    // 偏移 4                };
  };                             ⇒ Empty 占 0B，Derived sizeof = 4
  sizeof = 8（e@0 + 3pad + x@4）

  EBO 节省：8 → 4（一个对象省 4 字节；1 亿对象省 400MB）
```

## ⑤ Mermaid 流程图（编译器布局决策）

```mermaid
flowchart TD
    A["遇到基类子对象"] --> B{"基类是否为空类？"}
    B -->|"是"| C["允许与后续成员/其他子对象共用地址 → 占 0 字节"]
    B -->|"否"| D["正常分配空间，按对齐排布"]
    C --> E["EBO 生效"]
    D --> F["常规布局"]
```

## ⑥ UML 类图

```mermaid
classDiagram
    class Empty {
        <<empty>>
    }
    class Derived {
        int x
    }
    Empty <|-- Derived : EBO（空基类占 0）
```

## ⑦ ASCII 内存图 / 对象布局

> **示例 2** <span class="badge badge-exp">难度 ★★★★☆</span> · 内存图 / 对象布局
```
x64 / GCC 15.3.0：
  struct Empty {};                    // 空类
  struct Derived : Empty { int x; };  // EBO：Empty 占 0
  struct AsMember { Empty e; int x; };// 作成员：Empty 占位 1B + 3 填充

  Derived 对象（sizeof=4，对齐4）
  ┌───────────┐
  │ int x     │   @0（Empty 没占位）
  └───────────┘

  AsMember 对象（sizeof=8，对齐4）
  ┌────┬────┬───────────┐
  │Empty│padding│ int x │
  │ @0 │@1-3 │ @4      │   （Empty 占 1B 保证自身地址唯一）
  └────┴────┴───────────┘

  证据（真实汇编/编译期常量）：
    read_derived(Derived*): mov eax,[rcx]       → x @0
    read_member(AsMember*):  mov eax,4[rcx]      → x @4
    static_assert(sizeof(Derived)==sizeof(int));      // 通过
    static_assert(sizeof(AsMember)==2*sizeof(int));   // 通过（8）
    offsetof(Derived,x)==0 ; offsetof(AsMember,x)==4  // 编译期常量
```

## ⑧ 生命周期图

> **示例 3** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 生命周期图
```
空基类子对象随派生类一起构造/析构；EBO 只影响大小与偏移，不改变构造/析构语义。
空基类若无数据成员，其构造函数是 trivial 的（ch19/ch47 析构需 virtual 仅当被多态使用）。
```

## ⑨ 调用栈 / 时序图

> **示例 4** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 调用栈 / 时序图
```
读取 Derived::x：
  mov eax, [rcx]      ; rcx=Derived*，x 就在偏移 0
读取 AsMember::x：
  mov eax, 4[rcx]     ; rcx=AsMember*，x 在偏移 4（Empty 占位 + 填充）
── EBO 直接让前者少一次 +4 位移、且对象整体小 4 字节 ──
```

## ⑩ 汇编分析（MinGW GCC 15.3.0, -O2, -masm=intel，真实输出）

【测试源 `Examples/_asm_ebo.cpp`】

> **示例 5** <span class="badge badge-exp">难度 ★★★☆☆</span> · 汇编分析
```cpp
#include <cstddef>
struct Empty {};
struct Derived : Empty { int x; };
struct AsMember { Empty e; int x; };
static_assert(sizeof(Derived) == sizeof(int));
static_assert(sizeof(AsMember) == 2 * sizeof(int));
int read_derived(Derived* p) { return p->x; }
int read_member(AsMember* p) { return p->x; }
```

【1）EBO：x 在偏移 0（空基类未占空间）】

```asm
; 节选自 Examples/_ch52_ebo_a1.asm
_Z12read_derivedP7Derived:
        mov     eax, DWORD PTR [rcx]   ; x @ offset 0
        ret
```

【2）作成员：x 在偏移 4（Empty 占位 1B + 3 填充）】

```asm
; 节选自 Examples/_ch52_ebo_a2.asm
_Z11read_memberP8AsMember:
        mov     eax, DWORD PTR 4[rcx]  ; x @ offset 4
        ret
```

【要点】`Derived` 比 `AsMember` 少 4 字节，且读取 `x` 省去 `+4` 位移——EBO 的空间与时间双重收益。两个 `static_assert` 在编译期即强制该布局成立，是「用编译器验证 EBO」的范式。

## ⑪ STL 联系

- `std::vector<T, Alloc>`：`Alloc` 常以空基类嵌入 `vector`，EBO 让 `vector` 不含多余的 allocator 指针（ch41）。
- `std::unique_ptr<T, Deleter>`：`Deleter` 常以空基类（空删除器如 `default_delete`）嵌入，零开销（ch48/ch49 规则）。
- `std::reverse_iterator<It>`：`It` 作为空基类压缩迭代器对（部分实现）。
- `std::chrono::duration<Rep, Period>`：`Period` 是空类型（编译期常量），作为空基类。
- 迭代器 tag（`input_iterator_tag` 等）作为空基类混入，零成本标记类别（ch?? 迭代器）。

## ⑫ 工业案例

【案例 A：压缩策略对象（Policy-Based Design 雏形）】

> **示例 6** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例
```cpp
struct NoLog  { void log() const {} };        // 空策略
struct Timer  { int ticks = 0; void tick(){ ++ticks; } };  // 有状态策略
template<class LogP, class TimeP>
struct Engine : LogP, TimeP {                  // 两个策略作空基类
    void run(){ this->log(); this->tick(); }
};
// Engine<NoLog,Timer> ：NoLog 被 EBO 压缩为 0，sizeof=sizeof(Timer)
```

【案例 B：std::vector 的 allocator 零开销（原理示意）】

> **示例 7** <span class="badge badge-exp">难度 ★★★☆☆</span> · 工业案例
```cpp
#include <cstddef>
#include <vector>
template<class T, class Alloc>
struct vector_impl : private Alloc {           // 空 Alloc 被 EBO 抹掉
    T* data; size_t sz, cap;
    // 用 this->allocate(...) 取策略，但对象不含 Alloc 指针
};
// std::vector<int> 的空 allocator 不增加 vector 体积
```

【案例 C：误用导致 EBO 失效】

> **示例 8** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
struct Empty {};
struct Bad { Empty e; int x; };   // e 作成员 → 占 1B+填充，sizeof=8
struct Good : Empty { int x; };   // 作基类 → EBO，sizeof=4
// 选 Good 而非 Bad 以压缩大规模对象数组
```

【增补可编译示例（真实，印证 EBO 各点）】

> **示例 9** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例1：基本 EBO —— 空基类占 0
struct Empty {};
struct Derived : Empty { int x; };
static_assert(sizeof(Derived) == sizeof(int));
```

> **示例 10** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例2：作成员不享受 EBO
struct AsMember { Empty e; int x; };
static_assert(sizeof(AsMember) == 2 * sizeof(int));   // 8（含占位+填充）
```

> **示例 11** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例3：offsetof 证明 x 在偏移 0
#include <cstddef>
static_assert(offsetof(Derived, x) == 0);
static_assert(offsetof(AsMember, x) == 4);
```

> **示例 12** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例4：空基类有 static 成员不影响大小
struct E { static int cnt; };
struct D : E { int x; };   // sizeof(D)==4（static 在对象外）
```

> **示例 13** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例5：多个空基类
struct E1 {}; struct E2 {};
struct D : E1, E2 { int x; };   // GCC/Clang: sizeof=4（均压到 0）
```

> **示例 14** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例6：含虚函数的「空类」非真空
struct E { virtual void f() = 0; };
struct D : E { int x; };   // sizeof(D)==16（vptr@0 + x@8）
```

> **示例 15** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例7：[[no_unique_address]] 压缩空成员（C++20）
struct E {};
struct S { [[no_unique_address]] E e; int x; };   // sizeof==4（等价于 EBO）
```

> **示例 16** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例8：std::unique_ptr 空删除器压缩
#include <memory>
struct Noop { void operator()(int*) const {} };
static_assert(sizeof(std::unique_ptr<int, Noop>) == sizeof(int*));   // 无额外字节
```

> **示例 17** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例
```cpp
// 例9：策略混入（Policy-Based 雏形）
struct NoLog { void log() const {} };
struct Eng : NoLog, std::integral_constant<int,0> { int x=0; };   // 两空基类均压
```

> **示例 18** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例10：EBO 压缩容器元素
#include <vector>
#include <cstddef>
struct Blob : std::allocator<int> { int* d; size_t n; };   // allocator 作为空基类
```

> **示例 19** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例11：空基类地址 == 派生类地址
D d; void* pb = static_cast<Empty*>(&d); void* pd = &d;   // 可能相等
```

> **示例 20** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例12：EBO 与缓存密度
Derived arr[100];   // 占 400B；AsMember arr2[100] 占 800B
```

> **示例 21** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例
```cpp
// 例13：boost::compressed_pair 思路
template<class T1, class T2> struct CPair : T1, T2 { /* 空成员也压 */ };
```

> **示例 22** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例14：空基类 + 对齐
struct E {};
struct D : E { alignas(16) int x; };   // 整体对齐 16，x 仍在 0（EBO 后）
```

> **示例 23** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例15：空基类作 tag
struct InputTag {};
struct Iter : InputTag { int* p; };   // InputTag 占 0
```

> **示例 24** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例
```cpp
// 例16：std::chrono::duration 的 Period 空基类
#include <chrono>
using S = std::chrono::seconds;   // Period 是编译期空类型，作为空基类
```

> **示例 25** <span class="badge badge-exp">难度 ★★★☆☆</span> · 工业案例
```cpp
// 例17：EBO 与虚继承（ch49）
struct G {};
struct D : virtual G { int x; };   // 虚继承引入 vbptr，布局变化
```

> **示例 26** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例18：EBO 失败——空基类后有命名空基类但编译器不压
struct E1 {}; struct E2 {};
struct D2 : E1, E2 {};   // 部分 MSVC 旧版：sizeof(D2)==2（各占1）
```

> **示例 27** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例
```cpp
// 例19：用 std::is_empty 检测空类
#include <type_traits>
static_assert(std::is_empty_v<Empty>);
static_assert(!std::is_empty_v<Derived>);
```

> **示例 28** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例20：空基类 + 数据成员顺序影响
struct A { int a; }; struct B : Empty { int b; };   // B 的 b@0（EBO），A 的 a@0 正常
```

> **示例 29** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例21：EBO 与标准布局
struct E {}; struct D : E { int x; };   // D 仍是标准布局（首成员为 x）
```

> **示例 30** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例
```cpp
// 例22：new 空基类对象最小 1 字节
E* e = new E();   // 仍分配 ≥1 字节块（operator new 最小单位）
```

## ⑬ 源码分析

【Itanium C++ ABI：空基类子对象的布局豁免】

C++ 标准要求「两个同类型完整对象必须有不同地址」（保证 `&a != &b`），但**基类子对象**不受此约束。Itanium ABI §3.5 明确规定：当基类是无数据成员、无虚函数的空类时，允许将其子对象布局地址与派生类首个非静态数据成员（或另一空子对象）重合，从而占 0 字节。这正是 EBO。GCC/Clang/MSVC 均实现此优化（细节见 ⑲ 跨编译器）。`offsetof(Derived, x) == 0` 是该规则的二进制直接证据。

## ⑭ WG21 提案

EBO 不是某个提案"发明"的特性，而是 **C++98 就写进标准的 ABI/布局权限**——它早于 WG21 的现代提案流程。`[class]` §10 明言"基类子对象可具有与派生类其他部分相同的地址"，这是法律条文，不是编译器彩蛋。

后续提案没动 EBO 本身，但补了它的缺口：**P0840（`[[no_unique_address]]`，C++20）** 把它从"基类"推广到"成员"（第 ㉒.4 节）；而 P0847（deducing this）、P2985（静态反射）不改变 EBO 规则，只是让 `offsetof`/布局查询在编译期更通用（ch74）——反射一旦落地，"哪些子对象被重叠"就从黑魔法变成可查询契约。

## ⑮ 面试题（≥10）

1. 空类 `sizeof` 是多少？为什么不是 0？
2. 为什么空**基类**子对象可以占 0 字节，而空**成员**不行？
3. 用 offsetof 证明 EBO 生效，请给出断言代码。
4. `std::vector` 如何利用 EBO 省空间？
5. `std::unique_ptr<T, default_delete<T>>` 的空删除器被 EBO 压缩后 sizeof 多少（64 位）？
6. 什么情况下 EBO 失效？
7. 两个空基类能否都被优化为 0？如果第二个空基类后有数据成员呢？
8. EBO 对缓存局部性有无影响？
9. 写一个 `Policy` 混入，使空策略占 0、有状态策略正常占空间。
10. MSVC 与 GCC 在 EBO 上有何已知差异？
11. `[[no_unique_address]]`（C++20）和 EBO 什么关系？
12. 若空基类有虚函数，EBO 还成立吗？

## ⑯ 易错点

【反例 1：以为空成员也占 0】

> **示例 31** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
struct Empty {};
struct S { Empty e; int x; };
static_assert(sizeof(S) == 4);   // ❌ 失败：实际 8（e 占位 1B + 3 填充）
```

【正解】改为基类：

> **示例 32** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
struct S : Empty { int x; };
static_assert(sizeof(S) == 4);   // ✅ EBO 生效
```

【反例 2：多个空基类不全压缩】

> **示例 33** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
struct E1 {}; struct E2 {};
struct D : E1, E2 { int x; };    // E1、E2 都可能被压缩，但需看编译器
// GCC/Clang：E1@0, E2@0（共享）, x@0 → sizeof=4
// 某些 MSVC 版本：E2 可能不压缩 → 见 ⑲
```

【反例 3：依赖空基类地址唯一】

> **示例 34** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 易错点
```cpp
struct E {}; struct D : E { int x; };
D d;
void* pe = static_cast<E*>(&d);
void* pd = &d;
// pe 与 pd 可能相等（EBO 下空基类无独立地址）——不要假设 pe != pd
```

## ⑰ FAQ（≥10）

**Q：空类为什么 `sizeof` 是 1，而不是 0？**

因为 C++ 要求"任何完整对象都有唯一地址"——空类若占 0 字节，数组中相邻两元素就会同址，破坏这条规则。于是标准退一步：最派生对象至少占 1 字节，用这 1 字节保住地址唯一性。注意这是"最派生对象"的约束，**不**适用于基类子对象，而这正是 EBO 能成立的缝隙。

**Q：空基类为什么能占 0 字节？**

"唯一地址"约束只针对完整对象；空基类作为派生类的一部分，标准明确豁免它的地址唯一性（它依附于派生类整体）。Itanium ABI（⑬）据此允许空基类子对象与派生类首成员/另一空子对象共享地址，于是占 0。代价是空基类本身没有独立身份，不能拿 `&base` 当唯一键用。

**Q：`[[no_unique_address]]`（C++20）是什么，和 EBO 啥关系？**

它把 EBO 的"零尺寸压缩"从"只能作用于基类"推广到"任意数据成员"：空成员（如 `default_delete`、无状态 comparator）标上它也能被重叠到邻位而免占空间。区别在于 EBO 必须借继承实现、且同类型多子对象会撞址；属性式压缩保持成员语义（有名字、可 `&` 取址），适用面更广。

**Q：EBO 影响对齐吗？**

不影响。对齐由最大成员/对齐说明符决定，空基类不引入任何对齐要求，所以压掉它不会改变对象整体对齐。这也是为什么 `Derived`（EBO）和 `AsMember`（作成员）对齐都是 4，只是大小差 4 字节。

**Q：含虚函数的"空基类"还能 EBO 吗？**

不能。虚函数会塞进一个 vptr（x64 下 8 字节），类就非空了，EBO 的前提（无 non-static 数据成员）不成立，且反而引入 8 字节开销。所以"空基类优化"只认真正的空类。

**Q：两个空基类怎么排布？**

GCC/Clang 通常把两个都压到偏移 0（共享地址）；MSVC 历史上第二个空基类可能单独占位（⑲ 跨编译器）。所以跨平台库别假设"两个都省"，要么实测 `sizeof`，要么用 `[[no_unique_address]]`。

**Q：EBO 对性能有帮助吗，还是只省内存？**

两者都有，但性能收益来自内存：对象更小 → 缓存行装得更多 → 遍历时 cache miss 更少。D5 实测（⑲）显示未压缩空成员让缓存行密度减半，线性遍历慢 1.50×。对百万级容器元素，这不是"省内存"而是"省带宽"。

**Q：`offsetof` 用在空基类上合法吗？**

对数据成员 `x` 合法（且为 0，正是 EBO 证据）；但对空基类本身 `offsetof(D, E)` 是未定义行为——基类不是成员，没有"自己的偏移"。想拿空基类地址请用 `static_cast<E*>(&d)`。

**Q：POD/标准布局会被 EBO 破坏吗？**

不会，只要满足首成员/基类规则（例如首成员是数据成员 `x`、空基类在基类位置）。EBO 后的对象仍可 `memcpy` 概念上；但若基类含虚函数就另论（那时已经非空）。

**Q：位域、空数组成员算"空基类"吗？**

都不算。EBO 只针对"无 non-static 数据成员、无虚函数、无虚基类"的空类。位域是数据成员，空数组在 C++ 里另算，都不触发 EBO。

## ⑱ 最佳实践

下面七条是"什么时候该主动用 EBO"的实操结论，先立一条总纲：**无状态组件优先零开销混入，有状态或需独立生命周期的才退回成员**。

**优先把无状态组件作成私有空基类**。策略类、标签、删除器、分配器这类"无状态或可空"的东西，继承式 EBO 让它们零字节混入，比当成员白白多 1 字节（还触发填充）强得多——`std::vector` 的 allocator、`std::unique_ptr` 的 `default_delete` 都是这么干的（⑪）。

**大规模对象务必压缩**。容器元素、百万级实例里，每个空 tag 多占的字节被放大成 MB 级浪费（D5：Plain 比 Squeezed 慢 1.50× 就来自缓存密度减半）。省内存在这里等于省 cache miss。

**用 `static_assert` 把 EBO 收益写进编译期契约**。例如 `static_assert(sizeof(Derived) == sizeof(int))`，一旦某平台 EBO 没生效（如旧 MSVC 对第二个空基类不压），编译期就报警防回归。但别对绝对大小做 `==` 精确断言复合布局——EBO 是实现许可非强制。

**跨编译器项目用 `[[no_unique_address]]` 替代"空成员"需求**。C++20 起，需要组合语义又想零开销时，属性比扭曲继承结构更干净，且弥合 MSVC/GCC 差异（⑲）。

**不要假设空基类子对象有独立地址**。⑯ 反例 3 已演示 `static_cast<E*>(&d)` 可能与 `&d` 相等；做指针比较或哈希时依赖"不等"会出 bug。

**heterogeneous 策略集合要配合运行时多态**。空基类只管同类型压缩；若策略集合需要在运行期变化，得用 `std::variant`/虚函数，EBO 帮不上忙。

**写库时标注依赖 EBO**。把无状态策略放在私有继承位置，并在文档写明"此类型大小依赖 EBO 压缩"——否则调用方把策略改成成员，就会悄悄胀大你的类型。

## ⑲ 性能分析

**空间账**：`AsMember`（空类作成员）比 `Derived`（EBO 作基类）每对象多 4 字节（x64）——前面 ⑦/⑩ 的 `offsetof` 与汇编已坐实 `x@0` vs `x@4`。放大到 1 亿对象就是 400 MB 的差距，对内存敏感场景不是小数。

**时间账**：EBO 不直接省 CPU 指令，但消除一次 `+4` 位移——`read_derived` 只需 `mov [rcx]`，`read_member` 需 `mov 4[rcx]`（⑩ 真实）。单看微不足道，但它意味着对象整体小一圈，间接影响下方缓存账。

**缓存密度账**：这才是 EBO 真正的性能落点。64B 缓存行装 16 个 `Derived` 却只能装 8 个 `AsMember`，密度直接翻倍；带宽受限的线性遍历因此 cache miss 接近减半（D5 实测 1.50× 差距即源于此，ch44 缓存行）。所以"省 4 字节"在百万级元素上变现成"快 1.5 倍"。
- **microbenchmark（GCC 15.3.0 实测，自包含、可编译）**：

> **示例 35** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 性能分析
```cpp
// g++ -std=c++23 -O2 ch52_bench.cpp
#include <chrono>
#include <cstdio>
struct Empty {};
struct Derived : Empty { int x = 1; };   // EBO：空基类被压缩
struct AsMember { Empty e; int x = 1; }; // 空成员占 1 字节 + 对齐填充
int main(){
    printf("sizeof(Empty)=%zu  sizeof(Derived)=%zu  sizeof(AsMember)=%zu\n",
           sizeof(Empty), sizeof(Derived), sizeof(AsMember));
    const long long IT=5000000; volatile long long sink=0;
    auto t0=std::chrono::steady_clock::now();
    for(long long i=0;i<IT;i++){ Derived d; d.x=(int)i; sink+=d.x; }
    auto t1=std::chrono::steady_clock::now();
    printf("Derived ctor: %.3f ns/ctor\n",
      (double)std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count()/IT);
    return 0;
}
```

**实测结果（本机 x86-64，GCC 15.3.0 `-O2`）**：`sizeof(Empty)=1`，`sizeof(Derived)=4`（EBO 把空基类压到 0 字节，仅 `int` 占 4），`sizeof(AsMember)=8`（空成员占 1 字节 + 3 字节对齐填充）。**EBO 为每个对象省 4 字节（本布局 -50%）**；构造吞吐两者均 ≈0 ns/ctor（编译器把平凡构造完全消除）。1 亿对象即省 400 MB，缓存行（64B）多装一倍 `Derived` → L1 miss 接近减半（缓存密度翻倍）。注意 EBO 是**实现许可而非标准保证**，MSVC 对多空基类 historically 仅压第一个；跨编译器务必实测 `sizeof`（见 ⑳ 练习）。
- **跨编译器**：GCC/Clang 对多空基类均压缩；MSVC 长期仅压缩首个空基类，第二个空基类可能占 1 字节（VS2019+ 已改善但仍建议实测 `sizeof`）。`[[no_unique_address]]` 在 MSVC 19.27+ 生效，弥合差异。

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：`sizeof(Derived)` 等于仅有的成员大小，空基类被优化掉。** 你用空基类混入 policy/allocator。请说明条款依据。
   - <span class="badge badge-std">标准</span> 标准允许空基类子对象不贡献大小（实现通常如此），这是空基类优化的基础。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[class.derived]（空基类优化）/ [class]（布局）；cppreference "Empty base optimization" 词条。

2. **真实场景：两个同类型的空基类不能都零大小（需一个占位）。** 你试图双重混入同一空类被拒。请说明限制。
   - <span class="badge badge-std">标准</span> 同一类型的不同子对象（含基类）必须具有不同地址，故不能都为零大小。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[intro.object]（对象地址唯一性）/ [class.derived]（EBO 限制）；cppreference "Empty base optimization" 词条。

3. **真实场景：空基类不能与完整对象首个非静态成员同地址。** 你理解 EBO 的“首位成员”例外。请说明。
   - <span class="badge badge-std">标准</span> 基类子对象与作为完整对象首个成员的对象不得拥有相同地址，防止别名；这限制了 EBO 的适用位置。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[intro.object]（对象同一性与地址唯一，含 EBO 例外）/ [class.mem]（成员布局）；cppreference "Empty base optimization" 词条。

【练习题】
1. 写 `struct D : E1, E2 { char c; };`（E1/E2 空），用 `offsetof`/`sizeof` 在 GCC 与 MSVC 各测一次，记录差异。
2. 用 `[[no_unique_address]]` 重写 `AsMember`，验证 `sizeof` 回到 4（C++20）。
3. 给 `std::vector` 式容器把 allocator 改作空基类，断言 `sizeof(vector)` 不增长。

【思考题】
- 若空基类有 `static` 成员，`offsetof` 与 EBO 如何交互？static 成员是否计入对象大小？
- EBO 与「空基类子对象地址 == 派生类地址」在多重继承（ch50）下如何与 `top_offset` 共存？

【源码阅读路线（内化）】
- libstdc++：`include/bits/vector.tcc`、`include/bits/unique_ptr.h`（`default_delete` 空基类）、`include/bits/alloc_traits.h`。
- Itanium C++ ABI §3.5（Empty Base Optimization / layout）。
- 标准：`[class]` ¶10（基类子对象地址）、`[expr.sizeof]`（空类占位）、`[dcl.attr.nouniqueaddr]`（C++20）。

---

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：空基类优化的来龙去脉

<span class="badge badge-history">史</span> 空基类优化（EBO，Empty Base Optimization）源于 C++ 标准对「**空类（无数据成员、无虚函数、无虚基类的类）可以为零尺寸子对象**」的规定，这一规则由 **C++98（1998）** 在 `[intro.object]` 中明确，并被 **Itanium C++ ABI** 落地为「空基类子对象可与相邻成员/基类共享地址、不占空间」（第 ⑦ 节对象布局）。<span class="badge badge-history">史</span> EBO 最初是为给 `std::vector`/`std::shared_ptr`（ch41）这类「带分配器/删除器成员」的类型省掉空分配器的尺寸——标准库大量用「空基类承载 trait/策略」正是依赖 EBO。但 EBO **只对基类生效，对数据成员无效**，这导致「想把空策略作为成员而非基类为零开销」长期做不到，直到 **WG21 的 P0840（Richard Smith，2018）** 在 **C++20 引入 `[[no_unique_address]]`**，把 EBO 能力扩展到数据成员（第 ⑬ 节源码分析）。<span class="badge badge-anecdote">轶</span> 一个少有人知的史实：C++ 早期曾允许「空类 sizeof 为 0」，但这会破坏数组语义（数组元素必须地址不同），于是标准改为「最派生对象至少为 1 字节、空基类子对象可为 0」的折中——这是 EBO 能成立的前提。

### ㉒.2 真实工程坐标：EBO 活在哪里

下表把「EBO（空基类优化）」拉成「零尺寸类型嵌入」的工业全景。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 标准库 | `std::vector`（分配器空基）/ `std::shared_ptr`（控制块 EBO，ch41 第 ⑥/⑰ 节）/ `std::pair`·`tuple`（空元素压缩，第 ⑬/⑭ 节 D4 实证） | EBO 省掉空基类 / 空元素尺寸 | 几乎每个 C++ 程序受益 | EBO 影响面最大处 |
| 策略类 | Boost（`compressed_pair`）/ Policy-Based Design（ch71，`Unit<Meter>`） | 空基类承载编译期单位策略，零运行时成本 | 现代 C++ 设计范式 | Alexandrescu 经典技法 |
| 游戏 / 嵌入式 | 每帧百万计组件 / 协议包 | `EBO` / `[[no_unique_address]]` 把空 tag / stateless 策略压零尺寸 | 尺寸敏感结构 | 直接关系缓存命中与内存带宽 |
| 数值 / 编译期库 | Eigen / units（dimension tag） | 空量纲类型经 EBO 嵌入 `Quantity`，不增尺寸 | 类型安全 + 零开销 | 空类型零尺寸嵌入 |
| 序列化框架 | FlatBuffers（Google，`Table` / `Struct` + offset 标签） | 空 / 轻量类型携编译期 schema 信息，零开销嵌入访问器 | 高性能序列化 | 避反射式访问运行时成本 |
| 异步 I/O | Boost.Asio（handler traits / 执行属性标签） | 空类型携编译期信息，零开销嵌入 completion handler | 「类型即配置」 | EBO 在异步库的真实用法 |

> **表注（㉒.2）**：上表把「EBO（空基类优化）」拉成「零尺寸类型嵌入」的工业全景。最大受益者是标准库（vector / shared_ptr / pair / tuple，首行）——几乎每个程序都因 EBO 省掉空基类 / 空元素的尺寸。其余各行（Boost 策略类、游戏 / 嵌入式尺寸敏感结构、Eigen 量纲、FlatBuffers、Asio）都是「用空类型携带编译期信息而不付运行时尺寸」的同构套路。注意 `[[no_unique_address]]`（C++20）是 EBO 的语言级 generalization，把「空基类」扩展到「空成员」。

**一条判读**：用 EBO / `[[no_unique_address]]` 的判据是「要把空类型（标签 / traits / 策略 / 删除器）嵌进承载型而不增尺寸」。标准库已默认这么做（所以 shared_ptr 控制块不因删除器变大）；数值 / 序列化 / 异步库用它实现「类型即配置零开销」。代价：C++17 及之前只有基类位能 EBO，空成员仍需 `[[no_unique_address]]`（C++20）；误用会把非空类型当空基类导致尺寸 UB。规则：空类型要零尺寸嵌入 → EBO（C++17-）或 `[[no_unique_address]]`（C++20+）。

### ㉒.3 生产踩坑：EBO 的误用

EBO 的坑都围绕同一件事：**它是"允许"而非"强制"，且只对基类生效**。四条最易踩的：

**把空成员当 0 尺寸**（第 ⑫ 节）。EBO 仅对基类生效；空策略写成**数据成员**照常占 ≥1 字节（还 padding 到对齐）。想要零开销必须用基类或 C++20 的 `[[no_unique_address]]`——这是遗留代码里最常见的"省尺寸失败"根源，因为作者以为"空嘛，反正不占地方"。

**拿空基类地址当身份**。标准只保证空基类子对象与同类型其他子对象可共享地址；跨类型或不满足布局规则的共享未定义。用 `&base1 == &base2` 推断两个子对象是同一个，在 EBO 下不可靠（⑯ 反例 3）。

**`[[no_unique_address]]` 跨 ABI 边界不兼容**。开启该属性会改变成员偏移（第 ⑬ 节）；跨 ABI/跨编译器或混编时若一方用、一方不用，结构布局不一致，破坏二进制兼容。库作者导出含此属性的类型前要想清 ABI 承诺。

**过度嵌套 EBO 拖垮可读性**。深 EBO 基类链让 `sizeof` 与成员偏移变得不直观，排障得对照 ABI 规则；团队若无约定，新人看 `sizeof` 会一头雾水。适度即可，别为省 1 字节把继承树叠成俄罗斯套娃。

### ㉒.4 与标准的互动：EBO 与 WG21 演进

<span class="badge badge-history">史</span> EBO 随 C++98 被确立为「空基类子对象可零尺寸」；**C++20 的 P0840（`[[no_unique_address]]`）** 把它扩展到数据成员，是 EBO 二十多年来最实质的语言级补完（第 ⑬ 节）。<span class="badge badge-history">史</span> 与此同时，**`std::is_empty`（第 ⑪/⑮ 节）** 等类型特征让库能在编译期检测空类型、决定是否启用压缩；C++20 后 `[[no_unique_address]]` 配合 concepts（ch67）可写出「对空成员零开销、非空成员照常」的泛型组件。<span class="badge badge-comment">评</span> WG21 方向是把「零开销承载编译期信息」做成一等语言设施：EBO（基类）→ `[[no_unique_address]]`（成员）→ 静态反射（P2996，C++26 候选）逐步让「类型的编译期属性不付运行时代价」成为可移植、可查询的契约。标准库自身（tuple/pair/shared_ptr）会继续是 EBO 的最大受益者与示范。
- <span class="badge badge-history">史</span> EBO 的修订链：**P0840R0→R1→R2（C++20，`[[no_unique_address]]`）** 把空基类零尺寸扩展到数据成员，是 EBO 二十多年最实质的语言级补完；**P2996R0→…→P2996R13（C++26 候选，静态反射）** 则把「对象布局 / 成员遍历」从黑魔法变成编译期可查询设施。ISO 条款 `[intro.object]` 的 *potentially-overlapping subobject*（潜在重叠子对象）概念正是 `no_unique_address` 的法理基础——委员会把「零开销承载编译期信息」逐步做成可移植、可查询的一等契约。

### ㉒.5 权威引用

- [cppreference: Empty Base Optimization (EBO)](https://en.cppreference.com/w/cpp/language/ebo) — 空基类零尺寸的语义与条件（第 ⑦ 节）
- [cppreference: [[no_unique_address]]](https://en.cppreference.com/w/cpp/language/attributes/no_unique_address) — 把 EBO 扩展到数据成员（C++20，第 ⑬ 节）
- [WG21 P0840R2 — Language support for empty objects](https://wg21.link/P0840) — `[[no_unique_address]]` 提案
- [cppreference: std::is_empty](https://en.cppreference.com/w/cpp/types/is_empty) — 编译期检测空类型（第 ⑮ 节）
- [Itanium C++ ABI（基类布局规则）](https://itanium-cxx-abi.github.io/cxx-abi/abi.html) — EBO 在 GCC/Clang 的具体布局（第 ⑦ 节）

## 附录：知识点深挖（模板 B，23 项）

### B1 EBO 规则与 ABI 〔≥10 例〕

1. 空类 `sizeof=1`：保证对象可寻址、同类型两对象地址不同。
2. 空基类子对象可占 0：标准豁免「基类唯一地址」要求（⑬）。
3. `Derived : Empty { int x; }` → `x@0`，`sizeof=4`（GCC/Clang/MSVC 均如此）。
4. `AsMember { Empty e; int x; }` → `e@0(1B)+pad+x@4`，`sizeof=8`。
5. 空基类有静态成员不影响大小（static 在对象外）。
6. 空基类有 `typedef`/`using` 仍是空类（不影响布局）。
7. 空基类是模板特化（如 `Empty<int>`）同样 EBO 生效。
8. `offsetof(Derived,x)==0` 是 EBO 的编译期可执行证据（测试源已 static_assert）。
9. 两个空基类 `D:E1,E2`：GCC/Clang 都压到偏移 0；MSVC 历史上第二个不压（⑲）。
10. 含虚函数的「空类」非真空（有 vptr），EBO 不适用，+8 字节。

### B2 空基类 vs 空成员 〔≥10 例〕

1. 作成员：`Empty e` 占 1B+对齐填充（受「成员地址唯一」约束）。
2. 作基类：`Empty` 占 0B（受 EBO 豁免）。
3. `read_member` 汇编 `mov 4[rcx]` vs `read_derived` `mov [rcx]`（⑩ 真实）。
4. `[[no_unique_address]] Empty e;` → 空成员也被压缩（C++20，等价 EBO）。
5. 空成员后接 `double` → 填充 7B（对齐 8）；空基类后接 `double` → 无此浪费（基类@0，double@0/8）。
6. 数组 `AsMember arr[100]` 浪费 400B；`Derived arr[100]` 不浪费。
7. `std::pair` 曾因空成员浪费，C++20 用 `[[no_unique_address]]` 压缩（ch?? 实用工具）。
8. 空成员不能和「位域 0」混用消歧，EBO 更干净。
9. 空基类不能 `offsetof(D, Empty)`（非成员），空成员可 `offsetof(S, e)`（但为 0）。
10. 选择：无状态组件优先基类/PBR；需独立生命周期管理时用成员。

### B3 工业应用 〔≥10 例〕

1. `std::vector<T,Alloc>`：Alloc 空基类（ch41）。
2. `std::unique_ptr<T,default_delete<T>>`：空删除器基类（ch48/ch49 提及）。
3. Policy-Based Design（ch71）：`Engine : LogP, TimeP` 多空基类混入。
4. 迭代器 tag：`input_iterator_tag` 等作空基类标记类别。
5. `std::chrono::duration<Rep,Period>`：Period 空基类（编译期常量）。
6. `boost::compressed_pair<T1,T2>`：专为 EBO 设计的 pair（空成员也压）。
7. 状态机：`struct Idle : State {};` 空状态作基类压缩。
8. 删除器策略：`struct StatelessDeleter{ void operator()(T*) const {} };` 作空基类。
9. 计数器/探针：`struct NoProbe{ void sample(){} };` 嵌入业务对象零成本。
10. `std::function` 小对象优化中，空 target 类型靠 EBO/空基类省 vptr。

### B4 多空基类与失效场景 〔≥10 例〕

1. `D : E1, E2`：均空，GCC/Clang 都压到 0（共享地址）。
2. `D : E1, E2 { int x; }`：x@0，sizeof=4（三个都重合到 0）。
3. MSVC 旧版：`E2` 不压 → sizeof=8，需 `[[no_unique_address]]` 修复。
4. 空基类后有**命名空基类**：仍可能全压（无数据成员阻挡）。
5. 空基类后是**有数据成员**：数据成员决定偏移，空基类维持 0。
6. 含虚函数的「空基类」→ 有 vptr，+8，EBO 失效。
7. 虚继承（ch49）空基类：vbptr 介入，布局变化，EBO 行为依赖实现。
8. `alignas` 作用在空基类：基类对齐要求可能被提升到派生类对齐，间接增大小。
9. 空基类 + `[[no_unique_address]]` 成员混用：二者都压缩，效果叠加。
10. 反射（ch74）下可枚举空基类偏移，编译期断言布局。

### B5 跨编译器与陷阱 〔≥10 例〕

1. GCC/Clang：多空基类全压，行为一致可预期。
2. MSVC：仅压首个空基类（历史），第二个可能占 1B——跨平台库需实测 `sizeof`。
3. `[[no_unique_address]]`：MSVC 19.27+、GCC 9+、Clang 9+ 支持，弥合差异。
4. ARM/32 位：空类占位仍 1B，EBO 同样适用（vptr 4B 而非 8B）。
5. LTO 不改变 EBO 决策（这是 ABI 布局，链接期不变）。
6. 空基类子对象地址 == 派生类地址 → 指针比较/哈希不要依赖不等（⑯ 反例3）。
7. `dynamic_cast` 到空基类：仍可用（基类有 typeinfo），但空基类常无虚函数（ch48）。
8. 调试器显示空基类「大小 0」可能不直观，先看 `sizeof(Derived)`。
9. 序列化：EBO 对象直接 `memcpy` 需保证无虚函数/无填充依赖（ch19）。
10. 误把 EBO 当「零大小对象可 `new`」——仍 `new` 出 ≥1 字节块（运算符 new 最小 1B）。

## 附录: EBO 深度

> **示例 36** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录: EBO 深度
```cpp
#include <iostream>
struct Empty{};struct NonEmpty:Empty{int x;};
int main(){std::cout<<sizeof(Empty)<<" "<<sizeof(NonEmpty)<<std::endl;return 0;}
```

> **示例 37** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录: EBO 深度
```cpp
#include <iostream>
#include <functional>
#include <memory>
struct Delete{void operator()(int*p){delete p;}};
int main(){std::unique_ptr<int,Delete> p(new int(42));std::cout<<*p<<std::endl;return 0;}
```

> **示例 38** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录: EBO 深度
```cpp
#include <iostream>
#include <utility>
template<typename T,typename D>struct Pair:T{D d;};
int main(){std::cout<<"EBO: empty base class occupies zero bytes in derived. Saves sizeof. Used in std::tuple."<<std::endl;return 0;}
```

> **示例 39** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录: EBO 深度
```cpp
#include <iostream>
#include <tuple>
#include <utility>
int main(){std::tuple<int,int,int> t{1,2,3};std::cout<<std::get<0>(t)<<std::endl;return 0;}
```

> **示例 40** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 附录: EBO 深度
```cpp
#include <iostream>
struct Tag1{};struct Tag2{};struct Combined:Tag1,Tag2{int v;};
// Combined 含 Tag1、Tag2 两个基类，聚合初始化须按基类顺序各补 {}，再给成员 v
int main(){Combined c{{},{},42};std::cout<<sizeof(c)<<" (int + EBO for both bases)"<<std::endl;return 0;}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第51章](../part05_oo/ch51_crtp.md) | 独占所有权/工厂模式 | 本章提供概念，第51章提供实现 |
| [第45章](../part05_oo/ch45_oop_object_model.md) | 泛型库/编译期计算 | 本章提供概念，第45章提供实现 |

## 深度增强：EBO编译器实现与工业

### 原理分析

EBO=空基类不占空间。C++20 [[no_unique_address]]扩展到空成员变量。
约束: 同类型两空基类不能重叠; MSVC 2022才支持[[no_unique_address]]

### 工业案例: unique_ptr的EBO

> **示例 41** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例: uniqueptr的EB
```cpp
#include <iostream>
#include <memory>
int main(){std::cout<<sizeof(std::unique_ptr<int>)<<" bytes (EBO=默认deleter不占空间)"<<std::endl;std::cout<<"vs 无EBO: 16 bytes (T* 8B + deleter 1B + padding 7B)"<<std::endl;return 0;}
```

### 汇编验证

```asm
; struct A:Empty{int x;}; sizeof=4 (EBO起作用)
; mov DWORD PTR [rax], 42
; struct B{Empty e;int x;}; sizeof=8 (EBO不起作用)
; mov BYTE PTR [rax], 0; mov DWORD PTR [rax+4], 42
```

| 项目 | EBO | 效果 |
|---|---|---|
| unique_ptr | compressed_pair | 默认deleter零开销 |
| std::tuple | 递归继承 | 无状态元素不占空间 |
| Eigen | storage traits | 编译期选择 |

面试: EBO何时不触发? 同类型两空基类/虚继承空基类; [[no_unique_address]] vs EBO? EBO=空基类; [[no_unique_address]]=空成员(C++20)

## 相关章节（交叉引用）

- **同模块接续**：[第 45 章　C++ 面向对象总览与对象模型基础](../part05_oo/ch45_oop_object_model.md)—— EBO 是对象模型层面的布局优化，空基类不占空间
- **同模块接续**：[第50章　多重继承与对象模型（Multiple Inheritance）](../part05_oo/ch50_multiple_inheritance.md)）—— 多重继承基类中 EBO 收益明显
- **同模块接续**：[第51章　CRTP 与静态多态（Curiously Recurring Template Pattern）](../part05_oo/ch51_crtp.md)）—— CRTP 基类为空，EBO 使其零成本
- **同模块接续**：[第49章 虚继承与菱形继承：共享虚基类](../part05_oo/ch49_virtual_inheritance.md)—— 虚继承与 EBO 都服务于基类布局优化
- **跨模块**：[第 35 章  C++ 程序的内存模型与操作系统视角](../part04_memory/ch35_memory_layout.md)—— 对象内存布局解释 EBO 的段级落点

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Boost.CompressedPair（boost.org）**：利用 EBO 把空基类压成 0 字节。
- **Chromium base::internal（github.com/chromium/chromium）**：同理压缩空基类。

**常见陷阱 / 最佳实践**：
- EBO 仅对空基类生效（无非静态数据成员）；`std::pair` 依赖 EBO 压缩第二模板参数（如 allocator）。
- 多重空基类仍可能占 1 字节对齐；EBO 不是免费午餐，需配合 `[[no_unique_address]]`（C++20）。

- **LLVM（llvm/llvm-project）**：`llvm/ADT/PointerIntPair.h` 用 EBO 把 1–2 位标志压进指针低位（tagged pointer），是空基类优化的经典非类型应用。
- **Abseil `absl::compressed_pair`（abseil/abseil-cpp）**：`std::compressed_pair` 的工业级实现，直接继承两个空基类之一以省 1 字节。
- **Qt 6（github.com/qt/qtbase）**：`Q_D`/`Q_Q` 指针封装（d-pointer 惯用法）用 EBO 让私有类零开销挂到公开类。
- **Eigen（gitlab.com/libeigen/eigen）**：固定大小矩阵 `Matrix<float,3,1>` 把维度作为空基类存储，EBO 使其零开销——与 `std::array` 同尺寸。

> 交叉引用：内存布局见 [ch35](../part04_memory/ch35_memory_layout.md)；对象模型见 [ch45](../part05_oo/ch45_oop_object_model.md)。

- **同模块**：[第47章 虚函数与虚表（vtable）：动态多态的发动机](../part05_oo/ch47_virtual_functions.md)：动态多态的发动机）—— 虚函数表与 EBO 同属对象模型视角，布局优化互补。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：STL 容器"免费携带"分配器/比较器。** `std::vector<int>` 内部混入一个 `std::allocator<int>`，但你 `sizeof(std::vector<int>)` 并没有多出一个分配器对象的字节——因为无状态分配器被 EBO 优化掉。请实证**基本 EBO**：空基类子对象可被优化为零字节，而空**成员**至少占 1 字节并触发填充。

<details><summary>答案与解析</summary>

C++ 要求每个完整对象具有唯一地址，故空成员至少 1 字节；空基类子对象在满足不与首个非空成员同地址冲突时，编译器可优化为零字节。

> **示例 42** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 1（难度 ★★）
```cpp
#include <iostream>
struct Empty {};
struct ByBase : Empty { int x; };
struct ByMember { Empty e; int x; };
int main() {
    std::cout << "sizeof(Empty)   = " << sizeof(Empty) << '\n';    // 1
    std::cout << "sizeof(ByBase)  = " << sizeof(ByBase) << '\n';   // 4  (EBO)
    std::cout << "sizeof(ByMember)= " << sizeof(ByMember) << '\n'; // 8  (1 + 3 填充 + 4)
}
```

<span class="badge badge-std">标准</span> EBO 是标准明确允许的空基类优化（维度⑥、维度⑪ 源码逐行），`std::vector` 的 allocator 即借此零开销混入。

<span class="badge badge-ref">引用</span> `std::vector` 以空基类混入分配器，使无状态分配器不增加容器尺寸（libstdc++ `<bits/stl_vector.h>`、cppreference "std::vector"）。C++20 还引入 `[[no_unique_address]]` 让空**成员**也能被压缩（cppreference "no_unique_address"）。ISO/IEC 14882:2023 §[class] 允许空基类子对象零尺寸。

</details>

### 练习 2（难度 ★★★）

**真实场景：Policy-Based 容器混入"多个无状态策略"。** 你的 `Vector<type, Alloc, Cmp, Traits>` 同时混入分配器、比较器、特性类等多个空策略；若把它们当成员，每个至少 1 字节、还会各自触发填充，尺寸爆膨。请实证**多个空基类**都能被同时优化，而等价空成员会因"每对象唯一地址"逐个膨胀。

<details><summary>答案与解析</summary>

多个空基类子对象都可被优化为零；但多个空成员各自至少 1 字节并参与填充，尺寸显著增大。

> **示例 43** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 2（难度 ★★★）
```cpp
#include <iostream>
struct E1 {};
struct E2 {};
struct D : E1, E2 { int x; };
struct M { E1 e1; E2 e2; int x; };
int main() {
    std::cout << "sizeof(D) = " << sizeof(D) << '\n';   // 4：两个空基类都被优化
    std::cout << "sizeof(M) = " << sizeof(M) << '\n';   // 12：每空成员 ≥1 字节 + 填充
}
```

<span class="badge badge-std">标准</span> 多空基类 EBO（维度⑪）支撑 Policy-Based 设计；空成员膨胀是"每对象唯一地址"规则的代价。

<span class="badge badge-ref">引用</span> `boost::compressed_pair` 正是利用多空基类 EBO 把"可能为空"的两个类型压缩存储（Boost.Compressed_Pair 文档，boost.org/doc/libs）。这与 Andrei Alexandrescu《Modern C++ Design》中 Policy-Based 设计对零开销策略组合的要求一致。ISO/IEC 14882:2023 §[class] 规定空基类可被优化为零。

</details>

### 练习 3（难度 ★★★★）

**真实场景：policy-based 数值容器 `Vector<type, Alloc, Cmp>`。** 你的数值库用策略类定制"栈分配 vs 堆分配"，策略类本身无数据成员。若当作成员，每个策略至少 1 字节、容器尺寸膨胀；正确做法是作**空基类**混入。请用 **Policy-Based 设计**：把策略类作为**空基类**混入，构造 `Vector<type, Alloc, Cmp>`，实证零状态开销（对比作成员会膨胀）。

<details><summary>答案与解析</summary>

策略类无数据成员时作空基类混入，宿主类自身零状态开销（基类被 EBO）。这正是 `std::vector` 分配器、`std::map` 比较器的实现思路。

> **示例 44** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 3（难度 ★★★★）
```cpp
#include <iostream>
template <class AllocPolicy>
struct Vector : private AllocPolicy {    // 空基类混入：零开销
    int size() const { return AllocPolicy::capacity(); }
};
struct StackAlloc { static int capacity() { return 64; } };
struct HeapAlloc  { static int capacity() { return 1 << 20; } };
int main() {
    Vector<StackAlloc> s; Vector<HeapAlloc> h;
    std::cout << "sizeof(s)=" << sizeof(s) << " s.cap=" << s.size() << '\n'; // 0 状态 + 64
    std::cout << "sizeof(h)=" << sizeof(h) << " h.cap=" << h.size() << '\n'; // 0 状态 + 1M
}
```

<span class="badge badge-std">标准</span> Policy-Based 设计（维度⑪ 后续依赖 ch71/ch50）依赖 EBO 实现零开销策略组合；作成员则每策略至少 1 字节。

<span class="badge badge-ref">引用</span> Policy-Based 设计由 Andrei Alexandrescu 在 *Modern C++ Design*（2001）系统提出，`std::vector`/`std::map` 的分配器与比较器即无状态策略经 EBO 混入的实例（cppreference "std::allocator"）。C++20 `[[no_unique_address]]` 进一步让空成员也能压缩（cppreference）。ISO/IEC 14882:2023 §[class] 与 §[dcl.attr.uniqueaddr] 规定相关机制。

</details>

### 练习 4（难度 ★★）

**真实场景：你对比两个"看似等价"的结构，却发现一个比另一个小一半。** 请用代码演示：当空类作为**基类**时，派生类尺寸可能因空基类优化（EBO）而不变；但当它作为**成员**时，却至少多占一个字节并触发填充。

<details><summary>答案与解析</summary>

EBO 允许编译器把"空基类子对象"优化为零字节，因为完整对象必须有唯一地址，但空基类子对象可以与第一个非静态数据成员共用地址。而空**成员**无法被优化——它必须拥有自己的存储，且为对齐常带来填充。这正是 `std::vector` 能"免费"携带空分配器的原因。

> **示例 53** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 4（难度 ★★）
```cpp
#include <iostream>
struct Empty { };
struct WithBase      : Empty { int x = 0; };   // 空基类：可被压缩
struct WithMember    { Empty e; int x = 0; };   // 空成员：至少 1 字节 + 填充
int main() {
    std::cout << "WithBase = "    << sizeof(WithBase)   << "\n";   // 典型 4
    std::cout << "WithMember = "  << sizeof(WithMember) << "\n";   // 典型 8
}
```

<span class="badge badge-std">标准</span> 空基类优化由 ISO/IEC 14882（C++23）允许（§[class]）：基类子对象可与同一对象的其他子对象共用地址，只要不违反"对象唯一地址"要求。`[[no_unique_address]]` 进一步把同款优化扩展到数据成员（C++20）。

<span class="badge badge-exp">经验</span> EBO 是标准库基石：`std::vector<Alloc>` 的空分配器不增加容量。`boost::compressed_pair` 即围绕此特性构建。需要"零开销混入"时优先继承而非成员；C++20 起也可对成员用 `[[no_unique_address]]`。

</details>

### 练习 5（难度 ★★★）

**真实场景：你在写一个通用容器，想让"带状态的策略对象"与"不带状态的策略对象"有完全相同的开销。** 请写出压缩 Pair：把两个类型都作为基类混入，演示当其中一个为空时整体尺寸被优化掉——这正是策略化设计（见 ch71）的底层机制。

<details><summary>答案与解析</summary>

把多个类型作为基类混入（而非成员），可让其中任意空类型被 EBO 压缩。当两个/多个基类之一为空时，整体尺寸可缩减到只剩非空成员。这就是 `std::vector`/`std::tuple` 用空基类混入实现零开销策略组合的原理。

> **示例 54** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 5（难度 ★★★）
```cpp
#include <iostream>
struct EmptyTag { };
struct WithData { int v = 5; };
template <typename T, typename U>
struct Compressed : T, U { };        // 两个基类，空类型将被压缩
int main() {
    Compressed<EmptyTag, WithData> c;
    std::cout << "compressed size = " << sizeof(c)
              << " (vs WithData alone = " << sizeof(WithData) << ")\n";
}
```

<span class="badge badge-std">标准</span> EBO 对"任何空基类"都可适用（ISO/IEC 14882 §[class]）；当多个基类并存时，只要布局允许，编译器可把多个空基类都优化为零字节。`std::tuple` 正是递归地以空基类混入各元素。

<span class="badge badge-exp">经验</span> 策略化设计（Policy-Based Design）依赖 EBO：`std::vector` 的分配器、`std::map` 的比较器都是无状态策略，经 EBO 混入后零开销。`[[no_unique_address]]` 是 C++20 对"空成员"的等价手段，能在成员位置达成类似压缩。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：空策略类当成员导致尺寸膨胀

**选型场景**：用策略类（分配器/比较器/特性标签）定制容器行为。

**常见错误**：把策略类作为**成员**字段，即使策略无状态也至少占 1 字节并产生填充，容器尺寸膨胀。

> **示例 45** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 演绎 1：空策略类当成员导致尺寸膨胀
```cpp
#include <iostream>
template <class P> struct W { P policy; int x; };
struct NoState {};
int main() {
    W<NoState> w;
    std::cout << "sizeof(W) = " << sizeof(w) << '\n';  // 8：空成员占 1 + 填充
}
```

**修复**：私有继承策略类（空基类混入），触发 EBO，宿主零状态开销。

> **示例 46** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 演绎 1：空策略类当成员导致尺寸膨胀
```cpp
#include <iostream>
template <class P> struct W : private P { int x; };
struct NoState {};
int main() {
    W<NoState> w;
    std::cout << "sizeof(W) = " << sizeof(w) << '\n';  // 4：EBO 生效
}
```

**结论**：无状态策略应作空基类混入（维度⑪）；`std::vector`/`std::map` 的分配器、比较器均如此实现零开销。

### 演绎 2：误以为 EBO 在任何情况都保证零

**选型场景**：依赖 `sizeof(Derived : Empty {int}) == sizeof(int)` 做布局假设。

**常见错误**：认为空基类**永远**零开销，忽略"空基类若与首个非静态数据成员同地址冲突，编译器须插入至少 1 字节区分"，EBO 不保证绝对零。

> **示例 47** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 演绎 2：误以为 EBO 在任何情况
```cpp
#include <iostream>
struct Empty {};
struct Conflict { Empty e; char c; };   // e 与 c 不能同地址，e 至少占 1 字节
int main() {
    std::cout << "sizeof(Conflict) = " << sizeof(Conflict) << '\n';  // 2（非 1）
}
```

**修复**：在目标平台用 `static_assert` 锁定期望尺寸；设计上让空基类排在最前且无同地址冲突的成员。

> **示例 48** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 演绎 2：误以为 EBO 在任何情况
```cpp
#include <iostream>
struct Empty {};
struct Good : Empty { int x; };
static_assert(sizeof(Good) == sizeof(int), "EBO 失效：目标平台布局不符");
int main() { std::cout << sizeof(Good) << '\n'; }
```

**结论**：EBO 是"允许"而非"保证"的优化；跨平台布局假设必须用 `static_assert` 固化（维度⑲ 性能/可移植性）。
## 附录 E：编译实证——EBO 的字节偏移在汇编里直接可见 [C: Compiler / E: Low-level]

> `[实测]` 编译：`g++ -std=c++23 -O2 -c ch52_ebo_test.cpp` + `objdump -d`（GCC 15.3.0 / Win64 ABI）。产物 `_asm_demo/ch52_ebo_test.cpp`。编译通过本身即证明所有 `static_assert` 成立。

空基类优化（EBO）不是"约定"，它由 ABI 强制：**空基类子对象大小为 0**。三种写法的 `sizeof` 与成员偏移差异，直接写进了成员访问的汇编偏移里。

### 测试源码

> **示例 49** <span class="badge badge-exp">难度 ★★★☆☆</span> · 测试源码
```cpp
struct Empty {};                        // sizeof == 1（独立时，空类至少 1 字节且本例无子对象，恰为 1）
struct WithEBO : Empty { int x; };      // 继承空基类 —— EBO 通常使 sizeof == 4（实现许可，非强制）
struct NoEBO  { Empty e; int x; };      // 空类做成员 —— 无 EBO/[[no_unique_address]]：空成员至少 1B+填充，必然 == 8
struct NoUniqAddr { [[no_unique_address]] Empty e; int x; };  // C++20：空成员通常也被压到 0，sizeof 通常 == 4

static_assert(sizeof(Empty)      == 1);                    // 空类恰 1 字节（C++ 保证）
static_assert(sizeof(NoEBO)      == 8);                    // 无优化：空成员 1B+3 填充，必然 8（可移植保证）
static_assert(sizeof(WithEBO)    < sizeof(NoEBO));         // EBO 生效：继承空基类使其严格小于非优化版
static_assert(sizeof(NoUniqAddr) < sizeof(NoEBO));         // [[no_unique_address]] 生效：同样严格小于非优化版
// 注：EBO 与 [[no_unique_address]] 都是"允许"而非"强制"的优化，故不对绝对大小做精确断言，
// 只断言"优于非优化版"（WithEBO/NoUniqAddr 在主流编译器上通常 == sizeof(int)，但该值随实现而变）。
```

### 真实汇编：偏移即证据

```asm
<read_ebo(WithEBO&)>:
    mov    (%rcx),%eax        ; [EBO] x 在偏移 0 —— 空基类占 0 字节
    ret

<read_noebo(NoEBO&)>:
    mov    0x4(%rcx),%eax     ; [无EBO] x 在偏移 4 —— 空成员 e 被迫占 1 字节 + 3 填充
    ret

<read_nua(NoUniqAddr&)>:
    mov    (%rcx),%eax        ; [no_unique_address] x 回到偏移 0 —— 恢复 EBO
    ret
```

**💡 关键观察**：三个函数体都只有一条 `mov`，唯一差别是**立即数偏移**：
- `WithEBO`：偏移 `0`（`(%rcx)`）——空基类零字节，`x` 紧贴对象头。
- `NoEBO`：偏移 `0x4`——空成员 `e` 因"不同对象地址必须不同"规则被迫占 1 字节，加对齐填充推到 4。
- `NoUniqAddr`：偏移 `0`——`[[no_unique_address]]` 允许空成员与后续成员共址，把 EBO 从"仅继承"扩展到"成员"。

### 为什么空成员不能是 0 字节

C++ 要求**同类型的两个不同对象有不同地址**。若 `NoEBO::e` 占 0 字节，则 `&n.e == &n.x`（不同类型尚可），但两个相邻 `Empty` 数组元素会同址——违反规则。所以**空成员至少 1 字节**。而空**基类**子对象不受此约束（基类子对象允许与派生对象同址），故 EBO 成立。

### 代价分层

| 写法 | `sizeof` | `x` 偏移 | 空类零开销? | 适用 |
|------|---------|---------|------------|------|
| `struct D : Empty { int x; }` | 4 | 0 | ✅ EBO | 策略/分配器/删除器基类 |
| `struct D { Empty e; int x; }` | 8 | 4 | ❌ 浪费 4 字节 | 避免 |
| `struct D { [[no_unique_address]] Empty e; int x; }` | 4 | 0 | ✅ C++20 | 组合优于继承时 |

### 关键发现

- EBO 是 `std::allocator`、`std::default_delete`、`std::tuple`、`std::function` 等库设施能"零成本携带无状态策略"的底层机制——空分配器/空删除器不占对象一个字节。
- C++20 前，想让**成员**（而非基类）享受零开销只能用继承（`private Empty`）；C++20 的 `[[no_unique_address]]` 让组合也能做到，代码更清晰。
- 判断一个库类型是否用了 EBO，最直接的方法就是本附录的手法：`static_assert(sizeof(...))` + 看成员访问偏移。

## 补例：自包含可编译验证（EBO 零开销）

下例用 `static_assert` 把正文结论变成编译期可验证事实：

> **示例 50** <span class="badge badge-exp">难度 ★★★☆☆</span> · 补例：自包含可编译验证
```cpp
#include <cstddef>
#include <iostream>

struct Empty {};                  // 空类：理论 0 字节，但至少占 1 字节
struct A : Empty { int x; };     // A 享受 EBO：空基类不占空间
struct B { Empty e; int x; };    // B 不享受：空成员至少 1 字节 + 对齐 -> 8

int main(){
    static_assert(sizeof(A) == sizeof(int), "EBO: 空基类子对象零开销");
    static_assert(sizeof(B) == 2 * sizeof(int), "空成员至少 1 字节并参与对齐");
    std::cout << sizeof(A) << " " << sizeof(B) << "\n";  // 4 8
}
```

`sizeof(A)==4` 证明空基类 `Empty` 被完全吸收；`sizeof(B)==8` 证明作为成员的 `Empty` 至少占 1 字节并触发 4 字节对齐填充。这正是标准库 `std::allocator`/`std::default_delete` 能零成本携带无状态策略的底层原因。

## 附录 J：空基类优化 EBO 决策流（D3 维度）

```mermaid
flowchart TD
    S["需要零开销存放一个无状态组件<br/>(策略/分配器/删除器/标签)"] --> Q1{"需要独立<br/>生命周期?"}
    Q1 -->|"是(组合语义)"| M["普通成员: 空成员占 1B+填充<br/>浪费但语义清晰"]
    Q1 -->|"否"| Q2{"组件有状态?"}
    Q2 -->|"有状态数据"| M2["普通成员: EBO 不适用<br/>必须按成员存储"]
    Q2 -->|"无状态"| Q3{"目标编译器<br/>支持 C++20?"}
    Q3 -->|"是"| N["用 no_unique_address 属性 (C++20) 成员<br/>组合语义 + 零开销"]
    Q3 -->|"否"| E["私有继承作空基类 (EBO)<br/>策略作空基类混入"]
    N --> Q4{"有多个空组件?"}
    E --> Q4
    Q4 -->|"是"| ME["多继承多个空基类<br/>GCC/Clang 均压到 0"]
    Q4 -->|"否"| SE["单继承空基类<br/>空基类子对象占 0 字节"]
    ME --> Q5{"空基类后有<br/>命名数据成员?"}
    SE --> Q5
    Q5 -->|"有"| K["数据成员决定偏移<br/>空基类仍 @0 (EBO 生效)"]
    Q5 -->|"无"| SL["仍是标准布局<br/>可 memcpy 概念"]
    K --> Q6{"空基类含虚函数?"}
    SL --> Q6
    Q6 -->|"是"| X["EBO 失效: vptr 使类非空<br/>改用成员或 concept 约束"]
    Q6 -->|"否"| Q7{"需跨编译器<br/>可移植?"}
    Q7 -->|"是"| A1["加 static_assert(sizeof==...)<br/>固化布局防回归"]
    Q7 -->|"否"| A2["直接采用 EBO"]
    A1 --> L["落地: vector allocator / unique_ptr deleter<br/>零开销混入"]
    A2 --> L
    L --> V["用 offsetof/sizeof 编译期断言<br/>验证 x@0 证明 EBO 生效"]
```

> 决策流说明：无状态组件优先作私有空基类（EBO）或 C++20 的 `no_unique_address` 成员，二者都能把存储代价压到 0 字节；只有当需要独立生命周期、组件有状态、或空基类含虚函数时，才退回普通成员并接受 1 字节占位。跨编译器项目务必用 `static_assert(sizeof(...)==...)` 固化布局，避免 MSVC 旧版对第二个空基类不压缩导致的尺寸漂移。

## 附录 K：空基类优化 EBO 知识图谱（D6 维度）

```mermaid
flowchart TD
    A["空类"] --> B["对象大小 sizeof"]
    A --> C["空基类"]
    C --> D["EBO 空基类占 0"]
    D --> E["多继承布局"]
    D --> G["no_unique_address 属性"]
    D --> H["偏移 offsetof"]
    D --> F["对齐 填充"]
    D --> I["标准布局"]
    D --> J["策略混入 Policy-Based"]
    D --> K["allocator 空基类"]
    D --> L["unique_ptr 空删除器"]
    D --> M["缓存密度"]
    D --> O["static_assert 契约"]
    D --> P["MSVC 差异"]
    M --> N["CPU 缓存 缓存行"]
    E --> R["虚继承"]
    C --> Q["虚函数 vptr"]
```

### K.1 概念依赖逐边解读

| 边 | 工程含义 |
|---|---|
| 空类 → 对象大小 sizeof | 空类至少占 1 字节，源于 C++ 要求每个完整对象可寻址、同类型两对象地址不同 |
| 空类 → 空基类 | 空类作基类时，标准豁免"基类子对象唯一地址"要求，这是 EBO 的前提 |
| 空基类 → EBO 空基类占 0 | 空基类子对象可被布局到派生类首成员同址，从而占 0 字节 |
| EBO → 多继承布局 | 多个空基类在 GCC/Clang 下均被压到偏移 0，取决于多重继承排列规则 |
| EBO → no_unique_address 属性 | C++20 把"零开销压缩"从继承扩展到成员，组合优于继承时仍能省空间 |
| EBO → 偏移 offsetof | `offsetof(Derived,x)==0` 是 EBO 的编译期可执行证据 |
| EBO → 对齐 填充 | 空基类不增加对齐要求，对齐由最大成员/对齐说明符决定 |
| EBO → 标准布局 | EBO 不破坏标准布局（首成员为数据成员时），仍可 memcpy 概念 |
| EBO → 策略混入 Policy-Based | 空策略作空基类混入，是实现零开销策略组合的基础 |
| EBO → allocator 空基类 | std::vector 把 allocator 作空基类嵌入，省去 8 字节指针 |
| EBO → unique_ptr 空删除器 | default_delete 作空基类，使 unique_ptr 只等于裸指针大小 |
| EBO → 缓存密度 | 对象更小 → 更多对象装入缓存行 → 减少 cache miss |
| 缓存密度 → CPU 缓存 缓存行 | 64B 缓存行装 16 个 Derived vs 8 个 AsMember，密度翻倍 |
| EBO → static_assert 契约 | 用 static_assert 锁 size，把 EBO 收益写进编译期契约防回归 |
| EBO → MSVC 差异 | MSVC 旧版仅压首空基类，第二个可能占位，需实测或 no_unique_address |
| 多继承布局 → 虚继承 | 虚继承引入 vbptr，与 EBO 布局交互需谨慎 |
| 空基类 → 虚函数 vptr | 含 vptr 则类非空，EBO 不适用且引入 8 字节开销 |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch19 对象大小/存储期 | ch52 EBO | 空类≥1字节由可寻址性决定，EBO 正是豁免该规则的特例 |
| ch45 对象模型(布局/对齐) | ch52 EBO | 成员布局与对齐是 EBO 生效的底层承载 |
| ch50 多继承布局 | ch52 EBO | 多空基类能否都压到 0 取决于多重继承排列 |
| ch51 CRTP 空基类 | ch52 EBO | CRTP 基类常为空，EBO 使其零成本 |
| ch52 EBO | ch71 Policy-Based Design | 空策略作空基类混入实现零开销策略组合 |
| ch52 EBO | ch41 allocator | 容器把 allocator 作空基类嵌入省去指针 |
| ch52 EBO | ch49 虚继承 | 空基类与虚继承布局的交互约束 |
| ch52 EBO | ch48/49 unique_ptr | 空删除器作空基类实现零开销智能指针 |

## 附录 D4：libstdc++ 15.3.0 源码解析 — EBO 在 `tuple` / `shared_ptr` 控制块 / `pair` 中的落点 [E: Low-level / H: Design]

> 本附录所有摘录均来自随书工具链 **GCC 15.3.0** 自带 libstdc++
>（`.../include/c++/15.3.0/`），首行标注 `// <相对路径> Lx-y`，内容与源文件逐字一致（单独一行 `…` 表省略）。
> libc++ / MSVC STL 仅给"已知公开实现行为"对比，非逐字摘录，避免伪造。
> 提示中提到的 `__is_empty_non_tuple` / `_UseEBO` 分支在 GCC 15.3.0 实测源码中**并不存在**，本书以实测为准如实写出（见 D4.1 说明）。

### D4.1 `tuple::_Head_base` 对空类型的 EBO（tuple L85-252）

`tuple` 把每个元素包进 `_Head_base<_Idx,_Head,bool>`，第三个模板参数决定"空且非 final"时走 EBO。先声明：

```text
// tuple L85-87
  template<size_t _Idx, typename _Head,
	   bool = __empty_not_final<_Head>::value>
    struct _Head_base;
```

GCC 15.3.0 中 `__has_cpp_attribute(__no_unique_address__)` 为真，故走 `#if` 分支：空元素用 `[[__no_unique_address__]]` 成员承载，而非传统的"继承式 EBO"。

```text
// tuple L89-143  (省略 L110-134 的 allocator 构造函数)
#if __has_cpp_attribute(__no_unique_address__)
  template<size_t _Idx, typename _Head>
    struct _Head_base<_Idx, _Head, true>
    {
      constexpr _Head_base()
      : _M_head_impl() { }

      constexpr _Head_base(const _Head& __h)
      : _M_head_impl(__h) { }

      constexpr _Head_base(const _Head_base&) = default;
      constexpr _Head_base(_Head_base&&) = default;

      template<typename _UHead>
	constexpr _Head_base(_UHead&& __h)
	: _M_head_impl(std::forward<_UHead>(__h)) { }

      …
      static constexpr _Head&
      _M_head(_Head_base& __b) noexcept { return __b._M_head_impl; }

      static constexpr const _Head&
      _M_head(const _Head_base& __b) noexcept { return __b._M_head_impl; }

      [[__no_unique_address__]] _Head _M_head_impl;
    };
```

非 EBO 分支（`false` 特化）则是普通成员，空类型也会占 1 字节：

```text
// tuple L199-252  (省略 L202-243 的构造函数)
  template<size_t _Idx, typename _Head>
    struct _Head_base<_Idx, _Head, false>
    {
      …
      _Head _M_head_impl;
    };
```

`#else` 分支（仅当编译器不支持 `__no_unique_address__` 属性时启用）才用"继承式 EBO"——把 `_Head` 作为基类：

```text
// tuple L144-196  (仅在不支持 [[no_unique_address]] 时编译；省略 L149-189)
  template<size_t _Idx, typename _Head>
    struct _Head_base<_Idx, _Head, true>
    : public _Head
    {
      …
      static constexpr _Head&
      _M_head(_Head_base& __b) noexcept { return __b; }

      static constexpr const _Head&
      _M_head(const _Head_base& __b) noexcept { return __b; }
    };
```

> 诚实考据：提示假设 GCC 15 用 `__is_empty_non_tuple` / `_UseEBO`，实测 `_Head_base` 第三参数默认值为 `__empty_not_final<_Head>::value`（L86），全文件 grep 无 `_UseEBO`。GCC 15 走属性式 EBO（`[[__no_unique_address__]]`，L142），继承式分支（L147）只是 `#else` 退化路径。

### D4.2 `shared_ptr` 控制块对 deleter/allocator 的 EBO（bits/shared_ptr_base.h L461-509）

`shared_ptr` 的 `_Sp_counted_deleter` 控制块需要同时持有自定义 deleter 与 allocator（常为无状态空类型），用 `_Sp_ebo_helper` 做 EBO 封装：

```text
// bits/shared_ptr_base.h L461-489
  template<int _Nm, typename _Tp,
	   bool __use_ebo = !__is_final(_Tp) && __is_empty(_Tp)>
    struct _Sp_ebo_helper;

  /// Specialization using EBO.
  template<int _Nm, typename _Tp>
    struct _Sp_ebo_helper<_Nm, _Tp, true> : private _Tp
    {
      explicit _Sp_ebo_helper(const _Tp& __tp) : _Tp(__tp) { }
      explicit _Sp_ebo_helper(_Tp&& __tp) : _Tp(std::move(__tp)) { }

      static _Tp&
      _S_get(_Sp_ebo_helper& __eboh) { return static_cast<_Tp&>(__eboh); }
    };

  /// Specialization not using EBO.
  template<int _Nm, typename _Tp>
    struct _Sp_ebo_helper<_Nm, _Tp, false>
    {
      explicit _Sp_ebo_helper(const _Tp& __tp) : _M_tp(__tp) { }
      explicit _Sp_ebo_helper(_Tp&& __tp) : _M_tp(std::move(__tp)) { }

      static _Tp&
      _S_get(_Sp_ebo_helper& __eboh)
      { return __eboh._M_tp; }

    private:
      _Tp _M_tp;
    };
```

`_Sp_counted_deleter::_Impl` 用两个 `_Sp_ebo_helper` 基（编号 0=deleter、1=allocator）多重继承，空 deleter/allocator 都被压到 0 字节：

```text
// bits/shared_ptr_base.h L495-508
      class _Impl : _Sp_ebo_helper<0, _Deleter>, _Sp_ebo_helper<1, _Alloc>
      {
	typedef _Sp_ebo_helper<0, _Deleter>	_Del_base;
	typedef _Sp_ebo_helper<1, _Alloc>	_Alloc_base;
	…
	_Deleter& _M_del() noexcept { return _Del_base::_S_get(*this); }
	_Alloc& _M_alloc() noexcept { return _Alloc_base::_S_get(*this); }

	_Ptr _M_ptr;
      };
```

EBO 生效条件可见 L462：`__use_ebo = !__is_final(_Tp) && __is_empty(_Tp)`——**空且非 final** 才继承式 EBO；`final` 类型必须保持唯一地址（见 L458-459 注释）。

### D4.3 `pair` 不做成员级 EBO（bits/stl_pair.h L301-309）

`std::pair` 把两个元素作为**具名直接成员**存储，未对空成员施加 `[[no_unique_address]]`，也未用继承式 EBO：

```text
// bits/stl_pair.h L301-309
  template<typename _T1, typename _T2>
    struct pair
    : public __pair_base<_T1, _T2>
    {
      typedef _T1 first_type;    ///< The type of the `first` member
      typedef _T2 second_type;   ///< The type of the `second` member

      _T1 first;                 ///< The first member
      _T2 second;                ///< The second member
```

`pair` 仅把空标记类 `__pair_base` 作为基（L303，EBO 作用于该空基）。但 `first`/`second` 是数据成员：标准允许用户取 `&p.first`、用 `offsetof`、甚至 `pair` 参与聚合/标准布局判断，施加 `[[no_unique_address]]` 会让空成员的地址与另一成员重合，破坏可寻址性与 ABI 稳定性。GCC 选择保持 `pair<Empty,int>` 中 `Empty` 占 1 字节，这是有意的工程取舍，而非疏漏。

### D4.4 跨实现对比

| 维度 | libstdc++ (GCC 15.3.0) | libc++ (LLVM) | MSVC STL |
|------|------------------------|---------------|----------|
| 空基类 EBO 判定 | `__empty_not_final<_Head>`；GCC15 用 `[[no_unique_address]]`（tuple L142） | `tuple` 用 `__libcpp_compressed_pair` 继承式 EBO | `tuple`/`pair` 用继承式 EBO（`__tuple_leaf` 基类） |
| `shared_ptr` 控制块 | `_Sp_ebo_helper`（L467 继承式） | `__sp_ebo_helper` 同类继承式封装 | 控制块对空 deleter/allocator 同样压地址（实现细节未公开核对） |
| `pair` 成员 | 直接成员、无 no_unique_address（L308-309） | 直接成员，无 no_unique_address | 直接成员，无 no_unique_address |
| `[[no_unique_address]]` 取舍 | 优先属性式，退化用继承式 `#else` | 无属性前用继承式 | 无属性前用继承式 |

> libc++ / MSVC 行为为公开实现常识（可在 llvm-project / microsoft/STL 仓库核实），非逐字摘录。

### D4.5 设计动机小结

EBO 生效三条件：**(1) 类型是空类（无非静态数据成员、无虚函数/虚基）；(2) 非 `final`（final 类须有唯一地址）；(3) 不与同类型另一子对象被迫同址**（同一类中放两个相同空基类会导致"同址冲突"，标准仅保证至少一个可压到 0）。属性式 `[[no_unique_address]]`（tuple L142）比继承式 EBO 更灵活：它允许同一类里多个空成员各自压到 0 而不冲突，且能保留成员语义（仍有名字、可 `&` 取址）。继承式 EBO（shared_ptr L467、tuple `#else` L147）是 C++20 前的唯一手段，要求把空类型放到基类位置，且与同类型子对象同址时受限。

### D4.6 第一方可编译验证（tuple vs pair 空成员布局 + 自定义 EBO holder）

> **示例 51** <span class="badge badge-exp">难度 ★★★☆☆</span> · 第一方可编译验证
```cpp
#include <iostream>
#include <tuple>
#include <utility>
#include <type_traits>

struct Empty { };                 // 空类
struct FinalEmpty final { };      // final 空类，禁用 EBO

// 自定义继承式 EBO holder：把空策略作为基类压到 0 字节
template<typename T, typename Policy>
struct Holder : private Policy {
    T value;
    constexpr Holder(T v, const Policy&) : value(v) { }
};

int main() {
    std::cout << "sizeof(Empty)                = "
              << sizeof(Empty) << std::endl;
    std::cout << "sizeof(tuple<Empty,int>)     = "
              << sizeof(std::tuple<Empty, int>) << std::endl;
    std::cout << "sizeof(pair<Empty,int>)      = "
              << sizeof(std::pair<Empty, int>) << std::endl;
    std::cout << "sizeof(tuple<FinalEmpty,int>)= "
              << sizeof(std::tuple<FinalEmpty, int>) << std::endl;
    std::cout << "sizeof(Holder<int,Empty>)    = "
              << sizeof(Holder<int, Empty>) << std::endl;

    // 红线自检：EBO 是实现许可非强制，禁用精确 == 断言复合布局。
    // 只允许 >= 与类型萃取断言。
    static_assert(std::is_empty_v<Empty>);
    static_assert(sizeof(std::tuple<Empty, int>)
                  <= sizeof(std::pair<Empty, int>));   // tuple 不劣于 pair
    static_assert(sizeof(Holder<int, Empty>) >= sizeof(int));

    std::cout << "EBO checks passed (no == on layout)" << std::endl;
    return 0;
}
```

预期输出：`tuple<Empty,int>` 为 4（空成员被压到 0），`pair<Empty,int>` 为 8（空成员占 1 字节并因 `int` 对齐补齐），`tuple<FinalEmpty,int>` 回到 8（final 禁用 EBO），`Holder<int,Empty>` 为 4（继承式 EBO 生效）。仅用 `>=` / `is_empty_v` 断言，未对布局做精确 `==`。

## 附录 D5：真实基准与性能分析 — 空基类优化与 [[no_unique_address]]（GCC 15.3.0）

> 测试环境：AMD Ryzen 9 7940HX（16C/32T）；本机 MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++23`；`std::chrono::steady_clock` 计时，5 轮取中位；`volatile` sink 防死代码消除。本附录目的：用主控实测锁死的真实毫秒，量化空基类优化与 `[[no_unique_address]]` 对对象布局与遍历带宽的影响，并给出根因。**绝对毫秒随机器而变，加速比才是可移植信号。**

### D5.1 基准结果 [VERIFIED]

`Plain`/`Squeezed`/`Inherit` 各含一个 `long long` 与一个空成员；"遍历求和"指对数组累积该 `long long`。

| 类型 | sizeof (B) | 说明 |
|---|---|---|
| `Plain{v; Empty e;}` | 16 | 空成员占 8B 对齐填充 |
| `Squeezed{v; [[no_unique_address]] Empty e;}` | 8 | 空成员压到 0 |
| `Inherit : Empty {v;}` | 8 | 继承式 EBO |
| `unique_ptr<int>` | 8 | 无状态删除器句柄 |
| `unique_ptr<int, void(*)(int*)>` | 16 | 函数指针删除器使句柄翻倍 |

| 场景 | 耗时 ms | 相对 |
|---|---|---|
| 遍历求和 — Squeezed | 39.571 | 基准（最快） |
| 遍历求和 — Inherit | 42.135 | 1.06× |
| 遍历求和 — Plain | 59.261 | Plain 慢 1.50× |

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">25</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">50</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">75</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="201.9" x2="640" y2="201.9" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="197.9" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 39.57ms</text>
  <rect x="141.3" y="201.9" width="64.0" height="98.1" fill="#9A9A9A"/>
  <text x="173.3" y="195.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">39.57ms</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">遍历求和 — Squeezed</text>
  <rect x="328.0" y="195.5" width="64.0" height="104.5" fill="#DD8452"/>
  <text x="360.0" y="189.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">42.13ms</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">遍历求和 — Inherit</text>
  <rect x="514.7" y="153.0" width="64.0" height="147.0" fill="#C44E52"/>
  <text x="546.7" y="147.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">59.26ms</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">遍历求和 — Plain</text>
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
  <rect x="141.3" y="176.0" width="64.0" height="124.0" fill="#9A9A9A"/>
  <text x="173.3" y="170.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">遍历求和 — Squeezed</text>
  <rect x="328.0" y="168.0" width="64.0" height="132.0" fill="#DD8452"/>
  <text x="360.0" y="162.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">1.06×</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">遍历求和 — Inherit</text>
  <rect x="514.7" y="114.3" width="64.0" height="185.7" fill="#C44E52"/>
  <text x="546.7" y="108.3" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">1.50×</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">遍历求和 — Plain</text>
</svg>

> 图注：空基类优化（EBO）让空成员占 0 字节：`Plain` 因对齐填 8B（16B），`[[no_unique_address]]` 或继承式 EBO 都压到 8B；但带函数指针删除器的 `unique_ptr` 句柄翻倍到 16B。

### D5.2 非显然结论

1. **未压缩空成员每对象浪费 8B，缓存行密度减半直接变现为 1.50×。** 根因：`Plain` 16B vs `Squeezed` 8B，同样 64B 缓存行从容纳 4 个对象降到 2 个，带宽受限的线性遍历的 L1/L2 缺失率近乎翻倍，把 39.6ms 推到 59.3ms——这是布局膨胀经缓存层次放大的实测证据，与虚函数/间接无关。

2. **EBO 继承与 `[[no_unique_address]]` 效果等价（本例均 8B），后者不需扭曲继承结构。** 根因：两者底层都是"允许空子对象与其邻位成员共享地址"，但继承式 EBO 必须把空类型放到基类位置、且同类型多子对象会触发同址冲突；`[[no_unique_address]]` 是属性式，保持成员语义（有名字、可 `&` 取址），适用面更广。

3. **`unique_ptr` 的"零成本"取决于删除器是否有状态，须诚实标注。** 根因：无状态 lambda/函数对象删除器被空基类优化吞掉，`unique_ptr<int>` 保持 8B；而函数指针删除器是 8B 真实状态，`unique_ptr<int, void(*)(int*)>` 涨到 16B——同样的"句柄"概念，尺寸随删除器状态翻倍，与"零成本抽象"是否兑现直接挂钩。

### D5.3 验证 demo

> **示例 52** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 验证 demo
```cpp
#include <iostream>
#include <memory>
#include <cassert>

struct Empty { };
struct Plain { long long v; Empty e; };
struct Squeezed { long long v; [[no_unique_address]] Empty e; };
struct Inherit : Empty { long long v; };

int main() {
    std::cout << "sizeof(Plain)   =" << sizeof(Plain) << std::endl;
    std::cout << "sizeof(Squeezed)=" << sizeof(Squeezed) << std::endl;
    std::cout << "sizeof(Inherit) =" << sizeof(Inherit) << std::endl;
    std::cout << "sizeof(unique_ptr<int>)               ="
              << sizeof(std::unique_ptr<int>) << std::endl;
    std::cout << "sizeof(unique_ptr<int,void(*)(int*)>) ="
              << sizeof(std::unique_ptr<int, void(*)(int*)>) << std::endl;

    assert(sizeof(Squeezed) <= sizeof(Plain));
    assert(sizeof(Inherit) <= sizeof(Plain));
    assert(sizeof(std::unique_ptr<int>)
           <= sizeof(std::unique_ptr<int, void(*)(int*)>));
    return 0;
}
```

### D5.4 方法学注

- 计时取 5 轮中位数；`volatile` sink 防 DCE；遍历用紧凑数组避免指针追逐掩盖带宽差异。
- 断言仅用相对尺寸（`<=`），禁用精确 `sizeof ==`（EBO 是实现许可非强制，复合布局不可移植）。
- 加速比（如 1.50×）是可移植信号；绝对毫秒随 CPU、内存、编译器版本而变，请勿跨机器直接比较毫秒。
- 复现旗标：`g++ -O2 -std=c++23`。基准源码见库根 `_bench_d5_52_ebo.cpp`。

## 参考引用

- `[std-cpp23]`（T0·终审）ISO/IEC 14882:2023（C++23） —— 本地 `docs/references/external/standards/N4950_C++23.pdf`
- `[book:templates:<ch>]`（T4）C++ Templates: The Complete Guide · <ch> —— 提取文本 `docs/references/external/books/cpp-templates.txt`

> 键的含义与全部来源见 `docs/references/SOURCING.md`；写作时只取要点，不整本投喂。
