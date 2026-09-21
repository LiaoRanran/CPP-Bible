# PCK 证书 · EV-MEM-042

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-042`
- **命题**：三种生命周期行为可用**零依赖信号**（volatile 析构计数）区分，且该区分**不依赖任何 sanitizer**： `scoped`（局部对象）析构 =1；`cycle`（shared_ptr 强引用闭环）析构 =0 且**不可达**（真泄漏）； `owned`（堆对象被全局容器持有）析构 =0 但**退出时仍可达**（与 cycle 语义完全不同）。 一个"析构 =0"的信号对应**两种不同语义**，因此它必须与"可达性"一起看才能下判断。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-042.md | sha256:ed44b0c6e06d2fcfdd88336417838e19eaf67ffb24e2f229d67e4a94a7f7b512 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-042.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-042.md|M2|路径转大写（Examples/atoms/_atom_leak_detection.cpp → EXAMPLES/ATOMS/_ATOM_LEAK_DETECTION.CPP）` | blocked |
| `evidence/mem/EV-MEM-042.md|M2|路径加 ./（Examples/atoms/_atom_leak_detection.cpp → ./Examples/atoms/_atom_leak_detection.cpp）` | blocked |
| `evidence/mem/EV-MEM-042.md|M2|分隔符换反斜杠（Examples/atoms/_atom_leak_detection.cpp → Examples\atoms\_atom_leak_detection.cpp）` | blocked |
| `evidence/mem/EV-MEM-042.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-042.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-042.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-042.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-042.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-042.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-042.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 删键（移除 opt: [-O2（本卡）/ -O1（同夹具在 EV-MEM-043 的 sanitizer 观测）]）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 非法值（opt: [-O2（本卡）/ -O1（同夹具在 EV-MEM-043 的 sanitizer 观测）] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-042.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-042.md|M7|sha256 改一位（ed44b0c6… → 0d44b0c6…）` | blocked |
| `evidence/mem/EV-MEM-042.md|M7|读数篡改（42 → 43）` | blocked |

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

