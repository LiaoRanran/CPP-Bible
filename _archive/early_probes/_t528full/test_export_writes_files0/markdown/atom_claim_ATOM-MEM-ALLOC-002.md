# ATOM-MEM-ALLOC-002（atom_claim）

## 正面

【MEM】ATOM-MEM-ALLOC-002
以下论断是否成立？依据是什么？
三种小对象分配策略的元数据开销与**是否支持单块释放**绑定，可用统一口径 （struct_bytes + bookkeeping_bytes）量化：同一 workload（1000 次 24 B 分配，-O2）下， arena 元数据 total 32 B（struct 32 + bookkeeping 0，**前提：仅批量申请 + 整体释放—— 夹具 `release_all()` 只支持整体重置，中途释放单块会产生不可复用空洞**）； bitmap total 181 B（struct 56 + bookkeeping 125 B = 1 bit/块，且随块数线性增长： n=8000 时 1056 B）；pool total 8056 B（struct 56 + bookkeeping 8000 B = 8 B/块 free-list 指针，n=8000 时 64056 B）——排序为 arena << bitmap << pool， 与"pool 元数据最省"的直觉相反；内部碎片：arena 0、pool 8000 B （定长块 32 B => 8 B x 1000）、bitmap 0（位图不占用户区）。

## 背面

论断：三种小对象分配策略的元数据开销与**是否支持单块释放**绑定，可用统一口径 （struct_bytes + bookkeeping_bytes）量化：同一 workload（1000 次 24 B 分配，-O2）下， arena 元数据 total 32 B（struct 32 + bookkeeping 0，**前提：仅批量申请 + 整体释放—— 夹具 `release_all()` 只支持整体重置，中途释放单块会产生不可复用空洞**）； bitmap total 181 B（struct 56 + bookkeeping 125 B = 1 bit/块，且随块数线性增长： n=8000 时 1056 B）；pool total 8056 B（struct 56 + bookkeeping 8000 B = 8 B/块 free-list 指针，n=8000 时 64056 B）——排序为 arena << bitmap << pool， 与"pool 元数据最省"的直觉相反；内部碎片：arena 0、pool 8000 B （定长块 32 B => 8 B x 1000）、bitmap 0（位图不占用户区）。
边界：{'standard': ['C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0 (MinGW-w64)', 'GCC 14.2.0 (WSL)'], 'opt': ['-O2'], 'platform': ['x86-64']}
关键证据：
  - EV-MEM-040: confirm
  - EV-MEM-041: confirm
常见误解：
  - MIS-MEM-030
