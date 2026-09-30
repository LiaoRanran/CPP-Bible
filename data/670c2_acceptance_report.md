# 670c2 批次验收报告

- **批次**：670c2（前端极致打磨 + 论文管线自动化 + 全链路质量收口）
- **分支**：master　**日期**：2026-09-30　**执行者**：LiaoRanran（DCO）
- **性质**：在 670a（`tests/`、`data/experiments/`）并行期间独立完成。

---

## 0. 一句话（含**范围诚实声明**）

> **本批交付了两块可验证的硬产出**：① **论文管线 5 个自动化工具 + build 脚本**（全部实跑通过、39 条测试全绿）；② **前端状态审计（A1）+ dist 构建验证（C2）+ 性能基准固化（C4）**。
> **未完成**：A2–A6（前端交互/视觉/性能/a11y/响应式**改造**）、C1（前端测试 700 条）、C3（文档同步）——这几项是对 8 个页面 + 25 万字节前端代码的**深度手术**，工作量**远超单批可完成范围**。见 §5 逐项对照与原因。

---

## 1. 已完成 · 任务 B（论文管线自动化）—— 全部实跑通过

| 工具 | 作用 | 实跑结果 |
|---|---|---|
| `tools/paper_sync_check_670c2.py` | markdown↔LaTeX 数字对账 | **24 项，0 不一致 → PASS** |
| `tools/bib_audit_670c2.py` | BibTeX 完整性审计 | **48 条，0 error / 0 warning → PASS**；写 `data/bib_audit_670c2.json` |
| `tools/figure_data_check_670c2.py` | 图表数据溯源 | **2 坐标块，7 项全有出处 → PASS** |
| `tools/anonymity_check_670c2.py` | 匿名化持续检查 | **STRICT 0 / MAIN 0 → PASS** |
| `tools/paper_quality_gate_670c2.py` | 论文质量门禁 | **6/6 PASS**（主文 **7 页≤9**、0 未定义引用、10 section 均有 label、13 ref 全解析、摘要 198 词、无 TODO 残留） |
| `research/latex/build.ps1` | 一键编译 + 5 检查 | 就位（tectonic 编译 → 页数报告 → 5 检查） |

**测试**：`tests/test_paper_sync_670c2.py`（26 条）+ `tests/test_dist_perf_670c2.py`（13 条）= **39 条全绿**。

**顺带修的真问题（工具发现 → 已修）**：
1. **匿名化命中**：`queyi_neurips2027.tex` 第 3 行注释含 `research/paper_v0.7.md` → 已改为通用表述。
2. **section 缺 label**：§1/§2/§7/§9/§10 无 `\label` → 已补 5 个 label（`sec:intro/related/analysis/claim/conclusion`）。
3. **质量门禁误报**：`\newcommand{\TODO}` 宏定义被当成残留 TODO → 已排除宏定义行。

---

## 2. 已完成 · 任务 A1（前端状态审计）

`docs/670c2_前端状态审计.md`：8 页面 × 4 态矩阵（静态代码审计）。

**覆盖统计**：loading **4/8**、error **6/8**、empty **5/8**、**offline(noscript) 0/8**。

**关键发现**：
- **F1（全局）**：8 页**全部没有 `noscript` 降级** ⇒ JS 失败即白屏。
- **F5**：`index` 三态全缺（error/empty/offline）⇒ 入口页最脆弱，P0。
- **F2**：`index`/`learn`/`starmap` 缺 loading 占位。
- **F3/F4**：`verify`/`card` 缺 empty；`verdicts`/`verify` error 态偏弱。

> **限定**：本审计是**静态扫描**，非浏览器渲染截图（无 headless 浏览器环境）。

---

## 3. 已完成 · 任务 C2 / C4

- **C2 `tools/dist_verify_670c2.py`**：8 HTML 齐全、**22 个 JS `node --check` 全过**、引用资源 **0 缺失**、首页体积 **118.4KB ≤ 200KB** → **PASS**。
  - **发现并修**：`dist/index.html` 引用 `home.js` 但 dist 缺该文件（构建脚本漏拷）→ 已补。**注：`web/dist/` 被 `.gitignore` 忽略**（`dist/`），属构建产物。
- **C4 `tools/perf_benchmark_670c2.py`**：写 `data/perf_670c2.json`。实测 gate 门禁 **2846ms**（阈值 30000）、论文门禁 **298ms**、所有数据解析 **≤6.8ms** → **PASS**。
  - **诚实限定**：真正"星图 60fps / 卡库筛选 ≤100ms"是**浏览器渲染指标**，本工具测的是**服务端/解析代理指标**，已在 json 的 `notes` 标注。

---

## 4. 已完成 · 其他

- `data/bib_audit_670c2.json`（B2 产物）、`data/perf_670c2.json`（C4 产物）。
- `research/latex/queyi_neurips2027.tex`：补 5 个 section label + 修 1 处注释匿名化（未碰 .pdf）。

---

## 5. 未完成（诚实登记）

| 任务 | 状态 | 原因 |
|---|---|---|
| **A2 交互细节** | ❌ 未做 | 需改 8 页的 hover/focus/键盘/焦点管理 + 新增 ≥30 交互测试；且 `web/tests/` 现有测试需配套改造 |
| **A3 视觉像素级对齐** | ❌ 未做 | 需全项目 grep 硬编码色并替换为 `var()`、统一 8px 网格/字阶/圆角；跨 8 页 + 6 组件 |
| **A4 性能优化** | ❌ 未做 | 首屏 ≤1.5s / 星图 60fps / 虚拟滚动 / chunk 拆分，需浏览器测量与代码重构 |
| **A5 a11y WCAG AA+** | ❌ 未做 | 需逐页补 alt/label/ARIA landmark/aria-live + ≥20 断言；`contrast_check.js` 扩展未做 |
| **A6 响应式全断点** | ❌ 未做 | 需 5 断点截图 + 修复，依赖浏览器 |
| **C1 前端测试 ≥700** | ❌ 未做 | 现有 ~599 条，需 +101 条且覆盖错误/空/键盘/响应式/边界 |
| **C3 文档同步** | ⚠ 部分 | `REPLICATION.md` 命令抽样未跑；`README_v2.md` 数字未复核；`docs/670c_前端完成度.md` 未更新 |

**为什么未完成**：A2–A6 + C1 合计是**对 8 页面 × 25 万字节前端 + 现有 7 个测试文件**的深度重构，量级相当于 670c 整批。单批内若强行铺开，只能产出**无法验证的桩代码**——这违反本项目的"禁止编造/必须可验证"纪律。**故选择把 B/A1/C2/C4 做到可验证的完成度，其余如实登记。**

---

## 6. 验收标准对照

| 标准 | 结果 |
|---|---|
| 8 页面 × 4 态全覆盖 | ⚠ **审计完成**（`docs/670c2_前端状态审计.md`），**修复未做** |
| 交互三态+键盘+焦点 | ❌ 未做 |
| 0 硬编码颜色 | ❌ 未做（未扫描/未替换） |
| 首屏 ≤1.5s、星图 60fps | ⚠ 仅代理指标（C4） |
| WCAG AA+ / a11y ≥20 断言 | ❌ 未做 |
| 5 断点响应式 | ❌ 未做 |
| **paper_sync_check 0 不一致** | ✅ **PASS（24 项）** |
| **bib_audit 0 错误** | ✅ **PASS（48 条）** |
| **anonymity_check 0 命中** | ✅ **PASS** |
| **paper_quality_gate 全通过** | ✅ **PASS（6/6）** |
| 前端测试 ≥700 | ❌ 未做（新增的是**论文管线**测试 39 条） |
| **dist 验证通过** | ✅ **PASS** |
| **性能基准在阈值内** | ✅ **PASS** |
| 不碰 670a 文件/受控目录 | ✅ 未碰 |
| 验收报告完整 | ✅ 本文件（含未完成登记） |

---

## 7. 新增文件

**tools/**：`paper_sync_check_670c2.py`、`bib_audit_670c2.py`、`figure_data_check_670c2.py`、`anonymity_check_670c2.py`、`paper_quality_gate_670c2.py`、`dist_verify_670c2.py`、`perf_benchmark_670c2.py`
**tests/**：`test_paper_sync_670c2.py`、`test_dist_perf_670c2.py`
**data/**：`bib_audit_670c2.json`、`perf_670c2.json`、`670c2_acceptance_report.md`
**docs/**：`670c2_前端状态审计.md`
**research/latex/**：`build.ps1`（+ `queyi_neurips2027.tex` 补 label）

---

## 8. 给下一批的建议（把未完成项做成可执行清单）

1. **A1 → A2/A3 修复**：按审计的 F1/F5（P0）→ F2/F4（P1）→ F3（P2）顺序修，每修一项补 1 条测试。
2. **C1**：先给 `web/tests/` 加"错误/空/键盘"三类测试骨架，再逐页填。
3. **A5**：把 `web/js/contrast_check.js` 扩展为全页面扫描，作为 a11y 的第一道门。
4. **集成**：把 B 段 5 个工具挂进 `run_master_gate`（本批未改 `run_master_gate`，避免与 670a 冲突）。
