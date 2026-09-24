# 634 B1 · 探针 L3.3 字段注入

- risk：high
- 防御载体：`tools/gate_engine.py`
- 机制信号：`CONTROL|控制字符|YAML`
- **机制存在：✅**
- 说明：gate YAML 硬化 + 626 控制字符清洗

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
