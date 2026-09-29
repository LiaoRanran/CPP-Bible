# 方向 33：Python 测试工具链（pytest / hypothesis / coverage / mutmut）

> 调研日期：2026-09-29　联网搜索 13 次　WebFetch 3 次（coverage.py 配置页 / 分支页 / mutmut 文档全文）　curl+PDF 提取 1 份原文
> 锚点：阙疑 / queyi（内核 `tools/gate_engine.py` **3826 行**；`tools/` 目录 640 条目 / 595 个 `.py`；67 条判决规则 block 44；452 条判决账本；`data/` 下 30 seeds holdout + 40 条外部 corpus + 15 条缺陷夹具）

## 核心结论

1. **覆盖率口径必须写死在配置里，否则数字不可复现**：coverage.py 的 `[run] branch` **默认是 `False`**，即"不配置就只测语句覆盖"。阙疑若对外报"覆盖率 X%"，必须同时声明 `branch = true`、`precision`、`source`/`omit`、`exclude_lines`/`exclude_also` 与 `fail_under`——这五个字段缺一个，审稿人就无法复算。
2. **覆盖率不能当质量目标，这是 2014 年 ICSE 已被量化的结论**：Inozemtseva & Holmes 用 **31,000 个测试套件 / 5 个系统**证明，"当控制住测试用例数后，覆盖率与有效性只有**低到中等**相关"；Joda Time 上相关性从（不控制规模时的）**0.80–0.85** 掉到**几乎为零**。因此阙疑的评估协议**不应以覆盖率为主要指标**，而应以变异得分 + holdout 检出率为主要指标（与论文 v0.3"主动放弃内部变异率当缺陷检测率"的立场一致）。
3. **mutmut 3 是 Python 侧唯一"配置化程度足够进 CI"的变异工具，但它有两个硬边界**：① `mutate_only_covered_lines` 默认 `false`，不显式打开会浪费大量算力在死代码上；② 它**只支持 pyrefly / mypy 两种类型检查器**做无效变异过滤，**不支持 pyright**。阙疑若想用类型检查器削减变异体，工具链选择被 mutmut 反向约束了。

---

## 精确数字与案例

### 1. coverage.py 的配置面（官方文档 7.16.2 全文提取，全部为默认值）

**配置文件查找顺序**（原文，当 `.coveragerc` 不存在且未指定 `--rcfile`/`COVERAGE_RCFILE` 时）：
1. `.coveragerc.toml` → 2. `setup.cfg` → 3. `tox.ini` → 4. `pyproject.toml`
"使用第一个含 coverage.py 设置的文件，其余不再咨询。"——**这是一个静默陷阱**：如果仓库里同时有 `setup.cfg` 和 `pyproject.toml`，`pyproject.toml` 里的覆盖率配置会被**完全忽略**。
- TOML 支持条件：**Python 3.11+**，或安装 `coverage[toml]` 扩展。
- TOML 段名：`[tool.coverage.run]` / `[tool.coverage.report]`；INI 段名：`[coverage:run]`（setup.cfg/tox.ini）。

**`[run]` 关键项（默认值）**：

| 选项 | 默认 | 说明 |
|---|---|---|
| `branch` | **`False`** | 是否额外测分支覆盖 |
| `source` | 无 | 要测量的包/目录；**若设置则忽略 `include`** |
| `include` / `omit` | 无 | 文件名模式；`[run] omit` 是从**测量**中排除，`[report] omit` 是从**报告**中排除 |
| `data_file` | `".coverage"` | 数据文件名 |
| `parallel` | `False` | 数据文件名附加机器名+PID+随机数（并行/CI 必备） |
| `concurrency` | `"thread"` | 可选 `multiprocessing`/`gevent`/`greenlet`/`eventlet` |
| `core` | 依 Python 版本 | `ctrace`（3.13 前默认）/ `sysmon`（3.12+ 可用，**3.14+ 默认**）/ `pytrace` |
| `relative_files` | `False` | 数据文件存相对路径（跨机器合并必备，5.0+） |
| `source_pkgs` / `source_dirs` | 无 | 消解"包 vs 目录"歧义（5.3+ / 7.8+） |

**`[report]` 关键项（默认值）**：

| 选项 | 默认 | 说明 |
|---|---|---|
| `fail_under` | 无（不启用） | 低于阈值则**退出码 2**；设 `100` 时任何低于 100 都失败，**不论 `precision`** |
| `precision` | **`0`** | 小数位；**若非整数的 `fail_under` 要生效，必须同时调大 `precision`** |
| `show_missing` | `False` | 摘要里显示缺失行号 |
| `skip_covered` / `skip_empty` | `False` / `False` | 不报 100% 文件 / 不报无可执行代码的文件 |
| `exclude_lines` | 含 `pragma: no cover` | **会覆盖默认集**（危险） |
| `exclude_also` | 保留默认 | 7.2.0+ 新增，**推荐用这个** |
| `partial_branches` | 含 `pragma: no branch` | 覆盖默认 |
| `partial_also` | 保留默认 | 7.10.0+ 新增，**推荐** |
| `sort` | `"Name"` | 可选 `Stmts`/`Miss`/`Branch`/`BrPart`/`Cover`，前缀 `-` 降序 |
| `format` | `"text"` | 7.0+ 支持 `markdown` / `total` |

**输出目标默认路径**：`[html] directory = "htmlcov"`；`[xml] output = "coverage.xml"`、`package_depth = 99`；`[json] output = "coverage.json"`、`pretty_print = false`；`[lcov] output = "coverage.lcov"`（6.3+）、`line_checksums = false`（7.6.2+）。

**`[paths]` 跨机器合并**（CI 分片/多平台必备）：把不同绝对路径映射到同一源文件；原文规则——"**第一个值必须是报告机器上真实存在的文件路径**"，其余值可为模式；多组列表按序尝试，**仅当重映射结果存在时才生效**；`combine` 命令才做多文件重映射，报告阶段只在单个数据文件内重映射；可用 `--debug=pathmap` 观察。

### 2. 分支覆盖率的精确语义（为什么语句覆盖会骗人）

**官方《Branch coverage measurement》页给出的定义与机制**：
- 测量时 coverage.py 收集**行号对（pairs of line numbers）**——每次"从某行跳到某行"的转换；再用**静态分析**得到"可能转换"清单；二者相减得到**缺失分支**。
- 报告中的呈现：**缺失分支写成 `源行->目标行`**，HTML 里"部分分支"行标**黄色**，右侧注出未走到的目标行号。
- **分母口径**：文件的覆盖率 = 实际执行数 / 执行机会数，其中"**每一次执行机会既包括文件中的每一行，也包括每一个分支目标**"——这就是为什么开 `branch` 后百分比会掉。

**官方三组最小例子（可直接作为阙疑的"覆盖率口径"教学素材）**：

```python
# 例 A：for 循环
1 items = [1]
2 for x in items:
3     print(x)
4     if x:
5         print("x is true")
6 print("done")
# items 为空 → Missing: 3-5（循环体未执行，但不报缺失分支）
# items = [1] → Missing: 4->2（if 恒真，从未回跳）
```
```python
# 例 B：if/else
1 flag = True
2 if flag:
3     do_true()
4 else:
5     do_false()
# Missing: 2->5（else 从未走；else 本身不是可执行行，故不提及）
```
```python
# 例 C：while
3 while condition:
5     if flag:
6         condition = False
# Missing: 5->3（if 的假分支从未走）
```

**两类"假警报"与对应 pragma**：
- **结构性部分分支**：`while True: ... break` 与 `if 0:` 这类"永不完全退出"的结构，coverage.py **能理解语义、不标记**；但用户自己的"故意部分分支"它无法推断，需 `# pragma: no branch`。
- **生成器表达式**：`next(i in range(1))` 之类可能被报部分分支（生成器未迭代到 `StopIteration`），同样用 `# pragma: no branch`。
- **排除代码会改变分支计数**（原文）："**若条件分支的某个选项被排除，则该条件不会被计为分支**"——例如 `else: # pragma: no cover` 会使整个 `if` **根本不被视为分支**。这条是"刷覆盖率"最常见的无意识手段，必须在论文中声明。

### 3. 覆盖率的效度上限：ICSE 2014 的 31,000 个测试套件

**论文**：Laura Inozemtseva, Reid Holmes, *"Coverage is not strongly correlated with test suite effectiveness"*，**ICSE 2014**，DOI **10.1145/2568225.2568271**（PDF: https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf ，本次已提取全文 11 页）。

- **规模**：为 **5 个系统**（含 JFreeChart、Joda Time、Closure、Apache POI、SQLITE / YAFFS2 一类大型 C 项目）生成了 **31,000 个测试套件**，用 **PIT** 生成变异体（等价变异体被排除）。
- **结论**："**当控制住测试用例数后，覆盖率与有效性只有低到中等相关**"；原文摘要："Our results suggest that coverage, while useful for identifying under-tested parts of a program, **should not be used as a quality target**"。
- **极端案例（原文）**：Joda Time——不控制规模时，覆盖率与有效性的相关性 **0.80–0.85**；**控制规模后掉到"essentially zero"（几乎为零）**。Apache POI 在另一端：不控制规模时用非归一化有效性指标，相关性 **0.94**。
- **另一个数字**：最初考虑的项目中 **58%** 因测试套件不充分而被排除。
- **对阙疑的直接含义**：`gate_engine.py` 3826 行的"代码覆盖率"是**内部工程指标**，不能作为论文的核心证据；核心证据必须是 holdout 检出率（66.7%）、外部 corpus 检出率（43.8%）、缺陷夹具重注入检出（100%）。

### 4. mutmut 3 的完整配置面（官方文档全文提取）

**配置文件**：`setup.cfg` 的 `[mutmut]`，或 `pyproject.toml` 的 `[tool.mutmut]`（TOML 下路径必须写成数组）。

| 配置项 | 默认 | 作用 |
|---|---|---|
| `source_paths` | — | 要变异的源码路径（旧版叫 `paths_to_mutate`，**已改名**） |
| `pytest_add_cli_args_test_selection` | — | 传给 pytest 的测试选择参数（旧版 `tests_dir` **已废弃**） |
| `also_copy` | — | 额外需要复制到变异沙箱的文件/目录（如 `conftest.py`、snapshot 目录） |
| `max_stack_depth` | — | 只在栈深度低于该值时才算"相关测试"；**值越低越快，但存活变异体更多** |
| `only_mutate` / `do_not_mutate` | — | 白/黑名单（glob） |
| `mutate_only_covered_lines` | **`false`** | 只变异被 coverage 判定"被调用"的行；**遵循 `# pragma: no cover` 与 `exclude_lines`/`exclude_also`** |
| `type_check_command` | — | 用类型检查器过滤无效变异体；**仅支持 pyrefly 与 mypy**（需输出 JSON） |
| `do_not_mutate_patterns` | — | 正则列表，匹配行上的表达式全部跳过变异 |
| `process_isolation` | `"fork"` | 或 `"forkserver"` |
| `forkserver_warmup` | `"collect"` | 或 `"import"` / `"none"` |
| `max_forkserver_restarts` | **`3`** | 超过则抛 `ForkServerCrashError` |
| `use_git_change_detection` | `true` | 关掉则回退到内置文件哈希列表（`pyproject.toml`、`setup.cfg`、`setup.py`、`requirements*.txt`、`poetry.lock`、`uv.lock`、`Pipfile*`） |
| `on_dependency_change` | `"warn"` | 或 `"rerun"` / `"ignore"` |
| `timeout_constant` / `timeout_multiplier` | **`1.0` / `15.0`** | 超时公式：**`(原测试耗时 + 1.0) × 15.0` 秒**（官方标注为 unstable config） |

**三个 pragma（禁用变异）**：
- `# pragma: no mutate` —— 单行；
- `# pragma: no mutate block`（或 `: block`）—— 整个缩进块；
- `# pragma: no mutate start` / `# pragma: no mutate end` —— 区间（忽略缩进）。
  **解析错误处理**：孤立 `end`、未闭合 `start`、嵌套开启新上下文，都会抛 **`PragmaParseError`**（含文件名与行号）——这是"配置可校验"的好设计。

**CLI 与工作流**：
```bash
pip install mutmut
mutmut run                       # 默认在 tests/ 或 test/ 目录跑 pytest
mutmut run "my_module*"          # 通配符限定变异体
mutmut run "my_module.my_function*"
mutmut browse                    # 交互式 TUI：r 重跑当前、f 重测函数、m 重测模块
mutmut apply <mutant>            # 把变异体写盘（做人工分析）
mutmut export-cicd-stats         # 导出 CI 统计
mutmut badge --output mutation-score.json   # 转 Shields endpoint JSON
```
- 数据保存在 `mutants/` 目录，**删掉即从头开始**；支持中断续跑（"Remembers work that has been done, so you can work incrementally"，GitHub README）。
- 官方 README 明列 **JUnit XML support**（对应 CI 集成）。
- **重要提示（本次调研发现的坑）**：网上大量中文教程仍在教 mutmut 2 的 `paths_to_mutate` / `tests_dir` / `runner` / `dict_synonyms` / `mutmut results` / `mutmut html`——**这些在 mutmut 3 里已不存在**（文档明确列出）。写稿引用配置时必须核对版本。

### 5. pytest 侧的"最小可复现"配置

pytest 官方配置参考（https://docs.pytest.org/en/stable/reference/customize.html ）推荐优先用 `pyproject.toml`（段名 `[tool.pytest.ini_options]`）、`tox.ini` 或 `setup.cfg`（段名 `[tool:pytest]`）而非 `pytest.ini`。常用字段：
- `testpaths`：限定默认收集目录；
- `addopts`：固定加 `--strict-markers --strict-config -ra`；
- `markers`：注册自定义标记（否则未注册标记会被警告，`--strict-markers` 下会**直接失败**）；
- `filterwarnings = ["error"]`：把警告升级为错误（pytest 文档《How to capture warnings》说明：标记上的过滤器**优先于**命令行与 `filterwarnings` 配置）。

**并行**：`pytest-xdist` 的 `-n auto` 按 CPU 核数起 worker（https://github.com/pytest-dev/pytest-xdist ）；配合 coverage 时必须 `[run] parallel = True` 再 `coverage combine`，否则多 worker 的数据会互相覆盖。

**CI 矩阵**：GitHub Actions 用 `strategy.matrix.python-version` 同时跑多版本（社区教程示例覆盖 3.8–3.11 / 3.10–3.12 等）。

---

## 对阙疑的 3 条具体行动

1. **把覆盖率配置"钉死"成一份可复算文件，并主动声明它只是工程指标**。
   具体：在 `_arch_v46/` 内产出 `33_覆盖率配置稿.md`，给出**完整 `[tool.coverage.*]` 片段**（写进 `pyproject.toml` 的形态）：
   ```toml
   [tool.coverage.run]
   branch = true
   source = ["tools"]
   omit = ["tools/*_bak*.py", "*/__pycache__/*"]
   parallel = true
   relative_files = true
   [tool.coverage.report]
   precision = 2
   show_missing = true
   skip_empty = true
   exclude_also = ["if TYPE_CHECKING:", "raise NotImplementedError", "@overload", "if __name__ == .__main__.:"]
   partial_also = ["if __name__ == .__main__.:"]
   fail_under = 70
   ```
   并在论文的 Evaluation 节**主动写一句**："覆盖率仅作工程指标报告，不作为有效性证据（依据 Inozemtseva & Holmes, ICSE 2014, DOI 10.1145/2568225.2568271）"。**这一句会显著提升审稿人对测量素养的评价**。同时必须在方法节说明 `exclude_also` 排除了哪些行、为什么（因为排除分支会改变分支计数）。

2. **用 mutmut 3 的正确配置替换现有口径，并先做一次"覆盖率引导变异"的对照**。
   具体：`pyproject.toml` 中写
   ```toml
   [tool.mutmut]
   source_paths = ["tools"]
   also_copy = ["data", "conftest.py"]
   mutate_only_covered_lines = true
   do_not_mutate_patterns = ["logger\\.\\w+", "^\\s*#"]
   process_isolation = "forkserver"
   pytest_add_cli_args_test_selection = ["tests/"]
   ```
   **要点**：`mutate_only_covered_lines = true` 是必须开的（默认 false，会把算力浪费在死代码上）；`also_copy` 必须包含 `data/`，否则变异沙箱里读不到 `data/_gate_rules.json` 与 holdout，测试会集体失败并被误判为"killed"。**对照实验**：分别在 `mutate_only_covered_lines = true / false` 下各跑一轮，报告变异体总数、存活数、耗时——**这个 Δ 就是"死代码占比"的量化**，可直接写进论文附录。**产出物**：`33_mutmut对照实验设计.md`（写在 `_arch_v46/`，不改仓库）。

3. **建立"覆盖率 + 变异 + holdout"三口径对照表，作为 Threats to Validity 的实证**。
   具体：一张三列表——
   | 口径 | 数字 | 含义 | 可否当有效性证据 |
   |---|---|---|---|
   | 语句覆盖率 | 待测（`branch = false`） | 执行了多少行 | **否** |
   | 分支覆盖率 | 待测（`branch = true`） | 走过多少分支目标 | **否**（ICSE 2014：控制规模后相关性近零） |
   | 内部变异得分 | core 97.3% / all 81.5%（现有登记） | 测试集杀死变异体比例 | **否**（论文 v0.3 已主动放弃该口径） |
   | holdout 检出率 | **66.7%（10/15 可测）** | 对 30 seeds 中 17 真错的检出 | **是** |
   | 外部 corpus 检出率 | **43.8%**（A 54.2% / B 12.5% / C 0%） | 对 40 条外部样本 | **是** |
   | 缺陷夹具重注入 | **6/6 = 100%**（历史覆盖 12/15 = 80%） | 对 15 条真实缺陷 | **是** |
   这张表的用途：**主动承认前三个口径不是证据**，用后三个支撑主张。**依据**：Inozemtseva & Holmes 的 0.80→~0 案例 + OOPSLA 2025 关于"单测数量占优所以总量上找的 bug 更多"的诚实结论——两者都说明"堆量指标"必然误导。**执行**：这张表直接写进 `research/07_baselines.md` 的对应位置（**注意：零污染约束下只写 `_arch_v46/` 内的建议稿，不直接改 `research/`**）。

---

## 盲区（诚实标注）

1. **阙疑当前实际的覆盖率数字完全未知**：本次调研**未运行任何 coverage/mutmut**（遵守"零污染：不改仓库、不跑 gate/pytest"），因此"语句覆盖率/分支覆盖率"两行是**待测**。`00_仓库扫描.md` 也只统计了工具数量，未给覆盖率。
2. **`tools/` 目录 640 条目 / 595 个 `.py` 中，哪些应纳入 `source` 未定**：595 个 `.py` 里包含大量 `*_<批次号>.py` 的历史快照，纳入覆盖率统计会严重稀释百分比。**具体 `omit` 列表需在仓库侧人工核定**，本文无法给出。
3. **mutmut 3 的版本号与发布时间未核实**：官方文档与 PyPI 页均未标注当前版本号；"mutmut 3 与 mutmut 2 的配置差异"是文档明示的（`paths_to_mutate`/`tests_dir` 在 3 中不存在），但**具体从哪个版本开始变更、变更日志在哪，本次未查到**。
4. **mutmut 的性能数据完全未查到**：`timeout_multiplier = 15.0` 的来历、"fork vs forkserver"的实测差异、与 xdist 的兼容性——**官方文档均无量化数据**，社区博客也未见基准测试。
5. **coverage.py 的 `exclude_lines` "默认正则集"官方未完整列出**：文档只说"含 `pragma: no cover`"，未给出完整默认列表；本文的 `exclude_also` 示例是我按常见实践拟的，**不是官方默认值**。
6. **Inozemtseva & Holmes 论文中"5 个系统"的完整名单未逐字确认**：PDF 文本流中只清晰出现 JFreeChart / Joda Time / Closure / Apache POI 与两个大型 C 项目（SQLITE / YAFFS2）的提及，**"5"这个数字是论文自述（"31,000 test suites for five systems"），但哪五个需再核对**。
7. **未查到**：pytest 官方对 `addopts` 是否应包含 `--strict-markers` 的明确推荐；coverage.py `sysmon` core 相对 `ctrace` 的实测性能对比；GitHub Actions 上跑 mutmut 的真实耗时案例。
8. **本文所有配置片段均为"设计稿"**，未在阙疑仓库中验证过能否跑通（尤其 `also_copy = ["data"]` 是否足够，取决于测试如何加载 `data/` 下的 JSON）。

---

## 来源

1. Coverage.py 官方文档. *Configuration reference*（7.16.2）. https://coverage.readthedocs.io/en/latest/config.html （本次已抓全文：配置查找顺序、`[run]`/`[report]` 全部默认值）
2. Coverage.py 官方文档. *Branch coverage measurement*. https://coverage.readthedocs.io/en/latest/branch.html （本次已抓全文：行号对机制、三组最小例子、`# pragma: no branch`）
3. Coverage.py 官方文档. *Excluding code from coverage.py*. https://coverage.readthedocs.io/en/latest/excluding.html
4. Inozemtseva, L.; Holmes, R. *Coverage is not strongly correlated with test suite effectiveness*. **ICSE 2014**. DOI **10.1145/2568225.2568271**. PDF: https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf （本次已 curl 下载并提取全文 11 页）
5. pytest-cov 官方文档. *Configuration*. https://pytest-cov.readthedocs.io/en/latest/config.html
6. pytest 官方文档. *Configuration*. https://docs.pytest.org/en/stable/reference/customize.html
7. pytest 官方文档. *How to capture warnings*. https://pytest.cn/en/stable/how-to/capture-warnings.html
8. pytest-xdist 官方仓库与文档. https://github.com/pytest-dev/pytest-xdist ；https://pytest-xdist.readthedocs.io/en/latest/
9. mutmut 官方文档. https://mutmut.readthedocs.io/en/latest/index.html （本次已抓全文：全部配置项、pragma、CLI、超时公式）
10. mutmut 官方仓库. https://github.com/boxed/mutmut （JUnit XML support、增量运行）
11. mutmut on PyPI. https://pypi.org/project/mutmut/
12. Hypothesis 官方文档（与方向 32 共用）. https://hypothesis.readthedocs.io/en/latest/tutorial/settings.html
13. Ravi, S.; Coblenz, M. *An Empirical Evaluation of Property-Based Testing in Python*. **OOPSLA 2025**, PACMPL 9(OOPSLA2), Article 412（与方向 32 共用；"单测数量占优"结论出处）
14. GitHub Actions 矩阵测试社区教程. https://rexbytes.com/2026/02/21/github-actions-ci-cd-5-10-matrix-testing/
