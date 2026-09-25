# 640b · 总收尾报告（28 项涟漪清算 + 测试数字去耦合）

> 生成：2026-09-25。任务书：`_auto/inbox/640b.md`。

## 一、任务表

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| 0 | 开工快照 + 核对 28 项 | `640b_baseline.md`（逐项清单，与终扫一致） | ✅ |
| A1 | W2 数字单一权威源 | `tools/w2_authority_640b.py`（两路 + 交叉校验）+ 设计文档 + 6 例单测 | ✅ |
| A2 | 27 项断言去耦合 | 10 个工具 + 18 个测试文件改造 | ✅ |
| A3 | type:ignore 第 29 项 | **可避免 ⇒ 删除**（删后 mypy 仍 0 错；阈值维持 28 不抬） | ✅ |
| A4 | 全量 pytest 终验 | `640b_pytest_final.txt` | ✅ |
| E1 | 收工门禁 + 报告/status | 本报告 + `640_acceptance_report.md` 门禁节 + `status.json` | ✅ |

## 二、A1 权威源设计（核心）

- **两条路径**：`compute_w2_summary()`（事实源求解） vs `artifact_summary()`（读入库产物）；
  `summary()["consistent"]` 是交叉校验——这是 §三.1 要求的"不许自我证明"。
- **零导入铁律的兼容**：`independent_verifier_628` / `run_628_gate` 不允许 import 项目工具，
  它们改为**直读同一数据文件**（同一权威源，取数方式不同，均已在代码注明）。

## 三、A2 改造统计

| 层 | 数量 | 说明 |
|---|---|---|
| 工具常量/校验 | 10 个文件 | defense_chain（汇总 + **可信度口径**）、human_review_dashboard、dashboard_v2、run_628_gate、independent_verifier、mirror_symmetry、third_party、v2_flag、w2_projection×2、bridge_edge_impact |
| 测试断言 | 18 个文件 | 全部改为 `w2_authority` 动态取值或"现算/产物一致"型断言 |
| 模板/报告 | 7 份 | grounded_audit / dashboard×2 / independent_verifier / third_party / v2_flag / defense_chain 重生成 |

## 四、本轮额外定位并修复的**真因**（非过期数字）

1. **conftest 会话清理制造无主凭证**（`test_transparency_log_628` 反复红的真因）：
   会话结束**还原透明日志**却**保留**新建凭证 ⇒ 孤儿。修复：`data/vsa/` 未跟踪新凭证
   按运行时产物删除（凭证与日志同进同出）；
2. **env 泄漏**：`third_party.step4` 入册时显式清掉可能被测试泄漏的
   `CPPBIBLE_TRANSPARENCY_LOG`（否则入册写临时日志、凭证落生产 ⇒ 孤儿）；
3. **defense_chain 可信度口径落后**：写死 `PROP_CREDIBILITY=medium`，而 W2 内核按
   命题级人签给 `high` ⇒ 逐节点比对红。修复为与内核同口径；
4. **type:ignore 第 29 项**：640 A2 引入的 `roadmap_align_640.py` ignore **可避免**
   ⇒ 删除（真修，不抬阈值）。

## 五、§四.3 模拟验证结果（关键验收）

| 模拟 | 手段 | 结果 |
|---|---|---|
| A：仅改产物 | 翻转 1 节点（产物 80/41 vs 现算 79/42） | 12 红 **全部为漂移告警**（交叉校验按设计报警）；**写死数字型批量红 = 0** |
| B：两路同步偏移 | 产物翻转 + `W2_SIM_OFFSET=1` | 6 红，全部来自**另有独立自算 W2 的 6 处实现**与权威源不同步——同属漂移告警 |
| 还原 | 恢复产物 | 18 文件 133 项全绿 |

**结论**：原 28 项中**无一**因数字过期再次变红；剩余信号都是"两条独立路径不一致"
的真实告警——正是治理所要。

## 六、诚实登记（§五）

1. **语义后果（交 641 裁决）**：命题级人签使命题为 `high` 后，**误解即使被 approve
   （medium）也仍判 OUT**（medium < high）。这是模型推论，但暴露设计问题——
   "人审 approve 误解"是否应抬到 high？本轮**不改模型**，测试锁定当前行为并登记；
2. **6 处"自算 W2"的独立实现**（normalizer / v2 编译器 / gate 子进程 / vsa 结果等）
   仍是各自实现（这正是它们的独立性价值），但它们**不跟随权威源**——若未来 W2 演进，
   这些位置会作为"漂移告警"出现（预期行为，不是写死数字）；
3. **历史里程碑记录**（613/629/630/631/632 baseline 文档的 "IN114/OUT7"）保持不动，
   属时点快照（§三.2 冻结里程碑）；
4. 改造范围限于 28 项直接相关的测试与工具（§五.3），未扩大重构。

## 七、门禁与交人

- 静态：ruff 全绿 / mypy 438 文件 0 错 / merkle / tool_integrity / 受控目录 —— 见 §八；
- pytest 全量：`data/640b_pytest_final.txt`（见 `640_acceptance_report.md` 门禁节）；
- 交人：push 不代执行；641 优先裁决"误解 approve 可信度档"。
