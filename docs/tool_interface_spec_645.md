# 645 工具接口统一规范（D2 · 强制约束）

> 本文件是 645 轮次所有工具必须遵守的接口契约。新增/修改 645 工具须通过 `interface_audit_645`
> 静态审计（`tools/interface_audit_645.py --audit`）。不遵守任一契约 → 门禁失败。

## 一、CLI 契约

1. **只读自检**：每个工具必须有 `--check` 参数，执行**只读幂等自检**（不写盘、不联网、
   不编译全库、exit 0 表示通过）。CI 与门禁先跑所有工具的 `--check`。
2. **真跑参数**：真实数据采集用明确动词参数，禁止用「dry-run / 代理 / 降级完事」冒充真跑：
   - 智能层采集：`--discover` / `--attack` / `--draft` / `--detect` / `--track` / `--run`
   - 头部层采集：`--probe` / `--acquire` / `--grade` / `--judge` / `--search`
   - 编排/反馈：`--run`（编排）/ `--feedback`
3. **退出码**：成功 0；环境缺失（如缺 g++）非 0 且打印可读原因；不静默吞错。

## 二、文档契约

每个工具模块顶部 docstring 必须含三段，且含「645」字样（供审计识别）：
- **目标**：本工具在 645 哪一层、达成什么验收。
- **数据源**：真实数据从哪来（文件名/类/账本），如何保证非代理。
- **铁律**：本工具遵守的 645 铁律（不污染受控目录、不自动上线、不编造等）。

## 三、数据模型契约（三层耦合唯一通道）

三层之间**只**用 `tools/queyi_data_models_645.py` 的三个数据类传递：
- 智能层 → `Issue`（issue_id / title / root_cause / severity / evidence_refs / suggested_next）
- 头部层 → `EvidencePackage`（package_id / topic / evidence / grade_summary / sufficiency / counterexamples）
- 尾端 → `VerificationResult`（result_id / target_id / verdict / confidence / detail / escape_assoc）

约束：
- 所有数据类可 `to_dict()` / `from_dict()` 往返；层间传递用 `serialize()`/`deserialize()`。
- `root_cause` 与 `evidence_refs` 必须引用**真实数据**（规则 ID / 卡 ID / 账本 seq），禁止启发式凑数。
- `verdict` 取值：`pass | fail | escape | false_positive | unknown`；`needs_human` 仅在确实缺证据时使用。

## 四、质量契约

- **注释充分**：模块/类/关键函数 docstring + 关键行内注释（中文）。
- **单测覆盖**：每个 645 工具配 `tests/test_*_645.py`，fast 组不调用编译器/不联网；
  调用编译器/联网的测试标 `@pytest.mark.slow` 并在 `conftest` 注册。
- **不污染受控目录**：`atoms/`、`evidence/`、`Examples/`、`Book/` 零写入（只读 + 沙箱编译）。
- **不动 CORE_TOOLS**：5 个核心判决工具的判决逻辑零改动；草案注入在隔离环境跑（见 A3）。

## 五、命名契约

- 工具文件：`tools/<功能>_645.py`；测试：`tests/test_<功能>_645.py`。
- 报告产物：`data/645_<功能>_report.md` + `.json`；统一前缀 `645_` 便于门禁核对。

## 六、违反处理

门禁 `run_645_gate.py` 在阶段 D 检查 `interface_audit_645` 结果：若有工具不满足契约，
记 `needs_fix` 并阻断收工（诚实登记，不「改到绿」）。
