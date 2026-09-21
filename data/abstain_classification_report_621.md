# 621 C2 · 全量 83 张卡 ABSTAIN 分类

> 分类器：`tools/abstain_classifier_621.py --all`
> 产物：`data/abstain_classification_621.jsonl`（83 条）
> 六态见 `data/abstain_state_definition_621.md`

---

## 一、83 张卡的 6 态分布

| 状态 | 张数 | 占比 | 弃权态 |
|---|---|---|---|
| **SUPPORTED** | **56** | 67.5% | 否 |
| **UNDECIDED** | **27** | 32.5% | ✅ **是** |
| REFUTED | 0 | 0% | 否 |
| INSUFFICIENT_EVIDENCE | 0 | 0% | ✅ 是 |
| CONFLICTED | 0 | 0% | ✅ 是 |
| STALE | 0 | 0% | ✅ 是 |

**弃权合计：27 / 83（32.5%）** —— 近三分之一的卡，系统诚实地说"我不知道"。

## 二、原子卡 vs 证据卡对比

| 类型 | 张数 | 分布 |
|---|---|---|
| 原子卡（27） | 27 | **UNDECIDED 27（100%）** |
| 证据卡（56） | 56 | **SUPPORTED 56（100%）** |

**原因**（可从输入字段复算）：

- **证据卡**：frontmatter 有 `verdict: confirm` + 有 `artifact_sha256` ⇒ SUPPORTED
- **原子卡**：**没有 `verdict` 字段**（原子卡用 `status` 而非 `verdict`）⇒ 落入 UNDECIDED

⇒ 这不是分类器的 bug，而是**两类卡的元数据字段口径不一致**的真实反映。
原子卡从来没有机器判决字段，所以系统对它们**只能弃权** —— 这正是雷6 要暴露的东西。

## 三、各主题（domain）分布

| domain | 张数 | 分布 |
|---|---|---|
| mem | 66 | UNDECIDED 21 · SUPPORTED 45 |
| conc | 9 | UNDECIDED 3 · SUPPORTED 6 |
| lang | 3 | UNDECIDED 1 · SUPPORTED 2 |
| ub | 3 | UNDECIDED 1 · SUPPORTED 2 |
| hist | 2 | UNDECIDED 1 · SUPPORTED 1 |

各主题的弃权比例都在 **~33%**（21/66=31.8%、3/9=33.3%、1/3、1/3、1/2），
分布均匀 ⇒ 弃权不是某个主题的局部问题，而是**原子卡 vs 证据卡的结构性差异**。

## 四、与 PCK authorized 状态的交叉对比（⚠ 关键发现）

| ABSTAIN 状态 × `human_authority.status` | 张数 |
|---|---|
| **SUPPORTED × pending** | **56** |
| **UNDECIDED × approved** | **27** |

**这是一个完全反相关的结果**：

- **机器说"支持"的 56 张（全部证据卡），人全部未批准（pending）**；
- **机器说"不知道"的 27 张（全部原子卡），人全部已批准（approved）**。

**解读（诚实）**：

1. 机器判据与人的判定**基于完全不同的信号**：
   - 机器的 SUPPORTED 只看 `verdict: confirm` + 有工件哈希；
   - 人的 approved 来自卡 frontmatter 的 `status: verified*`。
2. 证据卡虽然机器侧写着 `verdict: confirm`，但 `status` 仍是 `draft` ⇒ **人从未批准**。
   这说明"机器确认"**不等于**"人接受" —— 620 C3 已经发现证据卡 0% authorized，此处再次印证。
3. 原子卡虽然人已标 `verified`，但**没有机器判决字段** ⇒ 机器只能弃权。
   ⇒ **人的"已验证"没有对应的机器判据支撑**，这是治理上的真空地带。
4. **结论**：ABSTAIN 分类与 human_authority 是**两套独立口径**，
   交叉对比暴露出"机器说知道、人没认"和"人认了、机器不知道"**两个方向的缺口同时存在**。

## 五、为什么 CONFLICTED / STALE / INSUFFICIENT_EVIDENCE 都是 0（如实）

| 状态 | 为 0 的原因 |
|---|---|
| **CONFLICTED** | 依赖 frontmatter `relations[].type` 含 `contradict*`；实测 83 张卡的 `relations` **几乎全为空数组** ⇒ 检测不到矛盾 |
| **STALE** | 依赖 `verified_at`；原子卡有该字段但都在 90 天内（最近 2026-09-12，距今 9 天），证据卡**没有**该字段 ⇒ 判不出过期 |
| **INSUFFICIENT_EVIDENCE** | 83 张卡**都有**至少 1 个证据锚（证据卡有 `artifact_sha256`，原子卡有 `claim_structured[].evidence`） |
| **REFUTED** | 没有任何卡的 `verdict` 是 `refute` |

⇒ **0 不等于"不存在这些问题"**，而是**现有卡的元数据不足以支撑这些判定**。
特别是 CONFLICTED=0 很可疑：不是真的没有矛盾，而是 `relations` 字段普遍没填。

## 六、局限性声明

1. **规则-based，不是语义理解**：只看字段存在性、日期、`verdict` 字面值，
   **不理解证据内容是否真的证成主张**。
2. **阈值 90 天是拍的**，无数据支撑；且因缺 `verified_at`，STALE 实际未被真正检验。
3. **CONFLICTED=0 是元数据缺失的结果**，不应读作"系统无矛盾证据"。
4. **原子卡 UNDECIDED 是字段口径问题**：若要让原子卡可分，需给原子卡补
   `verdict` 字段或让分类器改用 `status`——但改分类器去适配字段会**掩盖口径不一致**，
   本批**不做**（留 622 + 人拍板）。
5. **不与 human_authority 打通**：交叉对比只是并列展示，**不代签**、不改变任何审批状态。
6. 分类结果基于**当前** frontmatter；卡一旦补字段，分类会变（可重跑）。
