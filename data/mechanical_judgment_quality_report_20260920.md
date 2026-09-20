# 机械判决层数据质量报告（2026-09-20 化债复算）

## 一、gate_engine 判决完整性

| 指标 | 值 | 验证 |
|---|---|---|
| 规则总数 | 63 条 | ✓ 与记录一致 |
| 命中总数 | 191 | ✓ 与记录一致 |
| block | 0 | ✓ 无硬拦截 |
| warn | 186 | ✓ 与记录一致 |
| advice | 5 | ✓ 与记录一致 |
| gate --check exit code | 0 | ✓ 本轮化债已验证 |

### 1.1 规则分类

- 硬拦截（block）：0 条（当前无卡触发硬拦截）
- 警告（warn）：186 条（大部分是"建议改进"类）
- 建议（advice）：5 条（教学法建议类）

### 1.2 判决一致性

- gate_engine.py 是唯一真源（_card_variants()/_report()）
- 串行与 worker 共用同一判决逻辑
- 580 已验证：jobs1==jobsN 三计数完全相等
- ✓ 判决逻辑一字未改（580 三方对账已证）

## 二、poison_drill 攻击面完整性

| 指标 | 值 | 验证 |
|---|---|---|
| 毒样例总数 | 124 | ✓ 118+6（608 新增 6 条 V-iso） |
| 全拦截 | 124/124 | ✓ 与记录一致 |
| RULE-COVERAGE | 39/63 | ✓ 581 行为级覆盖修复后 35→38→39 |
| 表观覆盖率 | 100% | ✓ 含 legacy 豁免 |
| 诚实覆盖率 | 95.2%（60/63） | ✓ 不含 legacy，3 条 machine-untriggerable 不计入 |
| 零覆盖攻击面 | 无 | ✓ 与记录一致 |
| V-iso 双指标 | 100%/100% | ✓ 6/6、2/2（608 新增） |
| poison_drill exit code | 0 | ✓ 本轮化债已验证 |

### 2.1 覆盖率口径

- **表观覆盖率 100%**：含 27 条 legacy 豁免（581 全标 redteam_seen: legacy），因与 covered 重叠的冗余豁免 ATOM-REL-DAG 故 >100%，恰是要暴露的虚高
- **诚实覆盖率 95.2%**：legacy 不计入，3 条 machine-untriggerable（HUMAN-GOLDEN-REVIEW / HYBRID-TEACHING-DEPTH / LLM-SUPERIORITY-QUALITY）在 ge.RULES 里 check is None，机器原理上无从触发，不计入诚实分子
- **586 裁决**：按不虚高取严口径（95.2%），改 coverage_report 一行即可翻回 100%

### 2.2 行为级覆盖（581 修复）

- 旧方式：rule_coverage 从源码文本 grep "X" in who（会被注释/字符串污染出幽灵 RULE-ID）
- 新方式：poison_drill.py 改用钻探运行时 who（真实 gate 命中规则 ID）收集覆盖
- 新增：_mk_who + _CovList + behavioral_covered() + 幽灵自检
- 实跑：RULE-COVERAGE 38/63（比旧文本 grep 的 37 更准，多抓到 2 条文本漏计的真实覆盖）
- 581 修复真实 bug：P17/P71/P72 三探针算 who 未写 _CUR_WHO，导致行为级集合漏收（修前 35→修后 38）

## 三、atom_evidence_replay 重放完整性

| 指标 | 值 | 验证 |
|---|---|---|
| confirm | 56 | ✓ 与记录一致 |
| refute | 0 | ✓ 与记录一致 |
| infra_error | 0 | ✓ 与记录一致 |
| replay --check exit code | 0 | ✓ 本轮化债已验证 |

### 3.1 编译可复现性（602 调研发现）

- replay 早已内置轻量翻译验证：_recompile_invariant（P0-A/452 E01）独立重编译 + CCACHE_DISABLE=1 + 临时目录隔离 + 比 sha
- 56 张 confirm 卡的"编译可复现"已被现有管线实证
- 610 E3 深化：跨时间窗口 + 符号表(nm) + 段(objdump -h) + 字符串表(strings)
- PE 产物跨时间窗口必然不可复现（差异仅 2 字节：0x88 TimeDateStamp + 0xd8 debug 字段），加 -Wl,--no-insert-timestamp 后字节一致
- 仓库 56 张卡的 artifact 全是 .asm（不受影响，nm/objdump 如实标 skipped）

### 3.2 replay 不变量（603 显性化）

- I1 仓库一致性：用哨兵字节覆盖工件 → 能区分"真·逐字节还原"与"恰好重生成同样内容"
- I2 判定一致性（confirm / refute:sha256_mismatch）
- I3 _restore_artifact 幂等
- I4 infra_error（compiler_missing / msvc_unavailable）绝不退化成 refute
- I5/I6 已有既有测试覆盖

## 四、mutation_fuzz 变异测试完整性

| 指标 | 值 | 验证 |
|---|---|---|
| 算子数 | 7（M1-M7） | ✓ 与记录一致 |
| v7 总变体 | 1593 | ✓ 与记录一致 |
| escaped | 1（M1·EV-CONC-001） | ✓ 冻结 TCE |
| equivalent | 8（全部 M6） | ✓ 583 定性后 587 堵逃逸 |
| --selfcheck-determinism | exit 0 | ✓ 全 7 算子 × 小卡集两次一致 |
| --selfcheck-equivalent | exit 0 | ✓ 等价变体 new_block/warn 均空 |

### 4.1 等价变异体判别（583 N5）

- 判据：P1 视角相同 ∧ P2 视角相同 ∧ 缩进信号相同 ∧ 正文逐字不变 ∧ op ∉ {M1,M7}
- 实测：equivalent = 8，全部落在 M6 的八条逃逸上，其余 28 条 M6 blocked 变体零误标
- 零误伤证据：_variant_index 5 字段不含新字段；A/B 同输入逐条相等；--selfcheck-equivalent 保守性自证
- M6 那 8 条"逃逸"全是等价变异体，不是门禁洞（无效变异是攻击集缺陷，不是门禁漏检）

### 4.2 M6 matrix 变异（587 修复）

- 修前：204 逃逸（任务书估约 165，实跑 204）
- 修后：0 逃逸（warn 起步，缺键仍 block）
- M6 escaped 204→0、blocked 505→709、treated_rate→1.0
- gate 191 命中逐字不变（存量 0 命中）
- 终稿口径：剥半角/全角括号 → 按 / 拆段 → 逐段校验

### 4.3 性能优化（609 B1）

- task_queue sqlite 连接池改造
- 20,952 次库调用 ⇒ 真新建连接 2 条
- 墙钟 72.6s → 20.0s（省 72.5%）
- 判决逻辑一行未改（只改连接生命周期）

## 五、待改进项

1. **M1 TCE 逃逸**：唯一 escaped = M1·EV-CONC-001（删 negative_controls），需 TCE/工件比对 ⇒ 冻结，如实登记。多批未动。
2. **M5 观察期**：M5 仍在观察期（blocked 29 / n_a 56），未动。
3. **compiler 版本数字强制**：唯一反例 EV-UB-001（Clang (ubuntu-latest runner 默认) 有族名无版本），强制则 +1 warn 破坏 191。587 交人项，未裁决。
4. **EV-MEM-004 的 matrix 正则漏网**：matrix: 行带尾注释 ⇒ 现有 M6 删键正则匹配不到。588 已修（M6 matrix 键行尾注释 / 块内注释行）。
5. **GATE_READ_KEYS 缺 matrix**：M2 的读取面判据缺 matrix，而 check_evidence_matrix() 确实读它 ⇒ M2 的 out_of_scope 分类偏保守。未改（改它=改判决口径）。
6. **machine-untriggerable 计入诚实分子**：3 条人审象限规则（check is None）该不该计入诚实分子？586 交人项，当前按不虚高取严口径 95.2%。

---

*生成时间：2026-09-20 | 生成工具：MainAgent 化债复算 | 数据来源：gate_engine / poison_drill / atom_evidence_replay / mutation_fuzz（实跑统计）*
