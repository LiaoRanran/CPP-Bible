# 620 D3 · 工具命名规范评估

> 目标：评估 `tools/` 命名一致性，给出规范建议 + 迁移成本，供人拍板。

---

## 一、现状盘点

```powershell
(Get-ChildItem tools/*.py).Count                                  → 240
(Get-ChildItem tools/*.py | ? Name -match '_\d{3}\.py$').Count    →  41
(Get-ChildItem tools/*.py | ? Name -match '^_').Count             →   1
```

| 命名形态 | 示例 | 数量 | 评价 |
|---|---|---|---|
| **批次后缀型** `xxx_NNN.py` | `gate_engine.py` 之外的 `vfdr_619.py`、`pck_renderer_619.py`、`metrics_613.py` | **41** | ✅ 可溯源批次，但**只有 17%** |
| **无批次后缀（稳定名）** | `gate_engine.py`、`poison_drill.py`、`atom_evidence_replay.py`、`snapshot_manifest.py` | ~198 | ⚠ 无法从名字看出诞生批次 |
| **批次前缀型** `NNN_xxx.py` | `612_baseline.py`、`613_baseline.py` | 2 | ❌ 与后缀型不一致 |
| **下划线前缀（内部）** `_clean_junk.py` | 1 | ⚠ 私有/临时语义不明 |

**620 新增命名**（均遵循批次后缀型，一致）：
`adversarial_loop_620.py`、`adversarial_weight_calibration_620.py`、`vfdr_realtime_620.py`、
`pck_batch_migrator_620.py`、`pck_status_stats_620.py`、`authority_log_620.py`、
`pck_authority_sync_620.py`（+ E1 的 `run_620_gate.py`）

---

## 二、问题诊断

1. **双轨制**：同一类工具有的带批次后缀（619/620 系），有的不带（`gate_engine`）。
   不带后缀的多是**核心/长期**工具（CORE_TOOLS），带后缀的多是**批次产物**——
   这个区分**有实际意义**，但从未写成规范，导致边界模糊（如 `snapshot_manifest.py`
   无后缀但会被批次改动）。
2. **前缀/后缀混用**：`612_baseline.py`（前缀）vs `metrics_613.py`（后缀），纯属历史偶然。
3. **无统一动词表**：`generator` / `migrator` / `renderer` / `stats` / `verifier` /
   `sync` / `log` 混用，同类职责命名不统一。

---

## 三、建议规范（供人拍板，620 不强制落地）

```
<domain>_<action>_<batch>.py        批次产出的新工具（强制带 _NNN）
<domain>_<action>.py                晋升为长期/核心工具后可去掉批次后缀
_NNN_<name>.py  或  _<name>.py      仅内部/临时脚本，下划线前缀
```

**动词表建议**：`generator` / `migrator` / `renderer` / `verifier` / `stats` /
`sync` / `log` / `calibration` / `realtime` —— **同类职责用同一个词**。

**规则**：
- **新批次工具一律带 `_NNN`**（620 已执行）；
- **CORE_TOOLS 永不改名**（在 `tools/golden_state.json` / `tool_integrity` 基准里钉死）；
- 工具**晋升为核心**时（被 CI 长期引用、跨批次复用）才去掉批次后缀，且需同步改所有引用。

---

## 四、迁移成本评估（关键）

实测：41 个 `_NNN` 工具**全部**被其他文件引用；引用文件累计 **318 处**
（`tools/` `tests/` `.github/` `data/` 下的 .py/.md/.yml）。

| 成本项 | 量级 | 说明 |
|---|---|---|
| 需改名的工具 | 41 | 全部有外部引用 |
| 需改的引用处 | **318** | 含 `ci.yml` 里的工具路径、**跨工具 import**、单测 import、文档引用 |
| 高风险点 | CI 硬门禁 | `ci.yml` 直接写 `python3 tools/gate_engine.py` 等；改名漏改 = CI 静默失效 |
| 历史可追溯性 | 受损 | 旧批次报告引用旧工具名，改名后**报告与代码对不上** |

**结论：全量改名成本 ≫ 收益。**

---

## 五、620 的建议（不代决）

1. ✅ **新批次强制带 `_NNN`**（620 已全部执行，零成本）。
2. ❌ **存量 41 个工具不改名**：318 处引用 + CI 硬门禁风险 + 历史报告脱钩，
   收益（美观）远小于风险（静默破坏门禁）。
3. ⚠ **2 个前缀型**（`612_baseline.py` / `613_baseline.py`）**也不动**——
   它们是冻结基线数据工具，改名同样有引用成本，且名字本身已足够表意。
4. 📌 **把"新工具必须带批次后缀"写进 CONTRIBUTING / 铁律**，从 621 起固化。
5. 📌 **CORE_TOOLS 名单**（`tool_integrity` 基准里的 5 个）**永久冻结命名**，
   任何改名提案须走监工门禁。

---

## 六、诚实登记

- 本评估**未实际执行**任何改名（620 硬边界：不改 CORE_TOOLS，且改名需人拍板）。
- 318 处引用为**文件级**计数（同一文件引用多个工具会重复计），
  实际需编辑的行数可能更高；此处仅作量级估计，非精确工数。
- 「晋升为核心后去批次后缀」的具体判定标准（谁有权判定）**未定义**，留 621+。
