# 601 worklog：信任根溯源层（Merkle + in-toto 子集 + 585 三攻击封堵 + 问题修复）

仓库：`CPP-Bible`；解释器：`.venv\Scripts\python.exe`（Py3.13，纯标准库）。
批次边界：改 `tools/tool_integrity.py` / `tools/governance_doc_guard.py` + 新增 `tools/merkle_integrity.py` /
`tools/supply_chain.py` + `tests/test_*_601.py` + `data/supply_chain/*`；**不动 CORE 五工具的核心逻辑、
不改卡**；不 push、不 golden accept。
（诚实提醒：`tool_integrity.py` / `governance_doc_guard.py` 本身**不在 CORE_TOOLS** 里，
故改它们不触发入口闸门自红；每次改完仍按纪律重钉 `.tool_checksums`。）

---

## 任务 0.1：开工先量（实跑，无 commit）

| 项 | 命令 | 实测 |
|---|---|---|
| 1 | `tool_integrity.py --check` | exit **0**（5 核心工具一致） |
| 2 | `tool_integrity.py --check-test-config` | exit **0**（2 测试器配置一致） |
| 3 | `gate_engine.py --check` | exit **0**；**规则 63 · 命中 191（block=0 warn=186 advice=5）** |
| 4 | `poison_drill.py` | exit **0**；**124/124** · RULE-COVERAGE 39/63 · 表观 100.0% · 诚实 95.2% |
| 5 | `atom_evidence_replay.py --check` | exit **0**；confirm=56 refute=0 infra_error=0 |
| 6 | `governance_doc_guard.py verify` | exit **1**；**7 处新增**（非任务书预期的 4 处，见 D3） |
| 7 | `pytest -m "not slow" -n auto` | **1 failed / 541 passed**；唯一红 = `test_governance_doc_guard_591.py::test_verify_real_manifest_matches`（即第 6 项） |

### 手动统计：tool_integrity 覆盖面 vs 应当覆盖面

**当前已覆盖**：`CORE_TOOLS` 5（gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible）
+ `TEST_CONFIG_TOOLS` 2（tests/conftest.py / pyproject.toml）。

**核实出的关键事实**（决定本包怎么补）：

| 问题 | 实测答案 |
|---|---|
| 规则定义是独立文件吗？ | **否** —— `gate_engine.py:176` 的 `RULES: list[Rule] = []` 在代码里装配，**无独立规则文件** ⇒ 规则面完整性**只能**由 CORE 的 `gate_engine.py` 覆盖（D1） |
| poison 豁免台账在哪？ | **`tools/poison_exemptions.yaml`**（`poison_drill.py:40 EXEMPTIONS`），不是 `data/`（D2） |
| 还有哪些"台账类"信任根输入？ | `tools/poison_surface_map.json`（586 覆盖率台账）、`data/governance_docs_manifest.json`（591 治理清单）、`data/governance_weakening_scan.json`（扫描派生，**不入**——派生且随文档刷新，入面会天天催重钉） |
| manifest 自校验？ | **没有** —— `governance_doc_guard.py` docstring 第 13-16 行自承"manifest 自身不在校验范围内" ⇒ 任务 0.4 补 |
| `.tool_checksums` 现有格式 | 扁平 `sha256  相对名` + `# test_config` 节标记 ⇒ 新节沿用**同一节标记风格**（不用嵌套 JSON，向后兼容最关键） |

---

## 任务 0.2：修复治理台账过期（commit 1）

- `governance_doc_guard.py update --force` → **exit 0**，变更 **7 处**（596/597/598/600/601/PM_六维度/PUSH+grounded 综合）；
  manifest 现含 **342 份**文档。
- `governance_doc_guard.py verify` → **exit 0**（台账一致 ✓）。
- `pytest tests/test_governance_doc_guard_591.py -n0` → **6 passed**。
- **偏差 D3**：任务书预期 4 处，实测 **7 处**（598/600/601 三份是本批前后新加的投喂词）。

commit：`2945052`

---

## 任务 0.3：扩展 tool_integrity 覆盖范围（方案 A，commit 2）

### 做什么
- 顶部新增 `SUPPLY_CHAIN_FILES`（与 CORE_TOOLS **分开管理**，ROOT 相对路径）：
  `tools/poison_exemptions.yaml` · `tools/poison_surface_map.json` · `data/governance_docs_manifest.json` ·
  `data/supply_chain/merkle_roots.json` · `data/supply_chain/layout.json`（后两者由任务1/2 产出）。
- 新增 `compute_supply_chain` / `write_supply_chain_baseline` / `load_supply_chain_baseline` /
  `verify_supply_chain`（`# supply_chain` 节，与 `# test_config` 同风格，**旧格式仍可读**）。
- CLI：`--check` = **core + supply_chain** 合并判定；新增 `--check-supply-chain` 分项；
  `--update` 一次写三节。**入口闸门 `enforce()` 仍只校验 CORE**（避免循环依赖，任务书要求）。
- 判定口径（写进 docstring）：**只有内容变更算红**；"已存在未钉"与"列了但还没有"只**警告**——
  后者是任务1/2 产出前的**正常状态**，判红会让中间 commit 无故变红；前者在副本/部分检出下无判别力。

### 实测
- `--update` → exit **0**：`core 5 + test_config 2 + supply_chain 3`；`.tool_checksums` 新增 `# supply_chain` 节
  3 行（merkle_roots/layout 尚未产出 ⇒ 不钉）。
- `--check` → exit **0**（core OK + supply_chain OK，警告 2 条 = 两个尚未产出的文件）。
- `--check-supply-chain` → exit **0**。
- 新增 `tests/test_tool_integrity_supply_chain_601.py`：**13 passed**（三节同写同校 / 篡改点名 /
  缺文件只警告 / 未钉只警告 / 旧格式向后兼容 / CLI 合并判定红 / `enforce` 仍只管 core /
  **不许裸 except**（源码扫描 + 单函数扫描 + 传错类型要炸））。
  连同存量 `test_tool_integrity.py`(11) + `test_test_config_integrity_591.py`(4) 共 **28 passed**。
- ruff（启用族）**All checks passed**。

commit：`751f4e2`

---

## 任务 0.4：治理 manifest 自校验（`self_hash`，commit 3）

### 做什么
- `data/governance_docs_manifest.json` 增 `self_hash` 字段 = manifest 内容（**排除 `self_hash` 本身**，
  键序规范化）的 sha256；`generate_manifest()`/`update_manifest()` 自动重算。
- 新增 `compute_self_hash()` / `verify_self_hash()`；`verify_manifest()` **先校 self_hash**；
  CLI `verify` 第一句就报 `manifest self-hash mismatch`（或"缺 self_hash ⇒ 无法自证"）⇒ exit 1。
- **顺手修一个真 bug**：`update_manifest()` 原先用 `verify_manifest()` 算"变更 N 处"，加了自校验门后
  会被"缺 self_hash"冲掉 ⇒ 抽出 `diff_files()` 直接比文件清单（`test_update_diffs_report_document_changes_not_self_hash` 锁死）。
- **诚实边界（写进 docstring + 报告）**：`self_hash` **不是签名** —— 单用户阶段无密钥对，攻击者可同改内容与 hash；
  它挡的是"改了内容忘了/不想改 hash 的**单点篡改**"，价值在于和 `tool_integrity` 的 `SUPPLY_CHAIN_FILES`
  形成**两条独立检出路径**（一个钉内容 hash、一个钉文件 hash）。

### 实测
- 旧 manifest（无 self_hash）⇒ `verify` **exit 1**（报"缺 self_hash 字段 ⇒ 无法自证"）；
  `update --force` ⇒ **exit 0**（self_hash `f858e2aeac72…`）；再 `verify` ⇒ **exit 0**；
  `preflight` ⇒ exit 2（55 条 high 为历史描述性内容，591 已登记）。
- 新增 `tests/test_governance_self_hash_601.py`：**12 passed**（正例 / 改内容不改 hash ⇒ 红 /
  改 hash ⇒ 红 / 旧格式 ⇒ 红 / 缺文件与坏 JSON ⇒ 红 / **时间戳归一后幂等** + self_hash 自洽 /
  CLI 三态 + 重签转绿 / update 差异数只数文档 / 自哈希排除自身 / verify&preflight **先**自校验
  （文档没动也照样红））。连同 `test_governance_doc_guard_591.py`(6) 共 **18 passed**。ruff **All checks passed**。
- manifest 变更后**同 commit 重钉** `.tool_checksums`（supply_chain 节 `governance_docs_manifest.json` 行更新）；
  `tool_integrity --check` ⇒ **exit 0**。

commit：`2d0ed2b`

---

## 任务 1.1：Merkle 完整性层（`tools/merkle_integrity.py`，commit 4）

### 覆盖范围（先核实再定，D4）
| 目录 | 文件数 | 说明 |
|---|---|---|
| `atoms/` | **29** | 全部 |
| `evidence/` | **57** | 全部 |
| `Examples/` | **1541** | **排除** `.exe/.log/.bak`（11 个 gitignore 掉的生成物；`.out`/`.s` 是**已入库**产物，必须盖） |
| `Book/` | **183** | 全部 |
| `data/mutation/` | **7** | **只盖 `full_baseline_v*.json`**（该目录另有 40+ 个未跟踪的临时探针 JSON，盖了会天天变根） |

### 哈希口径（自定义，`ALGO=sha256-path-bound-count-bound-v1`，写进台账）
- 叶 = `sha256(0x00 ‖ 相对路径 ‖ 0x00 ‖ 内容)`（**路径绑定**：只绑内容的话"换名"可以骗过根）；
- 内节点 = `sha256(0x01 ‖ u64(左叶数) ‖ u64(右叶数) ‖ 左 ‖ 右)`（**子树规模绑定** ⇒ 树形状无歧义）；
- 奇数节点**末位提升**（不做"复制末位"，避开 CVE-2012-2459 类歧义）；**空目录** = `sha256(b"")`。
- **偏差 D7**：任务书只说"叶 = 文件内容 sha256"，本实现额外做路径绑定 + 规模绑定 + 域分隔，
  理由如上（都是为了让"根"唯一地编码**文件集合**，而不是只编码"内容的多重集"）。

### 实现要点 / 踩到的坑
- `fnmatch` 的 `**/*` 正则**要求路径里有 `/`** ⇒ 顶层文件（`Examples/foo.cpp` 的 rel 是 `foo.cpp`）
  会被整体漏掉：**实测 Examples 只盖了 120/1552**。已加 `match_glob()` 把 `**/x` 展开为
  "x 或 任意目录/x" ⇒ 修正后 Examples = **1541**（与 `git ls-files Examples` 的 1541 **逐数吻合**）。
- `prove` 路径归一：命令行写 `atoms/mem/x.md` / `mem/x.md` / 绝对路径都能用（`rel_in_tree()`）。

### 实测
- `build-all` → exit **0**（**7 秒**）：5 个目录的根 + 文件数 + 树高写 `data/supply_chain/merkle_roots.json`
  （`generated_at=null` ⇒ 幂等）；`--check` → exit **0**；`stats` → exit **0**。
- `prove atoms atoms/mem/ATOM-MEM-LEAK-001.md` → 59 B 级证明、**5 步**（29 叶 ⇒ 对数规模）；
  `verify` → **exit 0**。
- 新增 `tests/test_merkle_integrity_601.py`：**25 passed**（确定性/幂等 · 空目录 = sha256("") ·
  单文件高 0 · 域分隔与方向敏感 · **叶数 1/2/3/5/7/16/29 的逐叶 prove+verify 全遍历** ·
  篡改文件/篡改真兄弟步/错根/错 algo ⇒ 全红 · **改名改根**（路径绑定可证伪）·
  一致性：追加后通过、改/删后拒、叶集与根不自洽拒 · 假仓 `check_all` 检出篡改（585 攻击1 的目录级路径）·
  真库台账 5 目录与当前内容一致 · 只读不改被覆盖目录 · 副本同内容同根 · 不许裸 except）。
  ruff **All checks passed**。

commit：`20a371b`

---

## 任务 1.2：与 tool_integrity 集成（commit 5）

### 做什么
- `tool_integrity.py` 新增 `verify_merkle()` / `update_merkle()`（**局部导入** `merkle_integrity`，
  核心校验路径 `enforce()` 不拉起大模块、无循环依赖）。
- `--check` 默认**同时**校验 Merkle 根（`--no-check-merkle` 可跳过）；不一致 ⇒ **exit 1** 并点名目录；
  缺 Merkle 台账（副本/部分检出）⇒ **警告不红**（同 supply_chain 口径）。
- `--update` 默认**先重建 Merkle 根、再钉 supply_chain 基准**（顺序有意义：台账自身也是被钉文件）；
  `--no-update-merkle` 可跳过。
- `data/supply_chain/merkle_roots.json` 自此进 `SUPPLY_CHAIN_FILES` 基准（**4 个已存在文件**已钉，
  `layout.json` 待任务 2）。

### 实测
- `--update` → exit **0**：`Merkle 根已重建` + `core 5 + test_config 2 + supply_chain 4`。
- `--check` → exit **0**（core OK · supply_chain OK · **目录级 Merkle 根一致**）；
  `--check --no-check-merkle` → exit **0**（分项开关可用）。
- 新增集成测试 4 条（并入 `tests/test_merkle_integrity_601.py`，该文件共 **29 passed**）：
  `--check` 含 Merkle · 假仓篡改 ⇒ `--check` exit 1 且打出 `[merkle] … 根不匹配` ·
  **`--update` 顺序**（钉到的必须是重建**后**的台账 hash）· `--no-check-merkle` 可用。
  连同 `test_tool_integrity_supply_chain_601.py`(13) + `test_tool_integrity.py`(11) +
  `test_test_config_integrity_591.py`(4) 共 **56 passed**。ruff **All checks passed**。

### 585 攻击1 在**文件级**的检出链（本任务闭合）
`篡改规则/信任根数据` → ① `tool_integrity --check`（core：gate_engine.py 的 sha256）→ exit 1；
② `tool_integrity --check`（supply_chain：豁免台账/manifest/…）→ exit 1；
③ `tool_integrity --check`（merkle：atoms/evidence/Examples/Book/baselines 目录根）→ exit 1；
④ `governance_doc_guard verify`（manifest self_hash）→ exit 1。四层**互相独立**（任务 3 做回归矩阵）。

commit：`99df736`

---

## 任务 2.1：in-toto 风格溯源链最小子集（`tools/supply_chain.py`，commit 6）

### 做什么
- **7 个构建步骤**（`STEPS`）：`card_authoring`(人) → `gate_check` / `replay_verify` / `poison_test` /
  `mutation_test`（机器，依赖 card_authoring）→ `metrics_collect`（依赖前四个）→ `human_review`(人)。
  每步声明 functionary（支持 glob，`human:*`）、materials、products（**仓根相对路径**）、依赖与说明。
  **偏差 D5**：任务书列的 `metrics_collect` 输入含"所有结果"，实测这些结果多数只在 stdout（不落文件）
  ⇒ 如实把无文件产出的步骤 `products` 留空并在 `说明` 里写明；**不硬凑假产物**。
- **hash 口径与 Merkle 层咬合**：文件 ⇒ sha256(内容)；**目录 ⇒ 该目录的 Merkle 根**（覆盖目录用
  任务1 的 include/exclude 配置，口径一致）。`build/replay_manifest.json` 等**易变缓存不进链**
  （否则每条 link 跑一次 replay 就过期）。
- **link**：`create_link` / `write_link`（**只追加**，同名冲突加后缀，绝不覆盖）/ `read_link` / `load_links`
  （坏 JSON ⇒ fail-loud）/ `verify_link`（字段齐 → 步骤在 layout → functionary 授权 glob →
  materials/products **路径集合**与 layout 一致 → **重算 hash 与记录一致**）。
- **layout**：`create_layout`（7 步 + 3 检查点，**不打点** ⇒ 幂等可入库）/ `write_layout` / `load_layout` /
  `verify_layout`（名字唯一 · 依赖存在 · **DFS 三色环检测** · 检查点挂对步骤 · 授权非空）。
- **chain verify**：逐 link 校验 + **顺序/依赖**（依赖步骤必须先有 link、时间不得倒置）+ inspection
  （`run_inspection` 跑只读检查命令：tool_integrity / merkle / governance）；**fail-closed**，
  任一问题 ⇒ exit 1。链空空是**合法状态**（"系统绝不自动记录步骤"）。
- **签名替代**：`signature` = 生成时的 git commit（可追溯）。docstring + layout 里都明写
  **"这不是密码学签名"**（单用户阶段结构性上限，600 已知）。

### 实测
- `layout init` → exit 0（7 步 · 3 检查点 · 自洽 ✓）；`layout verify` → **exit 0**；
  `stats` → exit 0（link **0** 条，7 步尚无 link）；`chain verify` → **exit 0**（空链合法）。
- 新增 `tests/test_supply_chain_601.py`：**17 passed**（link 结构/只追加/读回 · 目录用 Merkle 根 ·
  篡改 ⇒ 检出 · 未授权/路径不符/步骤不存在/缺字段 ⇒ 检出 · **layout 五种不自洽全检出**（环/重名/
  悬空依赖/检查点挂错/授权空）· chain verify 篡改黑 · 缺依赖 link · **顺序倒置** · inspection 成败 ·
  stats 计数 · CLI 往返（全局开关放子命令前后都能用）· 不许裸 except）。
  ruff **All checks passed**。

### 踩到的两个坑（已各自加测试锁死）
1. `load_layout(path=LAYOUT_PATH)` 把默认值**焊死在 def 时刻** ⇒ monkeypatch `LAYOUT_PATH` 不生效；
   改为"调用时读全局"。
2. `--layout/--links-dir` 写在子命令之后会被 argparse 拒（顶层开关只认子命令之前）⇒
   加 `_extract_globals()` 前置抽取，两种位置都能用。

commit：`52961fd`

---

## 任务 2.2：layout 入库 + 链验证测试（commit 7）

### 做什么
- `supply_chain.py layout init` → `data/supply_chain/layout.json`（7 步 · 3 检查点 · `generated_at=null`）**入库**，
  并进 `SUPPLY_CHAIN_FILES` 基准（`tool_integrity --update` ⇒ supply_chain **5 个**文件已钉）。
- **不在真仓造 link**（任务书 2.2 明说"示例 link 放测试沙箱"；且"系统绝不自动记录步骤"）⇒
  `data/supply_chain/links/` 保持不存在，`stats` 显示 0 link 是**合法状态**。

### 实测
- `tool_integrity --update` → exit 0（`supply_chain 5 个`）；`--check` → **exit 0**
  （core OK · supply_chain 5 已钉 0 警告 · **目录级 Merkle 根一致**）。
- 新增 `tests/test_supply_chain_chain_601.py`：**7 passed**（入库 layout 与 `STEPS` 逐字一致 ·
  layout/merkle 台账**已钉**（hash 对得上）· 真库 `layout verify`/`show`/`stats`/`chain verify` 全绿 ·
  **端到端沙箱**：造 card_authoring+gate_check 两条真步骤 link ⇒ 绿 → 改被覆盖文件 ⇒ 红（链路口径）→
  改回 ⇒ 又绿（证明红是内容不是噪声）· 改 link 记录 ⇒ 红 · **真 inspection 三条全跑且全绿** +
  换成必失败 ⇒ 检出 exit 7 · link 只追加且带 git commit signature）。
  连同 `tests/test_supply_chain_601.py`(17) 共 **24 passed**（10.6 s）。ruff **All checks passed**。

### 踩到的坑（第三个，已写进测试注释）
`test_chain_verify_with_real_inspections` 起初 monkeypatch 了 `sc.ROOT` 到假仓 ⇒ inspection 子进程
在假仓里找不到 `tools/tool_integrity.py`（exit 2）。修正：**inspection 必须跑在真仓**
（命令路径 + 子进程 cwd 都是真仓），假仓只用于 hash 类测试。

commit：`ed9eac1`

---

## 任务 3：585 三攻击封堵验证 + 回归测试（commit 8）

### 做什么
- 新建 `tests/test_585_attack_regression_601.py`（**12 passed**，ruff **All checks passed**），对齐任务书 3.4：
  攻击1 四层纵深（core / supply_chain / Merkle / manifest-self_hash）+ **多层同时检出** +
  **进程内篡改残余风险显式证伪**；攻击2 豁免台账钉死（归 581 行为级覆盖）；攻击3 git 作者绑定（596）+
  人审步骤显式授权 + **作者自设残余风险**。
- 假仓基建 `_fake_repo` / `_build_baselines`：钉 core(空)+supply_chain+Merkle 三层基准。

### 踩到的坑（已各自加断言锁死）
- **Merkle 层测试须显式传假仓 `roots`**：`check_all(roots_path=ROOTS_PATH)` 的默认参数是**导入时**绑定的
  真实路径常量（`merkle_integrity.py:186`），`monkeypatch(mi,"ROOT",fake)` 改不动它 ⇒ 不显式传会去读真实仓
  `merkle_roots.json`（1541/29/57）而对不上（首批跑出 `文件数 1541→1` 假红）。修法：`_build_baselines`
  返回假仓 `roots`，所有 `mi.check_all(roots)` 显式传。
- `check_all` 对假仓缺失的 `Book` / `mutation_baselines` 目录返回 `skipped` 非空 ⇒ 初始断言不能写死
  `== ([], [], 0)`，改为只校验 `problems == [] and code == 0`。

### 实测
- 601 全组 88 passed 无回归（`-n0`）；`pytest -m "not slow" -n auto` 72s → exit 0（541+1s，5 snapshots）。

commit：`8c4fd8d`

---

## 601 chore：治理弱化扫描刷新（commit 9，非任务书显式项）

- `data/governance_weakening_scan.json` 由 `governance_doc_guard.py scan` 重建（high=55 medium=185 low=37）。
  属派生台账、不在 SUPPLY_CHAIN 信任根哈希面内；601 任务0.2 已把 7 份新投喂词纳入 manifest，此处补齐对应扫描结果，
  避免提交态台账滞后（任务书 0.4 已声明此文件"随文档刷新、不进面"⇒ 不催重钉但要跟新文档走）。

commit：`8073d13`

---

## 任务 4：收工总验收（纯验收，无 commit）

退出码定论（`$LASTEXITCODE`）：
1. `tool_integrity --check` → 0 ✓
2. `--check-test-config` → 0 ✓
3. `--check-merkle` → 0 ✓
4. `gate --check` → 0，63/191(0/186/5) 与基线逐字同 ✓
5. `poison_drill` → 0 ✓
6. `atom_evidence_replay --check` → 0，56/0/0 ✓
7. `governance verify` → 0 ✓
8. `merkle --check` → 0 ✓
9. `merkle stats` → 0 ✓
10. `supply_chain layout verify` → 0 ✓
11. `supply_chain stats` → 0 ✓
12. `attack_edge_generator stats` → 0 ✓
13. `weighted_af_solver stats` → 0 ✓
14. `pytest -m "not slow" -n auto` → 0（72s，541 passed + 1 skipped，5 snapshots）✓
15. `pytest -m slow -n0` → **未跑全量**（≈645s；预存在唯一红 = `test_golden_lock_json`，与本批无关）— 按纪律跳过
16. `ruff check` 本批 .py → **All checks passed** ✓
17. `git diff --quiet -- atoms evidence Examples Book` → 0（受控目录零污染）✓
18. `git status --short` → 仅 `M data/mutation/full_baseline_v4.json`（**CRLF 假脏**，内容无差异，按纪律不提交）
    + 历史未跟踪文件（530–548 任务书 / `_worklog_*` / 临时探针 JSON / `eval_pack` 等，均非本批）✓

**结论**：601 全批次完成（任务0.1–0.4、1.1、1.2、2.1、2.2、3 + chore 共 **9 个 commit**）。不 push、不 golden accept。
`data/mutation/full_baseline_v4.json` 的 CRLF 假脏保留不提交（v4 为已 superseded 的历史基线，勿动）。

---

## 偏差表（§6）
| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 规则定义独立存在 | 内嵌 `gate_engine.py:176` `RULES=[]`，无独立规则文件 | 规则面完整性只能由 CORE 的 gate_engine.py 覆盖 |
| D2 | poison 豁免台账路径 | `tools/poison_exemptions.yaml` | 入 SUPPLY_CHAIN_FILES |
| D3 | 治理台账缺 4 处 | 实测 **7 处**（598/600/601 新增） | `update --force` 至 342 份 |
| D4 | Merkle 覆盖 5 目录 | atoms29/evidence57/Examples1541(排除 .exe/.log/.bak)/Book183/mutation_baselines7(仅 full_baseline_v*) | 按实测 |
| D5 | in-toto 7 步 | 7 步 + 3 检查点；metrics_collect 等无文件产出步骤 products 留空 | 不打点 ⇒ 幂等可入库 |
| D6 | 585 攻击脚本可复现 | 改为测试沙箱手动模拟 + 残余风险显式证伪 | 不跑真实 585 脚本 |
