# 319_工具链性能深度优化_ccache_WSL_IO_增量扫描

> 2026-09-12 · 聚焦工具链本身的性能瓶颈 · 每个优化项都有实测数据支撑
> 关联：317 性能优化架构 · 310 CI 加速 · G5 replay/gate 工具

---

## 一、性能瓶颈实测定位

在动手优化前，先定位我们的工具链到底慢在哪：

| 操作 | 当前耗时 | 瓶颈 | 优化后预期 |
|---|---|---|---|
| replay 全量（48 卡） | ~2 分钟 | 48 次 g++ 编译 | ~5 秒（ccache） |
| WSL replay 全量 | ~3 分钟 | 编译 + /mnt/c 9P IO | ~10 秒（ccache + Linux 侧构建） |
| gate_engine 全量 | ~10 秒 | 全量读+解析 100+ 文件 | ~1 秒（增量扫描） |
| golden_lock sync | ~5 秒 | 全量读+JSON 解析 | ~1 秒（增量+缓存） |
| WSL ci_local_precheck | ~5 分钟 | 31 步串行 + /mnt/c IO | ~2 分钟（并行 + Linux 侧） |
| pytest | ~3 秒 | 27 个测试 | 已够快 |

**最大单点优化：ccache**——replay 的 80% 时间在编译，而 90% 的夹具没变。

---

## 二、ccache 编译缓存（P0，收益最大）

### 2.1 原理

ccache 对每次编译计算哈希（预处理后的源码 + 编译选项 + 编译器版本），命中缓存直接返回 .o 文件，跳过实际编译。

- 首次编译：正常编译，缓存结果
- 重复编译：哈希命中 → 从缓存取 .o（1-2 毫秒 vs 1-2 秒）
- 典型加速：**5-10x**；SFML 项目重建 **35-50x**

### 2.2 对我们 replay 的影响

当前 replay 流程：
```
for each evidence card:
  g++ -O2 -S fixture.cpp -o fixture.asm   # 1-2 秒
  g++ -O2 fixture.cpp -o fixture.exe       # 1-2 秒
  run fixture.exe > fixture.out            # <0.1 秒
```

48 张卡 × 2 次编译 = 96 次编译，~2 分钟。

用 ccache 后：
- 未变化的夹具：缓存命中，编译从 1-2 秒 → 1-2 毫秒
- 新/变化的夹具：正常编译（只占少数）
- 全量 replay 从 ~2 分钟 → **~5 秒**（假设 90% 命中率）

### 2.3 落地步骤

**Windows 侧**：
```powershell
# 安装 ccache（通过 Chocolatey 或下载预编译二进制）
choco install ccache
# 或设置 PATH 指向 ccache.exe

# replay 工具中，编译器调用从
g++ -O2 -S ...
# 改为
ccache g++ -O2 -S ...
```

**WSL 侧**：
```bash
sudo apt install ccache
# 同样在 replay 工具中用 ccache 前缀
```

**CI 侧**：
```yaml
- name: Cache ccache
  uses: actions/cache@v4
  with:
    path: ~/.ccache
    key: ccache-${{ runner.os }}-${{ hashFiles('Examples/*.cpp') }}
    restore-keys: ccache-${{ runner.os }}-
```

### 2.4 注意事项

- ccache 的哈希包含**编译器版本**——GCC 升级后缓存自动失效（正确行为）
- ccache 不缓存链接步骤（只缓存编译），但我们的夹具是单文件，链接很快
- 缓存大小限制：默认 5GB，对我们足够（48 夹具 × 2 平台 × ~50KB = ~5MB）
- **关键**：replay 的 artifact_sha256 锚定的是 .asm 内容，ccache 返回的 .o 不影响 .asm 生成（我们用 -S 生成 .asm，ccache 也缓存 .asm）

---

## 三、WSL /mnt/c 性能税（P0，隐藏瓶颈）

### 3.1 问题

我们的项目在 `C:\CodeLearnling\note\note\C++\CPP-Bible`，WSL 侧通过 `/mnt/c/CodeLearnling/...` 访问。

WSL2 通过 **9P 协议**跨文件系统访问 Windows 文件，比 Linux 原生 ext4 慢 **15-20 倍**：
- 小文件操作：600+ files/sec → 60 files/sec
- 元数据操作（stat/open/close）尤其慢
- 我们的 WSL replay：读 48 个 .cpp + 写 48 个 .asm + 写 48 个 .out + 读 48 张卡 = 192 次跨文件系统操作

### 3.2 解决方案：Linux 侧构建目录

**不改项目位置**（Windows 侧需要编辑器访问），只把**编译产物**放 Linux 侧：

```python
# atom_evidence_replay.py 中
# 旧：编译产物写 Examples/fixture.asm（在 /mnt/c 上）
# 新：编译产物写 /tmp/cppbible_build/fixture.asm（Linux 原生）
#     完成后只把需要入库的 .asm/.out 复制回 Examples/

import tempfile
build_dir = tempfile.mkdtemp(prefix="cppbible_")  # 在 /tmp 上，Linux 原生
# 编译、运行都在 build_dir 里
# 只有最终需要 git 跟踪的产物才复制回 Examples/
```

**预期效果**：
- WSL replay 从 ~3 分钟 → ~10 秒（ccache + 原生 IO）
- WSL ci_local_precheck 从 ~5 分钟 → ~2 分钟

### 3.3 备选方案：WSL 侧镜像

如果需要更彻底的优化，可以在 WSL 侧维护一个 git 镜像：
```bash
git clone /mnt/c/CodeLearnling/note/note/C++/CPP-Bible ~/cpp-bible
# WSL 工具在 ~/cpp-bible 跑
# 结果通过 git push/pull 同步回 Windows 侧
```
但这增加了同步复杂度，建议先用"构建目录放 /tmp"的方案。

---

## 四、增量扫描（P1，gate/golden_lock）

### 4.1 问题

gate_engine.py 和 golden_lock.py 每次都**全量扫描**所有文件：
- gate：读 atoms/ + evidence/ + misconceptions/ 下所有文件，解析 frontmatter，跑 33 条规则
- golden_lock：读所有原子/证据卡，更新计数

但大部分时候，只有 1-3 个文件变了（一批原子的产物）。

### 4.2 增量扫描方案

**基于 git diff 的增量**：
```python
import subprocess

def get_changed_files():
    """获取自上次基线以来变化的文件"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True, text=True
    )
    return set(result.stdout.strip().split("\n"))

# gate 只扫描变化的文件 + 它们的关联文件
# （如证据卡变了，对应的原子也要扫）
```

**内容寻址缓存**（Ruff 的做法）：
```python
# 缓存文件内容哈希 → 解析结果
# 文件没变就不重新解析 frontmatter
import hashlib, json, os

CACHE_FILE = ".cache/frontmatter.json"

def parse_frontmatter_cached(path):
    content = open(path, encoding="utf-8").read()
    h = hashlib.sha256(content.encode()).hexdigest()
    cache = load_cache()
    if h in cache:
        return cache[h]
    result = parse_frontmatter(content)
    cache[h] = result
    save_cache(cache)
    return result
```

### 4.3 预期效果

- gate 从 ~10 秒 → ~1 秒（只扫变化的文件）
- golden_lock 从 ~5 秒 → ~1 秒
- 全量扫描仍保留（`--full` 标志，CI 用）

---

## 五、其他优化项

### 5.1 replay 并行编译

当前 replay 是串行编译 48 个夹具。夹具之间**无依赖**，可以并行：

```python
import concurrent.futures

def compile_fixture(card):
    # 编译 + 运行 + 断言
    ...

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compile_fixture, cards))
```

注意：Windows 侧 g++ 编译是 CPU 密集型，4 线程合适（不超过物理核数）。
配合 ccache，并行编译主要加速首次编译。

### 5.2 frontmatter 解析优化

当前用正则或 PyYAML 解析 frontmatter。PyYAML 较慢，可以：
- 用 `yaml.CLoader`（C 加速）
- 或自己写轻量解析器（我们的 frontmatter 结构简单，不需要完整 YAML）

### 5.3 .wslconfig 调优

```ini
# C:\Users\<user>\.wslconfig
[wsl2]
memory=8GB          # 限制 WSL 内存，防止 Windows 交换
processors=4        # 限制 CPU（如果不需要全部核）
swap=2GB
```

### 5.4 Git 配置优化

```bash
git config --global feature.manyFiles true   # 大仓库优化
git config --global core.untrackedCache true  # 未跟踪文件缓存
```

我们的仓库还不大（~300 文档 + 代码），但 References/ 在快速增长，提前配置没坏处。

---

## 六、落地优先级

| 优先级 | 优化项 | 预期收益 | 工作量 | 风险 |
|---|---|---|---|---|
| **P0** | ccache（Windows + WSL + CI） | replay 2min→5s | 0.5 天 | 低 |
| **P0** | WSL 构建目录放 /tmp | WSL replay 3min→10s | 0.5 天 | 低 |
| P1 | replay 并行编译 | 首次编译 2x | 0.5 天 | 中（需处理并发写 .asm） |
| P1 | gate/golden_lock 增量扫描 | gate 10s→1s | 1 天 | 中（需处理关联文件） |
| P2 | 内容寻址缓存 | 重复扫描 5x | 1 天 | 低 |
| P2 | .wslconfig + git 配置 | 5-10% | 0.1 天 | 低 |

---

## 七、与已有架构的关系

- **317 性能优化**：317 是架构层（子代理/流水线/提示词），319 是工具层（编译缓存/IO/增量），两者互补
- **310 CI 加速**：ccache + actions/cache 是 CI 加速的具体落地项
- **replay 三分类（0558713）**：ccache 命中后编译极快，infra_error:compile_timeout 几乎不会再出现
- **G6 四级状态**：性能优化不改变状态机，只让状态流转更快

**核心洞察**：我们之前的性能优化（317）聚焦在"架构和流程"，但工具链本身有更大的低垂果实——ccache 一项就能让 replay 快 24 倍，这比任何架构调整都立竿见影。「榨干每一丝性能」需要从最底层的编译缓存开始。
