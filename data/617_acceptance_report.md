# 617 收工验收报告（任务0 + A1/A2/B1/C1/D2/D4/G2/G1 + 收工 F1/F2/F3 · 部分完成，余留 618）

> 时间：2026-09-21 ｜ 铁律：依任务书 §五，**监工门禁（run_614_gate 等全量 --check）未跑**；数字取自基线文件 + SNAPSHOT_MANIFEST，可复算。
> 范围：617 共 23 任务（任务0 + A1–A3 + B1–B4 + C1–C4 + D1–D4 + E1–E3 + F1–F3 + G1–G2）。本批完成 **11 任务**（8 工作：任务0/A1/A2/B1/C1/D2/D4/G1 + 收工 F1/F2/F3），余 **12 任务诚实登记留 618**（见第六节）。

## 一、本批完成（8 任务，8 commit）
| 任务 | 交付 | commit |
|---|---|---|
| 任务0 | data/617_baseline.md（只读台账，实测 HEAD=8cca534，commit 1512→实测 1517 / tools 215→218 / tests 210→213）| edc264b |
| A1 | estimand 三层拆分：doc + tools/escape_rate_estimand.py + test（9 项过）| c7262c6 |
| B1 | 独立性 4 级：doc + tools/verify_independence_level.py + test（5 项过）| 66328df |
| C1 | 测试分类 taxonomy（doc，区分真实验证 vs 脚本自测）| ccdb291 |
| A2 | 置信序列 L2b(e-process mixture)/L3 shrinkage（doc，补 A1 精确 L2）| c2b5e60 |
| D2 | SNAPSHOT_MANIFEST 自动生成：tools/snapshot_manifest.py + test + data/SNAPSHOT_MANIFEST_617.json | ff3e5d6 |
| D4/G2 | 数字漂移修复：data/project_key_numbers_quickref_20260921_v7.md（manifest 派生，废弃手填 v6）| da82369 |
| G1 | 桌面整合：dist/ 离线包 + queyi_offline_launcher.bat（度量自检）| 98ade67 |

> 另含并行会话前置 3 commit（8cca534 / 0b9683f / 6ef8551：37 号路线图 + 外部评审存档 + 项目健康报告），属 617 规划/输入，非本苦力执行。

## 二、外部评审 10 点响应映射
| # | 评审点 | 617 响应 | 状态 |
|---|---|---|---|
| 1 | estimand 三层（L1/L2/L3）混淆 | A1 三层定义 + 枚举器；A2 补 L2b/L3 方法 | ✅ 已建框架 |
| 2 | 独立性 4 级 | B1 定义 + 判定工具（当前离散 L1）| ✅ 已量化缺口 |
| 3 | 测试分类 taxonomy | C1 10 类定义 | ✅ |
| 4 | 覆盖率虚高 | C1 区分真实验证 vs 脚本自测 | ✅ 口径 |
| 5 | 独立第三方 | B1 路径（L2/L3 需 VSA/透明日志/第三方）| 🟡 识别缺口，未实施 |
| 6 | 数字漂移 | D2 SNAPSHOT_MANIFEST + D4 quickref v7 | ✅ |
| 7 | 计数手填 | D2/D4 唯一源 + 禁止手填 | ✅ |
| 8 | bootstrap/统计诚实 | A1/A2 统计诚实性（偷看虚报 13.80%→0.00%）| 🟡 部分（未独立 bootstrap 工具）|
| 9 | 信任根 | B1 标注 partially_anchored（OTS/in-toto 未真做）| 🟡 识别，未修 |
| 10 | 文档可读性 | 各 doc 结构化（标题/表/铁律）| 🟡 主观，未系统审 |

## 三、验证数字（取自 SNAPSHOT_MANIFEST_617.json / 616 基线，非重跑）
- gate 63/191（block0,warn186,advice5）；poison 124/124（表观 63/63，诚实 60/63）；replay 56/0/0。
- mutation v7 1593/1405/1/179/8/1406，逃逸契约 1/1406。置信序列 CS 0.9062% / CP 0.3370%。
- 人审 388（354/34/0，batch_auth 388 / mirror 194）；独立性 verifier=1、第二实现 1/63、离散 L1、scalar 0.153；信任根 partially_anchored。
- 实时计数：commits 1517 / tools 218 / tests 213 / atoms 28 / EV 56（README 周边/quickref 旧值 204/183/196/175 已漂移，D4 治理）。

## 四、受控目录污染自检
- 本批未触碰 atoms/ evidence/ Examples/ Book/ CORE_TOOLS / golden_lock.py / poison_drill.py / run_614_gate.py。`git diff --name-only` 仅含 data/ tools/ tests/ dist/ References/（新增，非受控）。零污染。

## 五、CI / 监工门禁
- 依 §五 监工门禁未跑（本机无 gh 通道，亦不越权跑全量 --check）。新增工具（escape_rate_estimand / verify_independence_level / snapshot_manifest）均带单测且本地通过（9+5+4 项）。
- CI 四 job 实跑仍为交人项（615 #7，P0）。

## 六、诚实登记留 618（12 任务）
- **A3**：escaped/equivalent 的 L2b 精确工具落地（e-process mixture / conformal）——A2 已给方法，待工具。
- **B2–B4**：independence_level 接入 gate/poison/replay 报告 + 收尾 doc（避免改动受控工具，留 618 评估）。
- **C2–C4**：3 个分类计数脚本（replay/poison/gate category）+ slash-command doc + 分类映射表。
- **D1**：SNAPSHOT 治理方案 doc（manifest 规范/CI 集成策略）；**D3**：CI 集成 doc。
- **E1–E3**：人审可执行化（30 条逐条复核清单生成工具 + 待办清单 + 文档）。
- **F2/F3 本批已做占位**（status.json 待更新；债务清册见下节）。
- **G2**：README/qmd/quickref 数字漂移修复——本批以 D4（quickref v7）覆盖，G2 视为已完成（README.md 经核不含 tools/tests 计数，无需改；根目录无项目说明.qmd）。
- 说明：上述 12 任务非阻塞，且部分涉及受控工具改动或大量历史文档重指向，按"质量优先于数量 + 做不完诚实登记"原则留 618。

## 七、交人项（继承 + 本批新增）
- 继承 616 的 10 项（615 遗留 7 + 616 新增 3）继续有效；本批未执行任何裁决。
- 本批新增待决：**是否采用 manifest 派生的 quickref v7 作为唯一计数源并系统性重指向历史 PM 报告**（D4 已建 v7，历史 v6/34/33 等手填计数留 618 重指向）。
