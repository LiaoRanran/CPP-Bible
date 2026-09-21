# PCK 证书 · EV-CONC-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-CONC-002`
- **命题**：`atomic_signal_fence` 与 `atomic_thread_fence` 在**指令层**完全不同、在**位置层**同样敏感： `signal_fence` 是纯编译器屏障（实测自旋侧与写入侧两条路径**都是零机器指令**）， `thread_fence` 才产生硬件屏障（x86-64 实测 `lock or … [rsp], 0`，riscv64 实测 `fence iorw,iorw`）； 而且这条硬件屏障**锁在栈地址 `[rsp]` 上，不碰被保护的普通 `int`**—— 被保护的标志仍走普通 `mov` 访存 ⇒ **屏障≠原子类型**（不提供原子性、不建立 happens-before）。 同一屏障从循环体内挪到循环体外，`spin_fence_outside` 立刻与无屏障版本同形（被整段消除）。
- **domain**：conc · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/conc/EV-CONC-002.md | sha256:8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3 |

## 负向测试（negative_tests · 26 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/conc/EV-CONC-002.md|M1|删 artifact_sha256` | blocked |
| `evidence/conc/EV-CONC-002.md|M1|删 run_match_file` | blocked |
| `evidence/conc/EV-CONC-002.md|M2|路径转大写（Examples/atoms/_atom_fence_vs_atomic.cpp → EXAMPLES/ATOMS/_ATOM_FENCE_VS_ATOMIC.CPP）` | blocked |
| `evidence/conc/EV-CONC-002.md|M2|路径加 ./（Examples/atoms/_atom_fence_vs_atomic.cpp → ./Examples/atoms/_atom_fence_vs_atomic.cpp）` | blocked |
| `evidence/conc/EV-CONC-002.md|M2|分隔符换反斜杠（Examples/atoms/_atom_fence_vs_atomic.cpp → Examples\atoms\_atom_fence_vs_atomic.cpp）` | blocked |
| `evidence/conc/EV-CONC-002.md|M3|contains_in → contains（区间断言降级为全文存在性）` | blocked |
| `evidence/conc/EV-CONC-002.md|M3|absent_in → absent（区间断言降级为全文不存在）` | blocked |
| `evidence/conc/EV-CONC-002.md|M3|删掉一条 run_match_keys 声明（弱化：少声明读数键 spin_fence_outside_ret）` | blocked |
| `evidence/conc/EV-CONC-002.md|M4|注入通用符号 main` | blocked |
| `evidence/conc/EV-CONC-002.md|M4|注入通用符号 ret` | blocked |
| `evidence/conc/EV-CONC-002.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/conc/EV-CONC-002.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/conc/EV-CONC-002.md|M5|-` | n_a |
| `evidence/conc/EV-CONC-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/conc/EV-CONC-002.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/conc/EV-CONC-002.md|M7|sha256 改一位（8dd19bc6… → 0dd19bc6…）` | blocked |
| `evidence/conc/EV-CONC-002.md|M7|读数篡改（2 → 3）` | blocked |

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

