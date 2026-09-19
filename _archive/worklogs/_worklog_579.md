# _worklog_579 · 修死 mutation 跑批非确定性：工件层根隔离 + 确定性自检

> 任务书：`References/architecture_架构演进/579_苦力_修死mutation非确定性_工件层根隔离.md`
> 承接：578 收尾后（`b4173ac` / `76efae8` / `d116d9c`）+ 578b 自查报告 `_worklog_578b.md`
> 权威值（不改数）：全量 `989/9/185（严格 619）`、M5 `29/0/56`、M6 `324/8/0`
> 本文件按惯例**不入库**。

## 0 · 任务 0（侦察）：ROOT 用法全审计 + 沙箱复制面

**结论：监工诊断成立，且我把"改哪里"落到了行级清单。**

* 全部 **124 条** artifact/fixture 路径的顶层目录**只有 `Examples/` 一个**（实测统计）
  ⇒ 沙箱必须把 `Examples/` 一起复制，否则工件层根本不进沙箱。
* replay 对**真实文件**的写/删点（原文行号）：`1031/1043/1053`（工件备份-还原-删备份）、
  `1487`（`(ROOT/"build").mkdir`）、`1515/1517`（`art_path.unlink` —— M1 的"删旧工件重生成"）、
  `1682/1690`（`write_bytes(original)` 还原）、`1850-1853`（写 manifest）。
  ⇒ M1/M7 变体跑批期间，**真实工件处于"已删/待重生成"窗口**，这正是 M6 变体全库扫描读到
  "034 的 artifact 不存在"（`EV-ARTIFACT-FILE-EXISTS` block + `EV-ASSERT-SYMBOL-MAPPED` warn）的来源。
* **ROOT 用法分类清单**（gate 14 处、replay 22 处）：

| 类别 | 处理 | 位置 |
|---|---|---|
| **工件层读**（fixture / artifact / run_match_file / .out 内容与存在性） | **改为跟随跑批根** | gate：`913`(self_satisfied) `1001/1085`(trivial_observation / out_undeclared_key) `1144`(run_key_declared) `1433/1444`(fixture_no_echo) `1504`(env_dependent_key) `1554`(out_stale_mtime) `1746`(`_assert_haystack`→EV-ASSERT-SYMBOL-MAPPED) `2626`(EV-ARTIFACT-FILE-EXISTS) `2672`(zero_diag_werror) `3125/3155`(s3_*)；replay：`871/883`(sanitizer 夹具) `1240/1256/1263`(阴面夹具) `1296/1327/1391/1519`(run_commands cwd) `1429`(展示) `1453`(art_path) `1464`(extra_arts) `1487`(build/) `1537`(run_match_file) `1745/1750/1760/1839/1850`(manifest 与指纹) |
| **必须留真实 ROOT**（工具自身配置 / 跨进程设施） | **不动** | gate：`PYPROJECT` `CPPBIBLE` `MISCONCEPTIONS` `_ARTIFACT_PRODUCER_EXEMPT` `_CLAIM_STAGING` `concept_aliases.txt` `knowledge_graph.db` `ASSERT_BASELINE` `_VERIFY_REASON_EXEMPT` `_ARTIFACT_LEDGER` `cwd=str(ROOT)`(git 调用)；replay：`_REPLAY_LOCK`（跨进程并发锁）、`CCACHE_DIR = ROOT/build/.ccache`（编译缓存，进沙箱会让每次跑都冷启动）、CLI 的 `find_cards()` / `--card` 解析 |

## 1 · 任务 1：工件层根隔离（**方案 A 全量**，非最小子集）

* **机制**（`atom_evidence_replay.py`）：`_RUN_ROOT: ContextVar` + `run_root()`（默认 = 真实 ROOT ⇒
  所有现存 CLI/测试行为逐字不变）+ `batch_root(path)` 上下文管理器（try/finally 无条件还原）
  + `manifest_path()`。**没有用全局 monkeypatch**（监工要求），跑批期由上下文显式激活。
* **replay**：上表 15 处全部改走 `run_root()` / `manifest_path()`；manifest 的**键**（`_manifest_key`）、
  **指纹默认根**（`card_fingerprint` 的 `calc_root or run_root()`）、**alive 检查**（`update_manifest`）
  一并跟随 ⇒ 跑批的 manifest 完全落在跑批根内，**不读不写**真实 `build/replay_manifest.json`。
* **gate**：上表 14 处工件读取改走 `replay.run_root()`（gate 已 import replay，无新耦合）；
  `_rel()` 也改为跟随跑批根 ⇒ 跑批 findings 的 target 变**仓内相对形**（`evidence/mem/EV-MEM-034.md`），
  不再打印 `…\Temp\mutfuzz_xxx\…`（这一条同时是任务 2 自检能"逐字比对"的前提；**有意变更**，见 §6-1）。
* **`mutation_fuzz.sandbox()`**：复制 `atoms/` + `evidence/` + **`Examples/`**（13.4 MB / 1552 文件，
  每跑一次，毫秒级），建**空** `tmp/build`，并在 `with replay.batch_root(tmp)` 内 yield ⇒
  卡文本与工件在同一个根内自洽，任何规则都读不到真实仓库的瞬态。

## 2 · 任务 2：确定性自检（把"同输入同输出"变成机器判据）

* `mutation_fuzz --selfcheck-determinism`：主跑结束后对关键子集（`M1/M6/M7`，至少覆盖
  "动工件层"的 M1/M7 与"跨卡 finding"的 M6）**重跑一次**，逐变体比对
  `(verdict, kind, why, new_block, new_warn)`；不一致 **fail-loud exit 2** 并打印"哪张卡哪个变异点抖了"。
* 正反例测试（`tests/test_mutation_isolation_579.py`）：
  * 正例：小批 M6 两次跑一致 ⇒ `(True, [])`；
  * **反例 1**（可证伪）：把基线篡改一条 ⇒ 自检必须报不一致（否则自检是恒真摆设）；
  * **反例 2**（CLI 面）：主跑干净、自检那次抖动 ⇒ `--selfcheck-determinism` 必须 exit 2 且打印"抖动"；
  * **反例 3**（锁旧病）：预置**异源 manifest + build 残留**，两次跑逐变体必须一致（旧代码在此必红）。

## 3 · 任务 3：报告诚实性（便宜项）

`metrics_collector` 的 v5 tag 追加**方差声明**：
> 【579 方差声明：该点估计含**运行间方差**（实测 ≥2/998，继承跑批残留状态时曾得 991/7）；
> 下方 C-P 区间只覆盖**抽样误差**，不覆盖跑批非确定性。579 已把工件层根隔离进沙箱并加
> `--selfcheck-determinism`，待自检稳定 N 轮后再撤此声明】

## 4 · 任务 4：缓存失效契约收紧

* `gate_engine.py:198` 起身的注释原文"改盘即失效，不存在'改了内容还命中旧值'的窗口"**过强**，
  已按实测改写：同尺寸同 tick 改写会相撞（间隔 0ms 时 200 次里 **132 次**；≥0.5ms 起 **0/12**）
  ⇒ 窗口是**亚毫秒级**，现存流程不受影响（写入间隔含一次全库扫描）。
* 新增 `invalidate_meta(path)`（O(n)，只摘该路径，不牺牲其它卡）+ 规定"进程内改盘必须显式调用"。
  正反例：`tests/test_meta_cache_579.py`（同尺寸改写 → invalidate → 读到新值；作用域与幂等）。

## 5 · 验收（fresh）

| 项 | 实测 |
|---|---|
| gate | `规则 63 条 · 命中 191 (block=0 warn=186 advice=5)` —— **命中数未变** ✓ |
| replay | `confirm=56 refute=0 infra_error=0` ✓ |
| poison | `118/118 —— 制衡层有效（全部拦截 + 阴性放行）` ✓（见 §6-6 的 116/118 事故与修正） |
| `tool_integrity --check` | exit 0 ✓（gate/replay 属 CORE_TOOLS，本批改动已同 commit 重钉） |
| **全量 #1（预置脏 manifest + build 残留）** | **`989/9/185（严格 619）`** —— 与权威 v5 逐字一致 ✓ |
| 全量 #2（同脏态 + `--selfcheck-determinism`） | `989/9/185` + 自检 ✓（见 §5-1） |
| pytest fast `-m "not slow" -n auto` | **exit 0** ✓ |
| pytest slow `-n0` | exit 1，**唯一失败 = `test_json_output.py::test_golden_lock_json`**（任务书允许的 1 个待人 accept 预期红）✓ |
| 真实仓零副作用 | `Examples/` 全树 sha256 指纹不变（`ffba4cbdbddaddb5`）；真实 `build/replay_manifest.json` **字节不变**（预置值原地不动）✓ |
| 受控目录 | `git diff --quiet -- atoms/ evidence/ data/` 全 exit 0 ✓ |
| 新增 pytest | `test_mutation_isolation_579.py`（7 例）+ `test_meta_cache_579.py`（2 例）全绿 ✓ |

**一次未复现的瞬态（诚实记录，不下结论）**：收工验收首轮的 fast 里，本批新增的两条用例红过一次
（`test_579_sandbox_activates_batch_root_and_copies_artifacts`、`test_579_dirty_manifest_does_not_change_verdicts`）。
随后**串行 8/8 绿**、**完整 fast 套件复跑 `exit 0` 绿**、单文件 `-n auto` 绿 —— 均未复现。
当时的可疑干扰源：前一轮验收脚本被 `Stop-Process` 强杀，可能有遗留 worker 仍在抢 `_REPLAY_LOCK`
或写真实 manifest；但**未取得直接证据**，故只记录现象、不宣称原因（避免把"没查清"说成"已排除"）。

### 5-1 · 全量 #2 与自检结果

```
=== 2) 全量跑 #2（同脏态 + --selfcheck-determinism）===
[mutation] blocked=989（严格 619） escaped=9 n_a=185（其中 malformed=0）
[mutation] ✓ 确定性自检：关键子集两次跑逐变体一致（1183 变体 / 子集算子 ['M1','M6','M7']）
=== 3) 对照 ===
两次脏态跑逐算子一致: True | 与 v5 权威逐算子一致: True
Examples 全树指纹（应 ffba4cbdbddaddb5）: ffba4cbdbddaddb5
真实 manifest 仍在且是预置脏值: True   ← 跑批没读没写它
```

⇒ **三方逐算子一致**（脏态跑 #1 / 脏态跑 #2 / 权威 v5），且**预置脏 manifest + build 残留**下
数字与清态完全一样 ⇒ 578b 的离群（991/7）在机制上被消灭，不是"运气好没踩到"。

## 6 · 诚实边界 / 有意变更

1. **`_rel()` 语义变更（有意）**：跑批期 findings 的 target 从"沙箱绝对路径"变为**仓内相对形**。
   数字（verdict/逃逸/严格）逐字不变；变的是报告**字符串**，且是变好（两次跑可比。此前 578b
   必须手工归一化临时路径才能 diff）。**若监工要求报告保持旧字符串形，请明示**——那会让自检重新
   需要路径归一化。
2. **仍留在真实仓的东西（有意）**：`build/.ccache`（编译缓存：进沙箱等于每次冷编译）；
   `build/.replay_lock`（跨进程并发锁，必须全局唯一）。二者都不承载判决输入；
   因此"真实 build 零差异"的核验口径是 **manifest 字节 + 残留文件**，不含 ccache 内部增长。
3. **未动**：replay 的 `_shown_path()` 展示函数（非判决面，仓内相对 + 兜底绝对）；
   规则语义、口径、C-P 区间、分母定义**一律未改**（本批只修"尺子会抖"）。
4. `--selfcheck-determinism` 是**opt-in**（默认关）：全量跑加自检会让耗时再涨一个子集
   （M1+M6+M7 全卡）。收工验收已手动跑过一次带自检的全量（§5-1）。
5. 570/571 那类"批内并发"（560 B2 卡间隔离并行）**本批不做**，但监工点出的复用点成立：
   `batch_root()` 正是"每 worker 独立根（`build_<pid>`）"要的同一机制，届时直接复用。
6. **首版踩坑并已修（诚实记录）**：第一版把 gate 的 14 处工件读取直接改走 `replay.run_root()`
   （默认 = `replay.ROOT`），**绕过了毒样例自建的沙箱**——P60/P61/P62 等载荷按注释要求
   `monkeypatch ge.ROOT` 指向临时目录，期待"工件相对路径跟**本模块** ROOT 解析" ⇒ 实测
   **poison 116/118**（`P61-阴` 被 `EV-RUN-KEY-DECLARED-EXISTS` 拦、`P62-阴` 被
   `EV-ARTIFACT-FILE-EXISTS` 拦，均为"应放行却拦"）。修法：gate 本地 `_artifact_root()` ——
   **跑批根激活时以跑批根为准，否则用本模块 `ROOT`**（`_rel()` 一并跟它）⇒ poison **118/118** 恢复。
   修正单独 commit（`2cc5a5a`）便于 review；该修正**不改变跑批行为**（跑批期两者等价），
   故 §5 的全量数字不受影响。
   *附带说明*：`P2` 那次红出现在"与收工验收脚本并发跑"的时刻（`infra_error:replay_busy`）——
   `_REPLAY_LOCK` 是有意留在真实仓的跨进程锁，**并发跑 poison 会互抢锁**，单独跑即绿。

## 7 · 交后续

1. `--selfcheck-determinism` 建议进 CI（或每日轮）：**尺子的确定性必须自己守着**——
   本批的教训是"测试全绿 + 单次跑自洽"完全挡不住这类非确定性。
2. 560 B2 并行化：复用 `batch_root()`（每 worker 一个根），manifest 已天然按根分片，不再互相踩。
3. metrics 的方差声明：等自检连续 N 轮稳定（建议 N≥5）后再撤。
