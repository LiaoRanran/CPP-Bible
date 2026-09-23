# 628 B3 · 透明日志报告（他验三件套 #3）

- 日志：`data/transparency_log.jsonl`（append-only）
- 当前状态：**20 条**，链完整：True
- 最早条目：2026-09-23T03:01:32Z · 最新条目：2026-09-23T04:34:40Z
- 日志引用凭证文件完整性：True（missing=[] / drifted=[]）
- 未入册凭证：无
- 尾部凭证存在性：True（index=19）
- 追加幂等：同一凭证（相同 sha256）重复追加为 no-op（不新增条目）

## 设计说明

- 结构：线性哈希链——`entry_hash = sha256(除 entry_hash 外全字段)`，
  `prev_log_hash` 指向上一条 entry_hash，首条 prev=GENESIS。
- **append-only**：追加只写文件末尾；任何历史条目的修改/删除都会使其后所有 prev_log_hash/entry_hash 校验失败。
- 与 Rekor v2 对比：本项目用简单哈希链而非 Merkle tree——单用户阶段日志量小（几十条），线性链足够；Merkle 优势在百万条级。
- 不 import 613/625 的 Merkle/OTS 工具（保持独立性），自实现哈希链。

## 局限性（诚实）

- 日志存储在本地，**没有外部见证者**。真正的透明日志需要外部可审计
（如推送到公开 Rekor 实例），留后续批次。
