# 673u · governance_docs_manifest 漂移修复报告

**生成日期**：2026-10-03
**任务**：673u 任务 A —— 修复 `data/governance_docs_manifest.json` 漂移 634 处，并评估 4 处 `residue_present` 型 skip 能否解除
**一句话结论**：**漂移不是"忘了重算"，而是生成器有两条口径 bug**（扫描面含 gitignore 的本机落盘口 + 哈希的是含 CRLF 的工作区字节）。修逻辑后重签，漂移 **634 → 0**；**4 处 skip 全部解除**（原 3 处由本批解除，第 4 处依赖 673t 的 Merkle 修复，亦已复验绿）。

---

## 1. 现象与基线

```
$ python tools/governance_doc_guard.py verify
[gov] manifest 不一致（634 处）：
[gov]   新增：_arch_v21/00_方向地图.md
[gov]   新增：_arch_v21/01_验证层.md
...
```

| 口径 | 漂移数 | 构成 |
|---|---|---|
| **本机主仓** | **634** | 633 新增 + 1 内容变更 |
| **干净检出（worktree @ a412b8ff）** | **623** | 589 新增 + 30 删除 + 4 内容变更 |

同一份 manifest，**两个环境给出两组不同的数字** —— 这本身就是"manifest 机器相关"的直接证据，而不是单纯的"基准过期"。

---

## 2. 根因（三条，按性质分）

### 2.1 口径 bug ①：扫描面把 **gitignore 的本机落盘口** 算进了入库 manifest

607 把 `_auto/inbox/*.md`（各批投喂词落盘口）与仓根 `_arch_*/**` 并入扫描面。但 `.gitignore` 里有：

```
124:_auto/          ← 投喂词落盘口（本机才有）
128:_arch_v18/      ← Trae 调研进行中（本机才有）
```

实测：

| 目录 | 本地 .md 数 | git 在册数 | 后果 |
|---|---|---|---|
| `_auto/inbox/` | 70 | 5（604–608） | 本地"新增 44 处"；干净检出对 manifest 里 21 条未跟踪条目报"删除" |
| `_arch_v18/` | 9 | 0 | 干净检出报"删除 9 处" |

⇒ **同一份 manifest 在开发机与 CI 上都不可能一致**（本地多文件、CI 少文件），这是"漂移"永远修不干净的结构性原因。

### 2.2 口径 bug ②：哈希的是**工作区字节**（含 CRLF），不是提交内容

`_sha256()` 直接 `path.read_bytes()`。Windows 编辑器回写会让工作区变成 CRLF，而 `.gitattributes` 是：

```
12:* text=auto eol=lf
```

⇒ 同一份文档：开发机算 CRLF 的 hash，CI（LF 检出）算 LF 的 hash ⇒ 必不相等。

实测（976 份在册受治理文档）：

| 项 | 数 |
|---|---|
| 工作区含 CRLF（hash 会变） | **236** |
| `sha256(CRLF→LF 归一) == sha256(git blob)` | **976 / 976（0 处不符）** |

⇒ 归一换行**精确等价于**"哈希提交内容"，是让 manifest 机器无关的最小改法。

### 2.3 陈旧漂移（真实、合理）：590 份文档在 Sep 22 之后入库未登记

manifest 生成于 `2026-09-22T20:19:01`（`git_commit 6b559d10`，417 条）。此后 `_arch_v24..v47`、`_auto` 等大量文档入库，manifest 从未重算 ⇒ 589 份在册文档"新增"。其中 **1 份是真实内容变更**：

```
内容变更：References/architecture_架构演进/306_原子知识图谱与关系网络架构调研_从扁平列表到可导航知识体系.md
```

`git log` 溯源：`7e838b10 633 [D2]：文档债清理——修 306 文档 3 处裸文件名死链接` —— **合理的内容变更**（不是篡改）。

> 另 3 处"内容变更"（`415_` / `494_` / `README_INDEX.md`）经逐字节比对，manifest 记的正是它们的 **CRLF 版** hash ⇒ 属 2.2 的伪影，不是内容变更。

---

## 3. 修复（改逻辑 + 重签，不是"改基线数字"）

### 3.1 `tools/governance_doc_guard.py`

| 改动 | 内容 | 为什么 |
|---|---|---|
| 新增 `_git_tracked(root)` | 取 `git ls-files` 在册集合；**根 ≠ 工作树根 / 非 git 仓 ⇒ 返回 None（不过滤）** | 让默认扫描面只含"提交进仓的文档"；同时保住 607 假仓测试与 591 注入测试的既有语义 |
| `iter_governed_docs()` | 默认面按在册过滤；`docs_root` 显式注入**不**过滤 | 见 §3.2 的 591 回归 |
| 新增 `_content_bytes()` | `_sha256()` / `scan_docs()` 统一按 `.gitattributes` 归一换行（CRLF→LF） | 让 hash 与"CI 检出内容"一致；`size` 与 `sha256` 同源，避免自相矛盾 |
| 模块 docstring | 增记 673u 两条口径 bug 与边界 | 与仓内"改动必须留痕"的惯例一致 |

**口径澄清（不是放水）**：manifest 仍**逐字节**钉住每份在册文档；改的只是"扫谁、按什么字节算"。对"投喂词被篡改"的检出能力**不变**（改内容 ⇒ hash 变 ⇒ `verify` 红）。

### 3.2 修的过程中的一个回归（如实登记）

第一版把**整个**默认面都按在册过滤，导致既有测试 `tests/test_governance_doc_guard_591.py::test_preflight_combinations` 由红转绿（**假绿**）：该用例把 `DOCS_ROOT` `monkeypatch` 到 `tmp_path`（在 `.pytest_tmp/` 下，本身也是 gitignore），注入的临时文档被过滤掉 ⇒ 篡改检测失效。

**修法**：`DOCS_ROOT`（591 原始治理面）**豁免**在册过滤。依据：
1. 实测该目录 **345 份 .md 全部在册**（过滤在真仓是 no-op，不损失覆盖）；
2. 保住"显式注入 > 在册过滤"的语义优先级。

修后该用例恢复正常（红→绿的路径重新可测）。

### 3.3 重签与重钉

```
$ python tools/governance_doc_guard.py update --force
[gov] manifest 已更新 → data/governance_docs_manifest.json（变更 623 处）（self_hash 13ff769a6fba…）
$ python tools/governance_doc_guard.py verify
[gov] manifest 一致 ✓（self_hash 已校验）        # exit 0
```

`data/governance_docs_manifest.json` 同时被 `tool_integrity.SUPPLY_CHAIN_FILES` 钉住，故必须重钉基准：

```
$ python tools/tool_integrity.py --update --no-update-merkle
$ python tools/tool_integrity.py --check
[tool_integrity] OK：5 个核心工具与基准一致
[tool_integrity] OK：信任根数据文件与基准一致（6 个已存在，警告 0 条）
[tool_integrity] OK：目录级 Merkle 根与当前内容一致（警告 0 条）
[tool_integrity] OK：判决尺子与基准一致（22 个）
```

`tools/.tool_checksums` 的净改动仅 2 行（`data/governance_docs_manifest.json`、`governance_doc_guard.py`）。

---

## 4. 验证（三层，逐层加强）

### 4.1 本地 `verify` 一致（exit 0）

### 4.2 **与 git blob 逐条比对**（证明"CI 也一致"）

```
manifest 条数: 976     blob 缺失: 0     与 HEAD blob 不一致: 0
=> manifest 与"干净检出(CI)"逐字节相同
```

方法：对 manifest 的 976 条逐条取 `git cat-file HEAD:<path>` 的字节，与 manifest 记录的 sha256 比对。**全等 ⇒ CI 上必然 `verify` 绿**（CI 拿到的就是这些 blob）。

### 4.3 **真干净检出复验**（`git worktree add --detach`，= CI 所见）

```
=== 干净检出（HEAD = 673t 1072c605）===
PASS 1 test_governance_manifest_verified
PASS 2 test_verify_real_manifest_matches
PASS 3 test_real_manifest_has_valid_self_hash
PASS 4 test_chain_verify_with_real_inspections
```

---

## 5. 4 处 skip 的处置结果

原状（673s 审计）：4 处用 `@pytest.mark.skipif(clr.residue_present(), …)`，而 `residue_present()` 恒真（`_arch_v19..v23/_adv_v80` 已全部入库）⇒ **4 个用例在 CI 也从未跑过**。673s 摘守卫实测 4/4 全红，根因即本报告的漂移 634 处。

**本批实测（先修漂移，再看能否解除）**：

| # | 用例 | 本地 | 干净检出 | 处置 |
|---|---|---|---|---|
| 1 | `test_ci_pytest_fix_625.py::test_governance_manifest_verified` | PASS | **PASS** | ✅ **解除** |
| 2 | `test_governance_doc_guard_591.py::test_verify_real_manifest_matches` | PASS | **PASS** | ✅ **解除** |
| 3 | `test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash` | PASS | **PASS** | ✅ **解除** |
| 4 | `test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` | PASS | PASS（**依赖 673t**） | ✅ **解除** |

**关于第 4 处（跨批次依赖，如实登记）**：本批单独修漂移后，第 4 处在干净检出**仍红**，真阻塞是它的 `integrity_check` inspection 里
`merkle_integrity --check` 的 5 个目录根不匹配（Book/Examples/atoms/evidence/data/mutation，**文件数一致、根不同**）——
与治理清单**同一类** CRLF/LF 口径 bug，但出在 `tools/merkle_integrity.py`。
该问题由并行批次 **673t** 在 commit `1072c605`（"让 Merkle 根与 tool_integrity 摆脱检出环境（CRLF 归一）"）修复。
在 673t 的新 HEAD + 本批改动下，干净检出复验第 4 处 **PASS** ⇒ 一并解除。

**改动范围**：仅摘除 `skipif` 装饰器、删除随之不再使用的导入、更新注释说明；**未改动任何断言**（红线 3）。

---

## 6. 交付物

| 文件 | 变更 |
|---|---|
| `tools/governance_doc_guard.py` | 修两条口径 bug（在册过滤 + 换行归一）+ 文档 |
| `data/governance_docs_manifest.json` | 重签（417 → **976** 条；漂移 0） |
| `tools/.tool_checksums` | 重钉 2 行（manifest / governance_doc_guard） |
| `tests/test_ci_pytest_fix_625.py` | 摘 skip 守卫（+ 清理无用导入） |
| `tests/test_governance_doc_guard_591.py` | 摘 skip 守卫（+ 清理无用导入） |
| `tests/test_governance_self_hash_601.py` | 摘 skip 守卫（+ 清理无用导入） |
| `tests/test_supply_chain_chain_601.py` | 摘 skip 守卫（+ 清理无用导入） |
| `data/673u_governance漂移修复报告.md` | 本文件 |

---

## 7. 遗留与建议（不擅自做）

1. **`_auto/` 与 `_arch_v18/` 是否该继续留在扫描面**：现在被"在册过滤"挡住了，语义正确；但扫描面声明里仍列着它们，读者容易误解。是否把 `GOVERNED_INBOX_DIR` 显式标注为"仅在册"（或直接移出），属治理口径决策。
2. **写盘换行**：`update_manifest()` / `auto_update()` 用 `Path.write_text()` 不带 `newline="\n"`，在 Windows 上写出 CRLF 文件（git 提交时归一为 LF）。当前由 673t 的 `sha256_of` 归一兜住；若要彻底消除这层依赖，可在两处写盘加 `newline="\n"`。本批未改（避免与 673t 的 tool_integrity 线交叉）。
3. **`_arch_v19..v23` + `_adv_v80` 是否继续留仓**（168 tracked 文件）：owner 的取舍，本批不动。
