# 619 A3 · VFDR 状态机 v1（漏洞反馈驱动修复）

## 一、状态机定义
- 状态集：`OPEN → TRIAGED → FIXING → VERIFYING → CLOSED`
- 转移表：

| 当前状态 | 事件 | 下一个状态 |
| OPEN | TRIAGE | TRIAGED |
| TRIAGED | START_FIX | FIXING |
| FIXING | FIX_SHIPPED | VERIFYING |
| VERIFYING | VERIFY_PASS | CLOSED |
| VERIFYING | VERIFY_FAIL | FIXING |
| CLOSED | REOPEN | FIXING |

> 闭环：VERIFY_FAIL 退回 FIXING 重修；CLOSED 可 REOPEN 回 FIXING（回归则重开）。

## 二、三历史教训复盘（种子漏洞，演示闭环）
### VFDR-585 · 红队：meta 攻击面缺口（供应链溯源 / 信任根 / Merkle 证明）
- 来源：`REDTEAM` · 严重度：`critical`
- 教训：验证系统未覆盖三层 meta 攻击：依赖链投毒、信任根缺失、证明树被篡改。
- 修复落点（历史真实）：601 supply_chain.py / merkle_integrity.py + 614 trust_root_status_check（in-toto HMAC / OTS / Merkle proof 三链）
- VFDR 闭环：OPEN `TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS` → **CLOSED** （路径：`OPEN → TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS`）

### VFDR-615 · EV-MATRIX 规则误报（双实现一致率仅 68.4%）
- 来源：`MATRIX` · 严重度：`high`
- 教训：ev_matrix_unbacked 单实现与 gate_engine 隐性剥字段（artifact_sha256 行），导致 31.6% 分歧 = 误报/漏报。
- 修复落点（历史真实）：616 ev_matrix_unbacked_v2.py（独立语义）+ ev_matrix_dual_impl_lock.py（双实现锁 100%）
- VFDR 闭环：OPEN `TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS` → **CLOSED** （路径：`OPEN → TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS`）

### VFDR-616 · CP 置信偷看（e-process 之前置信序列被反复偷看）
- 来源：`STATS` · 严重度：`high`
- 教训：置信序列在「看结果后」反复调参，虚报逃逸率 13.80%；统计偷看夸大确定性。
- 修复落点（历史真实）：616 confidence_sequence.py（Beta-混合 e-process，anytime 0.9062% vs CP 0.3370%；偷看虚报归零）
- VFDR 闭环：OPEN `TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS` → **CLOSED** （路径：`OPEN → TRIAGE → START_FIX → FIX_SHIPPED → VERIFY_PASS`）

## 三、与 A1/A2 的前向链路（留 620）
- A2 的 `ranked` Top20 排序 → 可自动开 `VFDR-*` OPEN 条目（按 A1 子目标分类：
  `rule_blind_spot→MATRIX` / `provenance→REDTEAM` / `verdict_regime_disagreement→GOV`）。
- 闭环闸门：`VERIFY_PASS` 须由**真实门禁**（gate + replay，非攻击方自评）确认，
  与 619 §六「不跑监工门禁」一致：A3 只设计机，不自行宣布修复通过。

## 四、已知限制
- 状态机是**确定性骨架**，不含时间/人审判定；真实 `REOPEN` 由人/CI 触发。
- 三历史教训已 CLOSED（修复已落历史批次）；本机只做**结构闭环演示**，不重新执行其修复。
