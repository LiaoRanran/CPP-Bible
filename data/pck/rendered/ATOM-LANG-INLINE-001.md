# PCK 证书 · ATOM-LANG-INLINE-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-LANG-INLINE-001`
- **命题**：`inline` 函数（及变量）的定义可以出现在**多个翻译单元**，但各定义必须由**相同的 token 序列**构成 （[basic.def.odr]/16.4）；违反属 ill-formed, **no diagnostic required**——实测 GCC 家族**零诊断**， 且**当两个定义的可观测结果不同时**，其可观测行为由**链接顺序**与**优化档**共同决定：-O0（未内联）下链接器只保留同名符号的一个定义 （取先遇到的），行为随链接顺序改变；-O2（内联发生）下各 TU 内联「自己看到的定义」，行为与链接顺序 无关、两个值并列出现。
- **domain**：lang · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/lang/EV-LANG-001.md | — |
| replay | evidence/lang/EV-LANG-002.md | — |
| replay | evidence/lang/EV-LANG-001.md | — |
| replay | evidence/lang/EV-LANG-002.md | — |
| replay | evidence/lang/EV-LANG-001.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M1|-` | n_a |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M4|-` | n_a |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M6|块式 → flow 写法（status_history）` | blocked |
| `atoms/lang/ATOM-LANG-INLINE-001.md|M7|读数篡改（1 → 2）` | blocked |

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
- **commit**：`d6c3e0453d9ec341c4e760f86a7fae5b647f7fbc`
- **first_authorized_at**：unknown

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

