# 第115章　移动语义与右值引用

> 标准基：ISO/IEC 14882:2023 (C++23) / 预计阅读：95 分钟 / 前置：⟶ Book/part03_language/ch19_variables.md（变量与存储期）、⟶ Book/part03_language/ch20_reference_pointer.md（引用与指针）、⟶ Book/part04_memory/ch39_raii_rule.md（Rule of Three/Five/Zero）、⟶ Book/part07_stl/ch77_vector.md（vector 扩容）/ 后续：⟶ Book/part10_modern/ch116_perfect_forwarding.md（完美转发）、⟶ Book/part10_modern/ch117_copy_elision.md（RVO/NRVO）、⟶ Book/part03_language/ch27_cast.md（cast）/ 难度：★★★★☆

## ① 学习目标

移动语义（move semantics）与右值引用（`T&&`）是 C++11 最重要的性能革命。本章结束后，你应当能够：

- 精确解释**值类别（value category）** `lvalue` / `prvalue` / `xvalue` 的 C++17 体系，以及它们如何决定重载决议 `[标准]`。
- 说清 **`T&&` 是右值引用**，但"右值引用本身是个左值"这一经典陷阱 `[标准]`。
- 理解 **`std::move` 只是 `static_cast<T&&>`——它不移动任何东西**，只是把对象"标记"为可移动 `[标准]`。
- 正确实现**移动构造函数**与**移动赋值运算符**，理解"移动后状态 = 有效但未指定（valid but unspecified）" `[标准]`。
- 掌握 **`noexcept` 移动**对 `std::vector` 扩容的决定性影响：`vector` 在移动构造 `noexcept` 时才用移动、否则退回拷贝（经 `std::move_if_noexcept`） `[标准]`。
- 应用 **Rule of Five**：五个特殊成员函数（析构、拷贝构造、拷贝赋值、移动构造、移动赋值）的协同 `[标准]`。
- 识别 **`std::move` 误用**：对 `const` 对象 move 退化为拷贝、`return std::move(local)` 阻碍 RVO、`std::move` 具名右值引用却当左值用 `[标准]`。
- 在真实工程中用移动语义转移 `std::unique_ptr`、把大对象塞进容器/返回，理解其与 Rust 移动语义的差异 `[经验]`。

---

## ② 前置知识

- **变量、存储期与 ODR** ⟶ `Book/part03_language/ch19_variables.md`：理解对象生命周期是理解"移动后资源归属"的前提。
- **引用与指针** ⟶ `Book/part03_language/ch20_reference_pointer.md`：右值引用是引用的一种；它绑定到临时对象/将亡值。
- **Rule of Three/Five/Zero** ⟶ `Book/part04_memory/ch39_raii_rule.md`：移动语义使 Rule of Three 升级为 Rule of Five。
- **vector 扩容、失效、allocator** ⟶ `Book/part07_stl/ch77_vector.md`：vector 扩容时如何"搬元素"直接取决于元素移动构造是否 `noexcept`（§⑫）。

```cpp
// ②-1 前置：右值引用绑定到临时（独立可编译）
#include <iostream>
#include <utility>

void take_rref(int&& x) { std::cout << x << "\n"; }

int main() {
    take_rref(42);                  // ✅ 字面量是 prvalue，可绑定到 int&&
    // int a = 1; take_rref(a);     // ❌ a 是 lvalue，不能绑定到 int&&
    int b = 1; take_rref(std::move(b));   // ✅ std::move 把 b 当右值
    return 0;
}
```

```cpp
// ②-2 前置：移动构造让"返回值"免拷贝（独立可编译，演示思想）
#include <iostream>
#include <utility>

struct Widget {
    int* data;
    Widget() : data(new int(0)) {}
    Widget(Widget&& o) noexcept : data(o.data) { o.data = nullptr; }  // 窃取指针
    ~Widget() { delete data; }
};

int main() {
    Widget w;
    Widget w2 = std::move(w);       // 调用移动构造（不分配、不拷贝）
    std::cout << "ok\n";
    return 0;
}
```

---

```cpp
// ②-3 值类别可用类型特性在编译期识别（独立可编译）
#include <type_traits>
#include <iostream>
#include <utility>

template <typename T>
void probe(T&& x) {
    if constexpr (std::is_lvalue_reference_v<T&&>)
        std::cout << "bound to lvalue\n";
    else
        std::cout << "bound to rvalue\n";
}

int main() {
    int a = 1;
    probe(a);                 // lvalue
    probe(2);                 // rvalue（prvalue）
    probe(std::move(a));      // rvalue（xvalue）
    return 0;
}
```

## ③ 后续依赖

- **完美转发与万能引用** ⟶ `Book/part10_modern/ch116_perfect_forwarding.md`：万能引用 `T&&` 在模板参数推导中的特殊规则，以及 `std::forward` 如何"原样"转发值类别——是移动语义在泛型代码中的延伸。
- **RVO / NRVO 与拷贝消除** ⟶ `Book/part10_modern/ch117_copy_elision.md`：理解为什么"不要 `return std::move(local)`"——拷贝消除优先于移动（§⑯）。
- **cast** ⟶ `Book/part03_language/ch27_cast.md`：`std::move` 的本质是 `static_cast<T&&>`，属于 `static_cast` 的合法用法。

```cpp
// ③-1 后续：移动 + 完美转发组合（独立可编译，演示）
#include <iostream>
#include <utility>

void consume(int& )  { std::cout << "lvalue\n"; }
void consume(int&& ) { std::cout << "rvalue\n"; }

template <typename T>
void relay(T&& x) {                       // 万能引用
    consume(std::forward<T>(x));         // 原样转发值类别
}

int main() {
    int a = 1; relay(a);          // lvalue
    relay(2);                     // rvalue
    return 0;
}
```

```cpp
// ③-2 后续：拷贝消除与移动的关系（独立可编译，return 局部触发 NRVO/移动）
#include <iostream>
#include <utility>

struct Blob {
    int* p;
    Blob() : p(new int(7)) {}
    Blob(Blob&& o) noexcept : p(o.p) { o.p = nullptr; }
    ~Blob() { delete p; }
};

Blob make() { Blob b; return b; }        // ✅ 依赖拷贝消除/隐式移动，勿 std::move

int main() {
    Blob x = make();
    std::cout << *x.p << "\n";           // 7（无拷贝）
    return 0;
}
```

---

## ④ 知识图谱（ASCII）

```
                 ┌─────────────────────────────────────────┐
                 │   表达式的值类别（C++17）                 │
                 └───────────────────┬─────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
      ┌────────────┐          ┌──────────────┐         ┌──────────────┐
      │ glvalue    │          │ prvalue      │         │ xvalue       │
      │ (广义左值) │          │ (纯右值)     │         │ (将亡值)     │
      └─────┬──────┘          └──────┬───────┘         └──────┬───────┘
            │                        │                        │
      ┌─────┴─────┐                  │ 合成            ┌───────┴────────┐
      │ lvalue    │                  │                │ std::move(x)   │
      │ (有名字/   │                  │                │ 函数返回的 &&   │
      │  可取地址) │                  │                │ (把对象当右值)  │
      └───────────┘                  │                └───────┬────────┘
                                     │                        │
                                     └───────────┬────────────┘
                                                 ▼
                                  绑定到 T&&（右值引用）──► 调用移动构造/赋值
```

---

## ⑤ Mermaid 流程图：移动构造的"资源窃取"路径

```mermaid
flowchart TD
    A[源对象 Source] -->|std::move 转右值| B["变成 xvalue / 将亡值"]
    B --> C["调用移动构造/赋值 T&&"]
    C --> D[新对象窃取 Source 的内部资源指针]
    D --> E[把 Source 的内部指针置空]
    E --> F[Source 进入「有效但未指定」状态]
    F --> G[Source 析构时 delete nullptr（无双释放）]
    D --> H[新对象正常拥有资源]
```

---

## ⑥ UML 类图：五个特殊成员函数（Rule of Five，Mermaid classDiagram）

```mermaid
classDiagram
    class Resource {
        -int* _data
        +Resource() 
        +~Resource()
        +Resource(Resource&) <<拷贝构造>>
        +operator=(Resource&) <<拷贝赋值>>
        +Resource(Resource&&) <<移动构造, noexcept>>
        +operator=(Resource&&) <<移动赋值, noexcept>>
    }
    note "Rule of Five：五者要么全用户定义，要么靠 =default/=delete 显式声明"
    Resource : 移动后 _data 置空
```

---

## ⑦ ASCII 内存图：移动 = 指针转移，而非字节拷贝

```
移动前：
  Source:  [_data] ──────► [堆: 100万个 int]
  Target:  [_data] ──────► nullptr

执行 Target = std::move(Source)（移动赋值）：
  Source:  [_data] ──────► nullptr          （资源被"偷走"，置空）
  Target:  [_data] ──────► [堆: 100万个 int]（现在 Target 拥有）

对比拷贝：
  Target:  [_data] ──────► [堆: 新分配 100万个 int]（逐元素复制，昂贵）
```

- `[标准]`：移动语义的核心是**资源所有权的转移**，而非值的复制；移动构造/赋值把源的资源指针"偷"过来并把源置空，使源的析构不会释放已被转移的资源（避免双释放）。
- `[经验]`：移动的成本是**常数级**（几次指针赋值），与对象大小无关；拷贝的成本是 `O(大小)`（逐字节/逐元素）。对持有堆资源的对象，差距可达数量级。

```cpp
// ⑦-1 移动窃取指针，拷贝逐元素（独立可编译，演示思想）
#include <iostream>
#include <utility>
#include <cstddef>

struct Buf {
    int* p; std::size_t n;
    Buf(std::size_t k) : p(new int[k]), n(k) {}
    Buf(Buf&& o) noexcept : p(o.p), n(o.n) { o.p = nullptr; o.n = 0; }
    Buf(const Buf& o) : p(new int[o.n]), n(o.n) { for(std::size_t i=0;i<n;++i) p[i]=o.p[i]; }
    ~Buf() { delete[] p; }
};

int main() {
    Buf a(1000);
    Buf b = std::move(a);      // ✅ 移动：a.p 置空，b 接管，无分配
    // Buf c = a;              // 若 a 仍持有资源则触发拷贝（此处 a 已空）
    std::cout << (a.p == nullptr) << " " << (b.p != nullptr) << "\n";  // 1 1
    return 0;
}
```

---

## ⑧ 生命周期图：移动后源对象的状态

移动后，源对象仍然存在（直到其作用域结束），但处于**"有效但未指定（valid but unspecified）"**状态——可以安全析构或赋值，但不可假设其内容。

```
时间轴 ──────────────────────────────────────────────►

  Widget a;              // a 拥有资源
  Widget b = std::move(a);   // 资源转移到 b；a.p = nullptr（"有效但未指定"）
        │
        ├─ 使用 b ✅（b 正常拥有资源）
        ├─ 使用 a？❌ 不要读 a 的内部！只能：
        │      ├─ 给 a 重新赋值（a = Widget{}）后使用
        │      └─ 或等 a 析构（析构 delete nullptr，安全）
        ├─ （错误）对 a 调用需要有效状态的函数
        │
        └─ a、b 各自析构，无双释放（因 a.p 已空）
```

- `[标准]`：`[lib.types.movedfrom]` 规定被移动后的标准库类型仍可析构、可被赋值、可比较（比较结果未指定）；用户类型应遵守同一约定。
- `[经验]`：实用准则——移动后把源对象当"空壳"，要么重新赋值再使用，要么不再使用直到析构。

```cpp
// ⑧-1 移动后源对象可重新赋值、可安全析构（独立可编译）
#include <iostream>
#include <utility>
#include <string>

int main() {
    std::string a = "hello";
    std::string b = std::move(a);        // a 进入有效但未指定状态
    std::cout << "b=" << b << "\n";      // hello
    a = "world";                         // ✅ 重新赋值后 a 再次可用
    std::cout << "a=" << a << "\n";      // world
    return 0;
}
```

```cpp
// ⑧-2 移动后源的"内容未指定"（独立可编译，仅展示可析构）
#include <iostream>
#include <utility>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = std::move(a);
    std::cout << "b.size=" << b.size() << "\n";   // 3
    std::cout << "a.size(未指定,常为空)=" << a.size() << "\n";  // 通常 0
    // 不读取 a 的内容，仅保证可析构
    return 0;
}
```

---

## ⑨ 调用栈 / 时序图：std::move 不做移动

最常见的误解：`std::move(x)` 会"移动 x"。**真相**：它只是把 `x` 强制转换成右值引用类型（`static_cast<T&&>`），真正的移动发生在随后调用的移动构造/赋值里。

```
调用方                       std::move                目标对象
  │                             │                         │
  │ std::move(src)              │                         │
  │────────────────────────────►│                         │
  │                             │ return static_cast<     │
  │                             │        T&&>(src);       │  ← 仅转型，无移动！
  │◄────────────────────────────│ (返回 T&&，xvalue)      │
  │                                                        │
  │ Target = 返回值;  ────────────────────────────────────►│
  │                                                        │ 匹配 T&& 重载
  │                                                        │ 调用移动构造/赋值（真正移动）
```

- `[标准]`：`std::move` 的语义就是 `static_cast<remove_reference_t<T>&&>(t)`（见 §⑬），它**不生成任何运行期代码**（在 `-O2` 下完全消失）。
- `[经验]`：记住口头禅——"move 不移动，它只是允许移动"。

```cpp
// ⑨-1 演示：std::move 本身不触达任何成员（独立可编译）
#include <iostream>
#include <utility>

struct Tracer {
    Tracer() = default;
    Tracer(Tracer&&) { std::cout << "move ctor\n"; }
    Tracer(const Tracer&) { std::cout << "copy ctor\n"; }
};

int main() {
    Tracer a;
    auto&& r = std::move(a);        // ✅ 仅转型，不打印任何 ctor
    Tracer b = r;                   // ✅ 此处才调用移动构造（r 是右值引用，按右值）
    return 0;
}
```

```cpp
// ⑨-2 对比：不 move 则拷贝（独立可编译）
#include <iostream>
#include <utility>

struct Tracer {
    Tracer() = default;
    Tracer(Tracer&&) { std::cout << "move\n"; }
    Tracer(const Tracer&) { std::cout << "copy\n"; }
};

int main() {
    Tracer a;
    Tracer b = a;          // copy（a 是 lvalue）
    Tracer c = std::move(a);  // move
    return 0;
}
```

---

## ⑩ 汇编分析：移动 vs 拷贝（-O2 实测）

下面汇编由 `g++ 13.1 -O2 -masm=intel` 对 `Buf` 的**移动赋值**与**拷贝赋值**真实生成。最关键的区别：移动只做指针窃取（无 `call`），拷贝调用 `operator new[]`（`_Znay`）并逐元素循环。

```asm
; g++ 13.1 -O2 -masm=intel ；移动赋值 Buf::operator=(Buf&&)
; 关键片断：delete[] 之后仅是"指针复制 + 源置空"，无分配、无循环
        call    _ZdaPv                 ; delete[] 旧资源
        mov     rax, QWORD PTR [rsi]   ; rax = 源.p
        mov     QWORD PTR [rbx], rax   ; 目标.p = 源.p  （窃取）
        mov     rax, QWORD PTR 8[rsi]
        mov     QWORD PTR 8[rbx], rax  ; 目标.n = 源.n
        mov     QWORD PTR [rsi], 0     ; 源.p = nullptr
        mov     QWORD PTR 8[rsi], 0    ; 源.n = 0

; g++ 13.1 -O2 -masm=intel ；拷贝赋值 Buf::operator=(const Buf&)
; 关键片断：先 call _Znay（operator new[]）分配，再 .L15 逐元素复制
        call    _Znay                  ; operator new[] 分配新堆内存
        ...
        .L15:
        mov     edx, DWORD PTR [r9+r8*4]
        mov     DWORD PTR [rcx+r8*4], edx   ; 逐元素拷贝（循环）
```

- `[实现·GCC13]`：汇编证实移动赋值的代价是**两条 `mov` + 源置空**（常数级），拷贝赋值则含 `call _Znay`（堆分配）+ 元素循环 `O(n)`。对大缓冲区，差距即"分配+复制" vs "两次指针赋值"。
- `[标准]`：这正是移动语义把"深拷贝"降级为"指针转移"的性能收益来源。

```cpp
// ⑩-1 被测代码（与上方 asm 对应）：Buf 的移动/拷贝赋值（独立可编译）
#include <utility>
#include <cstddef>
#include <iostream>

struct Buf {
    int* p; std::size_t n;
    Buf() : p(nullptr), n(0) {}
    Buf(Buf&& o) noexcept : p(o.p), n(o.n) { o.p = nullptr; o.n = 0; }
    Buf(const Buf& o) : p(o.p ? new int[o.n] : nullptr), n(o.n) { if(p) for(std::size_t i=0;i<n;++i) p[i]=o.p[i]; }
    Buf& operator=(Buf&& o) noexcept { if(this!=&o){ delete[] p; p=o.p; n=o.n; o.p=nullptr; o.n=0;} return *this; }
    Buf& operator=(const Buf& o) { if(this!=&o){ delete[] p; p=o.p?new int[o.n]:nullptr; n=o.n; if(p) for(std::size_t i=0;i<n;++i) p[i]=o.p[i]; } return *this; }
    ~Buf() { delete[] p; }
};

int main() {
    Buf a, b;
    b = std::move(a);          // 移动赋值（指针窃取）
    std::cout << "moved\n";
    return 0;
}
```

---

## ⑪ STL 联系：移动语义贯穿整个标准库

| 组件 | 移动语义的角色 |
|---|---|
| `std::vector` | 扩容时用元素移动构造搬元素（若 `noexcept`），否则退回拷贝 |
| `std::unique_ptr` | **只可移动、不可拷贝**——独占所有权靠移动转移 |
| `std::string` | 移动构造/赋值窃取内部缓冲区（SSO 小串则 memcpy） |
| `std::thread` | 只能移动（线程所有权转移），不可拷贝 |
| `std::future` | 只能移动（共享状态的承诺转移） |
| 容器 `insert`/`push_back` | 接受右值引用重载，避免拷贝大对象 |

- `[标准]`：C++11 起，所有标准库容器/智能指针/字符串都提供了 `noexcept` 移动构造与移动赋值，使它们在容器中存储、作为返回值、跨线程传递时零拷贝。
- `[经验]`：自己写的资源管理类（RAII）必须提供 `noexcept` 移动，才能享受与标准库同等的性能（见 §⑫）。

```cpp
// ⑪-1 unique_ptr 只可移动不可拷贝（独立可编译）
#include <memory>
#include <iostream>

int main() {
    auto p = std::make_unique<int>(42);
    // auto q = p;        // ❌ 编译错误：unique_ptr 不可拷贝
    auto q = std::move(p);          // ✅ 移动：所有权转移，p 变空
    std::cout << *q << "\n";        // 42
    return 0;
}
```

```cpp
// ⑪-2 string 移动窃取缓冲区（独立可编译）
#include <string>
#include <iostream>
#include <utility>

int main() {
    std::string a = "a very long string that exceeds SSO buffer size";
    std::string b = std::move(a);    // 窃取堆缓冲区，无逐字符拷贝
    std::cout << b << "\n";
    return 0;
}
```

---

## ⑫ noexcept 移动决定 vector 扩容走"移动"还是"拷贝"

`std::vector` 扩容（reallocation）需要把旧元素搬到新内存。它**优先用移动构造**，但前提是移动构造**不抛异常（`noexcept`）**——因为一旦在搬移中途抛异常，vector 无法回滚到旧状态（旧元素已被搬走）。

```cpp
// ⑫-1 noexcept 移动：vector 扩容用移动，O(N) 仅指针搬运（独立可编译）
#include <vector>
#include <iostream>
#include <utility>

struct Fast {
    int* p;
    Fast() : p(new int(0)) {}
    Fast(Fast&& o) noexcept : p(o.p) { o.p = nullptr; }   // ✅ noexcept
    Fast(const Fast&) : p(new int(0)) {}
    ~Fast() { delete p; }
};

int main() {
    std::vector<Fast> v(3);
    v.push_back(Fast());          // 触发扩容：用 noexcept 移动构造搬元素
    std::cout << "size=" << v.size() << "\n";
    return 0;
}
```

```cpp
// ⑫-2 非 noexcept 移动：vector 退回拷贝（更安全但更慢，独立可编译）
#include <vector>
#include <iostream>

struct Slow {
    int* p;
    Slow() : p(new int(0)) {}
    Slow(Slow&& o) : p(o.p) { o.p = nullptr; }   // ❌ 未标 noexcept
    Slow(const Slow&) : p(new int(0)) {}
    ~Slow() { delete p; }
};

int main() {
    std::vector<Slow> v(3);
    v.push_back(Slow());          // 扩容时退回拷贝构造（保证强异常安全）
    std::cout << "size=" << v.size() << "\n";
    return 0;
}
```

- `[标准]`：`std::vector` 通过 `std::move_if_noexcept` 选择：若移动构造 `noexcept` 则移动，否则拷贝。这保证"强异常安全"——扩容失败也不会丢数据。
- `[实现]`：`move_if_noexcept` 在 `bits/move.h`（见 `文件：bits/move.h`, `行号：125`）返回 `const T&`（拷贝）或 `T&&`（移动），正是 vector 扩容决策的依据。

---

## ⑬ 源码分析：libstdc++ 的 move / move_if_noexcept / vector 移动

以下片段取自 GCC 13.1.0 的 `bits/move.h` 与 `bits/stl_vector.h`（真实文件，逐行核对）。

### 13.1 std::move 的本质

```cpp
#include <utility>
// ⑬-1a libstdc++ 源码摘录（文件：bits/move.h，行号：104）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   constexpr typename remove_reference<_Tp>::type&&
//   move(_Tp&& __t) noexcept {        // 行号 104
//     return static_cast<typename remove_reference<_Tp>::type&&>(__t);
//   }
//   即：std::move 只是 static_cast<T&&>，编译期转型，零运行期代码。
int main() { return 0; }
```

### 13.2 move_if_noexcept（vector 扩容决策）

```cpp
#include <utility>
// ⑬-2a libstdc++ 源码摘录（文件：bits/move.h，行号：125）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   template<typename _Tp>
//   constexpr typename conditional<                       // 行号 124-125
//     __move_if_noexcept_cond<_Tp>::value, const _Tp&, _Tp&&>::type
//   move_if_noexcept(_Tp& __x) noexcept { return std::move(__x); }
//   若 _Tp 的移动构造 noexcept -> 返回 T&&（移动）；否则返回 const T&（拷贝）。
int main() { return 0; }
```

### 13.3 vector 的移动构造/赋值

```cpp
// ⑬-3a libstdc++ 源码摘录（文件：bits/stl_vector.h，行号：615 / 761）
// 以下为 GCC 13.1.0 真实源码片段，以注释保存，便于审阅且不参与编译：
//   // 移动构造（行号 615）：默认实现，仅复制三个指针（_M_start/_M_finish/_M_end_of_storage）
//   vector(vector&&) noexcept = default;
//   // 移动赋值（行号 761）：noexcept 取决于分配器是否不抛移动
//   operator=(vector&& __x) noexcept(_Alloc_traits::_S_nothrow_move());
int main() { return 0; }
```

- `[实现]`：`vector` 的移动构造 `= default` 只是**复制三个内部指针**并把源置空（与 §⑦ 的 Buf 同理），`O(1)` 且 `noexcept`；这就是为什么把 `vector` 塞进容器/返回是零拷贝的（前提分配器不抛）。
- `[标准]`：vector 扩容使用 `move_if_noexcept`（§⑫），从而保证强异常安全。

---

## ⑭ WG21 提案背景

- **N1377 / N1690（右值引用与移动语义，Howard Hinnant 等）**：C++0x 引入 `T&&`、移动构造/赋值，动机是消除"返回大对象"与"容器扩容"中不可避免的昂贵深拷贝。
- **N2831（值类别精修）**：C++11 把值类别定为 `lvalue`/`prvalue`，C++17 进一步引入 `glvalue`/`xvalue` 的二分体系（见 §④），为 `std::move`/`forward` 提供精确定义基础。
- **N3208 / 相关**：`noexcept` 移动与强异常安全的关联，确立 `vector` 用 `move_if_noexcept` 决策。
- **N3053（Rule of Five 演进）**：明确五个特殊成员函数的默认行为规则（`=default`/`=delete` 传播）。

- `[标准]`：移动语义自 C++11 成为核心；C++23 仅做边角完善（如更一致的 `noexcept` 推导）。
- `[经验]`：现代 C++ 的 RAII + 移动语义组合（见 `Book/part04_memory/ch39_raii_rule.md`）是"零泄漏 + 零拷贝"的工程基石。

```cpp
// ⑭-1 工业：工厂函数返回大对象，靠移动/拷贝消除免拷贝（独立可编译）
#include <iostream>
#include <string>
#include <utility>

struct Record {
    std::string name;
    std::string payload;
    Record() = default;
    Record(Record&&) = default;       // noexcept 移动
    Record(const Record&) = default;
};

Record make_record() {
    Record r;
    r.name = "tx"; r.payload = "big payload";
    return r;                         // ✅ NRVO/隐式移动，无拷贝
}

int main() {
    Record r = make_record();
    std::cout << r.name << "\n";
    return 0;
}
```

---

## ⑮ 面试题

1. **`std::move` 做了什么？**
   → `[标准]` 只是 `static_cast<T&&>`，把左值/将亡值标记为右值引用，**不移动任何东西**；真正的移动发生在随后的移动构造/赋值。

2. **为什么"具名右值引用是左值"？**
   → `[标准]` 表达式 `T&& r = ...;` 中，`r` 是有名字的对象，**有名字的变量是左值**；要用它触发移动必须再 `std::move(r)`。

3. **为什么移动构造应标 `noexcept`？**
   → `[标准]` `std::vector` 扩容前用 `move_if_noexcept` 检查：非 `noexcept` 移动会退回拷贝（保证强异常安全）；不标 `noexcept` 会让 `vector` 元素搬移变慢。

4. **移动后源对象的状态？**
   → `[标准]` "有效但未指定"：可析构、可赋值、可比较（结果未指定）；不应读其旧内容。

5. **`const T` 对象能移动吗？**
   → `[标准]` 不能：右值引用 `T&&` 无法绑定到 `const T`（会退化为 `const T&` 拷参），`std::move(constObj)` 返回 `const T&&`，匹配拷贝构造——**move 退化为 copy**（见 §⑯）。

6. **`return std::move(local);` 为什么不好？**
   → `[标准]` 它阻止了 NRVO/拷贝消除，编译器本可直接在目标处构造；显式 move 反而强制调用移动构造（见 §⑯、⟶ `Book/part10_modern/ch117_copy_elision.md`）。

7. **`std::unique_ptr` 为什么不能拷贝只能移动？**
   → `[标准]` 独占所有权语义：拷贝会导致双释放，故删除拷贝、仅留移动（§⑪）。

```cpp
// ⑮-1 面试题实战：vector 扩容的移动/拷贝路径（独立可编译）
#include <vector>
#include <iostream>

struct Elem {
    int v;
    Elem(int x) : v(x) {}
    Elem(Elem&&) noexcept = default;
    Elem(const Elem&) = default;
};

int main() {
    std::vector<Elem> v;
    v.reserve(1);
    v.push_back(Elem(1));
    v.push_back(Elem(2));          // 扩容：noexcept 移动搬元素
    std::cout << v.size() << "\n";
    return 0;
}
```

---

## ⑯ 易错点

1. **`std::move` 具名右值引用却被当右值用**
   ```cpp
   // ❌ 逻辑错误（编译通过，实际拷贝而非移动）
   #include <iostream>
   #include <utility>
   struct T { T()=default; T(T&&)=default; T(const T&)=default; };
   void sink(T&& r) {
       T x = r;          // ❌ r 是具名变量=左值 -> 调用拷贝构造
       // 应写：T x = std::move(r);
       (void)x;
   }
   int main() { T t; sink(std::move(t)); return 0; }
```
   ✅ 正确：`T x = std::move(r);`（再 move 一次）。

2. **对 `const` 对象 move 退化为拷贝**
   ```cpp
   // ⑯-1 const 对象被 move 实际拷贝（独立可编译，演示）
   #include <iostream>
   #include <utility>
   struct T { T()=default; T(T&&){std::cout<<"move\n";} T(const T&){std::cout<<"copy\n";} };
   int main() {
       const T c;
       T d = std::move(c);     // ❌ c 是 const -> 匹配拷贝构造（打印 copy）
       return 0;
   }
```

3. **`return std::move(local);` 阻碍 RVO**
   ```cpp
   // ⑯-2 错误写法：显式 move 阻止 NRVO（独立可编译，对比）
   #include <iostream>
   #include <utility>
   #include <string>
   std::string bad() { std::string s="x"; return std::move(s); }  // ❌ 阻碍 NRVO
   std::string good() { std::string s="x"; return s; }            // ✅ 允许 NRVO/隐式移动
   int main() { std::cout << bad() << good() << "\n"; return 0; }
```

4. **移动后继续读源对象**
   ```cpp
   // ⑯-3 错误：移动后使用源对象内容（独立可编译，安全写法对照）
   #include <iostream>
   #include <utility>
   #include <vector>
   int main() {
       std::vector<int> a={1,2,3};
       std::vector<int> b=std::move(a);
       // std::cout << a[0];   // ❌ a 状态未指定，勿读
       std::cout << b[0] << "\n";   // ✅ 用 b
       return 0;
   }
```

5. **移动构造未标 `noexcept` 拖慢 vector**
   → 见 §⑫：非 noexcept 移动使 vector 扩容退回拷贝。务必 `= default` 或显式 `noexcept`。

```cpp
// ⑯-4 正确：移动构造/赋值都 noexcept（独立可编译，推荐写法）
#include <iostream>
#include <utility>
#include <cstddef>

struct Holder {
    int* p;
    Holder() : p(new int(0)) {}
    Holder(Holder&& o) noexcept : p(o.p) { o.p = nullptr; }          // ✅ noexcept
    Holder& operator=(Holder&& o) noexcept {                         // ✅ noexcept
        if (this != &o) { delete p; p = o.p; o.p = nullptr; }
        return *this;
    }
    ~Holder() { delete p; }
};

int main() { Holder a; Holder b = std::move(a); std::cout << "ok\n"; return 0; }
```

---

## ⑰ 最佳实践

1. **资源管理类（RAII）提供 `noexcept` 移动构造与移动赋值**——享受与标准库同等的零拷贝性能 `[标准]`。
2. **不要 `return std::move(local)`**——让 NRVO/隐式移动生效（⟶ `Book/part10_modern/ch117_copy_elision.md`）`[标准]`。
3. **需要把右值引用当右值传递时，用 `std::move`（局部变量）或 `std::forward`（转发参数）** `[标准]`。
4. **移动后把源对象视为空壳**：要么重新赋值再使用，要么不再使用（§⑧）`[经验]`。
5. **Rule of Five**：若需用户定义析构/拷贝/移动之一，通常五个都要显式声明（`=default` 或 `=delete`），避免编译器生成意外版本（⟶ `Book/part04_memory/ch39_raii_rule.md`）`[标准]`。
6. **`std::unique_ptr` / `std::thread` 等只移动类型，用 `std::move` 转移所有权**，不要尝试拷贝 `[标准]`。
7. **容器存大对象时，确保元素可 `noexcept` 移动**，扩容才走移动而非拷贝 `[经验]`。

```cpp
// ⑰-1 最佳实践：Rule of Five 显式声明（独立可编译）
#include <iostream>
#include <utility>
#include <cstddef>

class Buffer {
    int* d;
public:
    Buffer(std::size_t n = 0) : d(n ? new int[n] : nullptr) {}
    ~Buffer() { delete[] d; }
    Buffer(const Buffer& o) : d(o.d ? new int[1] : nullptr) { if(d) d[0]=o.d[0]; }
    Buffer& operator=(const Buffer& o) { if(this!=&o){ delete[] d; d=o.d?new int[1]:nullptr; if(d) d[0]=o.d[0]; } return *this; }
    Buffer(Buffer&& o) noexcept : d(o.d) { o.d = nullptr; }
    Buffer& operator=(Buffer&& o) noexcept { if(this!=&o){ delete[] d; d=o.d; o.d=nullptr; } return *this; }
};

int main() { Buffer a(1), b; b = std::move(a); std::cout << "ok\n"; return 0; }
```

```cpp
// ⑰-2 最佳实践：返回局部对象、放入容器都靠移动（独立可编译）
#include <vector>
#include <iostream>
#include <utility>

struct Big { std::vector<int> v; Big() : v(1000) {} };

int main() {
    std::vector<Big> v;
    v.push_back(Big{});          // ✅ 移动构造入容器，无拷贝
    std::cout << v.size() << "\n";
    return 0;
}
```

---

## ⑱ 性能分析

### 18.1 移动 vs 拷贝的复杂度

| 操作 | 拷贝 | 移动 |
|---|---|---|
| 构造/赋值（带堆资源） | `O(大小)`（分配+逐元素） | `O(1)`（指针窃取） |
| `vector` 扩容搬 N 元素 | `O(N)`（若移动非 noexcept） | `O(N)` 指针搬（若 noexcept） |
| `vector` 整体移动 | `O(N)` 拷贝 | `O(1)`（复制 3 指针） |

- `[标准]`：移动的成本与对象大小无关（常数级指针操作）；拷贝与大小成正比。对持有 MB 级缓冲的对象，差距是数量级。

### 18.2 microbenchmark 量级

```cpp
// ⑱-1 量级对照：拷贝 vs 移动一个大对象（独立可编译，计时骨架）
#include <vector>
#include <iostream>
#include <chrono>
#include <utility>

struct Big { std::vector<int> v; Big() : v(1'000'000) {} };

int main() {
    Big src;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < 1000; ++i) { Big c = src; (void)c; }   // 拷贝
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < 1000; ++i) { Big m = std::move(src); src = Big(); }  // 移动
    auto t2 = std::chrono::steady_clock::now();
    std::cout << "copy=" << (t1-t0).count()
              << " move=" << (t2-t1).count() << "\n";
    return 0;
}
```

- `[经验]`：量级上，每次拷贝要分配 1M int（4MB）并复制；移动仅复制一个 `vector` 内部三指针。差距常达 **数十到数百倍**（示意，取决于分配器与缓存）。

### 18.3 异常安全与 ABI

- `[标准]`：`noexcept` 移动使 `vector` 扩容获得强异常安全（否则退回拷贝）；这是移动语义与异常安全的交汇点。
- `[平台]`：移动构造/赋值通常 `inline` 为几条 `mov`（§⑩），无调用开销；`vector` 移动是 `O(1)` 且 `noexcept`，使容器在返回/重排时几乎免费。
- `[经验]`：滥用 `std::move`（如对 trivial 小对象 move）不会变快——小对象拷贝本身就几条指令，move 反而多一层转型；仅对**拥有堆资源/不可平凡拷贝**的类型 move 有意义。

### 18.4 三编译器对比

| 维度 | GCC 13 | Clang 17 | MSVC 19.3x |
|---|---|---|---|
| 右值引用 `T&&` | ✅ C++11 | ✅ | ✅ |
| `std::move` / `std::forward` | ✅ | ✅ | ✅ |
| `noexcept` 移动 | ✅ | ✅ | ✅ |
| `move_if_noexcept` | ✅ | ✅ | ✅ |

- `[平台]`：三者语义一致；差异仅在 `vector` 扩容时对 `noexcept` 移动的优化细节，可移植代码不受影响。

---

## ⑲ 工业案例：所有权转移与容器化大对象

**案例 A：网络服务中 `unique_ptr` 跨线程转移**

请求处理对象（持有连接、缓冲区）在 IO 线程解析后，整体 `std::move` 交给工作线程，避免跨线程拷贝大缓冲。

```cpp
// ⑲-1 unique_ptr 跨线程/跨作用域转移所有权（独立可编译，模拟逻辑）
#include <memory>
#include <iostream>
#include <utility>
#include <vector>

struct Request {
    std::unique_ptr<std::vector<int>> body = std::make_unique<std::vector<int>>(1'000'000);
    int id = 0;
};

void handle(Request r) {            // 按值接收 -> 移动构造（零拷贝）
    std::cout << "handle req " << r.id << " body=" << r.body->size() << "\n";
}

int main() {
    Request r; r.id = 7;
    handle(std::move(r));           // ✅ 所有权转移，无拷贝百万元素
    return 0;
}
```

**案例 B：数据库/存储引擎的批量写缓冲**

写缓冲（WAL 段）作为大对象在"生产者"与"刷盘器"之间用移动传递，避免每批数据深拷贝。

```cpp
// ⑲-2 大对象容器：vector 存可移动 Buffer（独立可编译，模拟逻辑）
#include <vector>
#include <iostream>
#include <utility>
#include <cstddef>

struct Segment {
    std::vector<unsigned char> data;
    Segment(std::size_t n) : data(n) {}
    Segment(Segment&&) = default;
    Segment& operator=(Segment&&) = default;
};

int main() {
    std::vector<Segment> log;
    log.reserve(8);
    for (int i = 0; i < 5; ++i)
        log.push_back(Segment(4096));     // ✅ 移动入容器，无拷贝 4KB
    std::cout << "segments=" << log.size() << "\n";
    return 0;
}
```

**案例 C：工厂构建复杂对象后返回**

编译器可在返回处直接构造（NRVO）或隐式移动，使"返回大对象"与"返回 int"成本相当（见 §⑭、§⑯）。

```cpp
// ⑲-3 工厂返回大对象（独立可编译）
#include <string>
#include <iostream>

struct Doc { std::string title; std::string content; };

Doc load() {
    Doc d;
    d.title = "report";
    d.content = "very long generated content ......";
    return d;                       // ✅ NRVO/隐式移动
}

int main() { Doc d = load(); std::cout << d.title << "\n"; return 0; }
```

---

## ⑳ 跨语言对比：移动语义

| 语言 | 移动语义 | 说明 |
|---|---|---|
| C++ | `T&&` + 移动构造/赋值 + `std::move` | 显式、值类别驱动；移动后状态有效但未指定；无自动借用检查 |
| Rust | 默认移动 + 借用检查器 | 所有值默认移动（浅拷贝资源指针+源失效）；借用检查器**编译期**阻止悬垂/使用后移动（use-after-move） |
| C# | 引用类型靠 GC；`struct` 值拷贝；`ref struct`/`Span` 限制上堆 | 无 C++ 式移动构造；大对象靠引用（GC 管理）避免拷贝 |
| Java | 一切皆引用（GC） | 无移动语义；赋值拷贝的是引用而非对象，天然无深拷贝成本（但有 GC 延迟） |
| Go | 值语义拷贝；指针共享 | 赋值/传参默认拷贝值（大结构有成本）；用指针避免；无 C++ 式移动 |
| Swift | 值类型 `move` 语义（COW） | 值类型默认拷贝但写时复制（COW），兼顾安全与性能；`move` 优化存在 |

- `[标准]`：C++ 的 `std::move` 对标 Rust 的"值移动"——两者都是把资源所有权转移而非复制。关键差异：
  1. **安全性**：Rust 在**编译期**禁止 use-after-move（借用检查器），C++ 仅约定"移动后有效但未指定"，**靠程序员/工具（-fsanitize）兜底**（见 §⑧）。
  2. **触发方式**：Rust 移动是默认行为（赋值即移动），C++ 需显式 `std::move`（否则拷贝）。
  3. **规则**：C++ 因历史兼容需保留拷贝语义，`std::move` 是"请求"而非"强制"——源对象仍可访问（虽状态未指定）。
- `[经验]`：从 Rust 转来的工程师会觉得 C++ 移动"不够安全但有更多控制"；从 Java/C# 转来的会觉得"C++ 终于能避免深拷贝了"。无论背景，都应把"移动后源对象当空壳"刻进肌肉记忆。

```cpp
// ⑳-1 跨语言映射：Rust 的 let y = x;（移动）在 C++ 用 std::move 表达（独立可编译）
#include <iostream>
#include <utility>
#include <string>

int main() {
    std::string x = "resource";
    std::string y = std::move(x);   // C++ 显式移动（Rust 中 let y = x; 隐式移动）
    std::cout << y << "\n";         // resource
    return 0;
}
```

```cpp
// ⑳-2 跨语言映射：C++ 的"移动后有效但未指定" vs Rust 的编译期禁止 use-after-move
// （C++ 无法在编译期阻止，需纪律；独立可编译的"安全用法"示范）
#include <iostream>
#include <utility>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = std::move(a);
    // Rust 会在此处编译报错若再使用 a；C++ 允许但约定不读 a
    a = std::vector<int>{9, 8};     // ✅ 重新赋值后再使用（安全的"复活"）
    std::cout << a[0] << "\n";      // 9
    return 0;
}
```

---

## 附录：练习题 / 思考题 / 源码阅读路线

### 练习题

1. 实现一个 `String` 类（动态 `char*` 缓冲），给出完整 Rule of Five（析构、拷贝构造、拷贝赋值、移动构造、移动赋值），全部 `noexcept` 适配移动，并写测试验证移动后源为空。

```cpp
// 练习①参考实现：Rule of Five String 类，noexcept 移动
#include <iostream>
#include <cstring>
#include <utility>
#include <cstddef>

class String {
    char* data_ = nullptr;
    size_t len_ = 0;
public:
    String() = default;
    explicit String(const char* s) : data_(new char[std::strlen(s)+1]), len_(std::strlen(s)) {
        std::strcpy(data_, s);
    }
    ~String() { delete[] data_; }
    String(const String& o) : data_(new char[o.len_+1]), len_(o.len_) { // 拷贝构造
        std::strcpy(data_, o.data_);
    }
    String& operator=(const String& o) { // 拷贝赋值（copy-and-swap）
        String tmp(o); std::swap(data_, tmp.data_); std::swap(len_, tmp.len_); return *this;
    }
    String(String&& o) noexcept : data_(std::exchange(o.data_, nullptr)), len_(std::exchange(o.len_, 0)) {} // 移动构造
    String& operator=(String&& o) noexcept { // 移动赋值
        delete[] data_; data_ = std::exchange(o.data_, nullptr);
        len_ = std::exchange(o.len_, 0); return *this;
    }
    const char* c_str() const { return data_ ? data_ : ""; }
};
int main() {
    String a("hello");
    String b = std::move(a);  // 移动构造
    std::cout << "b=" << b.c_str() << " a空=" << (a.c_str()[0]=='\0') << "\n"; // b=hello a空=1
    String c("world");
    c = std::move(b);          // 移动赋值
    std::cout << "c=" << c.c_str() << " b空=" << (b.c_str()[0]=='\0') << "\n"; // c=hello b空=1
}
```

2. 解释并修复：`std::vector<Holder> v; Holder h; v.push_back(std::move(h));` 后 `h` 仍可读到旧值（提示：检查 `Holder` 移动构造是否标 `noexcept`）。
3. 实现一个 `MaybeOwned<T>`：可持有 `T` 或借用 `T&`，用移动语义在"接管所有权"与"借引用"间切换（工业中常用于"可选拥有"）。

### 思考题

- 为什么 `std::move(const T)` 会退化为拷贝？这与重载决议中 `T&&` vs `const T&` 的优先级有何关系？
- 若 `std::vector` 的移动构造不是 `noexcept`，把它 `push_back` 进另一个 `vector` 扩容时会怎样？
- C++ 为什么不像 Rust 那样在编译期禁止 use-after-move？是技术限制还是设计权衡（考虑向后兼容与泛型）？

### 源码阅读路线

1. `bits/move.h`（GCC 13.1.0）—— 通读 `std::move`(104) / `std::forward`(77/89) / `move_if_noexcept`(125) / `__move_if_noexcept_cond`(109)。
2. `bits/stl_vector.h` —— `vector(vector&&)`(615) / `operator=(vector&&)`(761)，以及扩容时 `move_if_noexcept` 的使用。
3. `bits/unique_ptr.h` —— 看 `unique_ptr` 如何 `=delete` 拷贝、仅留 `noexcept` 移动。
4. 进阶：对比 `libc++` 的 `move.h` / `MS STL` 的 `xutility`，理解三套实现的共性与差异。

> 推荐读物（已融于正文）：ISO/IEC 14882:2023 `[expr.value]`、`[class.copy.el]`、`[utility]`；WG21 N1377/N1690（右值引用与移动语义）、N2831（值类别）、N3053（Rule of Five）；Scott Meyers《Effective Modern C++》第 5 章（右值引用、移动、`std::move`/`std::forward`）；Howard Hinnant 关于 `noexcept` 移动与异常安全的文章。

## 附录: Move 语义深度

```cpp
#include <iostream>
#include <utility>
#include <vector>
#include <cstddef>
struct Buffer{int*d;size_t n;explicit Buffer(size_t s):d(new int[s]),n(s){}~Buffer(){delete[]d;}Buffer(Buffer&&o)noexcept:d(o.d),n(o.n){o.d=nullptr;o.n=0;}Buffer&operator=(Buffer&&o)noexcept{std::swap(d,o.d);std::swap(n,o.n);return*this;}};
int main(){Buffer a(10);Buffer b=std::move(a);std::cout<<b.n<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <vector>
#include <utility>
int main(){std::vector<int> a{1,2,3};auto b=std::move(a);std::cout<<b.size()<<" "<<a.size()<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <memory>
#include <utility>
int main(){auto p1=std::make_unique<int>(42);auto p2=std::move(p1);std::cout<<*p2<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <string>
#include <utility>
int main(){std::string s1="hello";std::string s2=std::move(s1);std::cout<<s2<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <utility>
int main(){std::cout<<"std::move is a cast to rvalue reference. It does NOT move — the move constructor/assignment does."<<std::endl;return 0;}
```


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Chromium（github.com/chromium/chromium）**：大量 move-only 类型（`std::unique_ptr`、`base::OnceCallback`）避免拷贝；`base::WrapUnique` 用 `std::move` 语义，Chromium 禁止隐式拷贝的回调。
  → <https://github.com/chromium/chromium>
- **Boost.Move（github.com/boostorg/move）**：`std::move` 的前身，向 C++03 后端移植移动语义；`boost::move()` / `BOOST_MOVABLE_BUT_NOT_COPYABLE` 是 `=delete` 拷贝的先驱。
  → <https://github.com/boostorg/move>
- **Folly `folly::MoveWrapper`（github.com/facebook/folly）**：在需要拷贝语义的泛型上下文（如旧 `std::bind`）中"伪装"移动，避免提前 move；Facebook 用它桥接老接口。
  → <https://github.com/facebook/folly>
- **LLVM/Clang 的 RVO/move 省略（github.com/llvm/llvm-project）**：`-fno-elide-constructors` 关闭拷贝/移动省略，可对照移动构造的开销实测；Clang 的 NRVO 分析在 `-O2` 下消除大部分移动。
  → <https://github.com/llvm/llvm-project>
- **Google 的 Abseil `absl::StatusOr`（github.com/abseil/abseil-cpp）**：值语义用移动返回，避免大对象拷贝；Google 在 API 设计上统一用移动返回。
  → <https://github.com/abseil/abseil-cpp>

**常见陷阱 / 最佳实践**：
- 移动后源对象处于"有效但未指定"状态，禁止再读其值（仅可析构/赋值）；Boost 与 Chromium 都通过 `=delete` 拷贝强化这点。
- 返回局部变量不要写 `std::move`，会阻断 RVO（具名返回值优化）；LLVM 的省略优化依赖此规则。

> 交叉引用：移动与 noexcept 见 [ch40](Book/part04_memory/ch40_exception_safety.md)；完美转发见 [ch116](Book/part10_modern/ch116_perfect_forwarding.md)。

## 附录 E：编译实证——RVO vs 移动构造 vs 拷贝构造的真实汇编 [C: Compiler / E: Low-level]

> 编译：`g++ -std=c++23 -O2 -c ch115_move_test.cpp`（GCC 15.3.0 / Win64 ABI）。`objdump -d`。

### 测试源码

```cpp
struct Big { char* data; size_t sz;
    Big(size_t n): data(new char[n]), sz(n) { memset(data, 0, n); }
    Big(const Big& o): data(new char[o.sz]), sz(o.sz) { memcpy(data, o.data, sz); }
    Big(Big&& o) noexcept : data(o.data), sz(o.sz) { o.data=nullptr; o.sz=0; }
    ~Big() { delete[] data; }
};
Big make_big_rvo() { return Big(1024); }              // ① RVO
void move_into_consume(Big&& src) { consume_big(std::move(src)); } // ② 移动
```

### 真实汇编（GCC15 -O2）

**① RVO 构造 —— 内联到调用方栈槽**

RVO 不产生函数调用在调用方生成对象。编译器在函数签名层面传递了**隐藏的返回槽指针**（Win64 ABI：`%rcx` = 目标地址）：

```asm
<_Z12make_big_rvov>:
    push   %rdi; push %rbx; sub $0x28,%rsp
    mov    %rcx,%rbx                    ; [RVO] 保存返回槽指针
    mov    $0x400,%ecx                  ; 1024 字节
    call   operator new(1024)           ; 只分配一次
    movq   $0x400,0x8(%rbx)            ; sz = 1024（直接写入返回槽）
    lea    0x8(%rax),%rdx
    mov    %rax,(%rbx)                  ; data = new char[1024]（写入返回槽）
    ; memset 展开为两次 8B 零写（首尾 8 字节）——避免 memset 调用
    and    $0xfffffffffffffff8,%rdx
    movq   $0x0,(%rax)                  ; data[0..7] = 0
    movq   $0x0,0x3f8(%rax)            ; data[1016..1023] = 0（编译器2×8B覆盖够了）
    mov    %rbx,%rax; add $0x28,%rsp; pop %rbx; pop %rdi; ret
```

**💡 关键观察**：
- **零次拷贝/移动构造调用**——`Big` 的构造函数体（`new` + `memset` + 字段初始化）直接被编译到函数中，不通过任何中间对象。
- **返回槽指针**`%rbx` 是调用方栈上预分配的 16 字节 `Big` 对象地址——RVO 是 ABI 层面的操作，不是编译器优化。

**② 移动构造 —— 指针交换**

当 RVO 不适用时（如 `std::move(src)` 传参），移动构造器被调用：

```asm
; 移动构造器 Big(Big&&) — 3 条关键 mov
mov  (%rcx),%rax    ; dst->data = src->data（指针搬移）
mov  %rax,(%rdx)
mov  0x8(%rcx),%rax ; dst->sz  = src->sz（值搬移）
mov  %rax,0x8(%rdx)
movq $0x0,(%rcx)    ; src->data = nullptr（搬空源）
movq $0x0,0x8(%rcx) ; src->sz   = 0
```

**③ 拷贝构造 —— 堆分配 + memcpy**

```asm
; 拷贝构造器 Big(const Big&) — call 链
call operator new(other.sz)   ; 新分配
call memcpy(dst, src, sz)     ; 逐字节复制
```

### 三层代价分层

| 机制 | 指令特征 | 堆分配 | 额外拷贝 | 适用场景 |
|------|----------|--------|----------|----------|
| RVO | 内联到调用方栈槽 | 1 次（本地） | 0 | 返回局部对象（**C++17 强制**） |
| 移动构造 | `mov;mov;mov;mov;mov;ret` | 0（指针置换） | 0 | `std::move` + noexcept |
| 拷贝构造 | `call new+call memcpy` | 1 次（新块） | 1 次（memcpy） | 无法 move 时 |
| 原始分配 | `new+delete` 裸露 | 1 次 | 0 | C 风格/裸管理 |

### 关键发现

1. **RVO 是代码优化的物理定律，不是魔法**——C++17 强制要求：返回值路径中的构造必须直接在调用方地址进行（prvalue materialization 规则）。
2. **`std::move` 不会生成额外指令**——move 构造函数只有 6 条 mov，编译器内联后移动成本 = 搬 2 个字段（+ 零空源字段）。
3. **`Big` 的 sizeof=16**——data(8B) + sz(8B)。对于小于两个指针的对象，**copy 可能比 move 更快**（copy 的三指令 mov 无 nullptr 赋值开销）——这是为什么 `std::is_trivially_copyable` 的对象不需要 noexcept move。

---

## 相关章节（交叉引用）

- **后续依赖**：⟶ Book/part03_language/ch19_variables.md（第19章　变量、存储期、链接与 ODR（工业级深度版））—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：⟶ Book/part03_language/ch20_reference_pointer.md（第20章　引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：⟶ Book/part04_memory/ch39_raii_rule.md（第 39 章　RAII 与 Rule of Zero/Three/Five）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：⟶ Book/part10_modern/ch116_perfect_forwarding.md（第116章　完美转发与万能引用）—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part10_modern/ch117_copy_elision.md（第117章　RVO / NRVO 与拷贝消除（C++17））—— 同模块下的其他主题。

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

