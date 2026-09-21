# PCK 证书 · ATOM-MEM-ALLOC-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-ALLOC-002`
- **命题**：三种小对象分配策略的元数据开销与**是否支持单块释放**绑定，可用统一口径 （struct_bytes + bookkeeping_bytes）量化：同一 workload（1000 次 24 B 分配，-O2）下， arena 元数据 total 32 B（struct 32 + bookkeeping 0，**前提：仅批量申请 + 整体释放—— 夹具 `release_all()` 只支持整体重置，中途释放单块会产生不可复用空洞**）； bitmap total 181 B（struct 56 + bookkeeping 125 B = 1 bit/块，且随块数线性增长： n=8000 时 1056 B）；pool total 8056 B（struct 56 + bookkeeping 8000 B = 8 B/块 free-list 指针，n=8000 时 64056 B）——排序为 arena << bitmap << pool， 与"pool 元数据最省"的直觉相反；内部碎片：arena 0、pool 8000 B （定长块 32 B => 8 B x 1000）、bitmap 0（位图不占用户区）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-040.md | — |
| replay | evidence/mem/EV-MEM-041.md | — |
| replay | evidence/mem/EV-MEM-040.md | — |
| replay | evidence/mem/EV-MEM-041.md | — |
| replay | evidence/mem/EV-MEM-040.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M6|块式 → flow 写法（pedagogy）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-002.md|M7|读数篡改（2 → 3）` | blocked |

## 验证器（verifiers）
- `gate_engine` → **pass**
> ⚠ 仅 1 个验证器：`verifier_disagreement` 不适用（A1 雷2 口径）。

## 人审判定（human_authority）
- **status**：pending
- **review_method**：batch_authorization
> ⚠ 批量授权，非逐条独立审阅（615 诚实审计结论）。

## 不确定性（uncertainty）
- **cs_upper_bound**：0.009062（estimand `L1`）

## 溯源（provenance）
- **commit**：`e60ed82dc7afe1f5857d5104f26bac6cc138cfae`
- **first_authorized_at**：2026-09-12

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

