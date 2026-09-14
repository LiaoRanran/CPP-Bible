# Examples 行尾漂移检查报告（499 任务6）

> 方法：实跑统计 + `git status` + Read `.gitattributes`
> 结论：**无需一次性 renormalize，维持"碰到即转"策略**

## 1. 实测数据（来自 `Examples/` 全量 rglob `*.cpp`）

| 范围 | 文件总数 | CRLF | LF |
|---|---|---|---|
| `Examples/` 全部 | 1053 | 444 | 609 |
| `Examples/atoms/`（工具唯一写入范围） | 56 | 50 | 6 |
| `Examples/` 其他子目录 | 997 | 394 | 603 |

- CRLF 占比约 **42%**（444/1053）。
- `atoms/` 子目录 CRLF 比例更高（50/56 ≈ 89%），即工具写入范围的夹具 `.cpp` 多数仍是 CRLF。

## 2. git 视角

```
git status --porcelain Examples/   →   0 行变更
```

`.gitattributes` 的 `* text=auto eol=lf` 已在检出/暂存时把工作树字节归一化为 LF，**git 完全看不到这批漂移**（Windows 侧 stat 缓存也会掩盖）。所以 `git status` 干净 ≠ 工作树字节是 LF——工作树实际仍有 444 个 CRLF 文件，只是 git 认为它们"应等于 LF"因而无差异。

## 3. `.gitattributes` 内容（472 批次引入，监工裁决"暂不 renormalize"）

```
* text=auto eol=lf
*.bat  text eol=crlf
*.cmd  text eol=crlf
*.ps1  text eol=crlf
*.asm  -text      # 证据工件：字节即身份，禁转换
*.out  -text
*.o    -text
*.obj  -text
*.exe  -text
```

三条原则：①手写文本统一 LF；②Windows 脚本保留 CRLF；③证据工件（`.asm/.out/.o/.obj/.exe`）声明为 binary，**永久禁转换**——replay 的 `artifact_sha256` 强校验与 `run_match` 逐字比对都基于工作树字节，任何行尾转换都会让全库 refute。

## 4. 风险评估：若执行 `git add --renormalize .`

- 会制造 **444 个假 M**（CRLF→LF 的纯行尾变更），淹没真实改动，等于给下一次真实回归提供藏身处。
- 历史教训：这正是 437 个 `Examples/*.cpp` 曾让 WSL 侧工作树清洁检查恒红、门禁沦为"狼来了"的根因。
- 证据工件 `.asm/.out` 因 `-text` 保护不会被 renormalize 破坏（这是 472 加该条的直接动机）。

## 5. 建议

1. **不做一次性 renormalize**，维持监工裁决的"碰到即转"策略：谁修改某 `.cpp`、谁顺手转 LF 一并提交；新文件由 `* text=auto eol=lf` 保证为 LF。
2. 漂移清理进度继续由 `tools/debt_ledger.json` 的 `DEBT-002` 跟踪（票到期即停线，避免无限期挂着）。
3. **不确定点（留给好模型裁决）**：本次实测 `atoms/` 子目录 CRLF 高达 50/56，与早期"atoms 仅 1 处漂移"的说法明显不符。两种可能：①早期说法针对特定子集（`_atom_*.cpp`）而非全 `atoms/`；②近期某批写入在 `atoms/` 留下了大量 CRLF 夹具而未被"碰到即转"消化。建议核实 `atoms/` 是否真的由工具统一写 LF，若是则 50 个 CRLF 是回归信号，应纳入 `DEBT-002` 优先清理。
