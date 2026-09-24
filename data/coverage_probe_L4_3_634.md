# 634 B1 · 探针 L4.3 regex heuristic 绕过

- risk：high
- 防御载体：`tools/gate_engine.py`
- 机制信号：`heuristic|启发`
- **机制存在：✅**
- 说明：gate 规则内置的 regex/启发式判定

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
