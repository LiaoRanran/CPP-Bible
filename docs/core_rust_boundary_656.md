# 核心 Rust 边界（656 B5 · **只做准备，不真翻译**）

> 任务书：核心边界冻结——列出核心函数清单 + 接口签名 + 不变量；说明哪些进 Rust、哪些留 Python、接口怎么定义。
> 本批**一行 Rust 都不写**：先把"要搬什么、搬过去怎么算对"冻结下来，翻译是后续批次的事。

## 一、先划清"核心"是谁

本仓叫"核心"的东西有好几层，搬运前必须先切清楚（否则会把文件 I/O 和纯逻辑一起搬走）：

| 层 | 模块 | 性质 | 本批是否纳入 Rust 候选 |
|---|---|---|---|
| 判决合成（纯） | `four_state_verdict_638.classify / _raw_state / has_boundary / boundary_of` | 纯函数：dict → dict，无 I/O | ✅ 主候选 |
| 四态半格（纯） | `tests/test_core_pbt_656.combine`（现仍在测试里，**应先下沉到内核**） | 纯：4 值 meet | ✅ 主候选 |
| 账本哈希链（纯 + 少量 I/O） | `decision_event_v2_626.DecisionEvent.compute_self_hash / validate / _payload`；`AuthorityLedger.append / verify_chain` | 哈希与校验纯；落盘是 I/O | ✅ 纯部分可搬，落盘留 Python |
| Merkle（纯） | `ledger_checkpoint_651.mth / inclusion_path / verify_inclusion / consistency_proof / verify_consistency` | 纯（RFC6962），**热**（每次 checkpoint 全树重算） | ✅ 主候选（性能收益最大） |
| 规则引擎（重 I/O） | `gate_engine`（3826 行、67 条规则，扫 `atoms/ evidence/ Examples/`） | 大量文件遍历 + front-matter 解析 | ❌ 留 Python（I/O 密集 + 规则频繁变更） |
| 卡解析（I/O） | `classify_card`（open + 正则抽字段） | I/O | ❌ 留 Python（只把"抽完字段后的 classify"搬走） |
| 报告 / CLI | 各 `write_report` / `main` | 格式化输出 | ❌ 留 Python |

## 二、函数清单 + 签名（冻结）

> 签名按**当前实测**抄录；改动本文件前请重跑 `python tools/core_profile_656.py` 与 `tests/test_core_*_656.py`。

### ① 四态（纯）

```text
has_boundary(rec: Map<String, Value>) -> bool
    # 边界三元组齐且格式合法：hash∈64hex、count>0（可转 int）、version 非空
    # 656 B3：非 dict 入参 ⇒ false（不再抛 AttributeError）

_raw_state(rec) -> State            # 私有：原始判决词 → {pass|pass_with_exception|fail|unknown}

classify(rec: Map<String, Value>) -> {
    state: State, requested: State, downgraded: bool,
    boundary_ok: bool, reasons: Vec<String>
}
    # 不变量：先看边界，再定态；缺边界一律降级 unknown（P6 单调性）
    # 不变量：pass_with_exception 缺 explanation ⇒ 降级 unknown

combine(a: State, b: State) -> State        # 半格 meet：worst-wins（P1/P2）
```

### ② 账本哈希链

```text
DecisionEvent._payload() -> String          # canonical JSON（sort_keys，排除 self_hash/event_id，空值字段不参与）
DecisionEvent.compute_self_hash() -> String # sha256("{prev_hash}|{payload}")
DecisionEvent.finalize(prev_hash, seq) -> Self   # 分配 seq/prev_hash/event_id/self_hash（幂等前置）
DecisionEvent.validate() -> Vec<String>     # 枚举 + 条件必填（MODIFY⇒modification、REPLACE⇒supersedes…）
DecisionEvent.from_dict_strict(d) -> Self   # 未知字段 / 缺必填 / 校验不过 ⇒ 抛错（新事件专用）
DecisionEvent.from_dict_lenient(d) -> Self  # 宽容（历史 452 条专用，重算哈希必须不变）

AuthorityLedger.append(event) -> String     # append-only；656 B3 起临界区显式加锁
AuthorityLedger.verify_chain() -> bool      # prev_hash 链 + 每条 self_hash 重算（P8/P9）
AuthorityLedger.get_current(type, id) -> Option<Event>   # 未被 supersede 的最后一条
```

### ③ Merkle（RFC6962，纯且热）

```text
mth(leaves: Vec<Vec<u8>>) -> Option<[u8;32]>        # 空 ⇒ None
inclusion_path(m, leaves) -> Vec<[u8;32]>           # 656 B3：空/越界 ⇒ []（原会无限递归）
verify_inclusion(m, n, leaf, proof, root) -> bool
consistency_proof(m, leaves) -> Vec<[u8;32]>
verify_consistency(m, n, proof, old_root, new_root) -> bool
```

## 三、进 Rust 的判据（三条，缺一不搬）

1. **纯**：输入 → 输出，不读盘、不依赖全局状态（否则 Rust 侧就要带一个文件系统，白搬）。
2. **热**：被 profile 证明确实花钱（见 `data/656_core_profile_report.md`；本批实测 `re.Pattern.search` 是头号热点，
   单卡端到端 0.59 ms 中大部分是**读盘 + 正则**；纯 `classify` 仅 0.002 ms）。
3. **有性质可锁**：655 B 的 INV-1…INV-15 与 656 B1 的 P1–P12 能直接写成 Rust 侧的属性测试
   （不变量能搬过去 ⇒ 才敢说"搬对了"）。

按这三条：**Merkle 组 + 四态组 + 哈希链纯部分** 进 Rust；**规则引擎 + 卡解析 + 报告** 留 Python。

## 四、接口怎么定义（两阶段，先可测再求快）

**阶段 1（推荐先做）：JSON-in / JSON-out 的 CLI 管道。**

```text
# Python 侧负责 I/O 与编排，Rust 侧只做纯计算
$ cppbible-core merkle-mth --leaves-file leaves.json        → {"root":"…"} | {"root":null}
$ cppbible-core merkle-inclusion --m 3 --leaves-file …      → {"proof":["…"]}
$ cppbible-core verdict-classify --rec-file rec.json        → {"state":"…","reasons":[…]}
$ cppbible-core event-self-hash --event-file event.json     → {"self_hash":"…"}
```

约定：
- 输入/输出都是 **UTF-8 JSON**；字节数组用 **hex 字符串**（避免 base64 与 JSON 转义的歧义）。
- 退出码：`0 = 成功`；`2 = 入参非法（含空/越界）`；`3 = 内部不一致（应不可能）`。
- **错误必须带原因字符串**：与四态的 `reasons` 同风格，禁止"静默失败"。
- 校验用**同一套 PBT**：把 `tests/test_core_pbt_656.py` 的 P1–P12 用 Rust 属性测试重跑一遍（proptest），
  再加上差分测试：随机 10⁴ 条记录，Python 与 Rust 的 `classify` / `mth` 输出必须**逐字节相同**。

**阶段 2（等阶段 1 稳定后再说）：PyO3 原生绑定。**

- 只在**真成为瓶颈**时做（阶段 1 的进程/JSON 开销约毫秒级，对本仓的批处理不是瓶颈）；
- 绑定层**不得**持有 Python 对象引用跨越 FFI 边界（GIL + 生命周期是事故源）；
- 仍保留阶段 1 的 CLI 作为**独立复核通道**：绑定与 CLI 两条路必须给出相同结果（互为交叉验证）。

## 五、不变量清单（搬过去必须仍然成立）

| # | 不变量 | 对应测试 |
|---|---|---|
| 1 | 判决合成：交换 / 结合 / 幂等 / 封闭（半格） | P1 |
| 2 | worst-wins：折叠结果 = 最坏分量 | P2 |
| 3 | 账本追加前缀保持（append-only） | P3 / P8 |
| 4 | Merkle：任意前缀可验 consistency + 全量 inclusion | P4 |
| 5 | 保护器标记置换不变 | P5 |
| 6 | 单调性（偏序：加担子不变好；`fail` 与 `unknown` **不可比**） | P6 |
| 7 | 冲突检测：确定性 + 规则顺序无关 | P7 |
| 8 | 哈希链：改任一事件任一字段 ⇒ `verify_chain` 必假 | P9 |
| 9 | 迁移合法集 = 655 B §2 的 6 类；`fail→pass` 只能人审 | P10 |
| 10 | 并发追加：不丢、seq 连续唯一、链成立 | P11 |
| 11 | 确定性 / 可重放：同输入 ⇒ 同 `self_hash` | P12 |
| 12 | 空 / 坏入参 ⇒ `unknown` 或空证明，**不抛异常** | B3 边界锁 |

## 六、本批**没做**的事（诚实登记）

1. **没写一行 Rust**（任务书明确只做准备）。
2. **没做绑定 / 构建管线**（不引入 maturin/cargo 到本仓；CI 仍是纯 Python）。
3. **没搬 `combine`**：它现在住在测试文件里（`tests/test_core_pbt_656.py`），
   真要搬得先**下沉到内核模块**（否则 Rust 侧没有"官方定义"可对齐）⇒ 列为后续批次的第一步。
4. **性能收益未实测**：Rust 的收益是按 profile 推断的（Merkle 全树重算、大批量 classify）；
   要拿数字，得等阶段 1 的 CLI 出来后跑差分基准。**本批不宣称"Rust 会快多少倍"**。

---
_656 B5 产物。配套：`data/656_core_profile_report.{md,json}`（B4 实测）、
`tests/test_core_pbt_656.py`（P1–P12）、`tests/test_core_boundary_656.py`（边界锁）、
`tools/mutation_test_656.py`（B2 检出率）。_
