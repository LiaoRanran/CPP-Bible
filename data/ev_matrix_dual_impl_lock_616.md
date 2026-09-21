# 616 B3 · EV-MATRIX 双实现一致性回归锁

> **用途**：未来改 `gate_engine.py` 后跑本工具，自动验证官方实现与独立第二实现的一致性。
> 官方侧 = `import gate_engine; check_evidence_matrix_backed()`（**单规则函数，非 `--check` 门禁**）。

## 一、当前一致性基线

- 适用卡（多编译器）：**19**；官方 UNBACKED：**16**
- 一致 **19** / 分歧 **0** ⇒ 一致率 **100.0%**
- 状态：**PASS**（阈值 ≥95%）

## 二、分歧卡（如有）

| 卡 | 官方 | 第二实现 v2 |
|---|---|---|
| （无） | — | — |

## 三、如何使用

1. 每次修改 `gate_engine.py`（尤其 `check_evidence_matrix_backed`）后，跑 `python tools/ev_matrix_dual_impl_lock.py`；
2. 一致率 < 阈值（95%）⇒ 状态 `fail`，**不一致即告警**；
3. 处理流程：**先分析原因**（是官方实现改了对、还是第二实现漏了预处理），再决定修官方还是修第二实现；
4. 修完重跑本工具 + 更新基线 `data/ev_matrix_dual_impl_baseline_616.json`。

## 四、边界

- 本工具**只对比**，不改任何实现；未跑 `gate_engine.py --check`。
- `import gate_engine` 只为取单规则函数（对比用途）；其模块级副作用为只读缓存（无写盘）。

