---
id: ATOM-UB-GRAY-001
title: 先分清副作用是 unsequenced 还是 indeterminately sequenced：前者是 UB，后者只是未指定
domain: UB
type: contrast
gray_zone: ub                  # 五类单值归属（M2 §7）：本原子域在 UB 侧、主体是"识别真 UB"
                               # （正文以"unspecified vs UB"对照展开，对照的另一侧见 claim）
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-10        # 签署日期（第 2 轮人审通过）
dal: A                            # 失效后果分级（G6 §3）：A=UB/并发致程序崩溃或数据错误；须人审
human_review: required            # DAL A/B ⟹ 强制人审（G6）
status_history:                   # 四级晋升链（G6 §2），链尾须等于 status
  - {level: draft, at: legacy, by: writer:agent}
  - {level: machine-verified, at: 2026-09-10, by: machine:gate}
  - {level: human-verified, at: 2026-09-10, by: human:liaoranran}
# ---- 认知适切（G5 新增字段）----
audience: intermediate         # 默认读者：写过 C++ 但没系统区分过 unspecified / UB 的进阶者
cognitive_load: high           # 需同时持有"测序关系 / 版本边界 / 优化器利用"三条线索
prerequisites_readable: false  # 前置 ATOM-UB-DEF-001 尚未锻造（relations 已登记意图）
claim: >-
  `f(g(), h())` 的实参求值顺序是**未指定**（unspecified）：两种顺序都合法、程序不会崩，但不可依赖；
  **未测序（unsequenced）的同一标量修改**（如 `i = i++ + ++i`）与**通过不兼容类型指针访问对象**
  （严格别名）属于**未定义行为**，标准不再要求任何行为，优化器可据此删除你的访问。
  （版本边界：函数实参 `f(i++, i++)` 自 **C++17 起是 _indeterminately sequenced_** → **unspecified**；
  C++11/14 下才是 UB。）
claim_boundary:
  standard: [C++11, C++14, C++17, C++23]
  compilers: [GCC 15.3.0, GCC 13.1.0, GCC 8.1.0, Clang (CI ubuntu-latest runner 默认)]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64, x86-64 Linux]
relations:
  - {type: contrasts, target: ATOM-UB-ALIAS-001}    # 与"严格别名"原子对照（G5 迁移时建实体）
  - {type: prerequisite, target: ATOM-UB-DEF-001}   # 前置：未定义行为的定义（G5 迁移时建实体）
evidence:
  - EV-UB-001
  - EV-UB-002
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.call]（函数参数初始化是 indeterminately sequenced）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.execution]（未测序的标量修改为 UB；indeterminately sequenced 定义为不重叠）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.lval]（严格别名：访问对象的 glvalue 类型受限）", independent: true}
  - {kind: cppreference, ref: "Undefined behavior / Order of evaluation", independent: true}
first_hand: true
superiority: >-
  现有资料通常把两类分两页讲（"求值顺序"一页、"严格别名"一页），读者拿不到**统一判据**，
  于是把 unspecified 当 UB 恐慌（本书灰色地带实测：1478 个候选句里 74.4% 被判 UB、仅 6.3% 判
  unspecified，量级差 12 倍——"未定义"被泛用是**可测量的**），或把 UB 当"偏门技巧"照用。
  本原子给出**可操作判据**（*unsequenced* 可重叠 → UB；*indeterminately sequenced* 不重叠 →
  unspecified），并给出**版本边界**（C++17 把实参初始化从前者改为后者 ⇒ `f(i++, i++)` 由 UB 变
  unspecified，而 `i = i++ + ++i` 始终是 UB），用同一份可编译夹具把两类并排对照：
  unspecified 侧 **GCC 六组一致、Clang 相反**（教"顺序不是标准规定的"），UB 侧用
  `-fno-strict-aliasing` 把"优化器利用了 UB"直接翻出来（教"能跑 ≠ 合法"）。
depth:
  layer: asm
  drill_note: >-
    UB 被利用与否在汇编层可见：`alias_kill`（`_atom_strict_alias.asm` `@L8–L14`）里返回值
    `mov eax, 1` 排在两次写之前、且函数体内**没有**对 `[rcx]` 的二次读取——优化器已假定两个
    不同类型的指针不指向同一对象。求值顺序侧则看 `main` 内三次 `call __mingw_printf` 的出现
    顺序（`@L70`/`@L72`/`@L76`），它是实现的选择、不保证。
pedagogy:
  motivation: 为什么标准要区分"未指定"和"未定义"？合起来叫"不确定"不就完了？
  # G5：误解统一引用全局库（level 与反例以库为准，见 misconceptions/README.md）
  misconceptions: [MIS-UB-014, MIS-UB-013, MIS-UB-015, MIS-UB-001]
  socratic:
    - "同一段代码在 GCC 8.1 到 15.3 上跑了一致结果——这能证明标准规定了顺序吗？"
    - "如果标准说'未定义'，编译器能不能假设这段代码永远不会执行？"
  predict_first: 把 `-O2` 换成 `-O2 -fno-strict-aliasing`，`alias_kill` 的返回值会变吗？（先预测，再看 EV-UB-002）
---

## 论断

**先分清副作用是 unsequenced 还是 indeterminately sequenced：前者是 UB，后者只是未指定。**

"未定义行为"这个词在中文技术写作里被泛用得很厉害——本书自测就量到了这个偏差：全书 1478 个
灰色地带候选句里，**74.4% 被判为 UB，只有 6.3% 判为 unspecified**（相差 12 倍，
`tools/gray_zone_scan.py` 实测）。而被抓到的真实误用长这样：

> `std::sort` 的比较器抛异常后，容器元素顺序**未定义**。

这句话会让人以为"程序坏了"，实际标准给的定性是**顺序未指定**（unspecified）——元素集合仍然合法，
只是顺序不保证。**读者会因此恐慌或误判代码不可用。**

## 机制

判断两类**不能**只问"有没有副作用冲突"，要问两个副作用处于哪种关系：

- ***unsequenced***（**可能重叠**）→ 命中 UB 条款（[intro.execution]：未测序的标量修改）→ **UB**；
- ***indeterminately sequenced***（**不保证顺序、但绝不允许重叠**）→ 只是顺序不确定 → **unspecified**。

**版本边界（最容易踩的坑）**：C++17（P0145R3）把**函数参数初始化**从 unsequenced 改为
indeterminately sequenced（[expr.call]）；而**运算符操作数仍是 unsequenced**。

| 代码 | 两个副作用处于什么关系 | 标准给了什么 | 定性 |
|---|---|---|---|
| `f(g(), h())`（`g`/`h` 只打印） | 实参初始化：*indeterminately sequenced* | 两种调用顺序**都合法** | **unspecified** |
| `f(i++, i++)`（**C++17 起**） | 实参初始化：*indeterminately sequenced*（**不重叠**） | 两种顺序都合法，`i` 最终都是 `i+2` | **unspecified** |
| `f(i++, i++)`（**C++11/14**） | 实参求值：*unsequenced*（**可重叠**） | 同一标量两侧副作用冲突 | **UB**（版本边界） |
| `i = i++ + ++i`（所有版本） | 运算符操作数：*unsequenced* | 任何结果都可能 | **UB** |
| `*reinterpret_cast<float*>(&int_obj)` | ——（不是测序问题，而是访问类型受限） | 违反 [basic.lval] | **UB** |

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-UB-001`（GCC 8.1/13.1/15.3 × -O0/-O2，6 组） | 全部输出 `h` → `g` → `f(1,2)`（右→左），rc=0，sanitizer 无报错 | 属 unspecified（有合法集合、不崩） |
| `EV-UB-001`（**CI 的 Clang，`-O2`**） | 输出 `g` → `h` → `f(1,2)`（**左→右**） | **与 GCC 相反**——顺序不是标准规定的 |
| `EV-UB-002`（`-O2`） | 函数返回 `1` 而内存实际 `1073741824` → **不自洽** | UB 被优化器利用 |
| `EV-UB-002`（`-O2 -fno-strict-aliasing`，证伪对照） | 二者恢复自洽 | 差异确实来自别名假设，而非我算错 |
| 汇编（`_atom_strict_alias.asm` `@L8–L14`） | `mov eax, 1` 在两次写之前，且**无二次读** `[rcx]` | 优化器已假定两指针不指向同一对象 |

**关键教学点**：GCC 三个版本（跨 7 年）× 两档优化 **6 组全部一致**，很容易让人误以为"标准规定了
右→左"；而 **CI 的 Clang 给出完全相反的顺序**：

```text
GCC   (6 组，8.1/13.1/15.3 × -O0/-O2) : h → g → f(1,2)     右→左
Clang (CI, -O2)                       : g → h → f(1,2)     左→右   ← 相反
```

两边 `rc` 都是 0、都没有 sanitizer 报错——**两种顺序都合法**，这正是 unspecified 与 UB 的分界：
前者给你两个都对的答案，后者给你一个"什么都可能"的空白。

`EV-UB-002` 另有一处必须留痕的方法论：它的**第一版夹具自己踩了 UB，连踩三次**
（`volatile int` 溢出 → `long` 在 **Windows LLP64 下仍是 32 位** → `long long` 但 `int + int`
**在 int 域内先溢出**），三次都是**证据卡的 sanitizer 校验**在 Linux 侧抓到的。
教训：**研究 UB 的实验代码自己最容易踩 UB，且 UB 类证据卡必须在 Linux 侧过一遍 sanitizer。**

## 反例（证伪导向：让它失败的实验）

**反例一：真正的 UB 长什么样（`i = i++ + ++i`）。** C++17 起 `f(i++, i++)` 已是 unspecified，
**不能**再用它当 UB 例子——但运算符的操作数求值仍是 unsequenced：`i = i++ + ++i` 在 C++17+
依然"任何结果都可能"。把这一对并排看，判据就清楚了。

**反例二：把 UB 当"能跑就行"的偏门技巧。** `EV-UB-002` 实测同一份代码：

```text
-O0                              A 函数返回=1073741824 内存实际=1073741824 自洽=是
-O2（严格别名）                  A 函数返回=1          内存实际=1073741824 自洽=否   ← UB 被利用
-O2 -fno-strict-aliasing         A 函数返回=1073741824 内存实际=1073741824 自洽=是   ← 对照
```

`-O0` 下"好好的"，`-O2` 下函数返回值与内存实际值**不一致**——这不是"优化出 bug"，
而是**你的代码已经在标准意义上失去意义**，编译器只是恰好利用了这一点。

**证伪条件**：求值顺序侧——任何一次运行崩溃、或同一二进制两次跑输出不同，即证伪"它是 unspecified"；
严格别名侧——若 `-fno-strict-aliasing` 开关不影响结果，说明观测到的差异不来自别名假设，证据作废。

## 边界（合法与违规的分界）

- ✅ `char*` / `unsigned char*` / `std::byte*` **可以**别名任何对象类型（[basic.lval] 明文例外）；
- ✅ 需要按位看浮点数的位模式 → 用 `std::memcpy`（夹具的合规对照路径就是它）或 `std::bit_cast`（C++20）；
- ❌ 通过 `reinterpret_cast` 得到的 `float*` 去读 `int` 对象；
- ❌ 依赖同表达式内的顺序/副作用组合：`i = i++ + ++i`（未测序 → **UB**）、`f(i++, i++)`
  （**C++17 起是 unspecified**——不崩但不可依赖；C++11/14 下才是 UB）。正确写法是**拆成两条语句**。

**什么时候不该用**：本原子不是"叫你别用某特性"，而是**两个"不该"**：
① **不该把 unspecified 当 UB** 去掉恐慌（正确处置是"不依赖它"而非"删掉这段代码"）；
② **不该把 UB 当 unspecified** 去心安（"我本地跑着好好的"不构成任何保证，见三档对照）。

## 学习者常见误解

1. **「函数参数的求值顺序是未定义行为」**（surface）——C++17 起实参初始化是 indeterminately
   sequenced：顺序不可依赖，但既不重叠、也不是 UB。
2. **「`f(i++, i++)` 是未定义行为」**（surface）——C++11/14 确实如此，**C++17 起已是 unspecified**；
   这是"用旧规则套新标准"的典型误判（**本原子在编写过程中就犯过这个错，由人审判正并留痕**）。
3. **「同一段代码在多个编译器/版本下结果一致，说明标准规定了顺序」**（surface）——GCC 六组一致
   但 Clang 相反，实测反例见上。
4. **「只要我这台机器、这个编译器上结果稳定，就可以依赖这个行为」**（deep，反例：`EV-UB-001` +
   `EV-UB-002`）——`EV-UB-001` 用六组一致反证"一致 ≠ 规定"；`EV-UB-002` 用 `-fno-strict-aliasing`
   开关把"看似稳定的行为"一翻就变，两处独立反例共同推翻这个深层误解。

## 签收（S1：声明的"verified"必须由人签）

- 人审记录（四步流程 + 两轮人审）：`goldens/B_eval_order.md`；第 2 轮人审（2026-09-10）**通过并授予
  5 分**，锚定依据见该文件「5 分锚定依据」。
- **签署记录**：`status: verified` · `verified_by: human:liaoranran` · `verified_at: 2026-09-10`
  —— 由人签署（Agent 未自置，守 S1 三权分立）。
