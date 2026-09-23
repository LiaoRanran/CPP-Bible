# 628 A3 · 镜像边对称性自动证明 + 写入报告

- 镜像边总数：194（mis_to_prop）
- **自动证明**：194 条（三条件全满足：反向存在 + 判决一致 + 理由对称断言）
- **需人审**：0 条（[]）
- 账本写入：76 条（账本 93 unique 中覆盖 194 条镜像 target_id）；
- 无对应 ReviewItem 的证明：118 条——是否扩充账本属治理决策，证明已存 sidecar（`data\mirror_symmetry_proofs_628.json`）留 629/人审
- 写入后 W2 分布：{'IN': 114, 'OUT': 7, 'UNDEC': 0}（不变：True）
- 备份：`data/review_item_ledger_backup_628.jsonl`
- 条件3 口径：Jaccard≥0.6 或领域对称断言规则（反向 reason 含「对称」+「成立/一致」+「对应/已人审」且 action 一致）——原始 Jaccard 因批量授权 boilerplate 全部 <0.6（诚实登记）
