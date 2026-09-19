# _worklog_498 · P0 收尾 + P1 地基批次执行记录（2026-09-14）

> 零上下文接手标准：每项含 ①当前状态 ②未完成原因 ③下一步精确命令。
> 纪律：不 push、不 golden sync、逐任务独立 commit、存量零误伤、数字全部实跑。

## 0. 开工基线 → 收工终值（全部实跑）

| 项 | 开工基线 | 收工终值 | 判读 |
|---|---|---|---|
| gate | 52 规则 · BLOCK=0 WARN=32 ADVICE=5 | **53 规则**（+`EV-ARTIFACT-VERSION-MATCH`）· BLOCK=0 WARN=32 ADVICE=5 | 存量零误伤 |
| replay | confirm=56 | **confirm=56**（全量 245.0s / 增量 0.3s / 单卡 2.3s） | 未降；新增增量能力 |
| poison | 65/65 · 26/52 覆盖 | **68/68 · 27/53 覆盖**+27 豁免 · 攻击面 11/11 | +P60 三态 |
| pytest | 320 点 | **354 点**（+34）| 全绿 |
| git | ahead 150 | **ahead 157**（+7 提交） | 均未 push |

## 1. 任务完成状态（7/7）

| # | 任务 | 状态 | commit | 关键实测 |
|---|---|---|---|---|
| 1 | P0-7 架构文档 frontmatter | ✅ | `e5d51d7` | 230 份加 5 字段；**幂等 0 改动**；206 tracked 文件 each +7 行 |
| 2 | P0-3 工件-卡版本绑定 | ✅ 两轮修正 | `d3b2cb7` + `0ce5301` | 56 卡加字段 + 版本台账（**工件字节不可改**）；规则 52→53；毒 P60 三态 |
| 3 | P1-10 核心工具完整性 | ✅ | `80b88ab` | 基准 5 文件；篡改检出 exit 1 → 还原 exit 0 |
| 4 | P1-12 trace_logger | ✅ | `551afa7` | 3 事件 seq 1/2/3；read --fail-only 正确 |
| 5 | P0-1 增量 replay（选做） | ✅ | `e23a0b1` | **245.0s → 0.3s → 2.3s**（三档实测） |
| 6 | P1-8 预注册模板（选做） | ✅ | `5474166` | 8 字段模板 + Writer 流程 §3.1 |
| 7 | 历史临时件清理（选做） | ✅ | （无 commit） | 删 **17 件**（11 历史 + 6 本会话中间产物），REMAIN=0 |

## 2. 关键任务要点

### 任务 1：frontmatter（230 份）
- `tools/doc_frontmatter.py`：5 字段（id/title/status/type/created_at）；默认 dry-run，`--apply` 才写。
- **字节级插入**（沿用原文件行尾）——走 `read_text/write_text` 会把 CRLF 归一成 LF、改写整文件（494 同款教训）。
- **抽查修正**：`archive_365B_…` 首版正则只取数字 ⇒ id 应为 `archive-365B`（字母后缀属编号），
  否则 title 会混入 "B"（已修 + 加回归锁）。
- 验收：230/230 首行 `---`；**第二次 --apply 改动 0**；gate/doc_lint 无新增。

### 任务 2：工件-卡版本绑定（**两轮迭代：首版改工件字节失败 → 修正为旁路台账**）
- **提示词 2.1/2.2 不可执行（实测硬证据）**：提示词要求"给 51 个 .asm 加头部注释 + 重算 sha256 同步卡"。
  实测发现工件字节被**两处硬契约**同时锁死：
  ① **replay** 的 artifact 校验 =「删旧工件 → 重跑生成命令 → 比卡值 sha256」⇒ 手工注释**不在重生成产物里**；
  ② **writer_selfcheck `WC-01`** = 「**磁盘工件** sha256 == 卡值」。
  - 首版（`d3b2cb7`）照提示词做了 2.1（51 asm 插注释）：replay 仍 confirm（注释被重生成覆盖），
    但 **WC-01 全库 fail（实测 56/56）**；
  - 反向按 2.2 同步卡值 ⇒ **replay 全库 `refute:sha256_mismatch`**（EV-CONC-001 期望 `3d6f55e6…`
    vs 实际 `8dd19bc6…`，实测）；
  - ⇒ 两条契约同时成立意味着 **工件字节不可改**（改任一方向都会打破另一处的字节等式）。
- **修正（`0ce5301`）**：版本号改走**旁路台账** `Examples/atoms/artifact_versions.json`（51 条）——
  ① **还原 51 个 .asm**（`git diff d3b2cb7^..HEAD -- Examples/atoms` 只剩新增台账，字节彻底回滚）；
  ② `EV-ARTIFACT-VERSION-MATCH` 改读台账，三态不变（缺卡字段 warn / 台账未登记 warn / 不一致 **block**）；
  ③ 毒样例 P60 与 pytest（7 例，含"台账损坏按未登记处理"）改台账版；
  ④ 卡字段 `artifact_version: 1`（56 张）**保留**（这一半是有效的）。
- 验证：gate BLOCK=0 WARN=32 ADVICE=5 且新规则存量命中 **0**；poison **68/68**（P60 三态）；
  `writer_selfcheck` 56 卡 **fail=0**（还原后恢复）；单卡 replay **confirm**；台账生成幂等（第二次 0 新增/51 保留）。
- **踩坑（首版遗留，已修）**：卡侧幂等检查只看前 2000 字节 ⇒ 7 张长 frontmatter 卡被重复插入字段
  （会触发 `EV-FM-DUP-KEY` block）→ 改按 frontmatter 段检查 + 新增 `--dedupe` 清理（已清 7 份）。
- 其它 asm 门禁实测不受影响：`verify_asm_evidence`（MISSING_FILE=0）、`book_asm_freshness`（0 真过期）。

### 任务 3：工具完整性
- `--update` 建 `tools/.tool_checksums`（5 个核心工具）；默认比对——全匹配 0 / 被改 1 / 缺基准 2。
- **顺序依赖已遵守**：基准在任务 2 commit **之后**生成；任务 5 改了 replay ⇒ 基准**同步更新**（含在 `e23a0b1`）。
- 篡改实测：给 `poison_drill.py` 尾部加一个空格 ⇒ exit 1 且打印期望/实际 hash ⇒ 还原后 exit 0。

### 任务 4：trace_logger
- `data/traces/trace-YYYY-MM-DD.jsonl`；字段 timestamp/seq/pid/actor/action/target/result/details；
  枚举校验（6 actor / 10 action / 5 result）——枚举外报错不静默；`--details` 非法 ⇒ exit 2 且不落盘。
- `.gitignore` 加 `/data/traces/`（与 `/data/tasks/` 同口径）。

### 任务 5：增量 replay（**三档实测**）
| 档 | 场景 | 耗时 | 结果 |
|---|---|---|---|
| ① | 全量 `--rebuild-manifest` | **245.0s** | confirm=56，清单 56 条 |
| ② | `--incremental` 无改动 | **0.3s** | 56 张全部命中缓存（未跑任何编译） |
| ③ | 改 1 个独占夹具后 `--incremental` | **2.3s** | **1 run / 55 skip**（如预期只跑 1 张） |

⇒ 达成 476 第一波的「日常 replay <30s」目标（提速 100×+）。夹具已还原。
- 设计：指纹 = sha256(卡 ‖ fixture ‖ artifact)；五条选卡规则；MISSING ⇒ 强制重跑；
  清单损坏 ⇒ 全量跑（宁可多跑不可漏跑）；单卡模式不维护清单（避免收窄）。

## 3. 与提示词不符之处（以实跑为准）

1. **任务 2.1/2.2 整体不可执行**（详见 §2 任务 2）：改工件字节撞 `WC-01`（实测 56/56 fail）、
   同步 sha 撞 replay（实测 `refute:sha256_mismatch`）⇒ 首版按提示词做的一切已**全部回滚**，
   改用旁路台账（`0ce5301`）。这是本批最重要的偏差，两个方向都有实测证据。
2. **任务 1 的文档数**：提示词说 229 份 ⇒ 实测 **230 份**（含 494 新增的 497）。
3. **任务 5 的 manifest 更新时机**：提示词说"跑完都更新"⇒ 已实现，但**单卡模式（--card）不更新**（防收窄），
   这是对提示词的合理收窄，已在 docstring 注明。
4. **任务 6 的字段名**：提示词给的 8 项与 491 原表一致 ✅（无偏差）。

## 4. 收工五项复跑

| 项 | 命令 | 结果 |
|---|---|---|
| gate | `tools/gate_engine.py --check` | 规则 **53** · **BLOCK=0 WARN=32 ADVICE=5** |
| replay | 全量（任务 5 实测）+ 增量验证 | **confirm=56**；增量 0.3s 全 skip |
| poison | `tools/poison_drill.py --write-surface-map` | **68/68** · RULE-COVERAGE **27/53**+豁免 27 |
| pytest | `-m pytest tests -q` | **354 点全绿** |
| git | `git status -sb` | ahead **156**，工作树仅 untracked（文档/沙箱/worklog/临时件） |
| tool_integrity | `tools/tool_integrity.py` | exit **0**（5 工具与基准一致） |

## 5. 未完成项与原因

1. ~~任务 7（临时件清理）未完成~~ → **已完成**：删除 **17 件**（11 个历史件 `_po*.txt`/`_rp*.txt`/`_pt.*`
   等 + 6 个本会话中间产物 `_stamp*.txt`/`_fm_dry.txt`/`_dedupe.txt`/`_t.*`），`REMAIN=0`。
   仍属运行时产物、可在收工后一并删除（不影响仓库）：
   ```powershell
   cd C:\CodeLearnling\note\note\C++\CPP-Bible
   Remove-Item _timeit.py,_inc1*,_inc2*,_inc3*,_po498*,_po498b*,_pt498*,_rp498* -Force -ErrorAction SilentlyContinue
   ```
2. **`_probe_ch132_blk*.cpp/.exe`（6 件）**：非本批产物，按"不删用户文件"继续保留（494 已记录）。

## 6. 提交清单（498，**均未 push**）

| commit | 内容 |
|---|---|
| `e5d51d7` | feat(docs): 架构文档批量添加 frontmatter（P0-7）+ doc_frontmatter.py |
| `d3b2cb7` | feat(gate): 工件-卡版本绑定 EV-ARTIFACT-VERSION-MATCH + 存量迁移（P0-3，首版走工件注释） |
| `0ce5301` | fix(gate): 版本绑定改用旁路台账（工件字节受两处硬契约约束，不可改）——**修正 `d3b2cb7`** |
| `80b88ab` | feat(tools): 核心工具完整性校验 tool_integrity.py + checksums 基准（P1-10） |
| `551afa7` | feat(tools): trace_logger 结构化操作日志（P1-12） |
| `e23a0b1` | feat(replay): 增量 replay --incremental/--rebuild-manifest（P0-1） |
| `5474166` | docs(kernel): 实验预注册模板（P1-8） |

**合计 7 提交**（任务 7 无 commit；含任务 2 的修正提交 `0ce5301`）。本地 ahead **157**。
注：任务 4 的 `cppbible` trace 子命令注册因同文件编辑，随 `80b88ab` 一并入库（如实记录，未回改历史）。

## 7. 关键教训（供后续批次）

1. **冻结工件（`.asm`）的字节同时受两处等式约束，不可改**：改字节 → `WC-01`（**磁盘** sha == 卡值）
   全库 fail；同步卡值 → replay（**重生成** sha == 卡值）全库 refute。**版本/元数据类需求一律走
   旁路载体（台账 / 卡字段），绝不改工件字节**。通用判据：动手改任何"被 hash 引用的文件"前，
   先问「这份字节被哪些等式引用？」——本轮就是漏问这一步才返工（两处等式方向相反，必须先扫全）。
2. **幂等检查必须覆盖完整作用域**：`raw[:2000]` 这类"取样检查"对大 frontmatter 会漏（本轮 7 张卡中招）。
3. **并发窗口会制造假信号**：replay 运行期工件处于"删除→重生成→还原"中间态，此时并行跑 gate
   会对工件类规则读出瞬时误报 —— 工件缺失应交给 replay 判，gate 侧跳过。
4. **`Start-Process` 传多参数给 python 脚本不可靠**（本轮 wrapper 静默失败两次）；计时改用
   "时间戳文件 + 产物内时间字段"（如 manifest 的 ts）。

## 8. 实测数字（终态）
- 开工 pytest **320 点**；收工 **354 点**（+34：doc_frontmatter 7 / artifact_version 7 /
  tool_integrity 5 / trace_logger 7 / incremental_replay 8），全绿。
- 数字纪律：本文件所有计数来自实跑输出（终态 pytest 5 行进度点 72+72+72+72+66=354）。
