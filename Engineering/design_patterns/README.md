# design_patterns — 设计模式（GoF + 现代 C++）

平行核心章：`Book/part15_design/`（ch159–164）。

- 主参考：`book:tour`、`core`、`isocpp`、`cppref:cpp/...`
- 计划内容（每条=意图 + 经典实现 + **现代 C++ 实现**（用 `std::function`/模板/CRTP 替代继承）+ 反模式 + 与 STL/泛型结合）：
  - 创建型：Factory / Builder / Singleton（含 Meyers 单例、`inline` 变量）
  - 结构型：Adapter / Bridge / Decorator / Facade / Proxy
  - 行为型：Strategy（用 `std::function` 替代）/ Observer（信号槽）/ Command / Visitor（双分派）/ Template Method（CRTP 非虚）
  - 现代补充：RAII 即 C++ 最原生模式、PIMPL、类型擦除（`std::any`/`std::function` 原理）
- 引用键示例：`[book:effective-cpp:itemxx]` `[core:C.130]` `[std-cpp23]`
