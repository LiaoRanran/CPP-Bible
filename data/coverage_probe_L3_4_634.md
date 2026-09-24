# 634 B1 · 探针 L3.4 解析器特性绕过

- risk：medium
- 防御载体：`tools/gate_engine.py`
- 机制信号：`YAML-HARDENING`
- **机制存在：✅**
- 说明：gate 规则 EV-FM-YAML-HARDENING（真实 PyYAML 复核）

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
