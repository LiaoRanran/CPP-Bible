---
id: EV-MEM-012
serves: [ATOM-MEM-UNIQUE-001]
kind: run
hypothesis: >-
  unique_ptr 移动转移所有权：移动后源被置空（get()==nullptr）、目标获得对象；析构恰好一次
  （唯一所有权，无双释放）。拷贝构造被删除——unique_ptr 不可拷贝，这是"唯一所有权"的编译期保证。
controlled_vars: 同一 Box 类型、同一编译器、同一 -O2；唯一变量 = 用移动还是拷贝构造 unique_ptr
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_unique_move.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_unique_move.cpp -o Examples/_atom_unique_move.asm
  g++ -std=c++23 -O2 Examples/_atom_unique_move.cpp -o build/_replay_umv.exe && ./build/_replay_umv.exe
artifact: Examples/_atom_unique_move.asm
artifact_sha256: 23a91759d786ca662ccdb8cbb9f43aded5424541b41e8c5f6d87c9099b710c63
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed"}    # "box destroyed count=" 进入工件（唯一析构可观测）
expected:
  run: 移动后源置空(a empty=1)、目标获对象(b->v=7)、析构恰好一次(destroyed count=1)
  asm: 析构路径真实存在（"destroyed" 字符串进入工件）
actual:
  run_cxx23_O2: "after move a empty=1|b->v=7|box destroyed count=1"
verdict: confirm
falsification: >-
  ① 若移动后源仍持有对象（a empty=0），则"移动转移所有权"被推翻 => refute；
  ② 若析构计数 != 1（双释放或泄漏），则"唯一所有权"被推翻 => refute；
  ③ 编译期证伪"可拷贝"：取消注释 `std::unique_ptr<Box> c = a;` 编译红，实测报错
     `error: use of deleted function 'std::unique_ptr<...>::unique_ptr(const std::unique_ptr<...>&)'`
     （[unique.ownership] copy deleted）——若拷贝可用则"唯一所有权"名存实亡。
  运行观测 ①②均成立（a empty=1 / count=1），编译期 ③成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  移动后 a 为空、b 持有对象，作用域末尾只有 b 析构一次（volatile g_destroy==1）——证明所有权
  唯一且转移干净，无双释放。拷贝被删是 [unique.ownership] 的硬保证，以编译错误形式堵死"共享同一
  对象"的歧义；这正是它区别于 shared_ptr 的根本（见 ATOM-MEM-SHARED-001）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **双重观测（转移 + 唯一析构）**：`a empty=1` 证明源交出对象，`count=1` 证明没有双释放——二者合起来
   才是"唯一所有权"的完整证据，而非只看一半。
2. **编译期证伪留痕**：拷贝删除用真实编译错误文本坐实（非引述），满足"注释断言须有实证"的纪律。
3. **与 RAII-001 自洽**：unique_ptr 就是"把堆指针交给栈对象管"的具体形态（构造获取、析构 delete）。
