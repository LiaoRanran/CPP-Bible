# EXPANSION_RECIPES.md — Top 5 扩写处方

> 由 `expansion_audit.py` 数据驱动 + 逐章源码分析生成
> 每章预估时间含：写代码 + 跑编译验证 + 命令行测性能 + 搜 GitHub issue

---

## Recipe 1: ch64_fold（综合 79/100 — 样例重灾）

**现状**：101 个 cpp 块 / 94 浅（93%）/ 自含 13（13%）/ 0 工业引用
**节结构**：学习目标 → 速查 → 核心结构 → 空包处理 → 适用场景 → 完整示例 → 二元折叠 → 一元折叠 → 逗号折叠 → 与变参对比 → 编译期折叠 → 工业陷阱

### 操作（3-4h）

1. **样例重构（2h）**
   - 当前 ~94 个 <5 行散块分别展示 `(... + args)`、`(... * args)` 等语法变体
   - 合并为 12 个完整程序，每个针对一个应用场景：
     - (1) 求和/求积/字符串拼接（覆盖二元折叠 3 种运算符）
     - (2) 逗号折叠 + 打印所有参数
     - (3) 一元折叠 + 空包处理（`&& true`/`|| false`）
     - (4) 编译期 `static_assert` 用折叠验证属性
     - (5) 变参 `std::cout` vs 折叠对比
     - (6) 类型萃取：`is_all_same<Ts...>`
     - (7) 继承链：`(Ts::value && ...)`
     - (8) SFINAE + fold：`enable_if` + 折叠条件
     - (9) `std::apply` + fold 组合
     - (10) 实际场景：日志格式化参数
     - (11) 实际场景：编译期配置校验
     - (12) 性能对比：fold vs 手写递归 vs 运行时循环
   - 每个含 `#include` + `int main()` + 输出注释，可独立编译运行

2. **工业引用（30min）**
   - 找 LLVM/Clang 源码中 fold expression 的实际使用：`clang/lib/Sema/SemaTemplateVariadic.cpp`
   - 找 Boost.Hana / folly 中 fold 实现
   - 引用 1-2 个真实 issue：如 GCC fold expression bug (gcc.gnu.org/bugzilla)

3. **广度（30min）**
   - 补交引 → ch63（变参模板，fold 的前置知识）
   - 补交引 → ch68（TMP，编译期折叠的元编程背景）
   - 补交引 → ch121（contracts，编译期断言 vs 折叠验证）

4. **验证**
   - `run_cpp_assertions.py` 确认 FAIL=0
   - `consistency_check.py` 确认门禁 100/100
   - `expansion_audit.py --chapter ch64_fold` 预期 79→<60

---

## Recipe 2: ch04_cpp11（综合 78/100）

**现状**：49 个 cpp 块 / 46 浅（94%）/ 自含 26（53%）/ 13 处估算 / 0 工业
**节结构**：学习目标 → 前置知识 → 后续依赖 → 知识图谱 → Mermaid → 移动语义 → 智能指针 → lambda → auto → 范围for → constexpr → nullptr → ...

### 操作（2-3h）

1. **样例重构（1h）**
   - C++11 演化章的特性展示格式可保留，但补 3 个贯穿性大示例：
     - (1) **移动语义贯穿例**：从原始指针 → `unique_ptr` → `move` → 工厂函数 → 返回值优化，展示 C++11 的完整故事线
     - (2) **lambda 贯穿例**：从函数指针 → `std::function` → lambda → 闭包捕获 → 结合 STL 算法
     - (3) **类型推导贯穿例**：`auto` → `decltype` → 尾置返回类型 → `decltype(auto)`

2. **实证替换（1h）**
   - 13 处 `~N单位` 估算用语，逐条 GCC 13.1 `-O2` 实测替换
   - 对移动语义、`unique_ptr` 开销、lambda vs 函数指针加 Compiler Explorer 汇编链接

3. **工业引用（30min）**
   - C++11 是工业分水岭——引用真实的"从 C++03 迁移到 C++11"案例
   - 如 Chromium 的 `scoped_ptr` → `std::unique_ptr` 迁移 commit

4. **验证**：`hy3_check.py`

---

## Recipe 3: ch62_specialization（综合 77/100）

**现状**：94 个 cpp 块 / 84 浅（89%）/ 自含 23（24%）/ 0 估算 / 0 工业

### 操作（2-3h）

1. **样例重构（1.5h）**
   - 84 个浅块 → 11 个完整程序：
     - 全特化 + 偏特化 + 函数模板特化 + 类模板偏特化 + 变量模板特化
     - `std::hash` 自定义特化（真实用例）
     - `std::numeric_limits` 自定义类型特化
     - 特化 + SFINAE 组合
     - 偏序规则完整示例（多个特化候选，展示编译器选择）
     - 特化 vs 重载的分辨示例

2. **工业引用（30min）**
   - `std::hash<std::string>` 特化源码引用（libstdc++）
   - `std::char_traits` 特化实际用法
   - folly/abseil 中的特化惯用法

3. **验证**：`hy3_check.py`

---

## Recipe 4: ch61_template_overload（综合 77/100）

**现状**：77 个 cpp 块 / 65 浅（84%）/ 自含 11（14%）/ 0 估算 / 1 工业

### 操作（2h）

1. **样例重构（1h）**
   - 合并为 9 个完整程序：
     - 重载优先级完整演示（非模板 > 特化 > 通用模板）
     - SFINAE + 重载组合（`enable_if` 控制重载集）
     - Concepts（C++20）重载 vs SFINAE 重载对比
     - 变参模板重载
     - 实际场景：`to_string` 多类型重载

2. **交引**：CROSSREF 已显示 ch61↔ch62 密切相关，补更明确指引

3. **验证**：`hy3_check.py`

---

## Recipe 5: ch60_template_basics（综合 76/100）

**现状**：83 个 cpp 块 / 69 浅（83%）/ 自含 18（22%）/ 0 估算 / 1 工业

### 操作（2h）

1. **样例重构（1h）**
   - 合并为 10 个完整程序：
     - 函数模板 + 类模板 + 成员模板 + 别名模板基础
     - 隐式实例化 vs 显式实例化完整对比
     - 两阶段查找完整示例（依赖名 vs 非依赖名）
     - 模板参数推导（含 C++17 CTAD）
     - 默认模板参数

2. **汇编（30min）**
   - 模板实例化后的代码膨胀 → Compiler Explorer 看编译器如何为不同 T 生成代码
   - 两阶段查找的汇编层面影响

3. **验证**：`hy3_check.py`

---

_生成时间：2026-07-11 | 数据源：expansion_audit.py JSON + 逐章源码分析_
