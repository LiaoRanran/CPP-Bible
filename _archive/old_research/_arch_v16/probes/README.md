# probes/ — 600 手搓实验索引

> 全部纯标准库、只读探针；只读扫仓库 tools/ data/ atoms/ misconceptions/，输出本目录下的调研产出（非仓库正式文件）。

## probe_supply_chain.py
- **验证理论**：方向 1（in-toto 风格链式溯源）+ 方向 4（Merkle 树 inclusion/consistency）+ 方向 5（链路绑定篡改检测）。
- **做法**：
  - 读真实文件哈希：`tools/` CORE(5)+TEST_CONFIG(2)、`data/overturned_events.jsonl`、部分 `atoms/**`/`misconceptions/**`。
  - 建 5 步链 `write_cards→gate_validate→replay_verify→poison_test→human_review`，每步 link 含 materials/products/command/functionary(git HEAD)/timestamp/模拟签名。
  - 验链：签名有效 + 链路绑定（step N materials ⊇ step N-1 products）+ 工具哈希与磁盘一致。
  - 篡改检测：把 write_cards 某 product 改假值 → 重验应失败。
  - Merkle：7 工具哈希 + 10 atoms 样例 → RFC6962 树；inclusion proof + 验证；改一叶 → 根变、包含证明失败；一致性（追加一叶，前缀根一致）。
- **实测结果**（`report.json`）：
  - functionary(git HEAD) = `2af99a31…`；author = `LiaoRanran`
  - chain_steps = [write_cards, gate_validate, replay_verify, poison_test, human_review]
  - chain_verify_ok = **true**；chain_tamper_detected = **true**（断链路/改产品被检出）
  - merkle_root = `35ad36b10e796852939d5ea67c853a7cc533a1e00a231cbb7a841d255d87f73f`；merkle_height = 5
  - merkle_inclusion_ok = **true**；merkle_tamper_detected = **true**；merkle_consistency_ok = **true**
- **诚实说明**：`sim_sign` 为 git HEAD 模拟签名，**非密码学签名**；RFC6962 简洁 consistency proof 留 W 档；纯演示可行性。
- **运行**：`python _arch_v16/probes/probe_supply_chain.py`（需仓库 `.venv` 或系统 Python3，无第三方依赖）。
- **产出文件**：`layout.json`、`links/*.json`、`merkle_report.json`、`report.json`。

## 未做但可做的探针（留给后续）
- 真实 .ots 时间戳（需联网 + ots CLI，违反只读纪律"不装依赖"，留阶段 3）。
- RFC6962 简洁 consistency proof（O(log n) 哈希证明，非前缀重算），留 W 档。
- 运行时规则集指纹（封堵攻击 1 进程内篡改），留阶段 4。
