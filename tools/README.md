# tools/ · 脚本索引与工程纪律

> 本目录有 **716 个 `.py`**。这一页回答：*某个功能的脚本在哪、命名怎么来的、改之前要注意什么。*
> 693-D1 的**分类是标注出来的**（下表 + 命名前缀），**不是靠目录结构猜的**——
> 物理重整的代价与理由见 §3。

---

## 1. 命名规范

| 前缀 / 形态 | 含义 | 例子 |
|---|---|---|
| `<批次>_<主题>.py` | 某批次的一次性分析/产物生成 | `analyze_692_environment.py` |
| `<功能>_<批次>.py` | 通用功能在某批次的落盘版 | `recompute_a5_676m.py` |
| `<名词>_gate.py` | **门禁**：带 `--check`，失败退非 0 | `paper_quality_gate_670c2.py` |
| `audit_*.py` | 只读审计 | `audit_676k_integrity.py` |
| `verify_*.py` | 校验（对账 / 完整性） | `verify_paper_numbers.py` |
| `gen_*.py` | 生成产物（清单 / 元数据 / 图表） | `gen_693_manifest.py` |
| `bench_*.py` | 性能实测（数字现算） | `bench_693_data_access.py` |
| `test_*.py` | 该工具自带的性质测试 | `test_fast_gate.py` |

**硬规范**

1. **一律 `snake_case`**；
2. 每个脚本必须有 **SPDX 头**（`tools/license_header_check_655.py` 硬门禁）；
3. 门禁类脚本必须支持 `--check`，且**失败退非 0**，不允许静默降级；
4. 新脚本的共用代码放 **`tools/utils/`**（见 §2），不要再造一遍轮子。

---

## 2. `tools/utils/` —— 共用基础设施包（693-D1 新建）

| 模块 | 提供什么 |
|---|---|
| `utils/errors.py` | 统一异常层次：`QueyiError` → `QueyiDataError` → `DataMissingError` / `ChecksumMismatchError` / `SchemaError`；另有 `EnvironmentError_` / `GateFailure`。每个异常带**可执行**的 `hint` |
| `utils/logging_setup.py` | `get_logger(name)`：统一格式 `HH:MM:SS LEVEL name | msg`；`QUEYI_LOG_LEVEL` 环境变量可临时提级 |
| `utils/data_access.py` | `load_json_cached()`（按 mtime+size 失效的进程内缓存）、`sha256_file()`（自适应分块）、`require_fields()`、`verify_manifest()` |

用法（脚本里先 `sys.path.insert(0, str(ROOT / "tools"))`）：

```python
from utils.data_access import load_json_cached, sha256_file
from utils.errors import ChecksumMismatchError
from utils.logging_setup import get_logger

log = get_logger("my_tool")
matrix = load_json_cached(ROOT / "data" / "blindspot_676g_detection_matrix.json")
```

**性能实测**（693-D4，数字由 `tools/bench_693_data_access.py` 现算，存 `data/693_perf_bench.json`）：

| 项 | 结果 |
|---|---|
| 1147×8 冻结矩阵冷读 → 缓存命中 | ~42.9 ms → ~0.29 ms（**×147.8**） |
| 复现流水线模拟（同文件读 4 次） | ~175 ms → ~1.0 ms（**省 99.4%**） |
| 大文件（>2 MiB）sha256 峰值内存 | 2.96 MB → 2.11 MB（流式省 ~853 KB） |
| ≤2 MiB 文件 sha256 | 走一次性读入（**流式反而更费内存**，已按实测切换） |

---

## 3. 为什么**没有**把 `tools/` 拆成 `analysis/ verification/ visualization/ utils/` 子目录

任务书原本要求按功能分子目录。**我们没有做**，理由必须写明，不能含糊过去：

| 代价 | 具体 |
|---|---|
| 信任根断裂 | `tools/tool_integrity.py` 的 **34 条哈希面**以字面路径引用脚本，移动 ⇒ 全部失配 |
| CI 变红 | `.github/workflows/ci.yml` 十余个 job、`conftest.py`、`fast_gate.py` 都以字面路径调用 |
| 回归成本 | 716 个脚本逐个改 import + 回归，数十小时，且失败模式是**静默的**（路径错但没报错） |
| 收益 | 目录更好看 |

**结论**：优化动作本身不能制造事故。693-D1 采取渐进方案——**新增共用代码一律放 `tools/utils/`**，
分类由本文件维护。未来若要搬迁，必须**逐个脚本**做，每搬一个同步更新哈希面与 CI 引用。

---

## 4. 常用脚本速查

| 我想… | 用哪个 |
|---|---|
| 体检环境（编译器/sanitizer/已知坑） | `../scripts/verify_environment.sh` |
| 一键复现 | `../scripts/reproduce_all.sh` |
| 校验冻结产物 sha256 | `gen_693_manifest.py --check` |
| 全面数据完整性检查 | `verify_data_integrity.py` |
| 论文数字对账 | `verify_paper_numbers.py` |
| 论文门禁 | `paper_quality_gate_670c2.py` |
| 批次快速回归 | `fast_gate.py --tests tests/test_<批次>.py` |
| 信任根哈希面 | `tool_integrity.py --check`（改 `pyproject.toml` 后要 `--update`） |
| AI 双标 / 裁决表 | `annotate_693_b.py --csv` |
| 人类裁决一致性 | `compute_693_iaa.py`（裁决回来后跑） |
| 缺陷类型深度分析 | `analyze_693_defect_types.py` |
| 可检测性模型 | `fit_693_detectability_model.py` |
| 反事实扩展 | `analyze_693_counterfactual.py` |
| 元评估 v2 | `eval_693_meta_evaluation.py` |
| 性能实测 | `bench_693_data_access.py` |

---

## 5. 改脚本前必读

1. **改 `pyproject.toml` 后必须** `python tools/tool_integrity.py --update` 重钉哈希面；
2. **不新增 `# type: ignore`** —— 环境性 stub 缺口集中在 `pyproject.toml` 的
   `[[tool.mypy.overrides]]` 声明（现有 `yaml.*` / `numpy.*` / `opentimestamps.*` / `utils.*`）；
3. **门禁失败不许静默**：要么修，要么在验收报告里写明为什么跳过；
4. **性能数字不许写死在文档里**：用 `bench_*.py` 现算，文档引用 JSON 字段。
