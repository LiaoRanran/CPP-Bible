# 693-B4 · Docker 复现阶段验证报告（宿主机实测 + 容器未实测）

- 生成：2026-10-08（693 批次）
- 脚本：`scripts/reproduce_all.sh` / `scripts/verify_environment.sh`
- 产物：`docker/reproduce/Dockerfile`、`docker/reproduce/docker-compose.yml`、`.dockerignore`、
  `docs/ENVIRONMENT.md`、`requirements.txt`、`data/693_data_manifest.sha256`

---

## 1. 结论先行

| 项 | 状态 |
|---|---|
| 本机是否安装 Docker | **否**（`docker --version` → `bash: line 1: docker: command not found`） |
| Dockerfile / compose 是否**实际构建过** | **否** —— 如实登记"未实测构建"（693 红线 7） |
| 复现脚本是否在**宿主机**跑通 | **是**（见 §2） |
| sha256 数据完整性 | **通过**：14 项权威冻结产物，`missing=0 mismatch=0` |
| 论文数字复算（S2） | **通过**（复用 676h `docker/paper/run_all.sh`，含 tectonic 编译 PDF） |
| 论文门禁 | **PASS**（`paper_quality_gate_670c2.py`） |
| fast_gate | **FAIL** —— 见 §4，**与 693 无关的环境/既有问题** |

**一句话**：Docker 相关文件是**设计完备但未实测**的；复现流水线本身在宿主机上跑通了
S0–S2 与论文门禁。任何人拿到一台装了 Docker 的机器，应当能直接
`docker compose -f docker/reproduce/docker-compose.yml build`。

---

## 2. 宿主机实测记录（`bash scripts/reproduce_all.sh --out out/693_reproduce`）

```
[reproduce] S0 环境体检
  结果：OK=3  FAIL=0  WARN=11  (mode=report)

[reproduce] S1 数据完整性校验（sha256）
  missing=0 mismatch=0

[reproduce] S2 论文数字复算（复用 docker/paper/run_all.sh）
  OK  run_all 通过
  note: Writing `../../out\queyi_neurips2027_v1.1.pdf` (279.9 KiB)
  [run_all] 全部完成。输出目录：out/693_reproduce

[reproduce] S3 门禁检查
  OK  paper_quality_gate
  [OK ] 摘要≤250词                摘要英文词数 = 229
  [OK ] 无 TODO/FIXME/HACK 残留   仅已登记占位（TODO{670a} 宏 + 0 个 ablation 占位）
  [paper-gate] PASS
  fast_gate 退出非 0（见 §4）
```

耗时：约 52 s（`--skip-env` 档）／约 78 s（含环境体检）。

### 2.1 环境体检的实测输出（Windows native 画像）

```
g++ = 13.1.0      clang = 22.1.8      cppcheck = 2.21.0      clang-tidy = 22.1.8
cmake: MISSING    valgrind: MISSING
python = 3.13.14
-fsanitize=address|undefined|thread → 当前画像下不可用（MinGW 无 sanitizer 运行时，属已知预期）
-Wunsequenced 不被接受 ⇒ 该资产恒 unknown（673u 已登记的 MinGW 坑）
检测到 WSL ⇒ 提示必须 export WSL_UTF8=1 + WSLENV=WSL_UTF8/u
```

三条 sanitizer 警告**不是环境配置错误**，而是 `windows-native-mingw` 画像的已知属性
（689/692 已实测登记）。脚本对此做了区分：只有当画像**明确声称支持** sanitizer
（`wsl-gcc-13.3` / `docker-ubuntu-22.04`）却不可用时才判 FAIL。

---

## 3. sha256 清单覆盖的 14 项权威冻结产物

| 文件 | 说明 |
|---|---|
| `data/blindspot_676g_detection_matrix.json` | 冻结检测矩阵 1147×8（681 修复后） |
| `data/676m_a5_matrix_corrected.json` | 676m A5 修正矩阵 |
| `data/a5_676f_detection_matrix.json` | A5 全量检测矩阵 |
| `data/676m_sample_manifest_corrected.json` | 34 类规范词表 + 样本清单 |
| `data/681_type_stats_normalized.json` | 34 类归一化类型统计（n=1147） |
| `data/683_real_world_detection_matrix.json` | 真实世界检测矩阵 |
| `data/683_real_world_project_matrix.json` | 真实世界项目矩阵 |
| `data/683_real_world_type_matrix.json` | 真实世界类型矩阵 |
| `data/684_complementarity_matrix.json` | 资产互补性矩阵 |
| `data/685_literature_matrix.json` | 文献对照矩阵 |
| `data/689_annotation_key_mapping.json` | 人类标注密钥 |
| `data/holdout_reveal_5_672h.json` | holdout reveal 产物 |
| `data/external_corpus_reveal_672h.json` | 外部语料 reveal 产物 |
| `data/authority/decision_event_v2_ledger.jsonl` | 权威判决账本（452 事件） |

复算命令：`python tools/gen_693_manifest.py`（重写）/ `python tools/gen_693_manifest.py --check`（校验）

---

## 4. fast_gate 未通过的三条（**均与 693 本批改动无关**）

| 条目 | 失败原因 | 是否 693 引入 |
|---|---|---|
| `pytest（本批指定）` | `fast_gate` 用 `sys.executable`；此处解析到托管 Python 3.13.12，该解释器**未装 pytest**。用 `.venv/Scripts/python.exe` 跑即正常 | 否（环境/调用方式问题） |
| `658 门禁 S6 单元测试(658)` | `[658 gate] overall=FAIL L0 4/5`，S6 单元测试 rc=1。**工作树在 693 开始前就已存在对该门禁报告的未提交修改** | 否（既有状态） |
| `前端自测 node web/run_tests.mjs` | 命中沙箱的批量删除保护（`SAFE_DELETE_BULK_CONFIRM_REQUIRED`，web/dist 57 项），属执行环境策略拦截 | 否（沙箱策略） |

处理：**不修改 658 门禁相关文件**（693 红线 4：不裹挟其他批次在途文件）。
在 F1 阶段以 `.venv/Scripts/python.exe` 重跑 `--skip-frontend` 档，登记真实门禁状态。

---

## 5. 容器内复现的**未实测**清单（诚实登记）

以下动作**一次都没有执行过**，没有任何实测输出可以引用：

1. `docker build -f docker/reproduce/Dockerfile`
2. `docker compose -f docker/reproduce/docker-compose.yml build`
3. `docker compose ... run --rm verify-env`
4. `docker compose ... run --rm reproduce`

已做的**静态**核对：

- Ubuntu 22.04（jammy）官方仓库中 `gcc-12=12.3.0-1ubuntu1~22.04`、`clang-14=1:14.0.0-1ubuntu1.1`、
  `cppcheck=2.7-0ubuntu2`、`clang-tidy-14`、`valgrind=1:3.18.1-1ubuntu2`、
  `python3.10=3.10.12-1~22.04.3` 的包名与版本串已逐条核对；
- 与 `docs/ENVIRONMENT.md` 的版本表做了一致性核对；
- Dockerfile 内置了版本自检 `RUN`（`gcc --version | grep -q 12.3.0` 等），装错会在构建期失败而非运行期静默给错数。

**首次构建请务必把失败输出原样贴进 issue**，不要靠改版本号"让它过"——那会把环境锁定文档变成谎言。

---

## 6. 为什么 693 的复现镜像放在 `docker/reproduce/` 而不是仓库根

仓库根的 `Dockerfile` 已存在且被 CI 引用（`gcc:15.3.0` 工具链镜像，钉 digest 用于 compile job）。
693 **不覆写**它，避免破坏既有门禁；本镜像独立放在 `docker/reproduce/`。
同理，`docker-compose.yml`（683-E3，两个服务）也未被覆写，新增文件为
`docker/reproduce/docker-compose.yml`。
