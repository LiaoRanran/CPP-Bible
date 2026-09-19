# 587 建设包 · M6 矩阵「非法值替换」逃逸收口（matrix 值校验硬化，warn 起步）

> 角色：你是机械建设苦力。严格按本任务书执行，不自由发挥、不扩范围。
> 铁律不变：**先量后动、新收紧一律 warn 起步、存量零误伤、一任务一 commit、正反例毒样例、改 CORE 必须同 commit `--update` 重钉、跑多少报多少、取证用 `$LASTEXITCODE`、poison/replay/工件指纹类串行勿并发。**
> 全程不 push、不 golden accept、不替人签。做不完停在任务边界，不留半成品。

## 0. 背景与已确认根因（豆包已侦察，不必重新定位，直接用）

- 门禁函数 `tools/gate_engine.py::check_evidence_matrix()`（约 2849 行）当前只做两件事：
  1. `matrix` 必须是 dict；
  2. `compiler/std/opt` 三个键必须存在且 truthy。
  **完全不校验值**——把 `std` 改成 `c++99`、`opt` 改成 `-O9`、`compiler` 改成垃圾字符串，键还在 ⇒ 门禁放行。
- 发现器 `tools/mutation_fuzz.py::_mut_matrix_values()`（约 399 行）在 586 任务 2 只加了「删键」变异
  （删 compiler/std/opt 之一，EV-MATRIX 以 block「matrix 缺键」拦得住）。
  该函数注释已明确记录：**「非法值替换会逃逸，check_evidence_matrix 只校验键存在」——但该变异点当时故意没实现**
  （预估灌入约 165 个真逃逸，停在 Part 边界交本批）。
- matrix 真实形态（值是 **YAML 列表**，不是标量）：
  - `std: [c++14, c++17, c++23]`
  - `opt: [-O0, -O2]`
  - `arch: [x86-64]`
  - `compiler: [GCC 15.3.0]` 或 `[GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL), Clang (ubuntu-latest runner 默认)]`
  - 可选 `stdlib: [pthread]` / `[libstdc++]`（不是每卡都有，**不得强制**）。
- 本批开工基线（2026-09-18 豆包 fresh 复跑确认）：
  gate 63 规则 / 191 命中（block=0 warn=186 advice=5）；poison 118/118、RULE-COVERAGE 38/63、
  表观 100% / 诚实 95.2%（60/63，3 条 machine-untriggerable 单列）；replay confirm=56/refute=0；
  tool_integrity exit 0；fast 全绿。

## 任务 0 · 先量（不落规则，只出事实）

0.1 全量扫描 `evidence/**/EV-*.md` 的 frontmatter `matrix`，对 compiler/std/opt/arch 四个键
   **逐元素去重列出全部真实取值**，落 `data/matrix_value_inventory.md`（新文件，机器生成、只读台账）：
   - 每个键：去重值清单 + 出现该值的卡数；
   - 标注哪些值带括号注释、自由文本（预期集中在 compiler）。
0.2 用 0.1 的**真实分布反推**合法值口径（不要拍脑袋白名单）。建议起点（最终以覆盖全部存量真实值为准）：
   - `std` 每个元素匹配 `^(gnu|c)\+\+(98|03|11|14|17|20|23|26)$`（若真实分布出现其他年份，据实放宽并记录）；
   - `opt` 每个元素匹配 `^-O[0-3sgz]$` 或 `-Ofast`（据实）；
   - `arch` 每个元素在真实出现集合内（如 x86-64；若有 aarch64 等一并纳入），**本批只对真实出现过的形态开口**；
   - `compiler` 最宽松：元素须含编译器族关键词之一（GCC/Clang/clang/MSVC/g++/clang++，大小写不敏感）
     **且**含至少一段版本数字（如 `15.3.0`、`13`）；括号注释 `(...)` 一律放行。
     目的只是拦「纯垃圾 / 无族名 / 无版本」，不做精确版本白名单。
0.3 零误伤前置自证：用 0.2 口径对**存量 56 卡**跑一遍，必须 **0 命中**。
   若有存量卡不满足，**不得放宽到放过垃圾**，而是停下来在 worklog 报告该卡实际值，交人裁决
   （可能是口径写错，也可能是真脏数据）——不许靠改卡来凑绿。

## 任务 1 · 发现器：补「非法值替换」变异点（先量逃逸）

1.1 在 `_mut_matrix_values()` 中，**保留**现有删键变异，新增「非法值替换」变异（每个键各造，描述带键名+原值）：
   - std 元素 → `c++99`（不存在标准年份）；
   - opt 元素 → `-O9`（不存在优化级）；
   - arch 元素 → `z80-nonexistent`（不存在三元组）；
   - compiler 元素 → `totally-not-a-compiler xyz`（无族名、无版本）。
   只替换列表内元素、保持键与列表结构不变；正文逐字不动（沿用现有 M6「正文逐字不变」契约）。
1.2 跑全量（`--cards all --limit 999 --operators M6`，注意 `--cards all` 不解除默认 limit，教训已在 571），
   **量出新增非法值变体数、其中逃逸数**。586 估约 165，以你实跑为准；把逐键（std/opt/arch/compiler）
   逃逸数分别列出。这一步预期全逃逸（规则还没加），数字用于证明任务 2 的必要性。
1.3 独立 commit（发现器侧）。若该 commit 导致基线快照/冻结结论变化，按实测重冻结并注明「非回归，新增变异点」。

## 任务 2 · 门禁：matrix 值校验（warn 起步，逐元素）

2.1 在 `check_evidence_matrix()` 内、现有「缺键 block」之后，增加值校验：
   - 仅当键存在且为列表时逐元素检查（非列表形态 ⇒ 也 warn，提示应为 flow/block 列表）；
   - 任一元素不满足任务 0.2 口径 ⇒ 产出 **warn**（不是 block；沿用 EV-MATRIX rule_id，
     文案明确子类型，如 `matrix.<键> 含非法值: <值>（疑似被弱化/伪造）`）；
   - **缺键仍为 block（语义不变），值非法为 warn（新增）**，二者不得混淆。
2.2 存量零误伤自证（硬门）：对真实 56 卡跑 gate，命中数必须仍是 **191（block=0 warn=186 advice=5）逐字不变**；
   新规则对存量 0 命中。一旦 warn 增量 >0，回退并按 0.3 交人，不许改卡凑数。
2.3 复跑任务 1 的非法值变体：逃逸应 → 0（被新 warn 拦，按 warn_only 计处置）；逐键给出修前/修后逃逸数。
2.4 独立 commit。`gate_engine.py` 属 CORE_TOOLS ⇒ 同 commit 跑
   `.venv\Scripts\python.exe tools\tool_integrity.py --update` 并带上 `.tool_checksums`。

## 任务 3 · 毒样例 + 回归锁 + 收工

3.1 在 `tools/poison_drill.py` 顺延新增毒载荷（编号接当前最大值，先查现有最大 P 编号，勿撞号）：
   - 阳性：matrix 的 std/opt/compiler 各一张「非法值」沙箱卡 ⇒ 必须命中 EV-MATRIX warn；
   - 阴性对照：与阳性同构但值全部合法的卡 ⇒ 必须放行（防白名单过宽误伤）；
   - 至少 3 阳 + 对应 3 阴。登记 ATTACK_TYPES 攻击面分类。
3.2 若新增/改动了 pytest，遵循 580/583 教训：断言真实仓工件指纹/跑 replay 的用例若在 `-n auto` 下
   被其他 worker 的合法写盘干扰，按既有 `conftest.py` 的 SERIAL_EXTRA / replay_serial 机制归类，不要裸奔。
   护栏/自检不许裸 `except Exception`（570 教训），其「绿」必须有一条能被证伪的测试。
3.3 收工总验收（fresh，串行，全部用退出码定论并贴出）：
   - `tool_integrity.py --check` exit 0；
   - `gate_engine.py --check`：报规则数与命中数；命中数须仍 191（除非你能证明增量全部来自新变异沙箱而非存量卡）；
   - `poison_drill.py`：N/N 全过 + 双指标 100%/100% + 诚实覆盖率口径不下降；
   - `atom_evidence_replay.py --check`：confirm=56 refute=0 infra_error=0；
   - `pytest -m "not slow" -n auto` exit 0；`pytest -m slow -n0` 除已知 `test_golden_lock_json`
     （warn 136→186 待人审 accept 的预期红）外全绿；
   - 受控目录 `git diff --quiet -- atoms evidence Examples` exit 0；
   - 本批新增 ruff 告警为 0（改动文件过 `ruff check`，启用族 E4,E7,E9,F,I001,FURB167）。
3.4 独立 commit（毒样例 + 重钉 + 测试）。

## 任务 4 · 顺手提交 .gitignore（独立小 commit，与上面解耦）

工作树 `.gitignore` 有 3 行未提交改动（空行 + `# local secrets (never commit)` + `.env`），
是保护密钥的正确改动。**只提交 `.gitignore` 这一个文件**：
- 提交前再跑一次 `git check-ignore .env` 必须输出 `.env`、`git ls-files | grep '^\.env$'` 必须无输出；
- `git add .gitignore`（严禁 `git add .` / `git add -A`，绝不能把 `.env` 或其他 WIP 带进来）；
- 独立 commit，message 注明「chore: gitignore .env 本地密钥」。
- `.env` 本身永远不提交。

## 交人（不要自作主张）

- 任务 0.3 若发现存量脏数据：停，报卡 id 与实际值，不改卡。
- compiler 值校验若你判断连「含族名+版本数字」都太严或太松，给出你的实测依据再定，不擅自改口径。
- 是否把值校验从 warn 升 block：本批**不做**，观察期 warn，升级交人。
- 不做：M1 那条 TCE 逃逸、PoC#1/#3、585 冻结项（仓内第二锚、人签通道）、ruff 余族大清扫。

## 交付汇报格式

逐任务给：commit 短 hash、任务 0 真实值分布摘要、任务 1 逐键逃逸数（修前）、
任务 2 逐键逃逸数（修后，应 0）、任务 3 收工门禁全套退出码与数字、任务 4 的 check-ignore 证据、
偏差表（提示词假设 X / 实测 Y 逐条）。worklog 落 `_worklog_587.md`（不入库惯例）。
