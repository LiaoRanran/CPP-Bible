# 历史 OTS 凭据（真实证明，666 A1 归档）

- 文件：`data/supply_chain/ots_archive/merkle_roots.json.c09ee380e15b.ots`（786 B）
- 覆盖摘要：`sha256:c09ee380e15ba46e20d4e1d44c4f808f15d8c32ffe484c0f1c82860824aa83cd`（= 666 重钉前那一版 `merkle_roots.json` 的内容）
- 布局：官方 `DetachedTimestampFile`（含 PendingAttestation，日历 URI 见文件尾部）
- **为何移出主位**：666 A1 重钉 Merkle 台账（atoms 边界回填后根变化）⇒ 该凭据不再覆盖
  当前台账；留在主位会让 `ots_anchor_613 --check` 报"摘要与当前信任根不一致"（这是真话音，
  不该被压掉，也不该伪装成仍然有效）。
- **不是删除**：证据保留在此。重新锚定当前台账需人执行
  `ots stamp data/supply_chain/merkle_roots.json`（需 opentimestamps-client + 网络），
  属 666 交人项。
