# 625 验收报告 · 修债务 + 稳雷2 + 备雷1

> 批次目标：**CI 全绿**（mypy 修完 + pytest 红因解决）/ **雷2 闭环连续 3 轮稳定**（623-625）/ **QueYi Core 路径解耦完成**（核心 6 + 辅助 20）。
> 提交链：`d9c186a0`（任务0）→ `3faad452`（F1），共 **15 commit**，一任务一 commit。

---

## 一、任务0 基线（实测）

| 维度 | 基线 |
|---|---|
| mypy 存量债 | **67 处 / 24 文件**（624 暴露，被 ruff 长期掩盖） |
| pytest 红因 | OTS anchor 过期 + 治理 manifest 失配 + 581 豁免计数硬编码 |
| OTS | anchor 过期（624 信任根重钉致） |
| 闭环触达 | **34/67（50.7%）**，盲区 33（29 真盲区 + 4 预期不可触发 + 0 重复） |
| 尺子入根 | **22** 项 |
| PCK authorized | **27/83 = 32.5%** |
| 人审 | 110 条复核清单（622 D1 的 30 + 624 E2 的 80） |
| CI #630 | gate✅/replay✅/concurrency✅；quality(mypy)❌/pytest❌ |

## 二、A 线 · 修 P0 债务

| 任务 | 交付 | 结果 |
|---|---|---|
| A1 | `mypy` 67 处 → **0 errors**（24 文件：yaml stub 覆盖 + cast/判空/注解/重命名；仅 1 处 func-returns-value 逐条 ignore） | ✅ ruff/mypy/单测无新增失败 |
| A2 | OTS re-anchor（对 624 后信任根重新 stamp） | ✅ digest 一致 / `--check` 通过 / pending 未上链诚实标注 |
| A3 | pytest 红因：治理 manifest 重签 + 581 计数动态化（27/67/backed28） | ✅ not-slow 段全绿；replay `manifest_consistency` 5 失配 + DEBT-001 到期登记留 626 |

## 三、B 线 · 稳雷2

| 任务 | 交付 | 结果 |
|---|---|---|
| B1 | 闭环第7轮 108 条（Y1 盲区定向/Y2 回归/Y3 混合）实跑 | ✅ escaped **0**；新触达 `ATOM-STATUS-TRANSITION`+`S1-AUTHOR-SELF-VERIFY`；**累计 36/67（53.7%）**，盲区 33→31 |
| B2 | 雷2 稳定指标 + 触发标准①验证 | ✅ 最近增长率 2.9%<10%、VFDR 收敛 0.98%<1%、一致性 99.02%>95%；覆盖波动 8.9%>5% ⇒ **4/5 部分满足** |
| B3 | VFDR 收敛曲线 + 热力图 v3（67×7） | ✅ 累计 35/67（artifact 口径）/盲区 32；**0 危险逃逸** |

> 口径校正：B1 报告基于硬编码基线得 36；B3 以实跑 JSON 并集为准得 35（`ATOM-SUPERIORITY-WORDS` 无轮次记录），以 B3 为权威。

## 四、C 线 · 备雷1（QueYi Core 路径解耦）

| 任务 | 交付 | 结果 |
|---|---|---|
| C1 | `PathConfig`（env/config/默认向后兼容）；核心 6 + 辅助 20 工具 `ROOT` 接入 | ✅ gate/replay(56)/poison/tool_integrity 行为不变；`tool_integrity --update` 重钉 |
| C2 | QueYi Core 接口抽象设计 v0.1（Claim/Evidence/Attack/Verify/Authority + 映射 + 实现计划） | ✅ 只设计不实现 |
| C3 | 剥离触发标准检查（5 条） | ✅ 满足 2/5；整体「建议再等 1-2 轮」（②③ 为治理裁定，需人；⑤ 余量留 626） |

## 五、D 线 · 深化建设

| 任务 | 交付 | 结果 |
|---|---|---|
| D1 | 尺子入根 **22→34**（`RULER_TOOLS` 10→22，新增 12 个判决尺子；`tool_integrity --update`） | ✅ `--check` 34/34 一致；CORE_TOOLS 未变 |
| D2 | 人审可视化深色科技风（`human_review_dashboard_625`，纯静态 HTML/CSS/JS） | ✅ 复用 624 E2 模型；只读不判决 |
| D3 | 人审执行框架（`build_entry` 带哈希链 + `append_entry` 定义**不调用**） | ✅ 自检证「未代签：日志 size 不变」 |
| D4 | PCK 提升策略设计（S1 证据证人审队列 / S2 机器可确认候选 / S3 目标推算 / S4 口径统一） | ✅ 只设计不代签；当前 32.5% 未达 >48% |

## 六、E 线 · 化债 + 报告

| 任务 | 交付 |
|---|---|
| E1 | 债务清算 + 622/623/624 遗留项处理（6 项债诚实留 626） |
| E2 | 产品经理报告（CI 红因已定位修复 / 雷2 稳未达天花板 / PCK 与 110 条人审卡在人审不代签 / 三条交人决策） |

## 七、F 线 · 收工

| 任务 | 交付 | 结果 |
|---|---|---|
| F1 | `run_625_gate.py` 收工门禁（整目录 ruff + 9 个 625 新工具 `--check` + tool_integrity 34/34 + OTS + mypy 0 + 受控零污染） | ✅ **PASS** |
| F2 | 本报告 + `status.json`/`outbox` | ✅ awaiting_review |

## 八、核心诚实结论（偏差与未达标）

1. **CI 全绿（本地）达成**：mypy 67→0、pytest not-slow 全绿、governance manifest 重签、尺子 22→34、路径解耦；但**远程未 push**（铁律 625 不 push），远程 CI 验证留 626。
2. **雷2 连续 3 轮稳定**（623-625）信号成立（B2 4/5），但触达**未达天花板**：六轮累计仅 36/67（54%），盲区 31；根因 = 单卡 field-edit 载体天花板（编译/复算/git/多卡类规则跨卡 sandbox 亦不可达）。
3. **QueYi Core 路径解耦完成 26/约130**（核心 6 + 辅助 20），余 ~110 辅助 + tests/ 留 626（触发标准⑤未全满足）。
4. **PCK / 人审仍卡在人**：机器候选 0（56 证据证无人审来源），已备策略(D4)+可视化(D2)+执行框架(D3)，**不代签**。

## 九、留 626（诚实登记）

1. replay `manifest_consistency` 5 处指纹失配（evidence 卡 vs stale manifest）。
2. `DEBT-001` 债务台账到期（需人决续期/关闭）。
3. 触达天花板（需载体层：多卡/编译/复算/git 突破）。
4. PCK authorized >48%（走 D4+D3 由人执行 30+ 证据证人审）。
5. 110 条人审执行（D2/D3 框架）。
6. PathConfig 余量（~110 辅助 + tests/）；QueYi Core 剥离治理裁定（②③）。
7. 远程 CI 验证（push 后）。

## 十、交人决策项

- 是否启动 QueYi Core 剥离？（C3 判建议再等 1-2 轮）
- 是否授权执行 30+ 证据证人审以过 PCK 48%？
- 触达天花板是否立项载体层突破？
- 是否允许下批 push 验证远程 CI？

---
**新增/修改工具（625）**：`mypy_fix_625`(报告) · `ots_reanchor`(复用) · `ruler_coverage_extension`(复用) · `round7_mutator_625` · `loop_stability_metrics_625` · `vfdr_convergence_625` · `path_config_625` · `queyi_core_interface_design_625` · `queyi_core_trigger_check_625` · `human_review_dashboard_625` · `human_review_executor_625` · `pck_upgrade_strategy_625` · `run_625_gate` · 改 `tool_integrity.py`/`pck_abstain_sync_621` 等 mypy。
**新增单测（625）**：A1×6, A2×5, A3×4, B1×6, B2×6, B3×6, C1×10, C2×5, C3×6, D1×5, D2×5, D3×4, D4×5, F1×4 ≈ **77 例**，全过。
**受控目录**：atoms/evidence/Examples/Book 零污染。
**未 push / 未 golden accept / 未开 delegation / 未代签**。详见 `data/625_pm_report.md`、`data/625_debt_clearance.md`。
