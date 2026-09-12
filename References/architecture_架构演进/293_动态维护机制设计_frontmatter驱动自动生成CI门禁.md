# 动态维护机制设计：让分类清洗从「一次性快照」变成「自更新系统」

> 2026-09-12 · 第 293 份。289–292 是静态快照，项目发展就会过时。本文设计动态维护机制：frontmatter 驱动 + 自动生成索引 + CI 门禁，让分类自更新。

---

## 一、问题诊断

### 为什么静态分类会过时

| 静态快照 | 过时触发 | 过时后果 |
|---|---|---|
| 289 全量分类 | 新增 References 文档 | 00 导航不覆盖新文档 |
| 290 质量评级 | 新资料研究完成 | 评级表缺新文档 |
| 290 原子吸收映射 | 新原子 verified | 映射表不更新 |
| 291 架构落地状态 | 新概念落地/新提案 | 落地率过时 |
| 292 工具普查 | 新工具添加/旧工具归档 | 工具清单过时 |

**根因**：分类信息存在文档里（289–292），而不是存在被分类对象的元数据里。对象变了，分类文档不会自动变。

### 解决思路

把分类信息从「分类文档」迁移到「被分类对象的 frontmatter」，分类文档由工具自动生成。

```
旧模式：人写分类文档 → 过时 → 人重新整理（289–292 模式）
新模式：对象带分类元数据 → 工具自动生成索引 → CI 强制元数据完整
```

---

## 二、方案设计：frontmatter 驱动 + 自动生成 + CI 门禁

### 2.1 References 文档 frontmatter schema

每份 `References/*.md` 顶部加：

```yaml
---
id: "11"                          # 编号（与文件名一致）
title: "C++内存模型与并发"         # 标题
category: "E"                     # A/B/C/D/E/F 六大类
subcategory: "E1"                 # 18 子类（E1–E17）
quality: "S"                      # S/A+/A/B+/B/C（资料研究必填，其他类可空）
status: "active"                  # active / archived / proposal / executed
absorbed_by: ["MOVE-002"]         # 已被哪些原子吸收（可空，自动反推辅助）
related_to: ["18", "77"]          # 相关文档编号
version: "v1.0"
last_updated: "2026-09-12"
---
```

**字段说明**：
- `category` / `subcategory`：从 289 的分类体系，枚举值固定
- `quality`：从 290 的评级，仅 E 类（资料研究）必填
- `status`：从 291 的落地状态（active/archived/proposal/executed）
- `absorbed_by`：从 290 的原子映射，**可半自动**——从 atoms/ 的 relations 反推
- `related_to`：人工标注的相关文档

### 2.2 tools/ 工具元数据 schema

每个 `tools/*.py` 的 module docstring 加：

```python
"""
工具名称：gate_engine
分类：T1 核心门禁
CI 调用：是
功能：33 规则机械判定
入口：python tools/gate_engine.py --check
维护状态：active
"""
```

### 2.3 自动生成工具：tools/references_index.py

**功能**：
1. 扫描 `References/*.md` 的 frontmatter
2. 按 category/subcategory 分组
3. 自动生成 `References/00_导航_自动生成.md`（不覆盖手写的 00，而是生成 00_auto）
4. 输出统计：各类数量、质量分布、吸收率

**输入**：References/*.md frontmatter + atoms/*.md relations（反推 absorbed_by）
**输出**：00_auto.md（导航）+ 统计 JSON

**关键设计**：
- 00 导航分两部分：**手写核心发现**（保留现有 00 的二~五节）+ **自动生成导航**（由工具生成，标记 `<!-- AUTO-GENERATED -->`）
- 工具只替换自动生成部分，不碰手写部分

### 2.4 CI 门禁规则

给 gate_engine.py 加新规则（或独立的 references_meta_check.py）：

| 规则 | 检查 | 级别 |
|---|---|---|
| REF-META-REQUIRED | 新增 References .md 必须有 category/subcategory | block |
| REF-QUALITY-REQUIRED | E 类文档必须有 quality 字段 | block |
| REF-ID-MATCH | frontmatter id 与文件名编号一致 | warn |
| REF-CATEGORY-VALID | category 必须是 A/B/C/D/E/F 之一 | block |
| REF-SUBCATEGORY-VALID | subcategory 必须是已定义的子类 | warn |

**触发时机**：CI 检查新增或修改的 References 文档（用 git diff 过滤）。

---

## 三、最小可用版（先做什么）

不追求一次完美，按以下顺序落地：

### 阶段 1：schema 定义 + 生成工具（零风险，不动现有文档）
- [ ] 定义 frontmatter schema（本文档 §2.1）
- [ ] 写 `tools/references_index.py` v0.1（扫描 frontmatter + 生成导航）
- [ ] 用现有 85 份文档测试（即使大部分没有 frontmatter，工具应优雅处理）

### 阶段 2：批量加 frontmatter（脚本辅助 + 人工确认）
- [ ] 写 `tools/references_meta_init.py`：基于 289/290/291 的分类数据，自动给 85 份文档生成 frontmatter 草稿
- [ ] 人工确认 quality 评级（290 已评级，可直接导入）
- [ ] 人工确认 absorbed_by（290 已映射，可直接导入）
- [ ] 批量写入 frontmatter

### 阶段 3：CI 门禁 + 自动导航
- [ ] gate_engine 加 REF-META-REQUIRED / REF-QUALITY-REQUIRED 规则
- [ ] 00 导航改为「手写核心发现 + 自动生成导航」混合模式
- [ ] CI 加一步：跑 references_index.py --check，确保导航与 frontmatter 同步

### 阶段 4：扩展到 tools/ 和 atoms/
- [ ] tools/ 加 docstring 元数据（90 个工具，脚本辅助）
- [ ] atoms/ 加 coverage 字段（被哪些资料研究覆盖，反推）
- [ ] 统一生成「项目全资产索引」

---

## 四、迁移路径：现有 85 份文档如何加 frontmatter

### 4.1 自动生成草稿

基于 289/290/291 已有的分类数据，写脚本自动生成 frontmatter：

```python
# 伪代码
classification_289 = {
    "11": {"category": "E", "subcategory": "E1", "title": "C++内存模型与并发"},
    "14": {"category": "E", "subcategory": "E1", "title": "真实并发Bug案例", "quality": "S"},
    ...
}
absorption_290 = {
    "11": ["MOVE-002", "RVREF-001"],
    "26": ["GRAY-001"],
    ...
}
status_291 = {
    "277": "active",
    "273": "proposal",
    ...
}
```

### 4.2 人工确认清单

脚本生成后，人工只需确认：
- quality 评级是否准确（290 已评级，确认即可）
- absorbed_by 是否完整（290 已映射，确认即可）
- status 是否准确（291 已标注，确认即可）

预计 85 份文档，人工确认约 30 分钟（大部分可直接导入）。

### 4.3 增量维护

新增文档时：
- 复制模板（含 frontmatter）
- 填写 category/subcategory（必填）
- quality/absorbed_by 可后补，但 CI 会 warn
- CI 自动检查 + 自动更新导航

---

## 五、扩展：动态质量评级与吸收状态

### 5.1 absorbed_by 自动反推

从 atoms/*.md 的 frontmatter relations 反推：
```
如果 ATOM-MEM-MOVE-002 的 relations 提到「参考 References/11」
→ 自动在 11 的 absorbed_by 加 MOVE-002
```

这需要 atoms 的 relations 有结构化的 References 引用。当前 atoms 的 relations 是文本，需要加 `references: ["11"]` 字段。

### 5.2 quality 评级半自动

quality 评级目前是人工判断。可半自动的维度：
- **是否有一手来源**：扫描文档中是否有标准条文/源码/官方文档链接（自动）
- **是否被原子吸收**：absorbed_by 非空（自动）
- **技术深度**：人工判断（不可自动）

建议：quality 保留人工评级，但加 `quality_evidence` 字段（自动检测一手来源数量）。

### 5.3 工具 CI 调用状态自动检测

从 .github/workflows/ci.yml 自动提取 `python tools/xxx.py` 调用，更新工具的 `ci_invoked` 字段。292 已手动做了一次，可脚本化。

---

## 六、与现有体系的对接

| 现有机制 | 动态维护对接 |
|---|---|
| gate_engine（33 规则） | 加 REF-META 系列规则（34–38 条） |
| golden_lock | 检查 References frontmatter 与 atoms relations 的一致性 |
| debt_ledger | 「未加 frontmatter 的文档」作为债务，owner=human，到期 30 天 |
| poison_drill | 加毒样例：缺 category 的文档应被 REF-META-REQUIRED 拦住 |
| 00 导航 | 改为手写+自动生成混合模式 |

---

## 七、风险与缓解

| 风险 | 缓解 |
|---|---|
| frontmatter 加错（分类不准） | CI 只检查字段存在性，不检查准确性；准确性靠人审 + 定期复核 |
| 工具生成的导航覆盖手写内容 | 明确分隔：`<!-- AUTO-GENERATED:START -->` ... `<!-- AUTO-GENERATED:END -->`，工具只替换标记内 |
| 85 份文档批量改动大 | 分阶段：先加 frontmatter（纯添加，不改正文），再改导航 |
| 新工具增加维护负担 | references_index.py 控制在 200 行内，纯标准库，无外部依赖 |
| atoms relations 无结构化引用 | 先不做自动反推，absorbed_by 人工维护；等 atoms 加 references 字段后再自动化 |

---

## 八、下一步（按优先级）

### P0（立即做，零风险）
1. 写 `tools/references_index.py` v0.1（扫描+生成，不改动现有文档）
2. 定义 frontmatter schema（本文档 §2.1 即为规格）

### P1（本周做，低风险）
3. 写 `tools/references_meta_init.py`（基于 289/290/291 数据批量生成 frontmatter 草稿）
4. 人工确认 85 份文档的 frontmatter
5. 批量写入 frontmatter

### P2（下周做，需 gate 改动）
6. gate_engine 加 REF-META-REQUIRED / REF-QUALITY-REQUIRED 规则
7. 00 导航改为手写+自动生成混合模式
8. CI 加 references_index.py --check

### P3（后续扩展）
9. tools/ docstring 元数据 + 自动分类
10. atoms/ 加 references 字段 + absorbed_by 自动反推
11. 质量评级半自动（一手来源检测）

---

## 九、给执行 Agent 的投喂提示词

```
任务：实现 References 动态维护机制 v0.1（阶段 1）

项目根：C:\CodeLearnling\note\note\C++\CPP-Bible

1. 读 293 §2.1 的 frontmatter schema
2. 写 tools/references_index.py（纯标准库，≤200 行）：
   - 扫描 References/*.md frontmatter
   - 按 category/subcategory 分组
   - 生成 References/00_auto.md（自动导航，标记 AUTO-GENERATED）
   - 输出统计 JSON（各类数量/质量分布）
   - 无 frontmatter 的文档归入「未分类」组并 warn
3. 跑一次：python tools/references_index.py
   - 验证：85 份文档全部被扫描，未分类的列出
   - 验证：00_auto.md 生成成功
4. 不改动现有任何文档（只读扫描+生成新文件）
5. 不混 References/（铁律 3）——00_auto.md 是生成产物，可提交

验收：
- [ ] tools/references_index.py 存在且 py_compile 通过
- [ ] 扫描 85 份文档无报错
- [ ] 00_auto.md 生成，含分类导航
- [ ] 未分类文档数量正确（当前 85 份都无 frontmatter，应全部归入未分类）
- [ ] 统计 JSON 输出正确
```

---

*核心原则：分类信息存在对象里，不存在分类文档里。分类文档是生成产物，不是事实源。*
