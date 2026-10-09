# 701 批 — 新增原始项目缺陷（第二批，18 个）

> 在 699 的 22 个之上再收集 18 个真实 C/C++ 项目缺陷，凑足 40 个案例库。全部为公开 CVE，附构建命令与触发条件。

## 清单

| id | CVE | 项目 | family | type | 严重度 | 修复版本 | 构建 |
|----|-----|------|--------|------|--------|----------|------|
| NPD-001 | CVE-2021-3156 | sudo | memory-safety | heap-buffer-overflow | High | 1.9.5p2 | script-provided |
| NPD-002 | CVE-2014-6271 | GNU Bash | logic | env-var-function-def-injection (RCE) | Critical | 4.3 (patch) | script-provided |
| NPD-003 | CVE-2023-44487 | nghttp2 | logic | DoS (HTTP/2 Rapid Reset, missing stream limit) | High | 1.57.0 | script-provided |
| NPD-004 | CVE-2022-0543 | Redis | logic | Lua sandbox escape (packaging-dependent) | High | 7.0.11 | script-provided |
| NPD-005 | CVE-2017-7529 | nginx | ub | integer-overflow (range filter) | High | 1.13.3 / 1.12.1 | script-provided |
| NPD-006 | CVE-2019-11043 | PHP (php-fpm) | memory-safety | buffer-underflow/overflow (env_path_info) | Critical | 7.1.33/7.2.24/7.3.11 | script-provided |
| NPD-007 | CVE-2024-6387 | OpenSSH (sshd) | concurrency | signal-handler race (regreSSHion) | High | 9.8p1 | script-provided |
| NPD-008 | CVE-2021-38001 | V8 (Chrome) | ub | type-confusion (inline cache) | High | Chrome 95.0.4638.69 | script-provided |
| NPD-009 | CVE-2016-8655 | Linux kernel | memory-safety | heap-buffer-overflow (packet_set_ring) | High | 4.8.12 | script-provided |
| NPD-010 | CVE-2017-1000367 | sudo | memory-safety | heap-buffer-overflow (getopt) | High | 1.8.20p2 | script-provided |
| NPD-011 | CVE-2022-42898 | MIT Kerberos 5 (krb5) | ub | integer-overflow (PAC parsing) | High | 1.19.4 / 1.20.1 | script-provided |
| NPD-012 | CVE-2020-10735 | CPython | logic | algorithmic-complexity DoS (int<->str) | Medium | 3.7.15+ | script-provided |
| NPD-013 | CVE-2021-35937 | rpm | concurrency | race-condition (signature check bypass) | High | 4.18.0 | script-provided |
| NPD-014 | CVE-2017-15277 | ImageMagick | memory-safety | uninitialized-memory-leak (GIF encoder) | High | 7.0.7-29+ | script-provided |
| NPD-015 | CVE-2022-38784 | poppler | ub | integer-overflow (JBIG2 decoder) | High | 22.09.0 | script-provided |
| NPD-016 | CVE-2019-7310 | libpng | memory-safety | use-after-free (png_image_free) | Critical | 1.6.37 | script-provided |
| NPD-017 | CVE-2021-44790 | Apache HTTP Server (httpd) | memory-safety | buffer-overflow (mod_lua parsebody) | High | 2.4.52 | script-provided |
| NPD-018 | CVE-2022-0847 | Linux kernel (Dirty Pipe) | memory-safety | page-cache-corruption (PIPE_BUF_FLAG_CAN_MERGE) | High | 5.16.11 / 5.15.25 / 5.10.102 | script-provided |

## provenance（诚实）

- **修复 commit**：本批新增 18 个均以**官方公告/安全跟踪器 URL** 引用，未逐一核实完整 SHA（verified=false）。与 699 中 5 个 verified=true 不同。
- **CVSS**：全部标 `nvd-reported`，发表前须用 NVD 2.0 API 复核。
- **构建**：18 个均 `script-provided-not-executed`（本批把实测预算用在 699 的 22 个上）。其中 redis/nginx/sudo/libpng/krb5/nghttp2/python 等为标准 autotools/Makefile，可行性高。
