# 688 · A3 真实靶场按 CVSS 严重度细分

- **批次**：688 ｜ **数据**：`688_real_world_by_severity.json`（严重度从 `fields.year` 字符串解析："CRITICAL/HIGH/MEDIUM/LOW"）
- **方法**：按 CVSS 严重度分组；每组 n、OR 检出率、资产分布。

## 1. 结果

| 严重度 | n | OR 检出率 | 主要捕获资产 |
|---|---:|---:|---|
| CRITICAL | 8 | 62.5% | asan(5)/cross-compile(3) |
| HIGH | 65 | 60.0% | asan(30)/tsan(14)/cross-compile(13)/ubsan(8)/compiler-warn(4) |
| MEDIUM | 34 | 61.76% | asan(19)/tsan(11)/ubsan(11)/cross-compile(6) |
| LOW | 3 | 0.0% | 无 |

## 2. 分析
- **严重度与检出率无强相关**：CRITICAL/HIGH/MEDIUM 检出率都在 60%–62.5% 窄带内（差异 <3pp）。
- **LOW 检出率 0% 但 n=3**，统计不可靠，仅描述。
- 资产分布按严重度一致：asan 在所有档位都是主导捕获者（CRITICAL 5/8、HIGH 30/65、MEDIUM 19/34），印证 asan 的核心地位（A5/B2）。

## 3. 解读
- 该结果符合直觉：**Queyi 的 8 资产主要抓内存安全类缺陷（asan/ubsan/tsan），与缺陷严重度无关**——一个 MEDIUM 的内存越界和一个 CRITICAL 的内存越界，被 asan 捕获的概率相同。严重 bug 并不"更容易被检测器抓到"。

## 4. 诚实边界
- 严重度标签来自 NVD 字符串解析，未统一到具体 CVSS 向量；分类依赖源数据。
- 样本严重度分布偏 HIGH（65/110），LOW 仅 3 条，跨严重度比较受不平衡影响。

## 5. 对论文建议
- 可补充一句："缺陷严重度与 Queyi 检出率无显著关联（各档 60–62%），说明当前装置的能力边界由缺陷*类型*而非*严重程度*决定。"
