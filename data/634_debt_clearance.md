# 634 化债报告（A 线）

| 任务 | 动作 | 结果 |
|---|---|---|
| A1 | 根级 conftest 会话级写保护 | pytest 后 data/ 净 0 改动 ✅ |
| A2 | 79 老工具补 --check | 79/79 加载即校验通过 |
| A3 | 16 处真脆弱断言转动态基线 | 单一基线 data/634_soft_baseline.json |
| C1 | 4 卡 12 prop 补 signed_by | 自身免疫率 14.3%→0% |
| C2 | 快照更新 + .pytest_tmp | 5/5 快照绿；.pytest_tmp 已 gitignore |
| D1 | mypy 注解 | mypy tools/ 0 errors |
