# 零污染自证（v5 对抗复测）

## git status --porcelain（结束时实拍）

```
 M Examples/atoms/_atom_alloc_arena.asm
?? "References/architecture_架构演进/471_调研消化成果_450-467_突破性发现与逻辑依赖.md"
?? _adv_v80/
?? _worklog_403.md
?? _worklog_470.md
```

## 逐项归属

| 条目 | 归属 | 说明 |
|---|---|---|
| `M Examples/atoms/_atom_alloc_arena.asm` | **非本轮探针造成** | 开工基线即存在（见 REPORT §2 N4）：该文件属 `EV-MEM-027` 的 artifact，已被清空（426 行全删，磁盘 sha `e3b0c442…`=空串）。本轮所有探针的 `artifact` 均指向 `_adv_v80/probes/` 或 `_adv_v70/probes/`，**不触碰正式工件**。**建议由建设者 `git checkout` 恢复**。 |
| `?? _adv_v80/` | 本轮（对抗沙箱） | 探针卡 + 夹具 + 脚本 + 本报告。⚠️ 该目录**实际未被 .gitignore 忽略**（`git check-ignore _adv_v80/` 无输出），与任务前提不符；如需真正忽略，需由建设者加入 `.gitignore`（我不改正式文件）。 |
| `?? 471_*.md` | 外部（并行会话/用户） | 非本轮产物。 |
| `?? _worklog_403.md` / `_worklog_470.md` | 建设者交付物 | 非本轮产物。 |

## 正式目录改动检查（空 = 通过）

```
git status --porcelain | Select-String "^\s*M\s+(atoms|evidence|tools|Book)"
（无输出）
```

`atoms/`、`evidence/`、`tools/`、`Book/` 全部零改动。

## 探针索引（可复现）

| 逃逸 | 探针卡 | 复现脚本 | 预期 / 实测 |
|---|---|---|---|
| N2 全局恒真断言 | `probes/EV-ADV80-N3.md` | `probe_final2.py` | 预期 confirm（零信息断言）/ **实测 confirm = 逃逸** |
| E10a 字段位移 | `probes/EV-ADV80-E10E.md` | `probe_final2.py` | 实测 confirm + gate warn = 仍逃逸 |
| E10b pragma 消音 | `probes/EV-ADV80-E10F.md` | `probe_final2.py` | 实测 confirm + gate warn = 仍逃逸 |
| E05 cat 式证据 | `probes/EV-ADV80-E05E.md` | `probe_final2.py` | 实测 confirm（exp-scan 命中但零输出）= 仍逃逸 |
| E05 阴性对照 | `probes/EV-ADV80-E05F.md` | `probe_final2.py` | exp-scan **无**命中（扫描特异 ✓） |
| E01 编译后覆写 | `_adv_v70/probes/EV-ADV70-H1.md` | `probe_core2.py` | 实测 `refute:artifact_tampered` = 已拦 |
| E03 恒真符号 | `_adv_v70/probes/EV-ADV70-H3.md` | `probe_core2.py` | 实测 `refute:artifact_assert_failed` = 已拦（原探针） |
| E07 五变体 | 内联构造 | `probe_core2.py` | 5/5 `block:indent-smuggle` = 已拦 |
| E11 同义词 | 内联构造（cancels / refutes） | `probe_batch.py` | cancels 已拦；**refutes 静默 = N3** |
| E12 签收自证 | 沙箱复制正式 atoms+evidence 改写 | `probe_core2.py` | 0 block 0 warn = 仍逃逸 |
| E09 并发 | 双进程同卡 | `probe_misc.py` | `['confirm','confirm']` = 串行化成功 |
| E16 闪卡 | `probe_misc.py` | 同左 | 106 张含 4 张非 verified = 仍逃逸 |
| E08 退出码 | `poison_drill.gate_exit_code` | `probe_misc.py` | 0/1/1 = 已拦 |
| N1 僵尸锁 | 现场证据 `build/.replay_lock` | 诊断脚本 | 取锁超时 600.22s = DoS |

复现方式（任选一条）：

```bat
cd C:\CodeLearnling\note\note\C++\CPP-Bible
python -X utf8 _adv_v80\probe_final2.py    :: N2 / E10a / E10b / E05
python -X utf8 _adv_v80\probe_core2.py     :: E01 / E03 / E12 / E07 变体
python -X utf8 _adv_v80\probe_batch.py     :: E11 / E04 / E06
python -X utf8 _adv_v80\probe_misc.py      :: E09 / E16 / E08 / E14
```

> 注：`probe_core.py`（首版）使用正式锁路径，会撞上 N1 僵尸锁而返回 `replay_busy`；
> 后续脚本均已重定向到沙箱锁 `_adv_v80/.replay_lock`，**保留正式锁文件不删**（N1 现场证据）。
