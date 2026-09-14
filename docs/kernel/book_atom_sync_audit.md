# book_atom_sync.py 功能分析（499 任务5）

> 分析对象：`tools/book_atom_sync.py`（224 行，已提交、已注册）
> 方法：Read 全文件 + 全仓搜索引用 + 比对现有工具
> 结论：**建议保留观察（已入库且已注册 cppbible，不建议删除，但缺测试）**

## 1. 它做什么

检查 Book（教材）与原子（atoms/）之间的双向同步关系，三类检查：

| 检查 | 触发条件 | 严重度 | 退出码影响 |
|---|---|---|---|
| 原子无 Book 引用 | 原子的 `sources:` 里没有 `Book/` 路径 | WARN | 不阻断 |
| Book 论断无原子支撑 | 章含"实测/实验/benchmark"等关键词的段落但没有 `<atom>` 标注 | WARN | 不阻断 |
| 孤儿原子引用 | Book 中 `<atom>XXX</atom>` 指向不存在的原子 | BLOCK | exit 1 |

设计要点（见文件内 373 §5 注释）：**只有 block 类（孤儿引用）才 exit 1**，warn 类只提示。原因：当前存量 27/27 原子无 Book 引用、143/147 章缺 `<atom>` 标注（共约 170 处 warn），若 warn 也 exit 1，工具一接入质量门就恒红 → "狼来了"。补标注属 Book 内容改动（本批铁律禁止），登记为债务逐步消化。

## 2. 输入输出

- **读**：`atoms/` 下所有 `ATOM-*.md`（rglob）、`Book/` 下所有 `ch*.md`（rglob）。
- **写**：无。三类子命令 `--check`/`--report`/`--atom` 都只打印到 stdout，不落盘。
- 通过 `parse_frontmatter` 解析每张原子的 frontmatter（`id`/`sources`/`status`）。

## 3. 与现有工具的重叠

- **gate_engine.py**：gate 校验单卡结构（claim/artifact/verdict 等）。`book_atom_sync` 的"孤儿引用 block"与 gate 的引用完整性校验在语义上互补但**不重复**——gate 管卡内结构，本工具管 Book↔原子跨树引用。
- **consistency_check.py**：做跨文档一致性（含 `前置：` 元数据、术语表 chapter_ref 等）。本工具的 Book↔原子引用检查是 consistency 的一个子集，但 consistency_check 不查 `<atom>` 标签孤儿。
- **atom_evidence_replay.py**：本工具已 `import parse_frontmatter`（373 §5 收编时砍掉了自带的前置 matter 解析器，**复用单点实现**），无双轨。
- **cppbible.py**：已在 `cmd_check` 元组注册（line 241），可被 `cppbible check` 统一调用。

**重叠结论**：功能有少量交集但无实质重复，且已接入统一入口，无需合并或删除。

## 4. 代码质量

- ✅ 无硬编码绝对路径：`ROOT = Path(__file__).resolve().parent.parent`，所有路径相对 ROOT。
- ✅ 退出码与 severity 对齐（只有 block 类 exit 1），符合"warn 类不恒红"的红线。
- ✅ 注释充分，373 §5 收编历史与"为什么 warn 不阻断"的理由写清。
- ⚠️ **无测试**：`tests/` 下没有针对它的用例（仅 `pyproject.toml` 引用其名做登记）。`EVIDENCE_KEYWORDS` 关键词列表与 `ATOM_TAG_RE`/`BOOK_PATH_RE` 正则均未被测试覆盖。
- ⚠️ `scan_book` 把"证据关键词段落"按 `\n\n` 切分，对含单换行换段的段落可能漏判/误判（边界，非 bug）。

## 5. 全仓引用确认

`Select-String -Pattern 'book_atom_sync'` 命中：`tools/cppbible.py`、`tools/book_atom_sync.py` 自身，以及多篇架构/验收文档（309/369/370/372/373/390/474 等历史讨论）。**无 CI workflow 直接调用**，仅通过 `cppbible check` 间接进入。

## 6. 建议

**保留观察（推荐）**：

1. 它已提交、已注册、已复用单点 `parse_frontmatter`，不是"孤立脚本"——与提示词"判断该入库还是删除"的前提不符，它**已在库内**。
2. 不建议删除：跨树孤儿引用检查是其他工具没覆盖的死角，且退出码设计正确。
3. 唯一短板是**缺测试**。建议下一步（超出本批铁律范围，留给好模型决策）：
   - 加 `tests/test_book_atom_sync.py`：构造 1 颗孤儿引用 / 1 段缺 `<atom>` 的 fixture，断言 `--check` exit 1 / warn 计数正确。
   - 把 `EVIDENCE_KEYWORDS` 与两个正则纳入 pytest 参数化，防止静默退化。

> 注：本批铁律#3 禁止改 `tools/*.py`，故本报告只给建议，未改动 `book_atom_sync.py` 本身。
