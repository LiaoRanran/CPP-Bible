---
id: 487
title: 性能优化与队列设计详细方案 ccache接入 replay并行 增量replay 任务队列 资源分配
status: active
type: architecture-note
created_at: 2026-09-14
---
# 487 性能优化与队列设计详细方案
## ccache 全面接入 + replay 并行化 + 增量 replay + 任务队列 + 资源分配

> 生成时间：2026-09-14
> 前置实测：ccache 缓存 0%（完全没用上）、replay 全局锁 .replay_lock 阻止并行、32 核只用 1 核、全量 replay 4.5min 编译占 99.5%
> 用户反馈："有的跑的真的很慢，性能优化和队列设计和资源分配设计的不好"

---

## 一、现状与瓶颈

### 实测数据

| 指标 | 现状 | 理论上限 | 差距 |
|---|---|---|---|
| ccache 命中率 | 0% | 80%+ | 完全没接入 |
| replay 并行度 | 1（全局锁） | 32（CPU 核数） | 32× |
| 全量 replay 耗时 | 4.5min | <15s（并行+ccache） | 18× |
| 单卡 replay 差异 | 0.7s~13.7s（20×） | 均匀 | 慢卡拖全量 |
| CI quality job | 37 步串行 | 4 job 并行 | 3-4× |
| 增量 replay | 无（每次全量） | 只跑改动的卡 | 日常 50×+ |

### 三大瓶颈

1. **ccache 零命中率**：装了但 replay 编译命令没加 ccache 前缀，每次都全量编译
2. **全局锁阻止并行**：`.replay_lock` 是全局互斥锁，56 张卡只能一张一张跑
3. **没有增量**：改一张卡也要全量 replay 56 张

---

## 二、ccache 全面接入

### 2.1 问题

ccache 已安装（Windows C:\tools\ccache\，WSL 4.9.1），但：
- replay 编译命令没有 ccache 前缀
- CI 没有配置 ccache
- 缓存目录 0% 使用率

### 2.2 改法

#### replay 接入 ccache

修改 `atom_evidence_replay.py` 的编译命令构造：
```python
# 改前
cmd = f"{compiler} {flags} -o {output} {input}"

# 改后
ccache = find_ccache()  # Windows: C:\tools\ccache\ccache.exe, WSL: /usr/bin/ccache
if ccache:
    cmd = f"{ccache} {compiler} {flags} -o {output} {input}"
else:
    cmd = f"{compiler} {flags} -o {output} {input}"  # 降级：无 ccache 也能跑
```

#### ccache 配置

```bash
# 最大缓存 5GB
ccache --max-size=5G

# 缓存目录（Windows 和 WSL 分开，避免跨平台缓存冲突）
# Windows: %LOCALAPPDATA%\ccache
# WSL: ~/.cache/ccache

# 关键：hash 命令行包含编译器版本和路径，避免跨编译器误用缓存
export CCACHE_COMPILERCHECK=content
```

#### CI 接入 ccache

```yaml
# .github/workflows/ci.yml
- name: ccache cache
  uses: actions/cache@v4
  with:
    path: ~/.ccache
    key: ccache-${{ runner.os }}-${{ hashFiles('**/*.cpp') }}
    restore-keys: ccache-${{ runner.os }}-

- name: Install ccache
  run: sudo apt-get install -y ccache

- name: Configure ccache
  run: |
    ccache --max-size=2G
    echo "CC=gcc" >> $GITHUB_ENV
    echo "CXX=g++" >> $GITHUB_ENV
```

### 2.3 预期效果

- 首次全量 replay：4.5min（无缓存）
- 二次全量 replay（无代码改动）：<30s（ccache 命中 80%+）
- 改一张卡后全量 replay：<1min（只有改动的卡重新编译）

### 2.4 验收

- ccache 命中率 >70%（二次运行）
- 全量 replay 二次运行 <1min
- 无 ccache 环境降级正常（不报错）

---

## 三、replay 并行化

### 3.1 问题

`.replay_lock`（:846）是全局互斥锁，56 张卡串行跑。32 核 CPU 只用 1 核。

锁的初衷是防止并发 replay 冲突（470 对抗发现的僵尸锁 DoS），但全局锁太粗了。

### 3.2 改法：per-card 隔离 + 无锁设计

#### 方案 A：per-card 临时目录（推荐）

每张卡在独立的临时目录中编译运行，互不干扰：

```python
def replay_card(card_path, workers=8):
    """并行 replay 多张卡"""
    cards = collect_cards(card_path)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(_replay_single, cards))
    return aggregate(results)

def _replay_single(card):
    """单卡 replay，使用独立临时目录"""
    with tempfile.TemporaryDirectory(prefix=f"replay_{card.id}_") as tmpdir:
        # 编译到 tmpdir，运行在 tmpdir
        # 不触碰共享的 build/ 目录
        result = compile_and_run(card, tmpdir)
        # 工件校验在原位置（只读）
        verify_artifact(card, result)
    return result
```

关键：
- 编译输出到临时目录，不共享 build/
- 工件校验只读原位置的 .asm/.out，不修改
- 不需要全局锁（没有共享写）

#### 方案 B：保留全局锁但加并行（过渡方案）

如果 per-card 隔离改动太大，先做：
- 全局锁只保护"工件还原"这一步（唯一的共享写）
- 编译运行可以并行

### 3.3 并行度控制

```python
def get_optimal_workers():
    """根据 CPU 核数和内存决定并行度"""
    cpu = os.cpu_count() or 4
    # 每个编译进程约 500MB 内存，留 2GB 给系统
    mem_gb = psutil.virtual_memory().total / (1024**3)
    mem_workers = int((mem_gb - 2) / 0.5)
    return min(cpu, mem_workers, 16)  # 上限 16，避免磁盘 IO 瓶颈
```

### 3.4 僵尸锁修复（470 遗留）

470 对抗发现的僵尸锁 DoS（锁残留导致 replay 阻塞 600s）：
- 锁文件写 pid
- 获取锁时检查 pid 是否存活（`os.kill(pid, 0)`）
- stale 时间从 3600s 缩到 300s
- atexit/signal 释放锁

但如果用 per-card 隔离方案，全局锁就不需要了，僵尸锁问题自然消失。

### 3.5 预期效果

- 全量 replay（冷缓存）：4.5min → 30s（32 核并行，编译占 99.5%，并行效率接近线性）
- 全量 replay（热缓存）：30s → <10s
- 单卡最慢 13.7s → 并行后不影响总时间（其他卡同时跑）

### 3.6 验收

- 全量 replay <30s（冷缓存，32 核）
- 并行度 = min(CPU, 内存限制, 16)
- 无共享写冲突（per-card 临时目录）
- 僵尸锁问题消失

---

## 四、增量 replay

### 4.1 问题

改一张卡也要全量 replay 56 张，4.5min。日常开发中 90% 的改动只影响 1-2 张卡。

### 4.2 改法：基于 git diff 的增量 replay

```python
def replay_incremental(base_ref='HEAD'):
    """只 replay 改动的卡"""
    changed_files = git_diff(base_ref)
    affected_cards = find_affected_cards(changed_files)
    # 改动证据卡 → replay 该卡
    # 改动夹具 → replay 所有引用该夹具的卡
    # 改动工具 → 全量 replay（工具改动影响所有卡）
    if is_tool_change(changed_files):
        return replay_all()
    return replay_cards(affected_cards)

def find_affected_cards(changed_files):
    """根据改动文件找受影响的卡"""
    affected = set()
    for f in changed_files:
        if f.startswith('evidence/'):
            affected.add(f)  # 证据卡本身
        elif f.startswith('Examples/atoms/'):
            # 夹具改动 → 找所有引用该夹具的卡
            affected.update(find_cards_using_fixture(f))
        elif f.startswith('atoms/'):
            # 原子改动 → 找其引用的证据卡
            affected.update(find_evidence_for_atom(f))
    return affected
```

### 4.3 接入 CI

CI 中：
- PR 模式：只 replay 改动的卡（增量）
- main 分支 push：全量 replay（确保基线）
- 定时（每天）：全量 replay

### 4.4 预期效果

- 日常开发（改 1-2 张卡）：4.5min → <10s
- CI PR 检查：15min → <2min
- main 分支仍全量，保证基线完整

---

## 五、任务队列设计

### 5.1 问题

多 Agent 同时干活时：
- 两个 Agent 同时改同一个文件 → 冲突
- 两个 Agent 同时跑 replay → 抢锁（全局锁）
- 任务分配靠人，没有队列
- 没有优先级（紧急修复和普通改进混在一起）

### 5.2 改法：简单任务队列

#### 队列文件

`data/tasks/queue.jsonl`：
```json
{"id": "task_001", "type": "fix_gate", "target": "EV-MEM-017", "priority": "P0", "status": "pending", "assigned_to": null, "created_at": "..."}
{"id": "task_002", "type": "write_atom", "target": "ATOM-CONC-LOCK-002", "priority": "P1", "status": "pending", "assigned_to": null, "created_at": "..."}
```

#### 队列操作

```python
# tools/task_queue.py
def add_task(task_type, target, priority='P2'):
    """添加任务"""

def claim_task(agent_id):
    """领取任务（原子操作，避免两个 Agent 领同一个）"""
    # 按优先级排序，取第一个 pending
    # 标记为 in_progress，assigned_to=agent_id
    # 用文件锁保证原子性

def complete_task(task_id, result):
    """完成任务"""

def fail_task(task_id, error):
    """任务失败，回退到 pending"""
```

#### 文件锁

用 `fcntl`（Linux）或 `msvcrt`（Windows）的文件锁保证队列操作原子性。

### 5.3 冲突避免

- 每个任务有明确的 target 文件
- Agent 领取任务时，检查 target 是否被其他 in_progress 任务锁定
- 如果被锁定，跳过该任务，领下一个
- 任务完成后释放 target 锁

### 5.4 优先级

- P0：门禁红、replay 下降、阻断级问题
- P1：红队发现的高级问题、性能退化
- P2：普通改进、新功能
- P3：文档更新、清理

---

## 六、资源分配

### 6.1 问题

- 32 核 CPU，但 replay 只用 1 核
- 编译可能 OOM（并行太多）
- 磁盘可能满（build/ 目录、ccache 缓存、trace 日志）
- 没有资源配额，一个 Agent 可以吃光所有资源

### 6.2 改法：资源配额

#### CPU 配额

```python
# 每个 Agent 的最大并行度
RESOURCE_LIMITS = {
    'writer_agent': {'cpu': 4, 'memory_gb': 4},    # 写卡不需要太多编译
    'redteam_agent': {'cpu': 8, 'memory_gb': 8},   # 红队需要编译验证
    'gate_agent': {'cpu': 16, 'memory_gb': 16},    # 门禁全量 replay
    'ci': {'cpu': 32, 'memory_gb': 32},            # CI 用满
}
```

#### 磁盘配额

- build/ 目录：定期清理（>1GB 时清理旧文件）
- ccache 缓存：上限 5GB（ccache 自动管理）
- trace 日志：按天分割，>30 天归档
- 临时目录：用 tempfile，用完即删

#### 内存保护

- 并行度计算考虑内存（见 3.3）
- 编译命令加内存限制（ulimit 或 cgroups，Linux）
- OOM 时自动降低并行度重试

### 6.3 资源监控

`tools/resource_monitor.py`（约 60 行）：
- 实时显示 CPU/内存/磁盘使用率
- 超过阈值告警
- 记录到 trace 日志

---

## 七、CI 并行化细化（481 的补充）

### 7.1 当前

CI quality job 37 步串行，Set up Python 重复 5 次。

### 7.2 改法：4 job 并行

```yaml
jobs:
  quality:
    # 内容审计：gate + poison + doc_lint + selfcheck
    steps: [gate, poison, doc_lint, selfcheck]
  
  verification:
    # 编译验证：replay + compile_all + chapter_compile_check
    steps: [replay, compile_all, chapter_check]
  
  tests:
    # 测试：pytest + coverage
    steps: [pytest, coverage]
  
  site:
    # 站点构建：mkdocs + gen_mkdocs_nav
    steps: [mkdocs, gen_nav]
    needs: [quality, verification, tests]  # 最后构建
```

### 7.3 预期效果

- CI 总耗时：15min → <5min
- Set up Python：5 次 → 4 次
- pip 缓存命中（463 CI1）

---

## 八、实施计划

### 第一阶段（零/低成本，立即做）

1. **ccache 接入 replay**：改编译命令加 ccache 前缀（约 20 行改动）
2. **ccache 配置**：Windows + WSL + CI 配置 ccache
3. **僵尸锁修复**：锁写 pid + 存活检测 + stale 缩到 300s（470 遗留）
4. **增量 replay**：基于 git diff 只跑改动的卡（约 80 行）

### 第二阶段（中等成本，下一批做）

5. **replay 并行化**：per-card 临时目录 + ThreadPoolExecutor（约 100 行改动）
6. **任务队列**：tools/task_queue.py（约 120 行）
7. **CI 并行化**：改 ci.yml 为 4 job 并行

### 第三阶段（高成本，积累数据后做）

8. **资源配额**：每个 Agent 的 CPU/内存配额
9. **资源监控**：tools/resource_monitor.py
10. **智能调度**：根据任务类型和资源状态自动分配并行度

---

## 九、预期效果总览

| 场景 | 当前 | 第一阶段后 | 第二阶段后 |
|---|---|---|---|
| 全量 replay（冷） | 4.5min | 4.5min（ccache 冷） | 30s（并行） |
| 全量 replay（热） | 4.5min | <1min（ccache） | <10s（并行+ccache） |
| 改 1 张卡 replay | 4.5min | <10s（增量） | <10s（增量） |
| CI 总耗时 | 15min | 10min（ccache） | <5min（并行） |
| 多 Agent 冲突 | 靠人协调 | 靠人协调 | 任务队列自动 |
| 资源管理 | 无 | 无 | 配额+监控 |

**最大单点提升**：ccache 接入（零成本，4.5min→<1min）+ replay 并行（32×，4.5min→30s）

---

## 十、风险与缓解

| 风险 | 缓解 |
|---|---|
| ccache 跨编译器误用缓存 | CCACHE_COMPILERCHECK=content，hash 包含编译器版本 |
| 并行 replay 工件冲突 | per-card 临时目录，工件只读不写 |
| 增量 replay 漏卡 | 工具改动强制全量，夹具改动找所有引用卡 |
| 任务队列文件锁跨平台 | 用 fcntl/msvcrt 封装，Windows/Linux 都支持 |
| 并行编译 OOM | 并行度考虑内存，OOM 时自动降级 |
| CI 并行依赖问题 | 用 needs: 明确依赖关系，artifact 传递 |
| ccache 在 CI 冷启动慢 | actions/cache 持久化 ccache 目录 |
