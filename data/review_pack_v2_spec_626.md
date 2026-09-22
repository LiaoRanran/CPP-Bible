# 626 E2 · Review Pack v2 规范（两层包）

> 工具：`tools/review_pack_v2_626.py`（纯标准库，`--check` 自检）
> 判据：13（外部 Review Pack 可以独立复核至少一个完整 item）

---

## 一、为什么分成两层

外部大模型指出：现有包是「治理决策摘要包」，不是完整证据包。一层包无法同时满足
「小到可以快速浏览」和「全到可以独立复核」——所以拆成两层：

| 包 | 目的 | 体积 | 能否据此下判决 |
|---|---|---|---|
| **Review Pack** | 治理决策摘要 + 审查调度 | 小（~55 KB） | ❌ 只够调度与提问 |
| **Evidence Pack** | 对指定 item 打包最小充分证据 | 按 item 数（Top10 ~24 KB） | ✅ 最小闭环审查 |

## 二、Review Pack 内容

| 文件 | 内容 |
|---|---|
| `00_README.md` | 包定位 + 内容索引 + 血缘（git_sha / 93 unique / 独立确认强度） |
| `01_review_items.json` | **93 个唯一**待审 item（不是 110 条记录） |
| `02_decision_points.md` | 8 大决策点（需人裁决） |
| `03_authority_summary.md` | Authority Ledger 摘要（452 events / 分布 / 独立确认强度 0） |
| `04_w2_summary.json` | W2 投影摘要 |
| `05_pck_summary.json` | PCK 状态摘要（严格/宽松双策略） |
| `SNAPSHOT_MANIFEST.json` | git_sha + dataset_sha256 + generated_at |

## 三、Evidence Pack 内容

- `items/<review_item_id>.json` —— 每个 item 的结构化数据
- `pages/<review_item_id>.html` —— **最小闭环审查页面**（一屏看全）
- `SNAPSHOT_MANIFEST.json`

### 最小闭环审查页面（HTML）

一屏内包含：
- review_item_id / status / 歧义度 / 优先级 / 来源批次
- target_type / target_id / review_revision
- **`symmetry_proof_id`**（未验证时显示 `null（未验证）`）
- **当前 Authority 决定**：result / review_method / decision_origin / event_id

> 深色科技风、自包含（无外部依赖）、不需跳转到其他文件即可形成判断所需的核心信息。
> 完整 evidence / negative test / replay 仍需对照仓库 `evidence/`、`build/`（已如实标注）。

## 四、核心改进（相对旧包）

| 改进 | 实现 |
|---|---|
| **自动生成** | 脚本打包，不再手动 |
| **跨平台** | 路径分隔符统一 `/`（`zipfile.ZipInfo` 显式写入） |
| **控制字符清洗** | 写入前对文本文件清洗（0x00-0x1F 除 \n\r） |
| **SNAPSHOT_MANIFEST** | 绑定 git_sha + dataset_sha256 + generated_at |
| **最小闭环页面** | 每个 item 一屏看全核心信息 |

## 五、实跑产物（桌面）

| 包 | 路径 | 大小 | 内容 |
|---|---|---|---|
| Review Pack v2 | `阙疑_ReviewPack_v2_20260922.zip` | 55,515 B | 7 entries |
| Evidence Pack Top10 | `阙疑_EvidencePack_Top10_20260922.zip` | 23,618 B | 10 items + 10 HTML |

两者 `--validate` 均通过：`backslash=0 / has_manifest=True / control_chars=0 / bad_crc=None`。

## 六、CLI

```bash
python tools/review_pack_v2_626.py --check                     # 自检
python tools/review_pack_v2_626.py --generate-review            # Review Pack
python tools/review_pack_v2_626.py --generate-evidence --top 10 # Evidence Pack Top10
python tools/review_pack_v2_626.py --generate-evidence --items <id1,id2>
python tools/review_pack_v2_626.py --validate <zip>
```

## 七、验证

- `--check` → PASS
- `tests/test_review_pack_v2_626.py` → 9 例全绿
- 桌面两个包均生成并通过验证
