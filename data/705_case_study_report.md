# 705-A · 真实缺陷案例深读汇总报告

- 生成：只读 683 冻结检测矩阵 + 683 失败/成功案例深读，未跑新 detect()。
- 案例总数：**28** 条
  - 独苗命中（unique-hit，单资产 catch 其余 miss）：22 条
  - 8 资产全漏（miss）：6 条
  - 多资产联合命中：0 条
- 覆盖缺陷类型：data_race, double_free, integer_overflow, logic_error, memory_leak, out_of_bounds, type_punning, use_after_free

## 选择标准
按任务卡优先级：① 8 资产全漏的（最有故事性）；② 独苗命中的（说明为何只有该检测器能抓）；
③ 跨类型（内存安全/UB/逻辑/并发各选）；④ 高知名度项目（OpenSSL/Linux/FFmpeg/curl/glibc 等）。

## 文件清单
- `data/case_studies/<CVE_ID>.md`（28 个）
- `data/case_studies/README.md`

## 诚实边界
- 案例卡片的'为什么漏了'基于 683 归因分类（a/c/d/f）推理，非新实验。
- '修复 commit' 在 683 冻结数据中缺失，统一标'数据待补'（见 NVD 来源链接）。
- '对论文的意义'是素材建议，最终采用权在作者；本批未改论文正文。
