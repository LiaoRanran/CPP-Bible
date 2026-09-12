---
id: ATOM-LANG-INLINE-001
title: inline 函数的定义必须跨 TU 一致：违反 ODR 是「无须诊断」的 UB，且形态由链接顺序与优化档决定
domain: LANG
type: rule
status: draft
dal: A
human_review: required
status_history:
  - {level: draft, at: 2026-09-12, by: writer:agent}
audience: intermediate
cognitive_load: high
prerequisites_readable: true
claim: >-
  `inline` 函数（及变量）的定义可以出现在**多个翻译单元**，但各定义必须由**相同的 token 序列**构成
  （[basic.def.odr]/16.4）；违反属 ill-formed, **no diagnostic required**——实测 GCC 家族**零诊断**，
  且**当两个定义的可观测结果不同时**，其可观测行为由**链接顺序**与**优化档**共同决定：-O0（未内联）下链接器只保留同名符号的一个定义
  （取先遇到的），行为随链接顺序改变；-O2（内联发生）下各 TU 内联「自己看到的定义」，行为与链接顺序
  无关、两个值并列出现。
claim_boundary:
  standard: [C++11, C++14, C++17, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (Linux)]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64, x86-64 Linux]
  n_a: >-
    ①实测限 GCC 家族两版本两平台；Clang/MSVC 未实测（按标准同为 IFNDR，但"取其一 vs 各用各"的
    具体映射未验证）。②"token 序列相同"不等于"语义相同"：空白与注释不属于 token，除此之外
    任何差异（含宏展开后的 token 差异）都越界。③本卡不覆盖模板/类定义的多 TU 情形（同一条款的
    其他分支）。④`1/1` 与 `1/2` 是**实现映射**，不是标准保证的行为。
relations:
  - {type: contrasts, target: ATOM-UB-GRAY-001}
evidence:
  - EV-LANG-001
  - EV-LANG-002
sources:
  - {kind: iso, ref: "ISO/IEC 14882 [basic.def.odr]/16.4（同一实体的所有定义须 consist of the same sequence of tokens）；稳定名 [ifndr:basic.def.odr.definition.matches]（违反为 IFNDR，仅具名模块实体才要求诊断）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882 [basic.def.odr]/18（含多个定义的实体，行为如同「single entity with a single definition」）", independent: true}
  - {kind: cppreference, ref: "One Definition Rule —— 多 TU 中 inline 函数/变量的定义必须 token 级一致；违反为 ill-formed, no diagnostic required", independent: true}
first_hand: true
superiority: >-
  通行教材只写"inline 函数可以在多个 TU 里定义"，把"必须完全一致"一句带过，且几乎从**不展示违反的
  可观测后果**——读者于是形成"这规则靠自觉"的印象。本卡的三点增量：①把"**零诊断**"做成实测
  （`-Wall -Wextra` 编译两个不同定义的 TU，输出为空）；②把"行为不可预测"落成**两个可复现的确定性
  观测**（仅换链接顺序 → `1/1` 变 `2/2`；仅换优化档 → 变 `1/2` 且顺序无关），并做成 **20 项机器可
  断言读数**（其中 **12 项非恒真主证 + 8 项恒真对照**，同一 `.out` 内并存；恒真项只作噪声下限，
  不充当证据强度）；③给出反直觉推论——**"固定链接顺序"不是解药**（`-O2` 那支
  换形态），这是把"UB"从口号变成可操作判据的关键一步。
depth:
  layer: asm
  drill_note: >-
    `_atom_inline_odr_a.asm`（-O2）中 `_Z10tu_a_valuev` 的函数体为 `movl $1, %eax`——即 TU A 的调用点
    已把 `odr_fn` **内联为常量 1**（与本卡 -O2 组 `tu_a=1` 互相印证）；而 `_atom_inline_odr_main.asm`
    的 `main` 中对四个包装函数各有一条 `call`（跨 TU 调用未内联），是"观测点不在同一 TU"的结构证据。
    -O0 组因未内联，符号经链接器合并 ⇒ 交换 .o 顺序即换定义 ⇒ 读数改变。
pedagogy:
  motivation: "一个 inline 函数、两个 TU 写了不同实现——编译器一声不吭，程序却随链接顺序给出两个答案。"
  misconceptions: [MIS-LANG-001]
  socratic:
    - "编译器为什么不能报错？（它一次只看到一个 TU——那链接器呢？它只看到符号名，看不到函数体。）"
    - "如果固定链接顺序就安全了，那换到 -O2 为什么形态又变了？"
  predict_first: "先预测：把两个 .o 的链接顺序对调，输出会变吗？再预测：改成 -O2 呢？（先写答案，再看 EV-LANG-001 的 16 项读数。）"
misconceptions: [MIS-LANG-001]
---

## 论断

**`inline` 函数的定义可以出现在多个 TU，但必须由相同的 token 序列构成；违反是「无须诊断」的 UB——
编译器不会告诉你，而程序会按链接顺序与优化档给出不同的答案。**

```cpp
// 两个 TU 都 include 这个头，但各自先定义了不同的 ODR_VALUE：
inline int odr_fn() { return ODR_VALUE; }   // TU A 展开成 return 1;，TU B 展开成 return 2;
```

编译两个 TU、链接成一个程序，`-Wall -Wextra` **零警告零错误**；而：

| 档位 \ 链接顺序 | `a b` | `b a` |
|---|---|---|
| `-O0` | `tu_a=1 tu_b=1` | `tu_a=2 tu_b=2` |
| `-O2` | `tu_a=1 tu_b=2` | `tu_a=1 tu_b=2` |
| 对照 `stable_fn`（两侧定义相同） | 42 / 42 | 42 / 42 |

**同一份源码**，只动链接顺序或优化档，就是**三个不同的程序**。而按标准，这甚至不要求编译器说一句话。

## 为什么（机制）

- **编译期看不到**：编译器一次只处理一个 TU，无从比较两个 TU 的定义；
- **链接期看不到函数体**：链接器只看到**符号名**（weak 定义），不解析函数体，自然无法判定"两个定义是否 token 相同"；
- **标准的选择**：`[basic.def.odr]/16.2` 把这类违反定为 **IFNDR**（ill-formed, no diagnostic required）——
  只有在具名模块（named module）场景下才强制要求诊断。于是在传统多 TU 编译模型里，"不报"是**合规行为**；
- **`/18` 不能被读成"两形态都受标准背书"**：那句 "as if there is a single entity with a single definition"
  是**对合规程序**的描述；本卡的程序是 IFNDR，**不获得任何保证**。实测的两种形态（`1/1` 取其一、
  `1/2` 各用各的）都是**实现行为**——没有标准条文为它们"选定"哪一个，换编译器/链接器/实现即可能
  在两形态间跳变。换言之：`o2_tu_a=1, o2_tu_b=2` 恰恰意味着"像两个实体"，**不是**"如同单一定义"。

## MCC 留痕（371 首次真实落地 · 六步）

1. **异常附证据**：现象 = "两个 TU 定义不同 ⇒ 零诊断 + 输出随链接顺序变"。附实测：`-Wall -Wextra` 三条
   编译**零输出**；`-O0` 顺序 `a b` → `1/1`，顺序 `b a` → `2/2`（双编译器一致，见 EV-LANG-001 §2）。
   先排工具假象：确认 `.o` 确实重新生成（每次实验前重编译）、`g++ --version` 为 15.3.0 / 13.3.0、
   且输出前缀参数生效（`ab_` / `ba_` 区分两次运行）。
2. **≥2 假设含 ≥1 反直觉**：H1（直觉）——"编译器/链接器会发现并报错"；**H2（反直觉）**——"不报错是标准
   规定（IFNDR），且行为随链接顺序改变"；H3（备选）——"`-O2` 下完全内联，于是形态变成『各用各的』、
   与顺序无关"。
3. **预言冻结**：`docs/kernel/371_预言冻结_ATOM-LANG-INLINE-001.md`（实验前单独 commit，git 时间戳为见证）。
   **命中情况**：E1 预言 `1/1` ✓、E2 预言 `2/2` ✓、E3/E4 预言"两分支均合法"✓（实测 H3 分支）、C1 预言恒 42 ✓。
   唯一措辞修正：预言文件写"逐字相同"，标准原文为 **token 序列相同**（本卡 §边界已显式记录，冻结文件按纪律不改）。
4. **判别实验**：自变量三元组 = {定义同一性（固定"不同"）、链接顺序、优化档}；**活性对照** = `stable_fn`
   （两侧定义相同 ⇒ 恒 42）；**机制判别对照** = 内部链接孪生（`static inline`，其余构造同）——红队指出
   原稿仅用**演绎**排除"内部链接"假设，本轮补做**实测**（`EV-LANG-001 §4`）；有界（无循环、无网络、
   单次 <1s）；断言候选先在 Linux `.asm` 中 grep 实测存在（`_Z10tu_a_valuev` / `_Z11tu_a_stablev` 双端均在）。
5. **盲裁决**（中性标签 + ≥3 替代解释，逐条排除见下）；读数不标注"谁的定义"，只标 TU 编号与顺序。
6. **固化/证伪**：H2/H3 存活 → 本卡 + `EV-LANG-001`/`EV-LANG-002`；**H1 被否** → 入误解库 `MIS-LANG-001`。

### 第 5 步的替代解释与排除

| # | 替代解释 | 排除方式 |
|---|---|---|
| A1 | "两个 TU 的 `odr_fn` 其实各自是内部链接（static 语义）⇒ 本来各用各的" | **实测对照**（非演绎）：内部链接孪生（`static inline`，其余构造同）在同一 `-O0` 两顺序下**恒为** `sa=1 sb=2`（顺序无关），而实验组顺序依赖 ⇒ 两者链接属性确实不同。**排除**（详见 `EV-LANG-001 §4`） |
| A2 | "输出变化来自『链接顺序』本身，与定义是否相同无关" | 对照组 `stable_fn`（两侧定义相同）在同样的两种顺序下**恒 42**。**排除**（顺序本身无害） |
| A3 | "差异来自我改动了源码（两个 `.cpp` 内容不同）" | 两个 `.cpp` 的差异**正是**"定义不同"的载体；唯一变量按设计就是"定义是否 token 相同"。**这是实验意图，不是混淆** |
| A4 | "这是某个编译器的 bug" | IFNDR 是标准允许的（`[ifndr:basic.def.odr.definition.matches]`）；且 MinGW 15.3 与 Linux 13.3 **双编译器等值复现**。**排除** |

## 边界（不覆盖什么）

- 只实测 **GCC 家族两版本两平台**；Clang/MSVC 未测（标准同为 IFNDR，但具体映射未验证）；
- **不等同**于"模板/类的多 TU 定义"（同一条款其他分支）；
- `1/1`、`2/2`、`1/2` 三种读数是**实现映射**，不是标准保证——标准只说"不要求诊断、行为无保证"；
- "token 序列相同"**不是**"语义相同"：除空白/注释外的任何 token 差异（含宏展开结果）都越界。

## 本颗原子暴露的系统问题（锚必填口径 · 371 交付物）

| # | 问题描述 | 严重度 | 复现方式 | 建议修法 |
|---|---|---|---|---|
| S1 | `artifact` / `artifact_sha256` 是**单产物**字段，而多 TU 一次产出 3 个 `.asm`（a/b/main），卡只能锚 1 个，另两个无字段可登记 | warn | 本卡 `command` 产出 3 个 `.asm`；`gate_engine.py --list` 无多产物规则 | 加 `artifacts[]` 或在 `G1_layout.md §3` 明确"主工件 + 其余仅留痕"口径 |
| S2 | `contains_in` 只能锚**符号存在性**，无法断言"函数体内出现 `movl $1`"（内联证据） | warn | `atom_evidence_replay.py` 的 contain 分支仅查符号；`EV-CONC-004 §2` 已遇同类 | 扩展断言种类（如 `contains_text_in_function`）或固化"正文留痕"口径 |
| S3 | 夹具/卡**行尾不统一**：既有 `Examples/atoms/` 与 `evidence/conc/` 为 CRLF（99 个文件 `i/crlf`），本批新增文件为 LF，仓库无 `.gitattributes` | advice | `git ls-files --eol Examples/atoms/`；`git ls-files --eol evidence/` | 加 `.gitattributes`（`* text=auto eol=lf`）或显式登记豁免 |
| S4 | 两张证据卡共用同一 `.out`（`_atom_inline_odr.out`），各自取 keys 子集；无机制检查跨卡 keys 重叠/矛盾 | advice | `EV-LANG-001` 与 `EV-LANG-002` 的 `actual.run_match_file` 相同 | 规模增长后加"同一 `.out` 的 keys 归属登记" |
| S5 | **预期暴露项未暴露（正向结论）**：371 选题时预判"`command` 可能不支持多文件构建"——实测**支持**（21 行命令、6 次链接，20 项读数全部复现成功） | — | 本卡 `command`；replay 本地双平台 `confirm=2` | 无需修；记录为"该处系统比预期健壮" |
| S6 | `falsification` 中"无警告/零诊断"类判据**必须显式用 `-Werror`** 才可机器判定（replay 的 `compile_rc` 只看 rc，警告不影响 rc） | advice | 证据 `EV-LANG-001 §7 S6`；本卡 `command` 第 16–18 行 | 建议在 `docs/kernel/M2_empirical.md` 补一句体裁约定 |
| S7 | 371 冻结文件 §0 预判的"『UB 必须有 sanitizer 证据』隐含假设"**已确认成立**：ASan/UBSan 对 ODR 违反不敏感，本卡主动声明该边界 | advice | 冻结文件 `371_预言冻结_ATOM-LANG-INLINE-001.md`；`EV-LANG-001 §6` | 已按边界声明处理；未来若加 sanitizer 维须先验证其对 ODR 的敏感性 |

## 修订记录

- v1（本稿）：371 MCC 六步首次真实落地（`lang` 域首颗）；预言冻结见
  `docs/kernel/371_预言冻结_ATOM-LANG-INLINE-001.md`；证据 `EV-LANG-001`/`EV-LANG-002`；误解 `MIS-LANG-001`。
- v2（红队第一轮后）：①删去"两形态都符合 `/18`『如同单一定义』"的错误法理表述（被 `o2_tu_a=1,tu_b=2`
  反证，且与冻结文件红线冲突）——改为"IFNDR 程序不获得任何保证，两形态均为实现行为"；②claim 因果
  加限定"**当两个定义的可观测结果不同时**"；③补**内部链接孪生**实测对照（机制判别，A1 排除由演绎
  升级为实测）；④证据强度诚实化（20 项 = 12 主证 + 8 恒真对照）；⑤S 表补 S6/S7。
