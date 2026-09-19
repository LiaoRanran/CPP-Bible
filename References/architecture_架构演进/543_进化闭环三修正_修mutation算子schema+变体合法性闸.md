# 543 · 进化闭环三（修正版）：修 mutation 算子 schema + 变体合法性闸，gate 原则上不动

> 你是建设苦力。**542 已作废**——监工红队实测证明：上批以为的"M4 门禁逃逸"是 mutation_fuzz **算子自己字段写错**造出的假逃逸。本批主战场是**修 mutation_fuzz 自己**，gate_engine 原则上零改动（只有 P3 可能轻触）。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`f034d2c`。门禁用 `.venv\Scripts\python.exe`。动手前 Read 源码，规格与磁盘冲突以磁盘为准记 worklog。

## 监工已实测钉死的事实（照做，别再重新怀疑 gate）
`gate_engine._assert_targets` 的 kind→字段映射：
- `contains`/`absent` → 读单数 **`text`**
- `contains_any`/`absent_any` → 读**复数 `texts`（列表）**
- `contains_in`/`absent_in` → 读 **`symbol`（区间选择器）**，text 是被检索文本
- `call_count` → 读 `symbols`
实测：
- 合法 `{kind:contains_any, texts:['.file']}` → 取到 `.file`、`_is_universal_symbol('.file')=True` → 主路径 1645 **block（gate 本就拦得住）**。
- M4 算子实际注入 `{kind:contains_any, symbol:main, text:'.file'}`（单数 text）→ `_assert_targets` 取空 → 1604 `if not texts: continue` 跳过 = **假逃逸**。
- `je/main/call/ret/.file` 均 universal；`mov/lock` 不是。

## 开工基线（亲手量）
gate（60 / block=0 / warn=136 / advice=5）、poison 90/90、replay confirm=56、fast pytest 约 280（含 slow mutation 5 例）。mutation smoke：`--limit 2` escaped 12（**其中 M4 的 .file 是假逃逸，本批要剔除**）。

---

## P0 · 修 mutation 算子的字段正确性（核心）
1. Read `tools/mutation_fuzz.py` 的 `mut_m4`（及全部 `mut_m1..mut_m7`）。
2. **M4 修正**：`contains_any/absent_any` 注入必须用复数列表 `texts: ['.file']`，不许用单数 `text`。其余三个 contains_in 注入保留（它们字段对、symbol=main/call 本就该被 block，是有效反例）。
3. **全算子字段审计**：逐个对齐上面的 kind→字段映射，凡注入/改写 artifact_assert 的算子，生成的字段名必须与 `_assert_targets` 一致；列出审计表（哪个算子、生成什么 kind、用了什么字段、对不对）写进 worklog。
独立 commit。

## P1 · 变体合法性自检闸（防止再出假逃逸污染拦截率）
1. 每个变异变体在判决前，过一道**有效性校验**：用 `_assert_targets`（或等价 schema 检查）确认被变异的 artifact_assert 仍能取到**非空 targets**；字段名写错/断言被掏空的，判 **`n_a(malformed)`**——既不算 blocked 也不算 escaped，不进拦截率分母/分子。
2. 报告里把 malformed 单列一类，和现有 n_a（解析失败/infra）区分标注。
3. 加 pytest：构造一个"单数 text 的 contains_any"废变体，断言它落 `n_a(malformed)` 而非 escaped（把这次的教训钉成回归锁）。
独立 commit。

## P2 · 重算真实拦截率（闭环证据）
P0/P1 完成后重跑 `mutation_fuzz.py --limit 2`：
- M4 的 `.file` 假逃逸应消失（合法形态被 block / 或废形态落 malformed）；
- **escaped 从 12 下降，逐条重新定性**：剩下的每个 escaped 挂"卡 id/算子/为什么合法形态下仍逃逸"，写进 worklog。**不许为了数字好看把真逃逸判成 blocked。**
独立 commit（报告落 data/mutation/，注意 gitignore 口径）。

## P3（可选，唯一可能轻触 gate 的地方）· M3 区间降级真洞
真洞定性（监工实测）：`contains_in{symbol:区间, text:标签}` 被 M3 改成 `contains{text:标签}` 后，标签在全文有出处→放行，但"必须在 symbol 指定函数区间内"的约束丢了，主路径只验 text 出处、不验区间锚定被删。
- 若做：在 gate 第二路径（约 1630）**只对"全文 contains/absent 且其 text 是本机标签、却丢了区间锚定"**这一窄情形出 **warn**（不是 block）。
- 严守 541 教训：空/纯中文 block 只对 `*_in`；先量存量 56 卡命中数；**block 保持 0、warn 136 增量如实报**；配正反例毒样例；改 gate_engine 必 `tool_integrity.py --update` 重钉校验和。
- 上下文不够就**留 worklog 不做**，绝不为做它破坏 P0-P2。

## P4 · mutation 按卡批性能（541/542 遗留，时间够再做）
真大头是每变体跑一次完整 `ge.run()` 全库扫描。改为一卡全部变体共用一次基线扫描、只 diff `Finding.target==该卡`。
⚠️**红线**：ge.run 含**跨卡规则**（EV-ID-UNIQUE/serves/relations），变异卡可能让 finding.target 指向别的卡——只 diff 本卡 target 会漏掉跨卡逃逸。故按卡批优化时，跨卡规则那部分仍需对变异副本单独判，不许为提速牺牲跨卡正确性。补 `cppbible mutation` 子命令。验收：`--limit 2` <1 分钟且**判决数字与优化前一致**。

---

## 收工
fresh 全量门禁终值；重跑 mutation smoke 对比（修前 escaped 12 → 修后多少、其中 malformed 多少、真 escaped 多少，三数分开报）；写 `_worklog_543.md`（P0 字段审计表、P1 闸实现、P2 逐逃逸定性、P3 存量命中、每条 commit）。
**不 push、不 --no-verify、不 golden accept；本批重点是修 mutation 自己、gate 能不动就不动；变异只在 tempfile、原卡零改动。做不完停在 P 边界。**
