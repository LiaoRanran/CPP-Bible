# 465 · 苦力 Agent 下一轮执行提示词

> 投喂对象：苦力 Agent（便宜模型，确定性杂活）
> 前置：464 二十轮调研整合已入库（8e20bef）；用户已授权 ccache 安装
> 铁律：不 push、不 golden sync、人审前不 commit 工具改动（本提示词内的 commit 均为用户预授权的工具落地）

---

## 〇、开工前必读（防止凭记忆写代码）

1. `Read tools/gate_engine.py` — 确认当前规则注册表、DAG_REL/CONFLICT_REL、warn 处理逻辑
2. `Read tools/atom_evidence_replay.py` — 确认 _command_uses_msvc、EV-ARTIFACT-PRODUCER、三分类（confirm/refute/infra_error）当前实现
3. `Read tools/poison_drill.py` — 确认 gate_exit_code()、RULE-COVERAGE 当前状态
4. `Read tools/cppbible.py` — 确认 cmd_check 元组，新工具必须登记
5. `git log --oneline -5` — 确认 417（ed6297e）是否已提交；若未提交，先完成它
6. `git status --short` — 确认当前工作树有哪些未提交改动，先收尾再开新活

---

## 一、任务 A：ccache 安装与 replay 集成（464-T1，用户已授权）

### A1. WSL 安装 ccache
```bash
wsl -e bash -c "sudo apt-get update && sudo apt-get install -y ccache && which ccache && ccache --version"
```
若 apt 失败，尝试：
```bash
wsl -e bash -c "cd /tmp && wget https://github.com/ccache/ccache/releases/download/v4.10/ccache-4.10-linux-x86_64.tar.xz && tar xf ccache-4.10-linux-x86_64.tar.xz && sudo cp ccache-4.10-linux-x86_64/ccache /usr/local/bin/ && ccache --version"
```

### A2. Windows 侧评估（可选，若 WSL 成功则跳过）
- `where ccache` 确认 Windows 侧是否已有
- 若无，不自动安装（Windows 侧 replay 用 MinGW，ccache 对 MinGW 支持有限），只在 WSL 侧集成

### A3. replay 集成
修改 `tools/atom_evidence_replay.py`：
- 编译命令前缀从 `g++` 改为 `ccache g++`（仅 WSL 路径，Windows MinGW 不改）
- 检测 `which ccache` 可用性，不可用时回退到 `g++`（标 infra_error:ccache_unavailable 但不阻断，继续用 g++）
- ccache 配置：`CCACHE_DIR=/tmp/ccache_cache`，`CCACHE_MAXSIZE=2G`
- 实测：全量 replay 56 卡，记录首次耗时（冷缓存）和二次耗时（热缓存）

### A4. 验证
- 冷缓存：`ccache -C` 清空后跑 `python tools/atom_evidence_replay.py --check`，记录耗时
- 热缓存：立即再跑一次，记录耗时
- 预期：热缓存 replay 从 ~2min 降到 ~10s（编译命中 ccache）
- 确认 confirm=56/refute=0/infra_error=0（ccache 不改变编译结果）

### A5. 提交
- 只提交 `tools/atom_evidence_replay.py` 的改动
- commit message: `feat(replay): WSL 侧集成 ccache，热缓存全量 replay 从 Xs 降到 Ys`
- 不提交 ccache 缓存目录（.gitignore 加 `/tmp/ccache_cache` 不适用，因为在 /tmp）

---

## 二、任务 B：规则渐进发布机制（464-T2，零成本）

### B1. 规则状态字段
在 `tools/gate_engine.py` 的规则注册表中，每条规则增加 `status` 字段：
- `experimental`：只 warn，不 block（新规则默认）
- `stable`：可 block（经过 ≥1 批次观察，误报率 < 5%）
- `deprecated`：只 warn，计划删除（给过渡期）

### B2. 渐进发布流程
- 新规则加入时默认 `status: experimental`，只产生 warn
- 经过 ≥1 个完整批次（≥3 颗原子生产）后，若误报率 < 5%，可升 `stable`
- 升级需在 commit message 中记录：规则名、观察批次数、误报数/总数
- `--list` 输出增加 status 列

### B3. 存量规则处理
- 当前 42+ 条规则全部标 `stable`（已验证）
- 新增规则（如未来的 ATOM-REL-CONFLICT 若还没合）先标 `experimental`
- warn 32 条中，属于 experimental 规则的 warn 不计入"技术债"（单独计数）

### B4. 验证
- `python tools/gate_engine.py --list` 确认每条规则有 status
- `python tools/gate_engine.py --check` 确认 block=0（存量规则不受影响）
- 新增一条测试规则（experimental），确认它只 warn 不 block
- pytest 增加 2 例：experimental 规则不 block、stable 规则可 block

### B5. 提交
- `tools/gate_engine.py` + `tests/test_gate_engine.py`
- commit message: `feat(gate): 规则渐进发布——experimental/stable/deprecated 三状态，新规则先 warn 观察`

---

## 三、任务 C：对抗稳态假设形式化（464-T3，更新 452 补充）

### C1. 写 452 补充文档
新建 `References/architecture_架构演进/452B_对抗稳态假设补充.md`：
- 每个攻击用例必须声明稳态假设：`在 [攻击X] 下，[门禁指标Y] 应 [维持/变化]`
- 示例：
  - "在 cl 卡免检攻击下，gate block 应非零（否则 verified 可直推）"
  - "在编译后覆写攻击下，replay 应 refute 或 infra_error（否则 confirm 是假阳性）"
  - "在 contains_in 通用符号攻击下，gate 应 block（否则断言无判别力）"
- 逃逸判定：若攻击后稳态假设被违反（如 gate block=0），记为"逃逸成功"
- 拦截率计算：`拦截数 / (拦截数 + 逃逸数)`，按攻击类别分组

### C2. 回溯 402 对抗结果
- 读取 `_adv_v61/REPORT.md`（若存在），将 13 个逃逸按稳态假设重新分类
- 确认每个逃逸都有对应的稳态假设违反
- 输出：`docs/kernel/402_逃逸稳态假设分析.md`

### C3. 提交
- 452B 补充文档 + 402 回溯分析
- commit message: `docs(architecture): 452B 对抗稳态假设形式化 + 402 逃逸回溯分类`

---

## 四、任务 D：每原子成本 trace（464-T4，412 数据来源）

### D1. trace JSON 格式
在 `tools/atom_evidence_replay.py` 或新工具 `tools/cost_trace.py` 中，定义：
```json
{
  "trace_id": "ATOM-MEM-RAII-001_2026-09-13",
  "spans": [
    {"name": "fixture_compile", "duration_ms": 1200, "token_estimate": 0},
    {"name": "evidence_card_write", "duration_ms": 0, "token_estimate": 3500},
    {"name": "red_team", "duration_ms": 0, "token_estimate": 15000},
    {"name": "gate_check", "duration_ms": 300, "token_estimate": 0},
    {"name": "replay_verify", "duration_ms": 8000, "token_estimate": 0}
  ],
  "total_tokens_estimate": 18500,
  "total_wall_time_ms": 9500
}
```

### D2. 采集点
- 夹具编译：replay 已有耗时，直接记录
- 红队：红队子 agent 的 token 数（若可获取）或估算（按工具调用次数 × 平均）
- 卡写作：无法自动采集，留空（由 Writer 自报）
- 门禁：gate/replay/poison 耗时

### D3. 输出
- 每颗原子生产完成后，trace JSON 写入 `traces/ATOM-{ID}.json`
- `traces/` 加 .gitignore（不入库，本地数据）
- 汇总脚本：`tools/cost_summary.py`，输出每批次平均 token/耗时

### D4. 验证
- 对 1 颗已完成原子（如 ATOM-CONC-FENCE-001）手动生成 trace JSON
- 确认格式合法、字段完整
- 不修改现有门禁逻辑

### D5. 提交
- `tools/cost_trace.py`（新工具，必须登记到 cppbible.py cmd_check）
- `tools/cost_summary.py`（新工具）
- `.gitignore` 加 `traces/`
- commit message: `feat(cost): 每原子 trace JSON + 汇总脚本，为 412 成本核算提供数据来源`

---

## 五、任务 E：414 P0 收尾（若未完成）

### E1. 确认状态
- `git log --oneline | grep -i "414\|F01\|F02\|cl.*免检\|编译后覆写"`
- 若 F01（cl 免检链的 verified 绑定）和 F02（编译后覆写的根本解法）已修，跳过
- 若未修，按 414 文档规格执行

### E2. F01 根本解法（若未修）
- 当前 `_command_uses_msvc` 标 infra_error:msvc_unavailable，但 gate 只认 verdict:confirm
- 修法：gate 的 S2 检查增加——若卡的 command 含 cl/cl.exe/clang-cl，verdict 必须是 `infra_error` 而非 `confirm`，否则 block
- 毒样例：P32（cl 卡写 verdict:confirm → block）

### E3. F02 根本解法（若未修）
- 当前 EV-ARTIFACT-PRODUCER 检查 producer 段逐字在 command + -o 目标==artifact
- 但"编译后覆写"（真编译行 + python 覆写工件）可绕过
- 根本解法（426 InvariantChecker）：解析 command 的所有写操作（>、>>、cp、mv、python 写文件、tee），若 artifact 被多个写操作触及，标 warn（"artifact 可能被覆写，需人工确认"）
- 不做完整的 InvariantChecker（太重），只做"多写操作检测"

### E4. 验证
- 毒样例 P32/P33 通过
- 存量 56 卡零误伤
- pytest 全绿

---

## 六、执行顺序与停止条件

### 顺序
1. **先收尾当前工作树**：`git status` 看有什么未提交，若 writer_selfcheck 已完成则提交（若未完成，先完成它）
2. **任务 E**（414 P0 收尾，若未完成）—— 最优先，因为是已知阻断
3. **任务 A**（ccache）—— 用户已授权，加速后续所有 replay
4. **任务 B**（规则渐进发布）—— 零成本，治理 warn 债务
5. **任务 C**（对抗稳态假设）—— 文档工作，不碰代码
6. **任务 D**（成本 trace）—— 新工具，为 412 铺路

### 停止条件（任一触发即停手等用户）
1. 任何任务需要修改 `atoms/`、`evidence/`、`misconceptions/` 下的正式文件（本提示词只动 tools/、tests/、docs/architecture/）
2. 门禁出现 block 且无法在 2 轮内修复
3. ccache 安装失败（WSL 无网络/无权限）
4. 414 P0 的修法与 414 文档规格冲突（需用户裁决）
5. 上下文耗尽（写工作日志 `_worklog_465.md` 记录进度）

### 每任务完成后必须
- 跑 `python tools/gate_engine.py --check`（block=0）
- 跑 `python tools/poison_drill.py`（全过）
- 跑 `python -m pytest tests/ -x`（全绿）
- 跑 `python tools/atom_evidence_replay.py --check`（confirm=56）
- 单独 commit，不混批

---

## 七、交付物清单

| 任务 | 交付物 | 预期 commit |
|---|---|---|
| A | tools/atom_evidence_replay.py（ccache 前缀） | 1 条 |
| B | tools/gate_engine.py（status 字段）+ tests | 1 条 |
| C | 452B 文档 + 402 回溯分析 | 1 条 |
| D | tools/cost_trace.py + cost_summary.py + .gitignore | 1 条 |
| E | tools/atom_evidence_replay.py + gate_engine.py + 毒样例 | 1-2 条 |

总计：4-6 条 commit，均不 push（铁律 7）。

---

## 八、诚实报告要求

每轮结束时报告：
1. 完成了哪些任务（commit hash）
2. 哪些任务未完成，原因
3. 门禁结果（gate/poison/pytest/replay 数字）
4. 发现的新问题（若有）
5. 下一步建议

**禁止**：用"基本完成""大致 OK"等模糊表述。数字必须实跑，问题必须挂行号/命令。
