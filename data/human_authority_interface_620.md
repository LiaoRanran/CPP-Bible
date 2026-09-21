# 620 C1 · Human Authority 接口定义（雷5）

> 状态：**设计定义，未启用**（是否替换现有人审通道 = 人拍板项，见 §七）
> 配套实现：C2 `tools/authority_log_620.py`（append-only 日志）、C3 `tools/pck_authority_sync_620.py`（与 PCK 集成）

> **来源说明（诚实登记）**：提示词要求「读 37 号路线图雷5节」，但在本仓库内
> （`ROADMAP_v2/v3.md`、`WORKLIST_v4.md`、`docs/`）**未检索到**"雷5 / Human Authority / Authority" 相关章节。
> 因此本接口定义依据 **620 提示词 C1 的规格** + **与现有系统的实际映射**推导，
> 未引用到原始路线图原文。若路线图另有规定，以路线图为准并需回改本文件（留人/621）。

---

## 一、第一原则：Model ≠ Verifier ≠ Authority

| 角色 | 谁能当 | 职责 | 能否自评 |
|---|---|---|---|
| **Model**（生成方） | LLM / 苦力批次 | 产出主张、证据、代码 | ❌ 不能判自己对 |
| **Verifier**（验证方） | `gate_engine`、`atom_evidence_replay` | 机器可判的结构/复算校验 | ❌ 只能判"机器能判的" |
| **Authority**（裁定方） | **人** | 对 Verifier 判不了 / 判不准的部分做终局裁定 | ✅ 唯一终局 |

**核心分离**：Model 产出的东西不能由 Model 自己宣布通过；Verifier 只能给机器判据；
**只有 Authority 能把「机器判据 + 语义/价值判断」合成终局决策**。
⇒ 任何"攻击方自评修复通过"（619 A4 §一 明确禁止）都违反本原则。

---

## 二、四权力定义

| 权力 | 语义 | 对 certificate 的影响 | 可逆性 |
|---|---|---|---|
| **ACCEPT** | 人明确接受该主张 | `human_authority.status → approved` | 可被 OVERRIDE 撤销（追加新决策） |
| **REJECT** | 人明确否决 | `status → rejected` | 可被后续 ACCEPT 覆盖（追加） |
| **OVERRIDE** | 推翻**既有**决策（含机器判决或前人决策） | 追加一条指向 `overrides: <decision_id>` 的新决策 | 只追加，不删改 |
| **ABSTAIN** | 人明确弃权（不表态） | `status → abstain`（**不等于 approved**） | 可撤销 |

**关键约束**：
- **ABSTAIN ≠ ACCEPT**。弃权必须显式记录为弃权，不得静默当作通过。
  （对应 B3 统计中 `conditionally_authorized` / `abstain` 两级当前恒为 0 的现状。）
- **OVERRIDE 必须指名**被推翻的 `decision_id`，否则无法审计"推翻了什么"。
- **撤销只能追加**：不提供 update / delete 语义（与 C2 日志的 append-only 一致）。

---

## 三、Authority 接口（Python 风格规格，本批不落地为 .py）

```python
class Authority(Protocol):
    """终局裁定方接口。实现者必须是人（或人显式授权的代理），不得是 Model/Verifier。"""

    def decide(self, target: Target, power: Power, reason: str,
               overrides: str | None = None) -> AuthorityDecision:
        """施加一次权力。
        - power in {ACCEPT, REJECT, OVERRIDE, ABSTAIN}
        - reason 必填（空 reason 的决策无效）
        - power == OVERRIDE 时 overrides 必须指向既有 decision_id
        """

    def list_decisions(self, target: Target) -> list[AuthorityDecision]:
        """列出某目标上的全部决策（按时间序，含被推翻的）。"""

    def current_status(self, target: Target) -> AuthorityStatus:
        """当前生效状态（取最后一条非 ABSTAIN 决策；全 ABSTAIN 则为 abstain）。"""

    def verify_chain(self) -> bool:
        """校验日志哈希链完整性（C2 实现）。篡改 ⇒ False。"""
```

> 说明：本批 **不实现** `Authority` 类（避免造出一个"机器 Authority"），
> 只定义契约；C2 实现的是**日志**（记录人已做出的决策），不是"自动决策器"。

---

## 四、AuthorityDecision 数据结构（YAML）

```yaml
decision_id: "dec-000001"
target:
  type: certificate            # certificate | atom_card | evidence_card | rule
  id: "ATOM-CONC-FENCE-001"
power: ACCEPT                  # ACCEPT | REJECT | OVERRIDE | ABSTAIN
reviewer: "human:<实名>"       # 必填；"human:" 后必须有实名（619 poison P13 教训）
reason: "已逐条核对 4 条符号断言与 .out 留痕"
overrides: null                # power=OVERRIDE 时必填，指向被推翻的 decision_id
review_method: item_by_item    # item_by_item | batch_authorization
evidence_refs:
  - "evidence/conc/EV-CONC-001.md"
decided_at: "2026-09-21T15:30:00+00:00"
prev_hash: "sha256:..."        # 链上前一条决策的哈希
self_hash: "sha256:..."        # 本条决策的哈希（C2 计算）
```

**必填校验**（C2 实现）：`reviewer`（含实名）、`reason`、`power`、`target.id`、`decided_at`。
空名签收（`human:` 后无实名）视为**无效**——沿用 619 poison P13 的教训。

---

## 五、与现有系统的映射

| 现有机制 | 对应权力 | 粒度 | 缺口 |
|---|---|---|---|
| 人审通道（`data/human_attack_edge_annotations.jsonl` 等） | ≈ **ACCEPT / REJECT** | 较细（逐条标注） | 无 OVERRIDE/ABSTAIN；无防篡改链 |
| `golden_lock`（golden accept） | ≈ **ACCEPT** | **太粗**（整批/整个 golden） | 粒度粗到无法表达"某张卡被否决" |
| PCK `human_authority.status` | 结果的**投影** | 单卡 | 当前 schema 仅 `pending/approved/rejected`，**缺 abstain / conditionally_authorized** |
| `batch_authorization`（388 条） | 批量 ACCEPT | 批量 | 非逐条独立审阅（615 诚实审计结论） |

⇒ **Authority 接口的价值**：把上述分散机制统一到**同一套可审计决策语义**下。

---

## 六、No single principal 原则

> **任何单一主体不得同时拥有「产出」「验证」「裁定」中的两项以上。**

| 主体 | 产出 | 验证 | 裁定 |
|---|---|---|---|
| Model（苦力/LLM） | ✅ | ❌ | ❌ |
| Verifier（gate/replay） | ❌ | ✅ | ❌ |
| Authority（人） | ❌ | ❌ | ✅ |

**现实冲突（诚实登记）**：本仓库是**单用户系统**——
产出方（苦力批次）、操作者、Authority 实际都是**同一个人**。
⇒ No single principal 在当前**只能靠纪律维持，无法靠架构强制**。
这是本接口的**最大局限**，见 §七。

---

## 七、局限性（诚实登记）

1. **单用户系统**：Authority 只有一个人，"Model ≠ Verifier ≠ Authority" 三角色
   在**人身层面**是同一人，仅靠**流程分离**（不同批次、不同工具、不同日志）近似实现。
2. **本批不启用**：C1 只是定义；C2 记录的是**从现有人审通道导入的历史决策**，
   不是"通过本接口新做的决策"。
3. **schema 未支持全部级别**：619 B1 schema 的 `human_authority.status`
   只有三值，`conditionally_authorized` 与 `abstain` 需 schema 升级（留后续）。
4. **未实现 Authority 类**：刻意不实现——实现它就等于造出机器 Authority，违反 §一。
5. **未做 30 条逐条人审**：620 不代签任何决策（硬边界 9）。

---

## 八、交人项（620 不代决）

1. Authority 接口是否**正式启用**并替换现有人审通道？
2. 30 条逐条人审是否通过本 Authority 接口执行？
3. PCK 是否成为权威源（83 张证书已就绪，待拍板）？
4. schema 是否升级以支持 `abstain` / `conditionally_authorized`？
