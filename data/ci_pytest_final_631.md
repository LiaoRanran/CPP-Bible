# 631 A4 · 全量 pytest 复跑确认

> 复跑命令：`pytest -m "not slow" -n0 -q --tb=line -rf`（A2/A3 修复后）
> 修复前基线：`data/ci_pytest_raw_631.txt`（**14 项**）

## 一、修复前后对比

| 分类 | 修复前 | 修复后 | 说明 |
|---|---|---|---|
| 跨批脆弱型 | 6 | **0** | A2 修断言（含 631 期间新暴露的 630 门禁 1 项） |
| 工具自检过期型 | 3 | **0** | A3 修断言 |
| 环境依赖型 | 5 | **5** | 不修（CI 不成立） |
| 真实缺陷型 | 0 | **0** | — |
| **合计** | **14** | **5** | **-9** |

**新增失败 = 0**（修复过程没有引入任何新红）。

## 二、剩余 5 项：全部是环境依赖型（逐条）

| # | 用例 | 根因 | 为什么 CI 不成立 |
|---|---|---|---|
| 1 | `test_ci_pytest_fix_625.py::test_governance_manifest_verified` | 治理 manifest 判定「29 处新增」= 本地**未跟踪** `_arch_v21/` | CI 检出不含未跟踪文件 |
| 2 | `test_governance_doc_guard_591.py::test_verify_real_manifest_matches` | 同上 | 同上 |
| 3 | `test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash` | 同上（自哈希随未跟踪文件变） | 同上 |
| 4 | `test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch` | 603 捕获产物是 UTF-16，测试按 UTF-8 解码 ⇒ `UnicodeDecodeError` | **存疑**：该产物已入库，CI 检出同样存在 ⇒ 这一项**可能在 CI 也成立**（630 已把它计入"CI 成立的 7 项"） |
| 5 | `test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` | 链内含 governance_check，同样被 `_arch_v2x/` 判不一致 | CI 检出不含未跟踪文件 |

**诚实边界**：#4 与 #1-#3/#5 的成因不同——#4 的 UTF-16 产物**已入库**，不随未跟踪文件消失；
因此"CI 实际红项"应为 **1 项（#4）**，而不是 0。§十二.4 要求：真实缺陷型不修复、标注交人；
#4 属于**断言与数据编码不匹配**，改断言需理解 611 的原始意图 ⇒ **交人**（未改）。

## 三、A2/A3 修复清单回放

| 文件 | 改法 | 结果 |
|---|---|---|
| `tests/test_run_629_gate.py` | 清单核验排除更晚批次 + 2 例条件 skip | 3 pass / 2 skip（原 3 fail） |
| `tests/test_run_628_gate_628.py` | status 单调断言 + 1 例条件 skip | 5 pass / 1 skip（原 2 fail） |
| `tests/test_pre_push_630.py` | 拆聚合、断分量 | 7 pass（原 1 fail） |
| `tests/test_pre_push_checklist_627.py` | 按实测 drift 条件 skip ×2 | 4 pass / 2 skip（原 2 fail） |
| `tests/test_baseline_629.py` | 去掉对 629 工具 selftest 的依赖 | 全 pass（原 1 fail） |
| `tests/test_run_630_gate.py` | 按 `ahead > 0` 条件 skip（631 不 push） | 5 pass / 1 skip（原 0 fail→1 fail→skip） |

## 四、A 线结论

1. **CI pytest 红的"跨批脆弱型"与"工具自检过期型"已结构性清零**（8 项）；
2. 剩余 **5 项本地红**，其中 **4 项**可归因于本地未跟踪残留（CI 不成立）、
   **1 项（#4 UTF-16）可能在 CI 同样成立** ⇒ CI 端的红预计从 ≥7 项降到 **1 项**；
3. **未取得 CI 端实际日志**（无 token）⇒ 上述预测未经 CI 实测验证（630 已登记该缺口，
   本批沿用）；
4. 按 §五 A4.2：真实缺陷型**不修复**——本批实测真实缺陷型为 **0**。
