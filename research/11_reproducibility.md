# 11 · 复现性（Reproducibility）

- **环境锁**：编译器版本 gcc 13.1.0 / clang 22.1.8（见于 baseline.json / boundary provenance）；
  Node 18.20.8（前端冒烟）；Python 3.11（CI DCO/质量门禁）。
- **OTS 锚**：每条证据 SHA256 锚到开放时间戳服务（provenance 字段），别人可重算。
- **对账可离线**：status_reconciler_658 仅依赖 git + 文件系统，无第三方服务。
- **数据冻结**：D2 holdout reveal 后写 .revealed，旧态保留不可改；D4 独立集版本化。
- **一键复现**：`python tools/status_reconciler_658.py --check` 复核元状态；
  `python tools/holdout_658.py --reveal` 跑盲化（不可逆）；各 fixture 工具 `--rate` 复算检测率。
- **随机数固定**：B3 随机基线用固定 seed 记录，保证可复跑。
