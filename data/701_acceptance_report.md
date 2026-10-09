# 701 批 — 验收报告

- **批次：** 701（承接 699，真实编译 + 新增案例 + 统一案例库）
- **日期：** 2026-10-09
- **仓库：** C:\CodeLearnling\note\note\C++\CPP-Bible
- **提交：** DCO 2–3 次（unpushed），仅 `data/701_*` 与 `data/raw_external/`

---

## 0. 一句话结论

**699 的结论“WSL 无网络出口、构建未实测”在 701 被实测推翻。** 本批在 WSL Ubuntu（gcc/g++ 13.3）**真实克隆并编译了 699 的 22 个项目缺陷**：**14 个编译成功、8 个失败**（失败均有可复现的真实原因，未做任何“刷绿”变通）；并新增 **18 个**真实 C/C++ 缺陷，案例库统一为 **40 个**（含 `index.json` 与一键 `build_all.sh`）。

---

## 1. Task A — 22 个原始项目缺陷真实编译

**环境（关键前提）**：699 记录 WSL 无出口；701 实测 **WSL 可联网**（`git ls-remote`/`curl` 均成功）。据此在 WSL 中真实 clone + checkout + build。

**结果：14 built_true / 8 built_false（或 clone_fail）**

- **成功（14）**：libwebp 1.3.1、curl 8.3.0、zlib 1.2.12、sqlite 3.27.2、xz 5.6.1、libxml2 2.9.14/2.10.2/2.10.3、openssl 1.1.1i/3.0.6/3.0.7/3.0.8（openssl 多 tag 覆盖 6 个 CVE）。
- **失败（8）**：
  - glibc 2.17/2.26/2.34 — 要求 **autoconf 恰好 2.69**（宿主 2.71）；且 sourceware.org 返回 **HTTP 429**。
  - openssl 1.0.1f(2014)、ffmpeg 3.2.1(2016) — **旧源码 × gcc 13.3 不兼容**。
  - polkit 0.119 — 缺运行期依赖 **mozjs-78**。
  - gnutls 3.6.13 — bootstrap 工具链链不完整。
  - linux 4.8.2 — 标签解析/超大仓库克隆 + 完整内核构建超预算。

**产物**：`data/701_build_results.md`；22 个 `original_projects/<CVE>/README.md` 的 `Build status` 字段已回填真实结果，`clone_build.sh` 追加 701 result。

**结构性发现（有价值，非缺陷）**：现代标准工具链能构建 2016 年之后的项目；失败集中在「远古低层项目（旧 autoconf/旧编译器）」与「外部限流/重依赖」两类——这是真实可复现的壁垒。

---

## 2. Task B — 新增 15–20 个真实项目缺陷

**交付：18 个**（`data/701_new_project_defects.json` + `.md`）。

- 覆盖：sudo×2、Bash、nghttp2、Redis、nginx、PHP-FPM、OpenSSH、V8/Chrome、Linux kernel×2、krb5、CPython、rpm、ImageMagick、poppler、libpng、Apache httpd。
- 家族分布：memory-safety 8 / ub 4 / logic 4 / concurrency 2。
- 每条含：CVE、repo、affected/fixed 版本、严重度、family/type/CWE、fixing commit 引用、files、build_command、trigger。

**诚实边界**：新增 18 个的 fixing commit **均以公告 URL 引用（verified=false）**，未逐一核对完整 SHA；CVSS 全标 `nvd-reported`（发表前须 NVD 2.0 API 复核）；**未实测编译**（本批实测预算用于 699 的 22 个）。

---

## 3. Task C — 统一可构建案例库

- `data/raw_external/index.json` — **40 个案例**统一索引（batch 699=22 / 701=18；built_true=14 / built_false=8；按 family 统计）。
- `data/raw_external/original_projects/build_all.sh` — 一键遍历全部 40 个 `clone_build.sh`，输出 `summary.tsv`。
- 18 个新目录：`original_projects/<CVE>/README.md` + `clone_build.sh`（与 699 同构）。
- `data/raw_external/README.md` 增补 701 更新段并修正“构建未实测”的过期声明。

---

## 4. Task D — 提交

- DCO 签名，身份用命令行覆盖：`git -c user.name="LiaoRanran" -c user.email="1026708211@qq.com" commit -s`。
- **仅 add 显式路径**：`data/701_*`、`data/raw_external/`。**不 push**。

---

## 5. 诚实边界与遗留

| 项 | 状态 |
|----|------|
| 22 个实测编译 | ✅ 14 built_true / 8 built_false（真实执行） |
| 失败项目是否“刷绿” | ❌ 未做（未自装 autoconf 2.69/旧 GCC 强行通过） |
| 新增 18 个实测编译 | ⬜ 未做（仅提供脚本） |
| 新增 18 个 fixing commit | ⚠️ verified=false（公告 URL 引用） |
| CVSS | ⚠️ nvd-reported，待 NVD API 复核 |
| 案例库“可构建”口径 | 40 个已提供构建脚本，其中 **14 个经实测通过** |

**遗留/待办**：
1. 在已装 **autoconf 2.69** 或旧 GCC 的容器中补测 glibc/openssl-1.0.1f/ffmpeg 3.2，据实回填。
2. 新增 18 个的 fixing commit 用 GitHub API/commit 页解析完整 SHA 并升级 verified。
3. 用 NVD 2.0 API 复核全部 CVSS。
4. 在干净 Linux 上跑 `build_all.sh` 得到 40 项的统一实测基线。

---

## 6. 红线遵守

- ✅ 未运行任何 `detect()`；未修改检测器/样本/冻结矩阵。
- ✅ 未触碰 research/latex/、queyi_refs.bib。
- ✅ 提交仅限 `data/701_*` 与 `data/raw_external/`；显式路径 add；DCO；不 push。
