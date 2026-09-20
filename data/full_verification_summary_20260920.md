# 全量验证汇总报告（化债第三轮）

> 生成时间：2026-09-20 · 仓库 HEAD：6d8f37c

## 一、核心门禁（4/4 绿）

| 门禁 | 结果 | 关键数字 |
|---|---|---|
| tool_integrity --check | ✅ exit 0 | core 5 + test_config 2 + supply_chain 5 一致 |
| gate_engine --check | ✅ exit 0 | 63 规则 / 191 命中 (block=0 warn=186 advice=5) |
| poison_drill | ✅ exit 0 | 124/124 · RULE-COVERAGE 39/63 · 表观100% · 诚实95.2% |
| atom_evidence_replay --check | ✅ exit 0 | confirm=56 refute=0 infra_error=0 |

## 二、只读验证工具（全绿）

| 工具 | 结果 | 关键数字 |
|---|---|---|
| prop_closure cross-check | ✅ | 79/79 双实现一致 |
| prop_closure stats | ✅ | 79命题/27卡/274边/26连通分量/闭包avg6.076 |
| prop_network_inventory --check | ✅ | 台账与事实源一致（151行） |
| overturned_events check | ✅ | 通道合法，0 条事件 |
| governance verify | ✅ | manifest 一致（457+文件） |
| governance scan | ✅ | high=55 medium=186 low=38 |
| ruff check | ✅ | All checks passed |

## 三、测试（子集全绿）

- test_governance_doc_guard_591.py + test_merkle_integrity_601.py：36 passed ✅

## 四、本轮化债成果

1. governance chore：manifest 登记 _arch_v2/v11 等 60 处 + scan 刷新 + Merkle 根重建 + 校验和重钉
2. governance high=55 语义分类报告：全部为历史文档描述性内容，非真实攻击指令（辅助 M15 人审）
3. _arch_v18 调研产品经理摘要：D5 学习者镜像是下一个跃迁（第 30 份导航文档）
4. 导航总索引更新：加入第 30 份文档，计数 30→31
5. _adv_v80/ CRLF 假脏恢复（34+1 文件）
6. .git/index.lock 残留锁删除

## 五、仓库状态

- 工作区：干净
- 远程：已同步（GitHub LiaoRanran/CPP-Bible:master）
- 六维度平均：8.1/10（机械9.2/信任8.5/度量8.5/人审7.8/论证7.0/知识7.5）
- v7 变异基线：1593/1405/1/179/8，契约 1/1406，C-P95 上界 0.40%
- 人审：388/388 全量完成（354 approve / 34 modify / 0 reject），W2 IN114/OUT7
