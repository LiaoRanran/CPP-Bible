# 样板 B：灰色地带——「未指定」与「未定义」（`goldens/B_eval_order.md`）

> **状态**：**人审通过（第 2 轮，2026-09-10）· 授予 5 分 · 已原子化** →
> `atoms/ub/ATOM-UB-GRAY-001.md`（`status: verified`，`verified_by: human:liaoranran`）。
> 本文件保留四步留痕与人审轮次记录，作为 G4 第二块样板。
>
> **四步流程（一轮内走完，每步独立留痕）**：① 3 分平庸版 → ② 红队按 S1–S6 攻击 →
> ③ 升级 5 分候选（逐条写明补了什么）→ ④ 人审（**两轮**，见文末轮次记录）。
>
> **配套证据**：`evidence/ub/EV-UB-001.md`（求值顺序：6 组矩阵实测）、
> `evidence/ub/EV-UB-002.md`（严格别名：UB 被优化器利用 + 汇编铁证）；
> 夹具 `Examples/atoms/_atom_eval_order.cpp` · `Examples/atoms/_atom_strict_alias.cpp`（含 `.asm` 工件）。

---

## 第 1 步：3 分平庸版（正确但平庸）

> 保留原文不改。判断标准：**正确但读者看完仍分不清两类**——把 unspecified 与 UB 混着讲。

**求值顺序与严格别名**

C++ 中函数参数的求值顺序是未定义的，所以不要写 `f(i++, i++)` 这种依赖顺序的代码，
结果可能因编译器而异。这是初学者常踩的坑。

严格别名是指不能用不同类型的指针访问同一块内存，例如：

```cpp
int x = 1;
float* p = (float*)&x;      // 违反严格别名
printf("%f", *p);           // 未定义行为
```

开了 `-O2` 之后编译器会做各种优化，这些代码可能不按你的预期工作，所以应该避免。

**结论**：参数求值顺序和严格别名都可能导致未定义行为，写代码时要小心。

---

## 第 2 步：红队攻击报告（按 S1–S6 逐条）

### S1（签收是不是人？）

- 平庸版无 frontmatter、无 `status`、无 `verified_by` → **不合格**。
- 处置：5 分版给 `status: draft`；`verified` 只能由人置。

### S2（断言有没有可独立复算的证据？）

- 平庸版把两类问题都归为"未定义行为"，**且没有任何证据引用**。→ **不合格**。
- 更严重的是**定性错误（两处，方向相反）**：平庸版把 `f(g(), h())` 的顺序说成"未定义"（在
  C++17+ 应为 unspecified）；它同时也没提 `f(i++, i++)` 的**版本边界**——C++11/14 是 UB、
  **C++17 起是 unspecified**。本样板的靶子正在这里（见 S3-①）。

### S3（反例真会失败吗？期望值有没有硬编码？矩阵够不够？）

**红队在这一步抓到五处真缺陷——本样板最大的价值都在这里。**

**① 🔴 定性错误——一次完整的「纠错 → 被纠正」往返，两层都留痕（人审记录）**

任务书把知识点写成「`f(i++, i++)` 的两个 `i++` 顺序未指定，但不是 UB」。

- **执行方初判（错）**：认为后半句可疑——`f(i++, i++)` 是同一标量在两处修改，应属 UB。
  于是把它当作"任务书写错"写进正文，依据引的是 [intro.execution] "未测序的标量修改"。
- **人审复核（2026-09-10，监工）**：**执行方错了**。C++17（P0145R3）已把**函数参数初始化**
  从 *unsequenced* 改为 **indeterminately sequenced**：
  - [expr.call]：参数的初始化"含其全部值计算与副作用，与其他参数的初始化是 **indeterminately
    sequenced**"；
  - [intro.execution]：indeterminately sequenced = "A 在 B 前或 B 在 A 前，**但哪个不确定**"，
    且**不可重叠**（note：cannot overlap）；
  - 而 UB 条款**只针对 _unsequenced_ 的副作用**。

  → 因此 **C++17 起 `f(i++, i++)` 是 unspecified，不是 UB**（函数收到 `(i, i+1)` 或 `(i+1, i)`，
  两种都合法，`i` 最终都是 `i+2`）。**任务书在 C++17+ 下的说法是对的，执行方纠正过头。**

**正确的说法必须带版本边界**：

| 写法 | C++11/14 | C++17 起 |
|---|---|---|
| `f(i++, i++)`（**函数实参**） | **UB**（实参求值 unsequenced） | **unspecified**（indeterminately sequenced，不重叠） |
| `i = i++ + ++i`（**运算符操作数**） | UB | **仍是 UB**（运算符操作数求值仍是 unsequenced） |

**这条往返本身成了样板最有价值的部分之一**：
① 它纠正的是**执行方**而非任务书——"**用旧版本的规则套新标准**"正是本项目最该防的口径漂移
   （与"同一概念三套口径"同类）；
② 它给出可迁移判据：**先判断两个副作用是 _unsequenced_ 还是 _indeterminately sequenced_**，
   而不是笼统问"有没有副作用冲突"；
③ `i = i++ + ++i` 在 C++17+ 依然是 UB，正好留下一个真正属于"未测序标量修改"的例子。

**② 🔴 夹具输出的 `|` 与证据卡的字段分隔符冲突（实测 `refute:run_match`）。**

首版 `_atom_eval_order.cpp` 把三者拼成一行 `hg|f(1,2)`，而证据卡 `run_*` 字段用 `|` 分隔多变体
→ 工具把 1 行拆成 2 段、与实际 3 行对不上。修法：夹具改为三行独立输出（语义也更清晰：
谁先出现谁先被求值）。

**③ 🔴 我原本设计的"汇编层证据"不成立。**

原设想是"在 asm 里看 `call _Z1hv` 在 `call _Z1gv` 之前"——实测 **`-O2` 把 `g`/`h` 全内联了**，
asm 里根本没有这两个 `call`。改用**可观测的等价证据**：`main` 内三次
`call __mingw_printf` 的出现顺序（`@L70` → `@L72` → `@L76`，即 h → g → f）。
**教训**：不要预设"汇编里应该能看到什么"，先看工件。

**④ 🔴 严格别名夹具自己踩了 UB，而且连踩三次（由证据卡的 sanitizer 校验抓到）。**

| 次序 | 写法 | 报错 | 根因 |
|---|---|---|---|
| 一 | `volatile int g_sink` | UBSan `signed integer overflow` | 1073741824×2 > `INT_MAX` |
| 二 | `volatile long g_sink` | 仍溢出（asm 里仍是 `.lcomm …,4,4`） | **Windows 是 LLP64：`long` = 32 位** |
| 三 | `long long` + `a_func + a_mem` | 仍溢出 | `int + int` **在 int 域内先溢出**，提升得太晚 |

最终版：`static_cast<long long>(a) + static_cast<long long>(b)`。
**"研究 UB 的夹具自己踩 UB"** 这件事本身就是最好的教材——而且三次都不是靠肉眼发现，
是被**证据卡的 sanitizer 校验**逼出来的（第一次直接判 `refute:sanitizer_reported`）。

**⑤ 🔴 异构环境复算会静默污染仓库工件（工具缺陷，已修）。**

在 WSL/Linux 上跑 `atom_evidence_replay.py --check` 时，复算流程「删旧工件 → 重生成」会把仓库里
**MinGW 归属**的 `.asm` 换成 Linux 产物（汇编里出现 `endbr64` / `__printf_chk@PLT`），
而卡里的 `artifact_sha256` 仍是 MinGW 的 → 仓库工件与卡**不同代**，且**没有任何报错**。
修法：校验前快照工件字节、`finally` 里还原（校验工具是只读角色）；加 `--no-restore` 供调试；
新增回归测试 `test_artifact_restored_after_replay`。

矩阵：`EV-UB-001` 覆盖 `{GCC 15.3, 13.1, 8.1} × {-O0, -O2}` 6 组 + **Clang（CI runs）**
↔ **两者给出相反顺序** ✓；`EV-UB-002` 覆盖 `-O2`（主档）+ `-O0` / `-O2 -fno-strict-aliasing`
（人工补跑）✓。

### S4（入库会不会让黄金锁恶化？）

- 样板落在 `goldens/`，不进 `atoms/` → 不参与原子库指标 ✓
- 两卡新增会使 `evidence_total` / `replay_confirm` 上升（改善）；`EV-SERVES-EXIST` 会新增
  2 条 warn（服务的原子尚未锻造）→ 按项目机制 `check --accept "<理由>"` 留痕后 sync。

### S5（有没有需要开的豁免票？`owner` 必须 `human:*`）

- **Clang 列已实测，无需豁免票**：CI 的 `Gray-zone Matrix` 步用 runner 自带的 `clang++` 编译运行了
  同一夹具，结果经 `::notice::` 注解留痕（本仓 job 日志需 admin，注解可公开读取）——
  **`g` → `h` → `f(1,2)`，与 GCC 的 `h` → `g` 相反**。这直接满足 M2 §2
  "**GCC + Clang 双编译器实测**"的边界，不必降级。
- MSVC 无任何可执行路径 → 按 M2 §2 永久边界以标准条文代替。准确表述是
  **"GCC + Clang 双编译器实测 + MSVC 标准条文"**，**不得写成"三编译器全部实测"**。

### S6（把这份样板当毒样例攻击制衡层：现有规则抓不抓得住它的问题？）

| 注入 | 期望被拦 | 实际 |
|---|---|---|
| 把 `pedagogy.misconception` 写成字符串列表 | `ATOM-MISCONCEPTION-LEVELS` | ✅ 拦 |
| frontmatter 里 `status: verified` 但清空 `evidence` | S1/S2 绑定 | ✅ 拦 |
| `artifact_sha256` 写错 | `refute:sha256_mismatch`（身份匹配时） | ✅ 拦 |
| **实验代码自身带 UB** | —— | ⚠️ **只有"跑 sanitizer 真跑"才能抓到**（本地 MinGW 不支持 ASan → 在 Windows 上跑会**静默放过**，靠 WSL 才抓到，见 S3-④） |

**红队结论**：第 4 项暴露一个**覆盖不对称**——`sanitizer` 校验在 Windows 上 `skip`（工具链不支持），
在 Linux 上才真跑。**"UB 类证据卡必须在 Linux 侧过一遍 sanitizer"应成为流程要求**，
否则 Windows 单侧开发会漏掉整类问题。→ 已在本样板执行（WSL 复核 4/4），并建议写入 M2。

---

## 第 3 步：升级到 5 分候选（逐条写明补了什么）

### 补了什么（对照红队清单）

| 红队问题 | 补了什么 |
|---|---|
| S2/S3-① 定性错误（含**执行方自己纠错过头**） | 主线改为「看标准有没有给合法结果集合」；补**版本边界表**（`f(i++,i++)`：C++11/14 = UB → **C++17 起 = unspecified**），并换 `i = i++ + ++i` 作真正属于"未测序标量修改"的 UB 例子 |
| S3-① 知识点本身有误 | 在正文与 falsification 中**显式纠正**，并列入"常见误解"第 1 条 |
| S3-② `|` 冲突 | 夹具改三行输出，语义更清晰 |
| S3-③ 汇编写错方向 | 改用可验证的 `__mingw_printf` 顺序（`@L70/72/76`），并把"先看工件再断言"写进流程 |
| S3-④ 夹具自身 UB ×3 | 全部修掉并留痕；把"UB 类实验必须过 sanitizer"写成教训 |
| S3-⑤ 工具污染工件 | 修工具（快照+还原）+ `--no-restore` + 回归测试 |
| S2 无证据 | 绑定 `EV-UB-001` / `EV-UB-002`，均 confirm，且**双平台复核**（Windows sha 轨 / WSL 断言轨 + sanitizer 真跑） |
| 无纵深 | 补汇编行号级证据（`alias_kill` `@L8–L14`；`__mingw_printf` 顺序） |
| 无"不该做" | 三问题主线第三问：不该依赖求值顺序、不该用类型双关读位模式（给 `memcpy` 合规替代） |

### 5 分候选正文（原子化后的形态）

```markdown
---
id: ATOM-UB-GRAY-001
title: 先问"标准给了合法结果集合吗"：给集合的是未指定，连集合都没有才是未定义
domain: UB
type: contrast
status: draft                  # draft|verified|rejected（唯人可置 verified）
claim: >-
  `f(g(), h())` 的实参求值顺序是**未指定**（unspecified）——两种顺序都合法、程序不会崩，
  但不可依赖；而**未测序（unsequenced）的同一标量修改**（如 `i = i++ + ++i`）与**通过不兼容
  类型指针访问对象**（严格别名）属于**未定义行为**，标准不再要求任何行为，优化器可据此删除
  你的访问。（版本边界：函数实参 `f(i++, i++)` 自 **C++17 起是 _indeterminately sequenced_** →
  **unspecified**，不再是 UB；C++11/14 下才是 UB。）
claim_boundary:
  standard: [C++17, C++23]
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
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.call]（实参求值顺序未指定）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.execution]（未测序的标量修改为 UB；indeterminately sequenced 定义为不重叠）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.call]（函数参数初始化是 indeterminately sequenced）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.lval]（严格别名：访问对象的 glvalue 类型受限）", independent: true}
  - {kind: cppreference, ref: "Undefined behavior / Order of evaluation", independent: true}
first_hand: true
superiority: >-
  现有资料通常把两类分两页讲（"求值顺序"一页、"严格别名"一页），读者拿不到**统一判据**，
  于是把 unspecified 当 UB 恐慌（本书灰色地带实测：1478 个候选句里 74.4% 被判 UB、仅 6.3% 判
  unspecified，量级差 12 倍——"未定义"被泛用是**可测量的**），或把 UB 当"偏门技巧"照用。
  本原子给出**一句话判据**（标准有没有给合法结果集合），并用同一份可编译夹具把两类并排对照：
  unspecified 侧**GCC 六组一致、Clang 相反**（教"顺序不是标准规定的"），UB 侧用
  `-fno-strict-aliasing` 开关把"优化器利用了 UB"直接翻出来（教"能跑 ≠ 合法"）。
depth:
  layer: asm
  drill_note: >-
    UB 被利用与否在汇编层可见：`alias_kill`（`@L8–L14`）里返回值 `mov eax, 1` 排在两次写之前、
    且函数体内**没有**对 `[rcx]` 的二次读取——优化器已假定两个不同类型的指针不指向同一对象。
pedagogy:
  motivation: 为什么标准要区分"未指定"和"未定义"？合起来叫"不确定"不就完了？
  misconception:
    - level: surface
      text: "函数参数的求值顺序是未定义行为"（C++17 起实参初始化是 indeterminately sequenced：顺序不可依赖，但既不重叠、也不是 UB）
    - level: surface
      text: "f(i++, i++) 是未定义行为"（C++11/14 确实如此，**C++17 起已是 unspecified**——"用旧规则套新标准"的典型误判）
    - level: surface
      text: "同一段代码在多个编译器/版本下结果一致，说明标准规定了顺序"
    - level: deep
      text: "只要我这台机器、这个编译器上结果稳定，就可以依赖这个行为"
      refutations: [EV-UB-001, EV-UB-002]
  socratic:
    - "同一段代码在 GCC 8.1 到 15.3 上跑了一致结果——这能证明标准规定了顺序吗？"
    - "如果标准说'未定义'，编译器能不能假设这段代码永远不会执行？"
  predict_first: 把 `-O2` 换成 `-O2 -fno-strict-aliasing`，`alias_kill` 的返回值会变吗？（先预测，再看 EV-UB-002）
---
```

#### 先问"标准给了合法结果集合吗"：给集合的是未指定，连集合都没有才是未定义

**问题（是什么）**

"未定义行为"这个词在中文技术写作里被泛用得很厉害——本书自测就量到了这个偏差：全书 1478 个
灰色地带候选句里，**74.4% 被判为 UB，只有 6.3% 判为 unspecified**（相差 12 倍，
`tools/gray_zone_scan.py` 实测）。而被抓到的真实误用长这样：

> `std::sort` 的比较器抛异常后，容器元素顺序**未定义**。

这句话会让人以为"程序坏了"，实际标准给的定性是**顺序未指定**（unspecified）——元素集合仍然合法，
只是顺序不保证。**读者会因此恐慌或误判代码不可用。**

**机制（为什么需要）**

区分两类只需要问一句话：**标准有没有给出合法结果的集合？**

1. 有集合、实现任选其一 → **unspecified**（不要求写进文档）
2. 连集合都没有、"任何行为都可能" → **UB**
3. 有集合、且**要求**实现写进文档 → **implementation_defined**（第三类，本文不展开）

拿本样板的两组例子套：

| 代码 | 两个副作用处于什么关系 | 标准给了什么 | 定性 |
|---|---|---|---|
| `f(g(), h())`（`g`/`h` 只打印） | 实参初始化：*indeterminately sequenced* | 两种调用顺序**都合法** | **unspecified** |
| `f(i++, i++)`（**C++17 起**） | 实参初始化：*indeterminately sequenced*（**不重叠**） | 两种顺序都合法，`i` 最终都是 `i+2` | **unspecified** |
| `f(i++, i++)`（**C++11/14**） | 实参求值：*unsequenced*（**可重叠**） | 同一标量两侧副作用冲突 | **UB**（版本边界） |
| `i = i++ + ++i`（所有版本） | 运算符操作数：*unsequenced* | 任何结果都可能 | **UB** |
| `*reinterpret_cast<float*>(&int_obj)` | ——（不是测序问题，而是访问类型受限） | 违反 [basic.lval] | **UB** |

**注意第三、四行**——这是最容易搞错、而且**纠错方向常常相反**的一条：`f(g(), h())` 与 `f(i++, i++)`
在 **C++17 起同类**（都是 unspecified），但在 **C++11/14 不同类**（后者是 UB）。

**判断依据不是"有没有副作用"，也不是"顺序确定不确定"**，而是两个副作用处于哪种关系：

- ***unsequenced***（**可能重叠**）→ 命中 UB 条款 → **UB**；
- ***indeterminately sequenced***（**不保证顺序、但绝不允许重叠**）→ 只是顺序不确定 → **unspecified**。

C++17（P0145R3）把**函数参数初始化**从前者改成了后者；**运算符操作数仍是前者**——
所以 `f(i++, i++)` 变了，`i = i++ + ++i` 没变。

**证据（怎么知道）**

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-UB-001`（GCC 8.1/13.1/15.3 × -O0/-O2，6 组） | 全部输出 `h` → `g` → `f(1,2)`（右→左），rc=0，sanitizer 无报错 | 属 unspecified（有合法集合、不崩） |
| `EV-UB-001`（**CI 的 Clang，`-O2`**） | 输出 `g` → `h` → `f(1,2)`（**左→右**） | **与 GCC 相反**——顺序不是标准规定的 |
| `EV-UB-002`（`-O2`） | 函数返回 `1` 而内存实际 `1073741824` → **不自洽** | UB 被优化器利用 |
| `EV-UB-002`（`-O2 -fno-strict-aliasing`，证伪对照） | 二者恢复自洽 | 差异确实来自别名假设，而非我算错 |
| 汇编（`_atom_strict_alias.asm` `@L8–L14`） | `mov eax, 1` 在两次写之前，且**无二次读** `[rcx]` | 优化器已假定两指针不指向同一对象 |

**关键教学点（EV-UB-001 的真正价值）**：GCC 三个版本（跨 7 年）× 两档优化 **6 组全部一致**，
很容易让人误以为"标准规定了右→左"；而 **CI 的 Clang 给出完全相反的顺序**（`g` 先于 `h`）。
**这就是"未指定"的实证**：不是"我们还没测出规律"，而是**根本没有规律可测**——
实测的落地版：

```text
GCC   (6 组，8.1/13.1/15.3 × -O0/-O2) : h → g → f(1,2)     右→左
Clang (CI, -O2)                       : g → h → f(1,2)     左→右   ← 相反
```

两边的 `rc` 都是 0、都没有 sanitizer 报错——**两种顺序都合法**，这正是 unspecified 与 UB 的分界：
前者给你两个都对的答案，后者给你一个"什么都可能"的空白。

**反例与边界**

**反例一：真正的 UB 长什么样（`i = i++ + ++i`）。** C++17 起 `f(i++, i++)` 已是 unspecified，
**不能**再用它当 UB 例子——但**运算符的操作数求值仍是 unsequenced**：`i = i++ + ++i` 在 C++17+
依然是"任何结果都可能"（[intro.execution] 未测序的标量修改）。把这一对并排看，判据就清楚了：
**问两个副作用是 unsequenced（可能重叠 → UB）还是 indeterminately sequenced（不重叠 → unspecified）**，
而不是笼统问"有没有副作用冲突"。

**反例二：把 UB 当"能跑就行"的偏门技巧。** `EV-UB-002` 实测同一份代码：

```text
-O0                              A 函数返回=1073741824 内存实际=1073741824 自洽=是
-O2（严格别名）                  A 函数返回=1          内存实际=1073741824 自洽=否   ← UB 被利用
-O2 -fno-strict-aliasing         A 函数返回=1073741824 内存实际=1073741824 自洽=是   ← 对照
```

`-O0` 下"好好的"，`-O2` 下函数返回值与内存实际值**不一致**——这不是"优化出 bug"，
而是**你的代码已经在标准意义上失去意义**，编译器只是恰好利用了这一点。

**边界（合法与违规的分界）**：
- ✅ `char*` / `unsigned char*` / `std::byte*` **可以**别名任何对象类型（[basic.lval] 明文例外）；
- ✅ 需要按位看浮点数的位模式 → 用 `std::memcpy`（本夹具的合规对照路径就是它）；
- ✅ `std::bit_cast`（C++20）是编译期的合规替代；
- ❌ 通过 `reinterpret_cast` 得到的 `float*` 去读 `int` 对象；
- ❌ 依赖同表达式内的顺序/副作用组合：`i = i++ + ++i`（未测序 → **UB**）、`f(i++, i++)`
  （**C++17 起是 unspecified**——不崩但不可依赖；C++11/14 下才是 UB）。正确写法是**拆成两条语句**。

**什么时候不该用**：本原子不是"叫你别用某特性"，而是**两个"不该"**：
① **不该把 unspecified 当 UB**去掉恐慌（正确处置是"不依赖它"而非"删掉这段代码"）；
② **不该把 UB 当 unspecified**去心安（"我本地跑着好好的"不构成任何保证，见上面三档对照）。

---

## 第 4 步：人审（待用户）

请按 0.4 rubric 的 5 分锚（**外行能懂 · 行家挑不出硬伤 · 有别处看不到的洞见**）裁决。
本文件是**候选**，Agent 不自称达标。G4 的 5 分口径见 `goldens/A_move.md`「5 分锚定依据」。

**人审轮次记录**：

- **第 1 轮（2026-09-10）**：监工评估 **3/5，阻断放行**。指出三处：
  ① 【严重】`f(i++, i++)` 定性错误——C++17+ 下不是 UB（详见 S3-①）；
  ② 【一般】`EV-UB-001` 的 `expected.run` 表述与 `actual` 格式不一致；
  ③ 【建议】把 sanitizer 覆盖不对称写入 M2。
  **三处已全部修正**：补版本边界表 + 换 `i = i++ + ++i` 作真 UB 例子；`expected` 与 `actual`
  格式统一；M2 §2 补"UB 类证据卡必须在 Linux 侧过 sanitizer"、§7 改写灰区判据。
- **第 2 轮（2026-09-10）**：**通过，授予 5 分**。确认版本边界表准确（`f(i++, i++)`：
  C++11/14 = UB / C++17 起 = unspecified）、`i = i++ + ++i` 作为 UB 例子恰当、三处修正到位。
  锚定依据见上方「5 分锚定依据」。

**建议人审重点看三处**：

1. **`f(i++, i++)` 的版本边界**（S3-①，**已被人审纠正过一次**）：执行方最初把任务书**正确**的说法
   改错了——声称 C++17+ 下 `f(i++, i++)` 是 UB。经人审复核：C++17（P0145R3）已把实参初始化改为
   *indeterminately sequenced*，故 **C++17 起是 unspecified，C++11/14 才是 UB**。
   现已按版本边界表改写，并另取 `i = i++ + ++i` 作真正属于"未测序标量修改"的 UB 例子。
   **这是一次"执行方纠错过头"的完整往返**，两层留痕见 S3-①。
2. **"连编译器之间都不一致"的教法**：GCC 六组（跨 7 年版本）一致、Clang 相反——用这个
   **实测出来的矛盾**说明"顺序不是标准规定的"，是否比单纯念标准条文更有说服力？
3. **S6 暴露的覆盖不对称**：`sanitizer` 校验在 Windows 上 `skip`、只在 Linux 真跑 →
   建议把"**UB 类证据卡必须在 Linux 侧过一遍 sanitizer**"写入 M2（本轮已在 WSL 实跑）。

## Clang 列处置（按任务书路线执行 —— 结果：**实测通过，无需降级**）

任务书给了两条路：Clang 编译通过 → 留痕实测；不通过 → 降级"标准条文代替" + 豁免票。
**实测走的是第一条**：

- 为本仓 CI 的 `Gray-zone Matrix` 步补了 `::notice::` 输出（job 日志需 admin 权限，注解可经
  check-runs API 公开读取），随后推送触发 CI。
- **CI 结果**（quality job 全绿）：
  ```text
  [notice] Gray-zone GCC 求值顺序   = h/g/f(1,2)/
  [notice] Gray-zone Clang 求值顺序 = g/h/f(1,2)/
  ```
  → **两个编译器给出相反顺序**，两边 `rc` 均为 0、无 sanitizer 报错。
- **结论**：Clang 列实测成立（满足 M2 "GCC + Clang 双编译器"边界），**不登记豁免票、不标"部分达成"**；
  MSVC 仍按 M2 §2 永久边界以标准条文代替。
- **正面副作用**：这个"相反顺序"把本样板的教学点从"多版本一致 ≠ 可依赖"直接升级为
  "**连编译器之间都不一致**"——比任何文字论述都硬。

## rubric 自评（从几分升到几分，具体补了什么）

| 版本 | 分数 | 判定依据 |
|---|---|---|
| 第 1 步 平庸版 | **2/5** | 把 unspecified 与 UB 混为一谈（定性错误）+ 无证据 + 无边界 + 无"不该做"；外行看完更糊涂 |
| 第 3 步 5 分候选 | **5 分（人审授予，2026-09-10，第 2 轮通过）** | 三条锚逐条对照见下；人审记录见文末"人审轮次记录" |

### 5 分锚定依据（2026-09-10 第 2 轮人审授予）

1. **版本边界精确**——`f(i++, i++)` 明确区分 **C++11/14 = UB** 与 **C++17 起 = unspecified**，
   判据收敛为「*unsequenced*（可重叠 → UB）vs *indeterminately sequenced*（不重叠 → unspecified）」，
   并给出 `i = i++ + ++i` 作跨版本恒为 UB 的对照。
2. **独有洞见**——① **Clang 与 GCC 求值顺序相反的实测**（右→左 vs 左→右，比"多版本一致"硬）；
   ② 「**执行方纠错过头**」的完整往返留痕（把"如何发现自己错了"变成可迁移的判据）；
   ③ **gray_zone 量化偏差**（本书 1478 句中 74.4% 判 UB、仅 6.3% 判 unspecified，"未定义被泛用"可测量）。
3. **行家无硬伤**——标准原文 [expr.call] / [intro.execution] / [basic.lval] 全部核对到条款级；
   双平台复核（Windows sha 轨 + WSL 断言轨含 sanitizer 真跑）；未覆盖项（MSVC）按永久边界明标。

| 锚 | 第 1 步 | 第 3 步 | 具体补了什么 |
|---|---|---|---|
| 外行能懂 | ❌（两类混讲） | ✅ | 一句话判据「标准有没有给合法结果集合」+ 三行对照表；把"未指定"翻译成"顺序不确定**但都合法**" |
| 行家挑不出硬伤 | ❌ | ✅ | 三处定性均给标准条款；两组实验双平台复核（Windows sha 轨 / WSL 断言轨 + sanitizer 真跑 4/4）；**Clang 列已实测**（与 GCC 相反顺序，满足 M2 双编译器边界）；夹具三次自身 UB 全部修掉并留痕；MSVC 按永久边界以标准条文代替 |
| 有别处看不到的洞见 | ❌ | ✅ | ① 用量化数据说话（本书 1478 句里 74.4% 判 UB、6.3% 判 unspecified，**偏差可测量**）；② 用 `-fno-strict-aliasing` 把"优化器利用了 UB"直接翻出来当证伪对照；③ **测序规则在 C++17 变过**：`f(i++, i++)` 由 UB 变 unspecified，而 `i = i++ + ++i` 没变——判据落到 *unsequenced* vs *indeterminately sequenced*；④ 「连编译器之间都不一致」（GCC 右→左 / Clang 左→右） |

### 本轮自证材料（可独立复跑）

```bash
python3 tools/atom_evidence_replay.py --check   # 4 张卡 confirm（MEM-001/002 + UB-001/002）
python3 tools/gray_zone_scan.py                 # 灰色地带分布（本文"74.4% vs 6.3%"的来源）
python3 tools/poison_drill.py                   # 制衡层 4/4
```
