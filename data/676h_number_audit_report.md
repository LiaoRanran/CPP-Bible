# 676h · 论文数字可追溯性审计报告

- 生成时间：2026-10-09T20:16:40+08:00
- 被审计稿件：`research/latex/queyi_neurips2027_v1.1.tex`（正文 None 页 / 全稿 37 页，取自编译日志）
- 权威源：14 个文件
- 检察条数：**130**，其中 consistent 116，硬 missing（active）0，软 missing（not_printed 等）0，skipped/no_source 0

## 0. 结论速览

**已有数字的逐条检察全部命中**（不一致率 = 0）。
待 676f/676g 数据就绪后刷新的检察：0 条（见 §3）。

## 1. 硬不一致清单（missing + active：源里有值、论文里必须出现却找不到）

（空）—— 论文里已有的数字逐条追到了权威源，且写法一致。

### 1b. 软登记：源里算了、论文没打印（not_printed / retired，非不一致）

| ID | 说明 | 状态 |
|---|---|---|
| A15 | 扩样前 corpus 54.2% (26/48) | superseded:689重构 |
| A16 | H4 子集差额 corpus +33.3pp / holdout +4.0pp | superseded:689重构 |
| B08 | holdout 新子集 17/20 = 85.0%（round5） | superseded:689重构 |
| C05.conc | VC 分域 conc 3/3 | superseded:689重构 |
| C05.hist | VC 分域 hist 1/1 | superseded:689重构 |
| C05.mem | VC 分域 mem 22/24 | superseded:689重构 |
| C05.ub | VC 分域 ub 5/6 | superseded:689重构 |
| C05.lang | VC 分域 lang 0/8 | superseded:689重构 |
| C06 | VC 的 Clopper–Pearson 95% CI [58.0, 86.1] | superseded:689重构 |
| D02b | A5 corpus 2000 次随机分布：FD 严格优于的比例与均值/标准差 | superseded_by_676f |
| I11 | corpus 分层 sanitizer 29/34 CI ⇒ [68.9, 95.0] | superseded:689重构 |
| I12 | corpus 分层 compiler-warn 9/18 CI ⇒ [26.0, 74.0] | superseded:689重构 |
| I13 | corpus 分层 cross-compile 2/12 CI ⇒ [2.1, 48.4] | superseded:689重构 |
| I14 | 缺陷重注入 6/6 CI ⇒ [54.1, 100.0] | superseded:689重构 |

### 1c. un-pinned 历史值（源不可得 / 口径已退役）

| ID | 说明 | 状态 | 处置 |
|---|---|---|---|
| K01 | tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现 | unpinned_no_artifact | 论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注） |
| K02 | tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径 | unpinned_retired_caliber | 该值口径已退休，只能作为“当时口径下读到的数”引用 |

## 2. 逐组概览

| 分组 | consistent | 其它 |
|---|---|---|
| A.核心三臂 | 17 | 2 |
| B.reveal | 9 | 1 |
| C.系统计数 | 6 | 6 |
| D.A5 | 10 | 1 |
| D2.A5-676f | 22 | 0 |
| D3.盲区地图 | 6 | 0 |
| E.外部工具 | 11 | 0 |
| F.LLM/锚点 | 5 | 0 |
| G.变异/注入 | 3 | 0 |
| H.样本量 | 6 | 0 |
| I.CI重算 | 10 | 4 |
| K.历史 un-pinned | 2 | 0 |
| N.诚实性反向检察 | 1 | 0 |
| Z.689重构 | 4 | 0 |
| Z.691修正 | 4 | 0 |

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

扫描到数字 token **1925** 个（已排除注释行与导言区行）。分类：

| 类别 | 数量 | 占比 |
|---|---|---|
| claim | 1469 | 76.3% |
| unclassified | 175 | 9.1% |
| design_constant | 71 | 3.7% |
| batch_id | 60 | 3.1% |
| method_constant | 40 | 2.1% |
| format_layout | 26 | 1.4% |
| repro_command | 24 | 1.2% |
| year | 11 | 0.6% |
| system_constant | 9 | 0.5% |
| engineering_narrative | 9 | 0.5% |
| logic_constant | 7 | 0.4% |
| external_literature | 6 | 0.3% |
| historical_retired | 5 | 0.3% |
| structural | 4 | 0.2% |
| sample_id | 4 | 0.2% |
| cited_context | 3 | 0.2% |
| external_regulation | 2 | 0.1% |

未归类 token：175 个（前 60 条见下；全量在 json 里）。

| 行 | token | 上下文 |
|---|---|---|
| 301 | `40` | `\emph{same} 40 catches; a flag change once moved holdout recall $66.7\%\to87.5\%$ with the` |
| 373 | `34` | `across 34 normalized types (8 families), including 64 corpus-null controls and 35 hung` |
| 374 | `110` | `samples. \emph{Source-derived real-defect corpus} (110 samples): minimal reconstructions of` |
| 375 | `30` | `defects from 30+ real projects (CVE/NVD-verified mechanisms, responses frozen; \emph{not}` |
| 399 | `13.3` | `Four profiles are declared: \texttt{wsl-gcc-13.3} (asan/ubsan/tsan, primary),` |
| 401 | `200` | `\texttt{wsl-clang-18.1.3} (200-sample stratified replication), and MSVC/clang-cl (absent on` |
| 428 | `24` | `\paragraph{F1. A $+24$pp ``selection gain'' is mostly measurement-pool composition` |
| 435 | `24.03` | `\textbf{composition-dominated within the pools measured} ($+24.03$pp at $k{=}4$,` |
| 448 | `5` | `$1/\binom{5}{4}{=}0.2$). Against the 2000-draw random \emph{mean} the same tiers read` |
| 456 | `711` | `\emph{Causal decomposition (read-only, added in 711).} The headline decomposes exactly, one knob at` |
| 457 | `24.03` | `a time: $+24.03$pp (single-point caliber, full pool, $k{=}4$) $\to+14.48$ (expectation caliber,` |
| 467 | `110` | `large step (dropping \texttt{linker}, $-4.65$pp) is itself $110\%$ pool geometry: with a zero-yield` |
| 468 | `5.12` | `sixth asset as separator, the slot effect at $k{=}4$ is $5.12$pp and \texttt{linker}'s own coverage` |
| 470 | `5.35` | `cross-frame recomputation gives $5.35$pp and the $g_{\text{app}}$ slope of the Type~I scan gives` |
| 471 | `5.32` | `$5.32$pp. The residual tier is also predictable rather than mysterious: under clone-family-aware` |
| 483 | `13` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 483 | `34` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 485 | `60` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 485 | `62` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 490 | `86.96` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 490 | `30.77` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 493 | `52.2` | `harder on real defects than on synthetic ones (type punning $-52.2$pp, logic $-22.5$pp,` |
| 499 | `65` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 499 | `110` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 501 | `39` | `\textbf{23.64\%} ($-35.45$pp) with \emph{no} unknown increase: 39 catches depend on Linux` |
| 511 | `13.3` | `($n_{\text{env}}{=}1$; E1 \texttt{wsl-gcc-13.3} vs.\ E2 \texttt{windows-native-mingw}), \emph{not}` |
| 532 | `36.9` | `instrument is good at (bounds$+$memory$+$integer $=64.5\%$ of samples vs.\ $36.9\%$ in the` |
| 534 | `31` | `(\texttt{language\_oop}/logic: real $1/31$ vs.\ synthetic $9/35$). Two corpora can share a` |
| 557 | `17496` | `simple optimal selection already exists (all 17496 triples checked; greedy attains ratio` |
| 587 | `55.84` | `A degradation-grade replication in LLM-as-a-judge evaluation scores $55.84/100$ on the` |
| 590 | `33.33` | `non-transferable because a rule change moved the LLM report by only $1.03$pp against $33.33$pp` |
| 594 | `25.00` | `mean-type rule is pulled down by $25.00$pp while OR and majority move by $0.00$pp---the same` |
| 595 | `33.3` | `structural signature as here ($\sigma(\mathrm{OR}){=}0$, $\sigma(\mathrm{mean}){=}33.3\%$). The` |
| 596 | `78.26` | `corrected transfer score is $78.26/100$ (conservative $73.26$): the protocol's migration was` |
| 596 | `73.26` | `corrected transfer score is $78.26/100$ (conservative $73.26$): the protocol's migration was` |
| 610 | `19` | `We report five threat classes with direction and mitigation status (the 19-item table and` |
| 628 | `6.6` | `$6.6\%\to14.3\%$ under $\le15\%$ flips, though contrast directions are stable).` |
| 633 | `110` | `The 110-sample source-derived corpus improves ecological validity but is` |
| 659 | `5` | `rate by $-16.36$pp. Cross-run stability: 5\% grid flips; the shadow-mapped` |
| 668 | `24` | `detecting that collapse. On a software-verification apparatus: a $+24$pp selection gain was` |
| 672 | `17.9` | `explained by a $-17.9$pp composition offset; and failure-driven evolution produced no` |
| 970 | `30` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 970 | `17` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 1322 | `703` | `\paragraph{(10) Cross-domain transfer to LLM-as-a-judge evaluation (added in 703; aggregation axis` |
| 1323 | `711` | `corrected in 711).}` |
| 1325 | `240` | `LLM-judge benchmarks (240 samples downloaded live), a ``longer is better'' lazy judge agrees with` |
| 1326 | `55.83` | `the human-preferred side only $44.17\%$ of the time on JudgeBench---so on $55.83\%$ of samples` |
| 1329 | `55.84` | `LLM arm scores $55.84/100$ on the published four-component transfer scale (caliber $15.62$, environment` |
| 1332 | `33.33` | `report by only $1.03$pp against $33.33$pp in C++, and the original reading held that an LLM` |
| 1340 | `25.00` | `the same frozen verdicts: a mean-type rule is pulled down by $25.00$pp (relative $26.32\%$) by an` |
| 1342 | `33.33` | `C++ ($\sigma(\mathrm{OR}){=}0$, $\sigma(\mathrm{mean}){=}33.33\%$). Restoring the aggregation` |
| 1343 | `78.26` | `component under its own caliber gives a corrected transfer score of \textbf{$78.26/100$}` |
| 1344 | `73.26` | `(conservative \textbf{$73.26$}): the protocol's migration was understated by a test-design false` |
| 1351 | `240` | `pre-registered cross-domain study---the 240 samples were downloaded live and their` |
| 1414 | `13.3` | `The experiment ran the same samples under E1 (\texttt{wsl-gcc-13.3}; six assets) and E2` |
| 1433 | `200` | `catch   & 140 & 200 & 0 & 140 & 0 & 200 \\` |
| 1433 | `200` | `catch   & 140 & 200 & 0 & 140 & 0 & 200 \\` |
| 1434 | `226` | `miss    & 0   & 226 & 0 & 0   & 0 & 226 \\` |
| 1434 | `226` | `miss    & 0   & 226 & 0 & 0   & 0 & 226 \\` |
| 1441 | `200` | `Under un-aware accounting the matrix looks like a \emph{capability loss}: 200 samples move` |

## 5. 每条检察的命中明细

**A01 · holdout 可测检出率 82.9% (34/41) CI[67.9,92.8]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `82.9` × 9 @ L805,826,889,975,1156,1573,1636,1669
  - ✓ `34/41` × 5 @ L805,826,889,975,1156
  - ✓ `67.9, 92.8` × 4 @ L805,826,889,975
**A02 · corpus 可测检出率 62.5% (40/64) CI[49.5,74.3]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `62.5` × 8 @ L805,826,889,957,968,1156,1669,2145
  - ✓ `40/64` × 4 @ L805,826,889,1156
  - ✓ `49.5, 74.3` × 3 @ L805,826,889
**A03 · corpus 全样本口径 52.6%** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `52.6` × 2 @ L807,2145
**A04 · Static 臂 holdout 2.4% (1/41) / corpus 17.2% (11/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `2.4` × 3 @ L820,824,2366
  - ✓ `1/41` × 1 @ L824
  - ✓ `17.2` × 1 @ L824
  - ✓ `11/64` × 1 @ L824
**A05 · Random† 臂 holdout 9.8% (4/41) / corpus 21.9% (14/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `9.8` × 1 @ L825
  - ✓ `4/41` × 1 @ L825
  - ✓ `21.9` × 1 @ L825
  - ✓ `14/64` × 1 @ L825
**A06 · Δ(Static→FD) holdout +80.5pp CI[68.4,92.6] p=2.3e-10 h=1.98** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+80.5pp` × 1 @ L827
  - ✓ `68.4, 92.6` × 1 @ L827
  - ✓ `2.3\times10^{-10}` × 1 @ L753
  - ✓ `1.98` × 1 @ L753
**A07 · Δ(Random†→FD) holdout +73.2pp CI[59.6,86.7] p=1.9e-9 h=1.65** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+73.2pp` × 1 @ L828
  - ✓ `59.6, 86.7` × 1 @ L828
  - ✓ `1.9\times10^{-9}` × 1 @ L755
  - ✓ `1.65` × 1 @ L755
**A08 · Δ(Static→FD) corpus +45.3pp CI[33.1,57.5] p=3.7e-9 h=0.97** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+45.3pp` × 1 @ L827
  - ✓ `33.1, 57.5` × 1 @ L827
  - ✓ `3.7\times10^{-9}` × 1 @ L754
  - ✓ `0.97` × 3 @ L754,1106,2010
**A09 · Δ(Random†→FD) corpus +40.6pp CI[28.6,52.7] p=3.0e-8 h=0.85** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+40.6pp` × 1 @ L828
  - ✓ `28.6, 52.7` × 1 @ L828
  - ✓ `3.0\times10^{-8}` × 1 @ L756
  - ✓ `0.85` × 1 @ L756
**A10 · 配对不一致对 (b, c)（tab:e5 四行）** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `(33, 0)` × 1 @ L753
  - ✓ `(29, 0)` × 1 @ L754
  - ✓ `(30, 0)` × 1 @ L755
  - ✓ `(26, 0)` × 1 @ L756
  - 注：四个对比都是 c=0 结构（对手的 catch 是 FD catch 的子集）
**A11 · 对照假阳性 0.0% (0/11)** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `0.0\% (0/11)` × 4 @ L826,951,1669,2394
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
**A12 · 缺陷重注入 6/6 = 100%** — consistent/active `✓✗`
- 源：`data/current_numbers.json`
  - ✓ `6/6` × 2 @ L824,826
  - ✗ `100.0` × 0 @ L
**A13 · CP95 半宽 12.5pp（holdout）** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `12.5` × 3 @ L825,1620,2174
**A14 · 扩样前 holdout 81.0% (17/21) CI[58.1,94.6]** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `81.0` × 3 @ L806,807,974
  - ✓ `17/21` × 1 @ L974
**A15 · 扩样前 corpus 54.2% (26/48)** — retired/superseded:689重构 `✗✗`
- 源：`data/current_numbers.json`
  - ✗ `54.2` × 0 @ L
  - ✗ `26/48` × 0 @ L
  - 注：689 重构：扩样前后口径随旧正文段落移出正文（数据仍在产物）
**A16 · H4 子集差额 corpus +33.3pp / holdout +4.0pp** — retired/superseded:689重构 `✗✗`
- 源：`data/current_numbers.json`
  - ✗ `+33.3pp` × 0 @ L
  - ✗ `+4.0pp` × 0 @ L
  - 注：689 重构：H4 子集差额随旧正文段落移出正文（数据仍在产物）
**A17 · ±5pp 半宽所需样本量 holdout 236 / corpus 378** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `236` × 4 @ L898,951,1128,1132
  - ✓ `378` × 4 @ L898,951,1128,1132
**A18 · ±10pp 半宽所需样本量 holdout 61 / corpus 97** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `61` × 12 @ L318,523,527,951,973,1127,1618,1970
  - ✓ `97` × 5 @ L951,1127,1773,2026,2275
**B01 · holdout 累计 catch/miss/unknown = 34/7/1，分母 41** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/41` × 5 @ L805,826,889,975,1156
  - ✓ `1` × 172 @ L16,17,38,71,107,115,150,169
**B02 · holdout 口径 B（unknown→miss）34/42 = 81.0%** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/42` × 2 @ L806,807
  - ✓ `81.0` × 3 @ L806,807,974
**B03 · holdout 分层 sanitizer 84.6% (33/39)** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `84.6` × 1 @ L721
  - ✓ `33/39` × 1 @ L721
**B04 · corpus 分层 sanitizer 85.3% (29/34) / compiler-warn 50.0% (9/18) / cross-compile 16.7% (2/12)** — consistent/active `✓✓✓✓✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `85.3` × 1 @ L719
  - ✓ `29/34` × 1 @ L719
  - ✓ `50.0` × 2 @ L719,1626
  - ✓ `9/18` × 1 @ L719
  - ✓ `16.7` × 3 @ L719,2173,2388
  - ✓ `2/12` × 1 @ L720
**B05 · corpus 口径 B（unknown→miss）40/73 = 54.8%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/73` × 1 @ L806
  - ✓ `54.8` × 1 @ L806
**B06 · corpus 口径 C（全样本）40/76 = 52.6%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/76` × 1 @ L807
  - ✓ `52.6` × 2 @ L807,2145
**B07 · corpus 分层 Excluded unknown=9 / not_error=3** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `9` × 38 @ L15,300,318,458,534,537,548,634
  - ✓ `3` × 79 @ L17,25,27,110,158,209,314,404
**B08 · holdout 新子集 17/20 = 85.0%（round5）** — retired/superseded:689重构 `✗✗`
- 源：`data/holdout_reveal_5_672h.json`
  - ✗ `17/20` × 0 @ L
  - ✗ `85.0` × 0 @ L
  - 注：689 重构：round5 子集数字随旧正文段落移出正文（数据仍在产物）
**B09 · 历史批次 669：87.5%（14/16）与 CI[61.7, 98.4]** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `87.5` × 4 @ L796,972,973,1151
**B10 · 历史批次 660：80.0%（batch compare before）** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `80.0` × 2 @ L710,969
**C01 · 判决规则数 67（len(gate_engine.RULES)）** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES))"`
  - ✓ `67` × 13 @ L19,264,805,826,840,889,975,982
**C02 · 权威账本事件数 452（decision_event_v2_ledger.jsonl 非空行）** — consistent/active `✓`
- 源：`python -c "n=sum(1 for l in open(r'data/authority/decision_event_v2_ledger.jsonl',encoding='utf-8') if l.strip());print(n)"`
  - ✓ `452` × 8 @ L19,263,270,840,891,930,1163,1377
**C03 · 实卡数 atoms_real = 42（counts_659.py 现算）** — consistent/active `✓`
- 源：`python tools/counts_659.py --json`
  - ✓ `42` × 6 @ L806,807,1160,1947,1948
**C04 · Verifier Coverage = 31/42 = 73.8%** — consistent/active `✗✓`
- 源：`atoms/**/ATOM-*.md 排除 draft650/；status∈{verified,red-team-verified,machine-verified}`
  - ✗ `31/42` × 0 @ L
  - ✓ `73.8` × 2 @ L38,1159
  - 注：本工具重算 anchored=31 real=42
**C05.conc · VC 分域 conc 3/3** — retired/superseded:689重构 `✗`
- 源：`atoms/conc/ATOM-*.md`
  - ✗ `conc 3/3` × 0 @ L
  - 注：689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）
**C05.hist · VC 分域 hist 1/1** — retired/superseded:689重构 `✗`
- 源：`atoms/hist/ATOM-*.md`
  - ✗ `hist 1/1` × 0 @ L
  - 注：689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）
**C05.mem · VC 分域 mem 22/24** — retired/superseded:689重构 `✗`
- 源：`atoms/mem/ATOM-*.md`
  - ✗ `mem 22/24` × 0 @ L
  - 注：689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）
**C05.ub · VC 分域 ub 5/6** — retired/superseded:689重构 `✗`
- 源：`atoms/ub/ATOM-*.md`
  - ✗ `ub 5/6` × 0 @ L
  - 注：689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）
**C05.lang · VC 分域 lang 0/8** — retired/superseded:689重构 `✗`
- 源：`atoms/lang/ATOM-*.md`
  - ✗ `lang 0/8` × 0 @ L
  - 注：689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）
**C06 · VC 的 Clopper–Pearson 95% CI [58.0, 86.1]** — retired/superseded:689重构 `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(31,42)])"`
  - ✗ `58.0, 86.1` × 0 @ L
  - 注：689 重构：VC 及其 CI 已从论文删除（工程遥测，非科学证据）
**C07 · 规则严重度分解 block 44 / warn 16 / advice 7** — consistent/active `✗✓✓✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;from collections import Counter;c=Counter(getattr(r,'severity',None) for r in gate_engine.RULES);print(c.get('block',0),c.get('warn',0),c.get('advice',0))"`
  - ✗ `44/16/7` × 0 @ L
  - ✓ `44` × 5 @ L710,1326,1564,1628,2348
  - ✓ `16` × 17 @ L588,659,719,797,972,1330,1770,1885
  - ✓ `7` × 42 @ L16,17,45,108,308,345,445,446
  - 注：旧稿的 0/176/55 不可复现，已按现算值纠正
**C08 · 边界卡 26 张；provenance 完整 26/26；scope 完整 0/26** — consistent/active `✓✗✓`
- 源：`data/boundary_provenance_658.json`
  - ✓ `26` × 13 @ L756,897,925,950,1340,1588,1680,1766
  - ✗ `26/26` × 0 @ L
  - ✓ `0/26` × 5 @ L897,925,950,1833,2189
  - 注：provenance 完整 = provenance 字典字段数 ≥3（mutationset/generator/evidence）
**N01 · 81.2% 必须在出现的每一处都被标为从未落盘/作废** — consistent/active `✓`
- 源：`673c/676h 诚实边界：81.2% 不得作为已落盘结果引用`
  - ✓ `81.2` × 1 @ L
  - 注：若 81.2 出现在没有 never-landed 标注的句子里 ⇒ 违反
**D01 · A5 holdout 主端点 FD 90.0% (18/20) vs Random 35.0%** — consistent/superseded_by_676f `✓✗✓✗✓✗✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `90.0` × 2 @ L2136,2428
  - ✗ `18/20` × 0 @ L
  - ✓ `35.0` × 5 @ L796,1152,1182,2136,2159
  - ✗ `7/20` × 0 @ L
  - ✓ `10.0` × 1 @ L1182
  - ✗ `2/20` × 0 @ L
  - ✗ `+55.0pp` × 0 @ L
  - ✗ `33.2, 76.8` × 0 @ L
  - ✗ `9.8\times10^{-4}` × 0 @ L
  - ✗ `1.23` × 0 @ L
  - 注：673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹
**D01b · A5 holdout 2000 次随机分布：FD 严格优于的比例与均值/标准差** — consistent/superseded_by_676f `✗✗✓✗`
- 源：`data/experiments/a5_673p.json`
  - ✗ `93.75` × 0 @ L
  - ✗ `93.8` × 0 @ L
  - ✓ `55.0` × 1 @ L2349
  - ✗ `23.4` × 0 @ L
**D01c · A5 设计量：holdout 派生 n=21 / 评估 n=20** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `21` × 14 @ L539,588,825,950,974,975,1281,1330
  - ✓ `20` × 19 @ L228,230,308,343,494,738,854,950
  - ✓ `4` × 86 @ L25,112,289,310,321,344,432,434
  - ✓ `2000` × 9 @ L290,448,1770,1774,1948,2026,2275,2304
  - ✓ `8` × 55 @ L16,155,373,445,458,700,756,824
  - ✓ `41` × 31 @ L109,343,387,491,738,753,755,805
**D02 · A5 corpus 主端点 FD 81.25% (13/16) vs Random 37.5%** — consistent/superseded_by_676f `✓✓✓✗✓✗✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `81.2` × 4 @ L971,1830,2168,2383
  - ✓ `13/16` × 1 @ L2383
  - ✓ `37.5` × 1 @ L2136
  - ✗ `6/16` × 0 @ L
  - ✓ `37.5` × 1 @ L2136
  - ✗ `6/16` × 0 @ L
  - ✗ `+43.8pp` × 0 @ L
  - ✗ `13.9, 73.6` × 0 @ L
  - ✗ `0.039` × 0 @ L
  - ✗ `0.93` × 0 @ L
  - 注：673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹
**D02b · A5 corpus 2000 次随机分布：FD 严格优于的比例与均值/标准差** — retired/superseded_by_676f `✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✗ `95.80` × 0 @ L
  - ✗ `95.8` × 0 @ L
  - ✗ `53.7` × 0 @ L
  - ✗ `16.0` × 0 @ L
**D02c · A5 设计量：corpus 派生 n=48 / 评估 n=16** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `48` × 11 @ L950,957,968,975,1573,1670,1675,1921
  - ✓ `16` × 17 @ L588,659,719,797,972,1330,1770,1885
  - ✓ `4` × 86 @ L25,112,289,310,321,344,432,434
  - ✓ `2000` × 9 @ L290,448,1770,1774,1948,2026,2275,2304
  - ✓ `8` × 55 @ L16,155,373,445,458,700,756,824
  - ✓ `64` × 25 @ L373,387,532,754,756,805,807,824
**F01x · 676f 样本簿记：1137 总样本；派生 571；评估 566** — consistent/active `✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `1137` × 12 @ L380,1193,1553,1734,1765,1934,1943,2138
  - ✓ `571` × 1 @ L2203
  - ✓ `566` × 26 @ L289,343,386,395,431,469,738,894
  - ✓ `1063` × 1 @ L2206
  - ✓ `74` × 15 @ L805,826,889,1565,1567,1629,1631,1714
  - ✓ `10` × 39 @ L31,32,113,379,449,459,525,526
**F02x · 676f 主端点（k=4，全 8 资产池）FD/Random/Static 三臂** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `54.6` × 4 @ L430,2268,2280,2328
  - ✓ `309/566` × 1 @ L2268
  - ✓ `30.6` × 7 @ L430,738,894,2269,2282,2327,2328
  - ✓ `173/566` × 1 @ L2269
  - ✓ `24.7` × 1 @ L2270
  - ✓ `140/566` × 1 @ L2270
  - ✓ `60.1` × 5 @ L2271,2330,2331,2332
  - ✓ `340/566` × 1 @ L2271
**F03x · 676f 主端点 Δ(FD−Random) +24.0pp CI[+20.5, +27.5] p=2.3e-41 h=0.49 (b=136, c=0)** — consistent/active `✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `+24.0pp` × 10 @ L29,45,107,306,343,431,738,899
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L343,738,2269,2328
  - ✓ `0.49` × 1 @ L2269
  - ✗ `(136,0)` × 0 @ L
**F04x · 676f 主端点 Δ(FD−Static) +29.9pp CI[+25.2, +34.5] p=1.9e-31** — consistent/active `✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+29.9pp` × 4 @ L738,894,1813,2270
  - ✗ `25.2, 34.5` × 0 @ L
  - ✓ `1.9\times10^{-31}` × 3 @ L738,894,2270
  - ✓ `0.62` × 1 @ L2270
**F05x · 676f 2000 次随机分布：FD 严格优于 97.6%（Random 均值 40.2%，SD 9.3pp）** — consistent/active `✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `97.6` × 2 @ L2026,2275
  - ✓ `40.2` × 1 @ L2276
  - ✓ `9.3` × 1 @ L2276
  - ✓ `2000` × 9 @ L290,448,1770,1774,1948,2026,2275,2304
**F06x · 676f 并列分析（剔退化资产）：Δ(FD−Random)=0.0pp p=1.0；Δ(FD−Static)=+30.6pp CI[+26.0,+35.1] p=8.1e-34** — consistent/active `✓✓✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
  - ✓ `1.0` × 20 @ L344,433,446,558,840,900,1098,1154
  - ✓ `+30.6pp` × 3 @ L738,894,2282
  - ✗ `26.0, 35.1` × 0 @ L
  - ✓ `8.1\times10^{-34}` × 1 @ L2282
  - ✓ `24.0` × 13 @ L29,45,107,306,343,431,738,899
  - ✗ `136/566` × 0 @ L
**F07x · 676f k 扫描（k=1..8）各档 Δ 与 p** — consistent/active `✗✓✗✓✓✓✗✓✗✓✓✓✗✓✗✗✓✓✓✓✗✓✓✓✗✓✗✓✓✓✓✓✗✓✓✓✗✓✗✓✓✓✗✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+33.0pp` × 0 @ L
  - ✓ `+33.0` × 1 @ L2325
  - ✗ `29.2, 36.9` × 0 @ L
  - ✓ `1.0\times10^{-56}` × 1 @ L2325
  - ✓ `33.0` × 2 @ L2325
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
  - ✗ `+30.7pp` × 0 @ L
  - ✓ `+30.7` × 1 @ L2326
  - ✗ `26.2, 35.3` × 0 @ L
  - ✓ `7.8\times10^{-35}` × 1 @ L2326
  - ✓ `45.1` × 1 @ L2326
  - ✓ `14.3` × 1 @ L2326
  - ✗ `+20.5pp` × 0 @ L
  - ✓ `+20.5` × 5 @ L343,738,2269,2327,2328
  - ✗ `16.5, 24.5` × 0 @ L
  - ✗ `2.1\times10^{-22}` × 0 @ L
  - ✓ `51.1` × 1 @ L2327
  - ✓ `30.6` × 7 @ L430,738,894,2269,2282,2327,2328
  - ✓ `+24.0pp` × 10 @ L29,45,107,306,343,431,738,899
  - ✓ `+24.0` × 13 @ L29,45,107,306,343,431,738,899
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L343,738,2269,2328
  - ✓ `54.6` × 4 @ L430,2268,2280,2328
  - ✓ `30.6` × 7 @ L430,738,894,2269,2282,2327,2328
  - ✗ `+20.7pp` × 0 @ L
  - ✓ `+20.7` × 1 @ L2329
  - ✗ `17.3, 24.0` × 0 @ L
  - ✓ `1.2\times10^{-35}` × 1 @ L2329
  - ✓ `59.4` × 1 @ L2329
  - ✓ `38.7` × 1 @ L2329
  - ✓ `+11.3pp` × 4 @ L345,1591,1813,1823
  - ✓ `+11.3` × 5 @ L345,1591,1813,1823,2330
  - ✗ `8.7, 13.9` × 0 @ L
  - ✓ `1.1\times10^{-19}` × 1 @ L2330
  - ✓ `60.1` × 5 @ L2271,2330,2331,2332
  - ✓ `48.8` × 3 @ L1573,1670,2330
  - ✗ `+10.6pp` × 0 @ L
  - ✓ `+10.6` × 1 @ L2331
  - ✗ `8.1, 13.1` × 0 @ L
  - ✓ `1.7\times10^{-18}` × 1 @ L2331
  - ✓ `60.1` × 5 @ L2271,2330,2331,2332
  - ✓ `49.5` × 4 @ L805,826,889,2331
  - ✗ `+0.0pp` × 0 @ L
  - ✗ `+0.0` × 0 @ L
  - ✓ `0.0, 0.0` × 1 @ L2332
  - ✗ `1.000` × 0 @ L
  - ✓ `60.1` × 5 @ L2271,2330,2331,2332
  - ✓ `60.1` × 5 @ L2271,2330,2331,2332
**F08x.undefined_behavior · 676f 子组 undefined_behavior：Δ +58.1pp，BH-FDR p=1e-06，Bonferroni p=1e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+58.1pp` × 0 @ L
  - ✓ `+58.1` × 1 @ L2344
  - ✓ `1.0\times10^{-6}` × 3 @ L2344,2345
  - ✓ `1.0\times10^{-6}` × 3 @ L2344,2345
  - ✓ `43` × 3 @ L796,2099,2344
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.memory_safety · 676f 子组 memory_safety：Δ +46.9pp，BH-FDR p=1e-06，Bonferroni p=3e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+46.9pp` × 0 @ L
  - ✓ `+46.9` × 1 @ L2345
  - ✓ `1.0\times10^{-6}` × 3 @ L2344,2345
  - ✓ `3.0\times10^{-6}` × 1 @ L2345
  - ✓ `49` × 6 @ L805,826,889,1850,2331,2345
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.legacy · 676f 子组 legacy：Δ +36.2pp，BH-FDR p=5.6e-05，Bonferroni p=0.00017** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+36.2pp` × 0 @ L
  - ✓ `+36.2` × 1 @ L2346
  - ✓ `5.6\times10^{-5}` × 1 @ L2346
  - ✓ `1.7\times10^{-4}` × 2 @ L2346,2347
  - ✓ `47` × 1 @ L2346
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.stl · 676f 子组 stl：Δ +15.0pp，BH-FDR p=0.00017，Bonferroni p=0.00067** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+15.0pp` × 0 @ L
  - ✓ `+15.0` × 1 @ L2347
  - ✓ `1.7\times10^{-4}` × 2 @ L2346,2347
  - ✓ `6.7\times10^{-4}` × 1 @ L2347
  - ✓ `100` × 24 @ L587,596,824,826,1327,1329,1343,1353
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.real_world · 676f 子组 real_world：Δ +29.5pp，BH-FDR p=0.00054，Bonferroni p=0.0027** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+29.5pp` × 0 @ L
  - ✓ `+29.5` × 1 @ L2348
  - ✓ `5.4\times10^{-4}` × 1 @ L2348
  - ✓ `0.003` × 1 @ L1861
  - ✓ `44` × 5 @ L710,1326,1564,1628,2348
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.optimization_sensitive · 676f 子组 optimization_sensitive：Δ +55.0pp，BH-FDR p=0.0018，Bonferroni p=0.011** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+55.0pp` × 0 @ L
  - ✓ `+55.0` × 1 @ L2349
  - ✗ `0.002` × 0 @ L
  - ✗ `0.011` × 0 @ L
  - ✓ `20` × 19 @ L228,230,308,343,494,738,854,950
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.conditional_trigger · 676f 子组 conditional_trigger：Δ +45.0pp，BH-FDR p=0.0061，Bonferroni p=0.043** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+45.0pp` × 0 @ L
  - ✓ `+45.0` × 1 @ L2350
  - ✗ `0.006` × 0 @ L
  - ✗ `0.043` × 0 @ L
  - ✓ `20` × 19 @ L228,230,308,343,494,738,854,950
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.concurrency · 676f 子组 concurrency：Δ +7.3pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+7.3pp` × 1 @ L2360
  - ✓ `+7.3` × 2 @ L2351,2360
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `109` × 2 @ L2351,2359
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.language_semantics · 676f 子组 language_semantics：Δ +17.8pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+17.8pp` × 0 @ L
  - ✓ `+17.8` × 1 @ L2352
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `45` × 6 @ L827,1869,1875,2326,2350,2352
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.embedded · 676f 子组 embedded：Δ +8.1pp，BH-FDR p=0.034，Bonferroni p=0.34** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+8.1pp` × 0 @ L
  - ✓ `+8.1` × 2 @ L2331,2353
  - ✗ `0.034` × 0 @ L
  - ✗ `0.344` × 0 @ L
  - ✓ `74` × 15 @ L805,826,889,1565,1567,1629,1631,1714
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.odr_link · 676f 子组 odr_link：Δ +6.7pp，BH-FDR p=1，Bonferroni p=1** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+6.7pp` × 1 @ L2358
  - ✓ `+6.7` × 2 @ L2354,2358
  - ✗ `1.000` × 0 @ L
  - ✗ `1.000` × 0 @ L
  - ✓ `15` × 19 @ L464,588,710,951,1133,1181,1329,1578
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F09x · 676f 子组检验族大小 11** — consistent/active `✓`
- 源：`data/a5_676f_results.json`
  - ✓ `11` × 32 @ L16,108,345,445,526,552,824,826
**F10x.planted_false · 676f 真实缺陷 planted=false: FD 64.7% (22/34)，Δ +29.4pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `64.7` × 1 @ L2364
  - ✗ `22/34` × 0 @ L
  - ✓ `+29.4pp` × 1 @ L2365
  - ✗ `14.1, 44.7` × 0 @ L
  - ✓ `2.0\times10^{-3}` × 1 @ L2365
  - ✓ `35.3` × 2 @ L2326,2364
**F10x.planted_true · 676f planted=true: FD 53.9% (287/532)，Δ +23.7pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `53.9` × 1 @ L2366
  - ✗ `287/532` × 0 @ L
  - ✓ `+23.7pp` × 1 @ L2366
  - ✗ `20.1, 27.3` × 0 @ L
  - ✓ `2.4\times10^{-38}` × 1 @ L2366
  - ✓ `30.3` × 1 @ L2366
**F11x · 676f 资产诊断：8 资产各自 catch 率；wunsequenced/compile-time 100% unknown（退化）** — consistent/active `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `35.1` × 1 @ L2250
  - ✓ `399` × 1 @ L2250
  - ✓ `0.88` × 6 @ L14,1061,2250,2251,2252,2255
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
  - ✓ `0` × 265 @ L14,18,116,169,223,224,225,227
  - ✓ `100` × 24 @ L587,596,824,826,1327,1329,1343,1353
  - ✓ `12.6` × 1 @ L2254
  - ✓ `143` × 1 @ L2254
  - ✓ `15.0` × 2 @ L2253,2347
  - ✓ `170` × 3 @ L1120,2253,2443
  - ✓ `3.34` × 1 @ L2253
  - ✓ `0.9` × 1 @ L1621
  - ✓ `10` × 39 @ L31,32,113,379,449,459,525,526
  - ✓ `22.4` × 1 @ L2252
  - ✓ `255` × 2 @ L1779,2252
  - ✓ `0.88` × 6 @ L14,1061,2250,2251,2252,2255
  - ✓ `23.6` × 1 @ L2251
  - ✓ `268` × 1 @ L2251
  - ✓ `0.88` × 6 @ L14,1061,2250,2251,2252,2255
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
  - ✓ `0` × 265 @ L14,18,116,169,223,224,225,227
  - ✓ `100` × 24 @ L587,596,824,826,1327,1329,1343,1353
  - 注：退化资产是 A5 主/并列分析差异的唯一来源
**G01x · 676g 总盘：n=1147，catch 707，miss 440，盲区比 38.4%** — consistent/active `✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `1147` × 15 @ L106,155,217,372,381,481,895,1560
  - ✓ `707` × 3 @ L1560,1617,2040
  - ✓ `440` × 3 @ L481,1560,1617
  - ✓ `38.4` × 11 @ L109,217,318,329,481,669,895,1561
**G02x · 676g 互补性：6 资产并集 61.6%，最佳单资产 35.6%** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `61.6` × 3 @ L318,1618,2438
  - ✓ `707` × 3 @ L1560,1617,2040
  - ✓ `35.6` × 2 @ L1618,1620
**G03x · 676g 逐资产覆盖率（asan/ubsan/tsan/compiler-warn/cross-compile/linker）** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `35.6` × 2 @ L1618,1620
  - ✓ `23.5` × 1 @ L1620
  - ✓ `22.9` × 1 @ L1620
  - ✓ `12.5` × 3 @ L825,1620,2174
  - ✓ `10.6` × 2 @ L1621,2331
  - ✓ `0.9` × 1 @ L1621
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
  - ✓ `0.0` × 24 @ L344,432,455,553,738,826,899,902
**G04x · 676g 按 planted：true 41.0% [38.0, 44.1]；false 21.6% [13.8, 32.3]** — consistent/active `✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `41.0` × 2 @ L1564,1628
  - ✓ `38.0, 44.1` × 2 @ L1564,1628
  - ✓ `21.6` × 4 @ L539,1281,1565,1628
  - ✓ `13.8, 32.3` × 2 @ L1565,1628
  - ✓ `74` × 15 @ L805,826,889,1565,1567,1629,1631,1714
**G05x · 676g 盲区分带：18 个类型 >50% 盲；类型总数 70** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `18` × 12 @ L37,167,168,401,492,658,719,1204
  - ✓ `70` × 3 @ L37,1493,1792
  - ✓ `50` × 20 @ L329,483,700,710,719,895,934,1353
**G06x · 676g TSan 稳定性：3/180 不稳定（1.7%）** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `3` × 79 @ L17,25,27,110,158,209,314,404
  - ✓ `180` × 3 @ L1574,1632,2252
  - ✓ `1.7` × 7 @ L820,867,1575,1633,2331,2346,2347
**E01 · clang-analyzer holdout 48.8% (20/41) p=1.2e-4** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `48.8` × 3 @ L1573,1670,2330
  - ✗ `20/41` × 0 @ L
  - ✓ `1.2\times10^{-4}` × 1 @ L1670
**E02 · cppcheck holdout 41.5% (17/41) p=1.5e-5** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `41.5` × 4 @ L109,491,1671,1854
  - ✗ `17/41` × 0 @ L
  - ✓ `1.5\times10^{-5}` × 1 @ L1671
**E03 · cppcheck corpus 54.7% (35/64) p=0.38331031799316406** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `54.7` × 1 @ L1671
  - ✗ `35/64` × 0 @ L
  - ✓ `0.383` × 1 @ L1671
**E03b · cppcheck corpus Δ +7.8pp CI[-6.1, 21.7]（CI 跨 0 ⇒ tie）** — consistent/active `✓✓✗`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+7.8pp` × 1 @ L1676
  - ✓ `-6.1, 21.7` × 1 @ L1676
  - ✗ `(13,8)` × 0 @ L
**E04 · E9 附录 StrictA 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1670,1671
  - ✓ `1/11` × 2 @ L1670,1671
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E05 · E9 附录 cppcheck 主口径 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1670,1671
  - ✓ `1/11` × 2 @ L1670,1671
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E06 · E9 附录：holdout Δ(FD−StrictA) +34.1pp [19.6, 48.7]，对子 (14,0)** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+34.1pp` × 1 @ L1675
  - ✓ `19.6, 48.7` × 1 @ L1675
  - ✓ `(14,0)` × 1 @ L1675
**E07 · E9 附录：corpus StrictA 34.4% (22/64)，Δ +28.1pp 对子 (23,5)，p=9.1e-4** — consistent/active `✓✗✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `34.4` × 1 @ L1670
  - ✗ `22/64` × 0 @ L
  - ✓ `+28.1pp` × 1 @ L1676
  - ✓ `(23,5)` × 1 @ L1676
  - ✓ `9.1\times10^{-4}` × 1 @ L1670
**E08 · E9 附录：corpus 分层 FD/ct/cp（sanitizer 29/17/26；compiler-warn 9/5/8；cross-compile 2/0/1）** — consistent/active `✗✗✓✓✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✗ `29 / 17 / 26` × 0 @ L
  - ✗ `9 / 5 / 8` × 0 @ L
  - ✓ `2 / 0 / 1` × 1 @ L1681
  - ✓ `12` × 26 @ L45,436,440,449,459,463,699,720
  - ✓ `FD 29 vs clang-analyzer 17 / cppcheck 26` × 1 @ L1680
  - ✓ `FD 9 / cppcheck 8` × 1 @ L1680
  - ✓ `2 / 0 / 1` × 1 @ L1681
**E10 · E9 附录：clang-tidy 主口径 holdout 100% recall / 100% FPR（零区分度 ⇒ 该口径被弃用）** — consistent/active `✗✓✗✓✗✗`
- 源：`data/673e_comparison_stats.json`
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 24 @ L587,596,824,826,1327,1329,1343,1353
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 24 @ L587,596,824,826,1327,1329,1343,1353
  - ✗ `41/41` × 0 @ L
  - ✗ `11/11` × 0 @ L
**E09 · E9 附录：8 个反向对（工具 catch / FD miss）** — consistent/active `✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `8` × 55 @ L16,155,373,445,458,700,756,824
**F01 · 外部锚点子集 A（准则原文）28.6% (10/35) CI[14.6,46.3]** — consistent/active `✓✗✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `28.6` × 3 @ L709,828,893
  - ✗ `10/35` × 0 @ L
  - ✗ `14.6, 46.3` × 0 @ L
**F02 · 外部锚点子集 B（UB 片段重建）80.0% (12/15)** — consistent/active `✓✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `80.0` × 2 @ L710,969
  - ✗ `12/15` × 0 @ L
**F03 · 外部锚点合计 44.0% (22/50)；扫描规则 87** — consistent/active `✓✗✓✓✓✓✓✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `44.0` × 1 @ L710
  - ✗ `22/50` × 0 @ L
  - ✓ `22` × 12 @ L493,1178,1179,1204,1620,1658,1686,1844
  - ✓ `50` × 20 @ L329,483,700,710,719,895,934,1353
  - ✓ `87` × 6 @ L708,796,972,973,1151,2207
  - ✓ `35` × 23 @ L373,501,534,642,671,709,796,1152
  - ✓ `15` × 19 @ L464,588,710,951,1133,1181,1329,1578
  - ✗ `11/60` × 0 @ L
**F04 · LLM 臂：GLM-4 12/12 vs FD 6/12；对照误报 4/8 = 50%** — consistent/active `✓✓✓✓✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✓ `12/12` × 2 @ L699,2192
  - ✓ `6/12` × 1 @ L699
  - ✓ `4/8` × 2 @ L700,2192
  - ✓ `50.0` × 2 @ L719,1626
  - ✓ `50.0` × 2 @ L719,1626
  - 注：FD 的 6/12 由 fd_detect_rate_pct=50.0% × llm_n 重算得到
**F05 · LLM 臂配对 b/c = (0,6)，p=0.03125** — consistent/active `✗✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✗ `0,6` × 0 @ L
  - ✓ `0.031` × 1 @ L701
**G01 · 变异（core）110/114 = 96.5%** — consistent/active `✓✓✗`
- 源：`data/656_mutation_report.json`
  - ✓ `110/114` × 2 @ L958,973
  - ✓ `96.5` × 3 @ L901,973,1153
  - ✗ `91.3, 99.0` × 0 @ L
**G02 · 变异（all-scope）130/159 = 81.8%** — consistent/active `✓✓`
- 源：`data/656_mutation_report_all.json`
  - ✓ `130/159` × 1 @ L958
  - ✓ `81.8` × 1 @ L1153
**G03 · 缺陷重注入 6/6 = 100%；total 15；软覆盖 12/15** — consistent/active `✓✗✓`
- 源：`data/defect_injection_661.json`
  - ✓ `6/6` × 2 @ L824,826
  - ✗ `12/15` × 0 @ L
  - ✓ `15` × 19 @ L464,588,710,951,1133,1181,1329,1578
**H01 · 样本量：独立两比例 0.35→0.50 ⇒ n=170** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=None, α=0.05, power=0.8, recomputed=169.09`
  - ✓ `170` × 3 @ L1120,2253,2443
  - ✗ `170 (holdout)` × 0 @ L
**H02 · 样本量：独立两比例 0.35→0.55 ⇒ n=96** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.55,psi=None, α=0.05, power=0.8, recomputed=95.77`
  - ✓ `96` × 5 @ L901,973,1121,1153,2442
  - ✗ `96 (holdout)` × 0 @ L
**H03 · 样本量：独立两比例 0.35→0.45 ⇒ n=376** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.45,psi=None, α=0.05, power=0.8, recomputed=375.27`
  - ✓ `376` × 1 @ L1122
  - ✗ `376 (holdout)` × 0 @ L
**H04 · 样本量：配对 ψ=0.3 ⇒ n=103** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.3, α=0.05, power=0.8, recomputed=102.26`
  - ✓ `103` × 3 @ L1123,2218,2231
  - ✗ `103 (holdout)` × 0 @ L
**H05 · 样本量：配对 ψ=0.4 ⇒ n=138** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.4, α=0.05, power=0.8, recomputed=137.15`
  - ✓ `138` × 1 @ L1124
  - ✗ `138 (holdout)` × 0 @ L
**H06 · 样本量：配对 ψ=0.5 ⇒ n=173** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.5, α=0.05, power=0.8, recomputed=172.04`
  - ✓ `173` × 6 @ L951,1125,1578,1819,2269,2370
  - ✗ `173 (holdout)` × 0 @ L
**K01 · tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现** — consistent/unpinned_no_artifact `✓✓`
- 源：`data/656_mutation_report*.json 现存值为 110/114 与 130/159；全仓扫描 `30/48` 无产物命中（唯一产出是更早被覆盖的报告）`
  - ✓ `62.5` × 8 @ L805,826,889,957,968,1156,1669,2145
  - ✓ `30/48` × 2 @ L957,968
  - 注：论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注）
**K02 · tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径** — consistent/unpinned_retired_caliber `✓`
- 源：`仅能追溯到 research/paper_v0.4.md 与 data/669_caliber_report.json::doc_sightings；对应 -O1 单档产物已被 665/668 双档口径取代`
  - ✓ `66.7` × 3 @ L301,959,970
  - 注：该值口径已退休，只能作为“当时口径下读到的数”引用
**I01 · Static holdout 1/41 CI ⇒ [0.1, 12.9]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(1,41)])"`
  - ✓ `0.1, 12.9` × 1 @ L824
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I02 · Random† holdout 4/41 CI ⇒ [2.7, 23.1]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(4,41)])"`
  - ✓ `2.7, 23.1` × 1 @ L825
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I03 · FD holdout 34/41 CI ⇒ [67.9, 92.8]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,41)])"`
  - ✓ `67.9, 92.8` × 4 @ L805,826,889,975
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I04 · Caliber B holdout 34/42 CI ⇒ [65.9, 91.4]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,42)])"`
  - ✓ `65.9, 91.4` × 2 @ L806,807
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I05 · Static corpus 11/64 CI ⇒ [8.9, 28.7]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(11,64)])"`
  - ✓ `8.9, 28.7` × 1 @ L824
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I06 · Random† corpus 14/64 CI ⇒ [12.5, 34.0]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(14,64)])"`
  - ✓ `12.5, 34.0` × 1 @ L825
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I07 · FD corpus 40/64 CI ⇒ [49.5, 74.3]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,64)])"`
  - ✓ `49.5, 74.3` × 3 @ L805,826,889
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I08 · Caliber B corpus 40/73 CI ⇒ [42.7, 66.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,73)])"`
  - ✓ `42.7, 66.5` × 1 @ L806
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I09 · Caliber C corpus 40/76 CI ⇒ [40.8, 64.2]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,76)])"`
  - ✓ `40.8, 64.2` × 1 @ L807
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I10 · 对照 FPR 0/11 CI ⇒ [0.0, 28.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(0,11)])"`
  - ✓ `0.0, 28.5` × 1 @ L826
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I11 · corpus 分层 sanitizer 29/34 CI ⇒ [68.9, 95.0]** — retired/superseded:689重构 `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(29,34)])"`
  - ✗ `68.9, 95.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I12 · corpus 分层 compiler-warn 9/18 CI ⇒ [26.0, 74.0]** — retired/superseded:689重构 `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(9,18)])"`
  - ✗ `26.0, 74.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I13 · corpus 分层 cross-compile 2/12 CI ⇒ [2.1, 48.4]** — retired/superseded:689重构 `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(2,12)])"`
  - ✗ `2.1, 48.4` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**I14 · 缺陷重注入 6/6 CI ⇒ [54.1, 100.0]** — retired/superseded:689重构 `✗`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(6,6)])"`
  - ✗ `54.1, 100.0` × 0 @ L
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致
**D03 · A5 矩阵 105×8 = 840 次 detect** — consistent/superseded_by_676f `✓✗✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `105` × 1 @ L2135
  - ✗ `840` × 0 @ L
  - ✓ `8` × 55 @ L16,155,373,445,458,700,756,824
**A19 · ±5pp 缺口：holdout 还差 195，corpus 还差 314** — consistent/active `✓✓`
- 源：`sample_size_672k.±5pp.n − 当前可测 n`
  - ✓ `195` × 1 @ L1132
  - ✓ `314` × 1 @ L1132
**D11 · clone-aware 重切分 Δ +23.0~+26.7pp（677b，逐 split 为 +23.02/+25.70）** — consistent/active `✓✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_a5_results_family_random.json / _family_stratified.json`
  - ✓ `23.02` × 2 @ L1766,2291
  - ✓ `25.70` × 2 @ L1767,2291
**D12 · cluster bootstrap 有效 n≈133–140（677b，design effect ≈4.1–4.3）** — consistent/active `✗✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_cluster_bootstrap.json`
  - ✗ `133` × 0 @ L
  - ✓ `140` × 12 @ L322,345,449,651,894,899,1433,1815
**D13 · 非退化池选择效应 +11.31pp（677c，k=1，p=6.02e-08）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `11.31` × 5 @ L16,445,899,2284,2302
**D14 · 退化资产对均值的贡献 ≈+12.81pp（677c）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `12.81` × 1 @ L2304
**Z01 · 689 TOST：±10pp 未过，90% CI [-10.61, 5.52]pp，p_TOST=0.064** — consistent/active `✓✓✓`
- 源：`current_numbers.reframed_689.equivalence_tost ← data/689_equivalence_test.json`
  - ✓ `-10.61` × 5 @ L32,113,525,1857,2043
  - ✓ `5.52` × 5 @ L32,113,525,1857,2043
  - ✓ `0.064` × 3 @ L525,2043,2044
**E02 · 689 TOST 最小通过 margin 10.61pp（deff 校正 11.67pp）** — consistent/active `✓✓`
- 源：`data/689_equivalence_test.json`
  - ✓ `10.61` × 9 @ L32,113,525,526,1857,1858,2043,2044
  - ✓ `11.67` × 2 @ L526,2046
**E03 · 689 标准化：正向 -17.92pp（R_syn_std=77.01%），反向 +1.70pp，类型级 -13.52pp** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.standardized_analysis ← data/689_standardized_analysis.json`
  - ✓ `-17.92` × 5 @ L33,529,541,1858,2056
  - ✓ `77.01` × 2 @ L529,2055
  - ✓ `1.70` × 2 @ L530,2058
  - ✓ `-13.52` × 2 @ L537,2059
**E04 · 689 环境：真实 59.09%→23.64%（-35.45pp，Δunknown=0），clang↔g++ 93.5%** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.environment_metrics ← data/689_environment_metrics.json`
  - ✓ `59.09` × 12 @ L111,314,492,499,523,527,904,1849
  - ✓ `23.64` × 4 @ L111,501,2070
  - ✓ `35.45` × 4 @ L501,642,1445,1454
  - ✓ `93.5` × 4 @ L504,660,1917,2074
**Z11 · 691 机制级：Pool A k=1 +11.31pp (p=6.0e-8)；k=2/k=3 +7.42pp；k=4 0.00pp** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_691.mechanism_level_poolA_vs_single_random ← data/677c_a5_nondegenerate_results.json`
  - ✓ `11.31` × 5 @ L16,445,899,2284,2302
  - ✓ `6.0` × 4 @ L16,445,899,2302
  - ✓ `7.42` × 6 @ L16,17,445,2284,2302
  - ✓ `0.00` × 9 @ L446,594,1341,2303,2426,2428,2429,2430
**Z12 · 691 四个 κ（AI 自一致）：0.727 / 0.789 / 0.437 / 0.157** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_691.label_kappa_ai_self_consistency ← data/682_kappa.json`
  - ✓ `0.727` × 1 @ L618
  - ✓ `0.789` × 1 @ L618
  - ✓ `0.437` × 2 @ L18,619
  - ✓ `0.157` × 3 @ L18,487,619
**Z13 · 691 治理计数：452 ledger 事件 / 67 规则 / rules_sha256 v1.0.0** — consistent/active `✓✓`
- 源：`current_numbers.reframed_691.governance`
  - ✓ `452` × 8 @ L19,263,270,840,891,930,1163,1377
  - ✓ `67` × 13 @ L19,264,805,826,840,889,975,982
**Z14 · 691 池计数：Pool B ≡ Pool C（同一六资产集）；9 个不同 (池,k) 块 / 14 块实例** — consistent/active `✓✓✓`
- 源：`current_numbers.reframed_691.pools ← data/677c_asset_pools.json + 677c_evolution_operator_results.json`
  - ✓ `2` × 85 @ L16,18,108,154,218,226,228,230
  - ✓ `9` × 38 @ L15,300,318,458,534,537,548,634
  - ✓ `14` × 16 @ L457,548,552,825,902,972,1063,1675
