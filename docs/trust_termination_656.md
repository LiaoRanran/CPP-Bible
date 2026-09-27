# 信任终止声明（Trust Termination）· 656 A

> 任务书要求："信任终止声明——最底层是『作者本人』+ 比特币时间戳 + 外部锚"。
> 本文只写**真实成立**的东西：写到哪一层算哪一层，**不多写一个字的强度**。

## 一、什么叫"信任终止"

任何验证链条都不能无限递归——"谁来验证验证者？"这个问题必须在某处**停止**，否则永远在同一台机
器上自证。真正诚实的做法不是"假装没有终点"，而是**明确写出终点是什么**、以及**终点断了会怎样**。

本仓的链条是四层，**逐层把信任放在更不可伪造的东西上**：

```
L3  人              作者本人（commit signoff / PR review / 裁决记录）——不可再向下归约
                        ▲
L2  外部锚          OTS 时间戳 → 比特币工作量证明（656 A 本批新增）
                        ▲
L1  代码 / 口径     tools/.tool_checksums：5 个核心工具 + 2 个测试配置 + 6 个信任根数据 + 22 条判决尺子
                        ▲
L0  内容            data/supply_chain/merkle_roots.json：atoms / evidence / Examples / Book / mutation_baselines 的目录级 Merkle 根
```

- **L0→L1**：`tools/tool_integrity.py --check` 同时校验 4 节；`--check-merkle` 比对目录实际内容重算出的根。
- **L1→L2**：`tools/ots_anchor_656.py --analyze` 判定 OTS 文件是否真的覆盖
  `merkle_roots.json` 当前内容的 sha256（**挂错对象即刻判 `invalid`**，见 §三）。
- **L2→L3**：OTS 证明"该 digest 在某一时刻之前已存在"；**是谁把它放上去**由人的 commit/PR 负责。

## 二、为什么选比特币时间戳做外部锚

OTS（OpenTimestamps）把 digest 提交给公开的**聚合日历**，日历把它折进一棵 Merkle 树，再把根写进一笔
比特币交易。于是该 digest 获得一条由**累积工作量**支撑的时间下界：要伪造它等于重做那段比特币 PoW。

它提供的是**三件具体的事**（不更多）：

1. **时间下界**：证明这个 digest 在区块高度 N 之前已存在（不是"现在补生成"的）。
2. **不可伪造的公共记录**：验证方不需要信任本仓、不需要信任服务器，只要有比特币区块头即可。
3. **多中心冗余**：本批同时提交到 4 个独立日历（`alice` / `bob` / `catallaxy` / `finney`），
   任一存活即可核验，全部失效才断。

## 三、当前状态（诚实：**pending，不是已入块**）

| 项 | 值 |
|---|---|
| 锚定对象 | `data/supply_chain/merkle_roots.json`（1081 字节） |
| 其 sha256 | `c09ee380e15ba46e20d4e1d44c4f808f15d8c32ffe484c0f1c82860824aa83cd` |
| OTS 文件 | `data/supply_chain/merkle_roots.json.ots`（786 字节） |
| verdict | **`pending`** —— 已进日历 Merkle 树，**尚未**拿到比特币区块头证明 |
| attestation | 4 条 `PendingAttestation`（4 个日历各一条） |
| 升级命令 | `python tools/ots_anchor_656.py --upgrade`（日历打包进区块后才会成功；本次当场尝试 ⇒ 0 条升级、`not_ready`） |

**状态机不许越级叫**：
`missing → pending → bitcoin_anchored`；另有 `invalid`（文件无效）、`unverified`（环境无官方实现，只能验文件头）、
`downgraded_json`（只有待上链登记表）。

⚠️ **本批没有做到"已入块"**：日历通常数小时内把 commitment 打包进比特币交易。**这一步不该由本仓证明**
（否则要引入"信任某个 API 的返回值"），留给后续批次 `--upgrade` 并回填区块高度/TXID。

## 四、前情：为什么本批要重做，而不是沿用旧的 `.ots`

| 事实 | 取证 |
|---|---|
| 旧文件由 **613 E1 自制的生成器**产出（`tools/ots_anchor_613.py`），从未 submit | `git log --follow data/supply_chain/merkle_roots.json.ots`；`data/ots_anchor_613.md` 自述"本工具不 submit 日历"、"比特币证明段是占位零" |
| 它**不能被官方实现解析**：magic 与 `DetachedTimestampFile.HEADER_MAGIC` 不符 | `ots_anchor_656 --analyze` 对旧文件 ⇒ `verdict=invalid`；官方库 `deserialize` 直接抛错 |
| 613 文档称"可被任何 OTS 客户端解析" —— **该断言实测不成立** | 同上（这正是"自写自验"的典型形状：`generate(x)` 与 `verify(x)` 出自同一套手写格式） |
| 它挂载的 digest 已**过期**（对应 613 时代的台账内容） | 旧文件内 digest `7ab71c2f…` ≠ 当前 `c09ee380…` |
| 处置 | `git mv` 归档为 `merkle_roots.json.ots.homemade-613to652`（保留证据、不删历史），用**官方实现**产出真锚 |

> 结论：旧文件不是"恶意造假"——613 已如实写了"不得当作时间戳证明"。真正的问题是**它顶着 `.ots` 扩展名**，
> 而 `.ots` 在生态里的语义就是"OTS 证明"。把它留在信任根旁边，等于让最外层锚点挂着一个"看着像锚点的假凭证"。

## 五、怎么自己复核（不信任本仓的任何人）

```bash
# 1) 本机判定：到哪一级 / 覆盖的 digest 是否等于目标文件当前内容
python tools/ots_anchor_656.py --analyze

# 2) 官方 CLI（独立实现，与本仓工具互为交叉验证）
ots info data/supply_chain/merkle_roots.json.ots
ots verify data/supply_chain/merkle_roots.json.ots -f data/supply_chain/merkle_roots.json

# 3) 等入块后再回来拉比特币区块头证明（联网）
python tools/ots_anchor_656.py --upgrade
#    ⇒ verdict 变 bitcoin_anchored；`ots info` 会显示区块高度与交易
```

没有任何 `ots` CLI 也没关系：`--analyze` 用的是同一份官方 Python 实现（`opentimestamps` 0.4.5）。
**两者都缺**时只能验文件头 ⇒ 判 `unverified`（**明确不说"已锚"**）。

## 六、它做不到什么（这节是本文的诚实边界）

1. **不证明"正确"，只证明"此前已存在"**：错误的 Merkle 根同样可以被锚；判"对不对"是 L0/L1 的事。
2. **pending 不等于时间证据提交完成**：只有拿到 Bitcoin attestation 才算拿到**公共时间**；
   在此之前，日历的 PendingAttestation 证明的是"我交给了它"，不是"它进了块"。
3. **依赖日历的存活**：4 个日历若全部消失且未越迁实，链断 ⇒ 需要在有 attestation 后把**区块高度 + TXID 写回本文**，
   使任何人可以只靠比特币主网（不看日历）复核。
4. **不保护端到端**：OTS 锚的是 `merkle_roots.json` 这一个文件；到"某一行 C++ 代码没被动过"之间，
   依赖 `tool_integrity` 的 4 节与 Merkle 树的完整性——任一层被同权限者篡改，OTS 都不会叫。

## 七、交人 / 后续

| # | 事项 | 触发条件 |
|---|---|---|
| 1 | 执行 `--upgrade` 并把**区块高度 / TXID** 回填本文 §三 | 日历打包后（通常数小时） |
| 2 | 每次 **`merkle_roots.json` 变化**（受控目录内容变更）都要重新 stamp + 重钉 | 内容侧任何变更 |
| 3 | 定期跑 `--analyze`：发现 `invalid` ⇒ 立即停线调查 | 每批收工门禁已含 |
| 4 | 关闭被删除的历史 item：`<target>.ots.homemade-613to652` 何时可删 | 由人裁决（本批只归档，保留证据） |

---
_656 A · G9 总闸门产物。相关工具 `tools/ots_anchor_656.py`；回归锁 `tests/test_ots_anchor_656.py`；
报告 `data/656_ots_anchor_report.{md,json}`。_
