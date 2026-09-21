# 人审待办清单使用指南（618 E3）

> 配套 E2 生成的 `data/human_review_todo_30_618.md`。本指南说明如何填写与使用清单。

## 一、清单字段
| 字段 | 含义 |
|---|---|
| 序号 | 1–30 |
| 证据卡 | evidence/ 下的 EV-*.md（按路径排序取前 30）|
| 复核类型 | 固定为"逐项语义审查"（填补 615 缺口）|
| 镜像边 | 卡内容含"镜像/mirror/对称边"则为"是"（提示，非判定）|
| 状态 | pending（待人工填，可改为 approved/modified/rejected）|
| 裁决选项 | approve / modify / reject |

## 二、填写步骤
1. 打开 `data/human_review_todo_30_618.md`。
2. 逐行人工审查对应证据卡（在仓库中找到该 EV-*.md 阅读）。
3. 在该行"状态"列填：`approved` / `modified` / `rejected`；"裁决"列填理由（modified 须说明改动的证据）。
4. 不要修改"证据卡/复核类型"列（由工具生成）。

## 三、裁决语义
- **approve**：该证据卡独立语义上真支撑其 atom 主张，无修改必要。
- **modify**：证据卡需修正（如补齐活性锚、修正命题表述），并附修改说明。
- **reject**：证据卡不支撑或错误，须回退对应 atom 主张。

## 四、重新生成
- 若 evidence/ 新增/重命名卡，重跑 E2 工具刷新清单：
  `.venv\Scripts\python.exe tools/human_review_todo_generator_618.py`
- 重生成会覆盖 `human_review_todo_30_618.md`，已填写的裁决会丢失（工具只生成 TODO 模板，不保存裁决）。**裁决留痕请另存至交人项台账**。

## 五、纪律
- 本指南与清单工具**不代签任何裁决**；approve/modify/reject 权唯人。
- 清单为抽样（30 条），全量逐条复核是持续工程。
