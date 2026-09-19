# 12 · 本仓落地路径（NDW 分类）

## 12.1 关键路径（综合维度 1–11）

```
N1 人审标注 CLI (prop_graph query --pending-attack-edges)   [N, 扩展 566]
N2 标注数据文件 data/human_annotations.jsonl (append-only)  [N]
N3 grounded 可视化报告 (本探针 visualization/index.html)      [N, 已完成原型]
   │
   ▼
D1 42 组 MIS 人审确认 (群组级, ~25min)                       [D, 人时]
D2 反馈闭环 (拒绝→生成器/权重更新→W2重算)                    [D]
   │
   ▼
W1 Web 人审界面 (悬停/拖拽/实时重算)                         [W, 需前端]
W2 多模型辅助复核 (异族 API 集成)                            [W, 需 API]
W3 主动学习 ML (不确定性采样)                                [W, 需模型]
```

## 12.2 NDW 分类

- **N（现在能做，零 Oracle 风险）**：
  - 人审 CLI 视图（`--pending-attack-edges`）
  - `data/human_annotations.jsonl` schema + 读写
  - 可视化原型 HTML（本探针已生成）
  - W2 重算钩子（594 已证 <0.5ms）
- **D（攒数据）**：
  - 42 组 MIS 人审确认（维度 5：~25min）
  - 人审理由库 / 陷阱题设计（维度 2/3）
  - 反馈闭环规则（维度 9）
- **W（等条件）**：
  - Web 界面（前端框架）
  - 多模型辅助复核（异族 API，且警惕 common-mode failure，维度 7）
  - 主动学习 ML（模型）

## 12.3 每步前置条件与验收标准

| 步 | 前置 | 验收标准 |
|---|---|---|
| N1 | 无 | `query --pending-attack-edges` 返回 42 组待审 |
| N2 | N1 | 提交写入 jsonl，含 6 必备字段 |
| N3 | 无 | 打开 index.html 可见 IN/OUT 图 |
| D1 | N1+N2 | 42 组全审完；agree_rate<1.0（非 rubber-stamp）；理由非空 |
| D2 | D1 | 跑完一轮后，生成器下轮拒绝率下降 |
| 上线 | D1+D2 | 零误伤率=0；退化指数<0.9 |

## 12.4 一句话边界

**人审层已从"瓶颈"翻转为"可 ~25min 完成的群组级确认 + 自我减负的反馈闭环"。算法/可视化/接口均在 N 段就绪，落地只剩 D 段 42 组人审。**
