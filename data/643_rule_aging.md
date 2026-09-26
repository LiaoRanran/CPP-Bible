# 643 E2 · 规则老化检测（抗 Goodhart #2）

> 规模 **67** 条规则；建议分布 `{'拆分候选': 6, '保留': 26, 'insufficient_data': 33, '收紧候选': 2}`；趋势阈值 `≤ -2`；日历窗口 **30 天（不可用，见下）**。

## 一、建议清单（非「保留」项）

| 规则 | 级别 | 触达轮数 | 趋势 | 逃逸关联 | 建议 | 理由 |
|---|---|---|---|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `ATOM-MISCONCEPTION-LEVELS` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `ATOM-REL-TARGET-HC` | block | 0/0 | — | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `ATOM-REL-UNKNOWN-HC` | block | 0/0 | — | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `ATOM-SUPERIORITY-WORDS` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `CARD-PATH-NOT-CANONICAL-HC` | block | 0/0 | — | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `DOC-ZERO-PLACEHOLDER` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-ENV-DEPENDENT-KEY` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-FALSIFICATION-QUANT` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-FIXTURE-NO-ECHO-DATA` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-MATRIX-UNBACKED` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-OUT-STALE-MTIME` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-OUT-UNDECLARED-KEY` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-RUN-KEY-DECLARED-EXISTS` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-SELF-SATISFIED-ASSERT` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-SERVES-EXIST-HC` | block | 0/0 | — | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-TRIVIAL-OBSERVATION` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-WERROR-DECL-BIND` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `EV-ZERO-DIAG-WERROR` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `HUMAN-GOLDEN-REVIEW` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `HYBRID-TEACHING-DEPTH` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `INFERENCE-NOT-MACHINE-VERIFIED` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `LLM-SUPERIORITY-QUALITY` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `META-MANIFEST` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `MIS-LIBRARY` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `OBSERVATION-LIVENESS` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `PED-MISCONCEPTION` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `PED-MOTIVATION` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `PED-PREDICT-FIRST` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `PED-SOCRATIC` | advice | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `S1-AUTHOR-SELF-VERIFY` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `S1-GIT-AUTHOR-BINDING` | warn | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `S3-EXPECTED-HARDCODED` | block | 0/6 | 0 | 0 | **insufficient_data** | 六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判** |
| `ATOM-FM-REQUIRED` | block | 4/6 | 0 | 2 | **拆分候选** | 被 2 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `ATOM-ID-FORMAT` | block | 2/6 | 0 | 4 | **拆分候选** | 被 4 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `ATOM-ID-UNIQUE` | block | 2/6 | 0 | 3 | **拆分候选** | 被 3 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `ATOM-NO-UNVERIFIED` | block | 1/6 | -1 | 3 | **拆分候选** | 被 3 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `ATOM-STATUS-VALUE` | block | 2/6 | -2 | 3 | **拆分候选** | 被 3 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `ATOM-VERIFIED-BOUND` | block | 1/6 | 1 | 2 | **拆分候选** | 被 2 条逃逸案例关联 ⇒ 可能一条规则管了两件事 |
| `EV-FM-REQUIRED` | block | 2/6 | -2 | 0 | **收紧候选** | 轮次趋势 -2 ≤ -2 ⇒ 后半程明显少触达（老化/条件漂移） |
| `EV-MATRIX` | block | 2/6 | -2 | 0 | **收紧候选** | 轮次趋势 -2 ≤ -2 ⇒ 后半程明显少触达（老化/条件漂移） |

## 二、⚠️ 口径替代与数据缺口

- **最近 30 天的命中趋势**：本仓**没有带日期的逐规则命中明细** ⇒ 只能用**轮次轴**（6 轮变异跑批）替代，**不等于日历时间**
- **误报率趋势**：642 追踪器 67/67 为**代理值** ⇒ 不据此下结论（A3 教训 3）
- **每条逃逸的时间归属**：逃逸案例无时间字段 ⇒ 只能算"关联数"，不能算"最近"

> 这三项**不是漏做**而是**数据缺该维度**；本工具**不编造趋势**。

## 三、判据（可复算）

| 建议 | 判据 |
|---|---|
| `退役候选` | 六轮全未触达 **且** 有逃逸关联 |
| `拆分候选` | 被 ≥2 条逃逸案例关联 |
| `收紧候选` | `trend ≤ -2`（后半程明显少触达） |
| `保留` | 有触达且无老化证据 |
| `insufficient_data` | 零触达且零关联 ⇒ **没有证据 ⇒ 不判** |

## 诚实登记

1. **轮次轴 ≠ 日历时间**：6 轮跑批的间隔由批次节奏决定，**不能**解释为「最近 30 天」；
2. **代理误报率不进判据**（A3 教训 2）：67/67 是代理值，用它判老化等于自欺；
3. **`insufficient_data` 是「结论」不是失败**：没有证据时给「保留/退役」都是编；
4. **阈值 `trend ≤ -2` 是本批经验值**（边界已在单测固定）；
5. 本工具**只读**：不改规则、不重钉台账。
