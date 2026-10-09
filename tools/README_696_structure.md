# tools/ · 696 结构索引（功能分类 + 不物理搬动理由）

> 本文件由 **696 批次（线 B：工程线）** 新增。仓库既有 [`tools/README.md`](README.md)
> 保留不动（它讲命名规范与 `tools/utils/`），本文件补充**机器可生成的五类功能索引**
> 与「为什么不把 `tools/` 拆成子目录」的**逐条代价**。
>
> 机器可读清单：[`tools/manifest.json`](manifest.json)（由
> [`tools/gen_tool_manifest_696.py`](gen_tool_manifest_696.py) 生成）。

---

## 1. 分类总览（生成时快照）

生成命令：

```bash
.venv/Scripts/python.exe tools/gen_tool_manifest_696.py     # 写 tools/manifest.json
```

| 分类 | 数量（生成时） | 判据（文件名启发式，首个命中即归类） |
|---|---:|---|
| `analysis` | 510 | **兜底桶**：研究 / 实验 / 统计 / 生成类 |
| `verification` | 188 | `verify` `gate` `check` `audit` `guard` `integrity` `lint` `validate` `consistency` `poison` `drill` `replay` `invariant` `triage` `exempt` … |
| `visualization` | 19 | `visual` `plot` `chart` `graph` `dashboard` `render` `svg` `figure` `site_` `web_data` `html` … |
| `utils` | 6 | `util` `common` `helper` `path_config` `utf8_console` `toolchain` `console` `config` |
| `batch` | 4 | 文件名以 3 位批次号开头（如 `612_baseline.py`），或含 `batch` / `acceptance` |

> 数量是**生成时刻的快照**；并发批次增删 `tools/*.py` 会使其漂移。清单可随时重生成，
> 单测 `tests/test_tool_manifest_696.py` 用**运行时 glob 计数**断言，不写死数字。
> 总数（生成时）= **727**。

**为什么把 `analysis` 设为兜底**：本仓 `tools/` 主体就是研究/实验脚本，逐条穷举关键词会
过拟合命名；而 `utils` / `verification` / `visualization` / `batch` 四类的**命名信号清晰**，
用精确 token 先判，剩余即"分析/实验/其它"。**这是索引、不是判决**，不参与任何门禁 pass/fail。

---

## 2. 每类代表脚本

| 分类 | 代表脚本 | 说明 |
|---|---|---|
| `verification` | `gate_engine.py`、`tool_integrity.py`、`verify_paper_numbers.py`、`consistency_check.py`、`exempt_audit.py`、`poison_drill.py`、`atom_evidence_replay.py` | 门禁与校验：带 `--check`、失败退非 0 |
| `analysis` | `analyze_693_defect_types.py`、`benchmark_676l_analysis.py`、`mutation_fuzz.py`、`counts_659.py`、`compute_697_drift_algebra.py` | 分析 / 统计 / 生成产物 |
| `visualization` | `human_review_dashboard.py`、`web_data_pipeline_656.py`、`site_683_data.py`、`figures_683.py`、`knowledge_graph.py` | 图表 / 前端数据 / 静态站 |
| `utils` | `queyi_common.py`、`path_config_625.py`、`toolchain.py`、`utf8_console.py` | 共用基础设施 |
| `batch` | `612_baseline.py`、`613_baseline.py`、`coverage_probe_batch_634.py` | 批次一次性脚本 |

---

## 3. 为什么不把 `tools/` 物理拆成子目录

任务书原本设想按功能分子目录。**本批没有做**，与 693-D1 结论一致，理由必须写明：

| 代价 | 具体 |
|---|---|
| **信任根断裂** | `tools/tool_integrity.py` 的哈希面（core / test_config / supply_chain / ruler 四节，30+ 条）以**字面文件名**引用脚本，移动 ⇒ 全部失配 ⇒ 所有判定入口 `enforce()` fail-loud 拒绝运行 |
| **CI / 门禁变红** | `.github/workflows/ci.yml`、`tools/prepush_check.py`、`tools/cppbible.py` 的 `quality_gates` 元组、`pyproject.toml` 的 `quality_gates` 列表、`tests/conftest.py` 均以**字面路径**（`tools/xxx.py`）调用 |
| **回归成本与静默失败** | 700+ 脚本逐个改 import + 回归；失败模式是**静默的**（路径错但不报错） |
| **收益** | 目录更好看 |

**结论**：结构整理以**索引 + 清单 + 文档**形式落地（本文件 + `manifest.json`），
**不物理移动**任何既有文件。未来若要搬迁，必须**逐个脚本**做，每搬一个同步更新
`tool_integrity` 哈希面与全部字面路径引用。

---

## 4. 新增代码的落点约定（696 起）

- 需要一个**零依赖、无 `sys.path` 耦合**的公共库 ⇒ 用 [`tools/queyi_common.py`](queyi_common.py)
  （异常层次 / `setup_logging` / `read_json` / `sha256_file` / `atomic_write_text`）。
- 已在 `tools/utils/` 生态内的脚本 ⇒ 继续复用 [`tools/utils/`](utils/)（693-D1 建的共用包）。
  二者语义一致、**并列不互相依赖**，详见 `queyi_common.py` 的模块 docstring。
