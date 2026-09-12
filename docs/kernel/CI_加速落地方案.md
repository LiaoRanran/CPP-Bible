# CI 加速落地方案（310 实施版）

> 2026-09-12 · 基于 310 调研，按风险/收益排序，分三阶段实施
> 关联：.github/workflows/ci.yml（752 行）

---

## 一、实施优先级

| 阶段 | 方案 | 预计节省 | 风险 | 状态 |
|---|---|---|---|---|
| P0 | 路径过滤（只改 atoms/ 时跳过 compile/site/pdf/epub） | 大量（5min vs 60min） | 低 | 待实施 |
| P0 | quality 内部并行（matrix 5 组） | 2-3 min | 中 | 待实施 |
| P1 | pip 缓存 | 1-2 min | 低 | 待实施 |
| P1 | compile 与 quality 并行 | 5 min | 中 | 待实施 |
| P2 | ccache 编译器缓存 | 3-5 min | 中 | 待实施 |
| P2 | 按需构建 site/pdf/epub | 15-20 min | 低 | 待实施 |

---

## 二、P0-1：路径过滤（最先实施）

### 2.1 原理

用 `dorny/paths-filter` 检测变更路径，只在相关文件变更时运行特定 job。

### 2.2 具体修改

在 ci.yml 顶部新增 changes job：

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      tools: ${{ steps.filter.outputs.tools }}
      atoms: ${{ steps.filter.outputs.atoms }}
      book: ${{ steps.filter.outputs.book }}
      examples: ${{ steps.filter.outputs.examples }}
    steps:
      - uses: actions/checkout@v7
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            tools:
              - 'tools/**'
              - 'tests/**'
            atoms:
              - 'atoms/**'
              - 'evidence/**'
              - 'misconceptions/**'
              - 'goldens/**'
            book:
              - 'Book/**'
              - 'Examples/**'
            examples:
              - 'Examples/**'
```

然后各 job 加条件：

```yaml
quality:
  if: needs.changes.outputs.tools == 'true' || needs.changes.outputs.atoms == 'true' || needs.changes.outputs.book == 'true'
  needs: changes

compile:
  if: needs.changes.outputs.book == 'true'
  needs: changes  # 不再 needs: quality

site:
  if: needs.changes.outputs.book == 'true'
  needs: [compile, publish-check]
```

### 2.3 效果

- 只改 atoms/evidence/（原子生产）：quality 5min，compile/site/pdf/epub 全部跳过 → **总 5min**
- 只改 Book/：quality + compile + site/pdf/epub → 全流程
- 只改 tools/：quality 5min → **总 5min**

### 2.4 风险

- `dorny/paths-filter` 是第三方 action，需要信任
- 路径过滤规则写错会导致该跑的没跑（漏检）
- **缓解**：先在 PR 上测试，确认无误后再合入 master

---

## 三、P0-2：quality 内部并行

### 3.1 原理

把 quality 的 ~30 步拆成 5 组，用 matrix 并行。

### 3.2 分组

| 组 | 步骤 | 预计耗时 |
|---|---|---|
| lint | Ruff + Mypy | 1 min |
| metrics | Metrics + Star/H2 + Consistency + Whitespace + Density | 2 min |
| gate | Gate Engine + Golden Lock + Debt Ledger | 1 min |
| replay | Evidence Replay + Poison Drill + Cross-check Matrix | 3 min |
| tests | Pytest + Preflight + Data Sanity + Xref | 2 min |

### 3.3 注意

- replay 组最慢（48 卡编译+运行），决定总时间
- 各组都需要完整 checkout，不能共享工作区
- **风险**：matrix 内的 if 条件容易写错，导致某组跳过

---

## 四、P1：pip 缓存

### 4.1 修改

在每个需要 pip install 的 step 前加缓存：

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.lock.txt') }}
    restore-keys: pip-${{ runner.os }}-
```

### 4.2 效果

pip install 从 ~30s 降到 ~5s（命中缓存时）。

---

## 五、实施顺序建议

1. **第一波**：P0-1 路径过滤（收益最大、风险最低）
2. **第二波**：P1 pip 缓存（零风险）
3. **第三波**：P0-2 quality 内部并行（需要仔细测试）
4. **第四波**：compile 与 quality 并行（需要确认 compile 不依赖 quality 结果）
5. **第五波**：ccache + 按需构建

---

## 六、当前状态

- ci.yml 未修改（等第六批 CONC 域 CI 完成后再改）
- 本文件为实施方案，修改时按阶段逐步落地
- 每阶段修改后必须在 PR 上验证 CI 全绿
