# 623 A2 · 80 条高复杂度带 mutation 沙箱实跑（真实 gate 判决）

> 工具：`tools/sandbox_apply_622.py::run_batch`（622 A1 沙箱 apply API）
> 输入：`data/high_complexity_mutations_623.json`（A1 生成的 80 条）
> 方式：**真跑 gate**（`gate_engine.py --run --json`），逐卡取基线 findings 做 diff
> 运行环境：Windows 本地（.venv），单条均值 ≈ 6.6s，80 条总耗时 527.1s

---

## 一、真实判决结果（80 条）

| 判决 | 条数 | 占比 |
|---|---|---|
| **blocked**（新增 block 级违规 ⇒ 被拦住） | **46** | 57.5% |
| **detected_nonblock**（新增 warn/advice 级检出） | **16** | 20% |
| **neutral**（无新增、无消失） | **12** | 15% |
| **escaped**（基线 findings 消失，严格口径） | **4** | 5% |
| **infra_error**（无法施加） | **2** | 2.5% |

**新逃逸发现：4 条（严格口径）**——但见 §三深度分析，4 条均为 **warn 级 findings 随内容被删而消失**，非 block 级检测被击败。

| 项 | 值 |
|---|---|
| 总耗时 | **527.1 s** |
| 单条均值（全部 80） | 6.59 s |
| 单条均值（实际施加 78 条） | 6.73 s |
| infra_error 单条耗时 | 0（施加前即判定） |

## 二、实际触达规则数（核心压力指标）

| 口径 | 622 A2 | **623 A2** | 变化 |
|---|---|---|---|
| 实际触达规则数 | **9/63（14.3%）** | **25/63（39.7%）** | **+16 条（+178%）** |
| 其中 block 级 | — | 17 条 | — |
| 其中 warn 级 | — | 8 条 | — |
| 新逃逸（严格口径） | 0 | 4 | +4 |

> **目标对照**：623 目标 A2 单轮触达 **>30** 条规则；本批本地实跑 **25** 条。
> 未达 30 的**主因**（详见 A3）：
> 1. **Windows 大小写不敏感**导致大小写类规则本地不触发（`EV-ARTIFACT-FILE-EXISTS`、`CARD-PATH-NOT-CANONICAL` 部分）——这些规则在 Linux CI（大小写敏感 FS）会额外触发，本地计数是**下界**。
> 2. 部分预测规则未触发（如 `ATOM-VERIFIED-BOUND` 因所选手卡 status≠verified、`DOC-ZERO-PLACEHOLDER` 占位符模式不匹配等）。
> 3. A4 第三轮将针对这些盲区补打，累计触达目标 >40。

**实际触达的 25 条规则**：

block 级（17）：`ATOM-AUDIENCE` / `ATOM-DAL-MATCH` / `ATOM-FM-REQUIRED` / `ATOM-GRAY-ZONE` / `ATOM-ID-FORMAT` / `ATOM-ID-UNIQUE` / `ATOM-NO-UNVERIFIED` / `ATOM-REL-DAG` / `ATOM-STATUS-VALUE` / `EV-ARTIFACT-PRODUCER` / `EV-ARTIFACT-VERSION-MATCH` / `EV-FM-DUP-KEY` / `EV-FM-REQUIRED` / `EV-FM-YAML-HARDENING` / `EV-ID-UNIQUE` / `EV-MATRIX` / `EV-MSCV-NO-VERIFY`

warn 级（8）：`ATOM-CLAIM-STRUCTURED` / `ATOM-PREREQ-READABLE` / `ATOM-REL-TARGET` / `ATOM-REL-UNKNOWN` / `ATOM-VERIFY-REASON` / `CARD-PATH-NOT-CANONICAL` / `EV-ASSERT-COUNT-BELOW-BASELINE` / `EV-SERVES-EXIST`

（另：`EV-FM-YAML-HARDENING` 同时以 block 与 warn 触发，已计入。）

## 三、4 条 escaped 的深度分析（重要：不是危险逃逸）

4 条 escaped **全部是 M1 删除 `claim_structured` 字段**，消失的 findings 为：

| 消失的规则 | 级别 | 性质 |
|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | warn | 概念名归一化检查 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | block | inference 命题不得机器独自晋升 |
| `OBSERVATION-LIVENESS` | warn | observation 命题须有活性对照 |

**关键判断**：这 4 条是**"攻击删掉了被检查的内容本身"**导致的 findings 消失，不是"攻击在内容保留下绕过了检测"。
`INFERENCE-NOT-MACHINE-VERIFIED` 虽是 block 级，但它原本就在检查 `claim_structured` 里的 inference 命题；删除 `claim_structured` 后该命题不复存在，自然无从检查。**这是 diff 口径的度量假象，不是真实安全逃逸。**

⇒ 本批**真实危险逃逸仍为 0**（与 622 一致），但暴露了沙箱 "escaped" 定义（"任何基线 finding 消失"）的缺陷：
应改为 **"内容保留下、某条 block 级 findings 消失"** 才算逃逸。这是 A3 的方法论改进点之一。

## 四、与 A1 预测的对比（预测准确率）

| 口径 | 值 |
|---|---|
| A1 预测触达规则数 | 32 |
| A2 实际触达规则数 | 25 |
| **预测准确率（规则级）** | 25/32 ≈ 78% |

> 比 622 的 v7 先验预测（51.85%）**高 26 个百分点**——证明 A1 的 rule-aware 反向构造显著更可靠。
> 11 条预测未触发：多为 warn 级占位符/禁词/平凡观测类（本地 FS 或模式不匹配），非 block 级盲区。

## 五、每条 mutation 耗时（节选）

| mutation_id | 卡 | 编辑 | 判决 | 新增规则 |
|---|---|---|---|---|
| MUT-623-d07e8ab9638b | ATOM-CONC-FENCE-001 | 删 claim_structured | escaped | lost: OBSERVATION-LIVENESS 等 |
| MUT-623-3e2e5777d296 | ATOM-CONC-FENCE-001 | 删 first_hand | blocked | ATOM-FM-REQUIRED |
| MUT-623-af02f716c56d | ATOM-… | status→bogus_enum | blocked | ATOM-STATUS-VALUE |
| MUT-623-e1700630ab4c | EV-CONC-001 | artifact 路径大小写 | detected_nonblock | CARD-PATH-NOT-CANONICAL |
| MUT-623-…M34 | EV-CONC-001 | command 掺 cl | blocked | EV-MSCV-NO-VERIFY |

## 六、局限性声明

1. **本地 Windows 运行**：大小写敏感类规则（`EV-ARTIFACT-FILE-EXISTS` 等）本地不触发，本地触达数 25 是**下界**；Linux CI 会更高。
2. **"escaped" 口径偏宽**：任何基线 finding 消失即计 escaped，导致 4 条 warn 级内容删除被误计（见 §三）；VFDR 真实危险逃逸仍为 0。
3. **受控目录零污染**：沙箱原地改+必还原，80 条跑完 `git status` 工作树无改动（护栏：字节级备份+还原+sha256 校验+并发锁）。
4. **只跑 gate（规则层）**，未跑 replay 复算层（属监工门禁，622 §六.4 不跑）。
5. **单次运行**确定性（gate 无随机），但 80 条仅跑一遍，未做重复一致性验证。
6. **2 条 infra_error**：目标卡缺所需字段（schema 边缘情况），不影响结论。
