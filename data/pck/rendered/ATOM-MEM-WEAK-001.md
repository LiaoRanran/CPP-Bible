# PCK 证书 · ATOM-MEM-WEAK-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-WEAK-001`
- **命题**：std::weak_ptr 是非拥有观察者：指向 shared_ptr 管理的对象但不增加引用计数；.lock() 临时提升为 shared_ptr（对象活着则成功、计数 +1），对象已销毁则 .lock() 返回空（expired）。它用来在"需要旁观共享对象 但不延长其寿命"的场景（尤其子->父反向引用）打破 shared_ptr 的循环引用，避免泄漏。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-015.md | — |
| replay | evidence/mem/EV-MEM-016.md | — |
| replay | evidence/mem/EV-MEM-015.md | — |
| replay | evidence/mem/EV-MEM-016.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-WEAK-001.md|M7|读数篡改（1 → 2）` | blocked |

## 验证器（verifiers）
- `gate_engine` → **pass**
> ⚠ 仅 1 个验证器：`verifier_disagreement` 不适用（A1 雷2 口径）。

## 人审判定（human_authority）
- **status**：approved
- **review_method**：batch_authorization
> ⚠ 批量授权，非逐条独立审阅（615 诚实审计结论）。

## 不确定性（uncertainty）
- **cs_upper_bound**：0.009062（estimand `L1`）

## 溯源（provenance）
- **commit**：`5b9cc24f239e4901099f8c3b70522ede537d10df`
- **first_authorized_at**：2026-09-11

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

