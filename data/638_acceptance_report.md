# 638 验收报告（收工门禁自动生成）

> 生成时间：2026-09-25T09:50:27；工具：`tools/run_638_gate.py`。
> **总判定：PASS**

## 一、门禁结果

| 检查项 | 结果 |
|---|---|
| 受控目录零污染 | ✅ |
| 7 个新工具 `--check` | ✅ 7/7 |
| ruff tools/ tests/ | ✅ All checks passed! |
| mypy tools/ 0 errors | ✅ Success: no issues found in 430 source files |
| 交付文件齐备 | ✅ 22/22 |
| 638 测试套件 | ✅ 57 例通过 / 7 个测试文件 |

## 二、8 个任务交付情况

| 任务 | 名称 | 交付文件 | 存在 |
|---|---|---|---|
| 0 | 开工快照 + 637 闭环复盘 | ✅ `638_baseline.md` | ✅ |
| 3.1 | 四态结论 schema | ✅ `four_state_verdict_638.py`; ✅ `test_four_state_verdict_638.py`; ✅ `638_four_state_schema.md` | ✅ |
| 3.2 | Lifecycle FSM | ✅ `lifecycle_fsm_638.py`; ✅ `test_lifecycle_fsm_638.py`; ✅ `638_lifecycle_fsm.md` | ✅ |
| B1 | known_error_rate 收集器 | ✅ `error_rate_collector_638.py`; ✅ `test_error_rate_collector_638.py`; ✅ `638_error_rate_estimate.md` | ✅ |
| B2 | RR 冲突分类器 | ✅ `rr_conflict_classifier_638.py`; ✅ `test_rr_conflict_classifier_638.py`; ✅ `638_rr_conflict_analysis.md` | ✅ |
| C1 | 闭环第二次运行 | ✅ `loop_rerun_638.py`; ✅ `test_loop_rerun_638.py`; ✅ `638_evolution_memo.md` | ✅ |
| C2 | 闭环规则调优 | ✅ `loop_tuning_638.py`; ✅ `test_loop_tuning_638.py`; ✅ `638_loop_tuning.md` | ✅ |
| E1 | 收工门禁 + 报告 | ✅ `run_638_gate.py`; ✅ `test_run_638_gate.py`; ✅ `638_acceptance_report.md` | ✅ |

## 三、本批核心结论（实测）

| 项 | 结果 | 来源 |
|---|---|---|
| 四态 schema | 已定义并强制边界三元组；**23 张 verified 卡 0 边界 ⇒ 全 `unknown`** | `638_four_state_schema.md` |
| Lifecycle FSM | 五态 + 11 条合法迁移；28 卡初态 `draft 2 / verified 26`；**0 卡有 `lifecycle` 字段** | `638_lifecycle_fsm.md` |
| known_error_rate | **67/67 规则「无数据」**（ledger 无规则字段、target_type 全 edge）；全库代理：改判率 18.81% / 人审改判 8.76% / 逃逸率 0.071% | `638_error_rate_estimate.md` |
| RR 冲突 | 同 scope 候选 **927 对**（退化），**高置信仅 24 对**（type1 6 / type2 14 / type3 4）；卡级 23 张全分类 | `638_rr_conflict_analysis.md` |
| 闭环第二次运行 | 异常 **4 → 2**，误报 **2 → 0**（误报率 0.5 → 0.0），top3 已变 | `638_evolution_memo.md` |
| 闭环调参 | 3 项（T1/T2/T3），**未改 637 工具**（覆盖层实现） | `638_loop_tuning.md` |

## 四、诚实登记

1. 本门禁只校验**本批 638 交付物**，不替历史批次背锅；
2. 门禁的 `--check` 只读（exit 0 不写盘），`--report` 才落盘；
3. **测试套件数据隔离**：根级 `conftest.py`（634 A1）在 pytest 会话结束时**删除会话期间**在 `data/` 新建的文件（**已存在的文件不受影响**——本批实证：把文件放回后跑 `pytest tests/test_run_638_gate.py`，15 个 638 文件全部存活）；
   因此本批丢失**已存在**的 `data/638_*.md/json` **不能**由 conftest 解释，已按「环境/工具层不稳定」登记（见 §五），此后一律**先跑测试、后生成报告、生成后立即核验文件大小、再提交**；
4. mypy 断言用「`Success: no issues found` + exit 0」双条件，避免只看 exit；
5. 四态/FSM 是**新数据用新格式**，历史判决与报告**未改**（§零.1 向后兼容）；
6. known_error_rate / RR / 调参均为**先有再说**（§四.1~4），不是最终形态。

## 五、本批偏差与事故（如实登记）

| 项 | 事实 | 影响 |
|---|---|---|
| 637 闭环产物缺失 | 开工时 `637_evolution_memo.md` 等不存在（637 未落盘），本批**重跑**得到「第一次产出」 | 复盘基于重跑产物，非 637 原物 |
| `637_observer.json` 被污染 | 本批中途该文件被其它进程/测试改写为（`pytest_failures=82`、`tools_total=428`） | C2/C1 改用**实时采集**，并已 `git checkout` 还原该文件 |
| `data/638_*` 文件两度凭空丢失 | 先后丢失 `638_baseline.md` / `638_four_state_schema.{md,json}` / `638_lifecycle_fsm.{md,json}` / `638_rr_conflict_analysis.{md,json}`（7 个，含**已提交**文件）。**机制未查明**：已排除根 conftest（实证已存在文件不受影响）；另观察到 `write_to_file` 写 `data/638_baseline.md` 曾产生 **0 字节**文件 | 全部已用 `git checkout` / 重新生成复原；登记为本环境**工具层不稳定**风险，收工前已逐个核验文件大小 |
| §一 表两处过期 | 工具数（表 417 / 实测 429）、四态 fail（表 25 / 实测 26） | 以实测为准 |
