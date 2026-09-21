# PCK 证书 · EV-MEM-040

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-040`
- **命题**：**统一口径**下（元数据 := 为管理这批分配、分配器自身占用且不承载用户数据的全部字节， 逐项拆为 struct_bytes + bookkeeping_bytes），三种分配策略的真实开销排序是 **arena 32 B < bitmap 181 B ≪ pool 8056 B**（n=1000），n=8000 时为 **arena 32 B < bitmap 1056 B ≪ pool 64056 B** —— 即 pool 的 free-list 堆数组 （8 B/块）使它的 bookkeeping **远超** bitmap 的位图（1 bit/块）； 且 pool 与 bitmap 的元数据**都随块数增长**（7.95× 与 5.83× @8× 规模）， arena 则恒为 32 B（它不维护任何 bookkeeping）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-040.md | sha256:4f482fdcdb7ec335d833422dec2a9b2cce85d0e7a45b9550c1e176308c415510 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-040.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-040.md|M2|路径转大写（Examples/atoms/_atom_alloc_strategies.cpp → EXAMPLES/ATOMS/_ATOM_ALLOC_STRATEGIES.CPP）` | blocked |
| `evidence/mem/EV-MEM-040.md|M2|路径加 ./（Examples/atoms/_atom_alloc_strategies.cpp → ./Examples/atoms/_atom_alloc_strategies.cpp）` | blocked |
| `evidence/mem/EV-MEM-040.md|M2|分隔符换反斜杠（Examples/atoms/_atom_alloc_strategies.cpp → Examples\atoms\_atom_alloc_strategies.cpp）` | blocked |
| `evidence/mem/EV-MEM-040.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/mem/EV-MEM-040.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-040.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-040.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-040.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-040.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-040.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-040.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-040.md|M7|sha256 改一位（4f482fdc… → 0f482fdc…）` | blocked |
| `evidence/mem/EV-MEM-040.md|M7|读数篡改（40 → 41）` | blocked |

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

