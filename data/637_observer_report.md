# 637 · 系统体检报告（SelfObserver 自动生成）

> 生成时间：2026-09-25T09:25:45；重指标采集：是。

## 一、14 项指标

| 指标 | 当前值 |
|---|---|
| 规则数 | 67 |
| 工具数 | 423 |
| 测试数 | 422 |
| commits 数 | 1848 |
| pytest 失败数 | 1 |
| ruff 错误数 | 0 |
| mypy 错误数 | 0 |
| 接地率(%) | 35.8 |
| 击败器覆盖率(%) | 100.0 |
| taint=true 卡数 | 8 |
| 例外条款条目数 | 227 |
| 观察态规则数 | 67 |
| ahead 数 | 9 |
| 最近 5 commit | 5 条（见文末） |
| 观察态比例(%) | 100.0 |

## 二、最近 5 个 commit

```
1cc2c722 636 [E1]：_auto/status.json 更新为 636 收工(awaiting_review,last_completed_batch=636,next=637,last_commit=d846149b)+ outbox/636.md 完成报告
d846149b 636 [E1]：收工门禁+三份报告——run_636_gate PASS(8新工具--check 8/8+ruff+mypy 0/417文件+受控零污染+8交付齐备);生成636_acceptance_report/636_protector_shadow_report/636_next_steps;附修blind_protocol_636的mypy var-annotated;--check只读+6例单测
4132a883 636 [V26-补2]：四态判决模拟(影子)——36份baseline按pass/pass_with_exception/fail/unknown重分类:fail25/pass9/unknown1/带例外1;假pass=1(二态下算pass实为带例外);关键词启发式分类已登记;不改历史判决;只读+6例单测
dc48ebb7 636 [V26-补1]：污染传播自动追踪器(影子)——从635台账8张taint=true卡选ATOM-MEM-ALLOC-001,自动追踪下游引用清单+逐条三阀门(独立来源/必然发现/善意),产出tainted清单;不标taint不改判决;文本级引用图已登记;只读+6例单测
8db0f315 636 [2.5]：MDL边际判据试运行(影子)——admit⟺savings>L(rule),savings=触达轮数×50×log2(1593),L=8×len(id)+8×len(title)+32;67规则:admit30/reject37(通过率44.8%);豁免率趋势早期66.7%->近期23.5%(下降);未拦截新规则;编码长度启发式已登记;只读+6例单测
```

## 三、诚实登记

- 本报告**只读**，不修改系统任何状态；所有数值来自实测，非抄表。
