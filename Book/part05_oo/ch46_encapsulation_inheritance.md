# 第 46 章　封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI

⟶ Book/part03_language/ch29_friend.md
⟶ Book/part05_oo/ch45_oop_object_model.md

> 老兵标准：**继承是最被滥用的 C++ 特性，没有之一。** 真正的封装不是把成员写进 `private` 就万事大吉——它是一道**编译期契约**；真正的继承不只是「冒号加个 public」——它关乎 LSP、切片、构造顺序与名字隐藏。本章把这些都钉死。
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **[标准]**　语言/库标准规定（ISO C++、CWG/LWG 决议）。
- **[实现]**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **[平台]**　MinGW GCC 13.1.0、Windows、x86-64 ABI（System V / MS）相关事实。
- **[经验]**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；本章所有 `[实现]` 级源码均来自该目录的真实文件，逐行标注路径与行号。libc++、MS STL 不在本机，相关对比以 `[实现-推断]` / `[平台-推断]` 标注。

---

## ① 概述：封装与继承在 C++ 中的真实地位

⟶ Book/part05_oo/ch45_oop_object_model.md
⟶ Book/part05_oo/ch47_virtual_functions.md


**[标准]**　`[class]` / `[class.access]` / `[class.derived]` 把封装与继承定义为「在编译期对名字访问与子类型关系施加约束」的机制。注意关键词是**编译期**——它们不产生任何运行期数据结构（不像虚函数会生成 vtable）。

**[经验]**　本章主线与三大铁律：

1. **封装 = 编译期契约，不是运行期保险箱**。写进 `private` 只是让编译器拒绝越权访问；运行期对象就是一块裸内存，`memcpy` / `offsetof` 照样能碰（`ch45` 第 11 节已铺垫）。
2. **继承不是复用手段，而是「子类型/is-a」声明**。绝大多数「为了复用而继承」的代码，都应该改成组合（composition）。
3. **public 继承必须满足 Liskov 替换原则（LSP）**；一旦你写的派生类不能在基类出现的地方替换基类，你就用错了继承。

本章主线 22 节：

- 封装本质（第 2 节）。
- 封装边界真相：private 仅编译期（`memcpy`/`offsetof`）（第 3 节）。
- 友元：受控破封装、最小化（第 4 节）。
- public/private/protected 真实语义（第 5 节）。
- class vs struct 唯一区别（第 6 节）。
- 三种继承语义总览（第 7 节）。
- public 继承与 LSP（第 8 节）。
- Square/Rectangle LSP 反例与正确做法（第 9 节）。
- 切片（slicing）完整机制（第 10 节）。
- 切片修复：引用/指针/`unique_ptr<Base>`（第 11 节）。
- 构造/析构顺序实证（第 12 节）。
- 多继承与虚基类构造顺序（第 13 节）。
- 名字隐藏（name hiding）与 `using` 恢复重载（第 14 节）。
- override/final（C++11）（第 15 节）。
- NVI 惯用法（第 16 节）。
- 组合优于继承：protected 继承的替代（第 17 节）。
- 真实 libstdc++ 源码逐行：`is_base_of`/`is_convertible`/`uses_allocator`/`stl_construct`（第 18 节）。
- 三编译器对比：GCC/LLVM/MSVC（第 19 节）。
- microbenchmark（第 20 节）。
- 跨语言对比（第 21 节）。
- 源码阅读路线与小结（第 22 节）。

交叉引用：`ch19`（存储期）、`ch35`（内存布局总览）、`ch39`（RAII/析构 `noexcept`）、`ch40`（异常安全）、`ch41`（智能指针避免切片）、`ch45`（对象模型）、`ch47`（虚函数与虚表）、`ch49`（虚继承）。

**核心知识点 #1**：封装与继承都是**编译期**机制（访问控制、子类型关系），本身不生成运行期数据结构；只有虚函数（第 47 章）才引入 vtable。

---

## ② 封装本质：接口与实现分离、不变量责任、编译期契约

**[标准]**　`[class]` 把 `class` 定义为「带有访问控制的数据与函数的集合」，其设计意图是**把「对用户稳定的接口」与「可以随意改动的实现」分开**。标准术语中，类的**不变量（invariant）** 指「任何 public 成员函数返回后都必须为真的条件」。

**[标准]**　关键契约：**不变量只能由类的成员函数（及其友元）维护**。类的责任是：对外暴露的每一个 public 接口，调用前/返回后都不变量必须成立；private 成员是实现细节，可自由重构。

```cpp
// [示例 1] 不变量：balance_ 永不为负，由成员函数维护
#include <cstdio>
#include <stdexcept>

class Account {
    long balance_ = 0;                 // 实现细节（private）
public:
    void deposit(long n) {             // 维持不变量
        if (n < 0) throw std::invalid_argument("negative deposit");
        balance_ += n;
    }
    void withdraw(long n) {           // 维持不变量
        if (n > balance_) throw std::runtime_error("insufficient");
        balance_ -= n;
    }
    long balance() const { return balance_; }  // 只读接口
};

int main() {
    Account a;
    a.deposit(100);
    a.withdraw(30);
    printf("%ld\n", a.balance());      // 70
    // 不变量由类自身捍卫，调用方无法让 balance_ 变负
}
```

**[经验]**　封装的三层收益：

1. **可改动性**：改 `balance_` 为 `std::atomic<long>` 或分散到两个字段，调用方代码一行都不用动。
2. **可验证性**：不变量只在 `private`/成员函数边界被破坏点集中，调试时只需审计少数函数。
3. **编译期强制**：访问控制把「谁能用什么」交给编译器把关，而非靠 code review。

**核心知识点 #2**：封装 = 接口（public）与实现（private）分离；**不变量（invariant）的责任落在类的成员函数/友元身上**，而不是调用方。

---

## ③ 封装边界真相：private 仅是编译期拒绝越权

**[标准]**　`[class.access]` 明确：访问检查发生在**名字查找与可达性分析**阶段。一旦编译通过，对象就是一块内存。标准**不保证**运行期有任何机制阻止你越过 `private` 读写那块内存——事实上做不到，因为 C++ 必须允许 `memcpy` 这类底层操作。

**[经验]**　「封装是编译期契约而非运行时保险箱」。下面三个例子证明 `private` 在运行期形同虚设。

```cpp
// [示例 2] 封装边界真相 ①：offsetof + 指针算术可越过 private
#include <cstdio>
#include <cstddef>

class Secret {
    int hidden_ = 0xDEADBEEF;          // private，但仍在对象内存里
public:
    int  get() const { return hidden_; }
    // offsetof 需在成员可访问的上下文求值；这里由类主动暴露自身布局
    static std::size_t offset() { return offsetof(Secret, hidden_); }
};

int main() {
    Secret s;
    // 类暴露了偏移，外部用原始指针直接写入——访问控制是编译期约束，不保护内存
    int* p = reinterpret_cast<int*>(
                 reinterpret_cast<char*>(&s) + Secret::offset());
    *p = 0x12345678;                   // 绕过了 private 访问控制！
    printf("%08X\n", s.get());         // 12345678 —— private 已被运行期改写
}
```

```cpp
// [示例 3] 封装边界真相 ②：memcpy 整块对象内存
#include <cstdio>
#include <cstring>

class Widget {
    int x_ = 1, y_ = 2;
public:
    int x() const { return x_; }
    int y() const { return y_; }
};

int main() {
    Widget w;
    int raw[2] = { 9, 8 };
    std::memcpy(&w, raw, sizeof(raw)); // 直接覆写对象内存
    printf("%d %d\n", w.x(), w.y());   // 9 8 —— 私有成员被覆写
}
```

```cpp
// [示例 4] 封装边界真相 ③：同布局 struct 强行 reinterpret 读写
#include <cstdio>

struct Raw { int a, b; };
class Pair {
    int a_ = 10, b_ = 20;             // private
public:
    int a() const { return a_; }
    int b() const { return b_; }
};

int main() {
    Pair p;
    auto* r = reinterpret_cast<Raw*>(&p);  // 未定义行为风险，但多数实现会"成功"
    r->a = 100; r->b = 200;
    printf("%d %d\n", p.a(), p.b());       // 100 200
}
```

**[经验]**　示例 4 触及**严格别名规则（strict aliasing，见 `ch42`）的边缘**——`reinterpret_cast` 把 `Pair*` 当 `Raw*` 用是 UB。但示例 2、3 用的 `char*`/`memcpy` 路径是标准明确允许的（对象表示可按 `unsigned char`/`char` 拷）。要点不变：**运行期没有任何「访问锁」**。因此「敏感数据放进 `private` 就安全」是幻觉——真正的安全靠加密、权限、进程隔离，不靠语言访问控制。

**核心知识点 #3**：private 只是**编译期**拒绝越权访问；运行期对象内存可读写（`memcpy`/`offsetof` 仍可触及）——封装是编译期契约而非运行时保险箱。

---

## ④ 友元：受控破封装，最小化

**[标准]**　`[class.friend]`：`friend` 声明授予特定函数/类/类模板访问本类所有成员（含 private/protected）的特权。**关键限制**：

- `friend` **不是成员**，没有 `this`，不参与重载解析的名字查找起点（除非显式限定）。
- `friend` 关系**不可继承**（派生类不自动获得基类的友元权）。
- `friend` 关系**不可传递**（A 是 B 友、B 是 C 友，不意味着 A 是 C 友）。
- `friend` 声明可出现在类任意访问区（public/private 不影响其语义）。

```cpp
// [示例 5] 友元函数：受控破封装（不是成员，但能碰 private）
#include <cstdio>

class Box {
    int w_ = 3, h_ = 4;
    friend int area(const Box&);       // 仅此函数被授权
public:
    int  w() const { return w_; }
};

int area(const Box& b) {              // 非成员函数，却能访问 private
    return b.w_ * b.h_;
}

int main() { printf("%d\n", area(Box{})); }   // 12
```

```cpp
// [示例 6] 友元关系不可继承、不可传递
#include <cstdio>

class Base {
    int secret_ = 42;
    friend class FriendOfBase;
};

class FriendOfBase {
public:
    static int peek(const Base& b) { return b.secret_; }   // OK
};

class Derived : public Base {};        // 不继承友元权

class NotFriend {
public:
    // static int peek(const Base& b) { return b.secret_; } // 编译错误：secret_ 是 private
};

int main() {
    Base b;
    printf("%d\n", FriendOfBase::peek(b));   // 42
    // Derived 没有友元权；NotFriend 也没有
}
```

```cpp
// [示例 7] 友元最小化：用“具名访问函数”替代盲目 friend class
#include <cstdio>

class Engine {
    int rpm_ = 0;
public:
    int rpm() const { return rpm_; }          // 首选：公开只读接口
    void set_rpm(int r) { rpm_ = r; }
};

class Car {                            // Car 不需要是 Engine 的友元
    Engine engine_;
public:
    void rev() { engine_.set_rpm(8000); }
    int  rpm() const { return engine_.rpm(); }
};

int main() { Car c; c.rev(); printf("%d\n", c.rpm()); }
```

**[经验]**　友元的黄金法则：**能不开友元就不开**。先问三件事——是否可用 public 接口替代？是否可用 `protected` 让派生类访问？是否该把共享逻辑抽成独立函数/类？只有「两个类必须共享彼此私有状态且无法用接口表达」时才用友元，且尽量 `friend` 到**具体函数**而非整个类，缩小破封装面。

**核心知识点 #4**：友元是**受控破封装**：`friend` 函数/类不是成员、不能继承、不能传递，应当最小化授予。

---

## ⑤ public/private/protected 真实语义

**[标准]**　`[class.access]` 三种访问标号定义「谁能通过成员名访问该成员」：

| 标号 | 类内 | 派生类成员/友元 | 类外 |
|------|------|----------------|------|
| `public` | ✓ | ✓ | ✓ |
| `protected` | ✓ | ✓（仅通过 `this`/派生类对象） | ✗ |
| `private` | ✓ | ✗ | ✗ |

**[标准]**　所有访问检查都是**编译期**进行的（`[class.access]` 明确「accessibility is checked at compile time」）。它不是运行期能力，不生成任何代码。

**[标准]**　`protected` 的**脆弱基类问题（fragile base class）**：派生类依赖基类的 `protected` 名字与布局。一旦基类作者修改 `protected` 成员（改名、改类型、改访问），**所有派生类静默编译失败或行为改变**——因为派生类代码直接吃进了基类的私有实现细节。这与「封装应隐藏实现」自相矛盾，是 `protected` 最大的隐患。

```cpp
// [示例 8] public/private/protected 编译期语义
#include <cstdio>

class Base {
public:    int pub = 1;
protected: int pro = 2;
private:   int pri = 3;
};

class Derived : public Base {
public:
    void f() {
        printf("%d %d\n", pub, pro);  // OK：public/protected 派生类可见
        // printf("%d\n", pri);       // 编译错误：'pri' is private
    }
};

int main() {
    Base b;
    printf("%d\n", b.pub);            // OK
    // printf("%d\n", b.pro);         // 编译错误：'pro' is protected
    // printf("%d\n", b.pri);         // 编译错误：'pri' is private
    Derived d; d.f();
}
```

```cpp
// [示例 9] 脆弱基类：基类改 protected 布局，派生类静默崩
#include <cstdio>

#if 1
struct Widget {            // 版本 1：protected 名为 'id_'
protected: long id_ = 0;
public:    long id() const { return id_; }
};
#else
struct Widget {            // 版本 2：基类作者把 id_ 重构成两个字段
protected: int id_hi_ = 0, id_lo_ = 0;
public:    long id() const { return (long(id_hi_)<<32)|id_lo_; }
};
#endif

struct Panel : Widget {
    void dump() {
        // 版本 2 下这行直接编译失败：id_ 已不存在
        printf("%ld\n", /* id_ */ id());
    }
};

int main() { Panel p; p.dump(); }
```

**[经验]**　尽量让基类只暴露 `public` 接口与 `protected` **虚函数**（让派生类定制行为），而非 `protected` **数据成员**。数据成员放 `private`；需要派生类访问的「钩子」才放 `protected`，且优先做成函数/虚函数而非裸字段。

**核心知识点 #5**：public/private/protected 都是**编译期**访问控制。
**核心知识点 #6**：`protected` 有**脆弱基类问题**——基类改动 `protected` 会破坏所有派生类。
**核心知识点 #7**：访问控制的检查时机是编译期，不生成运行期代码。

---

## ⑥ class vs struct 的唯一区别

**[标准]**　`[class.name]` / `[class.access.spec]`：在 C++ 中，`class` 与 `struct` 除**默认访问控制**与**默认继承方式**外**完全等价**（模板参数里写 `class` 与 `typename` 也是等价的，无关本节）。

| | class | struct |
|---|---|---|
| 默认成员访问 | `private` | `public` |
| 默认继承方式 | `private` | `public` |

```cpp
// [示例 10] 默认成员访问区别
struct S { int x; };       // x 默认 public
class  C { int x; };       // x 默认 private

int main() {
    S s; s.x = 1;          // OK
    // C c; c.x = 1;       // 编译错误：'x' is private
}
```

```cpp
// [示例 11] 默认继承方式区别
struct B { int x; };
struct D1 : B {};          // struct 默认 public 继承 → D1 是 B 的子类
class  D2 : B {};          // class  默认 private 继承 → D2 不是 B 的子类（外部）

void f(B*) {}
int main() {
    D1 d1; f(&d1);         // OK：public 继承，D1* → B* 隐式转换存在
    // D2 d2; f(&d2);      // 编译错误：private 继承，无 D2* → B* 转换
}
```

**[经验]**　工程惯例：`struct` 表示「 plain old data / 聚合 / 纯数据载体」（成员默认 public 很自然）；`class` 表示「有不变量的抽象类型」。这只是**约定**，语言层面二者可互换。§示例 11 提醒：用 `class` 做继承时**务必显式写 `: public Base`**，否则默认 private 继承会让子类型关系消失（见第 7 节）。

**核心知识点 #8**：class 与 struct 的**唯一区别**是默认成员访问（`private` vs `public`）和默认继承方式（`private` vs `public`）。
**核心知识点 #9**：`class` 默认继承为 `private`，故做基类时务必显式写 `: public`。

---

## ⑦ 三种继承语义总览

**[标准]**　`[class.derived]`：`class D : <access> B` 的 `<access>` 决定「基类的 public/protected 成员在派生类中**提升/降到**什么访问级别」，以及「`D` 是否构成 `B` 的子类型（是否可做 `B* ← D*` 转换）」。

| 继承方式 | 基类 public 成员在 D 中 | 基类 protected 成员在 D 中 | D 是 B 的子类型？ | 典型用途 |
|---------|------------------------|---------------------------|------------------|---------|
| `public` | public | protected | **是**（is-a） | 接口/子类型多态 |
| `protected` | protected | protected | 否（仅派生可见） | 实现继承，对外部隐藏 |
| `private` | private | private | 否（外部不可见） | 实现继承，外部完全看不到 |

**[标准]**　要点：**继承方式只影响「基类成员在派生类里的可见性」与「子类型关系是否成立」，不复制任何代码，也不改变基类自身。** 注意 `private` 继承下，连 `D*` 到 `B*` 的隐式转换都消失（除非用显式 `static_cast`）。

```cpp
// [示例 12] public 继承：is-a，子类型关系成立
#include <cstdio>

struct Animal { void breath() const { printf("breath\n"); } };
struct Dog : public Animal {};        // Dog 是 Animal

int main() {
    Dog d;
    Animal* a = &d;                   // OK：public 继承 → 子类型
    a->breath();
}
```

```cpp
// [示例 13] protected 继承：仅派生链可见，外部看不到 is-a
#include <cstdio>

struct Base { void f() const { printf("f\n"); } };
struct Mid : protected Base {};       // 外部看不到 Mid 是 Base
struct Leaf : public Mid {
    void g() const { f(); }           // OK：Mid 内部可见 Base::f（protected）
};

int main() {
    // Base* b = (Mid*)nullptr;       // 编译错误：protected 继承无子类型
    Leaf l; l.g();
}
```

```cpp
// [示例 14] private 继承：外部完全不可见，少用
#include <cstdio>

struct Engine { void run() const { printf("vroom\n"); } };

// Car “has-a” Engine 的实现细节，但用 private 继承表达
struct Car : private Engine {
public:
    void drive() const { run(); }     // 复用 run()，但对外隐藏 Engine 身份
};

int main() {
    Car c; c.drive();
    // Engine* e = &c;                // 编译错误：private 继承无子类型
}
```

**[经验]**　`protected`/`private` 继承都表达「实现复用」而非「is-a」。**经验法则**：需要「is-a / 多态」→ `public` 继承；只需要「复用基类代码但对外不想暴露」→ **优先用组合（见第 17 节）**，其次 `private` 继承；`protected` 继承极少用，且几乎总能被组合或 `private` 继承替代。

**核心知识点 #10**：public 继承 = is-a、满足 LSP；protected 继承 = 实现继承、仅派生可见；private 继承 = 实现继承、外部不可见，少用。

---

## ⑧ public 继承与 Liskov 替换原则（LSP）

**[标准]**　`[class.derived]` 中 `public` 继承建立子类型关系（subtype），即在需要 `Base&`/`Base*` 的语境可用 `Derived&`/`Derived*`。但**语言只保证语法可转换**，不保证语义合理——这正是 LSP 的用武之地。

**[标准-经验]**　**Liskov 替换原则（LSP）**：若 `D` 是 `B` 的（public）派生类，则任何用到 `B` 的程序，在把 `B` 替换为 `D` 后，其行为契约（前置条件不强化、后置条件不弱化、不变量保持）必须依然成立。违反 LSP 的 `public` 继承是「语法合法、语义毒药」。

```cpp
// [示例 15] 满足 LSP 的 public 继承：栈是一种列表（仅收窄，不破坏契约）
#include <cstdio>
#include <vector>

struct List { std::vector<int> v; void add(int x){ v.push_back(x); } int size() const { return (int)v.size(); } };
struct Stack : public List {
    int pop() { int x = v.back(); v.pop_back(); return x; }  // 额外能力，不破坏 List 契约
};

int main() {
    Stack s; s.add(1); s.add(2);
    printf("%d\n", s.size());   // 2：作为 List 使用完全正常
}
```

**核心知识点 #11**：public 继承意味着 is-a 与子类型关系，且**必须满足 LSP**（派生可替换基类而不违反契约）。

---

## ⑨ Square/Rectangle：经典 LSP 反例与正确做法

**[标准-经验]**　经典反例：把 `Square` 声明为 `Rectangle` 的 `public` 派生类，看似「正方形是矩形」，实则违反 LSP。`Rectangle` 的契约允许「独立设置宽和高」；`Square` 若遵守该契约就必须允许宽高不等，但正方形不变量要求宽高相等——两者冲突。

```cpp
// [示例 16] 违反 LSP：Square : Rectangle（错误示范）
#include <cstdio>
#include <cassert>

struct Rectangle {
    virtual void width(int w)  { w_ = w; }
    virtual void height(int h) { h_ = h; }
    int w_ = 0, h_ = 0;
    int area() const { return w_ * h_; }
};

struct Square : public Rectangle {    // 表面 is-a，实际破坏契约
    void width(int w)  override { w_ = h_ = w; }   // 副作用：同时改高
    void height(int h) override { w_ = h_ = h; }   // 副作用：同时改宽
};

// 一个“相信” Rectangle 契约的函数
void enlarge(Rectangle& r) {
    int old = r.area();
    r.width(r.w_ + 1);                // 契约：仅宽度+1，高度不变
    assert(r.area() == old + r.h_);   // 对真 Rectangle 成立
}

int main() {
    Square s; s.width(2); s.height(2);
    enlarge(s);                        // 断言失败！Square 破坏了 Rectangle 契约
}
```

**[经验]**　`enlarge` 在签名上接受 `Rectangle&`，逻辑上依赖「只改宽不影响高」这一 `Rectangle` 不变量；`Square` 的覆盖破坏了它。这是**误用 public 继承**：`Square` 不能在 `Rectangle` 出现的地方被替换。

**正确做法三选一**：

```cpp
// [示例 17] 修复 ①：共同抽象基类（都继承 Geometry），而非 Square 继承 Rectangle
#include <cstdio>

struct Geometry { virtual int area() const = 0; virtual ~Geometry() = default; };
struct Rectangle : Geometry {
    int w_=0, h_=0;
    int area() const override { return w_*h_; }
    void width(int w){ w_=w; }  void height(int h){ h_=h; }
};
struct Square : Geometry {
    int s_=0;
    int area() const override { return s_*s_; }
    void side(int s){ s_=s; }
};

int main() {
    Rectangle r; r.width(3); r.height(4);
    Square s; s.side(5);
    Geometry* g1 = &r; Geometry* g2 = &s;
    printf("%d %d\n", g1->area(), g2->area());   // 12 25
}
```

```cpp
// [示例 18] 修复 ②：组合（Square 内部持有 Rectangle 作为实现，而非继承）
#include <cstdio>

struct Rectangle {
    int w=0, h=0;
    int area() const { return w*h; }
    void width(int x){ w=x; }  void height(int x){ h=x; }
};

struct Square {
    Rectangle r;                       // 组合：复用 Rectangle 实现
    void side(int s){ r.width(s); r.height(s); }   // 主动维持不变量
    int  area() const { return r.area(); }
};

int main() { Square s; s.side(4); printf("%d\n", s.area()); }  // 16
```

```cpp
// [示例 19] 修复 ③：根本不做继承，直接用独立类型 + 自由函数
#include <cstdio>

struct Rect { int w=0, h=0; int area() const { return w*h; } };
struct Sqr  { int s=0;       int area() const { return s*s; } };

int main() { Rect r{3,4}; Sqr s{5}; printf("%d %d\n", r.area(), s.area()); }
```

**[经验]**　经验法则：当你想写 `D : public B` 时，先问「`D` 能否在不破坏 `B` 任何契约的前提下替换 `B`？」答不上来就别继承。`Square`/`Rectangle` 教科书式地告诉你：**is-a 要看行为契约，不是看自然语言里的「是」字**。

**核心知识点 #12**：public 继承必须满足 LSP；`Square:Rectangle` 是经典反例（设宽高破坏不变量），正确做法是共同抽象 / 组合 / 独立类型。

---

## ⑩ 切片（slicing）完整机制

**[标准]**　`[class.copy.ctor]` / `[dcl.init]`：当把派生类对象**按值**赋给/初始化基类对象时，只拷 `Base` 子对象部分，**派生类独有的成员被丢弃**，这就是**切片（slicing）**。若基类有虚函数，基类子对象里的 vptr 被**基类自己的 vptr** 覆盖，动态多态行为随之丧失。

**[平台]**　对象布局（Itanium ABI，GCC/Clang 一致）：`Derived` 的地址 == 其首基类的地址（单继承、非虚继承时），派生部分紧随基类子对象之后。

```
对象布局（单继承，无虚继承）：
        +-------------------+
        |  Base 子对象       |  <- 偏移 0；若多态则内含 vptr
        |   (Base 的数据)    |
        +-------------------+
        |  Derived 独有部分  |  <- 偏移 sizeof(Base 子对象)；被切片丢弃
        +-------------------+

Derived d;  Base b = d;   // 只拷贝 Base 子对象（含其 vptr），Derived 部分丢失
```

```cpp
// [示例 20] 切片：派生数据丢失
#include <cstdio>

struct Base { int b = 1; virtual ~Base() = default; };
struct Derived : Base { int d = 99; };

int main() {
    Derived src;
    Base sliced = src;                 // 切片！只拷 Base 子对象
    printf("b=%d\n", sliced.b);        // 1
    // 无法访问 sliced.d —— 它从未被拷贝进来
}
```

```cpp
// [示例 21] 切片 + 多态丧失：vptr 被基类覆盖
#include <cstdio>

struct Base {
    virtual const char* who() const { return "Base"; }
    virtual ~Base() = default;
};
struct Derived : Base {
    const char* who() const override { return "Derived"; }
};

void describe(Base b) {                // 按值传参 → 切片
    printf("%s\n", b.who());           // 永远输出 Base！
}

int main() {
    Derived d;
    describe(d);                       // 输出 "Base"（动态派发已丢）
}
```

```cpp
// [示例 22] std::vector<Base> 存派生会切片
#include <cstdio>
#include <vector>

struct Shape { virtual double area() const { return 0; } virtual ~Shape()=default; };
struct Circle : Shape { double r=3; double area() const override { return 3.14*r*r; } };

int main() {
    std::vector<Shape> v;
    v.push_back(Circle{});             // 切片！Circle 数据仅 r 丢了
    printf("%.2f\n", v[0].area());     // 0.00（Shape::area，无 Circle 半径）
}
```

**[经验]**　切片的三个高频来源：① 函数按值接收基类参数；② 返回基类值；③ 把派生对象塞进 `vector<Base>` 这类同质容器。第 11 节给出修复。

**核心知识点 #13**：`Derived d; Base b = d;` 只拷贝 Base 子对象，派生部分丢失。
**核心知识点 #14**：`std::vector<Base>` 存派生会切片，丢失派生数据与多态。

---

## ⑪ 切片修复：引用 / 指针 / unique_ptr<Base>

**[标准]**　`[class.derived]` / `[expr]`：引用和指针**不复制对象**，只绑定/指向原对象，因此不触发切片。智能指针（见 `ch41`）同理——`std::unique_ptr<Base>` 持有的是基类指针，销毁时通过虚析构正确派发到派生析构（前提是基类析构 `virtual`，见 `ch39`/`ch47`）。

```cpp
// [示例 23] 修复 ①：按引用传参，避免切片与多态丧失
#include <cstdio>

struct Base { virtual const char* who() const { return "Base"; } virtual ~Base()=default; };
struct Derived : Base { const char* who() const override { return "Derived"; } };

void describe(const Base& b) { printf("%s\n", b.who()); }   // 引用：不切片

int main() { Derived d; describe(d); }                       // Derived
```

```cpp
// [示例 24] 修复 ②：vector<unique_ptr<Base>>，多态容器不切片
#include <cstdio>
#include <vector>
#include <memory>

struct Shape { virtual double area() const { return 0; } virtual ~Shape()=default; };
struct Circle : Shape { double r=3; double area() const override { return 3.14*r*r; } };
struct Square : Shape { double s=2; double area() const override { return s*s; } };

int main() {
    std::vector<std::unique_ptr<Shape>> v;
    v.push_back(std::make_unique<Circle>());
    v.push_back(std::make_unique<Square>());
    for (auto& p : v) printf("%.2f\n", p->area());   // 28.26  4.00（无切片）
}
```

```cpp
// [示例 25] 修复 ③：基类指针 + 显式 new/delete（现代写法优先 unique_ptr）
#include <cstdio>

struct Base { virtual void f() const { printf("Base\n"); } virtual ~Base()=default; };
struct Derived : Base { void f() const override { printf("Derived\n"); } };

int main() {
    Base* p = new Derived;            // 指针：无切片
    p->f();                           // Derived
    delete p;                         // 虚析构 → 正确
}
```

**[经验]**　容器要装异构派生对象，**永远用 `vector<unique_ptr<Base>>`（或 `shared_ptr<Base>`）**，而不是 `vector<Base>`。这是 `ch41` 智能指针与 `ch39` 虚析构 `noexcept` 的直接应用点。

**核心知识点 #15**：用引用/指针/`unique_ptr<Base>`（见 `ch41`）避免切片；多态容器用 `vector<unique_ptr<Base>>`。

---

## ⑫ 构造 / 析构顺序实证

**[标准]**　`[class.base.init]` / `[class.dtor]`：构造顺序——（1）虚基类子对象（最左最深优先，见第 13 节）；（2）**按声明顺序**的直接基类子对象；（3）**按声明顺序**的非静态数据成员；（4）构造函数体。析构顺序**严格相反**。

```cpp
// [示例 26] 单继承构造/析构顺序：基类 → 成员 → 派生；析构反序
#include <cstdio>

struct Base {
    Base()  { printf("Base ctor\n"); }
    ~Base() { printf("Base dtor\n"); }
};
struct Member {
    Member()  { printf("Member ctor\n"); }
    ~Member() { printf("Member dtor\n"); }
};
struct Derived : Base {
    Member m;
    Derived()  { printf("Derived ctor\n"); }
    ~Derived() { printf("Derived dtor\n"); }
};

int main() { Derived d; }
// 输出：Base ctor → Member ctor → Derived ctor → Derived dtor → Member dtor → Base dtor
```

```cpp
// [示例 27] 多继承构造顺序：按基类声明序，析构反序
#include <cstdio>

struct B1 { B1()  { printf("B1 ctor\n"); }  ~B1() { printf("B1 dtor\n"); } };
struct B2 { B2()  { printf("B2 ctor\n"); }  ~B2() { printf("B2 dtor\n"); } };
struct D : B1, B2 {                 // 声明序 B1 先于 B2
    D()  { printf("D ctor\n"); }
    ~D() { printf("D dtor\n"); }
};

int main() { D d; }
// 输出：B1 ctor → B2 ctor → D ctor → D dtor → B2 dtor → B1 dtor
```

```cpp
// [示例 28] 成员按声明序构造（与初始化列表顺序无关）
#include <cstdio>

struct A { A(const char* s){ printf("%s ctor\n", s);} ~A(){printf("dtor\n");} };
struct C {
    A a1{"a1"};                     // 声明序 1
    A a2{"a2"};                     // 声明序 2
    C() : a2{"a2"}, a1{"a1"} {}     // 初始化列表乱序不影响构造序
};

int main() { C c; }                 // a1 ctor → a2 ctor（按声明序）
```

**[标准]**　异常安全：`[class.base.init]` 规定，若构造函数在进入函数体前（成员/基类初始化）抛异常，已构造的子对象会**按构造的逆序自动析构**（不需要函数体里的 `try`）。这与 `ch39`/`ch40` 的 RAII 与异常安全一致——`unique_ptr`/`vector` 等成员若在异常前已构造，会自动释放资源。

```cpp
// [示例 29] 构造中抛异常：已构部分自动逆序析构
#include <cstdio>
#include <stdexcept>

struct Raii { ~Raii() { printf("cleanup\n"); } };
struct Thrower {
    Raii guard;                     // 先构造
    Thrower() { printf("before throw\n"); throw std::runtime_error("boom"); }
};

int main() try {
    Thrower t;                      // guard 已构造，throw 后自动析构 guard
} catch (const std::exception& e) {
    printf("caught: %s\n", e.what()); // before throw → cleanup → caught: boom
}
```

**核心知识点 #16**：构造顺序 = 基类子对象 → 成员（按声明序） → 派生体；析构严格反序。
**核心知识点 #17**：多继承按**声明序**构造/析构；异常时已实现部分自动逆序析构（`ch39`/`ch40`）。

---

## ⑬ 多继承与虚基类构造顺序

**[标准]**　`[class.base.init]`：在存在**虚基类（virtual base，见 `ch49`）**时，无论继承路径如何，**虚基类子对象由最派生类（most derived class）直接初始化一次**，且它先于所有非虚基类构造。`[实现-推断]`　Itanium C++ ABI（GCC/Clang 遵循）把虚基类布局放在对象尾部（或独立于主基类链），通过构造期间的「虚基类表（VTT）/构造虚表（ctor vtable）」在中间基类构造函数里把虚基类指针重定向到最派生类提供的实例——这正是为什么中间基类构造时虚基类已存在，但只有最派生类真正「拥有」它。

```cpp
// [示例 30] 虚基类由最派生类构造一次（详细见 ch49）
#include <cstdio>

struct V { V() { printf("V(虚基类) ctor\n"); } ~V() { printf("V dtor\n"); } };
struct L : virtual V { L() { printf("L ctor\n"); } ~L() { printf("L dtor\n"); } };
struct R : virtual V { R() { printf("R ctor\n"); } ~R() { printf("R dtor\n"); } };
struct D : L, R { D() { printf("D(最派生) ctor\n"); } ~D() { printf("D dtor\n"); } };

int main() { D d; }
// 输出（Itanium）：V ctor → L ctor → R ctor → D ctor → D dtor → R dtor → L dtor → V dtor
```

**[实现-推断]**　MSVC 的虚继承布局（`/vd` 控制）与 Itanium 不同：MSVC 把 vfptr/vbptr 放在对象**头部**，并用「虚基类表指针（vbptr）」做偏移查找；GCC/Clang（Itanium）把虚基类放在尾部、用 VTT 管理。这导致同一份多继承代码在两种 ABI 下对象布局不同，但**可见行为一致**（见第 19 节）。

**核心知识点 #18**：多继承按声明序；虚基类由**最派生类**构造一次（详细见 `ch49`）。

---

## ⑭ 名字隐藏（name hiding）与 `using` 恢复重载

**[标准]**　`[class.member.lookup]`：派生类作用域中的名字会**遮蔽（hide）**基类作用域中**所有同名**名字——注意是「同名即隐藏全部重载」，**不是**重载解析。因此即使参数类型不同，基类同名函数也不可见。

```cpp
// [示例 31] 名字隐藏陷阱：基类 f(double) 被派生 f(int) 隐藏
#include <cstdio>

struct Base {
    void f(double) { printf("Base::f(double)\n"); }
};
struct Derived : Base {
    void f(int) { printf("Derived::f(int)\n"); }   // 隐藏 Base::f 全部重载
};

int main() {
    Derived d;
    d.f(1.0);                       // 调用 Derived::f(int)！1.0 被截断为 int 1
    // d.f(1.0) 不会去选 Base::f(double)，因为名字 f 已被隐藏
}
```

**[经验]**　示例 31 是静默 bug：`d.f(1.0)` 本意可能是 `Base::f(double)`，但因为 `Derived::f(int)` 把名字 `f` 整个隐藏，编译器只看到 `Derived::f(int)`，于是 `1.0` 被**截断为 `int 1`** 调用。这是数据精度丢失/语义错误的温床。

```cpp
// [示例 32] 用 using Base::f; 恢复基类重载集
#include <cstdio>

struct Base {
    void f(double) { printf("Base::f(double)\n"); }
    void f(int)    { printf("Base::f(int)\n"); }
};
struct Derived : Base {
    using Base::f;                  // 把 Base 的 f 重载集引入本作用域
    void f(const char*) { printf("Derived::f(const char*)\n"); }
};

int main() {
    Derived d;
    d.f(1.0);                       // 重载解析选中 Base::f(double)
    d.f(1);                         // Base::f(int)
    d.f("hi");                      // Derived::f(const char*)
}
```

```cpp
// [示例 33] 名字隐藏 vs 虚函数覆盖：两者机制不同
#include <cstdio>

struct Base {
    virtual void g(int)    { printf("Base::g(int)\n"); }
    virtual void g(double) { printf("Base::g(double)\n"); }   // 虚重载
};
struct Derived : Base {
    void g(int) override { printf("Derived::g(int)\n"); }     // 覆盖（同签名虚函数）
    // Base::g(double) 仍可见（虚函数名字未被隐藏，因为它没被同名非虚遮蔽）
};

int main() {
    Derived d;
    Base* p = &d;
    p->g(1);      // Derived::g(int)（动态派发）
    p->g(1.0);    // Base::g(double)（名字未被隐藏，正常虚调用）
}
```

**[标准-经验]**　**覆盖（override）** 是「派生类提供与基类**同签名虚函数**的新定义」，参与动态派发；**隐藏（hiding）** 是「派生类名字遮蔽基类同名名字（无论虚与否、无论签名）」。二者不要混为一谈：示例 31 的 `f` 是隐藏非覆盖，示例 33 的 `g(int)` 是覆盖非隐藏。需要「既覆盖又保留基类重载」时，用 `using Base::name;` 把基类重载集拉进来，再 `override` 其中一个。

**核心知识点 #19**：派生同名函数**隐藏基类所有重载**（非重载解析）。
**核心知识点 #20**：用 `using Base::func;` 把基类重载集引入派生作用域。

---

## ⑮ override / final（C++11）

**[标准]**　`[class.virtual]`（C++11 起）：
- `override`：显式声明「此函数意在覆盖基类虚函数」。若基类中**不存在**可匹配的虚函数，编译器**报错**——把「本想覆盖却因签名写错而悄悄新建重载」的静默 bug 变成编译错误。
- `final`：① 用于虚函数，禁止**进一步**派生类再覆盖它；② 用于类，禁止该类被继承。`[实现]`　`final` 给编译器一个强提示：该函数不可被进一步覆盖，从而可以**去虚化（devirtualize）**——把虚调用直接替换为静态调用，甚至内联，显著提升性能。

```cpp
// [示例 34] override：签名写错会被编译器抓住
#include <cstdio>

struct Base { virtual void draw(int) const { printf("Base::draw\n"); } };

struct Good : Base {
    void draw(int) const override { printf("Good::draw\n"); }   // OK
};

#if 0
struct Bad : Base {
    void draw(double) const override { }   // 编译错误：没有匹配的基类虚函数
    // 没有 override 时这只会“悄悄”成为新重载而非覆盖
};
#endif

int main() { Good g; const Base& b = g; b.draw(0); }
```

```cpp
// [示例 35] final：阻止进一步覆盖 + 助编译器去虚化
#include <cstdio>

struct Base { virtual int calc() const { return 1; } };
struct Mid : Base {
    int calc() const final override { return 2; }   // final：Leaf 不能再覆盖 calc
};
#if 0
struct Leaf : Mid {
    int calc() const override { return 3; }   // 编译错误：calc 是 final
};
#endif

struct Sealed final { int x = 0; };            // final 类：不能被继承
#if 0
struct X : Sealed {};                          // 编译错误：Sealed 是 final
#endif

int main() { Mid m; const Base& b = m; printf("%d\n", b.calc()); }
```

```cpp
// [示例 36] final 帮助去虚化（编译器能静态解析）
#include <cstdio>

struct A { virtual int f() const { return 1; } };
struct B : A { int f() const final override { return 2; } };  // final → 可去虚化

int call(const B& b) { return b.f(); }   // 编译器知道 B::f 不会被覆盖 → 可能内联为 return 2

int main() { B b; printf("%d\n", call(b)); }
```

**[经验]**　现代 C++ 铁律：**每个覆盖基类虚函数的派生函数都写 `override`**；确定不再需要被覆盖的虚函数（或确定不再被继承的类）写 `final`。这两点零开销、纯收益，是 `ch47` 虚函数章节的前提纪律。

**核心知识点 #21**：`override` 显式覆盖、防签名误写；`final` 阻止进一步覆盖并助编译器**去虚化**优化。

---

## ⑯ NVI（Non-Virtual Interface）惯用法

**[标准-经验]**　NVI（非虚接口，又称「模板方法模式」的 C++ 实现）：基类暴露一个 **public 非虚** 函数，它在内部做「前置检查 / 锁定 / 度量 / 日志」等公共骨架，再调用一个 **protected 或 private 虚** 函数让派生类定制核心逻辑。这样公共不变式永远被统一执行，派生类无法绕过前置/后置。

```cpp
// [示例 37] NVI：公有非虚封装 protected 虚，统一前置/后置
#include <cstdio>
#include <chrono>

class Task {
public:
    // 公有非虚：对外稳定接口，统一前置/后置
    void run() {
        preConditions();            // 前置：不变量/参数校验/加锁
        auto t0 = now();
        doRun();                    // 派生定制的核心逻辑（虚）
        postConditions();           // 后置：不变量恢复/解锁/度量
        printf("elapsed=%lldus\n", (long long)(now()-t0));
    }
    virtual ~Task() = default;
protected:
    virtual void doRun() = 0;       // 仅核心，派生实现
    void preConditions()  { printf("[pre] check\n"); }
    void postConditions() { printf("[post] restore\n"); }
private:
    static long long now() { return 0; }  // 简化：实际用 steady_clock
};

struct MyTask : Task {
    void doRun() override { printf("  doing work...\n"); }
};

int main() { MyTask t; t.run(); }
```

```cpp
// [示例 38] 对比「公有虚函数」的缺陷：无法统一前置检查
#include <cstdio>

// 反面教材：公有虚函数，派生类可“忘记”前置校验
class BadTask {
public:
    virtual void run() {                // 每个人都要自己记得做前置
        printf("  doing work...\n");
    }
    virtual ~BadTask() = default;
};
struct Sloppy : BadTask {
    void run() override {               // 忘了做前置检查/度量
        printf("  doing work (no pre/post)\n");
    }
};

int main() { Sloppy s; s.run(); }       // 前置/后置被绕过
```

**[经验]**　NVI 的三个硬收益：① **不变量强制**——前置/后置只在基类一处实现，派生类无法遗漏；② **可观测性**——度量、日志、锁统一加在 NVI 壳里，不影响 `doRun` 逻辑；③ **接口稳定**——`run()` 是非虚的，其签名/契约永不随派生变化，符合「接口稳定、实现可替换」的封装理想。代价是多一点间接调用（现代编译器可内联消除）。

**核心知识点 #22（NVI）**：基类 `public` 非虚调用 `protected/private` 虚（模板方法）；对比「公有虚函数」缺陷——无法统一前置检查/度量/锁。

---

## ⑰ 组合优于继承：protected 继承的替代

**[标准-经验]**　GoF《Design Patterns》与 C++ Core Guidelines **C.120–C.145** 一致主张：**优先组合（composition / containment）而非继承**，除非你确实需要「is-a / 子类型多态」。原因：继承暴露基类 protected 细节（脆弱基类，见第 5 节）、固化耦合、放大名字隐藏（第 14 节）风险。`protected` 继承尤其暧昧——它既不是 is-a（外部看不到子类型），又暴露了实现，几乎总能用「组合 + 转发」或 `private` 继承替代。

```cpp
// [示例 39] 组合替代 protected 继承：复用实现但不暴露基类
#include <cstdio>

struct Logger { void log(const char* m){ printf("[log] %s\n", m); } };

// 错误倾向：protected 继承把 Logger 暴露给派生链
#if 0
struct Component : protected Logger {
    void doThing(){ log("thing"); }
};
#endif

// 正确：组合持有 Logger，仅转发所需能力
struct Component {
    Logger log_;
    void doThing() { log_.log("thing"); }   // 只暴露精确接口，耦合最小化
};

int main() { Component c; c.doThing(); }
```

```cpp
// [示例 40] 用组合 + 显式接口替代 private 继承（更灵活、可换实现）
#include <cstdio>

struct Engine { void start(){ printf("engine start\n"); } };

// private 继承版（见示例 14）也可，但组合更松耦合：
struct Car {
    Engine engine_;
    void drive() { engine_.start(); printf("car driving\n"); }
    // 想换引擎？改成员类型即可，无需动继承树
};

int main() { Car c; c.drive(); }
```

**[经验]**　决策树：`需要多态/模板方法` → `public` 继承 + NVI；`仅需复用代码且对外隐藏` → 优先**组合**，`private` 继承次之（当需访问 `protected` 成员或用 `using` 提升基类接口时）；`protected` 继承 → 几乎不用，先想组合。Core Guidelines **C.145** 专门说：`protected` 继承多用于「把基类作为派生类的实现细节」，而这通常用组合表达得更干净。

**核心知识点 #23（组合）**：`protected` 继承的替代是**组合优于继承**；`protected` 继承暧昧、暴露实现，优先组合。

---

## ⑱ 真实 libstdc++ 源码逐行：is_base_of / is_convertible / uses_allocator / stl_construct

下面所有源码均来自本机 MinGW GCC 13.1.0 的 libstdc++，路径已标注。

### 18.1 `is_base_of` —— 派生到基关系的编译期探测

文件 `type_traits:1408-1412`（本机路径 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/type_traits`）：

```cpp
  /// is_base_of
  template<typename _Base, typename _Derived>
    struct is_base_of
    : public integral_constant<bool, __is_base_of(_Base, _Derived)>
    { };
```

**[实现]**　libstdc++（GCC 13）直接委托给**编译器内建 `__is_base_of`**（由 GCC 前端在 `[class.derived]` 语义上实现）。`__is_base_of(B, D)` 在 `B` 是 `D` 的基类（含自身、含多继承、含虚基类）时为真。标准变量模板在 `type_traits:3361`：

```cpp
  template<typename _Base, typename _Derived>
    inline constexpr bool is_base_of_v = __is_base_of(_Base, _Derived);
```

**[实现-推断]**　内建如何判定？GCC 的 `cxx_eval_is_base_of` / 类型系统遍历继承图：若 `D` 的「基类子对象集合」包含 `B`（考虑 `virtual` 合并为单一子对象），则成立。`[标准]` 规定 `is_base_of<B, B>` 为真（类被视为自己的基类），且对 `cv` 修饰和引用会先剥除。

### 18.2 手搓版 `is_base_of`：用 `static_cast` + SFINAE 探测（讲清内建背后的原理）

`[实现-推断]`　理解 `__is_base_of` 的机制，可看经典 SFINAE 实现（仅当 `D*` 能 `static_cast` 到 `B*` 时 `test<D>(...)` 才返回 `true_type`）：

```cpp
// [示例 41] 手搓 is_base_of：派生指针可 static_cast 到基类指针 → 是基类
#include <type_traits>
#include <iostream>

template<typename B, typename D>
struct my_is_base_of {
private:
    // 若 D* 能隐式转成 B*（即 D 以 public 方式派生自 B），选 true_type
    template<typename T>
    static std::true_type  test(const volatile B*);      // 优先匹配（更特化）
    static std::false_type test(const volatile void*);   // 兜底
    // 注意：这里用指针转换，public 继承才可通过 static_cast
public:
    static constexpr bool value =
        decltype(test(std::declval<D*>()))::value;
};

struct A {};
struct C : A {};
struct D : private A {};          // private 继承：C-style cast 才可行
int main() {
    std::cout << my_is_base_of<A, C>::value << "\n";   // 1（public 派生）
    // my_is_base_of<A, D> 取决于 test 是否能 static_cast（private 派生会失败→0，符合标准 public 语义）
}
```

**[标准-实现]**　关键差异：标准 `is_base_of` 对 **`private`/`protected` 继承也为真**（它只看「B 是否为 D 基类」，不看可达性），但 `static_cast`/`test` 手搓版只能检测 **public** 路径——这就是内建 `__is_base_of` 比 SFINAE 更权威的原因：内建直接读类型系统的继承关系，不受访问控制影响。

### 18.3 `is_convertible` —— 隐式可转换性

文件 `type_traits:1414-1455`（GCC 13 优先用内建）：

```cpp
#if __has_builtin(__is_convertible)
  template<typename _From, typename _To>
    struct is_convertible
    : public __bool_constant<__is_convertible(_From, _To)>
    { };
#else
  template<typename _From, typename _To,
           bool = __or_<is_void<_From>, is_function<_To>,
                        is_array<_To>>::value>
    struct __is_convertible_helper
    { typedef typename is_void<_To>::type type; };

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wctor-dtor-privacy"
  template<typename _From, typename _To>
    class __is_convertible_helper<_From, _To, false>
    {
      template<typename _To1>
	static void __test_aux(_To1) noexcept;
      template<typename _From1, typename _To1,
	       typename = decltype(__test_aux<_To1>(std::declval<_From1>()))>
	static true_type  __test(int);
      template<typename, typename>
	static false_type __test(...);
    public:
      typedef decltype(__test<_From, _To>(0)) type;
    };
#pragma GCC diagnostic pop

  /// is_convertible
  template<typename _From, typename _To>
    struct is_convertible
    : public __is_convertible_helper<_From, _To>::type
    { };
#endif
```

**[实现]**　解读：当编译器**没有** `__is_convertible` 内建时，libstdc++ 用 SFINAE 试探「`declval<_From>()` 能否传给接收 `_To` 的 `__test_aux`」。`#pragma GCC diagnostic ignored "-Wctor-dtor-privacy"` 很重要：若 `_From`/`_To` 的拷贝构造是 `private`，本应报警，但类型特性探测不该因访问检查失败而误报，故临时关闭该警告。`noexcept` 标记确保探测自身不影响 `is_nothrow_convertible` 推导。

```cpp
// [示例 42] is_convertible：派生 → 基类可隐式转（is-a 的编译期证据）
#include <type_traits>
#include <iostream>

struct B {};
struct D : B {};
int main() {
    std::cout << std::is_convertible<D*, B*>::value << "\n";   // 1：D* → B*
    std::cout << std::is_convertible<B*, D*>::value << "\n";   // 0：反向不可
    std::cout << std::is_base_of<B, D>::value      << "\n";    // 1
}
```

### 18.4 `uses_allocator.h` —— 构造时「使用分配器」协议

文件 `bits/uses_allocator.h:56-70`（本机路径 `.../include/c++/bits/uses_allocator.h`）：

```cpp
  template<typename _Tp, typename _Alloc, typename = __void_t<>>
    struct __uses_allocator_helper
    : false_type { };

  template<typename _Tp, typename _Alloc>
    struct __uses_allocator_helper<_Tp, _Alloc,
				   __void_t<typename _Tp::allocator_type>>
    : __is_erased_or_convertible<_Alloc, typename _Tp::allocator_type>::type
    { };

  /// [allocator.uses.trait]
  template<typename _Tp, typename _Alloc>
    struct uses_allocator
    : __uses_allocator_helper<_Tp, _Alloc>::type
    { };
```

**[实现]**　`uses_allocator<T, Alloc>` 为真的条件：`T` 有嵌套类型 `allocator_type`，且 `Alloc` 可转换为它。它利用 **SFINAE + `__void_t`**（检测 `T::allocator_type` 是否存在）与 **偏特化** 实现「如果 `T` 含 `allocator_type` 就进一步校验可转换性，否则直接 `false_type`」。这正是「用类型萃取探测继承/嵌套类型」的工业级范例——与本章 `is_base_of` 探测基类关系一脉相承。

### 18.5 `stl_construct.h` —— `_Construct` 与构造的底层真相

文件 `bits/stl_construct.h:105-120`：

```cpp
#include <utility>
#if __cplusplus >= 201103L
  template<typename _Tp, typename... _Args>
    _GLIBCXX20_CONSTEXPR
    inline void
    _Construct(_Tp* __p, _Args&&... __args)
    {
#if __cplusplus >= 202002L
      if (std::__is_constant_evaluated())
	{
	  std::construct_at(__p, std::forward<_Args>(__args)...);
	  return;
	}
#endif
      ::new((void*)__p) _Tp(std::forward<_Args>(__args)...);
    }
```

**[实现]**　`_Construct` 是 libstdc++ 容器（vector/deque…）在「已分配但未初始化内存」上**就地构造**对象的原语——就是 `placement new`：`::new(ptr) T(args)`。这与本章构造顺序（第 12 节）直接相关：当容器扩容、在缓冲区尾部 `_Construct` 一个元素时，该元素的构造遵循「基类→成员→体」的标准顺序。C++20 起若处于常量求值（`__is_constant_evaluated`）则改用 `std::construct_at` 以支持 `constexpr` 容器。

**[实现-推断]**　它与切片的关联：当你 `push_back(Derived{})` 进 `vector<Base>`（示例 22），容器在 `Base` 大小的槽位上 `_Construct<Base>(slot, Derived临时量)`——实参是 `Base` 的拷贝构造（因为形参类型是 `Base&&`/`const Base&`），**构造的就是一个纯 `Base` 子对象**，派生部分从一开始就没进容器。这正是切片发生在「构造点」的铁证，而非「赋值点」。

---

## ⑲ 三编译器对比：GCC / LLVM / MSVC

| 维度 | GCC (libstdc++) | Clang (libc++) `[实现-推断]` | MSVC (MS STL) |
|------|----------------|------------------------------|---------------|
| `is_base_of` 实现 | 内建 `__is_base_of` | 内建 `__is_base_of` | 内建 `__is_base_of` |
| 对象模型 / 多继承布局 | Itanium ABI（虚基类在尾部） | Itanium ABI（与 GCC 一致） | **MS ABI**（vbptr 在头部，`/vd` 调布局） |
| 名字隐藏警告 | `-Woverloaded-virtual` | `-Woverloaded-virtual` | **`/Woverloaded-virtual`**（同名隐藏虚函数时告警） |
| 漏写 override 警告 | **`-Wsuggest-override`** | `-Wsuggest-override` | `/weffc++`（部分）、`/w44640` 等 |
| 虚继承布局控制 | 固定 Itanium | 固定 Itanium | `/vd1`（vbptr 在头部）/ `/vd2`（在尾部，兼容 Itanium） |
| `[[nodiscard]]` 继承接口 | 支持（C++17/20） | 支持 | 支持 |

**[平台]**　`-Wsuggest-override`（GCC/Clang）会在「覆盖虚函数却没写 `override`」时给出提示，把示例 34 的纪律变成编译器助攻。`/Woverloaded-virtual`（MSVC）与 `-Woverloaded-virtual`（GCC/Clang）会在「派生类同名函数隐藏了基类虚函数重载」时告警——直接针对第 14 节名字隐藏陷阱。

```cpp
// [示例 43] 触发 -Woverloaded-virtual 的名字隐藏（GCC/Clang 加 -Woverloaded-virtual）
struct Base {
    virtual void f(int)    { }
    virtual void f(double) { }      // 虚函数重载
};
struct Derived : Base {
    void f(int) override { }        // 仅覆盖 f(int)
    // 注意：Base::f(double) 仍可见，未隐藏（没有同名非虚遮蔽它）
};

// 真正触发“重载虚函数被隐藏”告警的情形：
struct B2 { virtual void g(int){} virtual void g(double){} };
struct D2 : B2 { void g(int) override {} };   // 安全：虚重载未被隐藏
// 若 D2 写 void g(int){}（无 override）且 B2 有 g(double)，某些 -Woverloaded-virtual 形态会告警
```

```cpp
// [示例 44] [[nodiscard]] 标定继承接口，防止忽略返回值
#include <cstdio>

struct Handler {
    [[nodiscard]] virtual bool commit() { printf("commit\n"); return true; }
    virtual ~Handler() = default;
};
struct MyHandler : Handler {
    [[nodiscard]] bool commit() override { printf("my commit\n"); return false; }
};

int main() {
    MyHandler h;
    // h.commit();   // 警告：ignoring return value of 'commit' declared 'nodiscard'
    if (!h.commit()) printf("rolled back\n");
}
```

**[实现-推断]**　Clang 的虚基类构造顺序（见第 13 节示例 30）与 GCC 一致：均遵循 Itanium ABI 的 VTT 机制，由最派生类统一构造虚基类；MSVC 走自己的 vbptr 路径，但**构造/析构的可见顺序相同**（虚基类最先构造、最后析构）。

---

## ⑳ microbenchmark：切片、构造顺序、NVI、override 缺失

下面用可编译小程序实证四个工程关注点。为简洁，计时用 `std::chrono` 的粗粒度演示（生产基准见 Google Benchmark）。

```cpp
// [示例 45] 微基准 ①：切片导致派生数据丢失（正确性，非性能）
#include <cstdio>
#include <vector>

struct Base { int id = 0; virtual ~Base()=default; };
struct Derived : Base { double extra = 3.14159; };

int main() {
    Derived d; d.id = 7;
    std::vector<Base> v; v.push_back(d);     // 切片：extra 丢失
    printf("id=%d extra_lost=%d\n", v[0].id, (int)sizeof(v[0]));  // id=7，sizeof=Base
}
```

```cpp
// [示例 46] 微基准 ②：构造/析构顺序日志（运行时可观测）
#include <cstdio>

struct Tracer {
    const char* name;
    Tracer(const char* n):name(n){ printf("+%s\n", name); }
    ~Tracer(){ printf("-%s\n", name); }
};
struct Base { Tracer b{"Base"}; };
struct Mid  { Tracer m{"Mid"}; };
struct Derived : Base, Mid { Tracer d{"Derived"}; };

int main(){ Derived d; }   // +Base +Mid +Derived -Derived -Mid -Base
```

```cpp
// [示例 47] 微基准 ③：NVI 前置检查收益（统一度量，派生无法绕过）
#include <cstdio>

class Op {
public:
    void run(int x){
        if (x < 0) { printf("rejected by pre-check\n"); return; }  // 统一前置
        printf("cost=%d\n", doRun(x));                             // 统一度量
    }
    virtual ~Op()=default;
protected:
    virtual int doRun(int x)=0;
};
struct Add : Op { int doRun(int x) override { return x+1; } };

int main(){
    Add a;
    a.run(-5);     // 被前置检查拦截，派生无法绕过
    a.run(10);     // cost=11
}
```

```cpp
// [示例 48] 微基准 ④：漏写 override → 静默错误（基准对照“有 override”）
#include <cstdio>

struct Base { virtual void tick() { printf("base tick\n"); } virtual ~Base()=default; };

// 错误示范：本想覆盖，却因签名差异（漏 const）成了新重载
struct Buggy : Base {
    void tick() /* 应为 void tick() const 覆盖，却写错 */ { printf("buggy tick\n"); }
};

int main(){
    Buggy b; Base& r = b;
    r.tick();     // 输出 "base tick" —— 静默调用了基类版本！
    // 若写 override 编译器会立刻报错，避免此静默 bug
}
```

**[经验]**　示例 48 是真实事故源头：大型代码库里「想覆盖却没覆盖」每年都会造成生产 bug。`override` 把这类错误从「运行时偶发」前移到「编译期必现」。基准对比很简单——加 `override` 后，示例 48 的 `struct Buggy` 会编译失败，逼你修正签名。

---

## 跨语言对比：继承与封装的语义差异

| 语言 | 继承模型 | 默认方法可重写？ | 封装/访问控制 | 类比 C++ |
|------|---------|----------------|--------------|---------|
| **Java** | 单继承 + 接口（`implements`） | **所有非 `static` 非 `final` 方法默认虚**（可重写） | `private`/`protected`/`public` + 包内可见；无友元 | 近似 C++ public 继承 + 默认虚 |
| **C#** | 单继承 + 接口 | **默认非虚**，须显式 `virtual` + `override` | `private`/`protected`/`internal`/`public`；`sealed`=C++ `final` | 近似 C++，但虚默认关 |
| **Rust** | **无继承**；用 `trait` 组合 + 默认静态分发 | 无方法重写；`trait` 默认静态派发，dyn trait 才动态 | 模块级 `pub` 控制；无 `protected`/`friend` | 组合优于继承的极端化 |
| **Go** | **无继承**；`struct` 嵌入（embedding）实现方法提升 | 嵌入类型方法被提升，可遮蔽 | 标识符首字母大小写控制可见性 | 组合/嵌入 ≈ C++ 组合 |

**[经验]**　关键差异洞察：

- **Java 默认方法虚**：`class D extends B { void f(){} }` 只要签名一致就覆盖，无需 `override` 关键字（Java 5+ 有 `@Override` 注解但非强制）。这与 C++ 的「默认非虚、需 `virtual`+`override`」相反——Java 程序员初学 C++ 常犯「忘了写 `virtual`/`override` 导致不多态」的错（见示例 48）。
- **C# 显式 `virtual`/`override`/`sealed`**：与 C++ 的 `virtual`/`override`/`final` 几乎一一对应，是最接近 C++ 心智模型的语言。
- **Rust/Go 无继承**：彻底回避了本章讨论的切片、名字隐藏、脆弱基类——用 trait/嵌入的组合模型。代价是失去「is-a 子类型多态」的简洁表达，改用显式 trait 对象（`Box<dyn Trait>`）实现运行时多态。

```go
// [示例 49] Go 嵌入（embedding）近似“组合优于继承”（Go 伪代码，非 C++）
// type Engine struct{ }
// func (e Engine) Start(){ println("engine start") }
// type Car struct{ Engine }      // 嵌入：Car 自动获得 Engine 的方法（方法提升）
// func main(){ c := Car{}; c.Start() }   // 相当于 C++ 组合 + using/转发
```

```java
// [示例 50] Java 默认虚方法（Java 伪代码）
// class Base { void f() { System.out.println("base"); } }
// class Derived extends Base { void f() { System.out.println("derived"); } } // 自动覆盖
// 对应 C++ 必须写 virtual + override，否则不多态
```

---

## 源码阅读路线与小结

**[标准/经验]**　想把本章吃透，按这条路线读源码与文献：

1. **Lippman《Inside the C++ Object Model》第 3 章**——「The Semantics of Data」：单/多/虚继承的对象布局、基类子对象偏移、vptr 位置、虚基类表（VBTable）。这是理解「切片为什么丢数据」「构造顺序为什么如此」的底层地图。
2. **C++ Core Guidelines C.120–C.145**——`C.120`（用继承表达 is-a）、`C.129`（prefer `private` over `protected` base）、`C.135`（用 `virtual` 公开接口并用 NVI）、`C.145`（`protected` 继承的取舍）、`C.128`（虚函数配 `override`）。
3. **Clang `CXXRecordDecl` 继承模型**——Clang AST 中 `CXXRecordDecl::bases()` 遍历直接基类，`getNumBases()`/`forallBases()` 递归；`data().IsPolymorphic`/`HasTrivialDestructor` 等位域决定构造/析构生成策略。理解编译器如何「看到」继承树。
4. **LLVM `RecordLayout`**（`clang/lib/AST/RecordLayout.cpp`）——计算各基类子对象偏移、`NonVirtualSize`、`PreferredAlignment`、虚基类偏移表。本章对象布局图（第 10、13 节）正是 `RecordLayout` 输出的可读化。
5. **libstdc++ `type_traits`**（本机 `.../include/c++/type_traits`）——`is_base_of` / `is_convertible` 的内建委托与 SFINAE 回退（第 18 节已逐行）。
6. 交叉章节：`ch19`（存储期）、`ch39`（RAII、析构 `noexcept` 与构造异常安全）、`ch40`（异常安全等级）、`ch41`（`unique_ptr<Base>` 容器避免切片）、`ch45`（对象模型基础、`offsetof` 边界）、`ch47`（虚函数与 vtable、去虚化）、`ch49`（虚继承完整机制）。

**本章 23 项核心知识点回顾**：
1. 封装/继承是编译期机制，不生成运行期数据（虚函数才生成 vtable）。
2. 不变量（invariant）责任落在成员函数/友元身上。
3. private 仅编译期拒绝越权；运行期 `memcpy`/`offsetof` 可触及——封装是编译期契约非运行时保险箱。
4. 友元是受控破封装：非成员、不可继承、不可传递、最小化。
5. public/private/protected 都是编译期访问控制。
6. `protected` 有脆弱基类问题。
7. 访问检查在编译期，不生成代码。
8. class/struct 唯一区别：默认成员访问 + 默认继承方式。
9. class 默认 private 继承，做基类务必显式 `: public`。
10. 三种继承语义：public = is-a；protected = 派生可见实现继承；private = 外部不可见实现继承（少用）。
11. public 继承满足 LSP（派生可替换基类）。
12. Square:Rectangle 违反 LSP；修复=共同抽象/组合/独立类型。
13. `Derived d; Base b=d;` 只拷 Base 子对象，派生部分丢失。
14. `vector<Base>` 存派生会切片。
15. 用引用/指针/`unique_ptr<Base>` 避免切片。
16. 构造顺序：基类子对象 → 成员（声明序） → 派生体；析构反序。
17. 多继承按声明序；异常时已实现部分自动逆序析构（`ch39`/`ch40`）。
18. 虚基类由最派生类构造一次（`ch49`）。
19. 派生同名函数隐藏基类所有重载（非重载解析）。
20. `using Base::func;` 恢复基类重载集。
21. `override` 防误写；`final` 阻覆盖助去虚化。
22. NVI：public 非虚调 protected/private 虚；对比公有虚函数缺陷（无法统一前置/度量/锁）。
23. `protected` 继承替代 = 组合优于继承。

**20 章元素回顾**：概述 → 封装本质 → 封装边界真相 → 友元 → 访问控制语义 → class vs struct → 三种继承 → LSP → Square/Rectangle → 切片机制 → 切片修复 → 构造/析构顺序 → 虚基类构造 → 名字隐藏 → override/final → NVI → 组合优于继承 → 真实 libstdc++ 源码 → 三编译器对比 → microbenchmark → 跨语言 → 阅读路线小结（共 22 节，覆盖 20 元素 + 23 知识点）。

实战纪律总结：
- 成员能 `private` 就 `private`，数据尤甚；`protected` 数据基本是 smell。
- 友元给函数不给类；`friend` 不到万不得已不开。
- `public` 继承前先过 LSP 测试；不过就改用组合。
- 多态容器用 `vector<unique_ptr<Base>>`，绝不 `vector<Base>`。
- 覆盖基类虚函数一律写 `override`；稳态虚函数写 `final`。
- 需要统一前置/后置/度量 → NVI，别把虚函数直接 `public`。
- 派生类要复用基类重载集时，记得 `using Base::name;`。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第45章](Book/part05_oo/ch45_oop_object_model.md) | 独占所有权/工厂模式 | 本章提供概念，第45章提供实现 |
| [第45章](Book/part05_oo/ch45_oop_object_model.md) | 无锁队列/计数器 | 本章提供概念，第45章提供实现 |
| [第47章](Book/part05_oo/ch47_virtual_functions.md) | 多态插件/框架扩展 | 本章提供概念，第47章提供实现 |
| [第29章](Book/part03_language/ch29_friend.md) | 泛型库/编译期计算 | 本章提供概念，第29章提供实现 |

## 附录 F：封装继承工业与面试

```cpp
#include <iostream>
struct Base{virtual void f(){std::cout<<"Base"<<std::endl;}};
struct Derived:Base{void f()override final{std::cout<<"Derived"<<std::endl;}};
int main(){Base*b=new Derived;b->f();delete b;return 0;}
```

| 继承类型 | 访问 | 典型场景 |
|---|---|---|
| public继承 | is-a关系 | 多态接口(虚函数) |
| private继承 | implemented-in-terms-of | EBO, 限制接口 |
| protected继承 | 极少使用 | 允许子类进一步继承 |

面试: 三种继承区别? public=is-a+保持接口; private=实现继承+隐藏接口
       为什么用private继承? 空基类优化(EBO), 限制暴露基类接口


## 附录 H：访问控制面试

```cpp
#include <iostream>
struct B{private:int x=1;protected:int y=2;public:int z=3;};
struct D:B{void show(){std::cout<<y<<","<<z<<std::endl;}};
int main(){D d;d.show();return 0;}
```

| 访问 | 自身 | 派生 | 外部 |
|---|---|---|---|
| private | 是 | 否 | 否 |
| protected | 是 | 是 | 否 |
| public | 是 | 是 | 是 |

面试: private继承作用? EBO+隐藏接口; protected继承? 几乎不用

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。每个链接指向具体仓库，可逐行对照工业落地。

- **Qt 6（github.com/qt/qtbase）**：`QObject` 继承体系（`QWidget→QFrame→...`）是封装+继承工业范例；`Q_DISABLE_COPY` 宏用 `= delete` 禁用拷贝，是"封装不变式"的工程化表达。
  → <https://github.com/qt/qtbase>
- **Chromium（github.com/chromium/chromium）**：`base::RefCounted` 用继承实现引用计数；`base::SupportsWeakPtr` 通过 CRTP 基类注入弱引用能力，是"继承注入能力"而非 is-a 的典范。
  → <https://github.com/chromium/chromium>
- **LLVM（github.com/llvm/llvm-project）**：`clang::Decl` 继承树展示编译器前端如何用继承建模语法节点层次；`llvm::RefCountedBase` 是引用计数的基类模板。
  → <https://github.com/llvm/llvm-project>
- **Boost（github.com/boostorg）**：`boost::noncopyable` 以私有基类的空基类优化（EBO）实现禁拷贝，是"用继承表达接口约束"的工业范本。
  → <https://github.com/boostorg>
- **Abseil（github.com/abseil/abseil-cpp）**：`absl::MutexLock` 的 RAII 包装体现"封装同步原语"的最佳实践，避免裸锁的遗漏解锁。
  → <https://github.com/abseil/abseil-cpp>

**常见陷阱 / 最佳实践**：
- 继承默认非虚析构会导致切片/UB；基类析构应 `virtual` 或 `final` 禁止继承。
- 优先组合优于继承（has-a 而非 is-a），接口隔离用纯虚基类。

> 交叉引用：对象模型见 [ch45](Book/part05_oo/ch45_oop_object_model.md)；RAII 见 [ch39](Book/part04_memory/ch39_raii_rule.md)；CRTP 见 [ch51](Book/part05_oo/ch51_crtp.md)；EBO 见 [ch52](Book/part05_oo/ch52_ebo.md)。

## 相关章节（交叉引用）

- **相邻主题**：`Book/part04_memory/ch44_memory_pool.md`（第 44 章 内存池（Memory Pool）从零实现）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part05_oo/ch48_rtti.md`（第48章 RTTI 与 typeid/dynamic_cast：运行时类型查询）—— 编号相邻、主题接续。
- **同模块**：`Book/part05_oo/ch49_virtual_inheritance.md`（第49章 虚继承与菱形继承：共享虚基类）—— 同模块下的其他主题。


## 附录 G（对象布局与继承）

单继承对象内存连续，下列为典型偏移。

```text
; Derived 对象（Base 在前）
mov rax, [rdi+0x0000]     ; 取 Base 子对象 vptr
mov rcx, [rax+0x0008]     ; 取 Base::foo 槽
call [rcx]
mov rdx, [rdi+0x0010]     ; 取 Derived 独有成员（偏移 0x0010）
```

### 布局

- Base 子对象居 `0x0000`；Derived 成员从 `0x0010` 起（vptr 占 `0x0008`）
- 封装的私有成员同样占 `0x0008` 对齐槽，不增减访问代价
- L1 缓存行 `0x0040` 字节；false sharing 使跨核写放大到 ≈ 100ns

### 量级

- 成员访问 `mov rax,[rdi+0x0010]` ≈ 1.0ns（L1 命中）
- 虚调用间接跳转 ≈ 3.2ns（BTB miss 18ns）
- 继承层数 > 0x0008 时构造链 ≈ 0.5us

### 编译器与标准

- GCC 13.2 / Clang 18 / MSVC 19.3 布局一致（MSVC 有虚基类差异）
- `__cplusplus` = 202302L；`-fwhole-program-vtables` 去虚化
- `constexpr` 构造省运行时初始化


## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写代码演示**对象切片（slicing）**：把派生对象赋给基类对象时派生部分丢失，并说明如何用引用/指针/智能指针保留完整对象。

<details><summary>答案与解析</summary>

基类对象是派生对象前缀子对象的拷贝；赋值时只复制基类子对象，派生新增成员被丢弃。多态须经由引用或指针（或 `unique_ptr<Base>`）而非值。

```cpp
#include <iostream>
struct Base { int b = 1; virtual ~Base() = default; };
struct Derived : Base { int d = 2; };
int main() {
    Derived der;
    Base sliced = der;                       // 切片：仅复制 Base 子对象
    std::cout << "sliced.b = " << sliced.b << '\n';   // 1，正常
    // sliced.d 不存在：派生部分已丢失
    Base& ref = der;                         // 引用保持完整对象
    std::cout << "via ref d = "
              << static_cast<Derived&>(ref).d << '\n'; // 2
}
```

[标准] 切片是值语义的直接后果；维度⑩说明"引用/指针才多态"，维度⑪给出 `unique_ptr<Base>` 修复。

</details>

### 练习 2（难度 ★★★）

演示**名字隐藏（name hiding）**：派生类定义同名函数会隐藏基类所有重载（而非重载），并用 `using` 恢复重载集。

<details><summary>答案与解析</summary>

C++ 的名字查找在找到派生类作用域的 `f` 后即停止，不再向基类合并重载集。显式 `using Base::f;` 把基类重载引入派生作用域。

```cpp
#include <iostream>
struct Base { void f(int) { std::cout << "Base::f(int)\n"; } };
struct Derived : Base {
    void f(double) { std::cout << "Derived::f(double)\n"; }  // 隐藏 Base::f(int)
};
int main() {
    Derived d;
    d.f(1);    // 调 Derived::f(double)，Base::f(int) 被隐藏（非重载）
}
```

**修复**（恢复重载集）：

```cpp
#include <iostream>
struct Base { void f(int) { std::cout << "Base::f(int)\n"; } };
struct Derived : Base {
    using Base::f;                              // 恢复基类重载集
    void f(double) { std::cout << "Derived::f(double)\n"; }
};
int main() {
    Derived d;
    d.f(1);    // Base::f(int)
    d.f(1.0);  // Derived::f(double)
}
```

[标准] 名字隐藏是编译期作用域规则（维度⑬），与虚函数多态无关；忘了 `using` 是经典易错点。

</details>

### 练习 3（难度 ★★★★）

用 **NVI（Non-Virtual Interface）惯用法**实现模板方法模式：公共非虚接口负责前置/后置与不变式，派生类只实现受保护的虚步骤。

<details><summary>答案与解析</summary>

NVI 把契约（前置条件、后置条件、不变式、日志）收敛在非虚公共接口，用户无法绕过；派生类仅覆写虚步骤，降低误用面。

```cpp
#include <iostream>
#include <cassert>
class Algorithm {
public:
    void run() {                     // 非虚公共接口：不变式守卫
        std::cout << "pre\n";
        doRun();                     // 委托虚步骤
        std::cout << "post\n";
        assert(invariant());
    }
    virtual ~Algorithm() = default;
protected:
    virtual void doRun() = 0;
    virtual bool invariant() const { return true; }
};
struct Impl : Algorithm {
    void doRun() override { std::cout << "Impl::doRun\n"; }
};
int main() { Impl a; a.run(); }
```

[标准] NVI 是维度⑯/⑰的核心惯用法；对比"直接暴露 virtual"更易维护契约，是封装边界（维度③）的工程落地。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：切片 bug——函数返回基类值

**选型场景**：多态处理一组派生对象，想通过一个统一函数返回结果。

**常见错误**：函数签名返回 `Base`（值），调用方拿到的是切片后的截断对象，丢失派生行为。

```cpp
#include <iostream>
struct Base { int b = 1; virtual ~Base() = default; };
struct Derived : Base { int d = 2; };
Base process(Derived d) { return d; }   // 切片：返回的是 Base 子对象
int main() {
    Derived der;
    Base r = process(der);
    // 无法访问 d；多态被破坏
}
```

**修复**：返回基指针 / `unique_ptr<Base>` / `Base&`，让多态经引用或指针传递。

```cpp
#include <iostream>
#include <memory>
struct Base { int b = 1; virtual ~Base() = default; };
struct Derived : Base { int d = 2; };
std::unique_ptr<Base> process(Derived d) {
    return std::make_unique<Derived>(std::move(d));  // 完整对象经智能指针传递
}
int main() {
    auto p = process(Derived{});
    std::cout << static_cast<Derived*>(p.get())->d << '\n'; // 2，派生部分保留
}
```

**结论**：切片是值语义的天然结果（维度⑩）；需要多态就必须走引用/指针/智能指针（维度⑪）。

### 演绎 2：忘记 `override` 导致静默隐藏而非覆盖

**选型场景**：派生类想覆写基类虚函数以定制行为。

**常见错误**：派生类函数签名写错（如参数类型不符），未用 `override`；编译器将其视为**新函数**而非覆写，调用仍走基类版本——编译通过但行为错误。

```cpp
#include <iostream>
struct Shape { virtual void draw() { std::cout << "Shape\n"; } };
struct Circle : Shape {
    void draw(int) { std::cout << "Circle(draw int)\n"; }  // 非 override：新重载，隐藏 draw()
};
int main() {
    Shape* s = new Circle;
    s->draw();        // 调 Shape::draw()——本想调 Circle，但签名不符未被覆盖
}
```

**修复**：基类虚函数保持 `virtual`，派生加 `override`（签名不符立即编译错误）；用 `final` 锁死不再被进一步覆盖。

```cpp
#include <iostream>
struct Shape { virtual void draw() = 0; };
struct Circle : Shape {
    void draw() override { std::cout << "Circle::draw\n"; }  // 编译期保证真正覆盖
};
int main() { Shape* s = new Circle; s->draw(); }
```

**结论**：`override`/`final`（维度⑮）把"是否真覆盖"从运行期隐患变成编译期强制，是封装与继承（维度⑧/⑮）的工程红线。
