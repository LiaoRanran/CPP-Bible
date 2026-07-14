# Changelog

本项目遵循"竣工即记"原则，按日期记录里程碑。版本号语义见 [`RELEASE.md`](RELEASE.md)。

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
