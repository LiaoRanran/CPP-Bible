# ADR-0005：S4 黄金非回归锁底座 = 抽象 `l2_state` 的快照-漂移三件套

- 状态：**已接受**（2026-09-10，G1 附加调研，用户 G0 答复第 2 条附加指令）
- 决策人：架构师提议，随 G1 交付报人确认

## 背景（已查证事实）

调研两个既有快照机制，得到两种成熟模式：

**模式 A（快照-漂移）——`tools/l2_state.py`**：
- `measure() -> dict`（重新实测）→ `load_state()/save_state()`（schema 版本化 + git head 留痕，字节写）→ `cmd_sync`（写入快照）/ `cmd_check`（比对：**恶化即 exit 1、改善提示重跑 sync、新增记账**）。
- 同款已复制到 `star_h2_audit.py`（H2 数 + 扩展膨胀基线）。两处独立演化证明该模式可复用。

**模式 B（豁免-重跑）——`tools/exempt_audit.py`**：
- 豁免清单（预期失败白名单）vs 当前干净重跑结果逐条核对：豁免块现在 PASS 了→清单冗余；非豁免块 FAIL 了→新增回归；另有 `expected_fail(reason, platform)` 处理平台差异（POSIX 块在 Linux 预期 PASS）。

## 决策

- **S4（黄金非回归锁）复用模式 A**：质量分数快照 = `measure()` 的推广（原子完备度/五剖面达标数等），快照文件带 schema + commit，`check` 拦"任何指标下降"；改阈值须过全部历史 golden 回归即"快照重放"。
- **S5（豁免=带息债务）复用模式 B**：豁免 ticket 清单 vs 实际状态核对（到期未清→红、问题消失→清单冗余即债清），`expected_fail` 的平台差异处理原样继承。
- G3 实现时把模式 A 抽成通用底座（约 80 行：`measure/load/save/check` 四函数 + schema 约定），`l2_state`/`star_h2_audit`/S4 三处共用，**不重写第三份**。

## 候选与否决

**候选 B：S4 直接用 git tag / CI artifact 存 golden。**
否决：golden 快照需要进库可 diff、可被门禁工具读（CI artifact 拉取受网络与权限影响，本地 pre-push 不可用）；git tag 无法承载结构化字段（分数、阈值、生效范围）。

## 后果

- 正面：S4/S5 零新概念，审查者只需理解一种快照格式；三处共用底座后修 bug 一处生效。
- 负面：`l2_state` 与 `star_h2_audit` 现有两份相似代码在抽象前仍各自维护（抽象动作本身排进 G3，不在 G1 动——避免本轮碰既有门禁工具）。
- 约束：底座抽象必须**字节写 + schema 版本化 + commit 留痕**三件套齐全（MEMORY 铁律：文本模式写回会制造行尾伪 diff）。
