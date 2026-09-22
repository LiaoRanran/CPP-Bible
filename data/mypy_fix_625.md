# 625 A1 · mypy 67 处存量债修复（CI quality 红因）

> 目标：`mypy tools/` 错误数 = 0。
> 铁律：只改类型注解/导入/小修，**不改 CORE_TOOLS 核心逻辑**；禁止批量 `# type: ignore`。

---

## 一、结果

| 阶段 | `mypy tools/` 错误数 |
|---|---|
| 修复前 | **67**（24 文件） |
| yaml stub 覆盖后 | 60 |
| 逐文件修复后 | **0**（271 源文件，`Success: no issues found`） |

- `ruff check tools/ tests/`：**All checks passed**（修复 mypy 后未引入新 ruff 错误）。
- 单测回归：非 slow 套件失败数 **未新增**（仅剩治理 manifest 待重签 + OTS 过期，属 A2/F2 范围）。

## 二、错误类型分类与处置

| 类型 | 数量 | 处置方式 |
|---|---|---|
| `import-untyped`（yaml 缺 stub） | 7 | **pyproject `[[tool.mypy.overrides]] module="yaml.*" ignore_missing_imports=true`**（types-PyYAML 非本仓依赖，集中声明） |
| `no-any-return`（json/yaml 返回 Any） | ~12 | `cast("dict[str, Any]", ...)` 或 `str(...)` 收敛（vfdr_619 / ci_concurrency_check_621 / vfdr_calculator_622 / pck_certificate_verifier_619 / pck_renderer_619 / pck_pilot_generator_619 / pck_batch_migrator_620 / high_complexity_attack_surface_623 / adversarial_loop_620 / vfdr 等） |
| `arg-type`（`Any \| None` 作 dict 键） | ~15 | `str(x.get(...) or "")` 收敛（authority_pending_621 / pck_status_stats_620 / pck_authority_sync_620 / pck_abstain_sync_621 / human_review_quality_compare_621 / human_review_anonymize_621 / verification_horizon_622） |
| `var-annotated`（缺注解） | 5 | 补注解（round3_mutator_623 RECIPES / high_complexity_mutator_623 atoms/evidences/pools / adversarial_attacker_619 equiv / escape_root_cause_622 rows / verification_horizon_622 rows） |
| `assignment`（变量类型冲突） | 4 | 重命名循环/局部变量（authority_log_620 `e`→`rec`；high_complexity_mutator_623 `c`→`_c`） |
| `dict-item`（字典值 str/None 混杂） | 2 | 首个赋值补 `list[dict]` 注解（pck_pilot_generator_619 / pck_batch_migrator_620 evidence） |
| `attr-defined` / `type-var` / `index` | ~7 | 收敛返回值类型 / 键类型（human_review_anonymize_621 scrub_text/names；round3_mutator_623 RECIPES 注解消除 object 索引） |
| `func-returns-value` | 1 | `# type: ignore[func-returns-value]` + 原因（`sub_verifier_disagreement` 按设计恒 N/A） |

## 三、修改文件（23 个）

round3_mutator_623 · high_complexity_mutator_623 · high_complexity_attack_surface_623 · escape_root_cause_622 ·
verification_horizon_622 · vfdr_619 · vfdr_calculator_622 · ci_concurrency_check_621 ·
pck_certificate_verifier_619 · pck_renderer_619 · pck_pilot_generator_619 · pck_batch_migrator_620 ·
pck_status_stats_620 · pck_authority_sync_620 · pck_abstain_sync_621 · human_review_anonymize_621 ·
human_review_quality_compare_621 · authority_log_620 · authority_pending_621 · adversarial_loop_620 ·
adversarial_attacker_619 · adversarial_objective_619 · adversarial_weight_calibration_620
（另 `pyproject.toml` mypy 覆盖；`tools/.tool_checksums` 因触及受保护 pyproject 而重钉）。

## 四、`# type: ignore` 清单（仅 1 处，逐条说明）

| 文件:行 | 错误码 | 原因 |
|---|---|---|
| `tools/adversarial_objective_619.py:141` | `func-returns-value` | `sub_verifier_disagreement` **按设计恒为 N/A（显式 `return None`）**；该处显式取 None 属预期，非逻辑错误 |

> **无批量 ignore**：其余 66 处均为真实修复（补注解 / cast / 判空 / 重命名）。

## 五、回归结果

- `mypy tools/`：**Success（0 errors）**。
- `ruff check tools/ tests/`：**All checks passed**。
- `pytest -m "not slow"`：失败项 **未新增**（残留 4 项 = 治理 manifest 重签 ×3 + OTS 过期 ×1，均非 A1 引入）。

## 六、局限性声明

1. `mypy tools/ tests/` 联跑会触发 `metrics_collector` **模块名重复**（mypy 已知限制，非代码错误）⇒ CI 口径为 `mypy tools/`（本任务已 0）。
2. yaml 覆盖是**环境性 stub 缺口的集中声明**，不掩盖 yaml 使用处的真实类型（业务处仍逐个 cast/判空）。
3. 修改 `pyproject.toml`（受保护）⇒ 已同 commit `tool_integrity.py --update` 重钉。
4. 本批只修类型债，**不改任何运行时逻辑**。
