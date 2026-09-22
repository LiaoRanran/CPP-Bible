# 626 A4 · 人审决策包小问题修复 + v2 重新打包

> 说明：决策包实体位于仓库外（`C:\Users\ASUS\Desktop\阙疑_人审决策包_20260922\`），
> 不入库。本文档为**仓库内可见的修复记录与验证结果**。

---

## 一、README 修复（4 项）

| 项 | 修复前 | 修复后 |
|---|---|---|
| 文件数/大小 | 手填"约 1.5MB" | **36 文件 / 解压后 770.7 KB（789,186 B）**，由 `pack_review_zip.py` 自动取值并写入 README 尾部「包内实际统计」表 |
| 唯一待审项 | "110 条" | **93 个唯一 item**（记录 110，含 17 条重复）——626 A1 修正并加说明 |
| 总豁免 | "27 条 legacy" | **31 条 = 27 legacy + 4 HC**——626 A1 修正并加说明 |
| 30 条口径 | 视为"逐条人审" | **USER_AUTHORIZED_EXECUTION，不计独立人审，强度仍 0**——626 A3 修正 |

### 新增三节

1. **「〇、包定位」**——明确本包是**治理决策摘要包 + 审查调度包**，**不是完整证据包**；
   与 Evidence Pack 的对比表；说明"只够调度，不够独立复核"。
2. **「包内未包含的关键文件」**——列出 7 类缺失项（atoms/*.md、evidence/*.md、tools/*.py、
   build/replay_manifest.json、data/mutation/、Examples//Book/、完整 git 历史），
   并注明 `authority_log.jsonl`（262 KB < 500 KB）**已加入包内**（外部发布前按需脱敏）。
3. **「外部审查建议流程」**——6 步：读定位 → 读 8 大决策点 → 按 **93 唯一 item** 排优先级 →
   索取 Evidence Pack → **盲审优先（Pass A 不看 AI 推荐）** → 回报 decision+reason+review_method。

## 二、authority_log.jsonl 入包

- 体积 **267,921 B（≈262 KB）< 500 KB** ⇒ 按任务要求加入包内
- 位置：`02_388条人审诚实化/authority_log.jsonl`
- ⚠ 该日志含审查者标识 `LiaoRanran`，**外部发布前需按需脱敏**（已在 README 标注）

## 三、v2 打包与验证

用 A2 的 `tools/pack_review_zip.py` 重新打包（正斜杠跨平台）：

| 项 | v1（原包） | v1_fixed（A2） | **v2（A4）** |
|---|---|---|---|
| entries | 36 | 37 | **38** |
| 路径分隔符 | `\`（36/36 反斜杠） | `/` | **`/`** |
| SNAPSHOT_MANIFEST | ❌ | ✅ | **✅** |
| authority_log.jsonl | ❌ | ❌ | **✅** |
| 控制字符 | 有 | 0 | **0** |

`pack_review_zip.py --check --zip …v2.zip` 结果：

```json
{"ok": true, "entries": 38, "backslash": 0,
 "has_manifest": true, "bad_crc": 0, "control_chars": 0}
```

SNAPSHOT_MANIFEST（v2）：

| 项 | 值 |
|---|---|
| generated_at | 2026-09-22T15:45:07Z |
| git_sha | `8dfec744f34390ea9a5bb4f0ce8f07522658e462` |
| file_count | 37（+ manifest = 38 entry） |
| uncompressed_bytes | 1,060,559 |
| dataset_sha256 | `8b7314cfb297394c70b3e4ad5a7d7598d8ed58c2803777574de85c73a8442c87` |
| path_separator | `/` |

## 四、产物路径

- `C:\Users\ASUS\Desktop\阙疑_人审决策包_20260922_v2.zip`（v2，含 A1-A4 全部修复）
- `C:\Users\ASUS\Desktop\阙疑_人审决策包_20260922_v1_fixed.zip`（A2 中间产物，仅修正分隔符）

## 五、遗留

- README 仍有历史章节引用旧口径处（已就地加标注，不重写历史）。
- 真正的"最小闭环审查页面"由 626 E2 的 Evidence Pack 提供（每个 item 一屏看全证据）。
