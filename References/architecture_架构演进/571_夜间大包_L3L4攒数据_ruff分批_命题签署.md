# 571 · 夜间大包：L3/L4 攒数据 + 收口（一次干完四件，不等中间确认）

承接 `82c89ce`（570，监工已亲验 M3 逃逸 0、自检静默空转修复）。解释器只用 `.venv\Scripts\python.exe`；**一任务一 commit；做不完停在任务边界、不留半成品；不 push、不 golden accept**。本批四个任务相对独立，串行做完；每个任务都先量后动、warn 起步、存量零误伤。中间不要等人，按回退条件自行取舍。

---
## 任务 1（L3 攒数据，核心）：mutation 补样 + 全量逃逸基线 v2
现状（570 亲测）：M3 可判样本只有 7 < 59 ⇒ 诚实标注"样本不足、不宣称率"。这堵死了"错误率有上界"这个核心卖点。
1. 先量：为什么 M3 只有 7 个可判变体？哪些卡/断言让 M3 变异落进 n_a（out_of_scope）？
2. **扩大可判面**（不改 gate 判定逻辑）：让 M3 能对更多卡的断言产生"可判"变异（例如更多卡有区间锚定断言、更多 run 型断言），目标 **M3 可判样本 ≥ 59**。
3. 重跑全量 mutation，出 `data/mutation/full_baseline_v2.json`：按算子给 blocked/escaped/n_a、严格拦截率、含 warn 处置率、C-P 95% 区间（用 tools/stat_bounds.py）。
4. 机器判据：v1→v2 逐算子对比贴数；逃逸必须仍能逐条定性（真洞 vs 无效变异）；**不许为了数字好看改判据口径**（分子分母定义沿用 565b 口径：可判分母 = blocked+escaped，warn_only 不入严格分子）。

## 任务 2（L4 实体，562 留的口子）：overturned 事件通道 + 三曲线实化
现状：`overturned` 恒 0（无产生路径）、三曲线只有 1 个时点（metrics 已埋字段但没人写事件）。
1. 建 `overturned_by_stronger_verifier` 事件的最小 schema（命题 id / 旧判决 / 新判决 / 推翻者版本 / 时间）——**只接"人或异族明确推翻"动作，系统绝不自动产生推翻**（自动 LLM 推翻在战略冻结档）。
2. 给 metrics 三曲线（mutation_escape_rate / overturned / escape_survival）接上真实写入路径：每跑一次全量 mutation 自动落一个时点；overturned 有人签推翻时落一个时点。
3. 机器判据：mock 一次"推翻"事件，三曲线 JSON 能读出该时点；escape_survival 在无数据时仍 null 不填 0；pytest 锁 schema。
4. 范围：只建事件通道和写入，**不做自动检测、不做 dashboard**。

## 任务 3（卫生）：ruff 914 项分批清
570 已钉 `select = ["E4","E7","E9","F"]`（22 项 0）。本批把其余规则**分批**引入：
1. 先按规则族出一份清单（哪些规则、多少命中、是否自动可修）；
2. 用 `ruff check --select <族> --fix` 自动修一批，**逐族 commit**；改完跑相关 pytest 确认无行为变化；
3. 不可自动修的列清单交人，不硬改逻辑。
4. 每引入一族都要 `ruff check tools/ tests/` 0 新增、相关测试绿；不许一次把 914 项全打开（会雪崩）。

## 任务 4（信任细化）：命题级 signed_by 最小骨架
现状：79 命题（obs50/inf29），命题级 signed_by 当前 0，全靠卡级人签兜底。
1. 给 claim_structured 的命题加可选 `signed_by` 字段（卡级 verified_by 仍兜底）；
2. gate 校验：命题级 signed_by 若存在，其名须与该文件最后 git 提交作者一致（复用卡级同款 principal_ok 逻辑）；
3. **只建 schema + 校验 + prop_graph 查询视图**，不自动签任何命题；现有 3 条未签命题（ATOM-LANG-INLINE-001/prop-1,2,3）仍只由人签，不代签。
4. 机器判据：pytest 正反例（命题级 signed_by 合法通过 / 冒名 block / 缺省仍靠卡级）；存量 79 命题不因新字段变红。

---
## 收工总验收（四个任务全做完后 fresh 跑）
- gate 62 条·命中逐字不新增存量（block=0）· poison 110/110 · replay confirm=56 · `--check` exit 0 · ruff 全过 · pytest fast/slow 全绿 · 受控目录零残留；
- 任务 1：full_baseline_v2.json 落盘 + M3 可判 ≥59 + C-P 区间贴数；
- 任务 2：mock 推翻事件三曲线可读；
- 任务 4：命题级 signed_by 正反例绿、存量命题不红；
- 改了 CORE_TOOLS（gate/replay/poison/toolchain/cppbible）就 `--update` 重钉同 commit 带上；
- 写 `_worklog_571.md`：每任务改前/改后贴数、偏差表、哪些做了哪些因回退条件停下。

## 硬纪律（违反即作废）
- 先量后动、warn 起步、存量零误伤；
- 任何护栏/自检不许裸 except Exception（570 刚抓过空转）；
- 不编数字、不抄旧账，所有率贴实跑；
- 不做：自动 KG 入库、自动 LLM 推翻、LLM-as-judge、PoC#3/#4/#5（等 trae）、golden fork 并行。
