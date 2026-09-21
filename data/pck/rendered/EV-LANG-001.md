# PCK 证书 · EV-LANG-001

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-LANG-001`
- **命题**：inline 函数在两个 TU 中被定义为**不同 token 序列**（违反 [basic.def.odr]/16.4）时，GCC 家族 **不产生任何诊断**（16.2 属 IFNDR）；且其可观测后果**依赖优化档**：-O0 下未内联，链接器只保留 同名 weak 符号的一个定义（取先遇到者）→ 程序行为随**链接顺序**改变；-O2 下两 TU 的调用点各自 内联「自己看到的定义」→ 行为与链接顺序无关。**内部链接（static）孪生对照**证明：顺序依赖来自 "外部链接 + 未内联时的符号合并"这一机制，而非"两 TU 代码不同"本身。
- **domain**：lang · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/lang/EV-LANG-001.md | sha256:63c7e3b73ea9646cbad081ba6b8c0a5ad6e5b77f780aebf944ffd65ba15fbc9f |

## 负向测试（negative_tests · 28 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/lang/EV-LANG-001.md|M1|删 artifact_sha256` | blocked |
| `evidence/lang/EV-LANG-001.md|M1|删 run_match_file` | blocked |
| `evidence/lang/EV-LANG-001.md|M2|路径转大写（Examples/atoms/_atom_inline_odr_main.cpp → EXAMPLES/ATOMS/_ATOM_INLINE_ODR_MAIN.CPP）` | blocked |
| `evidence/lang/EV-LANG-001.md|M2|路径加 ./（Examples/atoms/_atom_inline_odr_main.cpp → ./Examples/atoms/_atom_inline_odr_main.cpp）` | blocked |
| `evidence/lang/EV-LANG-001.md|M2|分隔符换反斜杠（Examples/atoms/_atom_inline_odr_main.cpp → Examples\atoms\_atom_inline_odr_main.cpp）` | blocked |
| `evidence/lang/EV-LANG-001.md|M3|contains_in → contains（区间断言降级为全文存在性）` | blocked |
| `evidence/lang/EV-LANG-001.md|M3|absent_in → absent（区间断言降级为全文不存在）` | blocked |
| `evidence/lang/EV-LANG-001.md|M3|-Werror 被删（编译告警不再算失败）` | blocked |
| `evidence/lang/EV-LANG-001.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/lang/EV-LANG-001.md|M3|删掉一条 run_match_keys 声明（弱化：少声明一个读数键 ab_tu_a）` | blocked |
| `evidence/lang/EV-LANG-001.md|M4|注入通用符号 main` | blocked |
| `evidence/lang/EV-LANG-001.md|M4|注入通用符号 ret` | blocked |
| `evidence/lang/EV-LANG-001.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/lang/EV-LANG-001.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/lang/EV-LANG-001.md|M5|-` | n_a |
| `evidence/lang/EV-LANG-001.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|块式 → flow 写法（controlled_vars）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 删键（移除 opt: [-O0, -O2]）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 非法值（opt: [-O0, -O2] → 首元素 -O9）` | blocked |
| `evidence/lang/EV-LANG-001.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/lang/EV-LANG-001.md|M7|sha256 改一位（63c7e3b7… → 03c7e3b7…）` | blocked |
| `evidence/lang/EV-LANG-001.md|M7|读数篡改（1 → 2）` | blocked |

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

