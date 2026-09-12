---
id: EV-MEM-044
serves: [ATOM-MEM-PERF-004]
kind: run
hypothesis: >-
  两个"逻辑上独立"的变量是否落在**同一条缓存行**可由地址直接判定（不依赖计时）：
  相邻布局 `tight_same_line=1`（伪共享成立），`alignas(hardware_destructive_interference_size)`
  隔离后 `padded_same_line=0`（消除）；POD 结构体的相邻成员同样命中 ⇒ 伪共享的**结构性前提**
  可确定性观测。
controlled_vars: 同一夹具、同一判据函数、同一编译档；唯一变量 = 布局（相邻 vs alignas 隔离）；判据自带活性对照与反例对照
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 跨平台确定性对照（可核对锚）：WSL 复跑命令
  #   `g++-14 -std=c++23 -O2 Examples/atoms/_atom_false_sharing.cpp`，输出与 Windows 侧**逐字相同**
fixture: Examples/atoms/_atom_false_sharing.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_false_sharing.cpp -o Examples/atoms/_atom_false_sharing.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_false_sharing.cpp -o build/_replay_false_sharing.exe && ./build/_replay_false_sharing.exe
artifact: Examples/atoms/_atom_false_sharing.asm
artifact_sha256: 9a97596f1792a72502bcd84a3d13f203d142e55118309d40ead1ac777d860f80
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["tight_same_line=", "padded_same_line="]}     # 布局判据的打印格式串
  - {kind: contains_any, texts: ["self_same_line=", "cross_object_same_line="]} # 活性/反例对照的格式串
expected:
  run: >-
    缓存行 64 字节、atomic<long long> 8 字节；tight 相邻（偏移 8）⇒ 同一行 =1；
    alignas 隔离后偏移 64、`padded_sizeof=128` ⇒ 不同行 =0；POD 相邻成员同样 =1（真实场景）；
    判据自身活性对照 `self_same_line=1`（同一对象必然同行）与反例对照
    `cross_object_same_line=0`（不同对象强制分行的判据会翻转）。
  asm: 四条判据的打印格式串在工件 `.rodata` 中可见（断言不依赖任何 mangle 符号）
actual:
  run_cxx23_O2: "cache_line_size=64|atomic_ll_size=8|tight_offset_bytes=8|tight_same_line=1|padded_offset_bytes=64|padded_same_line=0|padded_sizeof=128|pod_offset_bytes=8|pod_same_line=1|same_object_members_same_line=1|cross_object_same_line=0|kline_source=std"
verdict: confirm
falsification: >-
  **真对照（唯一变量 = 布局）**：若 `alignas` 不产生隔离，`padded_same_line` 应为 **1**
  —— 实测 **0**；反方向若判据失灵（把任何地址都判成同行），`cross_object_same_line` 应为 1
  —— 实测 **0**（判据会翻转）。若判据把同一对象的成员判成不同行，`self_same_line` 应为 0
  —— 实测 **1**。
  **与性能侧的交叉印证（另一张卡）**：同一布局差异在 EV-MEM-045 中对应
  `ratio_tight_over_padded_x1000=18860`（Windows）/ `18538`（Linux）⇒ 结构判据与性能后果一致，
  两条独立证据链指向同一因果（缓存行共享）。
depth_layer: runtime
drill_note: >-
  "伪共享"的教学难点是它**看不见**：两个变量语义独立、无数据竞争、代码正确，性能却掉一个数量级。
  本卡的价值是给出一个**不依赖计时**的判据：`reinterpret_cast<uintptr_t>(&a)/kLine == ...(&b)/kLine`
  —— 只要地址能取到，任何平台上都能当场判定结构前提是否成立。计时留给 EV-MEM-045（并明确标注
  跨机器不可复现）。
---

# EV-MEM-044 · 伪共享的结构前提：缓存行共享可确定性判定

## 观测（Windows/MinGW 15.3.0 与 WSL/g++-14 **逐字相同**）

| 读数 | 值 | 含义 |
|---|---|---|
| `cache_line_size` | 64 | `std::hardware_destructive_interference_size` |
| `tight_offset_bytes` / `tight_same_line` | 8 / **1** | 相邻 ⇒ **同一行** ⇒ 伪共享成立 |
| `padded_offset_bytes` / `padded_same_line` | 64 / **0** | `alignas` 隔离 ⇒ 消除 |
| `padded_sizeof` | 128 | 填充后的对象大小（代价：空间） |
| `pod_offset_bytes` / `pod_same_line` | 8 / **1** | POD 相邻成员同样命中（最常见的真实场景） |
| `same_object_members_same_line` | 1 | **活性对照**：同一对象的两个**不同成员**同行（真运行时比较） |
| `kline_source` | std | 缓存行常量来源（`std` / `fallback64`）——区分"实现给的真值"与"回退常量" |
| `cross_object_same_line` | 0 | **反例对照**：强制分行后判据会翻转 |

## 边界

- 判据给出的是**前提**（是否共享缓存行），不是后果（性能下降多少）——后果由 EV-MEM-045 量化；
- `hardware_destructive_interference_size` 在部分实现上不可用（本夹具带 `#else` 回退 64 并打印实际值）；
- 本卡不断言"padding 一定值得"：`padded_sizeof=128` 是空间代价，是否值得取决于访问模式（见原子卡的边界节）。
