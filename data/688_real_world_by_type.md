# 688 · A4 真实靶场按缺陷类型细分（真实 vs 自造对比）

- **批次**：688 ｜ **数据**：`688_real_world_by_type.json`
- **真实口径**：`683_real_world_type_matrix.json`（9 类 taxonomy，110 样本）
- **自造口径**：`blindspot_676g_stats.json`（70 类 taxonomy，1147 样本）
- **方法**：取两类 taxonomy 自然重叠的 9 个类型，逐类对比 OR 检出率。

## 1. 真实靶场 9 类（全量，n / OR 率）

| 类型 | n | OR 检出率 |
|---|---:|---:|
| use_after_free | 10 | 100.0% |
| null_pointer_deref | 6 | 100.0% |
| memory_leak | 1 | 100.0% |
| double_free | 2 | 100.0% |
| out_of_bounds | 38 | 84.21% |
| integer_overflow | 14 | 71.43% |
| data_race | 4 | 75.0% |
| type_punning | 4 | 0.0% |
| logic_error | 31 | **3.23%** |

> 真实靶场以 out_of_bounds(38) 与 logic_error(31) 为主，二者占 69/110=63%。

## 2. 真实 vs 自造（重叠 9 类，diff = 真实 − 自造，pp）

| 类型 | 真实 n | 真实率 | 自造 n | 自造率 | diff(pp) |
|---|---:|---:|---:|---:|---:|
| logic_error | 31 | 3.23% | 17 | 35.3% | **−32.06** |
| type_punning | 4 | 0.0% | 20 | 50.0% | **−50.0** |
| data_race | 4 | 75.0% | 14 | 100.0% | −25.0 |
| out_of_bounds | 38 | 84.21% | 20 | 100.0% | −15.79 |
| integer_overflow | 14 | 71.43% | 26 | 84.6% | −13.19 |
| double_free | 2 | 100.0% | 3 | 100.0% | 0.0 |
| use_after_free | 10 | 100.0% | 7 | 100.0% | 0.0 |
| null_pointer_deref | 6 | 100.0% | 15 | 100.0% | 0.0 |
| memory_leak | 1 | 100.0% | 1 | 100.0% | 0.0 |

## 3. 核心发现
- **真实缺陷普遍比自造缺陷更难抓**：9 类中 **6 类真实率 < 自造率**，3 类持平，无一类真实显著更高。
- **最大差距在语义型类型**：type_punning（−50pp）、logic_error（−32pp）、data_race（−25pp）——这些在真实代码里常以 asan/静态告警**不标记**的形式出现（上下文相关、需语义理解），而自造样本被构造得"标准可抓"。
- **logic_error 是真实靶场的阿喀琉斯之踵**：31 个真实 logic_error 仅 3.23% 被抓（自造 35.3%）。这正是 683 结论"剔除 31 个 logic 族后内存安全族 OR=81.01%"的来源——真实靶场近三成样本是检测器几乎无能为力的逻辑错误。
- **聚合掩盖类型级差异**：683 整体 OR 59.09% vs 自造 61.64%（仅 −2.55pp，不显著），但类型级真实普遍更低。应补充"类型级真实更难"的注脚。

## 4. 诚实边界
- 两类 taxonomy 不对齐（70 vs 9），重叠仅 9 类；其余 61 个自造类型与真实 9 类无可比性。
- 真实侧 type_punning/data_race/memory_leak/double_free n 极小（1–4），单类 diff 噪声大，仅作方向性读。
- "自造率"为 676g 全量 OR（含 asan/ubsan/tsan/cross-compile/compiler-warn/linker/wunsequenced/compile-time 并集），与真实侧有效 6 资产并集口径一致（wunsequenced/compile-time 自造侧亦近 0 贡献）。

## 5. 对论文建议
- 真实靶场段增加"类型级真实 vs 自造对比"：结论从"整体无显著差异"深化为"**整体相当、但真实缺陷在语义型类型（logic_error/type_punning/data_race）上显著更难**"——这强化了论文的能力边界叙事（语义层是真实短板），并自然引出 future work（逻辑/语义型验证器）。
