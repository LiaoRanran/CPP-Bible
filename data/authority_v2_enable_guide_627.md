# 627 B3 · Authority V2 启用 / 回滚指南

## 一、声明（重要）
- V2 是 **Authority 单一真源** 驱动的只读投影层（W2/PCK/golden/dashboard/textbook）。
- 627 B1 已验证：**5 种投影在 V2 模式下全部成功运行**。
- 627 B2 已验证：**CORE_TOOLS 完全隔离 V2 flag/工具，启用无回归风险**。
- **启用需人确认（交人项 #1）**：本工具不替人自动开启生产路径。

## 二、启用步骤
```bash
# 1) 记录启用意图（仅写 data/authority_v2_mode.json，不修改任何代码/数据）
python tools/authority_v2_switch_627.py enable

# 2) 让模式真正生效（读模式文件 → 设置环境变量 → 调 626 编译器）
python tools/authority_v2_switch_627.py run w2

# 或在 shell 中直接导出（对所有子进程生效）
export QUEYI_AUTHORITY_V2=1
```

## 三、回滚步骤
```bash
python tools/authority_v2_switch_627.py rollback   # 模式置回 false
export QUEYI_AUTHORITY_V2=0                          # 或直接在 shell 关闭
```
- 回滚**零副作用**：V2 是纯增量只读投影，不影响原始 ledger / 受控目录。

## 四、验证清单（启用前建议确认）
1. B1 端到端：5 种投影 V2 全部成功 ✅
2. B2 回归：CORE_TOOLS 隔离 ✅
3. 627 A1：W2 归一化 121 节点 diff=0 ✅
4. push 后由远程 CI 实跑 gate/poison/replay（交人项 #3）

> 本指南与脚本**不修改 626 工具、不修改受控目录**；开关仅由人在本地掌控。
