# 元系统 · 债务与决策总账（Single Source of Truth）

> 生成：2026-09-16（监工并行化债产出）｜数据源：近 30 轮 worklog + 现场 git status + 门禁实测
> 用途：把散落各 worklog / 对话里的"待裁决、待建设、资产风险"集中成一份，避免再靠记忆。
> 维护规则：每批收工由监工更新；**标【557 正在做】的项不要再重复派**；决策类执行权永远在人。
> 口径：本账只管**元系统层**（tools/门禁/对抗/调度/验证/L2-L4）。Book 内容层债见 `docs/references/content_debt_tasklist.md`（已基本清零）与 `docs/S6_tool_debt.md`（可能过时，以实测为准）。

---

## §0 资产风险（最紧急，优先级 P0 风险）
| 项 | 现状 | 建议 |
|---|---|---|
| **530–557 核心架构文档全部 untracked** | `References/architecture_架构演进/` 下 530–557 共 28 份（六轮对抗报告、蓝图、所有投喂词、调研 549–555）从未 `git add`，只在工作区。误删/环境重置即全丢——这是元系统的命根子 | 等 557 收工、确认工作树干净后，**一次性把这批文档纳入版本控制**（人审是否连同 worklog 一起；worklog 历史惯例不入库，可单独决定）。监工不擅自 commit。 |
| worklog 25+ 份（403…556） | 按惯例不入库，散在根目录 | 同上，决定是否归档到 `docs/worklog_archive/` 后入库，或维持不入库仅本地留存。 |
| `_adv_*/_arch_*` 沙箱/对抗产物 | 按惯例保留未跟踪（可复跑探针） | 维持现状；其中 `_adv_v95b/` 是第五轮对抗正本，建议至少纳入版本控制留证。 |
| `_probe_ch132_blk*` 等临时件 | 非任何本批产物，一直保留 | 人确认无历史价值后清理；不擅自删。 |
| 本地 ahead ≈246 commit 未 push | SSH `git@github.com:LiaoRanran/CPP-Bible.git` 报 exit 141（数据通道被远端关） | 人切手机热点手动 push；agent 不自推、不 --no-verify。 |

## §1 待用户拍板的决策债（每条都卡着某件事）
| # | 决策项 | 现状 | 选项与建议 | 阻塞谁 |
|---|---|---|---|---|
| D1 | golden_lock warn 59→136 分类签署 | 基线停在 67c1962(warn59)，落后于 548/553 新增规则(现136)；slow 套件唯一红的就是它 | 557 Part A 正产"分桶+排序+建议 accept 命令"。人看桶③约15条后 `golden_lock check --accept "<实测理由>"`。监工不代签 | slow 测试恒红、CI 干净信号 |
| D2 | 攻击面分类学 A/B | 代码 A1–A10 与 409 原表同名异义（仅 A8/A9 一致）；中立对照已写 `docs/kernel/attack_surface_taxonomy.md` | 方案 A=改代码对齐 409（~1h）；方案 B=改文档标注 409 已被取代。**建议 B**（409 是历史快照，代码是活引用） | 后续攻击面工作的口径 |
| D3 | doc_lint 是否接 CI | 存量 19 处文档失真，严格模式会恒红；工具已有 --observe | 先 --observe 跑一段时间攒清单，再决定升格；不直接上严格 | 文档漂移无人管 |
| D4 | CI ruff 存量债 ≈4 项 | 530 §6.8 遗留，会动几个未改文件 | 独立小批，逐个判语义后清；不急 | CI ruff job 干净 |
| D5 | 跨键 parser divergence | 前导零/YAML1.1 陷阱词已 xfail 登记 | 557 Part B2 正在实测定性：真放行分歧则补硬化，不构成则转确定性测试 | parser 层灰色态 |
| D6 | EV-MATRIX-UNBACKED 桶② | 16 条里混着 gate:1000-1002 刻意"排除 actual"的设计 | 557 Part A2 正逐条甄别"设计内 vs 真缺支撑" | warn 信噪比 |
| D7 | 概念名归一范围 | "栅栏"vs"内存屏障(fence)"、子类 vs 别名未一刀切 | 528 已刻意不收编译器屏障/硬件屏障（子类）与裸"锁"；维持"只借词汇、不自动合并"，冻结条件见 §4 | 概念图连通 |

## §2 排队技术债（建设 backlog，按层）
| 层 | 项 | 状态 | 说明 / 触发 |
|---|---|---|---|
| L1 | V-iso N1–N7 毒样例 | 【557 正在做 Part B1】判决已在，只补载荷 | — |
| L1 | M3 区间降级收口 + M2 诚实化 | 【557 正在做 Part C】带 541 安全形状，零误伤不达标即回退 | — |
| L1 | B1/B6 异族对抗 | 未打 | 真编译 -O0/-O2/-Os 测 nc1 阴面诚实性；交异族，不占苦力 |
| L1 | 545 L2 异族 A1/A2/A4/A6 | 未打 | 只闭合了 A3/A5/A7；L2 调度层还需一轮异族渗透 |
| L1 | impact_analysis 多跳闭包 | 【557 正在做 Part D】纯 Python 传递闭包+环检测，勿用 CTE | — |
| L4 | 人审经济学（review-order） | 【557 正在做 Part A】 | 本批后人审瓶颈应大幅缓解 |
| L4 | V5 命题回填 backlog | 未做 | 26 张待回填 + 3 张红队卡需人签/登记独立基准；等 557 分桶后按队列填 |
| L4 | 概念真连通（批次 V） | 未做 | 共指/实体归一/orphan 不丢弃；**只产候选清单，不 embedding 不自动连边** |
| L4 | model canary（批次 W） | 未做 | 冻结 20–30 任务 + 结构断言（不比字符串），主/备模型同跑；换模型时用 |
| L4 | CPVA 全阶段 | 未做 | 现仅 fixture 阶段；红队/人审/修订成本零观测——补全才有"每颗原子真实成本" |
| 性能 | golden_lock 自身并行化 | 未做 | slow 125s 硬下限；涉 replay 全局锁，单开一批，勿塞进普通批次 |
| 环境 | pytest tmp 卡 safe-delete 守卫 | 已定位 | pytest 默认 tmp 在系统 `%TEMP%\pytest-of-ASUS`（writable root 外），收尾 `rmtree` 累计 >500 文件即被 safe-delete 批量确认拦下，表现为"每次跑完卡很久"+首跑假红 rc=1（复跑即绿）。根治：pyproject `addopts` 加 `--basetemp=.pytest_tmp --tmp-path-retention=failed`（tmp 挪进项目 root 内删除不拦 + 只留失败 run 不堆 garbage），`.pytest_tmp/` 入 .gitignore。改核心配置需全量回归，勿在批次进行中改。治标：手动清一次 `%TEMP%\pytest-of-ASUS`（需提权，下次仍攒）。 |

## §3 战略层冻结项（等模型变强，勿提前动工）
触发条件才解禁，提前做=白做：
- **L3 智能 / LLM 进闸**：门 = EIR 95% 置信上界 ≤5% + 异族判决 + 可回滚（非"模型够强"）。当前观测：L3=12%。
- **G-supervisor（系统自起 worker）**：默认 OFF；接管决策永远归人。
- **概念自动合并 / LLM-as-judge 终审 / 同质辩论 / 在线改权重 / 自动 KG 入库**：明令禁止。
- **知识层数学引擎**（Dung/ASPIC+/SHACL/TMS）：551 降级为只借词汇；解冻条件=原子>100 且出现真实跨原子矛盾。
- **Kùzu / tree-sitter / DuckDB / Pydantic / mutmut**：552 结论——现用 Hypothesis/syrupy/scipy/纯 Python 闭包足够；规模到了再换，不提前造轮子。

## §4 当前基线（2026-09-16 实测口径，供对账）
- gate：规则 61 · 命中 141（block=0 warn=136 advice=5）
- poison：96/96，RULE-COVERAGE 36/61 + 27 豁免，零覆盖攻击面无
- replay：confirm=56 / refute=0 / infra_error=0（全量 ~165s，增量 0.3s）
- pytest：fast 全绿（~280–290 点）；slow 仅 pre-existing golden_lock_json
- kg：325 节点 / 291 边；概念 157 节点中跨原子连通 0/157（标签袋，待批次 V）
- mutation：83 卡 × 7 算子 = 1188 变体，严格拦截率 ~64.33%（M2 收口后）
- 五层完成度（历史口径）：L0 强 / L1 强 / L2≈12%（骨架已成）/ L3≈12% / L4≈40%（本批人审解锁上抬中）

## §5 更新纪律
- 每批收工：监工核对 §4 基线数字是否漂移、§2 项是否移入"已完成"、§1 是否有人拍板。
- 数字一律实跑，不从旧账抄；旧账与磁盘冲突以磁盘为准并标注。
- 决策类（§1）不替人执行；建设类（§2）一任务一 commit + 毒样例 + pytest。
