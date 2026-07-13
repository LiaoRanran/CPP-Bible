# TASKS — 任务看板

> 最后更新: 2026-07-11 | 关联: ⟶ PROGRESS.md ⟶ ISSUES.md ⟶ REVIEW.md ⟶ CROSSREF.md
> **Hy3 接手者**：先读 `HANDOVER.md`，AGENT.md 已重写为真实状态。
> **铺路完工**：hy3_check.py（一键秒级）+ .bak 全清(311→0) + 临时探针全清 + 工具链13/13解析完好
> **竣工路线**：见 `ROADMAP_v2.md`（6 步达标 → 1.0 正式版，然后6个打磨方向）

## P0: 阻塞项

| # | 任务 | 文件 | 状态 |
|---|---|---|---|
| 1 | ch121 密度评估（原"补到30cpp/当前21"——**已过时**） | Book/part10_modern/ch121_contracts.md | ✅ 评估达标，不补 |

> **ch121 密度评估结论（2026-07-11）**：实测 46 个 cpp 块（门禁记 45 示例，远超 ≥20 阈值），883 行；门禁 元素20/20、立场Y、断链0 → 100/100。结构覆盖全 10 维度（标准/原理-WG21/编译器-GCC13/STL/性能-x86-64/工业-安全关键/设计权衡/面试-FAQ-实战），约 24 个二级标题。去水词审计：DUP%=0.0%、WTR%=0.45%、147 章中排第 23（高质量端）。cpp 块均 15 行、33/46≥10 行，无灌水碎块。TASKS 原"当前21"系 2026-07-09 增强前快照，期间已补至 45+。依 AGENT.md 红线（密度到顶不稀释、禁止注水、禁止空洞cpp），**判定无需再补，原"补30cpp"任务作废**。
| 2 | ch122 修复 6 个编译 fail | Book/part10_modern/ch122_pmr.md | ✅ 复验 0 fail |
| 3 | ch120 编译 0 fail 验证 | Book/part10_modern/ch120_coroutine_app.md | ✅ 0 fail |
| 4 | ch157 编译 0 fail 验证 | Book/part14_perf/ch157_compiler_explorer.md | ✅ 0 fail |
| 5 | ch158 编译 0 fail 验证 | Book/part14_perf/ch158_perf_antipatterns.md | ✅ 0 fail |
| 6 | ch155 SIMD 复验收官（harness bug 修复 + 块[9]自含修复） | Book/part14_perf/ch155_simd.md + tools/chapter_compile_check.py | ✅ 49 块 0 fail |

> 编译修复战役收官（2026-07-11）：历史失败 180 块 → 修复 104、剩余 76（frag=39/env=17/other=20，全部为跨围栏节选、GCC13.1 缺 C++23 特性、或故意反面教学，无遗漏真实 bug）。**补充（2026-07-11 续）**：ch155 的 3 处 SIMD 失败经复验定位为 `chapter_compile_check.py` 的 **harness 缺陷**（标准库头 `<experimental/simd>` 被裹入 `namespace chk_…` 导致名字空间错位）+ 1 处 **内容自含缺漏**（块[9] `simd_math` 依赖块[8] 的 `namespace stdx` 别名却不自含），二者均已修复，**不计入上述 76 残余内容缺陷**；ch155 现 **49 块 0 fail**（原 24→3→0）。详见 PROGRESS.md「编译修复战役」与「Phase 5」。

## P1: 结构性

| # | 任务 | 范围 | 状态 |
|---|---|---|---|
| 6 | ch43 交叉引用补齐 | Book/part04_memory/ch43_cache_locality.md | ✅ 系统回填已覆盖（全书≥3引用） |
| 7 | part01-06 交叉引用回填 | 53 章 | ✅ 统一回填（全147章≥3引用） |
| 8 | part08-09、11-16 交叉引用回填 | 48 章 | ✅ 统一回填（全147章≥3引用） |
| 9 | 全书门禁 → ERROR=0 WARN=0 | 全部 | ✅ 100/100（ERROR=0/WARN=0，持续维持） |

## P2: 完善

| # | 任务 | 范围 | 状态 |
|---|---|---|---|
| 10 | ch118 Modules 工业级扩写 | Book/part10_modern/ch118_modules.md | ✅ 清理灌水218行 + 核实并入「附录E：标准演进与工业采纳」(WG21 P1103R3/P2465R3/P2996 + 三编译器矩阵 + 工业采纳) |
| 11 | ch81 string 工业级扩写 | Book/part07_stl/ch81_string.md | ✅ 清理灌水(原"→900行"堆字目标依 AGENT.md 红线#1 撤销，密度到顶不稀释) |
| 12 | **工业级扩写=清理灌水**（系统） | 144 章 | ✅ 删除 13,369 行 / 527 个垃圾节(附录Z/Z+/ZZ/ZZZ/FINAL/维度增强)，0 残留、0 重复H2 |
| 13 | Mermaid 图 10 章注入 | 10 个关键章 | ✅ 10章各1块(幂等不重复注)；门禁100/100 |
| 18 | CROSSREF.md 全局依赖索引（导航件 + 生成器） | 根级 CROSSREF.md + tools/gen_crossref.py | ✅ 147章/732边/40策展/0断链/门禁不受影响 |

## P3: 长期

| # | 任务 | 范围 | 状态 |
|---|---|---|---|
| 14 | 全书 PDF 生成 | tools/generate_pdf.sh + rewrite_links.py --mode pdf | 🟡 脚本就位(本地无pandoc,靠CI出) |
| 15 | 全书静态站点 | tools/rewrite_links.py --mode site + gen_mkdocs_nav.py | ✅ 150页 strict零告警 |
| 16 | CI/CD GitHub Actions | .github/workflows/ci.yml (quality/compile/site/pdf) | ✅ 四job就位 |
| 17 | 编译期断言单测 | tools/run_cpp_assertions.py(8核并行) | ✅ FAIL=0(三轮:修2真bug+隔离/反例判定) |
| 18 | 残留污染节清理（维度补齐/维度批量补齐） | tools/clean_dimension_junk.py | ✅ 19文件/974行已删 |

> **#18 改造待办（✅ 2026-07-11 完成）**：
> - **根因**：用户贴出 `ch14_debugging.md` 的"乱码"截图，定位为 `## 维度补齐` / `## 维度批量补齐` 小节。与 Phase 3 已清 `维度增强` **同构的批量污染节**，但 Phase 3 清理签名只匹配"维度增强"，漏掉"维度补齐/维度批量补齐"，致 19 章残留。
> - **性质**：占位提案号 `PxxxxRxx`/`Nxxxx`、无来源数字断言 `~5ns`/`~50cycles`、以及无空格拼接的关键词沙拉（`StackHeapCache...`）。生成式灌水，触犯红线#1/#3。
> - **清理**：`tools/clean_dimension_junk.py`（section-aware，从污染头删到下一个真实 `## ` 节，含双污染头/沙拉/stray 行；保留 `## 相关章节`/`## 自测练习`）。`--apply` 删 **19 文件 / 974 行**，逐章 `.dimension_junk.bak` 备份，幂等。
> - **验证**：`consistency_check.py` 仍 **100/100**（ERROR=0/WARN=0）；全 Book 残留污染签名 = **0**；ch14 优质节（`相关章节`+`自测练习`）完好。
>
> **#17 编译期断言单测（工具就绪，重跑中）**：
> - 新建 `tools/run_cpp_assertions.py`：两类——A 编译期 `static_assert`（包裹编译，失败=书声明错误）；B 运行期 `assert` 完整程序（独立编译+实跑，超时15s）。复用 `chapter_compile_check` 的 PRELUDE/sanitize/GPP。
> - 初版顺序扫描 498 断言块（406 编译期+92 运行期）过慢（~20块/分）。改为 **ProcessPoolExecutor 并行（8 worker）+ 编译超时30s**，重跑预计 ~3–4 分钟。结果写入 `build/assert_report.txt`。

> 发布管线备注（2026-07-11）：
> - #15 站点：`rewrite_links.py --mode site` 重写 3249 处跨章引用（含修复 1461 处无 `Book/` 前缀的旧 markdown 链接），`gen_mkdocs_nav.py` 生成 16-part nav；`mkdocs build --strict` 150 HTML 页、零告警、中文搜索 + 127 Mermaid 图全渲染。产出 `build/site_out/`（52MB）。
> - #14 PDF：`rewrite_links.py --mode pdf` 合并 147 章 14.2 万行、1481 处引用转书内锚点、147 章 H1 注入 `{#chNN}`；本地缺 pandoc/xelatex，实际产出由 CI `pdf` job 完成（`--by-part` 分卷）。
> - 均只写 `build/` 临时区，源树只读；一致性门禁 100/100 不受影响。
