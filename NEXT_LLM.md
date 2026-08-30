# NEXT_LLM.md — 项目接手入口（2026-08-30 快照，零上下文即可接手）

> **本文件是唯一权威接手入口。** 读完就能开始干活。不需要读 AGENT.md / HANDOVER.md / START_HERE.md。
> 上一版（2026-07-17，停在 APP15）已过时作废，本版覆盖到 2026-08-30 深夜——JSON 台阶二收尾 + 工具链升级剩余项规划。

---

## 30 秒速览

| 问题 | 答案 |
|------|------|
| 什么项目？ | 《现代 C++ 终极圣经》147 章 C++ 技术书 + Python 质量门禁工具链，仓库 `LiaoRanran/CPP-Bible` |
| 根目录？ | `C:/CodeLearnling/note/note/C++/CPP-Bible/` |
| 当前阶段？ | **quality_consolidation（第三阶段：质量收尾 + 高含金量升级）**，CI 八 job 已首次全链路真绿 |
| 在飞的活？ | 无——工具链升级 P0-1 / P0-2 已收口（ruff 债务人工清零 + 接入 CI 硬门禁 + 控制台编码修复），见「已收口批次」 |
| 剩余待办？ | 工具链升级剩余项见 `TOOLCHAIN_UPGRADE_NEXT.md`（mypy 类型 triage + 容器 digest + 指标事实源 + CROSSREF 裁决）；内容五阶主线见 `CONTENT_DEPTH_ROADMAP.md` |
| HEAD？ | **一律以 `git rev-parse HEAD` 为准**——本文件不复制哈希。写死的哈希在提交那一刻就已过期，这正是「指标单一事实源」待办项要根治的反例 |
| 编译器？ | MinGW GCC 15.3：`C:/Qt/Tools/mingw1530_64/bin/g++.exe`（`-std=c++23`） |
| Python？ | ✅ 已收敛：配置 glob 识别托管 3.13.14 + `toolchain.py` 版本自检（漂移即非零退出）；`.venv` 仍 3.14.5 但不影响门禁（门禁改走托管 3.13.14） |
| 权威文档？ | `STATE.json`（事实源）+ `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` + `UPGRADE_PLAN_2026-08-30.md` + `TOOLCHAIN_UPGRADE_NEXT.md` |

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

### 工具链升级 P0-1 / P0-2 完成 → ✅ 已提交

- **P0-1 Python 版本收窄（`fc784ba`）**：`toolchain.toml` 的 `[python].prefer` 改 glob `versions/3.13.*/python.exe`（容忍目录名 3.13.12 但其内二进制实 3.13.14）+ 新增 `expected="3.13"`；`toolchain.py` 加 `resolve_python_version()` 版本自检（漂移即非零退出）；**单一事实源收敛**（`cppbible.py`/`snapshot.py`/`pyproject.toml` 的 4 处 `3.13.12` 硬编码 → 1 处 glob）；新增 `.python-version`=`3.13`。quality 16/16 回归通过。
  - 后续修订：`resolve_python()` 的 glob 候选排序由字典序改为**版本号数值排序取最高 patch**（字典序会把 `3.13.12` 排在 `3.13.2` 之前）。
- **P0-2 静态检查链完成**：`pre-commit` 已装（`uv tool install pre-commit`）；用钉定版本 `ruff==0.6.9`（非最新 0.16.5，避免规则集漂移）对 `tools/` 做安全自动修 150 处（`4f62438`），随后**人工清零剩余 99 处**（E741×34 变量改名 / E701×27 + E702×21 拆行 / F841×17 删死变量，逐个确认语义），并接入 `ci.yml` quality job 硬门禁。`ruff check tools/` 现为 `All checks passed`。
- **Windows 控制台编码坑修复**：`toolchain.py` 入口 reconfigure + `cppbible.py` `run()` 对**所有子进程**注入 `PYTHONIOENCODING=utf-8:replace`。**修复前，默认 GBK 控制台下 quality 实为 15/16 exit=1**（`d5_appendix_audit.py` 打印 ✅ 抛 `UnicodeEncodeError`）——上一版记录的「16/16」只在 UTF-8 环境下成立；修复后默认控制台即 16/16 exit=0，结论不再依赖环境。
- **剩余（勿算本次已做）**：mypy 全程未动（需 `uv sync --extra dev` 装依赖 + 类型标注 triage，量大）+ 后续 P1/P2 项。详见 `TOOLCHAIN_UPGRADE_NEXT.md`。

### JSON 贯穿项目线（台阶二）→ ✅ 已提交并推送

- **范围**：台阶二「贯穿全书实战项目线」首个项目 = 手写 JSON 库（`Examples/json/`），里程碑 M1–M4 全部完成。
- **已完成**：
  - 骨架 + 46 例自测 → 错误行号/可变编辑/点路径（62 例）→ UTF-8 完整转义含代理对（68 例）→ 美化序列化 + demo → 数字三元组分流 int64/uint64/double（84 例，大整数无损）。
  - ch162 正文「项目实战回链」：模块↔章节映射表 + 可导航链接。
  - **门禁纳入 CI**：`tools/json_project_gate.py` + `ci.yml` compile job 新增 JSON Project Gate（gcc-only 硬门禁），本地 GCC15.3 实测 2/2。
- **提交**：`fb329d5`(P1 内存实证) → `d295733`…`7263d27`(JSON M1–M4) → `502387d`(回链) → `4b04439`(门禁入 CI) → `972bbe9`(回链可导航化)。

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
| 6 | 工具链升级剩余项（Python 收窄/静态检查链/指标事实源/容器 digest/CROSSREF 裁决） | `TOOLCHAIN_UPGRADE_NEXT.md` | 🔶 P0 全完成 + P1 两项完成 + P2 完成；只剩 mypy 类型 triage |

---

## 关键文件速查

| 文件 | 作用 | 接手必读 |
|------|------|:--:|
| **NEXT_LLM.md** | **本文件——唯一权威接手入口** | ✅ |
| `STATE.json` | 进度状态 + execution_order + metrics（事实源 build/metrics.json 派生） | ✅ |
| `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` | 全量审计 + 风险清单 + 路线图 | ✅ |
| `UPGRADE_PLAN_2026-08-30.md` | 升级方案（7 目标 / 阶段 A-D / 关键决策） | ✅ |
| `TOOLCHAIN_UPGRADE_NEXT.md` | 工具链升级剩余项执行规划（P0-P2 五剩余项 + CROSSREF 裁决策略） | ✅ |
| `metrics.schema.json` | **指标单一事实源定义**（12 个字段 + 出处 + 可回写字段 + 待校验正则） | ✅ |
| `tools/gen_metrics.py` | 指标落地校验器：`--check` 校验文档写死数字（CI 硬门禁）/ `--sync` 回写 STATE.json 派生字段 | ✅ |
| `CONTENT_DEPTH_ROADMAP.md` | **内容深化主线**（五阶：汇编实证矩阵 / 实战项目线 / 陷阱体系 / 人文温度 / 内容形态补全） | ✅ |
| `docs/references/P1_memory_object_model_checklist.md` | 台阶一 P1 内存/对象模型实证结论清单（强模型定结论，弱模型施工图） | ✅ |
| `ISSUES.md` | 遗留清单（2026-08-30 口径） | ✅ |
| `docs/references/content_debt_tasklist.md` | 内容债任务单（已清零，留档） | 需要时 |
| `tools/cppbible.py` | 门禁聚合入口（quality/compile） | ✅ |
| `tools/consistency_check.py` | 一致性门禁（147 章 ERROR=0 WARN=0） | 参考 |
| `Book/part*/ch*.md` | 147 章正文 | 按批 |

---

## 外部参考范式手册（台阶五范式来源）

用户此前用其他 Agent 搓成的两份独立手册，位于本机 `docs/references/external/`（已 `.gitignore`，**未随仓库推送**，仅本地作范式参照），**非本书内容、不占章节**：

| 文件 | 是什么 | 对本项目的用途 |
|------|--------|----------------|
| `docs/references/external/C语言极致详解手册.md` | C 语言完整手册（逐行注释演示体） | 台阶五子线 C「基础语法逐行演示」的范式 |
| `docs/references/external/Linux内核极致详细手册.md` | Linux 内核逐行注释版（CFS 调度 / 伙伴系统等真实内核源码精读） | 台阶五子线 D「标准库源码剖析」的范式；系统级视角 |

> 后续接手 Agent 写「逐行演示」「源码剖析」前，先读这两份范文，对齐风格与深度。

---

## 环境要点

- **工具链事实源**：`toolchain.toml`（GCC 15.3.0 已钉）。
- **本机已装**：GCC 15.3.0、uv、项目 `.venv`、pre-commit（`uv tool install pre-commit`，隔离）；ruff 可经 `uvx "ruff==0.6.9"` 临时拉取。
- **本机缺失**（依赖 CI）：pandoc、xelatex、mkdocs、mypy、cmake。
- **Windows 中文控制台坑已修（两处，缺一不可）**：①`cppbible.py` 入口 reconfigure 自身 stdout；②其 `run()` 对**所有子进程**注入 `PYTHONIOENCODING=utf-8:replace`。只做①时子进程（如 `d5_appendix_audit.py` 打印 ✅）仍会在 GBK 控制台抛 `UnicodeEncodeError`——这正是「quality 16/16」一度只在 UTF-8 环境下成立的原因。`toolchain.py` 自带 reconfigure 可单独跑；其余 `tools/*.py` 若单独直接运行仍有此坑，需要时 `chcp 65001` 或设 `PYTHONIOENCODING=utf-8`。
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

_更新时间：2026-08-31 | 覆盖到 JSON 台阶二收尾 + 工具链升级 P0-1/P0-2 完成（ruff 清零 + CI 硬门禁 + 控制台编码修复）_
_HEAD：不写死——一律以 `git rev-parse HEAD` 与 `git status -sb` 为准（写死的哈希在提交那一刻即过期）_
_历史：2026-07-17 版（APP15 阶段）已作废；2026-08-30 深夜版停在「P0-2 一半」，其 HEAD 尾注当时已落后一个提交，且 push 状态标反_