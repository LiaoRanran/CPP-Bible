---
id: EV-UB-002
serves: [ATOM-UB-GRAY-001]      # G4 样板 B 配套证据（灰区判据原子）；人审通过原子化时启用
status: example                  # example：样板配套证据，随样板一并人审
kind: asm                        # run（自洽性观测）+ asm（优化器假定不别名的铁证）
hypothesis: >-
  通过不兼容类型指针访问对象（严格别名）是**未定义行为**：优化器会假定不同类型的指针不指向同一
  对象，并据此**消除对同一对象的再次读取**——该假设在 -O2 下默认启用，在 -fno-strict-aliasing
  下关闭。
controlled_vars: >-
  同一 TU、同一编译器、同一优化档；唯一变量 = 是否启用严格别名假设
  （对比组：`-O2` 默认 vs `-O2 -fno-strict-aliasing`；另加 `-O0` 说明"无优化则不咬人"）
matrix:
  compiler: [GCC 15.3.0]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_strict_alias.cpp
command: |          # POSIX 语义；产物必须写 build/（仓库源只读）
  # 注：机器复算契约是「一条 command 的 stdout ↔ 一组 run_* 值」，故 command 只跑主档 -O2；
  #     `-O0` 与 `-fno-strict-aliasing` 为同夹具人工补跑（见 actual），并用 expected_key 指明对应组。
  g++ -std=c++23 -O2 Examples/atoms/_atom_strict_alias.cpp -o build/_replay_alias.exe && ./build/_replay_alias.exe
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_strict_alias.cpp -o Examples/atoms/_atom_strict_alias.asm
artifact: Examples/atoms/_atom_strict_alias.asm
artifact_sha256: 900a3e43f70ed68bcdf621d907a39996f62ec289fe4e453c910aa435c027575e
# 2026-09-10 两次重生成：7bbf2506… 是"汇点仍为 32 位"的版本、8de76a9e… 是"宽度已改但提升时机错"
# 的版本，见下"踩坑"①②③（三次自身 UB 都留痕，最终版才与断言同代）。
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植的结构断言（身份不匹配时的替代校验）
  - {kind: contains, text: "_Z10alias_killPiPf"}   # 夹具函数被 noinline 固定为独立符号
  - {kind: contains, text: "_ZL6g_sink"}           # volatile 汇点符号存在（防折叠证据）
expected_key: run_GCC15.3_O2_cxx23   # command 跑的是 -O2 主档，对应下面这一组
expected:
  run: >-
    -O2（严格别名默认）：形态 A 的函数返回被优化成常量 1，而内存实际是 2.0f 的位模式
    1073741824 → **自洽=否**；合规路径（memcpy）两读法一致。这"不一致"就是 UB 被利用的实证。
  asm: >-
    alias_kill 函数体内**不出现对 [rcx] 的第二次读取**：返回值为静态常量 1（`mov eax, 1`
    出现在两次写之前）——优化器假定 `[rdx]`（float*）不影响 `[rcx]`（int*）。
actual:                      # 逐项实测（2026-09-10）
  run_GCC15.3_O2_cxx23: "A 函数返回=1 内存实际=1073741824 自洽=否 | B UB路径=1073741824 合规路径=1073741824 一致=是"
  run_GCC15.3_O0_cxx23: "A 函数返回=1073741824 内存实际=1073741824 自洽=是 | B UB路径=1073741824 合规路径=1073741824 一致=是"
  run_GCC15.3_O2_no_strict_alias: "A 函数返回=1073741824 内存实际=1073741824 自洽=是 | B UB路径=1073741824 合规路径=1073741824 一致=是"
  asm_GCC15.3_O2: "alias_kill (L8-14)：mov eax,1（返回值静态化）→ mov DWORD PTR [rcx],1 → mov DWORD PTR [rdx],0x40000000 → ret，**无二次读 [rcx]**"
verdict: confirm
falsification: >-
  **`-fno-strict-aliasing` 对照**：关闭别名假设后"自洽"从 否 恢复为 是（实测）。若开关不影响
  结果，说明观测到的差异不来自严格别名假设，本证据作废。另：`-O0` 下同样自洽——说明这不是
  "程序本来就错"，而是**优化器利用了 UB 才出错**。
depth_layer: asm
drill_note: >-
  `alias_kill` 的 -O2 汇编里，返回值 `mov eax, 1` 排在两次写之前，且函数体内没有对 `[rcx]` 的
  二次读取——机器码层面直接展示"优化器已假定两个不同类型的指针不指向同一对象"。
reproduce: 见 command 两行；对照档 `-O0` / `-O2 -fno-strict-aliasing` 用同一夹具人工补跑
---

## 为什么这个证据可信

1. **有证伪对照且对照真的改变了结果**：`-fno-strict-aliasing` 关掉假设 → 自洽性从"否"回到"是"。
   这排除了"我把语义算错了"与"程序本身有 bug"两种替代解释。
2. **双层互证**：
   - 运行层：同一对象的"函数返回值"与"内存实际内容"**不一致**（1 vs 1073741824）；
   - 汇编层：`alias_kill` 内返回值被静态化成常量、且**没有第二次读取** `[rcx]`。
   两者指向同一事实：优化器假定了不别名。
3. **`-O0` 三档一致对照**：`-O0` 下自洽 → 说明 UB 不是"立刻崩"，而是"**允许优化器做任何事**"，
   这在教学上正是最容易误导人的地方（"我本地跑着好好的"）。

## 踩坑（研究 UB 的夹具自己最容易踩 UB——**连踩三次**，全部留痕）

**① 首版"防折叠汇点"用了 `volatile int`，自身整数溢出。**
`g_sink = a_func + a_mem` 累加到 2147483648（> `INT_MAX`），UBSan 报
`signed integer overflow` → 证据卡判 `refute:sanitizer_reported`。
**是被证据卡自己的 sanitizer 校验抓到的**——这正是该校验存在的意义（"研究 UB 的实验代码也必须过 sanitizer"）。

**② 第二版改用 `long`，仍然溢出。**
因为 **Windows 是 LLP64：`long` = 32 位**（只有 Linux/macOS 的 LP64 才是 64 位）。
识别方式很直接——重新生成的 `.asm` 里该符号仍是 `.lcomm _ZL6g_sink,4,4`（4 字节），
改 `long long` 后才变成 `,8,8`。
**教训**："换一个更宽的类型"这一步在此项目里也绕不开**数据模型差异**（LLP64 vs LP64）。

两次踩坑都没有被"输出看起来正常"掩盖——因为观测通路（sanitizer + 汇编字节宽度）是活的。

## 观测口径的诚实说明

- **不断言 UB 的"结果值"**：UB 按定义不可预测，把"返回值=1"写成 expected 等于把"我这次跑出来的
  值"当规律。本卡断言的是**两种读法是否自洽**（那是"UB 是否被利用"的可判定观测），并把不同档位的
  结果分别留痕（`expected_key` 指明 command 对应哪一组，其余为人工补跑）。
- **本卡只覆盖 GCC**：Clang 列由 CI 的 Gray-zone 步骤留痕（本机与 WSL 均无 Clang），MSVC 无任何
  可执行路径——按 M2 §2 永久边界，MSVC 以标准条文代替，**不得宣称"三编译器实测完备"**。
- **`-fno-strict-aliasing` 档为人工补跑**：受复算契约（一条 command ↔ 一组 run_*）限制，
  与 EV-MEM-002 的 `-O0` 同法处理。

## 教学中要接的另一刀：它和"求值顺序 unspecified"不是一类

同一样板里对照 `EV-UB-001`（`f(g(), h())` 的求值顺序）：

| | 求值顺序（EV-UB-001） | 严格别名（本卡） |
|---|---|---|
| 标准分类 | **unspecified** | **UB** |
| 标准给了什么 | 合法结果集合（两种顺序都合法） | **不再要求任何行为** |
| 会不会崩 | 不会 | 可能，也可能"看起来很对" |
| 能不能依赖 | 不能（但可以依赖"不崩"） | 完全不能，**代码已失去意义** |
| 优化器动作 | 只是选一种顺序 | **可基于"不存在"的假设删除你的访问** |
