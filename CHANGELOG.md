# Changelog

本项目遵循"竣工即记"原则，按日期记录里程碑。版本号语义见 [`RELEASE.md`](RELEASE.md)。

---

## [Unreleased] - 2026-08-30

全量仓库审计 + 治理加固里程碑。交付 `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` 与仓库外备份，并修复一批门禁/工具缺陷。已分主题提交并推送远端（至 `4c5cb32`），CI 远端验收中。

### 备份与恢复验证

- 仓库外全量备份至 `C:\RepositoryBackups\CPP-Bible\20260830-090558`（工作树 tar.zst + Git bundle + SHA-256）。
- 验证通过：归档与 bundle SHA-256 复算一致、全量恢复文件/目录差异 0、恢复仓库 `git fsck` 退出 0、`git bundle verify` 通过、ACL 已隔离（关闭继承）。
- 已知残留：备份与源同机同盘（`C:`），第二故障域需加密外置介质/对象存储。

### 质量与工具修复

- **章节口径统一（P0）**：`compile_all.py`、`density_audit.py` 曾把 `Book/` 下全部 Markdown 当章节（151），`consistency_check.py` 把 `assets/history/MANIFEST.md` 当章节；三工具统一只扫描 `chNN_*.md`，章节数固定 147。密度审计修正为 147 章均分 25.7/30，一致性 WARN 33→30（索引文件不再计数）。
- **legacy 审计工具修复（P1）**：`audit_py_tools.py` / `audit_cpp_defects.py` / `chapter_number_audit.py` 根路径改为按 `__file__` 推导，输出写入正确目录；扫描集合为空时退出码 2（原静默假绿 0）。已在任意 cwd 与空仓库副本验证。
- **Windows 中文控制台编码修复**：`xref_check.py` 打印 `⟶` 抛 `UnicodeEncodeError`、`cppbible.py` 按 GBK 解码子进程 UTF-8 输出导致日志线程崩溃——均已统一为 UTF-8 输出/解码。Linux CI 无影响；本机 quality 现可完整复现跑通。
- **内容修复**：清理 11 个章节 12 处 W2 连续空行（`whitespace_fix --apply`）；修复 `ch92_chrono.md:147` 无连线的 Mermaid 图块（补语义边）；`fix_ch36.py` 语法错误修正（仅 `py_compile` 验证，未执行）。
- **CI 发布依赖图（工作树，待远端验收）**：`site/pdf/epub` 由 `needs: quality` 改为 `needs: [compile, publish-check]`；`deploy` 由 `needs: site` 改为 `needs: [site, pdf, epub]`。依据：GitHub Actions `#373` 实测 deploy 于 10:08 完成而 GCC 编译 10:38 才完成，且 EPUB 失败仍发布，证明原依赖可绕过编译。

### 门禁复验结果

- `cppbible.py check --stage quality`：16/16 全绿（审计初 15/16）。
- `cppbible.py check --stage compile`：5/5 全绿（Compile All / Compile Gate / Exempt Audit / D5 Compile Gate / Assertions）。
- Mermaid 静态校验 511/511（审计初 1 处错误）。

### 升级与优化（阶段 A：工具链 · 合规 · 规范 · 环境）

- 新增《[UPGRADE_PLAN_2026-08-30.md](UPGRADE_PLAN_2026-08-30.md)》全面升级方案：7 目标现状-差距-行动矩阵、ABCD 四阶段、资源需求清单。
- **许可（已裁决 MIT）**：新增 `LICENSE`（MIT）；README 许可行由 CC BY-NC-SA 修正为 MIT，消除与 pyproject 的冲突。
- **依赖锁定（已选 uv）**：生成 `uv.lock`（解析 45 包）；`tools/bootstrap.ps1` 改 uv 优先（回退 pip）；新增 `.env.example` 与 `SECURITY.md`。
- **CI 工具链升级**：全部 actions 升级到最新主版本（checkout/setup-python@v7、upload-artifact@v7、upload-pages-artifact@v5、deploy-pages@v5），消除 Node20 弃用告警。
- **规范流程**：新增 `.github/PULL_REQUEST_TEMPLATE.md`（含门禁自检清单）与 `.github/ISSUE_TEMPLATE/`（bug / 内容勘误）；新增 `.pre-commit-config.yaml`（trailing-whitespace、ruff、mypy）。
- 用户裁决：UI 深度「先搞内容」，阶段 C 调整为内容深化与质量收口。

### 工具栈升级 + 门禁 + 前端工具（2026-08-30 追加）

- **依赖锁定（uv）**：全部依赖升级到最新并写入 `uv.lock`（mkdocs-material 9.7.7、ruff 0.16.5、mypy 2.3.1、mkdocs-mermaid2-plugin 1.2.3、pagefind 1.5.2、pypandoc 1.17）；导出 `requirements.lock.txt`（hash 校验），CI `site` job 改为锁定安装。
- **CI actions 再升级**：site/pdf/epub/publish-check/deploy 等全部升级到最新主版本（checkout/setup-python@v7、upload-artifact@v7、upload-pages-artifact@v5、deploy-pages@v5）。
- **新门禁 `cppbible env`**：工具链自检（Python/GCC 15.3.0/objdump/c++filt/uv/git + 锁文件存在性），缺失或版本不符即非零；已接入 bootstrap 第 4 步。
- **前端工具 `tools/site_audit.py`**：站点产物健康自检（首页/章节页可达/静态资源完整性/徽章注入/Mermaid/pagefind），已接入 CI `site` job（构建后、上传前阻断）；附最小 fixture 自测（GOOD=PASS、BAD=FAIL）。
- **内容债任务单**：[docs/references/content_debt_tasklist.md](docs/references/content_debt_tasklist.md) —— 55 处悬空章号引用（按语义建议映射）、7 处前置问题（6 倒置 + 1 悬空）、30 一致性 WARN 执行顺序。

### 内容债清零（2026-08-30 完成）

- **55 处悬空章号引用全部清零**：ch33→ch28、ch34→ch40、ch54/56→ch49、ch59→ch60、ch73→ch51、ch75→ch67（映射）；ch74/ch114/ch102-105 无对应现章，按语义改写至 ch123/ch113/ch93/ch107。20 章节共 89± 行修改，权威映射见 [docs/references/chapter_mapping.md](docs/references/chapter_mapping.md)。
- **7 处前置问题清零**：悬空前置 ch114→ch113；6 处历史/导读章前瞻引用列入 `FORWARD_PRE_EXEMPT` 白名单（作者设计意图，逐项注释依据）。
- **30 处一致性 WARN 清零（根因为工具误报）**：L1 徽章化迁移后 `consistency_check` 仍只认字面 `[标准]` 括号，对 30 个仅用徽章 span 的章误报；新增 `STANCE_BADGE_RE` 兼容两种载体后 `ERROR=0 / WARN=0`（恢复 100/100 基线）。抽样验证（ch04/ch22/ch60/ch165：徽章 52-99、字面 0）确认为规则过时而非内容缺失。
- **门禁转硬 + 两项健壮性修复**：`dangling_ref_linter` / `prereq_topo_check` 由软转硬；修复 `--json` 输出目录不存在时崩溃（CI 干净 checkout 无 outputs/ 抛 FileNotFoundError，曾致 #375 误红——本地 pass/CI fail 的根因）；已全库排查其余写 JSON 工具均带 mkdir，无同类隐患。
- 复验：`quality` 16/16、`dangling=0`、`topology=0`、consistency `ERROR=0 / WARN=0`。

### D5 覆盖口径统一（2026-08-30 完成）

- **根因**：`d5_gap_scanner` 用正文「附录 D5」字面量匹配（=113），`metrics_snapshot` 用标题正则 `^#{2,4}\s*D5\b`（=119）；实测 6 章（ch05/ch11/ch15/ch128/ch146/ch151）标题为 `## D5 真实性能基准：…`/`## D5 性能附录：…` 变体，被字面量口径漏判。
- **修复**：两工具统一为 `^#{2,4}\s*(?:附录\s*)?D5\b` 标题正则（`D5_HEADING_RE`），口径收口为 **119/147（81%）**；该指标在 metrics 中为非阻塞 dashboard，无 CI 影响。
- 复验：quality 16/16 保持全绿。

### 事实源同步（2026-08-30 完成）

- **STATE/ISSUES/README 三文件接入单一事实源**：README 头部数字更新为 metrics 派生值（23.7 万行 / 7530 cpp / 密度 25.7 / D5 119）；STATE.json 刷新 last_commit=4c5cb32、density 24.9→25.7、新增 d5_coverage/mermaid/cpp/lines 指标与 `fact_source` 声明；ISSUES.md 10 项逐条复核——9 项已解决（附证据：ch121 cpp=50、ch122 cpp=45 双门禁 0 fail、ch118 945 行、ch81 1175 行、crossref 0 断链、GCC 硬编码已清），仅 #9 部分遗留（ch01/02/08/09/10 fragment 待批），并新增 2026-08-30 口径遗留清单。
- **UPGRADE_PLAN 状态同步**：D5 口径统一、deploy 依赖解锁两项 P1 标记完成；阶段 A+ CI 远端验收标记进行中。

### CI site/epub 失败修复（2026-08-30）

- **site job「Install MkDocs stack (locked)」必红**：`requirements.lock.txt` 含 uv export 默认注入的 `-e .`（editable），pip 在带 `--hash` 的锁文件中处于哈希校验模式，与 editable 安装不兼容（本地 `pip install --dry-run` 复现同一报错）。修复：改用 `uv export --no-emit-project` 重新导出（site job 仅用独立 tools 脚本与 mkdocs/pagefind CLI，不依赖项目包安装，移除 `-e .` 无副作用）；ci.yml 内生成命令注释同步。
- **site job「Site front-end health audit」误报（本地复现定位）**：`site_audit.py` 三处误报——(1) `Path(base)/"/绝对路径"` 会丢弃 base 从盘根解析，404.html 的 `/Appendix/ub/` 等 174 个绝对目录链接全部误判缺失；(2) ch61 Mermaid 内联 SVG 文本含字面 `<a href="x">` 被当资源引用；(3) `/.`（主题 logo 根链接）与 `/pagefind/*`（索引产物由检查 6 专责）。修复后本地全站 1595 个资源引用全通过，fixture 自测维持 GOOD=PASS/BAD=FAIL。
- **epub job「Generate EPUB」步骤 1~3 分钟内被 cancelled（4/4 复现，#373 时代即存在的旧疾，新依赖图将其暴露）**：pandoc 单次处理 6.2MB combined.md + mermaid-filter（Chromium）在 ubuntu runner 上连带 bash 被信号终止，降级逻辑来不及生效。修复：epub 的 mermaid-filter 改为 `CPPBIBLE_EPUB_MERMAID=1` 显式开启、CI 默认关闭（Mermaid 降级为代码块，保证 EPUB 必产出；PDF job 的分卷管线不受影响）。随 `b2a5a02` 远端复验。

### 现状与遗留

- 内容债已清零（55 悬空 + 7 前置 + 30 WARN + D5 口径）+ 事实源冲突已同步；仍遗留：分支保护未启用、断言 55 WARN、ch01/02/08/09/10 cpp 完整化、legacy 候选人工复核、第二故障域备份（需介质），详见审计报告 §7/§8/§10。

---

## [1.1.0] - 2026-07-15

第三阶段"质量收尾 + 高含金量升级"首个发布。在 1.0.0 全绿基线上，追加实测/工程价值内容，并修复一处编译器特性支持的事实性错误。

### 新增（高含金量）

- **性能数据实测化（P0-1）**：ch27/ch50/ch93 关键数据点由 `[示意]` 升级为 GCC 15.3.0 本机 `[实测]`——多继承 vptr 布局（主 `0x0`/次 `0x8`/槽宽 `0x8`）、同步代价（atomic 3.5ns / mutex 7.6ns / thread 125µs）、转型代价（virtual 0.5ns / dynamic_cast 6.9ns，慢 13.6×）。测量程序落 `_emp_bench/`。
- **编译器版本矩阵（P0-2）**：新增 `docs/compiler-matrix.md`（GCC 列本机实测，Clang/MSVC 标 `[DOC]`）+ 验证工具 `tools/verify_compiler_features.py`，正文引用统一指向本表，禁止在正文写死三编译器版本号。
- **UB / Sanitizer 反例库（P0-3）**：`Appendix/ub/` 15 例（内存 5 + 并发 5 + 生命周期 5），每例配真实 ASan/TSan/UBSan 输出与修复。
- **WG21 提案跟踪表（B3）**：新增 `WG21/TRACKER.md`（C++20/23/26 提案 → feature-test 宏 → 三编译器支持）+ `tools/generate_wg21_tracker.py`（解析并对比本机探测基线出 diff）。
- **面试题嵌入式分类（B2）**：`Interview/` 拆 `general/`（20 题 + 难度分级 + 🔧 嵌入相关标注）+ `embedded/`（E1-E10 STM32F4 硬核题：无堆容器 / 跨 TU ABI / volatile MMIO / 中断安全 / placement new / 内存池 / DMA 抽象 / 零开销寄存器映射 / 全局构造顺序）。
- **汇编实证扩展（B4，累计 8→12 例）**：ch42/48/52/117 各加「附录 E 编译实证」，全部 GCC 15.3 `-O2` objdump 真实生成——
  - ch42 严格别名：翻转 `-fstrict-aliasing` 开关的生成码分歧（缓存返回值 vs 重载内存）；
  - ch48 RTTI：`typeid` 读 `vtable[-1]` 的 `type_info`、`dynamic_cast` 尾调 `__dynamic_cast`；
  - ch52 EBO：空基类偏移 0 vs 空成员偏移 4（sizeof 4 vs 8 汇编可见）；
  - ch117 复制消除：prvalue 直接写返回槽零 copy/move 调用，删 move 仍编译。

### 修复（事实性）

- **deducing this 特性支持误判**（重大）：1.0.0 期间 P0-2 误用不存在的宏名 `__cpp_deducing_this` / `__cpp_explicit_this`（均探测为 UNDEF），错误结论"GCC 15.3 不支持 deducing this"。本机 `-dM` 实探证明正确宏名 `__cpp_explicit_this_parameter` = 202110 **已支持**。全链修正 5 处：`WG21/TRACKER.md`、`docs/compiler-matrix.md`、`_cpp_probe_gcc.json`、`tools/verify_compiler_features.py`、`Book/…/ch10_version_matrix.md`。
- 附带修正：`__cpp_lib_flat_map` = 202207（已支持）、`std::mdspan` / `inplace_vector` 确为 UNDEF、P2300 `std::execution` 宏尚未定名（并澄清 `__cpp_lib_execution` = 201902 是 C++17 并行算法，与 P2300 无关）。

### 质量审计（A 系）

- **交叉引用审计（A1）**：`tools/crossref_audit.py` 实跑 147 章 / 1190 引用 / 断链 0 / part 覆盖率 100%。
- **CI 豁免消化（A2）**：定向重测 66 个豁免块（GCC 13.1，CI 同款 flags）全部合法失败（modules / 外部库 / POSIX / MSVC / 多文件 / 故意错误演示），0 stale；新增防呆工具 `tools/prune_exempt.py`。全量 `--main-only` 复扫：147 章 / 112 通过 / 66 失败块与基线一致。

### 一致性审计（C 系）

- **术语一致性（C1）**：修复索引层 32 处断链引用——`GLOSSARY.md`（ABI/CRTP/data race/deadlock/EBO/UB/vtable 共 7 条）、`CROSSREF.md`（生命周期/虚函数链/协程链/CRTP 链 4 条核心链）、`MISCONCEPTIONS.md`（章节区间头 + 条目章号共 21 处）全部映射到真实章号；`glossary.json` 129 术语 0 断链；术语变体审计（运行期/运行时/范本/解构/指标/多形/内连）确认均为有意用法，0 实际错误。
- **Mermaid 图表审计（C2）**：新增 `tools/mermaid_audit.py`（静态结构校验）+ `tools/mermaid_parse_check.mjs`（官方 `mermaid.parse` + jsdom 真实解析）；全量 88 图块静态 + 官方解析双重校验 0 失败。
- **章编号一致性（C3）**：新增 `tools/chapter_number_audit.py`——校验文件名 `chNN` ↔ H1 `第NN章`、序列连续性、重号、part 区间重叠、mkdocs nav 悬空引用；147 章 0 错、18 个缺号确认为有意预留（33/34/53-59/73-75/102-106/114）。

### 质量基线（不变）

- `consistency_check.py` 147 章 ERROR=0 / WARN=0；CI 编译门禁保持全绿。

---

## [1.0.0] - 2026-07-14

首个可发布快照。147 章全部竣工，质量门禁"本地 + CI"双向全绿。

### 发布质量基线

- **规模**：147 章 / 16 part / 约 14.7 万行 / 6840 个可编译 cpp 块
- **密度审计 v3**：均分 **24.2/30**，浅章（<15 分）**0** 个 —— 密度深化封顶，主线转向质量收尾
- **一致性**：`consistency_check.py` ERROR=0 / WARN=0
- **交叉引用**：0 断链
- **断言**：编译期 + 运行期断言全 PASS

### 2026-07-14 加固（相对 07-13 候选）

- **CI 编译门禁上线**：`compile_all.py --main-only` → `compile_gate.py`（双层豁免：显式清单 + 错误模式）。
  新真实 `SYNTAX` / `TYPE_MISMATCH` 错误一旦引入，CI 立即变红。
- **跨平台回归修复**（本地 mingw 软过、Linux gcc13 暴露）：
  - `ch30` 补 `<csignal>`（`sig_atomic_t`，Linux gcc 不隐式带）
  - `ch35` / `ch36` 补 `<cstdint>`（`uintptr_t`）
  - `ch62` `W<int>` 成员 `double` → `char`（LP64 下 `static_assert` 失败，LLP64 巧合掩盖）
  - 门禁 WINDOWS 模式补 `winsock2.h | ws2tcpip.h`
- **EPUB 去封面**：移除 `--epub-cover-image` 与 `assets/cover.png`（独立作品，无外部封面依赖）；
  EPUB / PDF 构建经 CI 实证干净。
- **豁免清单元数据化**：`compile_exempt.json` 由 `gen_compile_exempt.py` 从审计报告生成，
  66 块 **0 UNCLASSIFIED**。

### 已知设计性豁免（非 bug）

多文件示例、C++20 Modules（`import std;` 需 MSVC 17.5+ / Clang 18+，GCC / MinGW 诚实豁免）、
POSIX / Windows 专用 API、外部库、故意展示的错误 / UB、跨块依赖 —— 详见 `tools/compile_exempt.json`。

---

## [1.0.0-rc] - 2026-07-12 / 07-13

初版竣工候选（详见 [`RELEASE.md`](RELEASE.md)）：

- 清理 311 个 `.bak` 与 6 个临时探针
- 去重审计清零（DUP%=0.0 / WTR%=0.00）
- 单章 lint GPA 98.7（A=146）
- 本地门禁全绿，待 CI 实跑确认
