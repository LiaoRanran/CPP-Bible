# 知识资产层数据质量报告（2026-09-20 化债复算）

## 一、原子卡（atoms/）

| 指标 | 值 | 验证 |
|---|---|---|
| 原子卡总数 | 28 张 | ✓ 与记录一致 |
| 命题总数 | 79 条 | ✓ observation 50 / inference 29 |
| 每卡命题数 | 2-4 条 | ✓ 无单命题卡 |
| 活性锚（liveness） | 0 条已填 | ⚠️ 50 条 observation 命题全缺活性锚 |
| verified_by_oracle | 0 张已填 | ⚠️ 全库 83 张卡缺 verified_by_oracle |
| 卡面可信度字段 | 0 张有 | ⚠️ MIS 卡面 0 张有 verified_by/machine_verified |

### 1.1 命题完整性（592 T4 台账）

- 79 命题完整性校验（data/prop_network_inventory.md，151 行）
- 闭包异常命题：0 条
- 孤立命题：0 条（prop_closure stats：孤立 0）
- 连通分量：26 个（prop_closure stats）
- 闭包 avg 6.076 / max 8 / min 4

### 1.2 知识债（如实登记）

- **observation 命题 50 条全缺活性锚**：活性锚是"命题被实测验证过"的证据，当前 0 条已填
- **verified_by_oracle 0 张卡填**：83 张卡（28 原子卡 + 55 其他卡）缺 oracle 验证
- **MIS 卡面 0 张有可信度字段**：42 个 MIS 全 low（人审后 35 个升到 medium，但卡面字段未更新）
- **论证图碎片化**：11 个连通分量，最大仅覆盖 66%（610 C 漏洞检测发现）
- **4 条命题无攻击者**：无任何 MIS 关联，无法通过论证框架验证

## 二、证据卡（evidence/）

| 指标 | 值 | 验证 |
|---|---|---|
| 证据卡总数 | 57 张 | ✓ 与记录一致 |
| MIS 误解库 | 42 个（带 related_atoms） | ✓ 596 独立复算：79 MIS → 42 带 related_atoms |
| MIS 总数 | 79 个 | ✓ 592 台账：MIS 实为 79 条（非 80，差 1） |
| MIS refutations | 160 条反驳文本 | ✓ 593 调研实测 |
| MIS→命题候选边 | 194 条 | ✓ 596 独立复算 |
| 命题→MIS 对称边 | 194 条 | ✓ 596 独立复算 |
| 候选边总数 | 388 条 | ✓ 人审全量完成 |

### 2.1 MIS 出处锚（582 N4）

- 26 条 MIS 连文件名级出处锚都没有（582 调研实测）
- lexical_present（只证可达）：只报不判
- check_citations.py 行为不变

### 2.2 MIS 关联统计

- 42 个带 related_atoms 的 MIS → 194 条 MIS→命题边
- 25 张关联原子卡
- 0 悬空
- 每 MIS 2-12 条（avg 4.619）
- 节点 121（79 命题 + 42 误解）
- 原子卡侧 8 张有 misconceptions 反向字段（MIS 侧 0 张）
- 代价：2 张卡的 4 条命题无任何误解攻击（审计已标注）

## 三、示例代码（Examples/）

| 指标 | 值 | 验证 |
|---|---|---|
| C++ 文件 | 1054 个 | ✓ 实跑统计 |
| 汇编文件 | 404 个 | ✓ 实跑统计 |
| 总文件数 | 1458 个 | ✓ Merkle 台账 1541（含其他文件） |
| Merkle 覆盖 | ✅ | ✓ data/supply_chain/merkle_roots.json |

### 3.1 M1 TCE 工件

- Examples/atoms/_atom_fence_vs_atomic.nc1.cpp（M1 TCE 工件）
- 本轮化债修复：Merkle 台账文件数 1540→1541（该工件未同步）
- 已运行 tool_integrity.py --update 重钉

## 四、参考文档（References/）

| 指标 | 值 | 验证 |
|---|---|---|
| Markdown 文档 | 443 份 | ✓ 实跑统计 |
| 导航文档 | 30 份 | ✓ References/00_导航/ |
| 架构演进文档 | ? 份 | References/architecture_架构演进/ |
| 异族调研 | 9 轮（_arch_v10-v18） | ✓ 根目录保留最近 9 轮 |
| 归档旧调研 | 9 轮（_arch_v2-v9） | ✓ 本轮化债归档到 _archive/old_research/ |
| 归档旧广告 | 7 轮（_adv_v61-v96） | ✓ 本轮化债归档到 _archive/old_advocacy/ |

### 4.1 导航文档结构（30 份，4 层组织）

- 第 0 层：00_总索引
- 第 1 层：01-03（项目健康度/工具分类索引/测试分类索引）
- 第 2 层：04-09（六维度状态快照：论证层/机械判决层/信任根层/度量诚实层/知识资产层/人审层）
- 第 3 层：10-18（详情台账：tests 分类/工具链全景/论证层详情/人审层详情/信任根层详情）
- 第 4 层：19-29（产品经理报告/时间线/债务清单/工具链全景/测试覆盖率/六维度演进/关键数字速查/对外发布准备/仓库结构全景）

### 4.2 本轮化债新增/更新

- 新增：29_仓库结构全景_20260920.md
- 新增（data/）：人审/论证框架/信任根/度量诚实化/机械判决层 5 个数据质量报告
- 更新：00_总索引（待 611 完成后统一更新）
- 归档：_arch_v2-v9 → _archive/old_research/
- 归档：_adv_v61-v96 → _archive/old_advocacy/

## 五、工具链（tools/）

| 指标 | 值 | 验证 |
|---|---|---|
| Python 工具 | 151 个 | ✓ 实跑统计 |
| CORE 核心工具 | 5 个 | gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible |
| 测试文件 | 137 个 | ✓ 实跑统计 |
| 测试用例 | ~1250 | ✓ 估算 |
| 归档旧工具 | 49 个 | ✓ 608 化债27 归档到 _archive/old_tools/ |

### 5.1 工具链分层（6 层架构）

1. CORE 核心（5）：判决/重放/攻击/工具链/主入口
2. 变异测试（7）：mutation_fuzz / shape_audit / selfcheck
3. 论证框架（10）：weighted_af_solver / attack_edge_generator / prop_closure / prop_asof / oracle_rotation
4. 人审工具链（9）：human_review_queue / confirm / pre_annotate / dashboard / quality
5. 信任根（9）：tool_integrity / merkle_integrity / supply_chain / governance_doc_guard / open_timestamps
6. 度量收集（8）：metrics_collector / metrics_608 / metrics_610 / escape_rate_trend
7. 智能原型（5）：defense_chain / argument_vulnerability / proposition_liveness_audit
8. 编译验证（6）：build_reproducibility / replay_invariants
9. 其他（86）：各类审计、台账、探针、辅助工具

## 六、待改进项

1. **活性锚 0/50**：50 条 observation 命题全缺活性锚。建议下批补全（需人审确认每条命题的实测验证证据）。
2. **verified_by_oracle 0/83**：全库 83 张卡缺 oracle 验证。这是人审权力，永不自动。建议分批补全（优先补高优先级卡）。
3. **论证图碎片化**：11 个连通分量，最大仅覆盖 66%。建议下批补全桥接攻击边（611 线 C 可能正在做）。
4. **4 条孤立命题**：无任何 MIS 关联。建议补全 MIS 关联或标记为"无需攻击验证"。
5. **MIS 出处锚 26/79 缺失**：26 条 MIS 连文件名级出处锚都没有。建议下批补全（582 N4 已给方案）。
6. **导航总索引待更新**：本轮化债新增 29_仓库结构全景 + 5 个数据质量报告，待 611 完成后统一更新 00_总索引。
7. **未提交变更 260 个**：含 611 线B1 未提交工作 + 我的化债 + 历史未提交。待 611 状态确认后统一处理 commit 和 push。

---

*生成时间：2026-09-20 | 生成工具：MainAgent 化债复算 | 数据来源：atoms/ evidence/ Examples/ References/ tools/（实跑统计）*
