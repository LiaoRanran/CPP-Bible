# 647 开工基线（阶段 0.1）

> 任务书：`_auto/inbox/647.md`。开工时刻实测，**数字均可复算**（不给"大概"）。
> 原则：本批=「硬骨头逐个啃」，每个任务先写回滚方案（见 `data/647_rollback_plan.md`）。

## 一、仓库状态

| 项 | 值 | 采集方式 |
|---|---|---|
| HEAD | `f36b59c8`（646 C3：status.json last_commit 收敛） | `git log --oneline -1` |
| 未 push 提交数 | **88** | `git rev-list --count origin/master..HEAD` |
| 分支 | `master`（跟踪 `origin/master`） | `git status` |
| 工作区 | 脏项：既有遗留改（629/630/631 基线、`tools/queyi_data_models_645.py` 等）+ 1 未跟踪锁文件 | `git status --porcelain` |
| 总提交数 | 1927 | `git rev-list --count HEAD` |

**工作区脏项说明（诚实）**：`data/629_baseline.md`、`data/630_baseline.*`、`data/631_baseline.*`、
`data/*.jsonl|html` 等为本批**之前**遗留（645/646 已登记「本批不动」）；`data/.622_apply.lock` 为 622
沙箱锁残留。647 不清理这些遗留（避免与 645/646 登记冲突），仅在验收报告登记。

## 二、关键工程指标

| 指标 | 值 | 说明 |
|---|---|---|
| 工具数（`tools/*.py`） | **524** | 其中 646 工具 12 + 646 门禁 1 |
| 测试文件数（`tests/test_*.py`） | **521** | 646 新增 13 个 |
| 现有规则数 | **67** | `calibration_tracker_636.rules()` 实测 |
| 真实原子卡数 | **27** | `atoms/**/*.md` − `README.md` |
| verified 卡数 | **23** | `conflict_detector_636.verified_cards()` |
| Authority 判决事件 | **452** | `data/authority/decision_event_v2_ledger.jsonl` 行数 |
| 人审队列 | `data/autoimmune_human_queue_631.jsonl` | anti-windup 消费对象（642 记 65 项） |
| CORE_TOOLS | **5** | gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible |
| RULER_TOOLS（尺子） | **22** | 625 D1 起 |

## 三、四个硬骨头的开工现状（核对 647 §一）

### 3.1 信任根（A 线，最硬的骨头）

| # | 现状 | 复核结果 |
|---|---|---|
| A1 | `tool_integrity.verify_supply_chain()` 缺文件只 **warning** | ✅ 复现：`SUPPLY_CHAIN_FILES` 5 个**当前全部存在**（`poison_exemptions.yaml` / `poison_surface_map.json` / `governance_docs_manifest.json` / `merkle_roots.json` / `layout.json`）⇒ 当前绿，但**删任一文件不改 exit code**（642 B3 FO-A 实测 exit=0） |
| A2 | `DecisionEvent.from_dict()` 缺字段用默认、未知字段静默忽略 | ✅ 复现：`from_dict({})` ⇒ `result=APPROVE` + `review_method=BATCH_AUTH` + `decision_origin=human_observed`（642 B3 FO-B，高危） |
| A3 | `verifier_closure_641` 闭包 = 23 文件 | ✅ 现状：闭包只跟 `tools/*.py` import 图 + 3 个配置信任根 glob + `data/supply_chain/*`；**不含 67 条规则文件 / Authority schema / 透明日志 anchor / checksum baseline / 证据索引** |
| A4 | 外部锚**不存在** | ✅ 无 `external_anchor_*` 工具；透明日志 anchor 在本地 |

### 3.2 保护器（B 线）

| 保护器 | 642 状态 | 647 目标 |
|---|---|---|
| 冲突检测 `conflict_detector_642` | flag 模式（`block` 显式未实现，exit 2） | 真上岗，高置信 block |
| anti-windup `anti_windup_642` | 只标记（`frozen` 不丢请求） | 真上岗，冻结超预算队列 |
| blind_protocol `blind_protocol_642` | 新开单盲化 + 历史只标记（258 违规） | 新判决**强制**盲化 |
| 校准追踪 `calibration_tracker_642` | 只记账，降级动作 `enabled=False` | 超阈**降级/暂停** |
| MDL 准入 `mdl_gate_642` | 只对新规则出结论（侧车元数据） | 新规则**必须过 MDL 才能上线** |

### 3.3 仓库拆分（C 线）

- 645 D 阶段调研方案：`git subtree split`（保留历史）；
- core 文件清单：`queyi_core_v10_641` / `queyi_core_cpp_641` / `queyi_core_toy_641` / `verifier_closure_641` / 证据层 / 智能层 / 头部层 / 保护器；
- **未执行**（本批执行）。

### 3.4 工具合并（D 线）

- 646 B4 方案：15 → 10（3 组合并）：
  1. `three_layer_orchestrator_645` + `coupling_feedback_645` + `coupling_effect_645` → 1；
  2. `evidence_grading_645` + `evidence_sufficiency_645` → 1；
  3. `loop_r5_runner_645` + `rule_error_tracker_645` + `rule_aging_detector_645` → 1；
- **未执行**（646 明确：删工具会使 645 测试套件整体红 ⇒ 需同步改测试）。本批执行。

## 四、本批开工硬边界（对照 647 §零）

1. 5 个 CORE_TOOLS **判决逻辑零改动**（A1 改 `tool_integrity.py` 属例外，显式登记）；
2. 受控目录（`atoms/` `evidence/` `Examples/` `Book/`）**零污染**；
3. 不代签人审、不 golden accept；
4. **本轮不 push**（ahead=88，交人统一 push）；
5. 高风险（仓库拆分 / 保护器上岗 / 信任根修改）**先沙箱**，**回滚方案先写**；
6. 找不到根因/做不到的**诚实登记**，不编造、不"改到绿"。

## 五、采集命令（可复算）

```text
git --no-pager log --oneline -1                 # HEAD
git rev-list --count origin/master..HEAD        # ahead
python tools/calibration_tracker_636.py --json  # rules=67
python tools/conflict_detector_636.py --json    # verified_cards=23
wc -l data/authority/decision_event_v2_ledger.jsonl   # 452
python -c "import sys;sys.path.insert(0,'tools');import tool_integrity as t;print(len(t.CORE_TOOLS),len(t.RULER_TOOLS))"
```
