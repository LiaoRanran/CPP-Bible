# 614 D1：M1 逃逸根因分析（唯一 escaped）

> 铁律：不臆造"已修复"；数字以基线文件为准。基线 = `data/mutation/full_baseline_v7.json`（591 冻结）。

## 一、逃逸事实（基线原文）
```
escaped_list = [{
  "card": "evidence/conc/EV-CONC-001.md",
  "op": "M1",
  "point": "删 negative_controls",
  "verdict": "escaped",
  "new_block": [], "new_warn": [],
  "replay": "confirm",
  "equivalent": false
}]
```
- 全量：变体 1593 · blocked 1405 · **escaped 1** · n_a 179 · malformed 0 · equivalent_invalid 8 · 可判分母 1406。
- 分算子：`M1 = {blocked: 64, escaped: 1, n_a: 27}`（M1 可判 65）。
- 基线 `notes`：**"唯一 escaped=1 = M1 / EV-CONC-001 / 删 negative_controls（冻结 TCE）"**。

## 二、M1 算子语义
`mutation_fuzz.py`：`M1 = 字段删除（artifact_sha256 / run_match_file / negative_controls / signed_by）`；
且 **M1 属 `REPLAY_OPS`**（判决需真跑 replay 读**工件与命令**）。
本逃逸的变异点是「**整段删除 `negative_controls` 键**」（EV-CONC-001.md 该字段原为块式序列，L53 起）。

## 三、根因（为何门禁+replay 都漏）
| 检测点 | 是否覆盖"键被删" | 说明 |
|---|---|---|
| `EV-FM-REQUIRED`（证据卡必填） | ❌ **不覆盖** | `EV_REQUIRED = (id, serves, hypothesis, command, fixture, artifact, artifact_sha256, actual)`——**不含 `negative_controls`**；删它不影响其余必填 ⇒ 不触发。 |
| `EV-FM-YAML-HARDENING [nc-form]` | ❌ **空转** | 该规则**仅在 `negative_controls` 键存在时**校验形态（flow/map/scalar ⇒ block）；键被删 ⇒ `_NC_KEY_LINE` 不匹配 ⇒ 无命中。 |
| replay `check_negative_controls` | ❌ **缺省即过** | 该检查要求**存在时为 block 列表**；字段缺失时 replay 仍返回 **`confirm`**（基线实测 `replay":"confirm"`）⇒ 无 refute。 |
| 结论 | — | **无新 block、无新 warn、replay confirm ⇒ 判 `escaped`**。 |

⇒ 根因是**「负对照字段的**存在性**」无人负责**：gate 只验"有则形态"，replay 只验"有则内容"，**没有任何一层验"必须有"**。

## 四、为何属"结构性"而非"可修 bug"
1. **修法 A（把 `negative_controls` 加进 `EV_REQUIRED`）被**零误伤**否决**：存量证据卡中**并非每张都写 negative_controls**
   ⇒ 直接新增 **block 命中**（`EV-FM-REQUIRED`）⇒ 违反铁律「block 不新增、存量零误伤」。
2. **修法 B（TCE 式产物/负对照比对）是冻结项**：M1/M7 的判决需**读 replay 工件与命令**做**TCE 式比对**
   （`full_baseline_v7` 明确「冻结 TCE」；`mutation_fuzz.py` 注释亦载「需要 TCE 式产物比对，属冻结项 W2」）。
   ⇒ 未实现前，M1 的"删字段"检测**结构上不可能**由现有 gate/replay 覆盖。
3. ⇒ 该逃逸是**已知、可解释、结构性**的，**不是**活雷（活雷需 new_block/new_warn 全空但**本应**被判出的**逻辑漏洞**）。

## 五、判定与去向
- **性质**：known structural escape（已知结构性逃逸），**非**活雷。
- **处置**：D2 做**结构性登记**（`data/known_tce.jsonl` + gate 规则豁免标注 + metrics 反映），**不**改 gate 行为（避免破坏冻结基线）。
- **诚实口径**：逃逸率契约**仍为 1/1406**；报告须注明"该 1 为已登记的冻结 TCE"，**不得**宣称"0 逃逸"。

## 六、复现
```
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards evidence/conc/EV-CONC-001.md --operators M1 --limit 1
```
（按铁律，本批**未**重跑 mutation 监工门禁；结论取自冻结基线 v7。）
