# 634 B1 · 探针 L8.2 签名投毒

- risk：high
- 防御载体：`tools/vsa_verify_628.py`
- 机制信号：`signature|hmac|verify`
- **机制存在：✅**
- 说明：vsa_verify_628 的 HMAC/签名复核

> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。
