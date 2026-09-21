# 614 C1：OTS 真实上链可行性评估

> 铁律：不改受控目录；诚实标注；**不臆造"已上链"**。评估时间 2026-09-21。

## 一、当前状态（实地核验）
| 项 | 实测值 | 结论 |
|---|---|---|
| 文件 | `data/supply_chain/merkle_roots.json.ots`（131 B） | 存在 |
| 魔数头 | `00 4f 70 65 6e 54 69 6d 65 73 74 61 6d 70 73 00 00 70 72 6f 6f 66 00 ...` | ✅ 与真实 OTS magic 一致 |
| 生成方式 | `tools/opentimestamps_anchor.py::build_ots`（**本地序列化，不 submit**） | 结构化占位 |
| attestation 段 | **占位零**（32B 全 0） | ⚠ **pending** |
| .ots 内 digest == 文件 digest | ✅（`47c330c9…6e0db5`） | 绑定成立 |
| 判定 | **pending（未上链）** | **不是**时间戳证明 |

⇒ 现状与 613 报告 `data/ots_anchor_613.md` 一致：**可证明「该 .ots 绑定此摘要」，不能证明「此摘要在某时刻已存在」**。

## 二、真实上链可行性（实测）
| 前提 | 实测 | 结论 |
|---|---|---|
| 日历服务器网络可达 | `https://a.pool.opentimestamps.org` → **HTTP 200** | ✅ 可达 |
| `ots` CLI 客户端 | `Get-Command ots` → **NOT FOUND** | ❌ 缺 |
| `python-opentimestamps` 库 | `import opentimestamps` → **ModuleNotFoundError** | ❌ 缺 |
| 出块等待 | 比特币平均 10 min/块，日历聚合 + 确认窗口 ~1–2h | ⏳ 需等待 |

⇒ **技术可行**（网络通），但需先装客户端、再等待出块。

## 三、为何本批**不自动执行**（诚实障碍清单）
1. **交人项**：609 铁律第 9 条 / 613 报告明确「**不实际上链**」，真实 `submit` 已定为**人类执行项**。
2. **不可逆外部副作用**：向公共 OTS 日历**发布**信任根哈希是外发动作，需人授权（本批未授权外发）。
3. **出块等待**：`ots upgrade` 需等比特币出块（~1–2h），超出本会话时限。
4. **门禁解释器污染风险**：`.venv` 为门禁唯一可信解释器，装 OTS 客户端可能引入依赖漂移。
5. **失败代价**：手搓 OTS 提交/序列化若出错，会产出**非法 .ots**，比"诚实的 pending 占位"更糟。

## 四、交人执行 Runbook（精确命令）
```bash
# 1) 装客户端（提供 ots CLI）
pip install opentimestamps-client
# 2) 提交到日历（生成真实 pending 回执，写入 .ots）
ots stamp data/supply_chain/merkle_roots.json
# 3) 等待 ~1–2 小时（比特币出块）
ots upgrade data/supply_chain/merkle_roots.json.ots
# 4) 验证
ots verify data/supply_chain/merkle_roots.json.ots
# 5) 回仓复核（回填后 pending 列应转 confirmed）
python tools/ots_anchor_613.py --check
```
> 注：`ots stamp` 会**覆盖**当前占位 .ots；若信任根 `merkle_roots.json` 之后发生变更，须重新 stamp（旧证明作废）。

## 五、结论
- **当前状态**：`pending`（占位零，未上链）——诚实、可核验、不被误用。
- **真实上链**：**技术上可行**（网络可达），但受制于「交人项 + 外部发布授权 + 出块等待 + 解释器卫生」，
  本批**不自动执行**；障碍已逐项记录。
- **后续**：由人按第四节 Runbook 执行；届时 C3 的 `trust_root_status_check` 与 613 报告的 pending 列自动转 ✅。

## 六、诚实边界
- 未安装 OTS 客户端、未向任何公共日历提交、未修改 `data/supply_chain/*.ots`。
- 网络探针仅为**只读** GET（HTTP 200），未产生任何发布副作用。
