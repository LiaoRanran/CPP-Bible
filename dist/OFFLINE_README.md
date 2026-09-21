# 阙疑 QueYi Protocol · 桌面离线包（617 G1）

> 本目录为离线桌面整合包。仓库本身即自包含（git 克隆后无需网络），本包提供一键启动器与离线说明。

## 一、一键启动
- 双击 `queyi_offline_launcher.bat`（Windows）。
- 它做两件事：
  1. **度量自检**：运行 `tools/snapshot_manifest.py`（只读，由 git/filesystem 直取计数，写 `data/SNAPSHOT_MANIFEST_617.json` 并打印）。
  2. **项目说明**：打印 `README.md` 头部 30 行。
- 不自动跑全量 `--check` 门禁（避免长时占用）；如需完整验证，按 README 门禁命令手动执行。

## 二、离线可复算性
- 所有验证数字与计数均可离线复算：计数来自 git/filesystem（无需网络）；冻结验证基线（`data/616_baseline.md` / SNAPSHOT_MANIFEST）为历史快照。
- 统计诚实性：置信序列/estimand 工具（`tools/confidence_sequence.py`、`tools/escape_rate_estimand.py`）纯标准库，离线可跑。

## 三、目录说明
- `queyi_offline_launcher.bat`：启动器。
- `OFFLINE_README.md`：本文件。

## 四、与 617 其他任务的关系
- 计数源唯一化见 `data/SNAPSHOT_MANIFEST_617.json` 与 `data/project_key_numbers_quickref_20260921_v7.md`（D4/G2）。
- 验证独立性分级见 `tools/verify_independence_level.py`（B1）；estimand 三层见 `tools/escape_rate_estimand.py`（A1）。
