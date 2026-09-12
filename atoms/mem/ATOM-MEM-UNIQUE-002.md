---
id: ATOM-MEM-UNIQUE-002
title: unique_ptr 自定义删除器与数组：删除器进不进类型系统
domain: MEM
type: mechanism
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
dal: B                            # 失效后果分级（G6 §3）：B=教学结论方向错；A/B 须人审
human_review: required            # DAL A/B ⟹ 强制人审（G6）
status_history:                   # 四级晋升链（G6 §2），链尾须等于 status
  - {level: draft, at: legacy, by: writer:agent}
  - {level: machine-verified, at: 2026-09-11, by: machine:gate}
  - {level: human-verified, at: 2026-09-11, by: human:liaoranran}
# ---- 认知适切 ----
audience: intermediate                # 默认读者：会用智能指针、但把删除器当"同样的写法"的人
cognitive_load: medium                # 需同时持有"类型参数 vs 类型擦除"与"实现边界 vs 语言保证"两条线索
prerequisites_readable: true          # 前置 ATOM-MEM-UNIQUE-001 已 verified
claim: >-
  unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统），因此删除器会影响
  对象大小与类型：libstdc++ 下，空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节），
  而空但 final 的删除器与有状态删除器都必须存储（16 字节）——这是**实现边界**而非语言保证
  （final 反例实测 16，见 EV-MEM-032）。数组特化 `unique_ptr<T[]>` 是独立特化：只提供 operator[]、
  不提供 operator* 与 operator->，且在默认删除器下走 delete[]。与之对照，shared_ptr 的删除器被
  **类型擦除**——语言层面不存在 `shared_ptr<T, D>`，删除器只能经构造函数按值注入并被控制块持有，
  对象大小恒为两个指针、与删除器类型无关；代价是控制块自身的堆分配（裸指针构造 2 次分配、
  make_shared 合并为 1 次，见 EV-MEM-033）。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  stdlib: [libstdc++]                 # EBO 门槛与 _Sp_counted_deleter 类型名是实现特性
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-UNIQUE-001}   # unique_ptr 的基本所有权语义（本原子答"删除器与数组这一层"）
  - {type: contrasts, target: ATOM-MEM-SHARED-001}      # 同一删除器需求的两种机制：类型参数 vs 类型擦除
  - {type: contrasts, target: ATOM-MEM-NEW-001}         # new[]/delete[] 配对律：数组特化的删除器默认走 delete[]
evidence:
  - EV-MEM-032          # 删除器进类型系统：sizeof 六连 + trait 三连 + mangled 类型名（含 final 真反例）
  - EV-MEM-033          # 删除器类型擦除：sizeof 恒定 + 控制块类型 + 分配计数对照（2/1/1）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [unique.ptr]/[unique.ptr.single]/[unique.ptr.single.ctor]（删除器作为类型参数、可调用性约束）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared]/[util.smartptr.shared.const]（shared_ptr 只有 T 一个模板参数；删除器经构造函数注入）", independent: true}
  - {kind: cppreference, ref: "std::unique_ptr（数组特化接口）、std::shared_ptr 构造函数与 make_shared 的分配语义", independent: true}
first_hand: true
superiority: >-
  多数资料停在"unique_ptr 的删除器是类型的一部分、shared_ptr 不是"这一句，读者记住结论却
  ① 不知道这句话**能用来判断什么**（对象大小、接口约束、分配次数），② 更不知道"空删除器零开销"
  其实是 libstdc++ 的实现优化（空但 final 就失效）、不是可以依赖的保证。本原子多给三样：
  （a）把两个指针的差异做成**同 TU 对照 + 镜像汇编证据**（删除器出现在 unique_ptr 类型名里
  `unique_ptrIi12StatelessDelE`，而在 shared_ptr 侧只出现在控制块 `_Sp_counted_deleterIPi6TagDel...`）；
  （b）用 `final` 空删除器做**真证伪对照**（实测 16），把假命题"无状态 ⇒ 不增大"逼回可辩护的
  实现边界；（c）把擦除的代价量化为**分配计数三连**（裸指针构造 2 / make_shared 1 / unique_ptr 1），
  与值类别无关，堵死"shared_ptr 只是多了个计数器"的半步理解。
depth:
  layer: asm
  drill_note: >-
    两层证据：编译期（sizeof 六连、trait 三连：数组特化 subscript=1/deref=0/arrow=0）与符号级
    （删除器出现在哪一侧的类型名里）。删除器的**调用形态**随编译器和优化档变化——unique_ptr 侧
    在 -O2 下完全内联，shared_ptr 侧保留控制块虚派发 `call [QWORD PTR 16[rax]]`（MinGW 工件
    322/365 行），但该间接调用在 gcc-14 工件里也被进一步内联，故不写进跨编译器断言。
pedagogy:
  motivation: >-
    为什么给 unique_ptr 写删除器要放进模板参数，而 shared_ptr 不用（也不能）？写了自定义删除器
    会不会让对象变大？shared_ptr 的删除器藏在哪、代价是什么？三个问题分别由 sizeof、类型名符号、
    分配计数来回答。
  misconceptions: [MIS-MEM-024, MIS-MEM-025]   # 只差独占/共享 / T[] 只是语法糖
  socratic:
    - "把一个空结构体当删除器传给 unique_ptr，对象会不会变大？如果把那个结构体标成 final 呢？"
    - "为什么 `shared_ptr<int, MyDel>` 编译不过？这个'编译不过'透露了什么机制？"
    - "`shared_ptr<T>(new T)` 与 `make_shared<T>()` 差在哪一次分配上？unique_ptr 有没有这个问题？"
    - "`unique_ptr<int[]>` 为什么不提供 `operator*`？如果非要用 `unique_ptr<int>` 管 `new int[8]` 会怎样？"
  predict_first: >-
    先预测三个数字再看证据：`sizeof(unique_ptr<int>)`、`sizeof(unique_ptr<int, 空删除器>)`、
    `sizeof(unique_ptr<int, 有状态删除器>)`——再预测把"空删除器"改成 `final` 后是哪个数
    （EV-MEM-032 的 final 组会给出一致性检验）。
---

## 论断

**unique_ptr 把删除器放进类型；shared_ptr 把删除器擦进控制块。** 这条差异有四个可检验后果：

| 后果 | unique_ptr（删除器 = 类型参数） | shared_ptr（删除器 = 类型擦除） | 证据 |
|---|---|---|---|
| 对象大小 | 随删除器变化：8（空且非 final）/ 16（空但 final、有状态） | 恒 16，与删除器无关 | EV-MEM-032 / 033 |
| 类型名 | 删除器出现在 `unique_ptr<T, D>` 的 mangled 名里 | 删除器只在控制块 `_Sp_counted_deleter<...>` 里 | 两卡的工件 |
| 额外分配 | 无（只有对象本身：1 次） | 控制块：裸指针构造 2 次、`make_shared` 1 次 | EV-MEM-033 |
| 接口 | 数组特化是独立类型：只有 `operator[]` | 无数组特化（用 `shared_ptr<T>` 管数组需自定义删除器） | EV-MEM-032 trait |

## 为什么（把"两个不同的问题"分开）

**问题一：删除器该不该影响类型？** unique_ptr 回答"该"——它把 D 写进模板参数，于是编译期就能检查
删除器可调用性、就能对空删除器做存储优化；代价是**每个删除器都是一个新类型**（不能放进同一个容器、
不能在同一变量里换删除器）。shared_ptr 回答"不该"——它的模板参数表里只有 T（实测
`shared_ptr<int, TagDel>` 报 `wrong number of template arguments (2, should be 1)`），删除器经构造函数
按值注入、被搬进控制块；代价是类型系统看不见删除器，换来"同一静态类型可持有任意删除器"
（实测 tag=11 → tag=22）。

**问题二：零开销从哪来？** "空删除器不增大对象"是**实现优化**，不是语言保证。libstdc++ 的门槛是
"空**且非 final**"：普通空删除器 sizeof=8（与裸指针同），一旦标 `final` 就失去 EBO、变 16。
所以正确的心智模型是"我依赖的是这套标准库在当前版本下的行为"，而不是"标准规定它零开销"。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-032`（c++23 -O0/-O2 同串） | sizeof 六连 8/8/16/8/16/**16**；trait 三连 1/0/0；三种删除器调用 delta 各 1；`array delete calls=1` vs `single object delete[] delta=0` | 删除器进类型系统；EBO 有 final 边界；数组特化接口与释放路径独立 |
| `EV-MEM-033`（c++23 -O0/-O2 同串） | sizeof 恒 16；拷贝 on ctor=1 / on share=0；三次持有者全 reset 只调 1 次；分配 2/1/1；tag 11→22 | 删除器被擦除进控制块、持有副本、额外一次堆分配 |

汇编层镜像证据：`unique_ptrIi12StatelessDelE`（删除器在 unique_ptr 类型名里）vs
`Sp_counted_deleterIPi6TagDel...`（删除器在控制块类型名里，shared_ptr 类名里没有）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A（已成立）**：若"无状态删除器不增大对象"是普遍规则，`StatelessFinalDel`（空但 final）
  的 sizeof 应为 8——**实测 16**，故该表述被证伪，claim 退守到"libstdc++ 实现边界"。
- **证伪条件 B**：若数组特化走 delete 而非 delete[]，`array delete calls` 与 `single object delta`
  应同时为 0——实测 1 / 0，路径区分成立（运行层重载计数给出）。
- **证伪条件 C**：若 shared_ptr 不需要控制块，`shared_ptr from raw ptr allocs` 应为 1——实测 2，
  且 `make_shared`=1、`unique_ptr`=1 三行互证。
- 实测：A 触发（并因此改写 claim）、B/C 不成立 ⇒ 本原子经受住了自身证伪条件。

## 学习者常见误解

1. **`[MIS-MEM-024]` 两者只差"独占 vs 共享"**——删除器位置（类型参数 vs 类型擦除）是与所有权模型
   正交的第二条轴；EV-MEM-032/033 给出类型名镜像与分配计数。
2. **`[MIS-MEM-025]` `unique_ptr<T[]>` 只是语法糖**——它是独立特化：接口（只有 `operator[]`）与
   释放路径（delete[]）都不同；用 `unique_ptr<int>` 接 `new int[]` 属 UB。

## 不该用 / 边界

- **删除器必须可调用**：D 不满足 `d(ptr)` 时在编译期报错（类型参数的好处正是能早报）。
- **引用删除器要管生命周期**：`unique_ptr<T, D&>` 不持有删除器，被引用的删除器必须活得比指针长
  （实测该形态 sizeof=16：指针 + 引用各 8 字节）。
- **空指针不调用删除器**；删除器抛异常会让 `unique_ptr` 析构（`noexcept`）直接 terminate。
- **不要依赖"空删除器零开销"**：那是 libstdc++ 的实现优化（`final` 反例），跨标准库不成立。
- **shared_ptr 管数组**：C++17 起可用 `shared_ptr<T[]>`，但**默认删除器**在 C++20 前不保证 `delete[]`；
  显式给删除器更稳妥。

## 学习路径

`ATOM-MEM-UNIQUE-001`（unique_ptr 所有权）→ **本原子**（删除器与数组这一层）→
`ATOM-MEM-SHARED-001`（共享所有权的代价）→ `ATOM-MEM-WEAK-001`（打破循环）。

---

## Step 1：3 分平庸版（留痕）

初版只有结论没有判据：claim 未量化（"不增加大小"无数字）、未说明 EBO 是**实现**还是**语义**保证、
数组特化只提 delete[] 漏了接口差异、缺边界与学习路径、标准条款未落小节、教学封装各只有 1 条。
自评 **3/5**。（完整缺项清单见 Git 历史：本文件 Step 1 版提交内容。）

## Step 2：红队攻击报告（独立子 agent，S1–S6）

> 红队由 Task 工具启动的独立子 agent 执行（视角与作者分离），**只挑错不改正文**。以下为报告要点，
> 完整报告含逐条工件行号，已随本卡提交记录留痕。

**阻断项（2）**

1. **B1 · 自证断言**：`EV-MEM-032` 原 `artifact_assert` 的 `{contains_any: ["_ZdaPv","_ZdaPvy"]}` 是
   **夹具自身定义**满足的——工件里只有夹具重载的 `operator delete[]` 定义（271–286 行），
   **没有任何 `call _ZdaPv` 调用点**（`-O2` 把数组路径完全内联）。断言恒真 = 伪证据，违反
   M2 §5（汇编层必须能找到对应调用点）与铁律 6。`expected.asm` 的措辞还把"存在"当"被调用"。
   → **处置**：删除该断言；把"delete[] 路径"的结论**只**交给运行层重载计数；卡内明写"调用点被内联，
   汇编层不可判"。
2. **B2 · 伪证伪 / 恒真观测**：两卡的 `falsification` 全是"若…则应…"假设句，无真实失败对照；
   且 033 的 `sizes equal=1`（同型自比）与 `retargeted=1`（只查非空）**定义上不可能失败**。
   → **处置**：新增真对照（032 的 `final` 空删除器组、033 的分配计数 2/1/1），删掉恒真条件。

**高危项（7）**

3. **"无间接调用"被自家工件反例化**：工件里存在 `call [QWORD PTR 16[rax]]`（032 322/365 行、
   033 352/395/441 行）——作者的 grep 模式 `call\s+(rax|...)` 匹配不到该写法，属实测盲区。
   → **处置**：表述改为"unique_ptr 侧完全内联；shared_ptr 侧保留控制块虚派发 `call [QWORD PTR 16[rax]]`"，
   并注明该点随编译器内联决策变化、不进跨编译器断言。
4. **拷贝对照被值类别污染**：033 原版拿"unique_ptr 传右值（0 拷贝）vs shared_ptr 传左值（1 拷贝）"
   当对照——差异只来自实参值类别，与"类型参数 vs 擦除"无关。 → **处置**：撤除，换成与值类别无关的
   **分配计数**对照（2/1/1）。
5. **"拷贝进控制块恰一次"错误归因**：实测那 1 次拷贝发生在**按值形参初始化**，控制块内是 move/字段搬运。
   → **处置**：卡内改述归因，并标注"次数属实现细节"。
6. **`stateless calls=2`/`stateful calls=3` 构成未交代**（累计值混入 shared_ptr 块的调用）。
   → **处置**：夹具改为**差分**计数（`...delta=1`），语义自明。
7. **`array len=8 elem3=42` 是折叠恒真值**（工件里 `mov edx,8` / `mov r8d,42` 直接喂 printf）。
   → **处置**：改为从 `argc` 派生的运行期长度与下标（现输出 `array len=8 elem=12`）。
8. **"三平台 12/12/7、22/22/13"口径不明**（未给计数命令，读者无法复现）。
   → **处置**：卡内注明口径（`grep -c <符号> <工件>` 按行计）并给出各平台数值 7/12/12、43/65/65。
9. **`final` 空删除器反例**（可证伪 claim 的字面表述）。 → **处置**：夹具新增该组，**实测 16**，
   claim 相应改写（见 Step 3）。

**中危项（9，摘要）**：`expected` 未覆盖 actual 全部字段（已补齐为全字段）；claim 三处越界
（数组+自定义删除器未测、EBO 当保证、与 SHARED-001 重复——已分别限定/改写/去重）；
`-O0` 无命令无口径（已补口径披露）；matrix 缺 `stdlib`（已补）；引用了**尚不存在**的
`ATOM-MEM-SHARED-002`（已改指 SHARED-001）；"跨标准库稳定"过度宣称（已改为"仅跨 libstdc++ 版本"）；
`tag after first/second assignment` 标签与测点不符（已改 `tag seen after reset #1/#2`）；
控制块 32 vs 24 字节、`(void)up2` 掩盖观测源、单对象路径缺正向计数（记为后续可选增强）。

**低危项**：`rubric_self` 不在 G1 字段表（入库前移除）；`[unique.ptr.dltr]` 等小节名需逐条核对标准原文
（**不照抄**历史写法）；`EV-SERVES-EXIST` 债（原子入库后自动清零）。

**S6 制衡缺口（本批暴露的工具债，非本卡内容问题）**：现有毒样例 P1–P3 抓不到本批两类缺陷——
①"断言被夹具自身定义满足"（自证断言，`contains_any` 全文匹配必然放行）；
②"falsification 为假设句且无对照值"（现口径只查非空）。建议下一批新增毒样例：
**P4 自证断言**（断言文本来自夹具自身定义即判无效）、**P5 伪证伪**（无对照 `run_*`/差分值即拦）、
**P6 恒真观测**（值对应工件里的立即数即 warn）、**P7 无留痕矩阵**（声明了某编译器却无工件/留痕即拦）。

## Step 3：升 5 分候选（逐条回应红队）

| 红队指控 | 处置 | 证据 / 落点 |
|---|---|---|
| B1 自证断言 | 删除 `_ZdaPv` 断言；结论改由运行层重载计数承担；卡内明写内联事实 | `expected.asm` + drill_note；断言现为 3 条（类型名 / 控制块 / `_Znwm`） |
| B2 伪证伪 | 新增 `final` 空删除器真对照 + 分配计数三连；删除恒真条件 | 032 的 `sizeof ... final stateless=16`；033 的 `allocs=2/1/1` |
| 值类别污染 | 撤除该对照，换分配计数 | 033 §③ 重写，夹具注释留痕拦截原因 |
| 无间接调用表述错 | 改写为两卡镜像表述并注明不可跨编译器断言 | drill_note（032/033 各一段） |
| 归因错误（拷进控制块） | 改为"按值形参初始化时拷贝 1 次，块内持有副本" | 033 边界说明第 2 条 |
| 计数构成不可解释 | 夹具改差分 | `stateless/stateful/final calls delta=1` |
| 恒真观测（array 行） | 改由 `argc` 派生的运行期值 | `array len=8 elem=12` |
| 数字口径不明 | 卡内注明 grep 口径与三平台数值 | 032/033 的「机器口径」节 |
| `final` 反例 | 实测 16，claim 改写为"实现边界" | claim + 反例条件 A + superiority |

**平庸版 → 5 分候选的关键补丁（三处增量）**

1. **统一解释有增量**：把"两个智能指针的差异"从一维（所有权）扩成二维（所有权 × 删除器位置），
   并给出四个可检验后果（大小 / 类型名 / 额外分配 / 接口）；再用 `final` 反例把"零开销"从
   "语言保证"降级为"实现边界"——这是多数资料不会写的一层。
2. **量化到机器证据**：四组数字（sizeof 六连、trait 三连、调用 delta 三连、分配 2/1/1）全部来自
   同 TU 对照夹具，或 -O0/-O2 逐字一致；汇编层用**镜像类型名**（`unique_ptrIi12StatelessDelE` vs
   `_Sp_counted_deleterIPi6TagDel...`）钉住机制，且已剔除自证断言。
3. **过程本身有教学价值**：本卡的 Step 2/3 记录了一次真实的"作者被红队打回"——包括一个
   自证断言、一个被值类别污染的对照、一个被自己的工件证伪的表述。把这三处留痕比只给结论更有用：
   读者看到的是一套**可复用的自检清单**（断言是否被夹具自满足？对照的差异是否来自目标变量？
   复现命令能不能让第二个人拿到同一个数？）。

## Step 4：人审准备（等 human:liaoranran）

1. **claim 的边界表述**：把"空且非 final ⇒ 8 字节"写成 libstdc++ 实现边界（并留 `final` 反例）是否
   足够精确？是否需要把标准库版本写进 `claim_boundary.stdlib`（现为 `libstdc++`）？
2. **汇编断言的取舍**：删掉 `_ZdaPv` 自证断言后，"delete[] 路径"只剩运行层证据。是否接受
   （本卡判断：接受，因为运行层是**真观测**且两档一致），还是要求补一条"内联后的 main 内联路径
   特征"断言？
3. **`final` 反例的归属**：它现在是 032 内的一个对照组。是否值得升为独立证据卡
   （EV-MEM-034「EBO 的实现边界」），供后续讲 allocator/OOP 时复用？

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（3 条独立源含两条 ISO 段级 + cppreference；两卡一手实证含真反例与 -O0/-O2 双档；superiority 见 Step 3；depth=asm；教学封装含 4 条 socratic + predict_first）；自评上限 4：**跨编译器仅 GCC 系（Clang 列待 CI 回填）**，且 `final` 反例与 `_Sp_counted_deleter` 类型名绑定 libstdc++。 |
