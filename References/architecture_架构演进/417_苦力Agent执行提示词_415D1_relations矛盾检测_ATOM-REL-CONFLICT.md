---
id: 417
title: 苦力Agent执行提示词 415D1 relations矛盾检测 ATOM-REL-CONFLICT
status: active
type: architecture-note
created_at: 2026-09-13
---
# 417 苦力Agent执行提示词：415 D1 relations 矛盾检测（ATOM-REL-CONFLICT）

> 投喂对象：苦力Agent（纯白嫖模型）。前置条件：414 修复批已完成（尤其 P1-8 F07 relations 纯标量已修）。任务：实现 relations 矛盾检测，让 relations 从"静态声明"变成"互相校验"。

---

## 铁律（违反即返工）

1. **不 push**：只 commit，push 交用户
2. **工具改动分离提交**：独立 commit，不混文档
3. **存量 0 误伤**：修复后 `gate --check` 的 block=0，warn 数不增加（当前 32），`replay` confirm 数不减少（当前 56）
4. **配毒样例 + pytest**：每个新规则配毒样例和回归测试
5. **修完跑全量门禁**：gate + replay + poison + pytest，全绿才提交
6. **先 Read 再改**：必须先 Read `tools/gate_engine.py` 确认当前 `DAG_REL`、`_relations_norm`、规则注册表的真实状态（414 可能已改 relations 解析入口），禁止凭历史上下文写代码

---

## 背景（为什么做这个）

415 调研发现：阙疑 27 颗原子的 relations 是"写了但不用"——没有矛盾检测。实读 gate_engine.py 确认：
- D3 误解悬空 → `ATOM-MISCONCEPTION-REF`（已有，block）
- D2 serves 悬空 → `EV-SERVES-EXIST`（已有，warn）
- **D1 relations 矛盾 → 真空白**，因为 `DAG_REL={prerequisite, specializes, realizes, evolved_from}` 没有 `contradicts` 类型，机器无从表达"矛盾"

本任务 = 填补 D1 空白。

---

## 实现步骤

### Step 1：Read 确认当前状态（必须先做）

```python
# Read tools/gate_engine.py，确认：
# 1. DAG_REL 的当前定义（414 是否扩展了）
# 2. _relations_norm 的当前实现
# 3. 规则注册表的格式（RULES 列表）
# 4. ATOM-REL-TARGET 的实现（参考写法）
# 5. 414 P1-8（relations 纯标量 warn）是否已合入
```

如果 414 未合入，先停手报告——本任务依赖 414 的 relations 解析扩展。

### Step 2：schema 加性扩展

在 `gate_engine.py` 中新增（不修改现有 DAG_REL）：

```python
# 冲突关系类型（加性扩展，不破坏现有 DAG_REL）
CONFLICT_REL = {"contradicts", "conflicts_with"}

# 支持关系 = DAG_REL ∪ CONFLICT_REL（用于解析时识别）
ALL_REL = DAG_REL | CONFLICT_REL
```

如果 `_relations_norm` 只识别 DAG_REL，扩展它使其也识别 CONFLICT_REL（但冲突关系不参与 DAG 排序，只参与矛盾检测）。

### Step 3：新规则 ATOM-REL-CONFLICT（block）

实现函数 `check_atom_rel_conflict() -> list[Finding]`：

**检测逻辑（纯图遍历，零 LLM）**：

```python
def check_atom_rel_conflict():
    findings = []
    # 1. 加载所有原子的 relations（用 _relations_norm 解析）
    # 2. 构建两个集合：
    #    - supports[A] = A 的 prerequisite/specializes/realizes/evolved_from 中的原子
    #    - conflicts[A] = A 的 contradicts/conflicts_with 中的原子
    # 3. 对每颗原子 A：
    #    for B in supports[A]:
    #        if A in conflicts[B]:  # B 声明与 A 矛盾，但 A 依赖/支持 B
    #            findings.append(Finding("ATOM-REL-CONFLICT", "block", path,
    #                f"A 支持/依赖 B（{rel_type}），但 B 声明 contradicts A",
    #                "移除矛盾关系或修正依赖方向"))
    #    for B in conflicts[A]:
    #        if A in supports[B]:  # 对称情况
    #            findings.append(...)
    # 4. 自相矛盾：A 在自己的 conflicts 中 → block
    #    if A in conflicts[A]:
    #        findings.append(Finding("ATOM-REL-CONFLICT", "block", path,
    #            "原子自相矛盾（contradicts 自身）",
    #            "移除自引用"))
```

**L1 机械/L2 语义边界（严守）**：
- ✅ 检测：relations 字段中的结构化矛盾（A 依赖 B 且 B contradicts A）
- ❌ 不检测：claim 文本中的语义矛盾（"A 说 X，B 说非 X"）——归红队，不进 L1
- ❌ 不检测：证据卡之间的数值矛盾——归 replay/gate 的其他规则

### Step 4：注册规则

在规则注册表中新增：
```python
("ATOM-REL-CONFLICT", "relations 矛盾检测：A 支持/依赖 B 且 B 声明 contradicts A（415 D1）",
 "atom", check_atom_rel_conflict),
```

### Step 5：毒样例

在 `tests/poison/` 下新增：

**P29：双向矛盾**
```yaml
# atoms/test/ATOM-TEST-CONFLICT-001.md
---
id: ATOM-TEST-CONFLICT-001
relations:
  prerequisite: [ATOM-TEST-CONFLICT-002]
---
# 依赖矛盾者
```
```yaml
# atoms/test/ATOM-TEST-CONFLICT-002.md
---
id: ATOM-TEST-CONFLICT-002
relations:
  contradicts: [ATOM-TEST-CONFLICT-001]
---
# 被依赖但声明矛盾
```
预期：`ATOM-REL-CONFLICT` block（001 依赖 002，但 002 contradicts 001）

**P30：自相矛盾**
```yaml
# atoms/test/ATOM-TEST-SELF-CONFLICT-001.md
---
id: ATOM-TEST-SELF-CONFLICT-001
relations:
  contradicts: [ATOM-TEST-SELF-CONFLICT-001]
---
# 自相矛盾
```
预期：`ATOM-REL-CONFLICT` block（自引用）

**P31：合法共存（阴性对照）**
```yaml
# atoms/test/ATOM-TEST-LEGAL-001.md
---
id: ATOM-TEST-LEGAL-001
relations:
  prerequisite: [ATOM-TEST-LEGAL-002]
  contrasts: [ATOM-TEST-LEGAL-003]
---
```
```yaml
# atoms/test/ATOM-TEST-LEGAL-002.md
---
id: ATOM-TEST-LEGAL-002
relations:
  contrasts: [ATOM-TEST-LEGAL-001]
---
```
预期：**不触发** ATOM-REL-CONFLICT（contrasts 不是 contradicts，合法的对比关系）

### Step 6：pytest

在 `tests/test_gate_engine.py` 中新增：

```python
class TestAtomRelConflict:
    def test_prerequisite_contradicts_block(self):
        # A.prereq=B 且 B.contradicts=A → block
        ...

    def test_self_contradicts_block(self):
        # A.contradicts=A → block
        ...

    def test_contrasts_not_conflict(self):
        # A.contrasts=B → 不 block（contrasts ≠ contradicts）
        ...

    def test_no_false_positive_legal_atoms(self):
        # 存量 27 颗原子 0 误伤
        ...
```

### Step 7：存量 0 误伤验证

跑 `gate_engine.py --check`，确认：
- block=0
- warn 数不增加（当前 32）
- 存量 27 颗原子没有触发 ATOM-REL-CONFLICT

如果存量有误伤，**先报告不修复**——存量原子的 relations 可能真的有矛盾（那是内容问题，不是工具问题），需人审裁决。

### Step 8：全量门禁

```bash
python tools/gate_engine.py --check
python tools/atom_evidence_replay.py --check
python tools/poison_drill.py
python -m pytest tests/ -v
```

全绿才提交。

---

## 验收标准

- [ ] `gate_engine.py --list` 包含 `ATOM-REL-CONFLICT`
- [ ] 规则数 42→43（+1）
- [ ] 毒样例 44→47/47（+3：P29/P30/P31）
- [ ] pytest 含 TestAtomRelConflict（4 例）
- [ ] replay confirm=56 refute=0 infra_error=0
- [ ] gate block=0，warn 数不增加
- [ ] 存量 27 颗原子 0 误伤
- [ ] 独立 commit，message 含 `feat(gate): 415 D1 ATOM-REL-CONFLICT relations矛盾检测`
- [ ] 提交后报告：commit hash + 门禁数字 + 存量误伤检查结果

---

## 不做的事

- 不做 claim 文本语义矛盾检测（归红队/L2）
- 不做循环依赖检测（ATOM-REL-CYCLE，留待下一批）
- 不做影响分析（415 L2，留待下一批）
- 不改存量 27 颗原子的 relations（只改工具和测试）
- 不 push
- 不混 414 的修复（如果 414 未完成，先停手报告）

---

## 与 414 的衔接（关键）

414 P1-8（relations 纯标量 warn）必须先完成——纯标量 relations 不经过 DAG 校验，矛盾检测覆盖不到。顺序：
1. 414 让纯标量进视野（warn）
2. 417（本任务）让关系互相校验（block）

如果 414 未合入，本任务的 `_relations_norm` 可能不识别纯标量 relations，导致漏检。先 Read 确认。
