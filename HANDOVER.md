# HANDOVER.md — 项目接手快照（2026-08-31 晚）

> 接手者先读本文件 + `NEXT_LLM.md`。本快照覆盖 **2026-08-31「极致打磨」收尾后** 的真实状态，
> 数字派生自 `build/metrics.json`（由 `tools/gen_metrics.py --check` 门禁守护，散文里的写死数字与事实源一致）。
> 更早的历史（07-13 前四轮质量验证）见 `RELEASE.md` 与本文末节。

## 一句话概况

《现代 C++ 终极圣经》147 章 / 16 part，已推送 GitHub（`origin = https://github.com/LiaoRanran/CPP-Bible.git`，master 分支）。
CI 七 job 实跑（quality / compile / publish-check / site / pdf / epub / deploy）。
「极致打磨」15 条验收标准 **10/15**：写作质量三件套（one_liner / analogy / pitfall）满标，
写作质量门禁 16/16 全绿。剩余 5 项未达标中 3 项为**内容类诚实天花板**、2 项为**项目有意保留**，不可再注水推进（见「诚实边界」）。

## 当前状态总表（2026-08-31 实测）

| 维度 | 数据 | 状态 |
|------|------|------|
| 章节 | 147 章 / 16 part / 151 文件 / 239,016 行 | ✅ |
| cpp 代码块 | 7,531 | ✅ |
| asm 块 | 497（锚定 137 = 27.6%，**DRIFT=0**） | ✅ 证据真实 |
| D5 性能附录 | 127/147 章（86%），结构 ERROR=0 | ✅ 口径统一为 GCC 15.3.0 |
| 写作质量门禁 | `cppbible.py check --stage quality` **16/16** | ✅ |
| 一致性 | 147 章 ERROR=0 WARN=0，章节一致性 100/100 | ✅ |
| 交引 | crossref_audit 0 断链 + xref_check 0 断裂链接 | ✅ |
| 极致打磨 15 条 | **10/15** | 🟡 见诚实边界 |
| CI | `.github/workflows/ci.yml` 七 job | ✅ |
| Git | 有 remote，master 已推送，工作树干净 | ✅ |

### 「极致打磨」15 条看板（达标 10/15）

已达标：`chapter_levels` 147 · `one_liner` 147 · `analogy` 147 · `pitfall` 147 · `exercise_zero_chapters` 0 ·
`exercise_median` 5 · `extra_css_lines` 411 · `material_features` 16 · `changelog_lag` 0 · `gcc_hardcodes` 0。

未达标 5 项（诚实边界）：

| 指标 | 现状 | 目标 | 诚实边界 |
|---|---|---|---|
| `asm_anchor_rate` | 27.6% | 60% | ≈27.6%（剩余 334 未锚定中约 178 无符号、其余真实源码不在书内） |
| `d5_coverage` | 127 | 147 | ≈127（约 20 章为历史/工具链/库内部，无真实可测性能现象） |
| `unverified` | 294 | 120 | ≈192（130 微架构 + 56 声明头 + 6 C++26 假设，0 个可本机复测数据声明） |
| `root_docs` | 41 | 10 | 有意保留（根目录元文档互链，见 `RELEASE.md`） |
| `glossary_lines` | 39 | 800 | 自动生成（`gen_indexes.py` 文件头明令勿手改） |

## Git 提交链（近期）

```
7a66baa docs(asm): 补锚定 ch88 的 1 个 asm 块（ACCURATE 136→137，27.4%→27.6%）
57a60fc docs(evidence): 真实编译证据锚定 69 个 asm 块 + GCC 15.3.0 重测 8 章 D5 附录
463b8c1 docs(verification): ch79/ch40 本机实测翻牌（unverified 302→294）
b938235 docs(verification): ch41/36/37/44 本机实测翻牌（unverified 314→302）
a50ed89 docs(D5): ch07/08/124/157 补真实性能基准附录
7f8577c docs(D5): ch04/06/14/152 补真实性能基准附录
d4631fb build(site): extra.css 扩至 411 行 + 启用 16 个 mkdocs-material 特性
```

## 环境速查

```bash
# Python
C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe

# C++ 编译器（两套，D5/asm 证据口径 = GCC 15.3.0）
C:/Qt/Tools/mingw1310_64/bin/g++.exe                       # GCC 13.1.0（asm 锚定符号级证据够用）
C:/Users/ASUS/Desktop/gcc-15.3.0-binary/mingw64/bin/g++.exe # GCC 15.3.0（WinLibs ucrt r1，2026-08-31 装）

# 项目根目录
C:/CodeLearnling/note/note/C++/CPP-Bible/
```

## 关键工具速查

| 命令 | 用途 | 预期输出 |
|------|------|----------|
| `python tools/cppbible.py check --stage quality` | 写作质量门禁（16 项） | 16/16 |
| `python tools/gen_metrics.py --check` | 文档数字 vs 事实源（**CI 硬门禁，README 数字漂移即红**） | 全部一致 |
| `python tools/consistency_check.py` | 一致性 | 147 章 ERROR=0 WARN=0 |
| `python tools/verify_asm_evidence.py --root Book --examples Examples` | asm 符号真实性 | ACCURATE=137，DRIFT=0 |
| `python tools/d5_appendix_audit.py` | D5 附录结构 | ERROR=0（WARN=3 措辞建议不阻断） |
| `python tools/metrics_snapshot.py --check` | 重算看板（gitignored） | 10/15 |

> ⚠️ 发布管线正确顺序：`rewrite_links.py --mode site` → **必须** `gen_mkdocs_nav.py` → `mkdocs build --strict`。
> 漏掉第二步会丢 `index.md` + 导航用裸目录名。

## 项目文件结构（关键项）

```
CPP-Bible/
├── AGENT.md / HANDOVER.md / NEXT_LLM.md   ← 接手文档（本文件 + NEXT_LLM 为权威入口）
├── RELEASE.md / CONVENTIONS.md / GOVERNANCE.md  ← 发布快照 / 写作规范 / 治理
├── Book/                  ← 147 章源文件（part01_history … part16_reading，共 16 part）
├── Examples/              ← 真实编译证据（_bench_d5_*.cpp、_chNN_aN.{cpp,asm} 等）
├── tools/                 ← 门禁/审计/发布脚本（cppbible.py 为总入口）
├── .github/workflows/ci.yml ← CI 七 job
└── build/                 ← 构建临时区（gitignored，不入库）
```

## 接手第一步（5 分钟检查清单）

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible
PY="C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"

"$PY" tools/gen_metrics.py --check        # 1) 文档数字 vs 事实源（CI 硬门禁）
"$PY" tools/cppbible.py check --stage quality  # 2) 写作质量 16 项
"$PY" tools/verify_asm_evidence.py --root Book --examples Examples  # 3) asm 证据 DRIFT=0
```

## 诚实边界（不可注水，红线）

1. **内容类三指标已触诚实天花板**：`asm_anchor_rate`（≈27.6%）、`d5_coverage`（≈127）、`unverified`（≈192）。
   强行压到目标值（60% / 147 / 120）只能编造数字或谎报工具链，违反项目「禁注水」红线。
   - `unverified` 翻牌**仅限** `[实验·本机实测]` 且确实在本机跑过基准的声明；`[微架构·x86-64]`（单机器不可验）
     与 `[假设·C++26]`（未来标准）必须保留 UNVERIFIED。
   - D5 附录标题必须写真实工具链版本：**不要为过审计而把 13.1.0 改成 15.3.0**——那是谎报；正确做法是用真
     GCC 15.3.0 重测后改数据。
2. **`root_docs` 41、`glossary_lines` 39 不建议动**：前者是项目有意保留的根目录元文档（`RELEASE.md` 明确列举，
   大量互链）；后者由 `gen_indexes.py` 自动生成、文件头明令勿手改。
3. 若用户接受，可把上述 5 项的验收目标修订为诚实可达值，使看板全绿且无注水项。

## 2026-08-31 当日工作（本轮）

1. **asm 证据诚实锚定 +70**（13.5% → 27.6%）：取书内 asm 块前文的真实 cpp 源码 → `Examples/_chNN_aN.cpp`，
   用 GCC 13.1.0 真实编译 → `Examples/_chNN_aN.asm`，在 asm 块首行插 `; 节选自 Examples/...`（不改原有汇编内容）。
   全程 `DRIFT=0`（零捏造符号）。第二轮窗口搜索仅再命中 1 块，证实剩余块源码不在书内。
2. **装真 GCC 15.3.0**：WinLibs `15.3.0posix-14.0.0-ucrt-r1`（zip 版，Python `zipfile` 解压；
   不要下 .7z——py7zr 不支持其 BCJ2 滤镜）。桌面 `gcc-15.3.0\` 目录是**源码树**（无 g++.exe），不可当工具链。
3. **D5 工具链口径统一（8 章）**：ch04/06/07/08/14/124/152/157 的 D5 附录用真 15.3.0 重测（各 3 次取中位）后改数据。
   典型：ch157 -O0/-O2 3.79×→1.67×、ch14 调试/发布 40.4×→8.20×、ch07 format/snprintf 1.23×→2.82×。
4. **修 CI 报错**：`gen_metrics.py --check` 漂移 3 处（README cpp 7523→7531、d5 119→127、d5_pct 81→86），已回填。
5. **修 9 处 D5.3 demo** `<<"\n"` → `<<std::endl`（d5_appendix_audit 约定）。

## 已知非 bug 编译失败（豁免清单）

`chapter_compile_check.py` 逐块隔离编译，以下失败均为「教学序列/环境缺失/故意反例」，非文档缺陷：

| 章 | 失败块 | 性质 | 说明 |
|----|--------|------|------|
| `ch161_logger` | #1,#9,#17,#28,#30,#34 | FRAG/checker 伪影 | 跨块教学依赖 |
| `ch11_compilers` | `max_of` 块 | 故意反例 | 展示编译推导冲突报错 |
| `ch12_buildsystems` / `ch13_packaging` / `ch16_ide` | 若干 | FRAG/ENV | 本地头/pkg-config/Qt 依赖 |

判定原则：凡属上表性质不计为真实缺陷。语法错误 / 误用 std 符号 / 逻辑错误且非跨块依赖，方为真实 bug。

## 关键决策与经验（含踩坑）

1. **「禁注水」是第一红线**：密度已达天花板，宁可诚实标注，不可为凑绿而掩盖。
2. **asm 锚定不需要 GCC 15.3.0**：`verify_asm_evidence.py` 只做符号级比对（Itanium mangled 名跨 GCC 次版本稳定），
   且证据库本就是 13.1.0/15.3.0 混合。用 13.1.0 编译的 `.asm` 在符号级完全合法。
3. **改 D5 工具链标签 = 谎报**：`d5_appendix_audit` 要求标题含 `(GCC 15.3.0)`；若数字是 13.1.0 测的，改标签就是编造，
   必须用真 15.3.0 重测。
4. **字节级改文件**：批改 Book 用字节级读写保留原行尾（`\r\n`/`\n` 混用）；用 `replace_in_file` 工具比
   `pathlib.write_text` 安全（后者会把 LF 翻成 CRLF 造巨大 diff）。
5. **pre-push 卫生门禁**：`tools/cppbible.py` 在 push 前扫仓库根 `*.cpp/*.exe/*.o` 未跟踪产物并阻断；
   `git status` 不显示被 gitignore 覆盖的文件，需直接枚举。删文件 + push 合成一条命令可一次授权通过。
6. **发布管线顺序**：`rewrite_links → gen_mkdocs_nav → mkdocs build`。

---

_生成时间：2026-08-31 晚 | 上一代 Agent：WorkBuddy（阿信）→ 本代续推「极致打磨」收尾_
