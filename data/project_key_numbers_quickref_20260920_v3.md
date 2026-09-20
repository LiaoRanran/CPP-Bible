# 阙疑项目关键数字速查表（2026-09-20 v3 · 613 进行中 + CI 化债后）

> 本文件由 MainAgent 化债轮自动生成，所有数字可复算。口径与最新收工报告一致。
> 613 苦力正在跑，commit/工具/测试数仍在增长，本快照为 2026-09-20 23:55。

---

## 一、项目规模

| 指标 | 数字 | 备注 |
|------|------|------|
| 总 commit 数 | **1424** | 截至 2026-09-20 23:55（613 进行中） |
| 最近 7 天 commit | **436** | 日均 62 个（608-613 巨型批次驱动） |
| 最近 1 天 commit | **123** | 612 + 613 + CI 化债 |
| 工具数（tools/*.py） | **190** | 含 CORE 5 + 各批次新工具（613 新增中） |
| 测试文件数（tests/test_*.py） | **168** | fast + slow |
| 原子卡 | **28** | atoms/**/ATOM-*.md（含子目录 conc/hist/lang/mem/ub） |
| 证据卡 | **57** | evidence/**/EV-*.md |
| 命题总数 | **79** | observation 50 / inference 29 |
| MIS 误解库 | **80** | 共 80 文件，其中 42 带 related_atoms |
| 人审候选边 | **388** | 194 MIS→命题 + 194 对称（已全量人审：354 approve / 34 modify / 0 reject） |
| Book 章节 | **151** | Book/**/*.md |
| data 文件 | **413** | data/**/* |
| References 文档 | **446** | References/**/*.md |
| 调研目录 | **19** | _arch_v2 到 _arch_v18（含 v2_round2） |
| _* 目录 | **31** | 27 跟踪 + 4 忽略 |

---

## 二、核心门禁（基准数字，611 后冻结，613 完成后更新）

| 门禁 | 结果 | 关键数字 |
|------|------|---------|
| **gate_engine --check** | ✅ exit 0 | 63 规则 / 191 命中（block=0 warn=186 advice=5） |
| **poison_drill** | ✅ exit 0 | 124/124 · RULE-COVERAGE 39/63 · 表观 100% · 诚实 95.2%(60/63) |
| **atom_evidence_replay --check** | ✅ exit 0 | confirm=56 refute=0 infra_error=0 |
| **tool_integrity --check** | ✅ exit 0 | 5 核心工具 + 2 测试配置 + merkle 一致 |
| **governance verify** | ✅ exit 0 | 台账已纳入 613 提示词（f78c4f7） |
| **pytest fast（本地 -n0）** | ✅ 全绿 | 541+ passed / 5 snapshots |
| **pytest fast（CI -n16）** | ⚠️ 已修复待验证 | test_touch_normalization_same_lock 平台差异（e997d14），等 #606 |
| **pytest slow** | ⚠️ 1 红 | test_golden_lock_json（预期，golden 待人工 accept，warn 136→186） |
| **ruff** | ✅ 全绿 | 0 错误 |
| **mypy** | ✅ 0 错误 | CI 化债后全绿（48c63e3） |

### CI 四 job 状态（#605 及之前持续红，#606 含 pytest 修复待验证）

| Job | #605 状态 | 根因 | 修复状态 |
|-----|-----------|------|---------|
| **pytest** | ❌ failure | test_touch_normalization_same_lock 平台差异（Linux ext4 大小写敏感） | ✅ 已修复（e997d14），等 #606 验证 |
| **replay** | ✅ success | — | — |
| **gate** | ❌ failure | golden_lock exit 1，OBSERVATION-LIVENESS warn=50（活性锚补全中间态） | ⏳ 613 线 A 会修 |
| **quality** | ❌ failure | D5 基准文件系统失效（8 章引用缺失 + 22 孤儿文件，历史遗留） | ⏳ 613 线 B 会修 |

---

## 三、论证层（W2 加权 AF）

### 3.1 判决结果（双口径同时报告，不选边，待用户裁决）

| 口径 | IN | OUT | UNDEC | 击败边 | 说明 |
|------|----|-----|-------|--------|------|
| **keep-low**（入库权威，默认） | 114 | 7 | 0 | 17/388 | modify 保持 low，7 个 MIS 因置信度不足被击败 |
| **upgrade-medium**（609 A3） | 121 | 0 | 0 | 0/388 | modify 升 medium，攻击性被抽空 |
| **divergence** | 7 节点 | — | — | — | 差异即 OUT 的 7 个 MIS |

### 3.2 OUT 的 7 个 MIS（keep-low 口径）

MIS-LANG-001、MIS-MEM-001、MIS-MEM-003、MIS-UB-001、MIS-UB-004、MIS-UB-008、MIS-UB-014

> 关键发现：这 7 个 MIS 的所有攻击边全部是 `modify`（保持 low 置信度），不是 `approve`——这是它们被 W2 判为 OUT 的原因。

### 3.3 论证图结构（611 数据，613 线 D 深化中）

| 指标 | 数字 |
|------|------|
| 节点总数 | 121（79 命题 + 42 MIS） |
| 连通分量 | 11 |
| 孤立节点 | 4 |
| 最大分量 | 80 节点（覆盖 66.1%） |
| 桥接候选 | 98 条（全 weak） |
| 加桥 what-if | 分量 11→7、覆盖 66.1%→80.2%、判决变化 0 |
| 承重节点 | 107/121 |
| 最大级联深度 | 1（论证图局部稳定，无深度级联风险） |

---

## 四、人审层（全量完成，项目最大里程碑）

| 指标 | 数字 |
|------|------|
| 候选边总数 | 388 |
| 已审 | **388（100%）** |
| approve | 354 |
| modify | 34 |
| reject | 0 |
| 审核者 | LiaoRanran（单人） |
| 平均理由长度 | 47-80 字符 |
| rubber-stamp | 0 |
| 耗时 | 约 13 分钟（MIS 群组级聚合，非边级 1.89 小时） |

---

## 五、学习者镜像（612 原型，613 线 C 实装中）

| 指标 | 数字 |
|------|------|
| KC（知识组件） | 27（对应 27 原子卡） |
| BKT 参数 | 四参数 + 网格 MLE 拟合 |
| 初始掌握度 | 27 × 0.1 |
| 推荐硬约束 | 前置未达 0.5 一律不推荐 |
| 仪表盘 | 自包含 HTML 四模块（热力图/进度曲线/推荐路径/统计） |

---

## 六、信任根层

| 指标 | 状态 |
|------|------|
| tool_integrity | ✅ 5 核心 + 2 测试配置 + merkle |
| Merkle 完整性 | ✅ 已建（merkle_roots.json） |
| in-toto 溯源 | 📋 调研完成（_arch_v16），待落地 |
| OpenTimestamps | 📋 工具已建（opentimestamps_anchor.py），缺真实上链 |
| governance 台账 | ✅ 505 文档（含 _arch_*/** 156 + _auto/inbox 4 + 根级 PM_* 1） |
| 弱化指令扫描 | high=55 / medium=186 / low=38（high 待语义人审） |

---

## 七、度量诚实化

| 指标 | 数字 |
|------|------|
| v7 权威基线 | 1593 变体 / blocked 1405 / escaped 1 / n_a 179 / equivalent 8 |
| 可判分母 | 1406 |
| 逃逸率 | 1/1406 = 0.0711% |
| C-P95 上界 | [0.0018%, 0.3956%]（Clopper-Pearson 95% CI） |
| 唯一 escaped | M1·EV-CONC-001（冻结 TCE，待攻坚） |
| replay 假阳性上界 | 5.21%（56 张卡 0 假阳性） |
| 要宣称 ≤5% 需 | 59 张卡 |
| 要宣称 ≤2% 需 | 149 张卡 |

---

## 八、六维度成熟度评分（2026-09-20，610 后）

| 维度 | 分数 | 说明 |
|------|------|------|
| 论证层 | 7.0 | W2 已落地，但 grounded 从退化到可用刚起步 |
| 机械判决 | 9.2 | 契约逃逸 1/1406，缺口全部显式登记 |
| 信任根 | 8.5 | Merkle+in-toto+OTS 调研完成，待真实上链 |
| 度量 | 8.5 | 统计上界+收敛曲线+方差声明齐全 |
| 知识资产 | 7.5 | 28 原子卡+57 证据卡+79 命题，oracle 验证 0/83 |
| 人审 | 7.8 | 388/388 全量完成，但单人评审+无 review_seconds |
| **平均** | **8.1** | 已达"基建+智能并行"阶段（阈值 8.0） |

---

## 九、已知债务清单（按优先级）

### P0（阻塞 CI 全绿）
1. ~~pytest 平台差异~~ → ✅ 已修复（e997d14），等 #606 验证
2. gate golden_lock OBSERVATION-LIVENESS warn=50 → ⏳ 613 线 A
3. quality D5 基准文件系统失效 → ⏳ 613 线 B

### P1（影响可信度）
4. oracle 验证 0/83 卡（56 证据 + 27 原子）
5. 活性锚缺 50 条 observation 命题
6. modify 口径冲突（keep-low vs upgrade-medium）待用户裁决
7. golden_lock warn 136→186 待人工 accept

### P2（整理类）
8. _arch_v2 到 _arch_v9 归档到 _archive/old_research/（19 个调研目录）
9. _adv_v80/probes/ 约 192 个 CRLF 假脏文件（历史遗留）
10. D5 基准文件重建（8 章引用缺失 + 22 孤儿文件）
11. 人审 schema 缺 review_seconds（耗时不可回溯）

---

## 十、路线图与里程碑

### 已完成里程碑
- ✅ 560-574：基础门禁（gate/poison/replay/integrity）
- ✅ 575-589：变异测试体系（M1-M7 算子 + v7 基线 + 等价变异体判别）
- ✅ 590-597：异族调研（_arch_v10 到 _arch_v17，9 轮）
- ✅ 598-602：信任根增强（Merkle + governance + 人审通道）
- ✅ 603-607：人审全量完成（388/388）+ 论证层 W2 落地
- ✅ 608-612：学习者镜像原型 + 辩护链推理 + 论证漏洞检测
- ✅ CI 化债：行尾修复 + mypy 189→0 + pytest 平台差异修复

### 进行中
- 🔄 613：CI 全绿攻坚 + 学习者镜像实装 + 论证层落地 + 信任根上链

### 下一步
- ⏳ 614+：基于 613 结果的深化（M1 TCE 攻坚 / M6 落地 / 电子领域扩展准备）
- ⏳ 包装层：内核成熟后做漂亮简洁的包装层（用户已确认先内核后包装）
- ⏳ 领域扩展：C++ → 电子 → 金融（确定性系统→半确定系统→概率系统）

---

*本文件由 MainAgent 化债轮生成，所有数字可复算。下次更新：613 完成后。*
