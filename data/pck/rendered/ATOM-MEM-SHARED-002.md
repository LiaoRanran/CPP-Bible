# PCK 证书 · ATOM-MEM-SHARED-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-SHARED-002`
- **命题**：shared_ptr 的控制块引用计数用 LOCK 前缀的原子 RMW 修改，因此**各线程持有各自副本**时的并发 拷贝/销毁是安全的；但**被指对象**与**同一个 shared_ptr 实例**都不受这层保护（并发读写同一实例 需外部同步，C++20 起可用 std::atomic<std::shared_ptr<T>>；use_count() 在并发下只是近似值）。 unique_ptr 的所有权转移是纯指针搬运、不含原子 RMW，代价是**不可拷贝**——要共享必须显式改用 shared_ptr，于是"要不要付原子代价"成了编译期可判的选择，而不是运行期祈祷。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-034.md | — |
| replay | evidence/mem/EV-MEM-034.md | — |
| replay | evidence/mem/EV-MEM-034.md | — |
| replay | evidence/mem/EV-MEM-035.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-002.md|M7|读数篡改（2 → 3）` | blocked |

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
- **commit**：`d66ee59d7e313095f28e0ee4f39fdc172e0c7181`
- **first_authorized_at**：2026-09-11

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

