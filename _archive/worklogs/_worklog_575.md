# _worklog_575 · 堵 M5 活雷：活性从「卡级」提到「命题级」

> 任务书：`References/architecture_架构演进/575_夜间大包_堵M5活雷_命题级活性锚.md`
> 承接：`dd5d29d`（574）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。
> 提交：`a10c6e0`。**M5 报告口径仍未翻盘（有已验证的修法，本批预算耗尽 ⇒ 回退，交下一批，见 §4）。**

## 0 · 任务 0：先量（不量清楚不许建字段）

**0.1 fresh 基线**（改动前）：gate `63 条·141 (block=0 warn=136 advice=5)` · replay `confirm=56` ·
`--check` exit 0 · ruff 启用族 0 · pytest fast 绿。

**0.2 读到的真实判据**（行号以磁盘为准）：
* `check_observation_liveness`（2411 起）：逐原子卡的 `claim_structured` 命题，只看
  `claim_type == observation`，取命题 `evidence` 引用的证据卡，三条 `_has_*` 任一成立即放行；
  三条皆无 ⇒ warn。**判定对象是"引用卡"，不是"这条命题"** ⇒ 这就是活雷的根源。
* `_has_fixture_specific_assert_symbol(meta)`：复用 `_assert_targets`/`_assert_haystack`/`symbol_map`
  /`_is_universal_symbol`；`_has_non_env_run_key(meta)` 复用 `_is_env_key`；量化用
  **`_falsification_quantified(text)`**（注意：不是 `_FALSIFICATION_QUANTIFIED_RE`，我第一次写错）。

**0.3 盘点表**（`_t0_575.py`，27 张原子卡 / **50 条 observation 命题**）：

| 项 | 数 |
|---|---|
| observation 命题 | 50 |
| 引用卡上能定位到至少一种活性形态（fixture_symbol / quantified / run_key） | **50** |
| 引用卡上找不到任何形态 | 0 |
| 卡面**已写** `liveness` 字段 | **0** |
| ⇒ 若强制命题级锚，**新增 warn = 50** | **50** |

⇒ 这个数先报了才建的字段（债务规模 = 50，不得为压低数字放宽判据）。

## 1 · 任务 1：命题级活性锚字段 + 机检（warn）

* **字段**（可选，命题项内）：`liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}`；
  机检：符号须真实出现在**本命题引用卡**的 `artifact_assert` 目标里 + 非通用 + 非散文；
  缺锚 / 锚通用符号（`.file`）/ 锚不存在的符号 ⇒ **warn**（假锚也必须被看见）。
  *只做 fixture_symbol 一种形态*：quantified / run_key 的命题级指认需要更细的"取值串/键名"口径，
  拿不准就不做（已在代码注释与本节写明）。
* **挂既有 `OBSERVATION-LIVENESS`**，不新增规则 id（RULE-COVERAGE 仍 38/63，无覆盖债）；**只 warn 不 block**。
* inference 命题不要求（沿用 external_basis）。

**实测**：gate `63 条 · 命中 191 (block=0 warn=136→186)` —— **新增 warn 恰好 50**，与盘点逐条对得上。

**踩到的顺序坑（最重要的一条）**：锚检查必须放在"引用卡"判断**之前**。最初我把它放在
`if any(三条): ...` 分支里，v4 首跑 **M5 仍 29/29 逃逸** —— 因为 M5 的变异体是"inference 命题
改标 observation"，而这些命题**没有 `evidence` 引用**（靠 external_basis）⇒ 前面的
`if not cards: continue` 把整条跳过了。定点诊断（把变异体写进沙箱直接调规则）显示：改到前面后
prop-2 立刻多出一条 warn（51 条 = 存量 50 + 新 1）⇒ 规则本身是对的。

## 2 · 任务 2：毒样例

| 载荷 | 结果 |
|---|---|
| P74（+）observation 命题缺命题级锚 ⇒ warn | ✅ |
| P74-阴（−）锚了真实夹具特有符号 ⇒ 放行 | ✅ |
| P75（+）锚通用符号 `.file` ⇒ warn | ✅ |
| P76（+）锚引用卡里不存在的符号 ⇒ warn | ✅ |
| P68-阴（旧阴性对照）"卡级活性 ⇒ 放行" | 按**新语义**补了命题级锚后 ✅（旧对照正是被堵的那个洞） |

poison **114 → 118**，台账重算 11/11，改 CORE_TOOLS 同 commit 重钉。

## 3 · v4 基线 + metrics 时点 + 待补锚清单

* `data/mutation/full_baseline_v4.json`（含顺序修复后的全量 7 算子）；**v1/v2/v3 保留不覆盖**。
* metrics 逃逸率时点升 v4（历史时点 3 个：v1/v2/v3）。
* 待补锚清单：`data/prop_liveness_todo.md` —— **50 条**缺锚 observation 命题（卡/命题/引用卡/
  可锚形态/建议可锚符号）。**机器绝不写入卡面**（补锚是知识活，交人或 576 之后的强模型知识轮）。

## 4 · ⚠️ 未达成项：M5 在**报告口径**上仍是 escaped（修法已验证，本批回退）

* 现状：M5 复跑仍是 `escaped 29`。**但规则确实命中**（毒样例 + 定点诊断双证）。
* 真因：`mutation_fuzz._findings_key` = `(规则 id, 严重度, 目标)` ⇒ **同一张卡上第二条同规则告警
  会被"基线里已有该 (规则, 目标)"吞掉** ⇒ prop-2 新增的 warn 在 `new - baseline` 里看不见。
* **已验证的修法**：把文案并入键 ⇒ 实跑 M5 = **blocked 29 / escaped 0**，其中 **warn_only 27 + strict 2**
  （含 warn 处置率 **29/29 = 100%**；严格率 2/29 —— 这 2 条另有真 block 规则命中，**不是把 warn
  算成 block**）。
* **为什么回退**：该改动会打散两条 548 用例（`test_548_diff_is_not_card_scoped`、
  `test_548_replay_runs_only_when_it_can_change_verdict`—— 它们自己造假 `new` 集、按 3 元组解包）。
  本批预算已耗尽 ⇒ 按"不留半成品"**回退键改动**，在代码注释里写明修法与定位，交下一批。
* ⇒ **下一批第一件事**：把 `_findings_key` 改为含文案（同步 `classify` 里两处解包 + 那两条 548 用例），
  然后重跑 v5，M5 即可在报告口径上翻盘。

## 5 · 收工验收（fresh）

| 项 | 实测 |
|---|---|
| gate | `63 条 · 191 (block=0 warn=186 advice=5)`；**新增 warn = 50 = 任务 0 盘点数** |
| poison | `118/118` |
| `tool_integrity --check` | exit 0（同 commit 重钉） |
| ruff 启用族 | **All checks passed!** |
| pytest fast `-n auto` | exit 0（含 test_mutation_fuzz 21 例） |
| golden_lock | **判"恶化 1"**（warn_findings 136→186）——按纪律**不 accept**，交人 |
| 受控目录 | 零残留 |
| M5 报告口径 | 仍 29 escaped（规则命中但被 diff 键吞，见 §4，有已验证修法） |

（本批未复跑 slow 组；M3/M5 相关 targeted 与 fast 全绿。）

## 6 · 偏差表

1. **债务 50 条 warn** 是本批**设计内**的暴露（任务 0 先报的数），不是误伤；不得为压数字放宽判据。
2. **只做了 fixture_symbol 一种锚形态**（quantified / run_key 的命题级口径拿不准 ⇒ 不做，已写明）。
3. **M5 报告口径未翻盘**（§4），修法已验证但因预算回退。
4. **一处顺序 bug**（锚检查放在引用卡判断之后）⇒ v4 首跑白跑一次，靠定点诊断才发现。
5. **第一次写盘点脚本用错了函数名**（`_FALSIFICATION_QUANTIFIED_RE` 不存在，真名 `_falsification_quantified`）。

## 7 · 交下一批

1. **`_findings_key` 并入文案**（含两处解包 + 两条 548 用例）⇒ 重跑 v5，M5 翻盘（§4）。
2. **50 条待补锚**：`data/prop_liveness_todo.md` —— 知识活，交人或强模型知识轮。
3. **golden 恶化 1**（warn 136→186）需要人审 accept + 分类留痕（`check --accept "理由" --classify …`），
   苦力不得自行 accept。
4. 冻结项：自动 KG / LLM-as-judge / 自动推翻 / PoC#3/#4/#5 / 阴面（归 576）/ golden fork / ruff 噪声族。
