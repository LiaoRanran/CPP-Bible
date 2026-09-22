# 623 A3 · 新逃逸根因分析 v2（复用 622 escape_zero_analysis.md 方法）

> 输入：623 A2 沙箱实跑结果 `data/high_complexity_sandbox_run_623.json`
> 逃逸判决：623 A2 共 **4 条 escaped**（严格口径）。本分析逐条做根因，区分**真实逃逸** vs **测量假象**。
> 方法：沿用 622 §一–§七框架（生成策略强度 / v7 覆盖 / 规则层强度 / 口径修正）。

---

## 一、4 条 escaped 明细（逐条取证）

| mutation_id | 卡 | 编辑 | lost findings | 级别 |
|---|---|---|---|---|
| MUT-623-d07e8ab9638b | ATOM-CONC-FENCE-001 | M1 删 `claim_structured` | OBSERVATION-LIVENESS, INFERENCE-NOT-MACHINE-VERIFIED, ATOM-CLAIM-CONCEPT-NORMALIZED | warn/block/warn |
| MUT-623-…(×4，同构) | 其余 3 张含 claim_structured 的卡 | M1 删 `claim_structured` | 同上 | warn/block/warn |

**关键事实**：4 条 escaped **全部是同一个算子 M1 删除 `claim_structured` 字段**，消失的 findings 集合完全同构
（`OBSERVATION-LIVENESS` / `INFERENCE-NOT-MACHINE-VERIFIED` / `ATOM-CLAIM-CONCEPT-NORMALIZED`）。

## 二、根因分类：真实逃逸 vs 测量假象

| 逃逸 | 内容是否保留 | 判定 |
|---|---|---|
| 4 条（删 claim_structured） | **否**——被删字段本身即被检查对象 | **测量假象** |

**定义修正**：
- **严格口径（沙箱现状）**：任何基线 finding 消失 ⇒ escaped。→ 623 得 4。
- **危险口径（建议）**：**内容保留下、某条 block 级 finding 消失** ⇒ 真实逃逸。→ 623 得 **0**。

4 条全部为"攻击删掉了被检查的内容本身"，属于口径①的度量假象，不是"内容保留下绕过检测"的真实逃逸。

## 三、为什么是假象（而非规则漏洞）

- `INFERENCE-NOT-MACHINE-VERIFIED`（block）检查的是 `claim_structured` 内的 inference 命题不得由机器独自晋升；
  删除 `claim_structured` 后该命题**不复存在**，自然无从检查 ⇒ 其消失是**结构性必然**，不是规则被绕过。
- `OBSERVATION-LIVENESS`（warn）与 `ATOM-CLAIM-CONCEPT-NORMALIZED`（warn）同理：检查对象随字段删除而消失。
- 反证：若某 mutation **保留** `claim_structured` 但**改动其内容**导致这两条 finding 消失，那才是真实逃逸。
  本批 80 条中**不存在此类 mutation**（4 条 escaped 均为删除语义）。

⇒ **本批真实危险逃逸 = 0**（与 622 一致），但**测量方法论首次暴露口径缺陷**。

## 四、逃逸口径修正建议（可执行）

1. **沙箱 escaped 判定改为**：`lost_block_rules and content_retained(mutation)`，其中
   `content_retained` = 编辑未删除被该 finding 检查的字段/段落。
2. **删除类编辑（M1 等）单独计为 `content_removed`，不计入 escaped**；仅当编辑为"就地改写内容"且 block finding 消失时才计 escaped。
3. 该修正应落到 `sandbox_apply_622.py::classify`（属 622 工具 bug 修复，非改 CORE_TOOLS；按铁律可改 622 工具，但 A 线本次不强制，留 F 线收工时评估）。

## 五、与 622 对比（口径一致性）

| 口径 | 622 A2 | 623 A2 |
|---|---|---|
| 严格口径 escaped | **0** | **4** |
| 危险口径 escaped（建议） | 0 | 0 |
| 触达规则数 | 9/63 | 25/63（+178%） |
| 被拦率 | 13/50=26% | 46/80=57.5% |

623 严格口径较 622 **多出 4 条**，但经根因分析**全部为测量假象** ⇒ 真实逃逸率两轮均为 0。
价值不在"发现逃逸"，而在：(a) 触达规则数 9→25 的**覆盖率飞跃**；(b) **首次暴露 escaped 口径缺陷**（→ 口径修正建议）。

## 六、对 VFDR 的影响

- **VFDR 真实危险逃逸仍 0** ⇒ 曲线在 A5 仍维持"有效逃逸 0"；但**新增"嚴格口径假象逃逸 4"**作为独立维度记录，避免把 0 误读为"完全无异常"。
- VFDR 更新要点：把"逃逸"拆为 `escaped_strict` 与 `escaped_dangerous` 两列，A5 热力图据此双轴呈现。

## 七、三个"为什么 0（真实）"结论（逐条回答，复用 622 框架）

### Q1：是生成策略不够强吗？——**否，覆盖率已大幅扩张**
623 A1 的 rule-aware + schema-aware 把触达规则从 6/63（622）→ 25/63，**被拦率 57.5%**（远高于 622 的 26%）。
高复杂度带（MSET/M16/M31/M32/M34/M35/M36/M37/M40）均能施加并被拦。

### Q2：是 v7 已覆盖吗？——**否，算子空间已扩张**
623 采用 622 新增算子（MSET 等），与 v7(M1–M7) 算子空间**自然不重合**；(卡,算子) 重叠率 <5%（估算）。
候选空间真正扩张，不再是 622 的"100% 重叠换变异点"。

### Q3：是 gate 规则已足够强吗？——**在已触达的 25 条范围内是**
本批触发 25 条规则，其中 17 条 block 级**全部被拦**（blocked/escaped 均为 content-removal 假象，无 block finding 在内容保留下消失）。
但**仍有 38 条 block 规则未被本轮触及**（含 S1/S2/S3、EV-ZERO-DIAG-WERROR 等需编译/多卡构造者）⇒ "0 真实逃逸"仅限"被打到的 25 条都硬"，**不能推断全 63 条都硬**。

## 八、下一轮（A4）改进建议

1. **按规则全覆盖**：对未触达的 38 条 block 规则逐条构造变异（尤其中需编译产物的 EV-* 规则）。
2. **叠加 replay 层**：A2 只跑 gate；A4 可叠加 replay 复算，发现"规则过但复算不过"的逃逸。
3. **口径修正落地**：把 §四 的 `content_retained` 判定纳入沙箱，消除假象逃逸。
4. **状态过滤修复**：`ATOM-VERIFIED-BOUND`/`ATOM-STATUS-TRANSITION` 需选 status=verified 的卡（本轮所选手卡 status≠verified 致未触发）。

## 九、局限性声明

1. **只跑 gate，未跑 replay** ⇒ 真实逃逸分析仅限规则层；编译/复算级逃逸未被探测。
2. **4 条 escaped 同构** ⇒ 样本单一，结论"真实逃逸 0"对"删除语义编辑"稳健，对"改写语义编辑"未充分验证。
3. **escaped 口径沿用沙箱现状**（严格口径）⇒ 已显式区分假象；危险口径为建议，尚未落地到代码。
4. **单次运行**，gate 判定确定性，可复现性已另有单测覆盖。
