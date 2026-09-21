# PCK 证书 · EV-MEM-036

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-036`
- **命题**：正确侧基线：owner/observer 结构（父节点用 shared_ptr 拥有子节点、子节点只用 weak_ptr 导航）在 构树函数返回时整棵树正常析构——实测 constructed=3 / destroyed after scope=3，反向导航仍可用 （parent reachable=1）；且本场景下进程**无 sanitizer 报错**。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-036.md | sha256:0fd4a1acb85f83b5bd27c62c4022a9085e9b2ad36401ceb8f36b5c10825649f0 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-036.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-036.md|M2|路径转大写（Examples/atoms/_atom_leak_tree_ok.cpp → EXAMPLES/ATOMS/_ATOM_LEAK_TREE_OK.CPP）` | blocked |
| `evidence/mem/EV-MEM-036.md|M2|路径加 ./（Examples/atoms/_atom_leak_tree_ok.cpp → ./Examples/atoms/_atom_leak_tree_ok.cpp）` | blocked |
| `evidence/mem/EV-MEM-036.md|M2|分隔符换反斜杠（Examples/atoms/_atom_leak_tree_ok.cpp → Examples\atoms\_atom_leak_tree_ok.cpp）` | blocked |
| `evidence/mem/EV-MEM-036.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-036.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-036.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-036.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-036.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-036.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-036.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|块式 → flow 写法（matrix）` | escaped |
| `evidence/mem/EV-MEM-036.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-036.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-036.md|M7|sha256 改一位（0fd4a1ac… → 1fd4a1ac…）` | blocked |
| `evidence/mem/EV-MEM-036.md|M7|读数篡改（36 → 37）` | blocked |

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

