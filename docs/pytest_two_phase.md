# 工程纪律 · 全量 pytest 两阶段跑法

> 643 任务 0.2 固化。依据 `pyproject.toml:151-173` 与 `tests/conftest.py`。
> 数据型报告（含最近一次实测数字）：`data/643_pytest_two_phase.md`。

## 规矩

1. **默认跑两阶段，不跑全量串行**（全量串行 ≈ 35–40 min，两阶段 ≈ 6 min + 11 min）：

   ```bash
   pytest -m "not slow" -n auto    # fast：纯逻辑，并行安全
   pytest -m slow -n0              # slow：真编译/replay/poison，共享真实仓状态 ⇒ 串行
   ```

2. **计数以 junit XML 为准**：`--junitxml=data/643_pytest_<phase>.xml`；
   不依赖终端汇总行（642 实测它会丢），也不靠进度行推导（脆弱）。
   统一入口：`python tools/pytest_two_phase_643.py --fast|--slow|--both`。
3. **新增测试默认落 fast 组**；若新测试**真调编译器 / 真跑 replay / 真跑 poison /
   读真实仓可变状态 / 起子进程读同一批状态**，**必须**把模块名加进
   `tests/conftest.py` 的 `SLOW_MODULES`（编译类）或 `SERIAL_EXTRA`（读真实状态类）。
4. **不要**把 `-n auto` 写进 `addopts`（`pyproject.toml:156-172` 已实测：
   并发下假红；xdist 3.8 的 `--dist loadgroup` 分组**不生效**）。
5. **写入 `data/` 的测试日志必须净化**（`--color=no` + `sanitize()`）：
   仓库有"`data/` 无控制字符"门禁，ANSI ESC 会直接打破它。

## 改标记后必须做的事

`tests/conftest.py` 与 `pyproject.toml` 是 **`tool_integrity` 的 `test_config` 受控文件**
（`tools/.tool_checksums` 的 `# test_config` 节）⇒ 改完必须重钉：

```bash
python tools/tool_integrity.py --update    # 重钉 core + test_config + supply_chain + ruler
python tests/../tools/tool_integrity.py --check   # 四项全 OK 才算完
```

否则 `pytest_configure` 的测试器配置完整性自检会**拒绝开跑**（591 任务3）。

## 已知代价（如实登记）

- 墙钟是**参考值非契约**（随核数/负载漂移）；
- 串行组随批次增长（643 实测：31 → 77 个模块）；串行组越大，`slow` 阶段越长；
- `SLOW_MODULES`/`SERIAL_EXTRA` 是**经验累积清单，不声称完备**：
  并行跑再现新红时按实测增量登记（清单里逐批留了取证说明）。
