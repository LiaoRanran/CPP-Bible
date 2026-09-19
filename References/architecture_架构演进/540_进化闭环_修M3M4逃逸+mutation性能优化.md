# 540 · 进化闭环第一批：修 mutation 扫出的 M3/M4 逃逸 + mutation_fuzz 性能

> 你是建设苦力。上一批 mutation_fuzz（L3 自动变异器）首跑扫出 12 个逃逸，这批把其中最高价值的两个补成门禁规则，再把变异器性能提上来——这是"机器扫逃逸 → 门禁补上 → 拦截率上涨"进化闭环的第一圈。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`f034d2c`。门禁用 `.venv\Scripts\python.exe`。**动手前先 Read 目标源码（行号漂移），规格与磁盘冲突以磁盘为准并记 worklog。**

## 开工基线（亲手量）
gate（60 规则 / block=0 / warn=136）、poison（90/90）、replay（confirm=56）、`pytest -m fast -q`（约 280）。
另记 mutation_fuzz smoke 现状：`tools/mutation_fuzz.py --limit 2` ≈28 变体 / blocked 14（严格 13）/ escaped 12 / n_a 2，严格拦截率 46.2%。**修完要复跑同一条，escaped 应明显下降**——这是本批核心验收。

---

## T0（最高优先）· M3+M4：扩展恒真/判别力检测到 contains/contains_any

### 背景（mutation 首跑实证，不是猜）
- **M4**：卡内写 `contains_any: ['.file']` → 漏网。`.file` 是 `g++ -S` 产物**每行都有的恒真伪指令**，断言必然成立、零判别力。
- **M3**：把区间断言 `contains_in: X` 降级成全文 `contains: X`，判别力从"锚定函数区间"掉到"全文任意位置"，且**无人告警**——比漏报更坏。
- 两者同族：**断言的目标符号在工件里"到处都是"，断言就没有判别力**。

### 修法（扩展现有机制，别新造规则）
1. **先 Read**：530 已有的恒真符号判别（`gate_engine.py` 里 UNIVERSAL_SYMBOLS / 帧伪指令 `.p2align/.seh_endproc/.cfi_startproc` 那套），以及 533 E03 的"contains_in 目标在所有区间出现 → 恒真"检测。
2. **扩展 1：黑名单补 `.file`**（及同类 gcc 恒真伪指令，如 `.def/.endef/.ident/.section` 等先列最小集，别一次堆太多误伤）——进现有恒真符号判别。
3. **扩展 2：判别力检测从 contains_in 扩到 contains/contains_any**——同一思路：统计目标符号在**整个工件**的出现次数；若它在工件中"处处出现"（如 N≥阈值且无函数区间边界区分），判为**判别力弱** warn。
4. **M3 专门点**：若一张卡同一命题上同时/等价使用全文 `contains`，而该断言在工件全区间都成立 → warn "全文存在性断言，判别力弱（考虑 contains_in 锚定区间）"。
5. **先 warn 不 block**：存量 56 卡可能本就用了弱 contains，先量命中数；`.file` 这种明确恒真伪指令可直接 block。配正反例毒样例（escaped 的 M3/M4 变体改造成"应被拦"的毒样例）。

### 验收
- 复跑 `mutation_fuzz.py --limit 2`：**M3/M4 的逃逸从 6 个降到接近 0**（M2 路径类本批不修，仍 escaped，预期内）。
- gate 新 warn 量如实报（多少存量命中），不擅自 --accept。
- 配 poison 毒样例 + pytest；gate/poison/replay/pytest fast 零误伤（存量 block 数不增、replay confirm=56）。
独立 commit。

---

## T1 · mutation_fuzz 性能优化（让全量可跑）
现状：--limit 2 就 >4 分钟（每变体跑整轮门禁 + M1/M7 replay），全量 392 变体不现实。照做：
1. **分算子跑**：`--operators M1,M2,M3` 已支持则确认；默认 `--limit 5`、全量用显式 `--full`。
2. **只 M1/M7 跑 replay**：确认 REPLAY_OPS 逻辑——M2/M3/M4/M5/M6 纯 gate 不跑 replay（它们不碰工件字节），把耗时大头砍掉。
3. **基线缓存**：同一基线卡的 gate/replay 结果缓存一次，变异变体只重跑差异项；smoke 模式不写 data/。
4. **接入 cppbible**：补 `cppbible mutation` 子命令（B3 末条遗留），模式照 poison/cost。
### 验收
- `--limit 2` 从 >4 分钟降到 <1 分钟量级；`--limit 5` 能在一批会话内跑完并落报告。
- 变体数/拦截率口径与优化前**完全一致**（性能优化不许改变判决结论）——优化前后同 smoke 跑一遍对比数字应相同。
独立 commit。

---

## T2（P2，时间够再做）· M2 跨平台路径弱检测
卡内证据/夹具路径声明用异体写法（大小写/./反斜杠），Windows 能开、Linux CI 找不到文件。加一条 **warn**（不 block）：发现路径写法非规范 posix 或含 `/./` 时提示"跨平台可移植性风险"。只记录、不阻断。配 1 例 pytest。独立 commit（时间不够就留 worklog）。

---

## 收工
fresh 全量门禁报实测终值；复跑 mutation smoke 对比修前（escaped 12 → 多少）；写 `_worklog_540.md`（T0 新 warn 命中数、T1 优化前后耗时与口径一致性、每条 commit、交人项）。
**不 push、不 --no-verify、不 golden accept、不改 56 卡信任结论；新规则先 warn 后 block；mutation 变异只在 tempfile，原卡零改动。做不完停在 T 边界。**
