# 639 批次 · 开工快照与全量债务复扫（Task 0）

> 生成：2026-09-25。来源：实测（git / pytest / ruff / mypy / merkle / tool_integrity）。

## 一、快照

| 维度 | 值 |
|---|---|
| 基线 commit | 638 收工态（ahead=19 未 push ⇒ D10） |
| tools/*.py | 429 |
| tests/test_*.py | 430+ |
| 受控目录（atoms/evidence/Examples/Book） | git diff 干净 |

## 二、12 债逐项复核（第一轮修复依据）

| # | 债务 | 复扫实测 | 修复策略 |
|---|---|---|---|
| D1 | 23 卡缺边界三元组 | `four_state_verdict_638.audit()`：cards_with_boundary=0/23；mutation 基线 `by_card` 只盖 **evidence/** 83 卡，**不含 atoms 卡** ⇒ 不可考 | 回填工具逐卡核查 + 诚实标注"边界不可考"（overlay，不污染 evidence） |
| D2 | ledger 缺规则归属 | `decision_event_v2_ledger.jsonl` 452 条，rule 字段 **0**；`basis_refs` 全指向 authority_log（其 418 条亦无规则引用）⇒ 历史不可归属 | schema 加 rule_id/rule_version + 回填工具标 undetermined + 重跑 error_rate |
| D3 | RR 24 对高置信 | top3 均为 ATOM-REL 族 type1 P0 | 代码级 co-fire 复核（见 `639_rr_top3_fix.md`） |
| D4 | tool_integrity 未重钉 | 6 处 violation（toolchain/debt_ledger/golden_lock/governance_doc_guard/mutation_fuzz + merkle 联动） | `tool_integrity --update` 重钉 ✅ |
| D5 | atoms Merkle 不匹配 | 台账 30249ea… vs 实际 eb631e8…；atoms 自 624 台账后经 631 B1/632 C2/634 C1 **合法**改动（liveness/signed_by，均有批次门禁）而台账未重建 | `merkle_integrity build-all` 重建 ✅（根 eb631e8…，5 目录全绿） |
| D6 | metrics_613 红测试 | `test_line_e_pending_and_proofs`(4≠5) + `test_check_passes` —— **根因=D5** Merkle 证明未过 | D5 修复后 8/8 绿 ✅ |
| D7 | v2_regression_627 红测试 | `no_core_change`/`passed` 红 —— 根因：比对区间 `528e9ab2..HEAD` 随 HEAD 漂移，把后续批次的**合法**核心工具改动误判为回归 | 区间钉死 `528e9ab2..0f23af0d`（已核实该区间 CORE_TOOLS 零改动=627 纯增量）✅ |
| D8 | data/638 文件丢失 | 根因定位：conftest（634 A1）会话 fixture 在 pytest 会话结束删除**会话期间新建**的 data/ 文件；638 生成报告与 pytest 交错执行 ⇒ 报告被误删 | 根因分析 `639_file_loss_rootcause.md` ✅ |
| D9 | 闭环路线图错配（P2） | 登记 | 留 640 |
| D10 | ahead=19 未 push（P2） | 登记，收工后由人 push | 留交人 |
| D11 | 工具数表过期（P3） | 登记 | 留 640 |
| D12 | 79 老工具缺 --check（P2） | 登记 | 留 640 |

## 三、第一轮开始前状态

- pytest 全量：D6/D7 相关 4 例红（其余见各轮扫描记录）
- ruff / mypy：全绿（0 errors / 430 文件）
- tool_integrity --check：红（6 violation）→ 第一轮内重钉
- merkle --check：红（atoms 根不匹配）→ 第一轮内重建
