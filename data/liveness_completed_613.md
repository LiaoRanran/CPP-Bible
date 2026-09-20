# 613 · 活性锚补全补丁集（A2）

> 生成：`python tools/liveness_completion_613.py` ｜ 时间：2026-09-20T23:32:35
> **状态：补丁已算出，尚未落卡**——atoms/ 为受控目录，落卡需人审授权（交人项）。
> 只补 cost=low 档（class A / B+high）；medium/high 档留作人审。

## 一、规模与投影

| 项 | 值 |
|---|---|
| 缺锚命题总数 | 50 |
| 本次低成本补全 | **9** |
| 投影 warn（前） | 50 |
| 投影 warn（后） | **41** |
| 剩余待补（medium/high） | 41 |

## 二、补全补丁（精确锚点）

| # | 命题 | 卡 | 锚类型 | 锚符号 | 来源证据卡 | 校验 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-HIST-AUTOPTR-001::prop-2` | ATOM-HIST-AUTOPTR-001 | fixture_symbol | `is_copy_constructible` | EV-MEM-003 | ✅ |
| 2 | `ATOM-MEM-PERF-003::prop-1` | ATOM-MEM-PERF-003 | fixture_symbol | `capacity_at_len1` | EV-MEM-038 | ✅ |
| 3 | `ATOM-MEM-RAII-002::prop-2` | ATOM-MEM-RAII-002 | fixture_symbol | `Correct` | EV-MEM-024 | ✅ |
| 4 | `ATOM-MEM-UNIQUE-001::prop-1` | ATOM-MEM-UNIQUE-001 | fixture_symbol | `Big` | EV-MEM-011 | ✅ |
| 5 | `ATOM-MEM-VALUE-001::prop-1` | ATOM-MEM-VALUE-001 | fixture_symbol | `type_traits` | EV-MEM-006 | ✅ |
| 6 | `ATOM-MEM-LEAK-002::prop-1` | ATOM-MEM-LEAK-002 | fixture_symbol | `cycle_allocated` | EV-MEM-043 | ✅ |
| 7 | `ATOM-MEM-PERF-004::prop-1` | ATOM-MEM-PERF-004 | fixture_symbol | `padded_offset_bytes` | EV-MEM-044 | ✅ |
| 8 | `ATOM-MEM-SHARED-002::prop-2` | ATOM-MEM-SHARED-002 | fixture_symbol | `_M_release` | EV-MEM-034 | ✅ |
| 9 | `ATOM-CONC-LOCK-001::prop-1` | ATOM-CONC-LOCK-001 | fixture_symbol | `single_thread_baseline` | EV-CONC-003 | ✅ |

## 三、待插入 YAML 片段（按命题）

### `ATOM-HIST-AUTOPTR-001::prop-2`（ATOM-HIST-AUTOPTR-001）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: is_copy_constructible
```

### `ATOM-MEM-PERF-003::prop-1`（ATOM-MEM-PERF-003）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: capacity_at_len1
```

### `ATOM-MEM-RAII-002::prop-2`（ATOM-MEM-RAII-002）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: Correct
```

### `ATOM-MEM-UNIQUE-001::prop-1`（ATOM-MEM-UNIQUE-001）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: Big
```

### `ATOM-MEM-VALUE-001::prop-1`（ATOM-MEM-VALUE-001）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: type_traits
```

### `ATOM-MEM-LEAK-002::prop-1`（ATOM-MEM-LEAK-002）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: cycle_allocated
```

### `ATOM-MEM-PERF-004::prop-1`（ATOM-MEM-PERF-004）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: padded_offset_bytes
```

### `ATOM-MEM-SHARED-002::prop-2`（ATOM-MEM-SHARED-002）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: _M_release
```

### `ATOM-CONC-LOCK-001::prop-1`（ATOM-CONC-LOCK-001）

```yaml
    liveness:
      kind: fixture_symbol
      symbol: single_thread_baseline
```

> 落卡位置：对应原子卡 frontmatter 的 `claim_structured[]` 中该 proposition 条目下。
> 落卡后 `OBSERVATION-LIVENESS` 该条不再 warn（规则要求 kind=fixture_symbol 且符号真实可断言）。

## 四、未补部分（交人）

- medium 档（class B + confidence=medium）：需人审复核锚符号后补。
- high 档（class C，无候选锚）：建议改标 `inference` 或人工指定锚，需人审裁决。
