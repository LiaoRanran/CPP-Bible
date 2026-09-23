# 628 A2 · PCK hash 漂移处置报告

- 处置证书：83 张（备份 83 张 → `data/pck_backup_628/`）
- 重算（content_drift）：**56** 条 hash 更新
- 补 hash（hash_absent）：**106** 条
- 需人审（ref_missing）：**2** 条——[{'cert': 'ATOM-HIST-AUTOPTR-001.pck', 'ref': 'evidence/hist/EV-MEM-003.md'}, {'cert': 'ATOM-HIST-AUTOPTR-001.pck', 'ref': 'evidence/hist/EV-MEM-003.md'}]
- 重算前 B2-R：27/83 → 重算后：**162/164 一致**
- **未判任何证书失效**：hash 重算是机械操作；"失效"是语义判断需人审
- **语义字段未动**：verdict/authorized/status/uncertainty 等与备份逐字段一致

## 回滚方法

```bash
cp data/pck_backup_628/*.yaml data/pck/certificates/
```
