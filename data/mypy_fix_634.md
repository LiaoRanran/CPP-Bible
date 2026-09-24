# 634 D1 · mypy 632 工具注解修复（改注解不改逻辑）

## 一、目标与结果

- 验收：`mypy tools/` **0 errors**。
- 结果：**`Success: no issues found in 393 source files`**（修前 14 errors / 11 files）。

## 二、修复清单（14 处，全部**只改注解/类型收窄，不改逻辑**）

| 文件:行 | 错误 | 修法 |
|---|---|---|
| `pollution_guard_session_632.py:50` | `__exit__ -> bool` 恒返回 False | `-> Literal[False]`（+ `from typing import Literal`） |
| `coverage_probe_l2_3_632.py:193/201` | `fh` 变量 `wb`/`w` 复用致 BufferedWriter↔TextIOWrapper 冲突 | 二进制那次改名 `fhb` |
| `ci_debt_clear_633.py:80` | `json.loads` 返回 Any | `isinstance(data, dict)` 收窄 |
| `autoimmune_human_fill_helper_632.py:89` | `pri = {}` 需注解 | `pri: dict = {}` |
| `autoimmune_human_fill_apply_632.py:29` | `out = []` 需注解 | `out: list = []` |
| `transparency_anchor_632.py:73` | `rec.get(..)==..` 返回 Any | `bool(...)` 包裹 |
| `test_debt_taxonomy_633.py:79` | `d.get(..)` 返回 Any | `isinstance(v, list)` 收窄 |
| `run_633_gate.py:119` | 同上 | 同上 |
| `soft_baseline_634.py:36` | `json.load` 返回 Any | `isinstance(data, dict)` 收窄 |
| `baseline_634.py:70/72` | `STANDING[...]` 为 Any → 期望 int | `int(STANDING[...])` |
| `add_check_batch_634.py:93` | `m2` 可能为 None | `if m2 is None: return "no_main"` |

## 三、附带修复：A2 引入的导入顺序（10 文件）

A2 给 79 个老工具补 `import sys` 时，部分工具的首个导入被插到 `import argparse` 之前 ⇒
`ruff` I001 导入顺序违规。本批用 `ruff --fix tools/` 一并整理（**纯导入排序，无逻辑变更**）：

`artifact_version_stamp.py` · `asm_regen.py` · `asm_repro_spotcheck.py` · `crossref_audit.py` ·
`d5_gap_scanner.py` · `debt_ledger.py` · `human_review_pre_annotate.py` · `l2_state.py` ·
`patch_blocks.py` · `test_dependency_graph.py`

## 四、纪律与诚实登记

1. **只改注解/导入，不改任何生产逻辑**（§零.5 允许「修注解」）；
2. 触及 632/633 工具（如 `pollution_guard_session_632`/`coverage_probe_l2_3_632` 等）——均
   **非 CORE_TOOLS**（CORE=gate_engine/atom_evidence_replay/poison_drill/toolchain/cppbible）
   ⇒ 无需 `tool_integrity --update`；
3. 修后复跑相关 **146 例**测试全绿；`ruff check tools/` 全绿；
4. `mypy tools/` 现为 **0 errors**。
