# 真实缺陷案例深读 · 索引（705-A）

共 28 条案例卡片（独苗命中 + 全漏），基于 683 冻结数据只读生成。

## 按缺陷类型分组

### out_of_bounds（13 条）
- [CVE-2014-0160](CVE-2014-0160.md) · RW-001 · 独苗=asan
- [CVE-2021-3711](CVE-2021-3711.md) · RW-003 · 独苗=asan
- [CVE-2022-3602](CVE-2022-3602.md) · RW-008 · 独苗=asan
- [CVE-2023-6246](CVE-2023-6246.md) · RW-015 · 独苗=asan
- [CVE-2023-38545](CVE-2023-38545.md) · RW-016 · 独苗=asan
- [CVE-2017-1000257](CVE-2017-1000257.md) · RW-020 · 独苗=asan
- [CVE-2017-9047](CVE-2017-9047.md) · RW-032 · 独苗=asan
- [CVE-2018-25032](CVE-2018-25032.md) · RW-034 · 独苗=asan
- [CVE-2016-0718](CVE-2016-0718.md) · RW-045 · 独苗=asan
- [CVE-2020-12284](CVE-2020-12284.md) · RW-049 · 独苗=asan
- [CVE-2023-49502](CVE-2023-49502.md) · RW-051 · 独苗=asan
- [CVE-2019-13750](CVE-2019-13750.md) · RW-062 · 独苗=asan
- [CVE-2023-4911](CVE-2023-4911.md) · RW-012 · 全漏

### data_race（3 条）
- [CVE-2024-6387](CVE-2024-6387.md) · RW-027 · 独苗=tsan
- [CVE-2016-5195](CVE-2016-5195.md) · RW-075 · 独苗=tsan
- [CVE-2016-8655](CVE-2016-8655.md) · RW-090 · 全漏

### integer_overflow（3 条）
- [CVE-2021-30663](CVE-2021-30663.md) · RW-057 · 独苗=cross-compile
- [CVE-2022-35737](CVE-2022-35737.md) · RW-060 · 独苗=ubsan
- [CVE-2021-46143](CVE-2021-46143.md) · RW-096 · 独苗=ubsan

### logic_error（3 条）
- [CVE-2022-0778](CVE-2022-0778.md) · RW-002 · 全漏
- [CVE-2021-41773](CVE-2021-41773.md) · RW-025 · 全漏
- [CVE-2022-0847](CVE-2022-0847.md) · RW-074 · 全漏

### double_free（2 条）
- [CVE-2022-4450](CVE-2022-4450.md) · RW-006 · 独苗=cross-compile
- [CVE-2016-8618](CVE-2016-8618.md) · RW-019 · 独苗=asan

### use_after_free（2 条）
- [CVE-2022-23308](CVE-2022-23308.md) · RW-029 · 独苗=cross-compile
- [CVE-2022-31747](CVE-2022-31747.md) · RW-059 · 独苗=tsan

### memory_leak（1 条）
- [CVE-2023-5868](CVE-2023-5868.md) · RW-064 · 独苗=asan

### type_punning（1 条）
- [CVE-2023-0286](CVE-2023-0286.md) · RW-005 · 全漏

## 一句话摘要（按代表性）

- **CVE-2014-0160** (RW-001, out_of_bounds)：独苗命中(asan)
- **CVE-2021-3711** (RW-003, out_of_bounds)：独苗命中(asan)
- **CVE-2022-4450** (RW-006, double_free)：独苗命中(cross-compile)
- **CVE-2022-3602** (RW-008, out_of_bounds)：独苗命中(asan)
- **CVE-2023-6246** (RW-015, out_of_bounds)：独苗命中(asan)
- **CVE-2023-38545** (RW-016, out_of_bounds)：独苗命中(asan)
- **CVE-2016-8618** (RW-019, double_free)：独苗命中(asan)
- **CVE-2017-1000257** (RW-020, out_of_bounds)：独苗命中(asan)
- **CVE-2024-6387** (RW-027, data_race)：独苗命中(tsan)
- **CVE-2022-23308** (RW-029, use_after_free)：独苗命中(cross-compile)
- **CVE-2017-9047** (RW-032, out_of_bounds)：独苗命中(asan)
- **CVE-2018-25032** (RW-034, out_of_bounds)：独苗命中(asan)
- **CVE-2016-0718** (RW-045, out_of_bounds)：独苗命中(asan)
- **CVE-2020-12284** (RW-049, out_of_bounds)：独苗命中(asan)
- **CVE-2023-49502** (RW-051, out_of_bounds)：独苗命中(asan)
- **CVE-2021-30663** (RW-057, integer_overflow)：独苗命中(cross-compile)
- **CVE-2022-31747** (RW-059, use_after_free)：独苗命中(tsan)
- **CVE-2022-35737** (RW-060, integer_overflow)：独苗命中(ubsan)
- **CVE-2019-13750** (RW-062, out_of_bounds)：独苗命中(asan)
- **CVE-2023-5868** (RW-064, memory_leak)：独苗命中(asan)
- **CVE-2016-5195** (RW-075, data_race)：独苗命中(tsan)
- **CVE-2021-46143** (RW-096, integer_overflow)：独苗命中(ubsan)
- **CVE-2022-0778** (RW-002, logic_error)：8资产全漏
- **CVE-2021-41773** (RW-025, logic_error)：8资产全漏
- **CVE-2022-0847** (RW-074, logic_error)：8资产全漏
- **CVE-2023-0286** (RW-005, type_punning)：8资产全漏
- **CVE-2023-4911** (RW-012, out_of_bounds)：8资产全漏
- **CVE-2016-8655** (RW-090, data_race)：8资产全漏