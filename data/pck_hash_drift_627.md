# 627 A3 · PCK evidence.hash 漂移根因分析

- 扫描证书：**83** 张
- **content_drift（hash 不符）**：56 张
- **hash_absent（无 hash 字段）**：26 张
- **ref_missing（引用失效）**：2 条

## 根因子分布（content_drift 子类）

- `content_changed`: 56

## 处置建议

- content_drift·真实变更：重新签发 / 重算 / 标记 stale（**需人裁决**）
- content_drift·行尾/编码：规范化后重算 hash（低风险）
- hash_absent：补算 hash 后重新签发
- ref_missing：修正 ref 或标记 stale

> 本工具**只分析不执行**；是否接受漂移由人裁决（626 交人项 #6）。
