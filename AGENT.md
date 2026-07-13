# AGENT.md — C++ Bible 永恒入口

> **接手者优先读 HANDOVER.md**（本文件是项目宪法，HANDOVER.md 是当前快照）

## 核心理念

```
这是 C++ 圣经的最终编辑阶段，不是从零开始。
你的工作 = 在已有147章之上提升质量，不是堆砌密度。
密度已到顶。继续推分 = 注水，零信息增量。
```

## 🚨 四条红线（禁止事项）

1. **禁止注水提升v3分**：关键词堆砌、附录批量追加、表格注水 → 全部禁止
2. **禁止增加章节数**：147 是已立项规模，不再扩展
3. **禁止幻觉**：WG21 提案号、库版本、平台差异必须可查证；不确定 = 不写
4. **禁止批量单行追加**：每条新内容 ≥5 行，必须有信息增量
5. **禁止伪造汇编证据**：书中 `⑩ 汇编/符号证据` 类 asm 块的 mangled 符号必须 ⊆ `Examples/*.asm` 真实产物；改 asm 前先跑 `python3 tools/verify_asm_evidence.py`，DRIFT≠0 禁止提交（2026-07-13 抓出并修复 6 处真实笔误/虚假归因）

## 🎯 四条绿线（核心方向）

1. **代码可编译验证**：`chapter_compile_check.py` 单章 / `compile_all.py` 全量
2. **门禁 100/100**：`consistency_check.py` ERROR=0 WARN=0
3. **断言契约成立**：`run_cpp_assertions.py` FAIL=0
4. **去水词 v4 审计**：`deduplication_audit.py` 惩罚重复段落

## 🛠 核心命令（按优先级）

```bash
python3 tools/consistency_check.py          # 门禁，必跑，期望 100/100
python3 tools/run_cpp_assertions.py          # 断言单测，期望 FAIL=0
python3 tools/deduplication_audit.py         # v4 去水词审计
python3 tools/chapter_compile_check.py Book/partXX/chYYY.md  # 单章编译
python3 tools/compile_all.py                 # 全量编译
python3 tools/crossref_audit.py              # 交引完整性
```

## 📋 工具链清单

| 工具 | 作用 | 状态 |
|---|---|---|
| `consistency_check.py` | 门禁：20 元素/章，0/0=通过 | ✅ |
| `chapter_lint.py` | 单章级质量门禁（行号级缺陷+项目GPA，复用围栏判定） | ✅ 新轮子 |
| `verify_asm_evidence.py` | **汇编证据准确性守卫**（书内asm符号⊆真实`Examples/*.asm`，0捏造） | ✅ 新轮子 |
| `clean_root_artifacts.py` | 根目录编译产物清理（移入 build/_root_artifacts/，可逆） | ✅ 新轮子 |
| `chapter_compile_check.py` | 单章编译校验（namespace 包裹 + PRELUDE） | ✅ |
| `compile_all.py` | 批量编译 | ✅ |
| `run_cpp_assertions.py` | 编译期 static_assert + 运行期 assert 单测（8核并行） | ✅ FAIL=0 |
| `rewrite_links.py` | 跨章引用重写（site/pdf 共用，幂等，只写 build/） | ✅ |
| `gen_mkdocs_nav.py` | 从 INDEX.md 生成 MkDocs nav（16-part 中文标题） | ✅ |
| `clean_dimension_junk.py` | 维度补齐/批量补齐污染节清理（section-aware） | ✅ |
| `gen_crossref.py` | CROSSREF.md 全局依赖导航生成器 | ✅ |
| `xref_backfill.py` | 交叉引用回填 | ✅ |
| `exercise_gen.py` | 练习题注入（内容感知 v2） | ✅ |
| `verify_exercises.py` | 练习题全量编译校验 | ✅ |
| `inject_mermaid.py` | Mermaid 图注入（幂等） | ✅ |
| `density_audit.py` | v3 密度审计（dim 0-3 + depth 加权） | ✅ |
| `density_tracker.py` | 历史快照 + 趋势 | ✅ |
| `deduplication_audit.py` | v4 去水词审计 | ✅ |
| `crossref_audit.py` | 交引完整性，断链=0 | ✅ |
| `suggest.py` | 智能建议引擎 | ✅ |
| `knowledge_connect.py` | 知识连接表生成 | ✅ |
| `learning_path.py` | 学习路径依赖图 | ✅ |
| `build_path_viz.py` | 依赖 DAG 可视化 HTML | ✅ |
| `generate_pdf.sh` | PDF 生成（pandoc + xelatex，靠 CI 出） | 🟡 脚本就位 |
| `fix_includes_all.py` / `fix_missing_includes.py` | 批量修复缺失头文件 | ✅ |
| `compile_classify.py` / `compile_p0.py` / `fast_compile.py` | 编译分类/优先级/快速编译 | ✅ |
| `reverify_failures.py` | 回归重验失败块 | ✅ |

## 📁 文档矩阵

```
AGENT.md             ← 项目宪法（本文件）
HANDOVER.md          ← 当前状态快照（接手者先读）
TASKS.md             ← 任务看板（P0-P3 全部 ✅，仅剩 .bak 清理）
MEMORY.md            ← 项目长期记忆（.workbuddy/memory/）
PROGRESS.md          ← 完成度与里程碑详情
CROSSREF.md          ← 全局依赖导航（732 边/0 断链）
ROADMAP.md           ← 路线图
ENHANCEMENT_MATRIX.md ← 增强矩阵
CHAPTER_TEMPLATE.md  ← 新章模板
```

## ⚙️ 工作纪律

- **接项目后**：必跑 `consistency_check.py` 确认基线
- **每完成 5 项工作**：必跑门禁 + 统计；若退步 → 回滚
- **每条新内容**：必含可编译代码 / 真实数据 / 可查证引用
- **每章末尾**：已有 ≥3 道练习题（`## 自测练习`，`<details>` 折叠答案）

## 🏁 接续模型行动指南

1. **跑 `consistency_check.py`** → 确认 100/100
2. **读 `HANDOVER.md`** → 了解当前状态与剩余待办
3. **读 `MEMORY.md`** → 了解历史决策与踩坑
4. **不要追加水词。** 直接做：
   - 跑 `deduplication_audit.py` → 定位重复段落
   - 跑 `run_cpp_assertions.py` → 确认 FAIL=0
   - 跑 `chapter_lint.py` → 看单章质量门禁（行号级缺陷，改完即查）
   - 确认 CI site/pdf job 一次实跑通过
   - 若根目录再现 `.cpp/.exe/.o` 泄漏 → `python3 tools/clean_root_artifacts.py`

## 📊 交付物状态（2026-07-11 实测）

| 类别 | 已完成 | 状态 |
|---|---|---|
| 章节内容 | 147 章，~141K 行 | ✅ 密度天花板 |
| 代码块 | ~7033 cpp | ✅ 编译失败 76（frag/env/other，无遗漏 bug） |
| 表格 | 1648+ | ✅ |
| 交叉引用 | 1180，0 断链 | ✅ |
| 全局依赖导航 | CROSSREF.md（732 边，0 断链） | ✅ |
| 练习题 | 147 章全注入（441 练习块，0 编译失败） | ✅ |
| 知识连接 | 136/147 章 | ✅ |
| Mermaid 图 | 127 块（10 章注入 + 源生） | ✅ |
| 灌水清理 | Phase 3 维度增强 + #18 维度补齐（全清，0 残留） | ✅ |
| 编译修复 | 180→76（frag=39/env=17/other=20） | ✅ |
| 静态站点 | MkDocs Material（150 页，strict 零告警） | ✅ |
| PDF | 脚本就位（靠 CI 出，本地缺 pandoc/xelatex） | 🟡 |
| CI/CD | `.github/workflows/ci.yml` 四 job（quality/compile/site/pdf） | ✅ |
| 断言单测 | 498 块（FAIL=0，2 DEMO，51 WARN 全隔离伪影） | ✅ |
| 学习路径 | learning_paths.md + 依赖 DAG 可视化 | ✅ |
| 项目地图 | 6/6 | ✅ |
| .bak 清理 | 311 个备份文件 | ✅ 已清理 |

**结论**：密度已满，**下一阶段必须转向质量验证与去水词**。

---

_最后更新：2026-07-11 14:58 by WorkBuddy（AGENT.md 全量重写，同步真实状态）_
_代际：第 4 代 Agent（WorkBuddy → Hy3）_
