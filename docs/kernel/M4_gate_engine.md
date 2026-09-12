# G3.1 门禁引擎 M4（Gate Engine）

> 工具：`tools/gate_engine.py`（21 条规则注册在册）· 测试：`tests/test_gate_engine.py`（17 用例，含元门禁）
> 设计依据：**ADR-0004**（挂 `cppbible.py:cmd_check`，收敛双清单）· **ADR-0005**（快照底座留给 S4）

## 1. 统一 Rule 接口

| 字段 | 含义 | 取值 |
|---|---|---|
| `id` | 规则唯一标识（工单里出现的名字） | 如 `ATOM-VERIFIED-BOUND` |
| `title` | 一句话说明 | — |
| `kind` | 规则族 | `fact` / `pedagogy` / `literature` / `meta` |
| `quadrant` | 判定归属（四象限） | `programmatic` / `llm` / `hybrid` / `human` |
| `severity` | 违规处置 | `block` / `warn` / `advice` |
| `scope` | 作用对象 | `atom` / `evidence` / `repo` |
| `check` | `Callable[[], list[Finding]]`；`None` = 未自动化（进人工队列） | — |
| `basis` | **学习科学依据**（`pedagogy`/`literature` 必填，注册时强校验） | — |
| `fix_hint` | 可执行修复提示（工单里给出） | — |

注册中心 = 本文件 `_register_all()`：**ID 重复即抛错**、**教学规则缺 `basis` 即抛错**（这两条由测试锁死）。

## 2. 四象限分流

| 象限 | 语义 | 本引擎的处置 |
|---|---|---|
| `programmatic` | 机器可判、可复算 | 进 CI（`--check`，block 即红） |
| `llm` | 语义判定（如 superiority 是否真有洞见） | **本轮不接模型**（DRQ-5）；在 `--list` 登记，进人工队列 |
| `hybrid` | 机器初筛 + 人工裁定（如教学深度） | 初筛入工单，裁定留人 |
| `human` | 纯人工（Golden 人审） | 只登记，不自动判定 |

## 3. 三 severity 与红绿语义

- `block`：`--check` 退出码 1（CI 红）。
- `warn`：**记债**——打印但不红（如"证据服务的原子尚未锻造"，G4 后自动清零）。
- `advice`：教学/文学建议，**只建议不改文**（铁律）；永不阻断，由 `test_advice_rules_never_block` 锁死。

## 4. 事实门禁（`fact` / programmatic）

| 规则 | 拦什么 | 依据 |
|---|---|---|
| `ATOM-FM-REQUIRED` | 原子卡必填字段缺失（含 `sources[]` 空——多源精炼要求 ≥1 源） | G1_layout §3 |
| `ATOM-ID-FORMAT` | ID 格式 / 域不在 16 域 / 目录与域不一致 / `type` 不在 10 类 | M1 §2/§5 |
| `ATOM-VERIFIED-BOUND` | `status=verified` 但证据/一手/superiority 缺项 | G1_layout §3 硬约束（S2 落地） |
| `ATOM-NO-UNVERIFIED` | 新原子停留在 unverified/needs-verify | DRQ-4 红线 |
| `ATOM-REL-TARGET` | 关系目标不存在 | M1 §3（warn：目标未锻造时记债） |
| `ATOM-REL-DAG` | 学习路径 DAG 成环 | M1 §3（环路=内容切分有问题） |
| `ATOM-SUPERIORITY-WORDS` | superiority 命中禁词表 | M3 §4 |
| `ATOM-GRAY-ZONE` | UB 域原子未标 `gray_zone` 五类 | M2 §7 决策树 |
| `ATOM-MISCONCEPTION-LEVELS` | 误解未分层（非结构化/层非法）/ **deep 类反例 <2** | G1_layout §3（调研核心结论：surface 一次纠正即可，deep 须 ≥2 独立反例） |
| `MIS-LIBRARY` | 误解库自身：字段齐 / level 合法 / **deep 反例 ≥2**；缺出处 warn | misconceptions/README.md（G5 前置资产，条目写歪会污染全库，故与原子双向校验） |
| `ATOM-MISCONCEPTION-REF` | 原子引用的误解 ID 必须存在 | G1_layout §3（引用不存在的 ID = 引用了不存在的反例） |
| `ATOM-AUDIENCE` | 认知适切：值非法 block；**缺失 warn**（渐进标注）；beginner 缺类比段 warn | G5 指令 §2.2（未标注只影响路径排序，不损害断言可信度） |
| `ATOM-PREREQ-READABLE` | `prerequisites_readable` 声明与实算一致（relations 中 prerequisite 目标是否已锻造） | G1_layout §3（声明失真会让学习路径把原子排到前置之前） |
| `EV-FM-REQUIRED` | 证据卡必填字段缺失 / `kind` 越界 | M2 §1 |
| `EV-FALSIFICATION` | 缺证伪对照（恒真测试） | M2 §3 证伪导向 |
| `EV-MATRIX` | `matrix` 缺 compiler/std/opt | M2 §2 两档与选取规则 |
| `EV-SERVES-EXIST` | 服务的原子不存在 | warn（G4 前原子未锻造） |
| `DOC-ZERO-PLACEHOLDER` | atoms/ + evidence/ 出现 TODO/TBD/占位 | 新体系零占位（Book 存量债单列） |
| `META-MANIFEST` | pyproject 清单 ↔ cmd_check 执行器不一致 | ADR-0004 |

### 4.1 覆盖映射（G3.1 点名的门禁 → 现状，**诚实标注缺口**）

| G3.1 要求 | 覆盖者 | 状态 |
|---|---|---|
| 可编译 | `compile_gate.py`（既有，在 cmd_check） | ✅ 复用 |
| 运行一致 | `run_expected.py`（`//@`）+ `atom_evidence_replay` 的 `run_match` | ✅ |
| ASM–C 锚定 | `verify_asm_evidence.py`（既有，符号级五态） | ✅ 复用 |
| 一手实证 | `ATOM-VERIFIED-BOUND`（`first_hand`）+ `EV-FM-REQUIRED` | ✅ 新增 |
| 原创性 / superiority | `ATOM-SUPERIORITY-WORDS`（机器只查禁词）+ `LLM-SUPERIORITY-QUALITY`（人审） | ⚠️ **机器覆盖不完整**（真洞见判定靠红队/人） |
| 证据完备度 | `ATOM-VERIFIED-BOUND` + `EV-FM-REQUIRED` | ✅ |
| 版本矩阵 | `EV-MATRIX` | ✅ 新增 |
| 灰色地带标注 | `ATOM-GRAY-ZONE` | ✅ 新增 |
| 反例存在 | `EV-FALSIFICATION` | ✅ 新增 |
| 术语一致 | `terminology_normalize.py --check`（既有） | ✅ 复用 |
| 交叉引用有效 | `crossref_audit` / `xref_check` / `fix_book_links`（既有） | ✅ 复用 |
| 零占位 | `DOC-ZERO-PLACEHOLDER`（新体系） | ✅（Book 存量单列） |
| （自加）DAG 无环 / ID 规范 / 双清单 | `ATOM-REL-DAG` / `ATOM-ID-FORMAT` / `META-MANIFEST` | ✅ |

## 5. 教学 / 文学门禁（`advice`：只建议不改文）

| 规则 | 检查 | 学习科学依据（`basis`） |
|---|---|---|
| `PED-MOTIVATION` | `pedagogy.motivation` 非空 | Merrill 首要教学原理：以问题/需求激活先备经验 |
| `PED-MISCONCEPTION` | `pedagogy.misconception[]` 非空 | 认知冲突 / 反驳性文本（refutation text） |
| `PED-SOCRATIC` | `pedagogy.socratic[]` 非空 | 自我解释效应 |
| `PED-PREDICT-FIRST` | `pedagogy.predict_first` 非空 | 生成性学习 / 预测试效应 |

**尚未实现的教学文学项（点名缺口，勿当成已覆盖）**：认知负荷（新概念上限/分块）、具体性衰减、正反对照的机器判据、费曼 rubric（现为 `HYBRID-TEACHING-DEPTH` 人工）、适度难度、决策路径、文学性四项（叙事弧/节奏/记忆锚点/声音一致）。这些需要"可算的口径"才能落规则，属 M5 及后续写作波次。

## 6. 评分聚合（口径设计；实现落 M5）

- 原子得分 `S_atom = Σ(w_i · pass_i) / Σ w_i`，权重按 severity：`block=3, warn=1, advice=1`。
- 章得分 `S_chapter = Σ(S_atom · 该原子在章内的权重) / Σ 权重`（章=原子组装视图）。
- 全书 `S_book = Σ(S_chapter · 章权重) / Σ 权重`（章权重暂按"原子数"）。
- **阈值校准**：**先标 golden 再反推**——G4 三样板达标后取其得分作基线，阈值由基线回推，而不是先拍一个数（S4 黄金锁：改阈值须过历史 golden 回归）。

## 7. 元门禁（规则自身的误报 / 漏报回归）

- 每条规则在 `tests/test_gate_engine.py` 里**正例触发 + 反例不触发**成对出现。
- 误报回归实例：「待补」在本项目是**合法缺口留痕**（证据卡 `## 待补`、M2 `【待确认】`），曾被误判为占位符 → 已从正则移除，并由 `test_daibu_is_not_placeholder` 锁死。
- 漏报回归实例：`relations: [{type: prerequisite, target: X}]` 是 G1_layout 的标准写法，解析器曾读不出 dict（关系规则全瞎）→ 已修并锁死。

## 8. 双清单收敛（ADR-0004 落地）

- 引擎 `--manifest-check` 用 **AST** 解析 `cppbible.py:cmd_check` 的 quality 元组，与 `pyproject.toml:quality_gates` 逐条比对。
- 首跑即抓到**两条已漂移项**（`atom_coverage_map.py --check --check-doc`、`atom_evidence_replay.py --check` 执行器有而清单缺）→ 已补齐，现恒为 0 漂移（`test_manifest_has_no_drift_in_repo` 锁死）。
- 引擎自身也作为**单个 gate** 注入：`("Gate Engine", [PYTHON_EXE, "tools/gate_engine.py", "--check"])`；规则粒度在引擎内聚合，不产生"每条规则一个子进程"的开销。

## 9. 反例自检（什么情况算没做到）

- 规则只有名字、跑不出拦截效果 → 不合格（测试里必须正例触发）。
- `advice` 规则导致 CI 变红 → 违背"只建议不改文" → 不合格（已被测试锁死）。
- 教学规则没有 `basis`（学习科学依据）→ 注册即抛错 → 不合格。
- `--manifest-check` 报 0 漂移但实际两份清单不一致（如 AST 解析静默失败）→ 不合格（故解析失败返回 `warn` 而非静默通过）。
- 覆盖映射表里把"未实现"标成 ✅ → 不合格（§4.1/§5 已显式标注缺口）。
