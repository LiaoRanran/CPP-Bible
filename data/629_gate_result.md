# 629 F1 · 收工门禁终跑输出（存档）

> 命令：`.venv\Scripts\python.exe tools\run_629_gate.py --check`
> 时间：2026-09-23 · 结果：**PASS ✅** · 耗时约 35 分钟（含全量非 slow 套件）

```text
  [ok] 工具 baseline_629.py --check
  [ok] 工具 autoimmune_rate_framework.py --check
  [ok] 工具 autoimmune_probe_629.py --check
  [ok] 工具 autoimmune_dashboard_629.py --check
  [ok] 工具 attack_surface_taxonomy.py --check
  [ok] 工具 attack_mapping_629.py --check
  [ok] 工具 uncovered_attack_surfaces.py --check
  [ok] 工具 vsa_asymmetric_signer_629.py --check
  [ok] 工具 authority_log_integration_629.py --check
  [ok] 工具 independence_static_check.py --check
  [ok] 工具 e2e_attestation_629.py --check
  [ok] 工具 attack_objective_629.py --check
  [ok] 工具 attack_round8_629.py --check
  [ok] 工具 loop_metrics_629.py --check
  [ok] 门禁覆盖本批全部新增工具（git 交叉核验） ([])
  [ok] 整目录 ruff 全绿
  [ok] mypy tools/ = 0 errors
  [ok] 本批新增测试全过（13 文件）
  [i] 非 slow 全量：既有失败 11 项 · 新增失败 0 项 · 基线已消失 0 项
  [ok] 非 slow 全量无新增失败（失败集 ⊆ 629 开工冻结基线） (新增 0)
  [ok] 受控目录零污染 ([])
  [ok] 未跑监工四门禁（AST 扫描：无监工门禁调用） ([])
  [ok] 未改 ci.yml / 未改 CORE_TOOLS 生产逻辑
629 收工门禁: PASS ✅
```

## 说明（与任务书口径的差异，已在验收报告 §四 登记）

1. **任务书要求「`pytest -m "not slow"` 全绿」**；629 开工实测存在 11 项真实既有失败
   （628 数据处置使 627 断言过期 5 项 / 本地未跟踪 `_arch_v2x/` 使治理 manifest 不一致 4 项 /
   625 阈值过期 1 项 / 611 快照 1 项），均属**他批资产**（§零.11 不改）。
   门禁因此改为「**失败集 ⊆ 冻结基线**」口径并打印偏差；`--strict-full` 保留任务书字面口径。
2. **本批曾出现 1 项真实回归（已修）**：C2 首版 anchor 非确定性 ⇒ 628 B3「日志引用文件哈希一致」
   漂移 ⇒ `test_run_628_gate_628` 等失败。C2 修复（anchor 确定性 + 凭证一次性写入 +
   回滚 4 条未提交重复条目）后，该项已消失（基线已消失 0 / 新增失败 0 证明）。
3. 门禁自带 `--no-tests` 反递归模式，由 `tests/test_run_629_gate.py::test_gate_other_steps_pass`
   覆盖（该子进程跑除 pytest 外的全部步骤）。
