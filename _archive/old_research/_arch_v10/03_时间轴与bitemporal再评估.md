# 585 · 03 时间轴与 bitemporal 再评估（Q3）

> 核心问题：把 `git 时间` 当 asserted 轴是否够强？582 否掉 bitemporal 引擎是否被 585 推翻？答案：**推翻的是"否决的理由"，不是"否决的结论方向"**——该否的是"重型引擎"，不是"时序语义"。

## Q3 · git 时间轴能当 asserted 轴吗？怎么才算"时间轴被改写"？

### 3.1 git 的拓扑事实（标准 git 行为，非本仓特例）
- git 历史是 **append-only Merkle DAG**：每个 commit 哈希含 parent 哈希，改任一历史 commit 会**级联改变其后所有 commit 的哈希**。这是 git 的天然防篡改结构（与区块链同源思路）。
- 但**可改写命令**：`rebase` / `amend` / `squash` / `cherry-pick -x` 会**重写历史**，使旧 commit 哈希"消失"，新哈希接上。本地 `commit --amend` 不报错。
- **git author/committer date 是自申报的**：`git config user.name/email` 任意配置；`commit --date` 可倒填；`GIT_AUTHOR_DATE/GIT_COMMITTER_DATE` 环境变量可伪造。所以"author time"本质是 B 级证据（自我声明），不是独立时间戳。

### 3.2 "时间轴被改写"如何被只读侦测（前提：有外部锚点）
| 改写动作 | 本地只读可见性 | 必需的外部锚 |
|---|---|---|
| `amend` | **reflog** 有旧 hash（直到 `gc` 过期，默认 90 天）；`fsck --lost-found` 可捞 dangling commit | 若无外部备份，决心够大的攻击者删 reflog + gc 后可抹除 |
| `rebase/squash` | 同上；parent 链断裂可被 commit-graph 审计发现 | 远端"forced update 拒绝"或带外 head hash 副本 |
| `cherry-pick` | 新 commit 无原 parent 链，可被"孤儿 commit"检测 | 带外全量镜像 |
| 倒填 date | **不可侦测**（date 本就是自申报） | 第三方时间戳（见下） |

→ **结论**：git 的"不可篡改"只在**你持有一个 git 自己算不出的外部锚点**（远端/带外副本/第三方时间戳）时才成立。单用户本地无外部锚时，**时间轴可被同一人改写且本地无痕**——所以 git 时间在本仓约束下是 **B 级证据**，可降级，这也正是 583/584 设计里给 `asserted_at_approx_from_card_commit` 加 `_approx` 后缀、报告标注 B 级的正确性所在。

### 3.3 对 582 否决的修正
- 582 的"否掉 bitemporal"——**其结论（不引入重型时序引擎）本预审同意**：在单用户本地，重型 bitemporal 引擎（XTDB/Datomic）是 overkill，且它的"不可篡改"同样退化为"同一 git 根"，没有真增信。
- 但 582 的**理由可能混淆了"重型引擎"与"时序语义"**。git 本身已廉价提供**四轴时间线**：
  1. commit time（提交时刻）
  2. author time（作者自申报）
  3. reflog（本地操作序列，可审计 amend/rebase）
  4. parent chain / commit-graph（拓扑可溯）
- **该做的是**：从这四轴**廉价派生** asserted 轴与"是否改写"哨兵（如：发布快照时记 `head_hash` 到不可变介质；CI 比对 parent chain 连续性），**而不是**推翻"我们确实需要时序语义"。
- **诚实边界**：这四条轴全由 git 根供养，最终信任仍退化为"对同一 git 根的访问权"——这正是 Thompson/DDC 警告的单点。要真防改写需**第三方时间戳/公证**（W，等条件）。所以 585 推翻的是 582 的"时序语义无用"论据，保留其"不建重型引擎"结论。

### 3.4 判定与建议
- **N（现在能做）**：发布 `metrics_collector` 报告/正式数据集时，附 `git head_hash + 四轴时间戳 + "本快照生成时 parent chain 连续"声明`；`asserted_at` 一律标 B 级、后缀 `_approx`。
- **W（该等）**：真不可篡改时间戳——等第三方 notary / Sigstore 式透明日志（单用户离线不可得，见 `01` ⑥⑧ 环）。
- **不推荐**：为了"时间轴"引入 XTDB/Datomic 等重型引擎（582 否得对）。

> 参考：[Thompson 1984][一手论文] 同根单点警告 · [Wheeler DCC][一手论文] 异源验证思路 · bitemporal 概念（[二手·一方称] Martin Fowler bitemporal pattern；重型引擎 XTDB https://docs.xtdb.com/ 与本仓约束不符，故不采纳）。
