# 621 B1 · CI 竞态根治（gate + replay 加 needs）

> 改动文件：**仅** `.github/workflows/ci.yml`
> 未改 `gate_engine.py` / `atom_evidence_replay.py`（硬边界 §六.2）

---

## 一、竞态根因分析

### 1.1 现象

619 独立验收时 `gate_engine --check` 报出 2 条 BLOCK：

```
[BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-003.md
         卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
[BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-004.md
         卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
```

### 1.2 620 已证伪（不是数据问题）

620 任务1 复测确认：

- `Examples/atoms/_atom_lock_cost.asm` **确实存在**（28190 字节，git 已跟踪）；
- 两卡 `artifact_sha256 = d84c75168df0fda9…` 与 replay 独立重编译结果**逐字相符**；
- 稳态 `gate --check` 连跑 3 次均为 **191 命中 / block=0**，与冻结基线一致；
- 该文件 `LastWriteTime` 恰在验收会话期间 —— 被 replay 的 recompile 重写过。

### 1.3 真正的病灶：写者与读者并发

| job | 对 `Examples/atoms/` 的动作 |
|---|---|
| `replay` | **写**（recompile 以 `-o` 删旧写新重写 `.asm`） |
| `gate` | **读**（`EV-ARTIFACT-FILE-EXISTS` 检查工件存在性） |

在 620 之前的 ci.yml 中，这两个 job **都没有 `needs`，完全并行**
⇒ gate 可能在 replay「删掉旧文件、尚未写入新文件」的窗口内采样 ⇒ 假 BLOCK。

这在 CI 上是**真实存在的风险**：ci.yml 的 `replay` 与 `gate` 就是并行 job，
与 620 任务1 在本地复现竞态的条件**同构**。

---

## 二、修复方案：为什么选方案 A

提示词给了两个方案：

| 方案 | 内容 | 评价 |
|---|---|---|
| **A（采用）** | `gate` 加 `needs: [replay]` | ✅ **写者先、读者后** |
| B（不采用） | `replay` 加 `needs: [gate]` | ❌ 读者先、写者后 |

**选 A 的理由**：
- gate 的结论必须建立在**最终状态**的工件上。replay 写完后 gate 再读 ⇒ 读到的必然是最终态。
- 方案 B 则相反：gate 先判定，随后 replay 继续改写工件 ⇒ **gate 的结论立刻失效**
  （判完就被改），且没有任何机制让 gate 重判。这是更糟的语义。
- 一言以蔽之：**写者先、读者后**。

### 2.1 改动内容

```diff
   gate:
+    # 621 B1：**并发安全** —— gate 必须等 replay 跑完再启动。
+    # 根因：replay 的 recompile 会「删旧写新」重写 Examples/atoms/*.asm（如
+    # _atom_lock_cost.asm），而 gate 的 EV-ARTIFACT-FILE-EXISTS 要读同一批工件。
+    # 两者并行时，gate 可能采样到「删旧未写新」的中间窗口 ⇒ 报出**假的** BLOCK
+    # （619 验收的 2 条 BLOCK 误报即由此而来，620 任务1 已定位并证伪）。
+    # 故让 gate 依赖 replay：replay 写完后 gate 才读，读到的一定是最终状态。
+    # 注意：不要反向（replay needs gate）——那样 replay 会在 gate 判定之后继续改工件，
+    # gate 的结论立刻失效。方向必须是「写者先、读者后」。
+    needs: [replay]
     runs-on: ubuntu-latest
     timeout-minutes: 25
     steps:
```

### 2.2 修改前后的依赖关系对比

| job | 修改前 needs | 修改后 needs |
|---|---|---|
| quality | — | — |
| pytest | — | — |
| replay | — | — |
| **gate** | **—** | **`[replay]`** |
| compile | `[quality, pytest, replay, gate]` | 不变（gate 已传递依赖 replay） |
| publish-check | `[quality, pytest, replay, gate]` | 不变 |
| site / pdf / epub | `[compile, publish-check]` | 不变 |
| deploy | `[site, pdf, epub]` | 不变 |

### 2.3 语法验证

```
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
→ ci.yml YAML OK

jobs 依赖实测：
  quality=None pytest=None replay=None gate=['replay']
  compile=['quality','pytest','replay','gate']
  publish-check=['quality','pytest','replay','gate']
```

---

## 三、预期效果

1. **杜绝 619 那类 BLOCK 误报**：gate 不再与 replay 抢 `Examples/atoms/*.asm`。
2. **代价**：`gate` 从"与 replay 并行"变为"串在 replay 之后"，
   该路径 wall time 增加约一个 replay 的时长（replay timeout 上限 25min，实测通常数分钟）。
   ⇒ 这是**用时间换正确性**，对门禁而言是正确的取舍。
3. **不改变任何判定逻辑**：只改调度顺序，`gate_engine` 的规则一字未动
   ⇒ 不会引入新的漏报/误报，也不会改变 block/warn/advice 的判定口径。

---

## 四、诚实登记 / 局限

1. **本修复未在 CI 上实跑验证**（621 不 push，硬边界 §六.6）。
   CI 上的实际效果需推送后观察（属 §八 人拍板项 4）。
2. **只修了 gate↔replay 这一对**：其它共享资源（如 `quality` 的
   "Worktree Cleanliness" 步骤也读 `Examples/atoms/`）与 replay **仍然是并行的**。
   ⇒ 该步骤理论上也可能读到 replay 的中间态。本批**未处理**（见下）。
   - 缓解因素：该步骤检查的是 `git status --porcelain`，
     而 replay 正常会 restore/重写为与 HEAD 一致的内容，中间态窗口极短；
     且它判的是"工作树是否干净"，误报表现为**偶发红**，与 gate 的假 BLOCK 同类。
   - 留 622：考虑把 `quality` 也串在 replay 之后，或让 replay 改为**原子替换**写文件。
3. **更彻底的方案（未做）**：让 `atom_evidence_replay.py` 先写临时文件再
   `os.replace()` 原子替换 ⇒ 从根上消除"删旧未写新"窗口。
   但这要改 `atom_evidence_replay.py`，属**硬边界 §六.2 禁止**（B 线只改 ci.yml）。
4. `compile` / `publish-check` 仍并列依赖 replay 与 gate —— 因 gate 已 needs replay，
   二者实际都会在 replay 完成后才启动，无新增竞态。
