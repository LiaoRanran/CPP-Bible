# 683-D4 · 演示视频脚本（3 分钟，分镜 + 旁白）

> 用途：GitHub Pages 首页 / 投稿补充材料 / 组会演示。总时长 ≈ 3:00。
> 录制方式：纯屏幕录屏（docs/ 官网 + 终端），无需真人出镜；字幕中英双语可选。

## 时间轴总览

| 时间 | 分镜 | 画面 | 旁白（中文） | 旁白（English, optional） |
|---|---|---|---|---|
| 0:00–0:18 | S1 冷开场 | 黑底白字逐行打字：`pass / fail / unknown / contradict`，然后四态聚成一个问号 | "检测器给出的答案，不只有对与错。阙疑的第一个设计决策：承认'不知道'。" | "Verifiers don't just say yes or no. Queyi's first design decision: admitting 'unknown'." |
| 0:18–0:45 | S2 问题 | 热力图（34 类 × 8 资产）缓慢推近，红色盲区格闪动 | "在一个 1,147 样本、8 个检测器的全量矩阵里，三分之一的缺陷类型盲区超过 50%。没有单个检测器是够用的。" | "Across 1,147 samples and 8 detectors, a third of defect types are blind in >50% of cases. No single detector is enough." |
| 0:45–1:15 | S3 方法 | 动画：失败样本集合 → 四个分量分数（failure/novel/cost/redundancy）→ 选中下一个资产；循环两轮 | "阙疑把'选哪些检测器'变成一个可演化的算子：上一轮的失败驱动下一轮的选择。四分量打分，全部只用派生集信息——不是事后挑好看的。" | "Queyi turns detector selection into an evolving operator: last round's failures drive the next round's choice." |
| 1:15–1:45 | S4 结果 | Results 页：A5 四 split 柱状图 + 5,000 次随机分布钟形曲线，FD 点落在第 97.3 百分位 | "在评估集上，演化选择比预注册随机预算高 24 个百分点（p≈2e-41）；换切分、换种子、穷举 255 个资产子集，结论不翻转。" | "+24pp over a pre-registered random budget; robust to splits, seeds, and all 255 asset subsets." |
| 1:45–2:20 | S5 真实靶场 | 切到 Real-World 页：筛选器点击（OpenSSL→curl→Linux kernel），表格滚动，点开一条 CVE 详情 | "然后是最硬的问题：这些数字在真实缺陷上还算数吗？683 批次收集了 110 条真实缺陷——每条有 CVE 编号、修复 commit 和最小复现，全部经 NVD 在线验证。" | "Do the numbers survive real-world defects? 110 reconstructed defects, every one traceable and NVD-verified." |
| 2:20–2:45 | S6 诚实 | 切到 Results 页工具链表 + 验收报告截图：红字标出"未闭合项清单" | "我们公开全部失败：哪些真实样本漏报、为什么漏、clang 和 g++ 差多少、哪些还没做。这张'未闭合清单'和结果同样重要。" | "We publish every miss, every toolchain gap, and every open item — the honesty list is part of the result." |
| 2:45–3:00 | S7 收尾 | 仓库 URL + CITATION + Apache-2.0 + "reproduce in minutes" | "阙疑：每个数字都能被独立复算的检测器演化框架。代码、数据、论文，全部开源。" | "Queyi — a detector-evolution framework where every number can be independently recomputed. All open source." |

## 制作备注

- **音乐**：低音量环境铺底，S2 热力图处加 1 秒低频震感；S6 降为纯人声。
- **字幕**：关键数字（+24.03pp、97.3 百分位、110/109）以角标固定 3 秒。
- **口径纪律（重要）**：旁白所有数字必须与 `docs/assets/data/core_numbers.json`
  逐位一致；渲染前跑 `python tools/site_683_data.py` 再核对一次。
- **不出现**：任何未闭合项的"乐观化"表述（如"解决了 X"）；一律用"当前证据支持/未闭合"两态。
- **素材清单**：`docs/figures/*.png`（8 张）、Results 页 GIF（热力图 zoom）、
  真实靶场筛选录屏、验收报告"未闭合清单"截图。
