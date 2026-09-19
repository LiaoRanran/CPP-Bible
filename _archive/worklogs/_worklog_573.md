# _worklog_573 · 夜间大包（扩展版）：ruff 精选族 + 三曲线/推翻事件

> 任务书：`References/architecture_架构演进/573_夜间大包_推翻事件三曲线_ruff精选_阴面扩覆盖.md`
> 承接：`0a4dc80`（572）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。
> **停在任务边界**：任务 0 / B / A **完成并逐项提交**；**任务 D、E、C 未开工**（见 §6）。

## 0 · 任务 0（开工先量，改动前跑的 `_acc573.log`）

| 项 | 实测 |
|---|---|
| `tool_integrity --check` | OK exit 0 |
| gate | `规则 63 条 · 命中 141 (block=0 warn=136 advice=5)` |
| replay | `confirm=56 refute=0 infra_error=0` |
| pytest fast / slow | 验收脚本跑完（DONE） |

⇒ 基线干净，允许往上叠。

## 1 · 任务 B：ruff 精选族（**逐族独立 commit**，每族后 pytest）

各族规模（开工时实测）：I001 127 / PTH123 142 / PTH118 111 / FURB167 93 /
PLW1510 102 / S603 101 / 其余（SIM115 77、BLE001 65、ISC004 69、RUF100 97、UP009 93…）留待后续。

| 族 | 结果 | commit |
|---|---|---|
| I001（import 排序） | **127 处自动修**，117 文件，pytest 全绿 | `c99a7be` |
| PTH123（builtin-open→Path.open） | ruff **未标记为安全可修**（只报告、未改）⇒ 交人 | — |
| PTH118（os.path.join→/） | 同上 ⇒ 交人 | — |
| FURB167（regex flag 别名） | **93 处自动修**，pytest 全绿 | `8163482` |
| PLW1510 / S603 | **只审计不改逻辑**（570 subprocess 教训）⇒ 清单 210 行落盘 | `65d5a08` |
| 钉最终 select | `["E4","E7","E9","F","I001","FURB167"]` + 永久不开族的**理由写进 pyproject 注释** | `65d5a08` |
| 收尾（hy3 E402 + 新代码自身告警） | 启用族 **0** | `2393a05`, `d79a4a7` |

* 审计报告：`docs/kernel/subprocess_audit.md`（210 行，逐处"文件:行"清单，是否真需容错由人判断）。
* **永久不开**（理由已写进 pyproject，免得重复争论）：`RUF001/002/003`（中文 2 万+噪声）、
  `T201`（CLI 本就 print）、`S101`（assert）、`CPY001`（版权头）、`D*`/`ANN*`（另批）、
  `Q000`（引号 churn）、`PTH123`/`PTH118`（未标记安全可修且需人核）、`PLW1510`/`S603`（只审计）。

## 2 · 任务 A：三曲线从占位变真数据 + overturned 事件通道（`522767d`）

**A-1 逃逸率升 v2**（v1 保留为历史时点**不覆盖**）：
```
source data/mutation/full_baseline_v2.json · judged 969 · n_a 212
point 0.062951（61/969）· C-P95 [0.048491, 0.080133]
```
（v1 是 227/956 = 0.2374，含 M2 的 207 条**假逃逸**——571 已证实是 GATE_READ_KEYS 尺子 bug。）

**A-2 overturned 事件通道**（`data/overturned_events.jsonl`，只追加）：
* schema：`{ts, target, card, old_verdict, new_verdict, by, reason}`；
* `by` = `human:<名>` 或 `adversary:<族>`；**human 名必须与该卡最后一次 git 提交作者一致**
  （复用 gate_engine 同款判据）；冒名 / git 不可用 / 缺字段 / 卡解析不到 ⇒ **拒绝写入（fail-closed）**；
* CLI：`metrics_collector.py --log-overturned --target … --old … --new … --by … --reason … [--card …]`
  （不合规 ⇒ exit 2 并打印原因）；
* **系统绝不自动产生推翻**（自动 LLM 推翻在冻结档）——本函数只接显式的人/异族动作。

**A-3 survival 第一批真实数据（不编）**：
`M3 = 1 批`（571 v2 浮出 52 条 → 572 全部收口）；`M2 = None`（207 条是尺子 bug 的假逃逸，不计入）；
其余算子 `None`（不填 0）。

**回归锁**：`tests/test_overturned_curves.py` 7 例（v2 与 `stat_bounds` **逐值一致** / 事件 schema /
冒名拒写 / 缺字段拒写 / git 不可用拒写 / 异族放行不核签 / 曲线计数来自事件流 / survival 只数 M3）。

## 3 · 任务 A 的连带修正（如实留痕）

既有 3 条曲线用例钉的是 **v1 与占位**（227/956、`"真值"`、`survival is None`）⇒ 升级后必然失效，
按实测更新为 v2（61/969）、"绝不自动产生推翻"、`M3=1 批且其余 None`（`42efad1`）。
另：我新用例里写的卡 id `ATOM-MEM-MOVE-001` **不存在**（核验必定拒写）⇒ 改为真实卡
`ATOM-LANG-INLINE-001`。修后 targeted + fast 均 exit 0。

## 4 · 收工验收（本批实测）

| 项 | 实测 |
|---|---|
| gate | `63 条 · 141 (block=0 warn=136 advice=5)` —— 与基线逐字相同（**存量零误伤**） |
| poison | `114/114` |
| `tool_integrity --check` | exit 0（每族改到 CORE_TOOLS 都同 commit 重钉） |
| ruff（启用族） | **All checks passed!** |
| pytest fast `-n auto` | **exit 0** |
| A-1 v2 point | 0.062951（61/969）· C-P95 [0.0485, 0.0801] |
| A-2 无签名拒写 | 冒名 / git 不可用 / 缺字段 ⇒ ValueError，且**不落任何行** |
| A-3 survival | M3 = 1 批；M2、others = None |

## 5 · 偏差表

1. **PTH123/PTH118 未自动修**：提示词把它们列进"安全自动修族"，实测 ruff **未标记为安全可修**
   （只报告）⇒ 按"不可自动修的列清单交人"处理，并把理由写进 pyproject（不做 unsafe fix）。
2. **既有曲线用例被我改了**：口径升级的必然后果（同 571/572 的重冻结），已在 commit message 与 §3 注明。
3. **任务 A 的两个 commit**（实现 `522767d` + 测试修正 `42efad1`）：修正属于同一任务的收尾，
   单独立 commit 便于 review。
4. **慢速验收**沿用开工那份（改动前）；**改动后**的 fast 已复跑 exit 0，slow 未单独复跑（见 §7）。

## 6 · 停在任务边界：D / E / C 未开工

本批预算被 **B 的逐族修（4 次全量 pytest）+ A 的事件通道与连带修正** 消耗殆尽，按任务书
"做不完停任务边界、不留半成品"，**任务 D（verified_by_oracle 只写不读）、E（M5 算子诊断）、
C（V-iso 阴面扩 3 张）一行未动**，移交下一批；三者都无新增侦察负担（现状与做法已在任务书与
本文件写明）。下一批建议顺序：**E（最像 571 修 M3，性价比高）→ D（纯接口 + 锁）→ C（最重）**。

## 7 · 交下一批

* E：`mut_m5` 的正则 `^(\s*)claim_type:\s*(\w+)\s*$` 只匹配卡面顶层，而 29 条 inference 命题在
  `claim_structured[*].claim_type` 里 ⇒ 先打逐卡证据再决定是"真 n_a"还是"算子 bug"。
* D：全仓 `verified_by_oracle`/`oracle_version` **0 出现**；只建字段 + registry + "判决逐字不变"的锁。
* C：57 卡只有 EV-CONC-001 有真阴面；19 张 run_match 卡是候选池，**只挑 3 张**、判据一条不降。
* ruff 余族（SIM115/UP031/DTZ005/BLE001/ISC004/RUF100/UP009/UP035/PIE810/SIM103）按族分批继续。
