# 623 E2 · 高复杂度带 block 级规则（3-5 条）

> 规则定义文件：`data/gate_rules_high_complexity_block_623.yaml`
> 背景：622 E2 Horizon + 623 E1 攻击面分析 → 高复杂度带仅 warn 级兜底，无 block 级结构规则。

---

## 一、补的 4 条 block 级规则

| 新规则 ID | 提升自（既有 warn 规则） | scope | 填补的漏洞 |
|---|---|---|---|
| `EV-SERVES-EXIST-HC` | `EV-SERVES-EXIST` | evidence | serves 指向虚无目标（M9）由 warn 升 block |
| `ATOM-REL-TARGET-HC` | `ATOM-REL-TARGET` | atom | relations 悬空目标由 warn 升 block |
| `ATOM-REL-UNKNOWN-HC` | `ATOM-REL-UNKNOWN` | atom | 未知 relations 类型由 warn 升 block |
| `CARD-PATH-NOT-CANONICAL-HC` | `CARD-PATH-NOT-CANONICAL` | atom | 非规范路径由 warn 升 block |

## 二、为何是这 4 条

623 E1 复现 622 E2：高复杂度带触发的 warn 级规则为 `EV-SERVES-EXIST` / `ATOM-REL-TARGET` /
`ATOM-REL-UNKNOWN` / `CARD-PATH-NOT-CANONICAL`（外加 `ATOM-VERIFY-REASON`）。
其中前 4 条对应**跨卡引用 / 关系结构**类攻击面——这正是高复杂度 mutation（H4 跨卡一致性攻击）的主战场。
把这 4 条在其高复杂度上下文提升为 block，等于给"高复杂度带的软腹部"装上硬拦截。

## 三、铁律合规说明

- **不碰 gate_engine.py 逻辑**：本批只产出"规则定义文件"（yaml），不修改任何 CORE_TOOLS 检测逻辑。
- **接线留人审/624**：把 yaml 中的 4 条 `register(Rule(...))` 接入 `gate_engine.py` 的 `register()`
  属 CORE_TOOLS 改动（铁律禁止 623 做），故**本批不接线**；yaml 已给出每条的 `bind`（建议复用的既有 check 函数），
  接线时无需新写检测逻辑，仅"提升 severity"即可，工作量极小、风险可控。
- **未运行 tool_integrity --update**：yaml 为新增数据文件，不在 RULER_TOOLS/CORE_TOOLS 保护清单内，
  无需重钉；若人审决定接线，应在同 commit 对 gate_engine.py 改动后运行 `--update`。

## 四、预期效果（接线后）

高复杂度带（complexity ≥60）的 M9/H4 类攻击将从"warn 记债、0% 被拦"变为"block 阻断"，
直接消灭 622 E2 Horizon 曲线指出的"高复杂度带检测率归零"现象，使 VFDR 在高复杂度带也保持高拦截率。

## 五、局限性声明

1. yaml 为规则定义，**未实际接入 gate**，故 623 收工门禁不会因本文件变红/变绿；效果为预期值，需接线后验证。
2. "高复杂度上下文"的判定（如 complexity 阈值）需接线时在 gate_engine.py 内实现，本文件仅声明意图。
3. 仅覆盖 4 条最相关的 warn→block 提升；其余高复杂度 warn 规则（如 ATOM-VERIFY-REASON）可按同法扩展。
