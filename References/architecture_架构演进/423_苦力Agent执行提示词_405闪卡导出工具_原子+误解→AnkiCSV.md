# 423 苦力Agent执行提示词：405 闪卡导出工具（原子+误解 → Anki CSV）

> 投喂对象：苦力Agent。前置条件：无（可与 414/420/421 并行）。任务：把 27 颗 verified 原子 + 80 条误解导出为 Anki 闪卡，让阙疑的知识第一次被学习者消费。零风险——只读不写生产文件。

---

## 铁律

1. **不 push**：只 commit
2. **工具改动分离提交**
3. **零风险**：只读 atoms/evidence/misconceptions，不修改任何生产文件
4. **配 pytest**
5. **先 Read 再改**：Read 3 颗原子 + 3 条误解的真实格式，确认字段名

---

## 背景

405 调研指出：阙疑 27 颗 verified 原子 + 80 条误解 = 教学内容已经存在，但没有任何面向学习者的输出。知识生产了但没被消费。

最小可行闭环 = 闪卡导出器：把原子的 claim 和误解的反例，转成 Anki CSV 格式，学生可直接导入。

---

## 实现步骤

### Step 1：Read 确认数据格式

```python
# Read 3 颗原子，确认 frontmatter 字段：
# - id, claim, type, domain, misconception（pedagogy.misconception）
# Read 3 条误解，确认格式：
# - id, level (surface/deep), claim（误解的错误说法）, examples（反例列表）
```

### Step 2：创建 tools/flashcard_export.py

```python
#!/usr/bin/env python3
"""
闪卡导出工具：原子 + 误解 → Anki CSV
用法：
  python tools/flashcard_export.py --format anki --output data/flashcards/
  python tools/flashcard_export.py --format markdown --output data/flashcards/
输出：CSV（Anki 导入格式）或 Markdown
零风险：只读不写生产文件。
"""
```

### Step 3：闪卡类型

#### 类型 A：原子 Claim 卡（每颗原子 1 张）

```
Front: 【{domain}】{atom_id}
       {claim 的问题化表述}
Back:  {claim 原文}
       ---
       关键证据：{evidence 卡的 verdict 和核心读数}
       常见误解：{关联的 misconception id}
```

**问题化表述**：把 claim 从陈述句改成问题。
- 例：claim="多线程独立变量因共享缓存行可慢约一个数量级"
- 问题化："多线程各自读写独立变量时，是否可能因共享缓存行而变慢？慢多少？"

#### 类型 B：误解反例卡（每条误解 1 张）

```
Front: 【误解】{misconception_id}
       {误解的错误说法}
Back:  为什么错：{1 句话解释}
       反例 1：{examples[0]}
       反例 2：{examples[1]}
       反例 3：{examples[2]}
       关联原子：{引用此误解的原子 id}
```

#### 类型 C：证据对照卡（可选，每颗原子 1 张）

```
Front: 【{atom_id}】实测证据是什么？
Back:  {evidence 卡的核心读数，2-3 行}
       工件 sha：{artifact_sha256 前 8 位}
       编译器：{artifact_compiler}
```

### Step 4：Anki CSV 格式

```csv
# 字段：Front, Back, Tags, Deck
"多线程各自读写独立变量时是否可能变慢？","约一个数量级（实测 18.86×）...","PERF-004 false_sharing cache_line","CPP-Bible::mem"
```

- 第一行是表头（Anki 可识别）
- Front/Back 用双引号包裹，内部双引号转义为 `""`
- Tags 用空格分隔
- Deck 用 `::` 分层（CPP-Bible::mem、CPP-Bible::conc 等）

### Step 5：Markdown 格式（备选）

```markdown
# PERF-004 闪卡

## 正面
多线程各自读写独立变量时，是否可能因共享缓存行而变慢？

## 背面
约一个数量级（实测 18.86×，Linux 18.54×）。
结构前提可用地址确定性判定，padding 有空间代价（16×）。
```

### Step 6：统计与验证

导出后输出统计：
```json
{
  "total_cards": 107,
  "by_type": {"atom_claim": 27, "misconception": 80, "evidence": 0},
  "by_domain": {"mem": 45, "conc": 12, "ub": 30, "lang": 5, "hist": 15},
  "by_misconception_level": {"surface": 50, "deep": 30},
  "output_files": ["data/flashcards/anki.csv", "data/flashcards/markdown/"]
}
```

**验证标准**：
- 27 颗 verified 原子 → 27 张 claim 卡
- 80 条误解 → 80 张反例卡
- 合计 107 张
- 每张卡 Front 非空、Back 非空
- CSV 可被 Anki 导入（格式正确）

### Step 7：pytest

```python
class TestFlashcardExport:
    def test_atom_claim_card_generation(self):
        # 用一颗已知原子 → 生成 1 张 claim 卡，字段正确
        ...

    def test_misconception_card_generation(self):
        # 用一条已知误解 → 生成 1 张反例卡，含 3 反例
        ...

    def test_anki_csv_format(self):
        # CSV 格式正确（表头、引号转义、字段数）
        ...

    def test_all_verified_atoms_exported(self):
        # 27 颗 verified 原子全部有卡
        ...

    def test_all_misconceptions_exported(self):
        # 80 条误解全部有卡
        ...

    def test_no_empty_fields(self):
        # 所有卡 Front/Back 非空
        ...
```

### Step 8：注册到 cppbible.py

```bash
cppbible flashcards export --format anki
cppbible flashcards export --format markdown
```

---

## 验收标准

- [ ] `tools/flashcard_export.py` 存在
- [ ] `data/flashcards/anki.csv` 生成，107 张卡
- [ ] `data/flashcards/markdown/` 生成，107 个 .md 文件
- [ ] 27 颗 verified 原子全部有 claim 卡
- [ ] 80 条误解全部有反例卡
- [ ] 每张卡 Front/Back 非空
- [ ] CSV 格式可被 Anki 导入（表头+引号转义）
- [ ] pytest 含 TestFlashcardExport（≥6 例）
- [ ] `cppbible flashcards export` 可执行
- [ ] 零风险：不修改 atoms/evidence/misconceptions 下任何文件
- [ ] 独立 commit，message 含 `feat(tools): 405 闪卡导出工具 原子+误解→Anki CSV`

---

## 不做的事

- 不做在线编译/交互（L4 活代码，留待后续）
- 不做诊断 MCQ（L2，留待后续）
- 不做学习路径（L3，留待后续）
- 不修改原子/误解的内容（只读取）
- 不 push
- 不混 414/417/420/421 的改动

---

## 为什么这是 P1

405 指出：阙疑的知识是"实测出来的"不是"写出来的"——这意味着闪卡的背面不是"教材式讲解"，而是"实测数据+反例"。这是阙疑与传统学习资料的根本区别。

本工具零风险（只读），但价值极高——它让 27 颗原子第一次被学习者消费，而不是躺在仓库里。
