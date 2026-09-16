# mutation 全量逃逸基线 v1（548 Part 1）

**这是第一份"全量"基线**——以前只有 `--limit 2` 的 smoke。数字全部来自实跑，
机器可读原报告在 `data/mutation/full_baseline_v1.json`（每个变体一行，含复现命令）。

- 生成命令：
  ```bat
  .venv\Scripts\python.exe tools/mutation_fuzz.py --cards all --operators M1,M2,M3,M4,M5,M6,M7 ^
      --limit 999 --report data/mutation/full_baseline_v1.json --progress
  ```
- 生成时 HEAD：`ed3dff3`（548 Part 0 之后）· 卡 **83** 张（56 张证据卡 + 27 张原子卡）·
  算子 **7** 类 · 变体 **1188** 个 · 全库扫描 `ge.run()` **957** 次 · replay **65** 次
  （门禁已拦而跳过 **139** 次）· 墙钟 **659.7s（11 分钟）**。

## 1. 口径（539 B2 三分类，不许把 n_a 当 blocked 凑拦截率）

| 类别 | 定义 | 进拦截率分母？ |
|---|---|---|
| `blocked` | 变异后**新增** block/refute，或新增 warn（后者记 `kind=warn_only`） | ✅ |
| `escaped` | 变异后**没有任何**新增 block/warn | ✅ |
| `n_a` | 该卡本就没有被变异的字段 / 变异文本 YAML 解析失败 / replay 落 `infra_error` | ❌ |
| `n_a(malformed)` | 变体自身不合法（按 kind 取不到断言 targets ⇒ 门禁会静默跳过） | ❌（n_a 里单列） |

两个率：
- **严格拦截率** = 严格 blocked（block/refute）÷ (blocked + escaped) = **64.33%**；
- **含 warn 处置率** = blocked（含 warn_only）÷ (blocked + escaped) = **76.26%**。

## 2. 总量

| 指标 | 数 |
|---|---|
| 变体 | 1188 |
| blocked | 729（其中严格 615，warn_only 114） |
| escaped | **227** |
| n_a | 232（**malformed 0**；232 条全部是"该卡本就没有被变异的字段"） |
| 严格拦截率 | 64.33% |
| 含 warn 处置率 | 76.26% |

## 3. 按算子

| 算子 | 变体 | blocked | escaped | n_a | 备注 |
|---|---|---|---|---|---|
| M1 字段删除 | 92 | 64 | 1 | 27 | 删 `artifact_sha256`/`run_match_file` 全被拦（gate+replay 双保险） |
| M2 路径变形 | 221 | **0** | **207** | 14 | **全逃逸**：三种路径异体写法无任何规则（→ Part 2 加 warn） |
| M3 断言弱化 | 88 | 2 | 11 | 75 | 区间断言降级 / 去 `-Werror` |
| M4 恒真注入 | 233 | 200 | 0 | 33 | 全拦（543 P0 修好字段后） |
| M5 claim 自标 | 83 | 0 | 0 | 83 | 证据/原子卡无 `claim_type` ⇒ 恒 n_a（算子对这批卡不适用） |
| M6 YAML 变形 | 332 | 324 | 8 | 0 | 8 条逃逸全是"块式 → flow 写法（matrix）" |
| M7 数值/哈希篡改 | 139 | 139 | 0 | 0 | 全拦（replay 重算 sha 兜住） |

## 4. 逃逸逐类定性（**不许把 malformed 混进逃逸率**；本轮 malformed = 0）

| 类 | 条数 | 卡数 | 形态 | 定性 | 收口方向 |
|---|---|---|---|---|---|
| **M2 跨平台路径异体** | 207 | 69 | `Examples/…cpp` → 全大写 / 加 `./` / 换反斜杠 | **真逃逸（可移植性）**：Windows 能打开、Linux CI 找不到文件；卡内路径写法**无任何规则约束** | Part 2：加 **warn 级**规则（不 block，避免撞存量） |
| **M3 区间断言降级** | 9 | 7 | `contains_in → contains`、`absent_in → absent` | **真逃逸（已知清单，543 已定性）**：文本在全文有出处 ⇒ 放行，"必须在 symbol 指定区间内"的约束被丢掉 | 等 V-iso / 单点互斥判定（541 已实测：直接扩 gate 会撞存量） |
| **M3 去 `-Werror`** | 2 | 2 | 编译告警不再算失败 | 真逃逸：命令形态降级无门禁 | 同上（等规则形态白名单） |
| **M6 块式 → flow（matrix）** | 8 | 8 | `matrix:` 块式列表改写成 `{a, b}` flow 写法 | **本轮新发现**：两个解析器都能读 flow，且**无规则要求块式** ⇒ 形态完全不受约束 | 交人裁决：是"允许 flow 写法"还是"要求块式"（属形态约定，不是事实缺陷） |
| **M1 删 `negative_controls`** | 1 | 1 | 删掉阴性对照字段 | 真逃逸：**阴性对照缺失无闸门**（只有"有没有"，没有"够不够/在不在"） | 等门禁规则（观察：目前仅 1 张卡有该字段） |

每卡逃逸数分布：**3 条 53 张 / 4 条 13 张 / 5 条 2 张 / 6 条 1 张**（共 69/83 张卡有逃逸；
其余 14 张是 M2 不适用或全被拦）。逃逸最多的卡：`EV-CONC-001`（6）、`EV-CONC-002`（5）、
`ATOM-LANG-INLINE-001`（5）。

## 5. 复跑与对账

```bat
REM 复跑全量（覆盖本报告）
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards all --limit 999 ^
    --report data/mutation/full_baseline_v2.json --progress

REM 与 v1 对账（逐变体 verdict/kind/规则 id，不许因提速而漂移）
.venv\Scripts\python.exe -c "import json;a=json.load(open('data/mutation/full_baseline_v1.json',encoding='utf-8'));b=json.load(open('data/mutation/full_baseline_v2.json',encoding='utf-8'));f=lambda r:[(x['card'],x['op'],x['point'],x['verdict'],x.get('kind')) for x in r['results']];print('identical', f(a)==f(b))"

REM 单卡单算子复现（报告里每条都带 reproduce 命令）
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards evidence/conc/EV-CONC-001.md ^
    --operators M3 --limit 1
```

## 6. 诚实边界

1. **M5 对这批卡恒 n_a**：证据卡/原子卡没有 `claim_type` 字段，M5 在这 83 张卡上**没有产出**；
   要让 M5 有意义，得换一批带 `claim_type` 的卡（或给算子加"无字段 ⇒ 造一个"的形态）。
2. **n_a 232 条全部是"无字段"**，没有一条是解析失败或 replay infra_error ⇒ 本轮**无假逃逸污染**。
3. **Part 2 会故意改变 M2 的结论**（207 条 escaped → blocked/warn_only）；收口结果见 §7，
   v1 保留作"加规则前"的对照。
4. 耗时 659.7s 是**改后**口径；改前同 `--limit 2` 样本实测 99.2s → 24.1s（4.1×），
   全量外推约 43 分钟（未实跑，避免烧 40 分钟机器）。

## 7. Part 2 收口后（M2 专项复跑，post-`CARD-PATH-NOT-CANONICAL`）

```bat
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards all --operators M2 --limit 999 ^
    --report data/mutation/m2_after_p2.json
```

| M2 | Part 2 之前（v1） | Part 2 之后 |
|---|---|---|
| blocked | 0 | **141**（全部 `warn_only`，严格 0——**故意不 block**：形态约定不是事实缺陷） |
| escaped | 207 | **66** |
| n_a | 14 | 14 |
| 含 warn 处置率 | 0% | **68.1%** |
| 耗时 | ≈9 分钟 | 122s（Part 0 提速 + 规则内目录列表缓存） |

**剩余 66 条不是新洞**：它们的变异点落在**注释/正文**里（M2 取"卡内第一个带 `/` 的路径"，
而 83 张卡里有 22 张的第一条路径在注释/正文中）——门禁**从不读**那些位置，改前改后都不会
有反应 ⇒ 属**"变异点无效"**（对门禁的无效提问），不许算成"门禁漏了 66 条"。
人工抽验：`evidence/conc/EV-CONC-001.md` 的路径写在 `# 可核对锚 1` 注释里，
`fixture:` 字段本身未被 M2 触及 ⇒ 该变异对任何规则都不可见。

> 这也是本批学到的口径教训：**"逃逸"必须分三类**——真逃逸 / malformed（已单列）/
> 变异点无效。把第三类混进去会虚高逃逸数，把注意力从真洞上引开。
