# 619 B1 · PCK（Proof-Carrying Knowledge）证书 schema v1

> 来源：37 号路线图 雷4（信任根结构）。本文件**只定义 schema**，不生成证书（B3 做）。
> 口径：619 §五/§六（不改受控目录、不跑门禁）。`mutation_id` 沿用 A1/A2 的 `(card, op, point)` 三元组（v7 无稳定 id）。

## 一、设计原则

1. **诚实优先**：所有「暂无」的字段（如 `verifiers` 只有 gate、`human_authority.review_method` 实为 `batch_authorization`）必须**显式登记**，不得填 0 或编造。
2. **可被 B2 验证**：每个字段声明 `required/optional` 与类型；B2 按本表做结构校验。
3. **与现有 markdown 卡可映射**：字段尽量对齐 `atoms/*.md` / `evidence/*.md` frontmatter（映射见 §三）。
4. **可逐张独立校验**：一张 certificate 对应一张卡（atom 或 evidence），是信任根的「便携凭证」。

## 二、schema 字段表

```yaml
schema_version: "619-pck-v1"            # 必填 · string · 守卫版本漂移
claim:                                 # 必填 · object
  id: "ATOM-CONC-FENCE-001"            # 必填 · string · = 卡 frontmatter.id
  statement: "..."                     # 必填 · string · = 卡 claim / hypothesis
  domain: "conc"                       # 必填 · string · = 卡 domain
  type: "inference"                     # 必填 · enum · inference|observation（对齐 claim_type）
evidence:                              # 必填 · 非空 array
  - type: "replay"                      #   enum · replay|artifact|url|standard
    ref: "evidence/conc/EV-CONC-001.md" #   引用（卡内 serves[] 反向边；evidence 本身无 evidence[] 数组）
    hash: "sha256:..."                  #   可选 · 当前卡仅 artifact_sha256 覆盖主工件
negative_tests:                        # 可选 · array（机制级 negative_controls 或 M1–M7 级）
  - mutation_id: "EV-CONC-001|M1|删 negative_controls"  # (card,op,point) 三元组
    result: "blocked"                   #   enum · blocked|escaped|n_a
verifiers:                             # 必填 · 非空 array（诚实：当前只 1 个）
  - name: "gate_engine"                 #   string · 验证器名
    result: "pass"                      #   enum · pass|fail|n_a
human_authority:                       # 必填 · object（人审判定，A1 的 verifier_disagreement 仍 N/A）
  status: "pending"                     #   enum · pending|approved|rejected
  review_method: "batch_authorization"  #   string · 诚实：615 全 batch_authorization，逐条独立 0
uncertainty:                           # 必填 · object（置信上界，信任根的诚实度）
  cs_upper_bound: 0.009062              #   number · 617 A1 estimand 三层 CS anytime 上界
  estimand: "L1"                        #   enum · L1|L2|L3
provenance:                            # 必填 · object（溯源，诚实：卡内无 commit）
  commit: "<git-sha>"                   #   string · 该卡首次授权的 commit（需 git 反查）
  first_authorized_at: "ISO8601"        #   对应卡 verified_at
expiry: "ISO8601"                      # 可选 · string
```

## 三、与现有 markdown 卡的字段映射

| certificate 字段 | atom 卡 frontmatter | evidence 卡 frontmatter |
|---|---|---|
| `claim.id` | `id` | `id` |
| `claim.statement` | `claim` / `claim_structured[].statement` | `hypothesis` |
| `claim.type` | `claim_structured[].claim_type` | `kind` + 推导 |
| `evidence[].ref` | `claim_structured[].evidence[]` | `serves[]`（反向边） |
| `evidence[].hash` | — | `artifact_sha256`（仅主工件） |
| `negative_tests` | `claim_structured[].external_basis`（部分） | `negative_controls[]` + v7 `results[]` |
| `verifiers` | —（仅单一验证器） | —（仅 gate + replay） |
| `human_authority.status` | `status` / `verified_by` | `status` / `verified_by` |
| `human_authority.review_method` | —（**缺口**） | —（缺口；615 证均为 batch_authorization） |
| `uncertainty.cs_upper_bound` | —（**缺口**） | —（缺口；全局 CS 0.9062% 已定义） |
| `provenance.commit` | —（**缺口**） | —（缺口） |
| `provenance.first_authorized_at` | `verified_at` | `verified_at` |

> **缺口总览**（B3 试点会显式登记，不编造）：
> - `verifiers` 只有 1 个（`gate_engine`/`replay`），`second_implementation = 1/63`（A3 雷2 印证 verifier_disagreement N/A）。
> - `human_authority.review_method` 全项目为 `batch_authorization`（615 诚实审计）。
> - `uncertainty` 卡内无，须引用全局 estimand（L1=0.9062%）。
> - `provenance.commit` 卡内无，须 `git log` 反查。

## 四、B2 验证器的最小校验契约（本表即契约）

`pck_certificate_verifier_619.py` 须校验：
- `schema_version == "619-pck-v1"`
- `claim` 四字段齐备且非空
- `evidence` 为非空数组，每项有合法 `type`
- `verifiers` 为非空数组，每项 `result ∈ {pass,fail,n_a}`
- `uncertainty.cs_upper_bound` 为数值（>0）
- `provenance.commit` 非空字符串
- 若 `verifiers` 长度 == 1 → 在报告里**标注**「单验证器，verifier_disagreement 不适用」（不报错，只诚实登记）
- 若 `human_authority.review_method == "batch_authorization"` → 标注「非逐条独立审阅」

> 不变量：验证器**只验证结构诚实性**，不代替真实门禁判 `pass/fail`（与 §六 一致）。
