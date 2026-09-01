# unreal — 虚幻引擎 C++ 实战

平行核心章：`Book/part14_engineering`（工程实践）。

- 主参考：`msvc`、`book:tour`、`cppref:cpp/...`
- 计划内容：
  - UObject / UClass 反射与 `UCLASS`/`UFUNCTION` 宏（对比 C++ RTTI `[std-cpp23]`）
  - 垃圾回收（对比 `std::shared_ptr`/`unique_ptr` `[book:effective-modern:item]`）
  - 游戏框架模式：Actor/Component、单例子系统、委托（对比 `std::function`）
  - 与标准库边界：引擎容器（`TArray`/`TMap`）vs `std::`；何时用哪种
  - 性能：`UPROPERTY` 标记的内存布局影响（呼应 Part0 A5 对齐）
- 引用键示例：`[msvc:ext]` `[std-cpp23]` `[book:effective-modern:itemxx]`
- 官方文档：**在线** `ue:` → `docs.unrealengine.com`（本机 403，需登录；未 vendored）。涉及 UE 反射/GC/容器的事实性陈述以此在线文档为准，并标 `[ue:...]` 以备溯源。
