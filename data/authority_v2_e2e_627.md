# 627 B1 · feature flag 端到端验证报告

- flag：`QUEYI_AUTHORITY_V2`
- **V2 模式 5 种投影全部成功**：True

| 投影 | V2 状态 | V2 摘要 | V1 参照 |
|---|---|---|---|
| w2 | ok | `{"IN": 484, "OUT": 35, "UNDEC": 0}` | legacy_grounded_labels |
| pck | ok | `{"count": 83, "strict_authorized": 0, "relaxed_authorized": 0, "delta_relaxed_mi` | legacy_pck_certificates |
| golden | ok | `{"warn_disposition_events": 0, "accepted_legacy": 0, "accepted_legacy_events": [` | v2_only |
| dashboard | ok | `{"v2_enabled": true, "review_items_unique": 93, "review_items_records": 93, "by_` | v2_only |
| textbook | ok | `{"atom_id": "ATOM-CONC-FENCE-001", "render_state": "ABSTAIN", "pck_status": "pen` | v2_only |

## 诚实说明

- 626 编译器内部 `v2_enabled()` **未真正接入**编译函数：无论 flag 开/关都走 Authority 路径（本工具实测确认）。
- 因此「V1 vs V2」的真实差异体现在 **V2 输出 vs legacy 数据源**：
  - W2：V2(626 编译器, 519 节点) vs legacy(grounded_labels, 121 节点) 的粒度差异已在 627 A1 单独对账（归一化后 diff=0）。
  - PCK：V2 投影 vs legacy 证书四层验证结果（详见 627 A3）。
  - golden/dashboard/textbook 为 V2 原生，无 legacy 等价物。
- **结论**：feature flag 的「开关机制」可用且 5 种投影在 V2 下全部正常；但 flag 尚未产生行为分支——建议 627+ 将 V1 接回 legacy 数据源以实现真正双模。
