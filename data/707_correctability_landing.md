# 707 Task C — 可纠错边界落地（698-B 定理 T6）

- 日期：2026-10-09
- 科研依据：**698-B 定理 T6（可纠错边界）**：可纠正 ⟺ 漂移只作用于**后处理层**；获取层漂移**必须重测**。
- 实测残留误差（698-B）：asan **30.04%** / ubsan **21.38%** / tsan **21.73%**；结构性恒 unknown 列残留 **0**。
- 红线：detect_calls = 0；只读冻结矩阵。

## 1. 落地做了什么

| 文件 | 改动 | 科研依据标注 |
|------|------|--------------|
| `tools/check_drift_correctability.py`（**新**） | 按 T6 对漂移分类：**获取层**（资产可用性/逐资产裁决变化）⇒ `must_retest=True`；**后处理层**（记账/聚合/标签）⇒ `correctable=True`。支持 `--case 692-e1e2` 与 `--matrices A B` | 文件头「科研依据（698-B 定理 T6）」+ doc 字段 `research_basis` |
| `Scripts/verify_environment.sh`（改） | 新增 `ACQ_GAP` 标志（sanitizer 不可用 / `-Wunsequenced` 缺失时置 1）+ **T6 可纠错边界警告块**：检测到获取层缺口 ⇒ 提示「不可事后纠正，必须重测」 | 警告块注释标注「707-C / 698-B 定理 T6」并给出残留误差数字 |

## 2. 验证

**工具**（`--case 692-e1e2`，环境门控撤除 = E1 6 资产 → E2 3 资产）：
```
获取层资产=['asan', 'tsan', 'ubsan']  结构资产=['compile-time', 'wunsequenced']
层=acquisition（获取层）  correctable=False  must_retest=True
动作：必须重测（re-measure）：原始矩阵无此测量，事后校正不可靠
T6 断言（环境门控撤除 ⇒ asan/ubsan/tsan 必须重测）= True
```
⇒ 与 T6 一致：撤除的 `{asan,ubsan,tsan}` 是**获取层**资产（E2 根本无法测量）⇒ **必须重测**；`wunsequenced`/`compile-time` 是**结构性**资产（两环境同等缺实现）⇒ 不算获取层漂移，属可纠正的结构缺口（残留 0）。

**复现脚本**（WSL `bash Scripts/verify_environment.sh --report`，本机 MinGW 缺 sanitizer）：
```
-- 707-C / 698-B T6：可纠错边界 --
  WARN 检测到【获取层能力缺口】：缺失资产/工具 ⇒ 按 698-B 定理 T6，此漂移【不可事后纠正】，
       必须【重测】（re-measure），不要靠事后校正；详见 tools/check_drift_correctability.py
```
`bash -n` 语法检查通过；`ruff check tools/check_drift_correctability.py` 通过。

## 3. 诚实边界

- 工具是**分类器/护栏**，不执行任何重测；只把「可纠正 vs 必须重测」判据固化，防止有人对获取层漂移做**不可靠的事后校正**。
- 残留误差 30.04% / 21.38% / 21.73% / 结构列 0 为 **698-B 已实测值**，在本工具中作为**参考常量**登记（不重算、不新实测）。
- `--matrices` 模式按「逐资产裁决是否变化」判获取层；若两环境的**资产集合不同**（如 692 的 6 vs 3），建议用 `--case 692-e1e2` 的显式剖面。

## 4. 产物

- `tools/check_drift_correctability.py`（新）
- `Scripts/verify_environment.sh`（+14 行 T6 警告）
- `data/707_correctability.json`（验证产物）
- 本报告
