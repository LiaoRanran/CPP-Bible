# real_world — 开源项目架构赏析

平行核心章：跨章（当作「为什么这样设计」的实证）。

- 主参考：`so` `cppcon` `core` `cert`
- 计划内容（抽取知名项目片段作赏析，不整本搬运）：
  - 标准库实现：libstdc++/libc++ 的 `std::vector`/`std::string` 小字符串优化（呼应 Part0 A5 布局、A6 读编译器输出）
  - 引擎/框架：Chromium、Qt、Unreal 的某些 C++ 模式
  - CppCon 演讲中的「把坑讲清楚」案例（`[cppcon:20xx/title]`）
  - 每条赏析 = 现象 + 源码片段 + 用到的核心章知识点回链
- 引用键示例：`[cppcon:2019/type-deduction]` `[so:dingbat-reference]` `[core:xxx]`
