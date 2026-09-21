# PCK 证书 · EV-MEM-028

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-028`
- **命题**：std::pmr 把内存策略变成运行时多态（memory_resource 虚接口，策略在构造时注入、可运行时替换）。 monotonic_buffer_resource 用一块栈上缓冲区伺候所有分配：pmr::vector 16 次 push_back 全程未触碰 上游（upstream_allocs=0 ⇒ 零堆分配）；对照组把同一容器接到"计数+委托 new_delete_resource"的 资源上，扩容路径可见（res_calls=5、bytes=124）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-028.md | sha256:1a9fc2e41d821784582ff71d626a1bb59ac93fcbd5977be089a2302e3d8a6f42 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-028.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-028.md|M2|路径转大写（Examples/atoms/_atom_alloc_pmr.cpp → EXAMPLES/ATOMS/_ATOM_ALLOC_PMR.CPP）` | blocked |
| `evidence/mem/EV-MEM-028.md|M2|路径加 ./（Examples/atoms/_atom_alloc_pmr.cpp → ./Examples/atoms/_atom_alloc_pmr.cpp）` | blocked |
| `evidence/mem/EV-MEM-028.md|M2|分隔符换反斜杠（Examples/atoms/_atom_alloc_pmr.cpp → Examples\atoms\_atom_alloc_pmr.cpp）` | blocked |
| `evidence/mem/EV-MEM-028.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-028.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-028.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-028.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-028.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-028.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-028.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-028.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-028.md|M7|sha256 改一位（1a9fc2e4… → 0a9fc2e4…）` | blocked |
| `evidence/mem/EV-MEM-028.md|M7|读数篡改（28 → 29）` | blocked |

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

