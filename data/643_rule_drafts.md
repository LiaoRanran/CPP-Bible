# 643 D2 · 规则草案（智能层：自动提案规则 #2；**只出草案**）

> 草案 **10** 条（上限 10）；形态 `{'NEW': 1, 'MODIFY': 9}`；证据类型 `{'反例': 1, '静态盲点': 9}`。
> 来源：反例（可行动案例 **1** 条）+ 静态盲点（**44** 条候选，取前 10）。
> **默认 severity = `advice`**（从宽起步，A1-C4）；**未写入规则库**（`written_to_rule_db=False`）。

## 一、草案清单（按 priority 降序）

| # | 形态 | 拟用 id | 标题 | 触发条件 | 判定 | MDL bits | blast | 证据 | priority |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `NEW` | `ATOM-DRAFT-001` | 补：evidence/conc/EV-CONC-001.md 上的逃逸面（M1） | 卡 `evidence/conc/EV-CONC-001.md`；缺失面 = M1 | 命中即报（建议先 advice） | 464 | 卡1/规则0 | 反例 | 0.414 |
| 2 | `MODIFY` | `MOD-ATOM-DAL-MATCH` | 为 `ATOM-DAL-MATCH` 补「必备字段缺失即报」分支 | scope=atom；引用字段 dal, status | 字段缺失时**显式报告**（当前可能静默跳过） | 432 | 卡1/规则1 | 静态盲点 | 0.296 |
| 3 | `MODIFY` | `MOD-ATOM-GRAY-ZONE` | 为 `ATOM-GRAY-ZONE` 补「必备字段缺失即报」分支 | scope=atom；引用字段 domain | 字段缺失时**显式报告**（当前可能静默跳过） | 432 | 卡1/规则1 | 静态盲点 | 0.296 |
| 4 | `MODIFY` | `MOD-ATOM-ID-FORMAT` | 为 `ATOM-ID-FORMAT` 补「必备字段缺失即报」分支 | scope=atom；引用字段 id, type | 字段缺失时**显式报告**（当前可能静默跳过） | 432 | 卡1/规则1 | 静态盲点 | 0.296 |
| 5 | `MODIFY` | `MOD-ATOM-ID-UNIQUE` | 为 `ATOM-ID-UNIQUE` 补「必备字段缺失即报」分支 | scope=atom；引用字段 id, status | 字段缺失时**显式报告**（当前可能静默跳过） | 432 | 卡1/规则1 | 静态盲点 | 0.296 |
| 6 | `MODIFY` | `MOD-ATOM-FM-REQUIRED` | 为 `ATOM-FM-REQUIRED` 补「必备字段缺失即报」分支 | scope=atom；引用字段 sources | 字段缺失时**显式报告**（当前可能静默跳过） | 464 | 卡1/规则1 | 静态盲点 | 0.276 |
| 7 | `MODIFY` | `MOD-ATOM-NO-UNVERIFIED` | 为 `ATOM-NO-UNVERIFIED` 补「必备字段缺失即报」分支 | scope=atom；引用字段 status | 字段缺失时**显式报告**（当前可能静默跳过） | 496 | 卡1/规则1 | 静态盲点 | 0.258 |
| 8 | `MODIFY` | `MOD-ATOM-CLAIM-STRUCTURED` | 为 `ATOM-CLAIM-STRUCTURED` 补「必备字段缺失即报」分支 | scope=atom；引用字段 claim, id | 字段缺失时**显式报告**（当前可能静默跳过） | 544 | 卡1/规则1 | 静态盲点 | 0.235 |
| 9 | `MODIFY` | `MOD-ATOM-MISCONCEPTION-REF` | 为 `ATOM-MISCONCEPTION-REF` 补「必备字段缺失即报」分支 | scope=atom；引用字段 pedagogy | 字段缺失时**显式报告**（当前可能静默跳过） | 560 | 卡1/规则1 | 静态盲点 | 0.229 |
| 10 | `MODIFY` | `MOD-ATOM-MISCONCEPTION-LEVELS` | 为 `ATOM-MISCONCEPTION-LEVELS` 补「必备字段缺失即报」分支 | scope=atom；引用字段 pedagogy | 字段缺失时**显式报告**（当前可能静默跳过） | 608 | 卡1/规则1 | 静态盲点 | 0.211 |

## 二、逐条理由（可追溯）

1. `ATOM-DRAFT-001`（NEW）：provenance = `{"kind": "NEW", "case_id": "v7#0", "source": "B4", "card": "evidence/conc/EV-CONC-001.md", "op": "M1"}`
2. `MOD-ATOM-DAL-MATCH`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-DAL-MATCH", "check_fn": "check_dal_match", "fields": ["dal", "status"]}`
3. `MOD-ATOM-GRAY-ZONE`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-GRAY-ZONE", "check_fn": "check_atom_gray_zone", "fields": ["domain"]}`
4. `MOD-ATOM-ID-FORMAT`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-ID-FORMAT", "check_fn": "check_atom_id_format", "fields": ["id", "type"]}`
5. `MOD-ATOM-ID-UNIQUE`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-ID-UNIQUE", "check_fn": "check_atom_id_unique", "fields": ["id", "status"]}`
6. `MOD-ATOM-FM-REQUIRED`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-FM-REQUIRED", "check_fn": "check_atom_frontmatter", "fields": ["sources"]}`
7. `MOD-ATOM-NO-UNVERIFIED`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-NO-UNVERIFIED", "check_fn": "check_no_unverified_status", "fields": ["status"]}`
8. `MOD-ATOM-CLAIM-STRUCTURED`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-CLAIM-STRUCTURED", "check_fn": "check_atom_claim_structured", "fields": ["claim", "id"]}`
9. `MOD-ATOM-MISCONCEPTION-REF`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-MISCONCEPTION-REF", "check_fn": "check_misconception_ref", "fields": ["pedagogy"]}`
10. `MOD-ATOM-MISCONCEPTION-LEVELS`（MODIFY）：provenance = `{"kind": "MODIFY", "target_rule": "ATOM-MISCONCEPTION-LEVELS", "check_fn": "check_misconception_levels", "fields": ["pedagogy"]}`

## 诚实登记

1. **自动提案 ≠ 规则真的好**（§十二.3）：MDL/反涟漪通过**不代表规则正确**，必须人审；
2. **`expected_block_rate` 一律为 `None`**（本工具**不估**）：没有实测就没有数字，估了就是编（估计留 D4/E1 用实测填）；
3. **静态盲点类草案（MODIFY）是「软线索」**：C1 只证明「该规则引用了字段」，**没有**证明它缺「缺失即报」分支 ⇒ 证据权重只有反例的 1/3，且**必须逐条人读代码**后才能立项；
4. **反例类草案只有1 条**：因为 v7 的 9 条逃逸里 8 条是语义等价（能力天花板，不该自动化）⇒ 反例供给**天然稀薄**，这是实情不是漏做；
5. **排序公式含证据强度**（反例 3 / 静态 1）：刻意修掉 637 的「公式不含严重度/证据强度」型倒挂；
6. 本工具**只写侧车 JSON**：不动 `gate_engine.py`、不动现有 67 条规则。
