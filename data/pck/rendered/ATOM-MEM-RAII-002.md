# PCK 证书 · ATOM-MEM-RAII-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-RAII-002`
- **命题**：特殊成员函数要不要写，判据是"成员形状"而非记忆口诀：成员全是 RAII 类型（unique_ptr/vector/string） 时一个都不写（Rule of Zero）——编译器隐式生成的特殊成员函数语义全部正确（可拷贝成员拷贝隐式生成 且语义正确、不可拷贝成员如 unique_ptr 的拷贝被删除，移动/析构正确生成；实测 allocs=dtors=frees=1）； 管理裸资源时三件套（析构/拷贝构造/拷贝赋值，Rule of Three）或五件套（+ 移动构造/移动赋值，Rule of Five）必须齐写——只写析构会得到隐式浅拷贝，同一资源两次析构，析构真释放即 double free； 写移动构造必须标 noexcept，否则 vector 扩容搬迁退化为逐个拷贝。 （Rule of Zero 的隐式语义按成员形状各得其所：可拷贝 RAII 成员的拷贝**隐式生成且语义正确**， 不可拷贝成员如 unique_ptr 的拷贝被**删除**——不是一律"删除拷贝"。）
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-023.md | — |
| replay | evidence/mem/EV-MEM-024.md | — |
| replay | evidence/mem/EV-MEM-025.md | — |
| replay | evidence/mem/EV-MEM-023.md | — |
| replay | evidence/mem/EV-MEM-024.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-RAII-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-RAII-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-RAII-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-RAII-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-RAII-002.md|M5|[命题 prop-4] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-RAII-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-RAII-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-RAII-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-RAII-002.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-RAII-002.md|M7|读数篡改（2 → 3）` | blocked |

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

