# 545 · 零污染自证

## 结论

**正式目录零改动**：本轮只新建 `_adv_v95/`（对抗工作区，`.gitignore` 已忽略 `_adv_*`）与系统临时目录下的队列库/交接物；
未修改任何已跟踪文件、未 `git add`、未 commit、未 push、未 accept 任何建议。

## 证据 1 · 开工前基线（快照存于本目录）

- `_adv_v95/.baseline_status.txt`：`git status --porcelain`，63 行
- `_adv_v95/.baseline_diff.txt`：`git diff --stat`

开工前工作树**已存在**的改动（非本轮所为）：

- 已跟踪文件改动：`evidence/conc/EV-CONC-001.md | 5 ++++-`（4 增 1 删，开工前即存在）
- 未跟踪文件 63 项（`_arch_*`/`_adv_*`/`_t535_*`/工具产物等，均为前几轮遗留）

## 证据 2 · 收工对比

```
$ git status --porcelain > now.txt
$ Compare-Object (Get-Content _adv_v95/.baseline_status.txt) $now
=== NEW vs BASELINE ===
（无输出 ⇒ 完全一致）

$ git diff --stat
 evidence/conc/EV-CONC-001.md | 5 ++++-      ← 与基线逐字相同，仍是开工前那一条
 1 file changed, 4 insertions(+), 1 deletion(-)
```

`Compare-Object` 无任何差异行：本轮新建的 `_adv_v95/**` 被 `.gitignore` 覆盖，不进入 `git status`；
已跟踪文件集合与内容与开工前逐字一致。

## 证据 3 · 探针的落点

`probes/probe_l2_attacks.py` 每次沙箱化都做两件事：

```python
d = Path(tempfile.mkdtemp(prefix="adv95_"))
tq.DB_PATH = d / "q.db"        # 队列库在系统临时目录
tq.ANCHOR_ROOT = d             # 锚根（产物/git 审计根）也在系统临时目录
```

即：DB、`data/tasks/**`、worker token、handoff 全部落在 `%TEMP%\adv95_*`，仓库内的 `data/tasks/queue.db` 未被读写。
`_touch_audit` 触发的 `git status` 也只在临时目录里跑（该目录非 git 仓库 ⇒ 走 `audit_note` 分支，不碰真实仓库）。
