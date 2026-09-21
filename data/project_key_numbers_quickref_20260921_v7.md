# 项目关键数字 quickref（v7 · 617 D4/G2 · 由 SNAPSHOT_MANIFEST 直取，禁止手填）

> **来源**：`data/SNAPSHOT_MANIFEST.json`（工具 `tools/snapshot_manifest.py` 生成；619 C1 收敛后的**权威**快照，generated_at 见该文件。历史版本化归档 `SNAPSHOT_MANIFEST_617.json` 仍保留为冻结 pin）。
> **铁律**：本表计数全部由 git/filesystem 直取，**禁止手写**；v6（手填 204/183/196/175）已废弃，存在漂移，勿再引用。
> 重跑验证数字须走监工门禁；本表 frozen 段为冻结数字（last_verified 见 manifest）。

## 一、实时计数（live_counts，可复算）
| 指标 | 值 | 获取方式 |
|---|---|---|
| 总 commit 数 | **1517** | `git rev-list --count HEAD` |
| tools/*.py 数 | **218** | filesystem 直数 |
| tests/*.py 数 | **213** | filesystem 直数 |
| atoms/*.md 数 | **28** | filesystem 直数（recursive）|
| evidence EV-*.md 数 | **56** | filesystem 直数（recursive）|
| HEAD commit | `66328df4b60e85c439e447e8059a62c789dc6b64` | `git rev-parse HEAD` |

> 漂移对照：v6 写 tools 204 / tests 183；README 周边文档写 196 / 175；本表实测 218 / 213。一切以本 manifest 为准。

## 二、冻结验证数字（verification_baseline_frozen）
| 维度 | 值 |
|---|---|
| gate 规则/命中 | 63 / 191（block 0 / warn 186 / advice 5）|
| poison | 124/124 通过；表观 63/63；诚实 60/63 |
| replay | confirm 56 / refute 0 / infra_error 0 |
| mutation v7 | 1593/1405/1/179/8/1406；逃逸契约 1/1406 |
| 置信序列 | CP 单侧 0.3370% / CS anytime 0.9062% |
| 人审 | 388（approve 354 / modify 34 / reject 0；batch_auth 388 / mirror 194）|
| 独立性 | verifier 1；第二实现 1/63；离散 L1；连续 scalar 0.153 |
| 信任根 | partially_anchored（OTS 未真上链 / in-toto hmac 非标准）|

## 三、六维度评分（616 后，取自 36 号 PM 报告）
- 综合 ≈ **8.4 / 10**（机械 9.2 / 人审 7.8 / 论证 7.6 / 信任根 8.9 / 度量诚实 8.6 / 知识资产 7.6）。
- 最大短板：人审（388=全 batch_authorization，194 mirror，逐条独立语义审查 0）。

## 四、已知债务（610 后，可能已过期，见 617 收工 F3）
学习者镜像门未开 / M1 TCE 未根治 / oracle 未校验 / 活性锚落卡 / modify 口径未定 / OTS 真上链未做 / in-toto 真签名未做 / 数字漂移（本表已治理）。
