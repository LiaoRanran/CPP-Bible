# debugging — 调试技巧 / 崩溃复盘

平行核心章：`Book/part02_toolchain/`（工具链）/ `Book/part14_engineering`。

- 主参考：`gcc` `clang` `msvc` `ubsan` `asan` `so`（调试类高频帖）
- 计划内容：
  - 工具：gdb / WinDbg / VS 调试器 / Qt Creator 调试；`[gcc]` `-g -Og` 编译选项
  - 消毒器：AddressSanitizer / UBSan / ThreadSanitizer 复现代码（`[asan:heap-buffer-overflow]` `[ubsan:signed-overflow]`），用来校验手册示例是否触发 UB
  - 崩溃复盘：段错误/访问违例、核心转储、栈回溯（呼应 Part0 A3 栈帧）
  - 静态分析：`-fsanitize`、clang-tidy、MSVC `/analyze`
- 引用键示例：`[gcc:fsanitize]` `[ubsan:xxx]` `[asan:xxx]` `[clang:tidy]`
