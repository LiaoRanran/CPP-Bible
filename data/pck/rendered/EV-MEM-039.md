# PCK 证书 · EV-MEM-039

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-039`
- **命题**：小对象分配策略的开销**必须实测，且"谁更快"本身就是平台/实现相关的**：同一夹具、同一工作量 （10000 次 64 字节分配+释放 × 7 轮取中位数）在 MinGW/libstdc++ 上单调缓冲与池都胜过全局 new （约 4.4× 与 2.0×），而在 Linux/glibc 上**三者全部翻转**——全局 new 最快，两种资源反而慢 （约 1.9× 与 1.37×）。故"池分配器更快"不是可移植结论；可移植的是因果链（回收与否） 与"必须实测"这条方法论。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-039.md | sha256:bf7d01826185a168c385702b3cc0c2def902601312052bffaa47c6d4e2c629f9 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-039.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-039.md|M2|路径转大写（Examples/atoms/_atom_allocator_bench.cpp → EXAMPLES/ATOMS/_ATOM_ALLOCATOR_BENCH.CPP）` | blocked |
| `evidence/mem/EV-MEM-039.md|M2|路径加 ./（Examples/atoms/_atom_allocator_bench.cpp → ./Examples/atoms/_atom_allocator_bench.cpp）` | blocked |
| `evidence/mem/EV-MEM-039.md|M2|分隔符换反斜杠（Examples/atoms/_atom_allocator_bench.cpp → Examples\atoms\_atom_allocator_bench.cpp）` | blocked |
| `evidence/mem/EV-MEM-039.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-039.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-039.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-039.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-039.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-039.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-039.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-039.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-039.md|M7|sha256 改一位（bf7d0182… → 0f7d0182…）` | blocked |
| `evidence/mem/EV-MEM-039.md|M7|读数篡改（39 → 40）` | blocked |

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

