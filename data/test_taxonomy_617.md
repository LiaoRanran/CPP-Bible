# 测试分类 taxonomy（617 C1）

> 背景（外部评审 #3 / #4）：当前 215 个测试（tests/*.py）未显式分类，读者难辨「每个测试类证明什么」「覆盖率是否虚高」。本文件定义测试 taxonomy，并区分「真实验证测试」与「脚本/工具自测」。
> 机器可读分类映射见 C4（`tests/test_category_map.py`）；分类计数脚本见 C2。

## 一、测试类别定义（每类证明什么）
| 类别 | 证明对象 | 典型文件前缀 | 关键性 |
|---|---|---|---|
| **gate** | 63 条规则引擎正确性（命中/分级/冻结）| test_gate* | 核心 |
| **evidence** | EV-* 证据卡校验（schema/锚/哈希）| test_evidence* | 核心 |
| **poison** | 124 毒丸触发 + 规则覆盖（诚实口径）| test_poison* | 核心 |
| **replay** | atom↔evidence 重放一致（56 confirm）| test_replay* | 核心 |
| **mutation** | 变异测试基线（v7 1/1406 契约）| test_mutation* | 核心 |
| **independent_verification** | 他验接口/签名/VSA（616 D 原型）| test_independent* | 增量 |
| **statistics** | 置信序列/e-process/estimand（617 A）| test_confidence* / test_escape_rate* | 增量 |
| **tooling_integrity** | 工具 checksum 保护（22 项）| test_tool_integrity* | 支持 |
| **snapshot** | SNAPSHOT_MANIFEST 计数一致性（617 D2）| test_snapshot* | 支持 |
| **script_self_test** | 辅助脚本/CLI 自测（非验证断言）| test_*_script* | 元 |

## 二、真实验证测试 vs 脚本自测
- **真实验证测试**：gate / evidence / poison / replay / mutation / independent_verification / statistics / tooling_integrity —— 直接对「验证系统正确性」做断言，是逃逸率可信度的基础。
- **脚本自测 / 元测试**：snapshot / script_self_test —— 保障工具链自身不坏，不直接证明验证正确性。
- **防虚高原则**：对外报告「测试数」时须区分两者；覆盖率口径只计真实验证测试，不把脚本自测计入「验证覆盖」。

## 三、当前计数口径（取自 SNAPSHOT_MANIFEST_617.json）
- 总 tests/*.py = **213**（manifest live_counts.tests_py，2026-09-21 实测；README 写 183 ⇒ 漂移）。
- 精确分类计数由 C2 脚本扫描文件名前缀得出（留 C2 落地）；本文件仅定义类别与证明语义。

## 四、治理结论
1. 每个新增测试须归入上表一类，并在 docstring 注明「证明对象」。
2. 对外计数引用 SNAPSHOT_MANIFEST，禁止手写；覆盖率口径剔除 script_self_test。
3. 类别缺口（如 independent_verification 仅原型级）须在 PM 报告与交人项中显式标注。
