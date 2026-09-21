# PCK 证书 · EV-MEM-007

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-007`
- **命题**：xvalue 有身份（指代特定对象 x），prvalue 没有身份（不指代任何命名对象）。若 std::move(x) 真是 prvalue （即"x 的一份临时副本"），则从它移动不应改动 x；实测移动后 x 被改动 => std::move(x) 指代真实对象 x => 它是 xvalue，不是 prvalue。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-007.md | sha256:988f921283b0be3977df0ca79baed518ca5d55c9e0b1db5e7b40856b74fa7006 |

## 负向测试（negative_tests · 24 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-007.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-007.md|M2|路径转大写（Examples/atoms/_atom_value_xvalue.cpp → EXAMPLES/ATOMS/_ATOM_VALUE_XVALUE.CPP）` | blocked |
| `evidence/mem/EV-MEM-007.md|M2|路径加 ./（Examples/atoms/_atom_value_xvalue.cpp → ./Examples/atoms/_atom_value_xvalue.cpp）` | blocked |
| `evidence/mem/EV-MEM-007.md|M2|分隔符换反斜杠（Examples/atoms/_atom_value_xvalue.cpp → Examples\atoms\_atom_value_xvalue.cpp）` | blocked |
| `evidence/mem/EV-MEM-007.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/mem/EV-MEM-007.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-007.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-007.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-007.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-007.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-007.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-007.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-007.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-007.md|M7|sha256 改一位（988f9212… → 088f9212…）` | blocked |
| `evidence/mem/EV-MEM-007.md|M7|读数篡改（7 → 8）` | blocked |

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

