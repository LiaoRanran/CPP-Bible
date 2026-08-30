# NEXT_LLM.md — 项目接手入口（2026-08-30 快照，零上下文即可接手）

> **本文件是唯一权威接手入口。** 读完就能开始干活。不需要读 AGENT.md / HANDOVER.md / START_HERE.md。
> 上一版（2026-07-17，停在 APP15）已过时作废，本版覆盖到 2026-08-30 升级战役收官。

---

## 30 秒速览

| 问题 | 答案 |
|------|------|
| 什么项目？ | 《现代 C++ 终极圣经》147 章 C++ 技术书 + Python 质量门禁工具链，仓库 `LiaoRanran/CPP-Bible` |
| 根目录？ | `C:/CodeLearnling/note/note/C++/CPP-Bible/` |
| 当前阶段？ | **quality_consolidation（第三阶段：质量收尾 + 高含金量升级）**，CI 八 job 已首次全链路真绿 |
| 在飞的活？ | 无——上一批 ch01/08/09/10 完整化已提交并推送（见「已收口批次」） |
| 剩余待办？ | 见「遗留清单」：55 断言 WARN 分类、legacy 审计人工复核（异盘备份已落 D:\） |
| HEAD？ | `6d7d6e9`（本地 = origin/master，无分叉） |
| 编译器？ | MinGW GCC 15.3：`C:/Qt/Tools/mingw1530_64/bin/g++.exe`（`-std=c++23`） |
| Python？ | 项目 `.venv/Scripts/python.exe`（uv 管理）；门禁内部调 `C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe` |
| 权威文档？ | `STATE.json`（事实源）+ `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` + `UPGRADE_PLAN_2026-08-30.md` |

---

## 启动序列（4 步确认现状）

```powershell
cd C:/CodeLearnling/note/note/C++/CPP-Bible

# 1. 确认 HEAD 与远程一致（应无 ahead/behind）
git status -sb ; git log --oneline -3

# 2. 看工作树（应只有 ch01/08/09/10 + 编译报告产物未提交）
git status --short

# 3. 跑质量门禁（期望 16/16）
.venv/Scripts/python.exe tools/cppbible.py check --stage quality

# 4. 跑编译门禁（期望 5/5，全量约 3-5 分钟）
.venv/Scripts/python.exe tools/cppbible.py check --stage compile
```

---

## ⚠️ 接手须知（三个易错点）

1. **先读 STATE.json 的 `last_commit`/`git_status` 与 `ISSUES.md` 遗留清单**，不要信 HANDOVER.md / START_HERE.md / .workbuddy/memory/MEMORY.md 的旧数字（均停留在 07 月）。
2. **核心门禁是 `tools/cppbible.py check --stage quality|compile`**，它聚合了 consistency/crossref/density/D5/ASM/whitespace 等 16 项 + compile/gate/exempt/D5-gate/assertions 5 项。单独跑 `tools/consistency_check.py` 已不足够。
3. **不注水红线仍在**：147 章上限锁定、不增章、不批量附录、汇编必须 GCC15.3 真机 objdump、不可用特性诚实标注。

---

## 已收口批次（2026-08-30，勿重做）

### ch01/02/08/09/10 cpp 块完整化 → ✅ 已提交并推送

- **目标**：把 part01 历史章的 2-3 行 fragment 示例，升级为「含 `int main()` + 显式 `#include`」的自包含可编译程序；不可编译的示意块（如 C++26 反射/契约语法）改为 ` ```text ` 围栏。
- **已完成并推送**：ch01/08/09/10（`+332/-52`）→ 提交 `7e99ea9` + `b1bd202` + `6d7d6e9`。
- **已验证**：ch02_standardization 实测已完整（18 cpp 块 19 main），无需处理。
- 门禁：quality 16/16、compile 5/5 双绿，CI 八 job 已触发。

### 已执行提交（留档，勿重跑）

```powershell
# 内容提交（4 章）
git add Book/part01_history/ch01_c_history.md Book/part01_history/ch08_cpp23.md Book/part01_history/ch09_cpp26.md Book/part01_history/ch10_version_matrix.md
git commit -m "feat(part01): ch01/08/09/10 cpp 块完整化——fragment 改自包含可编译程序"

# 门禁产物（编译报告随内容更新）
git add tools/compile_report.json tools/exempt_audit_report.json
git commit -m "chore(gate): 更新 GCC15 编译报告基线（ch01/08/09/10 完整化后）"
```

---

## 遗留清单（绿色为待办，按优先级）

| # | 事项 | 入口 | 说明 |
|---|------|------|------|
| 1 | ch01/08/09/10 完整化收口 | ✅ 已完成 | 已推送 `7e99ea9` + `b1bd202` + `6d7d6e9` |
| 2 | 55 断言 WARN 分类与豁免收敛 | 审计报告 §5.2 / §8.3 | 阶段 C；`run_cpp_assertions.py` 输出 WARN 分「隔离伪影/故意演示/真实缺陷」 |
| 3 | legacy 审计候选人工复核 | 审计报告 §5.3 | 10 unsafe C / 94 裸 new / 101 reinterpret_cast，分批留档（`audit_cpp_defects.py`） |
| 4 | 备份第二故障域 | ✅ 已完成 2026-08-30 | 已推 `D:\CPP-Bible-Backup\20260830-201021`（明文副本，恢复演练 PASS），见本节末 |
| 5 | 站点/PDF/EPUB 本地重建 | 审计报告 §11 | 本机缺 pandoc/xelatex/mkdocs，出版产物走 CI 八 job |

---

## 关键文件速查

| 文件 | 作用 | 接手必读 |
|------|------|:--:|
| **NEXT_LLM.md** | **本文件——唯一权威接手入口** | ✅ |
| `STATE.json` | 进度状态 + execution_order + metrics（事实源 build/metrics.json 派生） | ✅ |
| `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` | 全量审计 + 风险清单 + 路线图 | ✅ |
| `UPGRADE_PLAN_2026-08-30.md` | 升级方案（7 目标 / 阶段 A-D / 关键决策） | ✅ |
| `CONTENT_DEPTH_ROADMAP.md` | **内容深化主线**（三阶：汇编实证矩阵 / 实战项目线 / 陷阱体系） | ✅ |
| `ISSUES.md` | 遗留清单（2026-08-30 口径） | ✅ |
| `docs/references/content_debt_tasklist.md` | 内容债任务单（已清零，留档） | 需要时 |
| `tools/cppbible.py` | 门禁聚合入口（quality/compile） | ✅ |
| `tools/consistency_check.py` | 一致性门禁（147 章 ERROR=0 WARN=0） | 参考 |
| `Book/part*/ch*.md` | 147 章正文 | 按批 |

---

## 环境要点

- **工具链事实源**：`toolchain.toml`（GCC 15.3.0 已钉）。
- **本机已装**：GCC 15.3.0、uv、项目 `.venv`。
- **本机缺失**（依赖 CI）：pandoc、xelatex、mkdocs、ruff、mypy、cmake。
- **Windows 中文控制台坑已修**：工具已统一 UTF-8 输出（`xref_check.py`、`cppbible.py` 入口）。
- **行尾约定**：仓库 markdown 为 CRLF，`git config core.autocrlf false`（已设），注入脚本须 bytes 级处理行尾避免整文件伪 diff。

---

## 快速恢复（模型被打断后）

```
1. 读本文件（NEXT_LLM.md）
2. 读 STATE.json（last_commit / git_status）+ ISSUES.md 遗留清单
3. git status -sb 看工作树（ch01/08/09/10 是否还在）
4. 跑 tools/cppbible.py check --stage quality（16/16）
5. 从「在飞的活」续做，不要回头重做已完成批次
```

---

_重写时间：2026-08-30 | 覆盖到升级战役收官（CI 八 job 真绿，b90fa5d）_
_HEAD：445eaa5 | 本地 = origin/master，无分叉_
_上一版 NEXT_LLM.md（2026-07-17，APP15 阶段）已作废，由本版全面替换_