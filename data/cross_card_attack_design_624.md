# 624 A1 · 跨卡一致性攻击设计（H4 策略升级：多卡修改）

> 工具：`tools/cross_card_attack_624.py`（复用 `sandbox_apply_622.py` 的单卡沙箱 + gate JSON 工具）
> 目的：突破 623 的「载体天花板」——单卡 field-edit 只能触达 26/63 规则；跨卡攻击触达卡间一致性规则。

---

## 一、跨卡修改机制（继承 622 六重护栏并扩展到 N 卡）

| # | 护栏 | 624 扩展 |
|---|---|---|
| 1 | 字节级备份 | apply 前把**每张**目标卡读成 bytes 存内存（`apply_multi` 逐卡备份） |
| 2 | finally 必还原 | `apply_and_run_multi` 的 `try/finally` 保证异常/超时也还原**所有**被改卡 |
| 3 | 还原校验 | `restore_multi` 逐卡重算 sha256 与原比对，任一不符报 `restore_failed` |
| 4 | 并发锁 | 复用 `data/.622_apply.lock`（同时只允许一个 apply_and_run） |
| 5 | 超时保护 | gate 子进程 `timeout=30s` |
| 6 | 路径白名单 | 只允许改 `atoms/`、`evidence/`（多卡同规则） |
| + | **失败回滚** | `apply_multi` 中任一卡施加失败 ⇒ 立即还原此前已施加的卡（原子性） |

## 二、4 种跨卡攻击策略

| 策略 | 名称 | 构造 | 目标规则（预测） |
|---|---|---|---|
| **X1** | 悬空引用 | A 引用 B，把 B 的 `id` 改掉 ⇒ A 的引用悬空、B 成孤儿 | ATOM-REL-TARGET / ATOM-ID-UNIQUE / EV-SERVES-EXIST |
| **X2** | 循环引用 | A 追加 `prerequisite→B`、B 追加 `prerequisite→A`（依赖环） | ATOM-REL-DAG / ATOM-REL-TARGET |
| **X3** | 矛盾引用 | A 追加 `supports→B`、B 追加 `contradicts→A`（卡间矛盾） | ATOM-REL-CONFLICT / ATOM-REL-TARGET / ATOM-REL-DAG |
| **X4** | 孤儿引用 | 证据 `serves→不存在原子` + `artifact→不存在文件` + 原子 `misconceptions→不存在误解` | EV-SERVES-EXIST / ATOM-MISCONCEPTION-REF / EV-ARTIFACT-FILE-EXISTS |

## 三、60 条跨卡 mutation（4 策略 × 15）

- **复杂度评分**：X1=55+3·(n−2)…（base 66/72/78/70，随编辑卡数递增，全部 >60，目标达「高复杂度带」）。
- **去重**：按 `(strategy, 卡组合, op)` 天然区分；与 v7 既有 1593 + 623 的 120 条载体不同（多卡 vs 单卡）。
- **预测触达新规则（A1 目标 >15 条新，累计 >40/63）**：见 `STRATEGY_PREDICT`，四策略并集含
  ATOM-REL-CONFLICT、ATOM-MISCONCEPTION-REF、EV-ARTIFACT-FILE-EXISTS、ATOM-REL-DAG 等 623 盲区。

## 四、安全护栏确认

- 工具自检 `--check`（13 例）**PASS**；自检内含「多卡 apply+restore 后 sha256 不变」验证。
- 自检后 `git diff --quiet -- atoms evidence` **CLEAN**（受控目录零污染）。
- 所有修改只在沙箱临时模式（备份+还原），**不修改原始卡**，**不修改 gate_engine.py**。

## 五、局限性声明

1. **跨卡语义受 gate 规则实际覆盖限制**：gate_engine.py 无专门的「跨卡一致性」检查族；X1–X4 主要通过
   既有引用类规则（ATOM-REL-DAG/TARGET、EV-SERVES-EXIST、ATOM-MISCONCEPTION-REF 等）触发 ⇒ 实际触达
   以 A2 沙箱实跑为准，A1 预测为启发式。
2. **「矛盾引用」依赖 ATOM-REL-CONFLICT 的触发条件**（A supports B 且 B contradicts A）；若规则另有共存
   前置（如 status/证据绑定），可能不触发（A3 分析）。
3. **风险性**：多卡编辑扩大了对受控目录的临时改动面，故护栏升级为「逐卡 sha256 校验 + 失败回滚 + finally 还原」。
4. **复杂度评分为代理值**（按策略/编辑卡数映射），非 AST/语义精确度量。
