# PCK 证书 · ATOM-MEM-SHARED-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-SHARED-001`
- **命题**：std::shared_ptr<T> 用引用计数实现共享所有权：拷贝 +1、析构 -1，计数归零才释放资源（析构恰好一次）。 控制块（RAII）管理计数与资源。但它不能自动处理循环引用——两个对象互相 shared_ptr 持有，彼此计数 为 2，离开作用域后各减到 1 仍互指，计数永不归零 => 泄漏；循环必须用 weak_ptr 打破。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-013.md | — |
| replay | evidence/mem/EV-MEM-014.md | — |
| replay | evidence/mem/EV-MEM-013.md | — |
| replay | evidence/mem/EV-MEM-014.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-SHARED-001.md|M7|读数篡改（1 → 2）` | blocked |

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

