# _worklog_569 · 收口 mutation 自发现真洞 M3：区间锚定丢失（单点互斥判定）

> 任务书：`References/architecture_架构演进/569_M3区间锚定收口_单点互斥判定.md`
> 承接：`12d484d`（568）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付

| 任务 | 结论 | commit |
|---|---|---|
| 0 · T0 量清 | M3 两半已收口；**(b) 仍有 1 逃逸**（只登记） | 无代码（见 §1） |
| 1 · 单点互斥判定 | **不做**（T0 判断 (a) 已饱和；提示词授权） | — |
| 2 · 毒样例 + 复跑 | 补 `P70b`（absent 侧）+ M3 复跑对比 | `f583022`（见 §3） |
| 3 · mutation 退出自检 | 装饰器实现 + 4 例回归锁 | `51d8634` |

## 1 · 任务 0：M3 改前实测（**实跑，不抄 543 旧数**）

命令：`.venv\Scripts\python.exe tools/mutation_fuzz.py --cards all --operators M3 --limit 999 --progress`
（注意 `--limit` 默认 **5**；`--cards all` 不解除该上限——第一次只跑了 5 卡，已重跑）

**全量 83 卡 / 87 变体，耗时 7.25s，报告 `data/mutation/_569_t0full.json`**：

| 子情形 | 变体数 | 逃逸 | 结论 |
|---|---|---|---|
| (a) `contains_in → contains`（区间锚定丢失） | 3 | **0** | 已被 **558 B1** 的 `区间锚定已丢失` warn 收口 |
| (a) `absent_in → absent`（同上） | 3 | **0** | 同上（同一 warn 分支覆盖两 kind） |
| (b) 去 `-Werror` | 1 | **1** ✗ | `evidence/lang/EV-LANG-001.md` —— **未覆盖** |
| 面外（门禁读取面无弱化点） | 80 | — | `n_a(out_of_scope)`（558 B2 的诚实化口径） |

⇒ 按任务书第 3 条："若 T0 发现 M3 已被 558 全部收口（逃逸=0），**就不做任务 1**"。
**(a) 两个子情形的逃逸都是 0** ⇒ 任务 1（单点互斥判定）**不做**（未动 `gate_engine.py`，
`gate --check` 仍 `61/141 block=0 warn=136 advice=5`，存量零误伤是硬约束⇒零风险达成）。

### (b) 为什么没被既有 P11 拦住（读了规则正文）
`check_evidence_zero_diag_werror`（`gate_engine.py:2568` 起）只在**卡里有"零诊断措辞"**
（`falsification/expected/hypothesis/claim_boundary` 命中 `_ZERO_DIAG_RE`）时才要求 `command`
带 `-Werror`。`EV-LANG-001` 不属于"零诊断类"卡（它的 `-Werror` 是为别的主张服务的）
⇒ 删掉它**没有任何规则会命中**。这是一条真实逃逸，但它属**编译 flag 层**而非断言 kind 层，
本批形状覆盖不了 ⇒ 按任务书**只登记、不硬做**，交下一批（见 §5 交人项 1）。

## 2 · 任务 1：不做（附"如果要做"的边界，备下一批）

541 §1.3 的三条件（血换来的）已在读档中确认，若下一批要动，必须逐条遵守：
①非锚定 kind 的 warn 必须与既有"通用符号 ⇒ block"路径**单点互斥**（541 试验 2 因双命中打散 2 例）；
②**"空/纯中文 text ⇒ block" 只对 `contains_in/absent_in` 可达**，绝不扩到新 kind（541 试验 1：一扩 block 0→38）；
③严重度从 warn 起步、warn 增量>0 时逐条列卡 id 交人，不许直接升 block。
本批实测 (a) 已 0 逃逸 ⇒ 无新增规则的必要，也就没有任何存量误伤风险。

## 3 · 任务 2：毒样例 + 复跑对比

* 新增 `P70b`（`poison_drill.py`）：M3 的**另一半**——`absent` 残留 `symbol`（`absent_in→absent`
  降级形态）须被同一条 warn 抓住。实测：`命中 severity=['warn','warn'] ✅`。
* 既有的 `P70`（`contains` 侧）/ `P70-阴`（合法全文散文放行）保持 ✅。
* 攻击面分类登记 `("P70b ", "A3")`（不加就会落"未分类"）。
* **复跑对比**：T0（改前）6 变体 0 逃逸 → 收口后仍是 6 变体 0 逃逸（本批未改判定，故逐值不变；
  这部分是**回归锁**而非"修复验证"，因为修复发生在 558 B1，本批只是把它载荷化+登记）。
* `existing gate tests`：`tests/test_mutation_fuzz.py` 20 例全绿（**没有打散任何既有期望**；
  期间发现并修正一处：改名包装函数会让既有"文档字符串契约"测试红 ⇒ 改用装饰器 + 手动转存
  `__doc__/__wrapped__`，主体一行未动）。

## 4 · 任务 3：`run_fuzz` 退出自检（568 遗留）

* 实现：`_selfcheck_on_exit` 装饰器 —— 正常返回与异常路径都在 `finally` 里跑
  `git diff --name-only -- evidence/ atoms/`；有残留 ⇒ 打印逐文件清单 + `SystemExit(1)`（fail-loud）。
* **不盖错因**：已在传播异常时（`sys.exc_info()[0] is not None`）只报不抛 —— 护栏不得把真正错因替换掉。
* **不重排主体**：用装饰器而非把主体包进 `try/finally`（避免 60 行重缩进的风险），
  手动转存 `__name__/__doc__/__wrapped__` 以保住既有契约测试与 `inspect.getsource`。
* 回归锁 4 例：脏目录报红（exit 1 + 列出文件）/ 干净静默 / `inflight=True` 只报不抛 /
  异常路径仍报出；外加"真实受控目录零残留"的活体基线。

## 5 · 偏差表 + 交人项

1. **合并提交**：任务 2 与任务 3 各一个 commit（`poison_drill.py` 与 `mutation_fuzz.py` 文件边界干净），
   任务 0/1 无代码改动 ⇒ 无 commit。提示词"一任务一 commit"在本批等价于两个 commit（已在 message 写明）。
2. **任务 1 的跳过依据**：提示词写"若 M3 已被 558 全部收口（逃逸=0）就不做任务 1"——
   严格说 (b) 还有 1 条逃逸，但提示词第 4 条把 (b) 单列为"形状覆盖不了就只登记"，
   且任务 1 的形状（断言 kind 层）**不覆盖**编译 flag 层 ⇒ (a) 饱和即跳过，理由如上，未硬做。

### 交下一批（登记在案）
* **(b) 去 `-Werror` 逃逸（`EV-LANG-001`）**：属编译 flag 层。可能的收口形状（待设计，别急着上）：
  ①凡 `command` 带 `-Werror` 的卡，加一条"该 `-Werror` 必须是**声明过的**判据要素"（类似 P11 的反面）；
  ②或纳入 M3 复跑白名单并在 `--strict` 下报 warn。**注意**：任何新规则都要先量存量（541 的教训）。
* `ruff` 显式钉 `select`（568 交人项，仍然有效）。
* PoC#3/#4/#5 等 trae 564 规格。

## 6 · 收工验收（fresh）

后台 fresh 全量跑（`_acc569.log` / `_acc569.err`，含 slow）+ 末尾复跑取退出码。

| 项 | 实测 |
|---|---|
| `tool_integrity.py --check`（验收头尾各一次） | `OK：5 个核心工具与基准一致` **exit 0** |
| gate（**硬约束：存量零误伤**） | `规则 61 条 · 命中 141 (block=0 warn=136 advice=5)` —— 与改前**逐字相同**（本批未动 `gate_engine.py`） |
| poison | **108/108**（107 + 新增 P70b；P70 / P70b / P70-阴 三条全 ✅）· 双指标 `trap_block_rate=100% (6/6) · clean_pass_rate=100% (2/2)` |
| replay | `confirm=56 refute=0 infra_error=0 共 56 张卡` |
| pytest fast `-n auto` | **exit 0** |
| pytest slow `-n0`（含 stateful 7 例） | **exit 0** |
| 受控目录 | `git diff --quiet -- evidence/ atoms/` **exit 0**（且从本批起有 `_exit_selfcheck` 常驻盯着） |
| T0 M3 复跑（改前基线） | 83 卡 / 87 变体 / 7.25s：判 7 条 —— (a) 6 条全拦下（0 逃逸）、(b) 1 条逃逸（只登记）、面外 80 条 |

> 取证口径（沿 567/568）：pytest 一律用**退出码**定论（汇总行抓不到时不拿"没看到 failed"当绿）。
