---
id: EV-MEM-002
serves: [ATOM-MEM-MOVE-002, ATOM-MEM-PERF-001]      # MOVE-002（G4 样板）+ PERF-001（G5 批量生产，量化支撑）
status: example                  # example：G4 样板配套证据，随样板一并人审（非已验收原子的正式证据）
kind: asm                        # run（分配计数）+ asm（字节搬运）双观测
hypothesis: >-
  移动的收益来自"掏空源对象"：对不含间接资源的纯值类型，移动退化为拷贝——既不减少分配，
  也不改变源对象，只是把字节搬进新对象。
controlled_vars: >-
  同一 TU、同一编译器、同一 -O2；唯一变量 = 类型是否持有间接资源（HeapBuf 堆指针
  vs FixedBuf/std::array 栈上定长数组）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_move_no_gain.cpp
command: |          # POSIX 语义；产物必须写 build/（仓库源只读）
  # 注：机器复算契约是「一条 command 的 stdout ↔ 一组 run_* 值」，故 command 只跑主档 -O2；
  #     -O0 档为**同夹具人工实测**（数据见 actual.run_GCC15.3_O0_cxx23），与 EV-MEM-001 同法。
  g++ -std=c++23 -O2 Examples/atoms/_atom_move_no_gain.cpp -o build/_replay_nogain.exe && ./build/_replay_nogain.exe
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_move_no_gain.cpp -o Examples/atoms/_atom_move_no_gain.asm
artifact: Examples/atoms/_atom_move_no_gain.asm
artifact_sha256: d9f5a254fb21d2f2a05c74fedfbceb28be68aa8ea3361a0792ee4259d66639ff
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植的结构断言（身份不匹配时的替代校验）
  - {kind: contains, text: "_ZL8g_allocs"}                                          # volatile 计数器未被折叠
  - {kind: contains_any, texts: ["movaps", "vmovaps", "movups", "movdqu", "memcpy"]} # 纯值组确有字节搬运
expected:
  run: >-
    HeapBuf 拷贝分配=1 / 移动分配=0，且移动后源被掏空；
    FixedBuf 与 array 的拷贝与移动分配**均为 0**，且源内容完好
  asm: >-
    main 内 call malloc 恰 1 次（HeapBuf 的拷贝构造），移动路径无分配调用；
    纯值组出现 32 字节 SIMD 搬运（std::array<int,8> = 32 字节）
actual:                      # 逐项实测（2026-09-10）
  # -O0 与 -O2 输出**逐字一致** —— 本论断不是优化器的假象（这才是补 -O0 档要回答的问题）。
  run_GCC15.3_O2_cxx23: "HeapBuf  拷贝分配=1 移动分配=0 移动后源被掏空=是 | FixedBuf 拷贝分配=0 移动分配=0 移动后源完好=是 | array    拷贝分配=0 移动分配=0 移动后源完好=是"
  run_GCC15.3_O0_cxx23: "HeapBuf  拷贝分配=1 移动分配=0 移动后源被掏空=是 | FixedBuf 拷贝分配=0 移动分配=0 移动后源完好=是 | array    拷贝分配=0 移动分配=0 移动后源完好=是"
  # 两组值逐字相同 ⇒ 工具判为「同一变体」，不触发 ambiguous（这也是"跨档位一致"的机器体现）。
  asm_GCC15.3_O2: "main: call malloc ×1 (L117) + call free ×1 (L126)；pshufd + movaps XMMWORD PTR [rsp+80]/[rsp+96] = 32 字节搬运；volatile 读回 mov r15d,[rcx] (L144) 与 cmp/cmove 运行时判定"
verdict: confirm
falsification: >-
  ① 若 HeapBuf 的移动也发生分配（把移动实现成假移动），说明计数没接上，实验作废；
  ② 若纯值组也显示"源被掏空"，说明结论写反，实验作废。
  本卡另含一处**自证伪留痕**：第一版夹具把内容写成编译期常量（42），-O2 把纯值组的构造/移动/读回
  整体消除（main 里没有任何搬运指令，"源完好=是"是编译期常量）——这正是红队阶段由**汇编断面**
  抓到的零观测伪证据；改用"argc 派生初值 + volatile 读回"后才获得真实观测（见下"踩坑"）。
depth_layer: asm
drill_note: >-
  移动的"省"与"不省"在汇编层可分辨：HeapBuf 的移动只搬 8 字节指针并把源置空；FixedBuf<8> 的移动
  必须搬 32 字节且源分毫未动。数据量本身说明收益来自"掏空源对象"，而非"移动这个动作更快"。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有对照且控制变量干净**：`HeapBuf`（持堆指针）与 `FixedBuf`/`std::array`（纯值）在同一 TU、
   同一优化档下对比；唯一差异是"是否持有间接资源"。`std::array` 组的加入把结论从"自定义类型的
   特性"提升到"标准库类型同样如此"。
2. **双观测互证**：
   - 运行层：分配计数（HeapBuf 拷贝 1 / 移动 0）；
   - 汇编层：`main` 内 `call malloc` 恰 1 次（对应 HeapBuf 的拷贝构造），移动路径无任何分配调用；
     纯值组则出现 `pshufd` + `movaps XMMWORD PTR` ×2 = **32 字节搬运**（`std::array<int,8>` 正好 32 字节）。
3. **"源是否被掏空"是运行时判定**，不是编译期常量：汇编里可见 volatile 读回（`mov r15d, DWORD PTR [rcx]`）
   与 `cmp` / `cmove` 比较，证明输出"是/否"来自真实读取。
4. **反常量折叠已处理并在卡内留痕**：初版是这个实验最危险的地方——见下。

## 观测口径的两点诚实说明（红队要求）

- **分配计数对纯值组没有分辨力**：`FixedBuf`/`array` 的拷贝与移动都分配 0 次，所以"移动分配=0"
  这一列**不能**单独用来证明"移动更省"。真正有分辨力的是**第二列观测**：移动后源是否被掏空
  （HeapBuf=是，纯值组=否），以及**汇编层的字节搬运量**（0 字节 vs 32 字节）。
  → 结论表述必须绑定观测：本项目断言的是"**没有间接资源可掏空时，移动不发生资源转移**"，
  而不是"移动分配次数总是更低"。
- **`源完好=是` 是实现事实，不是标准保证**：标准只承诺移动后源"有效但未指定"。本卡实测的是
  libstdc++/GCC 15.3.0 的行为（对 `int` 逐元素 move 等价于拷贝），故 `claim_boundary` 不含其他
  实现；换标准库/编译器需重跑而非外推。

## 踩坑（必须留痕，供后续夹具参考）

- **零观测伪证据**：第一版夹具把纯值组的内容写成编译期常量，`-O2` 直接把整组的构造、移动、读回
  消除——`main` 里只有对 `volatile` 计数器的清零与读取，**没有任何搬运指令**，而输出照样打印
  "移动分配=0 源完好=是"。这是一种最难自查的伪证据：**数字看起来完美符合预期，但它不是观测来的**。
- **发现方式**：红队阶段不看输出、改看**汇编断面**（`main` 段里有没有搬运指令）。
  → 教训固化：**凡"证明某件事没有发生"的实验，必须证明观测通路是活的**（本卡用 volatile 读 +
  汇编指令双证据）；这也再次印证 M2 第 5 节"计数类实验必须 `-O0`/`-O2` 双跑 + volatile"。
- **修法**：初值由 `argc` 派生（运行时值不可常量折叠）+ 用 `volatile` 指针读回源内容（volatile
  访问是标准明文的可观测行为，编译器必须真实发射读指令）。

## 待补（人审通过后的扩展项）

- ~~`-O0` 档~~ → **已补**（2026-09-10，人审放行条件之一）：`-O0` 与 `-O2` 输出**逐字一致**，
  说明"移动无收益"**不是优化器的假象**（这是补这一档真正要回答的问题，而非走形式）。
  该档为**同夹具人工实测**（数据见 `actual.run_GCC15.3_O0_cxx23`）——因为机器复算契约是
  「一条 `command` 的 stdout ↔ 一组 `run_*` 值」，两档并入同一 command 会让输出累积成 6 行、
  无法逐字比对（实测 `refute:run_mismatch`），与 EV-MEM-001 的处理方式一致。
- **工具契约边界（建议纳入工具修复波）**：多档位实验目前只能"主档进 command + 其余人工跑"。
  若未来多档位实验变多，可考虑让 `atom_evidence_replay.py` 支持「多组 run_* ↔ 多段输出」的
  映射（例如按 `expected_key` 列表分段比对），使 `-O0/-O2` 这类正交维度也能全自动复算。
- Clang 列：本机无 Clang；CI 的 Clang-19 矩阵为 `continue-on-error`，可在 G4 后续补一列对照。
