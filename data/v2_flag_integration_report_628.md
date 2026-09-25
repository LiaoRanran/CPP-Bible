# 628 A1 · V2 flag 接入验证报告

## 接入前状态
- `v2_enabled()` 已定义（L46-47）但**全文件无调用点**——flag 是概念开关。
- compile_w2 无条件走 ledger edge 粒度（519 节点）。

## 接入位置与逻辑
- `__init__`：`self.v2_mode = v2_enabled()`（编译时读取一次）。
- `compile_w2()`：V1 → `_compile_w2_v1()`（legacy grounded_labels，121 节点）；V2 → `_compile_w2_v2()`（ledger + 627 A1 归一化，121 节点）。
- 输出 schema 不变（dict[node]→label）；PCK/golden/dashboard/textbook 保持 authority-driven（626 前无 legacy 等价物，诚实登记）。
- **偏差项登记**：626 测试 `test_w2_projection_vs_grounded_labels_deviation_registered` 锁定 `len(w2)!=121`（当时偏差存在）——A1 落地后偏差被解决，该测试同 commit 更新为对齐断言；`test_empty_ledger_handled` 适配双模式。

## V1 vs V2 对比
- V1（flag=0）：nodes=121 summary={'IN': 79, 'OUT': 42, 'UNDEC': 0}
- V2（flag=1）：nodes=121 summary={'IN': 79, 'OUT': 42, 'UNDEC': 0}
- 逐节点标签一致：True

## 回归验证
- 默认（未设置）= V1：True
- CORE_TOOLS 读 flag 的文件：无
- tool_integrity --update 已重钉：True

- **总判定**：FAIL ❌
