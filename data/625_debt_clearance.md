# 625 E1 · 化债与遗留项处理

> 本批定位「修债务+稳雷2+备雷1」。本节汇总本批已化债项、对 622/623/624 遗留项的处理结果，以及**仍留 626** 的债。

---

## 一、本批已化债（P0）

| 债项 | 来源 | 处理 | 结果 |
|---|---|---|---|
| mypy 67 处存量债（24 文件） | 620-623 被 ruff 掩盖 | 625 A1 注解/cast/判空/重命名 | **0 errors** ✅ |
| OTS anchor 过期 | 624 信任根重钉致 anchor 失配 | 625 A2 re-anchor（pending 未上链，诚实标注） | `--check` ✅ |
| CI pytest 红因 | 治理 manifest 待重签 + 581 计数硬编码 | 625 A3 重签 + 计数动态化（27/67/backed28） | not-slow 段全绿 ✅ |
| 尺子入根 22 | 完整性根覆盖不足 | 625 D1 `RULER_TOOLS` 10→22（总量 34） | `tool_integrity --check` ✅ |
| 路径写死（核心 6 + 辅助 20） | QueYi Core 剥离阻塞 | 625 C1 `PathConfig` 接入 | 向后兼容 ✅ |
| 3 个 CLI 缺 `--check` | 收工门禁不可机验 | 624 D1（本批前）已补 | 3/3 exit0 |
| 豁免治理硬编码 27 | 624 新增豁免后口径错 | 624 D3 动态化 | ✅ |

## 二、622/623/624 遗留项处理状态

| 遗留项 | 原登记批 | 本批处理 |
|---|---|---|
| 触达天花板（>45/63、盲区<25） | 623/624 | **未达**（编译/复算/git/词表盲区跨卡亦不可达）；策略留 626（多卡/编译门载体） |
| E2 4 条 block 规则接线 | 623→624 | 624 B1 已接线（63→67，基线 0 误报）；625 B-line 验证稳定 |
| 8 原子 UNRESOLVED→IN 认可 | 623 D2 | 已落地（W2 重算）；本批未改 |
| E1 PCK authorized >48% | 624 | **未达**（机器候选 0；瓶颈=56 证据证人审缺失）；625 D4 已设计策略，待人审 |
| E2 110 条人审执行 | 624 | **未执行**（不代签）；625 D2/D3 已备可视化+执行框架 |
| mypy 存量债 | 620-623 | **已化**（A1） |
| OTS re-anchor | 624 | **已化**（A2） |
| CI pytest 红因 | 624 | **已化**（A3，not-slow 全绿） |

## 三、仍留 626（诚实登记）

1. **replay `manifest_consistency` 5 处指纹失配**：evidence 卡内容与 stale manifest 不符（存量债，非本批引入）。
2. **`DEBT-001` 债务台账过期**：治理债务 ticket 到期，需人决续期/关闭。
3. **触达天花板**：需在载体层（多卡/编译/复算/git）突破，非单卡 field-edit 所能及。
4. **E1 PCK 提升**：需走 625 D4 策略 + D3 框架由人执行 30+ 证据证人审。
5. **E2 110 条人审执行**：由人走 D2/D3 框架完成。
6. **CI `quality`(mypy)/`pytest`(slow 段) 仍红**：slow 段 replay/581 已修，但 replay manifest_consistency + DEBT-001 需在 626 立项清理；且远程 CI 自 625 起**未 push**（铁律 625 不 push）。
7. **PathConfig 余量**：~110 辅助工具 + tests/ 仍写死路径，留 626 补全（触发标准⑤）。

## 四、验证

- `ruff check tools/ tests/` → All checks passed
- `mypy tools/` → 0 errors
- `pytest -m "not slow"` → 全绿（A3 后）
- `tool_integrity --check` → Merkle 根一致、尺子 34/34 一致
- `run_624_gate.py --skip-tools` → 收工门禁 PASS（详见 F1）
