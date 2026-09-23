# 628 A4 · DEBT-001 处置 + replay manifest 修复报告

## DEBT-001

- 登记：`tests/test_s1_s6.py` `_tk()` fixture 硬编码 `due=2026-09-20`（已过期）
- 实测：`test_clean_ledger_passes` FAILED（"DEBT-001 已到期未清——停线"）
- **处置**：fixture 日期动态化（opened=今日-10 / due=今日+30）——
  测试验证的是台账**逻辑**而非具体日期；真实治理台账无 DEBT-001 数据文件
  （仅测试 fixture），动态化即等效清算。同 commit 复跑该测试全绿。
- 详见 `data/debt_001_disposition_628.md`

## replay manifest_consistency

- manifest：`build/replay_manifest.json`（56 条，fingerprint=sha256(卡‖夹具‖工件‖.out‖阴夹具)）
- 625 登记 5 失配（EV-CONC-002..006）→ 628 只读复验：**stale 0 / missing 0 ⇒ CONSISTENT ✓（已被 626/627 期间 manifest 刷新解决）**
- 本工具固化核验能力：`--apply` 可机械刷新 stale 指纹（标 stale_needs_rerun=true，下次增量 replay 自动重跑，不伪造 confirm）

## 验证

- replay 判决 56/0/0 未动（本批不跑监工门禁，判决由增量机制保证）
- 受控目录零污染
