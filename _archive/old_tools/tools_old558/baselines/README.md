# 编译基线归档（Compile Baselines）

本目录固化历次**编译基线快照**，作为大规模治理动作前后的**回归比对锚点**。
每份基线是一次 `compile_all.py --main-only` 全量报告（`partial=False`）的不可变副本，
附带治理元信息（`baseline_meta`），可被 `compile_gate.py` / `prune_exempt.py` 直接以 `--report` 消费。

## 命名规范

```
baseline_<YYYY-MM-DD>_<commit7>_gcc<major>.json
```

例：`baseline_2026-07-18_374a563_gcc15.json`

- `<YYYY-MM-DD>`：归档日期
- `<commit7>`：归档时 HEAD 的 7 位短 SHA
- `gcc<major>`：审计所用编译器主版本

## 现存基线

| 文件 | 日期 | Commit | 编译器 | 章数 | 通过/失败章 | 检查块 | 失败块 | 豁免数 |
|------|------|--------|--------|------|------------|--------|--------|--------|
| `baseline_2026-07-18_374a563_gcc15.json` | 2026-07-18 | `374a563` | MinGW GCC 15.3.0 | 147 | 113 / 34 | 3720 | 65 | 65（已审计） |

> **阶段2 治理前基线**：本快照建立于阶段1技术债清理完成、阶段2大规模治理开始**之前**，
> 是后续治理（重构、批量编辑、章节调整等）的回归比对基准。

## 比对方法

### 1. 用基线作为门禁参照，检测新增回归

```bash
# 重新生成当前全量报告（本地 MinGW gcc-15.3.0）
python3 tools/compile_all.py --main-only \
    --gcc "C:/Qt/Tools/mingw1530_64/bin/g++.EXE" \
    --json tools/_audit_now.json

# 与基线豁免清单比对（--strict-stale 最严：冗余豁免也失败）
python3 tools/compile_gate.py --report tools/_audit_now.json --strict-stale
```

- `新增回归 > 0` → 有编辑破坏了原本可编译的块，必须修复或补豁免。
- `清单冗余 > 0` → 有块已修好（或删除），可从 `compile_exempt.json` 清理。

### 2. 直接检视基线快照本身

```bash
python3 tools/compile_gate.py \
    --report tools/baselines/baseline_2026-07-18_374a563_gcc15.json --strict-stale
```

预期输出：`报告失败块 65 = 已知豁免 65（显式 65 / 模式 0）`、`新增回归 0`、`PASS`。

## 编译器与平台差异（重要）

- **本地审计编译器** = MinGW GCC 15.3.0（`mingw1530`），与汇编证据库同源。
- **CI 门禁编译器** = Linux `g++-15`（经 `ppa:ubuntu-toolchain-r/test` 安装）。
- 两者对 **POSIX 块**判定相反：如 `ch35_memory_layout.md#blk6`（`<sys/mman.h>` mmap）、
  `#blk14`（`<sys/wait.h>` fork）在**本地 MinGW 失败**、在 **Linux 可编译**。
  `compile_gate.py` 的 `AUTO_PATTERNS`（错误文本正则）吸收此类平台差异，避免 CI 误报红。
- 因此基线的 65 个失败块是**本地 MinGW 视角**的失败集；CI Linux 视角失败集更小，
  差集正是 POSIX/WINDOWS 平台专属块。这是设计预期，非缺陷。

## 维护约定

1. **不可变**：已归档的基线文件禁止修改。需要新基线时按命名规范另建一份。
2. **入库**：基线文件与本 README 纳入 git 版本控制（`_` 前缀临时报告不入库）。
3. **同提交**：新基线应与其对应的 `compile_exempt.json` 状态在**同一 commit** 固化，保证可追溯。
