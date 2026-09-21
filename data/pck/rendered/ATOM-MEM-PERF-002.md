# PCK 证书 · ATOM-MEM-PERF-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-PERF-002`
- **命题**：SSO（Small String Optimization）：短于阈值的字符串存在 string 对象内部缓冲，零堆分配；达到阈值 才落堆——本机 libstdc++（GCC 15.3.0）阈值 15 字符、sizeof=32，len≤15 构造/拷贝 allocs=0（赋值 走同一实现路径），len=16 首次落堆。SSO 是实现内建（标准不要求），三实现参数不保证一致 （libstdc++ 32/15、libc++ 24/22、MSVC 32/15——libc++ 与另两家不同），阈值不可移植。历史： C++11 禁 COW 后 libstdc++ 才全面转向 SSO。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-029.md | — |
| replay | evidence/mem/EV-MEM-029.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-PERF-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-002.md|M5|[命题 prop-2] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-002.md|M6|块式 → flow 写法（claim_structured）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-002.md|M7|读数篡改（2 → 3）` | blocked |

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

