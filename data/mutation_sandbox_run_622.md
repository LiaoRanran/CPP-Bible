# 622 A2 · 50 条新 mutation 沙箱实跑（真正 gate 判决）

> 工具：`tools/sandbox_apply_622.py`（622 A1）· 输入：621 A2 的 50 条新 mutation
> 方式：**真跑 gate**（`gate_engine.py --run --json`），不再是 v7 先验预测
> 基线：整仓 gate 一次（191 findings，status=pass），逐卡取基线 findings 做 diff

---

## 一、真实判决结果（50 条）

| 判决 | 条数 | 占比 |
|---|---|---|
| **blocked**（新增 block 级违规 ⇒ 被拦住） | **13** | 26% |
| **neutral**（无新增 block、也无检测消失） | **14** | 28% |
| **infra_error**（无法施加到该卡） | **23** | 46% |
| **escaped**（无新增 block 且基线检测消失） | **0** | 0% |

**新逃逸发现：0 条**（严格口径：必须"检测消失"才算逃逸）。

| 项 | 值 |
|---|---|
| 总耗时 | **180.0 s** |
| 单条均值（全部 50） | 3.60 s |
| 单条均值（**实际施加的 27 条**） | **6.66 s**（≈ 一次整仓 gate 的开销） |
| 单条中位 | 6.51 s |
| infra_error 单条耗时 | 0 ms（施加前即判定，不跑 gate） |

## 二、⚠ 23 条 infra_error 的根因（重要发现）

`infra_error` **不是** sandbox 的缺陷，而是**621 生成器的质量缺陷**。
原因：621 A1 生成 mutation 时，把 `target_rule` **机械映射**到该规则"按理该管"的字段，
但**没有检查目标卡上是否真的有这个字段**。

| 失败原因（按 op） | 条数 | 缺失字段示例 |
|---|---|---|
| M7 篡改 `id` / `claim_structured` | 7 | 证据卡没有 `claim_structured` |
| M2 路径变形 `artifact` / `falsification` | 5 | 卡上无 `artifact` / `falsification` |
| M6 键名变形 `artifact_producer` / `falsification` | 4 | 字段不存在 |
| M3 弱化断言（`liveness`） | 4 | 卡上无 `run_match_keys` |
| M1 删字段 `matrix` / `artifact_producer` | 2 | 字段不存在 |
| M5 status 变形（`matrix`） | 1 | 字段不存在 |

⇒ **46%（23/50）的 mutation 对目标卡"不适用"**。
即 621 的 `point`/`detail` 是**描述性意图**，与**卡的实际 schema** 脱节。

## 三、与 621 v7 先验预测的对比

| 口径 | 值 |
|---|---|
| 可比对条数 | 27（23 条 infra_error 不可比） |
| 一致 | **14** |
| 不一致 | **13** |
| **一致率** | **51.85%** |

**差异类型**（抽样）：

| mutation | 卡 | 预测 | 实际 | 说明 |
|---|---|---|---|---|
| `MUT-621-af15a0c5cc3a` | ATOM-CONC-FENCE-001 | n_a | **blocked** | 删 `id` 触发 `ATOM-FM-REQUIRED`（预测漏判） |
| `MUT-621-030f3c3bc310` | ATOM-MEM-LEAK-002 | n_a | **blocked** | 同上 |
| `MUT-621-d4303e9a3979` | EV-CONC-003 | blocked | **neutral** | 预测高估（以为会被拦，实际无变化） |

**结论**：v7 先验预测的**一致率只有 51.85%**，接近抛硬币。
⇒ **621 的"预测口径"不可靠**，本批用沙箱真跑纠正了这一点。
这是 622 A1 存在价值的最直接证据。

## 四、为什么是 0 条逃逸（初步；详见 A3）

1. **23 条根本没施加**（§二）⇒ 有效样本只有 27 条；
2. 27 条中 13 条被 block、14 条 neutral，**没有一条造成"检测消失"**；
3. 14 条 neutral 的含义：变异既没触发新 block，也没抹掉既有 finding
   —— 多为 `status → draft`、恒真断言注入这类**不改变规则判定**的编辑。

## 五、局限性声明

1. **有效样本仅 27/50**（54%）：近半 mutation 不适用（§二）。
2. **`escaped` 采用严格口径**（必须"检测消失"），
   ⇒ 14 条 neutral 里可能藏有"弱化但未完全抹除"的情况，本口径**不把它们计为逃逸**（保守）。
3. **单次运行**：gate 判定是确定性的（无随机），但**未做重复运行**验证稳定性。
4. **沙箱为原地改+还原**（`gate_engine` 无自定义 root / 单卡模式）：
   护栏为字节级备份 + finally 还原 + sha256 校验 + 并发锁；
   实测 50 条跑完后受控目录 `git status` **零改动**（见 A1 单测与 F2 门禁）。
5. **只跑 gate，未跑 replay**：`replay --check` 属监工门禁（622 §六.4），
   故本批判决**只反映 gate 规则层**，不含 replay 复算层。
6. **未判定 equivalent**：等效性需语义比对，本批如实记 0。
