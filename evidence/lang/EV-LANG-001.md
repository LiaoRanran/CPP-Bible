---
id: EV-LANG-001
domain: lang
type: criterion
status: draft
dal: A
verdict: confirm
kind: asm
hypothesis: >-
  inline 函数在两个 TU 中被定义为**不同 token 序列**（违反 [basic.def.odr]/16.4）时，GCC 家族
  **不产生任何诊断**（16.2 属 IFNDR）；且其可观测后果**依赖优化档**：-O0 下未内联，链接器只保留
  同名 weak 符号的一个定义（取先遇到者）→ 程序行为随**链接顺序**改变；-O2 下两 TU 的调用点各自
  内联「自己看到的定义」→ 行为与链接顺序无关。**内部链接（static）孪生对照**证明：顺序依赖来自
  "外部链接 + 未内联时的符号合并"这一机制，而非"两 TU 代码不同"本身。
fixture: Examples/atoms/_atom_inline_odr_main.cpp
command: |
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_a.cpp -o build/_replay_odr_a_O0.o
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_b.cpp -o build/_replay_odr_b_O0.o
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_main.cpp -o build/_replay_odr_main_O0.o
  g++ build/_replay_odr_a_O0.o build/_replay_odr_b_O0.o build/_replay_odr_main_O0.o -o build/_replay_odr_ab_O0.exe && ./build/_replay_odr_ab_O0.exe ab_
  g++ build/_replay_odr_b_O0.o build/_replay_odr_a_O0.o build/_replay_odr_main_O0.o -o build/_replay_odr_ba_O0.exe && ./build/_replay_odr_ba_O0.exe ba_
  g++ -O2 -std=c++23 -c Examples/atoms/_atom_inline_odr_a.cpp -o build/_replay_odr_a_O2.o
  g++ -O2 -std=c++23 -c Examples/atoms/_atom_inline_odr_b.cpp -o build/_replay_odr_b_O2.o
  g++ -O2 -std=c++23 -c Examples/atoms/_atom_inline_odr_main.cpp -o build/_replay_odr_main_O2.o
  g++ build/_replay_odr_a_O2.o build/_replay_odr_b_O2.o build/_replay_odr_main_O2.o -o build/_replay_odr_ab_O2.exe && ./build/_replay_odr_ab_O2.exe o2_
  g++ build/_replay_odr_b_O2.o build/_replay_odr_a_O2.o build/_replay_odr_main_O2.o -o build/_replay_odr_ba_O2.exe && ./build/_replay_odr_ba_O2.exe o2b_
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_static_a.cpp -o build/_replay_ods_a_O0.o
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_static_b.cpp -o build/_replay_ods_b_O0.o
  g++ -O0 -std=c++23 -c Examples/atoms/_atom_inline_odr_static_main.cpp -o build/_replay_ods_main_O0.o
  g++ build/_replay_ods_a_O0.o build/_replay_ods_b_O0.o build/_replay_ods_main_O0.o -o build/_replay_ods_ab.exe && ./build/_replay_ods_ab.exe stO0_
  g++ build/_replay_ods_b_O0.o build/_replay_ods_a_O0.o build/_replay_ods_main_O0.o -o build/_replay_ods_ba.exe && ./build/_replay_ods_ba.exe stO0b_
  g++ -O2 -std=c++23 -Wall -Wextra -Werror -c Examples/atoms/_atom_inline_odr_a.cpp -o build/_replay_odr_diag_a.o
  g++ -O2 -std=c++23 -Wall -Wextra -Werror -c Examples/atoms/_atom_inline_odr_b.cpp -o build/_replay_odr_diag_b.o
  g++ -O2 -std=c++23 -Wall -Wextra -Werror -c Examples/atoms/_atom_inline_odr_main.cpp -o build/_replay_odr_diag_main.o
  g++ -O2 -std=c++23 -S Examples/atoms/_atom_inline_odr_a.cpp -o Examples/atoms/_atom_inline_odr_a.asm
artifact: Examples/atoms/_atom_inline_odr_a.asm
artifact_sha256: 63c7e3b73ea9646cbad081ba6b8c0a5ad6e5b77f780aebf944ffd65ba15fbc9f
artifact_compiler: GCC 15.3.0 (MinGW-w64)
serves: [ATOM-LANG-INLINE-001]
relations: []
evidence: []
controlled_vars:
  - 自变量三元组: ①定义同一性（固定为「不同」：TU A = `return 1;` / TU B = `return 2;`）②链接顺序（a b / b a）③优化档（-O0 / -O2）
  - 活性对照: `stable_fn`（两 TU 定义 token 序列相同）→ 在全部 4 组中恒 42（噪声下限，见 §2 读数分级）
  - 机制判别对照: **内部链接孪生**（`static inline`，其余构造同实验组）→ 若顺序依赖确由「外部链接弱符号合并」造成，孪生必须在两顺序下读数相同（§4 实测）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
  sanitizer_note: "本卡**不**以 sanitizer 为判据：ASan/UBSan 对 ODR 违反不敏感（本卡主动声明的检测边界，见 §6）"
actual:
  run_match_file: Examples/atoms/_atom_inline_odr.out
  run_match_keys:
    - ab_tu_a
    - ab_tu_b
    - ab_stable_a
    - ab_stable_b
    - ba_tu_a
    - ba_tu_b
    - ba_stable_a
    - ba_stable_b
    - o2_tu_a
    - o2_tu_b
    - o2_stable_a
    - o2_stable_b
    - o2b_tu_a
    - o2b_tu_b
    - o2b_stable_a
    - o2b_stable_b
    - stO0_sa
    - stO0_sb
    - stO0b_sa
    - stO0b_sb
artifact_assert:
  - {kind: contains_in, symbol: "_Z10tu_a_valuev", text: "movl $1, %eax"}
  - {kind: absent_in, symbol: "_Z10tu_a_valuev", text: "call"}
  - {kind: contains_in, symbol: "_Z11tu_a_stablev", text: "movl $42, %eax"}
  - {kind: call_count, symbols: ["_Z10tu_a_valuev", "_Z11tu_a_stablev"], max: 0}
falsification: |
  若以下任一发生，判 refute：
  1. 「零诊断」由 `-Werror` 承担：三条 `-Wall -Wextra -Werror` 编译**任一 rc≠0**（即编译器发出警告或
     错误）→ IFNDR 的"无须诊断"被否（注：不带 `-Werror` 时警告不影响 rc，故判据必须带 `-Werror`）；
  2. `-O0` 两种链接顺序输出相同（ab_tu_* 与 ba_tu_* 相等）→ 「未内联时链接器取其一」被否；
  3. **机制判别对照失败**：内部链接孪生在 `-O0` 两顺序下读数**不同**（stO0_sa≠stO0b_sa）→
     「顺序依赖来自弱符号合并」这一机制解释被否（须改写机制章）；
  4. 对照组 `*_stable_*` 不恒为 42 → 夹具存在未控住的混淆变量，实验作废；
  5. `-O2` 两顺序读数不同（o2_* 与 o2b_* 不等）→ 「内联后与链接顺序无关」被否；
  6. `-O2` 组出现 `o2_tu_a == o2_tu_b` → 未按预期内联（该组若也"取其一"，说明内联未发生，须查明）；
  7. `_atom_inline_odr_a.asm` 缺 `_Z10tu_a_valuev` → 工件与夹具不同代。
expected: |
  20 项读数分两类（**非恒真 12 项承担主证，恒真 8 项只作噪声下限**）：
  【主证 12】`-O0`：ab_tu_a==ab_tu_b==1、ba_tu_a==ba_tu_b==2（取其一 ⇒ 随顺序变）；
  `-O2`：o2_tu_a==o2b_tu_a==1、o2_tu_b==o2b_tu_b==2（各自内联 ⇒ 顺序无关）；
  内部链接孪生：stO0_sa==stO0b_sa==1、stO0_sb==stO0b_sb==2（**顺序无关** ⇒ 机制判别）。
  【恒真 8】四处 *_stable_* 恒 42（对被测机制零响应，仅证明夹具框架未漂移）。
  另：三条 `-Wall -Wextra -Werror` 编译 rc=0 且零输出（零诊断）。
---

# EV-LANG-001 · ODR 违反的判别实验：两个 TU 的定义不同 ⇒ 行为随链接顺序 / 优化档改变

## §0 选题：为什么这个实验能支撑 claim

`ATOM-LANG-INLINE-001` 的 claim 是「inline 函数的多个定义必须 token 序列相同；违反是**无须诊断**的
未定义行为」。这句话有两个可被独立检验的硬点，本卡锚它们：

1. **零诊断**：编译器/链接器**不会**告诉你它发现了两个不同的定义（16.2 属 IFNDR）；
2. **行为可见地不确定**：同一个程序，仅改**链接顺序**（`-O0`）或仅改**优化档**（`-O2`），输出就变——
   这是"存在两个互斥定义"的**运行时证据**，且**不需要 sanitizer**（见 §6）。

## §1 夹具设计（多 TU，本仓首例）

| 文件 | 角色 |
|---|---|
| `_atom_inline_odr_shared.h` | 共享头：`inline int odr_fn() { return ODR_VALUE; }`（实验组）+ `inline int stable_fn() { return 42; }`（活性对照） |
| `_atom_inline_odr_a.cpp` / `_b.cpp` | TU A：`#define ODR_VALUE 1`；TU B：`#define ODR_VALUE 2`（**定义不同 ⇒ 违反 ODR**） |
| `_atom_inline_odr_main.cpp` | 观测点：接收 `argv[1]` 前缀，打印 `tu_a/tu_b/stable_a/stable_b` |
| `_atom_inline_odr_static_a.cpp` / `_b.cpp` / `_static_main.cpp` | **机制判别对照**（内部链接孪生）：`static inline int sfn(){return 1/2;}`，其余构造同实验组；`sfn` 为内部链接 ⇒ 两 TU 各持一份、**不发生弱符号合并** |

**自变量三元组**：①定义同一性（固定"不同"）②链接顺序（`a b` / `b a`）③优化档（`-O0` / `-O2`）。
对照有两层：**活性对照** `stable_fn`（定义相同 ⇒ 排除"顺序本身扰动框架"）；**机制判别对照** 内部链接孪生
（排除"两 TU 代码不同"这一泛化解释，见 §4）。

## §2 实测矩阵（2026-09-12）

| 实验 | 变量 | MinGW GCC 15.3 | WSL GCC 13.3 |
|---|---|---|---|
| E1 | `-O0`，顺序 `a b` | `tu_a=1 tu_b=1` | `tu_a=1 tu_b=1` |
| E2 | `-O0`，顺序 `b a` | `tu_a=2 tu_b=2` | `tu_a=2 tu_b=2` |
| E3 | `-O2`，顺序 `a b` | `tu_a=1 tu_b=2` | `tu_a=1 tu_b=2` |
| E4 | `-O2`，顺序 `b a` | `tu_a=1 tu_b=2` | `tu_a=1 tu_b=2` |
| C1 | 活性对照（四组） | `stable=42/42` | `stable=42/42` |
| D1 | `-Wall -Wextra -Werror` 三条编译 | **rc=0，零输出** | **rc=0，零输出** |

## §3 工件证据

`_atom_inline_odr_a.asm`（`-O2`）中 `_Z10tu_a_valuev` 的函数体为 `movl $1, %eax`——TU A 的调用点
**内联了自己看到的定义**（与 E3 的 `tu_a=1` 互证）；`_b.asm` 同位置为 `movl $2`（对应 `tu_b=2`）。
`_atom_inline_odr_main.asm` 的 `main` 对四个包装函数各有一条 `call`（跨 TU 调用未内联），是"观测点不在
同一 TU"的结构证据。

> **本卡机器断言的判别力声明（2026-09-12 W2 修复后重写）**：`artifact_assert` 四条——
> ① `contains_in … "movl $1, %eax"`：TU A 中 `odr_fn()` 被常量折叠并**内联**进 `tu_a_value` 的
> 直接工件证据（若内联未发生，函数体内是 `call` 而非立即数 → refute）；② `absent_in … "call"`：
> 同一函数区间的否定证据——**内联与否是质变**，不随指令选择/寄存器分配漂移，跨编译器稳健；
> ③ 活性对照 `stable_fn` 的 `movl $42, %eax`；④ `call_count … max: 0`：本 TU 是这两个包装函数的
> **定义方**，不应出现对它们的调用点。
>
> 关于 ④ **不违反原段落对 `call_count` 的顾虑**：漂移的是**精确次数**（实测 3 vs 4），而 `max: 0`
> 锚的是**"有无调用"的质变**——内联成立时任何编译器都产生 0 个调用点，故阈值形态跨编译器稳健
> （此即 W2 对断言引擎的扩展：`min`/`max` 区间语义，见 `tools/atom_evidence_replay.py`）。
> ①–④ 均两平台实测成立（MinGW GCC 15.3 / WSL GCC 13.3）。
>
> **修复背景（诚实记录）**：本卡原有两条 `{contains_in, symbol: …, scope: file}` —— `scope` 是引擎
> **从未支持**的键（被静默忽略）且缺 `text`，而空 `text` 的 `str.count("")` 恒为 `len+1 > 0`，
> 故两条断言实际退化为**恒真断言**（零校验，比无断言更隐蔽）。引擎已补参数完备性检查
> （缺参/未知键一律判失败，见 `_ASSERT_ALLOWED_KEYS`），断言随之改为上述真实锚。
> 同批修复另 5 张卡（CONC-003/004/005/006、LANG-002）的同型失效断言。

## §4 机制判别对照：内部链接孪生（本轮红队要求补做的强对照）

| 构造 | 链接属性 | `-O0` 顺序 `a b` | `-O0` 顺序 `b a` | 判读 |
|---|---|---|---|---|
| 实验组 `odr_fn`（`inline`） | **外部** | `tu_a=1 tu_b=1` | `tu_a=2 tu_b=2` | **顺序依赖**（weak 符号合并取其一） |
| 孪生 `sfn`（`static inline`） | **内部** | `stO0_sa=1 stO0_sb=2` | `stO0b_sa=1 stO0b_sb=2` | **顺序无关**（各持一份，无合并） |

**唯一差异 = 链接属性**（外部 vs 内部）⇒ 顺序依赖确实来自"外部链接 symbol 在未内联时被合并"，
而不是"两个 TU 代码不同"这种泛化说法。机制解释由此从**演绎**升级为**实测对照**。

## §5 双平台复核记录

| 平台 | 命令 | 结果 |
|---|---|---|
| Windows（MinGW GCC 15.3） | `python tools/atom_evidence_replay.py --check --card evidence/lang/EV-LANG-001.md --card evidence/lang/EV-LANG-002.md` | `confirm=2 refute=0 infra_error=0`；`artifact_sha` 命中卡值；20/8 个 key 逐字一致 |
| WSL（Ubuntu GCC 13.3，= CI 同版） | 同上 | `confirm=2 refute=0 infra_error=0`；走 `artifact_assert` 结构断言（2 条全过）；20/8 个 key 逐字一致 |

⇒ 本卡的双编译器结论**不再是"只在开发机跑过"**：两侧 replay 均已实跑通过（复核者按上表命令可自行复现）。

## §6 反例与边界

- **不得用 sanitizer 判本卡**：ASan/UBSan 对 ODR 违反不敏感；本实验的可观测性来自链接顺序与内联决策。
  这是**主动声明的检测边界**——勿以"sanitizer 没报"反推"没问题"，也勿以"没跑 sanitizer"判本卡不成立。
- **活性和机制对照的判别力**：`stable_fn` 四组恒 42（噪声下限）；孪生对照（§4）才是机制判别的主力。
- **标准措辞**：原文为「consist of the same **sequence of tokens**」（[basic.def.odr]/16.4），**不是**
  字符级"逐字相同"（空白与注释不属于 token）。预测冻结文件写作"逐字相同"系口语化措辞，**此处显式修正**；
  冻结文件本身按纪律不改。
- **标准引用版本**：条款按 C++20 起的编号写作 `[basic.def.odr]/16.2`（IFNDR 判定）、`/16.4`（token 序列
  要求）、`/18`（如同单一定义）；引用的**稳定名** `[ifndr:basic.def.odr.definition.matches]` 与版本无关，
  是主锚。C++17 及更早的段号不同（`/16.x` 体系自 C++20 模块措辞并入后形成）。
- **实测范围**：仅 `-std=c++23`、GCC 15.3/13.3、x86-64；`standard` 列表中的其他版本未实测。

## §7 本卡暴露的系统问题（锚必填口径）

| # | 问题 | 严重度 | 复现 | 建议 |
|---|---|---|---|---|
| S1 | `artifact` / `artifact_sha256` 是**单产物**字段：多 TU 产出 3 个 `.asm`（a/b/main），只能锚 1 个 | warn | `command` 产出 3 个 `.asm`；`gate_engine.py --list` 无多产物规则 | 加 `artifacts[]` 或明确"主工件 + 其余仅留痕"口径 |
| S2 | `contains_in` 只能锚**符号存在性**，无法断言函数体内 `movl $1`（内联证据）；本卡因此只能给"最低锚 + 正文留痕" | warn | `atom_evidence_replay.py` 的 contain 分支；`EV-CONC-004 §2` 同遇 | 扩展断言种类或固化"正文留痕"口径；`call_count` 因跨编译器漂移（`EV-MEM-001`）不宜替代 |
| S3 | 夹具/卡**行尾不统一**：既有 `Examples/atoms/` 与 `evidence/conc/` 为 CRLF，本批新增文件为 LF，仓库无 `.gitattributes` | advice | `git ls-files --eol Examples/atoms/` | 加 `.gitattributes` 或登记豁免 |
| S4 | 两张证据卡共用同一 `.out`，各自取 keys 子集；无机制检查跨卡 keys 重叠 | advice | `EV-LANG-001/002` 的 `run_match_file` 相同 | 规模增长后加 keys 归属登记 |
| S5 | **预期暴露项未暴露（正向结论）**：预判"`command` 可能不支持多文件构建"——实测**支持**（21 行命令、6 次链接全部复现） | — | 本卡 `command`；replay 双平台 confirm | 无需修 |
| S6 | **`falsification` 的"零诊断"判据必须显式带 `-Werror` 才可机器判定**（replay 只看 rc，警告不影响 rc） | advice | 本卡 `command` 第 16–18 行；`atom_evidence_replay.py` 的 compile_rc 判定 | 建议在 `docs/kernel/M2_empirical.md` 补一句体裁约定：凡"无警告"类判据须用 `-Werror` 落地 |

## §8 修订记录

- v1（本稿）：MCC 首次落地；多 TU 夹具。
- v2（红队第一轮后）：①falsification 第 1 条改用 `-Werror`（原判据不可机器判定）；②补**内部链接孪生**
  机制判别对照（§4，把演绎升级为实测）；③读数分级（12 主证 / 8 恒真）；④补双平台复核记录（§5）；
  ⑤标准引用精确化（`/16.2` vs `/16.4` 的分工 + 稳定名为主锚 + 版本说明）；⑥断言判别力诚实声明（§3）。
