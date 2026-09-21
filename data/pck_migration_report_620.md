# 620 B2 · 全量 PCK 证书迁移报告（83 张）

> 工具：`tools/pck_batch_migrator_620.py --all`
> 输出目录：`data/pck/certificates/{CARD_ID}.pck.yaml`
> 来源：只读派生 `atoms/`（27 张原子卡）+ `evidence/`（56 张证据卡）
> 验证器：619 B2 `pck_certificate_verifier_619.py`

---

## 一、迁移统计

| 指标 | 值 |
|---|---|
| 自动发现卡数 | **83**（原子 27 + 证据 56） |
| 成功生成 | **83** |
| 失败 | **0** |
| B2 验证通过 | **83 / 83（100%）** |
| B2 验证失败 | 0 |
| 工具退出码 | 0 |

**结论**：全量 83 张证书全部生成且全部通过 B2 结构诚实性校验。

---

## 二、字段完整度统计（7 个字段）

| 字段 | 完整数 | 完整率 | 判定口径 |
|---|---|---|---|
| `claim.statement` | 83 / 83 | **100%** | 非空且非「退回卡路径」占位 |
| `evidence` | 83 / 83 | **100%** | 非空且非 `(见 claim_structured.evidence)` 占位 |
| `negative_tests` | 83 / 83 | **100%** | 来自 v7 baseline 真实 `results[]`，非空 |
| `provenance.commit` | 83 / 83 | **100%** | git 反查成功（非 `unknown`） |
| `uncertainty` | 83 / 83 | **100%**（结构） | 但为**全局** estimand L1，卡内无本地置信字段 |
| `human_authority.status = approved` | **23 / 83** | **27.7%** | 其余 60 张为 `pending` |
| `provenance.first_authorized_at` | **26 / 83** | **31.3%** | 其余 57 张为 `unknown` |

### 按卡类型拆分 `human_authority.status`

| 类型 | approved | pending | 通过率 |
|---|---|---|---|
| 原子卡（27） | 23 | 4 | 85.2% |
| **证据卡（56）** | **0** | **56** | **0%** |

> **诚实发现**：**全部 56 张证据卡的 frontmatter `status` 均非 `verified*`**
> （实测多为 `draft`），因此其 `human_authority.status` 一律派生为 `pending`。
> 这不是迁移工具的缺陷，而是**证据卡本身尚未走完验证流程**的真实反映。

---

## 三、与 619 的 10 张试点对比

| 维度 | 619 B3 试点（10 张） | 620 B2 全量（83 张） | 变化 |
|---|---|---|---|
| 卡来源 | 硬编码 `PILOT_CARDS` 列表 | **自动发现**（ATOM-*.md + EV-*.md） | 从试点 → 全量 |
| B2 验证 | 10 / 10 PASS | **83 / 83 PASS** | 结论可外推 |
| `human_authority approved` | 4 / 10（40%） | 23 / 83（27.7%） | 全量口径下**更低** |
| `first_authorized_at` 已知 | 4 / 10（40%） | 26 / 83（31.3%） | 全量口径下更低 |

**解读**：试点 10 张是**精选**的（含 5 张已 verified 原子卡），完整率偏高；
全量 83 张纳入 56 张 `draft` 证据卡后，真实完整率显著下降。
⇒ **试点的 40% 不代表全量水平**，全量真实水平是 ~28%。这正是做全量迁移的价值。

---

## 四、缺失最严重的字段 Top 5

| # | 字段 | 缺失数 / 83 | 缺失率 | 说明 |
|---|---|---|---|---|
| 1 | `uncertainty`（卡内**本地**置信字段） | 83 | 100% | 全部引用**全局** estimand L1=0.9062%，卡内无本地 CS |
| 2 | `review_method`（逐条独立审阅） | 83 | 100% | 全部为 `batch_authorization`（615 诚实审计结论） |
| 3 | `verifiers` ≥ 2 | 83 | 100% | 全部仅 1 个（gate_engine）⇒ `verifier_disagreement` N/A |
| 4 | `human_authority.status = approved` | 60 | 72.3% | 含全部 56 张证据卡 |
| 5 | `provenance.first_authorized_at` | 57 | 68.7% | 卡内无 `verified_at` 字段 |

---

## 五、需要人补全的卡清单

### 5.1 `human_authority` 待补（pending，60 张）

- **全部 56 张证据卡**（status 为 `draft`，需走完验证流程）
- 原子卡 4 张：
  - `atoms/lang/ATOM-LANG-INLINE-001.md`
  - `atoms/mem/ATOM-MEM-ALLOC-002.md`
  - `atoms/mem/ATOM-MEM-LEAK-002.md`
  - `atoms/mem/ATOM-MEM-PERF-004.md`

### 5.2 `first_authorized_at` 待补（unknown，57 张）

- 56 张证据卡 + `atoms/lang/ATOM-LANG-INLINE-001.md`
- 补全方式：卡内补 `verified_at` 字段（属**改受控目录**，620 不做，留人/621）

### 5.3 结构性缺口（全部 83 张，非单卡可补）

- 卡内本地 `uncertainty`（需 per-card CS 估计）
- 第二个独立 verifier（需 B 线后续建设）
- 逐条独立人审（当前全为 batch_authorization）

---

## 六、硬边界遵守

- ✅ **未修改任何原始 markdown 卡**（只读 frontmatter）
- ✅ 缺失字段如实标 `null` / `unknown`，未编造
- ✅ `negative_tests` 全部来自 v7 baseline 真实 `results[]`
- ✅ verdict 不在 B2 允许域的 negative test 已如实丢弃并登记
  （本次实测：**丢弃 0 条**，v7 的 verdict 均落在 allowed 域内）
- ✅ 输出写在 `data/pck/certificates/`（非受控目录）
