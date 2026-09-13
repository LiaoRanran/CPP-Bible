# MIS-MEM-031（misconception）

## 正面

【误解】MIS-MEM-031 ASan/LSan 没报泄漏就是没有泄漏（把一次工具运行的静默当安全证明）
触发说法：跑了一遍 ASan，没报错，所以没有内存泄漏

## 背面

为什么错：**本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_leak=1`），而在 WSL/Linux 用 `-O1 -g -fsanitize=address,undefined` 运行，stderr **没有任何 LeakSanitizer 报告**（无 `ERROR: LeakSanitizer`、无 `SUMMARY: ... leaked`）
反例 1：**且不能归因于"简单内联"**：同一夹具的 `run_cycle()`/`run_scoped()`/`run_owned()` **本就带 `__attribute__((noinline))`**（构环函数被隔离在独立函数里）⇒ 最直接的内联解释已被排除，说明\"没报\"的成因不止一种
反例 2：**同族证据（LEAK-001）已证\"报与不报可完全相反\"**：极简两节点环 `-O0` 报 80 B/2 次分配、`-O2` 不报；树形夹具 `-O0`/`-O1` 不报、加 `noinline` 隔离后 `-O2` 报 224 B/4 次分配——同一份泄漏代码、不同档位结论相反
关联原子：ATOM-MEM-LEAK-002 ATOM-MEM-LEAK-001 ATOM-MEM-WEAK-001 ATOM-MEM-SHARED-001
