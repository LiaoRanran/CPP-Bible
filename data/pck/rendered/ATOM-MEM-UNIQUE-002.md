# PCK 证书 · ATOM-MEM-UNIQUE-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-UNIQUE-002`
- **命题**：unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统），因此删除器会影响 对象大小与类型：libstdc++ 下，空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节）， 而空但 final 的删除器与有状态删除器都必须存储（16 字节）——这是**实现边界**而非语言保证 （final 反例实测 16，见 EV-MEM-032）。数组特化 `unique_ptr<T[]>` 是独立特化：只提供 operator[]、 不提供 operator* 与 operator->，且在默认删除器下走 delete[]。与之对照，shared_ptr 的删除器被 **类型擦除**——语言层面不存在 `shared_ptr<T, D>`，删除器只能经构造函数按值注入并被控制块持有， 对象大小恒为两个指针、与删除器类型无关；代价是控制块自身的堆分配（裸指针构造 2 次分配、 make_shared 合并为 1 次，见 EV-MEM-033）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-032.md | — |
| replay | evidence/mem/EV-MEM-033.md | — |
| replay | evidence/mem/EV-MEM-032.md | — |
| replay | evidence/mem/EV-MEM-033.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md|M7|读数篡改（2 → 3）` | blocked |

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

