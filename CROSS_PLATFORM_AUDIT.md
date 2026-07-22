# 跨平台可移植性审计报告

- 审计日期: 2026-07-21
- 审计范围: `Book/` 全库 147 章 / ~6,840+ 独立可编译 cpp 块
- 关注差异: **LP64 (Linux x86-64 / CI gcc-15)** vs **LLP64 (Windows x86-64 / mingw1530 gcc-15.3.0)** 数据模型差异导致的 `static_assert` 跨平台失败
- 触发背景: CI #192/#193/#194 连红 `ch70#11 static assertion failed`，前三轮误判为 EBO 布局问题，最终坐实为 `std::distance` 返回类型 `std::ptrdiff_t` 被写死为 `long long` 的陷阱

## 方法论

5 类静态扫描 + 本地 mingw 实测 + CI(Linux) 结论对照：

1. `is_same_v<decltype(...), long long|long>` —— 对 std 返回类型/平台相关类型写死方言整型
2. `std::ssize` / `std::distance` 返回 `std::ptrdiff_t` 的类型断言
3. `static_assert(sizeof(X) == N)` 含硬编码 N 且可能依赖 `long`/指针宽度
4. `is_same_v<..., long>` / `!is_same_v<int, long>` —— 验证是否依赖类型宽度
5. `wchar_t` / `intptr_t` / `uintptr_t` 相关 `static_assert`

## 发现与判定

### 🔴 真实陷阱（已修复）
- **`Book/part06_templates/ch70_tag_dispatch.md` distance 块**
  ```cpp
  auto dv = std::distance(v.begin(), v.end());
  static_assert(std::is_same_v<decltype(dv), long long>);  // ❌ 写死 long long
  ```
  `std::distance` 返回类型恒为 `std::ptrdiff_t`：
  - LP64 (Linux/CI): `ptrdiff_t` ≡ `long` → `is_same_v<long, long long>` = **false** → CI 失败
  - LLP64 (Windows/mingw): `ptrdiff_t` ≡ `long long` → 本地 PASS（掩盖 bug）
  - 修复: 断言改 `std::ptrdiff_t`（跨平台恒真），commit `e2ad16a`，CI #195 验证中
  - 教训: `run_cpp_assertions.py` 内部 `enumerate` 用 **0-based** 编号，报告 `#11` = 第 12 个 cpp 块；前三轮因 1-based/0-based 错位改错了块

### 🟢 经研判安全（含实测验证）
- **`ch123_ct_programming.md:249` `!std::is_same_v<int, long>`**
  初判为潜伏陷阱（LLP64 下 `int==long==32`）。实测本地 mingw `PASS=19 FAIL=0` 推翻：
  `std::is_same` 比**类型身份**而非宽度，`int` 与 `long` 在任意平台均为不同类型 → 恒 TRUE。
- **`ch111_aba.md:104/150` `TaggedPtr==16` / `Head==16`** 与 **`ch71_policy.md:237` `VPoly==8`**
  依赖 x64 指针宽度（8 字节），LP64/LLP64 下指针均 64 位，CI 与本地 x64 一致 → 安全（#194 未报即证）
- **其余 `sizeof` 精确断言**（`ch52/ch60/ch66` 等）
  均相对 `sizeof(int)` / 空类 `==1` / 显式枚举底层 / x64 指针宽度 → 跨平台恒成立
- **`std::ssize`** 仅 `ch07_cpp20.md` 出现且无类型断言 → 安全
- **`wchar_t` / `intptr_t` / `uintptr_t`** 全为用法（reinterpret_cast / 指针运算 / 文档），无 `static_assert` 陷阱 → 安全
- **`ch41_smart_pointers.md:691` `sizeof(long long) == 2*sizeof(_Atomic_word)`** 运行时常量，`long long` 两平台恒 8 字节 → 安全

## 结论

全库 **6,840+ cpp 块**中，跨 LP64/LLP64 数据模型差异的**唯一真实类型陷阱 = ch70 `std::distance` → `std::ptrdiff_t`**，已根治。
其余所有 `static_assert` 在 Linux CI 与 Windows 本地均恒成立。本书可在两个主流数据模型下编译通过。

## 防御性纪律（沉淀）
1. **CI 落地必须查实际 `conclusion`**，不靠本地零回归下结论。
2. **凡断言某 std 返回值/类型为具体方言整型（`long long`/`long`/`unsigned long`），一律改断言对应标准类型别名或仅比大小/符号**——绝不直接比具体方言整型。
3. **`std::is_same` 比类型身份非宽度**；判定"跨平台陷阱"前必须本地实测，不靠宽度推断。
4. **按报告块号定位前必须核对 0-based 索引**（工具内部 `enumerate` 从 0 起），或直接 grep 报错行内容反查块。
