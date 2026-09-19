# 541 · 进化闭环二：钉死 M4/M3 根因扩判别力覆盖 + mutation 按卡批性能重构

> 你是建设苦力。上一批侦察+监工已把 M4 逃逸根因**钉死**（不是黑名单、不是解析截断，是 kind 门控），本批照精确定位动刀。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`f034d2c`。门禁用 `.venv\Scripts\python.exe`。

## 开工基线（亲手量）
gate（60 规则 / block=0 / warn=136）、poison（90/90）、replay（confirm=56）、`pytest -m fast -q`（约 280）+ slow 组 mutation 5 例。mutation smoke 现状：`--limit 2` ≈28 变体 / escaped 12（M2×6 / M3×4 / M4×2）。

---

## T0（最高优先）· gate_engine.py 判别力检查扩 kind 覆盖（根因已钉死）

### 根因（监工已实测复跑，照做即可，别再分辨）
- `.file` 注入变体**确实进了 `meta["artifact_assert"]`**（监工复跑确认：解析没截断，第一条就是 `{kind:contains_any, symbol:main, text:.file}`）。
- 逃逸根因：`gate_engine.py` 判别力 text 侧检查（约 1630 行）有行 `if kind not in ("contains_in","absent_in"): continue`——**`contains`/`contains_any` 被直接 continue 跳过**。`.file` 出现在 text 字段，而查 text 判别力那段不认这俩 kind，于是恒真文本零检查。

### 修法（精确到行）
1. Read `gate_engine.py` 约 1599-1645 行，看清两条路径：
   - 通用符号恒真拦截（约 1599-1621，遍历 artifact_assert、`_is_universal_symbol` 进 bad_universal ⇒ block）；
   - text 侧判别力检查（约 1630-1644，目前 `if kind not in ("contains_in","absent_in"): continue`）。
2. **把第二处的 kind 白名单从 `("contains_in","absent_in")` 扩到 `("contains","contains_in","contains_any","absent_in","absent_any")`**——让 contains/contains_any 也走 text 判别力。
3. 该检查内的既有分支（空 text→block / 纯中文→block / 通用助记符→advice / 全区间出现→判别力弱 warn）对扩进来的 kind 同样生效。`.file` 这类 gcc 恒真伪指令应落到"恒真/判别力弱"分支。
4. **先 warn 后 block 判据**：空/纯中文 text 维持 block；`.file` 等恒真伪指令若在存量 56 卡有命中，先量数、按 warn 观察（铁律：新规则先 warn 不直接 block，除非明确恒真）。
5. **M3 专点同处落地**：同命题用全文 `contains` 且该断言在工件全区间都成立 ⇒ warn「全文存在性断言，判别力弱，建议 contains_in 锚定区间」。

### 验收
- 复跑 `mutation_fuzz.py --limit 2`：**M4 的 2 个、M3 的 4 个逃逸应收口为 blocked/warn**（M2 路径类本批不修，仍 escaped，预期内）。
- 配正反例毒样例（M4 `.file`/M3 contains_in→contains 各一条应被拦）+ pytest。
- gate 新 warn/block 数如实报；**`gate_engine.py` 被 `.tool_checksums` 钉住，改完必须按流程重钉校验和**；poison/replay/fast+slow pytest 全绿、存量 56 卡 replay confirm=56 零误伤。
独立 commit。

---

## T1 · mutation_fuzz 按卡批性能重构（真大头）
上批已确认：分算子/只 M1/M7 跑 replay 都已实现；**真大头是每个变体跑一次完整 `ge.run()` 全库扫描**。照做：
1. **按卡批处理**：一张卡的全部变体共用一次基线扫描，只 diff `Finding.target == 该卡` 的部分，别每个变体都全库扫。
2. 算子分组合并报告（多算子跑完合并成一份 JSON）。
3. 补 `cppbible mutation` 子命令接入（模式照 poison/cost）。
### 验收
- `--limit 2` 从 >4 分钟降到 <1 分钟量级；**判决结论数字与重构前完全一致**（提速不许改结论——前后各跑一遍同 smoke 对比 escaped 数应相同）。
独立 commit。

---

## 收工
fresh 全量门禁报实测终值；复跑 mutation smoke 对比（修前 escaped 12 → T0 后多少）；写 `_worklog_541.md`（T0 新规则存量命中数、T1 前后耗时与口径一致性、每条 commit、交人项）。
**不 push、不 --no-verify、不 golden accept；新规则先 warn 后 block；改 gate_engine 必重钉校验和；mutation 变异只在 tempfile。做不完停在 T 边界。**
