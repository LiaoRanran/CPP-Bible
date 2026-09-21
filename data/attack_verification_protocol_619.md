# 619 A4 · 攻击-验证迭代协议（设计文档，不执行）

> 配套：A2 攻击者（`adversarial_attacker_619.py`）· A3 VFDR 状态机（`vfdr_619.py`）
> **本文件只设计协议，不实际运行迭代**（619 §五/§六：不生成新 mutation、不跑监工门禁、不碰受控目录）。
> 迭代的增益/收敛曲线均**未实测**，留 620 落地。

## 一、三个角色

| 角色 | 实现 | 职责 |
|---|---|---|
| **攻击方** | A2 排序（`adversarial_attacker_619.py`）+ 本协议的「施加 mutation」步骤 | 按 A1 目标函数挑最该打的 mutation，施加到沙箱副本 |
| **验证方** | `gate_engine.py` + `atom_evidence_replay.py`（隔离环境） | 对沙箱副本判定 `verdict`（blocked / escaped / n_a） |
| **裁判** | A3 VFDR 状态机 + **真实门禁 CI**（非攻击方自评） | 把「新逃逸」登记为 `VFDR-OPEN`；把「修复后重判通过」作为 `VERIFY_PASS → CLOSED` 的唯一合法闸门 |

> 关键分离：**攻击方不得自判修复通过**。A2 只能排序 + 施改；`VERIFY_PASS` 必须由真实门禁（与 §六
> 一致，本批不跑，但协议规定其归属）确认，杜绝「自己打自己评」的循环论证。

## 二、一轮迭代（R₀ → R₁…）

```
1. 攻击方：从 A2 的 ranked Top-k（建议 k=20）取本轮目标 mutation 集
2. 攻击方：在【沙箱副本】上施加 mutation（M1–M7 任一类），【绝不】写受控目录 atoms/evidence/Examples/Book
3. 验证方：对沙箱副本跑 gate + replay（隔离），得到 verdict
4. 若 verdict == escaped 且 not equivalent：
     开 VFDR-OPEN，按 A1 子目标分类：
       rule_blind_spot      → 类别 MATRIX（规则层盲区）
       provenance           → 类别 REDTEAM（溯源/供应链）
       verdict_regime_disc.  → 类别 GOV（口径治理，warn→advice 降级风险）
       evidence_ambiguity   → 类别 PARSE（解析/判别力）
5. 修复方（人/CI）：修 gate 规则或修卡 → 触发 VFDR START_FIX → FIX_SHIPPED
6. 验证方（真实门禁）：重跑，VERIFY_PASS → CLOSED；VERIFY_FAIL → 回 FIXING（重修）
7. 收敛：逃逸率契约重算（1/1406 为下限，不得劣化）
```

## 三、终止条件（协议收敛判据）

达成任一即停（或交由人决策继续）：

1. **稳定性**：连续 `N=3` 轮无新增「真逃逸」（escaped 且非等效）。
2. **Top20 消化**：A2 `ranked` 的 Top20 全部转为 `n_a`（无可变形点）或被「已知规则」blocked（命中规则已登记，非盲区）。
3. **置信收敛**：A1 目标函数加权 Top1 的 `composite` 与 CS 逃逸率上界在连续 3 轮变化 < 1%（说明攻击-验证已进入边际收益递减区）。
4. **否决**：攻击方穷举完 `ranked` 1406 条仍零新增真逃逸。

## 四、不变量（协议必须遵守，违反即停）

- **逃逸率契约不劣化**：迭代后真逃逸数 ≥ 基线 1（`1/1406` 是下限，不是上限）；A2 的 `check_contract()` 每轮断言。
- **受控目录零污染**：mutation 只施加在沙箱副本；`atoms/ evidence/ Examples/ Book/` 与 CORE_TOOLS 不改（619 §六）。
- **门禁真实性**：`VERIFY_PASS` 来自真实门禁，不接受攻击方/修复方自报。
- **等效不重排**：`equivalent`（8 条）仍剔出 `ranked`，迭代不把它们当作真逃逸反复打。

## 五、与 A3 的状态机衔接

| 协议事件 | VFDR 事件 |
|---|---|
| 步骤 4 发现新逃逸 | `TRIAGE`（OPEN→TRIAGED） |
| 步骤 5 修复提交 | `START_FIX` → `FIX_SHIPPED`（TRIAGED→FIXING→VERIFYING） |
| 步骤 6 真实门禁通过 | `VERIFY_PASS`（VERIFYING→CLOSED） |
| 步骤 6 失败 | `VERIFY_FAIL`（回 FIXING） |
| 回归（已在 CLOSED 的漏洞复发） | `REOPEN`（CLOSED→FIXING） |

## 六、诚实登记（留 620）

1. 协议未执行任何一轮；上述步骤、终止条件、不变量是**设计**，未用真实数据校准。
2. A1 目标函数的加权排序在 W1 下把真逃逸排到第 57 位（见 A1 §五），迭代优先级需先拍板权重（W2 校准）再跑，否则前 20 轮多在打「被 EV-FM-REQUIRED 薄拦截」的无害项。
3. 迭代增益（每轮真逃逸收敛速度）需要 A1 子目标与 VFDR 类别映射的标定数据，本批未做。
4. 攻击方施加 mutation 需要沙箱机制（当前 `mutation_fuzz` 是**只读基线生成器**，不提供「施加到副本」API）——沙箱封装是 620 前置。
