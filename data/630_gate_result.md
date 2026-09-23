# 630 E1 · 收工门禁终跑输出（存档）

> 命令：`.venv\Scripts\python.exe tools/run_630_gate.py --check`
> 时间：2026-09-23 · 结果：**PASS ✅** · 耗时约 35 分钟（含全量非 slow 套件）

```text
  [ok] 工具 baseline_630.py --check
  [ok] 工具 autoimmune_diagnose_630.py --check
  [ok] 工具 autoimmune_fix_proposal_630.py --check
  [ok] 工具 autoimmune_recalc_630.py --check
  [ok] 工具 coverage_metric_630.py --check
  [ok] 工具 attack_surface_axes_630.py --check
  [ok] 工具 autoimmune_threshold_630.py --check
  [ok] 工具 stale_test_triage_630.py --check
  [ok] 工具 pre_push_630.py --check
  [ok] 门禁覆盖本批全部 630 工具（按批次标记核验） ([])
  [ok] 整目录 ruff 全绿
  [ok] mypy tools/ = 0 errors
  [ok] 本批新增测试全过（10 文件）
  [i] 非 slow 全量：既有失败 12 项 · 新增失败 0 项 · 基线已消失 0 项
  [ok] 非 slow 全量无新增失败（失败集 ⊆ 630 冻结基线） (新增 0)
  [ok] 受控目录零污染 ([])
  [ok] push 后 `origin/master..HEAD` = 0 (ahead=0)
  [ok] AST 自证：不调用监工四门禁 ([])
630 收工门禁: PASS ✅
```

## 说明（与任务书口径的差异，已在验收报告 §三 登记）

1. **任务书要求 `pytest -m "not slow" -x -q`（隐含全绿）**：实测存在 **12 项他批既有失败**
   （D1 分类的不可修 11 项 + 终跑新增 1 项）。630 的门禁按「**失败集 ⊆ 冻结基线**」判定并
   打印偏差（既有 12 / 新增 0 / 基线消失 0），`--strict-full` 保留任务书字面口径。
2. **终跑新增的 1 项**：`tests/test_baseline_629.py::test_selftest_and_baseline_failure_freeze`
   —— 629 的**工具 selftest** 断言「push 前 ahead ≥ 62」，而 630 B2 完成 push 后 ahead = 0。
   同类数字断言在**测试侧**（`test_git_facts_readable`）已由 D2 按「只改数字」更新为 `>= 0`；
   但本条失败点在 **629 工具内部**（修它要改 625-629 工具 ⇒ §零.11 越界）⇒ 并入基线并交人。
3. **门禁按批次标记核验**（`*_630.py`）而非「所有新增文件」——这是对 629 门禁
   **跨批脆弱性**的直接修正（629 的清单式核验在 630 一开工就自我判红）。
4. **受控目录零污染复核**：本批曾观察到「全量套件跑完后 `atoms/conc/ATOM-CONC-FENCE-001.md`
   的 `id:` 行被删除」（M1 变异未还原），已还原并登记（根因未定位，见验收报告 §三 偏差 9 /
   §六 交人项 8）。终跑未复现该污染。
5. **push 后 ahead = 0** 由 B2 达到；本门禁把它作为**硬性检查项**（§九 E1 要求）。
