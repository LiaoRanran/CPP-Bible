# PCK 证书 · EV-CONC-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-CONC-001`
- **命题**：`while (!b) {}`（b 为非原子非 volatile 全局 `int`）在 `-O2` 下是否被整段消除， 由**同步操作落在循环体内还是体外**决定，而不是由"函数里有没有屏障"决定： 无屏障（`spin_plain`）与屏障在**循环体外**（`spin_fence_outside`）都被整段消除， 函数符号区间内**零** `s_*_b` 符号引用；屏障在**循环体内**（`spin_signal_fence` 零机器指令 / `spin_with_fence` 产 `lock`）则循环保留，区间内可见 `s_sf_b` / `s_f_b` 与循环回边。
- **domain**：conc · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/conc/EV-CONC-001.md | sha256:8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3 |

## 负向测试（negative_tests · 27 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/conc/EV-CONC-001.md|M1|删 artifact_sha256` | blocked |
| `evidence/conc/EV-CONC-001.md|M1|删 run_match_file` | blocked |
| `evidence/conc/EV-CONC-001.md|M1|删 negative_controls` | escaped |
| `evidence/conc/EV-CONC-001.md|M2|路径转大写（Examples/atoms/_atom_fence_vs_atomic.cpp → EXAMPLES/ATOMS/_ATOM_FENCE_VS_ATOMIC.CPP）` | blocked |
| `evidence/conc/EV-CONC-001.md|M2|路径加 ./（Examples/atoms/_atom_fence_vs_atomic.cpp → ./Examples/atoms/_atom_fence_vs_atomic.cpp）` | blocked |
| `evidence/conc/EV-CONC-001.md|M2|分隔符换反斜杠（Examples/atoms/_atom_fence_vs_atomic.cpp → Examples\atoms\_atom_fence_vs_atomic.cpp）` | blocked |
| `evidence/conc/EV-CONC-001.md|M3|contains_in → contains（区间断言降级为全文存在性）` | blocked |
| `evidence/conc/EV-CONC-001.md|M3|absent_in → absent（区间断言降级为全文不存在）` | blocked |
| `evidence/conc/EV-CONC-001.md|M3|删掉一条 run_match_keys 声明（弱化：少声明读数键 spin_plain_ret）` | blocked |
| `evidence/conc/EV-CONC-001.md|M4|注入通用符号 main` | blocked |
| `evidence/conc/EV-CONC-001.md|M4|注入通用符号 ret` | blocked |
| `evidence/conc/EV-CONC-001.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/conc/EV-CONC-001.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/conc/EV-CONC-001.md|M5|-` | n_a |
| `evidence/conc/EV-CONC-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|块式 → flow 写法（matrix）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/conc/EV-CONC-001.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/conc/EV-CONC-001.md|M7|sha256 改一位（8dd19bc6… → 0dd19bc6…）` | blocked |
| `evidence/conc/EV-CONC-001.md|M7|读数篡改（1 → 2）` | blocked |

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
- **commit**：`e374517d153b8a063b04317a13e3553787fb66d2`
- **first_authorized_at**：unknown

## 诚实注释（B2）
- ℹ️ 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
- ℹ️ review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

