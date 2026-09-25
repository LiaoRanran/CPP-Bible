# 619 开工基线台账（任务0，只读实测）

> 批次：619（八条雷霆正式开工：雷2 攻击者目标函数 + 雷4 PCK 结构 + D1 manifest 收敛）
> 生成时间：2026-09-21 · 解释器：`.venv\Scripts\python.exe`
> 口径：本文所有数字均为**开工时实测**；冻结门禁数字取 `data/SNAPSHOT_MANIFEST_617.json`，**不跑监工门禁**（619 §六 硬边界 2）。

## 一、仓库状态

| 项 | 实测值 | 取证 |
|---|---|---|
| HEAD commit | `e050b00`（619 补完 …） | `git log --oneline -1` |
| 617+618 commit 范围 | `cbd0fbd..HEAD` = **30** commit | `git log --oneline cbd0fbd..HEAD \| Measure-Object -Line` |
| 其中（逐条相核） | 并行会话前置 **3**（`8cca534` 37号路线图 / `0b9683f` _arch_v21 / `6ef8551` 项目健康报告）+ 617 段 **11**（`edc264b~6549a8c`）+ 618 段 **16**（`d077730~e050b00`）= **30** ✓ | `git log --oneline --reverse cbd0fbd..HEAD` |
| 本地领先 origin/master | **30** commit（**不 push**，619 §六 硬边界 6） | `git rev-list --count origin/master..HEAD` |

### 工作树状态（`git status --short`）

```
 M _adv_v80/probes/p57.cpp      ← 仅 CRLF 假脏（长期残留，非本批）
 M data/metrics_612.md          ← 仅重生成时间戳（长期残留，非本批）
?? _arch_v19/                   ← 并行会话评审存档（未跟踪）
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
```

> 处置：以上 6 项**均非 619 产生**，本批不提交、不删除、不清理（避免误伤并行会话产出）。

### SNAPSHOT_MANIFEST_617.json（唯一权威计数源）

| 字段 | 值 |
|---|---|
| `generated_at` | 2026-09-21T10:46:08Z |
| `head_commit`（生成时） | `66328df`（**已落后于当前 HEAD `e050b00`** ⇒ 619 C1 收敛时须重生成） |
| `live_counts.commits` | **1517** |
| `live_counts.tools_py` | **218** |
| `live_counts.tests_py` | **213** |
| `live_counts.atoms_md` | **28**（含 README.md；实际卡 27 张） |
| `live_counts.evidence_ev_md` | **56** |

冻结门禁基线（`verification_baseline_frozen`，619 §八 逐字一致）：

| 门禁 | 数字 |
|---|---|
| gate_engine | 63 规则 / 191 命中（block=**0** / warn=**186** / advice=**5**） |
| poison_drill | 124/124（表观覆盖 63/63，诚实 60/63） |
| atom_evidence_replay | confirm=**56** / refute=0 / infra_error=0 |
| mutation v7 | variants 1593 · blocked 1405 · escaped **1** · n_a 179 · equivalent 8 · 可判分母 **1406** · 契约 `1/1406` |
| 置信 | CP 固定终点 0.00337 · CS anytime 0.009062 |
| 人审 | 388（approve 354 / modify 34 / reject 0，batch_authorization 388、镜像边 194） |
| 独立性 | verifier_count 1 · second_implementation 1/63 · discrete_level **L1** · continuity_scalar **0.153** |
| 信任根 | `partially_anchored` |

## 二、mutation 算子清单（M1–M7，只读抄录 `tools/mutation_fuzz.py`）

| 算子 | 语义（源码逐字） | 攻击对象 |
|---|---|---|
| **M1** | 字段删除（`artifact_sha256` / `run_match_file` / `negative_controls` / `signed_by`） | 卡必填键的存在性 |
| **M2** | 路径变形（大小写翻转 / 加 `./` / 正反斜杠互换） | 路径归一化 |
| **M3** | 断言弱化（`contains_in`→`contains` / 去 `-Werror` / 量化→存在性） | 断言强度（区间→全文） |
| **M4** | 恒真注入（`main` / `ret` / `.p2align` / `.file` 这类通用或 ABI 帧符号） | 断言的判别力（真空通过） |
| **M5** | claim 自标（`inference`→`observation`） | claim_type 分类 |
| **M6** | YAML 变形（重复键 / 缩进提升 / 全角键名 / flow 写法 / matrix 值层删键） | frontmatter 解析 |
| **M7** | 数值/哈希篡改（计数 ±1 / sha256 改一位） | 哈希与读数绑定 |

判决三分类：`blocked` / `escaped` / `n_a`（n_a 与 malformed **永不进分母**）；`equivalent` 单列（等价变异体，剔除出逃逸与分母）。

### v7 实测分布（`data/mutation/full_baseline_v7.json`，`frozen_at_commit=d36d5c8`）

| 项 | 值 |
|---|---|
| `results` 条数 | **1593** |
| `verdict` 原始计数 | blocked 1405 · n_a 179 · **escaped 9** |
| 其中 escaped 真逃逸 | **1**（`evidence/conc/EV-CONC-001.md` · M1 · 删 `negative_controls`，TCE-614-001 冻结） |
| 其中 escaped 等价体 | **8**（全部是 M6「块式 → flow 写法（matrix）」：EV-HIST-001、EV-MEM-032~037、EV-UB-002） |
| 可判分母 | **1406** = 1593 − 179(n_a) − 8(equivalent) |
| 按算子变体数 | M6 724 · M4 251 · M2 195 · M7 139 · M3 107 · M1 92 · M5 85 |
| 覆盖卡数 | 83 |
| `results[]` 字段 | `card / op / point / verdict / kind / new_block / new_warn / replay_skipped / reproduce / equivalent` |
| `rate_flags` | M5 可判样本仅 29 < 59 ⇒ 样本不足（要宣称 ≤5%@95% 需补样至 n≥59） |
| TCE 登记 | `data/mutation/known_tce.jsonl` 共 1 条（`TCE-614-001`，status `known-structural`） |

> **A2/A3 用得到的结构事实**：`results[]` **不含"分数"字段**（无目标函数、无难度、无攻击强度）⇒ A2 的目标函数分数必须**从上述字段纯计算**得出，不得编造；`new_block` / `new_warn` 是唯一可用的"证据锚点"信息。

## 三、攻击面分类现状（617 C1 + 618 C2/C4）

| 项 | 现状 |
|---|---|
| 分类文档 | `data/test_taxonomy_617.md`（10 类：gate / evidence / poison / replay / mutation / independent_verification / statistics / tooling_integrity / snapshot / script_self_test） |
| 真实验证测试 vs 脚本自测 | 前 8 类为真实验证；snapshot / script_self_test 为元测试；**覆盖率口径剔除 script_self_test** |
| 机器可读映射 | `tests/test_category_map.py` + `tests/test_category_map.json`（618 C4） |
| 分类计数脚本 | `tools/test_classifier_618.py`（618 C2） |
| 计数口径 | 总 `tests/*.py` = **213**（manifest 实测；README 写 183 ⇒ 已判漂移，治理留 C1/C2） |

> **与雷2 的关系**：现有分类是**测试侧**的（"每个测试证明什么"），**不是攻击侧**的。619 A1 的 4 个子目标需要**新建**攻击面→子目标的映射，不能直接复用 C1 的 10 类（那是测试归类，不是攻击面）。

## 四、PCK 雏形现状（atoms/ + evidence/ 的 markdown 结构）

### 4.1 原子卡 `atoms/<domain>/ATOM-*.md`

27 张卡（`live_counts.atoms_md` 28 含 README.md）。frontmatter 实测字段（`atoms/conc/ATOM-CONC-FENCE-001.md`）：

```yaml
id / title / domain / type / status / verified_by / verified_at / dal /
human_review / status_history[] / audience / cognitive_load / prerequisites_readable /
claim / claim_structured[] / claim_boundary / ...
```

其中 `claim_structured[]` 已经是"命题级"结构：`{id, subject, predicate, object, claim_type, statement, evidence[], external_basis, extracted_by}`，`claim_type ∈ {observation, inference}`。

### 4.2 证据卡 `evidence/<domain>/EV-*.md`

56 张卡。frontmatter 实测字段（`evidence/conc/EV-CONC-001.md`）：

```yaml
id / serves[] / kind / hypothesis / controlled_vars / matrix{compiler,stdlib,std,opt,arch} /
fixture / command / artifact / artifact_version / artifact_sha256 / artifact_compiler /
artifact_assert[] ({kind: contains_in|absent_in, symbol, text}) / negative_controls[] ({id,variant,mutation,fixture,anchor,remove,retain,probe{channel,symbol,text,op},note}) /
actual{run_match_file,run_match_keys} / expected{run,asm} / verdict / falsification /
depth_layer / drill_note
```

### 4.3 PCK 雏形 → certificate 的缺口（B1 的输入）

| certificate 建议字段（37 号路线图 雷4） | 现有 markdown 是否有 | 缺口 |
|---|---|---|
| `claim.id / statement / domain / type` | ✅ `id / claim / domain / type` | 字段名需映射（`type` 语义不同：卡侧是 mechanism，证书侧是 inference/observation） |
| `evidence[].type/ref/hash` | ⚠️ 部分：`serves[]` 是反向边；`artifact_sha256` 只覆盖 1 个主工件 | **无 evidence 数组**、无 url/standard 引用结构的哈希 |
| `negative_tests[].mutation_id/result` | ✅ `negative_controls[]`（机制级） + `data/mutation/full_baseline_v7.json`（M1–M7 级） | `mutation_id` 在 v7 里是 `(card, op, point)` 三元组，**无稳定 id** |
| `verifiers[].name/result` | ⚠️ 只有"单一验证器"（gate + replay），`second_implementation 1/63` | **无 verifiers 数组**；独立性 L1 |
| `human_authority.status/review_method` | ⚠️ `verified_by / human_review / status_history[]` | 无 `review_method`（615 已证 388 条全是 `batch_authorization`，逐条独立 0） |
| `uncertainty.cs_upper_bound/estimand` | ❌ 卡内**无** | 只有全局 CS 0.9062%（617 A1 estimand 三层已定义） |
| `provenance.commit/first_authorized_at` | ⚠️ `verified_at` 有；**commit 无** | 需从 git 反查 |
| `expiry` | ❌ 无 | — |

> 结论：**没有任何一张现有卡能"逐字映射"成完整 certificate** ⇒ B3 试点必然要**显式登记缺失字段**（这正是试点报告的价值），而不是把缺失当 0 或编造。

## 五、本批硬边界复述（619 §六）

1. 不改受控目录：`atoms/ evidence/ Examples/ Book/` + CORE_TOOLS（`gate_engine.py` / `atom_evidence_replay.py` / `poison_drill.py` / `toolchain.py` / `cppbible.py`）+ `golden_lock.py` + `mutation_fuzz.py`
2. 不跑监工门禁（`tool_integrity --check` / `gate --check` / `poison` / `replay --check`）
3. 不生成新 mutation（A2 只读分析现有 1593 variants / 1406 可判）
4. 不实际运行攻击-验证迭代（A4 只写协议）
5. 不修改原始 markdown 卡（B3 只生成新 certificate）
6. 不 push；7. 不 golden accept；8. 不打开 delegation
9. 不做雷1/雷3完整版/雷5/雷6/雷7/雷8（留 620+）
10. 不执行人审（B3 证书只从现有数据生成）
11. 做不完的诚实登记，留 620

> 619 §五：**本批不修改 CORE_TOOLS** ⇒ 无需 `tool_integrity --update`（C1 只改 `tools/snapshot_manifest.py`，该文件不在 CORE/钉扎面内，已核对）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
