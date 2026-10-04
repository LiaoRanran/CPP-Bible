# REPRODUCE · Queyi 论文数字复现手册（676h）

> 定位：本文件只回答一件事——**别人拿到这个仓库，能不能把论文里的数字重新算出来**。
> 设计原则是 *fail-loud*：拿不到数字就报错退出，不做静默降级；任何"做不到"都写进 §7，
> 而不是含糊过去。

---

## 0. 30 秒自检（最快判断环境对不对）

```bash
bash docker/paper/run_all.sh          # 本机：PY=python bash docker/paper/run_all.sh
```

预期输出（任一不符即 fail 并退出非 0）：

```
OK  判决规则数 len(RULES) = 67
OK  权威账本事件数 = 452
OK  实卡数 atoms_real = 42
Verifier Coverage 31/42 的 CP95 = 58.0 86.1
holdout  82.9% (34/41)
corpus   62.5% (40/64)
corpusC  52.6% (40/76)
layer sanitizer       85.3% (29/34)
layer compiler-warn   50.0% (9/18)
layer cross-compile   16.7% (2/12)
```

随后会跑 `tools/stats_672k.py --selftest`（统计口径自检）与
`tools/verify_paper_numbers.py`（论文数字 vs 权威源，有任何硬不一致就退出非 0），
最后在装有 `tectonic` 时编译论文。全部输出落在 `out/`，**不覆盖 `data/` 下任何产物**。

Docker 路径（原生 Linux，与书稿工具链镜像互不适用）：

```bash
docker build -f docker/paper/Dockerfile -t queyi-paper-repro .
docker run --rm -v "$PWD/out:/workspace/out" queyi-paper-repro
```

---

## 1. 环境版本快照（2026-10-03 实测，`data/` 产物生成环境）

| 组件 | 版本 | 来源 / 核验方式 |
|---|---|---|
| Python（产物生成环境） | **3.13.13** | `data/holdout_reveal_5_672h.json::env.python`；仓库 `.venv` 同值 |
| WSL 发行版 | Ubuntu 24.04.4 LTS | `wsl -- bash -lc "lsb_release -d"` |
| WSL g++（头版检出率用它） | **13.3.0**（Ubuntu 13.3.0-6ubuntu2~24.04.1） | `wsl -- g++ --version` |
| setarch（corpus 档位依赖） | util-linux 2.39.3 | `wsl -- setarch --version` |
| 本机 MinGW g++ | 13.1.0 | `g++ --version`（**无 UBSan 运行时**：`cannot find -lubsan`） |
| 本机 clang | 22.1.8 | `clang++ --version` |
| clang-tidy（E9） | LLVM **22.1.8**，Windows 原生 | `data/673e_验收报告.md` |
| cppcheck（E9） | **2.13.0**，WSL Ubuntu 24.04 | 同上 |
| tectonic（论文编译） | **0.17.0** | `tectonic --version` |

依赖安装（实际项目全部重算**只用标准库**，下面这些是跑测试/可选复算用的）：

```bash
python -m pip install -r requirements.txt
```

### 1.1 必需的 WSL 环境变量（**直调 `wsl.exe` 的脚本一律要先设**）

本机 **WSL 2.7.10 + Windows 系统代理开启**时，每次 `wsl.exe` 调用都会向 stderr 写一条
**UTF-16LE 横幅**。Python 侧 `subprocess.run(..., text=True)` 会因此解码失败 ⇒
`stderr` 变成 `None` ⇒ **依赖 stderr 的报告（ASan / UBSan / TSan）全部丢失 ⇒ 系统性假 miss**。

```bash
export WSL_UTF8=1
export WSLENV=WSL_UTF8/u
```

- 治本层；`unset HTTP(S)_PROXY` **没用**（横幅来自注册表代理配置，不是环境变量）。
- 适用：`tools/detect_for_assets.py`、`data/blindspot_676g_runner.py`、
  `tools/audit_676k_compile.py`，以及任何直接 `subprocess` 调 `wsl.exe` 的工具。
- **反向坑**：`detect_for_assets.py --check` 的"适配层卸载后 env 已还原"断言**假设
  `WSL_UTF8` 初始未设**；跑 pytest 时**不要**带这个变量（否则该断言会红）。
- 出处：673r（`data/673r_A5实验报告.md` §适配层）、673u（`data/673u_wunsequenced修复报告.md`）。

---

## 2. 数据 / 扩样（如需重新生成样本；通常不必，样本已在 `data/holdout_expansion/`）

```bash
python data/expansion_676c/generate_676c.py      # 扩样 A（模板 + 生成）
python data/expansion_676c/verify_676c.py        # 扩样 A 校验
python data/expansion_676c/analyze_676c.py       # 扩样 A 分析
# B–G 六批分别在 data/expansion_676c{B,C,_D,_E,_F,_G}/ 下，脚本命名一致
```

预计耗时：每批 10–40 分钟（含编译/真机校验）。

---

## 3. 检测器运行与 reveal（**需要 WSL**；这一步才是"头版数字"的来源）

```bash
wsl -- bash -lc "cd /mnt/c/CodeLearnling/note/note/C++/CPP-Bible && \
  python tools/holdout_reveal_5_672h.py && \
  python tools/external_corpus_reveal_672h.py"
python tools/holdout_merge_672h.py               # 合并历史 + 新样本
python tools/verify_expand_672h.py               # 扩样自检（分母/分层/口径）
```

预计耗时：holdout 41 样本 × 双档 × 3 回合 ≈ 20–40 分钟；corpus 64 样本 ≈ 30–60 分钟。
**不在 WSL 里跑会静默降级**（15 条样本变 `unknown`，corpus 35.0%→10.0% 且门禁仍绿）——
这是论文 §Analysis(2) 记录的真实事故，`run_all.sh` 第 0 步会显式检查 `setarch` 是否存在。

---

## 4. 统计检验 / 三臂对照 / A5 / 盲区

```bash
python tools/stats_672k.py --selftest     # 统计口径自检（不读产物）
python tools/stats_672k.py                # 重算 δ/CI/McNemar/h/power/e-value
python tools/run_a5_experiment_673p.py    # A5（673p/673r 口径，840 次 detect）
python data/676f_pipeline.py              # 676f：A5 全量重跑（1147 样本；小时级）
python data/676f_analysis.py              # 676f 结果汇总
python data/blindspot_676g_runner.py      # 676g：检测器盲区地图（小时级）
python data/blindspot_676g_analysis.py
python tools/mutation_test_656.py --seed 20260928   # 变异（core，默认种子即 20260928）
python tools/external_anchor_672j.py      # E8 外部锚点
python tools/llm_arm_672i.py              # E7 LLM 裁判臂（需 API key）
```

预计耗时：A5（673p 口径）≈ 分钟级；676f/676g 全量 ≈ 小时级（WSL + 双档）。

---

## 5. 论文数字 vs 权威源（本批新增的两个审计工具）

```bash
python tools/verify_paper_numbers.py      # 数字→权威源：118 检察 / 113 一致 / 0 硬伤
python tools/recompute_a5_676f.py         # 从原始 verdict 矩阵**独立重算** A5 与 676g 盲区
python tools/data_integrity_676h.py       # 1137 样本清单：去重/切分/planted 不变式 + md5 重算
python tools/seed_audit_676h.py           # 种子登记：实验类未固定种子须为 0
```

- `verify_paper_numbers.py` 退出码 1 表示存在**硬不一致**（某个源里的值在论文里找不到）。
- `recompute_a5_676f.py` 不读结果文件里的率，直接从 `data/a5_676f_detection_matrix.json` 与
  `data/blindspot_676g_detection_matrix.json` 重算：FD 309/566、Random 173/566、Static 140/566、
  full-pool 340/566，并列分析 Δ(FD−Random)=0.00pp、Δ(FD−Static)=+30.57pp，盲区比 0.3836、
  并集 61.6%——任一不符即非零退出。
- `data_integrity_676h.py` 重算 md5 与 `data/676f_pipeline.py::_md5_files` 同口径（文件名 + 字节，
  排序）；当前一致 1080 条、跳过 57 条（内联代码 / 语料文件不在库内）、失配 0；
  清单指纹 `sha256[:16] = c9f51f51bc96f034`。
- `seed_audit_676h.py` 退出码 1 表示有实验类脚本未固定种子（当前为 0）。

---

## 6. 论文编译

```bash
cd research/latex
tectonic -X compile queyi_neurips2027_v1.1.tex
```

- 样式：`neurips_2025.sty`（Datasets & Benchmarks track，`[dandb]` 选项，默认匿名）。
- 预期：全稿 **30 页**（676m 起；676h 时为 29 页）；正文在 `\label{page:endmain}` 处结束，
  **正文 ≤ 9 页**（676m 实测仍为 9 页 —— 见 `data/676m_论文更新报告.md` §0）。
- 编译 log 里不得出现 `undefined`（引用缺失）或 `??`（`\ref` 落空）。
- **正文零余量**：676m 实测基线正文已满 9 页，任何主文本净增都会溢出到第 10 页
  ⇒ 新增内容必须同步把等量细节移入附录。

---

## 6.1 数据修复与 A5 重算（676m）

```bash
# 数据修复（H1 挂起样本判据 / H2 统一词表 / M1–M5 字段完整性）—— 幂等，重跑零改写
.venv/Scripts/python.exe tools/fix_676m_schema.py --stage all

# 只校验（门禁用）：H1 残留须为 0、待迁移须为 0；有残留则 exit 1
.venv/Scripts/python.exe tools/fix_676m_schema.py --verify

# A5 重算（修正标签后主端点须与 676f 逐位一致）
.venv/Scripts/python.exe tools/recompute_a5_676m.py

# 只校验（门禁用）：不写任何 data/ 产物，主端点逐位比对；不一致则 exit 1
.venv/Scripts/python.exe tools/recompute_a5_676m.py --check
```

预期输出（实测）：

```
[676m][OK] 数据已处于 676m 修复后的稳定态（H1 残留 0、待迁移 0）
[676m-D][check] 修正件：expected_verdict 34 处、defect_type 308 处
[676m-D][check] k=4 主端点逐位比对：14/14 一致
[676m-D][check][OK] 标签修正对 A5 主端点零影响（逐位一致）
```

**为什么主端点不变（原理）**：A5 的 catch 判定读 `per_asset`（真实 `detect` 判定），
`expected_verdict` 全程不参与 ⇒ H1 改标注不改观测。唯一受影响的是 `expected=catch` 口径：
8 资产并集 recall **93.86% → 98.42%**（分母 668 → 634）。

---

```bash
python tools/recompute_a5_676f.py    # A5 全量 + 676g 盲区：从 1137×8 / 1147×8 原始矩阵重算
python tools/data_integrity_676h.py  # 数据完整性：清单不变式 + md5 重算（零失配）
```

## 7. 已知不可复现 / 不可一键复现（fail-loud 清单，不掩饰）

| # | 项目 | 状态 | 原因与处置 |
|---|---|---|---|
| 1 | 头版检出率（82.9% / 62.5%） | **仅 WSL 可复现** | 依赖 `g++ 13.3 + setarch + ASan/UBSan/TSan`；本机 MinGW 无 UBSan 运行时。Docker 镜像装的是原生 Linux g++ 13.3，环境不同 ⇒ 只能作口径理解，不得用于改结论 |
| 2 | E9（clang-tidy / cppcheck） | **不可一键复现** | 驱动脚本未保留在仓库，只保留了 `data/673e_*_raw.json` 与统计产物；且 clang-tidy 是 Windows 原生 LLVM 22.1.8、cppcheck 是 WSL 2.13.0，Ubuntu 24.04 的 clang-tidy 是 LLVM 18 ⇒ 版本不对称 |
| 3 | tab:e3 的 656 行（62.5%, 30/48） | **无产物可复现** | 现存变异报告重算为 110/114 与 130/159；论文已加"un-pinned"脚注 |
| 4 | tab:e3 的 665 行（66.7%） | **口径已退役** | 属旧 `-O1` 单档口径，只能追溯到 `research/paper_v0.4.md`；论文同上标注 |
| 5 | 变异脚本的双种子 | 需注意 | `tools/mutation_test_656.py` 模块级 `SEED = 20260930`，而 `run()` 的 `--seed` 默认是 **20260928**（产物登记值）。变异体抽样由后者决定，重跑请用 `--seed 20260928` |
| 6 | OTS 时间锚 | 只是占位 | 零见证，论文已声明"on-chain"不成立 |
| 7 | macOS | 不可复现 | 无 `setarch`（BSD 系），corpus 档位无法实现 |
| 8 | 676m 的 H1/H2 修正**是否影响 A5** | **已验证零影响** | `recompute_a5_676m.py --check` 逐位比对 14/14 一致。**注意**：主分析不读 `expected_verdict`，所以"标签改了数字没变"是原理必然，不是漏算 |
| 9 | `planted` 的层级分歧 | **未解决（已登记）** | 676f 的 A5 矩阵把 `corpus` 记为 `planted=true`；676g 清单为 `null`；676m 的 M3 修正件为 `false`。本批按红线 9 **只修 676g 层**，未改 A5 层 ⇒ 论文的 planted 子组分析仍按 `true` 计。见 `data/676m_数据修复总报告.md` §8 |
| 10 | 676k 的编译抽检 / 来源核查 | **需要外部条件** | `audit_676k_compile.py --sample --run` 需要 g++ 13.x + WSL（约 10 分钟）；`audit_676k_source.py --collect --probe` 需要联网访问 NVD / GitHub API。已落盘结果：`data/676k_compile_results.json`（217/217）、`data/676k_source_results.json`（74/74）。`run_all.sh` 默认**只跑**离线的完整性 + 去重两项 |
| 11 | 676l 的矩阵与 676f 的矩阵不一致 | **已披露** | 两者在 349 个共同样本上有 38/1396 格（2.7%）判定不同，与 ~5% 跑间不稳定同量级。排序结论稳健，**逐格结论不稳健**（论文附录 `app:bench676l` 已写明） |

---

## 8. 随机种子表（`tools/seed_audit_676h.py` 自动登记）

| 种子 | 用途 | 登记处 |
|---|---|---|
| `20260930` | 项目约定种子：Random† 臂、A5 单点、扩样（672h）、多数实验脚本 | `tools/baseline_670a.py`、`tools/selection_strategies_673p.py`、`tools/run_a5_experiment_673p.py`、`data/current_numbers.json::seed` |
| `20260928` | 变异体抽样 | `tools/mutation_test_656.py --seed`（产物 `data/656_mutation_report*.json::seed` 同值） |
| `20261003` | 676f 派生/评估切分 | `data/676f_pipeline.py::SEED_SPLIT` |
| `6761 / 6762 / …` | 676c 扩样各批 | `data/expansion_676c*/` |
| `636` | 盲化协议 | `tools/blind_protocol_636.py` |
| `676 / 67610` | 676g 盲区抽签 | `data/blindspot_676g_runner.py`（`random.Random(676)` / `Random(67610)`） |

实验类脚本**未固定种子**的数量：**0**（`data/676h_seed_audit.json::summary.experiment_unseeded`）。
