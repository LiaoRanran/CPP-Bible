# 541 建设日志：T0 试验两次均未达标 → **已回退**（无 commit）+ T1 未做

> 依据：`References/architecture_架构演进/541_进化闭环二_判别力kind门控修复+mutation按卡批性能.md`
> 纪律：不 push / 不 golden accept / **存量零误伤** / 新规则先 warn 后 block / 改 gate 必重钉校验和 / **做不完停在 T 边界、不留半成品**。本批**无 commit**（T0 试验已 `git checkout` 回退，仓库零残留）。

## 0. 开工基线（HEAD=`f034d2c`，亲手实测）

`gate 60 规则 · 141 命中 (block=0 warn=136 advice=5)` · `poison 90/90` · `replay confirm=56` · `tests/test_gate_engine.py` 49 例全绿 · mutation smoke（`--limit 2 --operators M2,M3,M4,M5,M6`）：变体 28 / blocked 14（严格 13）/ escaped 12 / n_a 2（M2×6 · M3×4 · M4×2）。

**收工复测（回退后）**：`gate 60 · 141 · block=0 warn=136 advice=5`、`test_gate_engine.py` 49 例全绿、`git status -- tools/` 仅剩既存未跟踪 `env_check.py` ⇒ **与开工逐字一致，零残留**。

---

## 1. T0 根因确认（与 541 一致）与**两次试验的实测结果**

**根因确认**：`tools/gate_engine.py:1632` 原为
`if kind not in ("contains_in", "absent_in"): continue` —— `contains`/`contains_any`/`absent_any`
被这行直接跳过，于是落在 `text` 字段里的恒真文本（`.file` 等）**零检查**。541 的精确定位成立。

### 试验 1（天真扩白名单：text 侧三分支全开）—— **存量误伤，弃**

把白名单扩成五种 kind、并让既有三个分支（空/纯中文 → block、`*_in` + 通用符号 → advice、
非锚定 + 通用符号 → warn）全部对新 kind 生效。

| 指标 | 开工 | 试验 1 |
|---|---|---|
| `gate --check` | block=0 warn=136 advice=5 | **block=38** warn=136 advice=8 |

⇒ **block 0→38**：那三个分支里"空/纯中文 text ⇒ block"此前只对 `contains_in/absent_in` 可达，
一扩就把**大量既有 `contains` 的散文文本**判成 block。直接违反"存量零误伤 + 先 warn 后 block"。

### 试验 2（收紧：新纳入 kind 只允许"恒真文本 ⇒ warn"）—— **仍有冲突，弃**

新纳入的 kind 走"散文/空文本 ⇒ 维持原行为（continue）"，只保留"通用/恒真文本 ⇒ warn"一条。

| 指标 | 开工 | 试验 2 |
|---|---|---|
| `gate --check` | block=0 warn=136 advice=5 | **block=0** warn=**136（存量零新增 ✓）** advice=**8（+3）** |
| `tests/test_gate_engine.py` | 49 全绿 | **2 例失败**：`test_assert_universal_symbol_blocks`、`test_assert_universal_symbol_blocks_even_if_in_artifact` |

失败原因（**这是本轮最有价值的发现**）：**同一条 `artifact_assert` 条目上有两条重叠路径**——
① 既有的"通用符号 ⇒ `bad_universal` ⇒ block"（`:1599-1621` + `:1645`）；
② 我新增的"非锚定 kind + 通用文本 ⇒ warn"。
两者会**并发命中同一张卡**，既有测试的精确期望集合被打散（block 之外多出一条 warn）。
⇒ 正确修法不是"再加一条分支"，而是**把新 warn 与既有 block 路径做互斥/合并成单点判定**
（同一条目已被 block 就不必再出 warn；或统一到一处按 kind+severity 出一次）。

### 结论与下一步（精确，照做即可）

1. **回退已完成**（`git checkout -- tools/gate_engine.py`），仓库与开工逐字一致、零半成品。
2. 下一轮 T0 的正确形状：
   - 在**同一处**判定：先按既有 `bad_universal` 出 block（不变）；**仅当该条目不进 block 时**，
     对非锚定 kind（`contains`/`contains_any`/`absent_any`）+ 通用/恒真文本出 **warn**（互斥）；
   - 空/纯中文 text 的 block **必须保持只对 `contains_in/absent_in`**（否则复现试验 1 的 38 命中）；
   - 配两例毒样例（M4 `.file` 注入、M3 `contains_in→contains` 降级）+ 既有 49 例全绿；
   - 复跑 `mutation_fuzz.py --limit 2 --operators M2,M3,M4,M5,M6` 验证 M4×2 收口；
   - `gate_engine.py` 被 `.tool_checksums` 钉住 ⇒ 改完 `tool_integrity.py --update` 重钉。
3. **M3 的 4 例另有半壁**：`contains_in → contains` 降级要判"该断言在工件**全区间**都成立"，
   这需要**工件侧**数据（`_assert_haystack` / `_discriminative_span` 可复用），
   **单靠 text 侧检查抓不到**（text 侧只看字面量本身）。下一轮请把这条与 §2 的互斥改造一起做。

## 2. T1 · mutation_fuzz 按卡批性能重构 —— 未做

上批已确认的现状（复述，避免重复侦察）：分算子 `--operators` 与"只 M1/M7 跑 replay"（`REPLAY_OPS`）**都已实现**；
真大头是**每个变体跑一次完整 `ge.run()` 全库扫描**。541 §T1 的三条（按卡批处理 / 算子分组合并报告 / cppbible 接入）**本会话未动**。
建议顺序：**先做 T0 的互斥改造（小、可验证）**，再做 T1 的按卡批重构（要拆 `ge.run()` 的按目标入口，改动面比 T0 大）。

## 3. 交人项 / 未做清单

1. **T0 未落地**（两次试验均触发存量误伤或既有测试冲突，已回退）——修法与验收在 §1.3，属"小改动但需一次改对"，请下轮优先。
2. **T1 未做**（按卡批性能重构 + `cppbible mutation` 接入）。
3. mutation smoke 本轮**未复跑**（T0 未落地 ⇒ 复跑无意义；开工数字已记在 §0）。
4. 本批 **0 commit**；本地仍 **ahead 16 个提交（未 push）**。
