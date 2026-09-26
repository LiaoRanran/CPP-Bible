# 643 阶段0 · 两阶段 pytest 纪律固化

> 依据：`pyproject.toml:151-173`（为什么不用 `-n auto` 跑全部）+ `tests/conftest.py:18-46`（快慢标记的**语义**口径）。

## 一、权威命令（两阶段）

```bash
# fast：纯逻辑，并行安全
pytest -m "not slow" -n auto      # 参考 85–90s（589 任务4b 实测）
# slow：真编译/replay/poison，共享真实仓可变状态 ⇒ 必须串行
pytest -m slow -n0                # 参考 ≈644.8s（589 任务4b 实测）
```

## 二、标记从哪来（不是装饰器扫出来的）

- `tests/conftest.py:159-171` 的 `pytest_collection_modifyitems` **按模块名**打标：
  `SLOW_MODULES`（20 个）+ `SERIAL_EXTRA`（11 个）⇒ 共 **31 个模块**自动带 `slow`；
- 其余模块自动带 `fast`；未加 `-m` 时标记不影响结果（默认跑全部）。
- ⇒ **新增测试文件默认落在 fast 组**；若新测试真调编译器/真跑 replay，**必须**把模块名加进 `tests/conftest.py` 的 `SLOW_MODULES`（否则会并行假红）。

## 三、为什么不能把 `-n auto` 写进 addopts（已实测，别再试）

1. ~14 个模块共享**真实仓库可变状态**（`build/.replay_lock`、`Examples/atoms/*.asm` 删-重建-比 sha-还原）⇒ 并发下 `replay 锁被占用超时` 假红；
2. `--dist loadgroup` + `xdist_group("serial")` 在 xdist 3.8 **实测无效**（调度器读不到 item 上的 marker）；
3. 故改为**按标记切两阶段**：不依赖分组，**构造上安全**。

## 四、计数口径（643 起）

- **以 junit XML 为准**：`pytest ... --junitxml=data/643_pytest_<phase>.xml`，计数与失败 node id 都从 XML 读（`counts_from_junit` / `failed_node_ids`）；
- **为什么**：642 D2 实测「终端末尾汇总行未被后台捕获」（文件止于 `snapshot report summary`），当时只能靠进度行推导；XML 是机器可读的权威口径，免受捕获/编码问题影响；
- 每阶段另存原始输出 `data/643_pytest_<phase>.txt`（保留给人工查证）。

## 五、墙钟预算（告警线，非契约）

| 阶段 | 命令 | 参考墙钟 | 告警线 |
|---|---|---|---|
| fast | `-m "not slow" -n auto` | 85–90s（589 任务4b 实测） | 120s |
| slow | `-m slow -n0` | ≈644.8s（589 任务4b 实测） | 900s |

> 超告警线**不失败**，只登记 —— 墙钟随机器负载/核数漂移（pyproject:170 已声明"参考值、非契约"）。

## 六、最近一次实测

| 阶段 | tests | passed | failures | errors | skipped | 秒 | 判定 |
|---|---|---|---|---|---|---|---|
| fast | 2833 | 2806 | 17 | 0 | 10 | 368.6 | ❌ 红 |
| slow | — | — | — | — | — | — | **未跑** |

## 诚实登记

1. 墙钟是**参考值非契约**（同机同核数下近似可复现，负载变化即漂移）；
2. `-n auto` 的 worker 数取决于本机核数 ⇒ **同一命令在不同机器上不同墙钟**；
3. 本模块**不改** `pyproject.toml` 的 `addopts`（保持别人的串行默认），两阶段只在本模块与 `run_643_gate` 里显式指定；
4. junit XML 是 pytest 官方产物，但其 `tests/failures/errors/skipped` 口径与终端汇总行**在 `-n auto` 下可能因 worker 崩溃而略异**（本批未遇到，仅登记）。
5. **并发写入污染（本批实测的重大情境）**：643 执行期间检测到**另一批次（644）在同一工作区写入**（`_auto/inbox/644.md` 11:18 入队；`tools/*_644.py` 于 11:25–11:42 连续落盘；644 的 pytest 进程实测在跑）。后果：表里"最近一次实测"的**部分红与 643 无关** —— 实测 mypy 报`tools/evidence_conflict_644.py` 的 `arg-type`、ruff 报`tests/test_evidence_card_link_644.py` 的 `F401`，都是**644 的半成品文件**。⇒ **静态检查类红（mypy/ruff/integrity/门禁自检）不得计入本模块的"并行安全"判定**；本模块的并行安全结论建立在**第一轮 fast（早于 644 开工）**与其**串行复跑取证**上（`_auto/_643_parallel_reds.json`）。
6. **证据新鲜度闸门（真实缺陷的修法）**：pytest 在收集期崩溃/`pytest.exit()` 时**不写 junit**，若直接读路径就会拿到**上一轮陈旧 XML**（本批实测：第四轮打印的失败清单与第三轮**逐字相同**，一度误判"`-m` 过滤失效"）。修法：跑前删除 XML + 跑后校验存在性，缺失则 `evidence_valid=False` 且**不报计数**。
7. **node id 必须含 `.py`（真实缺陷的修法）**：junit 的 `classname` 是点号模块名，转成 pytest 选例路径时漏 `.py` 会让 `pytest <id>` 报`file or directory not found` 而**静默 0 例**（本批实测：一次"串行全绿"的取证其实跑了 0 个用例）。
