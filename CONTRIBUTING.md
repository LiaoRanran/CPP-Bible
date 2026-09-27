# CONTRIBUTING — 贡献指南

> 面向**第一次来这个仓库的人**：这一页告诉你环境怎么装、测试怎么跑、PR 怎么提。
> 更深的设计约定见 [`CONVENTIONS.md`](CONVENTIONS.md)、[`GOVERNANCE.md`](GOVERNANCE.md)、
> [`NEXT_LLM.md`](NEXT_LLM.md)（接手者的第一入口）。
> 提交前请先读行为准则 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) 与签署方式 [`DCO.md`](DCO.md)。

## 一、项目在做什么（30 秒版）

CPP-Bible 不只是"一本 C++ 教程"，它是**可执行知识的验证基础设施**：

- `Book/` 是 147 章 C++ 教程，正文里的每个 ```cpp 代码块都要能独立编译；
- `atoms/` 是知识卡（原子命题），`evidence/` 是证据卡，二者构成"每句话都有出处"的账本；
- `tools/` 是门禁与判决工具（67 条规则 / 9 个保护器 / 信任根哈希面）；
- `web/` 是把真实台账渲染出来的静态站（星图 / 现场验哈希 / 复现清单）。

所以本仓库有两条铁律：**不注水**（每个数字、每段汇编、每条结论都要有真实产物）与
**可复核**（任何人可用同样命令跑出同样结论）。贡献时请默认按这两条自律。

## 二、开发环境

| 项 | 要求 |
|---|---|
| Python | **3.11+**（CI 主跑 3.11；本地实测 3.12/3.13/3.14 亦可） |
| C++ 工具链 | GCC 13.1+（`toolchain.toml` 记录本机解析结果；汇编实证用 GCC 15.3） |
| 可选 | `node`（前端 JS 语法自检 `node --check`）、`pandoc`+`texlive`（PDF）、`mkdocs`（站点） |

```bash
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible
python -m pip install -r requirements.lock.txt   # 或 uv sync（有 uv.lock）
python tools/cppbible.py check --stage quality    # 快速自检：期望全绿
```

## 三、测试怎么跑（两阶段，别混用）

```bash
python -m pytest -m "not slow" -n auto     # fast：纯逻辑，可并行（本地约 6 分钟）
python -m pytest -m slow -n0               # slow：真编译 / replay / poison，必须串行
python tools/pytest_two_phase_643.py --fast|--slow|--both   # 统一入口（计数以 junit XML 为准）
```

约定（详见 [`docs/pytest_two_phase.md`](docs/pytest_two_phase.md)）：

- 新增测试默认落 **fast**；碰到编译器、真实仓库状态、子进程写盘的，必须登记进
  `tests/conftest.py` 的 `SLOW_MODULES` / `SERIAL_EXTRA`，否则会污染并行跑；
- 改了 `SLOW_MODULES` / `SERIAL_EXTRA` 或 `pyproject.toml` 后必须重钉信任根：
  `python tools/tool_integrity.py --update`（否则门禁拒跑）；
- **不要**把 `-n auto` 写进 `addopts`（会与串行锁打架，见 `pyproject.toml` 的长注释）。

## 四、提交前必须过的门禁

```bash
python tools/tool_integrity.py --check      # 信任根哈希面（工具/配置/刻度 34 条）
python -m ruff check tools/ tests/          # 静态风格
python -m mypy --ignore-missing-imports tools/
python tools/license_header_check_655.py    # 许可证头（新增 .py 必须有 Apache-2.0 SPDX 头）
python tools/cppbible.py check --stage quality    # 内容/结构门禁（16 项）
```

涉及内容章节时再加：

```bash
python tools/chapter_compile_check.py Book/partXX/chYYY_xxx.md   # 单章编译
python tools/consistency_check.py                                # 全文一致性（期望 0 ERROR / 0 WARN）
python tools/compile_gate.py                                     # 编译回归分账（NEW=0）
```

> 这些命令的当前结果都写在 [`README.md`](README.md) 的"质量门禁"表里 —— 数字会过期，请以你本地实跑为准。

## 五、提 PR 的流程

1. **开 Issue 先说**：Bug / 功能 / 提问三个模板见 `.github/ISSUE_TEMPLATE/`；内容勘误用 `content_errata.md`。
2. **建分支**：`feat/xxx`、`fix/xxx`、`docs/xxx`；一个 PR 只做一件事（小步快跑）。
3. **写测试**：新增工具要有 `--check` 自检 + 单测；修 Bug 要有能复现的用例（红→绿）。
4. **签 DCO**：`git commit -s`，每个 commit 带 `Signed-off-by`（见 [`DCO.md`](DCO.md)）。
5. **填 PR 模板**：`.github/PULL_REQUEST_TEMPLATE.md`，勾选门禁自检、贴证据（命令 + 关键输出）。
6. **诚实登记**：做不到的、只做了一半的、口径有疑的，**写进 PR 描述**而不是藏起来 ——
   本项目的治理原则是"没做到的明说"，隐瞒比做不到严重。

## 六、good first issue 候选（欢迎从这里开始）

| 方向 | 具体入口 | 难度 |
|---|---|---|
| 存量 `.py` 补许可证头 | `python tools/license_header_check_655.py --report`（`--apply` 可批量补），重点是 `_archive/` 以外的活跃目录 | ★ |
| 文档死链巡检 | `python tools/crossref_audit.py` 的 WARN 项、`References/` 内部互引 | ★ |
| 前端可用性 | `web/` 的键盘可达性、移动端布局、`verify.html` 大批量文件的进度条 | ★★ |
| 增量测试选择 | `tools/test_selector_655.py` 的 `--since` 映射表补全（新测试↔源文件的关联规则） | ★★ |
| 新增门禁自检 | 给 `tools/` 里还没有 `--check` 的老工具补只读自检（照抄 `tools/liveness_impact.py` 的写法） | ★★ |
| 收敛 `docs/` 陈述 | 把过期的口径数字改成"从产物现算"，参考 `tools/w2_derived_640c.py` | ★★★ |

> 认领方式：在对应 Issue 下留言，或直接开 PR 并在描述里引用本表条目。

## 七、禁止操作（红线）

- ❌ 覆盖已有章节文件 / 修改章节编号 / 重命名 part 目录；
- ❌ 删除 `_legacy_*`、`_archive/` 目录；
- ❌ 手改 `glossary.json`（用脚本追加）；
- ❌ 改动判决核心（`tools/gate_engine.py` 等 `CORE_TOOLS`）、67 条规则、历史账本
  （`data/authority/*.jsonl`）与受控目录（`atoms/`、`evidence/`、`Book/`、`Examples/`）—— 这些需要维护者评审；
- ❌ 编造数据（示意值必须显式标注，且不得冒充实测）。
