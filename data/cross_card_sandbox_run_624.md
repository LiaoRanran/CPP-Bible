# 624 A2 · 60 条跨卡攻击沙箱实跑（真实 gate 判决）

> 工具：`tools/cross_card_attack_624.py::run_batch`（多卡 apply → 跑 gate → 还原所有卡）
> 输入：`data/cross_card_sandbox_run_624.json`（A1 生成的 60 条）
> 方式：**真跑 gate**（`gate_engine.py --run --json`），多卡 findings 取并集做 diff
> 环境：Windows 本地（.venv），总耗时 **167.0s**

---

## 一、真实判决结果（60 条）

| 判决 | 条数 | 占比 |
|---|---|---|
| **blocked** | **47** | 78.3% |
| **detected_nonblock**（warn/advice 级） | **13** | 21.7% |
| neutral | 0 | 0% |
| **escaped（严格口径）** | **0** | 0% |
| infra_error | 0 | 0% |

**新逃逸发现：0 条。** 跨卡攻击在真实 gate 下无一逃逸（无基线 finding 消失）。

按策略：
| 策略 | blocked | detected_nonblock |
|---|---|---|
| X1 悬空引用 | 15 | 0 |
| X2 循环引用 | 13 | 2 |
| X3 矛盾引用 | 4 | 11 |
| X4 孤儿引用 | 15 | 0 |

## 二、实际触达规则（核心压力指标）

| 口径 | 622 A2 | 623 累计 | **624 A2 本轮** | **624 累计** |
|---|---|---|---|---|
| 触达规则数 | 9/63 | 26/63 | **13**（本轮） | **28/63（44.4%）** |
| 其中 block | — | 21 | 5 | 23 |
| 其中 warn | — | 5 | 8 | — |

- 本轮触达 13 条：ATOM-ID-FORMAT · ATOM-ID-UNIQUE · ATOM-PREREQ-READABLE · **ATOM-REL-CONFLICT** ·
  ATOM-REL-DAG · ATOM-REL-TARGET · ATOM-REL-UNKNOWN · ATOM-VERIFY-REASON · **EV-ARTIFACT-FILE-EXISTS** ·
  EV-ARTIFACT-VERSION-MATCH · EV-ASSERT-SYMBOL-MAPPED · EV-FM-YAML-HARDENING · EV-SERVES-EXIST。
- **相对 623 的新规则仅 2 条**：`ATOM-REL-CONFLICT`（block，623 盲区）· `EV-ARTIFACT-FILE-EXISTS`（block，623 盲区）。
- **622/623 盲区突破**：X3 矛盾引用成功触达 `ATOM-REL-CONFLICT`（623 从未触达）；X4 孤儿 artifact 触达 `EV-ARTIFACT-FILE-EXISTS`。

> **目标对照**：624 A2 目标「>15 条新规则、累计 >40/63」。**实测新 2 条、累计 28/63 —— 未达标**（见 A3 根因）。

## 三、与 A1 预测对比（预测准确率）

| 预测规则 | 是否触达 |
|---|---|
| ATOM-REL-TARGET | ✅ |
| ATOM-REL-DAG | ✅ |
| ATOM-REL-CONFLICT | ✅ |
| ATOM-ID-UNIQUE | ✅ |
| EV-SERVES-EXIST | ✅ |
| EV-ARTIFACT-FILE-EXISTS | ✅ |
| ATOM-MISCONCEPTION-REF | ❌ |

- **预测命中 6/7（85.7%）**。
- 未命中：`ATOM-MISCONCEPTION-REF` —— X4 把原子 `misconceptions` 改为不存在的 `MIS-NOPE-999`，但该规则未触发 ⇒ 说明 `check_misconception_ref` 的触发条件或字段名与预期不同（A3 分析）。

## 四、局限性声明

1. **触达 13 条中 11 条与 623 已触达重叠**：跨卡攻击主要激活的是既有引用类规则（ATOM-REL-TARGET/DAG、EV-SERVES-EXIST、ATOM-ID-UNIQUE），真正新增仅 2 条 ⇒ **跨卡并未如预期大幅突破天花板**。
2. **gate_engine 无专门「跨卡一致性」规则族**：X1–X4 只能借既有规则的引用检查触发，覆盖面受规则设计限制。
3. **判决只含 gate（规则层）**：未含 replay 复算层。
4. **样本 60 条**，分策略后 X3 仅 15 条。
