# PCK 证书 · ATOM-MEM-PERF-004

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-PERF-004`
- **命题**：多线程各自读写**逻辑独立**的变量时仍可能因共享缓存行（false sharing）付出约一个数量级的性能代价 ——本机实测 4 线程各累加 1e7 次：相邻布局中位数 562500600 ns vs `alignas` 隔离后 29824800 ns （**18.86×**，Linux 同夹具 18.54×，方向一致）；该结构前提可用地址**确定性判定** （`tight_same_line=1` / `padded_same_line=0`，不依赖计时），而 padding 的代价是空间 （`padded_sizeof=128`）⇒ 存在最优对齐粒度，"padding 一定值得"同样是过度概括。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-044.md | — |
| replay | evidence/mem/EV-MEM-045.md | — |
| replay | evidence/mem/EV-MEM-044.md | — |
| replay | evidence/mem/EV-MEM-045.md | — |
| replay | evidence/mem/EV-MEM-044.md | — |

## 负向测试（negative_tests · 10 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-PERF-004.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-004.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-004.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-004.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-004.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-004.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-004.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-004.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-004.md|M6|块式 → flow 写法（pedagogy）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-004.md|M7|读数篡改（4 → 5）` | blocked |

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

