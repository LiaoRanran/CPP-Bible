---
id: ATOM-MEM-UNIQUE-001
title: std::unique_ptr 是唯一所有权智能指针：移动转移、拷贝删除、sizeof 等于裸指针
domain: MEM
type: mechanism
status: draft                 # 唯人可置 verified（S1 三权分立）；Writer 自评最高 4
# ---- 认知适切（G5 新增字段）----
audience: intermediate         # 默认读者：会用裸 new，正在学"该用哪个智能指针"
cognitive_load: medium         # 需同时持有"移动转移所有权"与"拷贝被删"两条线索
prerequisites_readable: true   # 前置 ATOM-MEM-RAII-001 已锻造（relations 目标存在，机器可查）
claim: >-
  std::unique_ptr<T> 是唯一所有权智能指针：移动转移所有权（源被置空、目标获得对象），拷贝构造被删除
  （不可共享），析构恰好 delete 一次（无双释放）。它是零开销抽象——sizeof 等于裸指针（x86-64 下 8 字节），
  所有权语义只体现在编译期（拷贝删除 + 移动转移），不在运行时加字段。禁用裸 new；需要共享才升级到 shared_ptr。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-RAII-001}   # unique_ptr 是"堆指针交给栈对象管"的具体形态
  - {type: contrasts, target: ATOM-MEM-SHARED-001}    # 唯一 vs 共享：拷贝删 vs 引用计数
evidence:
  - EV-MEM-011          # 零开销：sizeof == 裸指针
  - EV-MEM-012          # 移动转移所有权 + 唯一析构 + 拷贝删（编译期证伪）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [unique.ownership]（唯一所有权；拷贝构造/赋值被删除，移动构造/赋值转移）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [unique.single]（析构调用 deleter 释放资源；单对象）", independent: true}
  - {kind: cppreference, ref: "std::unique_ptr（独占所有权的智能指针，零开销）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 描述 unique_ptr 的接口，但没把"为什么它是默认选择"讲成可证伪的三点。本原子多给：
  ① sizeof==裸指针的运行期证据（零开销不是口号）；② 移动转移的"双重观测"（源置空 + 析构恰好一次），
  而非只看一半；③ 拷贝删除用**真实编译错误文本**坐实（满足"注释断言须有实证"），把"唯一所有权"
  从约定变成编译期铁律。与 RAII-001 分工：它讲"为什么用栈对象管资源"，本原子讲"具体用 unique_ptr 时
  所有权怎么流动"；与 SHARED-001 分工：本原子是"唯一"基准，SHARED-001 是"需要共享时为什么换 shared_ptr"。
depth:
  layer: compiler
  drill_note: >-
    零开销由 sizeof（编译期）证明；移动转移由源置空 + 唯一析构（运行期 volatile 计数）证明；拷贝删除
    由 [unique.ownership] 编译错误证明。三者对应"零开销 / 转移 / 唯一"三性质，互相支撑。
pedagogy:
  motivation: 既然有 new/delete 和 shared_ptr，为什么默认用 unique_ptr？
  misconceptions: [MIS-MEM-009]   # 全局误解库：裸资源管理 / 忘记释放
  socratic:
    - "unique_ptr 比裸指针大吗？多出来的字段存了什么？"
    - "std::unique_ptr<Box> b = a; 能编译吗？为什么？"
    - "移动后 a 还指向原来的对象吗？"
  predict_first: 下面移动后，`a == nullptr` 是真还是假？析构会被调用几次？先预测，再看 EV-MEM-012。
---

## 论断

**默认用 `std::unique_ptr` 管理独占资源：它把"堆指针"包成一个栈对象，移动转移所有权、拷贝被删、
析构自动 delete，且零开销。**

| 性质 | 表现 | 证据 |
|---|---|---|
| 零开销 | `sizeof(unique_ptr<T>) == sizeof(T*)`（8 字节） | `EV-MEM-011` |
| 移动转移 | 移动后源置空、目标获对象 | `EV-MEM-012` |
| 唯一所有 | 拷贝被删、析构恰好一次（无双释放） | `EV-MEM-012` |

## 为什么（三条性质互相支撑）

- **零开销**：unique_ptr 内部只有一个指针成员，没有 vtable、没有计数器。所有权信息在**编译期**——
  拷贝删除 + 移动转移是类型层面的约束，不占运行时空间（`EV-MEM-011`：8 == 8）。
- **移动转移**：`b = std::move(a)` 后，`a` 被置空、`b` 持有对象。这与 PERF-001 的"移动只偷指针"完全一致。
- **唯一所有**：拷贝构造被删除（`[unique.ownership]`），所以不可能出现"两个 unique_ptr 指向同一对象"
  的歧义——析构必然只一次，不会双释放（`EV-MEM-012`：destroyed count=1）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若移动后 `a` 仍持有对象（empty=0），则"移动转移所有权"被推翻 → `EV-MEM-012` refute。
- **证伪条件 B**：若析构计数 != 1，则"唯一所有权"被推翻 → `EV-MEM-012` refute。
- **证伪条件 C（编译期）**：若 `std::unique_ptr<Box> c = a;` 能编译，则"唯一所有权"名存实亡 → 实测
  报错 `error: use of deleted function 'std::unique_ptr<...>::unique_ptr(const std::unique_ptr<...>&)'`。
- 实测 A/B 运行成立、C 编译成立 ⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用

- **禁裸 new**：`std::unique_ptr<T> p = std::make_unique<T>(args);`（用 `make_unique` 避免裸 `new`）。
- **传参**：需要"拿走"用 `std::unique_ptr<T>&&` 或返回值；需要"借用"用 `T&` 或 `const T&`。
- **需要共享才升级**：当一个资源被多个所有者共享时，才换 `std::shared_ptr`（见 `ATOM-MEM-SHARED-001`）——
  不要默认用 shared_ptr，那会白付引用计数开销。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-009]`（裸资源管理靠"记得释放"）：本原子给出替代——把裸指针塞进 unique_ptr，
让析构（不是人）负责 delete，且零开销、移动转移、拷贝删三重保险。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全；三点（零开销/转移/唯一）互证。留待人审一点：未跑 `-O0` 双验（sizeof 与移动转移均优化无关，
  已在卡内注明；可在原子化前补 -O0 同输出留痕）。 |

### 4 分锚定依据
1. **零开销有运行期证据**：sizeof==8==裸指针，不是"标准说零开销"的转述。
2. **转移有双重观测**：源置空 + 唯一析构，合起来才是"唯一所有权"完整证明。
3. **拷贝删有真实编译错误**：注释断言配实证文本，满足"注释里的机制断言必须有代码实证"。

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S1 注释无实证**：初版只写"拷贝被删"无证据 → 实编临时夹具捕获真实错误
    `error: use of deleted function 'std::unique_ptr<...>::unique_ptr(const std::unique_ptr<...>&)'`，写入卡内。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：明写"需要共享才升级 shared_ptr"
  的迁移判据，已补进 "这条原则怎么用"）。
