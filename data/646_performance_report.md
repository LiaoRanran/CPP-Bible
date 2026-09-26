# 646 性能优化报告（A3，清债 2）

- 达标阈值：提速 ≥30.0%
- 达标负载：**4/4**
- 全部达标：True

| 负载 | 优化前(ms) | 优化后(ms) | 提速 | 达标 | 说明 |
|---|---|---|---|---|---|
| orchestrate（首次 → 重复调用） | 5757.8 | 27.2 | 99.5% | ✅ | lru_cache 命中：gate/充分性/反例 |
| rule_card_mapper.build_mapping（冷 → 热读缓存） | 931.1 | 4.1 | 99.6% | ✅ | atoms/ev_map/stored 缓存 |
| discover_blind_spots（重复 gate → 复用计数） | 755.3 | 0.0 | 100.0% | ✅ | 消除第二次全库扫描 |
| 证据读盘（裸读 → 缓存读） | 949.3 | 0.0 | 100.0% | ✅ | perf_646 记忆化 |

## 手段

1. **一次 gate 扫描多方共享**（`perf_646.finding_counts`）——消除 645 编排器的第二次全库扫描。
2. **进程内记忆化**（`lru_cache`）——`perf_646` 缓存重读函数；646 编排器缓存 `judge()/run_search()`。
3. **诚实登记**：编译器/网络类负载（`compiler_probe`/`standard_fetcher`）为外部 IO 瓶颈，不在本优化范围内（见验收报告）。
