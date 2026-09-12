---
id: EV-MEM-028
serves: [ATOM-MEM-ALLOC-001]
kind: run
hypothesis: >-
  std::pmr 把内存策略变成运行时多态（memory_resource 虚接口，策略在构造时注入、可运行时替换）。
  monotonic_buffer_resource 用一块栈上缓冲区伺候所有分配：pmr::vector 16 次 push_back 全程未触碰
  上游（upstream_allocs=0 ⇒ 零堆分配）；对照组把同一容器接到"计数+委托 new_delete_resource"的
  资源上，扩容路径可见（res_calls=5、bytes=124）。
controlled_vars: 同一 pmr::vector<int> + 同一 16 次 push_back、同一编译器；唯一变量 = 注入的 memory_resource（monotonic+栈缓冲 vs 计数委托堆）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_alloc_pmr.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_alloc_pmr.cpp -o Examples/atoms/_atom_alloc_pmr.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_alloc_pmr.cpp -o build/_replay_alloc_pmr.exe && ./build/_replay_alloc_pmr.exe
artifact: Examples/atoms/_atom_alloc_pmr.asm
artifact_sha256: 1a9fc2e41d821784582ff71d626a1bb59ac93fcbd5977be089a2302e3d8a6f42
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "monotonic"}     # monotonic 观测点字符串进入工件
  - {kind: contains, text: "delegating"}    # 对照组观测点字符串进入工件
expected:
  run: monotonic 组 upstream_allocs=0（零堆）；delegating 组 res_calls=5 bytes=124（扩容走堆可见）
  asm: 两组观测点字符串进入工件（对照真实存在）
actual:
  run_cxx23_O2: "monotonic: upstream_allocs=0 (zero heap: buffer served everything)|delegating: res_calls=5 bytes=124 (growth path, heap-backed)"
  run_cxx23_O0: "monotonic: upstream_allocs=0 (zero heap: buffer served everything)|delegating: res_calls=5 bytes=124 (growth path, heap-backed)"
verdict: confirm
falsification: >-
  ① 若 monotonic 会溢出到上游（缓冲不够或策略失效），upstream_allocs>0——实测 0；② 若 pmr 容器不经
  注入的 resource（多态不成立），delegating 组 res_calls=0——实测 5。均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  "零堆"的判据是**上游计数**而非 operator new 重载：本机实测 MinGW libstdc++ 为动态 DLL，
  new_delete_resource（编进 DLL 的非模板代码）内部的 operator new 调用不经过 exe 的替换版本
  （DLL 内符号自绑定）——初版夹具用全局 operator new 观测对照组得 heap_new=0（假阴性，观测通路
  已死），重写为虚资源层计数（我们的 do_allocate 在 exe 内实例化，虚调用必达）后才得到 res_calls=5。
  这是"证明某事没发生，必须同时证明观测通路活着"（M2 §5）的 pmr 版实例：对照组 res_calls=5 正是
  观测通路活着的证明。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **零堆判据自洽**：monotonic 组 upstream_allocs=0 = 缓冲全程够用 = 无上游调用 = 无堆（上游唯一
   去处是 new_delete_resource）；对照组 res_calls=5 bytes=124 证明同一容器在同序列下的真实分配
   需求，二者相减即"栈缓冲省下的堆流量"。
2. **观测通路已验证**：计数放在虚资源层（exe 内实例化的 do_allocate），对照组给出非零计数证明
   通路活着——不重蹈"operator new 钩子测 DLL 内部分配"的假阴性（初版实测踩坑，已留痕）。
3. **-O0/-O2 双跑一致**：输出逐字相同。

## 边界诚实说明

- res_calls=5/bytes=124 是 libstdc++ 倍增扩容指纹（同 EV-MEM-027），换实现数字可变、结论不变。
- 初版假阴性已修正并留痕：operator new 重载在 MinGW 动态 libstdc++ 下观测不到 DLL 内部的分配
  （new_delete_resource / 库内静态对象路径），pmr 证据一律以资源层计数为准。Clang 列由 CI 回填。
