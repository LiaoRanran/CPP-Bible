---
id: EV-LANG-002
domain: lang
type: criterion
status: draft
dal: A
verdict: confirm
kind: asm
hypothesis: >-
  ODR 违反的**可观测形态由内联决策主导**：未内联（-O0）时两个同名定义经链接器合并（取先遇到者），
  行为随**链接顺序**改变；内联发生（-O2）时两个 TU 各自内联「自己看到的定义」，行为与链接顺序**无关**。
  即"这个 UB 长什么样"是**优化档的函数**——同一份源码、同一组定义差异，仅换档位即换形态。
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
  g++ -O2 -std=c++23 -S Examples/atoms/_atom_inline_odr_a.cpp -o Examples/atoms/_atom_inline_odr_a.asm
artifact: Examples/atoms/_atom_inline_odr_a.asm
artifact_sha256: 63c7e3b73ea9646cbad081ba6b8c0a5ad6e5b77f780aebf944ffd65ba15fbc9f
artifact_compiler: GCC 15.3.0 (MinGW-w64)
serves: [ATOM-LANG-INLINE-001]
relations: []
evidence: []
controlled_vars:
  - 唯一变量: 优化档（-O0 vs -O2）；定义差异固定为「TU A 看到 return 1 / TU B 看到 return 2」
  - 活性对照: 两档位下对照组 stable_fn（两 TU 定义 token 序列相同）均恒 42 ⇒ 换档位本身不改变合规代码
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
actual:
  run_match_file: Examples/atoms/_atom_inline_odr.out
  run_match_keys:
    - ab_tu_a
    - ab_tu_b
    - ba_tu_a
    - ba_tu_b
    - o2_tu_a
    - o2_tu_b
    - o2b_tu_a
    - o2b_tu_b
artifact_assert:
  - {kind: contains_in, symbol: "_Z10tu_a_valuev", scope: file}
falsification: |
  若以下任一发生，判 refute：
  1. `-O0` 两链接顺序输出相同（ab_tu_a == ba_tu_a）→「未内联时链接器取其一」被否；
  2. `-O2` 两链接顺序输出不同（o2_tu_b != o2b_tu_b）→「内联后与顺序无关」被否；
  3. `-O2` 组出现 o2_tu_a == o2_tu_b → 未按预期内联，须先排除夹具被优化掉（这一组若"取其一"，说明内联未发生）；
  4. `_atom_inline_odr_a.asm` 缺 `_Z10tu_a_valuev` → 工件与夹具不同代。
expected: |
  `-O0`：ab_tu_a==ab_tu_b==1 且 ba_tu_a==ba_tu_b==2（链接器取先遇到的定义 ⇒ 随顺序变）；
  `-O2`：o2_tu_a==o2b_tu_a==1 且 o2_tu_b==o2b_tu_b==2（各自内联 ⇒ 与顺序无关）；
  两档位下 stable 均恒 42（换档位不改变合规代码）。
---

# EV-LANG-002 · 同一 UB 的两种形态：优化档是"可观测行为"的第二变量

## §0 选题：为什么这个实验能支撑 claim

`ATOM-LANG-INLINE-001` 说 ODR 违反"行为不可预测"。若只给一条"顺序变了结果就变"的证据，读者容易
得出**错的推广**："只要固定链接顺序就没事了"。本卡补上第二组事实：

> **同一份源码、同一组定义差异**，仅把优化档从 `-O0` 换到 `-O2`，可观测形态就从"取其一（顺序依赖）"
> 变成"各用各的（顺序无关）"——**两个形态都是同一个 UB 的合法实现**。

所以"固定链接顺序"**不是**规避手段：它只挡住了 `-O0` 那一支。这条对照是本卡与 `EV-LANG-001` 的分工：
001 立"顺序依赖"，002 立"档位决定形态"。

## §1 实测矩阵（2026-09-12，双编译器交叉一致）

| 档位 \ 链接顺序 | `a b` | `b a` | 判读 |
|---|---|---|---|
| `-O0` | `tu_a=1 tu_b=1` | `tu_a=2 tu_b=2` | **顺序依赖**（链接器取先遇到的 weak 定义，未内联） |
| `-O2` | `tu_a=1 tu_b=2` | `tu_a=1 tu_b=2` | **顺序无关**（两个 TU 各自内联自己看到的定义） |
| 对照组 `stable`（两档 × 两序） | 42/42 | 42/42 | 恒 42（换档位/换顺序均不影响合规代码） |

MinGW GCC 15.3 与 WSL GCC 13.3 **四组读数完全一致**（见 `EV-LANG-001` §2 的同源矩阵）。

> **与 `EV-LANG-001` 的分工**：001 立「顺序依赖」（`-O0` 两顺序）+ **机制判别对照**（内部链接孪生，
> 001 §4）；本卡立「档位决定形态」（`-O0` 取其一 vs `-O2` 各用各的）。两卡共用同一 `.out` 与同一组
> 命令、keys 各取子集（该共用关系的风险见 §4 S4）。

## §2 工件侧印证

`_atom_inline_odr_a.asm`（`-O2`）中 `_Z10tu_a_valuev` 的函数体为 `movl $1, %eax`——TU A 的
`odr_fn` 在 `-O2` 下被内联为常量 `1`，与 §1 的 `o2_tu_a=1` 互相印证（"各用自己看到的定义"）。

## §3 边界

- **不是"两档位任选其一都安全"**：两个形态都是 UB 的表现，标准不保证任一形态稳定可移植
  （换编译器/链接器/ISM 实现都可能在两形态间跳变）。
- **不得据此推出"`-O2` 更安全"**：`-O2` 的"顺序无关"只是本例在内联发生时的表现；若函数体大到
  不被内联，`-O2` 同样会退化为"取其一"（本卡把它写进 falsification 第 3 条的反方向）。

## §4 本卡暴露的系统问题（锚必填口径）

| # | 问题 | 严重度 | 复现 | 建议 |
|---|---|---|---|---|
| S4 | 两张证据卡（001/002）**共用同一 `.out` 与同一组实验**，各自取 `run_match_keys` 子集；无机制检查两卡 keys 是否重复或互相矛盾 | advice | 本卡与 `EV-LANG-001` 的 `actual.run_match_file` 同为 `_atom_inline_odr.out` | 若卡数增长，可加"同一 `.out` 的 keys 归属登记"；当前规模下可接受 |
| S5 | `-O0`/`-O2` 两组读数**在同一 `.out` 内以不同前缀并存**，这是本项目首次把"对照组"做成可断言读数（此前对照组多写在正文） | advice | 本卡 `run_match_keys` 8 项全部来自同一 `.out` | 可作为"对照组进 actual"的范式，供后续卡参考 |

## §5 修订记录

- v1（本稿）：MCC 六步首次落地；与 `EV-LANG-001` 同源夹具、分工锚定（顺序依赖 / 档位形态）。
