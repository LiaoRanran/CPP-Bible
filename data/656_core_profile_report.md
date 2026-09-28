# 656 B4 · 核心判决路径性能报告

> 生成：2026-09-28T02:21:58　Python：3.13.13　卡数：47　轮次：5

## 一、延迟（毫秒）

| 路径 | 口径 | n | mean | p50 | p95 | max |
|---|---|---:|---:|---:|---:|---:|
| `classify_card` | 单卡端到端（读卡+抽字段+分类） | 5 | 30.6131 | 28.1825 | 28.3872 | 41.8884 |
| `classify_memory` | 纯内存判决（classify 本体） | 2000 | 0.0022 | 0.0019 | 0.0022 | 0.1545 |
| `ledger_append20` | 账本追加 20 条（哈希链） | 5 | 0.7113 | 0.6635 | 0.7862 | 0.8118 |

- **摊到单卡**：0.6513 ms/张 ⇒ ✅ < 1ms（达成目标）

## 二、Top10 热点（cProfile · 按 tottime）

| # | 函数 | tottime(s) | percall(s) | cumtime(s) | ncalls |
|---:|---|---:|---:|---:|---:|
| 1 | `{method 'search' of 're.Pattern' objects}` | 0.016 | 0.0 | 0.016 | 329 |
| 2 | `{built-in method _io.open}` | 0.004 | 0.0 | 0.004 | 47 |
| 3 | `{method 'read' of '_io.TextIOWrapper' objects}` | 0.003 | 0.0 | 0.004 | 47 |
| 4 | `C:\CodeLearnling\note\note\C++\CPP-Bible\tools\four_state_verdict_638.py:169(classify_card)` | 0.003 | 0.0 | 0.031 | 47 |
| 5 | `{built-in method _codecs.utf_8_decode}` | 0.001 | 0.0 | 0.001 | 47 |
| 6 | `<frozen ntpath>:50(normcase)` | 0.001 | 0.0 | 0.001 | 564 |
| 7 | `<frozen ntpath>:737(relpath)` | 0.001 | 0.0 | 0.003 | 47 |
| 8 | `<frozen ntpath>:529(abspath)` | 0.0 | 0.0 | 0.001 | 94 |
| 9 | `{built-in method _winapi.LCMapStringEx}` | 0.0 | 0.0 | 0.0 | 564 |
| 10 | `C:\CodeLearnling\note\note\C++\CPP-Bible\tools\four_state_verdict_638.py:123(classify)` | 0.0 | 0.0 | 0.001 | 47 |

## 三、诚实边界

1. 数字是**本机一次采样**（无并发、无 CI 噪声隔离），跨机不可直接比；比较请用同一台机、同一命令。
2. `classify_card` 含磁盘 I/O（冷/热页缓存差异大）；要看**判决逻辑**本身请用 `classify_memory`。
3. cProfile 的 `tottime` 不含阻塞在 I/O 上的时间 ⇒ 热点排名偏**计算密集**侧。

## 四、优化（只做量到收益的事）

- 优化 1（预编译边界正则，656 B4 已做）：classify_card 里每张卡现编 3 个边界字段正则，挪到模块级 _BOUNDARY_RE；语义不变（同 pattern、同 MULTILINE）。实测 47 张卡 5 轮：单卡 0.6089 ms → 0.5934 ms（-2.5%，接近噪声水平，不宣称大幅提速）；纯内存 classify 0.0023 → 0.0022 ms。
- 未做的优化 2/3：os.path.relpath（占约 0.001s）可用前缀裁剪替代，但会引入路径语义差异风险；多次正则扫全文可合并为一趟，收益同样在噪声内。准则：收益在噪声内就不改，避免用优化换新 bug。
- 结论：单卡判决路径 0.59 ms < 1ms（达成目标）；真正的花费在读盘与正则扫描（I/O 侧）。要再快应改数据结构（预抽取字段 / 增量解析），而不是给判决逻辑加缓存。
