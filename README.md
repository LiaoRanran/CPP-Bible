# 现代 C++ 终极圣经 (The Ultimate Modern C++ Bible)

> **147 章 · 16 part · 约 14.7 万行 · 6840 个可编译 cpp 代码块**
> 密度审计 v3 均分 **24.2/30**，浅章（<15 分）**0** 个

一本面向**系统 / 嵌入式 / 高性能**方向的现代 C++ 硬核教程，覆盖 C++11 至 C++26。
全部示例以**可编译、可运行、不注水**为铁律——每个 cpp 块都是真实代码，关键断言经
`static_assert` / 运行期验证，而非"示意性伪代码"。

---

## 它适合谁

- 想从 C / 旧式 C++ 过渡到现代 C++ 的工程师
- 嵌入式 / 系统 / 游戏 / 高频等性能敏感方向的开发者
- 准备面试、想建立完整现代 C++ 知识树的读者

## 目录结构（16 part / 147 章）

| Part | 主题 | 章数 |
|------|------|------|
| part01_history | 语言演进与哲学 | 10 |
| part02_toolchain | 编译器 / 构建 / 模块 | 8 |
| part03_language | 语言核心（引用/指针/类型/UB） | 14 |
| part04_memory | 对象模型 / 布局 / 栈堆 / 缓存 | 10 |
| part05_oo | 类 / 继承 / 多态 | 8 |
| part06_templates | 模板 / 特化 / 概念 / 元编程 | 13 |
| part07_stl | 容器 / 智能指针 / 字符串 | 19 |
| part08_algorithms | 算法 / 迭代器 / 范围 | 7 |
| part09_concurrency | 线程 / 原子 / 内存模型 | 7 |
| part10_modern | C++20 / 23 / 26 新特性 | 9 |
| part11_source | 编译 / 链接 / ABI | 11 |
| part12_patterns | 设计模式 / idioms | 9 |
| part13_engineering | 测试 / CI / 代码评审 | 8 |
| part14_perf | 性能剖析 / 优化 | 7 |
| part15_cases | 实战案例 | 6 |
| part16_reading | 延伸阅读 | 1 |

## 质量门禁

本项目用一套"本地 + CI 双跑"的自动化校验，保证**不注水、不破链、可编译**：

| 门禁 | 命令 | 当前结果 |
|------|------|----------|
| 一致性检查 | `python tools/consistency_check.py` | ERROR=0 / WARN=0 |
| 全量编译 | `python tools/compile_all.py --main-only` | 147 章，112 章自包含通过 |
| 编译门禁 | `python tools/compile_gate.py` | 0 真实语法/类型回归（66 设计性豁免块） |
| 密度审计 v3 | `python tools/density_audit.py --json` | 均分 24.2/30，浅章 0 |
| 交叉引用 | `python tools/crossref_audit.py` | 0 断链 |

> **豁免说明**：`tools/compile_exempt.json` 中的 66 个失败块均为**设计性不可单编**内容
> （多文件示例、C++20 Modules、POSIX / Windows 专用 API、外部库、故意展示的错误 / UB、
> 跨块依赖），**非**内容 bug。真实语法 / 类型错误一旦出现，CI 编译门禁立即变红。

## 本地构建（EPUB / PDF / 站点）

> 构建依赖 `pandoc` + `texlive-xetex`（PDF），建议在本机 WSL 或 CI 中执行；本地 Windows
> 缺依赖时脚本会明确报错并给出安装指引，**不产出半成品**。

```bash
# EPUB3
bash tools/generate_epub.sh

# PDF（单卷全书，或 --by-part 分卷）
bash tools/generate_pdf.sh
bash tools/generate_pdf.sh --by-part
```

## 约定与贡献

- 红线宪法见 [`AGENT.md`](AGENT.md)：准确性＞速度、完整性＞简洁、禁注水、禁增章、禁幻觉、源只读只写 `build/`。
- 写作 / 工程约定见 [`CONVENTIONS.md`](CONVENTIONS.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)。
- 发布与质量快照见 [`RELEASE.md`](RELEASE.md)；进度见 [`tools/ROADMAP.md`](tools/ROADMAP.md)。

## 许可

CC BY-NC-SA 4.0
