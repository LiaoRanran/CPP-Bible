# _worklog_570 · 收口去 -Werror 逃逸 + ruff 口径钉死

> 任务书：`References/architecture_架构演进/570_去Werror声明绑定_ruff钉select.md`
> 承接：`51d8634`（569）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付（一任务一 commit）

| 任务 | 内容 | commit |
|---|---|---|
| 1 | 新规则 `EV-WERROR-DECL-BIND`（warn，存量零命中）+ 毒载荷 P71/P71-阴 | `e659a2a` |
| 2 | ruff 显式钉 `select = [E4,E7,E9,F]` | `1338ef8` |
| 附 | 修正 569 的退出自检**静默空转**（见 §4） | `82c89ce` |

## 1 · 任务 0：两张计数表（先量后动）

脚本：解析全部 56 张 `EV-*.md` 的 frontmatter，在 `falsification/expected/hypothesis/claim_boundary`
四个**判据声明字段**里找 warning/error 级措辞与 `-Werror`。

**表 1 · `command` 带 `-Werror` 的卡**：**1 张** —— `EV-LANG-001`（其命令里三条
`g++ -O2 -std=c++23 -Wall -Wextra -Werror -c …` 诊断编译）。

**表 2 · 声明里出现 warning 级措辞的卡**：**2 张**，逐张定性：

| 卡 | 命中字段 | 定性 |
|---|---|---|
| `EV-LANG-001` | `falsification`, `expected` | **判据性**：`falsification` 明写「『零诊断』由 `-Werror` 承担……**判据必须带 `-Werror`**」；`expected` 写「三条 `-Wall -Wextra -Werror` 编译 rc=0 且零输出」 |
| `EV-CONC-006` | `expected` | **误报**：命中的是 TSan **运行时输出串** `"WARNING: ThreadSanitizer: data race"`，与"编译期警告级判据"无关 |

⇒ **判据性 vs 装饰性的判别指纹**（本批核心口径）：**判据性 `-Werror` 会写进"判据声明"字段，
装饰性只出现在 `command` 里**。EV-LANG-001 正是前者；EV-CONC-006 说明"按措辞宽匹配"会误伤
⇒ 弃用宽匹配（一个真误报就够否掉）。

**表 3 · 新规则存量误伤预估 = 0**：前提集（声明含 `-Werror`）= 1 张（EV-LANG-001）；
它的三条诊断编译行**都**带 `-Werror` ⇒ 违例行 **0** ⇒ 允许上规则。

## 2 · 任务 1：声明↔flag 绑定（形状与关键设计发现）

**关键发现（与提示词设想不同，必须先说）**：提示词假设 M3 是"被删去 `-Werror`"⇒ 简单包含检查即可。
实测 M3 算子 `text.replace("-Werror", "", 1)` **只删第一条出现** ⇒ 整卡**仍然含** `-Werror`
⇒ "整卡包含"式规则**抓不到这个变异**，P11 也照样不响（它同样只看整卡）。

⇒ 落地的窄形状：
* 只在**判据声明里出现 `-Werror`** 的卡上生效（判据性指纹，见 §1）；
* 对其 `command` 里**每一条带诊断开关（`-Wall`/`-Wextra`）的编译行**逐个绑定 —— 缺 `-Werror`
  即违例（这才抓得住"三条里删一条"）；
* 出 **warn**（不 block，541 教训）；与 P11 **单点互斥**（P11 已对该卡 block 时不再叠 warn）。

**实测**：
| 指标 | 改前 | 改后 |
|---|---|---|
| gate 规则数 / 命中 | 61 / **141（block=0 warn=136 advice=5）** | 62 / **141（block=0 warn=136 advice=5）** ← 命中逐字未变 = 零误伤 |
| M3 全量 87 变体（83 卡，6.96s） | 逃逸 **1**（`EV-LANG-001` 的 `-Werror` 变体） | 逃逸 **0**；**唯一变化**就是那一条：`escaped → blocked`（`kind=warn_only`，`new_warn=['EV-WERROR-DECL-BIND:…']`） |
| poison | 108/108 | **110/110**（+`P71` ✅ +`P71-阴` ✅ 阴性对照）· RULE-COVERAGE 37/62 |

## 3 · 任务 2：ruff 钉 select

`[tool.ruff.lint] select = ["E4","E7","E9","F"]`（568 已清零的那套）。
钉后 `ruff check tools/ tests/` ⇒ **All checks passed!**。
**为何必须钉**：此前无 `select` ⇒ 告警数随版本漂移（本机 0.16.5 报 914 项 vs 经典默认集 22 项），
"存量债"没有可复现口径。其余规则（I/SIM/UP/BLE/…）另开一批分批 `--fix` + 人审（本批不做）。

## 4 · 意外收获：569 的退出自检**一直是静默空转**（已修）

* ruff 的 `F821 Undefined name subprocess` 抓到：569 的 `_controlled_dirty()` 用了 `subprocess`
  但模块**没 import** ⇒ `NameError` 被裸 `except Exception` 吞掉 ⇒ 该函数**永远返回 `[]`**，
  即"自检永远绿"。**这正是 567 立规矩要防的"没查成却像查过"**，而且是我自己在 569 写下的。
* 改法：补 `import subprocess`；`except` 收窄到 `(OSError, subprocess.SubprocessError)`
  —— **环境类故障容错，代码错误必须冒出来**（否则下一次还会静默）。
* 新增回归锁：mock `subprocess.run` 验"真实现真调 git 并解析 stdout"/非 0 返回码放行/
  环境故障容错/**NameError 必须抛**。
* 教训（写进交人项）：**自检/护栏代码不许用裸 `except Exception`**；护栏的"绿"必须能被证伪。

## 5 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **逃逸机制**：提示词说"被 M3 删去 `-Werror`"（像全删）；实测 M3 只删**第一条** ⇒ 规则必须做成
   **逐诊断编译行绑定**才收得住（§2）。若照提示词做"整卡包含"检查，本批会**假绿**（变异仍逃逸）。
2. **EV-CONC-006**：提示词未预料到"按措辞匹配"会命中 TSan 运行时串 ⇒ 无"逐条解释的存量误伤"，
   而是**直接把误报源否掉**（不采用宽匹配），从而做到真的 0 误伤。
3. **poison 计数**：提示词预计"若加毒样例则 109"；实测 **110**（除 `P71` 还加了阴性对照
   `P71-阴`——防误伤的正反例缺一不可）。
4. **gate 规则数**：61 → **62**（新增一条规则）；**命中数 141 与 block/warn/advice 分布逐字未变**
   （提示词写的"61/141"里 61 是规则数，本批只改规则数、不改命中）。
5. **多了一个 commit**（`82c89ce`）：修 569 遗留的自检缺陷；与任务 1 同批发现、独立文件、独立提交。

## 6 · 收工验收（fresh）

见 `_acc570.log`（后台 fresh 跑，含 slow）+ 末尾复跑取退出码。取证纪律沿 567/568：**pytest 用退出码定论**。

| 项 | 实测 |
|---|---|
| 任务 0 两张表 + 误伤预估 | §1（误伤 = 0，逐条定性） |
| gate | `规则 62 条 · 命中 141 (block=0 warn=136 advice=5)` —— 命中逐字未变 |
| M3 逃逸 | **1 → 0**（逐值对比：仅 `EV-LANG-001/-Werror` 一条变化） |
| poison | **110/110** · 双指标 `100%(6/6) / 100%(2/2)` |
| replay | `confirm=56 refute=0 infra_error=0` |
| pytest fast / slow | **exit 0 / exit 0** |
| ruff | `All checks passed!`（select 已钉） |
| `tool_integrity.py --check` | exit 0（gate/poison 改后已重钉，同一 commit） |
| 受控目录 | `git diff --quiet -- evidence/ atoms/` exit 0（且自检已修真、不再空转） |

## 7 · 交人项

1. **护栏代码纪律（新增，血换的）**：任何自检/护栏**不许裸 `except Exception`**，且其"绿"
   必须有一条能被证伪的测试（本次 `_controlled_dirty` 静默空转即反例）。
2. **其余 ruff 规则**（914 项那套）另开一批，**先钉 select 已完成**，分批 `--fix` + 人审。
3. PoC#3/#4/#5（等 trae 564 规格）；`manifest` 信任边界仍在（`golden_lock check --no-reuse` 可对账）。
4. 本批未动的近似面（**登记不硬做**）：宽措辞类"声称 warning 级判据"（如
   "警告即失败/无告警"）若将来出现在**别的卡**上，本批的窄形状（声明含 `-Werror`）**不覆盖**——
   届时应先量存量再决定是否扩面。
