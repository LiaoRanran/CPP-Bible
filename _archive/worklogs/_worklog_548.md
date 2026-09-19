# 548 建设日志：mutation 日常化 + 全量逃逸基线收口

> 依据：`References/architecture_架构演进/548_系统证据收集与优化大轮_mutation日常化全量逃逸基线收口.md`
> 纪律：不 push / 不 golden accept / 每个 Part 独立 commit / 先量后改 / 收工前跑全量门禁 / 做不完停在 Part 边界。

## 幂等进度看板

```
Part 0 mutation 速度与跑法（按卡批 + 解析缓存）        [x] ed3dff3
Part 1 全量逃逸基线 v1（83 卡 × 7 算子 = 1188 变体）  [x] 31bb219
Part 2 M2 路径规则收口（CARD-PATH-NOT-CANONICAL）      [x] 1b3ff12 + 96fbfeb（自查修正）
Part 3 治理文档接线（L3 定位 + 基线指针）              [x] 96fbfeb
收工：门禁复跑 + 本文件                                [x] 本文件（含 d06c224 ruff 修正）
```

提交序列（本地、未 push）：`ed3dff3` → `31bb219` → `1b3ff12` → `96fbfeb` → `d06c224`。

## 0. 开工基线（HEAD=`7ee082b`，亲手实测）

| 项 | 实测 |
|---|---|
| `mutation_fuzz.py --limit 2`（全算子） | **99.2s** · 37 变体 · blocked 24（严格 22）· escaped 11 · n_a 2 · 严格率 62.9% |
| 单次全库扫描 `ge.run()`（温） | **2.43s**（cProfile：`_meta` 被调 **2475 次**，占 ~2/3） |
| 单次 `replay_card` | 1.32s（M1/M7 每变体一次） |
| 全量变体数（83 卡 × 7 算子） | **956** 个进判决（+232 条 n_a 行） |
| gate / poison / replay | 规则 60 · 命中 141（block=0 warn=136 advice=5）· poison **90/90** · confirm=56 |
| `pytest -m fast` | 290 项绿 |

改前全量外推：`956 × 2.68s + 139 次 replay × 1.3s ≈ 2742s ≈ 46 分钟`（未实跑，见 §5.4）。

## 1. Part 0 · 速度与跑法（`ed3dff3`）

### 1.1 改点

| # | 改点 | 说明 |
|---|---|---|
| 1 | `gate_engine._meta` **解析缓存** | 键 `(path, mtime_ns, size)`；命中即返回。**纯性能，不改判决**（cProfile 实测 `_meta` 单次扫描被调 2475 次 = 56 张卡被 ~44 条规则反复解析） |
| 2 | `gate_engine._fm_hardening_hits` **硬化命中缓存** | 同键；把 `check_frontmatter_hardening` 的内层循环体原样抽出（**逻辑一字未改**），只加一层按卡缓存（pyyaml `safe_load` 是第二热点，1.3s/83 卡） |
| 3 | `clear_meta_cache()` | 两个缓存的显式失效口子（给测试与"进程内改盘"场景） |
| 4 | `run_fuzz` **按卡批** | 卡维外层；全库基线**整轮只扫 1 次**；每张卡跑完统一还原沙箱副本（原先是每变体还原一次——多余写盘） |
| 5 | replay 按卡批省 | M1/M7 变体若**门禁已严格拦截** ⇒ 跳过 replay（replay 只可能往 `new_block` 再加一条，**verdict 不变**）；门禁没拦或只 warn ⇒ **照跑**（543 P0 的教训：只看 gate 会把"删必需字段"判成逃逸） |
| 6 | `cppbible mutation` 子命令 | `--all/--cards/--operators/--limit/--report/--out/--fail-on-escaped` 透传 |
| 7 | `--progress` + 报告扩维 | 逐卡进度打到 stderr（全量轮不许静默十分钟）；报告加 `by_operator/by_card/elapsed_s/ge_runs/replay_runs/replay_skipped` |
| 8 | 顺手修一处真缺陷 | `main()` 打印报告路径用 `relative_to(ROOT)`，`--report` 给仓库外绝对路径时**直接抛 ValueError**（cppbible 透传即触发）⇒ 改为 try/except 兜底 |

### 1.2 提速实测（同口径）

| 口径 | 改前 | 改后 | 倍数 |
|---|---|---|---|
| 单次全库扫描（温） | 2.43s | **0.49s** | 5.0× |
| `--limit 2`（2 卡 × 7 算子 = 37 变体） | 99.2s | **24.1s** | 4.1× |
| 全量（1188 变体） | 外推 ≈2742s | **659.7s（11 分钟）** | **≈4.2×** |

### 1.3 结论一致性对账（**硬约束：只许变快，不许变结论**）

拿改前的 `data/mutation/before_548.json` 与改后的 `after_548_smoke.json` **逐变体**对账
（键 = 卡 + 算子 + 变异点 + verdict + kind + 门禁规则 id 集合 + warn 规则 id 集合）：

```
same_order_and_len True   identical True   diff []
replay 字段数 before/after = 9 / 5（差的 4 条 = 门禁已 strict 拦截而跳过的 replay，verdict 不变）
```

### 1.4 回归锁（`tests/test_mutation_fuzz.py` +6，slow 组）

| 锁 | 钉住什么 |
|---|---|
| `test_548_perf_conclusions_unchanged` | 冻结基线（M3/M4 逐变体 verdict/kind/规则 id）**逐字一致**；`ge_runs == 1 + 变体数`（一次不多一次不少） |
| `test_548_diff_is_not_card_scoped` | 注入一条**别的卡**上的 block ⇒ 必须被算作 blocked（证明 diff 没被"按卡裁剪"） |
| `test_548_replay_runs_only_when_it_can_change_verdict` | 门禁已拦 ⇒ replay 不跑；门禁没拦 ⇒ replay **必须**跑 |
| `test_548_meta_cache_is_transparent` | 缓存值 == 现解析值；**改盘即失效**（不许拿旧 frontmatter 判决） |
| `test_548_gate_findings_stable_across_warm_cache` | 冷/温两次全库扫描**逐字一致**（缓存若被规则改写会现形） |
| `test_548_cppbible_mutation_subcommand` | CLI 接线 + `--out` 仓库外路径（就是 §1.1-8 那个真缺陷） |

> 为什么冻结基线只取 M3/M4：Part 2 的路径 warn 会**故意**改变 M2 的结论，不能混进"性能对账"锁。

## 2. Part 1 · 首份全量逃逸基线（`31bb219`）

落盘：`data/mutation/full_baseline_v1.json`（逐变体 + 复现命令）+ `data/mutation/README_v1.md`
（方法、口径、每类逃逸定义、复跑与对账命令）。

| 项 | 数 |
|---|---|
| 卡 / 算子 / 变体 | 83（56 证据 + 27 原子）/ 7 / **1188** |
| blocked / escaped / n_a | 729（严格 **615**，warn_only 114）/ **227** / 232（**malformed 0**） |
| 严格拦截率 / 含 warn 处置率 | **64.33%** / **76.26%** |
| 全库扫描 / replay / 跳过 | 957 / 65 / 139 · 耗时 **659.7s** |

**按算子**：M1 64/1/27 · **M2 0/207/14** · M3 2/11/75 · M4 200/0/33 · M5 0/0/83（恒 n_a）·
M6 324/8/0 · M7 139/0/0（blocked/escaped/n_a）。

**逃逸逐类定性（每一条都有归属，不许"227 条不明"）**：

| 类 | 条数 | 定性 | 去向 |
|---|---|---|---|
| M2 ×3 形态（大写 / `./` / 反斜杠） | 207 | **真逃逸（跨平台）**：Windows 三种写法都打得开、Linux CI 找不到 | Part 2 收口 |
| M3 `contains_in→contains` / `absent_in→absent` | 9 | 真逃逸（区间约束丢失），543 已知清单 | 留"单点互斥判定" |
| M3 去 `-Werror` | 2 | 真逃逸（"零诊断"不可判定） | 同上 |
| M6 块式 → flow（`matrix`） | 8 | **本轮新发现**：门禁对**形态**零要求 | 交人裁决（允许 flow 还是要求块式） |
| M1 删 `negative_controls` | 1 | 真逃逸（阴性对照缺闸门） | 待立规则（全库仅 1 张卡带该字段） |
| — | 0 | malformed / 解析失败 / infra_error | **本轮无假逃逸污染** |

## 3. Part 2 · M2 收口（`1b3ff12` + 自查修正 `96fbfeb`）

### 3.1 新规则 `CARD-PATH-NOT-CANONICAL`（warn）

判据（只读 `fixture` / `artifact` / `run_match_file` / `artifacts` 四个字段）：
① 含反斜杠分隔符；② 含 `./` 或 `..` 段；③ **大小写与磁盘逐字不符**（沿盘逐级比对）。
绝对路径 / URL 不在口径内；盘上不存在的路径**不判**（那是 `EV-ARTIFACT-FILE-EXISTS` 的活）。

**为什么只 warn**：路径写法是**形态约定**不是事实缺陷（文件确实在、内容确实对）；
存量 83 卡实测 **0 命中**（零误伤）；541 已实测"形态类规则直接升 block 会撞存量"。

### 3.2 配套

- 毒样例 **P69**（正：`EXAMPLES/ATOMS/P69.CPP` ⇒ warn；阴：逐字一致的 posix ⇒ 放行）+ `ATTACK_TYPES` 登记 `("P69 ", "A2")`；台账 `tools/poison_surface_map.json` 已重算落盘。
- pytest：`tests/test_gate_engine.py` +2（异体三形态 ⇒ warn / 规范 ⇒ 零命中；**真实仓库存量零命中**锁）。

### 3.3 收口数据（M2 专项全量复跑）

| M2 | Part 2 之前 | Part 2 之后 |
|---|---|---|
| blocked | 0 | **141**（全 `warn_only`，严格 0） |
| escaped | 207 | **66** |
| n_a | 14 | 14 |
| 含 warn 处置率 | 0% | **68.1%** |

**剩余 66 条不是洞**：M2 取"卡内第一个带 `/` 的路径"，而 22 张卡的第一条路径在
**注释/正文**里（门禁从不读那些位置）⇒ 属**"变异点无效"**。抽验：`EV-CONC-001` 的路径写在
`# 可核对锚 1` 注释里，`fixture:` 字段本身没被 M2 触及。

### 3.4 自查抓到的性能坑（**新规则自己成了瓶颈**）

第一版 `_path_case_mismatch` 用 `Path.iterdir()`：83 张卡 × 4 字段都要从 ROOT 走一遍，
而 ROOT 含 `.venv/build` 数百项 ⇒ **单次全库扫描 0.5s → 2.6s**（全量直接翻 4 倍）。
改 `os.listdir` + 单次调用内共享的**目录列表缓存**（不做跨调用缓存，避免"目录变了拿旧列表"）
⇒ 规则自身 0.59s → **0.07s**，全库扫描回到 **0.49s**。

## 4. Part 3 · 治理文档（`96fbfeb`）

| 文档 | 加了什么 |
|---|---|
| `docs/kernel/mutation_test_499.md` §六 | 从"手动 40 变异"到"自动全量基线"：基线数字 + 逃逸四类定性 + **L3 定位（发现器不参与门禁、不进 CI）** |
| `docs/kernel/S1_S6_controls.md`（S6 补充） | 与 poison 的边界、三分类口径、产物路径、处置（逃逸不阻断→定性交人裁决）+ **"逃逸分三类"**提醒 |

## 5. 偏差表（与本批任务书不一致处，逐条给理由）

| # | 任务书写法 | 实际做法 | 理由 |
|---|---|---|---|
| 5.1 | Part 0「对每个变体只 diff `Finding.target == 该卡` 的命中」 | **保留全量 diff**（不过滤 target）；提速改由解析缓存 + 按卡批 + replay 跳过实现 | 任务书同一段又写"跨卡规则（EV-ID-UNIQUE/serves/relations）单独整体跑、不许漏判"。按卡裁剪会让**落在别的卡上的**跨卡命中消失；而实现"部分运行"需要把规则拆成卡内/跨卡两批（动判决结构，风险更大）。实测 4.1× 已达标，且 `test_548_diff_is_not_card_scoped` 把该红线钉死 |
| 5.2 | 缓存是"提速"手段，未提失效 | 缓存键 `(path, mtime_ns, size)` + `clear_meta_cache()` 显式口子 | 门禁读的是**盘上内容**，缓存必须随盘失效；新卡（poison 沙箱）用新路径 ⇒ 天然不命中旧值 |
| 5.3 | 「命中数与 Part 1 的 M2×6 对账」 | 实测收口 **141** 条（不是 6 条） | 6 条是旧 `--limit 2` smoke 的量；全量是 83 张卡 ⇒ M2 逃逸 207 条。**口径升级而非矛盾** |
| 5.4 | 性能目标 `全量 < 现有 1/4` | 实测 **≈4.2×（659.7s vs 外推 2742s）**，达标；但"改前"是**外推**不是实跑 | 实跑旧代码全量要 ~46 分钟，为省机器未跑；外推用的 2.68s/变体是**实测**（`--limit 2` 99.2s / 37），并补上了旧代码不会跳过的 139 次 replay（1.3s/次）⇒ 偏保守 |
| 5.5 | Part 1 报告"变体 1188" | 报告行数 1188 ≠ 进门禁判决的 956 | 1188 含 232 条 n_a 行（无字段/空操作，其中 M5 恒 n_a 83 条）；报告里 `variants` 与 `ge_runs` 都单列，便于对账 |
| 5.6 | 大 JSON 落盘 | `full_baseline_v1.json` **不入 git**，只 `README_v1.md` 入库 | 体量大且是实测产物，与 543 的 `after_543.json` 同例；README 记"哪个 commit、什么命令、什么口径"生成，可复跑重建 |
| 5.7 | ruff 门禁 | CI 口径 `ruff==0.6.9`：**本批没新增**（新增过 1 项 F402 已修，见 `d06c224`）；余 4 项是 530 §6.8 记录的存量 | 存量债不在本批范围（改了会扩面） |

## 6. 收工实测（三条硬条件逐条对照）

| 条件 | 实测 |
|---|---|
| Part 0 后 `--limit 2` 结论与改前**逐字一致** | ✅ 逐变体 `identical True`、`diff []`（§1.3） |
| Part 1 基线落盘 + 每条 escaped 有定性 | ✅ `data/mutation/{full_baseline_v1.json,README_v1.md}`；4 类定性 + 每卡分布 + 复现命令 |
| Part 2 存量零误伤 + 正反例 + 与 Part 1 对账 | ✅ 存量 **0 命中**（pytest 锁 + 实测）；P69 正反例入 poison；M2 207→66（§3.3） |
| Part 3 文档接线 | ✅ `mutation_test_499.md` §六 + `S1_S6_controls.md` S6 补充 |
| gate 不回归 | `[gate] 规则 **61** 条 · 命中 **141** (block=0 warn=136 advice=5)`，exit 0（**命中数与基线逐字一致**——新规则存量 0 命中） |
| poison 不回归 | **92/92**（基线 90/90，+2 = P69 正反例）· RULE-COVERAGE **36/61**（基线 35/60）· 零覆盖攻击面：无 |
| replay 不回归 | `confirm=56 / refute=0 / infra_error=0` |
| pytest | `-m fast` **290 项绿**（exit 0）；受影响的两模块 `test_mutation_fuzz`(13) + `test_gate_engine`(123) 全绿 |
| ruff（CI 口径 0.6.9） | 改动文件**无新增**（余 4 项 = 530 §6.8 存量） |

## 7. 未做与交人项

1. **M3 未收口**（15 条里 11 条）：`contains_in → contains` 的**区间约束丢失**、去 `-Werror` 后
   "零诊断"不可判定。541 两次实测证明"直接扩 gate 白名单/升 block"会撞存量 ⇒ 正确形状是
   **单点互斥判定**（只对"全文断言 + 文本是唯一来源 ⇒ 区间语义被丢"出 warn），本批不做。
2. **M6 块式 → flow（8 条）交人裁决**：这是"允不允许 flow 写法"的**形态约定**，
   不是事实缺陷（两个解析器都读得对）——门禁不该替人做这个决定。
3. **M1 `negative_controls` 缺失无闸门**：全库只有 1 张卡带该字段 ⇒ 立规则的收益/风险都不明朗，
   先登记不动。
4. **M5 对这 83 张卡恒 n_a**：证据/原子卡没有 `claim_type` 字段 ⇒ 该算子在这批卡上**没有产出**。
   要有意义得换卡集（或让算子造字段），本批只如实单列。
5. **M2 的 66 条"变异点无效"**：建议下一轮改进算子——**只挑门禁真读的字段内路径**
   （现在取"全文第一个路径"，22/83 张卡会挑到注释/正文），否则"逃逸数"里永远混着无效提问。
6. **全量不进 CI**：11 分钟不适合每次门禁；建议"人在该体检时跑"（`cppbible mutation --all`），
   或按卡/按算子小批复现（报告里每条都带 `reproduce` 命令）。
7. **本批未 push**；`data/mutation/*.json` 未入库（见 §5.6）。
