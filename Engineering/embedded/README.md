# embedded — 嵌入式 C/C++

平行核心章：Part0（汇编 + C）/ 系统编程。

- 蓝本：`C:\Users\ASUS\Desktop\cppb参考资料\嵌入式\`（29 篇 MD，本地素材）
- 主参考：`std-c11` `cert` `book:krc`
- 计划内容：
  - 无 libc / 无堆环境：自定义 `malloc`、静态分配、`placement new` `[cppref:cpp/memory/new]`
  - 寄存器与位带：用 Part0 A2 的 `lea`/位运算操作硬件；volatile 的正确与误用（`[cert:vol]`）
  - 中断与 RTOS：临界区、原子（对比 C++ `std::atomic` `[std-cpp23]`）
  - 对齐与 packing：呼应 Part0 A5（`#pragma pack`/`alignas` 在 MCU 上的后果）
  - 与 Linux 内核 C 的差异（见 `../linux_kernel/`）
- 引用键示例：`[std-c11]` `[cert:vol]` `[cppref:cpp/language/alignas]`
