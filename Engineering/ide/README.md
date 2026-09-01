# ide — IDE 使用建议

平行核心章：`Book/part02_toolchain/`（工具链与构建）。

- 主参考：`msvc` `gcc` `clang`
- 计划内容：
  - Visual Studio：断点/条件断点/内存视图/调用栈；MSVC STL 源码单步（`[msvc]`）
  - Qt Creator：与 qmake/CMake 集成、信号槽跳转
  - CLion / VS Code：clangd、CMake Presets、格式化（clang-format，呼应 Core Guidelines 风格）
  - 与 CI：本地格式化 + 静态分析集成，避免 push 触发 `quality` 门禁失败
- 引用键示例：`[msvc:ide]` `[gcc:cmake]` `[core:fmt]`
