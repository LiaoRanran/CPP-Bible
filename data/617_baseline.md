# 617 开工基线台账（任务0 · 只读，不跑任何 --check）

> 时间：2026-09-21 ｜ 铁律：不跑监工门禁；数字取自基线文件 + 历史记录，可复算。
> 说明：本基线采集于 617 开工时（HEAD `8cca534`）。自 616 收工（HEAD `cbd0fbd`）后，并行会话新增 1 个 commit（`8cca534` PM：37 号架构演进路线图 + 总索引更新）；617 的任务工具/文档尚未创建（已用 `ls tools/*617*` 核对，无冲突）。

## 1. 当前 HEAD 与提交计数（实测，git 命令直取）
| 指标 | 值 | 获取方式 | 备注 |
|---|---|---|---|
| HEAD commit | `8cca534a2eece83a0736a6bfc4e7cbab1b4e76d1` | `git log -1` | 2026-09-21 17:32:19 +0800 |
| HEAD message | PM：37号架构演进路线图（八条雷霆方向四层归类+617→625+落地路径+9决策点）+ 总索引更新 | — | 并行会话产出（617 架构规划文档） |
| 总 commit 数 | **1512** | `git rev-list --count HEAD` | README 写 1469、quickref 写 1446 ⇒ 数字漂移存在，见线 D |
| tools/*.py 数 | **215** | `Get-ChildItem tools -Filter *.py` | README 写 204、quickref 写 196 ⇒ 漂移 |
| tests/*.py 数 | **210** | `Get-ChildItem tests -Filter *.py` | README 写 183、quickref 写 175 ⇒ 漂移 |
| atoms/*.md 数 | **28** | `Get-ChildItem atoms -Filter *.md -Recurse` | 含 _arch 归档后口径 |
| evidence EV-*.md 数 | **56** | `Get-ChildItem evidence -Filter EV-*.md -Recurse` | 与基线一致 |

## 2. 六维度评分（取自 36 号 PM 报告，标注"616 后"）
- 来源：`References/00_导航/36_产品经理报告_20260921_616_*.md` + `data/project_health_report_20260920.md`（E2）。
- 616 后六维度综合评分 ≈ **8.4 / 10**（615 为 8.1）。
- 维度：① 验证正确性 ② 验证独立性 ③ 统计诚实性 ④ 人审可信度 ⑤ 攻击面覆盖 ⑥ 可复算/可审计性。616 主要拉动③（CS 修偷看）与②（他验原型）；④（人审 388=全 batch_authorization，194 mirror）仍为最大短板。

## 3. 核心验证数字快照（取自 `data/616_baseline.md` 与 standing baseline，非重跑）
### 3.1 gate
- 规则数 **63**；命中 **191**（block=**0** / warn=**186** / advice=**5**）。来源：`golden_state.json`（`_arch_v20` 复算，与 613–616 一致）。

### 3.2 poison
- 124/124 通过；表观覆盖率 100%（63/63）；诚实覆盖率 95.2%（60/63，`machine-untriggerable` 3 条不计）。
- 注：617 任务书 D2 模板写 `"rule_coverage": "39/63"`，与历史口径（63/63 表观）不一致，本基线以历史记录为准，39/63 未在本地复算到，列为待核。

### 3.3 replay
- confirm=**56** / refute=**0** / infra_error=**0**。来源：`atom_evidence_replay` standing baseline（613 起冻结）。

### 3.4 mutation（v7 冻结基线）
- variants **1593** / blocked **1405** / escaped **1** / n_a **179** / equivalent **8** / 可判分母 **1406** / 逃逸率契约 **1/1406**。
- 逃逸点：唯 M1 = `EV-CONC-001`（W2 冻结 TCE），登记 `data/mutation/known_tce.jsonl`(TCE-614-001)。来源：`data/mutation/full_baseline_v7.json`（591 冻结）。

### 3.5 置信序列 / 固定样本 CP（616 A 线，本批 A 线深化 estimand）
- 逃逸经验率 **1/1406 = 0.0711%**（L1 描述性）。
- 固定终点 Clopper-Pearson 单侧 95% 上界 **0.3370%**（CP，L2 fixed-endpoint）。
- confidence sequence（e-process + Ville）anytime 有效 95% 上界 **0.9062%**（CS，L2 anytime，= CP 的 2.69×）。
- 偷看虚报（探针，真实 p=0.01 每 20 样本偷看）：固定样本 CP **13.80%** vs e-process **0.00%**。
- 来源：`data/confidence_sequence_recalc_616.md` + `tools/confidence_sequence.py`。

### 3.6 人审（615 诚实化，本批 E 线可执行化）
- 388/388：approve **354** / modify **34** / reject **0**。
- review_method = batch_authorization **388**（全部）；mirror edge **194**；逐条独立语义审查 **0**。
- W2 判决：IN **114** / OUT **7** / UNDEC **0**（OUT7 = 7 个 MIS 对应攻击边）。
- 来源：`data/human_review_honesty_labels.jsonl` + `tools/human_review_honesty_615.py`。

### 3.7 他验 / 信任根（616 D 线，本批 B 线深化独立性分级）
- 验证者数量 **1**（项目自身 `gate_engine.py`），无独立第三方。
- 独立第二实现 **1** 条规则（`ev_matrix_unbacked_v2.py` / 63 条）。
- checksum 保护 **22** 项（`tool_integrity`：core5+test_config2+supply_chain5+ruler10）。
- 信任根判定 = partially_anchored（OTS pending 未真上链；in-toto `hmac` 非标准签名）。
- 第一原则单用户上限：生成者=判断者=同一主体 ⇒ 独立票结构性缺失。

## 4. 交人项状态（取自 `data/human_decision_tracking_616.md`）
### 615 遗留（7 项）
| # | 描述 | 优先级 | 状态 |
|---|---|---|---|
| 1 | 30 条逐条复核是否执行 | P0 | 待决策（清单就绪） |
| 2 | EV-MATRIX 规则定义补全是否合并进 evidence/ | P1 | 部分推进（616 B1 已出独立文档，是否合并待决） |
| 3 | warn 不增锁机制是否启用 | P1 | 待决策 |
| 4 | 27 条 legacy 豁免到期处置 | P1 | 待决策（默认继续豁免） |
| 5 | 工具合并 3 族是否执行 | P2 | 待决策 |
| 6 | data 目录整理方案是否执行 | P2 | 待决策 |
| 7 | CI 四 job 实跑确认 | P0 | 待决策（本机无 gh 通道） |

### 616 新增（3 项）
| # | 描述 | 优先级 | 状态 |
|---|---|---|---|
| 8 | 置信序列是否正式启用（cs_* 取代 cp_* 对外） | P0 | 待决策 |
| 9 | 他验架构是否进入实施 | P1 | 待决策 |
| 10 | 保形预测/弃权三态是否做（留 617+） | P2 | 待决策 |

## 5. 已知债务快照（610 后，可能已过期，待 F3 复核）
- 学习者镜像门未开（gate 仍 block=0，学习者门 closed）。
- M1 TCE（`EV-CONC-001`）未根治，靠 W2 冻结规避。
- oracle 验证未做（非确定毒丸未真 oracle 校验）。
- 活性锚落卡（部分 atom 活性锚未落地）。
- modify 口径未定（34 modify 是否真改证据）。
- OTS 真上链未做（信任根仅 partially_anchored）。
- in-toto 真签名未做（现 `hmac` 非标准）。
- 数字漂移（README/quickref 计数与 `git rev-list` 实值不一致，线 D 专项治理）。
