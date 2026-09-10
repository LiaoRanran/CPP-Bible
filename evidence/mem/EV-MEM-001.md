---
id: EV-MEM-001
serves: [ATOM-MEM-MOVE-001]      # 该原子在 G4 正式锻造，此处为 G2 示范证据
status: example                  # example：G2 方法示范，非已验收原子的正式证据
kind: run                        # run|asm|layout|abi|symbol|bench|sanitizer|godbolt|traceable_argument
hypothesis: >-
  对含堆缓冲的类型，移动构造不分配堆内存（分配 0 次），拷贝构造分配 1 次。
controlled_vars: 同一 Buf 类型、同一编译器、同一 -O2；唯一变量 = 拷贝构造 vs 移动构造
matrix:
  compiler: [GCC 15.3.0, GCC 13.1.0, GCC 8.1.0]
  std: [c++23, c++17]        # 8.1.0 不支持 c++23，其两档改用 c++17（见 M2 §2 夹具↔std 绑定）
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_move_alloc.cpp
command: |
  g++ -std=c++23 -O2 Examples/_atom_move_alloc.cpp -o a.exe && ./a.exe
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_move_alloc.cpp -o Examples/_atom_move_alloc.asm
artifact: Examples/_atom_move_alloc.asm
artifact_sha256: 460c39814167f8aee7d95b0a59076de0c69c7134adba79b49bde00bdd7b4002f
expected:
  run: 主实验 构造分配=1 拷贝分配=1 移动分配=0；证伪对照 假移动分配=1
  asm: main 中 call malloc 恰好 3 次 = Buf 构造 1 + Buf 拷贝 1 + 证伪对照 BadBuf 假移动 1；
       真实移动（Buf 移动构造）路径分配 0 次
actual:
  run_GCC15.3_O2: "构造分配=1 拷贝分配=1 移动分配=0 | 证伪对照(假移动)分配=1"
  run_GCC15.3_O0: "构造分配=1 拷贝分配=1 移动分配=0 | 证伪对照(假移动)分配=1"
  run_GCC13.1_O2: "构造分配=1 拷贝分配=1 移动分配=0 | 证伪对照(假移动)分配=1"
  run_GCC8.1_O2_cxx17: "构造分配=1 拷贝分配=1 移动分配=0 | 证伪对照(假移动)分配=1"
  asm_GCC15.3_O2: "main 中 call malloc 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次"
verdict: confirm
falsification: >-
  对照实现 BadBuf 的移动构造写成"也 new 一次"（假移动）。实测输出"证伪对照(假移动)分配=1"
  ——若本实验对它也输出 0，则是恒真空测试，证据作废。
depth_layer: asm
drill_note: 运行时计数与 -O2 汇编的 malloc 调用点互证；计数器必须 volatile，否则 -O2 会常量折叠
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照**：假移动实现产出 1 次分配，证明实验能区分真假移动，不是恒真。
2. **双层互证**：运行时计数（主实验 1/1/0 + 对照 1）与汇编层调用点（`main` 中 `call malloc`
   3 次，含对照那一次）独立指向同一结论。

> 口径留痕（2026-09-10 复跑修正）：本卡原记"call malloc 2 次（构造+拷贝）"，是按**只看主实验**
> 数的；夹具后来加入证伪对照 `BadBuf`（其假移动也 `new` 一次），`main` 内实际为 3 次。数字必须
> 与"是否含对照"绑定说明，否则复核者会误判为不可复现——这类"计数口径漂移"正是 S3 伪证据检测
> 要拦的形态（不是造假，但会让证据看起来对不上）。
3. **跨优化级别一致**：`-O0` 与 `-O2` 同结果，排除"结论只在一档优化下成立"。
4. **跨版本一致**：GCC 13.1 与 15.3 同结果。

## 踩过的坑（必须留痕，供后续夹具参考）

- 初版只替换 `operator new`，代码走 `operator new[]` → 计数恒 0 → **空测试**。
- 补 `operator new[]` 后，-O2 把计数**常量折叠**（`main` 里只剩 `mov edx,1`，无 `call _Znay`）→ 输出看似证实，实则零观测。
- 用 `argc` 让大小运行时确定仍折叠（次数与大小无关）→ 最终靠 `volatile` 计数器阻断。

**教训（已写入 M2 第 5 节）**：计数类实验必须 `-O0` 与 `-O2` 双跑，计数器必须 `volatile`。

## 待补

- Clang / MSVC 两列：本机无，需 CI 补齐（M2 第 2 节已标待确认）。
- 对象布局层（`-fdump-record-layouts`）证据：本级未做，G4 样板按需补。
