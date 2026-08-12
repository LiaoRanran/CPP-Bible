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

## 2026-08-12

### E6. 结构缺陷扫荡——标题层级（S1）+ 参差表格（S5）+ 反引号感知扫描器
- **范围**：全库 147 章 / 16 part，4 组 agent 分桶并行（part01-05 / 06-10 / 11-15 / 12-16 兜底校验），只读分析 + 安全结构修复，不碰 git、不动语义、保原生换行。
- **类别与修复量**：
  - **S1A 游离 H1 ×1**：`Book/part03_language/ch22_auto_decltype.md:517` 第二个一级标题 `# 核心知识点（23 项模板…）` → `##`。
  - **S1B 层级跳跃 ×6**：`Book/part03_language/ch26_lambda.md:263/699/971`（`#### ③.5…` → `###`，缺 H3 父级）；`Book/part05_oo/ch47_virtual_functions.md:422`、`ch48_rtti.md:468`、`ch49_virtual_inheritance.md:419`（`#### 源码剖析 1` → `###`，H2 后直跳 H4）。
  - **S5 参差表格 ×1（真缺陷）**：`Book/part07_stl/ch91_filesystem.md:408` 提案表行 `| P0218 | Adoptestd::filesystem` into C++17 | … |` 反引号不平衡（缺开引号+空格），塌成 2 单元格 → 补开引号+空格恢复 3 列。
- **扫描器**：新增 `tools/structure_audit.py`（围栏感知，跳过 ``` /~~~ 代码块；表格行按未转义顶层 `|` 切分，忽略行内代码 `` `…` `` 内的 `|` 与转义 `\|`，根治 25 处假阳性）。初版 `split_row` 漏写 `i += 1` 致全库扫描死循环（exit 1073807364），复跑中诊断修复。
- **核验**：升级后全库复扫 `files_with_hits=0`（S1=0 / S5=0）；`git diff` 6 文件 0 CR 翻转，纯结构改动无语义变更；标题 slug 仅依赖文本，改 `#` 数量不断锚（全库断锚=0）。
- **修正**：提交 `bf7a914`（7 files：6 修复 + 扫描器），SSH 推送 `cea8e90..bf7a914`，`master`↔`origin/master` 同步，工作树干净。

### E7. 空白符卫生扫荡——行尾空格/连续空行/末尾换行（MD009/MD012）
- **范围**：全库 147 章 / 16 part，4 组 agent 分桶并行（part01-04 / 05-07 / 08-11 / 12-16），仅用共享工具 `tools/whitespace_fix.py` 确定性修复，不碰 git、不动语义、保原生换行。
- **类别与修复量**（围栏感知，代码块内空白原样保留）：
  - **W1 行尾空格 ×88 行**（围栏外）：剥离行尾空白。
  - **W2 连续空行 ×780 处**：围栏外 2+ 连续空行折叠为 1（147 文件全部中招，本轮"巨大"主体）。
  - **W3 末尾换行 ×38 处**：确保文件以恰好一个换行结尾，去首尾多余空行。
- **工具**：新增 `tools/whitespace_fix.py`（围栏感知状态机 + 原生换行探测 `\r\n`/`\n`，确定性、幂等、`--apply` 落盘）。
- **核验**：全库 147 文件**内容指纹等式校验全过**（去空白后非空行序列与 HEAD 原版逐文件一致）→ 零内容变更、零换行翻转；`structure_audit`/`sweep_fences` 全库复扫 0 命中。
- **修正**：提交 `e6fe145`（147 文件 + 工具，+62728/-63431，净减约 818 行来自空行折叠），SSH 推送 `d4f87ed..e6fe145`，`master`↔`origin/master` 同步，工作树干净。

### E8. CI 常驻化 + §1 立场标签具体化硬化

#### E8-A. CI 质量门禁常驻化（防回归）
- **动机**：E6/E7 扫荡将结构/空白缺陷清零，但缺常驻门禁会随后续编辑回潮。
- **改动**：三扫描器加 `--check` 硬门禁——`tools/structure_audit.py`（S1/S5）、`tools/sweep_fences.py`（围栏/诊断输出/HTML 注释）、`tools/whitespace_fix.py`（W1/W2/W3）；接入 `.github/workflows/ci.yml` 的 `quality` job（Prerequisite Topology Check 之后、compile 之前）。`mermaid_audit.py` / `table_style_audit.py` / `verification_audit.py` 以 `continue-on-error: true` 接入作报告（观察一轮后转硬）。下游 site/pdf/epub 经 `needs: quality` 全覆盖。
- **核验**：干净树 exit 0；注入缺陷 exit 1；回退 exit 0；quality 共 22 steps。
- **修正**：提交 `9279beb`（ci.yml + 三扫描器 `--check`），本地领先 `origin/master` 待推送。

#### E8-B. §1 立场标签具体化硬化（71 高风险章收口）
- **范围**：并发/ABI/模板/性能/内存/源码库/工程/工具链 71 章（裸 `[实现]`/`[平台]` 待具体化；高风险集 76 章中 5 章经复查已合规无需改动）。
- **工具**：新增 `tools/label_specificity_harden.py`——确定性、围栏感知（跳过 ``` /~~~ 代码块）、保原生换行（`\r\n`/`\n` 探测）；仅自动补 `[实现·GCC15/libstdc++/...]` 与 `[平台·x86-64/Windows/...]` 确定限定符，`[微架构]`/`[ABI]` 不自动补（同文件常混用多种，须逐条人工判断），不确定即跳过，遵守 §0「禁止平均用力」。
- **内容**：71 章落具体实现/平台限定符；Agent 残留编辑补 `[VERIFIED]`（真实 D5 基准章）/ `[UNVERIFIED]`（绝对性能数字，§10.3）标记及 §12 绝对化改写（必然→条件式）。
- **审计**：`eol_flips=0`；三 CI 硬门禁（structure/fence/whitespace `--check`）全绿；全量不变式校验 0 语义漂移；全量 diff 标签正确性扫描修正 2 处 Agent 残留错误——`ch11` `[实现·GCC13]`→`[实现·GCC15.3.0]`（误用本机 PATH 的 13.1.0，非书证据基线 15.3.0）、`ch153` 分支误预测行破损括号修复并规范 `[微架构·x86-64][UNVERIFIED]`（x86-64 为 ISA 非微架构，初版误植 `[微架构·x86-64]` 且括号不配平）。
- **修正**：提交 `695d749`（71 文件 + 工具，+923/-666），本地领先 `origin/master` 待推送。

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
| `bf7a914` | 结构缺陷扫荡 S1（标题层级）+ S5（参差表格）+ structure_audit.py | E6 |
| `e6fe145` | 空白符卫生扫荡 W1+W2+W3 + whitespace_fix.py | E7 |
| `9279beb` | CI 常驻化：structure/fence/whitespace 硬门禁 + 三审计报告 | E8-A |
| `695d749` | §1 立场标签具体化硬化 + label_specificity_harden.py | E8-B |
