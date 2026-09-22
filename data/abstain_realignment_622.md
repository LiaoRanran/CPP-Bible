# 622 C3 · 全量 83 张 ABSTAIN 重新分类 + 与 PCK 交叉验证

> 分类器：`abstain_classifier_621.classify_v2`（622 C1 升级）+ 原子卡 verdict 提取（622 C2）
> 权威口径：**PCK 证书的 `human_authority.status`**（= 27 approved / 56 pending）
> 产物：`data/abstain_realignment_622.jsonl`（83 条）+ `.json`（汇总）

---

## 一、重新分类后的 6 态分布

| 状态 | 张数 | 占比 |
|---|---|---|
| **SUPPORTED** | **83** | **100%** |
| REFUTED | 0 | 0% |
| UNDECIDED | 0 | 0% |
| INSUFFICIENT_EVIDENCE | 0 | 0% |
| CONFLICTED | 0 | 0% |
| STALE | 0 | 0% |

**弃权态：0 / 83（0%）** —— 从 621 的 27 张（32.5%）降到 **0**。

### 判定依据分布（`basis`）

| basis | 张数 | 含义 |
|---|---|---|
| `card_verdict` | **56** | 卡面自带 `verdict: confirm`（全部证据卡） |
| `extracted_verdict` | **27** | 由卡面内容提取（全部原子卡，主要来自 `status=verified`） |

## 二、与 621 C2 旧分类的对比（变化 27 张）

| 项 | 621 C2（分类器 v1） | 622 C3（v2 + 提取） | 变化 |
|---|---|---|---|
| SUPPORTED | 56 | **83** | **+27** |
| UNDECIDED | **27** | **0** | **−27** |
| 弃权率 | 32.5% | **0%** | −32.5pt |

⇒ **27 张原子卡全部从 UNDECIDED 翻转为 SUPPORTED**，与 C2 的提取结果一致。

## 三、与 PCK `human_authority` 的交叉验证（核心）

| ABSTAIN × human_authority | 621 C2 | **622 C3** |
|---|---|---|
| SUPPORTED × approved | 0 | **27** ✅ 对齐 |
| SUPPORTED × pending | 56 | **56** ⚠ 缺口 |
| **UNDECIDED × approved** | **27** | **0** ✅ **反相关已消除** |
| UNDECIDED × pending | 0 | 0 |

| 指标 | 值 |
|---|---|
| 对齐（SUPPORTED×approved + REFUTED×rejected） | **27 / 83** |
| **对齐率** | **32.53%** |
| 「机器支持、人未批」缺口 | **56** |
| 「机器弃权、人已批」缺口 | **0** ✅ |

### 结论：ABSTAIN 与 Authority 是否对齐？

- ✅ **621 的"完全反相关"已被消除**：`UNDECIDED×approved` 从 27 → **0**。
- ⚠ **但仅剩单向缺口**：`SUPPORTED×pending` **56** 张（全部证据卡）——
  机器认为支持，人从未批准（`status=draft`）。
- 对齐率 32.53% 看似低，但它是**两类卡的固有差异**造成的，不是判定不一致：
  - 27 张原子卡：机器支持 + 人已批 ⇒ **真对齐**；
  - 56 张证据卡：机器支持 + 人未批 ⇒ **待补人审**（不是矛盾）。

## 四、⚠ 诚实警示：本次"对齐"有一部分是**构造性**的

**必须说清楚**，否则会高估本批成果：

1. **原子卡的 SUPPORTED 来自 `status=verified`** —— 而 `status` 本身就是**人审的产物**。
   ⇒ v2 用"人的字段"去对齐"人的批准"，**在逻辑上接近同义反复（tautology）**。
   `basis=extracted_verdict` 的 27 张里，**26 张的依据就是 `status=verified/red-team-verified`**。
2. **证据卡的 SUPPORTED 来自它们自己的 `verdict: confirm`** —— 这是卡面字段，
   与"人是否批准"**无关** ⇒ 因此 56 张仍然 pending，缺口真实存在。
3. ⇒ **"弃权率归零"不等于"系统变强"**：它意味着"机器现在能从既有字段推出结论"，
   **不代表**机器独立验证了这些命题。

## 五、局限性声明

1. **规则-based**：只看 `verdict` / `status` / `evidence` / `claim_type`，不判断证据内容质量。
2. **对齐过程部分构造性**（§四）：原子卡的对齐继承自人审字段，非独立证据。
3. **CONFLICTED / STALE / INSUFFICIENT_EVIDENCE 仍恒为 0**：因 `relations` 普遍为空、
   `verified_at` 缺失、所有卡至少有 1 个证据锚 ⇒ 这 3 态的**检测能力未被真正检验**。
4. **口径变更**：本批 C3 用 **PCK 证书** 的 `human_authority`（83 张全覆盖）作为权威口径；
   而**决策日志只覆盖 25 张原子卡**（`ae-MIS-*->ATOM-*` 形态）。
   两者曾产生 27 vs 25 的差异 ⇒ 已统一为 PCK 口径并在产物中标注 `authority_source`。
5. **未修改任何原始卡**：`verdict` 是否写回原子卡 = 622 §八.3 **人拍板项**。
6. **未重渲染 PCK**：`data/pck/rendered/` 未更新（ABSTAIN 是否对外展示 = 621 §八.2 人拍板项）。
