# PCK 证书 · EV-MEM-032

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-032`
- **命题**：unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统）：在 libstdc++ 实现下， 空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节），有状态删除器必须作为对象 成员存储（sizeof 16）；数组特化 `unique_ptr<T[]>` 走 delete[] 而不是 delete，且只提供 operator[]、 不提供 operator* / operator->——这些差异全部在**编译期**就能被类型系统看见。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-032.md | sha256:a96938954e8f1004381f75acf61793996e281bf5167f3d14f98a5198ba84eb14 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-032.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-032.md|M2|路径转大写（Examples/atoms/_atom_unique_deleter.cpp → EXAMPLES/ATOMS/_ATOM_UNIQUE_DELETER.CPP）` | blocked |
| `evidence/mem/EV-MEM-032.md|M2|路径加 ./（Examples/atoms/_atom_unique_deleter.cpp → ./Examples/atoms/_atom_unique_deleter.cpp）` | blocked |
| `evidence/mem/EV-MEM-032.md|M2|分隔符换反斜杠（Examples/atoms/_atom_unique_deleter.cpp → Examples\atoms\_atom_unique_deleter.cpp）` | blocked |
| `evidence/mem/EV-MEM-032.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-032.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-032.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-032.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-032.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-032.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-032.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/mem/EV-MEM-032.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-032.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-032.md|M7|sha256 改一位（a9693895… → 09693895…）` | blocked |
| `evidence/mem/EV-MEM-032.md|M7|读数篡改（32 → 33）` | blocked |

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

