# Release Notes — Queyi (阙疑) research line v1.0.0

Release date: **2026-10-07** · License: **Apache-2.0** · Tag: `v1.0.0`

本发布把"行远/论文线"的最后一个大幅批次（**683 · 究极收尾轮**）合并入仓：
真实靶场基准、跨工具链验证、operator 全枚举消融、研究报告官网与开源发布材料。

> 边界声明：`v1.0.0` 是**研究仓库快照**，不是"完备的产品"。
> 论文为投稿准备中（NeurIPS 2027 E&D 目标）；一切未闭合项在验收报告中如实登记。

---

## 一、数据集（新增/冻结）

| 资产 | 规模 | 文件 |
|---|---|---|
| 真实靶场 PoC（重构） | **110** 条（RW-001…RW-110） | `data/real_world/RW-*.cpp` |
| 真实靶场元数据 | 110 条（含 NVD 原文、CVSS、references） | `data/683_real_world_benchmark.json` |
| 真实靶场判定矩阵 | **110 × 8 = 880 格**（真实检测） | `data/683_real_world_detection_matrix.json` |
| CVE 在线验证记录 | **109/109 FOUND**（NVD API v2.0 应答原文冻结） | `data/683_real_world_candidates_verified.json` |
| 合成语料判定矩阵（沿用） | 1147 × 8 | `data/blindspot_676g_detection_matrix.json` |
| Croissant core + RAI（沿用） | 通过官方 mlcroissant 校验 | `data/croissant.json` |

真实靶场覆盖：**≥15 个项目**（OpenSSL / glibc / curl / nginx / Apache httpd / OpenSSH /
libxml2 / zlib / libpng / libwebp / FreeType / libtiff / expat / ImageMagick / FFmpeg /
Chromium-V8 / WebKit / Firefox / SQLite / PostgreSQL / Redis / protobuf / Boost / Qt /
Godot / Linux kernel / sudo / polkit / FreeBSD …），**≥10 类缺陷**（越界 / UAF / double-free /
空指针 / 整数溢出 / 类型混淆 / 数据竞争 / 逻辑绕过 / 内存泄露 / 无限循环 …）。

## 二、实验（683 新增）

- **A5 真实靶场检测**：110 样本 × 8 资产全量实测（WSL g++ 13.3 双档 + MinGW 本地资产），
  OR 检出率、逐资产排名、类型/项目/严重度/年份切片、失败与成功案例深读。
- **跨工具链（B）**：WSL clang++ 18.1.3 vs WSL g++ 13.3（asan/ubsan，n=200 分层抽样），
  一致率与 Cohen's κ；跨平台（Windows 原生 vs WSL）并发样本行为对比；
  MinGW clang 22 的 ASan 不可用已登记。
- **Operator 全枚举消融（C）**：2^4 = **16 配置**（+16 个 unique 模式配置，共 32 配置行）；
  7 基线（Random/Static/FD/Frequency/Greedy/Oracle/InfoGain）统一口径；
  数学结论验证：`fd_only ≡ set-cover greedy`（14/14 块）、`literal novel ≡ failure`
  （2f 权重平移等价，14/14 块）、unique 变体在 11/14 块改变选择。
- **官网与图表（D）**：`docs/` 8 页静态站（含真实靶场浏览器与交互 Demo）+ 8 张 ECharts 图。

## 三、论文

- 正文章节与全部既有数字**未改动**；683 以附录增量并入：
  `Real-World Validation`、`Toolchain Sensitivity`、`Operator Ablation (All 16 Configurations)`。
- 论文数字对账门禁：`tools/verify_paper_numbers.py`（发布工作流 fail-closed 依赖）。

## 四、工程与开源

- 新增：`CITATION.cff`、`RELEASE_NOTES_v1.0.md`、`README_RESEARCH.md`、
  `docker-compose.yml`、`docker/queyi/Dockerfile`、`research/pyproject.toml`、
  `.github/workflows/release.yml`、`.github/workflows/pages.yml`、`.github/dependabot.yml`。
- 既有：LICENSE（Apache-2.0）、CONTRIBUTING、CODE_OF_CONDUCT、SECURITY、PR/ISSUE 模板、
  ci.yml / dco.yml / deploy.yml。
- **未包含任何密钥、令牌或个人隐私数据**（683 红线 9；作者实名仅见于 CITATION/论文元数据）。

## 五、复现（最小路径）

```bash
# 纯 Python 数据链（无需编译器 / WSL / Docker）
python tools/verify_paper_numbers.py
python tools/analyze_683_oc.py --stage all
python tools/site_683_data.py

# 真实检测全链（需要 WSL g++ 13.3 + MinGW g++ 13.1 + clang）
python tools/collect_realworld_683.py --stage verify   # 需要网络（NVD API）
python data/realworld_683_runner.py --stage detect
python tools/cross_toolchain_683.py --stage b1
```

## 六、已知限制（诚实清单）

1. 真实靶场 PoC 为 **source-derived 重构**（最小复现），非原始项目上下文；
2. `wunsequenced` / `compile-time` 两资产在本工具链下**恒 unknown**（工具链事实，已冻结口径）；
3. 本机**无 Docker / 无 MSVC**：`docker-compose.yml` 通过 YAML 校验但未实测构建；MSVC 对照缺失；
4. 人类第三方 IAA 仍为 0 人（AI 二标 κ=0.73 不能替代）；
5. 部分真实样本为挂起/超时类（检测器以超时→miss 处理，逐条登记）。

## 七、校验和

发布产物（论文 PDF + 数据集 JSON + `real_world/`）由 `release.yml` 在打 tag 时
自动生成 `SHA256SUMS.txt` 一并挂出；本地可复算：
`python tools/gen_683_realworld_benchmark.py`（PoC 逐文件 SHA-256 内嵌于 benchmark JSON）。
