# 709 Task G — 新仓库匿名化报告

- 日期：2026-10-09
- 目标仓库：`C:\CodeLearnling\queyi-audit`（**匿名复现包**，双盲投稿用）

## 1. 扫描模式（任务书 5 条 + 追加）

`Ran Liao` / `廖冉` / `LiaoRanran`（含**大小写变体** `liaoranran`）/ `Hefei University` / `合肥`（含`合肥大学`）/
`1026708211@qq.com`（含 `1026708211`）/ `24302091007` / `CPP-Bible`（含 `cpp-bible`）/ `阿信` / `Anonymous Author(s)`。

## 2. 处理

| 轮次 | 动作 | 结果 |
|---|---|---|
| 第 1 轮 | 删除 6 个文件（书籍线脚本 + 匿名检查器自身）；对 59 个文件做替换 | 残留 NONE（当时全集） |
| 第 2 轮 | **补拷后**（Task I 补的 4 个模块 + pyproject + 2 个报告）再跑一遍 | 修 8 个文件 |
| 第 3 轮 | 定位 `LICENSE` / 2×`Dockerfile` / `decision_event_v2_ledger.jsonl` | 修 4 个文件 |
| 第 4 轮 | **大小写不敏感**替换（`liaoranran` / `cpp-bible` 等小写变体） | 修 3 个文件 |
| 第 5 轮 | 清理 `__pycache__` / `.pytest_cache` / `.mypy_cache` / `.ruff_cache`（编译字节码里残留真名） | 删 4 个缓存目录 |

替换映射（示例）：`LiaoRanran (阿信)`/`LiaoRanran`/`阿信` → `The Authors`；`Liao, Ran`/`Ran Liao` → `Anonymous`；
`Hefei University, School of …` → `Anonymous Institution`；`1026708211@qq.com` → `anonymous@example.org`；
`github.com/LiaoRanran/CPP-Bible` → `anonymous/queyi-audit`；`CPP-Bible` → `queyi-audit`；`24302091007` → 删除。

## 3. 最终验证（两道）

**(a) 工作区文件级扫描**（排除第三方 `.sty`）：
```
FINAL_LEAKS_EXCL_STY = 0
```

**(b) git 跟踪内容扫描**（`git grep`，权威）：
```
git grep -nIE "liaoranran|cpp-bible|hefei|1026708211|阿信|廖冉"
→ 0 命中
```

## 4. 唯一保留的 `Anonymous Author(s)`（**非泄漏**，已说明）

`paper/paper1/neurips_2025.sty` 与 `paper/paper2/neurips_2025.sty` 各 1 处含 `Anonymous Author(s)`。
这是 **NeurIPS 官方模板自带的通用占位符**（不含任何真实身份），且源仓库一直将该 `.sty` 视为**未修改的第三方文件**。
⇒ **不修改**（改它反而破坏"模板未修改"的声明与可复现性），并在此显式登记。

## 5. 其他匿名化

| 项 | 处理 |
|---|---|
| 两篇论文 tex | 均为匿名版：paper1 由 706 验证 0 泄漏；paper2 本批把 `\author` 改为 `Anonymous` 并去元数据（Task E） |
| 新 `README.md` | 署名 "The Authors"；无个人 GitHub 链接；项目名 **Queyi Audit** |
| 新 `CITATION.cff` | `authors: Anonymous / Anonymous Institution`；题名用现行题名 |
| 新 `CONTRIBUTING.md` / `REPRODUCTION.md` | 全篇不含作者标识 |
| `data/annotation_package/` | 源即去标识材料包（706 已登记 13 条注释残留问题在源侧，未带入新仓库的泄漏面） |

## 6. 诚实边界

- **子串替换是机械的**：它消除了标识串，但不等于"文本不可溯源"（若审稿人拿到源仓库，文本可对齐）。这是复现包匿名化的通行做法。
- `decision_event_v2_ledger.jsonl` 内的作者署名被替换为 `The Authors`：**事件条数（452）不变**，但该文件的 **sha256 变了**（因此在**新仓库**里不可再与源仓库的哈希清单对照）。已在报告中登记。
- 未做"改写措辞以隐藏写作风格"的匿名化（超出工程范围）。

## 7. 产物

- 匿名化后的新仓库（`git grep` 0 泄漏）
- 本报告
