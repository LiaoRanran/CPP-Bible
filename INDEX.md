# INDEX.md — 项目总索引

> 最后更新：2026-07-11 | 为 Hy3 交接铺路完成

## 阅读顺序（首次接手）

| 顺序 | 文件 | 用途 | 阅读时间 |
|------|------|------|----------|
| 1 | `AGENT.md` | 项目宪法 — 四条红线 + 四条绿线 + 工作纪律 | 3 min |
| 2 | `HANDOVER.md` | 当前状态快照 — 环境路径 + 工具速查 + 已知问题 | 5 min |
| 3 | `HY3_WORK_PACKAGE.md` | 首批工作包 — 模板5章22组预生成代码，可直接用 | 3 min |
| 4 | `python3 tools/hy3_check.py` | 一键健康检查 — 确认 6 项全绿 | 10 sec |
| 5 | `ROADMAP_v2.md` | 竣工路线 — 6 步达标 v1.0 | 3 min |
| 6 | `ROADMAP_v3.md` | 扩写路线 — 四维 x 四阶段 ~40h | 5 min |

---

## 文档地图

| 文件 | 类型 | 说明 |
|------|------|------|
| `AGENT.md` | 宪法 | 四条红线、四条绿线、核心命令、工具链清单 |
| `HANDOVER.md` | 快照 | 环境路径、工具速查、已知问题、接手第一步 |
| `TASKS.md` | 看板 | P0-P3 全部 ✅，竣工路线引用 |
| `ROADMAP_v2.md` | 路线 | 竣工 6 步 → v1.0 正式版 |
| `ROADMAP_v3.md` | 路线 | 竣工后扩写：四维四阶段 ~40h + 禁做清单 |
| `EVALUATION.md` | 审计 | 七项审计报告，加权 87/100 (A-) |
| `EXPANSION_RECIPES.md` | 指南 | Top5 章逐章扩写处方 |
| `EXPANSION_LOG.md` | 追踪 | 四阶段进度追踪模板（⬜→🟡→✅） |
| `HY3_WORK_PACKAGE.md` | 工作包 | 模板5章22组预生成+编译，6组可直接用 |
| `PROGRESS.md` | 里程碑 | 完成度与各阶段详情 |
| `CROSSREF.md` | 导航 | 全局依赖索引（732 边 / 0 断链） |
| `INDEX.md` | 索引 | 本文件 |

---

## 工具地图

### 健康检查 + 推送

| 工具 | 用途 | 耗时 |
|------|------|------|
| `tools/hy3_check.py` | 一键秒级健康检查（7项，含根目录产物+汇编证据） | <10s |
| `tools/chapter_lint.py` | **单章级质量门禁**（行号级缺陷+项目GPA） | <5s |
| `tools/verify_asm_evidence.py` | **汇编证据准确性守卫**（书内asm符号⊆真实产物，0捏造） | <15s |
| `tools/clean_root_artifacts.py` | 根目录编译产物清理（移入 build/） | <10s |
| `tools/pre_push_check.sh` | 推送前预检（7项） | ~60s |
| `tools/snapshot.py` | 质量快照 save/list/compare | ~30s |
| `tools/quality_dashboard.py` | 生成 HTML 仪表盘 | ~30s |

### 门禁 + 审计

| 工具 | 用途 | 耗时 |
|------|------|------|
| `tools/consistency_check.py` | 门禁 147 章 | <5s |
| `tools/crossref_audit.py` | 交引完整性 | <5s |
| `tools/density_audit.py` | v3 密度审计 | ~60s |
| `tools/deduplication_audit.py` | v4 去水词审计 | ~60s |
| `tools/expansion_audit.py` | 四维扩写审计 + 优先队列 | ~15s |

### 编译 + 断言

| 工具 | 用途 | 耗时 |
|------|------|------|
| `tools/chapter_compile_check.py` | 单章编译校验 | ~30s |
| `tools/compile_all.py` | 全量编译 | ~5min |
| `tools/run_cpp_assertions.py` | 断言单测（8核并行） | ~3min |
| `tools/verify_exercises.py` | 练习题编译校验 | ~1min |

### 扩写工具

| 工具 | 用途 | 耗时 |
|------|------|------|
| `tools/expand_assist.py` | 智能浅块合并+编译 | ~30s/章 |
| `tools/auto_include.py` | 自动补头文件 | ~10s |
| `tools/expansion_audit.py` | 扩写审计 + 优先队列 | ~15s |

### 发布管线

| 工具 | 用途 | 耗时 |
|------|------|------|
| `tools/rewrite_links.py` | 跨章引用重写（site/pdf 共用） | ~10s |
| `tools/gen_mkdocs_nav.py` | MkDocs nav 生成 | <5s |
| `tools/generate_pdf.sh` | PDF 生成（pandoc+xelatex） | CI |
| `.github/workflows/ci.yml` | CI 四 job | 推送触发 |

### 内容维护

| 工具 | 用途 |
|------|------|
| `tools/exercise_gen.py` | 练习题注入（内容感知 v2） |
| `tools/xref_backfill.py` | 交叉引用回填 |
| `tools/inject_mermaid.py` | Mermaid 图注入（幂等） |
| `tools/clean_dimension_junk.py` | 污染节清理（section-aware） |
| `tools/gen_crossref.py` | CROSSREF.md 生成器 |
| `tools/build_path_viz.py` | 学习路径 DAG 可视化 |
| `tools/fix_includes_all.py` | 批量修复缺失头文件 |
| `tools/_clean_junk.py` | Phase 3 灌水清理工具（保留） |

---

## 关键环境路径

```
Python:  C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe
mkdocs:  C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/mkdocs.exe
G++:     C:/Qt/Tools/mingw1530_64/bin/g++.exe  (15.3.0)
项目根:  C:/CodeLearnling/note/note/C++/CPP-Bible/
```

---

## Hy3 最小启动命令序列

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible
PY=C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe

# 1. 健康检查
"$PY" tools/hy3_check.py

# 2. 看全局
"$PY" tools/quality_dashboard.py --open

# 3. 看扩写优先级
"$PY" tools/expansion_audit.py --top 20

# 4. 开工作包
cat HY3_WORK_PACKAGE.md

# 5. 看仪表盘 → 质量柱在动 → snapshot 记录
"$PY" tools/snapshot.py save
```
