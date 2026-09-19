# 变异发现器 × 卡面合法形态 覆盖审计台账（588 任务 0，修前快照）

> 本台账为 **修前实跑** 快照（audit 脚本导入的是当时未改的 `mutation_fuzz`）。

> 矩阵键行尾注释漏网已于 **任务 1** 修复；其余结论以 `tools/mutation_shape_audit.py` 可复现重跑为准。


## Part A · matrix 尾注释漏网（0a）

- 含 `matrix` 块的卡总数：**56**
- `matrix` 键行带尾注释的卡（漏网，现正则 0 变体）：**1** → ['evidence/mem/EV-MEM-004.md']
- `matrix` 块内整行注释的卡：**42** → ['evidence/conc/EV-CONC-001.md', 'evidence/conc/EV-CONC-002.md', 'evidence/mem/EV-MEM-001.md', 'evidence/mem/EV-MEM-002.md', 'evidence/mem/EV-MEM-003.md', 'evidence/mem/EV-MEM-004.md', 'evidence/mem/EV-MEM-005.md', 'evidence/mem/EV-MEM-006.md', 'evidence/mem/EV-MEM-007.md', 'evidence/mem/EV-MEM-008.md', 'evidence/mem/EV-MEM-009.md', 'evidence/mem/EV-MEM-010.md', 'evidence/mem/EV-MEM-011.md', 'evidence/mem/EV-MEM-012.md', 'evidence/mem/EV-MEM-013.md', 'evidence/mem/EV-MEM-014.md', 'evidence/mem/EV-MEM-015.md', 'evidence/mem/EV-MEM-016.md', 'evidence/mem/EV-MEM-017.md', 'evidence/mem/EV-MEM-018.md', 'evidence/mem/EV-MEM-019.md', 'evidence/mem/EV-MEM-020.md', 'evidence/mem/EV-MEM-021.md', 'evidence/mem/EV-MEM-022.md', 'evidence/mem/EV-MEM-023.md', 'evidence/mem/EV-MEM-024.md', 'evidence/mem/EV-MEM-025.md', 'evidence/mem/EV-MEM-026.md', 'evidence/mem/EV-MEM-027.md', 'evidence/mem/EV-MEM-028.md', 'evidence/mem/EV-MEM-029.md', 'evidence/mem/EV-MEM-030.md', 'evidence/mem/EV-MEM-031.md', 'evidence/mem/EV-MEM-038.md', 'evidence/mem/EV-MEM-039.md', 'evidence/mem/EV-MEM-040.md', 'evidence/mem/EV-MEM-041.md', 'evidence/mem/EV-MEM-042.md', 'evidence/mem/EV-MEM-043.md', 'evidence/mem/EV-MEM-044.md', 'evidence/mem/EV-MEM-045.md', 'evidence/ub/EV-UB-001.md']
- `matrix` 值行带尾注释的卡：**1** → ['evidence/mem/EV-MEM-001.md']
- `matrix` 用块式列表（非 flow `[..]`）的卡：**0** → 无
- 现正则能产 matrix 变体的卡 / 含 matrix 的卡：**55/56**
- 现正则产出 **0** matrix 变体的卡（漏网）：['evidence/mem/EV-MEM-004.md']

## Part B · 全算子 × 卡面形态 覆盖（0b）

| 算子 | 变异点 | 目标字段 | 卡面形态 | 真实卡例(id,至少1个) | 现正则能否变异 | 漏网证据 |
|---|---|---|---|---|---|---|
| M6 | matrix 值层（删键/非法值） | matrix 块 | matrix 键行带尾注释（matrix:   # ...） | evidence/mem/EV-MEM-004.md | 漏(n=0) | EV-MEM-004 即此形态；现正则 ^(matrix:)\s*\n 要求键行仅空白再换行，撞 # 失配 ⇒ 整块 0 变体（漏） |
| M6 | matrix 值层 | matrix 块 | matrix 块内整行注释（含冒号） | evidence/conc/EV-CONC-001.md | 能(n=7) | 现遍历靠 ':' not in s 跳过注释行（侥幸），注释含冒号也不误当键；任务1 改为先剥注释再解析 |
| M6 | matrix 值层 | matrix 值行 | matrix 值行带尾注释（compiler: [...]  # ...） | atoms/mem/ATOM-MEM-LEAK-001.md | 能(n=7) | 现 _mut_matrix_values 不做剥注释；值行尾注释随值一起替换，变体照常产出（无漏） |
| M6 | matrix 值层 | matrix opt 值 | opt 值行全角括号注释（[-O2]（…）） | atoms/mem/ATOM-MEM-LEAK-001.md | 能(n=7) | 全角括号不影响 ASCII 正则；变体照常产出（无漏） |
| M2 | 路径变形 | command | command 行尾注释（g++ ... # ...） | evidence/hist/EV-HIST-001.md | 能(n=3) | _PATHP 只匹配路径本身（不含 #），尾注释不阻断定位（无漏） |
| M3 | 断言弱化 | actual.run_match_file | actual 项尾注释 | evidence/conc/EV-CONC-001.md | 能(n=1) | M3 在读取面内找 _in/-Werror/count:/条目，尾注释不影响（无漏） |
| M1 | 字段删除 | id | id 行尾注释（id: X  # ...） | 库内未出现 | 能(n=3) | M1 用 ^id:\s*(\S+) 取首个非空 token，尾注释不阻断（无漏） |

## Part C · CRLF 子审计（0c）

- 行尾分布：LF=83 · CRLF=0 · 混合=0
- 结论：**CRLF 无影响**
- LF/CRLF 同构对拍（BASE + EV-MEM-004，各 MUTATORS）：变体集逐字一致 ⇒ **CRLF 无影响**
