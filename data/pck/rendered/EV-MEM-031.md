# PCK 证书 · EV-MEM-031

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-031`
- **命题**：SSO 的形状参数是**实现内建**、不保证跨实现一致：本机 libstdc++（GCC 15.3.0）sizeof(std::string)=32、 空串 capacity=15（SSO 容量 15 字符）、len=15 零分配 / len=16 落堆。libc++（Clang）为 sizeof=24、 SSO 容量 22（与另两家不同）；MSVC 为 sizeof=32、SSO 容量 15——后两者为文档值（本机无 Clang/MSVC， M2 边界；Clang 列由 CI Cross-check 回填）。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-031.md | sha256:77f1164c3dc0340e09a55718e51adb7dcd9dc8b6a01e03bcbfd4e9670febf7ae |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-031.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-031.md|M2|路径转大写（Examples/atoms/_atom_sso_size.cpp → EXAMPLES/ATOMS/_ATOM_SSO_SIZE.CPP）` | blocked |
| `evidence/mem/EV-MEM-031.md|M2|路径加 ./（Examples/atoms/_atom_sso_size.cpp → ./Examples/atoms/_atom_sso_size.cpp）` | blocked |
| `evidence/mem/EV-MEM-031.md|M2|分隔符换反斜杠（Examples/atoms/_atom_sso_size.cpp → Examples\atoms\_atom_sso_size.cpp）` | blocked |
| `evidence/mem/EV-MEM-031.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/mem/EV-MEM-031.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-031.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-031.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-031.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-031.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-031.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0]）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 非法值（compiler: [GCC 15.3.0] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-031.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-031.md|M7|sha256 改一位（77f1164c… → 07f1164c…）` | blocked |
| `evidence/mem/EV-MEM-031.md|M7|读数篡改（31 → 32）` | blocked |

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

