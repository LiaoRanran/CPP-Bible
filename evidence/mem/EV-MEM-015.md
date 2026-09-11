---
id: EV-MEM-015
serves: [ATOM-MEM-WEAK-001]
kind: run
hypothesis: >-
  std::weak_ptr 是非拥有观察者：指向 shared_ptr 管理的对象但不增加引用计数；.lock() 临时提升为
  shared_ptr（对象活着则提升成功、计数 +1），对象已销毁则 .lock() 返回空（expired()==true）。
controlled_vars: 同一 Box 类型、同一编译器、同一 -O2；唯一变量 = 用 weak_ptr 旁观还是 shared_ptr 拥有
matrix:
  compiler: [GCC 15.3.0]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_weak_obs.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_weak_obs.cpp -o Examples/_atom_weak_obs.asm
  g++ -std=c++23 -O2 Examples/_atom_weak_obs.cpp -o build/_replay_wobs.exe && ./build/_replay_wobs.exe
artifact: Examples/_atom_weak_obs.asm
artifact_sha256: cf0453ebd15e23434daefcf4a28c33e381dee95f3871c20a581857b6fb7b3230
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed"}    # "box destroyed count=" 进入工件
expected:
  run: weak 不增计数(=1)；lock 后计数+1(=2)、提升成功(=1)；reset 后 expired(=1)、对象析构(=1)
  asm: 析构路径（"destroyed"）真实存在
actual:
  run_cxx23_O2: "use_count with weak=1|weak expired before=0|use_count after lock=2|locked bool=1|use_count after lock scope=1|weak expired after reset=1|box destroyed count=1"
verdict: confirm
falsification: >-
  若 weak_ptr 增加了引用计数（use_count with weak != 1），或对象销毁后 .lock() 仍成功（expired==0），
  则"weak 是非拥有观察者"被推翻 => refute。实测 weak 不增计数、reset 后 expired=1、destroyed=1 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  weak_ptr 只持有控制块指针（不持对象、不增强引用计数），故不影响对象寿命；.lock() 在控制块上原子地
  尝试提升，对象已销毁则提升失败。这与 SHARED-001 的计数语义一致：weak 动的是"弱计数"而非强计数。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **不增计数可直接观测**：`use_count with weak=1` 证明 weak 旁观不延长寿命（对比 shared 拷贝必 +1）。
2. **提升/过期两态都验证**：lock 成功（bool=1、计数+1）与 reset 后 expired=1（lock 失败）覆盖两种状态。
3. **与 SHARED-001 自洽**：weak 是 shared 的配套——共享用 shared、旁观用 weak，避免循环引用。
