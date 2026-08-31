# NEXT_LLM.md — 项目接手入口（2026-08-30 快照，零上下文即可接手）

> **本文件是唯一权威接手入口。** 读完就能开始干活。不需要读 AGENT.md / HANDOVER.md / START_HERE.md。
> 上一版（2026-07-17，停在 APP15）已过时作废，本版覆盖到 2026-08-30 深夜——JSON 台阶二收尾 + 工具链升级剩余项规划。

---

## 30 秒速览

| 问题 | 答案 |
|------|------|
| 什么项目？ | 《现代 C++ 终极圣经》147 章 C++ 技术书 + Python 质量门禁工具链，仓库 `LiaoRanran/CPP-Bible` |
| 根目录？ | `C:/CodeLearnling/note/note/C++/CPP-Bible/` |
| 当前阶段？ | **quality_consolidation（第三阶段：质量收尾 + 高含金量升级）**，CI 八 job 已全链路真绿 |
| 在飞的活？ | 内容侧「学习目标→问题驱动论证」打磨进行中——已收口 **46 章**（历史9 + OO6 + STL/现代10 + 模板12 + STL板块10），见「已收口批次（2026-09-01）」；**下一批 12 章（现代 ch116/120/122/123 + 语言 ch22/24/29/30/32 + 性能 ch152/153/158）已委托后台 Agent 执行中**，完成后需本地 quality 门禁验证 + 提交 |
| 剩余待办？ | 后台 Agent 完成后：验证 quality 门禁 → 提交 → 更新本文件收口批次；工具链升级剩余项见 `TOOLCHAIN_UPGRADE_NEXT.md`（mypy 类型 triage 等）；内容侧**优先审 8 个 UNVERIFIED 章**（ch02/05/16/132/148/149/150/165），见下文健康度评估；ch163 网络章是否补 POSIX 对照（低优先） |
| HEAD？ | **一律以 `git rev-parse HEAD` 为准**——本文件不复制哈希。写死的哈希在提交那一刻就已过期，这正是「指标单一事实源」待办项要根治的反例 |
| 编译器？ | MinGW GCC 15.3：`C:/Qt/Tools/mingw1530_64/bin/g++.exe`（`-std=c++23`） |
| Python？ | ✅ 已收敛：配置 glob 识别托管 3.13.14 + `toolchain.py` 版本自检（漂移即非零退出）；`.venv` 仍 3.14.5 但不影响门禁（门禁改走托管 3.13.14） |
| 权威文档？ | `STATE.json`（事实源）+ `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` + `UPGRADE_PLAN_2026-08-30.md` + `TOOLCHAIN_UPGRADE_NEXT.md` |

---

## 启动序列（1 条命令确认现状）

**接手第一步只跑这一条**：

```powershell
cd C:/CodeLearnling/note/note/C++/CPP-Bible
python tools/handover_check.py            # 约 2 分钟；加 --quick 只要几秒
```

它会一次性核对「接手文档里的声称是否与实际情况一致」。**这一步不是可选
的**——2026-08-31 实测，本文件当时三处声称与实际不符：`quality 16/16`
在默认控制台实为 15/16；`HEAD` 尾注记错且 push 状态记反；系统 python
版本记 3.10.11 而实测 3.14.5。直接信文档就会在错误的前提上开工。

覆盖项：git 同步（ahead / behind / 脏文件）、文档写死数字 vs 事实源、
ruff、quality 门禁；并打印接手简报（事实快照 + 剩余待办 + 已知陷阱）。
退出 0 = 现状可信；非 0 = 先处理再干活。

需要更细控制时再单独跑：

```powershell
.venv/Scripts/python.exe tools/cppbible.py check --stage quality   # 期望 16/16
.venv/Scripts/python.exe tools/cppbible.py check --stage compile   # 期望 5/5，3-5 分钟
```

---

## ⚠️ 接手须知（三个易错点）

1. **先读 STATE.json 的 `last_commit`/`git_status` 与 `ISSUES.md` 遗留清单**，不要信 HANDOVER.md / START_HERE.md / .workbuddy/memory/MEMORY.md 的旧数字（均停留在 07 月）。
2. **核心门禁是 `tools/cppbible.py check --stage quality|compile`**，它聚合了 consistency/crossref/density/D5/ASM/whitespace 等 16 项 + compile/gate/exempt/D5-gate/assertions 5 项。单独跑 `tools/consistency_check.py` 已不足够。
3. **不注水红线仍在**：147 章上限锁定、不增章、不批量附录、汇编必须 GCC15.3 真机 objdump、不可用特性诚实标注。

---

## 已收口批次（2026-09-01，勿重做）

### 内容打磨：学习目标 → 问题驱动论证（46 章，分 6 批提交，勿重做）

- **范式**：把「① 学习目标」纯罗列清单改写为「① 我们真正要回答的问题 <span class="badge badge-std">标准</span>」论证式导读——每个问题**先立判断再给论据**，逐条回指正文节号（⑦⑧⑨⑩⑬⑮等，均核证属实），保留前向导航链接与示例代码；章节回指错误已修正（如 ch80 ⑨ 实为"调用栈/时序图"而非"栈布局"）。
- **批次**：
  - `fd6897a` ch121 试点 → `bc4fd45` 历史 9 章（ch01, ch04–ch10）→ `e2ffc76` OO 6 章（ch47–52）→ `dc8ed07` STL/现代 4 章（ch80/82/83/115）→ `65b3bf1` STL 容器 4 章（ch77/84/85/86）→ `f80c7cd` 模板板块 12 章（ch60–64/66–72）→ `5cf5362` STL 板块 10 章（ch76/78/79/87/89–94）。
- **内容准确性修正（禁虚构红线）**：ch85 原声称「C++20 透明哈希」——透明哈希对 unordered 容器**并未进入标准库**（`std::hash` 非 transparent），已改为诚实表述；ch83 消除反引号内 `Book/` 前缀引用。
- **门禁**：每批本地 preflight 均 17/17 通过；CI 最近 4 run（10dc21e/dc8ed07/e2ffc76/65b3bf1）**全绿**（f80c7cd/5cf5362 两批已提交，CI 待确认）。
- **下一批（已委托后台 Agent，2026-09-01 执行中）**：现代 ch116/120/122/123 → 语言 ch22/24/29/30/32（ch24 模板节为「② 学习目标与前置知识」，格式特殊需保留前置知识部分）→ 性能 ch152/153/158。完成后：本地 quality 门禁 17/17 → 分批提交 → 更新本段。

### ch157 断言过强修复 → ✅ 已提交并全绿

- **现象**：CI Assertion Claims 门禁失败，`assert(s > -1.0 && s < 1.0)` 数学不成立——`s` 是 1000 个 `sin·cos` 之和，理论范围 ±500，实测 sum=353.8 必炸。
- **修复**：改为按 `M` 推导的真实上界 `±(M/2+1)` 并加 `std::isfinite`，本地 GCC 15.3 复现并修复，Assertion Claims 门禁通过。
- **提交**：`10dc21e`，CI 九 job（含 pdf/epub/site/deploy）全绿。

---

## 已收口批次（2026-08-31，勿重做）

### 交叉引用 Book/ 前缀结构性硬伤 → ✅ 已提交并已验证（模板级顽疾，根治+防复发）

- **现象（外部审计完整复核，全量 2941 条链接）**：SUMMARY.md 总目录 147/147 全有效；**147 章正文的 markdown 链接失效率 100%**——正文一律写成 `](Book/partXX/chYY.md)` 根相对路径，而章文件已在 `Book/` 内，任何标准相对渲染器（GitHub 预览/编辑器/mdBook）按当前文件目录解析 → 路径翻倍一层 → 一律 404。根因单一：SUMMARY 由 `gen_indexes.py` 生成、本就是相对路径，而正文引用是手写 `Book/` 前缀，两套路径规则从未对齐，且无链接可达性卡口。
- **掺假对照（值得警惕）**：zip 内 147 章元数据全部落在 2026-08-31 09:27–18:54（GitHub Actions 流水线全书级重跑）。重跑后 `Book/` bug **一字未变、100% 保留**——证明 (a) 质量门禁从未检查内部跳转链接可达性；且更可能 (b) `Book/` 前缀写在生成模板/prompt 里，每次重新生成都会原样复现。**只重跑没用，必须改模板/加卡口，否则 bug 随每次自动更新永久续命。** 区别在于：shared_from_this()/无锁栈 pop 两处此前的语义修正，重跑后依然保持修好状态 → 流水线不是暴力覆盖重写，不会把改好的改坏。
- **修复**：新增 `tools/fix_book_links.py`（字节级幂等修复器，`--check`/`--apply`），把 `](Book/` 改写为以当前章为基准的 `](../partXX/chYY.md)` 源相对路径，共修 **2628 处 / 147 章**。**字节级外科替换是硬要求**——仓库 markdown 为 CRLF（`core.autocrlf false`），文本模式 read/write 往返会把全文件行尾改坏（首轮因此产生 23.8 万行伪 diff 已回滚；字节级后净变更 = 链接量 2458/2431 行）。
- **协调式配套（防发布/审计口径退化）**：
  - `tools/rewrite_links.py` 支持源相对 `../partNN/` 形态（C），PDF 合并单文件归一化回 `Book/` 目标再映射 `#chNN` 锚点；site（174 文件/4772 重写/自检通过）+ pdf（3004 重写/147 H1 锚点/自检通过）双模式回归通过。pdf 仅 4 处 `../../docs/…`+`../../Appendix/…` 预存 warning（zip 范围外、非本次引入）。
  - `tools/crossref_audit.py` 新增 `REL_LINK_RE` 计数源相对链接（**按 Book 根解析**：`../` 恒指 Book 以便 `(ch.parent.parent / r)`），避免覆盖率口径缩水；修复后断链 0、part 覆盖率 100%。
  - `tools/cppbible.py` + `ci.yml`（quality job 新步骤）+ `pyproject.toml:quality_gates` 新增 **「Book Link Integrity」门禁**（`fix_book_links.py --check`），任何重新引入的 `](Book/…)` 即 BLOCK → 防模板/手写续命复现。
- **回归已验证**：`fix_book_links --check`（0 残留）、`xref_check` RESULT: **PASS**（2778 内部链接 / 0 断裂 / 0 孤儿 / 0 孤岛）、`crossref_audit` 断链 0、`gen_indexes --check` PASS。
- **提交**：`b9ffeaf`（fix(links)，153 文件 +2609/-2431）。

### 语义级元数据 + legacy 清理 + 全书健康度评估 → ✅ 已提交

- **ch28 元数据自引用（孤例，脚本难抓、靠逐字读原文才发现）**：前置字段原写 `ch31（异常与 UB）、ch28（异常安全）`——把自己列为自己的前置章；"异常安全"实为第 40 章；ch31 实为运算符重载、"异常与 UB"对不上 SUMMARY。修正为 `ch40（异常安全）`、删 ch31 条目。全套前置自引用扫描确认仅此一处。提交 `b6e921b`。
- **legacy 清理**：`_legacy_ModernCppBible/` 在当前 repo 工作树中**根本不存在**（git 无跟踪），zip 快照里的空壳在当前版本已无，无需清理。
- **全书健康度评估（外部 441 样本分层编译 + 全量扫描，结论需记录）**：
  - **内容底子好，不是空壳灌水**：441 个自包含代码块 GCC -std=c++23 编译净结果 **0 处真实编译错误**（12 处失败逐一查因皆假阳性：4 缺第三方头、2 Windows 专属、1 `import std;` 生态、5 是多块拆讲只取一块的脚本误判）。此前两处语义 bug（ch41 shared_from_this 版本限定、ch110 无锁栈 pop ABA 注释）已修且本次重跑未回退。
  - **标注体系是真货**：badge-std/history/comment/exp 四层标注 148 文件全在用，设计完整执行到位。147 章字符数 3w–11.2w（均值 6.3w），最短章集中在"版本历史"等天然短主题，分布合理无糊弄。
  - **验证体系初具雏形**：74/147 章带显式 `[VERIFIED]/[UNVERIFIED]` 标记（65 已验证 / 8 未验证）。**下一步优先审 8 个 UNVERIFIED**：ch02（标准化组织）、ch05（C++14）、ch16（IDE）、ch132（LevelDB/RocksDB）、ch148（Git 工作流）、ch149（CI/CD）、ch150（测试策略）、ch165（进阶路线图）。
  - **待定项**：ch163 网络编程整章仅 Winsock2、无 POSIX socket——若目标读者含 Linux 开发者，需评估补 POSIX 对照版。
- **低优先级外观项**（未处理）：章节标题 `第01章　`（全角空格×103）vs `第 22 章 `（半角×44）不统一。

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
| `tools/handover_check.py` | **接手自检（接手第一步就跑它）**：一条命令核对 git 同步 + 文档数字 vs 事实源 + ruff + quality，并打印接手简报 | ✅ |
| `CONTENT_DEPTH_ROADMAP.md` | **内容深化主线**（五阶：汇编实证矩阵 / 实战项目线 / 陷阱体系 / 人文温度 / 内容形态补全） | ✅ |
| `docs/references/P1_memory_object_model_checklist.md` | 台阶一 P1 内存/对象模型实证结论清单（强模型定结论，弱模型施工图） | ✅ |
| `ISSUES.md` | 遗留清单（2026-08-30 口径） | ✅ |
| `docs/references/content_debt_tasklist.md` | 内容债任务单（已清零，留档） | 需要时 |
| `tools/cppbible.py` | 门禁聚合入口（quality/compile） | ✅ |
| `tools/fix_book_links.py` | 正文跨章链接前缀修复器（`Book/`→源相对，字节级）；`--check` 即 CI「Book Link Integrity」卡口 | ✅ |
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
- **验收看板口径（2026-08-31 修正）**：`tools/metrics_snapshot.py --check` 的 `one_liner/pitfall/analogy` 三项按「达标章数」计（非总出现次数），且支持多写法别名——`pitfall` 含 陷阱/误区/踩坑/反模式，`one_liner` 须带结论后缀（避免误中表头 `| 一句话 |`）。最新值见 `build/metrics.json`（`git status` 不可见，因 `build/` 被 ignore）。
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

_更新时间：2026-09-01 | 覆盖到学习目标→问题驱动论证 25 章收口（历史9+OO6+STL/现代10）+ ch157 断言过强修复_<br/>_上一收口：交叉引用结构性硬伤根治（链接门禁入 CI）+ ch28 元数据修复 + 全书健康度评估落档_
_HEAD：不写死——一律以 `git rev-parse HEAD` 与 `git status -sb` 为准（写死的哈希在提交那一刻即过期）_
_历史：2026-07-17 版（APP15 阶段）已作废；2026-08-30 深夜版停在「P0-2 一半」，其 HEAD 尾注当时已落后一个提交，且 push 状态标反_