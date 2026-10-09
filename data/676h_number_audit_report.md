# 676h · 论文数字可追溯性审计报告

- 生成时间：2026-10-09T10:42:56+08:00
- 被审计稿件：`research/latex/queyi_neurips2027_v1.1.tex`（正文 None 页 / 全稿 40 页，取自编译日志）
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

扫描到数字 token **1860** 个（已排除注释行与导言区行）。分类：

| 类别 | 数量 | 占比 |
|---|---|---|
| claim | 1423 | 76.5% |
| unclassified | 156 | 8.4% |
| design_constant | 69 | 3.7% |
| batch_id | 60 | 3.2% |
| method_constant | 40 | 2.2% |
| format_layout | 26 | 1.4% |
| repro_command | 24 | 1.3% |
| year | 11 | 0.6% |
| system_constant | 9 | 0.5% |
| logic_constant | 9 | 0.5% |
| engineering_narrative | 9 | 0.5% |
| external_literature | 6 | 0.3% |
| historical_retired | 5 | 0.3% |
| structural | 4 | 0.2% |
| sample_id | 4 | 0.2% |
| cited_context | 3 | 0.2% |
| external_regulation | 2 | 0.1% |

未归类 token：156 个（前 60 条见下；全量在 json 里）。

| 行 | token | 上下文 |
|---|---|---|
| 301 | `40` | `\emph{same} 40 catches; a flag change once moved holdout recall $66.7\%\to87.5\%$ with the` |
| 373 | `34` | `across 34 normalized types (8 families), including 64 corpus-null controls and 35 hung` |
| 374 | `110` | `samples. \emph{Source-derived real-defect corpus} (110 samples): minimal reconstructions of` |
| 375 | `30` | `defects from 30+ real projects (CVE/NVD-verified mechanisms, responses frozen; \emph{not}` |
| 399 | `13.3` | `Four profiles are declared: \texttt{wsl-gcc-13.3} (asan/ubsan/tsan, primary),` |
| 401 | `200` | `\texttt{wsl-clang-18.1.3} (200-sample stratified replication), and MSVC/clang-cl (absent on` |
| 429 | `24` | `\paragraph{F1. A $+24$pp ``selection gain'' is mostly measurement-pool composition` |
| 436 | `24.03` | `\textbf{composition-dominated within the pools measured} ($+24.03$pp at $k{=}4$,` |
| 446 | `5` | `$1/\binom{5}{4}{=}0.2$). Against the 2000-draw random \emph{mean} the same tiers read` |
| 462 | `13` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 462 | `34` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 464 | `60` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 464 | `62` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 469 | `86.96` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 469 | `30.77` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 472 | `52.2` | `harder on real defects than on synthetic ones (type punning $-52.2$pp, logic $-22.5$pp,` |
| 478 | `65` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 478 | `110` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 480 | `39` | `\textbf{23.64\%} ($-35.45$pp) with \emph{no} unknown increase: 39 catches depend on Linux` |
| 490 | `13.3` | `($n_{\text{env}}{=}1$; E1 \texttt{wsl-gcc-13.3} vs.\ E2 \texttt{windows-native-mingw}), \emph{not}` |
| 511 | `36.9` | `instrument is good at (bounds$+$memory$+$integer $=64.5\%$ of samples vs.\ $36.9\%$ in the` |
| 513 | `31` | `(\texttt{language\_oop}/logic: real $1/31$ vs.\ synthetic $9/35$). Two corpora can share a` |
| 536 | `17496` | `simple optimal selection already exists (all 17496 triples checked; greedy attains ratio` |
| 566 | `55.84` | `A degradation-grade replication in LLM-as-a-judge evaluation scores $55.84/100$ on a` |
| 581 | `19` | `We report five threat classes with direction and mitigation status (the 19-item table and` |
| 599 | `6.6` | `$6.6\%\to14.3\%$ under $\le15\%$ flips, though contrast directions are stable).` |
| 604 | `110` | `The 110-sample source-derived corpus improves ecological validity but is` |
| 630 | `5` | `rate by $-16.36$pp. Cross-run stability: 5\% grid flips; the shadow-mapped` |
| 639 | `24` | `detecting that collapse. On a software-verification apparatus: a $+24$pp selection gain was` |
| 643 | `17.9` | `explained by a $-17.9$pp composition offset; and failure-driven evolution produced no` |
| 941 | `30` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 941 | `17` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 1293 | `703` | `\paragraph{(10) Cross-domain transfer to LLM-as-a-judge evaluation (added in 703).}` |
| 1295 | `240` | `LLM-judge benchmarks (240 samples downloaded live), a ``longer is better'' lazy judge agrees with` |
| 1296 | `55.83` | `the human-preferred side only $44.17\%$ of the time on JudgeBench---so on $55.83\%$ of samples` |
| 1299 | `55.84` | `LLM arm scores $55.84/100$ on a four-component transfer scale (caliber $15.62$, environment` |
| 1302 | `33.33` | `$1.03$pp against $33.33$pp in C++, because an LLM aggregation rule acts on a single judge's` |
| 1370 | `13.3` | `The experiment ran the same samples under E1 (\texttt{wsl-gcc-13.3}; six assets) and E2` |
| 1389 | `200` | `catch   & 140 & 200 & 0 & 140 & 0 & 200 \\` |
| 1389 | `200` | `catch   & 140 & 200 & 0 & 140 & 0 & 200 \\` |
| 1390 | `226` | `miss    & 0   & 226 & 0 & 0   & 0 & 226 \\` |
| 1390 | `226` | `miss    & 0   & 226 & 0 & 0   & 0 & 226 \\` |
| 1397 | `200` | `Under un-aware accounting the matrix looks like a \emph{capability loss}: 200 samples move` |
| 1400 | `200` | `the same 200 samples move catch$\to$unknown, and the 226 misses move miss$\to$unknown: the` |
| 1400 | `226` | `the same 200 samples move catch$\to$unknown, and the 226 misses move miss$\to$unknown: the` |
| 1401 | `426` | `conclusion changes from ``capability dropped 35.45pp'' to ``426 of 566 samples were not measured` |
| 1423 | `4096` | `$|A|{=}3$, \emph{all} $2^{4\times3}{=}4096$ coverage structures, seven aggregation families` |
| 1435 | `4096` | `(4096 structures, seven aggregation families), not a proof for arbitrary domains; and A2 and A5` |
| 1449 | `38.24` | `high-blindness share (38.24\% under 34 classes vs.\ 25.71\% under 70). Within this finite domain` |
| 1449 | `34` | `high-blindness share (38.24\% under 34 classes vs.\ 25.71\% under 70). Within this finite domain` |
| 1449 | `25.71` | `high-blindness share (38.24\% under 34 classes vs.\ 25.71\% under 70). Within this finite domain` |
| 1482 | `17` | `II  & environment E1$\to$E2       & $0.3534$ & $\mathbf{17}$  & 7 \\` |
| 1590 | `200` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `219` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `149` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `95` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `99` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `90` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1590 | `88` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1615 | `93` | `676m unification, which is exactly why the vocabulary was unified. (iii) $93\%$ of samples are` |

## 5. 每条检察的命中明细

**A01 · holdout 可测检出率 82.9% (34/41) CI[67.9,92.8]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `82.9` × 9 @ L776,797,860,946,1127,1777,1840,1906
  - ✓ `34/41` × 5 @ L776,797,860,946,1127
  - ✓ `67.9, 92.8` × 4 @ L776,797,860,946
**A02 · corpus 可测检出率 62.5% (40/64) CI[49.5,74.3]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `62.5` × 8 @ L776,797,860,928,939,1127,1528,1906
  - ✓ `40/64` × 4 @ L776,797,860,1127
  - ✓ `49.5, 74.3` × 3 @ L776,797,860
**A03 · corpus 全样本口径 52.6%** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `52.6` × 2 @ L778,1528
**A04 · Static 臂 holdout 2.4% (1/41) / corpus 17.2% (11/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `2.4` × 3 @ L791,795,1749
  - ✓ `1/41` × 1 @ L795
  - ✓ `17.2` × 1 @ L795
  - ✓ `11/64` × 1 @ L795
**A05 · Random† 臂 holdout 9.8% (4/41) / corpus 21.9% (14/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `9.8` × 1 @ L796
  - ✓ `4/41` × 1 @ L796
  - ✓ `21.9` × 1 @ L796
  - ✓ `14/64` × 1 @ L796
**A06 · Δ(Static→FD) holdout +80.5pp CI[68.4,92.6] p=2.3e-10 h=1.98** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+80.5pp` × 1 @ L798
  - ✓ `68.4, 92.6` × 1 @ L798
  - ✓ `2.3\times10^{-10}` × 1 @ L724
  - ✓ `1.98` × 1 @ L724
**A07 · Δ(Random†→FD) holdout +73.2pp CI[59.6,86.7] p=1.9e-9 h=1.65** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+73.2pp` × 1 @ L799
  - ✓ `59.6, 86.7` × 1 @ L799
  - ✓ `1.9\times10^{-9}` × 1 @ L726
  - ✓ `1.65` × 1 @ L726
**A08 · Δ(Static→FD) corpus +45.3pp CI[33.1,57.5] p=3.7e-9 h=0.97** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+45.3pp` × 1 @ L798
  - ✓ `33.1, 57.5` × 1 @ L798
  - ✓ `3.7\times10^{-9}` × 1 @ L725
  - ✓ `0.97` × 3 @ L725,1077,2272
**A09 · Δ(Random†→FD) corpus +40.6pp CI[28.6,52.7] p=3.0e-8 h=0.85** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+40.6pp` × 1 @ L799
  - ✓ `28.6, 52.7` × 1 @ L799
  - ✓ `3.0\times10^{-8}` × 1 @ L727
  - ✓ `0.85` × 1 @ L727
**A10 · 配对不一致对 (b, c)（tab:e5 四行）** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `(33, 0)` × 1 @ L724
  - ✓ `(29, 0)` × 1 @ L725
  - ✓ `(30, 0)` × 1 @ L726
  - ✓ `(26, 0)` × 1 @ L727
  - 注：四个对比都是 c=0 结构（对手的 catch 是 FD catch 的子集）
**A11 · 对照假阳性 0.0% (0/11)** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `0.0\% (0/11)` × 4 @ L797,922,1906,1956
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
**A12 · 缺陷重注入 6/6 = 100%** — consistent/active `✓✗`
- 源：`data/current_numbers.json`
  - ✓ `6/6` × 2 @ L795,797
  - ✗ `100.0` × 0 @ L
**A13 · CP95 半宽 12.5pp（holdout）** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `12.5` × 3 @ L796,1557,1824
**A14 · 扩样前 holdout 81.0% (17/21) CI[58.1,94.6]** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `81.0` × 3 @ L777,778,945
  - ✓ `17/21` × 1 @ L945
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
  - ✓ `236` × 4 @ L869,922,1099,1103
  - ✓ `378` × 4 @ L869,922,1099,1103
**A18 · ±10pp 半宽所需样本量 holdout 61 / corpus 97** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `61` × 12 @ L318,502,506,922,944,1098,1822,1873
  - ✓ `97` × 5 @ L922,1098,1658,2035,2288
**B01 · holdout 累计 catch/miss/unknown = 34/7/1，分母 41** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/41` × 5 @ L776,797,860,946,1127
  - ✓ `1` × 167 @ L16,17,38,71,107,115,150,169
**B02 · holdout 口径 B（unknown→miss）34/42 = 81.0%** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/42` × 2 @ L777,778
  - ✓ `81.0` × 3 @ L777,778,945
**B03 · holdout 分层 sanitizer 84.6% (33/39)** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `84.6` × 1 @ L692
  - ✓ `33/39` × 1 @ L692
**B04 · corpus 分层 sanitizer 85.3% (29/34) / compiler-warn 50.0% (9/18) / cross-compile 16.7% (2/12)** — consistent/active `✓✓✓✓✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `85.3` × 1 @ L690
  - ✓ `29/34` × 1 @ L690
  - ✓ `50.0` × 2 @ L690,1830
  - ✓ `9/18` × 1 @ L690
  - ✓ `16.7` × 3 @ L690,1556,1950
  - ✓ `2/12` × 1 @ L691
**B05 · corpus 口径 B（unknown→miss）40/73 = 54.8%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/73` × 1 @ L777
  - ✓ `54.8` × 1 @ L777
**B06 · corpus 口径 C（全样本）40/76 = 52.6%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/76` × 1 @ L778
  - ✓ `52.6` × 2 @ L778,1528
**B07 · corpus 分层 Excluded unknown=9 / not_error=3** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `9` × 37 @ L15,300,318,513,516,527,605,660
  - ✓ `3` × 78 @ L17,25,27,110,158,209,314,404
**B08 · holdout 新子集 17/20 = 85.0%（round5）** — retired/superseded:689重构 `✗✗`
- 源：`data/holdout_reveal_5_672h.json`
  - ✗ `17/20` × 0 @ L
  - ✗ `85.0` × 0 @ L
  - 注：689 重构：round5 子集数字随旧正文段落移出正文（数据仍在产物）
**B09 · 历史批次 669：87.5%（14/16）与 CI[61.7, 98.4]** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `87.5` × 4 @ L767,943,944,1122
**B10 · 历史批次 660：80.0%（batch compare before）** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `80.0` × 2 @ L681,940
**C01 · 判决规则数 67（len(gate_engine.RULES)）** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES))"`
  - ✓ `67` × 13 @ L19,264,776,797,811,860,946,953
**C02 · 权威账本事件数 452（decision_event_v2_ledger.jsonl 非空行）** — consistent/active `✓`
- 源：`python -c "n=sum(1 for l in open(r'data/authority/decision_event_v2_ledger.jsonl',encoding='utf-8') if l.strip());print(n)"`
  - ✓ `452` × 8 @ L19,263,270,811,862,901,1134,1333
**C03 · 实卡数 atoms_real = 42（counts_659.py 现算）** — consistent/active `✓`
- 源：`python tools/counts_659.py --json`
  - ✓ `42` × 6 @ L777,778,1131,2209,2210
**C04 · Verifier Coverage = 31/42 = 73.8%** — consistent/active `✗✓`
- 源：`atoms/**/ATOM-*.md 排除 draft650/；status∈{verified,red-team-verified,machine-verified}`
  - ✗ `31/42` × 0 @ L
  - ✓ `73.8` × 2 @ L38,1130
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
  - ✓ `44` × 5 @ L681,1296,1731,1768,1832
  - ✓ `16` × 16 @ L630,690,768,943,1300,1520,1556,1676
  - ✓ `7` × 42 @ L16,17,45,108,308,345,443,444
  - 注：旧稿的 0/176/55 不可复现，已按现算值纠正
**C08 · 边界卡 26 张；provenance 完整 26/26；scope 完整 0/26** — consistent/active `✓✗✓`
- 源：`data/boundary_provenance_658.json`
  - ✓ `26` × 12 @ L727,868,896,921,1572,1652,1674,1709
  - ✗ `26/26` × 0 @ L
  - ✓ `0/26` × 5 @ L868,896,921,1572,2095
  - 注：provenance 完整 = provenance 字典字段数 ≥3（mutationset/generator/evidence）
**N01 · 81.2% 必须在出现的每一处都被标为从未落盘/作废** — consistent/active `✓`
- 源：`673c/676h 诚实边界：81.2% 不得作为已落盘结果引用`
  - ✓ `81.2` × 1 @ L
  - 注：若 81.2 出现在没有 never-landed 标注的句子里 ⇒ 违反
**D01 · A5 holdout 主端点 FD 90.0% (18/20) vs Random 35.0%** — consistent/superseded_by_676f `✓✗✓✗✓✗✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `90.0` × 2 @ L1519,1863
  - ✗ `18/20` × 0 @ L
  - ✓ `35.0` × 5 @ L767,1123,1153,1519,1542
  - ✗ `7/20` × 0 @ L
  - ✓ `10.0` × 1 @ L1153
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
  - ✓ `55.0` × 1 @ L1732
  - ✗ `23.4` × 0 @ L
**D01c · A5 设计量：holdout 派生 n=21 / 评估 n=20** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `21` × 13 @ L518,796,921,945,946,1252,1300,1653
  - ✓ `20` × 19 @ L228,230,308,343,473,709,825,921
  - ✓ `4` × 79 @ L25,112,289,310,321,344,433,435
  - ✓ `2000` × 9 @ L290,446,1658,1687,1877,2032,2036,2210
  - ✓ `8` × 54 @ L16,155,373,443,671,727,795,842
  - ✓ `41` × 31 @ L109,343,387,470,709,724,726,776
**D02 · A5 corpus 主端点 FD 81.25% (13/16) vs Random 37.5%** — consistent/superseded_by_676f `✓✓✓✗✓✗✗✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `81.2` × 4 @ L942,1551,1945,2092
  - ✓ `13/16` × 1 @ L1945
  - ✓ `37.5` × 1 @ L1519
  - ✗ `6/16` × 0 @ L
  - ✓ `37.5` × 1 @ L1519
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
  - ✓ `48` × 11 @ L921,928,939,946,1713,1777,1907,1912
  - ✓ `16` × 16 @ L630,690,768,943,1300,1520,1556,1676
  - ✓ `4` × 79 @ L25,112,289,310,321,344,433,435
  - ✓ `2000` × 9 @ L290,446,1658,1687,1877,2032,2036,2210
  - ✓ `8` × 54 @ L16,155,373,443,671,727,795,842
  - ✓ `64` × 25 @ L373,387,511,725,727,776,778,795
**F01x · 676f 样本簿记：1137 总样本；派生 571；评估 566** — consistent/active `✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `1137` × 11 @ L380,1164,1521,1579,1585,1591,1670,1996
  - ✓ `571` × 1 @ L1586
  - ✓ `566` × 25 @ L289,343,386,395,432,709,865,922
  - ✓ `1063` × 1 @ L1589
  - ✓ `74` × 15 @ L776,797,860,1589,1607,1736,1745,1769
  - ✓ `10` × 38 @ L31,32,113,379,447,504,505,595
**F02x · 676f 主端点（k=4，全 8 资产池）FD/Random/Static 三臂** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `54.6` × 4 @ L431,1651,1663,1711
  - ✓ `309/566` × 1 @ L1651
  - ✓ `30.6` × 7 @ L431,709,865,1652,1665,1710,1711
  - ✓ `173/566` × 1 @ L1652
  - ✓ `24.7` × 1 @ L1653
  - ✓ `140/566` × 1 @ L1653
  - ✓ `60.1` × 5 @ L1654,1713,1714,1715
  - ✓ `340/566` × 1 @ L1654
**F03x · 676f 主端点 Δ(FD−Random) +24.0pp CI[+20.5, +27.5] p=2.3e-41 h=0.49 (b=136, c=0)** — consistent/active `✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `+24.0pp` × 10 @ L29,45,107,306,343,432,709,870
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L343,709,1652,1711
  - ✓ `0.49` × 1 @ L1652
  - ✗ `(136,0)` × 0 @ L
**F04x · 676f 主端点 Δ(FD−Static) +29.9pp CI[+25.2, +34.5] p=1.9e-31** — consistent/active `✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+29.9pp` × 4 @ L709,865,1653,2075
  - ✗ `25.2, 34.5` × 0 @ L
  - ✓ `1.9\times10^{-31}` × 3 @ L709,865,1653
  - ✓ `0.62` × 1 @ L1653
**F05x · 676f 2000 次随机分布：FD 严格优于 97.6%（Random 均值 40.2%，SD 9.3pp）** — consistent/active `✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `97.6` × 2 @ L1658,2288
  - ✓ `40.2` × 1 @ L1659
  - ✓ `9.3` × 1 @ L1659
  - ✓ `2000` × 9 @ L290,446,1658,1687,1877,2032,2036,2210
**F06x · 676f 并列分析（剔退化资产）：Δ(FD−Random)=0.0pp p=1.0；Δ(FD−Static)=+30.6pp CI[+26.0,+35.1] p=8.1e-34** — consistent/active `✓✓✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
  - ✓ `1.0` × 20 @ L344,434,444,537,811,871,1069,1125
  - ✓ `+30.6pp` × 3 @ L709,865,1665
  - ✗ `26.0, 35.1` × 0 @ L
  - ✓ `8.1\times10^{-34}` × 1 @ L1665
  - ✓ `24.0` × 13 @ L29,45,107,306,343,432,709,870
  - ✗ `136/566` × 0 @ L
**F07x · 676f k 扫描（k=1..8）各档 Δ 与 p** — consistent/active `✗✓✗✓✓✓✗✓✗✓✓✓✗✓✗✗✓✓✓✓✗✓✓✓✗✓✗✓✓✓✓✓✗✓✓✓✗✓✗✓✓✓✗✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+33.0pp` × 0 @ L
  - ✓ `+33.0` × 1 @ L1708
  - ✗ `29.2, 36.9` × 0 @ L
  - ✓ `1.0\times10^{-56}` × 1 @ L1708
  - ✓ `33.0` × 2 @ L1708
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
  - ✗ `+30.7pp` × 0 @ L
  - ✓ `+30.7` × 1 @ L1709
  - ✗ `26.2, 35.3` × 0 @ L
  - ✓ `7.8\times10^{-35}` × 1 @ L1709
  - ✓ `45.1` × 1 @ L1709
  - ✓ `14.3` × 1 @ L1709
  - ✗ `+20.5pp` × 0 @ L
  - ✓ `+20.5` × 5 @ L343,709,1652,1710,1711
  - ✗ `16.5, 24.5` × 0 @ L
  - ✗ `2.1\times10^{-22}` × 0 @ L
  - ✓ `51.1` × 1 @ L1710
  - ✓ `30.6` × 7 @ L431,709,865,1652,1665,1710,1711
  - ✓ `+24.0pp` × 10 @ L29,45,107,306,343,432,709,870
  - ✓ `+24.0` × 13 @ L29,45,107,306,343,432,709,870
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L343,709,1652,1711
  - ✓ `54.6` × 4 @ L431,1651,1663,1711
  - ✓ `30.6` × 7 @ L431,709,865,1652,1665,1710,1711
  - ✗ `+20.7pp` × 0 @ L
  - ✓ `+20.7` × 1 @ L1712
  - ✗ `17.3, 24.0` × 0 @ L
  - ✓ `1.2\times10^{-35}` × 1 @ L1712
  - ✓ `59.4` × 1 @ L1712
  - ✓ `38.7` × 1 @ L1712
  - ✓ `+11.3pp` × 4 @ L345,1795,2075,2085
  - ✓ `+11.3` × 5 @ L345,1713,1795,2075,2085
  - ✗ `8.7, 13.9` × 0 @ L
  - ✓ `1.1\times10^{-19}` × 1 @ L1713
  - ✓ `60.1` × 5 @ L1654,1713,1714,1715
  - ✓ `48.8` × 3 @ L1713,1777,1907
  - ✗ `+10.6pp` × 0 @ L
  - ✓ `+10.6` × 1 @ L1714
  - ✗ `8.1, 13.1` × 0 @ L
  - ✓ `1.7\times10^{-18}` × 1 @ L1714
  - ✓ `60.1` × 5 @ L1654,1713,1714,1715
  - ✓ `49.5` × 4 @ L776,797,860,1714
  - ✗ `+0.0pp` × 0 @ L
  - ✗ `+0.0` × 0 @ L
  - ✓ `0.0, 0.0` × 1 @ L1715
  - ✗ `1.000` × 0 @ L
  - ✓ `60.1` × 5 @ L1654,1713,1714,1715
  - ✓ `60.1` × 5 @ L1654,1713,1714,1715
**F08x.undefined_behavior · 676f 子组 undefined_behavior：Δ +58.1pp，BH-FDR p=1e-06，Bonferroni p=1e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+58.1pp` × 0 @ L
  - ✓ `+58.1` × 1 @ L1727
  - ✓ `1.0\times10^{-6}` × 3 @ L1727,1728
  - ✓ `1.0\times10^{-6}` × 3 @ L1727,1728
  - ✓ `43` × 3 @ L767,1727,2361
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.memory_safety · 676f 子组 memory_safety：Δ +46.9pp，BH-FDR p=1e-06，Bonferroni p=3e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+46.9pp` × 0 @ L
  - ✓ `+46.9` × 1 @ L1728
  - ✓ `1.0\times10^{-6}` × 3 @ L1727,1728
  - ✓ `3.0\times10^{-6}` × 1 @ L1728
  - ✓ `49` × 6 @ L776,797,860,1714,1728,2112
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.legacy · 676f 子组 legacy：Δ +36.2pp，BH-FDR p=5.6e-05，Bonferroni p=0.00017** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+36.2pp` × 0 @ L
  - ✓ `+36.2` × 1 @ L1729
  - ✓ `5.6\times10^{-5}` × 1 @ L1729
  - ✓ `1.7\times10^{-4}` × 2 @ L1729,1730
  - ✓ `47` × 1 @ L1729
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.stl · 676f 子组 stl：Δ +15.0pp，BH-FDR p=0.00017，Bonferroni p=0.00067** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+15.0pp` × 0 @ L
  - ✓ `+15.0` × 1 @ L1730
  - ✓ `1.7\times10^{-4}` × 2 @ L1729,1730
  - ✓ `6.7\times10^{-4}` × 1 @ L1730
  - ✓ `100` × 22 @ L566,795,797,1297,1299,1309,1459,1606
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.real_world · 676f 子组 real_world：Δ +29.5pp，BH-FDR p=0.00054，Bonferroni p=0.0027** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+29.5pp` × 0 @ L
  - ✓ `+29.5` × 1 @ L1731
  - ✓ `5.4\times10^{-4}` × 1 @ L1731
  - ✓ `0.003` × 1 @ L2123
  - ✓ `44` × 5 @ L681,1296,1731,1768,1832
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.optimization_sensitive · 676f 子组 optimization_sensitive：Δ +55.0pp，BH-FDR p=0.0018，Bonferroni p=0.011** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+55.0pp` × 0 @ L
  - ✓ `+55.0` × 1 @ L1732
  - ✗ `0.002` × 0 @ L
  - ✗ `0.011` × 0 @ L
  - ✓ `20` × 19 @ L228,230,308,343,473,709,825,921
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.conditional_trigger · 676f 子组 conditional_trigger：Δ +45.0pp，BH-FDR p=0.0061，Bonferroni p=0.043** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+45.0pp` × 0 @ L
  - ✓ `+45.0` × 1 @ L1733
  - ✗ `0.006` × 0 @ L
  - ✗ `0.043` × 0 @ L
  - ✓ `20` × 19 @ L228,230,308,343,473,709,825,921
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.concurrency · 676f 子组 concurrency：Δ +7.3pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+7.3pp` × 1 @ L1743
  - ✓ `+7.3` × 2 @ L1734,1743
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `109` × 2 @ L1734,1742
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.language_semantics · 676f 子组 language_semantics：Δ +17.8pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+17.8pp` × 0 @ L
  - ✓ `+17.8` × 1 @ L1735
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `45` × 6 @ L798,1709,1733,1735,2131,2137
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.embedded · 676f 子组 embedded：Δ +8.1pp，BH-FDR p=0.034，Bonferroni p=0.34** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+8.1pp` × 0 @ L
  - ✓ `+8.1` × 2 @ L1714,1736
  - ✗ `0.034` × 0 @ L
  - ✗ `0.344` × 0 @ L
  - ✓ `74` × 15 @ L776,797,860,1589,1607,1736,1745,1769
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.odr_link · 676f 子组 odr_link：Δ +6.7pp，BH-FDR p=1，Bonferroni p=1** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+6.7pp` × 1 @ L1741
  - ✓ `+6.7` × 2 @ L1737,1741
  - ✗ `1.000` × 0 @ L
  - ✗ `1.000` × 0 @ L
  - ✓ `15` × 17 @ L681,922,1104,1152,1299,1542,1636,1730
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F09x · 676f 子组检验族大小 11** — consistent/active `✓`
- 源：`data/a5_676f_results.json`
  - ✓ `11` × 32 @ L16,108,345,443,505,531,795,797
**F10x.planted_false · 676f 真实缺陷 planted=false: FD 64.7% (22/34)，Δ +29.4pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `64.7` × 1 @ L1747
  - ✗ `22/34` × 0 @ L
  - ✓ `+29.4pp` × 1 @ L1748
  - ✗ `14.1, 44.7` × 0 @ L
  - ✓ `2.0\times10^{-3}` × 1 @ L1748
  - ✓ `35.3` × 2 @ L1709,1747
**F10x.planted_true · 676f planted=true: FD 53.9% (287/532)，Δ +23.7pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `53.9` × 1 @ L1749
  - ✗ `287/532` × 0 @ L
  - ✓ `+23.7pp` × 1 @ L1749
  - ✗ `20.1, 27.3` × 0 @ L
  - ✓ `2.4\times10^{-38}` × 1 @ L1749
  - ✓ `30.3` × 1 @ L1749
**F11x · 676f 资产诊断：8 资产各自 catch 率；wunsequenced/compile-time 100% unknown（退化）** — consistent/active `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `35.1` × 1 @ L1633
  - ✓ `399` × 1 @ L1633
  - ✓ `0.88` × 6 @ L14,1032,1633,1634,1635,1638
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
  - ✓ `0` × 251 @ L14,18,116,169,223,224,225,227
  - ✓ `100` × 22 @ L566,795,797,1297,1299,1309,1459,1606
  - ✓ `12.6` × 1 @ L1637
  - ✓ `143` × 1 @ L1637
  - ✓ `15.0` × 2 @ L1636,1730
  - ✓ `170` × 3 @ L1091,1636,1878
  - ✓ `3.34` × 1 @ L1636
  - ✓ `0.9` × 1 @ L1825
  - ✓ `10` × 38 @ L31,32,113,379,447,504,505,595
  - ✓ `22.4` × 1 @ L1635
  - ✓ `255` × 2 @ L1635,2041
  - ✓ `0.88` × 6 @ L14,1032,1633,1634,1635,1638
  - ✓ `23.6` × 1 @ L1634
  - ✓ `268` × 1 @ L1634
  - ✓ `0.88` × 6 @ L14,1032,1633,1634,1635,1638
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
  - ✓ `0` × 251 @ L14,18,116,169,223,224,225,227
  - ✓ `100` × 22 @ L566,795,797,1297,1299,1309,1459,1606
  - 注：退化资产是 A5 主/并列分析差异的唯一来源
**G01x · 676g 总盘：n=1147，catch 707，miss 440，盲区比 38.4%** — consistent/active `✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `1147` × 14 @ L106,155,217,372,381,460,866,1764
  - ✓ `707` × 3 @ L1764,1821,2302
  - ✓ `440` × 3 @ L460,1764,1821
  - ✓ `38.4` × 11 @ L109,217,318,329,460,640,866,1765
**G02x · 676g 互补性：6 资产并集 61.6%，最佳单资产 35.6%** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `61.6` × 3 @ L318,1822,1873
  - ✓ `707` × 3 @ L1764,1821,2302
  - ✓ `35.6` × 2 @ L1822,1824
**G03x · 676g 逐资产覆盖率（asan/ubsan/tsan/compiler-warn/cross-compile/linker）** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `35.6` × 2 @ L1822,1824
  - ✓ `23.5` × 1 @ L1824
  - ✓ `22.9` × 1 @ L1824
  - ✓ `12.5` × 3 @ L796,1557,1824
  - ✓ `10.6` × 2 @ L1714,1825
  - ✓ `0.9` × 1 @ L1825
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
  - ✓ `0.0` × 24 @ L344,433,453,532,709,797,870,873
**G04x · 676g 按 planted：true 41.0% [38.0, 44.1]；false 21.6% [13.8, 32.3]** — consistent/active `✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `41.0` × 2 @ L1768,1832
  - ✓ `38.0, 44.1` × 2 @ L1768,1832
  - ✓ `21.6` × 4 @ L518,1252,1769,1832
  - ✓ `13.8, 32.3` × 2 @ L1769,1832
  - ✓ `74` × 15 @ L776,797,860,1589,1607,1736,1745,1769
**G05x · 676g 盲区分带：18 个类型 >50% 盲；类型总数 70** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `18` × 12 @ L37,167,168,401,471,629,690,1175
  - ✓ `70` × 3 @ L37,1449,2054
  - ✓ `50` × 20 @ L329,462,671,681,690,866,905,1309
**G06x · 676g TSan 稳定性：3/180 不稳定（1.7%）** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `3` × 78 @ L17,25,27,110,158,209,314,404
  - ✓ `180` × 3 @ L1635,1778,1836
  - ✓ `1.7` × 7 @ L791,838,1714,1729,1730,1779,1837
**E01 · clang-analyzer holdout 48.8% (20/41) p=1.2e-4** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `48.8` × 3 @ L1713,1777,1907
  - ✗ `20/41` × 0 @ L
  - ✓ `1.2\times10^{-4}` × 1 @ L1907
**E02 · cppcheck holdout 41.5% (17/41) p=1.5e-5** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `41.5` × 4 @ L109,470,1908,2116
  - ✗ `17/41` × 0 @ L
  - ✓ `1.5\times10^{-5}` × 1 @ L1908
**E03 · cppcheck corpus 54.7% (35/64) p=0.38331031799316406** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `54.7` × 1 @ L1908
  - ✗ `35/64` × 0 @ L
  - ✓ `0.383` × 1 @ L1908
**E03b · cppcheck corpus Δ +7.8pp CI[-6.1, 21.7]（CI 跨 0 ⇒ tie）** — consistent/active `✓✓✗`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+7.8pp` × 1 @ L1913
  - ✓ `-6.1, 21.7` × 1 @ L1913
  - ✗ `(13,8)` × 0 @ L
**E04 · E9 附录 StrictA 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1907,1908
  - ✓ `1/11` × 2 @ L1907,1908
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E05 · E9 附录 cppcheck 主口径 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1907,1908
  - ✓ `1/11` × 2 @ L1907,1908
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E06 · E9 附录：holdout Δ(FD−StrictA) +34.1pp [19.6, 48.7]，对子 (14,0)** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+34.1pp` × 1 @ L1912
  - ✓ `19.6, 48.7` × 1 @ L1912
  - ✓ `(14,0)` × 1 @ L1912
**E07 · E9 附录：corpus StrictA 34.4% (22/64)，Δ +28.1pp 对子 (23,5)，p=9.1e-4** — consistent/active `✓✗✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `34.4` × 1 @ L1907
  - ✗ `22/64` × 0 @ L
  - ✓ `+28.1pp` × 1 @ L1913
  - ✓ `(23,5)` × 1 @ L1913
  - ✓ `9.1\times10^{-4}` × 1 @ L1907
**E08 · E9 附录：corpus 分层 FD/ct/cp（sanitizer 29/17/26；compiler-warn 9/5/8；cross-compile 2/0/1）** — consistent/active `✗✗✓✓✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✗ `29 / 17 / 26` × 0 @ L
  - ✗ `9 / 5 / 8` × 0 @ L
  - ✓ `2 / 0 / 1` × 1 @ L1918
  - ✓ `12` × 22 @ L45,437,447,670,691,795,796,869
  - ✓ `FD 29 vs clang-analyzer 17 / cppcheck 26` × 1 @ L1917
  - ✓ `FD 9 / cppcheck 8` × 1 @ L1917
  - ✓ `2 / 0 / 1` × 1 @ L1918
**E10 · E9 附录：clang-tidy 主口径 holdout 100% recall / 100% FPR（零区分度 ⇒ 该口径被弃用）** — consistent/active `✗✓✗✓✗✗`
- 源：`data/673e_comparison_stats.json`
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 22 @ L566,795,797,1297,1299,1309,1459,1606
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 22 @ L566,795,797,1297,1299,1309,1459,1606
  - ✗ `41/41` × 0 @ L
  - ✗ `11/11` × 0 @ L
**E09 · E9 附录：8 个反向对（工具 catch / FD miss）** — consistent/active `✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `8` × 54 @ L16,155,373,443,671,727,795,842
**F01 · 外部锚点子集 A（准则原文）28.6% (10/35) CI[14.6,46.3]** — consistent/active `✓✗✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `28.6` × 3 @ L680,799,864
  - ✗ `10/35` × 0 @ L
  - ✗ `14.6, 46.3` × 0 @ L
**F02 · 外部锚点子集 B（UB 片段重建）80.0% (12/15)** — consistent/active `✓✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `80.0` × 2 @ L681,940
  - ✗ `12/15` × 0 @ L
**F03 · 外部锚点合计 44.0% (22/50)；扫描规则 87** — consistent/active `✓✗✓✓✓✓✓✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `44.0` × 1 @ L681
  - ✗ `22/50` × 0 @ L
  - ✓ `22` × 12 @ L472,1149,1150,1175,1635,1710,1824,1895
  - ✓ `50` × 20 @ L329,462,671,681,690,866,905,1309
  - ✓ `87` × 6 @ L679,767,943,944,1122,1590
  - ✓ `35` × 23 @ L373,480,513,613,642,680,767,1123
  - ✓ `15` × 17 @ L681,922,1104,1152,1299,1542,1636,1730
  - ✗ `11/60` × 0 @ L
**F04 · LLM 臂：GLM-4 12/12 vs FD 6/12；对照误报 4/8 = 50%** — consistent/active `✓✓✓✓✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✓ `12/12` × 2 @ L670,1575
  - ✓ `6/12` × 1 @ L670
  - ✓ `4/8` × 2 @ L671,1575
  - ✓ `50.0` × 2 @ L690,1830
  - ✓ `50.0` × 2 @ L690,1830
  - 注：FD 的 6/12 由 fd_detect_rate_pct=50.0% × llm_n 重算得到
**F05 · LLM 臂配对 b/c = (0,6)，p=0.03125** — consistent/active `✗✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✗ `0,6` × 0 @ L
  - ✓ `0.031` × 1 @ L672
**G01 · 变异（core）110/114 = 96.5%** — consistent/active `✓✓✗`
- 源：`data/656_mutation_report.json`
  - ✓ `110/114` × 2 @ L929,944
  - ✓ `96.5` × 3 @ L872,944,1124
  - ✗ `91.3, 99.0` × 0 @ L
**G02 · 变异（all-scope）130/159 = 81.8%** — consistent/active `✓✓`
- 源：`data/656_mutation_report_all.json`
  - ✓ `130/159` × 1 @ L929
  - ✓ `81.8` × 1 @ L1124
**G03 · 缺陷重注入 6/6 = 100%；total 15；软覆盖 12/15** — consistent/active `✓✗✓`
- 源：`data/defect_injection_661.json`
  - ✓ `6/6` × 2 @ L795,797
  - ✗ `12/15` × 0 @ L
  - ✓ `15` × 17 @ L681,922,1104,1152,1299,1542,1636,1730
**H01 · 样本量：独立两比例 0.35→0.50 ⇒ n=170** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=None, α=0.05, power=0.8, recomputed=169.09`
  - ✓ `170` × 3 @ L1091,1636,1878
  - ✗ `170 (holdout)` × 0 @ L
**H02 · 样本量：独立两比例 0.35→0.55 ⇒ n=96** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.55,psi=None, α=0.05, power=0.8, recomputed=95.77`
  - ✓ `96` × 5 @ L872,944,1092,1124,1877
  - ✗ `96 (holdout)` × 0 @ L
**H03 · 样本量：独立两比例 0.35→0.45 ⇒ n=376** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.45,psi=None, α=0.05, power=0.8, recomputed=375.27`
  - ✓ `376` × 1 @ L1093
  - ✗ `376 (holdout)` × 0 @ L
**H04 · 样本量：配对 ψ=0.3 ⇒ n=103** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.3, α=0.05, power=0.8, recomputed=102.26`
  - ✓ `103` × 3 @ L1094,1601,1614
  - ✗ `103 (holdout)` × 0 @ L
**H05 · 样本量：配对 ψ=0.4 ⇒ n=138** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.4, α=0.05, power=0.8, recomputed=137.15`
  - ✓ `138` × 1 @ L1095
  - ✗ `138 (holdout)` × 0 @ L
**H06 · 样本量：配对 ψ=0.5 ⇒ n=173** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.5, α=0.05, power=0.8, recomputed=172.04`
  - ✓ `173` × 6 @ L922,1096,1652,1753,1782,2081
  - ✗ `173 (holdout)` × 0 @ L
**K01 · tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现** — consistent/unpinned_no_artifact `✓✓`
- 源：`data/656_mutation_report*.json 现存值为 110/114 与 130/159；全仓扫描 `30/48` 无产物命中（唯一产出是更早被覆盖的报告）`
  - ✓ `62.5` × 8 @ L776,797,860,928,939,1127,1528,1906
  - ✓ `30/48` × 2 @ L928,939
  - 注：论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注）
**K02 · tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径** — consistent/unpinned_retired_caliber `✓`
- 源：`仅能追溯到 research/paper_v0.4.md 与 data/669_caliber_report.json::doc_sightings；对应 -O1 单档产物已被 665/668 双档口径取代`
  - ✓ `66.7` × 3 @ L301,930,941
  - 注：该值口径已退休，只能作为“当时口径下读到的数”引用
**I01 · Static holdout 1/41 CI ⇒ [0.1, 12.9]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(1,41)])"`
  - ✓ `0.1, 12.9` × 1 @ L795
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I02 · Random† holdout 4/41 CI ⇒ [2.7, 23.1]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(4,41)])"`
  - ✓ `2.7, 23.1` × 1 @ L796
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I03 · FD holdout 34/41 CI ⇒ [67.9, 92.8]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,41)])"`
  - ✓ `67.9, 92.8` × 4 @ L776,797,860,946
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I04 · Caliber B holdout 34/42 CI ⇒ [65.9, 91.4]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,42)])"`
  - ✓ `65.9, 91.4` × 2 @ L777,778
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I05 · Static corpus 11/64 CI ⇒ [8.9, 28.7]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(11,64)])"`
  - ✓ `8.9, 28.7` × 1 @ L795
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I06 · Random† corpus 14/64 CI ⇒ [12.5, 34.0]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(14,64)])"`
  - ✓ `12.5, 34.0` × 1 @ L796
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I07 · FD corpus 40/64 CI ⇒ [49.5, 74.3]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,64)])"`
  - ✓ `49.5, 74.3` × 3 @ L776,797,860
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I08 · Caliber B corpus 40/73 CI ⇒ [42.7, 66.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,73)])"`
  - ✓ `42.7, 66.5` × 1 @ L777
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I09 · Caliber C corpus 40/76 CI ⇒ [40.8, 64.2]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,76)])"`
  - ✓ `40.8, 64.2` × 1 @ L778
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I10 · 对照 FPR 0/11 CI ⇒ [0.0, 28.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(0,11)])"`
  - ✓ `0.0, 28.5` × 1 @ L797
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
  - ✓ `105` × 1 @ L1518
  - ✗ `840` × 0 @ L
  - ✓ `8` × 54 @ L16,155,373,443,671,727,795,842
**A19 · ±5pp 缺口：holdout 还差 195，corpus 还差 314** — consistent/active `✓✓`
- 源：`sample_size_672k.±5pp.n − 当前可测 n`
  - ✓ `195` × 1 @ L1103
  - ✓ `314` × 1 @ L1103
**D11 · clone-aware 重切分 Δ +23.0~+26.7pp（677b，逐 split 为 +23.02/+25.70）** — consistent/active `✓✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_a5_results_family_random.json / _family_stratified.json`
  - ✓ `23.02` × 2 @ L1674,2028
  - ✓ `25.70` × 2 @ L1674,2029
**D12 · cluster bootstrap 有效 n≈133–140（677b，design effect ≈4.1–4.3）** — consistent/active `✗✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_cluster_bootstrap.json`
  - ✗ `133` × 0 @ L
  - ✓ `140` × 12 @ L322,345,447,622,865,870,1389,1653
**D13 · 非退化池选择效应 +11.31pp（677c，k=1，p=6.02e-08）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `11.31` × 5 @ L16,443,870,1667,1685
**D14 · 退化资产对均值的贡献 ≈+12.81pp（677c）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `12.81` × 1 @ L1687
**Z01 · 689 TOST：±10pp 未过，90% CI [-10.61, 5.52]pp，p_TOST=0.064** — consistent/active `✓✓✓`
- 源：`current_numbers.reframed_689.equivalence_tost ← data/689_equivalence_test.json`
  - ✓ `-10.61` × 5 @ L32,113,504,2119,2305
  - ✓ `5.52` × 5 @ L32,113,504,2119,2305
  - ✓ `0.064` × 3 @ L504,2305,2306
**E02 · 689 TOST 最小通过 margin 10.61pp（deff 校正 11.67pp）** — consistent/active `✓✓`
- 源：`data/689_equivalence_test.json`
  - ✓ `10.61` × 9 @ L32,113,504,505,2119,2120,2305,2306
  - ✓ `11.67` × 2 @ L505,2308
**E03 · 689 标准化：正向 -17.92pp（R_syn_std=77.01%），反向 +1.70pp，类型级 -13.52pp** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.standardized_analysis ← data/689_standardized_analysis.json`
  - ✓ `-17.92` × 5 @ L33,508,520,2120,2318
  - ✓ `77.01` × 2 @ L508,2317
  - ✓ `1.70` × 2 @ L509,2320
  - ✓ `-13.52` × 2 @ L516,2321
**E04 · 689 环境：真实 59.09%→23.64%（-35.45pp，Δunknown=0），clang↔g++ 93.5%** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.environment_metrics ← data/689_environment_metrics.json`
  - ✓ `59.09` × 12 @ L111,314,471,478,502,506,875,2111
  - ✓ `23.64` × 4 @ L111,480,2332
  - ✓ `35.45` × 4 @ L480,613,1401,1410
  - ✓ `93.5` × 4 @ L483,631,2179,2336
**Z11 · 691 机制级：Pool A k=1 +11.31pp (p=6.0e-8)；k=2/k=3 +7.42pp；k=4 0.00pp** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_691.mechanism_level_poolA_vs_single_random ← data/677c_a5_nondegenerate_results.json`
  - ✓ `11.31` × 5 @ L16,443,870,1667,1685
  - ✓ `6.0` × 4 @ L16,443,870,1685
  - ✓ `7.42` × 6 @ L16,17,443,1667,1685
  - ✓ `0.00` × 7 @ L444,1686,1861,1863,1864,1865,1875
**Z12 · 691 四个 κ（AI 自一致）：0.727 / 0.789 / 0.437 / 0.157** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_691.label_kappa_ai_self_consistency ← data/682_kappa.json`
  - ✓ `0.727` × 1 @ L589
  - ✓ `0.789` × 1 @ L589
  - ✓ `0.437` × 2 @ L18,590
  - ✓ `0.157` × 3 @ L18,466,590
**Z13 · 691 治理计数：452 ledger 事件 / 67 规则 / rules_sha256 v1.0.0** — consistent/active `✓✓`
- 源：`current_numbers.reframed_691.governance`
  - ✓ `452` × 8 @ L19,263,270,811,862,901,1134,1333
  - ✓ `67` × 13 @ L19,264,776,797,811,860,946,953
**Z14 · 691 池计数：Pool B ≡ Pool C（同一六资产集）；9 个不同 (池,k) 块 / 14 块实例** — consistent/active `✓✓✓`
- 源：`current_numbers.reframed_691.pools ← data/677c_asset_pools.json + 677c_evolution_operator_results.json`
  - ✓ `2` × 83 @ L16,18,108,154,218,226,228,230
  - ✓ `9` × 37 @ L15,300,318,513,516,527,605,660
  - ✓ `14` × 15 @ L527,531,796,873,943,1034,1709,1912
