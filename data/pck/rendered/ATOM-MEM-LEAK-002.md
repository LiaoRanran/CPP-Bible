# PCK 证书 · ATOM-MEM-LEAK-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-LEAK-002`
- **命题**：泄漏检测工具的**报告与否高度依赖被测代码的具体形态**，因此不能直接等价于泄漏有无： 同一份循环引用夹具、同一编译器与档位（WSL/Linux `-O1 -g -fsanitize=address,undefined`）， **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节），**改后**（仅给 `Node` 加一个 与泄漏无关的 `volatile` 构造计数）LSan **报告** `64 byte(s) leaked in 2 allocation(s)` （stderr 1258 字节）——唯一变量是一个与泄漏无关的计数器，且报告数值自洽（64 B = 2 × 32 B） ⇒ 判定泄漏应先用零依赖观测（构造/析构计数、存活对象数）定性，工具报告只作补充证据。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-042.md | — |
| replay | evidence/mem/EV-MEM-043.md | — |
| replay | evidence/mem/EV-MEM-042.md | — |
| replay | evidence/mem/EV-MEM-043.md | — |
| replay | evidence/mem/EV-MEM-042.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M6|块式 → flow 写法（pedagogy）` | blocked |
| `atoms/mem/ATOM-MEM-LEAK-002.md|M7|读数篡改（2 → 3）` | blocked |

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
- **commit**：`e60ed82dc7afe1f5857d5104f26bac6cc138cfae`
- **first_authorized_at**：2026-09-12

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

