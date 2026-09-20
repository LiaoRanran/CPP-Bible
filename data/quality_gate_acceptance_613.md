# 613 · CI quality job 验收（B3）

> 生成：`python tools/quality_gate_613.py` ｜ 时间：2026-09-20T23:43:17
> 本地逐个复跑 `.github/workflows/ci.yml` quality job 的门禁步骤并记录 exit code。
> 本工具**只读**（各步骤自身可能写 build/ 等 ignore 产物，不碰受控目录）。

## 一、总览

- 步骤数：28 ｜ 通过：**28** ｜ 失败：**0**
- 受控目录清洁性：✅ 干净
- 本地跳过（环境依赖）：2 项

## 二、逐步结果

| 步骤 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| `ruff` | 0 ✅ | 0.2 | All checks passed! |
| `mypy` | 0 ✅ | 0.4 | Success: no issues found in 183 source files |
| `gen_metrics --check` | 0 ✅ | 1.9 | [gen-metrics] ✅ 全部文档数字与事实源一致 |
| `star_h2 --star` | 0 ✅ | 0.5 | [star-check] ✅ 星级格全合规 |
| `star_h2 h2-check` | 0 ✅ | 0.6 | [h2-check] 章=147 H2恶化=0 改善=0 新增=0 扩展膨胀=0 |
| `atom_coverage_map` | 0 ✅ | 0.6 | [coverage-map] ✅ 覆盖率 100% |
| `preflight_check` | 0 ✅ | 0.6 | [OK] 未发现 fenced/inline code 之外的致命反斜杠序列。 |
| `consistency_check` | 0 ✅ | 1.1 | ============================================================ |
| `data_sanity_audit` | 0 ✅ | 0.8 | 合计 7 处（ERROR 0 / WARN 0 / 已复核豁免 7），扫描 151 文件；HEX_QUANTITY 零误报可用 --fail-on ERROR 接门禁 |
| `crossref_audit` | 0 ✅ | 0.8 | [*] 交叉引用总计: 1758 条 |
| `xref_check` | 0 ✅ | 0.5 | RESULT: PASS (链接完整性 OK) |
| `gen_indexes --check` | 0 ✅ | 0.3 | [PASS] 三份索引均与磁盘一致。 |
| `density_audit` | 0 ✅ | 10.0 | [PASS] density gate: avg=25.8/20.0, shallow=0 |
| `d5_appendix_audit` | 0 ✅ | 6.7 | ======================================================================== |
| `d5_source_integrity` | 0 ✅ | 0.5 |     _bench_d5_ch50_demo.cpp <- Book\part05_oo\ch50_multiple_inheritance.md |
| `terminology_normalize` | 0 ✅ | 1.6 | --- 按文件（前 40，完整见 git diff）--- |
| `exercise_dup_guard` | 0 ✅ | 0.5 | OK: 未发现跨章克隆的练习代码块。 |
| `verify_asm_evidence` | 0 ✅ | 0.4 | 明细 → build\asm_evidence_report.json |
| `dangling_ref_linter` | 0 ✅ | 2.5 | [+] JSON 写入: outputs/t1_2_dangling.json |
| `prereq_topo_check` | 0 ✅ | 0.4 | [+] JSON 写入: outputs/t1_3_topo.json |
| `structure_audit` | 0 ✅ | 0.6 | --- summary: files_with_hits=0 counts={} |
| `sweep_fences` | 0 ✅ | 0.7 | 缺陷总数: 0  按类: {} |
| `whitespace_fix` | 0 ✅ | 0.4 | [dry-run] files_changed=0 totals={'w1': 0, 'w2': 0, 'w3': 0} |
| `s10_verify_mark` | 0 ✅ | 0.2 | [OK] 全部章均已含 §10 验证标记 |
| `fix_book_links` | 0 ✅ | 0.3 | [links] ✅ 无带 Book/ 前缀的正文链接（已全部为源相对或已清理） |
| `d5_gap_scanner(soft)` | 0 ✅ | 0.4 |   [json] -> C:\CodeLearnling\note\note\C++\CPP-Bible\build\d5_gap_report.json |
| `mermaid_audit(soft)` | 0 ✅ | 0.3 | ✅ 全部 511 个 Mermaid 图块通过静态校验。 |
| `table_style_audit(soft)` | 0 ✅ | 0.4 | 合计 0 处表格问题（扫描 151 文件，已排除代码围栏内伪表） |
| `worktree_cleanliness` | 0 ✅ | 0.1 | 干净 |

## 三、失败明细

- 无失败步骤 ✅

## 四、本地跳过（CI 上有环境）

- `cross-check matrix`：需 clang++ 对照；本地仅 MinGW g++（CI runner 上有）
- `book_asm_freshness`：需 binutils c++filt/objdump；CI ubuntu runner 自带

> 注：`mypy` 若本地未安装会记 127（模块不存在），CI 会自行安装 mypy==2.3.1。
