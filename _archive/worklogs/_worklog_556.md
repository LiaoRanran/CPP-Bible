# _worklog_556 · 556 返工：554 验收两问题（B5 硬化补全 + stateful flaky 根治）

> 任务书：`References/architecture_架构演进/556_返工投喂词_554验收两问题_B5硬化补全nc非block形态_stateful_flaky根治.md`
> 解释器：`.venv\Scripts\python.exe`。纪律：一问题一 commit；不 push、不 --no-verify、不 golden accept；存量 56 卡零误伤。

---

## 一、开工复核（554 信任基线未破）

| 项 | 值 |
|---|---|
| `gate --check` | 规则 61 · 命中 141（block=0 warn=136 advice=5） |
| `replay --check` | confirm=56 refute=0 infra_error=0 |
| `poison` | 覆盖 11/11 · RULE-COVERAGE 36/61 + 豁免 27 |
| `git status`（受控） | 仅 pre-existing `EV-CONC-001.md M` |

---

## 二、问题 1（P0，确定性真盲区）· B5 硬化不完整 —— commit `d088f73`

### 根因证据（先读码，行号以磁盘为准）

- **复现**：`.venv\Scripts\python.exe -m pytest tests/test_parser_differential.py::test_no_gray_state_between_parsers -n0 --tb=short` → 稳定红。
- **shrink 出的反例**：`fm = 'negative_controls: 00000000'`。
  - 自定义 `parse_frontmatter` 解析为**字符串** `'00000000'`；PyYAML `safe_load` 解析为**整数** `0`（前导零）。
  - 两解析器对 `negative_controls` 分歧，但硬化层 `blocked=False` ⇒ 谓词"分歧必须显式 block"失败。
- **代码根因**：`tools/gate_engine.py::_fm_hardening_uncached`（原 L1332）只用正则
  `^\s*negative_controls\s*:\s*\[` 堵了 **flow 列表一种形态**。`negative_controls` 的合法形态只应是
  **块式序列**（键独占一行、行末无值，下一行起缩进 `- `），而 gate **不跑 replay** 的 schema 校验
  （`check_negative_controls`），于是裸标量 / inline map / flow 等**一切非块式形态**都给"干净"假象。

### 修法（照磁盘现状）

`_fm_hardening_uncached`：把"正则枚举 flow `[`"升级为**白名单形态判定**（新增 `_NC_KEY_LINE = re.compile(r"^\s*negative_controls\s*:\s*(.*)$")`）：

- 键行冒号后**无值 / 仅注释** ⇒ 合法块式起点（跳过）；
- 否则按 值首字符 `[` / `{` / 其他 ⇒ `nc-flow` / `nc-map` / `nc-scalar`，统一出
  **`[nc-form]` block**（rule_id 仍 `EV-FM-YAML-HARDENING`，message 区分三子类）；
- **作用域严格限定 `negative_controls` 一个键**（其他字段合法用 flow/标量不受影响——实测 `matrix: [GCC]` 零命中）；
- 仍在 `yaml_mod is None` 早退**之前**执行（无 pyyaml 环境同样拦）。

### 毒样例 + 台账

- `tools/poison_drill.py` 新增 **P43d（裸标量 nc）/ P43e（inline-map nc）**；并把 **P43b/c/d/e 登记进 `ATTACK_TYPES`**（P43b/d/e→A6、P43c 借品阴面→A2），消除未分类的 `A?`。
- 完整毒钻探：**96/96 全过**（原 92/92），覆盖 **11/11**，RULE-COVERAGE 分子 **36/61 不变**。
- 重写 `tools/poison_surface_map.json`（台账 92→96；A6 3→6、A2 10→11）+ `tool_integrity.py --update` 重钉 `tools/.tool_checksums`。
- T2 快照 `test_poison_surface_map_committed` 同步更新（**仅** A2/A6/drill 三项，因毒样例新增，**非回归洗白**）。
- T3 `tests/test_parser_differential.py`：把 `nc-map`/`nc-scalar` 纳入已知 block 信号；P3 泛化为**任一非块式 nc 必落对应 `[nc-*]`**；并登记**非门禁键 YAML 1.1 陷阱**（前导零 / yes-no-on-off / `~`）为**已知未覆盖面**（`xfail(strict=False)`，指向 556 §问题1-3，是否扩硬化另开任务）。

### 验收（问题 1）

- ✅ `test_no_gray_state_between_parsers` 转绿（该文件 4 passed + 1 xfail）；
- ✅ **EV-CONC-001 零命中**（全库唯一合法块式 nc 卡；实跑 `check_frontmatter_hardening` 全库 block=0 warn=0）；
- ✅ gate 规则 61 / block=0 / warn=136 / advice=5 **不变**；poison 96/96；RULE-COVERAGE 36/61 不变；
- ✅ `tool_integrity.py --update` 已重钉；ruff 0.6.9 **零新增**（仅存量 4 项：F541 / E741×2 / E401）。

---

## 三、问题 2（P1，flaky 必须根治）· stateful TestTQ —— commit `35f3cc2`

### 根因证据（本机复现并抓到原文，非猜测）

- **复现**：`pytest -m "not slow" -n auto` 连跑，第 2 轮即复现 → 原文：
  ```
  hypothesis.errors.FlakyStrategyDefinition: Inconsistent data generation!
  The second test case drew a different type of value than the first.
    first:  integer
    second: boolean
  ```
- **根因**：多个 `@rule` 的 `data.draw(...)` **取决于外部状态**（`self.claimed` / `self.known` 是否为空、
  `pick` 是否 None），于是同一 choice 前缀在不同 run 里产出的 **draw 序列长度/类型不同** ⇒ 类型错位。
  逐条：
  - `_pick`：`if not seq: return None` 在抽 `_IDX` **之前** ⇒ `self.claimed` 空时不抽；
  - `claim_task`：`if self.claimed and data.draw(st.booleans())` ⇒ 布尔抽取挂在集合非空上；
  - `enqueue_task`：依赖抽取 `if self.known:` 挂在集合非空上；
  - `terminal_task`：`action = data.draw(...)` 挂在 `pick is not None` 上。
  （这也解释了监工看到的"零步/teardown"最小步骤——错位发生在很早的 draw 序号。）

### 修法（**纯测试侧**，不改任何判定逻辑）

把每个 rule 的 draw **全部改为无条件、按固定顺序**执行；外部状态只决定"用哪个值"：

- `_pick` 始终先抽 `_IDX`，再按 `len(seq)` 取模（空则返回 None）；
- `claim_task` 的 `takeover / t_idx / o_idx / worker` 一律先抽；
- `enqueue_task` 的 `with_touch / touch_variant / k / dep_idxs` 一律先抽；
- `terminal_task` 的 `action` 提到守卫之前。
- draw 数量只随**先前的 choice**（如 `k`）变化，不随外部状态变化。

> 未改 `tools/task_queue.py`：根因在**测试的抽取结构**，不在 tq 的连接/WAL（`_connect` 每次新开、`finally` 关闭，无模块级单例；已读码证伪 spec §问题2 方向 1/3）。

### 验收（问题 2）

- ✅ `pytest -m "not slow" -n auto` **连续 5 轮全绿**（开发期实测 75/77/67/76/65 秒），单跑亦绿；
- ✅ 未用 `@pytest.mark.serial` / 未踢出 `-n auto` / 未降 `max_examples` / 未新增 suppress 掩盖；
- ✅ ruff 0.6.9 全过。

---

## 四、收工总验收（fresh run）

| 判据 | 结果 |
|---|---|
| `pytest -m "not slow" -n auto` | ✅ **连续 3 轮全绿**（开发期另 5 轮，共 8 轮无红） |
| `pytest -m slow -n0` | ⚠️ 仅 1 条 **pre-existing** `test_golden_lock_json`；deselect 后**全绿**（100%） |
| gate | ✅ 规则 61 · 命中 141（block=0 warn=136 advice=5） |
| poison | ✅ 96/96 全过 · 覆盖 11/11 · RULE-COVERAGE 36/61 + 27 豁免 |
| replay | ✅ confirm=56 refute=0 infra_error=0 |
| 受控目录 | ✅ 零污染（仅 pre-existing `EV-CONC-001.md M` 与未跟踪 `tools/env_check.py`） |
| 问题 1 / 问题 2 | ✅ 各自独立 commit：`d088f73` / `35f3cc2` |

---

## 五、交监工裁决（未自动做）

1. **`golden_lock` warn 59→136 的分类签署**（含 INFERENCE 28 条等四桶）何时安排 `--accept`：
   `test_golden_lock_json` 为 **pre-existing** 失败（golden 基线 warn 59，最后 accept 于 `67c1962`；
   其后 548/553 新增 gate 规则使实数达 136）——**开工前（c15614e）就已红**，与 554/556 无关，**未代签**。
   现只需一次人工 `python tools/golden_lock.py check --accept "<理由>" --classify "RID=real,..."`。
2. **是否为"前导零 / YAML 1.1 陷阱词"的跨键 parser divergence 单开一个硬化任务**：
   本批已把非门禁键的同类分歧登记为已知未覆盖（`test_non_gate_key_yaml11_trap_should_block`，xfail），
   **未扩大硬化改动面**（556 §问题1-3 明示）。
