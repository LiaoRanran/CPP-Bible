# 693-E2 · 缺陷类型深度分析报告

- 生成：2026-10-08T21:10:47+08:00｜脚本：`tools/analyze_693_defect_types.py`
- 数据源：`blindspot_676g_detection_matrix.json`（1147 样本 × 8 资产，**已冻结**）、
  `692_environment_paired_experiment.json`（资产划分）、`692_llm_audit_raw.jsonl`（LLM 逐条）
- **`detect_calls` = 0**（本报告只读已有产物，符合红线 8）
- 类型数：**34**（34 项闭集中的在用子集）

## 1. 可检测性排序（按盲区率降序，Top 15）

| # | 缺陷类型 | n | 盲区% | OR 检出% | 条件 recall% |
|---:|---|---:|---:|---:|---:|
| 1 | `cross_tu_ub` | 7 | **100.0** | 0.0 | — |
| 2 | `strict_aliasing` | 15 | **100.0** | 0.0 | — |
| 3 | `uninitialized_read` | 20 | **100.0** | 0.0 | — |
| 4 | `volatile_misuse` | 28 | **92.9** | 7.1 | — |
| 5 | `endianness` | 28 | **89.3** | 10.7 | — |
| 6 | `deadlock` | 65 | **84.6** | 15.4 | 100.0 |
| 7 | `algorithm_misuse` | 35 | **77.1** | 22.9 | 100.0 |
| 8 | `logic_error` | 35 | **74.3** | 25.7 | 100.0 |
| 9 | `interrupt_safety` | 20 | **65.0** | 35.0 | — |
| 10 | `virtual_function` | 30 | **60.0** | 40.0 | 100.0 |
| 11 | `linker_odr` | 24 | **58.3** | 41.7 | 100.0 |
| 12 | `condition_variable` | 30 | **56.7** | 43.3 | 100.0 |
| 13 | `atomic_ub` | 65 | **53.8** | 46.2 | 96.0 |
| 14 | `memory_order` | 42 | **50.0** | 50.0 | 100.0 |
| 15 | `move_semantics` | 30 | **50.0** | 50.0 | 100.0 |

> **读法**：盲区率 = 八资产全部 `miss` 的比例。盲区率高的类型**不是标注错误**，
> 而是「现有检测器对这类缺陷没有观测手段」的量化证据。

## 2. 资产必要性（全局：去掉该资产会损失多少 catch）

| 资产 | 损失 catch 数 |
|---|---:|
| `asan` | **139** |
| `tsan` | **85** |
| `ubsan` | **83** |
| `compiler-warn` | **53** |
| `cross-compile` | **14** |
| `linker` | **10** |

> `linker` 的损失数很小但**不为 0** —— 与 676l 的结论一致：**低边际但不可替代**
> （它的 catch 全部落在 sanitizer 的 `unknown` 里）。

## 3. 环境敏感性（E1 六资产 vs E2 三资产，按类型）

| 缺陷类型 | n | E1 catch% | E2 catch% | Δpp |
|---|---:|---:|---:|---:|
| `data_race` | 23 | 95.7 | 0.0 | **95.7** |
| `null_pointer_deref` | 26 | 100.0 | 7.7 | **92.3** |
| `use_after_free` | 25 | 100.0 | 8.0 | **92.0** |
| `memory_safety` | 11 | 100.0 | 9.1 | **90.9** |
| `memory_leak` | 28 | 89.3 | 7.1 | **82.1** |
| `double_free` | 15 | 86.7 | 6.7 | **80.0** |
| `smart_pointer` | 30 | 90.0 | 10.0 | **80.0** |
| `integer_overflow` | 61 | 93.4 | 23.0 | **70.5** |
| `alignment` | 27 | 70.4 | 7.4 | **63.0** |
| `iterator_invalidation` | 35 | 62.9 | 2.9 | **60.0** |
| `stl_container_ub` | 35 | 91.4 | 34.3 | **57.1** |
| `out_of_bounds` | 92 | 90.2 | 35.9 | **54.3** |
| `other_ub` | 72 | 86.1 | 31.9 | **54.2** |
| `memory_order` | 42 | 50.0 | 0.0 | **50.0** |
| `type_punning` | 23 | 52.2 | 8.7 | **43.5** |
| `raii_violation` | 31 | 61.3 | 19.4 | **41.9** |
| `atomic_ub` | 65 | 46.2 | 7.7 | **38.5** |
| `interrupt_safety` | 20 | 35.0 | 0.0 | **35.0** |
| `condition_variable` | 30 | 43.3 | 10.0 | **33.3** |
| `string_ub` | 35 | 88.6 | 62.9 | **25.7** |

> **关键限定**：E2 的 catch 只统计**真实运行过**的 3 个资产；缺失的 3 个 sanitizer
> **不计为 miss**。因此 E2 的「负例」不可信（692 已量化：46.95% 的 E2 负例其实抓得到）。

## 4. 独苗资产分布

| 缺陷类型 | n | 独苗总数 | 独苗落在哪 | 多资产共抓 | 全无 |
|---|---:|---:|---|---:|---:|
| `integer_overflow` | 61 | 39 | `ubsan`×39 | 18 | 4 |
| `other_ub` | 72 | 38 | `ubsan`×12、`compiler-warn`×11、`asan`×8、`tsan`×4、`cross-compile`×2、`linker`×1 | 24 | 10 |
| `smart_pointer` | 30 | 24 | `asan`×24 | 3 | 3 |
| `atomic_ub` | 65 | 23 | `asan`×11、`tsan`×9、`cross-compile`×1、`ubsan`×1、`compiler-warn`×1 | 7 | 35 |
| `memory_leak` | 28 | 23 | `asan`×23 | 2 | 3 |
| `out_of_bounds` | 92 | 21 | `asan`×19、`ubsan`×1、`compiler-warn`×1 | 62 | 9 |
| `data_race` | 23 | 20 | `tsan`×20 | 2 | 1 |
| `memory_order` | 42 | 19 | `tsan`×18、`asan`×1 | 2 | 21 |
| `alignment` | 27 | 17 | `ubsan`×16、`asan`×1 | 2 | 8 |
| `raii_violation` | 31 | 17 | `asan`×11、`compiler-warn`×5、`ubsan`×1 | 2 | 12 |
| `condition_variable` | 30 | 10 | `tsan`×10 | 3 | 17 |
| `double_free` | 15 | 10 | `asan`×10 | 3 | 2 |
| `linker_odr` | 24 | 10 | `linker`×9、`asan`×1 | 0 | 14 |
| `register_ub` | 20 | 10 | `compiler-warn`×9、`tsan`×1 | 1 | 9 |
| `logic_error` | 35 | 9 | `compiler-warn`×6、`cross-compile`×2、`tsan`×1 | 0 | 26 |
| `move_semantics` | 30 | 9 | `compiler-warn`×9 | 6 | 15 |
| `stl_container_ub` | 35 | 9 | `cross-compile`×4、`tsan`×3、`asan`×2 | 23 | 3 |
| `string_ub` | 35 | 9 | `cross-compile`×5、`asan`×3、`tsan`×1 | 22 | 4 |
| `algorithm_misuse` | 35 | 8 | `asan`×8 | 0 | 27 |
| `deadlock` | 65 | 8 | `tsan`×7、`ubsan`×1 | 2 | 55 |

## 5. LLM vs sanitizer 分歧率（按类型）

| 缺陷类型 | LLM 样本数 | 分歧数 | 分歧% | san catch→LLM miss | san miss→LLM catch |
|---|---:|---:|---:|---:|---:|
| `bit_operation` | 1 | 1 | **100.0** | 0 | 1 |
| `endianness` | 4 | 3 | **75.0** | 0 | 3 |
| `iterator_invalidation` | 4 | 3 | **75.0** | 0 | 3 |
| `volatile_misuse` | 6 | 3 | **50.0** | 0 | 3 |
| `algorithm_misuse` | 3 | 0 | **0.0** | 0 | 0 |
| `alignment` | 1 | 0 | **0.0** | 0 | 0 |
| `memory_safety` | 3 | 0 | **0.0** | 0 | 0 |

> 仅统计被 692-C 抽中的 80 条（跨 2 模型 × 2 prompt 多数票）。
> `san catch→LLM miss` 表示**实测抓到了但 LLM 说没抓到**（LLM 保守）；
> `san miss→LLM catch` 表示**实测没抓到但 LLM 说抓到了**（LLM 乐观，或标签可疑）。

## 6. 单检测器表重算 + 与 676l 的陈旧性交叉核对（**重要发现**）

用**当前冻结标签**（expected catch 640 / miss 507）重算：

| 资产 | TP | FN | FP | TN | unknown | recall%（重算） | recall%（676l 已发布） | Δpp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `asan` | 389 | 242 | 19 | 487 | 10 | **61.65** | 58.5 | +3.15 |
| `ubsan` | 254 | 377 | 16 | 490 | 10 | **40.25** | 38.2 | +2.05 |
| `tsan` | 240 | 391 | 23 | 483 | 10 | **38.03** | 36.09 | +1.94 |
| `compiler-warn` | 129 | 511 | 14 | 493 | 0 | **20.16** | 19.14 | +1.02 |
| `cross-compile` | 102 | 517 | 20 | 470 | 38 | **16.48** | 15.62 | +0.86 |
| `linker` | 9 | 631 | 1 | 506 | 0 | **1.41** | 1.34 | +0.07 |

- 676l 声明的 ground truth：catch **674** / miss 473
- 当前冻结矩阵：catch **640** / miss 507
- 差 = **-34** 条，正是 676m 修正的 34 条挂起样本
- **陈旧判定：是（需要重算）**

> 676l 的表在 **676m 标签修复之前**生成，其 ground truth 为 catch 674 / miss 473；当前冻结矩阵为 catch 640 / miss 507（差 34 = 676m 修正的 34 条挂起样本）。TP/FP/TN 逐位不变，只有 FN 与分母变了 ⇒ recall 列系统性偏低 1.4–3.2pp。
>
> ⇒ **`data/676l_单检测器性能报告.md` 未在 676m 标签修复后重算**；
> 论文若引用其 recall 列（asan 58.5% / ubsan 38.2% / …），应改用上表的重算值。
> TP / FP / TN 逐位不变，**结论方向不变**，但幅度需更新。

## 7. 口径纪律

- OR 口径分母 = 该类全部样本（含 unknown）；条件 recall 分母 = expected_verdict==catch。
- E2（3 资产）的 catch 只统计真实运行过的资产，缺失资产不计为 miss ⇒ 负例不可信。
- asset_necessity[asset] = 去掉该资产后本类损失的 catch 数（不是独苗数）。
- LLM 分歧用跨 2 模型 × 2 prompt 的多数票；平票记 tie 且不计入分歧分子。
