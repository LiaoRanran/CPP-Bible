# HANDOVER.md — 项目接手快照（2026-07-13 午）⚠️ 已废弃

> **本文件是 Phase APP 应用层增强启动前（07-13）的快照，数字与当前状态严重不符。**
> **接手者请读 `NEXT_LLM.md`**（2026-07-17 铺路文档，Phase APP 唯一权威入口）。
> 本文件保留作历史参考（Git 仓库已初始化 → 已有 remote + 50+ 次提交；第三阶段 P0 任务 → 已被 Phase APP 替代）。

## 一句话概况

《现代 C++ 终极圣经》147 章知识工程 **v1.0.0 候选 / push-ready**。全部硬门禁实证全绿，文档真实缺陷已于第三四轮穷尽（5 处源修复 + PRELUDE 补强 + 编译豁免透明化）。Git 仓库已初始化（3 提交），无 remote 不 push。剩余仅环境阻塞：GitHub remote（→ CI 四 job 实跑）、xelatex（→ PDF）。

---

## 当前状态总表（2026-07-13 午 实测）

| 维度 | 数据 | 状态 |
|------|------|------|
| 章节 | 147 章 / 16 part | ✅ |
| 正文行数 | 143,469 行（Book/） | ✅ |
| cpp 代码块 | 7,013 个 | ✅ |
| 交引 | 1,190 引用 / 0 断链 / 16 part 覆盖 | ✅ |
| CROSSREF | 边 0 断链 / 幂等可重生成 | ✅ |
| Mermaid | 88 块（Book/，全部有效闭合且语法校验通过） | ✅ |
| 门禁 | `consistency_check` 100/100（ERROR=0 / WARN=0） | ✅ |
| 断言 | `run_cpp_assertions` FAIL=0 | ✅ |
| 汇编证据 | `verify_asm_evidence` ACCURATE=59 / DRIFT=0 | ✅ |
| 严格构建 | `mkdocs --strict` 0 警告（149 文档页） | ✅ |
| 单章质量 | `chapter_lint` GPA 98.7（A=146/B=2/C=2，0 HIGH） | ✅ |
| 去水词 | `deduplication_audit` DUP%=0 / WTR%=0 | ✅ |
| v4 质量 | 均分 17.1/30，全 16 part ≥15 | ✅ |
| 页内锚点 | 0 死链（2026-07-13 新增核查） | ✅ |
| 表格 | 597 表，0 真实缺陷（2026-07-13 新增核查） | ✅ |
| 结构化 JSON | glossary(129)+knowledge_graph+source_map(103)+learning_paths(4) | ✅ |
| 练习题 | 147 章全注入（441 练习块，0 编译失败） | ✅ |
| .bak | 311 个已全删，工作区干净 | ✅ |
| 编译门禁 | 仅 ch161(6 FRAG/伪影)+ch11(故意反例)+ch12/ch13/ch16(FRAG/ENV) | 🟢 已知非 bug，见豁免清单 |
| 静态站点 | `build/site_out/`（mkdocs material，mermaid2 渲染） | ✅ |
| PDF | `generate_pdf.sh` 就位（本地缺 xelatex，CI pdf job 出） | 🟡 |
| CI/CD | `.github/workflows/ci.yml` 四 job | ✅ 脚本就位 |
| Git 仓库 | 3 提交，2,297 文件，无 remote，工作树干净 | ✅ |

---

## Git 提交链

```
dc7d757 (HEAD -> master) docs: 编译门禁豁免清单透明化 + 修正 mermaid 计数
90fbbc1 docs: 第三轮完善文档本身真实缺陷（非注水）
9ebfe51 chore(release): v1.0.0 竣工 — 修复站点严格构建链接翻倍 + 导航中文 part 标题
```

**工作树**：干净（`git status --short` 为空）。无 remote，按项目红线约定不 push。
**保护**：`.gitignore` 已加固（`build/`、`site_out/`、`*.exe/*.o/*.obj/_probe*.cpp`、`.workbuddy/` 全部忽略）。

---

## 环境速查

```bash
# Python（Managed，优先用）
C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/python.exe

# MkDocs Material（站点构建，已装 mkdocs-material 9.7.6 + mkdocs-mermaid2-plugin 1.2.3）
# 但 mkdocs 通过 Python Path 直接调用：
C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/mkdocs.exe

# C++ 编译器（MinGW GCC 13.1.0）
C:/Qt/Tools/mingw1310_64/bin/g++.exe

# 项目根目录
C:/CodeLearnling/note/note/C++/CPP-Bible/
```

---

## 关键工具速查

| 命令 | 用途 | 预期输出 |
|------|------|----------|
| `python3 tools/hy3_check.py` | **一键健康检查（含 asm 证据守卫）** | 全部 ✅ |
| `bash tools/pre_push_check.sh` | **推送前必跑（6 项预检）** | 全部通过 |
| `python3 tools/consistency_check.py` | 门禁 | 100/100，ERROR=0 WARN=0 |
| `python3 tools/run_cpp_assertions.py` | **断言单测（约 2-3min）** | FAIL=0 |
| `python3 tools/crossref_audit.py` | 交引完整性 | 断链=0 |
| `python3 tools/chapter_compile_check.py Book/partXX/chYYY.md` | 单章编译（namespace 包裹 + PRELUDE） | 0 fail（注意豁免清单） |
| `python3 tools/chapter_lint.py` | 单章级质量门禁（行号级缺陷，秒级） | GPA 98.7 |
| `python3 tools/verify_asm_evidence.py` | **汇编证据准确性守卫** | DRIFT=0 |
| `python3 tools/deduplication_audit.py` | v4 去水词审计 | DUP=0 WTR=0 |
| `python3 tools/rewrite_links.py --mode site` | 站点链接重写（**必须先跑再 gen_mkdocs_nav**） | 重写链接 |
| `python3 tools/gen_mkdocs_nav.py` | 生成 MkDocs nav + `index.md`（**必须在 rewrite_links 之后跑**） | 159 行 nav |
| `mkdocs build --strict -f build/site/mkdocs.yml` | 站点严格构建 | 149 页，0 警告 |
| `python3 tools/quality_dashboard.py` | 生成质量仪表盘 HTML | `build/dashboard.html` |
| `python3 tools/clean_root_artifacts.py` | 根目录编译产物清理（移入 `build/_root_artifacts/`，可逆） | 幂等 |

> ⚠️ **发布管线正确顺序**：`rewrite_links.py --mode site` → **必须** `gen_mkdocs_nav.py`（否则 `index.md` 丢失）→ `mkdocs build --strict`。漏掉第二步会用裸目录名导航 + 无首页。

---

## 项目文件结构

```
CPP-Bible/
├── AGENT.md               ← 项目宪法（红线/绿线/工具清单，部分旧数待更新）
├── HANDOVER.md            ← 本文件（接手者先读，优先于 AGENT.md 的数字）
├── RELEASE.md             ← 发布快照 + 质量基线 + 编译豁免清单 + 四轮修复记录
├── INDEX.md               ← 总索引（阅读顺序/文档地图/工具地图）
├── EVALUATION.md          ← 工程验收评估（87/100 A-）
├── CROSSREF.md            ← 全局依赖导航（0 断链）
├── ROADMAP_v2.md          ← 竣工六步路线
├── ROADMAP_v3.md          ← 竣工后扩写路线（四维×四阶段）
├── TASKS.md               ← 任务看板
├── PROGRESS.md            ← 完成度详情
├── EXPANSION_LOG.md       ← 扩写日志
├── EXPANSION_RECIPES.md   ← 扩写处方
├── CONVENTIONS.md         ← 写作规范
├── GOVERNANCE.md          ← 治理规则
├── HY3_WORK_PACKAGE.md    ← Hy3 工作包
├── FAQ.md / ISSUES.md / CONTRIBUTING.md / DEPENDENCY.md / ENGINEERING.md /
│   PROJECT_HANDBOOK.md / REVIEW.md / REFERENCES.md  ← 配套文档
├── glossary.json          ← 129 术语（带标准条款 + 章引用）
├── knowledge_graph.json   ← 147 章 / 16 part / 4 学习路径 / 5 质量门禁 / 3 build
├── learning_paths.json    ← 4 分层路径（beginner/intermediate/advanced/expert）
├── learning_paths.md      ← 学习路径 Markdown 版
├── source_map.json        ← 103 章映射到 libstdc++ 真实源文件 + 行号
├── Book/                  ← 147 章源文件（只读：不改，只通过 tools/ 处理后写 build/）
│   ├── part01_history/    ← 简史与标准（ch07–ch09）
│   ├── part02_toolchain/  ← 工具链（ch10–ch16）
│   ├── part03_language/   ← 核心语言（ch17–ch39）
│   └── ...（共 16 part）
├── tools/                 ← 40+ 工具脚本（门禁/审计/发布/扩写辅助）
├── examples/              ← 汇编/示例程序
├── build/                 ← 构建临时区（gitignored，不入库）
│   ├── site_out/          ← 静态站点成品
│   ├── site/              ← 中间工作目录（docs/ + mkdocs.yml）
│   ├── dashboard.html     ← 质量仪表盘
│   └── _root_artifacts/   ← 根目录编译产物归档（由 clean_root_artifacts 移入）
├── .github/workflows/ci.yml ← CI 四 job（quality/compile/site/pdf）
├── .gitignore             ← 已加固（含 build/ / site_out/ / *.exe / .workbuddy/）
└── make.bat               ← 构建入口
```

---

## 质量验证历史（四轮进展）

| 轮次 | 日期 | 主要工作 | 关键产出 |
|------|------|----------|----------|
| 第一轮 | 07-12 | v4 均分拉升 + 底线清零 | v4 15.4→17.1/30，全 16 part ≥15 |
| 第二轮 | 07-13 早 | **竣工**：站点修建 + git init + 导航中文标题 | mkdocs strict 0 警告（修 2 处链接翻倍） |
| 第三轮 | 07-13 午 | **文档真实缺陷修复**（5 源 + PRELUDE 22 头） | ch09 围栏/ ch161 fstream/ ch22+20+19 过时引用 |
| 第四轮 | 07-13 午 | **全维度质量核查 + 透明化**（锚点/mermaid/表格/JSON） | 0 真实缺陷；编译豁免清单；Mermaid 88 ① |

### 第三轮落地修复明细

| # | 文件 | 缺陷 | 影响 |
|---|------|------|------|
| 1 | `ch09_cpp26.md` | ```` ```cpp ```` 收尾缺失 → 后续被吞 | 真渲染损坏 |
| 2 | `ch161_logger.md` | `FileSink` 用 `std::ofstream` 却缺 `#include <fstream>` | 读者照抄必败 |
| 3 | `ch22_auto_decltype.md` | `概念（Concepts，ch 待补）` → ch67 | 过时断链 |
| 4 | `ch20_reference_pointer.md` | 删除「智能指针章发布后补锚点」 | 过时陈述 |
| 5 | `ch19_variables.md` | `待补` → `可选扩展（非必需）` | 去未完成暗示 |
| 6 | `chapter_compile_check.py` | PRELUDE 补 22 个常用标准库头（g++ 13.1 实测可用） | 消除误报 |

---

## 已知非 bug 编译失败（豁免清单）

`chapter_compile_check.py` 逐块隔离编译（每块包进 `namespace chk_{stem}_{idx}` 单 TU 校验），以下失败均为「教学序列/环境缺失/故意反例」，**非文档逻辑缺陷**——读者顺序阅读或在本机对应环境下均可编译。

| 章 | 失败块 | 性质 | 说明 |
|----|--------|------|------|
| `ch161_logger` | #1,#9,#17,#28,#30,#34（6） | FRAG / checker 伪影 | 跨块教学依赖：`Level`/`log_if`/`g_mtx`/`now` 在前序块定义；#9 的 `std::formatter` 特化被 namespace 包裹误报 |
| `ch11_compilers` | `max_of` 块 | 故意反例 | 展示 GCC/Clang/MSVC 推导冲突报错（原文标 `❌ 推导冲突`） |
| `ch12_buildsystems` | 若干 | FRAG/ENV | 依赖本地头 `_ch12_mylib.h`（有该头可编译） |
| `ch13_packaging` | 若干 | FRAG/ENV | pkg-config / 系统包依赖（本机缺失） |
| `ch16_ide` | 若干 | ENV | 依赖 Qt `QPushButton`（MinGW 未装 Qt） |

**判定原则**：凡属上表性质不计为真实缺陷。若某块出现语法错误/错误使用 std 符号/逻辑错误且非跨块依赖，方为真实 bug，须修。
**权威全量重验**：`chapter_compile_check.py` 全量 147 章（新 PRELUDE），明细见 `build/_root_artifacts/_full_newprelude_fail.txt`。

---

## 已排除的假阳性（避免误修）

| 项目 | 现象 | 根因 | 结论 |
|------|------|------|------|
| `ch162_json.md` 围栏 | cpp open=40 / close=9"不平衡" | 审计脚本误判：作者开闭围栏均带语言标记（```` ```text ``` ```` 开/闭），CommonMark 允许收尾带 info 串；旧全量编译 ch162 零 FAIL | 非缺陷 |
| `ch11 max_of` | 编译失败 | 故意展示编译失败的教学反例（`❌ 推导冲突`） | 非缺陷 |
| 16 处表格列不一致 | 审计报告 | 审计脚本列计数公式 bug + 字面管道假阳性（`\|\|`/`\|=or`/`filter\|transform`） | 非缺陷 |
| 4 处重复标题 | `ch03 <built-in>/<command-line>/<stdin>` | 编译器诊断讲解中重复小节，MkDocs 自动消歧 | 非导航断点 |

---

## 已知限制与注意事项

1. **CI / PDF 未实跑**：本机无 xelatex，PDF 与 CI 四 job 需推送 GitHub 后由 Actions 产出。
2. **Git 无 remote**：仓库已 `git init`（3 提交），无远端地址。提供 GitHub repo URL 即可 push。
3. **根目录编译产物可能回漏**：`chapter_compile_check.py` 仍可能把 `.cpp` 写回根目录；门禁（`hy3_check.py` / `pre_push_check.sh`）可检出，`clean_root_artifacts.py` 可清理。
4. **占位符 `~N` 未启用全自动门禁**：`~N` 在本手册大量作泛型变量/模板参数（如 `~N()` 析构），正则误报率高，改由人工 + `expansion_audit.py` 处理。
5. **配置脚本 `pre_push_check.sh` 含 Git Bash × Windows 坑**（见 USER.md `长期记忆 > Git Bash × Windows 原生 Python 脚本坑`）：路径须用 `cygpath -w` 转 Windows 原生再传 python；跨 shell 计数管道 `| grep -v | wc -l` 需 `|| true` 兜底。
6. **AGENT.md 部分旧数待更新**：Mermaid 块数（127→88）、编译失败数（76→15-18 FRAG/ENV）仍写旧值；以本文件（HANDOVER.md）与 `RELEASE.md` 的数字为准。

---

## 接手第一步（5 分钟检查清单）

```bash
# 1. 一键健康检查（含 asm 守卫）
python3 tools/hy3_check.py
# 期望: 全部 ✅

# 2. 推送前必跑（6 项预检）
bash tools/pre_push_check.sh
# 期望: 全部通过

# 3. 生成质量仪表盘
python3 tools/quality_dashboard.py
# 打开 build/dashboard.html 看全景

# 4. 如果断言缓存缺失（首次运行）
python3 tools/run_cpp_assertions.py > build/assert_report.txt
# 约 2-3 分钟，再跑 hy3_check.py 即全绿

# 5. 本地站点预览
PY="C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
"$PY" -m http.server 8123 --directory build/site_out --bind 127.0.0.1
# 浏览器打开 http://127.0.0.1:8123/

# 6. 建站（按顺序）
python3 tools/rewrite_links.py --mode site   # 1) 链接重写
python3 tools/gen_mkdocs_nav.py             # 2) 导航 + index.md（必须）
"C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/mkdocs.exe" build --strict -f build/site/mkdocs.yml  # 3) 构建
```

---

## 建议的下一步

### 环境阻塞项（需外部资源）
1. **提供 GitHub remote** → `git remote add origin <URL>` → `git push` → CI 四 job（quality/compile/site/pdf）自动实跑 → 获取 PDF artifact。
2. **本机装 xelatex**（TeX Live / MiKTeX）→ `bash tools/generate_pdf.sh` → 出版式 PDF。

### 内容增强项（须避开禁注水红线）
- `ROADMAP_v3.md` 四阶段按优先级推进：
  1. **A 样例重构**：14 章浅块 → 完整可编译程序
  2. **B 实证替换**：~N 估算 → GCC 13.1 实测 + godbolt 汇编
  3. **C 工业引用**：无工业引用章 → 真实 GitHub permalink
  4. **D 广度关联**：模板/模式章内部交引加强
- 参考：`EXPANSION_RECIPES.md`（Top5 逐章处方）、`EXPANSION_LOG.md`（进度模板）。
- **禁做**：增章（ch166+）、批量附录、为凑分注水、编造 WG21 数字/性能数据。

---

## 关键决策与经验（含踩坑）

1. **"禁注水"是第一红线**：密度已达天花板，继续推分 = 零信息增量。宁可诚实标注 FRAG/ENV/故意反例，不可为了凑绿而掩盖。
2. **发布管线顺序**：`rewrite_links → gen_mkdocs_nav → mkdocs build`。漏第二步会丢 `index.md` + 导航用裸目录名。
3. **链接翻倍根因**：`rewrite_links.py` 只重写"目标能在章节索引解析"的链接。错章号（`ch72_concepts.md` 不存在实体文件）→ rewrite 跳过 → MkDocs 路径翻倍 → strict 构建中止。不是 rewrite 的 bug，是源文件的交叉引用错误。
4. **CommonMark 围栏变体**：收尾围栏允许带 info 串（```` ```text ```` 闭合 ```` ```text ```` 合法）。审计脚本不要用裸 `` ``` `` 做唯一闭合标识，会误报 ch162 等"不平衡"。
5. **后台任务输出丢失**：Git Bash 后台 `> file 2>&1` 若进程被会话切换 kill，文件 0 字节。编译重验这类重活在前台跑或用 `run_in_background` + `TaskOutput` 阻塞取 stdout。
6. **Git Bash × Windows 路径坑**（已写入用户级记忆）：`pwd` POSIX 路径 `/c/...` 传给 Windows 原生 exe → `C:\c\...` 误读。解决：`ROOT_WIN=$(cygpath -w "$ROOT")`。`pipefail` + `set -e` + `grep 空输出` → 脚本中止，需 `|| true`。

---

_生成时间：2026-07-13 13:55 | 第四轮质量核查完结后全量重写_
_上一代 Agent：WorkBuddy（阿信） → 第四轮由 WorkBuddy 续推_
_AGENT.md 部分旧数（Mermaid 127、编译失败 76）待下一轮独立修订；以本文件 + RELEASE.md 的数字为准。_
