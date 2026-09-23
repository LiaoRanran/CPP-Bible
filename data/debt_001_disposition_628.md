# 628 A4 · DEBT-001 到期处置记录

## 登记（625）

- 来源：625 A3 / 验收报告遗留项——`test_s1_s6::test_clean_ledger_passes`
  因债务票据 **DEBT-001 已到期未清（due=2026-09-20）⇒ 停线**。
- 定位（628 任务0）：`tests/test_s1_s6.py` `_tk()` fixture **硬编码**
  `"opened": "2026-09-10", "due": "2026-09-20"`。

## 性质判定

- `DEBT-001` 在**真实治理台账中不存在数据文件**——它只是 debt_ledger 测试的 fixture
  票据。到期的是 **fixture 日期**，不是任何真实治理债务。
- 因此"到期处置"的正确形式是：让 fixture 日期**动态化**（测逻辑而非测日期），
  与 625 A3 对 581 豁免计数动态化同一模式。

## 处置（628）

- `_tk()` 默认值改为 `opened=今日-10` / `due=今日+30`（`datetime.date.today()` 滚动）。
- blocking 场景（expired/over-90-days/agent-owner/ratio）仍用固定过去日期——
  它们测的是停线逻辑，与"今天"无关，不受日期漂移影响。
- 复跑 `tests/test_s1_s6.py` 全绿（含 `test_clean_ledger_passes`）。

## 结论

- **DEBT-001：closed（fixture 动态化，等效清算；真实台账无该债务实体）**。
- 若未来治理台账出现真实 DEBT-001 实体，其续期/关闭仍需人决（债务 owner 为人）。
