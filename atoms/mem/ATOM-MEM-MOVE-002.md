---
id: ATOM-MEM-MOVE-002
title: 用 std::move 申报所有权转移，真正的搬运发生在移动构造里
domain: MEM
type: mechanism
status: draft                  # draft|verified|rejected（**唯人可置 verified**：见下方"签收"）
claim: >-
  std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；
  移动构造的收益来自**掏空源对象**，因此源对象没有可掏空的间接资源时，移动退化为拷贝。
claim_boundary:
  standard: [C++11, C++17, C++20, C++23]
  compilers: [GCC 15.3.0, GCC 13.1.0, GCC 8.1.0, GCC 13.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64, x86-64 Linux]
relations:
  # G5 迁移时建立实体：本原子是本轮唯一入库原子，目标原子尚未锻造，先只登记意图（不写 target）。
  # 待 ATOM-MEM-VALUE-* / ATOM-MEM-PERF-* 入库后，用 id_migrations.json 补齐边并重跑门禁。
  - {type: prerequisite, target: ATOM-MEM-VALUE-001}
  - {type: misconceived_as, target: ATOM-MEM-PERF-001}
evidence:
  - EV-MEM-001
  - EV-MEM-002
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [xvalue.cast]（std::move 与 static_cast 明文等价）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [lib.types.movedfrom]（移动后源对象有效但未指定）", independent: true}
  - {kind: cppreference, ref: "std::move", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 只给出两条**分离**的事实（"move 是类型转换"与"源对象有效但未指定"），
  读者拿在手里仍不知道"什么时候移动真有用"。本原子把两者接起来给出统一解释——**收益来自掏空
  源对象**——并用可编译对照实验在运行层（分配计数）与汇编层（字节搬运量）双向验证；
  同时给出"不该用"的三条判据（纯值类型 / const 源 / return 语句），这是现有资料普遍缺失的部分。
depth:
  layer: asm
  drill_note: >-
    移动的"省"与"不省"在汇编层可分辨——HeapBuf 的移动只搬 8 字节指针并把源置空；
    FixedBuf<8> 的移动必须搬 32 字节且源分毫未动（EV-MEM-002 的 movaps 断面：`@L136`/`@L143`）。
pedagogy:
  motivation: 为什么标准要给一个"不搬东西"的函数起名叫 move？
  misconception:
    - level: surface
      text: "std::move 会移动对象"
    - level: surface
      text: "移动之后源对象变成空的，可以当空对象继续用"
    - level: deep
      text: "移动一定比拷贝快，所以到处加 std::move 准没错"
      refutations: [EV-MEM-001, EV-MEM-002]
  socratic:
    - "如果 std::move 只是类型转换，那么真正决定'省不省'的是什么？"
    - "std::array<int, 1000> 的移动和拷贝，在机器码上有什么区别？"
  predict_first: 移动一个 std::array<int, 8> 之后，源数组里的元素会变成什么？（先预测，再看 EV-MEM-002）
---

## 论断

**用 `std::move` 申报所有权转移，别指望它自己搬东西。**

`std::move` 是 C++ 里最容易读错的命名之一：它被调用之后并没有任何东西被搬走。标准明文规定
它与一次类型转换完全等价（[xvalue.cast]）：

```cpp
// 标准 [xvalue.cast] 的等价关系（可编译互证）
std::move(x)  ≡  static_cast<std::remove_reference_t<decltype(x)>&&>(x)
```

既然只是类型转换，为什么需要这个名字？因为在**重载解析**里"是不是右值"决定了调用哪个构造函数：
`std::move` 的职责不是搬运，而是**申报意图**，把选择权交给重载解析。

一次 `T b = std::move(a);` 实际发生三件事，只有第三件与"搬"有关：

1. `std::move(a)` 把左值 `a` 变成 **xvalue**（不产生机器码，纯编译期动作）；
2. 重载解析选中 `T(T&&)`（移动构造）而不是 `T(const T&)`（拷贝构造）；
3. **移动构造自己决定做什么**——对持有堆指针的类型是"偷指针并把源置空"；对没有间接资源的
   类型，它只能逐元素搬字节，与拷贝构造生成的代码相同。

所以"移动有多快"不取决于 `std::move`，取决于**被移动类型有没有可以掏空的间接资源**。

## 证据

两个独立证据层，缺一不可：

| 层 | 证据 | 观测 |
|---|---|---|
| 运行层 | `EV-MEM-001`（6 组矩阵 + 证伪对照） | 构造 1 次分配 / 拷贝 1 次 / **移动 0 次**；假移动对照 1 次 |
| 汇编层 | `Examples/_atom_move_alloc.asm` | `main` 内 `call malloc` 恰 3 次（`@L109` `@L117` `@L144`），移动路径 0 次 |
| 汇编层 | `Examples/_atom_move_no_gain.asm` | `call malloc` 仅 1 次（`@L117`，HeapBuf 的拷贝）；纯值组走 `pshufd` + `movaps XMMWORD PTR`（`@L136` `@L143`）= **32 字节搬运** |

两层的意义不同：运行层证明"移动确实没分配"，汇编层证明"移动**做了什么**"——这正是把
"移动更快"这种模糊说法换成可检验机制的抓手。

`EV-MEM-002` 另有一处必须留痕的方法论：它的**第一版是零观测伪证据**——纯值组的内容写成编译期
常量后，`-O2` 把该组的构造、移动、读回整体消除（`main` 段无任何搬运指令），而输出照样打印
"移动分配=0 移动后源完好=是"，**数字完美符合预期却不是观测来的**。发现方式是看汇编断面而非看
输出；修法是初值由 `argc` 派生 + `volatile` 指针读回。教训：**凡"证明某件事没有发生"的实验，
必须同时证明观测通路是活的。**

## 反例（证伪导向：让它失败的实验）

**反例一：纯值类型没有收益。** `EV-MEM-002` 在 `-O0` 与 `-O2` 两档实测（输出逐字一致）：

```text
HeapBuf  拷贝分配=1 移动分配=0 移动后源被掏空=是     ← 有间接资源：移动 = 偷指针
FixedBuf 拷贝分配=0 移动分配=0 移动后源完好=是       ← 纯值成员：移动 = 搬字节，源不动
array    拷贝分配=0 移动分配=0 移动后源完好=是       ← 标准库纯值类型：同上
```

`std::array<int, 8>` 的移动在汇编里是 32 字节 SIMD 搬运（`movaps`），而源数组一个字节都没变——
**移动的全部收益来自"掏空源对象"；没有可掏空的东西时，移动就是拷贝。**

**反例二：把"移动"实现成假移动**（`BadBuf`：移动构造里又 `new` 一次，见 `EV-MEM-001`）产出的分配
计数是 1——若对照也输出 0，说明计数没接上，整个实验作废。这条对照是"实验有分辨力"的证明。

**证伪条件**：若纯值组显示"源被掏空"，则统一解释被推翻，本原子应改写。

## 学习者常见误解

1. **「`std::move` 会移动对象」**（surface）——它只是类型转换；是否搬运由被调用的移动构造决定。
2. **「移动后源对象变成空的，可以当空对象继续用」**（surface）——标准只保证"有效但未指定"，
   且这个措辞要按三分法使用：
   - ✅ 可以：析构它、给它赋新值、`clear()` 后重新使用；
   - ❌ 不可以：读它的值、依赖它"是空的"、把它当空容器用。
3. **「移动一定比拷贝快，到处加 `std::move` 准没错」**（deep，反例：`EV-MEM-001` + `EV-MEM-002`）
   —— 收益来自掏空源对象，故三类场景**不该用**：
   - 纯值类型（`int`、`std::pair<int,int>`、`std::array`）——没有收益，只是更难读；
   - `std::move(const T& src)` —— 得到 `const T&&`，移动构造需要 `T&&`，**静默退化为拷贝**；
   - `return std::move(local);` —— 移动构造虽被选中，但**阻止了 NRVO**（[class.copy.elision]），
     结果比不写更慢。

## 签收（S1：声明的"verified"必须由人签）

- 人审记录（四步流程：平庸版 → 红队 → 5 分候选 → 人审）：`goldens/A_move.md`（监工质检报告
  2026-09-10：五重剖面 5/5、证据双 confirm、汇编行号硬校验通过、建议授予 5 分）。
- 本原子当前为 `draft`：**`verified` 须由人签署**（`verified_by: human:*`），Agent 不自置。
