# PCK 证书 · EV-HIST-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-HIST-001`
- **命题**：`std::auto_ptr` 的"拷贝构造"实际语义是**转移所有权**：拷贝后源被清空；因此把元素从容器里 读/拷出来这一步就会偷空源元素——这与容器"拷贝后两个对象等价"的隐含约定直接冲突。
- **domain**：hist · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/hist/EV-HIST-001.md | sha256:b4f993189459e84031d2a6b37f5bf04da88c140c637cb2c37fb7357f6dfdd691 |

## 负向测试（negative_tests · 24 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/hist/EV-HIST-001.md|M1|删 artifact_sha256` | blocked |
| `evidence/hist/EV-HIST-001.md|M2|路径转大写（Examples/atoms/_atom_auto_ptr.cpp → EXAMPLES/ATOMS/_ATOM_AUTO_PTR.CPP）` | blocked |
| `evidence/hist/EV-HIST-001.md|M2|路径加 ./（Examples/atoms/_atom_auto_ptr.cpp → ./Examples/atoms/_atom_auto_ptr.cpp）` | blocked |
| `evidence/hist/EV-HIST-001.md|M2|分隔符换反斜杠（Examples/atoms/_atom_auto_ptr.cpp → Examples\atoms\_atom_auto_ptr.cpp）` | blocked |
| `evidence/hist/EV-HIST-001.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/hist/EV-HIST-001.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/hist/EV-HIST-001.md|M4|注入通用符号 main` | blocked |
| `evidence/hist/EV-HIST-001.md|M4|注入通用符号 ret` | blocked |
| `evidence/hist/EV-HIST-001.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/hist/EV-HIST-001.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/hist/EV-HIST-001.md|M5|-` | n_a |
| `evidence/hist/EV-HIST-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/hist/EV-HIST-001.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 删键（移除 std: [c++14, c++17, c++23]）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 非法值（std: [c++14, c++17, c++23] → 首元素 c++99）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/hist/EV-HIST-001.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/hist/EV-HIST-001.md|M7|sha256 改一位（b4f99318… → 04f99318…）` | blocked |
| `evidence/hist/EV-HIST-001.md|M7|读数篡改（1 → 2）` | blocked |

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

