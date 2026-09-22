# 623 A5 · VFDR 更新 + 规则触达热力图

> VFDR = **V**erifiable **F**alsification **D**iscovery **R**ate（可验证证伪发现率）
> =（被拦 blocked + 检出非 block detected_nonblock）/ 总 mutation 数。
> 逃逸口径改为**双轴**（A3/A4 结论）：escaped_strict（任何基线 finding 消失）vs escaped_dangerous（内容保留下 block finding 消失）。
> 第二主指标：**闭环触达规则数 / 63**（度量闭环是否打到高复杂度带）。

---

## 一、VFDR 三轮对比

| 批次 | 总 mutation | blocked | detected_nonblock | neutral | escaped(strict) | escaped_dangerous | **VFDR(检测率)** |
|---|---|---|---|---|---|---|---|
| 622 A2 | 50 | 13 | 0 | 14 | 0 | 0 | 26.0% |
| **623 A2** | 80 | 46 | 16 | 12 | 4 | 0 | **77.5%** |
| **623 R3** | 40 | 12 | 14 | 14 | 0 | 0 | **65.0%** |

- **检测率跃升**：622 的 26% → 623 的 77.5%（A2）/ 65%（R3）。提升来自 A1 的 rule-aware + schema-aware（622 的 46% infra_error 在 623 降到 ~2.5%）。
- **真实危险逃逸（dangerous）全程 = 0**，与 622 一致；623 A2 的 4 条 strict-escaped 经 A3 证实为**删字段致 content 消失的假象**。
- **VFDR 未达 100% 的原因**：neutral 12+（A2）/ 14（R3）属"编辑生效但未触发规则"——多为 warn 级占位符/平凡观测/禁词表未命中，非 block 级漏检。

## 二、闭环触达规则数（第二主指标）

| 口径 | 622 A2 | 623 A2 | 623 R3 | 累计(A2+R3) |
|---|---|---|---|---|
| 触达规则数 / 63 | 9 (14.3%) | 25 (39.7%) | 6 (9.5%) | **26 (41.3%)** |
| 其中 block | — | 17 | — | 21/40 |
| 其中 warn | — | 8 | — | 5/16 |
| 其中 advice | — | 0 | — | 0/7 |

- **目标对照**：623 目标 A2 单轮 >30、三轮累计 >40。**实测 A2=25、累计=26，均未达目标**（诚实登记，见 §四根因）。
- **advice 级 0 触达**：7 条 pedagogy/LLM/human 建议级规则（PED-* / LLM-SUPERIORITY-QUALITY / HYBRID-TEACHING-DEPTH / HUMAN-GOLDEN-REVIEW）本就不该被 field-edit 攻击触发，属预期。

## 三、规则触达热力图（节选，全量见 data/rule_touch_heatmap_623.md）

- **已触达（26）**：ATOM-FM-REQUIRED / ATOM-ID-FORMAT / ATOM-ID-UNIQUE / ATOM-NO-UNVERIFIED / ATOM-STATUS-VALUE / ATOM-DAL-MATCH / ATOM-REL-DAG / ATOM-AUDIENCE / ATOM-PREREQ-READABLE / ATOM-GRAY-ZONE / ATOM-CLAIM-STRUCTURED / EV-FM-REQUIRED / EV-ID-UNIQUE / EV-MATRIX / EV-ARTIFACT-VERSION-MATCH / EV-MSCV-NO-VERIFY / EV-FM-DUP-KEY / EV-FM-YAML-HARDENING / EV-ARTIFACT-PRODUCER / EV-ASSERT-COUNT-BELOW-BASELINE / EV-ASSERT-SYMBOL-MAPPED / ATOM-REL-TARGET / ATOM-REL-UNKNOWN / ATOM-VERIFY-REASON / CARD-PATH-NOT-CANONICAL / EV-SERVES-EXIST
- **未触达（37）** 含：需编译/复算层（EV-ZERO-DIAG-WERROR / EV-WERROR-DECL-BIND / S3-EXPECTED-HARDCODED）、需 git 绑定（S1-*）、需多卡/claim 结构（ATOM-REL-CONFLICT / OBSERVATION-NEEDS-ARTIFACT / INFERENCE-NOT-MACHINE-VERIFIED）、禁词/平凡词表未命中（ATOM-SUPERIORITY-WORDS / EV-FALSIFICATION / EV-TRIVIAL-OBSERVATION / DOC-ZERO-PLACEHOLDER）、以及 7 条 advice 级。

## 四、未达 30/40 的根因（诚实登记，留 624 决策）

1. **载体上限（主因）**：本沙箱 = gate-only + 单卡 field-edit。约 14 条 block 规则需**编译产物 / replay 复算 / git 绑定 / 多卡语义**才能构造违规输入，远超单卡 field-edit 的表达力。
2. **词表黑盒**：SUPERIORITY-WORDS / FALSIFICATION 等规则的触发词表未在 623 内逆向，构造命中靠猜测，多数 neutral。
3. **status 共存条件**：VERIFIED-BOUND / STATUS-TRANSITION 即便选 verified 卡仍不触发，说明规则还依赖 evidence 绑定等共存条件，单删字段不够。
4. **Windows 本地下界**：EV-ARTIFACT-FILE-EXISTS 等大小写敏感规则本地不触发（Linux CI 更高），26 是本地下界。

**结论**：以现有沙箱载体，闭环触达天花板约 **26/63（41%）**。要突破 30/40，须扩展沙箱到复算/多卡/git 层（属 624 架构升级，非 623 工作量内可完成）。

## 五、VFDR 监控建议（落地）

1. **双轴逃逸看板**：`escaped_strict`（监控假象信号）+ `escaped_dangerous`（真实风险），A5 起分别记录。
2. **覆盖率看板**：把"闭环触达规则数/63"作为常态指标，目标逐步逼近天花板 26→（扩展后）更高。
3. **neutral 标注**：neutral mutation 在生成器侧标注"该规则需非 field-edit 构造"，避免重复空打。

## 六、局限性声明

1. 仅 gate 层，未跑 replay/compile（同 A2/A4）。
2. 触达数为 Windows 本地下界；Linux CI 会更高（大小写敏感规则）。
3. 词表为黑盒，禁词/平凡判定靠假设。
4. 单次运行，确定性。
