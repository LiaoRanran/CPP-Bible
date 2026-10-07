# 683-C2 · 7 基线统一口径对比（含 2000 次随机分布）


## Pool A（Pool A（严格）），k=4

| 方法 | selection | rate% | CP95 | Δ vs random(pp) | p |
|---|---|---:|---|---:|---:|
| greedy | asan,ubsan,tsan,compiler-warn | 56.0071 | [51.807, 60.1441] | 1.4134 | 0.302 |
| oracle | asan,compiler-warn,tsan,ubsan | 56.0071 | [51.807, 60.1441] | 1.4134 | 0.302 |
| random_single | tsan,ubsan,cross-compile,asan | 54.5936 | [50.3886, 58.7505] | 0.0 | 1 |
| fd | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 0.0 | 1 |
| frequency | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 0.0 | 1 |
| info_gain | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 0.0 | 1 |
| static | compiler-warn,cross-compile | 24.0283 | [20.5634, 27.7668] | -30.5654 | 8.05e-34 |

随机分布：n=2000、均值 52.9869%、中位 54.2403%、SD 2.5804pp、95% 区间 [48.7633, 56.0071]%、**FD 位于第 61.2 百分位**

## Pool B（Pool B（中等）），k=4

| 方法 | selection | rate% | CP95 | Δ vs random(pp) | p |
|---|---|---:|---|---:|---:|
| greedy | asan,ubsan,tsan,compiler-warn | 56.0071 | [51.807, 60.1441] | 16.6078 | 2.33e-16 |
| oracle | asan,compiler-warn,tsan,ubsan | 56.0071 | [51.807, 60.1441] | 16.6078 | 2.33e-16 |
| fd | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 15.1943 | 5.92e-13 |
| frequency | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 15.1943 | 5.92e-13 |
| info_gain | asan,ubsan,tsan,cross-compile | 54.5936 | [50.3886, 58.7505] | 15.1943 | 5.92e-13 |
| random_single | linker,ubsan,compiler-warn,cross-compile | 39.3993 | [35.3499, 43.56] | 0.0 | 1 |
| static | compiler-warn,cross-compile,linker | 24.735 | [21.2317, 28.5043] | -14.6643 | 2.07e-25 |

随机分布：n=2000、均值 48.4042%、中位 48.7633%、SD 4.9385pp、95% 区间 [39.3993, 56.0071]%、**FD 位于第 87.0 百分位**
