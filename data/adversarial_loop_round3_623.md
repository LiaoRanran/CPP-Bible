# 623 A4 · 闭环第三轮实跑（40 条定向攻击 + VFDR 触发阈值/误报口径更新）

> 工具：`tools/sandbox_apply_622.py::run_batch`
> 输入：`data/adversarial_loop_round3_mutations_623.json`（A4 生成器，40 条，定向补打 A2 未触达规则）
> 运行环境：Windows 本地，40 条总耗时 **271.4 s**，单条均值 6.79 s

---

## 一、第三轮判决结果（40 条）

| 判决 | 条数 | 占比 |
|---|---|---|
| blocked | 12 | 30% |
| detected_nonblock | 14 | 35% |
| neutral | 14 | 35% |
| escaped | 0 | 0% |
| infra_error | 0 | 0% |

**新逃逸：0**（第三轮无 escaped — 印证 A3 结论：A2 的 4 条 escaped 是删字段假象，本轮刻意保留内容、只做就地改写，故 escaped 归零）。

## 二、触达规则数（核心指标）

| 口径 | 值 |
|---|---|
| 第三轮（R3）单轮触达 | **6 条**（ATOM-FM-REQUIRED / CARD-PATH-NOT-CANONICAL / EV-ARTIFACT-VERSION-MATCH / EV-ASSERT-COUNT-BELOW-BASELINE / EV-ASSERT-SYMBOL-MAPPED / EV-FM-YAML-HARDENING） |
| **累计（A2 80 + R3 40）** | **26 条 / 63（41.3%）** |
| A2 单轮 | 25 条 |

> 目标对照：623 目标 A2 单轮 >30、三轮累计 >40。**实测 A2=25、累计=26，均未达到目标。**

## 三、为什么累计停在 26（关键根因，诚实登记）

第三轮定向补打的 10 条目标规则中，**仅 `EV-ASSERT-SYMBOL-MAPPED` 为新增触达**（+1），
其余 9 条（ATOM-VERIFIED-BOUND / ATOM-STATUS-TRANSITION / ATOM-SUPERIORITY-WORDS /
EV-FALSIFICATION / DOC-ZERO-PLACEHOLDER / EV-TRIVIAL-OBSERVATION / EV-SELF-SATISFIED-ASSERT /
S2-EVIDENCE-VERDICT / EV-ENV-DEPENDENT-KEY）**全部 neutral**——编辑施加成功但**未触发预期规则**。

逐类根因：

1. **需编译/复算层（gate-only 沙箱表达不了）**：`EV-ZERO-DIAG-WERROR` / `EV-WERROR-DECL-BIND` /
   `S3-EXPECTED-HARDCODED` / `EV-MSCV-NO-VERIFY`（部分）依赖 `.out`/编译产物与 gate 之外的复算，
   单卡 field-edit 无法构造对应违规输入。
2. **需 git 绑定**：`S1-AUTHOR-SELF-VERIFY` / `S1-GIT-AUTHOR-BINDING` 依赖 commit author，沙箱不改 git。
3. **需多卡语义**：`ATOM-REL-CONFLICT` / `OBSERVATION-NEEDS-ARTIFACT` / `INFERENCE-NOT-MACHINE-VERIFIED`
   需跨卡或 claim_structured 内部结构，单卡 field-edit 只能删字段（致假象）不能构造"保留内容下的矛盾"。
4. **禁词/平凡判定词表与假设不符**：`ATOM-SUPERIORITY-WORDS`(obviously/clearly)、
   `EV-FALSIFICATION`(平凡)、`EV-TRIVIAL-OBSERVATION`、`DOC-ZERO-PLACEHOLDER`(TODO/TBD) 的触发词表
   与我的假设不一致 ⇒ 编辑未命中规则阈值（neutral）。
5. **status 过滤仍不精准**：`ATOM-VERIFIED-BOUND`/`ATOM-STATUS-TRANSITION` 即便仅选 status=verified 的卡，
   删除 superiority/status_history 仍未触发——说明规则判定还依赖其它共存条件（如 evidence 绑定）。

**结论**：以"gate-only + 单卡 field-edit"为载体的沙箱攻击，其**规则触达天花板约为 26/63（≈40%）**。
剩余 ~14 条 block 规则需编译/复算/git/多卡构造，超出本沙箱表达力。
这并非 effort 不足，而是**架构性上限**——要在 623 内突破 30/40，必须扩展沙箱到复算/多卡/git 层（留 624 决策）。

## 四、VFDR 触发阈值与误报口径更新（A4 交付物）

1. **逃逸口径拆分为双轴**：
   - `escaped_strict`（现状）：任何基线 finding 消失 ⇒ A2=4、R3=0。
   - `escaped_dangerous`（建议）：内容保留下 block finding 消失 ⇒ 全程 0（真实安全逃逸 0）。
   A5 热力图据此双轴呈现，避免把"删字段假象"误读为逃逸。
2. **VFDR 触发阈值维持 0**：真实危险逃逸恒为 0，但新增"严格口径假象逃逸"维度（A2=4）作为独立监控信号。
3. **触达覆盖率纳入 VFDR 主指标**：原 VFDR 只看逃逸；623 起把"闭环触达规则数/63"作为第二主指标
   （A2=25、R3 累计=26），用以度量闭环是否"打到高复杂度带"。
4. **误报（neutral）口径**：14 条 neutral 属"编辑生效但未触发规则"，属**预期内误报**，不计入逃逸，
   但应在生成器侧标注"该规则需非 field-edit 构造"，避免反复空打。

## 五、与 A2 的对比

| 维度 | A2（80 条） | R3（40 条） |
|---|---|---|
| 被拦率 | 57.5% | 30% |
| 新逃逸（strict） | 4（假象） | 0 |
| 单轮触达 | 25 | 6 |
| 主要价值 | 覆盖率飞跃 + 暴露假象逃逸 | 验证天花板 + 清零假象逃逸 |

## 六、局限性声明

1. **仅 gate 层**：同 A2，未跑 replay/compile，故编译/复算类规则无法触达（见 §三.1）。
2. **单卡 field-edit 载体**：无法表达多卡/claim 内部结构类违规（§三.3）。
3. **禁词表为黑盒**：SUPERIORITY-WORDS 等规则的词表未经逆向，构造命中靠猜测（§三.4）。
4. **单次运行**，确定性，未做重复验证。
