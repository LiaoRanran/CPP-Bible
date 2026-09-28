# 658 验收报告

> 一键复算：`python tools/run_658_gate.py`（机器报告见 `data/658_gate_report.md`，状态见 `data/658_gate_status.json`）。
> 门禁结果：**PASS**（L0 5/5，L1 失败 0）。提交数 9，变更 48 文件。

## 一、闭环五问（I 段自检）

### 1. 改了什么？
| 段 | 交付 | 关键文件 |
|---|---|---|
| A 外部效度四层 | A1 真实缺陷夹具 / A2 盲化 holdout / A3 独立生成协议 / A4 外部 corpus 清单 / A5 指标分层 | `data/defect_fixtures/defects.json`、`data/holdout/holdout.json`、`docs/independent_generation_658.md`、`data/external_corpus_658.md`、`docs/metric_layers_658.md` |
| B 门禁两层 | L0 REDLINE / L1 ADVISORY 声明式分层 + 校验器 | `tools/gate_tiers_658.json`、`docs/gate_tiers_658.md`、`tools/gate_tier_check_658.py` |
| C boundary 拆概念 | provenance（实验来源）vs semantic scope（语义边界）拆分，受控零改动只读提取 | `docs/boundary_scope_split_658.md`、`tools/boundary_scope_658.py`、`data/boundary_provenance_658.json` |
| D 元状态可验证 | 反自证对账器 + canonical baseline + AGENT/NEXT_LLM GENERATED 块 | `tools/status_reconciler_658.py`、`data/baseline.json` |
| E 口径收敛+交人清理 | DCO 转硬 + 口径差登记 + 交人清单 | `.github/workflows/dco.yml`、`docs/caliber_convergence_658.md`、`data/658_handoff_pending.md` |
| F 逃逸率口径 | 明确 0.0711% 是对 v7 变异分布的漏检率、非本书错误率 | `README.md`、`web/data/status.json`、`web/index.html` |
| G Research Protocol | 实验宪法 v0.1（16 文件，冻结 RQ/数据集/流程） | `research/*` |
| H v41 新方向 | 轨迹层 spec + 反事实引文原型 + 小核查器种子 | `docs/trace_layer_spec_658.md`、`tools/counterfactual_citation_658.py`、`data/small_verifier_seed/*` |

### 2. 怎么验证？
- 一键门禁 `run_658_gate.py`：S0 元状态对账 / S1 门禁分层 / S2 真实缺陷检出 / S3 盲化 holdout / S4 边界 provenance / S5 research 骨架 / S6 单元测试 —— **全部 PASS**。
- 单元测试：`tests/test_status_reconciler_658.py`、`tests/test_external_validity_658.py` 通过。
- DCO：658 各提交 `git commit -s`，`dco_check_657.py` 对 `origin/master..HEAD` 全区间 **0 不合规**。

### 3. 红线有没有碰？
- **受控目录（atoms/evidence/Examples/Book）零改动**：`git diff --name-only origin/master..HEAD` 过滤为空 ✅
- **452 条账本零改动**：过滤为空 ✅
- 反自证：reconciler 源码无 `import gate_engine / four_state_verdict / queyi`（测试断言）✅

### 4. 还有哪些没做？（诚实登记）
见 `data/658_handoff_pending.md`：前端缺陷 #1/#4/#5、rebuild-manifest、CRLF 全量 renormalize、
slow 测试去写死、queyi-verifier move+push、A3 独立生成未跑、C4 semantic scope 未落 frontmatter、
口径差（规则 67/63、节点 178/121）待权威源。

### 5. 下一个会话第一步？
1. `python tools/status_reconciler_658.py --check` —— 若 META-STATE-CONFLICT 先停（元状态优先）。
2. `python tools/run_658_gate.py` —— 复算 658 门禁。
3. 按 `data/658_handoff_pending.md` 从交人项择一推进（建议先做 #5，成本最低）。

## 二、诚实边界
- mutation core 97.3% 是 **Test adequacy**，非外部效度；真实缺陷检出以 A1/A2 实测为准。
- A2 盲化 holdout 当前为 **blind**（演示 reveal 已重置），正式 reveal 留验收时执行且不可逆。
- 本批未训练任何模型（H3 仅备数据格式）。
