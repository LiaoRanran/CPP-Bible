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
python tools/verify_paper_numbers.py      # 输出 data/676h_number_audit.{json,md}
python tools/seed_audit_676h.py           # 输出 data/676h_seed_audit.{json,md}
```

`verify_paper_numbers.py` 退出码 1 表示存在**硬不一致**（某个源里的值在论文里找不到），
0 表示全部一致；`seed_audit_676h.py` 退出码 1 表示有实验类脚本未固定种子。

---

## 6. 论文编译

```bash
cd research/latex
tectonic -X compile queyi_neurips2027_v1.1.tex
```

- 样式：`neurips_2025.sty`（Datasets & Benchmarks track，`[dandb]` 选项，默认匿名）。
- 预期：全稿 24 页；正文在 `\label{page:endmain}` 处结束，**正文 ≤ 9 页**（见
  `data/676h_终检.md` 的实测页数，不用换算）。
- 编译 log 里不得出现 `undefined`（引用缺失）或 `??`（`\ref` 落空）。

---

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
