# PCK 证书 · ATOM-MEM-ALLOC-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-ALLOC-001`
- **命题**：allocator 是 STL 容器的内存**策略**抽象：容器只经 allocator_traits 要内存，不直接调 new/delete。 C++17 后 std::allocator 只剩 allocate/deallocate 纯分配层（construct/destroy 移除、统一走 traits）， 分配与对象构造是两个独立动作。策略可整体替换：自定义 arena 分配器接入 vector 后 16 次 push_back 零堆分配；std::pmr（C++17）把策略变成运行时多态——monotonic_buffer_resource 用栈缓冲伺候全部 分配、全程不触碰上游。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-026.md | — |
| replay | evidence/mem/EV-MEM-027.md | — |
| replay | evidence/mem/EV-MEM-028.md | — |
| replay | evidence/mem/EV-MEM-026.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M5|[命题 prop-4] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-ALLOC-001.md|M7|读数篡改（1 → 2）` | blocked |

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
- **commit**：`a0582f297c3cce6f0bea513a63b5a6b738834cd4`
- **first_authorized_at**：2026-09-11

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

