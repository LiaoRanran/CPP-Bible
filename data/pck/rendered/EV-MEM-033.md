# PCK 证书 · EV-MEM-033

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-033`
- **命题**：shared_ptr 的删除器被**类型擦除**：语言层面不存在 `shared_ptr<T, D>`（对比 `unique_ptr<T, D>` 有 D 参数），删除器只能经构造函数按值注入并被控制块持有（一次拷贝发生在形参初始化，块内不再拷贝）； 对象大小恒为两个指针（16 字节）、与删除器类型无关。擦除的运行期代价是**控制块自身的堆分配**： 实测 `shared_ptr<T>(new T)` 触发 2 次堆分配（对象 + 控制块）、`make_shared<T>` 合并为 1 次， 而 unique_ptr 对照路径恒为 1 次（只有对象本身）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-033.md | sha256:a26740cd570112fd429b27c01d43601d28a2d1f7d17899e871ef69f8bdd1dd25 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-033.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-033.md|M2|路径转大写（Examples/atoms/_atom_shared_deleter_erase.cpp → EXAMPLES/ATOMS/_ATOM_SHARED_DELETER_ERASE.CPP）` | blocked |
| `evidence/mem/EV-MEM-033.md|M2|路径加 ./（Examples/atoms/_atom_shared_deleter_erase.cpp → ./Examples/atoms/_atom_shared_deleter_erase.cpp）` | blocked |
| `evidence/mem/EV-MEM-033.md|M2|分隔符换反斜杠（Examples/atoms/_atom_shared_deleter_erase.cpp → Examples\atoms\_atom_shared_deleter_erase.cpp）` | blocked |
| `evidence/mem/EV-MEM-033.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-033.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-033.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-033.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-033.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-033.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-033.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/mem/EV-MEM-033.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-033.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-033.md|M7|sha256 改一位（a26740cd… → 026740cd…）` | blocked |
| `evidence/mem/EV-MEM-033.md|M7|读数篡改（33 → 34）` | blocked |

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

