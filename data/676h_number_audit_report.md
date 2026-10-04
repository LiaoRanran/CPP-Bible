# 676h · 论文数字可追溯性审计报告

- 生成时间：2026-10-04T09:16:21+08:00
- 被审计稿件：`research/latex/queyi_neurips2027_v1.1.tex`（正文 None 页 / 全稿 29 页，取自编译日志）
- 权威源：14 个文件
- 检察条数：**118**，其中 consistent 113，硬 missing（active）0，软 missing（not_printed 等）4，skipped/no_source 0

## 0. 结论速览

**已有数字的逐条检察全部命中**（不一致率 = 0）。
待 676f/676g 数据就绪后刷新的检察：0 条（见 §3）。

## 1. 硬不一致清单（missing + active：源里有值、论文里必须出现却找不到）

（空）—— 论文里已有的数字逐条追到了权威源，且写法一致。

### 1b. 软登记：源里算了、论文没打印（not_printed / retired，非不一致）

| ID | 说明 | 状态 |
|---|---|---|
| D02b | A5 corpus 2000 次随机分布：FD 严格优于的比例与均值/标准差 | superseded_by_676f |
| I11 | corpus 分层 sanitizer 29/34 CI ⇒ [68.9, 95.0] | not_printed |
| I12 | corpus 分层 compiler-warn 9/18 CI ⇒ [26.0, 74.0] | not_printed |
| I13 | corpus 分层 cross-compile 2/12 CI ⇒ [2.1, 48.4] | not_printed |
| I14 | 缺陷重注入 6/6 CI ⇒ [54.1, 100.0] | not_printed |

### 1c. un-pinned 历史值（源不可得 / 口径已退役）

| ID | 说明 | 状态 | 处置 |
|---|---|---|---|
| K01 | tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现 | unpinned_no_artifact | 论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注） |
| K02 | tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径 | unpinned_retired_caliber | 该值口径已退休，只能作为“当时口径下读到的数”引用 |

## 2. 逐组概览

| 分组 | consistent | 其它 |
|---|---|---|
| A.核心三臂 | 19 | 0 |
| B.reveal | 10 | 0 |
| C.系统计数 | 12 | 0 |
| D.A5 | 6 | 1 |
| D2.A5-676f | 22 | 0 |
| D3.盲区地图 | 6 | 0 |
| E.外部工具 | 11 | 0 |
| F.LLM/锚点 | 5 | 0 |
| G.变异/注入 | 3 | 0 |
| H.样本量 | 6 | 0 |
| I.CI重算 | 10 | 4 |
| K.历史 un-pinned | 2 | 0 |
| N.诚实性反向检察 | 1 | 0 |

## 3. 待 676f / 676g 更新清单

依赖就绪状态：**676f `True` / 676g `True`**

| 依赖 | 文件 | 当前行数 | 需要 | 就绪 |
|---|---|---|---|---|
| 676f | `data/a5_676f_results.json` | 1 | ≥1 | True |
| 676f | `data/a5_676f_matrix_local.jsonl` | 673 | ≥1147 | False |
| 676f | `data/a5_676f_matrix_san.jsonl` | 1054 | ≥1147 | False |
| 676g | `data/blindspot_676g_stats.json` | 1 | ≥1 | True |
| 676g | `data/blindspot_676g_ckpt_san.jsonl` | None | ≥3126 | False |

| ID | 说明 |
|---|---|

## 4. 数字覆盖度（tex 全量扫描）

扫描到数字 token **1432** 个（已排除注释行与导言区行）。分类：

| 类别 | 数量 | 占比 |
|---|---|---|
| claim | 1197 | 83.6% |
| method_constant | 42 | 2.9% |
| format_layout | 36 | 2.5% |
| repro_command | 30 | 2.1% |
| unclassified | 25 | 1.7% |
| batch_id | 19 | 1.3% |
| design_constant | 16 | 1.1% |
| engineering_narrative | 11 | 0.8% |
| external_literature | 10 | 0.7% |
| structural | 9 | 0.6% |
| logic_constant | 9 | 0.6% |
| year | 8 | 0.6% |
| system_constant | 7 | 0.5% |
| historical_retired | 4 | 0.3% |
| sample_id | 4 | 0.3% |
| erratum_retired | 2 | 0.1% |
| thirdparty_audit | 1 | 0.1% |
| cited_context | 1 | 0.1% |
| external_regulation | 1 | 0.1% |

未归类 token：25 个（前 60 条见下；全量在 json 里）。

| 行 | token | 上下文 |
|---|---|---|
| 534 | `40` | `\caption{Caliber ablation on the external corpus: the \emph{same} 40 catches, three` |
| 983 | `30` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 983 | `17` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 996 | `5` | `/ advice 7} (total 67). By kind: fact 61 / pedagogy 5 / meta 1. Fields:` |
| 1140 | `2` | `runtime); the script re-derives them \emph{from landed artifacts} instead. (2) E9's driver script is` |
| 1405 | `200` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `219` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `149` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `95` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `99` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `90` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1405 | `88` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1468 | `2` | `2 & 45.1\% & 14.3\% & +30.7 & [+26.2, +35.3] & $7.8\times10^{-35}$ \\` |
| 1469 | `24.5` | `3 & 51.1\% & 30.6\% & +20.5 & [+16.5, +24.5] & $2.2\times10^{-22}$ \\` |
| 1469 | `2.2` | `3 & 51.1\% & 30.6\% & +20.5 & [+16.5, +24.5] & $2.2\times10^{-22}$ \\` |
| 1470 | `27.5` | `\textbf{4} & \textbf{54.6\%} & \textbf{30.6\%} & \textbf{+24.0} & [+20.5, +27.5] & $2.3\times10^{-41}$ \\` |
| 1471 | `5` | `5 & 59.4\% & 38.7\% & +20.7 & [+17.3, +24.0] & $1.2\times10^{-35}$ \\` |
| 1471 | `17.3` | `5 & 59.4\% & 38.7\% & +20.7 & [+17.3, +24.0] & $1.2\times10^{-35}$ \\` |
| 1490 | `2.7` | `real world & 44 & +29.5 & $5.4\times10^{-4}$ & $2.7\times10^{-3}$ \\` |
| 1491 | `2` | `optimization sensitive & 20 & +55.0 & $1.8\times10^{-3}$ & $1.1\times10^{-2}$ \\` |
| 1492 | `6.1` | `conditional trigger & 20 & +45.0 & $6.1\times10^{-3}$ & $4.3\times10^{-2}$ \\` |
| 1492 | `2` | `conditional trigger & 20 & +45.0 & $6.1\times10^{-3}$ & $4.3\times10^{-2}$ \\` |
| 1493 | `2` | `concurrency & 109 & +7.3 & $9.6\times10^{-3}$ & $8.6\times10^{-2}$ \\` |
| 1494 | `2` | `language semantics & 45 & +17.8 & $9.6\times10^{-3}$ & $8.6\times10^{-2}$ \\` |
| 1495 | `2` | `embedded & 74 & +8.1 & $3.4\times10^{-2}$ & $3.4\times10^{-1}$ \\` |

## 5. 每条检察的命中明细

**A01 · holdout 可测检出率 82.9% (34/41) CI[67.9,92.8]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `82.9` × 19 @ L59,433,479,485,495,497,511,549
  - ✓ `34/41` × 9 @ L59,433,607,814,835,901,988,1087
  - ✓ `67.9, 92.8` × 7 @ L60,486,495,814,835,901,988
**A02 · corpus 可测检出率 62.5% (40/64) CI[49.5,74.3]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `62.5` × 21 @ L61,433,479,486,495,498,511,513
  - ✓ `40/64` × 9 @ L62,434,608,624,814,835,901,1087
  - ✓ `49.5, 74.3` × 6 @ L62,486,495,814,835,901
**A03 · corpus 全样本口径 52.6%** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `52.6` × 8 @ L434,512,513,531,535,624,816,1250
**A04 · Static 臂 holdout 2.4% (1/41) / corpus 17.2% (11/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `2.4` × 7 @ L63,480,487,495,829,833,1508
  - ✓ `1/41` × 1 @ L833
  - ✓ `17.2` × 5 @ L63,480,487,495,833
  - ✓ `11/64` × 1 @ L833
**A05 · Random† 臂 holdout 9.8% (4/41) / corpus 21.9% (14/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `9.8` × 6 @ L64,481,488,495,834,1230
  - ✓ `4/41` × 1 @ L834
  - ✓ `21.9` × 5 @ L64,481,488,495,834
  - ✓ `14/64` × 1 @ L834
**A06 · Δ(Static→FD) holdout +80.5pp CI[68.4,92.6] p=2.3e-10 h=1.98** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+80.5pp` × 3 @ L63,496,836
  - ✓ `68.4, 92.6` × 1 @ L836
  - ✓ `2.3\times10^{-10}` × 1 @ L762
  - ✓ `1.98` × 2 @ L762,1036
**A07 · Δ(Random†→FD) holdout +73.2pp CI[59.6,86.7] p=1.9e-9 h=1.65** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+73.2pp` × 3 @ L65,496,837
  - ✓ `59.6, 86.7` × 1 @ L837
  - ✓ `1.9\times10^{-9}` × 1 @ L764
  - ✓ `1.65` × 1 @ L764
**A08 · Δ(Static→FD) corpus +45.3pp CI[33.1,57.5] p=3.7e-9 h=0.97** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+45.3pp` × 3 @ L64,496,836
  - ✓ `33.1, 57.5` × 1 @ L836
  - ✓ `3.7\times10^{-9}` × 1 @ L763
  - ✓ `0.97` × 2 @ L763,1034
**A09 · Δ(Random†→FD) corpus +40.6pp CI[28.6,52.7] p=3.0e-8 h=0.85** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+40.6pp` × 3 @ L65,496,837
  - ✓ `28.6, 52.7` × 1 @ L837
  - ✓ `3.0\times10^{-8}` × 2 @ L587,765
  - ✓ `0.85` × 1 @ L765
**A10 · 配对不一致对 (b, c)（tab:e5 四行）** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `(33, 0)` × 1 @ L762
  - ✓ `(29, 0)` × 1 @ L763
  - ✓ `(30, 0)` × 1 @ L764
  - ✓ `(26, 0)` × 1 @ L765
  - 注：四个对比都是 c=0 结构（对手的 catch 是 FD catch 的子集）
**A11 · 对照假阳性 0.0% (0/11)** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `0.0\% (0/11)` × 3 @ L835,964,1592
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
**A12 · 缺陷重注入 6/6 = 100%** — consistent/active `✓✗`
- 源：`data/current_numbers.json`
  - ✓ `6/6` × 3 @ L432,833,835
  - ✗ `100.0` × 0 @ L
**A13 · CP95 半宽 12.5pp（holdout）** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `12.5` × 3 @ L834,1309,1563
**A14 · 扩样前 holdout 81.0% (17/21) CI[58.1,94.6]** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `81.0` × 10 @ L60,497,511,512,549,552,674,815
  - ✓ `17/21` × 3 @ L60,498,987
**A15 · 扩样前 corpus 54.2% (26/48)** — consistent/active `✓✗`
- 源：`data/current_numbers.json`
  - ✓ `54.2` × 3 @ L498,674
  - ✗ `26/48` × 0 @ L
**A16 · H4 子集差额 corpus +33.3pp / holdout +4.0pp** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+33.3pp` × 1 @ L501
  - ✓ `+4.0pp` × 1 @ L500
**A17 · ±5pp 半宽所需样本量 holdout 236 / corpus 378** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `236` × 4 @ L911,964,1058,1063
  - ✓ `378` × 4 @ L911,964,1058,1063
**A18 · ±10pp 半宽所需样本量 holdout 61 / corpus 97** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `61` × 6 @ L908,964,986,996,1057,1561
  - ✓ `97` × 3 @ L964,1057,1440
**B01 · holdout 累计 catch/miss/unknown = 34/7/1，分母 41** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/41` × 9 @ L59,433,607,814,835,901,988,1087
  - ✓ `1` × 117 @ L28,32,99,118,126,127,156,240
**B02 · holdout 口径 B（unknown→miss）34/42 = 81.0%** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/42` × 2 @ L815,816
  - ✓ `81.0` × 10 @ L60,497,511,512,549,552,674,815
**B03 · holdout 分层 sanitizer 84.6% (33/39)** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `84.6` × 1 @ L730
  - ✓ `33/39` × 1 @ L730
**B04 · corpus 分层 sanitizer 85.3% (29/34) / compiler-warn 50.0% (9/18) / cross-compile 16.7% (2/12)** — consistent/active `✓✓✓✓✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `85.3` × 2 @ L62,728
  - ✓ `29/34` × 1 @ L728
  - ✓ `50.0` × 2 @ L62,728
  - ✓ `9/18` × 1 @ L728
  - ✓ `16.7` × 3 @ L62,728,1309
  - ✓ `2/12` × 1 @ L729
**B05 · corpus 口径 B（unknown→miss）40/73 = 54.8%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/73` × 1 @ L815
  - ✓ `54.8` × 4 @ L511,531,535,815
**B06 · corpus 口径 C（全样本）40/76 = 52.6%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/76` × 1 @ L816
  - ✓ `52.6` × 8 @ L434,512,513,531,535,624,816,1250
**B07 · corpus 分层 Excluded unknown=9 / not_error=3** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `9` × 26 @ L9,64,298,481,488,495,512,535
  - ✓ `3` × 57 @ L103,133,168,298,408,410,475,521
**B08 · holdout 新子集 17/20 = 85.0%（round5）** — consistent/active `✓✗`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `17/20` × 1 @ L498
  - ✗ `85.0` × 0 @ L
**B09 · 历史批次 669：87.5%（14/16）与 CI[61.7, 98.4]** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `87.5` × 9 @ L275,549,552,673,805,985,986,1082
**B10 · 历史批次 660：80.0%（batch compare before）** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `80.0` × 6 @ L549,552,599,618,718,982
**C01 · 判决规则数 67（len(gate_engine.RULES)）** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES))"`
  - ✓ `67` × 23 @ L56,60,137,142,284,303,317,326
**C02 · 权威账本事件数 452（decision_event_v2_ledger.jsonl 非空行）** — consistent/active `✓`
- 源：`python -c "n=sum(1 for l in open(r'data/authority/decision_event_v2_ledger.jsonl',encoding='utf-8') if l.strip());print(n)"`
  - ✓ `452` × 8 @ L58,137,330,849,888,903,943,1096
**C03 · 实卡数 atoms_real = 42（counts_659.py 现算）** — consistent/active `✓`
- 源：`python tools/counts_659.py --json`
  - ✓ `42` × 10 @ L57,406,409,815,816,906,1090,1091
**C04 · Verifier Coverage = 31/42 = 73.8%** — consistent/active `✓✓`
- 源：`atoms/**/ATOM-*.md 排除 draft650/；status∈{verified,red-team-verified,machine-verified}`
  - ✓ `31/42` × 2 @ L409,906
  - ✓ `73.8` × 4 @ L58,409,906,1090
  - 注：本工具重算 anchored=31 real=42
**C05.conc · VC 分域 conc 3/3** — consistent/active `✓`
- 源：`atoms/conc/ATOM-*.md`
  - ✓ `conc 3/3` × 1 @ L410
  - 注：分域不通过汇票，只作辅助（论文写作 `conc 3/3, hist 1/1, mem 22/24, ub 5/6, lang 0/8`）
**C05.hist · VC 分域 hist 1/1** — consistent/active `✓`
- 源：`atoms/hist/ATOM-*.md`
  - ✓ `hist 1/1` × 1 @ L410
  - 注：分域不通过汇票，只作辅助（论文写作 `conc 3/3, hist 1/1, mem 22/24, ub 5/6, lang 0/8`）
**C05.mem · VC 分域 mem 22/24** — consistent/active `✓`
- 源：`atoms/mem/ATOM-*.md`
  - ✓ `mem 22/24` × 1 @ L410
  - 注：分域不通过汇票，只作辅助（论文写作 `conc 3/3, hist 1/1, mem 22/24, ub 5/6, lang 0/8`）
**C05.ub · VC 分域 ub 5/6** — consistent/active `✓`
- 源：`atoms/ub/ATOM-*.md`
  - ✓ `ub 5/6` × 1 @ L410
  - 注：分域不通过汇票，只作辅助（论文写作 `conc 3/3, hist 1/1, mem 22/24, ub 5/6, lang 0/8`）
**C05.lang · VC 分域 lang 0/8** — consistent/active `✓`
- 源：`atoms/lang/ATOM-*.md`
  - ✓ `lang 0/8` × 1 @ L410
  - 注：分域不通过汇票，只作辅助（论文写作 `conc 3/3, hist 1/1, mem 22/24, ub 5/6, lang 0/8`）
**C06 · VC 的 Clopper–Pearson 95% CI [58.0, 86.1]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(31,42)])"`
  - ✓ `58.0, 86.1` × 4 @ L58,409,906,1090
**C07 · 规则严重度分解 block 44 / warn 16 / advice 7** — consistent/active `✓✓✓✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;from collections import Counter;c=Counter(getattr(r,'severity',None) for r in gate_engine.RULES);print(c.get('block',0),c.get('warn',0),c.get('advice',0))"`
  - ✓ `44/16/7` × 1 @ L999
  - ✓ `44` × 8 @ L598,718,995,999,1490,1506,1523,1568
  - ✓ `16` × 18 @ L62,279,434,498,642,728,806,985
  - ✓ `7` × 21 @ L200,305,340,417,468,469,587,618
  - 注：旧稿的 0/176/55 不可复现，已按现算值纠正
**C08 · 边界卡 26 张；provenance 完整 26/26；scope 完整 0/26** — consistent/active `✓✓✓`
- 源：`data/boundary_provenance_658.json`
  - ✓ `26` × 17 @ L352,353,765,910,938,963,1372,1389
  - ✓ `26/26` × 2 @ L352,1372
  - ✓ `0/26` × 7 @ L353,910,938,963,1372,1389,1665
  - 注：provenance 完整 = provenance 字典字段数 ≥3（mutationset/generator/evidence）
**N01 · 81.2% 必须在出现的每一处都被标为从未落盘/作废** — consistent/active `✓`
- 源：`673c/676h 诚实边界：81.2% 不得作为已落盘结果引用`
  - ✓ `81.2` × 1 @ L
  - 注：若 81.2 出现在没有 never-landed 标注的句子里 ⇒ 违反
**D01 · A5 holdout 主端点 FD 90.0% (18/20) vs Random 35.0%** — consistent/superseded_by_676f `✓✓✓✓✓✗✓✗✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `90.0` × 1 @ L1228
  - ✓ `18/20` × 1 @ L1229
  - ✓ `35.0` × 7 @ L621,805,917,1083,1116,1229,1283
  - ✓ `7/20` × 1 @ L1229
  - ✓ `10.0` × 4 @ L621,917,1116,1283
  - ✗ `2/20` × 0 @ L
  - ✓ `+55.0pp` × 1 @ L1229
  - ✗ `33.2, 76.8` × 0 @ L
  - ✓ `9.8\times10^{-4}` × 1 @ L1230
  - ✓ `1.23` × 1 @ L1230
  - 注：673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹
**D01b · A5 holdout 2000 次随机分布：FD 严格优于的比例与均值/标准差** — consistent/superseded_by_676f `✗✗✓✗`
- 源：`data/experiments/a5_673p.json`
  - ✗ `93.75` × 0 @ L
  - ✗ `93.8` × 0 @ L
  - ✓ `55.0` × 2 @ L1229,1491
  - ✗ `23.4` × 0 @ L
**D01c · A5 设计量：holdout 派生 n=21 / 评估 n=20** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `21` × 18 @ L60,64,67,443,481,488,495,498
  - ✓ `20` × 28 @ L61,246,248,498,573,607,617,747
  - ✓ `4` × 46 @ L180,303,304,306,307,313,411,468
  - ✓ `2000` × 2 @ L571,1440
  - ✓ `8` × 34 @ L65,410,411,417,587,595,609,626
  - ✓ `41` × 45 @ L59,66,72,78,433,443,489,573
**D02 · A5 corpus 主端点 FD 81.25% (13/16) vs Random 37.5%** — consistent/superseded_by_676f `✓✓✓✓✓✓✓✗✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `81.2` × 11 @ L279,549,555,622,675,984,1266,1298
  - ✓ `13/16` × 3 @ L279,1230,1300
  - ✓ `37.5` × 1 @ L1231
  - ✓ `6/16` × 1 @ L1231
  - ✓ `37.5` × 1 @ L1231
  - ✓ `6/16` × 1 @ L1231
  - ✓ `+43.8pp` × 1 @ L1231
  - ✗ `13.9, 73.6` × 0 @ L
  - ✓ `0.039` × 1 @ L1231
  - ✓ `0.93` × 1 @ L1232
  - 注：673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹
**D02b · A5 corpus 2000 次随机分布：FD 严格优于的比例与均值/标准差** — retired/superseded_by_676f `✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✗ `95.80` × 0 @ L
  - ✗ `95.8` × 0 @ L
  - ✗ `53.7` × 0 @ L
  - ✗ `16.0` × 0 @ L
**D02c · A5 设计量：corpus 派生 n=48 / 评估 n=16** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `48` × 13 @ L443,607,963,970,981,988,1227,1309
  - ✓ `16` × 18 @ L62,279,434,498,642,728,806,985
  - ✓ `4` × 46 @ L180,303,304,306,307,313,411,468
  - ✓ `2000` × 2 @ L571,1440
  - ✓ `8` × 34 @ L65,410,411,417,587,595,609,626
  - ✓ `64` × 37 @ L62,66,434,443,489,582,586,605
**F01x · 676f 样本簿记：1137 总样本；派生 571；评估 566** — consistent/active `✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `1137` × 5 @ L569,1234,1394,1400,1406
  - ✓ `571` × 2 @ L570,1401
  - ✓ `566` × 19 @ L71,571,628,651,683,747,907,912
  - ✓ `1063` × 1 @ L1404
  - ✓ `74` × 13 @ L62,486,495,814,835,901,1404,1495
  - ✓ `10` × 24 @ L342,522,554,621,623,642,676,747
**F02x · 676f 主端点（k=4，全 8 资产池）FD/Random/Static 三臂** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `54.6` × 5 @ L72,572,1433,1446,1470
  - ✓ `309/566` × 2 @ L1433,1446
  - ✓ `30.6` × 11 @ L72,572,575,684,747,907,912,1434
  - ✓ `173/566` × 1 @ L1434
  - ✓ `24.7` × 3 @ L73,573,1435
  - ✓ `140/566` × 1 @ L1435
  - ✓ `60.1` × 5 @ L1436,1472,1473,1474
  - ✓ `340/566` × 1 @ L1436
**F03x · 676f 主端点 Δ(FD−Random) +24.0pp CI[+20.5, +27.5] p=2.3e-41 h=0.49 (b=136, c=0)** — consistent/active `✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `+24.0pp` × 6 @ L72,572,747,1434,1513,1538
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 5 @ L72,573,747,1434,1470
  - ✓ `0.49` × 1 @ L1434
  - ✗ `(136,0)` × 0 @ L
**F04x · 676f 主端点 Δ(FD−Static) +29.9pp CI[+25.2, +34.5] p=1.9e-31** — consistent/active `✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+29.9pp` × 6 @ L73,574,684,747,907,1435
  - ✗ `25.2, 34.5` × 0 @ L
  - ✓ `1.9\times10^{-31}` × 3 @ L747,907,1435
  - ✓ `0.62` × 1 @ L1435
**F05x · 676f 2000 次随机分布：FD 严格优于 97.6%（Random 均值 40.2%，SD 9.3pp）** — consistent/active `✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `97.6` × 1 @ L1440
  - ✓ `40.2` × 1 @ L1441
  - ✓ `9.3` × 1 @ L1441
  - ✓ `2000` × 2 @ L571,1440
**F06x · 676f 并列分析（剔退化资产）：Δ(FD−Random)=0.0pp p=1.0；Δ(FD−Static)=+30.6pp CI[+26.0,+35.1] p=8.1e-34** — consistent/active `✓✓✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
  - ✓ `1.0` × 14 @ L281,576,849,913,1027,1085,1446,1467
  - ✓ `+30.6pp` × 6 @ L575,684,747,907,912,1447
  - ✗ `26.0, 35.1` × 0 @ L
  - ✓ `8.1\times10^{-34}` × 1 @ L1447
  - ✓ `24.0` × 9 @ L72,572,747,1434,1457,1470,1471,1513
  - ✗ `136/566` × 0 @ L
**F07x · 676f k 扫描（k=1..8）各档 Δ 与 p** — consistent/active `✗✓✗✓✓✓✗✓✗✓✓✓✗✓✗✗✓✓✓✓✗✓✓✓✗✓✗✓✓✓✗✓✗✓✓✓✗✓✗✓✓✓✗✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+33.0pp` × 0 @ L
  - ✓ `+33.0` × 1 @ L1467
  - ✗ `29.2, 36.9` × 0 @ L
  - ✓ `1.0\times10^{-56}` × 1 @ L1467
  - ✓ `33.0` × 2 @ L1467
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
  - ✗ `+30.7pp` × 0 @ L
  - ✓ `+30.7` × 1 @ L1468
  - ✗ `26.2, 35.3` × 0 @ L
  - ✓ `7.8\times10^{-35}` × 1 @ L1468
  - ✓ `45.1` × 1 @ L1468
  - ✓ `14.3` × 1 @ L1468
  - ✗ `+20.5pp` × 0 @ L
  - ✓ `+20.5` × 5 @ L573,747,1434,1469,1470
  - ✗ `16.5, 24.5` × 0 @ L
  - ✗ `2.1\times10^{-22}` × 0 @ L
  - ✓ `51.1` × 1 @ L1469
  - ✓ `30.6` × 11 @ L72,572,575,684,747,907,912,1434
  - ✓ `+24.0pp` × 6 @ L72,572,747,1434,1513,1538
  - ✓ `+24.0` × 9 @ L72,572,747,1434,1457,1470,1471,1513
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 5 @ L72,573,747,1434,1470
  - ✓ `54.6` × 5 @ L72,572,1433,1446,1470
  - ✓ `30.6` × 11 @ L72,572,575,684,747,907,912,1434
  - ✗ `+20.7pp` × 0 @ L
  - ✓ `+20.7` × 1 @ L1471
  - ✗ `17.3, 24.0` × 0 @ L
  - ✓ `1.2\times10^{-35}` × 1 @ L1471
  - ✓ `59.4` × 1 @ L1471
  - ✓ `38.7` × 1 @ L1471
  - ✗ `+11.3pp` × 0 @ L
  - ✓ `+11.3` × 1 @ L1472
  - ✗ `8.7, 13.9` × 0 @ L
  - ✓ `1.1\times10^{-19}` × 1 @ L1472
  - ✓ `60.1` × 5 @ L1436,1472,1473,1474
  - ✓ `48.8` × 4 @ L607,1472,1532,1593
  - ✗ `+10.6pp` × 0 @ L
  - ✓ `+10.6` × 1 @ L1473
  - ✗ `8.1, 13.1` × 0 @ L
  - ✓ `1.7\times10^{-18}` × 1 @ L1473
  - ✓ `60.1` × 5 @ L1436,1472,1473,1474
  - ✓ `49.5` × 7 @ L62,486,495,814,835,901,1473
  - ✗ `+0.0pp` × 0 @ L
  - ✗ `+0.0` × 0 @ L
  - ✓ `0.0, 0.0` × 1 @ L1474
  - ✗ `1.000` × 0 @ L
  - ✓ `60.1` × 5 @ L1436,1472,1473,1474
  - ✓ `60.1` × 5 @ L1436,1472,1473,1474
**F08x.undefined_behavior · 676f 子组 undefined_behavior：Δ +58.1pp，BH-FDR p=1e-06，Bonferroni p=1e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+58.1pp` × 0 @ L
  - ✓ `+58.1` × 1 @ L1486
  - ✓ `1.0\times10^{-6}` × 3 @ L1486,1487
  - ✓ `1.0\times10^{-6}` × 3 @ L1486,1487
  - ✓ `43` × 3 @ L805,1231,1486
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.memory_safety · 676f 子组 memory_safety：Δ +46.9pp，BH-FDR p=1e-06，Bonferroni p=3e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+46.9pp` × 0 @ L
  - ✓ `+46.9` × 1 @ L1487
  - ✓ `1.0\times10^{-6}` × 3 @ L1486,1487
  - ✓ `3.0\times10^{-6}` × 1 @ L1487
  - ✓ `49` × 8 @ L62,486,495,814,835,901,1473,1487
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.legacy · 676f 子组 legacy：Δ +36.2pp，BH-FDR p=5.6e-05，Bonferroni p=0.00017** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+36.2pp` × 0 @ L
  - ✓ `+36.2` × 1 @ L1488
  - ✓ `5.6\times10^{-5}` × 1 @ L1488
  - ✓ `1.7\times10^{-4}` × 2 @ L1488,1489
  - ✓ `47` × 1 @ L1488
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.stl · 676f 子组 stl：Δ +15.0pp，BH-FDR p=0.00017，Bonferroni p=0.00067** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+15.0pp` × 0 @ L
  - ✓ `+15.0` × 1 @ L1489
  - ✓ `1.7\times10^{-4}` × 2 @ L1488,1489
  - ✓ `6.7\times10^{-4}` × 1 @ L1489
  - ✓ `100` × 12 @ L470,479,480,544,643,833,835,1421
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.real_world · 676f 子组 real_world：Δ +29.5pp，BH-FDR p=0.00054，Bonferroni p=0.0027** — consistent/active `✗✓✓✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+29.5pp` × 0 @ L
  - ✓ `+29.5` × 1 @ L1490
  - ✓ `5.4\times10^{-4}` × 1 @ L1490
  - ✗ `0.003` × 0 @ L
  - ✓ `44` × 8 @ L598,718,995,999,1490,1506,1523,1568
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.optimization_sensitive · 676f 子组 optimization_sensitive：Δ +55.0pp，BH-FDR p=0.0018，Bonferroni p=0.011** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+55.0pp` × 1 @ L1229
  - ✓ `+55.0` × 2 @ L1229,1491
  - ✗ `0.002` × 0 @ L
  - ✗ `0.011` × 0 @ L
  - ✓ `20` × 28 @ L61,246,248,498,573,607,617,747
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.conditional_trigger · 676f 子组 conditional_trigger：Δ +45.0pp，BH-FDR p=0.0061，Bonferroni p=0.043** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+45.0pp` × 0 @ L
  - ✓ `+45.0` × 1 @ L1492
  - ✗ `0.006` × 0 @ L
  - ✗ `0.043` × 0 @ L
  - ✓ `20` × 28 @ L61,246,248,498,573,607,617,747
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.concurrency · 676f 子组 concurrency：Δ +7.3pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+7.3pp` × 1 @ L1502
  - ✓ `+7.3` × 2 @ L1493,1502
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `109` × 2 @ L1493,1501
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.language_semantics · 676f 子组 language_semantics：Δ +17.8pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+17.8pp` × 0 @ L
  - ✓ `+17.8` × 1 @ L1494
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `45` × 7 @ L64,479,496,836,1468,1492,1494
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.embedded · 676f 子组 embedded：Δ +8.1pp，BH-FDR p=0.034，Bonferroni p=0.34** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+8.1pp` × 0 @ L
  - ✓ `+8.1` × 2 @ L1473,1495
  - ✗ `0.034` × 0 @ L
  - ✗ `0.344` × 0 @ L
  - ✓ `74` × 13 @ L62,486,495,814,835,901,1404,1495
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.odr_link · 676f 子组 odr_link：Δ +6.7pp，BH-FDR p=1，Bonferroni p=1** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+6.7pp` × 1 @ L1500
  - ✓ `+6.7` × 2 @ L1496,1500
  - ✗ `1.000` × 0 @ L
  - ✗ `1.000` × 0 @ L
  - ✓ `15` × 17 @ L433,620,649,718,908,964,1063,1115
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F09x · 676f 子组检验族大小 11** — consistent/active `✓`
- 源：`data/a5_676f_results.json`
  - ✓ `11` × 16 @ L408,502,723,833,835,964,1087,1230
**F10x.planted_false · 676f 真实缺陷 planted=false: FD 64.7% (22/34)，Δ +29.4pp** — consistent/active `✓✓✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `64.7` × 1 @ L1505
  - ✓ `22/34` × 1 @ L1505
  - ✓ `+29.4pp` × 1 @ L1506
  - ✗ `14.1, 44.7` × 0 @ L
  - ✓ `2.0\times10^{-3}` × 1 @ L1506
  - ✓ `35.3` × 2 @ L1468,1505
**F10x.planted_true · 676f planted=true: FD 53.9% (287/532)，Δ +23.7pp** — consistent/active `✓✓✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `53.9` × 1 @ L1507
  - ✓ `287/532` × 1 @ L1507
  - ✓ `+23.7pp` × 1 @ L1508
  - ✗ `20.1, 27.3` × 0 @ L
  - ✓ `2.4\times10^{-38}` × 1 @ L1508
  - ✓ `30.3` × 1 @ L1507
**F11x · 676f 资产诊断：8 资产各自 catch 率；wunsequenced/compile-time 100% unknown（退化）** — consistent/active `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `35.1` × 2 @ L1415,1447
  - ✓ `399` × 1 @ L1415
  - ✓ `0.88` × 4 @ L1415,1416,1417,1420
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
  - ✓ `0` × 169 @ L75,126,241,242,243,245,247,249
  - ✓ `100` × 12 @ L470,479,480,544,643,833,835,1421
  - ✓ `12.6` × 1 @ L1419
  - ✓ `143` × 1 @ L1419
  - ✓ `15.0` × 2 @ L1418,1489
  - ✓ `170` × 2 @ L1050,1418
  - ✓ `3.34` × 1 @ L1418
  - ✓ `0.9` × 1 @ L1564
  - ✓ `10` × 24 @ L342,522,554,621,623,642,676,747
  - ✓ `22.4` × 1 @ L1417
  - ✓ `255` × 1 @ L1417
  - ✓ `0.88` × 4 @ L1415,1416,1417,1420
  - ✓ `23.6` × 1 @ L1416
  - ✓ `268` × 1 @ L1416
  - ✓ `0.88` × 4 @ L1415,1416,1417,1420
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
  - ✓ `0` × 169 @ L75,126,241,242,243,245,247,249
  - ✓ `100` × 12 @ L470,479,480,544,643,833,835,1421
  - 注：退化资产是 A5 主/并列分析差异的唯一来源
**G01x · 676g 总盘：n=1147，catch 707，miss 440，盲区比 38.4%** — consistent/active `✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `1147` × 5 @ L649,688,908,1522,1559
  - ✓ `707` × 2 @ L1522,1560
  - ✓ `440` × 2 @ L1522,1560
  - ✓ `38.4` × 5 @ L649,688,908,1523,1560
**G02x · 676g 互补性：6 资产并集 61.6%，最佳单资产 35.6%** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `61.6` × 2 @ L908,1561
  - ✓ `707` × 2 @ L1522,1560
  - ✓ `35.6` × 3 @ L908,1561,1563
**G03x · 676g 逐资产覆盖率（asan/ubsan/tsan/compiler-warn/cross-compile/linker）** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `35.6` × 3 @ L908,1561,1563
  - ✓ `23.5` × 1 @ L1563
  - ✓ `22.9` × 1 @ L1563
  - ✓ `12.5` × 3 @ L834,1309,1563
  - ✓ `10.6` × 2 @ L1473,1564
  - ✓ `0.9` × 1 @ L1564
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
  - ✓ `0.0` × 22 @ L75,502,576,628,685,747,835,912
**G04x · 676g 按 planted：true 41.0% [38.0, 44.1]；false 21.6% [13.8, 32.3]** — consistent/active `✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `41.0` × 2 @ L1523,1568
  - ✓ `38.0, 44.1` × 2 @ L1523,1568
  - ✓ `21.6` × 2 @ L1524,1568
  - ✓ `13.8, 32.3` × 2 @ L1524,1568
  - ✓ `74` × 13 @ L62,486,495,814,835,901,1404,1495
**G05x · 676g 盲区分带：18 个类型 >50% 盲；类型总数 70** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `18` × 5 @ L502,728,1141,1229,1473
  - ✓ `70` × 5 @ L481,649,908,1526,1564
  - ✓ `50` × 15 @ L62,479,595,598,649,706,718,728
**G06x · 676g TSan 稳定性：3/180 不稳定（1.7%）** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `3` × 57 @ L103,133,168,298,408,410,475,521
  - ✓ `180` × 3 @ L1417,1533,1571
  - ✓ `1.7` × 6 @ L829,1473,1488,1489,1534,1572
**E01 · clang-analyzer holdout 48.8% (20/41) p=1.2e-4** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `48.8` × 4 @ L607,1472,1532,1593
  - ✓ `20/41` × 2 @ L607,1593
  - ✓ `1.2\times10^{-4}` × 2 @ L608,1593
**E02 · cppcheck holdout 41.5% (17/41) p=1.5e-5** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `41.5` × 2 @ L607,1594
  - ✓ `17/41` × 2 @ L607,1594
  - ✓ `1.5\times10^{-5}` × 2 @ L608,1594
**E03 · cppcheck corpus 54.7% (35/64) p=0.38331031799316406** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `54.7` × 2 @ L609,1609
  - ✓ `35/64` × 2 @ L609,1609
  - ✓ `0.383` × 2 @ L609,1609
**E03b · cppcheck corpus Δ +7.8pp CI[-6.1, 21.7]（CI 跨 0 ⇒ tie）** — consistent/active `✓✓✗`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+7.8pp` × 1 @ L1613
  - ✓ `-6.1, 21.7` × 1 @ L1613
  - ✗ `(13,8)` × 0 @ L
**E04 · E9 附录 StrictA 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1593,1594
  - ✓ `1/11` × 2 @ L1593,1594
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E05 · E9 附录 cppcheck 主口径 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1593,1594
  - ✓ `1/11` × 2 @ L1593,1594
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E06 · E9 附录：holdout Δ(FD−StrictA) +34.1pp [19.6, 48.7]，对子 (14,0)** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+34.1pp` × 1 @ L1599
  - ✓ `19.6, 48.7` × 1 @ L1599
  - ✓ `(14,0)` × 1 @ L1598
**E07 · E9 附录：corpus StrictA 34.4% (22/64)，Δ +28.1pp 对子 (23,5)，p=9.1e-4** — consistent/active `✓✓✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `34.4` × 1 @ L1608
  - ✓ `22/64` × 1 @ L1608
  - ✓ `+28.1pp` × 1 @ L1613
  - ✓ `(23,5)` × 1 @ L1613
  - ✓ `9.1\times10^{-4}` × 1 @ L1608
**E08 · E9 附录：corpus 分层 FD/ct/cp（sanitizer 29/17/26；compiler-warn 9/5/8；cross-compile 2/0/1）** — consistent/active `✗✗✓✓✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✗ `29 / 17 / 26` × 0 @ L
  - ✗ `9 / 5 / 8` × 0 @ L
  - ✓ `2 / 0 / 1` × 1 @ L1618
  - ✓ `12` × 21 @ L433,594,705,729,833,834,911,964
  - ✓ `FD 29 vs clang-analyzer 17 / cppcheck 26` × 1 @ L1617
  - ✓ `FD 9 / cppcheck 8` × 1 @ L1617
  - ✓ `2 / 0 / 1` × 1 @ L1618
**E10 · E9 附录：clang-tidy 主口径 holdout 100% recall / 100% FPR（零区分度 ⇒ 该口径被弃用）** — consistent/active `✗✓✗✓✗✗`
- 源：`data/673e_comparison_stats.json`
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 12 @ L470,479,480,544,643,833,835,1421
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 12 @ L470,479,480,544,643,833,835,1421
  - ✗ `41/41` × 0 @ L
  - ✗ `11/11` × 0 @ L
**E09 · E9 附录：8 个反向对（工具 catch / FD miss）** — consistent/active `✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `8` × 34 @ L65,410,411,417,587,595,609,626
**F01 · 外部锚点子集 A（准则原文）28.6% (10/35) CI[14.6,46.3]** — consistent/active `✓✗✓`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `28.6` × 7 @ L66,507,598,680,717,837,905
  - ✗ `10/35` × 0 @ L
  - ✓ `14.6, 46.3` × 1 @ L717
**F02 · 外部锚点子集 B（UB 片段重建）80.0% (12/15)** — consistent/active `✓✓`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `80.0` × 6 @ L549,552,599,618,718,982
  - ✓ `12/15` × 1 @ L433
**F03 · 外部锚点合计 44.0% (22/50)；扫描规则 87** — consistent/active `✓✗✓✓✓✓✓✓`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `44.0` × 2 @ L598,718
  - ✗ `22/50` × 0 @ L
  - ✓ `22` × 11 @ L410,1112,1113,1141,1417,1469,1505,1563
  - ✓ `50` × 15 @ L62,479,595,598,649,706,718,728
  - ✓ `87` × 11 @ L275,549,552,673,715,805,985,986
  - ✓ `35` × 22 @ L480,609,618,621,717,805,908,917
  - ✓ `15` × 17 @ L433,620,649,718,908,964,1063,1115
  - ✓ `11/60` × 1 @ L723
**F04 · LLM 臂：GLM-4 12/12 vs FD 6/12；对照误报 4/8 = 50%** — consistent/active `✓✓✓✓✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✓ `12/12` × 4 @ L594,705,1383,1385
  - ✓ `6/12` × 2 @ L594,705
  - ✓ `4/8` × 3 @ L595,706,1386
  - ✓ `50.0` × 2 @ L62,728
  - ✓ `50.0` × 2 @ L62,728
  - 注：FD 的 6/12 由 fd_detect_rate_pct=50.0% × llm_n 重算得到
**F05 · LLM 臂配对 b/c = (0,6)，p=0.03125** — consistent/active `✗✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✗ `0,6` × 0 @ L
  - ✓ `0.031` × 2 @ L707,1388
**G01 · 变异（core）110/114 = 96.5%** — consistent/active `✓✓✗`
- 源：`data/656_mutation_report.json`
  - ✓ `110/114` × 3 @ L624,971,986
  - ✓ `96.5` × 6 @ L432,624,914,986,1084,1384
  - ✗ `91.3, 99.0` × 0 @ L
**G02 · 变异（all-scope）130/159 = 81.8%** — consistent/active `✓✓`
- 源：`data/656_mutation_report_all.json`
  - ✓ `130/159` × 2 @ L624,971
  - ✓ `81.8` × 2 @ L624,1084
**G03 · 缺陷重注入 6/6 = 100%；total 15；软覆盖 12/15** — consistent/active `✓✓✓`
- 源：`data/defect_injection_661.json`
  - ✓ `6/6` × 3 @ L432,833,835
  - ✓ `12/15` × 1 @ L433
  - ✓ `15` × 17 @ L433,620,649,718,908,964,1063,1115
**H01 · 样本量：独立两比例 0.35→0.50 ⇒ n=170** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=None, α=0.05, power=0.8, recomputed=169.09`
  - ✓ `170` × 2 @ L1050,1418
  - ✗ `170 (holdout)` × 0 @ L
**H02 · 样本量：独立两比例 0.35→0.55 ⇒ n=96** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.55,psi=None, α=0.05, power=0.8, recomputed=95.77`
  - ✓ `96` × 7 @ L432,624,914,986,1051,1084,1384
  - ✗ `96 (holdout)` × 0 @ L
**H03 · 样本量：独立两比例 0.35→0.45 ⇒ n=376** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.45,psi=None, α=0.05, power=0.8, recomputed=375.27`
  - ✓ `376` × 1 @ L1052
  - ✗ `376 (holdout)` × 0 @ L
**H04 · 样本量：配对 ψ=0.3 ⇒ n=103** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.3, α=0.05, power=0.8, recomputed=102.26`
  - ✓ `103` × 1 @ L1053
  - ✗ `103 (holdout)` × 0 @ L
**H05 · 样本量：配对 ψ=0.4 ⇒ n=138** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.4, α=0.05, power=0.8, recomputed=137.15`
  - ✓ `138` × 1 @ L1054
  - ✗ `138 (holdout)` × 0 @ L
**H06 · 样本量：配对 ψ=0.5 ⇒ n=173** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.5, α=0.05, power=0.8, recomputed=172.04`
  - ✓ `173` × 6 @ L964,1055,1434,1512,1537,1653
  - ✗ `173 (holdout)` × 0 @ L
**K01 · tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现** — consistent/unpinned_no_artifact `✓✓`
- 源：`data/656_mutation_report*.json 现存值为 110/114 与 130/159；全仓扫描 `30/48` 无产物命中（唯一产出是更早被覆盖的报告）`
  - ✓ `62.5` × 21 @ L61,433,479,486,495,498,511,513
  - ✓ `30/48` × 2 @ L970,981
  - 注：论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注）
**K02 · tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径** — consistent/unpinned_retired_caliber `✓`
- 源：`仅能追溯到 research/paper_v0.4.md 与 data/669_caliber_report.json::doc_sightings；对应 -O1 单档产物已被 665/668 双档口径取代`
  - ✓ `66.7` × 6 @ L274,549,552,673,972,983
  - 注：该值口径已退休，只能作为“当时口径下读到的数”引用
**I01 · Static holdout 1/41 CI ⇒ [0.1, 12.9]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(1,41)])"`
  - ✓ `0.1, 12.9` × 1 @ L833
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I02 · Random† holdout 4/41 CI ⇒ [2.7, 23.1]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(4,41)])"`
  - ✓ `2.7, 23.1` × 1 @ L834
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I03 · FD holdout 34/41 CI ⇒ [67.9, 92.8]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,41)])"`
  - ✓ `67.9, 92.8` × 7 @ L60,486,495,814,835,901,988
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I04 · Caliber B holdout 34/42 CI ⇒ [65.9, 91.4]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,42)])"`
  - ✓ `65.9, 91.4` × 2 @ L815,816
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I05 · Static corpus 11/64 CI ⇒ [8.9, 28.7]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(11,64)])"`
  - ✓ `8.9, 28.7` × 1 @ L833
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I06 · Random† corpus 14/64 CI ⇒ [12.5, 34.0]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(14,64)])"`
  - ✓ `12.5, 34.0` × 1 @ L834
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I07 · FD corpus 40/64 CI ⇒ [49.5, 74.3]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,64)])"`
  - ✓ `49.5, 74.3` × 6 @ L62,486,495,814,835,901
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I08 · Caliber B corpus 40/73 CI ⇒ [42.7, 66.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,73)])"`
  - ✓ `42.7, 66.5` × 1 @ L815
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I09 · Caliber C corpus 40/76 CI ⇒ [40.8, 64.2]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,76)])"`
  - ✓ `40.8, 64.2` × 1 @ L816
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I10 · 对照 FPR 0/11 CI ⇒ [0.0, 28.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(0,11)])"`
  - ✓ `0.0, 28.5` × 1 @ L835
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I11 · corpus 分层 sanitizer 29/34 CI ⇒ [68.9, 95.0]** — missing/not_printed `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(29,34)])"`
  - ✗ `68.9, 95.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I12 · corpus 分层 compiler-warn 9/18 CI ⇒ [26.0, 74.0]** — missing/not_printed `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(9,18)])"`
  - ✗ `26.0, 74.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I13 · corpus 分层 cross-compile 2/12 CI ⇒ [2.1, 48.4]** — missing/not_printed `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(2,12)])"`
  - ✗ `2.1, 48.4` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I14 · 缺陷重注入 6/6 CI ⇒ [54.1, 100.0]** — missing/not_printed `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(6,6)])"`
  - ✗ `54.1, 100.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**D03 · A5 矩阵 105×8 = 840 次 detect** — consistent/superseded_by_676f `✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `105` × 1 @ L1227
  - ✓ `840` × 1 @ L1227
  - ✓ `8` × 34 @ L65,410,411,417,587,595,609,626
**A19 · ±5pp 缺口：holdout 还差 195，corpus 还差 314** — consistent/active `✓✓`
- 源：`sample_size_672k.±5pp.n − 当前可测 n`
  - ✓ `195` × 1 @ L1063
  - ✓ `314` × 1 @ L1063
