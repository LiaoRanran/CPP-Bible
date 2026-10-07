# Real-World C++ Defect Benchmark (Queyi, 683)

> 110 条真实系统缺陷的最小重构靶场：用于测"检测器组合在真实缺陷类别上的能力"。
> 生成批次：683（2026-10-07）｜许可：Apache-2.0｜机器可读元数据：
> `data/683_real_world_benchmark.json`

## 1. 这是什么

每条样本（`RW-001.cpp` … `RW-110.cpp`）是一个**单文件、可编译的最小重构**：
复现某个真实披露缺陷的**机制**（不是原始项目代码，也不是武器化利用链）。
样本头部注释内嵌全部元数据（**单一事实源**，JSON 由脚本从头部注释 + NVD 记录合成）：

```cpp
// RW-001 | CVE-2014-0160 | OpenSSL | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2014-0160
// project_url: https://www.openssl.org/
// year: 2014 | severity: HIGH | source_type: cve
// mechanism: Heartbleed —— ...
// notes: 最小重构（source-derived，非原始项目代码）。ASan 应报 heap-buffer-overflow read。
```

## 2. 统计（生成时）

| 维度 | 值 |
|---|---|
| 样本数 | 110 |
| 项目覆盖 | 30+（OpenSSL / glibc / curl / nginx / Apache httpd / OpenSSH / libxml2 / zlib / libpng / libwebp / FreeType / libtiff / expat / ImageMagick / FFmpeg / Chromium-V8 / WebKit / Firefox / SQLite / PostgreSQL / Redis / protobuf / Boost / Qt / Godot / Linux kernel / sudo / polkit / FreeBSD / ncurses / CUPS / XZ Utils …） |
| 缺陷类型 | 34 类规范词表子集（out_of_bounds / use_after_free / double_free / null_pointer_deref / integer_overflow / type_punning / data_race / logic_error / memory_leak / other_ub …） |
| 年份跨度 | NVD 首次发布年（含 2012–2024） |
| CVE 在线验证 | 109 个唯一 CVE，全部经 NVD API v2.0 查询确认（应答原文冻结） |
| 出处链接 | 51 条 fix-commit / 18 条 issue / 16 条 PR（NVD references 提取） |
| 检测矩阵 | 110 × 8 资产（`data/683_real_world_detection_matrix.json`） |

## 3. 怎么用

```bash
# 直接编译运行一条（以 asan 为例）
g++ -std=c++17 -O0 -g -fsanitize=address -pthread RW-001.cpp -o rw001 && ./rw001

# 全量重跑 8 资产检测（需 WSL g++ + MinGW；增量 checkpoint）
python data/realworld_683_runner.py --stage detect
python data/realworld_683_runner.py --stage merge

# 深度分析（检出率/类型矩阵/失败与成功案例）
python tools/analyze_683_realworld.py
```

运行注意：`RW-002`（CVE-2022-0778 重构）会**无限循环**——请用 `timeout 10 ./rw002`；
挂起类样本在检测矩阵中的观测口径为"超时 → miss"（如实登记）。

## 4. 许可与出处

- 本目录 PoC 文本：Apache-2.0（同仓库）。**每条样本标注原始出处 URL**；
  重构保留对上游项目公开披露的引用。
- CVE 描述/CVSS/时间：NVD 公共领域数据（API 应答原文冻结于
  `data/683_real_world_candidates_verified.json`）。
- 不含任何个人数据、密钥或可运行的真实攻击载荷（仅缺陷最小复现）。

## 5. 诚实边界（引用时请一并引用）

1. **source-derived 重构**：不等价于原始项目上下文（跨模块依赖、构建系统复杂度未复现）。
2. 部分样本依赖特定环境才能触发（如内核类用户态复刻、竞态类需要压力重现），
   逐条在 `notes` 与检测矩阵 `per_asset.note` 中登记。
3. 检出率数字的口径（unknown 不进分母、双档 -O0/-O2 等）与主实验一致，见
   `data/683_real_world_analysis.md`。
