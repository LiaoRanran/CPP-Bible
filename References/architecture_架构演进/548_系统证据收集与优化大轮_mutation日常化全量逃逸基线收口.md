# 548 · 系统证据收集与优化大轮：mutation 日常化 + 第一份全量逃逸基线 + 收口债（今晚最后一轮）

> 你是建设苦力。本轮不是加新规则，而是**把现有系统用真实数据摸一遍、把拖慢证据采集的瓶颈拆了、把已知债收口**。547 异族对抗尚未开打——你本轮只改 mutation 的**性能和跑法**，**不改判决逻辑**（malformed 闸/三分类/KIND_FIELD 保持 543 现状），这样 547 之后打的是优化后的新版。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD 以 `git rev-parse HEAD` 实测为准；门禁用 `.venv\Scripts\python.exe`。**先 Read 相关源码再改。**

## 开工基线（记你亲手量的数）
gate（60/block=0/warn=136）、poison 90/90、replay confirm=56、`pytest -m fast -q`（约 290）、`mutation_fuzz.py --limit 2` 当前耗时与 escaped/malformed/拦截率。先绿再动。

---

## Part 0 · mutation 性能：从"每变体全库扫"到"按卡批"（P0，前置）
**痛点**：现状每个变体都跑一次完整 `ge.run()` 全库扫描，`--limit 2` 已 >4 分钟，全量根本跑不完。
**改法（红线：不许为提速牺牲跨卡规则）**：
1. 按卡批处理：**一张卡的全部变体共用一次 ge.run() 基线扫描**，对每个变体只 diff `Finding.target == 该卡` 的命中；跨卡规则（EV-ID-UNIQUE/serves/relations/concepts 等）单独整体跑一遍、不按卡拆——**跨卡结论绝不能因为"只看本卡"而漏判**。
2. REPLAY_OPS={M1,M7} 的 replay 同样按卡批。
3. `cppbible mutation` 子命令接入（模式同 poison/cost），支持 `--all/--operators/--report/--out`。
4. 实测对比：同卡同算子，改前改后拦截结论必须**逐字一致**（拿 --limit 2 的旧报告对账，结论不同不许合并）。性能目标：全量 56 卡×7 算子 < 现有 1/4。
独立 commit + 性能回归锁（断言结论与基线一致、跨卡规则仍跑）。

## Part 1 · 第一份全量逃逸证据基线（P0，收集）
Part 0 完成后，**全量跑一遍 mutation**（全部卡×M1-M7），产出：
1. 逃逸分布：每算子 escaped 数、每卡 escaped 数、malformed 数，**严格拦截率与含 warn 处置率分开报**。
2. 把每条 escaped 定性：真逃逸 / malformed / 已知清单（M2 路径异体、M3 区间降级）——不许把 malformed 混进逃逸率。
3. 落盘 `data/mutation/full_baseline_v1.json` + 人读 `data/mutation/README_v1.md`（方法、口径、每类逃逸定义、复跑命令）。
**诚实第一**：跑出来多少报多少；性能若还是跑不完，如实报卡点，不要缩小样本凑数。

## Part 2 · M2 跨平台路径 warn（P1）
卡内 artifact/run_match_file 路径用异体写法（大小写、`./`、反斜杠混用、相对路径含 `..`）在 Windows 能开、Linux CI 会找不到。加一条 **warn 级**规则（不 block）：检测路径中非 posix 规范、或大小写与磁盘实际不符的，出 warn。
- 先量存量命中（预期就是已知 M2×6 那几条），存量零误伤是硬约束；命中数与 Part 1 的 M2×6 对账。
- 配毒样例正反例 + pytest；**只 warn 不 block**。
独立 commit。

## Part 3 · 已知逃逸登记 + 系统证据快照（P1，收集）
1. 把 M2/M3 及本轮新发现的真逃逸写进 `docs/kernel/known_semantic_escapes.md`：每条挂现象、为什么不归 L1 常态规则（541 撞存量的教训）、等什么收口（V-iso / warn 可见化 / 等模型）。**不要**为它们硬加 L1 block 规则。
2. 系统证据快照：实测并落盘一份"当前系统基线"（人读 `docs/kernel/system_baseline_v1.md`）：gate 规则数与 block/warn/advice 分布、poison 覆盖、replay 全量/增量耗时、pytest 数、mutation 全量拦截率、kg 节点/边/跨原子连通数、warn 136 逐条归因（哪条规则、哪些卡、能不能清零）。数字必须来自实跑，不许照文档自报。

---

## 收工
- Part 0/1/2/3 各自独立 commit；gate 判决逻辑零改动（只加 Part 2 一条 warn）。
- 门禁 fresh run：gate（block=0，warn 只增 Part 2 的 M2 命中）、poison 90/90、replay confirm=56、`pytest -m fast -q` 全绿；mutation 全量结论与旧 smoke 对账一致。
- 写 `_worklog_548.md`：性能改前改后耗时、全量逃逸分布、M2 命中数、证据快照要点、每条 commit。
**不 push、不 --no-verify、不 golden accept；做不完停在 Part 边界，不留半成品；547 即将在此版本上对抗，改完别再动 mutation 判决逻辑。**
