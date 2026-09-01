# qt — Qt 框架详细

平行核心章：`Book/part14_engineering`（工程实践）/ 实际应用案例。

- 主参考：`msvc`、`gcc`、`book:primercpp`、`cppref:cpp/...`
- 计划内容：
  - 元对象系统（moc）、信号槽（对比 `std::function`/观察者模式）、对象树与父子内存管理（RAII 之上）
  - 事件循环与跨线程（`Qt::QueuedConnection` 对比 C++ 内存模型 `[std-cpp23]`）
  - 与标准库协作：`QString`↔`std::string`、容器互操作、智能指针
  - 跨平台坑：MSVC/GCC/Clang 下 Qt 行为差异（标 `[msvc:ext]`/`[gcc:ext]`）
- 引用键示例：`[msvc:ext]` `[book:primercpp:secxx]` `[std-cpp23]`
