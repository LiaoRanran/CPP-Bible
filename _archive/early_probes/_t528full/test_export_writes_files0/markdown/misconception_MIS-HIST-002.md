# MIS-HIST-002（misconception）

## 正面

【误解】MIS-HIST-002 auto_ptr 反正被移除了，C++17 里编译不过
触发说法：C++17 起 auto_ptr 就没了，肯定编译失败

## 背面

为什么错：实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>）
反例 1：libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在 GCC 上看着还能用，换工具链即断）
关联原子：ATOM-HIST-AUTOPTR-001
