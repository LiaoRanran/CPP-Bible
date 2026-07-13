# Agent 速查卡：撰写章节的最小必要规则

> 每个 agent 开局读此文件（**仅此一个**），CONVENTIONS.md/INDEX.md/ch88 样板由主控在 prompt 中内联关键摘要。

---

## 一、结构硬门禁

```
# 第XX章 标题
> 立场: C++23 / 标准基:C++23 / 编译器:GCC13.1-MinGW / 预计阅读:XXmin / 前置:⟶chXX / 后续:⟶chXX / 难度:★★★☆☆

## ① …（意图/目标/范围）
## ② …（前置知识）
...
## ⑳ …（<-- 标题禁用"推荐阅读/参考文献/延伸阅读"，改用"跨语言对比"或"源码阅读路线"）

附录A: 完整可编译示例集
```

- ✅ **20 个圈码二级标题** `## ① …`~`## ⑳ …`（①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳）
- ✅ 每章 **≥30 个 `` ```cpp `` 块**
- ✅ 每个 cpp 块**独立完整可编译**（#include+定义+int main(){}），禁止裸片段
- ✅ 立场标签：`[标准]` `[实现·GCC13]` `[平台·x86-64]` `[经验]`
- ✅ libstdc++ 源码引用必须同时给 `文件：<路径>` 和 `行号：<范围>`
- ✅ 交叉引用 `⟶ Book/partXX/chYY_xxx.md`（≥3 条）
- ❌ **厳禁**独立 `## 推荐阅读` / `## 参考文献` / `## 延伸阅读`
- ❌ **不改** GLOSSARY.md / CROSSREF.md / INDEX.md

---

## 二、代码编译门禁

**编译命令**：
```
C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -Wall -Wextra
```

**GCC 13.1 限制（必须规避）**：

| 不可用 | 替代 |
|---|---|
| `<print>` | `<iostream>` + `std::cout` |
| `<mdspan>` | `<span>` + 手写多维索引 |
| `<flat_map>` | `<map>` |
| `<flat_set>` | `<set>` |
| `<generator>` | 手写 coroutine_handle + promise（或用文字说明） |
| `operator""_x` (无空格 UDL) | `operator"" _x` |
| `#if __cplusplus >= 202302L` | `#if __cplusplus >= 202002L`（GCC13=`202100`） |
| `(void)(args...)` 折叠丢弃 | `((void)args, ...)` |
| 命名空间/全局裸语句 | 包进函数体 |

---

## 三、自检与交付

**自检脚本**：
```
C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe tools/chapter_compile_check.py Book/partXX/chYY_xxx.md
```

- 输出必须 **`0 fail`**。有 fail 则读首条 error，修正对应块，重跑。
- 可批量检查：`...chapter_compile_check.py Book/partXX/chA.md Book/partXX/chB.md`

**交付汇报格式**：
```
chXX: 行=N cpp=N 圈码=20 禁词=0 chapter_compile_check: N blocks, 0 fail
chYY: 行=N cpp=N 圈码=20 禁词=0 chapter_compile_check: N blocks, 0 fail
```

---

## 四、深度要求速览

| 维度 | 标准 |
|---|---|
| 篇幅 | ≥900 行/章 |
| 汇编 | 每个关键特性至少一段 ` ```asm`（`-O2` 编译输出，标注指令含义） |
| 内存图 | ASCII 对象/缓存/虚表布局 |
| 源码 | libstdc++ 源码摘录（文件+行号，嵌在注释形式可编译 cpp 内） |
| benchmark | microbenchmark 给出数量级数字（如 "O(N log N) vs O(N²) 在 N=10000 时 xxμs vs xxms"） |
| 跨语言 | ⑳ 至少与 Rust/Go/Java/C# 中两种对比 |
| 工业案例 | 禁用 HelloWorld，用服务器/DB/引擎/网络/交易等 |
| 错误示例 | ❌ 错误 → ✅ 正确 → 解释差异 |

---

## 五、文件命名规则

```
Book/part07_stl/ch82_span.md        # snake_case, 章号+下划线+主题
Book/part10_modern/ch115_move.md
Book/part14_perf/ch152_perf_model.md
```

---

## 六、常见自陷

1. **int main 内写了线程但没 join/detach** → `std::terminate` → 编译通过但运行时炸。所有线程示例必须 join 或 detach。
2. **协程 <coroutine>**：GCC13 支持语法的子集，简单 generator 可编译，复杂 awaitable 需要 libstdc++ 特定头 → 优先用已验证模式（`suspend_always`/`suspend_never`）。
3. **__rdtsc** 需要 `#include <x86intrin.h>`（不是 `<immintrin.h>`）。
4. **std::hardware_destructive_interference_size** 在 GCC13 `<new>` 中已定义，可直接用。
5. **constexpr 函数内禁止** `std::cout` → 用 `static_assert` 验证编译期结果。
