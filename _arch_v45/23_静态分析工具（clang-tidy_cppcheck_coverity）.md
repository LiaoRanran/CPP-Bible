# 方向 23：静态分析工具（clang-tidy / cppcheck / coverity）

## 核心结论
1. 静态分析是 QueYi 的"近亲赛道"：clang-tidy / cppcheck / Coverity 都在不运行代码的情况下找缺陷——但都**不验证"知识正确性"，只找已知坏模式**，这正是 QueYi 的差异点（语义级验证 vs 模式级检查）。
2. 三者定位不同：clang-tidy（Clang 生态、modernize/bugprone 检查、可定制）、cppcheck（独立、跨平台、轻量）、Coverity（商业、深分析、企业级）。QueYi 应说明"它补的是静态分析抓不到的 UB/语义错"。
3. 对审稿人：展示 QueYi 本身的 C++ 代码过 clang-tidy 零警告，是"验证器自己干净"的基本门槛；同时用静态分析作 baseline 对比（QueYi 能抓 clang-tidy 漏的语义错）。

## 精确数字与案例
- **clang-tidy**：基于 Clang AST，数百条检查（`bugprone-*`, `modernize-*`, `cppcoreguidelines-*`）；可写自定义 check（QueYi 可做成"知识验证 check"？但那是另类产品）；`run-clang-tidy` 批量。
- **cppcheck**：独立解析器，跨平台，误报低；检查风格/未初始化/泄漏；支持 `--enable=all`；GUI 可选。
- **Coverity**：商业（Synopsys），深路径分析，GitHub 学生/开源可免费（Coverity Scan）；企业级 low false-positive。
- **对比**：clang-tidy 与编译器紧耦合（需 compile_commands.json）；cppcheck 无需编译命令但分析浅；Coverity 最深但闭源。
- **案例**：很多 C++ 项目 CI 跑 clang-tidy + cppcheck 双保险；Coverity Scan 曾发现大量开源项目高危漏洞。

## 对阙疑的 3 条具体行动
1. **内核过 clang-tidy**：QueYi 813 行 C++ 加 `clang-tidy -checks=bugprone*,cppcoreguidelines*` 到 CI，零警告作为质量门禁。
2. **做 baseline 对比表**：用 clang-tidy/cppcheck 跑你的 48 卡/15 夹具，统计"静态分析能抓 vs QueYi 能抓"的差集，证明 QueYi 补其盲区（如 UB 语义）。
3. **区分层次**：在 related work 澄清"静态分析 = 模式级；QueYi = 知识/语义级验证"，不把 clang-tidy 当竞争对手而是 baseline。

## 盲区（诚实标注）
- clang-tidy 检查项数量随版本增长，写稿时以 2027 版本为准。
- Coverity Scan 对纯单人开源的免费额度/接入方式需确认（可能需申请）。
- "QueYi 补静态分析盲区"需真实差集数据支撑，不能用宣称代替实验（行动 2）。

## 来源
- [1] clang-tidy — https://clang.llvm.org/extra/clang-tidy/
- [2] cppcheck — https://cppcheck.sourceforge.io/
- [3] Coverity Scan — https://scan.coverity.com/
- [4] Clang 静态分析 — https://clang.llvm.org/docs/ClangStaticAnalyzer.html
