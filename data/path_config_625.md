# 625 C1 · 工具路径配置化（QueYi Core 路径解耦第一步）

> 工具：`tools/path_config_625.py`（PathConfig）· 目标：核心工具不再写死 CPP-Bible 路径（触发标准⑤）
> 铁律：**只改路径解析，不改核心逻辑**；改 CORE_TOOLS 后同 commit `tool_integrity --update`。

---

## 一、写死路径现状

- 以 `ROOT = Path(__file__).resolve().parent.parent` 为根派生路径的工具：**约 130 个**（`tools/*.py`）。
- 分类：**核心工具 6**（gate_engine / atom_evidence_replay / poison_drill / tool_integrity / toolchain / cppbible）、
  辅助工具 ~124、测试工具（`tests/`）若干。

## 二、PathConfig 设计（`tools/path_config_625.py`）

| 组件 | 说明 |
|---|---|
| 默认值 | 仓根 = `tools/` 的父目录（与各工具原 `parent.parent` **完全一致**） |
| 配置文件 | `queyi_config.json`（`$QUEYI_CONFIG` 优先） |
| 环境变量 | `QUEYI_ROOT` / `QUEYI_ATOMS_DIR` / `QUEYI_EVIDENCE_DIR` / `QUEYI_DATA_DIR` / `QUEYI_EXAMPLES_DIR` / `QUEYI_BOOK_DIR` |
| 解析函数 | `resolve_atom_path` / `resolve_evidence_path` / `resolve_mutation_path` / `resolve_data_path` |
| 校验 | `validate()`（存在性/可写性）；`--check`（只读自检） |
| 优先级 | 环境变量 > 配置文件 > 默认（后者覆盖前者） |

**向后兼容**：不设环境变量/配置时，`root()` == 原 `parent.parent`，派生路径逐一相同。

## 三、改造详情

### 3.1 核心工具（6/6）✅
`ROOT` 改为 `path_config_625.root()`（默认值不变）：
`gate_engine.py` · `atom_evidence_replay.py` · `poison_drill.py` · `tool_integrity.py` · `toolchain.py` · `cppbible.py`。

### 3.2 辅助工具（20/20）✅
按「最常用」选取 20 个：`golden_lock` · `debt_ledger` · `governance_doc_guard` · `supply_chain` ·
`metrics_collector` · `mutation_fuzz` · `weighted_af_solver` · `replay_invariants` · `merkle_integrity` ·
`attack_edge_generator` · `knowledge_graph` · `defense_chain` · `escape_rate_honest_613` ·
`human_review_queue` · `human_review_dashboard` · `exemption_expiry` · `learner_state` · `prop_graph` ·
`ci_local_precheck` · `trust_root_status_check`。

### 3.3 未改造（留 626）
其余 ~110 个辅助工具 + `tests/` 内写死路径（测试工具依赖测试环境）⇒ **登记留 626**。

## 四、向后兼容验证（硬要求）

| 验证项 | 结果 |
|---|---|
| 6 核心工具可导入，`ROOT` = 仓根 | ✅ |
| `gate_engine.py --check` | ✅ 行为不变（warn 输出一致） |
| `atom_evidence_replay.py --check` | ✅ **confirm=56 / refute=0 / infra=0**（不变） |
| `poison_drill.py` | ✅ exit 0（124/124） |
| `tool_integrity.py --check` | ✅ Merkle 根一致 · 判决尺子 10 个一致 |
| `golden_lock check --no-replay` | ✅ 无恶化 |
| `debt_ledger check` | ✅ 问题 0 |
| 20 辅助工具导入 | ✅ 20/20 |
| `ruff check tools/ tests/` | ✅ All checks passed |
| `mypy tools/` | ✅ 0 errors |
| `pytest -m "not slow"` | ✅（提交 C1 后受控目录断言转绿） |

## 五、`tool_integrity --update` 重钉确认

已同 commit 重钉：`core 5 个 + test_config 2 个 + supply_chain 5 个 + ruler 10 个文件`。

## 六、局限性声明

1. **仅 26/约 130** 工具完成路径解耦（6 核心 + 20 辅助）；其余留 626。
2. `tests/` 内写死路径未改（依赖测试环境）。
3. 路径解耦只覆盖「根派生」层；工具内的**相对子路径字面量**（如 `"Examples/atoms"`）部分仍写死，留 626。
4. 未在真「异族靶场」上验证（仅证明默认 + env/config 覆盖可解析）。
