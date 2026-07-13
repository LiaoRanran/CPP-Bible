# Memory — 项目记忆系统

> 与 workbuddy 外部 memory/ 独立。本项目级记忆仅在 CPB 仓库内生效。
> 作用：checkpoint、决策记录、架构演进日志。

## 文件结构

```
memory/
├── README.md            # 本文件
├── ARCHITECTURE.md       # 架构决策记录
├── checkpoints/          # 每日 checkpoint（自动生成）
│   └── 2026-07-09.md
└── decisions/            # 重大技术决策
```

## Checkpoint 格式

每次 `make.bat full` 通过后自动生成（未来版本）。
当前手动记录到 `checkpoints/YYYY-MM-DD.md`。

## 与 workbuddy memory/ 的关系

| 维度 | workbuddy memory/ | 项目 memory/ |
|---|---|---|
| 位置 | ~/WorkBuddy/.workbuddy/memory/ | CPP-Bible/memory/ |
| 范围 | 跨项目、跨会话 | 仅 CPB 项目 |
| 受众 | Hy3 & user | 所有 CPB 贡献者 |
| 内容 | 每日工作日志 + 总结 | checkpoint + 架构决策 |
