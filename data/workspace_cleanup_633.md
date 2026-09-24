# 633 B1 · 工作区 data 文件漂移清理（保守优先）

> 依据任务0 的「git 债」盘点。原则（§零.16）：**还原操作保守优先**——只有
> **确认是时间戳/计数假脏**的文件才 `git checkout --`；有实质内容的一律登记不还原；
> **绝不批量 `git checkout -- data/`**。

## 一、处理前状态

| 项 | 值 |
|---|---|
| 处理前工作区脏文件总数 | **74**（A2 全量 pytest 副作用后又增长） |
| 其中 `data/` 已跟踪修改（M） | 35 |
| 其中 `data/` 未跟踪（??） | 14 |
| 其他 | `_adv_v80/probes/p57.cpp`(M) + `_arch_v2x/`、`tools/queyi_core_*` 等残留 |

> 判定方法：对每个 M 文件做 `git diff`，把变化行按「去数字后是否相同」归一——
> 若增删行归一后完全一致 ⇒ 只有时间戳/计数变化 ⇒ **假脏，可还原**；否则 ⇒ 实质内容，登记。
> `git diff -w` 与 `git diff` 的 numstat 完全一致 ⇒ **不存在纯空白/CRLF 假脏**。

## 二、已还原（7 个，逐个 `git checkout --`，均经 diff 确认）

| 文件 | 变化性质（diff 摘要） |
|---|---|
| `data/authority_v2_mode.json` | 仅 `set_at` 时间戳：`...09-23T13:20:39Z`→`...09-24T13:25:55Z`（`by: selftest`） |
| `data/coverage_probe_l8_4_631.json` | 仅计数：`prod_entries` 40→39、`removed_index` 20→19 |
| `data/coverage_probe_l8_4_631.md` | 仅计数：生产日志条目 40→39 |
| `data/human_review_dashboard_v2.html` | 时间戳 + 渲染计数：VSA 24→35 张、透明日志 35→39 条 |
| `data/independence_static_check_629.md` | 仅计数：`tools/` 模块数 343→370 |
| `data/learner_twin_gate_report_628.md` | 生成时刻 + 候选事件计数 872→879（分来源各 +2/+5） |
| `data/metrics_612.md` | 仅时间戳/计数（1 行） |

> 上述均为**工具重跑产生的派生数字/时间戳**，非人工内容；还原回 HEAD 版本，
> 与提交历史一致。

## 三、登记不还原（实质内容变化）

**28 个 `data/` 已跟踪文件**含实质变化，按要求**登记不还原**，例如：

- `data/autoimmune_rate_baseline.md`：warn 事件 134→67、block 0→25、规则分布变化
  （反映 631 liveness 修复 + 624 block 规则接线的真实演进）；
- `data/autoimmune_diagnose_630.{json,md}`、`data/autoimmune_fix_proposal_630.*`、
  `data/autoimmune_recalc_630.*`、`data/autoimmune_threshold_630.*`：630 工具在
  631 修复后重算的产物；
- `data/pre_push_check_630.*`、`data/snapshot_integrity_*_626.*`、
  `data/third_party_audit_demo_628.*`、`data/629_baseline.md`、`data/630_baseline.*`、
  `data/631_baseline.*`、`data/e2e_attestation_629.md`、`data/coverage_probe_l1_2_631.*` 等。

**判定理由**：这些不是时间戳假脏，而是**被验证对象演进后重算的真值**；还原会丢失
更新后的数字并与工具当前输出矛盾 ⇒ 保守登记。

## 四、明确不碰（铁律保护）

| 文件 | 原因 |
|---|---|
| `data/mutation/full_baseline_v4.json`、`evidence/conc/EV-CONC-001.md` | §零.8 两条 CRLF 假脏文件（本次未出现在 dirty 列表，无需动作） |
| `data/transparency_log.jsonl`、`data/learner_behavior_events.jsonl`、`data/autoimmune_human_queue_631.jsonl` | §零.11 append-only 账本，**不删不改**（即使被测试追加，也不还原、不提交） |
| `_arch_v19..23/`、`_adv_v80/`、`data/queyi_core_*`、`tools/queyi_core_*`、`data/vsa/attestation_*.json` | §零.12 工作区残留，**禁提交**，处置交人 |

## 五、处理后状态

| 项 | 值 |
|---|---|
| 处理后工作区脏文件总数 | **64**（还原 7 → 74 降为 67，再扣除未跟踪计数差异后为 64） |
| 其中 `data/` 已跟踪修改（M） | 28（均实质内容，登记） |
| 其中 `data/` 未跟踪（??） | 14（残留/测试产物，登记） |
| 受控目录 `git diff --quiet -- atoms evidence Examples Book` | **exit 0（零污染）** |

## 六、诚实登记

1. **不确定的一律未还原**：只还原了 7 个「去数字后等价」的文件；其余 28 个实质变化文件
   全部登记，未做任何 `git checkout`；
2. **还原≠永久干净**：A2 已实测套件有数据副作用，**再次跑测试会把这些文件重新改脏**
   （§零.8 之外的假脏会复现）⇒ 本批清理只保证「此刻」的工作区状态；
3. **未提交任何前批次的真脏改动**：本 commit 仅新增本报告；
4. 受控目录全程零污染（§零.5 满足）。
