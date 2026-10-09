# ENGINEERING_696 — 696 批次（线 B：工程线）报告

> 执行者：线 B（工程线）。仓库：`CPP-Bible`（master）。
> 本批**只新增文件**，不运行任何 git 命令，不物理移动 `tools/` 下任何既有文件。
> 所有数字均来自本机**实测**；未测项一律标注"未测"。

---

## 0. 交付物清单（精确相对路径）

| # | 路径 | 说明 |
|---|---|---|
| 1 | `tools/manifest.json` | 由脚本生成的分类清单（五类，确定性排序） |
| 2 | `tools/gen_tool_manifest_696.py` | manifest 生成器（纯标准库 / docstring / 类型注解 / `__main__`） |
| 3 | `tools/README_696_structure.md` | 功能分类 + 每类代表脚本 + 不物理搬动理由（`tools/README.md` 已存在，故不覆盖） |
| 4 | `tools/queyi_common.py` | 公共库：异常层次 + `setup_logging` + 文件纯函数 |
| 5 | `tests/test_queyi_common_696.py` | 公共库单测 |
| 6 | `tests/test_tool_manifest_696.py` | manifest 生成器单测 |
| 7 | `docs/ENGINEERING_696.md` | 本报告 |
| 8 | `docs/DATA_GOVERNANCE_696.md` | 数据治理说明（放 `docs/` 而非 `data/`，理由见该文件） |

> `pyproject.toml` / `requirements.txt`：**未改动**（本批新增代码纯标准库，无需增补依赖；
> 遵循"只做最小安全增补"，无增补即不动）。

---

## 1. 做了什么 / 为什么这样做

1. **索引而非搬动**：`tools/` 有 727 个 `.py`，命名规则多样。用**文件名启发式**把脚本归入
   `analysis` / `verification` / `visualization` / `utils` / `batch` 五类，产出机器可读
   `manifest.json` + 人读 `README_696_structure.md`。分类是**索引**，不参与门禁判决。
2. **公共库独立化**：新增 `tools/queyi_common.py`，刻意**不 import** `tools/utils/*`，
   以避免 `sys.path` 耦合，可被任意脚本直接 `import queyi_common`；异常层次 / 日志格式
   与 `tools/utils/` **语义一致、并列不互相依赖**。
3. **确定性**：生成器对文件名与分类键**双重排序**；除 `generated_at` 外逐字段确定，
   单测据此断言"两次生成一致"。

### 1.1 为什么不物理分子目录（核心决策）

**不搬动**。理由（与 693-D1 一致，逐条）：

| 代价 | 具体 |
|---|---|
| 信任根断裂 | `tools/tool_integrity.py` 的哈希面（core/test_config/supply_chain/ruler 四节）以**字面文件名**引用脚本，移动 ⇒ 全部失配 ⇒ 判定入口 `enforce()` fail-loud 拒跑 |
| 门禁/CI 变红 | `.github/workflows/ci.yml`、`tools/prepush_check.py`、`tools/cppbible.py` 的 `quality_gates`、`pyproject.toml` 的 `quality_gates`、`tests/conftest.py` 均以字面路径 `tools/xxx.py` 调用 |
| 回归成本 | 727 脚本逐个改 import + 回归，且失败模式**静默** |
| 收益 | 仅目录更好看 |

**结论**：结构整理以索引/清单/文档落地，**不移动文件**。

---

## 2. 质量门禁结果（命令与输出原样）

### 2.1 ruff（`ruff==0.16.5`）

```bash
$ .venv/Scripts/ruff.exe check tools/queyi_common.py tools/gen_tool_manifest_696.py \
      tests/test_queyi_common_696.py tests/test_tool_manifest_696.py
All checks passed!
（exit 0）
```

### 2.2 mypy（`mypy 2.3.1`）

```bash
$ .venv/Scripts/mypy.exe tools/queyi_common.py tools/gen_tool_manifest_696.py
Success: no issues found in 2 source files
（exit 0）

$ .venv/Scripts/mypy.exe tests/test_queyi_common_696.py tests/test_tool_manifest_696.py
tests\test_tool_manifest_696.py:22: error: Cannot find implementation or library stub for
    module named "gen_tool_manifest_696"  [import-not-found]
tests\test_queyi_common_696.py:27: error: Cannot find implementation or library stub for
    module named "queyi_common"  [import-not-found]
Found 2 errors in 2 files (checked 2 source files)
（exit 1）
```

**说明（不是缺陷，是口径）**：本仓 CI 用 `mypy tools/`（**不检查 `tests/`**，见
`.github/workflows/ci.yml:76`）；`tests/` 下的脚本靠 `tests/conftest.py` 注入 `tools/`
到 `sys.path` 才能 import。mypy 不读 conftest，故单独检查测试文件时需显式给出搜索路径：

```bash
$ MYPYPATH=tools .venv/Scripts/mypy.exe tests/test_queyi_common_696.py tests/test_tool_manifest_696.py
Success: no issues found in 2 source files
（exit 0）
```

⇒ **`tools/*.py` 用仓库口径（`mypy <file>`）双绿；`tests/*.py` 用 `MYPYPATH=tools` 双绿。**

### 2.3 pytest

```bash
$ .venv/Scripts/python.exe -m pytest tests/test_queyi_common_696.py tests/test_tool_manifest_696.py -q
........................                                                 [100%]
（exit 0；墙钟 2m15s，含仓库 conftest 收集开销）
```

* **通过 24 / 失败 0**（`test_queyi_common_696.py` 16 例 + `test_tool_manifest_696.py` 8 例）。

### 2.4 覆盖率

**环境无 `pytest-cov`，也无 `coverage` 模块**（均已实测确认未安装），故**未用工具实测**。
对 `tools/queyi_common.py` 做**人工分支清点**：

* 已覆盖分支：异常层次（4 类继承 + 基类兜捕 + `__str__` 有/无 hint）、
  `_coerce_level`（int / 合法字符串 / 非法字符串三路）、`setup_logging`（幂等 + 多级）、
  `read_json`（正常 / 缺文件 / 非法 JSON / 顶层非对象四路）、
  `sha256_file`（已知向量 / 空文件 / 缺文件三路）、`atomic_write_text`（往返 / 覆盖写 / 无残骸）。
* **未覆盖分支**：`atomic_write_text` 的 `except BaseException` 清理分支、`__main__` 自检块。
* 人工估算行覆盖 **≈85%**（**这是估算，非工具实测**）⇒ 满足 ≥60% 目标。

---

## 3. 性能分析（实测）

### 3.1 方法

* 候选脚本先做 **import 墙钟**实测（独立解释器，`time.perf_counter()`，仓库外临时脚本）；
* 对**只读**门禁做**真实运行**墙钟实测（bash `time`，`>/dev/null`）。
* **安全约束**：只跑 `--check` / 只读命令；凡默认写盘者**不跑**（见 §3.4）。

### 3.2 import 墙钟（全部候选，实测）

`import` 耗时全部 **< 0.16s**，前三：`mutation_fuzz` 0.157s、`benchmark_676l_analysis` 0.153s、
`teach_card_656` 0.110s。⇒ **导入不是瓶颈**，故改测真实运行。

### 3.3 最慢脚本（真实运行，实测秒数）

| 脚本（命令） | 实测耗时 | 主要瓶颈 | 是否优化 |
|---|---:|---|---|
| `exempt_audit.py --check` | **31.84 s** | 逐块调用 `g++ -std=c++23 -O0 -fsyntax-only` 重编 58 条豁免（subprocess + 真实编译） | 否（见下） |
| `tool_integrity.py --check` | **28.29 s** | `merkle_integrity.check_all()` 对目录树逐文件 sha256（含 Merkle 根重建） | 否（见下） |
| `gen_metrics.py --check` | **2.56 s** | 扫描 `Book/` 147 章做统计 | 否 |

对照（同批实测）：`consistency_check.py` 1.39s、`terminology_normalize.py --check` 1.90s、
`crossref_audit.py` 1.03s、其余 `--check` 门禁均 < 1s。

### 3.4 优化决策：**只报告，不优化**

判断为**高风险，不做优化**，理由：

1. `exempt_audit` 的耗时**就是真实编译**（`g++ -fsyntax-only` 58 次）——这是它存在的意义，
   加缓存 = 用旧结论冒充新编译结果，会**静默放过内容漂移**（它正是抓 DRIFT 的门禁）。
2. `tool_integrity` 的耗时是**对真实字节算 sha256**——缓存跨调用结果会**掩盖文件被改动**，
   与"信任根完整性校验"的目的直接冲突（`tool_integrity.py` 自身也在 ruler 哈希面内）。
3. 故**未做任何 `lru_cache` 等优化**（无前后对比可给）。这是**刻意**的：优化动作本身
   不能削弱门禁的判别力。

### 3.5 未测项

* `verify_data_integrity.py`：**未测**——它默认写 `data/693_data_integrity.json`（源码
  `verify_data_integrity.py:201`），为避免触碰 `data/` **未运行**。
* 需要编译器/网络/长跑的门禁（`compile_all.py`、`compile_gate.py`、`atom_evidence_replay.py`
  等）：**未测**（超出本批范围且耗时长）。

---

## 4. ⚠ 需要主 Agent 处置的越界（诚实披露）

在执行性能实测时，我运行了 `tools/exempt_audit.py --check`（当时未察觉它在 `--check` 下
**仍会重写**默认报告 `tools/exempt_audit_report.json`）。**该文件是受跟踪文件**
（已用 `.git/index` 字节串核对：index 中含 `exempt_audit_report` 路径），其
`Birth=2026-07-19`、`Modify=2026-10-09 08:40` ⇒ **被我覆盖**。

* 该报告**不含时间戳字段**（字段仅 `gcc/gcc_version/platform/flags/baseline/total/by_status/results`），
  内容**确定性**；若本机 gcc 与 `Book/` 自上次提交起未变，重新生成的字节**应与提交版一致**
  （即 `git status` 应显示无 diff）——但**我无法用 git 核实**（本批禁跑 git）。
* **建议**：主 Agent 在提交前跑 `git status -- tools/exempt_audit_report.json`；
  若显示 ` M`，用 `git restore tools/exempt_audit_report.json` 还原（我未、也不能自行还原）。
* 影响面：**仅此一个文件**。定向扫描（`mtime > 08:30`，排除忽略目录）确认我**没有**改动
  其他受跟踪文件；`build/asm_evidence_report.json`（`verify_asm_evidence.py` 的默认输出）落在
  **被忽略的 `build/`** 下，无影响。
* 另注：同工作区有**并发批次 697** 与另一 696 子线在写 `tools/`、`data/`、`docs/`（非本线文件），
  故 `tools/*.py` 计数会漂移；本批单测已用**运行时 glob** 断言，不写死数字。

---

## 5. 数据治理决策

**放 `docs/DATA_GOVERNANCE_696.md`，不放 `data/`**。理由（命中任务书触发条件）：
`tools/` 中确有会**枚举 `data/` 目录**的校验/机制——`gen_693_manifest.py`（`data_manifest`）、
`auto_executor_640.py`（`os.listdir(data)`）、`number_consistency_scan_671g.py`
（`data/*核查*.md`、`data/*报告*.md` glob）。按任务书"存在此类校验即不放 `data/`"的保守口径，
改放 `docs/`。详见 `docs/DATA_GOVERNANCE_696.md`（含 data 目录说明与回溯 changelog）。

---

## 6. 未完成 / 不确定项

1. `tools/exempt_audit_report.json` 越界覆盖（见 §4）——**未自行还原**（禁跑 git），交主 Agent。
2. 覆盖率**无工具实测**（环境无 `pytest-cov`/`coverage`），仅人工估算 ≈85%。
3. 依赖编译器/网络的门禁未做性能实测（见 §3.5）。
4. `tools/manifest.json` 是**生成时快照**（count=727），并发批次会使其滞后；重生成即可刷新。
