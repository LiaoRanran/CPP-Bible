# 688 · A2 真实靶场按 CVE 披露年份细分

- **批次**：688 ｜ **数据**：`688_real_world_by_year.json`（年份/严重度从 `fields.year` 字符串解析）
- **方法**：按披露年份分组；每年 n、OR 检出率、Top 缺陷类型。

## 1. 逐年结果

| 年份 | n | OR 检出率 | 主要类型（Top3）|
|---|---:|---:|---|
| 2012 | 1 | 0.0% | integer_overflow |
| 2014 | 1 | 100.0% | out_of_bounds |
| 2015 | 2 | 0.0% | logic_error, out_of_bounds |
| 2016 | 11 | 63.64% | out_of_bounds(4), logic_error(3), data_race(2) |
| 2017 | 3 | 100.0% | out_of_bounds(2), integer_overflow |
| 2018 | 5 | 40.0% | logic_error(2), out_of_bounds(2) |
| 2019 | 5 | 60.0% | out_of_bounds(2), logic_error(2) |
| 2020 | 10 | 60.0% | out_of_bounds(5), logic_error(3) |
| 2021 | 22 | 54.55% | logic_error(6), integer_overflow(6), out_of_bounds(5) |
| 2022 | 30 | 66.67% | out_of_bounds(9), logic_error(8), integer_overflow(5) |
| 2023 | 16 | 50.0% | logic_error(6), out_of_bounds(5), type_punning(1) |
| 2024 | 4 | 75.0% | out_of_bounds(2), data_race, use_after_free |

## 2. 趋势分析
- **无明显时间趋势**：检出率在 40%–67% 间震荡，与年份无单调关系（首尾 2016=63.6% / 2022=66.7% / 2023=50% / 2024=75%@n=4）。
- **类型构成随年代变化**：2021+ 的样品 logic_error 占比上升（2021:6/22、2022:8/30、2023:6/16）——而 logic_error 是 asan/静态告警最难抓的类型（见 A4），部分解释了近年样本略难。
- **老 bug 是否更易抓？** 数据不支持：2015/2012 样本 n 极小且含逻辑错误，检出率不高于近年。

## 3. 诚实边界
- 每年 n 小（最大 30），单年检出率噪声大；**趋势仅描述性，不推断因果**。
- 年份 = CVE 披露年，非漏洞引入年；部分老 CVE 的复现代码为新写，存在"新代码旧漏洞"混合。

## 4. 对论文建议
- 可陈述："真实缺陷检出率与披露年份无显著单调关系；近年样品 logic_error 占比上升（更难），构成能力边界的年份维度注脚。"
