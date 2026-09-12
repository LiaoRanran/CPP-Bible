---
id: EV-MEM-031
serves: [ATOM-MEM-PERF-002]
kind: run
hypothesis: >-
  SSO 的形状参数是**实现内建**、不保证跨实现一致：本机 libstdc++（GCC 15.3.0）sizeof(std::string)=32、
  空串 capacity=15（SSO 容量 15 字符）、len=15 零分配 / len=16 落堆。libc++（Clang）为 sizeof=24、
  SSO 容量 22（与另两家不同）；MSVC 为 sizeof=32、SSO 容量 15——后两者为文档值（本机无 Clang/MSVC，
  M2 边界；Clang 列由 CI Cross-check 回填）。
controlled_vars: 同一 std::string 类型、同一编译器；唯一变量 = 被测属性（sizeof / capacity / 阈值边界两侧的分配次数）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）；MSVC 以实现文档值代替（M2 边界）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_sso_size.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_sso_size.cpp -o Examples/atoms/_atom_sso_size.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_sso_size.cpp -o build/_replay_sso_size.exe && ./build/_replay_sso_size.exe
artifact: Examples/atoms/_atom_sso_size.asm
artifact_sha256: 77f1164c3dc0340e09a55718e51adb7dcd9dc8b6a01e03bcbfd4e9670febf7ae
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "sizeof"}    # 尺寸观测点字符串进入工件
expected:
  run: sizeof=32；empty capacity=15；len=15 allocs=0 / len=16 allocs=1（阈值与 capacity 自洽）
  asm: 观测点字符串进入工件（static_assert 锚定 libstdc++ 布局）
actual:
  run_cxx23_O2: "sizeof(std::string)=32|empty capacity=15 (SSO buffer chars)|len=15 allocs=0 len=16 allocs=1"
verdict: confirm
falsification: >-
  ① 若 capacity=15 与实测阈值不自洽（如 len=15 已落堆），则"capacity 即 SSO 容量"的解读被推翻——
  实测 len=15 allocs=0 与 capacity=15 吻合；② 若 sizeof 不是 32（布局假设错），static_assert 编译红
  （机器复算 compile_rc 拦截）。均不成立 => 经受住证伪。
depth_layer: compiler
drill_note: >-
  三实现布局差异：libstdc++ 32 字节（union：15 字符缓冲 vs 堆指针+容量，最低位标记模式）、
  libc++ 24 字节（union：22 字符缓冲，size 存最高位字节）、MSVC 32 字节（union：15 字符缓冲 +
  separate size/capacity）——这就是"SSO 阈值跨实现不可移植"的布局根源。历史注脚：libstdc++ 在
  C++11 前用 COW（引用计数共享），C++11 语义（要求独立表示 + 禁止有锁引用计数）使 COW 不再合法，
  才全面转向 SSO；EV-MEM-030 的"长拷贝 allocs=1"正是这一转变的可观测结果。SSO 是 SBO（Small
  Buffer Optimization）在 string 上的特例——std::function、std::any 同样用 SBO，机制同源。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

> 本卡定位：**布局锚定卡**（无独立反例组）——证伪力来自"sizeof / capacity / 阈值三值互相咬合"
> 的自洽约束，而非对照实验；三实现对比部分依赖文档值（已标注口径），这是形状卡的性质使然。
> 分层说明：depth_layer=compiler 指 sizeof/static_assert 主口径；len=15/16 分配计数为 runtime
> 侧辅证（与 EV-MEM-029 同一观测通路）。

1. **三值自洽**：sizeof=32（static_assert 锚定布局）、capacity=15（运行期）、阈值 15/16（分配计数）
   三个独立测量互相咬合——不是单点观测。
2. **实现归属显式声明**：static_assert 只锚定 libstdc++（artifact_compiler 声明归属），libc++/MSVC
   数值以文档值标注（M2 边界诚实），不冒充实测。
3. **类型系统论证**：sizeof/static_assert 是编译期事实（落在 compiler 层），与优化档无关，故只跑
   -O2 一档（沿 EV-MEM-006 先例）。

## 边界诚实说明

- libc++（24/22）与 MSVC（32/15）数值来自各自实现文档，非本机实测（本机无 Clang/MSVC）——这是
  "三实现对比"卡里唯一非一手的部分，已用文档值口径标注；Clang 列由 CI Cross-check 回填。
- C++11 前 libstdc++ 的 COW 历史以"EV-MEM-030 长拷贝 allocs=1"侧面佐证（COW 下应为 0），未在本机
  复现旧版本行为。
