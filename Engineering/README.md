# Engineering — 工程实践指南（平行 147 核心章）

> 定位：与 `Book/`（147 核心章）**平行**的文件夹，**不计入 147 章、不参与主书门禁**（`consistency_check.py` 只扫 `Book/`）。
> 内容：把 C++ 用到真实工程里的「设计模式 / 系统 / 框架 / 算法模板 / 调试 / IDE / 嵌入式 / 工程流程」——既有章节内扩展，也有此处独立深坑。
> 引用体系：见 `docs/references/SOURCING.md`（所有事实须带 T0–T6 引用键；标准=事实基线）。

## 子目录 → 平行 147 章 映射

| 子目录 | 主题 | 平行核心章 | 主参考源（键） |
|--------|------|-----------|----------------|
| `design_patterns/` | GoF + 现代 C++ 模式 | part15_design (ch159–164) | `book:tour` `core` `isocpp` |
| `linux_kernel/` | Linux 内核 C 实战 | Part0 C / part10–13 | `std-c11` `cert` `book:krc` |
| `qt/` | Qt 框架详细 | part14 工程 / 实际应用 | `msvc` `gcc` `book:primercpp` |
| `unreal/` | 虚幻引擎 C++ 实战 | part14 工程 | `msvc` `book:tour` |
| `algorithms/` | 算法题模板 / 算法实现 | part09_algorithms (ch95–113) | `cppref` `book:templates` |
| `debugging/` | 调试技巧 / 崩溃复盘 | part02 toolchain / part14 | `gcc` `clang` `ubsan` `asan` |
| `ide/` | IDE 使用建议 | part02 toolchain | `msvc` `gcc` |
| `real_world/` | 开源项目架构赏析 | 跨章 | `so` `cppcon` |
| `embedded/` | 嵌入式 C/C++ | Part0 / 系统 | `std-c11` `cert` |
| `software_engineering/` | 工程流程 / 评审 / 测试 | part14 / part16 | `core` `cert` `isocpp` |

## 写作约定

- 每条指南「规则 + 正例 + 反例 + 说明」格式（对齐 SOURCING §3.5）。
- 标准行为 vs 扩展 vs UB 三态标注。
- 章节内已展开的内容，此处只做「深挖/案例」，避免与核心章重复。
- 本地蓝本：`docs/references/external/Linux内核极致详细手册.md`、`C:\Users\ASUS\Desktop\cppb参考资料\嵌入式\`（29 篇）、Software Engineering at Google(PDF)。
