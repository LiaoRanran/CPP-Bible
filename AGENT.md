# AGENT.md — C++ Bible 永恒入口

> **接手者优先读 HANDOVER.md**（本文件是项目宪法，HANDOVER.md 是当前快照）

## 核心理念

```
这是 C++ 圣经的编辑与持续提升阶段，不是从零开始。
你的工作 = 在已有147章之上做有信息增量的质量提升。
每条新内容必须 ≥5 行且含有可查证引用/真实数据/可编译代码。
禁止堆砌关键词凑分，但真实工业引用 + 底层分析是合法增量。
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
2. **读 `NEXT_LLM.md`** → 一键接手工序（**比 HANDOVER.md 更精简，专为 LLM 设计**）
3. **读 `HANDOVER.md`** → 了解全貌与踩坑历史
4. **不要追加水词。** 合法工作方向：
   - 跑 `deduplication_audit.py --all` → 看 v4 最低章 → 对 IND 薄弱章追加「附录 G」（参考已注入的 15 章模板：工业引用表 + 底层分析段）
   - 跑 `run_cpp_assertions.py` → 确认 FAIL=0
   - 跑 `chapter_lint.py` → 看单章质量门禁（行号级缺陷，改完即查）
   - 若根目录再现 `.cpp/.exe/.o` 泄漏 → `python3 tools/clean_root_artifacts.py`

## 📊 交付物状态（2026-07-13 午 实测）

| 类别 | 已完成 | 状态 |
|---|---|---|
| 章节内容 | 147 章，143,469 行 | ✅ v4 均分 17.8/30 |
| 代码块 | 7,013 cpp | ✅ 编译残余 ~15-18 块，全部 FRAG/ENV/故意反例（见 RELEASE 豁免清单） |
| 表格 | 597 | ✅ 0 真实缺陷 |
| 交叉引用 | 1,190，0 断链 | ✅ |
| 全局依赖导航 | CROSSREF.md（0 断链） | ✅ |
| 练习题 | 147 章全注入（441 练习块，0 编译失败） | ✅ |
| Mermaid 图 | 88 块（Book/，全部有效闭合且语法校验通过） | ✅ |
| v4 底线 | v4=13 池已清零（14→0） | ✅ |
| 静态站点 | MkDocs Material（149 页，strict 零告警） | ✅ |
| PDF | 脚本就位（靠 CI 出，本地缺 pandoc/xelatex） | 🟡 |
| CI/CD | `.github/workflows/ci.yml` 四 job（脚本就位，待 GitHub remote 推送实跑） | 🟡 |
| 断言单测 | `run_cpp_assertions` FAIL=0 | ✅ |
| 汇编证据 | `verify_asm_evidence` DRIFT=0 | ✅ |
| 单章质量 | `chapter_lint` GPA 98.7（A=146/B=2/C=2，0 HIGH） | ✅ |
| .bak 清理 | 311 个备份文件 | ✅ 已清理 |
| Git 仓库 | 5 提交（`1daf928`→`352622a`→`dc7d757`→`90fbbc1`→`9ebfe51`），无 remote | ✅ |
| 结构化交付物 | glossary(129)+knowledge_graph+source_map(103)+learning_paths(4) | ✅ |
| 铺路附录 G | 15 章已注入（ch99/ch154/ch107/ch80/ch142/ch162/ch32/ch60/ch64/ch67/ch50/ch17/ch137/ch145/ch68） | ✅ |

**结论**：硬门禁全部通过，v4 底线已清零。下一阶段合法方向：① 继续附录 G 注入 v4=14 章；② ROADMAP_v3 阶段 A（浅块→完整程序）；③ 推 GitHub remote → CI 实跑 → PDF；④ 本机装 xelatex → 出 PDF。

---

_最后更新：2026-07-13 14:15 by WorkBuddy（第六轮铺路后同步状态，交付物表全量修正）_
_代际：第 4 代 Agent（WorkBuddy → Hy3）_
