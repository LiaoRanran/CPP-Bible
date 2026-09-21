# 614 收工验收报告

> 批次：614 · CI全绿收尾 + 学习者镜像真实验证 + 信任根评估 + M1 攻坚启动 + oracle 优先级
> 生成：2026-09-21 ｜ 苦力（CodeBuddy）｜ HEAD 见文末
> **铁律**：一任务一 commit；不跑监工门禁（tool_integrity --check / gate --check / poison / replay --check）；
> 不改受控目录；不 push；不 golden accept；不写 615。

---

## 一、任务清单与 commit

| # | 任务 | commit | 一句话 |
|---|---|---|---|
| 0 | 先量基线台账 | `a4d76f1` | 基线（git/文件计数/信任根现状/MISSING 学习者态） |
| A1 | CI gate 根因修复 | `512d991` | **根因=gate/quality job 缺 pyyaml**；ci.yml 补装 |
| A2 | governance 台账更新 | `9fc6a33` | manifest/scan 更新 + tool_integrity 重钉 |
| A3 | CI 全绿里程碑记录 | `4c9bbae` | 根因链（replay infra_error + 缺 pyyaml）+ 待 CI 确认 |
| B1 | 学习行为采集 + BKT | `191fd35` | `learner_behavior_logger`（行为日志+BKT+推荐） |
| B2 | 镜像仪表盘真实数据版 | `05b161b` | `learner_twin_dashboard_614`（读行为日志→HTML） |
| B3 | OOD + 跃迁判定 | `dc1e019` | `learner_ood_evaluator`（≥0.8+OOD≥80%⇒jump） |
| B4 | 学习者-论证层联动 | `582a51e` | `learner_argument_link`（KC→论证链→复盘推荐） |
| C1 | OTS 真实上链评估 | `29c5a3b` | 结论：pending；可行但受交人/授权/出块制约 |
| C2 | in-toto 真签名评估 | `7f50604` | 结论：HMAC 非标准；真签名需密钥托管（交人） |
| C3 | 信任根诚实标注 | `f25d42d` | `trust_root_status_check` ⇒ **partially_anchored** |
| D1 | M1 逃逸根因 | `b986b6a` | M1=删 negative_controls；字段存在性无人负责 |
| D2 | M1 结构性登记 | `af8e34f` | `data/mutation/known_tce.jsonl`（TCE-614-001）+ gate 注释豁免 |
| — | D2 路径修正 | `fa92ed6` | known_tce 对齐任务书路径（data/mutation/） |
| D3 | 逃逸率诚实化 | `c27be02` | 契约仍 1/1406；活雷 0/1405（单侧上界 0.213%） |
| E1 | oracle 优先级 | `30b4611` | `oracle_priority_614`（Top1=EV-CONC-001） |
| E2 | oracle 验证流程 | `2d7f1be` | `oracle_verification_614`（fail-closed，≥2 独立确认） |
| F1 | 收工门禁脚本 | `c4fa61d` | `run_614_gate.py`（跑 614 工具 + 卫生 + 回归） |
| G1 | _arch 归档 | `aa9a3a4` | v10-v17 → `_archive/old_research/`（136 文件） |
| G2 | worklog/临时清理 | `cafcc7e` | 上游已归档；无可安全删除项 |
| G3 | 重复工具评估 | `c194a80` | 判"有意版本化，不合并"（仅标注） |
| G4 | 导航/健康报告更新 | `63e05b4` | 健康报告 + 速查 v6 + PM 报告 34 + 索引/债务 |
| G5 | data/ 派生物整理 | `f559e72` | 引用密集 ⇒ 仅分类不移动（交人） |

> 共 **23** 个 commit（含任务0 与 D2 路径修正）。

---

## 二、实测数字

### 2.1 收工门禁（`run_614_gate.py` full）
| 项 | 结果 |
|---|---|
| 614 工具 `--check` | **7/7 exit 0** ✅ |
| ruff（tools/ tests/） | exit 0 ✅ |
| mypy（tools/） | exit 0（204 source files）✅ |
| **pytest_full**（`-m "not slow"`） | **exit 0**（275.3s）✅ ← G1 修复既有 601 漂移后**全量转绿** |
| pytest_614 | exit 0 ✅ |
| 受控目录零污染 | ✅ 干净 |
| **门禁结论** | **PASS** |

### 2.2 监工门禁（standing baseline · 苦力**未重跑**）
gate 63 规则/191 命中（block0/warn186/advice5）· poison 124/124（表观100%/诚实95.2%）· replay confirm=56/refute0/infra0 · tool_integrity 5核心+2配置+supply_chain5。

### 2.3 变异/mutation（v7 冻结）
变体 1593 · blocked 1405 · **escaped 1**（M1·EV-CONC-001）· 可判 1406 · 契约 **1/1406** · **known_tce 1** · 活雷 **0/1405**（单侧上界 0.213%）。

### 2.4 学习者镜像（真实闭环）
模拟 10 KC×5 轮（30%→80%）⇒ ≥5 KC 掌握度 ≥0.5；仪表盘平均 0.27、8/27≥0.5；推荐 3 KC；论证复盘推荐 8 KC（已掌握但论证未理解透）。**真实练习数仍 0**。

### 2.5 信任根
Merkle 摘要 `47c330c9…6e0db5`（与 .ots 一致，`ots verify` exit 0）· OTS **pending** · in-toto **hmac 非标准** · 总判定 **partially_anchored**。

### 2.6 oracle
83 卡待验 · **已验 0** · 优先级 Top1 `EV-CONC-001`（18 分）· 流程 fail-closed 就绪。

### 2.7 仓库
commits **1473** · tools **204** · tests **182** · 根 `_arch` **2**（v18,v19）· data **447**。

---

## 三、偏差表（任务书假设 vs 实测）

| # | 任务书 | 实测/处置 | 处理 |
|---|---|---|---|
| 1 | 任务0 步骤3-6 要求跑监工门禁 4 类 | §五 禁止苦力跑 | **未跑**，数字取 standing baseline |
| 2 | A1 假设根因在 poison/replay | 实测根因 = **gate/quality job 缺 pyyaml** | 按实测修复 ci.yml（非 poison） |
| 3 | A2 背景"45 处（_arch_v2/v3/v4/v5 删除）" | A2 时仅 2 处；真正漂移是 **`_arch_v19` 新增**（并行会话） | G1 归档 + governance 重钉修复 |
| 4 | A2 步骤6 要 `tool_integrity --check` | §五 禁止 | 只做 `--update` 重钉 |
| 5 | B2 "读 learner_state.jsonl" | 该文件不存在；真实源 = `learner_behaviors.jsonl` + BKT 递推 | 读真实行为日志（更诚实） |
| 6 | B4 提"learner_recommender.py" | 步骤3指定 `learner_argument_link.py` | 按步骤3命名 |
| 7 | D1 猜"编译器优化 TCE" | 实测 M1 = **删 negative_controls**；根因=字段存在性无人负责 + 冻结 TCE（W2） | 按实测定性（非编译器优化） |
| 8 | D2 要"gate_engine 加规则：已知TCE不算逃逸" | 加规则会改 gate 行为/破冻结基线 | 改为**注释豁免标注**（不改行为） |
| 9 | D2/F2 要"metrics_collector 加 known_tce_count" | 其测试硬锁 `len(ALL_METRICS)==27` | 不改 schema；用 `known_tce.jsonl` 内嵌 metrics + `known_tce_metrics_614.md` |
| 10 | E1 要"data/oracle_verification_priority_614.md" | 融合实现为 `data/oracle_priority_614.md`（全清单+Top20 理由） | 命名就近 |
| 11 | G3 要"合并重复工具" | 经查无安全可合真重复（皆有意版本化/叠加） | 仅标注（按安全条款） |
| 12 | G5 要"移动 data 派生物" | v4/v5 被 test/metrics 引用、*_report_* 被工具引用；v4 为 CRLF 假脏 | **不移动**，仅分类（安全条款） |
| 13 | F1 要"测试2例" | 实现 4 例 | 超出但兼容 |

---

## 四、交人项（需人审裁决）
1. **CI 四 job 实跑全绿确认**（`512d991` 后；本机无 gh 通道）。
2. **OTS 是否真实上链**（不可逆，需联网+授权；Runbook 见 C1）。
3. **in-toto 是否真签名**（需密钥托管；Runbook 见 C2）。
4. **行为采集两版合并方向**（613 `learner_behavior_ingest` vs 614 `learner_behavior_logger`）。
5. **活性锚补丁集是否落卡**（50→41，人审权）。
6. **modify 口径**（keep-low IN114/OUT7 vs upgrade-medium IN121/OUT0）。
7. **data/ 目录整理方案**（G5 建议的前置重构步骤）。

## 五、未做项（明确声明）
- 未跑监工门禁四类（§五）；未执行真实 oracle 验证（人审权）；未 OTS 真上链；未 in-toto 真签名；
- 未落活性锚补丁（需授权）；未重跑全量 mutation 重冻结（D2 未改 mutation 代码）；未 push；未 golden accept；
- 未写 615 提示词；未动受控目录。

## 六、边界自证
- `git diff --quiet -- atoms/ evidence/ Examples/ Book/` ⇒ **干净**（exit 0）。
- 遗留（非 614 引入）：两条 CRLF 假脏（`_adv_v80/probes/p57.cpp`、`data/metrics_612.md` 时间戳）；
  `_arch_v19/` 与 `_arch_v19_brief.md` 为并行会话未跟踪目录（未提交）。

---

*HEAD：见 `git log --oneline -1`。报告由 614 批次生成；所有门禁数字可复算（standing baseline 除外）。*
