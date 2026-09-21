# 03 · 时间轴与 bitemporal 再评估（Q3）

> 任务疑问：N1 把卡的 git 提交时间降级为 `asserted_at_approx`（B 级）。rebase/amend/squash/cherry-pick/浅克隆/跨机时钟/文件移动 下这个时间会怎么撒谎？有没有只读办法检测"时间轴被改写"？**关键反问：git 本身就是 append-only 的 Merkle 历史，582"否掉 bitemporal 引擎（XTDB/Datomic）"是否把"重型时序数据库"和"时序语义"混为一谈？**

---

## 1. git 作为时序源：能力 vs 盲区（代码实测）

- `prop_asof._git_commit_iso`（L48–57）取 `git log -1 --format=%cI -- <card_path>`，字段名硬约束为 `asserted_at_approx_from_card_commit`（L170），文档明确标 **B 级证据**（L188–189："git 历史可被 rebase/amend 重写，本字段不是权威断言时间"）。→ 已诚实标注，这是**正确**的。

### 各操作下 `%cI` 撒谎情况（只读推演，未跑写盘命令）

| 操作 | 对 `%cI`（committer date）影响 | 是否撒谎 | 检测手段（只读） |
|---|---|---|---|
| `rebase` | 新 commit 产生新 `%cI`（可设为 now 或保留原值） | 是（时间被改写） | parent 链非线性、`git log --graph` 异常；reflog |
| `commit --amend` | 改写作者/日期，生成新 hash | 是 | reflog（本地）、object store 旧对象（GC 前） |
| `squash` | 多提交合并，时间取合并点 | 是（丢失中间时间） | parent 链、reflog |
| `cherry-pick` | 可保留原日期或取新日期 | 视参数 | 同上 |
| 浅克隆 `--depth` | 无历史 | 是（根本取不到） | 无法本地检测（信息缺失） |
| 跨机时钟偏差 | 提交时时钟本身不准 | 是（源头错） | 无（需 NTP/第三方） |
| 文件移动 `git mv` + `--follow` | 历史保留 | 否 | `git log --follow` |

### 只读检测"时间轴被改写"的可行性
- **reflog**：记录 HEAD/分支的每次更新，**本地**且默认 90 天；`git reflog expire --all && git gc` 可抹掉 → 攻击者清得掉。
- **parent 链 / commit-graph**：可发现非线性、缺失父节点。
- **`git fsck` / `git cat-file` dangling**：改写后旧对象在 GC 前仍在 object store，可见为 dangling。
- **诚实结论**：只读检测**有**，但在"单用户 + 可清 reflog + 可 gc"前提下**不可靠**——和 Q1 同根问题。

---

## 2. 关键反问：582 是否把"引擎"和"语义"混为一谈？

**是的，混为一谈了。** 拆开看：

- **"重型时序数据库（XTDB/Datomic）"** 作为*具体实现*：单用户本地确实不需要引入一个独立的 bitemporal 数据库——它增依赖、增攻击面、增维护成本，且本仓已有 git 这个天然的 append-only Merkle 历史。**否掉这个引擎是对的（N 档）。**
- **"四轴时序语义"（断言时间 / 验证者版本 / 推翻事件 / 引用锚）** 作为*能力*：这**不该否**。而且它在本仓约束下可**低成本从 git 派生**，无需新引擎：

| 四轴 | 本仓已有派生源（只读） | 是否需新引擎 |
|---|---|---|
| ① 断言时间 | 卡的 `git log -1 %cI`（B 级，`prop_asof`） | 否 |
| ② 验证者版本 | 卡面 `verified_by_oracle` 比对 `data/oracle_registry.json`（`prop_asof._card_oracle` L104–121） | 否 |
| ③ 推翻事件 | `data/overturned_events.jsonl`（可缺，`metrics_collector.read_overturned_events` L377） | 否 |
| ④ 引用锚 | `data/propositions.db` 的 `anchor_source` 列 | 否 |

→ **`prop_asof.py` 已经把四轴做出来了**，只是诚实标了"断言时间是 B 级"。这恰恰证明：语义要保留，引擎要否掉。

---

## 3. 修正后的否决意见

- **该否的**：引入 XTDB/Datomic 等重型 bitemporal 引擎作为依赖（单用户无必要，增攻击面）。
- **不该否的**：四轴时序语义本身；应保留并强化 `prop_asof` 的四轴视图。
- **N 档补强（不引入新引擎）**：
  1. 在四轴视图里把"断言时间 = B 级"的标注**固化进任何下游报告**，禁止把 `asserted_at_approx` 当 A 级权威时间。
  2. 可选加一条**只读**提示：跑 `git reflog`/`git fsck` 看当前仓库是否有"近期被改写"迹象，仅作观察（warn），不阻断。
  3. 推翻事件流（`overturned_events.jsonl`）已只追加、系统绝不自动产生推翻（`metrics_collector.log_overturned` 注释 L406–416）——这是四轴的第三轴，保持。

---

## 4. 诚实边界

> 四轴中"断言时间"是 **B 级**（可被 rebase/amend 改），这**不是缺陷，是诚实标注**。真正需要 A 级权威时间时（如抗抵赖审计），必须等第三方可信时间戳（见 Q4/Q6 的 W 档）——单用户无密钥下不该假装拥有。

**外部来源**：git 作为 Merkle 历史是常识级事实；XTDB bitemporality 官方文档 [ES11]。 Thompson trusting-trust [ES1] 的"历史可被改写"同理适用于"把信任寄托在可被 rebase 的 git 时间上"。
