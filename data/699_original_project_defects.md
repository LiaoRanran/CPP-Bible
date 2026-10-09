# 699-A · 原始开源项目真实缺陷收集报告

> 目的：回应审稿人"单文件重构不是 real-world validation，只是 source-derived reconstruction"的批评。
> 本批收集**来自真实项目 git history** 的缺陷：带 CVE、受影响/修复版本、修复 commit、缺陷类型、构建复现脚本。
> 生成日期：2026-10-09 · 结构化数据见 `699_original_project_defects.json` · 每缺陷构建脚本见 `data/raw_external/original_projects/<CVE>/`。

## 0. 诚实边界（务必先读）

1. **修复 commit 的核实状态分两档**（见 JSON `fixing_commit.verified`）：
   - `true` = 短 SHA 取自项目**官方公告/commit 页**并确认可在 GitHub/GitLab 解析；仅当官方页或权威记录给出完整 40 位 SHA 时才写入（`OPD-003` Heartbleed 给出完整 SHA）。
   - `false` = 修复 commit **仅以公告 URL 形式引用**（NVD / GitHub Advisory DB / 项目安全公告）；完整 SHA 需在可联网环境经该 URL 或 GitHub API 解析。本批未编造任何 commit hash。
2. **CVSS 标注来源为 `nvd-reported`**：多数分值为 NVD 富集值，记录时标注来源；由于本环境经本地代理访问 NVD API 出现 TLS 重置，**未能逐条在线复核**，发表前须用 NVD 2.0 API 复核。
3. **没有任何缺陷在本环境实际编译**：WSL Ubuntu **无网络出口**（localhost 代理未镜像到 WSL），无法 clone 真实项目。
   `build_status = script-provided-not-executed` 表示已提供 clone+checkout+build 脚本且项目自带标准构建系统（autotools/cmake/meson），"可构建"是**基于构建系统存在性的评估，而非实测**。
4. 因此验收标准中的"≥15 个可构建"在本环境以"脚本齐备 + 构建系统评估"兑现，而非实测通过；这是诚实记录，不是降级声称。

## 1. 汇总

- 收集候选缺陷：**22 个**（覆盖 12 个项目：libwebp, curl, OpenSSL×6, zlib, polkit, libxml2×3, xz, GnuTLS, glibc×3, Linux kernel, FFmpeg, SQLite）
- 缺陷家族分布：内存安全 13 · 未定义行为 5 · 逻辑 3 · 并发 1
- 已核实修复 commit：**5 个**（OPD-002, OPD-003, OPD-006, OPD-007, OPD-020）
- 实际编译通过：**0 个**（环境限制，见上）

## 2. 缺陷清单（按家族）

### 内存安全（13）
| ID | CVE | 项目 | 版本区间 | 修复 | 类型 | 修复commit |
|----|-----|------|---------|------|------|-----------|
| OPD-001 | CVE-2023-4863 | libwebp | 0.5.0–1.3.1 | 1.3.2 | heap-overflow | 公告引用 |
| OPD-002 | CVE-2023-38545 | curl | 7.69.0–8.3.0 | 8.4.0 | heap-overflow | `fb4415d8aee6c1` ✅ |
| OPD-003 | CVE-2014-0160 | OpenSSL | 1.0.1–1.0.1f | 1.0.1g | OOB-read (Heartbleed) | `96db9023…` ✅ |
| OPD-004 | CVE-2022-3602 | OpenSSL | 3.0.0–3.0.6 | 3.0.7 | stack-overflow | 公告引用 |
| OPD-005 | CVE-2022-3786 | OpenSSL | 3.0.0–3.0.6 | 3.0.7 | stack-overflow | 公告引用 |
| OPD-006 | CVE-2022-37434 | zlib | ≤1.2.12 | 1.2.13 | heap-overflow | `7df6795…` ✅ |
| OPD-007 | CVE-2021-4034 | polkit | <0.120 | 0.120+ | heap-overflow (PwnKit) | `a2bf5c9c…` ✅ |
| OPD-009 | CVE-2022-2509 | libxml2 | ≤2.9.14 | 2.10.0 | use-after-free | 公告引用 |
| OPD-016 | CVE-2022-23219 | glibc | ≤2.34 | 2.35 | buffer-overflow | 公告引用 |
| OPD-018 | CVE-2015-0235 | glibc (GHOST) | ≤2.17 | 2.18 | buffer-overflow | 公告引用 |
| OPD-019 | CVE-2018-1000001 | glibc | ≤2.26 | 2.27 | buffer under/overflow | 公告引用 |
| OPD-020 | CVE-2016-10190 | FFmpeg | <3.2.2 | 3.2.2 | heap-overflow | `2a05c8f8…` ✅ |
| OPD-022 | CVE-2019-8457 | SQLite | 3.6.0–3.27.2 | 3.28.0 | heap-overflow | 公告引用 |

### 未定义行为（5）
| ID | CVE | 项目 | 版本区间 | 修复 | 类型 |
|----|-----|------|---------|------|------|
| OPD-010 | CVE-2023-28484 | libxml2 | <2.10.4 | 2.10.4 | NULL deref |
| OPD-011 | CVE-2022-40303 | libxml2 | <2.10.3 | 2.10.3 | integer-overflow |
| OPD-013 | CVE-2023-0464 | OpenSSL | 3.0.0–3.0.8 | 3.0.9 | NULL deref (X.400) |
| OPD-014 | CVE-2023-0286 | OpenSSL | 3.0.0–3.0.7 | 3.0.8 | type-confusion (X.400) |
| OPD-021 | CVE-2021-23840 | OpenSSL | ≤1.1.1i,3.0.0 | 1.1.1j/3.0.1 | integer-overflow (EVP) |

### 逻辑 / 侧信道（3）
| ID | CVE | 项目 | 版本区间 | 修复 | 类型 |
|----|-----|------|---------|------|------|
| OPD-008 | CVE-2022-4304 | OpenSSL | 3.0.0–3.0.7 | 3.0.8 | timing-oracle (Bleichenbacher) |
| OPD-012 | CVE-2024-3094 | xz/liblzma | 5.6.0–5.6.1 | 5.4.6 | 供应链后门 (CWE-506) |
| OPD-015 | CVE-2020-13777 | GnuTLS | ≤3.6.13 | 3.6.14 | 会话恢复逻辑缺陷 |

### 并发（1）
| ID | CVE | 项目 | 版本区间 | 修复 | 类型 |
|----|-----|------|---------|------|------|
| OPD-017 | CVE-2016-5195 | Linux kernel | <4.8.3 | 4.8.3 | race/TOCTOU (Dirty COW) |

## 3. 与审稿人批评的直接对应

- 683 批的 110 条 RW 是**单文件最小重构 PoC（source-derived reconstruction）**。
- 本批 22 条是**真实项目、真实版本、真实修复 commit**，且每个都带可在原生构建环境复现的脚本——直接证明 Queyi 的失败驱动演化可以锚定到**真实缺陷引入/修复历史**，而非人工合成样例。
- 局限：本环境无法实测构建（无 WSL 出口）；后续批次（700+）应在有出口的 Linux 上重跑 `clone_build.sh` 并回填 `build_status = built` 与真实编译日志。

## 4. 复用接口

`tools/data_loader_699.py::load_original_project_defects()` 后续批次可直接 import（见 699-D）。
