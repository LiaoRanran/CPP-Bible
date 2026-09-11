---
id: EV-MEM-030
serves: [ATOM-MEM-PERF-002]
kind: run
hypothesis: >-
  SSO 的操作代价差是确定性的分配次数差：短字符串（≤阈值）拷贝零堆分配（只搬对象内 32 字节
  缓冲；赋值走同一实现路径，未单列观测行）；长字符串同样的操作每次都要 1 次堆分配；短+短拼接
  一旦越过阈值（10+10=20>15），结果立即落堆 1 次。性能口径用分配次数而非墙钟（墙钟不可复现，
  沿 EV-MEM-008 先例）。
controlled_vars: 同一 std::string、同一编译器；唯一变量 = 操作对象（短 len=10 / 长 len=100）× 操作（拷贝/赋值/拼接）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_sso_cost.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_sso_cost.cpp -o Examples/_atom_sso_cost.asm
  g++ -std=c++23 -O2 Examples/_atom_sso_cost.cpp -o build/_replay_sso_cost.exe && ./build/_replay_sso_cost.exe
artifact: Examples/_atom_sso_cost.asm
artifact_sha256: 06579f60872a4111e9ff4a9531e30e1925a54507bafa7e09e329f7cfa754d77e
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "allocs"}    # 计数观测点字符串进入工件
expected:
  run: 短拷贝 allocs=0；长拷贝 allocs=1；长赋值 allocs=1；短+短拼接（越阈）allocs=1
  asm: 观测点字符串进入工件（四组观测真实存在）
actual:
  run_cxx23_O2: "copy short(len=10): allocs=0|copy long (len=100): allocs=1|assign long: allocs=1|concat 10+10=20chars: allocs=1"
  run_cxx23_O0: "copy short(len=10): allocs=0|copy long (len=100): allocs=1|assign long: allocs=1|concat 10+10=20chars: allocs=1"
verdict: confirm
falsification: >-
  ① 若短字符串拷贝也要分配（SSO 未覆盖拷贝路径），第 1 行应 allocs≥1——实测 0；② 若长字符串拷贝
  不分配（引用计数/共享，COW 行为），第 2 行应 allocs=0——实测 1（C++11 起禁止 COW，拷贝必独立）；
  ③ 若拼接永不落堆（结果仍走 SSO），第 4 行应 allocs=0——实测 1（20 字符已越阈）。均不成立 =>
  经受住证伪。
depth_layer: runtime
drill_note: >-
  四组观测同 TU 对照：唯一变量是操作对象与长度。短拷贝 allocs=0 = SSO 缓冲随对象整体复制（对象
  本身 32 字节，栈/寄存器级拷贝）；长拷贝 allocs=1 = C++11 起禁 COW 后拷贝必须独立持有缓冲
  （[string.requirements]：basic_string 的拷贝不共享表示）。拼接行说明 SSO 的边界效应：两个短串
  的结果不一定短——越阈立即付出堆代价。分配次数是墙钟的确定性代理：每 1 次堆分配 ≈ 数十至数百
  ns（实现相关），短串操作全程无系统调用/锁路径。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照（三向）**：短拷贝（0）vs 长拷贝（1）分出 SSO 有无；长拷贝（1）同时证伪 COW 残留
   （C++11 前的 libstdc++ 此处为 0）；拼接（1）给出"短+短≠短"的边界行为——实验有区分力。
2. **确定性口径**：分配次数可精确复现，-O0/-O2 双跑逐字一致；墙钟计时被有意排除（不可复现，
   与 EV-MEM-008 的性能量化口径一致）。
3. **与 EV-MEM-029 互证**：阈值卡测"哪里是边界"，本卡测"边界两侧的操作代价差"——同一夹具族的
   互补两张。

## 边界诚实说明

- allocs=1 的字节数由实现决定（libstdc++ 按 capacity 分配，未写死在断言里）；"每次长串操作恰 1 次
  堆分配"是 C++11 起的标准语义（无 COW）+ 本机实测。Clang 列由 CI Cross-check 回填。
