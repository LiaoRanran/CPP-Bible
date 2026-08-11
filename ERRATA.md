# ERRATA — 已校正内容与已知问题追踪

> 本文件记录《现代 C++ 终极圣经》仓库中**已发现并修正的实质性内容/工具链错误**，便于读者与协作者对照。
> 例行润色、扩写不在此列；仅登记「曾错误、现已改正」或「已知限制」事项。
> 每条标注发现/修正日期、`Book/` 章节或工具、以及根因。完整改动以 git 历史为准。

---

## 2026-08-11

### E1. ch159 线程池示例缺 `#include <thread>`（编译回归）
- **位置**：`Book/part15_cases/ch159_threadpool.md`（块 54 使用 `std::jthread`）
- **根因**：重写时仅保留 `<atomic>` + `<iostream>`，漏引 `<thread>`，致 GCC/Clang
  `-fsyntax-only` 报 `std::jthread` 未声明；CI compile job 因此红。
- **修正**：补 `#include <thread>`。提交 `d0a6069`。

### E2. 发布管线 `rewrite_links` 资产漏拷 → site/pdf/epub 断链「复报错」
- **位置**：`tools/rewrite_links.py`（`run_site`/`run_pdf`）
- **根因**：`d0a6069` 仅给 `run_site`（site 模式）补 `Book/assets/` 复制，`run_pdf`
  （pdf/epub 模式）未动；同一根因只修一个模式，致 run #276 的 pdf/epub 仍红。
- **修正**：
  1. `1740691` 给 `run_pdf` 补 assets 复制 + pdf/epub 脚本 `cd` 进 md 目录修图片解析 +
     mermaid 渲染崩溃降级 + 补 Chromium 库（run #277 全绿）。
  2. `4abf3dc` 令 `rewrite_links` 生成后**自检** site/pdf 产物断链与 nav 覆盖（断裂即退出 1），
     CI 新增 `publish-check` 门禁在重型构建前 ~15s 左移捕获。**红线：同根因须一次覆盖
     site+pdf+epub 全模式，本地跑通再推送。**

### E3. 汇编证据 DRIFT（ch143 `_Z6printfPKcz` ≠ `__mingw_printf`）
- **位置**：`Examples/ch143*.asm` 符号与书内 asm 围栏不一致
- **根因**：MinGW 与证据基线符号命名差异未对齐，触发 `verify_asm_evidence.py` DRIFT。
- **修正**：对齐符号（提交 `b42835e` 等），CI quality 门禁恢复绿。

### E4. 习题「题库串章」——通用模板题库被克隆进无关章
- **范围**：全库 147 章习题主题匹配度审计，发现 7 MISMATCH + 4 WEAK 共 11 章使用通用
  C++20 模板题（`cmp_less`/`std::integral`/`constexpr fact`/泛型 `max`）仅套薄主题包装。
- **修正**：
  - 7 MISMATCH 章重写提交（ch01/ch02 `14e3948`；ch08/09/76/101/129 由 agent 提交）。
  - 4 WEAK 章（`3d0ed65`）重写为紧扣本章主题：ch10 特性测试宏/迁移、ch130
    Chromium/Abseil 基础设施、ch133 ClickHouse/Redis 实现、ch134 Unreal 架构。
  - **残留清理（`f182c99`）**：ch50 误植的重复通用题库块（孤立 `max_safe` 答案 + 重复
    `std::integral add`/`constexpr fact` 练习）已删除；ch157 练习 1 由离题 `max_safe`
    改写为 Compiler Explorer 内联/常量折叠 asm 阅读题。
  - **防回归门禁**：`tools/exercise_dup_guard.py`（确定性，跨章克隆即 BLOCK）接入 CI
    quality job；与 `verify_exercises.py`（仅编译）互补。

### E5. 工具链钉 GCC 15.3.0（`e2fd55b`）
- **背景**：书内汇编证据（`Examples/*.asm`）由本地 MinGW GCC **15.3.0** 生成；CI compile
  矩阵装 `gcc-15`（ubuntu PPA，补丁版本随源浮动）。
- **修正**：
  - `Dockerfile`（`FROM gcc:15.3.0`）+ `.devcontainer/devcontainer.json` 固定镜像，供本地
    编译门禁复现与开发；注明 Linux GCC 不替代 Windows MinGW 的 asm 重生成。
  - CI compile(GCC-15) 新增 **Assert GCC toolchain version**：主版本非 15（14/16 漂移）硬失败；
    补丁版本 ≠ 15.3.0 仅 `::warning`（编译门禁仍有效，但 `Examples/*.asm` 重生成须回本地
    mingw1530 15.3.0）。

---

## 已知限制（非错误，刻意保留）

- **asm 证据工件** `Examples/*.asm` 仅在本地用 MinGW GCC 15.3.0 重生成；CI 不重编译 asm，
  仅做符号级一致性校验（`verify_asm_evidence.py` / `book_asm_freshness.py`）。
- **Clang-19 矩阵**为交叉验证性质，`continue-on-error`：即便 LLVM 源临时不可用也不阻断发布。
- **mermaid 图**在 CI 无沙箱环境下若 Chromium 启动失败，`generate_pdf.sh` / `generate_epub.sh`
  降级为纯代码块，保证 PDF/EPUB 始终产出（矢量图可能缺失，非内容错误）。
- **D5 覆盖扫描**（`d5_gap_scanner.py`）为咨询模式，不阻断 CI。

---

## 校正索引（按提交）

| 提交 | 主题 | 类别 |
|------|------|------|
| `b42835e` | ch143 asm DRIFT 对齐 | E3 |
| `d0a6069` | ch159 补 `<thread>`；rewrite_links site 资产复制 | E1, E2 |
| `1740691` | clang 改 apt.llvm.org；pdf/epub 图片解析 + mermaid 降级 | E2 |
| `4abf3dc` | rewrite_links 自检 + publish-check 门禁 | E2 |
| `3d0ed65` | 4 WEAK 章习题重写 | E4 |
| `f182c99` | exercise_dup_guard 门禁 + ch50/ch157 串章清理 | E4 |
| `e2fd55b` | 钉 GCC 15.3.0（Dockerfile/devcontainer + CI 版本断言） | E5 |
