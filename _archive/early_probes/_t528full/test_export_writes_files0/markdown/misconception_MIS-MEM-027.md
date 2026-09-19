# MIS-MEM-027（misconception）

## 正面

【误解】MIS-MEM-027 ASan 没报 = 没泄漏（把 sanitizer 的静默当成安全证明）
触发说法：跑了一遍 ASan，没报错，所以没有内存泄漏

## 背面

为什么错：退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用一个不携带信号的通道下判断
反例 1：ASan/LSan 的判定对优化档与对象存活位置高度敏感（实测三档 × 两结构 5 个数据点）：极简两节点环在 `-O0` 报 80 B/2 次分配、`-O2` 不报；树形结构（含 vector + 导航边）在 `-O0`/`-O1` 不报、加 `__attribute__((noinline))` 隔离构树后 `-O2` 报 224 B/4 次分配。同一份泄漏代码、不同档位的结论可以完全相反
反例 2：不依赖 sanitizer 的确定信号是存在的：夹具内 volatile 析构计数（destroyed=0 vs 3）与控制块 `use_count()`（= 局部持有 1 + 强边数）、`weak_ptr::expired()` 都能在没有任何 sanitizer 的环境下判定泄漏与否（实测 EV-MEM-036/037，MinGW 侧 sanitizer 本就 skip）
关联原子：ATOM-MEM-LEAK-001 ATOM-MEM-WEAK-001 ATOM-MEM-SHARED-001
