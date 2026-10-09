# 701 批 — 22 个原始项目缺陷真实编译结果

> 本批在 **WSL Ubuntu（有网络出口）** 实测编译 699 的 22 个项目缺陷。环境：gcc/g++ 13.3、autoconf 2.71、automake、libtool、meson+ninja、cmake。日期 2026-10-09。

## 汇总

- **实测编译成功：14 / 22**
- **编译失败/克隆失败：8 / 22**
- 这修正了 699 的结论：699 记录“WSL 无网络出口、构建未实测”**已过期**——701 实测 WSL 可联网并成功构建了 14 个。

## 构建成功（built:true，14）

| CVE | tag | 说明 |
|-----|-----|------|
| CVE-2019-8457 | version-3.27.2 | configure+make OK |
| CVE-2021-23840 | OpenSSL_1_1_1i | ./config+make OK |
| CVE-2022-2509 | v2.9.14 | autogen+configure+make OK |
| CVE-2022-3602 | openssl-3.0.6 | ./config+make OK |
| CVE-2022-37434 | v1.2.12 | configure+make OK |
| CVE-2022-3786 | openssl-3.0.6 | same build as CVE-2022-3602 |
| CVE-2022-40303 | v2.10.2 | autogen+configure+make OK |
| CVE-2022-4304 | openssl-3.0.7 | ./config+make OK |
| CVE-2023-0286 | openssl-3.0.7 | same build as CVE-2022-4304 |
| CVE-2023-0464 | openssl-3.0.8 | ./config+make OK |
| CVE-2023-28484 | v2.10.3 | autogen+configure+make OK |
| CVE-2023-38545 | curl-8_3_0 | autogen+configure --with-openssl+make OK |
| CVE-2023-4863 | v1.3.1 | autogen+configure+make OK (libwebp 1.3.1) |
| CVE-2024-3094 | v5.6.1 | autogen(autopoint)+configure+make OK |

## 构建失败（built:false / clone_fail，8）

| CVE | tag | 失败原因（诚实记录） |
|-----|-----|------|
| CVE-2014-0160 | OpenSSL_1_0_1f | built_false rc=2 — openssl 1.0.1f (2014年) 在 gcc 13.3/perl 现代工具链下配置/编译失败 |
| CVE-2015-0235 | glibc-2.17 | built_false rc=1 — 要求 autoconf 恰好 2.69，宿主为 2.71 |
| CVE-2016-10190 | n3.2.1 | built_false rc=2 — ffmpeg 3.2.1 (2016年) 在 gcc 13.3 下编译报错 |
| CVE-2016-5195 | v4.8.2 | clone_fail — linux 标签引用解析/超大仓库克隆；完整内核构建超出本批预算 |
| CVE-2018-1000001 | glibc-2.26 | built_false rc=1 — 要求 autoconf 恰好 2.69，宿主为 2.71 |
| CVE-2020-13777 | 3.6.13 | built_false rc=127 — ./bootstrap 工具链链不完整（autogen/autopoint 链） |
| CVE-2021-4034 | 0.119 | built_false rc=1 — meson 缺运行期依赖 mozjs-78 |
| CVE-2022-23219 | glibc-2.34 | clone_fail — sourceware.org 返回 HTTP 429 限流；且 glibc 要求恰好 autoconf 2.69 |

## 结构性发现（有价值）

现代标准工具链（gcc 13.3 + autoconf 2.71）能构建 **2016 年之后且不依赖旧 autoconf/旧 JS 引擎** 的项目（zlib/sqlite/xz/curl/libxml2/libwebp/openssl 1.1.1i 与 3.0.x）；
**构建失败集中在两类**：
1. **远古低层项目**：glibc 2.17/2.26/2.34 要求 autoconf **恰好 2.69**（宿主 2.71）；openssl 1.0.1f(2014)、ffmpeg 3.2.1(2016) 与 gcc 13.3 不兼容。这是“旧源码 × 现代编译器”的**真实可复现壁垒**，不是脚本缺陷。
2. **外部与依赖约束**：sourceware.org 对 glibc 克隆返回 HTTP 429；polkit 0.119 需 mozjs-78 运行期依赖；linux 4.8.2 标签解析/超大仓库克隆。

## 复现命令（片段）

```bash
# WSL Ubuntu
sudo apt-get install -y build-essential autoconf automake libtool autoconf-archive \
  pkg-config bison flex python3-dev gettext autopoint autogen intltool libssl-dev ninja-build meson cmake
# 单项目:  bash data/raw_external/original_projects/<CVE>/clone_build.sh
# 全量:    bash data/raw_external/original_projects/build_all.sh
```

## 诚实边界

- 失败项目**未使用任何变通**（如自装 autoconf 2.69/旧 GCC）去“刷绿”——保留原样失败即真实结论。
- 新增 18 个缺陷**未实测编译**（仅提供脚本），故案例库“可构建”总数应记 **40 个已提供构建脚本、其中 14 个经 701 实测通过**。
