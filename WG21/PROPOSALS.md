# WG21 提案整理 · PROPOSALS

> 关键提案索引：编号 / 标题 / 归入版本 / 动机。持续扩充。

## C++11（N3337，原 N/W 系列）
- **N1968** Rvalue References（右值引用）→ C++11，移动语义基础。⟶ ch115
- **N2658** Defining Move Special Member Functions → C++11。
- **N2672** Initializer Lists（统一初始化）→ C++11。⟶ ch32
- **N2761** `auto` 与 decltype 完善 → C++11。⟶ ch22
- **N2927** `nullptr` 与 `std::nullptr_t` → C++11。⟶ ch19
- **N2725** Lambda 表达式 → C++11。⟶ ch27
- **N2242** `constexpr` → C++11（后放宽）。⟶ ch21、ch69
- **N2249** `unique_ptr`/`shared_ptr` → C++11。⟶ ch48
- **N2660** `std::thread` 与相关 → C++11。⟶ ch93、ch102
- **N2429** 内存模型与原子 → C++11。⟶ ch107
- **N1836** `enum class` → C++11。⟶ ch25

## C++14（N4140）
- **N3649** 泛型 Lambda → C++14。⟶ ch27
- **N3638** 返回类型推导 → C++14。
- **N3656** `std::make_unique` → C++14。⟶ ch48
- **N3658** 广义 `constexpr` → C++14。

## C++17（N4659）
- **P0217R3** 结构化绑定 → C++17。
- **P0305R1** 选择初始化/if-switch 带初始化 → C++17。
- **P0226R1** `std::string_view` → C++17。⟶ ch82、ch81
- **P0138R2** `std::variant` → C++17。⟶ ch26、ch88
- **P0323R2** `std::optional` → C++17。⟶ ch88
- **P0298R3** `std::filesystem` → C++17。⟶ ch91
- **P0024R2** 并行算法执行策略 → C++17。⟶ ch99
- **P0067R1** `std::any` → C++17。⟶ ch89

## C++20（N4861）
- **P0734R0** Concepts → C++20。⟶ ch67
- **P1103R3** Modules → C++20。⟶ ch118
- **P0912R5** Coroutines → C++20。⟶ ch113
- **P0588R1** Ranges → C++20。⟶ ch90、ch119
- **P0515R3** 三路比较 `<=>` → C++20。
- **P1068R0** `std::span`（原 TS）→ C++20。⟶ ch82
- **P1135R2** `std::jthread`/stop_token → C++20。⟶ ch94、ch103

## C++23（N4950）
- **P0798R8** `std::expected` → C++23。⟶ ch88
- **P0429R9** `std::flat_map`/`flat_set` → C++23。
- **P2093R14** `std::print`/`std::format` 扩展 → C++23。⟶ ch131
- **P0881R7** `std::stacktrace` → C++23。
- **P2321R2** `std::zip_view` 等范围适配 → C++23。
- **P1467R9** 扩展 `float`/`enum` 的 `std::hash` 等。

## C++26（进行中，可能变动）
- **P2996R3** 静态反射（static reflection）⟶ ch74。
- **P0542R5 / 契约方向** Contracts 回归讨论 ⟶ ch121。
- **P2300R10** Sender/Receiver 执行器（std::execution）⟶ ch114。
- **P2641R?** 模块化标准库（std 模块）⟶ ch118。

## 提案阅读指引
- 官方：`https://www.open-std.org/jtc1/sc22/wg21/docs/papers/`
- 动机提炼：每条提案解决「旧写法痛点 + 新写法收益 + 兼容性」。
- 工业影响：标注哪类项目受益（库开发/嵌入式/高性能/前端）。

---
*随章节推进补充提案号与动机。*
