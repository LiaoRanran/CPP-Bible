# 634 B1 · 探针 L7.2 模板化人审

- risk：high
- 防御载体：`tools/human_review_executor_625.py`
- 机制信号：`reason|模板|boilerplate`
- **机制存在：✅**
- 说明：human_review 的 reason 统计（模板化检出）

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
