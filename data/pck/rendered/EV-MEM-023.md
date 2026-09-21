# PCK 证书 · EV-MEM-023

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-023`
- **命题**：Rule of Zero：成员全是 RAII 类型（std::unique_ptr）时，零特殊成员函数声明——编译器隐式生成的特殊 成员函数把正确语义全部做对：移动构造/移动赋值隐式生成（unique_ptr 可移动）、拷贝构造/拷贝赋值被 隐式**删除**（unique_ptr 不可拷贝）、析构隐式生成且正确（委托给成员析构）。 运行期：移动转移所有权、资源恰好构造 1 次析构 1 次释放 1 次（零泄漏、零双重析构）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-023.md | sha256:6016c553283a4ef716e8ffd081b50bdf31254b0e7ded878c31b1f8680f917fe8 |

## 负向测试（negative_tests · 24 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-023.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-023.md|M2|路径转大写（Examples/atoms/_atom_rule_zero.cpp → EXAMPLES/ATOMS/_ATOM_RULE_ZERO.CPP）` | blocked |
| `evidence/mem/EV-MEM-023.md|M2|路径加 ./（Examples/atoms/_atom_rule_zero.cpp → ./Examples/atoms/_atom_rule_zero.cpp）` | blocked |
| `evidence/mem/EV-MEM-023.md|M2|分隔符换反斜杠（Examples/atoms/_atom_rule_zero.cpp → Examples\atoms\_atom_rule_zero.cpp）` | blocked |
| `evidence/mem/EV-MEM-023.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/mem/EV-MEM-023.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-023.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-023.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-023.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-023.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-023.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-023.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-023.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-023.md|M7|sha256 改一位（6016c553… → 0016c553…）` | blocked |
| `evidence/mem/EV-MEM-023.md|M7|读数篡改（23 → 24）` | blocked |

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

