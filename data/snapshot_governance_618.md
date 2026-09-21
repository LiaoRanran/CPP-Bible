# SNAPSHOT 数字治理方案（618 D1）

> 响应 617 外部评审 #6/#7（数字漂移 / 计数手填）。本方案定义 `SNAPSHOT_MANIFEST` 的治理规范，使所有对外计数单一源、可复算、不可手填。

## 一、现状
- 617 D2 落地 `tools/snapshot_manifest.py` + `data/SNAPSHOT_MANIFEST_617.json`；D4 落地 `data/project_key_numbers_quickref_20260921_v7.md`（manifest 派生，废弃手填 v6）。
- 实测漂移：v6 写 tools 204 / tests 183；周边 PM 报告写 196 / 175；git 实值 tools 218 / tests 213。治理后统一以 manifest 为准。
- 问题：manifest 文件名带 `617` 后缀，后续批次（618/619…）若各自生成 `*_618.json`，会再次分裂计数源。

## 二、核心规范（铁律）
1. **单一 manifest**：收敛到**唯一** `data/SNAPSHOT_MANIFEST.json`（不带批次号）；批次后缀文件（如 `_617.json`）仅作历史快照，不再生成新批次后缀版本。617 工具可改名/合并到该唯一文件，或保持 `snapshot_manifest.py` 但输出固定为 `SNAPSHOT_MANIFEST.json`。
2. **计数源唯一**：README / qmd / quickref / PM 报告中的 commit/tools/tests/atoms/EV 计数，**必须**引用 `SNAPSHOT_MANIFEST.json` 的 `live_counts`，禁止手填任何数字。
3. **可复算**：manifest 由 `git rev-list --count HEAD` + filesystem 直取，任何人在本地重跑 `tools/snapshot_manifest.py` 即得相同计数（HEAD 一致时）。
4. **冻结数字单独标注**：验证基线数字（gate/poison/replay/mutation/confidence/human_review/independence/trust_root）放入 `verification_baseline_frozen` 段，标注 `last_verified` 与来源；重跑须走监工门禁，工具不跑。
5. **重指向历史手填**：`data/project_key_numbers_quickref_20260921_v6.md` 及 34/33 等 PM 报告中的手填计数，统一加注"已废弃，以 SNAPSHOT_MANIFEST.json 为准"，后续修订时删除手填行（低优先）。

## 三、与 617 工具的关系
- `snapshot_manifest.py` 的输出目标改为 `data/SNAPSHOT_MANIFEST.json`（本次批次可选；建议 619 收敛）。
- quickref v7 改为引用 `SNAPSHOT_MANIFEST.json` 而非 `_617.json`。
- C2/C4 的测试计数（`test_category_map.json`）也应以 manifest 的 `live_counts.tests_py` 为基准校验（CI 一致性门）。

## 四、防回归
- CI 新增"manifest 一致性"门（见 D3）：每次 PR 校验 manifest 的 `live_counts` 与当前 git/filesystem 重算一致，且 `head_commit == HEAD`；不一致则失败（catch 手填/漂移）。
- 禁止直接 `git commit` 修改 manifest 的 `live_counts` 数字段（工具生成是唯一写入路径）。

## 五、交付清单（本批）
- 本方案文档（D1）。
- 实际收敛（重命名/改输出目标）留待 619（避免本批触碰 617 已入库文件 `SNAPSHOT_MANIFEST_617.json` 的引用关系，稳妥起见先在文档锁定规范）。
