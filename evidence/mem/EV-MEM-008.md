---
id: EV-MEM-008
serves: [ATOM-MEM-PERF-001]
kind: asm
hypothesis: >-
  移动构造的收益来自"掏空源对象"：持堆指针的类型移动只偷指针（sizeof(void*)=8 字节）且 0 分配；
  无动态资源的纯值类型移动 = 拷贝（同样搬全部字节、源不被掏空），std::move 无性能收益。
controlled_vars: 同一 TU、同一编译器、同一 -O2；唯一变量 = 类型是否持有动态资源（Value32 栈上定长 vs HeapBuf 堆指针）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_perf_move.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_perf_move.cpp -o Examples/_atom_perf_move.asm
  g++ -std=c++23 -O2 Examples/_atom_perf_move.cpp -o build/_replay_perf.exe && ./build/_replay_perf.exe
artifact: Examples/_atom_perf_move.asm
artifact_sha256: fb588ba4ce07f41f348d528247706c04818548975c9f2dec6e9528e227576f78
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "_Znay"}                                  # operator new[] 编译进工件（堆组分配路径真实存在）
  - {kind: contains_any, texts: ["movaps", "vmovaps", "movdqu", "QWORD PTR"]}  # 值类型/堆移动确有字节搬运
expected:
  run: Value32 sizeof=32 且移动==拷贝字节；heap 拷贝分配=1、移动分配=0；值类型移动后源完好
  asm: main 内 _Znay 恰 2 次调用（h 构造 + hc 拷贝），hm 移动路径 0 次调用（只偷指针）；值类型逐字节搬
actual:
  run_cxx23_O2: "Value32 sizeof=32 move_eq_copy_bytes|heap copy_allocs=1 move_allocs=0|value move source intact=1"
  run_cxx23_O0: "Value32 sizeof=32 move_eq_copy_bytes|heap copy_allocs=1 move_allocs=0|value move source intact=1"
verdict: confirm
falsification: >-
  ① 若 heap 移动也发生分配（把移动实现成假移动），则"移动只偷指针"被推翻，运行计数变 1；
  ② 若值类型移动后源被掏空（move 真的"搬走"了字节），则"纯值类型移动=拷贝、无收益"被推翻。
  本卡实测 heap 移动 0 分配、值类型移动后源完好（ym.a[0]==seed），两条件均不成立 => 经受住证伪。
depth_layer: asm
drill_note: >-
  main 内 _Znay（operator new[]）被调用 2 次（h 构造 1 + hc 拷贝 1），hm 移动构造路径 0 次调用——
  移动只偷指针（8 字节）并置空源，拷贝才分配 + 搬堆数据。值类型 Value32 移动与拷贝在 -O2 下
  都落为逐 qword 搬运（sizeof=32，源不被掏空），与 EV-MEM-002 的 32 字节 SIMD 搬运互为印证。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照（且对照自带）**：卡内同时有"无收益"组（Value32 移动==拷贝、源完好）与"有收益"组
   （HeapBuf 移动 0 分配），二者同 TU 同优化档对比，唯一变量是"是否持有动态资源"——正是论断的核心。
2. **双层互证**：运行层（volatile 计数：heap 拷贝 1 / 移动 0）与汇编层（`_Znay` 调用点计数）独立指向
   同一结论；计数用 volatile 计数器，排除 -O2 常量折叠（M2 §5）。
3. **跨优化档一致**：`-O0` 与 `-O2` 运行输出逐字一致（见 `run_cxx23_O0`），说明"移动无收益"不是优化器假象。

## 与既有证据卡的关系（避免重复锻造）

- `EV-MEM-001`（移动不分配堆内存）提供"移动分配=0"的运行计数基础；本卡在其上**扩展**出"拷贝分配=1"
  的对照组与字节搬运视角，使"省 vs 不省"可量化。
- `EV-MEM-002`（纯值类型移动无收益）提供 32 字节 SIMD 搬运断面；本卡用同结论的 Value32 组补一个
  `-O0/-O2` 双跑的量化版本，并加入 heap 组的指针窃取对照。
- 三卡共同服务 `ATOM-MEM-PERF-001`（本卡为专属新卡），并互为 `ATOM-MEM-MOVE-002` 的量化支撑。
