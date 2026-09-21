# PCK 证书 · EV-MEM-043

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-MEM-043`
- **命题**：**对照实验（唯一变量 = 一个与泄漏无关的 volatile 计数器）**：同一份循环引用夹具、同一编译器、 同一优化档（WSL/Linux `-O1 -g -fsanitize=address,undefined`）， **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节）； **改后**（给 `Node` 加 `volatile int g_cycle_ctor` 并自增，用于证明"分配真发生"） LSan **报告** `SUMMARY: AddressSanitizer: 64 byte(s) leaked in 2 allocation(s)`（stderr 1258 字节）。 ⇒ 泄漏检测工具的**报告与否高度依赖被测代码的具体形态**——连"加一个计数器"这种与泄漏无关的 改动都能翻转结论；"没报"因此不能直接等价于"没泄漏"。
- **domain**：mem · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/mem/EV-MEM-043.md | sha256:ed44b0c6e06d2fcfdd88336417838e19eaf67ffb24e2f229d67e4a94a7f7b512 |

## 负向测试（negative_tests · 23 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/mem/EV-MEM-043.md|M1|删 artifact_sha256` | blocked |
| `evidence/mem/EV-MEM-043.md|M2|路径转大写（Examples/atoms/_atom_leak_detection.cpp → EXAMPLES/ATOMS/_ATOM_LEAK_DETECTION.CPP）` | blocked |
| `evidence/mem/EV-MEM-043.md|M2|路径加 ./（Examples/atoms/_atom_leak_detection.cpp → ./Examples/atoms/_atom_leak_detection.cpp）` | blocked |
| `evidence/mem/EV-MEM-043.md|M2|分隔符换反斜杠（Examples/atoms/_atom_leak_detection.cpp → Examples\atoms\_atom_leak_detection.cpp）` | blocked |
| `evidence/mem/EV-MEM-043.md|M3|M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys 的字面量都在正文/注释）` | n_a |
| `evidence/mem/EV-MEM-043.md|M4|注入通用符号 main` | blocked |
| `evidence/mem/EV-MEM-043.md|M4|注入通用符号 ret` | blocked |
| `evidence/mem/EV-MEM-043.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/mem/EV-MEM-043.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/mem/EV-MEM-043.md|M5|-` | n_a |
| `evidence/mem/EV-MEM-043.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 删键（移除 opt: [-O1（sanitizer 观测档）, -O2（零依赖判据档）]）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 非法值（opt: [-O1（sanitizer 观测档）, -O2（零依赖判据档）] → 首元素 -O9）` | blocked |
| `evidence/mem/EV-MEM-043.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/mem/EV-MEM-043.md|M7|sha256 改一位（ed44b0c6… → 0d44b0c6…）` | blocked |
| `evidence/mem/EV-MEM-043.md|M7|读数篡改（43 → 44）` | blocked |

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

