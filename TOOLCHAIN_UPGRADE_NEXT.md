# TOOLCHAIN_UPGRADE_NEXT.md — 工具链升级剩余项执行规划

> 制定：2026-08-30（晚）· 承接 [UPGRADE_PLAN_2026-08-30.md](UPGRADE_PLAN_2026-08-30.md) + [REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md](REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md)
> 定位：上一「升级战役」（2026-08-30 白天）已完成**依赖锁定、Actions 版本升级、pre-commit 配置、LICENSE/SECURITY/bootstrap、55+7 引用债务清零、异盘备份**。本文只聚焦**尚未落地的剩余项**，并补充本轮新发现（生成器过时问题）。
> 原则：可逆、可验证、可回滚；每项先清零再加固；**本文全部数字为本机实测，非推测**。

---

## 0. 结论速览

| # | 剩余项 | 实测现状 | 优先级 | 状态 |
|---|---|---|---|---|
| 1 | Python 版本漂移 | `.venv`=3.14.5、托管解释器实 3.13.14（目录名 3.13.12）、系统 `python`=3.14.5（WindowsApps Store stub） | P0 | ✅ 已落地（`fc784ba`；.venv 重建待后续） |
| 2 | 静态检查链 | ruff/mypy/pre-commit 配置已写，但三者 PATH 与 `.venv` 均缺失 | P0 | ✅ ruff 清零并进 CI（150 自动 + 99 人工）；🔶 mypy 待装 |
| 3 | 容器镜像 digest | `ci.yml`/`Dockerfile`/`.devcontainer` 仍用浮动 `gcc:15.3.0` | P1 | ⬜ |
| 4 | 指标单一事实源 | README 的 cpp 块数 7530（实 7523）、自包含章数 112（实 114）、STATE.json 的 `last_commit` 落后 HEAD 24 个提交 | P1 | ✅ 已落地（`metrics.schema.json` + `tools/gen_metrics.py`，已进 CI quality job） |
| 5 | CROSSREF 生成器过时 | dry-run 依赖边 732→103（退化 85%），生成器已与正文链接形式脱节 | P2 | ✅ 已裁决选项 A：CROSSREF.md 头部改「冻结+指向活跃门禁」，删除悬空生成器引用 |

---

## 1. Python 版本漂移（P0）

**实测（2026-08-30）**：

| 对象 | 值 | 备注 |
|---|---|---|
| `.venv/Scripts/python.exe` | 3.14.5 | `uv sync` 拉到了超出预期的 3.14 |
| 托管解释器（配置路径 `.../3.13.12/python.exe`） | 实际 3.13.14 | 目录名与真实版本不符 |
| 系统 `python` | 3.10.11 | 低于 `requires-python = ">=3.11"` |
| `toolchain.toml` `[python].prefer` / `pyproject [tool.cppbible].python` | 均写 `3.13.12` | 与真实 3.13.14 不一致 |

**行动**：
1. 定死目标解释器：以「托管 3.13.x」为**唯一门禁解释器**（它稳定、非 CI 用），本机 `.venv` 与 CI 对齐到同一主/次版本。
2. `toolchain.toml` 增加**版本自检**：`resolve_python()` 返回后校验 `--version` 是否匹配预期 `3.13`，不符即告警/失败（对齐 d5_compile_gate 的「工具链版本漂移即硬失败」范式）。
3. 修正配置路径：把 `3.13.12` 目录名与实际 3.13.14 对齐，或改为 glob 探测 `versions/3.13.*/python.exe`，消除「配置路径不可信」。
4. `.python-version`（uv）或 `uv.lock` 的 `requires-python` 收窄到 `==3.13.*`，阻止 `uv sync` 再拉到 3.14。

**验收**：任意环境跑 `python tools/toolchain.py` 报告的 g++/python 版本均与配置一致；版本漂移即非零退出。

**已落地（2026-08-30 深夜，`fc784ba`，quality 16/16 回归通过）**：

1. `toolchain.toml` `[python].prefer` 改为 glob `versions/3.13.*/python.exe`（容忍 patch 级目录改名），新增 `expected = "3.13"`。
2. `tools/toolchain.py`：`resolve_python()` 支持 glob；新增 `resolve_python_version()` / `expected_python()`；`_main()` 自检打印 `python@ 3.13.14` 并在版本漂移时**非零退出**（对齐 d5_compile_gate 的「漂移即硬失败」范式）。
3. **单一事实源收敛**：`cppbible.py` 的 `find_managed_python()`、`snapshot.py` 的 `PYTHON` 均委托 `resolve_python()`；删除双份硬编码与 `pyproject.toml` 的死配置 stale 路径。四处 `3.13.12` 硬编码 → 一处 glob。
4. 新增 `.python-version`（=`3.13`），阻止 `uv sync` 再拉到 3.14。

**未做（留待下一步）**：`.venv` 仍是 3.14.5（门禁已改走 resolve_python → 托管 3.13.14，故不影响门禁）；CI quality job 的解释器对齐（当前 3.11）未动。

---

## 2. 静态检查链 ruff/mypy/pre-commit（P0）

**实测**：`ruff`、`mypy`、`pre-commit` 在 PATH 与 `.venv` 均缺失；`.pre-commit-config.yaml` 已存在（ruff v0.6.9 + ruff-format + mypy v1.11.2 + pre-commit-hooks v4.6.0），但从未在本机真正跑通过。

**行动**：
1. 装依赖：`uv sync --extra dev`（pyproject 已声明 `ruff>=0.5.0`、`mypy>=1.10.0`）。
2. 安装 hooks：`.venv/Scripts/pre-commit.exe install`；然后 `pre-commit run --all-files` 首跑并回填 `--fix`（ruff 可自动修）。
3. 落地 grip：把首个全绿的 pre-commit 结果固化为基线，后续提交前必须 `pre-commit run`。
4. CI 强制：quality job 追加 `ruff check tools/` + `mypy tools/`（`continue-on-error:false`），使静态检查不再「本机缺失即跳过」。

**验收**：`pre-commit run --all-files` 退出 0；CI quality job 含 ruff/mypy 且失败即红。

**风险**：首跑 ruff 全量可能报大量既有问题，需分两步——先 `--fix` 自动修，剩余 WARN 建 `# noqa` 白名单或降级，切忌一次性大改工具代码。

**已落地（2026-08-30 深夜）**：

1. `pre-commit` 已装（`uv tool install pre-commit` → 4.6.2，隔离于 venv）。
2. **用钉定版本 ruff v0.6.9**（非最新 0.16.5，避免规则集漂移）对 `tools/` 做安全自动修（仅 `[*]` 标记）：**150 处**（去未用导入 F401 / 拆一行多导入 E401 / 去冗余 f 前缀 F541 等），`4f62438`，quality 16/16 + 全量 py_compile 回归通过。

**剩余 99 处 → ✅ 已人工清零（2026-08-31）**：

| 规则 | 数量 | 实际处理 |
|---|---:|---|
| `E741` ambiguous-variable-name | 34 | `l` → `line`（确认无同名遮蔽、无字符串字面量误伤后再改） |
| `E701` multiple-statements-on-one-line（冒号） | 27 | 拆分单行 `if ...: continue` / `try: ...` 体 |
| `E702` multiple-statements-on-one-line（分号） | 21 | 拆分 `a; b` 为两行 |
| `F841` unused-variable | 17 | 确认 RHS 无副作用后删除；**唯一例外**：`run_cpp_assertions.py` 的 `workers = min(8, (os_cpu := __import__("os").cpu_count() or 4))` 只摘除 walrus 目标 `os_cpu`、**保留 `cpu_count()` 调用本身** |

全程未用 `--unsafe-fixes`。清零后 `ruff check tools/` = `All checks passed`，并已加入 `ci.yml` quality job（钉定 `ruff==0.6.9`，`continue-on-error: false`）。

**未做（留待下一步）**：`mypy` 全程未动（需 `uv sync --extra dev` 装依赖 + 类型标注 triage，量大）。CI **只加了 ruff，未加 mypy**——现在加 mypy 必红。

---

## 3. 容器镜像 digest 固定（P1）

**实测**：`ci.yml` compile job 的 `container: gcc:15.3.0`（浮动 tag）；`Dockerfile`/`.devcontainer` 未钉 digest；本机无 `docker`。

**行动**：
1. 在能访问 registry 的环境查 `gcc:15.3.0` 的 digest：`docker manifest inspect gcc:15.3.0` 或 `docker pull gcc:15.3.0 && docker images --digests`。
2. 把 `ci.yml` 的 container 改成 `gcc:15.3.0@sha256:<digest>`；同步 `Dockerfile` 的 `FROM` 与 `.devcontainer` 的 `image`。
3. digest 值写入文档（本文），供日后审计比对。

**验收**：CI 无需因「镜像漂移」而红（#280 教训：PPA/容器微版本浮动会在两次运行间换语言前端）。

**风险**：digest 需联网/装 docker 获取，本机不可得——此项可挂到「有 CI/容器环境时」执行，不阻塞 1/2 项。

---

## 4. 指标单一事实源（P1）

**实测冲突实例**：`NEXT_LLM.md` 正文 HEAD=`6d7d6e9` vs 尾注 HEAD=`445eaa5`；`STATE.json` `last_commit`=`4c5cb32`（2026-08-31 复测时已落后 HEAD **24 个提交**）；README 的 cpp 块数 7530 vs 事实源 7523、自包含章数 112 vs 114。

**已落地（2026-08-31）**：

1. `metrics.schema.json`（库根）：声明 12 个指标字段及其出处——`scan`（Book/
   实时扫描）/ `compile_report`（`tools/compile_report.json`）/ `git` / `date` /
   `ratio_pct`（派生百分比）；外加 `sync`（允许回写的机器自有字段）与
   `checks`（待校验的文档正则 → 期望字段）。
2. `tools/gen_metrics.py`：`--check` 校验漂移（漂移即报 `文件:行号` 并 exit 1）、
   `--sync` 回写 `STATE.json` 的 `last_commit`/`last_updated`/`total_chapters`。
   已进 CI quality job（`continue-on-error: false`）。

**两处与原始方案的有意偏离（记录备查）**：

- **事实取自实时扫描，而非 `build/metrics.json` 快照**。`build/` 未进 git，
  CI 全新 checkout 时该文件根本不存在；且快照本身会陈旧（其 `commit` 字段
  落后于 HEAD）。实时扫描才是权威，快照只作缓存与人读。
- **散文文档只校验、不改写**。原方案要「README 徽章表 / STATE 顶部 /
  ISSUES 头 / NEXT_LLM 速览表全部由生成器产出」，但这些数字嵌在叙述里，
  程序改写会破坏语义与语气；且生成器一旦成为唯一写入者，后续人手改动会被
  静默覆盖。改为：漂移即 BLOCK 并指名行号；只有机器自有的 JSON 字段才
  `--sync` 自动回写。

**踩过的坑（留给后来者）**：`STATE.json` 是 **CRLF 且无末尾换行**。回写时若
统一按 LF + 末尾换行写，会产出 669 行的整文件伪 diff，把真正的 2 行变更
完全淹没。本项目 `core.autocrlf=false`，行尾必须 bytes 级对齐——
`gen_metrics.py` 里已用 `_write_json()` 保留原行尾与末尾换行有无。

**验收**：`python tools/gen_metrics.py --check` 退出 0；已在 quality job。

---

## 5. CROSSREF 生成器过时（P2 · 已裁决选项 A）

**已落地（2026-08-31）**：按选项 A 处理——改 `CROSSREF.md` 顶部声明为
「**冻结于 2026-07-11 · 仅供历史参考**」，删除悬空的「由
`tools/gen_crossref.py` 自动生成」与重生成命令；明确权威交叉引用由
`tools/crossref_audit.py` 与 `tools/xref_check.py` 两个活跃门禁维护。
不动 `gen_mkdocs_nav.py` 引用、不删文件、不重写生成器，代价最小，且不
影响任何现有门禁（它本就不在 CI 扫描范围）。

**背景（2026-08-30 实测）**：`python tools/legacy/gen_crossref.py --root Book`
后 `git restore` 还原，dry-run 结果从 732 条依赖边退化到约 103 条（-85%），
192 KB → 75 KB。根因是 `gen_crossref.py` 只识别旧式 `⟶` 箭头、反引号
`` `Book/...` `` 与 `前置·后续` 元数据，而当前正文已大量使用 Markdown
链接 `[第NN章](Book/...)`，后者由活跃门禁抓取。权威数据源早已转移。

**保留的选项 B/C**：作为后续可选工程记录在案；若未来需要一本可重生成的
交叉引用索引，再评估是否重写生成器以识别 Markdown 链接形式（选项 B），
或彻底删除 `CROSSREF.md`（选项 C）。

**验收**：`CROSSREF.md` 头部已无悬空生成器引用；不阻断任何现有门禁。

---

## 6. 分阶段顺序与护栏

**执行顺序**：`1（Python 版本）✅ → 2（静态检查链，mypy 除外）✅ → 4（指标事实源）✅ → 5（CROSSREF 裁决选项 A）✅ → 3（容器 digest，需容器/registry 环境）`。
理由：1/2 是「P0 且本机即可做」；4 依赖 1 的统一口径；5 是文档声明级、无风险；3 需外部容器环境且不影响本地门禁。

**当前剩余（2026-08-31）**：mypy 类型 triage、容器 digest 两项。

**护栏**（沿用项目红线）：

- 每项独立分支/提交，可 `git revert`；脚本改动须幂等 + `--check`。
- 禁止用扩大豁免/`# noqa` 换取绿色；先把真实债务清零。
- 涉及 `toolchain.toml`/`pyproject.toml` 的改动，改后立即 `python tools/toolchain.py` 自检 + `cppbible.py check --stage quality` 回归。
- 版本/依赖改动是本机 `C:` 唯一存储卷上的高风险操作，先确认 `D:\CPP-Bible-Backup` 异盘副本在手再动。

---

## 7. 给下一 Agent 的精确第一步

> 2026-08-31 已落地：项 1（Python 收敛）+ 项 2 完整（ruff 清零并进 CI）。下面的第一步从「mypy 类型 triage」开始，不再重复已做项。

```powershell
cd C:/CodeLearnling/note/note/C++/CPP-Bible

# 0) 确认接手状态（默认 GBK 控制台也应 exit 0；应报 python@ 3.13.14 且无漂移）
python tools/toolchain.py

# 1) 确认 ruff 仍为零（CI 已硬门禁，本地也别让它红）
uvx "ruff==0.6.9" check tools/                   # 期望 All checks passed

# 2) 装 mypy 并做类型标注 triage（量大，建议单独一批）
uv sync --extra dev                              # 注意：会按 .python-version=3.13 重建 .venv
uvx mypy tools/
#   逐文件补标注，切忌在 pyproject 里加 ignore 换绿

# 3) mypy 清零后，才把 mypy 追加进 ci.yml quality job（continue-on-error: false）
#    ruff 已于 2026-08-31 先行接入（钉定 0.6.9）

# 4) 回归门禁（默认控制台即 16/16，无需再设 PYTHONIOENCODING）
.venv/Scripts/python.exe tools/cppbible.py check --stage quality
```