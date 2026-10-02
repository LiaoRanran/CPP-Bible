# OTS 占位登记（**不是时间戳证明**）—— 666 A1

- 目标：`data/supply_chain/merkle_roots.json`
- 当前台账 sha256：`2af745a9bb57f259d9475468b274d123bfafc22c8142ddcbaa5e17f2d0566e86`
- 同目录 `merkle_roots.json.ots`：666 A1 重新生成的**待上链占位凭据**
  （magic 与官方 `DetachedTimestampFile.HEADER_MAGIC` 一致，attestation 段为占位零）

## 这是什么 / 不是什么

- **是**：一条「台账内容 → 摘要」的可核验绑定（`ots_anchor_613 --check` 逐次复算）。
- **不是**：时间戳证明。它**没有**提交到任何 OTS 日历，因此不含 PendingAttestation，
  更没有比特币区块头证明 ⇒ 它不能证明「该台账在某时刻已存在」。

## 为什么现在是占位（诚实登记）

666 A1 重钉了 Merkle 台账（atoms 边界回填后根变化），因此 666 之前那份**真实**凭据
（含 finney.calendar.eternitywall.com 的 PendingAttestation）不再覆盖当前台账，
已归档为 `data/supply_chain/ots_archive/merkle_roots.json.<旧摘要前12>.ots`（证据保留）。

## 交人项（真正锚定需要人执行）

1. 装 `opentimestamps-client`（提供 `ots` 命令）；
2. `ots stamp data/supply_chain/merkle_roots.json`（提交到公开日历，需网络）；
3. 稍后 `ots upgrade merkle_roots.json.ots`（等日历聚合出比特币区块头证明）；
4. 重钉信任根：`python tools/tool_integrity.py --update`（本文件在 supply_chain 哈希面内）；
5. 完成后**删除本占位登记**（`test_ots_anchor_656` 的占位通道随之关闭，真锚判据自动生效）。

> 机器不得代办第 2 步：对公开日历发起提交是**对外副作用**且需网络；
> 本机实测 DNS 解析到基准测试网段（198.18.0.0/15）⇒ 无法真的上链。
