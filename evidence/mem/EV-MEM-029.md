---
id: EV-MEM-029
serves: [ATOM-MEM-PERF-002]
kind: run
hypothesis: >-
  SSO（小字符串优化）：短于阈值的字符串存 std::string 对象内部缓冲，零堆分配；达到阈值才落堆。
  本机 libstdc++ 阈值为 15 字符（len≤15 分配 0 次、len=16 首次落堆）。双通路交叉验证：计数分配器
  （basic_string 模板在 exe 内实例化）与全局 operator new 钩子（std::string 默认 allocator 同样在
  exe 内实例化）测得同一阈值。
controlled_vars: 同一 basic_string 填充构造（len, 'x'）、同一编译器；唯一变量 = 字符串长度（0..24 扫描）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_sso_threshold.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_sso_threshold.cpp -o Examples/_atom_sso_threshold.asm
  g++ -std=c++23 -O2 Examples/_atom_sso_threshold.cpp -o build/_replay_sso_thr.exe && ./build/_replay_sso_thr.exe
artifact: Examples/_atom_sso_threshold.asm
artifact_sha256: 75130ec6ea8b66b719992510c634c956edf84c56691ff5ae633208e0a29794d8
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "max_zero_alloc_len"}   # 阈值观测点字符串进入工件
expected:
  run: len≤15 全部 allocs=0；len=16 首次落堆 allocs=1；max_zero_alloc_len=15 first_heap_len=16；std-string 交叉验证同阈值
  asm: 阈值观测点字符串进入工件（扫描实验真实存在）
actual:
  run_cxx23_O2: "len=0 allocs=0|len=14 allocs=0|len=15 allocs=0|len=16 allocs=1|len=22 allocs=1|len=23 allocs=1|sso: max_zero_alloc_len=15 first_heap_len=16|std-string: len=15 allocs=0 len=16 allocs=1"
  run_cxx23_O0: "len=0 allocs=0|len=14 allocs=0|len=15 allocs=0|len=16 allocs=1|len=22 allocs=1|len=23 allocs=1|sso: max_zero_alloc_len=15 first_heap_len=16|std-string: len=15 allocs=0 len=16 allocs=1"
verdict: confirm
falsification: >-
  ① 若 SSO 不存在（所有长度都落堆），len=0..15 应 allocs≥1——实测全 0；② 若阈值不是 15（如 10 或 31），
  first_heap_len 应相应移动——实测 len=15 仍 0 分配、len=16 落堆；③ 双通路不一致（计数分配器与
  operator new 钩子测得不同阈值）则实验设计失效——实测两者一致。均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  libstdc++ 的 string 是 32 字节 union：短串模式存 15 字符 + size 标记，长串模式存堆指针 + 容量
  （最低位标记模式）——SSO 是实现内建，标准只保证 string 语义、不要求 SSO（[string.requirements]）。
  len≥16 每次 allocs=1（一次缓冲分配），无二次扩容。初版夹具在 CountAlloc::allocate 里手动计数 +
  operator new 钩子双重计数（len=16 得 allocs=2 的假信号），修正为单一计数通路后得到 allocs=1——
  "计数通路唯一"与"观测通路活着"同样重要。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **全长度扫描**：不是只测一两个点，0..24 逐长度扫描把"阈值"变成边界可定位的阶跃（15→16 之间
   翻转），证伪空间覆盖任意阈值假设。
2. **双通路交叉验证**：自定义计数分配器与默认 allocator（operator new 钩子）两条独立观测路径测得
   同一阈值（15）——排除"计数器本身影响布局"的疑虑。
3. **-O0/-O2 双跑一致**：输出逐字相同（SSO 判定在库的类型逻辑层，与优化档无关）。

## 边界诚实说明

- 阈值 15 是 libstdc++ 实现细节：libc++ 为 22（sizeof=24）、MSVC 为 15（sizeof=32）——三实现数值
  见 EV-MEM-031；标准不保证 SSO 存在，换实现/换版本阈值可能变（本卡 artifact_compiler 已锚定归属）。
- 初版双重计数假信号已修正并留痕（见 drill_note）。Clang 列由 CI Cross-check 回填。
