# 复现指南（supplementary/REPRODUCTION.md）

> 论文：`queyi_neurips2027_v1.1.tex` ｜ 仓库：`github.com/LiaoRanran/CPP-Bible`
> 本指南从零讲清：装什么、clone 什么、build 什么、run 什么、每个实验预期多久 / 什么资源 / 什么输出。
> 对应批次：704-B。配套脚本：`docker/minimal_repro.sh`、`supplementary/environment.yml`。

---

## 0. 先读诚实边界（哪些能复现、哪些不能）

| 类别 | 能否在容器内复现 | 说明 |
|---|---|---|
| **数字对账 / 口径重算**（检出率、CI、p 值、样本量、系统计数） | ✅ 纯 Python，只读冻结产物 | `verify_paper_numbers.py`、`recompute_a5_676f.py` 等，无需编译器 |
| **论文编译**（tectonic 出 PDF） | ✅ 需 tectonic | `docker/paper` 镜像提供 |
| **真实检测链**（asan/ubsan/tsan 需 WSL g++ 13.3；compiler-warn 需 MinGW g++ 13.1） | ⚠️ **仅宿主机**（Windows + WSL） | 容器内 Linux 工具链与论文口径存在已知环境差异，详见 §6 |
| **Examples/*.asm**（书稿汇编证据） | ❌ 需 Windows MinGW GCC 15.3.0 | 由本地生成，不进复现链 |

> ⚠️ **本仓库所有 `Dockerfile` / `docker-compose.yml` 截至 704 批次均未经 `docker build` 实测**
> （作者执行环境 Windows 11 未安装 Docker）。它们通过 YAML 语法 / 路径 / 包名存在性核验，
> 但**没有构建的实际证据**。首次构建前请按 §3 的 digest / 版本提示核对基础镜像。

---

## 1. 前置依赖（宿主机）

| 工具 | 版本 | 用途 | 必须？ |
|---|---|---|---|
| git | 任意新版 | clone / 拉取冻结产物 | 必须 |
| Python | **3.13.x** | 数字重算、门禁、文档 | 必须（数据链） |
| Docker | 24+ | 容器复现 | 可选（无 Docker 走 §4 本地复现） |
| tectonic | 0.17.x | 论文 PDF 编译 | 可选（仅编译需要） |
| WSL2 + g++ 13.3 / MinGW g++ 13.1 / clang 17+ | — | 真实检测链端到端重跑 | 可选（仅全链需要） |

Python 依赖：论文数字重算**只用标准库**；门禁 / 文档站额外依赖见 `requirements.txt`（钉版本，全量 freeze）。最小集合只需 `pyyaml`。

---

## 2. Clone

```bash
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible
git checkout -b repro # 可选：在干净分支上复现
```

冻结产物（检测矩阵、stats JSON、a5 矩阵 jsonl 等）**已随仓库提交**，无需外部下载。

---

## 3. 三种复现方式

### 方式 A · 最小复现（无需 Docker，~1 分钟，3 个核心实验）

```bash
PY=python3 bash docker/minimal_repro.sh
```
- 只读冻结产物，**不跑任何检测器**；输出 `PASS/FAIL`。
- 复现：① A5 主端点 +24.03pp（FD 309/566 vs Random 173/566）；② 环境画像 60.07%→24.74%（Δ−35.34pp）；③ 真实 CVE 59.09%（65/110）。

### 方式 B · 数据链 + 论文编译（Docker，推荐审稿人用）

```bash
# 数据链口径对账（python:3.12-slim 镜像，纯 Python）
docker compose build queyi
docker compose run --rm queyi python tools/verify_paper_numbers.py

# 论文编译（ubuntu 24.04 + g++-13 + python3.13 + tectonic）
docker compose build paper
docker compose run --rm paper        # 编译 PDF 到 research/latex/
```
- compose 文件见仓库根 `docker-compose.yml`（服务：`queyi` / `paper`）。

### 方式 C · 全链复现（Docker，多阶段，UNTESTED build）

```bash
docker compose -f docker/reproduce/docker-compose.yml build
docker compose -f docker/reproduce/docker-compose.yml run --rm reproduce
# 或只做环境体检：
docker compose -f docker/reproduce/docker-compose.yml run --rm verify-env
```
- 镜像 `docker/reproduce/Dockerfile`（ubuntu:22.04 多阶段，gcc-12 / clang-14 / cppcheck / valgrind）。
- 入口 `Scripts/reproduce_all.sh`。**未实测构建**（见 §0 警告）。
- 容器内默认跳过 `-Wunsequenced` 资产（`QUEYI_SKIP_WUNSEQUENCED=1`），因容器内 clang-14 认该选项、论文口径（MinGW）不认，结果不可比。

---

## 4. 无 Docker 的本地复现（等价于方式 B 的数据链部分）

```bash
# ① 数字对账（fail-closed）
python tools/verify_paper_numbers.py \
  --out-json data/704_verify_paper_numbers.json \
  --out-md  data/704_verify_paper_numbers_report.md

# ② A5 / 盲区从冻结矩阵独立重算
python tools/recompute_a5_676f.py            # 写 data/676h_a5_recompute.json

# ③ 系统计数 / 种子审计 / 676m 修复校验（见 docker/paper/run_all.sh 的编排）
python tools/data_integrity_676h.py
python tools/seed_audit_676h.py --out-json out/s.json --out-md out/s.md
python tools/fix_676m_schema.py --verify

# ④ 论文编译（需 tectonic）
cd research/latex && tectonic -X compile queyi_neurips2027_v1.1.tex
```

---

## 5. 每个实验：预计时间 / 资源 / 预期输出

| 实验 | 命令 | 预计时间 | 资源 | 预期输出（节选） |
|---|---|---|---|---|
| 数字对账（全稿） | `verify_paper_numbers.py` | 1–3 min | 纯 CPU / 标准库 | 检察 130、missing 0、consistent 116、692 自洽 35/35、退出码 0 |
| A5 + 盲区重算 | `recompute_a5_676f.py` | <30 s | 纯 CPU | FD 309/566、Random 173/566、盲区 440/1147=38.4%、R1–R7 全 OK |
| 最小复现（3 实验） | `docker/minimal_repro.sh` | <1 min | 纯 CPU | PASS=3 FAIL=0 |
| 数据完整性 | `data_integrity_676h.py` | <10 s | 纯 CPU | n=1147 三数一致、sha256 missing 0 |
| 种子审计 | `seed_audit_676h.py` | <30 s | 纯 CPU | 未固定种子实验类脚本数 = 0 |
| 论文编译 | `tectonic ...` | 1–2 min | 纯 CPU | 0 编译错、正文 ≤9 页 |
| 真实检测链（全 8 资产） | `data/real_world_683_runner.py --stage detect` | 数小时 | WSL g++ 13.3 + MinGW + clang | 110×8 判定矩阵（需宿主机，非容器） |

---

## 6. 已知不可在容器内等价复现的部分（诚实边界，必须随结论一起声明）

1. **holdout / corpus 头版检出率**依赖 WSL(Ubuntu 24.04) + g++ 13.3 + setarch + ASan/UBSan/TSan 运行时；MinGW 无 UBSan 运行时。容器内 Linux g++ 理论口径一致但环境不同，结果**不等价**，只可用于口径理解，不得翻/改结论。
2. **E9 的 clang-tidy** 论文用 LLVM 22.1.8（Windows 原生），cppcheck 2.13.0（WSL）；容器 Ubuntu 24.04 的 clang-tidy 为 LLVM 18，版本不一致 ⇒ E9 数字不可由容器复核。
3. **Windows-native（MinGW g++ 13.1 / clang 22.1.8）** 一支：容器内是 Linux 工具链，环境画像 `windows-native-mingw` 只能在 Windows 宿主机取。
4. **Examples/*.asm** 由 Windows MinGW GCC 15.3.0 生成（Intel 语法 / Win64 ABI），容器内 Linux GCC 产物为 AT&T 语法 / Linux ABI，不可互替。
5. **人类 IAA 标注**截至 703 仍为 `pending`（0 条裁决填入）——不是复现问题，是数据采集未执行。

---

## 7. 复现验证清单（提交前自检）

- [ ] `docker/minimal_repro.sh` 输出 `PASS=3 FAIL=0`
- [ ] `verify_paper_numbers.py` 退出码 0（missing 0）
- [ ] `recompute_a5_676f.py` 输出 R1–R7 全 OK
- [ ] `data_integrity_676h.py` 三数一致
- [ ] 论文 `tectonic` 编译 0 错、正文 ≤9 页
- [ ] 已向审稿人声明 §6 的不可容器化部分

---

## 8. 参考文件

- `docker/minimal_repro.sh` — 本批最小复现脚本
- `docker/paper/Dockerfile` + `docker/paper/run_all.sh` — 论文数字一键复算镜像
- `docker/queyi/Dockerfile` — 数据链镜像（python:3.12-slim）
- `docker/reproduce/Dockerfile` + `docker/reproduce/docker-compose.yml` — 全链镜像（UNTESTED）
- 仓库根 `Dockerfile`（gcc:15.3.0 书稿汇编证据镜像）、`docker-compose.yml`（queyi/paper 服务）
- `supplementary/environment.yml` — 依赖清单
- `supplementary/scripts_index.md` — 复现关键脚本输入/输出/运行方式
