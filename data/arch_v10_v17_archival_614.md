# 614 G1 · _arch_v10–v17 调研目录归档记录

> 只读归档 + 引用核对；不删调研内容（仅移位）。时间 2026-09-21。

## 一、归档动作
- 目标：`_arch_v10` … `_arch_v17` → **`_archive/old_research/`**（保持原名）。
- 工具：逐目录 `git mv`（保留历史）。仓根仅保留最新两轮 **`_arch_v18` / `_arch_v19`**。
- 说明：`_arch_v2`…`_arch_v9` **此前已在** `_archive/old_research/`（本次续接），归档后仓根不再有 v10–v17。

## 二、逐目录（归档前文件数）
| 目录 | 批次 | 文件数 |
|---|---|---|
| _arch_v10 | 585 | 10 |
| _arch_v11 | 590 | 23 |
| _arch_v12 | 593 | 17 |
| _arch_v13 | 594 | 17 |
| _arch_v14 | 595 | 18 |
| _arch_v15 | 597 | 18 |
| _arch_v16 | 600 | 21 |
| _arch_v17 | 602 | 12 |
| **合计** | — | **136** |

## 三、引用核对（步骤 2/3）
- `References/00_导航/01_异族调研总索引_arch_v.md` 含 116 处 `_arch_v1[0-7]` 提及——经查为**编目表描述**（目录名/批次/主题/结论），**非路径链接**（无 `](_arch_v…/…)` 形式）。
- 已在索引顶部加**归档说明**：v2–v17 已入 `_archive/old_research/`，仓根仅留 v18/v19；各轮描述保留为历史编目。
- 其余引用点：`governance_doc_guard.py` 仅注释（示意 `_arch_v2…v17`，实际 glob=`_arch_*`，不影响）；`test_governance_auto_update_607.py` 用 tmp 目录、与真身无关；`data/governance_docs_manifest.json` 内的 `*arch_v1x*` 均为 `References/architecture_架构演进/` 下的**同名文档**（非根目录），不动。
- ⇒ 无硬编码路径断链。

## 四、治理台账更新（步骤 5/6）
- `governance_doc_guard.py update --force` → manifest 变更 **126 处**（移除 v10–v17 条目 + 吸收 v18/v19/614.md 等新文档），self_hash `cd324b8ef230…`。
- `scan` → high55 / medium186 / low38。
- `tool_integrity.py --update` 重钉（core5 + test_config2 + supply_chain5）。
- **`verify` exit 0**（manifest 一致 ✓）。

## 五、附带收益：既有 CI 漂移修好
- 归档+治理更新一并吸收 `_arch_v19/*`（并行会话新增、此前未入 manifest）⇒
  `tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` **转绿**（实测 exit 0）。
- ⇒ 全量 `pytest -m "not slow"` 的既有红灯**消除**。

## 六、信任根完整性
- `tool_integrity --update` 重建 Merkle 根，其摘要**仍为** `47c330c9…6e0db5`，与 `merkle_roots.json.ots` 内承诺**一致**（`ots verify` exit 0）⇒ 锚定绑定**未被破坏**。

## 七、边界
- 未删任何调研文件；仅移位。未改受控目录（atoms/evidence/Examples/Book）。
