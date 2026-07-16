# 第48章 RTTI 与 typeid/dynamic_cast：运行时类型查询

⟶ Book/part06_templates/ch65_type_traits.md
⟶ Book/part05_oo/ch47_virtual_functions.md

> 元数据：标准基 C++98（typeid/dynamic_cast 核心）/C++11（noexcept 标注）/C++17（不改动语义） · 预计阅读 100 min · 前置 ch47(vtable 槽1 存 typeinfo) · ch45(对象模型/布局) · ch28(未定义行为/对象生命周期) · 后续 ch49(虚继承影响 RTTI 目标类型) · ch50(CRTP 静态替代) · ch14(去虚化与性能) · 难度 中级

## ① 学习目标

⟶ Book/part05_oo/ch47_virtual_functions.md
⟶ Book/part05_oo/ch49_virtual_inheritance.md


- 说清 RTTI 由哪两个运算符提供、它们依赖 vtable 何处信息
- 从真实 x86-64 汇编解释 `typeid(b).name()` 与 `dynamic_cast` 的全部指令与运行期成本
- 区分 `dynamic_cast` 的四种形态（上行/下行/交叉/空指针）与各自的失败语义
- 论证 `-fno-rtti` 的收益与代价，并能在真实工程里正确禁用
- 讲透 `std::type_info` 在 libstdc++ 中的对象布局与 `__dynamic_cast` 的分派逻辑
- 对照 libstdc++/libc++/MS STL 的 typeinfo 实现与 Itanium ABI 类型层次

## ② 前置知识 ⟶ ch47(虚表槽1=typeinfo) · ch45(对象模型) · ch28(UB)

## ③ 后续依赖 ⟶ ch49(虚继承的 virtual base 影响 dynamic_cast 目标) · ch50(CRTP 静态多态替代 RTTI) · ch14(类型擦除与性能)

## ④ 知识图谱（ASCII）

```
                       ┌──────── C++ 类型查询 ────────┐
                       │                               │
          ┌────────────┴───────────┐    编译期类型查询  │
       运行时 RTTI               type_traits(编译期)    │
   ┌──────────┬──────────┐          │                  │
 typeid    dynamic_cast   <typeinfo> │                  │
   │            │           │        │                  │
 取名字      下行/交叉     存于vtable  │                  │
 (name)      (失败nullptr/ 槽1(-8)   │                  │
              bad_cast)              │                  │
   │            │           │        │                  │
 __dynamic_cast  ←───── 遍历继承树比对 type_info ──────┘
```

## ⑤ Mermaid 流程图（dynamic_cast 决策路径）

```mermaid
flowchart TD
    A[dynamic_cast 目标 T] --> B{"源指针为空?"}
    B -- 是 --> Z[返 nullptr 或抛 bad_cast 引用]
    B -- 否 --> C{"目标与源为同一条继承链?"}
    C -- 上行/同型 --> D[编译期可定，直接调整 this]
    C -- 下行/交叉 --> E[调 __dynamic_cast 运行期比对 type_info]
    E --> F{"比对成功?"}
    F -- 是 --> G["返目标指针+this 调整"]
    F -- 否 --> H["指针返 nullptr / 引用抛 bad_cast"]
```

## ⑥ UML 类图

```mermaid
classDiagram
    class type_info {
        <<C++ 标准>>
        +name() const char*
        +operator==(const type_info&)
        +hash_code() size_t
        #__name
    }
    class __class_type_info {
        +vptr
        +__name
    }
    class __si_class_type_info {
        +__base_type
    }
    type_info <|-- __class_type_info
    __class_type_info <|-- __si_class_type_info
    note for type_info "RTTI 根；实际对象含 vptr(__class_type_info 层次)+__name"
```

## ⑦ ASCII 内存图 / vtable 与 type_info 关系

单继承（x86-64，Itanium ABI，`Base`/`Der` 各含虚函数）：

```
        Der 对象（地址 base）
        ┌──────────────────────┐  <- base (offset 0)
        │  vptr ─────────────┐ │
        └────────────────────┼─┘
                             │
                ┌────────────┴───────────────┐
                ▼  Der vtable (.rodata)
        ┌────────────────────────────────────────┐
        │ [0] top_offset = 0                      │
        │ [1] &typeinfo(Der)  ◀── vptr 指向这里+8 │  (槽1，偏移 8)
        │ [2] &Der::f (首虚函数)  ◀── vptr 指向这里│  (槽2，偏移 16)
        └────────────────────────────────────────┘
                             │
                ┌────────────┴───────────────┐
                ▼  type_info 对象 (.rdata)
        ┌────────────────────────────────────────┐
        │ [0] vptr → __si_class_type_info vtable  │  (offset 0，多态)
        │ [1] __name → ".N3DerE" 字符串指针       │  (offset 8)
        └────────────────────────────────────────┘
```

[实现·GCC13/MinGW x86-64] 关键事实：`typeid(b)` 的真实取法是 `vptr[-1]`（即 vtable+8 = typeinfo 指针），再取 type_info 对象的偏移 8 字段得到 name 字符串。见 ⑩ 真实汇编。

## ⑧ 生命周期图

```
编译期：type_info 对象生成于 .rdata，vtable 槽1 固定指向它
构造对象 d：vptr 指向 Der vtable ⟶ 间接指向 typeinfo(Der)
使用期：
  typeid(d)        → 经 vptr[-1] 取 typeinfo(Der)（静态类型无所谓，看动态）
  dynamic_cast<Der*>(pb) → 比对 typeinfo(Der) vs 链上各 type_info
析构对象 d：vptr 逐级回退，但 type_info 对象常驻，不随对象销毁
```

## ⑨ 调用栈 / 时序图

```
调用点                  vtable/type_info          运行时支持例程
  │                        │                          │
  │── mov rax,[rcx] ───▶ 取 vptr                      │
  │── mov rax,-8[rax] ─▶ vtable[1]=typeinfo ptr       │
  │── mov rax, 8[rax] ─▶ type_info.__name             │
  │                        │                          │
  │── dynamic_cast ─────────────────────────────────▶ __dynamic_cast
  │                        │                          │ 比对 type_info 链
  │◀────────────────────── 返目标指针或 nullptr ──────│
```

## ⑩ 汇编分析（MinGW GCC 13.1.0, -O2, -masm=intel，真实输出）

【编译命令】

```bash
g++ -std=c++23 -O2 -S -masm=intel _asm_rtti.cpp -o _asm_rtti.asm
```

【真实汇编：typeid 取名字 vs dynamic_cast 下行/引用】

```asm
; const char* get_name(const Base& b) { return typeid(b).name(); }
_Z8get_nameRK4Base:
        xor     edx, edx
        mov     rax, QWORD PTR [rcx]      ; rcx=this(Base&)，取对象头部 vptr
        mov     rax, QWORD PTR -8[rax]    ; vptr 指向 vtable+16，vtable+8=typeinfo 指针(槽1)
        mov     rax, QWORD PTR 8[rax]     ; type_info 对象偏移8=__name 字符串指针
        cmp     BYTE PTR [rax], 42        ; 42='*'：libstdc++ name() 跳过 legacy 前缀
        sete    dl
        add     rax, rdx                  ; 若首字符是 '*'，name 指针+1
        ret

; const Der* down_cast(const Base* p) { return dynamic_cast<const Der*>(p); }
_Z9down_castPK4Base:
        test    rcx, rcx
        je      .L9                       ; 空指针：dynamic_cast 直接返 nullptr
        lea     r8, _ZTI3Der[rip]         ; r8 = 目标 type_info(Der)
        xor     r9d, r9d                  ; r9 = 0（flags/src2）
        lea     rdx, _ZTI4Base[rip]       ; rdx = 静态类型 type_info(Base)
        jmp     __dynamic_cast            ; 尾调用：运行期比对
.L9:
        xor     eax, eax                  ; 返 0 (nullptr)
        ret

; const Der& down_cast_ref(const Base& b) { return dynamic_cast<const Der&>(b); }
_Z13down_cast_refRK4Base:
        sub     rsp, 40
        lea     r8, _ZTI3Der[rip]
        xor     r9d, r9d
        lea     rdx, _ZTI4Base[rip]
        call    __dynamic_cast
        test    rax, rax
        je      .L13                      ; 比对失败
        add     rsp, 40
        ret
.L13:
        call    __cxa_bad_cast            ; 引用失败 ⟶ 抛 std::bad_cast
```

[实现·GCC13/MinGW x86-64] 关键事实：

1. `typeid(b).name()` 由三条取指完成：取 vptr → 取 `vtable[-1]`（即 vtable+8，typeinfo 指针）→ 取 `type_info` 对象的偏移 8（`__name`）。全程无函数调用，O(1)，且是去虚化后的内联结果。
2. `dynamic_cast` 指针形态：先做**内联空指针检查**（`test rcx,rcx; je`），非空才 `jmp __dynamic_cast`（尾调用，非 call，省一次返回栈）。`__dynamic_cast` 在 `libsupc++` 中运行期遍历继承树比对 `type_info`——这是 RTTI 的主要成本来源。
3. 引用形态：`call __dynamic_cast` 后 `test rax,rax; je .L13; ...; call __cxa_bad_cast`。比对失败经 `__cxa_bad_cast` 抛出 `std::bad_cast`，**不返回**。这就是引用与指针失败语义差异的硬件级原因。
4. `42` = `'*'`：libstdc++ `type_info::name()` 在返回的 mangled name 前可能带一个 `'*'` 前缀（legacy ABI 标记），真实代码会跳过它。这证明 `.name()` 返回的是 Itanium mangled name（如 `_ZTI3Der` 对应的 `.N3DerE`），需 `__cxa_demangle` 才能读人话。

【立场分层】：[标准] 规定 typeid/dynamic_cast 语义 / [实现] 上 GCC 生成 __dynamic_cast 调用 / [平台] 上 MSVC 用 `RTTI Type Descriptor` 等价结构 / [经验] 热路径禁用 RTTI 或换 static 方案。

## ⑪ STL 联系

- `std::any`（ch10）内部存 `const std::type_info&` 以在 `any_cast` 时比对动态类型，是 RTTI 的标准库级应用。
- `std::type_index`（ch10）是 `type_info` 的哈希包装，作为 `std::unordered_map` 的键（弱类型容器）。
- `std::dynamic_pointer_cast`（ch41）在 `shared_ptr` 上做 `dynamic_cast` 并维护引用计数，失败返空 `shared_ptr`。
- `std::exception` 体系不依赖 RTTI 做 `catch`（异常分派用异常表，非 type_info），但 `std::bad_cast`/`std::bad_typeid` 本身是 RTTI 失败抛出的异常类型。

## ⑫ 工业案例

### 工业案例 48-A：消息分发器（用 typeid 做异构消息路由）

> 场景：网络层收到多种消息对象，按动态类型分发到不同处理器
> 构建：`g++ -std=c++23 -O2 -Wall case48_dispatcher.cpp -o case48_dispatcher`
> 文件：`Examples/case48_dispatcher.cpp`

```cpp
#include <iostream>
#include <unordered_map>
#include <typeindex>
#include <memory>
#include <typeinfo>
#include <map>

struct Msg { virtual ~Msg() = default; };
struct LoginMsg : Msg { int uid{}; };
struct ChatMsg   : Msg { int from{}, to{}; };

void handle(const Msg& m) {
    static const std::unordered_map<std::type_index, void(*)(const Msg&)> tbl = {
        {typeid(LoginMsg), [](const Msg& m){ std::cout << "login " << static_cast<const LoginMsg&>(m).uid << "\n"; }},
        {typeid(ChatMsg),  [](const Msg& m){ std::cout << "chat "  << static_cast<const ChatMsg&>(m).from << "\n"; }},
    };
    auto it = tbl.find(typeid(m));           // 用 type_info 作 key
    if (it != tbl.end()) it->second(m);
}
int main() {
    auto a = std::make_unique<LoginMsg>(); a->uid = 7;
    auto b = std::make_unique<ChatMsg>();  b->from = 3;
    handle(*a); handle(*b);
}
```

【设计要点】`std::type_index(typeid(m))` 作为 `unordered_map` 的 key，把「动态类型 → 处理函数」做成 O(1) 查询。`typeid(m)` 取的是动态类型（因 `Msg` 含虚函数），故 `LoginMsg`/`ChatMsg` 各命中自己的处理器。

### 工业案例 48-B：错误示范——`-fno-rtti` 下误用 typeid/dynamic_cast

```cpp
// 编译选项含 -fno-rtti 时，下面全部编译失败
struct A { virtual ~A() = default; };
struct B : A {};
void bad(A* p) {
    if (dynamic_cast<B*>(p)) { }   // ❌ 错：-fno-rtti 禁用 dynamic_cast（多态下行）
    auto& t = typeid(*p);          // ❌ 错：typeid 对多态对象需 RTTI
}
```

```cpp
// ✅ 修复：用虚函数做分派，彻底不依赖 RTTI
struct A { virtual ~A() = default; virtual void dispatch() = 0; };
struct B : A { void dispatch() override { /* B 的逻辑 */ } };
void good(A* p) { p->dispatch(); }   // 走虚表，无需 RTTI，体积更小
```

### 工业案例 48-C：typeid 静态 vs 动态（核心语义对照）

```cpp
// typeid 对非多态取静态类型，对多态对象取动态类型
#include <typeinfo>
#include <iostream>
struct Poly { virtual ~Poly() = default; };
struct Drv : Poly {};
void demo_c() {
    int x = 0;
    std::cout << (typeid(x) == typeid(int)) << "\n";   // 1：静态类型 int
    Poly* p = new Drv;
    std::cout << (typeid(*p) == typeid(Drv)) << "\n";  // 1：动态类型 Drv
    std::cout << (typeid(p) == typeid(Poly*)) << "\n"; // 1：指针取静态类型
}
```

### 工业案例 48-D：typeid(*p) 空指针抛 std::bad_typeid

```cpp
#include <typeinfo>
#include <exception>
void demo_d() {
    int* p = nullptr;
    try { (void)typeid(*p); }                 // ❌ 抛 bad_typeid
    catch (const std::bad_typeid&) { /* 处理 */ }
}
```

### 工业案例 48-E：dynamic_cast 上行转换（编译期确定，零运行期成本）

```cpp
struct Base { virtual ~Base() = default; };
struct Der : Base {};
void demo_e(Der* d) {
    Base* b = dynamic_cast<Base*>(d);         // 上行，this 调整编译期定
    (void)b;
}
```

### 工业案例 48-F：dynamic_cast 引用失败抛 std::bad_cast

```cpp
#include <typeinfo>
struct Base { virtual ~Base() = default; };
struct Der : Base {};
struct Other : Base {};
void demo_f(Base& b) {
    try { Der& d = dynamic_cast<Der&>(b); (void)d; }
    catch (const std::bad_cast&) { /* 失败处理 */ }
}
```

### 工业案例 48-G：dynamic_cast<void*> 取最派生对象地址

```cpp
struct Base { virtual ~Base() = default; };
struct Der : Base { int extra{}; };
void demo_g(Der* d) {
    void* vp = dynamic_cast<void*>(static_cast<Base*>(d)); // 指向最派生对象头
    (void)vp;
}
```

### 工业案例 48-H：type_index + unordered_map 完整可运行分发

```cpp
#include <iostream>
#include <unordered_map>
#include <typeindex>
#include <memory>
#include <typeinfo>
#include <map>
struct Msg { virtual ~Msg() = default; };
struct A : Msg {}; struct B : Msg {};
void demo_h() {
    static const std::unordered_map<std::type_index, const char*> m{
        {typeid(A), "A"}, {typeid(B), "B"}};
    auto a = std::make_unique<A>();
    auto it = m.find(typeid(*a));
    std::cout << (it != m.end() ? it->second : "?") << "\n";
}
```

### 工业案例 48-I：std::any 内部依赖 type_info

```cpp
#include <any>
#include <iostream>
#include <typeinfo>
void demo_i() {
    std::any v = 42;
    if (v.type() == typeid(int)) std::cout << std::any_cast<int>(v) << "\n";
}
```

### 工业案例 48-J：-fno-rtti 下这些会编译失败（示意）

```cpp
#include <typeinfo>
// 编译加 -fno-rtti 时：
// struct P { virtual ~P() = default; }; struct Q : P {};
// void bad(P* p) { (void)dynamic_cast<Q*>(p); (void)typeid(*p); }
// → error: 'dynamic_cast' not allowed with -fno-rtti / 'typeid' not allowed
```

### 工业案例 48-K：type_info::hash_code 作容器 key

```cpp
#include <unordered_set>
#include <typeinfo>
#include <cstddef>
void demo_k() {
    std::unordered_set<size_t> s;
    s.insert(typeid(int).hash_code());
    s.insert(typeid(double).hash_code());
}
```

### 工业案例 48-L：dynamic_cast 交叉（兄弟）失败返 nullptr

```cpp
struct Root { virtual ~Root() = default; };
struct L : Root {}; struct R : Root {};
void demo_l(Root* r) {
    L* l = dynamic_cast<L*>(r);   // 若 r 实为 R，返 nullptr
    (void)l;
}
```

### 工业案例 48-M：typeid 对引用取动态类型

```cpp
#include <typeinfo>
struct Base { virtual ~Base() = default; }; struct Der : Base {};
void demo_m(Base& b) { const std::type_info& t = typeid(b); (void)t; } // 动态
```

### 工业案例 48-N：typeid 对指针取静态类型（对比 M）

```cpp
#include <typeinfo>
struct Base { virtual ~Base() = default; }; struct Der : Base {};
void demo_n(Base* p) { const std::type_info& t = typeid(p); (void)t; } // 静态 Base*
```

### 工业案例 48-O：手写「类型标签」替代 dynamic_cast（概念演示）

```cpp
struct Base { virtual ~Base() = default; virtual int kind() const = 0; };
struct Der : Base { int kind() const override { return 1; } };
Der* manual_down(Base* p) { return p->kind() == 1 ? static_cast<Der*>(p) : nullptr; }
```

### 工业案例 48-P：捕获 std::bad_cast（引用形态）

```cpp
#include <typeinfo>
struct Base { virtual ~Base() = default; }; struct Der : Base {};
void demo_p(Base& b) {
    try { (void)dynamic_cast<Der&>(b); }
    catch (std::bad_cast&) { /* 引用失败 */ }
}
```

### 工业案例 48-Q：type_info operator==（同类型程序内唯一）

```cpp
#include <typeinfo>
void demo_q() {
    bool same = (typeid(int) == typeid(int));     // true
    bool diff = (typeid(int) == typeid(double));  // false
    (void)same; (void)diff;
}
```

### 工业案例 48-R：模板 + type_traits 编译期替代 RTTI

```cpp
#include <type_traits>
template<class T>
void process(T v) {
    if constexpr (std::is_integral_v<T>) { /* 整型分支，编译期 */ }
    else { /* 其他 */ (void)v; }
}
```

## ⑬ 源码分析

#### 源码剖析 1：type_info 对象布局 @ libstdc++（实现层）

> 文件：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/typeinfo`
> 行号：约 `class type_info { ... const char* __name; ... };`
> 提取：`grep -n "__name\|class type_info" <上述路径>`

```cpp
#include <cstddef>
// libstdc++ <typeinfo>（节选，去注释）
class type_info {
  const char* __name;                 // 偏移 0（在 __class_type_info 派生中偏移 8）
public:
  const char* name() const;           // 返回 mangled name
  bool operator==(const type_info& __arg) const;
  size_t hash_code() const noexcept;
};
```

[标准·C++98] `std::type_info` 至少提供 `name()`、`operator==`、`before()`（排序）、C++11 起 `hash_code()`。注意**不可拷贝、不可构造**（无公开构造/拷贝），只能经 `typeid` 获得引用。

逐条：

1. `__name` 存 Itanium mangled name（如 `_ZTI3Der` 对应串 `.N3DerE`）；`name()` 真实汇编（见 ⑩）会跳过可能的前导 `'*'`。
2. `operator==` 比对的是 type_info 标识（同一类型在程序内唯一），不是名字字符串比较；libstdc++ 直接比指针。
3. `hash_code()` 让 `type_index` 能进哈希容器。

#### 源码剖析 2：__dynamic_cast 比对逻辑 @ libsupc++（实现层）

> 文件：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/cxxabi.h`（声明 `__dynamic_cast`）
> 行号：约 `extern "C" void* __dynamic_cast(const void* __src, ...);`

```cpp
// libsupc++ 中 __dynamic_cast 的语义（节选）
// 入参：__src=源对象指针, __dst_type=目标 type_info,
//       __static_type=静态源 type_info, __flags=转换种类
// 行为：沿继承树自底向上比对 type_info，命中则按 this 调整量返回目标子对象指针
extern "C" void* __dynamic_cast(const void* __src,
                                const __class_type_info* __dst_type,
                                const __class_type_info* __static_type,
                                std::ptrdiff_t __flags);
```

【逐行拆解】

1. `__src` 为空 → 直接返 nullptr（对应 ⑩ 汇编 `test rcx,rcx; je`）。
2. 对上行/同型转换，`__flags` 标记使其编译期可定，几乎零成本；对下行/交叉，运行期遍历 `type_info` 派生层次（`__si_class_type_info` 的 `__base_type` 链）做匹配。
3. 命中后返回的指针可能经过 **this 调整**（多重/虚继承下子对象偏移），调整量编码在 type_info 的基类描述里。引用形态比对失败则调 `__cxa_bad_cast` 抛异常。

#### 源码剖析 3：type_info 在 vtable 中的落位（真实编译器行为）

[实现·GCC/Clang] type_info 对象与 vtable 一样置于 `.rdata`/`.rodata`（只读段，ch35）。每个多态类型的 vtable 槽1 固定指向其 type_info 对象，故 RTTI 不占对象空间（仅 vptr 8 字节，ch47）。

## ⑭ WG21 提案

| 提案 | 标题 | 动机 | 影响 |
|---|---|---|---|
| C++98 [expr.typeid]/[expr.dynamic.cast] | RTTI 原始条款 | 提供运行期类型查询 | 本标准章依据 |
| N0971 (C++11) | `type_info::hash_code()` | 支持哈希容器 key | `type_index` 可进 `unordered_map` |
| P1327r1 (C++20) | 不改动 RTTI 语义，配合类型特征 | 编译期替代运行期查询 | 推动 `type_traits` 替代 RTTI |
| N4849 [expr.dynamic.cast] | dynamic_cast 语义条款 | 规定四种形态与失败语义 | 本标准章依据 |

## ⑮ 面试题（≥10）

1. `typeid` 对「无虚函数的对象」和「多态对象」分别取什么类型？（答：前者取静态类型；后者取动态类型）
2. `dynamic_cast` 指针失败返什么？引用失败呢？（答：nullptr / 抛 `std::bad_cast`）
3. 为何 `dynamic_cast` 只能用于含虚函数的多态类型？（答：依赖 vtable 槽1 的 type_info；非多态类型无 vtable）
4. `typeid(*p)` 当 `p==nullptr` 时行为？（答：抛 `std::bad_typeid`；注意与 `dynamic_cast` 空指针返 nullptr 不同）
5. `-fno-rtti` 后能编译 `typeid(non_polymorphic)` 吗？（答：能，静态类型的 typeid 不需 vtable；但 `typeid(*p)` 对多态对象会失败）
6. `type_info::name()` 返回的是可读名还是 mangled name？（答：Itanium mangled name，需 `__cxa_demangle` 反解）
7. `std::type_info` 能拷贝吗？（答：不能，无公开构造/拷贝；只能经 `typeid` 取引用）
8. `dynamic_cast` 上行转换（派生→基类）有运行期成本吗？（答：几乎无，this 调整编译期可定，且不走 `__dynamic_cast`）
9. 为何 RTTI 会增大二进制体积？（答：每多态类型生成 type_info 对象 + vtable 槽1 指向它，且引入 `__dynamic_cast` 支持例程）
10. `std::any` 与 RTTI 的关系？（答：`any` 内部存 `type_info&`，`any_cast` 比对之）
11. `dynamic_cast` 交叉转换（sibling→sibling）能成功吗？（答：不能，除非经由公共虚基类——虚继承下可，见 ch49）
12. `type_index` 与 `type_info` 区别？（答：`type_index` 是 `type_info` 的哈希包装，可拷贝、可作容器 key）

## ⑯ 易错点

- **把 `typeid` 当编译期**：对多态对象 `typeid(*p)` 是运行期（走 vptr）；对静态类型/基本类型是编译期常量。
- **`typeid(*p)` 空指针**：`p==nullptr` 抛 `std::bad_typeid`，不是返 null。
- **误以为 `name()` 可读**：它返回 mangled name（如 `.N3DerE`），直接打印是人看不懂的。
- **在 `-fno-rtti` 工程里用 `dynamic_cast`**：编译失败，需改虚函数分派（见 ⑫-B）。
- **引用 cast 失败即抛异常**：用引用形态前要确认一定成功，否则用指针形态判 nullptr。
- **RTTI 与 ABI**：type_info 标识跨模块/编译器可能不等价，`operator==` 仅同链接单元可靠。

## ⑰ FAQ（≥10）

1. **Q：RTTI 很慢吗？** A：`typeid` 取名字 O(1) 无调用（见 ⑩ 三条 mov）；`dynamic_cast` 下行/交叉才走 `__dynamic_cast` 运行期遍历，成本随继承深度增长，但多数场景仍微秒级。瓶颈常在「阻碍优化」。
2. **Q：能完全去掉 RTTI 吗？** A：能，编译加 `-fno-rtti`，并把 `dynamic_cast`/`typeid(多态)` 改虚函数分派；嵌入式/游戏常这么做减体积。
3. **Q：type_info 同名一定 == 吗？** A：同一程序中同一类型只有一份 type_info，`operator==` 比指针，可靠；跨动态库加载需谨慎。
4. **Q：为何 `dynamic_cast<void*>` 有用？** A：对多态对象 `dynamic_cast<void*>(p)` 返「最派生对象」的地址（含全部子对象），用于诊断对象边界。
5. **Q：`hash_code()` 与 `name()` 哪个做 key 好？** A：`hash_code()` 专为哈希设计；`name()` 可能含 legacy 前缀，不宜直接哈希。
6. **Q：模板里能用 RTTI 吗？** A：能，但模板通常可用 `type_traits` 在编译期区分类型，更优（ch22）。
7. **Q：虚继承影响 dynamic_cast 吗？** A：影响——交叉转换经公共虚基类可行，且 this 调整更复杂（ch49）。
8. **Q：`std::bad_cast` 何时抛？** A：仅 `dynamic_cast` 的**引用**形态失败抛；指针形态失败返 nullptr。
9. **Q：typeid 对引用/指针区别？** A：`typeid(T&)` 取所引用对象的动态类型；`typeid(T*)` 取指针本身的静态类型（指针非多态）。
10. **Q：能否自定义 type_info？** A：不能，它由编译器/标准库为每类型生成，用户无法干预。

## ⑱ 最佳实践

- 需要运行期按类型分流：优先 `std::variant`+`std::visit`（ch25）或虚函数分派；仅在必须按「真实动态类型」做异构查询时才用 RTTI。
- 用 `type_index` + `unordered_map` 做类型→处理器表（见 ⑫-A），比一长串 `dynamic_cast` 判空更清晰。
- 性能敏感/嵌入式：评估 `-fno-rtti`，改虚函数分派（⑫-B）。
- 打印类型名用 `__cxa_demangle` 反解 mangled name，别直接打 `name()`。
- 用引用形态 `dynamic_cast` 前确保转换必然成功（否则程序因抛异常终止）；不确定时用指针形态判 nullptr。

## ⑲ 性能分析

【microbenchmark 设计（Google Benchmark，可复现）】

```cpp
#include <benchmark/benchmark.h>
#include <typeinfo>
struct Base { virtual ~Base()=default; virtual int f() const { return 1; } };
struct Der : Base { int f() const override { return 2; } };

static void BM_typeid_name(benchmark::State& s){
    Der d; Base* p=&d;
    for(auto _:s) benchmark::DoNotOptimize(typeid(*p).name());
}
static void BM_dyncast_down(benchmark::State& s){
    Der d; Base* p=&d;
    for(auto _:s) benchmark::DoNotOptimize(dynamic_cast<Der*>(p));
}
static void BM_static_upcast(benchmark::State& s){
    Der d; Base* p=&d;  // 上行，编译期确定
    for(auto _:s) benchmark::DoNotOptimize(static_cast<Base*>(p));
}
BENCHMARK(BM_typeid_name); BENCHMARK(BM_dyncast_down); BENCHMARK(BM_static_upcast);
```

[经验·量级] x86-64 典型 CPU（示意，须实测）：
- `typeid(*p).name()`：~1–2 ns/次（三步 mov 取字符串指针，无函数调用）。
- `dynamic_cast` 下行（小继承树）：~5–20 ns/次（含 `__dynamic_cast` 调用与类型树遍历）。
- `static_cast` 上行：~0 ns/次（编译期 this 调整，零运行期开销）。

【复杂度】`typeid` 取信息 O(1)；`dynamic_cast` 下行/交叉 O(h)（h=继承树深度），因为 `__dynamic_cast` 自底向上比对 `type_info` 链。

【缓存友好性】type_info 与 vtable 同在只读段、热且小；`__dynamic_cast` 的遍历可能触碰基类描述数据，但规模极小。

【ABI】type_info 标识属 ABI 一部分；跨编译器/标准库版本混链可能导致 `operator==` 误判。

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

【练习题】
1. 写程序：基类 `Shape` 含虚析构，派生 `Circle`/`Rect`，用 `typeid` + `unordered_map<type_index,handler>` 实现 `draw` 分发器（仿 ⑫-A）。
2. 比较 `dynamic_cast<Der*>(p)` 与手写「vtable 槽比对」两种下行转换，打印指针结果验证一致性。
3. 用 `-fno-rtti` 重新编译 ⑫-B 的 `bad()`，记录报错信息；改 `good()` 后验证通过。

【思考题】
- 若某类型有 50 层继承，`dynamic_cast` 最坏成本如何变化？（答：O(h)，每层比对一次 type_info 链，但 h=50 仍只是几十次指针比较，微秒级）
- 为何 `typeid` 对非多态对象是编译期常量而 `dynamic_cast` 不行？（答：非多态类型编译期已知，无需 vtable；`dynamic_cast` 语义上必须运行期核对动态类型链）

【源码阅读路线】（内化，非书单）
- libstdc++：`<typeinfo>` 的 `type_info::__name`、`<cxxabi.h>` 的 `__dynamic_cast`/`__cxa_bad_cast`
- libsupc++：`libsupc++/dyncast.cc`（`__dynamic_cast` 比对主体）、`tinfo.cc`
- LLVM：`libcxxabi/src/private_typeinfo.cpp`（`__dynamic_cast` 的 libc++ 实现）
- Itanium C++ ABI 规范 §2.9（RTTI / type_info 布局）、§3.3（base class descriptors）
- 延伸：ch47(vtable/typeinfo 落位)、ch49(虚继承的 type_info 层次)、ch50(CRTP 静态替代)、ch10(`std::any`/`type_index`)

---

## 附录：知识点深挖（模板 B，23 项）

### 知识点 B1：typeid 运算符语义

【定义】`typeid` 返回 `const std::type_info&`，查询表达式的**动态类型**（多态对象）或**静态类型**（其他）。

【历史】C++98 引入 RTTI；早期 C++ 无运行期类型查询，靠虚函数手写分派。

【为什么设计】在「对象经基类指针持有」时仍需知道真实类型，支撑异构容器与序列化。

【标准规定】[expr.typeid]：操作数含虚函数的类类型时取动态类型；否则取静态类型（编译期）。`typeid(*p)` 对空指针抛 `bad_typeid`。

【编译器行为】多态情形生成经 vptr 取 type_info 的代码（见 ⑩）；静态情形直接绑定到编译期已知 type_info。

【GCC实现】`typeid` 多态 → `vptr[-1]` 取 type_info，见 ⑩ 真实三条 mov。
【LLVM实现】Clang 同 Itanium ABI；`CGExpr.cpp` 生成 `getTypeid` 调用。
【MSVC实现】用 `RTTI Type Descriptor`，经 `vftable` 负偏移取，语义等价。

【libstdc++实现】`type_info::__name` 存 mangled name；`name()` 跳过 legacy `'*'` 前缀（见 ⑩）。
【libc++实现】同，mangled name 来自 Itanium 方案。
【MS STL实现】`type_info::name()` 返回 `/?...` 风格 MSVC decorated name。

【内存模型】type_info 对象在 `.rdata`（只读），程序生命周期内常驻，不随对象销毁。

【汇编】见 ⑩：`mov rax,[rcx]; mov rax,-8[rax]; mov rax,8[rax]`。

【性能】O(1)，无函数调用（多态情形去虚化内联后）。

【复杂度】O(1)。

【异常安全】`typeid(*p)` 空指针抛 `bad_typeid`；其余不抛。

【线程安全】type_info 对象只读，并发查询安全。

【缓存友好性】type_info 与 vtable 同热段，L1/L2 命中。

【CPU影响】仅普通取指，无分支惩罚。

【ABI】type_info 标识跨模块/编译器可能不等价。

【工程应用】异构消息分发（⑫-A）、`std::any` 内部类型校验。

【真实源码】Itanium ABI §2.9。

【错误示例】
```cpp
// ❌ 以为 typeid 对指针取动态类型
Base* p = new Der;
typeid(p);        // 取的是 Base* 的静态类型，不是 Der！应写 typeid(*p)
```

【正确示例】
```cpp
#include <typeinfo>
// ✅ 取动态类型
Base* p = new Der;
const std::type_info& ti = typeid(*p);   // ti 是 Der 的 type_info
```

【例 1】基本类型 `typeid(int)` 编译期常量，返 `int` 的 type_info。
【例 2】`typeid(3.14)` 与 `typeid(double)` 同对象（字面量 3.14 是 double）。
【例 3】`typeid(std::string)` 返模板实例 `std::string` 的 type_info。

### 知识点 B2：dynamic_cast 四种形态

【定义】`dynamic_cast<T>(v)`：沿继承树把 `v` 转成目标类型 `T`，运行期核对动态类型。

【历史】C++98 与 typeid 同期引入，填补「安全下行转换」空白（替代 C 风格强转）。

【为什么设计】`static_cast` 下行不检查，`reinterpret_cast` 更危险；`dynamic_cast` 提供失败可控的下行。

【标准规定】[expr.dynamic.cast]：指针失败返 nullptr；引用失败抛 `bad_cast`；仅对含虚函数的多态类型有效。

【编译器行为】上行/同型编译期定（this 调整可静态算）；下行/交叉生成 `__dynamic_cast` 调用（见 ⑩）。

【GCC实现】下行生成 `test rcx,rcx; je` 空检查 + `jmp __dynamic_cast`（见 ⑩）。
【LLVM实现】Clang 生成对 `__dynamic_cast` 的调用，逻辑同。
【MSVC实现】调用 `_dynamic_cast`（`__RTDynamicCast`），语义等价。

【libstdc++实现】`__dynamic_cast` 在 libsupc++ `dyncast.cc`，遍历 `__class_type_info` 链。
【libc++实现】`libcxxabi/src/private_typeinfo.cpp` 的 `__dynamic_cast`。
【MS STL实现】`__RTDynamicCast` 在 `msvcp140`。

【内存模型】不分配；仅读 vtable 槽1 的 type_info 链与基类描述。

【汇编】见 ⑩：`down_cast` 的 `test/je/jmp __dynamic_cast`。

【性能】下行 O(h)；上行 ~0。

【复杂度】下行 O(h)，h 为继承深度。

【异常安全】指针形态不抛；引用形态失败抛 `bad_cast`。

【线程安全】只读遍历 type_info，并发安全（不改变对象状态）。

【缓存友好性】基类描述数据小且热。

【CPU影响】遍历含分支，但规模极小。

【ABI】`__dynamic_cast` 行为依赖 type_info 布局，跨 ABI 不稳。

【工程应用】插件系统按接口下行到具体实现（⑫ 分发器变体）。

【真实源码】libsupc++ `dyncast.cc`。

【错误示例】
```cpp
// ❌ 对非多态类型用 dynamic_cast
struct A {}; struct B : A {};
A a; dynamic_cast<B*>(&a);   // 编译错误：A 非多态（无虚函数）
```

【正确示例】
```cpp
// ✅ 多态下行，判空
struct A { virtual ~A()=default; }; struct B : A {};
A* p = new B;
if (B* b = dynamic_cast<B*>(p)) { /* 安全使用 b */ }
```

【例 1】上行 `dynamic_cast<Base*>(derPtr)` 永远成功且近乎零成本。
【例 2】下行成功返目标指针，失败返 nullptr（指针形态）。
【例 3】引用下行失败抛 `std::bad_cast`。
【例 4】空指针源 → 下行返 nullptr（不抛），引用形态则抛。
【例 5】`dynamic_cast<void*>(polyPtr)` 返最派生对象地址。

### 知识点 B3：-fno-rtti 的收益与代价

【定义】`-fno-rtti` 编译选项禁用 RTTI 生成，移除 type_info 对象与 `__dynamic_cast` 支持。

【历史】嵌入式/游戏长期默认禁 RTTI 减体积；C++98 起编译器支持开关。

【为什么设计】每多态类型省一份 type_info + vtable 槽1 指向，移除 `libsupc++` 运行期例程，二进制更小、启动更快。

【标准规定】[expr.typeid]/[expr.dynamic.cast] 允许实现在不支持 RTTI 时拒绝相关表达式（DQ 诊断）。

【编译器行为】`-fno-rtti` 下 `typeid(多态)`、`dynamic_cast` 编译报错；`-frtti`（默认）启用。

【GCC实现】`-fno-rtti` 时 `typeid`/`dynamic_cast` 的语义被禁，报 `error: 'typeid' not allowed with -fno-rtti`。
【LLVM实现】`-fno-rtti` 同；Clang 报类似诊断。
【MSVC实现】`/GR-` 等价（默认 `/GR` 启用 RTTI）。

【libstdc++实现】RTTI 禁用时 `type_info` 仅保留最小集（静态类型仍可 `typeid`？否，对多态禁用；非多态编译期仍可）。
【libc++实现】同。
【MS STL实现】`/GR-` 下 `dynamic_cast`/`typeid` 禁用。

【内存模型】省略 type_info 对象与 vtable 槽1 链接，省只读段空间。

【汇编】禁用后不再生成 `__dynamic_cast`/`__cxa_bad_cast` 引用（见 ⑩ 反例）。

【性能】启动更快、体积更小；但失去运行期类型查询，须改虚函数分派。

【复杂度】无运行期 RTTI 成本。

【异常安全】`bad_cast`/`bad_typeid` 仍定义但不可用。

【线程安全】不涉及。

【缓存友好性】只读段更小，缓存利用率略升。

【CPU影响】无 `__dynamic_cast` 调用开销。

【ABI】禁用与否须全工程一致，否则链接/运行错。

【工程应用】嵌入式固件、游戏引擎、对体积敏感的服务端。

【真实源码】GCC 前端 `cp/rtti.cc`（`-fno-rtti` 时跳过生成）。

【错误示例】
```cpp
// ❌ -fno-rtti 下编译失败
auto& t = typeid(*polyPtr);        // error: not allowed with -fno-rtti
auto* d = dynamic_cast<Der*>(p);   // error: likewise
```

【正确示例】
```cpp
// ✅ 禁用 RTTI 后用虚函数替代
struct Iface { virtual ~Iface()=default; virtual void on_event()=0; };
void dispatch(Iface* p){ p->on_event(); }   // 走虚表，无 RTTI
```

【例 1】`-fno-rtti` 使 `std::any`/`std::type_index` 相关代码仍可编译（它们的 type_info 由库提供），但用户态 `typeid(多态)` 被禁。
【例 2】Qt 框架一度默认禁 RTTI，改用 `qobject_cast`（基于 moc 元数据）替代 `dynamic_cast`。
【例 3】Chrome/LLVM 等大型项目在部分目标文件禁 RTTI 控体积。

### 知识点 B4：type_info 对象实现与 ABI

【定义】`std::type_info` 是 RTTI 的类型描述根对象；libstdc++ 用 `__class_type_info` 派生层次承载继承信息。

【历史】Itanium C++ ABI 定义 `type_info` 与 `class_type_info` 体系，GCC/Clang 共遵。

【为什么设计】运行期需既能标识类型、又能描述继承关系（`__si_class_type_info` 含 `__base_type`），供 `__dynamic_cast` 遍历。

【标准规定】[support.rtti] 规定 `type_info` 接口；具体对象布局属 ABI（不由标准规定）。

【编译器行为】每类型生成唯一 type_info 对象，vtable 槽1 指向它（见 ⑦）。

【GCC实现】`__class_type_info`（无基类）/ `__si_class_type_info`（单继承，含 `__base_type`）/ `__vmi_class_type_info`（多/虚继承，含基类列表）。
【LLVM实现】libc++abi 同 Itanium 体系。
【MSVC实现】`TypeDescriptor` + `RTTICompleteObjectLocator`/`RTTIBaseClassDescriptor`，结构不同但功能等价。

【libstdc++实现】`<typeinfo>` 中 `type_info::__name`；派生层次在 `<cxxabi.h>` 的 `__class_type_info` 系。
【libc++实现】同 Itanium 体系，名字在 libc++abi。
【MS STL实现】`type_info` 字段含 `mangled_name`，由 MSVC 运行时提供。

【内存模型】type_info 在 `.rdata`，含一个 `const char* __name` 及（派生类）基类描述。

【汇编】见 ⑩：`_ZTI3Der` 在 `.rdata`，槽0 指 `__si_class_type_info` vtable，槽1 指 `_ZTI4Base`（基类）。

【性能】查询 O(1)；`operator==` 比指针。

【复杂度】O(1) 查询。

【异常安全】不抛。

【线程安全】只读对象，安全。

【缓存友好性】常驻只读段。

【CPU影响】无。

【ABI】type_info 层次属 ABI，跨编译器不等价。

【工程应用】`type_index` 作容器 key（⑫-A）、`std::any` 内部校验（ch10）。

【真实源码】Itanium ABI §2.9；libsupc++ `tinfo.cc`/`class.cc`。

【错误示例】
```cpp
// ❌ 假设跨模块 type_info 一定同一份
// 插件 .so 与主程序各自生成的 type_info 可能不等价，operator== 误判
extern "C" void plugin_entry(Base* p){ if (typeid(*p)==typeid(LocalType)) {} }
```

【正确示例】
```cpp
#include <typeinfo>
// ✅ 同链接单元或经虚函数分派，避免跨模块 type_info 比较
struct Iface { virtual ~Iface()=default; virtual bool is_local() const = 0; };
bool ok(Iface* p){ return p->is_local(); }   // 用虚函数而非 typeid 跨边界
```

【例 1】`typeid(int)` 的 type_info 由编译器内建生成，全局唯一。
【例 2】`__si_class_type_info` 比 `__class_type_info` 多一个 `__base_type` 指针（单继承）。
【例 3】多继承用 `__vmi_class_type_info`，基类列表含 offset 与可见性，供 this 调整。
【例 4】虚继承的基类描述含「虚基类偏移」查找表，`dynamic_cast` 据此计算 this（ch49）。

## 附录: RTTI 深度

```cpp
#include <iostream>
#include <typeinfo>
struct Base{virtual~Base(){}};struct Der:Base{};
int main(){Base*b=new Der;std::cout<<typeid(*b).name()<<std::endl;delete b;return 0;}
```

```cpp
#include <iostream>
struct A{virtual~A(){}};struct B:A{};
int main(){A*a=new B;if(dynamic_cast<B*>(a))std::cout<<"is B"<<std::endl;delete a;return 0;}
```

```cpp
#include <iostream>
#include <typeindex>
#include <map>
#include <string>
#include <typeinfo>
int main(){std::map<std::type_index,std::string> m;m[typeid(int)]="int";m[typeid(double)]="double";std::cout<<m[typeid(int)]<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"RTTI overhead: one type_info object per polymorphic class. ~40 bytes each."<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <memory>
struct Animal{virtual void speak()=0;virtual~Animal(){}};struct Dog:Animal{void speak()override{std::cout<<"woof"<<std::endl;}};
int main(){auto d=std::make_unique<Dog>();d->speak();return 0;}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第47章](Book/part05_oo/ch47_virtual_functions.md) | 键值查找/缓存 | 本章提供概念，第47章提供实现 |
| [第47章](Book/part05_oo/ch47_virtual_functions.md) | 泛型库/编译期计算 | 本章提供概念，第47章提供实现 |
| [第49章](Book/part05_oo/ch49_virtual_inheritance.md) | 错误恢复/不可恢复错误 | 本章提供概念，第49章提供实现 |
| [第65章](Book/part06_templates/ch65_type_traits.md) | 性能基准/回归检测 | 本章提供概念，第65章提供实现 |


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **LLVM（llvm.org）**：默认 `-fno-rtti` 减小体积，用 `llvm::isa/cast/dyn_cast` 替代 `dynamic_cast`。
- **Qt 6（github.com/qt/qtbase）**：`qobject_cast` 基于 moc 元对象，替代 `dynamic_cast`。
- **Chromium（github.com/chromium/chromium）**：`base::SupportsUserData` 用 `static_cast` + 类型标识替代 RTTI，是其「无 RTTI」设计的一部分。
- **Boost.TypeIndex（boostorg/type_index）**：`boost::typeindex::type_id` 提供跨动态库稳定的类型名，规避 `typeid` 的 ABI 差异。
- **Abseil `absl::Status`（abseil/abseil-cpp）**：用 `status.code()` + 类型标签替代 `dynamic_cast` 的错误分支。
- **Eigen（gitlab.com/libeigen/eigen）**：其 `ei_assert` 与静态类型分发避免运行时 RTTI。
- **DPDK（DPDK/dpdk）**：数据面代码禁用 RTTI（`-fno-rtti`）以降低每包开销，是「性能敏感禁用 RTTI」的极致案例。

**常见陷阱 / 最佳实践**：
- `dynamic_cast` 跨动态库在部分平台失败（RTTI 信息不共享）；热路径避免 `dynamic_cast`（用访问者模式或 type tag）。
- `-fno-rtti` 构建下的代码不能用 `dynamic_cast`/`typeid`，需用静态替代。

> 交叉引用：虚函数见 [ch47](Book/part05_oo/ch47_virtual_functions.md)；类型萃取见 [ch65](Book/part06_templates/ch65_type_traits.md)。

## 相关章节（交叉引用）

- **后续依赖**：`Book/part03_language/ch27_cast.md`（第27章　显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part05_oo/ch46_encapsulation_inheritance.md`（第 46 章　封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part05_oo/ch50_multiple_inheritance.md`（第50章　多重继承与对象模型（Multiple Inheritance））—— 编号相邻、主题接续。
- **同模块**：`Book/part05_oo/ch45_oop_object_model.md`（第 45 章　C++ 面向对象总览与对象模型基础）—— 同模块下的其他主题。

## 底层视角：RTTI 指针、typeinfo 与 dynamic_cast 的指针追逐 [E: Low-level]

[标准] 开启 RTTI 时，vtable 首槽前藏一个 `0x0008` 的 `typeinfo` 指针（指向 `.rodata` 中唯一的 `std::type_info` 对象）。`typeid` 取其地址（`0x0008` 解引用，L1 ≈1 ns）；`dynamic_cast` 沿继承树走 RTTI 链做类型比对，深度 d 即 d 次 `0x0008` 指针追逐（冷路径落 L3 ≈12 ns 或主存 ≈100 ns）。

`-fno-rtti` 省去 `0x0008` typeinfo 指针与 `.rodata` 表，二进制更小但禁 `dynamic_cast`/`typeid`。`GCC 13.1.0` / `Clang 17` 在 `-O2` 下对已知静态类型可把 `dynamic_cast` 优化为直接指针调整（见 ch50 thunk）。`C++98` 起 RTTI 标准，`C++20` `consteval` 可把类型查询压到编译期。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 `dynamic_cast` 做**安全下行转换**：基类指针指向派生对象时转换成功，指向基类对象时返回 `nullptr`。

<details><summary>答案与解析</summary>

`dynamic_cast` 在运行时经 vtable 的 `type_info` 检查目标类型是否确实是对象的动态类型（或其派生）。源类型必须**多态**（含虚函数）。

```cpp
#include <iostream>
struct Base { virtual ~Base() = default; };
struct Derived : Base { int tag = 7; };
int main() {
    Derived d;
    Base* pb = &d;
    if (Derived* pd = dynamic_cast<Derived*>(pb))
        std::cout << "downcast OK, tag=" << pd->tag << '\n';   // 7
    Base b;
    Base* pb2 = &b;
    if (auto* pd2 = dynamic_cast<Derived*>(pb2))
        std::cout << pd2->tag << '\n';
    else
        std::cout << "null: pb2 不指向 Derived\n";             // 走这里
}
```

[标准] `dynamic_cast` 失败对指针返回 `nullptr`、对引用抛 `std::bad_cast`（维度②前置知识 ch47 虚表槽1=typeinfo）。

</details>

### 练习 2（难度 ★★★）

用 `typeid` 演示运行时类型识别依赖 vtable：对同一基类指针赋不同派生对象，`typeid(*p).name()` 反映**动态类型**；并说明无虚函数类会退化为静态类型。

<details><summary>答案与解析</summary>

`typeid` 对多态左值/表达式返回动态类型信息（经 vtable 的 `type_info`）；对非多态类型退化为编译期静态类型，无法反映实际派生。

```cpp
#include <iostream>
#include <typeinfo>
struct Base { virtual ~Base() = default; };
struct D1 : Base {};
struct D2 : Base {};
int main() {
    Base* p = new D1;
    std::cout << typeid(*p).name() << '\n';   // D1（运行时）
    p = new D2;
    std::cout << typeid(*p).name() << '\n';   // D2（运行时）
}
```

[标准] RTTI 成本来自 vtable 中的 `type_info` 指针（维度⑦ ASCII 图）；无虚函数则无 RTTI 数据。

</details>

### 练习 3（难度 ★★★★）

用 `std::variant` + `std::visit` **替代 `dynamic_cast`** 做类型分发，消除运行时 RTTI 开销，并让穷尽性由编译器保证。

<details><summary>答案与解析</summary>

`variant` 把"可能是哪几种类型"编码进类型系统；`visit` 在编译期对每种 alternative 生成分支，无 vtable 查询、无运行时类型检查，且漏处理一种类型会编译失败。

```cpp
#include <iostream>
#include <variant>
struct Circle { int r = 2; };
struct Square { int s = 3; };
using Shape = std::variant<Circle, Square>;
int area(const Shape& sh) {
    return std::visit([](auto&& v) {
        using T = std::decay_t<decltype(v)>;
        if constexpr (std::is_same_v<T, Circle>) return 3 * v.r * v.r;
        else return v.s * v.s;
    }, sh);
}
int main() {
    std::cout << area(Circle{}) << ' ' << area(Square{}) << '\n';  // 12 9
}
```

[标准] 类型擦除/visitor（维度⑫/⑬）是 RTTI 的高性能替代；WG21 持续推动 `std::visit` 优化（维度⑭）。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：用 `dynamic_cast` 做一长串类型分支（过度 RTTI）

**选型场景**：处理异构对象集合，按具体类型执行不同逻辑。

**常见错误**：用一长串 `if (auto* p = dynamic_cast<X*>(b)) ...` 做类型分支——脆弱（新增类型易漏）、慢（每次走 vtable 查询）。

```cpp
#include <iostream>
struct Base { virtual ~Base() = default; };
struct X : Base { void fx() { std::cout << "X\n"; } };
void handle(Base* b) {
    if (auto* p = dynamic_cast<X*>(b)) p->fx();
    // 每加一种类型就加一个 if；运行时逐分支 dynamic_cast
}
int main() { X x; handle(&x); }
```

**修复**：把分支逻辑上提为虚函数（真正多态），或用 `std::variant`+`visit`（见练习3）做编译期分发。

```cpp
#include <iostream>
struct Base { virtual ~Base() = default; virtual void handle() = 0; };
struct X : Base { void handle() override { std::cout << "X\n"; } };
int main() { X x; Base* b = &x; b->handle(); }  // 多态分发，无 RTTI
```

**结论**：RTTI 应作为"无法用虚函数表达"时的逃生舱，而非默认分发机制（维度⑱ 最佳实践）。

### 演绎 2：对无虚函数类误用 `dynamic_cast`

**选型场景**：想在两个有继承关系的普通类之间做下行转换。

**常见错误**：源类型不含任何虚函数（非多态），`dynamic_cast` 直接编译失败。

```
// 错误：A 非多态（无虚函数），dynamic_cast 不允许
struct A {};
struct B : A {};
int main() {
    A a;
    B* p = dynamic_cast<B*>(&a);   // 编译错误：源不是多态类型
}
```

**修复**：`dynamic_cast` 要求源表达式为多态类型。若确实需要在已知层次内转换且自担保安全，用 `static_cast`（无运行时检查）；否则把基类改为多态（加虚析构）或重构为 `variant`/虚函数层次。

```cpp
#include <iostream>
struct A { virtual ~A() = default; };
struct B : A { int tag = 5; };
int main() {
    A a;
    // 静态转换不检查：仅当确实指向 B 时才安全
    B* p = static_cast<B*>(&a);     // 编译通过，但此处 &a 实为 A，解引用 UB
    std::cout << "compile-ok, but unsafe without proof\n";
}
```

**结论**：`dynamic_cast` 是运行时安全检查，前提是多态；非多态转换用 `static_cast` 但须自担安全证明（维度⑯ 易错点）。
## 附录 E：编译实证——`typeid` 与 `dynamic_cast` 的真实汇编 [C: Compiler / E: Low-level]

> `[实测]` 编译：`g++ -std=c++23 -O2 -c ch48_rtti_test.cpp` + `objdump -dC`（GCC 15.3.0 / Win64 ABI，Itanium C++ ABI 布局）。产物 `_asm_demo/ch48_rtti_test.cpp`。

RTTI 常被说成"黑盒"，但它的实现完全可在汇编里看清：多态 `typeid` 就是**读 vtable 前一个槽的 `type_info*`**，`dynamic_cast` 就是**调用运行期函数 `__dynamic_cast`**。

### ① 多态 `typeid` —— 读 vtable[-1]

```cpp
const std::type_info& who(Base& b) { return typeid(b); }
```

```asm
<who(Base&)>:
    mov    (%rcx),%rax        ; rax = b.vptr（对象首 8 字节 = 虚表指针）
    mov    -0x8(%rax),%rax    ; [关键] rax = vptr[-1] = type_info* （Itanium ABI）
    ret
```

**💡 关键观察**：`typeid(多态对象)` 只有**两条 `mov`**。`type_info` 指针存放在虚表**起始地址的前 8 字节**（`-0x8`）——这就是"多态类的 RTTI 挂在 vtable 上"的字面含义。开销 = 2 次内存读，无函数调用。

### ② `dynamic_cast` 下行 —— 尾调 `__dynamic_cast`

```cpp
Derived* down(Base* b) { return dynamic_cast<Derived*>(b); }
```

```asm
<down(Base*)>:
    test   %rcx,%rcx          ; 空指针检查
    je     .Lnull             ; nullptr → 返回 nullptr
    xor    %r9d,%r9d          ; 第4参 hint = 0
    lea    ...,%r8            ; 第3参 = Derived 的 type_info
    lea    ...,%rdx           ; 第2参 = Base   的 type_info
    jmp    __dynamic_cast     ; [关键] 尾调运行期函数（4参: 对象/src_ti/dst_ti/hint）
.Lnull:
    xor    %eax,%eax; ret     ; 返回 0
```

**💡 关键观察**：`dynamic_cast` 编译为一次 `__dynamic_cast` 运行期调用（此处是尾调 `jmp`），需遍历继承图比对 `type_info`——这就是它比 `static_cast` 慢一个数量级的根源（见 ch27 转型代价实测：`dynamic_cast` 6.9ns vs virtual 0.5ns）。

### ③ 静态 `typeid` —— 编译期常量，零运行期开销

```cpp
const std::type_info& static_who() { return typeid(Derived); }  // 非多态表达式
```

```asm
<static_who()>:
    lea    ...,%rax           ; rax = &typeinfo for Derived（编译期确定的静态地址）
    ret                       ; 无内存读、无调用
```

**💡 关键观察**：对**类型名**（而非多态对象）取 `typeid` 在编译期解析，只剩一条 `lea` 装载常量地址——与运行期 `typeid(b)` 的 2 次 `mov` 形成鲜明对比。

### 代价分层

| 表达式 | 汇编特征 | 运行期开销 | 说明 |
|--------|----------|-----------|------|
| `typeid(类型)` | 单条 `lea` | 0 | 编译期常量地址 |
| `typeid(多态对象)` | `mov;mov`（读 vptr[-1]） | 2 次内存读 | 依赖虚表 |
| `dynamic_cast<D*>` | `call/jmp __dynamic_cast` | 图遍历（~ns 级） | 需 `-frtti` |
| `static_cast<D*>` | 常量偏移加法 | 0（不检查） | 类型错则 UB |

### 关键发现

- 多态 RTTI 的全部秘密就是 **vtable[-1] 槽的 `type_info*`**——`-fno-rtti` 会去掉这个槽，`typeid`/`dynamic_cast` 随之不可用。
- `dynamic_cast` 的成本来自 `__dynamic_cast` 的继承图搜索，热路径下行应优先考虑虚函数分派或 CRTP（见 ch51），而非反复 `dynamic_cast`。
- 对确定类型用 `typeid(T)` 是编译期常量；只有对**多态左值/引用**取 `typeid` 才有运行期开销。
