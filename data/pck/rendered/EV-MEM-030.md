# PCK 证书 · EV-MEM-030

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-030`
- **命题**：SSO 的操作代价差是确定性的分配次数差：短字符串（≤阈值）拷贝零堆分配（只搬对象内 32 字节 缓冲；赋值走同一实现路径，未单列观测行）；长字符串同样的操作每次都要 1 次堆分配；短+短拼接 一旦越过阈值（10+10=20>15），结果立即落堆 1 次。性能口径用分配次数而非墙钟（墙钟不可复现， 沿 EV-MEM-008 先例）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-030.md | sha256:06579f60872a4111e9ff4a9531e30e1925a54507bafa7e09e329f7cfa754d77e |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-030.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-030.md|M2|路径转大写（Examples/atoms/_atom_sso_cost.cpp → EXAMPLES/ATOMS/_ATOM_SSO_COST.CPP）` | blocked |
| `evidence/mem/EV-MEM-030.md|M2|路径加 ./（Examples/atoms/_atom_sso_cost.cpp → ./Examples/atoms/_atom_sso_cost.cpp）` | blocked |
| `evidence/mem/EV-MEM-030.md|M2|分隔符换反斜杠（Examples/atoms/_atom_sso_cost.cpp → Examples\atoms\_atom_sso_cost.cpp）` | blocked |
| `evidence/mem/EV-MEM-030.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-030.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-030.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-030.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-030.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-030.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-030.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-030.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-030.md|M7|sha256 改一位（06579f60… → 16579f60…）` | blocked |
| `evidence/mem/EV-MEM-030.md|M7|读数篡改（30 → 31）` | blocked |

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

