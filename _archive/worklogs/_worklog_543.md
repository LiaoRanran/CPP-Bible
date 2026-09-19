# 543 建设日志：P0 字段修正 + P1 合法性闸落地（gate 零改动）；P2 重算完成，P3/P4 未做

> 依据：`References/architecture_架构演进/543_进化闭环三修正_修mutation算子schema+变体合法性闸.md`
> 纪律：不 push / 不 golden accept / **本批主战场是修 mutation 自己、gate 原则上不动**（实际零改动）/ 变异只在 tempfile / 做不完停在 P 边界。

## 幂等进度看板

```
P0 mutation 算子字段正确性（M4 用复数 texts）   [x] 205a377
P1 变体合法性闸 n_a(malformed) + 回归锁         [x] 205a377 + e4d476e（测试注入位置修正）
P2 重算真实拦截率（escaped 12 → 10）           [x] 本文件 §3（报告 data/mutation/after_543.json）
P3 M3 区间降级真洞（可轻触 gate）               [ ] 未做（原因见 §4）
P4 mutation 按卡批性能 + cppbible 接入          [ ] 未做
```

## 0. 开工基线（HEAD=`f034d2c`，亲手实测）

`gate 60 规则 · 141 命中 (block=0 warn=136 advice=5)` · `poison 90/90` · `replay confirm=56` · fast pytest 280（+ slow 组 mutation 5 例）· mutation smoke（`--limit 2 --operators M2,M3,M4,M5,M6`）：变体 28 / blocked 14（严格 13）/ escaped 12 / n_a 2（**M2×6 · M3×4 · M4×2**）。

## 1. P0 · 算子字段审计表（`_assert_targets` 口径对齐）

| 算子 | 产出/改写的 kind | 使用的字段 | 对不对 |
|---|---|---|---|
| M1 字段删除 | 不改 kind，只删整键（`artifact_sha256`/`run_match_file`/`negative_controls`/`signed_by`） | — | ✅（删的是键本身，不涉 kind→字段映射） |
| M2 路径变形 | 不改断言，只改路径字面量 | — | ✅ |
| M3 断言弱化 | `contains_in`→`contains`、`absent_in`→`absent`（改 kind 名） | 原条目的 `text` 保留 | ✅ **形态合法**（`contains/absent` 读单数 `text` ✓）——所以它造出的是**真逃逸**不是假逃逸 |
| M4 恒真注入 | 新造 4 条：3 条 `contains_in`（`symbol: main/call`，`text: main/ret/.p2align`）+ 1 条 `contains_any` | 曾用 `symbol+text` ✗ → 现改 `symbol+texts: ['.file']` | **原为 ✗（假逃逸源），P0 已修 ✅** |
| M5 claim 自标 | 不改断言（改 `claim_type`） | — | ✅ |
| M6 YAML 变形 | 不改断言（改键形态/缩进） | — | ✅ |
| M7 数值/哈希 | 不改断言（改 sha/数字） | — | ✅ |

**映射权威（与 `gate_engine._assert_targets` 一致，已写成常量 `KIND_FIELD`）**：
`contains/absent → text`、`contains_any/absent_any → **texts（列表）**`、`contains_in/absent_in → symbol`、`call_count → symbols`。

## 2. P1 · 变体合法性闸（防假逃逸污染拦截率）

- 新增 `KIND_FIELD` + `_malformed_asserts(meta)`：逐条 `artifact_assert` 校验"该 kind 的取值字段非空"；
- `classify()` 在**解析成功后立即**自检，畸形 ⇒ `{"verdict": "n_a", "malformed": True, "why": "畸形变体（artifact_assert 字段不合规）：…"}`——**既不算 blocked 也不算 escaped、不进拦截率分子/分母**；
- 报告单列 `malformed` 计数（与"解析失败/infra"的 n_a 区分标注）；
- 回归锁 `tests/test_mutation_fuzz.py::test_malformed_variant_falls_into_n_a_not_escaped`（畸形落 n_a(malformed) + 合法形态不被误判 + 映射表契约）与 `test_m4_uses_correct_fields`（M4 每条断言字段合法、`contains_any` 必须用 `texts`）。
- **测试自身的坑（已修，`e4d476e`）**：把畸形条目插到 frontmatter **末尾**会被最后那个 block scalar（`falsification: >-`）**吞掉** ⇒ parse 后不在 `artifact_assert` 里，用例误判成 blocked。必须插在 **`artifact_assert:` 块头之后**（与 `mut_m4` 同一位置），已写进注释。

## 3. P2 · 重算真实拦截率（闭环证据，报告 `data/mutation/after_543.json`）

`--limit 2 --operators M2,M3,M4,M5,M6`：

| 指标 | 修前（541 开工口径） | 修后 | 说明 |
|---|---|---|---|
| 变体 | 28 | 28 | 口径不变 |
| blocked | 14（严格 13） | **16（严格 14）** | +2 = M4 两例改用合法 `texts` 后**被 gate 主路径 block** ✓ |
| escaped | **12** | **10** | **M4 的 2 例假逃逸消失** ✓（监工定性被闭环证实） |
| n_a | 2 | 2（malformed **0**） | M5 对证据卡的"不适用"；本批无畸形变体（算子已修） |
| 严格拦截率 | 46.2% | **~52.4%**（14/26） | 分母 = blocked+escaped = 26 |

**剩余 10 条 escaped 逐条定性（如实，不为数字好看改判）**：

| 卡 | 算子 | 变异点 | 定性 |
|---|---|---|---|
| EV-CONC-001 | M2 | 路径转大写 | **真洞（可移植性）**：Windows 能打开、Linux CI 找不到文件；无规则校验路径写法 |
| EV-CONC-001 | M2 | 路径加 `./` | 同上 |
| EV-CONC-001 | M2 | 分隔符换反斜杠 | 同上 |
| EV-CONC-002 | M2 | 同上三条 | 同上（该卡与 001 共用夹具） |
| EV-CONC-001 | M3 | `contains_in → contains`（区间→全文） | **真洞**：文本在全文有出处 ⇒ 放行，但"必须在 symbol 指定区间内"的约束**丢了**（P3 目标） |
| EV-CONC-002 | M3 | 同上 | 同上 |
| EV-CONC-001 | M3 | `absent_in → absent`（反向） | **真洞同类**：区间内"不存在"降级成全文"不存在"（更弱） |
| EV-CONC-002 | M3 | 同上 | 同上 |
| EV-CONC-001 | M4 | —（已收口） | ✅ 不再是逃逸 |
| EV-CONC-002 | M4 | —（已收口） | ✅ 不再是逃逸 |

> 结论：**M2/M3 这两类是真洞**（与 541 的两条线索一致）；M4 已闭环。

## 4. 未做与交人项

1. **P3（M3 区间降级真洞）未做**：它要求轻触 `gate_engine`；而 541 两次试验已实测证明 gate 侧"扩 kind 白名单"会撞存量（block 0→38）或与既有 block 路径重复命中（advice +3、2 个既有测试失败）。本会话预算见底，按纪律**不做**，避免为做它破坏 P0–P2。下一轮的正确形状（与 541 §1.3 一致）：**单点互斥判定**——只对"全文 `contains/absent` + text 是本机标签 + 丢了区间锚定"这一窄情形出 **warn**；空/纯中文 block 只对 `*_in`；先量存量命中；配正反例毒样例；改完 `tool_integrity.py --update` 重钉校验和。
2. **P4（按卡批性能 / cppbible 接入）未做**：543 已给出红线——跨卡规则（`EV-ID-UNIQUE`/`serves`/`relations`）下，只 diff `Finding.target == 本卡` 会漏跨卡逃逸，必须对变异副本单独判跨卡部分。
3. **M5 对证据卡恒为 n_a**（证据卡无 `claim_type`）：若要让 M5 有产出，需 `--cards atoms/**.md`（或让默认采样包含原子卡）。
4. **本批 commit**：`205a377`（P0+P1）、`e4d476e`（P1 测试注入位置修正）；本地 **ahead 18 个提交（未 push）**。
5. **门禁终值**：本批只改 `mutation_fuzz.py` 与 `tests/test_mutation_fuzz.py`，**未动 gate/poison/replay/卡** ⇒ `gate 60 · block=0 · warn=136 · advice=5`、`poison 90/90`、`replay confirm=56` 与本文件 §0 开工基线逐字一致（未复跑整轮，理由：改动面不含这些链路；已复跑项：`tests/test_mutation_fuzz.py` **7 passed**、ruff 0.6.9 全过、P2 mutation 报告已落盘）。
