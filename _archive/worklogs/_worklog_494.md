# _worklog_494 · P0 地基批次执行记录（2026-09-14）

> 零上下文接手标准：每项含 ①当前状态 ②未完成原因 ③下一步精确命令。
> 纪律：不 push、不 golden sync、逐任务独立 commit、存量零误伤、数字全部实跑。

## 0. 开工基线 → 收工终值（全部实跑）

| 项 | 开工基线 | 收工终值 | 判读 |
|---|---|---|---|
| gate | 51 规则 · BLOCK=0 WARN=32 ADVICE=5 | **52 规则**（+`ATOM-VERIFY-REASON`）· BLOCK=0 WARN=32 ADVICE=5 | 新增规则走存量豁免，零净增量 |
| replay | confirm=56 refute=0 infra_error=0 | **confirm=56 refute=0 infra_error=0** | 原子改动（任务 1）后复跑不变 |
| poison | 63/63 · 25/51 覆盖+27 豁免 | **65/65 · 26/52 覆盖+27 豁免** | +P59 配对；新规则被覆盖 |
| pytest | 302 点 | **320 点**（+18：verify_reason 8 / task_state 7 / adversarial 3）| 全绿 |
| git | ahead 143（工作树无 modified） | **ahead 150**（+7 提交） | 均未 push |

## 1. 任务完成状态（8/8）

| # | 任务 | 状态 | commit | 关键实测 |
|---|---|---|---|---|
| 1 | 原子 status 行尾注释清理 | ✅ | `6dd44e1` | 20 颗改；`^status:.*#` 0 命中；每文件恰 -1/+1 行 |
| 2 | 架构文档编号冲突修复 | ✅ | `54cd8fd` | 7 组冲突 → 0 组；5 个 git mv + 2 个 Rename |
| 3 | 模型能力档案 | ✅ | `63ea744` | yaml 可解析（4 模型）；success_rate 全 unknown |
| 4 | 认知偏差检查清单 | ✅ | `a07fe4b` | 8 条齐全（表现+自问）|
| 5 | ATOM-VERIFY-REASON gate 规则 | ✅ | `4ddd6a8` | 23 颗存量豁免；规则数 51→52；WARN 不变 |
| 6 | 对抗回归测试工具（选做） | ✅ | `d3fdec1` | **escape=0 · gap=0 · blocked=25**；visible=2；skip=35 |
| 7 | 任务状态文件工具（选做） | ✅ | `35532c9` | 4 子命令冒烟通过；pytest 7 例 |
| 8 | 479 临时件清理（选做） | ✅ | （无 commit） | 删 **28 件**；worklog/`_adv_*` 保留 |

## 2. 各任务要点

### 任务 1：status 注释清理（20 颗，非提示词所说的 22）
- **信息零丢失的逐颗核对**：两处含日期的注释（`ATOM-MEM-PERF-003` 2026-09-12、`ATOM-MEM-RVREF-001` 2026-09-11）
  与各自 `status_history` 中 human-verified 条目的 `at` **完全一致** ⇒ 直接删注释，无需改 status_history。
- **行尾安全（关键实现）**：二进制 `read_bytes/write_bytes` + 字节级正则。若走 `read_text/write_text`，
  Python 的 universal-newlines 会把 CRLF 归一成 LF ⇒ 整文件行尾被改写（diff 变整文件）。实测每文件 `-1/+1` 行。
- red-team-verified(3) 与 draft(1) 未动（27 = 23 verified + 3 red-team + 1 draft）。

### 任务 2：编号冲突（7 组）
- 实测分组（`^(\d+)`）：312/365/369/410/415/484/485 各 2 个，与提示词一致。
- **改名**：410→494、415→495、484→496、485→497、312_backup→archive_312_backup、365B→archive_365B、369-old→archive_369。
- **5 个 tracked 走 `git mv`（100% rename 保留历史）**；**484/485 实测未入库（untracked）**，
  只能用 `Rename-Item`（**无 git 历史可保留**——与提示词的 git mv 要求不符，原因见 §3）。
- 引用同步：`README_INDEX.md` 两处（365B / 369-old 行 → archive_ 名 + 标注已归档）；根 `INDEX.md`/`README.md` 实测无引用；
  历史提示词（401/403/410）中"当年备份命令"的旧路径**不改**（历史事实），且 archive_ 前缀保留原串 ⇒ grep 旧名仍可命中。
- 验收：`^(\d+)` 分组重名 **0 组**。

### 任务 3：model_marketplace.yaml
- 4 模型（cheap/strong/adversarial/architect）+ 字段按 492 §2.1；**success_rate 一律 unknown**
  （492 示例里的 0.85/0.60/0.15 是**示意值**，按铁律 4 禁止照抄；真实值待 492 §7 第二阶段"能力回溯"回填）。
- known_blind_spots 只收录有留痕依据的观察（relations 盲区 / 可见化≠拦住 / 文档数字漂移）。
- 验收：`yaml.safe_load` 解析通过（4 模型，三级 success_rate 全 unknown）。

### 任务 4：cognitive_bias_checklist.md
- 491 §七 8 条逐条落地，每条含「本项目典型表现（带事故实例）+ 决策前自问」；附与既有机制的接口表 + 3 问快速版。

### 任务 5：ATOM-VERIFY-REASON
- 判据：`status ∈ {verified, human-verified}` 且 `verified_reason` 空 ⇒ **warn**。
- 存量豁免 `tools/verify_reason_exempt.txt`（**23 颗**逐个列出，名单即迁移积压：补一颗删一行；新卡不豁免）。
- 级别 warn 的理由：①存量 23 颗全缺（block 会恒红）；②**理由内容需人判断**——铁律 4：苦力只建机制不填内容，
  规则不得逼人编造理由（470 P0-D 同款纪律）。
- 验证：gate RULES 51→52、BLOCK=0 WARN=32 不变、规则存量命中 0；毒样例 P59（名单外无 reason ⇒ 命中且 warn）
  + P59-阴（有 reason ⇒ 放行）；pytest 8 例；手工探针三态（名单外/名单内/有 reason）验证通过。

### 任务 6：adversarial_regression.py（选做，已做）
- **双轨判定（实测逼出来的设计）**：机器 verdict 优先（`refute*`/`infra_error*` ⇒ blocked、`confirm` ⇒ escape、
  `warn`/`advice` ⇒ visible 可见化层），自述兜底。
- 为什么必须双轨：首跑（只信自述）报 **escape=5**，逐条核对后：**3 条实际已拦**（E01×2、E03 的 verdict 已是
  `refute:artifact_tampered`/`artifact_assert_failed` —— 探针文本写于修复前，口径陈旧）、**2 条是有意 warn/advice**
  （E04/E06，414 F04/F06 设计选择）。双轨后 **escape=0**。
- 回归锁映射 21 个标签 → `tests/*.py`（锁文件缺失即记 escape）；`gap` 定义 = 有判定但无锁映射。
  **本工具自身就抓到两处 gap**（`P0-A 构建脚本边界`、`E03 恒真符号` 无锁映射）→ 已补 `test_recompile_invariant.py` /
  `test_discriminative.py`，gap 归零。
- 诚实边界（写进 docstring）：探针自述型判定如实转述（标 `source`）；无法自动化的一律 skip 且 **skip ≠ pass**；
  历史轮次默认 skip（口径漂移）。CI/新克隆无 `_adv_*/` ⇒ 自动空转 exit 0。
- 注册：cppbible quality 元组 + `pyproject.toml` 双清单（`--manifest-check` 0 命中）。

### 任务 7：task_state.py
- 4 子命令（create/update/continue-prompt/show）；状态字段逐字对齐 492 §4.2；状态机
  `pending → in_progress → needs_continue(>450) → done`；`update` 自动把上一步摘要归档进 `steps_completed`。
- `data/tasks/` 已加 `.gitignore`（运行时状态不入库）；注册为 cppbible `task` 子命令；pytest 7 例（全走 tmp_path）。

### 任务 8：临时件清理
- 删除 28 件：479 遗留（`_timeit.py`、`_rp479*` 11、`_pt479*` 6、`_po479.*` 2）+ 494 探针/日志（`_probe_status.py`、
  `_probe_fix_status.py`、`_probe_verify_reason.py`、`_po494.*`、`_pt494.*`）。
- 保留：`_worklog_*.md`（4 份）、`_adv_v61/v70/v80/`（对抗证据）、`_rp494.*`（终态 replay 输出，收工后才可删）。
- **未删**：`_probe_ch132_blk*.cpp/.exe`（非本批产物，属旧会话，按"不删用户文件"保留 → 交用户裁决）。

## 3. 与提示词不符之处（以实跑为准，逐条记录）

1. **原子数与注释数**：提示词"28 颗原子 / 22 颗带 status 注释 / 24 颗 verified" ⇒ 实测 **27 颗 / 20 颗 / 23 颗**
   （另 3 颗 red-team-verified、1 颗 draft）。
2. **doc_lint 没有编号检查功能**（提示词称"doc_lint 的 `^(\d+)` 正则都会判重"）⇒ 改用 PowerShell 分组实测
   （结果一致：7 组）。
3. **484/485 未入库** ⇒ 无法 `git mv`（提示词要求 git mv 保留历史），只能用 `Rename-Item`；
   496/497 改名后仍是 untracked（不入库），**不产生 git 历史的丢失**（因为它们本来就没有历史）。
4. **未跟踪文档不止 2 个**：提示词说"工作树有 2 个未跟踪 .md（471/473）" ⇒ 实测 471/473/474/475/476/477/478
   等 8+ 个（均非本批，未动）。
5. **492 §2.1 的 success_rate 具体数字**未照录（铁律 4：不编造），一律 `unknown`。
6. **任务 6 的探针自述口径已漂移**（5 条自述与实际 verdict 不符）⇒ 引入双轨判定（§2 任务 6）。
7. **ccache 说明**：479 已接入（热缓存 244.5s），本批 replay 复跑沿用；本批未改 replay 逻辑。

## 4. 未完成项与原因

1. **任务 6 的 skip=35 项**：说明型探针（`probes/*.md`）、历史轮次（v61/v70）、无可解析输出（`probe_misc.py`）
   —— 无法自动断言，按提示词"不要硬写"如实记 skip（不假装通过）。
2. **`_probe_ch132_blk*`（6 件）**未删（非本批产物）→ 待用户裁决。
3. 任务 5 的 **verified_reason 内容**未填（铁律 4：需人判断）——机制与豁免表已就位，理由由人签署时补。

## 5. 提交清单（494，**均未 push**）

| commit | 内容 |
|---|---|
| `6dd44e1` | style(atom): status 行尾注释清理（20 颗） |
| `63ea744` | docs(kernel): 模型能力档案 model_marketplace.yaml |
| `a07fe4b` | docs(kernel): 认知偏差检查清单 |
| `54cd8fd` | fix(docs): 架构文档编号冲突 7 组 + 归档 |
| `4ddd6a8` | feat(gate): ATOM-VERIFY-REASON + 豁免 + 毒样例 + pytest |
| `35532c9` | feat(tools): task_state.py（断点续跑） |
| `d3fdec1` | feat(tools): adversarial_regression.py（对抗回归） |

**合计 7 提交**（任务 8 无 commit：删除的是未跟踪文件）。本地 ahead **150**。

## 6. 临时件（收工后仍需清理）
```
Remove-Item _rp494.log,_rp494.err,_po494.log,_po494.err,_pt494*.log,_pt494*.err,_adv494*.log,_adv494*.err,_adv494b*, _pt494final*
```
（`*.log` 被 .gitignore 覆盖；删除需越界批准，本环境未执行）

## 7. 收工五项复跑（2026-09-14 终态）

| 项 | 命令 | 结果 |
|---|---|---|
| gate | `tools/gate_engine.py --check` | 规则 **52** · **BLOCK=0 WARN=32 ADVICE=5** |
| replay | `tools/atom_evidence_replay.py --check` | **confirm=56 refute=0 infra_error=0** |
| poison | `tools/poison_drill.py --write-surface-map` | **65/65** · RULE-COVERAGE **26/52**+豁免 27 |
| pytest | `-m pytest tests -q` | **320 点全绿** |
| git | `git status -sb` | ahead **150**，工作树仅 untracked（文档/沙箱/worklog） |

**收工校验（提示词红线）**：BLOCK 未新增 ✅ · replay 未降（56→56）✅ · pytest 全绿 ✅。

## 8. 每条修复的验证方式（可复现）
```powershell
# 任务 1：0 命中
(Select-String -Path "atoms\*\*.md" -Pattern "^status:.*#").Count            # => 0
# 任务 2：0 冲突
$d="References\architecture_架构演进"; (Get-ChildItem $d -Filter "*.md" | ForEach-Object { $m=[regex]::Match($_.Name,'^(\d+)'); if($m.Success){$m.Groups[1].Value} } | Group-Object | Where-Object Count -gt 1 | Measure-Object).Count   # => 0
# 任务 3：yaml 可解析
.\.venv\Scripts\python.exe -c "import yaml;d=yaml.safe_load(open('docs/kernel/model_marketplace.yaml',encoding='utf-8'));print(len(d['models']))"   # => 4
# 任务 5：豁免生效
Select-String -Path "tools\*" -Pattern "" > $null; .\.venv\Scripts\python.exe tools/gate_engine.py --check 2>&1 | Select-String "ATOM-VERIFY-REASON"   # => 无输出（0 命中）
# 任务 6：对抗回归（需沙箱）
.\.venv\Scripts\python.exe tools/adversarial_regression.py                  # => escape=0 gap=0 blocked=25 visible=2 skip=35, exit 0
# 任务 7：断点续跑
.\.venv\Scripts\python.exe tools/cppbible.py task create --type demo --desc "d" --total 3
```

## 9. 实测数字（终态，口径记录）
- 开工 pytest 基线 **302 点**（与提示词一致 ✅）；收工 **320 点**（+18：`test_verify_reason.py` 8 +
  `test_task_state.py` 7 + `test_adversarial_regression.py` 3），全绿。
- 数字纪律：本文件所有计数均来自实跑输出。撰写过程中曾按推算误记 325，已按终端实测 **320** 修正
  （记此一笔：口径以实跑为准）。
- 临时件清理进度：本批 494 的探针（`_probe_status.py`/`_probe_fix_status.py`/`_probe_verify_reason.py`）与
  日志已删 **8 件**；仅剩 `_pt494final.log/err`（pytest 终态日志，收工后同 §6 命令一并删）。
