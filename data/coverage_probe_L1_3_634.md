# 634 B1 · 探针 L1.3 命题范围偷换

- risk：high
- 防御载体：`tools/atom_evidence_replay.py`
- 机制信号：`frontmatter|冻结|frozen`
- **机制存在：✅**
- 说明：replay 对 frontmatter 的冻结校验

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
