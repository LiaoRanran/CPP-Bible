# PCK 证书 · EV-CONC-006

> 验证徽标：**✅ PASS**（B2 v619-pck-v1）

## 主张（claim）
- **id**：`EV-CONC-006`
- **命题**：TSan 能检测本夹具的 data race（bench_race 两线程无同步并发写 g_shared），且对无竞争版本 （bench_safe，std::atomic）零误报；但 TSan 有漏报边界，"没被报"≠"没有数据竞争"。
- **domain**：conc · **type**：observation

## 证据（evidence）
| type | ref | hash |
| artifact | evidence/conc/EV-CONC-006.md | sha256:5c5549aebfb148a053498f173aaa09757a92e180f54e956dc853c4761d2405bc |

## 负向测试（negative_tests · 26 条，来自 v7 baseline）
| mutation_id | result |
| `evidence/conc/EV-CONC-006.md|M1|删 artifact_sha256` | blocked |
| `evidence/conc/EV-CONC-006.md|M1|删 run_match_file` | blocked |
| `evidence/conc/EV-CONC-006.md|M2|路径转大写（Examples/atoms/_atom_data_race.cpp → EXAMPLES/ATOMS/_ATOM_DATA_RACE.CPP）` | blocked |
| `evidence/conc/EV-CONC-006.md|M2|路径加 ./（Examples/atoms/_atom_data_race.cpp → ./Examples/atoms/_atom_data_race.cpp）` | blocked |
| `evidence/conc/EV-CONC-006.md|M2|分隔符换反斜杠（Examples/atoms/_atom_data_race.cpp → Examples\atoms\_atom_data_race.cpp）` | blocked |
| `evidence/conc/EV-CONC-006.md|M3|删掉一条 flow 式断言条目（弱化：卡少查一项）` | blocked |
| `evidence/conc/EV-CONC-006.md|M3|contains 追加样板候选（弱化：恒真文本即可满足）` | blocked |
| `evidence/conc/EV-CONC-006.md|M3|删掉一条 run_match_keys 声明（弱化：少声明一个读数键 single_total）` | blocked |
| `evidence/conc/EV-CONC-006.md|M4|注入通用符号 main` | blocked |
| `evidence/conc/EV-CONC-006.md|M4|注入通用符号 ret` | blocked |
| `evidence/conc/EV-CONC-006.md|M4|注入 ABI 帧符号 .p2align` | blocked |
| `evidence/conc/EV-CONC-006.md|M4|注入 contains_any: ['.file']（合法形态）` | blocked |
| `evidence/conc/EV-CONC-006.md|M5|-` | n_a |
| `evidence/conc/EV-CONC-006.md|M6|重复 id 键（后写覆盖前写）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|缩进提升（id 多缩一格，改变嵌套归属）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|全角键名（ｉｄ）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|块式 → flow 写法（controlled_vars）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 删键（移除 compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 非法值（compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)] → 首元素 totally-not-a-compiler xyz）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 删键（移除 std: [c++23]）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 非法值（std: [c++23] → 首元素 c++99）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 删键（移除 opt: [-O2]）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 非法值（opt: [-O2] → 首元素 -O9）` | blocked |
| `evidence/conc/EV-CONC-006.md|M6|matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）` | blocked |
| `evidence/conc/EV-CONC-006.md|M7|sha256 改一位（5c5549ae… → 0c5549ae…）` | blocked |
| `evidence/conc/EV-CONC-006.md|M7|读数篡改（6 → 7）` | blocked |

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

