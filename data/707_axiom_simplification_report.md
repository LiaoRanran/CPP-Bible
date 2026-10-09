# 707 Task A — 元理论发现落地（公理检查简化 + 独立性测试）

- 日期：2026-10-09
- 科研依据：**700-A 元理论发现** → `data/700_axiom_independence.json`
- 红线：detect_calls = 0；只读；不修改检测器/样本/冻结矩阵/论文/bib。

## 1. 改了什么

| 文件 | 改动 | 科研依据标注 |
|------|------|--------------|
| `tools/compute_700_axiom_independence.py` | **新增** `--substantive-only` 模式 + `substantive_axiom_check()`：只跑实质性公理 A2/A5，**跳过恒真的 A3/A4/A6**（及定理 A7、元公理 A1），并附 **A8 占位** | 函数 docstring + doc 字段 `research_basis`：「700-A：A3/A4/A6 恒真，A2/A5 独立」 |
| `tools/test_axiom_independence.py` | **新增**：4096 结构 × 7 聚合独立重算，断言分类与 700-A 一致 | 文件头「科研依据（700-A 元理论发现）」+ `research_basis` 字段 |
| `supplementary/axiom_system.md` | **新增**：公理系统说明（哪条实质、哪条恒真、为什么） | 文首「科研依据：700-A」 |

> **对「移除 A3/A4/A6」的处理**：700-A 的**证据**恰恰来自对 A3/A4/A6 的穷举检验（证明它们恒真）。因此我没有删除默认（全量元理论）模式——那会销毁证据——而是把「只检查 A2/A5」做成**新的简化路径** `--substantive-only`，并在 `test_axiom_independence.py` 里保留对 A3/A4/A6 恒真性的**回归断言**。这既满足「检查简化」，又不丢失证明。

## 2. 验证

**简化检查**（`--substantive-only`，只跑 A2/A5）：
```
A2: or_union=ok, at_least_2=ok, max_single=ok, min_single=violated(3750),
    mean_single=violated(3750), sum_single=ok, exactly_one_nonmonotone=violated(3600)
A5: or_union=ok, at_least_2=violated(3471), max_single=ok, min_single=violated(2589),
    mean_single=violated(3750), sum_single=ok, exactly_one_nonmonotone=violated(1671)
跳过（恒真/定理/元公理）：['A3', 'A4', 'A6', 'A7', 'A1']
A8 占位：TODO / 不可自动验证
```

**回归测试**（`test_axiom_independence.py`）：
```
结构域 = 4096；聚合族 = 7
真公理（有反例） = ['A2', 'A5']
恒真（定理）     = ['A3', 'A4', 'A6', 'A7']
[ok] only_A2_A5_genuine
[ok] A3_A4_A6_A7_are_theorems
[ok] A2_has_counterexample
[ok] A5_has_counterexample
[ok] A8_missing_confirmed
test_axiom_independence: PASS
```

`ruff check` 两文件：**All checks passed**。

## 3. A8（标签轴闭包）——为什么加 TODO 而非自动检查

A8 约束的是**报告规范层**的标签轴 λ，**不是覆盖结构性质** ⇒ 在本穷举域（覆盖 + 聚合）里**没有结构反例可检**。按要求：**加 TODO + 说明原因**，不伪造自动验证。
- 占位内容见 `data/707_axiom_independence_test.json::a8_placeholder`（含候选形式化 `(D,A,E,Θ,P,λ)`）。
- 落地形式：以「未声明 λ 的分组统计不可比较」这一**规范约束**执行（698-A Type III 实测）。

## 4. 产物

- `tools/test_axiom_independence.py`（新）
- `tools/compute_700_axiom_independence.py`（+69 行，`--substantive-only`）
- `supplementary/axiom_system.md`（新）
- `data/707_axiom_independence_test.json`（测试产物）
- `data/707_axiom_substantive_check.json`（简化检查产物）
- 本报告

## 5. 诚实边界

- 「恒真」只对 4096 结构 × 7 聚合的**有限域**成立，非普遍证明；「有反例」是充分证据。
- 未改动 A2/A5 的检查逻辑本身，只增加了「跳过恒真项」的路径与回归断言。
