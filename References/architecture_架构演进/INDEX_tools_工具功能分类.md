# tools/ 工具功能分类索引

> 生成时间：2026-09-19 · 共 142 个 .py 工具
> 标注：🔴=CORE_TOOLS（tool_integrity 管，改后必须重钉）· 🟡=日常活跃 · ⚪=历史遗留/低频 · ❓=待确认用途

---

## 一、核心判决层（5 个，🔴）

| 工具 | 功能 | 入口 |
|---|---|---|
| `gate_engine` | 门禁引擎：63 规则/191 命中，三分类 block/warn/advice | `--check` |
| `atom_evidence_replay` | 证据回放：真编译三分类 confirm/refute/infra_error，56/0/0 | `--check` |
| `poison_drill` | 毒样例钻探：124 载荷，行为级覆盖 39/63，诚实 95.2% | 无参数 |
| `toolchain` | 工具链封装：g++/编译参数/环境 | 被调用 |
| `cppbible` | 主入口/CLI 路由 | 被调用 |

---

## 二、变异与攻击发现器（3 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `mutation_fuzz` | 自动变异器：M1-M7 七算子，全量 1593 变体，v7 逃逸 1/1406 | 🟡 活跃 |
| `mutation_shape_audit` | 变异形态审计：全算子卡面形态审计（588 新增） | 🟡 活跃 |
| `adversarial_regression` | 对抗回归库 | ⚪ 低频 |

---

## 三、度量与统计（6 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `stat_bounds` | Clopper-Pearson 精确置信区间，23 测试全绿 | 🟡 活跃 |
| `metrics_collector` | 指标采集：curves/逃逸率/overturned，**当前停在 9-17** | 🟡 需修 |
| `metrics_snapshot` | 指标快照 | ⚪ 低频 |
| `gen_metrics` | 生成指标 | ⚪ 低频 |
| `cost_tracker` | Token 成本追踪/CPVA 基线 | ⚪ 低频 |
| `data_sanity_audit` | 数据健全性审计 | ⚪ 低频 |

---

## 四、命题与知识层（7 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `prop_graph` | 命题状态图：79 命题/27 卡，pending-signoff/backlog 视图 | 🟡 活跃 |
| `prop_asof` | 四轴只读快照：asserted_at/oracle/推翻/anchor_source（583 新增） | 🟡 活跃 |
| `oracle_rotation` | 换代影响面：与 oracle_report 双实现对账（583 新增） | 🟡 活跃 |
| `knowledge_graph` | 知识图谱（旧版，7 类边） | ⚪ 待升级 |
| `impact_analysis` | 影响分析：改原子前看谁依赖它 | ⚪ 低频 |
| `learning_path` | 学习路径生成 | ⚪ 低频 |
| `test_dependency_graph` | 测试依赖图：72 测试/114 模块/75 无覆盖（589 新增） | 🟡 活跃 |

---

## 五、信任根与完整性（6 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `tool_integrity` | 工具完整性：5 CORE sha 校验，三入口 enforce() 强制自检 | 🟡 活跃 |
| `golden_lock` | 黄金锁：基线对账，**warn 136→186 待人工 accept** | 🟡 活跃 |
| `verify_asm_evidence` | ASM 证据验证 | ⚪ 低频 |
| `verification_audit` | 验证审计 | ⚪ 低频 |
| `consistency_check` | 一致性检查 | ⚪ 低频 |
| `viso_diff` | V-iso 差异比对 | ⚪ 低频 |

---

## 六、编译与运行（12 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `compile_all` | 全量编译 | 🟡 日常 |
| `compile_classify` | 编译结果分类 | 🟡 日常 |
| `compile_gate` | 编译门禁 | 🟡 日常 |
| `compile_triage` | 编译分诊 | ⚪ 低频 |
| `compile_run_sanitize_pipeline` | 编译+运行+消毒管道 | ⚪ 低频 |
| `chapter_compile_check` | 章节编译检查 | 🟡 日常 |
| `d5_compile_gate` | D5 编译门禁 | ⚪ 域专用 |
| `d5_runtime_gate` | D5 运行时门禁 | ⚪ 域专用 |
| `run_cpp_assertions` | 运行 C++ 断言 | ⚪ 低频 |
| `run_expected` | 运行预期测试 | ❓ 待确认 |
| `verify_compiler_features` | 验证编译器特性 | ⚪ 低频 |
| `env_check` | 环境检查 | 🟡 日常 |

---

## 七、ASM/汇编（6 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `asm_prepush_guard` | ASM 推送守卫 | 🟡 日常 |
| `asm_regen` | ASM 重生成 | 🟡 日常 |
| `asm_repro_spotcheck` | ASM 复现抽查 | ⚪ 低频 |
| `book_asm_freshness` | Book ASM 新鲜度 | ⚪ 低频 |
| `sweep_fences` | 扫 FENCE 标记 | 🟡 日常 |
| `artifact_version_stamp` | 工件版本戳 | ⚪ 低频 |

---

## 八、文档与书籍质量（35 个）

### 8.1 Lint/风格
| 工具 | 功能 |
|---|---|
| `doc_lint` | 文档 lint |
| `doc_frontmatter` | 文档 frontmatter 检查 |
| `chapter_lint` | 章节 lint |
| `markdown_style_guard` | Markdown 风格守卫 |
| `codeblock_style` | 代码块风格 |
| `table_style_audit` | 表格风格审计 |
| `mermaid_audit` | Mermaid 审计 |
| `comment_blocks` | 注释块检查 |
| `normalize_comments` | 规范化注释 |
| `terminology_normalize` | 术语规范化 |
| `whitespace_fix` | 空白修复 |

### 8.2 内容审计
| 工具 | 功能 |
|---|---|
| `prose_density` | 散文密度 |
| `scan_prose_backslash` | 扫描散文反斜杠 |
| `star_h2_audit` | 星号 H2 审计 |
| `caption_truncation_audit` | 标题截断审计 |
| `example_caption_cleanup` | 示例标题清理 |
| `example_exercise_audit` | 示例练习审计 |
| `example_tag_inject` | 示例标签注入 |
| `exercise_dup_guard` | 练习重复守卫 |
| `verify_exercises` | 验证练习 |
| `teaching_audit` | 教学审计 |
| `template_audit` | 模板审计 |
| `structure_audit` | 结构审计 |
| `density_audit` | 密度审计 |
| `expansion_audit` | 扩展审计 |
| `crossref_audit` | 交叉引用审计 |
| `xref_check` | 交叉引用检查 |
| `dangling_ref_linter` | 悬空引用 lint |
| `check_citations` | 引用检查（MIS 出处锚） |

### 8.3 链接/索引
| 工具 | 功能 |
|---|---|
| `fix_book_links` | 修复 Book 链接 |
| `rewrite_links` | 重写链接 |
| `gen_indexes` | 生成索引 |
| `gen_mkdocs_nav` | 生成 MkDocs 导航 |
| `site_audit` | 站点审计 |

---

## 九、D5 域专用（4 个）

| 工具 | 功能 |
|---|---|
| `d5_compile_gate` | D5 编译门禁 |
| `d5_runtime_gate` | D5 运行时门禁 |
| `d5_appendix_audit` | D5 附录审计 |
| `d5_gap_scanner` | D5 缺口扫描 |
| `d5_source_integrity` | D5 源完整性 |

---

## 十、任务调度与状态（5 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `task_queue` | L2 任务队列（534 落地） | 🟡 活跃 |
| `task_state` | 任务状态 | ⚪ 低频 |
| `l2_state` | L2 状态查询 | ❓ 待确认 |
| `handover_check` | 交接检查 | ⚪ 低频 |
| `preflight_check` | 起飞前检查 | 🟡 日常 |
| `prereq_topo_check` | 前置拓扑检查 | ⚪ 低频 |

---

## 十一、CI/卫生/备份（12 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `ci_local_precheck` | CI 本地预检查 | 🟡 日常 |
| `prepush_check` | 推送前检查 | 🟡 日常 |
| `backup` | 备份 | ⚪ 低频 |
| `clean_root_artifacts` | 清理根工件 | ⚪ 低频 |
| `_clean_junk` | 清理垃圾（下划线前缀=内部） | ⚪ 内部 |
| `collect_reports` | 收集报告 | ⚪ 低频 |
| `snapshot` | 快照 | ⚪ 低频 |
| `debt_ledger` | 债务台账 | ⚪ 低频 |
| `exempt_audit` | 豁免审计 | ⚪ 低频 |
| `deduplication_audit` | 去重审计 | ⚪ 低频 |
| `atom_coverage_map` | 原子覆盖图 | ⚪ 低频 |
| `utf8_console` | UTF8 控制台 | ⚪ 工具 |

---

## 十二、可观测性与日志（4 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `observability` | 可观测性 | ⚪ 低频 |
| `trace_logger` | 追踪日志器 | ⚪ 低频 |
| `log_query` | 日志查询 | ⚪ 低频 |
| `gray_zone_scan` | 灰区扫描 | ❓ 待确认 |

---

## 十三、Writer/创作辅助（6 个）

| 工具 | 功能 | 状态 |
|---|---|---|
| `writer_selfcheck` | Writer 自检（7 项确定性检查） | 🟡 活跃 |
| `suggest` | 建议生成 | ⚪ 低频 |
| `expand_assist` | 扩展辅助 | ⚪ 低频 |
| `flashcard_export` | 闪卡导出（Anki CSV） | ⚪ 低频 |
| `review_triage` | 评审分诊 | ❓ 待确认 |
| `patch_blocks` | 补丁块 | ❓ 待确认 |

---

## 十四、其他/待确认（5 个）

| 工具 | 推测功能 |
|---|---|
| `book_atom_sync` | Book 与原子同步 |
| `json_project_gate` | JSON 项目门禁 |
| `s10_verify_mark` | S10 验证标记 |
| `hy3_check` | hy3 检查 |
| `run_expected` | 运行预期 |

---

## 十五、统计汇总

| 类别 | 数量 | 占比 |
|---|---|---|
| 核心判决层 | 5 | 3.5% |
| 变异与攻击发现器 | 3 | 2.1% |
| 度量与统计 | 6 | 4.2% |
| 命题与知识层 | 7 | 4.9% |
| 信任根与完整性 | 6 | 4.2% |
| 编译与运行 | 12 | 8.5% |
| ASM/汇编 | 6 | 4.2% |
| 文档与书籍质量 | 35 | 24.6% |
| D5 域专用 | 5 | 3.5% |
| 任务调度与状态 | 6 | 4.2% |
| CI/卫生/备份 | 12 | 8.5% |
| 可观测性与日志 | 4 | 2.8% |
| Writer/创作辅助 | 6 | 4.2% |
| 其他/待确认 | 5 | 3.5% |
| **合计** | **138** | 100% |

> 注：实际 142 个，4 个在枚举时首行为空（无 docstring），归入"其他/待确认"。

---

## 十六、工具债建议（基于 519 工具债解剖）

### 可以合并/废弃的候选
- `compile_triage` + `compile_classify` → 功能重叠
- `metrics_snapshot` + `gen_metrics` → 功能重叠
- `crossref_audit` + `xref_check` + `dangling_ref_linter` → 三个交叉引用检查
- `density_audit` + `prose_density` → 两个密度审计
- `structure_audit` + `template_audit` → 功能重叠

### 核心工具链（日常必跑）
```
tool_integrity --check → gate_engine --check → poison_drill → atom_evidence_replay --check
```

### 建设批常用
```
mutation_fuzz --cards all --operators M1..M7 --limit 999 --jobs 4
mutation_fuzz --selfcheck-determinism
mutation_fuzz --selfcheck-equivalent
stat_bounds（被报告层调用）
prop_graph stats / query
```
