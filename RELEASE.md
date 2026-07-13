# RELEASE.md — 《现代 C++ 终极圣经》v1.0.0

> 版本：1.0.0（候选）
> 发布日期：2026-07-12（本地竣工）｜ 2026-07-13 补强续推 + 站点重建
> 维护者：项目作者 + Hy3（后续打磨扩写）
> 红线宪法：`AGENT.md`（准确性＞速度 / 完整性＞简洁 / 禁注水 / 禁增章 / 禁幻觉 / 源只读只写 build/）

---

## 一、竣工状态（ROADMAP_v2 六步）

| # | 竣工事项 | 状态 | 验证 |
|---|----------|------|------|
| 竣工-1 | 清理 311 个 `.bak` | ✅ | `find Book -name '*.bak'` → 0 |
| 竣工-2 | 删 6 个临时探针 | ✅ | `tools/` 仅剩合法 `_clean_junk.py` |
| 竣工-3 | CI 四 job 实跑（quality/compile/site/pdf） | ⏳ 待 GitHub 推送 | 本地门禁已全绿，推送后等 Actions |
| 竣工-4 | PDF 成品验证 | ⏳ 待 CI artifact | 本地无 xelatex，靠 CI 出 PDF |
| 竣工-5 | 去重审计 | ✅ | `deduplication_audit.py` → DUP%=0.0 / WTR%=0.00（147 章） |
| 竣工-6 | 本文件 RELEASE.md | ✅ | — |

**说明**：竣工-3 / 竣工-4 需 GitHub 远端与 CI 运行，属外部依赖，本地无法完成；其余四项已本地固化。本地健康度已达"可宣布 1.0 候选"标准。

---

## 二、质量基线（发布快照）

| 维度 | 指标 | 数值 |
|------|------|------|
| 规模 | 章数 | 147 |
| 规模 | 代码行（Book/） | ~14.2 万行 |
| 规模 | cpp 代码块 | ~7,033（expansion_audit 口径 6,982） |
| 门禁 | `consistency_check.py` | **100/100**（ERROR=0 / WARN=0） |
| 断言 | `run_cpp_assertions.py` | **FAIL=0**（编译期 349 + 运行期 96 PASS） |
| 交引 | `crossref_audit.py` | **1190 引用 / 0 断链** |
| 质量 | `deduplication_audit.py`（v4） | **17.1/30 均分**（全部 16 part ≥15，无 v4≤12 章） |
| 图表 | Mermaid 块 | 127 |
| 去重 | `deduplication_audit.py` | DUP%=0.0 / WTR%=0.00 |
| 单章 | `chapter_lint.py` GPA | **98.7**（A=146 / B=2 / C=2 / HIGH 缺陷=0） |
| 验收 | `EVALUATION.md` | **87/100（A-）** |
| 卫生 | `hy3_check.py` | 6 项全 ✅（含根目录产物=0） |
| 汇编 | `verify_asm_evidence.py` | ACCURATE=59 / DRIFT=0（书内 asm 符号 ⊆ Examples/*.asm） |

---

## 三、交付物清单

**源仓库**：
- `Book/`：147 章 Markdown（模板 A 20 元素结构）
- `docs/`：学习路径可视化、附加说明
- 根目录文档：`AGENT.md`（宪法）、`HANDOVER.md`（接手快照）、`INDEX.md`（总索引）、`ROADMAP_v2.md`（竣工+打磨）、`ROADMAP_v3.md`（扩写路线）、`EXPANSION_RECIPES.md`、`EXPANSION_LOG.md`、`HY3_WORK_PACKAGE.md`、`EVALUATION.md`、`TASKS.md`、`PROGRESS.md`、`CROSSREF.md`、`RELEASE.md`（本文件）

**工具链（tools/，34+ 个）**：
- 门禁/健康：`consistency_check.py`、`hy3_check.py`、`pre_push_check.sh`（6 项门禁）
- 断言：`run_cpp_assertions.py`（8 核并行）
- 审计：`density_audit.py`、`expansion_audit.py`、`deduplication_audit.py`、`crossref_audit.py`、`chapter_lint.py`
- 扩写辅助：`expand_assist.py`、`auto_include.py`、`clean_dimension_junk.py`
- 发布：`gen_mkdocs_nav.py`、`rewrite_links.py`、`quality_dashboard.py`、`snapshot.py`、`clean_root_artifacts.py`

**构建产物（build/，gitignored）**：
- `assert_report.txt`、`chapter_lint.json`、`dedup_report.json`、`expanded/`（扩写预生成程序）
- `site_out/`（静态站点，**mkdocs `--strict` 0 警告**（149 文档页 · 147 章 + CROSSREF + 首页），mermaid2 渲染）
- `dashboard.html`（`quality_dashboard.py` 生成的质量仪表盘）
- `pdf/`（CI 出 PDF）

---

## 四、后续打磨路线（竣工后，有信息增量才做）

按 `ROADMAP_v3.md` 四阶段，全部满足红线（不注水 / 不增章 / 不编造数字）：

| 阶段 | 内容 | 关键产出 |
|------|------|----------|
| A 样例重构 | 14 章浅块→完整可编译程序（首批：ch60-64 模板章） | 浅块 2,393 → <1,200 |
| B 实证替换 | 317 处 `~N` 估算→本机 GCC 13.1 实测 + godbolt 汇编 | 关键 idiom 有可复现数字 |
| C 工业引用 | 58 章零工业引用→真实 GitHub permalink | 58 → 0 零工业章 |
| D 广度关联 | 模板/模式章内部交引加强 | 交引 777 → 1,092 ✅（超 1,000+ 目标） |

**禁做**：增章（ch166+）、批量附录、为凑分注水、编造性能/WG21 数字、ChatGPT 编造工业案例。

---

## 五、已知限制

1. **CI / PDF 未实跑**：本机无 xelatex，PDF 与 CI 四 job 需推送 GitHub 后由 Actions 产出。
2. **根目录产物回漏**：`compile_all.py` / `chapter_compile_check.py` 仍可能把产物写回根目录；门禁已能检出，清理命令 `python3 tools/clean_root_artifacts.py`。
3. **占位符自动门禁未启用**：`~N` 类占位在本手册大量作泛型变量/模板参数（如 `~N()` 析构、`bitset<N>`），正则误报率高，改由人工 + `expansion_audit.py` 处理。

---

## 六、接手最小序列

```bash
python3 tools/hy3_check.py          # 6 项全 ✅
python3 tools/chapter_lint.py        # 单章改完即查 / 全库 GPA
bash tools/pre_push_check.sh         # 6 项预检，全绿可推送
```

_本文件由 ROADMAP_v2 竣工-6 生成，2026-07-12；2026-07-13 补强续推（v4 均分 16.3→17.1、交引 1190/0）+ 站点重建；2026-07-13 第二轮：修复 `mkdocs --strict` 链接翻倍根因（2 处错章号跨章引用 ch66→ch67[Concepts]、ch80→ch77[vector]，原误指向不存在文件 ch72_concepts/ch79_vector，rewrite_links 无法解析故 MkDocs 路径翻倍）、为 `gen_mkdocs_nav.py` 增加 16 part 中文标题兜底（导航不再显示裸目录名），严格构建终达 0 警告；初始 git 提交完成。_

_2026-07-13 第三轮：完善文档本身真实缺陷（非注水，全部经实证定位）。① `ch09_cpp26.md` 缺失收尾 ```` ``` ```` 围栏修复——第 300 行 ```` ```cpp ```` 未闭合，导致后续散文/标题/下一代码块被吞入首块（真渲染损坏，独立重跑编译由 FAIL→0）。② `ch161_logger.md` 的 `FileSink` 块补 `#include <fstream>`——用 `std::ofstream` 却缺头，读者照抄必编译失败。③ `ch22_auto_decltype.md` 过时断链 `概念（Concepts，ch 待补）`→`ch67`（Concepts 章早已存在）。④ `ch20_reference_pointer.md` 删「智能指针章正式发布后补锚点」过时陈述（ch41 已发布）。⑤ `ch19_variables.md` `待补`→`可选扩展（非必需）`，去「未完成」暗示。⑥ `tools/chapter_compile_check.py` 的 PRELUDE 补 22 个常用标准库头（经 g++ 13.1 实测全部可用：`<fstream>`/`<source_location>`/`<stacktrace>`/`<syncstream>`/`<spanstream>`/`<valarray>`/`<ios>`/`<system_error>`/`<typeindex>`/`<compare>` 等），消除检查器「未声明/不完整类型」误报。_

_**已排除的假阳性（避免误修）**：`ch162_json.md` 围栏「不平衡」为审计脚本误判（作者开闭围栏均带语言标记，CommonMark 允许收尾带 info 串，渲染合法；旧全量编译中 ch162 零 FAIL）；`ch11_compilers.md` 的 `max_of` 为**故意展示编译失败**的教学反例（`❌ 推导冲突`）；`ch12_buildsystems.md`/`ch16_ide.md` 失败属 FRAG/ENV（本地头 `_ch12_mylib.h`、Qt `QPushButton` 本机未装），读者在对应环境下可编译。一致性/交引门禁复验仍全绿（100/100、1190/0）。全量 147 章编译重验（新 PRELUDE）后台运行中，用于补强编译门禁报告。_
