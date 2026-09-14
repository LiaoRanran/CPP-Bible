---
id: 408
title: 苦力Agent下一轮执行提示词 安全残留修复+版本管理P0+闪卡工具
status: active
type: architecture-note
created_at: 2026-09-13
---
# 408 苦力Agent下一轮执行提示词：安全残留修复 + 版本管理P0 + 闪卡工具

> 投喂对象：苦力Agent（低成本模型）。任务全部机械可执行，有明确验收命令。不需要深度判断，不需要创新。
> 前置状态：403 批次已完成（A1/A2/A3/B1/C2 全绿），gate 42 条 block=0 warn=32，poison 36/36，pytest 含 JSON 测试 4/4。本地 ahead 若干，push 网络阻断（不处理）。

---

## 全局铁律（违反任何一条即任务失败）

1. **不 push**：只 commit，不 push。push 权在用户。
2. **不碰红队/对抗产物**：`_adv_v61/`、`_bypass_test/`、`_worklog_*.md` 不读不改不提交。
3. **不碰 References/architecture_架构演进/**：架构文档由监工维护，苦力不写。
4. **改工具必须配 pytest + 毒样例**：任何 gate_engine/replay 逻辑改动必须有对应测试。
5. **加性变更自由，破坏性变更必须先报告**：加字段可以直接做，删字段/改字段含义必须停手报告。
6. **所有数字以实跑为准**：不凭记忆写规则数、卡数、原子数，用命令实跑。
7. **提交分离**：工具改动、内容改动、文档改动分别 commit，不混。
8. **完成后跑门禁**：gate --check + poison + pytest 必须全绿才能报完成。

---

## 任务 0：P1a 残留漏洞核实（只核实，不修，报告结果）

### 背景
P1a 修复了声明-实现脱钩（EV-ARTIFACT-PRODUCER 要求 artifact_producer 段逐字出现在 command 且 -o 目标==artifact）。但可能没堵住"编译后覆盖"形态：command 末尾 `&& cp other.asm x.asm` 或 `&& mv other.asm x.asm`。

### 执行步骤
1. Read `tools/gate_engine.py`，找到 EV-ARTIFACT-PRODUCER 的实现代码
2. 检查是否有对 `cp` / `mv` / `copy` / `move` 命令的检测
3. 写一个临时测试卡（放在 `_diag/` 目录，不入库）：
   - command: `g++ -S fixture.cpp -o real.asm && cp real.asm fake.asm`
   - artifact: `fake.asm`
   - artifact_producer: `g++ -S fixture.cpp -o real.asm`
4. 跑 `python tools/gate_engine.py --check --file _diag/test_cp_cover.md`
5. 记录结果：是 block 还是 pass？如果 pass，说明漏洞存在

### 输出
报告："P1a 残留漏洞：存在/不存在。证据：gate 输出原文。"

---

## 任务 1：如果任务 0 发现漏洞，修复（如果没发现，跳过此任务）

### 修复要求
在 EV-ARTIFACT-PRODUCER 的检查中增加：
- 检测 command 中是否包含 `cp` / `mv` / `copy` / `move` 且目标文件 == artifact
- 如果是，block，fix_hint: "artifact 疑似由 cp/mv 从其他文件复制而来，声明-实现绑定不成立"
- 注意：不要误伤正常的 `cp fixture.cpp build/`（目标不是 artifact 的情况）

### 验收
- 新增毒样例 P20：cp 覆盖形态（必须 block）
- 新增毒样例 P21：mv 覆盖形态（必须 block）
- 新增 pytest 2 例
- 存量 56 张合法卡 0 误伤（跑全量 gate 确认 warn 数不变）

---

## 任务 2：406 P0——原子加 version 字段（批量，机械）

### 背景
406 定义了原子版本化：每颗原子加 `version: MAJOR.MINOR.PATCH`。当前所有 verified 原子初始版本 = 1.0.0，draft 原子 = 0.1.0。

### 执行步骤
1. 列出所有原子文件：`Get-ChildItem atoms/*/ATOM-*.md`
2. 对每个文件：
   - Read frontmatter
   - 如果已有 `version` 字段，跳过
   - 如果没有，在 `id:` 行之后加 `version: 1.0.0`（verified 原子）或 `version: 0.1.0`（draft 原子）
   - 判断 verified/draft：看 frontmatter 的 `status:` 字段
3. 用脚本批量做，不要手动一个个改
4. 改完后跑 `python tools/gate_engine.py --check` 确认 block=0

### 验收
- 所有原子文件都有 `version` 字段
- `grep -r "version:" atoms/` 的行数 == 原子文件数
- gate block=0（加字段不应该触发任何规则）

---

## 任务 3：406 P0——证据卡加 data_freshness 分类（批量，机械）

### 背景
406 定义了三类数据新鲜度：
- `deterministic`：方向量、符号存在性（长保质期）
- `performance`：纳秒、倍数、吞吐量（极短保质期，永不进断言）
- `tool_observation`：sanitizer 报不报（中保质期）

### 执行步骤
1. 列出所有证据卡：`Get-ChildItem evidence/*/EV-*.md`
2. 对每张卡，Read 后判断类型：
   - 卡内有 `ns` / `倍` / `throughput` / `ops/s` / 性能数字 → `performance`
   - 卡内有 `sanitizer` / `LSan` / `TSan` / `ASan` / `leak` / `data race` → `tool_observation`
   - 其他（方向量、符号断言、判据）→ `deterministic`
   - 如果一张卡同时有性能和判据（如 PERF-004 的两张卡），判据卡标 `deterministic`，性能卡标 `performance`
3. 在 frontmatter 加 `data_freshness: {stability: 类型, measured_at: "卡内已有的日期或未知"}`
4. 用脚本批量做
5. 改完后跑 gate 确认 block=0

### 验收
- 所有证据卡都有 `data_freshness` 字段
- 三类分布合理（performance 类应该是少数，约 10-15 张）
- gate block=0

### 注意
- 如果判断不确定，默认标 `deterministic`（最保守）
- 不要改卡的正文，只加 frontmatter 字段

---

## 任务 4：405 P0——闪卡导出工具（新建，有明确验收）

### 背景
405 定义了教学转化 L1：每颗原子→3-5 张闪卡（Anki 兼容，制表符分隔 Q/A）。

### 工具要求
新建 `tools/atom_to_flashcards.py`：
- 输入：原子文件路径（或 `--all` 处理所有原子）
- 输出：制表符分隔的 .txt 文件（Anki 导入格式）
- 每张原子生成 3 张闪卡：
  1. **概念卡**：正面=claim 的问题化（把 claim 改成问句），背面=claim 原文
  2. **误解卡**：正面=pedagogy.misconception 引用的误解的触发词+"对吗？"，背面=为什么错（引用误解卡的反例第一条）
  3. **实证卡**：正面=证据卡的关键读数+"说明什么？"，背面=含义（从原子正文提取）
- 如果原子没有 pedagogy.misconception 或 evidence，跳过对应卡，只生成有的

### 验收
- `python tools/atom_to_flashcards.py --all --output flashcards.txt` 能运行
- 输出文件非空，每行是 `问题\t答案` 格式
- 至少生成 50 张闪卡（27 原子 × 平均 2 张）
- 抽查 3 张：问题和答案与原子内容一致
- 工具登记到 `tools/cppbible.py` 的 cmd_check 元组（如果有这个机制）

### 注意
- 闪卡答案必须和原子 claim 逐字一致（不能改写）
- 问题化只是把陈述句改成问句，不改变含义
- 不要生成 Markdown，输出纯文本制表符分隔

---

## 完成清单（逐项打勾才能报完成）

- [ ] 任务 0：P1a 残留漏洞核实完成，有明确结论
- [ ] 任务 1（条件执行）：如果有漏洞，修复+毒样例+pytest，存量 0 误伤
- [ ] 任务 2：所有原子有 version 字段，gate block=0
- [ ] 任务 3：所有证据卡有 data_freshness 字段，gate block=0
- [ ] 任务 4：atom_to_flashcards.py 可运行，生成 ≥50 张闪卡
- [ ] 全量门禁：gate block=0 · poison 全过 · pytest 全过
- [ ] 提交分离：工具改动/内容改动/文档改动分别 commit
- [ ] 未 push（符合铁律）

---

## 提交规范

- 工具改动（任务 1/4）：`feat(tool): ...`
- 内容批量改动（任务 2/3）：`chore(atoms): add version field to all atoms` / `chore(evidence): add data_freshness to all cards`
- 每个 commit 前跑对应范围的门禁
- commit message 写清改了什么、为什么、验收结果

---

## 停止条件（遇到以下情况立即停手报告，不擅自处理）

1. 任务 0 发现漏洞但修复方案不确定
2. 批量改字段时 gate 出现 block（不是 warn）
3. 闪卡工具运行报错且 15 分钟内修不好
4. 任何需要判断"这个原子该标什么版本/类型"的歧义
5. 发现存量原子/证据卡的 frontmatter 格式不统一导致脚本失败

停手时报告：卡在哪、已完成什么、需要什么决策。
