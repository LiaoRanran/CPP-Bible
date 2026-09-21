# PCK 证书 · EV-UB-002

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-UB-002`
- **命题**：通过不兼容类型指针访问对象（严格别名）是**未定义行为**：优化器会假定不同类型的指针不指向同一 对象，并据此**消除对同一对象的再次读取**——该假设在 -O2 下默认启用，在 -fno-strict-aliasing 下关闭。
- **domain**：ub · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/ub/EV-UB-002.md | sha256:900a3e43f70ed68bcdf621d907a39996f62ec289fe4e453c910aa435c027575e |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/ub/EV-UB-002.md|M1|删 artifact_sha256` | blocked |
| `evidence/ub/EV-UB-002.md|M2|路径转大写（Examples/atoms/_atom_strict_alias.cpp → EXAMPLES/ATOMS/_ATOM_STRICT_ALIAS.CPP）` | blocked |
| `evidence/ub/EV-UB-002.md|M2|路径加 ./（Examples/atoms/_atom_strict_alias.cpp → ./Examples/atoms/_atom_strict_alias.cpp）` | blocked |
| `evidence/ub/EV-UB-002.md|M2|分隔符换反斜杠（Examples/atoms/_atom_strict_alias.cpp → Examples\atoms\_atom_strict_alias.cpp）` | blocked |
| `evidence/ub/EV-UB-002.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/ub/EV-UB-002.md|M4|注入通用符号 main` | blocked |
| `evidence/ub/EV-UB-002.md|M4|注入通用符号 ret` | blocked |
| `evidence/ub/EV-UB-002.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/ub/EV-UB-002.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/ub/EV-UB-002.md|M5|-` | n_a |
| `evidence/ub/EV-UB-002.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/ub/EV-UB-002.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/ub/EV-UB-002.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/ub/EV-UB-002.md|M7|sha256 改一位（900a3e43… → 000a3e43…）` | blocked |
| `evidence/ub/EV-UB-002.md|M7|读数篡改（2 → 3）` | blocked |

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

