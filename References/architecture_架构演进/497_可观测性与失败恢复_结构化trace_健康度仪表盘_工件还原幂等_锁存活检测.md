---
id: 497
title: 可观测性与失败恢复 结构化trace 健康度仪表盘 工件还原幂等 锁存活检测
status: active
type: architecture-note
created_at: 2026-09-14
---
# 485 可观测性与失败恢复落地方案
## 结构化 trace + 健康度仪表盘 + 工件还原幂等 + 锁存活检测

> 生成时间：2026-09-14
> 来源：483 差距分析 P1 级 + 真实事故（N1 僵尸锁、N4 工件丢失、E09 并发假失败）

---

## 一、可观测性

### 1.1 问题

系统运行时没有监控：
- 没有结构化 trace（每次 replay/gate 的耗时、失败原因）
- 没有告警（门禁红了、replay 失败了，谁通知？）
- 没有仪表盘（当前系统健康度一眼可见）
- 没有历史趋势（规则命中率、replay 耗时、成本随时间变化）

当前只有 `metrics_snapshot.py`（22KB，零测试），但没有形成完整的可观测性体系。

### 1.2 改法：三层可观测性

#### 层 1：结构化 trace 日志（JSONL）

所有工具运行时写 trace 日志到 `build/traces/`：

```json
// build/traces/replay_2026-09-14T10-00-00.jsonl
{"ts": "2026-09-14T10:00:01", "tool": "replay", "card": "EV-MEM-040", "stage": "compile", "duration_ms": 1234, "status": "ok"}
{"ts": "2026-09-14T10:00:02", "tool": "replay", "card": "EV-MEM-040", "stage": "sha_verify", "duration_ms": 45, "status": "ok"}
{"ts": "2026-09-14T10:00:03", "tool": "replay", "card": "EV-MEM-041", "stage": "compile", "duration_ms": 5678, "status": "failed", "error": "compile_timeout", "rc": 124}
```

每个工具的关键阶段都写 trace：
- replay：compile / run / sha_verify / artifact_assert / run_match / sanitizer / restore
- gate：rule_check / 每条规则的耗时和命中
- poison：每个毒样例的运行结果

#### 层 2：健康度仪表盘

`tools/health_dashboard.py`（约 100 行），输出系统健康度摘要：

```
=== 阙疑系统健康度 2026-09-14 ===
门禁: gate block=0 warn=32 | poison 61/61 | pytest 272 | replay 56/0/0 ✅
性能: 全量 replay 300s（ccache 热缓存）| CI 12min
质量: 规则有效命中率 24% | 零断言测试 32 | 孤儿卡 1
成本: 本批 token 5765/颗 | 红队校准率 67%
趋势: replay 耗时 ↓20% | 规则数 ↑3 | warn 持平
告警: ⚠️ 39 条规则零命中 | ⚠️ 11 个工具零测试
```

接入 CI，每次运行后输出健康度摘要。

#### 层 3：告警机制

简单的告警规则（不需要复杂系统）：
- gate block > 0 → 🔴 严重
- replay confirm < 基线 → 🔴 严重
- pytest 失败 → 🔴 严重
- warn 增长 >5 条 → 🟡 警告
- 新规则零命中 >1 个月 → 🟡 警告
- 单颗原子成本 > 阈值 → 🟡 警告

告警输出到 CI 日志和健康度仪表盘。

### 1.3 具体实现

1. 写 `tools/trace.py`（约 50 行）：统一的 trace 日志接口
2. 修改 replay/gate/poison，在关键阶段写 trace
3. 写 `tools/health_dashboard.py`（约 100 行）：聚合 trace + metrics，输出健康度
4. CI 中加一步：运行 health_dashboard，输出摘要

### 1.4 验收

- 每次 replay/gate 运行都有结构化 trace
- 健康度仪表盘一眼可见系统状态
- 告警规则生效（严重问题 🔴，警告 🟡）
- trace 日志可用于事后分析（为什么这次 replay 慢了？哪条规则最耗时？）

---

## 二、失败恢复

### 2.1 真实事故回顾

| 事故 | 根因 | 影响 |
|---|---|---|
| N1 僵尸锁 DoS | replay 锁只按 mtime 判陈旧（3600s），无 pid 存活检测 | 进程被杀后整条 replay 1 小时不可用 |
| N4 工件永久丢失 | replay「删工件→重生成→finally 还原」在进程被杀时还原不执行 | EV-MEM-027 的 .asm 被清空（426 行全删） |
| E09 并发假失败 | 并发 replay 无锁，6/6 轮假失败 | CI 随机红 |

### 2.2 改法：四个失败恢复机制

#### 2.2.1 replay 锁存活检测（修复 N1）

当前：`_acquire_replay_lock()` 只按 mtime 判陈旧（stale=3600s），无 pid 检测。

改法：
- 锁文件写 pid：`{"pid": 12345, "started_at": "..."}`
- 取锁时检查 pid 是否存活：`os.kill(pid, 0)`（Windows 用 `psutil` 或 `tasklist`）
- pid 不存在 → 锁是僵尸，直接接管
- stale 阈值从 3600s 缩到 300s
- `atexit` + `signal` 注册释放锁的回调

```python
# 伪代码
def _acquire_replay_lock(timeout=600):
    lock_path = ROOT / "build" / ".replay_lock"
    while True:
        try:
            with open(lock_path, 'x') as f:
                json.dump({"pid": os.getpid(), "started_at": now()}, f)
            return True
        except FileExistsError:
            # 检查锁是否是僵尸
            with open(lock_path) as f:
                lock_data = json.load(f)
            if not _pid_alive(lock_data['pid']):
                # 僵尸锁，接管
                os.remove(lock_path)
                continue
            # 检查是否过期
            if now() - lock_data['started_at'] > 300:
                os.remove(lock_path)
                continue
            # 等待
            time.sleep(1)
```

#### 2.2.2 工件还原幂等化（修复 N4）

当前：replay 先删工件→重生成→finally 还原。进程被杀时 finally 不执行，工件永久丢失。

改法：
- 不删原工件，先复制到 `.bak`
- 重生成到临时文件
- 用原子替换（`os.replace`）把临时文件移到目标位置
- 还原时：如果 `.bak` 存在，原子替换回来；如果 `.bak` 不存在（已经还原过），不做任何事（幂等）

```python
# 伪代码
def _swap_artifact(artifact_path, new_content):
    """原子替换工件，保留 .bak 用于还原"""
    bak_path = artifact_path.with_suffix('.bak')
    tmp_path = artifact_path.with_suffix('.tmp')
    
    # 1. 备份原工件（只备份一次）
    if not bak_path.exists():
        shutil.copy2(artifact_path, bak_path)
    
    # 2. 写新内容到临时文件
    tmp_path.write_text(new_content)
    
    # 3. 原子替换
    os.replace(tmp_path, artifact_path)

def _restore_artifact(artifact_path):
    """幂等还原：.bak 存在就还原，不存在就跳过"""
    bak_path = artifact_path.with_suffix('.bak')
    if bak_path.exists():
        os.replace(bak_path, artifact_path)  # 原子替换
```

#### 2.2.3 并发 replay 隔离（修复 E09）

当前：并发 replay 无锁，6/6 轮假失败。

改法：
- 470 P0-G1 已做了独占锁 + 陈旧接管 + infra_error:replay_busy
- 但锁的粒度是"全局"（一次只能跑一个 replay）
- 优化：按卡粒度加锁（不同卡可以并发跑，同一张卡串行）

```python
# 伪代码
def _card_lock_path(card_id):
    return ROOT / "build" / f".replay_lock_{card_id}"

def replay_card(card_path):
    lock_path = _card_lock_path(card_id)
    with _acquire_lock(lock_path, timeout=60):
        # 跑这张卡的 replay
```

#### 2.2.4 工具崩溃 dump 现场

任何工具崩溃时（未捕获异常），自动 dump：
- 崩溃时的输入参数
- 崩溃时的工作目录状态
- 最近的 trace 日志
- 堆栈信息

dump 到 `build/crash_dumps/<timestamp>/`，方便事后分析。

```python
# 伪代码
import traceback, atexit

def crash_dump(exc_type, exc_value, exc_tb):
    dump_dir = ROOT / "build" / "crash_dumps" / datetime.now().isoformat()
    dump_dir.mkdir(parents=True, exist_ok=True)
    (dump_dir / "traceback.txt").write_text(traceback.format_exc())
    (dump_dir / "context.json").write_text(json.dumps({
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "git_head": _git_head(),
    }))
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = crash_dump
```

### 2.3 验收

- replay 锁有 pid 存活检测，僵尸锁 300s 内自动接管
- 工件还原幂等（进程被杀后重启，工件能自动恢复）
- 并发 replay 按卡粒度隔离，不同卡可并发
- 工具崩溃自动 dump 现场
- N1/N4/E09 三类事故不再发生

---

## 三、两项的优先级与依赖

| 项 | 成本 | ROI | 优先级 | 依赖 |
|---|---|---|---|---|
| 结构化 trace | 低（50 行接口 + 各工具埋点） | 高（事后分析能力） | P1 | 无 |
| 健康度仪表盘 | 低（100 行） | 中（一眼可见状态） | P1 | 结构化 trace |
| 锁存活检测 | 低（改 _acquire_replay_lock） | 极高（修复 N1 真实事故） | P0 | 无 |
| 工件还原幂等 | 低（改 _swap_artifact/_restore_artifact） | 极高（修复 N4 真实事故） | P0 | 无 |
| 并发隔离优化 | 中（按卡粒度加锁） | 中（CI 加速） | P2 | 锁存活检测 |
| 崩溃 dump | 低（sys.excepthook） | 中（事后分析） | P1 | 无 |

**建议**：锁存活检测和工件还原幂等立即做（P0，修复真实事故），trace 和仪表盘下一批做（P1）。

---

## 四、和 476 计划的关系

这两项是 476 计划遗漏的——476 只关注"怎么让系统更强"，没有关注"系统失败了怎么恢复"。

N1/N4/E09 都是已经发生的真实事故，不是理论风险。失败恢复应该补入 476 第一波（地基加固），作为 1.12（锁存活检测）和 1.13（工件还原幂等）。
