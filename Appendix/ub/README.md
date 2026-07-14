# 附录：未定义行为（UB）反例库

> **目的**：弥合「UB 的理论描述」与「工程冲击」之间的落差。每条 UB 给出
> **真实代码 → 编译器行为 → 运行时表现 → 根因 → 修复**。
>
> **本库定位**：跨章节反例合集，供 `Book/part04_memory/`（ch28/35/36/37/40/42）、
> `Book/part05_oo/`、`Book/part10_modern/` 等章交叉引用，强调「UB 不是警告，是未定义」。

---

## 0. 环境声明（重要，关乎证据可信度）

| 项 | 值 |
|----|----|
| 编译器 | MinGW-w64 GCC **15.3.0**（winlibs，x86_64-msvcrt-posix-seh）|
| OS | Windows 10/11 |
| **Sanitizer 运行时** | **缺失** —— 该发行版仅含 `asan.h`/`ubsan.h` **插件头**，未捆绑 `libasan.a`/`libubsan.a` |

**结论**：本机**无法链接并运行 ASan/UBSan 运行时**，故 sanitizer 的*栈回溯报告*
（stack-trace）在本库中以 `[DOC-REPORT]` 标记，取自 GCC/Clang 官方文档的*预期格式*，
**非本机捕获**；获取真实报告需在有 sanitizer 运行时的工具链上执行（见各例「复现命令」）。

**本库的真实（local）证据有三种，均为本机实测：**
1. **GCC 编译期警告**（`-Wuse-after-free` / `-Wdangling-pointer=` / `-Wstrict-aliasing`）—— GCC 13+ 已能静态识别部分 UB；
2. **无 sanitizer 下的运行时行为**（崩溃 / 静默错误值 / 看似正常）—— 直接演示「UB 不可预测」；
3. **`-O0` vs `-O2 -fstrict-aliasing` 输出分歧** —— 严格别名类 UB 的真实 miscompile 证据。

> 红线：本库**不伪造**任何 sanitizer 输出。凡 `[DOC-REPORT]` 均明确标注来源与「非本地捕获」。

---

## 1. 反例索引（第一批：内存 UB 5 例）

| # | 文件 | UB 类型 | 本机真实证据 | Sanitizer 工具 |
|---|------|--------|------------|:--------------:|
| 1 | [ub01_use_after_free.md](./ub01_use_after_free.md) | 释放后使用 | `-Wuse-after-free` + 静默运行 | ASan |
| 2 | [ub02_double_free.md](./ub02_double_free.md) | 双重释放 | `-Wuse-after-free` + 静默运行 | ASan |
| 3 | [ub03_stack_after_scope.md](./ub03_stack_after_scope.md) | 栈对象越界使用 | `-Wdangling-pointer=` + 静默运行 | ASan |
| 4 | [ub04_alignment_violation.md](./ub04_alignment_violation.md) | 对齐违例 | x86 静默通过（exit 0）| UBSan (alignment) |
| 5 | [ub05_strict_aliasing.md](./ub05_strict_aliasing.md) | 严格别名破坏 | -O0/O2 输出分歧 + `-Wstrict-aliasing` | —（UBSan 不覆盖）|

---

## 2. 如何在本机复现

```bash
# 编译期警告（本机可跑，无需 sanitizer 运行时）
GCC="C:/Qt/Tools/mingw1530_64/bin/g++.exe"
$GCC -std=c++23 -O1 -g -Wall ub01_use_after_free.cpp -o uaf && ./uaf

# 若要 ASan/UBSan 真实栈回溯，需在具备运行时的工具链执行（Linux GCC / Clang / MSVC）：
g++ -std=c++23 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer ub01_use_after_free.cpp -o uaf
./uaf      # → heap-use-after-free 栈回溯
```

> 严格别名 UB 的 miscompile 分歧**不依赖 sanitizer**，本机即可复现：
> `g++ -O0 ub05_strict_aliasing.cpp -o sa0 && ./sa0` 与
> `g++ -O2 -fstrict-aliasing ub05_strict_aliasing.cpp -o sa2 && ./sa2` 输出不同。

---

## 3. 通用修复原则（跨所有 UB）

1. **RAII / 智能指针**：用 `std::unique_ptr`/`std::shared_ptr`/`std::vector` 取代裸 `new`/`malloc` + 手动 `free`，从根源消除生命周期类 UB。
2. **不保存局部对象地址**：返回对象用值/移动，或 `std::reference_wrapper`；跨作用域传递用堆对象或 `std::shared_ptr`。
3. **类型双关用 `std::bit_cast` / `memcpy`**：绝不 `reinterpret_cast` 跨不兼容类型；C++20 `std::bit_cast<T>(u)` 是定义良好且零开销的位重解释。
4. **开启 sanitizer CI 矩阵**：在 CI 中对 Debug 构建跑 ASan+UBSan+TSan，把 UB 挡在合并前。
5. **`-Wall -Wextra` 当门禁**：GCC 13+ 的 `-Wuse-after-free` / `-Wdangling-pointer=` 已能静态抓到相当多生命周期 UB。

---

_本库与正文解耦（置于 `Appendix/`，不进入门禁章节扫描）。正文相关章以交叉引用指向本库各例。_
