# 607 任务 0 · 两个债务的现状盘点（只读）

> 口径：全部数字为**本机实跑**（2026-09-19，`.venv\Scripts\python.exe`），命令逐条附在节末。
> 独立性：命题数字由 **PyYAML 独立解析**（`%TEMP%` 探针，不入库）取得，并与 gate 规则的 warn 条数**交叉核对**。

---

## 债务 1 · 治理台账

### 实测

- `python tools/governance_doc_guard.py verify` → **exit 0**：
  `[gov] manifest 一致 ✓（self_hash 已校验）`
  ⇒ **台账当前并不是"过期/不一致"状态**（603 chore `1eaba2c` 之后没有新文档落进它的扫描面）。
- manifest（`data/governance_docs_manifest.json`）：**344 条**，**全部**是
  `References/architecture_架构演进/*.md`——该目录**无子目录**（`Get-ChildItem -Directory` 空）。
- 任务书假设"'\_arch\_v12 到 \_arch\_v17、PM 文档、603/604/605/606 投喂词'未纳入台账导致 verify 报错"：
  **不成立**，两个具体原因：
  1. `_arch_v*` **不在** `References/architecture_架构演进/` 下，而在**仓库根**（`_arch_v2`…`_arch_v17`、`_arch_free`，
     共 **17** 个目录 / **156** 篇 `.md`）。`scan_docs()` 用 `DOCS_ROOT.rglob("*.md")`，从来看不到它们 ⇒
     台账里**从来没有**它们的条目，自然也不会报"缺"。
  2. `_auto/inbox/*.md`（604/605/606/607，共 **4** 篇）同样在根下，不在扫描面内。
- 根目录 `PM_*.md` / `PUSH_*.md` / `INDEX_*.md` / `MATRIX_*.md` / `CHECKLIST_*.md`：**当前 0 个文件**
  （注意：根下确有 `INDEX.md`，但它**不匹配** `INDEX_*.md`）。

### 结论：真实债务 = 台账**扫描面过窄** + 更新流程未脚本化

- 现有覆盖面 **344** 篇；**未覆盖面 160 篇** = `_arch_*/**/*.md` **156** + `_auto/inbox/*.md` **4**。
- 历轮靠人工 `update --force`（**全量重签**）顺手刷新，代价是"重签会顺手掩盖内容篡改"。
  607 要做的是**增量机械登记**：只**追加**新文档、只**标记**消失文档，**绝不刷新既有 hash**。
- **关键约束（施工必守）**：一旦把新扫描面接进 `verify`，**verify 与 auto-update 必须用同一扫描面**，
  否则新增条目会被 verify 判成"删除"而报红（本轮实现为此抽出统一入口 `iter_governed_docs()`）。

### 命令

```text
python tools/governance_doc_guard.py verify        # -> exit 0，manifest 一致
python -c "import json;m=json.load(open('data/governance_docs_manifest.json',encoding='utf-8'));print(len(m['files']))"   # -> 344
Get-ChildItem -Directory | ? {$_.Name -like '_arch_*'}    # -> 17 个目录 / 156 篇 md
Get-ChildItem _auto\inbox -File -Filter *.md              # -> 4 篇
```

---

## 债务 2 · 命题活性锚（`OBSERVATION-LIVENESS`）

### 实测（gate 侧）

- `python tools/gate_engine.py --check` → **exit 0**（整体仍 0 block）；其中
  `[WARN] OBSERVATION-LIVENESS` **50 条**。
- 语义澄清（读规则源码）：该 warn 的判据是"observation 命题**未在命题级**指认证伪锚"
  （`claim_structured[*].liveness = {kind: fixture_symbol, symbol: …}`），
  **不是**"缺工件断言"——后者由 **block** 规则 `OBSERVATION-NEEDS-ARTIFACT` 负责，实测 **0** 命中
  ⇒ 这 50 条观测命题**都有**工件断言，缺的只是**命题级锚**。

### 实测（独立解析 atoms）

| 指标 | 实测 |
|---|---|
| atoms 卡（`atoms/**/*.md`） | **28** 篇 |
| 含 `claim_structured` 的卡 | **27** 篇（1 篇无命题结构 ⇒ 不进分母） |
| 命题总数 | **79** |
| └ observation | **50** |
| └ inference | **29** |
| 含 `liveness` 字段的命题 | **0**（全库 `^\s*liveness:` 命中 **0 文件**） |
| 缺 liveness 的 observation | **50**（= 全部 observation） |

**交叉核对**：独立解析得到的 **50** 与 gate 报的 **50** 条 warn **一致**（两条独立路径互证）。

### 缺 liveness 清单（27 卡 / 50 条，按卡分组）

| 卡 id | observation 数 | 缺 liveness 的命题 id |
|---|---|---|
| ATOM-CONC-FENCE-001 | 1 | prop-1 |
| ATOM-CONC-LOCK-001 | 1 | prop-1 |
| ATOM-CONC-RACE-001 | 1 | prop-1 |
| ATOM-HIST-AUTOPTR-001 | 3 | prop-1 / prop-2 / prop-4 |
| ATOM-LANG-INLINE-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-ALIGN-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-ALLOC-001 | 3 | prop-1 / prop-2 / prop-3 |
| ATOM-MEM-ALLOC-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-LEAK-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-LEAK-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-MOVE-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-NEW-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-PERF-001 | 1 | prop-1 |
| ATOM-MEM-PERF-002 | 1 | prop-1 |
| ATOM-MEM-PERF-003 | 1 | prop-1 |
| ATOM-MEM-PERF-004 | 2 | prop-1 / prop-2 |
| ATOM-MEM-RAII-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-RAII-002 | 3 | prop-1 / prop-2 / prop-3 |
| ATOM-MEM-RVREF-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-SHARED-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-SHARED-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-UNIQUE-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-UNIQUE-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-VALUE-001 | 2 | prop-1 / prop-2 |
| ATOM-MEM-VALUE-002 | 2 | prop-1 / prop-2 |
| ATOM-MEM-WEAK-001 | 2 | prop-1 / prop-2 |
| ATOM-UB-GRAY-001 | 1 | prop-1 |
| **合计** | **50** | 27 卡 |

### `needs_review`（"无法被单一工件证伪 ⇒ 应改 inference"）候选

- 现库 **0** 条：任务书给 `needs_review` 的定义是"observation 且 `liveness.kind == external_basis`"，
  而全库**一个 `liveness` 字段都没有** ⇒ 该分类**只可能在补锚之后出现**。
- 工具仍按任务书实现该分类，并在报告中明写"当前为 0，原因是还没有任何命题填过 liveness"，
  以免把"0 条 needs_review"误读成"没有任何命题需要改标"。

---

## 未做（按任务书边界）

- **不**自动补 `liveness`（人审权力）：本轮只审计 + 出清单。
- **不**改 `atoms/` 任何卡（受控目录零改动）。
- **不**对治理文档做语义审查：auto-update 只是**机械登记**，判"善意/恶意"仍靠人读 diff + `scan` 的 high 清单。
