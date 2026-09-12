# 资料研究第二十三轮：C++ 对象模型与 ABI——vtable/vptr、虚函数调用、多继承与虚继承布局、RTTI/dynamic_cast、EBCO

> 2026-09-11，底层工程资料研究员。主题：C++ 对象内存布局、Itanium C++ ABI vtable 内部结构（offset-to-top/typeinfo/虚函数指针）、虚函数调用机制、单继承/多继承/虚继承对象布局、thunk 与 this 指针调整、vbtable 与虚基类偏移、RTTI 与 type_info 实现、dynamic_cast 原理、空基类优化（EBCO）、对象大小计算。
> 检索方式：general_search + Itanium C++ ABI 规范（Linux Foundation 1.75 + GitHub cxx-abi）+ peter0x44 vtable 详解 + Dr-Sergey Itanium ABI 布局 + Arthur O'Dwyer CppCon 2017 dynamic_cast + NDX GCC 逆向训练 + PVS-Studio 对齐系列 + LLVM Relative VTables。
> **ABI 域第一轮**。与第二十二轮 name mangling、第十六轮异常实现形成完整 ABI 知识链。

---

## 一、C++ 对象模型基础

### 1. 空类大小 = 1 字节（不是 0！）

```cpp
class Empty {};
sizeof(Empty);  // 1，不是 0
```

- **原因**：每个对象必须有唯一地址。如果 size=0，两个对象可能地址相同，无法区分。
- **标准要求**：most-derived 对象必须非零大小
- **例外**：基类子对象不受此限制 → 空基类优化（EBCO，见第八节）

### 2. 非多态对象

```cpp
struct Point { int x; int y; };
// 内存布局：[x(4)] [y(4)] = 8 字节
```

- 只有数据成员 + padding
- 没有 vptr，没有运行时开销

### 3. 多态对象

```cpp
struct Shape {
    virtual void draw();
    int color;
};
// 内存布局（64位）：[vptr(8)] [color(4)] [padding(4)] = 16 字节
```

- vptr 在 offset 0（Itanium ABI 约定）
- vptr 指向该类的 vtable
- 构造函数中设置 vptr，析构函数中恢复

- **来源**：DevTut object layout + PVS-Studio 对齐 + CSDN class 大小
- **可信度**：S

---

## 二、vtable 的内部结构（Itanium ABI）

### 1. vtable 不是简单的函数指针数组！

这是最常见的误解。Itanium ABI 的 vtable 结构：

```
vtable for Base (_ZTV4Base):
┌─────────────────────────┐ ← vtable 起始地址
│ offset-to-top (ptrdiff_t)│  8 字节：从当前子对象到完整对象的偏移
├─────────────────────────┤
│ typeinfo pointer         │  8 字节：指向 type_info 对象（RTTI）
├─────────────────────────┤ ← vptr 指向这里！（vptr[-2]=offset, vptr[-1]=typeinfo）
│ virtual function #0      │  8 字节：第一个虚函数地址
├─────────────────────────┤
│ virtual function #1      │  8 字节：第二个虚函数地址
├─────────────────────────┤
│ ...                      │
└─────────────────────────┘
```

### 2. 三个关键字段

| 字段 | 类型 | 用途 |
|---|---|---|
| **offset-to-top** | `ptrdiff_t` | 从当前子对象到完整对象的偏移。用于 `dynamic_cast<void*>` 和虚基类调整。主 vtable 中为 0，次 vtable 中为负数。 |
| **typeinfo pointer** | `type_info*` | 指向该类的 `type_info` 对象，用于 RTTI（`typeid`、`dynamic_cast`）。同一个类的所有 vtable 必须指向同一个 type_info。 |
| **虚函数指针** | `void(*)()` | 按声明顺序排列的虚函数地址。派生类重写的函数覆盖对应槽位。 |

### 3. vptr 指向哪里？

- vptr **不指向 vtable 开头**，而是指向**第一个虚函数指针**
- 所以 `vptr[-2]` 是 offset-to-top，`vptr[-1]` 是 typeinfo pointer
- 这是为了让虚函数调用更快（直接 `vptr[slot]`，不需要偏移）

### 4. 虚函数调用的汇编

```cpp
obj->draw();
// 编译为（x86-64）：
mov   rax, [rdi]        ; 加载 vptr（rdi = this）
call  [rax + 0x10]      ; vptr[2] = draw()（跳过 offset-to-top 和 typeinfo）
```

- **两次间接跳转**：加载 vptr → 索引 vtable → 跳转
- 比非虚函数多一次内存访问和一次间接跳转

- **来源**：Itanium C++ ABI 1.75 + peter0x44 vtable 详解 + Dr-Sergey Itanium ABI + LLVM Relative VTables
- **可信度**：S

---

## 三、单继承布局

### 1. 基本布局

```cpp
class Base {
public:
    virtual void f();
    virtual void g();
    int x;
};

class Derived : public Base {
public:
    void g() override;  // 重写
    virtual void h();   // 新增
    int y;
};
```

```
Derived 对象布局（64位）：
┌──────────┐ offset 0
│ vptr     │ → vtable for Derived
├──────────┤ offset 8
│ x (Base) │
├──────────┤ offset 12
│ padding  │ (4 字节对齐)
├──────────┤ offset 16
│ y        │
└──────────┘ = 24 字节

vtable for Derived:
┌───────────────┐
│ offset-to-top=0│
├───────────────┤
│ typeinfo=Derived│
├───────────────┤
│ Base::f()      │ ← 未重写，继承
├───────────────┤
│ Derived::g()   │ ← 重写，覆盖
├───────────────┤
│ Derived::h()   │ ← 新增，追加
└───────────────┘
```

### 2. 关键规则

- 主基类（primary base）的 vptr 在 offset 0
- 派生类数据成员在基类之后
- 重写的虚函数覆盖 vtable 对应槽位
- 新增的虚函数追加到主 vtable 末尾

- **来源**：NDX GCC 逆向训练 + cppcheatsheet polymorphism + ahmadsarraj vptr 布局
- **可信度**：S

---

## 四、多继承布局与 Thunk

### 1. 多继承的对象布局

```cpp
class A { virtual void fa(); int a; };
class B { virtual void fb(); int b; };
class C : public A, public B {
    void fb() override;
    int c;
};
```

```
C 对象布局（64位）：
┌──────────┐ offset 0
│ vptr_A   │ → primary vtable（A-in-C）
├──────────┤ offset 8
│ a (A)    │
├──────────┤ offset 12
│ padding  │
├──────────┤ offset 16
│ vptr_B   │ → secondary vtable（B-in-C）
├──────────┤ offset 24
│ b (B)    │
├──────────┤ offset 28
│ padding  │
├──────────┤ offset 32
│ c        │
└──────────┘ = 40 字节
```

- 每个多态基类有自己的 vptr 和子对象
- 主基类 A 的 vptr 在 offset 0
- 次基类 B 的子对象在 offset 16
- 次基类有自己的 secondary vtable

### 2. Thunk：this 指针调整

问题：通过 `B*` 指针调用 `fb()` 时，`this` 指向 B 子对象（offset 16），但 `C::fb()` 需要 `this` 指向完整 C 对象（offset 0）。

**解决方案：Thunk**

编译器生成一小段桩代码：

```asm
thunk_C_fb_from_B:
    sub rdi, 16        ; this -= 16（从 B 子对象调整到 C 完整对象）
    jmp C::fb          ; 跳转到真正的函数
```

- secondary vtable 中 `fb` 的槽位指向这个 thunk，而不是直接指向 `C::fb`
- thunk 只做两件事：调整 this + 跳转
- 开销：几条额外指令，不可见于源码

### 3. 虚继承中的更复杂 Thunk

- **vcall offset**：虚函数调用时，从 vtable 读取偏移量再调整 this
- **virtual thunk**：虚继承中重写虚函数时的 thunk
- 比普通多继承多一次内存加载（读 vcall offset）

- **来源**：juejin 内存布局 + subhashjha vtable tour + mg-04 thunk + jiaxw32 vcall offset
- **可信度**：S

---

## 五、虚继承与菱形问题

### 1. 菱形问题

```cpp
class A { int a; };
class B : virtual public A { int b; };
class C : virtual public A { int c; };
class D : public B, public C { int d; };
```

- 没有虚继承：D 中有两份 A（B 的 A 和 C 的 A）→ 歧义
- 有虚继承：D 中只有一份 A → 解决菱形问题

### 2. 虚继承的对象布局

```
D 对象布局（简化，64位）：
┌──────────┐ offset 0
│ vptr_B   │ → B-in-D vtable（含 vbtable 指针）
├──────────┤ offset 8
│ b        │
├──────────┤ offset 16
│ vptr_C   │ → C-in-D vtable
├──────────┤ offset 24
│ c        │
├──────────┤ offset 28
│ padding  │
├──────────┤ offset 32
│ d        │
├──────────┤ offset 36
│ padding  │
├──────────┤ offset 40
│ a (A)    │ ← 虚基类，只有一份！
└──────────┘ = 48 字节
```

### 3. vbtable（Virtual Base Table）

- 虚基类的位置是**动态的**（不同派生类中偏移不同）
- 编译器在 vtable 中存储 **vbase offset**（虚基类偏移表）
- 访问虚基类成员需要：读 vbtable → 获取偏移 → 计算地址

```cpp
d.a;  // 访问虚基类 A 的成员
// 编译为：
mov   rax, [rdi]        ; 加载 vptr
mov   rax, [rax - 24]   ; 从 vbtable 读取 A 的偏移（假设偏移在 vtable[-3]）
add   rax, rdi          ; 计算 A 子对象地址
mov   eax, [rax]        ; 读取 a
```

- 比普通成员访问多 2-3 条指令
- 这就是虚继承有运行时开销的原因

### 4. 构造顺序

- 虚基类**最先构造**（不管在继承列表中的位置）
- 然后按声明顺序构造非虚基类
- 最后构造派生类自己
- 析构顺序相反

- **来源**：PVS-Studio 对齐 Part 3 + Itanium ABI vbase offset + NDX 多继承
- **可信度**：S

---

## 六、RTTI（Run-Time Type Information）

### 1. type_info 对象

每个多态类有一个 `type_info` 对象（由编译器生成）：

```cpp
// libstdc++ 中的实现（简化）
class type_info {
    const char* __name;           // mangled name（如 "NSt6vectorIiEE"）
    // 内部还有 vtable，用于 dynamic_cast 的继承图遍历
};
```

- `typeid(x)` 返回 `const type_info&`
- `type_info::name()` 返回 mangled name（用 `c++filt` 解码）
- `type_info` 相等性：比较指针（同一个类的 type_info 对象地址相同）

### 2. type_info 的继承层次（libstdc++）

| 类型 | 用途 |
|---|---|
| `__class_type_info` | 无基类的类 |
| `__si_class_type_info` | 单继承（single inheritance） |
| `__vmi_class_type_info` | 多继承（multiple inheritance），含基类列表和标志 |

- `dynamic_cast` 通过遍历这些 type_info 的继承图来判断转型是否合法

### 3. RTTI 的开销

- 每个多态类一个 type_info 对象（~16-32 字节）
- vtable 中多一个 typeinfo 指针（8 字节）
- 可以用 `-fno-rtti` 禁用（但不能用 typeid/dynamic_cast）
- LLVM/Chromium 等项目禁用 RTTI 以减小二进制体积

- **来源**：NDX RTTI dynamic_cast + Itanium ABI typeinfo + cppcheatsheet
- **可信度**：S

---

## 七、dynamic_cast 实现原理

### 1. 三种转型

| 转型类型 | 机制 | 失败处理 |
|---|---|---|
| **向上转型**（派生→基类） | 静态偏移调整（编译期确定） | 不会失败 |
| **向下转型**（基类→派生） | 运行时检查 type_info 继承图 | 指针→nullptr，引用→bad_cast |
| **交叉转型**（基类A→基类B） | 运行时遍历完整对象的继承图 | 同上 |
| **转型到 void*** | 读 vtable 的 offset-to-top | 不会失败 |

### 2. dynamic_cast 的算法

1. 从 vptr 获取 type_info
2. 遍历 type_info 的继承图（单继承直接走，多继承遍历基类列表）
3. 检查目标类型是否在继承图中
4. 如果是，计算 this 指针偏移（可能需要调整）
5. 返回调整后的指针；否则返回 nullptr

### 3. Arthur O'Dwyer 的 "dynamic_cast from scratch"

CppCon 2017 经典演讲，从零实现 dynamic_cast：
- vtable 由 most-derived 对象控制
- vtable 的 schema（槽位布局）由静态类型决定
- vtable 的数据（函数指针）由动态类型决定
- dynamic_cast 需要同时知道 schema 和 data

### 4. 性能

- 向上转型：0 开销（编译期偏移）
- 向下转型：~几十条指令（遍历继承图）
- 交叉转型：更慢（可能需要遍历整个继承图）
- 虚继承的 dynamic_cast：最慢（需要读 vbtable）

- **来源**：Arthur O'Dwyer CppCon 2017 + FI MU PV264 + NDX RTTI + mg-04 dynamic_cast
- **可信度**：S

---

## 八、空基类优化（EBCO）

### 1. 原理

```cpp
class Empty {};  // sizeof(Empty) = 1

class Derived : public Empty {
    int x;
};
// sizeof(Derived) = 4，不是 5！
// Empty 基类子对象大小为 0（EBCO）
```

- 标准只要求 **most-derived 对象**非零大小
- **基类子对象**不受此限制，可以大小为 0
- 编译器可以把空基类"压缩"到 0 字节

### 2. 为什么重要？

- `std::tuple` 用递归继承 + EBCO 实现零开销存储
- 无状态分配器（如 `std::allocator`）作为基类不占空间
- 策略模式（policy-based design）的零开销基础

### 3. C++20 的 [[no_unique_address]]

```cpp
struct Config {
    [[no_unique_address]] Allocator alloc;  // 空分配器不占空间
    int* data;
};
```

- EBCO 只能用于基类，`[[no_unique_address]]` 可以用于成员
- MSVC 历史上 EBCO 支持有限，`[[no_unique_address]]` 是更通用的解决方案

### 4. 编译器支持差异

| 编译器 | EBCO 支持 |
|---|---|
| GCC/Clang | 完整支持 |
| MSVC | 历史上有限，VS2017 后改善 |

- **来源**：Microsoft Learn empty_bases + DevTut object layout + PVS-Studio 对齐
- **可信度**：S

---

## 九、对象大小计算

### 1. 计算公式

```
对象大小 = 数据成员总和 + padding + vptr（每个多态基类一个）+ 虚基类表指针
```

### 2. 对齐规则

- 每个成员按自身大小对齐（int→4 字节，double→8 字节）
- 整个对象按最大成员对齐
- vptr 要求 8 字节对齐（64位）

### 3. 经典示例

```cpp
class A { char c; int i; };
// 布局：[c(1)] [pad(3)] [i(4)] = 8 字节

class B { virtual void f(); char c; };
// 布局：[vptr(8)] [c(1)] [pad(7)] = 16 字节

class C : public A, public B { short s; };
// 布局：[A子对象(8)] [B子对象(16)] [s(2)] [pad(6)] = 32 字节
```

### 4. 减少对象大小的技巧

- 重新排列成员（大的放前面）
- 用 `#pragma pack` 或 `[[gnu::packed]]`（但可能降低性能）
- 用 EBCO / `[[no_unique_address]]`
- 避免不必要的虚函数（vptr 开销）
- 位域（bit-field）

- **来源**：CSDN class 大小 + PVS-Studio 对齐系列 + RDS sizeof
- **可信度**：A

---

## 十、VTT（Virtual Table Table）

### 1. 为什么需要 VTT？

虚继承中，构造函数需要在构造过程中切换 vptr。因为虚基类的位置在构造过程中是变化的（先构造虚基类，此时派生类还没构造）。

### 2. VTT 的结构

- VTT 是一个 vtable 指针数组
- 包含：主 vtable 指针 + 每个需要 VTT 的基类的子 VTT
- 构造函数按顺序使用 VTT 中的指针设置 vptr

### 3. 构造过程

```
D 的构造函数：
1. 用 VTT[0] 设置主 vptr（构造虚基类 A）
2. 用 VTT[1] 设置 B 的 vptr（构造 B）
3. 用 VTT[2] 设置 C 的 vptr（构造 C）
4. 用最终 vtable 设置主 vptr（构造 D 自己）
```

- 这是虚继承比普通继承复杂得多的原因之一
- jinjucat 的 "The Chronicles of VTT" 是最详细的中文资料

- **来源**：jinjucat VTT + Itanium ABI 构造 vtable
- **可信度**：A

---

## 十一、知识网络

```
C++ 对象模型与 ABI
├── 基础
│   ├── 空类 = 1 字节（唯一地址）
│   ├── 非多态对象：数据成员 + padding
│   ├── 多态对象：vptr + 数据成员
│   └── vptr 在 offset 0（Itanium ABI）
│
├── vtable 内部结构
│   ├── offset-to-top（到完整对象的偏移）
│   ├── typeinfo pointer（RTTI）
│   ├── 虚函数指针数组（声明顺序）
│   └── vptr 指向第一个虚函数（vptr[-2]=offset, vptr[-1]=typeinfo）
│
├── 虚函数调用
│   ├── 两次间接跳转：vptr → vtable[slot] → 函数
│   ├── 构造函数设置 vptr
│   └── 比非虚函数多一次内存访问
│
├── 单继承
│   ├── 主基类 vptr 在 offset 0
│   ├── 派生数据在基类之后
│   ├── 重写覆盖 vtable 槽位
│   └── 新增虚函数追加到主 vtable
│
├── 多继承
│   ├── 每个多态基类一个 vptr
│   ├── 主基类 + 次基类子对象
│   ├── secondary vtable
│   └── Thunk：调整 this 指针（sub + jmp）
│
├── 虚继承
│   ├── 菱形问题：虚基类只有一份
│   ├── vbtable：虚基类偏移表（动态偏移）
│   ├── 访问虚基类多 2-3 条指令
│   ├── 虚基类最先构造
│   ├── vcall offset / virtual thunk
│   └── VTT：构造过程中的 vtable 指针表
│
├── RTTI
│   ├── type_info 对象（每个多态类一个）
│   ├── typeid / type_info::name()（mangled name）
│   ├── __class_type_info / __si_class_type_info / __vmi_class_type_info
│   └── -fno-rtti 禁用
│
├── dynamic_cast
│   ├── 向上转型：编译期偏移（0 开销）
│   ├── 向下转型：遍历 type_info 继承图
│   ├── 交叉转型：遍历完整继承图
│   ├── 转型到 void*：读 offset-to-top
│   └── 失败：nullptr / bad_cast
│
├── EBCO（空基类优化）
│   ├── 空基类子对象大小为 0
│   ├── std::tuple 零开销存储的基础
│   ├── C++20 [[no_unique_address]]（成员版本）
│   └── MSVC 历史支持有限
│
└── 对象大小
    ├── 数据成员 + padding + vptr + vbtable
    ├── 对齐规则
    ├── 重排成员减少 padding
    └── 位域 / packed
```

---

## 十二、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | Itanium C++ ABI 1.75（Linux Foundation） | S | vtable/RTTI/对象布局的权威规范 |
| 2 | peter0x44 "How Virtual Tables Work" | S | vtable 内部结构的最清晰讲解 |
| 3 | Dr-Sergey Itanium ABI 布局规则 | S | vtable/RTTI/异常的完整布局 |
| 4 | Arthur O'Dwyer "dynamic_cast from scratch"（CppCon 2017） | S | dynamic_cast 原理的经典演讲 |
| 5 | NDX GCC 逆向训练（object model + RTTI） | A+ | 从二进制逆向理解对象布局 |
| 6 | Itanium C++ ABI GitHub（abi-layout.html） | S | vtable 布局的详细说明 |
| 7 | jinjucat "The Chronicles of VTT" | A | VTT 的最详细中文资料 |
| 8 | PVS-Studio 对齐系列（Part 2/3） | A | vptr/对齐/虚继承对对象大小的影响 |
| 9 | subhashjha "What's inside a C++ object" | A | thunk 和多继承的清晰示例 |
| 10 | LLVM "Relative VTables in C++"（2021） | A | vtable 优化的前沿方向 |

## 十三、强烈建议深入研究的 5 个资料

1. **Itanium C++ ABI 1.75**——对象布局、vtable、RTTI、异常的完整规范，ABI 域的圣经
2. **peter0x44 vtable 详解**——配合汇编示例，理解 vtable 内部结构和虚函数调用
3. **Arthur O'Dwyer dynamic_cast from scratch**——从零实现 dynamic_cast，理解 RTTI 继承图遍历
4. **NDX GCC 逆向训练**——从二进制角度理解对象布局，配 `objdump`/`gdb` 实战
5. **一个真实的多继承+虚继承项目**——用 `pahole` 或 `-fdump-record-layouts` 看实际布局

## 十四、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| vtable 内部结构 | "vtable 不是函数指针数组：offset-to-top 和 typeinfo" | ABI 域原子 |
| 虚函数调用机制 | "一次虚函数调用到底发生了什么" | ABI/LANG 域原子 |
| 多继承与 thunk | "多继承的代价：thunk 和 this 指针调整" | ABI 域原子 |
| 虚继承与 vbtable | "虚继承为什么慢：vbtable 和动态偏移" | ABI 域原子 |
| dynamic_cast 原理 | "dynamic_cast 是怎么工作的" | ABI/LANG 域原子 |
| EBCO | "空基类不占空间：EBCO 与 tuple 的秘密" | TMPL/STL 域原子 |
| 对象大小计算 | "sizeof 一个类到底是多少" | ABI 域专题 |

## 十五、对 CPP-Bible 的工程升级建议

1. **ABI 域新增"对象模型"专题**——vtable/vptr/单继承/多继承/虚继承全链路，配 `-fdump-record-layouts` 实验
2. **ABI 域新增"vtable 内部结构"原子**——offset-to-top/typeinfo/虚函数指针，这是最常见的误解
3. **ABI 域新增"thunk 与 this 调整"原子**——多继承的运行时代价
4. **ABI 域新增"dynamic_cast 原理"原子**——配合 Arthur O'Dwyer 的演讲
5. **TMPL 域新增"EBCO 与零开销抽象"原子**——std::tuple 的实现基础
6. **证据卡新增对象布局实验**——用 `pahole` 或 GCC `-fdump-record-layouts` 展示真实布局，验证 vptr 偏移、padding、thunk
7. **ALIGN-001 原子扩展**——当前 ALIGN-001 只讲对齐/padding，可以补充 vptr 对对齐和大小的影响

## 十六、发现的知识空白

1. **对象模型完全空白**——vtable/vptr/内存布局完全没讲
2. **vtable 内部结构空白**——offset-to-top 和 typeinfo 是最常见的误解
3. **多继承/thunk 空白**——多继承的运行时代价完全没讲
4. **虚继承/vbtable 空白**——虚继承为什么慢完全没讲
5. **RTTI/dynamic_cast 空白**——运行时类型信息的实现原理完全没讲
6. **EBCO 空白**——零开销抽象的基础机制完全没讲
7. **VTT 空白**——虚继承构造过程的复杂机制完全没讲

## 十七、下一轮推荐搜索方向

1. **性能分析与 profiling（按顺序）**——perf、gprof、Valgrind、cachegrind、火焰图、性能优化方法论
2. **数据库存储引擎**——B+树、LSM-tree、WAL、缓冲池、事务、MVCC
3. **网络编程与异步 IO**——epoll/io_uring、Reactor/Proactor、Boost.Asio、零拷贝
4. **调试器原理**——DWARF、ptrace、断点实现、调用栈回溯、GDB 内部
5. **GPU 与异构计算**——CUDA、HIP、SYCL、OpenCL、GPU 内存模型

---

*本轮新增知识节点：C++ 对象模型、vtable、vptr、offset-to-top、typeinfo pointer、虚函数调用、动态分发、单继承、多继承、primary base、secondary base、secondary vtable、thunk、adjustor、this 指针调整、虚继承、菱形问题、diamond problem、vbtable、virtual base table、vbase offset、vcall offset、virtual thunk、VTT、virtual table table、RTTI、type_info、typeid、__class_type_info、__si_class_type_info、__vmi_class_type_info、dynamic_cast、downcast、crosscast、std::bad_cast、EBCO、empty base class optimization、[[no_unique_address]]、对象大小、对齐、padding、most-derived 对象、构造顺序、析构顺序、-fno-rtti、-fdump-record-layouts、pahole。补齐了"ABI 域对象模型"的全部核心空白——这是 ABI 域的第一轮，与 name mangling（22轮）、异常实现（16轮）形成完整的 ABI 知识链。*
