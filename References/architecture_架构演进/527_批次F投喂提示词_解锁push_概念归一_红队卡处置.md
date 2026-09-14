# 527 批次F投喂提示词 · 解锁push + 概念归一 + 红队卡处置

> 投喂对象：苦力（便宜模型）
> 路径：`C:\CodeLearnling\note\note\C++\CPP-Bible`
> 本批目标：**先把push解锁**（ahead约187个commit堵着），再修概念图谱根基污染。
> 每任务独立commit，含毒样例/pytest（若改规则）。不push、不golden accept（accept命令交人审）。

---

## 〇、开工前先实测（禁止凭记忆）

依次跑并记录数字：
```
python tools/golden_lock.py check        # 看 warn_findings 现在几→几
python tools/poison_drill.py             # 记录 passed/total、RULE-COVERAGE、exit code
python tools/cppbible.py check --stage quality   # 记录 "N passed / M failed" 及失败项名
```
**关键矛盾（必须复现）**：`poison_drill.py` 单跑 exit 0（83/83），但 `cppbible check --stage quality` 里 Poison Drill 报 FAIL。把这个矛盾复现并定位根因。

---

## 任务A：定位 quality 里 Poison Drill FAIL 的根因（P0）

**现象**：单跑 poison_drill exit 0；quality stage 里同一脚本 FAIL。

**排查方向（按序试，记录每条结果）**：
1. quality stage 里 Poison Drill 前一步是 Golden Lock。Golden Lock FAIL 时会不会改 `tools/golden_state.json`，而 poison_drill 读它导致 RULE-COVERAGE 分母变化？对比两次 `rule_coverage()` 的 covered/total/uncovered。
2. poison_drill 运行时写临时探针（line ~838/861 write_text）。复现时确保**没有其他agent/replay进程在跑**（`tasklist | findstr python`），排除并发污染。
3. 读 `tools/cppbible.py` quality stage 的失败处理：它是否在某步FAIL后仍继续，但把退出码聚合错了？看它怎么汇总各step的exit code。
4. 如果根因是**并发污染**（工作树被别的进程改）：报告即可，不要"修"——但要在 quality stage 里加一句前置检查：`Examples/atoms/` 有未提交改动就WARN提示"可能有并发replay"。
5. 如果根因是**确定性bug**：修它，配pytest。

**交付**：`_worklog_527.md` 里写清根因+证据（哪行代码/什么数字）。

---

## 任务B：解锁 push（两步，第二步交人审）

**B1（你做）**：复现 Golden Lock FAIL 的数字。预期：
```
[golden] WORSE warn_findings: 32 → 57
```
确认这57 = 31基线 + 26张存量卡的 STAGING warn（批次E claim_structured所致，预期漂移）。
把构成列出来：跑 `gate_engine --check`，把57条warn按规则名分组计数。

**B2（你只准备命令，不执行）**：人审accept命令是
```
python tools/golden_lock.py check --accept "批次E claim_structured STAGING 对存量26卡warn，基线32→57"
```
**你不许执行 --accept**。把命令写进 worklog，等监工执行。

**B3**：任务A修完、任务B2人审后，push应能过。你跑 `python tools/prepush_check.py` 确认9项全✅（此时quality也应绿），报告结果。

---

## 任务C：概念名归一（P1，修图谱根基）

**问题**：原子层概念名是"内存屏障(fence)"，Book/层51处口语"栅栏"。`concepts 栅栏` 查不到 → 同一概念成两个节点，矛盾检测/覆盖度全乱。

**做法**：
1. 新建 `tools/concept_aliases.txt`，格式 `规范名 <- 别名1, 别名2`：
   ```
   内存屏障(fence) <- 栅栏, memory fence, 内存栅栏
   互斥量(mutex) <- 锁, mutex
   # 先grep Book/和atoms/里高频概念口语名，再填
   ```
2. 改 `tools/knowledge_graph.py`：build 时把命题里的 subject/object 经 alias 表归一到规范名，再入 concept_edges。
3. 跑 `knowledge_graph.py build` + `stats`，报告归一后概念节点数（现在是3，预期会从Book层吸收更多概念）。
4. grep 验证：`Select-String -Path Book/ -Pattern "栅栏"` 确认这些别名都被alias表覆盖，没覆盖的列出来。

**不做**：不改Book/原文（那是教学文本）；只做图谱层归一。

---

## 任务D：3张red-team卡的人签缺口（P1）

**问题**（526自报）：ATOM-MEM-ALLOC-002 / ATOM-MEM-LEAK-002 / ATOM-MEM-PERF-004 是 red-team-verified，但无人级签署。按规则3，回填inference命题会被拦。

**做法**：
1. Read这三张卡，把各自的 claim 拆成 observation/inference 两类命题（照CONC-FENCE-001粒度）。
2. observation类：正常回填，跑OBSERVATION-NEEDS-ARTIFACT验证有工件支撑。
3. inference类：**不要硬填**。对每条inference命题，判断：
   - 有独立标准源（ISO/cppreference/知名commit）→ 填 external_basis 并登记到独立来源表
   - 纯作者推断无标准源 → 标 `needs_human_review: true`，**不强行claim_type: inference+verified**，留在worklog等人签
4. 报告：3张卡各拆了几条命题、几条observation过了、几条inference挂起待签。

**铁律**：拿不准claim_type的，标inference并注明，绝不擅自定observation假装机验过。

---

## 任务E：26张存量卡采样回填（P2，不做完全部）

**不要求**一次回填26张（那是机械体力，且会跨多窗口）。**本批只做3张**：
- 从 `tools/claim_structured_staging.txt` 选3张最完整的原子（优先mem域）
- 照CONC-FENCE-001粒度拆命题
- 回填后跑gate/poison/replay确认零误伤
- 剩下23张列进backlog（worklog里列ID+一句话选题），下批再做

---

## 铁律

1. 不push、不golden accept
2. 一任务一commit；改规则才配毒样例+pytest
3. **存量零误伤**：每步 gate --check 对比 warn 数变化，不许新增 BLOCK
4. 不编造：跑出来的数字如实记录，拿不准的claim标inference
5. 任务A修quality里poison前，先确认不是并发污染（tasklist查python进程）
6. 工作树有其他agent并发时，先等其退出再跑全量门禁（526 replay_busy教训）

---

## 收工验收（fresh run）

```
python tools/golden_lock.py check       # 记录warn数（人审accept前应仍FAIL，预期）
python tools/poison_drill.py            # exit 0
python tools/cppbible.py check --stage quality   # 记录 N passed / M failed（任务A修后M应=0，除golden待accept）
python tools/knowledge_graph.py build && python tools/knowledge_graph.py stats
pytest -m fast
```

写 `_worklog_527.md`：
- 任务A根因结论+证据
- 任务B warn 57的分组构成表
- 任务C alias表内容+归一前后概念数
- 任务D 3张卡命题拆分结果
- 任务E 回填了哪3张 + 23张backlog清单

---

## 明确不做

- 不执行 --accept（人审权）
- 不一次回填26张卡
- 不改Book/教学原文
- 不push
- 不新增大工具目录（都在现有文件改）
- 不碰 L2调度层/多模型路由（那是更后批次）

---

## 为什么这一批

push堵着187个commit，再不解锁，所有新成果都在本地攒着、CI看不到、风险累积。任务A是解锁的技术前提，任务B是解锁的人审动作。任务C修的是概念图谱的根基污染——不做归一，后面知识图谱越建越歪。任务D/E是把526点火的claim结构化从"样板"推向"全库"的第一步。

---

*文档编号 527。批次F提示词，直接投喂苦力。*
