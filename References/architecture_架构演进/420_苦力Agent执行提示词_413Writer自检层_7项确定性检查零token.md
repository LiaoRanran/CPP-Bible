---
id: 420
title: 苦力Agent执行提示词 413Writer自检层 7项确定性检查零token
status: active
type: architecture-note
created_at: 2026-09-13
---
# 420 苦力Agent执行提示词：413 Writer 自检层（7 项确定性检查，零 token）

> 投喂对象：苦力Agent。前置条件：无（可与 414 并行）。任务：实现 Writer 自检层，在卡/原子提交前拦住 E1/E2 机械错误，不让它们进入红队。

---

## 铁律

1. **不 push**：只 commit
2. **工具改动分离提交**
3. **存量 0 误伤**：自检对存量 27 颗原子+56 张卡不报错（或报错是真问题，需人审裁决）
4. **配 pytest**
5. **修完跑全量门禁**
6. **先 Read 再改**：Read `tools/` 下现有工具的结构，保持代码风格一致

---

## 背景

413 调研将错误分为 E1-E6 六类，其中 E1（形式）和 E2（工件）是机械错误，可被确定性检查拦住。第五批 3 颗跨 6 窗口，根因就是 E1/E2 消耗了红队注意力。

Writer 自检层 = 在 Writer 完成卡/原子后、提交前，自动跑 7 项检查，拦住 E1/E2，让红队专注 E3/E4 语义错误。

---

## 实现步骤

### Step 1：创建 tools/writer_selfcheck.py

```python
#!/usr/bin/env python3
"""
Writer 自检层：7 项确定性检查，零 token，在提交前拦住 E1/E2 机械错误。
用法：python tools/writer_selfcheck.py <card_or_atom_path>
输出：JSON（与四工具 --json 格式一致）
退出码：0=全过，1=有 fail
"""
```

### Step 2：实现 7 项检查

#### 检查 1：工件同代（E1，最关键）

```python
def check_artifact_same_generation(card_path):
    """
    卡的 artifact_sha256 必须等于重生成工件的 sha256。
    如果卡改了计数但没重生成工件 → fail。
    """
    # 1. 从卡的 frontmatter 读 artifact 路径和 artifact_sha256
    # 2. 从卡的 command 提取编译命令
    # 3. 在临时目录重编译，生成新工件
    # 4. 计算新工件 sha256
    # 5. 比对：不一致 → fail（"工件与断言不同代，建议重生成"）
    # 注意：如果 command 含 -DBENCH_FULL 等宏，重编译时要带相同宏
```

#### 检查 2：断言字面量实测（E2，第五批踩过）

```python
def check_assert_labels_exist_in_artifact(card_path):
    """
    actual 中的每个断言标签必须在工件（.asm）中 grep 得到。
    Windows 侧走 sha 比对不检查断言，所以这条是 Windows 的盲区补全。
    """
    # 1. 从卡的 actual 提取所有断言标签（artifact_assert 中的 symbol/text）
    # 2. 在 artifact（.asm）中 grep 每个标签
    # 3. 找不到 → fail（"断言标签 X 在工件中不存在，可能是跨编译器未实测"）
    # 注意：contains_in/absent_in 的 text 也要检查
```

#### 检查 3：command 可执行

```python
def check_command_runnable(card_path):
    """
    command 必须在干净 checkout 能跑通（编译退出码 0）。
    """
    # 1. 从卡读 command
    # 2. 在临时目录执行 command
    # 3. 退出码非 0 → fail（"command 不可执行，退出码 X"）
    # 注意：含 cl/cl.exe 的卡跳过（MSVC 永久边界），标记 skip
```

#### 检查 4：.out 与断言同代

```python
def check_out_same_generation(card_path):
    """
    .out 的生成命令必须与卡的 command 一致（或 command 的子集）。
    如果 .out 是旧版本生成的 → fail。
    """
    # 1. 从 .out 文件头部读生成命令（如果 .out 有记录）
    # 2. 与卡的 command 比对
    # 3. 不一致 → fail（".out 与 command 不同代"）
    # 注意：如果 .out 没有记录命令，给 warn（"无法验证 .out 同代"）
```

#### 检查 5：活性对照

```python
def check_live_control(card_path):
    """
    卡的 actual 中至少有一个非编译期常量的读数（活性对照）。
    如果所有断言都是编译期折叠常量 → warn（"无活性对照，结论可能不可靠"）。
    """
    # 1. 从 actual 提取所有断言值
    # 2. 判断哪些是编译期常量（如 sizeof、functions_present=7）
    # 3. 如果全部是编译期常量 → warn
    # 注意：这是 warn 不是 fail，因为有些卡（如判据卡）确实只有常量
```

#### 检查 6：口径统一

```python
def check_metric_consistency(card_path):
    """
    卡中引用的所有数字在夹具/.out 中有对应输出。
    如果卡写了"pool 元数据 32 B"但 .out 里是 8056 B → fail。
    """
    # 1. 从卡的正文提取所有数字+单位（如 "32 B"、"18.86×"）
    # 2. 在 .out 中查找对应数字
    # 3. 找不到 → warn（"数字 X 在 .out 中无对应，可能口径不一致"）
    # 注意：这是启发式检查，可能误报，所以用 warn
```

#### 检查 7：无无限循环

```python
def check_no_infinite_loop(card_path):
    """
    夹具的 main() 必须有终止保证（有界循环或条件退出）。
    如果是 while(flag){} 且 flag 不会变 → fail。
    """
    # 1. 从卡读 fixture 路径
    # 2. 读 fixture 源码，检查 main() 中的循环
    # 3. 如果是 while(1)/for(;;)/while(flag) 且 flag 无写入 → fail
    # 注意：volatile flag 也算"可能终止"，只 warn
```

### Step 3：输出格式（JSON，与四工具一致）

```json
{
  "tool": "writer_selfcheck",
  "target": "evidence/mem/EV-MEM-040.md",
  "checks": [
    {"id": "WC-01", "name": "artifact_same_generation", "status": "pass"},
    {"id": "WC-02", "name": "assert_labels_in_artifact", "status": "pass"},
    {"id": "WC-03", "name": "command_runnable", "status": "pass"},
    {"id": "WC-04", "name": "out_same_generation", "status": "warn", "message": ".out 无生成命令记录"},
    {"id": "WC-05", "name": "live_control", "status": "pass"},
    {"id": "WC-06", "name": "metric_consistency", "status": "warn", "message": "数字 32 B 在 .out 中无对应"},
    {"id": "WC-07", "name": "no_infinite_loop", "status": "pass"}
  ],
  "summary": {"pass": 5, "warn": 2, "fail": 0},
  "exit_code": 0
}
```

### Step 4：注册到 cppbible.py

在 `tools/cppbible.py` 的 cmd_check 元组中新增 `writer_selfcheck`，使 `cppbible check --stage quality` 包含自检。

### Step 5：pytest

```python
class TestWriterSelfcheck:
    def test_artifact_same_generation_pass(self):
        # 用一张合法卡 → pass
        ...

    def test_artifact_same_generation_fail(self):
        # 构造卡：artifact_sha256 写错 → fail
        ...

    def test_assert_labels_in_artifact_fail(self):
        # 构造卡：断言标签不在工件中 → fail
        ...

    def test_command_runnable_skip_msvc(self):
        # 含 cl 的卡 → skip
        ...

    def test_no_infinite_loop_fail(self):
        # 构造夹具：while(1){} → fail
        ...

    def test_stock_atoms_zero_false_positive(self):
        # 存量 27 颗原子 + 56 张卡 → 0 fail（warn 可以有）
        ...
```

### Step 6：验证闭环（关键）

用第五批真实犯过的 E1/E2 错误回放：

```python
def test_fifth_batch_e1_e2_caught():
    """
    用第五批红队发现的 E1/E2 错误构造测试卡，确认自检能拦住。
    目标：拦住 ≥80%。
    """
    # E1 案例：EV-MEM-040 工件不同代（sha 旧）→ WC-01 应 fail
    # E2 案例：EV-MEM-040/041 断言字面量未实测 → WC-02 应 fail
    # E1 案例：.out 与 command 不同代 → WC-04 应 fail
    # ...
```

**这是验收的核心**——不是"7 项检查都实现了"，是"历史错误能拦住 ≥80%"。

### Step 7：全量门禁

```bash
python tools/writer_selfcheck.py evidence/mem/EV-MEM-040.md  # 单卡测试
python tools/gate_engine.py --check
python tools/atom_evidence_replay.py --check
python tools/poison_drill.py
python -m pytest tests/ -v
```

---

## 验收标准

- [ ] `tools/writer_selfcheck.py` 存在，7 项检查全部实现
- [ ] `cppbible check --stage quality` 包含自检
- [ ] pytest 含 TestWriterSelfcheck（≥6 例）
- [ ] 第五批 E1/E2 回放拦住 ≥80%（验证闭环）
- [ ] 存量 27 颗原子 + 56 张卡 0 fail（warn 可以有）
- [ ] replay confirm=56 refute=0
- [ ] gate block=0
- [ ] 独立 commit，message 含 `feat(tools): 413 Writer自检层 7项确定性检查零token`

---

## 不做的事

- 不做 E3/E4 语义错误检测（归红队）
- 不做自动修复（只检测，修复交 Writer）
- 不修改存量卡/原子
- 不 push
- 不混 414/417 的改动
