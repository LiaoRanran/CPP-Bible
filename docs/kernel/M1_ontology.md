# G1.2 本体模型 M1（Ontology）

> 配套：`G1_knowledge_map.md`（域）、`G1_terminology.md`（词表）、`G1_layout.md`（落盘与模板）。
> 标注约定：`【事实】`已查证、`【设计】`本轮决策、`【待确认】`需后续验证。

## 1. 原子是什么（一句话定义）

**原子 = 一条可被独立证伪的断言 + 支撑它的证据集 + 五重剖面元数据。**
"独立"是关键词：这条断言要能**自己**被判对或判错，不需要先信另一条未验证的断言。

反面例子（不是原子）：
- "移动语义是 C++11 最重要的特性" —— 无法证伪（价值判断），不是断言。
- "std::vector 扩容时会重新分配" —— 可证伪，但没有限定"哪个标准版本/哪个实现"，断言边界模糊。
正面例子（是原子）：
- "`std::vector` 在 `push_back` 触发扩容时，既有元素的地址全部改变（libstdc++，C++17，-O2）" —— 可编译验证、边界明确。

## 2. 原子类型学（10 类）

每类给：判据 / 必填字段 / 一个真实候选（来自现存 147 章，便于 G5 试点取材）。

| # | 类型 | 判据 | 特有必填字段 | 真实候选 |
|---|---|---|---|---|
| 1 | 概念 concept | 回答"这是什么" | `definition`, `boundary`（不是什么） | 值类别（lvalue/rvalue/xvalue） |
| 2 | 机制 mechanism | 回答"它内部怎么运作" | `mechanism_steps`, `observable_effect` | vector 扩容的重新分配与元素迁移 |
| 3 | 规则 rule | 标准/规范的规定，可引条文 | `standard_ref`（ISO 条款号）, `scope` | copy elision 的强制省略条件 |
| 4 | 惯用法 idiom | 社区约定的写法，非标准强制 | `canonical_form`, `why_better_than` | RAII、pimpl、CRTP |
| 5 | 反模式 anti-pattern | 常见但有害的写法 | `harm`, `detection_signal`, `counter_example_id` | 返回局部变量地址 |
| 6 | 陷阱 pitfall | 容易误判的语义细节 | `misconception`, `truth`, `trigger_condition` | strict aliasing 下的类型双关 |
| 7 | 横向对比 contrast | 两个及以上方案的取舍 | `candidates[]`, `decision_matrix`, `when_to_choose` | `vector` vs `deque` |
| 8 | 版本演化 evolution | 随标准版本变化的语义 | `version_timeline[]`, `migration_note` | `auto_ptr` → `unique_ptr` |
| 9 | 决策判据 decision | 给读者的"怎么选"规则 | `criteria[]`, `decision_tree` | 何时用 `shared_ptr` 而非 `unique_ptr` |
| 10 | 受控实验 experiment | 以实验本身为主体的原子 | `hypothesis`, `controlled_vars`, `matrix`, `expected`, `actual` | 移动构造是否真的比拷贝省一次分配 |

**通用必填字段（所有类型）**：见 `G1_layout.md` 第 3 节 frontmatter 规范。其中五重剖面字段（`sources[]` / `evidence[]` / `superiority` / `depth` / `pedagogy`）**任何类型都不得为空**——这是"缺一不可"的落点。

## 3. 关系边（11 种，含方向与是否入学习路径 DAG）

| 关系 | 语义（A → B） | 方向 | 入 DAG? | 说明 |
|---|---|---|---|---|
| `prerequisite` | 理解 A 必须先理解 B | A→B | **是** | 学习路径主干边 |
| `specializes` | A 是 B 的特化/细化 | A→B | **是** | 如 `unique_ptr` specializes `智能指针` |
| `realizes` | A 是 B 的一种具体实现 | A→B | **是** | 如 libstdc++ 的 vector 实现 realizes `vector 扩容机制` |
| `evolved_from` | A 由 B 演化而来 | A→B | **是** | `unique_ptr` evolved_from `auto_ptr` |
| `supersedes` | A 取代 B（B 已过时/废弃） | A→B | 否 | 与 evolved_from 区别：supersedes 带"别再用 B"的规范性 |
| `equivalent` | A 与 B 语义等价（可替换） | 双向 | 否 | 如"`std::move(x)` ≡ `static_cast<std::remove_reference_t<decltype(x)>&&>(x)`"（标准 [expr.static.cast] 明文等价，可编译互证） |
| `contradicts` | A 与 B 结论冲突 | 双向 | 否 | **触发"争议档案"**（G2.2），必须人工仲裁 |
| `causes` | A 导致 B（因果，非先后） | A→B | 否 | 如"迭代器失效" causes "UB" |
| `contrasts` | A 与 B 对照（取舍关系） | 双向 | 否 | 横向对比原子的主边 |
| `misconceived_as` | A 常被误认为 B | A→B | 否 | 陷阱/反模式原子的主边，喂给"误解清单" |
| `refines_evidence` | A 的证据强化/削弱 B 的结论 | A→B | 否 | 证据层关系（L2），不是知识层 |

**学习路径 DAG** = `{prerequisite, specializes, realizes, evolved_from}` 四个关系的子图。
**必须无环**：环路意味着"要学会 A 得先学 B，而 B 又依赖 A"——这在教材里表示内容切分有问题，门禁应报错。其余 7 种关系允许成环（如 `contradicts` 天然可互相矛盾）。

## 4. 粒度判据（一原子 = 一可独立证伪断言）

自评 4 问（全答"是"才算切对）：
1. **可证伪**：存在一个实验，其结果能判这条断言为假吗？
2. **边界闭合**：标准版本、编译器、优化级别、平台是否都写清了？
3. **单断言**：这句话里是否只含一个"因为…所以…"？含两个就该拆。
4. **可独立**：验证它需要依赖另一条**未验证**的断言吗？若是，先做那条。

**切对的 2 例**：
- ✅ `ATOM-MEM-MOVE-001`："对含堆指针的类型，`std::move` 后源对象处于有效但未指定状态，析构安全但值不可依赖" —— 可编译验证（析构不崩）、边界明确（标准措辞）、单断言、不依赖别的未验证断言。
- ✅ `ATOM-UB-ALIAS-001`："用 `char*` 读取 `float` 对象的字节不违反严格别名规则，反向（用 `float*` 读 `char` 缓冲区）违反" —— 可用 `-fstrict-aliasing -Wstrict-aliasing` + 实际行为对照验证，方向明确不会二义。

**切错的 2 例**：
- ❌ "移动语义与完美转发" —— 两个机制塞一个原子，第 3 问不过。应为 `ATOM-MEM-MOVE-*` 与 `ATOM-MEM-FWD-*` 两组。
- ❌ "智能指针用起来很安全" —— 第 1 问不过（无法证伪，"安全"未定义）、第 2 问不过（哪种指针？什么场景？），且是个价值判断。应拆成可验证的机制断言，如"shared_ptr 的引用计数增减是原子的"。

## 5. 稳定 ID 与迁移

**格式**（用户 DRQ-3 定调 A）：`ATOM-{DOMAIN}-{SHORT_TOPIC}-{NNN}`
- `DOMAIN` ∈ 地图 16 域缩写（`MEM` / `UB` / `STL`…）
- `SHORT_TOPIC` 大写英文短词，如 `MOVE` / `ALIAS` / `VECGROW`
- `NNN` 三位序号，域内递增
- 例：`ATOM-MEM-MOVE-001`、`ATOM-UB-ALIAS-001`、`ATOM-HIST-AUTOPTR-001`

**三条强制规则**（用户原话落地）：
1. 原子一旦发布入库，**ID 永久不变**。
2. 拆分/合并原子**禁止修改原 ID**；新增 ID，并在 `atoms/id_migrations.json` 记录新旧映射与迁移理由。
3. 同义文字改写但断言未变 → **保留原 ID**，仅更新元数据与证据哈希。

**迁移表结构**（`atoms/id_migrations.json`，G1 初始化为空表）：
```json
{
  "schema": "cppbible-atom-migrations/1.0",
  "migrations": [
    {
      "ts": "2026-09-10",
      "op": "split | merge | rename | supersede",
      "from": ["ATOM-MEM-MOVE-001"],
      "to": ["ATOM-MEM-MOVE-001", "ATOM-MEM-MOVE-002"],
      "reason": "原断言含移动语义与完美转发两个机制，按粒度判据第 3 问拆分",
      "by": "human:liaoranran",
      "evidence_rebind": {"ATOM-MEM-MOVE-001": ["EV-..."], "ATOM-MEM-MOVE-002": ["EV-..."]}
    }
  ]
}
```

**为什么不用内容寻址 hash**（本设计决策，记一笔）：教材要被人讨论、在评审里被点名。ID 必须能念出来、能在会议里说"MOVE-001 这条有问题"。hash 做不到。代价是必须维护迁移表，我们接受这个代价。

## 6. 反例自检（什么情况算没做到）

- 若某个原子能同时归两个类型而无判据 → 类型学失效，**不合格**。
- 若 `prerequisite` 图出现环而门禁没报 → DAG 约束没落实，**不合格**。
- 若拆分原子时改了原 ID 而没写迁移记录 → 历史引用断裂，**不合格**。
- 若粒度 4 问里有任意一问答"否"却仍入库 → 粒度判据形同虚设，**不合格**。
- 若本文件只画了 ER 图而没给字段名 → 落不到文件，**不合格**（故字段名全部写在第 2 节与 `G1_layout.md`）。
