# PCK 证书 · ATOM-MEM-PERF-003

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`ATOM-MEM-PERF-003`
- **命题**：小对象分配的开销由**实现参数**与**策略语义**共同决定，两者都必须现场测量： ① SSO 阈值不是语言保证——同一判据、**同一条 g++-14 驱动**下 libstdc++ 实测 `sizeof=32`/容量 15、 libc++-18 实测 `sizeof=24`/容量 22（唯一变量 = 标准库实现；两者都完全符合 [string]）； ② 小对象分配策略**连"谁更快"都是平台相关的**：同一夹具、同一工作量在 MinGW/libstdc++ 上 单调缓冲与池都胜过全局 new（约 4.4× 与 2.0×），而在 Linux/glibc 上**三者全部翻转**—— 全局 new 最快，两种资源反慢（约 1.9× 与 1.37×）。故"池分配器更快"不是可移植结论； 可移植的是因果链（释放是否回收）与"必须实测"这条方法论； ③ 因此 PERF 类证据必须区分**断言锚**（真正跨环境稳定：迭代常量 + 观测通路活性） 与**留痕**（时序数据与对比结论：供人复算，不作断言）——这条纪律由本批**两次真实失败**逼出。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| replay | evidence/mem/EV-MEM-038.md | — |
| replay | evidence/mem/EV-MEM-038.md | — |
| replay | evidence/mem/EV-MEM-039.md | — |

## 负向测试（negative_tests · 11 条，来自 v7 baseline）
| mutation_id | result |
| `atoms/mem/ATOM-MEM-PERF-003.md|M1|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-003.md|M2|M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-003.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `atoms/mem/ATOM-MEM-PERF-003.md|M4|-` | n_a |
| `atoms/mem/ATOM-MEM-PERF-003.md|M5|[命题 prop-2] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M5|[命题 prop-3] claim_type: inference → observation（自标绕过）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M6|全角键名（ｉｄ）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M6|块式 → flow 写法（pedagogy）` | blocked |
| `atoms/mem/ATOM-MEM-PERF-003.md|M7|读数篡改（3 → 4）` | blocked |

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
- **commit**：`4802c68c82efaebd99495bfda3d73e6fc0840c93`
- **first_authorized_at**：2026-09-12

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

