# build — 构建系统（CMake 为主）

平行核心章：`Book/part14_engineering`（工程实践）/ 实际应用案例；另 `Part0_Prerequisites/` 工具链章。

- 主参考（离线）：`cmake:` → `docs/references/external/vendor/cmake-doc/manual/`（CMake 官方概念文档 + 命令/变量/模块/策略总索引）
- 在线补充：命令/变量/模块/策略**逐页 leaf** 见 `cmake.org/cmake/help/latest/`（本机可达）
- 计划内容：
  - 现代 CMake 目标模型（`target`/`prop`/`INTERFACE`）、`target_*` 命令 vs 旧式全局变量
  - 生成器表达式、`find_package` 的 `CONFIG`/`MODULE` 模式、导出与 `install`、relocatable package
  - toolchain 文件、`CMakePresets.json`、交叉编译（呼应 Part0 交叉编译章）
  - 与框架集成：Qt（`qt:` `cmake-manual`）、UE 的 `Build.cs`、vcpkg / Conan
  - 陷阱：全局 `include_directories`、`add_compile_options` 误用、非 relocatable、隐式依赖
- 引用键示例：`[cmake:cmake-buildsystem.7]` `[cmake:cmake-language.7]` `[std-cpp23]`
