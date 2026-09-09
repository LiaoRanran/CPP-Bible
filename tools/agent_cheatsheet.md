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
C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++23 -O2 -Wall -Wextra
```

**GCC 13.1 历史约束（当前主编译器 GCC 15.3.0，下述多数限制在 15.3 已解除；保留为历史参考）**：

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

---

## 七、L2 深耕工具（注释型空块清理管线）

> 真机实证深耕时不再手写临时脚本，用下列两条命令替代（block 号 = compile_all 报告号）。

```
# 1) 盘点：全库或单章纯注释 cpp 块（只认 ```cpp 围栏，与 CI 编译编号一致）
python tools/comment_blocks.py scan --all
python tools/comment_blocks.py scan --chapter ch42            # 单章嫌疑块清单
python tools/comment_blocks.py scan --chapter ch42 --dump     # + 打印正文供判 A/B/C
python tools/comment_blocks.py scan --chapter ch42 --all-block# 全块概览核对编号

# 2) 替换：按 patch JSON 安全批量改块正文（dry 默认 / --apply 落盘）
python tools/patch_blocks.py Book/partX/chYY.md patch.json
python tools/patch_blocks.py --apply Book/partX/chYY.md patch.json

# 3) 运行期输出断言：跑含 //@ 的 main 块，stdout 与期望逐条比对（可 --check 挂 CI）
python tools/run_expected.py --all
python tools/run_expected.py --chapter ch42
python tools/run_expected.py --changed

# 4) 覆盖状态机：纯注释块存量落 tools/l2_state.json（回潮/新增可检出）
python tools/l2_state.py sync        # 测量并写入；章清到 0 时记 cleared_commit
python tools/l2_state.py check       # 与快照比对，漂移退出码 1（可挂 CI）
python tools/l2_state.py report      # 看板：残留 Top + 已清零章(含 commit)
```

- patch.json 格式：`[{"block":24,"fence":"cpp","body":"#include ...\n..."}, {"block":27,"fence":"bash","body":"# 命令\ncmake ..."}]`
- `fence:"bash"` 会把该块围栏换成 ```bash（工具命令块转真命令），自动报告 cpp 块数净减。
- 安全保证：保持原行尾(CRLF/LF)、从大到小替换、先拼 payload 再单次写盘、正文含 ``` 起始行即告警。
- 块数净减后必须同步 README 顶部写死的 cpp 块数（跑 `gen_metrics.py --check` 会给精确新值）。
- **//@ 契约（run_expected 强制）**：`//@` 只能放在「会产生输出的一句」之后；`//@` 到行尾的文本
  必须是 stdout 的连续子串（空白折叠比对、按序各匹配一次）；**禁止夹带注记/解释**（放代码上方
  `//` 行或去掉）；`//@` 后为空 = 无效标记。数值是四舍五入/机器相关时先实跑再写期望
  （例：`{:.3e}` 的 1.2345 实际按 round-half-even 得 1.234，不是 1.235）。

**覆盖记账**：每波结束跑 `l2_state.py sync` 落快照；提交前 `l2_state.py check`（回潮即红）。
已清零章由快照记录 cleared_commit，不再靠手记；种子数据在 `tools/l2_state.json`。

**策略分级（A/B/C）**：纯注释块 ≠ 全是赝品。
- A 源码锚点/标准库行为可实证 → 转自包含 C++ 实测（价值最高）
- B 工具命令块 → 转 `bash` 真实命令
- C 参考文本（选型/里程碑/治理/工具映射表/读书清单）→ **保留不转**
