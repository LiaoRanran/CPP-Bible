> ⚠️【本提示词已作废，勿投喂】监工红队实测推翻其前提：M4「.file 逃逸」是 mutation_fuzz 算子字段错配（contains_any 应用复数 texts，算子写成单数 text）造成的**假逃逸**；合法形态下 gate 主路径本就 block（universal(.file)=True），gate_engine 无需改。正确任务见 543。
>
# 542 · 进化闭环三：判别力扩覆盖（两路径互斥收口版）+ mutation 性能【作废】

> 你是建设苦力。541 两次试验均触发存量误伤已干净回退（仓库零残留），并挖到真因：**同一条 artifact_assert 条目上两条判定路径重叠**。本批按 `_worklog_541.md §1.3` 的精确形状动刀，别再天真扩白名单。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`f034d2c`。门禁用 `.venv\Scripts\python.exe`。

## 开工基线（亲手量，与 541 回退后逐字一致）
gate（60 规则 / 141 命中 / block=0 / warn=136 / advice=5）、poison（90/90）、replay（confirm=56）、`tests/test_gate_engine.py` 49 例全绿、fast pytest 约 280。

---

## T0 · 判别力 kind 覆盖（带互斥收口，三次纪律）

### 三次已验证的雷，照着绕
1. **空/纯中文 text → block，必须保持只对 `contains_in/absent_in`**——扩到含 contains/contains_any 会把存量散文文本判成 block（541 试验 1：block 0→38）。
2. **同一条目已被 block 就不要再出 warn**——既有"通用符号→bad_universal→block"与新增"非锚定 kind+通用文本→warn"重叠命中同卡，打散既有测试（541 试验 2：advice 5→8、2 测试红）。
3. **新纳入 kind 只加"恒真/通用文本 → warn"，不动 block 分支**。

### 做法
1. Read `gate_engine.py` 约 1599-1645 行，看清两条路径（通用符号 block 路径 / text 判别力 warn 路径）。
2. text 判别力检查的 kind 白名单扩到 `("contains","contains_in","contains_any","absent_in","absent_any")`，**但**：
   - "空/纯中文 → block"分支**仅对 `*_in` 生效**（对新扩的 contains/contains_any 不触发 block）；
   - 对新扩的 contains/contains_any，只跑"恒真/通用文本（.file 等 gcc 伪指令）→ warn 判别力弱"分支；
   - **互斥收口**：同一 artifact_assert 条目若已被 block 路径命中，则抑制该条目的 warn（或按 kind+severity 合并只出一次最高级），杜绝 541 试验 2 的双命中。
3. 配两例毒样例：M4 注入 `.file` 应 warn、M3 contains_in→contains 降级应 warn；**既有 49 例 gate 测试不得打散**（541 试验 2 打散的那两例期望要对着互斥收口重新核对，不是改测试凑数）。
4. **改完 `tools/tool_integrity.py --update` 重钉校验和**（gate_engine 被钉住）。

### 验收
- gate 新 warn 数如实报；**block 必须保持 0、存量 warn 136 不增**（541 试验 2 已做到存量零新增，保持）。
- 复跑 `mutation_fuzz.py --limit 2 --operators M2,M3,M4,M5,M6`：**M4 的 2 个逃逸应收口为 warn**（M2 路径类仍 escaped，预期内）。
- poison 90/90、replay confirm=56、fast+slow pytest 全绿、tool_integrity OK。独立 commit。

---

## T1 · M3 工件侧判别力（第二刀，时间够再做）
text 侧只看字面量抓不到"全文存在性"。复用 `_assert_haystack` / `_discriminative_span`，数目标在工件全区间的分布：若全文 `contains` 的目标在工件各区间都成立（无区间锚别）→ warn「判别力弱，建议 contains_in 锚定」。先 warn 不 block。配 1 例毒样例 + pytest。独立 commit（不够就留 worklog）。

---

## T2 · mutation_fuzz 按卡批性能重构（541 未动）
真大头是每变体跑一次完整 `ge.run()` 全库扫描。照做：
1. 按卡批处理：一卡全部变体共用一次基线扫描，只 diff `Finding.target == 该卡`。
2. 补 `cppbible mutation` 子命令接入（模式照 poison/cost）。
### 验收
- `--limit 2` 从 >4 分钟降到 <1 分钟；**前后判决 escaped 数完全一致**（提速不改结论）。独立 commit。

---

## 收工
fresh 全量门禁终值；复跑 mutation smoke 对比（修前 escaped 12 → T0 后多少）；写 `_worklog_542.md`（T0 互斥收口怎么实现的、新 warn 存量命中、T2 前后耗时、每条 commit、交人项）。
**不 push、不 --no-verify、不 golden accept；新规则先 warn 后 block；改 gate_engine 必重钉校验和；两路径互斥是本批灵魂，别再天真扩白名单。做不完停在 T 边界。**
