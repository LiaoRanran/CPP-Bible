# tools/legacy/ — 归档脚本说明

本目录收纳 **37 个已被确认无活依赖的脚本**（既不被 CI 直接调用，也不被任何活工具 import/子进程调用）。

归档时间：2026-08-14（T3 工具链收敛）。
迁移方式：`git mv tools/<x>.py tools/legacy/<x>.py`，保留全部历史。
运行方式不变：`python3 tools/legacy/<x>.py ...`（仍可直接执行，只是退出主命名空间）。

## 为什么归档
- `tools/` 原有 86 个 `.py`，其中 31 个被 CI 直接引用、18 个被活工具内部调用（活依赖）。
- 剩余 37 个为纯孤儿：多为一次性审计、历史波次残留、或被新工具（cppbible / compile_gate 等）取代的旧实现。
- 归档后 `tools/` 仅保留 49 个活工具，主命名空间清晰，cppbible 为唯一入口。

## 逐个用途（供日后检索）
| 脚本 | 用途 |
|---|---|
| audit_cpp_defects.py | 扫描 Book 内 cpp 代码块的结构性缺陷 |
| audit_cpp_warnings.py | 扫描 cpp 代码块的编译告警 |
| audit_py_tools.py | 审计 tools/ 自身 Python 工具的健康度 |
| auto_include.py | 自动推导并插入缺失的 #include |
| build_path_viz.py | 可视化构建依赖路径（配合 learning_path） |
| chapter_number_audit.py | 校验章节编号连续性 |
| ci_gate.py | 早期 CI 门禁（已被 compile_gate / cppbible 取代） |
| clean_dimension_junk.py | 清理维度升级实验产生的临时垃圾 |
| compile_p0.py | P0 阶段的编译批处理脚本 |
| d5_asm_evidence.py | 生成 D5 性能附录的汇编证据工件 |
| d5_asm_inject.py | 将汇编证据注入 Book 章节（幂等） |
| density_tracker.py | 跟踪章节内容密度变化 |
| disclaimer_audit.py | 审计章节免责声明完整性 |
| exercise_gen.py | 习题自动生成（实验性） |
| extract_exercise_sections.py | 抽取章节内习题段落 |
| fast_compile.py | 单章快速编译辅助 |
| fix_includes_all.py | 批量修复 include（被 compile_all 调用过，现已被取代路径） |
| fix_missing_includes.py | 修复缺失 include |
| gen_compile_exempt.py | 生成编译豁免候选清单 |
| gen_crossref.py | 生成跨章引用索引（产物已落库） |
| generate_wg21_tracker.py | 生成 WG21 提案跟踪表 |
| industrial_precision.py | 工业级精度/数值检查 |
| inject_mermaid.py | 注入 mermaid 图（已被 mermaid_theme_inject 取代） |
| knowledge_connect.py | 知识图谱连接（实验性） |
| label_specificity_harden.py | 强化标签特异性 |
| merge_exercise_theme_reports.py | 合并习题主题报告 |
| mermaid_lint.py | mermaid 语法 lint（已被 mermaid_audit 取代） |
| mermaid_theme_inject.py | 注入 mermaid 主题 |
| module_compile_check.py | C++20 模块编译检查 |
| prune_exempt.py | 修剪失效豁免项 |
| quality_dashboard.py | 质量仪表盘 HTML 生成 |
| reverify_failures.py | 对失败项重新验证 |
| scan_compiler_refs.py | 扫描编译器特性引用 |
| title_style_lint.py | 标题样式 lint |
| verify_prose_only.py | 校验纯 prose 改动不触碰代码块 |
| wave_intake_check.py | 波次任务接收检查 |
| xref_backfill.py | 跨章引用回填 |

> 若某归档脚本经实践证明确实需要复活为活工具，请用 `git mv tools/legacy/<x>.py tools/<x>.py` 移回，并同步在 `ci.yml` 或 `cppbible.py` 中接线。
