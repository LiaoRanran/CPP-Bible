# NEXT_LLM.md — 下任大模型接手脚本

> 专为 LLM Agent 设计：自包含、可执行、无需人类判断。
> 读完本文件 + `AGENT.md`（宪法）即可开工。

---

## 0. 环境速查

```bash
PY="C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
GPP="C:/Qt/Tools/mingw1310_64/bin/g++.exe"
MKDOCS="C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/mkdocs.exe"
ROOT="C:/CodeLearnling/note/note/C++/CPP-Bible/"
```

所有工具用 `"$PY" tools/xxx.py` 调用。**禁止**用 `python3` 或 `python`（路径不可靠）。

---

## 1. 接手工序（5 分钟，3 条命令）

```bash
# 命令 1：状态验证（秒级）
"$PY" tools/hy3_check.py
# 期望: "✅ 全部通过 — 项目健康"

# 命令 2：v4 审计（秒级）
"$PY" tools/deduplication_audit.py --all 2>&1 | head -15
# 期望: v4=13 池为空，最低分=14

# 命令 3：门禁
"$PY" tools/consistency_check.py 2>&1 | tail -3
# 期望: "ERROR=0 WARN=0" + "100/100"
```

**如果三项全过** → 项目健康，可以开始工作。
**如果某项失败** → 先看 `HANDOVER.md`「已知限制与注意事项」排查，再读 `RELEASE.md`。

---

## 2. 三种合法工作方向（选一个开始）

### 方向 A：铺路（附录 G 注入，v4 抬分）

1. 跑 `"$PY" tools/deduplication_audit.py --all 2>&1` 看 v4 排名
2. 取 v4 最低的 5 章，按 IND 排序（IND 越低 → 越需要工业引用）
3. 对每章：
   a. 读章头找主题
   b. 找 `## 自测练习（Exercises）` 前的那行（`- **同模块**：...` 或 `> 交叉引用：...`）
   c. 在它和 `## 自测练习` 之间插入「附录 G」，模板：

```
## 附录 G：{主题}工业实践与深度

| 项目/库 | 技术/模式 | 使用场景 | 源码/链接 |
|---------|----------|---------|----------|
| **LLVM**（github.com/llvm/llvm-project） | ... | ... | `llvm/include/...` |
| **Chromium**（github.com/chromium/chromium） | ... | ... | `base/...` |
| **Qt**（code.qt.io） | ... | ... | `qtbase/...` |
| **Boost**（github.com/boostorg/xxx） | ... | ... | `include/...` |
| **Google/Abseil**（github.com/abseil/abseil-cpp） | ... | ... | `absl/...` |

**底层深度**：{一段 ≥5 行的汇编/性能/编译器行为分析}
```

4. 每批 5 章完成后：
   a. 跑 `"$PY" tools/consistency_check.py` + `"$PY" tools/crossref_audit.py` 确认无断链
   b. 跑 `"$PY" tools/deduplication_audit.py --all 2>&1 | head -12` 看 v4 最低是否抬升
   c. `git add -A && git commit -m "feat: 附录G注入 chXX~chYY (v4 X→Y)"`

**关键约束**：
- 项目引用必须真实可查（GitHub link 为 permalink）
- 每条附录 ≥10 行实质性内容
- 不编造性能数据、不编造 GitHub 链接
- 禁止重复关键词堆砌（同一项目名在表内重复出现不计数）

### 方向 B：浅块重构（ROADMAP_v3 阶段 A）

1. 跑 `"$PY" tools/expansion_audit.py --top 20` 看清块优先队列
2. 对每个高优先级"浅块"（代码块 <10 行、缺 main、缺头文件）：
   a. 补全头文件（`auto_include.py --dry-run` 辅助）
   b. 补 `int main()` + 示例调用
   c. 跑 `"$PY" tools/chapter_compile_check.py Book/partXX/chYYY.md` 确认编译通过
3. 每批完成后跑门禁

### 方向 C：基础设施（GitHub CI / PDF）

1. **CI 实跑**：需 GitHub repo URL → `git remote add origin <url>` → `git push` → 等 Actions
2. **PDF 生成**：需本机有 xelatex → `bash tools/generate_pdf.sh`
3. **站点重建**：`"$PY" tools/rewrite_links.py --mode site` → `"$PY" tools/gen_mkdocs_nav.py` → `"$MKDOCS" build --strict -f build/site/mkdocs.yml`（三步骤顺序不可变）

---

## 3. 当前项目数据（2026-07-13 午实测）

| 维度 | 数值 | 来源 |
|------|------|------|
| 章节 | 147 章 / 16 part | `Book/` |
| 行数 | 143,469 行 | 逐文件累加 |
| cpp 块 | 7,013 | ```` ```cpp ```` 计数 |
| 交引 | 1,190 / 0 断链 | `crossref_audit.py` |
| Mermaid | 88 块（全部有效） | `Book/` 实测 |
| 表格 | 597（0 真实缺陷） | 2026-07-13 审计 |
| v4 均分 | 17.8/30 | `deduplication_audit.py` |
| v4 最低 | 14（v4=13 池已清零） | 同上 |
| GPA | 98.7（0 HIGH 缺陷） | `chapter_lint.py` |
| 门禁 | 100/100 | `consistency_check.py` |
| 断言 | FAIL=0 | `run_cpp_assertions.py` |
| asm | DRIFT=0 | `verify_asm_evidence.py` |
| 站点 | mkdocs strict 0 警告 | `mkdocs build --strict` |
| Git | 5 提交，无 remote | `git log --oneline` |
| 已注入附录 G | 20 章（ch17/ch32/ch50/ch60/ch64/ch67/ch68/ch80/ch99/ch107/ch137/ch142/ch145/ch154/ch162 + 本轮 ch07(G)/ch10(H)/ch92(G)/ch109(I)/ch117(G)） | — |

**v4=14 池（剩余可铺章，2026-07-13 第六轮后剩 9 章）**：ch13_packaging(IND=80) / ch62_specialization(IND=14) / ch76_stl_arch(IND=6) / ch79_list(IND=19) / ch121_contracts(IND=6) / ch129_qt(IND=83) / ch148_gitflow(IND=23) / ch149_ci_cd(IND=35) / ch155_simd(IND=4) |

---

## 4. 工具调用规范

- 所有 Python 调用：`"$PY" tools/xxx.py`
- 单章编译：`"$PY" tools/chapter_compile_check.py Book/partXX/chYYY.md`
- 读取文件：优先用 Read 工具（非 Bash cat）
- 编辑文件：优先用 Edit 工具（非 Bash sed）——**必须先 Read 再 Edit**
- Git Bash 下路径带空格需双引号；POSIX 路径给 Windows exe 前用 `cygpath -w` 转换
- 后台编译重验用 `run_in_background: true`，不轮询（等通知）

---

## 5. 红线（禁止事项）

1. **禁止注水**：不堆砌关键词、不批量追加空表、不编造 GitHub 链接
2. **禁止增章**：147 章规模已定，不新增 ch166+
3. **禁止伪造**：asm 符号必须 ⊆ `Examples/*.asm` 真实产物；WG21 提案号/库版本不确定 = 不写
4. **禁止单行追加**：每条新内容 ≥5 行，有信息增量
5. **禁止改门禁语义**：不修改检查器规则来"凑绿"

---

## 6. 参考文档

| 需要什么 | 看什么 |
|---------|--------|
| 项目宪法 + 红线 + 工具清单 | `AGENT.md` |
| 当前详细快照 + 四轮验证历史 + 踩坑 | `HANDOVER.md` |
| 发布基线 + 编译豁免清单 | `RELEASE.md` |
| 总索引（阅读顺序/工具地图） | `INDEX.md` |
| 竣工路线 | `ROADMAP_v2.md` |
| 扩写路线 | `ROADMAP_v3.md` |
| 扩写处方模板 | `EXPANSION_RECIPES.md` |
| 项目长期记忆 | `C:/Users/ASUS/WorkBuddy/2026-07-07-08-47-50/.workbuddy/memory/2026-07-13.md` |

---

_生成时间：2026-07-13 14:15 | 为下一个 LLM Agent 接手铺路_
