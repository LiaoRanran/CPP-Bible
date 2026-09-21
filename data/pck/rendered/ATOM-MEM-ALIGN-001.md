# PCK 证书 · ATOM-MEM-ALIGN-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-ALIGN-001`
- **命题**：每个类型有对齐要求；结构体成员按自身对齐排列，编译器在成员间/末尾插入 padding，使每个成员与整体满足对齐， sizeof 包含 padding（故通常 > 各成员大小之和）。alignas 可提升对齐、alignof 查询对齐；搬运结构体用 按字节 memcpy（安全），用 reinterpret_cast 强转指针对齐/类型双关是未定义行为。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-019.md | — |
| replay | evidence/mem/EV-MEM-020.md | — |
| replay | evidence/mem/EV-MEM-019.md | — |
| replay | evidence/mem/EV-MEM-020.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-ALIGN-001.md|M7|读数篡改（1 → 2）` | blocked |

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
- **commit**：`d6c3e0453d9ec341c4e760f86a7fae5b647f7fbc`
- **first_authorized_at**：2026-09-11

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

