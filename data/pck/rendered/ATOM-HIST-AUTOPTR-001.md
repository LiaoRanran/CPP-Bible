# PCK 证书 · ATOM-HIST-AUTOPTR-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-HIST-AUTOPTR-001`
- **命题**：std::auto_ptr 的"拷贝构造"签名是 auto_ptr(auto_ptr&)（非 const 左值引用）：它**不满足** CopyConstructible，却能从非 const 对象"拷贝"，且拷贝后**源被清空**（转移所有权）。 这是 C++98 缺少移动语义时的工程妥协——用拷贝的语法表达转移的语义，因而与容器 "拷贝后两对象等价"的隐含约定从根上冲突。C++11 用移动语义（unique_ptr）给出正确表达后， auto_ptr 被弃用（C++11 deprecated → C++17 从标准移除）。
- **domain**：hist · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/hist/EV-HIST-001.md | — |
| replay | evidence/hist/EV-MEM-003.md | — |
| replay | evidence/hist/EV-HIST-001.md | — |
| replay | evidence/hist/EV-MEM-003.md | — |
| replay | evidence/hist/EV-HIST-001.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M1|-` | n_a |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M4|-` | n_a |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md|M7|读数篡改（1 → 2）` | blocked |

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
- **first_authorized_at**：2026-09-10

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

