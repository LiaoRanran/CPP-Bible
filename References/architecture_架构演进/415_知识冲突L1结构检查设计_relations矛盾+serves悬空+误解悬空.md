# 415 知识冲突 L1 结构检查设计：relations 矛盾 + serves 悬空 + 误解悬空

> 日期：2026-09-13。衔接：404 §四（知识冲突 L1/L2/L3，当前 L1 几乎空白）、409 §二（攻击面 A7 符号映射缺失 / A9 规则逃逸）、413 §二（E4 内容错误需人审，E1/E2 机械）、414 P1-8（F07：relations 纯标量静默丢弃）。
> 核心问题：**知识库自己跟自己矛盾，机器现在基本看不见**。404 知识健康维列了 5 个指标（原子间冲突、重复原子、误解-原子对应率、relations 完整性、过期原子），但 gate 当前只有零星光点，没有成体系的 L1 结构冲突检测。402 对抗暴露的 F07 更说明 relations 解析本身就有盲区。

---

## 一、定位：L1 是零-LLM 结构层，当前几乎空白

404 定义的三层检测（从轻到重）：
- **L1 结构冲突**（零 LLM，可机器检测）——本次设计范围
- **L2 语义冲突**（LLM/嵌入辅助，需人确认）——不在本次
- **L3 跨模态冲突**（claim 数字 vs 工件实测）——不在本次

L1 的判断标准（与 413 错误分类对齐）：
- **机械可判** → 属于 L1，应交机器（gate 规则）。
- **需要判断"哪句 claim 对"** → 属于 E4 内容错误，必须人审/红队，**不进 L1**。

本设计的纪律：**只做结构层，不做语义层**。任何需要读 claim 文本比对的矛盾，一律定为 L2，留给红队。

---

## 二、现状盘点（先确认什么已经有了）

实读 `tools/gate_engine.py`（`DAG_REL`、规则注册表、`_relations_norm`）：

| 检测点 | 既有规则 | 级别 | 状态 | 缺口 |
|---|---|---|---|---|
| 误解悬空（原子引用不存在的 MIS-*） | `ATOM-MISCONCEPTION-REF` | **block** | ✅ 已实现 | 无（D3 完成） |
| serves 悬空（证据卡 serves 的原子不存在） | `EV-SERVES-EXIST` | warn | ✅ 已实现 | 仅存在性；缺"完整性"视角 |
| 关系目标存在 | `ATOM-REL-TARGET` | warn | ✅ 已实现 | 无 |
| DAG 无环 | `ATOM-REL-DAG` | block | ✅ 已实现 | 无 |
| 前置可读声明一致 | `ATOM-PREREQ-READABLE` | warn | ✅ 已实现 | 无 |
| **relations 矛盾（A 依赖 B，B 却与 A 冲突）** | —— | —— | 🔴 **完全空白** | 无 `contradicts` 类型、无冲突规则 |
| relations 纯标量静默丢弃 | —— | —— | 🔴 盲区（F07） | 414 P1-8 修（warn） |

**结论**：用户给的三个检测点里，**D3（误解悬空）早已实现**（block 级），**D2（serves 悬空）存在性已覆盖**（warn），只有 **D1（relations 矛盾）是真正的空白**，且它依赖 schema 扩展。所以 415 的重心是 D1，D2/D3 做补强与确认。

关键事实：`DAG_REL = {"prerequisite", "specializes", "realizes", "evolved_from"}`，**不含 `contradicts`/`conflicts_with`**。要检测"矛盾"，必须先把"冲突"变成一等关系类型。

---

## 三、三个检测点设计（machine criterion 直给）

### D1 relations 矛盾 —— 新增（block 级，零 LLM）

**为什么必须 schema 扩展**：当前关系只有"支持型"（prereq/specializes/realizes/evolved_from）。"A 的 prereq=B 但 B 与 A 矛盾"这种对立关系，没有承载它的类型，所以机器根本无从中立地表达，自然检测不到。补一个"冲突型"关系即可机械判定。

**① schema 扩展（加性变更，不破坏存量）**
- 在 `gate_engine.py` 新增 `CONFLICT_REL = {"contradicts", "conflicts_with"}`（与 `DAG_REL` 并列）。
- 扩展 `_relations_norm()`：对 mapping-form `- contradicts: ATOM-X` 也归一为 `{"type": "contradicts", "target": "ATOM-X"}`（当前只处理 `DAG_REL`，纯标量项 `continue` 跳过——这正是 F07 的盲区，414 P1-8 会补纯标量 warn）。

**② 新规则 `ATOM-REL-CONFLICT`（block）** —— 机器判据（伪代码，苦力可直接转代码）：

```python
def check_relations_conflict() -> list[Finding]:
    support, conflict = defaultdict(dict), defaultdict(dict)
    for p in _cards(ATOMS, "ATOM-*.md"):
        aid = id_of(p)
        for rel in _relations_norm(_meta(p)):
            t, g = rel.get("type"), rel.get("target")
            if t in DAG_REL:      support[aid][g] = t
            elif t in CONFLICT_REL: conflict[aid][g] = t
    out = []
    for a in support:
        for b, st in support[a].items():           # a 支持/依赖 b
            # 情况1：b 反过来声明与 a 冲突 → 直接矛盾
            if conflict.get(b, {}).get(a):
                out.append(Finding("ATOM-REL-CONFLICT", "block", _rel(owner[a]),
                    f"{a} {st} {b}，但 {b} 声明 contradicts {a}（关系自相矛盾）",
                    "拆分原子或修正其中一条 relations"))
            # 情况2：a 自己既支持 b 又声明与 b 冲突 → 自相矛盾
            if conflict.get(a, {}).get(b):
                out.append(Finding("ATOM-REL-CONFLICT", "block", _rel(owner[a]),
                    f"{a} 同时 {st} 且 contradicts {b}（自身关系矛盾）",
                    "删除其中一条 relations"))
    return out
```

**③ 验收（给苦力）**
- 毒样例 P29：`ATOM-A` 有 `relations: [{type: prerequisite, target: ATOM-B}]`，`ATOM-B` 有 `relations: [{type: contradicts, target: ATOM-A}]` → gate block。
- 毒样例 P30（阴）：`ATOM-C` 有 `contradicts: ATOM-D`，但两者无其他关系 → 放行（单条冲突声明本身合法，只是记录分歧）。
- pytest：test_relations_conflict（3 例：矛盾 block / 单声明放行 / 自相矛盾 block）。
- 存量 27 颗原子 0 误伤（warn 数不增）。

**④ 边界（明确不归 L1）**：404 说的"A 是 B 的 prereq，但 B 的 claim 说'不依赖 A'"——这是 claim 文本矛盾，属 **L2 语义层**，不进 `ATOM-REL-CONFLICT`。本规则只认"关系类型对立"，不读 claim。

### D2 serves 悬空 —— 补强（存在性已覆盖，加完整性视角）

- **存在性**：`EV-SERVES-EXIST`（warn）已覆盖"证据卡 serves 的原子不存在"。保持 warn（未锻造的原子是合法债务，G4 锻造后自动清零），**不升 block**。
- **完整性（新增 advice 级，可选）**：`serves` 指向的原子/概念，其对应主题应在误解库中有至少 1 条 `MIS-*` 记录（即"这个知识点有被记录的典型误解"）。若无 → advice（"该 served 概念无对应误解条目，知识封装可能不完整"）。这是 404「误解-原子对应率 ≥80%」指标的机器可算部分，零 LLM。

### D3 误解悬空 —— 已建（确认，无新工作）

- `ATOM-MISCONCEPTION-REF`（block）已实现：原子 `misconceptions: [MIS-X]` 中任一 ID 在 `misconceptions/` 找不到文件 → block。
- **可选补强（反向）**：`misconceptions/` 里某条 `MIS-X` 被零原子引用 → advice（"孤儿误解，可能该纳入某原子或下线"）。属知识健康维「误解-原子对应率」另一半，零 LLM。

---

## 四、与对抗 / 错误分类的关系

- **409 攻击面**：D1 属于 A9（规则逃逸）的"建设期"补强——relations 解析盲区（F07）曾让规则逃逸，D1 把"关系自相矛盾"变成可被门禁拦的硬错误。
- **413 错误分类**：L1 结构冲突 = E1/E2 机械层（自动可检）；若冲突是"claim 内容方向反"（如 ALLOC-002 "pool 32B 最省"），那是 **E4 内容错误**，必须人审/红队，**不进 L1**。本设计严格守住这条线。
- **413 Writer 自检层（P0）**：D1/D2/D3 的机器判据可直接塞进 `tools/writer_selfcheck.py` 的自检清单（确定性检查，零 token），在错误进红队前拦住。

---

## 五、与 414（F07）的衔接

- 414 P1-8 修 F07：relations 纯标量项（如 `relations: [PERF-001]`）当前被 `_relations_norm` 的 `continue` 静默丢弃 → 改 warn（`test_relations_scalar`）。这是**解析健壮性**，修的是"看不见的关系"。
- 415 D1 修的是"看见了但没比对的关系矛盾"。两者互补：**414 让关系进入视野，415 让关系互相校验**。建议 414 先合（F07 是 P1），本设计的 `ATOM-REL-CONFLICT` 作为下一轮苦力批次（见六），复用 414 已扩展的 `_relations_norm` 入口。

---

## 六、落地优先级

| 优先级 | 项 | 性质 | 依赖 |
|---|---|---|---|
| **P0** | `ATOM-REL-CONFLICT`（D1）schema 扩展 + 规则 + 毒样例 + pytest | 新能力，零 LLM | 414 P1-8 的 `_relations_norm` 扩展先合 |
| **P1** | D2 完整性 advice（served 概念无 MIS 对应） | 加性，低风险 | 误解库索引可枚举 |
| **P1** | D3 反向 advice（孤儿误解无原子引用） | 加性，低风险 | 无 |
| **P2** | 把 D1/D2/D3 判据并入 `writer_selfcheck.py` 自检清单 | 复用，零风险 | 413 P0 工具落地 |
| **P2** | L2 语义冲突（claim 文本比对）→ 红队/LLM | 需嵌入或 LLM | 环境支持 |

**投喂苦力注意（重要）**：苦力 Agent 上下文未同步，投喂时必须写入**「重读磁盘」指令**——先 `Read tools/gate_engine.py` 确认当前 `DAG_REL`、`_relations_norm`、规则注册表的实际内容（尤其 414 是否已合 F07），再动手改；禁止凭历史上下文里的旧 schema 写代码。relations 是 402/414 反复出盲区的字段，必须以磁盘真实状态为准。

---

## 七、元结论

知识库"自己打自己脸"是 404 知识健康维最该被看见、却最看不见的一类问题。好消息是：**三个检测点里两个早已实现**，真正的空白只有一个——relations 矛盾，而它只需一次加性的 schema 扩展（`contradicts` 类型 + 一条 block 规则）即可机械堵住，零 LLM、零语义判断。

402 对抗的 F07 已经证明 relations 解析有盲区；415 把盲区从"看不见"推进到"看得见还能互相校验"。这比任何语义层检测都便宜、都可靠，是 404 知识健康维最该先落的一砖。

**下一步**：414（F07 + 三 P0 阻断）优先投喂苦力执行（P0 三阻断是 CI 硬门禁失效，比调研紧急）；`ATOM-REL-CONFLICT` 作为紧随其后的苦力批次，复用 414 已扩展的 relations 解析入口。

累计 40 份（374-415）。
