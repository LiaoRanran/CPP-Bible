# 台阶一 P1 · 内存/对象模型实证结论清单（施工图）

> 版本：2026-08-30 · 关联 `_asm_demo/INDEX.md`（53 例真机实证看板）与 `CONTENT_DEPTH_ROADMAP.md` §1
> 定位：**强模型定结论，弱模型照此产证。** 每条结论须真机 objdump 验证（GCC 15.3.0），不手绘、不伪造。
> 口径：✅ 已有真机实证（`_asm_demo/*.cpp/.s`）｜🟡 正文有片段/数据但未锚定到证据文件｜❌ 缺口（有文字无 objdump 证据）

---

## 0. 一句话结论

P1（内存/对象模型）**不是白纸**：53 例精品实证里，对象模型主题已覆盖大半（虚调用、RTTI、EBO、SSO、shared_ptr 计数、虚继承 thunk、optional/variant/any/function 布局、全部 STL 容器内存模型均已真机实证）。真正的缺口是**四个核心结论**——它们"文字讲了、真机证据缺"，且都是对象模型里最能揭示底层真相的点。

---

## 1. 结论图谱（六大类 · 27 条）

### A. 虚函数与虚表（vptr / vtable）
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| A1 | 对象头部 vptr 指向虚表；虚调用 = `mov vptr; jmp [vtable]` 间接跳转 | ✅ | ASM-47-vs-51 |
| A2 | 单继承 1 个 vptr；vtable 按声明序排列；调用点 `call [vtable+off]` | 🟡 | ch47 章内片段 |
| A3 | **多继承多个 vptr、基类子对象顺序、非虚 MI 的 this 调整 thunk** | ❌ | —（缺口） |
| A4 | 虚继承 vbptr + 运行时查 vbtable 调整 this（比非虚 thunk 更贵） | ✅ | ASM-50-vi |
| A5 | RTTI：type_info 挂在 vtable `-1` 槽；dynamic_cast 沿继承链遍历 | ✅ | ASM-48-rtti |
| A6 | **虚析构 deleting destructor（`_ZdlPv` 调整删除，完成析构链）** | ❌ | —（缺口） |

### B. 对象布局与对齐
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| B1 | 字段对齐/padding/sizeof 与标准布局/平凡类型 | 🟡 | ch45（概念，无专门 asm） |
| B2 | EBO 空基类优化：空基类占 0 字节、子类不膨胀 | ✅ | ASM-52-ebo |

### C. 智能指针与控制块
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| C1 | unique_ptr 零开销（析构/解引用与裸指针等价） | 🟡 | ch41 章内片段 |
| C2 | shared_ptr 控制块原子计数：拷贝 = 16B memcpy + `lock add [rdx+8]` | ✅ | ASM-41-shared_ptr |
| C3 | **make_shared 单次分配 vs `shared_ptr(new)` 两次分配** | ❌ | —（缺口） |
| C4 | **enable_shared_from_this：控制块内嵌 weak_this 的初始化时机** | ❌ | —（缺口） |

### D. 移动语义与拷贝省略
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| D1 | 移动 = 指针浅拷，零深拷贝 | ✅ | ASM-115-move |
| D2 | NRVO/RVO 消除拷贝构造；多返回路径 NRVO 失效 | ✅ | ASM-117-elision / ASM-117-nrvo |

### E. 词汇类型存储布局（全真机实证）
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| E1 | optional：值 + `engaged` 标志，空间真实膨胀 | ✅ | ASM-88-optional |
| E2 | variant + visit：tag 字节分支链，≈ 手写 switch | ✅ | ASM-88-variant |
| E3 | string SSO：短串栈内缓冲免堆分配 | ✅ | ASM-81-sso |
| E4 | string_view：`{len@0,ptr@8}` 16B、O(1) substr | ✅ | ASM-81-string_view |
| E5 | span：裸 `ptr+len` 逐字节同码、无边界检查 | ✅ | ASM-82-span |
| E6 | tuple：递归继承致末参在最底地址 | ✅ | ASM-89-tuple |
| E7 | any：≤16B SBO 内联零堆 | ✅ | ASM-89-any |
| E8 | function：invoker 指针 + 小对象优化 | ✅ | ASM-std_function |

### F. 容器内存模型（全真机实证）
| # | 结论 | 现状 | 证据 |
|---|---|---|---|
| F1 | vector 扩容三连（new+memcpy+delete） | ✅ | ASM-77-vector_grow |
| F2 | deque 分块映射双间接 | ✅ | ASM-78-deque |
| F3 | list/forward_list 节点堆分配 + 指针追逐 | ✅ | ASM-79 / ASM-79-fwdlist |
| F4 | map/set 红黑树节点 + 指针追逐 | ✅ | ASM-83 / ASM-84 |
| F5 | unordered 桶链表 + hash 取桶 | ✅ | ASM-85 / ASM-85-uset |

**汇总**：27 条结论，✅ 19 条真机实证、🟡 4 条章内片段未锚定、❌ **4 条缺口**。

---

## 2. 四个优先缺口（弱模型下一批施工目标）

> 每条给出"要揭示的底层事实 + 验证方法"，弱模型照此写 `_asm_demo/*.cpp`、跑 objdump、归档 `.cpp/.s`，再更新 `_asm_demo/INDEX.md` 与 STATE 计数。

### ❌ P1-GAP-1：make_shared 单次分配（最优先，冲击力最强）
- **底层事实**：`make_shared<T>` 把对象和控制块分配在**同一块内存**（单次 `operator new`）；`shared_ptr<T>(new T)` 是**两次**分配（对象 + 控制块各一次）。后果：make_shared 少一次堆分配、缓存更友好，但对象内存无法单独释放（weak_ptr 存活时整块不析构）。
- **验证**：两个函数各编译，`objdump` 对比 `operator new` 调用次数与分配大小（make_shared 单次 `new(sizeof(T)+控制块)` vs 两次）；再验证 weak_ptr 存活时对象不析构。
- **落章**：ch41（shared_ptr 章）附录小节。

### ❌ P1-GAP-2：多继承对象布局（对象模型核心）
- **底层事实**：多继承下对象有**多个 vptr**（每个多态基类一个）；基类子对象按声明序排列；调用"第二个基类"的虚函数时，GCC 生成**非虚 thunk**（固定 `sub rdi,0x10` 调整 this 到该基类子对象）。
- **验证**：定义 `struct D : B1, B2`（两基类均有虚函数），打印对象布局（`offsetof`/地址差）+ `objdump` 看 thunk 的 this 调整量与固定偏移。
- **落章**：ch50（multiple_inheritance）附录；与已有 ASM-50-vi（虚继承运行时 thunk）形成"非虚固定 thunk vs 虚继承运行时查表"对照。

### ❌ P1-GAP-3：enable_shared_from_this（控制块机制）
- **底层事实**：继承了 `enable_shared_from_this<T>` 的类，其布局里嵌入 `weak_ptr<T>`（weak_this）；首次构造 `shared_ptr` 时，通过 `_M_assign(shared_ptr, nullptr)` 初始化 weak_this，之后 `shared_from_this()` 才能用。关键陷阱：**构造 shared_ptr 之前调用 shared_from_this 是 UB**（weak_this 未初始化）。
- **验证**：sizeof(含 enable_shared_from_this 的类) 与不含的对比（多出 weak_ptr 16B）；objdump 看 weak_this 初始化时机与 `shared_from_this` 走 weak.lock() + throw。
- **落章**：ch41（shared_ptr 章）附录。

### ❌ P1-GAP-4：虚析构 deleting destructor（析构链）
- **底层事实**：有虚析构的类，vtable 里有三个相关槽（complete / deleting 析构）。deleting destructor 负责"析构 + `operator delete`"；`delete 基类指针` 时经虚表间接调用**完整的派生析构链**。
- **验证**：`delete Base*` 指向派生对象，objdump 看经 vtable 间接跳转到派生 deleting destructor；对比无虚析构时直接 `call` 派生析构 + `operator delete` 的差异。
- **落章**：ch47（virtual_functions）或 ch40（exception_safety）析构小节。

---

## 3. 弱模型施工约定

1. 源文件命名 `_asm_demo/chNN_<机制>_test.cpp`，`.cpp` + `.s` 一并归档（`.o`/`.exe` 不入库）。
2. 编译：`g++ -std=c++26 -O2 -c` 编 `.o`，再 `objdump -d -M intel -C` 提取（工具链 `C:/Qt/Tools/mingw1530_64/bin/`）。
3. 结论写进对应章"附录"小节（不扩写正文），并更新 `_asm_demo/INDEX.md` 表 + STATE.json `assembly_empirical_examples` 计数。
4. 红线校验：`tools/consistency_check.py` 0/0；实证必须真机，不手绘。

---

_本清单由强模型定结论；弱模型照表产证后再回填，形成"结论清单 → 真机证据 → 看板锚定"闭环。_