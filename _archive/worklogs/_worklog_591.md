# _worklog_591 · 信任根扩边：v7 基线重冻结 + 治理文档完整性 + 测试器入哈希

> 性质：机械建设批。不 push、不 golden accept、不替人签。本文件不入库。

## §0 开工先量（只读，无 commit）

### 0.1 基线确认
- **HEAD = `6346b26`**（589 docs/worklog），**非任务书假设的 `d36d5c8`** —— 见 §6 偏差 **D0**。
- 工作树：两条 CRLF 假脏 `data/mutation/full_baseline_v4.json` / `evidence/conc/EV-CONC-001.md` 仍在（全程不碰）。
- `tool_integrity.py --check` → **exit 0**（5 核心工具与基准一致）。
- `gate_engine.py --check` → **exit 0**，**规则 63 · 命中 191（block=0 warn=186 advice=5）**。
- `poison_drill.py` → **exit 0**，**124/124 · RULE-COVERAGE 39/63 · 表观 100% · 诚实 95.2% · 双指标 100%/100%**。
- `atom_evidence_replay.py --check` → **exit 0**，**confirm=56 refute=0 infra_error=0**。

### 0.2 v7 数字预跑（串行 `--jobs 1`，清 `build/replay_manifest.json` 起手）
- 冷跑 #1 与热跑 #2 **逐变体 0 差异**（only_cold=0 / only_hot=0 / changed=0）。
- 两次一致：**变体 1593 · blocked 1405（严格 811）· escaped 1 · n_a 179 · malformed 0 · equivalent 8 · 可判 1406**。
- 逐算子可判：**M1 65 · M2 168 · M3 65 · M4 224 · M5 29 · M6 716 · M7 139**。
- 唯一 escaped = **M1 / evidence/conc/EV-CONC-001.md / 删 negative_controls**（冻结 TCE）。
- **与任务书预期逐条相符 ⇒ 允许进入任务 1。**

### 0.3 治理文档清单
- `References/architecture_架构演进/**/*.md` 总数 = **329**（无子目录）。
- `tool_integrity.CORE_TOOLS = (gate_engine.py, atom_evidence_replay.py, poison_drill.py, toolchain.py, cppbible.py)` —— **不含 References**；`TEST_CONFIG_TOOLS` 尚未定义（任务 3 新增）。
- `doc_lint.py` 扫描面 = `docs/kernel/`（`DOCS = ROOT/"docs"/"kernel"`），**不覆盖 References/**。

### 0.4 测试器现状
- `tests/conftest.py` 共 **140 行**；关键钩子：`pytest_configure`(L93)、`pytest_collection_modifyitems`(L128)、
  `replay_serial` fixture(L79)、`SLOW_MODULES`(L25/46/139)、`SERIAL_EXTRA`(L51/139)；**无** `pytest_runtest_makereport`。
- conftest.py **不在** CORE_TOOLS 中。

### §0 结论
任务 0 边界通过：v7 预跑数字与预期一致，任务 1 解锁。

## §6 偏差表
| # | 提示词假设 X | 实测 Y | 处理 |
|---|---|---|---|
| D0 | HEAD 起点 = `d36d5c8`（589 任务2） | 实际 HEAD = **`6346b26`**（589 之后还有 T4a `859f3d5`、T1补 `577d57a`、T4b `442020f`、worklog `6346b26` 共 4 个 commit） | v7 的 `frozen_at_commit` 按任务书写 `d36d5c8`（= M2 净化落点）；另加 `frozen_at_head` 记真实 HEAD。T4a/T4b/worklog **不影响 mutation 数字**（新工具/注释/文档），故 v7 数字仍与预期一致 |
| D1 | 1.4「再跑一次全量对账」 | 复用 0.2 的**热跑 #2**（同为串行 jobs1、代码自 #2 起未变）⇒ 省一次 ~15min 串行全量 | 见任务 1 |
| D2 | §1.2「metrics_collector 默认基线引用从 **v6** 改为 v7」 | 实际 metrics_collector 硬编码的是 **v5**（非 v6），且 `test_metrics_collector_curves.py`(1375/185) 与 `test_overturned_curves.py`(source=v5) 各硬编码 v5 口径 | 按任务**意图**把"当前尺子"v5→**v7**、v5/v6 入历史时点，并同步这 2 个测试的数字断言（属数据口径更新，非判决逻辑改动） |
| D3 | §1.2「data/metrics.jsonl 追加一行」（交付清单计入 Task1 commit） | `/data/metrics.jsonl` 被 `.gitignore` 排除（第 88 行，**未跟踪**运行期数据文件）⇒ 追加只落工作树、**不入 commit** | 已按任务追加（本地），不强行 `git add -f`（尊重既有 gitignore 设计）；如实登记 |
| D4 | 交付清单「4 个 commit（任务1/2/3/4）」 | 任务 4 是**纯验收（无文件改动）** ⇒ 无 commit；worklog 按「不入库」亦未提交 ⇒ 实际 **3 个 commit**（5d2a6ae/bf63621/bd9fdfb） | 如实登记；不造空 commit |

---

## 任务 1（commit `5d2a6ae`）v7 基线重冻结
- 新增 `data/mutation/full_baseline_v7.json`（源于 0.2 冷跑 #1），加 `frozen_at_commit=d36d5c8`、
  `frozen_at_head=6346b26`、`notes`（M2 un-mask 说明 + 唯一 escaped=M1 TCE）。
- `data/mutation/full_baseline_v6.json` 保留不删，加 `superseded_by=full_baseline_v7.json`、`frozen_at_commit=55c01c8`。
- `data/metrics.jsonl` 追加 v7 时点（ruler_version=v7，逃逸率 1/1406，逐算子可判 65/168/65/224/29/716/139）——**见 D3（未入库）**。
- `tools/metrics_collector.py`：当前尺子 v5→v7，v5/v6 入历史（连带同步 2 个测试，见 D2）。
- 新增 `tests/test_mutation_baseline_v7_591.py`（5 条）。
- 验收：v7 顶层 **1593/1405/1/179/8/可判1406** · M2 **168/0/27/0** · 唯一 escaped=M1·EV-CONC-001；
  热跑 #2 与 v7 **逐字段 0 差异**；两 selfcheck exit0；测试全绿、ruff All passed。

## 任务 2（commit `bf63621`）治理文档完整性防护
- 新增 `tools/governance_doc_guard.py`（manifest 机制 + 弱化指令扫描 + CLI verify/update/scan/preflight）。
- 首次生成 `data/governance_docs_manifest.json`（**329** 份投喂词哈希）+
  `data/governance_weakening_scan.json`（**high=55 / medium=162 / low=32，命中 93 份**）。
- 新增 `tests/test_governance_doc_guard_591.py`（6 条全绿）。
- **边界（如实登记）**：manifest 只发现"文档变了"、判不了善意/恶意；scan 只发现"含弱词"、判不了语义；
  不做 PKI/签名；只扫 `References/architecture_架构演进/`；**manifest 自身不在校验范围内**（与 `.tool_checksums`
  同类信任边界，PoC-1 敞口延伸）。

## 任务 3（commit `bd9fdfb`）测试器配置入哈希面
- `tool_integrity.py`：`TEST_CONFIG_TOOLS`（conftest.py + pyproject.toml）+ compute/verify/write test_config +
  `load_baseline` 节感知（core 停在 `#`）+ `--check-test-config`；`--update` 写 core + test_config 两节。
- `tests/conftest.py`：`pytest_configure` 首句加启动自检（`--check-test-config` 非 0 ⇒ `pytest.exit(2)`）。
- `tools/.tool_checksums` 重钉（core 5 + test_config 2）。
- 新增 `tests/test_test_config_integrity_591.py`（5 条全绿）。
- **边界（如实登记）**：钩子本身在 conftest 里，"改钩子+重签基准"仍可绕过 ⇒ 纵深防御、非根治
  （根治需 conftest 入 CORE_TOOLS 且 enforce() 在 pytest 之外独立校验，会改架构，本批不做）。

## 任务 4 · 收工总验收（fresh，退出码定论）
1. `tool_integrity.py --check` → **exit 0**
2. `tool_integrity.py --check-test-config` → **exit 0**
3. `gate_engine.py --check` → **exit 0**，**63/191（block=0 warn=186 advice=5）逐字不变**
4. `poison_drill.py` → **exit 0**，**124/124 · 39/63 · 表观 100% · 诚实 95.2% · 双指标 100%/100%**
5. `atom_evidence_replay.py --check` → **exit 0**，**confirm=56 refute=0 infra_error=0**
6. `governance_doc_guard.py verify` → **exit 0**
7. `governance_doc_guard.py preflight` → **exit 2**（55 条 high 级弱化关键词，**均为历史投喂词的描述性内容**，
   非新插入攻击指令；任务书允许如实记录、不强行清零）—— 见交人项 1
8. v7 全量对账：热跑 #2 与 `full_baseline_v7.json` **逐字段 0 差异**（复用见 D1）
9. `mutation_fuzz.py --selfcheck-determinism` → **exit 0**
10. `mutation_fuzz.py --selfcheck-equivalent` → **exit 0**
11. `pytest -m "not slow" -n auto` → **exit 0**（481 passed / 1 skipped / 5 snapshots）
12. `pytest -m slow -n0` → **exit 1**，唯一红 = `test_json_output.py::test_golden_lock_json`（334 passed）
13. ruff（本批全部新增/改动 .py）→ **All checks passed**（exit 0）
14. `git diff --quiet -- atoms evidence Examples Book` → **exit 0**
15. `git status --short`：仅本批文件（两条 CRLF 假脏 + `_worklog_591.md` 按惯例未入库）；无意外遗留

## 交人项
1. **governance 首次扫描 55 条 high**：均为历史投喂词中的**描述性讨论**（如"降级为 warn""跳过门禁""豁免毒样例"
   出现在任务书正文里讨论该做法），需人审逐条确认是"描述"还是"真实攻击指令"——**苦力不自行判定语义**。
2. **manifest 自身不在校验范围**（与 `.tool_checksums` 同类信任边界）；是否进一步加固（如 manifest 入 git 签名）由人裁决。
3. **conftest 钩子的纵深防御限制**（改钩子+重签可绕过）已登记；是否改架构（pytest 启动脚本独立于 conftest）由人裁决。
4. 588 期遗留 CRLF 假脏两条（`full_baseline_v4.json` / `EV-CONC-001.md`）本批沿例未动。

