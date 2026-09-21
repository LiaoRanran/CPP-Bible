# PCK 证书 · EV-MEM-034

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-034`
- **命题**：shared_ptr 的控制块引用计数用**原子 RMW** 修改——汇编层带 `lock` 前缀（MinGW 工件 `lock add` ×3 / `lock sub` ×5；gcc-14 工件 `lock add` ×3 / `lock xadd` ×5），且这些指令全部落在控制块符号的作用域 内（夹具自身**不含**任何原子计数器）；因此多线程**各持副本**时的并发拷贝/销毁是安全的：实测 4 线程 × 2000 次拷贝后引用计数收敛回 1、被指对象值完好。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-034.md | sha256:2f8097b8b0b7e21636c419f19934225093440bbdf57a7396311e41d70d72a97f |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-034.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-034.md|M2|路径转大写（Examples/atoms/_atom_shared_atomic.cpp → EXAMPLES/ATOMS/_ATOM_SHARED_ATOMIC.CPP）` | blocked |
| `evidence/mem/EV-MEM-034.md|M2|路径加 ./（Examples/atoms/_atom_shared_atomic.cpp → ./Examples/atoms/_atom_shared_atomic.cpp）` | blocked |
| `evidence/mem/EV-MEM-034.md|M2|分隔符换反斜杠（Examples/atoms/_atom_shared_atomic.cpp → Examples\atoms\_atom_shared_atomic.cpp）` | blocked |
| `evidence/mem/EV-MEM-034.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-034.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-034.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-034.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-034.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-034.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-034.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/mem/EV-MEM-034.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-034.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-034.md|M7|sha256 改一位（2f8097b8… → 0f8097b8…）` | blocked |
| `evidence/mem/EV-MEM-034.md|M7|读数篡改（34 → 35）` | blocked |

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
- **commit**：`d3b2cb709b2d84921d2e2571cdb8b90011ff8b3a`
- **first_authorized_at**：unknown

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

