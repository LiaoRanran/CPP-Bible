# 621 E1 · 620 交人项处理 + 化债

> 来源：`data/620_acceptance_report.md` §九（8 条交人项）+ 621 本批新增项

---

## 一、620 交人项处理状态（8 条）

| # | 620 交人项 | 类别 | 621 处理 | 状态 |
|---|---|---|---|---|
| 1 | 攻击目标权重拍板（W1 保守 vs W2 校准锚定） | 人拍板 | 621 未代决；A4 用 W2 跑第二轮（沿用 620 建议），**权重仍待人拍板** | ⏸ 留人 |
| 2 | 是否启用 Authority 接口替换现有人审通道 | 人拍板 | 621 C 线新增 pending 通道与脱敏，**未启用替换** | ⏸ 留人 |
| 3 | PCK 是否成为权威源（83 张已就绪） | 人拍板 | 未变更；621 C3 仅新增 `abstain_state`，**权威源地位仍待人拍板** | ⏸ 留人 |
| 4 | schema 升级支持 `abstain` / `conditionally_authorized` | 可机器 + 人拍板 | 621 C1/C3 **实现了 6 态与 `abstain_state` 字段**，但 **619 B1 schema 文档未同步更新**（冻结件，改它需人审） | 🟡 半完成 |
| 5 | 是否 push（620 未 push ⇒ 未经 CI 实跑） | 人拍板 | 621 仍未 push（硬边界 §六.6） | ⏸ 留人 |
| 6 | 工具命名规范（新批次强制 `_NNN`，存量 41 个不改名） | 可机器确认 | **本批确认采纳**：621 的 9 个新工具全部带 `_621` 后缀 ✅ | ✅ 已化 |
| 7 | CI 竞态修复：`gate` 与 `replay` 并行 ⇒ 建议加 `needs` | 可机器 | **621 B1 已修**（`gate needs: [replay]`）+ **B3 追加发现** `quality` 同样竞态并已修 | ✅ 已化 |
| 8 | 沙箱 API：`mutation_fuzz` 缺"施加到副本"接口 | 前置/人拍板 | **仍未解除**（621 A 线改用"生成 + 预测判决"绕行）；620 A1 沙箱接口在 621 **未被修改、保持稳定**（A4 直接复用 `run_loop`） | ⏸ 留人（仍是根本瓶颈） |

**小计**：✅ 已化 2 条（#6 #7）· 🟡 半完成 1 条（#4）· ⏸ 留人 5 条（#1 #2 #3 #5 #8）

---

## 二、本批化债内容（可机器处理的都做了）

### 2.1 CI 竞态根治（B 线，#7）

| 动作 | 内容 |
|---|---|
| **根因** | `replay` 写 `Examples/atoms/*.asm`，`gate` / `quality` 读同目录，**并行无依赖** ⇒ 采样到"删旧未写新"窗口 ⇒ 假 BLOCK（619 那 2 条） |
| **修复** | ci.yml：`gate needs: [replay]`（B1）+ `quality needs: [replay]`（B3 追加） |
| **固化** | 新增 `concurrency-safety` job + `tools/ci_concurrency_check_621.py`，静态校验"写者先、读者后"不变量 |
| **验证** | Ci.yml YAML 语法 OK；并发检查 **通过**（`REAL_EXIT:0`） |
| **未验证** | CI 实际运行（621 不 push） |

### 2.2 命名规范确认（#6）

- 621 新建 9 个工具，**全部**带 `_621` 后缀：
  `mutation_generator_621` / `mutation_quality_621` / `ci_race_reproducer_621` /
  `ci_concurrency_check_621` / `abstain_classifier_621` / `pck_abstain_sync_621` /
  `human_review_quality_compare_621` / `human_review_anonymize_621` / `run_621_gate`。
- 存量 41 个带批次后缀工具**未改名**（沿用 620 D3 结论：318 处引用，成本 ≫ 收益）。
- **新增偏差（如实登记）**：D1 需要可测试的代码，新增了第 10 个工具
  `tools/authority_pending_621.py`（提示词任务表未列此工具）。

### 2.3 沙箱接口稳定性确认（#8 部分）

- 621 A4 直接复用 `tools/adversarial_loop_620.py` 的 `run_loop()`，**未做任何修改** ⇒ 接口稳定 ✅
- 但"把 mutation 施加到沙箱副本"的能力**仍不存在**（`mutation_fuzz.py` 依旧只读基线生成器）
  ⇒ VFDR 仍无法真正脱离"预测口径"。**这是 621 最大的未解项。**

### 2.4 其它化债

| 项 | 处理 |
|---|---|
| 619 计数误差（57→53） | 620 D1 已修；621 未再变更 |
| 本机 `.venv` 解释器损坏（uv junction 不可遍历，error 448） | **本批修复**：以 base 解释器 3.13.13 恢复 `.venv\Scripts\python.exe`（详见 §四） |

---

## 三、仍留交人的项（621 之后）

| # | 项 | 为什么留人 |
|---|---|---|
| 1 | **攻击目标权重拍板**（W1 vs W2） | 价值排序，非技术问题 |
| 2 | **Authority 接口是否启用**替换现有人审通道 | 治理变更 |
| 3 | **PCK 是否成为权威源** | 权威性声明 |
| 4 | **schema 文档升级**（写入 `abstain_state` 等） | 619 B1 schema 是冻结件 |
| 5 | **是否 push**（含 CI 竞态修复的远程验证） | 发布决策 |
| 6 | **沙箱 apply API** 是否建设 | 需架构决策 + 可能触及 `mutation_fuzz`（受控） |
| 7 | **新 mutation 是否纳入 v8 基线** | 621 §八.1 |
| 8 | **ABSTAIN 是否对外展示**（写入 PCK 渲染） | 621 §八.2 |
| 9 | **30 条逐条人审是否执行** | 621 §八.3，D1 只建待审条目 |
| 10 | **脱敏数据是否开源** | 621 §八.5 |

---

## 四、环境修复记录（本批新增）

**问题**：621 D1 提交后，`.venv\Scripts\python.exe`（uv trampoline）开始报
`uv trampoline failed to spawn Python child process / entity not found (os error 2)`。

**根因**：uv 管理的 `%APPDATA%\uv\python\cpython-3.13-windows-x86_64-none` 是一个
**junction**，指向 `cpython-3.13.13-windows-x86_64-none`；该 junction 变得**不可遍历**
（Windows `os error 448`：包含不受信任的装入点）。uv 自身也无法重建
（`Failed to create Python minor version link directory`）。

**修复**（三步，均在 `.venv` 内或 uv 缓存内，**不触碰仓库受控目录**）：
1. 将损坏 junction 重命名为 `cpython-3.13-windows-x86_64-none.broken`（**未删除任何目标目录**）
2. 新建 junction 指向 versioned 目录 —— 仍不可遍历（环境限制）
3. **最终方案**：把 base 解释器的 `python.exe` / `pythonw.exe` / `python313.dll` /
   `python3.dll` / `vcruntime140.dll` / `vcruntime140_1.dll` 复制进 `.venv\Scripts\`，
   并将原 trampoline 备份为 `python.exe.uv-trampoline.bak`

**结果**：`.venv\Scripts\python.exe -c "import yaml, pytest"` → **OK（3.13.13 / pytest 9.1.1）**

**影响评估**：
- `.venv` 不在版本控制内（gitignored）⇒ **不影响仓库交付物**
- CI 在 Linux 上自建环境，**不受此影响**
- ⚠ 若 uv 日后重新管理该 venv，可能会覆盖此修复（属本地环境事项，交人知悉）
