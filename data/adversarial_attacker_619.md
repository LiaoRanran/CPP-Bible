# 619 A2 · 攻击者原型报告（只读 replay over v7）

> 输入：`data/mutation/full_baseline_v7.json`（可判 1406 / 总 1593）
> 权重：{'verdict_regime_disagreement': 0.25, 'evidence_ambiguity': 0.2, 'rule_blind_spot': 0.4, 'provenance_inconsistency': 0.15}（W1 默认；敏感度见 `data/adversarial_objective_619.md` §五）

## 一致性校验（逃逸率契约 1/1406）
- n_total=1593 escaped_real=1 equivalent=8 n_a=179 denom=1406
- **contract_ok = True** （断言：escaped_real==1 且 denom==1406；本工具只读不破坏基线）

## 一、加权 Top20（优先 fuzz 谁）
| # | card | op | kind | composite | point | hit_rules |
| 1 | evidence/conc/EV-CONC-001.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 2 | evidence/conc/EV-CONC-002.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 3 | evidence/conc/EV-CONC-003.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 4 | evidence/conc/EV-CONC-004.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 5 | evidence/conc/EV-CONC-005.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 6 | evidence/conc/EV-CONC-006.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 7 | evidence/hist/EV-HIST-001.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 8 | evidence/lang/EV-LANG-001.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 9 | evidence/lang/EV-LANG-002.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 10 | evidence/mem/EV-MEM-001.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 11 | evidence/mem/EV-MEM-002.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 12 | evidence/mem/EV-MEM-003.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 13 | evidence/mem/EV-MEM-004.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 14 | evidence/mem/EV-MEM-005.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 15 | evidence/mem/EV-MEM-006.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 16 | evidence/mem/EV-MEM-007.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 17 | evidence/mem/EV-MEM-008.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 18 | evidence/mem/EV-MEM-009.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 19 | evidence/mem/EV-MEM-010.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |
| 20 | evidence/mem/EV-MEM-011.md | M1 | strict | 0.42 | 删 artifact_sha256 | ['EV-FM-REQUIRED'] |

## 二、帕累托前沿（4 个不同非支配向量，多目标兜底）
> 按 4 子目标向量去重；同一向量可能含多条 mutation（见「count」）。
| vrd | evidence_ambiguity | rule_blind_spot | provenance | count | example |
| 0.0 | 0.85 | 1.0 | 0.0 | 8 | evidence/hist/EV-HIST-001.md · M6 · 块式 → flow 写法（matrix） |
| 1.0 | 0.0 | 0.0 | 0.8 | 8 | evidence/conc/EV-CONC-001.md · M3 · 删掉一条 run_match_keys 声明（弱 |
| 0.0 | 0.15 | 0.6 | 1.0 | 56 | evidence/conc/EV-CONC-001.md · M1 · 删 artifact_sha256 |
| 1.0 | 0.25 | 0.0 | 0.0 | 337 | evidence/conc/EV-CONC-001.md · M6 · 缩进提升（id 多缩一格，改变嵌套归属） |

## 三、每个子目标 Top5 贡献者
### verdict_regime_disagreement
| # | card | op | point | sub | composite |
| 1 | atoms/conc/ATOM-CONC-FENCE-001.md | M5 | [命题 prop-2] claim_type: inference →  | 1.0 | 0.25 |
| 2 | atoms/conc/ATOM-CONC-FENCE-001.md | M6 | 缩进提升（id 多缩一格，改变嵌套归属） | 1.0 | 0.3 |
| 3 | atoms/conc/ATOM-CONC-LOCK-001.md | M5 | [命题 prop-2] claim_type: inference →  | 1.0 | 0.25 |
| 4 | atoms/conc/ATOM-CONC-LOCK-001.md | M6 | 缩进提升（id 多缩一格，改变嵌套归属） | 1.0 | 0.3 |
| 5 | atoms/conc/ATOM-CONC-RACE-001.md | M5 | [命题 prop-2] claim_type: inference →  | 1.0 | 0.25 |

### evidence_ambiguity
| # | card | op | point | sub | composite |
| 1 | evidence/hist/EV-HIST-001.md | M6 | 块式 → flow 写法（matrix） | 0.85 | 0.57 |
| 2 | evidence/mem/EV-MEM-032.md | M6 | 块式 → flow 写法（matrix） | 0.85 | 0.57 |
| 3 | evidence/mem/EV-MEM-033.md | M6 | 块式 → flow 写法（matrix） | 0.85 | 0.57 |
| 4 | evidence/mem/EV-MEM-034.md | M6 | 块式 → flow 写法（matrix） | 0.85 | 0.57 |
| 5 | evidence/mem/EV-MEM-035.md | M6 | 块式 → flow 写法（matrix） | 0.85 | 0.57 |

### rule_blind_spot
| # | card | op | point | sub | composite |
| 1 | evidence/conc/EV-CONC-001.md | M1 | 删 negative_controls | 1.0 | 0.4 |
| 2 | evidence/hist/EV-HIST-001.md | M6 | 块式 → flow 写法（matrix） | 1.0 | 0.57 |
| 3 | evidence/mem/EV-MEM-032.md | M6 | 块式 → flow 写法（matrix） | 1.0 | 0.57 |
| 4 | evidence/mem/EV-MEM-033.md | M6 | 块式 → flow 写法（matrix） | 1.0 | 0.57 |
| 5 | evidence/mem/EV-MEM-034.md | M6 | 块式 → flow 写法（matrix） | 1.0 | 0.57 |

### provenance_inconsistency
| # | card | op | point | sub | composite |
| 1 | evidence/conc/EV-CONC-001.md | M1 | 删 artifact_sha256 | 1.0 | 0.42 |
| 2 | evidence/conc/EV-CONC-001.md | M7 | sha256 改一位（8dd19bc6… → 0dd19bc6…） | 1.0 | 0.27 |
| 3 | evidence/conc/EV-CONC-002.md | M1 | 删 artifact_sha256 | 1.0 | 0.42 |
| 4 | evidence/conc/EV-CONC-002.md | M7 | sha256 改一位（8dd19bc6… → 0dd19bc6…） | 1.0 | 0.27 |
| 5 | evidence/conc/EV-CONC-003.md | M1 | 删 artifact_sha256 | 1.0 | 0.42 |

## 四、逃逸 mutation 排名
- 真逃逸（唯一）：`evidence/conc/EV-CONC-001.md · M1 · 删 negative_controls` composite=0.4 **排名 = 57 / 1406**（W1 默认权重下）
- 已知等效（8 条，剔出排序）：M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）、M6 · 块式 → flow 写法（matrix）
- 解读：W1 下真逃逸被 8 条等效（0.57，已判无害）与 57 条 M1 删 artifact_sha256（0.42，被 EV-FM-REQUIRED 薄拦截兜住）压过；改用 W2（rule_blind_spot 0.50）真逃逸升至第 1。权重取舍为 620 人拍板项（见 A1 §五）。

## 五、用途与限制
- 本工具只**排序**既有 1593 条，不生成新 mutation、不调 gate/replay（619 §六）。
- `ranked` 集合 = judgeable 且非等效 = 1406（与 v7 可判分母一致）。
- 攻击-验证**迭代**增益未测（A4 只写协议）；本排序即攻击方的「下一步该打谁」。
