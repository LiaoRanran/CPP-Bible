# 620 D2 · CI 四 job 状态确认

> 工作流：`.github/workflows/ci.yml`（单文件，triggers: push/PR to main|master + workflow_dispatch）

---

## 一、所谓「CI 四 job」是哪四个

`ci.yml` 实际定义了 **10 个 job**，其中承担**门禁判定**的四个并行 job 是：

| job | 门禁内容 | 关键步骤 |
|---|---|---|
| **quality** | 文档/结构/引用/术语/汇编证据层 | ruff(tools/)、mypy(tools/)、gen_metrics --check、star_h2、atom_coverage_map、受控目录清洁、cross-check matrix、consistency、data_sanity、xref、gen_indexes、density、d5 系列、terminology、exercise_dup、asm 证据、structure/sweep/whitespace、s10 标记、链接完整性等 |
| **pytest** | 工具链单测 | `pytest tests/ -q -m "not slow" -n 16 --maxfail=1` + `-m slow -n0` |
| **replay** | 证据卡机器复算 | `atom_evidence_replay.py --check`（tools/ 有变更时 `--rebuild-manifest`，否则 `--incremental`） |
| **gate** | 规则引擎 + S1-S6 | `gate_engine.py --check`、`golden_lock check --no-replay`、`debt_ledger check`、`poison_drill.py` |

下游：`compile`（needs 四者）→ `publish-check` → `site` / `pdf` / `epub` → `deploy`。
任一硬门禁失败即不部署。

---

## 二、CI 覆盖点确认（关键更正）

```powershell
git rev-parse --short origin/master        →  d2f412b
git log --oneline -1 origin/master         →  d2f412b "619 D2：验收报告…"
git rev-list --count origin/master..HEAD    →  14
git rev-parse cbd0fbd == origin/master ?    →  DIFFERENT
```

| 项 | 619 报告所称 | 620 实测 | 结论 |
|---|---|---|---|
| CI 覆盖点 | `cbd0fbd`（616 F1 收工） | **`d2f412b`**（619 收工） | **619 报告该句已过时** |
| 617/618/619 是否被 CI 覆盖 | "未被覆盖" | **已被覆盖**（已随 617–619 推送进 origin/master） | **需更正** |
| 本地领先 origin/master | 41 | **14**（= 620 自身 commit） | 620 未 push |

⇒ **619 验收报告 §七.5 的说法已不成立**，已在原文件该处追加更正标注。

---

## 三、620 新增内容是否被 CI 覆盖

**结论：未被覆盖**（620 按硬边界**不 push**）。

| 620 新增 | 数量 | CI 覆盖？ |
|---|---|---|
| 新工具 | 7 个（A1/A2/A3/A4/B1/B3/C2/C3 → 实际 8 个，见下） | ❌ 未覆盖 |
| 新单测 | **80 例** | ❌ 未覆盖 |
| PCK 证书 | 83 张 + 83 份渲染 | ❌ 未覆盖（也非 CI 校验对象） |
| Authority 日志 | 388 条 | ❌ 未覆盖 |

> 620 新增工具实际为 **8 个**：`adversarial_loop_620`、`adversarial_weight_calibration_620`、
> `vfdr_realtime_620`、`pck_batch_migrator_620`、`pck_status_stats_620`、
> `authority_log_620`、`pck_authority_sync_620`、`run_620_gate`（E1）。

**本地等价验证已做**（替代 CI）：
- 每个新工具 `--check` 全过；
- `pytest` 80 例全绿；
- `ruff check` 对新工具/单测全过；
- 收工门禁 `run_620_gate.py`（E1）串起上述检查。

---

## 四、诚实登记 / 局限

1. **CI 实际运行结果无法在本机核实**：远程 run 状态需 GitHub API（本机无 token / 无网络调用），
   本报告只能确认**代码已进入 CI 覆盖范围**（`origin/master = d2f412b`），
   **不能**确认那次 CI 是绿是红。是否真绿需人在 GitHub Actions 页面核对。
2. **`gate` job 会跑 `gate_engine --check`**：620 稳态 block=0（任务1 已确认），
   推送后该项应通过；但推送前无法验证。
3. **`replay` job 与 `gate` job 在 CI 中是并行 job**（`needs` 只在 compile 层汇聚）——
   注意：这与 620 任务1 发现的「gate ∥ replay 并发会争抢 `Examples/atoms/*.asm`」
   是**同类风险**。CI 上二者同时跑，理论上可能复现该竞态导致 gate job 瞬时误报。
   ⇒ **建议（留 621）**：给 CI 的 `gate` job 加 `needs: [replay]` 或给 replay 改为
   原子替换写文件，从根上消除竞态。本批不改 CI（属基础设施决策，交人）。
4. 620 未 push（硬边界 6），故本批次交付物**均未经 CI 实跑**。
