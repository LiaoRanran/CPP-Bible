# 704-B · Docker 复现环境准备 · 执行报告

**批次**：704 · **任务**：B — Docker 复现环境准备
**红线遵守**：本任务**只写配置与文档**（`supplementary/REPRODUCTION.md`、`supplementary/environment.yml`、`docker/minimal_repro.sh`、`data/704_*`），**未实际 `docker build`**（本机 Windows 11 无 Docker，且 704 红线也禁止构建）。未修改既有 `Dockerfile` / `docker-compose.yml`（发现问题只给改进建议，见 §4）。

## 1. 现有 Docker 配置盘点

| 文件 | 作用 | 完整性 | 实测？ |
|---|---|---|---|
| 根 `Dockerfile` | 书稿汇编证据镜像（gcc:15.3.0，**钉 digest**） | 完整、目的明确 | 否（仅语法/路径核验） |
| 根 `docker-compose.yml` | 服务 `queyi`（数据链）+ `paper`（论文编译） | 结构完整，但有 §4 的 tectonic 矛盾 | 否 |
| `docker/paper/Dockerfile` | ubuntu:24.04 + g++-13 + python3.13 + cppcheck；`run_all.sh` 编排数字复算 | 完整 | 否 |
| `docker/paper/run_all.sh` | 数字复算编排（系统计数 / A5 / 盲区 / 种子 / 676m / 676k / 论文数字对账 / 编译） | 完整、fail-loud | 否 |
| `docker/queyi/Dockerfile` | python:3.12-slim 数据链镜像 | 完整（未钉 digest，honest：无 Docker 验证） | 否 |
| `docker/reproduce/Dockerfile` | ubuntu:22.04 多阶段（gcc-12 / clang-14 / cppcheck / valgrind）全链镜像 | 完整、版本钉死 | **否（从未 build）** |
| `docker/reproduce/docker-compose.yml` | 单服务 `reproduce` + `verify-env` | 完整 | 否 |

> 结论：配置**齐全且文档化充分**，主要风险是「未经实测构建」与一处命令/依赖矛盾（见 §4）。

## 2. 本批产出

| 文件 | 说明 |
|---|---|
| `supplementary/REPRODUCTION.md` | 从零复现指南：前置 / clone / 三种方式（最小 / 数据链 / 全链）/ 无 Docker 本地复现 / 每实验时间资源表 / 不可容器化部分 / 验证清单 |
| `supplementary/environment.yml` | 依赖清单（conda 格式）：python=3.13、pyyaml、门禁/文档可选包 + 系统级依赖（g++-13、tectonic、WSL/MinGW 工具链、MinGW GCC 15.3.0） |
| `docker/minimal_repro.sh` | 最小复现脚本（3 核心实验，只读冻结产物，输出 PASS/FAIL） |
| `data/704_docker_prep_report.md` | 本报告 |

`docker/minimal_repro.sh` 已实跑验证：输出 `PASS=3 FAIL=0`（A5 +24.03pp / 60.07%→24.74% / 真实CVE 59.09%）。

> ⚠️ 落点偏差（如实声明）：原 prompt 任务 B 写 `scripts/minimal_repro.sh`，但 704 红线 6 规定产出只写 `data/704_*` / `supplementary/` / `docker/`；且本仓库既有复现脚本目录为 `Scripts/`（大写 S）。故最小复现脚本落在 **`docker/minimal_repro.sh`**。若作者坚持 `scripts/`，需先放宽红线 6。

## 3. 复现可行性分级（诚实）

- **✅ 容器内可复现**：数字对账、A5/盲区重算、系统计数、种子审计、论文编译（若装 tectonic）。
- **⚠️ 仅宿主机（Windows+WSL）可复现**：真实检测链（asan/ubsan/tsan 需 WSL g++ 13.3；compiler-warn 需 MinGW g++ 13.1）；容器内 Linux 工具链与论文口径存在已知差异。
- **❌ 不进复现链**：Examples/*.asm（需 Windows MinGW GCC 15.3.0）。

## 4. 现有配置的问题与改进建议（**未直接修改**，按红线只给建议）

1. **【矛盾·建议修】根 `docker-compose.yml` `paper` 服务 `command` 为 `tectonic -X compile ...`，但 `docker/paper/Dockerfile` 未安装 tectonic（仅注释提及）。** 首次 `docker compose run --rm paper` 会报 `tectonic: command not found`。建议：在 `docker/paper/Dockerfile` 加 `apt-get install -y tectonic` 或改用 `run_all.sh`（其第 5 步已对缺 tectonic 做 skip 兜底）；或把 compose 的 paper command 改为 `bash docker/paper/run_all.sh`。
2. **【诚实登记】所有 Dockerfile/compose 均未经 `docker build` 实测**（作者机无 Docker）。建议首次构建前按各自头注释核对基础镜像 digest（根 Dockerfile 已钉 `gcc:15.3.0@sha256:...`；`docker/queyi/Dockerfile` 建议补 digest）。
3. **【范围】`docker/reproduce/Dockerfile` 用 gcc-12（jammy），而论文口径是 g++ 13.3（noble）**；镜像内默认 `QUEYI_SKIP_WUNSEQUENCED=1` 以规避 clang 版本差异。建议复现文档明确「容器全链结果 ≠ 论文数字，仅作口径理解」，与 §3 一致。
4. **【可选】缺 `docker/README.md` 索引**：建议在 `docker/` 放一份索引，指回 `supplementary/REPRODUCTION.md`，避免审稿人混淆三个 Dockerfile 的分工（书稿 / 论文 / 全链）。

## 5. 验收对照（704 验收标准 #2）

| 标准 | 状态 |
|---|---|
| 复现指南完整，有最小复现脚本 | ✅ REPRODUCTION.md + docker/minimal_repro.sh（已实跑 PASS=3） |
| 环境清单完整（必须/可选标注） | ✅ environment.yml |
| 不实际构建 Docker 镜像（只写配置/文档） | ✅ 遵守 |
| 现有配置有问题只给建议、不直接改 | ✅ §4 全部为建议 |
