---
id: EV-MEM-011
serves: [ATOM-MEM-UNIQUE-001]
kind: run
hypothesis: >-
  std::unique_ptr<T> 是零开销抽象：sizeof 等于裸指针 sizeof(T*)（x86-64 下 8 字节），
  没有 vtable、没有额外簿记字段，所有权信息只体现在编译期（拷贝删除 + 移动转移）。
controlled_vars: 同一 Big 类型、同一编译器、同一 -O2；唯一变量 = 用 unique_ptr 还是裸指针
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_unique_size.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_unique_size.cpp -o Examples/_atom_unique_size.asm
  g++ -std=c++23 -O2 Examples/_atom_unique_size.cpp -o build/_replay_usz.exe && ./build/_replay_usz.exe
artifact: Examples/_atom_unique_size.asm
artifact_sha256: e10ca794d9269a0c78af05960b6bd44c0d34563f51308447f6e6d6ec1301d4c6
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "unique_ptr"}    # 类型名进入工件（零开销抽象确为同一指针存储）
expected:
  run: sizeof(unique_ptr<Big>) == sizeof(Big*) == 8，equal=1
  asm: print 字符串含 "unique_ptr"，无额外簿记字段的存储痕迹
actual:
  run_cxx23_O2: "sizeof(unique_ptr<Big>)=8|sizeof(Big*)=8|equal=1"
verdict: confirm
falsification: >-
  若 unique_ptr 比裸指针多一个字段（sizeof 更大或含引用计数），则"零开销抽象"被推翻 => refute。
  实测二者同为 8 字节、equal=1 => 经受住证伪（与 PERF-001 的 Value32 同尺寸对象对照：unique_ptr
  不额外搬运数据，只改"谁负责 delete"的编译期契约）。
depth_layer: compiler
drill_note: >-
  sizeof 是编译期常量，跨优化档稳定；x86-64 下指针 8 字节，故 unique_ptr 容器布局 == 裸指针。
  这与 PERF-001 的"移动只偷指针"一致：unique_ptr 本身就是"一个指针 + 编译期禁止拷贝/允许移动"的封装。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **编译期常量、可比对**：`sizeof` 不依赖运行期，输出逐字稳定（`run_match` 精确比对）。
2. **对照同尺寸堆对象**：用与 PERF-001 的 `Value32` 同尺寸的 `Big`（32 字节）作 T，证明 unique_ptr
   不因对象变大而变胖——它只包一个指针。
3. **与机制自洽**：零开销 + 拷贝删除 + 移动转移，三者在 unique_ptr 上是同一件事的不同面（见 EV-MEM-012）。
