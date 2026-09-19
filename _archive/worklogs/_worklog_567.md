# _worklog_567 · 供给链加固第一批：完整性自检强制化

> 任务书：`References/architecture_架构演进/567_供给链加固第一批_完整性自检强制化.md`
> 承接：`76fc84a`（566 已验收）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付（一任务一 commit）

| 任务 | 内容 | commit |
|---|---|---|
| 0 | 基线核对（独立复算 sha256） | 无代码改动（结论见 §1） |
| 1 | `tool_integrity.py --check` + `enforce()` | `603a11f` |
| 2 | 三个判定入口强制自检 + 重钉 | `4a0fdd5` |
| 3 | 正反例回归锁（12 例） | `34e7d9f` |

## 1 · 任务 0：基线核对（动工前）

用临时脚本独立复算（不依赖工具自身的比对逻辑）：
```
基准条数 5
  OK  atom_evidence_replay.py  c08bc1de9809
  OK  cppbible.py              af8c89035f54
  OK  gate_engine.py           6574af0f0e6c
  OK  poison_drill.py          6a4f1f6280bb
  OK  toolchain.py             e343fbf2abf9
基线一致
```
**结论：动工前基线本来就干净（5/5 一致）**，无需先重钉（如实记录，不假装）。
另跑了一遍工具自身的默认比对（无参数=比对）：`[tool_integrity] OK：5 个核心工具与基准一致` exit 0。

## 2 · 任务 1：`--check` 独立验证入口

* 新增 `--check`（**显式**验证入口；无参数的默认动作本来就是比对，`--check` 是别名，两条都保留）；
* 失败输出按提示词改成**只打 12 位前缀**并逐文件列出（全量哈希在 `.tool_checksums` 里，别刷屏）：
  `[tool_integrity] ❌ gate_engine.py 被改动（期望 6574af0f0e6c… 实际 c3699a7d4d29…）`；
* 退出码不变：全匹配 0 / 改动或缺失 1 / **缺基准 2**。

新增 `enforce(tool_name)`：判定入口专用的**强制闸**。
* **fail-closed**：缺基准（2）/ 文件缺失 / **校验自身异常**（try/except 包住）一律当"不可信"⇒ 拒绝运行
  ——绝不因为校验代码自己出错就静默放行（那会把"没查"伪装成"查过且通过"）；
* 通过时**静默**（不打印）⇒ 不污染各入口的 stdout 契约（`--json` 等）；
* 拒绝时只报完整性问题（`SystemExit(1)`），并给出重钉修法。

## 3 · 任务 2：三个判定入口强制自检（本批核心）

| 入口 | 落点 | 顺序保证 |
|---|---|---|
| `gate_engine.py` | `main()` **第一句** | 在 `argparse` **之前** ⇒ 连参数解析都不做 |
| `atom_evidence_replay.py` | `main()` **第一句** | 在任何读卡/编译之前 |
| `poison_drill.py` | `__main__` 块（该文件无 `main()`） | 在任何钻探/编译之前 |

**实测（真实篡改态：我刚改完三个核心文件、尚未重钉那一刻）**：
```
$ .venv\Scripts\python.exe tools/tool_integrity.py --check
[tool_integrity] ❌ atom_evidence_replay.py 被改动（期望 c08bc1de9809… 实际 ca6d8a73ee39…）
[tool_integrity] ❌ gate_engine.py 被改动（期望 6574af0f0e6c… 实际 c3699a7d4d29…）
[tool_integrity] ❌ poison_drill.py 被改动（期望 6a4f1f6280bb… 实际 8d3834a9f726…）
exit=1

$ .venv\Scripts\python.exe tools/gate_engine.py --check
[integrity] ❌ 判定核心被改动且未重钉，拒绝运行（gate_engine.py 不执行任何规则/判决）
    atom_evidence_replay.py：期望 c08bc1de9809… 实际 ca6d8a73ee39…
    gate_engine.py：期望 6574af0f0e6c… 实际 c3699a7d4d29…
    poison_drill.py：期望 6a4f1f6280bb… 实际 8d3834a9f726…
    修法：确认改动**有意为之**后跑 `.venv\Scripts\python.exe tools/tool_integrity.py --update` 重钉（改判定核心必须显式留痕 —— 这正是本机制的设计目标）
gate exit=1          ← 三入口同款（replay / poison 亦拒绝运行）
```
**重钉后**：
```
$ .venv\Scripts\python.exe tools/tool_integrity.py --update
[tool_integrity] 基准已更新：tools/.tool_checksums（5 个文件）
$ .venv\Scripts\python.exe tools/tool_integrity.py --check
[tool_integrity] OK：5 个核心工具与基准一致      exit=0
$ .venv\Scripts\python.exe tools/gate_engine.py --check     exit=0
```

## 4 · 任务 3：正反例回归锁（`tests/test_tool_integrity.py` 5 → 12 例，全绿）

四态全覆盖 + 边界：
1. 真实仓库 `--check` 绿（**独立复核路径**，不靠 monkeypatch）；
2. 篡改一个无关字节 ⇒ `--check` 必红、**列出该文件**、只打前缀（断言"输出里没有 64 位全量哈希"）；
3. **入口拦截**：篡改态下 `gate_engine.main([])` / `replay.main([])` 在**任何参数解析之前** exit 1
   （同时断言拒绝文案 + 期望/实际前缀 —— 否则空 argv 自带的 usage 退出会让用例假过）；
4. `poison` 的入口在 `__main__` 块 ⇒ 用**整目录副本**验真入口拦截（副本里给 gate_engine.py 追加
   一个无关字节 ⇒ poison / gate / tool_integrity 三条 CLI 全部红，同一道闸）；
5. 缺基准 ⇒ **fail-closed** exit 1（"没查成"不许当"查过"）；
6. 通过时**静默**（stdout/stderr 均空）；
7. 末尾绿锁：`ti.verify() == ([], [], 0)` —— 证明**全程只动临时副本**，正式 tools/ 未受影响。

**篡改纪律**：所有篡改在 `tmp_path`（临时基准文件 / `shutil.copytree` 的整目录副本）上进行，
**从头到尾没有对正式 `tools/` 写过任何一个字节**（绿锁用例即证据）。

## 5 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **"没有 `--check`"更准确的说法**：`tool_integrity.py` **无参数的默认动作本来就是比对**
   （文档字符串第 12 行、exit 0/1/2 三态齐全），只是**没有 `--check` 这个名字**。
   按提示词新增了 `--check` 显式别名（保留默认行为，不破坏既有调用方）。
2. **`poison_drill.py` 没有 `main()`**：它的 CLI 在 `if __name__ == "__main__":` 块里（2043 行）
   ⇒ 闸门放在该块首句；因此**进程内** `drill()` 调用不受闸门约束（边界见 §6 诚实边界）。
3. **`enforce` 的作用范围**：闸门落在三个 **CLI 入口**（提示词原文"三个判定入口开头"+"篡改态下跑
   `gate_engine.py` 必须 exit 1"）。**进程内 import 后直接调规则函数**（如 `mutation_fuzz` 复用
   `gate_engine` 的规则）不经过闸门——这是有意的边界（避免把库调用也变成"必须先重钉"），
   已在此声明，若要覆盖需另立规格。
4. **实测异常插曲**（不影响结论，如实记录）：第一次测三入口退出码时用 `cmd /c "( ... & echo
   %errorlevel% )"`，`%errorlevel%` 是**解析期展开** ⇒ 打出的 `=0` 是假读数；随后用 PowerShell
   直接取 `$LASTEXITCODE` 复测，确认 gate `--check` 在篡改态 exit=1、重钉后 exit=0。
   本条写出来是为了避免后来者被那组 `=0` 误导。

5. **受控目录发现一处历史污染**（本批验收核对时抓到，非本批引入）：`evidence/conc/EV-CONC-001.md`
   里残留 3 行 M4 变异注入 `- {kind: contains_any, symbol: main, text: ".file"}`，且文件尾丢了一个
   换行——形态就是 `mutation_fuzz` 在 EV-CONC-001 上跑 M4 时**中途被打断/未还原**的产物
   （558 批我跑过 `--cards all --operators M2,M3,M4 --limit 5`，见 558 worklog）。
   **处置**：已从 HEAD 取回原文恢复（`git diff --quiet -- evidence/ atoms/` 复验 exit 0）；
   并实测**当前测试套件不再复现**（还原后跑 `tests/test_mutation_fuzz.py` 全绿、脏项计数不增）。
   **遗留风险**：`mutation_fuzz` 的"逐变体还原"缺一个异常安全的兜底（建议后续批次给
   `run_fuzz` 的写卡-还原段加 `try/finally`），本批不扩大范围。

## 6 · 诚实边界（本批**没**解决什么）

* `.tool_checksums` 自身不纳入校验（递归无解）——**谁改了基准仍可自签**，这正是提示词列入"本批不做"
  的 PoC#3（`--update` 无认证自签）；本批只堵"改核心文件不被发现"；
* PoC#4（RULE-COVERAGE 靠 grep 字符串）/ #5（poison_exemptions 无签名自批）按提示词不碰；
* 进程内库调用不过闸（见偏差 3）。

## 7 · 收工验收（fresh，改判定核心故全量）

后台 fresh 跑：`_acc567.log` / `_acc567.err`；pytest 明细 `_fast567.txt` / `_slow567.txt`。

| 项 | 实测 |
|---|---|
| `tool_integrity.py --check`（验收开头与结尾各一次） | `OK：5 个核心工具与基准一致` **exit 0** |
| 篡改一例（真实：改完核心未重钉那一刻） | 三入口拒绝运行、gate exit 1（§3 全文证据）；重钉后 `--check` exit 0 |
| gate | `规则 61 条 · 命中 141 (block=0 warn=136 advice=5)` |
| poison | `107/107` + 双指标 `trap_block_rate=100% (6/6) · clean_pass_rate=100% (2/2)` |
| replay | `confirm=56 refute=0 infra_error=0 共 56 张卡` |
| pytest fast `-n auto` | **exit 0** |
| pytest slow `-n0` | **exit 0** |
| 受控目录 | `git diff --quiet -- evidence/ atoms/` **exit 0**（内容零差异） |

**取证口径说明（诚实）**：这次 pytest 的**汇总行没被管道抓到**（终端只剩 syrupy 的
`5 snapshots passed.`）⇒ **不拿"没看到 failed"当绿**，改用**退出码**定论（pytest 无用例时是 5、
有失败是 1）⇒ 两个套件均为 **exit 0**。同理，早先那次用 `cmd /c` + `%errorlevel%` 得到的三入口
`=0` 是解析期展开的**假读数**，已用 `$LASTEXITCODE` 复测纠正（§5 偏差 4）。

## 8 · 交人项

1. **副作用纪律**（今后每批都要守）：任何人改了 `CORE_TOOLS` 五个文件中的任一个，**必须**
   `tool_integrity.py --update` 重钉并在**同一个 commit** 里带上 `tools/.tool_checksums`，
   否则下一个判定入口直接自红（设计目标，不是 bug）。建议写进 trae 的批次模板。
2. PoC#3/#4/#5（自签 / grep 覆盖率 / 无签名豁免）等 564 完整规格——本批留下了 `enforce()` 这个
   收口点，将来加认证只需改这一处。
3. `data/logs`、`.pytest_tmp`、`data/mutation/_558_*.json` 清理仍需非 agent 终端（agent 侧删不动）。
