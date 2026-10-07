# 676h · 论文数字可追溯性审计报告

- 生成时间：2026-10-07T22:14:54+08:00
- 被审计稿件：`research/latex/queyi_neurips2027_v1.1.tex`（正文 None 页 / 全稿 37 页，取自编译日志）
- 权威源：14 个文件
- 检察条数：**126**，其中 consistent 112，硬 missing（active）0，软 missing（not_printed 等）0，skipped/no_source 0

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

扫描到数字 token **1735** 个（已排除注释行与导言区行）。分类：

| 类别 | 数量 | 占比 |
|---|---|---|
| claim | 1269 | 73.1% |
| unclassified | 158 | 9.1% |
| design_constant | 73 | 4.2% |
| batch_id | 59 | 3.4% |
| method_constant | 49 | 2.8% |
| format_layout | 30 | 1.7% |
| repro_command | 24 | 1.4% |
| system_constant | 12 | 0.7% |
| engineering_narrative | 12 | 0.7% |
| year | 11 | 0.6% |
| logic_constant | 10 | 0.6% |
| external_literature | 8 | 0.5% |
| structural | 6 | 0.3% |
| historical_retired | 5 | 0.3% |
| sample_id | 4 | 0.2% |
| cited_context | 2 | 0.1% |
| erratum_retired | 2 | 0.1% |
| external_regulation | 1 | 0.1% |

未归类 token：158 个（前 60 条见下；全量在 json 里）。

| 行 | token | 上下文 |
|---|---|---|
| 135 | `2` | `(2)~\textbf{A systematic empirical audit} of a software-verification apparatus` |
| 196 | `2` | `invisible to the eight-asset instrument (Finding~2).` |
| 271 | `40` | `\emph{same} 40 catches; a flag change once moved holdout recall $66.7\%\to87.5\%$ with the` |
| 336 | `34` | `across 34 normalized types (8 families), including 64 corpus-null controls and 35 hung` |
| 337 | `110` | `samples. \emph{Source-derived real-defect corpus} (110 samples): minimal reconstructions of` |
| 338 | `30` | `defects from 30+ real projects (CVE/NVD-verified mechanisms, responses frozen; \emph{not}` |
| 362 | `13.3` | `Four profiles are declared: \texttt{wsl-gcc-13.3} (asan/ubsan/tsan, primary),` |
| 364 | `200` | `\texttt{wsl-clang-18.1.3} (200-sample stratified replication), and MSVC/clang-cl (absent on` |
| 392 | `24` | `\paragraph{F1. A $+24$pp ``selection gain'' is mostly measurement-pool composition` |
| 409 | `13` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 409 | `34` | `\textbf{13 of 34} normalized types exceed $50\%$ blindness. Blindness is organized by defect` |
| 411 | `60` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 411 | `62` | `link/ODR $\approx67.7\%$, while CRITICAL/HIGH/MEDIUM real defects all detect at $60$--$62\%$;` |
| 412 | `86.96` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 412 | `30.77` | `parsing/multimedia real defects detect at $86.96\%$, OS/kernel at $30.77\%$, web-server` |
| 415 | `52.2` | `harder on real defects than on synthetic ones (type punning $-52.2$pp, logic $-22.5$pp,` |
| 420 | `65` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 420 | `110` | `Under the declared WSL profile, the real corpus detects at 59.09\% ($65/110$); under the` |
| 422 | `39` | `\textbf{23.64\%} ($-35.45$pp) with \emph{no} unknown increase: 39 catches depend on Linux` |
| 451 | `14` | `to frequency-only and set-cover greedy in \textbf{14/14} pool$\times k$ blocks (in literal` |
| 451 | `14` | `to frequency-only and set-cover greedy in \textbf{14/14} pool$\times k$ blocks (in literal` |
| 453 | `14` | `selection in 11/14 blocks but adds no recall); on the real corpus, $k{=}1..7$ deltas are all` |
| 456 | `17496` | `simple optimal selection already exists (all 17496 triples checked; greedy attains ratio` |
| 457 | `2.29` | `$1.0$; adaptive ceiling only $+2.29$pp)---\textbf{the apparent need for sophisticated` |
| 491 | `19` | `We report five threat classes with direction and mitigation status (the 19-item table and` |
| 502 | `6.6` | `$6.6\%\to14.3\%$ under $\le15\%$ flips, though contrast directions are stable).` |
| 507 | `110` | `The 110-sample source-derived corpus improves ecological validity but is` |
| 533 | `5` | `rate by $-16.36$pp. Cross-run stability: 5\% grid flips; the shadow-mapped` |
| 542 | `24` | `detecting that collapse. On a software-verification apparatus: a $+24$pp selection gain was` |
| 546 | `17.9` | `explained by a $-17.9$pp composition offset; and failure-driven evolution produced no` |
| 842 | `30` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 842 | `17` | `665 & expand 20$\to$30 & true 17, \textbf{66.7\%} (single flag) & --- & denominator changed \\` |
| 855 | `5` | `/ advice 7} (total 67). By kind: fact 61 / pedagogy 5 / meta 1. Fields:` |
| 1082 | `2` | `runtime); the script re-derives them \emph{from landed artifacts} instead. (2) E9's driver script is` |
| 1323 | `200` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `219` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `149` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `95` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `99` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `90` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1323 | `88` | `stl 200, concurrency 219, embedded 149, legacy 95, memory 99, UB 87, language 90, real-world 88,` |
| 1348 | `93` | `676m unification, which is exactly why the vocabulary was unified. (iii) $93\%$ of samples are` |
| 1353 | `34` | `Two data-quality defects were repaired and are visible in this appendix's numbers: $34$` |
| 1355 | `56` | `(a hung sanitizer emits no report), and the $56$-value \texttt{defect\_type} vocabulary was` |
| 1356 | `34` | `consolidated to $34$ canonical types (with \texttt{conditional\_trigger} /` |
| 1415 | `5` | `Three pools are pre-registered on the same matrix: \textbf{A} (strict; 5 assets), \textbf{B}` |
| 1441 | `2` | `2 & 45.1\% & 14.3\% & +30.7 & [+26.2, +35.3] & $7.8\times10^{-35}$ \\` |
| 1442 | `24.5` | `3 & 51.1\% & 30.6\% & +20.5 & [+16.5, +24.5] & $2.2\times10^{-22}$ \\` |
| 1442 | `2.2` | `3 & 51.1\% & 30.6\% & +20.5 & [+16.5, +24.5] & $2.2\times10^{-22}$ \\` |
| 1443 | `27.5` | `\textbf{4} & \textbf{54.6\%} & \textbf{30.6\%} & \textbf{+24.0} & [+20.5, +27.5] & $2.3\times10^{-41}$ \\` |
| 1444 | `5` | `5 & 59.4\% & 38.7\% & +20.7 & [+17.3, +24.0] & $1.2\times10^{-35}$ \\` |
| 1444 | `17.3` | `5 & 59.4\% & 38.7\% & +20.7 & [+17.3, +24.0] & $1.2\times10^{-35}$ \\` |
| 1463 | `2.7` | `real world & 44 & +29.5 & $5.4\times10^{-4}$ & $2.7\times10^{-3}$ \\` |
| 1464 | `2` | `optimization sensitive & 20 & +55.0 & $1.8\times10^{-3}$ & $1.1\times10^{-2}$ \\` |
| 1465 | `6.1` | `conditional trigger & 20 & +45.0 & $6.1\times10^{-3}$ & $4.3\times10^{-2}$ \\` |
| 1465 | `2` | `conditional trigger & 20 & +45.0 & $6.1\times10^{-3}$ & $4.3\times10^{-2}$ \\` |
| 1466 | `2` | `concurrency & 109 & +7.3 & $9.6\times10^{-3}$ & $8.6\times10^{-2}$ \\` |
| 1467 | `2` | `language semantics & 45 & +17.8 & $9.6\times10^{-3}$ & $8.6\times10^{-2}$ \\` |
| 1468 | `2` | `embedded & 74 & +8.1 & $3.4\times10^{-2}$ & $3.4\times10^{-1}$ \\` |
| 1479 | `34` | `production code}; 34 evaluated) FD reads \textbf{64.7\%} vs.\ Random 35.3\%,` |

## 5. 每条检察的命中明细

**A01 · holdout 可测检出率 82.9% (34/41) CI[67.9,92.8]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `82.9` × 9 @ L674,695,761,847,1026,1509,1572,1638
  - ✓ `34/41` × 5 @ L674,695,761,847,1026
  - ✓ `67.9, 92.8` × 4 @ L674,695,761,847
**A02 · corpus 可测检出率 62.5% (40/64) CI[49.5,74.3]** — consistent/active `✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `62.5` × 8 @ L674,695,761,829,840,1026,1207,1638
  - ✓ `40/64` × 4 @ L674,695,761,1026
  - ✓ `49.5, 74.3` × 3 @ L674,695,761
**A03 · corpus 全样本口径 52.6%** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `52.6` × 2 @ L676,1207
**A04 · Static 臂 holdout 2.4% (1/41) / corpus 17.2% (11/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `2.4` × 3 @ L689,693,1481
  - ✓ `1/41` × 1 @ L693
  - ✓ `17.2` × 1 @ L693
  - ✓ `11/64` × 1 @ L693
**A05 · Random† 臂 holdout 9.8% (4/41) / corpus 21.9% (14/64)** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `9.8` × 1 @ L694
  - ✓ `4/41` × 1 @ L694
  - ✓ `21.9` × 1 @ L694
  - ✓ `14/64` × 1 @ L694
**A06 · Δ(Static→FD) holdout +80.5pp CI[68.4,92.6] p=2.3e-10 h=1.98** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+80.5pp` × 1 @ L696
  - ✓ `68.4, 92.6` × 1 @ L696
  - ✓ `2.3\times10^{-10}` × 1 @ L622
  - ✓ `1.98` × 1 @ L622
**A07 · Δ(Random†→FD) holdout +73.2pp CI[59.6,86.7] p=1.9e-9 h=1.65** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+73.2pp` × 1 @ L697
  - ✓ `59.6, 86.7` × 1 @ L697
  - ✓ `1.9\times10^{-9}` × 1 @ L624
  - ✓ `1.65` × 1 @ L624
**A08 · Δ(Static→FD) corpus +45.3pp CI[33.1,57.5] p=3.7e-9 h=0.97** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+45.3pp` × 1 @ L696
  - ✓ `33.1, 57.5` × 1 @ L696
  - ✓ `3.7\times10^{-9}` × 1 @ L623
  - ✓ `0.97` × 3 @ L623,976,2002
**A09 · Δ(Random†→FD) corpus +40.6pp CI[28.6,52.7] p=3.0e-8 h=0.85** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `+40.6pp` × 1 @ L697
  - ✓ `28.6, 52.7` × 1 @ L697
  - ✓ `3.0\times10^{-8}` × 1 @ L625
  - ✓ `0.85` × 1 @ L625
**A10 · 配对不一致对 (b, c)（tab:e5 四行）** — consistent/active `✓✓✓✓`
- 源：`data/current_numbers.json`
  - ✓ `(33, 0)` × 1 @ L622
  - ✓ `(29, 0)` × 1 @ L623
  - ✓ `(30, 0)` × 1 @ L624
  - ✓ `(26, 0)` × 1 @ L625
  - 注：四个对比都是 c=0 结构（对手的 catch 是 FD catch 的子集）
**A11 · 对照假阳性 0.0% (0/11)** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `0.0\% (0/11)` × 4 @ L695,823,1638,1688
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
**A12 · 缺陷重注入 6/6 = 100%** — consistent/active `✓✗`
- 源：`data/current_numbers.json`
  - ✓ `6/6` × 2 @ L693,695
  - ✗ `100.0` × 0 @ L
**A13 · CP95 半宽 12.5pp（holdout）** — consistent/active `✓`
- 源：`data/current_numbers.json`
  - ✓ `12.5` × 3 @ L694,1266,1556
**A14 · 扩样前 holdout 81.0% (17/21) CI[58.1,94.6]** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `81.0` × 3 @ L675,676,846
  - ✓ `17/21` × 1 @ L846
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
  - ✓ `236` × 4 @ L770,823,998,1002
  - ✓ `378` × 4 @ L770,823,998,1002
**A18 · ±10pp 半宽所需样本量 holdout 61 / corpus 97** — consistent/active `✓✓`
- 源：`data/current_numbers.json`
  - ✓ `61` × 13 @ L288,434,767,823,845,855,997,1554
  - ✓ `97` × 5 @ L823,997,1391,1767,2018
**B01 · holdout 累计 catch/miss/unknown = 34/7/1，分母 41** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/41` × 5 @ L674,695,761,847,1026
  - ✓ `1` × 145 @ L20,53,88,131,200,201,202,203
**B02 · holdout 口径 B（unknown→miss）34/42 = 81.0%** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `34/42` × 2 @ L675,676
  - ✓ `81.0` × 3 @ L675,676,846
**B03 · holdout 分层 sanitizer 84.6% (33/39)** — consistent/active `✓✓`
- 源：`data/holdout_reveal_5_672h.json`
  - ✓ `84.6` × 1 @ L590
  - ✓ `33/39` × 1 @ L590
**B04 · corpus 分层 sanitizer 85.3% (29/34) / compiler-warn 50.0% (9/18) / cross-compile 16.7% (2/12)** — consistent/active `✓✓✓✓✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `85.3` × 1 @ L588
  - ✓ `29/34` × 1 @ L588
  - ✓ `50.0` × 2 @ L588,1562
  - ✓ `9/18` × 1 @ L588
  - ✓ `16.7` × 3 @ L588,1266,1682
  - ✓ `2/12` × 1 @ L589
**B05 · corpus 口径 B（unknown→miss）40/73 = 54.8%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/73` × 1 @ L675
  - ✓ `54.8` × 1 @ L675
**B06 · corpus 口径 C（全样本）40/76 = 52.6%** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `40/76` × 1 @ L676
  - ✓ `52.6` × 2 @ L676,1207
**B07 · corpus 分层 Excluded unknown=9 / not_error=3** — consistent/active `✓✓`
- 源：`data/external_corpus_reveal_672h.json`
  - ✓ `9` × 28 @ L270,288,508,558,588,623,624,678
  - ✓ `3` × 67 @ L8,10,91,139,187,284,367,454
**B08 · holdout 新子集 17/20 = 85.0%（round5）** — retired/superseded:689重构 `✗✗`
- 源：`data/holdout_reveal_5_672h.json`
  - ✗ `17/20` × 0 @ L
  - ✗ `85.0` × 0 @ L
  - 注：689 重构：round5 子集数字随旧正文段落移出正文（数据仍在产物）
**B09 · 历史批次 669：87.5%（14/16）与 CI[61.7, 98.4]** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `87.5` × 4 @ L665,844,845,1021
**B10 · 历史批次 660：80.0%（batch compare before）** — consistent/active `✓`
- 源：`data/holdout_reveal_3_665.json`
  - ✓ `80.0` × 2 @ L579,841
**C01 · 判决规则数 67（len(gate_engine.RULES)）** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES))"`
  - ✓ `67` × 16 @ L674,695,709,761,847,852,854,855
**C02 · 权威账本事件数 452（decision_event_v2_ledger.jsonl 非空行）** — consistent/active `✓`
- 源：`python -c "n=sum(1 for l in open(r'data/authority/decision_event_v2_ledger.jsonl',encoding='utf-8') if l.strip());print(n)"`
  - ✓ `452` × 4 @ L709,763,802,1033
**C03 · 实卡数 atoms_real = 42（counts_659.py 现算）** — consistent/active `✓`
- 源：`python tools/counts_659.py --json`
  - ✓ `42` × 6 @ L675,676,1030,1945,1946
**C04 · Verifier Coverage = 31/42 = 73.8%** — consistent/active `✗✓`
- 源：`atoms/**/ATOM-*.md 排除 draft650/；status∈{verified,red-team-verified,machine-verified}`
  - ✗ `31/42` × 0 @ L
  - ✓ `73.8` × 2 @ L19,1029
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
**C07 · 规则严重度分解 block 44 / warn 16 / advice 7** — consistent/active `✓✓✓✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine;from collections import Counter;c=Counter(getattr(r,'severity',None) for r in gate_engine.RULES);print(c.get('block',0),c.get('warn',0),c.get('advice',0))"`
  - ✓ `44/16/7` × 1 @ L858
  - ✓ `44` × 6 @ L579,854,858,1463,1500,1564
  - ✓ `16` × 18 @ L533,588,666,844,854,858,1190,1257
  - ✓ `7` × 35 @ L27,89,278,315,399,757,771,841
  - 注：旧稿的 0/176/55 不可复现，已按现算值纠正
**C08 · 边界卡 26 张；provenance 完整 26/26；scope 完整 0/26** — consistent/active `✓✗✓`
- 源：`data/boundary_provenance_658.json`
  - ✓ `26` × 14 @ L625,769,797,822,1302,1309,1385,1407
  - ✗ `26/26` × 0 @ L
  - ✓ `0/26` × 6 @ L769,797,822,1302,1309,1827
  - 注：provenance 完整 = provenance 字典字段数 ≥3（mutationset/generator/evidence）
**N01 · 81.2% 必须在出现的每一处都被标为从未落盘/作废** — consistent/active `✓`
- 源：`673c/676h 诚实边界：81.2% 不得作为已落盘结果引用`
  - ✓ `81.2` × 1 @ L
  - 注：若 81.2 出现在没有 never-landed 标注的句子里 ⇒ 违反
**D01 · A5 holdout 主端点 FD 90.0% (18/20) vs Random 35.0%** — consistent/superseded_by_676f `✓✗✓✗✓✗✓✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `90.0` × 2 @ L1189,1595
  - ✗ `18/20` × 0 @ L
  - ✓ `35.0` × 5 @ L665,1022,1053,1189,1240
  - ✗ `7/20` × 0 @ L
  - ✓ `10.0` × 2 @ L1053,1240
  - ✗ `2/20` × 0 @ L
  - ✓ `+55.0pp` × 1 @ L1189
  - ✗ `33.2, 76.8` × 0 @ L
  - ✗ `9.8\times10^{-4}` × 0 @ L
  - ✗ `1.23` × 0 @ L
  - 注：673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹
**D01b · A5 holdout 2000 次随机分布：FD 严格优于的比例与均值/标准差** — consistent/superseded_by_676f `✗✗✓✗`
- 源：`data/experiments/a5_673p.json`
  - ✗ `93.75` × 0 @ L
  - ✗ `93.8` × 0 @ L
  - ✓ `55.0` × 2 @ L1189,1464
  - ✗ `23.4` × 0 @ L
**D01c · A5 设计量：holdout 派生 n=21 / 评估 n=20** — consistent/superseded_by_676f `✓✓✓✓✓✓`
- 源：`data/experiments/a5_673p.json`
  - ✓ `21` × 10 @ L694,822,846,847,1386,1501,1564,1646
  - ✓ `20` × 19 @ L206,208,278,313,416,607,724,822
  - ✓ `4` × 74 @ L8,93,259,280,291,314,396,398
  - ✓ `2000` × 8 @ L260,1391,1419,1609,1764,1768,1946,2018
  - ✓ `8` × 53 @ L136,336,569,625,693,743,765,767
  - ✓ `41` × 31 @ L90,313,350,413,607,622,624,674
**D02 · A5 corpus 主端点 FD 81.25% (13/16) vs Random 37.5%** — consistent/superseded_by_676f `✓✓✓✗✓✗✓✗✗✗`
- 源：`data/experiments/a5_673p.json`
  - ✓ `81.2` × 7 @ L843,1223,1255,1257,1310,1677,1824
  - ✓ `13/16` × 2 @ L1257,1677
  - ✓ `37.5` × 1 @ L1190
  - ✗ `6/16` × 0 @ L
  - ✓ `37.5` × 1 @ L1190
  - ✗ `6/16` × 0 @ L
  - ✓ `+43.8pp` × 1 @ L1190
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
  - ✓ `48` × 13 @ L822,829,840,847,1266,1445,1509,1639
  - ✓ `16` × 18 @ L533,588,666,844,854,858,1190,1257
  - ✓ `4` × 74 @ L8,93,259,280,291,314,396,398
  - ✓ `2000` × 8 @ L260,1391,1419,1609,1764,1768,1946,2018
  - ✓ `8` × 53 @ L136,336,569,625,693,743,765,767
  - ✓ `64` × 25 @ L336,350,442,623,625,674,676,693
**F01x · 676f 样本簿记：1137 总样本；派生 571；评估 566** — consistent/active `✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `1137` × 11 @ L343,1072,1192,1312,1318,1324,1403,1728
  - ✓ `571` × 1 @ L1319
  - ✓ `566` × 20 @ L259,313,349,358,395,607,766,771
  - ✓ `1063` × 1 @ L1322
  - ✓ `74` × 16 @ L674,695,761,1322,1340,1468,1477,1501
  - ✓ `10` × 37 @ L14,15,94,342,436,437,498,508
**F02x · 676f 主端点（k=4，全 8 资产池）FD/Random/Static 三臂** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `54.6` × 4 @ L394,1384,1396,1443
  - ✓ `309/566` × 1 @ L1384
  - ✓ `30.6` × 8 @ L394,607,766,771,1385,1398,1442,1443
  - ✓ `173/566` × 1 @ L1385
  - ✓ `24.7` × 1 @ L1386
  - ✓ `140/566` × 1 @ L1386
  - ✓ `60.1` × 5 @ L1387,1445,1446,1447
  - ✓ `340/566` × 1 @ L1387
**F03x · 676f 主端点 Δ(FD−Random) +24.0pp CI[+20.5, +27.5] p=2.3e-41 h=0.49 (b=136, c=0)** — consistent/active `✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `+24.0pp` × 9 @ L12,27,88,276,313,395,607,1385
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L313,607,1385,1443
  - ✓ `0.49` × 1 @ L1385
  - ✗ `(136,0)` × 0 @ L
**F04x · 676f 主端点 Δ(FD−Static) +29.9pp CI[+25.2, +34.5] p=1.9e-31** — consistent/active `✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+29.9pp` × 4 @ L607,766,1386,1807
  - ✗ `25.2, 34.5` × 0 @ L
  - ✓ `1.9\times10^{-31}` × 3 @ L607,766,1386
  - ✓ `0.62` × 1 @ L1386
**F05x · 676f 2000 次随机分布：FD 严格优于 97.6%（Random 均值 40.2%，SD 9.3pp）** — consistent/active `✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `97.6` × 2 @ L1391,2018
  - ✓ `40.2` × 1 @ L1392
  - ✓ `9.3` × 1 @ L1392
  - ✓ `2000` × 8 @ L260,1391,1419,1609,1764,1768,1946,2018
**F06x · 676f 并列分析（剔退化资产）：Δ(FD−Random)=0.0pp p=1.0；Δ(FD−Static)=+30.6pp CI[+26.0,+35.1] p=8.1e-34** — consistent/active `✓✓✓✗✓✓✗`
- 源：`data/a5_676f_results.json`
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
  - ✓ `1.0` × 19 @ L314,397,457,709,772,968,1024,1397
  - ✓ `+30.6pp` × 4 @ L607,766,771,1398
  - ✗ `26.0, 35.1` × 0 @ L
  - ✓ `8.1\times10^{-34}` × 1 @ L1398
  - ✓ `24.0` × 12 @ L12,27,88,276,313,395,607,1385
  - ✗ `136/566` × 0 @ L
**F07x · 676f k 扫描（k=1..8）各档 Δ 与 p** — consistent/active `✗✓✗✓✓✓✗✓✗✓✓✓✗✓✗✗✓✓✓✓✗✓✓✓✗✓✗✓✓✓✓✓✗✓✓✓✗✓✗✓✓✓✗✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+33.0pp` × 0 @ L
  - ✓ `+33.0` × 1 @ L1440
  - ✗ `29.2, 36.9` × 0 @ L
  - ✓ `1.0\times10^{-56}` × 1 @ L1440
  - ✓ `33.0` × 2 @ L1440
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
  - ✗ `+30.7pp` × 0 @ L
  - ✓ `+30.7` × 1 @ L1441
  - ✗ `26.2, 35.3` × 0 @ L
  - ✓ `7.8\times10^{-35}` × 1 @ L1441
  - ✓ `45.1` × 1 @ L1441
  - ✓ `14.3` × 1 @ L1441
  - ✗ `+20.5pp` × 0 @ L
  - ✓ `+20.5` × 5 @ L313,607,1385,1442,1443
  - ✗ `16.5, 24.5` × 0 @ L
  - ✗ `2.1\times10^{-22}` × 0 @ L
  - ✓ `51.1` × 1 @ L1442
  - ✓ `30.6` × 8 @ L394,607,766,771,1385,1398,1442,1443
  - ✓ `+24.0pp` × 9 @ L12,27,88,276,313,395,607,1385
  - ✓ `+24.0` × 12 @ L12,27,88,276,313,395,607,1385
  - ✗ `20.5, 27.5` × 0 @ L
  - ✓ `2.3\times10^{-41}` × 4 @ L313,607,1385,1443
  - ✓ `54.6` × 4 @ L394,1384,1396,1443
  - ✓ `30.6` × 8 @ L394,607,766,771,1385,1398,1442,1443
  - ✗ `+20.7pp` × 0 @ L
  - ✓ `+20.7` × 1 @ L1444
  - ✗ `17.3, 24.0` × 0 @ L
  - ✓ `1.2\times10^{-35}` × 1 @ L1444
  - ✓ `59.4` × 1 @ L1444
  - ✓ `38.7` × 1 @ L1444
  - ✓ `+11.3pp` × 4 @ L315,1527,1807,1817
  - ✓ `+11.3` × 5 @ L315,1445,1527,1807,1817
  - ✗ `8.7, 13.9` × 0 @ L
  - ✓ `1.1\times10^{-19}` × 1 @ L1445
  - ✓ `60.1` × 5 @ L1387,1445,1446,1447
  - ✓ `48.8` × 3 @ L1445,1509,1639
  - ✗ `+10.6pp` × 0 @ L
  - ✓ `+10.6` × 1 @ L1446
  - ✗ `8.1, 13.1` × 0 @ L
  - ✓ `1.7\times10^{-18}` × 1 @ L1446
  - ✓ `60.1` × 5 @ L1387,1445,1446,1447
  - ✓ `49.5` × 4 @ L674,695,761,1446
  - ✗ `+0.0pp` × 0 @ L
  - ✗ `+0.0` × 0 @ L
  - ✓ `0.0, 0.0` × 1 @ L1447
  - ✗ `1.000` × 0 @ L
  - ✓ `60.1` × 5 @ L1387,1445,1446,1447
  - ✓ `60.1` × 5 @ L1387,1445,1446,1447
**F08x.undefined_behavior · 676f 子组 undefined_behavior：Δ +58.1pp，BH-FDR p=1e-06，Bonferroni p=1e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+58.1pp` × 0 @ L
  - ✓ `+58.1` × 1 @ L1459
  - ✓ `1.0\times10^{-6}` × 3 @ L1459,1460
  - ✓ `1.0\times10^{-6}` × 3 @ L1459,1460
  - ✓ `43` × 3 @ L665,1190,1459
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.memory_safety · 676f 子组 memory_safety：Δ +46.9pp，BH-FDR p=1e-06，Bonferroni p=3e-06** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+46.9pp` × 0 @ L
  - ✓ `+46.9` × 1 @ L1460
  - ✓ `1.0\times10^{-6}` × 3 @ L1459,1460
  - ✓ `3.0\times10^{-6}` × 1 @ L1460
  - ✓ `49` × 6 @ L674,695,761,1446,1460,1844
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.legacy · 676f 子组 legacy：Δ +36.2pp，BH-FDR p=5.6e-05，Bonferroni p=0.00017** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+36.2pp` × 0 @ L
  - ✓ `+36.2` × 1 @ L1461
  - ✓ `5.6\times10^{-5}` × 1 @ L1461
  - ✓ `1.7\times10^{-4}` × 2 @ L1461,1462
  - ✓ `47` × 1 @ L1461
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.stl · 676f 子组 stl：Δ +15.0pp，BH-FDR p=0.00017，Bonferroni p=0.00067** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+15.0pp` × 0 @ L
  - ✓ `+15.0` × 1 @ L1462
  - ✓ `1.7\times10^{-4}` × 2 @ L1461,1462
  - ✓ `6.7\times10^{-4}` × 1 @ L1462
  - ✓ `100` × 17 @ L693,695,1339,1372,1373,1462,1596,1597
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.real_world · 676f 子组 real_world：Δ +29.5pp，BH-FDR p=0.00054，Bonferroni p=0.0027** — consistent/active `✗✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+29.5pp` × 0 @ L
  - ✓ `+29.5` × 1 @ L1463
  - ✓ `5.4\times10^{-4}` × 1 @ L1463
  - ✓ `0.003` × 1 @ L1855
  - ✓ `44` × 6 @ L579,854,858,1463,1500,1564
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.optimization_sensitive · 676f 子组 optimization_sensitive：Δ +55.0pp，BH-FDR p=0.0018，Bonferroni p=0.011** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+55.0pp` × 1 @ L1189
  - ✓ `+55.0` × 2 @ L1189,1464
  - ✗ `0.002` × 0 @ L
  - ✗ `0.011` × 0 @ L
  - ✓ `20` × 19 @ L206,208,278,313,416,607,724,822
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.conditional_trigger · 676f 子组 conditional_trigger：Δ +45.0pp，BH-FDR p=0.0061，Bonferroni p=0.043** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+45.0pp` × 0 @ L
  - ✓ `+45.0` × 1 @ L1465
  - ✗ `0.006` × 0 @ L
  - ✗ `0.043` × 0 @ L
  - ✓ `20` × 19 @ L206,208,278,313,416,607,724,822
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.concurrency · 676f 子组 concurrency：Δ +7.3pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+7.3pp` × 1 @ L1475
  - ✓ `+7.3` × 2 @ L1466,1475
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `109` × 2 @ L1466,1474
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.language_semantics · 676f 子组 language_semantics：Δ +17.8pp，BH-FDR p=0.0095，Bonferroni p=0.086** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+17.8pp` × 0 @ L
  - ✓ `+17.8` × 1 @ L1467
  - ✗ `0.010` × 0 @ L
  - ✗ `0.086` × 0 @ L
  - ✓ `45` × 7 @ L696,1441,1465,1467,1863,1869,2097
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.embedded · 676f 子组 embedded：Δ +8.1pp，BH-FDR p=0.034，Bonferroni p=0.34** — consistent/active `✗✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✗ `+8.1pp` × 0 @ L
  - ✓ `+8.1` × 2 @ L1446,1468
  - ✗ `0.034` × 0 @ L
  - ✗ `0.344` × 0 @ L
  - ✓ `74` × 16 @ L674,695,761,1322,1340,1468,1477,1501
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F08x.odr_link · 676f 子组 odr_link：Δ +6.7pp，BH-FDR p=1，Bonferroni p=1** — consistent/active `✓✓✗✗✓`
- 源：`data/a5_676f_results.json`
  - ✓ `+6.7pp` × 1 @ L1473
  - ✓ `+6.7` × 2 @ L1469,1473
  - ✗ `1.000` × 0 @ L
  - ✗ `1.000` × 0 @ L
  - ✓ `15` × 17 @ L579,823,1003,1052,1239,1369,1462,1469
  - 注：子组 p 必须报校正后值；未校正 p 不得单独宣称显著
**F09x · 676f 子组检验族大小 11** — consistent/active `✓`
- 源：`data/a5_676f_results.json`
  - ✓ `11` × 31 @ L89,315,399,437,453,583,693,695
**F10x.planted_false · 676f 真实缺陷 planted=false: FD 64.7% (22/34)，Δ +29.4pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `64.7` × 1 @ L1479
  - ✗ `22/34` × 0 @ L
  - ✓ `+29.4pp` × 1 @ L1480
  - ✗ `14.1, 44.7` × 0 @ L
  - ✓ `2.0\times10^{-3}` × 1 @ L1480
  - ✓ `35.3` × 2 @ L1441,1479
**F10x.planted_true · 676f planted=true: FD 53.9% (287/532)，Δ +23.7pp** — consistent/active `✓✗✓✗✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `53.9` × 1 @ L1481
  - ✗ `287/532` × 0 @ L
  - ✓ `+23.7pp` × 1 @ L1481
  - ✗ `20.1, 27.3` × 0 @ L
  - ✓ `2.4\times10^{-38}` × 1 @ L1481
  - ✓ `30.3` × 1 @ L1481
**F11x · 676f 资产诊断：8 资产各自 catch 率；wunsequenced/compile-time 100% unknown（退化）** — consistent/active `✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓`
- 源：`data/a5_676f_results.json`
  - ✓ `35.1` × 1 @ L1366
  - ✓ `399` × 1 @ L1366
  - ✓ `0.88` × 4 @ L1366,1367,1368,1371
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
  - ✓ `0` × 217 @ L96,201,202,203,205,207,209,314
  - ✓ `100` × 17 @ L693,695,1339,1372,1373,1462,1596,1597
  - ✓ `12.6` × 1 @ L1370
  - ✓ `143` × 1 @ L1370
  - ✓ `15.0` × 2 @ L1369,1462
  - ✓ `170` × 3 @ L990,1369,1610
  - ✓ `3.34` × 1 @ L1369
  - ✓ `0.9` × 1 @ L1557
  - ✓ `10` × 37 @ L14,15,94,342,436,437,498,508
  - ✓ `22.4` × 1 @ L1368
  - ✓ `255` × 2 @ L1368,1773
  - ✓ `0.88` × 4 @ L1366,1367,1368,1371
  - ✓ `23.6` × 1 @ L1367
  - ✓ `268` × 1 @ L1367
  - ✓ `0.88` × 4 @ L1366,1367,1368,1371
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
  - ✓ `0` × 217 @ L96,201,202,203,205,207,209,314
  - ✓ `100` × 17 @ L693,695,1339,1372,1373,1462,1596,1597
  - 注：退化资产是 A5 主/并列分析差异的唯一来源
**G01x · 676g 总盘：n=1147，catch 707，miss 440，盲区比 38.4%** — consistent/active `✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `1147` × 14 @ L87,136,195,335,344,407,767,1496
  - ✓ `707` × 3 @ L1496,1553,2037
  - ✓ `440` × 3 @ L407,1496,1553
  - ✓ `38.4` × 11 @ L90,195,288,299,407,543,767,1497
**G02x · 676g 互补性：6 资产并集 61.6%，最佳单资产 35.6%** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `61.6` × 4 @ L288,767,1554,1605
  - ✓ `707` × 3 @ L1496,1553,2037
  - ✓ `35.6` × 3 @ L767,1554,1556
**G03x · 676g 逐资产覆盖率（asan/ubsan/tsan/compiler-warn/cross-compile/linker）** — consistent/active `✓✓✓✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `35.6` × 3 @ L767,1554,1556
  - ✓ `23.5` × 1 @ L1556
  - ✓ `22.9` × 1 @ L1556
  - ✓ `12.5` × 3 @ L694,1266,1556
  - ✓ `10.6` × 2 @ L1446,1557
  - ✓ `0.9` × 1 @ L1557
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
  - ✓ `0.0` × 24 @ L314,396,404,454,607,695,771,774
**G04x · 676g 按 planted：true 41.0% [38.0, 44.1]；false 21.6% [13.8, 32.3]** — consistent/active `✓✓✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `41.0` × 2 @ L1500,1564
  - ✓ `38.0, 44.1` × 2 @ L1500,1564
  - ✓ `21.6` × 2 @ L1501,1564
  - ✓ `13.8, 32.3` × 2 @ L1501,1564
  - ✓ `74` × 16 @ L674,695,761,1322,1340,1468,1477,1501
**G05x · 676g 盲区分带：18 个类型 >50% 盲；类型总数 70** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `18` × 10 @ L19,364,414,532,588,1083,1446,1687
  - ✓ `70` × 2 @ L19,1786
  - ✓ `50` × 19 @ L299,409,569,579,588,767,806,1198
**G06x · 676g TSan 稳定性：3/180 不稳定（1.7%）** — consistent/active `✓✓✓`
- 源：`data/blindspot_676g_stats.json`
  - ✓ `3` × 67 @ L8,10,91,139,187,284,367,454
  - ✓ `180` × 3 @ L1368,1510,1568
  - ✓ `1.7` × 7 @ L689,739,1446,1461,1462,1511,1569
**E01 · clang-analyzer holdout 48.8% (20/41) p=1.2e-4** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `48.8` × 3 @ L1445,1509,1639
  - ✗ `20/41` × 0 @ L
  - ✓ `1.2\times10^{-4}` × 1 @ L1639
**E02 · cppcheck holdout 41.5% (17/41) p=1.5e-5** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `41.5` × 4 @ L90,413,1640,1848
  - ✗ `17/41` × 0 @ L
  - ✓ `1.5\times10^{-5}` × 1 @ L1640
**E03 · cppcheck corpus 54.7% (35/64) p=0.38331031799316406** — consistent/active `✓✗✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `54.7` × 1 @ L1640
  - ✗ `35/64` × 0 @ L
  - ✓ `0.383` × 1 @ L1640
**E03b · cppcheck corpus Δ +7.8pp CI[-6.1, 21.7]（CI 跨 0 ⇒ tie）** — consistent/active `✓✓✗`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+7.8pp` × 1 @ L1645
  - ✓ `-6.1, 21.7` × 1 @ L1645
  - ✗ `(13,8)` × 0 @ L
**E04 · E9 附录 StrictA 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1639,1640
  - ✓ `1/11` × 2 @ L1639,1640
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E05 · E9 附录 cppcheck 主口径 对照 FPR 9.1% (1/11)** — consistent/active `✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `9.1\% (1/11)` × 2 @ L1639,1640
  - ✓ `1/11` × 2 @ L1639,1640
  - 注：控制组 n=11（= holdout 对照样本数）；分母必须是 11
**E06 · E9 附录：holdout Δ(FD−StrictA) +34.1pp [19.6, 48.7]，对子 (14,0)** — consistent/active `✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `+34.1pp` × 1 @ L1644
  - ✓ `19.6, 48.7` × 1 @ L1644
  - ✓ `(14,0)` × 1 @ L1644
**E07 · E9 附录：corpus StrictA 34.4% (22/64)，Δ +28.1pp 对子 (23,5)，p=9.1e-4** — consistent/active `✓✗✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `34.4` × 1 @ L1639
  - ✗ `22/64` × 0 @ L
  - ✓ `+28.1pp` × 1 @ L1645
  - ✓ `(23,5)` × 1 @ L1645
  - ✓ `9.1\times10^{-4}` × 1 @ L1639
**E08 · E9 附录：corpus 分层 FD/ct/cp（sanitizer 29/17/26；compiler-warn 9/5/8；cross-compile 2/0/1）** — consistent/active `✗✗✓✓✓✓✓`
- 源：`data/673e_comparison_stats.json`
  - ✗ `29 / 17 / 26` × 0 @ L
  - ✗ `9 / 5 / 8` × 0 @ L
  - ✓ `2 / 0 / 1` × 1 @ L1650
  - ✓ `12` × 21 @ L27,398,568,589,693,694,770,771
  - ✓ `FD 29 vs clang-analyzer 17 / cppcheck 26` × 1 @ L1649
  - ✓ `FD 9 / cppcheck 8` × 1 @ L1649
  - ✓ `2 / 0 / 1` × 1 @ L1650
**E10 · E9 附录：clang-tidy 主口径 holdout 100% recall / 100% FPR（零区分度 ⇒ 该口径被弃用）** — consistent/active `✗✓✗✓✗✗`
- 源：`data/673e_comparison_stats.json`
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 17 @ L693,695,1339,1372,1373,1462,1596,1597
  - ✗ `100.0` × 0 @ L
  - ✓ `100` × 17 @ L693,695,1339,1372,1373,1462,1596,1597
  - ✗ `41/41` × 0 @ L
  - ✗ `11/11` × 0 @ L
**E09 · E9 附录：8 个反向对（工具 catch / FD miss）** — consistent/active `✓`
- 源：`data/673e_comparison_stats.json`
  - ✓ `8` × 53 @ L136,336,569,625,693,743,765,767
**F01 · 外部锚点子集 A（准则原文）28.6% (10/35) CI[14.6,46.3]** — consistent/active `✓✗✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `28.6` × 3 @ L578,697,765
  - ✗ `10/35` × 0 @ L
  - ✗ `14.6, 46.3` × 0 @ L
**F02 · 外部锚点子集 B（UB 片段重建）80.0% (12/15)** — consistent/active `✓✗`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `80.0` × 2 @ L579,841
  - ✗ `12/15` × 0 @ L
**F03 · 外部锚点合计 44.0% (22/50)；扫描规则 87** — consistent/active `✓✗✓✓✓✓✓✓`
- 源：`data/external_anchor_reveal_672j.json`
  - ✓ `44.0` × 1 @ L579
  - ✗ `22/50` × 0 @ L
  - ✓ `22` × 12 @ L415,1049,1050,1083,1368,1442,1556,1627
  - ✓ `50` × 19 @ L299,409,569,579,588,767,806,1198
  - ✓ `87` × 6 @ L577,665,844,845,1021,1323
  - ✓ `35` × 21 @ L336,422,516,545,578,665,767,1022
  - ✓ `15` × 17 @ L579,823,1003,1052,1239,1369,1462,1469
  - ✓ `11/60` × 1 @ L583
**F04 · LLM 臂：GLM-4 12/12 vs FD 6/12；对照误报 4/8 = 50%** — consistent/active `✓✓✓✓✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✓ `12/12` × 2 @ L568,1308
  - ✓ `6/12` × 1 @ L568
  - ✓ `4/8` × 2 @ L569,1308
  - ✓ `50.0` × 2 @ L588,1562
  - ✓ `50.0` × 2 @ L588,1562
  - 注：FD 的 6/12 由 fd_detect_rate_pct=50.0% × llm_n 重算得到
**F05 · LLM 臂配对 b/c = (0,6)，p=0.03125** — consistent/active `✗✓`
- 源：`data/experiments/llm_arm_672i.json`
  - ✗ `0,6` × 0 @ L
  - ✓ `0.031` × 1 @ L570
**G01 · 变异（core）110/114 = 96.5%** — consistent/active `✓✓✗`
- 源：`data/656_mutation_report.json`
  - ✓ `110/114` × 2 @ L830,845
  - ✓ `96.5` × 3 @ L773,845,1023
  - ✗ `91.3, 99.0` × 0 @ L
**G02 · 变异（all-scope）130/159 = 81.8%** — consistent/active `✓✓`
- 源：`data/656_mutation_report_all.json`
  - ✓ `130/159` × 1 @ L830
  - ✓ `81.8` × 1 @ L1023
**G03 · 缺陷重注入 6/6 = 100%；total 15；软覆盖 12/15** — consistent/active `✓✗✓`
- 源：`data/defect_injection_661.json`
  - ✓ `6/6` × 2 @ L693,695
  - ✗ `12/15` × 0 @ L
  - ✓ `15` × 17 @ L579,823,1003,1052,1239,1369,1462,1469
**H01 · 样本量：独立两比例 0.35→0.50 ⇒ n=170** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=None, α=0.05, power=0.8, recomputed=169.09`
  - ✓ `170` × 3 @ L990,1369,1610
  - ✗ `170 (holdout)` × 0 @ L
**H02 · 样本量：独立两比例 0.35→0.55 ⇒ n=96** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.55,psi=None, α=0.05, power=0.8, recomputed=95.77`
  - ✓ `96` × 5 @ L773,845,991,1023,1609
  - ✗ `96 (holdout)` × 0 @ L
**H03 · 样本量：独立两比例 0.35→0.45 ⇒ n=376** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.45,psi=None, α=0.05, power=0.8, recomputed=375.27`
  - ✓ `376` × 1 @ L992
  - ✗ `376 (holdout)` × 0 @ L
**H04 · 样本量：配对 ψ=0.3 ⇒ n=103** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.3, α=0.05, power=0.8, recomputed=102.26`
  - ✓ `103` × 3 @ L993,1334,1347
  - ✗ `103 (holdout)` × 0 @ L
**H05 · 样本量：配对 ψ=0.4 ⇒ n=138** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.4, α=0.05, power=0.8, recomputed=137.15`
  - ✓ `138` × 1 @ L994
  - ✗ `138 (holdout)` × 0 @ L
**H06 · 样本量：配对 ψ=0.5 ⇒ n=173** — consistent/active `✓✗`
- 源：`Cohen arcsine h + Connor 配对；p1=0.35,p2=0.5,psi=0.5, α=0.05, power=0.8, recomputed=172.04`
  - ✓ `173` × 6 @ L823,995,1385,1485,1514,1813
  - ✗ `173 (holdout)` × 0 @ L
**K01 · tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现** — consistent/unpinned_no_artifact `✓✓`
- 源：`data/656_mutation_report*.json 现存值为 110/114 与 130/159；全仓扫描 `30/48` 无产物命中（唯一产出是更早被覆盖的报告）`
  - ✓ `62.5` × 8 @ L674,695,761,829,840,1026,1207,1638
  - ✓ `30/48` × 2 @ L829,840
  - 注：论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注）
**K02 · tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径** — consistent/unpinned_retired_caliber `✓`
- 源：`仅能追溯到 research/paper_v0.4.md 与 data/669_caliber_report.json::doc_sightings；对应 -O1 单档产物已被 665/668 双档口径取代`
  - ✓ `66.7` × 3 @ L271,831,842
  - 注：该值口径已退休，只能作为“当时口径下读到的数”引用
**I01 · Static holdout 1/41 CI ⇒ [0.1, 12.9]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(1,41)])"`
  - ✓ `0.1, 12.9` × 1 @ L693
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I02 · Random† holdout 4/41 CI ⇒ [2.7, 23.1]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(4,41)])"`
  - ✓ `2.7, 23.1` × 1 @ L694
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I03 · FD holdout 34/41 CI ⇒ [67.9, 92.8]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,41)])"`
  - ✓ `67.9, 92.8` × 4 @ L674,695,761,847
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I04 · Caliber B holdout 34/42 CI ⇒ [65.9, 91.4]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(34,42)])"`
  - ✓ `65.9, 91.4` × 2 @ L675,676
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I05 · Static corpus 11/64 CI ⇒ [8.9, 28.7]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(11,64)])"`
  - ✓ `8.9, 28.7` × 1 @ L693
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I06 · Random† corpus 14/64 CI ⇒ [12.5, 34.0]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(14,64)])"`
  - ✓ `12.5, 34.0` × 1 @ L694
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I07 · FD corpus 40/64 CI ⇒ [49.5, 74.3]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,64)])"`
  - ✓ `49.5, 74.3` × 3 @ L674,695,761
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I08 · Caliber B corpus 40/73 CI ⇒ [42.7, 66.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,73)])"`
  - ✓ `42.7, 66.5` × 1 @ L675
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I09 · Caliber C corpus 40/76 CI ⇒ [40.8, 64.2]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(40,76)])"`
  - ✓ `40.8, 64.2` × 1 @ L676
  - 注：用仓库自带 tools/stat_bounds.py::cp_interval 现算
**I10 · 对照 FPR 0/11 CI ⇒ [0.0, 28.5]** — consistent/active `✓`
- 源：`python -c "import sys;sys.path.insert(0,'tools');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(0,11)])"`
  - ✓ `0.0, 28.5` × 1 @ L695
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
  - ✓ `105` × 1 @ L1188
  - ✗ `840` × 0 @ L
  - ✓ `8` × 53 @ L136,336,569,625,693,743,765,767
**A19 · ±5pp 缺口：holdout 还差 195，corpus 还差 314** — consistent/active `✓✓`
- 源：`sample_size_672k.±5pp.n − 当前可测 n`
  - ✓ `195` × 1 @ L1002
  - ✓ `314` × 1 @ L1002
**D11 · clone-aware 重切分 Δ +23.0~+26.7pp（677b，逐 split 为 +23.02/+25.70）** — consistent/active `✓✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_a5_results_family_random.json / _family_stratified.json`
  - ✓ `23.02` × 2 @ L1407,1760
  - ✓ `25.70` × 2 @ L1407,1761
**D12 · cluster bootstrap 有效 n≈133–140（677b，design effect ≈4.1–4.3）** — consistent/active `✗✓`
- 源：`current_numbers.a5_experiments.clone_aware_677b ← data/677b_cluster_bootstrap.json`
  - ✗ `133` × 0 @ L
  - ✓ `140` × 10 @ L292,315,400,525,766,771,1386,1410
**D13 · 非退化池选择效应 +11.31pp（677c，k=1，p=6.02e-08）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `11.31` × 3 @ L771,1400,1417
**D14 · 退化资产对均值的贡献 ≈+12.81pp（677c）** — consistent/active `✓`
- 源：`current_numbers.a5_experiments.nondegenerate_pool_677c ← data/677c_a5_nondegenerate_results.json`
  - ✓ `12.81` × 1 @ L1419
**Z01 · 689 TOST：±10pp 未过，90% CI [-10.61, 5.52]pp，p_TOST=0.064** — consistent/active `✓✓✓`
- 源：`current_numbers.reframed_689.equivalence_tost ← data/689_equivalence_test.json`
  - ✓ `-10.61` × 5 @ L15,94,436,1851,2040
  - ✓ `5.52` × 5 @ L15,94,436,1851,2040
  - ✓ `0.064` × 3 @ L436,2040,2041
**E02 · 689 TOST 最小通过 margin 10.61pp（deff 校正 11.67pp）** — consistent/active `✓✓`
- 源：`data/689_equivalence_test.json`
  - ✓ `10.61` × 9 @ L15,94,436,437,1851,1852,2040,2041
  - ✓ `11.67` × 2 @ L437,2043
**E03 · 689 标准化：正向 -17.92pp（R_syn_std=77.01%），反向 +1.70pp，类型级 -13.52pp** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.standardized_analysis ← data/689_standardized_analysis.json`
  - ✓ `-17.92` × 4 @ L16,440,1852,2053
  - ✓ `77.01` × 2 @ L439,2052
  - ✓ `1.70` × 2 @ L441,2055
  - ✓ `-13.52` × 2 @ L444,2056
**E04 · 689 环境：真实 59.09%→23.64%（-35.45pp，Δunknown=0），clang↔g++ 93.5%** — consistent/active `✓✓✓✓`
- 源：`current_numbers.reframed_689.environment_metrics ← data/689_environment_metrics.json`
  - ✓ `59.09` × 11 @ L92,284,414,420,434,776,1843,2037
  - ✓ `23.64` × 4 @ L92,422,2067,2068
  - ✓ `35.45` × 2 @ L422,516
  - ✓ `93.5` × 4 @ L425,534,1909,2072
