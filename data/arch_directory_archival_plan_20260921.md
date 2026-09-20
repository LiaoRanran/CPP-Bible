# _arch 调研目录归档计划

> 生成时间：2026-09-21
> 状态：待执行（等 613 苦力完成后，避免 git mv 冲突）

## 一、当前状态

### 根目录 _arch 目录（19 个，共 233 文件 / 约 1.6MB）

| 目录 | 文件数 | 大小 | git跟踪 | 阶段 | 归档建议 |
|------|--------|------|---------|------|---------|
| _arch_v2 | 7 | 74KB | ✅ | 早期 | 归档 |
| _arch_v2_round2 | 16 | 144KB | ✅ | 早期 | 归档 |
| _arch_v3 | 13 | 171KB | ✅ | 早期 | 归档 |
| _arch_v4 | 10 | 94KB | ✅ | 早期 | 归档 |
| _arch_v5 | 4 | 37KB | ✅ | 早期 | 归档 |
| _arch_v6 | 7 | 52KB | ✅ | 早期 | 归档 |
| _arch_v7 | 9 | 58KB | ✅ | 早期 | 归档 |
| _arch_v8 | 4 | 23KB | ✅ | 早期 | 归档 |
| _arch_v9 | 16 | 113KB | ✅ | 早期 | 归档 |
| _arch_v10 | 10 | 49KB | ✅ | 近期 | 保留 |
| _arch_v11 | 23 | 167KB | ✅ | 近期 | 保留 |
| _arch_v12 | 17 | 44KB | ✅ | 近期 | 保留 |
| _arch_v13 | 17 | 46KB | ✅ | 近期 | 保留 |
| _arch_v14 | 18 | 122KB | ✅ | 近期 | 保留 |
| _arch_v15 | 18 | 49KB | ✅ | 近期 | 保留 |
| _arch_v16 | 21 | 72KB | ✅ | 近期 | 保留 |
| _arch_v17 | 12 | 68KB | ✅ | 近期 | 保留 |
| _arch_v18 | 14 | 114KB | ❌（.gitignore） | 最新 | 保留（待决定是否入库） |

### _archive 已有子目录（1235 文件 / 约 13.3MB）

- benchmarks/ (135)
- early_probes/ (618)
- eval_pack/ (8)
- legacy_probes/ (23)
- old_tools/ (249)
- root_data/ (1)
- scripts/ (1)
- temp_json/ (39)
- temp_outputs/ (101)
- worklogs/ (56)
- _arch_free/ (1)

## 二、归档方案

### 归档目标
- 把早期调研（v2-v9 + v2_round2）移到 `_archive/old_research/`
- 保留近期调研（v10-v18）在根目录
- 归档后根目录 _arch 目录从 19 个减到 9 个（v10-v18）

### 执行命令（等 613 完成后）

```bash
# 创建归档目录
mkdir -p _archive/old_research

# git mv 早期调研目录
git mv _arch_v2 _archive/old_research/
git mv _arch_v2_round2 _archive/old_research/
git mv _arch_v3 _archive/old_research/
git mv _arch_v4 _archive/old_research/
git mv _arch_v5 _archive/old_research/
git mv _arch_v6 _archive/old_research/
git mv _arch_v7 _archive/old_research/
git mv _arch_v8 _archive/old_research/
git mv _arch_v9 _archive/old_research/

# commit
git commit -m "化债：归档早期调研 _arch_v2-v9 到 _archive/old_research/（根目录 _arch 从 19 减到 9）"
```

### 注意事项
1. **必须等 613 苦力完成后执行**——避免 git mv 与苦力的 git add/commit 冲突
2. **_arch_v18 未入库**——在 .gitignore 里，归档时不涉及
3. **引用检查**——归档前检查是否有文档引用了 _arch_v2-v9 的路径，如果有需要更新引用
4. **governance 台账**——归档后需要更新 governance_docs_manifest.json（如果这些目录在台账里）
5. **导航索引**——References/00_导航/ 里如果有 _arch_v2-v9 的链接，需要更新

## 三、引用检查清单（执行前必做）

- [ ] grep "_arch_v2" 全仓，确认无硬编码引用
- [ ] grep "_arch_v3" 全仓
- [ ] ...（v4-v9 同理）
- [ ] governance_docs_manifest.json 是否包含 _arch_v2-v9
- [ ] References/00_导航/ 是否有 _arch_v2-v9 链接
- [ ] 任何 worklog / 报告是否引用了 _arch_v2-v9 的具体文件路径

## 四、归档后验证

- [ ] `git status` 干净（除归档 commit 外无其他改动）
- [ ] `grep -r "_arch_v2" --include="*.md" --include="*.py"` 无结果（或只有 _archive/ 下的）
- [ ] governance verify 通过（如果台账需要更新）
- [ ] pytest fast 全绿
- [ ] ruff 全绿

---

*本计划由 MainAgent 化债轮生成，待 613 完成后执行。*
