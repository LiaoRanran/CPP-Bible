---
id: 498
title: 苦力Agent执行提示词 P0收尾 工件版本绑定 增量replay trace日志 工具完整性
status: active
type: architecture-note
created_at: 2026-09-14
---
# 苦力 Agent 执行提示词 · P0 收尾 + P1 地基批次（498）

> 投喂方式：整份投喂给苦力 Agent。仓库根目录 `C:\CodeLearnling\note\note\C++\CPP-Bible`。
> 开工前必须先 Read 本文档提到的每个文件的磁盘真实内容，禁止凭任务描述假设代码结构。
> 所有数字以实跑为准；若与本文档不符，以实跑为准并在报告中记录偏差。

## 〇、开工基线（2026-09-14，494 收工后实测）

| 项 | 命令 | 基线 |
|---|---|---|
| gate | `python tools/gate_engine.py --check` | 52 规则，BLOCK=0 WARN=32 ADVICE=5 |
| replay | `python tools/atom_evidence_replay.py --check` | confirm=56 refute=0 infra_error=0 |
| poison | `python tools/poison_drill.py` | 65/65，26/52 覆盖 + 27 豁免，攻击面 11/11 |
| pytest | `python -m pytest tests/ -q` | 320 点全绿 |
| git | `git status -sb` | ahead 150 |

收工时这五项必须复跑对比：BLOCK 不得新增、replay 必须 confirm=56、pytest 全绿。
每项任务一个独立 commit。禁止 push、禁止 golden_lock sync/--accept。

### 铁律

1. 改工具前先 Read 磁盘真实源码（文档数字可能过时）。
2. 一条修复一个 commit + 配毒样例（如适用）+ pytest 正反例。
3. 存量零误伤：新规则对存量卡不得新增 block（warn 也要说明原因）。
4. 不编造数据：需要人判断的字段只建机制不填内容。
5. 不删用户文件；临时探针放 `_probe_` 前缀，收工时清理。
6. 不 push、不 golden sync。
7. 遇到需求与磁盘不符，停下来在报告记录，不要硬做。
8. 插入大段代码后立即跑 `python tools/gate_engine.py --check` 验证可加载（494 教训：缩进破坏曾导致加载报错）。

---

## 任务 1 [必做] P0-7 架构文档 frontmatter 批量添加

**现状**：`References/architecture_架构演进/` 下 229 份 .md，0 份有 YAML frontmatter（以实跑数为准）。

**需求**：写脚本 `tools/doc_frontmatter.py`，批量给文档加 frontmatter。

frontmatter 格式：

```
---
id: <编号，纯数字；archive_ 前缀文件用 archive-编号；无编号文件用 slug>
title: <文件名去掉编号前缀和 .md，下划线转空格>
status: active
type: architecture-note
created_at: <文件 mtime 的 YYYY-MM-DD>
---
```

脚本要求：

- 支持 `--dry-run`（默认，只打印将做的改动，不写文件）和 `--apply`（实际写入）。
- 编号提取正则：文件名开头 `^(\d+)`；`archive_312_...` 提取 312，id 写 `archive-312`，status 写 `archived`。
- 无编号文件（如 README_INDEX.md）id 用文件名去扩展名的 slug。
- frontmatter 插入在文件最前面，原有内容一行不动。
- 已经有 frontmatter（首行是 `---`）的文件跳过，不重复添加。
- 幂等：跑第二次 `--apply` 不应产生任何改动。

执行顺序：

1. 写脚本；
2. `--dry-run` 检查输出，抽查 5 份确认 id/title/status/created_at 正确；
3. `--apply` 执行；
4. 跑 `python tools/doc_lint.py`（若存在）确认无新增问题；
5. 确认全部文档处理完成，archive_ 前缀的 status=archived。

验收：

- 所有非 archive 文档首行是 `---`，frontmatter 有 5 个字段；
- 幂等：再跑 `--apply` 改动 0 文件；
- 文件原有内容完整（每份只多 7 行 frontmatter）；
- pytest 全绿。

commit：`feat(docs): 架构文档批量添加 frontmatter（P0-7）+ doc_frontmatter.py 工具`

---

## 任务 2 [必做] P0-3 工件-卡版本绑定

**现状**：`Examples/atoms/` 下 51 个 .asm（Intel 语法，注释符 `;`，已实测含 `.intel_syntax noprefix`），
`evidence/` 下 56 张 EV-*.md，0 张卡有 artifact_version 字段。
.asm 是被 git 跟踪的冻结产物，replay 在临时目录重编译做不变量校验。

**目标**：卡和工件的版本号必须匹配，夹具改了但版本没递增则 gate block。

**严格按以下顺序执行（顺序错了 replay 会全红）**：

### 2.1 给 51 个 .asm 加头部版本注释

在每个 .asm 文件最前面（第一行之前）插入一行：

```
; artifact_version: 1
```

- Intel 语法 asm 注释符是 `;`；
- 只加这一行，不动其他任何内容；
- 用脚本批量做，不要手改 51 个文件。

### 2.2 重算所有 .asm 的 sha256 并同步卡

加注释后文件 hash 全变。写脚本：

1. 扫描每张证据卡的 `artifact:` 字段，拿到 .asm 路径；
2. 计算当前 .asm 的 sha256；
3. 更新卡的 `artifact_sha256:` 字段为新 hash；
4. 同时在卡 frontmatter 加 `artifact_version: 1`；
5. 多 TU 卡（EV-LANG-001/002 都锚定 `_atom_inline_odr_a.asm`）只处理锚定的那一个；
6. 没有 artifact 字段的卡（纯 run_match 形态）跳过并记录。

### 2.3 加 gate 规则 EV-ARTIFACT-VERSION-MATCH

先 Read `tools/gate_engine.py` 找到证据卡规则注册位置和现有 artifact 规则（如 EV-ARTIFACT-PRODUCER），照抄结构：

- 卡有 artifact 字段时：
  - 读卡的 artifact_version（缺字段 -> warn，迁移期不 block）；
  - 读 artifact 指向的 .asm 第一行 `; artifact_version: N`（缺注释 -> warn）；
  - 两者都存在但不相等 -> block；
- 存量卡步骤 2.2 已全部补 version=1，所以存量应 0 block 0 warn。

### 2.4 毒样例 + pytest

- 阳性：卡 version=2 但 asm 注释 version=1 -> 必须 block；
- 阴性：卡 version=1 且 asm version=1 -> 放行；
- warn：卡有 artifact 但缺 version 字段 -> warn；
- pytest 照 `tests/test_gate_engine.py` 现有模式加至少 3 个。

### 2.5 全量验证

- `python tools/atom_evidence_replay.py --check` 必须 confirm=56（sha 已同步）；
- gate BLOCK=0；
- 若 replay 有 refute，说明 sha 没同步对，逐个修，不要跳过。

验收：51 个 asm 头部有版本注释；有 artifact 字段的卡有 artifact_version=1 和新 sha256；
replay confirm=56；gate 0 block；毒样例阳性 block、阴性放行。

commit：`feat(gate): 工件-卡版本绑定 EV-ARTIFACT-VERSION-MATCH + 存量迁移（P0-3）`

---

## 任务 3 [必做] P1-10 核心工具完整性校验

**需求**：防止核心工具被静默篡改（供应链安全基础）。

新建 `tools/tool_integrity.py`：

1. 核心工具清单（5 个）：gate_engine.py、atom_evidence_replay.py、poison_drill.py、toolchain.py、cppbible.py；
2. `--update`：计算 5 个工具的 sha256，写入 `tools/.tool_checksums`（每行 `<sha256>  <filename>`）；
3. 默认运行（无参数）：读 .tool_checksums，重新计算当前 sha 逐行比对：
   - 全匹配 -> 输出 OK，exit 0；
   - 不匹配 -> 输出哪个文件被改、期望 hash、实际 hash，exit 1；
   - .tool_checksums 缺失 -> exit 2 并提示先 --update；
4. .tool_checksums 自身不纳入校验；
5. 注册进 `tools/cppbible.py` 的质量检查（先 Read cppbible.py 找到 cmd_check 或质量步骤注册位置照抄）；
6. pytest 至少 3 个（匹配通过 / 篡改检出 / 缺失文件），用 tmp_path 不写真实 tools/。

**顺序依赖**：任务 2 会改 gate_engine.py。必须在任务 2 commit 之后再跑 `--update` 生成基准。

验收：

- `tool_integrity.py --update` 生成 .tool_checksums；
- 默认运行 exit 0；
- 手工临时给一个工具加空格 -> exit 1 检出 -> 还原；
- pytest 全绿。

commit：`feat(tools): 核心工具完整性校验 tool_integrity.py + checksums 基准（P1-10）`

---

## 任务 4 [必做] P1-12 trace_logger 结构化操作日志

**需求**：所有 Agent 操作/编译/门禁/人审留痕，为后续诊断引擎（P2-2）和健康看板（P2-6）提供数据源。

新建 `tools/trace_logger.py`：

- 日志目录 `data/traces/`（不存在自动创建；先 Read `.gitignore` 确认 data/ 是否已忽略，没有则加）；
- 日志文件按日期：`data/traces/trace-YYYY-MM-DD.jsonl`，每行一个 JSON 事件。

命令行用法：

```
python tools/trace_logger.py log --actor <actor> --action <action> --target <target> --result <result> [--details '<json字符串>']
```

- 自动补充字段：timestamp（ISO8601 本地时间）、seq（当日递增序号）、pid；
- actor 枚举：writer、redteam、gatekeeper、human、coolie、architect；
- action 枚举：fixture_create、compile、replay、gate_check、poison_drill、redteam_review、human_sign、commit、tool_modify、other；
- result 枚举：pass、fail、warn、skip、info；
- details 是合法 JSON 字符串，解析失败报错不静默；
- 提供可 import 的 API：`log_event(actor, action, target, result, details: dict | None = None)`；
- read 子命令：`python tools/trace_logger.py read [--date YYYY-MM-DD] [--action xxx] [--fail-only]`，输出 JSONL；
- pytest 至少 4 个（log 写入格式正确 / seq 递增 / read 过滤 / 非法 details 报错），用 tmp_path 或 monkeypatch 日志目录；
- 注册进 cppbible.py。

验收：手工 log 3 条不同事件，jsonl 每行是合法 JSON、字段齐全、seq 递增；
read --fail-only 只输出 result=fail；pytest 全绿；data/ 在 .gitignore。

commit：`feat(tools): trace_logger 结构化操作日志（P1-12）`

---

## 任务 5 [选做，能力足够再做] P0-1 增量 replay

**现状**：`atom_evidence_replay.py` 的 `find_cards()`（约 :1428）扫描 `evidence/**/EV-*.md`，
`main()`（约 :1432）用 argparse，约 :1455 `for card in cards` 逐张 replay_card()。全量约 5 分钟。
`build/` 目录存在且已在 .gitignore。

**需求**：加 `--incremental` 参数，只重跑"自上次成功 replay 后发生变化"的卡。

设计：

1. 清单文件 `build/replay_manifest.json`，结构：
   `{"<卡相对路径>": {"fingerprint": "<sha256>", "verdict": "confirm", "ts": "ISO时间"}}`
2. 指纹计算（一张卡的 fingerprint）：sha256 拼接三部分内容：
   - 卡文件自身内容；
   - 卡 frontmatter 中 fixture 字段指向的 .cpp 文件内容；
   - 卡 artifact 字段指向的 .asm 文件内容（若有）。
   任一字段指向的文件不存在 -> 指纹标记为 `MISSING`（强制重跑）。
3. `--incremental` 逻辑（在 main() 选卡阶段，不改 replay_card() 内部）：
   - manifest 不存在 -> 全量跑；
   - manifest 存在 -> 逐卡算指纹：
     - manifest 无记录（新卡）-> 跑；
     - 指纹变了（卡/夹具/工件任一改动）-> 跑；
     - 指纹相同且上次 verdict=confirm -> skip（打印 `SKIP <卡>`）；
     - 指纹相同但上次非 confirm -> 跑（失败卡每次重试）；
   - 被删的卡（manifest 有记录但文件没了）-> 从 manifest 移除。
4. 无论是否 --incremental，跑完（--check 模式结束时）都更新 manifest：记录本次跑的卡指纹+verdict；skip 的卡保留原记录。
5. 加 `--rebuild-manifest`：忽略现有 manifest，全量跑并重建。
6. 输出汇总行：`X run / Y skip / Z refute`。

pytest（把选卡+指纹逻辑写成可单测的纯函数，用 tmp_path 构造假卡，monkeypatch EVIDENCE/ROOT）：

- 无 manifest -> 所有卡入选；
- 指纹未变 + confirm -> skip；
- 改 fixture 文件 -> 该卡入选；
- 新卡 -> 入选；
- 上次 refute -> 入选（即使指纹没变）。

至少 4 个测试。

注意：

- 不要动 replay_card() 的校验逻辑，只在 main() 选卡环节加过滤；
- 全局锁 _acquire_replay_lock 保持不变；
- 实测增量效果：先全量一次建 manifest，再 --incremental（应全 skip、秒级），
  touch 一张卡的 fixture 再 --incremental（应只跑 1 张）。把三个耗时写进报告。

commit：`feat(replay): 增量 replay --incremental/--rebuild-manifest（P0-1）`

---

## 任务 6 [选做] P1-8 预注册模板

新建 `docs/kernel/preregistration_template.md`，字段：

- 实验标题 / 日期 / 执行者；
- 假设 hypothesis（一句可证伪的陈述）；
- 预测结果 predicted_result（实验前写死的具体观测值/方向）；
- 零假设 null_hypothesis；
- 实验方案（fixture 结构、编译器、优化档、平台）；
- 判定指标 metrics（具体到 grep 什么标签、断言什么数值）；
- 证伪标准 falsification_criteria（看到什么结果就承认假设错）；
- 冻结见证 witness_commit（实验前单独 commit 的 hash，git 时间戳为证）。

在 `docs/kernel/writer_production_flow.md`（479 已建）合适位置加一段引用本模板，
说明"性能/对照类实验实验前必须填预注册，红队事后 diff 冻结 commit 与最终卡"。
纯文档，不改代码。

commit：`docs(kernel): 实验预注册模板（P1-8）`

---

## 任务 7 [选做] 历史临时件清理

仓库根目录有约 12 个历史临时探针文件（`_po.txt`、`_po3.txt`、`_po3e.txt`、`_po_err.txt`、
`_pt.err`、`_pt.log`、`_rp.txt`、`_rp2.txt`、`_rp2e.txt`、`_rp3.err`、`_rp_err.txt` 等，
以实测 `git status --porcelain` 的 ?? 名单为准）。

1. 逐个确认是未跟踪文件（??）；
2. 确认不是 `_worklog_*.md`、`_adv_*/`、正式目录文件；
3. 删除。

本任务无 commit（删未跟踪文件），报告列出删除清单。

---

## 收工要求

1. 顺序：任务 1 -> 2 -> 3 -> 4（必做），有余力做 5 -> 6 -> 7。
2. 任务 2 和任务 3 有顺序依赖：任务 2 改 gate_engine.py 并 commit 后，任务 3 才生成 checksums 基准。
3. 每个任务完成后立即跑相关门禁，不要攒到最后。
4. 全部完成后复跑开工基线五项，做前后对比表（规则数 / poison 数 / pytest 数 / replay confirm 数）。
5. 在 `_worklog_498.md` 写交接：每项 commit hash、实测结果、与本文档不符之处、未完成项及原因、
   任务 5 的增量耗时实测（全量 / 全 skip / 单卡）。
6. 不 push、不 golden sync、不删 `_adv_*/` 和 `_worklog_*.md`。
7. 请求数 >450 时用 `tools/task_state.py`（494 已建）记录进度并输出续跑提示词后停手。

## 参考文档（需要时 Read，不要全读）

- `References/architecture_架构演进/490_*知识冲突与版本管理*`（任务 2 设计来源，第三节）
- `References/architecture_架构演进/487_*性能优化与队列设计*`（任务 5 设计来源）
- `References/architecture_架构演进/497_可观测性与失败恢复*`（任务 4 设计来源，原 485/486）
- `References/architecture_架构演进/488_*安全性与信任模型*`（任务 3 来源）
- `References/architecture_架构演进/491_*人的因素*`（任务 6 来源）
- `tools/atom_evidence_replay.py`（任务 5 改这里，先 Read find_cards/main 约 :1428-1470）
- `tools/gate_engine.py`（任务 2 加规则，先 Read 现有 EV-ARTIFACT-* 规则结构）
