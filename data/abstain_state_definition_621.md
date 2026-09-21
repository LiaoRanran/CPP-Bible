# 621 C1 · ABSTAIN 状态定义 + 分类器（雷6）

> 状态：**定义 + 工具已落地，未对外启用**（是否写入 PCK 渲染 = §八 人拍板项 2）
> 配套：`tools/abstain_classifier_621.py`（6 态分类器）、C2 全量分类、C3 与 PCK 集成

> **来源说明（诚实登记）**：提示词要求「读 37 号路线图雷6节」，但仓库内
> （`ROADMAP_v2/v3.md`、`WORKLIST_v4.md`、`docs/`）**未检索到**「雷6 / 雷7 / 路线图37」相关章节
> —— 与 620 C1（雷5）遇到的情况一致。故本定义依据 **621 提示词 C1 的规格** +
> **与现有系统的实际映射**推导。若路线图另有规定，以路线图为准并需回改本文件（留 622）。

> **另一处提示词笔误（如实记录）**：C1 步骤 2 写「**5 态**定义」却列出 **6 个**状态名
> （SUPPORTED / REFUTED / UNDECIDED / INSUFFICIENT_EVIDENCE / CONFLICTED / STALE），
> 而步骤 3 与 commit 模板均称「6 态」。本实现按 **6 态**落地。

---

## 一、核心命题：ABSTAIN 不是失败，是能力

现有系统只有**三态**：`confirm` / `refute` / `infra_error`。
这逼着每张卡都必须"给个说法"——证据不足的卡也被塞进 confirm/refute 二选一，
于是**"我不知道"被伪装成"我确认"**。

雷6 要解决的正是这个：**让系统能显式说"我不知道"**。
`UNDECIDED` / `INSUFFICIENT_EVIDENCE` / `CONFLICTED` / `STALE` 都是**弃权态**，
它们不是"分类失败"，而是**分类正确的结果**——正确识别出"现在还不能下结论"。

> 一个只会说 TRUE/FALSE 的验证系统，等于**把不确定性藏起来**。
> 能说"我不知道"的系统，才配谈可信。

## 二、6 态定义

| 状态 | 含义 | 是弃权态？ | 典型触发 |
|---|---|---|---|
| **SUPPORTED** | 证据充分且一致，支持主张 | 否 | verdict=confirm + 有证据 + 未过期 |
| **REFUTED** | 证据充分且矛盾，反驳主张 | 否 | verdict=refute + 有证据 |
| **UNDECIDED** | 有证据但不足以判定 | ✅ **是** | verdict 缺失/未知，或 infra_error |
| **INSUFFICIENT_EVIDENCE** | 缺少关键证据 | ✅ **是** | 证据数为 0 |
| **CONFLICTED** | 证据之间互相矛盾 | ✅ **是** | relations 含 contradicts |
| **STALE** | 证据过期 | ✅ **是** | 超过 90 天未验证 |

**弃权态占 4/6** —— 这本身就是雷6 的立场：多数卡"其实还没有确定答案"。

## 三、判定优先级（分类器实现顺序）

```
1. INSUFFICIENT_EVIDENCE   证据数 == 0
2. CONFLICTED              relations 含 contradict*
3. STALE                   verified_at 已知 且 距今 > 90 天
4. REFUTED                 verdict == refute
5. SUPPORTED               verdict == confirm
6. UNDECIDED               其余（含 infra_error、verdict 缺失）
```

**为什么要这个顺序**：
- 没证据 ⇒ 谈"支持/反驳"没有意义，最优先；
- 证据自相矛盾 ⇒ 再多也不该下结论；
- 过期 ⇒ 结论可能已失效，不能当现成的用；
- 最后才按 verdict 二分。

## 四、输入字段（classifier 的 card_state）

| 字段 | 来源 | 说明 |
|---|---|---|
| `evidence_count` | 原子卡：`claim_structured[].evidence`；证据卡：`artifact_sha256` 是否存在 | 0 ⇒ INSUFFICIENT_EVIDENCE |
| `conflicted` | frontmatter `relations[].type` 含 `contradict*` | ⇒ CONFLICTED |
| `days_since_verify` | `verified_at` 解析为日期后计算 | >90 ⇒ STALE |
| `verdict` | frontmatter `verdict` | confirm/refute/其它 |
| `status` | frontmatter `status` | 仅作参考，不直接决定状态 |

## 五、与现有系统的映射

| 现有概念 | 映射到的 6 态 |
|---|---|
| `verdict: confirm` | SUPPORTED（前提是证据充分且未过期） |
| `verdict: refute` | REFUTED |
| `infra_error`（replay 环境错误） | **UNDECIDED**（不是失败，是"没能判"） ✅ 关键改进 |
| 无任何证据的卡 | **INSUFFICIENT_EVIDENCE**（此前会被硬塞成 confirm） ✅ 关键改进 |
| 过期证据（>90 天） | **STALE**（此前无此概念） ✅ 新增 |
| 证据互相矛盾 | **CONFLICTED**（此前无此概念） ✅ 新增 |

**最重要的改进**：`infra_error` 从"错误"变成 **UNDECIDED（弃权）** ——
跑不了不等于错，只是不知道。这正是雷6 的落点。

## 六、触发条件（什么时候应该 abstain）

 classifier 判定为弃权态，或人工遇到以下情形时应主动 abstain：

1. **证据缺失**：卡没有 `evidence` / `artifact_sha256` 等实证锚。
2. **证据过期**：超过 90 天未复核，且期间工件/编译器可能已变。
3. **证据冲突**：多份证据给出相反结论，且无仲裁规则。
4. **环境不可用**：replay 因工具链/平台限制跑不了（如 MinGW 缺 ASan）。
5. **超出机器能力**：需要语义/价值判断而不仅靠机器判据（如"教学深度够不够"）。

## 七、局限性（诚实登记）

1. **规则-based，不是语义理解**：只看字段存在性与日期，不理解证据内容质量。
2. **90 天阈值是拍的**：没有数据支撑，属约定；调阈值需人拍板。
3. **conflicted 依赖 relations 字段**：现有卡大多 `relations: []`，
   ⇒ CONFLICTED 很可能恒为 0（C2 会实测确认）。
4. **不判定"证据是否真的证成主张"**：只判"有没有/过没过期/矛不矛盾"。
5. **未与 PCK 的 human_authority 打通**：C3 只写 uncertainty 字段，不代签人审。
